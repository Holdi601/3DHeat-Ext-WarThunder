"""
The rendered look of War Thunder's placed objects: the render-instance
resources (`RendInst`, class 0x77F8232F) in the resource packs
(`content/*/res/*.grp`), each a set of LOD meshes, and their materials from
`riDesc.bin` beside the packs.

Written from the Dagor Engine's BSD-3-Clause source:

- `prog/engine/shaders/rendInstRes.cpp` (`RenderableInstanceLodsResource::loadResource`,
  `patchAndLoadData`, `RenderableInstanceResource::loadResourceInternal`) and
  `prog/dagorInclude/shaders/dag_rendInstRes.h`: a resource is a 32-bit dump size
  (bit 24: impostor data follows), four ints (texture and material counts, or -1, -1
  when the materials live in `riDesc.bin`; the vertex-data count; the size of the
  vertex-data header with its compression in the top bits), the vertex data, the
  LOD dump (a patchable table of LODs, then the box and sphere), and per LOD the
  mesh dump and its optional voxel data.
- `prog/engine/shaders/matVdataLoad.cpp` (`ShaderMatVdata::loadMatVdata`,
  `makeTexAndMat`) and `shaderMesh.cpp` (`GlobalVertexData::initGvd`,
  `unpackToBuffers`, `ShaderMesh::patchData`), `dag_shaderMesh.h` (`RElem`) and
  `dag_shaderCommon.h` (`CompiledShaderChannelId`): the vertex-data header is a
  table of materials and one of vertex buffers (count, stride, index sizes, flags
  and the channel declaration); then each buffer's vertices and its indices,
  16 or 32 bit, plain or packed with meshoptimizer's index-sequence codec.
- `prog/3rdPartyLibs/meshoptimizer/src/indexcodec.cpp` (MIT,
  `meshopt_decodeIndexSequence`): a header byte, then per index a varint whose low
  bit picks one of two baselines and whose rest is a zigzag delta from it.
- `prog/engine/gameRes/gameResDescBin.cpp`: `riDesc.bin` is a BLK with one block per
  render instance, its `tex` names and `mat` blocks (`cls`, `t0`..`t15` indices
  into `tex`).

What is read: the positions and triangles of every LOD and which material each
element uses; a material's colour is the average of its diffuse texture (alpha
weighted for cut-out leaves). Decal and impostor elements are left out.
"""

from __future__ import annotations

import re
import struct
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from . import oodle

RENDINST_CLASS = 0x77F8232F
_VDATA_I32, _VDATA_PACKED_IB = 0x40, 0x200
_RELEM = 48
_STG_TRANS = 4

# Vertex channel types (VSDT_* >> 16, `dag_consts_base.h`) and usages (SCUSAGE_*).
_FLOAT1, _FLOAT2, _FLOAT3, _FLOAT4, _E3DCOLOR, _UBYTE4, _SHORT2, _SHORT4 = 0, 1, 2, 3, 4, 5, 6, 7
_SHORT2N, _SHORT4N, _USHORT2N, _USHORT4N, _UDEC3, _DEC3N, _HALF2, _HALF4 = 9, 10, 11, 12, 13, 14, 15, 16
_TYPE_BYTES = {_FLOAT1: 4, _FLOAT2: 8, _FLOAT3: 12, _FLOAT4: 16, _E3DCOLOR: 4, _UBYTE4: 4, _SHORT2: 4, _SHORT4: 8,
               _SHORT2N: 4, _SHORT4N: 8, _USHORT2N: 4, _USHORT4N: 8, _UDEC3: 4, _DEC3N: 4, _HALF2: 4, _HALF4: 8,
               17: 4, 18: 8, 19: 12, 20: 16, 21: 4, 22: 8, 23: 12, 24: 16}
_USAGE_POS = 0


class RendInstError(ValueError):
    pass


def decode_index_sequence(buf: bytes, count: int) -> np.ndarray:
    """meshoptimizer's index-sequence codec (version 0 or 1), vectorised."""
    if len(buf) < 1 + count + 4 or buf[0] & 0xF0 != 0xD0 or buf[0] & 0x0F > 1:
        raise RendInstError("not a packed index sequence")
    data = np.frombuffer(buf, np.uint8, len(buf) - 5, 1)
    ends = np.flatnonzero(data < 0x80)
    if len(ends) < count:
        raise RendInstError("packed index sequence ends early")
    ends = ends[:count]
    if count and ends[-1] != len(data) - 1:
        raise RendInstError("packed index sequence does not end at its tail")
    starts = np.r_[0, ends[:-1] + 1]
    v = np.zeros(count, np.int64)
    for k in range(5):  # up to five 7-bit groups, least significant first
        at = starts + k
        live = at <= ends
        v[live] |= (data[at[live]].astype(np.int64) & 0x7F) << (7 * k)
    current = v & 1
    v >>= 1
    d = (v >> 1) ^ -(v & 1)  # zigzag
    out = np.empty(count, np.int64)
    for c in (0, 1):
        m = current == c
        out[m] = np.cumsum(d[m])
    return (out & 0xFFFFFFFF).astype(np.uint32)


def _channel(vb: np.ndarray, at: int, t: int) -> np.ndarray:
    """One channel of every vertex (vb: (n, stride) uint8) as floats."""
    n = len(vb)
    raw = np.ascontiguousarray(vb[:, at : at + _TYPE_BYTES[t]])
    if t in (_FLOAT1, _FLOAT2, _FLOAT3, _FLOAT4):
        return raw.view("<f4").reshape(n, -1).astype(np.float32)
    if t in (_HALF2, _HALF4):
        return raw.view("<f2").reshape(n, -1).astype(np.float32)
    if t in (_SHORT2N, _SHORT4N):
        return raw.view("<i2").reshape(n, -1).astype(np.float32) / 32767.0
    if t in (_USHORT2N, _USHORT4N):
        return raw.view("<u2").reshape(n, -1).astype(np.float32) / 65535.0
    if t in (_SHORT2, _SHORT4):
        return raw.view("<i2").reshape(n, -1).astype(np.float32)
    if t in (_E3DCOLOR, _UBYTE4):
        return raw.astype(np.float32)
    raise RendInstError(f"vertex channel type {t} is not read")


@dataclass
class _Vdata:
    verts: int
    stride: int
    idx_bytes: int
    packed: int
    flags: int
    decl: list[tuple[int, int, int]]  # (type, usage, usage index)
    at: int  # where its vertices start in the decoded stream


@dataclass
class Elem:
    mat: int
    vdata: int
    sv: int
    numv: int
    si: int
    numf: int
    base: int
    trans: bool


@dataclass
class Lod:
    range: float
    elems: list[Elem]


@dataclass
class Resource:
    """One render instance as stored: its vertex buffers (decoded on demand), LODs and elements."""

    name: str
    stream: bytes
    vdata: list[_Vdata]
    lods: list[Lod]
    box: tuple
    impostor: bool
    _cache: dict = field(default_factory=dict)

    def buffers(self, i: int) -> tuple[np.ndarray, np.ndarray]:
        """Vertex positions (n, 3) and the index list of vertex buffer `i`."""
        if i not in self._cache:
            vd = self.vdata[i]
            vb = np.frombuffer(self.stream, np.uint8, vd.verts * vd.stride, vd.at).reshape(vd.verts, vd.stride)
            at, pos = 0, None
            for t, usage, _ui in vd.decl:
                if usage == _USAGE_POS and pos is None:
                    pos = _channel(vb, at, t)[:, :3]
                at += _TYPE_BYTES.get(t, 0)
            if pos is None:
                raise RendInstError(f"{self.name}: vertex buffer {i} has no position")
            ib_at = vd.at + vd.verts * vd.stride
            wide = bool(vd.flags & _VDATA_I32) or (vd.verts > 65536 and not vd.flags & 0x20)
            count = vd.idx_bytes // (4 if wide else 2)
            if vd.flags & _VDATA_PACKED_IB:
                idx = decode_index_sequence(self.stream[ib_at : ib_at + vd.packed], count)
            else:
                idx = np.frombuffer(self.stream, "<u4" if wide else "<u2", count, ib_at).astype(np.uint32)
            self._cache[i] = (pos, idx)
        return self._cache[i]

    def lod_mesh(self, lod: int, skip=None) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """One LOD's vertices (object space), triangles and each triangle's material index.

        `skip(mat, trans)` says which elements to leave out (decals, impostors)."""
        vs, fs, ms, base = [], [], [], 0
        for e in self.lods[lod].elems:
            if e.numf <= 0 or (skip is not None and skip(e.mat, e.trans)):
                continue
            pos, idx = self.buffers(e.vdata)
            tri = idx[e.si : e.si + 3 * e.numf].astype(np.int64) + e.base
            if len(tri) < 3 * e.numf or tri.max() >= len(pos):
                raise RendInstError(f"{self.name}: element indexes past its vertices")
            used, local = np.unique(tri, return_inverse=True)
            vs.append(pos[used])
            fs.append(local.reshape(-1, 3) + base)
            ms.append(np.full(e.numf, e.mat, np.int32))
            base += len(used)
        if not vs:
            return np.zeros((0, 3), np.float32), np.zeros((0, 3), np.int64), np.zeros(0, np.int32)
        return np.concatenate(vs).astype(np.float32), np.concatenate(fs), np.concatenate(ms)

    def faces(self, lod: int) -> int:
        return sum(max(e.numf, 0) for e in self.lods[lod].elems)


def _block(b: bytes, p: int) -> tuple[bytes, int]:
    """A Dagor compressed block (`dag_btagCompr.h`: 30-bit length, tag in the top two bits) decoded, and its end."""
    (w,) = struct.unpack_from("<I", b, p)
    n, tag = w & 0x3FFFFFFF, w >> 30
    body = b[p + 4 : p + 4 + n]
    if tag == 2:  # Oodle: the decoded size, then the data
        (size,) = struct.unpack_from("<i", body, 0)
        return oodle.decompress(body[4:], size), p + 4 + n
    if tag == 1:
        import zstandard

        return zstandard.ZstdDecompressor().decompressobj().decompress(body), p + 4 + n
    raise RendInstError(f"vertex data packed with tag {tag} is not read")


def read_resource(b: bytes, name: str = "") -> Resource:
    """A render-instance resource from its first byte (its offset in the pack)."""
    res_sz_w, n_tex, n_mat, n_vd, hdr_w = struct.unpack_from("<iiiiI", b, 0)
    res_sz = res_sz_w & 0xFFFFFF
    impostor = bool((res_sz_w >> 24) & 1)
    p = 20
    if n_tex != -1 or n_mat != -1:
        # Materials saved inside the resource: a texture-name table to skip; their parameters are in the header.
        (sz,) = struct.unpack_from("<i", b, p)
        p += 4 + sz
    hdr_sz = hdr_w
    if (hdr_w & 0xE0000000) == 0xC0000000:
        hdr_sz = hdr_w & ~0xC0000000
        stream, p = _block(b, p)
    elif hdr_w & 0x80000000 or hdr_w & 0x40000000:
        raise RendInstError(f"{name}: vertex data packed with zlib or LZMA is not read")
    else:
        total = 0
        hdr = b[p : p + hdr_sz]
        vdp, vdn = struct.unpack_from("<II", hdr, 16)
        for i in range(vdn):
            vn, a, bb, fl = struct.unpack_from("<IIII", hdr, vdp + 32 * i)
            total += vn * (a & 0xFF) + (((a >> 8) | ((bb >> 28) << 24)) if fl & _VDATA_PACKED_IB else bb & 0xFFFFFFF)
        stream = b[p : p + hdr_sz + total]
        p += hdr_sz + total
    vdp, vdn = struct.unpack_from("<II", stream, 16)
    if vdn != n_vd:
        raise RendInstError(f"{name}: {vdn} vertex buffers where the resource says {n_vd}")
    vdata, at = [], hdr_sz
    for i in range(vdn):
        vn, a, bb, fl, dp, dn = struct.unpack_from("<IIIIII", stream, vdp + 32 * i)
        stride, isz = a & 0xFF, bb & 0xFFFFFFF
        packed = ((a >> 8) | ((bb >> 28) << 24)) if fl & _VDATA_PACKED_IB else isz
        decl = [(t >> 16, u, ui) for t, u, ui, _s in (struct.unpack_from("<iihH", stream, dp + 12 * k) for k in range(dn))]
        vdata.append(_Vdata(vn, stride, isz, packed, fl, decl, at))
        at += vn * stride + packed
    if at > len(stream):
        raise RendInstError(f"{name}: vertex data ends early")
    dump = b[p : p + res_sz]
    p += res_sz
    lp, ln = struct.unpack_from("<II", dump, 0)
    box = (struct.unpack_from("<3f", dump, 16), struct.unpack_from("<3f", dump, 28))
    ranges = [struct.unpack_from("<f", dump, lp + 16 * i + 8)[0] for i in range(ln)]
    lods = []
    for i in range(ln):
        msz, vox = struct.unpack_from("<ii", b, p)
        p += 8
        m = b[p : p + msz]
        p += msz
        ep, en = struct.unpack_from("<II", m, 0)
        (mat_pass,) = struct.unpack_from("<I", m, 32)
        if mat_pass & 0x80000000:  # stage ends per stage
            trans_from = struct.unpack_from("<8H", m, 16)[_STG_TRANS - 1]
            total = en
        else:  # older: opaque elements, then the transparent ones in a second table right after
            tp, tn = struct.unpack_from("<II", m, 16)
            trans_from, total = en, en + (tn if tp == ep + _RELEM * en else 0)
        elems = []
        for k in range(total):
            _e, mat, vd, _o, sv, nv, si, nf, bv = struct.unpack_from("<QQQiiiiii", m, ep + _RELEM * k)
            elems.append(Elem(int(mat), int(vd), sv, nv, si, nf, bv, k >= trans_from))
        lods.append(Lod(ranges[i], elems))
        if vox:
            (vs,) = struct.unpack_from("<i", b, p)
            p += 4 + vs
    return Resource(name, stream, vdata, lods, box, impostor)


# --- materials and colours -------------------------------------------------------------------------------------

_DIFFUSE = re.compile(r"(_d|_tex_d|_diffuse|_albedo|_d_\w+|_tex_d_\w+)$")
_NOT_COLOUR = re.compile(r"(_n|_nm|_normal|_m|_mask|_tex_n|_tex_m|_ao|_spec|_s)$")
_SKIP_CLASS = re.compile(r"decal|impostor|billboard|shadow|occluder|glass_refl|water", re.I)


@dataclass
class Material:
    cls: str
    textures: list[str]  # by slot (t0, t1, ...), "" where unset
    two_sided: bool = False
    alpha_test: bool = False

    def colour_textures(self) -> list[str]:
        """The textures whose mix gives the surface its colour: a perlin-layered shader blends up to three
        detail diffuses (t0, t3, t5) by noise, so their average; every other shader its `diffuse()`."""
        if "perlin_layered" in self.cls:
            layers = [self.textures[k] for k in (0, 3, 5) if k < len(self.textures) and self.textures[k]]
            layers = [t for t in layers if not _NOT_COLOUR.search(t) and "overlay" not in t]
            if layers:
                return layers
        d = self.diffuse()
        return [d] if d else []

    def alpha_of(self, name: str) -> str | None:
        """A separate cut-out mask the material pairs with a diffuse (`x_d` with `x_a`), if it has one."""
        for suffix in ("_tex_d", "_d"):
            if name.endswith(suffix):
                a = name[: -len(suffix)] + suffix.replace("_d", "_a")
                if a in self.textures:
                    return a
        return None

    def diffuse(self) -> str | None:
        """The texture that gives the surface its colour: t0 for most shaders; for layered ones the first
        detail diffuse when t0 is an overlay or mask."""
        names = [t for t in self.textures if t]
        first = self.textures[0] if self.textures else ""
        if first and not _NOT_COLOUR.search(first) and "overlay" not in first:
            return first
        for t in self.textures[1:]:
            if t and _DIFFUSE.search(t) and "overlay" not in t:
                return t
        for t in names:
            if not _NOT_COLOUR.search(t):
                return t
        return first or None


class Descriptions:
    """`riDesc.bin` of every resource folder: each render instance's textures and materials."""

    def __init__(self, res_dirs: list[Path]):
        from .vromfs import Vromfs

        self.blocks: dict[str, object] = {}
        for d in res_dirs:
            p = Path(d) / "riDesc.bin"
            if not p.is_file():
                continue
            try:
                root = Vromfs(files={"riDesc.bin": p.read_bytes()}).blk("riDesc.bin")
            except Exception:
                continue
            for blk in root.blocks:
                self.blocks.setdefault(blk.name, blk)

    def materials(self, name: str) -> list[Material]:
        blk = self.blocks.get(name)
        if blk is None:
            return []
        tex_blk, mat_blk = blk.block("tex"), blk.block("mat")
        tex = [str(v).split("*")[0] for _k, v in (tex_blk.params if tex_blk else [])]
        out = []
        for mb in (mat_blk.blocks if mat_blk else []):
            slots = [""] * 16
            for k, v in mb.params:
                if len(k) >= 2 and k[0] == "t" and k[1:].isdigit() and isinstance(v, int) and 0 <= v < len(tex):
                    s = int(k[1:])
                    if s < 16:
                        slots[s] = tex[v]
            while slots and not slots[-1]:
                slots.pop()
            par = str(mb.get("par", "") or "")
            out.append(Material(str(mb.get("cls", "")), slots, bool(mb.get("two_sided", False)), "atest" in par))
        return out


#: Colours (linear) for a material whose texture is missing, by what its shader class says it is.
_FALLBACK = [(re.compile(r"tree|leaves|leaf|bush|grass|veget", re.I), (0.10, 0.16, 0.06)),
             (re.compile(r"glass|window", re.I), (0.05, 0.07, 0.09))]
DEFAULT_COLOUR = (0.32, 0.29, 0.25)
_LEAVES = re.compile(r"colored|leaves|leaf|bush|grass|veget", re.I)
_LUMA = np.float32([0.2126, 0.7152, 0.0722])
_LEAF_LUMA = 0.06
_FOLIAGE = (0.05, 0.09, 0.03)


def texture_colour(textures, name: str | None, alpha: str | None = None) -> np.ndarray | None:
    """A texture's average colour in linear light, alpha-weighted (cut-out leaves count only where they are);
    `alpha` names a separate mask texture where the material keeps its cut-out in one (`<name>_a`)."""
    if not name or textures is None:
        return None
    img = textures.image(name, 32)
    if img is None:
        return None
    rgb = img[:, :, :3].reshape(-1, 3).astype(np.float32) / 255.0
    lin = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    a = img[:, :, 3].reshape(-1).astype(np.float32) / 255.0
    mask = textures.image(alpha, 32) if alpha else None
    if mask is not None:
        from PIL import Image

        h, w = img.shape[:2]
        m = np.asarray(Image.fromarray(mask[:, :, 0]).resize((w, h)), np.float32) / 255.0
        a = np.minimum(a, m.reshape(-1))
    w = np.where(a > 0.5, 1.0, 0.0) if (a < 0.99).mean() > 0.05 else np.ones_like(a)
    if w.sum() < 1:
        w = np.ones_like(a)
    return (lin * w[:, None]).sum(0) / w.sum()


@dataclass
class Look:
    """An object at one LOD, ready to place: vertices, triangles, per-vertex linear colour."""

    verts: np.ndarray
    faces: np.ndarray
    colours: np.ndarray
    lod: int
    lods: int
    faces_per_lod: list[int]
    impostor: bool


class RenderIndex:
    """Render instances of the install: where each lives, its materials, its LOD meshes and their colours."""

    def __init__(self, resources, textures=None, res_dirs: list[Path] | None = None):
        self.resources = resources  # collision.ResourceIndex
        self.textures = textures
        dirs = res_dirs or sorted({p.parent for p, _o in resources.where.values()})
        self.desc = Descriptions(dirs)
        self._res: dict[str, Resource | Exception | None] = {}
        self._colours: dict[str, np.ndarray] = {}
        self._sizes: dict[Path, list[int]] = {}

    def _span(self, path: Path, ofs: int) -> int:
        """Bytes from `ofs` to the next resource in the pack."""
        if path not in self._sizes:
            offs = sorted({o for (p, o) in self.resources.where.values() if p == path} | {path.stat().st_size})
            self._sizes[path] = offs
        offs = self._sizes[path]
        i = np.searchsorted(offs, ofs, side="right")
        return (offs[i] if i < len(offs) else path.stat().st_size) - ofs

    def resource(self, name: str) -> Resource | None:
        if name not in self._res:
            where = self.resources.where.get((name, RENDINST_CLASS))
            if where is None:
                self._res[name] = None
            else:
                path, ofs = where
                try:
                    with path.open("rb") as fh:
                        fh.seek(ofs)
                        blob = fh.read(self._span(path, ofs))
                    self._res[name] = read_resource(blob, name)
                except (RendInstError, struct.error, ValueError, IndexError, OSError) as e:
                    self._res[name] = e
        r = self._res[name]
        return r if isinstance(r, Resource) else None

    def error(self, name: str) -> str | None:
        r = self._res.get(name)
        return f"{type(r).__name__}: {r}" if isinstance(r, Exception) else None

    def material_colour(self, mat: Material) -> np.ndarray:
        key = mat.cls + "|" + "|".join(mat.textures)
        if key not in self._colours:
            cs = [texture_colour(self.textures, t, mat.alpha_of(t)) for t in mat.colour_textures()]
            cs = [x for x in cs if x is not None]
            c = np.mean(cs, axis=0) if cs else None
            if c is not None and _LEAVES.search(mat.cls) and float(c @ _LUMA) < _LEAF_LUMA:
                # Leaves the game tints at run time (`*_colored` tree shaders) are stored dark: keep their hue at
                # a foliage brightness, half way to a plain foliage green.
                c = 0.5 * c * (_LEAF_LUMA / max(float(c @ _LUMA), 1e-4)) + 0.5 * np.float32(_FOLIAGE)
            if c is None:
                c = next((np.array(col, np.float32) for rx, col in _FALLBACK if rx.search(mat.cls + " " + " ".join(mat.textures))),
                         np.array(DEFAULT_COLOUR, np.float32))
            self._colours[key] = np.asarray(c, np.float32)
        return self._colours[key]

    def look(self, name: str, lod: int) -> Look | None:
        """The object at a LOD (clamped to the LODs it has), without decals and impostor billboards."""
        res = self.resource(name)
        if res is None or not res.lods:
            return None
        mats = self.desc.materials(name)
        lod = int(np.clip(lod, 0, len(res.lods) - 1))

        def skip(m: int, trans: bool) -> bool:
            if m < len(mats):
                return bool(_SKIP_CLASS.search(mats[m].cls))
            return False

        v, f, m = res.lod_mesh(lod, skip)
        if not len(f):
            return None
        cols = np.empty((len(v), 3), np.float32)
        table = np.array([self.material_colour(x) for x in mats] or [DEFAULT_COLOUR], np.float32)
        fc = table[np.clip(m, 0, len(table) - 1)]
        cols[f.ravel()] = np.repeat(fc, 3, axis=0)
        return Look(v, f, cols, lod, len(res.lods), [res.faces(i) for i in range(len(res.lods))], res.impostor)

    def average_colour(self, name: str) -> np.ndarray | None:
        """The object's colour as one value: its coarsest mesh LOD's colours, weighted by triangle area."""
        lods = self.mesh_lods(name)
        if not lods:
            return None
        look = self.look(name, len(lods) - 1)
        if look is None:
            return None
        tri = look.verts[look.faces]
        area = np.linalg.norm(np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]), axis=1) + 1e-9
        return (look.colours[look.faces[:, 0]] * area[:, None]).sum(0) / area.sum()

    def leaf_colour(self, name: str) -> np.ndarray | None:
        """A tree's crown colour: of its coarsest mesh LOD, the material covering the most area."""
        lods = self.mesh_lods(name)
        res = self.resource(name)
        if not lods or res is None:
            return None
        mats = self.desc.materials(name)
        v, f, m = res.lod_mesh(len(lods) - 1, lambda k, _t: k < len(mats) and bool(_SKIP_CLASS.search(mats[k].cls)))
        if not len(f) or not mats:
            return None
        tri = v[f]
        area = np.linalg.norm(np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]), axis=1)
        per = np.bincount(np.clip(m, 0, len(mats) - 1), area, len(mats))
        return self.material_colour(mats[int(per.argmax())])

    def mesh_lods(self, name: str, ranges: bool = False) -> list:
        """Each LOD's triangle count (with `ranges`, (count, the distance up to which the game draws it)), without
        the impostor LOD at the end; empty when the object has no render mesh."""
        res = self.resource(name)
        if res is None:
            return []
        mats = self.desc.materials(name)
        out = []
        for i, lod in enumerate(res.lods):
            n = 0
            imp = False
            for e in lod.elems:
                cls = mats[e.mat].cls if e.mat < len(mats) else ""
                if "impostor" in cls or "billboard" in cls:
                    imp = True
                    continue
                if _SKIP_CLASS.search(cls):
                    continue
                n += max(e.numf, 0)
            if imp and n == 0:
                break
            out.append((n, float(lod.range)) if ranges else n)
        return out
