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

from . import ecs, wrpl

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
        "lookMode": "vector",
        "dirX": "dirX",
        "dirY": "dirY",
        "dirZ": "dirZ",
        "extra": ["event", "player", "life", "Vehicle", "kind", "type", "uid", "other", "weapon", "heading", "pitch",
                  "roll", "speed", "alive", "mission"],
    },
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
    ("mission", "str"),
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

    @property
    def id(self) -> str:
        return f"{self.uid}#{self.n}"

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
    #: Every message id seen, by "type" or "type/0xid" (ff-family by its first bytes), for the record of what is read.
    seen_ids: Counter = field(default_factory=Counter)


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
}


def _id_key(pk: wrpl.Packet) -> str:
    p = pk.payload
    if pk.type == 4 and pk.message is not None:
        return f"4/{pk.message:#06x}"
    if pk.type == 4 and len(p) >= 7 and p[0] == 0xFF:
        # Unit-addressed messages: ff, a flag byte, a length or flag byte, an object (2 bytes), the message id.
        return f"4/ff{p[1]:02x}/{p[5] | p[6] << 8:#06x}"
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
                entries, err = wrpl.read_flight(pk.payload, r.layout or "2026")
                if err:
                    # A list that does not parse to its end is not trusted at all.
                    problems["flight"] += 1
                    entries = []
                frames.append((t, [Sample(t, x, y, z, att, uid=uid) for uid, x, y, z, att in entries
                                   if _plausible(x, y, z)]))
            elif pk.type == 3:
                try:
                    r.chat.append({"t": t, **wrpl.read_chat(pk.payload)})
                except wrpl.FormatError:
                    problems["chat"] += 1
            elif pk.type == 6:
                seen["entity"] += 1
                r.stream.feed(pk.payload, t)
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
                except (wrpl.FormatError, EOFError, IndexError, ValueError, struct.error):
                    problems[name] += 1
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
        runs: list[tuple[Unit | None, list[Sample]]] = []
        for s in samples:
            u = owner(s.t)
            if runs and runs[-1][0] is u:
                p = runs[-1][1][-1]
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


def _split_own(run: list[Sample], kind: str, uid: int, r: Replay, limit: float) -> list[list[Sample]]:
    """A run cut again where it steps faster than its unit's own limit (`_own_limit`); the cuts go to `r.breaks`."""
    if len(run) < 2:
        return [run]
    for s in run:
        s.limit = limit
    pieces: list[list[Sample]] = [[run[0]]]
    for s in run[1:]:
        p = pieces[-1][-1]
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
    does (see `_retime`): it lies ahead along the flight path by 0.3 s or
    more, and the next sample carries on from the one before it. Such a
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
        if lead < RETIME_MIN_SHIFT:
            continue
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
    """A player's name; an AI unit by its vehicle and uid (the viewer shows "#<n>" as an id, not in the name)."""
    if life.player:
        return life.player
    if life.vehicle and life.vehicle != "dummy_plane":
        return f"{life.vehicle} #{life.uid}"
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
        return Sample(t, a.x + (b.x - a.x) * f, a.y + (b.y - a.y) * f, a.z + (b.z - a.z) * f, a.attitude, a.angles)
    return a


# ---------------------------------------------------------------- the table


def _attitude(s: Sample) -> tuple[float, ...] | None:
    """
    Compass heading, pitch and roll (degrees) and the look vector in the game's
    axes. The flight model's packed heading is counted from east: compass =
    heading + 90 deg (checked against the direction of travel on real replays);
    a ground state's angles are already compass, pitch, roll.
    """
    if s.attitude is not None:
        h, p, roll = wrpl._euler(s.attitude)
        compass = h + math.pi / 2
    elif s.angles is not None and s.angles[0] is not None:
        compass, p, roll = math.radians(s.angles[0]), math.radians(s.angles[1] or 0.0), math.radians(s.angles[2] or 0.0)
    else:
        return None
    cp = math.cos(p)
    return (math.sin(compass) * cp, math.sin(p), math.cos(compass) * cp,
            math.degrees(compass) % 360, math.degrees(p), math.degrees(roll))


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
    base = life.player or (life.vehicle if life.vehicle and life.vehicle != "dummy_plane" else f"uid {life.uid}")
    return f"{base} #{life.uid * 4096 + min(life.n, 4095):x}"


def _row(life: Life, s: Sample, event: str) -> dict[str, Any]:
    return {"time": s.t, "event": event, "track": _track(life), "player": _label(life), "userId": life.user_id, "team": life.team,
            "life": life.id, "uid": life.uid, "kind": life.figure, "type": life.type, "Vehicle": life.vehicle,
            "x": s.x, "y": s.y, "z": s.z, "mission": life.unit.mission if life.unit else ""}


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


def rows(r: Replay, all_lives: list[Life], all_weapons: list[Weapon] | None = None) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    by_uid: dict[int, list[Life]] = defaultdict(list)
    for life in all_lives:
        by_uid[life.uid].append(life)
        until = life.wreck_until()
        for s, v in zip(life.samples, _speeds(life.samples)):
            row = _row(life, s, "position")
            row["speed"] = v
            row["alive"] = 0.0 if until is not None and life.died < s.t <= until else 1.0
            a = _attitude(s)
            if a:
                row.update(dirX=a[0], dirY=a[1], dirZ=a[2], heading=a[3], pitch=a[4], roll=a[5])
            out.append(row)

    def at(uid: int | None, t: float) -> tuple[Life | None, Sample | None]:
        if uid is None or uid == wrpl.NO_UID:
            return None, None
        life = _life_at(by_uid.get(uid, []), t)
        return life, _at_time(life, t)

    for k in r.kills:
        killer, ks = at(k.get("killerUid"), k["t"])
        victim, vs = at(k.get("victimUid"), k["t"])
        names = (_label(killer) if killer else _uid_label(k.get("killerUid")),
                 _label(victim) if victim else _uid_label(k.get("victimUid")))
        for event, life, s, other in (("kill", killer, ks, names[1]), ("death", victim, vs, names[0])):
            if s is None or life is None:
                continue
            out.append({**_row(life, s, event), "time": k["t"], "other": other, "weapon": k.get("weapon", "")})
    for h in r.hits:
        victim, vs = at(h.get("victimUid"), h["t"])
        if vs is None or victim is None:
            continue
        attacker, _ = at(h.get("uid"), h["t"])
        out.append({**_row(victim, vs, f"hit_{h['severity']}"), "time": h["t"],
                    "other": _label(attacker) if attacker else _uid_label(h.get("uid")), "weapon": h.get("vehicle", "")})
    for m in r.part_kills:
        victim, vs = at(m.get("uid"), m["t"])
        if vs is None or victim is None:
            continue
        out.append({**_row(victim, vs, "module_destroyed"), "time": m["t"], "other": f"part {m.get('part')}"})
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
                       "z": p.z, "speed": v, "alive": 1.0, "other": owner}
                nxt = pts[i + 1] if i + 1 < len(pts) else pts[i - 1]
                d = (nxt.x - p.x, nxt.y - p.y, nxt.z - p.z) if i + 1 < len(pts) else (p.x - nxt.x, p.y - nxt.y, p.z - nxt.z)
                n = math.sqrt(sum(c * c for c in d))
                if n > 0:
                    row.update(dirX=d[0] / n, dirY=d[1] / n, dirZ=d[2] / n,
                               heading=math.degrees(math.atan2(d[0], d[2])) % 360,
                               pitch=math.degrees(math.asin(max(-1.0, min(1.0, d[1] / n)))))
                out.append(row)
    out.sort(key=lambda row: row["time"])
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


#: The recording player's instruments (0xD04A) that were checked against the replay's own track.
INSTRUMENTS = {
    40: "altitude, m (the author's track height: ratio 1.0007, correlation 0.999 in an air battle)",
    64: "compass heading, degrees (the author's track heading: correlation 0.95)",
}


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
            all_units: list[Unit] | None = None, all_weapons: list[Weapon] | None = None) -> dict:
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
        life = _life_at(lives_by_uid.get(uid, []), t) if uid not in (None, wrpl.NO_UID) else None
        if life:
            return _label(life)
        pid = _pid(pid)
        # 0 is also what units no player drives get; only another pid names someone.
        if pid and r.slots.get(pid, {}).get("name"):
            return r.slots[pid]["name"]
        return _uid_label(uid)

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
    unit_list = []
    for u in all_units:
        e = u.entity
        tm = e.comps.get("transform")
        unit_list.append({"eid": e.eid, "uid": u.uid, "template": e.template, "vehicle": u.vehicle, "kind": u.kind,
                          "type": u.type, "team": u.team, "pid": u.pid,
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
        "authorInstruments": {"known": {str(k): v for k, v in INSTRUMENTS.items()}, "series": dict(instruments)},
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
            "weapons": len(all_weapons),
            "weaponsWithFlight": sum(1 for w in all_weapons if len(w.track) >= 2),
            "packets": dict(r.packets),
            "unreadPackets": dict(r.problems),
            "droppedSamples": dict(r.dropped),
            "messageIds": dict(sorted(r.seen_ids.items())),
            "messageIdsNotRead": {k: r.seen_ids[k] for k in sorted(other)},
        },
        "selfCheck": {
            **check,
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
                      "AI units '<vehicle> #<uid>', 'uid <n>' when nothing names it",
            "kind": "aircraft, helicopter, tank, apc, spaa, truck, ship, boat, structure; weapons missile, rocket, bomb, "
                    "torpedo, payload, jettisoned",
            "type": "the game's own type where the results name it (fighter, destroyer, gun_boat), else the kind",
            "speed": "m/s over about two seconds of the track (derived, not in the replay)",
            "heading": "compass degrees, clockwise from north",
            "hits": "rows at the position of the unit hit; 'other' is who hit it, 'weapon' their vehicle",
            "launch": "rows at the launcher, the nearest unit within 300 m and 1.5 s of the release point",
            "impact": "a weapon's last sample when its entity was removed within 3 s after it",
        },
    }


#: Message ids this converter reads (the rest is counted under messageIdsNotRead).
_READ_IDS = {"2", "3", "0", "1", "6/0x24", "6/0x25", "6/0x26"} | {
    f"4/{m:#06x}" for m in (wrpl.KILL, wrpl.CRITICAL, wrpl.SEVERE, wrpl.SLOTS, wrpl.GROUND_CLIENT, wrpl.GROUND_SERVER,
                            wrpl.COCKPIT, wrpl.OBJECTS, *wrpl.SHELLS, *_MORE)}


def convert(paths: list[Path], out: Path) -> tuple[Path, Path]:
    """One battle's replay file(s) into `<out>/<map>/<match>.parquet` and `.match.json`."""
    import pyarrow.parquet as pq

    r = read(paths)
    all_units = units(r)
    all_lives = lives(r, all_units)
    check = identify(r, all_lives, players(r))
    all_weapons = weapons(r, all_lives)
    data = rows(r, all_lives, all_weapons)
    name = match_name(r.header)
    folder = Path(out) / (r.header["map"] or "unknown")
    folder.mkdir(parents=True, exist_ok=True)
    tpath = folder / f"{name}.parquet"
    jpath = folder / f"{name}.match.json"
    pq.write_table(table(data), tpath, compression="snappy", row_group_size=256_000)
    doc = summary(r, all_lives, data, check, all_units, all_weapons)
    jpath.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")
    return tpath, jpath
