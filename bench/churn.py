"""Q3: how long after a permission change at the source do an arm's answers reflect it?

Per arm, `--events` changes alternate between a revocation and a grant, each on a chunk of its own:

- revoke: a chunk a measured user may read loses every reader;
- grant: a chunk nobody may read (made so beforehand, then left to settle) gains the user as a reader.

Each change is applied at every source in parallel, the way a sync job would: both engines (SpiceDB
and OpenFGA relationships) and the store's copy of the chunk's principals. The probe is the chunk's
own vector, so the chunk is among the top hits whenever the user may read it. The arm is asked every
`--every` seconds until its answer reflects the change, up to `--cap` seconds. The delay counts from
the last acknowledgement among the source writes; each write's own latency is recorded too, and so
is every probe (time since the acknowledgement, its own latency, whether it held the chunk).

    python -m bench.churn --workload data/dev --store pgvector --out results/churn.jsonl.gz [--events 20]

That is the registered protocol (`published`). The follow-up diagnostic (`prereg/addendum-1.md`,
`--plan diag-a` or `diag-b`) runs each arm under several variants, one after the other:

- `symmetric`: a pause of `--settle` seconds without queries before every change; a revocation as
  above; a grant to a chunk no user of the workload may read, or if there is none, to a chunk the
  probed user could never read, whose readers are removed before the pause;
- consistency `at_least_as_fresh` (the ZedToken of the change's SpiceDB write) or `fully_consistent`
  on every SpiceDB read of the arm (`arms.Freshness`), beside `default`, what the integration sends.

A variant's rows are named `<arm>:<protocol>[+<consistency>]` and carry `protocol` and `consistency`;
the published protocol at the default consistency keeps the arm's own name.
"""

from __future__ import annotations

import argparse
import asyncio
import random
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

from . import arms, engines, stores
from .arms import Context
from .engines import Tuple
from .run import environment
from .util import log, write_json, write_jsonl_gz
from .workload import Workload, principals

PUBLISHED = (("published", "default"),)
ENGINE_ARMS = ("a1-", "a2-", "a3-", "a7-")  # the arms that ask an engine at query time (as bench.faults)


def plan(store, name: str) -> tuple[list[str], list[tuple[str, str]]]:  # noqa: ANN001
    """The arms and variants of a diagnostic job (prereg/addendum-1.md, section 4.3)."""
    engine_arms = [a for a in arms.names(store) if a.startswith(ENGINE_ARMS)]
    if name == "diag-a":
        return engine_arms, [("published", "default"), ("symmetric", "default")]
    if name == "diag-b":
        spicedb = [a for a in engine_arms if "spicedb" in a or a.startswith("a7-")]
        return spicedb, [("symmetric", c) for c in ("default", "at_least_as_fresh", "fully_consistent")]
    raise ValueError(f"unknown plan {name!r}")


def label(arm: str, protocol: str, consistency: str) -> str:
    if (protocol, consistency) == PUBLISHED[0]:
        return arm
    return f"{arm}:{protocol}" + ("" if consistency == "default" else f"+{consistency}")


def _chunk_readers(w: Workload, i: int):  # noqa: ANN202
    for u in w.user_idx[w.user_ptr[i] : w.user_ptr[i + 1]]:
        yield Tuple("chunk", f"c{i}", "reader", "user", w.user_names[u])
    for g in w.group_idx[w.group_ptr[i] : w.group_ptr[i + 1]]:
        yield Tuple("chunk", f"c{i}", "reader", "group", w.group_names[g], "member")


def unreadable_by_all(w: Workload) -> np.ndarray:
    """Chunks no user of the workload may read: no reader named directly, and no group any user of any
    layout belongs to."""
    held = {g for layout in w.layouts for groups in layout.user_groups.values() for g in groups}
    gids = [i for i, g in enumerate(w.group_names) if g in held]
    readable = np.zeros(w.n, dtype=bool)
    readable[np.repeat(np.arange(w.n), np.diff(w.user_ptr))] = True
    readable[np.repeat(np.arange(w.n), np.diff(w.group_ptr))[np.isin(w.group_idx, gids)]] = True
    return np.flatnonzero(~readable)


class Sources:
    """The three places a permission lives, changed together."""

    def __init__(self, w: Workload, store, fga: dict) -> None:  # noqa: ANN001
        self.w, self.store, self.fga = w, store, fga
        self.spicedb = engines.spicedb_client()
        self.current: dict[int, list[Tuple]] = {}

    def readers(self, i: int) -> list[Tuple]:
        if i not in self.current:
            self.current[i] = list(_chunk_readers(self.w, i))
        return self.current[i]

    def apply(self, i: int, new: list[Tuple]) -> dict:
        old = self.readers(i)
        add = [t for t in new if t not in old]
        remove = [t for t in old if t not in new]
        store_principals = [f"u:{t.subject_id}" if t.subject_type == "user" else f"g:{t.subject_id}" for t in new]
        vector = np.asarray(self.w.vectors[i], dtype=np.float32)
        tokens: dict[str, str | None] = {}

        def timed(name: str, call) -> tuple[str, float, float]:  # noqa: ANN001
            start = time.perf_counter()
            tokens[name] = call()
            end = time.perf_counter()
            return name, end - start, end

        jobs = {
            "spicedb": lambda: engines.spicedb_change(self.spicedb, add, remove),
            "openfga": lambda: engines.openfga_change(self.fga, add, remove),
            "store": lambda: self.store.set_principals(i, store_principals, vector),
        }
        with ThreadPoolExecutor(max_workers=3) as pool:
            done = list(pool.map(lambda kv: timed(*kv), jobs.items()))
        self.current[i] = list(new)
        return {"write_s": {name: s for name, s, _ in done}, "acked_at": max(end for _, _, end in done),
                "zedtoken": tokens.get("spicedb")}


async def probe(run, user: str, groups: list[str], chunk: int, want_present: bool, acked_at: float, every: float,
                cap: float) -> dict:  # noqa: ANN001
    asked = 0
    log_: list[list] = []  # per probe: seconds since the acknowledgement, own latency, chunk held (None: error)
    while True:
        sent = time.perf_counter()
        try:
            hits = [h[0] for h in await run(user, groups, f"v{chunk}")]
            error = None
        except Exception as e:  # noqa: BLE001
            hits, error = [], f"{type(e).__name__}: {e}"[:200]
        asked += 1
        now = time.perf_counter()
        log_.append([round(sent - acked_at, 4), round(now - sent, 4), None if error else int(chunk in hits)])
        if error is None and (chunk in hits) == want_present:
            return {"delay_s": now - acked_at, "censored": False, "probes": asked, "probe_log": log_}
        if now - acked_at > cap:
            return {"delay_s": now - acked_at, "censored": True, "probes": asked, "last_error": error,
                    "probe_log": log_}
        await asyncio.sleep(every)


def _grant_target(rng: random.Random, nobody: list[int], mask: np.ndarray, used: set[int]) -> tuple[int, str]:
    """A chunk for a symmetric grant: one no user may read if any is left, else one this user may not read."""
    left = [i for i in nobody if i not in used]
    if left:
        return rng.choice(left), "unreadable-by-all"
    while True:
        i = rng.randrange(len(mask))
        if not mask[i] and i not in used:
            return i, "unreadable-by-user"


async def measure(ctx: Context, sources: Sources, names: list[str], events: int, seed: int, every: float,
                  cap: float, settle: float, variants: tuple[tuple[str, str], ...] = PUBLISHED,
                  budget_s: float = 0) -> list[dict]:
    rng = random.Random(seed)
    users = [(layout, u) for layout in ctx.workload.layouts for u in sorted({x for x, _ in layout.queries})]
    used: set[int] = set()
    rows = []
    order = list(names)
    rng.shuffle(order)
    tagged = tuple(variants) != PUBLISHED
    nobody = [int(i) for i in unreadable_by_all(ctx.workload)] if any(p == "symmetric" for p, _ in variants) else []
    deadline = time.monotonic() + budget_s if budget_s else None
    for name in order:
        for protocol, consistency in variants:
            ctx.consistency = None if consistency == "default" else arms.Freshness(consistency)
            arm = label(name, protocol, consistency)
            tags = {"base": name, "protocol": protocol, "consistency": consistency} if tagged else {}
            run = arms.build(name, ctx)
            for e in range(events):
                kind = "revoke" if e % 2 == 0 else "grant"
                if deadline is not None and time.monotonic() > deadline:
                    rows.append({"arm": arm, "event": e, "kind": kind, **tags, "skipped": "time budget"})
                    continue
                layout, user = rng.choice(users)
                groups = layout.user_groups.get(user, [])
                mask = ctx.workload.readable(user, groups)
                readable = np.flatnonzero(mask)
                pool = None
                if protocol == "symmetric" and kind == "grant":
                    chunk, pool = _grant_target(rng, nobody, mask, used)
                else:
                    candidates = [int(i) for i in readable if int(i) not in used]
                    if not candidates:  # recorded, so a skipped event is counted rather than lost
                        rows.append({"arm": arm, "event": e, "kind": kind, **tags, "layout": layout.name,
                                     "user": user, "skipped": "no chunk left to change"})
                        continue
                    chunk = rng.choice(candidates)
                used.add(chunk)
                if kind == "revoke":
                    if protocol == "symmetric":
                        await asyncio.sleep(settle)
                    change = sources.apply(chunk, [])
                    probe_groups, want = groups, False
                else:
                    if pool != "unreadable-by-all":  # published: the user's chunk; symmetric: emptied before the pause
                        sources.apply(chunk, [])
                    await asyncio.sleep(settle)
                    change = sources.apply(chunk, [Tuple("chunk", f"c{chunk}", "reader", "user", user)])
                    probe_groups, want = [], True
                if ctx.consistency is not None:
                    ctx.consistency.token = change["zedtoken"]
                result = await probe(run, user, probe_groups, chunk, want, change["acked_at"], every, cap)
                rows.append({"arm": arm, "event": e, "kind": kind, **tags, "layout": layout.name, "user": user,
                             "chunk": chunk, "write_s": change["write_s"], **({"grant_pool": pool} if pool else {}),
                             **result})
                log(f"{arm} {kind} c{chunk}: {result['delay_s']:.2f} s{' (censored)' if result['censored'] else ''}")
    ctx.consistency = None
    return rows


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--workload", type=Path, required=True)
    p.add_argument("--store", required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--events", type=int, default=20)
    p.add_argument("--seed", type=int, default=2)
    p.add_argument("--every", type=float, default=0.1)
    p.add_argument("--cap", type=float, default=60.0)
    p.add_argument("--settle", type=float, default=10.0)
    p.add_argument("--arms", default="")
    p.add_argument("--plan", default="", choices=["", "diag-a", "diag-b"],
                   help="the follow-up change diagnostic (prereg/addendum-1.md); empty: the registered protocol")
    p.add_argument("--budget-s", type=float, default=0, help="start no change after this many seconds (0: no limit)")
    args = p.parse_args()
    w = Workload(args.workload)
    store = stores.make(args.store)
    meta: dict = {"args": {k: str(v) for k, v in vars(args).items()}, "environment": environment(), "workload": w.meta}
    meta["load"] = {"store": store.load(w), "spicedb": engines.load_spicedb(w), "openfga": engines.load_openfga(w)}
    time.sleep(args.settle)
    store.open()
    ctx = Context(w, store, fga=meta["load"]["openfga"])
    variants = PUBLISHED
    names = [a for a in arms.names(store) if a != "a0"]
    if args.plan:
        names, variants = plan(store, args.plan)
        meta["variants"] = [list(v) for v in variants]
        meta["unreadable_by_all"] = len(unreadable_by_all(w))
    names = [a for a in args.arms.split(",") if a] or names
    meta["arms"] = names
    rows = asyncio.run(measure(ctx, Sources(w, store, ctx.fga), names, args.events, args.seed, args.every, args.cap,
                               args.settle, variants=tuple(variants), budget_s=args.budget_s))
    store.close()
    if args.plan or args.budget_s:
        meta["status"] = {"skipped_for_budget": sum(r.get("skipped") == "time budget" for r in rows)}
    write_jsonl_gz(args.out, rows)
    write_json(args.out.with_name(args.out.name.replace(".jsonl.gz", ".meta.json")), meta)
    log(f"wrote {len(rows)} change events to {args.out}")


if __name__ == "__main__":
    main()
