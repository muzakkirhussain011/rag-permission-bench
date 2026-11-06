"""Timings and errors of a run, without scoring it, and on pgvector the shape of each recorded plan. Pilot
runs use this instead of `bench.analyze`, so no recall on real data is seen before the pre-registration is
deposited.

    python -m bench.timing --run results/pilot-run-w3-pgvector-seed1.jsonl.gz
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

from .util import read_jsonl_gz, write_json


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--run", type=Path, required=True)
    args = p.parse_args()
    cells: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in read_jsonl_gz(args.run):
        cells[(row["arm"], row["layout"])].append(row)
    out = []
    print("| arm | layout | queries | errors | p50 ms | p99 ms | total s |")
    print("|---|---|---|---|---|---|---|")
    for (arm, layout), rows in sorted(cells.items()):
        ms = np.array([r["ms"] for r in rows])
        errors = [r["error"] for r in rows if r["error"]]
        cell = {"arm": arm, "layout": layout, "queries": len(rows), "errors": len(errors),
                "first_error": errors[0] if errors else None, "p50_ms": float(np.percentile(ms, 50)),
                "p99_ms": float(np.percentile(ms, 99)), "total_s": float(ms.sum() / 1000)}
        out.append(cell)
        print(f"| {arm} | {layout} | {len(rows)} | {len(errors)} | {cell['p50_ms']:.1f} | {cell['p99_ms']:.1f} |"
              f" {cell['total_s']:.0f} |")
    for cell in out:
        if cell["first_error"]:
            print(f"ERROR {cell['arm']} {cell['layout']}: {cell['first_error']}")
    write_json(args.run.with_name(args.run.name.replace(".jsonl.gz", ".timing.json")), out)
    meta = args.run.with_name(args.run.name.replace(".jsonl.gz", ".meta.json"))
    if meta.exists():
        plans = json.loads(meta.read_text(encoding="utf-8")).get("plans", [])
        if plans:
            print("\n| arm | layout | plan (node types and indexes only) |\n|---|---|---|")
            for p in plans:
                print(f"| {p['arm']} | {p['layout']} | {plan_shape(p['plan']['Plan'])} |")


def plan_shape(node: dict) -> str:
    """Which scans a pgvector plan used, without row counts, so a pilot shows how an arm ran but not
    what it returned."""
    name = node["Node Type"] + (f"[{node['Index Name']}]" if "Index Name" in node else "")
    children = [plan_shape(child) for child in node.get("Plans", [])]
    return name + (" > " + ", ".join(children) if children else "")


if __name__ == "__main__":
    main()
