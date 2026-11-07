"""A whole battle built in code, converted: the table, its hints, who is who, the match document."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path

import pyarrow.parquet as pq
import pytest

import synth
from heat3d_ext_warthunder import cli, convert, names, wrpl

NAMES = names.Names({"f_15a_0": "◄F-15A Eagle", "f_15a_1": "F-15A"}, "test")

RESULTS = {
    "status": "success",
    "timePlayed": 30.0,
    "author": "Pilot One",
    "authorUserId": "111",
    "player": [
        {"name": "Pilot One", "userId": "111", "team": 1, "kills": 1, "deaths": 0, "score": 500},
        {"name": "Pilot Two", "userId": "222", "team": 2, "kills": 0, "deaths": 1, "score": 100},
    ],
    "uiScriptsData": {"playersInfo": {
        "__int_111": {"name": "Pilot One", "id": 111, "team": 1, "crafts": {"0": "f_15a", "1": "us_m1_abrams"},
                      "crafts_info": {"array0": {"slot": 0, "type": "fighter"},
                                      "array1": {"slot": 1, "type": "tank"}}},
        "__int_222": {"name": "Pilot Two", "id": 222, "team": 2, "crafts": {"0": "mig_29smt_9_19"},
                      "crafts_info": {"array0": {"slot": 0, "type": "fighter"}}},
    }},
}


def battle(compress: str = "zstd") -> bytes:
    """Two fighters fly north for 20 s at 4 Hz; One kills Two at 10 s, whose wreck falls; a tank sits still."""
    packets = [synth.packet(1, 0, b""),
               synth.packet(4, 100, synth.slots({0: (111, "Pilot One", 1), 1: (222, "Pilot Two", 2)}))]
    for i in range(81):
        ms = 1000 + i * 250
        t = i * 0.25
        two_y = 3000.0 if t <= 10 else 3000.0 - (t - 10) * 50  # falling after the kill
        packets.append(synth.packet(2, ms, synth.flight([
            (344, 0.0, 3000.0, 1000.0 + 200 * t, synth.attitude(0)),
            (345, 50.0, two_y, 1300.0 + 200 * t, synth.attitude(0)),
        ])))
        if i % 4 == 0:
            packets.append(synth.packet(4, None, synth.ground({177: (500.0, 120.0, 800.0 + t)}, number=i // 4)))
        if ms == 11000:
            packets.append(synth.packet(4, None, synth.damage(345, 344, 0, "f_15a")))
            packets.append(synth.packet(4, None, synth.kill(344, 0, "f_15a", 345, 1, "us_aim9l_sidewinder")))
    packets += [synth.packet(3, 15000, synth.chat("Pilot One", "gg")), synth.packet(0, 21000, b"")]
    return synth.replay(packets, RESULTS, compress=compress)


@pytest.fixture
def converted(tmp_path):
    f = tmp_path / "2026.11.07 12.00.00.wrpl"
    f.write_bytes(battle())
    table, doc = convert.convert([f], tmp_path / "out", names=NAMES)
    return pq.read_table(table), json.loads(doc.read_text(encoding="utf-8")), table


def test_writes_map_folder_and_hints(converted):
    t, doc, path = converted
    assert path.parent.name == "avg_test_land"
    hints = json.loads(t.schema.metadata[b"heat3d"])
    assert hints["axes"] == {"up": "y", "flipX": False, "flipY": False, "flipZ": True, "scale": 1}
    assert hints["columns"]["personId"] == "track" and hints["columns"]["lookMode"] == "vector"
    assert hints["columns"]["sessionId"] == "match"  # one match per file: two loaded replays never join tracks
    assert hints["conventions"]["roll"].startswith("degrees, right wing down positive")
    assert all(c in t.schema.names for c in hints["columns"]["extra"])
    assert "Vehicle" in t.schema.names


def test_tracks_and_identity(converted):
    t, doc, _ = converted
    rows = t.to_pylist()
    one = [r for r in rows if r["player"] == "Pilot One" and r["event"] == "position"]
    assert len(one) == 81 and {r["Vehicle"] for r in one} == {"f_15a"} and {r["team"] for r in one} == {"1"}
    assert one[0]["kind"] == "aircraft" and one[0]["life"] == "344#1"
    # The game's own name, without its font's country mark; a player is never AI.
    assert {(r["VehicleName"], r["VehicleShortName"], r["VehicleNameKey"]) for r in one} == {("F-15A Eagle", "F-15A", "f_15a_0")}
    assert {(r["ai"], r["isPlayer"]) for r in one} == {(False, True)}
    assert {r["match"] for r in rows} == {doc["match"]}
    # Flying north: the look vector points +z, the heading is about 0.
    assert one[0]["dirZ"] == pytest.approx(1, abs=0.01) and min(one[0]["heading"], 360 - one[0]["heading"]) < 0.5
    # Without an entity stream nothing names uid 345: a kill's "victim pid" is not the victim's slot.
    two = [r for r in rows if r["player"] == "uid 345"]
    assert {r["event"] for r in two} >= {"position", "death", "hit_critical"}
    assert {r["alive"] for r in two if r["event"] == "position" and r["time"] > 11} == {0.0}  # the falling wreck
    tank = [r for r in rows if r["kind"] == "ground"]
    assert len(tank) == 21 and tank[0]["player"] == "uid 177" and tank[0]["Vehicle"] == ""
    assert {r["ai"] for r in tank} == {True} and tank[0]["VehicleName"] == ""
    assert tank[0]["heading"] == pytest.approx(90.0) and tank[0]["speed"] == pytest.approx(1.0, abs=0.01)


def test_kill_rows_where_it_happened(converted):
    t, doc, _ = converted
    rows = t.to_pylist()
    kill = next(r for r in rows if r["event"] == "kill")
    death = next(r for r in rows if r["event"] == "death")
    assert kill["player"] == "Pilot One" and kill["other"] == "uid 345" and kill["weapon"] == "us_aim9l_sidewinder"
    assert kill["time"] == pytest.approx(11.0)
    assert (death["x"], death["z"]) == pytest.approx((50.0, 1300.0 + 200 * 10))
    assert (kill["x"], kill["z"]) == pytest.approx((0.0, 1000.0 + 200 * 10))


def test_match_document(converted):
    _, doc, _ = converted
    assert doc["format"] == "heat3d-wt-replay-match" and doc["map"] == "avg_test_land"
    assert doc["kills"][0]["killer"] == "Pilot One" and doc["kills"][0]["victim"] == "uid 345"
    assert doc["chat"] == [{"time": 15.0, "sender": "Pilot One", "text": "gg"}]
    c = doc["counts"]
    assert c["aircraftUids"] == 2 and c["groundUids"] == 1
    assert c["aircraftHz"] == pytest.approx(4.0) and c["groundHz"] == pytest.approx(1.0)
    assert c["unreadPackets"] == {}
    one = next(p for p in doc["players"] if p["name"] == "Pilot One")
    assert one["uids"] == [344] and one["vehicles"] == ["f_15a", "us_m1_abrams"]
    assert doc["selfCheck"]["lifeVehicleNotInPlayersCrafts"] == 0


def test_a_reused_uid_is_a_new_life(tmp_path):
    packets = [synth.packet(4, 0, synth.slots({0: (111, "Pilot One", 1)}))]
    for i in range(40):
        x = 0.0 if i < 20 else 20000.0  # spawned again far away
        packets.append(synth.packet(2, 1000 + i * 250, synth.flight([(344, x + i, 1000.0, 0.0, 0)])))
    f = tmp_path / "a.wrpl"
    f.write_bytes(synth.replay(packets, compress="zlib"))
    lives = convert.lives(convert.read([f]))
    assert [life.id for life in lives] == ["344#1", "344#2"]


def test_cli(tmp_path, capsys):
    (tmp_path / "in").mkdir()
    (tmp_path / "in" / "a.wrpl").write_bytes(battle("zlib"))
    (tmp_path / "in" / "bad.wrpl").write_bytes(b"not a replay" * 200)
    code = cli.main([str(tmp_path / "in"), "-o", str(tmp_path / "out")])
    out = capsys.readouterr().out
    assert code == 1  # the bad one
    assert "failed" in out and out.count("ok ") == 1
    assert list((tmp_path / "out" / "avg_test_land").glob("*.match.json"))
    assert cli.main([str(tmp_path / "empty-folder-that-is-missing"), "-o", str(tmp_path / "o2")]) in (1, 2)


def test_parts_of_different_battles_are_refused(tmp_path):
    a, b = tmp_path / "a.wrpl", tmp_path / "b.wrpl"
    a.write_bytes(synth.replay([synth.packet(1, 0, b"")], session=1))
    b.write_bytes(synth.replay([synth.packet(1, 0, b"")], session=2))
    with pytest.raises(wrpl.FormatError):
        convert.read([a, b])


#: A folder with the public sample replays of github.com/llama-for3ver/wt_replay_decoder (tests/replays),
#: kept outside the repository; set HEAT3D_WT_SAMPLES to it.
SAMPLES = Path(os.environ["HEAT3D_WT_SAMPLES"]) if os.environ.get("HEAT3D_WT_SAMPLES") else None


@pytest.mark.local
@pytest.mark.skipif(SAMPLES is None or not (SAMPLES / "client_2.wrpl").exists(), reason="HEAT3D_WT_SAMPLES not set")
def test_real_2025_air_battle(tmp_path):
    """A client replay of a 2025 air battle (version 101301): what was checked by hand stays true."""
    _, doc = convert.convert([SAMPLES / "client_2.wrpl"], tmp_path)
    d = json.loads(doc.read_text(encoding="utf-8"))
    c = d["counts"]
    assert d["flightLayout"] == "2025"
    assert c["aircraftUids"] >= 30 and c["aircraftSamples"] > 38000
    assert 3.5 < c["aircraftHz"] < 4.5
    assert len(d["kills"]) == 29 and len(d["chat"]) == 11
    assert d["selfCheck"]["lifeVehicleInPlayersCrafts"] >= 10
    assert d["selfCheck"]["lifeVehicleNotInPlayersCrafts"] == 0


def test_names_from_a_localisation_table():
    raw = ('"<ID|readonly|noverify>";"<English>";"<German>"\r\n'
           '"la-7_0";"La-7";"La-7"\r\n"la-7_1";"La-7";"La-7"\r\n'
           '"yak-3_france_0";"▄Yak-3";"▄Jak-3"\r\n'
           '"ships/fishboat1_0";"Boat";"Boot"\r\n').encode("utf-8")
    n = names.Names(names.read_table(raw))
    assert n.lookup("la-7") == ("La-7", "La-7", "la-7_0")
    assert n.lookup("yak-3_france") == ("Yak-3", "Yak-3", "yak-3_france_0")  # the font's mark is dropped
    assert n.lookup("fishboat1", "ships")[0] == "Boat"
    assert n.lookup("no_such_plane") == ("", "", "")
    assert names.Names(names.read_table(raw, "<German>")).lookup("yak-3_france")[0] == "Jak-3"


def _remote_battle() -> bytes:
    """
    The author flies north; uid 346 (another player) flies a steady left circle, but like a client replay the
    file has it as the client saw it: a received state every 1 s, and in between straight on at that state's
    velocity, rolled on at a constant rate, and snapped back at the next state.
    """
    packets = [synth.packet(4, 100, synth.slots({0: (111, "Pilot One", 1), 1: (222, "Pilot Two", 2)}))]
    radius, speed = 1000.0, 150.0
    w = speed / radius

    def truth(t):
        return radius * math.cos(w * t), 3000.0, radius * math.sin(w * t)

    for i in range(161):
        t = i * 0.25
        k = t - t % 1.0  # the last received state
        x0, y0, z0 = truth(k)
        vx, vz = -speed * math.sin(w * k), speed * math.cos(w * k)
        dt = t - k
        pos = (x0 + vx * dt, y0, z0 + vz * dt)
        compass = math.degrees(math.atan2(vx, vz))
        roll = 20.0 + 40.0 * dt  # spinning on between updates (packed sign)
        packets.append(synth.packet(2, 1000 + i * 250, synth.flight([
            (344, 0.0, 3000.0, 5000.0 + 200 * t, synth.attitude(0)),
            (346, *pos, synth.attitude(compass, 0.0, roll)),
        ])))
    return synth.replay(packets, RESULTS)


def test_dead_reckoning_is_marked_and_put_back_on_the_path(tmp_path):
    f = tmp_path / "r.wrpl"
    f.write_bytes(_remote_battle())
    table, _ = convert.convert([f], tmp_path / "out", names=NAMES)
    rows = [r for r in pq.read_table(table).to_pylist() if r["event"] == "position" and r["uid"] == 346]
    assert len(rows) == 161
    ext = [r for r in rows if r["extrapolated"]]
    assert 100 <= len(ext) <= 125  # three of every four samples, less the first run
    radius = 1000.0
    off_raw = max(abs(math.hypot(r["xRaw"], r["zRaw"]) - radius) for r in ext)
    # (the last second ends on the track's last sample, whose velocity is only the chord's)
    off = max(abs(math.hypot(r["x"], r["z"]) - radius) for r in ext if r["time"] < 40)
    assert off_raw > 6 and off < 0.1  # the straight line leaves the circle by 6.3 m; the cubic stays on it
    assert max(r["moved"] for r in ext) == pytest.approx(off_raw, abs=2)
    # The attitude between received states turns evenly instead of spinning on: the packed roll goes 20 to 50
    # deg (left wing down) and back each second; the table holds about -20 (right wing down positive).
    assert all(abs(r["roll"] + 20) < 1.5 for r in rows[4:-4] if r["extrapolated"])
    assert {round(r["rollRaw"]) for r in ext} >= {-30, -40}
    # The recording player's own aircraft is never moved.
    own = [r for r in pq.read_table(table).to_pylist() if r["uid"] == 344 and r["event"] == "position"]
    assert {r["moved"] for r in own} == {0.0}


def test_smoothing_can_be_switched_off(tmp_path):
    f = tmp_path / "r.wrpl"
    f.write_bytes(_remote_battle())
    table, doc = convert.convert([f], tmp_path / "out", smoothing=False, names=NAMES)
    rows = [r for r in pq.read_table(table).to_pylist() if r["event"] == "position" and r["uid"] == 346]
    assert any(r["extrapolated"] for r in rows)
    assert all((r["x"], r["z"]) == (r["xRaw"], r["zRaw"]) and r["moved"] == 0 for r in rows)
    assert json.loads(doc.read_text(encoding="utf-8"))["selfCheck"]["deadReckoning"]["on"] is False


def test_hit_rows_name_the_attacker_from_the_slot(tmp_path):
    """A hit whose attacker uid has no track at that moment is still put down to the slot's player."""
    packets = [synth.packet(4, 100, synth.slots({0: (111, "Pilot One", 1), 1: (222, "Pilot Two", 2)}))]
    for i in range(20):
        packets.append(synth.packet(2, 1000 + i * 250, synth.flight([(345, 50.0 * i, 3000.0, 0.0, 0)])))
        if i == 10:
            packets.append(synth.packet(4, None, synth.damage(345, 600, 1, "mig_29smt_9_19")))
    f = tmp_path / "h.wrpl"
    f.write_bytes(synth.replay(packets, RESULTS))
    table, _ = convert.convert([f], tmp_path / "out", names=NAMES)
    hit = next(r for r in pq.read_table(table).to_pylist() if r["event"].startswith("hit"))
    assert hit["other"] == "Pilot Two" and hit["weapon"] == "mig_29smt_9_19"
