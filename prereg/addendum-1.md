# Addendum 1 to the pre-registration: exploratory follow-up runs

Author: Syed Muzakkir Hussain. Written 2026-11-20, before any of the runs it describes, and published as release
`prereg-addendum-1` of this repository (archived by Zenodo) before the first of them starts. It adds runs to the
study registered in [`PREREGISTRATION.md`](PREREGISTRATION.md) (release `prereg-v1`,
doi:10.5281/zenodo.24026269). It changes nothing in that registration: H1 to H8, their judging rules and the
analysis of the 180 measured jobs in release `results-v1` stand as they are.

## 1. Status at writing, and why these runs are exploratory

- The 180 measured jobs of the registered study are finished and analysed (release `results-v1`, 2026-11-08), and
  the supplementary analyses of them are in `reports/extras-results-v1/`. The author has read those results.
- An internal pre-submission review of the paper draft (2026-11-20) predicted a major revision. Two of its decisive
  points ask for new measurements: (D2) every store was searched at one setting of its search breadth (ef = 100),
  and the arms that filter in the store receive the user's principals from the harness, so their latency leaves
  out resolving them; (D3) in the change runs every grant follows a 10 s pause without queries and re-grants a chunk
  the same user could read 10 s earlier, while every revocation follows the previous probes at once
  (`bench/churn.py`), so the measured difference between grants and revocations may come from the protocol.
- Since the results these runs extend are known, nothing here is confirmatory. No hypothesis with a judging rule is
  registered; the runs are reported descriptively, with intervals, whatever they show. Where the review stated an
  expectation, it is listed in section 7 so that it can be reported against, not tested.
- No run described here has started. Before deposit, only continuous-integration runs on the synthetic workload
  (`bench.devdata`) will exercise the new harness code; they check that it runs and are not reported.

## 2. Questions

- **F1, search breadth.** How do recall@10 and latency of each store's own filter (A4, at each of its settings) and
  of the post-filters (A1, A2) change when the store's search breadth is 40, 100 or 400, and how far does pgvector's
  iterative scan get when `hnsw.max_scan_tuples` and `hnsw.scan_mem_multiplier` are raised? In the W3 layouts at
  shares 0.01 and 0.05, which settings reach a mean recall@10 of 0.9 (where H6 was not supported at ef = 100), and
  at what latency?
- **F2, principal lookup.** What does one lookup of the user's principals from an authorization engine add per
  query to the arms that receive them from the harness: A4, A5 with row-level security, and A6 (`bench/arms.py`;
  A0, the exact control, also receives them, but it is a check of the harness, not a strategy)? OpenSearch's
  document-level security (A5) is not among them: it sends the query as the user, and the user's roles were mapped
  at load.
- **F3, latency per job.** p50 and p99 latency per job, for every arm, setting and layout of these runs.
- **F4, change protocol.** With the same pause before revocations and grants, and grants on chunks the probed user
  could never read, do the delays of the arms that ask SpiceDB or OpenFGA at query time still differ between grants
  and revocations? What delays, and what probe latencies, do SpiceDB's per-request consistencies
  `at_least_as_fresh` (with the change's ZedToken) and `fully_consistent` give, next to the default?

## 3. What stays as in `results-v1`

Everything not named in section 4: the GitHub-hosted `ubuntu-24.04` runners and the `cell` workflow; the images in
`compose.yml` and the packages in `requirements-run.txt` and `requirements-lock.txt`; the data releases
`data-msmarco-v1` and `data-enron-v2`, checked against their SHA-256 sums in every job; how each store and engine
is loaded; HNSW with m = 16 and ef_construction = 100; k = 10; seeds 1, 2 and 3; every pair of every layout a job
runs (A0 one question per user, as registered); arms in an order drawn from the seed, each after ten unrecorded
warm-up queries; one query at a time from one client; recall@10, empty, outside and errors as defined in sections
5 and 8 of the registration. The harness changes add options whose defaults leave every registered run unchanged;
the commit the runs use is named in the report.

## 4. Runs

All runs are jobs of one new workflow, `followup.yml`, which calls `cell.yml` once per job (label `followup`), at
most twelve jobs at a time; every job runs on its own runner. W3 jobs run one readable share each, with its three
folder orders (layouts `w3_s<share>_neg`, `_none`, `_pos`; "farthest first", "random" and "nearest first").

### 4.1 Search breadth (F1, F2, F3): 36 jobs

The search breadth `ef` is set per arm: pgvector `hnsw.ef_search` (session setting), Qdrant `hnsw_ef` (per
request), Milvus `ef` (per request; at least k, as in `results-v1`), Weaviate the collection's `ef` (a mutable
index setting, switched between arms and read back before the arm runs), OpenSearch `method_parameters.ef_search`
(per request). Arms carry their setting in their name: `<arm>:ef<value>`.

- **Sweep jobs** (`plan=sweep`): W3 shares 0.01 and 0.05; pgvector, Qdrant, Milvus, Weaviate, OpenSearch; seeds 1
  to 3: 30 jobs. In each, at ef 40, 100 and 400:
  - A4 at each of the store's settings: pgvector `default` and `iterative` (`hnsw.iterative_scan = relaxed_order`,
    as registered) and `iterative-100k` (the same with `hnsw.max_scan_tuples = 100000` and
    `hnsw.scan_mem_multiplier = 5`); Qdrant `default` and `acorn`; Milvus `default` and `iterative`; Weaviate
    `default` (ACORN) and `pathseer`; OpenSearch `default`;
  - A1 and A2 as registered: `a1-fga`, `a1-spicedb`, `a2-fga-x3`, `a2-fga-x10`, `a2-spicedb-x3`, `a2-spicedb-x10`;
  - on OpenSearch, A5 with document-level security (`a5-dls`).

  At ef 100 only:
  - A4 at each of the store's two registered settings (one on OpenSearch) with a principal lookup (section 5), once
    through SpiceDB and once through OpenFGA: `a4@<setting>:ef100+lookup-spicedb`, `...+lookup-openfga`;
  - on pgvector, A5 with row-level security at both settings, alone and with each lookup; and A0.
- **Wide-scan jobs** (`plan=wide`): pgvector, W3 shares 0.01 and 0.05, seeds 1 to 3: 6 jobs, one arm each, A4 at
  `iterative-1m` (`relaxed_order`, `hnsw.max_scan_tuples = 1000000`, the table's row count, and
  `hnsw.scan_mem_multiplier = 50`) at ef 100. This arm runs in its own job because a query may then visit the whole
  index, so its time is the hardest to bound; it runs at ef 100 only, since `ef_search` sizes the initial scan and
  `max_scan_tuples` bounds the iterations after it (pgvector README, "Iterative Scan Options").

The two raised settings raise the memory limit in proportion to the tuple limit (5 times and 50 times the default
20,000 tuples and 1 times `work_mem`, 64 MB here), because pgvector's README ties them: "Try increasing this if
increasing `hnsw.max_scan_tuples` does not improve recall". On pgvector, the executed plan of one query per layout,
setting and ef is recorded, as in `results-v1` for the registered settings.

### 4.2 Principal lookup on the other workloads (F2, F3): 24 jobs

**Lookup jobs** (`plan=lookup`), pgvector only, at ef 100, seeds 1 to 3: W1 (`data-enron-v2`); W2 Tree-α,
Uniform-α, ERBAC-α, ERBAC-β; W3 shares 0.001, 0.2 and 0.5 (the shares the sweep jobs do not cover). Arms: A4 and
A5 with row-level security at both settings, and on W1 and W2 A6 (`--partitions`, as registered), each alone and
with each lookup. pgvector only, because A6 exists only there and a lookup's cost does not depend on the store;
the sweep jobs measure the lookups beside all five stores at shares 0.01 and 0.05.

### 4.3 Change diagnostic (F4): 6 jobs

W3 (users and chunks drawn from all fifteen layouts, as in `results-v1`), pgvector, seeds 1 to 3, two jobs per
seed. In both, every arm and variant makes 20 changes one at a time, alternating a revocation and a grant (10 of
each, the first a revocation), with the registered settings: probes every 0.1 s, a 60 s cap, a 10 s pause, every
change applied in parallel at both engines and the store's copy, delay from the last acknowledgement.

- **Protocols.** `published` is `bench/churn.py` as it ran in `results-v1`: a revocation empties a chunk the user
  may read, right after the previous change's last probe, and is probed at once; a grant empties a chunk the user
  may read, pauses 10 s without queries, then names the user on it. `symmetric` pauses 10 s without queries before every change; its
  revocation is the same change; its grant goes to a chunk that no user of the workload may read if any exists,
  and otherwise to a chunk the probed user could not read at any point of the job, whose readers are removed
  before the pause, so that nobody may read it during the pause and no state the user was ever served contains it.
  Each grant records which of the two it used.
- **Consistency.** `default` is what each integration sends: langchain-spicedb sends no consistency, which SpiceDB
  serves as `minimize_latency`; wardowl (A7) sends `minimizeLatency`; the OpenFGA arms send none. `at_least_as_fresh`
  adds `Consistency(at_least_as_fresh=<the ZedToken of the change's SpiceDB write>)` to every SpiceDB request of the
  arm, and `fully_consistent` adds `Consistency(fully_consistent=true)`. For the langchain-spicedb arms the harness
  sets the field on the requests the package builds (it has no option for it); for A7 it sets wardowl's
  `consistency`. Nothing else in the packages changes.
- **Job `diag-a`:** the nine arms that ask an engine at query time (`a1-fga`, `a1-spicedb`, `a2-fga-x3`,
  `a2-fga-x10`, `a2-spicedb-x3`, `a2-spicedb-x10`, `a3-spicedb@default`, `a3-spicedb@iterative`, `a7-wardowl`),
  each under `published` and `symmetric`, both at `default`.
- **Job `diag-b`:** the six that ask SpiceDB (`a1-spicedb`, `a2-spicedb-x3`, `a2-spicedb-x10`,
  `a3-spicedb@default`, `a3-spicedb@iterative`, `a7-wardowl`), each under `symmetric` at `default`,
  `at_least_as_fresh` and `fully_consistent`.

Each change job also records the output of `spicedb serve --help` for the revision-quantization flags, so the
defaults the server ran with are on record.

### 4.4 Time limits and re-runs

Every run job stops starting new queries, and every change job new changes, after 5 hours of measuring
(`--budget-s 18000`), so that it can finish, score and upload inside GitHub's 6-hour job limit. Answers or changes
not reached are reported as not run, with their counts; arms run in a seed-drawn order and an arm's pairs in a
seed-drawn order, so what does run is not chosen by layout or user. A job that fails for an infrastructure reason is
run again with the same seed, and the newest finished attempt is analysed. No job is run again because of its
results.

## 5. Measures

As registered (sections 5 and 8 of `PREREGISTRATION.md`), plus:

- **Principal lookup.** A lookup arm asks the engine which groups the user is a member of, then runs the arm's
  search with `u:<user>` and those groups as the principals. SpiceDB: `LookupResources` (resource type `group`,
  relation `member`, subject the user) over gRPC, with no consistency field, as the langchain-spicedb arms send.
  OpenFGA: `ListObjects` (type `group`, relation `member`) through the openfga-sdk client, with no consistency, as
  the FGA arms send. Recorded per query: the lookup's time, the search's time, their sum (the arm's latency), the
  number of groups returned and whether they equal the harness's list for that user.
- **Per-job latency.** p50 and p99 of each job, per arm and layout (for lookup arms, of the lookup, the search and
  the sum), as well as their median and range over the jobs.
- **Change probes.** For every probe of a change: the time since the last acknowledgement, the probe's own latency,
  and whether the answer held the changed chunk or raised an error. From these: the probes that still returned a
  revoked chunk before the change showed, and the delay minus the latency of the probe that showed it.

## 6. Analysis

`bench.followup` makes the report in GitHub Actions from the jobs' outputs and from release `results-v1`:

- Every cell (workload, store, arm with its setting, ef and lookup, layout) as `bench.report` computes it: recall
  averaged per user and then over users, a failed query counting as recall 0, with a 95% bootstrap interval over
  users (10,000 resamples, seed 5 and the cell); empty, outside and error counts; p50 and p99 per job and their
  median and range. No Bonferroni correction and no verdicts: there is no hypothesis.
- **F1.** Per store, setting, layout and ef: recall with its interval, and the p50 and p99 medians. For each of the
  six layouts, the settings whose mean recall reaches 0.9 and those whose interval lies wholly at or above 0.9, with
  their p50 and p99.
- **F2.** Per workload (W3 per share) and engine: the lookup's p50 and p99 per job; each lookup arm's search and
  total p50 and p99 beside the same arm without a lookup in the same job; queries whose looked-up principals
  differed from the harness's.
- **F3.** A table of every job, arm and layout with its query count, p50 and p99.
- **F4.** Per arm, protocol, consistency and kind of change: changes made, censored, skipped, the delay's median,
  90th percentile and maximum, the probes that still returned a revoked chunk, and the delay less the last probe's
  latency; which grant pool each protocol used; and the published protocol's delays in these jobs beside
  `results-v1`'s pgvector change runs.
- **Reproduction of `results-v1`.** Every cell these runs measure at ef 100 under the same name as a `results-v1`
  cell (the sweep jobs' `<arm>:ef100` and the lookup jobs' arms without a lookup) is compared with it: both means,
  their difference, and whether `results-v1`'s mean lies inside the follow-up's 95% interval; p50 and p99 medians
  side by side. The report lists every cell, the largest difference and every cell outside the interval; it does
  not treat differences as errors or hide them.

The raw outputs and the report are published together as release `followup-v1` (`results-raw.tar.gz`,
`report.tar.gz`, `SHA256SUMS`), as `results-v1` was.

## 7. What the review expected, to report against

These are the review's expectations, written down so that the report can say whether the runs bore them out; they
are not hypotheses of this study.

- Under the symmetric protocol, both kinds of change through SpiceDB at the default consistency would show delays
  spread between 0 and about 5.5 s, rather than about 5 s for revocations and milliseconds for grants.
- `at_least_as_fresh` with the change's token, and `fully_consistent`, would reflect changes at the first probe.
- Some of H6's failures at shares 0.01 and 0.05 may be reached by a wider search, on pgvector by raising
  `hnsw.max_scan_tuples`, at a cost in latency.

## 8. Deviations

Any departure from this addendum (a job that cannot run, an arm that fails on a store, a setting a store refuses,
a change of plan) is dated, explained and listed in the report and in the paper. Cells that cannot run are reported
as not run, with the reason.

## Record of the runs and their deviations (added 2026-11-21, after the runs)

This section was added after the runs ended; nothing above it has changed since release `prereg-addendum-1`.

- **The runs.** All 66 jobs ran in run 44809360668 of the `followup` workflow at commit `1ed8977`, from 2026-11-20
  20:13 UTC to 2026-11-21 01:38 UTC, at most twelve at a time, each on its own GitHub-hosted runner. Every job ran
  once. No job reached the 5-hour budget.
- **An addition to the analysis (section 6).** On 2026-11-20, while the runs were in progress and after the first
  jobs had finished, the check against `results-v1` was extended to give each job's own recall in every compared
  cell, from the raw outputs of both runs, and each job's store load record (pull request #8; report code only).
  The reason was a result already seen: the first finished Qdrant sweep job (share 0.01, seed 1) recalled 0.983 at
  the default setting on the farthest-first layout, where `results-v1`'s cell, pooled over its three jobs, is
  0.917, and a comparison of pooled means cannot show whether one job or all of them differ. Nothing else in the
  analysis changed.
- **Grants under the symmetric protocol (section 4.3).** W3 has no chunk that no user of the workload may read
  (every change job recorded 0 such chunks), so every symmetric grant went to the second pool: a chunk the probed
  user could not read at any point of the job, emptied of its readers before the pause.
- **One job recorded as cancelled.** Job 136616467426, `sweep w3 s0p05 opensearch seed 3`, was still measuring after
  2.9 hours, while the other five OpenSearch sweep jobs had taken 0.79 to 0.87 hours, and its log could not be read
  while it ran (GitHub's API serves a job's log only once the job ends). At 01:38 UTC the run was cancelled so that
  the job could be run again with the same seed (section 4.4). The log, readable once the job had ended, shows that
  the job had already finished: it had answered every query of every arm (78,000 answers, no errors), scored them
  (its measuring step ended at 01:38:31) and uploaded its complete outputs (01:38:34) by the time the cancellation
  reached it, and GitHub then recorded the job, with the run, as cancelled. The job was not run again, and its outputs are analysed like every other job's. Its
  five A4 arms took 1,322 to 1,939 s each; at ef 100 without a lookup, their p50 was 385 to 536 ms per layout,
  against 7.6 to 10.3 ms in that cell's other two jobs.
