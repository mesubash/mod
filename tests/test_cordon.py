import math

import pytest

from pipeline.cordon import CAR_SPACE, HOURLY_SHARE, PCU, VTYPES, slice_bins

WINDOW_SHARE = sum(HOURLY_SHARE.values())


def test_a1_anchors():
    # sourced anchors: 20% of daily in 09:00-10:00, adjacent hours < half that
    assert HOURLY_SHARE[9] == 0.20
    assert HOURLY_SHARE[8] < 0.10 and HOURLY_SHARE[10] < 0.10
    assert set(HOURLY_SHARE) == set(range(6, 12))


def test_vtype_space_matches_pcu():
    for mode, a in VTYPES.items():
        assert a["length"] + a["minGap"] == pytest.approx(PCU[mode] * CAR_SPACE)


def test_slice_conserves_total():
    for daily in (0, 1, 2, 37, 1234.56):
        bins = slice_bins(daily)
        assert len(bins) == 24
        assert min(bins) >= 0
        assert sum(bins) == math.floor(daily * WINDOW_SHARE + 1e-9)


def test_slice_peak_hour_dominates():
    bins = slice_bins(4000)
    hours = [sum(bins[i:i + 4]) for i in range(0, 24, 4)]
    assert hours[3] == max(hours)  # 09:00-10:00
    assert hours[2] * 2 < hours[3] + 4  # adjacent under half, rounding slack
