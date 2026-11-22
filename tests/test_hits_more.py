"""Hit fields of 0.5.0: older games' part numbering, kept archives, aircraft's and ships' weapons and belts, the
modules a hit destroyed. Synthetic data only."""

from __future__ import annotations

import struct
from types import SimpleNamespace

import pyarrow.parquet as pq
import pytest

import synth
from heat3d_ext_warthunder import arsenal, convert, damage_parts, wrpl
from test_ecs import battle_with_entities
from test_hits import _Blk, _order


@pytest.fixture(autouse=True)
def _no_kept_archives(tmp_path, monkeypatch):
    monkeypatch.setenv("HEAT3D_WT_ARCHIVES", str(tmp_path / "archives"))


def vromfs_head(version: tuple[int, int, int, int]) -> bytes:
    """The start of an aces.vromfs.bin with an extended header naming its version."""
    return b"VRFx" + bytes(12) + struct.pack("<HH", 8, 0) + bytes(reversed(version)) + bytes(8)


def test_an_archives_version_is_in_its_header(tmp_path):
    f = tmp_path / "aces.vromfs.bin"
    f.write_bytes(vromfs_head((2, 61, 0, 37)))
    assert damage_parts.archive_version(f) == "2.61.0.37"
    f.write_bytes(b"VRFs" + bytes(20))
    assert damage_parts.archive_version(f) == "" and damage_parts.archive_version(tmp_path / "none") == ""


def test_archives_are_kept_once_per_version_and_found_beside_the_install(tmp_path):
    game = tmp_path / "game"
    game.mkdir()
    (game / "aces.vromfs.bin").write_bytes(vromfs_head((2, 61, 0, 37)))
    (game / "aces.vromfs.bin.old-2026-11-08").write_bytes(vromfs_head((2, 59, 0, 100)))
    assert damage_parts.keep_archive(game) == "2.61.0.37"
    assert (damage_parts.archives_dir() / "aces-2.61.0.37.vromfs.bin").is_file()
    got = damage_parts.kept_archives(game)
    assert set(got) == {"2.61.0.37", "2.59.0.100"} and got["2.59.0.100"].name.endswith("old-2026-11-08")


def test_an_older_numbering_reads_the_base_list_shifted():
    """The older list is the base list without the names inserted at its places 3 (two) and 5 (one)."""
    base = ["default", "a", "b", "new1", "new2", "c", "d", "new3", "e"]
    older = ["default", "a", "b", "c", "d", "e"]
    po = damage_parts.PartOrder().with_numbering(base, (((0, 0), (3, 2), (5, 3)), len(older)))
    assert [po.global_name(i) for i in range(len(older))] == older
    assert po.global_name(len(older)) == "" and po.game_number(4) == 6 and po.game_number(99) is None
    # The table of the 101404 replays: within the older list's length, never past the base list.
    t = damage_parts.OLDER_NUMBERING[101404]
    assert t["runs"][0] == (0, 0) and all(a[0] < b[0] and a[1] <= b[1] for a, b in zip(t["runs"], t["runs"][1:]))


def _fires_po(globals_: list[str]) -> damage_parts.PartOrder:
    po = _order({"body_front_dm", "driver_dm", "engine_dm", "transmission_dm"})
    po._global = list(globals_)
    return po


def test_the_numbering_is_chosen_by_the_fires(tmp_path, monkeypatch):
    """An older replay whose fires disagree with the install's list: the table of its game version is taken when the
    fires agree with it; with too few fires, by its version."""
    game = tmp_path / "game"
    game.mkdir()
    (game / "aces.vromfs.bin").write_bytes(vromfs_head((9, 1, 0, 1)))
    monkeypatch.setattr(convert.install, "find_game", lambda g=None: game)
    monkeypatch.setitem(damage_parts.OLDER_NUMBERING, 90001, {"archive": "9.0.0.1", "base": "9.1.0.1", "length": 3,
                                                                "runs": ((0, 0), (1, 2))})
    # The install's list has two names inserted after "default": the replay's 1 and 2 are its 3 and 4.
    po = _fires_po(["default", "x", "y", "engine", "driver"])
    keys = [("test_tank", 2, 1)] * 2 + [("test_tank", 1, 2)] * 2  # own 2 engine_dm, own 1 driver_dm
    monkeypatch.setattr(convert, "_fire_keys", lambda r, lives, lists: keys)
    r = SimpleNamespace(header={"version": 90001})
    named, info = convert.choose_numbering(r, [], [], po, None)
    assert info["matches"] is False and info["named"] and info["numbering"] == "table 90001" and info["by"] == "fires"
    assert named.global_name(1) == "engine" and named.name("test_tank", 1) == "driver_dm"
    monkeypatch.setattr(convert, "_fire_keys", lambda r, lives, lists: keys[:1])
    named, info = convert.choose_numbering(r, [], [], _fires_po(["default", "x", "y", "engine", "driver"]), None)
    assert info["numbering"] == "table 90001" and info["by"] == "version"
    # A version without a table and too few fires: no names.
    named, info = convert.choose_numbering(SimpleNamespace(header={"version": 90000}), [], [],
                                           _fires_po(["default", "x", "y", "engine", "driver"]), None)
    assert not info["named"] and named.global_name(1) == ""
    # The install's own numbering, where the fires agree with it.
    monkeypatch.setattr(convert, "_fire_keys", lambda r, lives, lists: [("test_tank", 2, 3)] * 3)
    named, info = convert.choose_numbering(r, [], [], _fires_po(["default", "x", "y", "engine", "driver"]), None)
    assert info["matches"] and info["numbering"] == "install"


def _aircraft_archive() -> SimpleNamespace:
    bullet = lambda t, cal=0.0127: _Blk("bullet", params={"bulletType": t, "caliber": cal, "speed": 880.0, "mass": 0.04})
    mg = _Blk("root", [bullet("ap_i_t_ball_M20"), bullet("ap_ball_M2"), _Blk("50cal_universal", [
        bullet("ap_i_ball_M8"), bullet("ap_i_t_ball_M20")]), _Blk("50cal_stealth", [bullet("ap_i_ball_M8")])])
    bomb = _Blk("root", [_Blk("bomb", params={"bulletType": "he_bomb", "caliber": 0.36, "mass": 227.0})])
    missile = _Blk("root", [_Blk("rocket", params={"bulletName": "us_aim9b", "bulletType": "aam", "caliber": 0.127})])
    plane = _Blk("root", [
        _Blk("commonWeapons", [_Blk("Weapon", params={"slot": 0, "preset": "guns"})]),
        _Blk("WeaponSlots", [
            _Blk("WeaponSlot", [_Blk("WeaponPreset", [_Blk("Weapon", params={"blk": "gamedata/weapons/gunM2.blk"}),
                                                      _Blk("Weapon", params={"blk": "gamedata/weapons/gunM2.blk"})],
                                     {"name": "guns"})], {"index": 0}),
            _Blk("WeaponSlot", [_Blk("WeaponPreset", [_Blk("Weapon", params={"blk": "gamedata/weapons/bombguns/us_500lb.blk"})],
                                     {"name": "bomb"}),
                                _Blk("WeaponPreset", [_Blk("Weapon", params={"blk": "gamedata/weapons/rocketguns/us_aim9b.blk"})],
                                     {"name": "aam"})], {"index": 1})])])
    files = {"gamedata/flightmodels/test_plane.blk": plane, "gamedata/weapons/gunm2.blk": mg,
             "gamedata/weapons/bombguns/us_500lb.blk": bomb, "gamedata/weapons/rocketguns/us_aim9b.blk": missile}
    return SimpleNamespace(files=files, blk=lambda p: files[p.lower()] if p.lower() in files else (_ for _ in ()).throw(KeyError(p)))


def test_an_aircrafts_weapons_come_from_its_slots_with_their_belts():
    arms = arsenal.Arsenal(_aircraft_archive())
    assert arms.unit_kind("test_plane") == "aircraft" and arms.unit_kind("other") == ""
    guns = arms.guns("test_plane")
    assert [(g.blk, g.kind, g.calibre) for g in guns] == [("gunm2.blk", "gun", 12.7), ("us_500lb.blk", "bomb", 360.0),
                                                         ("us_aim9b.blk", "rocket", 127.0)]
    mg = guns[0]
    assert mg.machine_gun and mg.fires_bullets and not mg.explosive
    assert mg.belts == {"": ["ap_i_t_ball_m20", "ap_ball_m2"], "50cal_universal": ["ap_i_ball_m8", "ap_i_t_ball_m20"],
                        "50cal_stealth": ["ap_i_ball_m8"]}
    assert guns[1].shells == {"us_500lb": ("bomb", 360.0)} and guns[2].shells == {"us_aim9b": ("AAM", 127.0)}
    assert not guns[1].machine_gun and guns[2].explosive


def test_a_belt_is_named_where_the_kills_leave_one():
    arms = arsenal.Arsenal(_aircraft_archive())
    row = lambda name: {"Vehicle": "test_plane", "calibre": 12.7, "ammoSource": "recorded" if name else "calibre",
                        "ammoName": name}
    hits = [(1, 7, 1.0, "", row("ap_i_ball_m8"), False), (1, 7, 2.0, "", row(""), False),
            (1, 8, 3.0, "", row("ap_i_t_ball_m20"), False)]
    got = convert._belts(hits, arms)
    # Shooter 7's kill round is in two belts (universal, stealth): none; shooter 8's in two as well.
    assert got["beltsNamed"] == 0 and "ammoBelt" not in hits[1][4]
    hits.append((1, 7, 4.0, "", row("ap_i_t_ball_m20"), False))
    got = convert._belts(hits, arms)
    assert got["beltsNamed"] == 1 and hits[1][4]["ammoBelt"] == "50cal_universal" and "ammoBelt" not in hits[2][4]


def test_signatures_take_the_one_calibre_every_vehicle_can_fire():
    got = convert._signature_calibres({("a", "s1"): {12.7, 20.0}, ("b", "s1"): {12.7}, ("a", "s2"): {12.7, 20.0}})
    assert got == {"s1": 12.7, "s2": 20.0}


@pytest.mark.parametrize("part, group", [
    ("fuse1_dm", "airframe"), ("wing_l_dm", "airframe"), ("wingcontrol_l_dm", "controls"), ("aileron_r_dm", "controls"),
    ("tank2_dm", "fuel"), ("oil1_dm", "engine"), ("water1_dm", "engine"), ("gun3_dm", "gun"), ("gear_r_dm", "gear"),
    ("pilot_dm", "crew"), ("gunner4_dm", "crew"), ("track_l_dm", "tracks"), ("turret_front_dm", "armour"),
])
def test_aircraft_part_groups(part, group):
    assert damage_parts.part_group(part) == group


def test_a_destroyed_module_goes_on_the_hit_and_stands_for_an_aircrafts_damaged_parts(tmp_path, monkeypatch):
    """No 0xF13A for the unit (an aircraft gets none): the modules its hit destroyed (0xF118) are its damaged parts."""
    po = _order({"engine_dm"})
    po._global = ["default", "body_front", "turret_front", "engine", "pilot", "wing_l"]
    monkeypatch.setattr(damage_parts.PartOrder, "from_game", classmethod(lambda cls, game=None, archive=None: po))
    kill = lambda part: b"\x02\x58" + synth.le(wrpl.PART_KILL, 2) + synth.id_fields(
        {1: (16, synth.le(177 | 0x800, 2)), 2: (16, synth.le(part, 2))})
    more = [synth.packet(4, 10900, synth.unit_message(3, 0xF0E9, synth.hit_effect(344, 7, (983, 328, -197),
                                                                                   part=synth.hit_part(5)))),
            synth.packet(4, 10920, kill(4)), synth.packet(4, 10920, kill(5))]
    f = tmp_path / "h.wrpl"
    f.write_bytes(battle_with_entities(more, version=101421))
    tpath, jpath = convert.convert([f], tmp_path / "out")
    shot = next(r for r in pq.read_table(tpath).to_pylist() if r["event"] == "shot")
    assert shot["hitPartName"] == "wing_l" and shot["hitPartNumber"] == 5
    assert shot["destroyedParts"] == "pilot,wing_l" and shot["damagedParts"] == "pilot_dm,wing_l_dm"
    assert shot["damagedFrom"] == "destroyed" and shot["crewDamaged"] == 1 and shot["damagedGroups"] == "airframe,crew"
