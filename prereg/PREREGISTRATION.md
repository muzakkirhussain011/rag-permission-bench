# Pre-registration (DRAFT, not deposited): enforcing document permissions in vector search

Author: Syed Muzakkir Hussain. Draft of 2026-11-06, first made public in this repository the same day. Until the
Zenodo deposit, which comes before the first measured run, every change to this file is visible in its git history.
Changes after deposit go in a dated amendments section at the end, never in place.

## 1. Status at writing

- No measured run of this study exists. Pilots only check that the harness runs and how long each arm takes:
  `bench.timing` reports their latencies and errors, recall is never computed for them, and they are never reported.
  Pilot latencies and errors bear on H4; H1 to H8 were committed publicly (commit c757b4c, 2026-11-06) before any
  run on real data, and their wording has not changed since.
- What the author already knows: the source code and documentation of the integrations and stores named in section 3,
  read 2026-11-06 (notes file); results of the author's earlier preprint on wardowl ("Testing Permission-Aware
  Retrieval for RAG across Vector Stores and Authorization Engines", archive 10.5281/zenodo.23874614), which used other
  data and measured only wardowl, plus one row-level-security side run. wardowl is the author's own library: a declared
  conflict of interest.
- Seen while testing the harness, before deposit: the CI runs on a small synthetic workload (random vectors, 3,000
  chunks; `bench.devdata`), whose numbers check the harness and say nothing about any arm. One observation is
  disclosed because it shapes an arm: auth0-ai-langchain 1.0.1's `FGARetriever.ainvoke` raised
  `TypeError: unhashable type: 'Document'` on every store (langchain-core 0.3.86, the newest its package allows).
  Arm A1-FGA therefore uses `invoke`, as Auth0's README does, and the async failure is reported as a finding.
  Also seen on that synthetic workload, and disclosed because they concern exploratory measures: OpenSearch
  document-level security (A5) returned fewer than k hits for users who may read few chunks; and in the short
  change runs, revocations took about 2 s to show on arms that ask SpiceDB, and under 0.2 s on the others.

## 2. Questions

- **Q1 quality:** how much of the readable top 10 does each arm return, by readable share and by query-permission correlation?
- **Q2 cost:** latency, throughput, memory, storage, build time.
- **Q3 change:** after a grant or revocation at the source, how long until answers reflect it, and what does it cost?
- **Q4 failure:** when a part fails, does an arm return chunks outside the readable set, return nothing, or raise an error?

## 3. Arms

| Arm | Strategy | Implementation, pinned version |
|---|---|---|
| A0 | Exact control | pgvector with index scans off and the user's principals as a filter; checks the harness |
| A1 | Post-filter, exact k | auth0-ai-langchain `FGARetriever` 1.0.1 on a self-hosted OpenFGA; langchain-spicedb 0.2.0 `SpiceDBAuthFilter` |
| A2 | Post-filter, over-fetch | A1 with 3k and with 10k candidates, then the first k readable |
| A3 | Engine pre-filter | langchain-spicedb 0.2.0 `SpiceDBPreFilterRetriever`, under each store setting |
| A4 | Reader groups on chunks | each store's filtered search at its default and at its documented alternative setting |
| A5 | Database-native | PostgreSQL row-level security with pgvector; OpenSearch document-level security |
| A6 | Partitioning | one pgvector table and HNSW index per role (W2) or per user (W1), searched and merged; HoneyBee if its authors license the code |
| A7 | wardowl | one commit, pinned before deposit, on pgvector and Qdrant |

Stores: pgvector, Qdrant, Milvus, Weaviate, OpenSearch; exact versions in `compose.yml` and the lock file, image
digests recorded with every run. HNSW is built with m = 16 and ef_construction = 100 and searched with ef = 100 on
every store, so that stores differ in how they filter, not in index breadth. Engines: SpiceDB and OpenFGA, both on
PostgreSQL, pinned the same way. Third-party integrations run as installed from PyPI; the harness only supplies the
store underneath them. k = 10 throughout.

## 4. Workloads

- **W1 Enron**, CMU release 2015-05-07. Messages deduplicated by Message-ID, then by a hash of subject and body
  (readers merged). One chunk per
  message: subject plus body, cut at the embedding model's limit. Readers: the addresses in From, To, Cc and Bcc.
  Users: the addresses that can read at least 50 messages; 200 sampled, stratified by readable count (seed fixed).
  Queries: per user, 10 subjects of messages that user can read ("own mail") and 10 subjects of messages they cannot
  ("other mail"); subjects of fewer than three words are skipped. Addresses are replaced by numbers before any output.
- **W2 RBAC generators**: Tree-α, Uniform-α, ERBAC-α and ERBAC-β with HoneyBee's published parameters (its section
  6.2), 1,000 users, 100 roles, re-implemented from the paper's text (its code has no license; choices where the text
  is silent are stated in `bench/w2.py`), over the first 200,000 MS MARCO passages, so that per-role partitions (arm
  A6) fit a runner. 100 users drawn at random, 10 questions each. The achieved readable shares are reported beside
  HoneyBee's Table 1; no claim of an exact replication is made.
- **W3 sweep**: the W2 corpus and questions. Readable share s in {0.001, 0.01, 0.05, 0.2, 0.5}; correlation in
  {negative, none, positive}. The corpus is split into k-means clusters (k = 1,000), each a folder that a user is
  granted whole. Positive grants the folders nearest the user's questions, none grants folders in random order,
  negative grants the farthest, each until the share is reached. The achieved share and correlation (Amanbayev et
  al.'s rho_q) are measured per query and reported; cells are labeled by what was achieved.
- **Churn** (`bench.churn`, fresh servers): per cell and arm, 20 changes one at a time, alternating a revocation (a
  chunk a measured user may read loses every reader) and a grant (a chunk nobody may read, left to settle 10 s, gains
  the user as a reader). Each change is applied in parallel at both engines and the store's copy of the chunk's
  principals, as a sync job would. The probe is the chunk's own vector, asked every 100 ms until the answer reflects
  the change, capped at 60 s.
- Embeddings: BAAI/bge-small-en-v1.5 through fastembed's ONNX build on CPU, normalized, computed once in GitHub
  Actions; the model file's and every output file's SHA-256 are published.

## 5. Measures

- **Recall@10**: |returned ∩ exact readable top 10| / min(10, readable count). Exact top 10: brute force over the
  user's readable chunks, inner product on normalized vectors, ties broken by chunk id; computed once and stored.
- **Empty answer**: zero hits for a user who can read at least 10 chunks.
- **Outside**: any returned chunk not in the user's readable set at query time. Counted in every run, not only fault runs.
- **Latency**: wall time from the call into the arm to its return, embedding excluded; p50 and p99 per job.
- **Throughput**: not measured with concurrent clients; every arm answers one query at a time from one client.
- **Memory and storage**: store-reported index and data size where the store reports it; container memory after the
  measured pass (`docker stats`).
- **Build time**: load and index time to queryable.
- **Change delay**: time from the last source acknowledging a change to the first probe that reflects it; each
  source's write latency is recorded too; probes still wrong at 60 s are reported as censored.
- **Faults** (`bench.faults`): the arms that ask an engine at query time answer 100 pairs through a proxy (Toxiproxy)
  under each of: no fault; engine connections refused; 2 s added to every engine response; engine connections closed
  after 16 KiB, which ends long LookupResources streams part-way. ID lists above a store's limits are observed in the
  main runs (A3 at large shares), not injected. For each: outside, empty and error counts.

## 6. Procedure

- Every measured run is a GitHub Actions job on a GitHub-hosted runner from the public repository's docker compose files.
- A cell is (workload, store, setting). Every arm that can run on a cell runs in the same job, in an order drawn from a
  seed logged with the job; one warm-up pass per arm is discarded.
- At least five jobs per cell, on different runners. Comparisons between arms are made within a job.
- Raw outputs kept for every query: the k hit ids with scores, latency, errors.

## 7. Hypotheses

Bonferroni over the eight: each is judged on a two-sided 99.375% interval (0.05 / 8). **Supported** if the interval lies
wholly on the predicted side, **not supported** if wholly on the other side, otherwise **inconclusive**.

- **H1** On W1 own-mail queries, A1 mean recall@10 is below 0.5.
- **H2** On W1 own-mail queries, A2 with 10k candidates has mean recall@10 below 0.9.
- **H3** In W3, at every share up to 0.05, A1 and A2 mean recall@10 is lower under negative than under positive correlation.
- **H4** In W3 at share 0.5, A3 fails (error or timeout at 30 s) or has p50 latency above 10 s on at least one store.
- **H5** In W3 at share 0.01, pgvector HNSW with iterative scans off has mean recall@10 below 0.5.
- **H6** In W3, A4 at each store's alternative setting (pgvector iterative scans, Qdrant ACORN, Milvus iterative
  filter, Weaviate PathSeer, OpenSearch efficient filtering) has mean recall@10 of at least 0.9 in every cell.
- **H7** In W3, A5 on pgvector and A4 on pgvector with the same scan settings differ in mean recall@10 by less than 0.02.
- **H8** With the engine stopped, no arm returns a chunk outside the readable set.

How each is judged (`bench/report.py`). A hypothesis over several cells is supported only if it is supported in every
cell, not supported if it is not supported in any cell, and inconclusive otherwise (an intersection-union rule, so
each cell's interval keeps the 99.375% level).

- H1, H2: cells are (store, implementation) on W1's own-mail pairs; the implementations are FGA and SpiceDB, which
  post-filter the same base search.
- H3: cells are (store, share 0.001, 0.01 or 0.05, post-filter arm); the interval is for mean(negative) minus
  mean(positive), with the users of each layout resampled independently; predicted side: below 0.
- H4: per store, the A3 cells at share 0.5 (both store settings, three correlations) meet the condition if in every
  one more than half the queries failed or the median of the jobs' p50 latencies exceeds 10 s. Supported if at least
  one store meets it, not supported otherwise. No interval: these are counts and medians.
- H5: cells are the three correlation layouts at share 0.01.
- H6: cells are (store, layout) for the five alternative settings and fifteen layouts; supported where the lower end
  is at least 0.9, not supported where the upper end is below 0.9.
- H7: cells are (setting default or iterative, layout); the interval is for the per-user mean of paired differences
  (A5 minus A4, same job, user and question); supported where it lies inside (-0.02, 0.02), not supported where it
  lies wholly outside.
- H8: a count over every fault run with engines refusing connections; supported if it is zero.

## 8. Analysis

- Unit: the user. Per-query values are averaged per user, then over users.
- Intervals: bootstrap over users, 10,000 resamples, seed fixed in the analysis script; latency intervals over jobs.
- Paired differences between arms use the same queries and the same users, from the same jobs.
- All cells are reported, including those no hypothesis covers. Failed or censored measurements are counted, not dropped.

## 9. Exploratory (no hypothesis, reported as such)

Change delays per arm; costs of a change; OpenSearch DLS hit counts (security#6737 concerns hybrid queries; plain
knn under DLS is untested in the docs read); W2 against HoneyBee's published numbers; other-mail queries on W1.

## 10. Deviations

Any change to arms, workloads, measures, procedure or analysis after deposit is dated, explained and listed in the
paper. Cells that cannot run (for example a store that cannot take an arm) are reported as not run, with the reason.

## Amendments

None yet.
