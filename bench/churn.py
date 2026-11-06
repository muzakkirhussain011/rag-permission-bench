"""Q3: how long after a permission change at the source do an arm's answers reflect it?

Per arm, `--events` changes alternate between a revocation and a grant, each on a chunk of its own:

- revoke: a chunk a measured user may read loses every reader;
- grant: a chunk nobody may read (made so beforehand, then left to settle) gains the user as a reader.

Each change is applied at every source in parallel, the way a sync job would: both engines (SpiceDB
and OpenFGA relationships) and the store's copy of the chunk's principals. The probe is the chunk's
own vector, so the chunk is among the top hits whenever the user may read it. The arm is asked every
`--every` seconds until its answer reflects the change, up to `--cap` seconds. The delay counts from
the last acknowledgement among the source writes; each write's own latency is recorded too.

    python -m bench.churn --workload data/dev --store pgvector --out results/churn.jsonl.gz [--events 20]
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


def _chunk_readers(w: Workload, i: int):  # noqa: ANN202
    for u in w.user_idx[w.user_ptr[i] : w.user_ptr[i + 1]]:
        yield Tuple("chunk", f"c{i}", "reader", "user", w.user_names[u])
    for g in w.group_idx[w.group_ptr[i] : w.group_ptr[i + 1]]:
        yield Tuple("chunk", f"c{i}", "reader", "group", w.group_names[g], "member")


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

        def timed(name: str, call) -> tuple[str, float, float]:  # noqa: ANN001
            start = time.perf_counter()
            call()
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
        return {"write_s": {name: s for name, s, _ in done}, "acked_at": max(end for _, _, end in done)}


async def probe(run, user: str, groups: list[str], chunk: int, want_present: bool, acked_at: float, every: float,
                cap: float) -> dict:  # noqa: ANN001
    asked = 0
    while True:
        try:
            hits = [h[0] for h in await run(user, groups, f"v{chunk}")]
            error = None
        except Exception as e:  # noqa: BLE001
            hits, error = [], f"{type(e).__name__}: {e}"[:200]
        asked += 1
        now = time.perf_counter()
        if error is None and (chunk in hits) == want_present:
            return {"delay_s": now - acked_at, "censored": False, "probes": asked}
        if now - acked_at > cap:
            return {"delay_s": now - acked_at, "censored": True, "probes": asked, "last_error": error}
        await asyncio.sleep(every)


async def measure(ctx: Context, sources: Sources, names: list[str], events: int, seed: int, every: float,
                  cap: float, settle: float) -> list[dict]:
    rng = random.Random(seed)
    users = [(layout, u) for layout in ctx.workload.layouts for u in sorted({x for x, _ in layout.queries})]
    used: set[int] = set()
    rows = []
    order = list(names)
    rng.shuffle(order)
    for name in order:
        run = arms.build(name, ctx)
        for e in range(events):
            layout, user = rng.choice(users)
            groups = layout.user_groups.get(user, [])
            readable = np.flatnonzero(ctx.workload.readable(user, groups))
            candidates = [int(i) for i in readable if int(i) not in used]
            if not candidates:
                continue
            chunk = rng.choice(candidates)
            used.add(chunk)
            if e % 2 == 0:
                kind, change = "revoke", sources.apply(chunk, [])
                result = await probe(run, user, groups, chunk, False, change["acked_at"], every, cap)
            else:
                sources.apply(chunk, [])
                await asyncio.sleep(settle)
                kind = "grant"
                change = sources.apply(chunk, [Tuple("chunk", f"c{chunk}", "reader", "user", user)])
                result = await probe(run, user, [], chunk, True, change["acked_at"], every, cap)
            rows.append({"arm": name, "event": e, "kind": kind, "layout": layout.name, "user": user, "chunk": chunk,
                         "write_s": change["write_s"], **result})
            log(f"{name} {kind} c{chunk}: {result['delay_s']:.2f} s{' (censored)' if result['censored'] else ''}")
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
    args = p.parse_args()
    w = Workload(args.workload)
    store = stores.make(args.store)
    meta: dict = {"args": {k: str(v) for k, v in vars(args).items()}, "environment": environment(), "workload": w.meta}
    meta["load"] = {"store": store.load(w), "spicedb": engines.load_spicedb(w), "openfga": engines.load_openfga(w)}
    time.sleep(args.settle)
    store.open()
    ctx = Context(w, store, fga=meta["load"]["openfga"])
    names = [a for a in args.arms.split(",") if a] or [a for a in arms.names(store) if a != "a0"]
    rows = asyncio.run(measure(ctx, Sources(w, store, ctx.fga), names, args.events, args.seed, args.every, args.cap,
                               args.settle))
    store.close()
    write_jsonl_gz(args.out, rows)
    write_json(args.out.with_name(args.out.name.replace(".jsonl.gz", ".meta.json")), meta)
    log(f"wrote {len(rows)} change events to {args.out}")


if __name__ == "__main__":
    main()
