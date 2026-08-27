"""Figures for the paper, generated from the run outputs they describe.

PDF (vector) into results/figures/paper/. Greyscale with distinct markers and
dash patterns: thesis and journal figures get printed in black and white, and
the series have to stay separable there.

The network meanData is written with excludeEmpty, so an edge appears in an
interval only if it carried traffic. Congestion shares are therefore shares of
edges carrying traffic, not of every edge in the network, and the axis says so.

Run: uv run python -m experiments.paper_figures
"""

import argparse
import collections
import csv
import xml.etree.ElementTree as ET
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402  (backend must precede pyplot)

from pipeline.common import REPO  # noqa: E402
from pipeline.cordon import HOURLY_SHARE  # noqa: E402
from pipeline.throughput_audit import audit  # noqa: E402

OUT = REPO / "results/figures/paper"
INK, MUTED, PALE = "#171717", "#666666", "#a3a3a3"
STYLES = [(INK, "o", "-"), (MUTED, "s", "--"), (PALE, "^", ":"),
          (INK, "D", "-."), (MUTED, "v", "-"), (PALE, "P", "--")]

plt.rcParams.update({"font.size": 9, "axes.labelsize": 9,
                     "legend.frameon": False, "figure.dpi": 200})


def _clean(ax):
    ax.spines[["top", "right"]].set_visible(False)


def _hours(rows):
    return [f"{h // 3600:02d}" for h, *_ in rows]


def profile(out):
    """The measured morning profile against the assumption it replaced."""
    hours = sorted(HOURLY_SHARE)
    fig, ax = plt.subplots(figsize=(5.0, 2.9))
    ax.bar([f"{h:02d}" for h in hours], [100 * HOURLY_SHARE[h] for h in hours],
           color=PALE, edgecolor=INK, linewidth=0.7)
    ax.axhline(20, color=INK, linestyle="--", linewidth=1)
    ax.text(0.02, 20.6, "share assumed from person-trip generation",
            fontsize=7.5, color=INK)
    ax.set_xlabel("clock hour")
    ax.set_ylabel("share of daily vehicle traffic (%)")
    ax.set_ylim(0, 23)
    _clean(ax)
    fig.tight_layout()
    fig.savefig(out / "profile.pdf")
    plt.close(fig)


def loading(runs, out):
    """Delivered flow by hour at each loading, and total delivered by loading."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.0))
    totals = []
    for (label, d), (colour, marker, dash) in zip(runs.items(), STYLES):
        rows = audit(d)
        ax1.plot(_hours(rows), [100 * r for *_, r in rows], color=colour,
                 marker=marker, linestyle=dash, markersize=4, label=label)
        totals.append((label, sum(g for _, _, g, _ in rows)))
    ax1.set_xlabel("clock hour")
    ax1.set_ylabel("delivered / counted (%)")
    ax1.legend(fontsize=8, ncol=2)
    _clean(ax1)

    ax2.bar([lb for lb, _ in totals], [t / 1000 for _, t in totals],
            color=PALE, edgecolor=INK, linewidth=0.7)
    ax2.set_xlabel("demand loading")
    ax2.set_ylabel("total delivered (thousand crossings)")
    _clean(ax2)
    fig.tight_layout()
    fig.savefig(out / "loading.pdf")
    plt.close(fig)


def _jam_profile(run):
    """[(hour, share of trafficked edges under 1 m/s)] for one run."""
    root = ET.parse(Path(run) / "edgedata_net.xml").getroot()
    out = []
    for iv in root.findall("interval"):
        speeds = [float(e.get("speed")) for e in iv.findall("edge")
                  if e.get("speed") is not None]
        if speeds:
            out.append((int(float(iv.get("begin"))) // 3600,
                        sum(s < 1.0 for s in speeds) / len(speeds)))
    return out


def lanes(before, after, out):
    """What deriving lanes from carriageway width recovered."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.0))
    for (label, d), (colour, marker, dash) in zip(
            (("lanes from markings", before),
             ("lanes from carriageway width", after)), STYLES):
        rows = audit(d)
        ax1.plot(_hours(rows), [100 * r for *_, r in rows], color=colour,
                 marker=marker, linestyle=dash, markersize=4, label=label)
        jam = _jam_profile(d)
        ax2.plot([f"{h:02d}" for h, _ in jam], [100 * j for _, j in jam],
                 color=colour, marker=marker, linestyle=dash, markersize=4,
                 label=label)
    ax1.set_xlabel("clock hour")
    ax1.set_ylabel("delivered / counted (%)")
    ax1.legend(fontsize=8)
    ax2.set_xlabel("clock hour")
    ax2.set_ylabel("trafficked edges below 1 m/s (%)")
    _clean(ax1)
    _clean(ax2)
    fig.tight_layout()
    fig.savefig(out / "lanes.pdf")
    plt.close(fig)


def corridor(out):
    """Study area: the network, with the counted junctions marked."""
    import sumolib

    net = sumolib.net.readNet(str(REPO / "sim/net/corridor-calibrated.net.xml"))
    counted = collections.defaultdict(list)
    for r in csv.DictReader(open(REPO / "sim/net/junction_map.csv")):
        if net.hasEdge(r["edge_id"]):
            counted[r["intersection"]].append(net.getEdge(r["edge_id"]))

    fig, ax = plt.subplots(figsize=(6.0, 4.2))
    for e in net.getEdges():
        xs, ys = zip(*e.getShape())
        major = any(t in (e.getType() or "")
                    for t in ("motorway", "trunk", "primary"))
        ax.plot(xs, ys, color=INK if major else "#dcdcdc",
                linewidth=0.7 if major else 0.3, zorder=2 if major else 1)

    for name, edges in counted.items():
        pts = [e.getShape()[len(e.getShape()) // 2] for e in edges]
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        ax.plot(cx, cy, "o", color=INK, markersize=5, zorder=3)
        ax.annotate(name, (cx, cy), xytext=(4, 4), textcoords="offset points",
                    fontsize=7, zorder=4)

    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(out / "corridor.pdf")
    plt.close(fig)


def _sweep(results, scenario, pattern=None):
    """{share: (mean delta delay %, sem %, mean delta throughput %)} for one
    scenario, read against that sweep's own baseline."""
    import json
    import re
    import statistics as st

    root = Path(results)
    base = json.load(open(root / "baseline/baseline/metrics.json"))
    bd, bh = base["D_net_veh_h"], base["H_cordon_pcu_0811"]
    runs = collections.defaultdict(list)
    for f in (root / scenario).glob("*/metrics.json"):
        tag = re.sub(r"_seed\d+", "", f.parent.name)
        if pattern and not re.match(pattern, tag):
            continue
        m = json.load(open(f))
        runs[tag].append((m["D_net_veh_h"], m["H_cordon_pcu_0811"]))
    out = {}
    for tag, v in runs.items():
        share = float(re.search(r"([\d.]+)$", tag).group(1))
        d = [x for x, _ in v]
        h = [y for _, y in v]
        sd = st.stdev(d) if len(d) > 1 else 0.0
        out[share] = (100 * (st.mean(d) - bd) / bd,
                      100 * sd / bd / len(d) ** 0.5,
                      100 * (st.mean(h) - bh) / bh)
    return dict(sorted(out.items()))


def levers(results, out):
    """The headline: what each intervention does to network delay."""
    series = [
        ("Mode shift (motorcycle to bus)",
         _sweep(results, "s3-joint", r"pt0\.0_dt-15_m")),
        ("Rerouting onto alternatives",
         _sweep(results, "s0-spatial-control", r"p_r")),
        ("Departure retiming",
         _sweep(results, "s2-retime-grid", r"pt[\d.]+_dt-15$")),
        ("School-hours shift",
         _sweep(results, "s1-school", r"sch")),
    ]
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    for (label, data), (colour, marker, dash) in zip(series, STYLES):
        if not data:
            continue
        xs = [100 * k for k in data]
        ys = [v[0] for v in data.values()]
        es = [v[1] for v in data.values()]
        ax.errorbar(xs, ys, yerr=es, color=colour, marker=marker,
                    linestyle=dash, markersize=4, capsize=3, label=label)
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.set_xlabel("share of trips treated (%)")
    ax.set_ylabel("change in network delay (%)")
    ax.legend(fontsize=8)
    _clean(ax)
    fig.tight_layout()
    fig.savefig(out / "levers.pdf")
    plt.close(fig)


def regime(stable, collapsed, out):
    """The same rerouting grid measured at two loadings. The sign flips."""
    fig, ax = plt.subplots(figsize=(5.4, 3.4))
    for (label, res), (colour, marker, dash) in zip(
            (("0.55 loading, network carries its demand", stable),
             ("full counted demand, network in collapse", collapsed)), STYLES):
        data = _sweep(res, "s0-spatial-control", r"p_r")
        if not data:
            continue
        ax.errorbar([100 * k for k in data], [v[0] for v in data.values()],
                    yerr=[v[1] for v in data.values()], color=colour,
                    marker=marker, linestyle=dash, markersize=4, capsize=3,
                    label=label)
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.set_xlabel("share of trips diverted (%)")
    ax.set_ylabel("change in network delay (%)")
    ax.legend(fontsize=8)
    _clean(ax)
    fig.tight_layout()
    fig.savefig(out / "regime.pdf")
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", type=Path, default=REPO / "results")
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    def has(d):
        return (d / "edgedata_net.xml").exists()

    profile(args.out)
    corridor(args.out)

    runs = {f"{p}%": args.results / f"diag-scale{p}" for p in (50, 55, 60, 65, 70)}
    runs["100%"] = args.results / "diag-laned"
    runs = {k: v for k, v in runs.items() if has(v)}
    if runs:
        loading(runs, args.out)

    before, after = args.results / "diag-stochastic", args.results / "diag-laned"
    if has(before) and has(after):
        lanes(before, after, args.out)

    sweep = args.results / "sweep"
    if (sweep / "baseline/baseline/metrics.json").exists():
        levers(sweep, args.out)
        collapsed = args.results.parent / "archive/pre-lane-width-results/sweep"
        if (collapsed / "baseline/baseline/metrics.json").exists():
            regime(sweep, collapsed, args.out)

    for f in sorted(args.out.glob("*.pdf")):
        print(f"{f.relative_to(REPO)}  {f.stat().st_size // 1024} kB")


if __name__ == "__main__":
    main()
