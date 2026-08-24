"""Does the network deliver the demand it was calibrated to carry?

The M3 criterion (A7) compares modeled leg volumes against counted volumes
summed over 07:00-12:00, and reports a pass rate. A pass rate hides when the
network delivers well early and collapses later: the baseline meets the demand
at 07:00 and carries 6.6% of it at 09:00, and one five-hour total cannot show
that. This audit reports delivered/target hour by hour on the routeSampler
count locations, which is the calibration's own target set.

Run: uv run python -m pipeline.throughput_audit [results/sweep/baseline/baseline]
"""

import argparse
import collections
from pathlib import Path
from xml.etree import ElementTree as ET

from pipeline.baseline_eval import PCU, edge_counts
from pipeline.common import REPO

TARGETS = REPO / "data/processed/count_targets.xml"


def targets(path=TARGETS):
    """{(edge, hour_begin): counted vehicles} from the routeSampler target file."""
    out = collections.defaultdict(float)
    for iv in ET.parse(path).getroot().iter("interval"):
        begin = int(float(iv.get("begin")))
        for e in iv.iter("edge"):
            out[(e.get("id"), begin)] += float(e.get("entered") or 0)
    return out


def delivered(results_dir, prefix=""):
    """{(edge, hour_begin): simulated vehicles} over the same locations."""
    counts = edge_counts(
        {vt: Path(results_dir) / f"{prefix}edgedata_{vt}.xml" for vt in PCU})
    out = collections.defaultdict(float)
    for (edge, begin), per_type in counts.items():
        out[(edge, int(begin))] += sum(per_type.values())
    return out


def audit(results_dir, prefix=""):
    """[(hour, target, delivered, ratio)] per counted hour."""
    tgt, got = targets(), delivered(results_dir, prefix)
    rows = []
    for hour in sorted({b for _, b in tgt}):
        keys = [k for k in tgt if k[1] == hour]
        t = sum(tgt[k] for k in keys)
        g = sum(got.get(k, 0.0) for k in keys)
        rows.append((hour, t, g, g / t if t else 0.0))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("results_dir", nargs="?",
                    default=REPO / "results/sweep/baseline/baseline")
    ap.add_argument("--prefix", default="")
    args = ap.parse_args()

    print(f"{'hour':>6}  {'target':>9}  {'delivered':>10}  {'ratio':>7}")
    for hour, t, g, r in audit(args.results_dir, args.prefix):
        print(f"{hour:6d}  {t:9.0f}  {g:10.0f}  {r:6.1%}")


if __name__ == "__main__":
    main()
