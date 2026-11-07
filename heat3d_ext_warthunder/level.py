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


#: Objects drawn as a tree glyph rather than by their collision shape (a trunk, for most trees).
VEGETATION = re.compile(
    r"tree|bush|oak|aspen|pine|palm|(?<![a-z])fir|birch|poplar|populus|tilia|cypress|spruce|willow|maple|beech|"
    r"acacia|baobab|shrub|flower|grass|reed|typha|cane|plant|vine|ivy|hedge(?!hog)|forest|jungle|cactus|bamboo"
)


def _tree_glyph(box) -> tuple[np.ndarray, np.ndarray]:
    """A double cone over the object's box: the crown of a tree whose collision is only its trunk."""
    (x0, y0, z0), (x1, y1, z1) = box
    h = max(y1 - y0, 0.5)
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    r = max(h * 0.22, (x1 - x0) / 2, (z1 - z0) / 2)
    mid = y0 + h * 0.55
    ring = [(cx + r * np.cos(a), mid, cz + r * np.sin(a)) for a in np.linspace(0, 2 * np.pi, 5)[:-1]]
    v = np.array([(cx, y0, cz), (cx, y0 + h, cz)] + ring, np.float32)
    f = []
    for i in range(4):
        a, b = 2 + i, 2 + (i + 1) % 4
        f += [(1, b, a), (0, a, b)]
    return v, np.array(f, np.int64)


DEFAULT_MAX_OBJECT_TRIANGLES = 4_000_000


def _box_shape(box) -> tuple[np.ndarray, np.ndarray]:
    from .collision import _box

    return _box(*box)


def _add_objects(geo, game: "Game", data_level, name: str, record: dict, log,
                 budget: int = DEFAULT_MAX_OBJECT_TRIANGLES) -> None:
    """The level's fixed objects (RIGz) as structure parts: buildings by their collision shapes, trees as glyphs.

    Within `budget` triangles: over it, the object types costing most are drawn as their boxes, and if that
    is not enough, the smallest objects (by box volume) are left out; the JSON lists both.
    """
    from .rigen import read_rigen

    data, bl = data_level
    if "RIGz" not in bl:
        return
    rg = read_rigen(data, bl["RIGz"][0])
    missing: dict[str, int] = {}
    plan = []  # [name, tree, matrices, verts, faces, box, volume]
    for obj, placed in rg.placed.items():
        shape = game.shape(obj)
        if shape is None:
            missing[obj] = rg.counts.get(obj, 0)
            continue
        tree = bool(VEGETATION.search(obj.lower()))
        sv, sf = _tree_glyph(shape.box) if tree else (shape.verts, shape.faces)
        m = np.concatenate(placed.matrices)
        lo, hi = sv.min(0), sv.max(0)  # the drawn shape's box (a tree's crown, not its trunk)
        (x0, y0, z0), (x1, y1, z1) = lo, hi
        scale = float(np.abs(np.linalg.det(m[0, :, :3]))) if len(m) else 1.0
        plan.append([obj, tree, m, sv, sf, shape.box, max((x1 - x0) * (y1 - y0) * (z1 - z0), 0.0) * scale])
    total = sum(len(p[2]) * len(p[4]) for p in plan)
    boxed, dropped = [], []
    if total > budget:
        for p in sorted(plan, key=lambda p: -len(p[2]) * (len(p[4]) - 12)):
            if total <= budget:
                break
            if len(p[4]) > 12:
                total -= len(p[2]) * (len(p[4]) - 12)
                p[3], p[4] = _box_shape(p[5])
                boxed.append(p[0])
    if total > budget:
        for p in sorted(plan, key=lambda p: p[6]):
            if total <= budget:
                break
            total -= len(p[2]) * len(p[4])
            dropped.append(p[0])
        plan = [p for p in plan if p[0] not in set(dropped)]
    groups = {"buildings": ([], []), "trees": ([], [])}
    counts = {"buildings": 0, "trees": 0}
    for obj, tree, m, sv, sf, _box, _vol in plan:
        w = np.einsum("nij,vj->nvi", m[:, :, :3], sv) + m[:, None, :, 3]
        w[:, :, 2] *= -1  # glb z = -game z
        key = "trees" if tree else "buildings"
        vl, fl = groups[key]
        start = sum(len(x) for x in vl)
        vl.append(w.reshape(-1, 3).astype(np.float32))
        offs = (np.arange(len(m)) * len(sv))[:, None, None]
        fl.append((sf[None, :, [0, 2, 1]] + offs).reshape(-1, 3) + start)  # mirrored: winding swapped
        counts[key] += len(m)
    for key, (vl, fl) in groups.items():
        if vl:
            v = np.concatenate(vl)
            f = np.concatenate(fl).astype(np.uint32)
            geo.add(f"structure:{name} {key}", v, f, colour=(0.62, 0.56, 0.48) if key == "buildings" else (0.30, 0.45, 0.28))
    record["parts"]["objects"] = {
        "instances": counts, "types": len(rg.placed),
        "withoutShape": {"types": len(missing), "instances": int(sum(missing.values()))},
        "budget": budget, "drawnAsBoxes": sorted(boxed), "leftOut": sorted(dropped),
        "landClassesNotGenerated": rg.land_classes,
        "note": "the level's fixed objects (RIGz pregen) by their collision shapes; trees as a crown glyph over their "
                "collision box. Objects the land classes generate at run time (most forests and fields of air maps) "
                "are not placed.",
    }
    log(f"  objects: {counts['buildings']} buildings, {counts['trees']} trees ({len(missing)} types without a shape"
        + (f", {len(boxed)} types as boxes, {len(dropped)} left out to stay within {budget:,} triangles" if boxed or dropped else "")
        + ")")


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
    count: int = 0

    def add(self, name: str, verts: np.ndarray, faces: np.ndarray, *, uv=None, texture=None, colour=None, extras=None):
        if not len(faces):
            return
        used, local = np.unique(faces, return_inverse=True)
        v = verts[used]
        self.verts.append(v)
        self.uvs.append(uv[used] if uv is not None else np.zeros((len(v), 2), np.float32))
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


def build(game: Game, level_path: Path, out_dir: Path, *, max_grid: int = DEFAULT_MAX_GRID,
          textures: bool = True, objects: bool = True, max_object_triangles: int = DEFAULT_MAX_OBJECT_TRIANGLES,
          log=print) -> dict:
    """Write `<out>/<level>.glb`, `.json` and the map PNGs. Returns the record written to the JSON."""
    t0 = time.time()
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
        "notRead": ["objects the land classes generate at run time (most forests and fields of air maps)", "the water heightmap (WHM) where a level has one"],
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

    geo = Geometry()
    ground_colour = (0.42, 0.40, 0.36)
    extents: list[tuple[float, float, float, float]] = []
    hm = level.heightmap
    if hm is not None:
        h, w = hm.heights.shape
        x0, z0 = hm.origin_x, hm.origin_z
        x1, z1 = x0 + (w - 1) * hm.cell, z0 + (h - 1) * hm.cell
        extents.append((x0, z0, x1, z1))
        detail = (tank or air)
        fine_rect = None
        if detail is not None:
            fine_rect = detail.rect
        elif blk is not None:
            fine_rect = _rect(blk, "tankMapCoord0", "tankMapCoord1")
        window = _sample_window(hm, fine_rect) if fine_rect else None
        whole_step = max(1, int(np.ceil(max(w, h) / max_grid)))
        if window and (window[0][1] - window[0][0] < w - 1 or window[1][1] - window[1][0] < h - 1):
            fine_step = max(1, int(np.ceil(max(window[0][1] - window[0][0], window[1][1] - window[1][0]) / max_grid)))
            fv, ff = _grid(hm, fine_step, window[0], window[1])
            _add_textured(geo, f"ground:{name}", fv, ff, tank or air, ground_colour)
            cv, cf = _grid(hm, whole_step, (0, w - 1), (0, h - 1))
            keep = ~_cells_inside(cv, cf, (x0 + window[0][0] * hm.cell, z0 + window[1][0] * hm.cell,
                                           x0 + window[0][1] * hm.cell, z0 + window[1][1] * hm.cell))
            _add_textured(geo, f"ground:{name} heightmap surroundings", cv, cf[keep], air, ground_colour)
            record["parts"]["heightmap"] = {"samples": [w, h], "cell": hm.cell, "detailStep": fine_step,
                                            "surroundingsStep": whole_step}
        else:
            gv, gf = _grid(hm, whole_step, (0, w - 1), (0, h - 1))
            _add_textured(geo, f"ground:{name}", gv, gf, tank or air, ground_colour)
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
        _add_textured(geo, part, v, f, air, ground_colour)
        mn, mx = lm.vertices.min(0), lm.vertices.max(0)
        extents.append((float(mn[0]), float(mn[2]), float(mx[0]), float(mx[2])))
        record["parts"]["landMesh"] = {"triangles": int(len(f)), "of": int(len(lm.faces)),
                                       "x": [float(mn[0]), float(mx[0])], "z": [float(mn[2]), float(mx[2])],
                                       "height": [float(mn[1]), float(mx[1])]}
    if objects and geo.parts:
        _add_objects(geo, game, (level.data, level.table), name, record, log, max_object_triangles)
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

    positions = np.concatenate(geo.verts)
    uvs = np.concatenate(geo.uvs) if any(p.texture is not None for p in geo.parts) else None
    glb_path = out_dir / f"{name}.glb"
    tmp = glb_path.with_suffix(".glb.part")
    write_glb(tmp, positions, parts=geo.parts, uvs=uvs)
    tmp.replace(glb_path)
    record["triangles"] = {p.name: int(len(p.faces)) for p in geo.parts}
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
