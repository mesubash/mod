# What We Know — Established Evidence

Everything here was verified in the 2026-08-14 audit unless marked
**Reported** (news coverage only; primary document unread). Source refs
(R1–R12, A1–A6) resolve in [06-sources.md](06-sources.md).

---

## 1. The problem is real and officially quantified

- **Established:** JICA figures (2026) put Kathmandu's east–west corridors at
  **150,000–200,000 passengers/km**, against ~100,000/km — the threshold JICA
  treats as the ceiling for road-based transit. Some roads already run ~20%
  over intended capacity. [A1]
- **Established:** JICA's 2012 survey (18,100-household interview) identified
  chronic congestion on major roads, insufficient public transport, and
  disorderly urbanization, and argued road, public-transport, and land-use
  development must be planned together. [R2]
- **Established:** Kathmandu's public transport developed through fragmented
  private operations, producing overlapping routes and uneven supply. [R3], [R6]

## 2. Planning history: plans exist; implementation fails

- **Reported (corrected by Phase 0, see
  [07-phase0-findings.md](07-phase0-findings.md)):** The *Kathmandu Valley
  Urban Transport System Master Plan* (JICA / Ministry of Infrastructure
  Development, renamed from MoPIT ~May 2026) was unveiled ~August 6, 2026 as
  a **draft final report at a stakeholder seminar — not yet Cabinet-approved,
  full document not publicly released**. Horizon 2050: 22 infrastructure
  projects + 13 "transport improvement programmes," ~NPR 188 billion
  (road-infrastructure portion; ~NPR 600bn incl. mass transit). Contents include elevated
  highways (Chabahil–Bagmati, Tripureshwor–Maitighar, Bishnumati corridor),
  underpasses/tunnels, Ring Road widening, upgrades to 107 intersections
  (23 by 2032, phased through 2040) including intelligent signals, and a
  proposed metro corridor Ratna Park → Suryabinayak. [A1]
  - **Caveat:** all of this is from news coverage. The primary document has
    not been read — a gating task (G2 in [04-open-questions.md](04-open-questions.md)).
  - **Reported:** the 13 management programmes cover route rationalization,
    fare/service integration, and physical traffic control — no dynamic,
    algorithmic demand-redistribution component was found in any coverage.
- **Established:** The 2014 KSUTP (ADB) route-rationalization plan — a
  three-tier hierarchy of 8 primary / 16 secondary / 42 tertiary routes —
  remains **unimplemented 12 years later**. As of mid-2026, Nepali media still
  describe it as something the government is "putting forward." [R3], [A2]
- **Established:** Officials at the 2026 Master Plan launch said focus should
  "shift from planning to implementation" — an implicit admission that the
  2012 and 2017 plan versions were not implemented. [A1]

**The pattern:** Kathmandu's route-planning failures have been
**institutional (authority, coordination, enforcement), not technical**. The
2014 plan was not under-designed; it was under-implemented. This is the
single most important critical finding of the audit.

## 3. Kathmandu-specific research (all verified)

| Work | What it did | What it is NOT |
| --- | --- | --- |
| Fleet optimization, Bajracharya & Nakarmi 2021 [R1] | Studied 163 PT routes, optimized vehicle allocation on top 10 via Excel Solver; modeled fleet could shrink ~41% | Static, one-time; never deployed |
| Graph-based journey planner, 2025 [R11] | Multi-modal shortest-path for Kathmandu's semi-formal transit; ~18% individual journey-time reduction | Explicitly **not** network-aware; individual trips only |
| AI traffic framework, 2024/25 [R9] | SUMO-based reinforcement-learning **signal control** at intersections | Not route/demand distribution |
| Bus priority / queue-jump studies [R7], [R8] | Corridor-level bus-priority and BRT feasibility | Largely not implemented; corridor-specific |
| IoT traffic-management review [R10] | Surveys sensing/control potential | Detection/control focus, not demand distribution |

## 4. Deployed systems (2026)

- **Established:** Sajha Plus (official live GPS bus tracking, single
  operator), Mero Sajha, LocaGo (multi-operator route lookup), Google Maps —
  all deployed and in use. All optimize or inform the **individual trip**;
  none reasons about network-wide congestion or redirects demand. [A4]
- **Established:** "Intelligent" traffic signals exist at ~5 Lalitpur
  intersections (since late 2024/2025). Only **35 of 64** signals in the
  Valley were functional as of April 2025; Kathmandu proper still runs
  largely on manual police control. [A5]

## 5. Global research

- **Established:** Google Research, *Nature Cities*, July 2026 — the first
  large-scale real-world empirical study of system-aware routing: rerouting a
  small share of Google Maps trips off ~100 congested segments across 10 US
  cities measurably reduced citywide delay and emissions. Google's own
  framing: system-wide routing optimization "is not yet present" in
  commercial navigation, and large-scale empirical validation was previously
  limited. [A3]
  - Implication (established, not interpretation): the individual-vs-system
    routing gap is a live, open research frontier — not solved even by the
    organization with the best global traffic data.
- **Established theory (60+ years old):** Wardrop's user-equilibrium vs.
  system-optimum distinction (1952), Braess's paradox (1968), congestion
  externalities, dynamic traffic assignment. The theory is settled; what is
  open is **real-world empirical validation, especially in data-sparse,
  semi-formal contexts**.

## 6. Methodological precedent

- **Established:** JICA's Kathmandu work used bounded study areas/cordons,
  OD (origin–destination) matrices, and user-equilibrium traffic assignment —
  corridor-scale modeling is standard practice, not a shortcut. [R2], [A6]
- **Established:** Recent Kathmandu research used the Thapathali–Koteshwor
  corridor as a simulation study area — precedent for corridor-scale
  experiments. [R9]
- **Established:** A simulation-based dynamic system-optimal assignment
  algorithm for SUMO exists (Mehrabani et al. 2022, SB-DSO). [A6]
