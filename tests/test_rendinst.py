"""Render instances (LOD meshes, materials, colours) and how the level chooses their LODs, on built data."""

from __future__ import annotations

import json
import struct

import numpy as np
import pytest

import levelsynth
from heat3d_ext_warthunder import collision, level as lv
from heat3d_ext_warthunder.rendinst import (
    RENDINST_CLASS, Descriptions, RenderIndex, decode_index_sequence, read_resource,
)

_CUBE_V = np.array([[-1, 0, -1], [1, 0, -1], [1, 0, 1], [-1, 0, 1], [-1, 2, -1], [1, 2, -1], [1, 2, 1], [-1, 2, 1]], float)
_CUBE_F = np.array([[0, 2, 1], [0, 3, 2], [4, 5, 6], [4, 6, 7], [0, 1, 5], [0, 5, 4],
                    [1, 2, 6], [1, 6, 5], [2, 3, 7], [2, 7, 6], [3, 0, 4], [3, 4, 7]])
_ROOF_V = np.array([[-1, 2, -1], [1, 2, -1], [0, 3, 0]], float)


def _hut(packed=True) -> bytes:
    """Two LODs: the walls and a roof (two materials) out to 80 m, then the walls alone."""
    return levelsynth.rendinst_resource(
        [(80.0, [(_CUBE_V, _CUBE_F, 0), (_ROOF_V, np.array([[0, 1, 2]]), 1)]), (400.0, [(_CUBE_V, _CUBE_F, 0)])],
        packed=packed, box=((-1.0, 0.0, -1.0), (1.0, 3.0, 1.0)))


def _ri_desc() -> bytes:
    mats = [("mat", [("cls", "rendinst_simple"), ("t0", 0), ("t2", 1)], []),
            ("mat", [("cls", "rendinst_decal"), ("t0", 0)], [])]
    hut = ("hut", [("lods", 2)], [("tex", [("tex", "hut_d*"), ("tex", "hut_n*")], []), ("mat", [], mats)])
    return levelsynth.blk(("", [], [hut]))


def test_index_sequence_both_baselines():
    idx = [0, 1, 2, 2, 1, 3, 70000, 5, 4]
    assert decode_index_sequence(levelsynth.pack_index_sequence(idx), len(idx)).tolist() == idx
    # Two baselines: 5 against baseline 0 (from 0), then 7 against baseline 1 (from 0), then 6 against baseline 0.
    vals = [(5 << 2) | 0, (7 << 2) | 1, (1 << 2) | 0]
    buf = bytes([0xD1] + vals + [0, 0, 0, 0])
    assert decode_index_sequence(buf, 3).tolist() == [5, 7, 6]
    with pytest.raises(ValueError):
        decode_index_sequence(b"\x00" * 10, 3)


@pytest.mark.parametrize("packed", [True, False])
def test_resource_lods_and_elements(packed):
    res = read_resource(_hut(packed), "hut")
    assert [round(l.range) for l in res.lods] == [80, 400]
    assert res.box == ((-1.0, 0.0, -1.0), (1.0, 3.0, 1.0))
    v, f, m = res.lod_mesh(0)
    assert len(f) == 13 and sorted(set(m.tolist())) == [0, 1]
    assert v.max(0).tolist() == [1.0, 3.0, 1.0]  # the roof's apex
    # Every triangle keeps its corners (no index past its vertices, same geometry as built).
    assert np.allclose(np.sort(v[f[:12]].reshape(-1, 3), axis=0), np.sort(_CUBE_V[_CUBE_F].reshape(-1, 3), axis=0))
    v1, f1, _ = res.lod_mesh(1)
    assert len(f1) == 12 and res.faces(1) == 12
    v2, f2, m2 = res.lod_mesh(0, skip=lambda mat, trans: mat == 1)
    assert len(f2) == 12 and set(m2.tolist()) == {0}


def test_render_index_materials_and_look(tmp_path):
    res_dir = tmp_path / "res"
    res_dir.mkdir()
    (res_dir / "a.grp").write_bytes(levelsynth.grp_pack({"hut": (RENDINST_CLASS, _hut())}))
    (res_dir / "riDesc.bin").write_bytes(_ri_desc())
    index = collision.ResourceIndex(res_dir)
    ri = RenderIndex(index, textures=None, res_dirs=[res_dir])
    mats = ri.desc.materials("hut")
    assert [m.cls for m in mats] == ["rendinst_simple", "rendinst_decal"]
    assert mats[0].textures == ["hut_d", "", "hut_n"] and mats[0].diffuse() == "hut_d"
    # The decal element (the roof here) is left out of the look and of the LOD costs.
    assert ri.mesh_lods("hut") == [12, 12]
    assert ri.mesh_lods("hut", ranges=True) == [(12, 80.0), (12, 400.0)]
    look = ri.look("hut", 0)
    assert len(look.faces) == 12 and look.colours.shape == (len(look.verts), 3)
    assert ri.look("no such thing", 0) is None and ri.mesh_lods("no such thing") == []


def test_descriptions_read_a_form_one_blk(tmp_path):
    (tmp_path / "riDesc.bin").write_bytes(_ri_desc())
    d = Descriptions([tmp_path])
    assert "hut" in d.blocks and len(d.materials("hut")) == 2


def _type(name, n, options, tree=False, volume=1.0):
    return lv._Type(name, tree, np.zeros((n, 3, 4), np.float32), options, 0, volume)


def test_choose_takes_the_game_lods_for_one_distance():
    inf = float("inf")
    house = _type("house", 10, [(0, 1000, 100.0), (1, 200, 600.0), (2, 50, 2000.0)], volume=500.0)
    crate = _type("crate", 1000, [(0, 300, 20.0), (1, 30, 80.0)], volume=1.0)
    tree = _type("tree", 1000, [(0, 600, 60.0), (lv._GLYPH, 18, inf)], tree=True)
    # Everything fits: the finest LODs.
    dropped, d = lv._choose([house, crate, tree], 10**9)
    assert dropped == [] and (house.pick, crate.pick, tree.pick) == (0, 0, 0) and d == 0.0
    # A budget that forces a distance past the crate's and the tree's mesh LODs, not the house's last one.
    dropped, d = lv._choose([house, crate, tree], 10 * 1000 + 1000 * 30 + 1000 * 18)
    assert dropped == [] and crate.pick == 1 and tree.pick == 1 and house.pick == 0
    # Past every range a building keeps its coarsest LOD; below that, the smallest types are left out.
    dropped, d = lv._choose([house, crate, tree], 10 * 50 + 1000 * 18)
    assert house.pick == 2 and dropped == ["crate"]


def test_choose_never_spends_past_the_budget():
    rng = np.random.default_rng(1)
    types = []
    for i in range(40):
        lods = sorted(rng.integers(10, 5000, 3).tolist(), reverse=True)
        ranges = sorted(rng.uniform(10, 1500, 3).tolist())
        types.append(_type(f"t{i}", int(rng.integers(1, 300)), [(k, n, r) for k, (n, r) in enumerate(zip(lods, ranges))]))
    for budget in (10**4, 10**5, 10**6):
        dropped, _d = lv._choose(types, budget)
        assert sum(t.cost for t in types if t.name not in dropped) <= budget


def test_tree_glyph_parts():
    v, f, crown = lv._tree_glyph(((-2, 0, -2), (2, 10, 2)))
    assert len(f) == 18 and f.max() < len(v) and crown.sum() == len(v) - 6
    assert v[:, 1].max() == pytest.approx(10) and v[:, 1].min() == pytest.approx(0)


def test_build_draws_render_meshes_with_their_colours(tmp_path):
    units = np.full((32, 32), 1000, np.uint16)
    m = np.c_[np.eye(3), [20.0, 0.0, 20.0]]
    level = levelsynth.level(levelsynth.heightmap_block(units, 2.0, -10.0, 655.35, 0.0, 0.0),
                             levelsynth.rigen_block(64.0, [("hut", 0, [m])]))
    root = tmp_path / "War Thunder"
    (root / "levels").mkdir(parents=True)
    (root / "levels" / "lvl.bin").write_bytes(level)
    tree = ("", [("water_level", -50.0), ("tankMapCoord0", [0.0, 0.0]), ("tankMapCoord1", [62.0, 62.0])], [])
    (root / "aces.vromfs.bin").write_bytes(levelsynth.vromfs({"levels/lvl.blk": levelsynth.blk(tree)}))
    res = root / "content" / "base" / "res"
    res.mkdir(parents=True)
    (res / "a.grp").write_bytes(levelsynth.grp_pack({"hut": (RENDINST_CLASS, _hut())}))
    (res / "riDesc.bin").write_bytes(_ri_desc())
    rec = lv.build(lv.Game(root), root / "levels" / "lvl.bin", tmp_path / "out", detail="high", log=lambda s: None)
    obj = rec["parts"]["objects"]
    assert obj["instances"] == {"buildings": 1, "trees": 0} and obj["drawnAs"] == {"lod0": 1}
    assert obj["triangles"] == 12 and rec["triangles"]["structure:lvl buildings"] == 12
    assert rec["detail"] == "high" and rec["trianglesTotal"] == sum(rec["triangles"].values())
    raw = (tmp_path / "out" / "lvl.glb").read_bytes()
    (n,) = struct.unpack_from("<I", raw, 12)
    doc = json.loads(raw[20 : 20 + n])
    mesh = next(mm for mm in doc["meshes"] if mm["name"] == "structure:lvl buildings")
    prim = mesh["primitives"][0]
    assert "COLOR_0" in prim["attributes"]
    acc = doc["accessors"][prim["attributes"]["POSITION"]]
    # The hut at game (20, 0, 20), its walls 2 m high (no roof: that element is a decal); glb z mirrored.
    assert acc["min"] == pytest.approx([19, 0, -21], abs=0.05) and acc["max"] == pytest.approx([21, 2, -19], abs=0.05)
