# Research Library — Index

Collected primary documents and papers for MOD Phase 0 (gathered
2026-08-14). All PDFs verified (`%PDF` header, >50KB). Sources that could
not be downloaded are listed under **Link-only** — fetch manually.

★ = needs user verification before treating as established.

---

## Master Plan & official planning (`masterplan-`)

| File | What it is | Source |
| --- | --- | --- |
| masterplan-jica-record-of-discussions-2023.pdf (9.9MB, scanned) | Signed MoPIT–JICA Record of Discussions for the 2026 Master Plan project — **the only official document of this exact project publicly available**: project description, outputs, report sequence (ICR→…→DFR→FR), schedule | [jica.go.jp RD.pdf](https://www.jica.go.jp/english/about/policy/environment/id/asia/south/a_b_fi/nepal/__icsFiles/afieldfile/2023/12/12/RD.pdf) |
| masterplan-predecessor-2017-kv-urban-transport-improvement-final-vol1.pdf | 2017 predecessor master plan (Final Report Vol. II "Master Plan and Pilot Project") — contains TDM menu Table 8.4.1 | [12289682_01.pdf](https://openjicareport.jica.go.jp/pdf/12289682_01.pdf) |
| masterplan-predecessor-2019-kv-transport-sector-survey-final.pdf | 2019 Data Collection Survey final report ★ (same file as data-jica-2019-…-vol01; see dating note below) | [12345484_01.pdf](https://openjicareport.jica.go.jp/pdf/12345484_01.pdf) |
| masterplan-jica-mlit-urban-transport-briefing-2025.pdf | JICA briefing (Mar 2025) with case-study section on the Master Plan project | [mlit.go.jp](https://www.mlit.go.jp/toshi/content/001879467.pdf) |
| masterplan-related-jica-traffic-management-project-almec-note.pdf | Companion JICA "Urban Transport Management" project note (107-intersection/signal programme) | [almec.co.jp](https://www.almec.co.jp/profile/pdf/report_Kathmandu~topic_072.pdf) |

**Dating note (RESOLVED):** report 12345484 title page confirms it is the
**July 2019** "Data Collection Survey on Urban Transport in Kathmandu
Valley" Final Report (Oriental Consultants Global / PADECO). The earlier
audit's "2014" label was wrong; the 8/16/42 route hierarchy is ADB KSUTP
(2014), a separate document.

## Demand / network data (`data-`)

| File | What it is | Source |
| --- | --- | --- |
| data-jica-2012-traffic-survey-vol01…06.pdf (6 files) | JICA 2012 Data Collection Survey. **Vol 4 = full 50×50 person-trip OD matrix (2011) + per-mode vehicle OD matrices, text-extractable.** Vol 2 = counts, screenlines, intersection saturation (Table 6.2.12). Vol 3 = demand models | [12082459_01…06.pdf](https://openjicareport.jica.go.jp/pdf/12082459_01.pdf) |
| data-jica-2017-urban-transport-vol01–02.pdf | JICA 2017 project report. Vol 1 = updated demand model, V/C assignment (inside-RR avg 1.22). Vol 2 §13.4 = **corridor-OD extraction recipe** (cordon method, Thapathali–Maitighar) | [12289682_01/_02.pdf](https://openjicareport.jica.go.jp/pdf/12289682_02.pdf) |
| data-jica-2019-urban-transport-survey-vol01–02.pdf | JICA 2019 survey. Vol 2 appendix = **15-hour classified turning-movement counts at 9 corridor intersections** (Koteshwor…Jadibuti axis, 15-min intervals, 9 vehicle classes, signal timings, queues). Vol 1 = node-to-node OD of Maitighar–Thapathali–Tripureshwor cluster | [12345484_01/_02.pdf](https://openjicareport.jica.go.jp/pdf/12345484_02.pdf) |
| data-dor-ssrn-aadt-kathmandu-valley-stations.csv | Scraped DoR HMIS: 29 valley/rim stations × FY 2011/12–2024/25 AADT (+PCU, per-year hourly-detail URLs). Growth ratios for OD updating | [ssrn.dor.gov.np](https://ssrn.dor.gov.np/) (POST `traffic_controller/get_summary`) |
| data-ato-kathmandu-transport-profile-2024.pdf | Asian Transport Observatory Kathmandu profile (Dec 2024) — recent mode shares, scaling factors | [asiantransportobservatory.org](https://asiantransportobservatory.org/) |
| data-tu-thesis-vissim-calibration-kathmandu.pdf | TU/IOE Pulchowk thesis: GA-calibrated VISSIM driving-behavior parameters for Kathmandu heterogeneous traffic (transferable to SUMO) | [elibrary.tucl.edu.np](https://elibrary.tucl.edu.np/) |

## Congestion-mechanism evidence (`evidence-`)

| File | Key finding |
| --- | --- |
| evidence-maitighar-tinkune-bottleneck-2017.pdf | 6,465 capital-hours lost/working day; buses >70% of loss; **78–80% of traffic is through-traffic**; damage located at point bottlenecks ([IOEGC-2017-81](http://conference.ioe.edu.np/ioegc2017/papers/IOEGC-2017-81.pdf)) |
| evidence-thapathali-intersection-performance-2023.pdf | LOS F, 99.6 s/veh delay; reconfiguration alone → 24.1 s/veh (−76%) ([IOEGC-13-004](https://conference.ioe.edu.np/publications/ioegc13/IOEGC-13-004-011.pdf)) |
| evidence-new-baneshwor-signal-improvement-2017.pdf | LOS F both peaks; flyover+phasing −80% travel time (simulated) |
| evidence-new-baneshwor-lane-use-restriction-2023.pdf | Lane reallocation alone only −5–19% delay — management gains small when junction deeply oversaturated |
| evidence-saturation-flow-delay-model-koteshwor-tinkune-jadibuti-2014.pdf | Kathmandu-specific PCU/saturation-flow models; non-lane-based operation degrades signal capacity |
| evidence-reversible-lane-jadibuti-koteshwor-2021.pdf | Tidal imbalance significant; reversible lanes cut worst queues >50%, avg travel time only ~11% ([NJCE](https://civil.pcampus.edu.np/journal/index.php/njce/article/view/2.1-1), TLS cert expired) |
| evidence-roadside-friction-midblock-speed-2023.pdf | Only "vehicle entry" statistically significant; max friction −14% speed — friction second-order on mid-blocks |
| evidence-roadside-friction-los-pokhara-2022.pdf | Friction→LOS elasticity (Pokhara; transferability limited) |
| evidence-bus-dwell-time-kathmandu-2022.pdf | Cash fares +1.39 s/pax boarding; crowding lengthens dwell |
| evidence-bus-bay-behavior-thapathali-2014.pdf | Dwell driven by boarding/fares; bus bay did not disrupt adjacent lanes except during upstream jams |
| evidence-bus-stops-ringroad-kalanki-koteshwor-2019.pdf | Ring Road bus-stop operations |
| evidence-bus-stop-consolidation-lagankhel-khokana.pdf | Stop consolidation study |
| evidence-microbus-route-delay-kathmandu-2015.pdf | Route delays split: stop/fare "operational" vs intersection "fixed" delay |
| evidence-onstreet-parking-new-road-2021.pdf | Core-area parking near/beyond capacity ([IJIERT](https://repo.ijiert.org/index.php/ijiert/article/view/157)) |
| evidence-public-transport-optimization-kathmandu-easts-2025.pdf | Commuter dissatisfaction: overcrowding, irregularity, no integration ([EASTS Vol 15](https://easts.info/on-line/proceedings/vol.15/pdf/I_PP4016.pdf)) |
| evidence-public-transport-banasthali-sundhara-2021.pdf | PT service study, Banasthali–Sundhara |
| evidence-macroscopic-flow-jadibuti-suryabinayak-2014.pdf | Macroscopic flow modeling, Araniko corridor |
| evidence-rastra-bank-chowk-intersection.pdf | Intersection case study |
| evidence-kathmandu-traffic-concerns-overview-2023.pdf | General review ([arXiv 2306.06121](https://arxiv.org/pdf/2306.06121)) — **low-quality student review, cite with care** ★ |

## Pivot evidence base — temporal + mode-shift demand distribution (`pivot-`)

Collected 2026-08-14 for the Phase-0 pivot (departure-time + mode-shift nudging).

| File | What it is | Source |
| --- | --- | --- |
| pivot-spitsmijden-overview.pdf | Donovan, review of 4 Dutch Spitsmijden peak-avoidance reward experiments; per-experiment behavior-change table (dep-time 4–35%, mode 4–16%) | [vtpi.org](https://www.vtpi.org/spitsmijden.pdf) |
| pivot-instant-bangalore-netecon.pdf | Merugu/Prabhakar/Rama, INSTANT Bangalore-Infosys pilot (NetEcon 2009): pre-8am arrivals doubled, bus commute 71→54 min, total rewards Rs 96,000 | [stanford.edu](https://web.stanford.edu/~balaji/papers/NetEcon_final.pdf) |
| pivot-instant-bangalore-final-report.pdf | Stanford PEEC funded-project final report on INSTANT | [stanford.edu](https://web.stanford.edu/group/peec/cgi-bin/docs/transportation/research/Final%20Report%20-%20An%20Incentive%20Mechanism%20for%20Reducing%20Congestion-Related%20Costs%20in%20Transportation%20Systems%20-%20A%20Pilot%20Program%20in%20India.pdf) |
| pivot-insinc-singapore.pdf | Pluntke & Prabhakar, INSINC platform (JOURNEYS 2013): 7.49% peak-shift overall, 10.1% for ≥5-peak-trip commuters | [stanford.edu](https://web.stanford.edu/~balaji/papers/13INSINC.pdf) |
| pivot-capri-stanford-trb2015.pdf | Zhu et al., Stanford CAPRI (TRB 2015): participants 21.2% less likely in AM peak, 13.1% PM | [microsoft.com](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/06/trb2015-3.pdf) |
| pivot-incentives-comparison-berkeley.pdf | "Which is the biggest carrot?" — cross-comparison of non-traditional demand-management incentives | [connected-corridors.berkeley.edu](https://connected-corridors.berkeley.edu/sites/default/files/Comparing%20Non-Traditional%20Incentives%20for%20Demand%20Management.pdf) |
| pivot-fhwa-incentives-compendium.pdf | FHWA HOP-18-071 "Expanding Traveler Choices through the Use of Incentives" — compendium incl. time-of-travel shift programs (ch. 3) | [ops.fhwa.dot.gov](https://ops.fhwa.dot.gov/publications/fhwahop18071/fhwahop18071.pdf) |
| pivot-gravert-nudges-incentives-pt.pdf | Gravert & Olsson Collentine (CEBI WP 10/19, publ. JEBO 2021): 32,500-person field experiments — nudges = tight zero; free-period incentives → durable PT uptake via habit formation | [econ.ku.dk](https://www.econ.ku.dk/cebi/publikationer/working-papers/CEBI_WP_10-19.pdf) |
| pivot-matsim-sumo-coupling.pdf | SUMO 2020 conf. paper: sequential MATSim–SUMO tool-coupling (departure-time/mode replanning in MATSim, microsimulation in SUMO) | [eclipse.dev/sumo](https://eclipse.dev/sumo/documents/2020/SUMO2020_paper_44.pdf) |

### Pivot link-only (paywalled or fetch-blocked)

- [Knockaert et al. 2012, "The Spitsmijden experiment: A reward to battle congestion", Transport Policy 24](https://www.sciencedirect.com/science/article/abs/pii/S0967070X12001229) — paywalled
- [Ben-Elia & Ettema 2011, "Rewarding rush-hour avoidance", TRA 45(7)](https://ideas.repec.org/a/eee/transa/v45y2011i7p567-582.html) — paywalled; green-OA docx at [eprints.uwe.ac.uk/14803](http://eprints.uwe.ac.uk/14803/1/BenElia_Ettema_TRA_revised2_3.docx) (server unreachable during collection)
- [Kumar, Bhat, Pendyala, You, Ben-Elia, Ettema 2016, "Impacts of Incentive-Based Intervention on Peak Period Traffic", TRR 2543](https://journals.sagepub.com/doi/10.3141/2543-20) — paywalled; transfers Spitsmijden response rates into a regional simulation (method template)
- [Li, Huang, Yang 2020, "Fifty years of the bottleneck model", TR-B 139](https://pmc.ncbi.nlm.nih.gov/articles/PMC7333998/) — OA copy behind AWS-WAF captcha
- [Zou et al. 2019, Beijing pre-peak discount retiming via smart-card data, J. Adv. Transp.](https://onlinelibrary.wiley.com/doi/10.1155/2019/6873912) — CC-BY but Cloudflare-blocked
- [Yang, Long et al. 2024, "Exploring travelers' responses to a prepeak discount fare policy…Beijing subway", TRA](https://www.sciencedirect.com/science/article/abs/pii/S0965856424003835) — paywalled; key: 2016 trial produced no discernible peak reduction
- [Understanding peak avoidance commuting by subway (Beijing), Utrecht Univ. thesis PDF](https://dspace.library.uu.nl/bitstream/handle/1874/432735/Understanding_peak_avoidance_commuting_by_subway_an_empirical_study_in_Beijing.pdf?sequence=1) — dspace fetch failed
- [MIT RCT in travel-demand management (dspace 1721.1/127271)](https://dspace.mit.edu/handle/1721.1/127271) — AWS-WAF blocked; null result across treatment arms
- [FEATHERS-HCMC motorcycle TDM scenarios, Procedia CS 2023 (OA)](https://www.sciencedirect.com/science/article/pii/S1877050923006075) — JS-challenge blocked
- [Jakarta BRT & motorcycle use, Case Studies on Transport Policy 2022](https://www.sciencedirect.com/science/article/abs/pii/S2213624X22001407) — paywalled
- [Khon Kaen BRT modal-shift SP study, IATSS Research (OA page)](https://www.sciencedirect.com/science/article/pii/S0386111215000138)
- [Modal shift & transport energy, Kathmandu Valley (72.2% of motorcycle users SP-willing to shift to PT)](https://www.academia.edu/56811240/Assessing_the_Role_of_Modal_Shift_in_Minimizing_Transport_Energy_Consumption_a_Case_Study_of_Kathmandu_Valley) — academia.edu login-walled
- [IPS Commons, "Shifting travel demand" (Singapore FPPT: peak/pre-peak ratio 2.7→2.1)](https://ipscommons.sg/shifting-travel-demand/)
- [The MATSim book (OA), esp. time-allocation mutator / co-evolutionary replanning](https://matsim.org/the-book/)

## Theory & canonical references (`theory-`)

Recovered 2026-08-14 (second collection pass).

| File | What it is | Source |
| --- | --- | --- |
| theory-wardrop-1952-road-traffic-research.pdf | Wardrop (1952) — user equilibrium vs system optimum, the canonical foundation | [irisa.fr mirror](https://www.irisa.fr/) |
| theory-braess-2005-paradox-translation.pdf | Braess paradox, official English translation (Transportation Science 2005) | Braess's RUB homepage |
| theory-braess-1968-original-german.pdf | Braess (1968) original | Braess's RUB homepage |
| theory-google-routing-app-congestion-relief-2026.pdf (+ -correction.pdf) | **Google / Nature Cities (Jul 2026), open access full text** — routing-app congestion-relief experiments, 10 US cities | [nature.com s44284-026-00443-x](https://www.nature.com/articles/s44284-026-00443-x) |

## Second-pass recoveries (Wayback Machine — nepjol down globally)

Added to their prefix families; recovered from archived galley URLs:

- `evidence-urban-congestion-multifaceted-kathmandu-2025.pdf` — JACEM 84536; congestion cost ~NPR 116bn/yr
- `evidence-ktft-expressway-traffic-dispersal-2024.pdf` — KTFTJ 70414, valley V/C assignment
- `evidence-satdobato-intersection-injet.pdf` — INJET 82461
- `evidence-ai-traffic-management-framework-fwr-2025.pdf` — FWR 79872 (SUMO framework)
- `data-kathmandu-gtfs-jie-2020.pdf` — JIE 32190, academic GTFS (data itself never published)
- `data-gfdrr-open-cities-kathmandu-report.pdf` — GFDRR Open Cities Kathmandu (OSM defensibility)
- `masterplan-adb-ksutp-completion-report-2020.pdf` — ADB KSUTP Project Completion Report (June 2020, Loan 2656; notes the restructuring plan **wasn't approved**)
- `masterplan-adb-ksutp-restructuring-maya-factsheet.pdf` — CEN MaYA fact sheet summarizing the 3-tier restructuring

Recovery trick for future nepjol outages: `https://web.archive.org/web/<ts>id_/<nepjol download URL>` works if the *download* URL (not view page) was ever captured.

## Link-only (fetch manually)

### Still unobtainable — manual browser download needed

- [INJET 95704](https://www.nepjol.info/index.php/injetindev/article/download/95704/72424) — Exclusive bus lane Kathmandu–Bhaktapur (−7–13% alone, −20–23% with signal priority). DOI 10.3126/injet-indev.v2i2.95704. Only OA copy is nepjol (Unpaywall-confirmed); zero Wayback captures. Retry when nepjol recovers.
- [INJET 82531](https://www.nepjol.info/index.php/injetindev/article/download/82531/63126) — New Baneshwor PCU/performance. DOI 10.3126/injet-indev.v2i1.82531. Same situation.
- [2014 SMEC "Public Transport Restructuring" report](https://pdfcoffee.com/public-transport-restructuring-pdf-free.html) — never published by ADB (PCR: plan not approved); sole full copy on pdfcoffee, Cloudflare-blocked to fetchers — **downloadable manually in a browser**.

### Official / institutional

- [JICA 2017 FR catalog](https://openjicareport.jica.go.jp/710/710/710_116_12289682.html) · [2019 survey catalog](https://openjicareport.jica.go.jp/710/710/710_116_12345476.html)
- [JICA ODA project page 202109574](https://www.jica.go.jp/oda/project/202109574/index.html) · [disclosure page](https://www.jica.go.jp/english/about/policy/environment/id/asia/south/a_b_fi/nepal/pj8nfn000000o56i.html) · [press index 2026](https://www.jica.go.jp/information/press/2026/index.html)
- [JICA press Dec 2025 — Koteshwor–Jadibuti ODA loan NPR 31.76bn](https://www.jica.go.jp/information/press/2025/20251204_11.html)
- [ADB KSUTP project docs](https://www.adb.org/projects/44058-013/main) · [ADB 2010 sector assessment (source of the "road pricing" line)](https://www.adb.org/sites/default/files/linked-documents/44058-01-nep-ssa.pdf)
- DoR "Statistics of National Highway 2022-23" — 167MB, road inventory only, no AADT: Google Drive id `14yVDt0GUOnstKGv439mBuOxZujEFW2go` (via dor.gov.np publications)
- [neogeomat/yatayat (GitHub)](https://github.com/neogeomat/yatayat) — Kathmandu PT routes from OSM relations via Overpass

### 2026 Master Plan news coverage (basis of G2 reconstruction)

- [Kathmandu Post, Aug 6 2026](https://kathmandupost.com/national/2026/08/06/new-kathmandu-transport-master-plan-proposes-metro-rail-linking-ratna-park-and-bhaktapur)
- [Ratopati EN 73392](https://english.ratopati.com/story/73392/) (project director quote: company model, route management, institutional reform) · [Ratopati EN 66490](https://english.ratopati.com/story/66490/) (ADB KSUTP hierarchy — distinct from JICA plan)
- Meroauto: [23-intersections priority](https://www.en.meroauto.com/23-key-kathmandu-intersections-prioritized-in-plan-to-upgrade-107-junctions/) · [car-free zones](https://www.en.meroauto.com/three-kathmandu-valley-areas-proposed-as-car-free-zones/) · [5-yr digitization (enforcement-scoped)](https://www.en.meroauto.com/nepal-sets-five-year-deadline-to-digitize-entire-transport-sector/)
- Clickmandu EN: [10796](https://english.clickmandu.com/2026/08/10796/) · [10813 (metro detail)](https://english.clickmandu.com/2026/08/10813/) · NP: [477241 (intersections)](https://clickmandu.com/2026/07/477241.html)
- [NepalAuto (tunnel/cycle/safety/emergency items, NP)](https://nepalauto.com/kathmandu-valley-road-tunnel-plan-jica/)
- [KP, Jun 13 2026 — Tinkune/Jadibuti flyover delay](https://kathmandupost.com/national/2026/06/13/tinkune-jadibuti-flyover-faces-delay-despite-secured-financing)
- Mirrors used for paywalled/blocked full text: bnkharel.wordpress.com (Karobar 403180, Gorkhapatra 217742), hamropatro.com, sharehubnepal.com

## Watchlist (check periodically)

1. **mopit.gov.np notice board** — SEA public-suggestion notice reported due mid-Aug 2026 (ministry renamed "Ministry of Infrastructure Development", same domain)
2. Cabinet approval of the Master Plan — reported "within 2026"
3. openjicareport.jica.go.jp — final report publication (likely 2027+; repository lags years)
4. nepjol.info recovery (down globally as of 2026-08-14, Wayback origin-523) — fetch INJET 95704 + 82531
5. April 2026 government office-hours change (10:00→9:00, 5-day week, per myrepublica) — verify implementation; if real, it is a natural experiment (see [../08-option-space.md](../08-option-space.md) A3)
