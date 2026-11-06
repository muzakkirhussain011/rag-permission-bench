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


def test_a0_and_a3_answer_the_preregistered_subsets():
    from bench.run import arm_pairs

    def layout(name, share, users=100, per_user=10):
        queries = [(f"{name}_u{u}", u * per_user + j) for u in range(users) for j in range(per_user)]
        return Layout(name, {u: [] for u, _ in queries}, queries, {"share": share})

    layouts = [layout("a", 0.01), layout("b", 0.05), layout("c", 0.2), layout("d", 0.5)]
    pairs = [(lay, u, q) for lay in layouts for u, q in lay.queries]

    def counts(arm):
        chosen = arm_pairs(arm, pairs, seed=7)
        return {lay.name: (len({u for x, u, _ in chosen if x is lay}), sum(x is lay for x, _, _ in chosen))
                for lay in layouts}

    assert counts("a3-spicedb@default") == {"a": (100, 1000), "b": (100, 300), "c": (100, 100), "d": (50, 50)}
    assert counts("a0") == {name: (100, 100) for name in "abcd"}
    assert counts("a4@default") == {name: (100, 1000) for name in "abcd"}
    assert arm_pairs("a3-spicedb@default", pairs, 7) == arm_pairs("a3-spicedb@iterative", pairs, 7)
    assert arm_pairs("a3-spicedb@default", pairs, 7) != arm_pairs("a3-spicedb@default", pairs, 8)
    assert arm_pairs("a3-spicedb@default", [(lay, u, q) for lay, u, q in pairs if lay.name == "a"][:5], 7)
