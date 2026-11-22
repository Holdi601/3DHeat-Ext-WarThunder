"""
A vehicle's damage-model parts in the order the replays number them, read from the install at conversion time
(nothing of it is kept or shipped).

A replay's list of the parts a hit damaged (0xF13A, see wrpl.read_part_damaged) numbers each part by its place in
the vehicle's own list: the leaf blocks of the unit blk's `DamageParts` (`gamedata/units/tankmodels/<vehicle>.blk`,
its groups depth first: `hull` { `body_front_dm` ... }, `crew` { `driver_dm` ... }, ...), counting only the parts
the vehicle's damage model has (a node of that name in its collision resource `<model>_collision`, the packs of
`content/base/res`). The blk's lists are generic (a light tank's lists 75 turret ammo racks), the model has the ones
it has. Checked against the vehicles' fires, whose list names each fire by both numbers (the vehicle's own and the
game's part name, convert.FIRES_EVENT): see the README's Damaged parts.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

from . import collision, install

#: Where a unit's blk may be, by kind of unit (the first that exists is read).
UNIT_FOLDERS = ("gamedata/units/tankmodels/", "gamedata/units/wheeled_vehicles/", "gamedata/units/tracked_vehicles/",
                "gamedata/units/air_defence/", "gamedata/flightmodels/", "gamedata/units/ships/")
#: The resource packs' folders under content/base/res (and the folder itself).
RES_FOLDERS = ("tanks", "aircrafts", "ships", ".")

#: Crew members' parts: `driver_dm`, `gunner_01_dm`, `commander_dm`, `loader_dm`, `machine_gunner_dm`, ... and
#: aircraft `pilot_dm`, `gunner1_dm`.
CREW = re.compile(r"^(driver|gunner|commander|loader|machine_gunner|pilot|radio_operator|bombardier|crew)(_?\d+)?_dm$")


def is_crew(part: str) -> bool:
    return bool(CREW.match(part or ""))


def part_group(part: str) -> str:
    """A part's kind for analysis: crew, ammo, fuel, engine, transmission, gun (barrel, breech), turret_drive,
    tracks (and wheels), optics, armour (hull, turret plates, screens), equipment, or ''."""
    p = (part or "").lower()
    if is_crew(p):
        return "crew"
    for prefix, group in (("ammo", "ammo"), ("fuel_tank", "fuel"), ("engine", "engine"), ("transmission", "transmission"),
                          ("radiator", "engine"), ("gun_barrel", "gun"), ("cannon_breech", "gun"),
                          ("autoloader", "gun"), ("drive_turret", "turret_drive"), ("turret_hydraulics", "turret_drive"),
                          ("track", "tracks"), ("wheel", "tracks"), ("optic", "optics"),
                          ("commander_panoramic", "optics"), ("body_", "armour"), ("superstructure", "armour"),
                          ("turret_", "armour"), ("gun_mask", "armour"), ("ex_", "armour"), ("cover", "armour"),
                          ("radio", "equipment"), ("electronic", "equipment"), ("fire_control", "equipment"),
                          ("power_system", "equipment"), ("driver_controls", "equipment")):
        if p.startswith(prefix):
            return group
    return ""


def cache_path() -> Path:
    """Where the parts each vehicle's model has are kept once read (`PartOrder`): `HEAT3D_WT_PARTS`, else
    ~/.cache/heat3d-wt/part-orders.json."""
    return Path(os.environ.get("HEAT3D_WT_PARTS") or Path.home() / ".cache" / "heat3d-wt" / "part-orders.json")


#: A kept list beside an install's files (a copy of the game files without the resource packs, as a converter on
#: another machine may have), read when the packs are not there; never written by this program.
GAME_COPY_FILE = "heat3d-part-orders.json"


class PartOrder:
    """
    Each vehicle's damage-model parts in replay order (`parts(vehicle)`), read as asked; empty without an install.
    The parts a vehicle's model has (its collision resource's nodes) are kept in `cache_path()` once read, so a
    machine with the unit files (aces.vromfs.bin) but not the resource packs (content/base/res, 14 GB) can still
    name them: the kept parts are put in the order of the vehicle's blk as that machine's install has it.
    """

    def __init__(self, archive=None, res_root: Path | None = None, kept: Path | None = None,
                 more_kept: tuple[Path, ...] = ()) -> None:
        self.archive = archive
        self.res_root = res_root
        self.kept_path = kept
        self._index: collision.ResourceIndex | None = None
        self._parts: dict[str, list[str]] = {}
        self._global: list[str] | None = None
        self._kept: dict[str, list[str]] | None = None
        self._more = more_kept
        self._new = False
        #: False for a replay that numbers the game's part list otherwise (an older game version): `global_name` ''.
        self.global_ok = True

    @classmethod
    def from_game(cls, game: str | os.PathLike[str] | None = None, archive=None) -> "PartOrder":
        root = install.find_game(game)
        if root is None:
            return cls()
        res = Path(root) / "content" / "base" / "res"
        if archive is None:
            path = Path(root) / "aces.vromfs.bin"
            try:
                from .vromfs import Vromfs

                archive = Vromfs(path) if path.is_file() else None
            except (OSError, ValueError, KeyError):
                archive = None
        return cls(archive, res if res.is_dir() else None, cache_path(), (Path(root) / GAME_COPY_FILE,))

    def __bool__(self) -> bool:
        return self.archive is not None and (self.res_root is not None or bool(self._load_kept()))

    def _load_kept(self) -> dict[str, list[str]]:
        if self._kept is None:
            self._kept = {}
            import json

            for path in (*self._more, self.kept_path):
                try:
                    doc = json.loads(Path(path).read_text(encoding="utf-8")) if path else {}
                except (OSError, ValueError):
                    continue
                for v, parts in (doc.get("vehicles") or {}).items():
                    if isinstance(parts, list):
                        self._kept[v] = [str(x) for x in parts]
        return self._kept

    def save(self) -> bool:
        """Keep the parts read in this run beside those kept before (`cache_path`); False when nothing was new or
        the file could not be written."""
        if not self._new or self.kept_path is None:
            return False
        import json

        kept = dict(self._load_kept())
        kept.update({v: p for v, p in self._parts.items() if p})
        try:
            self.kept_path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.kept_path.with_name(self.kept_path.name + f".{os.getpid()}.part")
            tmp.write_text(json.dumps({"format": "3dheat-wt-part-orders", "version": 1, "vehicles": kept},
                                      separators=(",", ":")), encoding="utf-8")
            tmp.replace(self.kept_path)
        except OSError:
            return False
        self._kept, self._new = kept, False
        return True

    def _unit_blk(self, vehicle: str):
        for folder in UNIT_FOLDERS:
            try:
                return self.archive.blk(f"{folder}{vehicle.lower()}.blk")
            except Exception:  # noqa: BLE001 - not in this folder
                continue
        return None

    def _model_nodes(self, model: str) -> set[str] | None:
        if self.res_root is None:
            return None
        if self._index is None:
            self._index = collision.ResourceIndex(*(self.res_root / d for d in RES_FOLDERS))
        where = self._index.collision(model)
        if where is None:
            return None
        try:
            return set(collision.node_names(collision.load_blob(where)))
        except (collision.CollisionError, OSError, ValueError, IndexError, EOFError):
            return None

    def parts(self, vehicle: str) -> list[str]:
        """The vehicle's parts by their replay number (index), [] when the install does not tell."""
        if not self or not vehicle:
            return []
        if vehicle in self._parts:
            return self._parts[vehicle]
        out: list[str] = []
        b = self._unit_blk(vehicle)
        dp = b.block("DamageParts") if b is not None else None
        model = b.get("model") if b is not None else None
        nodes = self._model_nodes(model) if dp is not None and isinstance(model, str) and model else None
        if nodes:
            self._new = True
        elif dp is not None and vehicle in self._load_kept():
            nodes = set(self._load_kept()[vehicle])
        if nodes:
            seen: set[str] = set()

            def walk(blk) -> None:
                for c in blk.blocks:
                    if c.name.endswith("_dm") or not c.blocks:
                        if c.name in nodes and c.name not in seen:
                            seen.add(c.name)
                            out.append(c.name)
                    else:
                        walk(c)

            walk(dp)
        self._parts[vehicle] = out
        return out

    def name(self, vehicle: str, number: int) -> str:
        p = self.parts(vehicle)
        return p[number] if 0 <= number < len(p) else ""

    def global_name(self, number: int) -> str:
        """A part's name by the game's own numbering (`global_names`), '' when not known."""
        if not self.global_ok:
            return ""
        if self._global is None:
            self._global = global_names(self.archive) if self.archive is not None else []
        return self._global[number] if 0 <= number < len(self._global) else ""


_TEMPLATE = re.compile(r"#(\d+)(?::(\d+))?#")


def _expand(t: str) -> list[str]:
    m = _TEMPLATE.search(t)
    if not m:
        return [t]
    a, b = m.group(1), m.group(2)
    lo, hi = (1, int(a)) if b is None else (int(a), int(b))
    out: list[str] = []
    for i in range(lo, hi + 1):
        out += _expand(t[: m.start()] + f"{i:0{len(a)}d}" + t[m.end():])
    return out


def global_names(archive) -> list[str]:
    """
    The game's list of part names, by the number a projectile's hit (0xF0E9, `hitPart`) and a fire (its node)
    name a part with: `config/damagemodelparts.blk`'s blocks depth first, `default` and `default_v1` first; a block
    with a `template` stands for the names it expands to (`name_#30#` -> name_01 .. name_30, the digits as wide
    as the number is written; `name#1:8#` -> name1 .. name8), a block without blocks under it for its own name, a
    block with blocks under it for what is under it; a name already listed keeps its first place. Checked against
    the hit points of six server battles: 98.7% of 4,249 hits lie on the part their number names.
    """
    try:
        blk = archive.blk("config/damagemodelparts.blk")
    except Exception:  # noqa: BLE001 - no such file in this install
        return []
    names: list[str] = []

    def walk(b) -> None:
        for sub in b.blocks:
            t = sub.get("template")
            if isinstance(t, str):
                names.extend(_expand(t))
            elif sub.name in ("default", "default_v1") or not sub.blocks:
                names.append(sub.name)
            else:
                walk(sub)

    walk(blk)
    seen: set[str] = set()
    out = []
    for n in names:
        if n not in seen:
            seen.add(n)
            out.append(n)
    return out


def keep_all(game: str | os.PathLike[str] | None = None, out: Path | None = None) -> tuple[int, Path | None]:
    """Read and keep the parts of every vehicle of the install (`cache_path`, or `out`): (vehicles, file)."""
    po = PartOrder.from_game(game)
    if po.archive is None or po.res_root is None:
        return 0, None
    if out is not None:
        po.kept_path = Path(out)
    n = 0
    for name in sorted(po.archive.files):
        folder, _, base = name.rpartition("/")
        if f"{folder}/" in UNIT_FOLDERS and base.endswith(".blk") and po.parts(base[:-4]):
            n += 1
    po._new = True
    po.save()
    return n, po.kept_path


def main(argv: list[str] | None = None) -> int:
    """`python -m heat3d_ext_warthunder.damage_parts [--game <folder>] [-o <file>]`: keep every vehicle's parts."""
    import argparse

    ap = argparse.ArgumentParser(prog="python -m heat3d_ext_warthunder.damage_parts", description=main.__doc__)
    ap.add_argument("--game")
    ap.add_argument("-o", "--out")
    a = ap.parse_args(argv)
    n, path = keep_all(a.game, Path(a.out) if a.out else None)
    if path is None:
        print("no install with its resource packs found (give --game)")
        return 2
    print(f"{n} vehicles' parts kept in {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
