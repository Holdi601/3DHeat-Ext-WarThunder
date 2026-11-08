"""
Objects the land classes generate at run time: the forests, bushes, stones and
town blocks a War Thunder level does not store instance by instance, but asks
the render-instance generator to scatter where its land-class masks say, the
same way every time.

Written from the Dagor Engine's BSD-3-Clause source
(github.com/GaijinEntertainment/DagorEngine); no game code was disassembled.

- The level's generator dump (`RIGz`, `prog/gameLibs/rendInst/riGen/riGenData.h`,
  `rendInstGen.cpp`: `RendInstGenData::create`): after the dump come the
  exclusion ("sweep") mask and one mask per land class, each a
  `RoHugeHierBitMap2d<4, 3>` (`prog/dagorInclude/util/dag_roHugeHierBitMap2d.h`,
  `dag_hierBitMap2d.h`); every cell lists the land classes that cover it.
- The land class itself (game resource class `0x03FB59C4`,
  `rendInstGenLand.cpp`: `AssetData::load`, `loadTiledEntities`,
  `loadPlantedEntities`; `riGen/landClassData.h`, `riGen/multiPointData.h`): a
  packed read-only BLK (`prog/dagorInclude/ioSys/dag_roDataBlock.h`,
  `prog/engine/ioSys/roDataBlk.cpp`), then the density maps of its planted
  groups. Its objects are the pack's references to the land class
  (`prog/engine/gameRes/grpData.h`), render instance and collision in pairs.
- Generation (`rendInstGen.cpp`: `precomputeCell` / `generateCell`, eight by
  eight sub-cells per cell; `riGen/genObjByMask.h`: tiled entities, a pattern
  repeated over the land; `riGen/genObjByDensGridMask.h`: planted entities,
  scattered by density over a grid or a density map; `riGen/genObjUtil.h`:
  placement, orientation, random rotation and scale) with the generator's
  own random numbers (`prog/gameLibs/publicInclude/gameMath/objgenPrng.h`).

What is the same as the game: which spots are tried, in which order, with
which random numbers, and which of them the land-class masks and the level's
exclusion mask let through; the object picked at each spot, its rotation,
scale and height offset. What is approximated: the ground height and normal
come from the caller's height function (the game traces a ray down onto the
ground and, for some land classes, onto collision); the exclusion boxes the
game registers at run time (`full_sweep_box_itm_list`) are not known here;
objects with an impostor (trees) are kept as a yaw and a uniform scale, where
the game snaps the yaw to the impostor's rotation palette; the de-tiling
cluster walk of newer engine versions is not applied (the levels read here
carry no de-tiling data).
"""

from __future__ import annotations

import re
import struct
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

LANDCLASS_CLASS = 0x03FB59C4
RENDINST_CLASS = 0x77F8232F
SUBCELL_DIV = 8
_CELL = 552
_M32 = 0xFFFFFFFF
_A, _C = 0x41C64E6D, 0x3039
f32 = np.float32

ORIENT_WORLD, ORIENT_NORMAL, ORIENT_NORMAL_XZ, ORIENT_WORLD_XZ = range(4)
MP_NONE, MP_YZ, MP_XY, MP_3POINT = range(4)

KINDS = ("trees", "bushes", "grass", "buildings", "props")


class LandGenError(ValueError):
    pass


# --- the generator's random numbers (objgenPrng.h) -------------------------------------------------------


def _nxt(s: int) -> int:
    return (s * _A + _C) & _M32


def _jump(k: int) -> tuple[int, int]:
    """(a, c) with LCG^k(s) = a * s + c (mod 2^32)."""
    a, c = 1, 0
    for _ in range(k):
        a, c = (a * _A) & _M32, (c * _A + _C) & _M32
    return a, c


_JUMP9 = _jump(9)
_TABLE_A = np.array([_jump(k)[0] for k in range(1, 10)], np.uint64)
_TABLE_C = np.array([_jump(k)[1] for k in range(1, 10)], np.uint64)


def _states(seeds: np.ndarray, k: int) -> np.ndarray:
    """LCG^k of each seed (k >= 1), vectorised."""
    s = seeds.astype(np.uint64)
    return ((s * _TABLE_A[k - 1] + _TABLE_C[k - 1]) & _M32).astype(np.uint64)


def _val(states: np.ndarray) -> np.ndarray:
    """rnd(): the 15 bits the generator takes from a state."""
    return ((states >> np.uint64(16)) & np.uint64(0x7FFF)).astype(np.int64)


def _seq_states(seed: int, n: int) -> np.ndarray:
    """States LCG^1 .. LCG^n of one seed."""
    out = np.empty(n, np.uint64)
    s = seed
    for i in range(n):
        s = _nxt(s)
        out[i] = s
    return out


def _frnd(v):
    return (np.asarray(v, np.float32) / f32(32768.0)).astype(np.float32)


def _srnd(v):
    return ((np.asarray(v, np.int64) * 2 - 32768).astype(np.float32) / f32(32768.0)).astype(np.float32)


# --- RoHugeHierBitMap2d<4, 3> ----------------------------------------------------------------------------


class HierBitmap:
    """A two-level bitmap: 128x128-pixel blocks of 8x8 leaves of 16x16 bits; an offset of 1 means "all set"."""

    L1, L2 = 16, 128

    def __init__(self, dump: bytes):
        if len(dump) % 4:
            dump = dump + b"\0" * (4 - len(dump) % 4)
        self.u32 = np.frombuffer(dump, "<u4")
        self.w, self.h = struct.unpack_from("<ii", dump, 0)
        (top,) = struct.unpack_from("<I", dump, 8)
        self.top = self.u32[top // 4 : top // 4 + self.w * self.h].astype(np.int64)
        self._words = None

    def get1(self, x: int, y: int) -> bool:
        """One pixel, without numpy (the sequential generator path)."""
        if x < 0 or y < 0 or x >= self.w * 128 or y >= self.h * 128:
            return False
        if self._words is None:
            from array import array

            self._words = array("I", self.u32.tobytes())
        wd = self._words
        o2 = int(self.top[(y >> 7) * self.w + (x >> 7)])
        if o2 <= 1:
            return o2 == 1
        o1 = wd[(o2 >> 2) + ((y >> 4) & 7) * 8 + ((x >> 4) & 7)]
        if o1 <= 1:
            return o1 == 1
        idx = ((y & 15) << 4) | (x & 15)
        return bool((wd[(o1 >> 2) + (idx >> 5)] >> (idx & 31)) & 1)

    @classmethod
    def read(cls, buf: bytes, p: int) -> tuple["HierBitmap", int]:
        l1, l2, size = struct.unpack_from("<3i", buf, p)
        if (l1, l2) != (4, 3):
            raise LandGenError(f"bitmap of {l1}/{l2} levels is not read")
        return cls(bytes(buf[p + 12 : p + 12 + size])), p + 12 + size

    @property
    def width(self) -> int:
        return self.w * self.L2

    @property
    def height(self) -> int:
        return self.h * self.L2

    def get(self, x, y) -> np.ndarray:
        x = np.asarray(x, np.int64)
        y = np.asarray(y, np.int64)
        out = np.zeros(np.broadcast(x, y).shape, bool)
        x, y = np.broadcast_to(x, out.shape), np.broadcast_to(y, out.shape)
        inside = (x >= 0) & (y >= 0) & (x < self.width) & (y < self.height)
        if not inside.any():
            return out
        xi, yi = x[inside], y[inside]
        o2 = self.top[(yi >> 7) * self.w + (xi >> 7)]
        res = o2 == 1
        part = o2 > 1
        if part.any():
            xp, yp, op = xi[part], yi[part], o2[part]
            o1 = self.u32[(op >> 2) + ((yp >> 4) & 7) * 8 + ((xp >> 4) & 7)].astype(np.int64)
            r1 = o1 == 1
            leaf = o1 > 1
            if leaf.any():
                idx = ((yp[leaf] & 15) << 4) | (xp[leaf] & 15)
                word = self.u32[(o1[leaf] >> 2) + (idx >> 5)].astype(np.int64)
                r1[leaf] = ((word >> (idx & 31)) & 1).astype(bool)
            res[part] = r1
        out[inside] = res
        return out

    def get_clamped(self, x, y) -> np.ndarray:
        return self.get(np.clip(x, 0, self.width - 1), np.clip(y, 0, self.height - 1))

    def leaves(self, x0: int, y0: int, x1: int, y1: int):
        """enumerateL1Blocks over an inclusive pixel box: (bits or None when full, u0, v0) per non-empty leaf."""
        bx0, bx1 = max(x0 >> 7, 0), min(x1 >> 7, self.w - 1)
        by0, by1 = max(y0 >> 7, 0), min(y1 >> 7, self.h - 1)
        for by in range(by0, by1 + 1):
            for bx in range(bx0, bx1 + 1):
                b2o = int(self.top[by * self.w + bx])
                if not b2o:
                    continue
                sx, sy = bx << 7, by << 7
                lx0, lx1 = max((x0 - sx) >> 4, 0), min((x1 - sx) >> 4, 7)
                ly0, ly1 = max((y0 - sy) >> 4, 0), min((y1 - sy) >> 4, 7)
                for ly in range(ly0, ly1 + 1):
                    for lx in range(lx0, lx1 + 1):
                        b1o = int(self.u32[(b2o >> 2) + ly * 8 + lx]) if b2o != 1 else 1
                        if not b1o:
                            continue
                        bits = None if b1o == 1 else self.u32[b1o >> 2 : (b1o >> 2) + 8]
                        yield bits, sx + lx * 16, sy + ly * 16


# --- the read-only BLK (dag_roDataBlock.h) -------------------------------------------------------------

T_STRING, T_INT, T_REAL, T_POINT2, T_POINT3, T_POINT4, T_IPOINT2, T_IPOINT3, T_BOOL, T_E3DCOLOR, T_MATRIX, T_INT64, T_IPOINT4 = range(1, 14)
_VEC = {T_POINT2: "<2f", T_POINT3: "<3f", T_POINT4: "<4f", T_IPOINT2: "<2i", T_IPOINT3: "<3i", T_IPOINT4: "<4i",
        T_MATRIX: "<12f", T_INT64: "<q"}


@dataclass
class RoBlk:
    name: str
    params: list  # (name, type, value)
    blocks: list

    def get(self, name: str, kind: int, default=None):
        for n, t, v in self.params:
            if n == name:
                return v if t == kind else default
        return default

    def block(self, name: str) -> "RoBlk | None":
        return next((b for b in self.blocks if b.name == name), None)

    def all(self, name: str) -> list:
        return [b for b in self.blocks if b.name == name]


def read_roblk(buf: bytes) -> RoBlk:
    """A RoDataBlock dump (the bytes after its size): 48-byte block records, 8-byte params, one name map."""

    def tab(o):
        return struct.unpack_from("<II", buf, o)

    (nm_at,) = struct.unpack_from("<I", buf, 32)
    map_at, n = tab(nm_at)
    names = []
    for i in range(n):
        (o,) = struct.unpack_from("<I", buf, map_at + 8 * i)
        names.append(buf[o : buf.index(b"\0", o)].decode("latin1"))

    def blk(o: int) -> RoBlk:
        po, pc = tab(o)
        bo, bc = tab(o + 16)
        (nm,) = struct.unpack_from("<I", buf, o + 32)
        (nid,) = struct.unpack_from("<i", buf, o + 40)
        params = []
        for i in range(pc):
            v, pn, pt = struct.unpack_from("<iHH", buf, po + 8 * i)
            if pt == T_INT:
                val = v
            elif pt == T_REAL:
                (val,) = struct.unpack("<f", struct.pack("<i", v))
            elif pt == T_BOOL:
                val = bool(v & 0xFF)
            elif pt == T_E3DCOLOR:
                val = v & _M32
            elif pt == T_STRING:
                a = nm + v
                val = buf[a : buf.index(b"\0", a)].decode("latin1")
            elif pt in _VEC:
                val = struct.unpack_from(_VEC[pt], buf, nm + v)
                if pt == T_INT64:
                    val = val[0]
            else:
                val = v
            params.append((names[pn], pt, val))
        return RoBlk(names[nid] if 0 <= nid < len(names) else "", params, [blk(bo + 48 * i) for i in range(bc)])

    return blk(0)


# --- the land class resource (rendInstGenLand.cpp) -----------------------------------------------------


@dataclass
class MpRec:
    kind: int = MP_NONE
    p1: tuple = (0.0, 0.0, 0.5)
    p2: tuple = (0.5, 0.0, 0.0)
    p3: tuple = (-0.4, 0.0, -0.4)
    bc21: float = 0.0
    bc31: float = 0.0


def _multipoint(b: RoBlk) -> MpRec:
    kind = {"yz": MP_YZ, "xy": MP_XY, "3point": MP_3POINT}.get((b.get("placement", T_STRING, "none") or "none").lower(), MP_NONE)
    r = MpRec(kind)
    if kind == MP_NONE:
        return r
    r.p1 = b.get("mpPoint1", T_POINT3, r.p1)
    r.p2 = b.get("mpPoint2", T_POINT3, r.p2)
    r.p3 = b.get("mpPoint3", T_POINT3, r.p3)
    u = np.subtract(r.p2, r.p1)
    v = np.subtract(r.p3, r.p1)
    w = -np.asarray(r.p1, float)
    cy = lambda a, b: a[2] * b[0] - a[0] * b[2]  # (x0z(a) % x0z(b)).y
    uv, vw, uw = cy(u, v), cy(v, w), cy(u, w)
    r.bc21 = vw / -uv if uv else 0.0
    r.bc31 = uw / uv if uv else 0.0
    return r


def _orient(s: str | None) -> int:
    s = (s or "world").lower()
    return {"world": ORIENT_WORLD, "normal": ORIENT_NORMAL, "normal_xz": ORIENT_NORMAL_XZ, "world_xz": ORIENT_WORLD_XZ}.get(s, ORIENT_WORLD)


@dataclass
class TiledPlaces:
    entity: int
    orient: int
    y_offset: tuple
    rseed: int
    mp: MpRec
    tms: list = field(default_factory=list)  # (3x3 math matrix, x, z) per spot, tile-local


@dataclass
class Tiled:
    places: list
    tile: tuple
    above: float


@dataclass
class PlantObj:
    entity: int
    orient: int
    weight: float
    rot: tuple  # (rotX, rotY, rotZ) as (base, spread) radians
    scale: tuple
    y_scale: tuple
    y_offset: tuple
    mp: MpRec


@dataclass
class Planted:
    density: float
    rseed: int
    sum_weight: float
    above: float
    objs: list
    dmap: HierBitmap | None
    cell: tuple
    size: tuple
    ofs: tuple


@dataclass
class LandClass:
    name: str
    objects: list  # render-instance names, by riResId
    tiled: Tiled | None
    planted: list
    layer: int = 0


def _tm(m: tuple) -> tuple[np.ndarray, float, float, float]:
    """A BLK TMatrix (four columns of three) as a math 3x3 and its translation."""
    a = np.asarray(m, np.float32).reshape(4, 3)
    return a[:3].T.copy(), float(a[3, 0]), float(a[3, 1]), float(a[3, 2])


def parse_land_class(raw: bytes, name: str = "", objects: list | None = None) -> LandClass:
    """A land class from its unpacked stream: the BLK (size, dump), then the planted groups' density maps."""
    (size,) = struct.unpack_from("<i", raw, 0)
    blk = read_roblk(raw[4 : 4 + size])
    p = 4 + size
    dmaps: dict[str, HierBitmap] = {}
    if blk.block("obj_plant_generate") is not None:
        (n,) = struct.unpack_from("<i", raw, p)
        p += 4
        for _ in range(n):
            (ln,) = struct.unpack_from("<i", raw, p)
            nm = raw[p + 4 : p + 4 + ln].decode("latin1")
            p += 4 + ln + ((4 - ln % 4) % 4)
            dmaps[nm], p = HierBitmap.read(raw, p)
    layer = blk.get("layerIdx", T_INT, 1 if blk.get("secondaryLayer", T_BOOL, False) else 0)
    tiled = None
    lim0 = blk.get("landBBoxLim0", T_POINT2, (0.0, 0.0))
    lim1 = blk.get("landBBoxLim1", T_POINT2, (0.0, 0.0))
    if blk.block("resources") is not None and lim1[0] > lim0[0] and lim1[1] > lim0[1]:
        tx, tz = f32(lim1[0] - lim0[0]), f32(lim1[1] - lim0[1])
        places: list[TiledPlaces] = []
        for res in blk.all("resources"):
            ofs = res.get("offset", T_POINT2, (0.0, 0.0))
            o_default = res.get("orientation", T_STRING, None)
            if o_default and o_default.lower() not in ("world", "normal"):
                o_default = None
            for ob in res.all("object"):
                m3, x, _y, z = _tm(ob.get("matrix", T_MATRIX, (1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0)))
                if not (lim0[0] <= x <= lim1[0] and lim0[1] <= z <= lim1[1]):
                    continue
                ent = ob.get("riResId", T_INT, -1)
                orient = _orient(ob.get("orientation", T_STRING, o_default))
                tp = next((t for t in reversed(places) if t.entity == ent and t.orient == orient), None)
                if tp is None:
                    tp = TiledPlaces(ent, orient,
                                     res.get("yOffset", T_POINT2, res.get("offset_y", T_POINT2, (0.0, 0.0))),
                                     res.get("rseed", T_INT, 123), _multipoint(res))
                    places.append(tp)
                px, pz = f32(x + ofs[0]), f32(z + ofs[1])
                px = f32(px - np.floor((px - f32(lim0[0])) / tx) * tx)
                pz = f32(pz - np.floor((pz - f32(lim0[1])) / tz) * tz)
                tp.tms.append((m3, px, pz))
        if lim0[0] or lim0[1]:
            for tp in places:
                for i, (m3, px, pz) in enumerate(tp.tms):
                    px, pz = f32(px - f32(lim0[0])), f32(pz - f32(lim0[1]))
                    tp.tms[i] = (m3, f32(px - np.floor(px / tx) * tx), f32(pz - np.floor(pz / tz) * tz))
        tiled = Tiled(places, (float(tx), float(tz)), blk.get("placeAboveHt", T_REAL, 1.0))
    planted = []
    deg = np.pi / 180.0
    for g in blk.all("obj_plant_generate"):
        density = g.get("density", T_REAL, 1.0)
        common_y = g.get("yOffset", T_POINT2, g.get("offset_y", T_POINT2, (0.0, 0.0)))
        dname = g.get("densityMap", T_STRING, None)
        size = g.get("mapSize", T_POINT2, (32.0, 32.0))
        dm = dmaps.get(dname) if dname else None
        cell = (0.0, 0.0)
        if dm is not None:
            cell = (float(f32(size[0]) / f32(dm.width)), float(f32(size[1]) / f32(dm.height)))
            per_block = density * cell[0] * cell[1] / 100.0 * 256
            if density > 0 and per_block < 1.0 / 64.0 and cell[0] * cell[1] < 1:
                density = 0.0
        objs, total = [], 0.0
        for ob in g.all("object"):
            w = ob.get("weight", T_REAL, 1.0)
            if w < 0:
                break
            total = float(f32(total) + f32(w))
            rx = ob.get("rot_x", T_POINT2, (0.0, 0.0))
            ry = ob.get("rot_y", T_POINT2, (0.0, 0.0))
            rz = ob.get("rot_z", T_POINT2, (0.0, 0.0))
            objs.append(PlantObj(
                ob.get("riResId", T_INT, -1), _orient(ob.get("orientation", T_STRING, "world")), w,
                tuple(tuple(float(f32(a * deg)) for a in r) for r in (rx, ry, rz)),
                ob.get("scale", T_POINT2, (1.0, 0.0)), ob.get("yScale", T_POINT2, (1.0, 0.0)),
                ob.get("yOffset", T_POINT2, ob.get("offset_y", T_POINT2, common_y)), _multipoint(ob)))
        if objs:
            planted.append(Planted(density, g.get("rseed", T_INT, 12345), total, g.get("placeAboveHt", T_REAL, 1.0),
                                   objs, dm, cell, size, g.get("mapOfs", T_POINT2, (0.0, 0.0))))
    return LandClass(name, list(objects or []), tiled, planted, layer)


def _unblock(buf: bytes) -> bytes:
    """A Dagor block body: zstd (flag 1) or the 7-zip LZMA stream (flag 0, the generator's default)."""
    (word,) = struct.unpack_from("<I", buf, 0)
    fmt, n = word >> 30, word & 0x3FFFFFFF
    body = buf[4 : 4 + n]
    if fmt == 1:
        import zstandard

        return zstandard.ZstdDecompressor().decompressobj().decompress(body)
    if fmt == 2:
        from . import oodle

        (src,) = struct.unpack_from("<i", body, 0)
        return oodle.decompress(body[4:], src)
    import lzma

    props = body[0]
    pb, rest = divmod(props, 45)
    lp, lc = divmod(rest, 9)
    (dict_size,) = struct.unpack_from("<I", body, 1)
    dec = lzma.LZMADecompressor(lzma.FORMAT_RAW, filters=[{"id": lzma.FILTER_LZMA1, "lc": lc, "lp": lp, "pb": pb,
                                                            "dict_size": dict_size}])
    return dec.decompress(body[5:])


_REFS: dict[Path, dict[str, list[str]]] = {}


def grp_refs(path: Path) -> dict[str, list[str]]:
    """Each land class of a pack with the names it references (render instance, collision, in pairs)."""
    if path in _REFS:
        return _REFS[path]
    with path.open("rb") as fh:
        head = fh.read(16)
        label, _desc, full, _rest = struct.unpack("<4sIII", head)
        d = head + fh.read(full)
    out: dict[str, list[str]] = {}
    if label in (b"GRP2", b"GRP3"):
        names_at, n_names = struct.unpack_from("<II", d, 16)
        data_at, n_data = struct.unpack_from("<II", d, 48)
        names = []
        for i in range(n_names):
            (o,) = struct.unpack_from("<i", d, names_at + 4 * i)
            names.append(d[o : d.index(b"\0", o)].decode("latin1") if o >= 0 else "")
        for i in range(n_data):
            if label == b"GRP2":
                cid, rid, _r, ofs, cnt = struct.unpack_from("<IHHII", d, data_at + 24 * i)
            else:
                cid, rid, cnt, ofs = struct.unpack_from("<IHHI", d, data_at + 16 * i)
            if cid != LANDCLASS_CLASS or rid >= len(names):
                continue
            refs = struct.unpack_from(f"<{cnt}H", d, ofs) if cnt else ()
            out[names[rid]] = [names[r] if r < len(names) else "" for r in refs]
    _REFS[path] = out
    return out


def load_land_class(where: dict, name: str) -> LandClass | None:
    """A land class by name from a resource index's `where` map ((name, class) -> (pack, offset))."""
    loc = where.get((name, LANDCLASS_CLASS))
    if loc is None:
        return None
    path, ofs = loc
    with path.open("rb") as fh:
        fh.seek(ofs)
        head = fh.read(4)
        (word,) = struct.unpack("<I", head)
        blob = head + fh.read(word & 0x3FFFFFFF)
    refs = grp_refs(path).get(name, [])
    return parse_land_class(_unblock(blob), name, refs[0::2])


def has_impostor(where: dict, name: str) -> bool:
    """A render instance with an impostor (a tree, for the generator: kept as a position and a scale)."""
    loc = where.get((name, RENDINST_CLASS))
    if loc is None:
        return False
    with loc[0].open("rb") as fh:
        fh.seek(loc[1])
        (w,) = struct.unpack("<I", fh.read(4))
    return bool((w >> 24) & 1)


# --- the level's generator layout (RIGz) ----------------------------------------------------------------


@dataclass
class RiGenLand:
    world0: tuple[float, float]
    grid2world: float
    cell_size: int
    cells_w: int
    cells_h: int
    pivot: tuple[float, float]
    sweep_scale: float
    sweep: HierBitmap | None
    names: list
    masks: list
    cells: list  # per cell: land class indices covering it


def read_rigen_land(data: bytes, start: int, primary: bool = True) -> RiGenLand:
    """The land-class half of a RIGz block: grid, land classes, their masks, the exclusion mask."""
    (word,) = struct.unpack_from("<I", data, start)
    raw = _unblock(data[start : start + 4 + (word & 0x3FFFFFFF)])
    (dsz,) = struct.unpack_from("<i", raw, 0)
    dump = raw[4 : 4 + dsz]
    cells_at, n_cells = struct.unpack_from("<II", dump, 8)
    cw, ch = struct.unpack_from("<ii", dump, 24)
    (csz,) = struct.unpack_from("<h", dump, 32)
    (sweep_scale,) = struct.unpack_from("<f", dump, 36)
    lc_at, n_lc = struct.unpack_from("<II", dump, 48)
    wx, wz = struct.unpack_from("<2f", dump, 64)
    g2w, pvx, pvz = struct.unpack_from("<3f", dump, 112)
    names = []
    for i in range(n_lc):
        (o,) = struct.unpack_from("<I", dump, lc_at + 32 * i)
        names.append(dump[o : dump.index(b"\0", o)].decode("latin1"))
    p = 4 + dsz
    sweep = None
    if primary:
        sweep, p = HierBitmap.read(raw, p)
    masks = []
    for _ in range(n_lc):
        m, p = HierBitmap.read(raw, p)
        masks.append(m)
    cells = []
    for ci in range(n_cells):
        o, n = struct.unpack_from("<II", dump, cells_at + _CELL * ci)
        cells.append([struct.unpack_from("<i", dump, o + 8 * k)[0] for k in range(n)])
    return RiGenLand((wx, wz), g2w, csz, cw, ch, (pvx, pvz), sweep_scale, sweep, names, masks, cells)


# --- generation --------------------------------------------------------------------------------------------


@dataclass
class _Cands:
    """Spots the planted generator tries, before the masks: one row per ADD_ENTITY_BYMASK."""

    seed: list = field(default_factory=list)
    ou: list = field(default_factory=list)
    ov: list = field(default_factory=list)
    bx: list = field(default_factory=list)  # mx + entity_ofs_x (float32)
    bz: list = field(default_factory=list)
    rect: list = field(default_factory=list)  # index into rects, or -1 for no rect test


def _plant_leaf(c: _Cands, bits, u0: int, v0: int, x0, y0, gx, gy, density, rseed: int, ofs_x, ofs_z, rect: int, seq=None):
    """GenObjCB::onNonEmptyL1Block: the spots of one 16x16 leaf of a density map."""
    if bits is None:
        cu = [1] * 256
        numc = 256
    else:
        cu = []
        for w in bits:
            w = int(w)
            cu.extend((w >> i) & 1 for i in range(32))
        numc = sum(cu)
    if not numc:
        return
    s1, s2 = _nxt((u0 + 97) & _M32), _nxt((v0 + 79) & _M32)
    seed = (((rseed & _M32) ^ s1 ^ s2) + s1 + s2) & _M32
    num = float(np.floor(f32(f32(numc) * density) * f32(1024.0) + f32(0.5)) / f32(1024.0))
    mx, my = f32(f32(gx * f32(u0)) + x0), f32(f32(gy * f32(v0)) + y0)
    bx, bz = float(f32(mx + ofs_x)), float(f32(my + ofs_z))
    a9, c9 = _JUMP9
    numu = 0
    while num >= 1:
        while True:
            a = _nxt(seed)
            b = _nxt(a)
            seed = b
            ou, ov = (a >> 16) & 15, (b >> 16) & 15
            if cu[ov * 16 + ou] == 1:
                break
        cu[ov * 16 + ou] = 2
        numu += 1
        if numu >= numc:
            numu = 0
            cu = [1 if v == 2 else v for v in cu]
        c.seed.append(seed)
        c.ou.append(ou)
        c.ov.append(ov)
        c.bx.append(bx)
        c.bz.append(bz)
        c.rect.append(rect)
        seed = (seed * a9 + c9) & _M32 if seq is None else seq(seed, ou, ov, bx, bz, rect)
        num -= 1
    if num > 0:
        while True:
            a = _nxt(seed)
            b = _nxt(a)
            seed = b
            ou, ov = (a >> 16) & 15, (b >> 16) & 15
            if cu[ov * 16 + ou] == 1:
                break
        seed = _nxt(seed)
        # The engine reads the leaf at (ov, ou) here, x and y swapped against the spot it picked.
        full = bits is None or (int(bits[(ou * 16 + ov) >> 5]) >> ((ou * 16 + ov) & 31)) & 1
        if ((seed >> 16) & 0x7FFF) < (int(np.floor(f32(num) * f32(32768))) + 1 if full else 0):
            c.seed.append(seed)
            c.ou.append(ou)
            c.ov.append(ov)
            c.bx.append(bx)
            c.bz.append(bz)
            c.rect.append(rect)


def _plant_grid(c: _Cands, x0, z0, box, density, rseed: int, ofs_x, ofs_z, rect: int, seq=None):
    """The planted path without a density map: a 16x16 grid over the sub-cell, each slot once in turn."""
    seed1 = _nxt((int(f32(x0) / f32(box)) + 97) & _M32)
    seed2 = _nxt((int(f32(z0) / f32(box)) + 79) & _M32)
    seed = (((rseed & _M32) ^ seed1 ^ seed2) + seed1 + seed2) & _M32
    dens = f32(f32(density) * f32(0.01))
    num = float(np.floor(f32(f32(box) * f32(box) * dens) * f32(128.0) + f32(0.5)) / f32(128.0))
    bx, bz = float(f32(f32(x0) + ofs_x)), float(f32(f32(z0) + ofs_z))
    used = [0] * 16
    a9, c9 = _JUMP9
    numu = 0

    def pick():
        nonlocal seed
        while True:
            a = _nxt(seed)
            b = _nxt(a)
            seed = b
            ou, ov = (a >> 16) & 15, (b >> 16) & 15
            if not used[ov] & (1 << ou):
                return ou, ov

    while num >= 1:
        ou, ov = pick()
        used[ov] |= 1 << ou
        numu += 1
        if numu >= 256:
            numu = 0
            used = [0] * 16
        c.seed.append(seed)
        c.ou.append(ou)
        c.ov.append(ov)
        c.bx.append(bx)
        c.bz.append(bz)
        c.rect.append(rect)
        seed = (seed * a9 + c9) & _M32 if seq is None else seq(seed, ou, ov, bx, bz, rect)
        num -= 1
    if num > 0:
        ou, ov = pick()
        seed = _nxt(seed)
        if ((seed >> 16) & 0x7FFF) < int(np.floor(f32(num) * f32(32768))) + 1:
            c.seed.append(seed)
            c.ou.append(ou)
            c.ov.append(ov)
            c.bx.append(bx)
            c.bz.append(bz)
            c.rect.append(rect)


def _align(p: np.ndarray) -> np.ndarray:
    """align_place_xz: snap to whole metres within 1/256."""
    eps = f32(0.00390625)
    f = np.floor(p).astype(np.float32)
    d = (p - f).astype(np.float32)
    return np.where(d < eps, f, np.where(d > f32(1.0) - eps, (f + f32(1.0)).astype(np.float32), p)).astype(np.float32)


def _rot(axis: str, a: np.ndarray) -> np.ndarray:
    """rotx_tm / roty_tm / rotz_tm as math matrices (n, 3, 3)."""
    c, s = np.cos(a), np.sin(a)
    o, z = np.ones_like(a), np.zeros_like(a)
    if axis == "x":
        rows = [[o, z, z], [z, c, s], [z, -s, c]]
    elif axis == "y":
        rows = [[c, z, -s], [z, o, z], [s, z, c]]
    else:
        rows = [[c, s, z], [-s, c, z], [z, z, o]]
    return np.stack([np.stack(r, -1) for r in rows], -2)


def _normalize(v: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(v, axis=-1, keepdims=True)
    return v / np.where(n > 0, n, 1)


def _basis(norm: np.ndarray, orient: np.ndarray, up_tm: np.ndarray | None = None) -> np.ndarray:
    """The orientation basis of genObjByDensGridMask / genObjByMask for ORIENT_NORMAL*, as math matrices."""
    n = norm.copy()
    x = np.cross(n, np.array([0.0, 0.0, 1.0]))
    nxz = np.stack([-n[:, 2], np.zeros(len(n)), n[:, 0]], 1)
    sel = orient == ORIENT_NORMAL_XZ
    x[sel] = np.cross(n[sel], nxz[sel])
    sel = orient == ORIENT_WORLD_XZ
    if sel.any():
        up = np.tile([0.0, 1.0, 0.0], (int(sel.sum()), 1)) if up_tm is None else up_tm[sel]
        flat = np.abs(n[sel, 0]) + np.abs(n[sel, 2]) > 1e-5
        xs = np.where(flat[:, None], np.cross(up, nxz[sel]), np.cross(up, [0.0, 0.0, 1.0]) if up_tm is not None else [[1.0, 0.0, 0.0]])
        x[sel] = xs
        n[sel] = up
    ln = np.linalg.norm(x, axis=1)
    tiny = ln <= 1.192092896e-06
    x[tiny] = _normalize(np.cross(n[tiny], [1.0, 0.0, 0.0]))
    x[~tiny] /= ln[~tiny, None]
    z = _normalize(np.cross(x, n))
    return np.stack([x, n, z], -1)  # columns


class _Ground:
    """Heights and normals from the caller's height function (x, z arrays -> y array)."""

    def __init__(self, height):
        self.height = height

    def y(self, x, z) -> np.ndarray:
        if self.height is None:
            return np.zeros(len(x))
        return np.asarray(self.height(np.asarray(x, float), np.asarray(z, float)), float)

    def normal(self, x, z, d: float = 1.0) -> np.ndarray:
        x, z = np.asarray(x, float), np.asarray(z, float)
        if self.height is None:
            return np.tile([0.0, 1.0, 0.0], (len(x), 1))
        hx = self.y(x + d, z) - self.y(x - d, z)
        hz = self.y(x, z + d) - self.y(x, z - d)
        return _normalize(np.stack([-hx / (2 * d), np.ones_like(x), -hz / (2 * d)], 1))


def _multipoint_place(mp: MpRec, pos: np.ndarray, rot: np.ndarray, ground: _Ground):
    """place_multipoint + rotate_multipoint for one kind of multi-point record, vectorised over instances."""
    p1 = np.einsum("nij,j->ni", rot, mp.p1) + pos
    p2 = np.einsum("nij,j->ni", rot, mp.p2) + pos
    p1[:, 1] = ground.y(p1[:, 0], p1[:, 2])
    p2[:, 1] = ground.y(p2[:, 0], p2[:, 2])
    out = pos.copy()
    if mp.kind == MP_3POINT:
        p3 = np.einsum("nij,j->ni", rot, mp.p3) + pos
        p3[:, 1] = ground.y(p3[:, 0], p3[:, 2])
        out = p1 + (p2 - p1) * mp.bc21 + (p3 - p1) * mp.bc31
    else:
        out[:, 1] = ground.y(out[:, 0], out[:, 2])
    return out, p1, p2, (p3 if mp.kind == MP_3POINT else None)


def _rotate_multipoint(tm: np.ndarray, mp: MpRec, p1, p2, p3) -> np.ndarray:
    v = tm[:, :, 1]
    pv = _normalize(p1 - p2)
    if mp.kind == MP_YZ:
        c0 = _normalize(np.cross(v, pv))
        c1 = _normalize(np.cross(pv, c0))
        c2 = _normalize(np.cross(c0, c1))
        return np.stack([c0, c1, c2], -1)
    if mp.kind == MP_XY:
        c2 = _normalize(np.cross(pv, v))
        c1 = _normalize(np.cross(c2, pv))
        c0 = _normalize(np.cross(c1, c2))
        return np.stack([c0, c1, c2], -1)
    if mp.kind == MP_3POINT:
        pv2 = _normalize(p3 - p2)
        nrm = _normalize(np.cross(pv2, pv))
        nrm[nrm[:, 1] < 0] *= -1
        out = np.empty_like(tm)
        for i in range(len(tm)):  # quat_rotation_arc(v, n) * tm
            a, b = _normalize(v[i]), nrm[i]
            axis = np.cross(a, b)
            s, c = np.linalg.norm(axis), float(np.dot(a, b))
            if s < 1e-9:
                r = np.eye(3)
            else:
                k = axis / s
                kx = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
                r = np.eye(3) + s * kx + (1 - c) * kx @ kx
            out[i] = r @ tm[i]
        return out
    return tm


_GRASS = re.compile(r"grass|flower|reed|fern|weed|clover|nettle|typha")
_BUSH = re.compile(r"bush|shrub|hedge(?!hog)")
_TREE = re.compile(r"tree|pine|spruce|birch|oak|aspen|palm|poplar|cypress|willow|maple|beech|fir(?![e])|tilia|acacia")


def classify(name: str, pos_inst: bool, tiled: bool) -> str:
    n = name.lower()
    if _GRASS.search(n):
        return "grass"
    if _BUSH.search(n):
        return "bushes"
    if pos_inst or _TREE.search(n):
        return "trees"
    return "buildings" if tiled else "props"


def _keep(x: np.ndarray, z: np.ndarray, factor: float) -> np.ndarray:
    """A deterministic thinning: keeps about `factor` of the instances, the same ones every run."""
    if factor >= 1:
        return np.ones(len(x), bool)
    if factor <= 0:
        return np.zeros(len(x), bool)
    xi = np.floor(np.asarray(x) * 16).astype(np.int64) & 0xFFFFFFFF
    zi = np.floor(np.asarray(z) * 16).astype(np.int64) & 0xFFFFFFFF
    h = ((xi * 73856093) ^ (zi * 19349663)) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 0x5BD1E995) & 0xFFFFFFFF
    h ^= h >> 15
    return (h & 0xFFFFFF) < int(factor * 0x1000000)


@dataclass
class _Out:
    mats: dict = field(default_factory=dict)  # name -> list of (n, 3, 4)
    per_class: dict = field(default_factory=dict)
    rect: tuple | None = None

    def add(self, lc: str, name: str, m: np.ndarray):
        if self.rect is not None and len(m):
            r = self.rect
            m = m[(m[:, 0, 3] >= r[0]) & (m[:, 0, 3] <= r[2]) & (m[:, 2, 3] >= r[1]) & (m[:, 2, 3] <= r[3])]
        if not len(m):
            return
        self.mats.setdefault(name, []).append(m.astype(np.float32))
        d = self.per_class.setdefault(lc, {})
        d[name] = d.get(name, 0) + len(m)


class Generator:
    """Generates the instances of one RIGz layer, sub-cell by sub-cell, the way the engine walks them."""

    def __init__(self, rg: RiGenLand, classes: dict, where: dict, ground: _Ground, kinds, density):
        self.rg, self.classes, self.where, self.ground = rg, classes, where, ground
        self.kinds = set(kinds) if kinds else set(KINDS)
        self.density = density or {}
        self.box = f32(f32(rg.grid2world) * f32(rg.cell_size) / f32(SUBCELL_DIV))
        self.w2g = f32(1.0 / rg.grid2world)
        self._imp: dict[str, bool] = {}
        self.kind_of: dict[str, str] = {}
        self.pos_inst: dict[str, bool] = {}
        self.tried = 0

    def impostor(self, name: str) -> bool:
        if name not in self._imp:
            self._imp[name] = has_impostor(self.where, name)
        return self._imp[name]

    def allowed(self, mask: HierBitmap, x: np.ndarray, z: np.ndarray) -> np.ndarray:
        """The land class's mask (clamped, as getClamped) and the level's exclusion mask."""
        rg = self.rg
        mx = (np.floor((x * self.w2g).astype(np.float32)) - np.floor(f32(self.w2g * f32(rg.world0[0])))).astype(np.int64)
        mz = (np.floor((z * self.w2g).astype(np.float32)) - np.floor(f32(self.w2g * f32(rg.world0[1])))).astype(np.int64)
        ok = mask.get_clamped(mx, mz)
        if rg.sweep is not None and ok.any():
            ix = np.floor((x.astype(np.float64) - rg.world0[0]) * rg.sweep_scale).astype(np.int64)
            iz = np.floor((z.astype(np.float64) - rg.world0[1]) * rg.sweep_scale).astype(np.int64)
            ok &= ~rg.sweep.get(ix, iz)
        return ok

    def subcells(self, rect):
        rg = self.rg
        box = float(self.box)
        for ci, cls in enumerate(rg.cells):
            if not cls:
                continue
            x, z = ci % rg.cells_w, ci // rg.cells_w
            for s in range(SUBCELL_DIV * SUBCELL_DIV):
                x0 = f32(f32(x * SUBCELL_DIV + s % SUBCELL_DIV) * self.box)
                z0 = f32(f32(z * SUBCELL_DIV + s // SUBCELL_DIV) * self.box)
                if rect is not None:
                    ax, az = rg.world0[0] + float(x0), rg.world0[1] + float(z0)
                    if ax > rect[2] or az > rect[3] or ax + box < rect[0] or az + box < rect[1]:
                        continue
                yield cls, x0, z0

    # -- planted ------------------------------------------------------------------------------------

    def planted(self, lc: LandClass, mask: HierBitmap, subs: list, out: _Out):
        rg = self.rg
        ex, ez = f32(rg.world0[0]), f32(rg.world0[1])
        for g in lc.planted:
            if g.density <= 0:
                continue
            c = _Cands()
            rects: list = []
            seq = self._sequential(g, mask, rects) if any(o.entity < 0 for o in g.objs) else None
            for x0, z0 in subs:
                r = (float(f32(x0 + ex)), float(f32(z0 + ez)), float(f32(f32(x0 + ex) + self.box)), float(f32(f32(z0 + ez) + self.box)))
                rects.append(r)
                ri = len(rects) - 1
                if g.dmap is None:
                    _plant_grid(c, x0, z0, self.box, g.density, g.rseed, ex, ez, ri, seq)
                    continue
                gx, gy = f32(g.cell[0]), f32(g.cell[1])
                dens = f32(f32(g.density) * gx * gy * f32(0.01))
                if 256 * float(dens) < 1.0 / 8192.0:
                    continue
                dx, dy = f32(g.size[0]), f32(g.size[1])
                rx, ry = f32(1.0) / gx, f32(1.0) / gy
                ofx = f32(f32(g.ofs[0]) + f32(rg.pivot[0]) - ex)
                ofz = f32(f32(g.ofs[1]) + f32(rg.pivot[1]) - ez)
                r0x, r0y = f32(x0 + ex), f32(z0 + ez)
                r1x, r1y = f32(r0x + self.box), f32(r0y + self.box)
                tx0 = f32(np.floor((r0x - f32(ex + ofx)) / dx) * dx + ofx)
                ty0 = f32(np.floor((r0y - f32(ez + ofz)) / dy) * dy + ofz)
                tx1 = f32(np.ceil((r1x - f32(ex + ofx)) / dx) * dx + ofx)
                ty1 = f32(np.ceil((r1y - f32(ez + ofz)) / dy) * dy + ofz)
                clip = (0, 0, int(f32(g.size[0]) * rx), int(f32(g.size[1]) * ry))
                mx = tx0
                while mx < tx1:
                    my = ty0
                    while my < ty1:
                        b0x = int(np.floor(f32((x0 - mx) * rx)))
                        b0y = int(np.floor(f32((z0 - my) * ry)))
                        b1x = int(np.ceil(f32(f32(r1x - f32(ex + mx)) * rx - f32(1))))
                        b1y = int(np.ceil(f32(f32(r1y - f32(ez + my)) * ry - f32(1))))
                        b0x, b0y = max(b0x, clip[0]), max(b0y, clip[1])
                        b1x, b1y = min(b1x, clip[2]), min(b1y, clip[3])
                        if b0x <= b1x and b0y <= b1y:
                            skip = (b0x, b0y, b1x, b1y) == clip
                            for bits, u0, v0 in g.dmap.leaves(b0x, b0y, b1x, b1y):
                                _plant_leaf(c, bits, u0, v0, mx, my, gx, gy, dens, g.rseed, ex, ez, -1 if skip else ri, seq)
                        my = f32(my + dy)
                    mx = f32(mx + dx)
            self.tried += len(c.seed)
            if c.seed:
                self._finish_planted(lc, g, c, rects, mask, out)

    def _sequential(self, g: Planted, mask: HierBitmap, rects: list):
        """
        The exact random stream for a group with an empty object (riResId -1): a spot that passes the masks and
        picks it consumes three numbers instead of nine, so the spots have to be decided one after another.
        """
        rg = self.rg
        w2g = float(self.w2g)
        mo_x = np.floor(f32(self.w2g * f32(rg.world0[0])))
        mo_z = np.floor(f32(self.w2g * f32(rg.world0[1])))
        gx, gz = (float(f32(g.cell[0])), float(f32(g.cell[1]))) if g.dmap is not None else (float(self.box / f32(16)),) * 2
        weights = [float(f32(o.weight)) for o in g.objs]
        empty = [o.entity < 0 for o in g.objs]
        sumw = float(f32(g.sum_weight))
        mw, mh = mask.width - 1, mask.height - 1
        sw = rg.sweep
        a7, c7 = _jump(7)

        def r32(v: float) -> float:
            return struct.unpack("<f", struct.pack("<f", v))[0]

        def align(v: float) -> float:
            fl = float(np.floor(v))
            d = r32(v - fl)
            return fl if d < 0.00390625 else (fl + 1 if d > r32(1 - 0.00390625) else v)

        def step(seed: int, ou: int, ov: int, bx: float, bz: float, rect: int) -> int:
            a = _nxt(seed)
            b = _nxt(a)
            x = align(r32(r32(r32(ou + ((a >> 16) & 0x7FFF) / 32768.0) * gx) + bx))
            z = align(r32(r32(r32(ov + ((b >> 16) & 0x7FFF) / 32768.0) * gz) + bz))
            ok = True
            if rect >= 0:
                r = rects[rect]
                ok = r[0] <= x <= r[2] and r[1] <= z <= r[3]
            if ok:
                mx = int(np.floor(r32(x * w2g)) - mo_x)
                mz = int(np.floor(r32(z * w2g)) - mo_z)
                ok = mask.get1(min(max(mx, 0), mw), min(max(mz, 0), mh))
            if ok and sw is not None:
                ok = not sw.get1(int(np.floor((x - rg.world0[0]) * rg.sweep_scale)), int(np.floor((z - rg.world0[1]) * rg.sweep_scale)))
            if not ok:
                return (b * a7 + c7) & _M32
            c3 = _nxt(b)
            w = r32(float(np.floor(r32(r32(r32(((c3 >> 16) & 0x7FFF) / 32768.0) * sumw) * 8192.0) + 0.5)) / 8192.0)
            k = 0
            for k, wt in enumerate(weights):
                w = r32(w - wt)
                if w <= 0:
                    break
            else:
                k = 0
            return c3 if empty[k] else (b * a7 + c7) & _M32

        return step

    def _finish_planted(self, lc: LandClass, g: Planted, c: _Cands, rects: list, mask: HierBitmap, out: _Out):
        seed = np.array(c.seed, np.uint64)
        ou, ov = np.array(c.ou, np.float32), np.array(c.ov, np.float32)
        bx, bz = np.array(c.bx, np.float32), np.array(c.bz, np.float32)
        ri = np.array(c.rect, np.int64)
        gx, gz = (f32(g.cell[0]), f32(g.cell[1])) if g.dmap is not None else (f32(self.box / f32(16)), f32(self.box / f32(16)))
        rndx, rndy = _frnd(_val(_states(seed, 1))), _frnd(_val(_states(seed, 2)))
        x = _align((((ou + rndx).astype(np.float32) * gx).astype(np.float32) + bx).astype(np.float32))
        z = _align((((ov + rndy).astype(np.float32) * gz).astype(np.float32) + bz).astype(np.float32))
        ok = np.ones(len(x), bool)
        tested = ri >= 0
        if tested.any():
            rr = np.array(rects, np.float32)[ri[tested]]
            xt, zt = x[tested], z[tested]
            ok[tested] = (xt >= rr[:, 0]) & (xt <= rr[:, 2]) & (zt >= rr[:, 1]) & (zt <= rr[:, 3])
        ok &= self.allowed(mask, x, z)
        if not ok.any():
            return
        seed, x, z = seed[ok], x[ok], z[ok]
        w = (np.floor((_frnd(_val(_states(seed, 3))) * f32(g.sum_weight) * f32(8192.0) + f32(0.5)).astype(np.float32))
             / f32(8192.0)).astype(np.float32)
        pick = np.full(len(w), -1)
        for k, o in enumerate(g.objs):
            w = (w - f32(o.weight)).astype(np.float32)
            pick[(pick < 0) & (w <= 0)] = k
        pick[pick < 0] = 0
        rx, ry, rz = _srnd(_val(_states(seed, 4))), _srnd(_val(_states(seed, 5))), _srnd(_val(_states(seed, 6)))
        s_r, sy_r, yo_r = _srnd(_val(_states(seed, 7))), _srnd(_val(_states(seed, 8))), _srnd(_val(_states(seed, 9)))
        for k, o in enumerate(g.objs):
            sel = pick == k
            if not sel.any() or not (0 <= o.entity < len(lc.objects)):
                continue
            name = lc.objects[o.entity]
            pos_inst = self.impostor(name)
            kind = classify(name, pos_inst, False)
            self.kind_of[name], self.pos_inst[name] = kind, pos_inst
            if kind not in self.kinds:
                continue
            xs, zs = x[sel].astype(np.float64), z[sel].astype(np.float64)
            keep = _keep(xs, zs, self.density.get(kind, 1.0))
            if not keep.any():
                continue
            idx = np.nonzero(sel)[0][keep]
            xs, zs = xs[keep], zs[keep]
            ang = (np.array([o.rot[0][0], o.rot[1][0], o.rot[2][0]], np.float32)
                   + np.stack([rx[idx], ry[idx], rz[idx]], 1) * np.array([o.rot[0][1], o.rot[1][1], o.rot[2][1]], np.float32))
            s = f32(o.scale[0]) + s_r[idx] * f32(o.scale[1])
            sy = f32(o.y_scale[0]) + sy_r[idx] * f32(o.y_scale[1])
            yoff = f32(o.y_offset[0]) + f32(o.y_offset[1]) * yo_r[idx]
            m = self._place(o.orient, o.mp, xs, zs, ang, s, sy, g.above, pos_inst)
            m[:, 1, 3] += yoff
            out.add(lc.name, name, m)

    def _place(self, orient: int, mp: MpRec, x, z, ang, s, sy, above, pos_inst, base=None) -> np.ndarray:
        """Orientation (world or by the ground normal), calc_matrix_33's rotation and scale, the height."""
        n = len(x)
        pos = np.stack([x, np.zeros(n), z], 1)
        rot3 = (_rot("z", ang[:, 2]) @ _rot("x", ang[:, 0]) @ _rot("y", ang[:, 1]))
        scl = np.zeros((n, 3, 3))
        scl[:, 0, 0], scl[:, 1, 1], scl[:, 2, 2] = s, s * sy, s
        p1 = p2 = p3 = None
        if mp.kind != MP_NONE:
            pos, p1, p2, p3 = _multipoint_place(mp, pos, rot3, self.ground)
        else:
            pos[:, 1] = self.ground.y(x, z)
        if orient == ORIENT_WORLD:
            tm = np.tile(np.eye(3), (n, 1, 1))
        else:
            tm = _basis(self.ground.normal(x, z), np.full(n, orient))
        if mp.kind != MP_NONE:
            tm = _rotate_multipoint(tm, mp, p1, p2, p3)
        tm = tm @ rot3 @ scl
        if pos_inst:
            # Kept as a position and a scale: the yaw stands in for the impostor's rotation palette.
            sc = np.linalg.norm(tm[:, :, 1], axis=1)
            tm = _rot("y", ang[:, 1]) * sc[:, None, None]
        out = np.zeros((n, 3, 4), np.float32)
        out[:, :, :3] = tm
        out[:, :, 3] = pos
        return out

    # -- tiled ------------------------------------------------------------------------------------

    def tiled(self, lc: LandClass, mask: HierBitmap, subs: list, out: _Out):
        t = lc.tiled
        rg = self.rg
        ex, ez = f32(rg.world0[0]), f32(rg.world0[1])
        px, pz = f32(rg.pivot[0]), f32(rg.pivot[1])
        dx, dy = f32(t.tile[0]), f32(t.tile[1])
        if not (dx > 0 and dy > 0):
            return
        for tp in t.places:
            if not (0 <= tp.entity < len(lc.objects)) or not tp.tms:
                continue
            name = lc.objects[tp.entity]
            pos_inst = self.impostor(name)
            kind = classify(name, pos_inst, True)
            self.kind_of[name], self.pos_inst[name] = kind, pos_inst
            if kind not in self.kinds:
                continue
            lx = np.array([p[1] for p in tp.tms], np.float32)[::-1]  # tmi runs from the last spot down
            lz = np.array([p[2] for p in tp.tms], np.float32)[::-1]
            m3 = np.array([p[0] for p in tp.tms], np.float64)[::-1]
            xs, zs, seeds, which = [], [], [], []
            for x0, z0 in subs:
                r0x, r0y = f32(f32(x0 + ex) - px), f32(f32(z0 + ez) - pz)
                r1x, r1y = f32(r0x + self.box), f32(r0y + self.box)
                tx = np.arange(np.floor(r0x / dx) * dx, np.ceil(r1x / dx) * dx, dx, dtype=np.float32)
                ty = np.arange(np.floor(r0y / dy) * dy, np.ceil(r1y / dy) * dy, dy, dtype=np.float32)
                if not len(tx) or not len(ty):
                    continue
                mxg, myg = np.meshgrid(tx, ty, indexing="ij")
                ax = (mxg.reshape(-1, 1) + lx[None, :]).astype(np.float32)
                az = (myg.reshape(-1, 1) + lz[None, :]).astype(np.float32)
                inside_tile = ((mxg >= r0x) & (myg >= r0y) & (mxg + dx <= r1x) & (myg + dy <= r1y)).reshape(-1, 1)
                inr = inside_tile | ((ax >= r0x) & (ax <= r1x) & (az >= r0y) & (az <= r1y))
                inr = inr.ravel()
                if not inr.any():
                    continue
                st = _seq_states(tp.rseed & _M32, int(inr.sum()))
                wx = (mxg.reshape(-1, 1).repeat(len(lx), 1).ravel()[inr] + px).astype(np.float32)
                wz = (myg.reshape(-1, 1).repeat(len(lx), 1).ravel()[inr] + pz).astype(np.float32)
                xs.append(_align((np.tile(lx, len(tx) * len(ty))[inr] + wx).astype(np.float32)))
                zs.append(_align((np.tile(lz, len(tx) * len(ty))[inr] + wz).astype(np.float32)))
                seeds.append(st)
                which.append(np.tile(np.arange(len(lx)), len(tx) * len(ty))[inr])
            if not xs:
                continue
            x, z = np.concatenate(xs), np.concatenate(zs)
            st, wh = np.concatenate(seeds), np.concatenate(which)
            self.tried += len(x)
            ok = self.allowed(mask, x, z)
            x, z, st, wh = x[ok], z[ok], st[ok], wh[ok]
            keep = _keep(x, z, self.density.get(kind, 1.0))
            x, z, st, wh = x[keep], z[keep], st[keep], wh[keep]
            if not len(x):
                continue
            yoff = f32(tp.y_offset[0]) + f32(tp.y_offset[1]) * _srnd(_val(st))
            m = self._place_tiled(tp, m3[wh], x.astype(np.float64), z.astype(np.float64), t.above, pos_inst)
            m[:, 1, 3] += yoff
            out.add(lc.name, name, m)

    def _place_tiled(self, tp: TiledPlaces, rot: np.ndarray, x, z, above, pos_inst) -> np.ndarray:
        n = len(x)
        pos = np.stack([x, np.zeros(n), z], 1)
        p1 = p2 = p3 = None
        if tp.mp.kind != MP_NONE:
            pos, p1, p2, p3 = _multipoint_place(tp.mp, pos, rot, self.ground)
        else:
            pos[:, 1] = self.ground.y(x, z)
        tm = rot
        if tp.orient != ORIENT_WORLD:
            basis = _basis(self.ground.normal(x, z), np.full(n, tp.orient), up_tm=rot[:, :, 1])
            tm = basis @ rot
        if tp.mp.kind != MP_NONE:
            tm = _rotate_multipoint(tm, tp.mp, p1, p2, p3)
        if pos_inst:
            sc = np.linalg.norm(tm[:, :, 1], axis=1)
            tm = _rot("y", np.arctan2(tm[:, 2, 0], tm[:, 0, 0])) * sc[:, None, None]
        out = np.zeros((n, 3, 4), np.float32)
        out[:, :, :3] = tm
        out[:, :, 3] = pos
        return out


def generate(game, level_bytes: bytes, block_table: dict, *, height=None, rect=None, kinds=None, density=None,
             log=None) -> tuple[dict[str, np.ndarray], dict]:
    """
    Every instance the level's land classes generate, as the game would.

    `game`: a `level.Game` (its `resources().where` finds the land classes and render instances).
    `level_bytes`, `block_table`: the level binary and its block table (`dagorlevel.blocks`).
    `height(x, z) -> y`: the ground, vectorised over arrays of game x and z; None puts everything at 0.
    `rect`: (x0, z0, x1, z1) in game metres: only sub-cells touching it are generated, and only
    instances inside it are returned. `kinds`: which of `KINDS` to keep (all by default).
    `density`: {kind: factor} keeps that share of a kind's instances, deterministically.

    Returns ({render-instance name: (n, 3, 4) float32 [R | t] in game space}, stats).
    """
    t0 = time.time()
    where = game.resources().where
    ground = _Ground(height)
    out = _Out(rect=tuple(rect) if rect is not None else None)
    stats: dict = {"layers": [], "landClasses": {}, "missingLandClasses": [], "tried": 0}
    for li, blk in enumerate(block_table.get("RIGz", [])):
        rg = read_rigen_land(level_bytes, blk.start, primary=li == 0)
        classes = {}
        for i, nm in enumerate(rg.names):
            try:
                lc = load_land_class(where, nm)
            except (OSError, struct.error, ValueError, LandGenError) as e:
                lc = None
                if log:
                    log(f"  land class {nm}: not read ({type(e).__name__}: {e})")
            if lc is None:
                stats["missingLandClasses"].append(nm)
                continue
            classes[i] = lc
        gen = Generator(rg, classes, where, ground, kinds, density)
        by_class: dict[int, list] = {}
        for cls, x0, z0 in gen.subcells(rect):
            for i in cls:
                by_class.setdefault(i, []).append((x0, z0))
        for i, subs in sorted(by_class.items()):
            lc = classes.get(i)
            if lc is None:
                continue
            t1 = time.time()
            n0 = sum(sum(len(a) for a in v) for v in out.mats.values())
            if lc.tiled is not None:
                gen.tiled(lc, rg.masks[i], subs, out)
            if lc.planted:
                gen.planted(lc, rg.masks[i], subs, out)
            n1 = sum(sum(len(a) for a in v) for v in out.mats.values())
            if log:
                log(f"  land class {lc.name}: {n1 - n0} instances over {len(subs)} sub-cells ({time.time() - t1:.1f} s)")
        stats["layers"].append({"landClasses": rg.names, "cells": [rg.cells_w, rg.cells_h], "cellMetres": rg.grid2world * rg.cell_size,
                                "world0": list(rg.world0), "tried": gen.tried})
        stats["tried"] += gen.tried
        for name, kind in gen.kind_of.items():
            stats.setdefault("objects", {}).setdefault(name, {"kind": kind, "posInst": gen.pos_inst[name]})
    mats = {k: np.concatenate(v) for k, v in out.mats.items()}
    for k, m in mats.items():
        stats.setdefault("objects", {}).setdefault(k, {})["count"] = int(len(m))
    stats["landClasses"] = out.per_class
    kinds_count: dict[str, int] = {}
    for k, m in mats.items():
        kd = stats["objects"][k].get("kind", "props")
        kinds_count[kd] = kinds_count.get(kd, 0) + int(len(m))
    stats["kinds"] = kinds_count
    stats["instances"] = int(sum(len(m) for m in mats.values()))
    stats["seconds"] = round(time.time() - t0, 2)
    return mats, stats
