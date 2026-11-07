"""
Builders for the level-side formats, written to the layouts `vromfs.py`,
`dxp.py` and `dagorlevel.py` document, so the tests need no game files.
"""

from __future__ import annotations

import struct

import numpy as np
import zstandard

from heat3d_ext_warthunder.vromfs import _deobfuscate  # XOR is its own inverse

_HIER = [0, 1, 5, 21, 85, 341, 1365, 5461]


def vromfs(files: dict[str, bytes]) -> bytes:
    names = list(files)
    n = len(names)
    names_at, data_at = 32, 32 + 8 * n
    strings_at = data_at + 16 * n
    body = bytearray(strings_at)
    struct.pack_into("<II", body, 0, names_at, n)
    struct.pack_into("<II", body, 16, data_at, n)
    for i, name in enumerate(names):
        struct.pack_into("<I", body, names_at + 8 * i, len(body))
        body += name.encode("latin1") + b"\0"
    for i, name in enumerate(names):
        while len(body) % 16:
            body.append(0)
        struct.pack_into("<II", body, data_at + 16 * i, len(body), len(files[name]))
        body += files[name]
    packed = _deobfuscate(zstandard.ZstdCompressor().compress(bytes(body)))
    head = struct.pack("<4sIII", b"VRFx", 0x5043, len(body), len(packed) | 0x40000000)
    return head + struct.pack("<HHI", 8, 0, 1) + packed


def _uint(v: int) -> bytes:
    out = bytearray()
    while True:
        b = v & 0x7F
        v >>= 7
        out.append(b | (0x80 if v else 0))
        if not v:
            return bytes(out)


def blk(tree: tuple[str, list[tuple[str, object]], list]) -> bytes:
    """A form-1 binary BLK. `tree` is (name, [(key, value)], [child trees]); values: str, int, float, bool, 2/3-float lists."""
    names: list[str] = []

    def nid(s: str) -> int:
        if s not in names:
            names.append(s)
        return names.index(s)

    order, queue = [], [tree]
    while queue:  # breadth first, as the format stores blocks
        node = queue.pop(0)
        order.append(node)
        queue += node[2]
    pool = bytearray()
    params = bytearray()
    layout = []
    first_child = 1
    for node in order:
        name, ps, kids = node
        for key, v in ps:
            if isinstance(v, bool):
                t, val = 9, int(v)
            elif isinstance(v, int):
                t, val = 2, v & 0xFFFFFFFF
            elif isinstance(v, float):
                t, val = 3, struct.unpack("<I", struct.pack("<f", v))[0]
            elif isinstance(v, str):
                t, val = 1, len(pool)
                pool += v.encode() + b"\0"
            else:
                t = 4 if len(v) == 2 else 5
                val = len(pool)
                pool += struct.pack(f"<{len(v)}f", *v)
            params += struct.pack("<II", nid(key) | (t << 24), val)
        layout.append((nid(name) + 1 if name else 0, len(ps), len(kids), first_child if kids else 0))
        first_child += len(kids)
    raw_names = b"".join(s.encode() + b"\0" for s in names)
    out = bytearray(b"\x01")
    out += _uint(len(names)) + _uint(len(raw_names)) + raw_names
    out += _uint(len(order)) + _uint(len(params) // 8) + _uint(len(pool)) + pool + params
    for n_id, pc, bc, fb in layout:
        out += _uint(n_id) + _uint(pc) + _uint(bc) + (_uint(fb) if bc else b"")
    return bytes(out)


def _block(tag: bytes, payload: bytes, flags: int = 0) -> bytes:
    tag = tag.rjust(4, b"\0")
    return struct.pack("<I", (len(payload) + 4) | (flags << 30)) + tag + payload


def _sub(payload: bytes, flags: int) -> bytes:
    return struct.pack("<I", len(payload) | (flags << 30)) + payload


def heightmap_block(heights_units: np.ndarray, cell: float, hmin: float, hscale: float, ox: float, oz: float) -> bytes:
    """A version-2 HM2 block of 8x8 blocks, one zstd chunk."""
    h, w = heights_units.shape
    shift = 3
    k = 1 << shift
    bw, bh = w // k, h // k
    infos, variance = bytearray(), bytearray()
    for by in range(bh):
        for bx in range(bw):
            blk_ = heights_units[by * k:(by + 1) * k, bx * k:(bx + 1) * k].astype(np.int64).ravel()
            mn, delta = int(blk_.min()), int(blk_.max() - blk_.min())
            infos += struct.pack("<HH", mn, delta)
            v = np.zeros(k * k, np.int64) if delta == 0 else ((blk_ - mn) * 255 + delta // 2) // delta
            stored = np.diff(np.r_[0, v]) & 0xFF
            variance += bytes(stored.astype(np.uint8))
    hrb_shift = 2  # height-range blocks of 4 samples: levels = log2(w / 4)
    levels = (w // (1 << hrb_shift)).bit_length() - 1
    payload = bytes(infos) + bytes(variance) + b"\0" * (_HIER[levels] * 16)
    head = struct.pack("<5f", cell, hmin, hscale, ox, oz)
    head += struct.pack("<2I", w | (2 << 24), h) + struct.pack("<4i", 0, 0, 0, 0)
    head += struct.pack("<I", shift | (hrb_shift << 8))
    return _block(b"HM2", head + _sub(zstandard.ZstdCompressor().compress(payload), 1))


def landmesh_block(verts: np.ndarray, faces: np.ndarray) -> bytes:
    """An lmap block whose land tracer (LTdump, zstd) is one cell holding `verts` and `faces`."""
    lo, hi = verts.min(0), verts.max(0)
    scale = np.where(hi > lo, (hi - lo) / 65535.0, 1.0)
    packed = np.round((verts - lo) / scale).astype(np.uint16)
    rec = struct.pack("<4f4ff3III2I", *lo, 0.0, *scale, 0.0, float(hi[1]), 0, 0, 0, 0, 0, 0, 0)
    lt = b"LTdump" + struct.pack("<iif", 1, 1, 100.0) + struct.pack("<3f", *lo) + struct.pack("<6f", *lo, *hi)
    lt += struct.pack("<i", 1) + rec + struct.pack("<i", 0) + struct.pack("<i", 0)
    lt += struct.pack("<i", faces.size) + faces.astype("<u2").tobytes()
    q = np.zeros((len(verts), 4), np.uint16)
    q[:, :3] = packed
    lt += struct.pack("<i", len(verts)) + q.tobytes()
    ray = zstandard.ZstdCompressor().compress(struct.pack("<i", len(lt)) + lt)
    head = b"lndm" + struct.pack("<iffiiiii", 4, 8.0, 4096.0, 1, 1, 0, 0, 0)
    offsets = struct.pack("<4i", 16, 16, 16, 20)  # mesh, detail, tile, ray tracer (from the offsets' start)
    return _block(b"lmap", head + offsets + _sub(ray, 1))


def level(*blocks: bytes, box=(-100.0, -10.0, -100.0, 100.0, 50.0, 100.0)) -> bytes:
    out = b"DBLD3x64" + struct.pack("<i", 0)
    out += _block(b"eVER", b"\0" * 8)
    for b in blocks:
        out += b
    out += _block(b"WBBX", struct.pack("<6f", *box))
    return out + _block(b"END", b"")


def texture_pack(name: str, rgb: np.ndarray) -> bytes:
    """A version-2 DxP2 pack with one uncompressed A8R8G8B8 texture."""
    h, w, _ = rgb.shape
    bgra = np.concatenate([rgb[:, :, ::-1], np.full((h, w, 1), 255, np.uint8)], 2).tobytes()
    dump = bytearray(48)
    names_at = len(dump)
    dump += b"\0" * 8
    string_at = len(dump)
    dump += (name + "*").encode() + b"\0"
    while len(dump) % 16:
        dump.append(0)
    headers_at = len(dump)
    dump += struct.pack("<4sIIHHBBHHBBII", b"DDSx", 21, 0, w, h, 1, 0, 1, 32, 0, 0, len(bgra), 0)
    records_at = len(dump)
    dump += b"\0" * 24
    struct.pack_into("<I", dump, names_at, string_at)
    struct.pack_into("<II", dump, 0, names_at, 1)
    struct.pack_into("<II", dump, 16, headers_at, 1)
    struct.pack_into("<II", dump, 32, records_at, 1)
    data_at = 16 + len(dump)
    struct.pack_into("<QIiii", dump, records_at, 0, 0xFFFFFFFF, data_at, len(bgra), 0)
    return struct.pack("<4sIII", b"DxP2", 2, 1, len(dump)) + bytes(dump) + bgra


def rigen_block(cell_xz: float, objects: list[tuple[str, int, list]], world0=(0.0, 0.0), ht=(0, 1000), wide=False) -> bytes:
    """A one-cell RIGz block. `objects`: (name, flags, instances); an instance is a 3x4 matrix (rotation and
    position, flags 0) or (x, y, z, scale) (flags 1). Matrices are packed 16-bit, or 32-bit with `wide`."""
    cell_sz, g2w = 64, cell_xz / 64
    n_types = len(objects)
    head = 152
    pool_at = head
    cell_at = pool_at + 32 * n_types
    cnt_at = cell_at + 552
    strings_at = cnt_at + 8 * n_types
    dump = bytearray(strings_at)
    struct.pack_into("<II", dump, 8, cell_at, 1)
    struct.pack_into("<iihBBf", dump, 24, 1, 1, cell_sz, 1, 0, 1.0)
    struct.pack_into("<II", dump, 48, 0, 0)
    struct.pack_into("<4f", dump, 64, world0[0], world0[1], world0[0], world0[1])
    struct.pack_into("<f", dump, 112, g2w)
    struct.pack_into("<II", dump, 128, pool_at, n_types)
    data = bytearray()
    add = np.array([world0[0], ht[0], world0[1]], np.float64)
    mul = np.array([cell_xz, ht[1], cell_xz], np.float64) / 32767.0
    for i, (name, flags, inst) in enumerate(objects):
        struct.pack_into("<I", dump, pool_at + 32 * i + 8, len(dump))
        struct.pack_into("<I", dump, pool_at + 32 * i + 24, flags | 4)  # no per-instance data
        dump += name.encode() + b"\0"
        struct.pack_into("<II", dump, cnt_at + 8 * i, i, len(inst))
        for it in inst:
            if flags & 1:
                x, y, z, s = it
                q = np.round((np.array([x, y, z]) - add) / mul)
                data += struct.pack("<4h", *[int(v) for v in q], int(round(s * 256)))
            else:
                m = np.asarray(it, np.float64)
                t = np.round((m[:, 3] - add) / mul)
                if wide:
                    r = np.round(m[:, :3] * 256 * 65536)
                    data += struct.pack("<12i", *[int(v) for v in np.c_[r, t * 65536].ravel()])
                else:
                    r = np.round(m[:, :3] * 256)
                    data += struct.pack("<12h", *[int(v) for v in np.c_[r, t].ravel()])
    struct.pack_into("<hhi", dump, cell_at + 24, ht[0], ht[1], 0)
    ptrs = [cnt_at] + [cnt_at + 8 * n_types] * 64  # everything in sub-cell 0
    struct.pack_into("<65Q", dump, cell_at + 32, *ptrs)
    first = _sub(zstandard.ZstdCompressor().compress(struct.pack("<i", len(dump)) + bytes(dump)), 1)
    cell = _sub(zstandard.ZstdCompressor().compress(bytes(data)), 1)
    second = _sub(cell, 0)
    return _block(b"RIGz", first + second)


def _leaf(o1: int, o2: int, o3: int, base: int = 0) -> tuple[int, int]:
    w0 = (o1 & 0x1FFF) | ((o2 & 0x1FFF) << 13) | ((o3 & 0x1F) << 26) | (1 << 31)
    w1 = base | (((o3 & 0x1FFF) >> 5) << 24)
    return w0, w1


def collision_resource(box_nodes: list[tuple], quad: np.ndarray | None) -> bytes:
    """A version-3 collision resource: box nodes ((lo, hi), node matrix 4x3) and, optionally, one mesh node
    holding a single quad (four corners, two triangles)."""
    nodes, tms, chunks = [], [], b""
    for (lo, hi), tm in box_nodes:
        nodes.append(struct.pack("<IIHhHHHBB6ff", 0, 0, 0, -1, 0xFFFF, 0, 0, 0, 2, *lo, *hi, 1.0))
        tms.append(np.asarray(tm, np.float32).tobytes())
    if quad is not None:
        lo, hi = quad.min(0), quad.max(0)
        span = np.where(hi > lo, hi - lo, 1.0)
        q = np.round((quad - lo) / span * 65535 * 32).astype(np.uint64)
        packed = q[:, 0] | (q[:, 1] << np.uint64(21)) | (q[:, 2] << np.uint64(42))
        inv = span / 65535
        frame = struct.pack("<9f", *(1 / inv), *inv, *lo)
        head = struct.pack("<4sHBBII6f", b"dBLi", 1, 8, 28, 28, 4, *lo, *hi)
        w0, w1 = _leaf(1, 2, 3)
        tree = bytes([0xFE]) + struct.pack("<II", w0, w1)
        chunks = frame + head + packed.astype("<u8").tobytes() + tree
        nodes.append(struct.pack("<IIHhHHHBB6ff", 0, 6, 0, -1, 0xFFFF, 0, 0, 0, 0, *lo, *hi, 1.0))
        tms.append(np.r_[np.eye(3), np.zeros((1, 3))].astype(np.float32).tobytes())
    n = len(nodes)
    counts = [n, n, 0, 0, len(chunks), 0, 0, 0, 0, 1, 0]
    head = struct.pack("<8f6ffI11I", 0, 0, 0, 1, 0, 0, 0, 1, -1, -1, -1, 1, 1, 1, 1.0, 0, *counts)
    body = head + b"\0" * (8 * n) + b"".join(nodes) + b"".join(tms) + chunks + b"\0"
    return struct.pack("<II", 0xACE50003, len(body)) + body


def grp_pack(resources: dict[str, tuple[int, bytes]]) -> bytes:
    """A GRP2 pack: name -> (class id, data)."""
    names = list(resources)
    desc = bytearray(48)
    names_at = 16 + len(desc)
    desc += b"\0" * (4 * len(names))
    table_at = 16 + len(desc)
    desc += b"\0" * (12 * len(names))
    str_at = []
    for nm in names:
        str_at.append(16 + len(desc))
        desc += nm.encode() + b"\0"
    struct.pack_into("<II", desc, 0, names_at, len(names))
    struct.pack_into("<II", desc, 16, table_at, len(names))
    data_at = 16 + len(desc)
    blobs = b""
    for i, nm in enumerate(names):
        struct.pack_into("<i", desc, names_at - 16 + 4 * i, str_at[i])
        cid, blob = resources[nm]
        struct.pack_into("<IIHH", desc, table_at - 16 + 12 * i, cid, data_at + len(blobs), i, 0)
        blobs += blob
    return struct.pack("<4sIII", b"GRP2", len(desc), len(desc), len(blobs)) + bytes(desc) + blobs


def water_heightmap_block(heights: np.ndarray, extent: float, offset: float, scale: float) -> bytes:
    """A WHM block: a 2x2 grid whose cell (0, 0) points at one page of `heights` (130 x 130 raw), the rest flat."""
    ps = 130
    page = np.asarray(heights, np.uint16).reshape(ps, ps)
    delta = np.diff(np.c_[np.zeros(ps, np.int64), page.astype(np.int64)], axis=1) & 0xFFFF
    grid = np.array([[1, 0xFFFF], [0xFFFF, 0xFFFF]], np.uint16)  # detailed, page (0, 0)
    raw = delta.astype("<u2").tobytes() + grid.astype("<u2").tobytes()
    head = struct.pack("<4i6f", 2, 1, 1, 1, offset, scale, 0.5, 0.5, 1 / extent, 1 / extent)
    return _block(b"WHM", head + _sub(zstandard.ZstdCompressor().compress(raw), 1))
