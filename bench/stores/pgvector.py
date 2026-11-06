"""pgvector: one table, an HNSW index on inner product, a GIN index on the principals.

Settings: `default` leaves `hnsw.iterative_scan` off (pgvector's default: the filter applies after
the index scan); `iterative` sets it to `relaxed_order`, which the pgvector README suggests for
filtering; `exact` turns index scans off, which makes every answer exact (the control arm A0).

Row-level security (arm A5) uses a second role, `bench_reader`, that is not the table's owner. Its
policy compares the row's principals with the session setting `bench.principals`, which the
application sets for each request.
"""

from __future__ import annotations

import time

import numpy as np

from ..util import log, retry
from ..workload import Workload, principals
from . import EF_CONSTRUCTION, EF_SEARCH, M

DSN = "postgresql://postgres:bench@localhost:5432/bench"
READER_DSN = "postgresql://bench_reader:reader@localhost:5432/bench"
SETTINGS = {
    "default": ["SET hnsw.iterative_scan = off", "SET enable_indexscan = on"],
    "iterative": ["SET hnsw.iterative_scan = relaxed_order", "SET enable_indexscan = on"],
    "exact": ["SET hnsw.iterative_scan = off", "SET enable_indexscan = off"],
}
SEARCH = (
    "SELECT id, -(embedding <#> %(q)s) FROM chunks {where} ORDER BY embedding <#> %(q)s LIMIT %(k)s"
)


def _connect(dsn: str):  # noqa: ANN202
    import psycopg
    from pgvector.psycopg import register_vector

    conn = psycopg.connect(dsn, autocommit=True)
    register_vector(conn)
    conn.execute(f"SET hnsw.ef_search = {EF_SEARCH}")
    return conn


class PgVector:
    name = "pgvector"
    settings = ("default", "iterative")

    def __init__(self) -> None:
        self.conn = None
        self.reader = None
        self.setting = None
        self.partitions: dict[str, str] = {}

    def load(self, w: Workload) -> dict:
        import psycopg
        from pgvector.psycopg import register_vector

        conn = retry(lambda: psycopg.connect(DSN, autocommit=True), "PostgreSQL")
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        register_vector(conn)
        conn.execute("DROP TABLE IF EXISTS chunks")
        conn.execute(
            f"CREATE TABLE chunks (id integer PRIMARY KEY, principals text[] NOT NULL,"
            f" embedding vector({w.vectors.shape[1]}) NOT NULL)"
        )
        vector_oid = psycopg.types.TypeInfo.fetch(conn, "vector").oid
        started = time.perf_counter()
        with conn.cursor() as cur, cur.copy("COPY chunks (id, principals, embedding) FROM STDIN WITH (FORMAT BINARY)") as copy:
            copy.set_types([23, 1009, vector_oid])  # int4, text[], vector
            for i in range(w.n):
                copy.write_row((i, w.chunk_principals(i), np.asarray(w.vectors[i], dtype=np.float32)))
        loaded = time.perf_counter()
        conn.execute("SET maintenance_work_mem = '2GB'")
        conn.execute("SET max_parallel_maintenance_workers = 3")
        conn.execute(
            f"CREATE INDEX chunks_hnsw ON chunks USING hnsw (embedding vector_ip_ops)"
            f" WITH (m = {M}, ef_construction = {EF_CONSTRUCTION})"
        )
        indexed = time.perf_counter()
        conn.execute("CREATE INDEX chunks_principals ON chunks USING gin (principals)")
        # wardowl's pgvector backend (arm A7) expects (id, content, metadata, embedding) and orders by cosine
        # distance. A view gives it that layout over the same rows; a cosine HNSW index serves its order
        # (on unit vectors, cosine and inner product rank alike). Other arms never touch either.
        conn.execute(
            "CREATE OR REPLACE VIEW wardowl_chunks AS SELECT 'c' || id AS id, ''::text AS content,"
            " jsonb_build_object('doc_id', 'c' || id) AS metadata, embedding FROM chunks"
        )
        conn.execute(
            f"CREATE INDEX chunks_hnsw_cosine ON chunks USING hnsw (embedding vector_cosine_ops)"
            f" WITH (m = {M}, ef_construction = {EF_CONSTRUCTION})"
        )
        conn.execute("ANALYZE chunks")
        conn.execute(
            "DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'bench_reader') THEN"
            " CREATE ROLE bench_reader LOGIN PASSWORD 'reader' NOBYPASSRLS; END IF; END $$"
        )
        conn.execute("GRANT SELECT ON chunks TO bench_reader")
        conn.execute("ALTER TABLE chunks ENABLE ROW LEVEL SECURITY")
        conn.execute("DROP POLICY IF EXISTS readable ON chunks")
        conn.execute(
            "CREATE POLICY readable ON chunks FOR SELECT TO bench_reader"
            " USING (principals && string_to_array(current_setting('bench.principals', true), ','))"
        )
        sizes = conn.execute(
            "SELECT pg_table_size('chunks'), pg_relation_size('chunks_hnsw'), pg_relation_size('chunks_principals')"
        ).fetchone()
        conn.close()
        log(f"pgvector: {w.n} rows in {loaded - started:.0f} s, HNSW in {indexed - loaded:.0f} s")
        return {
            "load_s": loaded - started,
            "index_s": indexed - loaded,
            "table_bytes": sizes[0],
            "hnsw_bytes": sizes[1],
            "gin_bytes": sizes[2],
        }

    def open(self) -> None:
        self.conn = _connect(DSN)
        self.reader = _connect(READER_DSN)

    def configure(self, setting: str) -> None:
        if setting != self.setting:
            for conn in (self.conn, self.reader):
                for statement in SETTINGS[setting]:
                    conn.execute(statement)
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
        self.configure(setting)
        where, params = "", {"q": q, "k": k}
        if principals is not None:
            where, params["p"] = "WHERE principals && %(p)s", principals
        elif ids is not None:
            where, params["ids"] = "WHERE id = ANY(%(ids)s::integer[])", ids
        rows = self.conn.execute(SEARCH.format(where=where), params).fetchall()
        return [(int(i), float(s)) for i, s in rows]

    def search_rls(self, q: np.ndarray, k: int, principals: list[str], setting: str = "default") -> list[tuple[int, float]]:
        """The same search as the reader role, with the policy doing the filtering."""
        self.configure(setting)
        self.reader.execute("SELECT set_config('bench.principals', %s, false)", [",".join(principals)])
        rows = self.reader.execute(SEARCH.format(where=""), {"q": q, "k": k}).fetchall()
        return [(int(i), float(s)) for i, s in rows]

    def explain(self, q: np.ndarray, k: int, *, principals: list[str] | None = None, setting: str = "default", rls: bool = False) -> dict:
        """The executed plan with row counts and buffers, recorded beside the results."""
        self.configure(setting)
        conn = self.reader if rls else self.conn
        if rls:
            conn.execute("SELECT set_config('bench.principals', %s, false)", [",".join(principals or [])])
        where, params = "", {"q": q, "k": k}
        if principals is not None and not rls:
            where, params["p"] = "WHERE principals && %(p)s", principals
        plan = conn.execute("EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) " + SEARCH.format(where=where), params).fetchone()
        return plan[0][0]

    def load_partitions(self, w: Workload) -> dict:
        """Arm A6: one table and HNSW index per principal held by a measured user (a role in W2, a
        user's own mail in W1). A user's search runs on each of their partitions and merges the hits."""
        held = sorted({p for layout in w.layouts for u in {*layout.user_groups, *(x for x, _ in layout.queries)}
                       for p in principals(u, layout.user_groups.get(u, []))})
        started = time.perf_counter()
        rows = 0
        self.partitions = {}
        with _connect(DSN) as conn:
            conn.execute("SET maintenance_work_mem = '2GB'")
            for n, p in enumerate(held):
                table = f"part_{n}"
                conn.execute(f"DROP TABLE IF EXISTS {table}")
                conn.execute(f"CREATE TABLE {table} AS SELECT id, embedding FROM chunks WHERE principals @> ARRAY[%s]::text[]",
                             [p])
                count = conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
                if count == 0:
                    conn.execute(f"DROP TABLE {table}")
                    continue
                conn.execute(f"CREATE INDEX ON {table} USING hnsw (embedding vector_ip_ops)"
                             f" WITH (m = {M}, ef_construction = {EF_CONSTRUCTION})")
                self.partitions[p] = table
                rows += count
            size = sum(conn.execute("SELECT pg_total_relation_size(%s)", [t]).fetchone()[0]
                       for t in self.partitions.values())
        log(f"pgvector: {len(self.partitions)} partitions, {rows} rows, in {time.perf_counter() - started:.0f} s")
        return {"partitions": len(self.partitions), "rows": rows, "bytes": size, "copies": rows / w.n,
                "build_s": time.perf_counter() - started}

    def search_partitions(self, q: np.ndarray, k: int, principals_: list[str]) -> list[tuple[int, float]]:
        self.configure("default")  # the partitions hold only readable rows: no filter, plain index scans
        best: dict[int, float] = {}
        for p in principals_:
            table = self.partitions.get(p)
            if table is None:
                continue
            for i, s in self.conn.execute(SEARCH.format(where="").replace("chunks", table), {"q": q, "k": k}).fetchall():
                best[int(i)] = max(best.get(int(i), -1e9), float(s))
        return sorted(best.items(), key=lambda x: (-x[1], x[0]))[:k]

    def set_principals(self, i: int, principals_: list[str], vector: np.ndarray) -> None:
        """Permission change for one chunk, as a sync job would apply it (partitions included)."""
        self.conn.execute("UPDATE chunks SET principals = %s WHERE id = %s", [principals_, i])
        for p, table in self.partitions.items():
            if p in principals_:
                self.conn.execute(f"INSERT INTO {table} SELECT id, embedding FROM chunks WHERE id = %(i)s"
                                  f" AND NOT EXISTS (SELECT 1 FROM {table} WHERE id = %(i)s)", {"i": i})
            else:
                self.conn.execute(f"DELETE FROM {table} WHERE id = %s", [i])

    def wardowl_backend(self):  # noqa: ANN201
        from psycopg_pool import ConnectionPool
        from wardowl.backends.pgvector import PgVectorBackend

        pool = ConnectionPool(DSN, min_size=1, max_size=2, kwargs={"autocommit": True}, open=True)
        return PgVectorBackend(pool, table="wardowl_chunks", iterative_scan="relaxed_order", ef_search=EF_SEARCH)

    def close(self) -> None:
        for conn in (self.conn, self.reader):
            if conn is not None:
                conn.close()
