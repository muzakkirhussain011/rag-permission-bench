# Digest of results-v1 (bench.report output)

Coverage: 1085 cells, seeds planned 3, cells short of seeds 0, jobs without scores 0. Exact control (A0) faults: 0.

All measured cells: 3,478,320 queries; outside the readable set 0; errors 0; empty answers 1,225,154; calls over 30 s 1,056.

Cells with any chunk outside the readable set: 0

Errors by arm, store and workload: none

## Hypotheses

### H1: supported

10 parts: {'supported': 10}

- store=pgvector, arm=a1-fga: [0.235, 0.297] supported
- store=pgvector, arm=a1-spicedb: [0.236, 0.298] supported
- store=qdrant, arm=a1-fga: [0.231, 0.295] supported
- store=qdrant, arm=a1-spicedb: [0.230, 0.295] supported
- store=milvus, arm=a1-fga: [0.229, 0.294] supported
- store=milvus, arm=a1-spicedb: [0.229, 0.295] supported
- store=weaviate, arm=a1-fga: [0.227, 0.290] supported
- store=weaviate, arm=a1-spicedb: [0.228, 0.290] supported
- store=opensearch, arm=a1-fga: [0.241, 0.306] supported
- store=opensearch, arm=a1-spicedb: [0.241, 0.305] supported

### H2: supported

10 parts: {'supported': 10}

- store=pgvector, arm=a2-fga-x10: [0.427, 0.507] supported
- store=pgvector, arm=a2-spicedb-x10: [0.426, 0.505] supported
- store=qdrant, arm=a2-fga-x10: [0.415, 0.499] supported
- store=qdrant, arm=a2-spicedb-x10: [0.416, 0.497] supported
- store=milvus, arm=a2-fga-x10: [0.414, 0.496] supported
- store=milvus, arm=a2-spicedb-x10: [0.415, 0.497] supported
- store=weaviate, arm=a2-fga-x10: [0.410, 0.493] supported
- store=weaviate, arm=a2-spicedb-x10: [0.410, 0.492] supported
- store=opensearch, arm=a2-fga-x10: [0.428, 0.512] supported
- store=opensearch, arm=a2-spicedb-x10: [0.428, 0.511] supported

### H3: supported

90 parts: {'supported': 90}

- store=pgvector, arm=a1-fga, share=0p001: [-0.008, -0.002] supported
- store=pgvector, arm=a1-spicedb, share=0p001: [-0.008, -0.002] supported
- store=pgvector, arm=a2-fga-x3, share=0p001: [-0.015, -0.005] supported
- store=pgvector, arm=a2-fga-x10, share=0p001: [-0.036, -0.015] supported
- store=pgvector, arm=a2-spicedb-x3, share=0p001: [-0.015, -0.005] supported
- store=pgvector, arm=a2-spicedb-x10, share=0p001: [-0.036, -0.016] supported
- store=pgvector, arm=a1-fga, share=0p01: [-0.049, -0.027] supported
- store=pgvector, arm=a1-spicedb, share=0p01: [-0.049, -0.027] supported
- store=pgvector, arm=a2-fga-x3, share=0p01: [-0.098, -0.065] supported
- store=pgvector, arm=a2-fga-x10, share=0p01: [-0.184, -0.135] supported
- store=pgvector, arm=a2-spicedb-x3, share=0p01: [-0.098, -0.065] supported
- store=pgvector, arm=a2-spicedb-x10, share=0p01: [-0.183, -0.135] supported
- store=pgvector, arm=a1-fga, share=0p05: [-0.186, -0.132] supported
- store=pgvector, arm=a1-spicedb, share=0p05: [-0.185, -0.133] supported
- store=pgvector, arm=a2-fga-x3, share=0p05: [-0.314, -0.245] supported
- store=pgvector, arm=a2-fga-x10, share=0p05: [-0.451, -0.379] supported
- store=pgvector, arm=a2-spicedb-x3, share=0p05: [-0.314, -0.245] supported
- store=pgvector, arm=a2-spicedb-x10, share=0p05: [-0.450, -0.379] supported
- store=qdrant, arm=a1-fga, share=0p001: [-0.008, -0.001] supported
- store=qdrant, arm=a1-spicedb, share=0p001: [-0.008, -0.001] supported
- store=qdrant, arm=a2-fga-x3, share=0p001: [-0.015, -0.005] supported
- store=qdrant, arm=a2-fga-x10, share=0p001: [-0.037, -0.017] supported
- store=qdrant, arm=a2-spicedb-x3, share=0p001: [-0.015, -0.005] supported
- store=qdrant, arm=a2-spicedb-x10, share=0p001: [-0.037, -0.017] supported
- store=qdrant, arm=a1-fga, share=0p01: [-0.047, -0.027] supported
- store=qdrant, arm=a1-spicedb, share=0p01: [-0.047, -0.027] supported
- store=qdrant, arm=a2-fga-x3, share=0p01: [-0.100, -0.068] supported
- store=qdrant, arm=a2-fga-x10, share=0p01: [-0.196, -0.147] supported
- store=qdrant, arm=a2-spicedb-x3, share=0p01: [-0.100, -0.068] supported
- store=qdrant, arm=a2-spicedb-x10, share=0p01: [-0.197, -0.148] supported
- store=qdrant, arm=a1-fga, share=0p05: [-0.186, -0.132] supported
- store=qdrant, arm=a1-spicedb, share=0p05: [-0.185, -0.133] supported
- store=qdrant, arm=a2-fga-x3, share=0p05: [-0.326, -0.255] supported
- store=qdrant, arm=a2-fga-x10, share=0p05: [-0.477, -0.404] supported
- store=qdrant, arm=a2-spicedb-x3, share=0p05: [-0.324, -0.254] supported
- store=qdrant, arm=a2-spicedb-x10, share=0p05: [-0.476, -0.404] supported
- store=milvus, arm=a1-fga, share=0p001: [-0.007, -0.001] supported
- store=milvus, arm=a1-spicedb, share=0p001: [-0.007, -0.001] supported
- store=milvus, arm=a2-fga-x3, share=0p001: [-0.015, -0.005] supported
- store=milvus, arm=a2-fga-x10, share=0p001: [-0.037, -0.017] supported
- store=milvus, arm=a2-spicedb-x3, share=0p001: [-0.015, -0.005] supported
- store=milvus, arm=a2-spicedb-x10, share=0p001: [-0.038, -0.017] supported
- store=milvus, arm=a1-fga, share=0p01: [-0.048, -0.027] supported
- store=milvus, arm=a1-spicedb, share=0p01: [-0.048, -0.027] supported
- store=milvus, arm=a2-fga-x3, share=0p01: [-0.101, -0.069] supported
- store=milvus, arm=a2-fga-x10, share=0p01: [-0.199, -0.150] supported
- store=milvus, arm=a2-spicedb-x3, share=0p01: [-0.101, -0.069] supported
- store=milvus, arm=a2-spicedb-x10, share=0p01: [-0.200, -0.149] supported
- store=milvus, arm=a1-fga, share=0p05: [-0.182, -0.130] supported
- store=milvus, arm=a1-spicedb, share=0p05: [-0.183, -0.131] supported
- store=milvus, arm=a2-fga-x3, share=0p05: [-0.323, -0.254] supported
- store=milvus, arm=a2-fga-x10, share=0p05: [-0.478, -0.409] supported
- store=milvus, arm=a2-spicedb-x3, share=0p05: [-0.324, -0.253] supported
- store=milvus, arm=a2-spicedb-x10, share=0p05: [-0.480, -0.410] supported
- store=weaviate, arm=a1-fga, share=0p001: [-0.008, -0.002] supported
- store=weaviate, arm=a1-spicedb, share=0p001: [-0.008, -0.002] supported
- store=weaviate, arm=a2-fga-x3, share=0p001: [-0.015, -0.005] supported
- store=weaviate, arm=a2-fga-x10, share=0p001: [-0.035, -0.016] supported
- store=weaviate, arm=a2-spicedb-x3, share=0p001: [-0.015, -0.005] supported
- store=weaviate, arm=a2-spicedb-x10, share=0p001: [-0.035, -0.016] supported
- store=weaviate, arm=a1-fga, share=0p01: [-0.047, -0.026] supported
- store=weaviate, arm=a1-spicedb, share=0p01: [-0.047, -0.026] supported
- store=weaviate, arm=a2-fga-x3, share=0p01: [-0.098, -0.066] supported
- store=weaviate, arm=a2-fga-x10, share=0p01: [-0.185, -0.136] supported
- store=weaviate, arm=a2-spicedb-x3, share=0p01: [-0.098, -0.066] supported
- store=weaviate, arm=a2-spicedb-x10, share=0p01: [-0.185, -0.136] supported
- store=weaviate, arm=a1-fga, share=0p05: [-0.185, -0.134] supported
- store=weaviate, arm=a1-spicedb, share=0p05: [-0.185, -0.133] supported
- store=weaviate, arm=a2-fga-x3, share=0p05: [-0.315, -0.246] supported
- store=weaviate, arm=a2-fga-x10, share=0p05: [-0.447, -0.376] supported
- store=weaviate, arm=a2-spicedb-x3, share=0p05: [-0.316, -0.245] supported
- store=weaviate, arm=a2-spicedb-x10, share=0p05: [-0.449, -0.376] supported
- store=opensearch, arm=a1-fga, share=0p001: [-0.008, -0.001] supported
- store=opensearch, arm=a1-spicedb, share=0p001: [-0.007, -0.001] supported
- store=opensearch, arm=a2-fga-x3, share=0p001: [-0.015, -0.005] supported
- store=opensearch, arm=a2-fga-x10, share=0p001: [-0.037, -0.017] supported
- store=opensearch, arm=a2-spicedb-x3, share=0p001: [-0.015, -0.005] supported
- store=opensearch, arm=a2-spicedb-x10, share=0p001: [-0.038, -0.017] supported
- store=opensearch, arm=a1-fga, share=0p01: [-0.047, -0.027] supported
- store=opensearch, arm=a1-spicedb, share=0p01: [-0.047, -0.026] supported
- store=opensearch, arm=a2-fga-x3, share=0p01: [-0.100, -0.069] supported
- store=opensearch, arm=a2-fga-x10, share=0p01: [-0.209, -0.158] supported
- store=opensearch, arm=a2-spicedb-x3, share=0p01: [-0.101, -0.069] supported
- store=opensearch, arm=a2-spicedb-x10, share=0p01: [-0.210, -0.158] supported
- store=opensearch, arm=a1-fga, share=0p05: [-0.181, -0.129] supported
- store=opensearch, arm=a1-spicedb, share=0p05: [-0.182, -0.130] supported
- store=opensearch, arm=a2-fga-x3, share=0p05: [-0.332, -0.262] supported
- store=opensearch, arm=a2-fga-x10, share=0p05: [-0.512, -0.438] supported
- store=opensearch, arm=a2-spicedb-x3, share=0p05: [-0.334, -0.263] supported
- store=opensearch, arm=a2-spicedb-x10, share=0p05: [-0.510, -0.439] supported

### H4: supported

5 parts: {'meets': 5}

- store=pgvector: cells=6, meets=True, needed=6
- store=qdrant: cells=6, meets=True, needed=6
- store=milvus: cells=6, meets=True, needed=6
- store=weaviate: cells=6, meets=True, needed=6
- store=opensearch: cells=3, meets=True, needed=3

### H5: supported

3 parts: {'supported': 3}

- layout=w3_s0p01_neg: [0.001, 0.007] supported
- layout=w3_s0p01_none: [0.046, 0.076] supported
- layout=w3_s0p01_pos: [0.139, 0.186] supported

### H6: not supported

75 parts: {'supported': 58, 'not supported': 13, 'inconclusive': 4}

- store=pgvector, layout=w3_s0p001_neg: [0.953, 1.000] supported
- store=pgvector, layout=w3_s0p001_none: [0.909, 0.984] supported
- store=pgvector, layout=w3_s0p001_pos: [0.960, 1.000] supported
- store=pgvector, layout=w3_s0p01_neg: [0.287, 0.360] not supported
- store=pgvector, layout=w3_s0p01_none: [0.636, 0.693] not supported
- store=pgvector, layout=w3_s0p01_pos: [0.747, 0.785] not supported
- store=pgvector, layout=w3_s0p05_neg: [0.585, 0.650] not supported
- store=pgvector, layout=w3_s0p05_none: [0.854, 0.881] not supported
- store=pgvector, layout=w3_s0p05_pos: [0.856, 0.884] not supported
- store=pgvector, layout=w3_s0p2_neg: [0.814, 0.850] not supported
- store=pgvector, layout=w3_s0p2_none: [0.859, 0.892] not supported
- store=pgvector, layout=w3_s0p2_pos: [0.908, 0.930] supported
- store=pgvector, layout=w3_s0p5_neg: [0.865, 0.895] not supported
- store=pgvector, layout=w3_s0p5_none: [0.917, 0.940] supported
- store=pgvector, layout=w3_s0p5_pos: [0.937, 0.956] supported
- store=qdrant, layout=w3_s0p001_neg: [1.000, 1.000] supported
- store=qdrant, layout=w3_s0p001_none: [1.000, 1.000] supported
- store=qdrant, layout=w3_s0p001_pos: [1.000, 1.000] supported
- store=qdrant, layout=w3_s0p01_neg: [0.915, 0.958] supported
- store=qdrant, layout=w3_s0p01_none: [0.981, 0.991] supported
- store=qdrant, layout=w3_s0p01_pos: [0.989, 0.994] supported
- store=qdrant, layout=w3_s0p05_neg: [0.639, 0.689] not supported
- store=qdrant, layout=w3_s0p05_none: [0.912, 0.933] supported
- store=qdrant, layout=w3_s0p05_pos: [0.961, 0.972] supported
- store=qdrant, layout=w3_s0p2_neg: [0.836, 0.870] not supported
- store=qdrant, layout=w3_s0p2_none: [0.955, 0.968] supported
- store=qdrant, layout=w3_s0p2_pos: [0.972, 0.981] supported
- store=qdrant, layout=w3_s0p5_neg: [0.924, 0.946] supported
- store=qdrant, layout=w3_s0p5_none: [0.968, 0.979] supported
- store=qdrant, layout=w3_s0p5_pos: [0.961, 0.977] supported
- store=milvus, layout=w3_s0p001_neg: [0.966, 0.976] supported
- store=milvus, layout=w3_s0p001_none: [0.947, 0.961] supported
- store=milvus, layout=w3_s0p001_pos: [0.931, 0.945] supported
- store=milvus, layout=w3_s0p01_neg: [0.929, 0.942] supported
- store=milvus, layout=w3_s0p01_none: [0.934, 0.947] supported
- store=milvus, layout=w3_s0p01_pos: [0.925, 0.941] supported
- store=milvus, layout=w3_s0p05_neg: [0.917, 0.936] supported
- store=milvus, layout=w3_s0p05_none: [0.940, 0.954] supported
- store=milvus, layout=w3_s0p05_pos: [0.938, 0.953] supported
- store=milvus, layout=w3_s0p2_neg: [0.898, 0.920] inconclusive
- store=milvus, layout=w3_s0p2_none: [0.938, 0.955] supported
- store=milvus, layout=w3_s0p2_pos: [0.956, 0.969] supported
- store=milvus, layout=w3_s0p5_neg: [0.918, 0.939] supported
- store=milvus, layout=w3_s0p5_none: [0.951, 0.966] supported
- store=milvus, layout=w3_s0p5_pos: [0.965, 0.975] supported
- store=weaviate, layout=w3_s0p001_neg: [1.000, 1.000] supported
- store=weaviate, layout=w3_s0p001_none: [1.000, 1.000] supported
- store=weaviate, layout=w3_s0p001_pos: [1.000, 1.000] supported
- store=weaviate, layout=w3_s0p01_neg: [1.000, 1.000] supported
- store=weaviate, layout=w3_s0p01_none: [1.000, 1.000] supported
- store=weaviate, layout=w3_s0p01_pos: [1.000, 1.000] supported
- store=weaviate, layout=w3_s0p05_neg: [0.896, 0.919] inconclusive
- store=weaviate, layout=w3_s0p05_none: [0.904, 0.928] supported
- store=weaviate, layout=w3_s0p05_pos: [0.917, 0.937] supported
- store=weaviate, layout=w3_s0p2_neg: [0.868, 0.897] not supported
- store=weaviate, layout=w3_s0p2_none: [0.897, 0.924] inconclusive
- store=weaviate, layout=w3_s0p2_pos: [0.933, 0.950] supported
- store=weaviate, layout=w3_s0p5_neg: [0.887, 0.913] inconclusive
- store=weaviate, layout=w3_s0p5_none: [0.927, 0.949] supported
- store=weaviate, layout=w3_s0p5_pos: [0.934, 0.955] supported
- store=opensearch, layout=w3_s0p001_neg: [1.000, 1.000] supported
- store=opensearch, layout=w3_s0p001_none: [1.000, 1.000] supported
- store=opensearch, layout=w3_s0p001_pos: [1.000, 1.000] supported
- store=opensearch, layout=w3_s0p01_neg: [1.000, 1.000] supported
- store=opensearch, layout=w3_s0p01_none: [1.000, 1.000] supported
- store=opensearch, layout=w3_s0p01_pos: [1.000, 1.000] supported
- store=opensearch, layout=w3_s0p05_neg: [1.000, 1.000] supported
- store=opensearch, layout=w3_s0p05_none: [1.000, 1.000] supported
- store=opensearch, layout=w3_s0p05_pos: [0.999, 1.000] supported
- store=opensearch, layout=w3_s0p2_neg: [0.860, 0.894] not supported
- store=opensearch, layout=w3_s0p2_none: [0.969, 0.980] supported
- store=opensearch, layout=w3_s0p2_pos: [0.974, 0.985] supported
- store=opensearch, layout=w3_s0p5_neg: [0.950, 0.967] supported
- store=opensearch, layout=w3_s0p5_none: [0.984, 0.993] supported
- store=opensearch, layout=w3_s0p5_pos: [0.983, 0.991] supported

### H7: supported

30 parts: {'supported': 30}

- layout=w3_s0p001_neg, setting=default: [0.000, 0.000] supported
- layout=w3_s0p001_none, setting=default: [0.000, 0.000] supported
- layout=w3_s0p001_pos, setting=default: [0.000, 0.000] supported
- layout=w3_s0p01_neg, setting=default: [0.000, 0.000] supported
- layout=w3_s0p01_none, setting=default: [0.000, 0.000] supported
- layout=w3_s0p01_pos, setting=default: [0.000, 0.000] supported
- layout=w3_s0p05_neg, setting=default: [0.000, 0.000] supported
- layout=w3_s0p05_none, setting=default: [0.000, 0.000] supported
- layout=w3_s0p05_pos, setting=default: [0.000, 0.000] supported
- layout=w3_s0p2_neg, setting=default: [0.000, 0.000] supported
- layout=w3_s0p2_none, setting=default: [0.000, 0.000] supported
- layout=w3_s0p2_pos, setting=default: [0.000, 0.000] supported
- layout=w3_s0p5_neg, setting=default: [0.000, 0.000] supported
- layout=w3_s0p5_none, setting=default: [0.000, 0.000] supported
- layout=w3_s0p5_pos, setting=default: [0.000, 0.000] supported
- layout=w3_s0p001_neg, setting=iterative: [0.000, 0.000] supported
- layout=w3_s0p001_none, setting=iterative: [0.000, 0.000] supported
- layout=w3_s0p001_pos, setting=iterative: [0.000, 0.000] supported
- layout=w3_s0p01_neg, setting=iterative: [0.000, 0.000] supported
- layout=w3_s0p01_none, setting=iterative: [0.000, 0.000] supported
- layout=w3_s0p01_pos, setting=iterative: [0.000, 0.000] supported
- layout=w3_s0p05_neg, setting=iterative: [0.000, 0.000] supported
- layout=w3_s0p05_none, setting=iterative: [0.000, 0.000] supported
- layout=w3_s0p05_pos, setting=iterative: [0.000, 0.000] supported
- layout=w3_s0p2_neg, setting=iterative: [0.000, 0.000] supported
- layout=w3_s0p2_none, setting=iterative: [0.000, 0.000] supported
- layout=w3_s0p2_pos, setting=iterative: [0.000, 0.000] supported
- layout=w3_s0p5_neg, setting=iterative: [0.000, 0.000] supported
- layout=w3_s0p5_none, setting=iterative: [0.000, 0.000] supported
- layout=w3_s0p5_pos, setting=iterative: [0.000, 0.000] supported

### H8: supported

{"outside": 0, "rows": 12300, "stores": ["milvus", "opensearch", "pgvector", "qdrant", "weaviate"]}

## W1, Enron (own-mail and other-mail questions together, as scored)

| store | arm | recall@10 [95%] | p50 ms (median of jobs) | p99 ms (median of jobs) | empty | errors | outside | queries |
|---|---|---|---|---|---|---|---|---|
| pgvector | a0 | 1.000 [1.000, 1.000] | 0.7 | 3.4 | 0 | 0 | 0 | 600 |
| pgvector | a1-fga | 0.131 [0.121, 0.142] | 25.7 | 34.5 | 7046 | 0 | 0 | 11955 |
| pgvector | a1-spicedb | 0.131 [0.120, 0.141] | 5.3 | 7.5 | 7046 | 0 | 0 | 11955 |
| pgvector | a2-fga-x10 | 0.234 [0.220, 0.249] | 45.8 | 137.4 | 6435 | 0 | 0 | 11955 |
| pgvector | a2-fga-x3 | 0.187 [0.173, 0.201] | 30.2 | 39.3 | 6724 | 0 | 0 | 11955 |
| pgvector | a2-spicedb-x10 | 0.234 [0.220, 0.249] | 8.7 | 12.5 | 6435 | 0 | 0 | 11955 |
| pgvector | a2-spicedb-x3 | 0.187 [0.173, 0.200] | 6.1 | 8.5 | 6724 | 0 | 0 | 11955 |
| pgvector | a3-spicedb@default | 1.000 [1.000, 1.000] | 8.8 | 142.3 | 0 | 0 | 0 | 11955 |
| pgvector | a3-spicedb@iterative | 1.000 [1.000, 1.000] | 8.9 | 145.9 | 0 | 0 | 0 | 11955 |
| pgvector | a4@default | 0.984 [0.969, 0.997] | 0.7 | 3.1 | 135 | 0 | 0 | 11955 |
| pgvector | a4@iterative | 0.996 [0.992, 0.999] | 0.7 | 23.1 | 0 | 0 | 0 | 11955 |
| pgvector | a5-rls@default | 0.984 [0.969, 0.997] | 0.9 | 3.3 | 135 | 0 | 0 | 11955 |
| pgvector | a5-rls@iterative | 0.996 [0.992, 0.999] | 0.8 | 24.0 | 0 | 0 | 0 | 11955 |
| pgvector | a6-partition | 1.000 [1.000, 1.000] | 0.3 | 1.6 | 0 | 0 | 0 | 11955 |
| pgvector | a7-wardowl | 0.635 [0.619, 0.652] | 214.8 | 2176.1 | 550 | 0 | 0 | 11955 |
| qdrant | a1-fga | 0.128 [0.118, 0.140] | 25.4 | 35.1 | 7177 | 0 | 0 | 11955 |
| qdrant | a1-spicedb | 0.128 [0.118, 0.140] | 3.6 | 5.3 | 7177 | 0 | 0 | 11955 |
| qdrant | a2-fga-x10 | 0.230 [0.216, 0.245] | 52.2 | 168.8 | 6522 | 0 | 0 | 11955 |
| qdrant | a2-fga-x3 | 0.183 [0.169, 0.197] | 31.0 | 42.6 | 6865 | 0 | 0 | 11955 |
| qdrant | a2-spicedb-x10 | 0.230 [0.216, 0.245] | 8.0 | 12.1 | 6522 | 0 | 0 | 11955 |
| qdrant | a2-spicedb-x3 | 0.183 [0.169, 0.197] | 4.5 | 6.8 | 6865 | 0 | 0 | 11955 |
| qdrant | a3-spicedb@acorn | 1.000 [1.000, 1.000] | 11.0 | 180.4 | 0 | 0 | 0 | 11955 |
| qdrant | a3-spicedb@default | 1.000 [1.000, 1.000] | 11.3 | 185.4 | 0 | 0 | 0 | 11955 |
| qdrant | a4@acorn | 1.000 [1.000, 1.000] | 0.8 | 1.4 | 0 | 0 | 0 | 11955 |
| qdrant | a4@default | 1.000 [1.000, 1.000] | 0.8 | 1.4 | 0 | 0 | 0 | 11955 |
| qdrant | a7-wardowl | 0.986 [0.974, 0.995] | 11.5 | 212.6 | 50 | 0 | 0 | 11955 |
| milvus | a1-fga | 0.128 [0.117, 0.140] | 27.4 | 37.1 | 7267 | 0 | 0 | 11955 |
| milvus | a1-spicedb | 0.128 [0.117, 0.139] | 4.5 | 6.8 | 7267 | 0 | 0 | 11955 |
| milvus | a2-fga-x10 | 0.229 [0.215, 0.244] | 53.6 | 139.3 | 6585 | 0 | 0 | 11955 |
| milvus | a2-fga-x3 | 0.183 [0.169, 0.197] | 33.3 | 45.1 | 6944 | 0 | 0 | 11955 |
| milvus | a2-spicedb-x10 | 0.229 [0.215, 0.244] | 8.8 | 13.3 | 6585 | 0 | 0 | 11955 |
| milvus | a2-spicedb-x3 | 0.183 [0.169, 0.197] | 5.6 | 8.6 | 6944 | 0 | 0 | 11955 |
| milvus | a3-spicedb@default | 1.000 [1.000, 1.000] | 11.4 | 151.8 | 0 | 0 | 0 | 11955 |
| milvus | a3-spicedb@iterative | 0.962 [0.958, 0.966] | 49.6 | 215.3 | 0 | 0 | 0 | 11955 |
| milvus | a4@default | 1.000 [1.000, 1.000] | 2.2 | 3.2 | 0 | 0 | 0 | 11955 |
| milvus | a4@iterative | 0.962 [0.958, 0.966] | 26.3 | 226.8 | 0 | 0 | 0 | 11955 |
| weaviate | a1-fga | 0.127 [0.117, 0.138] | 20.0 | 27.6 | 7233 | 0 | 0 | 11955 |
| weaviate | a1-spicedb | 0.127 [0.117, 0.138] | 2.9 | 4.4 | 7233 | 0 | 0 | 11955 |
| weaviate | a2-fga-x10 | 0.227 [0.212, 0.241] | 35.4 | 156.7 | 6630 | 0 | 0 | 11955 |
| weaviate | a2-fga-x3 | 0.181 [0.167, 0.195] | 21.2 | 34.5 | 6940 | 0 | 0 | 11955 |
| weaviate | a2-spicedb-x10 | 0.227 [0.212, 0.241] | 6.0 | 9.6 | 6630 | 0 | 0 | 11955 |
| weaviate | a2-spicedb-x3 | 0.181 [0.167, 0.195] | 3.6 | 7.3 | 6940 | 0 | 0 | 11955 |
| weaviate | a3-spicedb@default | 1.000 [1.000, 1.000] | 7.6 | 110.1 | 0 | 0 | 0 | 11955 |
| weaviate | a3-spicedb@pathseer | 1.000 [1.000, 1.000] | 6.9 | 110.2 | 0 | 0 | 0 | 11955 |
| weaviate | a4@default | 1.000 [1.000, 1.000] | 0.8 | 1.6 | 0 | 0 | 0 | 11955 |
| weaviate | a4@pathseer | 1.000 [1.000, 1.000] | 0.8 | 1.5 | 0 | 0 | 0 | 11955 |
| opensearch | a1-fga | 0.134 [0.123, 0.144] | 22.4 | 28.5 | 6841 | 0 | 0 | 11955 |
| opensearch | a1-spicedb | 0.134 [0.124, 0.145] | 6.1 | 8.0 | 6841 | 0 | 0 | 11955 |
| opensearch | a2-fga-x10 | 0.237 [0.222, 0.252] | 47.1 | 98.7 | 6156 | 0 | 0 | 11955 |
| opensearch | a2-fga-x3 | 0.190 [0.176, 0.204] | 27.3 | 35.9 | 6507 | 0 | 0 | 11955 |
| opensearch | a2-spicedb-x10 | 0.237 [0.222, 0.252] | 10.9 | 15.5 | 6156 | 0 | 0 | 11955 |
| opensearch | a2-spicedb-x3 | 0.190 [0.176, 0.204] | 7.4 | 10.3 | 6507 | 0 | 0 | 11955 |
| opensearch | a3-spicedb@default | 1.000 [1.000, 1.000] | 8.5 | 121.1 | 0 | 0 | 0 | 11955 |
| opensearch | a4@default | 1.000 [1.000, 1.000] | 1.3 | 2.6 | 0 | 0 | 0 | 11955 |
| opensearch | a5-dls | 0.209 [0.195, 0.222] | 4.0 | 280.3 | 5795 | 0 | 0 | 11955 |

## W2, w2_tree_a

| store | arm | recall@10 [95%] | p50 ms (median of jobs) | p99 ms (median of jobs) | empty | errors | outside | queries |
|---|---|---|---|---|---|---|---|---|
| pgvector | a0 | 1.000 [1.000, 1.000] | 12.3 | 15.8 | 0 | 0 | 0 | 300 |
| pgvector | a1-fga | 0.043 [0.039, 0.048] | 22.2 | 30.2 | 1978 | 0 | 0 | 3000 |
| pgvector | a1-spicedb | 0.043 [0.039, 0.048] | 4.3 | 5.9 | 1978 | 0 | 0 | 3000 |
| pgvector | a2-fga-x10 | 0.413 [0.391, 0.433] | 45.6 | 99.1 | 65 | 0 | 0 | 3000 |
| pgvector | a2-fga-x3 | 0.124 [0.115, 0.132] | 28.2 | 40.4 | 900 | 0 | 0 | 3000 |
| pgvector | a2-spicedb-x10 | 0.413 [0.392, 0.433] | 6.9 | 10.3 | 65 | 0 | 0 | 3000 |
| pgvector | a2-spicedb-x3 | 0.124 [0.115, 0.132] | 4.9 | 7.4 | 900 | 0 | 0 | 3000 |
| pgvector | a3-spicedb@default | 0.438 [0.413, 0.466] | 365.5 | 467.1 | 56 | 0 | 0 | 3000 |
| pgvector | a3-spicedb@iterative | 0.952 [0.947, 0.957] | 365.2 | 463.0 | 0 | 0 | 0 | 3000 |
| pgvector | a4@default | 0.413 [0.392, 0.433] | 1.9 | 2.9 | 65 | 0 | 0 | 3000 |
| pgvector | a4@iterative | 0.951 [0.946, 0.956] | 4.5 | 10.5 | 0 | 0 | 0 | 3000 |
| pgvector | a5-rls@default | 0.413 [0.391, 0.433] | 2.1 | 3.1 | 65 | 0 | 0 | 3000 |
| pgvector | a5-rls@iterative | 0.951 [0.946, 0.956] | 4.8 | 11.2 | 0 | 0 | 0 | 3000 |
| pgvector | a6-partition | 1.000 [1.000, 1.000] | 5.2 | 7.4 | 0 | 0 | 0 | 3000 |
| pgvector | a7-wardowl | 0.982 [0.979, 0.985] | 111.8 | 169.1 | 0 | 0 | 0 | 3000 |
| qdrant | a1-fga | 0.044 [0.039, 0.049] | 20.8 | 29.1 | 1974 | 0 | 0 | 3000 |
| qdrant | a1-spicedb | 0.044 [0.039, 0.049] | 3.1 | 4.1 | 1974 | 0 | 0 | 3000 |
| qdrant | a2-fga-x10 | 0.413 [0.392, 0.433] | 43.5 | 123.8 | 64 | 0 | 0 | 3000 |
| qdrant | a2-fga-x3 | 0.124 [0.116, 0.133] | 26.1 | 38.0 | 899 | 0 | 0 | 3000 |
| qdrant | a2-spicedb-x10 | 0.413 [0.392, 0.433] | 6.1 | 8.7 | 64 | 0 | 0 | 3000 |
| qdrant | a2-spicedb-x3 | 0.124 [0.116, 0.133] | 3.8 | 5.8 | 899 | 0 | 0 | 3000 |
| qdrant | a3-spicedb@acorn | 0.964 [0.959, 0.969] | 379.6 | 511.8 | 0 | 0 | 0 | 3000 |
| qdrant | a3-spicedb@default | 0.153 [0.083, 0.223] | 382.5 | 527.4 | 0 | 0 | 0 | 3000 |
| qdrant | a4@acorn | 0.964 [0.959, 0.969] | 2.9 | 4.4 | 0 | 0 | 0 | 3000 |
| qdrant | a4@default | 0.163 [0.093, 0.233] | 0.7 | 2.5 | 0 | 0 | 0 | 3000 |
| qdrant | a7-wardowl | 0.975 [0.971, 0.978] | 110.9 | 186.0 | 0 | 0 | 0 | 3000 |
| milvus | a1-fga | 0.044 [0.040, 0.049] | 28.4 | 38.9 | 1958 | 0 | 0 | 3000 |
| milvus | a1-spicedb | 0.044 [0.039, 0.049] | 5.3 | 8.7 | 1967 | 0 | 0 | 3000 |
| milvus | a2-fga-x10 | 0.412 [0.391, 0.432] | 59.9 | 124.2 | 67 | 0 | 0 | 3000 |
| milvus | a2-fga-x3 | 0.124 [0.115, 0.132] | 36.7 | 50.7 | 901 | 0 | 0 | 3000 |
| milvus | a2-spicedb-x10 | 0.412 [0.392, 0.433] | 9.4 | 13.9 | 70 | 0 | 0 | 3000 |
| milvus | a2-spicedb-x3 | 0.124 [0.115, 0.133] | 6.0 | 9.7 | 901 | 0 | 0 | 3000 |
| milvus | a3-spicedb@default | 1.000 [1.000, 1.000] | 462.6 | 583.0 | 0 | 0 | 0 | 3000 |
| milvus | a3-spicedb@iterative | 0.955 [0.951, 0.960] | 465.0 | 585.8 | 0 | 0 | 0 | 3000 |
| milvus | a4@default | 1.000 [1.000, 1.000] | 4.1 | 5.5 | 0 | 0 | 0 | 3000 |
| milvus | a4@iterative | 0.962 [0.958, 0.966] | 3.1 | 4.7 | 0 | 0 | 0 | 3000 |
| weaviate | a1-fga | 0.044 [0.039, 0.048] | 20.8 | 29.9 | 1978 | 0 | 0 | 3000 |
| weaviate | a1-spicedb | 0.044 [0.039, 0.048] | 3.6 | 6.3 | 1978 | 0 | 0 | 3000 |
| weaviate | a2-fga-x10 | 0.414 [0.393, 0.435] | 45.2 | 134.9 | 60 | 0 | 0 | 3000 |
| weaviate | a2-fga-x3 | 0.125 [0.116, 0.133] | 26.2 | 36.9 | 903 | 0 | 0 | 3000 |
| weaviate | a2-spicedb-x10 | 0.414 [0.394, 0.434] | 6.6 | 13.7 | 60 | 0 | 0 | 3000 |
| weaviate | a2-spicedb-x3 | 0.125 [0.116, 0.133] | 4.5 | 7.2 | 903 | 0 | 0 | 3000 |
| weaviate | a3-spicedb@default | 1.000 [1.000, 1.000] | 428.5 | 535.1 | 0 | 0 | 0 | 3000 |
| weaviate | a3-spicedb@pathseer | 1.000 [1.000, 1.000] | 426.2 | 540.2 | 0 | 0 | 0 | 3000 |
| weaviate | a4@default | 1.000 [1.000, 1.000] | 4.3 | 5.7 | 0 | 0 | 0 | 3000 |
| weaviate | a4@pathseer | 1.000 [1.000, 1.000] | 4.3 | 5.8 | 0 | 0 | 0 | 3000 |
| opensearch | a1-fga | 0.043 [0.038, 0.048] | 30.5 | 39.7 | 1987 | 0 | 0 | 3000 |
| opensearch | a1-spicedb | 0.043 [0.038, 0.048] | 9.2 | 14.2 | 1987 | 0 | 0 | 3000 |
| opensearch | a2-fga-x10 | 0.413 [0.392, 0.434] | 57.7 | 105.0 | 66 | 0 | 0 | 3000 |
| opensearch | a2-fga-x3 | 0.124 [0.116, 0.133] | 36.0 | 50.8 | 883 | 0 | 0 | 3000 |
| opensearch | a2-spicedb-x10 | 0.413 [0.392, 0.434] | 14.2 | 20.0 | 66 | 0 | 0 | 3000 |
| opensearch | a2-spicedb-x3 | 0.124 [0.116, 0.133] | 9.1 | 11.8 | 883 | 0 | 0 | 3000 |
| opensearch | a3-spicedb@default | 1.000 [1.000, 1.000] | 452.3 | 569.0 | 0 | 0 | 0 | 3000 |
| opensearch | a4@default | 1.000 [1.000, 1.000] | 3.8 | 6.1 | 0 | 0 | 0 | 3000 |
| opensearch | a5-dls | 0.322 [0.310, 0.333] | 5.5 | 305.3 | 5 | 0 | 0 | 3000 |

## W2, w2_uniform_a

| store | arm | recall@10 [95%] | p50 ms (median of jobs) | p99 ms (median of jobs) | empty | errors | outside | queries |
|---|---|---|---|---|---|---|---|---|
| pgvector | a0 | 1.000 [1.000, 1.000] | 11.8 | 24.1 | 0 | 0 | 0 | 300 |
| pgvector | a1-fga | 0.037 [0.031, 0.042] | 28.6 | 39.6 | 2120 | 0 | 0 | 3000 |
| pgvector | a1-spicedb | 0.037 [0.031, 0.042] | 5.6 | 7.8 | 2120 | 0 | 0 | 3000 |
| pgvector | a2-fga-x10 | 0.383 [0.342, 0.423] | 68.2 | 115.9 | 366 | 0 | 0 | 3000 |
| pgvector | a2-fga-x3 | 0.119 [0.105, 0.133] | 37.8 | 54.4 | 1103 | 0 | 0 | 3000 |
| pgvector | a2-spicedb-x10 | 0.383 [0.342, 0.425] | 8.2 | 12.8 | 366 | 0 | 0 | 3000 |
| pgvector | a2-spicedb-x3 | 0.119 [0.105, 0.133] | 6.4 | 9.1 | 1103 | 0 | 0 | 3000 |
| pgvector | a3-spicedb@default | 0.623 [0.573, 0.674] | 602.8 | 1275.0 | 38 | 0 | 0 | 3000 |
| pgvector | a3-spicedb@iterative | 0.958 [0.951, 0.965] | 605.6 | 1272.6 | 0 | 0 | 0 | 3000 |
| pgvector | a4@default | 0.429 [0.384, 0.474] | 2.2 | 4.0 | 247 | 0 | 0 | 3000 |
| pgvector | a4@iterative | 0.952 [0.946, 0.958] | 5.2 | 27.0 | 0 | 0 | 0 | 3000 |
| pgvector | a5-rls@default | 0.432 [0.388, 0.479] | 2.4 | 3.7 | 239 | 0 | 0 | 3000 |
| pgvector | a5-rls@iterative | 0.952 [0.946, 0.958] | 5.5 | 27.3 | 0 | 0 | 0 | 3000 |
| pgvector | a6-partition | 0.997 [0.996, 0.998] | 2.4 | 7.7 | 0 | 0 | 0 | 3000 |
| pgvector | a7-wardowl | 0.950 [0.933, 0.964] | 156.5 | 247.2 | 0 | 0 | 0 | 3000 |
| qdrant | a1-fga | 0.036 [0.031, 0.042] | 26.7 | 35.5 | 2129 | 0 | 0 | 3000 |
| qdrant | a1-spicedb | 0.036 [0.031, 0.042] | 4.4 | 6.0 | 2129 | 0 | 0 | 3000 |
| qdrant | a2-fga-x10 | 0.388 [0.345, 0.429] | 67.1 | 135.1 | 355 | 0 | 0 | 3000 |
| qdrant | a2-fga-x3 | 0.120 [0.106, 0.134] | 35.4 | 49.7 | 1093 | 0 | 0 | 3000 |
| qdrant | a2-spicedb-x10 | 0.388 [0.346, 0.429] | 7.8 | 11.5 | 355 | 0 | 0 | 3000 |
| qdrant | a2-spicedb-x3 | 0.120 [0.106, 0.135] | 5.2 | 7.8 | 1093 | 0 | 0 | 3000 |
| qdrant | a3-spicedb@acorn | 0.999 [0.998, 0.999] | 597.9 | 1247.3 | 0 | 0 | 0 | 3000 |
| qdrant | a3-spicedb@default | 0.871 [0.823, 0.914] | 594.9 | 1244.7 | 0 | 0 | 0 | 3000 |
| qdrant | a4@acorn | 0.999 [0.998, 0.999] | 14.1 | 24.8 | 0 | 0 | 0 | 3000 |
| qdrant | a4@default | 0.871 [0.823, 0.915] | 2.2 | 3.3 | 0 | 0 | 0 | 3000 |
| qdrant | a7-wardowl | 0.960 [0.943, 0.974] | 160.2 | 268.6 | 0 | 0 | 0 | 3000 |
| milvus | a1-fga | 0.036 [0.031, 0.042] | 30.7 | 42.2 | 2141 | 0 | 0 | 3000 |
| milvus | a1-spicedb | 0.036 [0.031, 0.042] | 5.3 | 8.9 | 2143 | 0 | 0 | 3000 |
| milvus | a2-fga-x10 | 0.383 [0.342, 0.424] | 72.9 | 134.2 | 359 | 0 | 0 | 3000 |
| milvus | a2-fga-x3 | 0.120 [0.106, 0.134] | 39.4 | 50.0 | 1086 | 0 | 0 | 3000 |
| milvus | a2-spicedb-x10 | 0.383 [0.342, 0.424] | 9.7 | 15.2 | 359 | 0 | 0 | 3000 |
| milvus | a2-spicedb-x3 | 0.120 [0.106, 0.134] | 6.9 | 10.9 | 1086 | 0 | 0 | 3000 |
| milvus | a3-spicedb@default | 0.998 [0.997, 0.999] | 603.9 | 1263.3 | 0 | 0 | 0 | 3000 |
| milvus | a3-spicedb@iterative | 0.954 [0.949, 0.958] | 597.8 | 1248.8 | 0 | 0 | 0 | 3000 |
| milvus | a4@default | 0.998 [0.997, 0.999] | 4.0 | 5.7 | 0 | 0 | 0 | 3000 |
| milvus | a4@iterative | 0.954 [0.949, 0.958] | 3.4 | 14.4 | 0 | 0 | 0 | 3000 |
| weaviate | a1-fga | 0.037 [0.031, 0.042] | 27.7 | 37.2 | 2117 | 0 | 0 | 3000 |
| weaviate | a1-spicedb | 0.037 [0.031, 0.042] | 4.5 | 6.8 | 2117 | 0 | 0 | 3000 |
| weaviate | a2-fga-x10 | 0.383 [0.343, 0.424] | 63.2 | 136.8 | 360 | 0 | 0 | 3000 |
| weaviate | a2-fga-x3 | 0.119 [0.105, 0.132] | 36.2 | 49.5 | 1105 | 0 | 0 | 3000 |
| weaviate | a2-spicedb-x10 | 0.383 [0.343, 0.423] | 8.7 | 13.0 | 360 | 0 | 0 | 3000 |
| weaviate | a2-spicedb-x3 | 0.119 [0.105, 0.132] | 5.7 | 9.1 | 1105 | 0 | 0 | 3000 |
| weaviate | a3-spicedb@default | 1.000 [1.000, 1.000] | 677.3 | 1433.7 | 0 | 0 | 0 | 3000 |
| weaviate | a3-spicedb@pathseer | 1.000 [1.000, 1.000] | 680.4 | 1411.0 | 0 | 0 | 0 | 3000 |
| weaviate | a4@default | 1.000 [1.000, 1.000] | 4.5 | 7.2 | 0 | 0 | 0 | 3000 |
| weaviate | a4@pathseer | 1.000 [1.000, 1.000] | 4.9 | 7.7 | 0 | 0 | 0 | 3000 |
| opensearch | a1-fga | 0.036 [0.031, 0.042] | 31.9 | 43.4 | 2140 | 0 | 0 | 3000 |
| opensearch | a1-spicedb | 0.036 [0.031, 0.041] | 8.9 | 13.0 | 2140 | 0 | 0 | 3000 |
| opensearch | a2-fga-x10 | 0.387 [0.347, 0.428] | 66.5 | 114.2 | 367 | 0 | 0 | 3000 |
| opensearch | a2-fga-x3 | 0.120 [0.106, 0.134] | 38.7 | 51.8 | 1104 | 0 | 0 | 3000 |
| opensearch | a2-spicedb-x10 | 0.387 [0.345, 0.429] | 15.6 | 23.0 | 367 | 0 | 0 | 3000 |
| opensearch | a2-spicedb-x3 | 0.120 [0.106, 0.134] | 10.3 | 14.9 | 1104 | 0 | 0 | 3000 |
| opensearch | a3-spicedb@default | 1.000 [0.999, 1.000] | 427.1 | 887.7 | 0 | 0 | 0 | 3000 |
| opensearch | a4@default | 1.000 [0.999, 1.000] | 4.1 | 7.8 | 0 | 0 | 0 | 3000 |
| opensearch | a5-dls | 0.282 [0.259, 0.305] | 5.8 | 306.0 | 200 | 0 | 0 | 3000 |

## W2, w2_erbac_a

| store | arm | recall@10 [95%] | p50 ms (median of jobs) | p99 ms (median of jobs) | empty | errors | outside | queries |
|---|---|---|---|---|---|---|---|---|
| pgvector | a0 | 1.000 [1.000, 1.000] | 19.7 | 39.6 | 0 | 0 | 0 | 300 |
| pgvector | a1-fga | 0.073 [0.063, 0.084] | 21.9 | 29.7 | 1569 | 0 | 0 | 3000 |
| pgvector | a1-spicedb | 0.073 [0.063, 0.083] | 4.9 | 6.8 | 1569 | 0 | 0 | 3000 |
| pgvector | a2-fga-x10 | 0.633 [0.577, 0.687] | 43.5 | 107.7 | 202 | 0 | 0 | 3000 |
| pgvector | a2-fga-x3 | 0.230 [0.204, 0.256] | 27.0 | 37.0 | 574 | 0 | 0 | 3000 |
| pgvector | a2-spicedb-x10 | 0.633 [0.578, 0.689] | 7.4 | 10.6 | 202 | 0 | 0 | 3000 |
| pgvector | a2-spicedb-x3 | 0.230 [0.204, 0.257] | 5.6 | 8.1 | 574 | 0 | 0 | 3000 |
| pgvector | a3-spicedb@default | 0.752 [0.709, 0.790] | 680.4 | 1441.2 | 7 | 0 | 0 | 3000 |
| pgvector | a3-spicedb@iterative | 0.946 [0.938, 0.953] | 673.4 | 1462.1 | 0 | 0 | 0 | 3000 |
| pgvector | a4@default | 0.673 [0.621, 0.723] | 2.1 | 3.2 | 100 | 0 | 0 | 3000 |
| pgvector | a4@iterative | 0.943 [0.936, 0.950] | 3.2 | 19.6 | 0 | 0 | 0 | 3000 |
| pgvector | a5-rls@default | 0.673 [0.622, 0.722] | 2.2 | 3.2 | 100 | 0 | 0 | 3000 |
| pgvector | a5-rls@iterative | 0.943 [0.936, 0.950] | 3.4 | 19.2 | 0 | 0 | 0 | 3000 |
| pgvector | a6-partition | 0.998 [0.996, 0.999] | 5.5 | 11.3 | 0 | 0 | 0 | 3000 |
| pgvector | a7-wardowl | 0.953 [0.939, 0.964] | 112.5 | 188.1 | 0 | 0 | 0 | 3000 |
| qdrant | a1-fga | 0.074 [0.063, 0.084] | 26.2 | 35.0 | 1564 | 0 | 0 | 3000 |
| qdrant | a1-spicedb | 0.074 [0.064, 0.084] | 4.5 | 6.4 | 1564 | 0 | 0 | 3000 |
| qdrant | a2-fga-x10 | 0.629 [0.574, 0.683] | 56.6 | 125.0 | 195 | 0 | 0 | 3000 |
| qdrant | a2-fga-x3 | 0.231 [0.205, 0.257] | 32.8 | 46.1 | 568 | 0 | 0 | 3000 |
| qdrant | a2-spicedb-x10 | 0.629 [0.574, 0.682] | 8.0 | 12.2 | 195 | 0 | 0 | 3000 |
| qdrant | a2-spicedb-x3 | 0.231 [0.205, 0.257] | 5.5 | 7.5 | 568 | 0 | 0 | 3000 |
| qdrant | a3-spicedb@acorn | 0.990 [0.988, 0.992] | 1117.7 | 2422.8 | 0 | 0 | 0 | 3000 |
| qdrant | a3-spicedb@default | 0.693 [0.637, 0.747] | 1110.9 | 2454.4 | 0 | 0 | 0 | 3000 |
| qdrant | a4@acorn | 0.990 [0.988, 0.993] | 6.3 | 11.0 | 0 | 0 | 0 | 3000 |
| qdrant | a4@default | 0.703 [0.649, 0.756] | 1.6 | 3.0 | 0 | 0 | 0 | 3000 |
| qdrant | a7-wardowl | 0.952 [0.940, 0.961] | 151.8 | 258.0 | 0 | 0 | 0 | 3000 |
| milvus | a1-fga | 0.074 [0.064, 0.085] | 29.0 | 40.0 | 1559 | 0 | 0 | 3000 |
| milvus | a1-spicedb | 0.073 [0.064, 0.084] | 6.0 | 10.3 | 1564 | 0 | 0 | 3000 |
| milvus | a2-fga-x10 | 0.627 [0.572, 0.678] | 56.1 | 113.0 | 190 | 0 | 0 | 3000 |
| milvus | a2-fga-x3 | 0.231 [0.205, 0.258] | 34.5 | 46.2 | 569 | 0 | 0 | 3000 |
| milvus | a2-spicedb-x10 | 0.635 [0.579, 0.690] | 9.4 | 14.6 | 193 | 0 | 0 | 3000 |
| milvus | a2-spicedb-x3 | 0.231 [0.205, 0.258] | 6.5 | 9.6 | 569 | 0 | 0 | 3000 |
| milvus | a3-spicedb@default | 0.986 [0.982, 0.989] | 891.6 | 1921.7 | 0 | 0 | 0 | 3000 |
| milvus | a3-spicedb@iterative | 0.953 [0.948, 0.959] | 882.9 | 1920.1 | 0 | 0 | 0 | 3000 |
| milvus | a4@default | 0.986 [0.982, 0.989] | 3.1 | 5.2 | 0 | 0 | 0 | 3000 |
| milvus | a4@iterative | 0.964 [0.959, 0.968] | 3.2 | 31.3 | 0 | 0 | 0 | 3000 |
| weaviate | a1-fga | 0.074 [0.064, 0.084] | 25.7 | 34.1 | 1565 | 0 | 0 | 3000 |
| weaviate | a1-spicedb | 0.074 [0.063, 0.084] | 4.9 | 6.8 | 1565 | 0 | 0 | 3000 |
| weaviate | a2-fga-x10 | 0.622 [0.566, 0.675] | 57.0 | 120.2 | 204 | 0 | 0 | 3000 |
| weaviate | a2-fga-x3 | 0.230 [0.204, 0.257] | 32.6 | 48.3 | 575 | 0 | 0 | 3000 |
| weaviate | a2-spicedb-x10 | 0.622 [0.567, 0.673] | 8.7 | 12.9 | 204 | 0 | 0 | 3000 |
| weaviate | a2-spicedb-x3 | 0.230 [0.204, 0.256] | 5.7 | 8.2 | 575 | 0 | 0 | 3000 |
| weaviate | a3-spicedb@default | 1.000 [1.000, 1.000] | 1252.4 | 2657.4 | 0 | 0 | 0 | 3000 |
| weaviate | a3-spicedb@pathseer | 1.000 [1.000, 1.000] | 1256.4 | 2668.0 | 0 | 0 | 0 | 3000 |
| weaviate | a4@default | 1.000 [1.000, 1.000] | 6.3 | 10.4 | 0 | 0 | 0 | 3000 |
| weaviate | a4@pathseer | 1.000 [1.000, 1.000] | 6.3 | 10.7 | 0 | 0 | 0 | 3000 |
| opensearch | a1-fga | 0.073 [0.064, 0.084] | 33.9 | 49.3 | 1563 | 0 | 0 | 3000 |
| opensearch | a1-spicedb | 0.073 [0.063, 0.084] | 10.2 | 14.1 | 1563 | 0 | 0 | 3000 |
| opensearch | a2-fga-x10 | 0.651 [0.592, 0.706] | 66.0 | 131.9 | 205 | 0 | 0 | 3000 |
| opensearch | a2-fga-x3 | 0.231 [0.205, 0.257] | 39.9 | 57.4 | 557 | 0 | 0 | 3000 |
| opensearch | a2-spicedb-x10 | 0.651 [0.593, 0.707] | 14.4 | 20.3 | 205 | 0 | 0 | 3000 |
| opensearch | a2-spicedb-x3 | 0.231 [0.205, 0.257] | 11.6 | 15.9 | 557 | 0 | 0 | 3000 |
| opensearch | a3-spicedb@default | 0.992 [0.990, 0.995] | 1130.0 | 2477.4 | 0 | 0 | 0 | 3000 |
| opensearch | a4@default | 0.992 [0.990, 0.995] | 5.6 | 9.6 | 0 | 0 | 0 | 3000 |
| opensearch | a5-dls | 0.418 [0.386, 0.449] | 6.0 | 339.0 | 129 | 0 | 0 | 3000 |

## W2, w2_erbac_b

| store | arm | recall@10 [95%] | p50 ms (median of jobs) | p99 ms (median of jobs) | empty | errors | outside | queries |
|---|---|---|---|---|---|---|---|---|
| pgvector | a0 | 1.000 [1.000, 1.000] | 33.8 | 52.0 | 0 | 0 | 0 | 300 |
| pgvector | a1-fga | 0.148 [0.133, 0.164] | 17.6 | 26.0 | 809 | 0 | 0 | 3000 |
| pgvector | a1-spicedb | 0.148 [0.132, 0.164] | 4.2 | 6.4 | 809 | 0 | 0 | 3000 |
| pgvector | a2-fga-x10 | 0.813 [0.770, 0.853] | 34.6 | 89.0 | 18 | 0 | 0 | 3000 |
| pgvector | a2-fga-x3 | 0.446 [0.402, 0.489] | 22.2 | 30.0 | 178 | 0 | 0 | 3000 |
| pgvector | a2-spicedb-x10 | 0.813 [0.770, 0.853] | 6.5 | 9.5 | 18 | 0 | 0 | 3000 |
| pgvector | a2-spicedb-x3 | 0.446 [0.403, 0.490] | 4.6 | 6.8 | 178 | 0 | 0 | 3000 |
| pgvector | a3-spicedb@default | 0.837 [0.799, 0.872] | 1043.1 | 1997.9 | 6 | 0 | 0 | 3000 |
| pgvector | a3-spicedb@iterative | 0.944 [0.937, 0.951] | 1075.6 | 2141.7 | 0 | 0 | 0 | 3000 |
| pgvector | a4@default | 0.813 [0.770, 0.853] | 1.8 | 3.0 | 18 | 0 | 0 | 3000 |
| pgvector | a4@iterative | 0.943 [0.936, 0.950] | 2.3 | 12.4 | 0 | 0 | 0 | 3000 |
| pgvector | a5-rls@default | 0.813 [0.769, 0.854] | 1.7 | 2.7 | 18 | 0 | 0 | 3000 |
| pgvector | a5-rls@iterative | 0.943 [0.936, 0.949] | 2.4 | 11.9 | 0 | 0 | 0 | 3000 |
| pgvector | a6-partition | 0.999 [0.997, 1.000] | 9.7 | 21.0 | 0 | 0 | 0 | 3000 |
| pgvector | a7-wardowl | 0.963 [0.956, 0.969] | 108.2 | 213.4 | 0 | 0 | 0 | 3000 |
| qdrant | a1-fga | 0.150 [0.134, 0.166] | 20.7 | 25.6 | 791 | 0 | 0 | 3000 |
| qdrant | a1-spicedb | 0.150 [0.134, 0.166] | 4.6 | 6.4 | 791 | 0 | 0 | 3000 |
| qdrant | a2-fga-x10 | 0.811 [0.768, 0.850] | 33.2 | 109.3 | 30 | 0 | 0 | 3000 |
| qdrant | a2-fga-x3 | 0.445 [0.401, 0.489] | 20.5 | 29.5 | 187 | 0 | 0 | 3000 |
| qdrant | a2-spicedb-x10 | 0.811 [0.767, 0.851] | 7.0 | 10.7 | 30 | 0 | 0 | 3000 |
| qdrant | a2-spicedb-x3 | 0.445 [0.400, 0.489] | 3.7 | 7.0 | 187 | 0 | 0 | 3000 |
| qdrant | a3-spicedb@acorn | 0.991 [0.989, 0.993] | 1066.9 | 2054.4 | 0 | 0 | 0 | 3000 |
| qdrant | a3-spicedb@default | 0.750 [0.701, 0.794] | 1099.1 | 2083.0 | 0 | 0 | 0 | 3000 |
| qdrant | a4@acorn | 0.991 [0.989, 0.993] | 4.7 | 7.4 | 0 | 0 | 0 | 3000 |
| qdrant | a4@default | 0.749 [0.701, 0.795] | 1.2 | 1.7 | 0 | 0 | 0 | 3000 |
| qdrant | a7-wardowl | 0.958 [0.951, 0.964] | 103.2 | 205.0 | 0 | 0 | 0 | 3000 |
| milvus | a1-fga | 0.151 [0.135, 0.166] | 23.1 | 31.1 | 778 | 0 | 0 | 3000 |
| milvus | a1-spicedb | 0.150 [0.135, 0.167] | 5.1 | 7.8 | 781 | 0 | 0 | 3000 |
| milvus | a2-fga-x10 | 0.806 [0.762, 0.847] | 45.6 | 122.2 | 27 | 0 | 0 | 3000 |
| milvus | a2-fga-x3 | 0.446 [0.401, 0.490] | 27.0 | 37.6 | 180 | 0 | 0 | 3000 |
| milvus | a2-spicedb-x10 | 0.822 [0.778, 0.863] | 7.6 | 13.7 | 21 | 0 | 0 | 3000 |
| milvus | a2-spicedb-x3 | 0.446 [0.402, 0.489] | 7.0 | 9.6 | 180 | 0 | 0 | 3000 |
| milvus | a3-spicedb@default | 0.975 [0.971, 0.979] | 1446.7 | 2837.0 | 0 | 0 | 0 | 3000 |
| milvus | a3-spicedb@iterative | 0.957 [0.952, 0.962] | 1433.6 | 2619.1 | 0 | 0 | 0 | 3000 |
| milvus | a4@default | 0.975 [0.970, 0.979] | 2.4 | 5.1 | 0 | 0 | 0 | 3000 |
| milvus | a4@iterative | 0.965 [0.961, 0.969] | 2.7 | 5.4 | 0 | 0 | 0 | 3000 |
| weaviate | a1-fga | 0.149 [0.133, 0.165] | 27.5 | 39.5 | 797 | 0 | 0 | 3000 |
| weaviate | a1-spicedb | 0.149 [0.133, 0.165] | 5.6 | 8.0 | 797 | 0 | 0 | 3000 |
| weaviate | a2-fga-x10 | 0.800 [0.758, 0.839] | 58.5 | 126.2 | 22 | 0 | 0 | 3000 |
| weaviate | a2-fga-x3 | 0.446 [0.401, 0.490] | 34.5 | 47.4 | 187 | 0 | 0 | 3000 |
| weaviate | a2-spicedb-x10 | 0.800 [0.759, 0.839] | 9.6 | 14.4 | 22 | 0 | 0 | 3000 |
| weaviate | a2-spicedb-x3 | 0.446 [0.401, 0.491] | 6.6 | 10.3 | 187 | 0 | 0 | 3000 |
| weaviate | a3-spicedb@default | 0.980 [0.974, 0.986] | 2639.2 | 4756.1 | 0 | 0 | 0 | 3000 |
| weaviate | a3-spicedb@pathseer | 0.988 [0.983, 0.991] | 2624.9 | 4874.3 | 0 | 0 | 0 | 3000 |
| weaviate | a4@default | 0.980 [0.974, 0.986] | 5.7 | 12.6 | 0 | 0 | 0 | 3000 |
| weaviate | a4@pathseer | 0.988 [0.983, 0.992] | 5.4 | 12.1 | 0 | 0 | 0 | 3000 |
| opensearch | a1-fga | 0.150 [0.134, 0.165] | 29.7 | 43.4 | 792 | 0 | 0 | 3000 |
| opensearch | a1-spicedb | 0.149 [0.134, 0.165] | 10.5 | 14.0 | 792 | 0 | 0 | 3000 |
| opensearch | a2-fga-x10 | 0.848 [0.802, 0.890] | 60.9 | 117.5 | 18 | 0 | 0 | 3000 |
| opensearch | a2-fga-x3 | 0.449 [0.404, 0.494] | 36.1 | 52.2 | 175 | 0 | 0 | 3000 |
| opensearch | a2-spicedb-x10 | 0.848 [0.801, 0.890] | 14.4 | 20.4 | 18 | 0 | 0 | 3000 |
| opensearch | a2-spicedb-x3 | 0.449 [0.404, 0.493] | 10.0 | 15.0 | 175 | 0 | 0 | 3000 |
| opensearch | a3-spicedb@default | 0.990 [0.988, 0.992] | 2277.4 | 4207.2 | 0 | 0 | 0 | 3000 |
| opensearch | a4@default | 0.990 [0.988, 0.992] | 5.1 | 9.6 | 0 | 0 | 0 | 3000 |
| opensearch | a5-dls | 0.519 [0.493, 0.545] | 5.2 | 329.0 | 3 | 0 | 0 | 3000 |

## W3: recall@10 by arm, store and layout

### a0

| store | 0p001 neg | 0p001 none | 0p001 pos | 0p01 neg | 0p01 none | 0p01 pos | 0p05 neg | 0p05 none | 0p05 pos | 0p2 neg | 0p2 none | 0p2 pos | 0p5 neg | 0p5 none | 0p5 pos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

### a1-fga

| store | 0p001 neg | 0p001 none | 0p001 pos | 0p01 neg | 0p01 none | 0p01 pos | 0p05 neg | 0p05 none | 0p05 pos | 0p2 neg | 0p2 none | 0p2 pos | 0p5 neg | 0p5 none | 0p5 pos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | 0.000 | 0.002 | 0.004 | 0.000 | 0.014 | 0.038 | 0.004 | 0.058 | 0.161 | 0.050 | 0.181 | 0.439 | 0.226 | 0.513 | 0.745 |
| qdrant | 0.000 | 0.002 | 0.004 | 0.000 | 0.014 | 0.037 | 0.003 | 0.058 | 0.161 | 0.049 | 0.183 | 0.443 | 0.225 | 0.515 | 0.749 |
| milvus | 0.000 | 0.002 | 0.003 | 0.000 | 0.014 | 0.037 | 0.003 | 0.058 | 0.159 | 0.049 | 0.183 | 0.446 | 0.226 | 0.517 | 0.755 |
| weaviate | 0.000 | 0.002 | 0.004 | 0.000 | 0.014 | 0.036 | 0.003 | 0.057 | 0.161 | 0.049 | 0.182 | 0.441 | 0.226 | 0.511 | 0.739 |
| opensearch | 0.000 | 0.002 | 0.004 | 0.000 | 0.014 | 0.036 | 0.003 | 0.058 | 0.158 | 0.050 | 0.184 | 0.446 | 0.226 | 0.521 | 0.761 |

### a1-spicedb

| store | 0p001 neg | 0p001 none | 0p001 pos | 0p01 neg | 0p01 none | 0p01 pos | 0p05 neg | 0p05 none | 0p05 pos | 0p2 neg | 0p2 none | 0p2 pos | 0p5 neg | 0p5 none | 0p5 pos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | 0.000 | 0.002 | 0.004 | 0.000 | 0.014 | 0.038 | 0.004 | 0.058 | 0.161 | 0.050 | 0.181 | 0.439 | 0.226 | 0.513 | 0.746 |
| qdrant | 0.000 | 0.002 | 0.004 | 0.000 | 0.014 | 0.037 | 0.003 | 0.059 | 0.161 | 0.049 | 0.182 | 0.443 | 0.225 | 0.515 | 0.749 |
| milvus | 0.000 | 0.002 | 0.003 | 0.000 | 0.014 | 0.037 | 0.003 | 0.058 | 0.159 | 0.049 | 0.183 | 0.446 | 0.226 | 0.517 | 0.755 |
| weaviate | 0.000 | 0.002 | 0.004 | 0.000 | 0.014 | 0.036 | 0.003 | 0.057 | 0.161 | 0.049 | 0.182 | 0.441 | 0.226 | 0.511 | 0.739 |
| opensearch | 0.000 | 0.002 | 0.004 | 0.000 | 0.014 | 0.036 | 0.003 | 0.058 | 0.158 | 0.050 | 0.184 | 0.446 | 0.226 | 0.521 | 0.761 |

### a2-fga-x10

| store | 0p001 neg | 0p001 none | 0p001 pos | 0p01 neg | 0p01 none | 0p01 pos | 0p05 neg | 0p05 none | 0p05 pos | 0p2 neg | 0p2 none | 0p2 pos | 0p5 neg | 0p5 none | 0p5 pos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | 0.000 | 0.005 | 0.025 | 0.003 | 0.061 | 0.162 | 0.030 | 0.254 | 0.444 | 0.206 | 0.620 | 0.757 | 0.593 | 0.878 | 0.909 |
| qdrant | 0.000 | 0.005 | 0.026 | 0.003 | 0.064 | 0.175 | 0.028 | 0.264 | 0.468 | 0.209 | 0.650 | 0.780 | 0.602 | 0.891 | 0.916 |
| milvus | 0.000 | 0.005 | 0.027 | 0.003 | 0.063 | 0.177 | 0.030 | 0.268 | 0.474 | 0.214 | 0.659 | 0.787 | 0.612 | 0.898 | 0.926 |
| weaviate | 0.000 | 0.005 | 0.025 | 0.003 | 0.061 | 0.163 | 0.027 | 0.249 | 0.439 | 0.199 | 0.605 | 0.747 | 0.582 | 0.859 | 0.898 |
| opensearch | 0.000 | 0.006 | 0.027 | 0.003 | 0.065 | 0.186 | 0.031 | 0.280 | 0.505 | 0.224 | 0.699 | 0.817 | 0.646 | 0.937 | 0.949 |

### a2-fga-x3

| store | 0p001 neg | 0p001 none | 0p001 pos | 0p01 neg | 0p01 none | 0p01 pos | 0p05 neg | 0p05 none | 0p05 pos | 0p2 neg | 0p2 none | 0p2 pos | 0p5 neg | 0p5 none | 0p5 pos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | 0.000 | 0.002 | 0.009 | 0.001 | 0.027 | 0.083 | 0.015 | 0.126 | 0.293 | 0.099 | 0.381 | 0.646 | 0.391 | 0.771 | 0.863 |
| qdrant | 0.000 | 0.002 | 0.009 | 0.001 | 0.028 | 0.085 | 0.012 | 0.126 | 0.301 | 0.100 | 0.390 | 0.658 | 0.392 | 0.778 | 0.867 |
| milvus | 0.000 | 0.002 | 0.010 | 0.001 | 0.028 | 0.086 | 0.014 | 0.127 | 0.301 | 0.102 | 0.391 | 0.662 | 0.396 | 0.784 | 0.876 |
| weaviate | 0.000 | 0.002 | 0.009 | 0.001 | 0.028 | 0.083 | 0.013 | 0.125 | 0.292 | 0.099 | 0.377 | 0.638 | 0.389 | 0.760 | 0.852 |
| opensearch | 0.000 | 0.002 | 0.010 | 0.001 | 0.028 | 0.086 | 0.013 | 0.127 | 0.309 | 0.104 | 0.401 | 0.678 | 0.407 | 0.812 | 0.896 |

### a2-spicedb-x10

| store | 0p001 neg | 0p001 none | 0p001 pos | 0p01 neg | 0p01 none | 0p01 pos | 0p05 neg | 0p05 none | 0p05 pos | 0p2 neg | 0p2 none | 0p2 pos | 0p5 neg | 0p5 none | 0p5 pos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | 0.000 | 0.005 | 0.025 | 0.003 | 0.061 | 0.162 | 0.030 | 0.254 | 0.444 | 0.206 | 0.620 | 0.757 | 0.593 | 0.878 | 0.909 |
| qdrant | 0.000 | 0.005 | 0.026 | 0.003 | 0.064 | 0.175 | 0.028 | 0.264 | 0.468 | 0.209 | 0.650 | 0.780 | 0.602 | 0.891 | 0.916 |
| milvus | 0.000 | 0.005 | 0.027 | 0.003 | 0.063 | 0.177 | 0.030 | 0.268 | 0.474 | 0.214 | 0.659 | 0.787 | 0.612 | 0.898 | 0.926 |
| weaviate | 0.000 | 0.005 | 0.025 | 0.003 | 0.061 | 0.163 | 0.027 | 0.249 | 0.439 | 0.199 | 0.605 | 0.747 | 0.582 | 0.859 | 0.898 |
| opensearch | 0.000 | 0.006 | 0.027 | 0.003 | 0.065 | 0.187 | 0.031 | 0.280 | 0.505 | 0.224 | 0.699 | 0.817 | 0.646 | 0.937 | 0.949 |

### a2-spicedb-x3

| store | 0p001 neg | 0p001 none | 0p001 pos | 0p01 neg | 0p01 none | 0p01 pos | 0p05 neg | 0p05 none | 0p05 pos | 0p2 neg | 0p2 none | 0p2 pos | 0p5 neg | 0p5 none | 0p5 pos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | 0.000 | 0.002 | 0.009 | 0.001 | 0.027 | 0.083 | 0.015 | 0.126 | 0.293 | 0.099 | 0.381 | 0.646 | 0.391 | 0.771 | 0.863 |
| qdrant | 0.000 | 0.002 | 0.009 | 0.001 | 0.028 | 0.085 | 0.012 | 0.126 | 0.301 | 0.100 | 0.390 | 0.658 | 0.392 | 0.778 | 0.867 |
| milvus | 0.000 | 0.002 | 0.010 | 0.001 | 0.028 | 0.086 | 0.014 | 0.127 | 0.301 | 0.102 | 0.391 | 0.662 | 0.396 | 0.783 | 0.876 |
| weaviate | 0.000 | 0.002 | 0.009 | 0.001 | 0.028 | 0.083 | 0.013 | 0.125 | 0.292 | 0.099 | 0.377 | 0.638 | 0.389 | 0.760 | 0.852 |
| opensearch | 0.000 | 0.002 | 0.010 | 0.001 | 0.028 | 0.086 | 0.013 | 0.127 | 0.309 | 0.104 | 0.401 | 0.678 | 0.407 | 0.812 | 0.896 |

### a3-spicedb@acorn

| store | 0p001 neg | 0p001 none | 0p001 pos | 0p01 neg | 0p01 none | 0p01 pos | 0p05 neg | 0p05 none | 0p05 pos | 0p2 neg | 0p2 none | 0p2 pos | 0p5 neg | 0p5 none | 0p5 pos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qdrant | 1.000 | 1.000 | 1.000 | 0.936 | 0.981 | 0.991 | 0.660 | 0.923 | 0.966 | 0.855 | 0.965 | 0.973 | 0.717 | 0.915 | 0.936 |

### a3-spicedb@default

| store | 0p001 neg | 0p001 none | 0p001 pos | 0p01 neg | 0p01 none | 0p01 pos | 0p05 neg | 0p05 none | 0p05 pos | 0p2 neg | 0p2 none | 0p2 pos | 0p5 neg | 0p5 none | 0p5 pos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | 1.000 | 1.000 | 1.000 | 0.003 | 0.061 | 0.162 | 0.029 | 0.271 | 0.457 | 0.236 | 0.625 | 0.758 | 0.569 | 0.902 | 0.898 |
| qdrant | 1.000 | 1.000 | 1.000 | 0.914 | 0.913 | 0.940 | 0.182 | 0.562 | 0.770 | 0.485 | 0.765 | 0.899 | 0.717 | 0.915 | 0.936 |
| milvus | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.955 | 0.966 | 0.967 | 0.917 | 0.963 | 0.969 |
| weaviate | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.547 | 0.823 | 0.888 | 0.738 | 0.872 | 0.914 | 0.944 | 0.960 | 0.961 |
| opensearch | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.886 | 0.970 | 0.978 | 0.958 | 0.997 | 0.987 |

### a3-spicedb@iterative

| store | 0p001 neg | 0p001 none | 0p001 pos | 0p01 neg | 0p01 none | 0p01 pos | 0p05 neg | 0p05 none | 0p05 pos | 0p2 neg | 0p2 none | 0p2 pos | 0p5 neg | 0p5 none | 0p5 pos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | 1.000 | 1.000 | 1.000 | 0.323 | 0.665 | 0.767 | 0.608 | 0.860 | 0.869 | 0.832 | 0.873 | 0.920 | 0.852 | 0.945 | 0.955 |
| milvus | 0.972 | 0.955 | 0.938 | 0.936 | 0.941 | 0.933 | 0.929 | 0.944 | 0.944 | 0.910 | 0.944 | 0.959 | 0.935 | 0.973 | 0.972 |

### a3-spicedb@pathseer

| store | 0p001 neg | 0p001 none | 0p001 pos | 0p01 neg | 0p01 none | 0p01 pos | 0p05 neg | 0p05 none | 0p05 pos | 0p2 neg | 0p2 none | 0p2 pos | 0p5 neg | 0p5 none | 0p5 pos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| weaviate | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.913 | 0.913 | 0.927 | 0.887 | 0.909 | 0.944 | 0.871 | 0.946 | 0.960 |

### a4@acorn

| store | 0p001 neg | 0p001 none | 0p001 pos | 0p01 neg | 0p01 none | 0p01 pos | 0p05 neg | 0p05 none | 0p05 pos | 0p2 neg | 0p2 none | 0p2 pos | 0p5 neg | 0p5 none | 0p5 pos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qdrant | 1.000 | 1.000 | 1.000 | 0.937 | 0.986 | 0.992 | 0.665 | 0.923 | 0.967 | 0.853 | 0.962 | 0.977 | 0.935 | 0.974 | 0.969 |

### a4@default

| store | 0p001 neg | 0p001 none | 0p001 pos | 0p01 neg | 0p01 none | 0p01 pos | 0p05 neg | 0p05 none | 0p05 pos | 0p2 neg | 0p2 none | 0p2 pos | 0p5 neg | 0p5 none | 0p5 pos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | 0.977 | 0.930 | 0.973 | 0.003 | 0.061 | 0.162 | 0.030 | 0.254 | 0.444 | 0.206 | 0.620 | 0.757 | 0.593 | 0.878 | 0.909 |
| qdrant | 1.000 | 1.000 | 1.000 | 0.917 | 0.933 | 0.942 | 0.200 | 0.555 | 0.776 | 0.485 | 0.752 | 0.895 | 0.722 | 0.894 | 0.938 |
| milvus | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.949 | 0.966 | 0.972 | 0.930 | 0.952 | 0.966 |
| weaviate | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.565 | 0.829 | 0.884 | 0.747 | 0.873 | 0.912 | 0.953 | 0.956 | 0.950 |
| opensearch | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.878 | 0.975 | 0.980 | 0.959 | 0.989 | 0.987 |

### a4@iterative

| store | 0p001 neg | 0p001 none | 0p001 pos | 0p01 neg | 0p01 none | 0p01 pos | 0p05 neg | 0p05 none | 0p05 pos | 0p2 neg | 0p2 none | 0p2 pos | 0p5 neg | 0p5 none | 0p5 pos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | 0.981 | 0.951 | 0.985 | 0.323 | 0.665 | 0.767 | 0.618 | 0.868 | 0.870 | 0.832 | 0.876 | 0.919 | 0.880 | 0.928 | 0.947 |
| milvus | 0.972 | 0.955 | 0.938 | 0.936 | 0.941 | 0.933 | 0.926 | 0.947 | 0.946 | 0.909 | 0.946 | 0.963 | 0.929 | 0.958 | 0.970 |

### a4@pathseer

| store | 0p001 neg | 0p001 none | 0p001 pos | 0p01 neg | 0p01 none | 0p01 pos | 0p05 neg | 0p05 none | 0p05 pos | 0p2 neg | 0p2 none | 0p2 pos | 0p5 neg | 0p5 none | 0p5 pos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| weaviate | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.907 | 0.917 | 0.927 | 0.883 | 0.911 | 0.942 | 0.900 | 0.938 | 0.945 |

### a5-dls

| store | 0p001 neg | 0p001 none | 0p001 pos | 0p01 neg | 0p01 none | 0p01 pos | 0p05 neg | 0p05 none | 0p05 pos | 0p2 neg | 0p2 none | 0p2 pos | 0p5 neg | 0p5 none | 0p5 pos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| opensearch | 0.001 | 0.015 | 0.054 | 0.011 | 0.111 | 0.262 | 0.069 | 0.389 | 0.589 | 0.335 | 0.771 | 0.850 | 0.733 | 0.952 | 0.957 |

### a5-rls@default

| store | 0p001 neg | 0p001 none | 0p001 pos | 0p01 neg | 0p01 none | 0p01 pos | 0p05 neg | 0p05 none | 0p05 pos | 0p2 neg | 0p2 none | 0p2 pos | 0p5 neg | 0p5 none | 0p5 pos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | 0.977 | 0.930 | 0.973 | 0.003 | 0.061 | 0.162 | 0.030 | 0.254 | 0.444 | 0.206 | 0.620 | 0.757 | 0.593 | 0.878 | 0.909 |

### a5-rls@iterative

| store | 0p001 neg | 0p001 none | 0p001 pos | 0p01 neg | 0p01 none | 0p01 pos | 0p05 neg | 0p05 none | 0p05 pos | 0p2 neg | 0p2 none | 0p2 pos | 0p5 neg | 0p5 none | 0p5 pos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | 0.981 | 0.951 | 0.985 | 0.323 | 0.665 | 0.767 | 0.618 | 0.868 | 0.870 | 0.832 | 0.876 | 0.919 | 0.880 | 0.928 | 0.947 |

### a7-wardowl

| store | 0p001 neg | 0p001 none | 0p001 pos | 0p01 neg | 0p01 none | 0p01 pos | 0p05 neg | 0p05 none | 0p05 pos | 0p2 neg | 0p2 none | 0p2 pos | 0p5 neg | 0p5 none | 0p5 pos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | 0.006 | 0.047 | 0.138 | 0.057 | 0.295 | 0.511 | 0.253 | 0.755 | 0.801 | 0.730 | 0.916 | 0.919 | 0.903 | 0.938 | 0.949 |
| qdrant | 0.006 | 0.047 | 0.140 | 0.054 | 0.294 | 0.520 | 0.252 | 0.752 | 0.799 | 0.717 | 0.915 | 0.930 | 0.891 | 0.944 | 0.953 |

## W3: median p50 latency (ms) by arm, store and share (median over correlations)

- a0: pgvector: 2.2 / 13.7 / 76.4 / 2104.6 / 3103.9
- a1-fga: pgvector: 26.1 / 17.6 / 20.2 / 27.1 / 22.1; qdrant: 26.2 / 26.0 / 26.1 / 27.9 / 20.4; milvus: 29.7 / 30.0 / 22.3 / 21.4 / 28.6; weaviate: 26.3 / 22.3 / 16.3 / 25.7 / 20.3; opensearch: 27.6 / 22.5 / 25.4 / 25.4 / 34.6
- a1-spicedb: pgvector: 5.0 / 3.9 / 4.2 / 5.0 / 4.8; qdrant: 4.0 / 4.4 / 4.1 / 4.5 / 3.6; milvus: 5.5 / 6.0 / 4.5 / 4.8 / 5.5; weaviate: 4.4 / 4.1 / 3.1 / 4.5 / 3.7; opensearch: 10.9 / 7.0 / 8.3 / 9.4 / 11.7
- a2-fga-x10: pgvector: 57.3 / 34.7 / 39.1 / 60.1 / 44.6; qdrant: 58.6 / 59.5 / 58.0 / 58.9 / 44.3; milvus: 61.8 / 53.9 / 47.2 / 44.5 / 57.5; weaviate: 60.0 / 45.9 / 32.2 / 58.8 / 35.7; opensearch: 53.4 / 42.5 / 50.0 / 49.8 / 68.0
- a2-fga-x3: pgvector: 32.6 / 24.4 / 22.7 / 34.8 / 26.3; qdrant: 32.4 / 34.3 / 32.9 / 33.5 / 25.8; milvus: 36.5 / 33.3 / 29.3 / 26.4 / 36.1; weaviate: 33.7 / 27.7 / 19.2 / 33.2 / 23.4; opensearch: 32.6 / 27.2 / 30.6 / 30.6 / 40.6
- a2-spicedb-x10: pgvector: 8.0 / 6.2 / 6.2 / 8.3 / 7.5; qdrant: 8.0 / 8.7 / 8.0 / 8.6 / 6.7; milvus: 8.9 / 9.4 / 7.1 / 7.5 / 8.8; weaviate: 8.9 / 7.9 / 5.2 / 8.9 / 5.8; opensearch: 15.2 / 10.4 / 13.6 / 14.5 / 17.4
- a2-spicedb-x3: pgvector: 6.1 / 4.3 / 4.5 / 5.7 / 5.4; qdrant: 4.9 / 5.0 / 5.0 / 5.1 / 4.9; milvus: 6.2 / 6.5 / 5.0 / 5.3 / 6.3; weaviate: 5.4 / 5.7 / 3.4 / 5.4 / 4.7; opensearch: 12.4 / 8.5 / 10.8 / 10.5 / 13.0
- a3-spicedb@acorn: qdrant: 97.5 / 752.7 / 3486.5 / 13971.3 / 22366.4
- a3-spicedb@default: pgvector: 98.5 / 322.0 / 1578.5 / 14166.0 / 21934.1; qdrant: 99.6 / 750.4 / 3478.2 / 13866.8 / 22412.7; milvus: 103.3 / 565.9 / 2186.2 / 8411.3 / 26899.3; weaviate: 112.4 / 541.2 / 1917.9 / 15592.9 / 18621.1; opensearch: 71.1 / 349.8 / 2238.4 / 8568.8 / 34947.1
- a3-spicedb@iterative: pgvector: 99.0 / 367.7 / 1580.9 / 14159.3 / 21888.6; milvus: 246.9 / 653.9 / 2221.9 / 8597.5 / 27165.1
- a3-spicedb@pathseer: weaviate: 112.3 / 544.5 / 1865.8 / 15594.2 / 18700.8
- a4@acorn: qdrant: 1.1 / 2.6 / 5.0 / 5.1 / 4.4
- a4@default: pgvector: 1.9 / 2.2 / 2.4 / 3.1 / 3.4; qdrant: 1.1 / 2.5 / 1.5 / 1.7 / 1.8; milvus: 3.2 / 4.1 / 8.6 / 4.2 / 5.0; weaviate: 1.8 / 5.8 / 3.6 / 6.7 / 5.2; opensearch: 2.2 / 2.8 / 9.9 / 12.3 / 15.4
- a4@iterative: pgvector: 1.9 / 46.6 / 13.4 / 4.7 / 3.7; milvus: 76.2 / 14.9 / 5.1 / 3.4 / 3.5
- a4@pathseer: weaviate: 1.8 / 5.8 / 3.9 / 5.8 / 5.2
- a5-dls: opensearch: 7.9 / 4.9 / 8.0 / 15.8 / 35.2
- a5-rls@default: pgvector: 2.0 / 2.3 / 2.3 / 3.9 / 3.5
- a5-rls@iterative: pgvector: 2.1 / 46.5 / 15.9 / 5.5 / 3.7
- a7-wardowl: pgvector: 194.9 / 155.6 / 204.4 / 472.8 / 617.3; qdrant: 198.2 / 229.4 / 313.5 / 444.1 / 575.5

## W3: median p99 latency (ms) by arm, store and share (median over correlations)

- a0: pgvector: 7.2 / 19.4 / 96.9 / 2211.7 / 3257.1
- a1-fga: pgvector: 39.7 / 25.1 / 29.5 / 41.6 / 30.1; qdrant: 36.0 / 36.5 / 35.9 / 35.9 / 26.7; milvus: 40.3 / 39.9 / 30.9 / 27.3 / 38.9; weaviate: 35.3 / 28.8 / 22.4 / 34.7 / 26.9; opensearch: 42.4 / 33.2 / 33.8 / 32.6 / 47.1
- a1-spicedb: pgvector: 8.9 / 6.6 / 7.3 / 9.0 / 7.8; qdrant: 5.7 / 6.7 / 5.9 / 6.8 / 5.5; milvus: 9.2 / 9.5 / 8.3 / 9.0 / 10.2; weaviate: 6.2 / 6.3 / 6.4 / 6.5 / 5.5; opensearch: 19.7 / 10.8 / 11.6 / 14.8 / 16.5
- a2-fga-x10: pgvector: 133.2 / 127.0 / 140.4 / 148.7 / 129.3; qdrant: 148.4 / 157.6 / 141.4 / 154.9 / 133.1; milvus: 145.6 / 151.6 / 136.3 / 130.7 / 139.1; weaviate: 137.0 / 178.4 / 118.7 / 132.3 / 150.2; opensearch: 126.5 / 108.6 / 116.5 / 126.0 / 124.6
- a2-fga-x3: pgvector: 50.5 / 41.4 / 38.1 / 51.9 / 37.3; qdrant: 44.7 / 47.4 / 44.8 / 44.6 / 34.3; milvus: 48.7 / 43.8 / 39.6 / 37.3 / 48.0; weaviate: 47.0 / 37.2 / 27.9 / 45.5 / 31.8; opensearch: 51.9 / 38.7 / 41.6 / 40.1 / 57.4
- a2-spicedb-x10: pgvector: 19.2 / 13.0 / 13.5 / 18.1 / 14.5; qdrant: 12.2 / 13.3 / 12.3 / 13.1 / 10.0; milvus: 17.5 / 14.7 / 13.8 / 16.2 / 20.8; weaviate: 13.4 / 11.9 / 8.3 / 13.1 / 10.5; opensearch: 25.0 / 19.0 / 22.0 / 22.5 / 35.3
- a2-spicedb-x3: pgvector: 9.7 / 6.8 / 8.9 / 9.8 / 8.3; qdrant: 7.2 / 7.3 / 6.7 / 7.9 / 6.8; milvus: 9.9 / 9.9 / 8.2 / 9.2 / 9.7; weaviate: 7.8 / 8.3 / 6.2 / 7.9 / 7.3; opensearch: 17.0 / 13.4 / 16.8 / 14.9 / 19.2
- a3-spicedb@acorn: qdrant: 187.3 / 903.3 / 3713.9 / 14287.0 / 22736.6
- a3-spicedb@default: pgvector: 185.9 / 396.6 / 1718.5 / 14488.8 / 22370.5; qdrant: 186.1 / 881.5 / 3679.0 / 14280.9 / 22783.2; milvus: 187.4 / 643.3 / 2283.4 / 8568.2 / 27413.6; weaviate: 205.5 / 629.5 / 2077.3 / 16041.7 / 19095.0; opensearch: 214.4 / 626.2 / 2716.3 / 8781.1 / 35792.5
- a3-spicedb@iterative: pgvector: 186.7 / 452.8 / 1860.2 / 14514.3 / 22333.8; milvus: 767.6 / 1057.8 / 2485.9 / 11714.6 / 29411.4
- a3-spicedb@pathseer: weaviate: 207.6 / 625.9 / 2001.0 / 16089.2 / 21050.9
- a4@acorn: qdrant: 1.5 / 3.9 / 7.7 / 8.7 / 8.0
- a4@default: pgvector: 5.5 / 4.2 / 4.1 / 4.7 / 5.1; qdrant: 1.6 / 3.9 / 2.2 / 2.5 / 2.6; milvus: 4.9 / 5.8 / 11.6 / 6.6 / 7.2; weaviate: 2.5 / 7.5 / 5.2 / 9.8 / 10.5; opensearch: 3.7 / 6.9 / 14.3 / 23.8 / 38.2
- a4@iterative: pgvector: 87.0 / 96.0 / 54.6 / 37.7 / 11.1; milvus: 338.2 / 58.7 / 14.7 / 7.0 / 5.6
- a4@pathseer: weaviate: 2.5 / 7.3 / 10.5 / 8.5 / 9.4
- a5-dls: opensearch: 290.3 / 232.9 / 286.4 / 296.3 / 366.1
- a5-rls@default: pgvector: 4.9 / 3.9 / 4.2 / 6.3 / 5.6
- a5-rls@iterative: pgvector: 116.7 / 135.5 / 79.1 / 49.2 / 21.8
- a7-wardowl: pgvector: 267.8 / 258.5 / 341.6 / 696.4 / 1116.5; qdrant: 295.6 / 339.1 / 448.3 / 659.2 / 808.7

## W3: p50 and p99 latency (ms, median over jobs), lowest and highest cell per arm

- a0: p50 2.0 to 3433.4; p99 5.1 to 3528.8 (15 cells)
- a1-fga: p50 16.3 to 34.6; p99 20.9 to 48.5 (75 cells)
- a1-spicedb: p50 3.1 to 11.8; p99 5.1 to 21.2 (75 cells)
- a2-fga-x10: p50 32.1 to 68.4; p99 107.7 to 180.4 (75 cells)
- a2-fga-x3: p50 19.2 to 40.7; p99 27.8 to 59.7 (75 cells)
- a2-spicedb-x10: p50 5.2 to 17.4; p99 8.0 to 35.6 (75 cells)
- a2-spicedb-x3: p50 3.4 to 13.2; p99 5.9 to 19.6 (75 cells)
- a3-spicedb@acorn: p50 94.9 to 22374.1; p99 169.1 to 22801.4 (15 cells)
- a3-spicedb@default: p50 68.4 to 34952.0; p99 139.1 to 35800.8 (75 cells)
- a3-spicedb@iterative: p50 95.4 to 27713.2; p99 173.1 to 33431.4 (30 cells)
- a3-spicedb@pathseer: p50 108.8 to 18725.6; p99 193.1 to 21423.3 (15 cells)
- a4@acorn: p50 1.0 to 5.9; p99 1.5 to 9.4 (15 cells)
- a4@default: p50 1.1 to 15.4; p99 1.5 to 456.6 (75 cells)
- a4@iterative: p50 1.8 to 174.4; p99 5.1 to 437.7 (30 cells)
- a4@pathseer: p50 1.8 to 12.7; p99 2.5 to 55.6 (15 cells)
- a5-dls: p50 4.9 to 37.3; p99 229.7 to 370.2 (15 cells)
- a5-rls@default: p50 2.0 to 4.8; p99 3.9 to 7.8 (15 cells)
- a5-rls@iterative: p50 1.9 to 94.1; p99 21.1 to 370.3 (15 cells)
- a7-wardowl: p50 142.6 to 676.2; p99 231.7 to 1222.0 (30 cells)

## W3: per-job p50 latency (ms), fastest and slowest job, for A0, A3 and A4, by store and layout

- a0 pgvector w3_s0p001_neg: median 2.0, jobs 1.9 to 2.3; p99 median 5.1, jobs 3.3 to 5.1
- a0 pgvector w3_s0p001_none: median 3.7, jobs 2.5 to 4.1; p99 median 7.2, jobs 5.0 to 7.5
- a0 pgvector w3_s0p001_pos: median 2.2, jobs 1.8 to 2.4; p99 median 7.2, jobs 4.5 to 9.6
- a0 pgvector w3_s0p01_neg: median 11.2, jobs 11.0 to 13.4; p99 median 15.5, jobs 13.8 to 25.6
- a0 pgvector w3_s0p01_none: median 14.0, jobs 13.9 to 16.3; p99 median 24.9, jobs 19.1 to 30.3
- a0 pgvector w3_s0p01_pos: median 13.7, jobs 13.3 to 15.2; p99 median 19.4, jobs 16.7 to 26.5
- a0 pgvector w3_s0p05_neg: median 72.9, jobs 63.6 to 78.6; p99 median 93.0, jobs 73.5 to 94.6
- a0 pgvector w3_s0p05_none: median 76.4, jobs 64.7 to 80.1; p99 median 99.5, jobs 81.1 to 113.5
- a0 pgvector w3_s0p05_pos: median 76.7, jobs 63.5 to 78.5; p99 median 96.9, jobs 96.8 to 111.0
- a0 pgvector w3_s0p2_neg: median 2621.9, jobs 2595.2 to 2624.7; p99 median 2731.6, jobs 2693.8 to 2735.7
- a0 pgvector w3_s0p2_none: median 2104.6, jobs 2068.0 to 2110.1; p99 median 2211.7, jobs 2179.2 to 2234.7
- a0 pgvector w3_s0p2_pos: median 1811.1, jobs 1778.3 to 1813.4; p99 median 1909.8, jobs 1873.0 to 1910.9
- a0 pgvector w3_s0p5_neg: median 3433.4, jobs 3250.8 to 4553.9; p99 median 3528.8, jobs 3330.2 to 4679.1
- a0 pgvector w3_s0p5_none: median 3103.9, jobs 2939.0 to 4121.1; p99 median 3257.1, jobs 3060.8 to 4271.4
- a0 pgvector w3_s0p5_pos: median 2802.0, jobs 2651.1 to 3715.1; p99 median 2923.3, jobs 2750.2 to 3840.5
- a3-spicedb@acorn qdrant w3_s0p001_neg: median 97.5, jobs 67.8 to 99.8; p99 median 169.1, jobs 117.9 to 180.1
- a3-spicedb@acorn qdrant w3_s0p001_none: median 108.3, jobs 73.1 to 111.7; p99 median 187.3, jobs 125.3 to 192.7
- a3-spicedb@acorn qdrant w3_s0p001_pos: median 94.9, jobs 66.1 to 96.9; p99 median 190.6, jobs 131.3 to 197.9
- a3-spicedb@acorn qdrant w3_s0p01_neg: median 736.3, jobs 545.3 to 737.4; p99 median 894.4, jobs 649.0 to 909.1
- a3-spicedb@acorn qdrant w3_s0p01_none: median 752.7, jobs 554.1 to 753.3; p99 median 903.3, jobs 662.9 to 912.9
- a3-spicedb@acorn qdrant w3_s0p01_pos: median 757.8, jobs 560.8 to 760.1; p99 median 933.3, jobs 672.0 to 937.5
- a3-spicedb@acorn qdrant w3_s0p05_neg: median 3486.5, jobs 2227.1 to 3576.3; p99 median 3694.7, jobs 2344.7 to 3786.6
- a3-spicedb@acorn qdrant w3_s0p05_none: median 3485.3, jobs 2225.9 to 3572.2; p99 median 3713.9, jobs 2358.0 to 3749.3
- a3-spicedb@acorn qdrant w3_s0p05_pos: median 3502.5, jobs 2236.3 to 3594.0; p99 median 3715.3, jobs 2380.3 to 3785.1
- a3-spicedb@acorn qdrant w3_s0p2_neg: median 13946.0, jobs 6429.9 to 14150.7; p99 median 14234.1, jobs 6854.1 to 14691.8
- a3-spicedb@acorn qdrant w3_s0p2_none: median 13971.3, jobs 6446.9 to 14160.6; p99 median 14287.0, jobs 6922.1 to 14484.6
- a3-spicedb@acorn qdrant w3_s0p2_pos: median 14010.5, jobs 6531.4 to 14182.7; p99 median 14294.1, jobs 6869.4 to 14511.3
- a3-spicedb@acorn qdrant w3_s0p5_neg: median 22349.2, jobs 21837.4 to 24363.2; p99 median 22639.2, jobs 22198.9 to 25480.1
- a3-spicedb@acorn qdrant w3_s0p5_none: median 22366.4, jobs 21827.6 to 24361.0; p99 median 22736.6, jobs 22249.5 to 25571.5
- a3-spicedb@acorn qdrant w3_s0p5_pos: median 22374.1, jobs 21795.1 to 24279.4; p99 median 22801.4, jobs 22247.8 to 25306.6
- a3-spicedb@default pgvector w3_s0p001_neg: median 98.5, jobs 64.4 to 100.4; p99 median 169.0, jobs 111.6 to 176.1
- a3-spicedb@default pgvector w3_s0p001_none: median 108.0, jobs 71.5 to 111.5; p99 median 185.9, jobs 120.5 to 186.1
- a3-spicedb@default pgvector w3_s0p001_pos: median 96.0, jobs 62.4 to 98.5; p99 median 196.4, jobs 123.5 to 199.5
- a3-spicedb@default pgvector w3_s0p01_neg: median 316.2, jobs 310.8 to 723.0; p99 median 393.2, jobs 383.2 to 847.0
- a3-spicedb@default pgvector w3_s0p01_none: median 322.0, jobs 317.2 to 732.4; p99 median 396.6, jobs 387.1 to 854.4
- a3-spicedb@default pgvector w3_s0p01_pos: median 325.2, jobs 319.6 to 738.2; p99 median 401.2, jobs 399.8 to 863.7
- a3-spicedb@default pgvector w3_s0p05_neg: median 1578.5, jobs 1557.5 to 2135.9; p99 median 1707.9, jobs 1706.6 to 2239.0
- a3-spicedb@default pgvector w3_s0p05_none: median 1578.4, jobs 1556.8 to 2135.1; p99 median 1718.5, jobs 1711.5 to 2238.1
- a3-spicedb@default pgvector w3_s0p05_pos: median 1587.3, jobs 1565.5 to 2146.5; p99 median 1749.5, jobs 1730.1 to 2264.5
- a3-spicedb@default pgvector w3_s0p2_neg: median 14133.0, jobs 13607.9 to 14153.5; p99 median 14430.9, jobs 13987.7 to 14496.6
- a3-spicedb@default pgvector w3_s0p2_none: median 14166.0, jobs 13651.8 to 14171.3; p99 median 14498.6, jobs 14004.7 to 14647.3
- a3-spicedb@default pgvector w3_s0p2_pos: median 14217.7, jobs 13727.1 to 14233.6; p99 median 14488.8, jobs 14148.8 to 14596.8
- a3-spicedb@default pgvector w3_s0p5_neg: median 21893.4, jobs 21147.6 to 35093.2; p99 median 22193.4, jobs 21436.0 to 35844.8
- a3-spicedb@default pgvector w3_s0p5_none: median 21976.9, jobs 21138.3 to 35114.8; p99 median 22370.5, jobs 21436.3 to 35543.1
- a3-spicedb@default pgvector w3_s0p5_pos: median 21934.1, jobs 21185.2 to 35172.6; p99 median 22387.7, jobs 21454.7 to 35687.7
- a3-spicedb@default qdrant w3_s0p001_neg: median 99.6, jobs 68.5 to 100.2; p99 median 172.6, jobs 122.2 to 175.6
- a3-spicedb@default qdrant w3_s0p001_none: median 108.1, jobs 74.3 to 110.3; p99 median 186.7, jobs 126.9 to 189.3
- a3-spicedb@default qdrant w3_s0p001_pos: median 96.5, jobs 66.5 to 97.7; p99 median 186.1, jobs 131.3 to 193.1
- a3-spicedb@default qdrant w3_s0p01_neg: median 733.4, jobs 542.6 to 739.9; p99 median 880.1, jobs 662.3 to 890.0
- a3-spicedb@default qdrant w3_s0p01_none: median 750.4, jobs 555.3 to 752.0; p99 median 881.5, jobs 663.8 to 889.4
- a3-spicedb@default qdrant w3_s0p01_pos: median 756.5, jobs 562.6 to 757.8; p99 median 910.5, jobs 684.7 to 920.2
- a3-spicedb@default qdrant w3_s0p05_neg: median 3458.7, jobs 2249.4 to 3559.1; p99 median 3679.0, jobs 2386.4 to 3730.2
- a3-spicedb@default qdrant w3_s0p05_none: median 3478.2, jobs 2242.7 to 3570.8; p99 median 3669.8, jobs 2383.1 to 3751.9
- a3-spicedb@default qdrant w3_s0p05_pos: median 3487.9, jobs 2263.0 to 3582.0; p99 median 3742.6, jobs 2407.0 to 3768.8
- a3-spicedb@default qdrant w3_s0p2_neg: median 13866.8, jobs 6506.6 to 14109.7; p99 median 14280.9, jobs 6725.1 to 14390.2
- a3-spicedb@default qdrant w3_s0p2_none: median 13863.7, jobs 6504.4 to 14112.0; p99 median 14382.0, jobs 6827.3 to 14386.6
- a3-spicedb@default qdrant w3_s0p2_pos: median 13894.9, jobs 6568.4 to 14110.9; p99 median 14231.7, jobs 6871.3 to 14449.2
- a3-spicedb@default qdrant w3_s0p5_neg: median 22451.1, jobs 21843.1 to 24332.0; p99 median 22744.2, jobs 22234.4 to 25216.8
- a3-spicedb@default qdrant w3_s0p5_none: median 22412.7, jobs 21866.3 to 24341.7; p99 median 22817.8, jobs 22117.5 to 25189.8
- a3-spicedb@default qdrant w3_s0p5_pos: median 22357.4, jobs 21807.2 to 24366.1; p99 median 22783.2, jobs 22246.6 to 25410.7
- a3-spicedb@default milvus w3_s0p001_neg: median 103.3, jobs 46.9 to 107.9; p99 median 179.7, jobs 79.6 to 182.1
- a3-spicedb@default milvus w3_s0p001_none: median 112.8, jobs 52.6 to 119.3; p99 median 187.4, jobs 86.2 to 196.4
- a3-spicedb@default milvus w3_s0p001_pos: median 97.9, jobs 45.8 to 103.8; p99 median 195.9, jobs 88.2 to 204.3
- a3-spicedb@default milvus w3_s0p01_neg: median 553.9, jobs 472.6 to 761.8; p99 median 639.7, jobs 568.6 to 882.4
- a3-spicedb@default milvus w3_s0p01_none: median 565.9, jobs 483.7 to 778.2; p99 median 643.3, jobs 574.0 to 876.9
- a3-spicedb@default milvus w3_s0p01_pos: median 572.5, jobs 488.9 to 784.1; p99 median 665.6, jobs 580.6 to 900.9
- a3-spicedb@default milvus w3_s0p05_neg: median 2185.5, jobs 2157.3 to 2765.2; p99 median 2283.4, jobs 2275.4 to 2872.8
- a3-spicedb@default milvus w3_s0p05_none: median 2186.2, jobs 2162.2 to 2770.1; p99 median 2288.6, jobs 2270.4 to 2873.8
- a3-spicedb@default milvus w3_s0p05_pos: median 2198.8, jobs 2175.5 to 2780.6; p99 median 2276.3, jobs 2253.0 to 2892.7
- a3-spicedb@default milvus w3_s0p2_neg: median 8401.7, jobs 6297.9 to 13959.8; p99 median 8535.0, jobs 6576.7 to 14334.2
- a3-spicedb@default milvus w3_s0p2_none: median 8411.3, jobs 6338.2 to 13955.0; p99 median 8568.2, jobs 6630.1 to 14351.1
- a3-spicedb@default milvus w3_s0p2_pos: median 8425.8, jobs 6372.9 to 13970.5; p99 median 8634.1, jobs 6656.3 to 14494.5
- a3-spicedb@default milvus w3_s0p5_neg: median 26940.5, jobs 21328.3 to 34217.6; p99 median 27413.6, jobs 21693.9 to 35598.7
- a3-spicedb@default milvus w3_s0p5_none: median 26890.3, jobs 21340.4 to 34359.7; p99 median 27243.8, jobs 21668.9 to 35196.8
- a3-spicedb@default milvus w3_s0p5_pos: median 26899.3, jobs 21324.8 to 34277.1; p99 median 27451.9, jobs 21601.9 to 35267.3
- a3-spicedb@default weaviate w3_s0p001_neg: median 112.4, jobs 89.0 to 113.6; p99 median 198.8, jobs 153.7 to 201.1
- a3-spicedb@default weaviate w3_s0p001_none: median 125.3, jobs 98.9 to 125.5; p99 median 205.5, jobs 163.6 to 211.7
- a3-spicedb@default weaviate w3_s0p001_pos: median 108.9, jobs 86.0 to 109.7; p99 median 215.5, jobs 174.0 to 218.9
- a3-spicedb@default weaviate w3_s0p01_neg: median 531.4, jobs 385.1 to 838.9; p99 median 629.5, jobs 463.6 to 995.0
- a3-spicedb@default weaviate w3_s0p01_none: median 541.2, jobs 394.3 to 854.5; p99 median 628.3, jobs 462.7 to 970.1
- a3-spicedb@default weaviate w3_s0p01_pos: median 548.8, jobs 398.9 to 861.7; p99 median 643.3, jobs 471.9 to 1003.5
- a3-spicedb@default weaviate w3_s0p05_neg: median 1914.4, jobs 1759.5 to 4103.8; p99 median 2077.3, jobs 1919.9 to 4297.1
- a3-spicedb@default weaviate w3_s0p05_none: median 1917.9, jobs 1763.2 to 4098.2; p99 median 2055.2, jobs 2008.5 to 4315.6
- a3-spicedb@default weaviate w3_s0p05_pos: median 1928.5, jobs 1770.1 to 4118.0; p99 median 2123.0, jobs 2045.9 to 4316.2
- a3-spicedb@default weaviate w3_s0p2_neg: median 15592.9, jobs 7009.9 to 16088.0; p99 median 16041.7, jobs 7327.6 to 16421.4
- a3-spicedb@default weaviate w3_s0p2_none: median 15521.2, jobs 7011.3 to 16079.8; p99 median 15955.1, jobs 7398.4 to 16447.3
- a3-spicedb@default weaviate w3_s0p2_pos: median 15633.4, jobs 7070.9 to 16117.4; p99 median 16055.1, jobs 7447.7 to 16497.0
- a3-spicedb@default weaviate w3_s0p5_neg: median 18621.1, jobs 18339.9 to 26411.9; p99 median 19095.0, jobs 19007.0 to 27195.3
- a3-spicedb@default weaviate w3_s0p5_none: median 18565.8, jobs 18219.0 to 26300.9; p99 median 19066.3, jobs 19035.1 to 27350.9
- a3-spicedb@default weaviate w3_s0p5_pos: median 18635.7, jobs 18293.8 to 26403.8; p99 median 19327.7, jobs 18948.5 to 27599.7
- a3-spicedb@default opensearch w3_s0p001_neg: median 71.1, jobs 63.9 to 102.6; p99 median 139.1, jobs 129.2 to 195.3
- a3-spicedb@default opensearch w3_s0p001_none: median 80.1, jobs 73.4 to 118.1; p99 median 329.4, jobs 293.4 to 436.0
- a3-spicedb@default opensearch w3_s0p001_pos: median 68.4, jobs 61.0 to 98.8; p99 median 214.4, jobs 192.7 to 217.5
- a3-spicedb@default opensearch w3_s0p01_neg: median 333.0, jobs 309.1 to 454.6; p99 median 504.7, jobs 412.2 to 611.3
- a3-spicedb@default opensearch w3_s0p01_none: median 366.8, jobs 317.8 to 480.0; p99 median 795.2, jobs 694.8 to 879.0
- a3-spicedb@default opensearch w3_s0p01_pos: median 349.8, jobs 319.9 to 472.5; p99 median 626.2, jobs 507.3 to 710.0
- a3-spicedb@default opensearch w3_s0p05_neg: median 2210.3, jobs 1579.7 to 3668.7; p99 median 2620.3, jobs 2210.7 to 4339.8
- a3-spicedb@default opensearch w3_s0p05_none: median 2288.4, jobs 1644.0 to 3841.7; p99 median 2873.2, jobs 2230.0 to 4632.4
- a3-spicedb@default opensearch w3_s0p05_pos: median 2238.4, jobs 1606.7 to 3735.1; p99 median 2716.3, jobs 2269.8 to 4452.1
- a3-spicedb@default opensearch w3_s0p2_neg: median 8537.0, jobs 8383.7 to 13538.0; p99 median 8726.1, jobs 8607.5 to 14097.4
- a3-spicedb@default opensearch w3_s0p2_none: median 8568.8, jobs 8401.3 to 13606.7; p99 median 8873.2, jobs 8830.9 to 14282.2
- a3-spicedb@default opensearch w3_s0p2_pos: median 8590.4, jobs 8402.6 to 13611.6; p99 median 8781.1, jobs 8765.3 to 14446.7
- a3-spicedb@default opensearch w3_s0p5_neg: median 34952.0, jobs 33920.4 to 35672.3; p99 median 35792.5, jobs 34994.0 to 36467.4
- a3-spicedb@default opensearch w3_s0p5_none: median 34947.1, jobs 34005.7 to 35800.8; p99 median 35800.8, jobs 34935.4 to 36594.4
- a3-spicedb@default opensearch w3_s0p5_pos: median 34924.2, jobs 34040.2 to 35855.9; p99 median 35537.1, jobs 34740.2 to 36520.9
- a3-spicedb@iterative pgvector w3_s0p001_neg: median 99.0, jobs 64.2 to 99.0; p99 median 173.1, jobs 109.8 to 173.5
- a3-spicedb@iterative pgvector w3_s0p001_none: median 108.2, jobs 71.2 to 109.9; p99 median 187.8, jobs 119.2 to 188.9
- a3-spicedb@iterative pgvector w3_s0p001_pos: median 95.4, jobs 62.3 to 97.2; p99 median 186.7, jobs 123.5 to 194.3
- a3-spicedb@iterative pgvector w3_s0p01_neg: median 383.5, jobs 378.3 to 785.4; p99 median 473.1, jobs 461.0 to 928.4
- a3-spicedb@iterative pgvector w3_s0p01_none: median 367.7, jobs 363.0 to 774.5; p99 median 450.8, jobs 443.4 to 894.2
- a3-spicedb@iterative pgvector w3_s0p01_pos: median 357.0, jobs 354.0 to 767.7; p99 median 452.8, jobs 451.1 to 897.2
- a3-spicedb@iterative pgvector w3_s0p05_neg: median 1601.6, jobs 1580.8 to 2181.4; p99 median 1860.2, jobs 1740.6 to 2287.3
- a3-spicedb@iterative pgvector w3_s0p05_none: median 1575.7, jobs 1553.1 to 2147.2; p99 median 1827.7, jobs 1688.7 to 2259.0
- a3-spicedb@iterative pgvector w3_s0p05_pos: median 1580.9, jobs 1553.9 to 2159.6; p99 median 1860.2, jobs 1725.9 to 2256.9
- a3-spicedb@iterative pgvector w3_s0p2_neg: median 14156.0, jobs 13595.0 to 14188.1; p99 median 14415.3, jobs 14021.6 to 14468.0
- a3-spicedb@iterative pgvector w3_s0p2_none: median 14159.3, jobs 13591.5 to 14204.2; p99 median 14514.3, jobs 13968.8 to 14520.4
- a3-spicedb@iterative pgvector w3_s0p2_pos: median 14164.7, jobs 13607.5 to 14215.9; p99 median 14558.8, jobs 13998.6 to 14564.4
- a3-spicedb@iterative pgvector w3_s0p5_neg: median 21877.3, jobs 21048.8 to 34990.6; p99 median 22261.8, jobs 21570.3 to 35288.7
- a3-spicedb@iterative pgvector w3_s0p5_none: median 21976.0, jobs 21053.6 to 35003.2; p99 median 22475.1, jobs 21652.5 to 35498.1
- a3-spicedb@iterative pgvector w3_s0p5_pos: median 21888.6, jobs 21051.8 to 34929.3; p99 median 22333.8, jobs 21621.9 to 35397.2
- a3-spicedb@iterative milvus w3_s0p001_neg: median 430.1, jobs 266.8 to 478.1; p99 median 1092.0, jobs 741.5 to 1294.0
- a3-spicedb@iterative milvus w3_s0p001_none: median 246.9, jobs 142.2 to 263.1; p99 median 767.6, jobs 515.8 to 934.7
- a3-spicedb@iterative milvus w3_s0p001_pos: median 151.0, jobs 79.8 to 158.1; p99 median 543.9, jobs 340.6 to 601.6
- a3-spicedb@iterative milvus w3_s0p01_neg: median 956.9, jobs 681.0 to 1063.2; p99 median 2463.8, jobs 1489.2 to 2567.6
- a3-spicedb@iterative milvus w3_s0p01_none: median 653.9, jobs 528.2 to 848.6; p99 median 1057.8, jobs 780.0 to 1253.5
- a3-spicedb@iterative milvus w3_s0p01_pos: median 611.6, jobs 509.6 to 814.1; p99 median 1027.5, jobs 735.2 to 1186.4
- a3-spicedb@iterative milvus w3_s0p05_neg: median 2414.3, jobs 2375.1 to 3052.4; p99 median 3291.9, jobs 3252.2 to 4158.6
- a3-spicedb@iterative milvus w3_s0p05_none: median 2221.9, jobs 2204.5 to 2807.8; p99 median 2377.0, jobs 2355.7 to 3018.8
- a3-spicedb@iterative milvus w3_s0p05_pos: median 2218.5, jobs 2194.2 to 2803.6; p99 median 2485.9, jobs 2459.9 to 3146.8
- a3-spicedb@iterative milvus w3_s0p2_neg: median 9409.4, jobs 7729.8 to 15747.8; p99 median 15379.9, jobs 14881.9 to 28734.2
- a3-spicedb@iterative milvus w3_s0p2_none: median 8597.5, jobs 6583.4 to 14243.2; p99 median 9711.8, jobs 8052.7 to 15763.4
- a3-spicedb@iterative milvus w3_s0p2_pos: median 8481.6, jobs 6490.4 to 14073.6; p99 median 11714.6, jobs 9720.2 to 19412.3
- a3-spicedb@iterative milvus w3_s0p5_neg: median 27713.2, jobs 21571.9 to 35601.3; p99 median 33431.4, jobs 29269.1 to 48117.8
- a3-spicedb@iterative milvus w3_s0p5_none: median 27165.1, jobs 21270.5 to 34713.5; p99 median 29074.8, jobs 21704.6 to 36501.4
- a3-spicedb@iterative milvus w3_s0p5_pos: median 27095.8, jobs 21224.3 to 34629.7; p99 median 29411.4, jobs 22161.2 to 36815.3
- a3-spicedb@pathseer weaviate w3_s0p001_neg: median 112.3, jobs 89.2 to 114.2; p99 median 193.1, jobs 153.0 to 195.4
- a3-spicedb@pathseer weaviate w3_s0p001_none: median 124.5, jobs 99.0 to 127.1; p99 median 207.6, jobs 164.1 to 212.8
- a3-spicedb@pathseer weaviate w3_s0p001_pos: median 108.8, jobs 86.6 to 110.9; p99 median 216.2, jobs 173.5 to 226.2
- a3-spicedb@pathseer weaviate w3_s0p01_neg: median 532.2, jobs 384.3 to 842.9; p99 median 619.5, jobs 464.9 to 985.8
- a3-spicedb@pathseer weaviate w3_s0p01_none: median 544.5, jobs 393.7 to 859.7; p99 median 625.9, jobs 464.8 to 984.3
- a3-spicedb@pathseer weaviate w3_s0p01_pos: median 550.6, jobs 398.5 to 870.7; p99 median 648.8, jobs 476.1 to 1025.0
- a3-spicedb@pathseer weaviate w3_s0p05_neg: median 1865.8, jobs 1799.1 to 4125.7; p99 median 2010.6, jobs 2009.6 to 4329.8
- a3-spicedb@pathseer weaviate w3_s0p05_none: median 1855.1, jobs 1792.6 to 4121.9; p99 median 1991.0, jobs 1987.3 to 4292.3
- a3-spicedb@pathseer weaviate w3_s0p05_pos: median 1869.6, jobs 1795.3 to 4127.1; p99 median 2001.0, jobs 1986.0 to 4344.1
- a3-spicedb@pathseer weaviate w3_s0p2_neg: median 15594.2, jobs 7141.0 to 16099.7; p99 median 16089.2, jobs 7502.1 to 16424.6
- a3-spicedb@pathseer weaviate w3_s0p2_none: median 15550.2, jobs 7225.5 to 16098.3; p99 median 15921.0, jobs 7602.6 to 16434.0
- a3-spicedb@pathseer weaviate w3_s0p2_pos: median 15632.1, jobs 7230.0 to 16124.8; p99 median 16112.6, jobs 7601.1 to 16572.2
- a3-spicedb@pathseer weaviate w3_s0p5_neg: median 18725.6, jobs 18096.4 to 27050.3; p99 median 21050.9, jobs 18988.9 to 27869.4
- a3-spicedb@pathseer weaviate w3_s0p5_none: median 18700.8, jobs 18295.5 to 27120.8; p99 median 20479.3, jobs 19128.6 to 27779.4
- a3-spicedb@pathseer weaviate w3_s0p5_pos: median 18619.2, jobs 18357.5 to 27005.3; p99 median 21423.3, jobs 19306.4 to 27819.6
- a4@acorn qdrant w3_s0p001_neg: median 1.0, jobs 1.0 to 1.2; p99 median 1.5, jobs 1.5 to 1.7
- a4@acorn qdrant w3_s0p001_none: median 1.1, jobs 1.1 to 1.2; p99 median 1.5, jobs 1.4 to 1.7
- a4@acorn qdrant w3_s0p001_pos: median 1.1, jobs 1.0 to 1.2; p99 median 1.5, jobs 1.4 to 1.7
- a4@acorn qdrant w3_s0p01_neg: median 2.5, jobs 1.9 to 3.1; p99 median 3.6, jobs 2.6 to 5.7
- a4@acorn qdrant w3_s0p01_none: median 2.6, jobs 2.2 to 3.8; p99 median 3.9, jobs 3.1 to 9.3
- a4@acorn qdrant w3_s0p01_pos: median 2.8, jobs 2.0 to 6.5; p99 median 4.1, jobs 2.9 to 9.3
- a4@acorn qdrant w3_s0p05_neg: median 4.1, jobs 3.7 to 4.2; p99 median 6.9, jobs 6.4 to 7.0
- a4@acorn qdrant w3_s0p05_none: median 5.0, jobs 4.4 to 5.1; p99 median 7.7, jobs 7.7 to 8.0
- a4@acorn qdrant w3_s0p05_pos: median 5.5, jobs 4.8 to 5.5; p99 median 8.1, jobs 8.0 to 8.3
- a4@acorn qdrant w3_s0p2_neg: median 5.1, jobs 4.0 to 5.2; p99 median 8.7, jobs 7.2 to 9.0
- a4@acorn qdrant w3_s0p2_none: median 5.9, jobs 4.6 to 6.1; p99 median 9.4, jobs 8.7 to 9.7
- a4@acorn qdrant w3_s0p2_pos: median 5.1, jobs 4.0 to 5.2; p99 median 8.6, jobs 7.6 to 8.6
- a4@acorn qdrant w3_s0p5_neg: median 4.4, jobs 4.3 to 4.6; p99 median 8.0, jobs 7.8 to 8.1
- a4@acorn qdrant w3_s0p5_none: median 4.6, jobs 4.3 to 4.7; p99 median 8.3, jobs 8.1 to 8.3
- a4@acorn qdrant w3_s0p5_pos: median 3.3, jobs 3.1 to 3.3; p99 median 6.3, jobs 6.0 to 6.4
- a4@default pgvector w3_s0p001_neg: median 1.8, jobs 1.7 to 1.8; p99 median 3.9, jobs 3.1 to 115.5
- a4@default pgvector w3_s0p001_none: median 2.0, jobs 2.0 to 2.1; p99 median 6.0, jobs 4.2 to 126.5
- a4@default pgvector w3_s0p001_pos: median 1.9, jobs 1.7 to 1.9; p99 median 5.5, jobs 3.8 to 134.5
- a4@default pgvector w3_s0p01_neg: median 2.3, jobs 2.0 to 2.5; p99 median 4.4, jobs 3.7 to 123.5
- a4@default pgvector w3_s0p01_none: median 2.2, jobs 2.0 to 2.5; p99 median 4.1, jobs 4.0 to 124.3
- a4@default pgvector w3_s0p01_pos: median 2.2, jobs 2.0 to 2.5; p99 median 4.2, jobs 4.1 to 137.0
- a4@default pgvector w3_s0p05_neg: median 2.5, jobs 2.2 to 2.6; p99 median 4.2, jobs 4.1 to 59.6
- a4@default pgvector w3_s0p05_none: median 2.4, jobs 2.1 to 2.4; p99 median 4.1, jobs 3.9 to 73.5
- a4@default pgvector w3_s0p05_pos: median 2.4, jobs 2.1 to 2.4; p99 median 4.1, jobs 4.0 to 75.9
- a4@default pgvector w3_s0p2_neg: median 3.4, jobs 3.4 to 4.2; p99 median 5.1, jobs 4.9 to 52.1
- a4@default pgvector w3_s0p2_none: median 3.1, jobs 3.0 to 3.9; p99 median 4.7, jobs 4.4 to 56.7
- a4@default pgvector w3_s0p2_pos: median 2.8, jobs 2.8 to 3.6; p99 median 4.4, jobs 4.1 to 58.0
- a4@default pgvector w3_s0p5_neg: median 3.8, jobs 3.8 to 4.2; p99 median 6.6, jobs 6.0 to 143.4
- a4@default pgvector w3_s0p5_none: median 3.4, jobs 3.3 to 3.6; p99 median 5.1, jobs 4.9 to 157.9
- a4@default pgvector w3_s0p5_pos: median 3.1, jobs 3.0 to 3.4; p99 median 5.1, jobs 4.6 to 142.4
- a4@default qdrant w3_s0p001_neg: median 1.1, jobs 1.0 to 1.1; p99 median 1.5, jobs 1.4 to 1.7
- a4@default qdrant w3_s0p001_none: median 1.1, jobs 1.1 to 1.2; p99 median 1.6, jobs 1.4 to 1.7
- a4@default qdrant w3_s0p001_pos: median 1.1, jobs 1.0 to 1.2; p99 median 1.6, jobs 1.4 to 1.7
- a4@default qdrant w3_s0p01_neg: median 2.5, jobs 1.9 to 2.6; p99 median 3.6, jobs 2.8 to 4.1
- a4@default qdrant w3_s0p01_none: median 2.7, jobs 2.2 to 2.9; p99 median 3.9, jobs 3.1 to 4.0
- a4@default qdrant w3_s0p01_pos: median 2.3, jobs 2.0 to 2.9; p99 median 4.1, jobs 2.9 to 4.8
- a4@default qdrant w3_s0p05_neg: median 1.5, jobs 1.2 to 1.5; p99 median 2.1, jobs 1.7 to 2.6
- a4@default qdrant w3_s0p05_none: median 1.5, jobs 1.3 to 1.6; p99 median 2.2, jobs 2.0 to 2.3
- a4@default qdrant w3_s0p05_pos: median 1.5, jobs 1.3 to 1.6; p99 median 2.2, jobs 1.8 to 2.5
- a4@default qdrant w3_s0p2_neg: median 1.8, jobs 1.2 to 1.8; p99 median 2.6, jobs 1.8 to 2.6
- a4@default qdrant w3_s0p2_none: median 1.7, jobs 1.2 to 1.8; p99 median 2.5, jobs 1.7 to 2.5
- a4@default qdrant w3_s0p2_pos: median 1.7, jobs 1.2 to 1.8; p99 median 2.4, jobs 1.8 to 2.6
- a4@default qdrant w3_s0p5_neg: median 1.9, jobs 1.7 to 2.0; p99 median 2.7, jobs 2.5 to 2.8
- a4@default qdrant w3_s0p5_none: median 1.8, jobs 1.7 to 1.9; p99 median 2.5, jobs 2.4 to 2.7
- a4@default qdrant w3_s0p5_pos: median 1.8, jobs 1.8 to 1.9; p99 median 2.6, jobs 2.6 to 2.8
- a4@default milvus w3_s0p001_neg: median 3.2, jobs 2.1 to 3.8; p99 median 4.9, jobs 3.7 to 5.9
- a4@default milvus w3_s0p001_none: median 3.2, jobs 2.1 to 3.8; p99 median 4.7, jobs 3.4 to 5.6
- a4@default milvus w3_s0p001_pos: median 3.2, jobs 2.1 to 3.8; p99 median 4.9, jobs 3.4 to 6.7
- a4@default milvus w3_s0p01_neg: median 4.0, jobs 3.3 to 5.1; p99 median 5.9, jobs 4.3 to 7.3
- a4@default milvus w3_s0p01_none: median 4.1, jobs 3.6 to 5.4; p99 median 5.8, jobs 4.9 to 7.8
- a4@default milvus w3_s0p01_pos: median 4.2, jobs 3.6 to 5.7; p99 median 5.6, jobs 4.7 to 8.0
- a4@default milvus w3_s0p05_neg: median 8.3, jobs 7.3 to 8.5; p99 median 11.4, jobs 10.2 to 11.7
- a4@default milvus w3_s0p05_none: median 8.6, jobs 7.6 to 8.8; p99 median 11.6, jobs 10.6 to 11.9
- a4@default milvus w3_s0p05_pos: median 8.8, jobs 7.8 to 8.9; p99 median 11.8, jobs 10.7 to 11.9
- a4@default milvus w3_s0p2_neg: median 5.6, jobs 4.4 to 5.9; p99 median 11.9, jobs 9.5 to 12.5
- a4@default milvus w3_s0p2_none: median 4.2, jobs 3.3 to 4.4; p99 median 6.6, jobs 5.6 to 7.0
- a4@default milvus w3_s0p2_pos: median 3.6, jobs 3.0 to 4.0; p99 median 6.2, jobs 5.6 to 6.5
- a4@default milvus w3_s0p5_neg: median 5.5, jobs 4.0 to 6.1; p99 median 8.3, jobs 6.0 to 9.0
- a4@default milvus w3_s0p5_none: median 5.0, jobs 3.6 to 5.6; p99 median 7.2, jobs 5.3 to 8.0
- a4@default milvus w3_s0p5_pos: median 4.8, jobs 3.4 to 5.4; p99 median 7.2, jobs 5.4 to 8.4
- a4@default weaviate w3_s0p001_neg: median 1.8, jobs 1.7 to 1.8; p99 median 2.3, jobs 2.2 to 2.5
- a4@default weaviate w3_s0p001_none: median 1.8, jobs 1.7 to 1.9; p99 median 2.5, jobs 2.2 to 2.6
- a4@default weaviate w3_s0p001_pos: median 1.8, jobs 1.7 to 1.8; p99 median 2.6, jobs 2.3 to 2.6
- a4@default weaviate w3_s0p01_neg: median 5.3, jobs 5.1 to 5.5; p99 median 7.1, jobs 6.9 to 7.7
- a4@default weaviate w3_s0p01_none: median 5.8, jobs 5.5 to 6.0; p99 median 7.5, jobs 7.4 to 7.8
- a4@default weaviate w3_s0p01_pos: median 6.2, jobs 6.0 to 6.5; p99 median 8.2, jobs 8.1 to 8.4
- a4@default weaviate w3_s0p05_neg: median 3.5, jobs 3.3 to 5.6; p99 median 5.2, jobs 5.0 to 8.8
- a4@default weaviate w3_s0p05_none: median 3.6, jobs 3.4 to 5.3; p99 median 5.1, jobs 4.9 to 7.6
- a4@default weaviate w3_s0p05_pos: median 3.7, jobs 3.6 to 5.5; p99 median 5.5, jobs 5.2 to 8.1
- a4@default weaviate w3_s0p2_neg: median 7.0, jobs 4.1 to 7.0; p99 median 9.8, jobs 6.4 to 10.1
- a4@default weaviate w3_s0p2_none: median 6.7, jobs 4.1 to 6.7; p99 median 10.2, jobs 6.0 to 10.3
- a4@default weaviate w3_s0p2_pos: median 5.7, jobs 3.3 to 5.8; p99 median 8.8, jobs 5.8 to 9.0
- a4@default weaviate w3_s0p5_neg: median 7.4, jobs 6.6 to 9.0; p99 median 24.7, jobs 20.6 to 26.1
- a4@default weaviate w3_s0p5_none: median 5.2, jobs 4.6 to 6.6; p99 median 9.4, jobs 8.5 to 9.6
- a4@default weaviate w3_s0p5_pos: median 4.6, jobs 4.0 to 5.9; p99 median 10.5, jobs 10.1 to 10.6
- a4@default opensearch w3_s0p001_neg: median 2.4, jobs 2.1 to 2.9; p99 median 4.4, jobs 3.3 to 5.0
- a4@default opensearch w3_s0p001_none: median 2.2, jobs 2.0 to 2.6; p99 median 3.7, jobs 3.2 to 4.9
- a4@default opensearch w3_s0p001_pos: median 2.1, jobs 1.9 to 2.5; p99 median 3.5, jobs 2.9 to 4.1
- a4@default opensearch w3_s0p01_neg: median 3.0, jobs 2.9 to 4.2; p99 median 5.7, jobs 4.8 to 13.5
- a4@default opensearch w3_s0p01_none: median 2.8, jobs 2.8 to 3.9; p99 median 9.3, jobs 6.7 to 77.5
- a4@default opensearch w3_s0p01_pos: median 2.8, jobs 2.8 to 3.9; p99 median 6.9, jobs 6.1 to 17.9
- a4@default opensearch w3_s0p05_neg: median 10.0, jobs 8.0 to 10.6; p99 median 14.3, jobs 12.9 to 70.7
- a4@default opensearch w3_s0p05_none: median 9.9, jobs 7.9 to 10.6; p99 median 20.7, jobs 15.0 to 246.3
- a4@default opensearch w3_s0p05_pos: median 9.7, jobs 7.9 to 10.6; p99 median 13.3, jobs 12.4 to 70.5
- a4@default opensearch w3_s0p2_neg: median 12.2, jobs 10.3 to 12.5; p99 median 456.6, jobs 436.2 to 708.3
- a4@default opensearch w3_s0p2_none: median 12.3, jobs 10.1 to 12.3; p99 median 23.8, jobs 18.3 to 62.2
- a4@default opensearch w3_s0p2_pos: median 12.3, jobs 9.9 to 12.4; p99 median 23.5, jobs 17.0 to 27.6
- a4@default opensearch w3_s0p5_neg: median 15.2, jobs 15.0 to 15.4; p99 median 42.4, jobs 34.6 to 43.3
- a4@default opensearch w3_s0p5_none: median 15.4, jobs 15.1 to 15.8; p99 median 38.2, jobs 36.8 to 39.2
- a4@default opensearch w3_s0p5_pos: median 15.4, jobs 15.1 to 15.8; p99 median 36.7, jobs 33.1 to 41.4
- a4@iterative pgvector w3_s0p001_neg: median 1.8, jobs 1.7 to 1.9; p99 median 87.9, jobs 5.0 to 262.4
- a4@iterative pgvector w3_s0p001_none: median 2.6, jobs 2.4 to 2.6; p99 median 87.0, jobs 84.9 to 512.7
- a4@iterative pgvector w3_s0p001_pos: median 1.9, jobs 1.8 to 2.1; p99 median 77.1, jobs 72.1 to 121.1
- a4@iterative pgvector w3_s0p01_neg: median 80.7, jobs 70.0 to 89.3; p99 median 115.5, jobs 110.8 to 137.6
- a4@iterative pgvector w3_s0p01_none: median 46.6, jobs 42.1 to 49.1; p99 median 96.0, jobs 90.9 to 103.7
- a4@iterative pgvector w3_s0p01_pos: median 30.6, jobs 27.7 to 31.5; p99 median 83.1, jobs 79.3 to 87.6
- a4@iterative pgvector w3_s0p05_neg: median 46.7, jobs 46.5 to 56.9; p99 median 101.8, jobs 97.6 to 279.8
- a4@iterative pgvector w3_s0p05_none: median 13.4, jobs 13.3 to 16.2; p99 median 51.4, jobs 48.8 to 114.7
- a4@iterative pgvector w3_s0p05_pos: median 6.4, jobs 6.4 to 7.9; p99 median 54.6, jobs 52.6 to 153.0
- a4@iterative pgvector w3_s0p2_neg: median 19.1, jobs 18.9 to 21.4; p99 median 113.4, jobs 99.8 to 352.7
- a4@iterative pgvector w3_s0p2_none: median 4.7, jobs 4.5 to 5.7; p99 median 28.0, jobs 23.4 to 123.3
- a4@iterative pgvector w3_s0p2_pos: median 3.7, jobs 3.6 to 4.5; p99 median 37.7, jobs 33.6 to 98.2
- a4@iterative pgvector w3_s0p5_neg: median 5.3, jobs 4.8 to 6.1; p99 median 52.5, jobs 50.2 to 270.8
- a4@iterative pgvector w3_s0p5_none: median 3.7, jobs 3.5 to 3.7; p99 median 11.1, jobs 10.0 to 155.9
- a4@iterative pgvector w3_s0p5_pos: median 3.4, jobs 3.1 to 3.5; p99 median 11.1, jobs 10.0 to 174.5
- a4@iterative milvus w3_s0p001_neg: median 174.4, jobs 142.1 to 194.4; p99 median 437.7, jobs 399.4 to 537.7
- a4@iterative milvus w3_s0p001_none: median 76.2, jobs 62.9 to 83.0; p99 median 338.2, jobs 294.5 to 382.5
- a4@iterative milvus w3_s0p001_pos: median 29.7, jobs 24.1 to 30.9; p99 median 226.3, jobs 201.6 to 257.6
- a4@iterative milvus w3_s0p01_neg: median 52.0, jobs 51.3 to 52.6; p99 median 181.4, jobs 170.4 to 214.9
- a4@iterative milvus w3_s0p01_none: median 14.9, jobs 14.6 to 15.3; p99 median 58.7, jobs 53.9 to 69.2
- a4@iterative milvus w3_s0p01_pos: median 8.3, jobs 7.9 to 8.4; p99 median 51.9, jobs 47.0 to 59.9
- a4@iterative milvus w3_s0p05_neg: median 15.1, jobs 15.1 to 17.0; p99 median 53.9, jobs 52.9 to 61.2
- a4@iterative milvus w3_s0p05_none: median 5.1, jobs 4.9 to 5.6; p99 median 12.2, jobs 12.1 to 13.6
- a4@iterative milvus w3_s0p05_pos: median 3.7, jobs 3.7 to 4.3; p99 median 14.7, jobs 14.4 to 15.4
- a4@iterative milvus w3_s0p2_neg: median 5.5, jobs 3.7 to 6.2; p99 median 18.3, jobs 14.5 to 19.4
- a4@iterative milvus w3_s0p2_none: median 3.4, jobs 2.4 to 3.9; p99 median 5.8, jobs 4.0 to 7.6
- a4@iterative milvus w3_s0p2_pos: median 3.1, jobs 2.2 to 3.6; p99 median 7.0, jobs 5.0 to 7.6
- a4@iterative milvus w3_s0p5_neg: median 4.0, jobs 3.0 to 4.8; p99 median 8.9, jobs 7.6 to 9.6
- a4@iterative milvus w3_s0p5_none: median 3.5, jobs 2.6 to 4.2; p99 median 5.1, jobs 3.7 to 7.8
- a4@iterative milvus w3_s0p5_pos: median 3.4, jobs 2.5 to 4.1; p99 median 5.6, jobs 3.9 to 6.4
- a4@pathseer weaviate w3_s0p001_neg: median 1.8, jobs 1.7 to 2.0; p99 median 2.5, jobs 2.2 to 2.7
- a4@pathseer weaviate w3_s0p001_none: median 1.9, jobs 1.7 to 2.0; p99 median 2.6, jobs 2.4 to 2.9
- a4@pathseer weaviate w3_s0p001_pos: median 1.8, jobs 1.7 to 1.9; p99 median 2.5, jobs 2.3 to 2.8
- a4@pathseer weaviate w3_s0p01_neg: median 5.4, jobs 4.6 to 5.4; p99 median 6.8, jobs 5.9 to 7.3
- a4@pathseer weaviate w3_s0p01_none: median 5.8, jobs 5.2 to 6.0; p99 median 7.3, jobs 6.5 to 7.5
- a4@pathseer weaviate w3_s0p01_pos: median 6.3, jobs 5.6 to 6.5; p99 median 8.1, jobs 7.2 to 8.1
- a4@pathseer weaviate w3_s0p05_neg: median 12.7, jobs 11.2 to 16.7; p99 median 55.6, jobs 47.3 to 64.0
- a4@pathseer weaviate w3_s0p05_none: median 3.9, jobs 3.5 to 5.6; p99 median 10.5, jobs 7.5 to 11.4
- a4@pathseer weaviate w3_s0p05_pos: median 3.2, jobs 2.8 to 4.6; p99 median 9.9, jobs 8.4 to 11.1
- a4@pathseer weaviate w3_s0p2_neg: median 7.5, jobs 4.5 to 7.5; p99 median 16.5, jobs 11.3 to 17.7
- a4@pathseer weaviate w3_s0p2_none: median 5.8, jobs 3.5 to 5.8; p99 median 8.5, jobs 5.2 to 8.7
- a4@pathseer weaviate w3_s0p2_pos: median 5.1, jobs 3.1 to 5.1; p99 median 7.9, jobs 5.4 to 8.0
- a4@pathseer weaviate w3_s0p5_neg: median 5.8, jobs 5.5 to 7.2; p99 median 10.9, jobs 9.4 to 11.1
- a4@pathseer weaviate w3_s0p5_none: median 5.2, jobs 4.9 to 6.4; p99 median 9.4, jobs 8.5 to 10.8
- a4@pathseer weaviate w3_s0p5_pos: median 4.8, jobs 4.6 to 5.9; p99 median 8.1, jobs 7.6 to 8.6

## W3 share 0.5, A3 (engine pre-filter): failures and latency (H4)

- milvus a3-spicedb@default w3_s0p5_neg: queries 150, failed_h4 50, over_30s 50, errors 0, p50 26940.5 ms, recall 0.917
- milvus a3-spicedb@default w3_s0p5_none: queries 150, failed_h4 50, over_30s 50, errors 0, p50 26890.3 ms, recall 0.963
- milvus a3-spicedb@default w3_s0p5_pos: queries 150, failed_h4 50, over_30s 50, errors 0, p50 26899.3 ms, recall 0.969
- milvus a3-spicedb@iterative w3_s0p5_neg: queries 150, failed_h4 55, over_30s 55, errors 0, p50 27713.2 ms, recall 0.935
- milvus a3-spicedb@iterative w3_s0p5_none: queries 150, failed_h4 51, over_30s 51, errors 0, p50 27165.1 ms, recall 0.973
- milvus a3-spicedb@iterative w3_s0p5_pos: queries 150, failed_h4 50, over_30s 50, errors 0, p50 27095.8 ms, recall 0.972
- opensearch a3-spicedb@default w3_s0p5_neg: queries 150, failed_h4 150, over_30s 150, errors 0, p50 34952.0 ms, recall 0.958
- opensearch a3-spicedb@default w3_s0p5_none: queries 150, failed_h4 150, over_30s 150, errors 0, p50 34947.1 ms, recall 0.997
- opensearch a3-spicedb@default w3_s0p5_pos: queries 150, failed_h4 150, over_30s 150, errors 0, p50 34924.2 ms, recall 0.987
- pgvector a3-spicedb@default w3_s0p5_neg: queries 150, failed_h4 50, over_30s 50, errors 0, p50 21893.4 ms, recall 0.569
- pgvector a3-spicedb@default w3_s0p5_none: queries 150, failed_h4 50, over_30s 50, errors 0, p50 21976.9 ms, recall 0.902
- pgvector a3-spicedb@default w3_s0p5_pos: queries 150, failed_h4 50, over_30s 50, errors 0, p50 21934.1 ms, recall 0.898
- pgvector a3-spicedb@iterative w3_s0p5_neg: queries 150, failed_h4 50, over_30s 50, errors 0, p50 21877.3 ms, recall 0.852
- pgvector a3-spicedb@iterative w3_s0p5_none: queries 150, failed_h4 50, over_30s 50, errors 0, p50 21976.0 ms, recall 0.945
- pgvector a3-spicedb@iterative w3_s0p5_pos: queries 150, failed_h4 50, over_30s 50, errors 0, p50 21888.6 ms, recall 0.955
- qdrant a3-spicedb@acorn w3_s0p5_neg: queries 150, failed_h4 0, over_30s 0, errors 0, p50 22349.2 ms, recall 0.717
- qdrant a3-spicedb@acorn w3_s0p5_none: queries 150, failed_h4 0, over_30s 0, errors 0, p50 22366.4 ms, recall 0.915
- qdrant a3-spicedb@acorn w3_s0p5_pos: queries 150, failed_h4 0, over_30s 0, errors 0, p50 22374.1 ms, recall 0.936
- qdrant a3-spicedb@default w3_s0p5_neg: queries 150, failed_h4 0, over_30s 0, errors 0, p50 22451.1 ms, recall 0.717
- qdrant a3-spicedb@default w3_s0p5_none: queries 150, failed_h4 0, over_30s 0, errors 0, p50 22412.7 ms, recall 0.915
- qdrant a3-spicedb@default w3_s0p5_pos: queries 150, failed_h4 0, over_30s 0, errors 0, p50 22357.4 ms, recall 0.936
- weaviate a3-spicedb@default w3_s0p5_neg: queries 150, failed_h4 0, over_30s 0, errors 0, p50 18621.1 ms, recall 0.944
- weaviate a3-spicedb@default w3_s0p5_none: queries 150, failed_h4 0, over_30s 0, errors 0, p50 18565.8 ms, recall 0.960
- weaviate a3-spicedb@default w3_s0p5_pos: queries 150, failed_h4 0, over_30s 0, errors 0, p50 18635.7 ms, recall 0.961
- weaviate a3-spicedb@pathseer w3_s0p5_neg: queries 150, failed_h4 0, over_30s 0, errors 0, p50 18725.6 ms, recall 0.871
- weaviate a3-spicedb@pathseer w3_s0p5_none: queries 150, failed_h4 0, over_30s 0, errors 0, p50 18700.8 ms, recall 0.946
- weaviate a3-spicedb@pathseer w3_s0p5_pos: queries 150, failed_h4 0, over_30s 0, errors 0, p50 18619.2 ms, recall 0.960

## Permission changes (churn): delay until the answer reflects the change, s (p50, p90, max)

| store | arm | kind | events | censored | skipped | p50 | p90 | max |
|---|---|---|---|---|---|---|---|---|
| milvus | a1-fga | grant | 30 | 0 | 0 | 0.024 | 0.031 | 0.034 |
| milvus | a1-fga | revoke | 30 | 0 | 0 | 0.024 | 0.030 | 0.039 |
| milvus | a1-spicedb | grant | 30 | 0 | 0 | 0.010 | 5.028 | 5.238 |
| milvus | a1-spicedb | revoke | 30 | 0 | 0 | 4.877 | 5.067 | 5.140 |
| milvus | a2-fga-x10 | grant | 30 | 0 | 0 | 0.048 | 0.061 | 0.065 |
| milvus | a2-fga-x10 | revoke | 30 | 0 | 0 | 0.044 | 0.061 | 0.121 |
| milvus | a2-fga-x3 | grant | 30 | 0 | 0 | 0.030 | 0.041 | 0.062 |
| milvus | a2-fga-x3 | revoke | 30 | 0 | 0 | 0.028 | 0.041 | 0.042 |
| milvus | a2-spicedb-x10 | grant | 30 | 0 | 0 | 0.016 | 4.933 | 5.035 |
| milvus | a2-spicedb-x10 | revoke | 30 | 0 | 0 | 4.926 | 5.142 | 5.236 |
| milvus | a2-spicedb-x3 | grant | 30 | 0 | 0 | 0.010 | 5.044 | 5.265 |
| milvus | a2-spicedb-x3 | revoke | 30 | 0 | 0 | 4.897 | 5.129 | 5.366 |
| milvus | a3-spicedb@default | grant | 30 | 0 | 0 | 2.970 | 22.513 | 52.224 |
| milvus | a3-spicedb@default | revoke | 30 | 0 | 0 | 5.318 | 31.708 | 52.935 |
| milvus | a3-spicedb@iterative | grant | 30 | 0 | 0 | 4.964 | 21.293 | 53.360 |
| milvus | a3-spicedb@iterative | revoke | 30 | 0 | 0 | 5.585 | 31.753 | 52.410 |
| milvus | a4@default | grant | 30 | 0 | 0 | 0.160 | 0.212 | 0.213 |
| milvus | a4@default | revoke | 30 | 0 | 0 | 0.212 | 0.221 | 0.235 |
| milvus | a4@iterative | grant | 30 | 0 | 0 | 1.388 | 1.862 | 1.885 |
| milvus | a4@iterative | revoke | 30 | 0 | 0 | 0.112 | 0.216 | 0.216 |
| opensearch | a1-fga | grant | 30 | 0 | 0 | 0.035 | 0.057 | 0.242 |
| opensearch | a1-fga | revoke | 30 | 0 | 0 | 0.030 | 0.048 | 0.074 |
| opensearch | a1-spicedb | grant | 30 | 0 | 0 | 0.016 | 0.028 | 1.221 |
| opensearch | a1-spicedb | revoke | 30 | 0 | 0 | 4.784 | 5.066 | 5.159 |
| opensearch | a2-fga-x10 | grant | 30 | 0 | 0 | 0.071 | 0.138 | 0.368 |
| opensearch | a2-fga-x10 | revoke | 30 | 0 | 0 | 0.074 | 0.121 | 4.443 |
| opensearch | a2-fga-x3 | grant | 30 | 0 | 0 | 0.042 | 0.084 | 0.236 |
| opensearch | a2-fga-x3 | revoke | 30 | 0 | 0 | 0.042 | 0.068 | 0.314 |
| opensearch | a2-spicedb-x10 | grant | 30 | 0 | 0 | 0.031 | 0.117 | 0.783 |
| opensearch | a2-spicedb-x10 | revoke | 30 | 0 | 0 | 4.847 | 5.060 | 5.124 |
| opensearch | a2-spicedb-x3 | grant | 30 | 0 | 0 | 0.021 | 0.146 | 0.479 |
| opensearch | a2-spicedb-x3 | revoke | 30 | 0 | 0 | 4.802 | 5.046 | 5.138 |
| opensearch | a3-spicedb@default | grant | 30 | 0 | 0 | 7.257 | 18.004 | 27.219 |
| opensearch | a3-spicedb@default | revoke | 30 | 0 | 0 | 8.182 | 45.653 | 54.902 |
| opensearch | a4@default | grant | 30 | 0 | 0 | 0.942 | 1.047 | 1.055 |
| opensearch | a4@default | revoke | 30 | 0 | 0 | 0.976 | 1.081 | 1.910 |
| opensearch | a5-dls | grant | 30 | 0 | 0 | 0.946 | 1.047 | 1.066 |
| opensearch | a5-dls | revoke | 30 | 0 | 0 | 0.948 | 1.040 | 1.101 |
| pgvector | a1-fga | grant | 30 | 0 | 0 | 0.029 | 0.038 | 0.039 |
| pgvector | a1-fga | revoke | 30 | 0 | 0 | 0.029 | 0.040 | 0.062 |
| pgvector | a1-spicedb | grant | 30 | 0 | 0 | 0.008 | 0.010 | 0.011 |
| pgvector | a1-spicedb | revoke | 30 | 0 | 0 | 4.729 | 4.922 | 5.042 |
| pgvector | a2-fga-x10 | grant | 30 | 0 | 0 | 0.058 | 0.075 | 0.116 |
| pgvector | a2-fga-x10 | revoke | 30 | 0 | 0 | 0.058 | 0.103 | 0.119 |
| pgvector | a2-fga-x3 | grant | 30 | 0 | 0 | 0.035 | 0.039 | 0.057 |
| pgvector | a2-fga-x3 | revoke | 30 | 0 | 0 | 0.036 | 0.049 | 0.063 |
| pgvector | a2-spicedb-x10 | grant | 30 | 0 | 0 | 0.015 | 0.021 | 0.033 |
| pgvector | a2-spicedb-x10 | revoke | 30 | 0 | 0 | 4.668 | 4.923 | 5.159 |
| pgvector | a2-spicedb-x3 | grant | 30 | 0 | 0 | 0.010 | 0.013 | 0.015 |
| pgvector | a2-spicedb-x3 | revoke | 30 | 0 | 0 | 4.668 | 4.893 | 5.017 |
| pgvector | a3-spicedb@default | grant | 30 | 0 | 0 | 4.509 | 34.995 | 51.451 |
| pgvector | a3-spicedb@default | revoke | 30 | 0 | 0 | 8.118 | 30.014 | 52.221 |
| pgvector | a3-spicedb@iterative | grant | 30 | 0 | 0 | 2.220 | 22.300 | 52.456 |
| pgvector | a3-spicedb@iterative | revoke | 30 | 0 | 0 | 6.620 | 29.234 | 69.724 |
| pgvector | a4@default | grant | 30 | 0 | 0 | 0.001 | 0.001 | 0.001 |
| pgvector | a4@default | revoke | 30 | 0 | 0 | 0.004 | 0.007 | 0.010 |
| pgvector | a4@iterative | grant | 30 | 0 | 0 | 0.001 | 0.001 | 0.001 |
| pgvector | a4@iterative | revoke | 30 | 0 | 0 | 0.004 | 0.006 | 0.018 |
| pgvector | a5-rls@default | grant | 30 | 0 | 0 | 0.001 | 0.001 | 0.002 |
| pgvector | a5-rls@default | revoke | 30 | 0 | 0 | 0.006 | 0.012 | 0.014 |
| pgvector | a5-rls@iterative | grant | 30 | 0 | 0 | 0.001 | 0.001 | 0.001 |
| pgvector | a5-rls@iterative | revoke | 30 | 0 | 0 | 0.005 | 0.008 | 0.017 |
| pgvector | a7-wardowl | grant | 30 | 0 | 0 | 0.212 | 0.889 | 4.503 |
| pgvector | a7-wardowl | revoke | 30 | 0 | 0 | 4.248 | 4.817 | 5.315 |
| qdrant | a1-fga | grant | 30 | 0 | 0 | 0.029 | 0.033 | 0.035 |
| qdrant | a1-fga | revoke | 30 | 0 | 0 | 0.028 | 0.030 | 0.034 |
| qdrant | a1-spicedb | grant | 30 | 0 | 0 | 0.008 | 0.009 | 0.019 |
| qdrant | a1-spicedb | revoke | 30 | 0 | 0 | 4.835 | 5.136 | 5.152 |
| qdrant | a2-fga-x10 | grant | 30 | 0 | 0 | 0.059 | 0.070 | 0.076 |
| qdrant | a2-fga-x10 | revoke | 30 | 0 | 0 | 0.054 | 0.071 | 0.122 |
| qdrant | a2-fga-x3 | grant | 30 | 0 | 0 | 0.035 | 0.042 | 0.120 |
| qdrant | a2-fga-x3 | revoke | 30 | 0 | 0 | 0.034 | 0.040 | 0.061 |
| qdrant | a2-spicedb-x10 | grant | 30 | 0 | 0 | 0.012 | 0.015 | 0.015 |
| qdrant | a2-spicedb-x10 | revoke | 30 | 0 | 0 | 4.900 | 5.083 | 5.180 |
| qdrant | a2-spicedb-x3 | grant | 30 | 0 | 0 | 0.008 | 0.013 | 0.029 |
| qdrant | a2-spicedb-x3 | revoke | 30 | 0 | 0 | 4.958 | 5.176 | 5.300 |
| qdrant | a3-spicedb@acorn | grant | 30 | 0 | 0 | 3.094 | 22.665 | 28.212 |
| qdrant | a3-spicedb@acorn | revoke | 30 | 0 | 0 | 11.004 | 32.179 | 54.886 |
| qdrant | a3-spicedb@default | grant | 30 | 0 | 0 | 2.807 | 27.738 | 54.550 |
| qdrant | a3-spicedb@default | revoke | 30 | 0 | 0 | 3.710 | 31.999 | 56.541 |
| qdrant | a4@acorn | grant | 30 | 0 | 0 | 0.002 | 0.002 | 0.003 |
| qdrant | a4@acorn | revoke | 30 | 0 | 0 | 0.004 | 0.006 | 0.008 |
| qdrant | a4@default | grant | 30 | 0 | 0 | 0.002 | 0.002 | 0.005 |
| qdrant | a4@default | revoke | 30 | 0 | 0 | 0.003 | 0.004 | 0.004 |
| qdrant | a7-wardowl | grant | 30 | 0 | 0 | 0.352 | 0.597 | 1.128 |
| qdrant | a7-wardowl | revoke | 30 | 0 | 0 | 4.405 | 4.898 | 5.440 |
| weaviate | a1-fga | grant | 30 | 0 | 0 | 0.028 | 0.034 | 0.036 |
| weaviate | a1-fga | revoke | 30 | 0 | 0 | 0.026 | 0.033 | 0.053 |
| weaviate | a1-spicedb | grant | 30 | 0 | 0 | 0.008 | 0.010 | 0.013 |
| weaviate | a1-spicedb | revoke | 30 | 0 | 0 | 4.858 | 5.073 | 5.235 |
| weaviate | a2-fga-x10 | grant | 30 | 0 | 0 | 0.048 | 0.065 | 0.073 |
| weaviate | a2-fga-x10 | revoke | 30 | 0 | 0 | 0.051 | 0.067 | 0.129 |
| weaviate | a2-fga-x3 | grant | 30 | 0 | 0 | 0.033 | 0.041 | 0.048 |
| weaviate | a2-fga-x3 | revoke | 30 | 0 | 0 | 0.031 | 0.044 | 0.059 |
| weaviate | a2-spicedb-x10 | grant | 30 | 0 | 0 | 0.012 | 0.019 | 0.027 |
| weaviate | a2-spicedb-x10 | revoke | 30 | 0 | 0 | 4.922 | 5.062 | 5.308 |
| weaviate | a2-spicedb-x3 | grant | 30 | 0 | 0 | 0.009 | 0.017 | 0.163 |
| weaviate | a2-spicedb-x3 | revoke | 30 | 0 | 0 | 4.875 | 5.042 | 5.294 |
| weaviate | a3-spicedb@default | grant | 30 | 0 | 0 | 2.330 | 26.561 | 78.896 |
| weaviate | a3-spicedb@default | revoke | 30 | 0 | 0 | 6.882 | 50.507 | 79.415 |
| weaviate | a3-spicedb@pathseer | grant | 30 | 0 | 0 | 5.076 | 35.096 | 39.449 |
| weaviate | a3-spicedb@pathseer | revoke | 30 | 0 | 0 | 5.805 | 40.384 | 52.028 |
| weaviate | a4@default | grant | 30 | 0 | 0 | 0.002 | 0.002 | 0.002 |
| weaviate | a4@default | revoke | 30 | 0 | 0 | 0.005 | 0.009 | 0.010 |
| weaviate | a4@pathseer | grant | 30 | 0 | 0 | 0.002 | 0.002 | 0.002 |
| weaviate | a4@pathseer | revoke | 30 | 0 | 0 | 0.006 | 0.009 | 0.024 |

## Faults (engine traffic through Toxiproxy), totals per fault and arm family

| fault | arm | cells | queries | outside | errors | empty | over 30 s |
|---|---|---|---|---|---|---|---|
| cut | a1-fga | 75 | 1500 | 0 | 0 | 1017 | 0 |
| cut | a1-spicedb | 75 | 1500 | 0 | 60 | 982 | 0 |
| cut | a2-fga-x10 | 75 | 1500 | 0 | 0 | 696 | 0 |
| cut | a2-fga-x3 | 75 | 1500 | 0 | 0 | 902 | 0 |
| cut | a2-spicedb-x10 | 75 | 1500 | 0 | 495 | 459 | 0 |
| cut | a2-spicedb-x3 | 75 | 1500 | 0 | 165 | 810 | 0 |
| cut | a3-spicedb | 135 | 2700 | 0 | 2700 | 0 | 0 |
| cut | a7-wardowl | 30 | 600 | 0 | 600 | 0 | 0 |
| none | a1-fga | 75 | 1500 | 0 | 0 | 1017 | 0 |
| none | a1-spicedb | 75 | 1500 | 0 | 0 | 1017 | 0 |
| none | a2-fga-x10 | 75 | 1500 | 0 | 0 | 696 | 0 |
| none | a2-fga-x3 | 75 | 1500 | 0 | 0 | 900 | 0 |
| none | a2-spicedb-x10 | 75 | 1500 | 0 | 0 | 696 | 0 |
| none | a2-spicedb-x3 | 75 | 1500 | 0 | 0 | 902 | 0 |
| none | a3-spicedb | 135 | 2700 | 0 | 0 | 99 | 296 |
| none | a7-wardowl | 30 | 600 | 0 | 0 | 165 | 0 |
| slow | a1-fga | 75 | 1500 | 0 | 0 | 1017 | 0 |
| slow | a1-spicedb | 75 | 1500 | 0 | 0 | 1017 | 0 |
| slow | a2-fga-x10 | 75 | 1500 | 0 | 0 | 696 | 0 |
| slow | a2-fga-x3 | 75 | 1500 | 0 | 0 | 902 | 0 |
| slow | a2-spicedb-x10 | 75 | 1500 | 0 | 0 | 696 | 0 |
| slow | a2-spicedb-x3 | 75 | 1500 | 0 | 0 | 902 | 0 |
| slow | a3-spicedb | 135 | 2700 | 0 | 0 | 99 | 613 |
| slow | a7-wardowl | 30 | 600 | 0 | 600 | 0 | 0 |
| stopped | a1-fga | 75 | 1500 | 0 | 1500 | 0 | 0 |
| stopped | a1-spicedb | 75 | 1500 | 0 | 1500 | 0 | 0 |
| stopped | a2-fga-x10 | 75 | 1500 | 0 | 1500 | 0 | 0 |
| stopped | a2-fga-x3 | 75 | 1500 | 0 | 1500 | 0 | 0 |
| stopped | a2-spicedb-x10 | 75 | 1500 | 0 | 1500 | 0 | 0 |
| stopped | a2-spicedb-x3 | 75 | 1500 | 0 | 1500 | 0 | 0 |
| stopped | a3-spicedb | 135 | 2700 | 0 | 2700 | 0 | 0 |
| stopped | a7-wardowl | 30 | 600 | 0 | 600 | 0 | 0 |

