import pandas as pd
import pytest

from pipeline.growth import growth_factors, load


def synth(values, start_year=2011):
    years = range(start_year, start_year + len(values))
    return pd.DataFrame({
        "station_no": 1,
        "location": "X",
        "road_link": "R",
        "aadt_pcu": values,
        "fiscal_year": [f"{y}/{(y + 1) % 100:02d}" for y in years],
        "year": years,
    })


@pytest.fixture(scope="module")
def real():
    return growth_factors(load()).set_index("station_no")


def test_flagged_jump_station_58(real):
    row = real.loc[58]
    # 2011/12 (aadt_pcu 4348 -> 16313, ratio 3.75) is a count-method break
    assert row["year_start"] == "2012/13"
    assert row["year_end"] == "2024/25"
    assert row["years_used"] == 9
    assert row["years_flagged"] == 1
    assert row["cagr"] == pytest.approx((27821 / 16313) ** (1 / 12) - 1)


def test_clean_series_station_53(real):
    row = real.loc[53]
    assert row["years_used"] == 10
    assert row["years_flagged"] == 0
    assert (row["year_start"], row["year_end"]) == ("2011/12", "2024/25")
    assert row["cagr"] == pytest.approx(0.06842, abs=1e-5)


def test_too_few_clean_years():
    out = growth_factors(synth([100, 1000, 100]))  # every transition implausible
    row = out.iloc[0]
    assert len(out) == 1
    assert pd.isna(row["cagr"]) and pd.isna(row["year_start"])
    assert row["years_used"] == 1
    assert row["years_flagged"] == 2


def test_tie_prefers_recent_run():
    # runs of length 1, 3, 3 -> the later 3-run (2015/16..2017/18) must win
    out = growth_factors(synth([100, 1000, 1500, 1000, 9000, 9000, 9000]))
    row = out.iloc[0]
    assert (row["year_start"], row["year_end"]) == ("2015/16", "2017/18")
    assert row["years_used"] == 3


def test_gap_annualization():
    # 2x over a 2-year survey gap annualizes to 1.41x/yr -> clean, kept
    out = growth_factors(pd.DataFrame({
        "station_no": 1, "location": "X", "road_link": "R",
        "aadt_pcu": [100, 200],
        "fiscal_year": ["2011/12", "2013/14"],
        "year": [2011, 2013],
    }))
    assert out.iloc[0]["cagr"] == pytest.approx(2 ** 0.5 - 1)
