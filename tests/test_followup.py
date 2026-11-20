"""The follow-up harness (prereg/addendum-1.md) on made-up data, no servers: arm names, plans, fresher SpiceDB
reads, the run's search breadth and time budget, the change protocols, and the follow-up report."""

from __future__ import annotations

import asyncio
import json
import sys
from types import SimpleNamespace

import numpy as np
import pytest

from bench import analyze, arms, churn, followup, run
from bench.util import write_json, write_jsonl_gz
from bench.workload import Layout, Workload, save


class FakeStore:
    def __init__(self, name="pgvector", settings=("default", "iterative"), extra=("iterative-100k", "iterative-1m")):
        self.name, self.settings, self.extra_settings = name, settings, extra
        self.ef, self.efs = 100, []

    def set_ef(self, ef):
        self.ef = ef
        self.efs.append(ef)


def test_names_parse_and_registered_names_stay_as_they_are():
    for name in ("a0", "a1-fga", "a2-spicedb-x10", "a3-spicedb@iterative", "a4@default", "a5-rls@default", "a5-dls",
                 "a6-partition", "a7-wardowl", "a4@iterative-100k"):
        assert arms.parse(name) == (name, None, None)
    assert arms.parse("a4@default:ef40") == ("a4@default", 40, None)
    assert arms.parse("a5-rls@iterative:ef100+lookup-openfga") == ("a5-rls@iterative", 100, "openfga")
    assert arms.parse("a6-partition+lookup-spicedb") == ("a6-partition", None, "spicedb")
    with pytest.raises(ValueError):
        arms.parse("a4@default+lookup-ldap")


def test_plans_name_the_registered_arms():
    pg = arms.plan_names(FakeStore(), "sweep")
    assert pg[0] == "a0" and len(pg) == len(set(pg))
    assert {arms.parse(n)[1] for n in pg if n != "a0"} == {40, 100, 400}
    assert "a4@iterative-100k:ef400" in pg and not any("iterative-1m" in n for n in pg)
    assert "a2-fga-x10:ef40" in pg and "a5-rls@iterative:ef100+lookup-openfga" in pg
    assert not any(arms.parse(n)[2] and arms.parse(n)[1] != 100 for n in pg)  # lookups at ef 100 only
    os_ = arms.plan_names(FakeStore("opensearch", ("default",), ()), "sweep")
    assert "a5-dls:ef400" in os_ and "a0" not in os_ and not any(n.startswith("a5-rls") for n in os_)
    assert len(os_) == 3 * (1 + 6 + 1) + 2
    assert arms.plan_names(FakeStore(), "wide") == ["a4@iterative-1m:ef100"]
    with pytest.raises(ValueError):
        arms.plan_names(FakeStore("qdrant", ("default", "acorn"), ()), "wide")
    store = FakeStore()
    assert len(arms.plan_names(store, "lookup")) == 4 * 3
    store.partitions = {"u:x": "part_0"}
    assert arms.plan_names(store, "lookup")[-3:] == ["a6-partition", "a6-partition+lookup-spicedb",
                                                     "a6-partition+lookup-openfga"]


def test_freshness_and_the_consistent_client():
    from authzed.api.v1 import LookupResourcesRequest

    fresh = arms.Freshness("at_least_as_fresh")
    assert fresh.grpc() is None and fresh.http() == {"minimizeLatency": True}  # before any change
    fresh.token = "GhUKEzE3"
    assert fresh.grpc().at_least_as_fresh.token == "GhUKEzE3"
    assert fresh.http() == {"atLeastAsFresh": {"token": "GhUKEzE3"}}
    assert arms.Freshness("fully_consistent").grpc().fully_consistent
    with pytest.raises(ValueError):
        arms.Freshness("minimize_latency")

    seen = []

    class Client:
        def LookupResources(self, request):  # noqa: N802
            seen.append(request)
            return "stream"

        def WriteRelationships(self, request):  # noqa: N802
            return "written"

    class Authorizer:
        def __init__(self):
            self._client = None

        @property
        def client(self):
            if self._client is None:
                self._client = Client()
            return self._client

    authorizer = Authorizer()
    arms.fresher(authorizer, fresh)
    assert authorizer.client.LookupResources(LookupResourcesRequest(permission="view")) == "stream"
    assert seen[0].consistency.at_least_as_fresh.token == "GhUKEzE3" and seen[0].permission == "view"
    assert authorizer.client.WriteRelationships("x") == "written"


def _pairs(n_users=3, per_user=4):
    layout = Layout("w3_s0p01_neg", {f"u{i}": ["f1"] for i in range(n_users)},
                    [(f"u{i}", i * per_user + j) for i in range(n_users) for j in range(per_user)], {"share": 0.01})
    return [(layout, u, q) for u, q in layout.queries]


def test_measure_sets_the_breadth_per_arm_and_records_lookups(monkeypatch):
    store = FakeStore()
    ctx = SimpleNamespace(store=store)

    def build(name, ctx_):
        async def go(user, groups, key):
            go.extra = {"lookup_ms": 1.5, "search_ms": 2.0} if "+lookup" in name else None
            return [(1, 0.5)]
        return go

    monkeypatch.setattr(arms, "build", build)
    names = ["a4@default:ef40", "a4@default:ef400", "a0", "a4@default:ef100+lookup-spicedb"]
    rows = asyncio.run(run.measure(ctx, names, _pairs(), seed=3, warmup=2))
    assert sorted(set(store.efs)) == [40, 100, 400]
    looked = [r for r in rows if "+lookup" in r["arm"]]
    assert looked and all(r["lookup_ms"] == 1.5 and r["search_ms"] == 2.0 for r in looked)
    assert all("lookup_ms" not in r for r in rows if "+lookup" not in r["arm"])

    plain = FakeStore()
    asyncio.run(run.measure(SimpleNamespace(store=plain), ["a4@default", "a0"], _pairs(), seed=3, warmup=2))
    assert plain.efs == []  # a registered job never changes the breadth


def test_measure_stops_at_the_budget(monkeypatch):
    def build(name, ctx_):
        async def go(user, groups, key):
            return []
        return go

    monkeypatch.setattr(arms, "build", build)
    import time

    clock = iter(range(0, 10_000, 10))
    monkeypatch.setattr(run, "time", SimpleNamespace(monotonic=lambda: next(clock), perf_counter=time.perf_counter,
                                                     perf_counter_ns=time.perf_counter_ns))
    status: dict = {}
    rows = asyncio.run(run.measure(SimpleNamespace(store=FakeStore()), ["a4@default", "a5-rls@default"], _pairs(),
                                   seed=1, warmup=0, budget_s=45, status=status))
    assert status["stopped_at_budget"] and len(rows) < 2 * 12
    assert status["arm_cut_short"] or status["arms_not_started"]


def _tiny_workload(tmp_path):
    vectors = np.eye(6, dtype=np.float32)
    layout = Layout("t", {"alice": ["blue"], "bob": []}, [("alice", 0), ("bob", 1)])
    save(tmp_path, name="tiny", vectors=vectors, queries=vectors[:2],
         chunk_users=[[], [0], [], [], [], []], chunk_groups=[[0], [], [1], [0], [1], []],
         user_names=["bob"], group_names=["blue", "red"], layouts=[layout], provenance={})
    return Workload(tmp_path)


def test_unreadable_by_all_and_grant_targets(tmp_path):
    import random

    w = _tiny_workload(tmp_path)
    # chunk 0, 3: blue (alice); 1: bob directly; 2, 4: red (nobody holds red); 5: no reader at all
    assert churn.unreadable_by_all(w).tolist() == [2, 4, 5]
    mask = w.readable("alice", ["blue"])
    chunk, pool = churn._grant_target(random.Random(1), [2, 4, 5], mask, {2, 4})
    assert (chunk, pool) == (5, "unreadable-by-all")
    chunk, pool = churn._grant_target(random.Random(1), [], mask, {1})
    assert pool == "unreadable-by-user" and not mask[chunk] and chunk != 1


class FakeSources:
    def __init__(self, log):
        self.log = log

    def apply(self, i, new):
        self.log.append(("apply", i, [t.subject_id for t in new]))
        return {"write_s": {}, "acked_at": 0.0, "zedtoken": f"t{len(self.log)}"}


def _churn_workload(tmp_path):
    # chunks 0-5 in blue (alice and bob), 6 and 7 bob's own, 8 and 9 in red (held by nobody), 10 and 11 no reader
    layout = Layout("t", {"alice": ["blue"], "bob": ["blue"]}, [("alice", 0), ("bob", 1)])
    save(tmp_path, name="tiny", vectors=np.eye(12, dtype=np.float32), queries=np.eye(12, dtype=np.float32)[:2],
         chunk_users=[[]] * 6 + [[0], [0]] + [[]] * 4, chunk_groups=[[0]] * 6 + [[], []] + [[1], [1]] + [[], []],
         user_names=["bob"], group_names=["blue", "red"], layouts=[layout], provenance={})
    return Workload(tmp_path)


def _churn(tmp_path, monkeypatch, variants):
    w = _churn_workload(tmp_path)
    log: list = []

    async def sleep(s):
        log.append(("sleep", s))

    monkeypatch.setattr(churn.asyncio, "sleep", sleep)
    tokens = []

    def build(name, ctx_):
        async def go(user, groups, key):
            tokens.append(None if ctx_.consistency is None else ctx_.consistency.token)
            chunk = int(key[1:])
            state = [e for e in log if e[0] == "apply" and e[1] == chunk][-1][2]
            return [(chunk, 1.0)] if user in state or (state and groups) else []
        return go

    monkeypatch.setattr(arms, "build", build)
    ctx = SimpleNamespace(workload=w, consistency=None)
    rows = asyncio.run(churn.measure(ctx, FakeSources(log), ["a1-spicedb"], events=4, seed=2, every=0.0, cap=5.0,
                                     settle=10.0, variants=variants))
    return rows, log, tokens


def test_the_published_protocol_pauses_before_grants_only(tmp_path, monkeypatch):
    rows, log, _ = _churn(tmp_path, monkeypatch, churn.PUBLISHED)
    assert [r["kind"] for r in rows] == ["revoke", "grant", "revoke", "grant"]
    assert all(r["arm"] == "a1-spicedb" and "protocol" not in r and "probe_log" in r for r in rows)
    steps = [e[0] for e in log]
    # revoke: apply; grant: apply (empty), sleep, apply (the user)
    assert steps == ["apply", "apply", "sleep", "apply", "apply", "apply", "sleep", "apply"]


def test_the_symmetric_protocol_pauses_before_both_and_grants_unreadable_chunks(tmp_path, monkeypatch):
    rows, log, tokens = _churn(tmp_path, monkeypatch, (("symmetric", "at_least_as_fresh"),))
    assert all(r["arm"] == "a1-spicedb:symmetric+at_least_as_fresh" and r["protocol"] == "symmetric" for r in rows)
    grants = [r for r in rows if r["kind"] == "grant"]
    assert grants and all(r["grant_pool"] == "unreadable-by-all" and r["chunk"] in (8, 9, 10, 11) for r in grants)
    assert log[0][0] == "sleep" and sum(e[0] == "sleep" for e in log) == 4
    assert all(t is not None and t.startswith("t") for t in tokens)  # probes carry the change's token


def test_analyze_passes_lookup_fields_on(tmp_path):
    w = _tiny_workload(tmp_path)
    truth = {("t", "alice", 0): {"n_readable": 2, "s_k": 0.0, "sigma_g": 0.1, "rho": 0.0}}
    rows = [{"arm": "a4@default+lookup-spicedb", "layout": "t", "user": "alice", "q": 0, "hits": [0], "scores": [1.0],
             "ms": 3.0, "error": None, "lookup_ms": 1.0, "search_ms": 2.0, "groups_found": 1,
             "principals_match": False}]
    _, problems, scored = analyze.summarize(w, rows, truth)
    assert scored[0]["lookup_ms"] == 1.0 and scored[0]["principals_match"] is False
    assert any("other groups" in p for p in problems)
    _, _, plain = analyze.summarize(w, [{k: v for k, v in rows[0].items() if k in
                                         ("arm", "layout", "user", "q", "hits", "scores", "ms", "error")}], truth)
    assert "lookup_ms" not in plain[0]


def _scored(arm, user, recall, ms=10.0, layout="w3_s0p01_neg", **extra):
    return {"arm": arm, "layout": layout, "user": user, "q": 1, "kind": None, "ms": ms, "error": None,
            "n_readable": 50, "sigma_g": 0.1, "rho": 0.0, "recall": recall, "outside": 0, "empty": False,
            "n_hits": 10, "duplicates": 0, **extra}


def test_the_report_runs_on_folders_laid_out_as_the_jobs_leave_them(tmp_path, monkeypatch):
    results = tmp_path / "artifacts"
    job = "followup-run-sweep-w3-s0p01-pgvector-seed1"
    rows = []
    for u in range(5):
        rows += [_scored("a4@default:ef40", f"u{u}", 0.5), _scored("a4@default:ef100", f"u{u}", 0.8),
                 _scored("a4@default:ef400", f"u{u}", 0.95, ms=30.0), _scored("a0", f"u{u}", 1.0),
                 _scored("a4@default:ef100+lookup-spicedb", f"u{u}", 0.8, ms=14.0, lookup_ms=4.0, search_ms=10.0,
                         groups_found=11, principals_match=True)]
    meta = {"args": {"store": "pgvector", "plan": "sweep", "seed": "1"}, "workload": {"name": "w3"},
            "environment": {"git_sha": "abc", "run_id": "1"}, "complete": True, "arms": ["x"],
            "status": {"stopped_at_budget": False}}
    write_json(results / job / f"{job}.meta.json", meta)
    write_jsonl_gz(results / job / f"{job}.scored.jsonl.gz", rows)
    cjob = "followup-churn-diag-a-w3-pgvector-seed1"
    change = [{"arm": "a1-spicedb", "event": 0, "kind": "revoke", "layout": "x", "user": "u", "chunk": 3,
               "delay_s": 4.8, "censored": False, "probes": 3, "probe_log": [[0.0, 0.01, 1], [0.1, 0.01, 1],
                                                                             [4.79, 0.01, 0]]},
              {"arm": "a1-spicedb:symmetric", "base": "a1-spicedb", "protocol": "symmetric", "consistency": "default",
               "event": 1, "kind": "grant", "grant_pool": "unreadable-by-user", "layout": "x", "user": "u",
               "chunk": 4, "delay_s": 0.02, "censored": False, "probes": 1, "probe_log": [[0.0, 0.02, 1]]}]
    write_json(results / cjob / f"{cjob}.meta.json", {**meta, "args": {"store": "pgvector", "plan": "diag-a"}})
    write_jsonl_gz(results / cjob / f"{cjob}.jsonl.gz", change)
    base = tmp_path / "base"
    v1 = [{"workload": "w3", "store": "pgvector", "arm": "a4@default", "layout": "w3_s0p01_neg", "recall": 0.6,
           "recall_95": [0.55, 0.65], "p50_ms": {"median": 9.0}, "p99_ms": {"median": 20.0}, "empty": 0, "errors": 0},
          {"workload": "w3", "store": "pgvector", "arm": "a0", "layout": "w3_s0p01_neg", "recall": 1.0,
           "recall_95": [1.0, 1.0], "p50_ms": {"median": 11.0}, "p99_ms": {"median": 15.0}, "empty": 0, "errors": 0}]
    write_json(base / "cells.json", v1)
    write_json(base / "churn.json", [{"workload": "w3", "store": "pgvector", "arm": "a1-spicedb", "kind": "revoke",
                                      "events": 30, "censored": 0, "delay_s": [4.7, 4.9, 5.0]}])
    write_json(base / "hypotheses.json", {"H6": {"parts": [{"store": "pgvector", "layout": "w3_s0p01_neg",
                                                            "interval": [0.287, 0.36]}]}})
    out = tmp_path / "report"
    raw = tmp_path / "v1raw"
    for seed, recall in ((1, 0.5), (2, 0.7)):
        v1job = f"measured-run-w3-s0p01-pgvector-seed{seed}"
        write_json(raw / v1job / f"{v1job}.meta.json", {"args": {"store": "pgvector"}, "workload": {"name": "w3"},
                                                         "load": {"store": {"segments": 3}}})
        write_jsonl_gz(raw / v1job / f"{v1job}.scored.jsonl.gz",
                       [_scored("a4@default", f"u{u}", recall) for u in range(5)] + [_scored("a4@iterative", "u0", 1.0)])
    monkeypatch.setattr(sys, "argv", ["followup", "--results", str(results), "--baseline", str(base), "--out", str(out),
                                      "--resamples", "200", "--baseline-raw", str(raw)])
    followup.main()
    repro = json.loads((out / "reproduction.json").read_text())
    assert repro["cells"] == 2 and repro["inside"] == 1
    assert [r["arm"] for r in repro["outside"]] == ["a4@default"]
    jobs = repro["outside"][0]["per_job"]
    assert [(j["seed"], j["recall"]) for j in jobs["results_v1"]] == [("1", 0.5), ("2", 0.7)]
    assert jobs["results_v1"][0]["store_load"] == {"segments": 3}
    assert [(j["seed"], j["recall"]) for j in jobs["followup"]] == [("1", 0.8)]
    tune = json.loads((out / "tunability.json").read_text())
    assert tune[0]["highest"]["arm"] == "a4@default:ef400" and tune[0]["h6_results_v1"] == [0.287, 0.36]
    look = json.loads((out / "lookup.json").read_text())
    assert look["cost"][0]["lookup_p50"]["median"] == 4.0 and look["arms"][0]["recall_without"] == 0.8
    changes = {(c["protocol"], c["kind"]): c for c in json.loads((out / "churn.json").read_text())}
    assert changes[("published", "revoke")]["stale_answers"] == 2
    assert changes[("published", "revoke")]["results_v1"]["delay_s"] == [4.7, 4.9, 5.0]
    assert changes[("symmetric", "grant")]["grant_pools"] == {"unreadable-by-user": 1}
    text = (out / "followup.md").read_text()
    assert "farthest first" in text and "Reproduction" in text
    assert chr(0x2014) not in text  # no em dash
