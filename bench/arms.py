"""The arms: ways of answering "the k best chunks this user may read", each as an async callable.

`build(name, ctx)` returns `run(user, groups, query_key) -> [(chunk id, score), ...]`. Query keys
are `q<index>`; the vector for a key comes from the workload, so embedding is never timed.

Third-party integrations run as their packages ship them. Their LangChain plumbing sits on two
thin adapters over the store: `StoreRetriever` (a plain top-k search, the base retriever a
post-filter wraps) and `IdFilteredStore` (a vector store whose `asimilarity_search` takes the
`ids_in` keyword our `filter_factory` passes, for the pre-filter).

| arm | what runs |
|---|---|
| a0 | exact search with the user's principals as a filter (pgvector, index scans off): the control |
| a1-fga | auth0-ai-langchain `FGARetriever` over a k-hit base retriever, OpenFGA batch check |
| a1-spicedb | langchain-spicedb `SpiceDBAuthFilter` over a k-hit base retriever |
| a2-fga-x3, a2-fga-x10, a2-spicedb-x3, a2-spicedb-x10 | the same over 3k and 10k hits, first k kept |
| a3-spicedb@S | langchain-spicedb `SpiceDBPreFilterRetriever`: LookupResources, then an id filter |
| a4@S | the store's own filter on the user's principals |
| a5-rls@S | PostgreSQL row-level security (pgvector only) |
| a5-dls | OpenSearch document-level security: an unfiltered search sent as the user (OpenSearch only) |
| a6-partition | one pgvector table and index per role (W2) or per user (W1); hits from the user's tables merged |
| a7-wardowl | wardowl's `PermissionedRetriever` with its SpiceDB authorizer (pgvector and Qdrant; the author's own) |

`@S` is the store setting the filtered search runs under (see `bench/stores`).
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any

import numpy as np
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.vectorstores import VectorStore
from pydantic import ConfigDict

from .engines import OPENFGA_URL, SPICEDB_GRPC, SPICEDB_TOKEN
from .workload import Workload, principals

K = 10
Hits = list[tuple[int, float]]
Run = Callable[[str, list[str], str], Awaitable[Hits]]


@dataclass
class Context:
    workload: Workload
    store: Any
    fga: dict = field(default_factory=dict)  # store_id, model_id from engines.load_openfga

    def vector(self, key: str) -> np.ndarray:
        """`q<i>`: question i; `v<i>`: chunk i's own vector (the probes of bench.churn)."""
        if key[0] == "v":
            return np.asarray(self.workload.vectors[int(key[1:])], dtype=np.float32)
        return self.workload.queries[int(key[1:])]


def _docs(hits: Hits) -> list[Document]:
    return [Document(id=str(i), page_content="", metadata={"resource_id": f"c{i}", "score": s}) for i, s in hits]


def _hits(docs: list[Document]) -> Hits:
    return [(int(d.metadata["resource_id"][1:]), float(d.metadata["score"])) for d in docs]


class StoreRetriever(BaseRetriever):
    """Unfiltered top-k from the store, as LangChain documents."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    ctx: Any
    k: int

    def _get_relevant_documents(self, query: str, *, run_manager: Any = None) -> list[Document]:
        return _docs(self.ctx.store.search(self.ctx.vector(query), self.k))

    async def _aget_relevant_documents(self, query: str, *, run_manager: Any = None) -> list[Document]:
        return self._get_relevant_documents(query)


class IdFilteredStore(VectorStore):
    """A LangChain vector store over our store whose search takes `ids_in=["c1", ...]`."""

    def __init__(self, ctx: Context, setting: str) -> None:
        self.ctx, self.setting = ctx, setting

    def add_texts(self, texts: Any, metadatas: Any = None, **kwargs: Any) -> list[str]:
        raise NotImplementedError

    @classmethod
    def from_texts(cls, texts: Any, embedding: Any, metadatas: Any = None, **kwargs: Any) -> IdFilteredStore:
        raise NotImplementedError

    def similarity_search(self, query: str, k: int = 4, **kwargs: Any) -> list[Document]:
        ids = [int(x[1:]) for x in kwargs["ids_in"]]
        return _docs(self.ctx.store.search(self.ctx.vector(query), k, ids=ids, setting=self.setting))

    async def asimilarity_search(self, query: str, k: int = 4, **kwargs: Any) -> list[Document]:
        return self.similarity_search(query, k, **kwargs)


# ---- arms -----------------------------------------------------------------------------------------


def _exact(ctx: Context) -> Run:
    async def run(user: str, groups: list[str], key: str) -> Hits:
        return ctx.store.search(ctx.vector(key), K, principals=principals(user, groups), setting="exact")

    return run


def _store_filter(ctx: Context, setting: str) -> Run:
    async def run(user: str, groups: list[str], key: str) -> Hits:
        return ctx.store.search(ctx.vector(key), K, principals=principals(user, groups), setting=setting)

    return run


def _rls(ctx: Context, setting: str) -> Run:
    async def run(user: str, groups: list[str], key: str) -> Hits:
        return ctx.store.search_rls(ctx.vector(key), K, principals(user, groups), setting=setting)

    return run


def _partitions(ctx: Context) -> Run:
    async def run(user: str, groups: list[str], key: str) -> Hits:
        return ctx.store.search_partitions(ctx.vector(key), K, principals(user, groups))

    return run


def _dls(ctx: Context) -> Run:
    async def run(user: str, groups: list[str], key: str) -> Hits:
        return ctx.store.search_dls(ctx.vector(key), K, user)

    return run


def _fga_post(ctx: Context, multiple: int) -> Run:
    from auth0_ai_langchain import FGARetriever
    from openfga_sdk import ClientConfiguration
    from openfga_sdk.client.models import ClientBatchCheckItem

    config = ClientConfiguration(
        api_url=OPENFGA_URL, store_id=ctx.fga["store_id"], authorization_model_id=ctx.fga["model_id"]
    )
    base = StoreRetriever(ctx=ctx, k=K * multiple)
    retrievers: dict[str, Any] = {}

    def retriever(user: str) -> Any:
        if user not in retrievers:
            retrievers[user] = FGARetriever(
                retriever=base,
                build_query=lambda doc: ClientBatchCheckItem(
                    user=f"user:{user}", relation="viewer", object=f"chunk:{doc.metadata['resource_id']}"
                ),
                fga_configuration=config,
            )
        return retrievers[user]

    async def run(user: str, groups: list[str], key: str) -> Hits:
        # `invoke`, as Auth0's README does; `ainvoke` is probed separately (see run.py).
        return _hits(retriever(user).invoke(key))[:K]

    return run


def _spicedb_post(ctx: Context, multiple: int) -> Run:
    from langchain_spicedb import SpiceDBAuthFilter

    auth = SpiceDBAuthFilter(
        spicedb_endpoint=SPICEDB_GRPC,
        spicedb_token=SPICEDB_TOKEN,
        resource_type="chunk",
        subject_type="user",
        permission="view",
        resource_id_key="resource_id",
    )
    base = StoreRetriever(ctx=ctx, k=K * multiple)

    async def run(user: str, groups: list[str], key: str) -> Hits:
        docs = await base.ainvoke(key)
        docs = await auth.ainvoke(docs, config={"configurable": {"subject_id": user}})
        return _hits(docs)[:K]

    return run


def _spicedb_pre(ctx: Context, setting: str) -> Run:
    from langchain_spicedb import SpiceDBPreFilterRetriever

    store = IdFilteredStore(ctx, setting)
    retrievers: dict[str, Any] = {}

    def retriever(user: str) -> Any:
        if user not in retrievers:
            retrievers[user] = SpiceDBPreFilterRetriever(
                vector_store=store,
                filter_factory=lambda ids: {"ids_in": ids},
                subject_id=user,
                spicedb_endpoint=SPICEDB_GRPC,
                spicedb_token=SPICEDB_TOKEN,
                resource_type="chunk",
                subject_type="user",
                permission="view",
                k=K,
            )
        return retrievers[user]

    async def run(user: str, groups: list[str], key: str) -> Hits:
        return _hits(await retriever(user).ainvoke(key))

    return run


def _wardowl(ctx: Context) -> Run:
    from wardowl import PermissionedRetriever, Query, Subject
    from wardowl.authorizers.spicedb import SpiceDBAuthorizer

    from .engines import SPICEDB_HTTP

    authorizer = SpiceDBAuthorizer(SPICEDB_HTTP, SPICEDB_TOKEN, permissions={"read": "view"}, resource_type="chunk",
                                   subject_type="user", resource_field="doc_id")
    retriever = PermissionedRetriever(ctx.store.wardowl_backend(), authorizer)

    async def run(user: str, groups: list[str], key: str) -> Hits:
        result = retriever.retrieve(Query(vector=ctx.vector(key).tolist()), Subject(user), k=K)
        return [(int(h.id[1:]), float(h.score)) for h in result.hits]

    return run


def names(store: Any) -> list[str]:
    """Every arm that can run on this store, in a fixed order (the run shuffles them)."""
    arms = ["a1-fga", "a1-spicedb"] + [f"a2-{e}-x{m}" for e in ("fga", "spicedb") for m in (3, 10)]
    arms += [f"a3-spicedb@{s}" for s in store.settings] + [f"a4@{s}" for s in store.settings]
    if store.name == "pgvector":
        arms = ["a0"] + arms + [f"a5-rls@{s}" for s in store.settings]
    if store.name == "opensearch":
        arms += ["a5-dls"]
    if getattr(store, "partitions", None):
        arms += ["a6-partition"]
    if hasattr(store, "wardowl_backend"):
        arms += ["a7-wardowl"]
    return arms


def build(name: str, ctx: Context) -> Run:
    arm, _, setting = name.partition("@")
    if arm == "a0":
        return _exact(ctx)
    if arm == "a4":
        return _store_filter(ctx, setting)
    if arm == "a5-rls":
        return _rls(ctx, setting)
    if arm == "a5-dls":
        return _dls(ctx)
    if arm == "a7-wardowl":
        return _wardowl(ctx)
    if arm == "a6-partition":
        return _partitions(ctx)
    if arm == "a3-spicedb":
        return _spicedb_pre(ctx, setting)
    if arm in ("a1-fga", "a1-spicedb") or arm.startswith("a2-"):
        engine = "fga" if "fga" in arm else "spicedb"
        multiple = int(arm.rsplit("-x", 1)[1]) if arm.startswith("a2-") else 1
        return _fga_post(ctx, multiple) if engine == "fga" else _spicedb_post(ctx, multiple)
    raise ValueError(f"unknown arm {name!r}")
