"""The header-only battle summary on replays built in code: no real replay, no real names."""

from __future__ import annotations

import zipfile

import pytest

import synth
from heat3d_ext_warthunder.replay_info import info

RESULTS = {
    "status": "fail",
    "timePlayed": 612.5,
    "author": "Tester A",
    "authorUserId": "101",
    "player": [
        {"name": "Tester A", "userId": "101", "team": 1, "clanTag": "[TST]", "score": 300},
        {"name": "Tester B", "userId": "202", "team": 2, "score": 900},
    ],
    "uiScriptsData": {"playersInfo": {
        "__int_101": {"name": "Tester A", "id": 101, "team": 1, "country": "country_test",
                      "crafts": {"0": "test_tank_a", "1": "test_plane_a"},
                      "crafts_info": {"array0": {"slot": 0, "type": "tank"}, "array1": {"slot": 1, "type": "fighter"}}},
        "__int_202": {"name": "Tester B", "id": 202, "team": 2, "crafts": {"0": "test_tank_b"},
                      "crafts_info": {"array0": {"slot": 0, "type": "tank"}}},
    }},
}


def _replay(results=RESULTS) -> bytes:
    packets = [synth.packet(1, 0, b""), synth.packet(0, 5000, b"")]
    return synth.replay(packets, results, compress="zlib", start=1793000000, version=101404)


def test_the_header_and_results(tmp_path):
    f = tmp_path / "a.wrpl"
    f.write_bytes(_replay())
    d = info(f)
    assert d["map"] == "99_testmap"
    assert d["mode"] == "RB"  # difficulty byte; the synthetic settings name no unit types
    assert d["date"] == "2026-10-26T07:33:20+00:00"
    assert d["duration_s"] == 612.5
    assert d["game_version"] == "101404"
    assert d["teams"] == [{"id": "1"}, {"id": "2"}]
    by_name = {p["name"]: p for p in d["players"]}
    assert by_name["Tester A"] == {"name": "Tester A", "team": "1", "clan": "[TST]",
                                   "vehicles": ["test_tank_a", "test_plane_a"], "country": "country_test",
                                   "userId": "101"}
    assert by_name["Tester B"]["team"] == "2" and by_name["Tester B"]["vehicles"] == ["test_tank_b"]
    # The author's team lost: the other team won.
    assert d["outcome"] == {"winner": "2", "result": "fail"}
    assert d["author"] == "Tester A"


def test_a_replay_without_results(tmp_path):
    f = tmp_path / "left.wrpl"
    f.write_bytes(_replay(results=None))
    d = info(f)
    assert d["map"] == "99_testmap" and d["date"]
    assert d["players"] == [] and d["teams"] == [] and d["outcome"] is None and d["duration_s"] is None


def test_a_zip_of_parts(tmp_path):
    z = tmp_path / "server.zip"
    with zipfile.ZipFile(z, "w") as out:
        out.writestr("0000.wrpl", _replay(results=None))
    assert info(z)["map"] == "99_testmap"


def test_not_a_replay(tmp_path):
    f = tmp_path / "junk.wrpl"
    f.write_bytes(b"not a replay" * 200)
    with pytest.raises(ValueError):
        info(f)
    empty = tmp_path / "empty.wrpl"
    empty.write_bytes(b"")
    with pytest.raises(ValueError):
        info(empty)
