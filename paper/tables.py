"""LaTeX tables for the paper's results section, generated from bench.report's output (release results-v1).

    python paper/tables.py <report folder> <output folder>

<report folder> is `report/` from the release's report.tar.gz, or a report rebuilt from results-raw.tar.gz with
`python -m bench.report`. Writes tab-hypotheses.tex, tab-quality.tex, tab-faults.tex, tab-regimes.tex and numbers.tex
(macros for the numbers the text quotes) into <output folder>. Every value is read from cells.json, hypotheses.json,
faults.json or churn.json; nothing is typed by hand.
"""

import collections
import json
import sys
from pathlib import Path

R, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
cells = json.loads((R / "cells.json").read_text(encoding="utf-8"))
hyp = json.loads((R / "hypotheses.json").read_text(encoding="utf-8"))
faults = json.loads((R / "faults.json").read_text(encoding="utf-8"))
churn = json.loads((R / "churn.json").read_text(encoding="utf-8"))


def f(x):
    return f"{x:.3f}"


def rng(values):
    lo, hi = min(values), max(values)
    return f(lo) if f(lo) == f(hi) else f"{f(lo)}--{f(hi)}"


# ---- Quality table: recall@10 per arm family and workload, range over stores ----
ROWS = [
    ("A1 post-filter, OpenFGA", lambda a: a == "a1-fga"),
    ("A1 post-filter, SpiceDB", lambda a: a == "a1-spicedb"),
    ("A2 over $3k$ (both engines)", lambda a: a.startswith("a2-") and a.endswith("-x3")),
    ("A2 over $10k$ (both engines)", lambda a: a.startswith("a2-") and a.endswith("-x10")),
    ("A3 engine pre-filter, default", lambda a: a == "a3-spicedb@default"),
    ("A3 engine pre-filter, alternative", lambda a: a.startswith("a3-spicedb@") and a != "a3-spicedb@default"),
    ("A4 store filter, default", lambda a: a == "a4@default"),
    ("A4 store filter, alternative", lambda a: a.startswith("a4@") and a != "a4@default"),
    ("A5 row-level security, default", lambda a: a == "a5-rls@default"),
    ("A5 row-level security, iterative", lambda a: a == "a5-rls@iterative"),
    ("A5 document-level security", lambda a: a == "a5-dls"),
    ("A6 partitions", lambda a: a == "a6-partition"),
    ("A7 wardowl", lambda a: a == "a7-wardowl"),
]
WORK = [("w1_enron", "W1"), ("w2_tree_a", "Tree"), ("w2_uniform_a", "Uniform"), ("w2_erbac_a", "ERBAC-A"),
        ("w2_erbac_b", "ERBAC-B")]
lines = [r"\begin{table*}[t]", r"\caption{Recall@10 on real sharing (W1, Enron, all 3{,}985 questions, 2{,}000 of them about "
         r"mail the user may not read) and HoneyBee's role-based "
         r"workloads (W2), mean over users and three seeds; a range spans the stores an arm ran on. The exact control "
         r"(A0) scored 1.000 in every cell. OpenSearch has one setting, counted in the default rows only. "
         r"Per-store values with 95\% intervals are in \texttt{cells.json} of the results release.}", r"\label{tab:quality}", r"\small", r"\begin{tabular}{@{}lrrrrr@{}}", r"\toprule",
         r" & W1 & \multicolumn{4}{c}{W2} \\ \cmidrule(l){3-6}",
         "Arm & Enron & " + " & ".join(n for _, n in WORK[1:]) + r" \\", r"\midrule"]
for label, pick in ROWS:
    row = [label]
    for wl, _ in WORK:
        vals = [c["recall"] for c in cells if c["workload"] == wl and pick(c["arm"]) and c["recall"] is not None]
        row.append(rng(vals) if vals else "--")
    lines.append(" & ".join(row) + r" \\")
lines += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
(OUT / "tab-quality.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")

# ---- Hypotheses table ----
TEXT = {
    "H1": "W1 own mail: A1 recall@10 below 0.5",
    "H2": "W1 own mail: A2 over $10k$ below 0.9",
    "H3": "W3, shares to 0.05: A1, A2 lower under negative than positive correlation",
    "H4": "W3 share 0.5: A3 fails or exceeds 10\\,s on a store",
    "H5": "W3 share 0.01: pgvector without iterative scans below 0.5",
    "H6": "W3: every store's alternative setting at least 0.9 in every cell",
    "H7": "W3: row-level security within 0.02 of the store filter",
    "H8": "Engine stopped: nothing outside the readable set",
}


def detail(k, v):
    parts = v.get("parts") or []
    if k in ("H1", "H2", "H5"):
        lo = min(p["interval"][0] for p in parts); hi = max(p["interval"][1] for p in parts)
        return f"{len(parts)} cells; intervals within {f(lo)}--{f(hi)}"
    if k == "H3":
        hi = max(p["interval"][1] for p in parts)
        return f"{len(parts)} cells; every upper end below 0 (at most ${f(hi)}$)"
    if k == "H4":
        return f"condition met on {sum(p['meets'] for p in parts)} of {len(parts)} stores"
    if k == "H6":
        c = collections.Counter(p["verdict"] for p in parts)
        return f"{c['supported']} supported, {c['not supported']} not, {c['inconclusive']} inconclusive of {len(parts)}"
    if k == "H7":
        w = max(max(abs(p["interval"][0]), abs(p["interval"][1])) for p in parts)
        return f"{len(parts)} cells; every difference exactly 0" if w == 0 else f"{len(parts)} cells; within $\\pm${f(w)}"
    if k == "H8":
        return f"{v['outside']} outside in {v['rows']:,} rows".replace(",", "{,}")
    return ""


lines = [r"\begin{table}[t]", r"\caption{The pre-registered hypotheses and their verdicts, each judged on a 99.375\% interval "
         r"(Bonferroni over eight) by the registered rule; a hypothesis over several cells is supported only if it is "
         r"supported in every cell.}", r"\label{tab:hypotheses}", r"\footnotesize\setlength{\tabcolsep}{4pt}",
         r"\begin{tabularx}{\columnwidth}{@{}l>{\raggedright\arraybackslash}X>{\raggedright\arraybackslash}p{1.3cm}"
         r">{\raggedright\arraybackslash}p{2.6cm}@{}}",
         r"\toprule", r"& Prediction & Verdict & Evidence \\", r"\midrule"]
for k, v in hyp.items():
    lines.append(f"{k} & {TEXT[k]} & {v['verdict']} & {detail(k, v)} \\\\")
lines += [r"\bottomrule", r"\end{tabularx}", r"\end{table}"]
(OUT / "tab-hypotheses.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")

# ---- Faults table ----
FAMS = [("A1 post-filter, OpenFGA", lambda a: a == "a1-fga"), ("A1 post-filter, SpiceDB", lambda a: a == "a1-spicedb"),
        ("A2 over $3k$/$10k$, OpenFGA", lambda a: a.startswith("a2-fga")),
        ("A2 over $3k$/$10k$, SpiceDB", lambda a: a.startswith("a2-spicedb")),
        ("A3 engine pre-filter", lambda a: a.startswith("a3-spicedb")), ("A7 wardowl", lambda a: a == "a7-wardowl")]
FAULTS = [("none", "none"), ("stopped", "refused"), ("slow", "+2\\,s"), ("cut", "cut at 16\\,KiB")]
agg = collections.defaultdict(collections.Counter)
for c in faults:
    arm, _, fault = c["arm"].partition("|")
    for label, pick in FAMS:
        if pick(arm.split("@")[0] if arm.startswith("a3") else arm):
            for x in ("queries", "errors", "empty", "outside", "over_30s"):
                agg[(label, fault or "none")][x] += c[x]
def thousands(n):
    return f"{n:,}".replace(",", "{,}")


lines = [r"\begin{table}[t]", r"\caption{Engine faults: per arm, how many of its $n$ questions raised an error (err.) and how "
         r"many came back empty (emp.) with no fault, with connections refused, with 2\,s added to every engine response, "
         r"and with connections closed after 16\,KiB; five stores, three seeds. No answer under any fault held a chunk "
         r"outside the readable set.}",
         r"\label{tab:faults}", r"\footnotesize\setlength{\tabcolsep}{2.5pt}", r"\begin{tabular}{@{}lrrrrrrrrr@{}}",
         r"\toprule",
         r" & & \multicolumn{2}{c}{none} & \multicolumn{2}{c}{refused} & \multicolumn{2}{c}{+2\,s} & \multicolumn{2}{c}{cut} \\",
         r"\cmidrule(lr){3-4}\cmidrule(lr){5-6}\cmidrule(lr){7-8}\cmidrule(l){9-10}",
         r"Arm & $n$ & err. & emp. & err. & emp. & err. & emp. & err. & emp. \\", r"\midrule"]
outside = sum(c["outside"] for c in faults)
for label, _ in FAMS:
    n = agg[(label, "none")]["queries"]
    row = [label, thousands(n)]
    for key, _ in FAULTS:
        v = agg[(label, key)]
        assert v["queries"] == n, (label, key)
        row += [thousands(v["errors"]), thousands(v["empty"])]
    lines.append(" & ".join(row) + r" \\")
lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
(OUT / "tab-faults.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")

# ---- Regimes: a summary of the W3 cells by readable share ----
SHARES = [("0p001", "0.001"), ("0p01", "0.01"), ("0p05", "0.05"), ("0p2", "0.2"), ("0p5", "0.5")]
CORRS = ("neg", "none", "pos")
STORES = [("pgvector", "pgvector"), ("qdrant", "Qdrant"), ("milvus", "Milvus"), ("weaviate", "Weaviate"),
          ("opensearch", "OpenSearch")]
SETTING = {"default": "default", "iterative": "iterative", "acorn": "ACORN", "pathseer": "PathSeer"}
W3 = {(c["layout"], c["store"], c["arm"]): c for c in cells if c["workload"] == "w3"}


def ms(x):
    return f"{x:.1f}" if x < 1000 else f"{x / 1000:.1f}\\,s"


def span(values):
    lo, hi = ms(min(values)), ms(max(values))
    return lo if lo == hi else f"{lo}--{hi}"


lines = [r"\begin{table*}[t]",
         r"\caption{The controlled sweep (W3) by readable share, summarizing Figures~\ref{fig:w3-recall} and "
         r"\ref{fig:w3-p50}: which stores' own filters (A4) recalled 1.000 (to three decimals) under all three "
         r"correlations, and their median latency, or else the store filter whose lowest recall over the correlations "
         r"was highest; the store filter with the lowest recall; the exact control's median "
         r"latency (A0, pgvector, one question per user, so over a subset of the questions the other arms answered); "
         r"and the highest recall of any post-filter (A1, A2). Latencies in ms unless marked; ranges span the three "
         r"correlations and the stores named.}",
         r"\label{tab:regimes}", r"\footnotesize", r"\begin{tabular}{@{}lllll@{}}", r"\toprule",
         r"Share & A4 recalling 1.000 under every correlation (median latency) & Lowest A4 recall & A0 median latency & "
         r"Best post-filter recall \\", r"\midrule"]
for code, label in SHARES:
    exact, lat, worst, best = [], [], None, None
    for st, name in STORES:
        settings = sorted({a.split("@")[1] for (l, s, a) in W3 if s == st and a.startswith("a4@")},
                          key=lambda x: x != "default")
        ok = []
        for setting in settings:
            cs = [W3[(f"w3_s{code}_{corr}", st, f"a4@{setting}")] for corr in CORRS]
            low = min(c["recall"] for c in cs)
            if worst is None or low < worst[0]:
                worst = (low, name, SETTING[setting])
            if best is None or low > best[0]:
                best = (low, name, SETTING[setting], [c["p50_ms"]["median"] for c in cs])
            if f(low) == "1.000":
                ok.append(setting)
                lat += [c["p50_ms"]["median"] for c in cs]
        if ok:
            exact.append(name if len(settings) == 1 else
                         f"{name} (both)" if len(ok) == len(settings) else f"{name} ({SETTING[ok[0]]})")
    a0 = [W3[(f"w3_s{code}_{corr}", "pgvector", "a0")]["p50_ms"]["median"] for corr in CORRS]
    post = max(c["recall"] for (l, s, a), c in W3.items() if l.startswith(f"w3_s{code}_") and a.startswith(("a1", "a2")))
    held = (", ".join(exact) + f" ({span(lat)})" if exact else
            f"none; best {f(best[0])} ({best[1]}, {best[2]}; {span(best[3])})")
    lines.append(" & ".join([label, held, f"{f(worst[0])} ({worst[1]}, {worst[2]})", span(a0), f(post)]) + r" \\")
lines += [r"\bottomrule", r"\end{tabular}", r"\end{table*}"]
(OUT / "tab-regimes.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")

# ---- Numbers the text quotes ----
tot = collections.Counter()
for c in cells:
    for x in ("queries", "outside", "errors", "empty", "over_30s"):
        tot[x] += c[x]
# Distinct (user, question) pairs: every pair is asked once per job by an arm that answers every pair (A1 with
# SpiceDB answers every pair in every cell), so its queries over its jobs, summed over workloads and layouts.
pairs = sum(c["queries"] // c["jobs"] for c in cells if c["store"] == "pgvector" and c["arm"] == "a1-spicedb")
nums = {
    "NumPairs": f"{pairs:,}",
    "NumCells": f"{len(cells):,}", "NumQueries": f"{tot['queries']:,}", "NumOutside": str(tot["outside"]),
    "NumErrors": str(tot["errors"]), "NumFaultRows": f"{sum(c['queries'] for c in faults):,}",
    "NumFaultOutside": str(outside), "NumChurnEvents": f"{sum(r['events'] for r in churn):,}",
    "NumChurnCensored": str(sum(r["censored"] for r in churn)),
}
(OUT / "numbers.tex").write_text("".join(f"\\newcommand{{\\{k}}}{{{v.replace(',', '{,}')}}}\n" for k, v in nums.items()),
                                 encoding="utf-8")
print({k: v for k, v in nums.items()})
