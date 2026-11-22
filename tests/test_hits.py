"""Hit analysis fields (0.3.1): hit keys, the projectile's last step, what came after a hit, the parts it damaged,
the vehicles' own part lists and the ammunition named by speed. Synthetic bytes only."""

from __future__ import annotations

import struct
from types import SimpleNamespace

import pyarrow.parquet as pq
import pytest

import synth
from heat3d_ext_warthunder import arsenal, convert, damage_parts, wrpl
from test_ecs import battle_with_entities


def key_bytes(shooter: int, kind: int, number: int) -> bytes:
    return synth.le(shooter | 0x800, 2) + bytes([kind]) + synth.le(number, 2) + b"\x00"


def shell_state(shooter: int, kind: int, number: int, t: float, point, direction, local, local_dir, speed: float,
                value: float = 266.9) -> bytes:
    """0xF15F's body: field 1 the shooter, field 2 the record (see wrpl.SHELL_STATE_AT), field 3 the shooter again."""
    rec = struct.pack("<If", 661235, t) + b"\x08" + bytes([kind]) + synth.le(number, 2) + b"\x00" + bytes(12)
    rec += struct.pack("<14f", *point, *direction, local[0], local[1], -local[2], local_dir[0], local_dir[1],
                       -local_dir[2], speed, value) + bytes(8)
    sh = synth.le(shooter | 0x800, 2)
    return synth.id_fields({1: (16, sh), 2: (len(rec) * 8, rec), 3: (16, sh)})


def after_hit(shooter: int, kind: int, number: int, flags: int, value: float) -> bytes:
    return synth.id_fields({1: (48, key_bytes(shooter, kind, number)), 2: (8, flags), 3: (32, struct.pack("<f", value))})


def after_hit_2(shooter: int, kind: int, number: int, flags: int, n: int, value: float) -> bytes:
    return synth.id_fields({1: (48, key_bytes(shooter, kind, number)), 2: (8, flags), 3: (8, n),
                            4: (32, struct.pack("<f", value))})


def part_damaged(part: int, flag: int = 0) -> bytes:
    return synth.id_fields({2: (16, synth.le(part, 2)), 3: (8, flag)})


def unit_on_hit(flags: int) -> bytes:
    return synth.id_fields({1: (8, 0x3B), 2: (8, 0x68), 3: (8, 0x2D), 4: (8, flags)})


def test_hit_key_names_a_hit_in_every_message_about_it():
    """The shooter's uid (low 11 bits), the kind byte and the hit's number, from the six bytes that open the hit."""
    assert wrpl.hit_key(key_bytes(25, 1, 1636)) == "25:1:1636"
    assert wrpl.hit_key(b"\x19\x08") == ""
    h = wrpl.read_hit_effect(synth.hit_effect(344, 7, (150, 50, -30)))
    assert h["key"] == "344:4:7"
    a = wrpl.read_after_hit(after_hit(25, 1, 1636, 0x51, 377.43))
    assert a["key"] == "25:1:1636" and a["n"] == 0x51 and a["value"] == pytest.approx(377.43, abs=1e-3)
    b = wrpl.decode_unit_message(0xF13C, after_hit_2(31, 1, 1640, 0x51, 2, 467.85))
    assert b == {"key": "31:1:1640", "flags": 0x51, "n": 2, "value": pytest.approx(467.85, abs=1e-3)}


def test_shell_state_reads_the_projectiles_last_step():
    """0xF15F: its key split over fields 1 and 2, the world point and direction, the same in the unit's frame (z sent
    to the left, read to the right) and the speed."""
    body = shell_state(25, 1, 1636, 126.887, (1200.0, 5.758, 2733.0), (0.991, -0.0318, 0.1299), (1.128, 2.14, -19.92),
                       (-0.0274, -0.082, 0.9963), 707.0)
    d = wrpl.decode_unit_message(0xF15F, body)
    assert d["key"] == "25:1:1636" and d["time"] == pytest.approx(126.887, abs=1e-3)
    assert d["point"] == pytest.approx((1200.0, 5.758, 2733.0), abs=1e-3)
    assert d["dir"] == pytest.approx((0.991, -0.0318, 0.1299), abs=1e-4)
    assert d["localPoint"] == pytest.approx((1.128, 2.14, -19.92), abs=1e-3)
    assert d["localDir"] == pytest.approx((-0.0274, -0.082, 0.9963), abs=1e-4)
    assert d["speed"] == pytest.approx(707.0) and d["value"] == pytest.approx(266.9, abs=1e-3)
    assert wrpl.read_shell_state(synth.id_fields({1: (16, b"\x19\x08"), 2: (64, bytes(8))})) is None


def test_part_damaged_is_one_part_number():
    assert wrpl.read_part_damaged(part_damaged(218)) == {"part": 218, "flag": 0}
    assert wrpl.decode_unit_message(0xF13A, part_damaged(54, 3)) == {"part": 54, "flag": 3}


class _Blk:
    def __init__(self, name, blocks=(), params=None):
        self.name, self.blocks, self.params = name, list(blocks), dict(params or {})

    def get(self, k, d=None):
        return self.params.get(k, d)

    def block(self, name):
        return next((b for b in self.blocks if b.name == name), None)


def _order(nodes: set[str]) -> damage_parts.PartOrder:
    unit = _Blk("root", [_Blk("DamageParts", [
        _Blk("hull", [_Blk("body_front_dm"), _Blk("body_side_dm"), _Blk("body_top_dm")]),
        _Blk("crew", [_Blk("driver_dm"), _Blk("loader_01_dm"), _Blk("gunner_dm"), _Blk("commander_dm")]),
        _Blk("power_block", [_Blk("engine_dm", [_Blk("fire")]), _Blk("transmission_dm")]),
        _Blk("ammo", [_Blk("ammo_turret_01_dm"), _Blk("ammo_turret_02_dm"), _Blk("ammo_body_01_dm")]),
        _Blk("chassis", [_Blk("submodule", [_Blk("ex_decor_07_dm")])]),
    ])], {"model": "test_tank"})
    archive = SimpleNamespace(blk=lambda path: unit if path.endswith("/test_tank.blk") else (_ for _ in ()).throw(KeyError(path)))
    po = damage_parts.PartOrder(archive, res_root=SimpleNamespace())
    po._model_nodes = lambda model: nodes if model == "test_tank" else None
    return po


def test_a_vehicles_parts_are_its_blks_parts_that_its_model_has():
    """The blk's parts depth first, only those the collision model has: a part with blocks of its own (`fire`)
    counts as one, a group's sub-group is walked into."""
    po = _order({"body_front_dm", "body_top_dm", "driver_dm", "gunner_dm", "commander_dm", "engine_dm",
                 "ammo_turret_02_dm", "ammo_body_01_dm", "ex_decor_07_dm", "gun_barrel_dm"})
    assert po.parts("test_tank") == ["body_front_dm", "body_top_dm", "driver_dm", "gunner_dm", "commander_dm",
                                     "engine_dm", "ammo_turret_02_dm", "ammo_body_01_dm", "ex_decor_07_dm"]
    assert po.name("test_tank", 5) == "engine_dm" and po.name("test_tank", 99) == "" and po.name("other", 0) == ""
    assert not damage_parts.PartOrder()


@pytest.mark.parametrize("part, group", [
    ("driver_dm", "crew"), ("gunner_01_dm", "crew"), ("machine_gunner_03_dm", "crew"), ("commander_dm", "crew"),
    ("loader_dm", "crew"), ("pilot_dm", "crew"), ("ammo_turret_12_dm", "ammo"), ("fuel_tank_exterior_r_01_dm", "fuel"),
    ("engine_dm", "engine"), ("transmission_dm", "transmission"), ("cannon_breech_dm", "gun"),
    ("drive_turret_h_dm", "turret_drive"), ("track_l_dm", "tracks"), ("body_front_dm", "armour"),
    ("optic_gun_dm", "optics"), ("radio_station_dm", "equipment"), ("something_dm", ""),
])
def test_part_groups(part, group):
    assert damage_parts.part_group(part) == group
    assert damage_parts.is_crew(part) == (group == "crew")


def test_global_part_names_follow_the_games_list():
    blk = _Blk("root", [_Blk("default"), _Blk("hull", [_Blk("body_front"), _Blk("body_side")]),
                        _Blk("tpl", params={"template": "track_#2#"}), _Blk("body_front"), _Blk("x", params={"template": "a#1:3#"})])
    names = damage_parts.global_names(SimpleNamespace(blk=lambda p: blk))
    assert names == ["default", "body_front", "body_side", "track_1", "track_2", "a1", "a2", "a3"]


def test_shell_props_and_impact_speed():
    bullet = _Blk("bullet", [_Blk("armorpower", params={"ArmorPower0m": [120.0, 10.0], "ArmorPower1000m": [100.0, 1000.0]}),
                             _Blk("damage", [_Blk("kinetic", params={"demarrePenetrationK": 0.9, "demarreSpeedPow": 1.43,
                                                                     "demarreMassPow": 0.71, "demarreCaliberPow": 1.07})])],
                  {"bulletName": "45mm_BR_243", "bulletType": "aphebc_tank", "speed": 760.0, "mass": 1.43,
                   "caliber": 0.045, "Cx": 0.39837, "explosiveMass": 0.019, "ricochetPreset": "apbc"})
    p = arsenal.shell_props(bullet)
    assert p["name"] == "45mm_br_243" and p["ammoType"] == "APHEBC" and p["caliber"] == 45.0
    assert p["armorPower"] == [[10.0, 120.0], [1000.0, 100.0]] and p["demarre"]["k"] == 0.9
    assert arsenal.impact_speed(p, 0) == pytest.approx(760.0)
    # Recorded on the ground test battle: 707 m/s after about 300 m (the model is within 1%).
    assert arsenal.impact_speed(p, 300) == pytest.approx(707.0, rel=0.01)
    assert arsenal.impact_speed({"speed": 760.0}, 300) is None


def _gun(shells: dict[str, tuple[str, float, float, float]]) -> arsenal.Gun:
    g = arsenal.Gun("test_cannon.blk", calibre=45.0)
    for name, (kind, speed, mass, cx) in shells.items():
        g.shells[name] = (kind, 45.0)
        g.props[name] = {"name": name, "speed": speed, "mass": mass, "caliber": 45.0, "Cx": cx}
    return g


def test_speed_match_names_the_one_shell_that_fits():
    g = _gun({"ap": ("APHEBC", 760.0, 1.43, 0.4), "apcr": ("APCR", 985.0, 0.85, 0.48), "he": ("HE", 335.0, 2.14, 0.49)})
    name, err, cal, kind = convert.speed_match([g], 835.0, 300)
    assert name == "apcr" and abs(err) < 0.01 and cal == 45.0 and kind == "APCR"
    assert convert.speed_match([g], 500.0, 300) is None
    # Two shells 3 m/s apart: no name, but the calibre (and the type they share).
    twin = _gun({"ap": ("APHEBC", 760.0, 1.43, 0.4), "ap2": ("APHEBC", 757.0, 1.43, 0.4)})
    assert convert.speed_match([twin], 700.0, 300) == ("", pytest.approx(-0.003, abs=0.01), 45.0, "APHEBC")


def test_a_hits_key_links_its_speed_its_after_hit_and_the_parts_it_damaged(tmp_path, monkeypatch):
    """
    344 hits the tank 177 (entity 3) with hit 1636: 0xF15F gives the projectile's last step, 0xF117 what came after,
    two 0xF13A at the same moment the parts it damaged (named by the tank's own list), 0xF144 that it killed. A
    second 0xF13A list a second later with no hit gets a row of its own.
    """
    po = _order({"body_front_dm", "driver_dm", "gunner_dm", "engine_dm", "ammo_body_01_dm"})
    po._parts["germ_flakpz_gepard"] = po.parts("test_tank")
    monkeypatch.setattr(damage_parts.PartOrder, "from_game", classmethod(lambda cls, game=None, archive=None: po))
    monkeypatch.setattr(arsenal.Arsenal, "from_game", classmethod(lambda cls, game=None: cls()))
    hit = synth.hit_effect(344, 1636, (983, 328, -197))
    hit = hit.replace(synth.le(344, 2) + b"\x04", synth.le(344, 2) + b"\x01", 1)
    more = [synth.packet(4, 10900, synth.unit_message(3, 0xF0E9, hit)),
            synth.packet(4, 10900, synth.unit_message(3, 0xF144, unit_on_hit(0x25))),
            synth.packet(4, 10900, synth.unit_message(3, 0xF15F, shell_state(
                344, 1, 1636, 10.9, (500.0, 121.0, 790.0), (0.0, 0.0, 1.0), (-9.0, 1.0, 0.0), (1.0, 0.0, 0.0), 707.0))),
            synth.packet(4, 10900, synth.unit_message(3, 0xF117, after_hit(344, 1, 1636, 0x51, 377.4))),
            synth.packet(4, 10900, synth.unit_message(3, 0xF13A, part_damaged(1))),
            synth.packet(4, 10900, synth.unit_message(3, 0xF13A, part_damaged(3))),
            synth.packet(4, 11230, synth.unit_message(3, 0xF13C, after_hit_2(344, 1, 1636, 0xC1, 1, 502.7))),
            synth.packet(4, 12000, synth.unit_message(3, 0xF13A, part_damaged(4)))]
    f = tmp_path / "h.wrpl"
    f.write_bytes(battle_with_entities(more, version=101421))
    tpath, _ = convert.convert([f], tmp_path / "out")
    rows = pq.read_table(tpath).to_pylist()
    shot = next(r for r in rows if r["event"] == "shot")
    assert shot["hitKey"] == "344:1:1636" and shot["hitOutcome"] == "kill"
    assert shot["shellSpeed"] == pytest.approx(707.0) and shot["shellValue"] == pytest.approx(266.9, abs=1e-3)
    assert (shot["shellPointX"], shot["shellPointY"], shot["shellPointZ"]) == pytest.approx((500.0, 121.0, 790.0))
    assert (shot["shellDirX"], shot["shellDirY"], shot["shellDirZ"]) == pytest.approx((0.0, 0.0, 1.0))
    assert (shot["shellLocalX"], shot["shellLocalY"], shot["shellLocalZ"]) == pytest.approx((-9.0, 1.0, 0.0))
    assert shot["shellLocalDirX"] == pytest.approx(1.0)
    assert shot["afterHitFlags"] == 0x51 and shot["afterHitValue"] == pytest.approx(377.4, abs=1e-3)
    assert shot["damagedPartIds"] == "1,3" and shot["damagedParts"] == "driver_dm,engine_dm"
    assert shot["damagedGroups"] == "crew,engine" and shot["crewDamaged"] == 1 and shot["ammoDamaged"] == 0
    after = [r for r in rows if r["event"] == "after_hit"]
    assert [(r["afterHitMessage"], r["hitKey"], r["afterHitFlags"]) for r in after] == [
        ("F117", "344:1:1636", 0x51), ("F13C", "344:1:1636", 0xC1)]
    assert after[1]["afterHitCount"] == 1 and after[1]["time"] == pytest.approx(11.23)
    own = next(r for r in rows if r["event"] == "parts_damaged")
    assert own["damagedParts"] == "ammo_body_01_dm" and own["ammoDamaged"] == 1 and own["time"] == pytest.approx(12.0)


def test_parts_without_an_install_keep_their_numbers(tmp_path, monkeypatch):
    monkeypatch.setattr(damage_parts.PartOrder, "from_game", classmethod(lambda cls, game=None, archive=None: cls()))
    more = [synth.packet(4, 10900, synth.unit_message(3, 0xF0E9, synth.hit_effect(344, 7, (983, 328, -197)))),
            synth.packet(4, 10920, synth.unit_message(3, 0xF13A, part_damaged(54)))]
    f = tmp_path / "h.wrpl"
    f.write_bytes(battle_with_entities(more, version=101421))
    tpath, _ = convert.convert([f], tmp_path / "out")
    shot = next(r for r in pq.read_table(tpath).to_pylist() if r["event"] == "shot")
    assert shot["hitKey"] == "344:4:7" and shot["damagedPartIds"] == "54" and shot["damagedParts"] == "#54"
    assert shot["crewDamaged"] == 0 and shot["shellSpeed"] is None


def test_kept_parts_name_a_vehicle_without_the_resource_packs(tmp_path):
    """Parts read from the packs are kept; a reader with the unit files only puts them in its blk's order."""
    nodes = {"body_front_dm", "driver_dm", "engine_dm"}
    po = _order(nodes)
    po.kept_path = tmp_path / "kept.json"
    assert po.parts("test_tank") == ["body_front_dm", "driver_dm", "engine_dm"] and po.save()
    other = damage_parts.PartOrder(po.archive, None, tmp_path / "kept.json")
    assert other and other.parts("test_tank") == ["body_front_dm", "driver_dm", "engine_dm"]
    assert not damage_parts.PartOrder(po.archive, None, tmp_path / "none.json")


def test_the_part_struck_and_a_destroyed_module_are_named_the_games_way(tmp_path, monkeypatch):
    """`hitPart`'s number and a destroyed module's (0xF118) are places in the game's list (`global_names`)."""
    po = _order({"engine_dm"})
    po._global = ["default", "body_front", "turret_front", "engine", "fin", "track_l"]
    monkeypatch.setattr(damage_parts.PartOrder, "from_game", classmethod(lambda cls, game=None, archive=None: po))
    kill = b"\x02\x58" + synth.le(wrpl.PART_KILL, 2) + synth.id_fields({1: (16, synth.le(177 | 0x800, 2)),
                                                                        2: (16, synth.le(5, 2))})
    more = [synth.packet(4, 10900, synth.unit_message(3, 0xF0E9, synth.hit_effect(344, 7, (983, 328, -197),
                                                                                   part=synth.hit_part(2)))),
            synth.packet(4, 10950, kill)]
    f = tmp_path / "h.wrpl"
    f.write_bytes(battle_with_entities(more, version=101421))
    tpath, _ = convert.convert([f], tmp_path / "out")
    rows = pq.read_table(tpath).to_pylist()
    assert next(r for r in rows if r["event"] == "shot")["hitPartName"] == "turret_front"
    m = next(r for r in rows if r["event"] == "module_destroyed")
    assert m["weapon"] == "part 5" and m["partName"] == "track_l" and m["partGroup"] == "tracks"


@pytest.mark.parametrize("agree, disagree, version, ok, by", [
    (20, 1, 101404, True, "fires"), (5, 9, 101421, False, "fires"), (1, 1, 101404, False, "version"),
    (0, 0, 101421, True, "version"),
])
def test_the_games_numbering_is_trusted_by_the_fires_else_the_version(agree, disagree, version, ok, by):
    got = convert.numbering_matches({"partNamesAgree": agree, "partNamesDisagree": disagree}, version)
    assert got["matches"] is ok and got["by"] == by
    po = damage_parts.PartOrder(SimpleNamespace(blk=lambda p: (_ for _ in ()).throw(KeyError(p))))
    po._global, po.global_ok = ["default", "engine"], ok
    assert po.global_name(1) == ("engine" if ok else "")
