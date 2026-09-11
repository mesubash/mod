"""Corridor road graph as portable JSON, for the routing product.

The product must not depend on SUMO or carry an 88 MB .net.xml. Routing needs
only the graph: nodes with coordinates, edges with length, speed, and which
vehicle classes may use them. That is a few MB, and it lets the product be
written in any language.

This is the one-way boundary between the research repo and the product repo:
the network is built and calibrated here, exported once, and consumed there as
a versioned artefact.

Run: uv run python -m pipeline.export_graph
"""

import gzip
import json

import sumolib

from pipeline.common import REPO

# The PRE-FILTER build, deliberately. corridor-filtered/-calibrated are built
# with --keep-edges.by-vclass passenger, which deletes every edge a car cannot
# use -- including the 488 motorcycle-only links that are the product's whole
# vehicle-class differentiator. The research needed that filter; routing does
# not. Width-derived lane counts (A14) are already in this build.
NET = REPO / "sim/net/corridor.net.xml"
OUT = REPO / "results/corridor-graph.json.gz"

# The classes the product routes for. SUMO knows ~30; carrying the rest would
# quadruple the file for classes no traveller selects.
CLASSES = {"motorcycle": "m", "passenger": "c", "bus": "b", "truck": "t"}


def edge_classes(edge):
    """Short codes for the product classes any lane of this edge allows."""
    allowed = set()
    for lane in edge.getLanes():
        perms = lane.getPermissions()
        allowed |= {code for vclass, code in CLASSES.items() if vclass in perms}
    return "".join(sorted(allowed))


def build(net_path=NET, out=OUT):
    net = sumolib.net.readNet(str(net_path))

    nodes = {}
    for node in net.getNodes():
        x, y = node.getCoord()
        lon, lat = net.convertXY2LonLat(x, y)
        nodes[node.getID()] = [round(lon, 6), round(lat, 6)]

    edges = []
    for edge in net.getEdges():
        cls = edge_classes(edge)
        if not cls:
            continue  # nothing the product routes can use it
        edges.append({
            "i": edge.getID(),
            "f": edge.getFromNode().getID(),
            "t": edge.getToNode().getID(),
            "l": round(edge.getLength(), 1),
            "s": round(edge.getSpeed(), 1),
            "n": edge.getLaneNumber(),
            "c": cls,
        })

    # Drop nodes no surviving edge touches, so the product does not carry
    # geometry for a graph it cannot route on.
    used = {e["f"] for e in edges} | {e["t"] for e in edges}
    nodes = {k: v for k, v in nodes.items() if k in used}

    graph = {
        "source": net_path.name,
        "classes": {code: vclass for vclass, code in CLASSES.items()},
        "nodes": nodes,
        "edges": edges,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(out, "wt", encoding="utf-8") as fh:
        json.dump(graph, fh, separators=(",", ":"))
    return graph, out


def main():
    graph, out = build()
    mb = out.stat().st_size / 1e6
    raw = len(json.dumps(graph)) / 1e6
    print(f"{out.relative_to(REPO)}  {len(graph['nodes']):,} nodes, "
          f"{len(graph['edges']):,} edges")
    print(f"  {mb:.1f} MB gzipped, {raw:.1f} MB raw")
    by_class = {}
    for e in graph["edges"]:
        for c in e["c"]:
            by_class[c] = by_class.get(c, 0) + 1
    names = graph["classes"]
    print("  edges per class: "
          + ", ".join(f"{names[c]} {n:,}" for c, n in sorted(by_class.items())))


if __name__ == "__main__":
    main()
