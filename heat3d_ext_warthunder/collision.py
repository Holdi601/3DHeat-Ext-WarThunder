"""
Object shapes from War Thunder's resource packs (`content/base/res/*.grp`): the
collision resource of each placed object (`<object>_collision`), as triangles.

Written from the Dagor Engine's BSD-3-Clause source:

- `prog/engine/gameRes/grpData.h`: a pack is `GRP2`/`GRP3`, the sizes, then a
  table of names and of (class id, file offset, name index) per resource.
- `prog/engine/sharedInclude/gameRes/collResStream.h` and
  `prog/engine/gameRes/collisionGameResLoad.cpp` (`loadStream`): a collision
  resource is the label `0xACE5_0003`, a block (zstd, Oodle or plain), a 108-byte
  header with eleven array counts, one 8-byte bind record per node, then the
  arrays: 48-byte node records (type, triangle count, model box), the node
  matrices, the per-node triangle chunks, and the name pools.
- `prog/engine/daBVH/bvhIO.cpp` (`deserializeQuadBLASToSoA4`) and
  `prog/dagorInclude/daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`: a triangle
  chunk is its dequantisation frame, a `dBLi` header, 21-bit packed vertices and
  a tree whose leaves hold one or two quads as offsets from an apex vertex.

Only the shapes are read; materials, physics and destruction data are skipped.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from . import oodle

COLLISION_CLASS = 0xACE50000
RENDINST_CLASS = 0x77F8232F
_ARRAYS = 11
_ELEM = {1: 48, 2: 48, 3: 48, 6: 2, 7: 28, 8: 16, 9: 1, 10: 1}  # bytes per element, by array id (0 nodes, 4 chunks apart)
_RAW, _SHORT, _SHORT_FLIP = 0xFF, 0xFE, 0xFD
_LEAF_FLAG = 1 << 31
_FLIPA, _FLIPB = 1 << 29, 1 << 30
TYPE_MESH, TYPE_POINTS, TYPE_BOX, TYPE_SPHERE, TYPE_CAPSULE, TYPE_CONVEX = range(6)


class CollisionError(ValueError):
    pass


def grp_table(path: Path) -> list[tuple[str, int, int]]:
    """(name, class id, offset) of every resource in a pack; [] for something else."""
    with path.open("rb") as fh:
        head = fh.read(16)
        if len(head) < 16:
            return []
        label, desc, _full, _rest = struct.unpack("<4sIII", head)
        if label not in (b"GRP2", b"GRP3"):
            return []
        d = head + fh.read(desc)
    names_at, n_names = struct.unpack_from("<II", d, 16)
    res_at, n_res = struct.unpack_from("<II", d, 32)
    names = []
    for i in range(n_names):
        (o,) = struct.unpack_from("<i", d, names_at + 4 * i)
        names.append(d[o : d.index(b"\0", o)].decode("latin1") if o >= 0 else "")
    out = []
    for i in range(n_res):
        cid, ofs, rid, _ = struct.unpack_from("<IIHH", d, res_at + 12 * i)
        if rid < len(names):
            out.append((names[rid], cid, ofs))
    return out


class ResourceIndex:
    """Where each resource lives, over the packs of the folders given (the first pack naming it wins)."""

    def __init__(self, *res_dirs: Path):
        self.where: dict[tuple[str, int], tuple[Path, int]] = {}
        packs = [p for d in res_dirs for p in sorted(Path(d).glob("*.grp"))]
        for p in packs:
            try:
                for name, cid, ofs in grp_table(p):
                    self.where.setdefault((name, cid), (p, ofs))
            except (OSError, struct.error, ValueError):
                continue

    def collision(self, name: str) -> tuple[Path, int] | None:
        return self.where.get((name + "_collision", COLLISION_CLASS))


def _sx13(v: int) -> int:
    v &= 0x1FFF
    return v - 0x2000 if v & 0x1000 else v


class _Reader:
    def __init__(self, b: bytes):
        self.b, self.p = b, 0

    def take(self, n: int) -> bytes:
        r = self.b[self.p : self.p + n]
        if len(r) != n:
            raise CollisionError("collision resource ends early")
        self.p += n
        return r

    def u8(self) -> int:
        return self.take(1)[0]


def _leaf_tris(w0: int, w1: int, w2: int, w3: int, out: list):
    base = w1 & 0xFFFFFF
    o1, o2 = _sx13(w0), _sx13(w0 >> 13)
    o3 = _sx13(((w0 >> 26) & 0x1F) | ((w1 >> 24) << 5))
    out.append((base, base + o1, base + o2))
    if o3 != o2:
        a, b = (o2, o1) if w2 & _FLIPA else (o1, o2)
        out.append((base + a, base + b, base + o3))
    o1b, o2b, o3b = _sx13(w2 >> 16), _sx13(w3), _sx13(w3 >> 13)
    if o1b != o2b:
        bb = base + (w2 & 0xFFFF)
        out.append((bb, bb + o1b, bb + o2b))
        if o3b != o2b:
            a, b = (o2b, o1b) if w2 & _FLIPB else (o1b, o2b)
            out.append((bb + a, bb + b, bb + o3b))


def _chunk(r: _Reader) -> tuple[np.ndarray, np.ndarray]:
    """One node's triangle chunk: vertices in the resource's space and their triangles."""
    frame = struct.unpack("<9f", r.take(36))
    inv_scale, bmin = np.array(frame[3:6], np.float32), np.array(frame[6:9], np.float32)
    magic, version, stride, leaf_size, tree_bytes, n_verts = struct.unpack("<4sHBBII", r.take(16))
    r.take(24)  # the whole box, again
    if magic != b"dBLi" or stride != 8:
        raise CollisionError("not a BLAS chunk")
    io_flags = struct.unpack("<I", r.take(4))[0] if version >= 2 else 0
    packed = np.frombuffer(r.take(8 * n_verts), "<u8")
    q = np.stack([packed & 0x1FFFFF, (packed >> 21) & 0x1FFFFF, packed >> 42], 1).astype(np.float32) / 32.0
    verts = q * inv_scale + bmin
    tris: list = []
    used = 0
    leaves = 0

    def node(depth: int):
        nonlocal used, leaves
        if depth > 256:
            raise CollisionError("BLAS tree too deep")
        cc = r.u8()
        if cc in (0, _RAW, _SHORT, _SHORT_FLIP):
            if cc in (_SHORT, _SHORT_FLIP):
                w0, w1 = struct.unpack("<II", r.take(8))
                w2, w3 = (_FLIPA if cc == _SHORT_FLIP else 0), 0
            else:
                w0, w1, w2, w3 = struct.unpack("<4I", r.take(16))
            used += 28
            leaves += 1
            if cc != _RAW and w0 & _LEAF_FLAG:
                _leaf_tris(w0, w1, w2, w3, tris)
            return
        used += 16
        for _ in range(cc):
            node(depth + 1)

    while used < tree_bytes:
        node(0)
    if used != tree_bytes:
        raise CollisionError("BLAS tree does not match its header")
    if io_flags & 1:
        r.take(2 * leaves)
    faces = np.array(tris, np.int64).reshape(-1, 3)
    if len(faces) and (faces.min() < 0 or faces.max() >= n_verts):
        raise CollisionError("BLAS triangle past its vertices")
    return verts, faces


_SANE = 1e5  # metres: an object's own space is never this large; empty boxes are stored as +-1e32


def _sane(lo, hi) -> bool:
    return all(abs(c) < _SANE for c in (*lo, *hi)) and all(a <= b for a, b in zip(lo, hi))


def _box(lo, hi) -> tuple[np.ndarray, np.ndarray]:
    x0, y0, z0 = lo
    x1, y1, z1 = hi
    v = np.array([[x0, y0, z0], [x1, y0, z0], [x1, y0, z1], [x0, y0, z1],
                  [x0, y1, z0], [x1, y1, z0], [x1, y1, z1], [x0, y1, z1]], np.float32)
    f = np.array([[0, 2, 1], [0, 3, 2], [4, 5, 6], [4, 6, 7], [0, 1, 5], [0, 5, 4],
                  [1, 2, 6], [1, 6, 5], [2, 3, 7], [2, 7, 6], [3, 0, 4], [3, 4, 7]], np.int64)
    return v, f


@dataclass
class Shape:
    verts: np.ndarray  # (n, 3) float32, the object's own space
    faces: np.ndarray  # (m, 3) int64
    box: tuple  # (min xyz, max xyz) of the whole resource


def read_collision(blob: bytes) -> Shape:
    """A collision resource (from its label on) as one triangle set: meshes and convex hulls as stored, boxes, spheres and capsules as boxes."""
    (label,) = struct.unpack_from("<I", blob, 0)
    if label & 0xFFFF0000 != COLLISION_CLASS:
        raise CollisionError("not a collision resource")
    if label & 0xFFFF != 3:
        raise CollisionError(f"collision resource version {label & 0xFFFF} is not read")
    (word,) = struct.unpack_from("<I", blob, 4)
    fmt, n = word >> 30, word & 0x3FFFFFFF
    body = blob[8 : 8 + n]
    if fmt == 2:
        (src,) = struct.unpack_from("<i", body, 0)
        body = oodle.decompress(body[4:], src)
    elif fmt == 1:
        import zstandard

        body = zstandard.ZstdDecompressor().decompressobj().decompress(body)
    r = _Reader(body)
    head = r.take(108)
    box = (struct.unpack_from("<3f", head, 32), struct.unpack_from("<3f", head, 44))
    counts = struct.unpack_from(f"<{_ARRAYS}I", head, 64)
    n_nodes = counts[0]
    r.take(8 * n_nodes)  # bind records
    nodes = []
    tms: list[np.ndarray] = []
    vs, fs = [], []
    for aid in range(_ARRAYS):
        if aid == 0:
            for _ in range(n_nodes):
                rec = r.take(48)
                n_idx = struct.unpack_from("<I", rec, 4)[0]
                ntype = rec[19]
                lo, hi = struct.unpack_from("<3f", rec, 20), struct.unpack_from("<3f", rec, 32)
                nodes.append((n_idx, ntype, lo, hi))
        elif aid == 1:
            # The node's placement in the object (TMatrix: three axes, then the position). Primitive
            # nodes (boxes, spheres, capsules) keep their box in the node's own space; meshes are stored
            # already placed.
            tms = [np.frombuffer(r.take(48), "<f4").reshape(4, 3) for _ in range(n_nodes)]
        elif aid == 4:
            for k, (n_idx, ntype, lo, hi) in enumerate(nodes):
                if n_idx:
                    v, f = _chunk(r)
                    vs.append(v)
                    fs.append(f)
                elif ntype in (TYPE_BOX, TYPE_SPHERE, TYPE_CAPSULE) and _sane(lo, hi) and all(a < b for a, b in zip(lo, hi)):
                    v, f = _box(lo, hi)
                    if tms:
                        v = v @ tms[k][:3] + tms[k][3]
                    vs.append(v)
                    fs.append(f)
        elif aid != 5 and counts[aid]:
            r.take(counts[aid] * _ELEM[aid])
    keep = [(v, f) for v, f in zip(vs, fs) if len(v) and np.isfinite(v).all() and np.abs(v).max() < _SANE]
    if not keep and _sane(*box) and box[0] != box[1]:
        keep = [_box(*box)]
    if not keep:
        raise CollisionError("no usable shape")
    # Re-index after dropping parts: each part's faces were offset by the vertices before it.
    out_v, out_f, at = [], [], 0
    for v, f in keep:
        out_f.append(f + at)
        out_v.append(v)
        at += len(v)
    return Shape(np.concatenate(out_v).astype(np.float32), np.concatenate(out_f), box)


def load_shape(index: ResourceIndex, name: str) -> Shape | None:
    where = index.collision(name)
    if where is None:
        return None
    path, ofs = where
    with path.open("rb") as fh:
        fh.seek(ofs)
        head = fh.read(8)
        (word,) = struct.unpack_from("<I", head, 4)
        blob = head + fh.read(word & 0x3FFFFFFF)
    return read_collision(blob)
