"""Small helpers shared by every module: logging, files, checksums, waiting for servers."""

from __future__ import annotations

import gzip
import hashlib
import json
import socket
import sys
import time
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", file=sys.stderr, flush=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_jsonl_gz(path: Path, rows: Iterable[dict]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with gzip.open(path, "wt", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, separators=(",", ":")) + "\n")
            n += 1
    return n


def read_jsonl_gz(path: Path) -> list[dict]:
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def wait_for_port(host: str, port: int, timeout: float = 300.0) -> None:
    deadline = time.monotonic() + timeout
    while True:
        try:
            with socket.create_connection((host, port), timeout=2):
                return
        except OSError:
            if time.monotonic() > deadline:
                raise TimeoutError(f"{host}:{port} did not open within {timeout:.0f} s") from None
            time.sleep(1)


def retry(call: Callable[[], Any], what: str, timeout: float = 300.0, every: float = 2.0) -> Any:
    """Call until it stops raising, for servers that accept connections before they can serve."""
    deadline = time.monotonic() + timeout
    while True:
        try:
            return call()
        except Exception as error:  # noqa: BLE001 - any failure means "not ready yet" here
            if time.monotonic() > deadline:
                raise TimeoutError(f"{what} was not ready within {timeout:.0f} s: {error}") from error
            time.sleep(every)
