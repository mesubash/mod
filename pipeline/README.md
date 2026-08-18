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

## dor_hourly.py

Input: the DoR SSRN hourly detail pages,
`https://ssrn.dor.gov.np/traffic_controller/get_detail/<location>/<id>` (ids
from the `hourly_detail_url` column of the AADT scrape). Three FY 2024/25
stations: 64 Manohara Bridge (the corridor's own Arniko Highway crossing),
65 Ring Road (Sinamangal), 58 Satdobato South (Chapagaun).

Each page prints one row per survey day and clock hour, per vehicle class,
per direction; the parser keeps the both-direction total (last cell) of each
hourly row and yields 3 survey days per station.

Output: `data/processed/hourly_profile.parquet`, 216 rows
(3 stations x 3 days x 24 hours): `station` int, `location` str, `date` str,
`hour` int, `total_veh` float. `hourly_shares()` pools it into the
share-of-daily-traffic per hour that A1 uses (spec §4): AM peak 6.8% at
09:00, 08:00-11:00 = 19.0%, PM peak 7.4% at 17:00.

Run: `uv run python -m pipeline.dor_hourly`

Ceilings: both-direction totals hide tidal asymmetry (the per-direction
columns are on the same pages); the three stations are highway/Ring-Road
cross-sections, so the profile is not corridor-interior (research/07 §"Measured
hourly profile").

## cordon.py

Inputs: `data/processed/od_2011.parquet`, `data/processed/growth_factors.csv`,
`sim/net/corridor-filtered.net.xml`, `sim/net/junction_map.csv`,
`data/raw/corridor.osm`.

Builds the baseline corridor demand (spec §4-§5) in five steps:

1. **Growth (A3 decision):** the 2011 vehicle OD is scaled by a single
   corridor-wide factor 1.9345 = aadt_pcu 75,453/39,004 from DoR SSRN
   station 64 (Manohara Bridge, road link H0303) over its clean
   2011/12-2024/25 run — the only valley station on the corridor's own road
   (Arniko Hwy at the Jadibuti end); all others sit on Ring Road or radials
   off the axis. Adjacent Ring Road stations bracket it for M3 sensitivity:
   65 Sinamangal 1.54x, 60 RR-Manohara 1.12x.
2. **Zone placement:** the eight corridor zones (spec §1) get hand-placed
   centroids on the OSM extract; the 42 external zones share one gate area
   per municipality group (code hundreds digit) anchored on that group's
   approach artery (ponytail notes in module: per-zone placement waits on
   the georeferenced zone map, A2 resolution). lon/lat -> net XY uses an
   affine fit on OSM-node/net-node pairs (max residual 1.3 m; asserted
   < 5 m), avoiding a pyproj dependency.
3. **Spawn edges (`zones.taz.xml`):** demand injects over many edges per
   zone, not one. The first baseline run injected each zone through a
   single edge and starved: 21,288 of 234,760 vehicles inserted over the
   6h window, 213,472 still waiting outside the net (the top origin edge
   was assigned ~58,000 trips/6h, about 5x its lane capacity). Now each
   corridor zone spawns on its minor-road mesh (residential, living
   street, unclassified, tertiary, secondary; >= 25 m so a bus fits)
   within 600 m of the centroid — 137-537 edges per zone; primary/trunk
   are excluded so through demand does not materialize on the study axis.
   Each external group spawns on every arterial crossing the OSM extract
   bbox, assigned to the nearest gate point (inbound as source, outbound
   as sink; 47 crossing arterials in the net), plus arterials within
   600 m of the gate point (covers groups 1xx/2xx/3xx that lie partly
   inside the bbox) — 48-88 edges per group. Edge weight = lane count x
   priority. Trips carry `fromTaz`/`toTaz` plus concrete `from`/`to`
   edges drawn per-trip from those weights (seeded RNG; duarouter's own
   TAZ resolution picks the single cheapest edge pair, which would
   re-concentrate demand, so the draw happens at emission — od2trips
   semantics). A one-hour smoke run of the rebuilt routes (06:00-07:00,
   SUMO 1.27.1) inserted 10,856 of 11,939 loaded vehicles, 624 waiting,
   mean depart delay 1.22 s, 863 teleports — insertion keeps pace with
   departures where the starved build left 213,472 waiting over 6h.
4. **Cordon sub-OD (spec §2, pragmatic):** one probe trip per distinct
   origin/destination edge combo (single representative edges per zone,
   oriented toward/away from the corridor center) is routed with
   duarouter; a zone pair is corridor-relevant iff its probe path crosses
   one of the 87 counted cordon edges in `junction_map.csv`. Kept:
   5,336/10,000 OD cells, 445,601 veh/day grown. Same-gate external pairs
   and intra-zonal trips drop out automatically (no cordon crossing).
   This step is unchanged by the TAZ injection, so `corridor_od.parquet`
   is byte-identical to the single-edge build.
5. **Time slicing (A1):** the measured hourly shares of daily traffic from
   `dor_hourly.py`, 06:00-12:00 = 3.8/4.7/5.5/6.8/6.7/6.4%. This replaced a
   3/6/9/20/9/6% profile that read JICA's person-trip *generation* peak
   [vol02 p.6-7, p.6-14] as a vehicle-departure share; measured road
   traffic is about 3x flatter. Departures spread evenly inside 15-min
   bins; per-cell cumulative-floor rounding conserves totals to <1 trip.

Vehicle types are PCU-consistent (spec §3): length+minGap = PCU x car space
(4.3+2.5 m), i.e. motorcycle 1.84+0.2 (0.3 PCU), bus/truck 24.7+2.5
(4.0 PCU, A4); other parameters are SUMO per-vClass defaults (module
ponytail note: bus/truck length is queue-space bookkeeping, not geometry).
Motorcycles additionally carry sublane laterals (A11): latAlignment
compact, minGapLat 0.3 m (TU thesis Table 4-25 calibrated standing
lateral distance 0.2-0.41 m); inert unless sumo runs with
--lateral-resolution (sim/stress-options.txt).

Outputs:

- `data/processed/corridor_od.parquet` — 5,336 rows: `origin_zone`,
  `dest_zone`, `mode`, `trips_2011` (seed), `trips` (grown daily float).
- `sim/demand/zones.taz.xml` — 16 TAZ (8 corridor zones, 8 gate groups;
  g4/g8 share the Arniko gate), 3,284 weighted source and 3,285 sink
  entries.
- `sim/demand/baseline.trips.xml` — 234,760 trips 06:00-12:00 (08:00-11:00:
  motorcycle 105,589, car 35,633, bus 17,191, truck 10,629), provenance in
  the file header.
- `sim/demand/baseline.rou.xml` (+ `.rou.alt.xml` for a later duaIterate) —
  duarouter 1.27.1 output, 232,986/234,760 trips routed (1,774 dropped by
  `--ignore-errors`: sampled minor-road edge pairs with no connecting
  path); 3,107 distinct origin edges, max per-edge share 0.82%. The exact
  call is recorded in the file's own configuration header.

Run: `uv run python -m pipeline.cordon` (~5 min, most of it duarouter).

Ceilings: the bbox clips Ring Road north at Chabahil, so
east<->north through trips all route via the corridor; single growth factor
holds the 2011 mode split (62% motorcycle vs the ~70% 2019 anchor, spec §6
sanity check at M3 calibration).
