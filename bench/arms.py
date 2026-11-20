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

The follow-up runs (`prereg/addendum-1.md`) name two more things in an arm's name, never used by the
registered runs: `:ef<N>`, the store's search breadth for that arm (the run sets it with `set_ef`),
and `+lookup-spicedb` or `+lookup-openfga`, which first asks that engine for the user's groups and
then runs the arm with them instead of the harness's list (`parse`, `plan_names`). For the change
diagnostic, `Context.consistency` makes the SpiceDB arms ask for fresher reads (`Freshness`).
"""

from __future__ import annotations

import re
import time
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
    consistency: Freshness | None = None  # None: what each integration sends (bench.churn's diagnostic sets it)

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


# ---- fresher SpiceDB reads (the change diagnostic of bench.churn) ----------------------------------


class Freshness:
    """A SpiceDB read consistency beyond what the integrations send. langchain-spicedb sends none, which
    SpiceDB serves as `minimize_latency`; wardowl sends `minimizeLatency`. `at_least_as_fresh` uses
    `token`, the ZedToken of the latest change, which bench.churn sets after every SpiceDB write;
    before the first change it asks for nothing more than the default."""

    MODES = ("at_least_as_fresh", "fully_consistent")

    def __init__(self, mode: str) -> None:
        if mode not in self.MODES:
            raise ValueError(f"unknown consistency {mode!r}")
        self.mode = mode
        self.token: str | None = None

    def grpc(self):  # noqa: ANN201 - an authzed Consistency message, or None
        from authzed.api.v1 import Consistency, ZedToken

        if self.mode == "fully_consistent":
            return Consistency(fully_consistent=True)
        return Consistency(at_least_as_fresh=ZedToken(token=self.token)) if self.token else None

    def http(self) -> dict:
        if self.mode == "fully_consistent":
            return {"fullyConsistent": True}
        return {"atLeastAsFresh": {"token": self.token}} if self.token else {"minimizeLatency": True}


READS = ("CheckPermission", "CheckBulkPermissions", "LookupResources")


class ConsistentClient:
    """An authzed client whose read requests carry a `Freshness`; every other call passes through."""

    def __init__(self, client: Any, freshness: Freshness) -> None:
        self._client, self._freshness = client, freshness

    def __getattr__(self, name: str) -> Any:
        attr = getattr(self._client, name)
        if name not in READS:
            return attr

        def call(request: Any, *args: Any, **kwargs: Any) -> Any:
            consistency = self._freshness.grpc()
            if consistency is not None:
                request.consistency.CopyFrom(consistency)
            return attr(request, *args, **kwargs)

        return call


def fresher(authorizer: Any, freshness: Freshness) -> None:
    """Make a langchain-spicedb `SpiceDBAuthorizer` send `freshness` on every read. The package has no
    option for it; only the requests it builds gain the field."""
    base = type(authorizer)

    class Fresh(base):  # type: ignore[valid-type, misc]
        @property
        def client(self) -> Any:
            return ConsistentClient(base.client.fget(self), freshness)

    authorizer.__class__ = Fresh


# ---- arm names of the follow-up runs ------------------------------------------------------------

_NAME = re.compile(r"(?P<base>[^:+]+)(?::ef(?P<ef>[0-9]+))?(?:\+lookup-(?P<lookup>spicedb|openfga))?")
ENGINES = ("spicedb", "openfga")
SWEEP_EF = (40, 100, 400)
POST_FILTERS = ("a1-fga", "a1-spicedb", "a2-fga-x3", "a2-fga-x10", "a2-spicedb-x3", "a2-spicedb-x10")


def parse(name: str) -> tuple[str, int | None, str | None]:
    """`a4@default:ef40+lookup-spicedb` -> ("a4@default", 40, "spicedb"); plain names -> (name, None, None)."""
    m = _NAME.fullmatch(name)
    if m is None:
        raise ValueError(f"unknown arm {name!r}")
    return m["base"], int(m["ef"]) if m["ef"] else None, m["lookup"]


def plan_names(store: Any, plan: str) -> list[str]:
    """The arms of one follow-up job (prereg/addendum-1.md, section 4)."""
    lookups = ("",) + tuple(f"+lookup-{e}" for e in ENGINES)
    if plan == "sweep":
        settings = list(store.settings) + list(getattr(store, "extra_settings", ()))[:1]  # pgvector: iterative-100k
        out = []
        for ef in SWEEP_EF:
            out += [f"a4@{s}:ef{ef}" for s in settings] + [f"{a}:ef{ef}" for a in POST_FILTERS]
            if store.name == "opensearch":
                out.append(f"a5-dls:ef{ef}")
        out += [f"a4@{s}:ef100+lookup-{e}" for s in store.settings for e in ENGINES]
        if store.name == "pgvector":
            out = ["a0"] + out + [f"a5-rls@{s}:ef100{x}" for s in store.settings for x in lookups]
        return out
    if plan == "wide":
        if store.name != "pgvector":
            raise ValueError("the wide-scan plan runs on pgvector only")
        return ["a4@iterative-1m:ef100"]
    if plan == "lookup":
        bases = [f"a4@{s}" for s in store.settings]
        if store.name == "pgvector":
            bases += [f"a5-rls@{s}" for s in store.settings]
        if getattr(store, "partitions", None):
            bases.append("a6-partition")
        return [b + x for b in bases for x in lookups]
    raise ValueError(f"unknown plan {plan!r}")


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

    run.prepare = lambda users: [retriever(u) for u in users]  # built before timing starts
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
    if ctx.consistency is not None:
        fresher(auth.authorizer, ctx.consistency)
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
            if ctx.consistency is not None:
                fresher(retrievers[user]._authorizer, ctx.consistency)
        return retrievers[user]

    async def run(user: str, groups: list[str], key: str) -> Hits:
        return _hits(await retriever(user).ainvoke(key))

    run.prepare = lambda users: [retriever(u) for u in users]  # built before timing starts
    return run


def _wardowl(ctx: Context) -> Run:
    from wardowl import PermissionedRetriever, Query, Subject
    from wardowl.authorizers.spicedb import SpiceDBAuthorizer

    from .engines import SPICEDB_HTTP

    authorizer = SpiceDBAuthorizer(SPICEDB_HTTP, SPICEDB_TOKEN, permissions={"read": "view"}, resource_type="chunk",
                                   subject_type="user", resource_field="doc_id")
    retriever = PermissionedRetriever(ctx.store.wardowl_backend(), authorizer)

    async def run(user: str, groups: list[str], key: str) -> Hits:
        if ctx.consistency is not None:
            authorizer.consistency = ctx.consistency.http()
        result = retriever.retrieve(Query(vector=ctx.vector(key).tolist()), Subject(user), k=K)
        return [(int(h.id[1:]), float(h.score)) for h in result.hits]

    return run


def _spicedb_groups(ctx: Context) -> Callable[[str], Awaitable[list[str]]]:
    """The user's groups from SpiceDB: LookupResources over gRPC with no consistency field, as the
    langchain-spicedb arms send it."""
    from authzed.api.v1 import AsyncClient, LookupResourcesRequest, ObjectReference, SubjectReference
    from grpcutil import insecure_bearer_token_credentials

    clients: list[Any] = []  # created inside the running event loop, which the aio channel is bound to

    async def lookup(user: str) -> list[str]:
        if not clients:
            clients.append(AsyncClient(SPICEDB_GRPC, insecure_bearer_token_credentials(SPICEDB_TOKEN)))
        request = LookupResourcesRequest(
            resource_object_type="group", permission="member",
            subject=SubjectReference(object=ObjectReference(object_type="user", object_id=user)),
        )
        return [r.resource_object_id async for r in clients[0].LookupResources(request)]

    return lookup


def _openfga_groups(ctx: Context) -> Callable[[str], Awaitable[list[str]]]:
    """The user's groups from OpenFGA: ListObjects through one reused openfga-sdk client, with no
    consistency, as the FGA arms send it."""
    from openfga_sdk import ClientConfiguration
    from openfga_sdk.client.models import ClientListObjectsRequest
    from openfga_sdk.sync import OpenFgaClient

    client = OpenFgaClient(ClientConfiguration(
        api_url=OPENFGA_URL, store_id=ctx.fga["store_id"], authorization_model_id=ctx.fga["model_id"]))

    async def lookup(user: str) -> list[str]:
        response = client.list_objects(ClientListObjectsRequest(user=f"user:{user}", relation="member", type="group"))
        return [o.split(":", 1)[1] for o in response.objects]

    return lookup


def _with_lookup(ctx: Context, base: str, engine: str) -> Run:
    """The arm `base`, given the groups the engine returns for the user instead of the harness's list.
    Each call leaves `run.extra`: the lookup's and the search's time (their sum is the arm's latency),
    how many groups came back and whether they equal the harness's list."""
    lookup = _spicedb_groups(ctx) if engine == "spicedb" else _openfga_groups(ctx)
    inner = build(base, ctx)

    async def run(user: str, groups: list[str], key: str) -> Hits:
        run.extra = {}
        t0 = time.perf_counter_ns()
        found = sorted(await lookup(user))
        t1 = time.perf_counter_ns()
        run.extra.update(lookup_ms=(t1 - t0) / 1e6, groups_found=len(found), principals_match=found == sorted(groups))
        hits = await inner(user, found, key)
        run.extra["search_ms"] = (time.perf_counter_ns() - t1) / 1e6
        return hits

    if hasattr(inner, "prepare"):
        run.prepare = inner.prepare
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
    name, _, lookup = parse(name)  # the search breadth is the run's to set (bench.run)
    if lookup is not None:
        return _with_lookup(ctx, name, lookup)
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
