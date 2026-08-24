import pytest

from experiments import transforms
from pipeline.common import REPO

_ANY_NET = REPO / "sim/net/corridor-calibrated.net.xml"


def _needs_net():
    # The net is a rebuildable artifact and is gitignored; these tests stub the
    # path search but reroute still loads the net first.
    if not _ANY_NET.exists():
        pytest.skip("corridor-calibrated.net.xml not built (run experiments/sweep.sh)")
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
    _needs_net()
    calls = {"n": 0}

    def fake_alternative(net, edges, vclass="passenger"):
        # every other trip has an alternative
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


def test_reroute_searches_with_the_vehicles_own_class():
    # A path a car may legally take can be illegal for a bus, and SUMO rejects
    # the whole route file at load time ("no valid route"). Each search must
    # use the vehicle's own vClass.
    _needs_net()
    seen = []

    def fake_alternative(net, edges, vclass="passenger"):
        seen.append(vclass)
        return None

    trips = [{"id": "b", "depart": "33000.0", "type": "bus", "route": "a b c"},
             {"id": "m", "depart": "33001.0", "type": "motorcycle", "route": "a b c"}]
    original = transforms._alternative
    transforms._alternative = fake_alternative
    try:
        transforms.reroute(trips, 1.0, seed=1, net_path=_ANY_NET)
    finally:
        transforms._alternative = original
    assert sorted(seen) == ["bus", "motorcycle"]


def test_expand_does_not_sweep_string_lists():
    # closed_edges is a value, not a grid axis: expanding it passed the bare
    # string to the transform, set() split it into characters, and all 24 S4
    # runs silently returned the baseline.
    from experiments.run import expand

    combos = expand({"spread_reroute": {"closed_edges": ["e1", "e2"],
                                        "p_r": [0.1, 0.5]}})
    assert len(combos) == 2, "p_r sweeps, closed_edges does not"
    for _, tfs in combos:
        params = dict(tfs)["spread_reroute"]
        assert params["closed_edges"] == ["e1", "e2"]
        assert params["p_r"] in (0.1, 0.5)


def test_spread_reroute_exists_and_spreads_across_alternatives():
    # spread_reroute was silently lost in a refactor and S4 failed at run time;
    # this pins both its presence and the round-robin behaviour that is the
    # whole point of the scenario.
    trips = [{"id": f"v{i}", "depart": f"{33000 + i}.0", "type": "car",
              "route": "a closed b"} for i in range(6)]
    trips.append({"id": "untouched", "depart": "33100.0", "type": "car",
                  "route": "x y z"})

    def fake_alternatives(net, edges, closed, k, vclass="passenger"):
        return [["a", "alt1", "b"], ["a", "alt2", "b"]][:k]

    original_alts, original_net = transforms._alternatives, transforms._net
    transforms._alternatives = fake_alternatives
    transforms._net = lambda p=None: None
    try:
        out, summary = transforms.spread_reroute(
            trips, ["closed"], p_r=1.0, k_alternatives=2, seed=1)
    finally:
        transforms._alternatives, transforms._net = original_alts, original_net

    assert summary["affected"] == 6 and summary["rerouted"] == 6
    routes = {t["route"] for t in out if t["id"] != "untouched"}
    assert len(routes) == 2, "guided trips must be split across both options"
    assert next(t for t in out if t["id"] == "untouched")["route"] == "x y z"


def test_scenario_closure_block_generates_a_rerouter(tmp_path):
    # A closure has to be enforced in the network, or p_r=0 is ordinary traffic
    # rather than the uncoordinated disruption response it is meant to be.
    import tomllib

    from pipeline.disruption import closure

    cfg = tomllib.load(open(REPO / "experiments/scenarios/s4-closure.toml", "rb"))
    block = cfg["closure"]
    assert block["begin"] < block["end"], "closure window must be non-empty"
    assert block["edges"] == cfg["transforms"]["spread_reroute"]["closed_edges"], \
        "the enforced closure and the transform's closed_edges must agree"

    xml = closure(block["edges"], block["begin"], block["end"])
    for edge in block["edges"]:
        assert f'<closingReroute id="{edge}"/>' in xml
    assert f'begin="{block["begin"]}"' in xml


def test_closure_edge_is_a_real_corridor_link():
    # The first closure edge was a 0.2 m junction connector: enforcing it
    # changed nothing, and the enforced and unenforced grids came back
    # identical. A closure has to shut a length of road someone drives along.
    import tomllib

    import sumolib

    net_path = REPO / "sim/net/corridor-calibrated.net.xml"
    if not net_path.exists():
        pytest.skip("corridor-calibrated.net.xml not built")
    cfg = tomllib.load(open(REPO / "experiments/scenarios/s4-closure.toml", "rb"))
    net = sumolib.net.readNet(str(net_path))
    for edge_id in cfg["closure"]["edges"]:
        edge = net.getEdge(edge_id)
        assert edge.getLength() >= 100, \
            f"{edge_id} is {edge.getLength():.1f} m — too short to be a closure"
        assert edge.allows("passenger")


def test_closure_edge_is_used_by_the_demand():
    # Two closures in a row shut roads the demand never touches: a 0.2 m
    # junction connector, then a 991 m trunk link with zero routes through it.
    # Both produced 24 identical runs. Verify usage before spending compute.
    import tomllib

    demand = REPO / "sim/demand/sampled_sorted.rou.xml"
    if not demand.exists():
        pytest.skip("count-matched demand not built")
    cfg = tomllib.load(open(REPO / "experiments/scenarios/s4-closure.toml", "rb"))
    text = demand.read_text()
    for edge in cfg["closure"]["edges"]:
        assert text.count(f" {edge} ") + text.count(f'"{edge} ') > 1000, \
            f"{edge} carries too little demand to be a meaningful closure"


def test_only_unguided_vehicles_get_a_rerouting_device(tmp_path):
    # A global rerouting device re-plans guided vehicles too, overwriting the
    # spread routes and making k=1 and k=3 identical. Guided vehicles must
    # carry has.rerouting.device=0, un-guided affected ones 1.
    trips = [{"id": f"v{i}", "depart": f"{33000 + i}.0", "type": "car",
              "route": "a closed b"} for i in range(4)]

    def fake_alternatives(net, edges, closed, k, vclass="passenger"):
        return [["a", "alt1", "b"], ["a", "alt2", "b"]][:k]

    orig_alts, orig_net = transforms._alternatives, transforms._net
    transforms._alternatives = fake_alternatives
    transforms._net = lambda p=None: None
    try:
        out, summary = transforms.spread_reroute(
            trips, ["closed"], p_r=0.5, k_alternatives=2, seed=1)
    finally:
        transforms._alternatives, transforms._net = orig_alts, orig_net

    guided = [t for t in out if t.get("reroute") == "0"]
    unguided = [t for t in out if t.get("reroute") == "1"]
    assert len(guided) == summary["rerouted"] == 2
    assert len(unguided) == 2, "affected but un-guided vehicles re-plan reactively"

    path = tmp_path / "o.rou.xml"
    transforms.write_trips(path, [], out, "t")
    xml = path.read_text()
    assert '<param key="has.rerouting.device" value="1"/>' in xml
    assert '<param key="has.rerouting.device" value="0"/>' in xml
    assert "reroute=" not in xml, "the flag is a param, not an attribute"


def test_kappa_controls_how_many_unguided_drivers_can_reroute():
    # The first S4 grid gave every un-guided vehicle a rerouting device, so the
    # control group already had live travel times and an optimal recomputation.
    # kappa is the share that keeps it; the rest take the closure's on-arrival
    # diversion.
    trips = [{"id": f"v{i}", "depart": f"{33000 + i}.0", "type": "car",
              "route": "a closed b"} for i in range(10)]

    def fake_alternatives(net, edges, closed, k, vclass="passenger"):
        return [["a", "alt1", "b"]]

    orig_alts, orig_net = transforms._alternatives, transforms._net
    transforms._alternatives = fake_alternatives
    transforms._net = lambda p=None: None
    try:
        runs = {kappa: transforms.spread_reroute(
            trips, ["closed"], p_r=0.0, k_alternatives=1, seed=1, kappa=kappa)
            for kappa in (0.0, 0.5, 1.0)}
    finally:
        transforms._alternatives, transforms._net = orig_alts, orig_net

    for kappa, (out, summary) in runs.items():
        devices = [t for t in out if t.get("reroute") == "1"]
        assert len(devices) == summary["knowing"] == round(kappa * 10), \
            f"kappa={kappa} must give exactly that share a rerouting device"


def test_kappa_grid_closes_the_same_edge_as_the_main_s4_grid():
    # s4-kappa is s4-closure with the control relaxed, so it must shut the same
    # link — otherwise the two grids are not comparable and the closure-edge
    # checks above (length, permissions, demand usage) do not cover it.
    import tomllib

    main = tomllib.load(open(REPO / "experiments/scenarios/s4-closure.toml", "rb"))
    kappa = tomllib.load(open(REPO / "experiments/scenarios/s4-kappa.toml", "rb"))
    assert kappa["closure"] == main["closure"]
    assert (kappa["transforms"]["spread_reroute"]["closed_edges"]
            == kappa["closure"]["edges"])
