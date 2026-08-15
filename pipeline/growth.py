"""Per-station traffic growth factors (CAGR on aadt_pcu) from DoR SSRN AADT counts."""

import pandas as pd

from pipeline.common import REPO

CSV_IN = REPO / "research/library/data-dor-ssrn-aadt-kathmandu-valley-stations.csv"
CSV_OUT = REPO / "data/processed/growth_factors.csv"

# Count-method changes produce implausible jumps (station 58: aadt_pcu 4348 ->
# 16313 in one year). A transition is plausible only if its per-year growth
# ratio, annualized across survey gaps, stays inside these bounds; CAGR is then
# computed over the longest clean run of surveys (most recent run wins ties).
# ponytail: fixed 0.5-2.0 band tuned by eye on these 29 stations; upgrade path:
# changepoint detection if new stations misclassify.
RATIO_LO, RATIO_HI = 0.5, 2.0
MIN_RUN = 2  # CAGR needs two points

OUT_COLS = ["station_no", "location", "road_link", "year_start", "year_end",
            "aadt_pcu_start", "aadt_pcu_end", "cagr", "years_used", "years_flagged"]


def load(path=CSV_IN):
    df = pd.read_csv(path, skipinitialspace=True)
    df.columns = df.columns.str.strip()
    text = df.select_dtypes(exclude="number").columns
    df[text] = df[text].apply(lambda c: c.str.strip())
    df["year"] = df["fiscal_year"].str[:4].astype(int)
    return df


def _longest_clean_run(years, values):
    """(start, stop) positional slice of the longest clean run."""
    ok = [
        RATIO_LO <= (values[i + 1] / values[i]) ** (1 / (years[i + 1] - years[i])) <= RATIO_HI
        for i in range(len(values) - 1)
    ]
    best, start = (0, 0), 0
    for i, good in enumerate(ok + [False]):
        if not good:
            if i - start + 1 >= best[0]:  # >= keeps the most recent run on ties
                best = (i - start + 1, start)
            start = i + 1
    return best[1], best[1] + best[0]


def growth_factors(df):
    rows = []
    for _, g in df.groupby("station_no", sort=True):
        g = g.sort_values("year")
        years = g["year"].to_numpy()
        vals = g["aadt_pcu"].to_numpy(dtype=float)
        s, e = _longest_clean_run(years, vals)
        n = e - s
        row = {
            "station_no": g["station_no"].iloc[0],
            "location": g["location"].iloc[0],
            "road_link": g["road_link"].iloc[0],
            "years_used": n,
            "years_flagged": len(g) - n,
        }
        if n >= MIN_RUN:
            row |= {
                "year_start": g["fiscal_year"].iloc[s],
                "year_end": g["fiscal_year"].iloc[e - 1],
                "aadt_pcu_start": int(vals[s]),
                "aadt_pcu_end": int(vals[e - 1]),
                "cagr": (vals[e - 1] / vals[s]) ** (1 / (years[e - 1] - years[s])) - 1,
            }
        rows.append(row)
    return pd.DataFrame(rows, columns=OUT_COLS)


if __name__ == "__main__":
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    growth_factors(load()).to_csv(CSV_OUT, index=False)
