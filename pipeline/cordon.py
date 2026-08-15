"""Baseline corridor demand (spec §4-§5): growth-scale the 2011 vehicle OD,
cut the corridor sub-OD at the count cordon, time-slice 06:00-12:00, emit
SUMO trips and duarouter routes.

Inputs: data/processed/od_2011.parquet, data/processed/growth_factors.csv,
sim/net/corridor-filtered.net.xml, sim/net/junction_map.csv,
data/raw/corridor.osm.
Outputs: data/processed/corridor_od.parquet, sim/demand/zones.taz.xml,
sim/demand/baseline.trips.xml, sim/demand/baseline.rou.xml.

Run: uv run python -m pipeline.cordon
"""

import csv
import math
import random
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter
from itertools import accumulate
from pathlib import Path

import numpy as np
import pandas as pd
import sumolib

from pipeline.common import REPO

NET = REPO / "sim/net/corridor-filtered.net.xml"
OSM = REPO / "data/raw/corridor.osm"
JUNCTION_MAP = REPO / "sim/net/junction_map.csv"
OUT_OD = REPO / "data/processed/corridor_od.parquet"
DEMAND = REPO / "sim/demand"
TAZ_FILE = DEMAND / "zones.taz.xml"
DUAROUTER = REPO / ".venv/bin/duarouter"

# A3: growth from DoR SSRN station 64 (Manohara Bridge, road link H0303), the
# only valley station on the corridor's own road — Arniko Hwy at the Jadibuti
# end; all other stations sit on Ring Road or radials off the axis. Single
# corridor-wide factor = aadt_pcu_end/aadt_pcu_start over its clean
# 2011/12-2024/25 run (1.93x). Nearest Ring Road stations bracket it for M3
# sensitivity: 65 Sinamangal 1.54x, 60 RR-Manohara 1.12x.
GROWTH_STATION = 64

# A1: share of DAILY trips departing per clock hour. Sourced anchors
# [vol02 p.6-7, p.6-14]: 09:00-10:00 carries 20% of daily trips and each
# adjacent hour is under half the peak share (9% < 10%). The taper shape
# (9/6/3%) between the anchors is the registered A1 assumption.
HOURLY_SHARE = {6: 0.03, 7: 0.06, 8: 0.09, 9: 0.20, 10: 0.09, 11: 0.06}
ANALYSIS = (8 * 3600, 11 * 3600)  # spec §4 analysis window 08:00-11:00

# PCU-consistent space (spec §3): length + minGap = PCU x car space (4.3+2.5 m),
# car=1.0, motorcycle=0.3, bus=truck=4.0 (A4). Other params come from SUMO's
# per-vClass defaults.
# ponytail: 24.7 m bus/truck is queue-space bookkeeping, not geometry — swap
# for real dims + sublane model at M3 if junction dynamics misbehave.
CAR_SPACE = 4.3 + 2.5
VTYPES = {
    "motorcycle": {"vClass": "motorcycle", "length": 1.84, "minGap": 0.2},
    "car": {"vClass": "passenger", "length": 4.3, "minGap": 2.5},
    "bus": {"vClass": "bus", "length": 24.7, "minGap": 2.5},
    "truck": {"vClass": "truck", "length": 24.7, "minGap": 2.5},
}
PCU = {"motorcycle": 0.3, "car": 1.0, "bus": 4.0, "truck": 4.0}

# Corridor-zone centroids (lon, lat), placed by eye on the OSM extract from the
# spec §1 zone descriptions (A2).
# ponytail: replace with georeferenced zone-map centroids at M3 (A2 resolution).
ZONE_POINTS = {
    107: (85.338, 27.691),   # New/Old Baneshwor
    108: (85.317, 27.6945),  # Tripureshwor-Thapathali-Maitighar
    109: (85.303, 27.694),   # Teku
    110: (85.295, 27.700),   # Kalimati
    114: (85.310, 27.7055),  # city core (Asan/New Road)
    119: (85.346, 27.683),   # Tinkune-Koteshwor-Jadibuti (ward 35)
    301: (85.313, 27.686),   # Lalitpur across Bagmati (Kupondole/Sanepa)
    502: (85.358, 27.6715),  # Thimi side of Jadibuti (Lokanthali)
}
# External zones share one gate area per municipality group (spec §1 hundreds
# digit), anchored on the group's main approach artery inside the net bbox.
# ponytail: per-zone placement needs the georeferenced zone map; until then the
# group gates are the cordon generation/attraction nodes (spec §2).
GROUP_POINTS = {
    1: (85.317, 27.712),   # KMC north (Kamalpokhari/Lazimpat side)
    2: (85.281, 27.679),   # Kirtipur approach
    3: (85.324, 27.673),   # Patan center
    4: (85.372, 27.670),   # Bhaktapur, via Arniko Hwy east
    5: (85.365, 27.679),   # Thimi (501)
    6: (85.281, 27.694),   # Kathmandu Dist. rim, via Tribhuvan Hwy (Kalanki)
    7: (85.333, 27.658),   # Lalitpur Dist., via Satdobato south
    8: (85.372, 27.670),   # Bhaktapur Dist., same Arniko gate as 4xx
}
CENTER = (85.335, 27.688)  # New Baneshwor; anchors inbound/outbound edge choice
MAJOR = ("motorway", "trunk", "primary", "secondary", "tertiary")

# TAZ demand injection. One edge per zone starved insertion (21,288/234,760
# vehicles entered the 6h baseline run; top edge was assigned ~5x its lane
# capacity), so each zone spawns over many weighted edges instead. Corridor
# zones use the minor-road mesh around their centroid — the primary/trunk axis
# itself is excluded so through demand doesn't materialize mid-corridor.
# External gates use every arterial crossing the OSM extract bbox
# (sim/net/README.md: 27.655-27.715/85.275-85.375; Overpass keeps complete
# ways, so crossing stubs overhang it) plus arterials around the gate point,
# which also covers groups lying partly inside the bbox (1xx, 2xx, 3xx).
MINOR = ("highway.residential", "highway.living_street", "highway.unclassified",
         "highway.tertiary", "highway.secondary")
OSM_BBOX = (85.275, 27.655, 85.375, 27.715)
TAZ_RADIUS = 600
MIN_EDGE_LEN = 25  # fits the 24.7 m bus/truck at insertion


def lonlat_to_xy(net):
    """Affine lon/lat -> net XY, least-squares fitted on OSM nodes matched to
    net nodes; exact enough (<5 m over the 13 km bbox) to skip pyproj."""
    pat = re.compile(r'<node id="(\d+)" lat="([\d.]+)" lon="([\d.]+)"')
    osm = {}
    with open(OSM) as f:
        for line in f:
            if m := pat.search(line):
                osm[m[1]] = (float(m[3]), float(m[2]))
    pairs = [(osm[n.getID()], n.getCoord())
             for n in net.getNodes() if n.getID() in osm]
    A = np.array([[lon, lat, 1.0] for (lon, lat), _ in pairs])
    X = np.array([xy for _, xy in pairs])
    coef = np.linalg.lstsq(A, X)[0]
    assert np.abs(A @ coef - X).max() < 5, "geo fit off; net/OSM mismatch"
    return lambda lon, lat: tuple(np.array([lon, lat, 1.0]) @ coef)


def pick_edges(net, x, y, cx, cy, major):
    """(origin edge, destination edge) nearest (x, y): origin heads toward the
    corridor center, destination away, so one-way boundary stubs don't
    dead-end routes. Probe representatives for the cordon filter only."""
    cands = []
    for e, d in net.getNeighboringEdges(x, y, 500):
        if not e.allows("passenger"):
            continue
        if major and not any(t in e.getType() for t in MAJOR):
            continue
        (fx, fy), (tx, ty) = e.getFromNode().getCoord(), e.getToNode().getCoord()
        inbound = (tx - fx) * (cx - fx) + (ty - fy) * (cy - fy) > 0
        cands.append((d, inbound, e.getID()))
    cands.sort()
    src = next(eid for _, inb, eid in cands if inb)
    dst = next(eid for _, inb, eid in cands if not inb)
    return src, dst


def zone_edges(net, zones, to_xy):
    cx, cy = to_xy(*CENTER)
    memo = {}
    out = {}
    for z in zones:
        point = ZONE_POINTS.get(z) or GROUP_POINTS[z // 100]
        if point not in memo:
            x, y = to_xy(*point)
            memo[point] = pick_edges(net, x, y, cx, cy, z not in ZONE_POINTS)
        out[z] = memo[point]
    return out


def taz_id(zone):
    return str(zone) if zone in ZONE_POINTS else f"g{zone // 100}"


def area_edges(net, x, y, minor):
    out = []
    for e, _ in net.getNeighboringEdges(x, y, TAZ_RADIUS):
        if not e.allows("passenger") or e.getLength() < MIN_EDGE_LEN:
            continue
        if minor and e.getType() in MINOR:
            out.append(e)
        elif not minor and any(t in e.getType() for t in MAJOR):
            out.append(e)
    return out


def build_taz(net, to_xy):
    """Write TAZ_FILE and return {taz_id: (sources, sinks)}, each a
    ([edge_id], [cumulative weight]) pair for sampling. Weight = lane count x
    edge priority (insertion capacity x road class)."""
    weight = lambda e: len(e.getLanes()) * e.getPriority()
    x0, y0 = to_xy(OSM_BBOX[0], OSM_BBOX[1])
    x1, y1 = to_xy(OSM_BBOX[2], OSM_BBOX[3])
    inside = lambda x, y: x0 <= x <= x1 and y0 <= y <= y1
    gate_pts = {}
    for g, p in GROUP_POINTS.items():
        gate_pts.setdefault(to_xy(*p), []).append(g)

    cross_src, cross_snk = {}, {}
    for e in net.getEdges():
        if (not e.allows("passenger") or e.getLength() < MIN_EDGE_LEN
                or not any(t in e.getType() for t in MAJOR)):
            continue
        fin = inside(*e.getFromNode().getCoord())
        tin = inside(*e.getToNode().getCoord())
        if fin == tin:
            continue
        nx, ny = (e.getToNode() if fin else e.getFromNode()).getCoord()
        pt = min(gate_pts, key=lambda p: (p[0] - nx) ** 2 + (p[1] - ny) ** 2)
        (cross_src if tin else cross_snk).setdefault(pt, []).append(e)

    taz = {}
    for z, p in ZONE_POINTS.items():
        edges = area_edges(net, *to_xy(*p), True)
        assert len(edges) >= 24, f"zone {z}: {len(edges)} spawn edges"
        taz[str(z)] = (edges, edges)
    for pt, groups in gate_pts.items():
        area = area_edges(net, *pt, False)
        src = list({e.getID(): e for e in area + cross_src.get(pt, [])}.values())
        snk = list({e.getID(): e for e in area + cross_snk.get(pt, [])}.values())
        assert len(src) >= 12 and len(snk) >= 12, f"groups {groups}: thin gate"
        for g in groups:
            taz[f"g{g}"] = (src, snk)

    with open(TAZ_FILE, "w") as f:
        f.write("<!-- zone/gate spawn edges, generated by pipeline/cordon.py;"
                " weight = lanes x priority. See pipeline/README.md. -->\n")
        f.write("<additional>\n")
        for tid, (src, snk) in sorted(taz.items()):
            f.write(f'    <taz id="{tid}">\n')
            for e in src:
                f.write(f'        <tazSource id="{e.getID()}"'
                        f' weight="{weight(e)}"/>\n')
            for e in snk:
                f.write(f'        <tazSink id="{e.getID()}"'
                        f' weight="{weight(e)}"/>\n')
            f.write("    </taz>\n")
        f.write("</additional>\n")

    return {tid: (([e.getID() for e in src],
                   list(accumulate(weight(e) for e in src))),
                  ([e.getID() for e in snk],
                   list(accumulate(weight(e) for e in snk))))
            for tid, (src, snk) in taz.items()}


def run_duarouter(trips, out, taz=None):
    cmd = [str(DUAROUTER), "-n", str(NET), "-r", str(trips), "-o", str(out),
           "--ignore-errors", "--no-warnings", "--no-step-log",
           "--routing-threads", "8"]
    if taz:
        cmd += ["--additional-files", str(taz)]
    subprocess.run(cmd, check=True, capture_output=True, text=True)


def probe_keep(zedge, cordon, tmp):
    """Cordon filter (spec §2, pragmatic): route one probe trip per distinct
    (origin-edge, destination-edge) combo; keep combos whose shortest path
    crosses a counted cordon edge. Zone pairs inherit their combo's verdict."""
    combos = sorted({(zedge[o][0], zedge[d][1])
                     for o in zedge for d in zedge if o != d})
    trips = tmp / "probe.trips.xml"
    with open(trips, "w") as f:
        f.write("<routes>\n")
        for i, (s, t) in enumerate(combos):
            f.write(f'  <trip id="{i}" depart="0" from="{s}" to="{t}"/>\n')
        f.write("</routes>\n")
    out = tmp / "probe.rou.xml"
    run_duarouter(trips, out)
    keep = set()
    for veh in ET.parse(out).getroot().iter("vehicle"):
        if cordon.intersection(veh.find("route").get("edges").split()):
            keep.add(combos[int(veh.get("id"))])
    return keep


def slice_bins(daily):
    """15-min departure counts for 06:00-12:00 from a daily total, per
    HOURLY_SHARE; cumulative floor conserves the window total to <1 trip."""
    bins, cum, prev = [], 0.0, 0
    for h in range(6, 12):
        for _ in range(4):
            cum += daily * HOURLY_SHARE[h] / 4
            n = math.floor(cum + 1e-9)
            bins.append(n - prev)
            prev = n
    return bins


def trips_header(factor):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<!-- baseline corridor demand, generated by pipeline/cordon.py:",
        "     od_2011.parquet (JICA 2012 vol04 vehicle OD) x growth"
        f" {factor:.4f} (DoR station {GROWTH_STATION}, A3),",
        "     cordon-filtered per sim/net/junction_map.csv, A1 departure"
        " profile 06:00-12:00,",
        "     edges drawn per zones.taz.xml weights."
        " See pipeline/README.md. -->",
        "<routes>",
    ]
    for mode, a in VTYPES.items():
        attrs = " ".join(f'{k}="{v}"' for k, v in a.items())
        lines.append(f'    <vType id="{mode}" {attrs}/>')
    return "\n".join(lines) + "\n"


def main():
    od = pd.read_parquet(REPO / "data/processed/od_2011.parquet")
    od = od[od["mode"] != "person_all"]
    gf = pd.read_csv(REPO / "data/processed/growth_factors.csv",
                     index_col="station_no").loc[GROWTH_STATION]
    factor = gf["aadt_pcu_end"] / gf["aadt_pcu_start"]

    net = sumolib.net.readNet(str(NET))
    to_xy = lonlat_to_xy(net)
    zones = sorted(set(od["origin_zone"]) | set(od["dest_zone"]))
    zedge = zone_edges(net, zones, to_xy)
    with open(JUNCTION_MAP) as f:
        cordon = {row["edge_id"] for row in csv.DictReader(f)}
    with tempfile.TemporaryDirectory() as td:
        keep = probe_keep(zedge, cordon, Path(td))

    mask = od.apply(
        lambda r: (zedge[r.origin_zone][0], zedge[r.dest_zone][1]) in keep,
        axis=1)
    cod = od[mask].rename(columns={"trips": "trips_2011"}).reset_index(drop=True)
    cod["trips"] = cod["trips_2011"] * factor
    cod.to_parquet(OUT_OD, index=False)

    DEMAND.mkdir(exist_ok=True)
    taz = build_taz(net, to_xy)
    rng = random.Random(20260815)  # fixed seed: reproducible edge draws
    entries = []
    window, analysis = Counter(), Counter()
    for r in cod.itertuples():
        ftz, ttz = taz_id(r.origin_zone), taz_id(r.dest_zone)
        src_ids, src_cw = taz[ftz][0]
        snk_ids, snk_cw = taz[ttz][1]
        for b, n in enumerate(slice_bins(r.trips)):
            t0 = 6 * 3600 + b * 900
            for i in range(n):
                dep = t0 + (i + 0.5) * 900 / n
                window[r.mode] += 1
                if ANALYSIS[0] <= dep < ANALYSIS[1]:
                    analysis[r.mode] += 1
                src = rng.choices(src_ids, cum_weights=src_cw)[0]
                dst = rng.choices(snk_ids, cum_weights=snk_cw)[0]
                entries.append((dep, (
                    f'<trip id="{r.mode}.{r.origin_zone}.{r.dest_zone}.{b}.{i}"'
                    f' type="{r.mode}" depart="{dep:.2f}" from="{src}"'
                    f' to="{dst}" fromTaz="{ftz}" toTaz="{ttz}"'
                    f' departLane="best"/>')))
    entries.sort()
    trips_path = DEMAND / "baseline.trips.xml"
    with open(trips_path, "w") as f:
        f.write(trips_header(factor))
        for _, line in entries:
            f.write("    " + line + "\n")
        f.write("</routes>\n")

    rou_path = DEMAND / "baseline.rou.xml"
    run_duarouter(trips_path, rou_path, taz=TAZ_FILE)
    origins = Counter()
    with open(rou_path) as f:
        for line in f:
            if m := re.search(r'<route edges="([^" ]+)', line):
                origins[m[1]] += 1
    routed = sum(origins.values())
    top_edge, top_n = origins.most_common(1)[0]

    print(f"growth factor (station {GROWTH_STATION}): {factor:.4f}")
    print(f"OD cells kept: {len(cod)}/{len(od)}"
          f" ({cod['trips'].sum():.0f} veh/day grown)")
    print("trips 06:00-12:00:", dict(sorted(window.items())))
    print("trips 08:00-11:00:", dict(sorted(analysis.items())))
    print(f"routed: {routed}/{len(entries)}")
    print(f"origin edges: {len(origins)} distinct;"
          f" max share {top_n / routed:.2%} ({top_edge}, {top_n} trips)")


if __name__ == "__main__":
    main()
