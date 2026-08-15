"""M4 demand transforms (spec §8): pure, seeded functions on lists of SUMO
<trip> attribute dicts (the sim/demand/baseline.trips.xml shape). Inputs are
never mutated; callers write results via write_trips.

Sign convention: dt_minutes is the spec's Δt — negative shifts earlier
(Δt ∈ {-15, -30}; S1 uses -60).
"""

import random
import xml.etree.ElementTree as ET

PEAK = (32400, 36000)      # 09:00-10:00, spec §4
ANALYSIS = (28800, 39600)  # 08:00-11:00, spec §4
MC_OCC = 1.1               # persons/motorcycle, spec §3
BUS_OCC = 15               # persons/bus, spec §3


def _depart(t):
    return float(t["depart"])


def _in(t, window):
    return window[0] <= _depart(t) < window[1]


def read_trips(path):
    """(vtypes, trips) as attribute dicts."""
    root = ET.parse(path).getroot()
    return ([dict(v.attrib) for v in root.iter("vType")],
            [dict(t.attrib) for t in root.iter("trip")])


def write_trips(path, vtypes, trips, comment):
    def tag(name, attrs):
        return f"<{name} " + " ".join(f'{k}="{v}"' for k, v in attrs.items()) + "/>"

    with open(path, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(f"<!-- {comment} -->\n<routes>\n")
        for v in vtypes:
            f.write("    " + tag("vType", v) + "\n")
        for t in sorted(trips, key=_depart):
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
        od = (t["from"], t["to"])
        od_pax[od] = od_pax.get(od, 0.0) + MC_OCC
        if od_pax[od] >= BUS_OCC * (od_buses.get(od, 0) + 1) - 1e-9:
            od_buses[od] = od_buses.get(od, 0) + 1
            buses.append({"id": f"busadd.{len(buses)}", "type": "bus",
                          "depart": t["depart"], "from": od[0], "to": od[1],
                          "departLane": "best"})
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
