"""The paper's figures, drawn from `bench.report`'s output only (cells.json, churn.json).

    python -m bench.figures --report report/ --out report/figures/

Every figure is a vector PDF with TrueType fonts (ACM's production checks refuse Type 3 fonts),
sized for PVLDB's columns: 3.33 in for one column, 7 in for both. Colors follow one fixed order per
strategy, so a strategy has the same color in every figure; each also has its own marker, so the
figures still read in grayscale. Intervals are the 95% bootstrap intervals over users from the
report; latency whiskers span the jobs' p50 from fastest to slowest job.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from .util import read_json

ONE, TWO = 3.33, 7.0  # PVLDB column widths, inches
# Categorical slots in a fixed order (a validated colorblind-safe palette); never cycled.
SLOTS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
MARKERS = ["o", "s", "^", "D", "v", "P", "X", "*"]
ALTERNATIVE = {"pgvector": "iterative", "qdrant": "acorn", "milvus": "iterative", "weaviate": "pathseer",
               "opensearch": "default"}
STORES = ["pgvector", "qdrant", "milvus", "weaviate", "opensearch"]
CORRELATIONS = [("neg", "negative"), ("none", "none"), ("pos", "positive")]
SHARES = [0.001, 0.01, 0.05, 0.2, 0.5]


def strategies(store: str) -> list[tuple[str, list[str]]]:
    """(label, arm names in order of preference) for the W3 figures; the first arm present is drawn.
    Post-filters are drawn with SpiceDB; OpenFGA's rows are in the tables. A store's alternative setting
    (`ALTERNATIVE`) shares one label, since each store has one."""
    alt = ALTERNATIVE[store]
    return [
        ("A1 post-filter, k", ["a1-spicedb"]),
        ("A2 post-filter, 3k", ["a2-spicedb-x3"]),
        ("A2 post-filter, 10k", ["a2-spicedb-x10"]),
        ("A3 engine pre-filter", ["a3-spicedb@default"]),
        ("A4 store filter, default", ["a4@default"]),
        ("A4 store filter, alternative", [f"a4@{alt}"] if alt != "default" else []),
        ("A5 database-native", ["a5-rls@default", "a5-dls"]),
        ("A7 wardowl", ["a7-wardowl"]),
    ]


SETTING_NAMES = {"default": "default", "iterative": "iterative", "acorn": "ACORN", "pathseer": "PathSeer"}


def arm_label(name: str) -> str:
    """A readable label for an arm id such as `a2-spicedb-x10` or `a4@acorn`."""
    arm, _, setting = name.partition("@")
    setting = SETTING_NAMES.get(setting, setting)
    engine = {"fga": "OpenFGA", "spicedb": "SpiceDB"}
    if arm.startswith(("a1-", "a2-")):
        parts = arm.split("-")
        what = "A1 post-filter" if parts[0] == "a1" else f"A2 over {parts[2][1:]}k"
        return f"{what}, {engine[parts[1]]}"
    labels = {"a0": "A0 exact control", "a3-spicedb": "A3 engine pre-filter", "a4": "A4 store filter",
              "a5-rls": "A5 row-level security", "a5-dls": "A5 document-level security", "a6-partition": "A6 partitions",
              "a7-wardowl": "A7 wardowl"}
    label = labels.get(arm, name)
    return f"{label}, {setting}" if setting else label


def _plt():  # noqa: ANN202
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "pdf.fonttype": 42, "ps.fonttype": 42, "font.size": 7, "axes.titlesize": 7, "axes.labelsize": 7,
        "xtick.labelsize": 6, "ytick.labelsize": 6, "legend.fontsize": 6, "axes.linewidth": 0.5,
        "lines.linewidth": 1.0, "lines.markersize": 3, "xtick.major.width": 0.5, "ytick.major.width": 0.5,
        "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.linewidth": 0.3,
        "grid.color": "#d9d9d6", "axes.edgecolor": "#52514e", "text.color": "#0b0b0b",
    })
    return plt


def _index(cells: list[dict]) -> dict[tuple, dict]:
    return {(c["workload"], c["store"], c["arm"], c["layout"]): c for c in cells}


def _layout(share: float, corr: str) -> str:
    return f"w3_s{share:g}".replace(".", "p") + f"_{corr}"


def w3_grid(cells: list[dict], out: Path, measure: str) -> Path | None:
    """Stores as rows, correlations as columns, readable share on x. `measure` is recall or p50."""
    plt = _plt()
    by = _index(cells)
    stores = [s for s in STORES if any(k[0] == "w3" and k[1] == s for k in by)]
    if not stores:
        return None
    fig, axes = plt.subplots(len(stores), 3, figsize=(TWO, 1.25 * len(stores) + 0.5), sharex=True,
                             sharey=measure == "recall", squeeze=False)
    handles = {}
    for row, store in enumerate(stores):
        for col, (corr, title) in enumerate(CORRELATIONS):
            ax = axes[row][col]
            for slot, (label, names) in enumerate(strategies(store)):
                arm = next((a for a in names if any(by.get(("w3", store, a, _layout(s, corr))) for s in SHARES)), None)
                if arm is None:
                    continue
                xs, ys, lo, hi = [], [], [], []
                for share in SHARES:
                    c = by.get(("w3", store, arm, _layout(share, corr)))
                    if c is None:
                        continue
                    if measure == "recall":
                        if c["recall"] is None:
                            continue
                        y, (a, b) = c["recall"], c["recall_95"]
                    else:
                        y, a, b = c["p50_ms"]["median"], c["p50_ms"]["min"], c["p50_ms"]["max"]
                    xs.append(share), ys.append(y), lo.append(y - a), hi.append(b - y)
                if not xs:
                    continue
                h = ax.errorbar(xs, ys, yerr=[lo, hi], color=SLOTS[slot], marker=MARKERS[slot], capsize=0,
                                elinewidth=0.6, label=label)
                handles.setdefault(label, h)
            ax.set_xscale("log")
            if measure == "recall":
                ax.set_ylim(-0.03, 1.03)
            else:
                ax.set_yscale("log")
            if row == 0:
                ax.set_title(f"correlation: {title}")
            if col == 0:
                ax.set_ylabel(f"{store}\n" + ("recall@10" if measure == "recall" else "p50 latency (ms)"))
            if row == len(stores) - 1:
                ax.set_xlabel("readable share")
    fig.legend(list(handles.values()), list(handles), loc="upper center", ncol=4, frameon=False,
               bbox_to_anchor=(0.5, 1.0))
    fig.tight_layout(rect=(0, 0, 1, 1 - 0.32 / (1.25 * len(stores) + 0.5)))
    path = out / f"w3-{measure}.pdf"
    fig.savefig(path)
    plt.close(fig)
    return path


def dots(cells: list[dict], workload: str, layout: str, out: Path) -> Path | None:
    """One panel per store: every arm's recall@10 with its 95% interval (W1 own mail, a W2 variant)."""
    plt = _plt()
    rows = [c for c in cells if c["workload"] == workload and c["layout"] == layout and c["recall"] is not None]
    stores = [s for s in STORES if any(c["store"] == s for c in rows)]
    if not stores:
        return None
    arms = sorted({c["arm"] for c in rows})
    fig, axes = plt.subplots(1, len(stores), figsize=(TWO, 0.16 * len(arms) + 0.6), sharey=True, squeeze=False)
    for i, store in enumerate(stores):
        ax = axes[0][i]
        for y, arm in enumerate(arms):
            c = next((c for c in rows if c["store"] == store and c["arm"] == arm), None)
            if c is None:
                continue
            a, b = c["recall_95"]
            ax.errorbar([c["recall"]], [y], xerr=[[c["recall"] - a], [b - c["recall"]]], color=SLOTS[0], marker="o",
                        capsize=0, elinewidth=0.6)
        ax.set_yticks(range(len(arms)), arms)
        ax.set_xlim(-0.03, 1.03)
        ax.set_title(store)
        ax.set_xlabel("recall@10")
    fig.tight_layout()
    path = out / f"{layout}-recall.pdf"
    fig.savefig(path)
    plt.close(fig)
    return path


def churn(rows: list[dict], out: Path) -> Path | None:
    """Median change delay per arm (dot) with its 90th percentile (whisker), revocations and grants."""
    plt = _plt()
    if not rows:
        return None
    arms = sorted({r["arm"] for r in rows})
    stores = [s for s in STORES if any(r["store"] == s for r in rows)]
    fig, axes = plt.subplots(1, 2, figsize=(TWO, 0.18 * len(arms) + 0.7), sharey=True, squeeze=False)
    for col, kind in enumerate(("revoke", "grant")):
        ax = axes[0][col]
        for slot, store in enumerate(stores):
            for y, arm in enumerate(arms):
                r = next((r for r in rows if r["store"] == store and r["arm"] == arm and r["kind"] == kind), None)
                if r is None or r["delay_s"] is None:
                    continue
                p50, p90, _ = r["delay_s"]
                offset = (slot - (len(stores) - 1) / 2) * 0.12
                ax.errorbar([max(p50, 1e-3)], [y + offset], xerr=[[0], [max(p90 - p50, 0)]], color=SLOTS[slot],
                            marker=MARKERS[slot], capsize=0, elinewidth=0.6, label=store if y == 0 else None)
        ax.set_xscale("log")
        ax.set_yticks(range(len(arms)), [arm_label(a) for a in arms])
        ax.set_title("revocation" if kind == "revoke" else "grant")
        ax.set_xlabel("delay until answers reflect it (s)")
    axes[0][1].legend(frameon=False, loc="lower right")
    fig.tight_layout()
    path = out / "churn.pdf"
    fig.savefig(path)
    plt.close(fig)
    return path


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    cells = read_json(args.report / "cells.json")
    made = [w3_grid(cells, args.out, "recall"), w3_grid(cells, args.out, "p50"),
            dots(cells, "w1_enron", "w1_enron", args.out)]
    made += [dots(cells, w, w, args.out) for w in sorted({c["workload"] for c in cells if c["workload"].startswith("w2_")})]
    churn_path = args.report / "churn.json"
    made.append(churn(read_json(churn_path), args.out) if churn_path.exists() else None)
    for path in made:
        if path is not None:
            print(f"wrote {path}")


if __name__ == "__main__":
    main()
