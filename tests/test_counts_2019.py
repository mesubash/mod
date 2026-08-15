import pytest

from pipeline.counts_2019 import extract


@pytest.fixture(scope="module")
def df():
    return extract()


def val(df, intersection, leg, direction, metric):
    rows = df[
        (df["intersection"] == intersection)
        & (df["leg"] == leg)
        & (df["direction"] == direction)
        & (df["metric"] == metric)
    ]
    return rows["value"].item()  # .item() also asserts exactly one row


def test_known_values(df):
    assert val(df, "Koteshwor", 1, "in", "pcu_24h") == 64543
    assert val(df, "Koteshwor", 1, "in", "observed_pcu") == 58675
    assert val(df, "Koteshwor", 1, "in", "hours_observed") == 15
    assert val(df, "Shahid Gate", 1, "out", "pcu_24h") == 81862
    assert val(df, "Maitighar", 1, "in", "pcu_24h") == 64413


def test_table_page_break(df):
    # New Baneshwor leg 3 straddles the A4-18/A4-19 page break
    assert val(df, "New Baneshwor", 3, "in", "pcu_24h") == 14564
    assert val(df, "New Baneshwor", 3, "out", "pcu_24h") == 15094
    # last data row of the table
    assert val(df, "Jadhibuti", 3, "out", "pcu_24h") == 64012


def test_direction_normalized(df):
    # source has one capitalized "Out" (Maitighar leg 5, one-way)
    assert set(df["direction"]) == {"in", "out"}
    assert val(df, "Maitighar", 5, "out", "observed_pcu") == 22233


def test_shape(df):
    assert len(df) == 231
    # 9 survey sites, Tinkune split into South/West/North sub-intersections
    assert df["intersection"].nunique() == 11
    assert df["value"].notna().all()
