# MOD — System Design & Build Plan

How the system gets built: architecture, tech stack, repo layout, and
milestones. Two phases with a hard gate between them:

- **Phase A — the simulation system (M1–M4)**: the research instrument.
  Buildable now; nothing blocks it.
- **Gate** — go/no-go on the traveler-facing product, decided by Phase A
  results (paper §5.5 criteria).
- **Phase B — the traveler-facing product (M7+)**: designed here so the
  target is visible, built **only if the gate passes**.

Method and evidence basis live in the paper
([paper/mod-feasibility-study.md](paper/mod-feasibility-study.md)); this
document is engineering only.

---

## 1. Phase A — Simulation system (M1–M4)

### 1.1 Architecture

```text
 research/library (PDFs, CSV)            OSM (Geofabrik extract)
        │                                        │
        ▼                                        ▼
 ┌─────────────┐   zones,OD,counts      ┌──────────────────┐
 │ M1 pipeline │ ─────────────────────► │ M3 SUMO testbed  │
 │  (Python)   │   parquet/csv          │ netconvert + net │
 └─────────────┘                        │ audit + calibrate│
        ▲                               └────────┬─────────┘
        │ QA tests (totals, filters)             │ validated baseline
 ┌──────┴──────┐                                 ▼
 │ M2 model    │  parameters, tolerances  ┌──────────────────┐
 │ spec (yaml) │ ────────────────────────►│ M4 experiment    │
 └─────────────┘                          │ runner (Python)  │
                                          └────────┬─────────┘
                                                   ▼
                                     results/ (parquet + figures)
```

### 1.2 Stack — Phase A

| Layer | Choice | Why (lazy ladder applied) |
| --- | --- | --- |
| Language | **Python 3.12** | SUMO tooling, pandas, everything in one language; no second language justified |
| Env/deps | **uv** (+ committed lockfile) | reproducibility in one tool |
| PDF extraction | **poppler `pdftotext -layout`** via subprocess + **pandas** parsing | already verified working on JICA Vol 4 matrices — no PDF library needed |
| Data wrangling | **pandas + numpy** | standard; nothing exotic required |
| Storage | **plain files**: CSV for hand-editable inputs, Parquet for pipeline outputs, SUMO XML for sim | no database — nothing queries concurrently; files diff in git |
| Simulator | **SUMO** (latest stable): `netconvert`, `duarouter`, `duaIterate.py`, **TraCI/libsumo** for metric extraction | chosen with evidence (paper §5.3); exogenous demand edits match our design |
| Network source | **Geofabrik Nepal OSM extract** → `netconvert` | OSM defensibility documented (GFDRR Open Cities, paper [36]) |
| Manual GIS | **QGIS** (human step, not code) | zone georeferencing from JICA maps + corridor attribute audit |
| Calibration params | TU thesis VISSIM values transferred (library `data-tu-thesis-*`) + saturation-flow checks | only local behavioral data that exists |
| Scenario config | **YAML** files, one per scenario (S0–S3 + surface grid) | config-driven runs; no scenario logic in code |
| Testing | **pytest** — QA-as-tests: matrix row/col totals vs printed totals, growth-factor sanity filter, GEH < 5 check | the paper's acceptance criteria become the test suite |
| Figures | **matplotlib** | final-report figures styled later |
| Compute | local machine | corridor-scale SUMO is cheap; cloud = zero justification |

### 1.3 Repo layout (same repo, grows from current root)

```text
mod/
├── research/            # existing workspace (unchanged)
├── specs/
│   └── model-spec.md    # M2: zones, cordon, time slices, PCU, metrics, tolerances
├── pipeline/            # M1: extraction + demand build
│   ├── extract_od.py    #   JICA Vol4 → od_2011.parquet
│   ├── growth.py        #   DoR CSV → filtered growth factors
│   ├── counts_2019.py   #   JICA 2019 Vol2 → calibration targets
│   └── cordon.py        #   valley OD → corridor OD (JICA §13.4.3.2 method)
├── sim/                 # M3: network + baseline
│   ├── net/             #   OSM extract, netconvert configs, audited .net.xml
│   └── calibrate/       #   baseline demand, duaIterate configs, GEH report
├── experiments/         # M4: runner + scenario configs
│   ├── scenarios/       #   s0-spatial-control.yaml … s3-joint.yaml, surface grid
│   └── run.py           #   config → SUMO run → metrics parquet
├── data/
│   ├── raw/             #   inputs copied from library (gitignored where large)
│   └── processed/       #   parquet outputs (gitignored; rebuildable)
├── results/             #   run outputs + figures (gitignored; rebuildable)
└── tests/               #   pytest QA suite
```

Rule carried over from the library: bulky/rebuildable artifacts stay out of
git; code, configs, specs, and small CSVs go in.

### 1.4 Milestone exit criteria (from the paper, made concrete)

| Milestone | Deliverable | Exit criterion |
| --- | --- | --- |
| M1 | `od_2011.parquet`, `growth_factors.csv`, `counts_2019.parquet` | **DONE 2026-08-15** — 14/14 tests; OD totals validated against printed totals (one documented source discrepancy: person table's unprinted external row, 3,636 trips); 29 stations' growth factors with per-station flag counts. See `pipeline/README.md`. |
| M2 | `specs/model-spec.md` + config schema | **DONE 2026-08-15** — adversarially verified against source PDFs (9 findings fixed, incl. replacing the daily-GEH gate with a ±15% criterion, A7); 138-fact cited base in `specs/facts-extracted.json`; 8 assumptions registered |
| M3 | audited `.net.xml` + validated baseline | **DONE WITH LIMITATION 2026-08-18** — demand calibrated by count-based generation (`pipeline/count_targets.py` → routeSampler): 95% of counted volume at 42 locations, GEH < 5 at 90.5%, above the 85% screening threshold. A7 (±15% daily) was **not** met — 0/77, median 8% of target, gap = 0.51 insertion × 0.20 allocation — and is superseded, not deleted (spec §7). Limitation: the network inserts ~49% of the count-matched demand (176,370 loaded), so scenario metrics are relative to the baseline under identical settings, never absolute (paper §5.6). History: starved (single-edge injection) → gridlocked (priority junctions) → collision-deleted (sublane, A13) → count-matched |
| M4 | results parquet + figures for surface, S0–S3, robustness | every run reproducible from YAML + seed; compliance-threshold curves produced |

## 2. The Gate (after M4)

Product build proceeds **only if** (paper §5.5):

1. Delay relief at binding intersections is **superlinear** in removed peak
   demand within the evidence-bounded region (p_t ≤ 25%, Δt ≤ 30 min), and
2. the compliance threshold for measurable effect is **at or below
   participation rates achieved by cited programs** (INSTANT/INSINC-level),
   and
3. the result survives robustness runs (demand ±20%, behavioral-parameter
   halving).

Fail any → publish the negative/bounded result, stop at Phase A. That
outcome is a success condition of the research, not a failure.

## 3. Phase B — Traveler-facing product (conditional)

Concept fixed by the evidence, not by preference: **an anchored
departure-time incentive platform** (INSTANT design transferred). Not a
navigation app — the spatial lever is falsified. Verification is anchored
at institutions because Kathmandu has no smart-card/telemetry layer to
verify travel any other way (paper §4.4, §2.4).

### 3.1 Product shape

- **Traveler PWA** — enroll, see personal off-peak window, check in, track
  credits, raffle results. PWA first: check-in is a QR scan at the anchor
  gate, needs no GPS or native app. Native wrapper only if PWA friction is
  proven.
- **Anchor kiosk/gate flow** — QR poster or badge-desk integration at the
  employer/school; arrival timestamp is the ground truth (INSTANT's
  badge-swipe lesson: verification quality decides credibility).
- **Incentive engine** — credits by arrival window; **raffle-based
  payouts** (dominates fixed payments on cost-effectiveness in every cited
  deployment); anti-gaming: pre-enrollment baseline weeks, per-person caps.
- **Admin dashboard** — for the anchor institution: participation, shift
  curves, payout log.
- **Measurement plane** — the point of the pilot: baseline vs intervention
  weeks, arrival-time distributions, and corridor observation (DoR station
  pulls + manual counts) so results are claimable.

### 3.2 Stack — Phase B

| Layer | Choice | Why |
| --- | --- | --- |
| Backend | **Python + FastAPI** | continuity with Phase A team/skills; one language across project |
| DB | **PostgreSQL** | boring, correct; events + enrollments are relational; no PostGIS until a geo query actually exists |
| Frontend | **one Next.js app** (PWA + admin routes) | single deployable; no separate admin stack |
| Auth | phone-number OTP | Nepal norm; no password support burden |
| Notifications | **SMS via Sparrow SMS** primary; web push secondary | reach beats elegance for motorcycle commuters; iOS web-push is unreliable |
| Payouts | **eSewa / Khalti** wallet transfer for raffle winners | the realistic Nepali payout channel; cash fallback via anchor HR |
| Hosting | **single VPS** (or Fly/Railway) + Postgres backup | pilot-scale (one anchor, 10²–10³ users); no k8s, no microservices |
| Analytics | Postgres + scheduled Python jobs → the same parquet/figure toolchain as Phase A | reuse, not new infra |

### 3.3 Pilot design constraints (carried from evidence)

- One anchor institution first (employer or school on the study corridor).
- Baseline measurement weeks **before** incentives start (Spitsmijden
  anti-gaming lesson).
- Budget expectation: INSTANT achieved its effect on ~US$2k of raffle
  payouts — pilot budget is small by design.
- Durability check built into the calendar: measure after incentives pause
  (evidence says retiming decays; quantify it, don't hide it).
- Ethics/consent + data minimization plan required before any human trial —
  institutional approval path to be confirmed with the supervising
  department. ★ unresolved.

## 4. Deliberate exclusions (both phases)

No microservices, no Kubernetes, no cloud data warehouse, no ML models, no
live traffic ingestion, no map tiles server, no native apps at pilot scale,
no database in Phase A. Each returns only when a concrete need appears;
`ponytail:` markers in code will flag any shortcut with a known ceiling.

## 5. Risks and upgrade paths

| Risk | Mitigation / upgrade path |
| --- | --- |
| OD extraction messier than the verified sample pages | fall back to page-targeted manual entry for bad zones; QA totals catch errors |
| OSM corridor attributes wrong | manual audit pass is already a milestone step (M3); 2019 signal data as cross-check |
| **2019 15-min turning-movement tables are raster images, not text** (found in M1: only Table 4.1 daily leg PCU summaries extract; spec sheets A4-2..11 are jpx images) | **Resolved without OCR.** The OCR route stayed closed (research/07 verdict); instead the daily leg totals are distributed over the measured A1 hourly profile into hourly count targets (`pipeline/count_targets.py`), which restores an hourly tier for GEH and doubles as the demand target |
| SUMO exogenous-shift design too coarse | upgrade path: MATSim coupling (library `pivot-matsim-sumo-coupling.pdf`) |
| Transferred behavioral params wrong | RQ4 sensitivity halving; upgrade: M5 local SP survey |
| Gate passes but no anchor institution signs on | product concept requires exactly one willing anchor — recruit during Phase A, not after |
| nepjol/library gaps (2 papers) | manual browser fetch; not load-bearing for any Phase A step |
