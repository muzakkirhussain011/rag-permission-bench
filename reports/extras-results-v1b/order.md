# (i) Arm order and latency

Arms run one after another in an order drawn from each job's seed, each after ten unrecorded warm-up queries. For every cell (workload, store, arm, layout) whose jobs placed the arm at different positions, this compares the arm's p50 latency across its jobs. If position and latency were unrelated, the job that ran the arm earliest would be the slowest in about a third of three-job cells, and an earlier job would be the slower one in about half of the job pairs. Jobs also ran on different runners, which adds noise but not bias, since the order is drawn independently of the runner.

- Cells compared: 1085; the earliest job was the slowest in 369 (about 362 expected if unrelated).
- Job pairs at different positions: 3020; the earlier one was slower in 0.500 of them.
- Median ratio of the earliest job's p50 to the latest job's: 0.987.

## Cells with calls over 30 s, by job

H4 counts a call over 30 s as failed. Per job: calls over 30 s of the job's calls, and the job's p50.

| workload | store | arm | layout | jobs: over 30 s / calls (p50 ms) |
|---|---|---|---|---|
| w3 | milvus | a3-spicedb@default | w3_s0p5_neg | 0/50 (21328); 0/50 (26941); 50/50 (34218) |
| w3 | milvus | a3-spicedb@default | w3_s0p5_none | 0/50 (21340); 0/50 (26890); 50/50 (34360) |
| w3 | milvus | a3-spicedb@default | w3_s0p5_pos | 0/50 (21325); 0/50 (26899); 50/50 (34277) |
| w3 | milvus | a3-spicedb@iterative | w3_s0p5_neg | 0/50 (21572); 5/50 (27713); 50/50 (35601) |
| w3 | milvus | a3-spicedb@iterative | w3_s0p5_none | 0/50 (21270); 1/50 (27165); 50/50 (34713) |
| w3 | milvus | a3-spicedb@iterative | w3_s0p5_pos | 0/50 (21224); 0/50 (27096); 50/50 (34630) |
| w3 | opensearch | a3-spicedb@default | w3_s0p5_neg | 50/50 (33920); 50/50 (34952); 50/50 (35672) |
| w3 | opensearch | a3-spicedb@default | w3_s0p5_none | 50/50 (34006); 50/50 (34947); 50/50 (35801) |
| w3 | opensearch | a3-spicedb@default | w3_s0p5_pos | 50/50 (34040); 50/50 (34924); 50/50 (35856) |
| w3 | pgvector | a3-spicedb@default | w3_s0p5_neg | 0/50 (21893); 0/50 (21148); 50/50 (35093) |
| w3 | pgvector | a3-spicedb@default | w3_s0p5_none | 0/50 (21977); 0/50 (21138); 50/50 (35115) |
| w3 | pgvector | a3-spicedb@default | w3_s0p5_pos | 0/50 (21934); 0/50 (21185); 50/50 (35173) |
| w3 | pgvector | a3-spicedb@iterative | w3_s0p5_neg | 0/50 (21877); 0/50 (21049); 50/50 (34991) |
| w3 | pgvector | a3-spicedb@iterative | w3_s0p5_none | 0/50 (21976); 0/50 (21054); 50/50 (35003) |
| w3 | pgvector | a3-spicedb@iterative | w3_s0p5_pos | 0/50 (21889); 0/50 (21052); 50/50 (34929) |
