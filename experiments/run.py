"""M4 scenario orchestrator (spec §8): TOML config -> seeded transforms on the
baseline demand -> duarouter -> sumo (same net/options as sim/baseline.sumocfg)
-> spec §7 metrics via pipeline.baseline_eval.s7_metrics.

Run: uv run python -m experiments.run experiments/scenarios/<cfg>.toml [--dry-run]
Outputs: sim/demand/<scenario>/<run_id>.trips.xml (+ .rou.xml),
results/<scenario>/<run_id>/{edgedata_*.xml, queues.xml, stats.xml, metrics.json}.
"""

import argparse
import itertools
import json
import subprocess
import tomllib
from pathlib import Path

from experiments import transforms
from pipeline.baseline_eval import s7_metrics
from pipeline.common import REPO, sumo_tool
from pipeline.cordon import run_duarouter

# Count-matched demand (pipeline/count_targets.py + routeSampler): reproduces
# the 2019 counted volumes at GEH < 5 on 90.5% of locations. Routes are
# embedded, so scenario runs skip duarouter — transforms move departs and
# change types without altering paths.
BASELINE_TRIPS = REPO / "sim/demand/sampled_sorted.rou.xml"
ADD = REPO / "sim/baseline.add.xml"
SUMO = None  # resolved lazily by sumo_tool (wheel binary or system install)
SCENARIO_DIR = REPO / "experiments/scenarios"

# Scenarios must run under identical physics to the baseline they are compared
# against: same net (A10 actuated signal proxies) and same options as
# sim/baseline.sumocfg (A11 sublane resolution, teleport and blocker handling).
# Keep this block in sync with that config.
SIM_NET = REPO / "sim/net/corridor-calibrated.net.xml"
SUMO_OPTS = [
    "--lateral-resolution", "0.8",
    "--time-to-teleport", "600",
    "--ignore-junction-blocker", "60",
    "--collision.mingap-factor", "0",
    "--collision.action", "warn",
    "--threads", "4", "--no-step-log", "--duration-log.statistics",
]

ABBR = {"p_t": "pt", "dt_minutes": "dt", "school_share": "sch", "b_cap": "bcap"}


def expand(tf_cfg):
    """[(tag, [(transform, params)])]: product over every list-valued param."""
    axes = [(tn, p, v) for tn, params in tf_cfg.items()
            for p, v in params.items() if isinstance(v, list)]
    combos = []
    for values in itertools.product(*[a[2] for a in axes]):
        point = dict(zip([(tn, p) for tn, p, _ in axes], values))
        tfs = [(tn, {p: point.get((tn, p), v) for p, v in params.items()})
               for tn, params in tf_cfg.items()]
        tag = "_".join(f"{ABBR.get(p, p)}{v}" for (_, p), v in point.items())
        combos.append((tag, tfs))
    return combos


def simulate(scenario, run_id, trips_path, outbase=None, mode="micro"):
    outdir = (outbase or REPO / "results" / scenario) / run_id
    outdir.mkdir(parents=True, exist_ok=True)
    if trips_path.suffix == ".xml" and trips_path.name.endswith(".rou.xml"):
        rou = trips_path          # routes already embedded
    else:
        rou = trips_path.parent / f"{run_id}.rou.xml"
        run_duarouter(trips_path, rou)
    # baseline.add.xml hardcodes ../results/baseline_* output paths; per-run
    # copy redirects them into outdir (files then match s7_metrics prefix="")
    add = outdir / "run.add.xml"
    add.write_text(ADD.read_text().replace("../results/baseline_", f"{outdir}/"))
    cmd = [sumo_tool("sumo"), "-n", str(SIM_NET), "-r", str(rou), "-a", str(add),
           "--begin", "21600", "--end", "43200",
           "--statistic-output", str(outdir / "stats.xml"),
           "--queue-output", str(outdir / "queues.xml"),
           "--queue-output.period", "60", *SUMO_OPTS]
    if mode == "meso":
        # Mesoscopic ignores sublane laterals and falls back to static signals;
        # it is the sweep mode (order-of-magnitude faster), with headline points
        # re-run microscopically.
        cmd = [c for c in cmd if c not in ("--lateral-resolution", "0.8")]
        cmd.append("--mesosim")
    done = subprocess.run(cmd, capture_output=True, text=True)
    if done.returncode:
        # capture_output hides SUMO's reason for failing, which turns a one-line
        # diagnosis into a round trip; surface the tail of stderr with the error.
        tail = "\n".join(done.stderr.strip().splitlines()[-15:])
        raise RuntimeError(
            f"sumo failed for {scenario}/{run_id} (exit {done.returncode}):\n{tail}")
    (outdir / "metrics.json").write_text(
        json.dumps(s7_metrics(outdir, prefix=""), indent=2))
    print(f"{scenario}/{run_id}: metrics.json written", flush=True)


def run_baseline(outbase, mode):
    """Unmodified baseline under the same options as every scenario.

    Writes to <outbase>/baseline/ so the result sits at the same depth as every
    scenario run; experiments.collect globs */*/metrics.json, and a baseline one
    level shallower is silently missed, which drops every delta column."""
    outbase.mkdir(parents=True, exist_ok=True)
    simulate("baseline", "baseline", BASELINE_TRIPS, outbase, mode)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config", nargs="?",
                    help="path to a scenario TOML (or use --scenario)")
    ap.add_argument("--scenario",
                    help="scenario name resolved in experiments/scenarios/, "
                         "or 'baseline' for the unmodified demand")
    ap.add_argument("--mode", choices=("micro", "meso"), default="micro",
                    help="meso is the sweep mode; micro for headline runs")
    ap.add_argument("--seeds", type=int,
                    help="use only the first N seeds from the config")
    ap.add_argument("--out", type=Path,
                    help="output base directory (default results/<scenario>)")
    ap.add_argument("--skip-completed", action="store_true",
                    help="skip runs whose metrics.json already exists")
    ap.add_argument("--dry-run", action="store_true",
                    help="stop after writing scenario trips (no duarouter/sumo)")
    args = ap.parse_args()

    if args.scenario == "baseline":
        run_baseline(args.out or REPO / "results/sweep/baseline", args.mode)
        return

    config = args.config or SCENARIO_DIR / f"{args.scenario}.toml"
    with open(config, "rb") as f:
        cfg = tomllib.load(f)
    tf_cfg = cfg["transforms"]
    if tf_cfg == "none":
        tf_cfg = {}

    vtypes, baseline = transforms.read_trips(BASELINE_TRIPS)
    demand_dir = REPO / "sim/demand" / cfg["name"]
    demand_dir.mkdir(parents=True, exist_ok=True)

    seeds = cfg["seeds"][:args.seeds] if args.seeds else cfg["seeds"]
    outbase = args.out or REPO / "results" / cfg["name"]

    for tag, tfs in expand(tf_cfg):
        for seed in seeds:
            run_id = f"{tag}_seed{seed}" if tag else f"seed{seed}"
            if args.skip_completed and (outbase / run_id / "metrics.json").exists():
                print(f"{cfg['name']}/{run_id}: complete, skipping", flush=True)
                continue
            trips, notes = baseline, []
            for tname, params in tfs:
                res = getattr(transforms, tname)(trips, seed=seed, **params)
                if isinstance(res, tuple):
                    trips, summary = res
                    notes.append(f"{tname} summary {summary}")
                else:
                    trips = res
            comment = (f"scenario {cfg['name']} run {run_id}, "
                       f"source sim/demand/baseline.trips.xml, "
                       f"config {config}, transforms {tfs or 'none'}"
                       + "".join(f"; {n}" for n in notes))
            trips_path = demand_dir / f"{run_id}.rou.xml"
            transforms.write_trips(trips_path, vtypes, trips, comment)
            print(f"{cfg['name']}/{run_id}: {len(trips)} trips -> {trips_path}",
                  flush=True)
            if not args.dry_run:
                simulate(cfg["name"], run_id, trips_path, outbase, args.mode)


if __name__ == "__main__":
    main()
