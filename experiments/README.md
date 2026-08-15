# Experiments

M4 scenario runs (spec §8): seeded demand transforms applied to the M3
baseline, routed and simulated with the same net and options as
`sim/baseline.sumocfg`, evaluated with the spec §7 metrics.

## Run one scenario

    uv run python -m experiments.run experiments/scenarios/s2-retime-grid.toml --dry-run
    uv run python -m experiments.run experiments/scenarios/s2-retime-grid.toml

`--dry-run` stops after writing the scenario trips files (no duarouter, no
sumo). Any list-valued transform param in the config is a grid axis; the
config expands to the full product, and each grid point runs once per seed
in `seeds`. `run_id` = grid values + seed, e.g. `pt0.1_dt-15_seed101`.

## Outputs

- `sim/demand/<scenario>/<run_id>.trips.xml` — transformed demand;
  provenance (source, config, transform params, seed, mode-shift summary)
  in the header comment.
- `sim/demand/<scenario>/<run_id>.rou.xml` — duarouter routes.
- `results/<scenario>/<run_id>/` — `edgedata_*.xml`, `queues.xml`,
  `stats.xml`, `run.add.xml` (per-run copy of `sim/baseline.add.xml` with
  output paths redirected), `metrics.json` (spec §7).

## Provenance chain

`sim/demand/baseline.trips.xml` (pipeline/cordon.py, see
[pipeline/README.md](../pipeline/README.md)) → `experiments/transforms.py`
(pure, seeded; params from `experiments/scenarios/<cfg>.toml`) → duarouter
(`pipeline.cordon.run_duarouter`) → sumo (options mirror
`sim/baseline.sumocfg`; SUMO's own random seed stays at its default as in
the baseline, so the config seeds vary only the transform sampling) →
`pipeline.baseline_eval.s7_metrics` → `metrics.json`.

## Scenario notes

- `s0-spatial-control`: marker config; the rerouting mechanics are decided
  at run time, so run.py refuses a full run (`--dry-run` works).
- `s1-school`: `school_share` is absent until sized via the A1 profile
  (spec §8 S1: 48% [vol02 p.6-7] is the peak concentration of to-school
  trips, not the school share of peak demand); run.py fails loudly without
  it.
- `s3-joint`: `b_cap` omitted = uncapped; B_cap (A5) is swept in the
  robustness runs, not fixed in the main grid.

Checks: `uv run pytest tests/test_transforms.py -q`.
