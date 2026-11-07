# rag-permission-bench

An experimental comparison of how retrieval-augmented generation (RAG) systems enforce document
permissions in vector search. **Work in progress:** the measured runs are under way. The plan of the
study, deposited before any measured run, is [`prereg/PREREGISTRATION.md`](prereg/PREREGISTRATION.md),
archived with the harness as release `prereg-v1`:
[doi:10.5281/zenodo.24026269](https://doi.org/10.5281/zenodo.24026269).

## What is compared

| Arm | Strategy | What runs |
|---|---|---|
| A0 | Exact control | an exact filtered scan in pgvector |
| A1 | Post-filter, exact k | auth0-ai-langchain `FGARetriever` (OpenFGA); langchain-spicedb `SpiceDBAuthFilter` |
| A2 | Post-filter with over-fetch | the same over 3k and 10k candidates |
| A3 | Pre-filter from the engine | langchain-spicedb `SpiceDBPreFilterRetriever` (LookupResources, then an id filter) |
| A4 | The store's own filter | each store's filtered search, at its default and its documented alternative |
| A5 | Database-native security | PostgreSQL row-level security; OpenSearch document-level security |
| A6 | Partitioning | one collection per role; HoneyBee if licensed |
| A7 | wardowl | one pinned commit |

Stores: pgvector, Qdrant, Milvus, Weaviate, OpenSearch. Engines: SpiceDB, OpenFGA. Every version is
pinned in [`compose.yml`](compose.yml) and [`requirements-run.txt`](requirements-run.txt).

## Running it

Everything runs in GitHub Actions ([`.github/workflows`](.github/workflows)); locally it needs Docker
and Python 3.12:

```bash
pip install -r requirements-run.txt
docker compose --profile pgvector --profile authz up -d
python -m bench.devdata --out data/dev
python -m bench.truth --workload data/dev
python -m bench.run --workload data/dev --store pgvector --out results/dev-pgvector.jsonl.gz
python -m bench.analyze --workload data/dev --run results/dev-pgvector.jsonl.gz --check
```

`bench.devdata` makes a small synthetic workload for checking the harness; its numbers say nothing
about any arm.

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
