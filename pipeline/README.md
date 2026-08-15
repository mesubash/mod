# Pipeline

Provenance: `extract_od` reads the JICA 2012 traffic survey Vol. 4 appendix,
`counts_2019` reads the JICA 2019 urban transport survey Vol. 2, `growth` reads
a scrape of DoR SSRN AADT station pages — all in
[`../research/library/`](../research/library/README.md), which lists source URLs.

Run from the repo root with `uv run python -m pipeline.<module>` (direct
`python pipeline/<x>.py` fails: the modules import `pipeline.common` as a
package). The two PDF modules need `pdftotext` (poppler) on PATH. Checks:
`uv run pytest -q`.

## extract_od.py

Input: `research/library/data-jica-2012-traffic-survey-vol04.pdf`.

Parses the five printed 2011 OD tables (person trip; motorcycle, car, truck,
bus vehicle trip) from `pdftotext -layout` output. Each table prints as two
column blocks, detected by their 3-digit zone-code header rows and rejoined
per origin; every matrix is validated against its printed row, column, and
grand totals before writing. External cordon zones 900/901 are dropped,
leaving the 50 survey zones in long form.

Output: `data/processed/od_2011.parquet`, 12,500 rows (5 modes x 50 x 50):
`origin_zone` int, `dest_zone` int, `mode` (`person_all`, `motorcycle`,
`car`, `truck`, `bus`), `trips` int.

Run: `uv run python -m pipeline.extract_od`

Caveats: the person table's printed column totals include an unprinted
external-901 origin row (3,636 trips); validation allows that shortfall only
if it is nonnegative and equals the grand-total gap. The vehicle tables
match their printed totals exactly.

## counts_2019.py

Input: `research/library/data-jica-2019-urban-transport-survey-vol02.pdf`.

Slices the extracted text between the "Table 4.1 Summary of Traffic Volume
Data" heading and "Appendix 5", then a row regex captures each leg-direction
record (intersection, leg, direction, observed PCU, hours observed, 24h PCU).
The row count is enforced: 77 leg-directions x 3 metrics = 231 rows.

Output: `data/processed/counts_2019.parquet`, 231 rows: `intersection` str
(11 names; Tinkune appears as three sub-intersections South/West/North,
"Jadhibuti" keeps the source spelling), `leg` int, `direction` (`in`, `out`),
`metric` (`observed_pcu`, `hours_observed`, `pcu_24h`), `value` float.

Run: `uv run python -m pipeline.counts_2019`

Ceiling (module ponytail note): only Table 4.1 is text in the PDF; the
15-minute classified turning-movement data (spec sheets A4-2..11, flow
diagrams, pie/line charts) is embedded images and is not extracted. Upgrade
path: OCR/camelot pass over those pages.

## growth.py

Input: `research/library/data-dor-ssrn-aadt-kathmandu-valley-stations.csv`
(29 valley/rim stations, FY 2011/12-2024/25).

Per station, finds the longest run of surveys whose year-over-year growth
ratios on `aadt_pcu`, annualized across survey gaps, stay within 0.5-2.0,
and computes CAGR over that run (ties keep the most recent run). Transitions
outside the band are treated as count-method breaks (e.g. station 58's
4,348 -> 16,313 one-year jump) and excluded; a station without two clean
points gets empty CAGR columns (none in the current data).

Output: `data/processed/growth_factors.csv`, 29 rows: `station_no`,
`location`, `road_link`, `year_start`, `year_end`, `aadt_pcu_start`,
`aadt_pcu_end`, `cagr`, `years_used`, `years_flagged`.

Run: `uv run python -m pipeline.growth`

Ceiling (module ponytail note): the 0.5-2.0 band is tuned by eye on these
29 stations; upgrade path is changepoint detection if new stations
misclassify.

## cordon.py

Inputs: `data/processed/od_2011.parquet`, `data/processed/growth_factors.csv`,
`sim/net/corridor-filtered.net.xml`, `sim/net/junction_map.csv`,
`data/raw/corridor.osm`.

Builds the baseline corridor demand (spec §4-§5) in four steps:

1. **Growth (A3 decision):** the 2011 vehicle OD is scaled by a single
   corridor-wide factor 1.9345 = aadt_pcu 75,453/39,004 from DoR SSRN
   station 64 (Manohara Bridge, road link H0303) over its clean
   2011/12-2024/25 run — the only valley station on the corridor's own road
   (Arniko Hwy at the Jadibuti end); all others sit on Ring Road or radials
   off the axis. Adjacent Ring Road stations bracket it for M3 sensitivity:
   65 Sinamangal 1.54x, 60 RR-Manohara 1.12x.
2. **Zone placement:** the eight corridor zones (spec §1) get hand-placed
   centroids on the OSM extract; the 42 external zones collapse to one gate
   per municipality group (code hundreds digit) on that group's approach
   artery, oriented so origins head into and destinations out of the
   corridor (ponytail notes in module: per-zone placement waits on the
   georeferenced zone map, A2 resolution). lon/lat -> net XY uses an affine
   fit on OSM-node/net-node pairs (max residual 1.3 m; asserted < 5 m),
   avoiding a pyproj dependency.
3. **Cordon sub-OD (spec §2, pragmatic):** one probe trip per distinct
   origin/destination edge combo is routed with duarouter; a zone pair is
   corridor-relevant iff its probe path crosses one of the 87 counted
   cordon edges in `junction_map.csv`. Kept: 5,336/10,000 OD cells,
   445,601 veh/day grown. Same-gate external pairs and intra-zonal trips
   drop out automatically (no cordon crossing).
4. **Time slicing (A1 decision):** hourly shares of daily trips
   06:00-12:00 = 3/6/9/20/9/6%. Sourced anchors [vol02 p.6-7, p.6-14]:
   09:00-10:00 carries 20% of daily trips, each adjacent hour under half
   the peak (9% < 10%); the 6/3% taper is the assumed part. Departures
   spread evenly inside 15-min bins; per-cell cumulative-floor rounding
   conserves totals to <1 trip.

Vehicle types are PCU-consistent (spec §3): length+minGap = PCU x car space
(4.3+2.5 m), i.e. motorcycle 1.84+0.2 (0.3 PCU), bus/truck 24.7+2.5
(4.0 PCU, A4); other parameters are SUMO per-vClass defaults (module
ponytail note: bus/truck length is queue-space bookkeeping, not geometry).

Outputs:

- `data/processed/corridor_od.parquet` — 5,336 rows: `origin_zone`,
  `dest_zone`, `mode`, `trips_2011` (seed), `trips` (grown daily float).
- `sim/demand/baseline.trips.xml` — 234,760 trips 06:00-12:00 (08:00-11:00:
  motorcycle 105,589, car 35,633, bus 17,191, truck 10,629), provenance in
  the file header.
- `sim/demand/baseline.rou.xml` (+ `.rou.alt.xml` for a later duaIterate) —
  duarouter 1.27.1 output, all 234,760 trips routed, zero failures; the
  exact call is recorded in the file's own configuration header.

Run: `uv run python -m pipeline.cordon` (~5 min, most of it duarouter).

Ceilings: group gates funnel each external group through one arterial edge
(insertion backlog risk at the Arniko east gate — split gates at M3 if
insertion delay shows up); the bbox clips Ring Road north at Chabahil, so
east<->north through trips all route via the corridor; single growth factor
holds the 2011 mode split (62% motorcycle vs the ~70% 2019 anchor, spec §6
sanity check at M3 calibration).
