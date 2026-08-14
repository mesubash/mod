# Framings, Interpretations, and Hypotheses

This document separates **our thinking** from the evidence. Nothing here is
established; every item is labeled. Evidence lives in
[01-what-we-know.md](01-what-we-know.md).

---

## 1. The original idea

> Kathmandu has many possible roads and transit routes, but during peak
> periods demand concentrates on a few corridors while alternatives may sit
> underused. Individuals optimize their own trip, not the network. Could a
> system understand network-wide demand and help distribute travel across
> better alternatives — improving the network while keeping individual
> journeys acceptable?

```text
Current situation:                      Investigated redistribution:

Major corridor ──► ███████████████      Major corridor ──► ██████████
                   OVERLOADED                              HEALTHIER

Alternative A ──►  █████                Alternative A ──►  ███████
Alternative B ──►  ████                 Alternative B ──►  █████
                   UNDERUSED                               BETTER USED
```

The core conceptual move — and the strongest part of the idea — is the
distinction between:

- **individual route optimization** (what every navigation tool does), and
- **network-level mobility optimization** (what nothing in Kathmandu does).

Concretely: a normal navigation system asks *"what route gets this traveler
there fastest?"* — say Route A at 32 minutes vs. Route B at 35 — and answers
"A" for everyone. Two thousand travelers making the same locally-optimal
choice saturate Route A. A network-aware system asks the further questions:
*what happens when everyone similar also takes A? Would Route B — three
minutes slower for this traveler — leave the whole network significantly
better?* A route can be individually fastest but collectively harmful.

## 2. Our interpretations (could be wrong)

- **Interpretation — the implementation gap is institutional.** Kathmandu's
  planning failures (2014 KSUTP, 2012/2017 master plans) were governance
  failures, not design failures. *Consequence:* any solution requiring
  authority/operator cooperation inherits a 12-year failure mode. A
  traveler-facing tool that ships value without institutional buy-in
  sidesteps it.
- **Interpretation — the "meantime gap."** The 2026 Master Plan covers the
  physical and static-design layers on a multi-decade timeline. Whatever
  manages demand on the *existing* network between now and then is exactly
  the layer the plan leaves open. This also positions the project as a
  complement to the Master Plan, not a competitor — a framing a thesis panel
  will expect.
- **Interpretation — optimize people, not vehicles.** A bus carrying 40
  people and a motorcycle carrying one shouldn't weigh the same. The
  objective should be people reaching destinations, which opens mode-shift as
  an intervention, not just route-shift.
- **Interpretation — traffic is a feedback system.** Recommendations change
  the network state they were computed from. Send 5,000 people to the
  alternative road and it stops being an alternative. Any credible model must
  account for its own effect:

  ```text
  travel demand → network state → route/mode choices → new network state
        ▲                                                    │
        └──────────── recommendations feed back ─────────────┘
  ```

- **Interpretation — "more redistribution" is not monotonically better.**
  Overshoot and the jam simply moves:

  ```text
  Before:                    After over-shifting:

  A █████████████            A ███████
  B ███                      B █████████████   ← jam moved, not removed
  ```

  The expected relationship between shift and network delay is nonlinear,
  with a reversal once alternatives saturate (shape illustrative, not data):

  ```text
  Demand shifted      Network delay

   0%                 ███████████████
   5%                 ███████████
  10%                 █████████
  15%                 ████████
  20%                 █████████   ← alternative saturates; benefit reverses
  ```

  Finding the *optimal amount of intervention* is itself a research result.
- **Interpretation — the congestion cause is unproven.** We assume demand
  concentration on corridors is the main mechanism. It might instead be
  intersection capacity, curbside stopping, badly distributed bus service,
  highly directional demand, or alternatives lacking real spare capacity.
  This assumption is gating check G3.

## 3. Working hypothesis

> **H1:** If travel demand is modeled at the network level and a portion of
> travelers are offered congestion-aware alternatives instead of everyone
> independently taking the currently-fastest route, total network delay and
> peak-corridor congestion can be reduced while keeping individual
> travel-time increases within an acceptable threshold.

This is falsifiable, and the acceptable outcomes include its failure. The
research may instead find:

- it works only under certain congestion regimes;
- it works for private vehicles but not transit (or vice versa);
- the network benefit is too small to justify individual cost;
- required compliance is impractically high;
- **a different lever (departure time, mode shift, intersections) beats route
  redistribution entirely.**

All of these are publishable findings, not failures of the project.

## 4. Competing framings (kept alive deliberately)

| | Framing | Scope | Status |
| --- | --- | --- | --- |
| **F1** | **Demand-aware route recommendation** — network-aware alternative to shortest-path, evaluated by simulation on a bounded Kathmandu network | Narrow, bounded, measurable | **Provisional leader** (audit's Candidate A), gated on G1–G3 |
| **F2** | **Adaptive urban mobility management** — a full observe → predict → optimize → influence → measure loop over the city network; interventions across route/time/mode/service | Research-program-scale umbrella | Long-horizon vision; too big for one project; F1 is its first testable slice |
| **F3** | **Traveler decision support for a fragmented network** — help people use the dysfunctional network better, rather than reorganize the network | Tractable; no institutional dependency | Reframing worth keeping; converges with F1 if enough users create a network effect (the Google result is literally this) |

The relationship: **F1 is the testable core shared by F2 and F3.** Choosing
F1 now does not foreclose either larger framing later.

What a mature F2-style system would eventually answer — different views of
the same mobility system (kept here as the long-horizon picture, not scope):

- **Traveler:** "I need to go from A to B. What should I take?"
- **Network:** "Which corridors are likely to overload in the next 30 minutes?"
- **Planner:** "What happens if 10% of demand moves from corridor A to B?"
- **Transit operator:** "Where is service supply mismatched with passenger demand?"
- **City authority:** "Which interventions give the greatest network benefit
  without new major infrastructure?" — including the long-term planning
  payoff: if no amount of operational redistribution fixes a corridor, that
  is evidence of a genuine capacity problem (build); if operations recover
  20% of capacity, that is evidence building can wait (operate).

## 5. The intervention-lever space (which lever is open)

Candidate mechanisms for redistributing demand — the research should
discover which matter in Kathmandu, not implement all of them:

1. **Route distribution** — don't send everyone down the same corridor *(assumed lever — unproven)*
2. **Time distribution** — don't send everyone at 8:30
3. **Mode distribution** — motorcycle trip → bus + walk
4. **Public-transport service distribution** — match service to corridor demand
5. **Intersection load management** — stop feeding saturated bottlenecks
6. **Parking/curb management** — stopped vehicles destroy effective capacity
7. **Incident response** — stop routing people toward a changed network

Illustrative situation, to show how levers would be compared (numbers
invented): the Koteshwor → Maitighar corridor begins saturating — demand
exceeds practical capacity, queues projected to grow, expected delay +18%.
Instead of displaying "traffic jam ahead," a network-aware system evaluates:
redirect 5% of trips; redirect 10%; shift some travelers to bus; delay some
departures; change transit service; combine several — and picks by predicted
network outcome. The research question is which of these levers actually
moves the needle in Kathmandu.

## 6. Candidate research directions, ranked (from the audit)

| Candidate | Novelty | Feasibility (student project) | Measurable impact | Key risk |
| --- | --- | --- | --- | --- |
| **A. Demand-aware route recommendation** (traveler-facing) | High — no Kathmandu precedent; global precedent is one month old | Medium — needs network graph + demand estimate + simulation | Strong — direct baseline comparison | Data availability |
| B. Dynamic PT demand balancing (live fleet/service matching) | Medium — extends R1 to live | Lower — needs ridership/GPS data that mostly doesn't exist | Medium | Data; overlaps policy work |
| C. Spatial + temporal distribution | Medium | Lower — scope grows fast | Medium | Scope explosion |
| D. What-if simulation tool for planners | Medium | Medium | Weaker — hard to validate without official data | Competing with consultant-built plans |
| E. Multimodal demand optimization | Medium | Low — would swallow a thesis | Medium | Scope explosion |
| F. Dynamic route restructuring | Medium-high | Low | High *if adopted* | Full exposure to the institutional failure mode |

**Provisional selection: Candidate A** — best combination of novelty,
feasibility, measurability; needs no institutional buy-in; has a live global
reference point (Google/Nature Cities, July 2026) to position against; and is
the direction most clearly *not* covered by the Master Plan or prior work.

**Why "provisional":** the audit locked this in; the later exploration
(archived transcript) correctly pushed back — committing to "SUMO + one
corridor + shortest-path vs. demand-aware routing" before verifying that
route redistribution is the highest-leverage lever is one step premature.
The gating checks in [04-open-questions.md](04-open-questions.md) resolve
this tension: pass G1–G3, then commit.

## 7. What we will NOT claim

Existing evidence already disproves the broad versions of all of these:

- "Nobody has solved / studied Kathmandu traffic."
- "Kathmandu has no route planning system."
- "Alternative routes are unused."
- "AI will solve congestion." / "Our system will eliminate jams."
- "We are the first traffic platform for Kathmandu."

The defensible position: Kathmandu has extensive planning and research;
persistent congestion and a documented implementation gap indicate existing
measures are insufficient; this project tests whether a dynamic,
network-aware demand layer adds measurable value — and reports honestly if it
doesn't.
