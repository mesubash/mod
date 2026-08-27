# MOD — product specification

**Route guidance for drivers who do not have the map in their head.**
Draft 1 · 2026-08-26 · companion to
[`../paper/mod-feasibility-study.md`](../paper/mod-feasibility-study.md)

Every claim here traces to a section of the paper or is marked as an open
assumption. Where the research does not support a claim, the product does not
make it.

## 1. What this is

A routing service for the Kathmandu corridor that answers one question well:
*given where you are, where you are going, what you are driving, and what is
broken right now — which way should you go?*

The study behind it ranks four demand-side interventions on one calibrated
network. Rerouting is the second strongest, behind shifting motorcycle trips
to bus and ahead of every departure-time instrument, both of which raise delay
(paper §5). Of the two that work, rerouting is the one a private product can
deliver: the other needs bus capacity the corridor does not have.

Reference points: Pathao and Yango both route on a road graph and neither
claims to reduce the city's congestion. They tell a rider where the road goes
and how long it takes. MOD is that, with three things they do not do.

## 2. What the research supports, and what it does not

**Supported.**

- Alternative routes exist for essentially every corridor trip. Of tested
  origin–destination pairs, 100% had at least one alternative when the primary
  path was excluded (paper §6, retraction note). The earlier "61% have no
  alternative" finding was a routing-code defect and is withdrawn.
- A driver without local knowledge gains real time from being given those
  routes. This needs no simulation: the alternative exists, and a driver who
  does not know it cannot use it.
- Non-recurring disruption — rain, VIP movement, an incident, a flooded
  underpass — is the regime where a fixed mental map fails hardest, and where
  a trip already underway can be rerouted but cannot be retimed or
  mode-shifted (paper §6.7).

- Diverting corridor trips onto alternatives reduces network delay, and the
  effect grows with the share diverted: −14.4 ± 3.1% at 5%, −25.7 ± 3.1% at
  10%, −42.6 ± 2.5% at 20%, across 24 treatment-assignment seeds. Cordon
  throughput rises with it. The network benefits, not only the driver.

**Withdrawn (2026-08-27).** This document previously said the product could
claim *faster for you* but never *better for the city*, because diverting
traffic onto lower-capacity alternatives cost throughput in every test. That
measurement was taken on a network already in congestion collapse, where the
alternatives are jammed too and no diversion can help. Re-run at a loading the
network carries, the sign reverses. The constraint is lifted.

**Not supported, and still not to be claimed.**

- That the measured effect transfers to the street. It is one corridor, one
  loading, mesoscopic, and it assumes the diverted share actually complies.
  The simulation says the roads can absorb the traffic; it does not say
  drivers will accept the route.
- Any specific percentage in public material. −42.6% is a modelled figure at a
  modelled loading, not a promise.

**The line, revised.** The product may say that spreading traffic across
alternatives helps the network as well as the driver, and should cite the
study rather than a number. It may not promise a congestion reduction to any
particular user or city authority.

## 3. What competitors do not do

### 3.1 Vehicle-class routing

A scooter can take internal roads a truck cannot. The corridor network encodes
this — a route legal for a motorcycle is rejected for a bus with "no
connection between X and Y" — and the routing already threads each vehicle's
own class (`experiments/transforms.py`, `VCLASS`). Neither Pathao nor Yango
routes differently for a scooter, a car and a truck on Kathmandu's internal
roads.

This is the clearest differentiator and it is already built.

### 3.2 Event-driven closures

VIP movement shuts a corridor link with minutes of notice. A generic traffic
layer learns about it only after congestion has built. A closure feed that
accepts "this link is shut from 09:00 to 10:00" and re-plans affected trips
immediately is a different product, and it is the S4 scenario made real
(`pipeline/disruption.py`).

### 3.3 Guidance calibrated to what the driver already knows

The value of a route is not the route, it is the gap between the route and
what the driver would have done. That gap is largest for someone new to the
city and near zero for a local who already takes the shortcut. The product
should know which it is talking to.

## 4. Users

- **Newcomer / occasional driver.** Highest value. Has no mental map. Wants a
  route that works for their vehicle.
- **Professional rider (delivery, ride-hail).** Knows the main roads; wants
  the disruption feed and the vehicle-class shortcuts.
- **Operator / traffic police.** Publishes closures, sees where diverted
  traffic goes. This is the console side, not the traveller app.

## 5. System

    closure feed  ──┐
    (operator, ops) │
                    ├──►  routing service  ──►  traveller app
    road graph  ────┤     (vClass-aware,        (route, why, alternatives)
    (OSM + width-   │      closure-aware)
     derived lanes) │
                    │
    live conditions ┘
    (see §7 — open)

### 5.1 Road graph

OpenStreetMap, with lane counts derived from carriageway width rather than
lane markings (`pipeline/lane_width.py`, A14). The corridor's arterials are
tagged `lanes=1` and are 6–8 m wide; taking the tag at face value builds a
third of the road. Width covers 1,578 road ways in the extract against 635
for lanes.

Reused from the research build; no new work.

### 5.2 Routing service

Dijkstra/A* over the graph with a hard exclusion set for closed links, keyed
by vehicle class. Already implemented and tested
(`experiments/transforms.py`, `_shortest`, `_alternatives`).

Note the defect it was built from: an earlier version "blocked" edges by
mutating edge speed, which sumolib's router ignores because it caches. The
exclusion must be in the search, not in the graph attributes. There is a test.

### 5.3 Closure feed

`pipeline/disruption.py` already emits closures. Two corrections it carries:

- The rerouter must sit **upstream** of the closed link. A vehicle cannot
  reach a closed edge, so a trigger placed on it never fires.
- A closure only means something if the link was flowing. Shutting a link that
  is already at 0.03 m/s removes nothing. The product's operator console
  should show current flow on a link before offering to close it.

### 5.4 Traveller app

Covered by [`../../UI-PROMPT.md`](../../UI-PROMPT.md) — monochrome,
mobile-first, onboarding / home (normal and disrupted) / alternatives /
after-trip question / how-it-works. Two changes that follow from this spec:

- Vehicle class is a first-class onboarding choice, not a setting buried in a
  profile. It changes the answer.
- The after-trip question should ask **"did you already know this route?"**
  That single answer measures the product's actual value — the gap in §3.3 —
  and it is the only way to get the local-knowledge number that no Kathmandu
  source provides.

## 6. MVP

1. Road graph with width-derived lanes for the corridor extract. *(done)*
2. Vehicle-class routing service behind an HTTP endpoint. *(routing done;
   service wrapper is new work)*
3. Operator closure publishing, with current-flow display before closing.
4. Traveller app: origin, destination, vehicle class, route, alternatives,
   disruption banner.
5. After-trip question: did you already know this route?

Not in the MVP: credits and retiming incentives. Retiming raised network delay
at every share tested, from +7.9 ± 3.1% at 5% to +36.1 ± 5.1% at 25%, because
the measured demand profile is a plateau rather than a spike. An incentive to
travel fifteen minutes earlier moves a trip into an hour that is already as
busy. Building it would be building the intervention the study measured as
counterproductive.

## 7. Open, and honest about it

- **Live conditions.** The product needs to know what is moving *now*. No
  Kathmandu real-time traffic feed was found in the research. Options: probe
  data from the app's own users (cold-start problem), operator reports, or a
  third-party layer. Unresolved, and it gates §3.3.
- **Local-knowledge share.** How many Kathmandu drivers already know the
  alternatives is unmeasured; the paper sweeps it as an assumption. The
  after-trip question in §5.4 is the cheapest way to measure it, and it is
  worth building for that reason alone.
- **Cold start.** Guidance quality depends on knowing conditions; knowing
  conditions depends on having users.
- **Induced demand.** If guidance works, it may attract traffic to internal
  roads through residential areas. Not measured; a real externality; flagged
  before it is discovered by residents.

## 8. What would falsify this

The product's core claim is that being told a route beats not being told. It
fails if the after-trip question comes back saying most users already knew the
route — in which case the value is the disruption feed alone, and the
vehicle-class routing, not the guidance.

That is a cheap experiment and it should be run early, before the guidance
engine is optimised for a benefit that may not be there.
