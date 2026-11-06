"""OpenSearch: one index, a faiss HNSW `knn_vector` on inner product, the principals as keywords.

Setting `default`: the filter goes inside the `knn` clause, which OpenSearch documents as efficient
filtering, applied during the search. Long id lists meet OpenSearch's own limits (for example
`index.max_terms_count`, 65,536 by default); those failures are results, not harness errors.

Document-level security (arm A5) uses the security plugin: one role per principal whose DLS query
is `term` on it, each user mapped to the roles of their principals, and an unfiltered `knn` search
sent as that user. The admin account bypasses DLS and serves every other arm.
"""

from __future__ import annotations

import json
import time

import numpy as np

from ..util import log, retry
from ..workload import Workload, principals
from . import EF_CONSTRUCTION, EF_SEARCH, M

HOST, PORT = "localhost", 9200
ADMIN = ("admin", "Tq7-vector-Bench-41!")
READER_PASSWORD = "Bench-Reader-2026!"
INDEX = "chunks"


def _client(auth: tuple[str, str] = ADMIN):  # noqa: ANN202
    from opensearchpy import OpenSearch

    return OpenSearch(hosts=[{"host": HOST, "port": PORT}], http_auth=auth, use_ssl=True, verify_certs=False,
                      ssl_show_warn=False, timeout=60)


def _body(q: np.ndarray, k: int, where: dict | None) -> dict:
    knn: dict = {"vector": np.asarray(q, dtype=np.float32).tolist(), "k": k, "method_parameters": {"ef_search": EF_SEARCH}}
    if where is not None:
        knn["filter"] = where
    return {"size": k, "_source": False, "query": {"knn": {"embedding": knn}}}


class OpenSearch:
    name = "opensearch"
    settings = ("default",)

    def __init__(self) -> None:
        self.client = None
        self.readers: dict = {}

    def load(self, w: Workload) -> dict:
        from opensearchpy import helpers

        client = _client()
        retry(lambda: client.cluster.health(wait_for_status="yellow", timeout=5), "OpenSearch", timeout=600)
        if client.indices.exists(index=INDEX):
            client.indices.delete(index=INDEX)
        client.indices.create(index=INDEX, body={
            "settings": {"index": {"knn": True, "number_of_shards": 1, "number_of_replicas": 0}},
            "mappings": {"properties": {
                "principals": {"type": "keyword"},
                "embedding": {"type": "knn_vector", "dimension": int(w.vectors.shape[1]), "space_type": "innerproduct",
                              "method": {"name": "hnsw", "engine": "faiss",
                                         "parameters": {"m": M, "ef_construction": EF_CONSTRUCTION}}},
            }},
        })
        started = time.perf_counter()

        def actions():  # noqa: ANN202
            for start in range(0, w.n, 10_000):
                part = np.asarray(w.vectors[start : start + 10_000], dtype=np.float32)
                for j, vector in enumerate(part):
                    i = start + j
                    yield {"_index": INDEX, "_id": str(i), "_source": {"principals": w.chunk_principals(i),
                                                                      "embedding": vector.tolist()}}

        ok, errors = helpers.bulk(client, actions(), chunk_size=1000, request_timeout=300, raise_on_error=False)
        if errors:
            raise RuntimeError(f"OpenSearch rejected {len(errors)} documents, first: {errors[0]}")
        client.indices.refresh(index=INDEX)
        loaded = time.perf_counter()
        users = self._dls_users(client, w)
        segments = client.cat.segments(index=INDEX, format="json")
        log(f"opensearch: {ok} documents in {loaded - started:.0f} s, {len(segments)} segments, {users} DLS users,"
            f" {self.dls_roles} DLS roles")
        return {"load_s": loaded - started, "documents": ok, "segments": len(segments), "dls_users": users,
                "dls_roles": self.dls_roles, "dls_s": time.perf_counter() - loaded}

    def _dls_users(self, client, w: Workload) -> int:  # noqa: ANN001
        """One role per principal (`term` on it) and each user mapped to the roles of their principals.
        OpenSearch joins a user's DLS queries with OR. A single role per user listing all their
        principals does not work at these sizes: the security API refuses role strings over 4,096
        characters, and a DLS query is a string."""
        holders: dict[str, list[str]] = {}
        users: set[str] = set()
        for layout in w.layouts:
            for user in sorted(set(layout.user_groups) | {u for u, _ in layout.queries}):
                users.add(user)
                for p in principals(user, layout.user_groups.get(user, [])):
                    holders.setdefault(p, []).append(user)
        role = {p: "dls_" + p.replace(":", "_") for p in holders}

        def patch(path: str, ops: list[dict]) -> None:
            for start in range(0, len(ops), 500):
                client.transport.perform_request("PATCH", f"/_plugins/_security/api/{path}", body=ops[start : start + 500])

        patch("roles", [{"op": "add", "path": f"/{role[p]}", "value": {"index_permissions": [{
            "index_patterns": [INDEX], "dls": json.dumps({"term": {"principals": p}}), "allowed_actions": ["read"]}]}}
            for p in holders])
        patch("internalusers", [{"op": "add", "path": f"/{u}", "value": {"password": READER_PASSWORD}}
                                for u in sorted(users)])
        patch("rolesmapping", [{"op": "add", "path": f"/{role[p]}", "value": {"users": sorted(set(holders[p]))}}
                               for p in holders])
        self.dls_roles = len(holders)
        return len(users)

    def open(self) -> None:
        self.client = _client()

    def search(
        self,
        q: np.ndarray,
        k: int,
        *,
        principals: list[str] | None = None,
        ids: list[int] | None = None,
        setting: str = "default",
    ) -> list[tuple[int, float]]:
        where = None
        if principals is not None:
            where = {"terms": {"principals": principals}}
        elif ids is not None:
            where = {"ids": {"values": [str(i) for i in ids]}}
        result = self.client.search(index=INDEX, body=_body(q, k, where), request_timeout=30)
        return [(int(h["_id"]), float(h["_score"])) for h in result["hits"]["hits"]]

    def search_dls(self, q: np.ndarray, k: int, user: str) -> list[tuple[int, float]]:
        if user not in self.readers:
            self.readers[user] = _client((user, READER_PASSWORD))
        result = self.readers[user].search(index=INDEX, body=_body(q, k, None), request_timeout=30)
        return [(int(h["_id"]), float(h["_score"])) for h in result["hits"]["hits"]]

    def set_principals(self, i: int, principals: list[str], vector: np.ndarray) -> None:
        """An update without `refresh`: the change shows once OpenSearch refreshes (every second by default)."""
        self.client.update(index=INDEX, id=str(i), body={"doc": {"principals": principals}})

    def close(self) -> None:
        for client in [self.client, *self.readers.values()]:
            if client is not None:
                client.close()
