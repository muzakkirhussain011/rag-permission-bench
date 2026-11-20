"""bench.extras2 on a small synthetic workload and made-up job outputs (no study data): the post-filter model predicts
an exact post-filter exactly, short and exact answers are counted, kept plans are summarized, and the change and
fault runs' records are read."""

from __future__ import annotations

import json
import sys

import numpy as np

from bench import analyze, devdata, extras2, report, truth
from bench.util import read_json, write_json, write_jsonl_gz
from bench.workload import Workload


def _post_filter(w: Workload, user: str, groups: list[str], q: int, m: int) -> list[int]:
    """An exact post-filter: the m nearest chunks, then the first ten the user may read."""
    scores = np.asarray(w.vectors, dtype=np.float32) @ w.queries[q]
    ids = np.arange(w.n)
    near = ids[np.lexsort((ids, -scores))][:m]
    mask = w.readable(user, groups)
    return [int(i) for i in near if mask[i]][:10]


def test_extras2_on_a_synthetic_workload(tmp_path, monkeypatch):
    wl, results, rep, out = tmp_path / "workloads", tmp_path / "artifacts", tmp_path / "report", tmp_path / "out"
    devdata.build(wl / "dev", n=1500, n_queries=20)
    w = Workload(wl / "dev")
    write_jsonl_gz(wl / "dev" / "truth.jsonl.gz", truth.compute(w, k=10, nn=200))
    exact = {(t["layout"], t["user"], t["q"]): t for t in truth.compute(w, k=10, nn=200)}

    raw = []
    for layout in w.layouts:
        for user, q in layout.queries:
            groups = layout.user_groups.get(user, [])
            for arm, m in (("a1-spicedb", 10), ("a2-spicedb-x10", 100)):
                raw.append({"arm": arm, "layout": layout.name, "user": user, "q": q,
                            "hits": _post_filter(w, user, groups, q, m), "scores": [], "ms": 2.0, "error": None})
            raw.append({"arm": "a4@default", "layout": layout.name, "user": user, "q": q,
                        "hits": exact[(layout.name, user, q)]["ids"], "scores": [], "ms": 1.0, "error": None})
    t = {(x["layout"], x["user"], x["q"]): x for x in truth.compute(w, k=10, nn=200)}
    _, _, scored = analyze.summarize(w, raw, t)
    plan = {"Plan": {"Node Type": "Limit", "Actual Rows": 3, "Plans": [
        {"Node Type": "Index Scan", "Index Name": "chunks_hnsw", "Filter": "(principals && $1)", "Plan Rows": 40,
         "Actual Rows": 3, "Actual Loops": 1, "Rows Removed by Filter": 97}]}, "Execution Time": 1.5}
    meta = {"args": {"store": "pgvector"}, "workload": {"name": "dev"}, "complete": True,
            "plans": [{"layout": "dev_few", "arm": "a4@default", "plan": plan}]}
    name = "measured-run-dev-pgvector-seed1"
    write_json(results / name / f"{name}.meta.json", meta)
    write_jsonl_gz(results / name / f"{name}.jsonl.gz", raw)
    write_jsonl_gz(results / name / f"{name}.scored.jsonl.gz", scored)

    churn = [{"arm": "a1-spicedb", "event": e, "kind": "revoke" if e % 2 == 0 else "grant", "layout": "dev_few",
              "user": "dev_few_u0", "chunk": e, "write_s": {}, "delay_s": 0.1, "censored": False, "probes": 1 + e}
             for e in range(4)]
    name = "measured-churn-dev-pgvector-seed1"
    write_json(results / name / f"{name}.meta.json", {**meta, "plans": []})
    write_jsonl_gz(results / name / f"{name}.jsonl.gz", churn)
    faults = [{**r, "arm": f"a1-spicedb|{fault}"} for fault in ("none", "stopped") for r in scored[:5]]
    name = "measured-faults-dev-pgvector-seed1"
    write_json(results / name / f"{name}.meta.json", {**meta, "plans": []})
    write_jsonl_gz(results / name / f"{name}.jsonl.gz", [])
    write_jsonl_gz(results / name / f"{name}.scored.jsonl.gz", faults)

    loaded, _, _, _ = report.load(results)
    write_json(rep / "cells.json", report.cells(loaded, 5, 50))

    monkeypatch.setattr(sys, "argv", ["extras2", "--results", str(results), "--report", str(rep), "--workloads", str(wl),
                                      "--out", str(out), "--nn", "200"])
    extras2.main()

    for part in ("model", "answers", "plans", "pairs", "churn-faults", "order"):
        assert (out / f"{part}.md").exists() and (out / f"{part}.json").exists(), part
    assert (out / "README.md").exists()
    model = read_json(out / "model.json")
    assert model["registered_analysis"] is False
    gaps = {(s["arms"], s["kind"]): s for s in model["summary"]}
    assert gaps[("a1", None)]["max_abs"] < 1e-12 and gaps[("a2", None)]["max_abs"] < 1e-12
    answers = read_json(out / "answers.json")
    assert answers["check"]["max_abs_recall_difference"] < 1e-12
    a4 = [c for c in answers["cells"] if c["arm"] == "a4@default"]
    assert all(c["short"] == 0 and c["exact_share"] == 1.0 for c in a4)
    plans = read_json(out / "plans.json")["plans"]
    assert plans[0]["hnsw_plans"] == 1 and plans[0]["estimated_rows"] == [40]
    first = w.layouts[0].queries[0]
    readable = int(w.readable(first[0], w.layouts[0].user_groups.get(first[0], [])).sum())
    assert plans[0]["planned_pair_readable"] == readable
    cf = read_json(out / "churn-faults.json")
    assert cf["churn"]["revoke_then_grant_alternate_in_every_job_and_arm"] is True
    revoke = next(e for e in cf["churn"]["events"] if e["kind"] == "revoke")
    assert revoke["answers_before_it_showed"] == 0 + 2  # probes 1 and 3
    assert cf["faults"]["same_pairs_for_every_arm_and_fault_within_a_job"] is True
    json.loads((out / "order.json").read_text(encoding="utf-8"))
