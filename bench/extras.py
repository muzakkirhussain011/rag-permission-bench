"""Supplementary analyses of a measured release (default results-v1), run in GitHub Actions by `extras.yml`.

None of this is the registered analysis, which is `bench.report`. Parts (a) and (b) report what the
pre-registration promised beside the hypotheses (sections 2, 4 and 5); part (c) is exploratory.

    python -m bench.extras --results artifacts/ --report report/ --workloads workloads/ --out extras/
        [--rebuilt rebuilt/report] [--resamples 10000] [--seed 5] [--release results-v1] [--checksums SHA256SUMS]

`--results` is results-raw.tar.gz extracted (one folder per measured job), `--report` the release's report.tar.gz
extracted, `--workloads` a folder holding each workload release extracted into its own subfolder (`meta.json`,
`layouts.json`, `truth.jsonl.gz`, stats file), and `--rebuilt` an optional report rebuilt from the raw outputs with
`bench.report`, which is compared with the published one.

- (a) Workloads: per layout, the readable share each user achieved (sigma_g) and the per-query correlation rho_q,
  as `bench.truth` wrote them when the data were built; the W2 readable shares beside HoneyBee's Table 1; W1 by
  question kind.
- (b) Costs the jobs recorded: p50 and p99 latency per job and cell (computed as `bench.report` does, and checked
  against the published cells), container memory after the measured pass (`docker stats`), what each store and
  engine reported about size and load or index time, the partitions of A6, the runners; and what was not recorded.
- (c) Exploratory: every interval of H1 to H8 recomputed at the registered level under three bootstrap schemes,
  users only (the registered scheme), questions as clusters, and users crossed with questions, each judged by the
  registered rule. In W2 and W3 users draw their questions from one pool of 300, so answers to one question are
  correlated across users, which a bootstrap over users alone does not see.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from . import report
from .util import log, read_json, read_jsonl_gz, write_json

SCHEMES = ("users", "questions", "users_x_questions")
SCHEME_TEXT = {
    "users": "users resampled, questions fixed: the registered scheme, recomputed here with its own generator",
    "questions": "questions resampled as clusters (all pairs of a drawn question, over every user and job), users "
                 "fixed",
    "users_x_questions": "users and questions resampled independently, each pair weighted by the product of the two "
                         "draws (the pigeonhole bootstrap of Owen 2007, which tends to overstate the variance)",
}
HYPOTHESES = ("H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8")
W1_ARMS = {"H1": ("a1-fga", "a1-spicedb"), "H2": ("a2-fga-x10", "a2-spicedb-x10")}
H3_LAYOUTS = frozenset(f"w3_s{s}_{c}" for s in report.SHARES[:3] for c in ("neg", "pos"))
H7_ARMS = ("a5-rls@default", "a5-rls@iterative", "a4@default", "a4@iterative")
PART_KEYS = {"H1": ("store", "arm"), "H2": ("store", "arm"), "H3": ("store", "share", "arm"), "H5": ("layout",),
             "H6": ("store", "layout"), "H7": ("setting", "layout")}
UNITS = {"B": 1, "KiB": 2**10, "MiB": 2**20, "GiB": 2**30, "TiB": 2**40, "kB": 1e3, "KB": 1e3, "MB": 1e6, "GB": 1e9,
         "TB": 1e12}
MIB = 2**20


# ---------------------------------------------------------------- helpers


def isnum(x: object) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and not math.isnan(x)


def stats(values) -> dict | None:  # noqa: ANN001
    """Count, mean and quantiles of the defined values."""
    v = np.array([x for x in values if isnum(x)], dtype=float)
    if not len(v):
        return None
    q = np.percentile(v, [0, 25, 50, 75, 100])
    return {"n": int(len(v)), "mean": float(v.mean()), "min": float(q[0]), "p25": float(q[1]),
            "median": float(q[2]), "p75": float(q[3]), "max": float(q[4])}


def spread(values) -> dict | None:  # noqa: ANN001
    """Median and range, as bench.report gives latency over jobs."""
    v = [float(x) for x in values if isnum(x)]
    if not v:
        return None
    return {"median": float(np.median(v)), "min": min(v), "max": max(v), "n": len(v)}


def fmt(x: object, digits: int = 3) -> str:
    return f"{x:.{digits}f}" if isnum(x) else "n/a"


def fmt_spread(s: dict | None, digits: int = 1, scale: float = 1.0) -> str:
    if not s:
        return "not recorded"
    med, lo, hi = s["median"] / scale, s["min"] / scale, s["max"] / scale
    if f"{lo:.{digits}f}" == f"{hi:.{digits}f}":
        return f"{med:.{digits}f}"
    return f"{med:.{digits}f} ({lo:.{digits}f} to {hi:.{digits}f})"


def job_kind(name: str) -> str:
    return "churn" if "-churn-" in name else "faults" if "-faults-" in name else "run"


def share_part(name: str) -> str:
    """The readable share a W3 job covered, from its name (measured-run-w3-s0p01-pgvector-seed1 -> s0p01)."""
    m = re.search(r"-w3-(s[0-9p+]+)-", name)
    return m.group(1) if m else ""


def mem_bytes(text: str) -> float | None:
    """`1.5GiB` (the used part of docker stats' MemUsage) in bytes."""
    m = re.match(r"\s*([0-9.]+)\s*([A-Za-z]+)", text or "")
    return float(m.group(1)) * UNITS[m.group(2)] if m and m.group(2) in UNITS else None


def service(container: str) -> str:
    """Compose container name to service name: bench-pgvector-1 -> pgvector."""
    return re.sub(r"-\d+$", "", re.sub(r"^bench-", "", container))


def flat(record: dict, prefix: str = "") -> dict:
    """Nested load records as dotted keys; numeric strings become numbers."""
    out: dict = {}
    for k, v in record.items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            out.update(flat(v, key + "."))
        elif isinstance(v, str):
            try:
                out[key] = float(v)
            except ValueError:
                out[key] = v
        else:
            out[key] = v
    return out


def mem_total_gib(line: str | None) -> float | None:
    m = re.search(r"(\d+)\s*kB", line or "")
    return round(int(m.group(1)) * 1024 / 2**30, 1) if m else None


# ---------------------------------------------------------------- (a) workloads


def workloads(root: Path) -> dict:
    out: dict = {}
    for meta_path in sorted(root.glob("*/meta.json")):
        folder = meta_path.parent
        if not (folder / "truth.jsonl.gz").exists():
            continue
        meta = read_json(meta_path)
        params = {x["name"]: x.get("params", {}) for x in read_json(folder / "layouts.json")}
        by_layout: dict[str, list[dict]] = defaultdict(list)
        for t in read_jsonl_gz(folder / "truth.jsonl.gz"):
            by_layout[t["layout"]].append(t)
        entry: dict = {"chunks": meta.get("n_chunks"), "questions_in_pool": meta.get("n_queries"), "layouts": {}}
        for name in ("w1-stats.json", "w2-stats.json"):
            if (folder / name).exists():
                entry[name] = read_json(folder / name)
        for name, rows in sorted(by_layout.items()):
            p = params.get(name, {})
            share_of = {t["user"]: t["sigma_g"] for t in rows}
            readable_of = {t["user"]: t["n_readable"] for t in rows}
            asked = Counter(t["q"] for t in rows)  # pairs per question: each user asks a question at most once
            item = {
                "share_target": p.get("share"), "correlation_target": p.get("correlation"),
                "achieved_share_mean_at_build": p.get("achieved_share_mean"),
                "pairs": len(rows), "users": len(share_of), "distinct_questions": len(asked),
                "users_per_question": stats(asked.values()),
                "sigma_g_per_user": stats(share_of.values()),
                "readable_chunks_per_user": stats(readable_of.values()),
                "rho_per_query": stats(t["rho"] for t in rows),
                "rho_undefined": sum(t["rho"] is None for t in rows),
                "sigma_l_per_query": stats(t["sigma_l"] for t in rows),
            }
            kinds = p.get("kinds") or {}
            if kinds:
                item["by_kind"] = {}
                for kind in sorted(set(kinds.values())):
                    chosen = [t for t in rows if kinds.get(f"{t['user']}|{t['q']}") == kind]
                    item["by_kind"][kind] = {"pairs": len(chosen), "rho_per_query": stats(t["rho"] for t in chosen),
                                             "sigma_l_per_query": stats(t["sigma_l"] for t in chosen)}
            entry["layouts"][name] = item
        out[meta["name"]] = entry
    return out


# ---------------------------------------------------------------- reading the raw outputs once


def needed(workload: str, store: str, arm: str, layout: str) -> bool:
    """Rows that some interval of H1 to H7 is computed from."""
    if workload == "w1_enron":
        return arm in W1_ARMS["H1"] + W1_ARMS["H2"]
    if workload != "w3":
        return False
    return ((arm in report.POST_FILTER and layout in H3_LAYOUTS) or arm == f"a4@{report.ALTERNATIVE.get(store)}"
            or (store == "pgvector" and arm in H7_ARMS))


def scan(results: Path) -> dict:
    """One pass over every job: load records, environment, memory, per-job latency percentiles, and the rows (c)
    needs, kept in the order bench.report reads them."""
    jobs: list[dict] = []
    loads: dict[tuple, list[dict]] = defaultdict(list)
    memory: dict[tuple, list[dict]] = defaultdict(list)
    latency: dict[tuple, dict] = defaultdict(lambda: {"p50": [], "p99": []})
    kept: dict[tuple, list[tuple]] = defaultdict(list)
    unscored: list[str] = []
    for meta_path in sorted(results.rglob("*.meta.json")):
        name = meta_path.name[: -len(".meta.json")]
        if name.startswith("pilot"):
            raise SystemExit(f"{meta_path} is a pilot; pilots are never reported")
        meta = read_json(meta_path)
        workload, store, kind = meta["workload"]["name"], meta["args"]["store"], job_kind(name)
        env = meta.get("environment", {})
        jobs.append({"job": name, "kind": kind, "workload": workload, "store": store, "cpus": env.get("cpus"),
                     "mem_total_gib": mem_total_gib(env.get("memory")), "runner": env.get("runner"),
                     "git_sha": env.get("git_sha"), "run_id": env.get("run_id"), "complete": meta.get("complete")})
        record = {"job": name, "kind": kind}
        for part, value in meta.get("load", {}).items():
            if isinstance(value, dict):
                record.update(flat(value, f"{part}."))
        loads[(workload, store)].append(record)
        if kind != "run":
            continue
        snapshot = {}
        for line in meta.get("docker_stats_after", []):
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            used = mem_bytes(str(d.get("MemUsage", "")).split("/")[0])
            if used is not None:
                snapshot[service(str(d.get("Name") or d.get("Container") or "?"))] = used
        if snapshot:
            memory[(workload, share_part(name), store)].append(snapshot)
        scored_path = meta_path.with_name(f"{name}.scored.jsonl.gz")
        if not scored_path.exists():
            unscored.append(name)
            continue
        per: dict[tuple, list[float]] = defaultdict(list)
        for r in read_jsonl_gz(scored_path):
            per[(r["arm"], r["layout"])].append(r["ms"])
            if needed(workload, store, r["arm"], r["layout"]):
                kept[(workload, store, r["arm"], r["layout"])].append(
                    (name, r["user"], r["q"], r.get("kind"), report.recall_of(r)))
        for (arm, layout), ms in per.items():
            cell = latency[(workload, store, arm, layout)]
            cell["p50"].append(float(np.percentile(ms, 50)))
            cell["p99"].append(float(np.percentile(ms, 99)))
        log(f"extras: read {name}")
    return {"jobs": jobs, "loads": loads, "memory": memory, "latency": latency, "kept": kept, "unscored": unscored}


# ---------------------------------------------------------------- (b) costs


def costs(scanned: dict, published_cells: list[dict]) -> dict:
    pub = {(c["workload"], c["store"], c["arm"], c["layout"]): c for c in published_cells}
    cells, worst, missing = [], 0.0, []
    for key, v in sorted(scanned["latency"].items()):
        p50, p99 = spread(v["p50"]), spread(v["p99"])
        c = pub.get(key)
        if c is None:
            missing.append(list(key))
        else:
            for field, mine in (("p50_ms", p50), ("p99_ms", p99)):
                for stat in ("median", "min", "max"):
                    worst = max(worst, abs(mine[stat] - c[field][stat]))
        cells.append({"workload": key[0], "store": key[1], "arm": key[2], "layout": key[3], "jobs": len(v["p99"]),
                      "p50_ms": p50, "p99_ms": p99})
    check = {"cells_here": len(cells), "cells_published": len(pub), "not_in_published": missing,
             "published_not_here": sorted(list(k) for k in set(pub) - set(scanned["latency"])),
             "max_abs_difference_ms": worst}

    builds = []
    for (workload, store), records in sorted(scanned["loads"].items()):
        keys = sorted({k for r in records for k in r if k not in ("job", "kind")})
        numeric = {k: spread(r.get(k) for r in records) for k in keys}
        text = {k: sorted({str(r[k]) for r in records if k in r and not isnum(r[k])}) for k in keys}
        builds.append({"workload": workload, "store": store, "jobs": len(records),
                       "kinds": dict(Counter(r["kind"] for r in records)),
                       "numeric": {k: v for k, v in numeric.items() if v},
                       "other_fields": sorted(k for k, v in text.items() if v and not numeric[k])})

    memory = []
    for (workload, part, store), snaps in sorted(scanned["memory"].items()):
        services = sorted({s for snap in snaps for s in snap})
        entry = {"workload": workload, "share": part or None, "store": store, "jobs": len(snaps),
                 "services_mib": {s: spread(snap[s] / MIB for snap in snaps if s in snap) for s in services},
                 "all_containers_mib": spread(sum(snap.values()) / MIB for snap in snaps)}
        memory.append(entry)

    env = scanned["jobs"]
    environment = {
        "jobs": dict(Counter(j["kind"] for j in env)),
        "cpus": dict(Counter(str(j["cpus"]) for j in env)),
        "mem_total_gib": dict(Counter(str(j["mem_total_gib"]) for j in env)),
        "distinct_runner_names": len({j["runner"] for j in env if j["runner"]}),
        "git_sha": dict(Counter(str(j["git_sha"]) for j in env)),
        "workflow_runs": dict(Counter(str(j["run_id"]) for j in env)),
        "incomplete_run_jobs": [j["job"] for j in env if j["kind"] == "run" and j["complete"] is not True],
        "run_jobs_without_scores": scanned["unscored"],
    }
    sized = sorted({b["store"] for b in builds if any(k.endswith("bytes") for k in b["numeric"])})
    timed = sorted({b["store"] for b in builds if "store.index_s" in b["numeric"]})
    return {"environment": environment, "latency_check": check, "latency": cells, "builds": builds,
            "memory_after_measured_pass": memory, "stores_reporting_a_size": sized,
            "stores_reporting_an_index_time": timed}


# ---------------------------------------------------------------- (c) sensitivity


def draw(rng: np.random.Generator, b: int, n: int) -> np.ndarray:
    """b bootstrap draws of n items with replacement, as counts per item: a (b, n) array."""
    idx = rng.integers(0, n, (b, n)) + (np.arange(b) * n)[:, None]
    return np.bincount(idx.ravel(), minlength=b * n).reshape(b, n).astype(float)


def matrix(entries: list[tuple], columns: dict) -> tuple[np.ndarray, np.ndarray]:
    """(user, question, value) triples as user x question sums and counts (jobs pooled)."""
    users = {u: i for i, u in enumerate(dict.fromkeys(u for u, _, _ in entries))}
    s = np.zeros((len(users), len(columns)))
    c = np.zeros_like(s)
    for u, q, v in entries:
        s[users[u], columns[q]] += v
        c[users[u], columns[q]] += 1
    return s, c


def estimate(s: np.ndarray, c: np.ndarray, wu: np.ndarray, wq: np.ndarray) -> np.ndarray:
    """bench.report's estimator, the mean over users of each user's mean, under user weights wu (b, U) and question
    weights wq (b, Q); with all weights 1 it is exactly the registered estimate."""
    num, den = wq @ s.T, wq @ c.T
    has = den > 0
    m = np.divide(num, den, out=np.zeros_like(num), where=has)
    w = wu * has
    total = w.sum(axis=1)
    return np.divide((w * m).sum(axis=1), total, out=np.full(len(total), np.nan), where=total > 0)


def bootstrap(samples: list[tuple], n_questions: int, scheme: str, rng: np.random.Generator, resamples: int,
              chunk: int = 500) -> np.ndarray:
    """(resamples, len(samples)) estimates. Samples share the question columns, so a drawn question counts in every
    sample at once; users are drawn for each sample on its own (the layouts of H3 have different users)."""
    out = np.empty((resamples, len(samples)))
    for start in range(0, resamples, chunk):
        b = min(chunk, resamples - start)
        wq = draw(rng, b, n_questions) if scheme != "users" else np.ones((b, n_questions))
        for j, (s, c) in enumerate(samples):
            wu = draw(rng, b, s.shape[0]) if scheme != "questions" else np.ones((b, s.shape[0]))
            out[start : start + b, j] = estimate(s, c, wu, wq)
    return out


def judge(h: str, lo: float, hi: float) -> str:
    """The registered rule of each hypothesis (bench.report)."""
    if not (isnum(lo) and isnum(hi)):
        return "not run"
    if h in ("H1", "H5"):
        return report.verdict_below(lo, hi, 0.5)
    if h == "H2":
        return report.verdict_below(lo, hi, 0.9)
    if h == "H3":
        return report.verdict_below(lo, hi, 0.0)
    if h == "H6":
        return "supported" if lo >= 0.9 else "not supported" if hi < 0.9 else "inconclusive"
    if h == "H7":
        return ("supported" if -0.02 < lo and hi < 0.02 else "not supported" if hi <= -0.02 or lo >= 0.02
                else "inconclusive")
    raise ValueError(h)


def entries_of(rows: list[tuple], kind: str | None = None) -> list[tuple]:
    """(user, question, recall) of rows with a recall (bench.report's recall_of: errors are 0, nothing readable is
    left out)."""
    return [(u, q, v) for _, u, q, k, v in rows if v is not None and (kind is None or k == kind)]


def columns_of(*lists: list[tuple]) -> dict:
    return {q: i for i, q in enumerate(sorted({q for entries in lists for _, q, _ in entries}))}


def part(h: str, key: tuple, lists: list[list[tuple]], resamples: int, seed: int) -> dict:
    """Point estimate and an interval under each scheme for one part; with two lists, the difference first - second."""
    if not lists or any(not x for x in lists):
        return {"estimate": None, **{s: {"interval": None, "verdict": "not run"} for s in SCHEMES}}
    columns = columns_of(*lists)
    samples = [matrix(x, columns) for x in lists]
    ones = [estimate(s, c, np.ones((1, s.shape[0])), np.ones((1, len(columns))))[0] for s, c in samples]
    out: dict = {"estimate": float(ones[0] - ones[1]) if len(ones) == 2 else float(ones[0]),
                 "n_users": [int(s.shape[0]) for s, _ in samples], "n_questions": len(columns),
                 "n_pairs": sum(int((c > 0).sum()) for _, c in samples)}
    for scheme in SCHEMES:
        draws = bootstrap(samples, len(columns), scheme, report.rng_for(seed, "extras", h, scheme, *key), resamples)
        stat = draws[:, 0] - draws[:, 1] if len(lists) == 2 else draws[:, 0]
        lo, hi = np.nanquantile(stat, [(1 - report.LEVEL) / 2, 1 - (1 - report.LEVEL) / 2])
        out[scheme] = {"interval": [float(lo), float(hi)], "verdict": judge(h, float(lo), float(hi)),
                       "failed_resamples": int(np.isnan(stat).sum())}
    return out


def plan(kept: dict) -> dict[str, list[tuple[tuple, list[list[tuple]]]]]:
    """For each hypothesis with an interval, its parts (in bench.report's order) and the rows of each."""
    parts: dict[str, list] = defaultdict(list)
    for h, arms in W1_ARMS.items():
        for store in report.STORES:
            for arm in arms:
                parts[h].append(((store, arm), [entries_of(kept[("w1_enron", store, arm, "w1_enron")], "own")]))
    for store in report.STORES:
        for share in report.SHARES[:3]:
            for arm in report.POST_FILTER:
                parts["H3"].append(((store, share, arm), [entries_of(kept[("w3", store, arm, f"w3_s{share}_{c}")])
                                                          for c in ("neg", "pos")]))
    for corr in report.CORRELATIONS:
        layout = f"w3_s0p01_{corr}"
        parts["H5"].append(((layout,), [entries_of(kept[("w3", "pgvector", "a4@default", layout)])]))
    for store in report.STORES:
        for layout in report.W3_LAYOUTS:
            parts["H6"].append(((store, layout), [entries_of(kept[("w3", store, f"a4@{report.ALTERNATIVE[store]}",
                                                                   layout)])]))
    for setting in report.SETTINGS["pgvector"]:
        for layout in report.W3_LAYOUTS:
            pair: dict[tuple, dict[str, float]] = defaultdict(dict)
            for arm in (f"a5-rls@{setting}", f"a4@{setting}"):
                for job, user, q, _, value in kept[("w3", "pgvector", arm, layout)]:
                    if value is not None:
                        pair[(job, user, q)][arm.split("@")[0]] = value
            diffs = [(user, q, v["a5-rls"] - v["a4"]) for (_, user, q), v in pair.items() if len(v) == 2]
            parts["H7"].append(((setting, layout), [diffs]))
    return parts


def sensitivity(kept: dict, registered: dict, resamples: int, seed: int) -> dict:
    out: dict = {"level": report.LEVEL, "resamples": resamples, "schemes": SCHEME_TEXT, "hypotheses": {}}
    for h, items in plan(kept).items():
        names = PART_KEYS[h]
        published = {tuple(p.get(n) for n in names): p for p in registered.get(h, {}).get("parts", [])}
        rows = []
        for key, lists in items:
            result = part(h, key, lists, resamples, seed)
            reg = published.get(key, {})
            result["registered"] = {"interval": reg.get("interval"), "verdict": reg.get("verdict", "not in report")}
            rows.append({**dict(zip(names, key)), **result})
            log(f"extras: {h} {key} done")
        combined = {s: report.combine([r[s]["verdict"] for r in rows]) for s in SCHEMES}
        changed = [r for r in rows if any(r[s]["verdict"] != r["registered"]["verdict"]
                                          for s in ("questions", "users_x_questions"))]
        check = [r for r in rows if r["users"]["verdict"] != r["registered"]["verdict"]]
        gaps = [abs(a - b) for r in rows if r["registered"]["interval"] and r["users"]["interval"]
                for a, b in zip(r["users"]["interval"], r["registered"]["interval"]) if isnum(a) and isnum(b)]
        widths = {}
        for s in ("questions", "users_x_questions"):
            ratios = []
            for r in rows:
                reg, mine = r["registered"]["interval"], r[s]["interval"]
                if reg and mine and all(isnum(x) for x in (*reg, *mine)) and reg[1] - reg[0] > 0:
                    ratios.append((mine[1] - mine[0]) / (reg[1] - reg[0]))
            widths[s] = stats(ratios)
        out["hypotheses"][h] = {
            "registered": registered.get(h, {}).get("verdict"), "combined": combined, "parts": rows,
            "parts_changed": len(changed), "users_scheme_differs_from_registered": len(check),
            "users_scheme_max_endpoint_gap": max(gaps) if gaps else None, "width_ratio_to_registered": widths,
        }
    for h in ("H4", "H8"):
        out["hypotheses"][h] = {
            "registered": registered.get(h, {}).get("verdict"),
            "combined": {s: registered.get(h, {}).get("verdict") for s in SCHEMES},
            "note": "judged on counts and medians, not on an interval, so no resampling scheme changes it",
        }
    out["verdict_changes"] = [
        {"hypothesis": h, "scheme": s, "registered": v["registered"], "now": v["combined"][s]}
        for h, v in out["hypotheses"].items() for s in ("questions", "users_x_questions")
        if v["combined"][s] != v["registered"]]
    out["hypotheses"] = {h: out["hypotheses"][h] for h in HYPOTHESES if h in out["hypotheses"]}
    return out


# ---------------------------------------------------------------- the rebuilt report


def walk(a: object, b: object, path: str, diffs: list[str], worst: list[float]) -> None:
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b), key=str):
            if k not in a or k not in b:
                diffs.append(f"{path}.{k}: in one only")
            else:
                walk(a[k], b[k], f"{path}.{k}", diffs, worst)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            diffs.append(f"{path}: {len(a)} items against {len(b)}")
        for i, (x, y) in enumerate(zip(a, b)):
            walk(x, y, f"{path}[{i}]", diffs, worst)
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        if not (math.isnan(a) and math.isnan(b)) and a != b:
            diffs.append(f"{path}: {a!r} against {b!r}")
            worst[0] = max(worst[0], abs(a - b))
    elif a != b:
        diffs.append(f"{path}: {a!r} against {b!r}")


def compare_reports(published: Path, rebuilt: Path) -> dict:
    out = {}
    for name in ("cells.json", "hypotheses.json", "faults.json", "churn.json", "coverage.json", "harness.json"):
        if not (published / name).exists() or not (rebuilt / name).exists():
            out[name] = {"compared": False}
            continue
        diffs: list[str] = []
        worst = [0.0]
        walk(read_json(published / name), read_json(rebuilt / name), name, diffs, worst)
        out[name] = {"compared": True, "identical": not diffs, "differences": len(diffs), "first": diffs[:20],
                     "max_abs_numeric_difference": worst[0]}
    return out


# ---------------------------------------------------------------- markdown


def md_workloads(a: dict) -> str:
    out = ["# (a) Workloads: achieved readable shares and query-permission correlation", "",
           "Source: each workload release's `truth.jsonl.gz` (the exact answers `bench.truth` wrote when the data were "
           "built), `layouts.json` and stats file. Definitions as in `bench/truth.py`: sigma_g is the share of the "
           "corpus a user may read; sigma_l is the share of the question's 2,048 nearest chunks, ignoring permissions, "
           "that the user may read (`bench.truth`'s default `--nn`, which the prepare workflows use); "
           "rho_q = (r - 1) / (r + 1) with r = sigma_l / sigma_g: 0 when readable chunks are as common near the "
           "question as in the whole corpus, above 0 when they are more common, below 0 when rarer (from -1 up to, "
           "not including, 1).", ""]
    w3 = a.get("w3")
    if w3:
        out += ["## W3, the controlled sweep", "",
                f"{w3['chunks']:,} chunks; questions drawn from a pool of {w3['questions_in_pool']}. Shares are "
                "per user (each user's sigma_g); rho_q is per (user, question) pair.", "",
                "| layout | target share | correlation | achieved share, mean over users (min to max) | "
                "rho_q mean | rho_q median (p25 to p75) | sigma_l mean | users per question, mean (max) |",
                "|---|---|---|---|---|---|---|---|"]
        for name, x in w3["layouts"].items():
            g, r, sl, upq = (x[k] or {} for k in ("sigma_g_per_user", "rho_per_query", "sigma_l_per_query",
                                                  "users_per_question"))
            out.append(f"| {name} | {x['share_target']} | {x['correlation_target']} | "
                       f"{fmt(g.get('mean'), 4)} ({fmt(g.get('min'), 4)} to {fmt(g.get('max'), 4)}) | "
                       f"{fmt(r.get('mean'))} | {fmt(r.get('median'))} ({fmt(r.get('p25'))} to {fmt(r.get('p75'))}) | "
                       f"{fmt(sl.get('mean'), 4)} | {fmt(upq.get('mean'), 2)} ({fmt(upq.get('max'), 0)}) |")
        undefined = [f"{n} {x['rho_undefined']}" for n, x in w3["layouts"].items() if x["rho_undefined"]]
        out += ["", "The mean achieved share recorded when the layouts were built (`achieved_share_mean` in "
                "`layouts.json`) is beside each layout in `workloads.json`. Pairs with an undefined rho_q (the user "
                "may read nothing): " + (", ".join(undefined) if undefined else "none") + ".", ""]
    w2 = {k: v for k, v in a.items() if k.startswith("w2_")}
    if w2:
        out += ["## W2, HoneyBee's role-based workloads, rebuilt from the paper's text", "",
                "| workload | HoneyBee Table 1, average access selectivity (as quoted in `bench/w2.py`) | readable share "
                "over all 1,000 users, mean (min, median, max) | the 100 measured users, mean (min to max) | "
                "rho_q mean (median) | users per question, mean (max) |", "|---|---|---|---|---|---|"]
        for name, x in sorted(w2.items()):
            st = x.get("w2-stats.json", {})
            quart = st.get("readable_share_quartiles") or [None] * 5
            (layout,) = x["layouts"].values()
            g, r, upq = (layout[k] or {} for k in ("sigma_g_per_user", "rho_per_query", "users_per_question"))
            out.append(f"| {name} | {st.get('honeybee_table1_avg_access_selectivity', 'n/a')} | "
                       f"{fmt(st.get('readable_share_mean'), 4)} ({fmt(quart[0], 4)}, {fmt(quart[2], 4)}, "
                       f"{fmt(quart[4], 4)}) | {fmt(g.get('mean'), 4)} ({fmt(g.get('min'), 4)} to "
                       f"{fmt(g.get('max'), 4)}) | {fmt(r.get('mean'))} ({fmt(r.get('median'))}) | "
                       f"{fmt(upq.get('mean'), 2)} ({fmt(upq.get('max'), 0)}) |")
        out.append("")
    w1 = a.get("w1_enron")
    if w1:
        (layout,) = w1["layouts"].values()
        g, n = layout["sigma_g_per_user"] or {}, layout["readable_chunks_per_user"] or {}
        out += ["## W1, Enron", "",
                f"{w1['chunks']:,} messages; {layout['users']} users; {layout['pairs']:,} (user, question) pairs over "
                f"{layout['distinct_questions']:,} distinct questions. Readable share per user: mean "
                f"{fmt(g.get('mean'), 4)} ({fmt(g.get('min'), 4)} to {fmt(g.get('max'), 4)}); readable messages per "
                f"user: median {fmt(n.get('median'), 0)} ({fmt(n.get('min'), 0)} to {fmt(n.get('max'), 0)}).", "",
                "| question kind | pairs | rho_q mean | rho_q median (p25 to p75) | sigma_l mean |", "|---|---|---|---|---|"]
        for kind, x in layout.get("by_kind", {}).items():
            r, sl = x["rho_per_query"] or {}, x["sigma_l_per_query"] or {}
            out.append(f"| {kind} | {x['pairs']:,} | {fmt(r.get('mean'))} | {fmt(r.get('median'))} "
                       f"({fmt(r.get('p25'))} to {fmt(r.get('p75'))}) | {fmt(sl.get('mean'), 4)} |")
        out.append("")
    return "\n".join(out)


def md_costs(b: dict) -> str:
    env, chk = b["environment"], b["latency_check"]
    out = ["# (b) Costs the measured jobs recorded", "",
           "Source: `results-raw.tar.gz`: each job's `.meta.json` (load records, environment, and on run jobs one "
           "`docker stats` snapshot after the measured pass) and `.scored.jsonl.gz` (every query's latency). Values are "
           "the median over jobs, with the range in brackets when the jobs differ.", "",
           "## Jobs and runners", "",
           f"- Jobs by kind: {', '.join(f'{k} {v}' for k, v in sorted(env['jobs'].items()))}.",
           f"- CPUs a job saw (`os.cpu_count()`): {', '.join(f'{k} in {v} jobs' for k, v in env['cpus'].items())}.",
           "- Memory a job saw (MemTotal, GiB): "
           f"{', '.join(f'{k} in {v} jobs' for k, v in env['mem_total_gib'].items())}.",
           f"- Distinct runner names: {env['distinct_runner_names']}; harness commit: "
           f"{', '.join(f'{k} ({v} jobs)' for k, v in env['git_sha'].items())}; workflow runs: "
           f"{', '.join(f'{k} ({v} jobs)' for k, v in env['workflow_runs'].items())}.",
           f"- Run jobs that did not finish: {len(env['incomplete_run_jobs'])}; run jobs without scores: "
           f"{len(env['run_jobs_without_scores'])}.", "",
           "## What was recorded, and what was not", "",
           f"- Latency: every query's wall time, embedding excluded. p50 and p99 per job and cell, recomputed here from "
           f"the raw rows as `bench.report` computes them: {chk['cells_here']} cells against "
           f"{chk['cells_published']} in the published `cells.json`, largest difference in any median, minimum or "
           f"maximum {chk['max_abs_difference_ms']:.6f} ms.",
           "- Memory: one `docker stats` snapshot per run job, after the measured pass. It is not a peak, it is not "
           "split by arm or setting (every arm and setting of a cell runs in the same job), and change and fault jobs "
           "record none.",
           f"- Size: stores that reported one: {', '.join(b['stores_reporting_a_size']) or 'none'}. pgvector's record "
           "is the table, its inner-product HNSW index and its GIN index (`bench/stores/pgvector.py`), and on W1 and "
           "W2 the partitions' total size; the cosine HNSW index built for A7 and the engines' PostgreSQL were not "
           "measured. The other stores recorded counts only (below).",
           f"- Build time: every store recorded `load_s`; stores that also recorded a separate index time: "
           f"{', '.join(b['stores_reporting_an_index_time']) or 'none'}. What each covers, from the code: pgvector "
           "`load_s` is the COPY and `index_s` the inner-product HNSW build only (the GIN and cosine indexes are built "
           "after it, untimed); Qdrant `index_s` runs from the end of the upload until the collection is green with "
           "every point counted; Milvus `index_s` runs from the flush until the index covers every row and the "
           "collection is loaded; Weaviate recorded the import only; OpenSearch `load_s` is the bulk import and a "
           "refresh, and `dls_s` the creation of the document-level-security roles and users.",
           "- Not recorded at all: peak memory, the CPU model, throughput (one client, as registered), and any cost of "
           "a permission change.", ""]

    out += ["## Build: load, index and engine times (s)", "",
            "| workload | store | jobs | store load_s | store index_s | SpiceDB load_s | OpenFGA load_s |",
            "|---|---|---|---|---|---|---|"]
    for x in b["builds"]:
        n = x["numeric"]
        out.append(f"| {x['workload']} | {x['store']} | {x['jobs']} | {fmt_spread(n.get('store.load_s'))} | "
                   f"{fmt_spread(n.get('store.index_s'))} | {fmt_spread(n.get('spicedb.load_s'))} | "
                   f"{fmt_spread(n.get('openfga.load_s'))} |")
    out += ["", "## Sizes pgvector reported (MiB)", "",
            "| workload | jobs | table | inner-product HNSW | GIN on principals |", "|---|---|---|---|---|"]
    for x in b["builds"]:
        n = x["numeric"]
        if "store.table_bytes" in n:
            out.append(f"| {x['workload']} | {x['jobs']} | {fmt_spread(n['store.table_bytes'], 1, MIB)} | "
                       f"{fmt_spread(n.get('store.hnsw_bytes'), 1, MIB)} | {fmt_spread(n.get('store.gin_bytes'), 1, MIB)} |")
    parts = [x for x in b["builds"] if "partitions.partitions" in x["numeric"]]
    if parts:
        out += ["", "## Partitions of A6 (pgvector, W1 and W2)", "",
                "| workload | jobs | partitions | rows | copies (rows per chunk) | size MiB | build s |",
                "|---|---|---|---|---|---|---|"]
        for x in parts:
            n = x["numeric"]
            out.append(f"| {x['workload']} | {x['jobs']} | {fmt_spread(n['partitions.partitions'], 0)} | "
                       f"{fmt_spread(n.get('partitions.rows'), 0)} | {fmt_spread(n.get('partitions.copies'), 2)} | "
                       f"{fmt_spread(n.get('partitions.bytes'), 1, MIB)} | {fmt_spread(n.get('partitions.build_s'))} |")
    out += ["", "## Other numbers the stores recorded at load", "", "| workload | store | field | value |",
            "|---|---|---|---|"]
    shown = {"store.load_s", "store.index_s", "store.table_bytes", "store.hnsw_bytes", "store.gin_bytes"}
    for x in b["builds"]:
        for k, v in x["numeric"].items():
            if k.startswith("store.") and k not in shown:
                out.append(f"| {x['workload']} | {x['store']} | `{k[6:]}` | {fmt_spread(v, 1)} |")
    out += ["", "## Container memory after the measured pass (MiB)", "",
            "| workload | share | store | jobs | store container | SpiceDB | OpenFGA | engines' PostgreSQL | all "
            "containers |", "|---|---|---|---|---|---|---|---|---|"]
    for x in b["memory_after_measured_pass"]:
        s = x["services_mib"]
        out.append(f"| {x['workload']} | {x['share'] or ''} | {x['store']} | {x['jobs']} | "
                   f"{fmt_spread(s.get(x['store']), 0)} | {fmt_spread(s.get('spicedb'), 0)} | "
                   f"{fmt_spread(s.get('openfga'), 0)} | {fmt_spread(s.get('authzdb'), 0)} | "
                   f"{fmt_spread(x['all_containers_mib'], 0)} |")
    lat = b["latency"]
    out += ["", "## p99 latency (ms)", "",
            "Each cell's p99 is computed per job; the tables give the median over its jobs (three seeds). The range over "
            "jobs and the p50 are in `costs.json`.", ""]
    for workload in sorted({c["workload"] for c in lat} - {"w3"}):
        cells = [c for c in lat if c["workload"] == workload]
        stores = [s for s in report.STORES if any(c["store"] == s for c in cells)]
        out += [f"### {workload}", "", "| arm | " + " | ".join(stores) + " |", "|---|" + "---|" * len(stores)]
        for arm in sorted({c["arm"] for c in cells}):
            row = []
            for s in stores:
                c = next((c for c in cells if c["arm"] == arm and c["store"] == s), None)
                row.append(fmt(c["p99_ms"]["median"], 1) if c else "")
            out.append(f"| {arm} | " + " | ".join(row) + " |")
        out.append("")
    w3 = [c for c in lat if c["workload"] == "w3"]
    if w3:
        out += ["### w3", "", "Per store, the median over the three correlation layouts of each cell's p99.", ""]
        for s in report.STORES:
            cells = [c for c in w3 if c["store"] == s]
            if not cells:
                continue
            out += [f"#### {s}", "", "| arm | " + " | ".join(report.SHARES) + " |",
                    "|---|" + "---|" * len(report.SHARES)]
            for arm in sorted({c["arm"] for c in cells}):
                row = []
                for share in report.SHARES:
                    v = [c["p99_ms"]["median"] for c in cells if c["arm"] == arm
                         and c["layout"].startswith(f"w3_s{share}_")]
                    row.append(fmt(float(np.median(v)), 1) if v else "")
                out.append(f"| {arm} | " + " | ".join(row) + " |")
            out.append("")
    return "\n".join(out)


def md_sensitivity(c: dict) -> str:
    out = ["# (c) Exploratory: the registered intervals when questions are resampled too", "",
           "**Exploratory. This is not the registered analysis and does not replace its verdicts.** The registered "
           "analysis (`bench.report`, pre-registration section 8) bootstraps users only. In W2 and W3 every user "
           "draws questions from one pool of 300 MS MARCO questions, so several users answer the same question, and "
           "in W1 some subjects are asked by more than one user (`workloads.md`, users per question). When recall "
           "depends on the question as well as on the user, an interval that resamples users alone can be too "
           "narrow. Here every interval of H1 to H8 is recomputed at the registered level "
           f"({100 * c['level']:.3f}%, {c['resamples']:,} resamples) under three schemes and judged by the "
           "registered rule; a hypothesis over several parts is combined by the registered intersection-union rule.",
           ""]
    out += [f"- `{k}`: {v}." for k, v in c["schemes"].items()]
    out += ["", "Every scheme uses `bench.report`'s estimator (each user's mean over their questions and jobs, then the "
            "mean over users; a failed query counts as 0). The `users` column is a check of this code: it should "
            "agree with the registered interval up to Monte Carlo error.", "",
            "## Verdicts", "",
            "| hypothesis | parts | registered | users (this code) | questions | users x questions | parts whose verdict "
            "differs from the registered one under a cluster scheme |", "|---|---|---|---|---|---|---|"]
    for h, v in c["hypotheses"].items():
        if "parts" in v:
            out.append(f"| {h} | {len(v['parts'])} | {v['registered']} | {v['combined']['users']} | "
                       f"{v['combined']['questions']} | {v['combined']['users_x_questions']} | {v['parts_changed']} |")
        else:
            out.append(f"| {h} | - | {v['registered']} | {v['registered']} | {v['registered']} | {v['registered']} | "
                       f"0 ({v['note']}) |")
    changes = c["verdict_changes"]
    out += ["", "Verdict changes: " + ("none: every hypothesis keeps its registered verdict under both cluster "
                                      "schemes." if not changes else
                                      "; ".join(f"{x['hypothesis']} under `{x['scheme']}`: {x['registered']} to "
                                                f"{x['now']}" for x in changes) + "."), ""]
    out += ["## Interval widths against the registered ones", "",
            "| hypothesis | users scheme: largest gap to a registered endpoint | parts where the users scheme's "
            "verdict differs from the registered one | width ratio, questions: median (max) | width ratio, users x "
            "questions: median (max) |", "|---|---|---|---|---|"]
    for h, v in c["hypotheses"].items():
        if "parts" not in v:
            continue
        wq, wb = v["width_ratio_to_registered"]["questions"], v["width_ratio_to_registered"]["users_x_questions"]
        out.append(f"| {h} | {fmt(v['users_scheme_max_endpoint_gap'], 4)} | "
                   f"{v['users_scheme_differs_from_registered']} | "
                   f"{fmt(wq['median'], 2) if wq else 'n/a'} ({fmt(wq['max'], 2) if wq else 'n/a'}) | "
                   f"{fmt(wb['median'], 2) if wb else 'n/a'} ({fmt(wb['max'], 2) if wb else 'n/a'}) |")
    out += ["", "A ratio is a part's interval width under the scheme over its registered width (parts with a registered "
            "width of 0 are left out).", ""]
    for h, v in c["hypotheses"].items():
        rows = [r for r in v.get("parts", []) if any(r[s]["verdict"] != r["registered"]["verdict"] for s in SCHEMES)]
        if not rows:
            continue
        names = PART_KEYS[h]
        out += [f"## {h}: parts whose verdict differs under some scheme", "",
                "| " + " | ".join(names) + " | estimate | registered | users | questions | users x questions |",
                "|" + "---|" * (len(names) + 5)]
        for r in rows:
            cells = []
            for s in ("registered", *SCHEMES):
                iv = r[s]["interval"]
                cells.append(f"[{fmt(iv[0])}, {fmt(iv[1])}] {r[s]['verdict']}" if iv else r[s]["verdict"])
            out.append("| " + " | ".join(str(r[n]) for n in names) + f" | {fmt(r['estimate'])} | " + " | ".join(cells)
                       + " |")
        out.append("")
    return "\n".join(out)


def md_index(meta: dict, a: dict, b: dict, c: dict, rebuilt: dict | None) -> str:
    where = (f"workflow run {meta['run_id']} of {meta['repository']} (`.github/workflows/extras.yml`)"
             if meta["run_id"] != "none" else "a run outside GitHub Actions")
    out = ["# Supplementary analyses of " + meta["release"], "",
           f"Made by `python -m bench.extras` in {where}. None of this is the registered analysis (`bench.report`). "
           "Parts (a) and (b) report what the pre-registration promised beside the hypotheses; part (c) is "
           "exploratory.", "",
           f"- Release: `{meta['release']}`; its `SHA256SUMS` (checked before use):"]
    out += [f"  - `{line}`" for line in meta["checksums"]]
    out += [f"- Code: commit `{meta['git_sha']}`.",
            f"- Bootstrap: {c['resamples']:,} resamples, seed {meta['seed']}.", "",
            "| file | what it holds |", "|---|---|",
            "| `workloads.md`, `workloads.json` | (a) achieved readable share per user and per-query correlation rho_q "
            "per W3 layout; W2 readable shares beside HoneyBee's Table 1; W1 by question kind |",
            "| `costs.md`, `costs.json` | (b) p50 and p99 latency per cell and job, container memory after the measured "
            "pass, sizes, load and index times, partitions, runners, and what was not recorded |",
            "| `sensitivity.md`, `sensitivity.json` | (c) exploratory: H1 to H8 with questions resampled as clusters |",
            "| `rebuild.json` | the report rebuilt from `results-raw.tar.gz` compared with the published one |", ""]
    if rebuilt is not None:
        same = [n for n, v in rebuilt.items() if v.get("identical")]
        differ = [n for n, v in rebuilt.items() if v.get("compared") and not v.get("identical")]
        out += ["## The report rebuilt from the raw outputs", "",
                f"`bench.report` run on `results-raw.tar.gz` gave files identical to the published report: "
                f"{', '.join(same) or 'none'}; files that differ: {', '.join(differ) or 'none'}"
                + (" (details in `rebuild.json`)." if differ else "."), ""]
    w3 = a.get("w3", {}).get("layouts", {})
    out += ["## (a) in brief", ""]
    ratios = [x["sigma_g_per_user"]["mean"] / x["share_target"] for x in w3.values()
              if x["share_target"] and x["sigma_g_per_user"]]
    if ratios:
        by_corr = []
        for corr in ("neg", "none", "pos"):
            means = [x["rho_per_query"]["mean"] for x in w3.values()
                     if x["correlation_target"] == corr and x["rho_per_query"]]
            if means:
                by_corr.append(f"{corr} {fmt(float(np.mean(means)))} (layouts from {fmt(min(means))} to "
                               f"{fmt(max(means))})")
        out.append(f"- W3: the mean achieved share was {min(ratios):.2f} to {max(ratios):.2f} times the target share "
                   f"across the {len(ratios)} layouts (folders are granted whole until the share is reached). Mean "
                   f"rho_q by target correlation: {'; '.join(by_corr)}.")
    w2 = {k: v for k, v in a.items() if k.startswith("w2_")}
    if w2:
        out.append("- W2 mean readable share over all 1,000 users (HoneyBee's Table 1 value): " + "; ".join(
            f"{k} {fmt(v.get('w2-stats.json', {}).get('readable_share_mean'), 4)} "
            f"({v.get('w2-stats.json', {}).get('honeybee_table1_avg_access_selectivity', 'n/a')})"
            for k, v in sorted(w2.items())) + ".")
    out += ["", "## (b) in brief", "",
            f"- p99 latency is available for all {b['latency_check']['cells_here']} cells; the per-job p50 and p99 "
            f"recomputed from the raw rows differ from the published `cells.json` by at most "
            f"{b['latency_check']['max_abs_difference_ms']:.6f} ms.",
            f"- Sizes were reported by: {', '.join(b['stores_reporting_a_size']) or 'no store'}; a separate index time "
            f"by: {', '.join(b['stores_reporting_an_index_time']) or 'no store'}. Memory is one snapshot after the "
            "measured pass of each run job.", "", "## (c) in brief (exploratory)", ""]
    for h, v in c["hypotheses"].items():
        out.append(f"- {h}: registered {v['registered']}; questions as clusters {v['combined']['questions']}; users "
                   f"crossed with questions {v['combined']['users_x_questions']}"
                   + (f"; {v['parts_changed']} of {len(v['parts'])} parts change verdict under a cluster scheme"
                      if "parts" in v else " (no interval)") + ".")
    out += ["", "Verdict changes under a cluster scheme: " + (
        "none." if not c["verdict_changes"] else
        "; ".join(f"{x['hypothesis']} ({x['scheme']}): {x['registered']} to {x['now']}" for x in c["verdict_changes"])
        + "."), ""]
    return "\n".join(out)


# ---------------------------------------------------------------- main


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--results", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--workloads", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--rebuilt", type=Path, default=None)
    p.add_argument("--resamples", type=int, default=10_000)
    p.add_argument("--seed", type=int, default=5)
    p.add_argument("--release", default="results-v1")
    p.add_argument("--checksums", type=Path, default=None)
    args = p.parse_args()

    meta = {"release": args.release, "seed": args.seed, "git_sha": os.environ.get("GITHUB_SHA", "local"),
            "run_id": os.environ.get("GITHUB_RUN_ID", "none"), "repository": os.environ.get("GITHUB_REPOSITORY", "-"),
            "checksums": args.checksums.read_text(encoding="utf-8").split("\n") if args.checksums else []}
    meta["checksums"] = [line for line in meta["checksums"] if line.strip()]
    a = workloads(args.workloads)
    scanned = scan(args.results)
    b = costs(scanned, read_json(args.report / "cells.json"))
    c = sensitivity(scanned["kept"], read_json(args.report / "hypotheses.json"), args.resamples, args.seed)
    rebuilt = compare_reports(args.report, args.rebuilt) if args.rebuilt else None

    args.out.mkdir(parents=True, exist_ok=True)
    label = {"made_by": "bench.extras", "registered_analysis": False, **meta}
    write_json(args.out / "workloads.json", {**label, "workloads": a})
    write_json(args.out / "costs.json", {**label, **b})
    write_json(args.out / "sensitivity.json", {**label, "exploratory": True, **c})
    if rebuilt is not None:
        write_json(args.out / "rebuild.json", {**label, "files": rebuilt})
    (args.out / "workloads.md").write_text(md_workloads(a) + "\n", encoding="utf-8")
    (args.out / "costs.md").write_text(md_costs(b) + "\n", encoding="utf-8")
    (args.out / "sensitivity.md").write_text(md_sensitivity(c) + "\n", encoding="utf-8")
    (args.out / "README.md").write_text(md_index(meta, a, b, c, rebuilt) + "\n", encoding="utf-8")
    print(json.dumps({"verdict_changes": c["verdict_changes"],
                      "rebuilt_identical": None if rebuilt is None else {k: v.get("identical") for k, v in rebuilt.items()},
                      "latency_check": {k: v for k, v in b["latency_check"].items() if k != "not_in_published"}},
                     indent=1))


if __name__ == "__main__":
    main()
