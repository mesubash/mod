# Temporal and Mode-Shift Travel-Demand Distribution for a Saturated Urban Network: A Feasibility Study for Kathmandu Valley

**Project MOD — feasibility and research-design paper**
Draft v1.0 · 2026-08-14 · status: working draft for supervisor/committee review

All claims cite numbered references (§References); bracketed numbers [n]
throughout. Sources marked **[local]** are held in
[`research/library/`](../library/README.md). Claims that could not be
independently verified are confined to §7 (Limitations) and marked ★.

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
(up to X = 2.27) [9]. The evidence instead supports a pivoted hypothesis:
Kathmandu's sharp morning peak is partly a coordination artifact of
institution start times synchronized at ~10:00 [27,28], and international
experiments show such peaks can be flattened by targeted departure-time
incentives (Bangalore INSTANT [22], Singapore INSINC [23], Dutch
Spitsmijden [21]) within honest bounds: shifts ≤ ~30 minutes [26], 5–10%
corridor-level peak reduction as an upper bound [23,25]. We propose a
simulation study — a sensitivity surface over retiming share, shift
magnitude, and capacity-constrained motorcycle→bus mode shift, evaluated at
the verified binding intersections — with two named policy scenarios: the
government's own unquantified 2020 school-timing proposal [29,30] and an
employer-anchored incentive design [22]. The methodological contribution is
a reusable sparse-data corridor demand pipeline and the first open,
calibrated corridor testbed for a motorcycle-dominant city.

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
4. **A research design**: a falsifiable simulation study of temporal +
   mode-shift demand distribution with named, locally-legitimized policy
   scenarios (§5.3–5.5), and a development plan with internal definitions
   (§6).

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

**Mode-shift interventions.** Across three Swedish field experiments
(n > 32,500), informational and social-norm nudges produced a tightly
estimated zero effect on public-transport uptake, while an extended
free-trial incentive produced significant, durable uptake concentrated among
prior low-users [31]. Motorcycle-heavy cities: 20% of Jakarta's early BRT
ridership came from private vehicles (6% from motorcycles) [39]; Khon Kaen
stated-preference work finds motorcycle users *more* willing than car users
to shift to BRT, with travel time the binding attribute [40]. A Kathmandu
stated-preference study reports 72.2% of motorcycle users willing to shift
to improved public transport [32] — a ceiling, not a forecast (★ §7).

### 2.5 Theory

Wardrop's user-equilibrium vs system-optimum distinction [41] and Braess's
paradox [42] ground the individual-vs-collective framing; Vickrey's
bottleneck model and its logit extensions [43] make departure-time choice
analytically tractable — an incentive enters as a negative toll, giving
closed-form sanity checks for simulation. Google's 2026 experiments [1]
provide the empirical demonstration that small coordinated shifts in
individual decisions produce measurable network effects.

## 3. Problem Statement and Research Questions

**Problem.** Kathmandu's AM peak concentrates home-based work and school
trips into a narrow window fixed by synchronized institutional start times
(~10:00 for government offices, schools, banks) [27,28], onto a network
whose binding intersections already operate at saturation degrees of
1.0–2.3 [9], with no spare parallel capacity [9] and no planned
traveler-facing demand instrument [15–20].

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
cost (retiming is a schedule cost, not a route cost). H1 is falsifiable: if
simulated relief is proportional or negligible, or the required compliance
is impractical (§RQ2), the hypothesis fails and the negative result stands.

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
  sanity filtering is mandatory (§7).
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
  pass (§6).
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
caveat: §7.)

### 4.3 The gap survives, rephrased (gate G2 — conditional PASS)

Across all located coverage of the draft 2026 Master Plan (≈12 English and
Nepali sources), no programme involves congestion pricing, TDM, traveler
information, or any demand-redistribution mechanism [15–20]; the plan's ITS
content is supply-side (coordinated signals, CCTV, sensors, a central
control system, >NPR 1bn) [18]. The gap MOD targets must therefore be
phrased precisely: **a live, traveler-facing demand layer** — not "no ITS."
Two caveats: the full plan document is unreleased (watchlist [45]), and its
2017 predecessor contained a TDM menu [9-v1], so an unreported TDM chapter
is possible (★ §7).

### 4.4 Why temporal + mode shift is the credible pivot

- **Structure**: Kathmandu's government offices run 10:00–17:00 (summer)
  [27]; schools cluster at ~10:00 [29]; banks ~10:00. Synchronized starts
  stack work and school trips into one sharp AM window — IOE studies find
  the AM peak higher and sharper than the flatter 3–4 h PM peak [2,3]. A
  coordination-artifact peak is precisely the kind the international record
  shows can be flattened [21,22,23].
- **Precedent inside government**: in March 2020 the traffic police and PM's
  Office proposed moving school hours to 9:00 explicitly to cut congestion;
  COVID intervened; it was never implemented or quantified [29,30]. A 2026
  announcement moves government offices to 9:00–17:00 with a 5-day week
  (★ implementation unverified) [28] — potentially a natural experiment.
- **Effect-size honesty**: participant-level retiming of 10–20% is
  achievable under sustained, verified incentives [21,22,23]; ~30 min is
  the acceptable-shift ceiling [26]; 5–10% corridor-level AM-peak reduction
  is the defensible upper bound [23,25]. The scientific interest is that at
  V/C ≥ 1.0, queueing theory predicts nonlinear returns to exactly such
  cuts — RQ1 tests whether that regime is real on this corridor.
- **Mode shift must be capacity-constrained**: 75% of Kathmandu PT users
  report peak overcrowding [45b]; odd-even episodes twice collapsed on PT
  capacity [46]. Nudges alone move nothing [31]; any modeled shift must
  respect bus supply.

## 5. Proposed Methodology and Architecture

### 5.1 Data pipeline (research architecture, stage 1)

```text
JICA 2012 Vol 4 (50×50 person-trip + mode OD)      [8]
        │  digitize (pdftotext -layout; ~1 day; QA vs row/col totals)
        ▼
Growth-factor update ── DoR AADT ratios FY11/12→24/25 [12]
        │               (per-station sanity filter; cross-check ATO 2024 [47])
        ▼
Corridor cordon OD ── JICA 2017 §13.4.3.2 method [9-v2]
        │             (cordon around study corridor; crossing-point OD)
        ▼
Calibration/validation ── JICA 2019 15-h classified counts,
        │                 9 intersections, signal timings, queues [10]
        ▼
Time-sliced demand (15-min departure profiles, AM window)
```

Acceptance criterion: simulated baseline link volumes and turning movements
within a stated tolerance (target GEH < 5 on calibrated movements — to be
finalized in the model spec) of the 2019 counts; queue patterns
qualitatively matching the documented bottlenecks [2,3].

### 5.2 Study network

**Primary candidate**: the Tripureshwor–Thapathali–Maitighar–New
Baneshwor–Tinkune–Koteshwor–Jadibuti axis with its cross streets — because
(a) every binding intersection on it is documented with verified saturation
data [9], (b) the 2019 ground-truth counts cover exactly these nine
junctions [10], (c) it hosts the falsification evidence [2], and (d) prior
simulation precedent exists [13b]. Study unit = corridor + feeding network,
per the workspace's network-not-isolated-corridor principle.

### 5.3 Simulation architecture (stage 2)

- **Platform**: SUMO microsimulation. SUMO has no endogenous
  departure-time/mode choice [48]; both levers are applied **exogenously to
  the demand file** — the honest match to our design, since we transfer
  behavioral response rates from the literature rather than estimating
  local choice models (upgrade path: MATSim coupling [48], or local SP
  survey, §6 M5).
- **Network build**: OSM extract → `netconvert` → manual corridor attribute
  audit (lanes, permitted movements, signal locations vs 2019 signal data
  [10]).
- **Calibration**: Kathmandu driving-behavior parameters from [44];
  saturation-flow sanity checks against [49].
- **Baseline**: current departure profile + current mode split, routed to
  equilibrium (`duaIterate`), validated per §5.1.

### 5.4 Experiment design (stage 3)

Sensitivity surface over three dials, each dimension bounded by evidence:

| Dial | Range | Basis |
| --- | --- | --- |
| p_t: share of targeted population retiming | 0–25% | participant-level results 10–20% [21,22,23] |
| Δt: retiming magnitude | −15 / −30 min (pre-peak) | ~30 min acceptability ceiling [26] |
| m: motorcycle→bus shift share | 0–15% of corridor motorcycle trips in the analysis window, bus-capacity-constrained | [31,39,40]; crowding constraint [45b] |

Named scenarios run on the surface:

- **S1 — School shift**: school-linked trips move −60 min (10:00→9:00
  start), per the 2020 proposal [29,30]. RQ3.
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

## 6. Development Plan

Internal definitions live in the model spec (M2); technology beyond the
simulation platform is deliberately undecided.

| Milestone | Content | Exit criterion |
| --- | --- | --- |
| M0 — Verification closeout | ★ items: office-hours change implementation [28]; obtain 2 remaining nepjol papers + SMEC report manually [45]; JICA OD license check for open release | each ★ resolved or documented as limitation |
| M1 — Data extraction | Digitize OD matrices [8]; filter DoR growth factors [12]; extract 2019 counts [10] into machine-readable form | QA: matrix totals match printed totals; growth factors pass sanity filter |
| M2 — Model spec | Written internal definitions: zone system, cordon, time slices, vehicle classes/PCU [49], metrics, GEH tolerance, scenario parameterization | spec reviewed against this paper's §5 |
| M3 — Network + baseline | OSM build, corridor audit, calibration, baseline validation | acceptance criterion §5.1 met |
| M4 — Experiments | Surface + S0–S3 + robustness | all runs reproducible from config |
| M5 — (Optional) local behavior | Small SP survey on corridor departure-time flexibility (replaces transferred parameters) | n, instrument TBD |
| M6 — Writeup | Results paper; testbed + digitized data released (license permitting) | — |

Sequencing note: M0–M2 require no simulation software; M3 is the first
build step. This ordering preserves the workspace's research-before-code
principle.

## 7. Limitations and Threats to Validity

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

## 8. Conclusion

The evidence collected and verified in this study supports a clear
conclusion: Kathmandu's congestion problem, at its saturated core, is not a
route-choice problem — it is a *when* and *what-mode* problem operating on a
network whose intersections are past saturation. The original redistribution
hypothesis was falsified by the city's own survey data, and the project's
direction was changed accordingly. What survives is stronger: a feasible,
fully-public-data corridor demand model; a demand-management gap that no
deployed or planned system occupies; a sharply synchronized AM peak that
international evidence says is the flattenable kind; and a government-
proposed, never-quantified school-timing policy waiting to be its first
test case. The proposed simulation study is falsifiable in both directions
and contributes reusable infrastructure — a sparse-data OD pipeline and an
open corridor testbed — regardless of which way the hypothesis resolves.

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
- Supporting compendia: FHWA HOP-18-071 — [local] `pivot-fhwa-incentives-compendium.pdf`; Berkeley incentives comparison — [local] `pivot-incentives-comparison-berkeley.pdf`

### Kathmandu — official data & plans

- [8] JICA (2012). *Data Collection Survey on Traffic Improvement in Kathmandu Valley* (6 vols; Vol 4 = OD matrices; Vol 2 = screenlines, Table 6.2.12). <https://openjicareport.jica.go.jp/pdf/12082459_01.pdf> — [local] `data-jica-2012-traffic-survey-vol01…06.pdf`
- [9] JICA (2017). *Project on Urban Transport Improvement for Kathmandu Valley*, Final Report (Vol 1 = master plan, V/C assignment, TDM Table 8.4.1 [9-v1]; Vol 2 = cordon method §13.4.3.2 [9-v2]). — [local] `data-jica-2017-urban-transport-vol01/02.pdf`
- [10] JICA (2019). *Data Collection Survey on Urban Transport in Kathmandu Valley*, Final Report (Vol 2 = 15-h classified counts, 9 intersections). — [local] `data-jica-2019-urban-transport-survey-vol01/02.pdf` (dating verified from title page)
- [12] Department of Roads, Nepal. *Traffic counts, ssrn.dor.gov.np* (scraped 29 stations, FY 2011/12–2024/25). — [local] `data-dor-ssrn-aadt-kathmandu-valley-stations.csv`
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
