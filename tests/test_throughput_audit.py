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
