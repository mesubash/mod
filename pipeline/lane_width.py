"""Lane counts from carriageway width, for a network without lane markings.

The corridor's arterials are tagged `lanes=1` in OSM and are 6-8 m wide. Both
facts are true: the roads carry no lane markings, so one is the honest marked
count. netconvert reads the tag and builds a single 3.2 m lane, which is a
third of Ram Shah Path. The calibrated demand then asks that lane for 4,563
veh/h against a physical ceiling near 2,000, it jams within minutes, and the
jam propagates until the network delivers 6.7% of counted volume at the peak
hour. Signals, junction control, route concentration and simulation mode were
each tested and each ruled out; this is the binding constraint.

Non-lane-based traffic uses the carriageway, not the markings: JICA 2012
records manual police metering at 9 of 10 study junctions, and the IOE
saturation-flow study documents non-lane-based operation departing from
conventional lane capacity. Deriving the lane count from width is the standard
way to give a lane-based simulator the road that is actually there.

Outputs data/processed/corridor-laned.osm; netconvert builds from that.

Run: uv run python -m pipeline.lane_width
"""

import argparse
import re
from pathlib import Path

from pipeline.common import REPO

SRC = REPO / "data/raw/corridor.osm"
OUT = REPO / "data/processed/corridor-laned.osm"

# A14: effective width of one traffic stream. A marked Nepali lane is 3.5 m,
# but non-lane-based operation packs streams tighter than the markings would
# allow; 3.0 m is the value used here and is the assumption to sweep (2.75/3.5)
# if the baseline proves sensitive to it.
STREAM_WIDTH = 3.0
MAX_LANES = 4
# Widths outside this range are tagging errors, not roads: the extract contains
# a way tagged 608 m and several tagged under 2 m (cycle lanes recorded as the
# carriageway). Fall back to the class default for those.
PLAUSIBLE = (2.5, 25.0)
# Class medians from the extract's own width tags, for ways carrying none.
CLASS_WIDTH = {"motorway": 8.0, "trunk": 7.0, "primary": 8.0, "secondary": 7.0,
               "tertiary": 7.0, "unclassified": 5.0, "residential": 4.5}

WAY = re.compile(r'<way id="(\d+)"(.*?)</way>', re.S)
TAG = re.compile(r'<tag k="([^"]+)" v="([^"]+)"\s*/>')


def parse_width(raw):
    """Metres from an OSM width value, or None. Handles '6', '6.0', '1.75 m'."""
    if raw is None:
        return None
    m = re.match(r"\s*([0-9]*\.?[0-9]+)", raw)
    if not m:
        return None
    value = float(m.group(1))
    if "'" in raw or "ft" in raw:
        value *= 0.3048
    return value


def lanes_from_width(tags):
    """Lane count per direction implied by the carriageway, or None to leave
    the way alone (not a road, or no usable width)."""
    highway = tags.get("highway")
    if highway not in CLASS_WIDTH:
        return None
    width = parse_width(tags.get("width"))
    if width is None or not PLAUSIBLE[0] <= width <= PLAUSIBLE[1]:
        width = CLASS_WIDTH[highway]
    # A two-way road's tagged width spans both directions; netconvert builds an
    # edge per direction, so each gets half.
    if tags.get("oneway") not in ("yes", "1", "-1"):
        width /= 2
    return max(1, min(MAX_LANES, round(width / STREAM_WIDTH)))


def patch(src=SRC, out=OUT):
    text = src.read_text(encoding="utf8", errors="ignore")
    stats = {"ways": 0, "raised": 0, "unchanged": 0, "added": 0}

    def repl(match):
        body = match.group(2)
        tags = dict(TAG.findall(body))
        derived = lanes_from_width(tags)
        if derived is None:
            return match.group(0)
        stats["ways"] += 1
        tagged = tags.get("lanes")
        # Never reduce a surveyed lane count: the width rule exists to recover
        # capacity the marked count omits, not to overrule a real survey.
        if tagged is not None:
            if derived <= int(re.sub(r"\D", "", tagged) or 1):
                stats["unchanged"] += 1
                return match.group(0)
            stats["raised"] += 1
            return match.group(0).replace(
                f'<tag k="lanes" v="{tagged}"/>', f'<tag k="lanes" v="{derived}"/>')
        stats["added"] += 1
        return match.group(0).replace(
            "</way>", f'  <tag k="lanes" v="{derived}"/>\n  </way>')

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(WAY.sub(repl, text), encoding="utf8")
    return stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, default=SRC)
    ap.add_argument("-o", "--out", type=Path, default=OUT)
    args = ap.parse_args()
    stats = patch(args.src, args.out)
    print(f"{args.out}: {stats['ways']} road ways; "
          f"lanes added {stats['added']}, raised {stats['raised']}, "
          f"left alone {stats['unchanged']}")


if __name__ == "__main__":
    main()
