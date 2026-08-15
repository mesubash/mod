from pipeline.baseline_eval import PCU, leg_volumes


def test_leg_volumes_sums_multirow_legs_and_pcu():
    jmap = [
        {"intersection": "X", "leg": "3", "edge_id": "a", "direction": "in"},
        {"intersection": "X", "leg": "3", "edge_id": "b", "direction": "in"},
        {"intersection": "X", "leg": "3", "edge_id": "c", "direction": "out"},
    ]
    counts = {
        ("a", 25200.0): {"motorcycle": 10, "bus": 2},   # 10*0.3 + 2*4 = 11
        ("b", 28800.0): {"car": 5},                     # 5
        ("b", 21600.0): {"car": 99},                    # outside hours, ignored
        ("c", 25200.0): {"truck": 1},                   # 4
    }
    vols = leg_volumes(jmap, counts, [25200, 28800])
    assert vols[("X", 3, "in")] == 11 + 5
    assert vols[("X", 3, "out")] == 4
    assert ("X", 3, "in") in vols and len(vols) == 2
    assert set(PCU) == {"motorcycle", "car", "bus", "truck"}
