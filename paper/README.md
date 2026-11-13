# The paper's tables

The scripts that generate the tables of the paper "Enforcing Document Permissions in Vector Search: An Experimental
Comparison" from the study's report. They read only `bench.report`'s output; beyond it they compute only groupings,
sums, counts, minima, maxima and medians over its cells. Every recall, interval and verdict comes from `bench.report`.

| script | writes |
|---|---|
| `tables.py` | `tab-quality.tex` (recall@10 on W1 and W2 per arm, range over stores), `tab-hypotheses.tex` (H1 to H8 and their verdicts), `tab-faults.tex` (errors and empty answers under engine faults), `tab-regimes.tex` (the W3 sweep summarized by readable share), `numbers.tex` (macros for the counts the text quotes) |
| `digest.py` | a Markdown digest of every cell, hypothesis part, change delay and fault count, from which the text's numbers were taken |

The figures are made by `bench.figures` (see the main README). The paper's text is not part of this repository.

## Run them

Both take the folder `report/` from the release `results-v1` (inside `report.tar.gz`), or a report rebuilt from the
raw outputs with `python -m bench.report` (see "Reproduce the paper" in the main README). From the repository root,
with Python 3.12 and nothing beyond the standard library:

```bash
gh release download results-v1 -R muzakkirhussain011/rag-permission-bench -p report.tar.gz -p SHA256SUMS
sha256sum -c SHA256SUMS --ignore-missing
tar xzf report.tar.gz
python paper/tables.py report paper-tables
python paper/digest.py report > paper-tables/digest.md
```

The `extras` workflow (`.github/workflows/extras.yml`) runs the last two commands on the published report and keeps
their output in its artifact. `tests/test_paper.py` runs both scripts on a made-up report in CI.
