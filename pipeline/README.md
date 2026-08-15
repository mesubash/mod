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
