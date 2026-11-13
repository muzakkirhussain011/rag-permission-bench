"""bench.extras on made-up outputs (no study data): its estimator is bench.report's, resampling questions widens an
interval when answers depend on the question, and the whole pass runs on folders laid out as the releases are."""

from __future__ import annotations

import json
import sys

import numpy as np

from bench import extras, report
from bench.util import read_json, write_json, write_jsonl_gz


def test_draw_gives_counts_that_sum_to_n():
    w = extras.draw(np.random.default_rng(1), 7, 13)
    assert w.shape == (7, 13) and (w.sum(axis=1) == 13).all()


def test_estimate_with_unit_weights_is_the_registered_estimate():
    rng = np.random.default_rng(2)
    rows = [{"user": f"u{u}", "q": int(q), "recall": float(rng.random()), "n_readable": 10, "error": None}
            for u in range(6) for q in rng.choice(20, 4, replace=False)]
    rows.append({"user": "u0", "q": 99, "recall": None, "n_readable": 10, "error": "TimeoutError: x"})  # counts as 0
    expected = float(np.mean(list(report.user_means(rows).values())))
    entries = [(r["user"], r["q"], report.recall_of(r)) for r in rows]
    columns = extras.columns_of(entries)
    s, c = extras.matrix(entries, columns)
    got = extras.estimate(s, c, np.ones((1, s.shape[0])), np.ones((1, len(columns))))[0]
    assert abs(got - expected) < 1e-12


def test_resampling_questions_widens_an_interval_that_users_alone_cannot_see():
    # every user asks the same 20 questions, and recall depends on the question only
    entries = [(f"u{u}", q, float(q % 2)) for u in range(30) for q in range(20)]
    result = extras.part("H6", ("pgvector", "w3_s0p01_neg"), [entries], resamples=400, seed=5)
    lo, hi = result["users"]["interval"]
    assert hi - lo < 1e-12  # every user's mean is 0.5
    lo, hi = result["questions"]["interval"]
    assert hi - lo > 0.1
    assert result["n_users"] == [30] and result["n_questions"] == 20


def test_memory_and_container_names():
    assert extras.mem_bytes("1.5GiB ") == 1.5 * 2**30
    assert extras.mem_bytes("512MiB") == 512 * 2**20
    assert extras.mem_bytes("--") is None
    assert extras.service("bench-pgvector-1") == "pgvector"
    assert extras.service("bench-openfga-migrate-1") == "openfga-migrate"
    assert extras.mem_total_gib("MemTotal:       16777216 kB") == 16.0


def _scored(arm, layout, user, q, recall, kind=None, ms=5.0):
    return {"arm": arm, "layout": layout, "user": user, "q": q, "kind": kind, "ms": ms, "error": None,
            "n_readable": 100, "sigma_g": 0.01, "rho": 0.0, "recall": recall, "outside": 0, "empty": False,
            "n_hits": 10, "duplicates": 0}


def _job(root, name, workload, store, rows, load):
    meta = {"args": {"store": store}, "workload": {"name": workload}, "complete": True,
            "environment": {"cpus": 4, "memory": "MemTotal:       16777216 kB", "runner": "runner-1", "git_sha": "abc",
                            "run_id": "7"},
            "load": load,
            "docker_stats_after": [json.dumps({"Name": f"bench-{store}-1", "MemUsage": "1.5GiB / 15.6GiB"}),
                                   json.dumps({"Name": "bench-spicedb-1", "MemUsage": "200MiB / 15.6GiB"})]}
    write_json(root / name / f"{name}.meta.json", meta)
    write_jsonl_gz(root / name / f"{name}.jsonl.gz", [])
    if "-churn-" not in name:
        write_jsonl_gz(root / name / f"{name}.scored.jsonl.gz", rows)


def _workload(root, name, layouts, truth, stats=None):
    write_json(root / name / "meta.json", {"name": name, "n_chunks": 1000, "n_queries": 6})
    write_json(root / name / "layouts.json", layouts)
    write_jsonl_gz(root / name / "truth.jsonl.gz", truth)
    if stats:
        write_json(root / name / stats[0], stats[1])


def test_the_whole_pass_on_made_up_releases(tmp_path, monkeypatch):
    results, rep, wl, out = tmp_path / "artifacts", tmp_path / "report", tmp_path / "workloads", tmp_path / "out"
    load = {"store": {"load_s": 1.0, "index_s": 2.0, "table_bytes": 2**20, "hnsw_bytes": 2**19, "gin_bytes": 2**18},
            "spicedb": {"relationships": 5, "load_s": 0.5}, "openfga": {"store_id": "s", "tuples": 5, "load_s": 0.7}}
    for seed in (1, 2):
        rows = []
        for corr in ("neg", "none", "pos"):
            layout = f"w3_s0p01_{corr}"
            for u in range(5):
                for q in range(u % 3, u % 3 + 3):
                    user = f"{layout}_u{u}"
                    rows += [_scored("a4@default", layout, user, q, 0.0, ms=float(seed + q)),
                             _scored("a4@iterative", layout, user, q, 1.0),
                             _scored("a5-rls@default", layout, user, q, 0.0),
                             _scored("a5-rls@iterative", layout, user, q, 1.0),
                             _scored("a1-fga", layout, user, q, 0.2 if corr == "neg" else 0.8)]
        _job(results, f"measured-run-w3-s0p01-pgvector-seed{seed}", "w3", "pgvector", rows, load)
        w1 = [_scored(arm, "w1_enron", f"u{u}", 10 * u + q, 0.1, kind="own" if q < 2 else "other")
              for arm in ("a1-fga", "a2-fga-x10") for u in range(6) for q in range(4)]
        _job(results, f"measured-run-w1-pgvector-seed{seed}", "w1_enron", "pgvector", w1, load)
    _job(results, "measured-churn-w3-pgvector-seed1", "w3", "pgvector", [], load)

    scored, _, faults, _ = report.load(results)
    table = report.cells(scored, 5, 50)
    write_json(rep / "cells.json", table)
    write_json(rep / "hypotheses.json", report.hypotheses(scored, faults, table, 5, 50))

    truth3 = [{"layout": f"w3_s0p01_{c}", "user": f"w3_s0p01_{c}_u{u}", "q": q, "sigma_g": 0.012, "sigma_l": 0.02,
               "rho": 0.25, "n_readable": 12} for c in ("neg", "none", "pos") for u in range(5) for q in range(3)]
    _workload(wl, "w3", [{"name": f"w3_s0p01_{c}", "params": {"share": 0.01, "correlation": c,
                                                              "achieved_share_mean": 0.012}}
                         for c in ("neg", "none", "pos")], truth3)
    kinds = {f"u{u}|{10 * u + q}": "own" if q < 2 else "other" for u in range(6) for q in range(4)}
    truth1 = [{"layout": "w1_enron", "user": f"u{u}", "q": 10 * u + q, "sigma_g": 0.001, "sigma_l": 0.0,
               "rho": -1.0, "n_readable": 60} for u in range(6) for q in range(4)]
    _workload(wl, "w1", [{"name": "w1_enron", "params": {"kinds": kinds}}], truth1,
              ("w1-stats.json", {"messages": 1000}))
    truth2 = [{"layout": "w2_tree_a", "user": f"u{u}", "q": q, "sigma_g": 0.04, "sigma_l": None, "rho": None,
               "n_readable": 40} for u in range(3) for q in range(2)]
    _workload(wl, "w2_tree_a", [{"name": "w2_tree_a", "params": {"variant": "tree_a"}}], truth2,
              ("w2-stats.json", {"readable_share_mean": 0.04, "readable_share_quartiles": [0.01, 0.02, 0.04, 0.05, 0.09],
                                 "honeybee_table1_avg_access_selectivity": 0.036}))

    monkeypatch.setattr(sys, "argv", ["extras", "--results", str(results), "--report", str(rep), "--workloads", str(wl),
                                      "--out", str(out), "--rebuilt", str(rep), "--resamples", "50"])
    extras.main()

    for name in ("README.md", "workloads.md", "costs.md", "sensitivity.md", "workloads.json", "costs.json",
                 "sensitivity.json", "rebuild.json"):
        assert (out / name).exists(), name
    sens = read_json(out / "sensitivity.json")
    assert sens["exploratory"] is True and sens["registered_analysis"] is False
    h5 = sens["hypotheses"]["H5"]  # A4 default recalls 0 on all three layouts: supported under every scheme
    assert h5["registered"] == "supported"
    assert all(h5["combined"][s] == "supported" for s in extras.SCHEMES)
    assert sens["verdict_changes"] == []
    h7 = sens["hypotheses"]["H7"]
    ran = [p for p in h7["parts"] if p["estimate"] is not None]
    assert len(ran) == 6 and all(p["users_x_questions"]["interval"] == [0.0, 0.0] for p in ran)
    costs = read_json(out / "costs.json")
    assert costs["latency_check"]["max_abs_difference_ms"] == 0.0
    assert costs["latency_check"]["cells_here"] == costs["latency_check"]["cells_published"] == len(table)
    assert costs["stores_reporting_a_size"] == ["pgvector"]
    (mem,) = [m for m in costs["memory_after_measured_pass"] if m["workload"] == "w3"]
    assert mem["share"] == "s0p01" and mem["services_mib"]["pgvector"]["median"] == 1536.0
    assert all(v["identical"] for v in read_json(out / "rebuild.json")["files"].values() if v["compared"])
    workloads = read_json(out / "workloads.json")["workloads"]
    assert workloads["w3"]["layouts"]["w3_s0p01_neg"]["users_per_question"]["max"] == 5
    assert workloads["w1_enron"]["layouts"]["w1_enron"]["by_kind"]["own"]["pairs"] == 12
