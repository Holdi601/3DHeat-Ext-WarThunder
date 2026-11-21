"""Game-mode layouts from mission areas (layouts.py), on hand-made missions."""

from heat3d_ext_warthunder import layouts as L


def area(name, kind, x, z, sx=10.0, sz=10.0, y=50.0):
    return {"name": name, "type": kind, "tm": [sx, 0, 0, 0, 10.0, 0, 0, 0, sz, x, y, z], "points": [], "file": "m.blk",
            "tier": ""}


def test_outline_is_in_the_levels_frame():
    pts = L._outline(area("dom_battle_area", "Box", 100.0, 200.0, 40.0, 20.0))
    assert sorted((p[0], p[2]) for p in pts) == [(80.0, -210.0), (80.0, -190.0), (120.0, -210.0), (120.0, -190.0)]


def test_selects_the_difficultys_areas_and_names_the_rest():
    data = {"areas": [
        area("dom_capture_area_01_arcade", "Cylinder", 10, 10), area("dom_capture_area_01_realistic", "Cylinder", 11, 10),
        area("dom_capture_area_02_arcade", "Cylinder", 50, 10),
        area("conq_capture_area_01", "Cylinder", 90, 90),
        area("dom_battle_area_arcade", "Box", 30, 30, 400, 400),
        area("battlearea_exclude_01", "Box", 200, 200, 30, 30),
        area("t1_killarea", "Cylinder", 0, -150, 50, 50), area("t1_killarea_hardcore", "Cylinder", 0, -150, 60, 60),
        area("t1_tankSpawn01_zone01", "Sphere", 0, -150), area("t1_tankSpawn01_zone02", "Sphere", 5, -150),
        area("t2_air_spawn_top", "Sphere", 0, 900, 300, 300, 1500),
        area("briefing_dom_capture_area_01_arcade", "Point", 10, 10),
    ], "groups": [{"name": "t1_airfield", "class": "dynaf_x", "kind": "airfield", "tm": area("a", "Point", 5, 5)["tm"],
                   "army": 1, "tier": "low", "file": "m.blk"}], "squads": [], "settings": {}}
    ab = L.select(data, "gamedata/missions/cta/tanks/test/test_dom.blk", "AB")
    zones = [o for o in ab["objectives"] if o["type"] == "capture_zone"]
    assert [(z["letter"], z["position"][0]) for z in zones] == [("A", 10.0), ("B", 50.0)]
    assert [z["type"] for z in ab["zones"]] == ["play_area", "out_of_bounds", "out_of_bounds"]
    kill = [z for z in ab["zones"] if z.get("kind") == "spawn_kill_area"]
    assert len(kill) == 1 and kill[0]["team"] == 2
    assert {(s["base"], s["vehicle"], s["team"]) for s in ab["spawns"]} == {("tankSpawn01", "ground", 1),
                                                                         ("air_spawn_top", "aircraft", 2)}
    rb = L.select(data, "gamedata/missions/cta/tanks/test/test_dom.blk", "RB")
    assert [o["position"][0] for o in rb["objectives"] if o["type"] == "capture_zone"] == [11.0, 50.0]
    assert [o["tier"] for o in ab["objectives"] if o["type"] == "airfield"] == ["low"]


def test_mode_names():
    assert L.mode_name("99_testmap_conq2") == "Conquest 2"
    assert L.mode_name("99_testmap_dom") == "Domination"
    assert L.family("99_testmap_01_ndom") == "ndom"
