"""The container and message readers, against payloads built to the documented layout (tests/synth.py)."""

from __future__ import annotations

import math
import struct

import pytest

import synth
from heat3d_ext_warthunder import wrpl


def test_bits_read_most_significant_first_and_numbers_little_endian():
    r = wrpl.Bits(bytes([0b10110000, 0x34, 0x12]))
    assert r.bits(1) == 1 and r.bits(3) == 0b011
    r.align()
    assert r.u16() == 0x1234
    with pytest.raises(EOFError):
        r.bits(1)
    assert wrpl.Bits(synth.uleb(300)).uleb() == 300
    assert wrpl.Bits(synth.uleb(5)).zigzag() == -3
    # Groups of up to 8 bits, the first lowest.
    assert wrpl.Bits(synth.BitWriter().bits(0x34, 8).bits(0x5, 5).bytes()).le_bits(13) == 0x534


def test_header_fields_and_map():
    h = wrpl.read_header(bytes(synth.header(level="levels/avg_test_land.bin", session=0xABC, server=True, part=3)))
    assert h["map"] == "avg_test_land"
    assert h["sessionId"] == "0000000000000abc"
    assert h["server"] and h["part"] == 3
    assert h["battleClass"] == "base_dom" and h["timeLimit"] == 25
    with pytest.raises(wrpl.FormatError):
        wrpl.read_header(b"\0" * 2000)


@pytest.mark.parametrize("compress", ["zstd", "zlib"])
def test_packet_stream_and_framing(compress):
    big = bytes(300)  # a two-byte size
    huge = bytes(20000)  # a three-byte size
    buf = synth.replay([synth.packet(1, 1000, b""), synth.packet(4, 1500, big), synth.packet(4, None, huge),
                        synth.packet(0, 2000, b"x")], compress=compress)
    h = wrpl.read_header(buf)
    got = [(p.type, p.ms, len(p.payload)) for p in wrpl.packets(wrpl.packet_stream(buf, h))]
    # The third has the second's time.
    assert got == [(1, 1000, 0), (4, 1500, 300), (4, 1500, 20000), (0, 2000, 1)]


def test_blk_nested_and_repeated():
    tree = {"status": "success", "timePlayed": 1.5, "n": -3, "ok": True,
            "player": [{"name": "A", "team": 1}, {"name": "B", "team": 2}],
            "ui": {"info": {"x": "y"}}}
    got = wrpl.read_blk(synth.blk(tree))
    assert got == tree
    with pytest.raises(wrpl.FormatError):
        wrpl.read_blk(b"\x02rest")


def test_kill_and_damage():
    k = wrpl.read_kill(synth.kill(372, 28, "su_25", 361, 4, "su_r_60"))
    assert k == {"killerPid": 28, "killerVehicle": "su_25", "victimUid": 361, "killerUid": 372, "weapon": "su_r_60",
                 "victimPid": 4}
    d = wrpl.read_damage(synth.damage(361, 372, 28, "su_25", severe=True))
    assert d == {"victimUid": 361, "pid": 28, "vehicle": "su_25", "uid": 372}
    assert wrpl.Packet(4, 0, synth.damage(1, 2, 3, "v", severe=True)).message == wrpl.SEVERE


def test_unknown_id_fields_are_skipped_by_their_width():
    body = synth.id_fields({1: (32, synth.le(7, 4)), 5: (24, b"abc"), 0xB: (32, synth.le(9, 4))})
    k = wrpl.read_kill(b"\x02\x58\x58\xf0" + body)
    assert k == {"killerPid": 7, "victimPid": 9}


@pytest.mark.parametrize("layout", ["2026", "2025"])
def test_flight_model(layout):
    planes = [(344, 100.5, 2000.0, -300.25, synth.attitude(90)), (345, -5.0, 10.0, 7.0, 0), (400, 1.0, 2.0, 3.0, 0)]
    payload = synth.flight(planes, layout)
    got, err = wrpl.read_flight(payload, layout)
    assert err is None
    assert [(u, x, y, z) for u, x, y, z, _ in got] == [(u, x, y, z) for u, x, y, z, _ in planes]
    assert wrpl.flight_layout([payload]) == layout
    other = "2025" if layout == "2026" else "2026"
    assert wrpl.read_flight(payload, other)[1] is not None


def test_attitude_is_counted_from_east():
    for compass in (0, 45, 90, 200, 315):
        h, p, r = wrpl._euler(synth.attitude(compass, pitch_deg=10, roll_deg=-30))
        off = (math.degrees(h + math.pi / 2) - compass + 180) % 360 - 180
        assert off == pytest.approx(0, abs=0.3)
        assert math.degrees(p) == pytest.approx(10, abs=0.3)
        assert math.degrees(r) == pytest.approx(-30, abs=0.3)


def test_ground_whole_then_delta():
    g = wrpl.GroundReader()
    first = g.read(synth.ground({177: (10.0, 150.0, -20.0), 180: (5.0, 1.0, 2.0)}, number=7))
    # The synthetic states' attitude is all zeros: yaw 0 from east, compass 90.
    assert first == [(177, 10.0, 150.0, -20.0, 90.0, 0.0, 0.0, False, [], None),
                     (180, 5.0, 1.0, 2.0, 90.0, 0.0, 0.0, False, [], None)]
    # An unchanged state, sent as a difference to packet 7.
    again = g.read(synth.ground({177: (0, 0, 0)}, number=8, delta={177}))
    assert again == [(177, 10.0, 150.0, -20.0, 90.0, 0.0, 0.0, False, [], None)]
    with pytest.raises(wrpl.FormatError):
        wrpl.GroundReader().read(synth.ground({177: (0, 0, 0)}, number=8, delta={177}))


def test_rle_of_zero_runs():
    assert wrpl._rle(bytes([0b00001100, 111])) == b"\0\0"
    with pytest.raises(wrpl.FormatError):
        wrpl._rle(b"\x00\x05")


def test_slots():
    got = wrpl.read_slots(synth.slots({3: (123456789012, "Pilot One", 1), 9: (5, "Two", 2)}), None)
    assert got == {3: {"userId": "123456789012", "name": "Pilot One", "team": 1},
                   9: {"userId": "5", "name": "Two", "team": 2}}


def test_chat_with_and_without_flag_byte():
    assert wrpl.read_chat(synth.chat("pilot", "hello")) == {"sender": "pilot", "text": "hello"}
    assert wrpl.read_chat(synth.chat("pilot", "hello", flag=False)) == {"sender": "pilot", "text": "hello"}
    with pytest.raises(wrpl.FormatError):
        wrpl.read_chat(b"\x00\x40abc")


def test_flight_entry_extras_wherever_the_entry_starts():
    # The second entry starts mid-byte: its 7 bytes are aligned to the packet, so the entry's phase is needed.
    word = synth.velocity_word(-120.0, 15.0, 240.0)
    extras = {
        344: {"word": word, "seven": bytes([0x0B, 0x5A, 0, 0, 0, 0x0C, 0]), "ammo": [250, 140, 170],
              "engines": [(7, 32767, None), (8, None, 90)]},
        345: {"word": word, "seven": bytes([0x04, 0x8C, 0, 0, 0, 0x03, 0]), "ammo": [1]},
    }
    payload = synth.flight([(344, 1.0, 2.0, 3.0, 0), (345, 4.0, 5.0, 6.0, 0)], extras=extras)
    raw: list = []
    got, err = wrpl.read_flight(payload, "2026", raw)
    assert err is None and len(raw) == 2
    assert {r[3] for r in raw} != {0}  # at least one entry starts mid-byte
    a, b = (wrpl.flight_extras(n, bits, "2026", phase) for _, n, bits, phase in raw)
    assert a["ammo"] == [250, 140, 170] and b["ammo"] == [1]
    assert a["nibbles"][1:4] == [11, 5, 10] and a["throttle"] == 12 / 15
    assert a["elevator"] == pytest.approx(3 / 7) and a["aileron"] == pytest.approx(-3 / 7)
    assert b["nibbles"][1:4] == [4, 8, 12] and b["throttle"] == 3 / 15
    assert a["engineStates"] == ["running", "dead"] and a["engines"][0][1] == 32767 and a["engines"][1][2] == 90
    for v, want in zip(a["velocity"], (-120.0, 15.0, 240.0)):
        assert v == pytest.approx(want, abs=0.6)


def test_velocity_word_signs_speed_and_cap():
    vx, vy, vz = wrpl.velocity(synth.velocity_word(10.0, -20.0, -30.0))
    assert (vx > 0, vy < 0, vz < 0) == (True, True, True)
    assert math.hypot(vx, vy, vz) == pytest.approx(math.hypot(10, 20, 30), abs=0.2)
    assert math.hypot(*wrpl.velocity(synth.velocity_word(0.0, 0.0, 900.0))) == pytest.approx(500.0)


def test_reflection_objects_both_forms_and_slot_statistics():
    stats = bytearray(54)
    for name, value in {"kills": 3, "deaths": 1, "assists": 2, "damageZone": 16659, "missileEvades": 27}.items():
        at, size = wrpl.SLOT_STATS[name]
        stats[at : at + size] = value.to_bytes(size, "little")
    body = synth.field_table({38: (874).to_bytes(4, "little") + bytes(12), 39: bytes(stats)})
    msg = synth.le(len(body) + 2, 2) + synth.le(0xE000 | 5, 2) + body
    flagged = b"\x02\x58\x2d\xf0" + b"\x00" + synth.le(1, 2) + msg
    plain = b"\x02\x58\xaa\xf0" + synth.le(1, 2) + msg
    for payload, flag in ((flagged, True), (plain, False)):
        (oid, ext, got), = wrpl.reflection_objects(payload, None, flag)
        assert oid == 0xE005 and ext is None
        s = wrpl.slot_stats(wrpl.reflection_fields(got))
        assert (s["kills"], s["deaths"], s["assists"], s["damageZone"], s["missileEvades"], s["score"]) == \
            (3, 1, 2, 16659, 27, 874)


def test_unit_messages_decoded():
    eff = synth.id_fields({1: (32, synth.le(4505, 4)), 2: (32, synth.le(0xDEADBEEF, 4)), 3: (8, 0), 4: (8, 0)})
    assert wrpl.read_effect(eff) == {"effect": 4505, "seed": 0xDEADBEEF, "f3": "00", "f4": "00"}
    gun = synth.id_fields({1: (16, synth.le(3, 2)), 2: (8, 0), 3: (96, bytes(12))})
    assert wrpl.read_gunner(gun) == {"gun": 3, "f2": "00", "vector": [0.0, 0.0, 0.0]}
    recs = b"".join(struct.pack("<IfdQ", 8 + i, 0.0, -1.5, 77) for i in range(2))
    assert wrpl.read_part_list(bytes([2]) + recs)["records"] == [[8, 0.0, -1.5, 77], [9, 0.0, -1.5, 77]]
    assert wrpl.read_part_list(bytes([3]) + recs) is None
    assert wrpl.decode_unit_message(0xF031, eff)["effect"] == 4505
    assert wrpl.decode_unit_message(0x1234, eff) is None


def test_hit_outcomes_from_unit_on_hit():
    # 0xF144 as sent with a hit that got through, one that destroyed, and one that did not get through.
    assert wrpl.read_unit_on_hit(bytes.fromhex("07001e3b682d214920"))["flags"] == 0x21
    assert wrpl.hit_outcome(wrpl.read_unit_on_hit(bytes.fromhex("07001e193b40274920"))["flags"]) == "kill"
    assert wrpl.hit_outcome(0x21) == "penetration"
    assert wrpl.hit_outcome(0x23) == "critical"
    assert wrpl.hit_outcome(0x2B) == "critical"
    assert wrpl.hit_outcome(0x20) == "nonpenetration"
    assert wrpl.hit_outcome(0x00) == "splash"
    assert wrpl.hit_outcome(None) == ""


def test_shell_signature_and_calibre():
    from heat3d_ext_warthunder.convert import calibre_of

    # The rest of two 120 mm KE-W hits, the marker one byte apart, and a guided missile's without one.
    assert wrpl.shell_signature(bytes.fromhex("ba7fc000c8d336000002401a005fcff3816322400380")) == "02401a00"
    assert wrpl.shell_signature(bytes.fromhex("d74000106436000002401a005fcff3816322400380")) == "02401a00"
    assert wrpl.shell_signature(bytes.fromhex("dccfc020285b3621e06d4014621fcff7416326400380")) == ""
    assert calibre_of("120mm_ke_w") == 120
    assert calibre_of("12_7mm_m2_hb") == 12.7
    assert calibre_of("us_aim_120c_5") is None
