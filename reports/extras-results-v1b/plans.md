# (f) pgvector's executed plans

`bench.run` kept the executed plan (`EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)`) of one query per layout and setting in every pgvector run job: the first (user, question) pair of the layout, so the three jobs of a layout planned the same query on different runners. `a4@exact` is the exact control's setting (A0). `estimated` is the planner's row estimate for the node that applies the principals condition, `actual` the rows that node produced (over all loops), `removed` the rows its filter removed, `returned` the rows the query returned.

`readable` is how many chunks the planned pair's user may read.

| workload | layout | arm | jobs | plan shapes (jobs) | readable | estimated | actual | removed | returned | ms |
|---|---|---|---|---|---|---|---|---|---|---|
| w1_enron | w1_enron | a4@default | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 54 | [146, 150] | [54] | [] | [10] | [0.08, 0.16, 0.16] |
| w1_enron | w1_enron | a4@exact | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 54 | [146, 150] | [54] | [] | [10] | [0.18, 0.18, 0.2] |
| w1_enron | w1_enron | a4@iterative | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 54 | [146, 150] | [54] | [] | [10] | [0.07, 0.13, 0.14] |
| w1_enron | w1_enron | a5-rls@default | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 54 | [146, 150] | [54] | [] | [10] | [0.1, 0.14, 0.16] |
| w1_enron | w1_enron | a5-rls@iterative | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 54 | [146, 150] | [54] | [] | [10] | [0.1, 0.13, 0.13] |
| w2_erbac_a | w2_erbac_a | a4@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 2092 | [1986, 2146, 2153] | [1, 2] | [98, 99] | [1, 2] | [2.33, 2.44, 3.06] |
| w2_erbac_a | w2_erbac_a | a4@exact | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 2092 | [1986, 2146, 2153] | [2092] | [] | [10] | [3.01, 3.29, 3.45] |
| w2_erbac_a | w2_erbac_a | a4@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 2092 | [1986, 2146, 2153] | [10] | [768, 770, 774] | [10] | [13.72, 14.08, 14.58] |
| w2_erbac_a | w2_erbac_a | a5-rls@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 2092 | [1986, 2146, 2153] | [1, 2] | [98, 99] | [1, 2] | [2.03, 2.25, 2.47] |
| w2_erbac_a | w2_erbac_a | a5-rls@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 2092 | [1986, 2146, 2153] | [10] | [768, 770, 774] | [10] | [13.27, 14.71, 16.03] |
| w2_erbac_b | w2_erbac_b | a4@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 47509 | [46914, 47506, 47523] | [10] | [21] | [10] | [2.07, 2.35, 3.16] |
| w2_erbac_b | w2_erbac_b | a4@exact | 3 | `Limit(Gather Merge(Sort(Seq Scan)))` (3) | 47509 | [19548, 19794, 19801] | [47508] | [50830] | [10] | [45.24, 48.75, 62.02] |
| w2_erbac_b | w2_erbac_b | a4@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 47509 | [46914, 47506, 47523] | [10] | [21] | [10] | [0.99, 1.8, 2.75] |
| w2_erbac_b | w2_erbac_b | a5-rls@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 47509 | [46914, 47506, 47523] | [10] | [21] | [10] | [1.01, 1.91, 1.98] |
| w2_erbac_b | w2_erbac_b | a5-rls@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 47509 | [46914, 47506, 47523] | [10] | [21] | [10] | [0.7, 1.47, 1.7] |
| w2_tree_a | w2_tree_a | a4@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 4000 | [4497, 4803, 4826] | [0] | [100] | [0] | [2.24, 2.59, 2.6] |
| w2_tree_a | w2_tree_a | a4@exact | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 4000 | [4497, 4803, 4826] | [4000] | [] | [10] | [5.97, 6.11, 6.37] |
| w2_tree_a | w2_tree_a | a4@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 4000 | [4497, 4803, 4826] | [10] | [470, 471, 473] | [10] | [7.82, 8.38, 10.18] |
| w2_tree_a | w2_tree_a | a5-rls@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 4000 | [4497, 4803, 4826] | [0] | [100] | [0] | [1.33, 1.61, 2.1] |
| w2_tree_a | w2_tree_a | a5-rls@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 4000 | [4497, 4803, 4826] | [10] | [470, 471, 473] | [10] | [7.59, 8.33, 9.7] |
| w2_uniform_a | w2_uniform_a | a4@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 10823 | [10766, 10805, 10997] | [3] | [97] | [3] | [1.44, 1.45, 1.62] |
| w2_uniform_a | w2_uniform_a | a4@exact | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 10823 | [10766, 10805, 10997] | [10823] | [] | [10] | [16.7, 17.59, 19.17] |
| w2_uniform_a | w2_uniform_a | a4@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 10823 | [10766, 10805, 10997] | [10] | [227, 228, 229] | [10] | [4.03, 5.16, 5.41] |
| w2_uniform_a | w2_uniform_a | a5-rls@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 10823 | [10766, 10805, 10997] | [3] | [97] | [3] | [0.96, 1.06, 1.49] |
| w2_uniform_a | w2_uniform_a | a5-rls@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 10823 | [10766, 10805, 10997] | [10] | [227, 228, 229] | [10] | [4.26, 5.15, 5.91] |
| w3 | w3_s0p001_neg | a4@default | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 1192 | [1366, 1399] | [1192] | [] | [10] | [0.99, 1.22, 1.69] |
| w3 | w3_s0p001_neg | a4@exact | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 1192 | [1366, 1399] | [1192] | [] | [10] | [3.0, 3.02, 3.09] |
| w3 | w3_s0p001_neg | a4@iterative | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 1192 | [1366, 1399] | [1192] | [] | [10] | [0.8, 1.02, 1.38] |
| w3 | w3_s0p001_neg | a5-rls@default | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 1192 | [1366, 1399] | [1192] | [] | [10] | [0.8, 1.07, 1.19] |
| w3 | w3_s0p001_neg | a5-rls@iterative | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 1192 | [1366, 1399] | [1192] | [] | [10] | [0.75, 0.99, 1.15] |
| w3 | w3_s0p001_none | a4@default | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 1042 | [933, 1167] | [1042] | [] | [10] | [1.06, 1.18, 1.22] |
| w3 | w3_s0p001_none | a4@exact | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 1042 | [933, 1167] | [1042] | [] | [10] | [3.18, 3.26, 3.5] |
| w3 | w3_s0p001_none | a4@iterative | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 1042 | [933, 1167] | [1042] | [] | [10] | [0.8, 0.91, 1.08] |
| w3 | w3_s0p001_none | a5-rls@default | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 1042 | [933, 1167] | [1042] | [] | [10] | [0.77, 0.98, 1.04] |
| w3 | w3_s0p001_none | a5-rls@iterative | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 1042 | [933, 1167] | [1042] | [] | [10] | [0.65, 0.85, 0.98] |
| w3 | w3_s0p001_pos | a4@default | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 1314 | [1100, 1300, 1500] | [1314] | [] | [10] | [1.66, 2.04, 2.25] |
| w3 | w3_s0p001_pos | a4@exact | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 1314 | [1100, 1300, 1500] | [1314] | [] | [10] | [3.5, 5.41, 5.42] |
| w3 | w3_s0p001_pos | a4@iterative | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 1314 | [1100, 1300, 1500] | [1314] | [] | [10] | [1.35, 1.75, 1.95] |
| w3 | w3_s0p001_pos | a5-rls@default | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 1314 | [1100, 1300, 1500] | [1314] | [] | [10] | [1.35, 1.48, 1.77] |
| w3 | w3_s0p001_pos | a5-rls@iterative | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 1314 | [1100, 1300, 1500] | [1314] | [] | [10] | [1.15, 1.35, 1.58] |
| w3 | w3_s0p01_neg | a4@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 10383 | [10055, 10351, 11672] | [0] | [100] | [0] | [2.01, 2.17, 5.81] |
| w3 | w3_s0p01_neg | a4@exact | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 10383 | [10055, 10351, 11672] | [10383] | [] | [10] | [17.95, 19.13, 25.02] |
| w3 | w3_s0p01_neg | a4@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 10383 | [10055, 10351, 11672] | [10] | [12166, 12173, 12181] | [10] | [59.62, 64.7, 102.02] |
| w3 | w3_s0p01_neg | a5-rls@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 10383 | [10055, 10351, 11672] | [0] | [100] | [0] | [2.0, 2.1, 2.33] |
| w3 | w3_s0p01_neg | a5-rls@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 10383 | [10055, 10351, 11672] | [10] | [12166, 12173, 12181] | [10] | [50.24, 55.02, 61.7] |
| w3 | w3_s0p01_none | a4@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 10842 | [10353, 10847, 10914] | [0] | [100] | [0] | [1.6, 1.86, 5.39] |
| w3 | w3_s0p01_none | a4@exact | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 10842 | [10353, 10847, 10914] | [10842] | [] | [10] | [22.82, 23.98, 32.27] |
| w3 | w3_s0p01_none | a4@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 10842 | [10353, 10847, 10914] | [10] | [18612, 18623, 18643] | [10] | [70.3, 80.61, 121.12] |
| w3 | w3_s0p01_none | a5-rls@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 10842 | [10353, 10847, 10914] | [0] | [100] | [0] | [1.54, 1.62, 1.82] |
| w3 | w3_s0p01_none | a5-rls@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 10842 | [10353, 10847, 10914] | [10] | [18612, 18623, 18643] | [10] | [51.01, 59.72, 63.89] |
| w3 | w3_s0p01_pos | a4@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 10663 | [10422, 10950, 10983] | [0] | [100] | [0] | [1.47, 1.52, 4.6] |
| w3 | w3_s0p01_pos | a4@exact | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 10663 | [10422, 10950, 10983] | [10663] | [] | [10] | [29.99, 31.66, 48.63] |
| w3 | w3_s0p01_pos | a4@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 10663 | [10422, 10950, 10983] | [10] | [3228, 3229, 3230] | [10] | [37.51, 37.61, 77.97] |
| w3 | w3_s0p01_pos | a5-rls@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 10663 | [10422, 10950, 10983] | [0] | [100] | [0] | [1.55, 1.59, 1.63] |
| w3 | w3_s0p01_pos | a5-rls@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 10663 | [10422, 10950, 10983] | [10] | [3228, 3229, 3230] | [10] | [30.7, 32.73, 34.97] |
| w3 | w3_s0p05_neg | a4@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 50682 | [47588, 50192, 52788] | [0] | [100] | [0] | [2.79, 2.96, 10.25] |
| w3 | w3_s0p05_neg | a4@exact | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 50682 | [47588, 50192, 52788] | [50682] | [] | [10] | [97.85, 108.11, 132.17] |
| w3 | w3_s0p05_neg | a4@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 50682 | [47588, 50192, 52788] | [10] | [19960, 19973, 19991] | [10] | [94.85, 119.08, 143.97] |
| w3 | w3_s0p05_neg | a5-rls@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 50682 | [47588, 50192, 52788] | [0] | [100] | [0] | [2.9, 3.0, 3.34] |
| w3 | w3_s0p05_neg | a5-rls@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 50682 | [47588, 50192, 52788] | [10] | [19960, 19973, 19991] | [10] | [103.02, 114.88, 134.06] |
| w3 | w3_s0p05_none | a4@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 50879 | [48643, 49340, 50734] | [1] | [99] | [1] | [1.74, 1.86, 6.62] |
| w3 | w3_s0p05_none | a4@exact | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 50879 | [48643, 49340, 50734] | [50879] | [] | [10] | [116.64, 119.02, 147.71] |
| w3 | w3_s0p05_none | a4@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 50879 | [48643, 49340, 50734] | [10] | [851, 852] | [10] | [12.9, 14.46, 30.52] |
| w3 | w3_s0p05_none | a5-rls@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 50879 | [48643, 49340, 50734] | [1] | [99] | [1] | [1.7, 1.72, 1.76] |
| w3 | w3_s0p05_none | a5-rls@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 50879 | [48643, 49340, 50734] | [10] | [851, 852] | [10] | [11.89, 12.61, 12.98] |
| w3 | w3_s0p05_pos | a4@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 50448 | [49438, 49565, 50992] | [10] | [34] | [10] | [1.96, 2.07, 7.56] |
| w3 | w3_s0p05_pos | a4@exact | 3 | `Limit(Sort(Bitmap Heap Scan(Bitmap Index Scan[chunks_principals])))` (3) | 50448 | [49438, 49565, 50992] | [50448] | [] | [10] | [123.41, 149.52, 168.58] |
| w3 | w3_s0p05_pos | a4@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 50448 | [49438, 49565, 50992] | [10] | [34] | [10] | [1.51, 1.66, 1.67] |
| w3 | w3_s0p05_pos | a5-rls@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 50448 | [49438, 49565, 50992] | [10] | [34] | [10] | [1.62, 1.71, 1.76] |
| w3 | w3_s0p05_pos | a5-rls@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 50448 | [49438, 49565, 50992] | [10] | [34] | [10] | [0.96, 1.3, 1.54] |
| w3 | w3_s0p2_neg | a4@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 200357 | [178262, 180263, 186801] | [1] | [99] | [1] | [2.52, 2.73, 114.58] |
| w3 | w3_s0p2_neg | a4@exact | 3 | `Limit(Gather Merge(Sort(Seq Scan)))` (3) | 200357 | [74276, 75110, 77834] | [200358] | [266548] | [10] | [2592.55, 2642.21, 2644.86] |
| w3 | w3_s0p2_neg | a4@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 200357 | [178262, 180263, 186801] | [10] | [636] | [10] | [13.45, 14.47, 284.83] |
| w3 | w3_s0p2_neg | a5-rls@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 200357 | [178262, 180263, 186801] | [1] | [99] | [1] | [3.35, 3.35, 4.75] |
| w3 | w3_s0p2_neg | a5-rls@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 200357 | [178262, 180263, 186801] | [10] | [636] | [10] | [19.88, 22.57, 35.42] |
| w3 | w3_s0p2_none | a4@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 201086 | [181553, 184389, 184661] | [4, 9] | [91, 96] | [4, 9] | [2.72, 2.96, 187.89] |
| w3 | w3_s0p2_none | a4@exact | 3 | `Limit(Gather Merge(Sort(Seq Scan)))` (3) | 201086 | [75647, 76829, 76942] | [201087] | [266305] | [10] | [2164.99, 2189.05, 2228.57] |
| w3 | w3_s0p2_none | a4@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 201086 | [181553, 184389, 184661] | [10] | [103, 105, 111] | [10] | [5.32, 5.48, 137.45] |
| w3 | w3_s0p2_none | a5-rls@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 201086 | [181553, 184389, 184661] | [4, 9] | [91, 96] | [4, 9] | [3.29, 3.5, 4.51] |
| w3 | w3_s0p2_none | a5-rls@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 201086 | [181553, 184389, 184661] | [10] | [103, 105, 111] | [10] | [5.29, 6.04, 6.95] |
| w3 | w3_s0p2_pos | a4@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 200002 | [179958, 180286, 180885] | [10] | [12, 14] | [10] | [2.86, 3.12, 215.8] |
| w3 | w3_s0p2_pos | a4@exact | 3 | `Limit(Gather Merge(Sort(Seq Scan)))` (3) | 200002 | [74982, 75119, 75369] | [200001] | [266666] | [10] | [1768.41, 1810.66, 1833.11] |
| w3 | w3_s0p2_pos | a4@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 200002 | [179958, 180286, 180885] | [10] | [12, 14] | [10] | [1.48, 2.4, 3.55] |
| w3 | w3_s0p2_pos | a5-rls@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 200002 | [179958, 180286, 180885] | [10] | [12, 14] | [10] | [1.75, 2.44, 3.55] |
| w3 | w3_s0p2_pos | a5-rls@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 200002 | [179958, 180286, 180885] | [10] | [12, 14] | [10] | [1.46, 2.11, 3.27] |
| w3 | w3_s0p5_neg | a4@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 500885 | [390398, 393139, 393300] | [10] | [1] | [10] | [1.65, 1.75, 176.31] |
| w3 | w3_s0p5_neg | a4@exact | 3 | `Limit(Gather Merge(Sort(Seq Scan)))` (3) | 500885 | [162666, 163808, 163875] | [500886] | [166372] | [10] | [3232.33, 3435.69, 4516.03] |
| w3 | w3_s0p5_neg | a4@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 500885 | [390398, 393139, 393300] | [10] | [1] | [10] | [0.87, 1.54, 2.0] |
| w3 | w3_s0p5_neg | a5-rls@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 500885 | [390398, 393139, 393300] | [10] | [1] | [10] | [1.35, 1.56, 1.65] |
| w3 | w3_s0p5_neg | a5-rls@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 500885 | [390398, 393139, 393300] | [10] | [1] | [10] | [1.22, 1.3, 1.87] |
| w3 | w3_s0p5_none | a4@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 502206 | [392049, 392840, 397080] | [10] | [3] | [10] | [2.73, 2.77, 193.12] |
| w3 | w3_s0p5_none | a4@exact | 3 | `Limit(Gather Merge(Sort(Seq Scan)))` (3) | 502206 | [163354, 163683, 165450] | [502206] | [165931] | [10] | [3001.18, 3193.7, 4240.77] |
| w3 | w3_s0p5_none | a4@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 502206 | [392049, 392840, 397080] | [10] | [3] | [10] | [2.04, 2.11, 3.0] |
| w3 | w3_s0p5_none | a5-rls@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 502206 | [392049, 392840, 397080] | [10] | [3] | [10] | [1.73, 2.09, 2.96] |
| w3 | w3_s0p5_none | a5-rls@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 502206 | [392049, 392840, 397080] | [10] | [3] | [10] | [1.52, 1.57, 2.84] |
| w3 | w3_s0p5_pos | a4@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 500860 | [393034, 396509, 396547] | [10] | [2] | [10] | [2.19, 2.21, 230.87] |
| w3 | w3_s0p5_pos | a4@exact | 3 | `Limit(Gather Merge(Sort(Seq Scan)))` (3) | 500860 | [163764, 165212, 165228] | [500859] | [166380] | [10] | [2694.66, 2832.55, 3764.96] |
| w3 | w3_s0p5_pos | a4@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 500860 | [393034, 396509, 396547] | [10] | [2] | [10] | [1.85, 2.03, 2.91] |
| w3 | w3_s0p5_pos | a5-rls@default | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 500860 | [393034, 396509, 396547] | [10] | [2] | [10] | [1.67, 1.87, 2.53] |
| w3 | w3_s0p5_pos | a5-rls@iterative | 3 | `Limit(Index Scan[chunks_hnsw])` (3) | 500860 | [393034, 396509, 396547] | [10] | [2] | [10] | [1.35, 1.47, 2.31] |
