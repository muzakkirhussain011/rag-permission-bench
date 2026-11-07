"""The vector stores, behind one small interface.

Every store is loaded with the same chunks: id, the chunk's principals (`u:<user>`, `g:<group>`)
and its vector. HNSW is built with m = 16 and ef_construction = 100 everywhere, and searched with
ef = 100, so that stores differ in how they filter, not in index breadth.

`search(query, k, principals=..., ids=..., setting=...)` returns `[(chunk id, score), ...]`:

- `principals`: only chunks naming at least one of them (the store's own filter, arm A4);
- `ids`: only these chunk ids (an authorization engine's lookup, arm A3);
- neither: no filter (the base search under a post-filter, arms A1 and A2).

`setting` picks the store's filter mode: `default` is what the store does unless told otherwise;
the other names are the store's documented alternatives.
"""

from __future__ import annotations

M = 16
EF_CONSTRUCTION = 100
EF_SEARCH = 100
# The harness never cuts a search short: each store's client may wait this long for one call
# (pre-registration, section 5). Longer calls are errors; for H4 any call over 30 s counts as failed.
CALL_LIMIT_S = 600


NAMES = ("pgvector", "qdrant", "milvus", "weaviate", "opensearch")


def make(name: str):  # noqa: ANN201
    if name == "pgvector":
        from .pgvector import PgVector

        return PgVector()
    if name == "qdrant":
        from .qdrant import Qdrant

        return Qdrant()
    if name == "milvus":
        from .milvus import Milvus

        return Milvus()
    if name == "weaviate":
        from .weaviate import Weaviate

        return Weaviate()
    if name == "opensearch":
        from .opensearch import OpenSearch

        return OpenSearch()
    raise ValueError(f"unknown store {name!r}")
