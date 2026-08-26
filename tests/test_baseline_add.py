"""Detector definitions derive from the junction map (pipeline/baseline_add.py)."""

import csv

from pipeline.baseline_add import JUNCTION_MAP, build
from pipeline.cordon import PCU


def test_every_mapped_cordon_edge_is_measured():
    # baseline.add.xml kept its own copy of the cordon edge list. Remapping one
    # counted edge updated junction_map.csv and left the detectors naming the
    # old id; SUMO refused the run with "Unknown edge '52916461' in edgeData
    # definition 'cnt_truck'".
    body, n = build()
    mapped = {r["edge_id"] for r in csv.DictReader(open(JUNCTION_MAP))}
    assert n == len(mapped)
    for edge in mapped:
        assert f'"{edge} ' in body or f' {edge} ' in body or f' {edge}"' in body, \
            f"{edge} is mapped but not measured"


def test_one_detector_per_vehicle_class_plus_the_network():
    body, _ = build()
    for vtype in PCU:
        assert f'id="cnt_{vtype}"' in body
        assert f'vTypes="{vtype}"' in body
    assert 'id="net_hourly"' in body


def test_the_generated_file_matches_what_is_committed():
    # The committed file is what SUMO actually reads; a drift means someone
    # edited it by hand again.
    from pipeline.baseline_add import OUT

    if not OUT.exists():
        return
    assert OUT.read_text() == build()[0], (
        "sim/baseline.add.xml differs from what junction_map.csv generates; "
        "run uv run python -m pipeline.baseline_add")
