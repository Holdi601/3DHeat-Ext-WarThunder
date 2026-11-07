"""The entity stream and the other messages read since 0.3, on streams built in code (no replay bytes)."""

from __future__ import annotations

import json
import os
import struct
from pathlib import Path

import pyarrow.parquet as pq
import pytest

import synth
from heat3d_ext_warthunder import convert, ecs, wrpl
from heat3d_ext_warthunder import names as vehicle_names
from heat3d_ext_warthunder.wrpl import Bits

TANK = [(0, "transform", "TMatrix"), (1, "unit_storage__tank", "0xunknown"), (2, "team", "int"),
        (3, "unit__className", "ecs::string"), (4, "uid", "int"), (5, "is_local", "bool"),
        (6, "unit__playerId", "int"), (7, "unit__missionName", "ecs::string"), (8, "modEids", "ecs::EidList")]


def tank_block(uid: int, team: int, name: str, mission: str, first: bool = True, pid: int | None = None) -> bytes:
    head = synth.template(0, "tank", TANK) if first else synth.uleb(0)
    entries = [
        (0, synth.tmatrix(100.0, 20.0, -300.0)),
        (0, bytes([0x5A, 0x00, 0x13, 0x37, 0x00, 0x13, 0x00])),  # a value of the game's own type
        (0, struct.pack("<i", team)),
        (0, name.encode() + b"\0"),
        (0, struct.pack("<i", uid)),
        (0, synth.BitWriter().flag(True)),  # is_local: one bit, so what follows is not byte-aligned
    ]
    if pid is not None:
        entries.append((0, struct.pack("<i", pid)))
    # The mission name's step skips unit__playerId when that is not written.
    entries += [(0 if pid is not None else 1, mission.encode() + b"\0"), (0, synth.uleb(2) + synth.eid(7) + synth.eid(8))]
    return synth.construction(head, entries)


def test_fnv1a_is_the_engines_hash():
    assert ecs.fnv1a("transform") == 0xE1AD931B and ecs.fnv1a("TMatrix") == 0xA27250C6
    assert ecs.NAMES[ecs.fnv1a("unit__className")] == "unit__className"


def test_eid_forms():
    assert ecs.read_eid(Bits(synth.le(5 << 2 | 1, 2))) == 5
    assert ecs.read_eid(Bits(synth.le(5 << 2 | 3, 2))) == 5 | 1 << 22
    assert ecs.read_eid(Bits(synth.le(5 << 2 | 2, 2) + b"\x01")) == 5 | 3 << 22
    v = (9 << 2) | (4 << 22)
    assert ecs.read_eid(Bits(synth.le(v & 0xFFFF, 2) + synth.le(v >> 16, 2))) == 9 | 4 << 22


def test_lz4_block_with_a_match():
    # "abcd", then 8 bytes copied from 4 back (an overlapping copy), then "xyz"
    block = bytes([4 << 4 | 4]) + b"abcd" + synth.le(4, 2) + bytes([3 << 4]) + b"xyz"
    assert ecs.lz4_block(block) == b"abcdabcdabcdxyz"
    with pytest.raises(wrpl.FormatError):
        ecs.lz4_block(bytes([1 << 4 | 0]) + b"a" + synth.le(9, 2))


def test_a_unit_is_read_past_a_value_of_unknown_length():
    s = ecs.Stream()
    s.feed(synth.creation([(3, tank_block(177, 2, "tankModels/us_m1_abrams", "t2_tank_01", pid=4))]), 1.5)
    (e,) = s.entities
    assert e.template == "tank" and e.eid == 3 and e.t == 1.5
    assert e.uid == 177 and e.class_name == "tankModels/us_m1_abrams"
    assert e.comps["team"] == 2 and e.comps["unit__playerId"] == 4 and e.comps["is_local"] is True
    assert e.comps["unit__missionName"] == "t2_tank_01" and e.comps["modEids"] == [7, 8]
    assert e.comps["transform"]["pos"] == [100.0, 20.0, -300.0]
    assert e.skipped == ["unit_storage__tank"] and not s.problems


def test_compressed_creation_reused_template_and_destruction():
    s = ecs.Stream()
    s.feed(synth.creation([(3, tank_block(177, 2, "tankModels/a", "m1"))]), 1.0)
    s.feed(synth.creation([(4, tank_block(178, 1, "tankModels/b", "m2", first=False))], compress=True), 2.0)
    s.feed(synth.destruction([3]), 5.0)
    a, b = s.entities
    assert (b.uid, b.class_name, b.comps["team"]) == (178, "tankModels/b", 1)
    assert a.destroyed == 5.0 and b.destroyed is None
    assert s.counts["0x24"] == 1 and s.counts["0x25"] == 1 and s.counts["0x26"] == 1


def test_projectile_release():
    head = synth.template(1, "bomb", [(9, "bomb_component", "Bomb"), (10, "active", "bool")])
    blob = synth.projectile_blob((1200.0, 3000.0, -500.0), (0.0, 0.0, 0.0, 1.0), (200.0, -5.0, 0.0))
    s = ecs.Stream()
    s.feed(synth.creation([(12, synth.construction(head, [(0, blob), (0, synth.BitWriter().flag(True))]))]), 7.0)
    rel = ecs.release(s.entities[0])
    assert rel == {"pos": [1200.0, 3000.0, -500.0], "quat": [0.0, 0.0, 0.0, 1.0], "vel": [200.0, -5.0, 0.0]}


def test_shells():
    got = wrpl.read_shells(synth.shells([(0, 12, 10.0, 20.0, 30.0), (2, 13, -1.0, -2.0, -3.0)]))
    assert got == [(0, 12, 10.0, 20.0, 30.0, True), (2, 13, -1.0, -2.0, -3.0, True)]


def test_cockpit():
    payload = b"\x03\x58\x4a\xd0\x80\x0b\x02\x00" + struct.pack("<Hf", 40, 1234.5) + struct.pack("<Hf", 64, 90.0)
    assert wrpl.read_cockpit(payload) == {40: 1234.5, 64: 90.0}


def test_objects_both_shapes():
    zone = synth.text("ndom_capture_area_01") + synth.text("ship_buoys") + struct.pack(
        "<12f", 100, 0, 0, 0, 1, 0, 0, 0, 100, 3185.5, 70.0, -1536.0)
    field = synth.text("kabul_airfield") + bytes([3]) + struct.pack("<9f", 0, 1500, 0, 100, 1500, 0, 200, 1500, 30)
    out = wrpl.read_objects(b"\x02\x58\x39\xd0\x00" + zone + b"\x00" + field)
    a, b = out
    assert a["name"] == "ndom_capture_area_01" and a["model"] == "ship_buoys" and a["pos"] == [3185.5, 70.0, -1536.0]
    assert a["size"] == [100.0, 1.0, 100.0]
    assert b["name"] == "kabul_airfield" and len(b["points"]) == 3 and b["pos"] == [100.0, 1500.0, 10.0]


def test_explosion_part_kill_and_award_fields():
    boom = b"\x02\x58" + synth.le(wrpl.EXPLOSION, 2) + synth.id_fields({
        1: (32, b"\x8b\x01\x00\x00"), 2: (96, struct.pack("<3f", 1.0, 2.0, 3.0)),
        3: (32, struct.pack("<f", 1.0)), 4: (96, struct.pack("<3f", 0.0, -1.0, 0.0))})
    e = wrpl.read_explosion(boom)
    assert e["pos"] == [1.0, 2.0, 3.0] and e["dir"] == [0.0, -1.0, 0.0] and e["kind"] == "8b010000"
    part = b"\x02\x58" + synth.le(wrpl.PART_KILL, 2) + synth.id_fields({1: (16, synth.le(114 | 0x800, 2)),
                                                                        2: (16, synth.le(4504, 2))})
    assert wrpl.read_part_kill(part) == {"uid": 114, "part": 4504}
    award = b"\x02\x58" + synth.le(wrpl.STREAK, 2) + synth.id_fields({
        1: (32, synth.le(4, 4)), 2: (8 + 8 * 11, synth.text("first_blood")), 3: (32, synth.le(1, 4))})
    assert wrpl.read_streak(award)["award"] == "first_blood"


def test_ground_attitude_from_the_16_bit_angles():
    body = synth.BitWriter().raw(b"\x00").flag(True).u16(16384).u16(65536 - 182).u16(364).flag(False).flag(True)
    body.f32(1.0).f32(2.0).f32(3.0)
    x, y, z, heading, pitch, roll, packed = wrpl._ground_position(body.bytes(), False)
    assert packed is False
    # yaw 90 deg from east is south: compass 180
    assert (x, y, z) == (1.0, 2.0, 3.0) and heading == pytest.approx(180.0)
    assert pitch == pytest.approx(-1.0, abs=0.01) and roll == pytest.approx(2.0, abs=0.01)


def test_ground_attitude_from_a_quaternion():
    import math
    half = math.radians(-90.0) / 2  # a turn of -90 deg about up: compass 0 (north)
    body = synth.BitWriter().raw(b"\x00").flag(True)
    body.f32(0.0).f32(math.sin(half)).f32(0.0).f32(math.cos(half)).flag(False).flag(False).flag(True)
    body.f32(5.0).f32(0.0).f32(6.0)
    got = wrpl._ground_position(body.bytes(), True)
    assert got[:3] == (5.0, 0.0, 6.0) and min(got[3], 360 - got[3]) == pytest.approx(0.0, abs=1e-3)
    assert got[4] is None and got[5] is None


def battle_with_entities(more: list[bytes] | None = None) -> bytes:
    """Two fighters (uids 344, 345) and a tank (177), created by the entity stream; 344 drops a bomb at 6 s."""
    air = [(20, "transform", "TMatrix"), (21, "team", "int"), (22, "unit__className", "ecs::string"),
           (23, "uid", "int"), (24, "unit__playerId", "int")]

    def plane(uid: int, team: int, vehicle: str, pid: int, first: bool) -> bytes:
        head = synth.template(2, "aircraft+player_unit", air) if first else synth.uleb(2)
        return synth.construction(head, [(0, synth.tmatrix(0, 0, 0)), (0, struct.pack("<i", team)),
                                         (0, vehicle.encode() + b"\0"), (0, struct.pack("<i", uid)),
                                         (0, struct.pack("<i", pid))])

    packets = [synth.packet(1, 0, b""),
               synth.packet(4, 100, synth.slots({0: (111, "Pilot One", 1), 1: (222, "Pilot Two", 2)})),
               synth.packet(6, 200, synth.creation([(1, plane(344, 1, "f_15a", 0, True)),
                                                    (2, plane(345, 2, "mig_29smt_9_19", 1, False)),
                                                    (3, tank_block(177, 2, "tankModels/germ_flakpz_gepard", "t2_aa"))]))]
    bomb = synth.template(1, "bomb", [(9, "bomb_component", "Bomb"), (10, "active", "bool")])
    for i in range(81):
        ms = 1000 + i * 250
        t = i * 0.25
        packets.append(synth.packet(2, ms, synth.flight([
            (344, 0.0, 3000.0, 1000.0 + 200 * t, synth.attitude(0)),
            (345, 50.0, 3000.0, 1300.0 + 200 * t, synth.attitude(0)),
        ])))
        if i % 4 == 0:
            packets.append(synth.packet(4, None, synth.ground({177: (500.0, 120.0, 800.0 + t)}, number=i // 4)))
        if ms == 6000:
            blob = synth.projectile_blob((10.0, 2990.0, 1000.0 + 200 * t), (0, 0, 0, 1), (0, -10, 200))
            packets.append(synth.packet(6, ms, synth.creation([(12, synth.construction(bomb, [(0, blob)]))])))
        if 6000 < ms <= 8000:
            packets.append(synth.packet(4, None, synth.shells([(1, 12, 10.0, 2990.0 - (t - 5) * 100, 2000.0 + 150 * (t - 5))])))
        if ms == 8000:
            packets.append(synth.packet(6, 8100, synth.destruction([12])))
        if ms == 11000:
            packets.append(synth.packet(4, None, synth.kill(344, 0, "f_15a", 345, 7, "us_aim9l_sidewinder")))
    packets += more or []
    packets.append(synth.packet(0, 21000, b""))
    return synth.replay(packets, {"timePlayed": 21.0, "authorUserId": "111", "author": "Pilot One"})


def test_convert_names_units_from_the_entity_stream(tmp_path):
    f = tmp_path / "e.wrpl"
    f.write_bytes(battle_with_entities())
    tpath, jpath = convert.convert([f], tmp_path / "out")
    rows = pq.read_table(tpath).to_pylist()
    doc = json.loads(jpath.read_text(encoding="utf-8"))
    two = [r for r in rows if r["player"] == "Pilot Two" and r["event"] == "position"]
    assert two and {r["Vehicle"] for r in two} == {"mig_29smt_9_19"} and {r["team"] for r in two} == {"2"}
    assert {r["kind"] for r in two} == {"aircraft"}
    # After the kill at 11 s the samples are its wreck.
    assert {r["alive"] for r in two if r["time"] > 11.0} == {0.0} and {r["alive"] for r in two if r["time"] < 11} == {1.0}
    gepard = [r for r in rows if r["uid"] == 177]
    assert gepard[0]["kind"] == "spaa" and gepard[0]["Vehicle"] == "germ_flakpz_gepard"
    assert gepard[0]["player"] == "germ_flakpz_gepard #177" and gepard[0]["mission"] == "t2_aa"
    assert gepard[0]["heading"] == pytest.approx(90.0)  # the synthetic states say yaw 0: east
    launch = next(r for r in rows if r["event"] == "launch")
    assert launch["player"] == "Pilot One" and launch["weapon"] == "bomb" and launch["time"] == pytest.approx(6.0)
    flight = [r for r in rows if r["life"].startswith("w")]
    assert len(flight) == 8 and flight[-1]["event"] == "impact" and flight[0]["kind"] == "bomb"
    assert flight[0]["track"].startswith("Pilot One bomb #") and flight[0]["team"] == "1"
    assert len({r["track"] for r in rows}) == 4  # two fighters, the tank, the bomb
    assert doc["selfCheck"]["recordVehicleMatchesEntity"] >= 1 and doc["selfCheck"]["weaponsWithLauncher"] == 1
    assert {u["vehicle"] for u in doc["units"]} == {"f_15a", "mig_29smt_9_19", "germ_flakpz_gepard"}
    w = doc["weapons"][0]
    assert w["launcher"] == "Pilot One" and w["launcherDistance"] == pytest.approx(14.1, abs=0.2) and w["removed"] == 8.1
    assert doc["kills"][0]["victim"] == "Pilot Two" and doc["kills"][0]["victimVehicle"] == "mig_29smt_9_19"
    assert doc["counts"]["fromEntities"] == 3 and not doc["counts"]["unreadPackets"]


def test_chat_line_with_the_2026_tail():
    payload = synth.text("Pilot One") + synth.text("Thank you!") + bytes.fromhex("00c1cc080c080c080c00")
    assert wrpl.read_chat(payload) == {"sender": "Pilot One", "text": "Thank you!"}


def test_a_packet_ahead_of_its_time_is_retimed():
    # Six aircraft fly north at 200 m/s, sampled every 0.25 s; at 2.0 s the client wrote all but uid 0 (the
    # recorder's own) where they would be 0.75 s later.
    frames = []
    for i in range(12):
        t = i * 0.25
        lead = 0.75 if i == 8 else 0.0
        frames.append((t, [convert.Sample(t, 100.0 * u, 3000.0, 200.0 * (t + (lead if u else 0.0)), uid=u)
                           for u in range(6)]))
    done = convert._retime(frames)
    assert len(done) == 1 and done[0]["lead"] == pytest.approx(0.75, abs=0.01) and done[0]["moved"] == 5
    moved = frames[8][1]
    assert moved[0].t == 2.0 and not moved[0].retimed
    assert all(s.t == pytest.approx(2.75, abs=0.01) and s.retimed for s in moved[1:])


def test_a_slow_aircraft_is_held_to_its_own_pace(tmp_path):
    # A piston fighter at 120 m/s for 30 s, weaving a little (its samples received, not dead-reckoned); one
    # sample 140 m ahead (560 m/s for that step): under the jets' 750 m/s, over its own 1.6 x 120 m/s, floored
    # at 250 m/s.
    packets = []
    for i in range(120):
        z = 30.0 * i + (110.0 if i >= 60 else 0.0)
        x = 0.5 * (i % 2)
        packets.append(synth.packet(2, 1000 + i * 250, synth.flight([(344, x, 3000.0, z, 0)])))
    f = tmp_path / "p.wrpl"
    f.write_bytes(synth.replay(packets, compress="zlib"))
    r = convert.read([f])
    lives = convert.lives(r)
    assert [life.id for life in lives] == ["344#1", "344#2"] and lives[0].limit == 250.0
    assert r.breaks[0]["limit"] == 250 and r.breaks[0]["distance"] == 140


def test_a_dead_reckoning_correction_does_not_cut(tmp_path):
    # A distant piston fighter as a client replay has it: a received state each second, flown on straight in
    # between and snapped 60 m to the next (480 m/s for that step); received to received it flies 120 m/s.
    packets = []
    for i in range(120):
        k, d = divmod(i, 4)
        x = 30.0 * k * k / 10.0  # its own path curves: each received state comes off the line
        z = 120.0 * k + 30.0 * d
        packets.append(synth.packet(2, 1000 + i * 250, synth.flight([(344, x, 3000.0, z, 0)])))
    f = tmp_path / "d.wrpl"
    f.write_bytes(synth.replay(packets, compress="zlib"))
    lives = convert.lives(convert.read([f]))
    assert [life.id for life in lives] == ["344#1"]
    assert sum(s.extrapolated for s in lives[0].samples) > 50


def test_a_track_is_cut_where_the_unit_moves_faster_than_it_can(tmp_path):
    packets = [synth.packet(4, 0, synth.slots({0: (111, "Pilot One", 1)}))]
    for i in range(40):
        x = 0.0 if i < 20 else 2400.0  # moved 2.4 km between two samples 0.25 s apart, in the air
        packets.append(synth.packet(2, 1000 + i * 250, synth.flight([(344, x, 3000.0, 50.0 * i, 0)])))
    f = tmp_path / "a.wrpl"
    f.write_bytes(synth.replay(packets, compress="zlib"))
    r = convert.read([f])
    lives = convert.lives(r)
    assert [life.id for life in lives] == ["344#1", "344#2"]
    (b,) = r.breaks
    assert b["distance"] == 2401 and b["seconds"] == 0.25  # 2400 m east, 50 m north


#: A folder of 2026 replays of your own (never in the repository); set HEAT3D_WT_REPLAYS to it.
OWN = os.environ.get("HEAT3D_WT_REPLAYS")


@pytest.mark.local
@pytest.mark.skipif(not OWN, reason="HEAT3D_WT_REPLAYS not set")
def test_own_replays_have_no_step_faster_than_the_unit_can_go(tmp_path):
    """Every track of every replay in the folder: no step between consecutive rows faster than its kind can go."""
    files = sorted(Path(OWN).glob("*.wrpl"))
    assert files
    names = vehicle_names.Names.from_game()
    arms = vehicle_names.Weapons.from_game()
    for f in files:
        table, doc = convert.convert([f], tmp_path, names=names, weapon_names=arms)
        d = json.loads(doc.read_text(encoding="utf-8"))
        # Every statistic of every player at the end equals the results'; the decoded velocity follows the track.
        sb = d["selfCheck"]["scoreboardVsResults"]
        assert sb and all(a == b for a, _, b in (v.partition(" of ") for v in sb.values())), (f.name, sb)
        fe = d["selfCheck"]["flightEntries"]
        for who in ("velocity_author", "velocity_others"):
            if fe[who]["samples"] > 100:
                assert fe[who]["angleMedian"] < 3 and abs(fe[who]["speedRatioMedian"] - 1) < 0.01, (f.name, fe)
        assert d["entityMessages"]["classBits"] is not None, f.name
        if arms:  # a ship's default belts (`*_universal`) are the ones the game names nowhere
            wn = d["selfCheck"]["weaponNames"]
            assert all(w.endswith("_universal") for w in wn["notNamed"]), (f.name, wn)
        # An event row says where its unit points (a ship's latest row is mostly gunfire).
        t = pq.read_table(table, columns=["event", "track", "heading"]).to_pylist()
        fired = [r for r in t if r["track"] and r["event"] in ("fire_start", "fire_stop", "gun_shot", "kill")]
        assert all(r["heading"] is not None and r["heading"] == r["heading"] for r in fired), f.name
        steps = d["selfCheck"]["stepSpeed"]
        assert all(v["faster than possible"] == 0 for v in steps.values()), (f.name, steps)
        assert all(v["faster than its own limit"] == 0 for v in steps.values()), (f.name, steps)
        # The recording player's own aircraft is not extrapolated: its own pace never cuts it (only respawns do).
        mine = {u for p in d["players"] if p["userId"] == str(d["authorUserId"]) for u in p["uids"]}
        assert not [b for b in d["trackBreaks"] if b.get("uid") in mine and "limit" in b], f.name
        assert steps.get("aircraft", {"max": 0})["max"] <= convert.TOP_SPEED["air"], f.name
        assert d["selfCheck"]["recordVehicleMatchesEntity"] > 0 and not d["selfCheck"].get("recordVehicleDiffersFromEntity")
        # Every row of a player the results name is a player's, not AI; every ground unit and ship row of a
        # non-player is AI (a naval battle's player ships are players).
        ident = d["selfCheck"]["identity"]
        assert ident["rowsOfPlayersAi"] == 0 and ident["rowsOfPlayersNotAi"] > 0, (f.name, ident)
        assert ident["rowsNotAiNotAPlayerName"] == 0, (f.name, ident)
        # The flight model's roll is turned to right wing down positive: the recording player's own turns agree.
        att = d["selfCheck"]["aircraftAttitude"]
        if att["turnsRollRightWingDownAgrees"] + att["turnsRollDisagrees"] >= 20:
            assert att["turnsRollRightWingDownAgrees"] > 9 * att["turnsRollDisagrees"], (f.name, att)
            assert att["headingVsTravelMedianDeg"] < 5, (f.name, att)
        # Dead reckoning: the own aircraft is (almost) never extrapolated; the smoother leaves fewer impossible steps.
        dr = d["selfCheck"]["deadReckoning"]
        if "own" in dr:
            assert dr["own"]["extrapolatedShare"] < 0.05 and dr["own"]["movedMetres"]["samples"] == 0, (f.name, dr)
        if "remote" in dr:
            acc = dr["remote"]["accelerationG"]
            assert acc["table"]["over15g"] < acc["replay"]["over15g"], (f.name, dr)
        if names:
            assert d["selfCheck"]["vehicleNames"]["named"] >= 0.9 * d["selfCheck"]["vehicleNames"]["vehicles"], f.name


def test_messages_to_units_name_their_entity(tmp_path):
    """
    Messages to units carry the unit's entity (index << 10 | generation): a projectile hit on 345 (entity 2) from
    344, its engine rpm, its death. The hit becomes a shot row on 344's track aimed at 345, 2 m behind its centre.
    """
    more = [synth.packet(4, 10900, synth.unit_message(2, 0xF0E9, synth.hit_effect(344, 7, (-200, 0, 0)))),
            synth.packet(4, 10950, synth.unit_message(1, 0xD047, synth.rpm(2400))),
            synth.packet(4, 11000, synth.unit_message(2, 0xF04B, b""))]
    f = tmp_path / "u.wrpl"
    f.write_bytes(battle_with_entities(more))
    tpath, jpath = convert.convert([f], tmp_path / "out")
    rows = pq.read_table(tpath).to_pylist()
    doc = json.loads(jpath.read_text(encoding="utf-8"))
    shot = next(r for r in rows if r["event"] == "shot")
    assert shot["player"] == "Pilot One" and shot["other"] == "Pilot Two" and shot["time"] == pytest.approx(10.9)
    # 345 flies north at z = 1300 + 200 t; the hit point is 2 m behind it.
    assert (shot["targetX"], shot["targetZ"]) == pytest.approx((50.0, 1300.0 + 200 * 9.9 - 2.0), abs=0.6)
    assert shot["dirZ"] > 0.9  # 344 is behind and below it
    dead = next(r for r in rows if r["event"] == "dead")
    assert dead["player"] == "Pilot Two" and dead["time"] == pytest.approx(11.0)
    one = [r for r in rows if r["player"] == "Pilot One" and r["event"] == "position" and r["time"] > 11]
    assert {r["rpm"] for r in one[:3]} == {2400.0}
    u = doc["selfCheck"]["unitMessages"]
    assert u["messages"] == u["withEntity"] == 3 and u["projectileHits"] == 1
    assert u["shooters"]["attackerAmongShooters"] == 1  # the kill at 11 s names 344, as the hit at 10.9 does
    side = pq.read_table(tpath.with_name(tpath.name.replace(".parquet", ".messages.parquet"))).to_pylist()
    assert {(r["message"], r["uid"]) for r in side if r["packet"] == 4} >= {("0xf0e9", 345), ("0xd047", 344)}


def test_replicated_components_are_read(tmp_path):
    """A replication packet (0x22): time, sequence, then per entity its eid, a block size and component values."""
    w = synth.BitWriter()
    w.raw(struct.pack("<I", 1234)).raw(struct.pack("<H", 7))
    block = synth.BitWriter().flag(True).raw(bytes([21])).raw(struct.pack("<i", 2)).flag(False).bytes()
    w.flag(True).raw(synth.eid(1)).raw(bytes([len(block)])).raw(block).flag(False)
    more = [synth.packet(6, 9000, bytes([0x22]) + w.bytes())]
    f = tmp_path / "r.wrpl"
    f.write_bytes(battle_with_entities(more))
    r = convert.read([f])
    assert [(eid & 0x3FFFFF, comp, v) for _, eid, comp, _, v, _ in r.stream.replications] == [(1, "team", 2)]


def test_entity_message_class_width_is_found_by_its_parity_bit():
    def message(cls: int, width: int, body: bytes) -> bytes:
        w = synth.BitWriter()
        for i in range(0, width, 8):  # the number a byte's worth at a time, the first group lowest
            k = min(8, width - i)
            w.bits(cls >> i & ((1 << k) - 1), k)
        if width & 7:
            w.bits(bin(cls).count("1") & 1, 1)
        return w.bytes() + body
    msgs = [(0.0, 5, message(c, 6, b"\x07\x01")) for c in (33, 40, 9, 62, 1)]
    width, classes = ecs.message_classes(msgs)
    assert width == 6 and classes == [33, 40, 9, 62, 1]
    assert ecs.message_classes([])[0] is None
