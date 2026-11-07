"""
War Thunder replays (.wrpl): every unit's track, who it was, and what happened where.

The game writes a replay of a battle when "save replays" is on (client
replays, `<War Thunder>/Replays/*.wrpl`), and keeps one of every battle on its
servers, in numbered parts (`0000.wrpl`, `0001.wrpl`, ...), downloadable from
warthunder.com's replay pages when signed in. Both are read the same way.

Reading a .wrpl means decoding an undocumented binary file. Gaijin's EULA (3.2.2,
3.2.9) forbids reverse engineering the game and mining data not meant to be
shown; nothing there names replays, which the game itself shows to the player.
That is why this reader is a converter of its own, apart from the 3DHeat
Watcher; see the README.

The layout
----------
Everything here is our own code. What it knows of the format comes from public
notes, not from other parsers' code:

* ShioUmiusi/WTACRP (MIT): docs/REPLAY-FORMAT.md, docs/REPLAY-DECODE.md,
  docs/QUICK-REF.md, and its own parser web/wrpl-parse.js (MIT, read for the
  bit layouts). WTACRP in turn names maxsupermanhd/wrpl-inspector (AGPL-3.0)
  and wt_blk (AGPL-3.0) as its references; neither was read or copied here.
* What the 2025 replays hold where they differ (the flight model's 2025
  layout, the chat line without a flag byte, the zlib stream) was worked out
  here on the public sample replays of llama-for3ver/wt_replay_decoder
  (tests/replays; the files only - that project is AGPL and its code was not
  read).

The file::

    0     u32  magic 0x1000ACE5
    4     u32  version (the game build's replay version, e.g. 101404)
    8     128  level, "levels/<map>.bin"           NUL-terminated text fields
    136   260  level settings (the mission blk)
    396   128  battle type
    524   128  environment ("day")
    652   32   visibility ("cloudy")
    684   u32  results offset (0: none)
    688   u8   difficulty
    724   u32  session type
    732   u64  session id
    740   u8   part number (server replays come in parts)
    744   u32  -
    748   u16  settings size
    780   128  localised mission name key
    908   u32  start time, Unix seconds
    912   u32  time limit, minutes
    916   u32  score limit
    968   128  battle class ("base_dom", ...)
    1096  128  kill streaks
    1226  the settings, settings-size bytes
          the packet stream: 8 bytes, then one zstd frame (2026); or at once
          a zlib stream (2025)
    rez   the results: a binary "FAT" blk to the end of the file

The packet stream is a run of packets, each a length (1 to 5 bytes, the top
bits of the first byte say how many) and a body. The body's first byte is the
packet type; with bit 0x10 set the packet has its predecessor's time and a
2-byte head, else bytes 2..5 are the time in milliseconds (6-byte head).

    type 2  flight model: every aircraft's position, attitude, about 4 per second
    type 3  chat
    type 4  game messages, `kind 0x58 id_lo id_hi` then the message:
            0xF058 kill, 0xF056 critical hit, 0xF157 severe damage,
            0xF073 / 0xF074 ground units' positions (client / server replay),
            0xF02D the player slots (names, teams)
    type 0 / 1  end / start of the battle

A unit is a `uid` of 11 bits (2047 = none), the same in every channel. It is
given to a new unit once its unit is gone. Players are `pid`s, the slot number
of the player slots; a kill or a hit names both the uid and the pid of the one
who dealt it (and a kill its victim's), and that is how tracks get their
player (see convert.py).

Coordinates are the game's own: metres, x east, y up, z north.
"""

from __future__ import annotations

import math
import re
import struct
import zlib
from dataclasses import dataclass
from typing import Any, Callable, Iterator

MAGIC = 0x1000ACE5
HEADER_SIZE = 1226
#: The settings blk is followed by 8 more bytes before the packet stream.
STREAM_GAP = 8
ZSTD_MAGIC = b"\x28\xb5\x2f\xfd"
NO_UID = 0x7FF

KILL = 0xF058
CRITICAL = 0xF056
SEVERE = 0xF157
GROUND_CLIENT = 0xF073
GROUND_SERVER = 0xF074
SLOTS = 0xF02D

#: A track is cut where its unit jumps further than a + b * seconds (m): a
#: reused uid, a respawn. Smaller jumps happen in client replays: a distant
#: aircraft is drawn flying straight on until an update corrects it by a few
#: hundred metres.
JUMP = {"air": (2500.0, 400.0), "ground": (400.0, 40.0)}
#: How far from a sample (s) an event may still take that sample's place.
NEAR = {"air": 2.0, "ground": 12.0}


class FormatError(ValueError):
    """The file is not a replay this reader understands."""


# ---------------------------------------------------------------- bit reading


class Bits:
    """
    Reads a bit stream the way the replay writes it: most significant bit of
    each byte first; multi-byte numbers are bytes in that stream, little-endian.
    """

    __slots__ = ("d", "pos", "n")

    def __init__(self, data: bytes, pos: int = 0) -> None:
        self.d = bytes(data)
        self.pos = pos
        self.n = len(self.d) * 8

    def bits(self, n: int) -> int:
        if n <= 0:
            return 0
        p = self.pos
        end = p + n
        if end > self.n:
            raise EOFError(f"bit {p}+{n} past {self.n}")
        first, last = p >> 3, (end + 7) >> 3
        v = int.from_bytes(self.d[first:last], "big") >> (last * 8 - end)
        self.pos = end
        return v & ((1 << n) - 1)

    def flag(self) -> bool:
        return self.bits(1) == 1

    def byte(self) -> int:
        return self.bits(8)

    def raw(self, count: int) -> bytes:
        if count <= 0:
            return b""
        if not self.pos & 7:
            at = self.pos >> 3
            if at + count > len(self.d):
                raise EOFError(f"{count} bytes past the end")
            self.pos += count * 8
            return self.d[at : at + count]
        return self.bits(count * 8).to_bytes(count, "big")

    def u16(self) -> int:
        return int.from_bytes(self.raw(2), "little")

    def u32(self) -> int:
        return int.from_bytes(self.raw(4), "little")

    def f32(self) -> float:
        return struct.unpack("<f", self.raw(4))[0]

    def uleb(self) -> int:
        """A LEB128 number: 7 bits a byte, low first, the top bit says more follow."""
        v = shift = 0
        for _ in range(10):
            b = self.byte()
            v |= (b & 0x7F) << shift
            shift += 7
            if not b & 0x80:
                return v
        raise FormatError("a variable-length number runs on")

    def zigzag(self) -> int:
        u = self.uleb() & 0xFFFFFFFF
        return (u >> 1) ^ -(u & 1)

    def le_bits(self, n: int) -> int:
        """n bits read a byte's worth at a time, the first group lowest."""
        v = shift = 0
        while n > 0:
            k = min(8, n)
            v |= self.bits(k) << shift
            shift += 8
            n -= k
        return v

    def align(self) -> None:
        self.pos = (self.pos + 7) & ~7

    def skip(self, n: int) -> None:
        if self.pos + n > self.n:
            raise EOFError("skip past the end")
        self.pos += n


def _uleb(buf: bytes, at: int) -> tuple[int, int]:
    v = shift = 0
    while True:
        b = buf[at]
        at += 1
        v |= (b & 0x7F) << shift
        shift += 7
        if not b & 0x80:
            return v, at


def _text(buf: bytes, at: int, size: int) -> str:
    raw = buf[at : at + size].split(b"\0", 1)[0]
    return raw.decode("utf-8", errors="replace")


# ---------------------------------------------------------------- the container


def read_header(buf: bytes) -> dict[str, Any]:
    if len(buf) < HEADER_SIZE or struct.unpack_from("<I", buf, 0)[0] != MAGIC:
        raise FormatError("not a War Thunder replay (no 0x1000ACE5 at the start)")
    u32 = lambda at: struct.unpack_from("<I", buf, at)[0]  # noqa: E731
    level = _text(buf, 8, 128)
    return {
        "version": u32(4),
        "level": level,
        "map": level.rsplit("/", 1)[-1].removesuffix(".bin"),
        "levelSettings": _text(buf, 136, 260),
        "battleType": _text(buf, 396, 128),
        "environment": _text(buf, 524, 128),
        "visibility": _text(buf, 652, 32),
        "resultsOffset": u32(684),
        "difficulty": buf[688],
        "sessionType": u32(724),
        "sessionId": f"{struct.unpack_from('<Q', buf, 732)[0]:016x}",
        "part": buf[740],
        "server": buf[742] == 0x5A,
        "settingsSize": struct.unpack_from("<H", buf, 748)[0],
        "locName": _text(buf, 780, 128),
        "startTime": u32(908),
        "timeLimit": u32(912),
        "scoreLimit": u32(916),
        "battleClass": _text(buf, 968, 128),
        "killStreaks": _text(buf, 1096, 128),
    }


def packet_stream(buf: bytes, header: dict[str, Any]) -> bytes:
    """The packet stream, uncompressed."""
    start = HEADER_SIZE + header["settingsSize"]
    end = header["resultsOffset"] if 0 < header["resultsOffset"] <= len(buf) else len(buf)
    at = buf.find(ZSTD_MAGIC, start, min(end, start + 64))
    if at >= 0:
        try:
            import zstandard
        except ImportError as e:
            raise FormatError("the replay's packets are zstd-compressed: pip install zstandard") from e
        reader = zstandard.ZstdDecompressor().stream_reader(buf[at:end])
        return reader.read()
    for at in range(start, min(end, start + 64)):
        if buf[at] == 0x78 and (buf[at] << 8 | buf[at + 1]) % 31 == 0:
            try:
                return zlib.decompressobj().decompress(buf[at:end])
            except zlib.error:
                continue
    raise FormatError("no compressed packet stream after the settings")


@dataclass
class Packet:
    type: int
    ms: int
    payload: bytes

    @property
    def message(self) -> int | None:
        """A game message's id (type 4): payload `kind 0x58 lo hi`."""
        p = self.payload
        if self.type == 4 and len(p) >= 4 and p[1] == 0x58:
            return p[2] | p[3] << 8
        return None


def packets(data: bytes) -> Iterator[Packet]:
    at, n, last = 0, len(data), 0
    while at < n:
        f = data[at]
        if f & 0x80:
            size, at = f & 0x7F, at + 1
        elif f & 0x40:
            size, at = (int.from_bytes(data[at : at + 2], "big") ^ 0x4000), at + 2
        elif f & 0x20:
            size, at = (int.from_bytes(data[at : at + 3], "big") ^ 0x200000), at + 3
        elif f & 0x10:
            size, at = (int.from_bytes(data[at : at + 4], "big") ^ 0x10000000), at + 4
        else:
            size, at = int.from_bytes(data[at + 1 : at + 5], "little"), at + 5
        if size < 2 or at + size > n:
            return
        body = data[at : at + size]
        at += size
        kind = body[0]
        if kind & 0x10:
            yield Packet(kind ^ 0x10, last, body[2:])
        else:
            if size < 6:
                return
            last = int.from_bytes(body[2:6], "little")
            yield Packet(kind, last, body[6:])


# ---------------------------------------------------------------- binary blk


def read_blk(raw: bytes) -> dict[str, Any]:
    """
    A binary blk of the "FAT" kind (first byte 1): a name table, the values,
    the value table (8 bytes each: name u24, type u8, value or offset u32) and
    the block table (name, value count, child count, first child), the root
    first. A name that repeats in one block becomes a list.
    """
    if not raw or raw[0] != 0x01:
        raise FormatError(f"not a FAT blk (first byte {raw[:1].hex() or 'none'})")
    buf = raw[1:]
    count, at = _uleb(buf, 0)
    size, at = _uleb(buf, at)
    names = buf[at : at + size].split(b"\0")[:count]
    names = [n.decode("utf-8", errors="replace") for n in names]
    at += size
    blocks, at = _uleb(buf, at)
    nparams, at = _uleb(buf, at)
    dsize, at = _uleb(buf, at)
    data = buf[at : at + dsize]
    at += dsize
    table = buf[at : at + nparams * 8]
    at += nparams * 8

    def value(kind: int, v: int) -> Any:
        word = struct.pack("<I", v)
        if kind == 0x01:
            return data[v:].split(b"\0", 1)[0].decode("utf-8", errors="replace")
        if kind == 0x02:
            return struct.unpack("<i", word)[0]
        if kind == 0x03:
            return round(struct.unpack("<f", word)[0], 6)
        if kind == 0x09:
            return v != 0
        if kind == 0x0A:
            return list(word)
        if kind == 0x0C:
            return struct.unpack_from("<q", data, v)[0]
        floats = {0x04: "<2f", 0x05: "<3f", 0x06: "<4f", 0x0B: "<12f", 0x07: "<2i", 0x08: "<3i"}.get(kind)
        if floats:
            return list(struct.unpack_from(floats, data, v))
        return None

    params = []
    for i in range(nparams):
        word = int.from_bytes(table[i * 8 : i * 8 + 3], "little")
        params.append((names[word] if word < len(names) else f"#{word}", value(table[i * 8 + 3], int.from_bytes(table[i * 8 + 4 : i * 8 + 8], "little"))))
    flat = []
    used = 0
    for _ in range(blocks):
        name, at = _uleb(buf, at)
        nvals, at = _uleb(buf, at)
        nkids, at = _uleb(buf, at)
        first = 0
        if nkids:
            first, at = _uleb(buf, at)
        flat.append(("" if name == 0 else names[name - 1] if name - 1 < len(names) else f"#{name}", params[used : used + nvals], first, nkids))
        used += nvals

    def build(i: int, depth: int = 0) -> dict[str, Any]:
        if depth > 64:
            raise FormatError("blk nested too deep")
        _, vals, first, nkids = flat[i]
        out: dict[str, Any] = {}
        repeated: set[str] = set()
        items = [(k, v) for k, v in vals] + [(flat[j][0], build(j, depth + 1)) for j in range(first, first + nkids)]
        for k, v in items:
            if k in out:
                if k not in repeated:
                    out[k] = [out[k]]
                    repeated.add(k)
                out[k].append(v)
            else:
                out[k] = v
        return out

    return build(0) if flat else {}


# ---------------------------------------------------------------- game messages


def id_fields(r: Bits, read: Callable[[int, Bits], None]) -> int:
    """
    The id-field encoding most game messages use: a u16 offset (bytes from the
    start) to a table of field widths, a LEB128 mask of the fields present, then
    the fields, lowest number first. A width is 3 bits - 1, 8, 16, 32, 64, 96,
    128 bits for 1..7 - or, for 0, a LEB128 number of bits. `read(number, r)`
    reads the fields it knows; each field ends where its width says.
    """
    if r.pos & 7:
        raise FormatError("id fields not on a byte boundary")
    start = r.pos
    offset = r.u16()
    mask = r.uleb()
    body = r.pos
    r.pos = start + offset * 8
    widths = []
    for _ in range(bin(mask).count("1")):
        code = r.bits(3)
        widths.append((0, 1, 8, 16, 32, 64, 96, 128)[code] if code else r.uleb())
    r.pos = body
    number = 0
    for width in widths:
        while not mask >> number & 1:
            number += 1
        at = r.pos
        try:
            read(number, r)
        finally:
            r.pos = at + width
        number += 1
    return mask


def _short_text(r: Bits) -> str:
    return r.raw(r.byte()).decode("utf-8", errors="replace")


def read_kill(payload: bytes) -> dict[str, Any]:
    """0xF058: who killed whom. The killer's uid, pid and vehicle, the victim's uid and pid, the weapon."""
    out: dict[str, Any] = {}

    def field(n: int, r: Bits) -> None:
        if n == 1:
            out["killerPid"] = r.u32()
        elif n == 2:
            out["killerVehicle"] = _short_text(r)
        elif n == 3:
            out["victimUid"] = r.u16() & NO_UID
        elif n == 4:
            out["killerUid"] = r.u16() & NO_UID
        elif n == 0xA:
            out["weapon"] = _short_text(r)
        elif n == 0xB:
            out["victimPid"] = r.u32()
        elif n == 0xC:
            out["destroyedWeapon"] = _short_text(r)

    id_fields(Bits(payload[4:]), field)
    return out


def read_damage(payload: bytes) -> dict[str, Any]:
    """0xF056 critical hit / 0xF157 severe damage: the unit hit, and the uid, pid and vehicle of who hit it."""
    out: dict[str, Any] = {}

    def field(n: int, r: Bits) -> None:
        if n == 1:
            out["victimUid"] = r.u16() & NO_UID
        elif n == 2:
            out["pid"] = r.u32()
        elif n == 3:
            out["vehicle"] = _short_text(r)
        elif n == 4:
            out["uid"] = r.u16() & NO_UID

    id_fields(Bits(payload[4:]), field)
    return out


def read_chat(payload: bytes) -> dict[str, Any]:
    """
    Type 3: the sender and the text, each after a length byte; replays from
    2026 put a flag byte first, those of 2025 do not. The reading that uses up
    the packet (up to 16 trailing bytes: 2026 lines end in ten) is taken.
    """
    for at in (1, 0):
        try:
            n = payload[at]
            sender = payload[at + 1 : at + 1 + n].decode("utf-8")
            m = payload[at + 1 + n]
            end = at + 2 + n + m
            text = payload[at + 2 + n : end].decode("utf-8")
        except (IndexError, UnicodeDecodeError):
            continue
        if end <= len(payload) <= end + 16 and sender:
            return {"sender": sender, "text": text}
    raise FormatError("not a chat line")


def read_slots(payload: bytes, decompress: Callable[[bytes], bytes] | None) -> dict[int, dict[str, Any]]:
    """
    0xF02D, the replicated player slots: a compressed flag (then two LEB128
    sizes and a zstd frame), a u16 count of messages, each a u16 length, a u16
    object id and its body. Object ids whose top 5 bits are 0xE are player
    slots, numbered by the low 11 bits; their body is a field table (u16 offset,
    u16 count | index width << 12, the index table just before the width table)
    whose field 2 is the user id (u64) and the name (65 bytes), 9 the team.
    """
    r = Bits(payload[4:])
    if r.byte():
        r.uleb()
        r.uleb()
        if decompress is None:
            return {}
        r = Bits(decompress(payload[4 + (r.pos >> 3) :]))
    out: dict[int, dict[str, Any]] = {}
    for _ in range(r.u16()):
        length = r.u16()
        before = r.pos
        oid = r.u16()
        if oid & 0x7FF == 0x7FF and oid != 0xFFFF:
            r.uleb()
        size = length - ((r.pos - before) >> 3)
        if size < 0:
            raise FormatError("a slot message shorter than its id")
        body = r.raw(size)
        if oid >> 11 == 0xE:
            slot = _slot(body)
            if slot:
                out.setdefault(oid & 0x7FF, {}).update(slot)
    return out


def _slot(body: bytes) -> dict[str, Any]:
    r = Bits(body)
    offset = r.u16()
    count = r.u16()
    fields, width = count & 0xFFF, count >> 12
    if not fields or fields >= 255:
        return {}
    r.pos = offset * 8
    sizes = []
    for _ in range(fields):
        code = r.bits(3)
        sizes.append((0, 1, 8, 16, 32, 64, 96, 128)[code] if code else r.uleb())
    r.pos = offset * 8 - ((width * fields + 7) // 8) * 8
    numbers = [r.le_bits(width) for _ in range(fields)]
    r.pos = 32
    out: dict[str, Any] = {}
    for number, size in zip(numbers, sizes):
        at = r.pos
        try:
            if number == 2:
                out["userId"] = str(r.u32() | r.u32() << 32)
                name = r.raw(65).split(b"\0", 1)[0].decode("utf-8", errors="replace")
                if name:
                    out["name"] = name
            elif number == 9:
                out["team"] = r.byte()
        except EOFError:
            pass
        r.pos = at + size
    return out


# ---------------------------------------------------------------- positions


def _euler(packed: int) -> tuple[float, float, float]:
    """
    The flight model's packed attitude: heading 10 bits, pitch 9, roll 10,
    three sign bits on top; radians. The heading counts from east, the roll
    is positive with the left wing down (see convert._angles, which turns
    both to the table's conventions).
    """
    heading = ((packed >> 19) & 0x3FF) * math.pi / 0x3FF
    pitch = ((packed >> 10) & 0x1FF) * (math.pi / 2) / 0x1FF
    roll = (packed & 0x3FF) * math.pi / 0x3FF
    if packed & 1 << 31:
        heading = -heading
    if packed & 1 << 30:
        pitch = -pitch
    if packed & 1 << 29:
        roll = -roll
    return heading, pitch, roll


#: The flight model's entry layouts. "2026" is the one documented by WTACRP
#: (replay version 101404, autumn 2026); "2025" is what the 2025 replays
#: (versions around 101301) hold: no nested lists, one byte less per engine,
#: no sensors. A file's layout is the one its packets parse with.
FLIGHT_LAYOUTS = {
    "2026": {"nested": True, "engine": 2, "sensors": True},
    "2025": {"nested": False, "engine": 1, "sensors": False},
}


def read_flight(payload: bytes, layout: str = "2026") -> tuple[list[tuple[int, float, float, float, int]], str | None]:
    """
    Type 2, the flight model: a bit-packed list of aircraft. Each entry starts
    with a flag - a new uid (LEB128, 11 bits) follows, or it is the previous
    uid plus one; uid 2047 ends the list. Then: no data (1 bit), two flags that
    together mean "skipped", a flag and a u32, a flag and an optional small
    block, a list of zigzag numbers, the position as three float32 (x east, y
    up, z north), the packed attitude (u32) and a u32; then, from the next byte,
    7 bytes, the engines, sensors, countermeasures, targets and two optional
    tails, whose sizes are all read and skipped. What follows the end of the
    list is not read.

    Returns (uid, x, y, z, attitude) per aircraft with data, and why the list
    stopped early, if it did.
    """
    form = FLIGHT_LAYOUTS[layout]
    r = Bits(payload)
    out = []
    uid = 0
    try:
        while True:
            uid = r.uleb() & NO_UID if r.flag() else uid + 1
            if uid == NO_UID:
                return out, None
            if r.flag():
                continue
            if r.flag() & r.flag():
                continue
            r.bits(1)
            r.u32()
            r.bits(1)
            if r.flag():
                r.bits(3)
                r.bits(r.bits(4))
            for _ in range(_count(r.zigzag(), 4096)):
                r.zigzag()
                if form["nested"]:
                    for _ in range(max(0, r.zigzag())):
                        r.zigzag()
            x, y, z = r.f32(), r.f32(), r.f32()
            attitude = r.u32()
            r.u32()
            r.align()
            r.raw(7)
            _engines(r, form["engine"])
            if form["sensors"] and _sensors(r):
                r.byte()
            n = r.byte()
            r.skip(n * 16)
            if n:
                r.byte()
            _targets(r)
            if r.flag():
                r.skip(32)
            if r.flag():
                r.skip(r.u32())
            out.append((uid, x, y, z, attitude))
    except (EOFError, FormatError) as e:
        return out, str(e)


def flight_layout(payloads: list[bytes]) -> str:
    """The layout most of these flight-model packets parse with to the end of their list."""
    best, score = "2026", -1
    for name in FLIGHT_LAYOUTS:
        ok = sum(1 for p in payloads if read_flight(p, name)[1] is None)
        if ok > score:
            best, score = name, ok
    return best


def _count(n: int, most: int) -> int:
    if n < 0 or n > most:
        raise FormatError(f"a count of {n}")
    return n


def _engines(r: Bits, tail: int) -> None:
    for _ in range(_count(r.byte(), 15)):
        has = r.flag()
        r.byte()
        if has:
            r.u16()
        if r.flag():
            r.byte()
        r.skip(8 * tail)


def _sensors(r: Bits) -> int:
    n = _count(r.byte(), 4)
    for _ in range(n):
        first = r.flag()
        kind = r.byte() >> 4
        if kind == 1:
            if not r.flag():
                continue
            a = r.u16()
            r.skip(32 + 16 * 3)
            if a >= 0x8000:
                r.byte()
            if r.flag():
                r.byte()
        elif kind == 2:
            if not first:
                continue
            r.bits(1)
            r.skip(16 + 24 * 8 + 32)
        elif kind == 3:
            raise FormatError("sensor kind 3")
        elif kind == 4:
            if r.flag():
                r.skip(96)
        if r.flag():
            r.skip(_count(r.bits(6), 63) * 32)
            r.bits(6)
    return n


def _targets(r: Bits) -> None:
    for _ in range(_count(r.bits(4), 8)):
        r.skip(16)
        if r.flag():
            r.skip(96)
        r.skip(96 + 48 if r.flag() else 192)
        r.skip(32 + 2)
        if r.flag():
            r.byte()
        r.bits(1)
        extra = r.flag()
        r.bits(1)
        if extra:
            r.byte()
        if r.flag():
            r.skip(32)


#: Ground position delta history: 32 bodies per unit, by packet number.
HISTORY = 32


def _rle(src: bytes) -> bytes:
    """The ground deltas' 2-bit run-length code; the last byte, 111 or 222, says if the final byte holds one code or two."""
    last = len(src) - 1
    if last < 0 or src[last] not in (111, 222):
        raise FormatError("not a ground delta")
    out = bytearray()
    acc = nbits = 0
    code = keep = -1
    for i in range(last):
        for k in range(1 if (i == last - 1 and src[last] == 111) else 2):
            v0, v1 = (src[i] >> (k * 4)) & 3, (src[i] >> (2 + k * 4)) & 3
            if code != 4:
                code = v0
            if code == 0:
                count, v0, v1 = v1 + 3, 0, 0
            elif code == 3:
                count, v0, v1 = v1 + 7, 0, 0
            elif code == 1:
                code, keep, count, v0 = 4, v1, 1, v1
            elif code == 2:
                count, v0 = 1, v1
            else:
                code, count = -1, 2
                if keep == 0 and v0 == 0 and v1 == 0:
                    count = 39
            for j in range(count):
                acc |= (v0 if j % 2 == 0 else v1) << nbits
                nbits += 2
                if nbits >= 8:
                    out.append(acc & 0xFF)
                    acc >>= 8
                    nbits -= 8
            if len(out) > 65536:
                raise FormatError("ground delta too long")
    if nbits:
        out.append(acc & 0xFF)
    return bytes(out)


def _angle16(v: int) -> float:
    """A 16-bit angle, signed, in degrees."""
    return (v - 65536 if v > 32767 else v) * 360.0 / 65536


def _ground_position(body: bytes, directions: bool) -> tuple[float, ...] | None:
    """
    (x, y, z, heading, pitch, roll, packed) from a ground state; the angles in degrees,
    the heading clockwise from north. The 16-bit attitude is yaw, pitch, roll;
    yaw counts from east like the flight model's, so the compass heading is
    yaw + 90 degrees: checked against the direction of travel of moving ships
    and tanks (median 1.4-2 degrees), and the pitch against the slope they
    drive on (correlation 0.94). Some ships send a quaternion (x, y, z, w)
    instead; its turn about the up axis, 2 atan2(y, w), + 90 degrees is the
    heading (median 2.5 degrees from the direction of travel); pitch and roll
    are then left empty.

    `packed`: the position came in 64 bits (x, z within 36 km in 2^21 steps,
    y in 2^20 steps of 7.6 mm from -100 m). On a level whose ground lies high
    the packed height is not from -100 m: on air_afghan it reads 1505 m low
    against the same units' float positions (spread 8 m over 20 pairs) - the
    level's water level, so the packed height likely counts from it. The
    converter measures the offset on the replay itself (see convert.py).
    """
    r = Bits(body)
    r.byte()
    if not r.flag():
        return None
    heading = pitch = roll = None
    if directions:
        qx, qy, qz, qw = r.f32(), r.f32(), r.f32(), r.f32()
        if abs(math.sqrt(qx * qx + qy * qy + qz * qz + qw * qw) - 1) < 0.02:
            heading = (math.degrees(2 * math.atan2(qy, qw)) + 90.0) % 360.0
        if r.flag():
            r.skip(21 * 32)
    else:
        yaw, p, q = r.u16(), r.u16(), r.u16()
        heading = (yaw * 360.0 / 65536 + 90.0) % 360.0
        pitch, roll = _angle16(p), _angle16(q)
    r.bits(1)
    packed = not r.flag()
    if not packed:
        x, y, z = r.f32(), r.f32(), r.f32()
    else:
        a, b = r.u32(), r.u32()
        x = max(-1.0, min(1.0, (a >> 10) * 4.7683727e-7 - 1)) * 36000
        y = (((a & 0x3FF) << 10) | (b >> 22)) * 0.007629402 - 100
        z = max(-1.0, min(1.0, (b & 0x3FFFFF) * 4.7683727e-7 - 1)) * 36000
    if not all(math.isfinite(v) and abs(v) < 1e6 for v in (x, y, z)):
        return None
    return x, y, z, heading, pitch, roll, packed


class GroundReader:
    """
    0xF073 / 0xF074, ground units' positions in batches: a LEB128 bit length,
    then from the next byte a uid range (u16 from, u16 to), a u32 time and a
    u16 sequence, and for each uid in the range a presence bit and its state.
    A state's body is either whole or the XOR difference to an earlier body of
    the same unit (packet number minus a 5-bit distance), run-length coded; so
    the reader keeps the last 32 bodies of every unit.
    """

    def __init__(self) -> None:
        self.history: dict[int, list[tuple[int, bytes] | None]] = {}

    def read(self, payload: bytes) -> list[tuple[Any, ...]]:
        """(uid, x, y, z, heading, pitch, roll, packed) per unit in the batch; see `_ground_position`."""
        r = Bits(payload[4:])
        length = r.uleb()
        r.align()
        g = Bits(r.raw((length + 7) // 8))
        low, high = g.u16(), g.u16()
        g.u32()
        g.u16()
        if not low < high <= 2048:
            raise FormatError(f"ground uids {low}..{high}")
        out = []
        for uid in range(low, high):
            if not g.flag():
                continue
            g.bits(1)
            if g.flag():
                g.skip(4)
            if g.flag() & g.flag():
                continue
            g.bits(1)
            directions = g.flag()
            turrets = g.byte()
            if not g.flag():
                raise FormatError("an uncompressed ground state")
            whole = g.flag()
            back = g.le_bits(5)
            number = g.le_bits(13)
            size = g.uleb()
            g.align()
            if not 0 < size <= 16384:
                raise FormatError(f"a ground state of {size} bytes")
            packed = g.raw(size)
            slots = self.history.setdefault(uid, [None] * HISTORY)
            if whole:
                body = packed
            else:
                base_no = (number - back) & 0x1FFF
                base = slots[base_no % HISTORY]
                if base is None or base[0] != base_no:
                    raise FormatError(f"uid {uid}: the state this one changes is missing")
                delta = _rle(packed)
                old = base[1]
                n = max(len(old), len(delta))
                body = bytes(
                    (old[i] if i < len(old) else 0) ^ (delta[i] if i < len(delta) else 0) for i in range(n)
                )
            slots[number % HISTORY] = (number & 0x1FFF, body)
            pos = _ground_position(body, directions)
            if pos is not None:
                out.append((uid, *pos))
            if g.flag():
                g.skip(4 * 32)
            if g.flag():
                for _ in range(turrets):
                    if not g.flag():
                        continue
                    g.byte()
                    g.skip(64)
                    g.skip(g.byte() * 16)
            if g.flag() and g.flag():
                g.skip(_count(g.u32(), 1 << 20))
            g.align()
        return out


# ---------------------------------------------------------------- more of the stream

#: Game messages read besides kills, hits, slots and ground positions (names as the community lists them).
COCKPIT = 0xD04A  # ReplayCockpitParams: the recording player's instruments
SHELLS = (0xF0DB, 0xF11A)  # ShellsData (client / server replay): rockets, missiles, bombs, torpedoes in flight
EXPLOSION = 0xD08E  # PlayExplosionVisual
FLAK = 0xD01F  # PlayFlakExplosionVisual
STREAK = 0xF078  # TextStreak: awards
PART_KILL = 0xF118  # UnitDamagePartKill: a module destroyed
DETECTED = 0xF037  # UnitDetected
WEATHER = 0xF0DF  # CustomWeatherParams
OBJECTS = 0xD039  # DeferredReplicatedObjectCreate: the mission's zones, airfields, spawns
UNIT_STATE = 0xF093  # not in the community lists: a unit, its position, attitude and velocity

#: The mission blk starts this many bytes after the header.
SETTINGS_SKIP = 8


def read_settings(buf: bytes) -> dict[str, Any]:
    """The mission settings blk after the header: mode, weather, time of day, date and place of the stars, wind, limits."""
    return read_blk(buf[HEADER_SIZE + SETTINGS_SKIP :])


def fields(payload: bytes) -> dict[int, bytes]:
    """A game message's id fields (see `id_fields`) as raw bytes in the stream's order, by field number."""
    r = Bits(payload[4:])
    start = r.pos
    offset = r.u16()
    mask = r.uleb()
    body = r.pos
    r.pos = start + offset * 8
    widths = []
    for _ in range(bin(mask).count("1")):
        code = r.bits(3)
        widths.append((0, 1, 8, 16, 32, 64, 96, 128)[code] if code else r.uleb())
    r.pos = body
    places = {}
    number = 0
    for width in widths:
        while not mask >> number & 1:
            number += 1
        places[number] = (r.pos, width)
        r.skip(width)
        number += 1
    out: dict[int, bytes] = {}
    for n, (at, width) in places.items():
        r.pos = at
        out[n] = r.bits(width).to_bytes((width + 7) // 8, "big") if width else b""
    return out


def _f3(b: bytes) -> list[float] | None:
    if len(b) < 12:
        return None
    v = struct.unpack_from("<3f", b)
    return [round(x, 3) for x in v] if all(math.isfinite(x) and abs(x) < 1e7 for x in v) else None


def _u16(b: bytes) -> int | None:
    return int.from_bytes(b[:2], "little") if len(b) >= 2 else None


def read_explosion(payload: bytes) -> dict[str, Any] | None:
    """0xD08E: an explosion's position (field 2) and direction (field 4); fields 1 and 3 (its kind) are kept raw."""
    f = fields(payload)
    pos = _f3(f.get(2, b""))
    if pos is None:
        return None
    return {"pos": pos, "dir": _f3(f.get(4, b"")), "kind": f.get(1, b"").hex(), "param": f.get(3, b"").hex()}


def read_flak(payload: bytes) -> dict[str, Any] | None:
    """0xD01F: a flak burst's position (field 1); fields 2 and 3 kept raw."""
    f = fields(payload)
    pos = _f3(f.get(1, b""))
    return None if pos is None else {"pos": pos, "kind": f.get(2, b"").hex(), "param": f.get(3, b"").hex()}


def read_streak(payload: bytes) -> dict[str, Any]:
    """0xF078: an award (field 2, the game's key); fields 1 and 3-5 are numbers (3 counts the award)."""
    f = fields(payload)
    name = f.get(2, b"")

    def num(n: int) -> int | None:
        return int.from_bytes(f[n][:4], "little") if n in f else None

    return {"award": name[1 : 1 + name[0]].decode("utf-8", errors="replace") if name else "", "field1": num(1),
            "count": num(3), "field4": num(4), "field5": num(5)}


def read_part_kill(payload: bytes) -> dict[str, Any]:
    """0xF118: a module destroyed: the unit (field 1) and the part's number in its damage model (field 2)."""
    f = fields(payload)
    uid = _u16(f.get(1, b""))
    return {"uid": None if uid is None else uid & NO_UID, "part": _u16(f.get(2, b""))}


def read_detected(payload: bytes) -> dict[str, Any]:
    """0xF037: fields 1 and 2 are units (the low 11 bits a uid); which saw which is not known."""
    f = fields(payload)
    a, b = _u16(f.get(1, b"")), _u16(f.get(2, b""))
    return {"a": None if a is None else a & NO_UID, "b": None if b is None else b & NO_UID}


def read_unit_state(payload: bytes) -> dict[str, Any] | None:
    """0xF093: a unit (field 1), its position (3), attitude quaternion (4) and velocity (5); what it marks is not known."""
    f = fields(payload)
    uid, pos = _u16(f.get(1, b"")), _f3(f.get(3, b""))
    if uid is None or pos is None:
        return None
    q = f.get(4, b"")
    quat = [round(x, 5) for x in struct.unpack_from("<4f", q)] if len(q) >= 16 else None
    return {"uid": uid & NO_UID, "pos": pos, "quat": quat, "vel": _f3(f.get(5, b"")),
            "field6": f[6][0] if f.get(6) else None}


def read_weather(payload: bytes) -> dict[str, Any] | None:
    """0xF0DF: a blk of the sky - sun and moon direction, wind, colours, cloud offsets, the server's time."""
    for at in range(4, min(len(payload), 24)):
        if payload[at] == 0x01:
            try:
                return read_blk(payload[at:])
            except (FormatError, IndexError, ValueError, struct.error):
                continue
    return None


_OBJECT = re.compile(rb"([-@])([a-zA-Z_][a-zA-Z0-9_./-]{2,63})([-@])([a-zA-Z_][a-zA-Z0-9_./-]{2,63})")
_NAMED = re.compile(rb"([-@])([a-zA-Z_][a-zA-Z0-9_./-]{2,63})([-@])")


def read_objects(payload: bytes) -> list[dict[str, Any]]:
    """
    0xD039: the mission's named objects - capture zones, airfields, spawn areas.
    The message's own layout is not known; two shapes are taken where they
    hold: a name and a model followed by a 4x3 matrix (three axes, each of
    length 0.01 to 100000, then the position), and a name followed by a count
    and that many points (three floats each, within 200 km; an airfield's
    outline). The position of the second is the points' mean.
    """
    out = []
    taken = set()
    for m in _OBJECT.finditer(payload):
        if m.group(1)[0] != len(m.group(2)) or m.group(3)[0] != len(m.group(4)):
            continue
        at = m.end()
        if at + 48 > len(payload):
            continue
        v = struct.unpack_from("<12f", payload, at)
        if not all(math.isfinite(x) and abs(x) < 1e7 for x in v):
            continue
        axes = [v[0:3], v[3:6], v[6:9]]
        size = [math.sqrt(sum(c * c for c in a)) for a in axes]
        if not all(0.01 <= s <= 100_000 for s in size):
            continue
        taken.add(m.start())
        out.append({"name": m.group(2).decode(), "model": m.group(4).decode(), "pos": [round(x, 2) for x in v[9:12]],
                    "size": [round(s, 2) for s in size], "axes": [[round(c, 4) for c in a] for a in axes]})
    for m in _NAMED.finditer(payload):
        if m.start() in taken or m.group(1)[0] != len(m.group(2)):
            continue
        n, at = m.group(3)[0], m.end()
        if at + 12 * n > len(payload):
            continue
        pts = [struct.unpack_from("<3f", payload, at + 12 * i) for i in range(n)]
        if not all(math.isfinite(c) and abs(c) < 200_000 for p in pts for c in p):
            continue
        if not any(abs(p[0]) > 10 or abs(p[2]) > 10 for p in pts):
            continue
        ys = [p[1] for p in pts]
        if max(ys) - min(ys) > 2000:
            continue
        mean = [round(sum(p[i] for p in pts) / n, 2) for i in range(3)]
        out.append({"name": m.group(2).decode(), "pos": mean, "points": [[round(c, 2) for c in p] for p in pts]})
    return out


def read_cockpit(payload: bytes) -> dict[int, float]:
    """
    0xD04A: the recording player's instruments: after the message id a flag
    byte, a 16-bit field (its low byte the count) and that many pairs of a
    16-bit instrument number and a float.
    """
    if len(payload) < 8:
        return {}
    out = {}
    for i in range(payload[6]):
        at = 8 + 6 * i
        if at + 6 > len(payload):
            break
        k, v = struct.unpack_from("<Hf", payload, at)
        if math.isfinite(v):
            out[k] = v
    return out


def _clamp1(v: float) -> float:
    return -1.0 if v < -1 else 1.0 if v > 1 else v


def read_shells(payload: bytes) -> list[tuple[int, int, float, float, float, bool]]:
    """
    0xF0DB / 0xF11A, weapons in flight: a LEB128 bit length, then from the next
    byte three groups (0 rockets and missiles, 1 bombs, 2 torpedoes), each a
    byte count of records. A record: guided (1 bit), no tail (1 bit), the
    entity (u32: its eid index << 10, so the entity stream's creation names
    it), raw (1 bit) and the position, three floats or packed in 64 bits
    (+-15 km), then unless "no tail" a tail whose sizes are read and skipped.
    Returns (group, eid index, x, y, z, guided) per record.
    """
    r = Bits(payload[4:])
    n = r.uleb()
    r.align()
    body = Bits(r.raw((n + 7) // 8))
    out = []
    for group in range(3):
        for _ in range(body.byte()):
            guided, notail = body.flag(), body.flag()
            ent = body.u32()
            if body.flag():
                x, y, z = body.f32(), body.f32(), body.f32()
            else:
                a, b = body.u32(), body.u32()
                x = _clamp1((a >> 10) / 2097152 - 1) * 15000
                y = _clamp1((((a & 0x3FF) << 10) | (b >> 22)) / 524288 - 1) * 15000
                z = _clamp1((b & 0x3FFFFF) / 2097152 - 1) * 15000
            if not notail:
                body.uleb()
                body.skip(3 * 32 + 6 * 16)
                if body.flag():
                    body.skip(16)
                flags = body.byte()
                for f in (1, 2, 4, 8):
                    if flags & f:
                        body.uleb()
                if not guided:
                    body.skip(32 + 1)
                    body.skip(body.u16())
                elif body.flag():
                    raise FormatError("a command-guided weapon's tail")
            if all(math.isfinite(v) and abs(v) < 1e7 for v in (x, y, z)):
                out.append((group, ent >> 10, x, y, z, guided))
    return out
