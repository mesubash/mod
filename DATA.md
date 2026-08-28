# Data provenance and terms

The MIT licence in `LICENSE` covers the code in this repository. It does not
cover the datasets below, which come from third parties and carry their own
terms. The extraction scripts are mine; the underlying figures are not.

## data/raw/corridor.osm

OpenStreetMap extract of the study corridor.

© OpenStreetMap contributors, available under the
[Open Database Licence](https://opendatacommons.org/licenses/odbl/) (ODbL).
Reuse requires attribution, and any derived database must be released under
the same licence. <https://www.openstreetmap.org/copyright>

`data/processed/corridor-laned.osm`, produced by `pipeline/lane_width.py`, is a
derived database and carries the same ODbL terms.

## data/processed/od_2011.parquet

Zone-to-zone vehicle origin–destination matrices, digitised from:

Japan International Cooperation Agency (2012). *Data Collection Survey on
Traffic Improvement in Kathmandu Valley*, Volume 4.
<https://openjicareport.jica.go.jp/pdf/12082459_01.pdf>

The machine-readable extraction is mine; the survey figures are JICA's.

## data/processed/counts_2019.parquet

Classified traffic counts at nine intersections, digitised from:

Japan International Cooperation Agency (2019). *Data Collection Survey on
Urban Transport in Kathmandu Valley: Final Report*, Volume 2, Table 4.1 and
Figure 4.2.

## data/processed/hourly_profile.parquet

Hourly, per-direction, per-class counts from three Department of Roads
stations (64 Manohara Bridge, 65 Ring Road Sinamangal, 58 Satdobato South),
FY 2024/25, three survey days each. Retrieved 2026-08-16 from
<https://ssrn.dor.gov.np/> by `pipeline/dor_hourly.py`.

Government of Nepal, Department of Roads.

## data/processed/growth_factors.csv

Derived from Department of Roads SSRN station AADT records, FY 2011/12 to
2024/25, filtered by `pipeline/growth.py`.

## Standards referenced, not redistributed

Capacity and carriageway figures are cited from Nepal Urban Road Standard
2076 (Government of Nepal, Ministry of Urban Development). The standard
itself is not included here; it is available from the Ministry.

## If you reuse this

Cite the original surveys, not this repository, for the underlying figures.
Cite this repository for the extraction, network build or testbed.
