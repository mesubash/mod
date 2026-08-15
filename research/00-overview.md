# MOD — Research Workspace Overview

**Project:** MOD — *modification / change of direction*: can small,
deliberate changes to individual movement decisions alter the behaviour of
the wider network?
**Topic:** Kathmandu Valley urban mobility — network-level travel-demand distribution
**Status:** Exploratory. Problem direction provisionally selected, not committed.
**Last reorganized:** 2026-08-14 (raw material preserved in `archive/`)

---

## What this workspace is

The research foundation for MOD's investigation of Kathmandu's mobility
problem. It is deliberately **not** a project specification. The problem
direction, study area, methodology, and eventual system are all still open to
revision based on what the research finds. See the project
[README](../README.md) for the framing statement.

## Document map

| File | Contains |
| --- | --- |
| [01-what-we-know.md](01-what-we-know.md) | Established, verified evidence — Kathmandu facts, planning history, global research, theory |
| [02-existing-solutions.md](02-existing-solutions.md) | Map of everything already proposed, built, or deployed for Kathmandu, with limitations |
| [03-framings-and-hypotheses.md](03-framings-and-hypotheses.md) | The original idea, our interpretations, working hypothesis, competing framings, candidate directions |
| [04-open-questions.md](04-open-questions.md) | What we don't know — gating questions, validation questions, methodological unknowns |
| [05-research-plan.md](05-research-plan.md) | Proposed research sequence, corridor selection criteria, experimental design options, explicit scope boundaries |
| [06-sources.md](06-sources.md) | Annotated bibliography with verification status |
| [07-phase0-findings.md](07-phase0-findings.md) | Phase 0 gating-check results (2026-08-14): G1 data PASS, G2 gap PASS-conditional, G3 lever FAIL; verification log; pivot evidence |
| [08-option-space.md](08-option-space.md) | Exhaustive enumeration of viable research directions with evidence basis and recommended composition |
| [paper/mod-feasibility-study.md](paper/mod-feasibility-study.md) | **The central deliverable** — full research-paper-format feasibility study with numbered citations |
| [library/](library/) | Downloaded primary documents & papers (37 files) + link-only index — see its README |
| `archive/` | Raw material this workspace was distilled from (chat transcript, original brief, audit) |

## Epistemic legend

Used throughout the workspace:

- **Established** — verified against credible sources (most claims audited 2026-08-14).
- **Reported** — from news coverage; primary document not yet read.
- **Interpretation** — our reading of the evidence; could be wrong.
- **Hypothesis** — testable claim we intend to investigate, not assert.
- **Open** — genuinely unknown; needs research.

## Current state of thinking (one paragraph)

Kathmandu's congestion is real, officially quantified, and will not be fixed
by infrastructure for years to decades. Every existing intervention is either
*physical/static* (master plans, route rationalization — slow to build and
historically unimplemented for institutional reasons) or *individual*
(journey planners, Google Maps — optimize one trip, ignore network effect).
No system, official or academic or commercial, occupies the middle layer:
continuously reading network state and steering demand toward underused
capacity. Google's July 2026 Nature Cities study validated that layer for the
first time anywhere — in GPS-rich US cities. Whether it can work in a
data-sparse, semi-formal, multimodal network like Kathmandu is the candidate
research question. **But the specific lever (route shifting vs. departure-time
shifting vs. mode shifting) has not been established, and three gating checks
must pass before the direction is locked** (see [04-open-questions.md](04-open-questions.md)).

## Open decisions

1. **Problem direction** — Candidate A as originally scoped (spatial route
   redistribution inside Ring Road) **failed gating check G3**
   ([07-phase0-findings.md](07-phase0-findings.md)): no spare alternative
   capacity; intersections bind; mode shift is the real slack. Pivot
   decision open: temporal + mode-shift demand distribution (evidence-favored) /
   outside-Ring-Road geography / intersection-level problem.
2. **Intervention lever** — route redistribution falsified as first lever for
   the saturated core; departure-time and mode-shift levers now lead.
3. **Study corridor / network boundary** — 3 candidates to be identified, then one selected.
4. **Data strategy** — JICA 2012 OD data vs. OSM + synthetic demand vs. small primary collection.
5. **Simulation platform** — SUMO (+ SB-DSO extension) is a candidate, not a decision.
6. **Scope of evaluation** — simulation-only vs. small real-world pilot.
7. **Project name** — settled: **MOD** (previously "Drift"). Archived material may still use old working titles ("Drift", "Kathmandu Adaptive Mobility").

No technology-stack, architecture, or product decisions are made anywhere in
this workspace, by design.
