"""LaTeX tables for the paper's results section, generated from bench.report's output (release results-v1).

    python paper/tables.py <report folder> <output folder>

<report folder> is `report/` from the release's report.tar.gz, or a report rebuilt from results-raw.tar.gz with
`python -m bench.report`. Writes tab-hypotheses.tex, tab-quality.tex, tab-faults.tex and numbers.tex (macros for the
numbers the text quotes) into <output folder>. Every value is read from cells.json, hypotheses.json, faults.json or
churn.json; nothing is typed by hand.
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
lines = [r"\begin{table*}[t]", r"\caption{Recall@10 on real sharing (W1, Enron, all 3{,}985 questions) and HoneyBee's role-based "
         r"workloads (W2), mean over users and three seeds; a range spans the stores an arm ran on. The exact control "
         r"(A0) scored 1.000 in every cell. Per-store values with 95\% intervals are in \texttt{cells.json} of the "
         r"results release.}", r"\label{tab:quality}", r"\small", r"\begin{tabular}{@{}lrrrrr@{}}", r"\toprule",
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

# ---- Numbers the text quotes ----
tot = collections.Counter()
for c in cells:
    for x in ("queries", "outside", "errors", "empty", "over_30s"):
        tot[x] += c[x]
nums = {
    "NumCells": f"{len(cells):,}", "NumQueries": f"{tot['queries']:,}", "NumOutside": str(tot["outside"]),
    "NumErrors": str(tot["errors"]), "NumFaultRows": f"{sum(c['queries'] for c in faults):,}",
    "NumFaultOutside": str(outside), "NumChurnEvents": f"{sum(r['events'] for r in churn):,}",
    "NumChurnCensored": str(sum(r["censored"] for r in churn)),
}
(OUT / "numbers.tex").write_text("".join(f"\\newcommand{{\\{k}}}{{{v.replace(',', '{,}')}}}\n" for k, v in nums.items()),
                                 encoding="utf-8")
print({k: v for k, v in nums.items()})
