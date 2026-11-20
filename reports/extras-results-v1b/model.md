# (d) The post-filter model against the measurements

A post-filter asks an unfiltered search for its m nearest chunks and keeps the first k = 10 the user may read. Any readable chunk among the m nearest is among the k nearest readable chunks whenever fewer than k readable chunks come before it, so with an exact unfiltered search the post-filter's recall@10 is min(10, readable among the m nearest) / min(10, readable). The predicted values below use each question's exact unfiltered neighbours (inner product, ties by chunk id) and each user's readable set from the workload release, averaged as `bench.report` averages recall (per user, then over users). A1 checks m = 10, A2 m = 30 and m = 100. The measured values are the post-filters' recall from the raw outputs; the differences come from the stores' approximate unfiltered search and from ties. sigma_l is the readable share of each question's 2,048 nearest chunks (`bench.truth`), averaged the same way.

## Measured minus predicted, over every store and cell

| workload | arms | question kind | cells | min | max | largest absolute |
|---|---|---|---|---|---|---|
| w1_enron | A1 (m = 10) | all | 10 | -0.011 | -0.004 | 0.011 |
| w1_enron | A1 (m = 10) | other | 10 | 0.000 | 0.000 | 0.000 |
| w1_enron | A1 (m = 10) | own | 10 | -0.022 | -0.009 | 0.022 |
| w1_enron | A2 (m = 30, 100) | all | 20 | -0.018 | -0.006 | 0.018 |
| w1_enron | A2 (m = 30, 100) | other | 20 | -0.001 | 0.000 | 0.001 |
| w1_enron | A2 (m = 30, 100) | own | 20 | -0.036 | -0.013 | 0.036 |
| w2_erbac_a | A1 (m = 10) | all | 10 | -0.000 | 0.001 | 0.001 |
| w2_erbac_a | A2 (m = 30, 100) | all | 20 | -0.039 | -0.000 | 0.039 |
| w2_erbac_b | A1 (m = 10) | all | 10 | -0.001 | 0.001 | 0.001 |
| w2_erbac_b | A2 (m = 30, 100) | all | 20 | -0.059 | -0.003 | 0.059 |
| w2_tree_a | A1 (m = 10) | all | 10 | 0.000 | 0.002 | 0.002 |
| w2_tree_a | A2 (m = 30, 100) | all | 20 | -0.001 | 0.002 | 0.002 |
| w2_uniform_a | A1 (m = 10) | all | 10 | 0.000 | 0.001 | 0.001 |
| w2_uniform_a | A2 (m = 30, 100) | all | 20 | -0.001 | 0.004 | 0.004 |
| w3 | A1 (m = 10) | all | 150 | -0.027 | 0.004 | 0.027 |
| w3 | A1 against sigma_l | all | 150 | -0.048 | 0.046 | 0.048 |
| w3 | A2 (m = 30, 100) | all | 300 | -0.107 | 0.001 | 0.107 |

## Per layout

Predicted recall of a post-filter over the m nearest chunks; measured A1 and A2 (SpiceDB) as the range over stores; OpenSearch's document-level security.

| workload | layout | kind | pairs | sigma_l | pred m=10 | A1 measured | pred m=30 | A2 3k measured | pred m=100 | A2 10k measured | pred m=200 | pred m=300 | DLS measured |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| w1_enron | w1_enron | all | 3985 | 0.0064 | 0.138 | 0.127 to 0.134 | 0.196 | 0.181 to 0.190 | 0.245 | 0.227 to 0.237 | 0.274 | 0.294 | 0.209 |
| w1_enron | w1_enron | other | 2000 | 0.0010 | 0.001 | 0.001 | 0.002 | 0.002 | 0.009 | 0.008 to 0.010 | 0.019 | 0.028 | 0.019 |
| w1_enron | w1_enron | own | 1985 | 0.0121 | 0.280 | 0.258 to 0.272 | 0.394 | 0.364 to 0.382 | 0.486 | 0.450 to 0.469 | 0.534 | 0.565 | 0.404 |
| w2_erbac_a | w2_erbac_a | all | 1000 | 0.0775 | 0.073 | 0.073 to 0.074 | 0.232 | 0.230 to 0.231 | 0.661 | 0.622 to 0.651 | 0.845 | 0.894 | 0.418 |
| w2_erbac_b | w2_erbac_b | all | 1000 | 0.1575 | 0.149 | 0.148 to 0.150 | 0.452 | 0.445 to 0.449 | 0.858 | 0.800 to 0.848 | 0.951 | 0.981 | 0.519 |
| w2_tree_a | w2_tree_a | all | 1000 | 0.0427 | 0.043 | 0.043 to 0.044 | 0.125 | 0.124 to 0.125 | 0.412 | 0.412 to 0.414 | 0.771 | 0.933 | 0.322 |
| w2_uniform_a | w2_uniform_a | all | 1000 | 0.0401 | 0.036 | 0.036 to 0.037 | 0.120 | 0.119 to 0.120 | 0.384 | 0.383 to 0.388 | 0.675 | 0.785 | 0.282 |
| w3 | w3_s0p001_neg | all | 1000 | 0.0001 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.001 |
| w3 | w3_s0p001_none | all | 1000 | 0.0012 | 0.002 | 0.002 | 0.002 | 0.002 | 0.006 | 0.005 to 0.006 | 0.013 | 0.019 | 0.015 |
| w3 | w3_s0p001_pos | all | 1000 | 0.0040 | 0.004 | 0.003 to 0.004 | 0.010 | 0.009 to 0.010 | 0.027 | 0.025 to 0.027 | 0.045 | 0.062 | 0.054 |
| w3 | w3_s0p01_neg | all | 1000 | 0.0011 | 0.000 | 0.000 | 0.002 | 0.001 | 0.003 | 0.003 | 0.008 | 0.012 | 0.011 |
| w3 | w3_s0p01_none | all | 1000 | 0.0114 | 0.014 | 0.014 | 0.028 | 0.027 to 0.028 | 0.065 | 0.061 to 0.065 | 0.108 | 0.143 | 0.111 |
| w3 | w3_s0p01_pos | all | 1000 | 0.0350 | 0.036 | 0.036 to 0.038 | 0.086 | 0.083 to 0.086 | 0.189 | 0.162 to 0.187 | 0.281 | 0.343 | 0.262 |
| w3 | w3_s0p05_neg | all | 1000 | 0.0106 | 0.004 | 0.003 to 0.004 | 0.014 | 0.012 to 0.015 | 0.032 | 0.027 to 0.031 | 0.066 | 0.099 | 0.069 |
| w3 | w3_s0p05_none | all | 1000 | 0.0529 | 0.058 | 0.057 to 0.059 | 0.128 | 0.125 to 0.127 | 0.282 | 0.249 to 0.280 | 0.418 | 0.521 | 0.389 |
| w3 | w3_s0p05_pos | all | 1000 | 0.1378 | 0.158 | 0.158 to 0.161 | 0.311 | 0.292 to 0.309 | 0.516 | 0.439 to 0.505 | 0.633 | 0.705 | 0.589 |
| w3 | w3_s0p2_neg | all | 1000 | 0.0725 | 0.051 | 0.049 to 0.050 | 0.104 | 0.099 to 0.104 | 0.232 | 0.199 to 0.224 | 0.376 | 0.482 | 0.335 |
| w3 | w3_s0p2_none | all | 1000 | 0.1978 | 0.183 | 0.181 to 0.184 | 0.402 | 0.377 to 0.401 | 0.711 | 0.605 to 0.699 | 0.838 | 0.901 | 0.771 |
| w3 | w3_s0p2_pos | all | 1000 | 0.3997 | 0.446 | 0.439 to 0.446 | 0.684 | 0.638 to 0.678 | 0.827 | 0.747 to 0.817 | 0.882 | 0.910 | 0.850 |
| w3 | w3_s0p5_neg | all | 1000 | 0.2731 | 0.227 | 0.225 to 0.226 | 0.412 | 0.389 to 0.407 | 0.662 | 0.582 to 0.646 | 0.805 | 0.867 | 0.733 |
| w3 | w3_s0p5_none | all | 1000 | 0.5111 | 0.521 | 0.511 to 0.521 | 0.820 | 0.760 to 0.812 | 0.948 | 0.859 to 0.937 | 0.982 | 0.993 | 0.952 |
| w3 | w3_s0p5_pos | all | 1000 | 0.7211 | 0.765 | 0.739 to 0.761 | 0.907 | 0.852 to 0.896 | 0.960 | 0.898 to 0.949 | 0.979 | 0.988 | 0.957 |
