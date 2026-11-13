# (b) Costs the measured jobs recorded

Source: `results-raw.tar.gz`: each job's `.meta.json` (load records, environment, and on run jobs one `docker stats` snapshot after the measured pass) and `.scored.jsonl.gz` (every query's latency). Values are the median over jobs, with the range in brackets when the jobs differ.

## Jobs and runners

- Jobs by kind: churn 15, faults 15, run 150.
- CPUs a job saw (`os.cpu_count()`): 4 in 180 jobs.
- Memory a job saw (MemTotal, GiB): 15.6 in 180 jobs.
- Distinct runner names: 180; harness commit: d31238ba002aa0962da1ac3c07f50ca313187e11 (180 jobs); workflow runs: 42330302365 (180 jobs).
- Run jobs that did not finish: 0; run jobs without scores: 0.

## What was recorded, and what was not

- Latency: every query's wall time, embedding excluded. p50 and p99 per job and cell, recomputed here from the raw rows as `bench.report` computes them: 1085 cells against 1085 in the published `cells.json`, largest difference in any median, minimum or maximum 0.000000 ms.
- Memory: one `docker stats` snapshot per run job, after the measured pass. It is not a peak, it is not split by arm or setting (every arm and setting of a cell runs in the same job), and change and fault jobs record none.
- Size: stores that reported one: pgvector. pgvector's record is the table, its inner-product HNSW index and its GIN index (`bench/stores/pgvector.py`), and on W1 and W2 the partitions' total size; the cosine HNSW index built for A7 and the engines' PostgreSQL were not measured. The other stores recorded counts only (below).
- Build time: every store recorded `load_s`; stores that also recorded a separate index time: milvus, pgvector, qdrant. What each covers, from the code: pgvector `load_s` is the COPY and `index_s` the inner-product HNSW build only (the GIN and cosine indexes are built after it, untimed); Qdrant `index_s` runs from the end of the upload until the collection is green with every point counted; Milvus `index_s` runs from the flush until the index covers every row and the collection is loaded; Weaviate recorded the import only; OpenSearch `load_s` is the bulk import and a refresh, and `dls_s` the creation of the document-level-security roles and users.
- Not recorded at all: peak memory, the CPU model, throughput (one client, as registered), and any cost of a permission change.

## Build: load, index and engine times (s)

| workload | store | jobs | store load_s | store index_s | SpiceDB load_s | OpenFGA load_s |
|---|---|---|---|---|---|---|
| w1_enron | milvus | 3 | 25.3 (15.0 to 26.8) | 18.0 (14.0 to 20.0) | 62.7 (44.7 to 73.1) | 121.8 (116.5 to 129.8) |
| w1_enron | opensearch | 3 | 113.8 (77.7 to 134.9) | not recorded | 41.7 (33.1 to 43.9) | 105.6 (86.9 to 161.1) |
| w1_enron | pgvector | 3 | 5.2 (4.3 to 5.2) | 62.7 (56.0 to 73.2) | 45.9 (44.0 to 49.5) | 119.3 (105.4 to 167.4) |
| w1_enron | qdrant | 3 | 33.7 (28.7 to 35.9) | 50.2 (48.1 to 58.1) | 44.8 (42.8 to 46.5) | 119.5 (95.8 to 163.0) |
| w1_enron | weaviate | 3 | 65.0 (61.5 to 84.9) | not recorded | 39.7 (36.4 to 45.9) | 100.8 (98.4 to 119.2) |
| w2_erbac_a | milvus | 3 | 18.6 (14.2 to 21.0) | 18.0 (16.0 to 18.0) | 4.8 (4.8 to 5.8) | 50.6 (50.0 to 51.4) |
| w2_erbac_a | opensearch | 3 | 110.6 (98.2 to 112.8) | not recorded | 5.1 (4.6 to 5.2) | 50.6 (11.1 to 52.9) |
| w2_erbac_a | pgvector | 3 | 3.5 (3.2 to 6.2) | 43.2 (36.3 to 48.2) | 4.7 (3.8 to 5.1) | 46.5 (38.2 to 56.8) |
| w2_erbac_a | qdrant | 3 | 25.3 (23.2 to 26.2) | 44.1 (40.1 to 48.2) | 5.0 (4.8 to 5.1) | 14.6 (14.5 to 63.6) |
| w2_erbac_a | weaviate | 3 | 57.5 (45.3 to 58.3) | not recorded | 5.0 (5.0 to 5.1) | 22.6 (21.9 to 31.6) |
| w2_erbac_b | milvus | 3 | 15.6 (14.1 to 16.8) | 16.0 (14.0 to 20.0) | 7.5 (5.9 to 7.5) | 49.0 (47.4 to 51.9) |
| w2_erbac_b | opensearch | 3 | 107.8 (94.2 to 112.7) | not recorded | 5.2 (4.6 to 5.2) | 58.1 (16.3 to 61.5) |
| w2_erbac_b | pgvector | 3 | 3.5 (3.4 to 3.7) | 35.6 (32.8 to 42.8) | 3.8 (3.7 to 4.2) | 44.7 (8.4 to 58.2) |
| w2_erbac_b | qdrant | 3 | 16.8 (16.4 to 17.7) | 34.1 (32.1 to 40.1) | 3.9 (3.7 to 4.6) | 27.3 (21.5 to 28.1) |
| w2_erbac_b | weaviate | 3 | 57.7 (48.1 to 58.9) | not recorded | 5.3 (5.1 to 5.4) | 23.1 (22.2 to 28.2) |
| w2_tree_a | milvus | 3 | 17.9 (16.0 to 19.8) | 18.0 (18.0 to 24.0) | 6.1 (5.9 to 7.2) | 50.4 (47.6 to 57.8) |
| w2_tree_a | opensearch | 3 | 107.5 (75.2 to 109.7) | not recorded | 5.6 (4.4 to 5.9) | 35.7 (20.4 to 58.2) |
| w2_tree_a | pgvector | 3 | 3.7 (3.4 to 4.6) | 42.9 (40.9 to 45.3) | 5.9 (5.3 to 6.4) | 44.7 (44.4 to 50.0) |
| w2_tree_a | qdrant | 3 | 19.8 (17.0 to 20.2) | 32.4 (32.0 to 40.1) | 6.0 (4.5 to 6.2) | 27.6 (25.1 to 29.2) |
| w2_tree_a | weaviate | 3 | 47.0 (41.1 to 60.0) | not recorded | 5.5 (4.9 to 5.9) | 31.2 (22.1 to 37.0) |
| w2_uniform_a | milvus | 3 | 18.2 (11.6 to 24.9) | 22.0 (14.0 to 34.1) | 14.2 (13.5 to 15.7) | 71.0 (63.1 to 131.1) |
| w2_uniform_a | opensearch | 3 | 107.0 (79.1 to 113.8) | not recorded | 13.3 (10.5 to 14.7) | 74.5 (45.0 to 89.5) |
| w2_uniform_a | pgvector | 3 | 3.5 (3.4 to 3.6) | 46.7 (41.2 to 49.8) | 14.2 (11.3 to 14.3) | 53.4 (50.2 to 54.7) |
| w2_uniform_a | qdrant | 3 | 26.2 (19.3 to 26.6) | 66.1 (64.1 to 72.1) | 13.7 (12.6 to 13.7) | 60.6 (53.4 to 61.1) |
| w2_uniform_a | weaviate | 3 | 58.5 (48.0 to 59.7) | not recorded | 13.9 (13.5 to 14.2) | 36.6 (36.5 to 46.0) |
| w3 | milvus | 21 | 86.5 (62.0 to 107.6) | 168.4 (84.2 to 262.5) | 63.7 (39.0 to 78.8) | 185.2 (92.1 to 287.3) |
| w3 | opensearch | 21 | 412.6 (289.2 to 494.0) | not recorded | 35.3 (25.9 to 39.5) | 127.4 (86.5 to 182.6) |
| w3 | pgvector | 21 | 20.2 (17.7 to 24.8) | 269.7 (217.0 to 336.2) | 37.1 (26.5 to 42.4) | 145.4 (81.0 to 186.9) |
| w3 | qdrant | 21 | 127.5 (92.2 to 155.7) | 130.2 (88.1 to 180.2) | 37.2 (26.6 to 39.1) | 156.7 (87.9 to 187.1) |
| w3 | weaviate | 21 | 290.5 (222.7 to 355.3) | not recorded | 36.5 (27.2 to 39.7) | 132.4 (53.0 to 183.7) |

## Sizes pgvector reported (MiB)

| workload | jobs | table | inner-product HNSW | GIN on principals |
|---|---|---|---|---|
| w1_enron | 3 | 449.4 | 480.0 (480.0 to 480.1) | 12.2 |
| w2_erbac_a | 3 | 312.6 | 390.5 | 0.9 |
| w2_erbac_b | 3 | 312.6 | 390.5 | 0.9 |
| w2_tree_a | 3 | 312.6 | 390.5 | 0.8 |
| w2_uniform_a | 3 | 333.6 | 390.5 | 2.0 |
| w3 | 21 | 1562.9 | 1952.3 | 3.8 |

## Partitions of A6 (pgvector, W1 and W2)

| workload | jobs | partitions | rows | copies (rows per chunk) | size MiB | build s |
|---|---|---|---|---|---|---|
| w1_enron | 3 | 200 | 51610 | 0.21 | 207.6 | 9.5 (8.5 to 11.0) |
| w2_erbac_a | 3 | 39 | 168711 | 0.84 | 602.7 (602.7 to 602.9) | 54.4 (38.1 to 59.1) |
| w2_erbac_b | 3 | 39 | 168711 | 0.84 | 602.8 (602.8 to 602.9) | 37.3 (35.6 to 40.9) |
| w2_tree_a | 3 | 100 | 200000 | 1.00 | 741.2 (740.1 to 742.2) | 46.2 (43.9 to 55.1) |
| w2_uniform_a | 3 | 100 | 497967 | 2.49 | 1775.2 (1775.1 to 1775.3) | 148.7 (115.1 to 151.0) |

## Other numbers the stores recorded at load

| workload | store | field | value |
|---|---|---|---|
| w1_enron | milvus | `index.M` | 16.0 |
| w1_enron | milvus | `index.efConstruction` | 100.0 |
| w1_enron | milvus | `index.indexed_rows` | 250251.0 |
| w1_enron | milvus | `index.pending_index_rows` | 0.0 |
| w1_enron | milvus | `index.total_rows` | 250251.0 |
| w1_enron | opensearch | `dls_roles` | 200.0 |
| w1_enron | opensearch | `dls_s` | 57.5 (43.7 to 62.6) |
| w1_enron | opensearch | `dls_users` | 200.0 |
| w1_enron | opensearch | `documents` | 250251.0 |
| w1_enron | opensearch | `segments` | 18.0 (18.0 to 19.0) |
| w1_enron | qdrant | `indexed_vectors` | 250251.0 |
| w1_enron | qdrant | `points` | 250251.0 |
| w1_enron | qdrant | `segments` | 2.0 |
| w1_enron | weaviate | `objects` | 250251.0 |
| w2_erbac_a | milvus | `index.M` | 16.0 |
| w2_erbac_a | milvus | `index.efConstruction` | 100.0 |
| w2_erbac_a | milvus | `index.indexed_rows` | 200000.0 |
| w2_erbac_a | milvus | `index.pending_index_rows` | 0.0 |
| w2_erbac_a | milvus | `index.total_rows` | 200000.0 |
| w2_erbac_a | opensearch | `dls_roles` | 1039.0 |
| w2_erbac_a | opensearch | `dls_s` | 369.3 (313.4 to 370.4) |
| w2_erbac_a | opensearch | `dls_users` | 1000.0 |
| w2_erbac_a | opensearch | `documents` | 200000.0 |
| w2_erbac_a | opensearch | `segments` | 17.0 |
| w2_erbac_a | qdrant | `indexed_vectors` | 200000.0 |
| w2_erbac_a | qdrant | `points` | 200000.0 |
| w2_erbac_a | qdrant | `segments` | 2.0 |
| w2_erbac_a | weaviate | `objects` | 200000.0 |
| w2_erbac_b | milvus | `index.M` | 16.0 |
| w2_erbac_b | milvus | `index.efConstruction` | 100.0 |
| w2_erbac_b | milvus | `index.indexed_rows` | 200000.0 |
| w2_erbac_b | milvus | `index.pending_index_rows` | 0.0 |
| w2_erbac_b | milvus | `index.total_rows` | 200000.0 |
| w2_erbac_b | opensearch | `dls_roles` | 1039.0 |
| w2_erbac_b | opensearch | `dls_s` | 365.5 (311.8 to 366.1) |
| w2_erbac_b | opensearch | `dls_users` | 1000.0 |
| w2_erbac_b | opensearch | `documents` | 200000.0 |
| w2_erbac_b | opensearch | `segments` | 17.0 |
| w2_erbac_b | qdrant | `indexed_vectors` | 200000.0 |
| w2_erbac_b | qdrant | `points` | 200000.0 |
| w2_erbac_b | qdrant | `segments` | 2.0 |
| w2_erbac_b | weaviate | `objects` | 200000.0 |
| w2_tree_a | milvus | `index.M` | 16.0 |
| w2_tree_a | milvus | `index.efConstruction` | 100.0 |
| w2_tree_a | milvus | `index.indexed_rows` | 200000.0 |
| w2_tree_a | milvus | `index.pending_index_rows` | 0.0 |
| w2_tree_a | milvus | `index.total_rows` | 200000.0 |
| w2_tree_a | opensearch | `dls_roles` | 1100.0 |
| w2_tree_a | opensearch | `dls_s` | 353.2 (251.4 to 369.7) |
| w2_tree_a | opensearch | `dls_users` | 1000.0 |
| w2_tree_a | opensearch | `documents` | 200000.0 |
| w2_tree_a | opensearch | `segments` | 16.0 (16.0 to 17.0) |
| w2_tree_a | qdrant | `indexed_vectors` | 200000.0 |
| w2_tree_a | qdrant | `points` | 200000.0 |
| w2_tree_a | qdrant | `segments` | 2.0 |
| w2_tree_a | weaviate | `objects` | 200000.0 |
| w2_uniform_a | milvus | `index.M` | 16.0 |
| w2_uniform_a | milvus | `index.efConstruction` | 100.0 |
| w2_uniform_a | milvus | `index.indexed_rows` | 200000.0 |
| w2_uniform_a | milvus | `index.pending_index_rows` | 0.0 |
| w2_uniform_a | milvus | `index.total_rows` | 200000.0 |
| w2_uniform_a | opensearch | `dls_roles` | 1100.0 |
| w2_uniform_a | opensearch | `dls_s` | 352.6 (245.6 to 364.2) |
| w2_uniform_a | opensearch | `dls_users` | 1000.0 |
| w2_uniform_a | opensearch | `documents` | 200000.0 |
| w2_uniform_a | opensearch | `segments` | 16.0 (16.0 to 17.0) |
| w2_uniform_a | qdrant | `indexed_vectors` | 200000.0 |
| w2_uniform_a | qdrant | `points` | 200000.0 |
| w2_uniform_a | qdrant | `segments` | 2.0 |
| w2_uniform_a | weaviate | `objects` | 200000.0 |
| w3 | milvus | `index.M` | 16.0 |
| w3 | milvus | `index.efConstruction` | 100.0 |
| w3 | milvus | `index.indexed_rows` | 1000000.0 |
| w3 | milvus | `index.pending_index_rows` | 0.0 |
| w3 | milvus | `index.total_rows` | 1000000.0 |
| w3 | opensearch | `dls_roles` | 2500.0 |
| w3 | opensearch | `dls_s` | 600.5 (437.3 to 730.9) |
| w3 | opensearch | `dls_users` | 1500.0 |
| w3 | opensearch | `documents` | 1000000.0 |
| w3 | opensearch | `segments` | 31.0 (22.0 to 31.0) |
| w3 | qdrant | `indexed_vectors` | 1000000.0 |
| w3 | qdrant | `points` | 1000000.0 |
| w3 | qdrant | `segments` | 3.0 |
| w3 | weaviate | `objects` | 1000000.0 |

## Container memory after the measured pass (MiB)

| workload | share | store | jobs | store container | SpiceDB | OpenFGA | engines' PostgreSQL | all containers |
|---|---|---|---|---|---|---|---|---|
| w1_enron |  | milvus | 3 | 797 (797 to 799) | 49 (46 to 59) | 36 (35 to 39) | 389 (371 to 390) | 1272 (1255 to 1286) |
| w1_enron |  | opensearch | 3 | 5334 (5316 to 5340) | 59 (46 to 61) | 36 (35 to 36) | 384 (375 to 396) | 5808 (5788 to 5827) |
| w1_enron |  | pgvector | 3 | 1814 (1812 to 1815) | 61 (61 to 81) | 33 (30 to 36) | 350 (332 to 393) | 2282 (2243 to 2299) |
| w1_enron |  | qdrant | 3 | 224 (222 to 230) | 56 (49 to 67) | 36 (35 to 36) | 382 (378 to 386) | 697 (691 to 720) |
| w1_enron |  | weaviate | 3 | 1085 (1024 to 1087) | 57 (49 to 62) | 36 (35 to 39) | 383 (375 to 384) | 1553 (1503 to 1567) |
| w2_erbac_a |  | milvus | 3 | 660 (653 to 666) | 296 (69 to 345) | 35 (35 to 37) | 339 (334 to 350) | 1340 (1093 to 1393) |
| w2_erbac_a |  | opensearch | 3 | 5260 (5247 to 5272) | 65 (61 to 71) | 35 (35 to 39) | 326 (324 to 345) | 5683 (5679 to 5724) |
| w2_erbac_a |  | pgvector | 3 | 1897 | 418 (83 to 554) | 35 (30 to 36) | 340 (290 to 340) | 2636 (2357 to 2830) |
| w2_erbac_a |  | qdrant | 3 | 154 (153 to 155) | 115 (79 to 277) | 35 (33 to 39) | 337 (280 to 340) | 646 (548 to 810) |
| w2_erbac_a |  | weaviate | 3 | 888 (884 to 893) | 74 (66 to 255) | 35 (35 to 37) | 340 (288 to 344) | 1338 (1278 to 1527) |
| w2_erbac_b |  | milvus | 3 | 659 (656 to 664) | 354 (82 to 468) | 35 (35 to 37) | 294 (285 to 343) | 1400 (1069 to 1449) |
| w2_erbac_b |  | opensearch | 3 | 5251 (5234 to 5253) | 72 (69 to 76) | 36 (35 to 36) | 299 (288 to 328) | 5665 (5647 to 5672) |
| w2_erbac_b |  | pgvector | 3 | 1895 (1890 to 1898) | 554 (342 to 753) | 34 (31 to 35) | 289 (280 to 289) | 2769 (2558 to 2970) |
| w2_erbac_b |  | qdrant | 3 | 154 (153 to 154) | 159 (90 to 430) | 35 (34 to 35) | 338 (286 to 348) | 689 (566 to 968) |
| w2_erbac_b |  | weaviate | 3 | 879 (878 to 893) | 77 (66 to 282) | 35 (34 to 36) | 284 (279 to 288) | 1281 (1279 to 1476) |
| w2_tree_a |  | milvus | 3 | 660 (651 to 668) | 71 (62 to 345) | 36 (35 to 36) | 336 (336 to 338) | 1106 (1104 to 1370) |
| w2_tree_a |  | opensearch | 3 | 5216 (5199 to 5241) | 69 (63 to 70) | 36 (35 to 38) | 336 (334 to 338) | 5653 (5640 to 5688) |
| w2_tree_a |  | pgvector | 3 | 2034 (2033 to 2036) | 246 (72 to 385) | 36 (35 to 36) | 336 (334 to 338) | 2656 (2480 to 2790) |
| w2_tree_a |  | qdrant | 3 | 150 (150 to 151) | 232 (77 to 464) | 37 (36 to 38) | 340 (335 to 341) | 754 (608 to 994) |
| w2_tree_a |  | weaviate | 3 | 886 (883 to 896) | 80 (65 to 327) | 36 (35 to 38) | 337 (336 to 339) | 1336 (1336 to 1593) |
| w2_uniform_a |  | milvus | 3 | 666 (658 to 668) | 68 (65 to 80) | 36 (36 to 42) | 367 (364 to 373) | 1143 (1135 to 1150) |
| w2_uniform_a |  | opensearch | 3 | 5256 (5225 to 5280) | 74 (63 to 74) | 37 (36 to 38) | 368 (367 to 371) | 5741 (5695 to 5758) |
| w2_uniform_a |  | pgvector | 3 | 2269 (2267 to 2271) | 244 (63 to 353) | 36 (35 to 38) | 357 (356 to 370) | 2906 (2729 to 3030) |
| w2_uniform_a |  | qdrant | 3 | 173 (173 to 174) | 80 (72 to 345) | 37 (36 to 38) | 374 (370 to 376) | 666 (654 to 933) |
| w2_uniform_a |  | weaviate | 3 | 892 (886 to 894) | 74 (64 to 236) | 36 (36 to 39) | 368 (364 to 370) | 1368 (1358 to 1540) |
| w3 | s0p001 | milvus | 3 | 2104 (2099 to 2114) | 74 (58 to 78) | 42 (42 to 45) | 387 (345 to 390) | 2611 (2555 to 2619) |
| w3 | s0p001 | opensearch | 3 | 6584 (6566 to 6595) | 69 (56 to 69) | 39 (37 to 42) | 366 (366 to 381) | 7058 (7031 to 7086) |
| w3 | s0p001 | pgvector | 3 | 2261 (2256 to 2291) | 75 (63 to 150) | 39 (37 to 40) | 370 (367 to 374) | 2777 (2735 to 2817) |
| w3 | s0p001 | qdrant | 3 | 427 (423 to 456) | 65 (55 to 82) | 36 (35 to 39) | 395 (390 to 396) | 941 (914 to 950) |
| w3 | s0p001 | weaviate | 3 | 3233 (3042 to 3397) | 63 (51 to 66) | 38 (36 to 38) | 395 (395 to 397) | 3731 (3543 to 3882) |
| w3 | s0p01 | milvus | 3 | 2135 (2129 to 2137) | 63 (63 to 80) | 42 (41 to 46) | 338 (322 to 341) | 2587 (2558 to 2599) |
| w3 | s0p01 | opensearch | 3 | 6622 (6503 to 6641) | 76 (62 to 79) | 39 (39 to 45) | 361 (354 to 384) | 7100 (6997 to 7115) |
| w3 | s0p01 | pgvector | 3 | 2274 (2221 to 2278) | 308 (80 to 473) | 37 (35 to 38) | 313 (312 to 344) | 2910 (2710 to 3100) |
| w3 | s0p01 | qdrant | 3 | 456 (422 to 459) | 69 (58 to 85) | 35 (35 to 37) | 340 (338 to 346) | 902 (857 to 926) |
| w3 | s0p01 | weaviate | 3 | 3826 (3053 to 3920) | 73 (64 to 255) | 36 (35 to 40) | 341 (340 to 398) | 4277 (3494 to 4614) |
| w3 | s0p05 | milvus | 3 | 2137 (2124 to 2165) | 77 (69 to 87) | 43 (40 to 45) | 344 (340 to 344) | 2604 (2593 to 2625) |
| w3 | s0p05 | opensearch | 3 | 6680 (6550 to 6693) | 73 (55 to 82) | 38 (37 to 39) | 329 (324 to 377) | 7131 (6973 to 7180) |
| w3 | s0p05 | pgvector | 3 | 2316 (2272 to 2355) | 550 (87 to 632) | 39 (32 to 40) | 316 (313 to 324) | 3169 (2808 to 3305) |
| w3 | s0p05 | qdrant | 3 | 428 (422 to 431) | 80 (64 to 95) | 35 (32 to 37) | 346 (323 to 347) | 880 (874 to 892) |
| w3 | s0p05 | weaviate | 3 | 3679 (3663 to 4100) | 76 (55 to 77) | 35 (34 to 40) | 345 (342 to 345) | 4137 (4105 to 4555) |
| w3 | s0p2 | milvus | 3 | 2136 (2116 to 2182) | 100 (92 to 272) | 43 (42 to 45) | 342 (340 to 350) | 2667 (2601 to 2796) |
| w3 | s0p2 | opensearch | 3 | 6637 (6545 to 6672) | 85 (75 to 87) | 40 (40 to 43) | 334 (317 to 340) | 7099 (6983 to 7140) |
| w3 | s0p2 | pgvector | 3 | 2318 (2307 to 2340) | 210 (101 to 769) | 38 (25 to 40) | 316 (290 to 329) | 2873 (2812 to 3405) |
| w3 | s0p2 | qdrant | 3 | 869 (868 to 901) | 106 (85 to 238) | 35 (33 to 38) | 335 (320 to 336) | 1360 (1329 to 1482) |
| w3 | s0p2 | weaviate | 3 | 3636 (3452 to 4092) | 74 (68 to 92) | 36 (35 to 39) | 342 (330 to 350) | 4108 (3911 to 4534) |
| w3 | s0p5 | milvus | 3 | 2146 (2126 to 2166) | 116 (109 to 122) | 44 (43 to 45) | 346 (325 to 350) | 2652 (2632 to 2659) |
| w3 | s0p5 | opensearch | 3 | 6688 (6687 to 6698) | 110 (93 to 110) | 40 (36 to 42) | 301 (290 to 306) | 7140 (7119 to 7148) |
| w3 | s0p5 | pgvector | 3 | 2276 (2253 to 2315) | 215 (120 to 930) | 41 (25 to 41) | 321 (264 to 354) | 2856 (2832 to 3473) |
| w3 | s0p5 | qdrant | 3 | 1526 (1493 to 1559) | 114 (103 to 124) | 36 (33 to 38) | 356 (336 to 357) | 2013 (2010 to 2058) |
| w3 | s0p5 | weaviate | 3 | 4498 (4042 to 4527) | 126 (116 to 608) | 37 (35 to 38) | 355 (340 to 361) | 5030 (4558 to 5501) |

## p99 latency (ms)

Each cell's p99 is computed per job; the tables give the median over its jobs (three seeds). The range over jobs and the p50 are in `costs.json`.

### w1_enron

| arm | pgvector | qdrant | milvus | weaviate | opensearch |
|---|---|---|---|---|---|
| a0 | 3.4 |  |  |  |  |
| a1-fga | 34.5 | 35.1 | 37.1 | 27.6 | 28.5 |
| a1-spicedb | 7.5 | 5.3 | 6.8 | 4.4 | 8.0 |
| a2-fga-x10 | 137.4 | 168.8 | 139.3 | 156.7 | 98.7 |
| a2-fga-x3 | 39.3 | 42.6 | 45.1 | 34.5 | 35.9 |
| a2-spicedb-x10 | 12.5 | 12.1 | 13.3 | 9.6 | 15.5 |
| a2-spicedb-x3 | 8.5 | 6.8 | 8.6 | 7.3 | 10.3 |
| a3-spicedb@acorn |  | 180.4 |  |  |  |
| a3-spicedb@default | 142.3 | 185.4 | 151.8 | 110.1 | 121.1 |
| a3-spicedb@iterative | 145.9 |  | 215.3 |  |  |
| a3-spicedb@pathseer |  |  |  | 110.2 |  |
| a4@acorn |  | 1.4 |  |  |  |
| a4@default | 3.1 | 1.4 | 3.2 | 1.6 | 2.6 |
| a4@iterative | 23.1 |  | 226.8 |  |  |
| a4@pathseer |  |  |  | 1.5 |  |
| a5-dls |  |  |  |  | 280.3 |
| a5-rls@default | 3.3 |  |  |  |  |
| a5-rls@iterative | 24.0 |  |  |  |  |
| a6-partition | 1.6 |  |  |  |  |
| a7-wardowl | 2176.1 | 212.6 |  |  |  |

### w2_erbac_a

| arm | pgvector | qdrant | milvus | weaviate | opensearch |
|---|---|---|---|---|---|
| a0 | 39.6 |  |  |  |  |
| a1-fga | 29.7 | 35.0 | 40.0 | 34.1 | 49.3 |
| a1-spicedb | 6.8 | 6.4 | 10.3 | 6.8 | 14.1 |
| a2-fga-x10 | 107.7 | 125.0 | 113.0 | 120.2 | 131.9 |
| a2-fga-x3 | 37.0 | 46.1 | 46.2 | 48.3 | 57.4 |
| a2-spicedb-x10 | 10.6 | 12.2 | 14.6 | 12.9 | 20.3 |
| a2-spicedb-x3 | 8.1 | 7.5 | 9.6 | 8.2 | 15.9 |
| a3-spicedb@acorn |  | 2422.8 |  |  |  |
| a3-spicedb@default | 1441.2 | 2454.4 | 1921.7 | 2657.4 | 2477.4 |
| a3-spicedb@iterative | 1462.1 |  | 1920.1 |  |  |
| a3-spicedb@pathseer |  |  |  | 2668.0 |  |
| a4@acorn |  | 11.0 |  |  |  |
| a4@default | 3.2 | 3.0 | 5.2 | 10.4 | 9.6 |
| a4@iterative | 19.6 |  | 31.3 |  |  |
| a4@pathseer |  |  |  | 10.7 |  |
| a5-dls |  |  |  |  | 339.0 |
| a5-rls@default | 3.2 |  |  |  |  |
| a5-rls@iterative | 19.2 |  |  |  |  |
| a6-partition | 11.3 |  |  |  |  |
| a7-wardowl | 188.1 | 258.0 |  |  |  |

### w2_erbac_b

| arm | pgvector | qdrant | milvus | weaviate | opensearch |
|---|---|---|---|---|---|
| a0 | 52.0 |  |  |  |  |
| a1-fga | 26.0 | 25.6 | 31.1 | 39.5 | 43.4 |
| a1-spicedb | 6.4 | 6.4 | 7.8 | 8.0 | 14.0 |
| a2-fga-x10 | 89.0 | 109.3 | 122.2 | 126.2 | 117.5 |
| a2-fga-x3 | 30.0 | 29.5 | 37.6 | 47.4 | 52.2 |
| a2-spicedb-x10 | 9.5 | 10.7 | 13.7 | 14.4 | 20.4 |
| a2-spicedb-x3 | 6.8 | 7.0 | 9.6 | 10.3 | 15.0 |
| a3-spicedb@acorn |  | 2054.4 |  |  |  |
| a3-spicedb@default | 1997.9 | 2083.0 | 2837.0 | 4756.1 | 4207.2 |
| a3-spicedb@iterative | 2141.7 |  | 2619.1 |  |  |
| a3-spicedb@pathseer |  |  |  | 4874.3 |  |
| a4@acorn |  | 7.4 |  |  |  |
| a4@default | 3.0 | 1.7 | 5.1 | 12.6 | 9.6 |
| a4@iterative | 12.4 |  | 5.4 |  |  |
| a4@pathseer |  |  |  | 12.1 |  |
| a5-dls |  |  |  |  | 329.0 |
| a5-rls@default | 2.7 |  |  |  |  |
| a5-rls@iterative | 11.9 |  |  |  |  |
| a6-partition | 21.0 |  |  |  |  |
| a7-wardowl | 213.4 | 205.0 |  |  |  |

### w2_tree_a

| arm | pgvector | qdrant | milvus | weaviate | opensearch |
|---|---|---|---|---|---|
| a0 | 15.8 |  |  |  |  |
| a1-fga | 30.2 | 29.1 | 38.9 | 29.9 | 39.7 |
| a1-spicedb | 5.9 | 4.1 | 8.7 | 6.3 | 14.2 |
| a2-fga-x10 | 99.1 | 123.8 | 124.2 | 134.9 | 105.0 |
| a2-fga-x3 | 40.4 | 38.0 | 50.7 | 36.9 | 50.8 |
| a2-spicedb-x10 | 10.3 | 8.7 | 13.9 | 13.7 | 20.0 |
| a2-spicedb-x3 | 7.4 | 5.8 | 9.7 | 7.2 | 11.8 |
| a3-spicedb@acorn |  | 511.8 |  |  |  |
| a3-spicedb@default | 467.1 | 527.4 | 583.0 | 535.1 | 569.0 |
| a3-spicedb@iterative | 463.0 |  | 585.8 |  |  |
| a3-spicedb@pathseer |  |  |  | 540.2 |  |
| a4@acorn |  | 4.4 |  |  |  |
| a4@default | 2.9 | 2.5 | 5.5 | 5.7 | 6.1 |
| a4@iterative | 10.5 |  | 4.7 |  |  |
| a4@pathseer |  |  |  | 5.8 |  |
| a5-dls |  |  |  |  | 305.3 |
| a5-rls@default | 3.1 |  |  |  |  |
| a5-rls@iterative | 11.2 |  |  |  |  |
| a6-partition | 7.4 |  |  |  |  |
| a7-wardowl | 169.1 | 186.0 |  |  |  |

### w2_uniform_a

| arm | pgvector | qdrant | milvus | weaviate | opensearch |
|---|---|---|---|---|---|
| a0 | 24.1 |  |  |  |  |
| a1-fga | 39.6 | 35.5 | 42.2 | 37.2 | 43.4 |
| a1-spicedb | 7.8 | 6.0 | 8.9 | 6.8 | 13.0 |
| a2-fga-x10 | 115.9 | 135.1 | 134.2 | 136.8 | 114.2 |
| a2-fga-x3 | 54.4 | 49.7 | 50.0 | 49.5 | 51.8 |
| a2-spicedb-x10 | 12.8 | 11.5 | 15.2 | 13.0 | 23.0 |
| a2-spicedb-x3 | 9.1 | 7.8 | 10.9 | 9.1 | 14.9 |
| a3-spicedb@acorn |  | 1247.3 |  |  |  |
| a3-spicedb@default | 1275.0 | 1244.7 | 1263.3 | 1433.7 | 887.7 |
| a3-spicedb@iterative | 1272.6 |  | 1248.8 |  |  |
| a3-spicedb@pathseer |  |  |  | 1411.0 |  |
| a4@acorn |  | 24.8 |  |  |  |
| a4@default | 4.0 | 3.3 | 5.7 | 7.2 | 7.8 |
| a4@iterative | 27.0 |  | 14.4 |  |  |
| a4@pathseer |  |  |  | 7.7 |  |
| a5-dls |  |  |  |  | 306.0 |
| a5-rls@default | 3.7 |  |  |  |  |
| a5-rls@iterative | 27.3 |  |  |  |  |
| a6-partition | 7.7 |  |  |  |  |
| a7-wardowl | 247.2 | 268.6 |  |  |  |

### w3

Per store, the median over the three correlation layouts of each cell's p99.

#### pgvector

| arm | 0p001 | 0p01 | 0p05 | 0p2 | 0p5 |
|---|---|---|---|---|---|
| a0 | 7.2 | 19.4 | 96.9 | 2211.7 | 3257.1 |
| a1-fga | 39.7 | 25.1 | 29.5 | 41.6 | 30.1 |
| a1-spicedb | 8.9 | 6.6 | 7.3 | 9.0 | 7.8 |
| a2-fga-x10 | 133.2 | 127.0 | 140.4 | 148.7 | 129.3 |
| a2-fga-x3 | 50.5 | 41.4 | 38.1 | 51.9 | 37.3 |
| a2-spicedb-x10 | 19.2 | 13.0 | 13.5 | 18.1 | 14.5 |
| a2-spicedb-x3 | 9.7 | 6.8 | 8.9 | 9.8 | 8.3 |
| a3-spicedb@default | 185.9 | 396.6 | 1718.5 | 14488.8 | 22370.5 |
| a3-spicedb@iterative | 186.7 | 452.8 | 1860.2 | 14514.3 | 22333.8 |
| a4@default | 5.5 | 4.2 | 4.1 | 4.7 | 5.1 |
| a4@iterative | 87.0 | 96.0 | 54.6 | 37.7 | 11.1 |
| a5-rls@default | 4.9 | 3.9 | 4.2 | 6.3 | 5.6 |
| a5-rls@iterative | 116.7 | 135.5 | 79.1 | 49.2 | 21.8 |
| a7-wardowl | 267.8 | 258.5 | 341.6 | 696.4 | 1116.5 |

#### qdrant

| arm | 0p001 | 0p01 | 0p05 | 0p2 | 0p5 |
|---|---|---|---|---|---|
| a1-fga | 36.0 | 36.5 | 35.9 | 35.9 | 26.7 |
| a1-spicedb | 5.7 | 6.7 | 5.9 | 6.8 | 5.5 |
| a2-fga-x10 | 148.4 | 157.6 | 141.4 | 154.9 | 133.1 |
| a2-fga-x3 | 44.7 | 47.4 | 44.8 | 44.6 | 34.3 |
| a2-spicedb-x10 | 12.2 | 13.3 | 12.3 | 13.1 | 10.0 |
| a2-spicedb-x3 | 7.2 | 7.3 | 6.7 | 7.9 | 6.8 |
| a3-spicedb@acorn | 187.3 | 903.3 | 3713.9 | 14287.0 | 22736.6 |
| a3-spicedb@default | 186.1 | 881.5 | 3679.0 | 14280.9 | 22783.2 |
| a4@acorn | 1.5 | 3.9 | 7.7 | 8.7 | 8.0 |
| a4@default | 1.6 | 3.9 | 2.2 | 2.5 | 2.6 |
| a7-wardowl | 295.6 | 339.1 | 448.3 | 659.2 | 808.7 |

#### milvus

| arm | 0p001 | 0p01 | 0p05 | 0p2 | 0p5 |
|---|---|---|---|---|---|
| a1-fga | 40.3 | 39.9 | 30.9 | 27.3 | 38.9 |
| a1-spicedb | 9.2 | 9.5 | 8.3 | 9.0 | 10.2 |
| a2-fga-x10 | 145.6 | 151.6 | 136.3 | 130.7 | 139.1 |
| a2-fga-x3 | 48.7 | 43.8 | 39.6 | 37.3 | 48.0 |
| a2-spicedb-x10 | 17.5 | 14.7 | 13.8 | 16.2 | 20.8 |
| a2-spicedb-x3 | 9.9 | 9.9 | 8.2 | 9.2 | 9.7 |
| a3-spicedb@default | 187.4 | 643.3 | 2283.4 | 8568.2 | 27413.6 |
| a3-spicedb@iterative | 767.6 | 1057.8 | 2485.9 | 11714.6 | 29411.4 |
| a4@default | 4.9 | 5.8 | 11.6 | 6.6 | 7.2 |
| a4@iterative | 338.2 | 58.7 | 14.7 | 7.0 | 5.6 |

#### weaviate

| arm | 0p001 | 0p01 | 0p05 | 0p2 | 0p5 |
|---|---|---|---|---|---|
| a1-fga | 35.3 | 28.8 | 22.4 | 34.7 | 26.9 |
| a1-spicedb | 6.2 | 6.3 | 6.4 | 6.5 | 5.5 |
| a2-fga-x10 | 137.0 | 178.4 | 118.7 | 132.3 | 150.2 |
| a2-fga-x3 | 47.0 | 37.2 | 27.9 | 45.5 | 31.8 |
| a2-spicedb-x10 | 13.4 | 11.9 | 8.3 | 13.1 | 10.5 |
| a2-spicedb-x3 | 7.8 | 8.3 | 6.2 | 7.9 | 7.3 |
| a3-spicedb@default | 205.5 | 629.5 | 2077.3 | 16041.7 | 19095.0 |
| a3-spicedb@pathseer | 207.6 | 625.9 | 2001.0 | 16089.2 | 21050.9 |
| a4@default | 2.5 | 7.5 | 5.2 | 9.8 | 10.5 |
| a4@pathseer | 2.5 | 7.3 | 10.5 | 8.5 | 9.4 |

#### opensearch

| arm | 0p001 | 0p01 | 0p05 | 0p2 | 0p5 |
|---|---|---|---|---|---|
| a1-fga | 42.4 | 33.2 | 33.8 | 32.6 | 47.1 |
| a1-spicedb | 19.7 | 10.8 | 11.6 | 14.8 | 16.5 |
| a2-fga-x10 | 126.5 | 108.6 | 116.5 | 126.0 | 124.6 |
| a2-fga-x3 | 51.9 | 38.7 | 41.6 | 40.1 | 57.4 |
| a2-spicedb-x10 | 25.0 | 19.0 | 22.0 | 22.5 | 35.3 |
| a2-spicedb-x3 | 17.0 | 13.4 | 16.8 | 14.9 | 19.2 |
| a3-spicedb@default | 214.4 | 626.2 | 2716.3 | 8781.1 | 35792.5 |
| a4@default | 3.7 | 6.9 | 14.3 | 23.8 | 38.2 |
| a5-dls | 290.3 | 232.9 | 286.4 | 296.3 | 366.1 |

