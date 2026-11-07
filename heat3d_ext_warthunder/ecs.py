"""
War Thunder's entity stream (packet type 6): every networked entity the
replay creates and destroys - each aircraft, tank, ship, fortification and
AI unit with its vehicle, team, player and uid, and each rocket, missile,
bomb, torpedo and drop tank where it was released.

The stream is the Dagor Engine's daECS replication, whose source Gaijin
published under the BSD 3-Clause licence (github.com/GaijinEntertainment/
DagorEngine). What is read here was written from it:

* `prog/engine/daECS/net/network.cpp`: the packet kinds - 0x20 entity message,
  0x22 replication, 0x24 creation, 0x26 destruction, each odd one (0x21, 0x23,
  0x25) the same with its body LZ4-compressed (`compression.h`).
* `prog/engine/daECS/net/connection.cpp`: a creation packet is a count minus
  one, then per entity its server eid (`read_server_eid`: 2, 3 or 4 bytes) and
  a block size; a destruction packet a count minus one and the eids.
* `prog/engine/daECS/net/serialize.cpp` (`serializeConstruction`,
  `deserializeComponentConstruction`, `syncReadTemplate`): a block is the
  template (an index; the first time also its name and its components, each
  an index and, the first time, two 32-bit hashes: the component's name and
  its type), new object-key strings, the number of components written, and
  from the next byte each written component as an index step (8 bits) and
  its value.
* `prog/engine/daECS/core/baseIo.cpp`, `componentTypes.cpp`: plain types are
  written as their bytes, `bool` as one bit, strings NUL-terminated, lists as
  a count (7 bits a byte) and the items, `ecs::Object` as a count and per item
  a key and a typed value.
* The hashes are FNV-1a of the names (`ECS_HASH`). The names below were found
  by hashing the words of the game's own archives; they are the game's
  identifiers, nothing more.

What War Thunder adds and the published source does not describe:

* `TMatrix` (the transform) is 8 bytes of packed rotation and the position
  as three floats; the rotation is not unpacked here.
* The game's own component types (`unit_storage__*`, `dm::PartIdList`,
  `BufferedHudData`, the projectile components) have their own encoders whose
  length is unknown. A unit's block is read past them by trying where the
  next component starts and keeping the reading that uses the rest of the
  block exactly, with the written count; no other reading of a block is taken.
* A projectile's component holds where it was released: three floats, then a
  unit quaternion (|q| = 1), then its velocity. Found by the quaternion and
  checked on real replays: the median release point is 4 to 29 m from the
  nearest aircraft or ship at that moment.

* Replication (0x22, 0x23; `Connection::readReplicationPacket`,
  `Object::deserializeComps`, `deserializeComponentReplication`): the sent
  time (u32), a sequence number (u16), then while a bit is set an entity's
  server eid, a block size (LEB128) and the block: while a bit is set a
  component index (LEB128) and its value, read like a creation's. Checked:
  the sequence numbers run on by one from packet to packet, and every block
  ends where its size says when its values are of known types. A value of
  War Thunder's own types (`BufferedHudData`) ends the block's reading; the
  rest is kept as bytes.
* Entity messages (0x20, 0x21): the target entity's server eid, then a
  message class number whose width and meaning are set at run time; only the
  entity is read.
"""

from __future__ import annotations

import math
import re
import struct
from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from .wrpl import Bits, FormatError


def fnv1a(s: str) -> int:
    h = 0x811C9DC5
    for c in s.encode():
        h = ((h ^ c) * 0x01000193) & 0xFFFFFFFF
    return h


#: Component names of the entities War Thunder replicates (their FNV-1a hashes are what the stream holds).
COMPONENT_NAMES = [
    'active', 'agent_dangers__tag', 'ai_target__noiseLevel', 'aps__rearmState', 'aps__shotCountRemain',
    'aps__timeToReady', 'aps__timeToRearm', 'base_player_id', 'bomb_component', 'buffered_hud_data',
    'canReloadFromBox', 'connid', 'curFrameDt', 'curUnitTickDt', 'damage_area__burnFxSize',
    'damage_area__burnFxType', 'damage_area__damage', 'damage_area__damageTypeId', 'damage_area__emitterCount',
    'damage_area__emitterDispersion', 'damage_area__endTime', 'damage_area__fallNorm', 'damage_area__fallVel',
    'damage_area__flightTime', 'damage_area__fxType', 'damage_area__maxFlightDist', 'damage_area__maxFlightTime',
    'damage_area__maxRise', 'damage_area__move', 'damage_area__pos1', 'damage_area__pos2', 'damage_area__pos2_prev',
    'damage_area__radius', 'damage_area__scorchDuration', 'damage_area__scorchMarginSize',
    'damage_area__scorchStrength', 'damage_area__seed', 'damage_area__vel', 'damage_area__velocityMult',
    'destroy_ri_area__clear_dynamic_ri', 'destroy_ri_area__clear_ri_extra', 'destroy_ri_area__clear_ri_gen',
    'destroy_ri_area__is_forced', 'destroy_ri_area__just_delete', 'destroy_ri_box_area__bbox__bmax',
    'destroy_ri_box_area__bbox__bmin', 'destroy_ri_box_area__itm', 'destroy_ri_sphere_area__pos',
    'destroy_ri_sphere_area__radius', 'editableObj', 'extinguish_system_auto_extinguisher',
    'extinguish_system_cooldown', 'extinguish_system_crew_busy_time', 'extinguish_system_crew_busy_time_end',
    'extinguish_system_extinguish_time_end', 'extinguish_system_extinguish_time_start',
    'extinguish_system_extinguisher_count', 'extinguish_system_extinguisher_count_max',
    'extinguish_system_extinguisher_time_max', 'extinguish_system_extinguisher_time_min',
    'extinguish_system_is_assisting', 'extinguish_system_last_extinguish_time',
    'extinguish_system_next_extinguisher_time', 'extinguish_system_penalty_without_mod',
    'extinguish_system_require_net_sync', 'fire_damage__isBurn', 'fire_damage__nextUpdateTime',
    'fire_damage__offender', 'fire_damage__updateBurnInterval', 'fire_data__extinguishProgress',
    'fire_data__fireParamsId', 'fire_data__initiatorId', 'fire_data__nodeId', 'fire_data__offset',
    'fire_data__packedPartId', 'fire_data__radius', 'fire_data__startTime', 'fire_data__underwaterTimer',
    'fire_fx__fxId', 'fire_fx__id', 'fire_fx__paramsId', 'fire_system_require_net_sync',
    'free_area_check_states_list', 'grid_holder__cellSize', 'grid_holder__smallCellSize', 'grid_holder__type',
    'grid_holder__typeHash', 'grid_obj__fixedTmScale', 'grid_obj__gridType', 'grid_obj__hidden',
    'inflict_specified_damage__awardedOffenders', 'is_local', 'jettisoned_component', 'killerEid', 'modEids',
    'mod__count', 'mod__count_effects_mod', 'mod__enabled_without_mod', 'mod__name', 'mod__ownerEid',
    'mod__send_economic_spend', 'mod__total_count', 'mod__type_name', 'mods', 'move_sys__maxDecel', 'ownedByPlr',
    'payload_component', 'physical_tracks__dontCreateTracks', 'physical_tracks__meshName',
    'physical_tracks__nonSymmetric', 'physical_tracks__trackCount', 'physical_tracks_enabled',
    'player__saved_poi_pos', 'possessed', 'proj__traceHandle', 'proximity_damage__partGlobalId',
    'proximity_damage__parts', 'proximity_damage__pos', 'proximity_damage__visualNum',
    'reloadFromBoxTriggerGroupMask', 'reloadedFromAmmoBoxCount', 'repair_system_auto_check_delay',
    'repair_system_delay_time_to_repair', 'repair_system_parts_hp', 'repair_system_parts_id',
    'repair_system_parts_speed_mult', 'repair_system_parts_state', 'repair_system_remaining_repair_time',
    'repair_system_repair_hp_multiplier', 'repair_system_scheduled_bot_repair_time',
    'repair_system_speed_multiplier', 'repair_system_speed_multiplier_base', 'repair_system_state',
    'repair_system_toolkit_count', 'repair_system_toolkit_count_max', 'repair_system_trailer_repair_progress',
    'repair_system_trailer_repair_time', 'rocket_component', 'server_load_stat__asan', 'server_load_stat__load',
    'server_load_stat__timer', 'ship__pumpsPartId', 'ship__repairBreachesRemainingTime',
    'ship__unwateringRemainingTime', 'ship__waterMassVelMult', 'ship_breaches__amountToRepair',
    'ship_breaches__coverId', 'ship_breaches__depthScale', 'ship_breaches__fatalPartId', 'ship_breaches__id',
    'ship_breaches__leakedAmount', 'ship_breaches__nextCheck', 'ship_breaches__nextId', 'ship_breaches__normal',
    'ship_breaches__partId', 'ship_breaches__pos', 'ship_breaches__size', 'ship_compartments__coverPartsRange',
    'ship_cover_parts__compartmentId', 'ship_cover_parts__disableDeadParts',
    'ship_cover_parts__innerPartsCriticalWater', 'ship_cover_parts__innerPartsId',
    'ship_cover_parts__innerPartsRange', 'ship_cover_parts__partId', 'ship_cover_parts__pos',
    'ship_cover_parts__water', 'ship_cover_parts__weight', 'ship_damage_control__cooldownEndTime',
    'ship_damage_control__cooldownTime', 'ship_damage_control__extinguishSpeedMult',
    'ship_damage_control__isPresetBased', 'ship_damage_control__presets', 'ship_damage_control__priorities',
    'ship_damage_control__repairSpeedMult', 'ship_damage_control__timePenalty',
    'ship_damage_control__unwateringSpeedMult', 'ship_flooding__floodStep', 'ship_flooding__waterLeftSide',
    'ship_flooding__waterRightSide', 'ship_phys_proxy__additionalWater', 'ship_phys_proxy__avgBreachPos',
    'ship_phys_proxy__groundCollision', 'ship_phys_proxy__velocitySq', 'ship_phys_proxy__waterLeaking',
    'ship_repair__partIdx', 'ship_repair__partRemainingTime', 'ship_repair__partsHp', 'ship_repair__partsPartId',
    'ship_repair__partsTime', 'smoke__activate_time', 'smoke__fx_id', 'smoke__fx_time', 'smoke__isExplosionSmoke',
    'smoke__pos', 'smoke__radius', 'smoke__smokeFxName', 'smoke__target_signature_type_flags', 'smoke__time',
    'smoke__transparent_for_thermal', 'supportForPlr', 'tank_engine__commandSent', 'tank_engine__isWorking',
    'tank_engine__overheat', 'tank_engine__soundStarted', 'tank_engine__stage', 'tank_engine__startDelay',
    'tank_engine__startDelayTimer', 'tank_engine__startSoundDelay', 'tank_engine__startSoundDelayTimer',
    'tank_engine__stopDelay', 'tank_engine__stopDelayTimer', 'tank_engine__stopSoundDelay',
    'tank_engine__stopSoundDelayTimer', 'team', 'torpedo_component', 'transform', 'uid', 'unitType', 'unitVersion',
    'unit__canChangeUnitInHangar', 'unit__changedFromEid', 'unit__className', 'unit__forceBailoutTimer',
    'unit__isAlwaysReplicated', 'unit__isReplicated', 'unit__missionName', 'unit__ownsUnitId', 'unit__playerId',
    'unit__reCreateOnRespawn', 'unit__shouldKeepDeadUnit', 'unit__verifyEcsTemplate', 'unit_storage__aircraft',
    'unit_storage__fortification', 'unit_storage__light_vehicle', 'unit_storage__ship', 'unit_storage__tank',
]

NAMES = {fnv1a(n): n for n in COMPONENT_NAMES}

_PLAIN = {
    "int": "<i", "float": "<f", "int8_t": "<b", "uint8_t": "<B", "int16_t": "<h", "uint16_t": "<H", "uint32_t": "<I",
    "int64_t": "<q", "uint64_t": "<Q", "Point2": "<2f", "Point3": "<3f", "Point4": "<4f", "IPoint2": "<2i",
    "IPoint3": "<3i", "IPoint4": "<4i", "DPoint3": "<3d", "BBox3": "<6f", "E3DCOLOR": "<I", "vec4f": "<4f",
    "bbox3f": "<8f", "mat44f": "<16f", "Quat": "<4f",
}
_LISTS = {
    "UInt8List": "uint8_t", "UInt16List": "uint16_t", "UInt32List": "uint32_t", "UInt64List": "uint64_t",
    "StringList": "ecs::string", "EidList": "ecs::EntityId", "FloatList": "float", "Point2List": "Point2",
    "Point3List": "Point3", "Point4List": "Point4", "IPoint2List": "IPoint2", "IPoint3List": "IPoint3",
    "IPoint4List": "IPoint4", "BoolList": "bool", "TMatrixList": "TMatrix", "ColorList": "E3DCOLOR",
    "Int8List": "int8_t", "Int16List": "int16_t", "IntList": "int", "Int64List": "int64_t",
}
#: Type names by hash: the engine's (componentTypes.h) and the game's own, whose encoding is not known.
TYPES = {fnv1a(n): n for n in [*_PLAIN, "bool", "TMatrix", "ecs::string", "ecs::EntityId", "ecs::Object", "ecs::Array",
                               "ecs::Tag", *(f"ecs::{n}" for n in _LISTS)]}
GAME_TYPES = ["dm::PartId", "dm::PartIdList", "BufferedHudData", "Bomb", "Rocket", "Torpedo", "Payload", "Jettisoned"]
TYPES.update({fnv1a(n): n for n in GAME_TYPES})
KNOWN = set(_PLAIN) | {"bool", "TMatrix", "ecs::string", "ecs::EntityId", "ecs::Object", "ecs::Array"} | {
    f"ecs::{n}" for n in _LISTS}

#: Templates of released weapons: their first component says where they were released.
PROJECTILES = {"rocket", "rocket+arh_shell", "bomb", "torpedo", "payload", "jettisoned"}

CREATION, DESTRUCTION = 0x24, 0x26
MESSAGE, REPLICATION = 0x20, 0x22


class Unknown(Exception):
    """A value of a type whose encoding is not known."""


def lz4_block(src: bytes, limit: int = 1 << 24) -> bytes:
    """An LZ4 block (no frame): tokens of literal and match lengths, literals, 16-bit back offsets."""
    out = bytearray()
    s, n = 0, len(src)
    while s < n:
        token = src[s]
        s += 1
        size = token >> 4
        if size == 15:
            while True:
                b = src[s]
                s += 1
                size += b
                if b != 255:
                    break
        out += src[s : s + size]
        s += size
        if s >= n:
            break
        back = src[s] | src[s + 1] << 8
        s += 2
        size = token & 15
        if size == 15:
            while True:
                b = src[s]
                s += 1
                size += b
                if b != 255:
                    break
        size += 4
        start = len(out) - back
        if start < 0 or back == 0:
            raise FormatError("lz4: a match before the start")
        if back >= size:
            out += out[start : start + size]
        else:
            for k in range(size):
                out.append(out[start + k])
        if len(out) > limit:
            raise FormatError("lz4: too long")
    return bytes(out)


def read_eid(r: Bits) -> int:
    """`read_server_eid`: the entity's index (bits 0-21) and generation (bits 22 up)."""
    first = r.u16()
    if first & 1:
        return (first >> 2) | (((first & 2) >> 1) << 22)
    if first & 2:
        return (first >> 2) | ((r.byte() + 2) << 22)
    v = r.u16() << 16 | first
    return ((v >> 2) & 0xFFFFF) | ((v >> 22) << 22)


def _cstr(r: Bits) -> str:
    out = bytearray()
    while True:
        c = r.byte()
        if not c:
            return out.decode("utf-8", errors="replace")
        out.append(c)
        if len(out) > 4096:
            raise FormatError("a string runs on")


def _compressed(r: Bits) -> int:
    v = 0
    for i in range(5):
        b = r.byte()
        v |= (b & 0x7F) << (7 * i)
        if not b & 0x80:
            break
    return v


def _key_no(r: Bits) -> int:
    """An interned key's number: 10 bits written from a little-endian word (a byte, then 2 bits)."""
    return r.bits(8) | r.bits(2) << 8


def value(r: Bits, kind: str, keys: dict[int, str]) -> Any:
    if kind == "bool":
        return r.bits(1) == 1
    if kind == "ecs::EntityId":
        return read_eid(r)
    if kind == "ecs::string":
        return _cstr(r)
    if kind == "TMatrix":
        rot = r.raw(8)
        pos = struct.unpack("<3f", r.raw(12))
        if not rot[0] & 0x80 or not all(math.isfinite(v) and abs(v) < 1e6 for v in pos):
            raise Unknown("TMatrix in another form")
        return {"pos": [round(v, 3) for v in pos], "rot": rot.hex()}
    if kind in _PLAIN:
        f = _PLAIN[kind]
        v = struct.unpack(f, r.raw(struct.calcsize(f)))
        return v[0] if len(v) == 1 else list(v)
    if kind.startswith("ecs::") and kind[5:] in _LISTS:
        n = _compressed(r)
        if n > 100_000:
            raise FormatError("a list too long")
        return [value(r, _LISTS[kind[5:]], keys) for _ in range(n)]
    if kind in ("ecs::Object", "ecs::Array"):
        n = _compressed(r)
        if n > 10_000:
            raise FormatError("an object too big")
        out: Any = {} if kind == "ecs::Object" else []
        for _ in range(n):
            key = (_cstr(r) if r.bits(1) else keys.get(_key_no(r), "?")) if kind == "ecs::Object" else None
            t = struct.unpack("<I", r.raw(4))[0]
            v = value(r, TYPES.get(t, f"{t:#x}"), keys) if t else None
            if key is None:
                out.append(v)
            else:
                out[key] = v
        return out
    raise Unknown(kind)


@dataclass
class Entity:
    eid: int
    template: str
    t: float
    comps: dict[str, Any] = field(default_factory=dict)
    #: Components whose value was skipped (a type of unknown encoding).
    skipped: list[str] = field(default_factory=list)
    #: The first component's bytes, for projectiles.
    blob: bytes = b""
    destroyed: float | None = None

    @property
    def uid(self) -> int | None:
        v = self.comps.get("uid")
        return v if isinstance(v, int) and 0 <= v < 0x7FF else None

    @property
    def class_name(self) -> str:
        v = self.comps.get("unit__className")
        return v if isinstance(v, str) else ""


_NAME = re.compile(rb"[\x00-\x0f]([a-zA-Z][a-zA-Z0-9_/.-]{2,80})\x00")


class Stream:
    """The entity stream of one replay; `feed` each type-6 packet in order."""

    def __init__(self) -> None:
        self.templates: dict[int, tuple[str, list[int]]] = {}
        self.components: dict[int, tuple[int, int]] = {}
        self.keys: dict[int, str] = {}
        self.entities: list[Entity] = []
        self._live: dict[int, Entity] = {}
        self.counts: Counter = Counter()
        self.problems: Counter = Counter()
        #: Component values replicated after creation: (t, eid, component, type, value; None when not read, then the bytes).
        self.replications: list[tuple[float, int, str, str, Any, bytes]] = []
        #: Entity messages: (t, the target's eid, the rest of the packet).
        self.messages: list[tuple[float, int, bytes]] = []

    def feed(self, payload: bytes, t: float) -> None:
        if not payload:
            return
        kind = payload[0]
        self.counts[f"{kind:#04x}"] += 1
        try:
            if kind == CREATION + 1:
                payload = bytes([CREATION]) + lz4_block(payload[1:])
                kind = CREATION
            r = Bits(payload, 8)
            if kind == CREATION:
                for _ in range(r.byte() + 1):
                    eid = read_eid(r)
                    size = r.uleb()
                    self._create(eid, r.raw(size), t)
            elif kind == DESTRUCTION:
                for _ in range(r.byte() + 1):
                    e = self._live.pop(read_eid(r), None)
                    if e is not None and e.destroyed is None:
                        e.destroyed = t
            elif kind in (REPLICATION, REPLICATION + 1):
                self._replication(payload, t)
            elif kind in (MESSAGE, MESSAGE + 1):
                eid = read_eid(r)
                self.messages.append((t, eid, payload[r.pos >> 3 :]))
        except (FormatError, EOFError, IndexError, struct.error) as ex:
            self.problems[f"{kind:#04x}: {type(ex).__name__}"] += 1

    def _replication(self, payload: bytes, t: float) -> None:
        body = payload[1:]
        if payload[0] == REPLICATION + 1:
            body = body[:4] + lz4_block(body[4:])
        r = Bits(body)
        r.u32()  # the time it was sent
        r.u16()  # the sequence number
        while r.flag():
            eid = read_eid(r)
            size = r.uleb()
            block = r.bits(size * 8).to_bytes(size, "big") if size else b""
            b = Bits(block)
            while b.pos < b.n and b.flag():
                cid = _compressed(b)
                if cid not in self.components:
                    self.replications.append((t, eid, f"#{cid}", "?", None, block[b.pos >> 3 :]))
                    break
                name, kind = self._name(cid), self._kind(cid)
                at = b.pos
                try:
                    v = value(b, kind, self.keys)
                except (Unknown, FormatError, EOFError, struct.error):
                    self.replications.append((t, eid, name, kind, None, block[at >> 3 :]))
                    break
                self.replications.append((t, eid, name, kind, v, b""))

    def _template(self, r: Bits) -> tuple[str, list[int]]:
        tid = r.uleb()
        if tid in self.templates:
            return self.templates[tid]
        name = r.raw(r.byte()).decode("utf-8", errors="replace")
        comps = []
        for _ in range(r.u16()):
            cid = r.uleb()
            if cid not in self.components:
                self.components[cid] = (r.u32(), r.u32())
            comps.append(cid)
        self.templates[tid] = (name, comps)
        return name, comps

    def _create(self, eid: int, block: bytes, t: float) -> None:
        r = Bits(block)
        name, comps = self._template(r)
        while True:
            key = _cstr(r)
            if not key:
                break
            self.keys[_key_no(r)] = key
        written = r.byte() if len(comps) < 256 else r.u16()
        r.align()
        e = Entity(eid, name, t)
        if name in PROJECTILES:
            e.blob = block[r.pos >> 3 :]
        elif written:
            unit = any(NAMES.get(self.components[c][0]) in ("uid", "unit__className") for c in comps)
            self._values(block, r.pos, comps, written, e, search=unit)
        self.entities.append(e)
        old = self._live.get(eid)
        if old is not None and old.destroyed is None:
            old.destroyed = t
        self._live[eid] = e

    def _kind(self, cid: int) -> str:
        t = self.components[cid][1]
        return TYPES.get(t, f"{t:#x}")

    def _name(self, cid: int) -> str:
        n = self.components[cid][0]
        return NAMES.get(n, f"{n:#x}")

    def _values(self, block: bytes, pos: int, comps: list[int], written: int, e: Entity, search: bool) -> None:
        r = Bits(block, pos)
        n = len(comps)
        prev = -1
        got = 0
        while got < written:
            try:
                step = r.byte() if n < 256 else _compressed(r)
            except EOFError:
                self.problems["component past the block"] += 1
                return
            idx = step if prev < 0 else prev + step + 1
            if idx >= n:
                self.problems["component index past the template"] += 1
                return
            kind = self._kind(comps[idx])
            at = r.pos
            if kind in KNOWN:
                try:
                    e.comps[self._name(comps[idx])] = value(r, kind, self.keys)
                    prev, got = idx, got + 1
                    continue
                except Unknown:
                    r.pos = at
                except (FormatError, EOFError, struct.error):
                    self.problems["component value"] += 1
                    return
            e.skipped.append(self._name(comps[idx]))
            got += 1
            if got == written or not search:
                return
            tail = self._tail(block, r.pos, comps, idx, written - got)
            if tail is None:
                self.problems[f"{e.template}: no reading past {self._name(comps[idx])}"] += 1
                return
            skipped, values = tail
            e.skipped += skipped
            e.comps.update(values)
            return

    def _tail(self, block: bytes, start: int, comps: list[int], idx: int, need: int):
        """Where the components after an unknown value start: the reading that ends with the block."""
        n = len(comps)
        known = [self._kind(c) in KNOWN for c in comps]
        unknown = [j for j in range(idx + 1, min(n, idx + 9)) if not known[j]]
        cands = []
        for prev in [idx] + unknown:
            between = [j for j in unknown if j <= prev]
            ok = {s for s in range(256) if prev + s + 1 < n and known[prev + s + 1]}
            cands.append((prev, between, ok))
        nbits = len(block) * 8
        big = int.from_bytes(block, "big")
        # Names (the class name, the mission name) anchor the search; then every bit.
        first: list[int] = []
        for sh in range(8):
            shifted = ((big << sh) & ((1 << nbits) - 1)).to_bytes(len(block), "big")
            for m in _NAME.finditer(shifted):
                q = m.start(1) * 8 - sh
                if q > start:
                    first.extend(range(max(start, q - 130), q - 7))
        seen = set(first)
        order = sorted(seen) + [p for p in range(start, nbits - 7) if p not in seen]
        for p in order:
            b = (big >> (nbits - p - 8)) & 0xFF
            for prev, between, ok in cands:
                if b not in ok:
                    continue
                got = self._strict(block, p, comps, prev, need)
                if got is not None and need - len(between) <= len(got) <= need:
                    k = need - len(got)
                    return [self._name(comps[j]) for j in between[:k]], dict(got)
        return None

    def _strict(self, block: bytes, pos: int, comps: list[int], prev: int, limit: int):
        r = Bits(block, pos)
        n = len(comps)
        nbytes = len(block)
        got = []
        while len(got) < limit:
            if r.n - r.pos < 8:
                return None
            step = r.byte() if n < 256 else _compressed(r)
            idx = prev + step + 1
            if idx >= n:
                return None
            kind = self._kind(comps[idx])
            if kind not in KNOWN:
                return None
            try:
                v = value(r, kind, self.keys)
            except (Unknown, FormatError, EOFError, struct.error, UnicodeDecodeError):
                return None
            got.append((self._name(comps[idx]), v))
            prev = idx
            if (r.pos + 7) >> 3 == nbytes:
                return got
        return got if (r.pos + 7) >> 3 == nbytes else None


def release(e: Entity) -> dict[str, Any] | None:
    """A projectile's release point, attitude (quaternion x, y, z, w) and velocity, from its first component."""
    b = e.blob
    for o in range(14, len(b) - 15):
        q = struct.unpack_from("<4f", b, o)
        if not all(abs(v) <= 1.001 for v in q):
            continue
        if not 0.98 < math.sqrt(sum(v * v for v in q)) < 1.02:
            continue
        p = struct.unpack_from("<3f", b, o - 12)
        if not all(math.isfinite(v) and abs(v) < 1e6 for v in p):
            continue
        if max(abs(p[0]), abs(p[2])) < 100 and abs(p[1]) < 100:
            continue  # zeros before the quaternion are not a position
        out = {"pos": [round(v, 2) for v in p], "quat": [round(v, 5) for v in q]}
        if o + 28 <= len(b):
            v = struct.unpack_from("<3f", b, o + 16)
            if all(math.isfinite(x) and abs(x) < 5000 for x in v):
                out["vel"] = [round(x, 2) for x in v]
        return out
    return None
