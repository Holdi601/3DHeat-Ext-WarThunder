"""
Each level's game-mode layouts from the missions in your install (`mis.vromfs.bin`, read only): for every
multiplayer mission played on a level, its capture zones, battle area and the ground excluded from it, the spawn
kill areas, the spawn points (ground, air, helicopter, naval, convoys), airfields, helipads, bases and bombing
targets - one layout per mission and difficulty (arcade, realistic, simulator; one layout where they agree). Where
the mission brings separate sets for battle-rating tiers (airfields, air spawns, bombing targets), each tier is a
stage of the layout, named in `stageNames`.

Written as `<Level>.layouts.json` in the viewer's layouts format (`format: 3dheat-layouts`), in the level's frame:
the glb's, so z is mirrored (glb (x, y, z) = game (x, y, -z), as `level.py` writes the level).

Shapes: a sphere or cylinder keeps its radius; a box or polygon becomes its outline; areas that are drawn as
ground (battle areas, excluded ground, kill areas) are outlines, a circle as a 48-sided one.
"""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Any

from .objectives import CONTAINER, _FAMILIES, _VARIANT, classify, team_of

FORMAT = "3dheat-layouts"
GAME = "warthunder"

#: The multiplayer missions: everything under `missions/cta/` that is a mission of its own, not a part or template.
_CTA = re.compile(r"^gamedata/missions/cta/")
_PART = re.compile(r"(^|/)template_|_part\.blk$|_template\.blk$|/templates/")
_TIER = re.compile(r"(?:^|[_/])(low|mid|high|top)(?:_ranks?)?(?:[_/.]|$)")
_RANK = re.compile(r"^rank_(\d+)_")
_ZONE_NO = re.compile(r"(?:capture_?(?:area|zone)|cz)_?(?:circle_)?(\d+)")
_SPAWN_GROUP = re.compile(r"(?:_zone|_spawnarea|_point|_pos)?_?\d+$")

#: Unit classes of `objectGroups` that are objectives.
_GROUPS = (
    (re.compile(r"^dynaf_|^dynAF_", re.I), "airfield"),
    (re.compile(r"^dynhelipad|helipad", re.I), "helipad"),
    (re.compile(r"bomb_target", re.I), "bombing_target"),
    (re.compile(r"^dynbase_|^dynport_|^dyn_sam_site", re.I), "base"),
)

#: What each family of mission is called (from the mission file's name).
_MODE_NAMES = {
    "dom": "Domination", "conq": "Conquest", "bttl": "Battle", "dbttl": "Battle (two zones)",
    "dbldom": "Double domination", "ctf": "Capture", "br": "Battle royale", "ndom": "Naval domination",
    "nconq": "Naval conquest", "nbttl": "Naval battle", "ntdm": "Naval team deathmatch", "bfd": "Air battle",
    "i2m": "Enduring confrontation", "n2m": "Enduring confrontation", "h2m": "Enduring confrontation",
    "gs": "Ground strike", "gsn": "Ground strike (naval)", "ad": "Air domination", "afd": "Air front",
    "aconq": "Air conquest", "infdom": "Infantry domination", "tdm": "Team deathmatch", "sead": "SEAD",
    "hs": "Helicopter strike", "ffa": "Free for all", "race": "Race", "norespawn": "Air battle",
}
#: Each difficulty's own areas first, then those the mission falls back to.
#: An area without a difficulty in its name ("") is the arcade one where others of its name have one.
_ORDER = {"AB": ("arcade", "", "realistic", "hardcore"), "RB": ("realistic", "hardcore", "", "arcade"),
          "SB": ("hardcore", "realistic", "", "arcade")}
_DIFFICULTY = {"AB": "arcade", "RB": "realistic", "SB": "simulator"}
CIRCLE = 48


# ---------------------------------------------------------------- the frame


def _p(x: float, y: float, z: float) -> list[float]:
    """A game position in the level's frame (z mirrored)."""
    return [round(float(x), 2), round(float(y), 2), round(-float(z), 2)]


def _heading(tm: list[float]) -> float:
    """The heading of the area's z axis in the level's frame (z mirrored: 180 - the game's)."""
    h = math.degrees(math.atan2(tm[6], tm[8]))
    return round((180.0 - h) % 360.0, 2)


def _size(tm: list[float]) -> list[float]:
    return [math.sqrt(sum(c * c for c in tm[i:i + 3])) for i in (0, 3, 6)]


def _outline(a: dict[str, Any]) -> list[list[float]]:
    """The area's ground outline in the level's frame: a box's corners, a polygon's points, a circle's."""
    tm = a["tm"]
    x, y, z = tm[9:12]
    kind = a["type"].lower()
    if kind == "polygon" and a.get("points"):
        return [_p(px, py, pz) for px, py, pz in a["points"]]
    if kind == "box":
        out = []
        for sx, sz in ((-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)):
            out.append(_p(x + sx * tm[0] + sz * tm[6], y, z + sx * tm[2] + sz * tm[8]))
        return out
    r = _size(tm)[0]
    return [_p(x + r * math.cos(2 * math.pi * i / CIRCLE), y, z + r * math.sin(2 * math.pi * i / CIRCLE))
            for i in range(CIRCLE)]


def _place(a: dict[str, Any]) -> dict[str, Any]:
    """An objective's place and shape: a radius for spheres and cylinders, an outline for boxes and polygons."""
    tm = a["tm"]
    kind = a["type"].lower()
    size = _size(tm)
    out: dict[str, Any] = {"position": _p(*tm[9:12])}
    if kind in ("box", "polygon"):
        out["shape"] = "outline"
        out["points"] = _outline(a)
        if kind == "box":
            out["size"] = [round(s, 2) for s in size]
            out["heading"] = _heading(tm)
    elif kind in ("sphere", "cylinder"):
        out["shape"] = kind
        out["radius"] = round(size[0], 2)
        if kind == "cylinder":
            out["height"] = round(size[1], 2)
    else:
        out["shape"] = "point"
        out["heading"] = _heading(tm)
    return out


# ---------------------------------------------------------------- the archive


def mission_index(arc) -> dict[str, list[str]]:
    """The multiplayer missions of every level, by level name (`99_testmap`): the files not imported by another."""
    by_level: dict[str, list[str]] = {}
    imported: set[str] = set()
    levels: dict[str, str] = {}
    for f in arc.files:
        low = f.lower()
        if not low.endswith(".blk") or not _CTA.match(low):
            continue
        try:
            blk = arc.blk(f)
        except Exception:
            continue
        imports = blk.block("imports")
        for rec in imports.blocks if imports else []:
            if rec.get("file"):
                imported.add(str(rec.get("file")).lower().replace("\\", "/"))
        ms = blk.block("mission_settings")
        m = ms.block("mission") if ms else None
        level = m.get("level") if m else None
        if level and not _PART.search(low):
            levels[f] = Path(str(level).replace("\\", "/")).stem
    for f, level in levels.items():
        if f.lower() not in imported:
            by_level.setdefault(level, []).append(f)
    for v in by_level.values():
        v.sort()
    return by_level


def collect(arc, top: str) -> dict[str, Any]:
    """The mission's areas, objective groups and area squads, with those of the files it imports."""
    files = {n.lower(): n for n in arc.files}
    areas: list[dict[str, Any]] = []
    groups: list[dict[str, Any]] = []
    squads: list[dict[str, Any]] = []
    seen: set[str] = set()
    settings: dict[str, Any] = {}

    def load(name: str, depth: int, want_areas: bool, want_units: bool) -> None:
        key = name.lower().replace("\\", "/")
        if key in seen or key not in files or depth > 8:
            return
        seen.add(key)
        try:
            blk = arc.blk(files[key])
        except Exception:
            return
        tier = _TIER.search(key.rsplit("/", 1)[-1])
        tier = tier.group(1) if tier else ""
        if depth == 0:
            ms = blk.block("mission_settings")
            m = ms.block("mission") if ms else None
            if m:
                settings.update({k: m.get(k) for k in ("level", "type", "postfix", "locName", "randomSpawnTeams")})
        if want_areas:
            block = blk.block("areas")
            for a in block.blocks if block else []:
                tm = a.get("tm")
                if not (isinstance(tm, list) and len(tm) == 12):
                    continue
                pts = [v for k, v in a.params if k == "polygonPoint" and isinstance(v, list) and len(v) == 3]
                areas.append({"name": a.name, "type": a.get("type") or "", "tm": tm, "points": pts,
                              "file": files[key], "tier": tier})
        if want_units:
            block = blk.block("units")
            for u in block.blocks if block else []:
                tm = u.get("tm")
                props = u.block("props")
                if u.name == "objectGroups" and isinstance(tm, list) and len(tm) == 12:
                    cls = str(u.get("unit_class") or "")
                    kind = next((k for p, k in _GROUPS if p.search(cls)), None)
                    if kind:
                        groups.append({"name": str(u.get("name") or ""), "class": cls, "kind": kind, "tm": tm,
                                       "army": props.get("army") if props else None, "tier": tier,
                                       "file": files[key]})
                elif u.name == "area_squad" and props:
                    members = [str(v) for k, v in props.params if k == "squad_members"]
                    squads.append({"name": str(u.get("name") or ""), "members": members})
        imports = blk.block("imports")
        for rec in imports.blocks if imports else []:
            if rec.get("file"):
                load(str(rec.get("file")), depth + 1, bool(rec.get("importAreas", True)),
                     bool(rec.get("importUnits", True)))

    load(top, 0, True, True)
    return {"areas": areas, "groups": groups, "squads": squads, "settings": settings}


# ---------------------------------------------------------------- one mission


def family(stem: str) -> str:
    """The mission's family from its file name (`99_testmap_conq2` -> `conq`), "" when it says none."""
    parts = stem.lower().split("_")
    for p in reversed(parts):
        bare = re.sub(r"\d+$", "", p)
        if bare in _MODE_NAMES:
            return bare
    return ""


def mode_name(stem: str) -> str:
    fam = family(stem)
    m = re.search(rf"_{fam}(\d+)(?:_|$)", stem.lower()) if fam else None
    base = _MODE_NAMES.get(fam, stem)
    return f"{base} {m.group(1)}" if m else base


def kind_of(name: str) -> str | None:
    """What an area is in a layout: the replay reader's classes, and the ground the battle excludes."""
    n = name.lower()
    if n.startswith(("briefing", "brief_")) or "aaa_point" in n or "detection_area" in n:
        return None
    if "battlearea_exclude" in n or "battle_area_exclude" in n or re.search(r"(^|_)exclude", n):
        return "excluded"
    if re.search(r"battle_?zone", n):
        return "battle_area"
    if "kill_area" in n or "killarea" in n:
        return "kill_area"
    return classify(name)


def _vehicle(name: str, default: str = "ground") -> str:
    n = name.lower()
    if re.search(r"heli", n):
        return "helicopter"
    if re.search(r"air|bomber|fighter|plane|interceptor|assault", n):
        return "aircraft"
    if re.search(r"boat|ship|naval", n):
        return "ship"
    if re.search(r"road|convoy", n):
        return "convoy"
    if re.search(r"tank", n):
        return "ground"
    return default


def _group(name: str) -> str:
    """A spawn point's group: its name without the team and its number (`t1_tankSpawn01_zone03` -> `tankSpawn01`)."""
    n = re.sub(r"^(?:[a-z]+_)?t[12]_|^team[ab]_", "", name, flags=re.I)
    n = _VARIANT.sub("", n)
    n = re.sub(r"_(?:zone|spawnarea|spawnsphere|sphere|point|pos|icon)\d+$", "", n, flags=re.I)
    return n


def _letter(name: str, fallback: int) -> str:
    m = _ZONE_NO.search(name.lower())
    i = int(m.group(1)) - 1 if m else fallback
    return chr(ord("A") + i) if 0 <= i < 26 else str(i + 1)


def _tier_of(a: dict[str, Any]) -> str:
    m = _RANK.match(a["name"].lower())
    if m:
        return f"rank {int(m.group(1))}"
    t = a.get("tier") or ""
    if not t:
        m = re.search(r"_(low|mid|high|top)$", _VARIANT.sub("", a["name"].lower()))
        t = m.group(1) if m else ""
    return t


#: A spawn's vehicle where its name does not say, by the mission's folder.
_FOLDER_VEHICLE = {"ships": "ship", "planes": "aircraft", "helicopters": "helicopter"}


def select(data: dict[str, Any], top: str, difficulty: str) -> dict[str, list[dict[str, Any]]]:
    """The mission's objectives, zones and spawns for one difficulty (`AB`, `RB`, `SB`); what belongs to one
    battle-rating tier only carries it (`tier`)."""
    stem = Path(top).stem
    folder = top.lower().split("/")
    default_vehicle = _FOLDER_VEHICLE.get(folder[3] if len(folder) > 4 else "", "ground")
    fam = family(stem)
    prefer = _ORDER[difficulty]
    areas = data["areas"]
    # Which variants each base name has, to keep only the difficulty's own (or the next the mission falls back to).
    variants: dict[str, set[str]] = {}
    for a in [*areas, *data["squads"]]:
        low = a["name"].lower()
        v = _VARIANT.search(low)
        variants.setdefault(low[: v.start()] if v else low, set()).add(v.group(1) if v else "")

    def wanted(a: dict[str, Any]) -> bool:
        low = a["name"].lower()
        other = next((f for f in _FAMILIES if low.startswith(f + "_")), None)
        if other is not None and fam and not fam.startswith(other) and not other.startswith(fam):
            return False
        v = _VARIANT.search(low)
        mine = v.group(1) if v else ""
        have = variants.get(low[: v.start()] if v else low, {mine})
        if len(have) > 1:
            choice = next((p for p in prefer if p in have), None)
            if choice is not None and mine != choice:
                return False
        return True

    # Spawn points that belong to a squad of another difficulty or mode are not this one's.
    keep_members: set[str] = set()
    drop_members: set[str] = set()
    for s in data["squads"]:
        fake = {"name": s["name"], "tier": ""}
        (keep_members if wanted(fake) else drop_members).update(m.lower() for m in s["members"])
    drop_members -= keep_members

    objectives: list[dict[str, Any]] = []
    zones: list[dict[str, Any]] = []
    spawns: list[dict[str, Any]] = []
    seen: set[tuple] = set()
    zone_no = 0
    for a in areas:
        kind = kind_of(a["name"])
        tm = a["tm"]
        if kind is None or (abs(tm[9]) < 1e-3 and abs(tm[11]) < 1e-3) or not wanted(a):
            continue
        if a["name"].lower() in drop_members:
            continue
        tier = _tier_of(a)
        key = (kind, a["name"].lower(), round(tm[9]), round(tm[11]), tier)
        if key in seen:
            continue
        seen.add(key)
        team = team_of(a["name"])
        n0 = len(objectives) + len(zones) + len(spawns)
        size = _size(tm)
        if kind in ("spawn", "convoy_spawn"):
            if size[0] > CONTAINER:
                continue  # the area the mission scatters spawns over, not one of them
            vehicle = "convoy" if kind == "convoy_spawn" else _vehicle(a["name"], default_vehicle)
            spawns.append({"type": "spawn" if vehicle == "ground" else "vehicle_spawn", "team": team,
                           "base": _group(a["name"]), "vehicle": vehicle, "name": a["name"],
                           "position": _p(*tm[9:12]), "radius": round(size[0], 2)})
        elif kind == "battle_area":
            zones.append({"type": "play_area", "team": team, "name": a["name"], "points": _outline(a)})
        elif kind == "excluded":
            zones.append({"type": "out_of_bounds", "team": team, "name": a["name"], "kind": "excluded",
                          "points": _outline(a)})
        elif kind == "kill_area":
            # A team's spawn kill area: out of bounds for the other side.
            zones.append({"type": "out_of_bounds", "team": (3 - team) if team in (1, 2) else None,
                          "name": a["name"], "kind": "spawn_kill_area", "owner": team, "points": _outline(a)})
        elif kind == "airfield" and size[0] > CONTAINER:
            continue
        else:
            obj: dict[str, Any] = {"type": kind, "team": team, "name": a["name"], "area": a["type"], **_place(a)}
            if kind == "capture_zone":
                obj["letter"] = _letter(a["name"], zone_no)
                zone_no += 1
            objectives.append(obj)
        if tier and len(objectives) + len(zones) + len(spawns) > n0:
            (objectives if objectives and objectives[-1]["name"] == a["name"] else
             zones if zones and zones[-1]["name"] == a["name"] else spawns)[-1]["tier"] = tier
    for g in data["groups"]:
        tm = g["tm"]
        key = (g["kind"], g["name"].lower(), round(tm[9]), round(tm[11]), g["tier"])
        if key in seen:
            continue
        seen.add(key)
        army = g.get("army")
        objectives.append({"type": g["kind"], "team": army if army in (1, 2) else team_of(g["name"]),
                           "name": g["name"], "model": g["class"], "shape": "point", "position": _p(*tm[9:12]),
                           "heading": _heading(tm), **({"tier": g["tier"]} if g["tier"] else {})})
    zs = [o for o in objectives if o["type"] == "capture_zone"]
    if len({o["letter"] for o in zs}) < len(zs):  # numbers that repeat (two files' zones): letters in order
        for i, o in enumerate(zs):
            o["letter"] = chr(ord("A") + i) if i < 26 else str(i + 1)
    return {"objectives": objectives, "zones": zones, "spawns": spawns}


#: Battle-rating tiers in the order their stages are numbered.
_TIER_ORDER = ("low", "mid", "high", "top")


def _tier_key(t: str) -> tuple[int, int]:
    if t in _TIER_ORDER:
        return (0, _TIER_ORDER.index(t))
    m = re.match(r"rank (\d+)$", t)
    return (1, int(m.group(1))) if m else (2, 0)


def mission_layouts(arc, top: str) -> list[dict[str, Any]]:
    """One mission's layouts, one a difficulty (those that agree merged); battle-rating tiers are its stages."""
    data = collect(arc, top)
    stem = Path(top).stem
    found: list[tuple[list[str], dict[str, Any]]] = []
    for diff in ("AB", "RB", "SB"):
        sel = select(data, top, diff)
        if not any(sel.values()):
            continue
        same = next((f for f in found if f[1] == sel), None)
        if same:
            same[0].append(diff)
        else:
            found.append(([diff], sel))
    out: list[dict[str, Any]] = []
    for diffs, sel in found:
        tiers = sorted({o["tier"] for k in sel for o in sel[k] if o.get("tier")}, key=_tier_key)
        stages: dict[str, str] = {}
        if len(tiers) > 1:
            for k in sel:
                for o in sel[k]:
                    if o.get("tier"):
                        o["stage"] = tiers.index(o["tier"]) + 1
            stages = {str(i + 1): (f"{t} ranks" if t in _TIER_ORDER else t) for i, t in enumerate(tiers)}
        suffix = "" if len(found) == 1 else "_" + "_".join(d.lower() for d in diffs)
        name = mode_name(stem) + (" " + "/".join(diffs) if len(found) > 1 else "")
        out.append({"id": f"{stem}{suffix}", "name": name, "mode": stem,
                    "aliases": sorted({stem, family(stem), str(data["settings"].get("postfix") or "").strip("_")}
                                      - {""}),
                    "mission": top, "difficulty": [_DIFFICULTY[d] for d in diffs],
                    **({"stageNames": stages} if stages else {}), **sel})
    return out


def level_layouts(arc, level: str, missions: list[str], tool: str) -> dict[str, Any]:
    layouts: list[dict[str, Any]] = []
    for m in missions:
        try:
            layouts += mission_layouts(arc, m)
        except Exception as e:  # one unreadable mission never stops the level
            layouts.append({"id": Path(m).stem, "name": Path(m).stem, "mode": Path(m).stem, "error": str(e),
                            "objectives": [], "zones": [], "spawns": []})
    # Ground battles first, then air, naval and the rest, each in name order.
    order = {"tanks": 0, "humans": 1, "planes": 2, "helicopters": 3, "ships": 4}
    layouts.sort(key=lambda l: (order.get(str(l.get("mission", "")).split("/")[3:4][0] if
                                          str(l.get("mission", "")).count("/") > 3 else "", 9), l["id"]))
    return {"format": FORMAT, "version": 1, "game": GAME, "level": level, "source": tool, "units": "m", "up": "y",
            "coordinates": "the level's frame: glb (x, y, z) = game (x east, y up, -z north)",
            "layouts": layouts}


def counts(doc: dict[str, Any]) -> tuple[int, int, int, int]:
    ls = doc["layouts"]
    return (len(ls), sum(len(l["objectives"]) for l in ls), sum(len(l["zones"]) for l in ls),
            sum(len(l["spawns"]) for l in ls))
