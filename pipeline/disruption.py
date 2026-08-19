"""Disruption scenarios: closures and weather, as SUMO additional files.

The project's primary module tests whether coordinated guidance beats the jam
traffic organises for itself when a link fails. That needs the failure to be
real in the simulation, so closures are written as rerouters with
<closingReroute>: SUMO then blocks the edge for the interval and reroutes
approaching vehicles reactively — which is exactly the uncoordinated response
we want as the comparison baseline. Guided vehicles are diverted in advance by
experiments.transforms.spread_reroute.

Kathmandu's non-recurring congestion has three documented shapes:
  closure  — VIP movement or an accident shutting a corridor link outright
  rain     — network-wide capacity loss, monsoon afternoons
  both     — the compound case

Run: uv run python -m pipeline.disruption --kind closure --edges E1 E2 \
        --begin 32400 --end 36000 -o sim/incidents/closure.add.xml
"""

import argparse
from pathlib import Path

# Wet-weather effects. SUMO has no rainfall model, so weather enters as reduced
# free-flow speed and longer following gaps, the two mechanisms wet roads act
# through. The 0.8 speed factor sits inside the 10-30% wet-weather speed
# reduction range reported in the highway-capacity literature ★ (no
# Kathmandu-specific measurement exists; sweep 0.7/0.9 as sensitivity).
RAIN_SPEED_FACTOR = 0.8


def closure(edges, begin, end):
    lines = ['<additional>']
    for i, edge in enumerate(edges):
        lines += [
            f'    <rerouter id="closure{i}" edges="{edge}">',
            f'        <interval begin="{begin}" end="{end}">',
            f'            <closingReroute id="{edge}"/>',
            '        </interval>',
            '    </rerouter>',
        ]
    lines.append('</additional>')
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
    ap.add_argument("-o", "--out", type=Path, required=True)
    args = ap.parse_args()

    body = (closure if args.kind == "closure" else rain)(
        args.edges, args.begin, args.end)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(body)
    print(f"{args.out}: {args.kind} on {len(args.edges)} edges, "
          f"{args.begin}-{args.end}s")


if __name__ == "__main__":
    main()
