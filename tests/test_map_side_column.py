"""War Thunder's map side columns (convert.map_sides, mapside.py): synthetic battles only."""

from heat3d_ext_warthunder import convert, objectives


def battle(team_at_north: str, extra_far: bool = False):
    """Rows of a battle: team `team_at_north`'s tanks start at the north (data z +700), the other's at the south."""
    rows = []
    for team in ("1", "2"):
        z = 700.0 if team == team_at_north else -800.0
        for i in range(6):
            track = f"{team}-{i}"
            rows.append({"time": i * 0.5, "track": track, "team": team, "x": 100.0 + i, "z": z, "kind": "tank", "isPlayer": True})
            rows.append({"time": 60.0 + i, "track": track, "team": team, "x": 0.0, "z": 0.0, "kind": "tank", "isPlayer": True})
        if extra_far:  # rockets fired from far east, aircraft spawning at the map's edge: no spawns
            for i in range(20):
                rows.append({"time": 2.0, "track": f"{team}-r{i}", "team": team, "x": 9000.0, "z": 0.0, "kind": "rocket", "isPlayer": True})
    rows.append({"time": 1.0, "track": "", "team": "", "x": 5.0, "z": 5.0, "kind": "effect", "isPlayer": False})
    return rows


def test_every_row_gets_its_team_side_south_first():
    # The viewer's world is south = -z (flipZ): data z -800 is the south.
    for north in ("1", "2"):
        rows = battle(north, extra_far=True)
        check = convert.map_sides(rows, [], "ground", {})
        south = "2" if north == "1" else "1"
        assert check["side1"] == [south] and check["side2"] == [north]
        assert {r["mapSide"] for r in rows if r["team"] == south} == {1}
        assert {r["mapSideFrom"] for r in rows if r["team"]} == {"spawn"}
        assert rows[-1]["mapSide"] == 0 and rows[-1]["mapSideFrom"] == "unknown"


def test_the_mission_spawn_areas_used_give_the_line():
    rows = battle("1")
    objs = [
        {"type": "spawn", "source": "mission", "name": "t1_tankSpawn01_zone01", "team": 1, "position": [100.0, 0.0, 700.0], "used": 6},
        {"type": "spawn", "source": "mission", "name": "t2_tankSpawn01_zone01", "team": 2, "position": [100.0, 0.0, -800.0], "used": 6},
        # A layout the battle did not use, and an aircraft spawn: left out.
        {"type": "spawn", "source": "mission", "name": "t1_tankSpawn02_zone01", "team": 1, "position": [-9000.0, 0.0, 0.0], "used": 0},
        {"type": "spawn", "source": "mission", "name": "t1_air_spawn_top", "team": 1, "position": [20000.0, 500.0, 0.0], "used": 2},
    ]
    assert convert.mission_line(objs, "ground") == (0.0, 1500.0)
    teams = {"from": "spawns", "swapped": False}
    check = convert.map_sides(rows, objs, "ground", teams)
    assert check["line"].startswith("the mission") and check["held"] == "north"
    assert check["missionTeam1Side"] == 2 and check["side1"] == ["2"] and check["agreesWithSpawnAreas"] is True


def test_without_spawn_areas_named_objectives_decide_the_swap():
    # Team 2 started near the mission's t1 airfield: the sides are swapped.
    objs = [{"type": "airfield", "name": "t1_airfield", "team": 1, "position": [0.0, 0.0, 900.0]},
            {"type": "airfield", "name": "t2_airfield", "team": 2, "position": [0.0, 0.0, -900.0]},
            {"type": "capture_zone", "name": "cz_a", "team": None, "position": [0.0, 0.0, 0.0]}]
    starts = [("2", 0.0, 0.0, 700.0), ("2", 5.0, 0.0, 710.0), ("1", 0.0, 0.0, -800.0)]
    got = objectives.replay_teams(objs, starts)
    assert got["swapped"] is True and got["from"] == "named objectives"
    assert objs[0]["team"] == 2 and objs[0]["missionTeam"] == 1
    assert objectives.replay_teams([], starts)["from"] == "none"
