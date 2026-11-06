"""The study's report: every cell with intervals, and the verdict on each pre-registered hypothesis.

    python -m bench.report --results artifacts/ --out report/ [--resamples 10000] [--seed 5]

`--results` holds the measured jobs' files (`*.scored.jsonl.gz` with their `*.meta.json`, and the
churn and fault outputs). Pilot files are refused. Per cell (workload, store, arm, layout): recall
averaged per user over every query of every job, then over users, with a bootstrap interval over
users; empty answers, outside and error counts; p50 and p99 latency per job, as their median and
range across jobs. Hypotheses use the intervals and rules in section 7 of the pre-registration.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

from .util import read_json, read_jsonl_gz, write_json

LEVEL = 1 - 0.05 / 8  # Bonferroni over the eight hypotheses
POST_FILTER = ("a1-fga", "a1-spicedb", "a2-fga-x3", "a2-fga-x10", "a2-spicedb-x3", "a2-spicedb-x10")
ALTERNATIVE = {"pgvector": "iterative", "qdrant": "acorn", "milvus": "iterative", "weaviate": "pathseer",
               "opensearch": "default"}


def load(results: Path) -> tuple[list[dict], list[dict], list[dict]]:
    """Scored query rows, churn rows and fault rows, each tagged with workload, store and job."""
    scored, churn, faults = [], [], []
    for meta_path in sorted(results.rglob("*.meta.json")):
        meta = read_json(meta_path)
        name = meta_path.name.replace(".meta.json", "")
        if name.startswith("pilot"):
            raise SystemExit(f"{meta_path} is a pilot; pilots are never reported")
        tag = {"workload": meta["workload"]["name"], "store": meta["args"]["store"], "job": name}
        scored_path = meta_path.with_name(f"{name}.scored.jsonl.gz")
        raw_path = meta_path.with_name(f"{name}.jsonl.gz")
        if "-churn-" in name:
            churn += [{**r, **tag} for r in read_jsonl_gz(raw_path)]
        elif scored_path.exists():
            target = faults if "-faults-" in name else scored
            target += [{**r, **tag} for r in read_jsonl_gz(scored_path)]
    return scored, churn, faults


def interval(values: np.ndarray, rng: np.random.Generator, resamples: int, level: float) -> tuple[float, float]:
    if len(values) == 0:
        return (float("nan"), float("nan"))
    means = values[rng.integers(0, len(values), (resamples, len(values)))].mean(axis=1)
    lo, hi = np.quantile(means, [(1 - level) / 2, 1 - (1 - level) / 2])
    return float(lo), float(hi)


def user_means(rows: list[dict], value: str = "recall") -> dict[str, float]:
    per: dict[str, list[float]] = defaultdict(list)
    for r in rows:
        if r.get(value) is not None and not r.get("error"):
            per[r["user"]].append(float(r[value]))
    return {u: float(np.mean(v)) for u, v in per.items()}


def cells(scored: list[dict], rng: np.random.Generator, resamples: int) -> list[dict]:
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for r in scored:
        groups[(r["workload"], r["store"], r["arm"], r["layout"])].append(r)
    out = []
    for (workload, store, arm, layout), rows in sorted(groups.items()):
        means = np.array(list(user_means(rows).values()))
        jobs: dict[str, list[float]] = defaultdict(list)
        for r in rows:
            jobs[r["job"]].append(r["ms"])
        p50 = [float(np.percentile(v, 50)) for v in jobs.values()]
        p99 = [float(np.percentile(v, 99)) for v in jobs.values()]
        out.append({
            "workload": workload, "store": store, "arm": arm, "layout": layout, "jobs": len(jobs),
            "users": len(means), "queries": len(rows),
            "recall": float(means.mean()) if len(means) else None,
            "recall_95": interval(means, rng, resamples, 0.95),
            "recall_bonferroni": interval(means, rng, resamples, LEVEL),
            "empty": sum(bool(r["empty"]) for r in rows), "outside": sum(r["outside"] for r in rows),
            "errors": sum(bool(r["error"]) for r in rows),
            "p50_ms": {"median": float(np.median(p50)), "min": min(p50), "max": max(p50)},
            "p99_ms": {"median": float(np.median(p99)), "min": min(p99), "max": max(p99)},
        })
    return out


def verdict_below(lo: float, hi: float, bound: float) -> str:
    return "supported" if hi < bound else "not supported" if lo >= bound else "inconclusive"


def combine(verdicts: list[str]) -> str:
    """Intersection-union: supported only if every part is; not supported if any part is not."""
    if not verdicts:
        return "not tested"
    if all(v == "supported" for v in verdicts):
        return "supported"
    if any(v == "not supported" for v in verdicts):
        return "not supported"
    return "inconclusive"


def hypotheses(scored: list[dict], faults: list[dict], table: list[dict], rng: np.random.Generator,
               resamples: int) -> dict:
    by = {(c["workload"], c["store"], c["arm"], c["layout"]): c for c in table}
    w3 = [c for c in table if c["workload"] == "w3"]
    result: dict = {}

    def w1_parts(arms: tuple[str, ...], bound: float) -> list[dict]:
        parts = []
        for store in sorted({r["store"] for r in scored if r["workload"] == "w1_enron"}):
            for arm in arms:
                rows = [r for r in scored if r["workload"] == "w1_enron" and r["store"] == store and r["arm"] == arm
                        and r["kind"] == "own"]
                lo, hi = interval(np.array(list(user_means(rows).values())), rng, resamples, LEVEL)
                parts.append({"store": store, "arm": arm, "interval": [lo, hi], "verdict": verdict_below(lo, hi, bound)})
        return parts

    parts = w1_parts(("a1-fga", "a1-spicedb"), 0.5)
    result["H1"] = {"parts": parts, "verdict": combine([p["verdict"] for p in parts])}
    parts = w1_parts(("a2-fga-x10", "a2-spicedb-x10"), 0.9)
    result["H2"] = {"parts": parts, "verdict": combine([p["verdict"] for p in parts])}

    parts = []
    for store in sorted({c["store"] for c in w3}):
        for share in ("0p001", "0p01", "0p05"):
            for arm in POST_FILTER:
                neg = [r for r in scored if r["workload"] == "w3" and r["store"] == store and r["arm"] == arm
                       and r["layout"] == f"w3_s{share}_neg"]
                pos = [r for r in scored if r["workload"] == "w3" and r["store"] == store and r["arm"] == arm
                       and r["layout"] == f"w3_s{share}_pos"]
                a, b = np.array(list(user_means(neg).values())), np.array(list(user_means(pos).values()))
                if not len(a) or not len(b):
                    continue
                diffs = (a[rng.integers(0, len(a), (resamples, len(a)))].mean(axis=1)
                         - b[rng.integers(0, len(b), (resamples, len(b)))].mean(axis=1))
                lo, hi = np.quantile(diffs, [(1 - LEVEL) / 2, 1 - (1 - LEVEL) / 2])
                parts.append({"store": store, "share": share, "arm": arm, "interval": [float(lo), float(hi)],
                              "verdict": verdict_below(float(lo), float(hi), 0.0)})
    result["H3"] = {"parts": parts, "verdict": combine([p["verdict"] for p in parts])}

    stores_meeting, parts = [], []
    for store in sorted({c["store"] for c in w3}):
        cells_ = [c for c in w3 if c["store"] == store and c["arm"].startswith("a3-") and c["layout"].startswith("w3_s0p5_")]
        if not cells_:
            continue
        meets = all(c["errors"] > c["queries"] / 2 or c["p50_ms"]["median"] > 10_000 for c in cells_)
        parts.append({"store": store, "cells": len(cells_), "meets": meets})
        stores_meeting += [store] if meets else []
    result["H4"] = {"parts": parts, "verdict": "not tested" if not parts else
                    "supported" if stores_meeting else "not supported"}

    parts = []
    for corr in ("pos", "none", "neg"):
        c = by.get(("w3", "pgvector", "a4@default", f"w3_s0p01_{corr}"))
        if c:
            lo, hi = c["recall_bonferroni"]
            parts.append({"layout": c["layout"], "interval": [lo, hi], "verdict": verdict_below(lo, hi, 0.5)})
    result["H5"] = {"parts": parts, "verdict": combine([p["verdict"] for p in parts])}

    parts = []
    for c in w3:
        if c["arm"] == f"a4@{ALTERNATIVE.get(c['store'])}":
            lo, hi = c["recall_bonferroni"]
            v = "supported" if lo >= 0.9 else "not supported" if hi < 0.9 else "inconclusive"
            parts.append({"store": c["store"], "layout": c["layout"], "interval": [lo, hi], "verdict": v})
    result["H6"] = {"parts": parts, "verdict": combine([p["verdict"] for p in parts])}

    parts = []
    for setting in ("default", "iterative"):
        for layout in sorted({c["layout"] for c in w3 if c["store"] == "pgvector"}):
            pair: dict[tuple, dict[str, float]] = defaultdict(dict)
            for r in scored:
                if (r["workload"] == "w3" and r["store"] == "pgvector" and r["layout"] == layout
                        and r["arm"] in (f"a5-rls@{setting}", f"a4@{setting}") and r["recall"] is not None
                        and not r["error"]):
                    pair[(r["job"], r["user"], r["q"])][r["arm"].split("@")[0]] = r["recall"]
            per: dict[str, list[float]] = defaultdict(list)
            for (_, user, _), v in pair.items():
                if len(v) == 2:
                    per[user].append(v["a5-rls"] - v["a4"])
            d = np.array([np.mean(v) for v in per.values()])
            lo, hi = interval(d, rng, resamples, LEVEL)
            v = ("supported" if -0.02 < lo and hi < 0.02 else "not supported" if hi <= -0.02 or lo >= 0.02
                 else "inconclusive")
            parts.append({"setting": setting, "layout": layout, "interval": [lo, hi], "verdict": v})
    result["H7"] = {"parts": parts, "verdict": combine([p["verdict"] for p in parts])}

    stopped = [r for r in faults if r["arm"].endswith("|stopped")]
    outside = sum(r["outside"] for r in stopped)
    result["H8"] = {"rows": len(stopped), "outside": outside,
                    "verdict": "not tested" if not stopped else "supported" if outside == 0 else "not supported"}
    return result


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--results", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--resamples", type=int, default=10_000)
    p.add_argument("--seed", type=int, default=5)
    args = p.parse_args()
    rng = np.random.default_rng(args.seed)
    scored, churn, faults = load(args.results)
    table = cells(scored, rng, args.resamples)
    fault_table = cells(faults, rng, 1000) if faults else []
    verdicts = hypotheses(scored, faults, table, rng, args.resamples)
    churn_table = []
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for r in churn:
        groups[(r["workload"], r["store"], r["arm"], r["kind"])].append(r)
    for (workload, store, arm, kind), rows in sorted(groups.items()):
        delays = np.array([r["delay_s"] for r in rows if not r["censored"]])
        churn_table.append({"workload": workload, "store": store, "arm": arm, "kind": kind, "events": len(rows),
                            "censored": sum(r["censored"] for r in rows),
                            "delay_s": np.percentile(delays, [50, 90, 100]).tolist() if len(delays) else None})
    args.out.mkdir(parents=True, exist_ok=True)
    write_json(args.out / "cells.json", table)
    write_json(args.out / "faults.json", fault_table)
    write_json(args.out / "churn.json", churn_table)
    write_json(args.out / "hypotheses.json", verdicts)
    print(json.dumps({h: v["verdict"] for h, v in verdicts.items()}, indent=1))


if __name__ == "__main__":
    main()
