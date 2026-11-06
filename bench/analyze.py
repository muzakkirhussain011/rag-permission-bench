"""Score a run against the exact answers and summarize it per arm and layout.

    python -m bench.analyze --workload data/dev --run results/dev-pgvector.jsonl.gz [--check]

Writes `<run>.summary.json` and prints a table. Recall is averaged per user, then over users.
`--check` fails unless the harness is sound: the exact control (a0) returns the exact answer for
every pair, returns nothing outside, and no arm raised an error. It checks the harness, never a
hypothesis.
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

from .metrics import score
from .util import read_jsonl_gz, write_json
from .workload import Workload


def summarize(w: Workload, rows: list[dict], truth: dict) -> tuple[list[dict], list[str]]:
    masks: dict[tuple[str, str], np.ndarray] = {}
    cells: dict[tuple[str, str], list] = defaultdict(list)
    problems: list[str] = []
    for row in rows:
        key = (row["layout"], row["user"])
        if key not in masks:
            masks[key] = w.readable(row["user"], w.layout(row["layout"]).user_groups.get(row["user"], []))
        t = truth[(row["layout"], row["user"], row["q"])]
        s = score(row["hits"], t, masks[key], w.vectors, w.queries[row["q"]])
        cells[(row["arm"], row["layout"])].append((row, s))
        if row["arm"] == "a0" and row["error"] is None and t["n_readable"] > 0 and s["recall"] != 1.0:
            problems.append(f"a0 recall {s['recall']} on {key} q{row['q']}")
        if row["arm"] == "a0" and s["outside"]:
            problems.append(f"a0 returned {s['outside']} unreadable chunks on {key} q{row['q']}")
    out = []
    for (arm, layout), items in sorted(cells.items()):
        per_user: dict[str, list[float]] = defaultdict(list)
        for row, s in items:
            if s["recall"] is not None and row["error"] is None:
                per_user[row["user"]].append(s["recall"])
        user_means = [float(np.mean(v)) for v in per_user.values()]
        ms = np.array([row["ms"] for row, _ in items])
        errors = [row["error"] for row, _ in items if row["error"]]
        if errors:
            problems.append(f"{arm} on {layout}: {len(errors)} errors, first: {errors[0]}")
        out.append({
            "arm": arm,
            "layout": layout,
            "queries": len(items),
            "users": len(per_user),
            "recall": float(np.mean(user_means)) if user_means else None,
            "empty": sum(s["empty"] for _, s in items),
            "outside": sum(s["outside"] for _, s in items),
            "errors": len(errors),
            "p50_ms": float(np.percentile(ms, 50)),
            "p99_ms": float(np.percentile(ms, 99)),
        })
    return out, problems


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--workload", type=Path, required=True)
    p.add_argument("--run", type=Path, required=True)
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    w = Workload(args.workload)
    truth = {(t["layout"], t["user"], t["q"]): t for t in read_jsonl_gz(args.workload / "truth.jsonl.gz")}
    summary, problems = summarize(w, read_jsonl_gz(args.run), truth)
    write_json(args.run.with_name(args.run.name.replace(".jsonl.gz", ".summary.json")),
               {"cells": summary, "problems": problems})
    print("| arm | layout | queries | recall@10 | empty | outside | errors | p50 ms | p99 ms |")
    print("|---|---|---|---|---|---|---|---|---|")
    for c in summary:
        recall = "-" if c["recall"] is None else f"{c['recall']:.3f}"
        print(f"| {c['arm']} | {c['layout']} | {c['queries']} | {recall} | {c['empty']} | {c['outside']} |"
              f" {c['errors']} | {c['p50_ms']:.1f} | {c['p99_ms']:.1f} |")
    for problem in problems[:50]:
        print("PROBLEM:", problem)
    if args.check and problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
