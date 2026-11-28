"""The content beside the maps: the catalogue of a built install, and the levels listed as maps."""

from __future__ import annotations

import json

import pytest

import levelsynth
from heat3d_ext_warthunder import catalog, standalone_spec


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "appdata"))
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "appdata"))
    monkeypatch.setenv("HEAT3D_WT_NO_NAMES", "1")


def _game(tmp_path):
    game = tmp_path / "game"
    (game / "levels").mkdir(parents=True)
    wpcost = ("", [], [
        ("tank_a", [("unitClass", "exp_tank"), ("country", "country_usa"), ("rank", 2), ("economicRankHistorical", 6)],
         [("modifications", [], [("new_tank_traks", [], []), ("tank_ammo_belt", [], [])])]),
        ("rifle_x", [("unitClass", "exp_human"), ("country", "country_ussr"), ("rank", 5)],
         [("weapons", [], [("rifle_x_default", [], []), ("rifle_x_preset_2", [], []), ("custom_presets", [], []),
                           ("fpv_drone", [], []), ("medic_box", [], []), ("rpg_default", [], [])]),
          ("modifications", [], [("scope_a", [], []), ("bulletproof_vest_light", [], [])])]),
    ])
    gun = ("", [], [("bullet", [("bulletName", "75mm_ap"), ("caliber", 0.075), ("bulletType", "ap_tank")], []),
                    ("bullet", [("bulletName", "75mm_he"), ("caliber", 0.075)], [])])
    aces = {
        "gamedata/units/tankmodels/tank_a.blk": levelsynth.blk(("", [("model", "tank_a"), ("type", "typeTank")], [])),
        "gamedata/units/tankmodels/ai_truck.blk": levelsynth.blk(("", [("model", "truck")], [])),
        "gamedata/flightmodels/heli_h.blk": levelsynth.blk(("", [("model", "heli")], [("helicopter", [], [])])),
        "gamedata/units/humans/rifle_x.blk": levelsynth.blk(("", [("subclass", "human")], [])),
        "gamedata/weapons/groundmodels_weapons/75mm_gun.blk": levelsynth.blk(gun),
        "gamedata/weapons/human_weapons/rifle_x.blk": levelsynth.blk(("", [], [])),
    }
    missions = {
        "gamedata/missions/cta/tanks/lvl_a_dom.blk": levelsynth.blk(
            ("", [], [("mission_settings", [], [("mission", [("level", "levels/lvl_a.bin")], [])])])),
    }
    (game / "aces.vromfs.bin").write_bytes(levelsynth.vromfs(aces))
    (game / "char.vromfs.bin").write_bytes(levelsynth.vromfs({"config/wpcost.blk": levelsynth.blk(wpcost)}))
    (game / "mis.vromfs.bin").write_bytes(levelsynth.vromfs(missions))
    for name in ("lvl_a", "hangar_field", "firing_range", "lvl_tutorial"):
        (game / "levels" / f"{name}.bin").write_bytes(b"DBLD3x64")
    return game


def test_install_items_by_kind(tmp_path):
    items = catalog.install_items(_game(tmp_path))
    assert items["vehicle"] == ["ai_truck", "heli_h", "tank_a"]
    assert items["operator"] == ["rifle_x"]
    assert items["weapon"] == ["75mm_gun", "rifle_x"]
    assert items["ammo"] == ["75mm_ap", "75mm_he"]
    # A squad's own presets and shared ones are weapons, not equipment.
    assert items["gadget"] == ["fpv_drone", "medic_box"]
    assert items["modification"] == ["bulletproof_vest_light", "new_tank_traks", "scope_a", "tank_ammo_belt"]


def test_catalogue_round_trip(tmp_path):
    game = _game(tmp_path)
    out = tmp_path / "levels" / "warthunder"
    pack = tmp_path / "levels" / "model-packs" / "warthunder"
    pack.mkdir(parents=True)
    (pack / "model-pack.json").write_text(json.dumps({"units": {"tank_a": {"file": "tank_a.glb"}}}), encoding="utf-8")
    dest = catalog.build(game, out)
    doc = json.loads(dest.read_text(encoding="utf-8"))
    assert doc["format"] == "3dheat-catalog" and doc["game"] == "warthunder"
    by = {(i["kind"], i["id"]): i for i in doc["items"]}
    tank = by[("vehicle", "tank_a")]
    assert tank["domain"] == "ground" and tank["class"] == "tank" and tank["nation"] == "usa"
    assert tank["br"]["rb"] == 3.0 and tank["model"] == "model-packs/warthunder/tank_a.glb"
    assert by[("vehicle", "heli_h")]["type"] == "helicopter"
    assert by[("operator", "rifle_x")]["domain"] == "infantry"
    assert by[("ammo", "75mm_ap")]["calibre"] == 75.0
    assert by[("gadget", "fpv_drone")]["units"] == 1
    # What was written is what the install holds: nothing new, nothing gone.
    assert catalog.extracted_items(out) == catalog.install_items(game)


def test_maps_are_the_levels_battles_are_played_on(tmp_path):
    game = _game(tmp_path)
    assert [m.id for m in standalone_spec._maps(game)] == ["lvl_a"]
    # Unreadable missions: every level but the hangars and test ranges.
    (game / "mis.vromfs.bin").unlink()
    assert [m.id for m in standalone_spec._maps(game)] == ["lvl_a", "lvl_tutorial"]


def test_content_outputs():
    from pathlib import Path

    out = Path("levels") / "warthunder"
    m = standalone_spec.MapSource("lvl_a", "lvl_a", [])
    assert standalone_spec._existing(out, m) == [out / "lvl_a" / "lvl_a.glb"]
    if standalone_spec._HAS_KIND:
        c = standalone_spec.MapSource("catalog", "catalog", [], kind="catalog")
        assert standalone_spec._existing(out, c) == [out / "catalog.json"]
