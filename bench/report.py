"""The study's report: every cell with intervals, and the verdict on each pre-registered hypothesis.

    python -m bench.report --results artifacts/ --out report/ [--resamples 10000] [--seed 5]

`--results` holds the measured jobs' files (`*.scored.jsonl.gz` with their `*.meta.json`, and the
churn and fault outputs). Pilot files are refused. Rules, as in the pre-registration (sections 5 to 8):

- Recall is averaged per user over every query of every job, then over users; a query that raised an
  error returned nothing, so its recall is 0 (counted, not dropped). Queries with nothing readable have
  no recall and are left out of recall only.
- Empty answers count queries that returned no hits without an error; errors are counted on their own.
- Latency: p50 and p99 per job, reported as the median and the range over the jobs.
- For H4 a call longer than 30 s counts as failed, as does a call that raised an error.
- Every interval is a bootstrap over users with its own random generator, seeded from `--seed` and the
  cell, so no interval depends on which other files are present.
- Every part a hypothesis needs is listed; a part with no data is "not run", which keeps the hypothesis
  from being supported (intersection-union rule).
"""

from __future__ import annotations

import argparse
import json
import zlib
from collections import defaultdict
from pathlib import Path

import numpy as np

from .util import read_json, read_jsonl_gz, write_json

LEVEL = 1 - 0.05 / 8  # Bonferroni over the eight hypotheses
TIMEOUT_MS = 30_000  # H4: a call longer than this counts as failed
SEEDS = 3  # measured jobs per cell (pre-registration, section 6)
STORES = ("pgvector", "qdrant", "milvus", "weaviate", "opensearch")
SETTINGS = {"pgvector": ("default", "iterative"), "qdrant": ("default", "acorn"), "milvus": ("default", "iterative"),
            "weaviate": ("default", "pathseer"), "opensearch": ("default",)}
ALTERNATIVE = {"pgvector": "iterative", "qdrant": "acorn", "milvus": "iterative", "weaviate": "pathseer",
               "opensearch": "default"}
POST_FILTER = ("a1-fga", "a1-spicedb", "a2-fga-x3", "a2-fga-x10", "a2-spicedb-x3", "a2-spicedb-x10")
SHARES = ("0p001", "0p01", "0p05", "0p2", "0p5")
CORRELATIONS = ("neg", "none", "pos")
W3_LAYOUTS = tuple(f"w3_s{s}_{c}" for s in SHARES for c in CORRELATIONS)


def rng_for(seed: int, *key: object) -> np.random.Generator:
    return np.random.default_rng([seed, zlib.crc32("|".join(map(str, key)).encode())])


def load(results: Path) -> tuple[list[dict], list[dict], list[dict], list[str]]:
    """Scored query rows, churn rows, fault rows (each tagged with workload, store and job), and the jobs
    whose run did not produce a scored file (listed in the coverage table)."""
    scored, churn, faults, unscored = [], [], [], []
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
        else:
            unscored.append(name)
    return scored, churn, faults, unscored


def interval(values: np.ndarray, rng: np.random.Generator, resamples: int, level: float) -> tuple[float, float]:
    if len(values) == 0:
        return (float("nan"), float("nan"))
    means = values[rng.integers(0, len(values), (resamples, len(values)))].mean(axis=1)
    lo, hi = np.quantile(means, [(1 - level) / 2, 1 - (1 - level) / 2])
    return float(lo), float(hi)


def recall_of(r: dict) -> float | None:
    """A query's recall: 0 if it raised an error (it returned nothing), None if nothing was readable."""
    if r.get("n_readable", 1) == 0:
        return None
    if r.get("error"):
        return 0.0
    return None if r.get("recall") is None else float(r["recall"])


def user_means(rows: list[dict]) -> dict[str, float]:
    per: dict[str, list[float]] = defaultdict(list)
    for r in rows:
        value = recall_of(r)
        if value is not None:
            per[r["user"]].append(value)
    return {u: float(np.mean(v)) for u, v in per.items()}


def cells(scored: list[dict], seed: int, resamples: int) -> list[dict]:
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for r in scored:
        groups[(r["workload"], r["store"], r["arm"], r["layout"])].append(r)
    out = []
    for key, rows in sorted(groups.items()):
        workload, store, arm, layout = key
        means = np.array(list(user_means(rows).values()))
        jobs: dict[str, list[float]] = defaultdict(list)
        for r in rows:
            jobs[r["job"]].append(r["ms"])
        p50 = [float(np.percentile(v, 50)) for v in jobs.values()]
        p99 = [float(np.percentile(v, 99)) for v in jobs.values()]
        errors = sum(bool(r["error"]) for r in rows)
        slow = sum(1 for r in rows if not r["error"] and r["ms"] > TIMEOUT_MS)
        out.append({
            "workload": workload, "store": store, "arm": arm, "layout": layout, "jobs": len(jobs),
            "users": len(means), "queries": len(rows),
            "recall": float(means.mean()) if len(means) else None,
            "recall_95": interval(means, rng_for(seed, *key, "95"), resamples, 0.95),
            "recall_bonferroni": interval(means, rng_for(seed, *key, "bonferroni"), resamples, LEVEL),
            "empty": sum(1 for r in rows if r["empty"] and not r["error"]),
            "outside": sum(r["outside"] for r in rows), "errors": errors, "over_30s": slow,
            "failed_h4": errors + slow,
            "p50_ms": {"median": float(np.median(p50)), "min": min(p50), "max": max(p50)},
            "p99_ms": {"median": float(np.median(p99)), "min": min(p99), "max": max(p99)},
        })
    return out


def verdict_below(lo: float, hi: float, bound: float) -> str:
    if np.isnan(lo) or np.isnan(hi):
        return "not run"
    return "supported" if hi < bound else "not supported" if lo >= bound else "inconclusive"


def combine(verdicts: list[str]) -> str:
    """Intersection-union: supported only if every part is; not supported if at least one part is not;
    otherwise (some part inconclusive or not run) inconclusive."""
    if not verdicts:
        return "not tested"
    if all(v == "supported" for v in verdicts):
        return "supported"
    if any(v == "not supported" for v in verdicts):
        return "not supported"
    return "inconclusive"


def hypotheses(scored: list[dict], faults: list[dict], table: list[dict], seed: int, resamples: int) -> dict:
    by = {(c["workload"], c["store"], c["arm"], c["layout"]): c for c in table}
    rows_by: dict[tuple, list[dict]] = defaultdict(list)
    for r in scored:
        rows_by[(r["workload"], r["store"], r["arm"], r["layout"])].append(r)
    result: dict = {}

    def w1_parts(name: str, arms: tuple[str, ...], bound: float) -> list[dict]:
        parts = []
        for store in STORES:
            for arm in arms:
                rows = [r for r in rows_by[("w1_enron", store, arm, "w1_enron")] if r.get("kind") == "own"]
                lo, hi = interval(np.array(list(user_means(rows).values())), rng_for(seed, name, store, arm), resamples,
                                  LEVEL)
                parts.append({"store": store, "arm": arm, "interval": [lo, hi], "verdict": verdict_below(lo, hi, bound)})
        return parts

    for name, arms, bound in (("H1", ("a1-fga", "a1-spicedb"), 0.5), ("H2", ("a2-fga-x10", "a2-spicedb-x10"), 0.9)):
        parts = w1_parts(name, arms, bound)
        result[name] = {"parts": parts, "verdict": combine([p["verdict"] for p in parts])}

    parts = []
    for store in STORES:
        for share in SHARES[:3]:
            for arm in POST_FILTER:
                a = np.array(list(user_means(rows_by[("w3", store, arm, f"w3_s{share}_neg")]).values()))
                b = np.array(list(user_means(rows_by[("w3", store, arm, f"w3_s{share}_pos")]).values()))
                if not len(a) or not len(b):
                    parts.append({"store": store, "share": share, "arm": arm, "interval": None, "verdict": "not run"})
                    continue
                rng = rng_for(seed, "H3", store, share, arm)
                diffs = (a[rng.integers(0, len(a), (resamples, len(a)))].mean(axis=1)
                         - b[rng.integers(0, len(b), (resamples, len(b)))].mean(axis=1))
                lo, hi = np.quantile(diffs, [(1 - LEVEL) / 2, 1 - (1 - LEVEL) / 2])
                parts.append({"store": store, "share": share, "arm": arm, "interval": [float(lo), float(hi)],
                              "verdict": verdict_below(float(lo), float(hi), 0.0)})
    result["H3"] = {"parts": parts, "verdict": combine([p["verdict"] for p in parts])}

    parts = []
    for store in STORES:
        needed = [(f"a3-spicedb@{s}", f"w3_s0p5_{c}") for s in SETTINGS[store] for c in CORRELATIONS]
        found = [by.get(("w3", store, arm, layout)) for arm, layout in needed]
        if any(c is None for c in found):
            parts.append({"store": store, "cells": sum(c is not None for c in found), "needed": len(needed),
                          "meets": None})
            continue
        meets = all(c["failed_h4"] > c["queries"] / 2 or c["p50_ms"]["median"] > 10_000 for c in found)
        parts.append({"store": store, "cells": len(found), "needed": len(needed), "meets": meets})
    complete = [p for p in parts if p["meets"] is not None]
    result["H4"] = {"parts": parts, "verdict": "supported" if any(p["meets"] for p in complete) else
                    "not supported" if len(complete) == len(parts) else "inconclusive"}

    parts = []
    for corr in CORRELATIONS:
        c = by.get(("w3", "pgvector", "a4@default", f"w3_s0p01_{corr}"))
        lo, hi = c["recall_bonferroni"] if c else (float("nan"), float("nan"))
        parts.append({"layout": f"w3_s0p01_{corr}", "interval": [lo, hi], "verdict": verdict_below(lo, hi, 0.5)})
    result["H5"] = {"parts": parts, "verdict": combine([p["verdict"] for p in parts])}

    parts = []
    for store in STORES:
        for layout in W3_LAYOUTS:
            c = by.get(("w3", store, f"a4@{ALTERNATIVE[store]}", layout))
            if c is None:
                parts.append({"store": store, "layout": layout, "interval": None, "verdict": "not run"})
                continue
            lo, hi = c["recall_bonferroni"]
            v = "supported" if lo >= 0.9 else "not supported" if hi < 0.9 else "inconclusive"
            parts.append({"store": store, "layout": layout, "interval": [lo, hi], "verdict": v})
    result["H6"] = {"parts": parts, "verdict": combine([p["verdict"] for p in parts])}

    parts = []
    for setting in SETTINGS["pgvector"]:
        for layout in W3_LAYOUTS:
            pair: dict[tuple, dict[str, float]] = defaultdict(dict)
            for arm in (f"a5-rls@{setting}", f"a4@{setting}"):
                for r in rows_by[("w3", "pgvector", arm, layout)]:
                    value = recall_of(r)
                    if value is not None:
                        pair[(r["job"], r["user"], r["q"])][arm.split("@")[0]] = value
            per: dict[str, list[float]] = defaultdict(list)
            for (_, user, _), v in pair.items():
                if len(v) == 2:
                    per[user].append(v["a5-rls"] - v["a4"])
            d = np.array([np.mean(v) for v in per.values()])
            lo, hi = interval(d, rng_for(seed, "H7", setting, layout), resamples, LEVEL)
            if np.isnan(lo):
                v = "not run"
            else:
                v = ("supported" if -0.02 < lo and hi < 0.02 else "not supported" if hi <= -0.02 or lo >= 0.02
                     else "inconclusive")
            parts.append({"setting": setting, "layout": layout, "interval": [lo, hi], "verdict": v})
    result["H7"] = {"parts": parts, "verdict": combine([p["verdict"] for p in parts])}

    stopped = [r for r in faults if r["arm"].endswith("|stopped")]
    stores_run = sorted({r["store"] for r in stopped})
    outside = sum(r["outside"] for r in stopped)
    result["H8"] = {"rows": len(stopped), "outside": outside, "stores": stores_run,
                    "verdict": "not tested" if not stopped else "not supported" if outside else
                    "supported" if set(stores_run) == set(STORES) else "inconclusive"}
    return result


def coverage(table: list[dict], unscored: list[str]) -> dict:
    """Cells with fewer jobs than the plan's seeds, and jobs that left no scored file."""
    short = [{k: c[k] for k in ("workload", "store", "arm", "layout", "jobs")} for c in table if c["jobs"] < SEEDS]
    return {"seeds_planned": SEEDS, "cells": len(table), "cells_short_of_seeds": short, "jobs_without_scores": unscored}


def harness_check(table: list[dict]) -> list[dict]:
    """The exact control (A0) must have recall 1, nothing outside and no error in every cell."""
    return [{k: c[k] for k in ("workload", "store", "layout", "recall", "outside", "errors")} for c in table
            if c["arm"] == "a0" and (c["recall"] is None or c["recall"] < 1.0 or c["outside"] or c["errors"])]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--results", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--resamples", type=int, default=10_000)
    p.add_argument("--seed", type=int, default=5)
    args = p.parse_args()
    scored, churn, faults, unscored = load(args.results)
    table = cells(scored, args.seed, args.resamples)
    fault_table = cells(faults, args.seed, args.resamples) if faults else []
    verdicts = hypotheses(scored, faults, table, args.seed, args.resamples)
    churn_table = []
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for r in churn:
        groups[(r["workload"], r["store"], r["arm"], r["kind"])].append(r)
    for (workload, store, arm, kind), rows in sorted(groups.items()):
        measured = [r for r in rows if not r.get("skipped")]
        delays = np.array([r["delay_s"] for r in measured if not r["censored"]])
        churn_table.append({"workload": workload, "store": store, "arm": arm, "kind": kind, "events": len(measured),
                            "skipped": len(rows) - len(measured), "censored": sum(r["censored"] for r in measured),
                            "delay_s": np.percentile(delays, [50, 90, 100]).tolist() if len(delays) else None})
    args.out.mkdir(parents=True, exist_ok=True)
    write_json(args.out / "cells.json", table)
    write_json(args.out / "faults.json", fault_table)
    write_json(args.out / "churn.json", churn_table)
    write_json(args.out / "hypotheses.json", verdicts)
    write_json(args.out / "coverage.json", coverage(table, unscored))
    write_json(args.out / "harness.json", harness_check(table))
    print(json.dumps({h: v["verdict"] for h, v in verdicts.items()}, indent=1))


if __name__ == "__main__":
    main()
