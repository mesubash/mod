"""Collect sweep run metrics into one CSV for analysis.

Walks results/sweep/<scenario>/<run_id>/metrics.json, flattens the spec §7
metrics, parses the scenario parameters back out of each run_id, and writes a
tidy table with deltas against the baseline run.

Run: uv run python -m experiments.collect --results results/sweep \
        --out results/sweep/summary.csv
"""

import argparse
import json
import re
from pathlib import Path

import pandas as pd

PARAM = re.compile(r"(p_r|pt|dt|sch|bcap|m)(-?[\d.]+)")


def flatten(metrics, prefix=""):
    """Nested metrics dict -> flat columns; per-junction values become
    <metric>_<junction> so every intersection is comparable across runs."""
    out = {}
    for key, value in metrics.items():
        name = f"{prefix}{key}"
        if isinstance(value, dict):
            out.update(flatten(value, f"{name}_"))
        elif isinstance(value, (int, float, str)):
            out[name] = value
    return out


def parse_run_id(run_id):
    params = {name: float(value) for name, value in PARAM.findall(run_id)}
    if seed := re.search(r"seed(\d+)", run_id):
        params["seed"] = int(seed.group(1))
    return params


def collect(results_dir):
    rows = []
    for metrics_file in sorted(Path(results_dir).glob("*/*/metrics.json")):
        run_id = metrics_file.parent.name
        rows.append(
            {
                "scenario": metrics_file.parent.parent.name,
                "run_id": run_id,
                **parse_run_id(run_id),
                **flatten(json.loads(metrics_file.read_text())),
            }
        )
    if not rows:
        raise SystemExit(f"no metrics.json found under {results_dir}")
    return pd.DataFrame(rows)


def add_deltas(df):
    """Percent change against the baseline run for every numeric metric."""
    base = df[df["scenario"] == "baseline"]
    if base.empty:
        return df
    reference = base.iloc[0]
    scenario_params = {"scenario", "run_id", "seed", "pt", "dt", "sch",
                       "bcap", "m", "p_r"}
    metrics = [
        c for c in df.columns
        if c not in scenario_params
        and pd.api.types.is_numeric_dtype(df[c])
        and pd.api.types.is_number(reference.get(c))
    ]
    for column in metrics:
        if reference[column]:
            df[f"delta_pct_{column}"] = (
                (df[column] - reference[column]) / reference[column] * 100
            )
    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default="results/sweep")
    ap.add_argument("--out", default="results/sweep/summary.csv")
    args = ap.parse_args()

    df = add_deltas(collect(args.results))
    df.to_csv(args.out, index=False)
    print(f"{args.out}: {len(df)} runs, {len(df.columns)} columns")
    print(df.groupby("scenario").size().to_string())


if __name__ == "__main__":
    main()
