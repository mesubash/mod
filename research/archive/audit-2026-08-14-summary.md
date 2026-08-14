Quick version:

**What already exists (Kathmandu):**
- **Master plan (Aug 2026, JICA/govt)** — roads, tunnels, metro corridor, intersection signals. Physical stuff, decades-long rollout.
- **Route rationalization plan (2014)** — good design, still not implemented 12 years later. Institutional failure, not technical.
- **Journey planners** — Sajha Plus (live GPS tracking, official), LocaGo, Google Maps. All optimize *your* trip only, not the network.
- **Signal-level ITS** — a handful of smart signals in Lalitpur, most of Kathmandu still runs on manual police whistles.
- **Academic work** — static fleet-allocation study (R1), one graph-based route planner (R11). Both one-off, not live/adaptive.

**What's missing — this is your opening:** nothing in Kathmandu continuously watches network-wide demand and nudges people toward less-congested routes/modes in real time. Everything above is either physical (years to build) or individual (doesn't care about collective effect).

**What overseas is doing:** Google just published (July 2026) the first real-world proof that this works — rerouting a small % of Google Maps trips off congested segments in 10 US cities measurably cut delay/emissions citywide. Their own line: system-wide routing "is not yet present" commercially, even they hadn't validated it at scale until now. So this isn't a solved problem you're re-doing — it's barely solved anywhere.

**Our approach — what you can actually build:** adapt that same idea to Kathmandu's harder conditions — no Google-scale GPS data, semi-formal microbus/tempo network instead of clean car traffic. Concretely:
1. Pick one bounded, already-known-congested corridor (JICA's own east-west corridors are documented at 150-200k passengers/km — over capacity).
2. Build/estimate an OD demand dataset (OSM road graph + JICA 2012 survey data, since you won't have live telemetry).
3. Simulate in SUMO: baseline (everyone takes shortest path) vs. demand-aware routing (some trips nudged to alternatives).
4. Measure: does total network delay drop, and how much extra time does the "nudged" traveler pay?

That's a contained, measurable, no-institutional-buy-in-needed project — unlike route reform or fleet rebalancing, which need government/operator cooperation and are exactly where past Kathmandu efforts got stuck.