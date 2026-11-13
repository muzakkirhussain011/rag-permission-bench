# (a) Workloads: achieved readable shares and query-permission correlation

Source: each workload release's `truth.jsonl.gz` (the exact answers `bench.truth` wrote when the data were built), `layouts.json` and stats file. Definitions as in `bench/truth.py`: sigma_g is the share of the corpus a user may read; sigma_l is the share of the question's 2,048 nearest chunks, ignoring permissions, that the user may read (`bench.truth`'s default `--nn`, which the prepare workflows use); rho_q = (r - 1) / (r + 1) with r = sigma_l / sigma_g: 0 when readable chunks are as common near the question as in the whole corpus, above 0 when they are more common, below 0 when rarer (from -1 up to, not including, 1).

## W3, the controlled sweep

1,000,000 chunks; questions drawn from a pool of 300. Shares are per user (each user's sigma_g); rho_q is per (user, question) pair.

| layout | target share | correlation | achieved share, mean over users (min to max) | rho_q mean | rho_q median (p25 to p75) | sigma_l mean | users per question, mean (max) |
|---|---|---|---|---|---|---|---|
| w3_s0p001_neg | 0.001 | neg | 0.0014 (0.0010 to 0.0024) | -0.955 | -1.000 (-1.000 to -1.000) | 0.0001 | 3.38 (10) |
| w3_s0p001_none | 0.001 | none | 0.0015 (0.0010 to 0.0025) | -0.781 | -1.000 (-1.000 to -1.000) | 0.0012 | 3.45 (9) |
| w3_s0p001_pos | 0.001 | pos | 0.0014 (0.0011 to 0.0026) | -0.410 | -1.000 (-1.000 to 0.196) | 0.0040 | 3.39 (8) |
| w3_s0p01_neg | 0.01 | neg | 0.0105 (0.0100 to 0.0121) | -0.898 | -1.000 (-1.000 to -0.909) | 0.0011 | 3.42 (11) |
| w3_s0p01_none | 0.01 | none | 0.0106 (0.0100 to 0.0119) | -0.488 | -0.677 (-0.914 to -0.156) | 0.0114 | 3.42 (9) |
| w3_s0p01_pos | 0.01 | pos | 0.0107 (0.0100 to 0.0124) | -0.054 | -0.032 (-0.653 to 0.550) | 0.0350 | 3.51 (12) |
| w3_s0p05_neg | 0.05 | neg | 0.0505 (0.0500 to 0.0517) | -0.810 | -0.943 (-1.000 to -0.776) | 0.0106 | 3.45 (10) |
| w3_s0p05_none | 0.05 | none | 0.0505 (0.0500 to 0.0517) | -0.228 | -0.253 (-0.589 to 0.107) | 0.0529 | 3.47 (10) |
| w3_s0p05_pos | 0.05 | pos | 0.0507 (0.0500 to 0.0522) | 0.112 | 0.246 (-0.308 to 0.600) | 0.1378 | 3.46 (9) |
| w3_s0p2_neg | 0.2 | neg | 0.2006 (0.2000 to 0.2022) | -0.618 | -0.749 (-0.898 to -0.449) | 0.0725 | 3.42 (8) |
| w3_s0p2_none | 0.2 | none | 0.2006 (0.2000 to 0.2018) | -0.095 | -0.073 (-0.278 to 0.129) | 0.1978 | 3.41 (8) |
| w3_s0p2_pos | 0.2 | pos | 0.2006 (0.2000 to 0.2015) | 0.175 | 0.322 (-0.018 to 0.481) | 0.3997 | 3.46 (9) |
| w3_s0p5_neg | 0.5 | neg | 0.5006 (0.5000 to 0.5018) | -0.396 | -0.439 (-0.672 to -0.126) | 0.2731 | 3.45 (9) |
| w3_s0p5_none | 0.5 | none | 0.5006 (0.5000 to 0.5022) | -0.013 | 0.001 (-0.104 to 0.100) | 0.5111 | 3.44 (9) |
| w3_s0p5_pos | 0.5 | pos | 0.5006 (0.5000 to 0.5019) | 0.141 | 0.220 (0.107 to 0.280) | 0.7211 | 3.47 (8) |

The mean achieved share recorded when the layouts were built (`achieved_share_mean` in `layouts.json`) is beside each layout in `workloads.json`. Pairs with an undefined rho_q (the user may read nothing): none.

## W2, HoneyBee's role-based workloads, rebuilt from the paper's text

| workload | HoneyBee Table 1, average access selectivity (as quoted in `bench/w2.py`) | readable share over all 1,000 users, mean (min, median, max) | the 100 measured users, mean (min to max) | rho_q mean (median) | users per question, mean (max) |
|---|---|---|---|---|---|
| w2_erbac_a | 0.128 | 0.0737 (0.0009, 0.0692, 0.2005) | 0.0779 (0.0009 to 0.1857) | -0.011 (-0.005) | 3.44 (10) |
| w2_erbac_b | 0.285 | 0.1557 (0.0009, 0.1555, 0.3533) | 0.1582 (0.0099 to 0.3355) | -0.003 (-0.002) | 3.45 (10) |
| w2_tree_a | 0.036 | 0.0415 (0.0200, 0.0400, 0.0500) | 0.0429 (0.0200 to 0.0500) | -0.005 (-0.004) | 3.45 (10) |
| w2_uniform_a | 0.054 | 0.0369 (0.0019, 0.0362, 0.0962) | 0.0402 (0.0026 to 0.0926) | -0.014 (-0.004) | 3.50 (13) |

## W1, Enron

250,251 messages; 200 users; 3,985 (user, question) pairs over 3,632 distinct questions. Readable share per user: mean 0.0010 (0.0002 to 0.0146); readable messages per user: median 121 (50 to 3659).

| question kind | pairs | rho_q mean | rho_q median (p25 to p75) | sigma_l mean |
|---|---|---|---|---|
| other | 2,000 | -0.519 | -1.000 (-1.000 to 0.066) | 0.0010 |
| own | 1,985 | 0.684 | 0.789 (0.565 to 0.915) | 0.0119 |

