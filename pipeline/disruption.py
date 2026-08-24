"""Disruption scenarios: closures and weather, as SUMO additional files.

The project's primary module tests whether coordinated guidance beats the jam
traffic organises for itself when a link fails. That needs the failure to be
real in the simulation, so closures are written as rerouters with
<closingReroute>: SUMO then blocks the edge for the interval and reroutes
approaching vehicles reactively — which is exactly the uncoordinated response
we want as the comparison baseline. Guided vehicles are diverted in advance by
experiments.transforms.spread_reroute.

The rerouter must sit UPSTREAM of the closed edge, on the approaches: SUMO
diverts a vehicle "as soon as they reach one of the edges given in the
edges-attribute" [SUMO Rerouter docs], and a vehicle can never reach an edge
that is closed. Placing the rerouter on the closed edge itself made the closure
invisible to every vehicle without a rerouting device — such a vehicle drove
through the shut road, and a run with no devices returned the baseline metrics
exactly.

Kathmandu's non-recurring congestion has three documented shapes:
  closure  — VIP movement or an accident shutting a corridor link outright
  rain     — network-wide capacity loss, monsoon afternoons
  both     — the compound case

Run: uv run python -m pipeline.disruption --kind closure --edges E1 E2 \
        --begin 32400 --end 36000 -o sim/incidents/closure.add.xml
"""

import argparse
from pathlib import Path

from pipeline.common import REPO

# Wet-weather effects. SUMO has no rainfall model, so weather enters as reduced
# free-flow speed and longer following gaps, the two mechanisms wet roads act
# through. The 0.8 speed factor sits inside the 10-30% wet-weather speed
# reduction range reported in the highway-capacity literature ★ (no
# Kathmandu-specific measurement exists; sweep 0.7/0.9 as sensitivity).
RAIN_SPEED_FACTOR = 0.8

# Approach depth for a closure rerouter (see closure()).
UPSTREAM_HOPS = 2


def upstream(net, edges, hops=UPSTREAM_HOPS):
    """Edge ids within `hops` of any closed edge, walking against traffic.

    Two hops is roughly a junction's worth of warning: enough that a diverted
    vehicle has a turn available, not so much that it is redirected from across
    the network. Closed edges are excluded — they are the thing being avoided."""
    closed = set(edges)
    frontier = {net.getEdge(e) for e in edges}
    found = set()
    for _ in range(hops):
        nxt = {p for e in frontier for p in e.getIncoming()
               if p.getID() not in closed and p not in found}
        found |= nxt
        frontier = nxt
    return sorted(e.getID() for e in found)


def closure(edges, begin, end, net):
    """Rerouter closing `edges` over the interval, triggered on the approaches.

    net is a sumolib net or a path to one. It is required: the approaches
    cannot be found without it, and defaulting to the closed edges is the bug
    that made the closure invisible to un-equipped vehicles."""
    if not hasattr(net, "getEdge"):
        import sumolib
        net = sumolib.net.readNet(str(net))
    trigger = upstream(net, edges)
    if not trigger:
        raise ValueError(
            f"no upstream approach to {edges}: the rerouter would never "
            "fire and the closure would be invisible")

    lines = ['<additional>',
             f'    <rerouter id="closure" edges="{" ".join(trigger)}">',
             f'        <interval begin="{begin}" end="{end}">']
    lines += [f'            <closingReroute id="{edge}"/>' for edge in edges]
    lines += ['        </interval>', '    </rerouter>', '</additional>']
    return "\n".join(lines) + "\n"


def rain(edges, begin, end, factor=RAIN_SPEED_FACTOR):
    """Network-wide speed reduction over the interval via variable speed signs."""
    lines = ['<additional>']
    for i, edge in enumerate(edges):
        lines += [
            f'    <variableSpeedSign id="rain{i}" lanes="{edge}_0">',
            f'        <step time="{begin}" speed="{factor:.2f}"/>',
            f'        <step time="{end}" speed="-1"/>',
            '    </variableSpeedSign>',
        ]
    lines.append('</additional>')
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", choices=("closure", "rain"), required=True)
    ap.add_argument("--edges", nargs="+", required=True)
    ap.add_argument("--begin", type=int, default=32400)   # 09:00, spec §4 peak
    ap.add_argument("--end", type=int, default=36000)     # 10:00
    ap.add_argument("--net", type=Path,
                    default=REPO / "sim/net/corridor-calibrated.net.xml",
                    help="net used to find the upstream approaches (closure)")
    ap.add_argument("-o", "--out", type=Path, required=True)
    args = ap.parse_args()

    body = (closure(args.edges, args.begin, args.end, args.net)
            if args.kind == "closure"
            else rain(args.edges, args.begin, args.end))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(body)
    print(f"{args.out}: {args.kind} on {len(args.edges)} edges, "
          f"{args.begin}-{args.end}s")


if __name__ == "__main__":
    main()
