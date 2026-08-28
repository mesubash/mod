# MOD

Travel-demand management on a saturated Kathmandu corridor: a calibrated SUMO
microsimulation testbed, the data it was built from, and the experiments run
on it.

MOD is short for *modification* and *change of direction* — the project began
as a study of spreading traffic in time and ended up measuring which
interventions actually work on this corridor.

## What this repository contains

The corridor runs Tripureshwor to Koteshwor through the Maitighar, Thapathali,
New Baneshwor, Tinkune and Jadibuti junctions. Four demand-side interventions
were tested on one calibrated network: departure retiming, mode shift from
motorcycle to bus, a school-hours shift, and spatial redistribution onto
alternative routes.

## Layout

```text
data/
  raw/          OpenStreetMap extract of the corridor
  processed/    digitised JICA 2011 OD matrices, 2019 classified counts,
                DoR growth factors, measured hourly profile
pipeline/       demand construction and evaluation
  cordon.py           corridor demand: growth-scaled OD, cordon cut, time slices
  count_targets.py    routeSampler targets from the 2019 counts
  lane_width.py       lane counts derived from carriageway width, not markings
  tls_patch.py        signal patch matched to junctions by cluster membership
  baseline_add.py     detector definitions, generated from the junction map
  disruption.py       closures and weather as SUMO additional files
  baseline_eval.py    spec section 7 metrics
  throughput_audit.py delivered flow against counted volume, per hour
experiments/    scenario definitions and the sweep
  transforms.py       the four demand transforms
  run.py              TOML scenario -> demand -> SUMO -> metrics
  sweep.sh            builds network and demand, runs the grid
  paper_figures.py    figures, generated from the runs they describe
  scenarios/          one TOML per scenario
sim/
  net/          junction map, signal patch, network build notes
  *.sumocfg     simulation configurations
results/
  sweep/summary.csv   the collected experiment surface
research/
  paper/        the study written up, with its full limitations record
  product/      what the evidence supports building
  library/      the sources, indexed in library/README.md
specs/          model specification and assumptions A1-A14
tests/          checks on the pipeline's output, not just its execution
```

## Reproducing

Requires [uv](https://docs.astral.sh/uv/) and SUMO 1.27.

```sh
uv sync
./experiments/sweep.sh
```

The script builds the network from the OSM extract, constructs and calibrates
demand, runs the baseline, then the scenario grid. `PROFILE=full` runs all
24 seeds per grid point; the default is a trimmed grid.

Demand matches the 2019 counted volumes at GEH < 5 on 95.2% of the 42 count
locations.

## Reading the results

Scenarios run at 0.55 demand loading. The network has no stable congested
regime: total morning throughput peaks at 50% loading and falls as demand is
added, and at 60% and above it gridlocks inside the analysis window. Results
taken past that tipping point reverse the sign of the rerouting effect.
`pipeline/throughput_audit.py` reports delivered flow against counted volume
for any run directory.

Absolute delay levels are not field predictions. The study's limitations are
recorded in full in `research/paper/`.

## Licence

Code is MIT (`LICENSE`). The datasets under `data/` are not mine to
relicense: the OpenStreetMap extract is ODbL, and the survey and count data
are digitised from JICA and Department of Roads publications. Terms and
provenance for each file are in `DATA.md`.

## Sources

Survey data from JICA (2012, 2019), traffic counts from the Department of
Roads, road geometry from OpenStreetMap, and capacity and carriageway figures
from Nepal Urban Road Standard 2076. Every source used is indexed in
`research/library/README.md`.
