"""
War Thunder texture packs (`content/base/res/*.dxp.bin`, form `DxP2`) and the
DDSx textures in them, as far as a tactical map needs: the top mip level of a
DXT1/DXT5/BC7 or 32-bit texture, as an RGB image.

Written from the Dagor Engine's BSD-3-Clause source:
`prog/engine/lib3d/texPackMgr2.cpp` (the pack: a 16-byte header, then a dump
holding a sorted name table, one 32-byte DDSx header per texture and one
24-byte record per texture with the data's offset and packed size; tables are
(32-bit offset, 32-bit count, 8 bytes padding)) and
`prog/engine/sharedInclude/3d/ddsxTex.h` (the DDSx header: D3D format, flags
with the compression in the top three bits, size, mip count).
"""

from __future__ import annotations

import io
import struct
from pathlib import Path

import numpy as np

from . import oodle

FLG_REV_MIP_ORDER = 0x00040000
_COMPRESSION = 0xE0000000
_ZSTD, _OODLE, _ZLIB, _LZMA = 0x20000000, 0x60000000, 0x80000000, 0x40000000


class DxpError(ValueError):
    pass


class TexturePack:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        with self.path.open("rb") as fh:
            head = fh.read(16)
            label, version, _count, dump_size = struct.unpack("<4sIII", head)
            if label != b"DxP2" or version not in (2, 3):
                raise DxpError(f"{self.path.name}: not a DxP2 texture pack")
            dump = fh.read(dump_size)
        names_at, n = struct.unpack_from("<II", dump, 0)
        headers_at, _ = struct.unpack_from("<II", dump, 16)
        records_at, _ = struct.unpack_from("<II", dump, 32)
        rec_size = 24 if version == 2 else 16
        self.textures: dict[str, tuple[bytes, int, int]] = {}
        for i in range(n):
            (o,) = struct.unpack_from("<I", dump, names_at + 8 * i)
            full = dump[o : dump.index(b"\0", o)].decode("latin1")
            header = dump[headers_at + 32 * i : headers_at + 32 * i + 32]
            if version == 2:
                _ptr, _tid, ofs, packed, _ = struct.unpack_from("<QIiii", dump, records_at + rec_size * i)
            else:
                _ptr, ofs, packed = struct.unpack_from("<QiI", dump, records_at + rec_size * i)
            self.textures[full.split("*")[0]] = (header, ofs, packed)

    def names(self) -> list[str]:
        return list(self.textures)

    def image(self, name: str) -> np.ndarray:
        """The texture's largest mip level as RGB, (height, width, 3) uint8."""
        header, ofs, packed = self.textures[name]
        label, fmt, flags, w, h, levels, _hq, _depth, bpp, _q1, _q2, mem, psz = struct.unpack(
            "<4sIIHHBBHHBBII", header
        )
        if label != b"DDSx":
            raise DxpError(f"{name}: not a DDSx texture")
        with self.path.open("rb") as fh:
            fh.seek(ofs)
            blob = fh.read(packed)
        kind = flags & _COMPRESSION
        if kind == _OODLE:
            raw = oodle.decompress(blob, mem)
        elif kind == _ZSTD:
            import zstandard

            raw = zstandard.ZstdDecompressor().decompress(blob, max_output_size=mem)
        elif kind == _ZLIB:
            import zlib

            raw = zlib.decompress(blob)
        elif kind == _LZMA:
            raise DxpError(f"{name}: LZMA-packed texture, not read")
        else:
            raw = blob
        fourcc = struct.pack("<I", fmt)
        if fourcc in (b"DXT1",):
            top = (max(w // 4, 1) * max(h // 4, 1)) * 8
        elif fourcc in (b"DXT3", b"DXT5", b"BC7 ", b"ATI2", b"BC5U"):
            top = (max(w // 4, 1) * max(h // 4, 1)) * 16
        elif fmt in (21, 22):  # A8R8G8B8 / X8R8G8B8
            top = w * h * 4
        else:
            raise DxpError(f"{name}: texture format {fourcc!r}/{fmt} not read")
        surface = raw[len(raw) - top :] if (flags & FLG_REV_MIP_ORDER and levels > 1) else raw[:top]
        if len(surface) != top:
            raise DxpError(f"{name}: {len(surface)} bytes where the top level needs {top}")
        if fmt in (21, 22):
            bgra = np.frombuffer(surface, np.uint8).reshape(h, w, 4)
            return np.ascontiguousarray(bgra[:, :, 2::-1])
        return _decode_bc(fourcc, w, h, surface)


def _decode_bc(fourcc: bytes, w: int, h: int, data: bytes) -> np.ndarray:
    from PIL import Image

    if fourcc == b"BC7 ":
        dxgi = 98  # DXGI_FORMAT_BC7_UNORM
        pf = struct.pack("<II4sIIIII", 32, 4, b"DX10", 0, 0, 0, 0, 0)
        dds = (
            struct.pack("<4sIIIIIII44s", b"DDS ", 124, 0x1007 | 0x80000, h, w, len(data), 0, 1, b"\0" * 44)
            + pf
            + struct.pack("<IIIII", 0x1000, 0, 0, 0, 0)
            + struct.pack("<IIIII", dxgi, 3, 0, 1, 0)
        )
    else:
        pf = struct.pack("<II4sIIIII", 32, 4, fourcc, 0, 0, 0, 0, 0)
        dds = (
            struct.pack("<4sIIIIIII44s", b"DDS ", 124, 0x1007 | 0x80000, h, w, len(data), 0, 1, b"\0" * 44)
            + pf
            + struct.pack("<IIIII", 0x1000, 0, 0, 0, 0)
        )
    im = Image.open(io.BytesIO(dds + data))
    return np.asarray(im.convert("RGB"))
