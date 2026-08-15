# Option Space — Every Viable Research Direction

Exhaustive enumeration of research-paper and problem-solving possibilities
supported by the collected evidence ([library/](library/),
[07-phase0-findings.md](07-phase0-findings.md)). Each option lists its
evidence basis, novelty, and feasibility for a student-scale project.
Ratings justified inline — nothing here is asserted without a collected
source.

Legend: ◎ = strong candidate · ○ = viable · △ = weak/conditional ·
✗ = falsified or blocked by evidence.

---

## A. Temporal (departure-time) levers

### A1 ◎ School/office start-time shift scenario study

Simulate the government's own March 2020 proposal (schools 10:00 → 9:00,
proposed explicitly to cut peak congestion, overtaken by COVID, never
quantified). Kathmandu's offices, schools, and banks synchronize at ~10:00,
making the sharp AM peak partly a coordination artifact — the one peak type
the international literature reliably flattens (Spitsmijden, INSTANT,
INSINC).
**Evidence:** pivot- series; JICA 2012 hourly profiles (Vol 1); onlinekhabar/
Himalayan Times 2020 coverage. **Novelty:** first quantification of a real,
politically pre-legitimized Nepali policy. **Feasibility:** high — pure
simulation on data we hold.

### A2 ◎ Employer/school-anchored departure-time incentive design

INSTANT-style: pre-peak arrival credits + raffle, anchored where arrival is
verifiable (campus badge, school gate). Closest analog doubled pre-8am
arrivals and cut bus commutes 24% for ~US$1,920 total in a motorcycle-heavy
developing city. Kathmandu lacks smart-card ubiquity, so anchored designs
are the only verifiable ones.
**Evidence:** pivot-instant-*, pivot-fhwa-*, pivot-incentives-comparison.
**Novelty:** first Nepali design + simulation; real pilot possible later.
**Feasibility:** high (simulation), medium (pilot).

### A3 ○ Natural experiment — the April 2026 office-hours change

Nepal announced government office hours moving 10:00–17:00 → 9:00–17:00
with a 5-day week (effective April 2026, per myrepublica — ★ verify
implementation). If implemented, DoR hourly count stations + 2019 baseline
counts allow a **before/after empirical study of a real mass retiming** —
no intervention needed, just data.
**Evidence:** DoR hourly-detail URLs (CSV in library); myrepublica report.
**Novelty:** very high — real-world evidence, not simulation. **Feasibility:**
medium — depends on whether the change actually happened and count
continuity. **Check first: this could upgrade the whole paper.**

### A4 ○ PT pre-peak incentive (INSINC-style) on Sajha

Free/discounted boarding before a cutoff on GPS-tracked Sajha buses.
System-level precedent: Singapore 7–8% AM-peak reduction.
**Blocker:** verification without smart cards on semi-formal fleet; Sajha
only. **Feasibility:** low-medium now; future work.

### A5 △ General staggered-hours optimization

Optimize offsets across institution types (schools vs offices vs banks).
Richer than A1 but scope-explosive; Tokyo's version was never rigorously
evaluated. Keep as extension of A1.

## B. Mode-shift levers

### B1 ◎ Capacity-constrained motorcycle→bus shift modeling

Model mode shift jointly with bus crowding (75% report peak overcrowding —
EASTS 2025; odd-even episodes collapsed on PT capacity). SP evidence:
72.2% of Kathmandu motorcycle users state willingness (ceiling, not
forecast); motorcycle users more shiftable than car users (Khon Kaen,
Jakarta 6% from motorcycles to BRT).
**Novelty:** no capacity-constrained mode-shift model exists for Kathmandu.
**Feasibility:** high as a simulation dimension of the core design.

### B2 ○ Bus dwell/fare micro-reform as corridor decongestant

Cash fares add 1.39 s/pax boarding; buses cause >70% of Maitighar–Tinkune
capital loss; dwell is the mechanism. Simulate digital-fare/stop-
consolidation effects on corridor delay.
**Evidence:** evidence-bus-dwell-*, evidence-maitighar-*, evidence-bus-stop-*.
**Novelty:** medium; concrete and cheap. **Feasibility:** high — small,
well-bounded.

### B3 △ Trunk-service mode-shift replication

Corridor-scale replication of JICA's Case 3 result (transit added → V/C
0.85→0.76). Planning-grade work already done by JICA; student version adds
little unless combined with B1.

## C. Spatial levers

### C1 ✗ Route redistribution inside Ring Road

Falsified by Phase 0 G3: all screenline crossings over capacity (2012),
parallel bridges V/C 2.7+, avg inside-RR V/C 1.22, ~80% through-traffic.
Keep only as the falsification narrative — it is itself a publishable
negative result and the paper's motivation.

### C2 ○ Through-traffic bypass study (outside-RR geography)

78–80% of Maitighar–Tinkune traffic is through-traffic; outside-Ring-Road
and valley-entry corridors were never examined for spare capacity. Question:
can through trips be kept on/routed to the (widened) Ring Road or outer
links?
**Feasibility:** medium — needs outer-corridor V/C evidence first (DoR
stations cover the rim). Honest secondary question, not the core.

### C3 △ Tidal/reversible lanes

Supply-side; simulated >50% worst-queue cut but only ~11% average gain
(Jadibuti–Koteshwor study exists). Already studied; MOD adds little.

## D. Methodological / artifact contributions (embed in any option above)

### D1 ◎ Sparse-data corridor OD pipeline

2012 50×50 OD seed (verified extractable) → DoR growth factors (needs
per-station sanity filtering — verified caveat) → JICA's own cordon method
(§13.4.3.2, verified) → calibration against 2019 15-hour counts (verified).
**Novelty:** a reusable "legacy-public-data demand model for data-sparse
cities" method — citable contribution independent of results.

### D2 ◎ Open calibrated Kathmandu corridor testbed (SUMO)

First open, calibrated corridor microsimulation for Kathmandu (VISSIM
behavior parameters from the TU thesis transfer to SUMO; no published
SUMO/MATSim departure-time study exists for any motorcycle-dominant city —
verified gap). Artifact contribution with reuse value.

### D3 ○ Digitized JICA OD matrices as an open dataset

Data paper / repository release. Low effort (~1 day extraction), real
community value. License/attribution of JICA tables ★ check before release.

### D4 ○ MATSim–SUMO coupling for a motorcycle city

Documented coupling exists (SUMO 2020 conf.); applying it to endogenous
departure-time choice in a motorcycle-dominant network is unpublished
territory. Higher effort than exogenous-shift SUMO-only.

## E. Combined / system-level designs

### E1 ◎ THE CORE CANDIDATE — multi-lever sensitivity surface

Simulate the surface over (share retiming p_t, shift size Δt ≤ 30 min,
mode-shift share p_m with bus-capacity constraint) applied to the corridor
OD, measured at the verified binding intersections (New Baneshwor 2.27,
Thapathali 1.89 …). Test the pivoted hypothesis: **a 5–10% AM-peak demand
cut lands in the queue-collapse regime at V/C ≈ 1.2 and yields nonlinear
delay relief — or it doesn't.** Includes A1 (school scenario) and B1 (mode
dimension) as named scenarios; D1+D2 are its infrastructure.

### E2 ○ Compliance-threshold analysis

Minimum participation for measurable network effect (12% vs 45% question).
Falls out of E1 nearly free — keep as a research question, not a separate
project.

### E3 ○ Retiming × signal-optimization interaction

Does demand retiming amplify signal-improvement gains at oversaturated
junctions (Thapathali −76% was demand-fixed)? Novel combination; needs
signal modeling on top of E1 — extension, not core.

### E4 △ Incentive-mechanism comparison in simulation

Raffle vs fixed payments with behavioral parameters from the literature.
Behavioral parameters are the weak link (transferred, not local) —
sensitivity-note level, not a headline claim.

## F. Non-simulation possibilities

### F1 ○ Primary SP/RP survey — Kathmandu departure-time flexibility

No local departure-time elasticity data exists (verified gap; all our
behavioral numbers are transferred). A small stated-preference survey
(commuters on the study corridor: how far would you shift, for what?)
would make MOD's behavioral assumptions local — highest-value primary data
collection available at student scale.

### F2 △ What-if decision-support tool for planners

Earlier audit rated this weaker (validation problem, competing with
consultant plans). Unchanged.

### F3 ✗ Anything requiring authority/operator cooperation to function

Route reform, fleet reallocation, live signal control — the documented
12-year institutional failure mode. Design-out, cite as scope boundary.

---

## Recommended composition (for the paper)

**Core:** E1 (sensitivity surface) = A1 school scenario + A2 incentive
scenario + B1 capacity-constrained mode shift, built on D1 (OD pipeline) +
D2 (open testbed), with E2 answered inside it.
**Validation upgrade if available:** A3 (office-hours natural experiment) —
check implementation status first.
**Primary-data add-on if time:** F1 (small SP survey).
**Motivation/negative result:** C1 falsification narrative.
**Future work section:** A4, B2, C2, E3, D4.

This composition keeps every claim on collected evidence, embeds two
methodological contributions, and preserves falsifiability (the
queue-collapse hypothesis can fail — that outcome is publishable too).
