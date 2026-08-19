"""Sweep results -> the paper's result tables and figures.

Reads the tidy table written by experiments/collect.py and produces, for the
spec §7 metrics at the binding intersections:

  results/figures/lever_comparison.png    the headline: which lever works
  results/figures/retiming_response.png   delay vs share retimed, by shift size
  results/figures/pareto.png              network benefit vs individual cost
  results/figures/compliance.png          effect vs participation (RQ2)
  results/tables/scenarios.md             headline comparison, S0-S3
  results/tables/sensitivity.csv          full surface, tidy

Run: uv run python -m experiments.analyse [--summary results/sweep/summary.csv]
"""

import argparse
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402  (backend must precede pyplot)

# The junctions the paper argues are binding (spec §7, saturation degrees from
# JICA 2012 Table 6.2.12). Delay at these is the headline outcome.
BINDING = ["New Baneshwor", "Thapathali", "Kalimati", "Koteshwor", "Maitighar"]
INK = "#171717"
MUTED = "#666666"


def load(summary):
    df = pd.read_csv(summary)
    if "scenario" not in df:
        raise SystemExit(f"{summary} is not a sweep summary (no scenario column)")
    # Summaries collected before p_r joined the parameter regex carry it only
    # in the run id; recover it so S0 can be plotted alongside the other levers.
    if "p_r" not in df:
        df["p_r"] = df.run_id.str.extract(r"p_r([\d.]+)").astype(float)
    return df


def delay_column(df):
    """Mean delay across binding intersections, falling back to whatever
    per-junction delay columns the runs actually produced."""
    cols = [c for c in df.columns if c.startswith("d_i_s_per_veh_")]
    binding = [c for c in cols if any(b in c for b in BINDING)]
    use = binding or cols
    if not use:
        raise SystemExit("no per-junction delay columns found in summary")
    return df[use].mean(axis=1), use


def retiming_response(df, out):
    """RQ1: does delay fall superlinearly as more of the peak is retimed?"""
    d = df[df.scenario.str.startswith("s2")].copy()
    if d.empty:
        return None
    d["delay"], _ = delay_column(d)
    # Greyscale with distinct markers and dash patterns: thesis figures get
    # printed in black and white, and the series must stay separable there.
    styles = [(INK, "o", "-"), (MUTED, "s", "--"), ("#a3a3a3", "^", ":")]
    fig, ax = plt.subplots(figsize=(6, 4))
    for (dt, grp), (colour, marker, dash) in zip(d.groupby("dt"), styles):
        agg = grp.groupby("pt")["delay"].agg(["mean", "std"]).reset_index()
        ax.errorbar(agg.pt * 100, agg["mean"], yerr=agg["std"].fillna(0),
                    marker=marker, linestyle=dash, color=colour, capsize=3,
                    label=f"{abs(int(dt))} min earlier")
    ax.set_xlabel("peak demand retimed (%)")
    ax.set_ylabel("mean delay at binding intersections (s/veh)")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(out / "retiming_response.png", dpi=200)
    plt.close(fig)
    return d


def lever_comparison(df, out):
    """The headline result: which lever moves network delay, and how much.

    Mode shift is isolated at p_t = 0 and spatial redistribution at its own
    grid, so each curve is that lever acting alone."""
    fig, ax = plt.subplots(figsize=(6.5, 4))
    series = [
        ("mode shift (motorcycle to bus)",
         df[(df.scenario == "s3-joint") & (df.pt == 0) & (df.dt == -15)],
         "m", INK, "o", "-"),
        ("departure retiming",
         df[(df.scenario == "s2-retime-grid") & (df.dt == -15)],
         "pt", MUTED, "s", "--"),
        ("spatial redistribution",
         df[df.scenario == "s0-spatial-control"], "p_r", "#a3a3a3", "^", ":"),
    ]
    for label, d, xcol, colour, marker, dash in series:
        if d.empty or xcol not in d:
            continue
        d = d.sort_values(xcol)
        ax.plot(d[xcol] * 100, -d["delta_pct_D_net_veh_h"], marker=marker,
                linestyle=dash, color=colour, label=label)
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.set_xlabel("share of peak demand treated (%)")
    ax.set_ylabel("network delay reduction (%)")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(out / "lever_comparison.png", dpi=200)
    plt.close(fig)


def pareto(df, out):
    """Network benefit against the schedule cost imposed on retimed travellers.

    Retiming carries no route penalty, so individual cost is the shift itself:
    (share retimed) x (minutes earlier), in traveller-minutes per 100 trips."""
    d = df[df.scenario.str.startswith(("s2", "s3"))].copy()
    if d.empty or "delta_pct_D_net_veh_h" not in d:
        return
    d["delay"], _ = delay_column(d)
    d["cost"] = d.pt * d.dt.abs() * 100
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(d.cost, -d["delta_pct_D_net_veh_h"], c=INK, s=28, alpha=0.8)
    ax.set_xlabel("schedule cost (traveller-minutes per 100 trips)")
    ax.set_ylabel("network delay reduction (%)")
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(out / "pareto.png", dpi=200)
    plt.close(fig)


def compliance(df, out):
    """RQ2: the participation level at which the effect becomes measurable."""
    d = df[df.scenario.str.startswith("s2")].copy()
    if d.empty or "delta_pct_D_net_veh_h" not in d:
        return
    agg = d.groupby("pt")["delta_pct_D_net_veh_h"].agg(["mean", "std"]).reset_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(agg.pt * 100, -agg["mean"], marker="o", color=INK)
    if agg["std"].notna().any():
        ax.fill_between(agg.pt * 100,
                        -agg["mean"] - agg["std"].fillna(0),
                        -agg["mean"] + agg["std"].fillna(0),
                        color=MUTED, alpha=0.2)
    ax.set_xlabel("participation (% of peak demand retimed)")
    ax.set_ylabel("network delay reduction (%)")
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(out / "compliance.png", dpi=200)
    plt.close(fig)


def scenario_table(df, out):
    """Headline comparison: one row per scenario at its strongest setting."""
    rows = []
    for scenario, grp in df.groupby("scenario"):
        delay, used = delay_column(grp)
        grp = grp.assign(delay=delay)
        # rank on network delay, the study's primary outcome — intersection
        # delay alone can improve while the network as a whole degrades
        key = ("delta_pct_D_net_veh_h" if "delta_pct_D_net_veh_h" in grp
               else "delay")
        best = grp.loc[grp[key].idxmin()]
        rows.append({
            "scenario": scenario,
            "runs": len(grp),
            "best setting": best.get("run_id", ""),
            "delay (s/veh)": round(best.delay, 1),
            "delay vs baseline (%)": round(best.get("delta_pct_D_net_veh_h", float("nan")), 1),
            "throughput vs baseline (%)": round(
                best.get("delta_pct_H_cordon_pcu_0811", float("nan")), 1),
        })
    table = pd.DataFrame(rows)
    lines = ["# Scenario results", "",
             "Delay is the mean across binding intersections; deltas are against",
             "the unmodified baseline under identical model settings. Absolute",
             "levels are not calibrated (see paper §7) — read the deltas.", "",
             table.to_markdown(index=False), ""]
    (out / "scenarios.md").write_text("\n".join(lines))
    return table


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", default="results/sweep/summary.csv")
    args = ap.parse_args()

    df = load(args.summary)
    figures = Path("results/figures")
    tables = Path("results/tables")
    figures.mkdir(parents=True, exist_ok=True)
    tables.mkdir(parents=True, exist_ok=True)

    lever_comparison(df, figures)
    retiming_response(df, figures)
    pareto(df, figures)
    compliance(df, figures)
    table = scenario_table(df, tables)
    df.to_csv(tables / "sensitivity.csv", index=False)

    print(f"{len(df)} runs across {df.scenario.nunique()} scenarios")
    print(table.to_string(index=False))
    print(f"\nfigures -> {figures}/  tables -> {tables}/")


if __name__ == "__main__":
    main()
