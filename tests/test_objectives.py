import struct

import pytest
import synth

from heat3d_ext_warthunder import convert, objectives, wrpl


def test_server_states_give_their_turrets_whatever_follows():
    # A server replay's tank state goes on after the turrets; its length no longer fits the client's layout.
    body = synth.tank_state(1.0, 2.0, 3.0, [(30.0, 5.0), (-90.0, 0.0)]) + bytes(40)
    client = wrpl.GroundReader().read(synth.ground(None, 1, tanks={5: (body, 2)}))
    server = wrpl.GroundReader().read(synth.ground(None, 1, tanks={5: (body, 2)}, message=wrpl.GROUND_SERVER))
    assert client[0][8] == []
    assert [tuple(round(v, 2) for v in t) for t in server[0][8]] == [(30.0, 5.0), (-90.0, 0.0)]
    # A state too short for the second turret still gives the first.
    short = synth.tank_state(1.0, 2.0, 3.0, [(12.0, -3.0)])
    got = wrpl.GroundReader().read(synth.ground(None, 1, tanks={5: (short, 2)}, message=wrpl.GROUND_SERVER))
    assert [tuple(round(v, 2) for v in t) for t in got[0][8]] == [(12.0, -3.0)]


def test_mode_in_the_match_name():
    h = {"map": "test_map", "difficulty": 5, "startTime": 86400, "sessionId": "ab", "server": True,
         "locName": "missions/_Conq4;test/name"}
    assert convert.match_name(h) == "test_map_RB_Conq4_1970-01-02_00-00-00_ab_server"
    assert convert.match_name({**h, "locName": ""}) == "test_map_RB_1970-01-02_00-00-00_ab_server"
    assert convert.mission_mode({"locName": "missions/_Dom"}) == "Dom"


def test_view_in_the_hull_frame():
    s = convert.Sample(0.0, 0.0, 0.0, 0.0, angles=(90.0, 0.0, 0.0))
    yaw, pitch = convert._in_hull(s, 120.0, 4.0)
    assert yaw == pytest.approx(30.0, abs=0.01) and pitch == pytest.approx(4.0, abs=0.01)  # in the hull frame (check only)


def test_classes_teams_and_shapes():
    assert objectives.classify("dom_capture_area_01_arcade") == "capture_zone"
    assert objectives.classify("briefing_zone01") is None
    assert objectives.classify("t1_spawn_01_spawnarea03") == "spawn"
    assert objectives.classify("bdt_t2_bomb_zone_01") == "bombing_target"
    assert objectives.classify("bdt_t2_bomb_zone_01_aaa_point_01") is None
    assert objectives.team_of("t2_air_spawn_arcade") == 2 and objectives.team_of("briefing_teamA_spawn") == 1
    assert objectives.team_of("battle_area") is None
    tm = [40, 0, 0, 0, 40, 0, 0, 0, 40, 100, 5, 200]
    assert objectives.shape("Sphere", tm) == {"shape": "sphere", "position": [100, 5, 200], "radius": 40}
    box = objectives.shape("Box", [0, 0, -500, 0, 50, 0, 300, 0, 0, 1, 2, 3])
    assert box["size"] == [500, 50, 300] and box["heading"] == 90.0


def area(name, kind, x, z, r=20.0):
    return {"name": name, "type": kind, "tm": [r, 0, 0, 0, r, 0, 0, 0, r, x, 1.0, z], "file": "f"}


def test_mission_objectives_of_this_mode_and_difficulty():
    areas = [area("conq_capture_area_01_arcade", "Sphere", 10, 10), area("dom_capture_area_01_arcade", "Sphere", 9, 9),
             area("conq_battle_area_arcade", "Box", 5, 5, 500), area("conq_battle_area_hardcore", "Box", 5, 5, 400),
             area("t1_spawn_01_spawnarea01", "Point", 100, 0), area("t1_spawn_01_spawnarea02", "Sphere", 110, 0),
             area("t2_air_spawn_hardcore", "Sphere", 0, 9000, 300), area("airfields_area", "Sphere", 5, 5, 30000),
             area("spawn_template", "Sphere", 0, 0), area("briefing_zone01", "Point", 10, 10)]
    got = {o["name"]: o for o in objectives.mission_objectives(areas, "Conq2", "RB")}
    assert set(got) == {"conq_capture_area_01_arcade", "conq_battle_area_hardcore", "t1_spawn_01",
                        "t2_air_spawn_hardcore"}
    assert got["t1_spawn_01"]["points"] == [[100, 1.0, 0], [110, 1.0, 0]] and got["t1_spawn_01"]["team"] == 1
    assert got["conq_battle_area_hardcore"]["size"] == [400, 400, 400]
    arcade = {o["name"] for o in objectives.mission_objectives(areas, "Conq2", "AB")}
    assert "conq_battle_area_arcade" in arcade and "conq_battle_area_hardcore" not in arcade


def transform(x, y, z, scale=1.0):
    return struct.pack("<12f", scale, 0, 0, 0, scale, 0, 0, 0, scale, x, y, z)


def test_replay_zones_and_their_captures():
    objs = [{"name": "cz_circle_01", "model": "capture_zone_circle", "pos": [0.0, 0.0, 0.0]},
            {"name": "cz_circle_02", "model": "capture_zone_circle", "pos": [10.0, 0.0, 0.0]},
            {"name": "t1_airfield", "model": "dynaf_x", "pos": [5000.0, 30.0, 0.0]}]
    k3, k5 = objectives.KIND_TRANSFORM * objectives.KIND_SPAN, objectives.KIND_ZONE * objectives.KIND_SPAN
    refl = [(4.0, 0, k3 + 0, None, {4: transform(300, 9, 400)}, b""),
            (4.0, 0, k3 + 1, None, {4: transform(600, 9, 400)}, b""),
            (4.0, 0, k3 + 2, None, {4: transform(5000, 30, 0)}, b""),
            (4.0, 0, k5 + 0, None, {2: b"\x00", 67: b"\x00", 69: b"\x00"}, b""),
            (4.0, 0, k5 + 1, None, {2: b"\x00", 67: b"\x00", 69: b"\x01"}, b""),
            (50.0, 0, k5 + 1, None, {67: b"\x9c"}, b""),
            (50.5, 0, k5 + 1, None, {2: b"\x01", 67: b"\x9c"}, b"")]
    out, rows = objectives.replay_objectives(refl, objs)
    zones = [o for o in out if o["type"] == "capture_zone"]
    assert [z["name"] for z in zones] == ["A", "B"] and zones[1]["position"] == [600, 9, 400]
    assert zones[1]["ownerAtStart"] == 0 and zones[1]["ownerAtEnd"] == 1
    assert out[2]["type"] == "airfield" and out[2]["team"] == 1 and not out[2]["moved"]
    assert [(r["zone"], r["event"], r.get("owner"), r.get("progress")) for r in rows[2:]] == [
        ("B", "progress", None, -100), ("B", "captured", 1, -100)]
    objectives.match_zones(out, [area("dom_capture_area_02_arcade", "Sphere", 600.5, 400, 40)])
    assert zones[1]["radius"] == 40 and zones[1]["shape"] == "sphere"


def test_spawns_decide_the_sides():
    objs = [{"type": "spawn", "team": 1, "name": "t1_spawn_01", "source": "mission", "position": [0, 0, 0],
             "radius": 20.0},
            {"type": "airfield", "team": 1, "name": "t1_airfield", "source": "replay", "position": [9, 0, 9]}]
    objectives.spawn_use(objs, [("2", 5.0, 0.0, 5.0), ("2", 30.0, 0.0, 0.0), ("1", 900.0, 0.0, 0.0)])
    assert objs[0]["used"] == 2 and objs[0]["usedByTeam"] == {"2": 2}
    assert objectives.replay_teams(objs)["swapped"]
    assert [o["team"] for o in objs] == [2, 2] and objs[1]["missionTeam"] == 1


def test_scene_units_are_named_and_stand_still(monkeypatch):
    tm = [1, 0, 0, 0, 1, 0, 0, 0, 1, 100.0, 9.8, 200.0]
    monkeypatch.setattr(convert, "_scene", lambda game, level: [("germ_railway_tram_a", "template:rail_wagon", True,
                                                                   tm)])
    samples = [convert.Sample(t * 0.5, 100.2, 9.8, 200.1, angles=(30.0, 0.0, 0.0)) for t in range(100)]
    life = convert.Life(8, "ground", 1, samples)
    r = convert.Replay([], {"level": "levels/test_level.bin"}, {}, {}, {}, [], [], [], 0, "")
    got = convert.scene_units(r, [life], None)
    assert got["matched"] == 1
    assert (life.vehicle, life.figure, life.type, life.team) == ("germ_railway_tram_a", "train", "tram", "")
    assert life.died is not None and life.died < samples[0].t
    # One sample every 10 s and the last: 0, 10, 20, ..., 40, 49.5.
    assert [s.t for s in life.samples] == [0.0, 10.0, 20.0, 30.0, 40.0, 49.5]
