# Open Questions

What we don't know, ordered by what blocks what. The three **gating checks**
must be answered before the problem direction (Candidate A in
[03-framings-and-hypotheses.md](03-framings-and-hypotheses.md)) is committed.

---

## Gating checks (answer first — each can change the direction)

### G1 — Data availability *(the single biggest risk)*

The Google result rests on GPS-scale telemetry. Kathmandu has no equivalent
public dataset. Options to investigate, in order:

1. Is the JICA 2012 household-survey / traffic-survey OD data obtainable
   (public output tables, or requestable)?
2. Is OpenStreetMap's Kathmandu road network good enough for a defensible
   study graph?
3. Is a synthetic/estimated demand model defensible, and by what method?
4. Is small-scale primary data collection feasible as a fallback?

If none of these produce a defensible OD/demand estimate for a bounded study
area, Candidate A is not feasible as scoped and the direction must change.

### G2 — Read the primary 2026 Master Plan document

Everything known about it comes from news coverage. The full document must be
located and read to confirm the 13 "transport improvement programmes" contain
nothing adjacent to dynamic demand redistribution. If they do, the gap claim
collapses and the project must reposition.

### G3 — Is route redistribution actually the highest-leverage lever?

We assume corridor demand concentration is the dominant congestion mechanism.
Plausible rivals: intersection capacity, curbside stopping, poorly
distributed bus service, highly directional demand, alternatives without real
spare capacity, departure-time peaking. Before locking the experiment design,
establish (from existing studies + corridor evidence) that route-shifting is
at least a credible first lever — or pivot the intervention accordingly.

---

## Problem-validation questions

- Which corridors show the clearest demand–capacity mismatch on available
  data? (JICA's flagged east–west corridors are the obvious starting set —
  using them makes the baseline claim independently corroborated.)
- Are alternative corridors *genuinely* underused, with real spare capacity —
  or do they saturate immediately when loaded?
- What is the causal mix of congestion: sheer demand vs. intersections vs.
  curb activity vs. transit stopping vs. driving behavior?
- How directional and time-peaked is demand on candidate corridors?

## Gap-validation questions

- Has system-optimal or dynamic traffic assignment ever been applied to
  Kathmandu specifically?
- What are the closest existing academic projects (Kathmandu or comparable
  South Asian cities)?
- Which parts of past route-rationalization proposals were implemented, which
  weren't, and why? (Deepens the institutional-failure evidence.)

## Methodological questions

- How to represent **semi-formal transit** in a network model — microbuses
  and tempos have no fixed schedules and mostly no GPS; what counts as a
  "route" requires judgment calls that must be documented.
- Where should the study-network boundary sit so traffic has somewhere to
  redistribute (a corridor in isolation cannot show redistribution)?
- How much simulated demand can shift before alternatives saturate?
- What is the individual-vs-network trade-off curve, and what individual
  cost threshold counts as "acceptable" (and who decides)?
- How robust are results to being wrong — demand ±20%, travel-time noise,
  incidents, imperfect information? An intervention that only works when the
  model is exactly right is not a result.

## Behavioral questions (later, but name them now)

- Will travelers accept a slower-but-network-better route? At what cost?
- What compliance level is required before the intervention produces a
  measurable network effect — 12% is deployable, 45% probably isn't. Both
  answers are valuable.
- Do incentives (non-monetary "mobility credits", off-peak benefits) change
  compliance? (This is the Travel Demand Management extension — out of
  initial scope.)

## Honest-limitation questions

- Even a simulation-validated result says nothing about real adoption; what
  real data would be needed to move beyond simulation, and is that path
  plausible? (Must be answered in the writeup, not solved.)
