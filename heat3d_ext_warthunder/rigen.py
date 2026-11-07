"""
Placed objects of a War Thunder level: the render-instance generator's fixed
("pregen") instances in the level binary's `RIGz` block.

Written from the Dagor Engine's BSD-3-Clause source:
`prog/gameLibs/rendInst/riGen/riGenData.h` (the dump: `RendInstGenData` and
its `Cell`, `PregenEntPoolDesc`, `PregenEntCounter` records, 64-bit patchable
pointers stored as offsets into the dump), `prog/gameLibs/rendInst/rendInstGen.cpp`
(`RendInstGenData::create`, and the per-cell unpacking in `generateCell`: a
block per cell, zstd or LZMA, instances by sub-cell in counter order) and
`prog/gameLibs/rendInst/riGen/genObjUtil.h` (`unpack_tm_full`, `unpack_tm_pos`:
a 3x4 matrix of 16-bit values (rotation / 256) or, in some levels, 32-bit ones (`unpack_tm32_full`,
rotation / 2^24), translation scaled into the cell;
or a position with a scale for objects placed without rotation).

What is read: every fixed instance, with its object name and transform. What is
not: the instances the land classes generate at run time from masks and rules
(most forests and fields on air maps); those need the land-class assets and the
generator, and are listed only by name.
"""

from __future__ import annotations

import lzma
import struct
from dataclasses import dataclass, field

import numpy as np

from . import oodle
from .dagorlevel import Block, LevelError

_CELL = 552  # PatchableTab cls (16) + cellRtData (8) + htMin, htDelta (4) + riDataRelOfs (4) + 65 entCnt pointers (520)
_POOL = 32  # PregenEntPoolDesc
_SUBCELLS = 64
PALETTE_ID_BITS = 3


@dataclass
class Placed:
    """Every fixed instance of one object type."""

    name: str
    matrices: list[np.ndarray] = field(default_factory=list)  # (n, 3, 4) float32 blocks: [R | t] in game space


def _unpack_block(data: bytes, p: int) -> tuple[bytes, int]:
    """One Dagor block at `p` (32-bit length with the compression in its top bits): its decoded bytes and its end."""
    (word,) = struct.unpack_from("<I", data, p)
    fmt, n, a = word >> 30, word & 0x3FFFFFFF, p + 4
    body = data[a : a + n]
    if fmt == 2:
        (src,) = struct.unpack_from("<i", body, 0)
        return oodle.decompress(body[4:], src), a + n
    if fmt == 1:
        import zstandard

        return zstandard.ZstdDecompressor().decompressobj().decompress(body), a + n
    # 0: the 7-zip LZMA stream: 5 property bytes, then raw LZMA1 data.
    props = body[0]
    pb, rest = divmod(props, 45)
    lp, lc = divmod(rest, 9)
    (dict_size,) = struct.unpack_from("<I", body, 1)
    dec = lzma.LZMADecompressor(lzma.FORMAT_RAW, filters=[{"id": lzma.FILTER_LZMA1, "lc": lc, "lp": lp, "pb": pb,
                                                            "dict_size": dict_size}])
    return dec.decompress(body[5:]), a + n


def _str(dump: bytes, ofs: int) -> str:
    return dump[ofs : dump.index(b"\0", ofs)].decode("latin1")


@dataclass
class RiGen:
    names: list[str]
    flags: list[int]  # per type: bit 0 position-only, bit 1 palette rotation, bit 2 no per-instance data
    land_classes: list[str]
    placed: dict[str, Placed]
    counts: dict[str, int]


def read_rigen(data: bytes, block: Block) -> RiGen:
    dump_raw, p2 = _unpack_block(data, block.start)
    (dsz,) = struct.unpack_from("<i", dump_raw, 0)
    dump = dump_raw[4 : 4 + dsz]
    cells_at, n_cells = struct.unpack_from("<II", dump, 8)
    cw, ch = struct.unpack_from("<ii", dump, 24)
    (cell_sz,) = struct.unpack_from("<h", dump, 32)
    dflags, per_inst = dump[34], dump[35]
    lc_at, n_lc = struct.unpack_from("<II", dump, 48)
    wx, wz = struct.unpack_from("<2f", dump, 64)
    (g2w,) = struct.unpack_from("<f", dump, 112)
    pool_at, n_pool = struct.unpack_from("<II", dump, 128)
    if not dflags & 1:
        raise LevelError("RIGz with old-style counters is not read")
    names, flags = [], []
    for i in range(n_pool):
        r = pool_at + _POOL * i
        (name_ofs,) = struct.unpack_from("<I", dump, r + 8)
        (bits,) = struct.unpack_from("<I", dump, r + 24)
        names.append(_str(dump, name_ofs))
        flags.append(bits & 7)
    land = [_str(dump, struct.unpack_from("<I", dump, lc_at + 32 * i)[0]) for i in range(n_lc)]
    # The second block holds the per-cell instance data; offsets are from its start.
    (word,) = struct.unpack_from("<I", data, p2)
    base = p2 + 4
    cell_xz = cell_sz * g2w
    placed: dict[str, Placed] = {}
    counts: dict[str, int] = {}
    for ci in range(n_cells):
        c = cells_at + _CELL * ci
        ht_min, ht_delta = struct.unpack_from("<hh", dump, c + 24)
        (rel,) = struct.unpack_from("<i", dump, c + 28)
        ptrs = [q & 0xFFFFFFFF for q in struct.unpack_from("<65Q", dump, c + 32)]
        entries = []
        for s in range(_SUBCELLS):
            for q in range(ptrs[s], ptrs[s + 1], 8):
                entries.append(struct.unpack_from("<II", dump, q))
        if rel < 0 or not entries:
            continue
        raw, _ = _unpack_block(data, base + rel)
        x, z = ci % cw, ci // cw
        add = np.array([wx + x * cell_xz, ht_min, wz + z * cell_xz], np.float32)
        mul = np.array([cell_xz, ht_delta or 8192, cell_xz], np.float32) / 32767.0
        # Matrices are 12 16-bit values in some levels and 12 32-bit values in others (the engine's
        # tmInst12x32bit); the cell's byte count says which.
        def size(wide: bool) -> int:
            total = 0
            for idx, cnt in entries:
                f = flags[idx]
                total += cnt * ((8 if f & 1 else (48 if wide else 24)) + (0 if f & 4 else 4 * per_inst))
            return total

        if size(False) == len(raw):
            wide = False
        elif size(True) == len(raw):
            wide = True
        else:
            raise LevelError(f"RIGz cell {ci}: {len(raw)} bytes of instance data, neither layout fits")
        at = 0
        for idx, cnt in entries:
            f = flags[idx]
            pos_inst, zero_seeds = bool(f & 1), bool(f & 4)
            body = 8 if pos_inst else (48 if wide else 24)
            stride = body + (0 if zero_seeds else 4 * per_inst)
            chunk = np.frombuffer(raw, np.uint8, cnt * stride, at).reshape(cnt, stride)
            at += cnt * stride
            m = np.zeros((cnt, 3, 4), np.float32)
            if pos_inst:
                v = chunk[:, :8].copy().view("<i2").astype(np.float32)
                w = v[:, 3].astype(np.int32) & 0xFFFF
                scale = ((w & ~((1 << PALETTE_ID_BITS) - 1)) if f & 2 else w) / 256.0
                for k in range(3):
                    m[:, k, k] = scale
                m[:, :, 3] = v[:, :3] * mul + add
                keep = (v[:, :4] != 0).any(axis=1)  # an all-zero record is an erased instance
            else:
                if wide:
                    rot = chunk[:, :48].copy().view("<i4").astype(np.float64).reshape(cnt, 3, 4)
                    m[:, :, :3] = rot[:, :, :3] / 256.0 / 65536.0
                    m[:, :, 3] = rot[:, :, 3] * (mul / 65536.0) + add
                else:
                    rot = chunk[:, :24].copy().view("<i2").astype(np.float32).reshape(cnt, 3, 4)
                    m[:, :, :3] = rot[:, :, :3] / 256.0
                    m[:, :, 3] = rot[:, :, 3] * mul + add
                keep = (rot[:, :, :3] != 0).any(axis=(1, 2))
            name = names[idx]
            counts[name] = counts.get(name, 0) + int(keep.sum())
            if keep.any():
                placed.setdefault(name, Placed(name)).matrices.append(m[keep])
    return RiGen(names, flags, land, placed, counts)
