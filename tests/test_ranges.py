"""The range catalogue (ranges.py) on a small archive built in code; nothing here comes from the game."""

from __future__ import annotations

from heat3d_ext_warthunder.ranges import build, thermal_gen
from heat3d_ext_warthunder.vromfs import Blk


def B(name: str = "", params: dict | list | None = None, *blocks: Blk) -> Blk:
    items = list(params.items()) if isinstance(params, dict) else list(params or [])
    return Blk(name, items, list(blocks))


class Archive:
    def __init__(self, blks: dict[str, Blk]) -> None:
        self.blks = blks
        self.files = {k: b"" for k in blks}

    def blk(self, name: str) -> Blk:
        return self.blks[name]


def archive() -> Archive:
    gun = B("", {"cannon": True, "aimMaxDist": 2500.0},
            B("bullet", {"bulletName": "100mm_test_apds", "bulletType": "apds_tank", "caliber": 0.1, "speed": 1400.0, "maxDistance": 9000.0}),
            B("bullet", {"bulletName": "100mm_test_he", "bulletType": "he_frag_tank", "caliber": 0.1, "speed": 800.0, "maxDistance": 12000.0}))
    smoke = B("", {}, B("bullet", {"bulletName": "smoke_test", "bulletType": "smoke_grenade", "caliber": 0.08}))
    sam = B("", {}, B("bullet", {"bulletType": "sam_tank", "minimalAltitude": 20.0},
                      B("rocket", {"guidanceType": "saclos", "minDistance": 500.0, "maxDistance": 8000.0})))
    aam = B("", {}, B("rocket", {"bulletName": "test_aam", "bulletType": "aam", "guidanceType": "ir", "minDistance": 300.0,
                                 "maxDistance": 10000.0, "loadFactorMax": 30.0},
                      B("guidance", {"lockDistance": 6000.0}, B("irSeeker", {"angleMax": 40.0}))))
    pod = B("", {"container": True, "blk": "gamedata/weapons/rocketguns/test_aam.blk"})
    radar = B("", {"type": "radar", "name": "Test search radar"},
              B("transivers", {}, B("search", {"rcs": 5.0, "range": 20000.0}), B("gtm", {"rcs": 50.0, "range": 40000.0})),
              B("scanPatterns", {}, B("searchWide", {"azimuthLimits": [-180.0, 180.0], "elevationLimits": [-5.0, 70.0]})))
    track = B("", {"type": "radar", "name": "Test track radar"},
              B("transivers", {}, B("track", {"rcs": 5.0, "range": 15000.0, "visibilityType": "radar"}),
                B("tiny", {"range": 10.0})),
              B("scanPatterns", {}, B("lock", {"azimuthLimits": [-60.0, 60.0], "elevationLimits": [-5.0, 80.0]})))
    rwr = B("", {"type": "rwr", "name": "Test warner", "range": 50000.0},
            B("receivers", {}, B("receiver", {"azimuth": 0.0, "azimuthWidth": 180.0, "elevationWidth": 90.0}),
              B("receiver", {"azimuth": -180.0, "azimuthWidth": 180.0, "elevationWidth": 90.0})))
    tank = B("", {}, B("commonWeapons", {}, B("Weapon", {"blk": "gamedata/weapons/groundmodels_weapons/test_gun.blk"}),
                                            B("Weapon", {"blk": "gamedata/weapons/groundmodels_weapons/test_smoke.blk"}),
                                            B("Weapon", {"blk": "gamedata/weapons/groundmodels_weapons/test_sam.blk"})),
             B("sensors", {}, B("sensor", {"blk": "gamedata/sensors/test_search.blk"}), B("sensor", {"blk": "gamedata/sensors/test_track.blk"})),
             B("cockpit", {"zoomOutFov": 20.0, "zoomInFov": 5.0}),
             B("commanderView", {"zoomOutFov": 30.0, "zoomInFov": 10.0}),
             B("modifications", {}, B("night_vision_system", {}, B("effects", {}, B("nightVision", {},
                                      B("gunnerThermal", {"resolution": [800, 600]}), B("driverIr", {"resolution": [800, 600]})))),
               B("laser_rangefinder", {}, B("effects", {"rangefinderMounted": True, "isLaser": True,
                                                        "distanceThresholdMax": [1000.0, 5000.0, 9999.0]}))))
    plane = B("", {}, B("WeaponSlots", {}, B("WeaponSlot", {}, B("WeaponPreset", {}, B("Weapon", {"blk": "gamedata/weapons/containers/test_pod.blk"})))),
              B("sensors", {}, B("sensor", {"blk": "gamedata/sensors/test_rwr.blk"})),
              B("cockpit", {"sightOutFov": 4.0, "sightInFov": 1.0, "targetingPodFov": [3.0, 0.5]}),
              B("nightVision", {}, B("sightTPodThermal", {"resolution": [1200, 800]})))
    return Archive({
        "gamedata/units/tankmodels/test_tank.blk": tank,
        "gamedata/flightmodels/test_plane.blk": plane,
        "gamedata/weapons/groundmodels_weapons/test_gun.blk": gun,
        "gamedata/weapons/groundmodels_weapons/test_smoke.blk": smoke,
        "gamedata/weapons/groundmodels_weapons/test_sam.blk": sam,
        "gamedata/weapons/rocketguns/test_aam.blk": aam,
        "gamedata/weapons/containers/test_pod.blk": pod,
        "gamedata/sensors/test_search.blk": radar,
        "gamedata/sensors/test_track.blk": track,
        "gamedata/sensors/test_rwr.blk": rwr,
    })


def test_thermal_generations():
    assert [thermal_gen(r) for r in ([500, 300], [800, 600], [1200, 800], None)] == [1, 2, 3, None]


def test_catalogue_of_a_small_archive():
    doc = build(archive())
    assert doc["version"] == 1 and doc["game"] == "wt" and doc["source"] == "your installation"
    w = {x["id"]: x for x in doc["weapons"]}
    gun = w["local-wt-test_gun"]
    assert gun["cls"] == "gun" and gun["range"] == [0, 2500, 12000]
    assert {"test_gun", "100mm_test_apds", "100mm_test_he"} <= set(gun["labels"])
    assert "local-wt-test_smoke" not in w
    sam = w["local-wt-test_sam"]
    assert sam["cls"] == "sam" and sam["range"][0] == 500 and sam["range"][2] == 8000 and sam["alt"] == [20, 8000]
    aam = w["local-wt-test_aam"]
    assert aam["cls"] == "aam" and aam["range"] == [300, 6000, 10000] and aam["shape"] == "cone" and aam["cone"] == 40

    units = {u["names"][0]: u for u in doc["units"]}
    tank = units["test_tank"]
    assert tank["weapons"] == ["local-wt-test_gun", "local-wt-test_sam"]
    sensors = {s: doc["sensors"][s] for s in tank["sensors"]}
    kinds = sorted((s["kind"], s["name"], s["range"], s["mount"]) for s in sensors.values())
    assert kinds == [("lrf", "Laser rangefinder", 9999, "gun"), ("radar", "Test search radar", 20000, "hull"),
                     ("radar", "Test track radar", 15000, "turret")]
    search = next(s for s in sensors.values() if s["name"] == "Test search radar")
    assert search["az"] == [-180.0, 180.0] and search["el"] == [-5.0, 70.0] and search["rcsRef"] == 5.0 and "gmti" in search["modes"]
    optics = {o["who"]: o for o in tank["optics"]}
    assert optics["gunner"]["fov"] == [20.0, 5.0] and optics["gunner"]["thermal"]["gen"] == 2 and optics["gunner"]["mount"] == "gun"
    assert optics["commander"]["fov"] == [30.0, 10.0] and optics["commander"]["thermal"] is None
    assert optics["driver"]["nv"] is True

    plane = units["test_plane"]
    assert plane["weapons"] == ["local-wt-test_aam"]
    rwr = doc["sensors"][plane["sensors"][0]]
    assert rwr["kind"] == "rwr" and rwr["range"] == 50000 and rwr["az"] == [-180, 180]
    tgp = next(o for o in plane["optics"] if o["who"] == "tgp")
    assert tgp["fov"] == [3.0, 0.5] and tgp["thermal"]["gen"] == 3
