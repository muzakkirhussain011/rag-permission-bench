# Supplementary analyses of results-v1

Made by `python -m bench.extras` in workflow run 43465687888 of muzakkirhussain011/rag-permission-bench (`.github/workflows/extras.yml`). None of this is the registered analysis (`bench.report`). Parts (a) and (b) report what the pre-registration promised beside the hypotheses; part (c) is exploratory.

- Release: `results-v1`; its `SHA256SUMS` (checked before use):
  - `176ab017dc7cd5f0a75a9c092c169cb867e2a6545cc6caaea39dc70945110506  results-raw.tar.gz`
  - `85f2f25eadf1b9f2192c6babcd05829918394ff7366a066bfac479ee1c9a7262  report.tar.gz`
- Code: commit `1260760b76ab1ee832b03d4065270733a0dd83c5`.
- Bootstrap: 10,000 resamples, seed 5.

| file | what it holds |
|---|---|
| `workloads.md`, `workloads.json` | (a) achieved readable share per user and per-query correlation rho_q per W3 layout; W2 readable shares beside HoneyBee's Table 1; W1 by question kind |
| `costs.md`, `costs.json` | (b) p50 and p99 latency per cell and job, container memory after the measured pass, sizes, load and index times, partitions, runners, and what was not recorded |
| `sensitivity.md`, `sensitivity.json` | (c) exploratory: H1 to H8 with questions resampled as clusters |
| `rebuild.json` | the report rebuilt from `results-raw.tar.gz` compared with the published one |

## The report rebuilt from the raw outputs

`bench.report` run on `results-raw.tar.gz` gave files identical to the published report: cells.json, hypotheses.json, faults.json, churn.json, coverage.json, harness.json; files that differ: none.

## (a) in brief

- W3: the mean achieved share was 1.00 to 1.55 times the target share across the 15 layouts (folders are granted whole until the share is reached). Mean rho_q by target correlation: neg -0.735 (layouts from -0.955 to -0.396); none -0.321 (layouts from -0.781 to -0.013); pos -0.007 (layouts from -0.410 to 0.175).
- W2 mean readable share over all 1,000 users (HoneyBee's Table 1 value): w2_erbac_a 0.0737 (0.128); w2_erbac_b 0.1557 (0.285); w2_tree_a 0.0415 (0.036); w2_uniform_a 0.0369 (0.054).

## (b) in brief

- p99 latency is available for all 1085 cells; the per-job p50 and p99 recomputed from the raw rows differ from the published `cells.json` by at most 0.000000 ms.
- Sizes were reported by: pgvector; a separate index time by: milvus, pgvector, qdrant. Memory is one snapshot after the measured pass of each run job.

## (c) in brief (exploratory)

- H1: registered supported; questions as clusters supported; users crossed with questions supported; 0 of 10 parts change verdict under a cluster scheme.
- H2: registered supported; questions as clusters supported; users crossed with questions supported; 0 of 10 parts change verdict under a cluster scheme.
- H3: registered supported; questions as clusters supported; users crossed with questions supported; 0 of 90 parts change verdict under a cluster scheme.
- H4: registered supported; questions as clusters supported; users crossed with questions supported (no interval).
- H5: registered supported; questions as clusters supported; users crossed with questions supported; 0 of 3 parts change verdict under a cluster scheme.
- H6: registered not supported; questions as clusters not supported; users crossed with questions not supported; 7 of 75 parts change verdict under a cluster scheme.
- H7: registered supported; questions as clusters supported; users crossed with questions supported; 0 of 30 parts change verdict under a cluster scheme.
- H8: registered supported; questions as clusters supported; users crossed with questions supported (no interval).

Verdict changes under a cluster scheme: none.

