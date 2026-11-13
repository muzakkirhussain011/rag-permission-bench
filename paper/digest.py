"""Digest of bench.report's output (release results-v1) for writing the paper: every number the text uses comes from here.

    python paper/digest.py <report folder> > digest.md

<report folder> is `report/` from the release's report.tar.gz, or a report rebuilt with `python -m bench.report`.

Reads cells.json, hypotheses.json, churn.json, faults.json, coverage.json and harness.json; computes nothing that
bench.report did not, except grouping, minima, maxima and counts over its cells.
"""

import collections
import json
import sys
from pathlib import Path

R = Path(sys.argv[1])
cells = json.loads((R / "cells.json").read_text(encoding="utf-8"))
hyp = json.loads((R / "hypotheses.json").read_text(encoding="utf-8"))
churn = json.loads((R / "churn.json").read_text(encoding="utf-8"))
faults = json.loads((R / "faults.json").read_text(encoding="utf-8"))
coverage = json.loads((R / "coverage.json").read_text(encoding="utf-8"))
harness = json.loads((R / "harness.json").read_text(encoding="utf-8"))
STORES = ["pgvector", "qdrant", "milvus", "weaviate", "opensearch"]


def f3(x):
    return "n/a" if x is None else f"{x:.3f}"


def ci(c):
    lo, hi = c.get("recall_95") or (None, None)
    return f"{f3(c['recall'])} [{f3(lo)}, {f3(hi)}]"


def ms(d):
    return "n/a" if not d else f"{d['median']:.1f}"


out = []
w = out.append
w("# Digest of results-v1 (bench.report output)\n")
w(f"Coverage: {coverage['cells']} cells, seeds planned {coverage['seeds_planned']}, cells short of seeds "
  f"{len(coverage['cells_short_of_seeds'])}, jobs without scores {len(coverage['jobs_without_scores'])}. "
  f"Exact control (A0) faults: {len(harness)}.\n")

tot = collections.Counter()
for c in cells:
    tot["queries"] += c["queries"]; tot["outside"] += c["outside"]; tot["errors"] += c["errors"]
    tot["empty"] += c["empty"]; tot["over_30s"] += c["over_30s"]
w(f"All measured cells: {tot['queries']:,} queries; outside the readable set {tot['outside']}; errors {tot['errors']:,}; "
  f"empty answers {tot['empty']:,}; calls over 30 s {tot['over_30s']:,}.\n")
bad = [c for c in cells if c["outside"]]
w(f"Cells with any chunk outside the readable set: {len(bad)}" + "".join(
    f"\n- {c['workload']} {c['store']} {c['arm']} {c['layout']}: {c['outside']}" for c in bad) + "\n")
err = collections.Counter()
for c in cells:
    if c["errors"]:
        err[(c["arm"], c["store"], c["workload"])] += c["errors"]
w("Errors by arm, store and workload: " + ("; ".join(f"{a} {s} {wl}: {n}" for (a, s, wl), n in sorted(err.items())) or "none") + "\n")

w("## Hypotheses\n")
for k, v in hyp.items():
    w(f"### {k}: {v['verdict']}\n")
    parts = v.get("parts")
    if parts:
        counts = collections.Counter(p.get("verdict", "meets" if p.get("meets") else "-") for p in parts)
        w(f"{len(parts)} parts: {dict(counts)}\n")
        for p in parts:
            iv = p.get("interval")
            label = ", ".join(f"{a}={p[a]}" for a in ("store", "arm", "layout", "share", "setting") if a in p)
            if iv is not None:
                w(f"- {label}: [{f3(iv[0])}, {f3(iv[1])}] {p.get('verdict')}")
            else:
                w(f"- {label}: " + ", ".join(f"{a}={p[a]}" for a in p if a not in ("store",)))
        w("")
    else:
        w(json.dumps({a: b for a, b in v.items() if a != "verdict"}) + "\n")


def table(workload, title):
    w(f"## {title}\n")
    w("| store | arm | recall@10 [95%] | p50 ms (median of jobs) | empty | errors | outside | queries |\n|---|---|---|---|---|---|---|---|")
    rows = [c for c in cells if c["workload"] == workload]
    for c in sorted(rows, key=lambda c: (STORES.index(c["store"]) if c["store"] in STORES else 9, c["arm"])):
        w(f"| {c['store']} | {c['arm']} | {ci(c)} | {ms(c['p50_ms'])} | {c['empty']} | {c['errors']} | {c['outside']} | {c['queries']} |")
    w("")


table("w1_enron", "W1, Enron (own-mail and other-mail questions together, as scored)")
for wl in ("w2_tree_a", "w2_uniform_a", "w2_erbac_a", "w2_erbac_b"):
    table(wl, f"W2, {wl}")

w("## W3: recall@10 by arm, store and layout\n")
shares = ["0p001", "0p01", "0p05", "0p2", "0p5"]
cors = ["neg", "none", "pos"]
w3 = [c for c in cells if c["workload"] == "w3"]
arms = sorted({c["arm"] for c in w3})
for arm in arms:
    w(f"### {arm}\n")
    w("| store | " + " | ".join(f"{s} {r}" for s in shares for r in cors) + " |")
    w("|---|" + "---|" * (len(shares) * len(cors)))
    for st in STORES:
        row = []
        found = False
        for s in shares:
            for r in cors:
                c = next((c for c in w3 if c["arm"] == arm and c["store"] == st and c["layout"] == f"w3_s{s}_{r}"), None)
                row.append(f3(c["recall"]) if c else "")
                found = found or c is not None
        if found:
            w(f"| {st} | " + " | ".join(row) + " |")
    w("")
w("## W3: median p50 latency (ms) by arm, store and share (median over correlations)\n")
for arm in arms:
    line = []
    for st in STORES:
        vals = []
        for s in shares:
            ps = [c["p50_ms"]["median"] for c in w3 if c["arm"] == arm and c["store"] == st and c["layout"].startswith(f"w3_s{s}_") and c["p50_ms"]]
            vals.append(f"{sorted(ps)[len(ps) // 2]:.1f}" if ps else "")
        if any(vals):
            line.append(f"{st}: " + " / ".join(vals))
    w(f"- {arm}: " + "; ".join(line))
w("")
w("## W3 share 0.5, A3 (engine pre-filter): failures and latency (H4)\n")
for c in w3:
    if c["arm"].startswith("a3") and c["layout"].startswith("w3_s0p5_"):
        w(f"- {c['store']} {c['arm']} {c['layout']}: queries {c['queries']}, failed_h4 {c['failed_h4']}, over_30s {c['over_30s']}, "
          f"errors {c['errors']}, p50 {ms(c['p50_ms'])} ms, recall {f3(c['recall'])}")
w("")
w("## Permission changes (churn): delay until the answer reflects the change, s (p50, p90, max)\n")
w("| store | arm | kind | events | censored | skipped | p50 | p90 | max |\n|---|---|---|---|---|---|---|---|---|")
for r in sorted(churn, key=lambda r: (r["store"], r["arm"], r["kind"])):
    d = r["delay_s"] or [None, None, None]
    w(f"| {r['store']} | {r['arm']} | {r['kind']} | {r['events']} | {r['censored']} | {r['skipped']} | "
      + " | ".join("n/a" if x is None else f"{x:.3f}" for x in d) + " |")
w("")
w("## Faults (engine traffic through Toxiproxy), totals per fault and arm family\n")
agg = collections.defaultdict(collections.Counter)
for c in faults:
    arm, _, fault = c["arm"].partition("|")
    fam = arm.split("@")[0]
    k = (fault or "none", fam)
    for x in ("queries", "outside", "errors", "empty", "over_30s"):
        agg[k][x] += c[x]
    agg[k]["cells"] += 1
w("| fault | arm | cells | queries | outside | errors | empty | over 30 s |\n|---|---|---|---|---|---|---|---|")
for (fault, fam), v in sorted(agg.items()):
    w(f"| {fault} | {fam} | {v['cells']} | {v['queries']} | {v['outside']} | {v['errors']} | {v['empty']} | {v['over_30s']} |")
w("")
print("\n".join(out))
