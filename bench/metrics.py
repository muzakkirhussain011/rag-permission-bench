"""Scoring one answer against the exact answer (see `truth.py`).

- recall@k: returned chunks that the user may read and that score at least the k-th exact score
  (minus `EPS`, so exact ties count), over min(k, readable count). Undefined when nothing is readable.
- outside: returned chunks the user may not read.
- empty: no hits although the user may read at least k chunks.

Hits are de-duplicated, keeping the first occurrence, and only the first k count.
"""

from __future__ import annotations

import numpy as np

EPS = 1e-5


def score(hits: list[int], truth: dict, mask: np.ndarray, vectors: np.ndarray, query: np.ndarray, k: int = 10) -> dict:
    seen: dict[int, None] = {}
    for h in hits:
        seen.setdefault(int(h), None)
    ids = list(seen)[:k]
    n_readable = truth["n_readable"]
    outside = sum(1 for i in ids if not mask[i])
    recall = None
    if n_readable > 0:
        readable_ids = [i for i in ids if mask[i]]
        correct = 0
        if readable_ids:
            exact = np.asarray(vectors[readable_ids], dtype=np.float32) @ query
            correct = int(np.sum(exact >= truth["s_k"] - EPS))
        recall = correct / min(k, n_readable)
    return {
        "recall": recall,
        "outside": outside,
        "empty": len(ids) == 0 and n_readable >= k,
        "n_hits": len(ids),
        "duplicates": len(hits) - len(seen),
    }
