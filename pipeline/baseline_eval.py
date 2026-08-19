"""M3 baseline calibration evaluation (spec §7, criterion A7).

Inputs: results/baseline_edgedata_{motorcycle,car,bus,truck}.xml,
results/baseline_edgedata_net.xml, results/baseline_queues.xml (all produced
by `uv run sumo -c sim/baseline.sumocfg`), sim/net/junction_map.csv,
data/processed/counts_2019.parquet, sim/net/corridor-filtered.net.xml.

Outputs: results/baseline_calibration.csv, results/baseline_metrics.json.

Daily-tier comparison (the OCR stage recovered no hourly counts): modeled
leg-direction PCU summed over 07:00-12:00 (warm-up hour excluded) is compared
against WINDOW_SHARE x pcu_24h, where WINDOW_SHARE is the sum of the measured
A1 hourly shares for 07:00-12:00 (pipeline/cordon.py HOURLY_SHARE, from
data/processed/hourly_profile.parquet). The same profile built the demand, so
this tier tests growth factor + spatial allocation + routing, not the profile
itself.
"""

import csv
import json
from xml.etree import ElementTree as ET

from pipeline.common import REPO as ROOT
from pipeline.cordon import HOURLY_SHARE

# spec §3 primary PCU set
PCU = {"motorcycle": 0.3, "car": 1.0, "bus": 4.0, "truck": 4.0}
# Derived from the demand profile itself so the two can never drift apart: a
# hardcoded 0.50 survived the A1 correction and inflated every target by 1.5x.
WINDOW_SHARE = sum(share for hour, share in HOURLY_SHARE.items() if hour >= 7)
COMPARE_HOURS = range(25200, 43200, 3600)   # 07:00-12:00 bins
ANALYSIS = (28800, 39600)    # 08:00-11:00
TOL, PASS_SHARE = 0.15, 0.85  # A7

RESULTS = ROOT / "results"


def edge_counts(files):
    """{(edge, interval_begin): {vtype: entered+departed}} from edgeData files."""
    out = {}
    for vt, path in files.items():
        for _, elem in ET.iterparse(path):
            if elem.tag == "interval":
                begin = float(elem.get("begin"))
                for e in elem:
                    n = int(e.get("entered", 0)) + int(e.get("departed", 0))
                    out.setdefault((e.get("id"), begin), {})[vt] = n
                elem.clear()
    return out


def leg_volumes(jmap_rows, counts, hours):
    """Modeled PCU per (intersection, leg, direction) over the given hour bins."""
    vols = {}
    for row in jmap_rows:
        key = (row["intersection"], int(row["leg"]), row["direction"])
        pcu = sum(
            counts.get((row["edge_id"], float(h)), {}).get(vt, 0) * PCU[vt]
            for h in hours
            for vt in PCU
        )
        vols[key] = vols.get(key, 0.0) + pcu
    return vols


def net_hourly(path):
    """{(edge, begin): (entered+departed, traveltime, timeLoss_total)}."""
    out = {}
    for _, elem in ET.iterparse(path):
        if elem.tag == "interval":
            begin = float(elem.get("begin"))
            for e in elem:
                out[(e.get("id"), begin)] = (
                    int(e.get("entered", 0)) + int(e.get("departed", 0)),
                    float(e.get("traveltime", 0)),
                    float(e.get("timeLoss", 0)),
                )
            elem.clear()
    return out


def queue_series(path, lanes_by_int):
    """Per-intersection {t: total_queue_m} sampled every 60 s, mapped approach lanes."""
    lane_to_int = {ln: i for i, lns in lanes_by_int.items() for ln in lns}
    series = {i: {} for i in lanes_by_int}
    for _, elem in ET.iterparse(path):
        if elem.tag == "data":
            t = float(elem.get("timestep"))
            for lane in elem.iter("lane"):
                i = lane_to_int.get(lane.get("id"))
                if i is not None:
                    series[i][t] = series[i].get(t, 0.0) + float(
                        lane.get("queueing_length")
                    )
            elem.clear()
    return series


def s7_metrics(results_dir, prefix="baseline_"):
    """Spec §7 metrics from one run's outputs: {prefix}edgedata_{vtype}.xml,
    {prefix}edgedata_net.xml, {prefix}queues.xml in results_dir. Shared by the
    baseline evaluation and experiments/run.py scenario runs."""
    import sumolib

    jmap = list(csv.DictReader(open(ROOT / "sim/net/junction_map.csv")))
    counts = edge_counts(
        {vt: results_dir / f"{prefix}edgedata_{vt}.xml" for vt in PCU}
    )
    nh = net_hourly(results_dir / f"{prefix}edgedata_net.xml")
    win_bins = [b for b in COMPARE_HOURS if ANALYSIS[0] <= b < ANALYSIS[1]]

    in_edges = {}
    for r in jmap:
        if r["direction"] == "in":
            in_edges.setdefault(r["intersection"], []).append(r["edge_id"])

    d_i = {}
    for i, edges in in_edges.items():
        veh = sum(nh.get((e, b), (0, 0, 0))[0] for e in edges for b in win_bins)
        loss = sum(nh.get((e, b), (0, 0, 0))[2] for e in edges for b in win_bins)
        d_i[i] = round(loss / veh, 1) if veh else None

    # T_c: shortest path Tripureshwor leg 1 <-> Jadhibuti leg 1 along the axis;
    # per-edge time = analysis-window mean traveltime (veh-weighted), free-flow
    # where no vehicle sampled the edge.
    net = sumolib.net.readNet(str(ROOT / "sim/net/corridor-filtered.net.xml"))

    def edge_time(eid):
        veh = sum(nh.get((eid, b), (0, 0, 0))[0] for b in win_bins)
        if veh:
            tt = sum(
                nh.get((eid, b), (0, 0, 0))[1] * nh.get((eid, b), (0, 0, 0))[0]
                for b in win_bins
            )
            return tt / veh
        e = net.getEdge(eid)
        return e.getLength() / e.getSpeed()

    def corridor_time(from_edge, to_edge):
        path, _ = net.getShortestPath(net.getEdge(from_edge), net.getEdge(to_edge))
        if path is None:
            return None, []
        return sum(edge_time(e.getID()) for e in path) / 60, [e.getID() for e in path]

    tc_east, path_east = corridor_time("422272357#2", "232104797#2")
    tc_west, path_west = corridor_time("-232104797#2", "422263674#1")

    # H: PCU over the unique cordon edges, analysis window
    cordon_edges = {r["edge_id"] for r in jmap}
    H = sum(
        counts.get((e, float(b)), {}).get(vt, 0) * PCU[vt]
        for e in cordon_edges
        for b in win_bins
        for vt in PCU
    )

    # D_net: total time loss vs desired speed, all edges, analysis window (veh-h)
    D_net = sum(v[2] for (e, b), v in nh.items() if b in win_bins) / 3600

    # Q_i and t_diss from queue output on mapped approach lanes
    lanes_by_int = {
        i: [
            f"{e}_{k}"
            for e in edges
            for k in range(len(net.getEdge(e).getLanes()))
        ]
        for i, edges in in_edges.items()
    }
    qs = queue_series(results_dir / f"{prefix}queues.xml", lanes_by_int)
    # Mesoscopic runs have no lane-level queues, so the queue file is empty of
    # non-zero samples. Report None rather than 0.0: a zero here reads as "no
    # queue formed", which is the opposite of "this mode cannot measure queues".
    has_queues = any(v for s in qs.values() for v in s.values())
    Q_i = {
        i: (round(max((v for t, v in s.items()
                       if ANALYSIS[0] <= t < ANALYSIS[1]), default=0.0), 1)
            if has_queues else None)
        for i, s in qs.items()
    }

    # t_diss: total mapped-approach queue, 5-min means; pre-peak ref = 08:00-09:00
    # mean; dissipated when a 5-min mean after 10:00 drops to <= ref and stays
    # there for 15 min; censored at 12:00.
    total = {}
    for s in qs.values():
        for t, v in s.items():
            total[t] = total.get(t, 0.0) + v
    def mean5(t0):
        vals = [total.get(t0 + 60 * k, 0.0) for k in range(5)]
        return sum(vals) / 5
    ref = sum(total.get(t, 0.0) for t in range(28800, 32400, 60)) / 60
    t_diss = ">120 min (censored)" if has_queues else None
    for t0 in range(36000, 43200 - 900, 300) if has_queues else []:
        if all(mean5(t0 + 300 * j) <= ref for j in range(3)):
            t_diss = round((t0 - 36000) / 60, 1)
            break

    return {
        "d_i_s_per_veh": d_i,
        "Q_i_max_queue_m": Q_i,
        "T_c_min": {"eastbound_Tripureshwor_to_Jadhibuti": round(tc_east, 1),
                    "westbound_Jadhibuti_to_Tripureshwor": round(tc_west, 1),
                    "route_edges": {"east": len(path_east), "west": len(path_west)}},
        "H_cordon_pcu_0811": round(H, 0),
        "t_diss_min_after_1000": t_diss,
        "t_diss_prepeak_ref_m": round(ref, 1),
        "D_net_veh_h": round(D_net, 0),
    }


def main():
    import pandas as pd

    jmap = list(csv.DictReader(open(ROOT / "sim/net/junction_map.csv")))
    counts = edge_counts(
        {vt: RESULTS / f"baseline_edgedata_{vt}.xml" for vt in PCU}
    )

    # --- calibration table ---
    modeled = leg_volumes(jmap, counts, COMPARE_HOURS)
    cdf = pd.read_parquet(ROOT / "data/processed/counts_2019.parquet")
    daily = cdf[cdf.metric == "pcu_24h"].set_index(
        ["intersection", "leg", "direction"]
    ).value
    rows = []
    for key, target_24h in daily.items():
        target = WINDOW_SHARE * target_24h
        m = modeled.get(key, 0.0)
        dev = (m - target) / target
        rows.append(
            {
                "intersection": key[0],
                "leg": key[1],
                "direction": key[2],
                "modeled_pcu_0712": round(m, 1),
                "target_pcu_0712": round(target, 1),
                "pcu_24h": target_24h,
                "deviation": round(dev, 4),
                "pass": abs(dev) <= TOL,
            }
        )
    cal = pd.DataFrame(rows).sort_values(["intersection", "leg", "direction"])
    cal.to_csv(RESULTS / "baseline_calibration.csv", index=False)
    n_pass = int(cal["pass"].sum())
    criterion_met = n_pass / len(cal) >= PASS_SHARE

    metrics = {
        "criterion": f"A7: |dev| <= {TOL} on >= {PASS_SHARE:.0%} of 77 leg-directions, "
                     f"daily tier via WINDOW_SHARE={WINDOW_SHARE} (A1 profile, 07:00-12:00)",
        "n_pass": n_pass,
        "n_records": len(cal),
        "pass_rate": round(n_pass / len(cal), 3),
        "criterion_met": criterion_met,
        **s7_metrics(RESULTS),
    }
    (RESULTS / "baseline_metrics.json").write_text(json.dumps(metrics, indent=2))
    print(json.dumps(metrics, indent=2))
    print(f"\npass {n_pass}/{len(cal)} ({n_pass / len(cal):.1%}) -> "
          f"criterion {'MET' if criterion_met else 'NOT MET'}")


if __name__ == "__main__":
    main()
