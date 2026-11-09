"""
The battle's objectives: capture zones, airfields, helipads, bases, spawns, battle areas, bombing targets - where
they are, their shape and team - and the capture zones' state over time.

Two sources, each named on every objective (`source`):

- `replay`: the mission's objects as the replay sends them. 0xD039 names them (`cz_circle_01`, `t1_airfield`)
  with the place the mission first gives them; the replicated objects (0xF02D / 0xF0AA, see wrpl.py) of kind 3
  carry each one's transform as it is now (a capture zone is moved from its template's place to this mode's zone
  at the start), in the same order; kind 5 is one capture zone each: field 2 its owner (0 none, 1, 2), field 67
  its capture progress (a signed byte, -100..100: positive towards team 2, negative towards team 1), field 69 its
  index (0 = A). Checked on the ground test battles: an owner change comes with the capturing players'
  `captureZone` count rising in the scoreboard at the same moment, and with a tank of that team inside the zone
  (`selfCheck.objectives`).
- `mission`: the mission file in your install (`mis.vromfs.bin`, read only) and the templates it imports: its
  areas (`Sphere`, `Cylinder`, `Box`, `Point`, each with its transform) classed by name. Areas of another mode of
  the same map (`conq_`, `dom_`, `bttl_`...) and of another difficulty (`_arcade`, `_realistic`, `_hardcore`)
  are left out. Spawn areas say how many tracks began in them (`used`).

Nothing here is drawn from code under another licence; the layouts were found on the test replays.
"""

from __future__ import annotations

import functools
import math
import re
import struct
from pathlib import Path
from typing import Any

#: Replicated objects: index = kind * KIND_SPAN + number.
KIND_SPAN = 2048
KIND_TRANSFORM = 3
KIND_ZONE = 5

#: Area classes by name (first match wins); None: not an objective (briefing markers, AA gun points, decor).
_CLASSES = (
    (re.compile(r"^briefing|aaa_point|^sample_|detection_area|_exclude|exclude_|gun_pit"), None),
    (re.compile(r"capture_area|capture_zone|^cz_"), "capture_zone"),
    (re.compile(r"battle_?area"), "battle_area"),
    (re.compile(r"bomb_zone|bombing|bomb_target"), "bombing_target"),
    (re.compile(r"exit_zone"), "exit_zone"),
    (re.compile(r"killarea|kill_area"), "kill_area"),
    (re.compile(r"rearm"), "rearm_zone"),
    (re.compile(r"_road_\d+_spawn|convoy"), "convoy_spawn"),
    (re.compile(r"spawn"), "spawn"),
    (re.compile(r"airfield"), "airfield"),
    (re.compile(r"helipad"), "helipad"),
)
#: The modes whose areas carry their name in front (`conq_capture_area_02_arcade`).
_FAMILIES = ("conq", "dom", "bttl", "dbttl", "dbldom", "ctf", "br")
_VARIANT = re.compile(r"_(arcade|realistic|hardcore)$")
_TEAM = re.compile(r"(?:^|_)(?:t([12])|team([ab]))(?:_|$)")
_SPAWN_POINT = re.compile(r"^(.*)_spawnarea\d+$")
#: A spawn or airfield area wider than this (m) is the area the mission scatters them over.
CONTAINER = 5000.0
#: The difficulty's own areas first, then the next the mission scripts fall back to.
_PREFER = {"AB": ("arcade",), "RB": ("realistic", "hardcore"), "SB": ("hardcore", "realistic")}


def classify(name: str) -> str | None:
    n = name.lower()
    for pattern, kind in _CLASSES:
        if pattern.search(n):
            return kind
    return None


def team_of(name: str) -> int | None:
    m = _TEAM.search(name.lower())
    if not m:
        return None
    return int(m.group(1)) if m.group(1) else (1 if m.group(2) == "a" else 2)


def shape(kind: str, tm: list[float]) -> dict[str, Any]:
    """An area's shape from its type and 4x3 transform (three axes, each as long as the area, then the place)."""
    axes = [tm[0:3], tm[3:6], tm[6:9]]
    size = [math.sqrt(sum(c * c for c in a)) for a in axes]
    pos = [round(float(c), 2) for c in tm[9:12]]
    heading = round(math.degrees(math.atan2(axes[2][0], axes[2][2])) % 360, 2) if size[2] else 0.0
    k = (kind or "").lower()
    if k == "sphere":
        return {"shape": "sphere", "position": pos, "radius": round(size[0], 2)}
    if k == "cylinder":
        return {"shape": "cylinder", "position": pos, "radius": round(size[0], 2), "height": round(size[1], 2)}
    if k == "box":
        return {"shape": "box", "position": pos, "size": [round(s, 2) for s in size], "heading": heading}
    return {"shape": "point", "position": pos, "radius": round(size[0], 2), "heading": heading}


# ---------------------------------------------------------------- the mission file


@functools.lru_cache(maxsize=4)
def _archive(game: str):
    from .vromfs import Vromfs

    path = Path(game) / "mis.vromfs.bin"
    return Vromfs(path) if path.is_file() else None


def find_mission(names: list[str], mission: str, game_mode: str) -> str | None:
    """The mission file `<mission>.blk` among the archive's names; of several, the one under the game mode's folder."""
    want = "/" + mission.lower() + ".blk"
    found = [n for n in names if n.lower().endswith(want)]
    folder = {"ground": "/tanks/", "air": "/planes/", "naval": "/ships/"}.get(game_mode, "")
    found.sort(key=lambda n: (folder not in n.lower(), len(n)))
    return found[0] if found else None


def mission_areas(game: str | None, mission: str, game_mode: str = "") -> tuple[list[dict[str, Any]], str]:
    """Every area of the mission file and the templates it imports (with `importAreas`), as (name, type, tm, file);
    and the mission file's name ("" when none is found)."""
    if not game or not mission:
        return [], ""
    try:
        arc = _archive(str(game))
    except Exception:  # an unreadable archive gives no mission areas, never a failed conversion
        return [], ""
    if arc is None:
        return [], ""
    files = {n.lower(): n for n in arc.files}
    top = find_mission(list(arc.files), mission, game_mode)
    if top is None:
        return [], ""
    out: list[dict[str, Any]] = []
    seen: set[str] = set()

    def load(name: str, depth: int) -> None:
        key = name.lower().replace("\\", "/")
        if key in seen or key not in files or depth > 8:
            return
        seen.add(key)
        try:
            blk = arc.blk(files[key])
        except Exception:
            return
        areas = blk.block("areas")
        for a in areas.blocks if areas else []:
            tm = a.get("tm")
            if isinstance(tm, list) and len(tm) == 12:
                out.append({"name": a.name, "type": a.get("type") or "", "tm": tm, "file": files[key]})
        imports = blk.block("imports")
        for rec in imports.blocks if imports else []:
            if rec.get("file") and rec.get("importAreas", True):
                load(str(rec.get("file")), depth + 1)

    load(top, 0)
    return out, top


def _family(mode: str) -> str:
    m = re.match(r"[a-z]+", mode.lower())
    return m.group(0) if m else ""


def mission_objectives(areas: list[dict[str, Any]], mode: str, difficulty: str) -> list[dict[str, Any]]:
    """The mission's areas that are objectives of this mode and difficulty; a spawn's numbered points as one."""
    fam = _family(mode)
    prefer = _PREFER.get(difficulty, ())
    kept: dict[str, dict[str, Any]] = {}
    variants: dict[str, set[str]] = {}
    for a in areas:
        name = a["name"]
        kind = classify(name)
        if kind is None or (abs(a["tm"][9]) < 1e-3 and abs(a["tm"][11]) < 1e-3):
            continue  # a template's area at the origin is placed by its importer, not here
        low = name.lower()
        other = next((f for f in _FAMILIES if low.startswith(f + "_")), None)
        if other is not None and fam and not fam.startswith(other):
            continue
        v = _VARIANT.search(low)
        base = low[: v.start()] if v else low
        variants.setdefault(base, set()).add(v.group(1) if v else "")
        kept.setdefault(f"{base}|{v.group(1) if v else ''}", {**a, "kind": kind, "base": base,
                                                              "variant": v.group(1) if v else ""})
    out: list[dict[str, Any]] = []
    groups: dict[str, dict[str, Any]] = {}
    for a in kept.values():
        have = variants[a["base"]]
        if a["variant"]:
            choice = next((p for p in prefer if p in have), None) if prefer else None
            if choice is not None and a["variant"] != choice:
                continue
        obj = {"type": a["kind"], "team": team_of(a["name"]), "name": a["name"], "source": "mission",
               "area": a["type"], **shape(a["type"], a["tm"])}
        if a["kind"] in ("spawn", "airfield") and (obj.get("radius") or 0) > CONTAINER:
            continue  # the area the mission scatters spawns or airfields over, not one of them
        if a["variant"]:
            obj["variant"] = a["variant"]
        point = _SPAWN_POINT.match(a["name"])
        if point and a["kind"] == "spawn":
            g = groups.get(point.group(1))
            if g is None:
                g = groups[point.group(1)] = {"type": "spawn", "team": team_of(point.group(1)), "name": point.group(1),
                                             "source": "mission", "shape": "points", "radius": obj["radius"],
                                             "points": []}
                out.append(g)
            g["points"].append(obj["position"])
            continue
        out.append(obj)
    for g in groups.values():
        n = len(g["points"])
        g["position"] = [round(sum(p[i] for p in g["points"]) / n, 2) for i in range(3)]
    return out


# ---------------------------------------------------------------- the replay


def _transform(raw: bytes) -> list[float] | None:
    if len(raw) < 48:
        return None
    v = list(struct.unpack_from("<12f", raw))
    return v if all(math.isfinite(x) and abs(x) < 1e7 for x in v) else None


def replay_objectives(reflection: list[tuple], objects: list[dict[str, Any]]) -> tuple[list[dict[str, Any]],
                                                                                    list[dict[str, Any]]]:
    """
    The mission objects the replay names (`objects`: 0xD039, in order) at their place as replicated (kind 3), and
    the capture zones' states (kind 5) as rows: (time, zone, owner, progress, ...). Returns (objectives, rows).
    """
    transforms: dict[int, list[float]] = {}
    states: list[tuple[float, int, dict[int, bytes]]] = []
    for t, _, oid, _, fields, _ in reflection:
        kind, n = divmod(oid, KIND_SPAN)
        if kind == KIND_TRANSFORM and 4 in fields and n not in transforms:
            tm = _transform(fields[4])
            if tm is not None:
                transforms[n] = tm
        elif kind == KIND_TRANSFORM and 4 in fields:
            tm = _transform(fields[4])
            if tm is not None and t < 60:  # the zones are placed at the start; later sends repeat it
                transforms[n] = tm
        elif kind == KIND_ZONE:
            states.append((t, n, fields))
    # Kind 3's numbers follow the named objects; one not moved lies where 0xD039 put it, which checks the order.
    named = [o for o in objects if o.get("pos")]
    out: list[dict[str, Any]] = []
    zones: list[dict[str, Any]] = []
    for i, o in enumerate(named):
        tm = transforms.get(i)
        model = o.get("model") or ""
        name = o["name"]
        low = (name + " " + model).lower()
        kind = ("capture_zone" if "capture_zone" in low or name.lower().startswith("cz_") else
                "airfield" if "airfield" in low or model.lower().startswith("dynaf") else
                "helipad" if "helipad" in low else
                "base" if model.lower().startswith("dynbase") else classify(name) or "object")
        pos = [round(c, 2) for c in tm[9:12]] if tm else o["pos"]
        obj: dict[str, Any] = {"type": kind, "team": team_of(name), "name": name, "source": "replay",
                               "object": name, "model": model, "shape": "point", "position": pos,
                               "moved": bool(tm) and math.dist(pos, o["pos"]) > 1.0}
        if tm:
            obj["scale"] = round(math.sqrt(sum(c * c for c in tm[0:3])), 4)
        if o.get("points"):
            obj["shape"], obj["points"] = "outline", o["points"]
        out.append(obj)
        if kind == "capture_zone":
            zones.append(obj)
    rows: list[dict[str, Any]] = []
    owner: dict[int, int] = {}
    for t, n, fields in states:
        if n >= len(zones):
            continue
        z = zones[n]
        if 69 in fields and fields[69]:
            z["index"] = fields[69][0]
        letter = chr(ord("A") + z.get("index", n)) if z.get("index", n) < 26 else str(n)
        z.setdefault("letter", letter)
        row: dict[str, Any] = {"time": round(t, 3), "zone": z["letter"], "zoneId": n, "object": z["name"]}
        if 2 in fields and fields[2]:
            row["owner"] = fields[2][0]
        if 67 in fields and fields[67]:
            row["progress"] = struct.unpack("<b", fields[67][:1])[0]
        prev = owner.get(n)
        if "owner" in row:
            if prev is None:
                z.setdefault("ownerAtStart", row["owner"])
                row["event"] = "state"
            elif row["owner"] != prev:
                row["event"] = "captured" if row["owner"] else "neutralised"
            else:
                row["event"] = "state"
            owner[n] = row["owner"]
        else:
            row["event"] = "progress"
        row["fields"] = {str(k): v.hex() for k, v in fields.items()}
        row["x"], row["y"], row["z"] = z["position"]
        rows.append(row)
    for n, z in enumerate(zones):
        z.setdefault("letter", chr(ord("A") + n))
        z["name"] = z["letter"]
        if n in owner:
            z["ownerAtEnd"] = owner[n]
    return out, rows


def match_zones(objectives: list[dict[str, Any]], areas: list[dict[str, Any]]) -> None:
    """A replay's zone gets the shape of the mission area it was moved to (the same place on the ground, 2 m)."""
    for z in objectives:
        if z["type"] != "capture_zone" or z["source"] != "replay":
            continue
        best = None
        for a in areas:
            if classify(a["name"]) != "capture_zone":
                continue
            d = math.hypot(a["tm"][9] - z["position"][0], a["tm"][11] - z["position"][2])
            if d <= 2.0 and (best is None or d < best[0]):
                best = (d, a)
        if best is not None:
            a = best[1]
            s = shape(a["type"], a["tm"])
            z.update({k: v for k, v in s.items() if k != "position"})
            z["area"] = a["name"]
            z["areaType"] = a["type"]


def spawn_use(objectives: list[dict[str, Any]], starts: list[tuple[str, float, float, float]],
              margin: float = 30.0) -> None:
    """How many tracks began in each spawn (`used`, and by team): a life's first sample within its radius and
    `margin` metres of the spawn's place or one of its points."""
    for o in objectives:
        if o["type"] not in ("spawn", "convoy_spawn"):
            continue
        pts = o.get("points") or [o["position"]]
        if (o.get("radius") or 0.0) > CONTAINER:
            continue
        reach = (o.get("radius") or 0.0) + margin
        used: dict[str, int] = {}
        for team, x, y, z in starts:
            if any(math.hypot(p[0] - x, p[2] - z) <= reach for p in pts):
                used[team or "?"] = used.get(team or "?", 0) + 1
        o["used"] = sum(used.values())
        if used:
            o["usedByTeam"] = used


def replay_teams(objectives: list[dict[str, Any]]) -> dict[str, int]:
    """
    The mission's sides (`t1_`, `t2_` in the names) as the replay's teams: a mission may swap them at random
    (`randomSpawnTeams`), so the spawns decide - when more tracks of team 2 began in the `t1_` spawns than of team
    1 (and the other way round), every objective's `team` is swapped and the name's kept as `missionTeam`.
    """
    same = swapped = 0
    for o in objectives:
        if o.get("team") in (1, 2) and o.get("usedByTeam"):
            for team, n in o["usedByTeam"].items():
                if team in ("1", "2"):
                    if int(team) == o["team"]:
                        same += n
                    else:
                        swapped += n
    swap = swapped > same
    for o in objectives:
        if o.get("team") in (1, 2):
            o["missionTeam"] = o["team"]
            if swap:
                o["team"] = 3 - o["team"]
    return {"spawnsSameTeam": same, "spawnsOtherTeam": swapped, "swapped": swap}
