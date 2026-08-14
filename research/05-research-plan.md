# Research Plan

Proposed sequence, not a commitment. Each phase can revise everything after
it — the model grows only where evidence says growth is warranted.

```text
REAL KATHMANDU CORRIDOR
        │
        ▼
observe / collect evidence ──► define small model ──► baseline
                                                         │
                                                         ▼
              improve model ◄── learn ◄── measure ◄── experiment
                    │                                    ▲
                    └────────────── new experiment ──────┘
```

---

## Phase 0 — Gating checks (before anything else)

Resolve G1–G3 from [04-open-questions.md](04-open-questions.md):

1. **G1 data:** attempt to obtain/reconstruct an OD demand dataset for a
   bounded study area (start: JICA 2012 public output tables + OSM road
   graph).
2. **G2 plan:** locate and read the full 2026 Master Plan; confirm the 13
   programmes contain nothing adjacent to this idea.
3. **G3 lever:** collect corridor-level evidence on congestion causes;
   confirm route redistribution is a credible first lever.

Only after these pass: commit to Candidate A and lock the study scope.

## Phase 1 — Corridor selection

Identify **3 candidate corridors**, then select **one** — chosen for research
characteristics, *not* worst congestion:

- recurring, documented peak congestion (prefer corridors JICA has already
  flagged as saturated, so the baseline claim is corroborated, not asserted);
- identifiable origin–destination demand;
- at least one plausible alternative path with suspected spare capacity;
- enough surrounding network for traffic to actually redistribute — the study
  unit is a **network around a corridor**, never an isolated road:

  ```text
               Alternative A
                    │
            ┌───────┴───────┐
  Origin ───┤ MAIN CORRIDOR ├─── Destination
            │  ███████████  │
            └───────┬───────┘
                    │
               Alternative B
  ```

  Modeling only `Origin ── Destination` gives traffic nowhere to go, and no
  redistribution experiment is possible;
- public transport operating along or around it;
- observable behavior / prior studies (e.g., Thapathali–Koteshwor has
  simulation precedent).

For each candidate, build a corridor profile: demand, capacity, travel time,
congestion pattern, OD structure, transit service, alternatives, intersection
bottlenecks, curb effects, incident pattern.

## Phase 2 — Baseline (the most important step)

A credible answer to: **what happens if nobody intervenes?**

- Document precisely: network + demand + route-choice assumption + time
  period. No live data required — a *defensible representation* is enough for
  the first experiments.

  ```text
  peak period → OD demand → current network → route-choice assumption
             → traffic assignment / simulation → baseline metrics
  ```

- Record: average travel time, total delay, per-link volume,
  volume/capacity, queue lengths, throughput, bottleneck locations, route
  distribution.
- **No optimization until the baseline is credible.** A garbage baseline
  makes every later experiment garbage.

## Phase 3 — Experiments (progressive; stop where evidence stops justifying growth)

### Model-growth ladder

| Model | Adds | Note |
| --- | --- | --- |
| 0 | Road network (links, intersections) | |
| 1 | OD demand | |
| 2 | Route choice / traffic assignment | |
| 3 | Time-dependent (peak) demand | |
| 4 | Demand-redistribution intervention | first real experiment |
| 5 | Behavior: compliance / route-choice response | |
| 6 | Multimodal (bus, motorcycle, car…) | only if earlier results justify |
| 7 | Uncertainty: noise, incidents, imperfect info | robustness pass |

Reaching Model 7 is not the goal; the research decides what earns inclusion.

### Experiment sequence

1. **E1 — Redistribution sweep:** shift 2% / 5% / 10% / 15% / 20% of peak
   demand off the dominant route; measure network delay. Expect nonlinearity
   and an eventual reversal when alternatives saturate — finding the *optimal
   amount of intervention* is itself a result.
2. **E2 — Individual cost:** for every shifted traveler, measure added trip
   time; construct the network-benefit vs. user-cost (Pareto) curve and find
   its knee:

   ```text
   Network benefit
         ▲              ●
         │          ●
         │      ●
         │  ●
         └────────────────► individual cost
   ```

   Target result shape (numbers invented): "redirecting 8% of travelers adds
   2.1 minutes to their average trip but cuts network-wide delay 14%."
3. **E3 — Targeted selection:** replace "shift 10%" with "*which* 10%?" —
   some OD pairs have good alternatives, others none; select shifts with the
   best benefit-to-cost ratio. This turns recommendation into optimization.
4. **E4 — Temporal:** compare/combine departure-time shifting with route
   shifting. (Only if route-only results are in and time permits — this is
   Candidate C territory.)
5. **E5 — Multimodal:** move people between modes, not vehicles between
   roads.
6. **E6 — Robustness:** rerun winning interventions under demand ±10–20%,
   travel-time noise, incidents. Does it still work when the model is wrong?
7. **E7 — Compliance:** sweep 0–100% compliance; find the minimum
   participation for measurable network effect. Either outcome is valuable:
   "12% compliance suffices" means deployable; "45% required" means the
   intervention is impractical as designed.

## Evaluation (defined before building)

| Metric | Baseline | Proposed |
| --- | --- | --- |
| Average travel time | ? | ? |
| Total network delay | ? | ? |
| Peak-corridor utilization | ? | ? |
| Overloaded segments | ? | ? |
| Individual cost to shifted travelers | — | ? |

Illustrative shape of a what-if comparison (numbers invented — the project
must compute them from the model):

```text
Scenario: baseline                   Scenario: 8% demand shifted

Average travel time:      42 min     Average travel time:      40 min
Total network delay:  18,400 min     Total network delay:  13,800 min
Peak corridor load:          91%     Peak corridor load:          77%
Shifted travelers:             —     +2.1 min average per shifted trip
```

**Success =** measurable, statistically credible reduction in network
delay/congestion vs. the shortest-path baseline on a real (even small)
Kathmandu study network, **with honest accounting** of the individual-cost
trade-off and of what real data a beyond-simulation claim would need. The
Google study's small single-digit gains from shifting a small trip share are
a reasonable order-of-magnitude expectation, not a guarantee. Not every
metric must improve — the trade-off itself is the scientific result.

## Explicitly out of scope (initial project)

- Anything requiring transport-authority, operator, or government cooperation
  to function (route reform, fleet reallocation, signal control) — that's the
  documented 12-year institutional failure mode.
- Valley-wide or all-modes deployment; one bounded study network only.
- Live production deployment with real users — simulation/prototype-level
  evaluation first. (A small controlled real-world trial with a bounded
  population — a campus, a company — is the natural *next* project.)
- Departure-time distribution (unless route-only work finishes early).
- Re-deriving master plans, metro proposals, or infrastructure
  recommendations — the 2026 Master Plan exists; position alongside it.

## Deliberately undecided

Programming language, frameworks, databases, architecture, ML models, UI,
hardware, simulator. **SUMO + the SB-DSO extension (Mehrabani et al. 2022) is
the noted candidate** for the simulation platform — recorded so it isn't
re-researched, decided only after Phase 0.
