# M2 — Model Specification

Internal definitions for the MOD corridor simulation. Every number cites its
source; extraction provenance in [facts-extracted.json](facts-extracted.json)
(page-cited, pulled from `research/library/` documents). Assumptions that are
decisions rather than sourced facts are registered in §9 with resolution
paths. Symbols are defined here once and reused everywhere.

## 1. Zone system

- **Basis:** JICA 2012 50-zone system (wards/VDCs; codes 101–803 grouped by
  municipality: 1xx KMC, 2xx Kirtipur, 3xx Lalitpur NP, 4xx Bhaktapur NP,
  5xx Madhyapur Thimi, 6xx Kathmandu Dist., 7xx Lalitpur Dist., 8xx
  Bhaktapur Dist.) [vol02 §5.1.3 p.5-3; vol04 App 1.1.1].
- **Externals:** person-trip table has destination-only external 901 (4,060
  trips); vehicle tables have external 900 as origin and destination.
  Externals are excluded from `od_2011.parquet` but parseable
  (`extract_od.extract()`); ~23,610 veh/day cross the survey boundary
  [vol02 Table 6.2.3].
- **Corridor zone set** (zones on/adjacent to the study axis, assumption
  A2): 107 (New/Old Baneshwor), 108 (Tripureshwor–Thapathali–Maitighar),
  109 (Teku), 110 (Kalimati), 114 (city core), 119 (Tinkune–Koteshwor–
  Jadibuti, ward 35), 301 (Lalitpur across Bagmati), 502 (Thimi side of
  Jadibuti).

## 2. Study corridor and cordon

- **Axis:** Tripureshwor–Thapathali–Maitighar–New Baneshwor–Tinkune–
  Koteshwor–Jadibuti, plus feeding cross-streets (selection basis:
  paper §5.2).
- **Cordon:** drawn around the corridor zone set; crossing points are
  generation/attraction nodes; corridor sub-OD extracted from the valley
  assignment between crossing points — JICA's own method
  [2017 vol02 §13.4.3.2, Figs 13.4.11–12; verified directly against the
  PDF, logged in research/07-phase0-findings.md verification log — the one
  sourced claim not in facts-extracted.json].
- **Calibration anchors:** the nine 2019 count intersections —
  `counts_2019.parquet`: 77 leg-direction records × 3 metrics = 231 rows
  across 11 intersection sites (Tinkune counted as South/West/North).

## 3. Vehicle classes, PCU, occupancy

Simulation classes match `od_2011.parquet` modes: motorcycle, car, bus,
truck (person_all is used only for person-level reporting, never summed
with vehicle modes).

**PCU (primary set** — JICA 2012 Table 6.2.7, p.6-27; basis: Nepal Road
Standards 2027 BS, motorcycle/bicycle from Vietnamese standards):

| Class | PCU | OD-mode mapping |
| --- | --- | --- |
| Motorcycle | 0.3 | motorcycle |
| Car (taxi 1.0, tempo 1.0 are separate count classes) | 1.0 | car (A8) |
| Bus (large 4.0; minibus 3.0; microbus 1.5) | 4.0 for OD "bus" (A4) | bus |
| Truck (heavy 4.0; light 1.5) | 4.0 for OD "truck" (A4) | truck |

**Sensitivity set** (locally estimated at Koteshwor/Tinkune/Jadibuti — IOE
2014, pp.389–391): motorcycle 0.25, car 1.0, bus 2.19, truck 2.65,
microbus 1.67, tempo 1.3. Robustness runs swap the primary set for this.

**Occupancy (person↔vehicle bridge** — JICA 2012 Table 6.2.2 p.6-19; bus
planning value §6.3.1 p.6-39): motorcycle 1.1, car 1.9, taxi 2.0,
tempo 7.8, light truck 1.8, heavy truck 1.9, **bus 15** (terminal
observations ranged 4.2–32.7 persons/bus, Table 6.3.3 — 15 is JICA's
reconciliation value). Tempo's 7.8 matters if tempos ride inside the OD
"car" mode — see A8.

## 4. Time structure

- **AM peak hour: 09:00–10:00, and it is broad.** Measured vehicle shares
  of daily traffic, pooled over three DoR stations × 3 survey days,
  FY 2024/25, 216 station-day-hours (`pipeline/dor_hourly.py` →
  `data/processed/hourly_profile.parquet`; portal endpoint in
  `pipeline/README.md`): 08:00 5.5%, **09:00 6.8%**, 10:00 6.7%, 11:00
  6.4% — the 08:00–11:00 window carries 19.0% of daily traffic and the
  peak hour is 1.63× the mean hour.
  The clock position agrees with JICA's 2012 road counts (peak 9:30–10:30
  on the Arniko and Tribhuvan highways [vol02 p.6-25]) and with the ~10:00
  institutional start times (paper §4.4). The magnitude does **not** agree
  with JICA's trip-**generation** peak (20% of daily trips in 09:00–10:00
  [vol02 §6.1 p.6-7]; 15–24% per mode, under half before/after [p.6-14]),
  which counts trip starts of all modes including walking and is not a
  vehicle-departure share — do not use it for A1.
- **Simulation window: 06:00–12:00**; 06:00–07:00 warm-up (excluded from
  metrics), analysis window 08:00–11:00. Demand departs in 15-minute
  slices (matches 2019 count resolution), uniform inside each hour.
- **Evening peak: not modeled in v1** — but it is the *larger* peak:
  17:00 carries 7.4% of daily traffic against the AM peak's 6.8%, and
  09:00–18:00 is a 6.0–7.4% plateau (same measurement). The 2012 report is
  itself inconsistent about its evening window (Table 6.2.12 says
  16:00–17:00, Table 6.2.13 says 17:00–18:00, same page 6-35).
- **24h conversions** (for any daily comparisons): 2019 report's stated
  rule is observed+10% [A4-13 §4.2.5]; 6 of 11 sites observed 14.5/14.75h
  rather than 15h and their printed ratios run 1.1017–1.1035 — always use
  the printed `pcu_24h` values from `counts_2019.parquet`, never re-derive.
  2012 day-night ratios 1.07/1.05/1.04 (national/feeder/urban) [p.6-25
  Table 6.2.6].

## 5. Demand construction

1. Seed: `data/processed/od_2011.parquet` vehicle modes (2011 base).
2. Growth: factor per corridor-relevant DoR station from
   `growth_factors.csv` (station→corridor mapping is A3, fixed at M3).
3. Time-slicing: the measured hourly shares of §4 — 06:00–12:00 =
   3.8/4.7/5.5/6.8/6.7/6.4% of daily trips (A1).
4. Corridor sub-OD via the §2 cordon method.

## 6. Supply-side reference values

- Ideal saturation flow: 2,000 PCU/h/lane [vol02 §6.2.3 p.6-34]; local
  alternative model S = 525.88·W PCU/h (W = approach width, R² 0.956)
  [IOE 2014 p.389].
- Link capacities (PCU/day, inside/outside Ring Road): narrow 2-lane
  6,000/7,000; 2-lane 17,000/20,000; 4-lane 52,000/57,000; 6-lane
  75,000/83,000 [vol03 Table 8.2.4a p.8-8].
- BPR function (macro sanity checks only): α=0.48, β=2.82 [vol03 §8.3.4
  p.8-24]. SUMO's own car-following governs the microsimulation;
  driving-behavior parameters transfer from the TU VISSIM calibration
  thesis at M3.
- Fleet-mix sanity anchor: motorcycles ≈70%, cars ≈15% of vehicles at all
  nine 2019 intersections [A4-13].

## 7. Metrics and tolerances

Per run, at the nine calibration intersections and corridor level:

| Symbol | Definition |
| --- | --- |
| d_i | average delay (s/veh) at intersection i, analysis window |
| Q_i | max queue length (m) at intersection i |
| T_c | mean corridor travel time end-to-end (min), by direction |
| H | corridor throughput (PCU crossing cordon, analysis window) |
| t_diss | time from 10:00 until queues dissipate to pre-peak levels; if queues persist at 12:00, record ">120 min (censored)" — if the baseline itself censors, extend the window before running scenarios |
| D_net | total network delay (veh·h) vs free-flow, analysis window |

**Calibration acceptance (M3 exit):** modeled daily leg-direction PCU
volume within **±15%** of `counts_2019.parquet` on ≥ 85% of the 77
leg-direction records, plus a documented qualitative match of queue
locations to the known bottlenecks. The ±15%/85% daily criterion is a
project decision (A7): the conventional GEH < 5 on ≥85% screening
standard (GEH = √(2(M−C)²/(M+C)), M modeled, C counted; ★ UK-DMRB
convention, citation to collect) is defined for **hourly** flows and is
not scale-invariant — applied to daily volumes of this magnitude it would
demand ~2% accuracy, unachievable from a 2011-seeded growth-factored
model. GEH < 5 becomes the criterion if and when the OCR upgrade
(pipeline/counts_2019.py ponytail note; decided at M3 start) yields
hourly counts.

## 8. Scenario parameterization

Symbols (defined once, used everywhere):

- **p_t** — share of targeted peak-hour demand retiming: {0, 5, 10, 15,
  20, 25}% (evidence ceiling: participant-level 10–20%, paper §2.4)
- **Δt** — retiming magnitude: {−15, −30} min (30-min acceptability
  ceiling, Beijing null — paper [26])
- **m** — motorcycle→bus mode-shift share: {0, 5, 10, 15}% of corridor
  motorcycle OD trips in the analysis window, converted via occupancy
  bridge (1.1 → 15), subject to **B_cap** (denominator aligned with paper
  §5.4 at next paper revision)
- **B_cap** — added bus passengers per corridor-hour; scenario parameter
  (A5), swept in robustness

Named scenarios (paper §5.4): S0 spatial-rerouting control (expected
fail), S1 school-shift — the to-school component of peak demand moves
−60 min; component sized via the A1 profile (note: 48% is the share of
to-school trips that fall in the peak hour [p.6-7], **not** the school
share of peak-hour demand — do not invert), S2 anchored incentive
(p_t × Δt sweep), S3 = S2 + m.

Robustness: demand ±10–20%, behavioral parameters halved, PCU sensitivity
set, B_cap sweep.

## 9. Assumption register

| ID | Assumption | Basis | Resolution |
| --- | --- | --- | --- |
| A1 | Hourly departure profile = the measured DoR shares of §4, applied to every corridor OD cell and uniform inside each hour | **measured**, not assumed (2026-08-16): 216 station-day-hours, 3 stations × 3 survey days, FY 2024/25, `pipeline/dor_hourly.py` | Two residual gaps, both narrowing the peak-shape claim rather than the levels: (a) the three stations are highway/Ring-Road cross-sections, not corridor-interior — no corridor-interior hourly data exists (2019 junction profiles are chart images, §10 / verification log); (b) the counts are both-direction totals, so a tidal profile is flattened — recoverable from the per-direction columns of the same detail pages. Δt = 15/30 min also runs below the profile's hourly resolution. Sensitivity: peak-hour share ±1 pp, and a per-direction profile when extracted |
| A2 | Corridor zone set (§1) | zoning-map figure, image-read | verify against georeferenced zone map during M3 network build |
| A3 | DoR station→corridor mapping for growth factors | not yet chosen | fix at M3 from station locations; document per-link |
| A4 | OD "bus"/"truck" PCU = large-class value (4.0) | OD modes are aggregates; class split unknown | sensitivity with IOE 2014 set (bus 2.19, truck 2.65) brackets it |
| A5 | B_cap value | no PT load data for the corridor | swept, not fixed; EASTS crowding evidence bounds the narrative |
| A6 | Zone table transcribed from raster pages (App 1.1.1 has no text layer) | agent visual transcription; total count matches Table 5.1.4 | ★ spot-verify 5 random zone rows before paper submission |
| A7 | ±15% daily-volume criterion, ≥85% of 77 leg-directions (M3 exit) | no collected source defines a daily-volume screening standard; hourly GEH inapplicable at daily magnitudes | replace with GEH < 5 hourly if OCR yields hourly counts; collect DMRB citation |
| A8 | OD "car" mode composition (whether taxi/tempo ride inside it) unknown | vol04 prints only 4 vehicle OD tables; aggregation not stated | check vol03 demand-model class definitions at M3; occupancy sensitivity (1.9 vs 7.8) if tempo included |
| A9 | S1 school_share = 0.46 of peak-hour trips, sensitivity 0.25 | derived from sourced person-trip values: to-school 19.1% of 3,438,393 daily trips (Table 6.1.5 p.6-5/6) × 48% peak concentration ÷ (20% × total) = 0.459; person-trip level — school trips skew to walking, so the vehicle-trip share is lower | sensitivity run at 0.25; upgrade if a mode-by-purpose split surfaces |
| A10 | Police control at study junctions modeled as actuated signals (sim/net/tls-patch.nod.xml → corridor-calibrated.net.xml): Thapathali, Kalimati, Shahid Gate, Maitighar island entries, Tinkune corners; New Baneshwor's 4 corner TLS joined into one controller | 9 of 10 study junctions are police-controlled [JICA 2012, facts-extracted.json]; SUMO priority junctions deadlock under conflicting saturated flows (baseline: 66,740 jam teleports); gap-based actuation is the nearest SUMO analog to police metering; no numeric signal timings exist as text in the 2019 report (§10) | calibrate green splits/cycle lengths against 2019 turning counts if the OCR upgrade (A7) yields hourly movements; sensitivity on cycle length otherwise |
| A11 | Sublane lateral parameters: motorcycle minGapLat 0.3 m (mid of TU thesis calibrated "Minimum Lateral Distance (Standing) at 0 km/h" 0.2–0.41 m, Table 4-25), latAlignment compact; other classes SUMO defaults (minGapLat 0.6, inside the thesis driving-range calibration 0.6–0.9 m); maxSpeedLat and lcSublane at SUMO defaults (1.0) — thesis has no lateral-speed analogue | thesis calibrated VISSIM at three Kathmandu intersections, not SUMO; VISSIM→SUMO parameter mapping is approximate | --lateral-resolution 0.8 m is a sensitivity run (0.4/1.6 bracket); minGapLat swept over the calibrated range ends 0.2/0.41 |

## 10. Fact provenance

`facts-extracted.json` (this directory) holds all 138 extracted facts with
file + printed page + verbatim quote, produced 2026-08-15 from the local
library PDFs. NOT-FOUND results recorded there are binding: e.g. the 2019
report never prints its PCU conversion factors, and no numeric signal
timings exist as text in it — do not cite either from memory.
