"""The report's rules on made-up rows (no study data): failed queries count, H4 counts slow calls, missing
parts keep a hypothesis from being supported, and intervals do not depend on unrelated files."""

from __future__ import annotations

from bench import report


def _row(user, q, recall, *, error=None, ms=10.0, arm="a4@default", layout="w3_s0p01_neg", store="pgvector",
         job="measured-run-w3-s0p01-pgvector-seed1", workload="w3", kind=None, n_readable=50):
    return {"workload": workload, "store": store, "job": job, "arm": arm, "layout": layout, "user": user, "q": q,
            "kind": kind, "ms": ms, "error": error, "n_readable": n_readable, "recall": recall,
            "outside": 0, "empty": error is not None or recall == 0, "n_hits": 0 if error else 10, "duplicates": 0}


def test_a_failed_query_counts_as_recall_zero_and_not_as_empty():
    rows = [_row("u1", 1, 1.0), _row("u1", 2, 0.0, error="TimeoutError: x")]
    (cell,) = report.cells(rows, seed=5, resamples=200)
    assert cell["recall"] == 0.5
    assert cell["errors"] == 1 and cell["empty"] == 0


def test_a_query_with_nothing_readable_has_no_recall():
    rows = [_row("u1", 1, None, n_readable=0), _row("u2", 1, 1.0)]
    (cell,) = report.cells(rows, seed=5, resamples=200)
    assert cell["recall"] == 1.0 and cell["users"] == 1


def test_h4_counts_calls_over_30_s_as_failed():
    rows = []
    for store, settings in report.SETTINGS.items():
        for setting in settings:
            for corr in report.CORRELATIONS:
                for u in range(4):
                    slow = store == "milvus" and u < 3  # three of four calls over 30 s, no errors
                    rows.append(_row(f"u{u}", u, 1.0, arm=f"a3-spicedb@{setting}", layout=f"w3_s0p5_{corr}",
                                     store=store, ms=40_000.0 if slow else 100.0))
    table = report.cells(rows, seed=5, resamples=50)
    h4 = report.hypotheses(rows, [], table, seed=5, resamples=50)["H4"]
    assert h4["verdict"] == "supported"
    assert [p["store"] for p in h4["parts"] if p["meets"]] == ["milvus"]


def test_h4_is_inconclusive_when_a_store_is_missing_and_none_meets():
    rows = [_row("u1", 1, 1.0, arm="a3-spicedb@default", layout=f"w3_s0p5_{c}", ms=100.0) for c in report.CORRELATIONS]
    table = report.cells(rows, seed=5, resamples=50)
    assert report.hypotheses(rows, [], table, seed=5, resamples=50)["H4"]["verdict"] == "inconclusive"


def test_missing_parts_are_not_run_and_block_support():
    rows = [_row(f"u{u}", 1, 0.0, arm="a4@default", layout=f"w3_s0p01_{c}") for u in range(20) for c in ("neg", "pos")]
    table = report.cells(rows, seed=5, resamples=200)
    h5 = report.hypotheses(rows, [], table, seed=5, resamples=200)["H5"]
    assert [p["verdict"] for p in h5["parts"]] == ["supported", "not run", "supported"]
    assert h5["verdict"] == "inconclusive"


def test_combine_is_intersection_union():
    assert report.combine(["supported", "supported"]) == "supported"
    assert report.combine(["supported", "not supported", "inconclusive"]) == "not supported"
    assert report.combine(["supported", "not run"]) == "inconclusive"
    assert report.combine([]) == "not tested"


def test_an_interval_does_not_depend_on_other_cells():
    base = [_row(f"u{u}", 1, u / 10) for u in range(10)]
    other = [_row(f"v{u}", 1, 1.0, layout="w3_s0p5_pos") for u in range(10)]
    alone = {c["layout"]: c for c in report.cells(base, seed=5, resamples=500)}["w3_s0p01_neg"]
    together = {c["layout"]: c for c in report.cells(base + other, seed=5, resamples=500)}["w3_s0p01_neg"]
    assert alone["recall_bonferroni"] == together["recall_bonferroni"]


def test_the_exact_control_is_checked():
    rows = [_row("u1", 1, 1.0, arm="a0"), _row("u2", 1, 0.9, arm="a0")]
    table = report.cells(rows, seed=5, resamples=50)
    assert len(report.harness_check(table)) == 1
