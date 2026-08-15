import math
import re
import xml.etree.ElementTree as ET
from collections import Counter

import pytest

from pipeline.common import REPO
from pipeline.cordon import (CAR_SPACE, DEMAND, GROUP_POINTS, HOURLY_SHARE,
                             PCU, TAZ_FILE, VTYPES, ZONE_POINTS, slice_bins)

WINDOW_SHARE = sum(HOURLY_SHARE.values())


def _built(path):
    if not path.exists():
        pytest.skip(f"{path.name} not built (run pipeline.cordon)")


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


def test_taz_edge_counts_and_weights():
    _built(TAZ_FILE)
    tazs = {t.get("id"): t for t in ET.parse(TAZ_FILE).getroot().iter("taz")}
    assert set(tazs) == ({str(z) for z in ZONE_POINTS}
                         | {f"g{g}" for g in GROUP_POINTS})
    for tid, t in tazs.items():
        src, snk = t.findall("tazSource"), t.findall("tazSink")
        # many spawn edges per zone, never one (insertion-starvation guard)
        floor = 24 if tid.isdigit() else 12
        assert len(src) >= floor, tid
        assert len(snk) >= floor, tid
        assert all(float(e.get("weight")) > 0 for e in src + snk)


def test_trips_origin_spread_and_conservation():
    trips = DEMAND / "baseline.trips.xml"
    _built(trips)
    _built(REPO / "data/processed/corridor_od.parquet")
    pd = pytest.importorskip("pandas")
    cod = pd.read_parquet(REPO / "data/processed/corridor_od.parquet")
    expected = sum(sum(slice_bins(t)) for t in cod["trips"])
    pat = re.compile(r'<trip .*? from="([^"]+)" to="[^"]+" fromTaz=')
    origins = Counter()
    with open(trips) as f:
        for line in f:
            if m := pat.search(line):
                origins[m[1]] += 1
    total = sum(origins.values())
    assert total == expected  # every OD trip emitted, all carry taz attrs
    assert len(origins) >= 200
    assert max(origins.values()) / total < 0.03
