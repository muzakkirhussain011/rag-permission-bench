"""A workload on disk: chunk vectors, who may read each chunk, and the permission layouts measured.

Files in a workload directory:

- `vectors.npy`: (N, d) float32, unit length. Chunk i has engine id `c<i>`.
- `queries.npy`: (Q, d) float32, unit length.
- `acl.npz`: who may read each chunk, as two CSR lists over name tables: `user_ptr`, `user_idx`
  (readers named directly) and `group_ptr`, `group_idx` (groups whose members may read).
- `names.json`: `{"users": [...], "groups": [...]}`, the name tables the indexes point into.
- `layouts.json`: the measured layouts (see `Layout`).
- `meta.json`: provenance, sizes and SHA-256 of every file above.

A user may read chunk i if the user is named on it or is a member of a group named on it.
Names use only `[A-Za-z0-9_]`, which every engine and store accepts as an identifier.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path

import numpy as np

from .util import read_json, sha256, write_json

NAME = re.compile(r"[A-Za-z0-9_]{1,128}")
FILES = ("vectors.npy", "queries.npy", "acl.npz", "names.json", "layouts.json")


@dataclass
class Layout:
    """Group memberships and the (user, query) pairs measured on them."""

    name: str
    user_groups: dict[str, list[str]]
    queries: list[tuple[str, int]]
    params: dict = field(default_factory=dict)

    def to_json(self) -> dict:
        return {"name": self.name, "user_groups": self.user_groups, "queries": self.queries, "params": self.params}

    @classmethod
    def from_json(cls, obj: dict) -> Layout:
        return cls(obj["name"], obj["user_groups"], [(u, int(q)) for u, q in obj["queries"]], obj.get("params", {}))


def principals(user: str, groups: list[str]) -> list[str]:
    """The strings a store filters on: `u:<user>` and `g:<group>` for each group."""
    return [f"u:{user}"] + [f"g:{g}" for g in groups]


class Workload:
    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.meta = read_json(self.root / "meta.json")
        self.vectors = np.load(self.root / "vectors.npy", mmap_mode="r")
        self.queries = np.load(self.root / "queries.npy")
        acl = np.load(self.root / "acl.npz")
        self.user_ptr, self.user_idx = acl["user_ptr"], acl["user_idx"]
        self.group_ptr, self.group_idx = acl["group_ptr"], acl["group_idx"]
        names = read_json(self.root / "names.json")
        self.user_names: list[str] = names["users"]
        self.group_names: list[str] = names["groups"]
        self.layouts = [Layout.from_json(x) for x in read_json(self.root / "layouts.json")]

    @property
    def n(self) -> int:
        return int(self.vectors.shape[0])

    @cached_property
    def _user_rows(self) -> np.ndarray:
        return np.repeat(np.arange(self.n, dtype=np.int32), np.diff(self.user_ptr))

    @cached_property
    def _group_rows(self) -> np.ndarray:
        return np.repeat(np.arange(self.n, dtype=np.int32), np.diff(self.group_ptr))

    @cached_property
    def _user_index(self) -> dict[str, int]:
        return {name: i for i, name in enumerate(self.user_names)}

    @cached_property
    def _group_index(self) -> dict[str, int]:
        return {name: i for i, name in enumerate(self.group_names)}

    def readable(self, user: str, groups: list[str]) -> np.ndarray:
        """Boolean mask over chunks: which ones this user may read."""
        mask = np.zeros(self.n, dtype=bool)
        if user in self._user_index:
            mask[self._user_rows[self.user_idx == self._user_index[user]]] = True
        gids = [self._group_index[g] for g in groups if g in self._group_index]
        if gids:
            mask[self._group_rows[np.isin(self.group_idx, gids)]] = True
        return mask

    def chunk_principals(self, i: int) -> list[str]:
        users = self.user_idx[self.user_ptr[i] : self.user_ptr[i + 1]]
        groups = self.group_idx[self.group_ptr[i] : self.group_ptr[i + 1]]
        return [f"u:{self.user_names[u]}" for u in users] + [f"g:{self.group_names[g]}" for g in groups]

    def layout(self, name: str) -> Layout:
        for layout in self.layouts:
            if layout.name == name:
                return layout
        raise KeyError(name)


def csr(lists: list[list[int]]) -> tuple[np.ndarray, np.ndarray]:
    ptr = np.zeros(len(lists) + 1, dtype=np.int64)
    ptr[1:] = np.cumsum([len(x) for x in lists])
    idx = np.fromiter((i for x in lists for i in x), dtype=np.int32, count=int(ptr[-1]))
    return ptr, idx


def save(
    root: Path,
    *,
    name: str,
    vectors: np.ndarray,
    queries: np.ndarray,
    chunk_users: list[list[int]],
    chunk_groups: list[list[int]],
    user_names: list[str],
    group_names: list[str],
    layouts: list[Layout],
    provenance: dict,
) -> None:
    """Write a workload directory, checking names and lengths, with checksums in meta.json."""
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    for label in user_names + group_names:
        if not NAME.fullmatch(label):
            raise ValueError(f"name {label!r} is not [A-Za-z0-9_]{{1,128}}")
    if len(chunk_users) != len(vectors) or len(chunk_groups) != len(vectors):
        raise ValueError("one ACL entry per chunk is needed")
    np.save(root / "vectors.npy", np.ascontiguousarray(vectors, dtype=np.float32))
    np.save(root / "queries.npy", np.ascontiguousarray(queries, dtype=np.float32))
    user_ptr, user_idx = csr(chunk_users)
    group_ptr, group_idx = csr(chunk_groups)
    np.savez(root / "acl.npz", user_ptr=user_ptr, user_idx=user_idx, group_ptr=group_ptr, group_idx=group_idx)
    write_json(root / "names.json", {"users": user_names, "groups": group_names})
    write_json(root / "layouts.json", [layout.to_json() for layout in layouts])
    meta = {
        "name": name,
        "n_chunks": int(len(vectors)),
        "dim": int(vectors.shape[1]),
        "n_queries": int(len(queries)),
        "provenance": provenance,
        "sha256": {f: sha256(root / f) for f in FILES},
    }
    write_json(root / "meta.json", meta)
