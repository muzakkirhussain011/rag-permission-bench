"""W3, the controlled sweep: readable share crossed with query-permission correlation.

The corpus is split into k-means clusters, each a folder (group) that users are granted whole. For a
layout (share s, correlation c), each user asks `per_user` questions, and is granted folders in an
order set by c until the folders hold at least s of the corpus:

- pos: folders whose centroid is nearest the mean of the user's questions first;
- none: folders in random order;
- neg: the farthest first.

The achieved share and correlation are measured per query in `bench.truth`.

    python -m bench.w3 --corpus data/msmarco --out data/w3 [--folders 1000] [--users 100] [--seed 13]

The workload directory holds a copy of the corpus vectors; releases ship them once, beside it.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import numpy as np

from .util import log, read_json
from .workload import Layout, save

SHARES = (0.001, 0.01, 0.05, 0.2, 0.5)
CORRELATIONS = ("pos", "none", "neg")


def share_code(share: float) -> str:
    return f"{share:g}".replace(".", "p")


def folders(vectors: np.ndarray, n_folders: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    from sklearn.cluster import MiniBatchKMeans

    km = MiniBatchKMeans(n_clusters=n_folders, random_state=seed, batch_size=8192, n_init=3, max_iter=100)
    labels = km.fit_predict(vectors)
    centroids = km.cluster_centers_
    centroids = centroids / np.linalg.norm(centroids, axis=1, keepdims=True)
    return labels.astype(np.int32), centroids.astype(np.float32)


def layouts(labels: np.ndarray, centroids: np.ndarray, queries: np.ndarray, users: int, per_user: int,
            seed: int) -> list[Layout]:
    rng = np.random.default_rng(seed)
    sizes = np.bincount(labels, minlength=len(centroids))
    n = len(labels)
    out = []
    for share in SHARES:
        for corr in CORRELATIONS:
            name = f"w3_s{share_code(share)}_{corr}"
            user_groups, pairs, achieved = {}, [], []
            for i in range(users):
                user = f"{name}_u{i}"
                qs = rng.choice(len(queries), per_user, replace=False)
                interest = queries[qs].mean(axis=0)
                sims = centroids @ (interest / np.linalg.norm(interest))
                order = {"pos": np.argsort(-sims), "neg": np.argsort(sims), "none": rng.permutation(len(sims))}[corr]
                taken = int(np.searchsorted(np.cumsum(sizes[order]), share * n) + 1)
                granted = order[:taken]
                user_groups[user] = [f"f{g}" for g in sorted(granted.tolist())]
                pairs += [(user, int(q)) for q in qs]
                achieved.append(sizes[granted].sum() / n)
            out.append(Layout(name, user_groups, pairs, {"share": share, "correlation": corr,
                                                         "achieved_share_mean": float(np.mean(achieved))}))
            log(f"{name}: mean achieved share {np.mean(achieved):.4f}")
    return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--corpus", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--folders", type=int, default=1000)
    p.add_argument("--users", type=int, default=100)
    p.add_argument("--per-user", type=int, default=10)
    p.add_argument("--seed", type=int, default=13)
    args = p.parse_args()
    vectors = np.load(args.corpus / "vectors.npy")
    queries = np.load(args.corpus / "queries.npy")
    labels, centroids = folders(vectors, args.folders, args.seed)
    log(f"{args.folders} folders, sizes {np.bincount(labels).min()} to {np.bincount(labels).max()}")
    layout_list = layouts(labels, centroids, queries, args.users, args.per_user, args.seed)
    save(args.out, name="w3", vectors=vectors, queries=queries,
         chunk_users=[[] for _ in range(len(labels))], chunk_groups=[[int(g)] for g in labels],
         user_names=[], group_names=[f"f{g}" for g in range(args.folders)], layouts=layout_list,
         provenance={"corpus": read_json(args.corpus / "meta.json"), "generator": "bench.w3",
                     "folders": args.folders, "users_per_layout": args.users, "per_user": args.per_user,
                     "seed": args.seed, "shares": SHARES, "correlations": CORRELATIONS})
    np.save(args.out / "folders.npy", labels)
    shutil.copy(args.corpus / "meta.json", args.out / "corpus-meta.json")


if __name__ == "__main__":
    main()
