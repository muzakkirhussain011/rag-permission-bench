"""Supplementary analyses of a measured release, second part (reports/extras-results-v1b), run in GitHub Actions by
`extras.yml` (part `v1b`). None of this is the registered analysis (`bench.report`), and nothing here runs a store or
an engine: every number comes from the release's raw outputs, its report and the workloads' published files.

    python -m bench.extras2 --results artifacts/ --report report/ --workloads workloads/ --out extras2/
        [--release results-v1] [--checksums SHA256SUMS] [--nn 300]

`--workloads` holds each workload release extracted into its own folder, with the corpus's `vectors.npy` and
`queries.npy` beside it (W2's folders may hold the whole MS MARCO corpus: only its first `n_chunks` rows are read).

- (d) The post-filter model. A post-filter that checks the m nearest chunks of an unfiltered search and keeps the first
  k readable ones returns readable chunks that are necessarily among the k nearest readable ones, so with an exact
  search its recall@k is min(k, readable among the m nearest) / min(k, readable). This part computes that prediction
  for every (layout, user, question) from the exact unfiltered neighbours of each question, for m = 10, 30, 100, 200
  and 300, and sets it beside the measured recall of the post-filters (A1: m = k; A2: m = 3k and 10k) and of
  OpenSearch's document-level security. It also sets the measured A1 beside sigma_l, the readable share of each
  question's 2,048 nearest chunks (`bench.truth`).
- (e) Answers per cell: queries, recall (`bench.report`'s estimator), answers with fewer hits than min(k, readable)
  ("short"; an exact search never returns one), answers with recall 1, empty answers; W1 also by question kind; the
  store filter's short and exact answers by how many chunks the user may read.
- (f) pgvector's executed plans, one per layout, setting and job, as `bench.run` kept them: the plan's shape, the
  planner's estimate of the rows the principals condition matches against the rows it did, and the rows returned.
- (g) The engine pre-filter (A3) and the store filter (A4) on the same (job, user, question) pairs where A3 answered
  a subset; on Qdrant, how often a setting changed the hits of the same query.
- (h) Change and fault runs: which layouts their users and pairs came from, probes before a change showed, and the
  fault runs' latencies by fault.
- (i) Latency: whether an arm's place in its job's order goes with its latency.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from . import report
from .truth import unfiltered_neighbours
from .util import log, read_json, read_jsonl_gz, write_json
from .workload import Workload

K = 10
MS = (10, 30, 100, 200, 300)
# Readable-count bins for the store filter's answers (part e): fine around W3's achieved counts at each share.
EDGES = (0, 100, 200, 500, 1000, 1250, 1500, 1750, 2000, 2500, 3000, 5000, 10000, 10500, 11000, 11500, 12500, 20000,
         40000, 50000, 51000, 60000, 100000, 200000, 500000, 10**9)
POST = {"a1-fga": 10, "a1-spicedb": 10, "a2-fga-x3": 30, "a2-spicedb-x3": 30, "a2-fga-x10": 100,
        "a2-spicedb-x10": 100}
SHARE_OF = {"0p001": 0.001, "0p01": 0.01, "0p05": 0.05, "0p2": 0.2, "0p5": 0.5}


def fmt(x: object, digits: int = 3) -> str:
    return f"{x:.{digits}f}" if isinstance(x, (int, float)) and not isinstance(x, bool) else "n/a"


def share_of(layout: str) -> str:
    m = re.match(r"w3_s([0-9p]+)_", layout)
    return m.group(1) if m else ""


def estimate(per_user: dict[str, list[float]]) -> float | None:
    """`bench.report`'s estimator: each user's mean, then the mean over users."""
    means = [float(np.mean(v)) for v in per_user.values() if v]
    return float(np.mean(means)) if means else None


def job_kind(name: str) -> str:
    return "churn" if "-churn-" in name else "faults" if "-faults-" in name else "run"


def seed_of(name: str) -> str:
    m = re.search(r"seed(\d+)$", name)
    return m.group(1) if m else "?"


# ---------------------------------------------------------------- (d) the post-filter model


def open_workload(folder: Path) -> Workload:
    w = Workload(folder)
    n = int(w.meta["n_chunks"])
    if w.vectors.shape[0] > n:  # W2 reads the first n passages of the corpus
        w.vectors = w.vectors[:n]
    return w


def sorted_neighbours(w: Workload, qs: list[int], nn: int) -> dict[int, np.ndarray]:
    """Each question's nn nearest chunks by inner product, best first, ties broken by chunk id (as `bench.truth`)."""
    queries = np.asarray(w.queries[qs], dtype=np.float32)
    ids = unfiltered_neighbours(w.vectors, queries, min(nn, w.n))
    out = {}
    for j, q in enumerate(qs):
        row = np.sort(np.asarray(ids[j], dtype=np.int64))
        scores = np.asarray(w.vectors[row], dtype=np.float32) @ queries[j]
        out[q] = row[np.lexsort((row, -scores))]
    return out


def model(folder: Path, nn: int) -> tuple[str, dict]:
    """Per (layout, user, question): readable among the m nearest, the prediction for each m, sigma_l, kind."""
    w = open_workload(folder)
    name = w.meta["name"]
    truth = {(t["layout"], t["user"], t["q"]): t for t in read_jsonl_gz(folder / "truth.jsonl.gz")}
    qs = sorted({q for layout in w.layouts for _, q in layout.queries})
    log(f"extras2: {name}: neighbours of {len(qs)} questions over {w.n:,} chunks")
    near = sorted_neighbours(w, qs, nn)
    pairs: dict[tuple, dict] = {}
    checked = 0
    for layout in w.layouts:
        kinds = layout.params.get("kinds") or {}
        by_user: dict[str, list[int]] = defaultdict(list)
        for user, q in layout.queries:
            by_user[user].append(q)
        for user, user_qs in by_user.items():
            mask = w.readable(user, layout.user_groups.get(user, []))
            r = int(mask.sum())
            for q in user_qs:
                t = truth[(layout.name, user, q)]
                if checked < 50:  # the masks agree with the exact answers the study scored against
                    assert t["n_readable"] == r, (layout.name, user, q, t["n_readable"], r)
                    checked += 1
                hits = np.cumsum(mask[near[q]])
                counts = {m: int(hits[min(m, len(hits)) - 1]) for m in MS}
                pairs[(layout.name, user, q)] = {
                    "n_readable": r, "readable_in": counts,
                    "pred": {m: (min(K, c) / min(K, r) if r else None) for m, c in counts.items()},
                    "sigma_l": t.get("sigma_l"), "kind": kinds.get(f"{user}|{q}")}
        log(f"extras2: {name}: layout {layout.name} done")
    return name, pairs


# ---------------------------------------------------------------- one pass over the raw outputs


def walk_plan(node: dict) -> str:
    label = node.get("Node Type", "?") + (f"[{node['Index Name']}]" if node.get("Index Name") else "")
    kids = [walk_plan(c) for c in node.get("Plans", [])]
    return label + (f"({', '.join(kids)})" if kids else "")


def principals_node(node: dict) -> dict | None:
    """The deepest node whose condition mentions the principals."""
    found = None
    for c in node.get("Plans", []):
        found = principals_node(c) or found
    if found is None and any("principals" in str(node.get(k, "")) for k in ("Index Cond", "Recheck Cond", "Filter")):
        found = node
    return found


def summarize_plan(entry: dict) -> dict:
    plan = entry["plan"]
    top = plan.get("Plan", plan) if isinstance(plan, dict) else plan[0]["Plan"]
    node = principals_node(top) or {}
    loops = node.get("Actual Loops", 1) or 1
    return {"layout": entry["layout"], "arm": entry["arm"], "shape": walk_plan(top),
            "uses_hnsw": "chunks_hnsw" in walk_plan(top),
            "principals_node": node.get("Node Type"), "estimated_rows": node.get("Plan Rows"),
            "actual_rows": (node.get("Actual Rows", 0) or 0) * loops if node else None,
            "removed_by_filter": node.get("Rows Removed by Filter"), "rows_returned": top.get("Actual Rows"),
            "execution_ms": plan.get("Execution Time") if isinstance(plan, dict) else None}


def scan(results: Path) -> dict:
    cells: dict[tuple, dict] = defaultdict(lambda: {"per_user": defaultdict(list), "queries": 0, "short": 0,
                                                    "exact": 0, "empty": 0, "errors": 0})
    kinds: dict[tuple, dict] = defaultdict(lambda: {"per_user": defaultdict(list), "queries": 0, "empty": 0,
                                                    "short": 0})
    by_readable: dict[tuple, Counter] = defaultdict(Counter)  # (workload, store, arm, bin) -> answers, short, exact
    joined: dict[tuple, float] = {}  # (store, layout, arm, job, user, q) -> recall, for A3 and A4 at shares >= 0.05
    order: list[dict] = []  # per run job and cell: the arm's position and its p50
    plans: list[dict] = []
    churn: list[dict] = []
    faults: list[dict] = []
    same_hits: dict[tuple, Counter] = defaultdict(Counter)
    for meta_path in sorted(results.rglob("*.meta.json")):
        name = meta_path.name[: -len(".meta.json")]
        if name.startswith("pilot"):
            raise SystemExit(f"{meta_path} is a pilot; pilots are never reported")
        meta = read_json(meta_path)
        workload, store, kind = meta["workload"]["name"], meta["args"]["store"], job_kind(name)
        if kind == "churn":
            for r in read_jsonl_gz(meta_path.with_name(f"{name}.jsonl.gz")):
                churn.append({**r, "store": store, "job": name, "seed": seed_of(name)})
            continue
        rows = read_jsonl_gz(meta_path.with_name(f"{name}.scored.jsonl.gz"))
        if kind == "faults":
            for r in rows:
                arm, _, fault = r["arm"].partition("|")
                faults.append({"store": store, "seed": seed_of(name), "arm": arm, "fault": fault or "none",
                               "pair": (r["layout"], r["user"], r["q"]), "ms": r["ms"], "error": bool(r["error"])})
            continue
        for p in meta.get("plans", []):
            plans.append({"workload": workload, "job": name, **summarize_plan(p)})
        position: dict[str, int] = {}
        per_job: dict[tuple, list[float]] = defaultdict(list)
        for r in rows:
            arm, layout = r["arm"], r["layout"]
            position.setdefault(arm, len(position))
            per_job[(arm, layout)].append(r["ms"])
            value = report.recall_of(r)
            c = cells[(workload, store, arm, layout)]
            c["queries"] += 1
            c["errors"] += bool(r["error"])
            if value is not None:
                c["per_user"][r["user"]].append(value)
            if not r["error"] and r["n_readable"]:
                short = r["n_hits"] < min(K, r["n_readable"])
                c["short"] += short
                c["exact"] += value == 1.0
                c["empty"] += bool(r["empty"])
                if arm.startswith("a4@"):
                    b = next(i for i in range(len(EDGES) - 1) if r["n_readable"] < EDGES[i + 1])
                    x = by_readable[(workload, store, arm, b)]
                    x["answers"] += 1
                    x["short"] += short
                    x["exact"] += value == 1.0
            if r.get("kind"):
                x = kinds[(workload, store, arm, layout, r["kind"])]
                x["queries"] += 1
                if value is not None:
                    x["per_user"][r["user"]].append(value)
                if not r["error"]:
                    x["empty"] += bool(r["empty"])
                    x["short"] += bool(r["n_readable"]) and r["n_hits"] < min(K, r["n_readable"])
            if workload == "w3" and share_of(layout) in ("0p05", "0p2", "0p5") and arm.startswith(("a3-", "a4@")):
                joined[(store, layout, arm, name, r["user"], r["q"])] = value
        for (arm, layout), ms in per_job.items():
            order.append({"workload": workload, "store": store, "arm": arm, "layout": layout, "job": name,
                          "position": position[arm], "arms": len(position), "p50": float(np.percentile(ms, 50)),
                          "queries": len(ms), "over_30s": sum(x > report.TIMEOUT_MS for x in ms)})
        if store == "qdrant" and workload == "w3":
            hits: dict[tuple, list] = {}
            for r in read_jsonl_gz(meta_path.with_name(f"{name}.jsonl.gz")):
                hits[(r["arm"], r["layout"], r["user"], r["q"])] = r["hits"]
            for (arm, layout, user, q), h in hits.items():
                if arm.endswith("@default"):
                    other = hits.get((arm.replace("@default", "@acorn"), layout, user, q))
                    if other is not None:
                        same_hits[(arm.split("@")[0], layout)]["same" if other == h else "different"] += 1
        log(f"extras2: read {name}")
    return {"cells": cells, "kinds": kinds, "joined": joined, "order": order, "plans": plans, "churn": churn,
            "faults": faults, "same_hits": same_hits, "by_readable": by_readable}


# ---------------------------------------------------------------- assembling each part


def part_answers(scanned: dict, published: list[dict]) -> dict:
    pub = {(c["workload"], c["store"], c["arm"], c["layout"]): c for c in published}
    cells, worst = [], 0.0
    for key, c in sorted(scanned["cells"].items()):
        recall = estimate(c["per_user"])
        p = pub.get(key)
        if p is not None and recall is not None and p["recall"] is not None:
            worst = max(worst, abs(recall - p["recall"]))
        answered = c["queries"] - c["errors"]
        cells.append({"workload": key[0], "store": key[1], "arm": key[2], "layout": key[3], "queries": c["queries"],
                      "recall": recall, "short": c["short"], "exact": c["exact"], "empty": c["empty"],
                      "errors": c["errors"], "short_share": c["short"] / answered if answered else None,
                      "exact_share": c["exact"] / answered if answered else None})
    by_kind = [{"workload": k[0], "store": k[1], "arm": k[2], "layout": k[3], "kind": k[4], "queries": x["queries"],
                "recall": estimate(x["per_user"]), "empty": x["empty"], "short": x["short"]}
               for k, x in sorted(scanned["kinds"].items())]
    by_readable = [{"workload": k[0], "store": k[1], "arm": k[2], "readable_from": EDGES[k[3]],
                    "readable_below": EDGES[k[3] + 1], "answers": x["answers"], "short": x["short"],
                    "exact": x["exact"]} for k, x in sorted(scanned["by_readable"].items())]
    return {"cells": cells, "by_kind": by_kind, "by_readable": by_readable,
            "check": {"cells": len(cells), "published": len(pub), "max_abs_recall_difference": worst}}


def part_model(models: dict[str, dict], answers: dict) -> dict:
    measured = {(c["workload"], c["store"], c["arm"], c["layout"]): c["recall"] for c in answers["cells"]}
    measured_kind = {(c["workload"], c["store"], c["arm"], c["layout"], c["kind"]): c["recall"]
                     for c in answers["by_kind"]}
    rows, gaps = [], defaultdict(list)
    for workload, pairs in models.items():
        groups: dict[tuple, list] = defaultdict(list)
        for (layout, user, q), p in pairs.items():
            groups[(layout, None)].append((user, p))
            if p["kind"]:
                groups[(layout, p["kind"])].append((user, p))
        for (layout, kind), items in sorted(groups.items(), key=lambda x: (x[0][0], x[0][1] or "")):
            pred = {}
            for m in MS:
                per: dict[str, list[float]] = defaultdict(list)
                for user, p in items:
                    if p["pred"][m] is not None:
                        per[user].append(p["pred"][m])
                pred[m] = estimate(per)
            per_sl: dict[str, list[float]] = defaultdict(list)
            for user, p in items:
                if p["sigma_l"] is not None:
                    per_sl[user].append(p["sigma_l"])
            row = {"workload": workload, "layout": layout, "kind": kind, "pairs": len(items),
                   "predicted": {str(m): v for m, v in pred.items()}, "sigma_l": estimate(per_sl), "measured": {}}
            for store in report.STORES:
                for arm in (*POST, "a5-dls"):
                    v = (measured_kind.get((workload, store, arm, layout, kind)) if kind
                         else measured.get((workload, store, arm, layout)))
                    if v is None:
                        continue
                    row["measured"][f"{store}|{arm}"] = v
                    if arm in POST and v is not None and pred[POST[arm]] is not None:
                        gaps[(workload, arm[:2], kind)].append(v - pred[POST[arm]])
                    if arm.startswith("a1") and workload == "w3" and row["sigma_l"] is not None:
                        gaps[("w3", "a1-vs-sigma_l", None)].append(v - row["sigma_l"])
            rows.append(row)
    summary = [{"workload": w, "arms": a, "kind": k, "n": len(v), "min": float(min(v)), "max": float(max(v)),
                "max_abs": float(max(abs(x) for x in v)), "mean": float(np.mean(v))}
               for (w, a, k), v in sorted(gaps.items(), key=lambda x: tuple(str(y) for y in x[0]))]
    return {"rows": rows, "summary": summary}


def part_plans(scanned: dict, models: dict[str, dict]) -> dict:
    out = []
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for p in scanned["plans"]:
        groups[(p["workload"], p["layout"], p["arm"])].append(p)
    planned = {}  # bench.run plans each layout's first pair; the model's pairs keep the layout's order
    for workload, pairs in models.items():
        for (layout, user, q), p in pairs.items():
            planned.setdefault((workload, layout), {"user": user, "q": q, "n_readable": p["n_readable"]})
    for (workload, layout, arm), items in sorted(groups.items()):
        out.append({"workload": workload, "layout": layout, "arm": arm, "jobs": len(items),
                    "planned_pair_readable": (planned.get((workload, layout)) or {}).get("n_readable"),
                    "shapes": dict(Counter(p["shape"] for p in items)),
                    "hnsw_plans": sum(p["uses_hnsw"] for p in items),
                    "estimated_rows": sorted({p["estimated_rows"] for p in items if p["estimated_rows"] is not None}),
                    "actual_rows": sorted({p["actual_rows"] for p in items if p["actual_rows"] is not None}),
                    "removed_by_filter": sorted({p["removed_by_filter"] for p in items
                                                 if p["removed_by_filter"] is not None}),
                    "rows_returned": sorted({p["rows_returned"] for p in items if p["rows_returned"] is not None}),
                    "execution_ms": sorted(round(p["execution_ms"], 2) for p in items if p["execution_ms"] is not None)})
    return {"plans": out}


def part_pairs(scanned: dict) -> dict:
    by_cell: dict[tuple, dict[tuple, dict]] = defaultdict(lambda: defaultdict(dict))
    for (store, layout, arm, job, user, q), v in scanned["joined"].items():
        by_cell[(store, layout)][(job, user, q)][arm] = v
    rows = []
    for store in report.STORES:
        for setting in report.SETTINGS[store]:
            for layout in report.W3_LAYOUTS:
                a3, a4 = defaultdict(list), defaultdict(list)
                n = 0
                for (_, user, _), arms in by_cell.get((store, layout), {}).items():
                    x, y = arms.get(f"a3-spicedb@{setting}"), arms.get(f"a4@{setting}")
                    if x is None or y is None:
                        continue
                    a3[user].append(x)
                    a4[user].append(y)
                    n += 1
                if n:
                    rows.append({"store": store, "setting": setting, "layout": layout, "pairs": n,
                                 "a3_recall": estimate(a3), "a4_recall_same_pairs": estimate(a4)})
    same = [{"arm": arm, "layout": layout, "same": c["same"], "different": c["different"]}
            for (arm, layout), c in sorted(scanned["same_hits"].items())]
    return {"pairs": rows, "qdrant_settings_same_hits": same}


def part_churn_faults(scanned: dict) -> dict:
    churn = scanned["churn"]
    by: dict[tuple, list[dict]] = defaultdict(list)
    for r in churn:
        if not r.get("skipped"):
            by[(r["store"], r["arm"], r["kind"])].append(r)
    events = []
    for (store, arm, kind), rows in sorted(by.items()):
        probes = [r["probes"] for r in rows]
        events.append({"store": store, "arm": arm, "kind": kind, "events": len(rows),
                       "answers_before_it_showed": int(sum(p - 1 for p in probes)),
                       "probes_median": float(np.median(probes)), "probes_max": int(max(probes))})
    sequence = defaultdict(list)
    for r in churn:
        sequence[(r["job"], r["arm"])].append((r["event"], r["kind"]))
    alternating = all([k for _, k in sorted(v)] == ["revoke" if e % 2 == 0 else "grant" for e, _ in sorted(v)]
                      for v in sequence.values())
    churn_layouts = Counter(share_of(r["layout"]) for r in churn if not r.get("skipped"))
    churn_users = len({(r["layout"], r["user"]) for r in churn})

    faults = scanned["faults"]
    sets: dict[tuple, set] = defaultdict(set)
    for r in faults:
        sets[(r["seed"], r["store"], r["arm"], r["fault"])].add(r["pair"])
    per_seed: dict[str, set] = defaultdict(set)
    per_job: dict[tuple, set] = defaultdict(set)
    for (seed, store, _, _), pairs in sets.items():
        per_seed[seed].add(frozenset(pairs))
        per_job[(seed, store)].add(frozenset(pairs))
    same_within_seed = all(len(v) == 1 for v in per_seed.values())
    same_within_job = all(len(v) == 1 for v in per_job.values())
    distinct = {seed: len(next(iter(v))) for seed, v in per_seed.items()}
    all_pairs = set().union(*(next(iter(v)) for v in per_seed.values())) if per_seed else set()
    fault_layouts = Counter(share_of(p[0]) for p in all_pairs)
    latency: dict[tuple, list[float]] = defaultdict(list)
    for r in faults:
        fam = "a1-fga" if r["arm"] == "a1-fga" else "a2-fga" if r["arm"].startswith("a2-fga") else \
            "a1-spicedb" if r["arm"] == "a1-spicedb" else "a2-spicedb" if r["arm"].startswith("a2-spicedb") else \
            r["arm"].split("@")[0]
        latency[(fam, r["fault"])].append(r["ms"])
    lat = [{"arms": a, "fault": f, "queries": len(v), "median_ms": float(np.median(v)),
            "p90_ms": float(np.percentile(v, 90))} for (a, f), v in sorted(latency.items())]
    return {"churn": {"events": events, "revoke_then_grant_alternate_in_every_job_and_arm": alternating,
                      "events_by_share": dict(churn_layouts), "distinct_layout_users": churn_users},
            "faults": {"same_pairs_for_every_arm_and_fault_within_a_job": same_within_job,
                       "same_pairs_for_every_store_arm_and_fault_within_a_seed": same_within_seed,
                       "pairs_per_seed": distinct, "distinct_pairs_over_seeds": len(all_pairs),
                       "pairs_by_share": dict(fault_layouts), "latency_by_fault": lat}}


def part_order(scanned: dict) -> dict:
    cells: dict[tuple, list[dict]] = defaultdict(list)
    for o in scanned["order"]:
        cells[(o["workload"], o["store"], o["arm"], o["layout"])].append(o)
    earliest_slowest, compared, ratios, concordant, pairs = 0, 0, [], 0, 0
    for items in cells.values():
        if len(items) < 2 or len({o["position"] for o in items}) < 2:
            continue
        items = sorted(items, key=lambda o: o["position"])
        compared += 1
        earliest_slowest += items[0]["p50"] == max(o["p50"] for o in items)
        if items[-1]["p50"] > 0:
            ratios.append(items[0]["p50"] / items[-1]["p50"])
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                if items[i]["position"] != items[j]["position"]:
                    pairs += 1
                    concordant += items[i]["p50"] > items[j]["p50"]
    slow = [{"workload": k[0], "store": k[1], "arm": k[2], "layout": k[3],
             "jobs": [{"job": o["job"], "queries": o["queries"], "over_30s": o["over_30s"], "p50_ms": o["p50"]}
                      for o in sorted(v, key=lambda o: o["job"])]}
            for k, v in sorted(cells.items()) if any(o["over_30s"] for o in v)]
    return {"cells_compared": compared, "earliest_was_slowest": earliest_slowest,
            "expected_if_unrelated": compared / 3 if compared else None,
            "job_pairs": pairs, "earlier_slower_share": concordant / pairs if pairs else None,
            "median_ratio_earliest_to_latest_p50": float(np.median(ratios)) if ratios else None,
            "cells_with_calls_over_30s": slow}


# ---------------------------------------------------------------- markdown


def md_model(m: dict) -> str:
    out = ["# (d) The post-filter model against the measurements", "",
           "A post-filter asks an unfiltered search for its m nearest chunks and keeps the first k = 10 the user may "
           "read. Any readable chunk among the m nearest is among the k nearest readable chunks whenever fewer than k "
           "readable chunks come before it, so with an exact unfiltered search the post-filter's recall@10 is "
           "min(10, readable among the m nearest) / min(10, readable). The predicted values below use each "
           "question's exact unfiltered neighbours (inner product, ties by chunk id) and each user's readable set "
           "from the workload release, averaged as `bench.report` averages recall (per user, then over users). A1 "
           "checks m = 10, A2 m = 30 and m = 100. The measured values are the post-filters' recall from the raw "
           "outputs; the differences come from the stores' approximate unfiltered search and from ties. sigma_l is "
           "the readable share of each question's 2,048 nearest chunks (`bench.truth`), averaged the same way.", "",
           "## Measured minus predicted, over every store and cell", "",
           "| workload | arms | question kind | cells | min | max | largest absolute |", "|---|---|---|---|---|---|---|"]
    names = {"a1": "A1 (m = 10)", "a2": "A2 (m = 30, 100)", "a1-vs-sigma_l": "A1 against sigma_l"}
    for s in m["summary"]:
        out.append(f"| {s['workload']} | {names.get(s['arms'], s['arms'])} | {s['kind'] or 'all'} | {s['n']} | "
                   f"{fmt(s['min'])} | {fmt(s['max'])} | {fmt(s['max_abs'])} |")
    out += ["", "## Per layout", "",
            "Predicted recall of a post-filter over the m nearest chunks; measured A1 and A2 (SpiceDB) as the range over "
            "stores; OpenSearch's document-level security.", "",
            "| workload | layout | kind | pairs | sigma_l | pred m=10 | A1 measured | pred m=30 | A2 3k measured | "
            "pred m=100 | A2 10k measured | pred m=200 | pred m=300 | DLS measured |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]

    def span(row: dict, arm: str) -> str:
        v = [x for k, x in row["measured"].items() if k.endswith(f"|{arm}") and x is not None]
        if not v:
            return ""
        lo, hi = fmt(min(v)), fmt(max(v))
        return lo if lo == hi else f"{lo} to {hi}"

    for r in m["rows"]:
        p = r["predicted"]
        out.append(f"| {r['workload']} | {r['layout']} | {r['kind'] or 'all'} | {r['pairs']} | {fmt(r['sigma_l'], 4)} | "
                   f"{fmt(p['10'])} | {span(r, 'a1-spicedb')} | {fmt(p['30'])} | {span(r, 'a2-spicedb-x3')} | "
                   f"{fmt(p['100'])} | {span(r, 'a2-spicedb-x10')} | {fmt(p['200'])} | {fmt(p['300'])} | "
                   f"{span(r, 'a5-dls')} |")
    return "\n".join(out)


def md_answers(a: dict) -> str:
    out = ["# (e) Answers per cell", "",
           "From every run job's scored rows. `short`: answers with fewer hits than min(10, readable) and no error; an "
           "exact search never returns one, so on pgvector a short answer of the filtered arms comes from a plan that "
           "filters the rows an index scan returns. `exact`: answers with recall 1. Shares are over the answers "
           "without an error. Recall is `bench.report`'s estimator; it matches the published `cells.json` to "
           f"{a['check']['max_abs_recall_difference']:.2e} over {a['check']['cells']} cells.", "",
           "## W3, the store-side arms", "",
           "| store | arm | layout | queries | recall | short | exact |", "|---|---|---|---|---|---|---|"]
    for c in a["cells"]:
        if c["workload"] == "w3" and c["arm"].startswith(("a0", "a3-", "a4@", "a5-", "a7-")):
            out.append(f"| {c['store']} | {c['arm']} | {c['layout']} | {c['queries']} | {fmt(c['recall'])} | "
                       f"{fmt(c['short_share'])} | {fmt(c['exact_share'])} |")
    out += ["", "## W1 and W2, every arm", "", "| workload | store | arm | queries | recall | empty | short | exact |",
            "|---|---|---|---|---|---|---|---|"]
    for c in a["cells"]:
        if c["workload"] != "w3":
            out.append(f"| {c['workload']} | {c['store']} | {c['arm']} | {c['queries']} | {fmt(c['recall'])} | "
                       f"{c['empty']} | {fmt(c['short_share'])} | {fmt(c['exact_share'])} |")
    out += ["", "## The store filter's answers by how many chunks the user may read", "",
            "Every workload pooled, per store and setting: answers whose user may read a number of chunks in the bin, "
            "how many were short and how many exact. Bins where every answer was exact are left out here (all are in "
            "`answers.json`).", "",
            "| workload | store | arm | readable from | below | answers | short | exact |", "|---|---|---|---|---|---|---|---|"]
    for x in a["by_readable"]:
        if x["exact"] < x["answers"]:
            out.append(f"| {x['workload']} | {x['store']} | {x['arm']} | {x['readable_from']:,} | {x['readable_below']:,} "
                       f"| {x['answers']} | {x['short']} | {x['exact']} |")
    out += ["", "## W1 by question kind (own mail, other mail)", "",
            "| store | arm | kind | queries | recall | empty | short |", "|---|---|---|---|---|---|---|"]
    for c in a["by_kind"]:
        out.append(f"| {c['store']} | {c['arm']} | {c['kind']} | {c['queries']} | {fmt(c['recall'])} | {c['empty']} | "
                   f"{c['short']} |")
    return "\n".join(out)


def md_plans(p: dict) -> str:
    out = ["# (f) pgvector's executed plans", "",
           "`bench.run` kept the executed plan (`EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)`) of one query per layout and "
           "setting in every pgvector run job: the first (user, question) pair of the layout, so the three jobs of a "
           "layout planned the same query on different runners. `a4@exact` is the exact control's setting (A0). "
           "`estimated` is the planner's row estimate for the node that applies the principals condition, `actual` "
           "the rows that node produced (over all loops), `removed` the rows its filter removed, `returned` the rows "
           "the query returned.", "",
           "`readable` is how many chunks the planned pair's user may read.", "",
           "| workload | layout | arm | jobs | plan shapes (jobs) | readable | estimated | actual | removed | returned | "
           "ms |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for x in p["plans"]:
        shapes = "; ".join(f"`{s}` ({n})" for s, n in x["shapes"].items())
        out.append(f"| {x['workload']} | {x['layout']} | {x['arm']} | {x['jobs']} | {shapes} | "
                   f"{x['planned_pair_readable']} | {x['estimated_rows']} | {x['actual_rows']} | "
                   f"{x['removed_by_filter']} | {x['rows_returned']} | {x['execution_ms']} |")
    return "\n".join(out)


def md_pairs(p: dict) -> str:
    out = ["# (g) The engine pre-filter and the store filter on the same pairs", "",
           "Where A3 answered a subset of the pairs (shares 0.05, 0.2 and 0.5), A4 at the same setting on exactly the "
           "(job, user, question) pairs A3 answered, averaged per user and then over users.", "",
           "| store | setting | layout | pairs | A3 recall | A4 recall, same pairs |", "|---|---|---|---|---|---|"]
    for r in p["pairs"]:
        out.append(f"| {r['store']} | {r['setting']} | {r['layout']} | {r['pairs']} | {fmt(r['a3_recall'])} | "
                   f"{fmt(r['a4_recall_same_pairs'])} |")
    out += ["", "## Qdrant: did ACORN change the hits of the same query?", "",
            "For each query an arm answered at both settings in one job, whether the hit lists at `default` and at "
            "`acorn` were identical.", "", "| arm | layout | identical | different |", "|---|---|---|---|"]
    for r in p["qdrant_settings_same_hits"]:
        out.append(f"| {r['arm']} | {r['layout']} | {r['same']} | {r['different']} |")
    return "\n".join(out)


def md_churn_faults(c: dict) -> str:
    ch, fa = c["churn"], c["faults"]
    out = ["# (h) Change and fault runs", "",
           "## Change runs (`bench.churn`)", "",
           f"- Kinds alternate revoke, grant, revoke, ... within every job and arm: "
           f"{ch['revoke_then_grant_alternate_in_every_job_and_arm']}.",
           f"- Change events by W3 share of the user's layout: {json.dumps(ch['events_by_share'], sort_keys=True)}; "
           f"distinct (layout, user) pairs: {ch['distinct_layout_users']}.",
           "- `answers before it showed`: probes answered before the one that reflected the change, summed over the "
           "events. For a revocation each such answer either held the revoked chunk or raised an error (the rows keep "
           "no per-probe record), so the sum is an upper bound on answers that held a revoked chunk.", "",
           "| store | arm | kind | events | answers before it showed | probes, median | probes, max |",
           "|---|---|---|---|---|---|---|"]
    for e in ch["events"]:
        out.append(f"| {e['store']} | {e['arm']} | {e['kind']} | {e['events']} | {e['answers_before_it_showed']} | "
                   f"{fmt(e['probes_median'], 1)} | {e['probes_max']} |")
    out += ["", "## Fault runs (`bench.faults`)", "",
            f"- Every arm and fault of a job answered the same pairs: "
            f"{fa['same_pairs_for_every_arm_and_fault_within_a_job']}.",
            f"- Every store, arm and fault of a seed answered the same pairs: "
            f"{fa['same_pairs_for_every_store_arm_and_fault_within_a_seed']}; pairs per seed: "
            f"{json.dumps(fa['pairs_per_seed'], sort_keys=True)}; distinct pairs over the seeds: "
            f"{fa['distinct_pairs_over_seeds']}.",
            f"- Those pairs by W3 share: {json.dumps(fa['pairs_by_share'], sort_keys=True)}.", "",
            "| arms | fault | queries | median ms | p90 ms |", "|---|---|---|---|---|"]
    for r in fa["latency_by_fault"]:
        out.append(f"| {r['arms']} | {r['fault']} | {r['queries']} | {fmt(r['median_ms'], 1)} | {fmt(r['p90_ms'], 1)} |")
    return "\n".join(out)


def md_order(o: dict) -> str:
    return "\n".join([
        "# (i) Arm order and latency", "",
        "Arms run one after another in an order drawn from each job's seed, each after ten unrecorded warm-up queries. "
        "For every cell (workload, store, arm, layout) whose jobs placed the arm at different positions, this compares "
        "the arm's p50 latency across its jobs. If position and latency were unrelated, the job that ran the arm "
        "earliest would be the slowest in about a third of three-job cells, and an earlier job would be the slower "
        "one in about half of the job pairs. Jobs also ran on different runners, which adds noise but not bias, since "
        "the order is drawn independently of the runner.", "",
        f"- Cells compared: {o['cells_compared']}; the earliest job was the slowest in {o['earliest_was_slowest']} "
        f"(about {fmt(o['expected_if_unrelated'], 0)} expected if unrelated).",
        f"- Job pairs at different positions: {o['job_pairs']}; the earlier one was slower in "
        f"{fmt(o['earlier_slower_share'])} of them.",
        f"- Median ratio of the earliest job's p50 to the latest job's: "
        f"{fmt(o['median_ratio_earliest_to_latest_p50'])}.", "",
        "## Cells with calls over 30 s, by job", "",
        "H4 counts a call over 30 s as failed. Per job: calls over 30 s of the job's calls, and the job's p50.", "",
        "| workload | store | arm | layout | jobs: over 30 s / calls (p50 ms) |", "|---|---|---|---|---|"]
        + [f"| {c['workload']} | {c['store']} | {c['arm']} | {c['layout']} | "
           + "; ".join(f"{j['over_30s']}/{j['queries']} ({j['p50_ms']:.0f})" for j in c["jobs"]) + " |"
           for c in o["cells_with_calls_over_30s"]])


def md_index(meta: dict, parts: dict) -> str:
    where = (f"workflow run {meta['run_id']} of {meta['repository']} (`.github/workflows/extras.yml`, part v1b)"
             if meta["run_id"] != "none" else "a run outside GitHub Actions")
    out = ["# Supplementary analyses of " + meta["release"] + ", second part", "",
           f"Made by `python -m bench.extras2` in {where}. None of this is the registered analysis (`bench.report`) "
           "and no store or engine ran: every number comes from the release's raw outputs and report and from the "
           "workload releases. The first part is `reports/extras-results-v1`.", "",
           f"- Release: `{meta['release']}`; its `SHA256SUMS` (checked before use):"]
    out += [f"  - `{line}`" for line in meta["checksums"]]
    out += [f"- Code: commit `{meta['git_sha']}`.", "", "| file | what it holds |", "|---|---|",
            "| `model.md`, `model.json` | (d) post-filter recall predicted from the exact unfiltered neighbours, against "
            "the measured post-filters and document-level security; A1 against sigma_l |",
            "| `answers.md`, `answers.json` | (e) per cell: recall, short answers, exact answers, empty answers; W1 by "
            "question kind |",
            "| `plans.md`, `plans.json` | (f) pgvector's kept executed plans: shape, estimated and actual rows |",
            "| `pairs.md`, `pairs.json` | (g) A3 and A4 on the same pairs; Qdrant's settings on the same queries |",
            "| `churn-faults.md`, `churn-faults.json` | (h) the change and fault runs' layouts, pairs and probes |",
            "| `order.md`, `order.json` | (i) arm order and latency |",
            "| `figures/` | the paper's figures, drawn by `bench.figures` at this commit from the published report (which "
            "`reports/extras-results-v1/rebuild.json` found identical to the one rebuilt from the raw outputs) |", "",
            "## In brief", ""]
    for s in parts["model"]["summary"]:
        out.append(f"- Model, {s['workload']} {s['arms']} {s['kind'] or 'all'}: measured minus predicted from "
                   f"{fmt(s['min'])} to {fmt(s['max'])} over {s['n']} cells.")
    o = parts["order"]
    out.append(f"- Arm order: the earliest job was the slowest in {o['earliest_was_slowest']} of "
               f"{o['cells_compared']} cells; an earlier job was slower in {fmt(o['earlier_slower_share'])} of "
               f"{o['job_pairs']} job pairs.")
    return "\n".join(out)


# ---------------------------------------------------------------- main


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--results", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--workloads", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--nn", type=int, default=max(MS))
    p.add_argument("--release", default="results-v1")
    p.add_argument("--checksums", type=Path, default=None)
    args = p.parse_args()
    meta = {"release": args.release, "git_sha": os.environ.get("GITHUB_SHA", "local"),
            "run_id": os.environ.get("GITHUB_RUN_ID", "none"), "repository": os.environ.get("GITHUB_REPOSITORY", "-"),
            "checksums": [x for x in (args.checksums.read_text(encoding="utf-8").split("\n") if args.checksums else [])
                          if x.strip()]}
    models = {}
    for folder in sorted(x.parent for x in args.workloads.glob("*/truth.jsonl.gz")):
        if (folder / "vectors.npy").exists():
            name, pairs = model(folder, args.nn)
            models[name] = pairs
    scanned = scan(args.results)
    parts = {"answers": part_answers(scanned, read_json(args.report / "cells.json"))}
    parts["model"] = part_model(models, parts["answers"])
    parts["plans"] = part_plans(scanned, models)
    parts["pairs"] = part_pairs(scanned)
    parts["churn-faults"] = part_churn_faults(scanned)
    parts["order"] = part_order(scanned)
    args.out.mkdir(parents=True, exist_ok=True)
    label = {"made_by": "bench.extras2", "registered_analysis": False, **meta}
    for name, obj in parts.items():
        write_json(args.out / f"{name}.json", {**label, **obj})
    writers = {"model": md_model, "answers": md_answers, "plans": md_plans, "pairs": md_pairs,
               "churn-faults": md_churn_faults, "order": md_order}
    for name, writer in writers.items():
        (args.out / f"{name}.md").write_text(writer(parts[name]) + "\n", encoding="utf-8")
    (args.out / "README.md").write_text(md_index(meta, parts) + "\n", encoding="utf-8")
    print(json.dumps({"model": parts["model"]["summary"], "answers_check": parts["answers"]["check"],
                      "order": parts["order"]}, indent=1))


if __name__ == "__main__":
    main()
