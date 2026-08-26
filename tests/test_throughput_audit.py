"""The audit that showed the baseline delivers 6.6% of counted flow at 09:00."""

import pytest

from pipeline import throughput_audit
from pipeline.common import REPO


def test_targets_read_the_entered_attribute(tmp_path):
    # count_targets.xml stores volumes in `entered`, not `count`; reading the
    # wrong attribute returned zero targets and a silent 0.0% everywhere.
    f = tmp_path / "t.xml"
    f.write_text('<data><interval begin="25200" end="28800">'
                 '<edge id="a" entered="100"/><edge id="b" entered="50"/>'
                 '</interval></data>')
    assert throughput_audit.targets(f) == {("a", 25200): 100.0, ("b", 25200): 50.0}


def test_audit_ratio_matches_the_reported_collapse():
    if not throughput_audit.TARGETS.exists():
        pytest.skip("count_targets.xml not built")
    results = REPO / "results/sweep/baseline/baseline"
    if not (results / "edgedata_car.xml").exists():
        pytest.skip("baseline run outputs not present")
    rows = throughput_audit.audit(results)
    assert rows, "no counted hours found"
    assert all(0.0 <= r <= 2.0 for _, _, _, r in rows)
    # The collapse is the finding: delivery must fall across the morning.
    assert rows[0][3] > rows[-1][3]


def test_demand_gives_an_od_pair_more_than_one_route():
    # The baseline gridlocked because duarouter ran once on free-flow weights:
    # all 51,612 OD pairs had exactly one route, 5% of edges carried 45.5% of
    # traversals, and the busiest was asked to move 6,258 veh/h. Nothing pinned
    # route diversity, so the concentration was invisible until the network was
    # audited hour by hour.
    import collections
    import xml.etree.ElementTree as ET

    demand = REPO / "sim/demand/sampled_sorted.rou.xml"
    if not demand.exists():
        pytest.skip("count-matched demand not built")

    routes = collections.defaultdict(set)
    for _, el in ET.iterparse(demand, events=("end",)):
        if el.tag == "vehicle":
            r = el.find("route")
            if r is not None:
                edges = r.get("edges").split()
                routes[(edges[0], edges[-1])].add(r.get("edges"))
            el.clear()

    assert routes, "no embedded routes in the demand"
    multi = sum(1 for v in routes.values() if len(v) > 1)
    assert multi / len(routes) > 0.05, (
        f"only {multi}/{len(routes)} OD pairs have more than one route: "
        "the demand routes every vehicle down the same path")


def test_scenarios_run_inside_the_stable_regime():
    # The network carries about 44,000 veh/h through the cordon and collapses
    # above it: at full counted demand the peak hour delivered 9,710 vehicles,
    # at half demand 44,094. Every M4 result before this ran in the collapse,
    # where a delay change reflects the gridlock spiral rather than the
    # intervention. The sweep's default loading must stay inside the ceiling.
    import re

    sweep = (REPO / "experiments/sweep.sh").read_text()
    m = re.search(r"^SCALE=\$\{SCALE:-([\d.]+)\}", sweep, re.M)
    assert m, "sweep.sh must set a default demand loading"
    assert 0.5 <= float(m.group(1)) <= 0.55, (
        "loading must stay in the band that is congested but does not collapse "
        "inside the analysis window: 0.6 and above gridlock by 10:00, and 0.5 "
        "is nearly free-flowing (D_net 3,054 veh-h against 7,577 at 0.55)")
