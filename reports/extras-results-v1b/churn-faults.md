# (h) Change and fault runs

## Change runs (`bench.churn`)

- Kinds alternate revoke, grant, revoke, ... within every job and arm: True.
- Change events by W3 share of the user's layout: {"0p001": 669, "0p01": 589, "0p05": 673, "0p2": 654, "0p5": 595}; distinct (layout, user) pairs: 611.
- `answers before it showed`: probes answered before the one that reflected the change, summed over the events. For a revocation each such answer either held the revoked chunk or raised an error (the rows keep no per-probe record), so the sum is an upper bound on answers that held a revoked chunk.

| store | arm | kind | events | answers before it showed | probes, median | probes, max |
|---|---|---|---|---|---|---|
| milvus | a1-fga | grant | 30 | 0 | 1.0 | 1 |
| milvus | a1-fga | revoke | 30 | 0 | 1.0 | 1 |
| milvus | a1-spicedb | grant | 30 | 423 | 1.0 | 50 |
| milvus | a1-spicedb | revoke | 30 | 1328 | 47.0 | 49 |
| milvus | a2-fga-x10 | grant | 30 | 0 | 1.0 | 1 |
| milvus | a2-fga-x10 | revoke | 30 | 0 | 1.0 | 1 |
| milvus | a2-fga-x3 | grant | 30 | 0 | 1.0 | 1 |
| milvus | a2-fga-x3 | revoke | 30 | 0 | 1.0 | 1 |
| milvus | a2-spicedb-x10 | grant | 30 | 358 | 1.0 | 47 |
| milvus | a2-spicedb-x10 | revoke | 30 | 1294 | 47.0 | 50 |
| milvus | a2-spicedb-x3 | grant | 30 | 417 | 1.0 | 50 |
| milvus | a2-spicedb-x3 | revoke | 30 | 1311 | 47.0 | 51 |
| milvus | a3-spicedb@default | grant | 30 | 134 | 2.0 | 28 |
| milvus | a3-spicedb@default | revoke | 30 | 130 | 2.0 | 29 |
| milvus | a3-spicedb@iterative | grant | 30 | 61 | 1.5 | 18 |
| milvus | a3-spicedb@iterative | revoke | 30 | 245 | 2.0 | 34 |
| milvus | a4@default | grant | 30 | 45 | 2.5 | 3 |
| milvus | a4@default | revoke | 30 | 46 | 3.0 | 3 |
| milvus | a4@iterative | grant | 30 | 30 | 2.0 | 2 |
| milvus | a4@iterative | revoke | 30 | 43 | 2.0 | 3 |
| opensearch | a1-fga | grant | 30 | 0 | 1.0 | 1 |
| opensearch | a1-fga | revoke | 30 | 0 | 1.0 | 1 |
| opensearch | a1-spicedb | grant | 30 | 10 | 1.0 | 11 |
| opensearch | a1-spicedb | revoke | 30 | 1191 | 44.0 | 48 |
| opensearch | a2-fga-x10 | grant | 30 | 0 | 1.0 | 1 |
| opensearch | a2-fga-x10 | revoke | 30 | 0 | 1.0 | 1 |
| opensearch | a2-fga-x3 | grant | 30 | 0 | 1.0 | 1 |
| opensearch | a2-fga-x3 | revoke | 30 | 0 | 1.0 | 1 |
| opensearch | a2-spicedb-x10 | grant | 30 | 6 | 1.0 | 7 |
| opensearch | a2-spicedb-x10 | revoke | 30 | 1220 | 43.0 | 46 |
| opensearch | a2-spicedb-x3 | grant | 30 | 0 | 1.0 | 1 |
| opensearch | a2-spicedb-x3 | revoke | 30 | 1150 | 44.0 | 46 |
| opensearch | a3-spicedb@default | grant | 30 | 31 | 1.0 | 11 |
| opensearch | a3-spicedb@default | revoke | 30 | 84 | 1.5 | 30 |
| opensearch | a4@default | grant | 30 | 263 | 10.0 | 11 |
| opensearch | a4@default | revoke | 30 | 193 | 8.0 | 10 |
| opensearch | a5-dls | grant | 30 | 154 | 6.0 | 8 |
| opensearch | a5-dls | revoke | 30 | 162 | 7.0 | 10 |
| pgvector | a1-fga | grant | 30 | 0 | 1.0 | 1 |
| pgvector | a1-fga | revoke | 30 | 0 | 1.0 | 1 |
| pgvector | a1-spicedb | grant | 30 | 0 | 1.0 | 1 |
| pgvector | a1-spicedb | revoke | 30 | 1336 | 46.0 | 49 |
| pgvector | a2-fga-x10 | grant | 30 | 0 | 1.0 | 1 |
| pgvector | a2-fga-x10 | revoke | 30 | 0 | 1.0 | 1 |
| pgvector | a2-fga-x3 | grant | 30 | 0 | 1.0 | 1 |
| pgvector | a2-fga-x3 | revoke | 30 | 0 | 1.0 | 1 |
| pgvector | a2-spicedb-x10 | grant | 30 | 0 | 1.0 | 1 |
| pgvector | a2-spicedb-x10 | revoke | 30 | 1269 | 45.0 | 51 |
| pgvector | a2-spicedb-x3 | grant | 30 | 0 | 1.0 | 1 |
| pgvector | a2-spicedb-x3 | revoke | 30 | 1261 | 45.0 | 50 |
| pgvector | a3-spicedb@default | grant | 30 | 37 | 1.0 | 16 |
| pgvector | a3-spicedb@default | revoke | 30 | 76 | 2.0 | 23 |
| pgvector | a3-spicedb@iterative | grant | 30 | 30 | 1.0 | 16 |
| pgvector | a3-spicedb@iterative | revoke | 30 | 178 | 2.0 | 33 |
| pgvector | a4@default | grant | 30 | 0 | 1.0 | 1 |
| pgvector | a4@default | revoke | 30 | 0 | 1.0 | 1 |
| pgvector | a4@iterative | grant | 30 | 0 | 1.0 | 1 |
| pgvector | a4@iterative | revoke | 30 | 0 | 1.0 | 1 |
| pgvector | a5-rls@default | grant | 30 | 0 | 1.0 | 1 |
| pgvector | a5-rls@default | revoke | 30 | 0 | 1.0 | 1 |
| pgvector | a5-rls@iterative | grant | 30 | 0 | 1.0 | 1 |
| pgvector | a5-rls@iterative | revoke | 30 | 0 | 1.0 | 1 |
| pgvector | a7-wardowl | grant | 30 | 27 | 1.0 | 28 |
| pgvector | a7-wardowl | revoke | 30 | 754 | 27.0 | 36 |
| qdrant | a1-fga | grant | 30 | 0 | 1.0 | 1 |
| qdrant | a1-fga | revoke | 30 | 0 | 1.0 | 1 |
| qdrant | a1-spicedb | grant | 30 | 0 | 1.0 | 1 |
| qdrant | a1-spicedb | revoke | 30 | 1347 | 47.0 | 50 |
| qdrant | a2-fga-x10 | grant | 30 | 0 | 1.0 | 1 |
| qdrant | a2-fga-x10 | revoke | 30 | 0 | 1.0 | 1 |
| qdrant | a2-fga-x3 | grant | 30 | 0 | 1.0 | 1 |
| qdrant | a2-fga-x3 | revoke | 30 | 0 | 1.0 | 1 |
| qdrant | a2-spicedb-x10 | grant | 30 | 0 | 1.0 | 1 |
| qdrant | a2-spicedb-x10 | revoke | 30 | 1297 | 46.0 | 49 |
| qdrant | a2-spicedb-x3 | grant | 30 | 0 | 1.0 | 1 |
| qdrant | a2-spicedb-x3 | revoke | 30 | 1338 | 48.0 | 51 |
| qdrant | a3-spicedb@acorn | grant | 30 | 13 | 1.0 | 7 |
| qdrant | a3-spicedb@acorn | revoke | 30 | 97 | 2.0 | 22 |
| qdrant | a3-spicedb@default | grant | 30 | 14 | 1.0 | 7 |
| qdrant | a3-spicedb@default | revoke | 30 | 123 | 2.0 | 28 |
| qdrant | a4@acorn | grant | 30 | 0 | 1.0 | 1 |
| qdrant | a4@acorn | revoke | 30 | 0 | 1.0 | 1 |
| qdrant | a4@default | grant | 30 | 0 | 1.0 | 1 |
| qdrant | a4@default | revoke | 30 | 0 | 1.0 | 1 |
| qdrant | a7-wardowl | grant | 30 | 0 | 1.0 | 1 |
| qdrant | a7-wardowl | revoke | 30 | 759 | 28.0 | 36 |
| weaviate | a1-fga | grant | 30 | 0 | 1.0 | 1 |
| weaviate | a1-fga | revoke | 30 | 0 | 1.0 | 1 |
| weaviate | a1-spicedb | grant | 30 | 0 | 1.0 | 1 |
| weaviate | a1-spicedb | revoke | 30 | 1341 | 47.0 | 51 |
| weaviate | a2-fga-x10 | grant | 30 | 0 | 1.0 | 1 |
| weaviate | a2-fga-x10 | revoke | 30 | 0 | 1.0 | 1 |
| weaviate | a2-fga-x3 | grant | 30 | 0 | 1.0 | 1 |
| weaviate | a2-fga-x3 | revoke | 30 | 0 | 1.0 | 1 |
| weaviate | a2-spicedb-x10 | grant | 30 | 0 | 1.0 | 1 |
| weaviate | a2-spicedb-x10 | revoke | 30 | 1343 | 47.0 | 51 |
| weaviate | a2-spicedb-x3 | grant | 30 | 0 | 1.0 | 1 |
| weaviate | a2-spicedb-x3 | revoke | 30 | 1332 | 47.0 | 51 |
| weaviate | a3-spicedb@default | grant | 30 | 49 | 1.0 | 15 |
| weaviate | a3-spicedb@default | revoke | 30 | 113 | 2.0 | 23 |
| weaviate | a3-spicedb@pathseer | grant | 30 | 83 | 1.0 | 31 |
| weaviate | a3-spicedb@pathseer | revoke | 30 | 155 | 2.0 | 36 |
| weaviate | a4@default | grant | 30 | 0 | 1.0 | 1 |
| weaviate | a4@default | revoke | 30 | 0 | 1.0 | 1 |
| weaviate | a4@pathseer | grant | 30 | 0 | 1.0 | 1 |
| weaviate | a4@pathseer | revoke | 30 | 0 | 1.0 | 1 |

## Fault runs (`bench.faults`)

- Every arm and fault of a job answered the same pairs: True.
- Every store, arm and fault of a seed answered the same pairs: True; pairs per seed: {"1": 100, "2": 100, "3": 100}; distinct pairs over the seeds: 299.
- Those pairs by W3 share: {"0p001": 48, "0p01": 51, "0p05": 69, "0p2": 61, "0p5": 70}.

| arms | fault | queries | median ms | p90 ms |
|---|---|---|---|---|
| a1-fga | cut | 1500 | 28.1 | 32.1 |
| a1-fga | none | 1500 | 29.9 | 97.5 |
| a1-fga | slow | 1500 | 2030.4 | 2033.4 |
| a1-fga | stopped | 1500 | 23.3 | 45.5 |
| a1-spicedb | cut | 1500 | 5.2 | 11.2 |
| a1-spicedb | none | 1500 | 5.7 | 17.2 |
| a1-spicedb | slow | 1500 | 2008.7 | 2015.1 |
| a1-spicedb | stopped | 1500 | 2.6 | 7.9 |
| a2-fga | cut | 3000 | 37.9 | 64.3 |
| a2-fga | none | 3000 | 39.0 | 64.1 |
| a2-fga | slow | 3000 | 2039.8 | 2064.7 |
| a2-fga | stopped | 3000 | 26.5 | 37.3 |
| a2-spicedb | cut | 3000 | 7.7 | 13.3 |
| a2-spicedb | none | 3000 | 8.6 | 16.6 |
| a2-spicedb | slow | 3000 | 2011.1 | 2020.9 |
| a2-spicedb | stopped | 3000 | 3.2 | 8.6 |
| a3-spicedb | cut | 2700 | 238.4 | 1704.0 |
| a3-spicedb | none | 2700 | 3597.9 | 32999.8 |
| a3-spicedb | slow | 2700 | 12594.8 | 42830.9 |
| a3-spicedb | stopped | 2700 | 1.4 | 1.6 |
| a7-wardowl | cut | 600 | 212.0 | 1044.8 |
| a7-wardowl | none | 600 | 407.9 | 916.4 |
| a7-wardowl | slow | 600 | 2002.2 | 2003.0 |
| a7-wardowl | stopped | 600 | 51.1 | 51.5 |
