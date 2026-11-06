"""Checks of the parts that decide the numbers: who may read what, the exact answers, the scoring."""

from __future__ import annotations

import numpy as np

from bench import devdata, engines, metrics, truth
from bench.workload import Layout, Workload, save


def _tiny(tmp_path):
    vectors = np.vstack([np.eye(4, dtype=np.float32), [[0.6, 0.8, 0, 0], [0, 0, 0.6, 0.8]]])
    queries = np.array([[1, 0, 0, 0], [0, 0, 1, 0]], dtype=np.float32)
    layout = Layout("t", {"alice": ["blue"], "bob": []}, [("alice", 0), ("alice", 1), ("bob", 0)])
    save(tmp_path, name="tiny", vectors=vectors, queries=queries,
         chunk_users=[[], [0], [], [], [0], []], chunk_groups=[[0], [], [1], [0], [], [1]],
         user_names=["bob"], group_names=["blue", "red"], layouts=[layout], provenance={})
    return Workload(tmp_path)


def test_readable_follows_users_and_groups(tmp_path):
    w = _tiny(tmp_path)
    assert np.flatnonzero(w.readable("alice", ["blue"])).tolist() == [0, 3]
    assert np.flatnonzero(w.readable("bob", [])).tolist() == [1, 4]
    assert np.flatnonzero(w.readable("carol", ["red", "blue"])).tolist() == [0, 2, 3, 5]
    assert w.chunk_principals(4) == ["u:bob"]
    assert w.chunk_principals(2) == ["g:red"]


def test_truth_is_the_best_readable(tmp_path):
    w = _tiny(tmp_path)
    rows = {(r["user"], r["q"]): r for r in truth.compute(w, k=2, nn=3)}
    assert rows[("alice", 0)]["ids"] == [0, 3]
    assert rows[("alice", 0)]["n_readable"] == 2
    assert rows[("bob", 0)]["ids"] == [4, 1]
    assert abs(rows[("bob", 0)]["scores"][0] - 0.6) < 1e-6


def test_truth_breaks_ties_by_id():
    ids, scores = truth.top_k(np.array([0.5, 0.9, 0.5, 0.5], np.float32), np.array([7, 3, 2, 9]), 3)
    assert ids.tolist() == [3, 2, 7]


def test_score_counts_ties_outside_and_empty(tmp_path):
    w = _tiny(tmp_path)
    t = {"n_readable": 2, "s_k": 0.0}
    mask = w.readable("alice", ["blue"])
    s = metrics.score([0, 1, 3, 0], t, mask, w.vectors, w.queries[0], k=10)
    assert s["outside"] == 1 and s["duplicates"] == 1 and s["recall"] == 1.0
    assert metrics.score([], t, mask, w.vectors, w.queries[0], k=2)["empty"]
    assert metrics.score([], {"n_readable": 0, "s_k": None}, mask, w.vectors, w.queries[0])["recall"] is None


def test_engine_tuples_are_unique_and_complete(tmp_path):
    devdata.build(tmp_path, n=200, n_queries=10)
    w = Workload(tmp_path)
    all_tuples = list(engines.tuples(w))
    assert len(all_tuples) == len(set(all_tuples))
    chunk_tuples = [t for t in all_tuples if t.resource_type == "chunk"]
    assert len(chunk_tuples) == len(w.user_idx) + len(w.group_idx)
    members = {(t.resource_id, t.subject_id) for t in all_tuples if t.resource_type == "group"}
    expected = {(g, u) for layout in w.layouts for u, gs in layout.user_groups.items() for g in gs}
    assert members == expected
