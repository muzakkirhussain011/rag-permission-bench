"""Qdrant: one collection, dot product, a keyword payload index on the principals.

Settings: `default` is Qdrant's query planner (filterable HNSW, payload index or full scan as it
estimates); `acorn` also lets the planner use ACORN-1 (`SearchParams.acorn.enable`), which
Qdrant documents as an opt-in per request, with its default `max_selectivity` of 0.4.
"""

from __future__ import annotations

import time

import numpy as np

from ..util import log, retry
from ..workload import Workload
from . import EF_CONSTRUCTION, EF_SEARCH, M

URL = "http://localhost:6333"
COLLECTION = "chunks"
UPLOAD_BATCH = 2000


class Qdrant:
    name = "qdrant"
    settings = ("default", "acorn")

    def __init__(self) -> None:
        self.client = None

    def _client(self):  # noqa: ANN202
        from qdrant_client import QdrantClient

        return QdrantClient(url=URL, prefer_grpc=True, timeout=300)

    def load(self, w: Workload) -> dict:
        from qdrant_client import models

        def ready():  # noqa: ANN202
            c = self._client()
            c.get_collections()
            return c

        client = retry(ready, "Qdrant")
        if client.collection_exists(COLLECTION):
            client.delete_collection(COLLECTION)
        client.create_collection(
            COLLECTION,
            vectors_config=models.VectorParams(size=int(w.vectors.shape[1]), distance=models.Distance.DOT),
            hnsw_config=models.HnswConfigDiff(m=M, ef_construct=EF_CONSTRUCTION),
        )
        client.create_payload_index(COLLECTION, "principals", models.PayloadSchemaType.KEYWORD, wait=True)
        started = time.perf_counter()
        for start in range(0, w.n, UPLOAD_BATCH):
            stop = min(start + UPLOAD_BATCH, w.n)
            client.upsert(
                COLLECTION,
                points=models.Batch(
                    ids=list(range(start, stop)),
                    vectors=np.asarray(w.vectors[start:stop], dtype=np.float32).tolist(),
                    payloads=[{"principals": w.chunk_principals(i)} for i in range(start, stop)],
                ),
                wait=False,
            )
        loaded = time.perf_counter()
        while True:
            info = client.get_collection(COLLECTION)
            done = info.status == models.CollectionStatus.GREEN and (info.points_count or 0) >= w.n
            if done:
                break
            time.sleep(2)
        indexed = time.perf_counter()
        log(f"qdrant: {w.n} points in {loaded - started:.0f} s, indexed after {indexed - loaded:.0f} s more")
        return {
            "load_s": loaded - started,
            "index_s": indexed - loaded,
            "points": info.points_count,
            "indexed_vectors": info.indexed_vectors_count,
            "segments": info.segments_count,
        }

    def open(self) -> None:
        self.client = self._client()

    def search(
        self,
        q: np.ndarray,
        k: int,
        *,
        principals: list[str] | None = None,
        ids: list[int] | None = None,
        setting: str = "default",
    ) -> list[tuple[int, float]]:
        from qdrant_client import models

        conditions = []
        if principals is not None:
            conditions.append(models.FieldCondition(key="principals", match=models.MatchAny(any=principals)))
        elif ids is not None:
            conditions.append(models.HasIdCondition(has_id=ids))
        params = models.SearchParams(hnsw_ef=EF_SEARCH)
        if setting == "acorn":
            params = models.SearchParams(hnsw_ef=EF_SEARCH, acorn=models.AcornSearchParams(enable=True))
        response = self.client.query_points(
            COLLECTION,
            query=np.asarray(q, dtype=np.float32).tolist(),
            query_filter=models.Filter(must=conditions) if conditions else None,
            limit=k,
            search_params=params,
            with_payload=False,
            with_vectors=False,
        )
        return [(int(p.id), float(p.score)) for p in response.points]

    def close(self) -> None:
        if self.client is not None:
            self.client.close()
