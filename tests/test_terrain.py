"""The terrain colour readers on built data: DDSx mips, land classes and their weight map (per-cell textures and
the packed atlas), the physics map's decals, splines, and the composed image."""

from __future__ import annotations

import struct

import numpy as np
import pytest

import levelsynth
from heat3d_ext_warthunder import dagorlevel, terrain


def _ddsx(rgba: np.ndarray, mips: list[np.ndarray] | None = None, rev: bool = False) -> bytes:
    """An uncompressed A8R8G8B8 DDSx: header and data (top level first, or last with `rev`)."""
    levels = [rgba] + (mips or [])
    surf = [np.ascontiguousarray(m[:, :, [2, 1, 0, 3]]).tobytes() for m in levels]
    data = b"".join(surf[::-1] if rev else surf)
    h, w = rgba.shape[:2]
    flags = 0x00040000 if rev else 0
    head = struct.pack("<4sIIHHBBHHBBII", b"DDSx", 21, flags, w, h, len(levels), 0, 1, 32, 0, 0, len(data), 0)
    return head + data


def _str(s: str) -> bytes:
    b = s.encode()
    return struct.pack("<i", len(b)) + b + b"\0" * ((-len(b)) % 4)


def _blk(params: list[tuple[str, object]], kids: list | None = None) -> bytes:
    return levelsynth.blk(("", params, kids or []))


def _lmap(classes: list[tuple[str, list]], cells: tuple[int, int], cell_size: float, origin: tuple[int, int],
          detail_map: bytes, textures: list[str] = ()) -> bytes:
    """A land mesh block: header, render-data texture names, land classes, then `detail_map` (built by the caller,
    whose offsets count from the header's base)."""
    names = b"".join(n.encode() + b"\0" for n in textures)
    hdr = bytearray(struct.pack("<II", 8, len(textures)))
    offs_at = len(hdr)
    hdr += b"\0" * (4 * len(textures))
    at = len(hdr)
    for i, n in enumerate(textures):
        struct.pack_into("<i", hdr, offs_at + 4 * i, at)
        at += len(n) + 1
    hdr += names
    mesh = struct.pack("<4i", len(textures), 0, 0, 0) + struct.pack("<i", len(hdr)) + bytes(hdr)
    lc = bytearray(struct.pack("<i", len(classes)))
    for name, params in classes:
        body = _str(name) + _blk(params[0], params[1] if len(params) > 1 else None)
        lc += struct.pack("<I", len(body)) + body
    detail = struct.pack("<I", len(lc)) + bytes(lc)
    mesh_ofs = 16
    detail_ofs = mesh_ofs + len(mesh)
    dm = detail_map(detail_ofs + len(detail)) if callable(detail_map) else detail_map
    tile_ofs = detail_ofs + len(detail) + len(dm)
    tail = _str("")  # no vertical texture
    payload = (b"lndm" + struct.pack("<iffiiiii", 4, 32.0, cell_size, cells[0], cells[1], origin[0], origin[1], 0)
               + struct.pack("<4i", mesh_ofs, detail_ofs, tile_ofs, 0) + mesh + detail + dm + tail)
    return levelsynth._block(b"lmap", payload)


def _legacy_detail_map(cells: tuple[int, int], tex: int, records: list[tuple[list[int], bytes, bytes]]):
    """DetailMap::load's legacy form: sizes, a cell offset table, then per cell ids, length, second offset, DDSx."""

    def build(start: int) -> bytes:
        sx, sy = cells
        head = struct.pack("<4i", sx, sy, tex, tex)
        table_at = start + len(head)
        body = bytearray()
        offs = []
        first = table_at + 4 * sx * sy
        for ids, t1, t2 in records:
            offs.append(first + len(body))
            rec = bytes(ids + [0xFF] * (7 - len(ids)))
            rec += struct.pack("<ii", len(t1) + len(t2), len(t1) if t2 else 0) + t1 + t2
            body += rec
        return head + struct.pack(f"<{sx * sy}i", *offs) + bytes(body)

    return build


def _level(*blocks: bytes):
    data = levelsynth.level(*blocks)
    return data, dagorlevel.blocks(data)


def test_ddsx_mips_and_reverse_order():
    top = np.zeros((8, 8, 4), np.uint8)
    top[..., 0] = 200
    top[..., 3] = 255
    small = np.zeros((4, 4, 4), np.uint8)
    small[..., 1] = 100
    small[..., 3] = 255
    for rev in (False, True):
        blob = _ddsx(top, [small], rev=rev)
        img = terrain.decode_ddsx(blob[:32], blob[32:])
        assert img.shape == (8, 8, 4) and img[0, 0, 0] == 200
        img = terrain.decode_ddsx(blob[:32], blob[32:], max_size=4)
        assert img.shape == (4, 4, 4) and img[0, 0, 1] == 100


def test_ddsx_without_its_top_levels():
    """A texture whose top level lives in the -hq pack: the levels present are found from the size."""
    top = np.zeros((8, 8, 4), np.uint8)
    small = np.full((4, 4, 4), 77, np.uint8)
    blob = _ddsx(top, [small])
    head = bytearray(blob[:32])
    data = blob[32 + 8 * 8 * 4 :]
    struct.pack_into("<I", head, 24, len(data))
    img = terrain.decode_ddsx(bytes(head), data)
    assert img.shape == (4, 4, 4) and img[0, 0, 0] == 77


def test_land_classes_and_legacy_weights():
    w = np.zeros((4, 4, 4), np.uint8)
    w[:, :, 1] = 255  # all of the second land class (channel G); the first is derived
    w[0, :, 1] = 0  # the first texel row (south edge): all first
    classes = [("a", [[("texture", "a_cm*"), ("detailmap", "a_det"), ("size", [64.0, 64.0])]]),
               ("b", [[("texture", "b_cm*"), ("splattingmap", "b_mask"), ("detailRed", "r"), ("size", [32.0, 32.0]),
                       ("offset", [5.0, 6.0])]])]
    dm = _legacy_detail_map((1, 1), 4, [([0, 1], _ddsx(w), b"")])
    data, table = _level(_lmap(classes, (1, 1), 100.0, (0, 0), dm, ["decal_road_sand_x_tex_d*", "other*"]))
    d = terrain.read_land_detail(data, table)
    assert [c.name for c in d.classes] == ["a", "b"]
    assert d.classes[0].colormap == "a_cm*" and d.classes[0].details[0] == "a_det"
    assert d.classes[1].splatting == "b_mask" and d.classes[1].tile == (1 / 32.0, 1 / 32.0)
    assert d.classes[1].offset == (-5.0, -6.0)
    assert list(d.ids[0, 0][:3]) == [0, 1, 0xFF]
    wt = d.weights(0)
    assert wt.shape == (7, 4, 4)
    assert wt[1, 2, 2] == pytest.approx(1.0) and wt[0, 2, 2] == pytest.approx(0.0)
    assert wt[0, 0, 0] == pytest.approx(1.0)  # derived: what the others leave
    _, at = terrain._weights_at(d, np.array([50.0, 50.0]), np.array([90.0, 1.0]))
    assert at[0, 1] == pytest.approx(1.0) and at[1, 0] == pytest.approx(1.0)
    assert terrain.land_mesh_textures(data, table) == ["decal_road_sand_x_tex_d*", "other*"]


def test_packed_weight_atlas():
    elem = 4
    page_w = (elem + 4 + 3) & ~3  # 8
    atlas = np.zeros((page_w, page_w * 2, 4), np.uint8)
    atlas[2 : 2 + elem, page_w + 2 : page_w + 2 + elem, 0] = 64  # page 1: first weight a quarter
    atlas[..., 3] = 255

    def build(start: int) -> bytes:
        sx = sy = 1
        out = struct.pack("<4i", sx, sy, 0, elem) + struct.pack("<i", 0) + bytes([0xFF] * 7) + b"\0" * 8
        rec = struct.pack("<I", 1 | (1 << 28)) + bytes([2, 0] + [0xFF] * 5) + b"\0"  # page 1, two classes
        out += struct.pack("<ii", 2, 2) + rec
        blob = _ddsx(atlas)
        return out + struct.pack("<i", len(blob)) + blob

    classes = [("a", [[("texture", "a*")]]), ("b", [[("texture", "b*")]]), ("c", [[("texture", "c*")]])]
    data, table = _level(_lmap(classes, (1, 1), 100.0, (0, 0), build))
    d = terrain.read_land_detail(data, table)
    assert list(d.ids[0, 0][:2]) == [2, 0]
    wt = d.weights(0)
    assert wt[0, 1, 1] == pytest.approx(64 / 255, abs=1e-3)
    assert wt[1, 1, 1] == pytest.approx(1 - 64 / 255, abs=1e-3)  # the last blended is derived
    assert wt[2:].sum() == 0


def _phys_block(version=1) -> bytes:
    names = ["default", "sand", "road"]
    head = struct.pack("<i", version) + struct.pack("<i", len(names)) + b"".join(_str(n) for n in names)
    head += struct.pack("<iifff", 32, 32, -10.0, -20.0, 2.0)
    # the tree: one node with 2x2 subnodes; three filled, one a 16x16 1-bit map
    tree = bytes([0x80, 1])
    tree += bytes([1, 0]) * 3
    bits = np.zeros(256, np.uint8)
    bits[:128] = 1
    tree += bytes([0x04 | 0x10, 1]) + bytes([0, 2]) + np.packbits(bits, bitorder="little").tobytes()
    decal = struct.pack("<H", 3) + np.array([[0, 0], [10, 0], [0, 10]], "<f4").tobytes()
    decal += struct.pack("<H", 0)
    decal += bytes([2]) + struct.pack("<H", 1) + struct.pack("<3H", 0, 1, 2)
    decal += struct.pack("<H", 0) + struct.pack("<3H", 0, 1, 2)  # bitmap texture id, texture-coordinate indices
    decal += bytes([0]) + struct.pack("<H", 0)
    raw = tree + struct.pack("<H", 1) + decal + struct.pack("<H", 0)
    import zstandard

    comp = zstandard.ZstdCompressor().compress(raw)
    return levelsynth._block(b"LMp2", head + struct.pack("<I", len(comp) | (1 << 30)) + comp)


def test_phys_map_tree_and_decals():
    data, table = _level(_phys_block())
    pm = terrain.read_phys_map(data, table)
    assert pm.materials == ["default", "sand", "road"]
    assert pm.size == 32 and pm.offset == (-10.0, -20.0) and pm.scale == 2.0
    g = pm.grid()
    assert (g[:16, :16] == 1).all() and (g[16:, :16] == 1).all() and (g[:16, 16:] == 1).all()
    assert (g[16:24, 16:] == 2).all() and (g[24:, 16:] == 0).all()
    assert len(pm.decals) == 1
    (mat, f), = pm.decals[0].runs
    assert mat == "road" and f.tolist() == [[0, 1, 2]]


def test_splines():
    pts = np.array([[[0, 0, 0], [0, 0, 0], [1, 0, 0]], [[9, 0, 0], [10, 0, 0], [10, 0, 0]]], "<f4")
    body = struct.pack("<i", 1) + _str("decal_road_x_12") + struct.pack("<i", 2) + pts.tobytes()
    data, table = _level(levelsynth._block(b"hspl", body))
    (s,) = terrain.read_splines(data, table)
    assert s.name == "decal_road_x_12" and terrain.spline_asset(s.name) == "decal_road_x"
    pl = s.polyline(4)
    assert pl[0].tolist() == [0, 0, 0] and pl[-1].tolist() == [10, 0, 0] and len(pl) == 5


class _FakeTextures(terrain.Textures):
    def __init__(self, images: dict[str, np.ndarray]):
        self.where = {}
        self._imgs = images
        self.missing = set()

    def image(self, name, max_size=512):
        n = self.clean(name or "")
        img = self._imgs.get(n)
        if img is None:
            self.missing.add(n)
            return None
        if img.shape[2] == 3:
            img = np.concatenate([img, np.full(img.shape[:2] + (1,), 255, np.uint8)], 2)
        return img


def test_terrain_colour_composes_classes_and_roads():
    w = np.zeros((4, 4, 4), np.uint8)
    w[:, 2:, 1] = 255  # east half: the second class
    classes = [("green", [[("texture", "g_cm*"), ("detailmap", "grey"), ("size", [50.0, 50.0])]]),
               ("red", [[("texture", "r_cm*"), ("detailmap", "grey"), ("size", [50.0, 50.0])]])]
    dm = _legacy_detail_map((1, 1), 4, [([0, 1], _ddsx(w), b"")])
    data, table = _level(_lmap(classes, (1, 1), 100.0, (0, 0), dm), _phys_block())
    # a mid grey detail leaves the colour map as it is: 0.2178 linear times 2^2.2 is 1
    grey = np.full((4, 4, 3), 128, np.uint8)
    imgs = {"g_cm": np.tile(np.array([40, 160, 40], np.uint8), (8, 8, 1)),
            "r_cm": np.tile(np.array([160, 40, 40], np.uint8), (8, 8, 1)), "grey": grey}
    fake = _FakeTextures(imgs)

    class G:
        root = None

    img, info = terrain.terrain_colour(G(), data, table, (0.0, 0.0, 100.0, 100.0), metres_per_pixel=1.0, textures=fake)
    assert img.shape == (100, 100, 3)
    assert img[50, 10, 1] > img[50, 10, 0] + 60  # west: green
    assert img[50, 90, 0] > img[50, 90, 1] + 60  # east: red
    # the road decal (game x 0..10, z 0..10 offset by nothing) is painted in the south-west corner: bottom rows
    assert info["roads"]["decalRuns"] == 1 and info["roads"]["pixels"] > 20
    assert tuple(img[97, 2]) != tuple(img[50, 10])
    assert info["pixels"] == [100, 100]
