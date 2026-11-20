# Supplementary analyses of results-v1, second part

Made by `python -m bench.extras2` in workflow run 44807243538 of muzakkirhussain011/rag-permission-bench (`.github/workflows/extras.yml`, part v1b). None of this is the registered analysis (`bench.report`) and no store or engine ran: every number comes from the release's raw outputs and report and from the workload releases. The first part is `reports/extras-results-v1`.

- Release: `results-v1`; its `SHA256SUMS` (checked before use):
  - `176ab017dc7cd5f0a75a9c092c169cb867e2a6545cc6caaea39dc70945110506  results-raw.tar.gz`
  - `85f2f25eadf1b9f2192c6babcd05829918394ff7366a066bfac479ee1c9a7262  report.tar.gz`
- Code: commit `2ce7be42f06d7b56281265b6c90c5850b35acd40`.

| file | what it holds |
|---|---|
| `model.md`, `model.json` | (d) post-filter recall predicted from the exact unfiltered neighbours, against the measured post-filters and document-level security; A1 against sigma_l |
| `answers.md`, `answers.json` | (e) per cell: recall, short answers, exact answers, empty answers; W1 by question kind |
| `plans.md`, `plans.json` | (f) pgvector's kept executed plans: shape, estimated and actual rows |
| `pairs.md`, `pairs.json` | (g) A3 and A4 on the same pairs; Qdrant's settings on the same queries |
| `churn-faults.md`, `churn-faults.json` | (h) the change and fault runs' layouts, pairs and probes |
| `order.md`, `order.json` | (i) arm order and latency |
| `figures/` | the paper's figures, drawn by `bench.figures` at this commit from the published report (which `reports/extras-results-v1/rebuild.json` found identical to the one rebuilt from the raw outputs) |

## In brief

- Model, w1_enron a1 all: measured minus predicted from -0.011 to -0.004 over 10 cells.
- Model, w1_enron a1 other: measured minus predicted from 0.000 to 0.000 over 10 cells.
- Model, w1_enron a1 own: measured minus predicted from -0.022 to -0.009 over 10 cells.
- Model, w1_enron a2 all: measured minus predicted from -0.018 to -0.006 over 20 cells.
- Model, w1_enron a2 other: measured minus predicted from -0.001 to 0.000 over 20 cells.
- Model, w1_enron a2 own: measured minus predicted from -0.036 to -0.013 over 20 cells.
- Model, w2_erbac_a a1 all: measured minus predicted from -0.000 to 0.001 over 10 cells.
- Model, w2_erbac_a a2 all: measured minus predicted from -0.039 to -0.000 over 20 cells.
- Model, w2_erbac_b a1 all: measured minus predicted from -0.001 to 0.001 over 10 cells.
- Model, w2_erbac_b a2 all: measured minus predicted from -0.059 to -0.003 over 20 cells.
- Model, w2_tree_a a1 all: measured minus predicted from 0.000 to 0.002 over 10 cells.
- Model, w2_tree_a a2 all: measured minus predicted from -0.001 to 0.002 over 20 cells.
- Model, w2_uniform_a a1 all: measured minus predicted from 0.000 to 0.001 over 10 cells.
- Model, w2_uniform_a a2 all: measured minus predicted from -0.001 to 0.004 over 20 cells.
- Model, w3 a1 all: measured minus predicted from -0.027 to 0.004 over 150 cells.
- Model, w3 a1-vs-sigma_l all: measured minus predicted from -0.048 to 0.046 over 150 cells.
- Model, w3 a2 all: measured minus predicted from -0.107 to 0.001 over 300 cells.
- Arm order: the earliest job was the slowest in 369 of 1085 cells; an earlier job was slower in 0.500 of 3020 job pairs.
