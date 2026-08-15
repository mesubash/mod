# Existing Solutions — Landscape Map

What has already been proposed, studied, or deployed for Kathmandu, and what
each leaves unsolved. Evidence for every row is in
[01-what-we-know.md](01-what-we-know.md); sources in [06-sources.md](06-sources.md).

---

## The map

| Problem | Existing approach | Status (2026) | Limitation | Remaining gap |
| --- | --- | --- | --- | --- |
| Peak corridor overload, weak network integration | 2026 Master Plan: 22 infra projects, 13 programmes, metro corridor [A1] | **Draft final unveiled Aug 2026; Cabinet approval pending**; multi-decade horizon | Physical/static; years-to-decades lead time; prior versions (2012, 2017) never implemented; does include supply-side ITS (central signal control, CCTV, sensors) | Demand management on the network **as it exists today** — specifically a *traveler-facing* demand layer, per Phase 0 G2 |
| Route duplication / overlap | 2014 KSUTP three-tier route hierarchy [R3], [A2] | Still "proposed" 12 years later | Static design; needs an empowered transport authority Kathmandu doesn't have | Institutional-capacity gap, **not** a technical one — software alone doesn't fix it |
| Uneven bus/vehicle supply vs. demand | Static fleet-optimization study [R1] | Academic, one-off, not deployed | Computed once against historical demand | Could it run continuously against live demand? (Candidate B) |
| Passengers can't find/plan routes | Sajha Plus, Mero Sajha, LocaGo, Google Maps [A4] | Deployed, in active use | Individual-trip tools; no network awareness | A demand-distribution layer is a **different category**, not a better journey planner |
| Intersection congestion | Smart signals, ~5 Lalitpur intersections [A5] | Pilot-stage; most of Kathmandu manual | Isolated intersection control, not network-aware | — |
| Individual route choice | Graph-based journey planner [R11]; Google Maps | Academic prototype / commercial | Optimizes the individual only, **by design** | The clearest literal confirmation of the individual-vs-system gap |
| AI/simulation traffic control | SUMO RL signal control [R9]; IoT review [R10] | Academic, simulation-only | Signal-timing focus | — |
| Bus priority / BRT | Queue-jump and BRT studies [R7], [R8] | Studied, not implemented at scale | Corridor/mode-specific | — |
| System-optimal routing (global) | Google routing-app intervention, 10 US cities [A3] | Published Jul 2026; real-world validated | Requires GPS-scale telemetry; wealthy, formal, car-dominant networks | **Untested in data-sparse, semi-formal, multimodal contexts like Kathmandu** |

## Solution categories and their structural limits

1. **Infrastructure expansion** — geographically and financially constrained
   in the Valley (JICA acknowledges this); decades to deliver; can't be the
   only answer.
2. **Public-transport restructuring** — static, long-term; doesn't answer
   "what should happen *today* between 7:30 and 9:30 when demand differs from
   the average"; historically stalls on institutions.
3. **Signal optimization** — intersection-local; doesn't distribute demand
   across the network.
4. **Bus priority / BRT** — corridor- and mode-specific.
5. **ITS / sensing / prediction** — detects and controls traffic; doesn't
   answer *how demand should be distributed*.
6. **Journey planning** — individual-optimal by construction; network-blind.

## The one-sentence takeaway

Every existing intervention is either **physical/static** (slow, expensive,
historically unimplemented) or **individual** (network-blind by design);
nothing — official, academic, or commercial — occupies the live,
network-aware demand layer in Kathmandu.

**Caveat (open):** this claim is only as strong as the audit's search. Two
checks remain before treating it as firm: reading the primary 2026 Master
Plan document (its 13 programmes might contain something adjacent), and a
deeper Kathmandu-specific literature pass on traffic assignment /
system-optimum applications. See [04-open-questions.md](04-open-questions.md), G2 and Q-gap.
