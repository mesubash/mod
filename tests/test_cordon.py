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


def test_a1_matches_measured_profile():
    # A1 is the measured DoR profile (pipeline/dor_hourly.py), not an assumed
    # peak: every hour within 0.005 of the pooled station-day mean, morning
    # rising monotonically to the 09:00 peak, no hour above 10% of daily.
    measured = {6: 0.038, 7: 0.047, 8: 0.055, 9: 0.068, 10: 0.067, 11: 0.064}
    assert set(HOURLY_SHARE) == set(range(6, 12))
    for hour, share in measured.items():
        assert abs(HOURLY_SHARE[hour] - share) < 0.005
    assert HOURLY_SHARE[6] < HOURLY_SHARE[7] < HOURLY_SHARE[8] < HOURLY_SHARE[9]
    assert max(HOURLY_SHARE.values()) < 0.10


def test_vtype_geometry_is_physical():
    # A12: lengths are real vehicle dimensions, not PCU-space bookkeeping —
    # encoding PCU as length gave buses 24.7 m and starved arterial capacity.
    # PCU stays a separate accounting weight, so the two must NOT agree.
    physical = {"motorcycle": 2.2, "car": 4.3, "bus": 12.0, "truck": 10.0}
    for mode, length in physical.items():
        assert VTYPES[mode]["length"] == length
        assert VTYPES[mode]["length"] + VTYPES[mode]["minGap"] <= 15.0
    assert VTYPES["bus"]["length"] != pytest.approx(PCU["bus"] * CAR_SPACE)


def test_vtype_forced_gap_behaviour():
    # A12: Kathmandu's manually-metered junctions flow because drivers force
    # gaps; motorcycles most aggressive, heavy vehicles least.
    probs = {m: VTYPES[m]["jmIgnoreFoeProb"] for m in VTYPES}
    assert probs["motorcycle"] > probs["car"] > probs["bus"]
    assert all(0 < p < 0.5 for p in probs.values())
    assert VTYPES["motorcycle"]["tau"] < VTYPES["bus"]["tau"]


def test_vtype_motorcycle_sublane_params():
    # A11: filtering behavior; minGapLat inside the thesis calibrated
    # standing range 0.2-0.41 m (Table 4-25)
    m = VTYPES["motorcycle"]
    assert m["latAlignment"] == "compact"
    assert 0.2 <= m["minGapLat"] <= 0.41
    # only motorcycle overrides laterals; others ride SUMO defaults
    assert all("minGapLat" not in VTYPES[k] for k in ("car", "bus", "truck"))


def test_slice_conserves_total():
    for daily in (0, 1, 2, 37, 1234.56):
        bins = slice_bins(daily)
        assert len(bins) == 24
        assert min(bins) >= 0
        assert sum(bins) == math.floor(daily * WINDOW_SHARE + 1e-9)


def test_slice_follows_measured_profile():
    # The measured profile is a broad plateau, not a spike: 09:00 is the
    # morning maximum but 08:00-11:00 sit within 20% of it (contrast with the
    # superseded trip-generation assumption, which put 09:00 at 2x its
    # neighbours). Guards against reintroducing an assumed peak.
    bins = slice_bins(4000)
    hours = [sum(bins[i:i + 4]) for i in range(0, 24, 4)]
    assert hours[3] == max(hours)  # 09:00-10:00
    for adjacent in (hours[2], hours[4], hours[5]):
        assert adjacent > 0.8 * hours[3]


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
