"""W2: HoneyBee's synthetic RBAC workloads (Zhong et al., arXiv 2505.01538v3, section 6.2), re-implemented.

Written from the paper's text, not its code (the repository has no license). Where the paper is
silent, this module chooses, and says so:

- counts "between 1 and m" are drawn uniformly from {1, ..., m}; members are drawn without replacement;
- Tree splits the documents into |R| random subsets of equal size (+-1);
- role inheritance (Tree) and business roles (ERBAC) are flattened into group memberships: a user is
  a member of every group whose documents the user may read, which gives the same readable sets.

Variants (paper's names): tree_a (h = 4, b0 = 3, b1 = 4), uniform_a (m_r = 2, m_p = 5|D|/|R|),
erbac_a (n_fr = 40, n_br = 100, m_fr = 3, m_br = 3, m_p = |D|/25), erbac_b (erbac_a with m_br = 9).
1,000 users and 100 roles. The paper's Table 1 reports average access selectivity 0.036 (Tree),
0.054 (Uniform), 0.128 and 0.285 (ERBAC); `meta.json` records what this implementation produced.

Queries: `users` users drawn at random, each asking `per_user` of the corpus questions (the paper
used database vectors as queries; we use real questions, as in W3).

    python -m bench.w2 --corpus data/msmarco --out data/w2 --variant tree_a [--n 200000] [--seed 17]
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from .util import log, read_json, write_json
from .workload import Layout, Workload, save

N_USERS = 1000
N_ROLES = 100


def _count(rng: np.random.Generator, high: int) -> int:
    return int(rng.integers(1, max(1, high) + 1))


def tree(n_docs: int, rng: np.random.Generator, h: int = 4, b0: int = 3, b1: int = 4):
    """Roles in a tree; each role owns one subset of documents and sees its ancestors' too."""
    parent = [-1]
    depth = [0]
    frontier = [0]
    while frontier and len(parent) < N_ROLES:
        nxt = []
        for node in frontier:
            if depth[node] >= h:
                continue
            for _ in range(_count_between(rng, b0, b1)):
                if len(parent) == N_ROLES:
                    break
                parent.append(node)
                depth.append(depth[node] + 1)
                nxt.append(len(parent) - 1)
        frontier = nxt
    n_roles = len(parent)
    owner = rng.permutation(np.arange(n_docs) % n_roles)  # equal subsets, random membership
    chunk_groups = [[int(r)] for r in owner]

    def ancestors(r: int) -> list[int]:
        out = []
        while r != -1:
            out.append(r)
            r = parent[r]
        return out

    non_root = list(range(1, n_roles))
    users = [[*ancestors(non_root[u % len(non_root)])] for u in range(N_USERS)]  # evenly, one role each
    return chunk_groups, users, n_roles, {"roles": n_roles, "max_depth": max(depth)}


def _count_between(rng: np.random.Generator, low: int, high: int) -> int:
    return int(rng.integers(low, high + 1))


def uniform(n_docs: int, rng: np.random.Generator, m_r: int = 2, m_p_factor: int = 5):
    m_p = n_docs * m_p_factor // N_ROLES
    members: list[list[int]] = [[] for _ in range(n_docs)]
    for r in range(N_ROLES):
        for d in rng.choice(n_docs, _count(rng, m_p), replace=False):
            members[int(d)].append(r)
    users = [sorted(rng.choice(N_ROLES, _count(rng, m_r), replace=False).tolist()) for _ in range(N_USERS)]
    return members, users, N_ROLES, {"m_r": m_r, "m_p": m_p}


def erbac(n_docs: int, rng: np.random.Generator, n_fr: int = 40, n_br: int = 100, m_fr: int = 3, m_br: int = 3,
          m_p_divisor: int = 25):
    """Groups are functional roles (they own documents); users get them through business roles."""
    m_p = n_docs // m_p_divisor
    members: list[list[int]] = [[] for _ in range(n_docs)]
    for f in range(n_fr):
        for d in rng.choice(n_docs, _count(rng, m_p), replace=False):
            members[int(d)].append(f)
    business = [rng.choice(n_fr, _count(rng, m_fr), replace=False).tolist() for _ in range(n_br)]
    users = []
    for _ in range(N_USERS):
        brs = rng.choice(n_br, _count(rng, m_br), replace=False)
        users.append(sorted({f for b in brs for f in business[b]}))
    return members, users, n_fr, {"n_fr": n_fr, "n_br": n_br, "m_fr": m_fr, "m_br": m_br, "m_p": m_p}


VARIANTS = {
    "tree_a": lambda n, rng: tree(n, rng),
    "uniform_a": lambda n, rng: uniform(n, rng),
    "erbac_a": lambda n, rng: erbac(n, rng),
    "erbac_b": lambda n, rng: erbac(n, rng, m_br=9),
}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--corpus", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--variant", choices=sorted(VARIANTS), required=True)
    p.add_argument("--n", type=int, default=200_000)
    p.add_argument("--users", type=int, default=100)
    p.add_argument("--per-user", type=int, default=10)
    p.add_argument("--seed", type=int, default=17)
    args = p.parse_args()
    rng = np.random.default_rng(args.seed)
    vectors = np.load(args.corpus / "vectors.npy", mmap_mode="r")[: args.n]
    queries = np.load(args.corpus / "queries.npy")
    chunk_groups, user_groups, n_groups, params = VARIANTS[args.variant](len(vectors), rng)
    names = [f"{args.variant}_u{u}" for u in range(N_USERS)]
    sizes = np.bincount([g for gs in chunk_groups for g in gs], minlength=n_groups)
    chosen = rng.choice(N_USERS, args.users, replace=False)
    pairs = [(names[u], int(q)) for u in chosen for q in rng.choice(len(queries), args.per_user, replace=False)]
    layout = Layout(f"w2_{args.variant}", {names[u]: [f"r{g}" for g in user_groups[u]] for u in range(N_USERS)},
                    pairs, {"variant": args.variant, **params})
    save(args.out, name=f"w2_{args.variant}", vectors=np.asarray(vectors), queries=queries,
         chunk_users=[[] for _ in range(len(vectors))], chunk_groups=chunk_groups, user_names=[],
         group_names=[f"r{g}" for g in range(n_groups)], layouts=[layout],
         provenance={"corpus": read_json(args.corpus / "meta.json"), "generator": "bench.w2",
                     "variant": args.variant, "params": params, "n": len(vectors), "seed": args.seed,
                     "group_sizes": sizes.tolist()})
    w = Workload(args.out)
    shares = np.array([w.readable(names[u], [f"r{g}" for g in user_groups[u]]).mean() for u in range(N_USERS)])
    write_json(args.out / "w2-stats.json", {
        "variant": args.variant,
        "readable_share_mean": float(shares.mean()),
        "readable_share_quartiles": np.percentile(shares, [0, 25, 50, 75, 100]).tolist(),
        "groups_per_user_max": max(len(g) for g in user_groups),
        "honeybee_table1_avg_access_selectivity": {"tree_a": 0.036, "uniform_a": 0.054, "erbac_a": 0.128,
                                                   "erbac_b": 0.285}[args.variant],
    })
    log(f"w2 {args.variant}: {n_groups} groups, mean readable share {shares.mean():.4f}, {len(pairs)} pairs")


if __name__ == "__main__":
    main()
