"""
A ground vehicle's weapons and their ammunition, from the install's
`aces.vromfs.bin`: `gamedata/units/tankmodels/<vehicle>.blk` lists the
weapons in order (`commonWeapons`, then its weapon preset's), each naming its
weapon blk; a weapon blk names every shell it can fire (`bullet` blocks:
`bulletName` "125mm_3bm46", `bulletType` "apds_fs_long_l30_tank", `caliber`
in m). The replay's 0xF0BD (UnitBulletRearm) counts rounds by the same weapon
index (see convert._shot_ammo).
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from . import install

#: A `bulletType` as the ammunition type the game's hit camera and shop name it (first match wins).
_TYPES = (
    ("apds_fs", "APFSDS"), ("apfsds", "APFSDS"), ("apds", "APDS"), ("apcbc", "APCBC"), ("apbc", "APBC"),
    ("apcr", "APCR"), ("aphebc", "APHEBC"), ("aphe", "APHE"), ("apc", "APC"), ("heat_fs", "HEAT-FS"),
    ("heat_grenade", "HEAT"), ("heat", "HEAT"), ("hesh", "HESH"), ("atgm", "ATGM"), ("sam", "SAM"),
    ("rocket", "rocket"), ("sap", "SAP"), ("he", "HE"), ("frag", "HE"), ("shrapnel", "shrapnel"),
    ("smoke", "smoke"), ("practice", "practice"), ("ap", "AP"), ("i_t", "kinetic"), ("t_", "kinetic"),
)

#: Ammunition types that burst on the target (a scorch mark), the rest go through or bounce.
EXPLOSIVE = {"HE", "HEAT", "HEAT-FS", "HESH", "ATGM", "SAM", "rocket", "SAP", "APHE", "APHEBC", "shrapnel"}


def ammo_type(bullet_type: str) -> str:
    """The ammunition type of a weapon blk's `bulletType` ("apds_fs_long_tank" APFSDS), '' when not known."""
    low = (bullet_type or "").lower()
    for prefix, name in _TYPES:
        if low.startswith(prefix):
            return name
    return ""


@dataclass
class Gun:
    """One weapon of a vehicle: its blk's file name, calibre (mm) and shells by name: (type, calibre mm)."""

    blk: str
    calibre: float | None = None
    shells: dict[str, tuple[str, float | None]] = field(default_factory=dict)

    @property
    def machine_gun(self) -> bool:
        return "machinegun" in self.blk.lower() or (self.calibre is not None and self.calibre < 20 and "dummy" not in self.blk)


class Arsenal:
    """The install's vehicles' weapons, read as asked (`guns(vehicle)`); empty without an install."""

    def __init__(self, archive=None) -> None:
        self.archive = archive
        self._guns: dict[str, list[Gun]] = {}
        self._blks: dict[str, Gun] = {}

    @classmethod
    def from_game(cls, game: str | os.PathLike[str] | None = None) -> "Arsenal":
        root = install.find_game(game)
        path = Path(root) / "aces.vromfs.bin" if root else None
        if path is None or not path.is_file():
            return cls()
        try:
            from .vromfs import Vromfs

            return cls(Vromfs(path))
        except (OSError, ValueError, KeyError):
            return cls()

    def __bool__(self) -> bool:
        return self.archive is not None

    def drive(self, vehicle: str) -> tuple[float, float] | None:
        """The main gun's turret drive: its traverse and elevation speed (`speedYaw`, `speedPitch` of the first
        `commonWeapons` weapon; degrees a second, before crew skills and modifications), None where not known."""
        if self.archive is None or not vehicle:
            return None
        try:
            b = self.archive.blk(f"gamedata/units/tankmodels/{vehicle.lower()}.blk")
        except Exception:  # no such vehicle file: no drive
            return None
        cw = b.block("commonWeapons") if b is not None else None
        for w in cw.blocks if cw else []:
            yaw, pitch = w.get("speedYaw"), w.get("speedPitch")
            if isinstance(yaw, (int, float)) and isinstance(pitch, (int, float)) and yaw > 0 and pitch > 0:
                return float(yaw), float(pitch)
        return None

    def _gun(self, blk_path: str) -> Gun:
        key = blk_path.lower().replace("\\", "/")
        if key in self._blks:
            return self._blks[key]
        gun = Gun(key.rpartition("/")[2])
        try:
            b = self.archive.blk(key)
        except (KeyError, ValueError, IndexError):
            b = None

        def walk(blk) -> None:
            for c in blk.blocks:
                if c.name == "bullet" and c.get("bulletName"):
                    cal = c.get("caliber")
                    cal = round(cal * 1000, 1) if isinstance(cal, float) else None
                    gun.shells.setdefault(str(c.get("bulletName")).lower(), (ammo_type(c.get("bulletType") or ""), cal))
                    if gun.calibre is None and cal:
                        gun.calibre = cal
                if c.name not in ("sabot", "rocket"):
                    walk(c)

        if b is not None:
            walk(b)
        if gun.calibre is None:
            from .convert import calibre_of

            gun.calibre = calibre_of(gun.blk)
        self._blks[key] = gun
        return gun

    def guns(self, vehicle: str) -> list[Gun]:
        """A ground vehicle's weapons in the game's order: `commonWeapons`, then its first weapon preset's."""
        if not self or not vehicle:
            return []
        if vehicle in self._guns:
            return self._guns[vehicle]
        out: list[Gun] = []
        try:
            b = self.archive.blk(f"gamedata/units/tankmodels/{vehicle.lower()}.blk")
        except (KeyError, ValueError, IndexError):
            b = None
        if b is not None:
            blocks = [b.block("commonWeapons")]
            presets = b.block("weapon_presets")
            preset = presets.block("preset") if presets is not None else None
            if preset is not None and preset.get("blk"):
                try:
                    blocks.append(self.archive.blk(str(preset.get("blk")).lower()))
                except (KeyError, ValueError, IndexError):
                    pass
            for blk in blocks:
                for w in (blk.blocks if blk is not None else []):
                    if w.name == "Weapon" and w.get("blk"):
                        out.append(self._gun(str(w.get("blk"))))
        self._guns[vehicle] = out
        return out
