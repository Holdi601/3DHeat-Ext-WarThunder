"""Vehicle fires from the entity event that lists them, on a battle built in code."""

from __future__ import annotations

import struct

from heat3d_ext_warthunder import convert, ecs

TANK = 0x400101  # an entity id: index 0x101, generation 1


def fires_list(fires: list[tuple[int, int, int, int]], burning: bool = True) -> bytes:
    """The hashed event (class byte, LEB128 bit count, hash) listing these fires, as the server sends it."""
    bits = "1" if burning else "0"
    bits += f"{3 * len(fires):08b}"
    for first, node, kind, state in fires:
        bits += "".join(f"{b:08b}" for b in struct.pack("<HHIi", first, node, kind, state))
    n = 32 + len(bits)
    bits += "0" * (-len(bits) % 8)
    body = bytes(int(bits[i : i + 8], 2) for i in range(0, len(bits), 8))
    head = bytearray()
    v = n
    while True:
        head.append((v & 0x7F) | (0x80 if v > 0x7F else 0))
        v >>= 7
        if not v:
            break
    return b"\x82" + bytes(head) + convert.FIRES_EVENT + body


def lit(first: int, node: int, kind: int, x: float, y: float, z: float) -> bytes:
    """The message that lights a fire: its ids, a u16, its kind, -1, the hit, the point (z to the left)."""
    return (b"\x8e" + struct.pack("<HHHIi", first, node, 0x1BB, kind, -1) + bytes(6)
            + struct.pack("<fff", x, y, z))


def replay(messages: list[tuple[float, bytes]], died: float | None = None) -> tuple[convert.Replay, list]:
    r = convert.Replay([], {}, {}, {}, {}, [], [], [], 60_000, "")
    r.stream.entities.append(ecs.Entity(TANK, "tank+player_unit", 0.0, {"uid": 7}))
    r.stream.messages = [(t, TANK, m) for t, m in messages]
    life = convert.Life(7, "ground", 0, [convert.Sample(float(t), 100.0 + t, 5.0, 200.0) for t in range(0, 41)],
                        figure="tank", died=died)
    return r, [life]


def test_a_fire_from_its_start_to_when_it_is_out():
    r, lives = replay([
        (1.0, fires_list([])),
        (10.0, fires_list([(301, 969, 26, -1)])),
        (10.0, lit(301, 969, 26, 0.5, 1.4, -1.7)),
        (12.0, fires_list([(301, 969, 26, 0), (200, 858, 1, 1)])),
        (15.0, fires_list([(301, 969, 26, 0)])),
        (20.0, fires_list([], burning=True)),
        (20.05, fires_list([], burning=False)),
    ])
    rows, check = convert.fire_rows(r, lives)
    got = [(x["event"], x["time"], x["fireId"]) for x in rows]
    assert got == [("fire_on", 10.0, "301:969"), ("fire_on", 12.0, "200:858"),
                   ("fire_off", 15.0, "200:858"), ("fire_off", 20.0, "301:969")]
    first = rows[0]
    assert first["fireKind"] == 26 and first["track"] and abs(first["x"] - 110.0) < 1e-6
    # The point in the vehicle's frame, z turned to the right.
    assert (round(first["fireLocalX"], 3), round(first["fireLocalY"], 3), round(first["fireLocalZ"], 3)) == (0.5, 1.4, 1.7)
    assert "fireLocalX" not in rows[1]
    assert check["lists"] == 6 and check["listsNotRead"] == 0 and check["fires"] == 2 and check["firesWithPlace"] == 1


def test_a_wreck_burns_until_it_is_gone():
    r, lives = replay([(30.0, fires_list([(225, 938, 27, 2)]))], died=30.0)
    lives[0].samples = lives[0].samples[:36]
    rows, check = convert.fire_rows(r, lives)
    assert [(x["event"], x["time"]) for x in rows] == [("fire_on", 30.0), ("fire_off", 35.0)]
    assert check["endedWithWreck"] == 1 and check["burnedAfterDeath"] == 1


def test_a_fire_without_an_end_ends_with_the_replay():
    r, lives = replay([(5.0, fires_list([(1, 2, 3, 0)]))])
    rows, check = convert.fire_rows(r, lives)
    assert rows[-1]["event"] == "fire_off" and rows[-1]["time"] == 60.0 and check["burningAtEnd"] == 1


def test_a_list_that_does_not_read_is_counted():
    bad = fires_list([(1, 2, 3, 0)])[:-6]
    r, lives = replay([(5.0, bad)])
    rows, check = convert.fire_rows(r, lives)
    assert rows == [] and check["listsNotRead"] == 1
