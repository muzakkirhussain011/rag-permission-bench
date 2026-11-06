"""Weaviate: one collection, HNSW on dot product, the principals as a filterable text array.

Settings: `default` is ACORN, the filter strategy Weaviate 1.40 uses unless told otherwise (set
explicitly so a change of server default cannot slip in); `pathseer` switches the collection to
PathSeer, added in 1.40. The strategy is a mutable index setting, so the run switches it between
arms; the strategy in force is read back and recorded.
Chunks get UUIDs derived from their ids; an id filter is a filter on those UUIDs.
"""

from __future__ import annotations

import time

import numpy as np

from ..util import log, retry
from ..workload import Workload
from . import EF_CONSTRUCTION, EF_SEARCH, M

HOST, PORT, GRPC_PORT = "localhost", 8090, 50061
COLLECTION = "Chunk"


def _uuid(i: int) -> str:
    from weaviate.util import generate_uuid5

    return generate_uuid5(i)


class Weaviate:
    name = "weaviate"
    settings = ("default", "pathseer")

    def __init__(self) -> None:
        self.client = None
        self.collection = None
        self.setting = None

    def _connect(self):  # noqa: ANN202
        import weaviate

        client = weaviate.connect_to_local(host=HOST, port=PORT, grpc_port=GRPC_PORT)
        if not client.is_ready():
            client.close()
            raise RuntimeError("Weaviate is not ready")
        return client

    def load(self, w: Workload) -> dict:
        from weaviate.classes.config import Configure, DataType, Property, Tokenization, VectorDistances

        client = retry(self._connect, "Weaviate")
        if client.collections.exists(COLLECTION):
            client.collections.delete(COLLECTION)
        client.collections.create(
            COLLECTION,
            vectorizer_config=Configure.Vectorizer.none(),
            vector_index_config=Configure.VectorIndex.hnsw(
                distance_metric=VectorDistances.DOT, ef_construction=EF_CONSTRUCTION, max_connections=M, ef=EF_SEARCH,
            ),
            properties=[
                Property(name="cid", data_type=DataType.INT),
                Property(name="principals", data_type=DataType.TEXT_ARRAY, tokenization=Tokenization.FIELD,
                         index_filterable=True),
            ],
        )
        collection = client.collections.get(COLLECTION)
        started = time.perf_counter()
        with collection.batch.fixed_size(batch_size=1000, concurrent_requests=2) as batch:
            for start in range(0, w.n, 10_000):
                part = np.asarray(w.vectors[start : start + 10_000], dtype=np.float32)
                for j, vector in enumerate(part):
                    i = start + j
                    batch.add_object(properties={"cid": i, "principals": w.chunk_principals(i)}, uuid=_uuid(i),
                                     vector=vector.tolist())
        failed = collection.batch.failed_objects
        if failed:
            raise RuntimeError(f"Weaviate rejected {len(failed)} objects, first: {failed[0].message}")
        loaded = time.perf_counter()
        count = collection.aggregate.over_all(total_count=True).total_count
        client.close()
        log(f"weaviate: {count} objects in {loaded - started:.0f} s")
        return {"load_s": loaded - started, "objects": count}

    def open(self) -> None:
        self.client = self._connect()
        self.collection = self.client.collections.get(COLLECTION)

    def configure(self, setting: str) -> None:
        from weaviate.classes.config import Reconfigure, VectorFilterStrategy

        if setting == self.setting:
            return
        strategy = VectorFilterStrategy.PATHSEER if setting == "pathseer" else VectorFilterStrategy.ACORN
        self.collection.config.update(vector_index_config=Reconfigure.VectorIndex.hnsw(filter_strategy=strategy))
        deadline = time.monotonic() + 60
        while self.collection.config.get().vector_index_config.filter_strategy != strategy:
            if time.monotonic() > deadline:
                raise RuntimeError(f"Weaviate did not switch to {strategy}")
            time.sleep(0.5)
        self.setting = setting

    def search(
        self,
        q: np.ndarray,
        k: int,
        *,
        principals: list[str] | None = None,
        ids: list[int] | None = None,
        setting: str = "default",
    ) -> list[tuple[int, float]]:
        from weaviate.classes.query import Filter, MetadataQuery

        self.configure(setting)
        where = None
        if principals is not None:
            where = Filter.by_property("principals").contains_any(principals)
        elif ids is not None:
            where = Filter.by_id().contains_any([_uuid(i) for i in ids])
        result = self.collection.query.near_vector(
            near_vector=np.asarray(q, dtype=np.float32).tolist(), limit=k, filters=where,
            return_metadata=MetadataQuery(distance=True), return_properties=["cid"],
        )
        return [(int(o.properties["cid"]), -float(o.metadata.distance)) for o in result.objects]

    def set_principals(self, i: int, principals: list[str], vector: np.ndarray) -> None:
        self.collection.data.update(uuid=_uuid(i), properties={"principals": principals})

    def strategy(self) -> str:
        return str(self.collection.config.get().vector_index_config.filter_strategy)

    def close(self) -> None:
        if self.client is not None:
            self.client.close()
