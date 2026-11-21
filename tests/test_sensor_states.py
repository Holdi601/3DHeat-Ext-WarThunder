"""
Sensor and sight states: the flight model's sensors and targets (every aircraft) and the players' cameras of a
server replay (0xF0CC). Synthetic data only, built to the layout wrpl documents.
"""

from __future__ import annotations

import math
import struct

import pytest
import synth
from synth import BitWriter, zigzag

from heat3d_ext_warthunder import convert, ecs, wrpl


def _contact_uid(uid: int) -> int:
    return 0xFFFF0000 | uid


def _contact_entity(index: int, generation: int) -> int:
    return index << 10 | generation


def _flight_with_sensors(uid: int, sensors: list[dict], targets: list[dict]) -> bytes:
    """One 2026-layout flight entry with the given sensors and targets (see wrpl.flight_sensors), then the list's end."""
    w = BitWriter()
    w.flag(True).uleb(uid)
    w.flag(False).flag(False).flag(False)
    w.flag(False).u32(0).flag(False).flag(False)
    w.raw(zigzag(0))  # no weapons
    w.f32(100.0).f32(2000.0).f32(-300.0).u32(0).u32(0).align()
    w.raw(bytes(7))
    w.raw(bytes([1])).flag(False).raw(bytes([7])).flag(False).raw(bytes(2))  # one engine, running
    w.raw(bytes([len(sensors)]))
    for s in sensors:
        w.flag(s.get("first", s["on"])).raw(bytes([s["kind"] << 4 | s["slot"]]))
        if s["kind"] == 1:
            w.flag(s["on"])
            if not s["on"]:
                continue
            w.u16(s["mode"]).f32(s["since"])
            for v in s["words"]:
                w.u16(v)
            if s["mode"] >= 0x8000:
                w.raw(bytes([s["modeByte"]]))
            w.flag(False)
        elif s["kind"] == 2:
            if not s["on"]:
                continue
            w.bits(1, 1).u16(s["word"])
            for v in (*s["point"], *s["velocity"], s["time"]):
                w.f32(v)
        contacts = s.get("contacts")
        w.flag(contacts is not None)
        if contacts is not None:
            w.bits(len(contacts), 6)
            for c in contacts:
                w.u32(c)
            w.bits(s.get("pick", wrpl.NO_PICK), 6)
    if sensors:
        w.raw(b"\x00")
    w.raw(b"\x00")  # no countermeasures
    w.bits(len(targets), 4)
    for t in targets:
        w.raw(bytes(t["id"])).flag(False)
        if "point" in t:
            w.flag(True)
            for v in t["point"]:
                w.f32(v)
            w.u16(0).u16(0).u16(0)
        else:
            w.flag(False)
            for v in (*t["direction"], 0.0, 0.0, 0.0):
                w.f32(v)
        w.f32(t.get("time", 1.0)).bits(0, 2).flag(False).bits(0, 1).flag(False).bits(0, 1).flag(False)
    w.flag(False).flag(False)  # no tails
    w.flag(True).uleb(wrpl.NO_UID)
    return w.bytes()


RADAR = {"kind": 1, "slot": 0, "on": True, "mode": 0x9850, "modeByte": 62, "since": 12.5, "words": [100, 7, 9],
         "contacts": [_contact_uid(161), _contact_entity(1614, 3), _contact_uid(168)], "pick": 2}
WARNER = {"kind": 1, "slot": 1, "on": True, "mode": 0x8000, "modeByte": 96, "since": 3.0, "words": [5, 0, 0],
          "contacts": [_contact_uid(116)]}
OFF = {"kind": 1, "slot": 2, "on": False}
POD = {"kind": 2, "slot": 3, "on": True, "word": 454, "point": (5553.0, 565.0, -5825.0),
       "velocity": (-7.5, -16.0, 33.0), "time": 277.0}
TARGETS = [{"id": (6, 0), "point": (4000.0, 900.0, 21000.0)}, {"id": (2, 7), "point": (120.0, 4.0, -80.0)},
           {"id": (3, 7), "direction": (0.6, 0.0, 0.8)}]


def _entry(sensors: list[dict], targets: list[dict]) -> tuple[int, bytes, int]:
    raw: list = []
    got, err = wrpl.read_flight(_flight_with_sensors(185, sensors, targets), "2026", raw)
    assert err is None and [g[0] for g in got] == [185]
    _, n, bits, phase = raw[0]
    return n, bits, phase


def test_sensor_contact_units_and_entities():
    assert wrpl.sensor_contact(_contact_uid(161)) == ("uid", 161)
    # A message's ext UID (index << 10 | generation) as the entity stream's eid (index | generation << 22).
    what, eid = wrpl.sensor_contact(_contact_entity(1614, 3))
    assert what == "eid" and eid & 0x3FFFFF == 1614 and eid >> 22 == 3


def test_flight_sensors_and_targets_read_whole():
    n, bits, phase = _entry([RADAR, WARNER, OFF, POD], TARGETS)
    fs = wrpl.flight_sensors(n, bits, "2026", phase)
    radar, warner, off, pod = fs["sensors"]
    assert (radar["kind"], radar["slot"], radar["on"], radar["mode"], radar["modeByte"]) == (1, 0, True, 0x9850, 62)
    assert radar["since"] == pytest.approx(12.5) and radar["words"] == [100, 7, 9]
    assert radar["contacts"] == RADAR["contacts"] and radar["pick"] == 2
    assert warner["pick"] == wrpl.NO_PICK and off == {"slot": 2, "kind": 1, "on": False}
    assert pod["on"] and pod["word"] == 454 and pod["point"] == pytest.approx(POD["point"])
    assert pod["velocity"] == pytest.approx(POD["velocity"]) and pod["time"] == pytest.approx(277.0)
    assert [t["id"] for t in fs["targets"]] == [(6, 0), (2, 7), (3, 7)]
    assert fs["targets"][0]["point"] == pytest.approx(TARGETS[0]["point"])
    assert fs["targets"][2]["direction"] == pytest.approx((0.6, 0.0, 0.8))
    # The rest of the entry still reads as before.
    assert wrpl.flight_extras(n, bits, "2026", phase)["engineStates"] == ["running"]
    # The 2025 layout has no sensors.
    assert wrpl.flight_sensors(n, bits, "2025", phase) is None


def test_sensor_columns():
    n, bits, phase = _entry([RADAR, WARNER, OFF, POD], TARGETS)
    eid = wrpl.sensor_contact(_contact_entity(1614, 3))[1]
    cols = convert._sensor_columns(wrpl.flight_sensors(n, bits, "2026", phase))
    assert cols["sensors"] == "d0+ d1+ d2- o3+"
    assert cols["sensorModes"] == "d0:9850/62 d1:8000/96"
    assert cols["sensorContacts"] == f"d0:161 w{eid:x} 168;d1:116"
    assert cols["sensorLocks"] == "d0:168"
    assert (cols["opticX"], cols["opticY"], cols["opticZ"]) == pytest.approx(POD["point"])
    assert (cols["lockX"], cols["lockY"], cols["lockZ"]) == pytest.approx(TARGETS[0]["point"])
    assert (cols["sightX"], cols["sightY"], cols["sightZ"]) == pytest.approx(TARGETS[1]["point"])


def test_no_sensors_no_columns():
    n, bits, phase = _entry([], [])
    assert convert._sensor_columns(wrpl.flight_sensors(n, bits, "2026", phase)) is None
    n, bits, phase = _entry([OFF], [])
    assert convert._sensor_columns(wrpl.flight_sensors(n, bits, "2026", phase)) == {"sensors": "d2-"}


def _unit_camera(mode: int, zoom: float, quat: tuple[float, ...] = (0.0, 0.0, 0.0, 1.0)) -> bytes:
    f = lambda *v: struct.pack(f"<{len(v)}f", *v)  # noqa: E731
    return synth.id_fields({1: (128, f(*quat)), 2: (96, f(4.6, 4.7, 6.8)), 3: (96, f(-0.56, -0.06, -0.82)),
                            4: (16, struct.pack("<H", mode)), 5: (32, f(zoom)), 6: (8, 0), 7: (16, b"\x01\x00")})


def test_unit_camera_and_views():
    c = wrpl.read_unit_camera(_unit_camera(39, 6.14))
    assert c["mode"] == 39 and c["zoom"] == pytest.approx(6.14) and c["look"] == pytest.approx((-0.56, -0.06, -0.82))
    assert wrpl.decode_unit_message(wrpl.UNIT_CAMERA, _unit_camera(29, 1.19))["mode"] == 29
    tank = ecs.Entity(5, "tank+player_unit", 0.0, comps={"uid": 42})
    msgs = [convert.UnitMessage(t, wrpl.UNIT_CAMERA, tank, _unit_camera(m, z))
            for t, m, z in ((10.0, 29, 1.19), (11.0, 39, 6.14), (11.5, 39, 18.64))]
    msgs.append(convert.UnitMessage(11.2, 0xF0BD, tank, b"\x00"))  # another message to the unit
    views, check = convert.unit_views(msgs)
    assert check["messages"] == 3 and check["units"] == 1
    assert check["modes"]["29"] == {"near1": 1} and check["modes"]["39"] == {"zoomed": 2}
    # Where the camera looks: its look vector (-0.56, -0.06, -0.82), as a compass heading and a pitch.
    look = (math.degrees(math.atan2(-0.56, -0.82)) % 360, math.degrees(math.asin(-0.06 / math.hypot(0.56, 0.06, 0.82))))
    assert convert._view_at(views[42], 10.5) == {"cameraMode": 29, "zoom": pytest.approx(1.19),
                                                 "viewYaw": pytest.approx(look[0], abs=1e-3),
                                                 "viewPitch": pytest.approx(look[1], abs=1e-3)}
    assert convert._view_at(views[42], 11.6)["zoom"] == pytest.approx(18.64)
    assert convert._view_at(views[42], 9.0) == {} and convert._view_at(views[42], 13.0) == {}
    assert check["withDirection"] == 3


def test_a_targeting_camera_looks_along_its_quaternion():
    # A drone's targeting camera (mode 21) turned 90 degrees right about the vertical, 30 down about its right axis:
    # it looks east and down, whatever look vector it was entered with.
    yaw = (0.0, math.sin(math.pi / 4), 0.0, math.cos(math.pi / 4))
    down = (math.sin(math.radians(15)), 0.0, 0.0, math.cos(math.radians(15)))
    x1, y1, z1, w1 = yaw
    x2, y2, z2, w2 = down
    q = (w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2, w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
         w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2, w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2)
    drone = ecs.Entity(6, "aircraft+player_unit", 0.0, comps={"uid": 77})
    views, _ = convert.unit_views([convert.UnitMessage(5.0, wrpl.UNIT_CAMERA, drone, _unit_camera(21, 3.17, q))])
    v = convert._view_at(views[77], 5.2)
    assert v["cameraMode"] == 21 and v["viewYaw"] == pytest.approx(90.0, abs=0.01)
    assert v["viewPitch"] == pytest.approx(-30.0, abs=0.01)


def test_new_columns_in_the_schema():
    names = [c for c, _ in convert.COLUMNS]
    for col in ("cameraMode", "sensors", "sensorModes", "sensorContacts", "sensorLocks", "opticX", "lockX", "sightZ"):
        assert col in names and col in convert.HINTS["columns"]["extra"]
