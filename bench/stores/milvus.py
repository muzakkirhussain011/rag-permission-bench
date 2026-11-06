"""Milvus: one collection, HNSW on inner product, an inverted index on the principals array.

Settings: `default` is Milvus's standard filtered search; `iterative` adds the `iterative_filter`
hint, which Milvus documents as searching in iterations until k results pass the filter.
Filters use templates (`filter_params`), so a long id list is sent as data, not pasted into text.
"""

from __future__ import annotations

import time

import numpy as np

from ..util import log, retry
from ..workload import Workload
from . import EF_CONSTRUCTION, EF_SEARCH, M

URI = "http://localhost:19530"
COLLECTION = "chunks"
MAX_PRINCIPALS = 4096
BATCH = 5000


class Milvus:
    name = "milvus"
    settings = ("default", "iterative")

    def __init__(self) -> None:
        self.client = None

    def _client(self):  # noqa: ANN202
        from pymilvus import MilvusClient

        client = MilvusClient(uri=URI, timeout=60)
        client.list_collections()
        return client

    def load(self, w: Workload) -> dict:
        from pymilvus import DataType, MilvusClient

        client = retry(self._client, "Milvus", timeout=600)
        if client.has_collection(COLLECTION):
            client.drop_collection(COLLECTION)
        widest = int(max(np.diff(w.user_ptr).max(initial=0) + np.diff(w.group_ptr).max(initial=0), 1))
        if widest > MAX_PRINCIPALS:
            raise ValueError(f"a chunk names {widest} principals; Milvus arrays here hold {MAX_PRINCIPALS}")
        schema = MilvusClient.create_schema(auto_id=False, enable_dynamic_field=False)
        schema.add_field("id", DataType.INT64, is_primary=True)
        schema.add_field("principals", DataType.ARRAY, element_type=DataType.VARCHAR, max_capacity=MAX_PRINCIPALS,
                         max_length=128)
        schema.add_field("embedding", DataType.FLOAT_VECTOR, dim=int(w.vectors.shape[1]))
        index = client.prepare_index_params()
        index.add_index(field_name="embedding", index_type="HNSW", metric_type="IP",
                        params={"M": M, "efConstruction": EF_CONSTRUCTION})
        index.add_index(field_name="principals", index_type="INVERTED")
        client.create_collection(COLLECTION, schema=schema, index_params=index)
        started = time.perf_counter()
        for start in range(0, w.n, BATCH):
            stop = min(start + BATCH, w.n)
            part = np.asarray(w.vectors[start:stop], dtype=np.float32)
            client.insert(COLLECTION, [{"id": i, "principals": w.chunk_principals(i), "embedding": part[i - start].tolist()}
                                       for i in range(start, stop)])
        client.flush(COLLECTION)
        loaded = time.perf_counter()
        while True:
            info = client.describe_index(COLLECTION, "embedding")
            if int(info.get("indexed_rows", 0)) >= w.n and int(info.get("pending_index_rows", 0)) == 0:
                break
            time.sleep(2)
        client.load_collection(COLLECTION)
        indexed = time.perf_counter()
        log(f"milvus: {w.n} rows in {loaded - started:.0f} s, indexed and loaded after {indexed - loaded:.0f} s more")
        return {"load_s": loaded - started, "index_s": indexed - loaded, "index": {k: str(v) for k, v in info.items()}}

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
        params: dict = {"params": {"ef": max(EF_SEARCH, k)}}
        if setting == "iterative":
            params["hints"] = "iterative_filter"
        expression, values = "", {}
        if principals is not None:
            expression, values = "array_contains_any(principals, {p})", {"p": principals}
        elif ids is not None:
            expression, values = "id in {ids}", {"ids": ids}
        result = self.client.search(
            COLLECTION, data=[np.asarray(q, dtype=np.float32).tolist()], anns_field="embedding", filter=expression,
            filter_params=values, limit=k, search_params=params, output_fields=[], timeout=30,
        )
        return [(int(hit["id"]), float(hit["distance"])) for hit in result[0]]

    def close(self) -> None:
        if self.client is not None:
            self.client.close()
