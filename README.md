# rag-permission-bench

An experimental comparison of how retrieval-augmented generation (RAG) systems enforce document permissions in
vector search: post-filters, engine pre-filters, each store's own filter, database-native security, partitions and
a permission-aware library, over five vector stores and two authorization engines. This repository holds the
harness, the pre-registration and the analysis; the data and the measured outputs are its releases.

## Status

The measured runs are finished and analysed.

- The plan was deposited before any measured run: [`prereg/PREREGISTRATION.md`](prereg/PREREGISTRATION.md), release
  `prereg-v1`, [doi:10.5281/zenodo.24026269](https://doi.org/10.5281/zenodo.24026269).
- All 180 measured jobs ran in one run of the `measure` workflow at commit `d31238b`, from 2026-11-07 02:39 UTC to
  2026-11-08 06:07 UTC, each on its own GitHub-hosted `ubuntu-24.04` runner, which every job recorded as 4 CPUs and
  15.6 GiB of memory; every job finished on its first attempt. A job took 0.23 to 4.59 hours (median 0.8), 214
  runner-hours in all (GitHub's job records).
- The pre-registered analysis of their outputs (`bench.report`, `bench.figures`) is the release `results-v1`
  (2026-11-08), made by the `report` workflow at commit `d3099e9`.
- Supplementary analyses of `results-v1` (section 4 below), outside the registered analysis, are in
  [`reports/extras-results-v1/`](reports/extras-results-v1/README.md).

## What is compared

| Arm | Strategy | What runs |
|---|---|---|
| A0 | Exact control | an exact filtered scan in pgvector (index scans off); checks the harness |
| A1 | Post-filter, as shipped | auth0-ai-langchain `FGARetriever` (OpenFGA batch check) and langchain-spicedb `SpiceDBAuthFilter`, each over the store's top k (k = 10) |
| A2 | Post-filter with over-fetch | the same over 3k and 10k candidates, the first k readable kept |
| A3 | Pre-filter from the engine | langchain-spicedb `SpiceDBPreFilterRetriever` (LookupResources, then an id filter in the store) |
| A4 | The store's own filter | each store's filtered search on the chunk's readers, at its default and its documented alternative setting (OpenSearch has one setting) |
| A5 | Database-native security | PostgreSQL row-level security (pgvector); OpenSearch document-level security |
| A6 | Partitioning | one pgvector table and HNSW index per role (W2) or per user (W1), searched and merged; W1 and W2 on pgvector only |
| A7 | wardowl | one pinned commit, on pgvector and Qdrant (the author's own library) |

Stores: pgvector, Qdrant, Milvus, Weaviate, OpenSearch. Engines: SpiceDB, OpenFGA. Every version is pinned in
[`compose.yml`](compose.yml), [`requirements-run.txt`](requirements-run.txt) and
[`requirements-lock.txt`](requirements-lock.txt). Workloads: W1 Enron (real sharing from mail headers), W2
HoneyBee's four role-based generators, W3 a sweep of readable share and query-permission correlation; details in the
pre-registration, section 4.

## Releases

| Release | Files | Archived elsewhere |
|---|---|---|
| `prereg-v1` | none besides the source: the harness and the pre-registration as deposited | Zenodo [10.5281/zenodo.24026269](https://doi.org/10.5281/zenodo.24026269), the repository's source zip |
| `data-msmarco-v1` | `vectors.npy` (1,000,000 passage vectors, 384 dimensions), `queries.npy` and `questions.json` (300 dev questions), `passages.json.gz` (BEIR passage ids in order), `corpus-meta.json`, `w3-workload.tar.gz`, four `w2_*-workload.tar.gz`, `SHA256SUMS` | no |
| `data-enron-v2` | `w1-vectors.npy`, `w1-queries.npy`, `w1-workload.tar.gz`, `SHA256SUMS` | no |
| `results-v1` | `results-raw.tar.gz` (254,808,407 bytes), `report.tar.gz`, `SHA256SUMS` (both archives) | Zenodo [10.5281/zenodo.24055691](https://doi.org/10.5281/zenodo.24055691) holds the repository's source zip at the tag `results-v1`, not these three files |

Each workload archive holds the access lists (`acl.npz`, `names.json`), the measured layouts (`layouts.json`),
`meta.json` (provenance, and the SHA-256 of the vectors, questions, access lists and layouts), the exact answers with
each pair's readable share and correlation (`truth.jsonl.gz`, from `bench.truth`); W1 and W2 add a stats file, W3 the
folder of every passage (`folders.npy`) and `corpus-meta.json`.

`results-raw.tar.gz` unpacks to `artifacts/`, one folder per measured job, named
`measured-<kind>-<workload>[-<share>]-<store>-seed<n>`:

- `<job>.jsonl.gz`: every answer (hit ids, scores, latency, error), or for change jobs every change event;
- `<job>.scored.jsonl.gz` and `<job>.summary.json`: each answer scored against the exact answer (`bench.analyze`);
- `<job>.meta.json`: package versions, container images, CPU count and memory, load and index records, probes, on
  pgvector the executed plans, and on run jobs a `docker stats` snapshot after the measured pass;
- `images.txt`: `docker compose images`.

`report.tar.gz` unpacks to `report/`: `cells.json` (every cell with its intervals), `hypotheses.json`,
`faults.json`, `churn.json`, `coverage.json`, `harness.json`, `collected.tsv` (each job's artifact and workflow
run) and `figures/`. Those figures were drawn at `d3099e9`; commit `08a183b` changed only their legends and arm
labels (`bench/figures.py`), and the paper's figures were drawn by `bench.figures` at `08a183b`.

## Reproduce the paper

Everything below uses commands that exist in this repository; the workflows in
[`.github/workflows`](.github/workflows) run the same ones. Python 3.12; `gh` is the GitHub CLI.

### 1. Rebuild the report, the figures and the tables from the raw outputs

No servers are needed. From a clone of this repository:

```bash
gh release download results-v1 -R muzakkirhussain011/rag-permission-bench
sha256sum -c SHA256SUMS
tar xzf results-raw.tar.gz        # artifacts/: one folder per measured job
tar xzf report.tar.gz             # report/: the published report
pip install -r requirements-lock.txt && pip install -r requirements-run.txt -r requirements-report.txt
python -m bench.report --results artifacts --out rebuilt
python -m bench.figures --report rebuilt --out rebuilt/figures
python paper/tables.py rebuilt paper-tables
python paper/digest.py rebuilt > paper-tables/digest.md
```

The install line is the one `report.yml` uses; `bench.report` itself needs only numpy, `bench.figures` also
matplotlib, and the scripts in [`paper/`](paper) only the standard library. `bench.report` seeds every interval
from `--seed` (default 5) and the cell. Run this way in GitHub Actions (`extras` workflow run 43465687888), the
rebuild gave `cells.json`, `hypotheses.json`, `faults.json`, `churn.json`, `coverage.json` and `harness.json`
identical to the published ones ([`rebuild.json`](reports/extras-results-v1/rebuild.json)). The tables and the
digest the paper's numbers come from are made by [`paper/tables.py` and `paper/digest.py`](paper/README.md).

### 2. Re-run one measured cell

A cell is one store on one workload, with every arm and setting in one job. In GitHub Actions, run the `cell`
workflow (Actions, "cell", "Run workflow") or:

```bash
gh workflow run cell.yml -f workload=w3 -f store=pgvector -f kind=run \
  -f layouts=w3_s0p01_neg,w3_s0p01_none,w3_s0p01_pos -f seed=1 -f label=measured
```

The inputs of the 180 measured jobs are in [`measure.yml`](.github/workflows/measure.yml): W3 one job per readable
share (`layouts=w3_s<share>_neg,w3_s<share>_none,w3_s<share>_pos`, shares `0p001`, `0p01`, `0p05`, `0p2`, `0p5`);
W1 and W2 one job per workload (`workload=w1`, `w2_tree_a`, `w2_uniform_a`, `w2_erbac_a`, `w2_erbac_b`, `layouts`
empty); change and fault runs with `workload=w3 kind=churn` or `kind=faults`; five stores; seeds 1 to 3.
`label=measured` scores the run (`bench.analyze`); `label=pilot` reports timings only. The job's outputs are the
artifact `measured-<kind>-<workload>[-<share>]-<store>-seed<n>`.

The workflow downloads the data releases from the repository it runs in, and GitHub does not copy releases into a
fork: in a fork, add `GH_REPO: muzakkirhussain011/rag-permission-bench` to the `env` of the step "Fetch and check
the workload" in `cell.yml`.

Outside GitHub Actions, on a Linux machine with Docker, the same W3 job runs as the steps of `cell.yml` do:

```bash
pip install -r requirements-lock.txt && pip install -r requirements-run.txt
mkdir -p data/w3 && cd data
gh release download data-msmarco-v1 -R muzakkirhussain011/rag-permission-bench \
  -p vectors.npy -p queries.npy -p w3-workload.tar.gz -p SHA256SUMS
sha256sum -c SHA256SUMS --ignore-missing
mv vectors.npy queries.npy w3/ && tar xzf w3-workload.tar.gz -C w3 && cd ..
sudo sysctl -w vm.max_map_count=262144
docker compose --profile pgvector --profile authz up -d
python -m bench.run --workload data/w3 --store pgvector --out results/measured-run-w3-s0p01-pgvector-seed1.jsonl.gz \
  --seed 1 --layouts w3_s0p01_neg,w3_s0p01_none,w3_s0p01_pos --pairs-per-layout 0
python -m bench.analyze --workload data/w3 --run results/measured-run-w3-s0p01-pgvector-seed1.jsonl.gz
```

W1 and W2 differ in the fetch step (see `cell.yml`): W1 comes from `data-enron-v2` with its own file names, a W2
workload uses the first `n_chunks` vectors of the corpus (named in its `meta.json`), and on pgvector both add
`--partitions` for A6. `python -m bench.churn` and `python -m bench.faults` run the change and fault experiments;
fault runs send the arms' engine traffic through Toxiproxy (the environment variables are in `cell.yml`).
Latencies depend on the machine; the measured jobs saw the CPU count and memory recorded in each `.meta.json`.

### 3. Re-run the whole study

```bash
gh workflow run measure.yml -f seeds=1,2,3
gh workflow run report.yml -f prefix=measured-
```

`measure` starts the 180 jobs, at most eight at a time (the measured run took about 27.5 hours). `report` collects
the newest artifact of every job whose name starts with the prefix, runs `bench.report` and `bench.figures`, and
keeps the result as the artifact `report`; with `-f publish=true -f tag=<tag>` it also publishes the raw outputs
and the report as a release. Job artifacts expire after 90 days (`cell.yml`).

### 4. Supplementary analyses

```bash
gh workflow run extras.yml -f tag=results-v1 -f resamples=10000
```

The `extras` workflow downloads `results-v1` and the workloads' exact answers, checks their checksums, rebuilds the
report and figures from the raw outputs and compares the rebuilt report with the published one, regenerates the
paper's tables, and runs `bench.extras`: (a) the readable share each user achieved and the per-query correlation
per layout, and the W2 readable shares beside HoneyBee's; (b) p99 latency, memory, sizes and build times as the jobs
recorded them, and what was not recorded; (c) an exploratory sensitivity analysis of the registered intervals of H1
to H8 with questions resampled as clusters. None of it is the registered analysis. The outputs are the artifact
`extras`; those of run 43465687888 (commit `1260760`, 10,000 resamples) are committed in
[`reports/extras-results-v1/`](reports/extras-results-v1/README.md).

### Check the harness on synthetic data

CI ([`ci.yml`](.github/workflows/ci.yml)) runs every arm end to end on a small synthetic workload on each store.
Locally, with Docker:

```bash
pip install -r requirements-run.txt
docker compose --profile pgvector --profile authz up -d
python -m bench.devdata --out data/dev
python -m bench.truth --workload data/dev
python -m bench.run --workload data/dev --store pgvector --out results/dev-pgvector.jsonl.gz
python -m bench.analyze --workload data/dev --run results/dev-pgvector.jsonl.gz --check
```

`bench.devdata` makes a small synthetic workload for checking the harness; its numbers say nothing about any arm.

## Conflict of interest

wardowl (arm A7) is the author's own library. It is one arm among several, run at one pinned
commit, and the third-party arms run as their packages ship them.

## License

Code: Apache-2.0 ([LICENSE](LICENSE)). The data releases keep their sources' terms, which the Apache license does
not override:

- `data-msmarco-v1` (W2, W3) is derived from MS MARCO (Bajaj et al., 2016) through BEIR's copy: passage vectors and
  ids (no passage text), and the ids, text and vectors of 300 dev questions. MS MARCO is for non-commercial research
  purposes only; its terms (https://microsoft.github.io/msmarco/) apply, and uses should cite it.
- `data-enron-v2` (W1) is derived from the CMU release of the Enron email corpus (2015-05-07): message vectors,
  numeric readers and workloads, with no message text, subject or address. It replaces `data-enron-v1`, whose
  questions could repeat a subject for one user (pre-registration, section 1); the measured runs use v2 only.
- `results-v1` holds identifiers, scores, latencies, errors, load and environment records and pgvector's executed
  plans, with no passage or message text; it refers to the two data releases above, whose terms apply to them.
