"""
Small replays built in code, to the layout the reader documents: a header,
a packet stream, a results blk. Nothing here comes from a real replay.
"""

from __future__ import annotations

import math
import struct
import zlib

from heat3d_ext_warthunder import wrpl


class BitWriter:
    def __init__(self) -> None:
        self.out: list[int] = []

    def bits(self, v: int, n: int) -> "BitWriter":
        for i in range(n - 1, -1, -1):
            self.out.append((v >> i) & 1)
        return self

    def flag(self, b: bool) -> "BitWriter":
        return self.bits(1 if b else 0, 1)

    def raw(self, data: bytes) -> "BitWriter":
        for b in data:
            self.bits(b, 8)
        return self

    def u16(self, v: int) -> "BitWriter":
        return self.raw(struct.pack("<H", v))

    def u32(self, v: int) -> "BitWriter":
        return self.raw(struct.pack("<I", v & 0xFFFFFFFF))

    def f32(self, v: float) -> "BitWriter":
        return self.raw(struct.pack("<f", v))

    def uleb(self, v: int) -> "BitWriter":
        return self.raw(uleb(v))

    def align(self) -> "BitWriter":
        while len(self.out) % 8:
            self.out.append(0)
        return self

    def bytes(self) -> bytes:
        self.align()
        return bytes(int("".join(map(str, self.out[i : i + 8])), 2) for i in range(0, len(self.out), 8))


def uleb(v: int) -> bytes:
    out = bytearray()
    while True:
        b = v & 0x7F
        v >>= 7
        out.append(b | (0x80 if v else 0))
        if not v:
            return bytes(out)


def attitude(compass_deg: float, pitch_deg: float = 0.0, roll_deg: float = 0.0) -> int:
    """The packed attitude for a compass heading (the packed heading counts from east)."""
    h = math.radians(compass_deg) - math.pi / 2
    h = (h + math.pi) % (2 * math.pi) - math.pi
    p, r = math.radians(pitch_deg), math.radians(roll_deg)
    v = round(abs(h) * 0x3FF / math.pi) << 19 | round(abs(p) * 0x1FF / (math.pi / 2)) << 10 | round(abs(r) * 0x3FF / math.pi)
    return v | (1 << 31 if h < 0 else 0) | (1 << 30 if p < 0 else 0) | (1 << 29 if r < 0 else 0)


def flight(aircraft: list[tuple[int, float, float, float, int]], layout: str = "2026") -> bytes:
    """A flight-model payload: (uid, x, y, z, attitude) per aircraft."""
    w = BitWriter()
    for uid, x, y, z, att in aircraft:
        w.flag(True).uleb(uid)
        w.flag(False).flag(False).flag(False)  # data; not skipped
        w.flag(False).u32(0).flag(False).flag(False)  # unknowns, no small block
        w.uleb(0)  # no zigzag list
        w.f32(x).f32(y).f32(z).u32(att).u32(0).align()
        w.raw(bytes(7))
        w.raw(b"\x01").flag(False).raw(b"\x00").flag(False).raw(bytes(2 if layout == "2026" else 1))  # one engine
        if layout == "2026":
            w.raw(b"\x00")  # no sensors
        w.raw(b"\x00")  # no countermeasures
        w.bits(0, 4).flag(False).flag(False)  # no targets, no tails
    w.flag(True).uleb(wrpl.NO_UID)
    return w.bytes()


def id_fields(fields: dict[int, tuple[int, bytes | int]]) -> bytes:
    """An id-field body: {number: (width in bits, value)}; bytes values are written as they are."""
    head = BitWriter()
    mask = sum(1 << n for n in fields)
    data = BitWriter()
    for n in sorted(fields):
        width, value = fields[n]
        data.raw(value) if isinstance(value, bytes) else data.bits(value, width)
    body = data.bytes()
    head_len = 2 + len(uleb(mask))
    widths = BitWriter()
    codes = {1: 1, 8: 2, 16: 3, 32: 4, 64: 5, 96: 6, 128: 7}
    for n in sorted(fields):
        width = fields[n][0]
        if width in codes:
            widths.bits(codes[width], 3)
        else:
            widths.bits(0, 3).uleb(width)
    return head.u16(head_len + len(body)).uleb(mask).bytes() + body + widths.bytes()


def text(s: str) -> bytes:
    b = s.encode()
    return bytes([len(b)]) + b


def le(v: int, n: int) -> bytes:
    return v.to_bytes(n, "little")


def kill(killer_uid: int, killer_pid: int, vehicle: str, victim_uid: int, victim_pid: int, weapon: str) -> bytes:
    body = id_fields({
        1: (32, le(killer_pid, 4)),
        2: (8 + 8 * len(vehicle), text(vehicle)),
        3: (16, le(victim_uid, 2)),
        4: (16, le(killer_uid, 2)),
        0xA: (8 + 8 * len(weapon), text(weapon)),
        0xB: (32, le(victim_pid, 4)),
    })
    return b"\x02\x58" + le(wrpl.KILL, 2) + body


def damage(victim_uid: int, uid: int, pid: int, vehicle: str, severe: bool = False) -> bytes:
    body = id_fields({
        1: (16, le(victim_uid, 2)),
        2: (32, le(pid, 4)),
        3: (8 + 8 * len(vehicle), text(vehicle)),
        4: (16, le(uid, 2)),
    })
    return b"\x02\x58" + le(wrpl.SEVERE if severe else wrpl.CRITICAL, 2) + body


def slot_body(user_id: int, name: str, team: int) -> bytes:
    data = BitWriter().u16(0).u16(0)  # offset and count, patched below
    data.u32(user_id & 0xFFFFFFFF).u32(user_id >> 32).raw(name.encode().ljust(65, b"\0")).raw(bytes([team]))
    body = bytearray(data.bytes())
    index = BitWriter().bits(2, 6).bits(9, 6).bytes()
    offset = len(body) + len(index)
    widths = BitWriter().bits(0, 3).uleb(64 + 65 * 8).bits(2, 3).bytes()
    body[0:2] = le(offset, 2)
    body[2:4] = le(2 | 6 << 12, 2)
    return bytes(body) + index + widths


def slots(players: dict[int, tuple[int, str, int]]) -> bytes:
    """An uncompressed player-slot payload: {slot: (user id, name, team)}."""
    out = bytearray(b"\x02\x58" + le(wrpl.SLOTS, 2) + b"\x00" + le(len(players), 2))
    for slot, (user_id, name, team) in players.items():
        body = slot_body(user_id, name, team)
        out += le(len(body) + 2, 2) + le(0xE << 11 | slot, 2) + body
    return bytes(out)


def ground(units: dict[int, tuple[float, float, float]] | None, number: int, delta: set[int] = frozenset(),
           message: int = wrpl.GROUND_CLIENT) -> bytes:
    """A ground batch: whole states with float positions, or (uids in `delta`) an unchanged delta to the last one."""
    uids = sorted(units)
    g = BitWriter().u16(uids[0]).u16(uids[-1] + 1).u32(0).u16(number)
    for uid in range(uids[0], uids[-1] + 1):
        if uid not in units:
            g.flag(False)
            continue
        g.flag(True).flag(False).flag(False).flag(False).flag(False).flag(False)
        g.flag(False).raw(b"\x00").flag(True)  # no directions, no turrets, compressed
        if uid in delta:
            g.flag(False).bits(1, 5)  # a change to the previous packet's state
            body = bytes([0b00001100, 111])  # six zero codes: nothing changed
        else:
            g.flag(True).bits(0, 5)
            x, y, z = units[uid]
            body = BitWriter().raw(b"\x00").flag(True).bits(0, 48).flag(False).flag(True).f32(x).f32(y).f32(z).bytes()
        g.bits(number & 0xFF, 8).bits(number >> 8, 5).uleb(len(body)).align().raw(body)
        g.flag(False).flag(False).flag(False).align()
    payload = g.bytes()
    return b"\x02\x58" + le(message, 2) + BitWriter().uleb(len(payload) * 8).bytes() + payload


def chat(sender: str, line: str, flag: bool = True) -> bytes:
    return (b"\x00" if flag else b"") + text(sender) + text(line) + b"\x00\x00"


def blk(tree: dict) -> bytes:
    """A FAT binary blk of nested dicts; a list of dicts is a repeated block."""
    names: list[str] = []

    def name(n: str) -> int:
        if n not in names:
            names.append(n)
        return names.index(n)

    data = bytearray()
    params: list[bytes] = []
    flat: list[list] = [["", tree, 0, 0, 0]]  # name, node, first child, children, values
    i = 0
    while i < len(flat):
        node = flat[i][1]
        kids = []
        values = 0
        for k, v in node.items():
            if isinstance(v, dict):
                kids.append([k, v])
            elif isinstance(v, list):
                kids += [[k, x] for x in v]
            else:
                values += 1
                nid = name(k)
                if isinstance(v, bool):
                    kind, word = 0x09, int(v)
                elif isinstance(v, int):
                    kind, word = 0x02, v & 0xFFFFFFFF
                elif isinstance(v, float):
                    kind, word = 0x03, struct.unpack("<I", struct.pack("<f", v))[0]
                else:
                    kind, word = 0x01, len(data)
                    data += str(v).encode() + b"\0"
                params.append(le(nid, 3) + bytes([kind]) + le(word, 4))
        flat[i][2], flat[i][3], flat[i][4] = len(flat), len(kids), values
        for k, v in kids:
            name(k)
            flat.append([k, v, 0, 0, 0])
        i += 1
    table = b"".join(params)
    out = bytearray(b"\x01")
    raw = b"".join(n.encode() + b"\0" for n in names)
    out += uleb(len(names)) + uleb(len(raw)) + raw
    out += uleb(len(flat)) + uleb(len(params)) + uleb(len(data)) + data + table
    for n, _, first, kids, values in flat:
        out += uleb(0 if not n else names.index(n) + 1) + uleb(values) + uleb(kids)
        if kids:
            out += uleb(first)
    return bytes(out)


def packet(kind: int, ms: int | None, payload: bytes) -> bytes:
    body = (bytes([kind | 0x10, 0]) if ms is None else bytes([kind, 0]) + le(ms, 4)) + payload
    n = len(body)
    if n < 0x80:
        size = bytes([0x80 | n])
    elif n < 0x4000:
        size = (n | 0x4000).to_bytes(2, "big")
    elif n < 0x200000:
        size = (n | 0x200000).to_bytes(3, "big")
    else:
        size = (n | 0x10000000).to_bytes(4, "big")
    return size + body


def header(level: str = "levels/avg_test_land.bin", session: int = 0x1234ABCD, start: int = 1793000000,
           server: bool = False, part: int = 0) -> bytearray:
    h = bytearray(wrpl.HEADER_SIZE)
    struct.pack_into("<II", h, 0, wrpl.MAGIC, 101404)
    for at, size, value in ((8, 128, level), (136, 260, "gamedata/missions/test.blk"), (396, 128, "test_Dom"),
                            (524, 128, "day"), (652, 32, "clear"), (780, 128, "missions/test"),
                            (968, 128, "base_dom")):
        h[at : at + len(value)] = value.encode()
    struct.pack_into("<Q", h, 732, session)
    h[740] = part
    h[742] = 0x5A if server else 0
    struct.pack_into("<III", h, 908, start, 25, 10000)
    return h


def replay(packets: list[bytes], results: dict | None = None, compress: str = "zstd", **kw) -> bytes:
    stream = b"".join(packets)
    if compress == "zstd":
        import zstandard

        packed = bytes(wrpl.STREAM_GAP) + zstandard.ZstdCompressor().compress(stream)
    else:
        packed = zlib.compress(stream)
    h = header(**kw)
    body = bytes(h) + packed
    if results is not None:
        struct.pack_into("<I", h, 684, len(body))
        body = bytes(h) + packed + blk(results)
    return body


# ---------------------------------------------------------------- the entity stream (packet type 6)

def eid(index: int) -> bytes:
    """A short server eid (generation 0 or 1 in its 2-byte form)."""
    return le(index << 2 | 1, 2)


def template(tid: int, name: str, comps: list[tuple[int, str, str]]) -> bytes:
    """A template the first time: its index, name and components (index, name, type), each with its two hashes."""
    from heat3d_ext_warthunder.ecs import fnv1a

    out = BitWriter().uleb(tid).raw(text(name)).u16(len(comps))
    for cid, cname, ctype in comps:
        out.uleb(cid).u32(fnv1a(cname)).u32(fnv1a(ctype))
    return out.bytes()


def construction(head: bytes, entries: list[tuple[int, bytes | BitWriter]]) -> bytes:
    """A creation block: the template, no new keys, the count, then (index step, value) per written component."""
    body = BitWriter().raw(head).raw(b"\x00").raw(bytes([len(entries)])).align()
    for step, value in entries:
        body.raw(bytes([step]))
        if isinstance(value, BitWriter):
            body.out += value.out
        else:
            body.raw(value)
    return body.bytes()


def creation(blocks: list[tuple[int, bytes]], compress: bool = False) -> bytes:
    """A creation packet: the count less one, then per entity its eid, block size and block."""
    body = bytes([len(blocks) - 1]) + b"".join(eid(i) + uleb(len(b)) + b for i, b in blocks)
    if not compress:
        return b"\x24" + body
    return b"\x25" + lz4_literals(body)


def destruction(indexes: list[int]) -> bytes:
    return b"\x26" + bytes([len(indexes) - 1]) + b"".join(eid(i) for i in indexes)


def lz4_literals(data: bytes) -> bytes:
    """An LZ4 block of one literal run (a valid block: the last sequence has literals only)."""
    n = len(data)
    out = bytearray([(15 if n >= 15 else n) << 4])
    if n >= 15:
        k = n - 15
        while k >= 255:
            out.append(255)
            k -= 255
        out.append(k)
    return bytes(out) + data


def tmatrix(x: float, y: float, z: float) -> bytes:
    return b"\x80" + bytes(7) + struct.pack("<3f", x, y, z)


def projectile_blob(pos: tuple[float, float, float], quat: tuple[float, ...], vel: tuple[float, float, float]) -> bytes:
    return bytes(range(1, 15)) + struct.pack("<3f", *pos) + struct.pack("<4f", *quat) + struct.pack("<3f", *vel) + bytes(8)


def shells(records: list[tuple[int, int, float, float, float]]) -> bytes:
    """A weapons-in-flight payload: (group, eid index, x, y, z) per record, raw floats, no tails."""
    body = BitWriter()
    for group in range(3):
        mine = [r for r in records if r[0] == group]
        body.raw(bytes([len(mine)]))
        for _, index, x, y, z in mine:
            body.flag(True).flag(True).u32(index << 10 | 2).flag(True).f32(x).f32(y).f32(z)
    payload = body.bytes()
    return b"\x02\x58" + le(0xF0DB, 2) + BitWriter().uleb(len(payload) * 8).bytes() + payload
