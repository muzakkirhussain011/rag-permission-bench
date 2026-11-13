"""The paper's table and digest scripts run from this repository on a made-up report (no study data)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from bench.util import write_json

ROOT = Path(__file__).resolve().parents[1]
FAULT_ARMS = ("a1-fga", "a1-spicedb", "a2-fga-x10", "a2-spicedb-x3", "a3-spicedb@default", "a7-wardowl")


def _cell(workload, store, arm, layout, recall, queries=30):
    return {"workload": workload, "store": store, "arm": arm, "layout": layout, "jobs": 3, "users": 10,
            "queries": queries, "recall": recall, "recall_95": [recall - 0.05, recall + 0.05],
            "recall_bonferroni": [recall - 0.08, recall + 0.08], "empty": 0, "outside": 0, "errors": 0,
            "over_30s": 0, "failed_h4": 0, "p50_ms": {"median": 5.0, "min": 4.0, "max": 6.0},
            "p99_ms": {"median": 9.0, "min": 8.0, "max": 10.0}}


def test_tables_and_digest_run_on_a_report(tmp_path):
    rep = tmp_path / "report"
    cells = [_cell("w1_enron", "pgvector", "a1-fga", "w1_enron", 0.3),
             _cell("w2_tree_a", "pgvector", "a4@default", "w2_tree_a", 0.9),
             _cell("w3", "pgvector", "a3-spicedb@default", "w3_s0p5_neg", 0.7)]
    # the regime table reads every W3 share and correlation of A0, the store filters and a post-filter
    for share in ("0p001", "0p01", "0p05", "0p2", "0p5"):
        for corr in ("neg", "none", "pos"):
            layout = f"w3_s{share}_{corr}"
            cells += [_cell("w3", "pgvector", "a0", layout, 1.0), _cell("w3", "pgvector", "a4@default", layout, 0.9),
                      _cell("w3", "pgvector", "a4@iterative", layout, 1.0),
                      _cell("w3", "pgvector", "a1-spicedb", layout, 0.5)]
    hypotheses = {
        "H1": {"verdict": "supported", "parts": [{"store": "pgvector", "arm": "a1-fga", "interval": [0.2, 0.3],
                                                   "verdict": "supported"}]},
        "H2": {"verdict": "supported", "parts": [{"store": "pgvector", "arm": "a2-fga-x10", "interval": [0.5, 0.6],
                                                   "verdict": "supported"}]},
        "H3": {"verdict": "supported", "parts": [{"store": "pgvector", "share": "0p001", "arm": "a1-fga",
                                                   "interval": [-0.3, -0.1], "verdict": "supported"}]},
        "H4": {"verdict": "supported", "parts": [{"store": "pgvector", "cells": 6, "needed": 6, "meets": True}]},
        "H5": {"verdict": "supported", "parts": [{"layout": "w3_s0p01_neg", "interval": [0.0, 0.1],
                                                   "verdict": "supported"}]},
        "H6": {"verdict": "not supported", "parts": [{"store": "pgvector", "layout": "w3_s0p001_neg",
                                                       "interval": [0.5, 0.6], "verdict": "not supported"}]},
        "H7": {"verdict": "supported", "parts": [{"setting": "default", "layout": "w3_s0p001_neg",
                                                   "interval": [0.0, 0.0], "verdict": "supported"}]},
        "H8": {"verdict": "supported", "rows": 1200, "outside": 0, "stores": ["pgvector"]},
    }
    faults = [_cell("w3", "pgvector", f"{arm}{fault}", "w3_s0p01_neg", 0.5, queries=10)
              for arm in FAULT_ARMS for fault in ("", "|stopped", "|slow", "|cut")]
    churn = [{"workload": "w3", "store": "pgvector", "arm": "a1-spicedb", "kind": "revoke", "events": 10,
              "skipped": 0, "censored": 0, "delay_s": [0.1, 0.5, 1.0]}]
    write_json(rep / "cells.json", cells)
    write_json(rep / "hypotheses.json", hypotheses)
    write_json(rep / "faults.json", faults)
    write_json(rep / "churn.json", churn)
    write_json(rep / "coverage.json", {"seeds_planned": 3, "cells": 4, "cells_short_of_seeds": [],
                                       "jobs_without_scores": []})
    write_json(rep / "harness.json", [])

    out = tmp_path / "generated"
    subprocess.run([sys.executable, str(ROOT / "paper" / "tables.py"), str(rep), str(out)], check=True)
    assert {p.name for p in out.iterdir()} == {"tab-hypotheses.tex", "tab-quality.tex", "tab-faults.tex",
                                               "tab-regimes.tex", "numbers.tex"}
    assert f"\\newcommand{{\\NumCells}}{{{len(cells)}}}" in (out / "numbers.tex").read_text(encoding="utf-8")
    digest = subprocess.run([sys.executable, str(ROOT / "paper" / "digest.py"), str(rep)], check=True,
                            capture_output=True, text=True, encoding="utf-8").stdout
    assert digest.startswith("# Digest of results-v1")
