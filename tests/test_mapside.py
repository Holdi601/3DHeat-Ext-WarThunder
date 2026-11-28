"""The map side rule (mapside.py), the same in every 3DHeat replay converter: synthetic matches only."""

import numpy as np
import pytest

try:  # a converter's copy sits in its package, the kit's beside its tests
    from mapside import add_to_table, declared_sides, for_columns, map_sides, orient, side_one_first, world_ground
except ImportError:  # pragma: no cover - in a converter: <pkg>.mapside
    import importlib
    import pathlib
    import sys

    root = pathlib.Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root))
    pkg = next(p.parent.name for p in root.glob("*/mapside.py"))
    m = importlib.import_module(f"{pkg}.mapside")
    add_to_table, declared_sides, for_columns = m.add_to_table, m.declared_sides, m.for_columns
    map_sides, orient, side_one_first, world_ground = m.map_sides, m.orient, m.side_one_first, m.world_ground


def match(a, b, n=4, team=("1", "2"), session="m1", rnd=None, t0=0.0):
    """`n` units of each team: team[0]'s first at spawn `a`, team[1]'s at `b` (east, south), then each moves."""
    rows = []
    for k, (tm, sp) in enumerate(zip(team, (a, b))):
        for i in range(n):
            p = f"{session}-{tm}-{i}"
            rows.append((session, p, tm, sp[0] + i, sp[1] - i, t0 + i * 0.1, rnd))
            rows.append((session, p, tm, 0.0, 0.0, t0 + 50 + i, rnd))  # later, in the middle of the map
    return rows


def run(rows, **kw):
    s, p, t, e, so, tm, r = zip(*rows)
    rounds = None if all(v is None for v in r) else [np.nan if v is None else v for v in r]
    return map_sides(list(s), list(p), list(t), np.array(e, float), np.array(so, float), list(tm), rounds, **kw)


def side_of(rows, side, team, session=None):
    return {int(v) for row, v in zip(rows, side) if row[2] == team and (session is None or row[0] == session)}


def test_east_west_spawns_west_team_is_side_1():
    rows = match((500, 30), (-500, -40))
    side, fro = run(rows)
    assert side_of(rows, side, "2") == {1} and side_of(rows, side, "1") == {2}
    assert set(fro) == {"spawn"}


def test_north_south_and_diagonal_spawns_south_team_is_side_1():
    # South is +south (the viewer's +z); north is -south.
    rows = match((40, -800), (-30, 700)) + match((-600, -650), (600, 650), session="m2")
    side, _ = run(rows)
    assert side_of(rows, side, "2", "m1") == {1}  # team 2 at south 700
    assert side_of(rows, side, "2", "m2") == {1}  # the diagonal: team 2 at the south-east


def test_orientation_boundary_is_22_5_degrees_from_east_west():
    assert orient((1.0, 0.4)) == (1.0, 0.4)  # 21.8 degrees: east
    assert orient((-1.0, 0.4))[0] > 0
    assert orient((1.0, 0.42))[1] < 0  # 22.8 degrees: north (-south)
    assert side_one_first((0, 10), (1, 0)) is True and side_one_first((1, 0), (0, 10)) is False


def test_each_round_is_lined_up_on_its_own():
    # Round 1: clan A at the west; round 2: the clans swap ends.
    rows = match((-900, 0), (900, 0), team=("A", "B"), rnd=1) + match((900, 0), (-900, 0), team=("A", "B"), rnd=2, t0=100)
    side, _ = run(rows)
    r1 = {int(v) for row, v in zip(rows, side) if row[2] == "A" and row[6] == 1}
    r2 = {int(v) for row, v in zip(rows, side) if row[2] == "A" and row[6] == 2}
    assert r1 == {1} and r2 == {2}


def test_no_team_third_team_and_one_team_get_unknown():
    rows = match((-900, 0), (900, 0)) + [("m1", "neutral", "0", 5.0, 5.0, 0.0, None)]
    side, fro = run(rows)
    assert side[-1] == 0 and fro[-1] == "unknown"
    three = match((-900, 0), (900, 0)) + [("m1", "x", "3", 0.0, 900.0, 0.0, None)]
    side, fro = run(three)
    assert not side.any() and set(fro) == {"unknown"}
    one = [r for r in match((-900, 0), (900, 0)) if r[2] == "1"]
    assert not run(one)[0].any()


def test_the_map_line_decides_where_the_match_line_would_not():
    # Team 1 used a spawn far to the east this match: its own line runs east-west, the map's runs north-south.
    rows = match((900, 100), (0, -150))
    assert side_of(rows, run(rows)[0], "1") == {2}  # by the match's line (15 degrees off east-west): team 2 is west
    side, _ = run(rows, axis=(0.0, -1.0))
    assert side_of(rows, side, "1") == {1}  # by the map's: team 1 is south


def test_spawn_rows_leave_projectiles_out_and_sides_go_to_every_row():
    rows = match((-900, 0), (900, 0))
    rows += [("m1", f"shell{i}", "1", 5000.0, 0.0, -1.0, None) for i in range(20)]  # team 1's shells far east
    s = np.array([not r[1].startswith("shell") for r in rows])
    side, _ = run(rows, spawn_rows=s)
    assert side_of(rows, side, "1") == {1}


def test_declared_sides():
    side, fro = declared_sides(["Attack", "defence", "", "RED", "blue", "ct", "T", "radiant", "Dire", None])
    assert side.tolist() == [2, 1, 0, 2, 1, 1, 2, 1, 2, 0]
    assert fro[2] == "unknown" and fro[0] == "declared"


def test_world_ground_follows_the_hints_axes():
    e, s = world_ground([1.0], [2.0], [3.0], {"up": "y", "flipZ": True})
    assert (e[0], s[0]) == (1.0, -3.0)
    e, s = world_ground([1.0], [2.0], [3.0], {"up": "z", "flipY": True, "flipX": True})
    assert (e[0], s[0]) == (-1.0, -2.0)


def test_for_columns_and_add_to_table():
    pa = pytest.importorskip("pyarrow")
    rows = match((-900, 0), (900, 0))
    cols = {"match": [r[0] for r in rows], "player": [r[1] for r in rows], "team": [r[2] for r in rows],
            "x": [r[3] for r in rows], "y": [-r[4] for r in rows], "z": [0.0] * len(rows), "time": [r[5] for r in rows]}
    hints = {"axes": {"up": "z", "flipY": True}, "columns": {"x": "x", "y": "y", "z": "z", "time": "time",
                                                             "personId": "player", "teamId": "team", "sessionId": "match"}}
    side, _ = for_columns(cols, hints)
    assert side_of(rows, side, "1") == {1}
    t = add_to_table(pa.table(cols), hints)
    assert t.column("mapSide").type == pa.int8() and t.column("mapSideFrom").to_pylist()[0] == "spawn"
    assert add_to_table(t, hints).num_columns == t.num_columns  # written again, not twice
