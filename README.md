# rag-permission-bench

An experimental comparison of how retrieval-augmented generation (RAG) systems enforce document
permissions in vector search. **Work in progress:** the harness is being built and no measured
results exist yet. The plan of the study, written before any measured run, is in
[`prereg/PREREGISTRATION.md`](prereg/PREREGISTRATION.md).

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

Code: Apache-2.0 ([LICENSE](LICENSE)). Datasets keep their own terms, stated with each workload.
