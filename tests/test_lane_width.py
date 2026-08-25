"""Lane counts derived from carriageway width (pipeline/lane_width.py)."""

from pipeline.lane_width import lanes_from_width, parse_width, patch


def test_parse_width_handles_the_units_in_the_extract():
    assert parse_width("6") == 6.0
    assert parse_width("6.0") == 6.0
    assert parse_width("1.75 m") == 1.75
    assert parse_width(None) is None
    assert parse_width("wide") is None


def test_a_six_metre_one_way_arterial_gets_two_lanes():
    # Ram Shah Path: highway=primary, lanes=1, width=6, oneway=yes. Built as
    # one 3.2 m lane it was asked for 4,563 veh/h and gridlocked the network.
    assert lanes_from_width(
        {"highway": "primary", "lanes": "1", "width": "6", "oneway": "yes"}) == 2


def test_a_two_way_width_is_split_between_the_directions():
    # netconvert builds an edge per direction, so a 7 m two-way road gives each
    # direction 3.5 m, which is one stream, not two.
    assert lanes_from_width({"highway": "trunk", "width": "7"}) == 1
    assert lanes_from_width({"highway": "trunk", "width": "7", "oneway": "yes"}) == 2


def test_implausible_widths_fall_back_to_the_class_default():
    # The extract tags one way 608 m and several under 2 m (a cycle lane
    # recorded as the carriageway).
    assert lanes_from_width({"highway": "primary", "width": "608"}) == \
        lanes_from_width({"highway": "primary"})
    assert lanes_from_width({"highway": "primary", "width": "1.75 m"}) == \
        lanes_from_width({"highway": "primary"})


def test_a_surveyed_lane_count_is_never_reduced(tmp_path):
    # The rule recovers capacity the marked count omits; it must not overrule a
    # survey that recorded more lanes than the width implies. The guard is in
    # patch(), so exercise the file it writes, not the width rule alone.
    src = tmp_path / "in.osm"
    src.write_text(
        '<osm>\n'
        '  <way id="1">\n'
        '  <tag k="highway" v="primary"/>\n'
        '  <tag k="lanes" v="4"/>\n'
        '  <tag k="width" v="6"/>\n'
        '  <tag k="oneway" v="yes"/>\n'
        '  </way>\n'
        '  <way id="2">\n'
        '  <tag k="highway" v="primary"/>\n'
        '  <tag k="lanes" v="1"/>\n'
        '  <tag k="width" v="6"/>\n'
        '  <tag k="oneway" v="yes"/>\n'
        '  </way>\n'
        '</osm>\n', encoding="utf8")
    out = tmp_path / "out.osm"
    stats = patch(src, out)
    text = out.read_text(encoding="utf8")

    assert '<tag k="lanes" v="4"/>' in text, "a surveyed 4 lanes must survive"
    assert '<tag k="lanes" v="1"/>' not in text, "1 lane on 6 m must be raised"
    assert '<tag k="lanes" v="2"/>' in text
    assert stats == {"ways": 2, "raised": 1, "unchanged": 1, "added": 0}


def test_non_roads_are_left_alone():
    assert lanes_from_width({"highway": "footway", "width": "3"}) is None
    assert lanes_from_width({"width": "6"}) is None
