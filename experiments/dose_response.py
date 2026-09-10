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
        d = df[df.scenario == scenario]
        if extra is not None:
            d = d[extra(d)]
        d = d.dropna(subset=[col, "delta_pct_D_net_veh_h"])
        x = d[col].to_numpy() * 100
        y = d["delta_pct_D_net_veh_h"].to_numpy()
        b, lo, hi, r2, p = slope(x, y)
        print(f"{name:<13} {b:+7.3f}  [{lo:+7.3f}, {hi:+7.3f}]     {r2:6.3f} {p:10.2e}")
        rows.append((name, len(d), b, lo, hi, r2, p))

    print()
    print("Effect at each grid point, against no change (one-sample t):")
    print(f"{'lever':<13} {'share':>6} {'n':>4} {'mean':>9} {'sem':>7} {'t':>8} {'p':>10}")
    print("-" * 62)
    for name, (scenario, col, extra) in LEVERS.items():
        d = df[df.scenario == scenario]
        if extra is not None:
            d = d[extra(d)]
        for share, grp in d.dropna(subset=[col]).groupby(col):
            y = grp["delta_pct_D_net_veh_h"].dropna().to_numpy()
            if len(y) < 2 or np.allclose(y, 0):
                continue
            t, p = stats.ttest_1samp(y, 0.0)
            print(f"{name:<13} {share*100:5.0f}% {len(y):4d} {y.mean():+9.2f} "
                  f"{y.std(ddof=1)/np.sqrt(len(y)):7.2f} {t:8.2f} {p:10.2e}")


if __name__ == "__main__":
    main()
