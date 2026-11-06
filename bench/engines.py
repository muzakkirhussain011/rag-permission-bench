"""Loading SpiceDB and OpenFGA with the same permissions, from a workload's ACL and layouts.

Both get the schema in `config/`, every chunk's readers (`chunk:c<i>#reader@user:<u>` and
`chunk:c<i>#reader@group:<g>#member`) and every layout's memberships (`group:<g>#member@user:<u>`).
Loading runs before any measured query and is timed separately.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from .util import log, retry
from .workload import Workload

CONFIG = Path(__file__).resolve().parent.parent / "config"
# Arms reach the engines here; fault runs point these at a fault-injecting proxy instead (bench.faults).
SPICEDB_GRPC = os.environ.get("BENCH_SPICEDB_GRPC", "localhost:50051")
SPICEDB_HTTP = os.environ.get("BENCH_SPICEDB_HTTP", "http://localhost:8443")
OPENFGA_URL = os.environ.get("BENCH_OPENFGA_URL", "http://localhost:8080")
SPICEDB_TOKEN = "bench"
# Loading and permission changes always go straight to the engines.
SPICEDB_ADMIN = "localhost:50051"
OPENFGA_ADMIN = "http://localhost:8080"
BATCH = 1000


@dataclass(frozen=True)
class Tuple:
    resource_type: str
    resource_id: str
    relation: str
    subject_type: str
    subject_id: str
    subject_relation: str = ""


def tuples(w: Workload) -> Iterator[Tuple]:
    """Every relationship of the workload, each once."""
    for i in range(w.n):
        for u in w.user_idx[w.user_ptr[i] : w.user_ptr[i + 1]]:
            yield Tuple("chunk", f"c{i}", "reader", "user", w.user_names[u])
        for g in w.group_idx[w.group_ptr[i] : w.group_ptr[i + 1]]:
            yield Tuple("chunk", f"c{i}", "reader", "group", w.group_names[g], "member")
    seen: set[tuple[str, str]] = set()
    for layout in w.layouts:
        for user, groups in layout.user_groups.items():
            for g in groups:
                if (g, user) not in seen:
                    seen.add((g, user))
                    yield Tuple("group", g, "member", "user", user)


def batches(items: Iterator[Tuple], size: int = BATCH) -> Iterator[list[Tuple]]:
    batch: list[Tuple] = []
    for item in items:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch


# ---- SpiceDB ------------------------------------------------------------------------------------


def spicedb_client():  # noqa: ANN201 - authzed's Client has no public type to import
    from authzed.api.v1 import Client
    from grpcutil import insecure_bearer_token_credentials

    return Client(SPICEDB_ADMIN, insecure_bearer_token_credentials(SPICEDB_TOKEN))


def _relationship(t: Tuple):  # noqa: ANN202
    from authzed.api.v1 import ObjectReference, Relationship, SubjectReference

    return Relationship(
        resource=ObjectReference(object_type=t.resource_type, object_id=t.resource_id),
        relation=t.relation,
        subject=SubjectReference(
            object=ObjectReference(object_type=t.subject_type, object_id=t.subject_id),
            optional_relation=t.subject_relation,
        ),
    )


def load_spicedb(w: Workload) -> dict:
    import authzed.api.v1 as v1

    client = spicedb_client()
    schema = (CONFIG / "spicedb.zed").read_text(encoding="utf-8")
    retry(lambda: client.WriteSchema(v1.WriteSchemaRequest(schema=schema)), "SpiceDB")
    # authzed 1.25 names the bulk import BulkImportRelationships; newer clients ImportBulkRelationships.
    request = getattr(v1, "ImportBulkRelationshipsRequest", None) or v1.BulkImportRelationshipsRequest
    method = getattr(client, "ImportBulkRelationships", None) or client.BulkImportRelationships
    started = time.perf_counter()
    response = method(request(relationships=[_relationship(t) for t in b]) for b in batches(tuples(w)))
    seconds = time.perf_counter() - started
    log(f"SpiceDB: {response.num_loaded} relationships in {seconds:.0f} s")
    return {"relationships": int(response.num_loaded), "load_s": seconds}


# ---- OpenFGA ------------------------------------------------------------------------------------


def _fga(method: str, path: str, body: dict | None = None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(
        OPENFGA_ADMIN + path, data=data, method=method, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.loads(response.read() or b"{}")
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"OpenFGA {method} {path}: {error.code} {error.read()[:500]!r}") from error


def _fga_key(t: Tuple) -> dict:
    subject = f"{t.subject_type}:{t.subject_id}" + (f"#{t.subject_relation}" if t.subject_relation else "")
    return {"user": subject, "relation": t.relation, "object": f"{t.resource_type}:{t.resource_id}"}


def load_openfga(w: Workload) -> dict:
    retry(lambda: _fga("GET", "/healthz"), "OpenFGA")
    store_id = _fga("POST", "/stores", {"name": "bench"})["id"]
    model = json.loads((CONFIG / "openfga-model.json").read_text(encoding="utf-8"))
    model_id = _fga("POST", f"/stores/{store_id}/authorization-models", model)["authorization_model_id"]
    started = time.perf_counter()

    def write(batch: list[Tuple]) -> int:
        body = {"writes": {"tuple_keys": [_fga_key(t) for t in batch]}, "authorization_model_id": model_id}
        _fga("POST", f"/stores/{store_id}/write", body)
        return len(batch)

    with ThreadPoolExecutor(max_workers=8) as pool:
        total = sum(pool.map(write, batches(tuples(w))))
    seconds = time.perf_counter() - started
    log(f"OpenFGA: {total} tuples in {seconds:.0f} s")
    return {"store_id": store_id, "model_id": model_id, "tuples": total, "load_s": seconds}


# ---- permission changes (bench.churn) ------------------------------------------------------------


def spicedb_change(client, touch: list[Tuple], delete: list[Tuple]) -> None:  # noqa: ANN001
    """One WriteRelationships call; returns when SpiceDB has acknowledged it."""
    from authzed.api.v1 import RelationshipUpdate, WriteRelationshipsRequest

    updates = [RelationshipUpdate(operation=RelationshipUpdate.Operation.OPERATION_TOUCH, relationship=_relationship(t))
               for t in touch]
    updates += [RelationshipUpdate(operation=RelationshipUpdate.Operation.OPERATION_DELETE,
                                   relationship=_relationship(t)) for t in delete]
    if updates:
        client.WriteRelationships(WriteRelationshipsRequest(updates=updates))


def openfga_change(fga: dict, write: list[Tuple], delete: list[Tuple]) -> None:
    """One Write call; returns when OpenFGA has acknowledged it. Deletes must name existing tuples."""
    body: dict = {"authorization_model_id": fga["model_id"]}
    if write:
        body["writes"] = {"tuple_keys": [_fga_key(t) for t in write]}
    if delete:
        body["deletes"] = {"tuple_keys": [_fga_key(t) for t in delete]}
    if write or delete:
        _fga("POST", f"/stores/{fga['store_id']}/write", body)
