# Kathmandu Mobility Project — Research Audit & Finalized Problem Definition

*Critical review of the working brief, dated August 14, 2026*

---

## 1. Audit of the brief's claims

Overall, the brief is unusually well-grounded — every numbered source (R1–R12) checks out and is accurately characterized. But two things need correcting before this goes further, and one major development isn't in the brief at all because it happened in the last two weeks.

### 1.1 What checks out

- **R1** (Bajracharya & Nakarmi, JACEM) — confirmed. 163 routes studied, top 10 analyzed, vehicle requirement optimized via Excel Solver; fleet size on the modeled routes could drop ~41% under the optimized allocation. This is a **static, one-time optimization**, not a live/adaptive system.
- **R2** (JICA 2012 traffic survey) — confirmed. 18,100-household interview survey, identified chronic congestion, weak public transport, disorderly urbanization.
- **R3 / R4** — confirmed and important context you're missing: the **primary/secondary/tertiary route-hierarchy proposal is from the 2014 Kathmandu Sustainable Urban Transport Project (KSUTP)**, backed by ADB. As of **June–July 2026**, Nepali media (Ratopati, Nepali Times) are still describing this exact restructuring as something the government is only now "putting forward" for implementation — meaning a plan proposed in **2014 has still not been executed by 2026**, twelve years later. Kanak Mani Dixit (Sajha Yatayat chair) was writing in July 2026 that this rationalization "must" be done, as if it still hasn't been. This is a stronger and more specific data point than the brief has: the bottleneck for route rationalization has been **institutional/implementation capacity, not lack of a plan or lack of technical design**.
- **R11** (graph-based journey planning) — confirmed, and worth being more precise about: it's classic multi-modal shortest-path routing for individual trips (reduces individual journey time by 18% in evaluation), explicitly **not** collective/network-aware. This is a clean, real example of "individual optimization" vs. what the brief wants to investigate.
- **R9** (AI-driven traffic framework) — confirmed, SUMO-based, focused on **reinforcement-learning signal control** at intersections, benchmarked against LA/Beijing/Singapore signal systems — not route/demand distribution.

### 1.2 What needs correcting

- **Section 5.5 treats the JICA Master Plan as still in progress ("is intended to...").** It is not. **It was unveiled on approximately August 6, 2026** — days before this brief was written — as the fourth comprehensive master plan for the Valley (after 1993, 2012, 2017 versions, none of which the 2012/2017 versions were reportedly implemented, per Meroauto's reporting). This is a live, current-affairs correction, not a nuance, and it materially changes what "the gap" is (see §2 below).
- **R6's framing of "route overlap and inability to absorb demand"** is accurate but dated — cite it as background, not as the state of current planning.

---

## 2. Major update: the JICA Master Plan just landed, and it changes your gap analysis

This is the single most important thing this audit found, and it isn't optional context — it's the ground the rest of the brief needs to be evaluated against.

**What happened:** The Ministry of Physical Infrastructure and Transport and JICA jointly unveiled the *Kathmandu Valley Urban Transport System Master Plan* in early August 2026, with a horizon to 2050. Headline contents:

- **22 infrastructure projects + 13 "transport improvement programmes,"** budgeted around NPR 188 billion, covering elevated highways (Chabahil–Bagmati, Tripureshwor–Maitighar, Bishnumati corridor), underpasses (Maharajgunj, Chabahil–Gaushala tunnel), a new Karmanasha Bridge, Ring Road widening (Gaushala–Tinkune), and upgrades to 107 intersections (23 in a first phase by 2032, phased through 2040), including **"intelligent traffic signals."**
- **A proposed metro/mass-transit corridor** from Ratna Park to Suryabinayak (Bhaktapur), justified by JICA's finding that Kathmandu's east–west corridors already carry 150,000–200,000 passengers/km — above the ~100,000/km threshold JICA treats as the ceiling for road-based transit.
- Officials (including a JICA HQ representative) are on record saying the "focus should now shift from planning to implementation" — an implicit admission that the 2012/2017 versions were not implemented.

**What it does *not* appear to include**, based on everything found in this search: any component describing **dynamic, algorithmic, network-level demand redistribution** — i.e., a system that continuously reads current demand and network state and actively steers trips (private, ride-share, or transit) toward underused capacity in near-real-time. The "13 management programmes" as reported are about **route rationalization, fare/service integration, and physical traffic control** (signals, enforcement, parking) — not a live demand-balancing layer.

**Why this matters for your project, both ways:**

1. **It strengthens the "individual vs. system optimum" framing as the right level to work at** — the master plan operates at the *infrastructure and static-network-design* level (build capacity, redesign routes once), not at the *minute-to-minute demand-shaping* level. That's a genuinely different layer, and it's the one your original idea is aimed at.
2. **It weakens the framing of this as a green-field research contribution to Kathmandu transport planning generally.** The valley now has an officially adopted, funded, 25-year plan. Any project you build should explicitly position itself as **operating within/alongside this master plan** (e.g., "how do you manage demand on the network we already have, between now and 2050, and especially on corridors still years from their master-plan intervention") rather than as a competing vision. A panel or thesis committee that has read the news in August 2026 will ask you this directly.
3. It also gives you a **built-in, current, and citable reason the problem is still unsolved for the next several years at minimum**: even the funded interventions (tunnels, elevated roads, metro) are multi-year to multi-decade builds. Whatever manages demand on the *existing* corridors in the meantime is exactly the gap the master plan leaves open.

---

## 3. Auditing existing solutions (updated map)

| Problem | Existing approach | Status | Limitation | Remaining gap |
|---|---|---|---|---|
| Peak corridor overload, weak network integration | JICA 2012 survey → 2026 Master Plan (22 infra projects, 13 programmes, metro corridor) | **Adopted Aug 2026**, implementation pending, multi-decade horizon | Physical/static; years-to-decades lead time; prior versions (2012, 2017) never implemented | Demand management on the network **as it exists today**, during the implementation gap |
| Route duplication / overlap | 2014 KSUTP three-tier route hierarchy (8 primary / 16 secondary / 42 tertiary) | Still being "proposed for implementation" as of **mid-2026**, 12 years after the report | Static route design; requires an empowered transport authority Kathmandu still doesn't fully have | Not a technical gap — an institutional-capacity and adoption gap. A software layer doesn't fix this by itself. |
| Uneven bus/vehicle supply vs. demand | Bajracharya & Nakarmi (2021) fleet-optimization study (R1) | Academic, one-off Excel-Solver optimization, not deployed | Static — computed once against 163 routes' historical demand | Could this be re-run continuously against live demand rather than a single dataset? |
| Passengers can't find/plan routes | Sajha Plus (live GPS bus tracking, official), Mero Sajha, LocaGo (multi-operator route search), Google Maps | **Deployed and in active use** in 2026 | Single-operator (Sajha Plus) or route-lookup only; none reason about network-wide congestion or redirect demand | Confirms individual-trip tools already exist; a demand-distribution layer is a different product category, not a better version of these |
| Intersection-level congestion | "Intelligent traffic lights" — deployed at ~5 Lalitpur intersections (Kupondole–Jawalakhel) since late 2024/2025; only 35 of 64 signals in the Valley are even functional as of April 2025; Kathmandu proper still runs mostly on manual police signaling | Pilot-stage, geographically narrow, Kathmandu-side lagging Lalitpur | Isolated intersection control, not network-aware, not deployed at scale | — |
| Individual route/journey choice | Graph-based journey planner for KTM's semi-formal transit (2025 study, R11); Google Maps | Academic prototype / global commercial tool | Optimizes the individual trip only; **explicitly not** aware of collective effects | This is the clearest, most literal confirmation of the "individual vs. system optimum" gap in your brief |
| AI/simulation-based traffic control | SUMO-based RL signal-control framework for Kathmandu (2024/25, R9); IoT traffic-management review (R10) | Academic, simulation-only | Signal-timing focus, not route/demand distribution | — |
| Bus priority / BRT | Queue-jump study at Narayan Gopal intersection (R7); BRT feasibility work (R8) | Studied, largely **not implemented** at scale | Corridor-specific, doesn't touch network-level allocation | — |

**Global context you should have and cite:** In July 2026, Google Research published (in *Nature Cities*) the first large-scale, real-world empirical study of exactly the concept your brief is chasing — rerouting a small share of Google Maps trips off ~100 congested segments across 10 US cities to measurably reduce citywide delay and emissions. Their own framing: "optimizing routing system-wide is not yet present" in commercial navigation, even though individual-trip routing has been standard for over a decade, and "large-scale empirical validation remains limited." This is important for two reasons:

1. It confirms your central thesis — individual-optimum routing dominates the market, and system-optimum routing is a genuinely open, live research question, **not solved even by the company with the best global traffic data**.
2. It also means you're not claiming a totally novel idea in the abstract — you'd be claiming a **novel Kathmandu-specific instantiation and empirical test** of a frontier that a major lab only validated at scale a month before you're writing this. That's a defensible framing for a student project: "apply/adapt an approach barely validated in wealthy, GPS-saturated, well-mapped US cities to a semi-formal, GPS-sparse, mixed-mode South Asian network, and see what breaks."

---

## 4. Critically testing the core assumption

> "Kathmandu's congestion can meaningfully be reduced by distributing travel demand across alternative routes/options rather than simply optimizing each individual's fastest route."

**Is it a significant Kathmandu problem?** Yes, on the evidence — JICA's own 2026 figures put some corridors at 150,000–200,000 passengers/km against what it treats as ~100,000/km road-based capacity, and separately reports some roads already running ~20% over intended capacity. That's real, current, and officially quantified.

**Is it already solved?** No — but be precise about what's *not* solved. The physical/infrastructure and static-route-design layers are now covered by an approved, funded 25-year plan (§2). What's *not* addressed by anything found — official plan, academic literature, or deployed app — is a **live, continuously-updating layer that shapes which route/mode/departure time people actually take, based on current network state**, as distinct from (a) fixed infrastructure, (b) fixed route hierarchies, or (c) individually-optimal navigation.

**Is it technically/research-wise meaningful?** Yes, with a caveat. System-optimal vs. user-equilibrium traffic assignment is 60+ years old as a theoretical field (Wardrop, 1952; Braess, 1968). What's still open, and what Google's own 2026 paper says is still open, is *empirical, real-world validation* — especially in low-GPS-penetration, semi-formal-transit contexts like Kathmandu, which is a meaningfully different environment from the 10 US cities Google tested. Kathmandu's OD (origin-destination) data, road-network digitization, and transit-formality are all much sparser, which is itself a research contribution angle (methodologically, not just applying an existing method) — but also a real feasibility risk (§7).

**Is there room for a genuinely new contribution?** Yes, specifically in:
- Doing this for a **semi-formal, multimodal network** (buses + microbuses + tempos + private vehicles + walking) rather than a car-only, GPS-rich network like the US case.
- Doing it with **sparse/estimated OD data** rather than assuming Google/Waze-scale telemetry — which is itself worth documenting as a contribution (what can you do with less data?).
- Framing it explicitly as **"what should happen on the corridors the 2026 Master Plan hasn't reached yet, and won't reach for years."**

**Are you misunderstanding the root cause?** Partially, yes — and this is the most important critical finding of this whole audit. The 2014 route-rationalization plan is a **textbook case of a good technical answer failing for non-technical reasons**: it wasn't under-designed, it was under-*implemented*, over 12 years, seemingly for institutional/governance/authority reasons (no empowered transport authority, fragmented private operators, weak enforcement). If your new system is *also* a good technical answer that assumes willing/coordinated adoption by transport authorities, operators, or a high fraction of travelers, you risk building something technically sound and institutionally unusable — again. This should shape your scope: a **traveler-facing recommendation/decision-support tool** (which doesn't require operator or authority buy-in to produce value — it can ship as an app people choose to use) is much more feasible for a student project than anything that depends on route/fleet **reform actually happening**.

**Is there a better problem hiding underneath?** One is worth naming explicitly: given that (a) route rationalization has stalled for over a decade for institutional reasons, and (b) semi-formal operators are the actual unit of supply, a strong alternate framing is **"decision support for travelers navigating a fragmented, under-coordinated network as it exists today"** rather than "help the network reorganize itself." That reframes the project from *changing the network* to *helping people use the network we already know is dysfunctional, better* — which is more tractable, doesn't depend on institutional cooperation, and still produces a measurable network-level effect if enough people use it (this is literally what the Google Research paper demonstrated).

---

## 5. Candidate problem directions, ranked

| Candidate | Kathmandu relevance | Novelty | Existing lit. coverage | Feasibility (student project) | Measurable impact | Engineering depth |
|---|---|---|---|---|---|---|
| **A. Demand-aware route recommendation** (traveler-facing, network-aware alternative to shortest-path) | High | High — no Kathmandu precedent found; global precedent (Google, July 2026) is brand new | Sparse for Kathmandu specifically; strong international theory (Wardrop/Braess/SO-DTA) and one very recent empirical study to build on | Medium — needs road-network graph + demand estimates + a simulation or small live pilot | Strong — directly comparable to baseline shortest-path via simulation (delay, corridor utilization) | High |
| **B. Dynamic public-transport demand balancing** (continuously matching bus/microbus supply to demand) | High | Medium — extends R1 (static) into a live/adaptive version | R1 exists but is static; some overlap risk with ongoing route-rationalization policy work | Lower — needs live ridership/GPS data you likely don't have access to (only Sajha Yatayat has GPS-tracked fleet; most microbuses don't) | Medium | High |
| **C. Spatial + temporal demand distribution** (route *and* departure-time shifting) | Medium-high | Medium | No Kathmandu-specific work found | Lower — broader scope, harder to bound for a single project | Medium | High, but scope-risk is real |
| **D. What-if / scenario simulation tool for planners** (decision support, not traveler-facing) | High (this is literally what the JICA plan needed and used consultants for) | Medium | JICA/UNESCAP/ADB reports are the "answers"; you'd be building the "instrument" | Medium — a SUMO/graph-based simulator is buildable; but you're competing with plans that already exist and were built by professional consultants over years | Weaker — hard to validate against ground truth without official data access | Medium |
| **E. Multimodal demand optimization** (cars + transit + walking together) | High | Medium | Thin | Low — scope explosion; would swallow a thesis timeline | Medium | Very high |
| **F. Dynamic public-transport route restructuring** (routes themselves adapt to demand, not just recommendations) | High | Medium-high | Overlaps directly with the stalled 2014 KSUTP effort | Low — this is the one most exposed to the "institutional adoption" failure mode identified above | High if adopted, but adoption is exactly the unsolved part | High |

**Recommendation: Candidate A.** It's the strongest combination of novelty, feasibility, and measurability, it doesn't require institutional buy-in to demonstrate value (a traveler can just use it), it has a live, citable, very recent global reference point (Google/Nature Cities, July 2026) to position against, and it's the one most clearly *not* already covered by the 2026 Master Plan, R1, R3/R4, or R11.

---

## 6. Finalized problem definition

### Final problem statement

> Kathmandu Valley's approved 2026 Urban Transport System Master Plan addresses physical capacity (roads, tunnels, a proposed metro corridor) and route-hierarchy reform on a multi-year-to-2050 timeline, and prior route-rationalization proposals (2014 KSUTP) remain largely unimplemented more than a decade after being proposed, for institutional rather than technical reasons. In the meantime, and independent of whether those reforms are ever executed, travelers on Kathmandu's existing road and semi-formal transit network continue to choose routes individually and largely without regard to the network-level effect of that choice, concentrating demand on already-saturated corridors (JICA reports 150,000–200,000 passengers/km on some corridors against a road-based ceiling it treats as ~100,000/km). No system — official, academic, or commercial — currently gives travelers or planners a live, network-aware alternative to individually-optimal ("shortest path") route choice for Kathmandu.

### Why it matters

Congestion costs are already large and worsening (JICA's own gridlock warnings for 2050), the network's formal fixes are years to decades away regardless of what gets built starting now, and the one class of intervention that requires no institutional coordination to deploy — traveler-facing, network-aware recommendation — is untested for Kathmandu and only just empirically validated anywhere (Google/Nature Cities, July 2026).

### Existing solutions (and why they're insufficient here)

- Physical/infrastructure plan (2026 Master Plan) — real, funded, but multi-year/decade lead time; doesn't touch minute-to-minute demand.
- Route rationalization (2014 KSUTP) — technically sound, institutionally stalled for 12+ years.
- Static fleet-allocation research (R1) — one-off, not adaptive, not deployed.
- Individual journey planners (R11, Sajha Plus, Google Maps) — optimize the individual only, by design.
- Intersection-level ITS (Lalitpur pilot) — narrow, isolated, doesn't reach network-level allocation, and much of Kathmandu itself still runs on manual signaling.

### Research gap

A network-aware, demand-distribution layer for Kathmandu's existing multimodal network — operating at the level of route/mode/timing *recommendation*, not infrastructure or route-authority reform — that can be deployed and evaluated without requiring transport-authority or operator cooperation.

### Proposed contribution

A Kathmandu-specific method and prototype for evaluating and recommending demand-distributing route choices, benchmarked against conventional shortest-path selection via simulation on a defined study network, explicitly adapted to Kathmandu's sparse-OD-data, semi-formal-transit conditions — positioned as a complement to, not a competitor of, the adopted 2026 Master Plan.

### Primary research question

> Can demand-aware route recommendations measurably reduce network-level congestion and total travel delay on a defined Kathmandu Valley study network, relative to conventional shortest/fastest-route selection, without imposing unacceptable individual travel-time costs?

### Secondary research questions

1. Which corridors in the chosen study network show the clearest mismatch between demand and capacity using available (or collectible) data?
2. How much simulated demand can be shifted to alternative corridors before those alternatives saturate in turn?
3. What is the individual-vs-network trade-off curve (individual delay added vs. network delay saved), and where's the acceptable threshold?
4. How sensitive are results to Kathmandu's specific data gaps — no valley-wide GPS-tracked private-vehicle or microbus fleet, unlike the Google study's home markets?
5. Does the presence of the 2026 Master Plan's phased interventions (e.g., 23 intersections upgraded by 2032) change which corridors are worth targeting first?

### Hypothesis

A network-aware demand-distribution strategy, simulated on a bounded Kathmandu study network, will reduce total network delay and peak-corridor utilization relative to individually-optimal routing, at an individual travel-time cost within a defined acceptable threshold (e.g., the Google study's benchmark of small, single-digit percentage speed/delay gains from shifting a small share of trips is a reasonable order-of-magnitude target, not a guarantee).

### What success would mean

A working prototype + simulation-based evaluation showing a measurable, statistically credible improvement in network delay/congestion metrics over a shortest-path baseline, on a real (even if small) Kathmandu corridor set, with an honest accounting of the individual-cost trade-off and of what real (not simulated) OD/GPS data would be needed to move beyond simulation.

### Explicitly out of scope

- Anything requiring transport-authority, operator, or government cooperation to function (route reform, fleet reallocation, signal control) — those are Candidates B/C/F, not this one.
- Valley-wide, all-modes deployment — pick one bounded study network.
- Live production deployment with real users — this is a simulation/prototype-level evaluation, not a launched product.
- Departure-time (temporal) distribution — real and interesting (Candidate C) but should stay out unless the route-only version is finished early.
- Building your own competing master plan, metro proposal, or infrastructure recommendation — the 2026 Master Plan already exists; don't re-derive it.

---

## 7. Key risks and unknowns still to investigate

1. **Data availability is the single biggest risk.** Google's July 2026 result rests on Google Maps' GPS-scale telemetry. Kathmandu has no equivalent public dataset. You'll likely need to either (a) get access to the JICA 2012 household-interview / 2011 traffic-survey OD data (R2's underlying dataset may be requestable), (b) use OpenStreetMap + a synthetic/estimated demand model, or (c) collect a small primary dataset yourself. This needs to be resolved before committing to Candidate A.
2. **"Semi-formal transit" is hard to simulate.** Microbuses/tempos don't run fixed schedules or always report GPS; your network graph will need real judgment calls about what counts as a "route."
3. **Where the study-network boundary sits matters a lot** — pick corridors JICA has flagged as already saturated (e.g., the east–west corridors it cites at 150–200k passengers/km) so your baseline congestion claim is independently corroborated, not asserted.
4. **You should read the actual Master Plan document (not just news coverage)** once it's published in full, to confirm precisely what the "13 management programmes" contain — this audit relied on news summaries (Kathmandu Post, Ratopati, Meroauto, Clickmandu), not the primary JICA/Ministry report, which wasn't yet found as a public PDF.
5. **Institutional-adoption risk still applies indirectly**: even a traveler-facing tool needs enough users to have a measurable network effect (this is exactly what the Google paper had to demonstrate). A prototype tested only in simulation sidesteps this, but it's worth naming as a limitation of any real-world claim.

---

## 8. Recommended next research step

Before any implementation: (1) try to obtain or reconstruct an OD/demand dataset for a bounded Kathmandu study area (start with the JICA 2012 survey's public output tables and OpenStreetMap road network); (2) locate and read the full 2026 Master Plan document once released, to confirm the "13 management programmes" don't already include something adjacent to this idea; (3) only then finalize the study-network boundary and simulation approach (SUMO with a system-optimal DTA extension, per the Mehrabani et al. 2022 SB-DSO method, is a reasonable technical starting point once the problem is locked).

---

### Sources

- Bajracharya, A. & Nakarmi, A.M. (2021), *Public Transportation Energy Planning by Network Analysis — Kathmandu Valley*, JACEM. https://nepjol.info/index.php/JACEM/article/view/38273
- JICA (2012), *Data Collection Survey on Traffic Improvement in Kathmandu Valley*. https://openjicareport.jica.go.jp/pdf/12082459_01.pdf
- JICA/MoPIT (2026), *Kathmandu Valley Urban Transport System Master Plan* — coverage: Kathmandu Post (Aug 6, 2026) https://kathmandupost.com/national/2026/08/06/new-kathmandu-transport-master-plan-proposes-metro-rail-linking-ratna-park-and-bhaktapur ; Meroauto (Aug 2026) https://www.en.meroauto.com/rs-82-billion-elevated-highway-plan-proposed-for-kathmandu/ ; Clickmandu (Aug 2026) https://english.clickmandu.com/2026/08/10796/
- ADB/KSUTP (2014), *Kathmandu Sustainable Urban Transport Project* route-hierarchy proposal — coverage: Ratopati (2026) https://english.ratopati.com/story/66490/ ; Nepali Times (Jul 2026) https://nepalitimes.com/first-public-transport-then-only-mass-transit
- UNESCAP (2022), *A Comprehensive Public Transport and Mass Transit Plan for Kathmandu Valley*. https://repository.unescap.org/handle/20.500.12870/6300
- (2025), *An Optimized Graph-Based Implementation for Efficient Journey Planning with Public Transport in Kathmandu Valley*, IJET. https://nepjol.info/index.php/injet/article/download/78657
- Google Research / Nature Cities (Jul 2026), *Urban Congestion Relief Experiments Through Routing-App Interventions*. https://www.nature.com/articles/s44284-026-00443-x ; https://research.google/blog/the-power-of-collaboration-how-we-can-reduce-traffic-congestion/
- Mehrabani et al. (2022), *Proposing a Simulation-Based Dynamic System Optimal Traffic Assignment Algorithm for SUMO*. https://doi.org/10.52825/scp.v3i.119
- OnlineKhabar/Ecosphere/Himalayan Times/New Business Age — Kathmandu/Lalitpur intelligent-traffic-signal coverage (2024–2026), various URLs cited inline above.
- Sajha Yatayat / Sajha Plus, LocaGo app listings — existing deployed journey/tracking tools, cited inline above.
