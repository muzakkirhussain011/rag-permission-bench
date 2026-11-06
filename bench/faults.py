"""Q4: what an arm returns when an authorization engine fails.

The arms reach SpiceDB and OpenFGA through Toxiproxy (set `BENCH_SPICEDB_GRPC=localhost:60051`,
`BENCH_SPICEDB_HTTP=http://localhost:60443`, `BENCH_OPENFGA_URL=http://localhost:60080` before
starting this module; loading still goes straight to the engines). For each fault, every arm that
asks an engine at query time answers the same `--queries` (layout, user, question) pairs:

- `none`: through the proxy, no fault (the baseline);
- `stopped`: both engine proxies disabled, so connections are refused;
- `slow`: 2 s added to every engine response;
- `cut`: each engine connection closed after `--cut-bytes` bytes, which ends long LookupResources
  streams part-way.

Answers are written raw; `bench.analyze` scores them (outside, empty, errors) per arm and fault.

    python -m bench.faults --workload data/dev --store pgvector --out results/faults.jsonl.gz
"""

from __future__ import annotations

import argparse
import asyncio
import json
import random
import time
import urllib.error
import urllib.request
from pathlib import Path

from . import arms, engines, stores
from .arms import Context
from .run import environment
from .util import log, retry, write_json, write_jsonl_gz
from .workload import Workload

API = "http://localhost:8474"
PROXIES = {
    "spicedb_grpc": ("0.0.0.0:60051", "spicedb:50051"),
    "spicedb_http": ("0.0.0.0:60443", "spicedb:8443"),
    "openfga": ("0.0.0.0:60080", "openfga:8080"),
}
FAULTS = ("none", "stopped", "slow", "cut")


def _toxi(method: str, path: str, body: dict | None = None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(API + path, data=data, method=method, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as error:
        if method == "DELETE" and error.code == 404:
            return {}
        raise


def setup_proxies() -> None:
    retry(lambda: _toxi("GET", "/version"), "Toxiproxy")


def apply(fault: str, cut_bytes: int) -> None:
    """Recreate every proxy for this fault. Deleting a proxy drops its open connections, so no
    client carries a connection, or a toxic's backlog, from one fault into the next."""
    for name, (listen, upstream) in PROXIES.items():
        _toxi("DELETE", f"/proxies/{name}")
        _toxi("POST", "/proxies", {"name": name, "listen": listen, "upstream": upstream, "enabled": fault != "stopped"})
        if fault == "slow":
            _toxi("POST", f"/proxies/{name}/toxics", {"name": "slow", "type": "latency", "stream": "downstream",
                                                      "attributes": {"latency": 2000, "jitter": 0}})
        elif fault == "cut":
            _toxi("POST", f"/proxies/{name}/toxics", {"name": "cut", "type": "limit_data", "stream": "downstream",
                                                      "attributes": {"bytes": cut_bytes}})


ENGINE_ARMS = ("a1-", "a2-", "a3-", "a7-")


async def measure(ctx: Context, names: list[str], pairs: list[tuple], cut_bytes: int) -> list[dict]:
    rows = []
    for fault in FAULTS:
        apply(fault, cut_bytes)
        time.sleep(1)
        for name in names:
            run = arms.build(name, ctx)  # fresh clients per fault, as after a restart
            errors = 0
            for layout, user, q in pairs:
                t0 = time.perf_counter_ns()
                try:
                    hits, error = await asyncio.wait_for(run(user, layout.user_groups.get(user, []), f"q{q}"), 60), None
                except Exception as e:  # noqa: BLE001 - what the arm does on failure is the result
                    hits, error = [], f"{type(e).__name__}: {e}"[:300]
                    errors += 1
                rows.append({"arm": f"{name}|{fault}", "layout": layout.name, "user": user, "q": q,
                             "hits": [h[0] for h in hits], "scores": [round(h[1], 6) for h in hits],
                             "ms": (time.perf_counter_ns() - t0) / 1e6, "error": error})
            log(f"{fault} {name}: {len(pairs)} queries, {errors} errors")
    apply("none", cut_bytes)
    return rows


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--workload", type=Path, required=True)
    p.add_argument("--store", required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--queries", type=int, default=100)
    p.add_argument("--cut-bytes", type=int, default=16_384)
    p.add_argument("--seed", type=int, default=3)
    args = p.parse_args()
    if "60051" not in engines.SPICEDB_GRPC or "60080" not in engines.OPENFGA_URL:
        raise SystemExit("set BENCH_SPICEDB_GRPC, BENCH_SPICEDB_HTTP and BENCH_OPENFGA_URL to the proxy first")
    w = Workload(args.workload)
    store = stores.make(args.store)
    meta: dict = {"args": {k: str(v) for k, v in vars(args).items()}, "environment": environment(), "workload": w.meta}
    meta["load"] = {"store": store.load(w), "spicedb": engines.load_spicedb(w), "openfga": engines.load_openfga(w)}
    setup_proxies()
    time.sleep(10)
    store.open()
    ctx = Context(w, store, fga=meta["load"]["openfga"])
    everything = [(layout, u, q) for layout in w.layouts for u, q in layout.queries]
    pairs = random.Random(args.seed).sample(everything, min(args.queries, len(everything)))
    names = [a for a in arms.names(store) if a.startswith(ENGINE_ARMS)]
    rows = asyncio.run(measure(ctx, names, pairs, args.cut_bytes))
    store.close()
    write_jsonl_gz(args.out, rows)
    write_json(args.out.with_name(args.out.name.replace(".jsonl.gz", ".meta.json")), meta)
    log(f"wrote {len(rows)} rows to {args.out}")


if __name__ == "__main__":
    main()
