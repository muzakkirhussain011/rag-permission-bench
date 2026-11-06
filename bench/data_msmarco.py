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

from .util import log, read_json, sha256, write_json

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


def _model(cache: Path):  # noqa: ANN202
    from fastembed import TextEmbedding

    return TextEmbedding(MODEL, cache_dir=str(cache))


def _embed(model, texts: list[str], batch: int, parallel: int | None) -> np.ndarray:  # noqa: ANN001
    started = time.perf_counter()
    vectors = np.empty((len(texts), 384), dtype=np.float32)
    done = 0
    for vector in model.passage_embed(texts, batch_size=batch, parallel=parallel):
        vectors[done] = vector
        done += 1
        if done % 20_000 == 0:
            log(f"embedded {done} passages, {done / (time.perf_counter() - started):.0f} per second")
    return vectors


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--n", type=int, default=1_000_000)
    p.add_argument("--queries", type=int, default=300)
    p.add_argument("--seed", type=int, default=11)
    p.add_argument("--batch", type=int, default=32)
    p.add_argument("--parallel", type=int, default=0, help="fastembed's data-parallel workers (0: one per core)")
    p.add_argument("--shard", type=int, default=None, help="embed only shard I of --shards and stop")
    p.add_argument("--shards", type=int, default=1)
    p.add_argument("--assemble", type=Path, default=None, help="join shard_*.npy from this directory")
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    cache = args.out.parent / "fastembed_cache"
    parallel = args.parallel if args.parallel >= 0 else None

    ids, texts = passages(args.n)
    log(f"{len(ids)} passages read")
    bounds = np.linspace(0, len(texts), args.shards + 1).astype(int)
    if args.shard is not None:
        start, stop = int(bounds[args.shard]), int(bounds[args.shard + 1])
        began = time.perf_counter()
        part = _embed(_model(cache), texts[start:stop], args.batch, parallel)
        np.save(args.out / f"shard_{args.shard}.npy", part)
        write_json(args.out / f"shard_{args.shard}.json", {"start": start, "stop": stop,
                                                           "seconds": time.perf_counter() - began})
        log(f"shard {args.shard}: passages {start} to {stop} in {time.perf_counter() - began:.0f} s")
        return
    model = _model(cache)
    started = time.perf_counter()
    if args.assemble is not None:
        parts, info = [], []
        for i in range(args.shards):
            meta = read_json(args.assemble / f"shard_{i}.json")
            if meta["start"] != int(bounds[i]) or meta["stop"] != int(bounds[i + 1]):
                raise ValueError(f"shard {i} covers {meta['start']}-{meta['stop']}, not {bounds[i]}-{bounds[i + 1]}")
            parts.append(np.load(args.assemble / f"shard_{i}.npy"))
            info.append(meta)
        vectors = np.concatenate(parts)
        seconds = sum(m["seconds"] for m in info)
    else:
        vectors = _embed(model, texts, args.batch, parallel)
        seconds = time.perf_counter() - started
    qs = questions(args.queries, args.seed)
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
        "model": {"name": MODEL, "library": "fastembed", "batch": args.batch, "parallel": args.parallel,
                  "onnx": {str(f.relative_to(cache)): sha256(f) for f in model_files}},
        "embed_s": seconds, "shards": args.shards,
        "sha256": {f: sha256(args.out / f) for f in files},
    })
    log(f"embedded {len(ids)} passages in {seconds:.0f} s")


if __name__ == "__main__":
    main()
