# Temporal and Mode-Shift Travel-Demand Distribution for a Saturated Urban Network: A Feasibility Study for Kathmandu Valley

**Project MOD — feasibility and research-design paper**
Draft v1.4 · 2026-08-19 · status: working draft for supervisor/committee review; §5.1, §5.3, §5.6 and §8 report the M3 calibration outcome (count-based demand generation, and the network-throughput limitation that follows from it); §6 reports the M4 scenario sweep

All claims cite numbered references (§References); bracketed numbers [n]
throughout. Sources marked **[local]** are held in
[`research/library/`](../library/README.md). Claims that could not be
independently verified are confined to §8 (Limitations) and marked ★.

---

## Abstract

Kathmandu Valley's peak-period congestion is officially quantified and
worsening, while its adopted remedies are either physical and slow
(infrastructure master plans with multi-decade horizons) or individual and
network-blind (journey planners). This study asks which demand-side lever, if
any, is feasible and credible for a student-scale research project. A
three-part gating investigation was conducted: (G1) data availability, (G2)
overlap with the draft 2026 Kathmandu Valley Urban Transport System Master
Plan, and (G3) the causal structure of corridor congestion. G1 passed: a
defensible corridor origin–destination (OD) demand model can be built
entirely from public data — the JICA 2012 50-zone OD matrices [8],
Department of Roads AADT time series [12], and JICA 2019 classified
intersection counts [10]. G2 passed conditionally: no traveler-facing
demand-management component appears in any account of the draft plan [15–20],
though the full document remains unreleased. G3 **falsified the project's
original hypothesis**: spatial route redistribution is not viable inside the
Ring Road because all screenline crossings already exceeded capacity in 2012,
parallel alternatives are the most oversaturated links in the network
(V/C 2.70–2.76) [9], and every major intersection operates above saturation
(up to X = 2.27) [9]. The evidence instead supports a pivoted hypothesis,
now stated on a measured rather than an assumed demand profile: Department
of Roads hourly counts at three valley stations put the AM peak hour at
6.8% of daily traffic, the 08:00–11:00 window at 19.0%, and the PM peak
above the AM peak [52]. The morning peak's *position* (~09:00–10:00) is the
coordination artifact of institution start times synchronized at ~10:00
[27,28]; its *height* is modest. Departure-time incentives have nonetheless
worked on baselines of comparable mildness — Stanford CAPRI's peak hour
held 38.2% of its 3-hour monitoring window against this corridor's 35.8%,
and cut participants' peak-hour travel by 21.2% [38] — alongside Bangalore
INSTANT [22], Singapore INSINC [23] and Dutch Spitsmijden [21], within
honest bounds: shifts ≤ ~30 minutes [26], 5–10% corridor-level peak
reduction as an upper bound [23,25], and an arithmetic ceiling of 6.8% from
levelling the measured 08:00–11:00 window outright. A simulation study was
built on that basis and run: 66 mesoscopic runs over a sensitivity surface in
retiming share, shift magnitude and motorcycle→bus mode shift, plus the
government's own unquantified 2020 school-timing proposal [29,30] and a
spatial-redistribution control, all evaluated at the verified binding
intersections (§6). Mode shift is the only lever that reduces network
delay: shifting 5%, 10% and 15% of corridor motorcycle trips to bus cuts
network delay by 2.73%, 5.17% and 7.91% while removing 1.98%, 3.97% and
5.94% of vehicles, an amplification of 1.33× stable across the range, and
departure retiming instead raises network delay monotonically, from +0.49%
at 5% retimed to +1.70% at 25% (Δt = −15 min) and +3.56% at Δt = −30, while
spatial redistribution moves network delay by under 0.2% at every share
tested and costs up to 1.87% of corridor throughput. The superlinear regime
H1 predicted is therefore real but reaches the network through demand
reduction, not through the retiming lever the pivot was built on; the
school-timing proposal is the worst intervention tested, at +10.5% network
delay. The methodological contribution is
a reusable sparse-data corridor demand pipeline and an open corridor testbed
for a motorcycle-dominant city, delivered with its demand calibrated to the
2019 counts (GEH < 5 at 90.5% of 42 count locations) and with one measured
limitation carried openly: the microsimulation inserts about half the
throughput those counts record, so scenario findings are reported as
relative effects against a baseline run under identical model settings, not
as absolute delay predictions (§5.6).

---

## 1. Introduction

### 1.1 Motivation

Kathmandu's congestion carries an estimated economic cost of ~NPR 116
billion per year [13]. JICA's 2026 planning figures put east–west corridor
loads at 150,000–200,000 passengers/km against a ~100,000/km ceiling for
road-based transit [15]. Yet as of 2026, traffic for more than 2 million
registered vehicles is still managed "largely through hand signals and
whistles" [19]; only 35 of 64 traffic signals in the valley were functional
in April 2025, and the few operational smart signals cover ~5 intersections
in Lalitpur [14].

The formal response is the *Kathmandu Valley Urban Transport System Master
Plan* (draft final unveiled August 6, 2026; horizon 2050) — 22 infrastructure
projects and 13 transport-improvement programmes [15,16]. Its remedies are
physical and institutional, with lead times of years to decades, and its two
predecessors (2012, 2017) were never implemented [16]. The 2014 ADB-financed
route-restructuring plan was never approved [33]. Meanwhile every deployed
navigation or journey-planning tool available to a Kathmandu traveler —
Google Maps, Sajha Plus, LocaGo, and the academic planner of [11] — optimizes
the individual trip and is structurally blind to collective effects.

Between the slow physical layer and the network-blind individual layer lies
an unoccupied middle layer: **shaping when and how people travel on the
network that exists today**. Google's July 2026 *Nature Cities* study [1]
demonstrated for the first time at scale that coordinated, small
interventions in individual routing decisions measurably reduce citywide
congestion — in GPS-rich US cities. Whether any demand-shaping layer is
feasible in a data-sparse, semi-formal, motorcycle-dominant network is an
open question, and Kathmandu is a hard, representative test case.

### 1.2 The project and its epistemic history

MOD ("modification / change of direction") began with the hypothesis that
*spatial* redistribution — steering travelers onto underused parallel routes —
could relieve Kathmandu's corridors. This paper reports, transparently, that
a structured gating investigation **falsified that hypothesis** for the
saturated core (§4.2) and redirected the project toward temporal and
mode-shift demand distribution (§4.4). We consider the falsification itself
a result: it is evidence-based, citable, and it prevents a simulation study
built on a premise the data contradicts.

### 1.3 Contributions

1. **A negative result**: documentary falsification of intra-Ring-Road route
   redistribution as a congestion lever (§4.2), grounded in JICA screenline
   and saturation data [8,9].
2. **A gap analysis** against the draft 2026 Master Plan and all deployed
   systems, establishing that a *traveler-facing* demand layer is claimed by
   no existing or planned system (§4.3) [15–20].
3. **A feasible data pipeline** for corridor OD demand in a city without
   telemetry, assembled entirely from verified public sources (§5.1)
   [8,10,12].
4. **A research design and its outcome**: a falsifiable simulation study of
   temporal + mode-shift demand distribution with named, locally-legitimized
   policy scenarios (§5.3–5.5), run over 66 scenario runs, of which the
   retiming lever and the spatial control both return negative results and
   mode shift returns a 1.33× amplified delay reduction (§6).

## 2. Background and Related Work

### 2.1 Kathmandu planning context

The valley has been planned repeatedly: JICA's 2012 household survey (18,100
households) diagnosed chronic congestion, weak public transport, and
disorderly urbanization [8]; the 2017 JICA master plan proposed a staged
road/transit program including a travel-demand-management (TDM) menu (Table
8.4.1: cordon charging, parking charges, park-and-ride, pre-trip
information) [9-v1]; UNESCAP (2022) reviewed decades of prior plans and
found public transport still inadequate [34]. The 2014 ADB KSUTP
public-transport restructuring (a 3-tier hierarchy) **was never approved**,
per ADB's own project completion report [33] — implementation, not design,
is Kathmandu's documented failure mode. The 2026 draft Master Plan
[15,16,17] continues the physical/institutional tradition; officials at its
unveiling conceded prior versions went unimplemented [16].

### 2.2 Kathmandu congestion research

Corridor and intersection studies (collected in [library/](../library/README.md)):
the Maitighar–Tinkune bottleneck study measured 6,465 capital-hours lost per
working day, attributed >70% of the loss to buses, and found 78–80% of
bikes/cars travel straight through the corridor [2]. Thapathali intersection
operates at LOS F with 99.6 s/veh average delay; SIDRA-modeled
reconfiguration alone cuts delay ~76% [3]. New Baneshwor reached saturation
degree 2.27 in the evening peak already in 2012 [9]; lane reallocation alone
yields only 5–19% delay relief there [4]. Roadside-friction analysis found
only "entry of vehicles" statistically significant for mid-block speeds
(max ~14% speed penalty) [5]. Reversible-lane simulation on
Jadibuti–Koteshwor cut worst queues >50% but average travel time only ~11%
[6]. Bus dwell studies attribute boarding delay to cash fares (+1.39 s/pax)
and crowding [7]. Signal-control research exists (SUMO-based RL framework
[13b]) but addresses supply, not demand.

### 2.3 Deployed systems

Sajha Plus (single-operator GPS tracking), Mero Sajha, LocaGo (route
lookup), and Google Maps are deployed and individual-trip-scoped [37]. No
maintained GTFS feed exists; an academic GTFS construction (2020) never
published its data [35]. Public-transport routes survive digitally as OSM
route relations [36].

### 2.4 International demand-management evidence

**Departure-time incentives.** The Dutch Spitsmijden experiments paid
recruited peak drivers €2–7 per avoided peak trip: participant peak trips
fell 50–61% in the strongest corridors, with the response dominated by
retiming rather than mode change — and behavior reverted when payments
stopped [21]. Bangalore's INSTANT program (Infosys campus, ~14,000
commuters) used raffle-based credits for pre-8:00 arrivals: pre-peak
arrivals doubled and average bus commutes fell 71→54 minutes, for a total
reward outlay of ~US$1,920 over six months [22]. Singapore's INSINC (rail)
shifted 7.49% of participant peak trips (10.1% among frequent peak riders)
[23]; the parallel Free Pre-Peak Travel policy contributed to a 7–8%
system-level AM-peak reduction and a peak:pre-peak ratio drop from 2.7 to
2.1 at CBD stations [25]; Singapore is reintroducing free pre-peak rides in
Dec 2025 [24]. Stanford CAPRI found participants 21.2%/13.1% less likely to
travel in AM/PM peaks [38]. The Beijing pre-peak fare discount is the
canonical null: a 30% discount before 7:00 produced "no discernible
reduction of peak demand" after a year — the window was placed too early;
~30 minutes appears to be the maximum acceptable retiming [26].

**What these programs started from.** Effect sizes are only interpretable
against baselines, and most of this literature does not publish one. Three
documents do. CAPRI defines a "peak-hour trip ratio" and measures
Stanford-wide AM traffic at 30.2 / 38.2 / 31.6% across 07:00–08:00 /
08:00–09:00 / 09:00–10:00 — a 1.21–1.27× peak-to-shoulder ratio [38].
INSINC reports a participant peak-hour share of 37.1% of 05:00–12:00 trips,
inside a worked example, and separately that "over 76% of morning peak
trips are due to just 20% of commuters" [23]. INSTANT gives only the
complement, the share departing before 07:30 falling from 29% (2005) to 16%
(2007) [22]. The Spitsmijden compilation, the Berkeley comparison and the
FHWA compendium state no baseline concentration for any program [21], and
**no document in this collection states a peak-to-base ratio, a peak factor,
or a sharp-versus-flat characterization of its baseline curve** — a claim
that these programs flattened *sharp* peaks would be unsupported by the
sources (★ §8). Spitsmijden does report that peak *width* predicts
response: participants shifted departure time 35% of the time against a
2-hour peak window (Zoetermeer) but 15–16% against 4-hour windows, and
states that departure-time shifts are "not as popular in experiments that
specify a longer peak period, such as 0600-1000" [21].

**Mode-shift interventions.** Across three Swedish field experiments
(n > 32,500), informational and social-norm nudges produced a tightly
estimated zero effect on public-transport uptake, while an extended
free-trial incentive produced significant, durable uptake concentrated among
prior low-users [31]. Motorcycle-heavy cities: 20% of Jakarta's early BRT
ridership came from private vehicles (6% from motorcycles) [39]; Khon Kaen
stated-preference work finds motorcycle users *more* willing than car users
to shift to BRT, with travel time the binding attribute [40]. A Kathmandu
stated-preference study reports 72.2% of motorcycle users willing to shift
to improved public transport [32] — a ceiling, not a forecast (★ §8).

### 2.5 Theory

Wardrop's user-equilibrium vs system-optimum distinction [41] and Braess's
paradox [42] ground the individual-vs-collective framing; Vickrey's
bottleneck model and its logit extensions [43] make departure-time choice
analytically tractable — an incentive enters as a negative toll, giving
closed-form sanity checks for simulation. Google's 2026 experiments [1]
provide the empirical demonstration that small coordinated shifts in
individual decisions produce measurable network effects.

## 3. Problem Statement and Research Questions

**Problem.** Kathmandu's AM peak falls in a window fixed by synchronized
institutional start times (~10:00 for government offices, schools, banks)
[27,28], onto a network whose binding intersections already operate at
saturation degrees of 1.0–2.3 [9], with no spare parallel capacity [9] and
no planned traveler-facing demand instrument [15–20]. Measured hourly
counts show the peak is broad, not narrow: 6.8% of daily traffic in the AM
peak hour against a 6.0–7.4% plateau from 09:00 to 18:00 [52]. That shapes
the problem twice over — the corridor is loaded near its peak level for
most of the working day, and the room available to departure-time shifting
is bounded, at 6.8% of peak-hour traffic if the 08:00–11:00 window were
levelled outright (§5.1).

**Primary research question (RQ1).** By how much does network performance
(delay, queue length, throughput) at the binding intersections of a
Kathmandu study corridor improve when p% of peak demand retimes by Δt ≤ 30
minutes, with and without a capacity-constrained motorcycle→bus mode-shift
share m% — and is there a nonlinear ("queue-collapse") regime where small
demand cuts yield disproportionate relief?

**RQ2.** What is the minimum participation (compliance threshold) at which
the intervention produces a measurable network effect?

**RQ3.** What would the government's 2020 school-timing proposal
(10:00→9:00) [29,30] have done to corridor performance — the first
quantification of an already-proposed Nepali policy?

**RQ4.** How sensitive are results to demand uncertainty (±10–20%), to the
2012→present OD-pattern drift, and to transferred (non-local) behavioral
parameters?

**Hypothesis (H1, pivoted).** On a corridor whose intersections operate
above saturation, retiming 10–20% of a targeted peak population by ≤30
minutes reduces peak-hour delay at binding intersections nonlinearly (more
than proportionally to the demand removed), at zero individual travel-time
cost (retiming is a schedule cost, not a route cost). The measured profile
makes H1 harder to satisfy, not easier: superlinear relief comes from the
network crossing out of oversaturation, and a 09:00–18:00 demand plateau
[52] points to continuous rather than transient oversaturation, under which
deterministic queueing gives delay roughly proportional to the integral of
excess demand. H1 is falsifiable: if
simulated relief is proportional or negligible, or the required compliance
is impractical (§RQ2), the hypothesis fails and the negative result stands.

**H1 outcome: partially supported, and the half that fails is the half the
pivot was built on (§6).** The superlinear regime exists. Removing demand
from the analysis window returns delay relief larger than the demand
removed, by a factor of 1.33 that is stable from 2% to 6% of vehicles
removed (§6.2). But it is reached by motorcycle→bus mode shift, which
removes vehicles from the window, not by retiming, which moves them within
it. Retiming raises network delay at every share and both shift magnitudes
tested, monotonically in both (§6.3), so the departure-time instrument the
pivot named as its lever is falsified on this corridor under this model.
The spatial control S0 reproduces the §4.2 documentary falsification inside
the model (§6.4), and RQ3's school-timing proposal is the largest
degradation measured (§6.5). RQ2 has no compliance threshold to report for
retiming, because no retiming share produces a benefit to threshold.

**Explicit non-goals.** No intra-Ring-Road spatial rerouting (falsified,
§4.2); no interventions requiring authority/operator cooperation to function
(documented institutional failure mode [33,16]); no valley-wide claims; no
production deployment.

## 4. Evidence Analysis

### 4.1 Data feasibility (gate G1 — PASS)

Verified against local copies (§References, [local] items):

- **OD demand**: the JICA 2012 survey publishes a full 50×50 person-trip OD
  matrix and per-mode vehicle OD matrices (motorcycle, car, truck, bus) as
  text-extractable tables (Vol 4) [8]. Extraction was verified directly
  (`pdftotext -layout` recovers clean matrices).
- **Growth factors**: Department of Roads AADT time series, 29 valley/rim
  stations, FY 2011/12–2024/25, scraped into CSV with per-year hourly-detail
  endpoints [12]. Caveat: some stations show implausible year-over-year
  jumps (e.g., Satdobato 5,275→20,735 AADT in one year) — per-station
  sanity filtering is mandatory (§8).
- **Corridor extraction method**: JICA's 2017 report documents a cordon-based
  corridor-OD extraction (§13.4.3.2, Figs 13.4.11–12) [9-v2] — the exact
  procedure a corridor study needs, pre-demonstrated on
  Thapathali–Maitighar.
- **Calibration ground truth**: JICA 2019 provides 15-hour classified
  directional turning-movement counts (15-min intervals, 9 vehicle classes)
  at nine intersections spanning the Tripureshwor–Koteshwor–Jadibuti axis,
  with signal timings and queue lengths [10].
- **Network**: OSM valley coverage rests on the Open Cities Kathmandu
  systematic mapping (3,716 km of roads) [36] and sustained community
  maintenance; corridor attributes (lanes, signals) require a manual audit
  pass (§7).
- **Local micro-behavior**: a TU/IOE thesis provides GA-calibrated VISSIM
  driving-behavior parameters for Kathmandu's heterogeneous traffic,
  transferable to SUMO [44].

### 4.2 Falsification of spatial redistribution (gate G3 — FAIL for original H)

Three independent, verified data points close the case for the saturated
core:

1. JICA 2012 screenlines: "at all the river sections, traffic volume
   exceeded the capacity"; the parallel minor bridges are the *most*
   oversaturated links in the survey — Kalo Pul V/C 2.76, Bhatkeko Pul 2.70
   [8].
2. JICA 2017 assignment: base-year average V/C inside the Ring Road = 1.22;
   only ~25% of road length below 0.75 [9].
3. All ten major intersections surveyed exceeded saturation in 2012 —
   New Baneshwor X = 2.27 (evening), Kalanki 1.99, Thapathali 1.89 —
   values verified against Table 6.2.12 directly [9]. Nine of the ten were
   police-controlled.

With alternatives more saturated than main corridors and ~80% of corridor
traffic passing straight through [2], there is nowhere to redistribute *to*.
Intersection saturation, not link choice, binds the network. (Data vintage
caveat: §8.)

### 4.3 The gap survives, rephrased (gate G2 — conditional PASS)

Across all located coverage of the draft 2026 Master Plan (≈12 English and
Nepali sources), no programme involves congestion pricing, TDM, traveler
information, or any demand-redistribution mechanism [15–20]; the plan's ITS
content is supply-side (coordinated signals, CCTV, sensors, a central
control system, >NPR 1bn) [18]. The gap MOD targets must therefore be
phrased precisely: **a live, traveler-facing demand layer** — not "no ITS."
Two caveats: the full plan document is unreleased (watchlist [45]), and its
2017 predecessor contained a TDM menu [9-v1], so an unreported TDM chapter
is possible (★ §8).

### 4.4 Why temporal + mode shift is the credible pivot

- **Structure — the peak's position is synchronized; its height is not
  extreme.** Kathmandu's government offices run 10:00–17:00 (summer) [27];
  schools cluster at ~10:00 [29]; banks ~10:00. The road counts agree on
  *when* the resulting peak falls, twice and 13 years apart: JICA's 2012
  counts put it at 9:30–10:30 on the Arniko and Tribhuvan highways [8], and
  the 2025 DoR counts put the two highest AM hours at 09:00 (6.8%) and
  10:00 (6.7%) [52]. They do not support calling it sharp. The earlier
  draft of this paper did, on the strength of JICA's 20% trip-*generation*
  peak [8]; that statistic counts trip starts of all modes including
  walking and is not a vehicle-departure share (§5.1). The claim this study
  now carries is the weaker and measurable one: institutional
  synchronization fixes the peak's clock position, which is what a
  departure-time instrument needs in order to have a target, while the
  peak's height sets how much that instrument can move.
- **How mild is too mild.** The programs in §2.4 that publish a baseline
  ran on peaks of similar mildness. On CAPRI's own denominator — the
  peak hour's share of a 3-hour window — Stanford was 38.2% and this
  corridor is 35.8%, with peak-to-early-shoulder ratios of 1.27× and 1.23×
  [38,52]; CAPRI still moved participants 21.2% off the peak hour [38]. The
  asymmetry matters more than the level: 08:00 sits 1.23× below the peak
  but 10:00 sits only 1.5% below it, so the corridor has an early shoulder
  to fill and effectively no late one. Every program that moved traffic
  rewarded *earlier* travel [22,23,38], which is the direction this shape
  permits. Against that, Spitsmijden's own comparison warns that wide peak
  windows draw weaker departure-time response [21], and Kathmandu's
  measured profile is a wide-window case.
- **Precedent inside government**: in March 2020 the traffic police and PM's
  Office proposed moving school hours to 9:00 explicitly to cut congestion;
  COVID intervened; it was never implemented or quantified [29,30]. A 2026
  announcement moves government offices to 9:00–17:00 with a 5-day week
  (★ implementation unverified) [28] — potentially a natural experiment.
- **Effect-size honesty**: participant-level retiming of 10–20% is
  achievable under sustained, verified incentives [21,22,23]; ~30 min is
  the acceptable-shift ceiling [26]; 5–10% corridor-level AM-peak reduction
  is the defensible upper bound [23,25]. The measured profile now supplies
  an arithmetic ceiling from the other direction: levelling 08:00, 09:00
  and 10:00 completely removes 6.8% of peak-hour traffic, which lands at
  the bottom of that 5–10% band, and reaching 13.0% would require pulling
  demand back to 07:00 — a two-hour shift, four times the acceptability
  ceiling [26]. Levelling 09:00 and 10:00 alone yields 0.8%, so any design
  that moves trips *later* within the window is not worth simulating. The
  scientific interest is that at V/C ≥ 1.0, queueing theory predicts
  nonlinear returns to small cuts; the flat plateau works against that
  prediction by keeping the network oversaturated between the hours a
  retiming policy can reach. RQ1 tests which effect dominates on this
  corridor, and a negative answer is now a live outcome.
- **Mode shift must be capacity-constrained**: 75% of Kathmandu PT users
  report peak overcrowding [45b]; odd-even episodes twice collapsed on PT
  capacity [46]. Nudges alone move nothing [31]; any modeled shift must
  respect bus supply.

## 5. Methodology and Architecture

### 5.1 Data pipeline (stage 1 — implemented)

```text
JICA 2012 Vol 4 (50×50 person-trip + mode OD)      [8]
        │  pdftotext -layout parse; validated vs printed totals
        ▼
Growth-factor update ── DoR AADT ratios FY11/12→24/25 [12]
        │               (per-station sanity filter; cross-check ATO 2024 [47])
        │
        ├── Departure profile ── DoR hourly detail pages, 3 stations [52]
        ▼
Corridor cordon OD ── JICA 2017 §13.4.3.2 method [9-v2]
        │             (cordon around study corridor; crossing-point OD)
        ▼
Calibration/validation ── JICA 2019 daily leg-direction counts
        │                 (Table 4.1: 77 records, 9 intersections) [10]
        ▼
Time-sliced demand (15-min departure profiles, AM window)
        │
        ▼
Count-matched demand ── count_targets.py → SUMO routeSampler [53] (§5.3)
```

The pipeline is implemented (M1; modules, provenance, and run commands in
`pipeline/README.md`). As-built extraction facts:

- **OD extraction confirmed.** All five printed 2011 tables (person trips
  plus motorcycle, car, truck, bus vehicle trips) parse from
  `pdftotext -layout` output; each matrix is validated against its printed
  row, column, and grand totals before writing. One source discrepancy is
  documented: the person table's printed column totals include an
  unprinted external-zone origin row of 3,636 trips; the four vehicle
  tables match their printed totals exactly.
- **Growth factors are filtered per station.** For each of the 29 DoR
  stations, growth is computed over the longest run of surveys whose
  annualized year-over-year ratios stay within 0.5–2.0; transitions
  outside the band (the Satdobato-type jumps flagged in §4.1) are treated
  as count-method breaks and excluded [12].
- **The departure profile is measured, not assumed (A1).** The hourly
  share of daily traffic now comes from the DoR portal's per-station
  hourly detail pages [52]: three FY 2024/25 stations (Manohara Bridge —
  the corridor's own Arniko Highway crossing, Ring Road Sinamangal,
  Satdobato South), 3 survey days each, 216 station-day-hours
  (`pipeline/dor_hourly.py` → `data/processed/hourly_profile.parquet`).
  The AM peak hour (09:00) carries **6.8%** of daily traffic, 10:00 6.7%,
  the 08:00–11:00 window 19.0%; the PM peak (17:00, 7.4%) is higher than
  the AM peak and 09:00–18:00 is a 6.0–7.4% plateau. This replaced an
  interpolated profile with a 20% peak hour, which had applied JICA's
  person-trip *generation* peak [8, vol02 p.6-7] — the share of daily trip
  *starts* over all modes including walking — as a vehicle-departure
  share. Measured road traffic is about three times flatter. The clock
  position is unchanged and independently corroborated: JICA's own 2012
  road counts put the peak at 9:30–10:30 on the Arniko and Tribhuvan
  highways [8, vol02 p.6-25]. Derivation and consequences in the
  verification log [07-phase0-findings](../07-phase0-findings.md).
- **The 2019 calibration counts are daily-tier only; the OCR question is
  closed.** Only the report's Table 4.1 summary (daily leg-direction PCU,
  77 records) exists as text in the PDF. The 15-minute classified sheets
  went to JICA as spreadsheets and were never printed; hourly volumes
  survive only as small unlabeled line-chart images whose values are line
  pixels, not characters. The OCR method itself passed its control:
  tesseract on the rendered Table 4.1 page matched the text-extracted data
  on 15 of 15 leg-direction rows — the failure is the source, not the
  method (verification log,
  [07-phase0-findings](../07-phase0-findings.md)).

The acceptance criterion changed during M3, and both versions are on the
record. The original (assumption A7,
[model spec §7](../../specs/model-spec.md)) was modeled daily leg-direction
PCU volume within ±15% of the 2019 counts on at least 85% of the 77
leg-direction records, plus a documented qualitative match of queue
locations to the known bottlenecks [2,3]. GEH < 5 had been ruled out at M2
because the GEH screening statistic is defined for hourly flows and is not
scale-invariant: applied to daily volumes of this magnitude it would demand
roughly 2% agreement, unachievable from a 2011-seeded growth-factored
model. A7 was not met, and the reason was structural rather than a matter
of tuning (§5.6). The demand is now generated from the counts themselves
(§5.3), which puts the comparison back on hourly flows and makes GEH the
applicable statistic: the criterion in force is GEH < 5 on at least 85% of
count locations, the conventional screening threshold (★ UK DMRB
convention, §8).

### 5.2 Study network (as built)

**Corridor**: the Tripureshwor–Thapathali–Maitighar–New
Baneshwor–Tinkune–Koteshwor–Jadibuti axis with its cross streets — because
(a) every binding intersection on it is documented with verified saturation
data [9], (b) the 2019 ground-truth counts cover exactly these nine
junctions [10], (c) it hosts the falsification evidence [2], and (d) prior
simulation precedent exists [13b]. Study unit = corridor + feeding network,
per the workspace's network-not-isolated-corridor principle.

**Network build**: an OSM bounding-box extract (27.655–27.715 N,
85.275–85.375 E, retrieved 2026-08-15) [36], converted with SUMO
`netconvert` [50] and filtered to the passenger-connected component:
27,969 edges, 11,355 nodes (`sim/net/`). All 77 count leg-directions are
mapped to network edges. The leg numbering is the 2019 report's own: it
was read from the report's intersection diagrams, and 38 observed-PCU
values printed on those diagrams were checked against the extracted count
data with zero mismatches, so the junction mapping reproduces the report's
numbering, not a convention chosen here [10]. Geometry caveat: OSM is
current, not 2019 — Koteshwor and Jadibuti were grade-separated after the
counts, so those two junctions are compared on cordon-edge volumes, not
turn-level movements.

### 5.3 Simulation architecture (stage 2 — built, in calibration)

- **Platform**: SUMO microsimulation [50]. SUMO has no endogenous
  departure-time/mode choice [48]; both levers are applied **exogenously to
  the demand file** — the honest match to our design, since we transfer
  behavioral response rates from the literature rather than estimating
  local choice models (upgrade path: MATSim coupling [48], or local SP
  survey, §7 M5).
- **Demand injection**: TAZ-based — 16 traffic-assignment zones (8
  corridor zones, 8 external gate groups) spawning demand over 3,284
  weighted source edges. This replaced the first baseline configuration,
  which injected each zone through a single edge and was falsified by
  insertion starvation: 21,288 of 234,760 vehicles entered the network
  over the 6 h window, with the top origin edge assigned about five times
  its lane capacity.
- **Count-matched demand generation (the M3 method change)**: the corridor
  sub-OD carries only the movements the JICA 50-zone system resolves — trips
  between the eight corridor zones and the eight external gate groups —
  while the counted junctions also carry local and through movements that
  zone system does not resolve, which capped modeled leg volumes at about
  a fifth of the counts (§5.6). `pipeline/count_targets.py` therefore
  converts the 38 counted inbound legs into hourly `edgeData` targets
  (407,561 vehicle-entries 07:00–12:00, distributed over the measured A1
  hourly shares). The counts are published in PCU and the 2019 report never
  prints its own PCU factors [10], so the conversion applies the model
  spec's primary PCU set at the fleet mix the report does state (~70%
  motorcycle, ~15% car): 0.96 PCU per vehicle. SUMO's `routeSampler` [53]
  then draws from the routed corridor demand until modeled flows match those
  targets, and `sort_routes` [53] writes the sampled file in departure order.
  This replaces rescaling of the sub-OD, global or per-junction, which would
  have required a growth factor outside the range any DoR station recorded
  between 2011 and 2025 [12] (`results/demand_sanity.md`).
- **Junction control (A10)**: nine of the ten binding junctions were
  police-controlled at survey time (§4.2), and no numeric signal timings
  exist as text in the 2019 report [10]. SUMO priority junctions deadlock
  under conflicting saturated flows, so the police-metered junctions are
  modeled as gap-based actuated signals [51] — the nearest SUMO analog to
  police metering — registered as assumption A10 with a cycle-length
  sensitivity path.
- **Driver behavior (A11)**: SUMO's sublane model [51] with motorcycle
  lateral parameters transferred from the GA-calibrated Kathmandu VISSIM
  thesis [44]: minGapLat 0.3 m, the middle of the thesis's calibrated
  0.2–0.41 m standing lateral distance. The VISSIM→SUMO mapping is
  approximate and is registered as assumption A11, swept over the
  calibrated range ends. Saturation-flow sanity checks against [49].
- **Baseline assignment**: current departure profile + current mode split.
  Paths come from `duarouter` on the corridor sub-OD; `routeSampler` selects
  from those paths against the count targets, so the sampled routes travel
  with each vehicle and every scenario run reuses them unchanged — a
  scenario transform moves departure times and changes vehicle types without
  touching paths, which keeps the scenario-versus-baseline comparison free
  of reassignment noise. Mesoscopic runs are used for demand-side checks,
  microscopic runs for metric extraction. Outcome in §5.6.

### 5.4 Experiment design (stage 3)

Sensitivity surface over three dials, each dimension bounded by evidence:

| Dial | Range | Basis |
| --- | --- | --- |
| p_t: share of targeted population retiming | 0–25% | participant-level results 10–20% [21,22,23] |
| Δt: retiming magnitude | −15 / −30 min (pre-peak) | ~30 min acceptability ceiling [26] |
| m: motorcycle→bus shift share | 0–15% of corridor motorcycle trips in the analysis window, bus-capacity-constrained | [31,39,40]; crowding constraint [45b] |

Named scenarios run on the surface:

- **S1 — School shift**: school-linked trips move −60 min (10:00→9:00
  start), per the 2020 proposal [29,30]. On the measured profile these
  departures land in 08:00–09:00, the one hour of the window materially
  below the peak (5.5% against 6.8% [52]), so the shift is in the right
  direction but into a 1.3-percentage-point trough. RQ3.
- **S2 — Anchored incentive**: p_t of employment-cluster trips retime ≤30
  min (INSTANT design transfer [22]). RQ1/RQ2.
- **S3 — Joint**: S2 + capacity-constrained mode shift m. RQ1.
- **S0 — Falsification control**: spatial-rerouting-only scenario, expected
  to fail per §4.2 — run to demonstrate the negative result in simulation,
  closing the loop on the original hypothesis.

Outputs per run: intersection delay and queue lengths at the nine junctions,
corridor travel time, throughput, time-to-queue-dissipation; compliance
threshold curves (RQ2) read off the surface. Robustness: demand ±10–20%,
departure-profile noise, behavioral-parameter halving (RQ4).

### 5.5 Evaluation criteria

H1 supported iff: delay relief at binding intersections is superlinear in
removed peak demand within the evidence-bounded region of the surface, and
the compliance threshold for measurable effect is ≤ the participation rates
achieved by the cited programs. Otherwise H1 fails and the paper reports
the bound.

### 5.6 Calibration outcome (M3)

The calibration has two halves, whether the model loads the right demand
and whether the network moves it, and they came out differently.

**The original criterion was not met, and the gap was structural.** Against
A7 the modeled leg-direction volumes reached a median of 8% of the ±15%
daily-volume target and 0 of 77 leg-directions passed
(`results/baseline_calibration.csv`). The shortfall decomposed
multiplicatively: 0.51 from insertion (the share of loaded vehicles the
network accepted) times 0.20 from demand allocation, giving 0.10 of
target. The 0.20 term is the binding one and no parameter setting reaches
it: even with perfect insertion, the corridor sub-OD covers only about a
fifth of the traffic the counted junctions carry, because the JICA
50-zone system resolves trips between the eight corridor zones and eight
external gates but not the local and through movements those junctions also
carry. The per-junction ratios in `results/demand_sanity.md` (0.23–1.24)
show the same thing spatially: the deficit is not a scale error, so scaling
cannot fix it.

**Demand is now calibrated to the counts.** With the counts converted to
hourly targets and `routeSampler` drawing against them (§5.3), the modeled
flows reproduce 95% of total counted volume at 42 count locations, with
GEH < 5 at **90.5%** of them (`results/routesampler.log`) — above the
conventional 85% screening threshold (★ §8). This is a stronger basis than
A7, not a relaxation of it. A7 settled for ±15% on daily volumes precisely
because the hourly tier was unavailable; the count-derived targets are
hourly by construction, which is the scale GEH is defined at, and GEH < 5
is a tighter test at these flow levels than ±15%.

**The network carries about half the counted throughput.** Loading the
count-matched demand (176,370 vehicles) into the corridor network inserts
roughly 49% of it (`results/sampled_meso.log`). This persists with every
capacity-side correction the model spec registers in place: actuated signal
proxies for police-metered junctions (A10), the sublane model with
motorcycle lateral parameters (A11), physical vehicle geometry and
forced-gap driving behaviour (A12), and collision logging rather than
vehicle removal (A13). SUMO's junction and car-following model delivers
roughly half the throughput Kathmandu's real junctions achieve at the same
demand. The behaviours that make those junctions work (continuous filtering
through gaps, right-of-way negotiated rather than assigned, several vehicles
abreast in a nominal lane) have no representation in a model built on lanes
and rectangular vehicles. That reading of the measurement, as a limitation
of lane-based microsimulation rather than a residual calibration error, is
marked ★ in §8: no alternative simulator was tested here.

**What this study therefore claims.** Scenario results are reported as
relative effects: each scenario against the baseline run under identical
network, demand, and model settings, on the same sampled routes. Absolute
delay and queue values from this model are not predictions of field
conditions and are not offered as such. The relative comparison stays valid
because the throughput limitation is a property of the model that both arms
share: a scenario transform changes departure times and vehicle types on a
fixed set of routes, so any difference between the two runs comes from the
demand change under test. What the limitation plausibly bounds is the size
of the effect rather than its sign — a network held below its real
throughput sits deeper in oversaturation than the real one, and §3's
deterministic-queueing argument then puts a small demand cut on the flatter
part of the response. Directional findings and the compliance thresholds of
RQ2 survive that; a claimed number of seconds saved per vehicle would not.

## 6. Results

### 6.1 What was run

The sweep is 66 runs: one baseline and 65 scenario runs over S0–S3,
executed by `experiments/sweep.sh` at its trimmed profile. Every run uses
the mesoscopic solver, the calibrated network of §5.2, and the
count-matched demand of §5.3 (182,251 vehicles in the route file, 176,370
loaded inside the 06:00–12:00 simulation window). Routes are fixed: a
scenario transform moves departure times and converts vehicle types, and
never re-routes, so a scenario run differs from the baseline only by the
demand change under test (§5.3, §5.6). Each grid point ran once, at
transform seed 101 (§8, limitation 15).

Metrics are the model spec §7 set over the 08:00–11:00 analysis window.
The headline outcome is D_net, total network delay against free flow; the
secondary outcome is H, corridor throughput across the cordon. Both are
reported as percentage change against the baseline under identical
settings, per the §5.6 relative-effects restriction. The baseline is
D_net = 69,923 veh·h and H = 110,242 PCU. Q_i and t_diss are in the metric
set but empty in these runs: the mesoscopic solver has no queue
representation to read them from (§8, limitation 16).

The grid is S0 at p_r ∈ {5, 10, 20}%; S1 at school_share ∈ {0.25, 0.46}
(A9); S2 at p_t ∈ {0, 5, 10, 15, 20, 25}% × Δt ∈ {−15, −30} min; S3 at
that same retiming grid crossed with m ∈ {0, 5, 10, 15}%. S3 contains
p_t = 0, which isolates the mode-shift lever, and its m = 0 column
reproduces S2, which isolates the retiming lever. Each lever below is read
in that isolated form.

| Lever (isolated) | Setting | D_net (veh·h) | ΔD_net (%) | ΔH (%) |
| --- | --- | ---: | ---: | ---: |
| — | baseline | 69,923 | 0 | 0 |
| Mode shift, motorcycle→bus | m = 5% | 68,017 | −2.73 | −0.07 |
| | m = 10% | 66,308 | −5.17 | −0.61 |
| | m = 15% | 64,392 | −7.91 | +0.59 |
| Departure retiming, Δt = −15 min | p_t = 5% | 70,269 | +0.49 | −0.19 |
| | p_t = 10% | 70,520 | +0.85 | +0.88 |
| | p_t = 15% | 70,597 | +0.96 | +0.25 |
| | p_t = 20% | 70,812 | +1.27 | +0.97 |
| | p_t = 25% | 71,115 | +1.70 | +0.76 |
| Departure retiming, Δt = −30 min | p_t = 5% | 70,262 | +0.48 | +0.74 |
| | p_t = 10% | 70,732 | +1.16 | +1.79 |
| | p_t = 15% | 71,268 | +1.92 | +0.65 |
| | p_t = 20% | 71,830 | +2.73 | +0.94 |
| | p_t = 25% | 72,410 | +3.56 | +1.49 |
| Spatial redistribution (S0) | p_r = 5% | 69,947 | +0.03 | −0.05 |
| | p_r = 10% | 70,052 | +0.18 | −1.32 |
| | p_r = 20% | 69,982 | +0.08 | −1.87 |
| School-timing shift (S1) | school_share = 0.25 | 77,279 | +10.52 | −0.95 |
| | school_share = 0.46 | 84,002 | +20.14 | −1.41 |

Full surface in `results/sweep/summary.csv`; figures from
`experiments/analyse.py`.

### 6.2 Mode shift is the only lever that reduces network delay

Isolated at p_t = 0, converting corridor motorcycle trips in the analysis
window to bus passengers reduces network delay at every share tested:
−2.73% at m = 5%, −5.17% at m = 10%, −7.91% at m = 15%. The response is
close to linear in m over that range. Corridor throughput moves between
−0.61% and +0.59% and is not ordered by m, so the delay reduction is not
bought by moving less traffic.

This is the only lever in the sweep with a negative sign on D_net.
`results/figures/lever_comparison.png` plots all three levers on one axis
of share treated against delay reduction; mode shift is the only curve
above zero.

Two properties of the mechanism bound what the result means. The transform
removes motorcycles and adds a bus per 15 accumulated passengers on the
same OD pair (spec §3 occupancy bridge, 1.1 → 15). At m = 15% that is
10,850 motorcycles removed and 24 buses added, because within a
three-hour window few single OD pairs accumulate a busload; the intervention
is therefore close to pure demand removal in this model, and B_cap was left
uncapped in these runs (§8, limitation 17). The result is an upper bound on
what a bus-capacity-constrained mode shift would deliver, not a forecast of
one.

### 6.3 The amplification is about 1.33× and stable

Net of the buses added, the three mode-shift settings remove 1.98%, 3.97%
and 5.94% of the 182,251 vehicles in the demand file and return 2.73%,
5.17% and 7.91% of network delay, giving amplification factors of 1.37,
1.30 and 1.33. The factor does not grow as the demand cut grows, which is
what a queue-collapse regime would show; it holds flat across a threefold
range of cut sizes.

So the superlinear response H1 predicted is present and measurable, and it
is modest. It is also the smaller half of the finding: the amplification
arrives through demand reduction, and the retiming lever H1 named produces
no amplification at all because it produces no reduction (§6.4). RQ1's
nonlinear regime exists; RQ1's stated instrument does not reach it.

### 6.4 Departure retiming increases network delay, monotonically

Retiming raises D_net at every share tested, and the increase grows with
the share: +0.49% at p_t = 5% to +1.70% at p_t = 25% for Δt = −15 min.
Doubling the shift magnitude doubles the penalty rather than the benefit:
at Δt = −30 min the same grid runs +0.48% to +3.56%.
`results/figures/retiming_response.png` shows both series, and
`results/figures/compliance.png` shows the RQ2 reading, which is that no
participation level in the evidence-bounded range crosses zero.

The measured departure profile explains the sign. Shifting departures
earlier moves load into the 08:00–09:00 shoulder, which already carries
5.5% of daily traffic against the peak hour's 6.8% [52]. On a plateau
there is no sharp peak to flatten, and 1.3 percentage points is the entire
trough the instrument has to fill; past that it is building a second peak.
This is the same arithmetic as §4.4, where levelling 08:00–11:00 outright
was shown to remove at most 6.8% of peak-hour traffic, now with a sign
attached to the residual.

Retiming also does not interact with mode shift. Across the S3 grid the
two effects are additive to within about 0.1 percentage point: at
p_t = 10%, Δt = −15 min, m = 10% the joint run gives −4.32%, against
−5.17% for mode shift alone and +0.85% for retiming alone. Adding retiming
to a mode-shift program subtracts from it.
`results/figures/pareto.png` puts the S2 and S3 runs on schedule cost
against delay reduction: the points that reduce delay are the ones carrying
mode shift, and schedule cost buys nothing on its own axis.

### 6.5 Spatial redistribution changes nothing and costs throughput

S0 diverts a share of peak trips onto the best alternative path avoiding
their mid-corridor edge. Network delay moves +0.03%, +0.18% and +0.08% at
p_r = 5%, 10% and 20%, which is flat and not ordered by p_r. Corridor
throughput falls with the share diverted: −0.05%, −1.32%, −1.87%.

The mechanism is visible in the transform's own accounting. At p_r = 20%,
8,280 peak trips were selected for diversion; 4,954 had an alternative
path avoiding their mid-corridor edge and 3,326, two in five, had none at
all (run provenance in
`sim/demand/s0-spatial-control/p_r0.2_seed101.rou.xml`; the same 60/40
split holds at p_r = 5% and 10%). Of the trips that could divert, the
diverted flow lands on links that carry it more slowly, which is where the
throughput loss comes from. This is the project's original hypothesis, and
the sweep falsifies it a second time: §4.2 falsified it from JICA's
screenline and saturation data, and S0 now falsifies it inside the
project's own calibrated model, on real routes drawn from the calibrated
demand.

### 6.6 The school-timing shift is the worst intervention tested

S1 moves the school-linked component of peak demand 60 minutes earlier,
the 2020 traffic-police and PM's Office proposal [29,30] (RQ3). At the
conservative A9 sensitivity value, school_share = 0.25, network delay
rises 10.52% and corridor throughput falls 0.95%. At the derived
school_share of 0.46 the degradation roughly doubles, to +20.14% delay and
−1.41% throughput.

That is the first quantification of the proposal, and three caveats travel
with it. It is a corridor-scale simulation result under the §5.6
relative-effects restriction, not a valley-wide or field prediction. The
school_share itself is an estimate (A9): 0.46 is derived from JICA
person-trip purpose shares and skews high because school trips skew to
walking, and 0.25 is the registered sensitivity value. And the direction
of the result is the same one §6.4 explains: a −60 minute shift is twice
the largest retiming magnitude in the S2 grid, applied to a larger share of
demand, landing in the same 08:00–09:00 shoulder. S1 is the retiming lever
at its extreme, and it fails in the same direction, harder.

## 7. Development Plan

Internal definitions live in the model spec (M2); technology beyond the
simulation platform is deliberately undecided.

| Milestone | Content | Exit criterion |
| --- | --- | --- |
| M0 — Verification closeout | ★ items: office-hours change implementation [28]; obtain 2 remaining nepjol papers + SMEC report manually [45]; JICA OD license check for open release | each ★ resolved or documented as limitation |
| M1 — Data extraction | Digitize OD matrices [8]; filter DoR growth factors [12]; extract 2019 counts [10] into machine-readable form | QA: matrix totals match printed totals; growth factors pass sanity filter |
| M2 — Model spec | Written internal definitions: zone system, cordon, time slices, vehicle classes/PCU [49], metrics, calibration tolerance (A7), scenario parameterization | spec reviewed against this paper's §5 |
| M3 — Network + baseline | OSM build, corridor audit, calibration, baseline validation | done with a documented limitation (§5.6): demand calibrated to the counts at GEH < 5 on 90.5% of count locations; network throughput limitation recorded, scenario claims restricted to relative effects |
| M4 — Experiments | Surface + S0–S3 + robustness | main surface done (§6): 66 runs, S0–S3, reproducible from `experiments/sweep.sh` + the scenario TOMLs. Outstanding: the three-seed profile (§8, limitation 15), the B_cap sweep (limitation 17), and the RQ4 robustness runs |
| M5 — (Optional) local behavior | Small SP survey on corridor departure-time flexibility (replaces transferred parameters) | n, instrument TBD |
| M6 — Writeup | Results paper; testbed + digitized data released (license permitting) | — |

Sequencing note: M0–M2 require no simulation software; M3 is the first
build step. This ordering preserves the workspace's research-before-code
principle.

## 8. Limitations and Threats to Validity

1. **Data vintage**: the OD pattern is 2011/12 [8]; growth factors correct
   totals, not structural drift (new links, Ring Road widening). Mitigation:
   2019 count calibration [10]; named openly in all claims. The
   falsification evidence (§4.2) is likewise 2012-vintage — demand growth
   since [12] makes *more* saturation likely, but this is inference, not
   measurement. ★
2. **Transferred behavioral parameters**: retiming propensities come from
   the Netherlands, India, Singapore [21,22,23]; no Kathmandu departure-time
   elasticity exists (verified gap). Mitigation: sensitivity halving (RQ4);
   upgrade path M5.
3. **Master Plan unknowns**: the full 2026 document is unreleased; the
   13-programme list is reconstructed from press coverage [15–20]; a TDM
   chapter is possible given the 2017 precedent [9-v1]. ★ Watchlist [45].
4. **Simulation-only**: results say nothing about real adoption; durability
   evidence warns effects decay when incentives end [21] and freed capacity
   partially refills (latent demand) [21]. Claims are corridor-simulation
   claims, not deployment claims.
5. **Semi-formal transit representation**: microbus/tempo services lack
   schedules and GPS; route relations in OSM [36] plus judgment calls —
   documented in M2 — will define "routes."
6. **Stated-preference ceiling**: the 72.2% motorcycle-shift willingness
   [32] is SP, login-walled, and uncorroborated — used only as a ceiling
   argument, never as an input parameter. ★
7. **Single-corridor external validity**: results bind to the study
   corridor; valley-wide generalization is future work.
8. **Calibration tier is daily leg volumes**: the 2019 hourly/15-minute
   counts are unrecoverable — the printed report holds them only as raster
   images and unlabeled charts, and the OCR route is closed after a passed
   method control (§5.1; verification log,
   [07-phase0-findings](../07-phase0-findings.md)). Within-day temporal
   validation therefore rests on the sourced departure-profile anchors
   (A1), not on counted hourly flows.
9. **A10/A11 are structural modeling assumptions**: police control modeled
   as actuated signals, and motorcycle lateral behavior transferred from a
   VISSIM calibration [44] into SUMO's sublane model. Both are registered
   decisions with sensitivity paths (cycle length; lateral-gap and
   lateral-resolution sweeps), not sourced facts
   ([model spec §9](../../specs/model-spec.md)).
10. **Demand-model class coverage**: modeled cordon demand in the analysis
    window was 0.61× what the 2019 counts imply, with per-junction ratios
    0.23–1.24. The gap is structural — the OD vehicle modes carry no
    separate taxi/tempo/microbus (A8), and centroid/gate placement is
    unresolved (A2) — not a growth-factor error: matching the counts by
    scale alone would need a factor outside every DoR station's observed
    2011–2025 range. Documented in
    [results/demand_sanity.md](../../results/demand_sanity.md). This is what
    count-based demand generation answers (§5.3): the counted volumes, not
    the zone system, now set how much traffic each counted leg carries. The
    OD structure still decides *which* paths that traffic takes, so the
    class-coverage and centroid-placement assumptions remain live for route
    composition even though they no longer set volumes.
11. **Simulation calibration was iterative, and the failures are part of
    the record**: three baseline configurations were falsified and
    documented before the current one — single-edge demand injection
    starved insertion (21,288 of 234,760 vehicles), the rebuilt TAZ-based
    demand gridlocked on unsignalized priority junctions, and the sublane
    build then deleted vehicles on minor lateral overlaps (96,225 of 145,191
    teleports were collision removals, A13). Two of the faults produced no
    error message at all, which is worth recording as method rather than
    anecdote, because either one invalidates a result set silently. First,
    SUMO discards vehicles that appear out of departure order in a route
    file; `routeSampler` writes in sampling order, and until the output was
    passed through `sort_routes` [53] this cost 85% of the demand, with the
    run completing normally each time. Second, the evaluator's
    analysis-window share was hardcoded at 0.50 and survived the A1
    correction that moved the measured 07:00–12:00 share to 0.301,
    inflating every calibration target by the ratio between them; it is now
    derived from the demand profile itself, so target and demand cannot
    drift apart again. Both were found by arithmetic on intermediate
    outputs, not by anything the simulator reported.
12. **Network throughput is about half the counted throughput, and this
    bounds what the study reports.** With count-matched demand loaded
    (176,370 vehicles) the simulation inserts roughly 49% (§5.6), with the
    A10–A13 capacity corrections all in place. The measured claim is that
    this configuration of SUMO moves about half the traffic Kathmandu's
    junctions move at the same demand. The wider reading — that this is a
    general limitation of lane-based open-source microsimulation applied to
    non-lane-based heterogeneous traffic, rather than residual calibration
    error specific to this build — is an interpretation and is marked ★: no
    alternative simulator was tested, and no ablation isolates the junction
    model from the car-following model. The consequence for the research
    design is stated in §5.6 and holds either way: scenario results are
    reported as relative effects against a baseline under identical model
    settings, and absolute delay levels from this model are not offered as
    field predictions.
13. **The peak-shape evidence is not corridor-interior.** The measured
    departure profile (A1, §5.1) comes from three DoR stations that are
    highway and Ring-Road cross-sections [52], and the counts used are
    both-direction totals, which flatten a tidal profile; the per-direction
    columns exist on the same pages and are the registered sensitivity
    path. No corridor-interior hourly profile is available: the 2019 JICA
    survey counted hourly flows at exactly the nine study junctions, but
    they survive only as unlabeled line-chart images (limitation 8). The
    two corridor-interior studies that print peak volumes disagree with
    each other and with the stations — Thapathali's weekday AM peak hour
    (5,593 PCU) exceeds its PM peak hour (4,883 PCU) [3], while
    Maitighar–Tinkune's printed evening counts exceed its 09:00–11:00
    morning counts [2] — and neither prints a daily denominator, so
    neither yields a peak-hour share. The corridor-interior AM peak could
    therefore be sharper than 6.8%; how much sharper is unmeasured. ★
    Note that the premise this measurement replaced had no
    corridor-interior support either: it rested on a household-survey
    trip-generation statistic.
14. **The 85% screening threshold is convention, not a collected source.**
    GEH < 5 on at least 85% of count locations is the criterion in force
    (§5.1, §5.6), and the model reaches 90.5%. The threshold is attributed
    to UK DMRB practice; no copy of that standard is held in
    [`research/library/`](../library/README.md), so the attribution is ★
    until the citation is obtained. The measured GEH distribution stands
    regardless of which threshold is applied to it.
15. **One seed per grid point, so the sweep carries no variance estimate.**
    The 66 runs of §6 are the trimmed profile of `experiments/sweep.sh`:
    every grid point ran once, at transform seed 101. Nothing in §6 is an
    average, and no confidence interval can be attached to any number there.
    The differences the paper leans on are large relative to that gap
    (mode shift −2.73% to −7.91%, school shift +10.52%) and the levers are
    monotone in their own parameter across five or six grid points, which is
    harder to produce from sampling noise than a single point difference.
    But the small values are not separable from noise: the S0 deltas of
    +0.03% to +0.18% support "no effect", not an ordering. The full profile
    (three seeds per point) is the registered path.
16. **Mesoscopic runs cannot measure queues or dissipation.** The sweep ran
    in SUMO's mesoscopic mode for tractability, which models links as
    queues with aggregate flow rather than resolving vehicle positions, so
    Q_i (max queue length) and t_diss (time to queue dissipation) from the
    model spec §7 metric set are unavailable and appear empty in
    `results/sweep/summary.csv`. RQ1 is phrased over delay, queue length and
    throughput; §6 answers it on delay and throughput only. The queue-based
    half of the queue-collapse argument in §3 is therefore inferred from
    D_net, not observed.
17. **The mode-shift result is a demand-reduction effect with its capacity
    constraint switched off.** B_cap (A5) is the bus-capacity ceiling in
    §5.4's dial table, and the S3 configuration omits it, so no conversion
    was ever clipped. Compounding this, the transform's busload threshold
    (15 passengers on one OD pair, spec §3) is rarely reached inside the
    analysis window, so m = 15% removes 10,850 motorcycles and returns 24
    buses (§6.2). What §6.2 measures is close to deleting 5.94% of the
    vehicles, and §6.3's amplification is the network's response to that
    deletion. A real motorcycle→bus shift adds bus vehicles to a corridor
    where 75% of PT users already report peak overcrowding [45b]. The
    −7.91% is an upper bound; the B_cap sweep is the registered path to a
    bounded figure.

## 9. Conclusion

Kathmandu's congestion problem, at its saturated core, is a *what-mode*
problem before it is a *when* problem, and it is neither a route-choice
problem. The study falsified two of its own hypotheses to get there. The
original spatial-redistribution hypothesis fell first to the city's own
survey data (§4.2) and then again inside the project's calibrated model,
where diverting up to 20% of peak trips moved network delay by 0.18% at
most and cost 1.87% of corridor throughput (§6.5). The retiming hypothesis
the project pivoted to, H1, fell in the simulation it was built for:
retiming raises network delay at every share and both shift magnitudes
tested, up to +3.56% at 25% retimed by 30 minutes, and the government's own
2020 school-timing proposal, quantified here for the first time, is the
worst intervention in the sweep at +10.52% (§6.4, §6.6). The measured
departure profile had already predicted this. A peak carrying 6.8% of daily
traffic against a 5.5% shoulder is not a peak with room to be flattened,
and a demand plateau running 09:00 to 18:00 leaves a retiming instrument
nowhere to move demand to.

H1 survives in one half. The superlinear regime it predicted is real:
motorcycle→bus mode shift returns delay relief 1.33× the demand it removes,
stably across a threefold range of cut sizes, reaching −7.91% network delay
at 15% of corridor motorcycle trips shifted (§6.2, §6.3). That relief comes
from taking vehicles out of the window, not from moving them within it, and
with B_cap uncapped in these runs it is an upper bound rather than a
forecast (§8, limitation 17). The instrument that works is therefore not
the one the pivot named, and the finding for a demand-management program on
this corridor is that mode shift is worth its cost while departure-time
incentives are not.

What survives beyond the hypotheses is the infrastructure: a feasible,
fully-public-data corridor demand model calibrated to the counted volumes
at GEH < 5 on 90.5% of count locations, a demand-management gap that no
deployed or planned system occupies, and an open corridor testbed for a
motorcycle-dominant city whose own throughput limitation is measured and
stated (§5.6). The results it produced are corridor-scale relative effects
from a single-seed sweep in mesoscopic mode (§8, limitations 15–17), and
they are negative on two of three levers. That is what the study set out to
be able to report.

---

## References

Format: [n] Author/Institution (year). *Title*. Source. — **[local]**
`library/<file>` where held.

### Theory & international

- [1] Google Research (2026). *Urban congestion relief experiments through routing-app interventions*. Nature Cities. <https://www.nature.com/articles/s44284-026-00443-x> — [local] `theory-google-routing-app-congestion-relief-2026.pdf` (+correction)
- [21] Donovan, S. (compilation incl. Bliemer et al. 2010; Ben-Elia & Ettema 2011). *Spitsmijden peak-avoidance experiments, Netherlands*. <https://www.vtpi.org/spitsmijden.pdf> — [local] `pivot-spitsmijden-overview.pdf`
- [22] Merugu, D., Prabhakar, B., Rama, N.S. (2009). *An incentive mechanism for decongesting the roads: a pilot program in Bangalore (INSTANT)*. NetEcon. <https://web.stanford.edu/~balaji/papers/NetEcon_final.pdf> — [local] `pivot-instant-bangalore-netecon.pdf`, `pivot-instant-bangalore-final-report.pdf`
- [23] Pluntke, C., Prabhakar, B. (2013). *INSINC: a platform for managing peak demand in public transit*. JOURNEYS. — [local] `pivot-insinc-singapore.pdf`
- [24] LTA Singapore (2025). *Free morning off-peak rail rides on NEL/SPLRT*. <https://www.lta.gov.sg/content/ltagov/en/newsroom/2025/10/news-releases/free_morning_off-peak_rail_rides.html>
- [25] IPS Commons. *Shifting travel demand* (FPPT: 7–8% AM-peak decrease; peak:pre-peak 2.7→2.1). <https://ipscommons.sg/shifting-travel-demand/>
- [26] Yang, Long et al. (2024). *Travelers' responses to a pre-peak discount fare, Beijing subway*. Transp. Res. A. <https://www.sciencedirect.com/science/article/abs/pii/S0965856424003835>; Zou et al. (2019) J. Adv. Transp. <https://onlinelibrary.wiley.com/doi/10.1155/2019/6873912>
- [31] Gravert, C., Olsson Collentine, L. (2021). *When nudges aren't enough*. JEBO / CEBI WP 10/19. — [local] `pivot-gravert-nudges-incentives-pt.pdf`
- [38] Zhu, C. et al. (2015). *Stanford CAPRI*. TRB. — [local] `pivot-capri-stanford-trb2015.pdf`
- [39] *TransJakarta BRT ridership sources*. Case Studies on Transport Policy (2022). <https://www.sciencedirect.com/science/article/abs/pii/S2213624X22001407>
- [40] *Khon Kaen BRT modal-shift SP study*. IATSS Research. <https://www.sciencedirect.com/science/article/pii/S0386111215000138>
- [41] Wardrop, J.G. (1952). *Some theoretical aspects of road traffic research*. — [local] `theory-wardrop-1952-road-traffic-research.pdf`
- [42] Braess, D. (1968; transl. 2005). *On a paradox of traffic planning*. — [local] `theory-braess-2005-paradox-translation.pdf`, `theory-braess-1968-original-german.pdf`
- [43] Li, Z-C., Huang, H-J., Yang, H. (2020). *Fifty years of the bottleneck model*. Transp. Res. B 139. <https://pmc.ncbi.nlm.nih.gov/articles/PMC7333998/>
- [48] SUMO 2020 conf. *MATSim–SUMO coupling*. — [local] `pivot-matsim-sumo-coupling.pdf`; The MATSim Book <https://matsim.org/the-book/>
- [50] Alvarez Lopez, P. et al. (2018). *Microscopic Traffic Simulation using SUMO*. IEEE ITSC. <https://elib.dlr.de/124092/>
- [51] Eclipse SUMO documentation (used at v1.27.1): sublane model, actuated traffic lights, duaIterate assignment. <https://sumo.dlr.de/docs/>
- [53] Eclipse SUMO calibration tools (used at v1.27.1): `routeSampler.py`, which samples a route set to match counted edge/turn volumes and reports per-interval GEH — <https://sumo.dlr.de/docs/Tools/Turns.html>; `route/sort_routes.py`, which writes a route file in departure order — <https://sumo.dlr.de/docs/Tools/Routes.html>
- Supporting compendia: FHWA HOP-18-071 — [local] `pivot-fhwa-incentives-compendium.pdf`; Berkeley incentives comparison — [local] `pivot-incentives-comparison-berkeley.pdf`

### Kathmandu — official data & plans

- [8] JICA (2012). *Data Collection Survey on Traffic Improvement in Kathmandu Valley* (6 vols; Vol 4 = OD matrices; Vol 2 = screenlines, Table 6.2.12). <https://openjicareport.jica.go.jp/pdf/12082459_01.pdf> — [local] `data-jica-2012-traffic-survey-vol01…06.pdf`
- [9] JICA (2017). *Project on Urban Transport Improvement for Kathmandu Valley*, Final Report (Vol 1 = master plan, V/C assignment, TDM Table 8.4.1 [9-v1]; Vol 2 = cordon method §13.4.3.2 [9-v2]). — [local] `data-jica-2017-urban-transport-vol01/02.pdf`
- [10] JICA (2019). *Data Collection Survey on Urban Transport in Kathmandu Valley*, Final Report (Vol 2 = 15-h classified counts, 9 intersections). — [local] `data-jica-2019-urban-transport-survey-vol01/02.pdf` (dating verified from title page)
- [12] Department of Roads, Nepal. *Traffic counts, ssrn.dor.gov.np* (scraped 29 stations, FY 2011/12–2024/25). — [local] `data-dor-ssrn-aadt-kathmandu-valley-stations.csv`
- [52] Department of Roads, Nepal. *Traffic count station hourly detail*, ssrn.dor.gov.np — per-hour, per-direction, per-class counts for the survey days behind each station-year AADT row; URL pattern `https://ssrn.dor.gov.np/traffic_controller/get_detail/<location>/<id>`, e.g. <https://ssrn.dor.gov.np/traffic_controller/get_detail/Manohara%20Bridge/1582>. Stations 64 Manohara Bridge, 65 Ring Road (Sinamangal), 58 Satdobato South, FY 2024/25, 3 survey days each, retrieved 2026-08-16 via `pipeline/dor_hourly.py` → `data/processed/hourly_profile.parquet`
- [33] ADB (2020). *Kathmandu Sustainable Urban Transport Project — Completion Report* (Loan 2656; restructuring plan not approved). — [local] `masterplan-adb-ksutp-completion-report-2020.pdf` (+ MaYA factsheet)
- [34] UNESCAP (2022). *Comprehensive Public Transport and Mass Transit Plan for Kathmandu Valley*. <https://repository.unescap.org/handle/20.500.12870/6300>
- [45] Watchlist & unobtained items: see `library/README.md` (Master Plan primary doc; INJET 95704/82531; SMEC 2014 restructuring report)
- [47] Asian Transport Observatory (2024). *Kathmandu Urban Transport Profile*. — [local] `data-ato-kathmandu-transport-profile-2024.pdf`
- JICA/MoPIT (2023). *Record of Discussions, KV Urban Transport System Master Plan project*. — [local] `masterplan-jica-record-of-discussions-2023.pdf`

### Kathmandu — studies

- [2] Timalsena, K., Marsani, A., Tiwari, H. (2017). *Impact of Traffic Bottleneck on Urban Road: Maitighar–Tinkune*. IOEGC. — [local] `evidence-maitighar-tinkune-bottleneck-2017.pdf`
- [3] Maharjan, S., Marsani, A. (2023). *Thapathali intersection performance*. IOEGC-13. — [local] `evidence-thapathali-intersection-performance-2023.pdf`
- [4] (2023). *New Baneshwor lane-use restriction (VISSIM)*. IOEGC. — [local] `evidence-new-baneshwor-lane-use-restriction-2023.pdf`; companion signal study — [local] `evidence-new-baneshwor-signal-improvement-2017.pdf`
- [5] Dhimal, S., Marsani, A. (2023). *Roadside friction and mid-block speed*. IOEGC. — [local] `evidence-roadside-friction-midblock-speed-2023.pdf`
- [6] Pradhananga, R. et al. (2021). *Reversible lane system, Jadibuti–Koteshwor*. NJCE. — [local] `evidence-reversible-lane-jadibuti-koteshwor-2021.pdf`
- [7] (2022). *Bus dwell time, Kathmandu*. IOEGC. — [local] `evidence-bus-dwell-time-kathmandu-2022.pdf` (+ bus-bay, bus-stop studies, `evidence-bus-*`)
- [11] (2025). *Optimized graph-based journey planning, Kathmandu Valley*. IJET. <https://nepjol.info/index.php/injet/article/download/78657>
- [13] (2025). *A multi-faceted approach to urban congestion: Kathmandu experience*. JACEM 11. — [local] `evidence-urban-congestion-multifaceted-kathmandu-2025.pdf`
- [13b] (2025). *Framework for AI-driven traffic management in Kathmandu*. Far Western Review. — [local] `evidence-ai-traffic-management-framework-fwr-2025.pdf`
- [32] *Modal shift & transport energy, Kathmandu Valley* (SP: 72.2%). <https://www.academia.edu/56811240/> ★ login-walled
- [44] Manandhar, A. *VISSIM calibration for heterogeneous traffic, Kathmandu (GA)*. TU/IOE thesis. — [local] `data-tu-thesis-vissim-calibration-kathmandu.pdf`
- [45b] Poudyal, Shahi (2025). *PT optimization survey, Kathmandu*. EASTS 15. — [local] `evidence-public-transport-optimization-kathmandu-easts-2025.pdf`
- [49] Shrestha, Marsani (2014). *Saturation flow & delay models, Koteshwor/Tinkune/Jadibuti*. IOEGC. — [local] `evidence-saturation-flow-delay-model-koteshwor-tinkune-jadibuti-2014.pdf`
- KTFT dispersal (2024) — [local] `evidence-ktft-expressway-traffic-dispersal-2024.pdf`; Satdobato — [local] `evidence-satdobato-intersection-injet.pdf`

### Kathmandu — news & policy (secondary sources)

- [14] Signal functionality coverage 2024–26 (OnlineKhabar / Himalayan Times / New Business Age) — see `library/README.md`
- [15] Kathmandu Post (2026-08-06). *New Kathmandu transport master plan…* <https://kathmandupost.com/national/2026/08/06/new-kathmandu-transport-master-plan-proposes-metro-rail-linking-ratna-park-and-bhaktapur>
- [16] Ratopati EN 73392; ekantipur/Karobar mirrors — implementation-gap statements. <https://english.ratopati.com/story/73392/>
- [17] JICA/MoPIT (2023) Record of Discussions — [local], report sequence establishing draft-final status
- [18] Meroauto (2026). *23 key intersections; >Rs 1bn ITS allocation*. <https://www.en.meroauto.com/23-key-kathmandu-intersections-prioritized-in-plan-to-upgrade-107-junctions/>
- [19] Meroauto (2026-08-13). *SSP Kafle: 2M+ vehicles, hand signals*. <https://www.en.meroauto.com/nepal-sets-five-year-deadline-to-digitize-entire-transport-sector/>
- [20] Clickmandu EN 10796/10813; NepalAuto — programme reconstruction, see `library/README.md`
- [27] Government of Nepal office hours (10:00–17:00 summer) — as reported in [28]
- [28] MyRepublica (2026). *Govt sets new office hours 9am–5pm* ★ implementation unverified. <https://myrepublica.nagariknetwork.com/news/govt-sets-new-office-hours-from-9-am-to-5-pm-29-97.html>
- [29] OnlineKhabar (2020). *Govt changing school hours to ease traffic*. <https://english.onlinekhabar.com/govt-changing-school-hours-to-ease-traffic.html>
- [30] The Himalayan Times (2020). *Change in school timing being considered*. <https://thehimalayantimes.com/kathmandu/change-in-school-timing-being-considered>
- [35] (2020). *GTFS for Kathmandu*. JIE. — [local] `data-kathmandu-gtfs-jie-2020.pdf`
- [36] GFDRR. *Open Cities Kathmandu* — [local] `data-gfdrr-open-cities-kathmandu-report.pdf`; yatayat OSM routes <https://github.com/neogeomat/yatayat>
- [37] Deployed apps (Sajha Plus, LocaGo) — listings, see `library/README.md`
- [46] Odd-even episodes: Kathmandu Post (2015-09-28; 2020-12-18); Annapurna Express — see `library/README.md`
