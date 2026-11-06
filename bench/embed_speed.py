"""How fast each way of running bge-small-en-v1.5 embeds MS MARCO passages on this machine.

    python -m bench.embed_speed [--n 2000]

Prints passages per second for each variant and the largest difference between their vectors and
the first variant's, so a faster variant can be checked for giving the same vectors.
"""

from __future__ import annotations

import argparse
import os
import time

import numpy as np

from .data_msmarco import MODEL, passages


def _unit(x: np.ndarray) -> np.ndarray:
    return x / np.linalg.norm(x, axis=1, keepdims=True)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=2000)
    args = p.parse_args()
    _, texts = passages(args.n)
    print("cpus", os.cpu_count())
    results = {}

    from fastembed import TextEmbedding

    for label, kwargs, embed_kwargs in (
        ("fastembed default, batch 256", {}, {"batch_size": 256}),
        ("fastembed threads=4, batch 32", {"threads": 4}, {"batch_size": 32}),
        ("fastembed parallel=0, batch 32", {}, {"batch_size": 32, "parallel": 0}),
    ):
        model = TextEmbedding(MODEL, cache_dir="fastembed_cache", **kwargs)
        list(model.passage_embed(texts[:64], **embed_kwargs))
        start = time.perf_counter()
        vectors = np.stack(list(model.passage_embed(texts, **embed_kwargs)))
        rate = len(texts) / (time.perf_counter() - start)
        results[label] = _unit(vectors)
        print(f"{label}: {rate:.1f} passages/s")

    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(MODEL, device="cpu")
    model.encode(texts[:64], batch_size=32)
    start = time.perf_counter()
    vectors = model.encode(texts, batch_size=32, normalize_embeddings=True)
    print(f"sentence-transformers cpu, batch 32: {len(texts) / (time.perf_counter() - start):.1f} passages/s")
    results["sentence-transformers"] = vectors
    first = next(iter(results.values()))
    for label, v in results.items():
        print(f"max |diff| vs first, {label}: {np.abs(v - first).max():.5f}; min cosine {(v * first).sum(1).min():.5f}")


if __name__ == "__main__":
    main()
