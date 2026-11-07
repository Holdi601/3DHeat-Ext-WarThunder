"""
War Thunder's `*.vromfs.bin` archives and the binary BLK files inside them.

Both formats are the Dagor Engine's, whose source Gaijin published under the
BSD 3-Clause licence (github.com/GaijinEntertainment/DagorEngine). What is read
here was written from that source:

- `prog/dagorInclude/osApiWrappers/dag_vromfs.h`, `prog/engine/ioSys/vromfsLoad.cpp`
  and `prog/dagorInclude/supp/dag_zstdObfuscate.h`: the archive header
  (`VRFs`/`VRFx`, full and packed size, a zstd flag), the body, zstd-compressed
  with its first and last 16 bytes XORed by a fixed key, and the file table
  (a name table and a table of (offset, size) pairs, 16 bytes each).
- `prog/engine/ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`,
  `blk_zstd.cpp`: the binary BLK. A first byte says the form (1 complete with
  its own names, 2 the same zstd-compressed, 3/4/5 using the archive's shared
  name map, plain, zstd, or zstd with the archive's dictionary). The body is a
  name list, counts, a pool of long values, 8-byte parameters (name id: 24 bits,
  type: 8 bits, value or offset: 32 bits) and the block tree in breadth-first
  order.

Only reading. Nothing is written back.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass, field
from pathlib import Path

import zstandard

_XOR = (0xAA55AA55, 0xF00FF00F, 0xAA55AA55, 0x12481248)
SHARED_NAMEMAP = chr(255) + "?nm"


class VromfsError(ValueError):
    pass


def _deobfuscate(data: bytes) -> bytes:
    b = bytearray(data)
    n = len(b)
    if n >= 16:
        w = struct.unpack_from("<4I", b, 0)
        struct.pack_into("<4I", b, 0, *(w[i] ^ _XOR[i] for i in range(4)))
    if n >= 32:
        o = (n // 4 - 4) * 4
        w = struct.unpack_from("<4I", b, o)
        struct.pack_into("<4I", b, o, *(w[i] ^ _XOR[3 - i] for i in range(4)))
    return bytes(b)


def read_vromfs_bytes(data: bytes) -> dict[str, bytes]:
    """Every file in a vromfs image, by its path inside."""
    if len(data) < 16:
        raise VromfsError("too short for a vromfs header")
    label, _target, full, hw = struct.unpack_from("<4sIII", data, 0)
    if label not in (b"VRFs", b"VRFx"):
        raise VromfsError(f"not a vromfs archive (label {label!r})")
    p = 16
    if label == b"VRFx":
        (ext,) = struct.unpack_from("<H", data, 16)
        p = 16 + ext
    packed = hw & 0x3FFFFFFF
    if packed:
        body = data[p : p + packed]
        if hw & 0x40000000:
            body = zstandard.ZstdDecompressor().decompress(_deobfuscate(body), max_output_size=full)
        else:
            import zlib

            body = zlib.decompress(body)
    else:
        body = data[p : p + full]
    if len(body) != full:
        raise VromfsError(f"body is {len(body)} bytes, the header says {full}")
    names_at, count = struct.unpack_from("<II", body, 0)
    data_at, count2 = struct.unpack_from("<II", body, 16)
    if count != count2:
        raise VromfsError("name and data tables differ in length")
    files: dict[str, bytes] = {}
    for i in range(count):
        (o,) = struct.unpack_from("<I", body, names_at + 8 * i)
        name = body[o : body.index(b"\0", o)].decode("latin1")
        fo, fs = struct.unpack_from("<II", body, data_at + 16 * i)
        files[name] = body[fo : fo + fs]
    return files


class _Reader:
    def __init__(self, b: bytes):
        self.b, self.p = b, 0

    def uint(self) -> int:
        v = shift = 0
        while True:
            c = self.b[self.p]
            self.p += 1
            v |= (c & 0x7F) << shift
            shift += 7
            if not c & 0x80:
                return v

    def take(self, n: int) -> bytes:
        r = self.b[self.p : self.p + n]
        if len(r) != n:
            raise VromfsError("BLK ends early")
        self.p += n
        return r


def _names(r: _Reader) -> list[str]:
    n = r.uint()
    if not n:
        return []
    raw = r.take(r.uint())
    return [x.decode("utf-8", "replace") for x in raw.split(b"\0")[:n]]


_SIZE = {1: 4, 2: 4, 3: 4, 4: 8, 5: 12, 6: 16, 7: 8, 8: 12, 9: 1, 10: 4, 11: 48, 12: 8, 13: 16}
_FMT = {2: "<i", 3: "<f", 4: "<2f", 5: "<3f", 6: "<4f", 7: "<2i", 8: "<3i", 10: "<4B", 11: "<12f", 12: "<q", 13: "<4i"}


@dataclass
class Blk:
    """One block: its name, its parameters in order, its child blocks in order."""

    name: str = ""
    params: list[tuple[str, object]] = field(default_factory=list)
    blocks: list["Blk"] = field(default_factory=list)

    def get(self, key: str, default=None):
        for k, v in self.params:
            if k == key:
                return v
        return default

    def block(self, name: str) -> "Blk | None":
        for b in self.blocks:
            if b.name == name:
                return b
        return None


def parse_blk_dump(b: bytes, shared: list[str] | None = None) -> Blk:
    """The binary BLK body (after its form byte), with the archive's shared names if it uses them."""
    r = _Reader(b)
    names = list(shared or []) + _names(r)
    nblocks, nparams, pool_size = r.uint(), r.uint(), r.uint()
    pool = r.take(pool_size)
    params = r.take(nparams * 8)
    layout = []
    for _ in range(nblocks):
        nid, pc, bc = r.uint(), r.uint(), r.uint()
        layout.append((nid, pc, bc, r.uint() if bc else 0))

    def value(t: int, v: int):
        if t == 1:
            if v & 0x80000000:
                return names[v & 0x7FFFFFFF]
            return pool[v : pool.index(b"\0", v)].decode("utf-8", "replace")
        if t == 9:
            return bool(v & 0xFF)
        size = _SIZE.get(t)
        if size is None:
            raise VromfsError(f"BLK parameter of unknown type {t}")
        raw = struct.pack("<I", v) if size <= 4 else pool[v : v + size]
        x = struct.unpack(_FMT[t], raw[:size])
        return x[0] if len(x) == 1 else list(x)

    first_param = [0]
    for item in layout:
        first_param.append(first_param[-1] + item[1])

    def build(i: int) -> Blk:
        nid, pc, bc, fb = layout[i]
        out = Blk(names[nid - 1] if nid else "")
        for k in range(first_param[i], first_param[i] + pc):
            w, v = struct.unpack_from("<II", params, 8 * k)
            out.params.append((names[w & 0xFFFFFF], value(w >> 24, v)))
        out.blocks = [build(j) for j in range(fb, fb + bc)]
        return out

    return build(0)


class Vromfs:
    """One archive, opened; `blk(path)` reads a BLK in it whatever its form."""

    def __init__(self, path: str | Path | None = None, *, files: dict[str, bytes] | None = None):
        self.files = files if files is not None else read_vromfs_bytes(Path(path).read_bytes())
        self._shared: list[str] | None = None
        self._dict: zstandard.ZstdCompressionDict | None = None
        nm = self.files.get(SHARED_NAMEMAP)
        if nm is not None and len(nm) >= 40:
            self._shared = _names(_Reader(zstandard.ZstdDecompressor().decompressobj().decompress(nm[40:])))
            d = self.files.get(nm[8:40].hex() + ".dict")
            if d is not None:
                self._dict = zstandard.ZstdCompressionDict(d)

    def blk(self, name: str) -> Blk:
        b = self.files[name]
        if not b:
            return Blk()
        form = b[0]
        unz = lambda data, d=None: (  # noqa: E731
            zstandard.ZstdDecompressor(dict_data=d) if d else zstandard.ZstdDecompressor()
        ).decompressobj().decompress(data)
        if form == 1:
            return parse_blk_dump(b[1:])
        if form == 2:
            n = int.from_bytes(b[1:4], "little")
            inner = unz(b[4 : 4 + n])
            return parse_blk_dump(inner[1:])
        if form in (3, 4, 5):
            if self._shared is None:
                raise VromfsError(f"{name} needs the archive's shared name map, which it lacks")
            body = b[1:] if form == 3 else unz(b[1:], self._dict if form == 5 else None)
            return parse_blk_dump(body, self._shared)
        raise VromfsError(f"{name}: text BLK or unknown form {form}")
