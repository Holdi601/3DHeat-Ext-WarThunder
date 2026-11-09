"""
A War Thunder level into the 3DHeat level contract: one `.glb` with parts named
`ground:<level>`, `water:<level>`, plus the tactical map images and a `.json`
recording what was read.

Coordinates are the game's metres with z mirrored: glb (x, y, z) = game
(x, y, -z). The game's world is left-handed (x east, y up, z north); glTF is
right-handed. The replay tables of `heat3d-wt-replay` keep the game's z and tell
the viewer to mirror it (`flipZ`), so a level written this way and a replay of
the same map land on top of each other with no placement step.

What goes in:

- the heightmap (`HM2`), as a grid: at full detail over the tank map's area
  (or the air map's, when the level has no tank map), coarser elsewhere, each
  within `max_grid` samples a side;
- the land mesh's collision triangles (`LTdump`), where the heightmap does not
  reach (the whole level for naval and many air maps, the surroundings of a
  tank map's heightmap otherwise);
- the water: one flat rectangle at the level's `water_level` over the whole
  terrain. That is how the game draws it: one plane, under which low ground is
  sea, lake or river bed. Levels with a water heightmap (`WHM`, sloping rivers)
  get only the plane;
- the tactical maps (`<level>_map`, `<level>_tankmap` or the level's own
  `customLevelMap`), as PNGs beside the glb, placed by the level's
  `mapCoord0/1` and `tankMapCoord0/1`, and as the ground's texture where they
  cover it.

Buildings and other placed objects (`RIGz`, the render-instance generator, and
the collision shapes in `content/base/res/*.grp`) are not read.
"""

from __future__ import annotations

import json
import re
import struct
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from . import __version__
from .dagorlevel import Heightmap, read_level, summary
from .dxp import TexturePack
from .glb import Part, write_glb
from .vromfs import Blk, Vromfs

DEFAULT_MAX_GRID = 1024


@dataclass
class MapImage:
    kind: str  # "map" (the air map, mapCoord) or "tankmap" (tankMapCoord)
    texture: str
    rect: tuple[float, float, float, float]  # x0, z0, x1, z1 in game metres
    image: np.ndarray | None = None


@dataclass
class Game:
    root: Path
    _aces: Vromfs | None = None
    _maps: TexturePack | None = None
    _blks: dict[str, Blk] = field(default_factory=dict)
    _resources: object = None
    _shapes: dict = field(default_factory=dict)
    _textures: object = None
    _render: object = None

    def levels(self) -> list[Path]:
        return sorted((self.root / "levels").glob("*.bin"))

    def aces(self) -> Vromfs:
        if self._aces is None:
            self._aces = Vromfs(self.root / "aces.vromfs.bin")
        return self._aces

    def level_blk(self, name: str) -> Blk | None:
        if name not in self._blks:
            path = f"levels/{name}.blk"
            self._blks[name] = self.aces().blk(path) if path in self.aces().files else None
        return self._blks[name]

    def map_pack(self) -> TexturePack | None:
        if self._maps is None:
            p = self.root / "content" / "base" / "res" / "locations_maps.dxp.bin"
            if p.is_file():
                self._maps = TexturePack(p)
        return self._maps


    def resources(self):
        if self._resources is None:
            from .collision import ResourceIndex

            content = self.root / "content"
            # The base packs first, then the optional packages (infantry, ...), which hold newer levels' objects.
            dirs = [content / "base" / "res"] + sorted(d for d in content.glob("*/res") if d.parent.name != "base")
            self._resources = ResourceIndex(*dirs)
        return self._resources

    def shape(self, name: str):
        """An object's collision shape (cached), or None when the packs have none."""
        if name not in self._shapes:
            from .collision import CollisionError, load_shape

            try:
                self._shapes[name] = load_shape(self.resources(), name)
            except (CollisionError, OSError, struct.error, ValueError) as e:
                self._shapes[name] = e
        s = self._shapes[name]
        return None if isinstance(s, Exception) else s

    def textures(self):
        """Every texture of the install by name (`terrain.Textures`), or None when the packs cannot be indexed."""
        if self._textures is None:
            from .terrain import Textures

            try:
                self._textures = Textures(self.root)
            except Exception:
                self._textures = False
        return self._textures or None

    def render_index(self):
        """The render instances' meshes and materials (`rendinst.RenderIndex`), or None without `riDesc.bin`."""
        if self._render is None:
            from .rendinst import RenderIndex

            try:
                self._render = RenderIndex(self.resources(), self.textures())
            except Exception:
                self._render = False
        return self._render or None


#: Objects drawn as a tree glyph rather than by their collision shape (a trunk, for most trees).
VEGETATION = re.compile(
    r"tree|bush|oak|aspen|pine|palm|(?<![a-z])fir|birch|poplar|populus|tilia|cypress|spruce|willow|maple|beech|"
    r"acacia|baobab|shrub|flower|grass|reed|typha|cane|plant|vine|ivy|hedge(?!hog)|forest|jungle|cactus|bamboo"
)


CONIFER = re.compile(r"pine|(?<![a-z])fir|spruce|cypress|conifer|larch|cedar|thuja|juniper|picea|abies")


def _tree_glyph(box, conifer: bool = False) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """A tree over its box in 18 triangles: a three-sided trunk and a six-sided crown (a cone for conifers, a
    double cone for broadleaves). Returns vertices, triangles and which of them are crown (True) or trunk."""
    (x0, y0, z0), (x1, y1, z1) = box
    h = max(y1 - y0, 0.5)
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    r = max(min((x1 - x0), (z1 - z0)) / 2, h * 0.12)
    base = y0 + h * (0.15 if conifer else 0.3)
    mid = y0 + h * (0.3 if conifer else 0.6)
    rt = max(h * 0.025, 0.08)
    trunk = [(cx + rt * np.cos(a), yy, cz + rt * np.sin(a)) for yy in (y0, base + h * 0.05) for a in (0, 2.1, 4.2)]
    ring = [(cx + r * np.cos(a), mid, cz + r * np.sin(a)) for a in np.linspace(0, 2 * np.pi, 7)[:-1]]
    v = np.array(trunk + [(cx, y0 + h, cz), (cx, base, cz)] + ring, np.float32)
    f = []
    for i in range(3):  # trunk sides, outward
        a, b = i, (i + 1) % 3
        f += [(a, b + 3, b), (a, a + 3, b + 3)]
    top, bottom = 6, 7
    for i in range(6):
        a, b = 8 + i, 8 + (i + 1) % 6
        f += [(top, b, a), (bottom, a, b)]
    crown = np.zeros(len(v), bool)
    crown[6:] = True
    return v, np.array(f, np.int64), crown


DEFAULT_MAX_OBJECT_TRIANGLES = 4_000_000

#: What each `--detail` costs and gives. `core` is the middle share of the tank map (by width) drawn at `core_step`
#: heightmap samples, the rest of the tank map at `ring_step`, both coarser where the two would pass `ground`
#: triangles (a heightmap finer than 2 m); `objects` is the placed objects' triangle budget,
#: `per_object` the most triangles one object may have before a coarser LOD is taken; `terrain_mpp` the ground
#: colour's metres per pixel; `whole_grid` the samples a side of a level without a tank map (air maps), drawn
#: whole at one step when `max_grid` is left at its default; `density` the share of generated objects kept, by kind.
DETAIL = {
    "low": {"core": 0.5, "core_step": 4, "ring_step": 8, "ground": 300_000, "objects": 1_200_000, "per_object": 1_500, "terrain_mpp": 4.0, "whole_grid": 1024,
            "density": {"trees": 0.35, "bushes": 0.2, "props": 0.5, "buildings": 1.0}},
    "medium": {"core": 0.5, "core_step": 2, "ring_step": 4, "ground": 1_000_000, "objects": 3_500_000, "per_object": 4_000, "terrain_mpp": 2.0, "whole_grid": 1024,
               "density": {"trees": 0.7, "bushes": 0.5, "props": 1.0, "buildings": 1.0}},
    "high": {"core": 0.5, "core_step": 1, "ring_step": 2, "ground": 3_700_000, "objects": 4_500_000, "per_object": 12_000, "terrain_mpp": 1.0, "whole_grid": 2048,
             "density": {"trees": 1.0, "bushes": 1.0, "props": 1.0, "buildings": 1.0}},
}
DEFAULT_DETAIL = "medium"
_GLYPH, _SHAPE = -1, -3  # stand-ins: a tree's crown, an object's collision shape (never a box: drawn, boxes are
#                         cubes around objects)


def _srgb(c: np.ndarray) -> np.ndarray:
    c = np.clip(np.asarray(c, np.float32), 0.0, 1.0)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(c, 1 / 2.4) - 0.055).astype(np.float32)


def height_sampler(hm: Heightmap):
    """Bilinear ground height at game (x, z) arrays from the heightmap, clamped to its edge."""
    hh = hm.heights
    rows, cols = hh.shape

    def height(x, z):
        fx = np.clip((np.asarray(x, np.float64) - hm.origin_x) / hm.cell, 0, cols - 1.001)
        fz = np.clip((np.asarray(z, np.float64) - hm.origin_z) / hm.cell, 0, rows - 1.001)
        c, r = np.floor(fx).astype(np.int64), np.floor(fz).astype(np.int64)
        tx, tz = fx - c, fz - r
        a = hh[r, c] * (1 - tx) + hh[r, c + 1] * tx
        b = hh[r + 1, c] * (1 - tx) + hh[r + 1, c + 1] * tx
        return (a * (1 - tz) + b * tz).astype(np.float32)

    return height


@dataclass
class _Type:
    name: str
    tree: bool
    matrices: np.ndarray  # (n, 3, 4)
    options: list  # [(LOD index or _GLYPH / _SHAPE, triangles, LOD range)], finest first
    pick: int  # index into options
    volume: float
    box: tuple = ((0, 0, 0), (0, 0, 0))
    shape: object = None
    generated: int = 0
    first: int = 0  # the pick within the per-object limit, the finest the budget may give back

    @property
    def cost(self) -> int:
        return len(self.matrices) * self.options[self.pick][1]


def _pick_at(t: _Type, d: float) -> int:
    """The option the game itself would draw at distance `d`: the first mesh LOD whose range reaches it; past the
    last one, a tree's glyph (the game shows its impostor there) or a building's coarsest LOD."""
    last = t.first
    for k in range(t.first, len(t.options)):
        opt, _n, rng = t.options[k]
        if opt < 0 and opt != _SHAPE:
            break
        last = k
        if rng >= d:
            return k
    if t.tree and t.options[-1][0] == _GLYPH:
        return len(t.options) - 1
    return last


def _choose(types: list[_Type], budget: int) -> tuple[list[str], float]:
    """LODs as the game would pick them for one viewing distance, the shortest whose total fits the budget: small
    props drop to coarse LODs early and large buildings late, by the ranges their makers gave each LOD. If even the
    coarsest fits not, the trees that save most become crowns, and then the smallest types are left out."""
    import heapq

    def total_at(d: float) -> int:
        return sum(len(t.matrices) * t.options[_pick_at(t, d)][1] for t in types)

    ranges = sorted({0.0} | {o[2] for t in types for o in t.options if np.isfinite(o[2])} | {float("inf")})
    lo, hi = 0, len(ranges) - 1
    if total_at(ranges[0]) <= budget:
        hi = 0
    while lo < hi:
        mid = (lo + hi) // 2
        if total_at(ranges[mid]) <= budget:
            hi = mid
        else:
            lo = mid + 1
    d = ranges[hi]
    for t in types:
        t.pick = _pick_at(t, d)
    total = sum(t.cost for t in types)
    if hi > 0:
        # What the step to `d` saved beyond the budget goes back to the largest objects: the LOD they had a step
        # nearer, largest first, while it fits.
        nearer = ranges[hi - 1]
        for t in sorted(types, key=lambda t: -t.volume):
            k = _pick_at(t, nearer)
            extra = len(t.matrices) * (t.options[k][1] - t.options[t.pick][1])
            if k < t.pick and total + extra <= budget:
                t.pick = k
                total += extra
    heap: list = []

    def push(i: int) -> None:
        t = types[i]
        if t.pick + 1 < len(t.options):
            heapq.heappush(heap, (-len(t.matrices) * (t.options[t.pick][1] - t.options[t.pick + 1][1]), i))

    if total > budget:
        for i in range(len(types)):
            push(i)
    while total > budget and heap:
        _gain, i = heapq.heappop(heap)
        t = types[i]
        total -= t.cost
        t.pick += 1
        total += t.cost
        push(i)
    dropped = []
    if total > budget:
        for t in sorted(types, key=lambda t: t.volume):
            if total <= budget:
                break
            total -= t.cost
            dropped.append(t.name)
    return dropped, d


def _add_objects(geo, game: "Game", level, name: str, record: dict, log, budget: int = DEFAULT_MAX_OBJECT_TRIANGLES,
                 detail: dict | None = None, generate: bool = True, rect=None, kinds=None) -> None:
    """The level's objects as structure parts: the fixed ones (RIGz) and, with `generate`, those its land classes
    generate (forests, bushes, town blocks), each drawn by its render mesh at the finest LOD the budget allows and
    coloured by its materials' textures. Objects without a render mesh fall back to their collision shape, trees
    without one to a crown glyph. Over the budget, the types costing most step down a LOD at a time (then to their
    crown), and if that is not enough the smallest types are left out; the JSON lists it.
    """
    from .rigen import read_rigen

    detail = detail or DETAIL[DEFAULT_DETAIL]
    data, bl = level.data, level.table
    if "RIGz" not in bl:
        return
    t0 = time.time()
    rg = read_rigen(data, bl["RIGz"][0])
    instances: dict[str, list[np.ndarray]] = {}
    generated: dict[str, int] = {}
    for obj, placed in rg.placed.items():
        instances.setdefault(obj, []).append(np.concatenate(placed.matrices))
    gen_stats = None
    kind_of: dict[str, str] = {}
    if generate and level.heightmap is not None:
        from .landgen import generate as land_generate

        try:
            gmats, gen_stats = land_generate(game, data, bl, height=height_sampler(level.heightmap), rect=rect,
                                             kinds=kinds or ("trees", "bushes", "buildings", "props"),
                                             density=detail.get("density"))
            for obj, m in gmats.items():
                instances.setdefault(obj, []).append(m.astype(np.float32))
                generated[obj] = len(m)
                kind_of[obj] = gen_stats.get("objects", {}).get(obj, {}).get("kind", "")
        except Exception as e:  # the fixed objects stand without the generated ones
            gen_stats = {"error": f"{type(e).__name__}: {e}"}
            log(f"  generated objects: not made ({type(e).__name__}: {e})")
    t_gen = time.time() - t0
    ri = game.render_index()
    missing: dict[str, int] = {}
    types: list[_Type] = []
    for obj, ms in instances.items():
        m = np.concatenate(ms) if len(ms) > 1 else ms[0]
        if not len(m):
            continue
        tree = kind_of.get(obj) in ("trees", "bushes", "grass") or bool(VEGETATION.search(obj.lower()))
        lods = ri.mesh_lods(obj, ranges=True) if ri is not None else []
        # (option, triangles, the game's LOD range in metres). A LOD that costs what the one before it does gains
        # nothing (it only stretches that one's range).
        options: list = []
        for i, (n, rng) in enumerate(lods):
            if n <= 0:
                continue
            if options and n >= options[-1][1]:
                options[-1] = (options[-1][0], options[-1][1], rng)
            else:
                options.append((i, n, rng))
        inf = float("inf")
        res = ri.resource(obj) if (ri is not None and options) else None
        shape = None
        if res is not None:
            box = res.box
            if tree:
                options.append((_GLYPH, 18, inf))
        else:
            shape = game.shape(obj)
            if shape is None:
                missing[obj] = len(m)
                continue
            box = shape.box
            options = [(_GLYPH, 18, inf)] if tree else [(_SHAPE, len(shape.faces), inf)]
        # The finest LOD within the per-object limit (or the coarsest mesh LOD).
        pick = next((k for k, o in enumerate(options) if o[1] <= detail["per_object"]), max(len(options) - 2, 0))
        (x0, y0, z0), (x1, y1, z1) = box
        scale = float(np.abs(np.linalg.det(m[0, :, :3])))
        types.append(_Type(obj, tree, m, options, pick, max((x1 - x0) * (y1 - y0) * (z1 - z0), 0.0) * scale,
                           box, shape, generated.get(obj, 0), pick))
    dropped, lod_distance = _choose(types, budget)
    dropped = set(dropped)
    groups = {"buildings": ([], [], []), "trees": ([], [], [])}
    counts = {"buildings": 0, "trees": 0}
    drawn_as: dict[str, int] = {}
    tris = 0
    for t in types:
        if t.name in dropped:
            continue
        opt = t.options[t.pick][0]
        if opt == _GLYPH:
            sv, sf, crown = _tree_glyph(t.box, bool(CONIFER.search(t.name.lower())))
            leaves = ri.leaf_colour(t.name) if (ri is not None and t.shape is None) else None
            sc = np.where(crown[:, None], leaves if leaves is not None else np.float32([0.05, 0.09, 0.03]),
                          np.float32([0.09, 0.06, 0.04])).astype(np.float32)
            label = "glyph"
        elif opt == _SHAPE:
            sv, sf = t.shape.verts, t.shape.faces
            sc, label = np.tile(np.float32([0.36, 0.32, 0.27]), (len(sv), 1)), "collision"
        else:
            look = ri.look(t.name, opt)
            if look is None:
                continue
            sv, sf, sc, label = look.verts, look.faces, look.colours, f"lod{opt}"
        drawn_as[label] = drawn_as.get(label, 0) + len(t.matrices)
        m = t.matrices
        key = "trees" if t.tree else "buildings"
        vl, fl, cl = groups[key]
        start = sum(len(x) for x in vl)
        w = np.einsum("nij,vj->nvi", m[:, :, :3], sv.astype(np.float32)) + m[:, None, :, 3]
        w[:, :, 2] *= -1  # glb z = -game z
        vl.append(w.reshape(-1, 3).astype(np.float32))
        cl.append(np.tile(sc.astype(np.float32), (len(m), 1)))
        # Mirroring z turns the winding; an instance that is itself mirrored turns it back.
        flip = np.linalg.det(m[:, :, :3].astype(np.float64)) < 0
        offs = (np.arange(len(m)) * len(sv))[:, None, None]
        f = np.where(flip[:, None, None], sf[None, :, :], sf[None, :, [0, 2, 1]]) + offs
        fl.append(f.reshape(-1, 3) + start)
        counts[key] += len(m)
        tris += len(m) * len(sf)
    for key, (vl, fl, cl) in groups.items():
        if vl:
            # sRGB-encoded, as the 3DHeat viewer reads COLOR_0 (it shows vertex colours as they are, the same
            # way it shows texture texels); the colours were averaged in linear light.
            geo.add(f"structure:{name} {key}", np.concatenate(vl), np.concatenate(fl).astype(np.uint32),
                    vcolours=_srgb(np.concatenate(cl)))
    gen_record = None
    if gen_stats is not None:
        gen_record = {k: gen_stats[k] for k in ("instances", "kinds", "tried", "seconds", "missingLandClasses", "error")
                      if k in gen_stats}
        gen_record["perLandClass"] = gen_stats.get("landClasses")
        gen_record["rect"] = list(rect) if rect is not None else None
        gen_record["density"] = detail.get("density")
    record["parts"]["objects"] = {
        "instances": counts, "types": len(types), "triangles": int(tris), "budget": budget,
        "lodDistance": lod_distance if np.isfinite(lod_distance) else "coarsest",
        "fixed": int(sum(sum(len(x) for x in p.matrices) for p in rg.placed.values())),
        "generated": gen_record,
        "drawnAs": drawn_as,
        "withoutShape": {"types": len(missing), "instances": int(sum(missing.values())), "names": sorted(missing)[:200]},
        "leftOut": sorted(dropped),
        "seconds": {"generate": round(t_gen, 1), "total": round(time.time() - t0, 1)},
        "note": "fixed objects (RIGz pregen) and the land classes' generated ones, by their render meshes (a LOD "
                "chosen within the budget; decals and impostor billboards left out), coloured per material by "
                "the average of its diffuse texture (COLOR_0 holds sRGB-encoded values, as the 3DHeat viewer reads "
                "them); without a render mesh by their collision shape, trees by a crown glyph.",
    }
    log(f"  objects: {counts['buildings']} buildings, {counts['trees']} trees and plants, {tris:,} triangles "
        f"({sum(generated.values())} generated; drawn as {drawn_as}; {len(missing)} types without a shape"
        + (f", {len(dropped)} types left out to stay within {budget:,} triangles" if dropped else "") + ")")


def _add_sloping_water(geo, level, name: str, record: dict, cells: int = 512) -> None:
    """Rivers that are not at the level's water level (`WHM`): a sloping surface over every cell the water map covers."""
    from .dagorlevel import read_water_heightmap

    whm = read_water_heightmap(level.data, level.table["WHM"][0])
    x0, z0, x1, z1 = whm.extent()
    xs = np.linspace(x0, x1, cells + 1)
    zs = np.linspace(z0, z1, cells + 1)
    gx, gz = np.meshgrid(xs, zs)
    h = whm.sample(gx, gz)
    wet = np.isfinite(h)
    quad = wet[:-1, :-1] & wet[1:, :-1] & wet[:-1, 1:] & wet[1:, 1:]
    if not quad.any():
        return
    nc = cells + 1
    verts = np.stack([gx.ravel(), np.nan_to_num(h).ravel(), -gz.ravel()], 1).astype(np.float32)
    r, c = np.nonzero(quad)
    a = r * nc + c
    b, d, e = a + 1, a + nc, a + nc + 1
    faces = np.concatenate([np.stack([a, d, b], 1), np.stack([b, d, e], 1)]).astype(np.uint32)
    geo.add(f"water:{name} rivers", verts, faces, colour=(0.16, 0.30, 0.42))
    record["parts"]["slopingWater"] = {"cells": int(quad.sum()), "of": cells * cells,
                                       "height": [float(np.nanmin(h)), float(np.nanmax(h))],
                                       "x": [float(x0), float(x1)], "z": [float(z0), float(z1)]}
    record["notRead"] = [n for n in record["notRead"] if "WHM" not in n]


def _rect(blk: Blk, a: str, b: str) -> tuple[float, float, float, float] | None:
    p0, p1 = blk.get(a), blk.get(b)
    if not p0 or not p1:
        return None
    x0, z0 = p0
    x1, z1 = p1
    return (min(x0, x1), min(z0, z1), max(x0, x1), max(z0, z1))


def map_images(game: Game, name: str, blk: Blk | None) -> list[MapImage]:
    """The level's tactical maps that exist in the game's map pack, with the rectangles they cover."""
    pack = game.map_pack()
    if blk is None or pack is None:
        return []
    have = set(pack.names())
    out: list[MapImage] = []
    air_rect = _rect(blk, "mapCoord0", "mapCoord1")
    tank_rect = _rect(blk, "tankMapCoord0", "tankMapCoord1") or air_rect
    custom = (blk.get("customLevelMap") or "").split("*")[0]
    custom_tank = (blk.get("customLevelTankMap") or "").split("*")[0]
    for kind, candidates, rect in (
        ("map", [custom, f"{name}_map"], air_rect),
        ("tankmap", [custom_tank, f"{name}_tankmap"], tank_rect),
    ):
        for tex in candidates:
            if tex and tex in have and rect and not any(m.texture == tex for m in out):
                out.append(MapImage(kind, tex, rect))
                break
    return out


def _grid(hm: Heightmap, step: int, x_range: tuple[int, int], z_range: tuple[int, int]):
    """Vertices (output space) and faces of the heightmap sampled every `step` over a sample window."""
    h, w = hm.heights.shape
    cols = np.unique(np.clip(np.r_[np.arange(x_range[0], x_range[1], step), x_range[1]], 0, w - 1))
    rows = np.unique(np.clip(np.r_[np.arange(z_range[0], z_range[1], step), z_range[1]], 0, h - 1))
    xs = hm.origin_x + cols * hm.cell
    zs = hm.origin_z + rows * hm.cell
    gx, gz = np.meshgrid(xs, zs)
    y = hm.heights[np.ix_(rows, cols)]
    verts = np.stack([gx.ravel(), y.ravel(), -gz.ravel()], 1).astype(np.float32)
    nr, nc = len(rows), len(cols)
    r, c = np.meshgrid(np.arange(nr - 1), np.arange(nc - 1), indexing="ij")
    a = (r * nc + c).ravel()
    b, d, e = a + 1, a + nc, a + nc + 1
    # z is mirrored on output, so (a, b, d) - east, then north - winds counter-clockwise seen from above.
    faces = np.concatenate([np.stack([a, d, b], 1), np.stack([b, d, e], 1)]).astype(np.uint32)
    return verts, faces


def _cells_inside(verts: np.ndarray, faces: np.ndarray, rect) -> np.ndarray:
    """Which faces have their centroid inside a game-space rectangle."""
    c = verts[faces].mean(axis=1)
    x, z = c[:, 0], -c[:, 2]
    return (x >= rect[0]) & (x <= rect[2]) & (z >= rect[1]) & (z <= rect[3])


def _sample_window(hm: Heightmap, rect) -> tuple[tuple[int, int], tuple[int, int]] | None:
    h, w = hm.heights.shape
    c0 = int(np.floor((rect[0] - hm.origin_x) / hm.cell))
    c1 = int(np.ceil((rect[2] - hm.origin_x) / hm.cell))
    r0 = int(np.floor((rect[1] - hm.origin_z) / hm.cell))
    r1 = int(np.ceil((rect[3] - hm.origin_z) / hm.cell))
    c0, c1, r0, r1 = max(c0, 0), min(c1, w - 1), max(r0, 0), min(r1, h - 1)
    if c1 - c0 < 2 or r1 - r0 < 2:
        return None
    return (c0, c1), (r0, r1)


@dataclass
class Geometry:
    verts: list[np.ndarray] = field(default_factory=list)
    uvs: list[np.ndarray] = field(default_factory=list)
    parts: list[Part] = field(default_factory=list)
    colours: list = field(default_factory=list)
    count: int = 0

    def add(self, name: str, verts: np.ndarray, faces: np.ndarray, *, uv=None, texture=None, colour=None, extras=None,
            vcolours=None):
        """A part; `vcolours` gives each vertex its own linear colour (else `colour` for all of them)."""
        if not len(faces):
            return
        used, local = np.unique(faces, return_inverse=True)
        v = verts[used]
        self.verts.append(v)
        self.uvs.append(uv[used] if uv is not None else np.zeros((len(v), 2), np.float32))
        if vcolours is not None:
            self.colours.append(np.asarray(vcolours, np.float32)[used])
        else:
            self.colours.append(None if colour is None else np.tile(np.float32(colour), (len(v), 1)))
        self.parts.append(
            Part(name=name, faces=local.reshape(-1, 3).astype(np.uint32) + self.count,
                 texture=texture, colour=colour, extras=extras)
        )
        self.count += len(v)


def _uv(verts: np.ndarray, rect) -> np.ndarray:
    """Tactical-map coordinates: u east from x0, v down from the north edge (the image's top is north)."""
    u = (verts[:, 0] - rect[0]) / (rect[2] - rect[0])
    v = (rect[3] - (-verts[:, 2])) / (rect[3] - rect[1])
    return np.stack([u, v], 1).astype(np.float32)


def _add_textured(geo: Geometry, name: str, verts, faces, image: MapImage | None, colour):
    if image is None or image.image is None:
        geo.add(name, verts, faces, colour=colour)
        return
    inside = _cells_inside(verts, faces, image.rect)
    geo.add(name, verts, faces[inside], uv=_uv(verts, image.rect), texture=image.image,
            extras={"texture": image.texture})
    geo.add(f"{name} outside the map", verts, faces[~inside], colour=colour)


def _replace(tmp: Path, dest: Path, tries: int = 10) -> None:
    """Rename the finished file over the old one; on Windows a viewer or a scanner holding the old file open
    refuses that for a moment, so retry before giving up (and then leave no half-file behind)."""
    for i in range(tries):
        try:
            tmp.replace(dest)
            return
        except PermissionError:
            if i == tries - 1:
                tmp.unlink(missing_ok=True)
                raise
            time.sleep(3)


def _add_rings(geo: Geometry, hm: Heightmap, name: str, tank_rect, preset: dict, whole_step: int, image, air,
               colour, record: dict) -> None:
    """The heightmap in rings: its middle (the `core` share of the tank map) every `core_step` samples, the rest of
    the tank map every `ring_step`, the rest of the heightmap every `whole_step` (at least four ring steps). Each ring leaves out the cells of
    the one inside it, and each ring's window lies on its own step's lattice, so the samples of an outer ring are
    samples of the inner one too."""
    h, w = hm.heights.shape
    x0, z0, x1, z1 = tank_rect
    cx, cz, half = (x0 + x1) / 2, (z0 + z1) / 2, preset["core"] * max(x1 - x0, z1 - z0) / 2
    core_rect = (max(cx - half, x0), max(cz - half, z0), min(cx + half, x1), min(cz + half, z1))
    core_step, ring_step = preset["core_step"], max(preset["ring_step"], preset["core_step"])
    # A heightmap finer than the usual 2 m would cost four times the triangles at the same steps: coarser steps,
    # the rest of the tank map first, until the two rings fit the detail's ground budget.
    tw, th = (x1 - x0) / hm.cell, (z1 - z0) / hm.cell
    cw, ch = (core_rect[2] - core_rect[0]) / hm.cell, (core_rect[3] - core_rect[1]) / hm.cell

    def cost(cs: int, rs: int) -> float:
        return 2 * (cw * ch / cs ** 2 + max(tw * th - cw * ch, 0) / rs ** 2)

    while cost(core_step, ring_step) > preset.get("ground", float("inf")) and core_step < 64:
        if ring_step <= core_step:
            ring_step *= 2
        else:
            core_step *= 2
    surround = (hm.origin_x, hm.origin_z, hm.origin_x + (w - 1) * hm.cell, hm.origin_z + (h - 1) * hm.cell)
    rings = [(core_rect, core_step, f"ground:{name}", image),
             (tank_rect, ring_step, f"ground:{name} tank map", image),
             (surround, max(whole_step, 4 * ring_step), f"ground:{name} heightmap surroundings", air)]
    inner = None
    steps = []
    for rect, step, part, img in rings:
        win = _sample_window(hm, rect)
        if win is None:
            continue
        (c0, c1), (r0, r1) = win
        c0, r0 = c0 - c0 % step, r0 - r0 % step
        c1, r1 = min(c1 + (-c1) % step, w - 1), min(r1 + (-r1) % step, h - 1)
        gv, gf = _grid(hm, step, (c0, c1), (r0, r1))
        if inner is not None:
            gf = gf[~_cells_inside(gv, gf, inner)]
        here = (hm.origin_x + c0 * hm.cell, hm.origin_z + r0 * hm.cell, hm.origin_x + c1 * hm.cell, hm.origin_z + r1 * hm.cell)
        inner = here if inner is None else (min(inner[0], here[0]), min(inner[1], here[1]),
                                            max(inner[2], here[2]), max(inner[3], here[3]))
        if not len(gf):
            continue
        _add_textured(geo, part, gv, gf, img, colour)
        steps.append({"part": part, "step": step, "metres": step * hm.cell, "x": [here[0], here[2]],
                      "z": [here[1], here[3]], "triangles": int(len(gf))})
    record["parts"]["heightmap"] = {"samples": [w, h], "cell": hm.cell, "rings": steps}


def build(game: Game, level_path: Path, out_dir: Path, *, max_grid: int = DEFAULT_MAX_GRID,
          textures: bool = True, objects: bool = True, max_object_triangles: int | None = None,
          detail: str = DEFAULT_DETAIL, generate: bool = True, terrain: bool = True, log=print) -> dict:
    """Write `<out>/<level>.glb`, `.json` and the map PNGs. Returns the record written to the JSON.

    `detail` (low, medium, high) sets the ground's sampling over the tank map, the ground colour's resolution and
    the objects' triangle budget (`max_object_triangles` overrides it); `generate` adds the objects the land classes
    generate over the tank map; `terrain` colours the ground over the tank map from the land classes and roads
    instead of the tactical map."""
    t0 = time.time()
    preset = DETAIL[detail]
    budget = max_object_triangles if max_object_triangles is not None else preset["objects"]
    timings: dict[str, float] = {}
    name = level_path.stem
    out_dir.mkdir(parents=True, exist_ok=True)
    blk = game.level_blk(name)
    level = read_level(level_path)
    record: dict = {
        "format": "heat3d-wt-level",
        "tool": f"heat3d-wt-level {__version__}",
        "level": name,
        "coordinates": "metres; glb (x, y, z) = game (x east, y up, -z north): z mirrored, matching heat3d-wt-replay tables with their flipZ hint",
        "blocks": level.tags,
        "parts": {},
        "detail": detail,
        "notRead": ["the water heightmap (WHM) where a level has one"],
    }
    water_level = float(blk.get("water_level", 0.0)) if blk is not None else 0.0
    record["waterLevel"] = water_level
    record["levelBlk"] = blk is not None

    maps = map_images(game, name, blk)
    for m in maps:
        try:
            m.image = game.map_pack().image(m.texture)
            from PIL import Image

            png = out_dir / f"{name}_{m.kind}.png"
            Image.fromarray(m.image).save(png)
            log(f"  {m.kind} {m.texture}: {m.image.shape[1]}x{m.image.shape[0]} px over x {m.rect[0]:g}..{m.rect[2]:g}, z {m.rect[1]:g}..{m.rect[3]:g}")
        except Exception as e:  # a map image is a nicety; the level stands without it
            log(f"  {m.kind} {m.texture}: not read ({type(e).__name__}: {e})")
            m.image = None
    record["maps"] = [
        {
            "kind": m.kind, "texture": m.texture, "file": f"{name}_{m.kind}.png" if m.image is not None else None,
            "gameRect": {"x0": m.rect[0], "z0": m.rect[1], "x1": m.rect[2], "z1": m.rect[3]},
            # Corners in the glb's space (z mirrored): the image's top-left is north-west.
            "glbCorners": {"topLeft": [m.rect[0], -m.rect[3]], "topRight": [m.rect[2], -m.rect[3]],
                           "bottomLeft": [m.rect[0], -m.rect[1]], "bottomRight": [m.rect[2], -m.rect[1]]},
            "imageTopIs": "north (game z max)",
        }
        for m in maps
    ]
    air = next((m for m in maps if m.kind == "map" and m.image is not None), None) if textures else None
    tank = next((m for m in maps if m.kind == "tankmap" and m.image is not None), None) if textures else None
    tank_rect = _rect(blk, "tankMapCoord0", "tankMapCoord1") if blk is not None else None
    timings["maps"] = round(time.time() - t0, 1)
    ground_image = tank or air
    # Without a tank map (air maps) the ground colour covers the air map's area, clipped to the heightmap (or the
    # land mesh where there is none), at the coarser resolution the 4096-pixel cap gives (about 32 m over 131 km).
    colour_rect = tank_rect
    if colour_rect is None and air is not None and (level.heightmap is not None or level.landmesh is not None):
        if level.heightmap is not None:
            hm0 = level.heightmap
            hh, hw = hm0.heights.shape
            ext = (hm0.origin_x, hm0.origin_z, hm0.origin_x + (hw - 1) * hm0.cell, hm0.origin_z + (hh - 1) * hm0.cell)
        else:
            lv0 = level.landmesh.vertices
            ext = (float(lv0[:, 0].min()), float(lv0[:, 2].min()), float(lv0[:, 0].max()), float(lv0[:, 2].max()))
        r = (max(air.rect[0], ext[0]), max(air.rect[1], ext[1]), min(air.rect[2], ext[2]), min(air.rect[3], ext[3]))
        colour_rect = r if r[2] > r[0] and r[3] > r[1] else None
    if textures and terrain and colour_rect is not None and "lmap" in level.table:
        t1 = time.time()
        try:
            from .terrain import terrain_colour

            img, info = terrain_colour(game, level.data, level.table, colour_rect, metres_per_pixel=preset["terrain_mpp"],
                                       heightmap=level.heightmap, textures=game.textures(), log=None)
            ground_image = MapImage("terrain", "land classes, ground decals and roads", colour_rect, img)
            from PIL import Image

            Image.fromarray(img).save(out_dir / f"{name}_terrain.png")
            info["file"] = f"{name}_terrain.png"
            record["parts"]["terrainColour"] = info
            where = "the tank map" if tank_rect is not None else "the air map"
            log(f"  terrain colour: {img.shape[1]}x{img.shape[0]} px over {where} ({time.time() - t1:.1f} s)")
        except Exception as e:  # the tactical map stands in
            record["parts"]["terrainColour"] = {"error": f"{type(e).__name__}: {e}"}
            log(f"  terrain colour: not made ({type(e).__name__}: {e}); the tactical map is used")
        timings["terrainColour"] = round(time.time() - t1, 1)

    geo = Geometry()
    ground_colour = (0.42, 0.40, 0.36)
    extents: list[tuple[float, float, float, float]] = []
    hm = level.heightmap
    if hm is not None:
        h, w = hm.heights.shape
        x0, z0 = hm.origin_x, hm.origin_z
        x1, z1 = x0 + (w - 1) * hm.cell, z0 + (h - 1) * hm.cell
        extents.append((x0, z0, x1, z1))
        detail_map = (tank or air)
        fine_rect = None
        if detail_map is not None:
            fine_rect = detail_map.rect
        elif blk is not None:
            fine_rect = tank_rect
        window = _sample_window(hm, fine_rect) if fine_rect else None
        if tank_rect is None and max_grid == DEFAULT_MAX_GRID:
            max_grid = preset["whole_grid"]
        whole_step = max(1, int(np.ceil(max(w, h) / max_grid)))
        if tank_rect is not None and _sample_window(hm, tank_rect):
            _add_rings(geo, hm, name, tank_rect, preset, whole_step, ground_image, air, ground_colour, record)
        elif window and (window[0][1] - window[0][0] < w - 1 or window[1][1] - window[1][0] < h - 1):
            fine_step = max(1, int(np.ceil(max(window[0][1] - window[0][0], window[1][1] - window[1][0]) / max_grid)))
            fv, ff = _grid(hm, fine_step, window[0], window[1])
            _add_textured(geo, f"ground:{name}", fv, ff, ground_image, ground_colour)
            cv, cf = _grid(hm, whole_step, (0, w - 1), (0, h - 1))
            keep = ~_cells_inside(cv, cf, (x0 + window[0][0] * hm.cell, z0 + window[1][0] * hm.cell,
                                           x0 + window[0][1] * hm.cell, z0 + window[1][1] * hm.cell))
            _add_textured(geo, f"ground:{name} heightmap surroundings", cv, cf[keep], air, ground_colour)
            record["parts"]["heightmap"] = {"samples": [w, h], "cell": hm.cell, "detailStep": fine_step,
                                            "surroundingsStep": whole_step}
        else:
            gv, gf = _grid(hm, whole_step, (0, w - 1), (0, h - 1))
            _add_textured(geo, f"ground:{name}", gv, gf, ground_image, ground_colour)
            record["parts"]["heightmap"] = {"samples": [w, h], "cell": hm.cell, "step": whole_step}
        record["parts"]["heightmap"].update(
            x=[x0, x1], z=[z0, z1], height=[float(hm.heights.min()), float(hm.heights.max())], version=hm.version)

    lm = level.landmesh
    if lm is not None:
        v = lm.vertices.copy()
        v[:, 2] = -v[:, 2]
        f = lm.faces
        if hm is not None:
            hx0, hz0, hx1, hz1 = extents[0]
            c = lm.vertices[f].mean(axis=1)
            inside = (c[:, 0] > hx0) & (c[:, 0] < hx1) & (c[:, 2] > hz0) & (c[:, 2] < hz1)
            f = f[~inside]
        # Mirroring z turns the winding; put it back so faces point up.
        f = f[:, [0, 2, 1]]
        if len(f):
            n = np.cross(v[f[:, 1]] - v[f[:, 0]], v[f[:, 2]] - v[f[:, 0]])
            if n[:, 1].sum() < 0:
                f = f[:, [0, 2, 1]]
        part = f"ground:{name}" if hm is None else f"ground:{name} land mesh"
        _add_textured(geo, part, v, f, ground_image if hm is None else air, ground_colour)
        mn, mx = lm.vertices.min(0), lm.vertices.max(0)
        extents.append((float(mn[0]), float(mn[2]), float(mx[0]), float(mx[2])))
        record["parts"]["landMesh"] = {"triangles": int(len(f)), "of": int(len(lm.faces)),
                                       "x": [float(mn[0]), float(mx[0])], "z": [float(mn[2]), float(mx[2])],
                                       "height": [float(mn[1]), float(mx[1])]}
    timings["ground"] = round(time.time() - t0 - sum(timings.values()), 1)
    if objects and geo.parts:
        t1 = time.time()
        _add_objects(geo, game, level, name, record, log, budget, preset, generate and tank_rect is not None,
                     rect=tank_rect)
        timings["objects"] = round(time.time() - t1, 1)
    if not geo.parts:
        raise ValueError(f"{name}: no heightmap and no land mesh")

    lowest = min(float(p.min()) for p in (([hm.heights] if hm is not None else []) + ([lm.vertices[:, 1]] if lm is not None else [])))
    if lowest < water_level:
        ex = np.array(extents)
        wx0, wz0 = ex[:, 0].min(), ex[:, 1].min()
        wx1, wz1 = ex[:, 2].max(), ex[:, 3].max()
        wv = np.array([[wx0, water_level, -wz0], [wx1, water_level, -wz0],
                       [wx1, water_level, -wz1], [wx0, water_level, -wz1]], np.float32)
        geo.add(f"water:{name}", wv, np.array([[0, 2, 1], [0, 3, 2]], np.uint32), colour=(0.16, 0.30, 0.42))
        record["parts"]["water"] = {"level": water_level, "x": [float(wx0), float(wx1)], "z": [float(wz0), float(wz1)]}
    if level.table and "WHM" in level.table:
        _add_sloping_water(geo, level, name, record)

    t1 = time.time()
    positions = np.concatenate(geo.verts)
    uvs = np.concatenate(geo.uvs) if any(p.texture is not None for p in geo.parts) else None
    colours = None
    if any(c is not None for c in geo.colours):
        colours = np.concatenate([c if c is not None else np.full((len(v), 3), 0.5, np.float32)
                                  for c, v in zip(geo.colours, geo.verts)])
    glb_path = out_dir / f"{name}.glb"
    tmp = glb_path.with_suffix(".glb.part")
    write_glb(tmp, positions, parts=geo.parts, uvs=uvs, colours=colours)
    _replace(tmp, glb_path)
    timings["write"] = round(time.time() - t1, 1)
    record["triangles"] = {p.name: int(len(p.faces)) for p in geo.parts}
    record["trianglesTotal"] = int(sum(record["triangles"].values()))
    record["glbBytes"] = glb_path.stat().st_size
    record["secondsBy"] = timings
    record["seconds"] = round(time.time() - t0, 1)
    (out_dir / f"{name}.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    return record


def describe(game: Game, level_path: Path) -> dict:
    """One line's worth for `list`: kind, what terrain the level has, its maps."""
    s = summary(level_path)
    blk = None
    try:
        blk = game.level_blk(level_path.stem)
    except Exception:
        pass
    s["maps"] = [m.texture for m in map_images(game, level_path.stem, blk)] if blk is not None else []
    return s
