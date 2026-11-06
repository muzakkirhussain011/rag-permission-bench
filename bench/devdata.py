"""A small synthetic workload for tests and CI. Its numbers mean nothing about any arm.

Random unit vectors, chunks in random folders (groups), a few chunks naming readers directly, and
two layouts: users in a few folders and users in many.

    python -m bench.devdata --out data/dev [--n 3000] [--seed 7]
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from .workload import Layout, save


def _unit(x: np.ndarray) -> np.ndarray:
    return (x / np.linalg.norm(x, axis=1, keepdims=True)).astype(np.float32)


def build(out: Path, n: int = 3000, dim: int = 384, n_queries: int = 40, n_groups: int = 30, seed: int = 7) -> None:
    rng = np.random.default_rng(seed)
    vectors = _unit(rng.normal(size=(n, dim)))
    queries = _unit(vectors[rng.choice(n, n_queries, replace=False)] + 0.6 * _unit(rng.normal(size=(n_queries, dim))))
    group_names = [f"folder_{g}" for g in range(n_groups)]
    chunk_groups = [[int(rng.integers(n_groups))] for _ in range(n)]
    layouts, direct_users = [], []
    for label, low, high in (("few", 1, 4), ("many", 8, 20)):
        users = [f"dev_{label}_u{i}" for i in range(8)]
        direct_users += users[:2]
        user_groups = {u: sorted(group_names[g] for g in rng.choice(n_groups, rng.integers(low, high), replace=False))
                       for u in users}
        queries_ = [(u, int(q)) for u in users for q in rng.choice(n_queries, 5, replace=False)]
        layouts.append(Layout(f"dev_{label}", user_groups, queries_, {"groups_per_user": [int(low), int(high)]}))
    chunk_users = [[] for _ in range(n)]
    for i in rng.choice(n, n // 20, replace=False):
        chunk_users[int(i)] = [int(rng.integers(len(direct_users)))]
    save(out, name="dev", vectors=vectors, queries=queries, chunk_users=chunk_users, chunk_groups=chunk_groups,
         user_names=direct_users, group_names=group_names, layouts=layouts,
         provenance={"generator": "bench.devdata", "n": n, "seed": seed})


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--n", type=int, default=3000)
    p.add_argument("--seed", type=int, default=7)
    args = p.parse_args()
    build(args.out, n=args.n, seed=args.seed)


if __name__ == "__main__":
    main()
