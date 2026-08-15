# sim/net

## corridor.net.xml

Built 2026-08-15 by SUMO netconvert 1.27.1 from `data/raw/corridor.osm`
(OSM extract, bbox 27.655-27.715 / 85.275-85.375). Full option set is
recorded in the file's own header comment (proj.utm, geometry.remove,
tls.discard-simple, tls.guess-signals, ramps.guess,
remove-edges.by-vclass pedestrian,bicycle, junctions.join).
33,593 edges, 13,545 nodes, 36 traffic lights, 3 roundabouts.

## corridor-filtered.net.xml

Derived from corridor.net.xml:

    netconvert -s sim/net/corridor.net.xml --keep-edges.by-vclass passenger \
      --keep-edges.components 1 -o sim/net/corridor-filtered.net.xml

Drops service/track/footway edges (no passenger access) and disconnected
components: 27,969 edges, 11,355 nodes, traffic lights unchanged. All 87
edges in junction_map.csv are present. This is the net M3 uses; the full
net is kept as the source it was derived from.

## corridor-calibrated.net.xml

Derived from corridor-filtered.net.xml by patching junction control at the
police-metered study junctions (assumption A10 in specs/model-spec.md §9):

    netconvert -s sim/net/corridor-filtered.net.xml -n sim/net/tls-patch.nod.xml \
      -o sim/net/corridor-calibrated.net.xml

tls-patch.nod.xml converts these priority nodes to actuated traffic lights
(netconvert default actuated programs; nodes sharing a `tl` id form one
joint controller):

- Thapathali: cluster_13459728246_... (single 4-leg cluster node)
- Kalimati: 3 sub-nodes of the divided-carriageway T joined as `Kalimati`
- Shahid Gate: the gyratory's 4 merge nodes joined as `ShahidGate`
  (absorbs the pre-existing lone TLS 31152551; the 2 diverge nodes are
  uncontrolled — single inflow, nothing to meter)
- Maitighar: the 2 unsignalized island entry merges (10901289775,
  1950468417); the area's 2 existing TLS clusters are untouched
- Tinkune: the 3 triangle corners (= count sub-sites South/West/North),
  separate controllers since they are ~300 m apart
- New Baneshwor: the 4 corner TLS (pairwise 8-26 m) joined as
  `NewBaneshwor`

Result: 40 TLS (was 36: 5 absorbed into joints, 9 new actuated programs,
31 pre-existing static programs unchanged). Edge/node counts unchanged
(27,969 / 11,355); all 87 junction_map.csv edges present. Koteshwor and
Jadhibuti are left alone (grade-separated in current OSM, see caveats
below); Tripureshwor's cluster was already a TLS.

Downstream: any sumocfg for calibration/stress/scenario runs must set
net-file to corridor-calibrated.net.xml (baseline.sumocfg still points at
corridor-filtered.net.xml and documents the gridlocked baseline as run).

## junction_map.csv

Maps every 2019 count leg-direction to net edges. Columns: intersection,
leg, edge_id, direction. intersection and leg match
`data/processed/counts_2019.parquet` (77 leg-direction records, all
mapped). direction: in = edge carries traffic toward the intersection,
out = away, as in Table 4.1 of the 2019 report (pp. A4-18/19).

Leg numbering comes from the report's own intersection diagrams,
Figure 4.2 pp. A4-14/15
(`research/library/data-jica-2019-urban-transport-survey-vol02.pdf`,
PDF pages 46-47), read visually 2026-08-15; 38 observed-PCU values read
off the diagrams were checked against the parquet with zero mismatches,
so the leg assignment is the report's, not a convention chosen here.
Diagram sub-sites "Tinkune 1/2/3" are parquet "Tinkune South/West/North"
respectively (identified by the same value match).

Edge selection: for each intersection, the edges crossing a cordon
circle of 70-170 m around the junction center, assigned to legs by
bearing and OSM road name. A leg-direction with several rows is a
divided or parallel-carriageway approach; its modeled volume is the sum
over its rows. Each edge cuts the cordon once, so flows are neither
double-counted nor bypassed.

Caveats for calibration:

- Tinkune is a one-way triangle; each side connects two count sub-sites
  and appears at both (e.g. Tinkune South leg 4 = Tinkune West leg 2),
  exactly as the 2019 survey counted it.
- Shahid Gate is a one-way gyratory in the net. Its internal westbound
  link 196269539 is deliberately unmapped; Kantipath southbound flow
  reaches leg 3 through it. Leg 1 is out-only and leg 2 in-only in both
  the report and the net.
- Maitighar leg 5 (Bhadrakali) is one-way out in both. Maitighar is
  modeled as one-way links around the island with priority junctions,
  not as a SUMO `<roundabout>` (the net's 3 roundabout elements are
  elsewhere).
- The OSM geometry is current, not 2019: Koteshwor and Jadhibuti were
  grade-separated after the Feb 2019 counts. Compare modeled volumes on
  the mapped cordon edges, not turn-level movements at those two.
