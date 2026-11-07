"""The container and message readers, against payloads built to the documented layout (tests/synth.py)."""

from __future__ import annotations

import math

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
    assert first == [(177, 10.0, 150.0, -20.0), (180, 5.0, 1.0, 2.0)]
    # An unchanged state, sent as a difference to packet 7.
    again = g.read(synth.ground({177: (0, 0, 0)}, number=8, delta={177}))
    assert again == [(177, 10.0, 150.0, -20.0)]
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
