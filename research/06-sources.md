# Sources — Annotated Bibliography

Verification status reflects the 2026-08-14 audit. **Verified** = checked
against the source and accurately characterized. **News-only** = known
through press coverage; primary document not yet read.

---

## Kathmandu — research literature

| Ref | Source | What it establishes | Status |
| --- | --- | --- | --- |
| R1 | Bajracharya & Nakarmi (2021), *Public Transportation Energy Planning by Network Analysis — Kathmandu Valley*, JACEM. <https://nepjol.info/index.php/JACEM/article/view/38273> | 163 PT routes studied; vehicle allocation optimized (Excel Solver); ~41% fleet reduction possible on modeled routes. Static, one-off. | Verified |
| R2 | JICA (2012), *Data Collection Survey on Traffic Improvement in Kathmandu Valley*. <https://openjicareport.jica.go.jp/pdf/12082459_01.pdf> | 18,100-household survey; chronic congestion, weak PT, disorderly urbanization; road+PT+land-use must integrate. Underlying OD data is the G1 target. | Verified |
| R3 | JICA / MoPIT (2014), *Data Collection Survey on Urban Transport in Kathmandu Valley*. <https://openjicareport.jica.go.jp/pdf/12345484_01.pdf> | The 8/16/42 three-tier route-rationalization proposal (66 routes) — with A2, proof of the implementation gap. | Verified |
| R4 | UNESCAP (2022), *A Comprehensive Public Transport and Mass Transit Plan for Kathmandu Valley*. <https://repository.unescap.org/handle/20.500.12870/6300> | Reviews decades of plans; PT still inadequate; corridor and mode recommendations. | Verified |
| R7 | Queue-jump lane study, Narayan Gopal intersection, IJET. <https://www.nepjol.info/index.php/injet/article/view/72572> | Bus-priority studied at corridor level; not implemented at scale. | Verified |
| R8 | Bus priority / BRT feasibility, IJET-ID. <https://nepjol.info/index.php/injetindev/article/view/82492> | BRT feasibility incl. governance obstacles. | Verified |
| R9 | AI-Driven Traffic Management Framework for Kathmandu, Far Western Review. <https://www.nepjol.info/index.php/fwr/article/view/79872> | SUMO-based RL **signal control**; also precedent for Thapathali–Koteshwor as a study corridor. Not demand distribution. | Verified |
| R10 | IoT in Traffic Management in Kathmandu Metropolitan City, SRA. <https://nepjol.info/index.php/sra/article/view/74284> | IoT sensing/control review. | Verified |
| R11 | *Optimized Graph-Based Journey Planning with Public Transport in Kathmandu Valley* (2025), IJET. <https://nepjol.info/index.php/injet/article/download/78657> | Individual multimodal shortest-path; ~18% individual journey-time gain; explicitly not network-aware. The cleanest local example of individual-only optimization. | Verified |
| R12 | Kathmandu congestion review (2025), JACEM. <https://www.nepjol.info/index.php/JACEM/article/view/84536> | Argues for multimodal, data-driven approach + institutional reform. | Cited, not deeply audited |

## Kathmandu — plans, policy, deployed systems

| Ref | Source | What it establishes | Status |
| --- | --- | --- | --- |
| A1 | JICA/MoPIT (2026), *Kathmandu Valley Urban Transport System Master Plan* — coverage: Kathmandu Post (Aug 6 2026) <https://kathmandupost.com/national/2026/08/06/new-kathmandu-transport-master-plan-proposes-metro-rail-linking-ratna-park-and-bhaktabur> ; Meroauto <https://www.en.meroauto.com/rs-82-billion-elevated-highway-plan-proposed-for-kathmandu/> ; Clickmandu <https://english.clickmandu.com/2026/08/10796/> | 22 projects + 13 programmes, NPR ~188B, metro corridor, 107 intersections, horizon 2050; corridor loads 150–200k passengers/km vs ~100k ceiling. **Primary document unread — gating task G2.** | News-only |
| A2 | KSUTP implementation-gap coverage: Ratopati (2026) <https://english.ratopati.com/story/66490/> ; Nepali Times (Jul 2026) <https://nepalitimes.com/first-public-transport-then-only-mass-transit> | 2014 route hierarchy still un-implemented mid-2026; framed as institutional, not technical. | Verified (coverage) |
| A4 | Sajha Plus, Mero Sajha, LocaGo app listings | Deployed individual-trip tools; single-operator GPS tracking (Sajha) or route lookup only. | Verified |
| A5 | OnlineKhabar / Ecosphere / Himalayan Times / New Business Age, smart-signal coverage 2024–26 | ~5 smart intersections (Lalitpur); 35/64 valley signals functional (Apr 2025); Kathmandu largely manual control. | Verified (coverage) |

## Global / theory

| Ref | Source | What it establishes | Status |
| --- | --- | --- | --- |
| A3 | Google Research / *Nature Cities* (Jul 2026), routing-app congestion interventions. <https://www.nature.com/articles/s44284-026-00443-x> ; <https://research.google/blog/the-power-of-collaboration-how-we-can-reduce-traffic-congestion/> | First large-scale real-world validation of system-aware rerouting; small trip share off ~100 segments, 10 US cities, measurable citywide gains. Frames system-optimal routing as commercially absent. | Verified |
| A6 | Mehrabani et al. (2022), *Simulation-Based Dynamic System Optimal Traffic Assignment for SUMO* (SB-DSO). <https://doi.org/10.52825/scp.v3i.119> | Candidate simulation method once problem is locked. | Verified |
| — | Wardrop (1952); Braess (1968) | User equilibrium vs. system optimum; paradox of added capacity. Theoretical foundation — settled theory, open empirics. | Canonical |

## Notes

- R5/R6 from the original brief (JICA master-plan project pages) are
  superseded by A1: the plan is no longer "in progress" — it was unveiled
  August 2026. Cite R6's route-overlap description as background only.
- Original raw material (chat transcript, first brief, audit prompt and
  outputs) is preserved in `archive/`.
