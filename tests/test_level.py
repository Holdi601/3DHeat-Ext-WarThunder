"""The level reader on built files: archive, BLK, level binary, texture pack, and the whole glb."""

from __future__ import annotations

import json
import struct

import numpy as np
import pytest

import levelsynth
from heat3d_ext_warthunder import dagorlevel
from heat3d_ext_warthunder.dxp import TexturePack
from heat3d_ext_warthunder.level import Game, build
from heat3d_ext_warthunder.vromfs import Vromfs, read_vromfs_bytes


def test_vromfs_round_trip():
    files = {"levels/a.blk": b"hello", "gamedata/x.bin": bytes(range(200)), "empty": b""}
    assert read_vromfs_bytes(levelsynth.vromfs(files)) == files


def test_blk_types_and_nesting():
    tree = ("", [("water_level", 4.5), ("customLevelMap", "a_tankmap*"), ("n", 7), ("on", True),
                 ("mapCoord0", [0.0, -10.0]), ("p3", [1.0, 2.0, 3.0])],
            [("stars", [("year", 1944)], [("inner", [("deep", "yes")], [])]), ("empty", [], [])])
    v = Vromfs(files={"levels/a.blk": levelsynth.blk(tree)})
    b = v.blk("levels/a.blk")
    assert b.get("water_level") == pytest.approx(4.5)
    assert b.get("customLevelMap") == "a_tankmap*"
    assert b.get("n") == 7 and b.get("on") is True
    assert b.get("mapCoord0") == [0.0, -10.0]
    assert b.get("p3") == [1.0, 2.0, 3.0]
    assert b.block("stars").get("year") == 1944
    assert b.block("stars").block("inner").get("deep") == "yes"
    assert b.block("empty") is not None and not b.block("empty").params


def _units(h: int = 32, w: int = 32) -> np.ndarray:
    y, x = np.mgrid[0:h, 0:w]
    return (1000 + 300 * x + 50 * y + 2000 * (np.sin(x / 3.0) > 0)).astype(np.uint16)


def test_heightmap_v2_decodes_to_the_quantised_heights():
    units = _units()
    data = levelsynth.level(levelsynth.heightmap_block(units, 2.0, -10.0, 655.35, 100.0, 200.0))
    bl = dagorlevel.blocks(data)
    hm = dagorlevel.read_heightmap(data, bl["HM2"][0])
    assert hm.heights.shape == units.shape
    assert (hm.cell, hm.origin_x, hm.origin_z) == (2.0, 100.0, 200.0)
    # 8-bit values within a block's range: at most delta/255/2 units off, plus rounding.
    expected = -10.0 + units * (655.35 / 65535.0)
    k = 8
    worst = max(int(np.ptp(units[r:r + k, c:c + k])) for r in range(0, 32, k) for c in range(0, 32, k))
    assert np.abs(hm.heights - expected).max() <= (worst / 255.0 + 1) * 0.01 + 1e-4


def test_land_tracer_triangles():
    verts = np.array([[0, 5, 0], [100, 5, 0], [100, 9, 100], [0, 9, 100]], np.float64)
    faces = np.array([[0, 1, 2], [0, 2, 3]])
    data = levelsynth.level(levelsynth.landmesh_block(verts, faces))
    lm = dagorlevel.read_landmesh(data, dagorlevel.blocks(data)["lmap"][0])
    assert lm is not None and lm.faces.tolist() == faces.tolist()
    assert np.allclose(lm.vertices, verts, atol=0.01)


def test_texture_pack_rgb(tmp_path):
    rgb = np.random.default_rng(1).integers(0, 255, (8, 16, 3), dtype=np.uint8)
    path = tmp_path / "maps.dxp.bin"
    path.write_bytes(levelsynth.texture_pack("lvl_tankmap", rgb))
    p = TexturePack(path)
    assert p.names() == ["lvl_tankmap"]
    assert np.array_equal(p.image("lvl_tankmap"), rgb)


def _game(tmp_path, level_bytes: bytes, blk_tree=None, map_rgb=None) -> Game:
    root = tmp_path / "War Thunder"
    (root / "levels").mkdir(parents=True)
    (root / "levels" / "lvl.bin").write_bytes(level_bytes)
    files = {"levels/lvl.blk": levelsynth.blk(blk_tree)} if blk_tree else {}
    (root / "aces.vromfs.bin").write_bytes(levelsynth.vromfs(files))
    if map_rgb is not None:
        res = root / "content" / "base" / "res"
        res.mkdir(parents=True)
        (res / "locations_maps.dxp.bin").write_bytes(levelsynth.texture_pack("lvl_tankmap", map_rgb))
    return Game(root)


def _glb_nodes(path):
    raw = path.read_bytes()
    (n,) = struct.unpack_from("<I", raw, 12)
    doc = json.loads(raw[20:20 + n])
    return doc, [node["name"] for node in doc["nodes"]]


def test_build_heightmap_level_with_map_and_water(tmp_path):
    units = _units()
    level = levelsynth.level(
        levelsynth.heightmap_block(units, 2.0, -10.0, 655.35, 0.0, 0.0),
        levelsynth.landmesh_block(np.array([[-200, -20, -200], [400, -20, -200], [400, -20, 400], [-200, -20, 400]], float),
                                  np.array([[0, 1, 2], [0, 2, 3]])),
    )
    tree = ("", [("water_level", 2.0), ("tankMapCoord0", [0.0, 0.0]), ("tankMapCoord1", [62.0, 62.0])], [])
    game = _game(tmp_path, level, tree, map_rgb=np.full((4, 4, 3), 90, np.uint8))
    rec = build(game, game.levels()[0], tmp_path / "out", log=lambda s: None)
    doc, names = _glb_nodes(tmp_path / "out" / "lvl.glb")
    assert "ground:lvl" in names and "water:lvl" in names
    assert any(n.startswith("ground:lvl land mesh") for n in names)
    assert rec["waterLevel"] == 2.0 and rec["maps"][0]["kind"] == "tankmap"
    assert (tmp_path / "out" / "lvl_tankmap.png").exists()
    # z is mirrored: the heightmap's z 0..62 lands at glb z 0..-62.
    # The tank map is drawn in rings (its middle finer); together they cover it.
    accs = [doc["accessors"][m["primitives"][0]["attributes"]["POSITION"]] for m in doc["meshes"]
            if m["name"] in ("ground:lvl", "ground:lvl tank map")]
    assert len(accs) == 2
    assert min(a["min"][2] for a in accs) == pytest.approx(-62.0) and max(a["max"][2] for a in accs) == pytest.approx(0.0)
    assert [r["part"] for r in rec["parts"]["heightmap"]["rings"]][:2] == ["ground:lvl", "ground:lvl tank map"]
    # The land mesh's two triangles lie partly outside the heightmap, so they are kept.
    assert rec["parts"]["landMesh"]["triangles"] == 2
    assert not list((tmp_path / "out").glob("*.part"))


def test_build_without_terrain_fails_cleanly(tmp_path):
    game = _game(tmp_path, levelsynth.level())
    with pytest.raises(ValueError, match="no heightmap and no land mesh"):
        build(game, game.levels()[0], tmp_path / "out", log=lambda s: None)
    assert not (tmp_path / "out" / "lvl.glb").exists()


def test_not_a_level():
    with pytest.raises(dagorlevel.LevelError):
        dagorlevel.blocks(b"NOPE" + b"\0" * 20)


def _rot_y(deg: float, scale: float = 1.0) -> np.ndarray:
    a = np.radians(deg)
    return scale * np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])


@pytest.mark.parametrize("wide", [False, True])
def test_rigen_instances(wide):
    from heat3d_ext_warthunder import rigen

    m = np.c_[_rot_y(30, 1.5), [100.0, 20.0, 300.0]]
    block = levelsynth.rigen_block(1024.0, [("house_a", 0, [m, np.c_[np.eye(3), [10.0, 5.0, 10.0]]]),
                                           ("tree_a", 1, [(500.0, 7.0, 600.0, 2.0)])], world0=(0.0, 0.0),
                                   ht=(0, 1000), wide=wide)
    data = levelsynth.level(block)
    rg = rigen.read_rigen(data, dagorlevel.blocks(data)["RIGz"][0])
    assert rg.counts == {"house_a": 2, "tree_a": 1}
    got = np.concatenate(rg.placed["house_a"].matrices)
    assert np.allclose(got[0], m, atol=0.06 if not wide else 0.05)
    tree = np.concatenate(rg.placed["tree_a"].matrices)[0]
    assert np.allclose(tree[:, 3], [500, 7, 600], atol=0.1) and tree[0, 0] == pytest.approx(2.0)


def test_collision_shapes(tmp_path):
    from heat3d_ext_warthunder import collision

    quad = np.array([[0, 0, 0], [4, 0, 0], [0, 3, 0], [4, 3, 0]], np.float64)
    # A box node whose matrix swaps y and z (as resources exported z-up have them).
    swap = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0], [5, 0, 0]], np.float32)
    box_only = collision.read_collision(levelsynth.collision_resource([(((-1, -2, 0), (1, 2, 6)), swap)], None))
    assert len(box_only.faces) == 12
    assert np.allclose(box_only.verts.min(0), [4, 0, -2]) and np.allclose(box_only.verts.max(0), [6, 6, 2])
    # Beside a mesh, a box is a coarse stand-in and is left out: drawn, it is a cube around the object.
    blob = levelsynth.collision_resource([(((-1, -2, 0), (1, 2, 6)), swap)], quad)
    shape = collision.read_collision(blob)
    assert np.allclose(shape.verts, quad, atol=1e-3)
    assert sorted(map(tuple, shape.faces)) == [(0, 1, 2), (1, 2, 3)]
    res = tmp_path / "res"
    res.mkdir()
    (res / "pack.grp").write_bytes(levelsynth.grp_pack({"hut": (collision.RENDINST_CLASS, b"x"),
                                                        "hut_collision": (collision.COLLISION_CLASS, blob)}))
    idx = collision.ResourceIndex(res)
    assert collision.load_shape(idx, "hut").faces.shape == (2, 3)
    assert collision.load_shape(idx, "nothing") is None


def test_collision_keeps_only_what_rays_hit():
    from heat3d_ext_warthunder import collision

    quad = np.array([[0, 0, 0], [4, 0, 0], [0, 3, 0], [4, 3, 0]], np.float64)
    eye = np.r_[np.eye(3), [[0, 0, 0]]]
    # A traceable box and a physics-only mesh: the box is what the game traces against, so it stays.
    blob = levelsynth.collision_resource([(((0, 0, 0), (1, 1, 1)), eye)], quad, box_flags=collision.TRACEABLE)
    assert len(collision.read_collision(blob).faces) == 12


def test_collision_skips_empty_boxes():
    from heat3d_ext_warthunder import collision

    # A node box stored as "empty" (+-1e32) is dropped; with nothing else the object has no shape (no
    # stand-in cube from the resource's own box).
    blob = levelsynth.collision_resource([(((-1e32, -1e32, -1e32), (1e32, 1e32, 1e32)), np.r_[np.eye(3), [[0, 0, 0]]])], None)
    with pytest.raises(collision.CollisionError):
        collision.read_collision(blob)


def test_water_heightmap():
    page = np.full((130, 130), 1000, np.uint16)
    page[:, 65:] = 3000
    data = levelsynth.level(levelsynth.water_heightmap_block(page, 2000.0, -1.0, 65.535))
    whm = dagorlevel.read_water_heightmap(data, dagorlevel.blocks(data)["WHM"][0])
    assert whm.extent() == pytest.approx((-1000.0, -1000.0, 1000.0, 1000.0), abs=0.01)
    h = whm.sample(np.array([-900.0, -100.0, 500.0]), np.array([-500.0, -500.0, -500.0]))
    assert h[0] == pytest.approx(1000 * 65.535 / 65535 - 1, abs=0.01)
    assert h[1] == pytest.approx(3000 * 65.535 / 65535 - 1, abs=0.01)
    assert np.isnan(h[2])  # a flat cell: the level's own water level applies


def test_build_places_objects(tmp_path):
    from heat3d_ext_warthunder import collision

    units = _units()
    m = np.c_[np.eye(3), [20.0, 0.0, 20.0]]
    level = levelsynth.level(levelsynth.heightmap_block(units, 2.0, -10.0, 655.35, 0.0, 0.0),
                             levelsynth.rigen_block(64.0, [("hut", 0, [m]), ("oak_tree", 1, [(40.0, 0.0, 40.0, 1.0)])]))
    game = _game(tmp_path, level, ("", [("water_level", -50.0)], []))
    res = game.root / "content" / "base" / "res"
    res.mkdir(parents=True)
    blob = levelsynth.collision_resource([(((-2, 0, -2), (2, 3, 2)), np.r_[np.eye(3), [[0, 0, 0]]])], None)
    (res / "a.grp").write_bytes(levelsynth.grp_pack({"hut_collision": (collision.COLLISION_CLASS, blob),
                                                     "oak_tree_collision": (collision.COLLISION_CLASS, blob)}))
    rec = build(game, game.levels()[0], tmp_path / "out", log=lambda s: None)
    doc, names = _glb_nodes(tmp_path / "out" / "lvl.glb")
    assert "structure:lvl buildings" in names and "structure:lvl trees" in names
    assert rec["parts"]["objects"]["instances"] == {"buildings": 1, "trees": 1}
    hut = next(mm for mm in doc["meshes"] if mm["name"] == "structure:lvl buildings")
    acc = doc["accessors"][hut["primitives"][0]["attributes"]["POSITION"]]
    # The hut at game (20, 0, 20): glb z mirrored.
    assert acc["min"] == pytest.approx([18, 0, -22], abs=0.05) and acc["max"] == pytest.approx([22, 3, -18], abs=0.05)
