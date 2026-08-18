# Running the M4 sweep on your own machine

Self-contained: clone the repo, run one script, send back two files. No Claude
session involved.

## Requirements

- Linux or macOS, ~4 CPU cores, ~20 GB free disk
- [uv](https://docs.astral.sh/uv/) — everything else (SUMO included) installs
  from the committed lockfile
- No internet needed after `uv sync`

## Run it

```bash
git clone <your-repo-url> mod && cd mod
nohup ./experiments/sweep.sh > sweep.log 2>&1 &
tail -f sweep.log
```

Profiles (pick with `PROFILE=`):

| Profile | Runs | Rough time | What it gives |
| --- | --- | --- | --- |
| `min` | ~25 | ~3 h | S0–S2 at evidence-relevant points only |
| `trimmed` (default) | ~70 | ~8 h | full grid, 1 seed interior |
| `full` | ~190 | ~22 h | full grid, 3 seeds everywhere |

`MODE=micro` switches from mesoscopic to microscopic (10–50× slower; use only
for headline points once the sweep is in).

The script is resumable — interrupt it, re-run it, and completed runs are
skipped. It rebuilds the network and demand on first run (~30 min), then
simulates.

## What to send back

```text
results/sweep/summary.csv          # one row per run, metrics + deltas vs baseline
results/sweep/*/*/metrics.json     # per-run detail (optional but useful)
sweep.log                          # so failures are diagnosable
```

`summary.csv` alone is enough to write up the results.

## If something fails

The script continues past a failing scenario and logs `WARNING`. Common cases:

- `uv not found` — install uv, re-run.
- `netconvert: command not found` — `uv sync` did not complete; re-run it.
- A scenario errors immediately — check `sweep.log` for the traceback; the
  other scenarios still run, so let it finish and report what failed.
- Out of disk — each run writes edge data; `min` profile needs least.

## What the runs mean

Scenarios and parameters are defined in `experiments/scenarios/*.toml` and
explained in `specs/model-spec.md` §8. In short: `s0` is the falsification
control, `s1` the school-timing shift, `s2` the departure-time retiming grid
(share × magnitude), `s3` retiming combined with motorcycle→bus mode shift.
