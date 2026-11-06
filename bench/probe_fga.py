"""Checks of auth0-ai-langchain's FGARetriever against a running OpenFGA, outside the measured arms.

Uses the store and model ids that `bench.run` recorded (`--meta`), and one user of the workload with one
chunk they may read and one they may not. A stub base retriever hands FGARetriever exactly those two
LangChain documents, then this prints what FGARetriever returns, beside what the user may read:

1. `ainvoke`, documents with ids;
2. `invoke`, documents with ids (the measured arm's path);
3. `invoke`, documents without ids, readable chunk last;
4. `invoke`, documents without ids, readable chunk first.

    python -m bench.probe_fga --workload data/dev --meta results/dev-pgvector.meta.json --out results/probe-fga.json
"""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path
from typing import Any

import numpy as np
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from pydantic import ConfigDict

from .engines import OPENFGA_URL
from .util import read_json, write_json
from .workload import Workload


class Fixed(BaseRetriever):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    docs: list

    def _get_relevant_documents(self, query: str, *, run_manager: Any = None) -> list[Document]:
        return list(self.docs)

    async def _aget_relevant_documents(self, query: str, *, run_manager: Any = None) -> list[Document]:
        return list(self.docs)


def main() -> None:
    from auth0_ai_langchain import FGARetriever
    from openfga_sdk import ClientConfiguration
    from openfga_sdk.client.models import ClientBatchCheckItem

    p = argparse.ArgumentParser()
    p.add_argument("--workload", type=Path, required=True)
    p.add_argument("--meta", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    w = Workload(args.workload)
    fga = read_json(args.meta)["load"]["openfga"]
    layout = w.layouts[0]
    user = layout.queries[0][0]
    mask = w.readable(user, layout.user_groups.get(user, []))
    readable, unreadable = int(np.flatnonzero(mask)[0]), int(np.flatnonzero(~mask)[0])
    config = ClientConfiguration(api_url=OPENFGA_URL, store_id=fga["store_id"], authorization_model_id=fga["model_id"])

    def doc(i: int, with_id: bool) -> Document:
        return Document(id=str(i) if with_id else None, page_content=f"chunk {i}", metadata={"resource_id": f"c{i}"})

    def retriever(docs: list[Document]):  # noqa: ANN202
        return FGARetriever(
            retriever=Fixed(docs=docs),
            build_query=lambda d: ClientBatchCheckItem(user=f"user:{user}", relation="viewer",
                                                       object=f"chunk:{d.metadata['resource_id']}"),
            fga_configuration=config,
        )

    def returned(docs: list[Document]) -> list[str]:
        return [d.metadata["resource_id"] for d in docs]

    cases = {}
    try:
        cases["ainvoke, with ids"] = {"returned": returned(asyncio.run(
            retriever([doc(readable, True), doc(unreadable, True)]).ainvoke("q")))}
    except Exception as e:  # noqa: BLE001
        cases["ainvoke, with ids"] = {"error": f"{type(e).__name__}: {e}"}
    for label, docs in (
        ("invoke, with ids", [doc(readable, True), doc(unreadable, True)]),
        ("invoke, no ids, readable last", [doc(unreadable, False), doc(readable, False)]),
        ("invoke, no ids, readable first", [doc(readable, False), doc(unreadable, False)]),
    ):
        try:
            cases[label] = {"returned": returned(retriever(docs).invoke("q"))}
        except Exception as e:  # noqa: BLE001
            cases[label] = {"error": f"{type(e).__name__}: {e}"}
    result = {"user": user, "readable": f"c{readable}", "unreadable": f"c{unreadable}", "cases": cases}
    for label, case in cases.items():
        outside = [c for c in case.get("returned", []) if c == f"c{unreadable}"]
        print(f"{label}: {case}  outside: {outside}")
    write_json(args.out, result)


if __name__ == "__main__":
    main()
