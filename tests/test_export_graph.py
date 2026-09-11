"""The exported product graph keeps what routing needs (pipeline/export_graph.py)."""

import gzip
import json

import pytest

from pipeline.export_graph import NET, OUT, CLASSES


pytestmark = pytest.mark.skipif(
    not OUT.exists(), reason="run `uv run --with pyproj python -m pipeline.export_graph`")


def graph():
    with gzip.open(OUT, "rt", encoding="utf-8") as fh:
        return json.load(fh)


def test_exported_from_the_prefilter_build():
    # corridor-filtered and -calibrated are built with
    # --keep-edges.by-vclass passenger, which deletes every edge a car cannot
    # use. Exporting from either silently drops the motorcycle-only links.
    assert graph()["source"] == NET.name == "corridor.net.xml"


def test_motorcycles_reach_edges_cars_cannot():
    # The product's vehicle-class differentiator. If this asymmetry is zero the
    # graph came from a passenger-filtered build and the feature does not exist.
    edges = graph()["edges"]
    moto = {e["i"] for e in edges if "m" in e["c"]}
    car = {e["i"] for e in edges if "c" in e["c"]}
    assert len(moto - car) > 100, "no motorcycle-only links: wrong source network"


def test_every_edge_endpoint_has_coordinates():
    g = graph()
    nodes = g["nodes"]
    for e in g["edges"]:
        assert e["f"] in nodes and e["t"] in nodes, f"{e['i']} has a dangling endpoint"


def test_no_edge_without_a_routable_class():
    assert all(e["c"] for e in graph()["edges"])


def test_class_codes_round_trip():
    g = graph()
    assert set(g["classes"]) == set(CLASSES.values())
    assert set(g["classes"].values()) == set(CLASSES)
