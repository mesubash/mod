"""Dose-response slopes and significance tests for the four levers.

The paper reported three or five grid points per lever with a standard error
each, and asserted monotonicity by inspection. A reviewer asked for inferential
treatment. This fits the effect against the share treated, which quantifies the
lever rather than tabulating it, and reports a test against no effect.

The seeds are the randomisation: each grid point is 24 independent
treatment assignments on one network and one demand. The slope is therefore
the response of this corridor to the share treated, not an estimate sampled
from a population of corridors, and is reported as such.

Run: uv run python -m experiments.dose_response
"""

import numpy as np
import pandas as pd
from scipy import stats

from pipeline.common import REPO

SUMMARY = REPO / "results/sweep/summary.csv"

# lever -> (scenario, share column, filter on the other transform axes)
LEVERS = {
    "Rerouting": ("s0-spatial-control", "p_r", None),
    "Mode shift": ("s3-joint", "m", lambda d: (d.pt == 0) & (d.dt == -15)),
    "Retiming": ("s2-retime-grid", "pt", lambda d: d.dt == -15),
    "School shift": ("s1-school", "sch", None),
}


def load():
    df = pd.read_csv(SUMMARY)
    return df[df.scenario != "baseline"].copy()


def treated(df, scenario, col, extra):
    """Rows for one lever, at non-zero doses only.

    The sweep writes an untreated row into the grid for the scenarios whose
    other axis is being varied (retiming at pt=0, mode shift at m=0). Those
    rows are not runs: every one carries the single baseline's D_net exactly,
    so they have zero variance. Including them in the fit would add 24 copies
    of one number at the origin for two levers and none for the other two,
    which is what the first version of this script did.
    """
    d = df[df.scenario == scenario]
    if extra is not None:
        d = d[extra(d)]
    d = d.dropna(subset=[col, "delta_pct_D_net_veh_h"])
    return d[d[col] > 0]


def assignment_sd(d, col):
    """Pooled standard deviation within a dose, across treatment assignments.

    This is the direct measure of how much *which* trips are treated matters.
    1 - R^2 is not: it also absorbs the width of the dose range, so a lever
    swept over a narrow range scores as noisy when it is not.
    """
    num = sum((len(g) - 1) * g["delta_pct_D_net_veh_h"].var(ddof=1)
              for _, g in d.groupby(col))
    den = sum(len(g) - 1 for _, g in d.groupby(col))
    return np.sqrt(num / den)


def slope(x, y):
    """OLS slope with a 95% interval, in delay-percent per percent treated."""
    res = stats.linregress(x, y)
    tcrit = stats.t.ppf(0.975, len(x) - 2)
    half = tcrit * res.stderr
    return res.slope, res.slope - half, res.slope + half, res.rvalue ** 2, res.pvalue


def main():
    df = load()
    print(f"{'lever':<13} {'slope (pp per 1% treated)':<28} {'R2':>6} {'p':>10}")
    print("-" * 62)
    rows = []
    for name, (scenario, col, extra) in LEVERS.items():
        d = treated(df, scenario, col, extra)
        x = d[col].to_numpy() * 100
        y = d["delta_pct_D_net_veh_h"].to_numpy()
        b, lo, hi, r2, p = slope(x, y)
        print(f"{name:<13} {b:+7.3f}  [{lo:+7.3f}, {hi:+7.3f}]     {r2:6.3f} {p:10.2e}")
        rows.append((name, len(d), b, lo, hi, r2, p))

    print()
    print("Spread across treatment assignments within a dose (pooled SD, pp):")
    for name, (scenario, col, extra) in LEVERS.items():
        d = treated(df, scenario, col, extra)
        print(f"  {name:<13} {assignment_sd(d, col):6.2f}")

    print()
    print("Effect at each grid point, against no change (one-sample t):")
    print(f"{'lever':<13} {'share':>6} {'n':>4} {'dD':>9} {'sem':>7} {'sd':>7} "
          f"{'dH':>8} {'t':>8} {'p':>10} {'p Holm':>10}")
    print("-" * 92)
    tests = []
    for name, (scenario, col, extra) in LEVERS.items():
        d = treated(df, scenario, col, extra)
        for share, grp in d.groupby(col):
            y = grp["delta_pct_D_net_veh_h"].dropna().to_numpy()
            if len(y) < 2:
                continue
            t, p = stats.ttest_1samp(y, 0.0)
            h = grp["delta_pct_H_cordon_pcu_0811"].dropna().to_numpy()
            tests.append([name, share, len(y), y.mean(),
                          y.std(ddof=1) / np.sqrt(len(y)), y.std(ddof=1),
                          h.mean() if len(h) else float("nan"), t, p])
    # Holm-Bonferroni across the whole family of grid-point tests.
    order = sorted(range(len(tests)), key=lambda i: tests[i][8])
    running = 0.0
    holm = [0.0] * len(tests)
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(tests) - rank) * tests[i][8]))
        holm[i] = running
    for row, ph in zip(tests, holm):
        name, share, n, mean, sem, sd, dh, t, p = row
        print(f"{name:<13} {share*100:5.0f}% {n:4d} {mean:+9.2f} {sem:7.2f} "
              f"{sd:7.2f} {dh:+8.2f} {t:8.2f} {p:10.2e} {ph:10.3f}")


if __name__ == "__main__":
    main()
