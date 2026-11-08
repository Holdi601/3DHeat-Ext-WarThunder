"""
The colour of a War Thunder level's ground, seen from above, and its roads.

The game shades its terrain with land classes: each is a colour map tiled over
the world every `size` metres, a splatting mask tiled with it, and detail
textures (one per mask channel) tiled every few metres. A weight map in the
level says, for every point, how much of up to seven land classes is there.
This module composes that into one top-down colour image, the way the game
shades the ground at a distance where the detail textures are only their
average colour; and it reads the level's ground decals (roads, tracks, town
squares) from the physics map so they can be painted in at their real shape.

Written from the Dagor Engine's BSD-3-Clause source
(github.com/GaijinEntertainment/DagorEngine); no game code was disassembled.

- The land mesh header and its detail data (`lmap`):
  `prog/gameLibs/landMesh/lmeshManager.cpp` (`LandMeshManager::loadDump`, the
  offsets after `lndm`; `DetailMap::load` and `read_cell_record`: per cell
  seven land-class ids, a length, the second texture's offset, then the weight
  textures as DDSx), `lmeshLandClasses.cpp` (`loadLandClasses`: a block per
  land class, its name, then a binary BLK; `load_land_class`: `texture`,
  `splattingmap`, `detailmap`, `detail{Red,Green,Blue,Black}`, `size`,
  `offset`), `lmeshWeightAtlasLegacyCpu.cpp` and `lmeshWeightAtlasInternal.h`
  (the weight textures: four channels in the first, two in the second, and
  `land_weight_derive` - the weight at index `(n - 1) & ~1` is what the others
  leave), `lmeshRenderer.cpp` (a land class's texture coordinates:
  `(x + offset.x) * tile`, `-(z + offset.y) * tile`) and
  `lmeshWeightAtlasGpu.cpp` (`setCellMapping`: cell = world / cell size - origin).
- How a land class's colours combine: `prog/daNetGame/shaders/land_aces.dshl`,
  colour map times detail times `COLOR_CORRECTION_MULTIPLIER` (2^2.2, in linear
  light).
- The physics map (`LMp2`): `prog/gameLibs/physMap/physMapLoad.cpp`
  (`load_phys_map`: version, material names, size, offset, scale, then a
  compressed tree bitmap and the decal meshes: 2D vertices, texture
  coordinates, per material a run of triangles) and
  `prog/engine/baseUtil/treeBitmap.cpp` (`TreeBitmapNode::load`, `get`).
- The level's splines (`hspl`): `prog/gameLibs/levelSplines/levelSplines.cpp`
  (`load_splines`: a count, then per spline a name and its Bezier points).
- Texture packs (`*.dxp.bin`, through `dxp.TexturePack`) and DDSx headers:
  `prog/engine/sharedInclude/3d/ddsxTex.h`.

Strings in the level binary are a 32-bit length, the characters, and zero
padding to four bytes.
"""

from __future__ import annotations

import io
import struct
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from . import oodle
from .vromfs import Blk, parse_blk_dump

DET_TEX_NUM = 7
# land_weight_atlas.hlsli: the packed atlas's page border and the bits of a cell's pages dword
_ATLAS_BORDER = 2
_ATLAS_PAGE_MASK, _ATLAS_PAGE1_SHIFT, _ATLAS_COUNT_SHIFT = 0x3FFF, 14, 28
#: COLOR_CORRECTION_MULTIPLIER: colour map times detail, in linear light, is scaled by 2^2.2.
COLOUR_MULTIPLIER = 2.0 ** 2.2
_REV_MIP_ORDER = 0x00040000
_COMPRESSION = 0xE0000000
_ZSTD, _LZMA, _OODLE, _ZLIB = 0x20000000, 0x40000000, 0x60000000, 0x80000000


class TerrainError(ValueError):
    pass


# --- small readers -----------------------------------------------------------------------------------------------


def _string(data: bytes, p: int) -> tuple[str, int]:
    """A level-binary string: 32-bit length, the characters, padded to four bytes."""
    (n,) = struct.unpack_from("<i", data, p)
    if n < 0 or p + 4 + n > len(data):
        raise TerrainError("string past the end of its block")
    return data[p + 4 : p + 4 + n].decode("latin1"), p + 4 + ((n + 3) & ~3)


def _unpack_block(data: bytes, p: int) -> tuple[bytes, int]:
    """A block at `p`: 32-bit length with the compression in its top two bits (1 zstd, 2 Oodle with its size
    first, 0 the 7-zip LZMA stream). Returns the decoded bytes and the block's end."""
    (word,) = struct.unpack_from("<I", data, p)
    fmt, n, a = word >> 30, word & 0x3FFFFFFF, p + 4
    body = data[a : a + n]
    if fmt == 2:
        (src,) = struct.unpack_from("<i", body, 0)
        return oodle.decompress(body[4:], src), a + n
    if fmt == 1:
        import zstandard

        return zstandard.ZstdDecompressor().decompressobj().decompress(body), a + n
    import lzma

    props = body[0]
    pb, rest = divmod(props, 45)
    lp, lc = divmod(rest, 9)
    (dict_size,) = struct.unpack_from("<I", body, 1)
    dec = lzma.LZMADecompressor(lzma.FORMAT_RAW, filters=[{"id": lzma.FILTER_LZMA1, "lc": lc, "lp": lp, "pb": pb,
                                                            "dict_size": dict_size}])
    return dec.decompress(body[5:]), a + n


# --- DDSx --------------------------------------------------------------------------------------------------------


def _block_bytes(fourcc: bytes) -> int | None:
    if fourcc == b"DXT1":
        return 8
    if fourcc in (b"DXT3", b"DXT5", b"BC7 ", b"ATI2", b"BC5U"):
        return 16
    return None


def _surface_size(fmt: int, w: int, h: int) -> int:
    fourcc = struct.pack("<I", fmt)
    bb = _block_bytes(fourcc)
    if bb:
        return max((w + 3) // 4, 1) * max((h + 3) // 4, 1) * bb
    if fmt in (21, 22):  # A8R8G8B8, X8R8G8B8
        return w * h * 4
    if fmt in (25, 26):  # A1R5G5B5, A4R4G4B4
        return w * h * 2
    if fmt == 50:  # L8
        return w * h
    raise TerrainError(f"texture format {fourcc!r}/{fmt} is not read")


def _decode_surface(fmt: int, w: int, h: int, data: bytes) -> np.ndarray:
    """One surface as RGBA (h, w, 4) uint8."""
    fourcc = struct.pack("<I", fmt)
    if fmt in (21, 22):
        bgra = np.frombuffer(data, np.uint8, w * h * 4).reshape(h, w, 4)
        out = bgra[:, :, [2, 1, 0, 3]].copy()
        if fmt == 22:
            out[:, :, 3] = 255
        return out
    if fmt == 26:  # A4R4G4B4
        v = np.frombuffer(data, "<u2", w * h).reshape(h, w).astype(np.uint16)
        return np.stack([((v >> s) & 15) * 17 for s in (8, 4, 0, 12)], -1).astype(np.uint8)
    if fmt == 25:  # A1R5G5B5
        v = np.frombuffer(data, "<u2", w * h).reshape(h, w).astype(np.uint16)
        c = [((v >> s) & 31) * 255 // 31 for s in (10, 5, 0)]
        return np.stack(c + [(v >> 15) * 255], -1).astype(np.uint8)
    if fmt == 50:
        v = np.frombuffer(data, np.uint8, w * h).reshape(h, w)
        return np.stack([v, v, v, np.full_like(v, 255)], -1)
    if _block_bytes(fourcc) is None:
        raise TerrainError(f"texture format {fourcc!r} is not read")
    from PIL import Image

    pw, ph = max(w, 4), max(h, 4)
    if fourcc == b"BC7 ":
        pf = struct.pack("<II4sIIIII", 32, 4, b"DX10", 0, 0, 0, 0, 0)
        tail = struct.pack("<IIIII", 0x1000, 0, 0, 0, 0) + struct.pack("<IIIII", 98, 3, 0, 1, 0)
    else:
        pf = struct.pack("<II4sIIIII", 32, 4, fourcc, 0, 0, 0, 0, 0)
        tail = struct.pack("<IIIII", 0x1000, 0, 0, 0, 0)
    dds = struct.pack("<4sIIIIIII44s", b"DDS ", 124, 0x1007 | 0x80000, ph, pw, len(data), 0, 1, b"\0" * 44) + pf + tail
    im = np.asarray(Image.open(io.BytesIO(dds + data)).convert("RGBA"))
    out = im[:h, :w].copy()
    if fourcc == b"DXT1":
        out[:, :, 3] = 255  # the weight readers treat a DXT1's alpha as absent
    return out


def _decompress(flags: int, blob: bytes, mem: int) -> bytes:
    kind = flags & _COMPRESSION
    if kind == _OODLE:
        return oodle.decompress(blob, mem)
    if kind == _ZSTD:
        import zstandard

        return zstandard.ZstdDecompressor().decompress(blob, max_output_size=mem)
    if kind == _ZLIB:
        import zlib

        return zlib.decompress(blob)
    if kind == _LZMA:
        raise TerrainError("LZMA-packed texture, not read")
    return blob


def _mip_chain(fmt: int, w: int, h: int, levels: int) -> list[tuple[int, int, int]]:
    sizes = [(max(w >> i, 1), max(h >> i, 1)) for i in range(max(levels, 1))]
    return [(a, b, _surface_size(fmt, a, b)) for a, b in sizes]


def decode_ddsx(header: bytes, blob: bytes, max_size: int = 0) -> np.ndarray:
    """A DDSx texture's largest mip level that is in `blob` and no wider than `max_size` (0: any), as RGBA.

    Textures whose top levels live in a separate high-quality pack hold only the lower levels here; which levels
    are present is found from the decoded size."""
    label, fmt, flags, w, h, levels, _hq, _depth, _bpp, _q1, _q2, mem, _psz = struct.unpack(
        "<4sIIHHBBHHBBII", header[:32])
    if label != b"DDSx":
        raise TerrainError("not a DDSx texture")
    raw = _decompress(flags, blob, mem)
    chain = _mip_chain(fmt, w, h, levels)
    first = None
    for k in range(len(chain)):  # the first k levels are missing (kept in the -hq pack)
        if sum(s for _, _, s in chain[k:]) == len(raw):
            first = k
            break
    if first is None:
        first = 0
        if len(raw) < chain[0][2]:
            raise TerrainError(f"texture of {len(raw)} bytes where its top level needs {chain[0][2]}")
    present = chain[first:]
    want = first
    while max_size and want < len(chain) - 1 and max(chain[want][0], chain[want][1]) > max_size:
        want += 1
    rev = bool(flags & _REV_MIP_ORDER) and len(present) > 1
    order = list(range(len(present)))[::-1] if rev else list(range(len(present)))
    at = 0
    for i in order:
        if first + i == want:
            mw, mh, sz = present[i]
            return _decode_surface(fmt, mw, mh, raw[at : at + sz])
        at += present[i][2]
    raise TerrainError("mip level not found")


# --- the install's textures --------------------------------------------------------------------------------------


_PACK_INDEX: dict[str, dict[str, Path]] = {}


class Textures:
    """Every texture of the install's packs (`content/*/res/*.dxp.bin`) by name, the first pack naming it winning,
    with decoded images and mean colours cached."""

    def __init__(self, root: Path, packs: list[Path] | None = None):
        from .dxp import TexturePack

        self._pack_cls = TexturePack
        key = str(root)
        if packs is not None:
            self.where = {}
            for p in packs:
                for n in TexturePack(p).names():
                    self.where.setdefault(n, p)
        else:
            if key not in _PACK_INDEX:
                where: dict[str, Path] = {}
                content = Path(root) / "content"
                files = sorted((content / "base" / "res").glob("*.dxp.bin")) + sorted(
                    p for p in content.glob("*/res/*.dxp.bin") if p.parent.parent.name != "base")
                # the full packs before their -hq halves, so a name resolves to the pack holding all its mips first
                files.sort(key=lambda p: ("-hq." in p.name, str(p)))
                for p in files:
                    try:
                        for n in TexturePack(p).names():
                            where.setdefault(n, p)
                    except Exception:
                        continue
                _PACK_INDEX[key] = where
            self.where = _PACK_INDEX[key]
        self._packs: dict[Path, object] = {}
        self._images: dict[tuple[str, int], np.ndarray | None] = {}
        self.missing: set[str] = set()

    @staticmethod
    def clean(name: str) -> str:
        return name.split("*")[0].split("?")[0].strip()

    def image(self, name: str, max_size: int = 512) -> np.ndarray | None:
        """RGBA uint8, or None when no pack has it or it cannot be decoded."""
        n = self.clean(name)
        k = (n, max_size)
        if k not in self._images:
            img = None
            p = self.where.get(n)
            if p is not None:
                try:
                    pack = self._packs.get(p) or self._packs.setdefault(p, self._pack_cls(p))
                    header, ofs, packed = pack.textures[n]
                    with p.open("rb") as fh:
                        fh.seek(ofs)
                        blob = fh.read(packed)
                    img = decode_ddsx(header, blob, max_size)
                except Exception:
                    img = None
            if img is None:
                self.missing.add(n)
            self._images[k] = img
        return self._images[k]

    def mean_linear(self, name: str | None) -> np.ndarray | None:
        """A texture's average colour in linear light (from a small mip level)."""
        if not name:
            return None
        img = self.image(name, 16)
        if img is None:
            return None
        return srgb_to_linear(img[:, :, :3].reshape(-1, 3) / 255.0).mean(0)


def srgb_to_linear(c: np.ndarray) -> np.ndarray:
    c = np.asarray(c, np.float32)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4).astype(np.float32)


def linear_to_srgb(c: np.ndarray) -> np.ndarray:
    c = np.clip(np.asarray(c, np.float32), 0.0, 1.0)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(c, 1 / 2.4) - 0.055).astype(np.float32)


# --- land classes and the weight map -----------------------------------------------------------------------------


@dataclass
class LandClass:
    name: str
    blk: Blk
    colormap: str | None
    splatting: str | None
    details: tuple[str | None, str | None, str | None, str | None]  # red, green, blue, black (or the one detailmap)
    tile: tuple[float, float]  # 1 / size
    offset: tuple[float, float]  # land-class offset, world origin already applied (the renderer's `offset`)


@dataclass
class LandDetail:
    """The land mesh's land classes and its weight map: per cell up to seven land classes and their weights."""

    classes: list[LandClass]
    cell_size: float
    origin: tuple[int, int]
    cells: tuple[int, int]  # x, y (y along z)
    tex_size: int
    ids: np.ndarray  # (cells_y, cells_x, 7) uint8, 0xFF unused
    records: dict[int, tuple[int, int, int]]  # cell index -> (start, length, second texture offset) in the level bytes
    data: bytes = b""
    vertical: dict = field(default_factory=dict)
    tile_texture: str | None = None
    atlas: dict | None = None  # the packed weight atlas, when the level ships one
    _atlas_image: np.ndarray | None = None
    _weights: dict[int, np.ndarray | None] = field(default_factory=dict)

    def weights(self, cell: int) -> np.ndarray | None:
        """(7, T, T) float32 weights of a cell's land classes, rows along +z; None for a cell without a record."""
        if cell not in self._weights:
            self._weights[cell] = self._decode(cell)
        return self._weights[cell]

    def _decode_atlas(self, cell: int) -> np.ndarray | None:
        """land_weight_inc.dshl `get_weights`: page 0 holds weights 0-2, page 1 weights 3-5; the last of the cell's
        `count` land classes is what the others leave."""
        a = self.atlas
        rec = int(a["words"][cell])
        count = ((rec >> _ATLAS_COUNT_SHIFT) & 7) + 1
        e = a["elem"]
        w = np.zeros((DET_TEX_NUM, e, e), np.float32)
        if count == 1:
            w[0] = 1.0
            return w
        if self._atlas_image is None:
            blob = a["ddsx"]
            self._atlas_image = decode_ddsx(blob[:32], blob[32:], 0)
        img = self._atlas_image
        pw, per = a["pageW"], a["perRow"]

        def page(pg: int) -> np.ndarray:
            px, py = (pg % per) * pw + _ATLAS_BORDER, (pg // per) * pw + _ATLAS_BORDER
            return img[py : py + e, px : px + e, :3].astype(np.float32).transpose(2, 0, 1) / 255.0

        w[0:3] = page(rec & _ATLAS_PAGE_MASK)
        if count > 4:
            p1 = page((rec >> _ATLAS_PAGE1_SHIFT) & _ATLAS_PAGE_MASK)
            w[3], w[4], w[5] = p1[0], p1[1], p1[2]
        last = count - 1
        w[last:] = 0
        w[last] = np.clip(1.0 - w[:last].sum(0), 0.0, 1.0)
        return w

    def _decode(self, cell: int) -> np.ndarray | None:
        if self.atlas is not None:
            return self._decode_atlas(cell)
        rec = self.records.get(cell)
        cy, cx = divmod(cell, self.cells[0])
        ids = self.ids[cy, cx]
        n = int((ids != 0xFF).sum())
        if rec is None or n == 0:
            return None
        start, length, tex2 = rec
        t = self.tex_size
        body = self.data[start : start + length]
        w = np.zeros((DET_TEX_NUM, t, t), np.float32)
        for k, (a, b, ch0, nch) in enumerate(((0, tex2 if tex2 else length, 0, 4), (tex2, length, 4, 2))):
            if (k == 1 and not tex2) or b <= a:
                continue
            blob = body[a:b]
            img = decode_ddsx(blob[:32], blob[32:], 0)
            if img.shape[0] != t or img.shape[1] != t:
                img = _resize_nearest(img, t)
            hdr_fmt = struct.unpack_from("<I", blob, 4)[0]
            planes = img.astype(np.float32) / 255.0
            for c in range(nch):
                if c == 3 and struct.pack("<I", hdr_fmt) == b"DXT1":
                    continue  # a DXT1's fourth channel is zero
                w[ch0 + c] = planes[:, :, c]
        # land_weight_derive: the derived weight is what the others leave
        n = max(1, min(n, DET_TEX_NUM))
        derived = (n - 1) & ~1
        w[n:] = 0
        w[derived] = 0
        w[derived] = np.clip(1.0 - w[:n].sum(0), 0.0, 1.0)
        return w


def _resize_nearest(img: np.ndarray, t: int) -> np.ndarray:
    ys = (np.arange(t) * img.shape[0] // t)
    xs = (np.arange(t) * img.shape[1] // t)
    return img[ys][:, xs]


def _land_class(name: str, blk: Blk, origin: tuple[int, int], cell_size: float) -> LandClass:
    size = blk.get("size")
    if isinstance(size, (list, tuple)):
        sx, sz = float(size[0]), float(size[1])
    elif size is not None:
        sx = sz = float(size)
    else:
        sx = sz = 1.0
    off = blk.get("offset") or [0.0, 0.0]
    if not isinstance(off, (list, tuple)):
        off = [float(off), float(off)]
    ox = -float(off[0]) - origin[0] * cell_size
    oz = -float(off[1]) - origin[1] * cell_size
    if blk.get("splattingmap"):
        details = tuple(blk.get(f"detail{c}") for c in ("Red", "Green", "Blue", "Black"))
        splat = blk.get("splattingmap")
    else:
        d = blk.get("detailmap")
        details = (d, None, None, None)
        splat = None
    return LandClass(name, blk, blk.get("texture"), splat, details, (1.0 / sx if sx else 1.0, 1.0 / sz if sz else 1.0),
                     (ox, oz))


def read_land_detail(data: bytes, table: dict) -> LandDetail | None:
    """The land classes and weight map of the level's land mesh (`lmap`), or None when it has none."""
    if "lmap" not in table:
        return None
    s = table["lmap"][0].start
    if data[s : s + 4] != b"lndm":
        raise TerrainError("land mesh block without lndm")
    version, _grid, cell_size, mx, my, ox, oy, use_tile = struct.unpack_from("<iffiiiii", data, s + 4)
    if version != 4:
        raise TerrainError(f"land mesh version {version} is not read")
    base = s + 36
    _mesh, detail_ofs, tile_ofs, _ray = struct.unpack_from("<4i", data, base)
    p = base + detail_ofs
    # loadLandClasses: a block holding the count and a block per land class (name, then a binary BLK)
    (word,) = struct.unpack_from("<I", data, p)
    lc_end = p + 4 + (word & 0x3FFFFFFF)
    q = p + 4
    (count,) = struct.unpack_from("<i", data, q)
    q += 4
    classes = []
    for _ in range(count):
        (w2,) = struct.unpack_from("<I", data, q)
        end = q + 4 + (w2 & 0x3FFFFFFF)
        name, r = _string(data, q + 4)
        blk = Blk()
        if r < end:
            form = data[r]
            if form != 1:
                raise TerrainError(f"land class {name}: BLK form {form} is not read")
            blk = parse_blk_dump(data[r + 1 : end])
        classes.append(_land_class(name, blk, (ox, oy), cell_size))
        q = end
    p = lc_end
    sx, sy, tex_size, elem = struct.unpack_from("<4i", data, p)
    p += 16
    ids = np.full((sy, sx, DET_TEX_NUM), 0xFF, np.uint8)
    records = {}
    atlas = None
    if tex_size == 0:
        # LandWeightAtlas::readPacked: the legacy table (one offset per cell to one empty record), pages per row,
        # page count, a 12-byte record per cell (pages dword, seven land-class ids), then the atlas as DDSx.
        q = p + 4 * sx * sy + DET_TEX_NUM + 8
        per_row, n_pages = struct.unpack_from("<ii", data, q)
        q += 8
        recs = np.frombuffer(data, np.uint8, sx * sy * 12, q).reshape(sx * sy, 12)
        q += sx * sy * 12
        (n,) = struct.unpack_from("<i", data, q)
        blob = data[q + 4 : q + 4 + n]
        ids[:] = recs[:, 4 : 4 + DET_TEX_NUM].reshape(sy, sx, DET_TEX_NUM)
        atlas = {"perRow": per_row, "pages": n_pages, "elem": elem,
                 "pageW": (elem + 2 * _ATLAS_BORDER + 3) & ~3,
                 "words": recs[:, :4].copy().view("<u4").ravel(), "ddsx": blob}
    offsets = np.frombuffer(data, "<i4", sx * sy, p) if atlas is None else []
    for i, o in enumerate(offsets):
        a = base + int(o)
        if o <= 0 or a + DET_TEX_NUM + 8 > len(data):
            continue
        ids[i // sx, i % sx] = np.frombuffer(data, np.uint8, DET_TEX_NUM, a)
        length, tex2 = struct.unpack_from("<ii", data, a + DET_TEX_NUM)
        if length < 0 or tex2 < 0 or tex2 > length:
            continue
        records[i] = (a + DET_TEX_NUM + 8, length, tex2)
    detail = LandDetail(classes, float(cell_size), (ox, oy), (sx, sy), tex_size or elem, ids, records, data,
                        atlas=atlas)
    # After the tile data and the land tracer: the vertical (cliff) texture and its blend.
    try:
        t = base + tile_ofs
        if use_tile:
            detail.tile_texture, t = _string(data, t)
            t += 8
        if _ray > 0:  # the land tracer's block, when the level has one
            (word,) = struct.unpack_from("<I", data, t)
            t += 4 + (word & 0x3FFFFFFF)
        vname, t = _string(data, t)
        if vname:
            xz, y, b0, b1, hb, yo = struct.unpack_from("<6f", data, t)
            detail.vertical = {"texture": vname.split(":")[0].rstrip("!"), "scaleXZ": xz, "scaleY": y,
                               "blendFromY": b0, "blendToY": b1, "horizontalBlend": hb}
    except (struct.error, TerrainError):
        pass
    return detail


# --- physics map: ground decals ----------------------------------------------------------------------------------


@dataclass
class Decal:
    vertices: np.ndarray  # (n, 2) game x, z
    runs: list[tuple[str, np.ndarray]]  # (material name, (m, 3) triangles)


@dataclass
class PhysMap:
    materials: list[str]
    size: int
    offset: tuple[float, float]
    scale: float
    decals: list[Decal]
    tree: bytes = b""
    tree_at: int = 0

    def grid(self) -> np.ndarray:
        """The material index per map pixel, (size, size) uint8, row = z; 0xFF where none."""
        out = np.full((self.size, self.size), 0xFF, np.uint8)
        _tree_fill(self.tree, [self.tree_at], out, 0, 0, self.size)
        return out


def _tree_fill(b: bytes, at: list[int], out: np.ndarray, x0: int, y0: int, size: int) -> None:
    fill, has = b[at[0]], b[at[0] + 1]
    at[0] += 2
    if not has:
        out[y0 : y0 + size, x0 : x0 + size] = fill
        return
    if fill & 0x80:
        dim = 1 << ((fill & 0x7F) + 1)
        sub = size // dim
        for y in range(dim):
            for x in range(dim):
                _tree_fill(b, at, out, x0 + x * sub, y0 + y * sub, max(sub, 1))
        return
    if fill & 4:
        n = 16 * 16 // 8 + 2
        raw = np.frombuffer(b, np.uint8, n, at[0])
        bits = np.unpackbits(raw[2:], bitorder="little")[: 256]
        vals = raw[:2][bits]
    elif fill & 8:
        n = 16 * 16 // 4 + 4
        raw = np.frombuffer(b, np.uint8, n, at[0])
        bits = np.unpackbits(raw[4:], bitorder="little")[: 512].reshape(256, 2)
        vals = raw[:4][bits[:, 0] | (bits[:, 1] << 1)]
    else:
        n = 256
        vals = np.frombuffer(b, np.uint8, n, at[0])
    at[0] += n
    rep = max(size // 16, 1)
    block = np.repeat(np.repeat(vals.reshape(16, 16), rep, 0), rep, 1)
    out[y0 : y0 + size, x0 : x0 + size] = block[:size, :size]


def _tree_skip(b: bytes, at: int) -> int:
    fill, has = b[at], b[at + 1]
    at += 2
    if not has:
        return at
    if fill & 0x80:
        dim = 1 << ((fill & 0x7F) + 1)
        for _ in range(dim * dim):
            at = _tree_skip(b, at)
        return at
    return at + (34 if fill & 4 else 68 if fill & 8 else 256)


def read_phys_map(data: bytes, table: dict) -> PhysMap | None:
    """The physics map (`LMp2`): material names, the per-pixel material tree and the ground decals."""
    if "LMp2" not in table:
        return None
    p = table["LMp2"][0].start
    (version,) = struct.unpack_from("<i", data, p)
    p += 4
    (n,) = struct.unpack_from("<i", data, p)
    p += 4
    names = []
    for _ in range(n):
        nm, p = _string(data, p)
        names.append(nm)
    if version == 0:
        p += 20
    size, _h, ox, oz, scale = struct.unpack_from("<iifff", data, p)
    p += 20
    raw, _ = _unpack_block(data, p)
    at = 0
    if version == 0:
        at = _tree_skip(raw, at)
    tree_at = at
    at = _tree_skip(raw, at)

    def u16() -> int:
        nonlocal at
        (v,) = struct.unpack_from("<H", raw, at)
        at += 2
        return v

    decals = []
    for _ in range(u16()):
        nv = u16()
        v = np.frombuffer(raw, "<f4", nv * 2, at).reshape(nv, 2).copy()
        at += nv * 8
        if version > 0:
            nt = u16()
            at += nt * 8
        runs = []
        while True:
            mat = raw[at]
            at += 1
            nf = u16()
            if nf == 0:
                break
            f = np.frombuffer(raw, "<u2", nf * 3, at).reshape(nf, 3).astype(np.int64)
            at += nf * 6
            if version > 0:
                at += 2 + nf * 6
            runs.append((names[mat] if mat < len(names) else str(mat), f))
        decals.append(Decal(v, runs))
    return PhysMap(names, size, (ox, oz), scale, decals, raw, tree_at)


# --- splines -----------------------------------------------------------------------------------------------------


@dataclass
class Spline:
    name: str
    points: np.ndarray  # (n, 3, 3): per point bezIn, pt, bezOut in game x, y, z

    def polyline(self, steps: int = 8) -> np.ndarray:
        """The curve through its points, `steps` segments per Bezier span, (m, 3)."""
        pts = self.points
        if len(pts) < 2:
            return pts[:, 1].copy()
        t = np.linspace(0, 1, steps, endpoint=False)[:, None]
        out = []
        for a, b in zip(pts[:-1], pts[1:]):
            p0, p1, p2, p3 = a[1], a[2], b[0], b[1]
            out.append(((1 - t) ** 3) * p0 + 3 * ((1 - t) ** 2) * t * p1 + 3 * (1 - t) * t * t * p2 + t ** 3 * p3)
        out.append(pts[-1, 1][None])
        return np.concatenate(out)


def read_splines(data: bytes, table: dict) -> list[Spline]:
    """The level's splines (`hspl`): roads, fences, rails, each named after the asset that follows it."""
    if "hspl" not in table:
        return []
    b = table["hspl"][0]
    p = b.start
    (n,) = struct.unpack_from("<i", data, p)
    p += 4
    out = []
    for _ in range(n):
        name, p = _string(data, p)
        (c,) = struct.unpack_from("<i", data, p)
        p += 4
        if c < 0 or p + 36 * c > b.end:
            raise TerrainError("spline past the end of its block")
        pts = np.frombuffer(data, "<f4", c * 9, p).reshape(c, 3, 3).copy()
        p += 36 * c
        out.append(Spline(name, pts))
    return out


def spline_asset(name: str) -> str:
    """The asset a spline follows: its name without the editor's trailing number."""
    head, _, tail = name.rpartition("_")
    return head if head and tail.isdigit() else name


# --- composing ---------------------------------------------------------------------------------------------------


def _sample_wrap(img: np.ndarray, u: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Bilinear, repeating; img (h, w, c) float32, u/v in texture space."""
    h, w = img.shape[:2]
    x = np.mod(u, 1.0) * w - 0.5
    y = np.mod(v, 1.0) * h - 0.5
    x0 = np.floor(x).astype(np.int64)
    y0 = np.floor(y).astype(np.int64)
    fx = (x - x0)[..., None].astype(np.float32)
    fy = (y - y0)[..., None].astype(np.float32)
    x0 %= w
    y0 %= h
    x1 = (x0 + 1) % w
    y1 = (y0 + 1) % h
    return ((img[y0, x0] * (1 - fx) + img[y0, x1] * fx) * (1 - fy) + (img[y1, x0] * (1 - fx) + img[y1, x1] * fx) * fy)


@dataclass
class _ClassLook:
    colormap: np.ndarray | None  # linear RGB (h, w, 3)
    mean: np.ndarray  # linear RGB, what the class looks like where nothing else is known
    splat: np.ndarray | None  # (h, w, 4) float32 RGBA mask
    details: np.ndarray  # (4, 3) linear mean colours of the detail textures (red, green, blue, black)
    indices: np.ndarray | None = None  # an indexed (biome) land class: the detail number per texel, (h, w) uint8
    index_colours: np.ndarray | None = None  # (256, 3) linear albedo per detail number


_FALLBACK = srgb_to_linear(np.array([0.42, 0.40, 0.33]))


def _indexed_details(tex: Textures, blk: Blk) -> np.ndarray | None:
    """An indexed land class's `details`: the linear albedo of each `detail` block, in order - the number the
    index texture holds. `scheme` names a detail's parameters and their defaults; its string parameters other than
    `detail_group` name texture blocks (each with an `albedo`), blended here by the scheme's `*weights` pair."""
    det = blk.block("details")
    if det is None:
        return None
    scheme = det.block("scheme") or Blk()
    tex_keys = [k for k, v in scheme.params if isinstance(v, str) and k != "detail_group"]
    weight_key = next((k for k, _ in scheme.params if k.endswith("weights")), None)
    named = {b.name: b for b in det.blocks if b.name not in ("detail", "detail_group", "scheme")}
    out = np.zeros((256, 3), np.float32)
    out[:] = _FALLBACK
    i = 0
    for b in det.blocks:
        if b.name != "detail":
            continue
        weights = b.get(weight_key, scheme.get(weight_key)) if weight_key else None
        if not isinstance(weights, (list, tuple)):
            weights = [1.0] * len(tex_keys)
        cols, ws = [], []
        for j, k in enumerate(tex_keys):
            t = b.get(k, scheme.get(k))
            src = named.get(t) if t else None
            m = tex.mean_linear(src.get("albedo")) if src is not None else None
            w = float(weights[j]) if j < len(weights) else 1.0
            if m is not None and w > 0:
                cols.append(m)
                ws.append(w)
        if cols and i < 256:
            out[i] = np.average(np.stack(cols), axis=0, weights=ws)
        i += 1
    return out


def _class_look(tex: Textures, lc: LandClass, max_size: int) -> _ClassLook:
    if "indexed_landclass" in (lc.blk.get("shader") or ""):
        lct = lc.blk.block("landClassTextures")
        idx = tex.image(lct.get("indices"), 0) if lct is not None and lct.get("indices") else None
        cols = _indexed_details(tex, lc.blk)
        if idx is not None and cols is not None:
            cm = tex.image(lc.colormap, max_size) if lc.colormap else None
            cm_lin = srgb_to_linear(cm[:, :, :3] / 255.0) if cm is not None else None
            ind = np.ascontiguousarray(idx[:, :, 0])
            u, c = np.unique(ind, return_counts=True)
            mean = (cols[u] * c[:, None]).sum(0) / c.sum()
            base = cm_lin.reshape(-1, 3).mean(0) if cm_lin is not None else np.full(3, 1 / COLOUR_MULTIPLIER,
                                                                                         np.float32)
            return _ClassLook(cm_lin, np.clip(base * mean * COLOUR_MULTIPLIER, 0, 1), None,
                              np.zeros((4, 3), np.float32),
                              ind, cols)
    cm = tex.image(lc.colormap, max_size) if lc.colormap else None
    cm_lin = srgb_to_linear(cm[:, :, :3] / 255.0) if cm is not None else None
    splat = tex.image(lc.splatting, max_size) if lc.splatting else None
    splat_f = splat.astype(np.float32) / 255.0 if splat is not None else None
    det = []
    for d in lc.details:
        m = tex.mean_linear(d)
        det.append(m if m is not None else np.full(3, 0.2178, np.float32))  # mid grey: the colour map alone
    details = np.stack(det).astype(np.float32)
    base = cm_lin.reshape(-1, 3).mean(0) if cm_lin is not None else _FALLBACK
    if splat_f is not None:
        r, g, b, _a = splat_f.reshape(-1, 4).mean(0)
        dm = r * details[0] + g * details[1] + b * details[2] + max(0.0, 1 - r - g - b) * details[3]
    else:
        dm = details[0]
    return _ClassLook(cm_lin, np.clip(base * dm * COLOUR_MULTIPLIER, 0, 1), splat_f, details)


def _class_colour(look: _ClassLook, lc: LandClass, x: np.ndarray, z: np.ndarray) -> np.ndarray:
    """The land class's linear colour at game (x, z)."""
    if look.indices is not None:
        # the detail the index texture names, under the colour map, combined as the other land classes are
        u = (x + lc.offset[0]) * lc.tile[0]
        v = -(z + lc.offset[1]) * lc.tile[1]
        h, w = look.indices.shape
        ix = (np.mod(u, 1.0) * w).astype(np.int64) % w
        iz = (np.mod(v, 1.0) * h).astype(np.int64) % h
        d = look.index_colours[look.indices[iz, ix]]
        c = _sample_wrap(look.colormap, u, v) if look.colormap is not None else 1 / COLOUR_MULTIPLIER
        return np.clip(c * d * COLOUR_MULTIPLIER, 0, 1)
    if look.colormap is None:
        return np.broadcast_to(look.mean, x.shape + (3,)).astype(np.float32)
    u = (x + lc.offset[0]) * lc.tile[0]
    v = -(z + lc.offset[1]) * lc.tile[1]
    c = _sample_wrap(look.colormap, u, v)
    if look.splat is not None:
        s = _sample_wrap(look.splat, u, v)
        r, g, b = s[..., 0:1], s[..., 1:2], s[..., 2:3]
        k = np.clip(1 - r - g - b, 0, 1)
        d = r * look.details[0] + g * look.details[1] + b * look.details[2] + k * look.details[3]
    else:
        d = look.details[0]
    return np.clip(c * d * COLOUR_MULTIPLIER, 0, 1)


def _weights_at(detail: LandDetail, x: np.ndarray, z: np.ndarray):
    """Per point: the cell index and the cell's seven weights (bilinear in the cell's weight texture)."""
    cfx = x / detail.cell_size - detail.origin[0]
    cfz = z / detail.cell_size - detail.origin[1]
    cx = np.clip(np.floor(cfx).astype(np.int64), 0, detail.cells[0] - 1)
    cz = np.clip(np.floor(cfz).astype(np.int64), 0, detail.cells[1] - 1)
    fx = np.clip(cfx - cx, 0, 1)
    fz = np.clip(cfz - cz, 0, 1)
    cell = cz * detail.cells[0] + cx
    out = np.zeros(x.shape + (DET_TEX_NUM,), np.float32)
    t = detail.tex_size
    for c in np.unique(cell):
        m = cell == c
        w = detail.weights(int(c))
        if w is None:
            ids = detail.ids[c // detail.cells[0], c % detail.cells[0]]
            if ids[0] != 0xFF:
                out[m, 0] = 1.0
            continue
        px = fx[m] * t - 0.5
        pz = fz[m] * t - 0.5
        x0 = np.clip(np.floor(px).astype(np.int64), 0, t - 1)
        z0 = np.clip(np.floor(pz).astype(np.int64), 0, t - 1)
        x1, z1 = np.minimum(x0 + 1, t - 1), np.minimum(z0 + 1, t - 1)
        ax = np.clip(px - x0, 0, 1)[:, None]
        az = np.clip(pz - z0, 0, 1)[:, None]
        wt = w.transpose(1, 2, 0)  # (rows = z, cols = x, 7)
        out[m] = ((wt[z0, x0] * (1 - ax) + wt[z0, x1] * ax) * (1 - az) + (wt[z1, x0] * (1 - ax) + wt[z1, x1] * ax) * az)
    return cell, out


def _rasterize_triangles(img: np.ndarray, verts_px: np.ndarray, faces: np.ndarray, colour: np.ndarray,
                         alpha: float = 1.0) -> int:
    """Fill triangles (pixel coordinates, x right, y down) into img (h, w, 3) float32. Returns pixels painted."""
    h, w = img.shape[:2]
    painted = 0
    tri = verts_px[faces]  # (m, 3, 2)
    lo = np.floor(tri.min(1)).astype(np.int64)
    hi = np.ceil(tri.max(1)).astype(np.int64)
    keep = (hi[:, 0] >= 0) & (lo[:, 0] < w) & (hi[:, 1] >= 0) & (lo[:, 1] < h)
    for t, a, b in zip(tri[keep], lo[keep], hi[keep]):
        x0, y0 = max(a[0], 0), max(a[1], 0)
        x1, y1 = min(b[0], w - 1), min(b[1], h - 1)
        if x1 < x0 or y1 < y0:
            continue
        gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        (ax, ay), (bx, by), (cx, cy) = t
        d = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
        if abs(d) < 1e-12:
            continue
        l1 = ((by - cy) * (gx - cx) + (cx - bx) * (gy - cy)) / d
        l2 = ((cy - ay) * (gx - cx) + (ax - cx) * (gy - cy)) / d
        inside = (l1 >= -1e-6) & (l2 >= -1e-6) & (l1 + l2 <= 1 + 1e-6)
        if not inside.any():
            continue
        sub = img[y0 : y1 + 1, x0 : x1 + 1]
        sub[inside] = sub[inside] * (1 - alpha) + colour * alpha
        painted += int(inside.sum())
    return painted


#: Ground-decal materials that are roads, paths or paved ground (physics material names, lower case, by part).
ROAD_MATERIALS = ("road", "asphalt", "concrete", "gravel", "pavement", "sett", "cobble")


def _is_road(material: str) -> bool:
    m = material.lower()
    return any(k in m for k in ROAD_MATERIALS)


def _decal_colours(tex: Textures, splines: list[Spline], decals: list[Decal]) -> list[np.ndarray | None]:
    """A linear colour per decal: the diffuse texture of the decal spline it lies along (`<asset>_tex_d`), else None."""
    cands = []
    for s in splines:
        a = spline_asset(s.name)
        if not a.startswith(("decal_", "ground_decal_")):
            continue
        m = tex.mean_linear(f"{a}_tex_d")
        if m is None:
            continue
        pl = s.polyline(4)[:, [0, 2]]
        cands.append((pl, m))
    out: list[np.ndarray | None] = []
    for d in decals:
        if not cands or not len(d.vertices):
            out.append(None)
            continue
        c = d.vertices.mean(0)
        best, best_d = None, 1e18
        for pl, m in cands:
            dd = float(np.min(((pl - c) ** 2).sum(1)))
            if dd < best_d:
                best, best_d = m, dd
        span = float(np.ptp(d.vertices, axis=0).max()) if len(d.vertices) > 1 else 0.0
        out.append(best if best_d <= (span * 0.5 + 30.0) ** 2 else None)
    return out


def land_mesh_textures(data: bytes, table: dict) -> list[str]:
    """The texture names of the land mesh's render data (`lmap`): its decals' textures among them.

    `LandMeshManager::loadMeshData` starts with `ShaderMatVdata::loadTexStr` (`prog/engine/shaders/matVdataLoad.cpp`):
    four counts, a byte size, then a header whose first table holds the names' offsets."""
    if "lmap" not in table:
        return []
    base = table["lmap"][0].start + 36
    (mesh_ofs,) = struct.unpack_from("<i", data, base)
    p = base + mesh_ofs + 16
    (size,) = struct.unpack_from("<i", data, p)
    hdr = data[p + 4 : p + 4 + size]
    ofs, cnt = struct.unpack_from("<II", hdr, 0)
    out = []
    for o in struct.unpack_from(f"<{cnt}i", hdr, ofs):
        if 0 <= o < len(hdr):
            out.append(hdr[o : hdr.index(b"\0", o)].decode("latin1"))
    return out


def _material_textures(tex: Textures, names: list[str]) -> dict[str, np.ndarray]:
    """Linear colours for road materials from the land mesh's decal textures whose names say what they are."""
    diffuse = [tex.clean(n) for n in names if tex.clean(n).endswith("_tex_d") and "decal" in n]
    out: dict[str, np.ndarray] = {}
    for key, words in (("sand", ("road_sand", "sand")), ("soil", ("road_soil", "road_dirt", "dirt", "soil")),
                       ("road", ("asphalt", "road"))):
        for w in words:
            hit = next((n for n in diffuse if w in n and "rail" not in n), None)
            m = tex.mean_linear(hit) if hit else None
            if m is not None:
                out[key] = m
                break
    return out


def _shore_textures(tex: Textures, names: list[str]) -> dict[str, np.ndarray]:
    """Linear colours for the non-road ground decals of the land mesh (beaches, cliffs), from its own textures
    whose names say what they are (detail textures excluded: they are tiling patterns, not colours)."""
    own = [n for n in map(tex.clean, names) if not n.startswith("detail_") and not n.endswith("_tex_r")]
    out: dict[str, np.ndarray] = {}
    for key, words in (("sand", ("beach", "shore", "border", "sand")), ("rocks", ("cliff", "rock"))):
        for w in words:
            hit = next((n for n in own if w in n and "road" not in n), None)
            m = tex.mean_linear(hit) if hit else None
            if m is not None:
                out[key] = m
                break
    return out


#: Linear colours for road materials when no decal texture says better (dry earth road, paving).
_ROAD_FALLBACK = {"soil": srgb_to_linear(np.array([0.48, 0.42, 0.33])),
                  "sand": srgb_to_linear(np.array([0.62, 0.56, 0.44])),
                  "default": srgb_to_linear(np.array([0.42, 0.41, 0.39]))}


def _ground_materials(tex: Textures, detail: LandDetail, looks: list) -> dict[str, np.ndarray]:
    """Linear colours for non-road decal materials: the land class that names the material as its physics
    material (`physMat*`), and for rock the level's cliff texture."""
    out: dict[str, np.ndarray] = {}
    for lc, lk in zip(detail.classes, looks):
        for k, v in lc.blk.params:
            if k.startswith("physMat") and isinstance(v, str) and not _is_road(v) and v not in out:
                if lc.splatting is None or k == "physMat":
                    out[v] = lk.mean
                else:  # the mask channel that carries this material
                    ch = {"physMatRed": 0, "physMatGreen": 1, "physMatBlue": 2, "physMatBlack": 3}.get(k)
                    if ch is not None and lk.colormap is not None:
                        out[v] = np.clip(lk.colormap.reshape(-1, 3).mean(0) * lk.details[ch] * COLOUR_MULTIPLIER, 0, 1)
    if detail.vertical:
        vm = tex.mean_linear(detail.vertical["texture"])
        if vm is not None:
            out.setdefault("rocks", np.clip(vm, 0, 1))
    return out


def terrain_colour(game, data: bytes, table: dict, rect: tuple[float, float, float, float], *,
                   metres_per_pixel: float = 2.0, max_pixels: int = 4096, texture_size: int = 512,
                   roads: bool = True, heightmap=None, textures: Textures | None = None,
                   log=None) -> tuple[np.ndarray, dict]:
    """A top-down colour image of the ground over `rect` = (x0, z0, x1, z1) in game metres.

    The image is RGB uint8, `(rows, cols, 3)`, its top row the north edge (z1) and its first column x0: the
    tactical-map convention of `level._uv`. At most `max_pixels` a side (the resolution drops to fit).
    `heightmap` (a `dagorlevel.Heightmap`), when given, blends the level's cliff texture in on steep slopes.
    `textures` is a `Textures` to reuse between levels (it caches decoded images); one is made otherwise.
    Returns the image and what was read."""
    t0 = time.time()
    x0, z0, x1, z1 = rect
    mpp = max(metres_per_pixel, (x1 - x0) / max_pixels, (z1 - z0) / max_pixels)
    W = max(int(round((x1 - x0) / mpp)), 1)
    H = max(int(round((z1 - z0) / mpp)), 1)
    info: dict = {"rect": [x0, z0, x1, z1], "pixels": [W, H], "metresPerPixel": [(x1 - x0) / W, (z1 - z0) / H]}
    detail = read_land_detail(data, table)
    if detail is None:
        raise TerrainError("the level has no land mesh, so no land classes")
    tex = textures or Textures(game.root)
    looks = [_class_look(tex, lc, texture_size) for lc in detail.classes]
    info["landClasses"] = [{"name": lc.name, "colormap": tex.clean(lc.colormap or "") or None,
                            "size": [1 / lc.tile[0], 1 / lc.tile[1]],
                            "mean": [round(float(v), 3) for v in linear_to_srgb(lk.mean)]}
                           for lc, lk in zip(detail.classes, looks)]
    info["weightMap"] = {"cells": list(detail.cells), "cellSize": detail.cell_size, "texels": detail.tex_size,
                         "metresPerTexel": detail.cell_size / detail.tex_size}
    vert = None
    if heightmap is not None and detail.vertical:
        vm = tex.mean_linear(detail.vertical["texture"])
        if vm is not None:
            vert = vm
    img = np.zeros((H, W, 3), np.float32)
    cliff = None  # the vertical (cliff) texture's share on steep ground, applied over the decals at the end
    if vert is not None and abs(detail.vertical["blendFromY"] - detail.vertical["blendToY"]) > 1e-6:
        cliff = np.zeros((H, W), np.float32)
    xs = x0 + (np.arange(W) + 0.5) * (x1 - x0) / W
    strip = max(1, 2_000_000 // W)
    for r0 in range(0, H, strip):
        r1 = min(H, r0 + strip)
        zs = z1 - (np.arange(r0, r1) + 0.5) * (z1 - z0) / H
        gx, gz = np.meshgrid(xs, zs)
        cell, wts = _weights_at(detail, gx, gz)
        acc = np.zeros(gx.shape + (3,), np.float32)
        total = np.zeros(gx.shape, np.float32)
        ids_grid = detail.ids.reshape(-1, DET_TEX_NUM)[cell]  # (rows, cols, 7)
        for slot in range(DET_TEX_NUM):
            w = wts[..., slot]
            lcs = ids_grid[..., slot]
            for lc_id in np.unique(lcs[w > 1e-3]):
                if lc_id == 0xFF or lc_id >= len(detail.classes):
                    continue
                m = (lcs == lc_id) & (w > 1e-3)
                col = _class_colour(looks[lc_id], detail.classes[lc_id], gx[m], gz[m])
                acc[m] += col * w[m][:, None]
                total[m] += w[m]
        ok = total > 1e-4
        acc[ok] /= total[ok][:, None]
        acc[~ok] = _FALLBACK
        if cliff is not None:
            ny = _normal_y(heightmap, gx, gz)
            b0, b1 = detail.vertical["blendFromY"], detail.vertical["blendToY"]
            # vertical_param: t = (normal.y - blendToY) / (blendFromY - blendToY) is the flat ground's share
            cliff[r0:r1] = 1.0 - np.clip((ny - b1) / (b0 - b1), 0, 1)
        img[r0:r1] = acc
    info["texturesMissing"] = sorted(tex.missing)
    if roads:
        pm = read_phys_map(data, table)
        splines = read_splines(data, table)
        painted = ground_px = 0
        n_dec = 0
        road_runs: list = []
        ground_runs: list = []
        lm_textures = land_mesh_textures(data, table)
        ground = _ground_materials(tex, detail, looks)
        ground.update({k: v for k, v in _shore_textures(tex, lm_textures).items() if k in ground})
        by_material = _material_textures(tex, lm_textures)
        if pm is not None and pm.decals:
            colours = _decal_colours(tex, splines, pm.decals)
            for d, c in zip(pm.decals, colours):
                vpx = np.stack([(d.vertices[:, 0] - x0) / (x1 - x0) * W, (z1 - d.vertices[:, 1]) / (z1 - z0) * H], 1)
                if vpx[:, 0].max() < 0 or vpx[:, 0].min() > W or vpx[:, 1].max() < 0 or vpx[:, 1].min() > H:
                    continue
                for mat, f in d.runs:
                    if not _is_road(mat):
                        continue
                    if len(f) and f.max() >= len(vpx):
                        continue
                    col = c
                    if col is None:
                        key = "sand" if "sand" in mat.lower() else "soil" if "soil" in mat.lower() else "road"
                        col = by_material.get(key)
                        if col is None:
                            col = _ROAD_FALLBACK.get(key, _ROAD_FALLBACK["default"])
                    road_runs.append((vpx, f, np.clip(col, 0, 1)))
                for mat, f in d.runs:
                    if _is_road(mat) or mat not in ground or (len(f) and f.max() >= len(vpx)):
                        continue
                    ground_runs.append((vpx, f, ground[mat]))
            # ground decals (beaches, rock) first, the roads over them
            for vpx, f, col in ground_runs:
                ground_px += _rasterize_triangles(img, vpx, f, col, 0.8)
            for vpx, f, col in road_runs:
                painted += _rasterize_triangles(img, vpx, f, col, 0.9)
                n_dec += 1
        info["roads"] = {"decalRuns": n_dec, "pixels": painted, "groundDecalPixels": ground_px,
                         "groundDecalMaterials": sorted(ground),
                         "physMap": None if pm is None else {"materials": pm.materials, "size": pm.size,
                                                             "metresPerPixel": pm.scale, "decals": len(pm.decals)},
                         "splines": len(splines)}
    if cliff is not None:
        img = img * (1 - cliff[..., None]) + np.clip(vert, 0, 1) * cliff[..., None]
        info["cliffPixels"] = int((cliff > 0.5).sum())
    out = (linear_to_srgb(img) * 255.0 + 0.5).astype(np.uint8)
    info["seconds"] = round(time.time() - t0, 2)
    if log:
        log(f"  terrain colour: {W}x{H} px at {info['metresPerPixel'][0]:.2f} m, {len(detail.classes)} land classes, "
            f"{info['seconds']} s")
    return out, info


def _normal_y(hm, x: np.ndarray, z: np.ndarray) -> np.ndarray:
    """The heightmap's up component of the normal at game (x, z) (1 where it does not reach)."""
    h, w = hm.heights.shape
    c = (x - hm.origin_x) / hm.cell
    r = (z - hm.origin_z) / hm.cell
    inside = (c >= 1) & (c < w - 2) & (r >= 1) & (r < h - 2)
    ci = np.clip(np.round(c).astype(np.int64), 1, w - 2)
    ri = np.clip(np.round(r).astype(np.int64), 1, h - 2)
    dx = (hm.heights[ri, ci + 1] - hm.heights[ri, ci - 1]) / (2 * hm.cell)
    dz = (hm.heights[ri + 1, ci] - hm.heights[ri - 1, ci]) / (2 * hm.cell)
    ny = 1.0 / np.sqrt(1 + dx * dx + dz * dz)
    return np.where(inside, ny, 1.0)


def roads(game, data: bytes, table: dict) -> list[dict]:
    """The level's road-like splines as polylines: `{"name", "asset", "points": (n, 3) game x, y, z}`.

    Widths are not in the spline data (they belong to the spline's asset); the painted footprint in
    `terrain_colour` comes from the physics map's decals instead."""
    out = []
    for s in read_splines(data, table):
        a = spline_asset(s.name)
        if "road" in a or "rail" in a or "path" in a:
            out.append({"name": s.name, "asset": a, "points": s.polyline(8)})
    return out
