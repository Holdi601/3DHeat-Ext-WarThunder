"""
A replay as the 3DHeat viewer reads it: one Parquet table of every unit's
track, the weapons in flight and the kills, hits and launches where they
happened, and one match document with everything else the replay holds.

The table carries its reading instructions in the Parquet footer under
`heat3d` (see 3DHeat's docs/data-formats.md): positions in the game's metres,
x east, y up, z north - so Y is up and Z is mirrored, or north would be drawn
south - the time in seconds of the replay's clock, the player, the team, the
life (a unit's track from spawn to death), the look direction as a vector,
and `Vehicle`, the game's own vehicle id, which the viewer's figures match.

Who a track is comes from the replay's own records, never from a guess. The
entity stream (see ecs.py) creates every unit with its uid, vehicle, team and
player slot; a uid's samples belong to the unit last created with that uid.
Where a replay has no entity stream (older replays), kills and hits name the
uid, slot and vehicle of whoever dealt them, and the slots name the player.
"""

from __future__ import annotations

import bisect
import json
import math
import struct
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import ecs, names as vehicle_names, wrpl

#: Vehicle types in the results' crafts_info: which are aircraft, which helicopters, which boats.
AIR_TYPES = {"fighter", "assault", "bomber", "helicopter", "attack_helicopter", "utility_helicopter", "aircraft"}
HELI_TYPES = {"helicopter", "attack_helicopter", "utility_helicopter"}
BOAT_TYPES = {"boat", "gun_boat", "torpedo_boat", "torpedo_gun_boat", "submarine_chaser", "naval_ferry_barge", "minelayer"}
#: A track is also cut where its unit is not seen for this long (s).
GAP = {"air": 30.0, "ground": 60.0}
#: A track is cut where its unit moves further than this speed allows (m/s; a fighter's top speed is under 750
#: m/s, a fast boat's 30, a missile's under 1800) and further than the slack (m, the samples' own scatter): a respawn, a rearm, a
#: relocation, a client's correction.
TOP_SPEED = {"air": 750.0, "ground": 40.0, "weapon": 1800.0}
SLACK = {"air": 60.0, "ground": 8.0, "weapon": 40.0}
#: Samples after a unit's death are its wreck for at most this long (s), or until its entity is removed.
WRECK = 60.0
#: A projectile's launcher: the nearest unit within this distance (m) and time (s) of its release.
LAUNCHER_M, LAUNCHER_S = 300.0, 1.5

#: How the viewer reads the table; see the module docstring.
HINTS = {
    "version": 1,
    "kind": "warthunder-replay",
    "game": "War Thunder",
    "axes": {"up": "y", "flipX": False, "flipY": False, "flipZ": True, "scale": 1},
    # No "entity" size: the viewer reads it as the width of a person (0.8 m) and would scale metres by it.
    "columns": {
        "x": "x",
        "y": "y",
        "z": "z",
        "time": "time",
        "timeUnit": "seconds",
        "personId": "track",
        "teamId": "team",
        # One match per file: keeps two loaded replays' tracks apart and lets the viewer pick a match.
        "sessionId": "match",
        "lookMode": "vector",
        "dirX": "dirX",
        "dirY": "dirY",
        "dirZ": "dirZ",
        "extra": ["event", "player", "userId", "life", "Vehicle", "VehicleName", "VehicleShortName", "VehicleNameKey",
                  "kind", "type", "uid", "ai", "isPlayer", "other", "weapon", "weaponName", "heading", "pitch", "roll", "speed", "alive",
                  "mission", "match", "extrapolated", "moved", "xRaw", "yRaw", "zRaw", "headingRaw", "pitchRaw",
                  "rollRaw", "targetX", "targetY", "targetZ", "otherVehicle", "otherLife", "hitLocalX", "hitLocalY",
                  "hitLocalZ", "hitDirX", "hitDirY", "hitDirZ", "hitPart", "rpm", "vx", "vy", "vz", "engine", "afterburner",
                  "engineCondition", "ammo", "throttle", "elevator", "aileron", "rudder", "ias", "vario", "fuel",
                  "manifoldPressure", "gear", "oilTemperature", "headTemperature"],
    },
    # Not mapping hints, a statement of the angles' sense for whoever draws attitudes.
    "conventions": {"heading": "compass degrees, clockwise from north", "pitch": "degrees, nose up positive",
                    "roll": "degrees, right wing down positive (aircraft; checked against turns)"},
}

COLUMNS = [
    ("time", "f64"),
    ("event", "str"),
    ("track", "str"),
    ("player", "str"),
    ("userId", "str"),
    ("team", "str"),
    ("life", "str"),
    ("uid", "i16"),
    ("kind", "str"),
    ("type", "str"),
    ("Vehicle", "str"),
    ("VehicleName", "str"),
    ("VehicleShortName", "str"),
    ("VehicleNameKey", "str"),
    ("ai", "bool"),
    ("isPlayer", "bool"),
    ("match", "str"),
    ("x", "f32"),
    ("y", "f32"),
    ("z", "f32"),
    ("dirX", "f32"),
    ("dirY", "f32"),
    ("dirZ", "f32"),
    ("heading", "f32"),
    ("pitch", "f32"),
    ("roll", "f32"),
    ("speed", "f32"),
    ("alive", "f32"),
    ("other", "str"),
    ("weapon", "str"),
    ("weaponName", "str"),
    ("mission", "str"),
    ("extrapolated", "bool"),
    ("moved", "f32"),
    ("xRaw", "f32"),
    ("yRaw", "f32"),
    ("zRaw", "f32"),
    ("headingRaw", "f32"),
    ("pitchRaw", "f32"),
    ("rollRaw", "f32"),
    ("targetX", "f32"),
    ("targetY", "f32"),
    ("targetZ", "f32"),
    ("otherVehicle", "str"),
    ("otherLife", "str"),
    ("hitLocalX", "f32"),
    ("hitLocalY", "f32"),
    ("hitLocalZ", "f32"),
    ("hitDirX", "f32"),
    ("hitDirY", "f32"),
    ("hitDirZ", "f32"),
    ("hitPart", "f32"),
    ("rpm", "f32"),
    ("vx", "f32"),
    ("vy", "f32"),
    ("vz", "f32"),
    ("engine", "str"),
    ("afterburner", "f32"),
    ("engineCondition", "f32"),
    ("ammo", "str"),
    ("throttle", "f32"),
    ("elevator", "f32"),
    ("aileron", "f32"),
    ("rudder", "f32"),
    ("ias", "f32"),
    ("vario", "f32"),
    ("fuel", "f32"),
    ("manifoldPressure", "f32"),
    ("gear", "f32"),
    ("oilTemperature", "f32"),
    ("headTemperature", "f32"),
]


@dataclass
class Sample:
    t: float
    x: float
    y: float
    z: float
    attitude: int | None = None
    #: Ground units: compass heading, pitch, roll in degrees (None when the state does not say).
    angles: tuple[float | None, float | None, float | None] | None = None
    #: Ground units: the position came packed in 64 bits (its height may need the replay's offset).
    packed: bool = False
    #: The flight-model entry's uid (while frames are re-timed).
    uid: int = -1
    #: Given the time it stands for, not its packet's (see `_retime`).
    retimed: bool = False
    #: Its unit's own speed limit (m/s; see `_own_limit`).
    limit: float = 0.0
    #: The client's dead reckoning, not a state it received (see `_dead_reckoned`).
    extrapolated: bool = False
    #: Before `_smooth` moved it: the position, and the attitude as (heading, pitch, roll) degrees.
    raw: tuple[float, float, float] | None = None
    raw_angles: tuple[float, float, float] | None = None
    #: The attitude `_smooth` gave it, (heading, pitch, roll) degrees in the table's conventions.
    smooth_angles: tuple[float, float, float] | None = None
    #: How far `_smooth` moved it (m).
    moved: float = 0.0
    #: Aircraft: its flight-model entry, an index into `Replay.flight_raw` (-1: none).
    entry: int = -1


@dataclass
class Unit:
    """One unit entity of the entity stream."""

    entity: ecs.Entity
    uid: int
    domain: str  # "air" or "ground": the channel its positions come in
    vehicle: str
    kind: str
    type: str
    team: str
    pid: int | None
    mission: str

    @property
    def placeholder(self) -> bool:
        return self.vehicle == "dummy_plane"


@dataclass
class Life:
    uid: int
    kind: str
    n: int
    samples: list[Sample]
    pid: int | None = None
    vehicle: str = ""
    player: str = ""
    user_id: str = ""
    team: str = ""
    unit: Unit | None = None
    #: When it was killed (replay seconds); the samples after it, for a while, are its wreck.
    died: float | None = None
    #: The figure kind and the game's type ("fighter", "destroyer").
    figure: str = ""
    type: str = ""
    #: The fastest step this life can take (m/s; see `_own_limit`).
    limit: float = 0.0
    #: The vehicle's names in the game's own localisation (see names.py): full, short, the key.
    vehicle_name: str = ""
    vehicle_short: str = ""
    vehicle_key: str = ""

    @property
    def id(self) -> str:
        return f"{self.uid}#{self.n}"

    @property
    def is_player(self) -> bool:
        """Driven by a player: a slot with a Gaijin account id. Everything else (mission units, AI aircraft,
        ground targets, ships, AA guns, placeholders) is AI."""
        return bool(self.user_id)

    @property
    def display(self) -> str:
        """The vehicle as a person reads it: the game's English name, else its id."""
        return self.vehicle_name or (self.vehicle if self.vehicle != "dummy_plane" else "")

    @property
    def start(self) -> float:
        return self.samples[0].t

    @property
    def end(self) -> float:
        return self.samples[-1].t

    def wreck_until(self) -> float | None:
        if self.died is None:
            return None
        end = self.died + WRECK
        gone = self.unit.entity.destroyed if self.unit else None
        return min(end, gone) if gone is not None and gone > self.died else end


@dataclass
class Replay:
    """What was read from one battle's replay file(s)."""

    files: list[str]
    header: dict[str, Any]
    results: dict[str, Any]
    slots: dict[int, dict[str, Any]]
    tracks: dict[tuple[str, int], list[Sample]]
    kills: list[dict[str, Any]]
    hits: list[dict[str, Any]]
    chat: list[dict[str, Any]]
    end_ms: int
    layout: str
    problems: Counter = field(default_factory=Counter)
    packets: Counter = field(default_factory=Counter)
    settings: dict[str, Any] = field(default_factory=dict)
    stream: ecs.Stream = field(default_factory=ecs.Stream)
    #: eid index -> (t, x, y, z, group, guided) of a weapon in flight.
    shells: dict[int, list[tuple]] = field(default_factory=dict)
    explosions: list[dict[str, Any]] = field(default_factory=list)
    flak: list[dict[str, Any]] = field(default_factory=list)
    awards: list[dict[str, Any]] = field(default_factory=list)
    part_kills: list[dict[str, Any]] = field(default_factory=list)
    detections: list[dict[str, Any]] = field(default_factory=list)
    unit_states: list[dict[str, Any]] = field(default_factory=list)
    weather: list[dict[str, Any]] = field(default_factory=list)
    objects: dict[str, dict[str, Any]] = field(default_factory=dict)
    cockpit: list[tuple[float, dict[int, float]]] = field(default_factory=list)
    triggers: list[dict[str, Any]] = field(default_factory=list)
    hints: list[dict[str, Any]] = field(default_factory=list)
    progress: list[dict[str, Any]] = field(default_factory=list)
    camera: list[dict[str, Any]] = field(default_factory=list)
    #: Single aircraft samples ahead of their time, re-timed (see `_relead`).
    releaded: int = 0
    #: Where a track was cut because its unit moved faster than it can (see `lives`).
    breaks: list[dict[str, Any]] = field(default_factory=list)
    #: Flight-model packets whose aircraft were all ahead of the packet's time (see `_retime`).
    retimed: list[dict[str, Any]] = field(default_factory=list)
    #: The packed ground heights' offset measured on this replay (see `_packed_height`).
    packed_height: dict[str, Any] = field(default_factory=dict)
    #: Samples left out of the table, by why.
    dropped: Counter = field(default_factory=Counter)
    #: Every message id seen, by "type" or "type/0xid" ("4/unit/0xid" for messages to a unit), for the record.
    seen_ids: Counter = field(default_factory=Counter)
    #: Messages to units (see wrpl.read_mpi): (t, ext UID, message id, payload), resolved by `unit_messages`.
    unit_msgs: list[tuple[float, int, int, bytes]] = field(default_factory=list)
    #: Replicated objects (0xF02D, 0xF0AA): (t, message id, object id, ext UID or None, its fields, its body).
    reflection: list[tuple[float, int, int, int | None, dict[int, bytes], bytes]] = field(default_factory=list)
    #: Packets no reader here takes, kept whole for the messages sidecar: (t, packet type, message id or None, payload).
    raw: list[tuple[float, int, int | None, bytes]] = field(default_factory=list)
    #: Every flight-model entry whole: (t, uid, bit count, bits, the bit it started at in its first byte), for the flight sidecar (see `flight_table`).
    flight_raw: list[tuple[float, int, int, bytes, int]] = field(default_factory=list)
    #: `flight_raw` decoded (wrpl.flight_extras; None where an entry does not read), made by `flight_entries`.
    flight_x: list[dict[str, Any] | None] | None = None


def _decompress():
    try:
        import zstandard
    except ImportError:
        return None
    return lambda b: zstandard.ZstdDecompressor().stream_reader(b).read()


#: Readers of further game messages: id -> (reader, the Replay list it goes to).
_MORE = {
    wrpl.EXPLOSION: (wrpl.read_explosion, "explosions"),
    wrpl.FLAK: (wrpl.read_flak, "flak"),
    wrpl.STREAK: (wrpl.read_streak, "awards"),
    wrpl.PART_KILL: (wrpl.read_part_kill, "part_kills"),
    wrpl.DETECTED: (wrpl.read_detected, "detections"),
    wrpl.UNIT_STATE: (wrpl.read_unit_state, "unit_states"),
    wrpl.WEATHER: (wrpl.read_weather, "weather"),
    wrpl.TRIGGER: (wrpl.read_trigger, "triggers"),
    wrpl.HINT: (wrpl.read_trigger, "hints"),
    wrpl.PROGRESS[0]: (wrpl.read_fields_hex, "progress"),
    wrpl.PROGRESS[1]: (wrpl.read_fields_hex, "progress"),
    wrpl.CAMERA: (wrpl.read_camera, "camera"),
}


def _id_key(pk: wrpl.Packet) -> str:
    p = pk.payload
    if pk.type == 4 and pk.message is not None:
        return f"4/{pk.message:#06x}"
    if pk.type == 4 and len(p) >= 5 and p[0] == 0xFF:
        # Messages to a unit: the object id, the unit's entity (LEB128), the message id (see wrpl.read_mpi).
        try:
            return f"4/unit/{wrpl.read_mpi(p)[2]:#06x}"
        except (wrpl.FormatError, IndexError):
            return "4/unit/?"
    if pk.type == 6 and p:
        return f"6/{p[0]:#04x}"
    return str(pk.type)


def read(paths: list[Path]) -> Replay:
    """
    One battle from its file or, for a server replay, its parts (every file
    must be of the same session; they are read in part order).
    """
    parts = []
    for p in paths:
        buf = Path(p).read_bytes()
        parts.append((wrpl.read_header(buf), buf, str(p)))
    sessions = {(h["sessionId"], h["server"]) for h, _, _ in parts}
    if len(sessions) > 1:
        raise wrpl.FormatError(f"files of {len(sessions)} different battles; give one battle's files at a time")
    parts.sort(key=lambda t: t[0]["part"])
    header = dict(parts[0][0])
    r = Replay([p for _, _, p in parts], header, {}, {}, {}, [], [], [], 0, "")
    tracks: dict[tuple[str, int], list[Sample]] = defaultdict(list)
    frames: list[tuple[float, list[Sample]]] = []
    shells: dict[int, list[tuple]] = defaultdict(list)
    problems, seen = r.problems, r.packets
    ground = wrpl.GroundReader()
    unzstd = _decompress()
    if header.get("settingsSize"):
        try:
            r.settings = wrpl.read_settings(parts[0][1])
        except (wrpl.FormatError, IndexError, ValueError, struct.error):
            problems["settings"] += 1
    for h, buf, _ in parts:
        if 0 < h["resultsOffset"] < len(buf):
            try:
                r.results = wrpl.read_blk(buf[h["resultsOffset"] :]) or r.results
            except (wrpl.FormatError, IndexError, ValueError):
                problems["results"] += 1
        stream = list(wrpl.packets(wrpl.packet_stream(buf, h)))
        if not r.layout:
            flight = [p.payload for p in stream if p.type == 2][:80]
            r.layout = wrpl.flight_layout(flight) if flight else ""
        for pk in stream:
            r.end_ms = max(r.end_ms, pk.ms)
            r.seen_ids[_id_key(pk)] += 1
            t = pk.ms / 1000.0
            if pk.type == 2:
                seen["flight"] += 1
                whole: list = []
                entries, err = wrpl.read_flight(pk.payload, r.layout or "2026", whole)
                if err:
                    # A list that does not parse to its end is not trusted at all; it is kept whole.
                    problems["flight"] += 1
                    entries = []
                    r.raw.append((t, 2, None, pk.payload))
                else:
                    base = len(r.flight_raw)
                    r.flight_raw += [(t, *w) for w in whole]
                frames.append((t, [Sample(t, x, y, z, att, uid=uid, entry=base + i if not err else -1)
                                   for i, (uid, x, y, z, att) in enumerate(entries) if _plausible(x, y, z)]))
            elif pk.type == 3:
                try:
                    r.chat.append({"t": t, **wrpl.read_chat(pk.payload)})
                except wrpl.FormatError:
                    problems["chat"] += 1
            elif pk.type == 6:
                seen["entity"] += 1
                r.stream.feed(pk.payload, t)
                if pk.payload and pk.payload[0] not in (0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26):
                    r.raw.append((t, 6, pk.payload[0], pk.payload))
            elif pk.type == 4 and pk.payload[:1] == b"\xff":
                try:
                    _, ext, mid, at = wrpl.read_mpi(pk.payload)
                    seen["unit"] += 1
                    r.unit_msgs.append((t, ext, mid, pk.payload[at:]))
                except (wrpl.FormatError, IndexError):
                    problems["unit"] += 1
                    r.raw.append((t, 4, None, pk.payload))
            elif pk.type == 4:
                m = pk.message
                name = "hit"
                try:
                    if m == wrpl.KILL:
                        name = "kill"
                        seen["kill"] += 1
                        r.kills.append({"t": t, **wrpl.read_kill(pk.payload)})
                    elif m in (wrpl.CRITICAL, wrpl.SEVERE):
                        seen["hit"] += 1
                        r.hits.append({"t": t, "severity": "critical" if m == wrpl.CRITICAL else "severe",
                                       **wrpl.read_damage(pk.payload)})
                    elif m == wrpl.SLOTS:
                        name = "slots"
                        seen["slots"] += 1
                        for k, v in wrpl.read_slots(pk.payload, unzstd).items():
                            r.slots.setdefault(k, {}).update(v)
                        for oid, ext, body in wrpl.reflection_objects(pk.payload, unzstd):
                            r.reflection.append((t, m, oid, ext, wrpl.reflection_fields(body), body))
                    elif m == wrpl.REDUNDANT_SLOTS:
                        name = "redundant reflection"
                        seen["redundantReflection"] += 1
                        for oid, ext, body in wrpl.reflection_objects(pk.payload, unzstd, flagged=False):
                            r.reflection.append((t, m, oid, ext, wrpl.reflection_fields(body), body))
                    elif m in (wrpl.GROUND_CLIENT, wrpl.GROUND_SERVER):
                        name = "ground"
                        seen["ground"] += 1
                        for uid, x, y, z, hd, pt, rl, packed in ground.read(pk.payload):
                            if _plausible(x, y, z):
                                tracks[("ground", uid)].append(Sample(t, x, y, z, None, (hd, pt, rl), packed))
                    elif m in wrpl.SHELLS:
                        name = "shells"
                        seen["shells"] += 1
                        for group, idx, x, y, z, guided in wrpl.read_shells(pk.payload):
                            shells[idx].append((t, x, y, z, group, guided))
                    elif m == wrpl.COCKPIT:
                        name = "cockpit"
                        seen["cockpit"] += 1
                        r.cockpit.append((t, wrpl.read_cockpit(pk.payload)))
                    elif m == wrpl.OBJECTS:
                        name = "objects"
                        seen["objects"] += 1
                        for o in wrpl.read_objects(pk.payload):
                            r.objects.setdefault(o["name"], {"t": round(t, 3), **o})
                    elif m in _MORE:
                        reader, where = _MORE[m]
                        name = where
                        seen[where] += 1
                        v = reader(pk.payload)
                        if v is not None:
                            getattr(r, where).append({"t": round(t, 3), **v})
                        if m == wrpl.CAMERA:
                            r.raw.append((t, 4, m, pk.payload))  # the table thins the camera; the sidecar keeps all
                    else:
                        r.raw.append((t, 4, m, pk.payload))
                except (wrpl.FormatError, EOFError, IndexError, ValueError, struct.error):
                    problems[name] += 1
                    r.raw.append((t, 4, m, pk.payload))
            elif pk.type not in (0, 1):
                r.raw.append((t, pk.type, None, pk.payload))
    r.retimed = _retime(frames)
    for _, samples in frames:
        for smp in samples:
            tracks[("air", smp.uid)].append(smp)
    r.tracks = dict(tracks)
    r.shells = dict(shells)
    r.packed_height = _packed_height(r)
    for k, v in r.stream.problems.items():
        problems[f"entity {k}"] += v
    return r


#: A flight-model packet is re-timed when at least this many moving aircraft are in it, ...
RETIME_MIN_AIRCRAFT = 5
#: ... their median lead over the packet's time is at least this (s), ...
RETIME_MIN_SHIFT = 0.3
#: ... and this share of them agree on it within 0.25 s.
RETIME_AGREE = 0.7


def _retime(frames: list[tuple[float, list[Sample]]]) -> list[dict[str, Any]]:
    """
    Now and then a client replay's flight-model packet holds every aircraft
    where it will be about 0.75 s later - all of them, by the same lead -
    and the next packet is back on time: the client wrote its extrapolated
    state after a network hitch. Read at the packet's time, each aircraft
    jumps forward and back (several thousand km/h). The lead is measured per
    packet: each aircraft's step from its last two on-time samples, along its
    velocity, against the time elapsed; when most moving aircraft agree, each
    aircraft that leads by that much is given the time it stands for (the
    recording player's own aircraft does not lead and keeps its time). The packet's own
    bytes do not say it (its entries and its tail are as usual); see the
    README. Returns the packets re-timed.
    """
    last: dict[int, list[Sample]] = {}
    out = []
    for t, samples in frames:
        leads: dict[int, float] = {}
        for smp in samples:
            hist = last.get(smp.uid)
            if not hist or len(hist) < 2:
                continue
            a, b = hist[-2], hist[-1]
            dt = b.t - a.t
            if not 0 < dt <= 1.5 or not 0 < t - b.t <= 1.5:
                continue
            v = ((b.x - a.x) / dt, (b.y - a.y) / dt, (b.z - a.z) / dt)
            vv = v[0] * v[0] + v[1] * v[1] + v[2] * v[2]
            if vv < 80.0 ** 2:
                continue
            step = (smp.x - b.x) * v[0] + (smp.y - b.y) * v[1] + (smp.z - b.z) * v[2]
            leads[id(smp)] = step / vv - (t - b.t)
        mid = 0.0
        if len(leads) >= RETIME_MIN_AIRCRAFT:
            ordered = sorted(leads.values())
            mid = ordered[len(ordered) // 2]
            agree = sum(1 for x in ordered if abs(x - mid) <= 0.25) / len(ordered)
            if mid >= RETIME_MIN_SHIFT and agree >= RETIME_AGREE:
                moved = 0
                for smp in samples:
                    # The recording player's own aircraft is not extrapolated: only those that lead are moved.
                    lead = leads.get(id(smp))
                    if lead is not None and abs(lead - mid) <= 0.25:
                        smp.t = t + lead
                        smp.retimed = True
                        moved += 1
                out.append({"time": round(t, 3), "lead": round(mid, 3), "aircraft": len(leads),
                            "agree": round(agree, 2), "moved": moved})
            else:
                mid = 0.0
        for smp in samples:
            if smp.t != t:
                continue
            # Only on-time samples are the reference for the next packets.
            hist = last.setdefault(smp.uid, [])
            hist.append(smp)
            if len(hist) > 2:
                del hist[0]
    return out


def _packed_height(r: Replay) -> dict[str, Any]:
    """
    Ground positions come as floats or packed in 64 bits; the packed height
    counts from -100 m on most levels but from higher up on a level whose
    ground lies high (air_afghan: 1505 m higher, its water level). The offset is measured on
    the replay's own data - a unit's float sample and its packed one under
    12 s apart, and a unit's creation point (entity stream) against its first
    packed sample within 15 s - and added to every packed height when at
    least three agree on more than 5 m (their median; the spread is kept).
    """
    deltas: list[float] = []
    for (kind, uid), samples in r.tracks.items():
        if kind != "ground":
            continue
        for a, b in zip(samples, samples[1:]):
            if a.packed != b.packed and abs(b.t - a.t) < 12:
                f, p = (a, b) if b.packed else (b, a)
                if math.hypot(f.x - p.x, f.z - p.z) < 300:
                    deltas.append(f.y - p.y)
    for e in r.stream.entities:
        tm = e.comps.get("transform")
        if e.uid is None or not isinstance(tm, dict) or e.template.startswith(("aircraft", "sync")):
            continue
        for s in r.tracks.get(("ground", e.uid), []):
            if s.t >= e.t - 0.1:
                if s.packed and s.t - e.t < 15 and math.hypot(tm["pos"][0] - s.x, tm["pos"][2] - s.z) < 300:
                    deltas.append(tm["pos"][1] - s.y)
                break
    out: dict[str, Any] = {"pairs": len(deltas), "applied": 0.0}
    if len(deltas) >= 3:
        deltas.sort()
        mid = deltas[len(deltas) // 2]
        out["median"] = round(mid, 2)
        out["spread"] = round(deltas[int(len(deltas) * 0.9)] - deltas[int(len(deltas) * 0.1)], 2)
        if abs(mid) > 5:
            out["applied"] = round(mid, 2)
            for (kind, _), samples in r.tracks.items():
                if kind == "ground":
                    for s in samples:
                        if s.packed:
                            s.y += mid
    return out


def _plausible(x: float, y: float, z: float) -> bool:
    return all(math.isfinite(v) for v in (x, y, z)) and abs(x) < 200_000 and abs(z) < 200_000 and -1000 < y < 40_000


# ---------------------------------------------------------------- units: what each uid was


def craft_types(r: Replay) -> dict[str, str]:
    """Every vehicle in any player's line-up, with the game's type for it (fighter, destroyer, gun_boat...)."""
    ui = (r.results.get("uiScriptsData") or {}).get("playersInfo") or {}
    out: dict[str, str] = {}
    if not isinstance(ui, dict):
        return out
    for p in ui.values():
        if not isinstance(p, dict):
            continue
        crafts = p.get("crafts") if isinstance(p.get("crafts"), dict) else {}
        info = p.get("crafts_info") if isinstance(p.get("crafts_info"), dict) else {}
        for v in info.values():
            if isinstance(v, dict):
                name = v.get("name") or crafts.get(str(v.get("slot")))
                if name and v.get("type"):
                    out[str(name)] = str(v["type"])
    return out


_AA = ("flak", "zsu", "spaa", "gepard", "_aa", "aa_", "tunguska", "pantsir", "shilka", "strela", "m163", "m247",
       "m42", "m16_", "chaparral", "roland", "crotale", "ito_", "vulcan", "bofors", "tor_m", "osa", "zu_23",
       "skyguard", "stormer", "adats", "type_87", "type_81", "lvkv", "wirbelwind", "ostwind", "kugelblitz",
       "sidam", "otomatic", "falcon", "pvkv", "_sam", "sam_", "gun_25mm", "ystervark")
_BOATS = ("boat", "_pr_", "mtb", "_pt_", "pt_", "s_boot", "schnellboot", "lcs", "barge", "_mpk", "mkl_", "bmo",
          "vlt", "rboot", "fahrprahm", "lcm", "mgb", "mas_", "tka_", "_tk_")
_HELIS = ("ah_", "uh_", "mi_", "ka_", "sa_341", "sa_342", "bo_105", "tiger", "mangusta", "rooivalk", "lynx",
          "wz_", "z_9", "z_10", "z_19", "oh_", "ah1", "ah64", "heli")


def classify(template: str, class_name: str, types: dict[str, str]) -> tuple[str, str, str, str]:
    """(domain, kind, type, vehicle): the channel its positions come in, the figure kind, the game's type, the id."""
    path, _, vehicle = class_name.rpartition("/")
    path = path.lower()
    low = vehicle.lower()
    t = types.get(vehicle, "")
    base = template.split("+", 1)[0]
    if base == "aircraft" or base == "helicopter":
        if t in HELI_TYPES or base == "helicopter" or (not t and low.startswith(_HELIS)):
            return "air", "helicopter", t or "helicopter", vehicle
        return "air", "aircraft", t or "aircraft", vehicle
    if base == "ship" or path == "ships":
        boat = t in BOAT_TYPES or (not t and any(k in low for k in _BOATS))
        return "ground", "boat" if boat else "ship", t or ("boat" if boat else "ship"), vehicle
    if path == "structures" and "radar" in low:
        return "ground", "structure", "radar", vehicle
    if path == "air_defence" or t == "spaa" or (not t and any(k in low for k in _AA)):
        return "ground", "spaa", t or "spaa", vehicle
    if base in ("tank", "light_vehicle") or path == "tankmodels":
        if "truck" in low or "jeep" in low or "car_" in low:
            return "ground", "truck", t or "truck", vehicle
        if not t and ("_apc" in low or "btr_" in low or "m113" in low):
            return "ground", "apc", "apc", vehicle
        return "ground", "tank", t or ("tank" if base == "tank" else "vehicle"), vehicle
    if base == "fortification" or path == "structures":
        return "ground", "structure", "structure", vehicle
    return "ground", "ground", t or base, vehicle


def units(r: Replay) -> list[Unit]:
    """Every unit entity with a uid, in creation order."""
    types = craft_types(r)
    out = []
    for e in r.stream.entities:
        uid = e.uid
        if uid is None or e.template.startswith("sync_player"):
            continue
        domain, kind, typ, vehicle = classify(e.template, e.class_name, types)
        team = e.comps.get("team")
        pid = e.comps.get("unit__playerId")
        out.append(Unit(e, uid, domain, vehicle, kind, typ, str(team) if isinstance(team, int) and team > 0 else "",
                        pid if isinstance(pid, int) and 0 <= pid < 0x7FF else None, e.comps.get("unit__missionName") or ""))
    return out


# ---------------------------------------------------------------- lives and who


def lives(r: Replay, all_units: list[Unit] | None = None) -> list[Life]:
    """
    Every uid's samples, given to the unit entity last created with that uid
    before them (when the replay has an entity stream), and cut into lives
    where the unit changes, jumps further than it could move (a respawn) or is
    not seen for long. A kill does not cut: the game goes on sending the wreck
    as it falls or sinks, and those samples stay in the life, after `died`. A
    life of one sample - a unit seen once where it spawned, then moved - is dropped.
    """
    if all_units is None:
        all_units = units(r)
    by_uid: dict[tuple[str, int], list[Unit]] = defaultdict(list)
    for u in all_units:
        by_uid[(u.domain, u.uid)].append(u)
    deaths: dict[int, list[float]] = defaultdict(list)
    for k in r.kills:
        if k.get("victimUid", wrpl.NO_UID) != wrpl.NO_UID:
            deaths[k["victimUid"]].append(k["t"])
    # When a uid deals a kill or a hit after it died, it is a new unit by then.
    acts: dict[int, list[float]] = defaultdict(list)
    for k in r.kills:
        acts[k.get("killerUid", wrpl.NO_UID)].append(k["t"])
    for h in r.hits:
        acts[h.get("uid", wrpl.NO_UID)].append(h["t"])
    out: list[Life] = []
    numbered: dict[int, int] = {}
    for (kind, uid), samples in sorted(r.tracks.items()):
        samples = sorted(samples, key=lambda s: s.t)
        cands = by_uid.get((kind, uid), [])
        starts = [u.entity.t for u in cands]

        def owner(t: float) -> Unit | None:
            i = bisect.bisect_right(starts, t + 0.5)
            for j in range(i - 1, -1, -1):
                if not cands[j].placeholder:
                    return cands[j]
            return cands[i - 1] if i else None

        if kind == "air":
            samples = _relead(samples, r)
            # A step out of the client's dead reckoning is measured from the last state it received (see `_from`).
            for q, e in zip(samples, _dead_reckoned(samples)):
                q.extrapolated = e
        runs: list[tuple[Unit | None, list[Sample]]] = []
        for s in samples:
            u = owner(s.t)
            if runs and runs[-1][0] is u:
                p = _from(runs[-1][1], s)
                dt = s.t - p.t
                d = math.dist((p.x, p.y, p.z), (s.x, s.y, s.z))
                if dt <= GAP[kind] and d <= max(SLACK[kind], TOP_SPEED[kind] * dt):
                    runs[-1][1].append(s)
                    continue
                if dt <= GAP[kind]:
                    r.breaks.append({"uid": uid, "kind": kind, "time": round(s.t, 3), "from": [round(p.x), round(p.y), round(p.z)],
                                     "to": [round(s.x), round(s.y), round(s.z)], "distance": round(d),
                                     "seconds": round(dt, 3)})
            runs.append((u, [s]))
        # A slow unit is held to its own pace: a piston fighter's client correction is no faster than a jet. The
        # pace is the unit's (all its samples under one entity), so every piece of it is held to the same.
        pace: dict[int, float] = {}
        for u, run in runs:
            pace.setdefault(id(u), 0.0)
        for key in pace:
            pace[key] = _own_limit([q for u, run in runs if id(u) == key for q in run], kind)
        runs = [(u, piece) for u, run in runs for piece in _split_own(run, kind, uid, r, pace[id(u)])]
        # Lives are numbered per uid across both channels: a uid can come as an aircraft and as a ground unit.
        n = numbered.get(uid, 0)
        while runs:
            u, run = runs.pop(0)
            if len(run) < 2:
                continue
            # Killed while this run was seen, or within a moment of its last sample.
            died = min((t for t in deaths.get(uid, []) if run[0].t <= t <= run[-1].t + 1.0), default=None)
            # Without an entity stream a uid acting after its death is a new unit by then. With one, the entity
            # says who it is, and an act after a death is a weapon that was already on its way (a missile
            # launched before the pilot was shot down still scores).
            if u is None and died is not None and any(died + 1.0 < t <= run[-1].t + 2.0 for t in acts.get(uid, [])):
                runs.insert(0, (u, [q for q in run if q.t > died]))
                run = [q for q in run if q.t <= died]
                if len(run) < 2:
                    continue
            n += 1
            if died is not None and kind == "ground":
                # A sunk ship or a burnt-out tank is sent on for minutes (a ship sinking 90 m): its wreck is kept
                # for WRECK seconds, the rest is dropped (counted). Aircraft are kept: a few AI aircraft fly on
                # after a kill record names them, and a falling wreck lands within a minute anyway.
                keep = [q for q in run if q.t <= died + WRECK]
                r.dropped["ground wreck after 60 s"] += len(run) - len(keep)
                run = keep
            life = Life(uid, kind, n, run, unit=u)
            life.died = died
            life.limit = run[0].limit or TOP_SPEED[kind]
            out.append(life)
        numbered[uid] = n
    return out


#: A life's own speed limit: this many times its own 95th-percentile step speed, ...
OWN_FACTOR = 1.6
#: ... within these bounds (m/s; a piston fighter's dive is under 250 m/s, a jet's top speed under 750).
OWN_BOUNDS = {"air": (250.0, 750.0), "ground": (15.0, 40.0)}


def _step_list(samples: list[Sample]) -> list[float]:
    """Speeds of the steps 0.2 to 5 s long (shorter ones are timing jitter, longer ones gaps)."""
    out = []
    for a, b in zip(samples, samples[1:]):
        dt = b.t - a.t
        if 0.2 <= dt <= 5.0:
            out.append(math.dist((a.x, a.y, a.z), (b.x, b.y, b.z)) / dt)
    return out


def _own_limit(samples: list[Sample], kind: str) -> float:
    """
    How fast this unit can go: 1.6 times its own 95th-percentile step speed,
    no less than a piston fighter's dive (250 m/s) or a tank's 15 m/s, no
    more than the kind's top speed. Checked on the recording player's own
    aircraft, which the client does not extrapolate: this limit cuts it
    nowhere in the four replays (see the README).
    """
    lo, hi = OWN_BOUNDS[kind]
    v = sorted(_step_list(samples))
    if len(v) < 20:
        return hi
    return max(lo, min(hi, OWN_FACTOR * v[int(len(v) * 0.95)]))


def _from(run: list[Sample], s: Sample) -> Sample:
    """
    The sample a step to `s` is measured from: the run's last sample, or, when
    that is the client's dead reckoning and `s` is not, the last state the
    client received before it. A distant aircraft flown on straight for a
    while and then snapped to its next update has not moved faster than it
    can: received state to received state, its pace is its own (on the air
    arcade battle this keeps hundreds of players' tracks whole that were cut
    at each correction).
    """
    p = run[-1]
    if not p.extrapolated or s.extrapolated or len(run) < 2:
        return p
    # Only a correction: s is no further than DR_SNAP from where the dead reckoning would have had it.
    o = run[-2]
    f = (s.t - p.t) / (p.t - o.t) if p.t > o.t else 0.0
    ahead = (p.x + (p.x - o.x) * f, p.y + (p.y - o.y) * f, p.z + (p.z - o.z) * f)
    if math.dist(ahead, (s.x, s.y, s.z)) > DR_SNAP:
        return p
    for q in reversed(run):
        if not q.extrapolated:
            return q
    return p


#: The largest correction of a dead-reckoned aircraft taken as one (m): on the air arcade battle the client's snaps
#: are 6 m at the median, 40 m at the 90th and 75 m at the 99th percentile; a respawn moves kilometres.
DR_SNAP = 300.0


def _split_own(run: list[Sample], kind: str, uid: int, r: Replay, limit: float) -> list[list[Sample]]:
    """A run cut again where it steps faster than its unit's own limit (`_own_limit`); the cuts go to `r.breaks`."""
    if len(run) < 2:
        return [run]
    for s in run:
        s.limit = limit
    pieces: list[list[Sample]] = [[run[0]]]
    for s in run[1:]:
        p = _from(pieces[-1], s)
        dt = s.t - p.t
        d = math.dist((p.x, p.y, p.z), (s.x, s.y, s.z))
        if d > max(SLACK[kind], limit * dt):
            r.breaks.append({"uid": uid, "kind": kind, "time": round(s.t, 3), "from": [round(p.x), round(p.y), round(p.z)],
                             "to": [round(s.x), round(s.y), round(s.z)], "distance": round(d), "seconds": round(dt, 3),
                             "limit": round(limit)})
            pieces.append([])
        pieces[-1].append(s)
    return pieces


def _relead(samples: list[Sample], r: Replay) -> list[Sample]:
    """
    One aircraft's sample now and then leads its track like a whole packet
    does (see `_retime`), or lags it (a state that came late: on the air
    arcade battle single samples 0.4 s behind, 30 m back along the path): it
    lies ahead or behind along the flight path by 0.3 s or more, and the next
    sample carries on from the one before it. Such a
    sample is given the time it stands for, as `_retime` does for packets.
    """
    out = list(samples)
    for i in range(2, len(out) - 1):
        a, b, c, nxt = out[i - 2], out[i - 1], out[i], out[i + 1]
        dt = b.t - a.t
        if not 0 < dt <= 1.5 or not 0 < c.t - b.t <= 1.5:
            continue
        v = ((b.x - a.x) / dt, (b.y - a.y) / dt, (b.z - a.z) / dt)
        vv = v[0] * v[0] + v[1] * v[1] + v[2] * v[2]
        if vv < 80.0 ** 2:
            continue
        step = (c.x - b.x, c.y - b.y, c.z - b.z)
        lead = (step[0] * v[0] + step[1] * v[1] + step[2] * v[2]) / vv - (c.t - b.t)
        if abs(lead) < RETIME_MIN_SHIFT:
            continue  # on time (a lag of 0.3 s or more is a late state, re-timed the same way)
        along = [v[k] * (c.t - b.t + lead) for k in range(3)]
        off = math.dist(step, along)
        # The next sample carries on from b (where b would be by then), not from c.
        span = nxt.t - b.t
        ahead = (b.x + v[0] * span, b.y + v[1] * span, b.z + v[2] * span)
        on_from_b = math.dist(ahead, (nxt.x, nxt.y, nxt.z)) <= 30.0 + 0.3 * math.sqrt(vv) * span
        if off <= 150 and on_from_b:
            c.t += lead
            c.retimed = True
            r.releaded += 1
    return _no_twins(out, r)


def _no_twins(samples: list[Sample], r: Replay) -> list[Sample]:
    """
    A sample given its own time (see `_retime`, `_relead`) can land within a
    moment of the sample the game sent for that time: the same moment twice,
    a few metres apart, reads as a burst of speed. The re-timed one is left out.
    """
    samples.sort(key=lambda q: q.t)
    out: list[Sample] = []
    for smp in samples:
        if out and smp.t - out[-1].t < 0.2 and (smp.retimed or out[-1].retimed):
            if out[-1].retimed and not smp.retimed:
                out[-1] = smp
            r.dropped["re-timed sample within 0.2 s of another"] += 1
            continue
        out.append(smp)
    return out


# ---------------------------------------------------------------- dead reckoning and the smoother

#: A flight sample is the client's dead reckoning when it continues the straight line of the two samples before it,
#: at their pace, to within this (m): float32 positions of a map's size are exact to a few millimetres. The recording
#: player's own aircraft, which the client does not extrapolate, comes this close in 0.2 to 4 % of its samples (steady
#: straight flight, where moving them would change nothing); other aircraft in up to 55 %.
DR_TOLERANCE = 0.03
#: Between two received samples at most this far apart (s), the samples in between are put on a cubic through both
#: (positions and velocities); further apart, the extrapolated line is only bent over towards the next received one.
DR_CUBIC = 3.0
#: The smoother: a quadratic in time fitted over this many samples each side of a received sample ...
SMOOTH_HALF = 2
#: ... moves it to the fit, but by no more than max(SMOOTH_MIN m, SMOOTH_SECONDS * its speed) - about the scatter of
#: the received samples (along the track 2.8 m, across 4.5 m at the 90th percentile in the air arcade battle).
SMOOTH_MIN, SMOOTH_SECONDS = 2.0, 0.04


def _dead_reckoned(samples: list[Sample]) -> list[bool]:
    """
    Which samples of one track are the client's dead reckoning rather than a
    state it received. A client replay records every aircraft at the client's
    0.25 s ticks; between the updates it gets for a distant aircraft, the
    client moves it on along its last velocity and turns it on at its last
    rates (an aircraft rolling at 128 deg/s keeps rolling for as long as no
    update comes) and, when the next update comes, snaps it there. Such a
    sample lies on the straight line of the two before it, at their pace,
    exactly: c = b + (b - a) * dt_bc / dt_ab within `DR_TOLERANCE`. Both b
    and c of such a triple are dead reckoning; a, where the run starts, is the
    received state. Nothing in the flight entry marks it (every field and bit
    of the entries was tested against this), so it is found this way.
    """
    out = [False] * len(samples)
    for i in range(2, len(samples)):
        a, b, c = samples[i - 2], samples[i - 1], samples[i]
        d1, d2 = b.t - a.t, c.t - b.t
        if d1 <= 0 or not 0 < d2 <= 1.5:
            continue
        if math.dist((b.x, b.y, b.z), (c.x, c.y, c.z)) < 0.5:
            continue  # standing still is no evidence
        f = d2 / d1
        timed = math.dist((b.x + (b.x - a.x) * f, b.y + (b.y - a.y) * f, b.z + (b.z - a.z) * f), (c.x, c.y, c.z))
        even = math.dist((2 * b.x - a.x, 2 * b.y - a.y, 2 * b.z - a.z), (c.x, c.y, c.z))
        if min(timed, even) < DR_TOLERANCE:
            out[i] = out[i - 1] = True
    return out


def _quat(h: float, p: float, r: float) -> tuple[float, float, float, float]:
    """(heading, pitch, roll) degrees in the table's conventions as a quaternion (w, x, y, z) in east-north-up axes."""

    def axis(ax: int, ang: float) -> tuple[float, float, float, float]:
        s, c = math.sin(ang / 2), math.cos(ang / 2)
        return c, s if ax == 0 else 0.0, s if ax == 1 else 0.0, s if ax == 2 else 0.0

    return _qmul(_qmul(axis(2, -math.radians(h)), axis(0, math.radians(p))), axis(1, math.radians(r)))


def _qmul(a: tuple, b: tuple) -> tuple[float, float, float, float]:
    aw, ax, ay, az = a
    bw, bx, by, bz = b
    return (aw * bw - ax * bx - ay * by - az * bz, aw * bx + ax * bw + ay * bz - az * by,
            aw * by - ax * bz + ay * bw + az * bx, aw * bz + ax * by - ay * bx + az * bw)


def _from_quat(q: tuple) -> tuple[float, float, float]:
    """A quaternion of `_quat` back to (heading, pitch, roll) degrees."""
    w, x, y, z = q
    # The turned body axes: forward (+y before turning), and the up components of right (+x) and up (+z).
    fx, fy, fz = 2 * (x * y - w * z), 1 - 2 * (x * x + z * z), 2 * (y * z + w * x)
    rz = 2 * (x * z - w * y)
    uz = 1 - 2 * (x * x + y * y)
    return (math.degrees(math.atan2(fx, fy)) % 360, math.degrees(math.asin(max(-1.0, min(1.0, fz)))),
            math.degrees(math.atan2(-rz, uz)))


def _slerp(a: tuple, b: tuple, f: float) -> tuple:
    dot = sum(x * y for x, y in zip(a, b))
    if dot < 0:
        b, dot = tuple(-x for x in b), -dot
    if dot > 0.9995:
        q = tuple(x + (y - x) * f for x, y in zip(a, b))
    else:
        th = math.acos(dot)
        sa, sb = math.sin((1 - f) * th) / math.sin(th), math.sin(f * th) / math.sin(th)
        q = tuple(x * sa + y * sb for x, y in zip(a, b))
    n = math.sqrt(sum(x * x for x in q))
    return tuple(x / n for x in q)


def _hermite(p0: tuple, v0: tuple, p1: tuple, v1: tuple, t0: float, t1: float, t: float) -> tuple:
    h = t1 - t0
    s = (t - t0) / h
    a, b, c, d = 2 * s ** 3 - 3 * s ** 2 + 1, s ** 3 - 2 * s ** 2 + s, -2 * s ** 3 + 3 * s ** 2, s ** 3 - s ** 2
    return tuple(a * p0[k] + b * h * v0[k] + c * p1[k] + d * h * v1[k] for k in range(3))


def _smooth(life: Life, move: bool) -> None:
    """
    Marks the dead-reckoned samples of an aircraft's track (`_dead_reckoned`)
    and, with `move`, puts the track where the received states say it was:

    * a dead-reckoned sample between two received ones goes on a cubic through
      both, with each one's own velocity (a received state's velocity is the
      pace of the dead reckoning that follows it; else that of the received
      samples around it). Over more than `DR_CUBIC` seconds the extrapolated
      line is bent over to the next received sample instead, by the snap the
      client made there, so no sample moves further than that snap. Its
      attitude is turned evenly (slerp) from the one received attitude to the
      next, instead of the client's constant-rate spin; after the last
      received sample of the track the attitude is held.
    * a received sample is moved to a quadratic in time fitted over
      `SMOOTH_HALF` samples each side, by at most `SMOOTH_MIN` m or
      `SMOOTH_SECONDS` of its speed: received states come with a few metres of
      scatter (along the track: the time the client got them, not when they
      were true). A quadratic keeps a steady turn or pull-up as it is.

    The samples keep what the replay said in `raw` / `raw_angles`; `moved` is
    how far each went.
    """
    ss = life.samples
    n = len(ss)
    ext = _dead_reckoned(ss)
    for s, e in zip(ss, ext):
        s.extrapolated = e
    if not move:
        return
    pos = [(s.x, s.y, s.z) for s in ss]
    ang = [_angles(s) for s in ss]
    rec = [i for i in range(n) if not ext[i]]

    def velocity(j: int) -> tuple | None:
        i = rec[j]
        if i + 1 < n and ext[i + 1] and ss[i + 1].t > ss[i].t:
            dt = ss[i + 1].t - ss[i].t
            return tuple((pos[i + 1][k] - pos[i][k]) / dt for k in range(3))
        a = rec[j - 1] if j > 0 else i
        b = rec[j + 1] if j + 1 < len(rec) else i
        dt = ss[b].t - ss[a].t
        return tuple((pos[b][k] - pos[a][k]) / dt for k in range(3)) if 0 < dt <= DR_CUBIC else None

    new = list(pos)
    att: list[tuple | None] = [None] * n
    for j, a in enumerate(rec):
        b = rec[j + 1] if j + 1 < len(rec) else n
        if b - a < 2:
            continue
        inside = range(a + 1, b)
        if b == n:
            # Dead reckoning to the track's end: nothing received to go to; only the spin is stopped.
            for i in inside:
                att[i] = ang[a]
            continue
        t0, t1 = ss[a].t, ss[b].t
        va, vb = velocity(j), velocity(j + 1)
        if va is not None and vb is not None and t1 - t0 <= DR_CUBIC:
            for i in inside:
                new[i] = _hermite(pos[a], va, pos[b], vb, t0, t1, ss[i].t)
        elif va is not None:
            snap = tuple(pos[b][k] - (pos[a][k] + va[k] * (t1 - t0)) for k in range(3))
            for i in inside:
                f = (ss[i].t - t0) / (t1 - t0)
                f = f * f * (3 - 2 * f)
                new[i] = tuple(pos[a][k] + va[k] * (ss[i].t - t0) + snap[k] * f for k in range(3))
        if ang[a] is not None and ang[b] is not None:
            qa, qb = _quat(*ang[a]), _quat(*ang[b])
            for i in inside:
                att[i] = _from_quat(_slerp(qa, qb, (ss[i].t - t0) / (t1 - t0)))
    for i, s in enumerate(ss):
        if new[i] != pos[i] or att[i] is not None:
            s.raw, s.raw_angles = pos[i], ang[i]
            s.x, s.y, s.z = new[i]
            s.moved = math.dist(pos[i], new[i])
            s.smooth_angles = att[i]
    _fit_received(ss, ext)


def _fit_received(ss: list[Sample], ext: list[bool]) -> None:
    """The second step of `_smooth`: each received sample to a local quadratic, within its scatter."""
    n = len(ss)
    pos = [(s.x, s.y, s.z) for s in ss]
    reach = 0.3 * SMOOTH_HALF + 0.05
    for i in range(n):
        if ext[i]:
            continue
        t = ss[i].t
        idx = [j for j in range(max(0, i - SMOOTH_HALF), min(n, i + SMOOTH_HALF + 1)) if abs(ss[j].t - t) <= reach]
        if len(idx) < 4:
            continue
        # Least squares of p = c0 + c1 dt + c2 dt^2 by the normal equations; c0 is the fit at the sample, c1 its velocity.
        m = [[0.0] * 3 for _ in range(3)]
        rhs = [[0.0] * 3 for _ in range(3)]
        for j in idx:
            d = ss[j].t - t
            pw = (1.0, d, d * d)
            for r_ in range(3):
                for c_ in range(3):
                    m[r_][c_] += pw[r_] * pw[c_]
                for k in range(3):
                    rhs[r_][k] += pw[r_] * pos[j][k]
        sol = _solve3(m, rhs)
        if sol is None:
            continue
        fit, vel = sol[0], sol[1]
        limit = max(SMOOTH_MIN, SMOOTH_SECONDS * math.sqrt(sum(v * v for v in vel)))
        d = [fit[k] - pos[i][k] for k in range(3)]
        dn = math.sqrt(sum(x * x for x in d))
        if dn < 1e-6:
            continue
        if dn > limit:
            d = [x * limit / dn for x in d]
        s = ss[i]
        if s.raw is None:
            s.raw, s.raw_angles = pos[i], _angles(s)
        s.x, s.y, s.z = pos[i][0] + d[0], pos[i][1] + d[1], pos[i][2] + d[2]
        s.moved = math.dist(s.raw, (s.x, s.y, s.z))


def _solve3(m: list[list[float]], rhs: list[list[float]]) -> list[list[float]] | None:
    """m X = rhs for a 3x3 m and three right-hand sides (Gauss-Jordan); X's rows are c0, c1, c2."""
    a = [m[r][:] + rhs[r][:] for r in range(3)]
    for c in range(3):
        piv = max(range(c, 3), key=lambda r: abs(a[r][c]))
        if abs(a[piv][c]) < 1e-12:
            return None
        a[c], a[piv] = a[piv], a[c]
        for r in range(3):
            if r != c:
                f = a[r][c] / a[c][c]
                a[r] = [x - f * y for x, y in zip(a[r], a[c])]
    return [[a[r][3 + k] / a[r][r] for k in range(3)] for r in range(3)]


def smooth(all_lives: list[Life], author: str, on: bool = True) -> dict[str, Any]:
    """
    `_smooth` on every aircraft track: marks dead reckoning everywhere, and
    with `on` moves the tracks of all units but the recording player's own
    (whose aircraft the client does not extrapolate). Returns the check: per
    group the share of dead-reckoned samples, the acceleration between
    consecutive 0.25 s samples (g) as the replay has them and as the table
    has them, and how far samples moved.
    """
    out: dict[str, Any] = {"on": on}
    groups: dict[str, dict[str, list]] = {"own": defaultdict(list), "remote": defaultdict(list)}
    for life in all_lives:
        if life.kind != "air":
            continue
        own = bool(author) and life.user_id == author
        g = groups["own" if own else "remote"]
        g["before"] += _accelerations(life.samples)
        _smooth(life, on and not own)
        g["after"] += _accelerations(life.samples)
        g["samples"].append(len(life.samples))
        g["extrapolated"].append(sum(s.extrapolated for s in life.samples))
        g["moved"] += [s.moved for s in life.samples if s.moved > 0]

    def q(v: list[float]) -> dict[str, Any]:
        v = sorted(v)
        if not v:
            return {}
        return {"p50": round(v[len(v) // 2], 2), "p90": round(v[int(len(v) * 0.9)], 2),
                "p99": round(v[int(len(v) * 0.99)], 2), "over15g": round(sum(x > 15 for x in v) / len(v), 4)}

    for name, g in groups.items():
        total = sum(g["samples"])
        if not total:
            continue
        mv = sorted(g["moved"])
        out[name] = {"samples": total, "extrapolated": sum(g["extrapolated"]),
                     "extrapolatedShare": round(sum(g["extrapolated"]) / total, 4),
                     "accelerationG": {"replay": q(g["before"]), "table": q(g["after"])},
                     "movedMetres": {"samples": len(mv), "p50": round(mv[len(mv) // 2], 2) if mv else 0,
                                     "p90": round(mv[int(len(mv) * 0.9)], 2) if mv else 0,
                                     "max": round(mv[-1], 2) if mv else 0}}
    return out


def _accelerations(ss: list[Sample]) -> list[float]:
    """|second difference| / 9.81 over consecutive samples 0.15-0.35 s apart (g)."""
    out = []
    for a, b, c in zip(ss, ss[1:], ss[2:]):
        d1, d2 = b.t - a.t, c.t - b.t
        if 0.15 < d1 < 0.35 and 0.15 < d2 < 0.35:
            acc = [((cc - bb) / d2 - (bb - aa) / d1) / ((d1 + d2) / 2)
                   for aa, bb, cc in ((a.x, b.x, c.x), (a.y, b.y, c.y), (a.z, b.z, c.z))]
            out.append(math.sqrt(sum(x * x for x in acc)) / 9.81)
    return out


def identify(r: Replay, all_lives: list[Life], table: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """
    Gives each life its pid, vehicle, player and team: from its unit entity
    where the replay has one, else from the kill and hit records (who dealt a
    kill or a hit names their uid, pid and vehicle).
    Returns how well this agrees with the replay's own other records (a self-check).
    """
    types = craft_types(r)
    seen: dict[int, list[tuple[float, int | None, str]]] = defaultdict(list)
    for k in r.kills:
        if k.get("killerUid", wrpl.NO_UID) != wrpl.NO_UID:
            seen[k["killerUid"]].append((k["t"], _pid(k.get("killerPid")), k.get("killerVehicle") or ""))
        # The kill's field 0xB ("victim pid" in community notes) is not the victim's slot: on a 2026 air battle it
        # named the victim's own slot in 2 of 66 kills, where the entity stream names it; it is not used.
    for h in r.hits:
        if h.get("uid", wrpl.NO_UID) != wrpl.NO_UID:
            seen[h["uid"]].append((h["t"], _pid(h.get("pid")), h.get("vehicle") or ""))
    by_uid: dict[int, list[Life]] = defaultdict(list)
    for life in all_lives:
        by_uid[life.uid].append(life)
        u = life.unit
        if u is not None:
            life.vehicle, life.pid, life.team = u.vehicle, u.pid, u.team
            life.figure, life.type = u.kind, u.type
    check = Counter()
    for uid, marks in seen.items():
        for t, pid, vehicle in marks:
            life = _life_at(by_uid.get(uid, []), t)
            if life is None:
                continue
            if life.unit is not None:
                # The entity stream already said; the kill and hit records check it.
                if vehicle:
                    check["recordVehicleMatchesEntity" if vehicle == life.vehicle else "recordVehicleDiffersFromEntity"] += 1
                if pid is not None and life.pid is not None:
                    check["recordPidMatchesEntity" if pid == life.pid else "recordPidDiffersFromEntity"] += 1
                continue
            if pid is not None and life.pid is None:
                life.pid = pid
            if vehicle and not life.vehicle:
                life.vehicle = vehicle
    agree = disagree = 0
    for life in all_lives:
        if not life.figure:
            life.figure = "aircraft" if life.kind == "air" else "ground"
            t = types.get(life.vehicle, "")
            if t:
                life.type = t
                if t in HELI_TYPES:
                    life.figure = "helicopter"
        if life.pid is None:
            continue
        slot = r.slots.get(life.pid, {})
        life.player = slot.get("name", "")
        life.user_id = slot.get("userId", "")
        p = table.get(life.user_id, {})
        life.player = life.player or p.get("name", "")
        if not life.team:
            team = slot.get("team", p.get("team"))
            life.team = str(team) if team is not None else ""
        if life.vehicle and p:
            if life.vehicle in p.get("vehicles", []):
                agree += 1
            else:
                disagree += 1
        if not life.vehicle and p:
            mine = [v for v, k in p.get("vehicleKinds", {}).items() if k == life.kind]
            if len(mine) == 1:
                life.vehicle = mine[0]
    return {"lifeVehicleInPlayersCrafts": agree, "lifeVehicleNotInPlayersCrafts": disagree, **dict(check)}


def players(r: Replay) -> dict[str, dict[str, Any]]:
    """The results' player table by user id, with each player's vehicles and their kinds."""
    ui = (r.results.get("uiScriptsData") or {}).get("playersInfo") or {}
    info = {str(v.get("id")): v for v in ui.values() if isinstance(v, dict)} if isinstance(ui, dict) else {}
    rows = r.results.get("player") or []
    rows = rows if isinstance(rows, list) else [rows]
    out: dict[str, dict[str, Any]] = {}
    for p in rows:
        if not isinstance(p, dict):
            continue
        uid = str(p.get("userId", ""))
        i = info.get(uid, {})
        crafts = i.get("crafts") if isinstance(i.get("crafts"), dict) else {}
        kinds = {}
        ci = i.get("crafts_info") if isinstance(i.get("crafts_info"), dict) else {}
        for v in ci.values():
            if isinstance(v, dict) and str(v.get("slot")) in crafts:
                kinds[crafts[str(v.get("slot"))]] = "air" if v.get("type") in AIR_TYPES else "ground"
        out[uid] = {**p, "vehicles": [crafts[k] for k in sorted(crafts)], "vehicleKinds": kinds,
                    "country": i.get("country"), "name": p.get("name") or i.get("name") or ""}
    for uid, i in info.items():
        if uid not in out:
            out[uid] = {"userId": uid, "name": i.get("name", ""), "team": i.get("team"), "vehicles": [],
                        "vehicleKinds": {}}
    return out


def _pid(v: Any) -> int | None:
    return v if isinstance(v, int) and 0 <= v < 0x7FF else None


def _life_at(candidates: list[Life], t: float) -> Life | None:
    best, gap = None, math.inf
    for life in candidates:
        if life.start - 2 <= t <= life.end + 2:
            d = 0.0 if life.start <= t <= life.end else min(abs(t - life.start), abs(t - life.end))
            if d < gap:
                best, gap = life, d
    return best


def _label(life: Life) -> str:
    """
    A player's name; an AI unit by its vehicle's name and uid ("La-7 #212"; the
    viewer shows "#<n>" as an id, not in the name), the vehicle id where the
    game's localisation is not at hand.
    """
    if life.player:
        return life.player
    if life.display:
        return f"{life.display} #{life.uid}"
    return f"uid {life.uid}"


def _at_time(life: Life | None, t: float, near: float = 0.3) -> Sample | None:
    """Like `_where`, but only between two samples of the life or within `near` seconds of one."""
    s = _where(life, t)
    if s is None or life is None:
        return None
    if s.t == t and life.samples[0].t <= t <= life.samples[-1].t:
        return s
    return s if abs(s.t - t) <= near else None


def _where(life: Life | None, t: float) -> Sample | None:
    """
    Where the life was at t: between its samples, on the line between them
    (an event row at its last sample's place would read, to the viewer, as a
    leap to the next one); after its last, that sample, if near enough.
    """
    if life is None:
        return None
    ts = [s.t for s in life.samples]
    i = bisect.bisect_right(ts, t) - 1
    if i < 0:
        first = life.samples[0]
        return first if first.t - t <= 0.05 else None
    a = life.samples[i]
    if t - a.t > wrpl.NEAR[life.kind]:
        return None
    if i + 1 < len(life.samples) and a.t < t:
        b = life.samples[i + 1]
        f = (t - a.t) / (b.t - a.t) if b.t > a.t else 0.0
        f = max(0.0, min(1.0, f))
        return Sample(t, a.x + (b.x - a.x) * f, a.y + (b.y - a.y) * f, a.z + (b.z - a.z) * f, a.attitude, a.angles,
                      smooth_angles=a.smooth_angles)
    return a


# ---------------------------------------------------------------- the table


def _angles(s: Sample) -> tuple[float, float, float] | None:
    """
    The attitude as the replay sends it, in the table's conventions: compass
    heading, pitch (nose up positive) and roll (right wing down positive), in
    degrees. The flight model's packed heading is counted from east: compass =
    heading + 90 deg (checked against the direction of travel); its roll is
    positive with the LEFT wing down - on the recording player's own aircraft,
    which the client does not extrapolate, the packed roll is positive in left
    turns in 235 of 237 samples of a clear turn (air arcade battle) - so its
    sign is turned. A ground state's angles are already compass, pitch, roll
    (its roll's sense is not checked).
    """
    if s.attitude is not None:
        h, p, roll = wrpl._euler(s.attitude)
        return (math.degrees(h) + 90.0) % 360, math.degrees(p), -math.degrees(roll)
    if s.angles is not None and s.angles[0] is not None:
        return s.angles[0] % 360, s.angles[1] or 0.0, s.angles[2] or 0.0
    return None


def _attitude(s: Sample) -> tuple[float, ...] | None:
    """The look vector in the game's axes, then compass heading, pitch and roll (degrees; see `_angles`): the
    smoothed attitude where `_smooth` gave one."""
    a = s.smooth_angles or _angles(s)
    if a is None:
        return None
    compass, p = math.radians(a[0]), math.radians(a[1])
    cp = math.cos(p)
    return math.sin(compass) * cp, math.sin(p), math.cos(compass) * cp, a[0], a[1], a[2]


def _speeds(samples: list[Sample]) -> list[float | None]:
    """Metres per second over about two seconds around each sample (the positions' own steps are noisy)."""
    ts = [s.t for s in samples]
    out: list[float | None] = []
    for i, s in enumerate(samples):
        a = bisect.bisect_left(ts, s.t - 1.0)
        b = bisect.bisect_right(ts, s.t + 1.0) - 1
        if b <= a:
            a, b = max(0, i - 1), min(len(samples) - 1, i + 1)
        p, q = samples[a], samples[b]
        dt = q.t - p.t
        out.append(math.dist((p.x, p.y, p.z), (q.x, q.y, q.z)) / dt if 0 < dt < 30 else None)
    return out


def _track(life: Life) -> str:
    """
    One thing the viewer draws: a life. Named for its player or unit; the
    "#<hex>" suffix keeps lives apart and is not shown as part of the name.
    """
    base = life.player or life.display or f"uid {life.uid}"
    return f"{base} #{life.uid * 4096 + min(life.n, 4095):x}"


def _row(life: Life, s: Sample, event: str) -> dict[str, Any]:
    """A row of the life at sample s, with the unit's attitude there: an event row keeps the heading of the unit it
    happens to, so a track's latest row (a ship's gunfire, say) still says where the unit points."""
    row = {"time": s.t, "event": event, "track": _track(life), "player": _label(life), "userId": life.user_id,
           "team": life.team, "life": life.id, "uid": life.uid, "kind": life.figure, "type": life.type,
           "Vehicle": life.vehicle, "VehicleName": life.display, "VehicleShortName": life.vehicle_short or life.display,
           "VehicleNameKey": life.vehicle_key, "ai": not life.is_player, "isPlayer": life.is_player,
           "x": s.x, "y": s.y, "z": s.z, "mission": life.unit.mission if life.unit else ""}
    a = _attitude(s)
    if a:
        row.update(dirX=a[0], dirY=a[1], dirZ=a[2], heading=a[3], pitch=a[4], roll=a[5])
    return row


@dataclass
class Weapon:
    """A rocket, missile, bomb, torpedo or dropped load: its entity, release, launcher and flight."""

    entity: ecs.Entity
    kind: str
    release: dict[str, Any] | None
    launcher: Life | None = None
    distance: float | None = None
    track: list[tuple] = field(default_factory=list)


def weapons(r: Replay, all_lives: list[Life]) -> list[Weapon]:
    """
    Every projectile entity, with where it was released (its component), the
    unit that released it (the nearest unit within 300 m and 1.5 s: the
    replay does not name the launcher) and its flight (the weapons-in-flight
    messages name the entity).
    """
    buckets: dict[int, list[tuple[Life, Sample]]] = defaultdict(list)
    for life in all_lives:
        for s in life.samples:
            buckets[int(s.t)].append((life, s))
    created: dict[int, list[float]] = defaultdict(list)
    for e in r.stream.entities:
        if e.template in ecs.PROJECTILES:
            created[e.eid & 0x3FFFFF].append(e.t)
    out = []
    for e in r.stream.entities:
        if e.template not in ecs.PROJECTILES:
            continue
        rel = ecs.release(e)
        idx = e.eid & 0x3FFFFF
        # The flight records name the entity's index; an index is given to the next weapon once this one is
        # gone, so its flight ends at its removal or the next creation with that index, whichever comes first.
        later = [c for c in created.get(idx, []) if c > e.t]
        end = min(e.destroyed if e.destroyed is not None else 1e12, later[0] if later else 1e12)
        track = [p for p in r.shells.get(idx, []) if e.t - 1 <= p[0] <= end + (1 if not later or end < later[0] else 0)]
        # A flight is one continuous run: a pause of more than 5 s is another weapon's records.
        for i in range(1, len(track)):
            if track[i][0] - track[i - 1][0] > 5.0:
                track = track[:i]
                break
        guided = any(p[5] for p in track)
        kind = {"rocket+arh_shell": "missile", "bomb": "bomb", "torpedo": "torpedo", "payload": "payload",
                "jettisoned": "jettisoned"}.get(e.template, "missile" if guided else "rocket")
        w = Weapon(e, kind, rel, track=track)
        if rel is not None:
            best = None
            for b in range(int(e.t) - 2, int(e.t) + 3):
                for life, s in buckets.get(b, ()):
                    if abs(s.t - e.t) > LAUNCHER_S:
                        continue
                    d = math.dist(rel["pos"], (s.x, s.y, s.z))
                    if d <= LAUNCHER_M and (best is None or d < best[0]):
                        best = (d, life)
            if best:
                w.distance, w.launcher = round(best[0], 1), best[1]
        out.append(w)
    return out


def rows(r: Replay, all_lives: list[Life], all_weapons: list[Weapon] | None = None,
         rpm: dict[int, tuple] | None = None, extra: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = list(extra or [])
    by_uid: dict[int, list[Life]] = defaultdict(list)
    rpm = rpm or {}
    entries = flight_entries(r)
    author = str(r.results.get("authorUserId") or "")
    cockpit = _cockpit_states(r)
    for life in all_lives:
        by_uid[life.uid].append(life)
        until = life.wreck_until()
        series = rpm.get(life.uid) if life.kind == "air" else None
        own = bool(author) and life.user_id == author
        for s, v in zip(life.samples, _speeds(life.samples)):
            row = _row(life, s, "position")
            row["speed"] = v
            if series:
                row["rpm"] = _rpm_at(series, s.t)
            if 0 <= s.entry < len(entries) and entries[s.entry] is not None:
                row.update(_flight_columns(entries[s.entry], own))
            if own and life.kind == "air":
                row.update(_cockpit_columns(cockpit, s.t))
            row["alive"] = 0.0 if until is not None and life.died < s.t <= until else 1.0
            a = _attitude(s)
            if a:
                row.update(dirX=a[0], dirY=a[1], dirZ=a[2], heading=a[3], pitch=a[4], roll=a[5])
            raw = s.raw or (s.x, s.y, s.z)
            row.update(xRaw=raw[0], yRaw=raw[1], zRaw=raw[2], extrapolated=s.extrapolated, moved=s.moved)
            ra = s.raw_angles or (a[3:6] if a else None)
            if ra:
                row.update(headingRaw=ra[0], pitchRaw=ra[1], rollRaw=ra[2])
            out.append(row)

    def at(uid: int | None, t: float) -> tuple[Life | None, Sample | None]:
        if uid is None or uid == wrpl.NO_UID:
            return None, None
        life = _life_at(by_uid.get(uid, []), t)
        return life, _at_time(life, t)

    def who(uid: Any, pid: Any, t: float) -> str:
        return _who(r, by_uid, uid, pid, t)

    for k in r.kills:
        killer, ks = at(k.get("killerUid"), k["t"])
        victim, vs = at(k.get("victimUid"), k["t"])
        names = (who(k.get("killerUid"), k.get("killerPid"), k["t"]), who(k.get("victimUid"), None, k["t"]))
        for event, life, s, other in (("kill", killer, ks, names[1]), ("death", victim, vs, names[0])):
            if s is None or life is None:
                continue
            out.append({**_row(life, s, event), "time": k["t"], "other": other, "weapon": k.get("weapon", "")})
    # Who last damaged a unit: a destroyed module names only the unit and the part.
    damage: dict[int, list[tuple[float, str, str]]] = defaultdict(list)
    for h in r.hits:
        victim, vs = at(h.get("victimUid"), h["t"])
        attacker = who(h.get("uid"), h.get("pid"), h["t"])
        if h.get("victimUid") not in (None, wrpl.NO_UID) and attacker:
            damage[h["victimUid"]].append((h["t"], attacker, h.get("vehicle", "")))
        if vs is None or victim is None:
            continue
        out.append({**_row(victim, vs, f"hit_{h['severity']}"), "time": h["t"], "other": attacker,
                    "weapon": h.get("vehicle", "")})
    for marks in damage.values():
        marks.sort()
    for m in r.part_kills:
        victim, vs = at(m.get("uid"), m["t"])
        if vs is None or victim is None:
            continue
        last = [d for d in damage.get(m.get("uid"), []) if m["t"] - PART_BY_HIT <= d[0] <= m["t"] + 0.5]
        out.append({**_row(victim, vs, "module_destroyed"), "time": m["t"], "other": last[-1][1] if last else "",
                    "weapon": f"part {m.get('part')}"})
    for w in all_weapons or []:
        name = w.kind
        s = _at_time(w.launcher, w.entity.t) if w.launcher is not None else None
        if s is not None:
            out.append({**_row(w.launcher, s, "launch"), "time": w.entity.t, "weapon": name})
        if len(w.track) < 2:
            continue
        owner = _label(w.launcher) if w.launcher else "unknown launcher"
        # The whole eid (index and generation): an index is given to one weapon after another.
        eid = w.entity.eid
        segments: list[list[Sample]] = [[]]
        for q in w.track:
            p = Sample(q[0], q[1], q[2], q[3])
            if segments[-1]:
                a = segments[-1][-1]
                d = math.dist((a.x, a.y, a.z), (p.x, p.y, p.z))
                if d > max(SLACK["weapon"], TOP_SPEED["weapon"] * (p.t - a.t)):
                    r.breaks.append({"uid": None, "eid": eid, "kind": "weapon", "time": round(p.t, 3),
                                     "from": [round(a.x), round(a.y), round(a.z)], "to": [round(p.x), round(p.y), round(p.z)],
                                     "distance": round(d), "seconds": round(p.t - a.t, 3)})
                    segments.append([])
            segments[-1].append(p)
        gone = w.entity.destroyed
        for k, pts in enumerate(segments):
            if len(pts) < 2:
                continue
            label = f"{owner} {name} #{eid * 16 + min(k, 15):x}"
            sp = _speeds(pts)
            for i, (p, v) in enumerate(zip(pts, sp)):
                last = k == len(segments) - 1 and i == len(pts) - 1
                event = "impact" if last and gone is not None and gone - p.t <= 3.0 else "position"
                row = {"time": p.t, "event": event, "track": label, "player": owner, "userId": "",
                       "team": w.launcher.team if w.launcher else "", "life": f"w{eid:x}" + (f"#{k + 1}" if k else ""),
                       "uid": None, "kind": name, "type": w.entity.template, "Vehicle": "", "x": p.x, "y": p.y,
                       "z": p.z, "xRaw": p.x, "yRaw": p.y, "zRaw": p.z, "speed": v, "alive": 1.0, "other": owner,
                       "ai": (not w.launcher.is_player) if w.launcher else None,
                       "isPlayer": w.launcher.is_player if w.launcher else None}
                nxt = pts[i + 1] if i + 1 < len(pts) else pts[i - 1]
                d = (nxt.x - p.x, nxt.y - p.y, nxt.z - p.z) if i + 1 < len(pts) else (p.x - nxt.x, p.y - nxt.y, p.z - nxt.z)
                n = math.sqrt(sum(c * c for c in d))
                if n > 0:
                    row.update(dirX=d[0] / n, dirY=d[1] / n, dirZ=d[2] / n,
                               heading=math.degrees(math.atan2(d[0], d[2])) % 360,
                               pitch=math.degrees(math.asin(max(-1.0, min(1.0, d[1] / n)))))
                out.append(row)
    out += _effects(r)
    match = match_name(r.header)
    for row in out:
        row["match"] = match
    out.sort(key=lambda row: row["time"])
    return out


#: A destroyed module is put down to the last hit on its unit no more than this long (s) before it.
PART_BY_HIT = 5.0


def _flight_columns(x: tuple, own: bool) -> dict[str, Any]:
    """
    An aircraft sample's columns from its flight entry (see `flight_entries`):
    the velocity it was sent with and its engines; on the recording player's
    own aircraft also its controls, throttle and rounds left. For other
    aircraft the entry's control bytes and rounds are refreshed only now and
    then (a median of 4 and 1 changes an aircraft in an hour's battle; their
    rounds fall within 3 s of 41 of 134 hits they score) and stay in the flight
    sidecar; their engine fields change with the engine (start, afterburner,
    loss) and are used.
    """
    v, nib, eng, ammo = x[0], x[1], x[2], x[3]
    state, burn, cond = _engine(eng)
    out = {"vx": v[0], "vy": v[1], "vz": v[2], "engine": state, "afterburner": burn, "engineCondition": cond}
    if own and nib:
        out.update(elevator=(nib[1] - 8) / 7, aileron=(nib[2] - 8) / 7, rudder=(nib[3] - 8) / 7, throttle=nib[11] / 15,
                   ammo=" ".join(map(str, ammo)))
    return out


#: Instruments the recording player's rows take from the cockpit (0xD04A), besides `AUTHOR_COLUMNS`: the throttle
#: of its first engine (1.1 is war emergency power or afterburner, which the flight entry's fifteenths do not show).
_COCKPIT_THROTTLE = 240


def _cockpit_states(r: Replay) -> tuple[list[float], list[dict[int, float]]]:
    """The recording player's instruments as they stood after each 0xD04A message (a simulator cockpit sends only
    the values that changed), for the instruments the table takes."""
    keep = set(AUTHOR_COLUMNS.values()) | {_COCKPIT_THROTTLE}
    times: list[float] = []
    states: list[dict[int, float]] = []
    now: dict[int, float] = {}
    for t, d in r.cockpit:
        changed = {k: v for k, v in d.items() if k in keep}
        if changed or not states:
            now = {**now, **changed}
            times.append(t)
            states.append(now)
    return times, states


def _cockpit_columns(cockpit: tuple[list[float], list[dict[int, float]]], t: float) -> dict[str, Any]:
    """The recording player's instruments at t: the last message at most 0.2 s after it (a tick's message comes
    about 0.1 s before its flight packet)."""
    times, states = cockpit
    i = bisect.bisect_right(times, t + 0.2) - 1
    if i < 0:
        return {}
    d = states[i]
    out = {col: d.get(k) for col, k in AUTHOR_COLUMNS.items() if k in d}
    if _COCKPIT_THROTTLE in d:
        out["throttle"] = d[_COCKPIT_THROTTLE]
    return out


def _who(r: Replay, by_uid: dict[int, list[Life]], uid: Any, pid: Any, t: float) -> str:
    """Who a record names: the life of its uid at that moment, else the player of its slot, else 'uid <n>'."""
    life = _life_at(by_uid.get(uid, []), t) if uid not in (None, wrpl.NO_UID) else None
    if life:
        return _label(life)
    pid = _pid(pid)
    # 0 is also what units no player drives get; only another pid names someone.
    if pid and r.slots.get(pid, {}).get("name"):
        return r.slots[pid]["name"]
    return _uid_label(uid)


def _effects(r: Replay) -> list[dict[str, Any]]:
    """
    Explosions (0xD08E) and flak bursts (0xD01F) as rows of their own, event
    `explosion` / `flak`, at their position, kind `effect`, no track (each is a
    moment, not a thing that moves); an explosion's direction where it has one.
    `type` is the message's kind field (hex), which is not named.
    """
    out = []
    for event, items in (("explosion", r.explosions), ("flak", r.flak)):
        for e in items:
            x, y, z = e["pos"]
            row = {"time": e["t"], "event": event, "track": "", "player": "", "kind": "effect", "type": e.get("kind", ""),
                   "x": x, "y": y, "z": z, "xRaw": x, "yRaw": y, "zRaw": z, "alive": 1.0}
            d = e.get("dir")
            n = math.sqrt(sum(c * c for c in d)) if d else 0.0
            if n > 0.5:
                row.update(dirX=d[0] / n, dirY=d[1] / n, dirZ=d[2] / n)
            out.append(row)
    return out


def _uid_label(uid: Any) -> str:
    return "" if uid in (None, wrpl.NO_UID) else f"uid {uid}"


def table(data: list[dict[str, Any]]):
    import numpy as np
    import pyarrow as pa

    arrays, fields = [], []
    for name, kind in COLUMNS:
        values = [row.get(name) for row in data]
        if kind == "str":
            arr = pa.array(["" if v is None else str(v) for v in values], type=pa.string()).dictionary_encode()
            fields.append(pa.field(name, pa.dictionary(pa.int32(), pa.string())))
        elif kind == "bool":
            arr = pa.array([None if v is None else bool(v) for v in values], type=pa.bool_())
            fields.append(pa.field(name, pa.bool_()))
        elif kind == "i16":
            mask = np.array([v is None for v in values], dtype=bool)
            arr = pa.array(np.array([0 if v is None else v for v in values], dtype=np.int16), mask=mask)
            fields.append(pa.field(name, pa.int16()))
        else:
            t = pa.float64() if kind == "f64" else pa.float32()
            arr = pa.array(np.array([np.nan if v is None else v for v in values], dtype=float), type=t,
                           from_pandas=True)
            fields.append(pa.field(name, t))
        arrays.append(arr)
    schema = pa.schema(fields, metadata={"heat3d": json.dumps(HINTS)})
    return pa.Table.from_arrays(arrays, schema=schema)


# ---------------------------------------------------------------- messages to units


@dataclass
class UnitMessage:
    """One message to a unit (see wrpl.read_mpi), with the entity it was sent to."""

    t: float
    mid: int
    entity: ecs.Entity | None
    body: bytes

    @property
    def uid(self) -> int | None:
        return self.entity.uid if self.entity is not None else None


def unit_messages(r: Replay) -> list[UnitMessage]:
    """
    Every message to a unit with its entity: the one whose eid (index and
    generation) is the message's ext UID and that was created by then (the
    last such; an index and generation can come again after the entity is
    gone).
    """
    made: dict[tuple[int, int], list[ecs.Entity]] = defaultdict(list)
    for e in r.stream.entities:
        made[(e.eid & 0x3FFFFF, e.eid >> 22)].append(e)
    out = []
    for t, ext, mid, body in r.unit_msgs:
        cands = made.get(wrpl.entity_of(ext), [])
        e = None
        for c in cands:
            if c.t - 1.0 <= t:
                e = c
        out.append(UnitMessage(t, mid, e, body))
    return out


#: Messages to units that become event rows at the unit: message id -> event.
UNIT_EVENTS = {
    0xF04B: "dead",          # OnUnitDead: every kill record's victim has one within 2 s (97 of 97, air arcade)
    0xF050: "bailout",       # UnitBailoutResponse
    0xF033: "repair",        # UnitRepair
    0xF054: "rearm",         # UnitRearm
    0xF0BD: "bullet_rearm",  # UnitBulletRearm
    0xD046: "reload",        # UnitReloadGun
    0xF01B: "fire_start",    # an AA gun opens fire (each is followed by 0xF01C)
    0xF01C: "fire_stop",     # GmDoStopFire
    0xF0B1: "gun_shot",      # UnitSingleShot: a gun's single shot (heavy AA and artillery)
    0xF0A0: "gun_shot",      # GmDoSingleShotUnreliable
}


def _basis(s: Sample) -> tuple[tuple[float, ...], tuple[float, ...], tuple[float, ...]] | None:
    """A unit's forward, up and right axes in the game's axes, by the sample's attitude (None without one)."""
    a = s.smooth_angles or _angles(s)
    if a is None:
        return None
    h, p, rl = (math.radians(v) for v in a)
    fwd = (math.sin(h) * math.cos(p), math.sin(p), math.cos(h) * math.cos(p))
    right0 = (math.cos(h), 0.0, -math.sin(h))
    up0 = (-math.sin(h) * math.sin(p), math.cos(p), -math.cos(h) * math.sin(p))
    c, sn = math.cos(rl), math.sin(rl)
    right = tuple(right0[k] * c - up0[k] * sn for k in range(3))
    up = tuple(up0[k] * c + right0[k] * sn for k in range(3))
    return fwd, up, right


def _rotate(s: Sample, local: tuple[float, float, float]) -> tuple[float, float, float] | None:
    """A point in a unit's own frame (x forward, y up, z right; m) in the game's axes, by the sample's attitude."""
    b = _basis(s)
    if b is None:
        return None
    fwd, up, right = b
    return tuple(s_ + fwd[k] * local[0] + up[k] * local[1] + right[k] * local[2]
                 for k, s_ in enumerate((s.x, s.y, s.z)))


def _unrotate(s: Sample, v: tuple[float, float, float]) -> tuple[float, float, float] | None:
    """A direction in the game's axes in a unit's own frame (x forward, y up, z right), by the sample's attitude."""
    b = _basis(s)
    if b is None:
        return None
    return tuple(sum(axis[k] * v[k] for k in range(3)) for axis in b)


def unit_rows(r: Replay, msgs: list[UnitMessage], all_lives: list[Life]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """
    Rows from the messages to units, and their check:

    * `shot`: one row per projectile that hit a unit (0xF0E9), at the
      shooter's position at the moment of the hit, `targetX/Y/Z` the hit point
      (the unit hit, moved by the hit point in its own frame), the direction
      towards it, `other` the unit hit. Hits only: a shot that missed is not
      in a client replay.
    * `gun_shot`, `fire_start`, `fire_stop` of AA guns and artillery, and
      `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` at the unit
      (`UNIT_EVENTS`); a static gun without a track at the place its entity
      was created.
    """
    by_uid: dict[int, list[Life]] = defaultdict(list)
    for life in all_lives:
        by_uid[life.uid].append(life)

    def where(uid: int | None, t: float) -> tuple[Life | None, Sample | None]:
        if uid is None:
            return None, None
        life = _life_at(by_uid.get(uid, []), t)
        return life, _at_time(life, t, near=1.0) if life else None

    def static(e: ecs.Entity | None) -> tuple[float, float, float] | None:
        tm = e.comps.get("transform") if e is not None else None
        return tuple(tm["pos"]) if isinstance(tm, dict) and tm.get("pos") else None

    entity_by_uid: dict[int, list[ecs.Entity]] = defaultdict(list)
    for e in r.stream.entities:
        if e.uid is not None:
            entity_by_uid[e.uid].append(e)

    def entity_at(uid: int, t: float) -> ecs.Entity | None:
        best = None
        for e in entity_by_uid.get(uid, []):
            if e.t - 1.0 <= t:
                best = e
        return best

    out: list[dict[str, Any]] = []
    check: Counter = Counter()
    for m in msgs:
        if m.mid == 0xF0E9:
            try:
                hit = wrpl.read_hit_effect(m.body)
            except (wrpl.FormatError, EOFError, IndexError, struct.error):
                check["hitEffectsNotRead"] += 1
                continue
            if hit is None or m.uid is None:
                check["hitEffectsNotRead"] += 1
                continue
            check["projectileHits"] += 1
            victim, vs = where(m.uid, m.t)
            shooter, ss = where(hit["shooter"], m.t)
            target = None
            if vs is not None:
                target = _rotate(vs, hit["local"]) if hit["aligned"] else None
                target = target or (vs.x, vs.y, vs.z)
            if ss is None:
                pos = static(entity_at(hit["shooter"], m.t))
                if pos is None:
                    check["shotWithoutShooterPlace"] += 1
                    continue
                row = {"time": m.t, "event": "shot", "track": "", "player": _uid_label(hit["shooter"]),
                       "uid": hit["shooter"], "kind": "effect", "x": pos[0], "y": pos[1], "z": pos[2]}
            else:
                row = {**_row(shooter, ss, "shot"), "time": m.t}
                pos = (ss.x, ss.y, ss.z)
            row["other"] = _label(victim) if victim else _uid_label(m.uid)
            if victim is not None:
                row.update(otherVehicle=victim.vehicle, otherLife=victim.id)
            row["hitPart"] = hit["part"]
            if target is not None:
                d = [target[k] - pos[k] for k in range(3)]
                n = math.sqrt(sum(c * c for c in d))
                row.update(targetX=target[0], targetY=target[1], targetZ=target[2])
                if n > 0:
                    row.update(dirX=d[0] / n, dirY=d[1] / n, dirZ=d[2] / n)
                check["shotsWithTarget"] += 1
                # The hit on the victim itself: the point in its own frame as sent, and the way the shot came,
                # turned into that frame by the victim's attitude then (only for a point sent in that frame).
                if vs is not None and hit["aligned"]:
                    loc = hit["local"]
                    row.update(hitLocalX=loc[0], hitLocalY=loc[1], hitLocalZ=loc[2])
                    check["shotsWithLocalPoint"] += 1
                    ld = _unrotate(vs, (d[0] / n, d[1] / n, d[2] / n)) if n > 0 else None
                    if ld is not None:
                        row.update(hitDirX=ld[0], hitDirY=ld[1], hitDirZ=ld[2])
            out.append(row)
        elif m.mid in UNIT_EVENTS:
            event = UNIT_EVENTS[m.mid]
            check[event] += 1
            life, s = where(m.uid, m.t)
            if s is not None:
                out.append({**_row(life, s, event), "time": m.t})
                continue
            pos = static(m.entity)
            if pos is None:
                check[f"{event}WithoutPlace"] += 1
                continue
            out.append({"time": m.t, "event": event, "track": "", "uid": m.uid, "kind": "effect",
                        "player": f"{m.entity.class_name.rpartition('/')[2]} #{m.uid}" if m.uid is not None else "",
                        "Vehicle": m.entity.class_name.rpartition("/")[2], "ai": True, "isPlayer": False,
                        "x": pos[0], "y": pos[1], "z": pos[2]})
    return out, dict(check)


def rpm_series(msgs: list[UnitMessage]) -> dict[int, tuple[list[float], list[list[int]]]]:
    """Each uid's engine rpm over time (0xD047 FmwRpm): uid -> (times, rpm per engine)."""
    out: dict[int, tuple[list[float], list[list[int]]]] = {}
    for m in msgs:
        if m.mid == 0xD047 and m.uid is not None:
            v = wrpl.read_rpm(m.body)
            if v:
                ts, vs = out.setdefault(m.uid, ([], []))
                ts.append(m.t)
                vs.append(v)
    return out


def _rpm_at(series: tuple[list[float], list[list[int]]] | None, t: float) -> float | None:
    """The rpm sent last before t (within 2 s): the mean over the engines."""
    if not series:
        return None
    ts, vs = series
    i = bisect.bisect_right(ts, t) - 1
    if i < 0 or t - ts[i] > 2.0:
        return None
    return sum(vs[i]) / len(vs[i])


def _rpm_check(r: Replay, series: dict[int, tuple], all_lives: list[Life]) -> dict[str, Any]:
    """The recording player's rpm (0xD047) against its own cockpit instrument 93 at the same moments."""
    author = str(r.results.get("authorUserId") or "")
    mine = {l.uid for l in all_lives if author and l.user_id == author}
    inst = [(t, d[93]) for t, d in r.cockpit if 93 in d]
    ts = [t for t, _ in inst]
    pairs = []
    for uid in mine:
        for t, v in zip(*series.get(uid, ([], []))):
            i = bisect.bisect_left(ts, t)
            if i < len(ts) and abs(ts[i] - t) < 0.2:
                pairs.append((sum(v) / len(v), inst[i][1]))
    if len(pairs) < 10:
        return {"pairs": len(pairs)}
    xs, ys = [a for a, _ in pairs], [b for _, b in pairs]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    sxy = sum((a - mx) * (b - my) for a, b in pairs)
    sxx, syy = sum((a - mx) ** 2 for a in xs), sum((b - my) ** 2 for b in ys)
    diffs = sorted(abs(a - b) for a, b in pairs)
    return {"pairs": len(pairs), "correlation": round(sxy / math.sqrt(sxx * syy), 4) if sxx and syy else None,
            "medianDifference": round(diffs[len(diffs) // 2], 1)}


def _shooter_check(r: Replay, msgs: list[UnitMessage]) -> dict[str, Any]:
    """Each hit or kill record's attacker against the shooters of the projectile hits (0xF0E9, 0xF133) on its victim in the 3 s before."""
    shooters: dict[int, list[tuple[float, int]]] = defaultdict(list)
    for m in msgs:
        if m.uid is None or m.mid not in (0xF0E9, 0xF133):
            continue
        try:
            v = wrpl.read_hit_effect(m.body) if m.mid == 0xF0E9 else wrpl.read_unit_explosion(m.body)
        except (wrpl.FormatError, EOFError, IndexError, struct.error):
            continue
        if v:
            shooters[m.uid].append((m.t, v["shooter"]))
    out: Counter = Counter()
    for rec in [*r.hits, *({**k, "uid": k.get("killerUid")} for k in r.kills)]:
        v, a = rec.get("victimUid"), rec.get("uid")
        if a in (None, wrpl.NO_UID) or v in (None, wrpl.NO_UID):
            continue
        near = {s for t, s in shooters.get(v, []) if rec["t"] - 3.0 <= t <= rec["t"] + 0.5}
        out["noProjectileHitNear" if not near else "attackerAmongShooters" if a in near else "attackerNotAmongShooters"] += 1
    return dict(out)


def _death_check(r: Replay, msgs: list[UnitMessage]) -> dict[str, Any]:
    """OnUnitDead (0xF04B) against the kill records: how many kills have one for their victim within 2 s."""
    dead: dict[int, list[float]] = defaultdict(list)
    for m in msgs:
        if m.mid == 0xF04B and m.uid is not None:
            dead[m.uid].append(m.t)
    kills = [k for k in r.kills if k.get("victimUid") not in (None, wrpl.NO_UID)]
    return {"onUnitDead": sum(len(v) for v in dead.values()), "kills": len(kills),
            "killsWithOnUnitDead": sum(1 for k in kills if any(abs(t - k["t"]) <= 2 for t in dead.get(k["victimUid"], [])))}


def flight_entries(r: Replay) -> list[tuple | None]:
    """
    Every flight-model entry of `r.flight_raw` decoded once (wrpl.flight_extras), kept small: (velocity, the 14
    nibbles, the engines as (state, afterburner, condition, tail) tuples, the ammunition per weapon, the velocity word,
    the number list as JSON); None where an entry does not read.
    """
    if r.flight_x is None:
        out: list[tuple | None] = []
        text: dict[str, str] = {}
        for _, _, n, bits, phase in r.flight_raw:
            try:
                x = wrpl.flight_extras(n, bits, r.layout or "2026", phase)
            except (wrpl.FormatError, EOFError):
                out.append(None)
                continue
            nums = json.dumps(x["numbers"], separators=(",", ":"))
            out.append((x["velocity"], bytes(x["nibbles"]), tuple(tuple(e) for e in x["engines"]), tuple(x["ammo"]),
                        x["velocityWord"], text.setdefault(nums, nums)))
        r.flight_x = out
    return r.flight_x


def _engine(engines: tuple) -> tuple[str | None, float | None, int | None]:
    """An aircraft's engines as one: the state (all engines' when they differ, "running/dead"), the afterburner (0-1,
    the most of any engine, 0 when none is lit), the lowest condition byte (only sent after a hit)."""
    if not engines:
        return None, None, None
    states = [wrpl.ENGINE_STATES.get(e[0], str(e[0])) for e in engines]
    state = states[0] if len(set(states)) == 1 else "/".join(states)
    burn = max((e[1] / 32767 for e in engines if e[1] is not None), default=0.0)
    cond = min((e[2] for e in engines if e[2] is not None), default=None)
    return state, burn, cond


def flight_table(r: Replay):
    """
    The flight sidecar: every flight-model entry of every aircraft, whole (its
    bits and the bit of its first byte it started at), with what is known of
    the fields the table does not use (`wrpl.flight_extras`): the velocity
    word and its velocity, the 14 nibbles after it (for the recording
    player's aircraft its elevator, ailerons, rudder and throttle; for others
    rarely updated), the engines' fields and states, the number list (the
    weapons' rounds left). The time is the packet's (before re-timing).
    """
    import pyarrow as pa

    names = ("time", "uid", "bits", "phase", "entry", "velocityWord", "vx", "vy", "vz", "control1", "control2",
             "control3", "throttle", "nibbles", "engines", "engineState", "afterburner", "engineCondition", "ammo",
             "numbers")
    cols: dict[str, list] = {k: [] for k in names}
    for (t, uid, n, bits, phase), x in zip(r.flight_raw, flight_entries(r)):
        cols["time"].append(t)
        cols["uid"].append(uid)
        cols["bits"].append(n)
        cols["phase"].append(phase)
        cols["entry"].append(bits)
        v, nib, eng, ammo, word, nums = x or (None, b"", (), (), None, "")
        state, burn, cond = _engine(eng)
        for k, val in zip(("vx", "vy", "vz"), v or (None, None, None)):
            cols[k].append(val)
        cols["velocityWord"].append(word)
        for k, i in (("control1", 1), ("control2", 2), ("control3", 3), ("throttle", 11)):
            cols[k].append(nib[i] if nib else None)
        cols["nibbles"].append(nib.hex())
        cols["engines"].append(json.dumps([list(e) for e in eng]) if eng else "")
        cols["engineState"].append(state or "")
        cols["afterburner"].append(burn)
        cols["engineCondition"].append(cond)
        cols["ammo"].append(" ".join(map(str, ammo)))
        cols["numbers"].append(nums)
    f32 = pa.float32()
    return pa.table({
        "time": pa.array(cols["time"], pa.float64()), "uid": pa.array(cols["uid"], pa.int16()),
        "bits": pa.array(cols["bits"], pa.int32()), "phase": pa.array(cols["phase"], pa.int8()),
        "entry": pa.array(cols["entry"], pa.binary()),
        "velocityWord": pa.array(cols["velocityWord"], pa.uint32()),
        "vx": pa.array(cols["vx"], f32), "vy": pa.array(cols["vy"], f32), "vz": pa.array(cols["vz"], f32),
        "control1": pa.array(cols["control1"], pa.int8()), "control2": pa.array(cols["control2"], pa.int8()),
        "control3": pa.array(cols["control3"], pa.int8()), "throttle": pa.array(cols["throttle"], pa.int8()),
        "nibbles": pa.array(cols["nibbles"], pa.string()).dictionary_encode(),
        "engines": pa.array(cols["engines"], pa.string()).dictionary_encode(),
        "engineState": pa.array(cols["engineState"], pa.string()).dictionary_encode(),
        "afterburner": pa.array(cols["afterburner"], f32),
        "engineCondition": pa.array(cols["engineCondition"], pa.int16()),
        "ammo": pa.array(cols["ammo"], pa.string()).dictionary_encode(),
        "numbers": pa.array(cols["numbers"], pa.string()).dictionary_encode(),
    })


def messages_table(r: Replay, msgs: list[UnitMessage]):
    """
    The sidecar: every message to a unit and every packet no reader here
    takes, whole, so nothing of the replay is lost to the table: time, packet
    type, message id and its community name, the unit's uid, entity id and
    template where the message names one, its id fields as hex where it has
    them, what is decoded of it (`decoded`, JSON; see wrpl.decode_unit_message)
    and the payload.
    """
    import pyarrow as pa

    cols: dict[str, list] = {k: [] for k in ("time", "packet", "message", "name", "uid", "eid", "template",
                                             "vehicle", "fields", "decoded", "payload")}

    def add(t, ptype, mid, uid, e, body, name=None, fields=None, unit=False):
        cols["time"].append(t)
        cols["packet"].append(ptype)
        cols["message"].append(f"{mid:#06x}" if mid is not None else "")
        cols["name"].append(name if name is not None else wrpl.UNIT_MESSAGES.get(mid, "") if mid is not None else "")
        cols["uid"].append(uid)
        cols["eid"].append(e.eid if e is not None else None)
        cols["template"].append(e.template if e is not None else "")
        cols["vehicle"].append(e.class_name.rpartition("/")[2] if e is not None else "")
        f = fields or ""
        if fields is None and ptype == 4 and body:
            try:
                f = json.dumps({str(n): v.hex() for n, (_, v) in wrpl.id_field_map(body).items()})
            except (wrpl.FormatError, EOFError, IndexError, ValueError):
                f = ""
        cols["fields"].append(f)
        d = wrpl.decode_unit_message(mid, body) if unit else None
        cols["decoded"].append(json.dumps(_jsonable(d)) if d is not None else "")
        cols["payload"].append(bytes(body))

    for m in msgs:
        add(m.t, 4, m.mid, m.uid, m.entity, m.body, unit=True)
    by_eid = {e.eid: e for e in r.stream.entities}
    for t, eid, comp, kind, v, rest in r.stream.replications:
        e = by_eid.get(eid)
        add(t, 6, 0x22, e.uid if e else None, e, rest, name=comp,
            fields=json.dumps({"type": kind, "value": _jsonable(v)}) if v is not None else json.dumps({"type": kind}))
    width, classes = ecs.message_classes(r.stream.messages)
    for (t, eid, rest), cls in zip(r.stream.messages, classes):
        e = by_eid.get(eid)
        add(t, 6, 0x20, e.uid if e else None, e, rest, name="entity message" if cls is None else f"entity message {cls}",
            fields=json.dumps({"class": cls, "classBits": width}) if cls is not None else None)
    for t, mid, oid, ext, fields, body in r.reflection:
        add(t, 4, mid, None, None, body, name=f"{_REFLECTION.get(mid, '')} {oid >> 11}/{oid & 0x7FF}",
            fields=json.dumps({"object": oid, "ext": ext, **{str(k): v.hex() for k, v in fields.items()}}))
    for t, ptype, mid, payload in r.raw:
        add(t, ptype, mid, None, None, payload[4:] if ptype == 4 and mid is not None else payload)
    order = sorted(range(len(cols["time"])), key=lambda i: cols["time"][i])
    arrays = {k: [v[i] for i in order] for k, v in cols.items()}
    return pa.table({
        "time": pa.array(arrays["time"], pa.float64()),
        "packet": pa.array(arrays["packet"], pa.int8()),
        "message": pa.array(arrays["message"], pa.string()).dictionary_encode(),
        "name": pa.array(arrays["name"], pa.string()).dictionary_encode(),
        "uid": pa.array(arrays["uid"], pa.int16()),
        "eid": pa.array(arrays["eid"], pa.int64()),
        "template": pa.array(arrays["template"], pa.string()).dictionary_encode(),
        "vehicle": pa.array(arrays["vehicle"], pa.string()).dictionary_encode(),
        "fields": pa.array(arrays["fields"], pa.string()),
        "decoded": pa.array(arrays["decoded"], pa.string()),
        "payload": pa.array(arrays["payload"], pa.binary()),
    })


# ---------------------------------------------------------------- the match


def match_name(h: dict[str, Any]) -> str:
    when = datetime.fromtimestamp(h["startTime"], tz=timezone.utc).strftime("%Y-%m-%d_%H-%M-%S") if h.get(
        "startTime") else "unknown"
    return f"{h['map'] or 'unknown'}_{when}_{h['sessionId']}{'_server' if h.get('server') else ''}"


def _rate(all_lives: list[Life], kind: str) -> float | None:
    """Samples per second along the tracks of one kind: the median over lives of at least 10 samples."""
    rates = sorted((len(l.samples) - 1) / (l.end - l.start) for l in all_lives
                   if l.kind == kind and len(l.samples) >= 10 and l.end > l.start)
    return round(rates[len(rates) // 2], 2) if rates else None


#: The recording player's instruments (0xD04A) by number: (name, unit, how it was checked). The numbers are one list
#: for all cockpits (rpm is 93 in a piston fighter and in a jet); a cockpit sends the ones its gauges show. Checked on
#: the I-185 of the air arcade battle and the Eurofighter of the two air simulator battles against what the replay
#: says otherwise: the aircraft's own track (speed, climb, height, attitude, turn), the flight entries (velocity,
#: controls, ammunition), FmwRpm, the weapon preset and the header's start time. "likely": the behaviour fits, nothing
#: independent to check it against.
INSTRUMENTS: dict[int, tuple[str, str, str]] = {
    0: ("ias", "m/s", "indicated airspeed: the track's speed corrected by the ISA air density at its height, "
                      "correlation 0.990, median 1.6 m/s apart (I-185)"),
    23: ("stickElevator", "-1..1", "the stick as the cockpit moves it (its sign differs between cockpits): with the "
                                   "flight entry's elevator 0.70 / -0.61, the angle of attack 0.93 / -0.31 (I-185 / Eurofighter)"),
    31: ("stickAilerons", "-1..1", "with the flight entry's ailerons 0.38 / 0.69, the roll rate 0.65 / 0.66"),
    39: ("vario", "m/s", "climb rate: the track's, correlation 0.9995, median 0.44 m/s apart"),
    40: ("altitude", "m", "the track's height, correlation 1.000, median 3.8 m apart"),
    41: ("altitudeHundreds", "m", "altitude modulo 1000, exactly (the altimeter's small hand)"),
    52: ("horizonRoll", "degrees", "minus the table's roll, median 0.63 degrees apart"),
    53: ("horizonPitch", "degrees", "minus the table's pitch, median 0.16 degrees apart"),
    58: ("slipBall", "-8..8", "likely the slip ball (moves with the side force, correlation -0.25 only)"),
    61: ("turnNeedle", "", "likely the turn needle (with the turn rate 0.44 only)"),
    64: ("compass", "degrees", "the table's heading, median 0.09 degrees apart"),
    69: ("clockHour", "h", "the recording computer's local time, 12-hour dial: the header's start (UTC+1) plus the "
                          "replay time, to the minute"),
    71: ("clockMinute", "min", "as clockHour"),
    73: ("clockSecond", "s", "as clockHour"),
    75: ("manifoldPressure", "atm", "1.55 at war emergency power, 1.29 at 100 % (median, I-185)"),
    135: ("oilTemperature", "C", "likely: rises from 60 to 129 over a sortie (I-185)"),
    159: ("headTemperature", "C", "likely: cylinder heads, rises from 140 to 249 (I-185)"),
    195: ("fuel", "kg", "falls in 2,077 of 2,080 steps, full again at the respawn (I-185); the unit is the gauge's"),
    223: ("airbrake", "0..1", "likely: only on approach (127-141 m/s), with flight-entry nibble 5 (correlation 0.82)"),
}
for _i in range(6):
    INSTRUMENTS[15 + _i] = (f"pedals{_i + 1}", "-1..1", "rudder pedals (all alike): with the side force on the "
                                                        "aircraft 0.84, the flight entry's rudder 0.57 / 0.40")
    INSTRUMENTS[81 + _i] = (f"rpm{_i + 1}", "rpm", f"engine {_i + 1}: equal to instrument {93 + _i}")
    INSTRUMENTS[87 + _i] = (f"rpm{_i + 1}Hundreds", "rpm", f"engine {_i + 1}'s rpm modulo 1000, exactly")
    INSTRUMENTS[93 + _i] = (f"rpm{_i + 1}Gauge", "rpm", f"engine {_i + 1}: FmwRpm (0xD047) correlation 0.973 to 0.996")
for _i in range(3):
    INSTRUMENTS[228 + _i] = (f"gear{_i + 1}", "0..1", "landing gear leg, 1 down: down only at the airfields' height "
                                                      "and under 125 m/s (Eurofighter, 9 spawns and 2 landings)")
    INSTRUMENTS[330 + _i] = (f"ammoCounter{_i + 1}", "rounds", "starts at the weapon preset's count (140, 250, 170 "
                                                              "on the I-185) and falls with the flight entry's ammunition")
    INSTRUMENTS[346 + _i] = (f"ammoCounter{_i + 1}b", "rounds", f"equal to instrument {330 + _i}")
for _i in range(2):
    INSTRUMENTS[240 + _i] = (f"throttle{_i + 1}", "0..1.1", "1.1 war emergency power or afterburner: the flight "
                                                           "entry's throttle 0.74; manifold pressure higher with it")
for _i in list(range(490, 498)) + list(range(500, 506)):
    INSTRUMENTS[_i] = (f"brake{_i - 489}", "0..1", "likely the wheel brakes: set only standing on the airfield "
                                                    "(0-14 m/s), with flight-entry nibble 4 (correlation 0.93)")

#: Columns of the table filled on the recording player's own aircraft from its instruments: column -> instrument.
AUTHOR_COLUMNS = {"ias": 0, "vario": 39, "fuel": 195, "manifoldPressure": 75, "gear": 228, "oilTemperature": 135,
                  "headTemperature": 159}


def _thin(items: list[dict[str, Any]], step: float) -> list[dict[str, Any]]:
    """Every item at least `step` seconds after the one kept before (all of them stay in the messages sidecar)."""
    out, last = [], -1e9
    for x in items:
        if x["t"] - last >= step:
            out.append({"time": x["t"], **{k: v for k, v in x.items() if k != "t"}})
            last = x["t"]
    return out


def _jsonable(v: Any) -> Any:
    if isinstance(v, float):
        return round(v, 6) if math.isfinite(v) else None
    if isinstance(v, dict):
        return {str(k): _jsonable(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_jsonable(x) for x in v]
    if isinstance(v, bytes):
        return v.hex()
    return v


def _travel_check(all_lives: list[Life]) -> dict[str, Any]:
    """Ground units' heading against their direction of travel (moving at 2 m/s or more, samples under 4 s apart)."""
    diffs = []
    for life in all_lives:
        if life.kind != "ground":
            continue
        for a, b in zip(life.samples, life.samples[1:]):
            if not b.angles or b.angles[0] is None or not 0 < b.t - a.t <= 4:
                continue
            dx, dz = b.x - a.x, b.z - a.z
            if math.hypot(dx, dz) / (b.t - a.t) < 2:
                continue
            travel = math.degrees(math.atan2(dx, dz)) % 360
            diffs.append(abs((b.angles[0] - travel + 180) % 360 - 180))
    diffs.sort()
    if not diffs:
        return {}
    return {"samples": len(diffs), "medianDeg": round(diffs[len(diffs) // 2], 2),
            "within10Deg": round(sum(d <= 10 for d in diffs) / len(diffs), 3)}


def _step_speeds(table_rows: list[dict[str, Any]], limits: dict[str, float] | None = None) -> dict[str, Any]:
    """
    Per kind, the speed between consecutive rows of a track as the viewer
    joins them (m/s): median, 99th percentile, highest, and how many steps
    are faster than the kind can go (TOP_SPEED, above the slack).
    """
    tracks: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in table_rows:
        if row["track"]:  # explosions and flak bursts are moments, not tracks
            tracks[row["track"]].append(row)
    by: dict[str, list[float]] = defaultdict(list)
    over: Counter = Counter()
    over_own: Counter = Counter()
    limits = limits or {}
    for track, rs in tracks.items():
        rs.sort(key=lambda row: row["time"])
        kind = rs[0]["kind"]
        dom = "weapon" if kind in ("missile", "rocket", "bomb", "torpedo", "payload", "jettisoned") else (
            "air" if kind in ("aircraft", "helicopter") else "ground")
        for a, b in zip(rs, rs[1:]):
            dt = b["time"] - a["time"]
            if dt <= 1e-3:
                continue
            d = math.dist((a["x"], a["y"], a["z"]), (b["x"], b["y"], b["z"]))
            by[kind].append(d / dt)
            if d > max(SLACK[dom], TOP_SPEED[dom] * dt):
                over[kind] += 1
            if track in limits and d > max(SLACK[dom], limits[track] * dt):
                over_own[kind] += 1
    out = {}
    for k, v in sorted(by.items()):
        v.sort()
        out[k] = {"steps": len(v), "median": round(v[len(v) // 2], 1), "p99": round(v[int(len(v) * 0.99)], 1),
                  "max": round(v[-1], 1), "faster than possible": over[k], "faster than its own limit": over_own[k]}
    return out


def _break_reasons(r: Replay, author_uids: set[int]) -> list[dict[str, Any]]:
    """Each track break with what it most likely is: a respawn or rearm point, the recording player's own aircraft
    moved by the game, or the client correcting a distant unit it had extrapolated."""
    out = []
    for b in r.breaks:
        again = sum(1 for o in r.breaks if o is not b and math.dist(o["to"], b["to"]) < 150)
        if again:
            why = "to a point other breaks also lead to: a respawn or rearm point"
        elif b["uid"] in author_uids:
            why = "the recording player's own aircraft, moved by the game (its own position in the packet moves too)"
        else:
            why = "a distant unit's position corrected after the client had extrapolated it"
        out.append({**b, "speed": round(b["distance"] / max(b["seconds"], 1e-3)), "reason": why})
    return out


def summary(r: Replay, all_lives: list[Life], table_rows: list[dict[str, Any]], check: dict[str, Any],
            all_units: list[Unit] | None = None, all_weapons: list[Weapon] | None = None,
            more: dict[str, Any] | None = None, names: vehicle_names.Names | None = None) -> dict:
    h = r.header
    roster = players(r)
    all_units = all_units or []
    all_weapons = all_weapons or []
    uids: dict[str, set[int]] = defaultdict(set)
    for life in all_lives:
        if life.user_id:
            uids[life.user_id].add(life.uid)
    keys = ("kills", "groundKills", "navalKills", "teamKills", "aiKills", "aiGroundKills", "aiNavalKills",
            "assists", "deaths", "captureZone", "damageZone", "score", "awardDamage", "missileEvades")
    plist = []
    for uid, p in roster.items():
        plist.append({"name": p.get("name", ""), "userId": uid, "team": str(p.get("team", "")),
                      "clanTag": p.get("clanTag", ""), "squad": p.get("squadId"), "country": p.get("country"),
                      "vehicles": p.get("vehicles", []), "uids": sorted(uids.get(uid, ())),
                      **{k: p.get(k) for k in keys if k in p}})
    plist.sort(key=lambda p: (p["team"], -(p.get("score") or 0)))
    lives_by_uid: dict[int, list[Life]] = defaultdict(list)
    for life in all_lives:
        lives_by_uid[life.uid].append(life)

    def who(uid: Any, pid: Any, t: float) -> str:
        return _who(r, lives_by_uid, uid, pid, t)

    kills = []
    for k in r.kills:
        kills.append({"time": round(k["t"], 3), "killer": who(k.get("killerUid"), k.get("killerPid"), k["t"]),
                      "killerVehicle": k.get("killerVehicle", ""), "victim": who(k.get("victimUid"), None, k["t"]),
                      "victimVehicle": (_life_at(lives_by_uid.get(k.get("victimUid"), []), k["t"]) or Life(0, "", 0, [])).vehicle,
                      "weapon": k.get("weapon", ""), "killerUid": k.get("killerUid"),
                      "victimUid": k.get("victimUid"), "crash": k.get("killerUid") == wrpl.NO_UID})
    air = [l for l in all_lives if l.kind == "air"]
    gnd = [l for l in all_lives if l.kind == "ground"]
    events = Counter(row["event"] for row in table_rows)
    start = datetime.fromtimestamp(h["startTime"], tz=timezone.utc).isoformat() if h.get("startTime") else None
    slot_list = [{"pid": pid, **v} for pid, v in sorted(r.slots.items())]
    by_eid = {e.eid: e for e in r.stream.entities}
    unit_list = []
    for u in all_units:
        e = u.entity
        tm = e.comps.get("transform")
        player = u.pid is not None and bool(r.slots.get(u.pid, {}).get("userId"))
        unit_list.append({"eid": e.eid, "uid": u.uid, "template": e.template, "vehicle": u.vehicle,
                          "vehicleName": names.lookup(u.vehicle, _folder(u))[0] if names else "",
                          "kind": u.kind, "type": u.type, "team": u.team, "pid": u.pid, "ai": not player,
                          "player": r.slots.get(u.pid, {}).get("name", "") if u.pid is not None else "",
                          "mission": u.mission, "created": round(e.t, 3),
                          "removed": round(e.destroyed, 3) if e.destroyed is not None else None,
                          "createdAt": tm["pos"] if isinstance(tm, dict) else None,
                          "skippedComponents": e.skipped})
    weapon_list = []
    for w in all_weapons:
        e = w.entity
        weapon_list.append({"eid": e.eid & 0x3FFFFF, "template": e.template, "kind": w.kind, "time": round(e.t, 3),
                            "removed": round(e.destroyed, 3) if e.destroyed is not None else None,
                            "release": w.release, "launcher": _label(w.launcher) if w.launcher else None,
                            "launcherUid": w.launcher.uid if w.launcher else None, "launcherDistance": w.distance,
                            "flightSamples": len(w.track),
                            "lastSeen": [round(v, 2) for v in w.track[-1][1:4]] if w.track else None})
    dists = sorted(w.distance for w in all_weapons if w.distance is not None)
    instruments: dict[str, list] = defaultdict(list)
    last: dict[int, float] = {}
    for t, d in r.cockpit:
        for k, v in d.items():
            if t - last.get(k, -1e9) >= 1.0:
                last[k] = t
                instruments[str(k)].append([round(t, 2), round(v, 4)])
    other = [k for k in r.seen_ids if k not in _READ_IDS]
    return {
        "format": "heat3d-wt-replay-match",
        "version": 2,
        "match": match_name(h),
        "map": h["map"],
        "level": h["level"],
        "mission": h["battleType"],
        "missionKey": h["locName"],
        "battleClass": h["battleClass"],
        "environment": h["environment"],
        "weather": h["visibility"],
        "sessionId": h["sessionId"],
        "server": h["server"],
        "replayVersion": h["version"],
        "flightLayout": r.layout,
        "files": [Path(f).name for f in r.files],
        "started": start,
        "timePlayed": r.results.get("timePlayed"),
        "replayEnd": round(r.end_ms / 1000.0, 3),
        "author": r.results.get("author"),
        "authorUserId": r.results.get("authorUserId"),
        "teams": sorted({p["team"] for p in plist if p["team"]}),
        "settings": _jsonable(r.settings),
        "sky": _jsonable(r.weather[0]) if r.weather else None,
        "players": plist,
        "slots": _jsonable(slot_list),
        "units": unit_list,
        "objects": _jsonable(list(r.objects.values())),
        "kills": kills,
        "hits": [{"time": round(x["t"], 3), "severity": x["severity"],
                  "attacker": who(x.get("uid"), x.get("pid"), x["t"]), "attackerVehicle": x.get("vehicle", ""),
                  "victim": who(x.get("victimUid"), None, x["t"])} for x in r.hits],
        "modulesDestroyed": [{"time": m["t"], "unit": who(m.get("uid"), None, m["t"]), "uid": m.get("uid"),
                              "part": m.get("part")} for m in r.part_kills],
        "weapons": weapon_list,
        "explosions": r.explosions,
        "flak": r.flak,
        "awards": r.awards,
        "detections": [{"time": d["t"], "a": who(d.get("a"), None, d["t"]), "b": who(d.get("b"), None, d["t"])}
                       for d in r.detections],
        "unitStates": [{**s, "unit": who(s.get("uid"), None, s["t"])} for s in r.unit_states],
        "authorInstruments": {"known": {str(k): {"name": v[0], "unit": v[1], "check": v[2]}
                                        for k, v in sorted(INSTRUMENTS.items()) if str(k) in instruments},
                              "notNamed": sorted(int(k) for k in instruments if int(k) not in INSTRUMENTS),
                              "series": dict(instruments)},
        "triggers": [{"time": x["t"], "action": x.get("action", ""), "words": x["words"], "raw": x["raw"]}
                     for x in r.triggers],
        "hints": [{"time": x["t"], "words": x["words"]} for x in r.hints],
        "missionProgress": [{"time": x["t"], **{k: v for k, v in x.items() if k != "t"}} for x in r.progress],
        "camera": _thin(r.camera, 0.25),
        "trackBreaks": _break_reasons(r, {l.uid for l in all_lives if l.user_id and l.user_id == str(r.results.get("authorUserId"))}),
        "chat": [{"time": round(c["t"], 3), "sender": c.get("sender", ""), "text": c.get("text", "")}
                 for c in r.chat],
        "results": _jsonable(r.results),
        "counts": {
            "rows": len(table_rows),
            "events": dict(events),
            "aircraftUids": len({l.uid for l in air}),
            "groundUids": len({l.uid for l in gnd}),
            "lives": len(all_lives),
            "identified": sum(1 for l in all_lives if l.player),
            "withVehicle": sum(1 for l in all_lives if l.vehicle),
            "fromEntities": sum(1 for l in all_lives if l.unit is not None),
            "kinds": dict(Counter(l.figure for l in all_lives)),
            "aircraftSamples": sum(len(l.samples) for l in air),
            "groundSamples": sum(len(l.samples) for l in gnd),
            "aircraftHz": _rate(all_lives, "air"),
            "groundHz": _rate(all_lives, "ground"),
            "entities": len(r.stream.entities),
            "entityTemplates": dict(Counter(e.template for e in r.stream.entities)),
            "replicatedComponents": {f"{k[0]} {k[1]}": n for k, n in Counter(
                ((by_eid[eid].template if eid in by_eid else "?"), comp)
                for _, eid, comp, _, _, _ in r.stream.replications).most_common()},
            "replicatedNotRead": sum(1 for x in r.stream.replications if x[4] is None),
            "entityMessages": len(r.stream.messages),
            "weapons": len(all_weapons),
            "weaponsWithFlight": sum(1 for w in all_weapons if len(w.track) >= 2),
            "packets": dict(r.packets),
            "unreadPackets": dict(r.problems),
            "droppedSamples": dict(r.dropped),
            "messageIds": dict(sorted(r.seen_ids.items())),
            "messageIdsNotRead": {k: r.seen_ids[k] for k in sorted(other)},
        },
        "vehicleNames": {"source": names.source if names else "",
                         "language": vehicle_names.LANGUAGE.strip("<>") if names else "",
                         "note": "read from the game's own localisation in your install when converting; "
                                 "not part of the converter"},
        "selfCheck": {
            **check,
            **(more or {}),
            "weaponLauncherDistanceMedian": dists[len(dists) // 2] if dists else None,
            "weaponsWithLauncher": len(dists),
            "groundHeadingVsTravel": _travel_check(all_lives),
            "packedGroundHeight": r.packed_height,
            "flightPacketsRetimed": r.retimed,
            "aircraftSamplesRetimed": r.releaded,
            "stepSpeed": _step_speeds(table_rows, {_track(l): l.limit for l in all_lives}),
            "trackBreaks": len(r.breaks),
        },
        "conventions": {
            "axes": "metres; x east, y up, z north (the game's own); the table's hints mirror z for the viewer",
            "time": "seconds of the replay's own clock",
            "life": "uid#n: a unit's track, cut where its entity changes, it jumps (respawn) or is long unseen; "
                    "w<hex>: a weapon's flight",
            "track": "what the viewer draws as one thing: '<player or unit> #<hex>', one per life or weapon flight",
            "alive": "0 for samples after a unit's death (its wreck), for at most 60 s or until its entity is removed; "
                     "a ground unit's samples after that are dropped (counts.droppedSamples)",
            "player": "a player's name from the entity stream's player slot, else the kill and hit records; "
                      "AI units '<VehicleName> #<uid>', 'uid <n>' when nothing names it",
            "VehicleName": "the vehicle's full English name from the game's localisation in your install "
                           "(VehicleShortName the short one, VehicleNameKey its key); the vehicle id where the "
                           "game has no name for it or no install was found",
            "ai": "true for every unit no player account drives (mission units, AI aircraft, ground targets, ships, "
                  "AA guns); isPlayer the opposite; for a weapon, its launcher's; empty when unknown",
            "match": "the match id (as 'match' here), on every row",
            "roll": "degrees, right wing down positive (the flight model's own sign is the opposite; checked against "
                    "the recording player's turns, selfCheck.aircraftAttitude)",
            "extrapolated": "an aircraft sample that is the client's dead reckoning (straight on at the last received "
                            "velocity, turning at the last received rates), not a state it received",
            "moved": "how far the smoother moved the sample (m); xRaw/yRaw/zRaw and headingRaw/pitchRaw/rollRaw "
                     "are the replay's own values (roll in the table's sign); selfCheck.deadReckoning",
            "explosion": "rows of explosions (0xD08E) and flak bursts (event flak) at their position, kind 'effect', "
                         "no track",
            "kind": "aircraft, helicopter, tank, apc, spaa, truck, ship, boat, structure; weapons missile, rocket, bomb, "
                    "torpedo, payload, jettisoned",
            "type": "the game's own type where the results name it (fighter, destroyer, gun_boat), else the kind",
            "speed": "m/s over about two seconds of the track (derived, not in the replay)",
            "heading": "compass degrees, clockwise from north",
            "hits": "rows at the position of the unit hit; 'other' is who hit it, 'weapon' their vehicle",
            "module_destroyed": "rows at the unit; 'weapon' the part's number, 'other' who last hit the unit "
                                "within 5 s before (empty when no hit record is that close)",
            "hitLocalX": "shot rows: the hit point on the unit hit, in its own frame as the replay sends it (m; "
                         "hitLocalX forward, hitLocalY up, hitLocalZ right), only where the message's point is in "
                         "that frame; hitDirX/Y/Z the way the shot travelled (shooter to hit point, a unit vector) "
                         "in the same frame, by the unit's attitude at the hit; otherVehicle and otherLife the unit "
                         "hit's vehicle id and life; hitPart the u16 the hit message sends before the point "
                         "(hits with the same number lie together on a vehicle: 1.1 m from their mean point on average "
                         "in the four test replays, against 3.5 m for all of a vehicle's hits; which part it names "
                         "is not known)",
            "launch": "rows at the launcher, the nearest unit within 300 m and 1.5 s of the release point",
            "impact": "a weapon's last sample when its entity was removed within 3 s after it",
            "vx": "vx, vy, vz: an aircraft's velocity as its flight entry sends it (m/s, the game's axes; speeds over "
                  "500 m/s read 500); selfCheck.flightEntries",
            "engine": "off, starting, running, dead (all engines', '/'-joined when they differ); afterburner 0-1; "
                      "engineCondition a byte sent only after the engine was hit",
            "ammo": "the recording player's rounds left per weapon, in its preset's order (everyone's, as last "
                    "refreshed, in the flight sidecar)",
            "throttle": "the recording player's aircraft only: 0-1.1 from its cockpit (1.1 war emergency power or "
                        "afterburner), else the flight entry's fifteenths; elevator, aileron, rudder -1..1 from the "
                        "flight entry (elevator positive pulling, aileron positive rolling right)",
            "ias": "the recording player's own instruments: ias and vario m/s, fuel, manifoldPressure atm, gear 0-1 "
                   "(1 down), oilTemperature, headTemperature; authorInstruments names every instrument",
        },
    }


_REFLECTION = {wrpl.SLOTS: "ReflectionData", wrpl.REDUNDANT_SLOTS: "RedundancyReflectionData"}
#: Replicated object kinds (an object id's top 5 bits) that are read: 14 player slots, 15 teams.
_SLOT_KIND, _TEAM_KIND = 14, 15


def entity_message_classes(r: Replay) -> dict[str, Any]:
    """The entity messages (0x20) by class number (see ecs.message_classes): how many, to which templates, how long."""
    width, classes = ecs.message_classes(r.stream.messages)
    by_eid = {e.eid: e for e in r.stream.entities}
    out: dict[str, dict[str, Any]] = {}
    for (t, eid, rest), cls in zip(r.stream.messages, classes):
        c = out.setdefault(str(cls), {"count": 0, "templates": Counter(), "bytes": Counter(), "first": round(t, 3)})
        c["count"] += 1
        e = by_eid.get(eid)
        c["templates"][e.template if e else ""] += 1
        c["bytes"][len(rest)] += 1
    for c in out.values():
        c["templates"] = dict(c["templates"].most_common(5))
        c["bytes"] = dict(c["bytes"].most_common(5))
    return {"classBits": width, "messages": len(classes),
            "classes": dict(sorted(out.items(), key=lambda kv: -kv[1]["count"]))}


def scoreboard(r: Replay) -> dict[str, Any]:
    """
    The battle's scoreboard over time from the replicated objects (0xF02D,
    0xF0AA; each message carries the fields that changed): per player slot
    its statistics (`wrpl.slot_stats`) each time they change, per team its
    score (field 7, a float: at the end equal to the sum of its players'
    scores in the results, 4 teams of 4 checked), field 3 (u16; likely the
    tickets left: lower for the team that lost more, 0 for the naval
    battle's losing side) and field 2 (u16, not known). Returns the series and
    the check of every player's last values against the results.
    """
    merged: dict[int, dict[int, bytes]] = defaultdict(dict)
    by_slot: dict[int, dict[str, Any]] = {}
    teams: dict[int, list[list]] = defaultdict(list)
    last: dict[int, Any] = {}
    for t, _, oid, _, fields, _ in r.reflection:
        kind, index = oid >> 11, oid & 0x7FF
        if kind not in (_SLOT_KIND, _TEAM_KIND) or not fields:
            continue
        merged[oid].update(fields)
        f = merged[oid]
        if kind == _SLOT_KIND:
            stats = wrpl.slot_stats(f)
            if stats and stats != last.get(oid):
                last[oid] = stats
                slot = by_slot.setdefault(index, {"slot": index, "series": []})
                slot["series"].append({"time": round(t, 3), **stats})
        else:
            score = struct.unpack("<f", f[7][:4])[0] if len(f.get(7, b"")) >= 4 else None
            row = [round(score, 1) if score is not None else None,
                   int.from_bytes(f[3][:2], "little") if len(f.get(3, b"")) >= 2 else None,
                   int.from_bytes(f[2][:2], "little") if len(f.get(2, b"")) >= 2 else None]
            if row != last.get(oid):
                last[oid] = row
                teams[index].append([round(t, 3), *row])
    for index, p in by_slot.items():
        p.update({k: v for k, v in r.slots.get(index, {}).items() if k in ("name", "userId", "team")})
    # The last values against the results.
    results = {p["name"]: {**p, "squad": p.get("squadId")} for p in players(r).values()}
    check: dict[str, list[int]] = {}
    for p in by_slot.values():
        res = results.get(p.get("name", ""))
        if not res or not p["series"]:
            continue
        end = p["series"][-1]
        for k, v in end.items():
            if k == "time" or k not in res:
                continue
            c = check.setdefault(k, [0, 0])
            c[1] += 1
            c[0] += int(v == (res.get(k) or 0))
    return {"players": sorted(by_slot.values(), key=lambda p: p["slot"]),
            "teams": {str(k): v for k, v in sorted(teams.items()) if k},
            "teamColumns": ["time", "score", "ticketsLikely", "field2"],
            "check": {k: f"{a} of {b}" for k, (a, b) in sorted(check.items())}}


#: Message ids this converter reads (the rest is counted under messageIdsNotRead).
_READ_IDS = {"2", "3", "0", "1", "6/0x24", "6/0x25", "6/0x26"} | {
    f"4/{m:#06x}" for m in (wrpl.KILL, wrpl.CRITICAL, wrpl.SEVERE, wrpl.SLOTS, wrpl.REDUNDANT_SLOTS, wrpl.GROUND_CLIENT,
                            wrpl.GROUND_SERVER,
                            wrpl.COCKPIT, wrpl.OBJECTS, *wrpl.SHELLS, *_MORE)} | {
    f"4/unit/{m:#06x}" for m in (0xF0E9, 0xF133, 0xD047, 0xF13E, 0xF031, 0xD041, 0xD0FE, *UNIT_EVENTS)}


def _folder(u: Unit | None) -> str:
    """A unit's folder in the game ("ships", "tankModels"), which some localisation keys carry."""
    return u.entity.class_name.rpartition("/")[0] if u else ""


def name_vehicles(all_lives: list[Life], names: vehicle_names.Names) -> dict[str, Any]:
    """Gives each life its vehicle's names (see names.py). Returns which vehicles the game names and which not."""
    named, unnamed = set(), set()
    for life in all_lives:
        if not life.vehicle or life.vehicle == "dummy_plane":
            continue
        full, short, key = names.lookup(life.vehicle, _folder(life.unit))
        life.vehicle_name, life.vehicle_short, life.vehicle_key = full, short, key
        (named if full else unnamed).add(life.vehicle)
    return {"vehicles": len(named) + len(unnamed), "named": len(named), "notNamed": sorted(unnamed)}


def _identity_check(table_rows: list[dict[str, Any]], roster: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Rows of the results' players against the ai flag (must all be ai false), and the AI ground units and ships."""
    names = {p.get("name") for p in roster.values() if p.get("name")}
    rows_ = [row for row in table_rows if row.get("track") and row.get("uid") is not None]
    of_players = [row for row in rows_ if row["player"] in names]
    ground = [row for row in rows_ if row["kind"] in ("tank", "apc", "spaa", "truck", "ship", "boat", "structure")]
    return {"playerNames": len(names),
            "playerNamesWithRows": len({row["player"] for row in of_players}),
            "rowsOfPlayersAi": sum(1 for row in of_players if row["ai"]),
            "rowsOfPlayersNotAi": sum(1 for row in of_players if not row["ai"]),
            "rowsAiNotAPlayerName": sum(1 for row in rows_ if row["ai"] and row["player"] not in names),
            "rowsNotAiNotAPlayerName": sum(1 for row in rows_ if not row["ai"] and row["player"] not in names),
            "groundAndShipRows": len(ground), "groundAndShipRowsAi": sum(1 for row in ground if row["ai"])}


def _flight_check(r: Replay, all_lives: list[Life], author: str) -> dict[str, Any]:
    """
    The flight entries' decoded fields against what else the replay says: the
    sent velocity against the step between the received samples before and
    after (direction in degrees, speed as a ratio; under 500 m/s), the
    recording player's ammunition against its cockpit counters, and an
    engine "dead" against the kill records and the track's end.
    """
    entries = flight_entries(r)
    out: dict[str, Any] = {}
    for who in ("author", "others"):
        angles: list[float] = []
        ratios: list[float] = []
        for life in all_lives:
            if life.kind != "air" or (who == "author") != (bool(author) and life.user_id == author):
                continue
            ss = life.samples
            for a, b, c in zip(ss, ss[1:], ss[2:]):
                x = entries[b.entry] if 0 <= b.entry < len(entries) else None
                if x is None or a.extrapolated or b.extrapolated or c.extrapolated or not 0 < c.t - a.t < 0.6:
                    continue
                raw_a, raw_c = a.raw or (a.x, a.y, a.z), c.raw or (c.x, c.y, c.z)
                d = [(raw_c[k] - raw_a[k]) / (c.t - a.t) for k in range(3)]
                sd, sv = math.hypot(*d), math.hypot(*x[0])
                if sd < 30 or sv <= 0 or sv >= 499:
                    continue
                cos = sum(d[k] * x[0][k] for k in range(3)) / (sd * sv)
                angles.append(math.degrees(math.acos(max(-1.0, min(1.0, cos)))))
                ratios.append(sv / sd)
        angles.sort()
        ratios.sort()
        out[f"velocity_{who}"] = {
            "samples": len(angles),
            "angleMedian": round(angles[len(angles) // 2], 3) if angles else None,
            "angle90": round(angles[int(len(angles) * 0.9)], 3) if angles else None,
            "speedRatioMedian": round(ratios[len(ratios) // 2], 4) if ratios else None}
    # The recording player's rounds against its cockpit's counters, one tick later.
    counters = [(t, sorted(v for k, v in d.items() if 330 <= k <= 345)) for t, d in r.cockpit]
    counters = [c for c in counters if c[1]]
    times = [c[0] for c in counters]
    same = total = 0
    for life in all_lives:
        if not (author and life.user_id == author and life.kind == "air"):
            continue
        for s in life.samples:
            x = entries[s.entry] if 0 <= s.entry < len(entries) else None
            if x is None or not x[3] or not times:
                continue
            i = bisect.bisect_right(times, s.t + 0.6) - 1
            if i < 0:
                continue
            total += 1
            guns = sorted(x[3])[-len(counters[i][1]):]
            same += guns == [round(v) for v in counters[i][1]]
    out["authorAmmoVsCockpit"] = {"samples": total, "equalOneTickLater": same}
    # An engine "dead": is the aircraft killed, or does its track end, soon after?
    kills: dict[int, list[float]] = defaultdict(list)
    for k in r.kills:
        kills[k.get("victimUid")].append(k["t"])
    dead = Counter()
    for life in all_lives:
        if life.kind != "air":
            continue
        first = next((s.t for s in life.samples if 0 <= s.entry < len(entries) and entries[s.entry]
                      and any(e[0] == 8 for e in entries[s.entry][2])), None)
        if first is None:
            continue
        dead["lives"] += 1
        if any(first - 5 <= t <= life.end + 5 for t in kills.get(life.uid, [])):
            dead["killed"] += 1
        elif life.end - first <= 120:
            dead["trackEndsWithin120s"] += 1
        else:
            dead["fliesOn"] += 1
    out["engineDead"] = dict(dead)
    return out


def _attitude_check(all_lives: list[Life], author: str) -> dict[str, Any]:
    """
    The aircraft attitude against the flight path, on the recording player's
    own aircraft (which the client does not extrapolate): heading against the
    direction of travel, pitch against the climb angle, and in clear turns
    (turning at 6 deg/s or more, banked 20 to 80 deg) whether the roll's sign
    is the turn's (right wing down in a right turn).
    """
    head, pitch, agree, disagree = [], [], 0, 0
    for life in all_lives:
        if life.kind != "air" or not author or life.user_id != author:
            continue
        ss = [s for s in life.samples if life.died is None or s.t <= life.died]
        for a, b, c in zip(ss, ss[1:], ss[2:]):
            if not (0.15 < b.t - a.t < 0.6 and 0.15 < c.t - b.t < 0.6):
                continue
            dx, dy, dz = c.x - a.x, c.y - a.y, c.z - a.z
            hv = math.hypot(dx, dz)
            if hv / (c.t - a.t) < 40:
                continue
            at = _attitude(b)
            if at is None:
                continue
            travel = math.degrees(math.atan2(dx, dz))
            if abs(at[4]) < 60:
                head.append(abs((at[3] - travel + 180) % 360 - 180))
                pitch.append(abs(at[4] - math.degrees(math.atan2(dy, hv))))
            t1 = math.degrees(math.atan2(b.x - a.x, b.z - a.z))
            t2 = math.degrees(math.atan2(c.x - b.x, c.z - b.z))
            rate = ((t2 - t1 + 180) % 360 - 180) / ((c.t - a.t) / 2)
            if abs(rate) >= 6 and 20 <= abs(at[5]) <= 80:
                if (rate > 0) == (at[5] > 0):
                    agree += 1
                else:
                    disagree += 1
    head.sort()
    pitch.sort()
    return {"samples": len(head), "headingVsTravelMedianDeg": round(head[len(head) // 2], 2) if head else None,
            "pitchVsClimbMedianDeg": round(pitch[len(pitch) // 2], 2) if pitch else None,
            "turnsRollRightWingDownAgrees": agree, "turnsRollDisagrees": disagree}


def name_weapons(data: list[dict[str, Any]], arms: vehicle_names.Weapons) -> dict[str, Any]:
    """Kill and death rows' weapon (an ammunition, bomb or missile id) in the install's English (`weaponName`)."""
    named, unnamed = set(), set()
    for row in data:
        if row.get("event") in ("kill", "death") and row.get("weapon"):
            name = arms.lookup(row["weapon"])[0]
            row["weaponName"] = name
            (named if name else unnamed).add(row["weapon"])
    return {"source": arms.source, "named": len(named), "notNamed": sorted(unnamed)}


def _hit_replay(m: UnitMessage, arms: vehicle_names.Weapons) -> dict[str, Any]:
    """0xD0FE: its texts, and the weapon (the text with a blk path) and ammunition (the text after it) named."""
    texts = wrpl.read_projectile_hit_replay(m.body)
    out: dict[str, Any] = {"time": round(m.t, 3), "uid": m.uid, "texts": texts}
    for i, x in enumerate(texts):
        if x.lower().endswith(".blk"):
            out["weapon"] = x.rpartition("/")[2][:-4]
            out["weaponName"], out["weaponShortName"] = arms.lookup(x)
            if i + 1 < len(texts):
                out["ammo"] = texts[i + 1]
                out["ammoName"], out["ammoShortName"] = arms.lookup(texts[i + 1])
            break
    return out


def convert(paths: list[Path], out: Path, game: str | None = None, smoothing: bool = True,
            names: vehicle_names.Names | None = None,
            weapon_names: vehicle_names.Weapons | None = None) -> tuple[Path, Path]:
    """
    One battle's replay file(s) into `<out>/<map>/<match>.parquet` and
    `.match.json`. `game`: the War Thunder folder whose localisation names the
    vehicles (found by itself when not given); `smoothing`: re-place other
    units' dead-reckoned samples and smooth their received ones (see `_smooth`).
    """
    import pyarrow.parquet as pq

    r = read(paths)
    all_units = units(r)
    all_lives = lives(r, all_units)
    roster = players(r)
    check = identify(r, all_lives, roster)
    names = names if names is not None else vehicle_names.load(game)
    more: dict[str, Any] = {"vehicleNames": name_vehicles(all_lives, names)}
    author = str(r.results.get("authorUserId") or "")
    more["deadReckoning"] = smooth(all_lives, author, smoothing)
    more["aircraftAttitude"] = _attitude_check(all_lives, author)
    more["flightEntries"] = _flight_check(r, all_lives, author)
    all_weapons = weapons(r, all_lives)
    msgs = unit_messages(r)
    rpm = rpm_series(msgs)
    extra, more["unitMessages"] = unit_rows(r, msgs, all_lives)
    more["unitMessages"].update(shooters=_shooter_check(r, msgs), deaths=_death_check(r, msgs),
                                rpm=_rpm_check(r, rpm, all_lives),
                                withEntity=sum(1 for m in msgs if m.entity is not None), messages=len(msgs))
    data = rows(r, all_lives, all_weapons, rpm, extra)
    arms = weapon_names if weapon_names is not None else vehicle_names.load_weapons(game)
    more["weaponNames"] = name_weapons(data, arms)
    more["identity"] = _identity_check(data, roster)
    name = match_name(r.header)
    folder = Path(out) / (r.header["map"] or "unknown")
    folder.mkdir(parents=True, exist_ok=True)
    tpath = folder / f"{name}.parquet"
    jpath = folder / f"{name}.match.json"
    pq.write_table(table(data), tpath, compression="snappy", row_group_size=256_000)
    pq.write_table(messages_table(r, msgs), folder / f"{name}.messages.parquet", compression="zstd")
    pq.write_table(flight_table(r), folder / f"{name}.flight.parquet", compression="zstd")
    doc = summary(r, all_lives, data, check, all_units, all_weapons, more, names)
    doc["projectileHitReplays"] = [_hit_replay(m, arms) for m in msgs if m.mid == 0xD0FE]
    doc["scoreboard"] = scoreboard(r)
    doc["entityMessages"] = entity_message_classes(r)
    doc["selfCheck"]["scoreboardVsResults"] = doc["scoreboard"].pop("check")
    for k in doc["kills"]:
        k["weaponName"] = arms.lookup(k.get("weapon") or "")[0]
    jpath.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")
    return tpath, jpath
