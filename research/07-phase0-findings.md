# Phase 0 — Gating-Check Findings

Field-research results for the three gating checks defined in
[04-open-questions.md](04-open-questions.md). Status: **agent-researched
2026-08-14, awaiting user verification** — treat as Reported until the
starred (★) items are independently checked. Downloaded documents live in
[library/](library/).

## Verification log (2026-08-14, checked against local PDFs)

| ★ Item | Result |
| --- | --- |
| Report 12345484 dating (was labeled 2014 in audit R3) | **RESOLVED: it is the July 2019 "Data Collection Survey on Urban Transport in Kathmandu Valley" Final Report** (Oriental Consultants Global / PADECO). The 8/16/42 route hierarchy remains ADB KSUTP 2014 — separate document. 06-sources corrected. |
| 2012 Vol 4 OD matrix extractable | **CONFIRMED** — `pdftotext -layout` recovers the clean 50-zone person-trip matrix (checked zone rows 101–201 with real values). |
| Table 6.2.12 intersection saturation | **CONFIRMED exactly**: New Baneshwor 2.27 (evening), Kalanki 1.99, Thapathali 1.89, Chabahil 1.86, Balaju 1.85 (morning), Sorakhutte 1.82; all 10 ≥ 1.04. Also confirms 9 of 10 junctions were police-controlled, only Koteshwor signalized (2012). |
| 2017 TDM menu | **CONFIRMED** — Vol 1 Table 8.4.1 "Traffic Demand Management (TDM) Measures", §8.4 pp. 8-73–77. |
| 2017 corridor cordon-OD method | **CONFIRMED** — Vol 2 **§13.4.3.2** "Method for Traffic Analysis", Figures 13.4.11–13.4.12 (agent's "§13.4" cite was loose; corrected). |
| DoR AADT CSV | Structure verified (290 rows, 29 stations, hourly-detail URLs work). ⚠️ Caveat found: some stations show implausible year-over-year jumps (Satdobato 5,275 → 20,735 between FY 2011/12 and 2012/13) — per-station sanity filtering required before using growth factors. |
| 2019 hourly/15-min counts OCR-recoverable (A7 / spec §7 decision) | **NOT RECOVERABLE** (checked 2026-08-15, all Appendix 4 pages 32–51 of vol02 rendered at 300dpi + tesseract). Pages A4-2..A4-11 are the survey Terms of Reference (contract text, no data; p.42's numbers are a sample deliverable diagram). Hourly volumes exist only as Figure 4.4 line charts (~570×280 px embedded, no data labels, one unlabeled series per leg, "out" direction absent) — OCR yields only legends/axis ticks; values are line pixels, not text. The 15-min sheets went to JICA as spreadsheets (ToR deliverable 4) and were never printed. OCR method itself validated: tesseract on the rendered Table 4.1 page (A4-19) matched `counts_2019.parquet` 15/15 leg-direction rows exactly. Consequence: M3 criterion stays ±15% daily (A7); GEH-hourly is off the table for this source. |

Still unverifiable locally: the 13-programme slicing (needs the unreleased
document), the NPR 188bn/600bn split (news-only), outside-Ring-Road spare
capacity (unexamined), and the 2012-vintage of all V/C data (inherent
limitation — name it in any writeup).

## Synthesis — where Phase 0 leaves the project

| Gate | Verdict |
| --- | --- |
| G1 data | **PASS** — defensible corridor OD dataset feasible from public JICA matrices + DoR counts + OSM |
| G2 master plan | **PASS (conditional)** — gap survives, rephrased as *traveler-facing demand layer*; full document unreleased, re-verify when it drops |
| G3 lever | **FAIL for spatial route redistribution inside Ring Road** — no spare alternative capacity; intersections bind; mode shift is the real slack |

Net: the research idea survives, the *original lever* does not. MOD's core
question ("can small deliberate changes to individual movement decisions
improve the network?") stands — but pointed at **when people travel and
which mode they take**, not which parallel road they drive. Decision on the
pivot is open — see end of G3 section.

---

## G2 — Primary 2026 Master Plan document

**Verdict: the full document is NOT publicly released yet — and the gap
claim SURVIVES, with one required rephrasing.**

### Document status

- What was unveiled Aug 6, 2026 was a **draft final report** presented at a
  stakeholder seminar — not an adopted plan. Suggestions are to be
  incorporated before submission to the **Cabinet** (finalization reported
  as "within 2026"; the published final report likely 2027, and JICA's
  repository historically lags years).
- No copy online: checked openjicareport (no entry for this project), JICA
  ODA project page 202109574, JICA press index, JICA disclosure pages, and
  the ministry site (mopit.gov.np — note the ministry was renamed
  **Ministry of Infrastructure Development**, ~May 2026).
- **Watchlist:** mopit.gov.np notice board (a Strategic Environmental
  Assessment public-suggestion notice was reported due mid-Aug 2026),
  Cabinet approval news late 2026, openjicareport for the final report.
- ★ Correction to our earlier docs: [01-what-we-know.md](01-what-we-know.md)
  and [02-existing-solutions.md](02-existing-solutions.md) say "Adopted
  Aug 2026" — should read "Draft final unveiled Aug 2026; Cabinet approval
  pending."

### The "13 transport improvement programmes"

No public source prints the verbatim 13-item list. Best multi-source
reconstruction (items 1–10 solidly evidenced; the exact 13-way slicing
unverifiable until the document is public):

1. Public-transport company-model reform — 65+ committees → 5–6 companies,
   valley in 6 operating blocks, 200+ routes restructured
2. Route management
3. Institutional reform of transport operations
4. Intersection + signal programme — 107 junctions (23 by 2032, 84 by
   2040), ~Rs 6bn, incl. coordinated signals, CCTV, roadside sensors, and a
   **central traffic management system**
5. Car-free zones — Thamel (9am–9pm), Kathmandu Durbar Sq, Patan Durbar Sq
6. Cycle-lane network — ~7.4 km short-term, up to 58 km full network
7. Traffic safety programme
8. Emergency road network — ~160 km keeping hospitals/security accessible
9. Off-street parking programme
10. Mass transit — E-W metro Ratna Park–Suryabinayak 14.6 km, N-S line
    11.35 km, Ring Road BRT 27.25 km dedicated lanes
11. Pedestrian environment improvement *(inference)*
12. PT promotion / motorcycle-to-PT mode-shift strategy *(single-source)*
13. Bus service modernization *(theme, multi-source)*

Caution: the three-tier route-hierarchy detail in some 2026 coverage
belongs to the separate **ADB KSUTP** work, not this JICA plan.

### Gap-claim verdict

- Across ~12 English + Nepali sources: **zero mention** of congestion
  pricing, travel demand management, traveler information systems, or any
  dynamic/network-aware demand-redistribution mechanism in the 2026 plan.
- **But** the plan DOES include real-time supply-side ITS: centralized
  signal control, CCTV, roadside sensors (>Rs 1bn). So our gap must be
  phrased as **"a live, traveler-facing demand-redistribution layer"** —
  not "no ITS in Kathmandu."
- Residual risk: the 2017 predecessor plan (downloaded) contains a TDM
  menu (cordon charging, parking charges, park-and-ride, pre-trip travel
  information, car pooling — Table 8.4.1), so a TDM chapter in the 2026
  full document is plausible even though unreported. **Re-verify when the
  document drops.**
- Context strengthening the gap: "more than 2 million vehicles… still
  being managed largely through hand signals and whistles" (SSP Kafle,
  Aug 2026); most existing signal heads inoperable.

### Facts to carry into workspace docs

- ★ Two cost figures circulate: **NPR 188bn** = road-infrastructure portion;
  **NPR ~600bn** = full plan incl. mass transit. Cite carefully.
- Plan vision title: *"Sustainable, Safe, and Inclusive Transport Master
  Plan for a Vibrant and Cultural Kathmandu Valley."*
- Phases: short 2032 / medium 2040 / long 2050.
- Koteshwor–Jadibuti intersection ODA loan (NPR 31.76bn) signed Dec 2025.
- Key downloaded primary/near-primary docs (see [library/](library/)):
  the signed 2023 MoPIT–JICA Record of Discussions (the only official
  document of this exact project available), the 2017 predecessor master
  plan, the 2019 sector survey.

---

## G1 — Data availability

**Verdict: a defensible corridor OD dataset IS feasible — no telemetry
needed.** The single biggest project risk is resolved, whichever direction
the project takes.

### What exists (all downloaded to [library/](library/) unless noted)

1. **JICA 2012 survey (6 volumes) — the OD goldmine.** Vol 4 appendix
   contains the **full 50×50 person-trip OD matrix (2011, all
   purposes/modes)** plus per-mode vehicle OD matrices (motorcycle, car,
   truck, bus) and PCU-converted tables — as machine-extractable text
   (`pdftotext -layout` recovers clean matrices; agent-verified). Vols 1–3:
   18,100-household methodology, 50-zone system, trip-generation/gravity/
   modal-split models, 42 count locations, 13 screenlines. ★
2. **JICA 2017 report (2 vols).** Updated demand models, and — critically —
   **JICA's own corridor-OD-extraction recipe** (Vol 2 §13.4: cordon around
   the Thapathali–Maitighar corridor, corridor OD cut from the valley
   assignment). The exact method a corridor study needs, pre-demonstrated.
3. **JICA 2019 survey (2 vols) — freshest counts, on exactly the obvious
   corridor.** Vol 2 appendix: **15-hour classified directional
   turning-movement counts (15-min intervals, 9 vehicle classes) at 9
   intersections**: Koteshwor, Tinkune, New Baneshwor, Maitighar,
   Thapathali, Tripureshwor, Kalimati, Shahid Gate, Jadibuti — plus signal
   phase/green times and queue lengths. Vol 1: node-to-node OD of the
   Maitighar–Thapathali–Tripureshwor cluster with 2030 forecasts.
4. **DoR traffic-count system (ssrn.dor.gov.np) — live, no auth.** Agent
   scraped **29 valley/rim stations × ~10 fiscal years (2011/12–2024/25)**
   into `data-dor-ssrn-aadt-kathmandu-valley-stations.csv` (290 rows:
   AADT, AADT-PCU, per-year detail URLs serving hourly classified counts).
   Gives station-level growth ratios (e.g. Kalanki AADT 30,176 → 62,669
   over the period). ★
5. **OSM network: defensible with caveats.** No peer-reviewed
   completeness study for Kathmandu; defensibility rests on Open Cities
   Kathmandu (World Bank/GFDRR, 3,716 km valley roads systematically
   mapped), the 2015 HOT earthquake response, and Kathmandu Living Labs.
   Geometry effectively complete; **attributes (lanes, signals, turn
   restrictions) need a manual corridor audit**. No maintained GTFS feed
   exists; bus/tempo routes live in OSM route relations (Overpass-queryable).
6. **Extras:** TU thesis with GA-calibrated VISSIM parameters for
   Kathmandu heterogeneous traffic (transferable to SUMO); ATO Kathmandu
   Urban Transport Profile 2024 (recent mode shares, scaling factors).
   CDR/mobile mobility data: request-only, impractical.

### The winning combination (agent recommendation)

1. Digitize 2012 50×50 OD matrices (≈1 day; text-extractable).
2. Growth-factor update via DoR AADT time series + 2017 model parameters.
3. Corridor sub-OD via JICA's 2017 cordon method; calibrate against the
   2019 15-hour counts at the 9 corridor intersections.
4. OSM graph + manual corridor attribute audit.

**Stated limitation:** growth factors fix totals, not structural pattern
shifts 2012→2026 (new bypasses, Ring Road widening). Lean on 2019 counts
for calibration; name it honestly in any writeup.

---

---

## G3 — Congestion-cause evidence

**Verdict: the working assumption does NOT survive contact with the
evidence. Route redistribution is not a credible first lever for
inside-Ring-Road Kathmandu.** This is exactly the outcome the gating check
existed to catch — H1 as originally scoped is likely falsified for the
obvious study area.

### The two findings that break the redistribution premise

1. **No spare alternative capacity.** JICA 2012 screenlines: traffic
   exceeded capacity at **all** river crossings; the small parallel
   "alternative" bridges are the **most** oversaturated links in the whole
   survey (Kalo Pul V/C **2.76**, Bhatkeko Pul **2.70**). JICA 2017
   assignment: average V/C inside the Ring Road **1.22** in the base year;
   only ~25% of road length below 0.75. There is nowhere to redistribute
   *to*. ★ (high confidence, but dated — 2012 survey / 2011 base year)
2. **Intersections bind, not links.** All 10 major junctions surveyed were
   over saturation a decade ago (New Baneshwor X=**2.27**, Kalanki 1.99,
   Thapathali 1.89). Largest measured/simulated gains come from
   signal/phase/grade-separation fixes: Thapathali delay 99.6 → 24.1 s/veh
   (~76%) from reconfiguration alone; JICA is spending ~Rs 33bn on exactly
   this (Koteshwor/Jadibuti grade separation). ★

### Supporting mechanism scoreboard

| Mechanism | Verdict | Confidence |
| --- | --- | --- |
| Demand concentration → redistribute | Concentration real (78–80% of Maitighar–Tinkune traffic is through-traffic), but premise fails: no spare room anywhere in the core | High |
| Intersection capacity binds | **Dominant mechanism** | High |
| Curbside friction | Real, second-order (~14% max mid-block speed penalty; only "vehicle entry" statistically significant); main friction = stopping public vehicles → transit-ops problem | Medium |
| Directionality / tidal flow | Present, exploitable (reversible lanes cut worst queues >50% in simulation) but average gains modest (~11%) | Medium |
| Transit service distribution | Structural driver; JICA's own modeling: **mode shift, not rerouting, de-saturates the network** (Case 3: inside-RR V/C 0.85 → 0.76) | High |

### Credible levers, in evidence order

1. Intersection signal/phase optimization (cheapest, largest measured headroom)
2. Grade separation at the worst 5–6 junctions (JICA already funding)
3. Tidal/reversible-lane operations on directional corridors (modest)
4. Bus dwell/stop/fare reform feeding trunk transit mode shift — **the only
   lever that reduces demand rather than reshuffling it**

### Caveats before treating this as final

- Core datasets are dated (2012 survey; 2011 assignment base). Demand has
  grown since — which likely makes the no-spare-capacity finding *stronger*,
  not weaker, but ★ verify.
- Intersection-improvement gains are mostly student-grade simulations
  (SIDRA/VISSIM), not field results.
- nepjol.info was down during research; several corroborating papers are
  link-only (listed in [library/README.md](library/README.md)).
- Finding applies to **inside-Ring-Road** networks. A corridor *outside*
  the saturated core (or the valley-entry corridors) might still have
  redistribution room — unexamined. ★

### What this means for MOD (decision point — user call)

Candidate A (route redistribution on an inside-RR corridor) fails its
gating check as scoped. Honest options:

- **Pivot lever:** same network-level framing, different intervention —
  temporal (departure-time) + mode-shift demand distribution, where the
  evidence says the real slack is. Keeps MOD's core idea (small deliberate
  changes to individual decisions), drops the falsified spatial-rerouting
  assumption.
- **Pivot geography:** test route redistribution where alternatives might
  actually have capacity (outside Ring Road / valley-entry corridors) —
  needs evidence that such corridors exist.
- **Pivot problem:** intersection-level optimization is where the
  measured headroom is — but it's supply-side, already JICA-funded and
  academically crowded (R9), and needs authority cooperation (the known
  institutional failure mode).

Downloaded evidence PDFs (14 verified) in [library/](library/).

---

## Phase 0.5 — Pivot evidence (added 2026-08-14)

International + Kathmandu evidence for the pivoted lever (temporal +
mode-shift demand distribution) collected; 9 further PDFs in
[library/](library/) (`pivot-` prefix). Full treatment with citations in
the research paper ([paper/](paper/)). Headlines:

- **Verdict: credible, with a narrowed claim.** Closest analog Bangalore
  INSTANT (employer-anchored departure-time raffle: pre-8am arrivals
  doubled, bus commute −24%, ~US$1,920 total rewards). Singapore
  INSINC/FPPT: −7.5 to −10% participant peak trips, 7–8% system-level AM
  reduction — best documented network-level number. Spitsmijden: −50–61%
  participant peak trips while paid, **reverts when payments stop**.
  Beijing pre-peak discount: **null** (window misplaced; ~30 min = max
  acceptable shift).
- **Kathmandu structural fact:** offices, schools, banks all start ~10:00 —
  the sharp AM peak is partly a coordination artifact, the one peak type
  this literature reliably flattens. Government's own 2020 school-timing
  proposal (10:00→9:00) is a ready-made, politically pre-legitimized
  simulation scenario — never quantified. PM peak is 3–4 h wide — little
  retiming room there.
- **Mode shift:** information nudges ≈ zero (tightly estimated); incentives
  modest but habit-forming for PT uptake; motorcycle users more shiftable
  than car users (SP evidence; 72% stated willingness in a Kathmandu
  survey — ceiling, not forecast); **binding constraint = peak bus
  crowding**, so mode shift must be modeled jointly with PT capacity.
- **Honest bounds for modeling:** departure shifts ≤30 min; 10–20% of a
  targeted population retiming; **5–10% AM-peak corridor volume reduction =
  upper bound**; on a network at V/C ≈ 1.2 at binding intersections that
  cut is nonlinearly valuable (queue-collapse regime) — the simulation's
  job is to demonstrate or falsify exactly that.
- **Method:** SUMO has no endogenous departure-time/mode choice — apply
  shifts exogenously to the demand file (or couple with MATSim);
  Vickrey/de Palma bottleneck theory gives closed-form sanity checks;
  Kumar et al. 2016 provides the transfer-observed-propensities template.
- **Adversarial notes retained:** durability decay, latent-demand refill
  (Downs), peak widening at shoulders, gaming/selection, PT-capacity
  failure under odd-even episodes.

---

## Measured hourly profile — the AM peak is broad (added 2026-08-16)

The departure-time assumption A1 was carried from Phase 0 as an *assumption*
interpolated between two JICA trip-generation anchors. It has now been
replaced by a measurement, and the measurement contradicts the shape the
earlier anchors implied.

### The measurement

Hourly vehicle counts were pulled from the Department of Roads SSRN traffic
portal's per-station detail pages
(`traffic_controller/get_detail/<location>/<id>`), which publish per-hour,
per-direction, per-class counts for the survey days behind each station-year
AADT row. Three FY 2024/25 stations, 3 survey days each, 216 station-day-hours
(`pipeline/dor_hourly.py` → `data/processed/hourly_profile.parquet`,
retrieved 2026-08-16):

| Station | Where |
| --- | --- |
| 64 Manohara Bridge | the study corridor's own Arniko Highway crossing |
| 65 Ring Road (Sinamangal) | Ring Road, north of the corridor's east end |
| 58 Satdobato South (Chapagaun) | southern radial out of Lalitpur |

Pooled share of daily traffic by clock hour (both directions):

| Hour | 06 | 07 | 08 | 09 | 10 | 11 | 12–16 | 17 | 18 | 19 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| % of daily | 3.8 | 4.7 | 5.5 | **6.8** | 6.7 | 6.4 | 6.0–6.3 | **7.4** | 7.0 | 5.8 |

- AM peak hour is 09:00 at 6.8% of daily traffic; 10:00 is 6.7%.
- The 08:00–11:00 analysis window carries 19.0% of daily traffic.
- The PM peak (17:00, 7.4%) is **higher** than the AM peak.
- 09:00–18:00 is a plateau, 6.0–7.4% per hour; the AM peak hour is 1.63× the
  mean hour, the PM peak 1.78×.
- Per station, the corridor's own crossing is the flattest in the morning:
  Manohara Bridge 6.5% at 09:00 against 8.5% at 17:00; Ring Road Sinamangal
  6.4% / 7.0%; only Satdobato South peaks in the morning (7.5% at 09:00).
- Not a weekend artifact: one of the nine station-days (Satdobato,
  2025-03-29) is a Saturday, Nepal's weekly holiday. Dropping it moves the
  pooled AM peak 6.79% → 6.76% and the 08:00–11:00 window 18.99% → 18.92%.

### What it corrects

A1 previously used 06:00–12:00 shares of 3/6/9/20/9/6%, anchored on JICA
2012: "the peak rate of trip generation for all purposes was 20% which
occurred from 9:00 to 10:00" [vol02 §6.1 p.6-7] and "15% to 24% were
concentrated in the peak hours of 9:00 to 10:00 … concentrations became less
than half before and after the peak hour" [p.6-14].

Both anchors are real and correctly quoted. The error was in their
application: they are **person-trip generation** rates — the share of daily
trip *starts*, over all modes including walking, from an 18,100-household
survey — and they were used as the share of daily *vehicle departures* at a
road cross-section. The two are not the same quantity. Trip generation
counts a trip once, at its start, and school trips (48% of which fall in the
peak hour [p.6-7]) skew heavily to walking; a road count records vehicles
present on a link in that hour, mixing purposes, trip lengths and start
times. The measured road profile is about three times flatter than the
generation profile.

The clock position of the peak is unaffected and is now corroborated twice.
JICA's own 2012 *road* counts put the peak at 9:30–10:30 on the Arniko and
Tribhuvan highways [vol02 p.6-25]; the 2025 DoR counts put the two highest
AM hours at 09:00 and 10:00. Two independent measurements 13 years apart
agree on *when* the AM peak falls. Neither supports the claim that it is
sharp.

### What the three stations cannot settle

The stations are highway and Ring-Road cross-sections, not corridor-interior
links. Two mechanisms would make a corridor-interior commuter profile
peakier than what was measured:

1. **Through traffic.** Highway and circumferential cross-sections carry
   freight and long-distance movements whose diurnal pattern is not
   commuter-driven. Against this: the corridor is itself dominated by
   through movements — 78–80% of bikes and cars on Maitighar–Tinkune travel
   straight through [evidence-maitighar-tinkune-bottleneck-2017], so the gap
   between "highway station" and "corridor link" may be narrower here than
   the objection assumes.
2. **Directional aggregation.** The parser keeps the both-direction total of
   each hourly row. A tidal flow — AM inbound, PM outbound — has directional
   peaks sharper than the two-way total. This is the stronger of the two
   objections, and it is recoverable: the per-direction columns are on the
   same detail pages.

Corridor-interior hourly evidence is unavailable from the collected sources.
The 2019 JICA survey counted hourly flows at exactly the nine corridor
junctions, but its hourly profiles survive only as Figure 4.4 line-chart
images with no data labels (verification log above, checked 2026-08-15), so
they cannot be read as numbers. This cuts both ways: the earlier "sharp AM
peak" premise had no corridor-interior support either — it rested on a
household-survey generation statistic.

### How flat is flat — the analogs' own baselines

The pivot rests on international programs that flattened peaks. Whether a
6.8% peak hour leaves room depends on what *their* baselines looked like, so
the collected `pivot-` PDFs were re-read for stated baseline peak
concentrations. Most do not state one.

| Source | Baseline peak concentration as stated | Peak window |
| --- | --- | --- |
| CAPRI, Stanford (TRB 2015) | **peak-hour trip ratio 38.2% AM, 37.3% PM**, of the 3-hour monitoring window 07:00–10:00; full AM distribution 30.2 / 38.2 / 31.6 (p.9–10) | 1 h (08:00–09:00) |
| INSINC, Singapore | **B = 37.1%** of a commuter's 05:00–12:00 trips in the peak hour — stated inside a worked "For example" calculation (p.5). Separately: "over 76% of morning peak trips are due to just 20% of commuters" (p.2) | 1 h (07:30–08:29) |
| INSTANT, Bangalore (NetEcon) | only the complement: "the proportion of early commuters has reduced from 29% in 2005 to 16% in 2007" (p.2), early = departing before 07:30 | none stated; credit thresholds 08:00 / 08:30 |
| Spitsmijden overview | none stated (only *reduction* shares, e.g. 250 cars ≈ 1.5% of peak flow) | 2 h Zoetermeer, 3 h Gouda, 4 h Hollandse Brug |
| Beijing pre-peak discount [26] | not held locally; the paper cites the null result only | discount before 07:00 |
| Berkeley comparison, FHWA compendium, Gravert | none stated for any program | various, tabulated in the FHWA doc |

No document in the library states a peak-to-base ratio, a peak factor, or a
sharp-versus-flat characterization of its baseline curve. ★ Any claim that
these programs ran on "sharp" peaks is therefore unsupported by the sources
the project holds.

Two comparisons are possible, and they point in opposite directions.

- **Against CAPRI, on CAPRI's own denominator, Kathmandu is only slightly
  flatter.** Kathmandu's 08:00–11:00 window splits 29.0 / 35.8 / 35.2 against
  Stanford's 30.2 / 38.2 / 31.6. Peak-to-early-shoulder is 1.23× here against
  Stanford's 1.27×. CAPRI made participants 21.2% less likely to travel in
  the AM peak hour off a baseline barely peakier than this one. On this
  comparison the headroom argument survives intact.
- **Against INSINC, Kathmandu is about half as concentrated.** INSINC's peak
  hour holds 37.1% of a participant's 05:00–12:00 trips; Kathmandu's 09:00
  holds 19.0% of the same 05:00–12:00 span. INSINC measures rail commuters —
  a filtered commute stream — against a mixed road cross-section here, so
  part of that gap is definitional rather than behavioral.

The difference between the two comparisons is the shoulder shape, and that is
the operative finding. Kathmandu has a usable *early* shoulder (08:00 is
1.23× below the peak) and effectively no *late* shoulder (10:00 is 1.5%
below the peak). Every program in the table that moved traffic rewarded
*earlier* travel — CAPRI, INSINC, INSTANT, BART Perks all pay for pre-peak
arrivals — so the shape is the right one for the intervention family the
project is transferring, and the wrong one for any late-shift design.

One warning sits in the same evidence. The Spitsmijden overview links peak
*width* to departure-time response: participants shifted departure time 35%
of the time at Zoetermeer's 2-hour window but only 16% and 15% at the
4-hour windows, and the report states plainly that "shifts in departure time
[are] not as popular in experiments that specify a longer peak period, such
as 0600-1000" (p.3). Kathmandu's measured road profile is a wide-window
case. The p_t = 10–20% dial in the paper's §5.4 sits at the low end of the
Spitsmijden range for precisely this reason, which is the right place for it.

### Consequences for the hypothesis and scenarios

The measurement narrows the arithmetic room for departure-time shifting, and
the size of that room can now be stated exactly rather than assumed.

- **Ceiling on within-window retiming.** Perfectly levelling 08:00, 09:00 and
  10:00 (19.0% of daily, mean 6.33%) cuts the peak hour from 6.79% to 6.33%
  — a **6.8% reduction in peak-hour traffic**, and that is the ceiling, not
  an expected value. Extending the levelling back to 07:00 raises the ceiling
  to 13.0%, but requires shifts up to two hours, well past the ~30-minute
  acceptability ceiling from the Beijing null [26].
- **A −60 min shift from 10:00 into 09:00 is worthless, and the reverse is
  what S1 does.** Levelling 09:00 and 10:00 alone yields a 0.8% peak-hour
  cut: the two hours are already within 0.1 pp of each other. S1's
  10:00→9:00 school-start change moves peak-hour (09:00–10:00) departures
  into 08:00–09:00, which is the one genuinely lighter hour (5.5%), so the
  direction is right — but the trough being filled is 1.3 pp deep, not the
  11 pp the old profile implied.
- **The threat to H1 is the plateau, not the smaller cut.** H1 claims
  superlinear delay relief at intersections above saturation. Superlinearity
  comes from the network crossing in and out of oversaturation; a 09:00–18:00
  plateau at 6.0–7.4% per hour means the binding intersections may be
  oversaturated continuously rather than transiently. Under continuous
  oversaturation, deterministic queueing makes total delay roughly
  proportional to the integral of excess demand, and relieving one hour while
  the next hour is equally loaded does not let queues dissipate — `t_diss`
  would stay censored (spec §7). The flat profile is therefore adverse to
  H1's superlinearity claim specifically. Testing it is still the point:
  RQ1 now has a real chance of returning the negative answer.
- **Resolution below the hourly grid.** Δt = 15 and 30 min operate inside a
  single hour of the profile; the model spreads departures uniformly within
  each hour, so sub-hourly retiming results inherit that assumption.

Registered in the assumption register as a measured A1
([specs/model-spec.md §9](../specs/model-spec.md)) with the per-direction
extraction as its sensitivity path.
