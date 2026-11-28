"""
The map side of each row's team: `mapSide` and `mapSideFrom`, the same rule in every 3DHeat replay converter and in
the viewer (`src/data/teamSides.ts`), so that laid over each other, side 1 is the same side of a map in every match.

Many games number a match's teams without regard to the map (War Thunder hands a mission's two sides to its teams
either way, match by match; World of Warships names them by the recording player, ally and enemy; a Counter-Strike
clan changes ends at half time). The converter adds, per row:

* `mapSide` - 1 or 2, the side of the map the row's team plays this match (or this round, where the table has
  rounds); 0 where the row has no team or the side cannot be told.
* `mapSideFrom` - how it was found:
  * `spawn`: from where the two teams' units first appear in the match or round (their spawn, below);
  * `declared`: the team states its side (attack or defence, a coalition): `mapSide` follows that statement, the
    same number for the same statement in every match (`DECLARED`);
  * `unknown`: no side (`mapSide` 0): no team, a third team, a match or round without exactly two, no positions.

The team the game gave each row stays as it was (`team`).

The spawn rule
--------------
The table's parts are its matches (the session column) or, where it has a round column (`round`, `roundNumber`,
...; the viewer reads the same names) and some match in the file has more than one round, each match's rounds.
In each part:

1. each person's first row (the earliest time; the first in the file on a tie) is where they spawned. Rows of no
   team (`0`, empty, `none`, `unknown`, `null`, `-1`) and rows without a finite position are then left out;
2. with exactly two teams left, a team's spawn is the median of its persons' first east and of their first north
   positions (the upper median: sorted, the value at index n // 2);
3. the line from one spawn to the other is held pointing north - or east, where it runs within 22.5 degrees of
   east and west. Side 1 is the team whose spawn lies first along it: the south team, or on a map whose spawns lie
   east and west, the west team. Side 2 is the other. (A line across the map's diagonal is held north: its south
   team is side 1. Of 346 War Thunder missions' spawn lines, 9 lie within 5 degrees of where the rule changes.)

A converter that knows the map's own spawn line (War Thunder: the mission's spawn areas) passes it as `axis`; the
two teams' spawns are then told apart by which lies first along it, so that a match whose players happened to use
the far spawn points of a team still gets the map's sides. Without it, the line is the match's own.

East and north are the viewer's: the table's axes as the converter's mapping hints (`axes`) put them into the
viewer's world (east = x, north = the ground's other axis, its sign as the flips say: the viewer's world has north
at -z). A table without positions gets `unknown` everywhere.

The viewer uses these columns where a table has them and works the same out itself for older tables (it then finds
each map's spawn line over all its loaded matches, held the same way). Teams whose names already say their side
(CT and T, attack and defence, red and blue) keep their names in the viewer; `mapSide` is written for them too.
"""

from __future__ import annotations

import math
import re
from typing import Any, Mapping, Sequence

import numpy as np

#: The columns this module writes.
SIDE, SIDE_FROM = "mapSide", "mapSideFrom"
#: Team labels that stand for no team (the viewer's `isUnassignedTeam`).
UNASSIGNED = frozenset({"0", "", "none", "unknown", "null", "-1", "nan"})
#: A round number column (the viewer's `ROUND_COLUMN`).
ROUND_COLUMN = re.compile(r"^(round|round.?num(ber)?|round.?index|round.?no)$", re.I)
#: The spawn line is held east (not north) when it runs within this angle of east and west (degrees).
EAST_WEST_DEG = 22.5
_FLAT = math.tan(math.radians(EAST_WEST_DEG))
#: Statements of a side and the number they get, the same in every converter: defence, blue, CT, Radiant 1.
DECLARED = {
    "defence": 1, "defense": 1, "defender": 1, "defenders": 1, "def": 1,
    "attack": 2, "attacker": 2, "attackers": 2, "atk": 2,
    "blue": 1, "red": 2,
    "ct": 1, "counter-terrorist": 1, "counter-terrorists": 1, "t": 2, "terrorist": 2, "terrorists": 2,
    "radiant": 1, "dire": 2,
}


def unassigned(label: Any) -> bool:
    """Whether a team label stands for no team."""
    if label is None:
        return True
    if isinstance(label, float) and not math.isfinite(label):
        return True
    return str(label).strip().lower() in UNASSIGNED


def _label(v: Any) -> str:
    """A team value as the viewer labels it (whole numbers without a decimal point)."""
    if isinstance(v, (float, np.floating)) and math.isfinite(v) and float(v).is_integer():
        return str(int(v))
    if isinstance(v, (np.integer,)):
        return str(int(v))
    return "" if v is None else str(v)


def world_ground(x: Sequence[float], y: Sequence[float], z: Sequence[float], axes: Mapping[str, Any]) -> tuple[np.ndarray, np.ndarray]:
    """The viewer's world east and south (its +z) of each row, from the table's x, y, z and the hints' `axes`."""
    fx = -1.0 if axes.get("flipX") else 1.0
    east = np.asarray(x, dtype=np.float64) * fx
    if axes.get("up", "y") == "z":
        south = np.asarray(y, dtype=np.float64) * (-1.0 if axes.get("flipY") else 1.0)
    else:
        south = np.asarray(z, dtype=np.float64) * (-1.0 if axes.get("flipZ") else 1.0)
    return east, south


def orient(axis: tuple[float, float]) -> tuple[float, float]:
    """A spawn line (east, south) held pointing north (-south), or east where it runs within 22.5 degrees of east-west."""
    ax, az = float(axis[0]), float(axis[1])
    east_west = abs(az) <= _FLAT * abs(ax)
    if (ax < 0) if east_west else (az > 0):
        ax, az = -ax, -az
    return ax, az


def side_one_first(ca: tuple[float, float], cb: tuple[float, float], axis: tuple[float, float] | None = None) -> bool:
    """
    Whether spawn `ca` (east, south) is side 1 against spawn `cb`: it lies first along the spawn line (`axis`, else the
    line from one to the other) held as `orient` holds it. A tie keeps `ca` first.
    """
    ox, oz = orient(axis if axis is not None else (cb[0] - ca[0], cb[1] - ca[1]))
    return ca[0] * ox + ca[1] * oz <= cb[0] * ox + cb[1] * oz


def _parts(session: np.ndarray, rounds: np.ndarray | None) -> np.ndarray:
    """Each row's part: its session, or its session and round where some session has more than one round."""
    _, sid = np.unique(session, return_inverse=True)
    if rounds is None:
        return sid
    r = np.asarray(rounds, dtype=np.float64)
    key = np.where(np.isfinite(r), np.round(r) + 1, 0)
    pairs = np.stack([sid.astype(np.float64), key], axis=1)
    _, part = np.unique(pairs, axis=0, return_inverse=True)
    part = part.reshape(-1)
    if len(np.unique(part)) <= len(np.unique(sid)):
        return sid
    return part


def map_sides(
    session: Sequence[Any] | None,
    person: Sequence[Any],
    team: Sequence[Any],
    east: np.ndarray,
    south: np.ndarray,
    time: Sequence[float] | None = None,
    rounds: Sequence[float] | None = None,
    axis: tuple[float, float] | None = None,
    spawn_rows: Sequence[bool] | None = None,
) -> tuple[np.ndarray, list[str]]:
    """
    `mapSide` (int8) and `mapSideFrom` of every row by the spawn rule (see the top). `east` and `south` are the
    viewer's world ground positions (`world_ground`); `session` None is one match. `axis` the map's own spawn line
    (east, south), where the converter knows it. `spawn_rows`: the rows that can show a spawn (a game's units, not
    its projectiles); all where None. Every row of a team gets its side either way.
    """
    n = len(team)
    side = np.zeros(n, dtype=np.int8)
    fro = ["unknown"] * n
    if n == 0:
        return side, fro
    sess = np.zeros(n, dtype=np.int64) if session is None else np.asarray([_label(s) for s in session], dtype=object)
    part = _parts(sess, None if rounds is None else np.asarray(rounds, dtype=np.float64))
    labels = np.asarray([_label(t) for t in team], dtype=object)
    _, pid = np.unique(np.asarray([_label(p) for p in person], dtype=object), return_inverse=True)
    order = np.arange(n)
    if time is not None:
        t = np.asarray(time, dtype=np.float64)
        t = np.where(np.isnan(t), np.inf, t)
        order = np.lexsort((order, t))
    # The first row of each (part, person) in time order.
    key = part.astype(np.int64) * (int(pid.max()) + 1) + pid
    if spawn_rows is not None:
        order = order[np.asarray(spawn_rows, dtype=bool)[order]]
    _, first_at = np.unique(key[order], return_index=True)
    first = order[first_at]
    spawns: dict[int, dict[str, tuple[list[float], list[float]]]] = {}
    for r in first:
        lab = labels[r]
        if unassigned(lab):
            continue
        ex, so = east[r], south[r]
        if not (math.isfinite(ex) and math.isfinite(so)):
            continue
        xs, zs = spawns.setdefault(int(part[r]), {}).setdefault(lab, ([], []))
        xs.append(float(ex))
        zs.append(float(so))
    names, tid = np.unique(labels, return_inverse=True)
    code = {str(v): i for i, v in enumerate(names)}
    lookup = np.zeros((int(part.max()) + 1, len(names)), dtype=np.int8)
    for p, teams in spawns.items():
        if len(teams) != 2:
            continue
        a, b = sorted(teams)
        med = lambda v: sorted(v)[len(v) // 2]  # noqa: E731 - the viewer's median
        ca = (med(teams[a][0]), med(teams[a][1]))
        cb = (med(teams[b][0]), med(teams[b][1]))
        one, two = (a, b) if side_one_first(ca, cb, axis) else (b, a)
        lookup[p, code[one]] = 1
        lookup[p, code[two]] = 2
    side = lookup[part, tid.reshape(-1)]
    fro = np.where(side > 0, "spawn", "unknown").tolist()
    return side, fro


def declared_sides(statement: Sequence[Any], table: Mapping[str, int] = DECLARED) -> tuple[np.ndarray, list[str]]:
    """`mapSide` and `mapSideFrom` from each row's own statement of its side (attack, defence, red, blue...)."""
    side = np.zeros(len(statement), dtype=np.int8)
    fro = ["unknown"] * len(statement)
    for i, v in enumerate(statement):
        s = table.get(str(v if v is not None else "").strip().lower())
        if s:
            side[i] = s
            fro[i] = "declared"
    return side, fro


def round_column(names: Sequence[str]) -> str | None:
    """The table's round column by the viewer's names, if it has one."""
    return next((c for c in names if ROUND_COLUMN.match(c)), None)


def for_columns(cols: Mapping[str, Sequence[Any]], hints: Mapping[str, Any], declared: str | None = None,
                table: Mapping[str, int] = DECLARED) -> tuple[np.ndarray, list[str]]:
    """
    `mapSide` and `mapSideFrom` for a table given as columns by name, its columns and axes read from the mapping
    hints the converter writes for the viewer (`personId`, `teamId`, `sessionId`, `x`/`y`/`z`, `time`). With
    `declared` a column naming each row's side (attack / defence...), the side is that statement's.
    """
    if declared is not None:
        return declared_sides(cols[declared], table)
    c = hints.get("columns", {})
    n = len(cols[c["teamId"]])
    if not all(k in c and c[k] in cols for k in ("x", "y", "z")):
        return np.zeros(n, dtype=np.int8), ["unknown"] * n
    east, south = world_ground(cols[c["x"]], cols[c["y"]], cols[c["z"]], hints.get("axes", {}))
    rc = round_column(list(cols))
    return map_sides(
        cols.get(c.get("sessionId", "")) if c.get("sessionId") in cols else None,
        cols[c["personId"]],
        cols[c["teamId"]],
        east,
        south,
        cols.get(c.get("time", "")) if c.get("time") in cols else None,
        cols[rc] if rc else None,
    )


def add_to_table(table: Any, hints: Mapping[str, Any], declared: str | None = None,
                 table_of: Mapping[str, int] = DECLARED) -> Any:
    """A pyarrow table with `mapSide` (int8) and `mapSideFrom` (string) appended (replaced where it had them)."""
    import pyarrow as pa

    c = hints.get("columns", {})
    want = [c.get(k) for k in ("sessionId", "personId", "teamId", "x", "y", "z", "time")]
    rc = round_column(table.column_names)
    names = {w for w in want + [rc, declared] if w and w in table.column_names}
    cols = {k: table.column(k).to_numpy(zero_copy_only=False) for k in names}
    side, fro = for_columns(cols, hints, declared, table_of)
    for name in (SIDE, SIDE_FROM):
        if name in table.column_names:
            table = table.drop([name])
    table = table.append_column(SIDE, pa.array(side, type=pa.int8()))
    return table.append_column(SIDE_FROM, pa.array(fro, type=pa.string()))
