"""
A War Thunder level binary (`<War Thunder>/levels/<level>.bin`, form `DBLD`):
its terrain heightmap, the land mesh's collision geometry and its bounds.

Everything here was written from the Dagor Engine's BSD-3-Clause source
(github.com/GaijinEntertainment/DagorEngine); file and function names are given
where each part comes from. No game code was disassembled.

- The file (`prog/engine/scene/loadLevel.cpp`): `DBLD`, version `3x64`, a
  texture count, then tagged blocks until `END`. A block is a 32-bit length
  (top two bits: compression, 1 zstd, 2 Oodle) followed by a 4-byte tag.
- `HM2`, the heightmap (`prog/gameLibs/heightmap/heightmapPhysHandler.cpp`,
  `HeightmapPhysHandler::loadDump`): cell size, minimum height, height scale,
  world offset (x, z), width | version << 24, height | mirror << 31, an
  exclusion box, and for version 2 a chunk word. Version 2 data
  (`prog/engine/heightMapLand/compressedHeightmap.cpp`) is blocks of 2^s x 2^s
  samples, each a (min, delta) pair and 8-bit values delta-coded along the
  block; height = min + (v * delta + 127) / 255, metres = hMin + height *
  hScale / 65535. Versions 0 and 1 are one compressed 16-bit raster (1: each
  row delta-coded).
- `lmap`, the land mesh (`prog/gameLibs/landMesh/lmeshManager.cpp`,
  `LandMeshManager::loadDump`; `landRayTracerSoA4.cpp`, `loadStreamToDump`):
  the header gives offsets; the land ray tracer's dump (`LTdump`) holds, per
  cell, vertices packed as 16-bit lanes with a scale and offset, and 16-bit
  cell-local triangle indices. That is the land's collision surface, the same
  triangles the game finds the ground with where there is no heightmap.
- `WBBX`, the world box: min and max x, y, z.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from . import oodle

_HIER = [0, 1, 5, 21, 85, 341, 1365, 5461, 21845, 87381, 349525, 1398101, 5592405, 22369621, 89478485]
ZSTD, OODLE = 1, 2


class LevelError(ValueError):
    pass


def unpack(fmt: int, data: bytes, size: int) -> bytes:
    if fmt == OODLE:
        return oodle.decompress(data, size)
    if fmt == ZSTD:
        import zstandard

        out = zstandard.ZstdDecompressor().decompressobj().decompress(data)
        if len(out) < size:
            raise LevelError(f"zstd block gave {len(out)} bytes, {size} expected")
        return out[:size]
    if fmt == 0 and len(data) >= size:
        return data[:size]
    raise LevelError(f"block compression {fmt} (LZMA) is not read")


@dataclass
class Block:
    tag: str
    start: int  # first byte after the tag
    end: int


def blocks(data: bytes) -> dict[str, list[Block]]:
    """The level's top-level blocks, by tag."""
    if data[:4] != b"DBLD":
        raise LevelError("not a Dagor level binary (no DBLD)")
    if data[4:8] != b"3x64":
        raise LevelError(f"level binary version {data[4:8]!r}, only 3x64 is read")
    out: dict[str, list[Block]] = {}
    p = 12
    while p + 8 <= len(data):
        (word,) = struct.unpack_from("<I", data, p)
        length = word & 0x3FFFFFFF
        tag = data[p + 4 : p + 8].lstrip(b"\0").decode("latin1")
        out.setdefault(tag, []).append(Block(tag, p + 8, p + 4 + length))
        if tag == "END":
            break
        p += 4 + length
    return out


@dataclass
class Heightmap:
    heights: np.ndarray  # (rows = z, cols = x) metres, float32
    cell: float
    origin_x: float
    origin_z: float
    version: int
    mirror: bool


def _sub(data: bytes, p: int) -> tuple[int, int, int]:
    (word,) = struct.unpack_from("<I", data, p)
    return p + 4, p + 4 + (word & 0x3FFFFFFF), word >> 30


def read_heightmap(data: bytes, block: Block) -> Heightmap:
    s = block.start
    cell, hmin, hscale, ox, oz = struct.unpack_from("<5f", data, s)
    wv, hm = struct.unpack_from("<2I", data, s + 20)
    version, w, h = wv >> 24, wv & 0xFFFFFF, hm & 0x7FFFFFFF
    p = s + 44
    if version == 2:
        (chunk,) = struct.unpack_from("<I", data, p)
        p += 4
        shift = chunk & 0xFF
        hrb = (1 << ((chunk >> 8) & 0xF)) if chunk & 0xF00 else 0
        chunk_bytes = chunk & ~0xFFF
        shift = min(shift, 5)
        bw, bh = w >> shift, h >> shift
        nb, bsz = bw * bh, 1 << (2 * shift)
        levels = (w // hrb).bit_length() - 1 if hrb else 0
        info_size, hrb_size = nb * 4, _HIER[levels] * 16
        var = np.empty(nb * bsz, np.uint8)
        if chunk_bytes == 0:
            a, b, f = _sub(data, p)
            raw = unpack(f, data[a:b], info_size + nb * bsz + hrb_size)
            var[:] = np.frombuffer(raw, np.uint8, nb * bsz, info_size)
        else:
            per = chunk_bytes >> (2 * shift)
            count = (nb + per - 1) // per
            a, b, f = _sub(data, p)
            raw = unpack(f, data[a:b], info_size + hrb_size)
            p = b
            for ci in range(1, count + 1):
                b0, b1 = (ci - 1) * per, min(nb, ci * per)
                a, b, f = _sub(data, p)
                var[b0 * bsz : b1 * bsz] = np.frombuffer(unpack(f, data[a:b], (b1 - b0) * bsz), np.uint8)
                p = b
        info = np.frombuffer(raw, "<u2", nb * 2).reshape(nb, 2).astype(np.uint32)
        v = (np.cumsum(var.reshape(nb, bsz).astype(np.uint32), axis=1) & 0xFF)
        units = info[:, :1] + (v * info[:, 1:2] + 127) // 255
        k = 1 << shift
        units = units.reshape(bh, bw, k, k).transpose(0, 2, 1, 3).reshape(h, w)
    elif version in (0, 1):
        a, b, f = _sub(data, p)
        raw = unpack(f, data[a:b], w * h * 2)
        units = np.frombuffer(raw, "<u2").reshape(h, w).astype(np.uint32)
        if version == 1:
            units = np.cumsum(units, axis=1) & 0xFFFF
    else:
        raise LevelError(f"heightmap version {version} is not read")
    heights = (hmin + units.astype(np.float64) * (hscale / 65535.0)).astype(np.float32)
    return Heightmap(heights, float(cell), float(ox), float(oz), version, bool(hm >> 31))


@dataclass
class LandMesh:
    vertices: np.ndarray  # (n, 3) float32, game x, y, z
    faces: np.ndarray  # (m, 3) uint32
    cell_size: float
    grid: tuple[int, int]


def read_landmesh(data: bytes, block: Block) -> LandMesh | None:
    """The land ray tracer's triangles, or None where the level has none (it then relies on the heightmap)."""
    s = block.start
    if data[s : s + 4] != b"lndm":
        raise LevelError("land mesh block without lndm")
    version, _gcs, _lcs, _mx, _my, _ox, _oy, use_tile = struct.unpack_from("<iffiiiii", data, s + 4)
    if version != 4:
        raise LevelError(f"land mesh version {version} is not read")
    base = s + 36
    _mesh_ofs, _detail_ofs, tile_ofs, ray_ofs = struct.unpack_from("<4i", data, base)
    if ray_ofs <= 0:
        # Levels of the game's 2.61 builds carry no land tracer: the land is the render mesh alone.
        return read_render_landmesh(data, block)
    p = base + tile_ofs
    if use_tile:
        (n,) = struct.unpack_from("<i", data, p)
        p += 4 + ((n + 3) & ~3) + 8
    (word,) = struct.unpack_from("<I", data, p)
    fmt, length, a = word >> 30, word & 0x3FFFFFFF, p + 4
    if fmt == OODLE:
        (src,) = struct.unpack_from("<i", data, a)
        raw = oodle.decompress(data[a + 4 : a + length], src)
    elif fmt == ZSTD:
        import zstandard

        raw = zstandard.ZstdDecompressor().decompressobj().decompress(data[a : a + length])
    else:
        raise LevelError("land tracer packed with LZMA is not read")
    r = raw[4:]
    if r[:6] != b"LTdump":
        raise LevelError("land tracer is not an LTdump")
    cx, cy, cs = struct.unpack_from("<iif", r, 6)
    q = 54
    (n,) = struct.unpack_from("<i", r, q)
    q += 4
    rec = np.frombuffer(r, np.uint8, n * 64, q).view(
        [("ofs", "<f4", 4), ("scale", "<f4", 4), ("maxHt", "<f4"), ("grid", "<u4", 3),
         ("faces", "<u4"), ("verts", "<u4"), ("resv", "<u4", 2)]
    )
    q += n * 64
    for _ in range(2):
        (k,) = struct.unpack_from("<i", r, q)
        q += 4 + 4 * k
    (nf,) = struct.unpack_from("<i", r, q)
    q += 4
    faces = np.frombuffer(r, "<u2", nf, q)
    q += nf * 2
    (nv,) = struct.unpack_from("<i", r, q)
    q += 4
    packed = np.frombuffer(r, "<u2", nv * 4, q).reshape(nv, 4)
    vs, fs, base_v = [], [], 0
    for i in range(n):
        v0 = int(rec["verts"][i])
        v1 = int(rec["verts"][i + 1]) if i + 1 < n else nv
        f0 = int(rec["faces"][i])
        f1 = int(rec["faces"][i + 1]) if i + 1 < n else nf
        if v1 <= v0 or f1 - f0 < 3:
            continue
        local = faces[f0:f1].astype(np.int64)
        if local.max() >= v1 - v0:
            raise LevelError(f"land tracer cell {i} indexes past its vertices")
        vs.append(packed[v0:v1, :3] * rec["scale"][i][:3] + rec["ofs"][i][:3])
        fs.append(local[: (len(local) // 3) * 3].reshape(-1, 3) + base_v)
        base_v += v1 - v0
    if not vs:
        return None
    return LandMesh(np.concatenate(vs).astype(np.float32), np.concatenate(fs).astype(np.uint32), float(cs), (cx, cy))


def _sub_block(data: bytes, p: int) -> tuple[int, int]:
    """A Dagor `beginBlock`: a 32-bit length (flags in the top two bits); the body's start and end."""
    (w,) = struct.unpack_from("<I", data, p)
    return p + 4, p + 4 + (w & 0x3FFFFFFF)


def _mesh_elems(data: bytes, a: int, b: int) -> list[tuple[int, int, int, int, int, int]]:
    """A `ShaderMesh` dump's elements (`dag_shaderMesh.h`, `RElem`): (vdata, sv, numv, si, numf, base vertex)."""
    from .rendinst import _RELEM

    if b - a < 36:
        return []
    ep, en = struct.unpack_from("<II", data, a)
    out = []
    for k in range(en):
        _e, _mat, vd, _o, sv, nv, si, nf, bv = struct.unpack_from("<QQQiiiiii", data, a + ep + _RELEM * k)
        out.append((int(vd), sv, nv, si, nf, bv))
    return out


def read_render_landmesh(data: bytes, block: Block) -> LandMesh | None:
    """The land's render mesh, the finest LOD of every cell (`LandMeshManager::loadMeshData`,
    `prog/gameLibs/landMesh/lmeshManager.cpp`; positions decoded as `LandMeshRenderer::getCellState` does).

    The mesh data starts with four counts (textures, materials, vertex datas, the header size with its packing in
    the top bits), the texture-name table, then the vertex data laid out as a render instance's
    (`rendinst.read_resource`); then a block of cells (`x + y * mapSizeX`), each a block of LOD blocks (a
    `ShaderMesh` each), the decal, the combined and optionally the patches mesh; then the cells' bounding boxes.
    Positions are SHORT4, -32767..32767 over the cell in x and z (cell centre `landCellSize * (x + originX + 0.5)`)
    and over the whole land's height range (the union of the cell boxes) in y."""
    from . import rendinst as ri

    s = block.start
    _version, _gcs, lcs, mx, my, ox, oy, _use_tile = struct.unpack_from("<iffiiiii", data, s + 4)
    base = s + 36
    mesh_ofs, detail_ofs = struct.unpack_from("<2i", data, base)
    if mesh_ofs <= 0 or detail_ofs <= mesh_ofs or mx <= 0 or my <= 0:
        return None
    p = base + mesh_ofs
    _n_tex, _n_mat, n_vd, hdr_w = struct.unpack_from("<iiiI", data, p)
    p += 16
    (sz,) = struct.unpack_from("<i", data, p)
    p += 4 + sz
    if (hdr_w & 0xE0000000) == 0xC0000000:
        hdr_sz = hdr_w & ~0xC0000000
        stream, p = ri._block(data, p)
    elif hdr_w & 0xC0000000:
        raise LevelError("land mesh vertex data packed with zlib or LZMA is not read")
    else:
        hdr_sz = hdr_w
        vdp, vdn = struct.unpack_from("<II", data, p + 16)
        total = 0
        for i in range(vdn):
            vn, a, bb, fl = struct.unpack_from("<IIII", data, p + vdp + 32 * i)
            total += vn * (a & 0xFF) + (((a >> 8) | ((bb >> 28) << 24)) if fl & ri._VDATA_PACKED_IB else bb & 0xFFFFFFF)
        stream = data[p : p + hdr_sz + total]
        p += hdr_sz + total
    vdp, vdn = struct.unpack_from("<II", stream, 16)
    if vdn != n_vd:
        raise LevelError(f"land mesh: {vdn} vertex buffers where the header says {n_vd}")
    vdata, at = [], hdr_sz
    for i in range(vdn):
        vn, a, bb, fl, dp, dn = struct.unpack_from("<IIIIII", stream, vdp + 32 * i)
        stride, isz = a & 0xFF, bb & 0xFFFFFFF
        packed = ((a >> 8) | ((bb >> 28) << 24)) if fl & ri._VDATA_PACKED_IB else isz
        decl = [(t >> 16, u, ui) for t, u, ui, _s in (struct.unpack_from("<iihH", stream, dp + 12 * k) for k in range(dn))]
        vdata.append(ri._Vdata(vn, stride, isz, packed, fl, decl, at))
        at += vn * stride + packed
    if at > len(stream):
        raise LevelError("land mesh vertex data ends early")

    cache: dict[int, tuple[np.ndarray, np.ndarray]] = {}

    def buffers(i: int) -> tuple[np.ndarray, np.ndarray]:
        if i not in cache:
            vd = vdata[i]
            t, usage, _ui = vd.decl[0]
            if usage != ri._USAGE_POS or t != ri._SHORT4 or vd.stride % 2:
                raise LevelError(f"land mesh vertex buffer {i}: position type {t} is not read")
            vb = np.frombuffer(stream, "<i2", vd.verts * vd.stride // 2, vd.at).reshape(vd.verts, vd.stride // 2)
            ib_at = vd.at + vd.verts * vd.stride
            wide = bool(vd.flags & ri._VDATA_I32) or (vd.verts > 65536 and not vd.flags & 0x20)
            count = vd.idx_bytes // (4 if wide else 2)
            if vd.flags & ri._VDATA_PACKED_IB:
                idx = ri.decode_index_sequence(stream[ib_at : ib_at + vd.packed], count)
            else:
                idx = np.frombuffer(stream, "<u4" if wide else "<u2", count, ib_at).astype(np.uint32)
            cache[i] = (vb[:, :3].astype(np.float32) / 32767.0, idx)
        return cache[i]

    a0, _e0 = _sub_block(data, p)
    cells: list[list[tuple[int, int, int, int, int, int]]] = []
    q = a0
    for _c in range(mx * my):
        ca, ce = _sub_block(data, q)
        la, le = _sub_block(data, ca)
        lod0: list = []
        if la < le:
            ma, me = _sub_block(data, la)
            lod0 = _mesh_elems(data, ma, me)
        cells.append(lod0)
        q = ce
    ba, _be = _sub_block(data, q)
    boxes = np.frombuffer(data, "<f4", mx * my * 6, ba).reshape(-1, 6)
    y0, y1 = float(boxes[:, 1].min()), float(boxes[:, 4].max())
    half_y, mid_y = 0.5 * (y1 - y0), 0.5 * (y1 + y0)
    vs, fs, nbase = [], [], 0
    for c, elems in enumerate(cells):
        cx, cy = c % mx + ox, c // mx + oy
        centre = np.array([lcs * (cx + 0.5), mid_y, lcs * (cy + 0.5)], np.float32)
        scale = np.array([lcs * 0.5, half_y, lcs * 0.5], np.float32)
        for vd, _sv, _nv, si, nf, bv in elems:
            if nf <= 0:
                continue
            pos, idx = buffers(vd)
            tri = idx[si : si + 3 * nf].astype(np.int64) + bv
            if len(tri) < 3 * nf or tri.max() >= len(pos):
                raise LevelError(f"land mesh cell {c} indexes past its vertices")
            used, local = np.unique(tri, return_inverse=True)
            vs.append(pos[used] * scale + centre)
            fs.append(local.reshape(-1, 3) + nbase)
            nbase += len(used)
    if not vs:
        return None
    return LandMesh(np.concatenate(vs).astype(np.float32), np.concatenate(fs).astype(np.uint32), float(lcs), (mx, my))


@dataclass
class WaterHeightmap:
    """The water surface of levels whose rivers slope (`WHM`, `prog/gameLibs/fftWater/fftWater.cpp`:
    `load_heightmap`, `WaterHeightmap::loadData` and `getHeightmapDataBilinear`): a grid of cells, each
    either flat (the level's water level) or pointing at a 130x130 page of 16-bit heights."""

    grid_size: int
    pages_x: int
    scale: int
    height_offset: float
    height_scale: float
    tc: tuple[float, float, float, float]  # offset x, z, scale x, z: grid = (world * scale + offset) * size
    pages: np.ndarray  # (pages_y * 130, pages_x * 130) uint16
    grid: np.ndarray  # (size, size) uint16

    def extent(self) -> tuple[float, float, float, float]:
        ox, oz, sx, sz = self.tc
        return (-ox / sx, -oz / sz, (1 - ox) / sx, (1 - oz) / sz)

    def sample(self, x: np.ndarray, z: np.ndarray) -> np.ndarray:
        """Water height at game (x, z), NaN where the level's flat water applies."""
        ox, oz, sx, sz = self.tc
        n = self.grid_size
        gx = (np.asarray(x, np.float64) * sx + ox) * n
        gz = (np.asarray(z, np.float64) * sz + oz) * n
        ix, iz = np.floor(gx).astype(np.int64), np.floor(gz).astype(np.int64)
        inside = (ix >= 0) & (ix < n) & (iz >= 0) & (iz < n)
        cell = np.full(gx.shape, 0xFFFF, np.int64)
        cell[inside] = self.grid[iz[inside], ix[inside]]
        out = np.full(gx.shape, np.nan)
        ok = cell != 0xFFFF
        if not ok.any():
            return out
        page, ps = 128, 130
        scale = np.where(cell & 1, 1.0, float(self.scale))
        fx = np.mod(gx / scale, 1.0)
        fz = np.mod(gz / scale, 1.0)
        fx = (fx * (page / (page + 2.0)) + 1.0 / (page + 2.0)) * ps
        fz = (fz * (page / (page + 2.0)) + 1.0 / (page + 2.0)) * ps
        cx = np.clip(fx.astype(np.int64), 1, ps - 2) + ((cell >> 1) & 0x7F) * ps
        cz = np.clip(fz.astype(np.int64), 1, ps - 2) + ((cell >> 8) & 0xFF) * ps
        wr, wt = fx - np.floor(fx), fz - np.floor(fz)
        h, w = self.pages.shape
        cx, cz = np.clip(cx, 0, w - 2), np.clip(cz, 0, h - 2)
        p = self.pages.astype(np.float64)
        v = ((p[cz, cx] * (1 - wt) + p[cz + 1, cx] * wt) * (1 - wr) + (p[cz, cx + 1] * (1 - wt) + p[cz + 1, cx + 1] * wt) * wr)
        val = np.round(v) * (self.height_scale / 65535.0) + self.height_offset
        out[ok] = val[ok]
        return out


def read_water_heightmap(data: bytes, block: Block) -> WaterHeightmap:
    s = block.start
    gs, px, py, scale = struct.unpack_from("<4i", data, s)
    ho, hs, tx, ty, tz, tw = struct.unpack_from("<6f", data, s + 16)
    (word,) = struct.unpack_from("<I", data, s + 40)
    fmt, n, a = word >> 30, word & 0x3FFFFFFF, s + 44
    ps = 130
    size = px * py * ps * ps * 2 + gs * gs * 2
    raw = unpack(fmt, data[a : a + n], size)
    pages = np.frombuffer(raw, "<u2", px * py * ps * ps).reshape(py * ps, px * ps)
    pages = (np.cumsum(pages.astype(np.uint32), axis=1) & 0xFFFF).astype(np.uint16)  # each row delta-coded
    grid = np.frombuffer(raw, "<u2", gs * gs, px * py * ps * ps * 2).reshape(gs, gs)
    return WaterHeightmap(gs, px, scale, ho, hs, (tx, ty, tz, tw), pages, grid)


def world_box(data: bytes, bl: dict[str, list[Block]]) -> tuple[float, ...] | None:
    if "WBBX" not in bl:
        return None
    return struct.unpack_from("<6f", data, bl["WBBX"][0].start)


@dataclass
class Level:
    name: str
    tags: list[str]
    heightmap: Heightmap | None
    landmesh: LandMesh | None
    box: tuple[float, ...] | None
    data: bytes = b""  # the whole file, for the readers of other blocks
    table: dict | None = None  # its block table


def read_level(path: str | Path) -> Level:
    path = Path(path)
    data = path.read_bytes()
    bl = blocks(data)
    hm = read_heightmap(data, bl["HM2"][0]) if "HM2" in bl else None
    lm = read_landmesh(data, bl["lmap"][0]) if "lmap" in bl else None
    return Level(path.stem, list(bl), hm, lm, world_box(data, bl), data, bl)


def scan(path: str | Path) -> tuple[dict[str, list[Block]], dict[str, bytes]]:
    """The block table by seeking from header to header, with the first 64 bytes of each block."""
    out: dict[str, list[Block]] = {}
    heads: dict[str, bytes] = {}
    with Path(path).open("rb") as fh:
        head = fh.read(12)
        if head[:4] != b"DBLD" or head[4:8] != b"3x64":
            raise LevelError("not a Dagor 3x64 level binary")
        p = 12
        while True:
            fh.seek(p)
            h = fh.read(8)
            if len(h) < 8:
                break
            (word,) = struct.unpack_from("<I", h, 0)
            length = word & 0x3FFFFFFF
            tag = h[4:8].lstrip(b"\0").decode("latin1")
            out.setdefault(tag, []).append(Block(tag, p + 8, p + 4 + length))
            heads.setdefault(tag, fh.read(min(64, max(length - 4, 0))))
            if tag == "END":
                break
            p += 4 + length
    return out, heads


def summary(path: str | Path) -> dict:
    """What a level holds, from its block headers alone (cheap: decompresses nothing)."""
    path = Path(path)
    bl, heads = scan(path)
    out: dict = {"level": path.stem, "bytes": path.stat().st_size, "blocks": sorted(bl)}
    if "HM2" in heads:
        cell, _hmin, _hs, ox, oz = struct.unpack_from("<5f", heads["HM2"], 0)
        wv, hm = struct.unpack_from("<2I", heads["HM2"], 20)
        w, h = wv & 0xFFFFFF, hm & 0x7FFFFFFF
        out["heightmap"] = {"samples": [w, h], "cell": cell, "x": [ox, ox + w * cell], "z": [oz, oz + h * cell]}
    if "WBBX" in heads:
        out["box"] = [round(v, 1) for v in struct.unpack_from("<6f", heads["WBBX"], 0)]
    if "lmap" in heads and heads["lmap"][:4] == b"lndm":
        ray = struct.unpack_from("<i", heads["lmap"], 48)[0]
        out["landTracer"] = ray > 0
    return out
