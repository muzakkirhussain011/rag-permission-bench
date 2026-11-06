"""The MS MARCO corpus for W2 and W3: the first N passages of BEIR MS MARCO and Q dev questions, embedded.

    python -m bench.data_msmarco --out data/msmarco [--n 1000000] [--queries 300] [--seed 11]

Writes `vectors.npy` (N, 384), `queries.npy` (Q, 384), `passages.json.gz` (BEIR ids in order),
`questions.json` (ids and text) and `meta.json` (sources at pinned revisions, model, SHA-256).
Embeddings: BAAI/bge-small-en-v1.5 through fastembed (ONNX, CPU), passages with `passage_embed` and
questions with `query_embed`, normalized to unit length.
"""

from __future__ import annotations

import argparse
import gzip
import json
import time
from pathlib import Path

import numpy as np

from .util import log, sha256, write_json

CORPUS = ("BeIR/msmarco", "a918e0d11a77ed33f42f29d98340b655593b96ad")
QRELS = ("BeIR/msmarco-qrels", "253fbf8a3f8d4a0932b63882b5162bedc84779f5")
MODEL = "BAAI/bge-small-en-v1.5"


def _unit(x: np.ndarray) -> np.ndarray:
    return (x / np.linalg.norm(x, axis=1, keepdims=True)).astype(np.float32)


def passages(n: int) -> tuple[list[str], list[str]]:
    import pyarrow.parquet as pq
    from huggingface_hub import hf_hub_download

    path = hf_hub_download(CORPUS[0], "corpus/corpus-00000-of-00001.parquet", repo_type="dataset", revision=CORPUS[1])
    ids: list[str] = []
    texts: list[str] = []
    for batch in pq.ParquetFile(path).iter_batches(batch_size=50_000, columns=["_id", "title", "text"]):
        for _id, title, text in zip(*(batch.column(c).to_pylist() for c in ("_id", "title", "text")), strict=True):
            ids.append(str(_id))
            texts.append(f"{title} {text}".strip() if title else text)
            if len(ids) == n:
                return ids, texts
    return ids, texts


def questions(count: int, seed: int) -> list[dict]:
    import pyarrow.parquet as pq
    from huggingface_hub import hf_hub_download

    path = hf_hub_download(CORPUS[0], "queries/queries-00000-of-00001.parquet", repo_type="dataset", revision=CORPUS[1])
    table = pq.read_table(path, columns=["_id", "text"]).to_pydict()
    text = dict(zip((str(i) for i in table["_id"]), table["text"], strict=True))
    dev = hf_hub_download(QRELS[0], "dev.tsv", repo_type="dataset", revision=QRELS[1])
    with open(dev, encoding="utf-8") as f:
        next(f)
        dev_ids = sorted({line.split("\t")[0] for line in f if line.strip()})
    unique = [i for i in dev_ids if i in text and text[i].strip()]
    chosen = np.random.default_rng(seed).choice(len(unique), count, replace=False)
    return [{"id": unique[i], "text": text[unique[i]].strip()} for i in sorted(chosen)]


def main() -> None:
    from fastembed import TextEmbedding

    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--n", type=int, default=1_000_000)
    p.add_argument("--queries", type=int, default=300)
    p.add_argument("--seed", type=int, default=11)
    p.add_argument("--batch", type=int, default=256)
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    ids, texts = passages(args.n)
    log(f"{len(ids)} passages read")
    qs = questions(args.queries, args.seed)
    cache = args.out.parent / "fastembed_cache"
    model = TextEmbedding(MODEL, cache_dir=str(cache))
    started = time.perf_counter()
    vectors = np.empty((len(texts), 384), dtype=np.float32)
    done = 0
    for vector in model.passage_embed(texts, batch_size=args.batch):
        vectors[done] = vector
        done += 1
        if done % 100_000 == 0:
            log(f"embedded {done} passages, {done / (time.perf_counter() - started):.0f} per second")
    seconds = time.perf_counter() - started
    query_vectors = np.stack(list(model.query_embed([q["text"] for q in qs])))
    np.save(args.out / "vectors.npy", _unit(vectors))
    np.save(args.out / "queries.npy", _unit(query_vectors))
    with gzip.open(args.out / "passages.json.gz", "wt", encoding="utf-8") as f:
        json.dump(ids, f)
    write_json(args.out / "questions.json", qs)
    model_files = sorted(cache.rglob("*.onnx"))
    files = ("vectors.npy", "queries.npy", "passages.json.gz", "questions.json")
    write_json(args.out / "meta.json", {
        "corpus": {"repo": CORPUS[0], "revision": CORPUS[1], "file": "corpus/corpus-00000-of-00001.parquet",
                   "first": len(ids)},
        "questions": {"repo": QRELS[0], "revision": QRELS[1], "split": "dev", "count": len(qs), "seed": args.seed},
        "model": {"name": MODEL, "library": "fastembed",
                  "onnx": {str(f.relative_to(cache)): sha256(f) for f in model_files}},
        "embed_s": seconds,
        "sha256": {f: sha256(args.out / f) for f in files},
    })
    log(f"embedded {len(ids)} passages in {seconds:.0f} s")


if __name__ == "__main__":
    main()
