"""Run one cell: load a store and both engines with a workload, then measure every arm.

    python -m bench.run --workload data/dev --store pgvector --out results/dev-pgvector.jsonl.gz
        [--seed 1] [--warmup 20] [--arms a0,a4@default] [--layouts name,...] [--settle 10]

All arms run in this one process, one query at a time, in an order drawn from `--seed`. Each arm
gets `--warmup` unrecorded queries first. Every answer is written raw (hit ids, scores, latency,
error); scoring is a separate step (`bench.analyze`). A `.meta.json` beside the output records
versions, images, machine, load timings, probes and, on pgvector, executed plans.
"""

from __future__ import annotations

import argparse
import asyncio
import importlib.metadata
import os
import platform
import random
import subprocess
import time
from pathlib import Path

from . import arms, engines, stores
from .arms import Context
from .util import log, write_json, write_jsonl_gz
from .workload import Workload, principals

PACKAGES = [
    "numpy", "psycopg", "pgvector", "qdrant-client", "pymilvus", "weaviate-client", "opensearch-py",
    "authzed", "openfga-sdk", "langchain-core",
    "langchain-spicedb", "auth0-ai-langchain", "auth0-ai", "grpcio", "protobuf", "pydantic",
]


def environment() -> dict:
    versions = {}
    for package in PACKAGES:
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            pass
    images = subprocess.run(["docker", "compose", "images", "--format", "json"], capture_output=True, text=True)
    meminfo = Path("/proc/meminfo")
    memory = meminfo.read_text().splitlines()[0] if meminfo.exists() else None
    return {
        "packages": versions,
        "images": images.stdout.strip(),
        "python": platform.python_version(),
        "cpus": os.cpu_count(),
        "memory": memory,
        "git_sha": os.environ.get("GITHUB_SHA"),
        "runner": os.environ.get("RUNNER_NAME"),
        "run_id": os.environ.get("GITHUB_RUN_ID"),
    }


async def probe_fga_async(ctx: Context, user: str, key: str) -> dict:
    """Whether FGARetriever's async path works, since the measured arm uses `invoke`."""
    from auth0_ai_langchain import FGARetriever
    from openfga_sdk import ClientConfiguration
    from openfga_sdk.client.models import ClientBatchCheckItem

    config = ClientConfiguration(api_url=engines.OPENFGA_URL, store_id=ctx.fga["store_id"],
                                 authorization_model_id=ctx.fga["model_id"])
    retriever = FGARetriever(
        retriever=arms.StoreRetriever(ctx=ctx, k=arms.K),
        build_query=lambda doc: ClientBatchCheckItem(
            user=f"user:{user}", relation="viewer", object=f"chunk:{doc.metadata['resource_id']}"
        ),
        fga_configuration=config,
    )
    try:
        docs = await retriever.ainvoke(key)
        return {"ok": True, "hits": len(docs)}
    except Exception as error:  # noqa: BLE001 - the probe reports whatever happens
        return {"ok": False, "error": f"{type(error).__name__}: {error}"[:500]}


async def measure(ctx: Context, names: list[str], pairs: list[tuple], seed: int, warmup: int) -> list[dict]:
    rng = random.Random(seed)
    order = list(names)
    rng.shuffle(order)
    rows: list[dict] = []
    for name in order:
        run = arms.build(name, ctx)
        for layout, user, q in rng.sample(pairs, min(warmup, len(pairs))):
            try:
                await run(user, layout.user_groups.get(user, []), f"q{q}")
            except Exception:  # noqa: BLE001 - warm-up failures show up again when measured
                pass
        sequence = list(pairs)
        rng.shuffle(sequence)
        started = time.perf_counter()
        errors = 0
        for layout, user, q in sequence:
            groups = layout.user_groups.get(user, [])
            t0 = time.perf_counter_ns()
            try:
                hits, error = await run(user, groups, f"q{q}"), None
            except Exception as e:  # noqa: BLE001 - recorded per query, never hidden
                hits, error = [], f"{type(e).__name__}: {e}"[:300]
                errors += 1
            t1 = time.perf_counter_ns()
            rows.append({
                "arm": name, "layout": layout.name, "user": user, "q": q,
                "hits": [h[0] for h in hits], "scores": [round(h[1], 6) for h in hits],
                "ms": (t1 - t0) / 1e6, "error": error,
            })
        log(f"{name}: {len(sequence)} queries in {time.perf_counter() - started:.0f} s, {errors} errors")
    return rows


def explain_samples(ctx: Context, pairs: list[tuple]) -> list[dict]:
    """One executed plan per layout and filtered pgvector arm, for the record."""
    plans = []
    seen = set()
    for layout, user, q in pairs:
        if layout.name in seen:
            continue
        seen.add(layout.name)
        p = principals(user, layout.user_groups.get(user, []))
        vector = ctx.vector(f"q{q}")
        for setting in ("exact", *ctx.store.settings):
            plans.append({"layout": layout.name, "arm": f"a4@{setting}",
                          "plan": ctx.store.explain(vector, arms.K, principals=p, setting=setting)})
        for setting in ctx.store.settings:
            plans.append({"layout": layout.name, "arm": f"a5-rls@{setting}",
                          "plan": ctx.store.explain(vector, arms.K, principals=p, setting=setting, rls=True)})
    return plans


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--workload", type=Path, required=True)
    p.add_argument("--store", required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--warmup", type=int, default=20)
    p.add_argument("--arms", default="")
    p.add_argument("--layouts", default="")
    p.add_argument("--settle", type=float, default=10.0, help="seconds between loading and the first query")
    p.add_argument("--partitions", action="store_true", help="also build per-principal partitions (arm A6, pgvector)")
    p.add_argument("--pairs-per-layout", type=int, default=0, help="sample this many pairs per layout (0: all)")
    args = p.parse_args()

    meta: dict = {"args": {k: str(v) for k, v in vars(args).items()}, "environment": environment()}
    w = Workload(args.workload)
    meta["workload"] = w.meta
    store = stores.make(args.store)
    meta["load"] = {"store": store.load(w), "spicedb": engines.load_spicedb(w), "openfga": engines.load_openfga(w)}
    if args.partitions:
        meta["load"]["partitions"] = store.load_partitions(w)
    time.sleep(args.settle)
    store.open()
    ctx = Context(w, store, fga=meta["load"]["openfga"])
    wanted = set(filter(None, args.layouts.split(",")))
    pairs = []
    sampler = random.Random(args.seed)
    for layout in w.layouts:
        if wanted and layout.name not in wanted:
            continue
        chosen = [(layout, u, q) for u, q in layout.queries]
        if args.pairs_per_layout:
            chosen = sampler.sample(chosen, min(args.pairs_per_layout, len(chosen)))
        pairs += chosen
    names = [a for a in args.arms.split(",") if a] or arms.names(store)
    meta["arms"] = names
    meta["pairs"] = len(pairs)
    layout, user, q = pairs[0]
    meta["probes"] = {"fga_ainvoke": asyncio.run(probe_fga_async(ctx, user, f"q{q}"))}
    log(f"probes: {meta['probes']}")
    rows = asyncio.run(measure(ctx, names, pairs, args.seed, args.warmup))
    if store.name == "pgvector":
        meta["plans"] = explain_samples(ctx, pairs)
    if hasattr(store, "strategy"):
        meta["filter_strategy_at_end"] = store.strategy()
    stats = subprocess.run(["docker", "stats", "--no-stream", "--format", "{{json .}}"], capture_output=True, text=True)
    meta["docker_stats_after"] = [line for line in stats.stdout.splitlines() if line.strip()]
    store.close()
    write_jsonl_gz(args.out, rows)
    write_json(args.out.with_name(args.out.name.replace(".jsonl.gz", ".meta.json")), meta)
    log(f"wrote {len(rows)} rows to {args.out}")


if __name__ == "__main__":
    main()
