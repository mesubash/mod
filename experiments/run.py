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

from experiments import transforms
from pipeline.baseline_eval import s7_metrics
from pipeline.common import REPO
from pipeline.cordon import NET, run_duarouter

BASELINE_TRIPS = REPO / "sim/demand/baseline.trips.xml"
ADD = REPO / "sim/baseline.add.xml"
SUMO = REPO / ".venv/bin/sumo"

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


def simulate(scenario, run_id, trips_path):
    outdir = REPO / "results" / scenario / run_id
    outdir.mkdir(parents=True, exist_ok=True)
    rou = trips_path.parent / f"{run_id}.rou.xml"
    run_duarouter(trips_path, rou)
    # baseline.add.xml hardcodes ../results/baseline_* output paths; per-run
    # copy redirects them into outdir (files then match s7_metrics prefix="")
    add = outdir / "run.add.xml"
    add.write_text(ADD.read_text().replace("../results/baseline_", f"{outdir}/"))
    subprocess.run(
        [str(SUMO), "-n", str(NET), "-r", str(rou), "-a", str(add),
         "--begin", "21600", "--end", "43200",
         "--statistic-output", str(outdir / "stats.xml"),
         "--queue-output", str(outdir / "queues.xml"),
         "--queue-output.period", "60",
         "--threads", "4", "--no-step-log", "--duration-log.statistics"],
        check=True, capture_output=True, text=True)
    (outdir / "metrics.json").write_text(
        json.dumps(s7_metrics(outdir, prefix=""), indent=2))
    print(f"{scenario}/{run_id}: metrics.json written")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--dry-run", action="store_true",
                    help="stop after writing scenario trips (no duarouter/sumo)")
    args = ap.parse_args()

    with open(args.config, "rb") as f:
        cfg = tomllib.load(f)
    tf_cfg = cfg["transforms"]
    if tf_cfg == "none":
        tf_cfg = {}
    if cfg.get("reroute_control") and not args.dry_run:
        raise SystemExit("S0 rerouting mechanics are decided at run time (M4) "
                         "and not implemented; only --dry-run works")

    vtypes, baseline = transforms.read_trips(BASELINE_TRIPS)
    demand_dir = REPO / "sim/demand" / cfg["name"]
    demand_dir.mkdir(parents=True, exist_ok=True)

    for tag, tfs in expand(tf_cfg):
        for seed in cfg["seeds"]:
            run_id = f"{tag}_seed{seed}" if tag else f"seed{seed}"
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
                       f"config {args.config}, transforms {tfs or 'none'}"
                       + "".join(f"; {n}" for n in notes))
            trips_path = demand_dir / f"{run_id}.trips.xml"
            transforms.write_trips(trips_path, vtypes, trips, comment)
            print(f"{cfg['name']}/{run_id}: {len(trips)} trips -> {trips_path}")
            if not args.dry_run:
                simulate(cfg["name"], run_id, trips_path)


if __name__ == "__main__":
    main()
