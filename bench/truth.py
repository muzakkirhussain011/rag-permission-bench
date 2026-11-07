"""The exact answer for every measured (layout, user, query): the k best chunks the user may read.

Brute force over the user's readable chunks, inner product on unit vectors (cosine), ties broken by
chunk id. For each pair it also records Amanbayev et al.'s selectivities: sigma_g, the share of
the corpus the user may read, and sigma_l, the share of the query's `nn` nearest chunks (ignoring
permissions) the user may read, with rho = (r - 1) / (r + 1) for r = sigma_l / sigma_g.

    python -m bench.truth --workload data/w3 [--k 10] [--nn 2048]

writes `truth.jsonl.gz` into the workload directory.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

import numpy as np

from .util import log, write_jsonl_gz
from .workload import Workload

DENSE_LIMIT = 2_500_000_000  # bytes: below this, all chunk-query scores are computed at once


def top_k(scores: np.ndarray, ids: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
    """The k best (score descending, id ascending) of parallel arrays."""
    if len(scores) > 4 * k:
        # Keep every score tied with the k-th best, so the id tie-break below sees all of them.
        kth = -np.partition(-scores, k - 1)[k - 1]
        keep = scores >= kth
        scores, ids = scores[keep], ids[keep]
    order = np.lexsort((ids, -scores))[:k]
    return ids[order], scores[order]


def unfiltered_neighbours(vectors: np.ndarray, queries: np.ndarray, nn: int) -> np.ndarray:
    """(Q, nn) ids of each query's nn nearest chunks, ignoring permissions."""
    block = max(1_000, int(2e8 // (12 * max(1, len(queries)))))  # about 2.4 GB of scores and ids at most
    best_ids = np.zeros((len(queries), 0), dtype=np.int64)
    best_scores = np.zeros((len(queries), 0), dtype=np.float32)
    for start in range(0, len(vectors), block):
        part = np.asarray(vectors[start : start + block], dtype=np.float32)
        scores = queries @ part.T
        ids = np.broadcast_to(np.arange(start, start + len(part)), scores.shape)
        best_scores = np.concatenate([best_scores, scores], axis=1)
        best_ids = np.concatenate([best_ids, ids], axis=1)
        if best_scores.shape[1] > nn:
            keep = np.argpartition(-best_scores, nn - 1, axis=1)[:, :nn]
            best_scores = np.take_along_axis(best_scores, keep, axis=1)
            best_ids = np.take_along_axis(best_ids, keep, axis=1)
    return best_ids


def compute(w: Workload, k: int = 10, nn: int = 2048) -> list[dict]:
    vectors = np.asarray(w.vectors, dtype=np.float32)
    dense = vectors.shape[0] * len(w.queries) * 4 <= DENSE_LIMIT
    all_scores = vectors @ w.queries.T if dense else None
    log(f"truth: {w.n} chunks, {len(w.queries)} queries, {'dense' if dense else 'per-user'} scores")
    neighbours = unfiltered_neighbours(vectors, w.queries, min(nn, w.n))
    rows: list[dict] = []
    for layout in w.layouts:
        by_user: dict[str, list[int]] = defaultdict(list)
        for user, q in layout.queries:
            by_user[user].append(q)
        for user, qs in by_user.items():
            mask = w.readable(user, layout.user_groups.get(user, []))
            idx = np.flatnonzero(mask)
            sigma_g = len(idx) / w.n
            if dense:
                sub = all_scores[np.ix_(idx, qs)]
            else:
                sub = vectors[idx] @ w.queries[qs].T
            for j, q in enumerate(qs):
                ids, scores = top_k(sub[:, j], idx, k) if len(idx) else (idx, np.zeros(0, np.float32))
                sigma_l = float(mask[neighbours[q]].mean())
                rho = None
                if sigma_g > 0:
                    r = sigma_l / sigma_g
                    rho = (r - 1) / (r + 1)
                rows.append(
                    {
                        "layout": layout.name,
                        "user": user,
                        "q": int(q),
                        "ids": [int(i) for i in ids],
                        "scores": [float(s) for s in scores],
                        "n_readable": int(len(idx)),
                        "s_k": float(scores[-1]) if len(scores) else None,
                        "sigma_g": sigma_g,
                        "sigma_l": sigma_l,
                        "rho": rho,
                    }
                )
        log(f"truth: layout {layout.name} done")
    return rows


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--workload", type=Path, required=True)
    p.add_argument("--k", type=int, default=10)
    p.add_argument("--nn", type=int, default=2048)
    args = p.parse_args()
    w = Workload(args.workload)
    n = write_jsonl_gz(args.workload / "truth.jsonl.gz", compute(w, args.k, args.nn))
    log(f"truth: {n} rows written")


if __name__ == "__main__":
    main()
