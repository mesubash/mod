import pytest

from experiments import transforms
from pipeline.common import REPO

_ANY_NET = REPO / "sim/net/corridor-calibrated.net.xml"
from experiments.transforms import PEAK, mode_shift, retime, s1_school_shift


def trip(i, depart, vtype="motorcycle", frm="a", to="b"):
    return {"id": f"{vtype}.{i}", "type": vtype, "depart": f"{depart:.2f}",
            "from": frm, "to": to, "departLane": "best"}


def fixture():
    peak = [trip(i, 32400 + 100 * i) for i in range(20)]
    off = [trip(100 + i, 25200 + 100 * i, "car") for i in range(10)]
    return peak + off


def test_retime_moves_exact_share_and_conserves():
    trips = fixture()
    before = [dict(t) for t in trips]
    out = retime(trips, 0.25, -15, seed=7)
    assert trips == before  # pure: input untouched
    assert len(out) == len(trips)
    assert [t["id"] for t in out] == [t["id"] for t in trips]
    moved = [(a, b) for a, b in zip(trips, out) if a != b]
    assert len(moved) == 5  # round(0.25 * 20 peak trips), exact
    for a, b in moved:
        assert PEAK[0] <= float(a["depart"]) < PEAK[1]
        assert float(b["depart"]) == float(a["depart"]) - 900
        assert {k: v for k, v in a.items() if k != "depart"} == \
               {k: v for k, v in b.items() if k != "depart"}


def test_retime_empty_and_zero_share():
    assert retime([], 0.25, -15, seed=1) == []
    trips = fixture()
    assert retime(trips, 0.0, -30, seed=1) == trips


def test_seed_reproducibility():
    trips = fixture()
    a = retime(trips, 0.25, -15, seed=7)
    assert a == retime(trips, 0.25, -15, seed=7)
    assert a != retime(trips, 0.25, -15, seed=8)  # deterministic, fixed seeds
    b, s = mode_shift(trips, 0.5, seed=7)
    b2, s2 = mode_shift(trips, 0.5, seed=7)
    assert b == b2 and s == s2


def test_mode_shift_bus_creation_and_accounting():
    trips = [trip(i, 29000 + 10 * i) for i in range(15)] + \
            [trip(99, 29000, "car")]
    out, s = mode_shift(trips, 1.0, seed=1)
    assert s == {"candidates": 15, "selected": 15, "converted": 15,
                 "clipped": 0, "passengers_moved": 16.5, "buses_added": 1,
                 "residual_passengers": 1.5}
    assert sum(t["type"] == "motorcycle" for t in out) == 0
    buses = [t for t in out if t["type"] == "bus"]
    assert len(buses) == 1
    assert (buses[0]["from"], buses[0]["to"]) == ("a", "b")
    # bus departs with the trip that completes 15 pax: 14th (13 * 1.1 < 15)
    assert float(buses[0]["depart"]) == 29000 + 10 * 13
    assert [t for t in out if t["type"] == "car"] == [trip(99, 29000, "car")]


def test_mode_shift_buses_per_od():
    # 14 pax-worth on each of two ODs: no OD reaches 15, so no bus anywhere
    trips = [trip(i, 29000 + i, frm="a") for i in range(13)] + \
            [trip(50 + i, 29000 + i, frm="c") for i in range(13)]
    out, s = mode_shift(trips, 1.0, seed=1)
    assert s["converted"] == 26 and s["buses_added"] == 0
    assert s["residual_passengers"] == pytest.approx(26 * 1.1)


def test_mode_shift_bcap_clips_per_hour():
    # 5 candidates in hour 08 and 5 in hour 09; cap 2.5 pax/h -> 2 each
    trips = [trip(i, 28800 + 60 * i) for i in range(5)] + \
            [trip(10 + i, 32400 + 60 * i) for i in range(5)]
    out, s = mode_shift(trips, 1.0, b_cap=2.5, seed=3)
    assert s["converted"] == 4 and s["clipped"] == 6
    assert s["passengers_moved"] == 4.4
    assert s["buses_added"] == 0
    assert sum(t["type"] == "motorcycle" for t in out) == 6


def test_mode_shift_window_and_type_filter():
    trips = [trip(0, 27000), trip(1, 40000), trip(2, 30000, "car"),
             trip(3, 30000)]
    out, s = mode_shift(trips, 1.0, seed=1)  # analysis window 28800-39600
    assert s["candidates"] == 1 and s["converted"] == 1
    assert sorted(t["id"] for t in out) == ["car.2", "motorcycle.0",
                                            "motorcycle.1"]


def test_s1_touches_only_peak_window():
    trips = fixture()
    out = s1_school_shift(trips, 0.5, seed=5)
    changed = [(a, b) for a, b in zip(trips, out) if a != b]
    assert len(changed) == 10  # round(0.5 * 20 peak trips)
    for a, b in changed:
        assert PEAK[0] <= float(a["depart"]) < PEAK[1]
        assert float(b["depart"]) == float(a["depart"]) - 3600
    assert out[20:] == trips[20:]  # off-peak identical


def test_s1_requires_sized_share():
    with pytest.raises(ValueError, match="A1"):
        s1_school_shift(fixture(), seed=1)


def test_route_file_round_trip(tmp_path):
    # Count-matched demand (routeSampler) is a <vehicle>+<route> file, not
    # <trip>s. Routes must survive transforms untouched while departs move.
    src = tmp_path / "v.rou.xml"
    src.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<routes>\n'
        '    <vType id="motorcycle" vClass="motorcycle" length="2.2"/>\n'
        '    <vehicle id="m1" depart="32500.0" type="motorcycle">'
        '<route edges="a b c"/></vehicle>\n'
        '    <vehicle id="c1" depart="30000.0" type="car">'
        '<route edges="f g"/></vehicle>\n</routes>'
    )
    vtypes, trips = transforms.read_trips(src)
    assert [t["route"] for t in trips] == ["a b c", "f g"]

    out = tmp_path / "out.rou.xml"
    transforms.write_trips(
        out, vtypes, transforms.retime(trips, p_t=1.0, dt_minutes=-30, seed=1), "t"
    )
    _, back = transforms.read_trips(out)
    by_id = {t["id"]: t for t in back}
    assert by_id["m1"]["route"] == "a b c"
    assert float(by_id["m1"]["depart"]) == 32500.0 - 1800   # in peak, shifted
    assert float(by_id["c1"]["depart"]) == 30000.0          # outside peak, kept


def test_reroute_preserves_trips_and_reports_no_alternative(tmp_path):
    # S0: diverted vehicles keep origin/destination and depart time; only the
    # path changes. Trips with no alternative stay put and are counted, since
    # "no alternative exists" is the finding the scenario tests.
    trips = [
        {"id": "a", "depart": "32500.0", "type": "car", "route": "e1 e2 e3"},
        {"id": "b", "depart": "32600.0", "type": "car", "route": "e1 e2 e3"},
        {"id": "outside", "depart": "20000.0", "type": "car", "route": "e1 e2 e3"},
    ]
    calls = {"n": 0}

    def fake_alternative(net, edges):      # every other trip has an alternative
        calls["n"] += 1
        return ["e1", "x9", "e3"] if calls["n"] % 2 else None

    original = transforms._alternative
    transforms._alternative = fake_alternative
    try:
        out, summary = transforms.reroute(trips, 1.0, seed=1, net_path=_ANY_NET)
    finally:
        transforms._alternative = original

    assert len(out) == len(trips)
    assert summary["selected"] == 2                      # peak-window trips only
    assert summary["diverted"] + summary["no_alternative"] == 2
    outside = next(t for t in out if t["id"] == "outside")
    assert outside["route"] == "e1 e2 e3"                 # untouched
    for before, after in zip(trips, out):
        assert before["depart"] == after["depart"]        # departs never move


def test_mode_shift_on_route_carrying_demand():
    # The count-matched demand has no from/to attributes — OD comes from the
    # route's first and last edge. This crashed the s3-joint sweep scenario.
    trips = [
        {"id": f"m{i}", "depart": f"{30000 + i}.0", "type": "motorcycle",
         "route": "origin mid dest"}
        for i in range(20)
    ]
    out, summary = transforms.mode_shift(trips, m=1.0, seed=3)
    assert summary["converted"] == 20
    buses = [t for t in out if t["type"] == "bus"]
    assert buses, "expected at least one added bus"
    assert all("route" in b for b in buses), "added buses must carry a route"
