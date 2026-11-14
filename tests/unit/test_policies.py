"""Learned-policy helpers used to draw paths on the Environments page."""

import json

import numpy as np

from sla.evaluation.policies import greedy, snapshot, walk


def test_greedy_picks_best_action_and_value():
    actions, values = greedy(np.array([[0.0, 2.0], [5.0, 1.0]]))
    assert actions == [1, 0] and values == [2.0, 5.0]


def test_walk_cliffwalking_shortest_path_along_the_edge():
    actions = [1] * 48           # always right ...
    actions[36] = 0              # ... except at START: go up first
    actions[35] = 2              # and step down into GOAL at the end
    path = walk("CliffWalking-v1", actions)
    assert path[0] == 36 and path[-1] == 47 and len(path) - 1 == 13


def test_walk_stops_in_a_hole_on_frozenlake():
    path = walk("FrozenLake-v1", [1] * 16)   # always down: 0 -> 4 -> 8 -> 12 (hole)
    assert path == [0, 4, 8, 12]


def test_snapshot_reads_a_file_and_tolerates_a_missing_one(tmp_path):
    f = tmp_path / "p.json"
    f.write_text(json.dumps([{"env": "CliffWalking-v1", "algorithm": "sarsa", "actions": [0], "values": [0.0]}]))
    assert snapshot(f)[0]["algorithm"] == "sarsa"
    assert snapshot(tmp_path / "missing.json") == []
