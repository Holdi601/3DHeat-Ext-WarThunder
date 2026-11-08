"""Land-class generation (`landgen.py`) on data built here to the layouts the module documents."""

from __future__ import annotations

import struct

import numpy as np
import pytest

from heat3d_ext_warthunder import landgen as lg

T = lg


# --- builders ------------------------------------------------------------------------------------------


def roblk(tree) -> bytes:
    """A RoDataBlock dump of (name, [(param, type, value)], [children]), the layout `read_roblk` reads."""
    names: list[str] = []

    def collect(t):
        for n in (t[0], *(p[0] for p in t[1])):
            if n not in names:
                names.append(n)
        for c in t[2]:
            collect(c)

    collect(tree)
    names.sort()
    # Block records: the root, then each block's children as one contiguous array.
    order, arrays = [tree], {}
    i = 0
    while i < len(order):
        t = order[i]
        if t[2]:
            arrays[id(t)] = len(order)
            order.extend(t[2])
        i += 1
    rec_at = 0
    params_at = 48 * len(order)
    n_params = sum(len(t[1]) for t in order)
    nm_at = params_at + 8 * n_params
    ptrs_at = nm_at + 16
    strings_at = ptrs_at + 8 * len(names)
    out = bytearray(strings_at)
    name_ofs = []
    for n in names:
        name_ofs.append(len(out))
        out += n.encode() + b"\0"
    while len(out) % 4:
        out += b"\0"
    struct.pack_into("<II", out, nm_at, ptrs_at, len(names))
    for k, o in enumerate(name_ofs):
        struct.pack_into("<I", out, ptrs_at + 8 * k, o)
    fmt = {T.T_POINT2: "<2f", T.T_POINT3: "<3f", T.T_POINT4: "<4f", T.T_IPOINT2: "<2i", T.T_MATRIX: "<12f"}
    p = params_at
    for bi, t in enumerate(order):
        r = rec_at + 48 * bi
        struct.pack_into("<II", out, r, p if t[1] else 0, len(t[1]))
        if t[2]:
            struct.pack_into("<II", out, r + 16, 48 * arrays[id(t)], len(t[2]))
        struct.pack_into("<I", out, r + 32, nm_at)
        struct.pack_into("<i", out, r + 40, names.index(t[0]))
        for pname, kind, v in t[1]:
            if kind == T.T_INT:
                raw = struct.pack("<i", v)
            elif kind == T.T_REAL:
                raw = struct.pack("<f", v)
            elif kind == T.T_BOOL:
                raw = struct.pack("<i", int(v))
            elif kind == T.T_E3DCOLOR:
                raw = struct.pack("<I", v)
            else:
                at = len(out) - nm_at
                out += (v.encode() + b"\0") if kind == T.T_STRING else struct.pack(fmt[kind], *v)
                while len(out) % 4:
                    out += b"\0"
                raw = struct.pack("<i", at)
            struct.pack_into("<4sHH", out, p, raw, names.index(pname), kind)
            p += 8
    return bytes(out)


def hier(dense: np.ndarray) -> bytes:
    """A RoHugeHierBitMap2d<4, 3> dump of a dense bool array (rows = y), with full blocks marked as 1."""
    h, w = dense.shape
    wb, hb = (w + 127) // 128, (h + 127) // 128
    pad = np.zeros((hb * 128, wb * 128), bool)
    pad[:h, :w] = dense
    top_at = 16
    body = bytearray(16 + 4 * wb * hb)
    struct.pack_into("<iiI", body, 0, wb, hb, top_at)
    for by in range(hb):
        for bx in range(wb):
            blk = pad[by * 128 : (by + 1) * 128, bx * 128 : (bx + 1) * 128]
            if not blk.any():
                continue
            if blk.all():
                struct.pack_into("<I", body, top_at + 4 * (by * wb + bx), 1)
                continue
            l2 = len(body)
            struct.pack_into("<I", body, top_at + 4 * (by * wb + bx), l2)
            body += b"\0" * 256
            for ly in range(8):
                for lx in range(8):
                    leaf = blk[ly * 16 : ly * 16 + 16, lx * 16 : lx * 16 + 16]
                    if not leaf.any():
                        continue
                    if leaf.all():
                        struct.pack_into("<I", body, l2 + 4 * (ly * 8 + lx), 1)
                        continue
                    struct.pack_into("<I", body, l2 + 4 * (ly * 8 + lx), len(body))
                    bits = np.packbits(leaf.ravel(), bitorder="little").view("<u4")
                    body += bits.tobytes()
    return bytes(body)


def hier_stream(dense: np.ndarray) -> bytes:
    d = hier(dense)
    return struct.pack("<3i", 4, 3, len(d)) + d


def land_class_stream(tree, dmaps: dict[str, np.ndarray] | None = None) -> bytes:
    b = roblk(tree)
    out = struct.pack("<i", len(b)) + b
    if any(c[0] == "obj_plant_generate" for c in tree[2]):
        dmaps = dmaps or {}
        out += struct.pack("<i", len(dmaps))
        for name, dense in dmaps.items():
            nb = name.encode()
            out += struct.pack("<i", len(nb)) + nb + b"\0" * ((4 - len(nb) % 4) % 4) + hier_stream(dense)
    return out


def plant_obj(rid, weight=1.0, scale=(1.0, 0.0), rot_y=(0.0, 0.0), orient="world"):
    return ("object", [("riResId", T.T_INT, rid), ("weight", T.T_REAL, weight), ("orientation", T.T_STRING, orient),
                       ("scale", T.T_POINT2, scale), ("rot_y", T.T_POINT2, rot_y)], [])


def rigen(mask: np.ndarray, cells=(2, 2), cell_size=16, g2w=8.0, world0=(0.0, 0.0), sweep=None) -> lg.RiGenLand:
    cw, ch = cells
    return lg.RiGenLand(world0, g2w, cell_size, cw, ch, world0, 0.5,
                        lg.HierBitmap(hier(sweep)) if sweep is not None else None, ["lc"],
                        [lg.HierBitmap(hier(mask))], [[0]] * (cw * ch))


# --- tests ---------------------------------------------------------------------------------------------


def test_random_numbers():
    s = 12345
    vals = []
    for _ in range(9):
        s = lg._nxt(s)
        vals.append(s)
    assert lg._nxt(0) == 0x3039
    for k in range(1, 10):
        assert int(lg._states(np.array([12345], np.uint64), k)[0]) == vals[k - 1]
    assert list(lg._seq_states(12345, 9)) == vals
    a, c = lg._JUMP9
    assert (12345 * a + c) & 0xFFFFFFFF == vals[8]
    assert lg._val(np.array([0xFFFFFFFF], np.uint64))[0] == 0x7FFF


def test_bitmap_get_and_leaves():
    rng = np.random.default_rng(1)
    dense = rng.random((200, 300)) < 0.3
    dense[0:128, 128:256] = True  # a full block
    dense[130:146, 0:16] = True  # a full leaf
    bm = lg.HierBitmap(hier(dense))
    ys, xs = np.mgrid[0:256, 0:384]
    got = bm.get(xs, ys)
    want = np.zeros((256, 384), bool)
    want[:200, :300] = dense
    assert (got == want).all()
    for x, y in [(0, 0), (130, 5), (299, 199), (5, 135), (383, 255)]:
        assert bm.get1(x, y) == want[y, x]
    assert not bm.get(-1, 0) and not bm.get1(400, 0)
    assert bm.get_clamped(-5, -5) == want[0, 0]
    seen = np.zeros_like(want)
    for bits, u0, v0 in bm.leaves(0, 0, 383, 255):
        leaf = np.ones((16, 16), bool) if bits is None else np.unpackbits(
            np.asarray(bits, "<u4").view(np.uint8), bitorder="little").reshape(16, 16).astype(bool)
        seen[v0 : v0 + 16, u0 : u0 + 16] = leaf
    assert (seen == want).all()


def test_roblk_round_trip():
    tree = ("", [("i", T.T_INT, -7), ("r", T.T_REAL, 2.5), ("b", T.T_BOOL, True), ("s", T.T_STRING, "abc"),
                 ("p2", T.T_POINT2, (1.0, 2.0)), ("c", T.T_E3DCOLOR, 0x80808080),
                 ("m", T.T_MATRIX, (1, 0, 0, 0, 1, 0, 0, 0, 1, 5, 6, 7))],
            [("child", [("x", T.T_INT, 3)], [("leaf", [], [])]), ("child", [("x", T.T_INT, 4)], [])])
    b = lg.read_roblk(roblk(tree))
    assert b.get("i", T.T_INT) == -7 and b.get("r", T.T_REAL) == 2.5 and b.get("b", T.T_BOOL) is True
    assert b.get("s", T.T_STRING) == "abc" and b.get("p2", T.T_POINT2) == (1.0, 2.0)
    assert b.get("c", T.T_E3DCOLOR) == 0x80808080 and b.get("m", T.T_MATRIX)[9:] == (5.0, 6.0, 7.0)
    assert b.get("i", T.T_REAL, "wrong type") == "wrong type"
    assert [c.get("x", T.T_INT) for c in b.all("child")] == [3, 4]
    assert b.all("child")[0].block("leaf") is not None


def _planted_class(density=5.0, objs=None, dmap=None, size=(256.0, 256.0)):
    params = [("density", T.T_REAL, density), ("rseed", T.T_INT, 777)]
    if dmap is not None:
        params += [("densityMap", T.T_STRING, "dm"), ("mapSize", T.T_POINT2, size)]
    tree = ("", [("riResCount", T.T_INT, 2)],
            [("obj_plant_generate", params, objs or [plant_obj(0, 3.0, (1.0, 0.2), (0.0, 180.0)), plant_obj(1, 1.0)])])
    raw = land_class_stream(tree, {"dm": dmap} if dmap is not None else {})
    return lg.parse_land_class(raw, "lc", ["obj_a", "obj_b"])


def test_parse_land_class():
    dm = np.zeros((128, 128), bool)  # density maps come in whole 128-pixel blocks
    dm[:16, :16] = True
    lc = _planted_class(dmap=dm)
    g = lc.planted[0]
    assert g.rseed == 777 and g.sum_weight == 4.0 and len(g.objs) == 2
    assert g.cell == (2.0, 2.0) and g.dmap.get1(3, 3) and not g.dmap.get1(20, 20)
    assert g.objs[0].scale == pytest.approx((1.0, 0.2)) and g.objs[0].rot[1][1] == pytest.approx(np.pi)


def _run(lc, rg, rect=None, height=None, kinds=None):
    gen = lg.Generator(rg, {0: lc}, {}, lg._Ground(height), kinds, None)
    out = lg._Out(rect=rect)
    subs = [(x0, z0) for _cls, x0, z0 in gen.subcells(rect)]
    if lc.tiled is not None:
        gen.tiled(lc, rg.masks[0], subs, out)
    gen.planted(lc, rg.masks[0], subs, out)
    return {k: np.concatenate(v) for k, v in out.mats.items()}


def test_planted_grid_follows_mask_and_is_deterministic():
    mask = np.zeros((32, 32), bool)
    mask[:, :16] = True  # the western half (8 m pixels: x < 128 m)
    rg = rigen(mask)
    lc = _planted_class(density=5.0)
    a = _run(lc, rg, height=lambda x, z: 0.1 * x + 3)
    b = _run(lc, rg, height=lambda x, z: 0.1 * x + 3)
    assert a.keys() == b.keys() and all(np.array_equal(a[k], b[k]) for k in a)
    allm = np.concatenate(list(a.values()))
    x, z = allm[:, 0, 3], allm[:, 2, 3]
    assert (x < 128).all() and (x >= 0).all() and (z >= 0).all() and (z <= 256).all()
    # 5 per 100 m^2 over 128 x 256 m.
    assert len(allm) == pytest.approx(0.05 * 128 * 256, rel=0.05)
    assert allm[:, 1, 3] == pytest.approx(0.1 * x + 3, abs=1e-3)
    assert len(a["obj_a"]) == pytest.approx(3 * len(a["obj_b"]), rel=0.15)
    sb = np.linalg.norm(a["obj_b"][:, :, 1], axis=1)
    assert sb == pytest.approx(1.0, abs=1e-5)


def test_sweep_mask_excludes():
    mask = np.ones((32, 32), bool)
    sweep = np.zeros((128, 128), bool)
    sweep[:, :64] = True  # 2 m pixels: x < 128 m is excluded
    m = _run(_planted_class(), rigen(mask, sweep=sweep))
    x = np.concatenate([v[:, 0, 3] for v in m.values()])
    assert len(x) and (x >= 128).all()


def test_density_map_and_rect():
    mask = np.ones((32, 32), bool)
    dm = np.zeros((128, 128), bool)
    dm[:64, :] = True  # the southern half of each 256 m tile of the density map (2 m pixels)
    rg = rigen(mask)
    lc = _planted_class(density=2.0, dmap=dm)
    full = _run(lc, rg)
    allm = np.concatenate(list(full.values()))
    assert len(allm) == pytest.approx(0.02 * 256 * 128, rel=0.05)
    assert (allm[:, 2, 3] <= 128.5).all()
    rect = (0.0, 0.0, 100.0, 100.0)
    part = _run(lc, rg, rect=rect)
    p = np.concatenate(list(part.values()))
    inside = (allm[:, 0, 3] <= 100) & (allm[:, 2, 3] <= 100)
    assert len(p) == inside.sum()
    assert np.allclose(np.sort(p[:, 0, 3]), np.sort(allm[inside, 0, 3]))


def test_empty_object_takes_the_sequential_path():
    mask = np.zeros((32, 32), bool)
    mask[::2, :] = True
    rg = rigen(mask)
    plain = _run(_planted_class(objs=[plant_obj(0, 1.0)]), rg)
    # A zero-weight empty object is never picked: the same instances, through the sequential path.
    zero = _run(_planted_class(objs=[plant_obj(0, 1.0), plant_obj(-1, 0.0)]), rg)
    assert np.array_equal(plain["obj_a"], zero["obj_a"])
    half = _run(_planted_class(objs=[plant_obj(0, 1.0), plant_obj(-1, 1.0)]), rg)
    assert len(half["obj_a"]) == pytest.approx(len(plain["obj_a"]) / 2, rel=0.15)


def test_tiled_pattern_repeats_over_the_mask():
    mask = np.zeros((32, 32), bool)
    mask[16:, :] = True  # z >= 128 m
    yaw = np.radians(30)
    c, s = np.cos(yaw), np.sin(yaw)
    # TMatrix columns: x axis, y axis, z axis, position.
    tm = (c, 0, -s, 0, 1, 0, s, 0, c, 10.0, 0.0, 20.0)
    tree = ("", [("landBBoxLim0", T.T_POINT2, (0.0, 0.0)), ("landBBoxLim1", T.T_POINT2, (64.0, 64.0)),
                 ("riResCount", T.T_INT, 1)],
            [("resources", [("rseed", T.T_INT, 5), ("yOffset", T.T_POINT2, (0.0, 0.0))],
              [("object", [("matrix", T.T_MATRIX, tm), ("riResId", T.T_INT, 0)], [])])])
    lc = lg.parse_land_class(land_class_stream(tree), "town", ["house_a"])
    m = _run(lc, rigen(mask), height=lambda x, z: np.full(np.shape(x), 7.0), kinds={"buildings"})["house_a"]
    x, z = m[:, 0, 3], m[:, 2, 3]
    assert len(m) == 4 * 2  # one per 64 m tile over 256 x 128 m
    assert np.allclose((x - 10) % 64, 0) and np.allclose((z - 20) % 64, 0) and (z >= 128).all()
    assert np.allclose(m[:, 1, 3], 7.0)
    assert np.allclose(m[0, :, :3], np.array(tm[:9]).reshape(3, 3).T, atol=1e-6)


def test_grp_refs_and_load(tmp_path):
    # A GRP2 pack with one land class referencing two (render instance, collision) pairs.
    names = ["lc", "tree_a", "tree_a_collision", "rock", ""]
    stream = land_class_stream(("", [("riResCount", T.T_INT, 2)],
                                [("obj_plant_generate", [("density", T.T_REAL, 1.0)], [plant_obj(0), plant_obj(1)])]))
    import zstandard

    packed = zstandard.ZstdCompressor().compress(stream)
    res = struct.pack("<I", (1 << 30) | len(packed)) + packed
    head = bytearray(64)
    name_tab = len(head)
    head += b"\0" * (4 * len(names))
    str_ofs = []
    for n in names:
        str_ofs.append(len(head))
        head += n.encode() + b"\0"
    while len(head) % 4:
        head += b"\0"
    refs_at = len(head)
    head += struct.pack("<4H", 1, 2, 3, 0xFFFF)
    entries_at = len(head)
    head += b"\0" * 12
    data_at = len(head)
    head += struct.pack("<IHHII", lg.LANDCLASS_CLASS, 0, 0, refs_at, 4) + b"\0" * 8
    for i, o in enumerate(str_ofs):
        struct.pack_into("<i", head, name_tab + 4 * i, o)
    res_at = len(head)
    struct.pack_into("<4sIII", head, 0, b"GRP2", len(head) - 16, len(head) - 16, len(res))
    struct.pack_into("<II", head, 16, name_tab, len(names))
    struct.pack_into("<II", head, 32, entries_at, 1)
    struct.pack_into("<II", head, 48, data_at, 1)
    struct.pack_into("<IIHH", head, entries_at, lg.LANDCLASS_CLASS, res_at, 0, 0)
    pack = tmp_path / "test.grp"
    pack.write_bytes(bytes(head) + res)
    assert lg.grp_refs(pack)["lc"] == ["tree_a", "tree_a_collision", "rock", ""]
    lc = lg.load_land_class({("lc", lg.LANDCLASS_CLASS): (pack, res_at)}, "lc")
    assert lc.objects == ["tree_a", "rock"] and len(lc.planted) == 1
    assert lg.load_land_class({}, "lc") is None


def test_keep_thins_deterministically():
    x = np.arange(10000, dtype=float) * 0.37
    z = np.arange(10000, dtype=float) * 1.91
    k = lg._keep(x, z, 0.25)
    assert k.mean() == pytest.approx(0.25, abs=0.03)
    assert np.array_equal(k, lg._keep(x, z, 0.25))
    assert lg._keep(x, z, 1.0).all() and not lg._keep(x, z, 0.0).any()


def test_classify():
    assert lg.classify("anything", True, False) == "trees"
    assert lg.classify("some_bush_a", True, False) == "bushes"
    assert lg.classify("ground_fern", False, False) == "grass"
    assert lg.classify("house_01", False, True) == "buildings"
    assert lg.classify("stone_a", False, False) == "props"
