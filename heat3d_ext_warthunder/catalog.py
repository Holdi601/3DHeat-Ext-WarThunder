"""
The install's catalogue, `<levels>/warthunder/catalog.json` (`format: 3dheat-catalog`): every vehicle, soldier
squad, weapon, round, piece of soldier equipment and modification the install lists, read from your own install
(read only) and written on your machine only. The viewer names units by it (`src/figures/unitcatalog.ts`); the
extractor's `status` compares the install against it, so a game update's new items are reported.

What is read:

- `char.vromfs.bin` `config/wpcost.blk`: one block per playable unit (its name the unit's id), `unitClass`
  (`exp_tank`, `exp_fighter`, `exp_human` for a soldier squad ...), `country`, `rank`, the battle ratings
  (`economicRank<Arcade|Historical|Simulation>`, BR = value / 3 + 1), and its `weapons` and `modifications`
  blocks: a squad's `weapons` hold its own weapon presets (`<id>_default`, `<id>_preset_N`) and the equipment it
  can take along (drones, grenades, launchers, ammunition and medical boxes, explosives), its `modifications`
  the attachments and armour (scopes, grips, suppressors, vests); a vehicle's its upgrades and ammunition belts.
- `aces.vromfs.bin`: the unit files (`gamedata/units/tankmodels/`, `.../wheeled_vehicles/`,
  `.../tracked_vehicles/`, `.../air_defence/`, `gamedata/flightmodels/`, `gamedata/units/ships/`,
  `gamedata/units/humans/`; AI-only units too), each one's `model` and `type` (an aircraft with a `helicopter`
  block is a helicopter); the weapon files (`gamedata/weapons/**.blk`, a weapon by its file name) and the rounds
  they fire (`bullet`, `rocket`, `bomb`, `torpedo`, `mine` blocks: `bulletName`, `caliber`, `bulletType`).
- the localisation (`names.py`) for display names, where the game has them.

Item kinds: `vehicle`, `operator` (a soldier squad), `weapon`, `ammo`, `gadget` (soldier equipment),
`modification`. A vehicle gets `model` where the local model pack (`<levels>/model-packs/warthunder/
model-pack.json`) has one.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

FORMAT = "3dheat-catalog"
GAME = "warthunder"

#: Unit folders and the kind of unit in each.
UNIT_FOLDERS = {
    "gamedata/units/tankmodels/": "tank",
    "gamedata/units/wheeled_vehicles/": "tank",
    "gamedata/units/tracked_vehicles/": "tank",
    "gamedata/units/air_defence/": "tank",
    "gamedata/flightmodels/": "aircraft",
    "gamedata/units/ships/": "ship",
    "gamedata/units/humans/": "human",
}
DOMAIN = {"tank": "ground", "aircraft": "air", "helicopter": "air", "ship": "sea", "human": "infantry"}
CLASS = {"exp_tank": "tank", "exp_heavy_tank": "heavy_tank", "exp_tank_destroyer": "tank_destroyer",
         "exp_SPAA": "spaa", "exp_fighter": "fighter", "exp_assault": "attacker", "exp_bomber": "bomber",
         "exp_helicopter": "helicopter", "exp_torpedo_boat": "torpedo_boat", "exp_gun_boat": "gun_boat",
         "exp_torpedo_gun_boat": "torpedo_gun_boat", "exp_submarine_chaser": "submarine_chaser",
         "exp_destroyer": "destroyer", "exp_naval_ferry_barge": "barge", "exp_cruiser": "cruiser",
         "exp_human": "infantry"}
HUMAN = "exp_human"
WEAPONS = "gamedata/weapons/"
_ROUNDS = ("bullet", "rocket", "bomb", "torpedo", "mine")
#: Weapon presets in a squad's `weapons` block (its own and those it shares; the rest is equipment).
_PRESET = re.compile(r"(_default|_preset_\d+)$")
KINDS = ("vehicle", "operator", "weapon", "ammo", "gadget", "modification")


def _unit_files(files) -> dict[str, tuple[str, str]]:
    """Unit id (lower case) -> (its file, the folder's unit kind)."""
    out: dict[str, tuple[str, str]] = {}
    for name in files:
        low = name.lower()
        for folder, kind in UNIT_FOLDERS.items():
            if low.startswith(folder) and low.endswith(".blk") and "/" not in low[len(folder):]:
                out.setdefault(low[len(folder):-4], (name, kind))
    return out


def weapon_files(files) -> dict[str, str]:
    """Weapon id (the file name, lower case) -> its file, every `.blk` under `gamedata/weapons/`."""
    out: dict[str, str] = {}
    for name in sorted(files):
        low = name.lower()
        if low.startswith(WEAPONS) and low.endswith(".blk"):
            out.setdefault(low.rsplit("/", 1)[-1][:-4], name)
    return out


def rounds_of(blk, depth: int = 0, out: dict[str, dict] | None = None) -> dict[str, dict]:
    """The rounds a weapon blk names, by `bulletName` (lower case): calibre (mm) and `bulletType`."""
    out = {} if out is None else out
    for s in blk.blocks:
        if s.name in _ROUNDS:
            n = s.get("bulletName")
            if isinstance(n, str) and n.strip():
                it: dict[str, Any] = {"round": s.name}
                cal = s.get("caliber")
                if isinstance(cal, (int, float)) and cal > 0:
                    it["calibre"] = round(float(cal) * 1000.0, 2)
                bt = s.get("bulletType")
                if isinstance(bt, str) and bt:
                    it["bulletType"] = bt
                out.setdefault(n.strip().lower(), it)
        if depth < 4:
            rounds_of(s, depth + 1, out)
    return out


def economy(wpcost) -> dict[str, Any]:
    """`config/wpcost.blk` sorted: vehicles and squads (id -> block, original-case name), gadgets, modifications."""
    vehicles: dict[str, Any] = {}
    squads: dict[str, Any] = {}
    gadgets: dict[str, set[str]] = {}
    mods: dict[str, set[str]] = {}
    for b in wpcost.blocks:
        uid = b.name.lower()
        human = b.get("unitClass") == HUMAN
        (squads if human else vehicles)[uid] = b
        w = b.block("weapons")
        if human and w is not None:
            for x in w.blocks:
                n = x.name.lower()
                if n == "custom_presets" or n == uid or _PRESET.search(n):
                    continue
                gadgets.setdefault(n, set()).add(uid)
        m = b.block("modifications")
        if m is not None:
            for x in m.blocks:
                mods.setdefault(x.name.lower(), set()).add(uid)
    return {"vehicles": vehicles, "squads": squads, "gadgets": gadgets, "modifications": mods}


def _cache_file(aces: Path) -> Path:
    from .app import paths

    st = aces.stat()
    key = hashlib.sha1(f"{aces.resolve()}|{st.st_size}|{st.st_mtime_ns}".encode()).hexdigest()[:12]
    return paths.data_dir() / "cache" / f"warthunder-rounds-{key}.json"


def all_rounds(archive, aces: Path | None = None) -> dict[str, dict]:
    """Every round of every weapon file (about a minute on a full install); kept per `aces.vromfs.bin` in the
    tool's cache folder, so a status after the first one reads it back."""
    cache = None
    if aces is not None:
        try:
            cache = _cache_file(aces)
            return json.loads(cache.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            pass
    out: dict[str, dict] = {}
    for f in weapon_files(archive.files).values():
        try:
            rounds_of(archive.blk(f), 0, out)
        except Exception:  # noqa: BLE001  one unreadable weapon file never stops the catalogue
            continue
    if cache is not None:
        try:
            cache.parent.mkdir(parents=True, exist_ok=True)
            tmp = cache.with_suffix(".part")
            tmp.write_text(json.dumps(out, sort_keys=True), encoding="utf-8")
            tmp.replace(cache)
        except OSError:
            pass
    return out


def _archives(game: Path):
    from .vromfs import Vromfs

    return Vromfs(Path(game) / "aces.vromfs.bin"), Vromfs(Path(game) / "char.vromfs.bin")


def install_items(game: Path) -> dict[str, list[str]]:
    """The ids the install holds, by kind (`GameSpec.catalog_items`)."""
    aces, char = _archives(game)
    eco = economy(char.blk("config/wpcost.blk"))
    units = _unit_files(aces.files)
    squads = set(eco["squads"]) | {u for u, (_f, kind) in units.items() if kind == "human"}
    vehicles = (set(units) | set(eco["vehicles"])) - squads
    return {
        "vehicle": sorted(vehicles),
        "operator": sorted(squads),
        "weapon": sorted(weapon_files(aces.files)),
        "ammo": sorted(all_rounds(aces, Path(game) / "aces.vromfs.bin")),
        "gadget": sorted(eco["gadgets"]),
        "modification": sorted(eco["modifications"]),
    }


def _br(c) -> dict[str, float]:
    br = {}
    for mode, k in (("ab", "economicRankArcade"), ("rb", "economicRankHistorical"), ("sb", "economicRankSimulation")):
        r = c.get(k)
        if isinstance(r, (int, float)):
            br[mode] = round(r / 3 + 1, 1)
    return br


def _unit_info(aces, path: str, kind: str) -> dict[str, Any]:
    try:
        b = aces.blk(path)
    except Exception:  # noqa: BLE001
        return {}
    if kind == "aircraft" and b.block("helicopter") is not None:
        kind = "helicopter"
    info: dict[str, Any] = {"domain": DOMAIN[kind], "type": "infantry" if kind == "human" else kind}
    return info


def build(game: Path, out: Path, log=None) -> Path:
    """Writes `<out>/catalog.json` (out = `<levels>/warthunder`); returns the file."""
    from . import names as wtnames

    aces, char = _archives(game)
    eco = economy(char.blk("config/wpcost.blk"))
    units = _unit_files(aces.files)
    lang = wtnames.load(str(game))
    weap = wtnames.load_weapons(str(game))
    pack: dict = {}
    pack_file = Path(out).parent / "model-packs" / GAME / "model-pack.json"
    try:
        pack = json.loads(pack_file.read_text(encoding="utf-8")).get("units", {})
    except (OSError, ValueError):
        pack = {}
    items: list[dict[str, Any]] = []
    ids = sorted(set(units) | set(eco["vehicles"]) | set(eco["squads"]))
    for n, uid in enumerate(ids):
        if log and n % 500 == 0:
            log(f"  units {n}/{len(ids)}")
        c = eco["vehicles"].get(uid) or eco["squads"].get(uid)
        u = _unit_info(aces, *units[uid]) if uid in units else {}
        raw = c.name if c is not None else uid
        full, short, _k = lang.lookup(raw)
        if not full and raw != uid:
            full, short, _k = lang.lookup(uid)
        human = (c is not None and c.get("unitClass") == HUMAN) or (uid in units and units[uid][1] == "human")
        it: dict[str, Any] = {"id": uid, "kind": "operator" if human else "vehicle", "name": (short or full or raw).strip()}
        if u.get("domain"):
            it["domain"], it["type"] = u["domain"], u["type"]
        if c is not None:
            uc = str(c.get("unitClass") or "")
            it["class"] = CLASS.get(uc, uc.removeprefix("exp_").lower()) or u.get("type", "")
            nat = str(c.get("country") or "")
            if nat:
                it["nation"] = nat.removeprefix("country_")
            if isinstance(c.get("rank"), int):
                it["rank"] = c.get("rank")
            br = _br(c)
            if br:
                it["br"] = br
        elif u.get("type"):
            it["class"] = u["type"]
        if full and full.strip() != it["name"]:
            it["longName"] = full.strip()
        it["key"] = it["name"]
        e = pack.get(uid)
        if isinstance(e, dict) and e.get("file"):
            it["model"] = f"model-packs/{GAME}/{e['file']}"
        items.append(it)
    if log:
        log("  weapons and rounds")
    for wid, path in weapon_files(aces.files).items():
        name, short = weap.lookup(wid)
        it = {"id": wid, "kind": "weapon", "name": (name or wid).strip(), "file": path}
        if short and short != it["name"]:
            it["shortName"] = short
        items.append(it)
    for rid, r in sorted(all_rounds(aces, Path(game) / "aces.vromfs.bin").items()):
        name, short = weap.lookup(rid)
        it = {"id": rid, "kind": "ammo", "name": (name or rid).strip(), **r}
        if short and short != it["name"]:
            it["shortName"] = short
        items.append(it)
    for kind, key in (("gadget", "gadgets"), ("modification", "modifications")):
        for gid, users in sorted(eco[key].items()):
            name, _s = weap.lookup(gid)
            items.append({"id": gid, "kind": kind, "name": (name or gid).strip(), "units": len(users)})
    dest = Path(out) / "catalog.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    from . import __version__

    doc = {"format": FORMAT, "version": 1, "game": GAME, "gameBuild": game_build(game),
           "source": f"heat3d-warthunder {__version__}", "items": items}
    tmp = dest.with_suffix(".json.part")
    tmp.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, dest)
    if log:
        counts: dict[str, int] = {}
        for it in items:
            counts[it["kind"]] = counts.get(it["kind"], 0) + 1
        log("  " + ", ".join(f"{v} {k}" for k, v in counts.items()))
    return dest


def game_build(game: Path) -> str | None:
    for name in ("content/pkg_main.ver", "version"):
        try:
            text = (Path(game) / name).read_text(encoding="utf-8", errors="replace").strip()
        except OSError:
            continue
        if text:
            return text.splitlines()[0][:40]
    return None


def extracted_items(out: Path) -> dict[str, list[str]]:
    """The ids `<out>/catalog.json` holds, by kind (`GameSpec.extracted_items`)."""
    try:
        data = json.loads((Path(out) / "catalog.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    got: dict[str, set[str]] = {}
    for it in data.get("items", []) if isinstance(data, dict) else []:
        if isinstance(it, dict) and it.get("id") is not None:
            got.setdefault(str(it.get("kind") or "vehicle"), set()).add(str(it["id"]))
    return {k: sorted(v) for k, v in got.items()}
