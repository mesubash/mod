import pytest

from pipeline.extract_od import MARKERS, PDF_PATH, build_long, extract

MODES = [m for m, _ in MARKERS]


@pytest.fixture(scope="module")
def mats():
    return extract(PDF_PATH)


@pytest.fixture(scope="module")
def od(mats):
    return build_long(mats)


def test_person_ground_truth(mats):
    m = mats["person_all"]["matrix"]
    for o, d, v in [(101, 101, 10442), (101, 102, 1527), (102, 101, 1872),
                    (103, 103, 58079), (105, 105, 68536)]:
        assert m.loc[o, d] == v


def test_vehicle_spot_checks(mats):
    # hand-read from pdftotext -layout output, incl. external zone 900 and a
    # printed-zero diagonal
    checks = {
        "motorcycle": [(101, 101, 2205), (118, 117, 12324), (900, 101, 70), (101, 900, 70)],
        "car": [(101, 101, 584), (105, 106, 2132), (105, 105, 0)],
        "truck": [(101, 101, 158), (103, 105, 1106)],
        "bus": [(101, 101, 57), (103, 105, 3107)],
    }
    for mode, cells in checks.items():
        for o, d, v in cells:
            assert mats[mode]["matrix"].loc[o, d] == v, (mode, o, d)


def test_printed_totals(mats):
    for mode in MODES:
        m = mats[mode]
        gap = m["col_totals"] - m["matrix"].sum()
        if mode == "person_all":
            # source discrepancy: printed column totals include an unprinted
            # external (901) origin row worth 3,636 trips
            assert (gap >= 0).all()
            assert gap.sum() == m["grand_total"] - m["row_totals"].sum() == 3636
        else:
            assert (gap == 0).all(), mode
            assert m["row_totals"].sum() == m["grand_total"], mode
    assert mats["person_all"]["grand_total"] == 3438393


def test_long_shape(od):
    assert list(od.columns) == ["origin_zone", "dest_zone", "mode", "trips"]
    assert len(od) == 5 * 50 * 50
    assert set(od["mode"]) == set(MODES)
    for _, g in od.groupby("mode"):
        assert g.pivot(index="origin_zone", columns="dest_zone", values="trips").shape == (50, 50)
    assert not od[["origin_zone", "dest_zone"]].isin([900, 901]).any().any()


def test_long_matches_matrices(od, mats):
    p = od[od["mode"] == "person_all"].set_index(["origin_zone", "dest_zone"])["trips"]
    assert p[(101, 101)] == 10442
    assert p[(104, 109)] == 0  # zero cells preserved, not dropped
    zones = mats["person_all"]["matrix"].index
    for mode in MODES:
        expected = mats[mode]["matrix"].loc[zones, zones].to_numpy().sum()
        assert od.loc[od["mode"] == mode, "trips"].sum() == expected, mode
