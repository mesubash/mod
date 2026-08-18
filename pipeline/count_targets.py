"""Counted leg volumes -> SUMO edgeData file for count-based demand generation.

The corridor sub-OD (pipeline/cordon.py) reproduced only ~20% of the traffic the
2019 counts record at the study junctions: it represents trips between the eight
corridor zones and eight external gates, while the junctions also carry local and
through movements the zone system does not resolve. Rather than scale that demand
by an unprincipled factor, this module turns the counts themselves into the
calibration target for SUMO's routeSampler, which then draws from the routed
corridor demand until modeled flows match the counts.

Input: data/processed/counts_2019.parquet, sim/net/junction_map.csv.
Output: data/processed/count_targets.xml (hourly edgeData intervals,
07:00-12:00, PCU-free vehicle counts per counted edge).

Run: uv run python -m pipeline.count_targets
"""

import csv
from xml.etree import ElementTree as ET

import pandas as pd

from pipeline.common import REPO
from pipeline.cordon import HOURLY_SHARE

COUNTS = REPO / "data/processed/counts_2019.parquet"
JUNCTION_MAP = REPO / "sim/net/junction_map.csv"
OUT = REPO / "data/processed/count_targets.xml"
HOURS = range(7, 12)

# The counts are published in PCU; routeSampler matches vehicle counts. The 2019
# report gives the fleet mix at these junctions (motorcycle ~70%, car ~15%,
# spec §6) but never its PCU factors, so convert with the spec §3 primary set at
# the reported mix: 0.70*0.3 + 0.15*1.0 + 0.15*4.0 = 0.96 PCU per vehicle.
PCU_PER_VEHICLE = 0.70 * 0.3 + 0.15 * 1.0 + 0.15 * 4.0


def leg_edges():
    """{(intersection, leg, direction): [edge_id]} for inbound legs only.

    Outbound legs would double-count the same vehicles at the same junction."""
    edges = {}
    for row in csv.DictReader(open(JUNCTION_MAP)):
        if row["direction"] == "in":
            key = (row["intersection"], int(row["leg"]))
            edges.setdefault(key, []).append(row["edge_id"])
    return edges


def daily_counts():
    df = pd.read_parquet(COUNTS)
    daily = df[(df.metric == "pcu_24h") & (df.direction == "in")]
    return {(r.intersection, int(r.leg)): float(r.value) for r in daily.itertuples()}


def build():
    edges, daily = leg_edges(), daily_counts()
    root = ET.Element("data")
    for hour in HOURS:
        interval = ET.SubElement(
            root,
            "interval",
            id=f"h{hour}",
            begin=str(hour * 3600),
            end=str((hour + 1) * 3600),
        )
        for key, edge_ids in edges.items():
            if key not in daily:
                continue
            # Hourly vehicles on this leg, split evenly where a leg is carried by
            # several parallel edges (divided carriageways).
            vehicles = daily[key] * HOURLY_SHARE[hour] / PCU_PER_VEHICLE
            per_edge = round(vehicles / len(edge_ids))
            for edge_id in edge_ids:
                ET.SubElement(interval, "edge", id=edge_id, entered=str(per_edge))
    ET.ElementTree(root).write(OUT, encoding="unicode")
    total = sum(
        int(e.get("entered")) for i in root for e in i
    )
    print(f"{OUT}: {len(root)} hourly intervals, "
          f"{len(edges)} counted legs, {total:,} vehicle-entries 07:00-12:00")


if __name__ == "__main__":
    build()
