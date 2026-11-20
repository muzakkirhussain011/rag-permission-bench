# (e) Answers per cell

From every run job's scored rows. `short`: answers with fewer hits than min(10, readable) and no error; an exact search never returns one, so on pgvector a short answer of the filtered arms comes from a plan that filters the rows an index scan returns. `exact`: answers with recall 1. Shares are over the answers without an error. Recall is `bench.report`'s estimator; it matches the published `cells.json` to 0.00e+00 over 1085 cells.

## W3, the store-side arms

| store | arm | layout | queries | recall | short | exact |
|---|---|---|---|---|---|---|
| milvus | a3-spicedb@default | w3_s0p001_neg | 3000 | 1.000 | 0.000 | 1.000 |
| milvus | a3-spicedb@default | w3_s0p001_none | 3000 | 1.000 | 0.000 | 1.000 |
| milvus | a3-spicedb@default | w3_s0p001_pos | 3000 | 1.000 | 0.000 | 1.000 |
| milvus | a3-spicedb@default | w3_s0p01_neg | 3000 | 1.000 | 0.000 | 1.000 |
| milvus | a3-spicedb@default | w3_s0p01_none | 3000 | 1.000 | 0.000 | 1.000 |
| milvus | a3-spicedb@default | w3_s0p01_pos | 3000 | 1.000 | 0.000 | 1.000 |
| milvus | a3-spicedb@default | w3_s0p05_neg | 900 | 1.000 | 0.000 | 1.000 |
| milvus | a3-spicedb@default | w3_s0p05_none | 900 | 1.000 | 0.000 | 1.000 |
| milvus | a3-spicedb@default | w3_s0p05_pos | 900 | 1.000 | 0.000 | 1.000 |
| milvus | a3-spicedb@default | w3_s0p2_neg | 300 | 0.955 | 0.000 | 0.713 |
| milvus | a3-spicedb@default | w3_s0p2_none | 300 | 0.966 | 0.000 | 0.777 |
| milvus | a3-spicedb@default | w3_s0p2_pos | 300 | 0.967 | 0.000 | 0.803 |
| milvus | a3-spicedb@default | w3_s0p5_neg | 150 | 0.917 | 0.000 | 0.587 |
| milvus | a3-spicedb@default | w3_s0p5_none | 150 | 0.963 | 0.000 | 0.793 |
| milvus | a3-spicedb@default | w3_s0p5_pos | 150 | 0.969 | 0.000 | 0.800 |
| milvus | a3-spicedb@iterative | w3_s0p001_neg | 3000 | 0.972 | 0.000 | 0.774 |
| milvus | a3-spicedb@iterative | w3_s0p001_none | 3000 | 0.955 | 0.000 | 0.680 |
| milvus | a3-spicedb@iterative | w3_s0p001_pos | 3000 | 0.938 | 0.000 | 0.583 |
| milvus | a3-spicedb@iterative | w3_s0p01_neg | 3000 | 0.936 | 0.000 | 0.588 |
| milvus | a3-spicedb@iterative | w3_s0p01_none | 3000 | 0.941 | 0.000 | 0.617 |
| milvus | a3-spicedb@iterative | w3_s0p01_pos | 3000 | 0.933 | 0.000 | 0.606 |
| milvus | a3-spicedb@iterative | w3_s0p05_neg | 900 | 0.929 | 0.000 | 0.572 |
| milvus | a3-spicedb@iterative | w3_s0p05_none | 900 | 0.944 | 0.000 | 0.659 |
| milvus | a3-spicedb@iterative | w3_s0p05_pos | 900 | 0.944 | 0.000 | 0.701 |
| milvus | a3-spicedb@iterative | w3_s0p2_neg | 300 | 0.910 | 0.000 | 0.563 |
| milvus | a3-spicedb@iterative | w3_s0p2_none | 300 | 0.944 | 0.000 | 0.653 |
| milvus | a3-spicedb@iterative | w3_s0p2_pos | 300 | 0.959 | 0.000 | 0.773 |
| milvus | a3-spicedb@iterative | w3_s0p5_neg | 150 | 0.935 | 0.000 | 0.647 |
| milvus | a3-spicedb@iterative | w3_s0p5_none | 150 | 0.973 | 0.000 | 0.840 |
| milvus | a3-spicedb@iterative | w3_s0p5_pos | 150 | 0.972 | 0.000 | 0.833 |
| milvus | a4@default | w3_s0p001_neg | 3000 | 1.000 | 0.000 | 1.000 |
| milvus | a4@default | w3_s0p001_none | 3000 | 1.000 | 0.000 | 1.000 |
| milvus | a4@default | w3_s0p001_pos | 3000 | 1.000 | 0.000 | 1.000 |
| milvus | a4@default | w3_s0p01_neg | 3000 | 1.000 | 0.000 | 1.000 |
| milvus | a4@default | w3_s0p01_none | 3000 | 1.000 | 0.000 | 1.000 |
| milvus | a4@default | w3_s0p01_pos | 3000 | 1.000 | 0.000 | 1.000 |
| milvus | a4@default | w3_s0p05_neg | 3000 | 1.000 | 0.000 | 1.000 |
| milvus | a4@default | w3_s0p05_none | 3000 | 1.000 | 0.000 | 1.000 |
| milvus | a4@default | w3_s0p05_pos | 3000 | 1.000 | 0.000 | 1.000 |
| milvus | a4@default | w3_s0p2_neg | 3000 | 0.949 | 0.000 | 0.687 |
| milvus | a4@default | w3_s0p2_none | 3000 | 0.966 | 0.000 | 0.777 |
| milvus | a4@default | w3_s0p2_pos | 3000 | 0.972 | 0.000 | 0.825 |
| milvus | a4@default | w3_s0p5_neg | 3000 | 0.930 | 0.000 | 0.659 |
| milvus | a4@default | w3_s0p5_none | 3000 | 0.952 | 0.000 | 0.756 |
| milvus | a4@default | w3_s0p5_pos | 3000 | 0.966 | 0.000 | 0.818 |
| milvus | a4@iterative | w3_s0p001_neg | 3000 | 0.972 | 0.000 | 0.774 |
| milvus | a4@iterative | w3_s0p001_none | 3000 | 0.955 | 0.000 | 0.680 |
| milvus | a4@iterative | w3_s0p001_pos | 3000 | 0.938 | 0.000 | 0.583 |
| milvus | a4@iterative | w3_s0p01_neg | 3000 | 0.936 | 0.000 | 0.588 |
| milvus | a4@iterative | w3_s0p01_none | 3000 | 0.941 | 0.000 | 0.617 |
| milvus | a4@iterative | w3_s0p01_pos | 3000 | 0.933 | 0.000 | 0.606 |
| milvus | a4@iterative | w3_s0p05_neg | 3000 | 0.926 | 0.000 | 0.572 |
| milvus | a4@iterative | w3_s0p05_none | 3000 | 0.947 | 0.000 | 0.676 |
| milvus | a4@iterative | w3_s0p05_pos | 3000 | 0.946 | 0.000 | 0.698 |
| milvus | a4@iterative | w3_s0p2_neg | 3000 | 0.909 | 0.000 | 0.541 |
| milvus | a4@iterative | w3_s0p2_none | 3000 | 0.946 | 0.000 | 0.699 |
| milvus | a4@iterative | w3_s0p2_pos | 3000 | 0.963 | 0.000 | 0.791 |
| milvus | a4@iterative | w3_s0p5_neg | 3000 | 0.929 | 0.000 | 0.657 |
| milvus | a4@iterative | w3_s0p5_none | 3000 | 0.958 | 0.000 | 0.782 |
| milvus | a4@iterative | w3_s0p5_pos | 3000 | 0.970 | 0.000 | 0.832 |
| opensearch | a3-spicedb@default | w3_s0p001_neg | 3000 | 1.000 | 0.000 | 1.000 |
| opensearch | a3-spicedb@default | w3_s0p001_none | 3000 | 1.000 | 0.000 | 1.000 |
| opensearch | a3-spicedb@default | w3_s0p001_pos | 3000 | 1.000 | 0.000 | 1.000 |
| opensearch | a3-spicedb@default | w3_s0p01_neg | 3000 | 1.000 | 0.000 | 1.000 |
| opensearch | a3-spicedb@default | w3_s0p01_none | 3000 | 1.000 | 0.000 | 1.000 |
| opensearch | a3-spicedb@default | w3_s0p01_pos | 3000 | 1.000 | 0.000 | 1.000 |
| opensearch | a3-spicedb@default | w3_s0p05_neg | 900 | 1.000 | 0.000 | 1.000 |
| opensearch | a3-spicedb@default | w3_s0p05_none | 900 | 1.000 | 0.000 | 1.000 |
| opensearch | a3-spicedb@default | w3_s0p05_pos | 900 | 1.000 | 0.000 | 0.999 |
| opensearch | a3-spicedb@default | w3_s0p2_neg | 300 | 0.886 | 0.000 | 0.513 |
| opensearch | a3-spicedb@default | w3_s0p2_none | 300 | 0.970 | 0.000 | 0.800 |
| opensearch | a3-spicedb@default | w3_s0p2_pos | 300 | 0.978 | 0.000 | 0.890 |
| opensearch | a3-spicedb@default | w3_s0p5_neg | 150 | 0.958 | 0.000 | 0.747 |
| opensearch | a3-spicedb@default | w3_s0p5_none | 150 | 0.997 | 0.000 | 0.973 |
| opensearch | a3-spicedb@default | w3_s0p5_pos | 150 | 0.987 | 0.000 | 0.887 |
| opensearch | a4@default | w3_s0p001_neg | 3000 | 1.000 | 0.000 | 1.000 |
| opensearch | a4@default | w3_s0p001_none | 3000 | 1.000 | 0.000 | 1.000 |
| opensearch | a4@default | w3_s0p001_pos | 3000 | 1.000 | 0.000 | 1.000 |
| opensearch | a4@default | w3_s0p01_neg | 3000 | 1.000 | 0.000 | 1.000 |
| opensearch | a4@default | w3_s0p01_none | 3000 | 1.000 | 0.000 | 1.000 |
| opensearch | a4@default | w3_s0p01_pos | 3000 | 1.000 | 0.000 | 1.000 |
| opensearch | a4@default | w3_s0p05_neg | 3000 | 1.000 | 0.000 | 1.000 |
| opensearch | a4@default | w3_s0p05_none | 3000 | 1.000 | 0.000 | 1.000 |
| opensearch | a4@default | w3_s0p05_pos | 3000 | 1.000 | 0.000 | 0.999 |
| opensearch | a4@default | w3_s0p2_neg | 3000 | 0.878 | 0.000 | 0.508 |
| opensearch | a4@default | w3_s0p2_none | 3000 | 0.975 | 0.000 | 0.835 |
| opensearch | a4@default | w3_s0p2_pos | 3000 | 0.980 | 0.000 | 0.889 |
| opensearch | a4@default | w3_s0p5_neg | 3000 | 0.959 | 0.000 | 0.792 |
| opensearch | a4@default | w3_s0p5_none | 3000 | 0.989 | 0.000 | 0.927 |
| opensearch | a4@default | w3_s0p5_pos | 3000 | 0.987 | 0.000 | 0.920 |
| opensearch | a5-dls | w3_s0p001_neg | 3000 | 0.001 | 1.000 | 0.000 |
| opensearch | a5-dls | w3_s0p001_none | 3000 | 0.015 | 0.993 | 0.001 |
| opensearch | a5-dls | w3_s0p001_pos | 3000 | 0.054 | 0.970 | 0.010 |
| opensearch | a5-dls | w3_s0p01_neg | 3000 | 0.011 | 0.998 | 0.000 |
| opensearch | a5-dls | w3_s0p01_none | 3000 | 0.111 | 0.935 | 0.025 |
| opensearch | a5-dls | w3_s0p01_pos | 3000 | 0.262 | 0.768 | 0.083 |
| opensearch | a5-dls | w3_s0p05_neg | 3000 | 0.069 | 0.963 | 0.008 |
| opensearch | a5-dls | w3_s0p05_none | 3000 | 0.389 | 0.636 | 0.136 |
| opensearch | a5-dls | w3_s0p05_pos | 3000 | 0.589 | 0.360 | 0.321 |
| opensearch | a5-dls | w3_s0p2_neg | 3000 | 0.335 | 0.612 | 0.095 |
| opensearch | a5-dls | w3_s0p2_none | 3000 | 0.771 | 0.073 | 0.449 |
| opensearch | a5-dls | w3_s0p2_pos | 3000 | 0.850 | 0.064 | 0.683 |
| opensearch | a5-dls | w3_s0p5_neg | 3000 | 0.733 | 0.087 | 0.439 |
| opensearch | a5-dls | w3_s0p5_none | 3000 | 0.952 | 0.000 | 0.815 |
| opensearch | a5-dls | w3_s0p5_pos | 3000 | 0.957 | 0.000 | 0.860 |
| pgvector | a0 | w3_s0p001_neg | 300 | 1.000 | 0.000 | 1.000 |
| pgvector | a0 | w3_s0p001_none | 300 | 1.000 | 0.000 | 1.000 |
| pgvector | a0 | w3_s0p001_pos | 300 | 1.000 | 0.000 | 1.000 |
| pgvector | a0 | w3_s0p01_neg | 300 | 1.000 | 0.000 | 1.000 |
| pgvector | a0 | w3_s0p01_none | 300 | 1.000 | 0.000 | 1.000 |
| pgvector | a0 | w3_s0p01_pos | 300 | 1.000 | 0.000 | 1.000 |
| pgvector | a0 | w3_s0p05_neg | 300 | 1.000 | 0.000 | 1.000 |
| pgvector | a0 | w3_s0p05_none | 300 | 1.000 | 0.000 | 1.000 |
| pgvector | a0 | w3_s0p05_pos | 300 | 1.000 | 0.000 | 1.000 |
| pgvector | a0 | w3_s0p2_neg | 300 | 1.000 | 0.000 | 1.000 |
| pgvector | a0 | w3_s0p2_none | 300 | 1.000 | 0.000 | 1.000 |
| pgvector | a0 | w3_s0p2_pos | 300 | 1.000 | 0.000 | 1.000 |
| pgvector | a0 | w3_s0p5_neg | 300 | 1.000 | 0.000 | 1.000 |
| pgvector | a0 | w3_s0p5_none | 300 | 1.000 | 0.000 | 1.000 |
| pgvector | a0 | w3_s0p5_pos | 300 | 1.000 | 0.000 | 1.000 |
| pgvector | a3-spicedb@default | w3_s0p001_neg | 3000 | 1.000 | 0.000 | 1.000 |
| pgvector | a3-spicedb@default | w3_s0p001_none | 3000 | 1.000 | 0.000 | 1.000 |
| pgvector | a3-spicedb@default | w3_s0p001_pos | 3000 | 1.000 | 0.000 | 1.000 |
| pgvector | a3-spicedb@default | w3_s0p01_neg | 3000 | 0.003 | 1.000 | 0.000 |
| pgvector | a3-spicedb@default | w3_s0p01_none | 3000 | 0.061 | 0.976 | 0.017 |
| pgvector | a3-spicedb@default | w3_s0p01_pos | 3000 | 0.162 | 0.903 | 0.051 |
| pgvector | a3-spicedb@default | w3_s0p05_neg | 900 | 0.029 | 0.991 | 0.007 |
| pgvector | a3-spicedb@default | w3_s0p05_none | 900 | 0.271 | 0.849 | 0.107 |
| pgvector | a3-spicedb@default | w3_s0p05_pos | 900 | 0.457 | 0.604 | 0.226 |
| pgvector | a3-spicedb@default | w3_s0p2_neg | 300 | 0.236 | 0.830 | 0.123 |
| pgvector | a3-spicedb@default | w3_s0p2_none | 300 | 0.625 | 0.460 | 0.330 |
| pgvector | a3-spicedb@default | w3_s0p2_pos | 300 | 0.758 | 0.237 | 0.563 |
| pgvector | a3-spicedb@default | w3_s0p5_neg | 150 | 0.569 | 0.500 | 0.333 |
| pgvector | a3-spicedb@default | w3_s0p5_none | 150 | 0.902 | 0.060 | 0.713 |
| pgvector | a3-spicedb@default | w3_s0p5_pos | 150 | 0.898 | 0.100 | 0.707 |
| pgvector | a3-spicedb@iterative | w3_s0p001_neg | 3000 | 1.000 | 0.000 | 1.000 |
| pgvector | a3-spicedb@iterative | w3_s0p001_none | 3000 | 1.000 | 0.000 | 1.000 |
| pgvector | a3-spicedb@iterative | w3_s0p001_pos | 3000 | 1.000 | 0.000 | 1.000 |
| pgvector | a3-spicedb@iterative | w3_s0p01_neg | 3000 | 0.323 | 0.472 | 0.073 |
| pgvector | a3-spicedb@iterative | w3_s0p01_none | 3000 | 0.665 | 0.026 | 0.207 |
| pgvector | a3-spicedb@iterative | w3_s0p01_pos | 3000 | 0.767 | 0.013 | 0.267 |
| pgvector | a3-spicedb@iterative | w3_s0p05_neg | 900 | 0.608 | 0.020 | 0.190 |
| pgvector | a3-spicedb@iterative | w3_s0p05_none | 900 | 0.860 | 0.000 | 0.390 |
| pgvector | a3-spicedb@iterative | w3_s0p05_pos | 900 | 0.869 | 0.000 | 0.450 |
| pgvector | a3-spicedb@iterative | w3_s0p2_neg | 300 | 0.832 | 0.000 | 0.373 |
| pgvector | a3-spicedb@iterative | w3_s0p2_none | 300 | 0.873 | 0.000 | 0.490 |
| pgvector | a3-spicedb@iterative | w3_s0p2_pos | 300 | 0.920 | 0.000 | 0.677 |
| pgvector | a3-spicedb@iterative | w3_s0p5_neg | 150 | 0.852 | 0.000 | 0.507 |
| pgvector | a3-spicedb@iterative | w3_s0p5_none | 150 | 0.945 | 0.000 | 0.740 |
| pgvector | a3-spicedb@iterative | w3_s0p5_pos | 150 | 0.955 | 0.000 | 0.747 |
| pgvector | a4@default | w3_s0p001_neg | 3000 | 0.977 | 0.023 | 0.977 |
| pgvector | a4@default | w3_s0p001_none | 3000 | 0.930 | 0.070 | 0.930 |
| pgvector | a4@default | w3_s0p001_pos | 3000 | 0.973 | 0.028 | 0.971 |
| pgvector | a4@default | w3_s0p01_neg | 3000 | 0.003 | 1.000 | 0.000 |
| pgvector | a4@default | w3_s0p01_none | 3000 | 0.061 | 0.976 | 0.017 |
| pgvector | a4@default | w3_s0p01_pos | 3000 | 0.162 | 0.903 | 0.051 |
| pgvector | a4@default | w3_s0p05_neg | 3000 | 0.030 | 0.990 | 0.007 |
| pgvector | a4@default | w3_s0p05_none | 3000 | 0.254 | 0.856 | 0.099 |
| pgvector | a4@default | w3_s0p05_pos | 3000 | 0.444 | 0.628 | 0.210 |
| pgvector | a4@default | w3_s0p2_neg | 3000 | 0.206 | 0.874 | 0.086 |
| pgvector | a4@default | w3_s0p2_none | 3000 | 0.620 | 0.456 | 0.292 |
| pgvector | a4@default | w3_s0p2_pos | 3000 | 0.757 | 0.252 | 0.538 |
| pgvector | a4@default | w3_s0p5_neg | 3000 | 0.593 | 0.475 | 0.362 |
| pgvector | a4@default | w3_s0p5_none | 3000 | 0.878 | 0.094 | 0.642 |
| pgvector | a4@default | w3_s0p5_pos | 3000 | 0.909 | 0.058 | 0.717 |
| pgvector | a4@iterative | w3_s0p001_neg | 3000 | 0.981 | 0.020 | 0.978 |
| pgvector | a4@iterative | w3_s0p001_none | 3000 | 0.951 | 0.041 | 0.935 |
| pgvector | a4@iterative | w3_s0p001_pos | 3000 | 0.985 | 0.009 | 0.975 |
| pgvector | a4@iterative | w3_s0p01_neg | 3000 | 0.323 | 0.472 | 0.073 |
| pgvector | a4@iterative | w3_s0p01_none | 3000 | 0.665 | 0.026 | 0.207 |
| pgvector | a4@iterative | w3_s0p01_pos | 3000 | 0.767 | 0.013 | 0.267 |
| pgvector | a4@iterative | w3_s0p05_neg | 3000 | 0.618 | 0.031 | 0.196 |
| pgvector | a4@iterative | w3_s0p05_none | 3000 | 0.868 | 0.000 | 0.405 |
| pgvector | a4@iterative | w3_s0p05_pos | 3000 | 0.870 | 0.000 | 0.437 |
| pgvector | a4@iterative | w3_s0p2_neg | 3000 | 0.832 | 0.000 | 0.376 |
| pgvector | a4@iterative | w3_s0p2_none | 3000 | 0.876 | 0.000 | 0.478 |
| pgvector | a4@iterative | w3_s0p2_pos | 3000 | 0.919 | 0.000 | 0.662 |
| pgvector | a4@iterative | w3_s0p5_neg | 3000 | 0.880 | 0.000 | 0.532 |
| pgvector | a4@iterative | w3_s0p5_none | 3000 | 0.928 | 0.000 | 0.698 |
| pgvector | a4@iterative | w3_s0p5_pos | 3000 | 0.947 | 0.000 | 0.748 |
| pgvector | a5-rls@default | w3_s0p001_neg | 3000 | 0.977 | 0.023 | 0.977 |
| pgvector | a5-rls@default | w3_s0p001_none | 3000 | 0.930 | 0.070 | 0.930 |
| pgvector | a5-rls@default | w3_s0p001_pos | 3000 | 0.973 | 0.028 | 0.971 |
| pgvector | a5-rls@default | w3_s0p01_neg | 3000 | 0.003 | 1.000 | 0.000 |
| pgvector | a5-rls@default | w3_s0p01_none | 3000 | 0.061 | 0.976 | 0.017 |
| pgvector | a5-rls@default | w3_s0p01_pos | 3000 | 0.162 | 0.903 | 0.051 |
| pgvector | a5-rls@default | w3_s0p05_neg | 3000 | 0.030 | 0.990 | 0.007 |
| pgvector | a5-rls@default | w3_s0p05_none | 3000 | 0.254 | 0.856 | 0.099 |
| pgvector | a5-rls@default | w3_s0p05_pos | 3000 | 0.444 | 0.628 | 0.210 |
| pgvector | a5-rls@default | w3_s0p2_neg | 3000 | 0.206 | 0.874 | 0.086 |
| pgvector | a5-rls@default | w3_s0p2_none | 3000 | 0.620 | 0.456 | 0.292 |
| pgvector | a5-rls@default | w3_s0p2_pos | 3000 | 0.757 | 0.252 | 0.538 |
| pgvector | a5-rls@default | w3_s0p5_neg | 3000 | 0.593 | 0.475 | 0.362 |
| pgvector | a5-rls@default | w3_s0p5_none | 3000 | 0.878 | 0.094 | 0.642 |
| pgvector | a5-rls@default | w3_s0p5_pos | 3000 | 0.909 | 0.058 | 0.717 |
| pgvector | a5-rls@iterative | w3_s0p001_neg | 3000 | 0.981 | 0.020 | 0.978 |
| pgvector | a5-rls@iterative | w3_s0p001_none | 3000 | 0.951 | 0.041 | 0.935 |
| pgvector | a5-rls@iterative | w3_s0p001_pos | 3000 | 0.985 | 0.009 | 0.975 |
| pgvector | a5-rls@iterative | w3_s0p01_neg | 3000 | 0.323 | 0.472 | 0.073 |
| pgvector | a5-rls@iterative | w3_s0p01_none | 3000 | 0.665 | 0.026 | 0.207 |
| pgvector | a5-rls@iterative | w3_s0p01_pos | 3000 | 0.767 | 0.013 | 0.267 |
| pgvector | a5-rls@iterative | w3_s0p05_neg | 3000 | 0.618 | 0.031 | 0.196 |
| pgvector | a5-rls@iterative | w3_s0p05_none | 3000 | 0.868 | 0.000 | 0.405 |
| pgvector | a5-rls@iterative | w3_s0p05_pos | 3000 | 0.870 | 0.000 | 0.437 |
| pgvector | a5-rls@iterative | w3_s0p2_neg | 3000 | 0.832 | 0.000 | 0.376 |
| pgvector | a5-rls@iterative | w3_s0p2_none | 3000 | 0.876 | 0.000 | 0.478 |
| pgvector | a5-rls@iterative | w3_s0p2_pos | 3000 | 0.919 | 0.000 | 0.662 |
| pgvector | a5-rls@iterative | w3_s0p5_neg | 3000 | 0.880 | 0.000 | 0.532 |
| pgvector | a5-rls@iterative | w3_s0p5_none | 3000 | 0.928 | 0.000 | 0.698 |
| pgvector | a5-rls@iterative | w3_s0p5_pos | 3000 | 0.947 | 0.000 | 0.748 |
| pgvector | a7-wardowl | w3_s0p001_neg | 3000 | 0.006 | 0.999 | 0.001 |
| pgvector | a7-wardowl | w3_s0p001_none | 3000 | 0.047 | 0.976 | 0.013 |
| pgvector | a7-wardowl | w3_s0p001_pos | 3000 | 0.138 | 0.917 | 0.034 |
| pgvector | a7-wardowl | w3_s0p01_neg | 3000 | 0.057 | 0.979 | 0.015 |
| pgvector | a7-wardowl | w3_s0p01_none | 3000 | 0.295 | 0.818 | 0.117 |
| pgvector | a7-wardowl | w3_s0p01_pos | 3000 | 0.511 | 0.563 | 0.214 |
| pgvector | a7-wardowl | w3_s0p05_neg | 3000 | 0.253 | 0.861 | 0.098 |
| pgvector | a7-wardowl | w3_s0p05_none | 3000 | 0.755 | 0.293 | 0.404 |
| pgvector | a7-wardowl | w3_s0p05_pos | 3000 | 0.801 | 0.183 | 0.462 |
| pgvector | a7-wardowl | w3_s0p2_neg | 3000 | 0.730 | 0.326 | 0.392 |
| pgvector | a7-wardowl | w3_s0p2_none | 3000 | 0.916 | 0.016 | 0.609 |
| pgvector | a7-wardowl | w3_s0p2_pos | 3000 | 0.919 | 0.038 | 0.695 |
| pgvector | a7-wardowl | w3_s0p5_neg | 3000 | 0.903 | 0.049 | 0.637 |
| pgvector | a7-wardowl | w3_s0p5_none | 3000 | 0.938 | 0.000 | 0.738 |
| pgvector | a7-wardowl | w3_s0p5_pos | 3000 | 0.949 | 0.005 | 0.771 |
| qdrant | a3-spicedb@acorn | w3_s0p001_neg | 3000 | 1.000 | 0.000 | 1.000 |
| qdrant | a3-spicedb@acorn | w3_s0p001_none | 3000 | 1.000 | 0.000 | 1.000 |
| qdrant | a3-spicedb@acorn | w3_s0p001_pos | 3000 | 1.000 | 0.000 | 1.000 |
| qdrant | a3-spicedb@acorn | w3_s0p01_neg | 3000 | 0.936 | 0.000 | 0.878 |
| qdrant | a3-spicedb@acorn | w3_s0p01_none | 3000 | 0.981 | 0.000 | 0.917 |
| qdrant | a3-spicedb@acorn | w3_s0p01_pos | 3000 | 0.991 | 0.000 | 0.941 |
| qdrant | a3-spicedb@acorn | w3_s0p05_neg | 900 | 0.660 | 0.000 | 0.273 |
| qdrant | a3-spicedb@acorn | w3_s0p05_none | 900 | 0.923 | 0.000 | 0.614 |
| qdrant | a3-spicedb@acorn | w3_s0p05_pos | 900 | 0.966 | 0.000 | 0.784 |
| qdrant | a3-spicedb@acorn | w3_s0p2_neg | 300 | 0.855 | 0.000 | 0.497 |
| qdrant | a3-spicedb@acorn | w3_s0p2_none | 300 | 0.965 | 0.000 | 0.777 |
| qdrant | a3-spicedb@acorn | w3_s0p2_pos | 300 | 0.973 | 0.000 | 0.827 |
| qdrant | a3-spicedb@acorn | w3_s0p5_neg | 150 | 0.717 | 0.000 | 0.313 |
| qdrant | a3-spicedb@acorn | w3_s0p5_none | 150 | 0.915 | 0.000 | 0.607 |
| qdrant | a3-spicedb@acorn | w3_s0p5_pos | 150 | 0.936 | 0.000 | 0.720 |
| qdrant | a3-spicedb@default | w3_s0p001_neg | 3000 | 1.000 | 0.000 | 1.000 |
| qdrant | a3-spicedb@default | w3_s0p001_none | 3000 | 1.000 | 0.000 | 1.000 |
| qdrant | a3-spicedb@default | w3_s0p001_pos | 3000 | 1.000 | 0.000 | 1.000 |
| qdrant | a3-spicedb@default | w3_s0p01_neg | 3000 | 0.914 | 0.000 | 0.858 |
| qdrant | a3-spicedb@default | w3_s0p01_none | 3000 | 0.913 | 0.000 | 0.822 |
| qdrant | a3-spicedb@default | w3_s0p01_pos | 3000 | 0.940 | 0.000 | 0.789 |
| qdrant | a3-spicedb@default | w3_s0p05_neg | 900 | 0.182 | 0.000 | 0.021 |
| qdrant | a3-spicedb@default | w3_s0p05_none | 900 | 0.562 | 0.000 | 0.148 |
| qdrant | a3-spicedb@default | w3_s0p05_pos | 900 | 0.770 | 0.000 | 0.318 |
| qdrant | a3-spicedb@default | w3_s0p2_neg | 300 | 0.485 | 0.000 | 0.133 |
| qdrant | a3-spicedb@default | w3_s0p2_none | 300 | 0.765 | 0.000 | 0.310 |
| qdrant | a3-spicedb@default | w3_s0p2_pos | 300 | 0.899 | 0.000 | 0.563 |
| qdrant | a3-spicedb@default | w3_s0p5_neg | 150 | 0.717 | 0.000 | 0.313 |
| qdrant | a3-spicedb@default | w3_s0p5_none | 150 | 0.915 | 0.000 | 0.607 |
| qdrant | a3-spicedb@default | w3_s0p5_pos | 150 | 0.936 | 0.000 | 0.720 |
| qdrant | a4@acorn | w3_s0p001_neg | 3000 | 1.000 | 0.000 | 1.000 |
| qdrant | a4@acorn | w3_s0p001_none | 3000 | 1.000 | 0.000 | 1.000 |
| qdrant | a4@acorn | w3_s0p001_pos | 3000 | 1.000 | 0.000 | 1.000 |
| qdrant | a4@acorn | w3_s0p01_neg | 3000 | 0.937 | 0.000 | 0.880 |
| qdrant | a4@acorn | w3_s0p01_none | 3000 | 0.986 | 0.000 | 0.938 |
| qdrant | a4@acorn | w3_s0p01_pos | 3000 | 0.992 | 0.000 | 0.943 |
| qdrant | a4@acorn | w3_s0p05_neg | 3000 | 0.665 | 0.000 | 0.276 |
| qdrant | a4@acorn | w3_s0p05_none | 3000 | 0.923 | 0.000 | 0.626 |
| qdrant | a4@acorn | w3_s0p05_pos | 3000 | 0.967 | 0.000 | 0.779 |
| qdrant | a4@acorn | w3_s0p2_neg | 3000 | 0.853 | 0.000 | 0.479 |
| qdrant | a4@acorn | w3_s0p2_none | 3000 | 0.962 | 0.000 | 0.767 |
| qdrant | a4@acorn | w3_s0p2_pos | 3000 | 0.977 | 0.000 | 0.845 |
| qdrant | a4@acorn | w3_s0p5_neg | 3000 | 0.935 | 0.000 | 0.690 |
| qdrant | a4@acorn | w3_s0p5_none | 3000 | 0.974 | 0.000 | 0.842 |
| qdrant | a4@acorn | w3_s0p5_pos | 3000 | 0.969 | 0.000 | 0.835 |
| qdrant | a4@default | w3_s0p001_neg | 3000 | 1.000 | 0.000 | 1.000 |
| qdrant | a4@default | w3_s0p001_none | 3000 | 1.000 | 0.000 | 1.000 |
| qdrant | a4@default | w3_s0p001_pos | 3000 | 1.000 | 0.000 | 1.000 |
| qdrant | a4@default | w3_s0p01_neg | 3000 | 0.917 | 0.000 | 0.861 |
| qdrant | a4@default | w3_s0p01_none | 3000 | 0.933 | 0.000 | 0.865 |
| qdrant | a4@default | w3_s0p01_pos | 3000 | 0.942 | 0.000 | 0.797 |
| qdrant | a4@default | w3_s0p05_neg | 3000 | 0.200 | 0.000 | 0.027 |
| qdrant | a4@default | w3_s0p05_none | 3000 | 0.555 | 0.000 | 0.138 |
| qdrant | a4@default | w3_s0p05_pos | 3000 | 0.776 | 0.000 | 0.305 |
| qdrant | a4@default | w3_s0p2_neg | 3000 | 0.485 | 0.000 | 0.125 |
| qdrant | a4@default | w3_s0p2_none | 3000 | 0.752 | 0.000 | 0.303 |
| qdrant | a4@default | w3_s0p2_pos | 3000 | 0.895 | 0.000 | 0.565 |
| qdrant | a4@default | w3_s0p5_neg | 3000 | 0.722 | 0.000 | 0.336 |
| qdrant | a4@default | w3_s0p5_none | 3000 | 0.894 | 0.000 | 0.580 |
| qdrant | a4@default | w3_s0p5_pos | 3000 | 0.938 | 0.000 | 0.719 |
| qdrant | a7-wardowl | w3_s0p001_neg | 3000 | 0.006 | 0.999 | 0.001 |
| qdrant | a7-wardowl | w3_s0p001_none | 3000 | 0.047 | 0.977 | 0.015 |
| qdrant | a7-wardowl | w3_s0p001_pos | 3000 | 0.140 | 0.917 | 0.037 |
| qdrant | a7-wardowl | w3_s0p01_neg | 3000 | 0.054 | 0.982 | 0.013 |
| qdrant | a7-wardowl | w3_s0p01_none | 3000 | 0.294 | 0.821 | 0.113 |
| qdrant | a7-wardowl | w3_s0p01_pos | 3000 | 0.520 | 0.557 | 0.217 |
| qdrant | a7-wardowl | w3_s0p05_neg | 3000 | 0.252 | 0.859 | 0.087 |
| qdrant | a7-wardowl | w3_s0p05_none | 3000 | 0.752 | 0.288 | 0.392 |
| qdrant | a7-wardowl | w3_s0p05_pos | 3000 | 0.799 | 0.183 | 0.490 |
| qdrant | a7-wardowl | w3_s0p2_neg | 3000 | 0.717 | 0.331 | 0.340 |
| qdrant | a7-wardowl | w3_s0p2_none | 3000 | 0.915 | 0.017 | 0.603 |
| qdrant | a7-wardowl | w3_s0p2_pos | 3000 | 0.930 | 0.039 | 0.714 |
| qdrant | a7-wardowl | w3_s0p5_neg | 3000 | 0.891 | 0.049 | 0.599 |
| qdrant | a7-wardowl | w3_s0p5_none | 3000 | 0.944 | 0.000 | 0.737 |
| qdrant | a7-wardowl | w3_s0p5_pos | 3000 | 0.953 | 0.005 | 0.781 |
| weaviate | a3-spicedb@default | w3_s0p001_neg | 3000 | 1.000 | 0.000 | 1.000 |
| weaviate | a3-spicedb@default | w3_s0p001_none | 3000 | 1.000 | 0.000 | 1.000 |
| weaviate | a3-spicedb@default | w3_s0p001_pos | 3000 | 1.000 | 0.000 | 1.000 |
| weaviate | a3-spicedb@default | w3_s0p01_neg | 3000 | 1.000 | 0.000 | 1.000 |
| weaviate | a3-spicedb@default | w3_s0p01_none | 3000 | 1.000 | 0.000 | 1.000 |
| weaviate | a3-spicedb@default | w3_s0p01_pos | 3000 | 1.000 | 0.000 | 1.000 |
| weaviate | a3-spicedb@default | w3_s0p05_neg | 900 | 0.547 | 0.000 | 0.198 |
| weaviate | a3-spicedb@default | w3_s0p05_none | 900 | 0.823 | 0.000 | 0.369 |
| weaviate | a3-spicedb@default | w3_s0p05_pos | 900 | 0.888 | 0.000 | 0.477 |
| weaviate | a3-spicedb@default | w3_s0p2_neg | 300 | 0.738 | 0.000 | 0.290 |
| weaviate | a3-spicedb@default | w3_s0p2_none | 300 | 0.872 | 0.000 | 0.457 |
| weaviate | a3-spicedb@default | w3_s0p2_pos | 300 | 0.914 | 0.000 | 0.583 |
| weaviate | a3-spicedb@default | w3_s0p5_neg | 150 | 0.944 | 0.000 | 0.753 |
| weaviate | a3-spicedb@default | w3_s0p5_none | 150 | 0.960 | 0.000 | 0.800 |
| weaviate | a3-spicedb@default | w3_s0p5_pos | 150 | 0.961 | 0.000 | 0.780 |
| weaviate | a3-spicedb@pathseer | w3_s0p001_neg | 3000 | 1.000 | 0.000 | 1.000 |
| weaviate | a3-spicedb@pathseer | w3_s0p001_none | 3000 | 1.000 | 0.000 | 1.000 |
| weaviate | a3-spicedb@pathseer | w3_s0p001_pos | 3000 | 1.000 | 0.000 | 1.000 |
| weaviate | a3-spicedb@pathseer | w3_s0p01_neg | 3000 | 1.000 | 0.000 | 1.000 |
| weaviate | a3-spicedb@pathseer | w3_s0p01_none | 3000 | 1.000 | 0.000 | 1.000 |
| weaviate | a3-spicedb@pathseer | w3_s0p01_pos | 3000 | 1.000 | 0.000 | 1.000 |
| weaviate | a3-spicedb@pathseer | w3_s0p05_neg | 900 | 0.913 | 0.000 | 0.548 |
| weaviate | a3-spicedb@pathseer | w3_s0p05_none | 900 | 0.913 | 0.000 | 0.579 |
| weaviate | a3-spicedb@pathseer | w3_s0p05_pos | 900 | 0.927 | 0.000 | 0.631 |
| weaviate | a3-spicedb@pathseer | w3_s0p2_neg | 300 | 0.887 | 0.000 | 0.513 |
| weaviate | a3-spicedb@pathseer | w3_s0p2_none | 300 | 0.909 | 0.000 | 0.583 |
| weaviate | a3-spicedb@pathseer | w3_s0p2_pos | 300 | 0.944 | 0.000 | 0.720 |
| weaviate | a3-spicedb@pathseer | w3_s0p5_neg | 150 | 0.871 | 0.000 | 0.567 |
| weaviate | a3-spicedb@pathseer | w3_s0p5_none | 150 | 0.946 | 0.000 | 0.760 |
| weaviate | a3-spicedb@pathseer | w3_s0p5_pos | 150 | 0.960 | 0.000 | 0.760 |
| weaviate | a4@default | w3_s0p001_neg | 3000 | 1.000 | 0.000 | 1.000 |
| weaviate | a4@default | w3_s0p001_none | 3000 | 1.000 | 0.000 | 1.000 |
| weaviate | a4@default | w3_s0p001_pos | 3000 | 1.000 | 0.000 | 1.000 |
| weaviate | a4@default | w3_s0p01_neg | 3000 | 1.000 | 0.000 | 1.000 |
| weaviate | a4@default | w3_s0p01_none | 3000 | 1.000 | 0.000 | 1.000 |
| weaviate | a4@default | w3_s0p01_pos | 3000 | 1.000 | 0.000 | 1.000 |
| weaviate | a4@default | w3_s0p05_neg | 3000 | 0.565 | 0.000 | 0.209 |
| weaviate | a4@default | w3_s0p05_none | 3000 | 0.829 | 0.000 | 0.383 |
| weaviate | a4@default | w3_s0p05_pos | 3000 | 0.884 | 0.000 | 0.456 |
| weaviate | a4@default | w3_s0p2_neg | 3000 | 0.747 | 0.000 | 0.294 |
| weaviate | a4@default | w3_s0p2_none | 3000 | 0.873 | 0.000 | 0.483 |
| weaviate | a4@default | w3_s0p2_pos | 3000 | 0.912 | 0.000 | 0.604 |
| weaviate | a4@default | w3_s0p5_neg | 3000 | 0.953 | 0.000 | 0.743 |
| weaviate | a4@default | w3_s0p5_none | 3000 | 0.956 | 0.000 | 0.785 |
| weaviate | a4@default | w3_s0p5_pos | 3000 | 0.950 | 0.000 | 0.760 |
| weaviate | a4@pathseer | w3_s0p001_neg | 3000 | 1.000 | 0.000 | 1.000 |
| weaviate | a4@pathseer | w3_s0p001_none | 3000 | 1.000 | 0.000 | 1.000 |
| weaviate | a4@pathseer | w3_s0p001_pos | 3000 | 1.000 | 0.000 | 1.000 |
| weaviate | a4@pathseer | w3_s0p01_neg | 3000 | 1.000 | 0.000 | 1.000 |
| weaviate | a4@pathseer | w3_s0p01_none | 3000 | 1.000 | 0.000 | 1.000 |
| weaviate | a4@pathseer | w3_s0p01_pos | 3000 | 1.000 | 0.000 | 1.000 |
| weaviate | a4@pathseer | w3_s0p05_neg | 3000 | 0.907 | 0.000 | 0.541 |
| weaviate | a4@pathseer | w3_s0p05_none | 3000 | 0.917 | 0.000 | 0.597 |
| weaviate | a4@pathseer | w3_s0p05_pos | 3000 | 0.927 | 0.000 | 0.621 |
| weaviate | a4@pathseer | w3_s0p2_neg | 3000 | 0.883 | 0.000 | 0.506 |
| weaviate | a4@pathseer | w3_s0p2_none | 3000 | 0.911 | 0.000 | 0.603 |
| weaviate | a4@pathseer | w3_s0p2_pos | 3000 | 0.942 | 0.000 | 0.708 |
| weaviate | a4@pathseer | w3_s0p5_neg | 3000 | 0.900 | 0.000 | 0.599 |
| weaviate | a4@pathseer | w3_s0p5_none | 3000 | 0.938 | 0.000 | 0.734 |
| weaviate | a4@pathseer | w3_s0p5_pos | 3000 | 0.945 | 0.000 | 0.743 |

## W1 and W2, every arm

| workload | store | arm | queries | recall | empty | short | exact |
|---|---|---|---|---|---|---|---|
| w1_enron | milvus | a1-fga | 11955 | 0.128 | 7267 | 0.979 | 0.021 |
| w1_enron | milvus | a1-spicedb | 11955 | 0.128 | 7267 | 0.979 | 0.021 |
| w1_enron | milvus | a2-fga-x10 | 11955 | 0.229 | 6585 | 0.867 | 0.124 |
| w1_enron | milvus | a2-fga-x3 | 11955 | 0.183 | 6944 | 0.920 | 0.077 |
| w1_enron | milvus | a2-spicedb-x10 | 11955 | 0.229 | 6585 | 0.867 | 0.124 |
| w1_enron | milvus | a2-spicedb-x3 | 11955 | 0.183 | 6944 | 0.920 | 0.077 |
| w1_enron | milvus | a3-spicedb@default | 11955 | 1.000 | 0 | 0.000 | 1.000 |
| w1_enron | milvus | a3-spicedb@iterative | 11955 | 0.962 | 0 | 0.000 | 0.721 |
| w1_enron | milvus | a4@default | 11955 | 1.000 | 0 | 0.000 | 1.000 |
| w1_enron | milvus | a4@iterative | 11955 | 0.962 | 0 | 0.000 | 0.721 |
| w1_enron | opensearch | a1-fga | 11955 | 0.134 | 6841 | 0.980 | 0.020 |
| w1_enron | opensearch | a1-spicedb | 11955 | 0.134 | 6841 | 0.980 | 0.020 |
| w1_enron | opensearch | a2-fga-x10 | 11955 | 0.237 | 6156 | 0.869 | 0.127 |
| w1_enron | opensearch | a2-fga-x3 | 11955 | 0.190 | 6507 | 0.920 | 0.078 |
| w1_enron | opensearch | a2-spicedb-x10 | 11955 | 0.237 | 6156 | 0.869 | 0.127 |
| w1_enron | opensearch | a2-spicedb-x3 | 11955 | 0.190 | 6507 | 0.920 | 0.078 |
| w1_enron | opensearch | a3-spicedb@default | 11955 | 1.000 | 0 | 0.000 | 1.000 |
| w1_enron | opensearch | a4@default | 11955 | 1.000 | 0 | 0.000 | 1.000 |
| w1_enron | opensearch | a5-dls | 11955 | 0.209 | 5795 | 0.916 | 0.060 |
| w1_enron | pgvector | a0 | 600 | 1.000 | 0 | 0.000 | 1.000 |
| w1_enron | pgvector | a1-fga | 11955 | 0.131 | 7046 | 0.980 | 0.020 |
| w1_enron | pgvector | a1-spicedb | 11955 | 0.131 | 7046 | 0.980 | 0.020 |
| w1_enron | pgvector | a2-fga-x10 | 11955 | 0.234 | 6435 | 0.868 | 0.126 |
| w1_enron | pgvector | a2-fga-x3 | 11955 | 0.187 | 6724 | 0.921 | 0.076 |
| w1_enron | pgvector | a2-spicedb-x10 | 11955 | 0.234 | 6435 | 0.868 | 0.126 |
| w1_enron | pgvector | a2-spicedb-x3 | 11955 | 0.187 | 6724 | 0.921 | 0.076 |
| w1_enron | pgvector | a3-spicedb@default | 11955 | 1.000 | 0 | 0.000 | 1.000 |
| w1_enron | pgvector | a3-spicedb@iterative | 11955 | 1.000 | 0 | 0.000 | 1.000 |
| w1_enron | pgvector | a4@default | 11955 | 0.984 | 135 | 0.019 | 0.981 |
| w1_enron | pgvector | a4@iterative | 11955 | 0.996 | 0 | 0.000 | 0.986 |
| w1_enron | pgvector | a5-rls@default | 11955 | 0.984 | 135 | 0.019 | 0.981 |
| w1_enron | pgvector | a5-rls@iterative | 11955 | 0.996 | 0 | 0.000 | 0.986 |
| w1_enron | pgvector | a6-partition | 11955 | 1.000 | 0 | 0.000 | 1.000 |
| w1_enron | pgvector | a7-wardowl | 11955 | 0.635 | 550 | 0.339 | 0.318 |
| w1_enron | qdrant | a1-fga | 11955 | 0.128 | 7177 | 0.980 | 0.020 |
| w1_enron | qdrant | a1-spicedb | 11955 | 0.128 | 7177 | 0.980 | 0.020 |
| w1_enron | qdrant | a2-fga-x10 | 11955 | 0.230 | 6522 | 0.868 | 0.124 |
| w1_enron | qdrant | a2-fga-x3 | 11955 | 0.183 | 6865 | 0.922 | 0.076 |
| w1_enron | qdrant | a2-spicedb-x10 | 11955 | 0.230 | 6522 | 0.868 | 0.124 |
| w1_enron | qdrant | a2-spicedb-x3 | 11955 | 0.183 | 6865 | 0.922 | 0.076 |
| w1_enron | qdrant | a3-spicedb@acorn | 11955 | 1.000 | 0 | 0.000 | 1.000 |
| w1_enron | qdrant | a3-spicedb@default | 11955 | 1.000 | 0 | 0.000 | 1.000 |
| w1_enron | qdrant | a4@acorn | 11955 | 1.000 | 0 | 0.000 | 1.000 |
| w1_enron | qdrant | a4@default | 11955 | 1.000 | 0 | 0.000 | 1.000 |
| w1_enron | qdrant | a7-wardowl | 11955 | 0.986 | 50 | 0.017 | 0.976 |
| w1_enron | weaviate | a1-fga | 11955 | 0.127 | 7233 | 0.980 | 0.019 |
| w1_enron | weaviate | a1-spicedb | 11955 | 0.127 | 7233 | 0.980 | 0.019 |
| w1_enron | weaviate | a2-fga-x10 | 11955 | 0.227 | 6630 | 0.871 | 0.119 |
| w1_enron | weaviate | a2-fga-x3 | 11955 | 0.181 | 6940 | 0.923 | 0.073 |
| w1_enron | weaviate | a2-spicedb-x10 | 11955 | 0.227 | 6630 | 0.871 | 0.119 |
| w1_enron | weaviate | a2-spicedb-x3 | 11955 | 0.181 | 6940 | 0.923 | 0.073 |
| w1_enron | weaviate | a3-spicedb@default | 11955 | 1.000 | 0 | 0.000 | 1.000 |
| w1_enron | weaviate | a3-spicedb@pathseer | 11955 | 1.000 | 0 | 0.000 | 1.000 |
| w1_enron | weaviate | a4@default | 11955 | 1.000 | 0 | 0.000 | 1.000 |
| w1_enron | weaviate | a4@pathseer | 11955 | 1.000 | 0 | 0.000 | 1.000 |
| w2_erbac_a | milvus | a1-fga | 3000 | 0.074 | 1559 | 1.000 | 0.000 |
| w2_erbac_a | milvus | a1-spicedb | 3000 | 0.073 | 1564 | 1.000 | 0.000 |
| w2_erbac_a | milvus | a2-fga-x10 | 3000 | 0.627 | 190 | 0.633 | 0.202 |
| w2_erbac_a | milvus | a2-fga-x3 | 3000 | 0.231 | 569 | 0.998 | 0.002 |
| w2_erbac_a | milvus | a2-spicedb-x10 | 3000 | 0.635 | 193 | 0.636 | 0.233 |
| w2_erbac_a | milvus | a2-spicedb-x3 | 3000 | 0.231 | 569 | 0.998 | 0.002 |
| w2_erbac_a | milvus | a3-spicedb@default | 3000 | 0.986 | 0 | 0.000 | 0.894 |
| w2_erbac_a | milvus | a3-spicedb@iterative | 3000 | 0.953 | 0 | 0.000 | 0.705 |
| w2_erbac_a | milvus | a4@default | 3000 | 0.986 | 0 | 0.000 | 0.894 |
| w2_erbac_a | milvus | a4@iterative | 3000 | 0.964 | 0 | 0.000 | 0.763 |
| w2_erbac_a | opensearch | a1-fga | 3000 | 0.073 | 1563 | 1.000 | 0.000 |
| w2_erbac_a | opensearch | a1-spicedb | 3000 | 0.073 | 1563 | 1.000 | 0.000 |
| w2_erbac_a | opensearch | a2-fga-x10 | 3000 | 0.651 | 205 | 0.639 | 0.297 |
| w2_erbac_a | opensearch | a2-fga-x3 | 3000 | 0.231 | 557 | 0.997 | 0.003 |
| w2_erbac_a | opensearch | a2-spicedb-x10 | 3000 | 0.651 | 205 | 0.639 | 0.297 |
| w2_erbac_a | opensearch | a2-spicedb-x3 | 3000 | 0.231 | 557 | 0.997 | 0.003 |
| w2_erbac_a | opensearch | a3-spicedb@default | 3000 | 0.992 | 0 | 0.000 | 0.942 |
| w2_erbac_a | opensearch | a4@default | 3000 | 0.992 | 0 | 0.000 | 0.942 |
| w2_erbac_a | opensearch | a5-dls | 3000 | 0.418 | 129 | 0.341 | 0.003 |
| w2_erbac_a | pgvector | a0 | 300 | 1.000 | 0 | 0.000 | 1.000 |
| w2_erbac_a | pgvector | a1-fga | 3000 | 0.073 | 1569 | 1.000 | 0.000 |
| w2_erbac_a | pgvector | a1-spicedb | 3000 | 0.073 | 1569 | 1.000 | 0.000 |
| w2_erbac_a | pgvector | a2-fga-x10 | 3000 | 0.633 | 202 | 0.635 | 0.222 |
| w2_erbac_a | pgvector | a2-fga-x3 | 3000 | 0.230 | 574 | 0.998 | 0.002 |
| w2_erbac_a | pgvector | a2-spicedb-x10 | 3000 | 0.633 | 202 | 0.635 | 0.222 |
| w2_erbac_a | pgvector | a2-spicedb-x3 | 3000 | 0.230 | 574 | 0.998 | 0.002 |
| w2_erbac_a | pgvector | a3-spicedb@default | 3000 | 0.752 | 7 | 0.505 | 0.352 |
| w2_erbac_a | pgvector | a3-spicedb@iterative | 3000 | 0.946 | 0 | 0.000 | 0.690 |
| w2_erbac_a | pgvector | a4@default | 3000 | 0.673 | 100 | 0.595 | 0.262 |
| w2_erbac_a | pgvector | a4@iterative | 3000 | 0.943 | 0 | 0.000 | 0.665 |
| w2_erbac_a | pgvector | a5-rls@default | 3000 | 0.673 | 100 | 0.595 | 0.262 |
| w2_erbac_a | pgvector | a5-rls@iterative | 3000 | 0.943 | 0 | 0.000 | 0.665 |
| w2_erbac_a | pgvector | a6-partition | 3000 | 0.998 | 0 | 0.000 | 0.977 |
| w2_erbac_a | pgvector | a7-wardowl | 3000 | 0.953 | 0 | 0.029 | 0.759 |
| w2_erbac_a | qdrant | a1-fga | 3000 | 0.074 | 1564 | 1.000 | 0.000 |
| w2_erbac_a | qdrant | a1-spicedb | 3000 | 0.074 | 1564 | 1.000 | 0.000 |
| w2_erbac_a | qdrant | a2-fga-x10 | 3000 | 0.629 | 195 | 0.639 | 0.215 |
| w2_erbac_a | qdrant | a2-fga-x3 | 3000 | 0.231 | 568 | 0.998 | 0.002 |
| w2_erbac_a | qdrant | a2-spicedb-x10 | 3000 | 0.629 | 195 | 0.639 | 0.215 |
| w2_erbac_a | qdrant | a2-spicedb-x3 | 3000 | 0.231 | 568 | 0.998 | 0.002 |
| w2_erbac_a | qdrant | a3-spicedb@acorn | 3000 | 0.990 | 0 | 0.000 | 0.922 |
| w2_erbac_a | qdrant | a3-spicedb@default | 3000 | 0.693 | 0 | 0.053 | 0.265 |
| w2_erbac_a | qdrant | a4@acorn | 3000 | 0.990 | 0 | 0.000 | 0.923 |
| w2_erbac_a | qdrant | a4@default | 3000 | 0.703 | 0 | 0.046 | 0.275 |
| w2_erbac_a | qdrant | a7-wardowl | 3000 | 0.952 | 0 | 0.028 | 0.745 |
| w2_erbac_a | weaviate | a1-fga | 3000 | 0.074 | 1565 | 1.000 | 0.000 |
| w2_erbac_a | weaviate | a1-spicedb | 3000 | 0.074 | 1565 | 1.000 | 0.000 |
| w2_erbac_a | weaviate | a2-fga-x10 | 3000 | 0.622 | 204 | 0.635 | 0.202 |
| w2_erbac_a | weaviate | a2-fga-x3 | 3000 | 0.230 | 575 | 0.998 | 0.002 |
| w2_erbac_a | weaviate | a2-spicedb-x10 | 3000 | 0.622 | 204 | 0.635 | 0.202 |
| w2_erbac_a | weaviate | a2-spicedb-x3 | 3000 | 0.230 | 575 | 0.998 | 0.002 |
| w2_erbac_a | weaviate | a3-spicedb@default | 3000 | 1.000 | 0 | 0.000 | 1.000 |
| w2_erbac_a | weaviate | a3-spicedb@pathseer | 3000 | 1.000 | 0 | 0.000 | 1.000 |
| w2_erbac_a | weaviate | a4@default | 3000 | 1.000 | 0 | 0.000 | 1.000 |
| w2_erbac_a | weaviate | a4@pathseer | 3000 | 1.000 | 0 | 0.000 | 1.000 |
| w2_erbac_b | milvus | a1-fga | 3000 | 0.151 | 778 | 1.000 | 0.000 |
| w2_erbac_b | milvus | a1-spicedb | 3000 | 0.150 | 781 | 1.000 | 0.000 |
| w2_erbac_b | milvus | a2-fga-x10 | 3000 | 0.806 | 27 | 0.296 | 0.446 |
| w2_erbac_b | milvus | a2-fga-x3 | 3000 | 0.446 | 180 | 0.935 | 0.052 |
| w2_erbac_b | milvus | a2-spicedb-x10 | 3000 | 0.822 | 21 | 0.296 | 0.511 |
| w2_erbac_b | milvus | a2-spicedb-x3 | 3000 | 0.446 | 180 | 0.935 | 0.052 |
| w2_erbac_b | milvus | a3-spicedb@default | 3000 | 0.975 | 0 | 0.000 | 0.833 |
| w2_erbac_b | milvus | a3-spicedb@iterative | 3000 | 0.957 | 0 | 0.000 | 0.738 |
| w2_erbac_b | milvus | a4@default | 3000 | 0.975 | 0 | 0.000 | 0.833 |
| w2_erbac_b | milvus | a4@iterative | 3000 | 0.965 | 0 | 0.000 | 0.779 |
| w2_erbac_b | opensearch | a1-fga | 3000 | 0.150 | 792 | 1.000 | 0.000 |
| w2_erbac_b | opensearch | a1-spicedb | 3000 | 0.149 | 792 | 1.000 | 0.000 |
| w2_erbac_b | opensearch | a2-fga-x10 | 3000 | 0.848 | 18 | 0.295 | 0.627 |
| w2_erbac_b | opensearch | a2-fga-x3 | 3000 | 0.449 | 175 | 0.934 | 0.058 |
| w2_erbac_b | opensearch | a2-spicedb-x10 | 3000 | 0.848 | 18 | 0.295 | 0.627 |
| w2_erbac_b | opensearch | a2-spicedb-x3 | 3000 | 0.449 | 175 | 0.934 | 0.058 |
| w2_erbac_b | opensearch | a3-spicedb@default | 3000 | 0.990 | 0 | 0.000 | 0.921 |
| w2_erbac_b | opensearch | a4@default | 3000 | 0.990 | 0 | 0.000 | 0.921 |
| w2_erbac_b | opensearch | a5-dls | 3000 | 0.519 | 3 | 0.152 | 0.006 |
| w2_erbac_b | pgvector | a0 | 300 | 1.000 | 0 | 0.000 | 1.000 |
| w2_erbac_b | pgvector | a1-fga | 3000 | 0.148 | 809 | 1.000 | 0.000 |
| w2_erbac_b | pgvector | a1-spicedb | 3000 | 0.148 | 809 | 1.000 | 0.000 |
| w2_erbac_b | pgvector | a2-fga-x10 | 3000 | 0.813 | 18 | 0.297 | 0.484 |
| w2_erbac_b | pgvector | a2-fga-x3 | 3000 | 0.446 | 178 | 0.935 | 0.055 |
| w2_erbac_b | pgvector | a2-spicedb-x10 | 3000 | 0.813 | 18 | 0.297 | 0.484 |
| w2_erbac_b | pgvector | a2-spicedb-x3 | 3000 | 0.446 | 178 | 0.935 | 0.055 |
| w2_erbac_b | pgvector | a3-spicedb@default | 3000 | 0.837 | 6 | 0.267 | 0.514 |
| w2_erbac_b | pgvector | a3-spicedb@iterative | 3000 | 0.944 | 0 | 0.000 | 0.697 |
| w2_erbac_b | pgvector | a4@default | 3000 | 0.813 | 18 | 0.297 | 0.484 |
| w2_erbac_b | pgvector | a4@iterative | 3000 | 0.943 | 0 | 0.000 | 0.688 |
| w2_erbac_b | pgvector | a5-rls@default | 3000 | 0.813 | 18 | 0.297 | 0.484 |
| w2_erbac_b | pgvector | a5-rls@iterative | 3000 | 0.943 | 0 | 0.000 | 0.688 |
| w2_erbac_b | pgvector | a6-partition | 3000 | 0.999 | 0 | 0.000 | 0.990 |
| w2_erbac_b | pgvector | a7-wardowl | 3000 | 0.963 | 0 | 0.007 | 0.797 |
| w2_erbac_b | qdrant | a1-fga | 3000 | 0.150 | 791 | 1.000 | 0.000 |
| w2_erbac_b | qdrant | a1-spicedb | 3000 | 0.150 | 791 | 1.000 | 0.000 |
| w2_erbac_b | qdrant | a2-fga-x10 | 3000 | 0.811 | 30 | 0.293 | 0.465 |
| w2_erbac_b | qdrant | a2-fga-x3 | 3000 | 0.445 | 187 | 0.933 | 0.051 |
| w2_erbac_b | qdrant | a2-spicedb-x10 | 3000 | 0.811 | 30 | 0.293 | 0.465 |
| w2_erbac_b | qdrant | a2-spicedb-x3 | 3000 | 0.445 | 187 | 0.933 | 0.051 |
| w2_erbac_b | qdrant | a3-spicedb@acorn | 3000 | 0.991 | 0 | 0.000 | 0.928 |
| w2_erbac_b | qdrant | a3-spicedb@default | 3000 | 0.750 | 0 | 0.035 | 0.269 |
| w2_erbac_b | qdrant | a4@acorn | 3000 | 0.991 | 0 | 0.000 | 0.928 |
| w2_erbac_b | qdrant | a4@default | 3000 | 0.749 | 0 | 0.035 | 0.268 |
| w2_erbac_b | qdrant | a7-wardowl | 3000 | 0.958 | 0 | 0.007 | 0.770 |
| w2_erbac_b | weaviate | a1-fga | 3000 | 0.149 | 797 | 1.000 | 0.000 |
| w2_erbac_b | weaviate | a1-spicedb | 3000 | 0.149 | 797 | 1.000 | 0.000 |
| w2_erbac_b | weaviate | a2-fga-x10 | 3000 | 0.800 | 22 | 0.299 | 0.426 |
| w2_erbac_b | weaviate | a2-fga-x3 | 3000 | 0.446 | 187 | 0.934 | 0.051 |
| w2_erbac_b | weaviate | a2-spicedb-x10 | 3000 | 0.800 | 22 | 0.299 | 0.426 |
| w2_erbac_b | weaviate | a2-spicedb-x3 | 3000 | 0.446 | 187 | 0.934 | 0.051 |
| w2_erbac_b | weaviate | a3-spicedb@default | 3000 | 0.980 | 0 | 0.000 | 0.892 |
| w2_erbac_b | weaviate | a3-spicedb@pathseer | 3000 | 0.988 | 0 | 0.000 | 0.932 |
| w2_erbac_b | weaviate | a4@default | 3000 | 0.980 | 0 | 0.000 | 0.892 |
| w2_erbac_b | weaviate | a4@pathseer | 3000 | 0.988 | 0 | 0.000 | 0.932 |
| w2_tree_a | milvus | a1-fga | 3000 | 0.044 | 1958 | 1.000 | 0.000 |
| w2_tree_a | milvus | a1-spicedb | 3000 | 0.044 | 1967 | 1.000 | 0.000 |
| w2_tree_a | milvus | a2-fga-x10 | 3000 | 0.412 | 67 | 0.979 | 0.016 |
| w2_tree_a | milvus | a2-fga-x3 | 3000 | 0.124 | 901 | 1.000 | 0.000 |
| w2_tree_a | milvus | a2-spicedb-x10 | 3000 | 0.412 | 70 | 0.980 | 0.016 |
| w2_tree_a | milvus | a2-spicedb-x3 | 3000 | 0.124 | 901 | 1.000 | 0.000 |
| w2_tree_a | milvus | a3-spicedb@default | 3000 | 1.000 | 0 | 0.000 | 1.000 |
| w2_tree_a | milvus | a3-spicedb@iterative | 3000 | 0.955 | 0 | 0.000 | 0.688 |
| w2_tree_a | milvus | a4@default | 3000 | 1.000 | 0 | 0.000 | 1.000 |
| w2_tree_a | milvus | a4@iterative | 3000 | 0.962 | 0 | 0.000 | 0.723 |
| w2_tree_a | opensearch | a1-fga | 3000 | 0.043 | 1987 | 1.000 | 0.000 |
| w2_tree_a | opensearch | a1-spicedb | 3000 | 0.043 | 1987 | 1.000 | 0.000 |
| w2_tree_a | opensearch | a2-fga-x10 | 3000 | 0.413 | 66 | 0.983 | 0.016 |
| w2_tree_a | opensearch | a2-fga-x3 | 3000 | 0.124 | 883 | 1.000 | 0.000 |
| w2_tree_a | opensearch | a2-spicedb-x10 | 3000 | 0.413 | 66 | 0.983 | 0.016 |
| w2_tree_a | opensearch | a2-spicedb-x3 | 3000 | 0.124 | 883 | 1.000 | 0.000 |
| w2_tree_a | opensearch | a3-spicedb@default | 3000 | 1.000 | 0 | 0.000 | 1.000 |
| w2_tree_a | opensearch | a4@default | 3000 | 1.000 | 0 | 0.000 | 1.000 |
| w2_tree_a | opensearch | a5-dls | 3000 | 0.322 | 5 | 0.831 | 0.000 |
| w2_tree_a | pgvector | a0 | 300 | 1.000 | 0 | 0.000 | 1.000 |
| w2_tree_a | pgvector | a1-fga | 3000 | 0.043 | 1978 | 1.000 | 0.000 |
| w2_tree_a | pgvector | a1-spicedb | 3000 | 0.043 | 1978 | 1.000 | 0.000 |
| w2_tree_a | pgvector | a2-fga-x10 | 3000 | 0.413 | 65 | 0.982 | 0.013 |
| w2_tree_a | pgvector | a2-fga-x3 | 3000 | 0.124 | 900 | 1.000 | 0.000 |
| w2_tree_a | pgvector | a2-spicedb-x10 | 3000 | 0.413 | 65 | 0.982 | 0.013 |
| w2_tree_a | pgvector | a2-spicedb-x3 | 3000 | 0.124 | 900 | 1.000 | 0.000 |
| w2_tree_a | pgvector | a3-spicedb@default | 3000 | 0.438 | 56 | 0.952 | 0.043 |
| w2_tree_a | pgvector | a3-spicedb@iterative | 3000 | 0.952 | 0 | 0.000 | 0.674 |
| w2_tree_a | pgvector | a4@default | 3000 | 0.413 | 65 | 0.982 | 0.013 |
| w2_tree_a | pgvector | a4@iterative | 3000 | 0.951 | 0 | 0.000 | 0.665 |
| w2_tree_a | pgvector | a5-rls@default | 3000 | 0.413 | 65 | 0.982 | 0.013 |
| w2_tree_a | pgvector | a5-rls@iterative | 3000 | 0.951 | 0 | 0.000 | 0.665 |
| w2_tree_a | pgvector | a6-partition | 3000 | 1.000 | 0 | 0.000 | 1.000 |
| w2_tree_a | pgvector | a7-wardowl | 3000 | 0.982 | 0 | 0.001 | 0.861 |
| w2_tree_a | qdrant | a1-fga | 3000 | 0.044 | 1974 | 1.000 | 0.000 |
| w2_tree_a | qdrant | a1-spicedb | 3000 | 0.044 | 1974 | 1.000 | 0.000 |
| w2_tree_a | qdrant | a2-fga-x10 | 3000 | 0.413 | 64 | 0.982 | 0.013 |
| w2_tree_a | qdrant | a2-fga-x3 | 3000 | 0.124 | 899 | 1.000 | 0.000 |
| w2_tree_a | qdrant | a2-spicedb-x10 | 3000 | 0.413 | 64 | 0.982 | 0.013 |
| w2_tree_a | qdrant | a2-spicedb-x3 | 3000 | 0.124 | 899 | 1.000 | 0.000 |
| w2_tree_a | qdrant | a3-spicedb@acorn | 3000 | 0.964 | 0 | 0.000 | 0.746 |
| w2_tree_a | qdrant | a3-spicedb@default | 3000 | 0.153 | 0 | 0.651 | 0.150 |
| w2_tree_a | qdrant | a4@acorn | 3000 | 0.964 | 0 | 0.000 | 0.750 |
| w2_tree_a | qdrant | a4@default | 3000 | 0.163 | 0 | 0.641 | 0.160 |
| w2_tree_a | qdrant | a7-wardowl | 3000 | 0.975 | 0 | 0.000 | 0.810 |
| w2_tree_a | weaviate | a1-fga | 3000 | 0.044 | 1978 | 1.000 | 0.000 |
| w2_tree_a | weaviate | a1-spicedb | 3000 | 0.044 | 1978 | 1.000 | 0.000 |
| w2_tree_a | weaviate | a2-fga-x10 | 3000 | 0.414 | 60 | 0.984 | 0.011 |
| w2_tree_a | weaviate | a2-fga-x3 | 3000 | 0.125 | 903 | 1.000 | 0.000 |
| w2_tree_a | weaviate | a2-spicedb-x10 | 3000 | 0.414 | 60 | 0.984 | 0.011 |
| w2_tree_a | weaviate | a2-spicedb-x3 | 3000 | 0.125 | 903 | 1.000 | 0.000 |
| w2_tree_a | weaviate | a3-spicedb@default | 3000 | 1.000 | 0 | 0.000 | 1.000 |
| w2_tree_a | weaviate | a3-spicedb@pathseer | 3000 | 1.000 | 0 | 0.000 | 1.000 |
| w2_tree_a | weaviate | a4@default | 3000 | 1.000 | 0 | 0.000 | 1.000 |
| w2_tree_a | weaviate | a4@pathseer | 3000 | 1.000 | 0 | 0.000 | 1.000 |
| w2_uniform_a | milvus | a1-fga | 3000 | 0.036 | 2141 | 1.000 | 0.000 |
| w2_uniform_a | milvus | a1-spicedb | 3000 | 0.036 | 2143 | 1.000 | 0.000 |
| w2_uniform_a | milvus | a2-fga-x10 | 3000 | 0.383 | 359 | 0.959 | 0.028 |
| w2_uniform_a | milvus | a2-fga-x3 | 3000 | 0.120 | 1086 | 1.000 | 0.000 |
| w2_uniform_a | milvus | a2-spicedb-x10 | 3000 | 0.383 | 359 | 0.959 | 0.028 |
| w2_uniform_a | milvus | a2-spicedb-x3 | 3000 | 0.120 | 1086 | 1.000 | 0.000 |
| w2_uniform_a | milvus | a3-spicedb@default | 3000 | 0.998 | 0 | 0.000 | 0.983 |
| w2_uniform_a | milvus | a3-spicedb@iterative | 3000 | 0.954 | 0 | 0.000 | 0.666 |
| w2_uniform_a | milvus | a4@default | 3000 | 0.998 | 0 | 0.000 | 0.983 |
| w2_uniform_a | milvus | a4@iterative | 3000 | 0.954 | 0 | 0.000 | 0.666 |
| w2_uniform_a | opensearch | a1-fga | 3000 | 0.036 | 2140 | 1.000 | 0.000 |
| w2_uniform_a | opensearch | a1-spicedb | 3000 | 0.036 | 2140 | 1.000 | 0.000 |
| w2_uniform_a | opensearch | a2-fga-x10 | 3000 | 0.387 | 367 | 0.957 | 0.039 |
| w2_uniform_a | opensearch | a2-fga-x3 | 3000 | 0.120 | 1104 | 1.000 | 0.000 |
| w2_uniform_a | opensearch | a2-spicedb-x10 | 3000 | 0.387 | 367 | 0.957 | 0.039 |
| w2_uniform_a | opensearch | a2-spicedb-x3 | 3000 | 0.120 | 1104 | 1.000 | 0.000 |
| w2_uniform_a | opensearch | a3-spicedb@default | 3000 | 1.000 | 0 | 0.000 | 0.998 |
| w2_uniform_a | opensearch | a4@default | 3000 | 1.000 | 0 | 0.000 | 0.998 |
| w2_uniform_a | opensearch | a5-dls | 3000 | 0.282 | 200 | 0.766 | 0.000 |
| w2_uniform_a | pgvector | a0 | 300 | 1.000 | 0 | 0.000 | 1.000 |
| w2_uniform_a | pgvector | a1-fga | 3000 | 0.037 | 2120 | 1.000 | 0.000 |
| w2_uniform_a | pgvector | a1-spicedb | 3000 | 0.037 | 2120 | 1.000 | 0.000 |
| w2_uniform_a | pgvector | a2-fga-x10 | 3000 | 0.383 | 366 | 0.958 | 0.028 |
| w2_uniform_a | pgvector | a2-fga-x3 | 3000 | 0.119 | 1103 | 1.000 | 0.000 |
| w2_uniform_a | pgvector | a2-spicedb-x10 | 3000 | 0.383 | 366 | 0.958 | 0.028 |
| w2_uniform_a | pgvector | a2-spicedb-x3 | 3000 | 0.119 | 1103 | 1.000 | 0.000 |
| w2_uniform_a | pgvector | a3-spicedb@default | 3000 | 0.623 | 38 | 0.688 | 0.298 |
| w2_uniform_a | pgvector | a3-spicedb@iterative | 3000 | 0.958 | 0 | 0.000 | 0.726 |
| w2_uniform_a | pgvector | a4@default | 3000 | 0.429 | 247 | 0.911 | 0.074 |
| w2_uniform_a | pgvector | a4@iterative | 3000 | 0.952 | 0 | 0.000 | 0.676 |
| w2_uniform_a | pgvector | a5-rls@default | 3000 | 0.432 | 239 | 0.908 | 0.078 |
| w2_uniform_a | pgvector | a5-rls@iterative | 3000 | 0.952 | 0 | 0.000 | 0.676 |
| w2_uniform_a | pgvector | a6-partition | 3000 | 0.997 | 0 | 0.000 | 0.978 |
| w2_uniform_a | pgvector | a7-wardowl | 3000 | 0.950 | 0 | 0.073 | 0.744 |
| w2_uniform_a | qdrant | a1-fga | 3000 | 0.036 | 2129 | 1.000 | 0.000 |
| w2_uniform_a | qdrant | a1-spicedb | 3000 | 0.036 | 2129 | 1.000 | 0.000 |
| w2_uniform_a | qdrant | a2-fga-x10 | 3000 | 0.388 | 355 | 0.956 | 0.034 |
| w2_uniform_a | qdrant | a2-fga-x3 | 3000 | 0.120 | 1093 | 1.000 | 0.000 |
| w2_uniform_a | qdrant | a2-spicedb-x10 | 3000 | 0.388 | 355 | 0.956 | 0.034 |
| w2_uniform_a | qdrant | a2-spicedb-x3 | 3000 | 0.120 | 1093 | 1.000 | 0.000 |
| w2_uniform_a | qdrant | a3-spicedb@acorn | 3000 | 0.999 | 0 | 0.000 | 0.987 |
| w2_uniform_a | qdrant | a3-spicedb@default | 3000 | 0.871 | 0 | 0.023 | 0.679 |
| w2_uniform_a | qdrant | a4@acorn | 3000 | 0.999 | 0 | 0.000 | 0.987 |
| w2_uniform_a | qdrant | a4@default | 3000 | 0.871 | 0 | 0.023 | 0.679 |
| w2_uniform_a | qdrant | a7-wardowl | 3000 | 0.960 | 0 | 0.075 | 0.806 |
| w2_uniform_a | weaviate | a1-fga | 3000 | 0.037 | 2117 | 1.000 | 0.000 |
| w2_uniform_a | weaviate | a1-spicedb | 3000 | 0.037 | 2117 | 1.000 | 0.000 |
| w2_uniform_a | weaviate | a2-fga-x10 | 3000 | 0.383 | 360 | 0.963 | 0.026 |
| w2_uniform_a | weaviate | a2-fga-x3 | 3000 | 0.119 | 1105 | 1.000 | 0.000 |
| w2_uniform_a | weaviate | a2-spicedb-x10 | 3000 | 0.383 | 360 | 0.963 | 0.026 |
| w2_uniform_a | weaviate | a2-spicedb-x3 | 3000 | 0.119 | 1105 | 1.000 | 0.000 |
| w2_uniform_a | weaviate | a3-spicedb@default | 3000 | 1.000 | 0 | 0.000 | 1.000 |
| w2_uniform_a | weaviate | a3-spicedb@pathseer | 3000 | 1.000 | 0 | 0.000 | 1.000 |
| w2_uniform_a | weaviate | a4@default | 3000 | 1.000 | 0 | 0.000 | 1.000 |
| w2_uniform_a | weaviate | a4@pathseer | 3000 | 1.000 | 0 | 0.000 | 1.000 |

## The store filter's answers by how many chunks the user may read

Every workload pooled, per store and setting: answers whose user may read a number of chunks in the bin, how many were short and how many exact. Bins where every answer was exact are left out here (all are in `answers.json`).

| workload | store | arm | readable from | below | answers | short | exact |
|---|---|---|---|---|---|---|---|
| w1_enron | milvus | a4@iterative | 0 | 100 | 4914 | 0 | 4026 |
| w1_enron | milvus | a4@iterative | 100 | 200 | 3021 | 0 | 2180 |
| w1_enron | milvus | a4@iterative | 200 | 500 | 2760 | 0 | 1780 |
| w1_enron | milvus | a4@iterative | 500 | 1,000 | 840 | 0 | 438 |
| w1_enron | milvus | a4@iterative | 1,250 | 1,500 | 120 | 0 | 50 |
| w1_enron | milvus | a4@iterative | 1,500 | 1,750 | 120 | 0 | 75 |
| w1_enron | milvus | a4@iterative | 2,000 | 2,500 | 60 | 0 | 20 |
| w1_enron | milvus | a4@iterative | 3,000 | 5,000 | 120 | 0 | 50 |
| w1_enron | pgvector | a4@default | 1,500 | 1,750 | 120 | 81 | 38 |
| w1_enron | pgvector | a4@default | 2,000 | 2,500 | 60 | 48 | 12 |
| w1_enron | pgvector | a4@default | 3,000 | 5,000 | 120 | 96 | 17 |
| w1_enron | pgvector | a4@iterative | 1,500 | 1,750 | 120 | 3 | 56 |
| w1_enron | pgvector | a4@iterative | 2,000 | 2,500 | 60 | 0 | 21 |
| w1_enron | pgvector | a4@iterative | 3,000 | 5,000 | 120 | 0 | 52 |
| w2_erbac_a | milvus | a4@default | 12,500 | 20,000 | 930 | 0 | 800 |
| w2_erbac_a | milvus | a4@default | 20,000 | 40,000 | 960 | 0 | 772 |
| w2_erbac_a | milvus | a4@iterative | 100 | 200 | 90 | 0 | 84 |
| w2_erbac_a | milvus | a4@iterative | 1,000 | 1,250 | 30 | 0 | 23 |
| w2_erbac_a | milvus | a4@iterative | 1,750 | 2,000 | 60 | 0 | 48 |
| w2_erbac_a | milvus | a4@iterative | 2,000 | 2,500 | 90 | 0 | 71 |
| w2_erbac_a | milvus | a4@iterative | 3,000 | 5,000 | 90 | 0 | 75 |
| w2_erbac_a | milvus | a4@iterative | 5,000 | 10,000 | 510 | 0 | 388 |
| w2_erbac_a | milvus | a4@iterative | 10,000 | 10,500 | 30 | 0 | 25 |
| w2_erbac_a | milvus | a4@iterative | 10,500 | 11,000 | 60 | 0 | 50 |
| w2_erbac_a | milvus | a4@iterative | 11,000 | 11,500 | 60 | 0 | 53 |
| w2_erbac_a | milvus | a4@iterative | 11,500 | 12,500 | 90 | 0 | 72 |
| w2_erbac_a | milvus | a4@iterative | 12,500 | 20,000 | 930 | 0 | 668 |
| w2_erbac_a | milvus | a4@iterative | 20,000 | 40,000 | 960 | 0 | 732 |
| w2_erbac_a | opensearch | a4@default | 12,500 | 20,000 | 930 | 0 | 900 |
| w2_erbac_a | opensearch | a4@default | 20,000 | 40,000 | 960 | 0 | 815 |
| w2_erbac_a | pgvector | a4@default | 1,750 | 2,000 | 60 | 60 | 0 |
| w2_erbac_a | pgvector | a4@default | 2,000 | 2,500 | 90 | 90 | 0 |
| w2_erbac_a | pgvector | a4@default | 3,000 | 5,000 | 90 | 90 | 0 |
| w2_erbac_a | pgvector | a4@default | 5,000 | 10,000 | 510 | 501 | 6 |
| w2_erbac_a | pgvector | a4@default | 10,000 | 10,500 | 30 | 30 | 0 |
| w2_erbac_a | pgvector | a4@default | 10,500 | 11,000 | 60 | 54 | 6 |
| w2_erbac_a | pgvector | a4@default | 11,000 | 11,500 | 60 | 60 | 0 |
| w2_erbac_a | pgvector | a4@default | 11,500 | 12,500 | 90 | 81 | 3 |
| w2_erbac_a | pgvector | a4@default | 12,500 | 20,000 | 930 | 622 | 190 |
| w2_erbac_a | pgvector | a4@default | 20,000 | 40,000 | 960 | 197 | 460 |
| w2_erbac_a | pgvector | a4@iterative | 1,750 | 2,000 | 60 | 0 | 40 |
| w2_erbac_a | pgvector | a4@iterative | 2,000 | 2,500 | 90 | 0 | 55 |
| w2_erbac_a | pgvector | a4@iterative | 3,000 | 5,000 | 90 | 0 | 74 |
| w2_erbac_a | pgvector | a4@iterative | 5,000 | 10,000 | 510 | 0 | 362 |
| w2_erbac_a | pgvector | a4@iterative | 10,000 | 10,500 | 30 | 0 | 24 |
| w2_erbac_a | pgvector | a4@iterative | 10,500 | 11,000 | 60 | 0 | 39 |
| w2_erbac_a | pgvector | a4@iterative | 11,000 | 11,500 | 60 | 0 | 51 |
| w2_erbac_a | pgvector | a4@iterative | 11,500 | 12,500 | 90 | 0 | 62 |
| w2_erbac_a | pgvector | a4@iterative | 12,500 | 20,000 | 930 | 0 | 576 |
| w2_erbac_a | pgvector | a4@iterative | 20,000 | 40,000 | 960 | 0 | 591 |
| w2_erbac_a | qdrant | a4@acorn | 5,000 | 10,000 | 510 | 0 | 458 |
| w2_erbac_a | qdrant | a4@acorn | 10,500 | 11,000 | 60 | 0 | 54 |
| w2_erbac_a | qdrant | a4@acorn | 11,000 | 11,500 | 60 | 0 | 55 |
| w2_erbac_a | qdrant | a4@acorn | 11,500 | 12,500 | 90 | 0 | 82 |
| w2_erbac_a | qdrant | a4@acorn | 12,500 | 20,000 | 930 | 0 | 838 |
| w2_erbac_a | qdrant | a4@acorn | 20,000 | 40,000 | 960 | 0 | 892 |
| w2_erbac_a | qdrant | a4@default | 5,000 | 10,000 | 510 | 83 | 240 |
| w2_erbac_a | qdrant | a4@default | 10,000 | 10,500 | 30 | 0 | 7 |
| w2_erbac_a | qdrant | a4@default | 10,500 | 11,000 | 60 | 8 | 0 |
| w2_erbac_a | qdrant | a4@default | 11,000 | 11,500 | 60 | 0 | 9 |
| w2_erbac_a | qdrant | a4@default | 11,500 | 12,500 | 90 | 1 | 6 |
| w2_erbac_a | qdrant | a4@default | 12,500 | 20,000 | 930 | 36 | 43 |
| w2_erbac_a | qdrant | a4@default | 20,000 | 40,000 | 960 | 9 | 161 |
| w2_erbac_b | milvus | a4@default | 12,500 | 20,000 | 360 | 0 | 312 |
| w2_erbac_b | milvus | a4@default | 20,000 | 40,000 | 1080 | 0 | 873 |
| w2_erbac_b | milvus | a4@default | 40,000 | 50,000 | 660 | 0 | 511 |
| w2_erbac_b | milvus | a4@default | 50,000 | 51,000 | 30 | 0 | 22 |
| w2_erbac_b | milvus | a4@default | 51,000 | 60,000 | 330 | 0 | 244 |
| w2_erbac_b | milvus | a4@default | 60,000 | 100,000 | 30 | 0 | 28 |
| w2_erbac_b | milvus | a4@iterative | 1,750 | 2,000 | 30 | 0 | 22 |
| w2_erbac_b | milvus | a4@iterative | 5,000 | 10,000 | 420 | 0 | 328 |
| w2_erbac_b | milvus | a4@iterative | 11,500 | 12,500 | 60 | 0 | 43 |
| w2_erbac_b | milvus | a4@iterative | 12,500 | 20,000 | 360 | 0 | 270 |
| w2_erbac_b | milvus | a4@iterative | 20,000 | 40,000 | 1080 | 0 | 844 |
| w2_erbac_b | milvus | a4@iterative | 40,000 | 50,000 | 660 | 0 | 524 |
| w2_erbac_b | milvus | a4@iterative | 50,000 | 51,000 | 30 | 0 | 24 |
| w2_erbac_b | milvus | a4@iterative | 51,000 | 60,000 | 330 | 0 | 252 |
| w2_erbac_b | opensearch | a4@default | 12,500 | 20,000 | 360 | 0 | 355 |
| w2_erbac_b | opensearch | a4@default | 20,000 | 40,000 | 1080 | 0 | 947 |
| w2_erbac_b | opensearch | a4@default | 40,000 | 50,000 | 660 | 0 | 600 |
| w2_erbac_b | opensearch | a4@default | 50,000 | 51,000 | 30 | 0 | 27 |
| w2_erbac_b | opensearch | a4@default | 51,000 | 60,000 | 330 | 0 | 295 |
| w2_erbac_b | opensearch | a4@default | 60,000 | 100,000 | 30 | 0 | 29 |
| w2_erbac_b | pgvector | a4@default | 1,750 | 2,000 | 30 | 30 | 0 |
| w2_erbac_b | pgvector | a4@default | 5,000 | 10,000 | 420 | 414 | 6 |
| w2_erbac_b | pgvector | a4@default | 11,500 | 12,500 | 60 | 60 | 0 |
| w2_erbac_b | pgvector | a4@default | 12,500 | 20,000 | 360 | 272 | 55 |
| w2_erbac_b | pgvector | a4@default | 20,000 | 40,000 | 1080 | 116 | 641 |
| w2_erbac_b | pgvector | a4@default | 40,000 | 50,000 | 660 | 0 | 456 |
| w2_erbac_b | pgvector | a4@default | 50,000 | 51,000 | 30 | 0 | 21 |
| w2_erbac_b | pgvector | a4@default | 51,000 | 60,000 | 330 | 0 | 246 |
| w2_erbac_b | pgvector | a4@default | 60,000 | 100,000 | 30 | 0 | 27 |
| w2_erbac_b | pgvector | a4@iterative | 1,750 | 2,000 | 30 | 0 | 22 |
| w2_erbac_b | pgvector | a4@iterative | 5,000 | 10,000 | 420 | 0 | 289 |
| w2_erbac_b | pgvector | a4@iterative | 11,500 | 12,500 | 60 | 0 | 43 |
| w2_erbac_b | pgvector | a4@iterative | 12,500 | 20,000 | 360 | 0 | 242 |
| w2_erbac_b | pgvector | a4@iterative | 20,000 | 40,000 | 1080 | 0 | 717 |
| w2_erbac_b | pgvector | a4@iterative | 40,000 | 50,000 | 660 | 0 | 456 |
| w2_erbac_b | pgvector | a4@iterative | 50,000 | 51,000 | 30 | 0 | 21 |
| w2_erbac_b | pgvector | a4@iterative | 51,000 | 60,000 | 330 | 0 | 246 |
| w2_erbac_b | pgvector | a4@iterative | 60,000 | 100,000 | 30 | 0 | 27 |
| w2_erbac_b | qdrant | a4@acorn | 5,000 | 10,000 | 420 | 0 | 376 |
| w2_erbac_b | qdrant | a4@acorn | 11,500 | 12,500 | 60 | 0 | 53 |
| w2_erbac_b | qdrant | a4@acorn | 12,500 | 20,000 | 360 | 0 | 331 |
| w2_erbac_b | qdrant | a4@acorn | 20,000 | 40,000 | 1080 | 0 | 1012 |
| w2_erbac_b | qdrant | a4@acorn | 40,000 | 50,000 | 660 | 0 | 615 |
| w2_erbac_b | qdrant | a4@acorn | 50,000 | 51,000 | 30 | 0 | 26 |
| w2_erbac_b | qdrant | a4@acorn | 51,000 | 60,000 | 330 | 0 | 312 |
| w2_erbac_b | qdrant | a4@acorn | 60,000 | 100,000 | 30 | 0 | 29 |
| w2_erbac_b | qdrant | a4@default | 5,000 | 10,000 | 420 | 92 | 153 |
| w2_erbac_b | qdrant | a4@default | 11,500 | 12,500 | 60 | 0 | 10 |
| w2_erbac_b | qdrant | a4@default | 12,500 | 20,000 | 360 | 10 | 22 |
| w2_erbac_b | qdrant | a4@default | 20,000 | 40,000 | 1080 | 1 | 239 |
| w2_erbac_b | qdrant | a4@default | 40,000 | 50,000 | 660 | 2 | 208 |
| w2_erbac_b | qdrant | a4@default | 50,000 | 51,000 | 30 | 0 | 7 |
| w2_erbac_b | qdrant | a4@default | 51,000 | 60,000 | 330 | 0 | 118 |
| w2_erbac_b | qdrant | a4@default | 60,000 | 100,000 | 30 | 0 | 16 |
| w2_erbac_b | weaviate | a4@default | 40,000 | 50,000 | 660 | 0 | 455 |
| w2_erbac_b | weaviate | a4@default | 50,000 | 51,000 | 30 | 0 | 23 |
| w2_erbac_b | weaviate | a4@default | 51,000 | 60,000 | 330 | 0 | 223 |
| w2_erbac_b | weaviate | a4@default | 60,000 | 100,000 | 30 | 0 | 25 |
| w2_erbac_b | weaviate | a4@pathseer | 40,000 | 50,000 | 660 | 0 | 526 |
| w2_erbac_b | weaviate | a4@pathseer | 50,000 | 51,000 | 30 | 0 | 24 |
| w2_erbac_b | weaviate | a4@pathseer | 51,000 | 60,000 | 330 | 0 | 265 |
| w2_tree_a | milvus | a4@iterative | 3,000 | 5,000 | 90 | 0 | 68 |
| w2_tree_a | milvus | a4@iterative | 5,000 | 10,000 | 1500 | 0 | 1080 |
| w2_tree_a | milvus | a4@iterative | 10,000 | 10,500 | 1410 | 0 | 1022 |
| w2_tree_a | pgvector | a4@default | 3,000 | 5,000 | 90 | 90 | 0 |
| w2_tree_a | pgvector | a4@default | 5,000 | 10,000 | 1500 | 1497 | 3 |
| w2_tree_a | pgvector | a4@default | 10,000 | 10,500 | 1410 | 1360 | 36 |
| w2_tree_a | pgvector | a4@iterative | 3,000 | 5,000 | 90 | 0 | 62 |
| w2_tree_a | pgvector | a4@iterative | 5,000 | 10,000 | 1500 | 0 | 1020 |
| w2_tree_a | pgvector | a4@iterative | 10,000 | 10,500 | 1410 | 0 | 913 |
| w2_tree_a | qdrant | a4@acorn | 5,000 | 10,000 | 1500 | 0 | 1142 |
| w2_tree_a | qdrant | a4@acorn | 10,000 | 10,500 | 1410 | 0 | 1017 |
| w2_tree_a | qdrant | a4@default | 5,000 | 10,000 | 1500 | 861 | 390 |
| w2_tree_a | qdrant | a4@default | 10,000 | 10,500 | 1410 | 1063 | 0 |
| w2_uniform_a | milvus | a4@default | 12,500 | 20,000 | 420 | 0 | 369 |
| w2_uniform_a | milvus | a4@iterative | 500 | 1,000 | 120 | 0 | 82 |
| w2_uniform_a | milvus | a4@iterative | 1,000 | 1,250 | 30 | 0 | 24 |
| w2_uniform_a | milvus | a4@iterative | 1,500 | 1,750 | 90 | 0 | 79 |
| w2_uniform_a | milvus | a4@iterative | 1,750 | 2,000 | 30 | 0 | 16 |
| w2_uniform_a | milvus | a4@iterative | 2,000 | 2,500 | 150 | 0 | 97 |
| w2_uniform_a | milvus | a4@iterative | 2,500 | 3,000 | 180 | 0 | 121 |
| w2_uniform_a | milvus | a4@iterative | 3,000 | 5,000 | 150 | 0 | 100 |
| w2_uniform_a | milvus | a4@iterative | 5,000 | 10,000 | 1260 | 0 | 827 |
| w2_uniform_a | milvus | a4@iterative | 10,000 | 10,500 | 60 | 0 | 36 |
| w2_uniform_a | milvus | a4@iterative | 10,500 | 11,000 | 180 | 0 | 115 |
| w2_uniform_a | milvus | a4@iterative | 11,000 | 11,500 | 60 | 0 | 45 |
| w2_uniform_a | milvus | a4@iterative | 11,500 | 12,500 | 270 | 0 | 170 |
| w2_uniform_a | milvus | a4@iterative | 12,500 | 20,000 | 420 | 0 | 287 |
| w2_uniform_a | opensearch | a4@default | 12,500 | 20,000 | 420 | 0 | 415 |
| w2_uniform_a | pgvector | a4@default | 1,000 | 1,250 | 30 | 10 | 20 |
| w2_uniform_a | pgvector | a4@default | 1,500 | 1,750 | 90 | 90 | 0 |
| w2_uniform_a | pgvector | a4@default | 1,750 | 2,000 | 30 | 30 | 0 |
| w2_uniform_a | pgvector | a4@default | 2,000 | 2,500 | 150 | 150 | 0 |
| w2_uniform_a | pgvector | a4@default | 2,500 | 3,000 | 180 | 180 | 0 |
| w2_uniform_a | pgvector | a4@default | 3,000 | 5,000 | 150 | 150 | 0 |
| w2_uniform_a | pgvector | a4@default | 5,000 | 10,000 | 1260 | 1251 | 3 |
| w2_uniform_a | pgvector | a4@default | 10,000 | 10,500 | 60 | 60 | 0 |
| w2_uniform_a | pgvector | a4@default | 10,500 | 11,000 | 180 | 171 | 7 |
| w2_uniform_a | pgvector | a4@default | 11,000 | 11,500 | 60 | 57 | 3 |
| w2_uniform_a | pgvector | a4@default | 11,500 | 12,500 | 270 | 244 | 18 |
| w2_uniform_a | pgvector | a4@default | 12,500 | 20,000 | 420 | 340 | 52 |
| w2_uniform_a | pgvector | a4@iterative | 1,000 | 1,250 | 30 | 0 | 29 |
| w2_uniform_a | pgvector | a4@iterative | 1,500 | 1,750 | 90 | 0 | 78 |
| w2_uniform_a | pgvector | a4@iterative | 1,750 | 2,000 | 30 | 0 | 27 |
| w2_uniform_a | pgvector | a4@iterative | 2,000 | 2,500 | 150 | 0 | 105 |
| w2_uniform_a | pgvector | a4@iterative | 2,500 | 3,000 | 180 | 0 | 145 |
| w2_uniform_a | pgvector | a4@iterative | 3,000 | 5,000 | 150 | 0 | 106 |
| w2_uniform_a | pgvector | a4@iterative | 5,000 | 10,000 | 1260 | 0 | 831 |
| w2_uniform_a | pgvector | a4@iterative | 10,000 | 10,500 | 60 | 0 | 30 |
| w2_uniform_a | pgvector | a4@iterative | 10,500 | 11,000 | 180 | 0 | 106 |
| w2_uniform_a | pgvector | a4@iterative | 11,000 | 11,500 | 60 | 0 | 42 |
| w2_uniform_a | pgvector | a4@iterative | 11,500 | 12,500 | 270 | 0 | 153 |
| w2_uniform_a | pgvector | a4@iterative | 12,500 | 20,000 | 420 | 0 | 256 |
| w2_uniform_a | qdrant | a4@acorn | 5,000 | 10,000 | 1260 | 0 | 1250 |
| w2_uniform_a | qdrant | a4@acorn | 10,000 | 10,500 | 60 | 0 | 58 |
| w2_uniform_a | qdrant | a4@acorn | 10,500 | 11,000 | 180 | 0 | 176 |
| w2_uniform_a | qdrant | a4@acorn | 11,000 | 11,500 | 60 | 0 | 58 |
| w2_uniform_a | qdrant | a4@acorn | 11,500 | 12,500 | 270 | 0 | 260 |
| w2_uniform_a | qdrant | a4@acorn | 12,500 | 20,000 | 420 | 0 | 409 |
| w2_uniform_a | qdrant | a4@default | 5,000 | 10,000 | 1260 | 58 | 931 |
| w2_uniform_a | qdrant | a4@default | 10,000 | 10,500 | 60 | 0 | 17 |
| w2_uniform_a | qdrant | a4@default | 10,500 | 11,000 | 180 | 12 | 39 |
| w2_uniform_a | qdrant | a4@default | 11,000 | 11,500 | 60 | 0 | 13 |
| w2_uniform_a | qdrant | a4@default | 11,500 | 12,500 | 270 | 0 | 60 |
| w2_uniform_a | qdrant | a4@default | 12,500 | 20,000 | 420 | 0 | 227 |
| w3 | milvus | a4@default | 200,000 | 500,000 | 9000 | 0 | 6870 |
| w3 | milvus | a4@default | 500,000 | 1,000,000,000 | 9000 | 0 | 6699 |
| w3 | milvus | a4@iterative | 1,000 | 1,250 | 3390 | 0 | 2426 |
| w3 | milvus | a4@iterative | 1,250 | 1,500 | 2460 | 0 | 1481 |
| w3 | milvus | a4@iterative | 1,500 | 1,750 | 1350 | 0 | 960 |
| w3 | milvus | a4@iterative | 1,750 | 2,000 | 1020 | 0 | 694 |
| w3 | milvus | a4@iterative | 2,000 | 2,500 | 660 | 0 | 477 |
| w3 | milvus | a4@iterative | 2,500 | 3,000 | 120 | 0 | 73 |
| w3 | milvus | a4@iterative | 10,000 | 10,500 | 4470 | 0 | 2697 |
| w3 | milvus | a4@iterative | 10,500 | 11,000 | 2850 | 0 | 1730 |
| w3 | milvus | a4@iterative | 11,000 | 11,500 | 1380 | 0 | 833 |
| w3 | milvus | a4@iterative | 11,500 | 12,500 | 300 | 0 | 173 |
| w3 | milvus | a4@iterative | 50,000 | 51,000 | 7440 | 0 | 4793 |
| w3 | milvus | a4@iterative | 51,000 | 60,000 | 1560 | 0 | 1048 |
| w3 | milvus | a4@iterative | 200,000 | 500,000 | 9000 | 0 | 6092 |
| w3 | milvus | a4@iterative | 500,000 | 1,000,000,000 | 9000 | 0 | 6813 |
| w3 | opensearch | a4@default | 50,000 | 51,000 | 7440 | 0 | 7437 |
| w3 | opensearch | a4@default | 200,000 | 500,000 | 9000 | 0 | 6696 |
| w3 | opensearch | a4@default | 500,000 | 1,000,000,000 | 9000 | 0 | 7918 |
| w3 | pgvector | a4@default | 1,750 | 2,000 | 1020 | 40 | 980 |
| w3 | pgvector | a4@default | 2,000 | 2,500 | 660 | 238 | 420 |
| w3 | pgvector | a4@default | 2,500 | 3,000 | 120 | 86 | 33 |
| w3 | pgvector | a4@default | 10,000 | 10,500 | 4470 | 4325 | 81 |
| w3 | pgvector | a4@default | 10,500 | 11,000 | 2850 | 2743 | 60 |
| w3 | pgvector | a4@default | 11,000 | 11,500 | 1380 | 1285 | 54 |
| w3 | pgvector | a4@default | 11,500 | 12,500 | 300 | 283 | 9 |
| w3 | pgvector | a4@default | 50,000 | 51,000 | 7440 | 6156 | 807 |
| w3 | pgvector | a4@default | 51,000 | 60,000 | 1560 | 1265 | 141 |
| w3 | pgvector | a4@default | 200,000 | 500,000 | 9000 | 4746 | 2746 |
| w3 | pgvector | a4@default | 500,000 | 1,000,000,000 | 9000 | 1882 | 5164 |
| w3 | pgvector | a4@iterative | 1,750 | 2,000 | 1020 | 17 | 981 |
| w3 | pgvector | a4@iterative | 2,000 | 2,500 | 660 | 162 | 436 |
| w3 | pgvector | a4@iterative | 2,500 | 3,000 | 120 | 30 | 44 |
| w3 | pgvector | a4@iterative | 10,000 | 10,500 | 4470 | 952 | 743 |
| w3 | pgvector | a4@iterative | 10,500 | 11,000 | 2850 | 440 | 529 |
| w3 | pgvector | a4@iterative | 11,000 | 11,500 | 1380 | 74 | 294 |
| w3 | pgvector | a4@iterative | 11,500 | 12,500 | 300 | 66 | 75 |
| w3 | pgvector | a4@iterative | 50,000 | 51,000 | 7440 | 80 | 2560 |
| w3 | pgvector | a4@iterative | 51,000 | 60,000 | 1560 | 14 | 552 |
| w3 | pgvector | a4@iterative | 200,000 | 500,000 | 9000 | 0 | 4545 |
| w3 | pgvector | a4@iterative | 500,000 | 1,000,000,000 | 9000 | 0 | 5935 |
| w3 | qdrant | a4@acorn | 10,000 | 10,500 | 4470 | 0 | 4294 |
| w3 | qdrant | a4@acorn | 10,500 | 11,000 | 2850 | 0 | 2496 |
| w3 | qdrant | a4@acorn | 11,000 | 11,500 | 1380 | 0 | 1239 |
| w3 | qdrant | a4@acorn | 11,500 | 12,500 | 300 | 0 | 255 |
| w3 | qdrant | a4@acorn | 50,000 | 51,000 | 7440 | 0 | 4130 |
| w3 | qdrant | a4@acorn | 51,000 | 60,000 | 1560 | 0 | 916 |
| w3 | qdrant | a4@acorn | 200,000 | 500,000 | 9000 | 0 | 6275 |
| w3 | qdrant | a4@acorn | 500,000 | 1,000,000,000 | 9000 | 0 | 7100 |
| w3 | qdrant | a4@default | 10,000 | 10,500 | 4470 | 0 | 4126 |
| w3 | qdrant | a4@default | 10,500 | 11,000 | 2850 | 0 | 2198 |
| w3 | qdrant | a4@default | 11,000 | 11,500 | 1380 | 0 | 1035 |
| w3 | qdrant | a4@default | 11,500 | 12,500 | 300 | 0 | 211 |
| w3 | qdrant | a4@default | 50,000 | 51,000 | 7440 | 0 | 1146 |
| w3 | qdrant | a4@default | 51,000 | 60,000 | 1560 | 0 | 262 |
| w3 | qdrant | a4@default | 200,000 | 500,000 | 9000 | 0 | 2980 |
| w3 | qdrant | a4@default | 500,000 | 1,000,000,000 | 9000 | 0 | 4904 |
| w3 | weaviate | a4@default | 50,000 | 51,000 | 7440 | 0 | 2612 |
| w3 | weaviate | a4@default | 51,000 | 60,000 | 1560 | 0 | 530 |
| w3 | weaviate | a4@default | 200,000 | 500,000 | 9000 | 0 | 4144 |
| w3 | weaviate | a4@default | 500,000 | 1,000,000,000 | 9000 | 0 | 6864 |
| w3 | weaviate | a4@pathseer | 50,000 | 51,000 | 7440 | 0 | 4345 |
| w3 | weaviate | a4@pathseer | 51,000 | 60,000 | 1560 | 0 | 935 |
| w3 | weaviate | a4@pathseer | 200,000 | 500,000 | 9000 | 0 | 5451 |
| w3 | weaviate | a4@pathseer | 500,000 | 1,000,000,000 | 9000 | 0 | 6228 |

## W1 by question kind (own mail, other mail)

| store | arm | kind | queries | recall | empty | short |
|---|---|---|---|---|---|---|
| milvus | a1-fga | other | 6000 | 0.001 | 5965 | 6000 |
| milvus | a1-fga | own | 5955 | 0.261 | 1302 | 5707 |
| milvus | a1-spicedb | other | 6000 | 0.001 | 5965 | 6000 |
| milvus | a1-spicedb | own | 5955 | 0.261 | 1302 | 5707 |
| milvus | a2-fga-x10 | other | 6000 | 0.009 | 5701 | 5995 |
| milvus | a2-fga-x10 | own | 5955 | 0.455 | 884 | 4365 |
| milvus | a2-fga-x3 | other | 6000 | 0.002 | 5904 | 6000 |
| milvus | a2-fga-x3 | own | 5955 | 0.369 | 1040 | 4995 |
| milvus | a2-spicedb-x10 | other | 6000 | 0.009 | 5701 | 5995 |
| milvus | a2-spicedb-x10 | own | 5955 | 0.455 | 884 | 4365 |
| milvus | a2-spicedb-x3 | other | 6000 | 0.002 | 5904 | 6000 |
| milvus | a2-spicedb-x3 | own | 5955 | 0.369 | 1040 | 4995 |
| milvus | a3-spicedb@default | other | 6000 | 1.000 | 0 | 0 |
| milvus | a3-spicedb@default | own | 5955 | 1.000 | 0 | 0 |
| milvus | a3-spicedb@iterative | other | 6000 | 0.957 | 0 | 0 |
| milvus | a3-spicedb@iterative | own | 5955 | 0.967 | 0 | 0 |
| milvus | a4@default | other | 6000 | 1.000 | 0 | 0 |
| milvus | a4@default | own | 5955 | 1.000 | 0 | 0 |
| milvus | a4@iterative | other | 6000 | 0.957 | 0 | 0 |
| milvus | a4@iterative | own | 5955 | 0.967 | 0 | 0 |
| opensearch | a1-fga | other | 6000 | 0.001 | 5966 | 6000 |
| opensearch | a1-fga | own | 5955 | 0.272 | 875 | 5713 |
| opensearch | a1-spicedb | other | 6000 | 0.001 | 5966 | 6000 |
| opensearch | a1-spicedb | own | 5955 | 0.272 | 875 | 5713 |
| opensearch | a2-fga-x10 | other | 6000 | 0.010 | 5683 | 6000 |
| opensearch | a2-fga-x10 | own | 5955 | 0.469 | 473 | 4383 |
| opensearch | a2-fga-x3 | other | 6000 | 0.002 | 5898 | 6000 |
| opensearch | a2-fga-x3 | own | 5955 | 0.382 | 609 | 5004 |
| opensearch | a2-spicedb-x10 | other | 6000 | 0.010 | 5683 | 6000 |
| opensearch | a2-spicedb-x10 | own | 5955 | 0.469 | 473 | 4383 |
| opensearch | a2-spicedb-x3 | other | 6000 | 0.002 | 5898 | 6000 |
| opensearch | a2-spicedb-x3 | own | 5955 | 0.382 | 609 | 5004 |
| opensearch | a3-spicedb@default | other | 6000 | 1.000 | 0 | 0 |
| opensearch | a3-spicedb@default | own | 5955 | 1.000 | 0 | 0 |
| opensearch | a4@default | other | 6000 | 1.000 | 0 | 0 |
| opensearch | a4@default | own | 5955 | 1.000 | 0 | 0 |
| opensearch | a5-dls | other | 6000 | 0.019 | 5295 | 5993 |
| opensearch | a5-dls | own | 5955 | 0.404 | 500 | 4952 |
| pgvector | a0 | other | 299 | 1.000 | 0 | 0 |
| pgvector | a0 | own | 301 | 1.000 | 0 | 0 |
| pgvector | a1-fga | other | 6000 | 0.001 | 5961 | 6000 |
| pgvector | a1-fga | own | 5955 | 0.265 | 1085 | 5712 |
| pgvector | a1-spicedb | other | 6000 | 0.001 | 5961 | 6000 |
| pgvector | a1-spicedb | own | 5955 | 0.265 | 1085 | 5712 |
| pgvector | a2-fga-x10 | other | 6000 | 0.009 | 5714 | 5997 |
| pgvector | a2-fga-x10 | own | 5955 | 0.465 | 721 | 4385 |
| pgvector | a2-fga-x3 | other | 6000 | 0.002 | 5899 | 6000 |
| pgvector | a2-fga-x3 | own | 5955 | 0.377 | 825 | 5013 |
| pgvector | a2-spicedb-x10 | other | 6000 | 0.009 | 5714 | 5997 |
| pgvector | a2-spicedb-x10 | own | 5955 | 0.465 | 721 | 4385 |
| pgvector | a2-spicedb-x3 | other | 6000 | 0.002 | 5899 | 6000 |
| pgvector | a2-spicedb-x3 | own | 5955 | 0.377 | 825 | 5013 |
| pgvector | a3-spicedb@default | other | 6000 | 1.000 | 0 | 0 |
| pgvector | a3-spicedb@default | own | 5955 | 1.000 | 0 | 0 |
| pgvector | a3-spicedb@iterative | other | 6000 | 1.000 | 0 | 0 |
| pgvector | a3-spicedb@iterative | own | 5955 | 1.000 | 0 | 0 |
| pgvector | a4@default | other | 6000 | 0.976 | 128 | 150 |
| pgvector | a4@default | own | 5955 | 0.993 | 7 | 75 |
| pgvector | a4@iterative | other | 6000 | 0.994 | 0 | 3 |
| pgvector | a4@iterative | own | 5955 | 0.998 | 0 | 0 |
| pgvector | a5-rls@default | other | 6000 | 0.976 | 128 | 150 |
| pgvector | a5-rls@default | own | 5955 | 0.993 | 7 | 75 |
| pgvector | a5-rls@iterative | other | 6000 | 0.994 | 0 | 3 |
| pgvector | a5-rls@iterative | own | 5955 | 0.998 | 0 | 0 |
| pgvector | a6-partition | other | 6000 | 1.000 | 0 | 0 |
| pgvector | a6-partition | own | 5955 | 1.000 | 0 | 0 |
| pgvector | a7-wardowl | other | 6000 | 0.413 | 546 | 3406 |
| pgvector | a7-wardowl | own | 5955 | 0.862 | 4 | 642 |
| qdrant | a1-fga | other | 6000 | 0.001 | 5962 | 6000 |
| qdrant | a1-fga | own | 5955 | 0.261 | 1215 | 5713 |
| qdrant | a1-spicedb | other | 6000 | 0.001 | 5962 | 6000 |
| qdrant | a1-spicedb | own | 5955 | 0.261 | 1215 | 5713 |
| qdrant | a2-fga-x10 | other | 6000 | 0.009 | 5695 | 5997 |
| qdrant | a2-fga-x10 | own | 5955 | 0.457 | 827 | 4385 |
| qdrant | a2-fga-x3 | other | 6000 | 0.002 | 5903 | 6000 |
| qdrant | a2-fga-x3 | own | 5955 | 0.369 | 962 | 5018 |
| qdrant | a2-spicedb-x10 | other | 6000 | 0.009 | 5695 | 5997 |
| qdrant | a2-spicedb-x10 | own | 5955 | 0.457 | 827 | 4385 |
| qdrant | a2-spicedb-x3 | other | 6000 | 0.002 | 5903 | 6000 |
| qdrant | a2-spicedb-x3 | own | 5955 | 0.369 | 962 | 5018 |
| qdrant | a3-spicedb@acorn | other | 6000 | 1.000 | 0 | 0 |
| qdrant | a3-spicedb@acorn | own | 5955 | 1.000 | 0 | 0 |
| qdrant | a3-spicedb@default | other | 6000 | 1.000 | 0 | 0 |
| qdrant | a3-spicedb@default | own | 5955 | 1.000 | 0 | 0 |
| qdrant | a4@acorn | other | 6000 | 1.000 | 0 | 0 |
| qdrant | a4@acorn | own | 5955 | 1.000 | 0 | 0 |
| qdrant | a4@default | other | 6000 | 1.000 | 0 | 0 |
| qdrant | a4@default | own | 5955 | 1.000 | 0 | 0 |
| qdrant | a7-wardowl | other | 6000 | 0.977 | 47 | 172 |
| qdrant | a7-wardowl | own | 5955 | 0.994 | 3 | 33 |
| weaviate | a1-fga | other | 6000 | 0.001 | 5964 | 6000 |
| weaviate | a1-fga | own | 5955 | 0.258 | 1269 | 5718 |
| weaviate | a1-spicedb | other | 6000 | 0.001 | 5964 | 6000 |
| weaviate | a1-spicedb | own | 5955 | 0.258 | 1269 | 5718 |
| weaviate | a2-fga-x10 | other | 6000 | 0.008 | 5735 | 5997 |
| weaviate | a2-fga-x10 | own | 5955 | 0.450 | 895 | 4413 |
| weaviate | a2-fga-x3 | other | 6000 | 0.002 | 5905 | 6000 |
| weaviate | a2-fga-x3 | own | 5955 | 0.364 | 1035 | 5034 |
| weaviate | a2-spicedb-x10 | other | 6000 | 0.008 | 5735 | 5997 |
| weaviate | a2-spicedb-x10 | own | 5955 | 0.450 | 895 | 4413 |
| weaviate | a2-spicedb-x3 | other | 6000 | 0.002 | 5905 | 6000 |
| weaviate | a2-spicedb-x3 | own | 5955 | 0.364 | 1035 | 5034 |
| weaviate | a3-spicedb@default | other | 6000 | 1.000 | 0 | 0 |
| weaviate | a3-spicedb@default | own | 5955 | 1.000 | 0 | 0 |
| weaviate | a3-spicedb@pathseer | other | 6000 | 1.000 | 0 | 0 |
| weaviate | a3-spicedb@pathseer | own | 5955 | 1.000 | 0 | 0 |
| weaviate | a4@default | other | 6000 | 1.000 | 0 | 0 |
| weaviate | a4@default | own | 5955 | 1.000 | 0 | 0 |
| weaviate | a4@pathseer | other | 6000 | 1.000 | 0 | 0 |
| weaviate | a4@pathseer | own | 5955 | 1.000 | 0 | 0 |
