"""W1, real sharing: the Enron mail corpus (CMU release of 2015-05-07), where the readers of a message
are the addresses in its From, To, Cc and Bcc headers.

- Messages are de-duplicated by Message-ID, then by a hash of subject and body (readers are merged).
- A chunk is one message: subject and body; the embedding model cuts it at its own limit.
- Users are the addresses that may read at least `min_readable` messages; `users` of them are sampled,
  stratified by quartile of readable count.
- Each sampled user asks 10 "own mail" questions (subjects of messages they may read) and 10 "other
  mail" questions (subjects of messages they may not); subjects without "Re:"/"Fw:" prefixes and with at
  least three words.
- Addresses become numbers (`u<n>`, by sorted address) before anything is written; message text is
  never written. The address-to-number map stays on the runner; the pipeline rebuilds it from the
  public corpus.

The CMU page asks users to be sensitive to the privacy of the people involved, and reports (April
2026) an impersonation capability in Enron's eMeet system; the From header is used as recorded.

    python -m bench.w1_enron --tarball enron_mail_20150507.tar.gz --out data/w1 [--users 200] [--seed 19]
"""

from __future__ import annotations

import argparse
import email
import email.policy
import hashlib
import re
import tarfile
import time
from collections import defaultdict
from email.utils import getaddresses
from pathlib import Path

import numpy as np

from .util import log, sha256, write_json
from .workload import Layout, save

MODEL = "BAAI/bge-small-en-v1.5"
PREFIX = re.compile(r"^\s*((re|fw|fwd)\s*:\s*)+", re.IGNORECASE)


def _addresses(message: email.message.Message, header: str) -> list[str]:
    values = message.get_all(header) or []
    return [a.strip().lower() for _, a in getaddresses([str(v) for v in values]) if "@" in a]


def _body(message: email.message.Message) -> str:
    if message.is_multipart():
        parts = [p for p in message.walk() if p.get_content_type() == "text/plain"]
        payload = parts[0].get_payload(decode=True) if parts else b""
    else:
        payload = message.get_payload(decode=True) or b""
    return payload.decode("latin-1", errors="replace") if isinstance(payload, bytes) else str(payload)


def read_messages(tarball: Path) -> tuple[list[str], list[str], list[set[str]], dict]:
    """(subjects, texts, readers) of unique messages, and counts of what was read and merged."""
    by_id: dict[str, int] = {}
    by_hash: dict[str, int] = {}
    subjects: list[str] = []
    texts: list[str] = []
    readers: list[set[str]] = []
    files = no_reader = 0
    with tarfile.open(tarball, "r:gz") as tar:
        for member in tar:
            if not member.isfile():
                continue
            files += 1
            raw = tar.extractfile(member).read()
            message = email.message_from_bytes(raw, policy=email.policy.compat32)
            people = set()
            for header in ("From", "To", "Cc", "Bcc"):
                people.update(_addresses(message, header))
            if not people:
                no_reader += 1
                continue
            subject = str(message.get("Subject") or "").strip()
            body = _body(message)
            message_id = str(message.get("Message-ID") or "").strip()
            digest = hashlib.sha256((subject + "\n" + body).encode("utf-8", "replace")).hexdigest()
            index = by_id.get(message_id) if message_id else None
            if index is None:
                index = by_hash.get(digest)
            if index is None:
                index = len(texts)
                subjects.append(subject)
                texts.append(f"{subject}\n{body}".strip())
                readers.append(set())
                by_hash[digest] = index
            if message_id:
                by_id[message_id] = index
            readers[index].update(people)
            if files % 100_000 == 0:
                log(f"read {files} files, {len(texts)} unique messages")
    return subjects, texts, readers, {"files": files, "unique": len(texts), "without_readers": no_reader}


def main() -> None:
    from fastembed import TextEmbedding

    p = argparse.ArgumentParser()
    p.add_argument("--tarball", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--users", type=int, default=200)
    p.add_argument("--min-readable", type=int, default=50)
    p.add_argument("--per-kind", type=int, default=10)
    p.add_argument("--seed", type=int, default=19)
    p.add_argument("--limit", type=int, default=0, help="read only the first N unique messages (tests)")
    args = p.parse_args()
    rng = np.random.default_rng(args.seed)

    subjects, texts, readers, counts = read_messages(args.tarball)
    if args.limit:
        subjects, texts, readers = subjects[: args.limit], texts[: args.limit], readers[: args.limit]
    addresses = sorted({a for r in readers for a in r})
    number = {a: i for i, a in enumerate(addresses)}
    chunk_users = [sorted(number[a] for a in r) for r in readers]
    readable: dict[int, list[int]] = defaultdict(list)
    for i, users in enumerate(chunk_users):
        for u in users:
            readable[u].append(i)
    eligible = np.array(sorted(u for u, msgs in readable.items() if len(msgs) >= args.min_readable))
    sizes = np.array([len(readable[u]) for u in eligible])
    quartile = np.digitize(sizes, np.percentile(sizes, [25, 50, 75]))
    chosen = []
    for q in range(4):
        pool = eligible[quartile == q]
        chosen += rng.choice(pool, min(len(pool), args.users // 4), replace=False).tolist()

    def usable(i: int) -> str | None:
        s = PREFIX.sub("", subjects[i]).strip()
        return s if len(s.split()) >= 3 else None

    query_texts: dict[str, int] = {}
    pairs, kinds = [], {}
    for u in chosen:
        own = [i for i in rng.permutation(readable[u]) if usable(int(i))][: args.per_kind]
        mine = set(readable[u])
        other: list[int] = []
        while len(other) < args.per_kind:
            i = int(rng.integers(len(texts)))
            if i not in mine and usable(i):
                other.append(i)
        for kind, msgs in (("own", own), ("other", other)):
            for i in msgs:
                text = usable(int(i))
                q = query_texts.setdefault(text, len(query_texts))
                pairs.append((f"u{u}", q))
                kinds[f"u{u}|{q}"] = kind
    log(f"{len(chosen)} users, {len(pairs)} pairs, {len(query_texts)} distinct questions")

    model = TextEmbedding(MODEL, cache_dir=str(args.out.parent / "fastembed_cache"))
    started = time.perf_counter()
    vectors = np.stack(list(model.passage_embed(texts, batch_size=64)))
    queries = np.stack(list(model.query_embed(list(query_texts))))
    seconds = time.perf_counter() - started
    unit = lambda x: (x / np.linalg.norm(x, axis=1, keepdims=True)).astype(np.float32)  # noqa: E731
    layout = Layout("w1_enron", {}, pairs, {"kinds": kinds, "min_readable": args.min_readable})
    save(args.out, name="w1_enron", vectors=unit(vectors), queries=unit(queries), chunk_users=chunk_users,
         chunk_groups=[[] for _ in texts], user_names=[f"u{i}" for i in range(len(addresses))], group_names=[],
         layouts=[layout], provenance={
             "source": {"url": "https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz",
                        "sha256": sha256(args.tarball)},
             "counts": counts, "addresses": len(addresses), "eligible_users": int(len(eligible)),
             "model": MODEL, "embed_s": seconds, "seed": args.seed, "generator": "bench.w1_enron",
         })
    write_json(args.out / "w1-stats.json", {
        "readers_per_message": np.percentile([len(r) for r in chunk_users], [50, 90, 99, 100]).tolist(),
        "readable_per_chosen_user": np.percentile([len(readable[u]) for u in chosen], [0, 25, 50, 75, 100]).tolist(),
        "messages": len(texts),
    })


if __name__ == "__main__":
    main()
