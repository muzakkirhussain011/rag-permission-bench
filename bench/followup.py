"""The report of the follow-up runs registered in `prereg/addendum-1.md`: exploratory, no hypotheses.

    python -m bench.followup --results artifacts/ --baseline results-v1/report --out report/
        [--resamples 10000] [--seed 5]

`--results` holds the follow-up jobs' outputs, one folder per job, as `followup-report.yml` collects them;
`--baseline` the report of release `results-v1` (its `cells.json`, `churn.json`, `hypotheses.json`), for
the reproduction check and the comparisons the addendum names. Rules (addendum, section 6):

- Cells as `bench.report.cells` computes them: recall per user, then over users, a failed query counting
  as recall 0, with a 95% bootstrap interval over users; p50 and p99 per job, with their median and range.
  The Bonferroni interval `bench.report` adds for the registered hypotheses is dropped: nothing is judged.
- An arm's name carries its search breadth and lookup (`bench.arms.parse`): `a4@default:ef40`,
  `a4@default:ef100+lookup-spicedb`. Plain names are the lookup jobs' arms at the default ef of 100.
- Change rows carry their protocol and consistency (`bench.churn`); the published protocol at the default
  consistency keeps the arm's own name, as in `results-v1`.

Writes `cells.json`, `per_job.json` and `per_job.tsv`, `sweep.json`, `tunability.json`, `lookup.json`,
`churn.json`, `reproduction.json`, `jobs.json`, and `followup.md`, which presents them.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

import numpy as np

from . import report
from .arms import parse as _parse
from .util import read_json, read_jsonl_gz, write_json

KEEP = ("arm", "layout", "user", "q", "ms", "error", "n_readable", "recall", "outside", "empty",
        "lookup_ms", "search_ms", "groups_found", "principals_match")
SWEEP_SHARES = ("0p01", "0p05")
ORDERS = {"neg": "farthest first", "none": "random", "pos": "nearest first"}


parse = lru_cache(maxsize=None)(_parse)  # one regex match per arm name, not per answer


# ---- loading ------------------------------------------------------------------------------------


def load(results: Path) -> tuple[list[dict], list[dict], list[dict]]:
    """Scored query rows (only the fields used here), change rows, and one record per job."""
    runs, churn, jobs = [], [], []
    for meta_path in sorted(results.rglob("*.meta.json")):
        name = meta_path.name.replace(".meta.json", "")
        if name.startswith("pilot"):
            raise SystemExit(f"{meta_path} is a pilot; pilots are never reported")
        meta = read_json(meta_path)
        args = meta.get("args", {})
        tag = {"workload": meta["workload"]["name"], "store": args["store"], "job": name}
        env = meta.get("environment", {})
        job = {**tag, "plan": args.get("plan", ""), "kind": "churn" if "-churn-" in name else "run",
               "seed": args.get("seed"), "git_sha": env.get("git_sha"), "run_id": env.get("run_id"),
               "cpus": env.get("cpus"), "memory": env.get("memory"), "complete": meta.get("complete"),
               "status": meta.get("status"), "arms": len(meta.get("arms", [])), "pairs": meta.get("pairs"),
               "unreadable_by_all": meta.get("unreadable_by_all"),
               "store_load": (meta.get("load") or {}).get("store")}  # e.g. Qdrant's and OpenSearch's segments
        raw = meta_path.with_name(f"{name}.jsonl.gz")
        scored = meta_path.with_name(f"{name}.scored.jsonl.gz")
        if job["kind"] == "churn":
            rows = read_jsonl_gz(raw) if raw.exists() else []
            churn += [{**r, **tag} for r in rows]
            job["rows"] = len(rows)
        elif scored.exists():
            rows = read_jsonl_gz(scored)
            runs += [{**{k: r[k] for k in KEEP if k in r}, **tag} for r in rows]
            job["rows"] = len(rows)
        else:
            job["rows"] = None
        jobs.append(job)
    return runs, churn, jobs


# ---- helpers ------------------------------------------------------------------------------------


def share_of(layout: str) -> str | None:
    """`w3_s0p01_neg` -> `0p01`; other workloads have no share."""
    parts = layout.split("_")
    return parts[1][1:] if layout.startswith("w3_s") and len(parts) == 3 else None


def order_of(layout: str) -> str | None:
    return layout.rsplit("_", 1)[1] if layout.startswith("w3_s") else None


def spread(values: list[float]) -> dict | None:
    """Median and range over jobs."""
    if not values:
        return None
    return {"median": float(np.median(values)), "min": float(min(values)), "max": float(max(values))}


def per_job_percentiles(rows: list[dict], field: str) -> dict:
    """p50 and p99 of `field` in each job, then their median and range over the jobs."""
    by_job: dict[str, list[float]] = defaultdict(list)
    for r in rows:
        if r.get(field) is not None:
            by_job[r["job"]].append(float(r[field]))
    p50 = [float(np.percentile(v, 50)) for v in by_job.values()]
    p99 = [float(np.percentile(v, 99)) for v in by_job.values()]
    return {"jobs": len(by_job), "p50": spread(p50), "p99": spread(p99)}


def counterpart(arm: str) -> str:
    """The same arm without its lookup: `a4@default:ef100+lookup-spicedb` -> `a4@default:ef100`."""
    return arm.split("+lookup-", 1)[0]


# ---- tables -------------------------------------------------------------------------------------


def cells(runs: list[dict], seed: int, resamples: int) -> list[dict]:
    table = report.cells(runs, seed, resamples)
    rows_by: dict[tuple, list[dict]] = defaultdict(list)
    for r in runs:
        if "lookup_ms" in r:
            rows_by[(r["workload"], r["store"], r["arm"], r["layout"])].append(r)
    for c in table:
        c.pop("recall_bonferroni", None)
        base, ef, lookup = parse(c["arm"])
        c.update(base=base, ef=ef, lookup=lookup, share=share_of(c["layout"]), order=order_of(c["layout"]))
        rows = rows_by.get((c["workload"], c["store"], c["arm"], c["layout"]))
        if rows:
            c["lookup_ms"] = per_job_percentiles(rows, "lookup_ms")
            c["search_ms"] = per_job_percentiles(rows, "search_ms")
            c["groups_found_mean"] = float(np.mean([r["groups_found"] for r in rows if "groups_found" in r]))
            c["principals_differ"] = sum(1 for r in rows if r.get("principals_match") is False)
    return table


def per_job(runs: list[dict]) -> list[dict]:
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for r in runs:
        groups[(r["job"], r["workload"], r["store"], r["arm"], r["layout"])].append(r)
    out = []
    for (job, workload, store, arm, layout), rows in sorted(groups.items()):
        ms = np.array([r["ms"] for r in rows])
        entry = {"job": job, "workload": workload, "store": store, "arm": arm, "layout": layout, "queries": len(rows),
                 "errors": sum(bool(r["error"]) for r in rows), "p50_ms": float(np.percentile(ms, 50)),
                 "p99_ms": float(np.percentile(ms, 99))}
        for field in ("lookup_ms", "search_ms"):
            values = [r[field] for r in rows if r.get(field) is not None]
            if values:
                entry[f"{field[:-3]}_p50_ms"] = float(np.percentile(values, 50))
                entry[f"{field[:-3]}_p99_ms"] = float(np.percentile(values, 99))
        out.append(entry)
    return out


def sweep(table: list[dict]) -> list[dict]:
    """F1: every W3 cell at shares 0.01 and 0.05 that ran at a stated search breadth, without a lookup."""
    out = []
    for c in table:
        if c["workload"] == "w3" and c["share"] in SWEEP_SHARES and c["ef"] is not None and c["lookup"] is None:
            out.append({k: c[k] for k in ("store", "base", "ef", "layout", "share", "order", "recall", "recall_95",
                                          "users", "queries", "jobs", "empty", "errors", "outside", "p50_ms",
                                          "p99_ms")})
    return sorted(out, key=lambda c: (c["store"], c["base"], c["layout"], c["ef"]))


def tunability(sweep_rows: list[dict], baseline_h6: dict) -> list[dict]:
    """F1: per layout and store, the A4 settings whose mean recall reaches 0.9, those whose interval lies wholly
    at or above it, and the highest mean reached, each with its latency; beside H6's registered interval."""
    out = []
    by: dict[tuple, list[dict]] = defaultdict(list)
    for c in sweep_rows:
        if c["base"].startswith("a4@"):
            by[(c["layout"], c["store"])].append(c)
    for (layout, store), rows in sorted(by.items()):
        def brief(c: dict) -> dict:
            return {"arm": f"{c['base']}:ef{c['ef']}", "recall": c["recall"], "recall_95": c["recall_95"],
                    "p50_ms": c["p50_ms"]["median"], "p99_ms": c["p99_ms"]["median"]}
        valid = [c for c in rows if c["recall"] is not None]
        best = max(valid, key=lambda c: c["recall"]) if valid else None
        out.append({
            "layout": layout, "store": store, "h6_results_v1": baseline_h6.get((store, layout)),
            "mean_at_least_0p9": [brief(c) for c in valid if c["recall"] >= 0.9],
            "interval_at_least_0p9": [brief(c) for c in valid if c["recall_95"][0] >= 0.9],
            "highest": brief(best) if best else None,
        })
    return out


def lookups(runs: list[dict], table: list[dict]) -> dict:
    """F2: the lookup's cost per workload (W3 per share) and engine, and each lookup arm beside its counterpart."""
    cost_rows: dict[tuple, list[dict]] = defaultdict(list)
    for r in runs:
        _, _, engine = parse(r["arm"])
        if engine is not None:
            group = f"w3 share {share_of(r['layout'])}" if r["workload"] == "w3" else r["workload"]
            cost_rows[(group, engine)].append(r)
    cost = []
    for (group, engine), rows in sorted(cost_rows.items()):
        cost.append({"workload": group, "engine": engine, "queries": len(rows),
                     "errors": sum(bool(r["error"]) for r in rows),
                     "groups_found_mean": float(np.mean([r["groups_found"] for r in rows if "groups_found" in r]))
                     if any("groups_found" in r for r in rows) else None,
                     "principals_differ": sum(1 for r in rows if r.get("principals_match") is False),
                     **{f"lookup_{k}": v for k, v in per_job_percentiles(rows, "lookup_ms").items()}})
    by = {(c["workload"], c["store"], c["arm"], c["layout"]): c for c in table}
    arms_ = []
    for c in table:
        if c["lookup"] is None:
            continue
        plain = by.get((c["workload"], c["store"], counterpart(c["arm"]), c["layout"]))
        arms_.append({
            "workload": c["workload"], "store": c["store"], "layout": c["layout"], "arm": c["arm"],
            "engine": c["lookup"], "recall": c["recall"], "recall_without": plain["recall"] if plain else None,
            "lookup_ms": c.get("lookup_ms"), "search_ms": c.get("search_ms"),
            "total_ms": {"p50": c["p50_ms"], "p99": c["p99_ms"]},
            "without_ms": {"p50": plain["p50_ms"], "p99": plain["p99_ms"]} if plain else None,
            "principals_differ": c.get("principals_differ"), "errors": c["errors"],
        })
    return {"cost": cost, "arms": arms_}


def churn_summary(rows: list[dict], baseline: list[dict]) -> list[dict]:
    """F4: per store, arm, protocol, consistency and kind of change."""
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for r in rows:
        base = r.get("base", r["arm"])
        groups[(r["workload"], r["store"], base, r.get("protocol", "published"), r.get("consistency", "default"),
                r["kind"])].append(r)
    old = {(b["store"], b["arm"], b["kind"]): b for b in baseline}
    out = []
    for (workload, store, base, protocol, consistency, kind), items in sorted(groups.items()):
        made = [r for r in items if not r.get("skipped")]
        shown = [r for r in made if not r["censored"]]
        delays = [r["delay_s"] for r in shown]
        stale_answers, errors, staleness, latencies, events_stale = 0, 0, [], [], 0
        for r in made:
            log_ = r.get("probe_log") or []
            before = log_[:-1] if not r["censored"] else log_
            wrong = 1 if kind == "revoke" else 0  # a revoked chunk still held, or a granted one still missing
            n = sum(1 for p in before if p[2] == wrong)
            stale_answers += n
            events_stale += n > 0
            errors += sum(1 for p in log_ if p[2] is None)
            latencies += [p[1] for p in log_]
            if not r["censored"] and log_:
                staleness.append(r["delay_s"] - log_[-1][1])
        pools: dict[str, int] = defaultdict(int)
        for r in made:
            if r.get("grant_pool"):
                pools[r["grant_pool"]] += 1
        entry = {
            "workload": workload, "store": store, "arm": base, "protocol": protocol, "consistency": consistency,
            "kind": kind, "events": len(made), "skipped": len(items) - len(made),
            "censored": sum(r["censored"] for r in made),
            "delay_s": np.percentile(delays, [50, 90, 100]).tolist() if delays else None,
            "delay_less_last_probe_s": np.percentile(staleness, [50, 90, 100]).tolist() if staleness else None,
            "stale_answers": stale_answers, "events_with_stale_answers": events_stale, "probe_errors": errors,
            "probe_latency_s": np.percentile(latencies, [50, 90, 100]).tolist() if latencies else None,
            "grant_pools": dict(pools),
        }
        if (protocol, consistency) == ("published", "default"):
            b = old.get((store, base, kind))
            entry["results_v1"] = {"events": b["events"], "censored": b["censored"], "delay_s": b["delay_s"]} if b else None
        out.append(entry)
    return out


def job_recalls(rows: list[dict]) -> dict[tuple, list[dict]]:
    """Each job's own recall in each cell (users' means within that job, then their mean), with its seed."""
    groups: dict[tuple, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for r in rows:
        groups[(r["workload"], r["store"], r["arm"], r["layout"])][r["job"]].append(r)
    out = {}
    for key, jobs in groups.items():
        out[key] = []
        for job, items in sorted(jobs.items()):
            means = list(report.user_means(items).values())
            out[key].append({"job": job, "seed": job.rsplit("-seed", 1)[-1],
                             "recall": float(np.mean(means)) if means else None})
    return out


def baseline_jobs(raw: Path, keys: set[tuple]) -> tuple[dict[tuple, list[dict]], dict[str, dict]]:
    """results-v1's per-job recall for the cells in `keys`, read from its raw outputs (one folder per job), and
    each job's load record of the store."""
    stores_of = {(k[0], k[1]) for k in keys}
    rows, loads = [], {}
    for meta_path in sorted(raw.rglob("*.meta.json")):
        name = meta_path.name.replace(".meta.json", "")
        meta = read_json(meta_path)
        workload, store = meta["workload"]["name"], meta["args"]["store"]
        scored = meta_path.with_name(f"{name}.scored.jsonl.gz")
        if (workload, store) not in stores_of or "-run-" not in name or not scored.exists():
            continue
        loads[name] = (meta.get("load") or {}).get("store")
        for r in read_jsonl_gz(scored):
            if (workload, store, r["arm"], r["layout"]) in keys:
                rows.append({**{k: r[k] for k in KEEP if k in r}, "workload": workload, "store": store, "job": name})
    return job_recalls(rows), loads


def reproduction(table: list[dict], baseline: list[dict], runs: list[dict] | None = None,
                 baseline_raw: Path | None = None) -> dict:
    """Every cell measured at ef 100 under a name results-v1 used, beside results-v1's cell; with the raw outputs
    of both, also each job's own recall (the registered cells pool the three jobs)."""
    old = {(c["workload"], c["store"], c["arm"], c["layout"]): c for c in baseline}
    compared = {(c["workload"], c["store"], c["base"], c["layout"]) for c in table
                if c["lookup"] is None and c["ef"] in (None, 100)}
    new_jobs = job_recalls([r for r in runs or [] if parse(r["arm"])[2] is None and parse(r["arm"])[1] in (None, 100)])
    old_jobs, old_loads = baseline_jobs(baseline_raw, compared) if baseline_raw else ({}, {})
    rows = []
    for c in table:
        if c["lookup"] is not None or c["ef"] not in (None, 100):
            continue
        b = old.get((c["workload"], c["store"], c["base"], c["layout"]))
        if b is None or c["recall"] is None or b["recall"] is None:
            continue
        lo, hi = c["recall_95"]
        rows.append({
            "workload": c["workload"], "store": c["store"], "arm": c["base"], "followup_arm": c["arm"],
            "layout": c["layout"], "results_v1": b["recall"], "results_v1_95": b["recall_95"],
            "followup": c["recall"], "followup_95": c["recall_95"], "difference": c["recall"] - b["recall"],
            "inside": lo <= b["recall"] <= hi,
            "intervals_overlap": lo <= b["recall_95"][1] and b["recall_95"][0] <= hi,
            "p50_ms": {"results_v1": b["p50_ms"]["median"], "followup": c["p50_ms"]["median"]},
            "p99_ms": {"results_v1": b["p99_ms"]["median"], "followup": c["p99_ms"]["median"]},
            "empty": {"results_v1": b["empty"], "followup": c["empty"]},
            "errors": {"results_v1": b["errors"], "followup": c["errors"]},
            "per_job": {
                "results_v1": [{**j, "store_load": old_loads.get(j["job"])} for j in
                               old_jobs.get((c["workload"], c["store"], c["base"], c["layout"]), [])],
                "followup": new_jobs.get((c["workload"], c["store"], c["arm"], c["layout"]), []),
            },
        })
    diffs = [abs(r["difference"]) for r in rows]
    ratios = [r["p50_ms"]["followup"] / r["p50_ms"]["results_v1"] for r in rows if r["p50_ms"]["results_v1"] > 0]
    return {
        "cells": len(rows), "inside": sum(r["inside"] for r in rows),
        "intervals_overlap": sum(r["intervals_overlap"] for r in rows),
        "largest_abs_difference": max(diffs) if diffs else None,
        "mean_abs_difference": float(np.mean(diffs)) if diffs else None,
        "p50_ratio": {"median": float(np.median(ratios)), "min": float(min(ratios)), "max": float(max(ratios))}
        if ratios else None,
        "outside": [r for r in rows if not r["inside"]],
        "rows": rows,
    }


# ---- presentation -------------------------------------------------------------------------------


def named(layout: str) -> str:
    """`w3_s0p01_neg` -> `w3_s0p01_neg (farthest first)`."""
    order = order_of(layout)
    return f"{layout} ({ORDERS[order]})" if order in ORDERS else layout


def _r(c: dict | None) -> str:
    if not c or c.get("recall") is None:
        return "-"
    lo, hi = c["recall_95"]
    return f"{c['recall']:.3f} [{lo:.3f}, {hi:.3f}]"


def _ms(value: float | None) -> str:
    if value is None:
        return "-"
    return f"{value:.0f}" if value >= 100 else f"{value:.1f}"


def _lat(c: dict | None) -> str:
    if not c:
        return "-"
    return f"{_ms(c['p50_ms']['median'])} / {_ms(c['p99_ms']['median'])}"


def markdown(table, sweep_rows, tune, look, churn_rows, repro, jobs) -> str:  # noqa: ANN001
    lines = ["# Follow-up runs (prereg/addendum-1.md): report", "",
             "Exploratory runs registered before they ran (release `prereg-addendum-1`). Recall@10 is the mean over "
             "users with a 95% bootstrap interval over users; latency is p50 / p99 in ms, each the median over the "
             "cell's jobs (their ranges are in the JSON files). No hypothesis is judged.", ""]
    kinds = defaultdict(int)
    for j in jobs:
        kinds[(j["plan"] or "registered", j["kind"])] += 1
    lines += ["## Jobs", "", "| plan | kind | jobs |", "|---|---|---|"]
    lines += [f"| {p} | {k} | {n} |" for (p, k), n in sorted(kinds.items())]
    stopped = [j for j in jobs if (j.get("status") or {}).get("stopped_at_budget") or
               (j.get("status") or {}).get("skipped_for_budget")]
    unscored = [j["job"] for j in jobs if j["rows"] is None]
    lines += ["", f"Jobs stopped by the 5-hour budget: {len(stopped)}"
              + (" (" + ", ".join(j["job"] for j in stopped) + ")" if stopped else "") + ".",
              f"Run jobs without a scored file: {len(unscored)}" + (" (" + ", ".join(unscored) + ")" if unscored else "")
              + ".", ""]

    lines += ["## F1: search breadth (W3, shares 0.01 and 0.05)", "",
              "Each entry: recall [95% interval]; p50 / p99 ms.", ""]
    by: dict[tuple, dict[int, dict]] = defaultdict(dict)
    for c in sweep_rows:
        by[(c["store"], c["base"], c["layout"])][c["ef"]] = c
    for store in sorted({k[0] for k in by}):
        lines += [f"### {store}", "", "| arm | layout | ef 40 | ef 100 | ef 400 |", "|---|---|---|---|---|"]
        for (s, base, layout), efs in sorted(by.items()):
            if s != store:
                continue
            cols = []
            for ef in (40, 100, 400):
                c = efs.get(ef)
                cols.append(f"{_r(c)}; {_lat(c)}" if c else "-")
            lines.append(f"| {base} | {named(layout)} | " + " | ".join(cols) + " |")
        lines.append("")

    lines += ["## F1: which A4 settings reach a mean recall of 0.9", "",
              "| layout | store | H6 interval in results-v1 | highest mean (arm, p50 / p99 ms) | arms with mean >= 0.9 "
              "(p50 ms) | arms with interval >= 0.9 |", "|---|---|---|---|---|---|"]
    for t in tune:
        h6 = t["h6_results_v1"]
        h6s = f"[{h6[0]:.3f}, {h6[1]:.3f}]" if h6 else "-"
        best = t["highest"]
        bests = f"{best['recall']:.3f} ({best['arm']}, {_ms(best['p50_ms'])} / {_ms(best['p99_ms'])})" if best else "-"
        reach = ", ".join(f"{x['arm']} ({_ms(x['p50_ms'])})" for x in t["mean_at_least_0p9"]) or "none"
        sure = ", ".join(x["arm"] for x in t["interval_at_least_0p9"]) or "none"
        lines.append(f"| {named(t['layout'])} | {t['store']} | {h6s} | {bests} | {reach} | {sure} |")
    lines.append("")

    lines += ["## F2: cost of looking up a user's principals", "",
              "Per job p50 / p99 of the lookup alone (median over jobs, range in brackets).", "",
              "| workload | engine | queries | groups per user (mean) | lookup p50 ms | lookup p99 ms | errors | "
              "lists that differed |", "|---|---|---|---|---|---|---|---|"]
    for c in look["cost"]:
        p50, p99 = c["lookup_p50"], c["lookup_p99"]
        g = "-" if c["groups_found_mean"] is None else f"{c['groups_found_mean']:.1f}"
        lines.append(f"| {c['workload']} | {c['engine']} | {c['queries']} | {g} | "
                     f"{_ms(p50['median'])} [{_ms(p50['min'])}, {_ms(p50['max'])}] | "
                     f"{_ms(p99['median'])} [{_ms(p99['min'])}, {_ms(p99['max'])}] | {c['errors']} | "
                     f"{c['principals_differ']} |")
    lines += ["", "Each lookup arm beside the same arm without a lookup, in the same jobs (p50 / p99 ms, medians over "
              "jobs).", "", "| workload | store | layout | arm | without lookup | lookup | search | total |",
              "|---|---|---|---|---|---|---|---|"]
    for a in look["arms"]:
        w = a["without_ms"]
        lk, se = a["lookup_ms"] or {}, a["search_ms"] or {}

        def pair(x: dict | None) -> str:
            if not x or not x.get("p50"):
                return "-"
            return f"{_ms(x['p50']['median'])} / {_ms(x['p99']['median'])}"

        lines.append(f"| {a['workload']} | {a['store']} | {a['layout']} | {a['arm']} | "
                     f"{pair(w) if w else '-'} | {pair(lk)} | {pair(se)} | {pair(a['total_ms'])} |")
    lines.append("")

    lines += ["## F4: change diagnostic", "",
              "Delay from the last acknowledgement to the first probe that showed the change: median / 90th "
              "percentile / maximum, in s, over changes not censored. Stale answers: probes before that one that "
              "still held a revoked chunk, or still lacked a granted one.", "",
              "| arm | protocol | consistency | kind | changes | censored | delay s | delay less last probe s | "
              "stale answers (changes) | probe latency median s | results-v1 delay s |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]

    def trio(x: list | None) -> str:
        return "-" if not x else " / ".join(f"{v:.2f}" for v in x)

    for c in churn_rows:
        old = c.get("results_v1")
        latency = "-" if not c["probe_latency_s"] else f"{c['probe_latency_s'][0]:.3f}"
        lines.append(f"| {c['arm']} | {c['protocol']} | {c['consistency']} | {c['kind']} | {c['events']} | "
                     f"{c['censored']} | {trio(c['delay_s'])} | {trio(c['delay_less_last_probe_s'])} | "
                     f"{c['stale_answers']} ({c['events_with_stale_answers']}) | {latency} | "
                     f"{trio(old['delay_s']) if old else '-'} |")
    lines.append("")

    def four(x: float | None) -> str:
        return "-" if x is None else f"{x:.4f}"

    lines += ["## Reproduction of results-v1 at ef 100", "",
              f"Cells compared: {repro['cells']}. results-v1's mean inside the follow-up's 95% interval: "
              f"{repro['inside']}; the two intervals overlap: {repro['intervals_overlap']}. Largest absolute "
              f"difference in mean recall: {four(repro['largest_abs_difference'])}; mean absolute difference: "
              f"{four(repro['mean_abs_difference'])}.", ""]
    if repro["p50_ratio"]:
        r = repro["p50_ratio"]
        lines += [f"p50 latency, follow-up over results-v1 (median over cells of each cell's ratio of job medians): "
                  f"{r['median']:.2f} (range {r['min']:.2f} to {r['max']:.2f}).", ""]
    def jobs_of(entries: list[dict]) -> str:
        return ", ".join(f"{j['seed']}: {j['recall']:.3f}" for j in entries if j["recall"] is not None) or "-"

    lines += ["Cells whose results-v1 mean lies outside the follow-up's interval, with each job's own recall "
              "(seed: recall):", "",
              "| workload | store | arm | layout | results-v1 | follow-up | difference | results-v1 jobs | "
              "follow-up jobs |", "|---|---|---|---|---|---|---|---|---|"]
    for r in repro["outside"]:
        lo, hi = r["followup_95"]
        lines.append(f"| {r['workload']} | {r['store']} | {r['arm']} | {r['layout']} | {r['results_v1']:.3f} | "
                     f"{r['followup']:.3f} [{lo:.3f}, {hi:.3f}] | {r['difference']:+.3f} | "
                     f"{jobs_of(r['per_job']['results_v1'])} | {jobs_of(r['per_job']['followup'])} |")
    if not repro["outside"]:
        lines.append("| none | | | | | | | | |")
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--results", type=Path, required=True)
    p.add_argument("--baseline", type=Path, required=True, help="results-v1's report folder")
    p.add_argument("--baseline-raw", type=Path, default=None,
                   help="results-v1's raw outputs (one folder per job), for each job's own recall in the check")
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--resamples", type=int, default=10_000)
    p.add_argument("--seed", type=int, default=5)
    args = p.parse_args()
    runs, churn, jobs = load(args.results)
    table = cells(runs, args.seed, args.resamples)
    jobs_table = per_job(runs)
    baseline_cells = read_json(args.baseline / "cells.json")
    baseline_churn = read_json(args.baseline / "churn.json")
    h6 = {(p_["store"], p_["layout"]): p_["interval"]
          for p_ in read_json(args.baseline / "hypotheses.json")["H6"]["parts"] if p_.get("interval")}
    sweep_rows = sweep(table)
    tune = tunability(sweep_rows, h6)
    look = lookups(runs, table)
    churn_rows = churn_summary(churn, baseline_churn)
    repro = reproduction(table, baseline_cells, runs, args.baseline_raw)
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / "cells.json", table)
    write_json(out / "per_job.json", jobs_table)
    with open(out / "per_job.tsv", "w", newline="", encoding="utf-8") as f:
        fields = ["job", "workload", "store", "arm", "layout", "queries", "errors", "p50_ms", "p99_ms",
                  "lookup_p50_ms", "lookup_p99_ms", "search_p50_ms", "search_p99_ms"]
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(jobs_table)
    write_json(out / "sweep.json", sweep_rows)
    write_json(out / "tunability.json", tune)
    write_json(out / "lookup.json", look)
    write_json(out / "churn.json", churn_rows)
    write_json(out / "reproduction.json", repro)
    write_json(out / "jobs.json", jobs)
    (out / "followup.md").write_text(markdown(table, sweep_rows, tune, look, churn_rows, repro, jobs), encoding="utf-8")
    print(f"{len(jobs)} jobs, {len(runs)} answers, {len(churn)} change rows, {len(table)} cells; reproduction: "
          f"{repro['inside']} of {repro['cells']} cells inside the follow-up interval")


if __name__ == "__main__":
    main()
