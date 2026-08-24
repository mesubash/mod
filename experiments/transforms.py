"""M4 demand transforms (spec §8): pure, seeded functions on lists of SUMO
<trip> attribute dicts (the sim/demand/baseline.trips.xml shape). Inputs are
never mutated; callers write results via write_trips.

Sign convention: dt_minutes is the spec's Δt — negative shifts earlier
(Δt ∈ {-15, -30}; S1 uses -60).
"""

import heapq
import random
import xml.etree.ElementTree as ET

from pipeline.common import REPO

PEAK = (32400, 36000)      # 09:00-10:00, spec §4
ANALYSIS = (28800, 39600)  # 08:00-11:00, spec §4
MC_OCC = 1.1               # persons/motorcycle, spec §3
BUS_OCC = 15               # persons/bus, spec §3
NET_DEFAULT = REPO / "sim/net/corridor-calibrated.net.xml"
# Permitted connections differ by class, so an alternative must be searched with
# the vehicle's own vClass: a path a car may take can be illegal for a bus ("no
# connection between X and Y"), which SUMO rejects at load time.
VCLASS = {"motorcycle": "motorcycle", "car": "passenger",
          "bus": "bus", "truck": "truck"}


def _depart(t):
    return float(t["depart"])


def _in(t, window):
    return window[0] <= _depart(t) < window[1]


def _od(t):
    """Origin/destination of a trip, however the demand expresses it: <trip>
    elements carry from/to, while routeSampler's <vehicle> elements carry an
    embedded route whose first and last edges are the OD."""
    if "from" in t and "to" in t:
        return t["from"], t["to"]
    edges = t["route"].split()
    return edges[0], edges[-1]


def read_trips(path):
    """(vtypes, vehicles) as attribute dicts.

    Handles both demand forms: <trip> elements (origin/destination, routed
    later by duarouter) and <vehicle> elements carrying an embedded <route>,
    which is what routeSampler emits for the count-matched demand. A vehicle's
    route travels with it under the "route" key so transforms can move departs
    and change types without touching the path itself."""
    root = ET.parse(path).getroot()
    vtypes = [dict(v.attrib) for v in root.iter("vType")]
    trips = [dict(t.attrib) for t in root.iter("trip")]
    for veh in root.iter("vehicle"):
        entry = dict(veh.attrib)
        if (route := veh.find("route")) is not None:
            entry["route"] = route.get("edges")
        trips.append(entry)
    return vtypes, trips


def write_trips(path, vtypes, trips, comment):
    def tag(name, attrs):
        return f"<{name} " + " ".join(f'{k}="{v}"' for k, v in attrs.items()) + "/>"

    with open(path, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(f"<!-- {comment} -->\n<routes>\n")
        for v in vtypes:
            f.write("    " + tag("vType", v) + "\n")
        for t in sorted(trips, key=_depart):
            reroute = t.get("reroute")
            if "route" in t:
                attrs = {k: v for k, v in t.items()
                         if k not in ("route", "reroute")}
                f.write(f"    {tag('vehicle', attrs)[:-2]}>\n")
                if reroute is not None:
                    # per-vehicle device: guidance is only a treatment if the
                    # guided vehicle keeps the route it was given
                    f.write('        <param key="has.rerouting.device" '
                            f'value="{reroute}"/>\n')
                f.write(f'        <route edges="{t["route"]}"/>\n'
                        "    </vehicle>\n")
            else:
                f.write("    " + tag("trip", t) + "\n")
        f.write("</routes>\n")


def retime(trips, p_t, dt_minutes, *, seed, window=PEAK):
    """Shift a seeded random p_t share of trips departing in window by
    dt_minutes. Exactly round(p_t * n_window) trips move; only depart changes."""
    assert dt_minutes < 0, "spec §8: Δt is negative (shift earlier)"
    idx = [i for i, t in enumerate(trips) if _in(t, window)]
    moved = set(random.Random(seed).sample(idx, round(p_t * len(idx))))
    return [{**t, "depart": f"{_depart(t) + dt_minutes * 60:.2f}"}
            if i in moved else t
            for i, t in enumerate(trips)]


def mode_shift(trips, m, b_cap=None, *, seed, window=ANALYSIS):
    """Convert a seeded random m share of window motorcycle trips to bus
    passengers via the occupancy bridge (1.1 -> 15, spec §3). A bus trip is
    added per 15 accumulated passengers on the same OD, departing with the
    trip whose passengers complete the busload; b_cap (added bus passengers
    per hour, A5; None = uncapped, TOML has no null so configs omit it) clips
    conversions in depart order, excess stays motorcycle.
    Returns (new_trips, summary)."""
    cand = [i for i, t in enumerate(trips)
            if t["type"] == "motorcycle" and _in(t, window)]
    selected = random.Random(seed).sample(cand, round(m * len(cand)))

    hour_pax, converted = {}, set()
    for i in sorted(selected, key=lambda i: _depart(trips[i])):
        h = int(_depart(trips[i]) // 3600)
        pax = hour_pax.get(h, 0.0) + MC_OCC
        if b_cap is None or pax <= b_cap + 1e-9:
            hour_pax[h] = pax
            converted.add(i)

    out = [t for i, t in enumerate(trips) if i not in converted]
    od_pax, od_buses, buses = {}, {}, []
    for i in sorted(converted, key=lambda i: _depart(trips[i])):
        t = trips[i]
        od = _od(t)
        od_pax[od] = od_pax.get(od, 0.0) + MC_OCC
        if od_pax[od] >= BUS_OCC * (od_buses.get(od, 0) + 1) - 1e-9:
            od_buses[od] = od_buses.get(od, 0) + 1
            buses.append({"id": f"busadd.{len(buses)}", "type": "bus",
                          "depart": t["depart"], "departLane": "best",
                          **({"route": t["route"]} if "route" in t
                             else {"from": od[0], "to": od[1]})})
    out += buses

    summary = {
        "candidates": len(cand), "selected": len(selected),
        "converted": len(converted), "clipped": len(selected) - len(converted),
        "passengers_moved": round(len(converted) * MC_OCC, 2),
        "buses_added": len(buses),
        "residual_passengers": round(len(converted) * MC_OCC
                                     - len(buses) * BUS_OCC, 2),
    }
    return out, summary


def s1_school_shift(trips, school_share=None, *, seed):
    """S1 (spec §8): school_share of peak-hour trips, all modes, moves -60 min.
    school_share must be sized via the A1 profile — 48% [vol02 p.6-7] is the
    peak concentration of to-school trips, NOT the school share of peak
    demand; there is no default, so an unsized config fails here."""
    if school_share is None:
        raise ValueError(
            "s1 school_share unset: size via the A1 profile first (spec §8 S1)")
    return retime(trips, school_share, -60, seed=seed)


def reroute(trips, p_r, *, seed, net_path=None, window=PEAK):
    """S0: divert a seeded random p_r share of peak trips onto their best
    alternative path, leaving departure times unchanged.

    This is the project's original hypothesis — spread traffic across roads
    rather than across time. Each diverted vehicle keeps its origin and
    destination but is rerouted so that its first counted corridor edge is
    avoided, forcing it onto a parallel path if one exists. Vehicles with no
    alternative stay on their route and are counted in the summary, because
    "no alternative exists" is itself the result the scenario tests.

    Operates on route-carrying demand (<vehicle> with embedded edges); trips
    without a route are returned unchanged.
    """
    net = _net(net_path)
    idx = [i for i, t in enumerate(trips) if _in(t, window) and t.get("route")]
    chosen = set(random.Random(seed).sample(idx, round(p_r * len(idx))))

    out, diverted, no_alternative = [], 0, 0
    for i, trip in enumerate(trips):
        if i not in chosen:
            out.append(trip)
            continue
        edges = trip["route"].split()
        alt = _alternative(net, edges, VCLASS.get(trip.get("type"), "passenger"))
        if alt:
            out.append({**trip, "route": " ".join(alt)})
            diverted += 1
        else:
            out.append(trip)
            no_alternative += 1
    return out, {"selected": len(chosen), "diverted": diverted,
                 "no_alternative": no_alternative}


_PATH_CACHE = {}
_NET_CACHE = {}


def _net(net_path=None):
    """Read the network once per process: reroute is called per grid point and
    the calibrated net is ~86 MB, so re-reading it dominated scenario runtime."""
    import sumolib

    key = str(net_path or NET_DEFAULT)
    if key not in _NET_CACHE:
        _NET_CACHE[key] = sumolib.net.readNet(key)
    return _NET_CACHE[key]


def _shortest(net, start, end, vclass, banned=frozenset()):
    """A* by edge length with a hard exclusion set, memoised.

    Written out rather than calling sumolib's getShortestPath because that
    method caches routing internally: mutating an edge's speed or length to
    "block" it has no effect on the returned path. The earlier implementation
    did exactly that, so every alternative search returned the original path,
    which still contained the blocked edge, and the transform reported "no
    alternative" for essentially every trip in the network.

    Straight-line distance to the destination is an admissible heuristic on a
    road graph and cuts the explored frontier sharply; the cache matters
    because routeSampler draws many trips from the same distinct routes, so
    the same (origin, destination, exclusion) query repeats thousands of times.
    """
    key = (start.getID(), end.getID(), frozenset(banned), vclass)
    if key in _PATH_CACHE:
        return _PATH_CACHE[key]
    if start is end:
        return [start.getID()]

    target = end.getShape()[-1]

    def heuristic(edge):
        x, y = edge.getShape()[-1]
        return ((x - target[0]) ** 2 + (y - target[1]) ** 2) ** 0.5

    queue = [(heuristic(start), 0.0, start.getID(), [start])]
    best = {}
    result = None
    while queue:
        _, cost, _, path = heapq.heappop(queue)
        edge = path[-1]
        if edge is end:
            result = [e.getID() for e in path]
            break
        if cost > best.get(edge.getID(), float("inf")):
            continue
        for nxt in edge.getOutgoing():
            eid = nxt.getID()
            if eid in banned or not nxt.allows(vclass):
                continue
            step = cost + nxt.getLength()
            if step < best.get(eid, float("inf")):
                best[eid] = step
                heapq.heappush(queue, (step + heuristic(nxt), step, eid, path + [nxt]))
    _PATH_CACHE[key] = result
    return result


def _alternative(net, edges, vclass="passenger"):
    """Shortest path avoiding the route's mid-section edge, or None when the
    origin and destination are genuinely cut apart without it."""
    if len(edges) < 3:
        return None
    blocked = edges[len(edges) // 2]
    try:
        start, end = net.getEdge(edges[0]), net.getEdge(edges[-1])
    except KeyError:
        return None
    return _shortest(net, start, end, vclass, banned={blocked})


def _alternatives(net, edges, closed, k, vclass="passenger"):
    """Up to k distinct paths avoiding the closed edges.

    Each successive alternative also avoids the previous one's mid-section, so
    the paths are different corridors rather than variations of one."""
    try:
        start, end = net.getEdge(edges[0]), net.getEdge(edges[-1])
    except KeyError:
        return []
    banned, found = set(closed), []
    for _ in range(k):
        path = _shortest(net, start, end, vclass, banned=banned)
        if path is None or path in found:
            break
        found.append(path)
        banned.add(path[len(path) // 2])
    return found


def spread_reroute(trips, closed_edges, p_r, k_alternatives=3, *, seed,
                   kappa=1.0, net_path=None, window=None):
    """S4: coordinated rerouting under disruption.

    Trips whose route uses a closed edge are the affected set. A seeded p_r
    share receives guidance; the rest keep their route, which is what happens
    when no one is told anything. Guided trips are spread round-robin across up
    to k distinct alternatives rather than all sent to the single best one,
    because sending every diverted vehicle down the same parallel road recreates
    the jam elsewhere (Braess, paper [42]).

    kappa is the share of un-guided affected drivers who know the network well
    enough to divert usefully on their own. They get a rerouting device, which
    reads live travel times — a local who knows both the shortcuts and which of
    them is moving. The remaining 1 - kappa meet the closure with no device and
    take whatever the rerouter hands them on arrival. kappa = 1 makes every
    un-guided driver an omniscient rerouter, which is the control the first S4
    grid used and the reason guidance appeared to add nothing; no Kathmandu
    measurement of route knowledge exists, so kappa is swept, not assumed.

    Returns (trips, summary); the summary reports how many affected trips had no
    alternative at all.
    """
    net = _net(net_path)
    closed = set(closed_edges)
    affected = [i for i, t in enumerate(trips)
                if t.get("route") and closed.intersection(t["route"].split())
                and (window is None or _in(t, window))]
    rng = random.Random(seed)
    guided = set(rng.sample(affected, round(p_r * len(affected))))
    unguided = [i for i in affected if i not in guided]
    knowing = set(rng.sample(unguided, round(kappa * len(unguided))))

    # A global rerouting device re-plans every vehicle periodically, which
    # overwrites the routes guidance just assigned and makes k=1 and k=3
    # identical. Devices are therefore assigned per vehicle: affected but
    # un-guided vehicles reroute reactively when they meet the closure, which
    # is today's behaviour; guided vehicles keep the route they were given.
    out, spread, no_alternative = [], 0, 0
    for i, trip in enumerate(trips):
        if i not in guided:
            if i in knowing:
                trip = {**trip, "reroute": "1"}
            out.append(trip)
            continue
        options = _alternatives(net, trip["route"].split(), closed,
                                k_alternatives,
                                VCLASS.get(trip.get("type"), "passenger"))
        if not options:
            out.append(trip)
            no_alternative += 1
            continue
        out.append({**trip, "route": " ".join(options[spread % len(options)]),
                    "reroute": "0"})
        spread += 1
    return out, {"affected": len(affected), "guided": len(guided),
                 "knowing": len(knowing), "rerouted": spread,
                 "no_alternative": no_alternative}
