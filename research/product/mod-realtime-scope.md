# MOD — scope for the live version

Draft 2026-09-11. Extends [`mod-product-spec.md`](mod-product-spec.md), which
describes a closure-driven product. This document scopes the thing actually
wanted: **continuous rerouting from live conditions**, where a traveller going
A → Z is re-advised mid-trip as traffic, incidents, flooding or weather change.

The difference matters. The original spec needs no live data feed. This one is
built on top of one, and that feed does not exist yet for Kathmandu.

## 0. The plan, as stated

Recorded as the author's intent, 2026-09-11, before it is cut into phases. The
phases below are how to reach it; this section is the thing being reached for.

> A traveller is going from A to Z. Along the way there may be twenty-six
> points where the advice could change. The road network is static, but
> everything else is live: where each user is, what the traffic is on each
> road, whether there is an emergency, a flood, heavy rain, a closure. The
> system takes all of that and re-advises the traveller in real time, sending
> them a different way when a different way is better.

Two commitments inside that, and they are the parts that make it MOD rather
than another router:

- **It advises, it does not command.** The product recommends a reroute. The
  traveller decides. Compliance is a thing to measure, not to assume.
- **Different travellers get different advice.** When one event displaces many
  people, sending them all down the same next-best road just moves the jam.
  Spreading them is the whole point, and it is what the study measured.

Everything in this document is subordinate to that goal. Where a phase looks
like a smaller product, it is a step toward this one and is only worth building
if it also stands up on its own.

## 1. What the product becomes

A traveller starts a trip. The app knows where they are, what they drive, and
where they are going. While they move, it watches conditions on the roads ahead
and re-advises when a materially better path appears — and, when many travellers
are displaced by the same event, sends them down *different* alternatives rather
than all down the same one.

Three things change from the closure-only version:

- routing weights come from **measured current speeds**, not free-flow speeds
- the trip is a **session**, not a single question
- the system holds **state about where everyone is**, which is what makes
  spreading possible at all

## 2. What already exists

Verified in this repo, not aspirational.

| Piece | State | Where |
| --- | --- | --- |
| Road graph, 11,693 nodes / 28,719 edges, with lane counts derived from carriageway width | **done**, exported at 0.6 MB gzipped | `pipeline/export_graph.py` → `results/corridor-graph.json.gz` |
| Vehicle-class permissions, including 488 motorcycle-only links | **done**, in the export, test-guarded | `tests/test_export_graph.py` |
| Shortest path with a hard exclusion set, per vehicle class | **done** | `experiments/transforms.py` `_shortest` |
| *k* genuinely distinct alternatives, each avoiding the previous one's mid-section | **done** | `experiments/transforms.py` `_alternatives` |
| Spreading travellers across those alternatives | **done** | `experiments/transforms.py` `spread_reroute` |
| Closure model, with the rerouter placed upstream of the closed link | **done** | `pipeline/disruption.py` |
| Evidence that spreading helps the network, not only the driver | **done**: −42.6 ± 2.5% network delay at a 20% diverted share, throughput up | paper §5, `results/sweep/summary.csv` |

Routing cost on the real graph: **4.2 ms per route in pure Python with no
heuristic**. Routing is not the hard part and never will be.

## 3. What does not exist

This is the whole project.

### 3.1 Live speed per road

There is no public real-time traffic feed for Kathmandu. The research found
none (`mod-product-spec.md` §7). Options, in order of how real they are:

- **Probe data from your own users.** Phones report position every 10–30 s
  while travelling; map-match each trace to an edge; aggregate to a rolling
  median speed per edge per time window. This is how Waze and Google began.
  Chicken-and-egg: needs users to produce the data that makes it useful.
- **Operator reports.** Traffic police know what is blocked. Low volume, high
  value, no density requirement. Works from day one.
- **User reports.** "Jam here", "flooded". Cheap, noisy, immediate.
- **Third-party layer.** Google/TomTom traffic APIs exist but are paid, and
  their licences generally forbid using them to build a competing routing
  product. Check before designing around one.

**The honest position:** until probe density exists, "live traffic" means
*reported* conditions, not *measured* ones. That is still a product. It is not
the same product.

### 3.2 Map matching

A GPS point is a lat/lon with error. Turning a stream of them into "this
vehicle is on edge X travelling at Y m/s" is its own problem — worse in dense
urban graphs where parallel roads sit 15 m apart, and worse again on
motorcycles that weave.

Standard approach is a hidden Markov model over candidate edges. There are
libraries. It is a week of work to get something usable and a long time to get
it good.

### 3.3 Trip sessions and continuous re-advice

A session holds: origin, destination, vehicle class, current position, the
route currently advised, and which alternative the traveller was assigned.

**Do not re-route every second.** Systems that do this flip-flop and users stop
trusting them. Re-advise only when:

- the remaining route's estimated time worsens by a meaningful margin, and
- an alternative is better by more than that margin, and
- the traveller has not been re-advised in the last few minutes

Those thresholds are product decisions, and getting them wrong is the most
common way this class of app fails.

### 3.4 Assignment across travellers

The novelty, and the thing the paper actually measured. When one event
displaces many travellers, the system must hand out *different* alternatives in
proportion, rather than the same best one to everyone.

Needs a live count of who has been sent where, decaying over time. This is a
counter with a time window, not a simulation.

Only matters above a density threshold: with ten users on the corridor,
spreading changes nothing. Below that, the app is an ordinary router and should
be honest about it.

### 3.5 The client

Mobile PWA with background geolocation, offline tolerance and battery
discipline. `UI-PROMPT.md` covers the screens. Background location on iOS in a
PWA is restricted — verify what is possible before designing around it.

### 3.6 Operator console

Post a closure, see where diverted traffic went. Partly specced already
(`mod-product-spec.md` §5.3), including the requirement to show current flow on
a link before offering to close it.

## 4. Build order

Each phase is useful on its own and generates what the next one needs.

### Phase 1 — Router as a service

Graph loader, vehicle-class Dijkstra, *k* alternatives, closure exclusion, one
HTTP endpoint. Free-flow weights. No users, no sessions, no live data.

Proves the engine works outside the simulator and gives the app something to
call. Small: the algorithm is about forty lines and the graph is already
exported.

### Phase 2 — Closures and the operator console

Operator posts a disruption; affected routes exclude it. Traveller app shows
origin/destination/vehicle class, a route, alternatives and a disruption
banner. Plus the after-trip question: *did you already know this route?*

**This is a complete, shippable product with zero live-traffic data**, and it is
what the original spec describes. Everything after this point depends on having
users.

### Phase 3 — Probe collection

The app reports position while travelling. Map-match, store traces. Do not
route on this yet — collect, and measure how much you have. The output of this
phase is an answer to: *how many active users does the corridor need before
edge speeds are usable?*

### Phase 4 — Live weights

Once density supports it, replace free-flow weights with measured speeds on the
edges that have data, falling back to free-flow where they do not. Now the
router is live.

### Phase 5 — Sessions and continuous re-advice

Trips become sessions. Re-advise on the thresholds from §3.3.

### Phase 6 — Spreading across travellers

Assignment counters, proportional alternatives. This is the research finding
made operational, and it is last because it needs everything above it.

## 5. What to be careful about

**Do not promise a percentage.** −42.6% is a modelled figure at a modelled
loading in a model that *forced* compliance. A real app advises. The product may
say spreading helps the network and cite the study; it may not promise a number
to a user or an authority.

**Compliance is unmeasured.** Nobody has established what share of Kathmandu
drivers will accept a longer route. The whole benefit is conditional on it.

**Induced demand is a real externality.** If guidance works, it sends traffic
through residential internal roads. Flagged in the original spec, still not
measured, and it is the kind of thing residents notice before developers do.

**Privacy.** Continuous location from identifiable users is sensitive data,
more so when the operator console is run by traffic police. Decide early what
is stored, for how long, and what the operator can see. Aggregated edge speeds
do not require retaining individual traces.

**Battery and data.** Background GPS drains phones. Kathmandu users are
price-sensitive about mobile data. Both are product-killing if ignored.

## 6. The shape of the honest answer

The road network is done and is the smallest part. Routing is done and costs
4 ms. What stands between here and the product described at the top of this
document is a **data layer that does not exist yet**, and the only credible way
to build it is from the app's own users — which means phases 1 and 2 have to be
worth using without any live data at all.

That is the plan: ship something useful with no traffic feed, use it to build
the feed, then become the live product.
