"""The figures are drawn from a report with made-up numbers (no study data), as vector PDFs whose
fonts are TrueType, not Type 3 (ACM's production checks refuse Type 3)."""

from __future__ import annotations

import json

from bench import figures


def _cell(workload, store, arm, layout, recall, p50):
    return {"workload": workload, "store": store, "arm": arm, "layout": layout, "jobs": 5, "users": 100,
            "queries": 1000, "recall": recall, "recall_95": [max(recall - 0.05, 0), min(recall + 0.05, 1)],
            "recall_bonferroni": [max(recall - 0.08, 0), min(recall + 0.08, 1)], "empty": 0, "outside": 0,
            "errors": 0, "p50_ms": {"median": p50, "min": p50 * 0.9, "max": p50 * 1.1},
            "p99_ms": {"median": p50 * 2, "min": p50 * 1.8, "max": p50 * 2.2}}


def test_every_figure_is_a_pdf_without_type3_fonts(tmp_path):
    cells = []
    for store in ("pgvector", "opensearch"):
        for arm in ("a1-spicedb", "a2-spicedb-x10", "a3-spicedb@default", "a4@default", "a4@iterative",
                    "a5-rls@default", "a5-dls", "a7-wardowl"):
            for share in figures.SHARES:
                for corr, _ in figures.CORRELATIONS:
                    cells.append(_cell("w3", store, arm, figures._layout(share, corr), min(1.0, share * 10), 5 + share * 100))
            cells.append(_cell("w1_enron", store, arm, "w1_enron", 0.5, 10))
            cells.append(_cell("w2_erbac_b", store, arm, "w2_erbac_b", 0.7, 10))
    churn = [{"workload": "w3", "store": s, "arm": a, "kind": k, "events": 10, "censored": 0, "delay_s": [0.2, 1.0, 2.0]}
             for s in ("pgvector", "qdrant") for a in ("a1-spicedb", "a4@default") for k in ("revoke", "grant")]
    report = tmp_path / "report"
    report.mkdir()
    (report / "cells.json").write_text(json.dumps(cells))
    (report / "churn.json").write_text(json.dumps(churn))
    out = tmp_path / "figures"
    out.mkdir()
    made = [figures.w3_grid(cells, out, "recall"), figures.w3_grid(cells, out, "p50"),
            figures.dots(cells, "w1_enron", "w1_enron", out), figures.dots(cells, "w2_erbac_b", "w2_erbac_b", out),
            figures.churn(churn, out)]
    assert all(p is not None and p.exists() for p in made)
    for path in made:
        data = path.read_bytes()
        assert data.startswith(b"%PDF")
        assert b"/Type3" not in data and b"/FontType 3" not in data


def test_arm_labels_are_readable():
    from bench.figures import arm_label

    assert arm_label("a1-fga") == "A1 post-filter, OpenFGA"
    assert arm_label("a2-spicedb-x10") == "A2 over 10k, SpiceDB"
    assert arm_label("a3-spicedb@acorn") == "A3 engine pre-filter, ACORN"
    assert arm_label("a4@pathseer") == "A4 store filter, PathSeer"
    assert arm_label("a5-rls@iterative") == "A5 row-level security, iterative"
    assert arm_label("a5-dls") == "A5 document-level security"
    assert arm_label("a7-wardowl") == "A7 wardowl"
