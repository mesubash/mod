"""Resolving the A10 signal patch onto renamed junctions (pipeline/tls_patch.py)."""

from pipeline.tls_patch import members, resolve


class FakeNode:
    def __init__(self, nid):
        self._id = nid

    def getID(self):
        return self._id


class FakeNet:
    def __init__(self, ids):
        self._nodes = [FakeNode(i) for i in ids]

    def getNodes(self):
        return self._nodes


def test_members_reads_ids_out_of_a_cluster_name():
    assert members("31152551") == {"31152551"}
    assert members("cluster_1968450265_31152551_6540538696") == {
        "1968450265", "31152551", "6540538696"}
    # netconvert truncates long names; membership is then a subset
    assert members("cluster_13459728246_13459728254_#1more") == {
        "13459728246", "13459728254"}


def test_two_patched_nodes_merged_into_one_cluster_still_resolve():
    # Deriving lanes from width joined the two Shahid Gate nodes, netconvert
    # stopped with "Missing position (at node ID='6540538696')", and the
    # rebuild died six hours in.
    net = FakeNet(["cluster_1968450265_31152551_6540538696", "999"])
    got = dict(resolve(["6540538696", "31152551"], net))
    assert got["6540538696"] == ["cluster_1968450265_31152551_6540538696"]
    assert got["31152551"] == ["cluster_1968450265_31152551_6540538696"]


def test_a_cluster_that_split_resolves_to_every_piece():
    net = FakeNet(["cluster_1_2", "3"])
    assert dict(resolve(["cluster_1_2_3"], net))["cluster_1_2_3"] == ["3", "cluster_1_2"]


def test_an_unplaceable_junction_reports_empty_rather_than_guessing():
    net = FakeNet(["cluster_7_8"])
    assert dict(resolve(["12345"], net))["12345"] == []
