#!/usr/bin/env bash
# Standalone M4 scenario sweep. Builds everything from a fresh clone and runs
# the full experiment grid unattended. Safe to interrupt and re-run: completed
# runs are skipped.
#
#   ./experiments/sweep.sh              # trimmed grid, 1 seed (~30 min)
#   PROFILE=full ./experiments/sweep.sh # complete surface, 24 seeds (~13h)
#   PROFILE=min ./experiments/sweep.sh  # headline points, 1 seed (~15 min)
#
# Timings are for 0.55 loading, where the network is not fighting itself; the
# same grid took many hours when scenarios ran at full demand in collapse.
# 24 seeds is not thoroughness for its own sake: at 3 seeds the spread across
# treatment assignments was as large as the effects being measured.
#   MODE=micro ./experiments/sweep.sh   # microscopic (slow; default meso)
#
# Nohup it and walk away:
#   nohup ./experiments/sweep.sh > sweep.log 2>&1 &
#   tail -f sweep.log
#
# BUILD_ONLY=1 stops after the network, demand and baseline are built, for
# re-running individual scenarios against results that already exist.
set -euo pipefail

cd "$(dirname "$0")/.."
REPO=$PWD
PROFILE=${PROFILE:-trimmed}
# Demand loading. The model has almost no stable congested regime: total
# morning throughput peaks at 50% loading and falls as demand is added, and
# every loading at or above 60% gridlocks by 10:00. 0.55 is the most congested
# loading whose analysis-window hours (08:00/09:00/10:00) all hold - delivered
# 47.2/50.5/32.5% of counted flow, D_net 7,577 veh-h against 3,054 at 50% and
# 65,592 at full demand, and peak-hour delivery the highest of any loading
# tested. Chosen on that criterion, not on maximum throughput: 50% maximises
# throughput precisely by being nearly free-flowing, which is not the regime a
# demand-management study is about.
SCALE=${SCALE:-0.55}
MODE=${MODE:-meso}
RESULTS=$REPO/results/sweep
mkdir -p "$RESULTS"

log() { echo "[$(date '+%F %T')] $*"; }

log "MOD sweep starting: profile=$PROFILE mode=$MODE"

# --- 1. environment -----------------------------------------------------
command -v uv >/dev/null || { echo "uv not found: https://docs.astral.sh/uv/"; exit 1; }
uv sync --quiet
NETCONVERT=$(uv run python -c 'from pipeline.common import sumo_tool; print(sumo_tool("netconvert"))') \
  || { echo "no working netconvert; install SUMO system-wide: sudo add-apt-repository ppa:sumo/stable && sudo apt install sumo"; exit 1; }
SUMO_TOOLS=$(uv run python -c 'import sumolib, os; print(os.path.join(os.path.dirname(os.path.dirname(sumolib.__file__)), "sumo", "tools"))')
[ -f "$SUMO_TOOLS/routeSampler.py" ] || SUMO_TOOLS=${SUMO_HOME:-/usr/share/sumo}/tools
[ -f "$SUMO_TOOLS/routeSampler.py" ] || { echo "SUMO tools not found; set SUMO_HOME"; exit 1; }
log "dependencies ready ($(uv run python -c 'import sumolib; print("sumo", sumolib.version.gitDescribe())' 2>/dev/null || echo 'sumo via eclipse-sumo'))"

# --- 2. network (rebuilt from the committed OSM extract) ----------------
NET=sim/net/corridor-calibrated.net.xml
if [ ! -f "$NET" ]; then
  log "deriving lane counts from carriageway width"
  uv run python -m pipeline.lane_width
  log "building network from data/processed/corridor-laned.osm"
  "$NETCONVERT" --osm-files data/processed/corridor-laned.osm -o sim/net/corridor.net.xml \
    --geometry.remove --ramps.guess --junctions.join --tls.discard-simple \
    --remove-edges.by-vclass pedestrian,bicycle
  "$NETCONVERT" -s sim/net/corridor.net.xml -o sim/net/corridor-filtered.net.xml \
    --keep-edges.by-vclass passenger --keep-edges.components 1
  # netconvert renames joined junctions, so the A10 patch is matched to this
  # network by cluster membership before it is applied.
  uv run python -m pipeline.tls_patch -n sim/net/corridor-filtered.net.xml \
    -o sim/net/tls-patch-resolved.nod.xml
  "$NETCONVERT" -s sim/net/corridor-filtered.net.xml \
    -n sim/net/tls-patch-resolved.nod.xml -o "$NET"
  log "network built"
else
  log "network present, skipping build"
fi

# --- 3. baseline demand (duarouter; ~20 min on first run) ---------------
if [ ! -f sim/demand/sampled_sorted.rou.xml ]; then
  log "building baseline demand + routes (~20 min)"
  [ -f sim/demand/baseline.rou.xml ] || uv run python -m pipeline.cordon
  log "generating count-matched demand (routeSampler)"
  uv run python -m pipeline.count_targets
  uv run python "$SUMO_TOOLS/routeSampler.py" \
      -r sim/demand/baseline.rou.xml -d data/processed/count_targets.xml \
      -o sim/demand/sampled.rou.xml --keep-attributes --seed 20260818
  # SUMO discards vehicles that are out of departure order, silently
  uv run python "$SUMO_TOOLS/route/sort_routes.py" \
      sim/demand/sampled.rou.xml -o sim/demand/sampled_sorted.rou.xml
  log "calibrated demand built"
else
  log "calibrated demand present, skipping build"
fi

# --- 4. baseline run (reference for every scenario delta) ---------------
if [ ! -f "$RESULTS/baseline/metrics.json" ]; then
  log "running baseline"
  mkdir -p "$RESULTS/baseline"
  uv run python -m experiments.run --scenario baseline --mode "$MODE" \
    --scale "$SCALE" --out "$RESULTS/baseline" || log "WARNING: baseline run returned nonzero"
else
  log "baseline metrics present, skipping"
fi

if [ -n "${BUILD_ONLY:-}" ]; then
  log "build complete (BUILD_ONLY): network, calibrated demand, baseline"
  exit 0
fi

# --- 5. scenario grid ---------------------------------------------------
case "$PROFILE" in
  full)    SCENARIOS=(s0-spatial-control s1-school s2-retime-grid s3-joint); SEEDS=24 ;;
  trimmed) SCENARIOS=(s0-spatial-control s1-school s2-retime-grid s3-joint); SEEDS=1 ;;
  min)     SCENARIOS=(s0-spatial-control s1-school s2-retime-grid);          SEEDS=1 ;;
  *) echo "unknown PROFILE=$PROFILE (full|trimmed|min)"; exit 1 ;;
esac

for scenario in "${SCENARIOS[@]}"; do
  log "=== scenario $scenario (seeds=$SEEDS) ==="
  uv run python -m experiments.run \
      --scenario "$scenario" \
      --mode "$MODE" \
      --seeds "$SEEDS" \
      --scale "$SCALE" \
      --out "$RESULTS/$scenario" \
      --skip-completed \
    || log "WARNING: $scenario returned nonzero; continuing"
done

# --- 6. collect ---------------------------------------------------------
log "collecting results"
uv run python -m experiments.collect --results "$RESULTS" \
    --out "$RESULTS/summary.csv" || log "WARNING: collect failed"

log "sweep complete. Summary: $RESULTS/summary.csv"
log "Send back: results/sweep/summary.csv and results/sweep/*/metrics.json"
