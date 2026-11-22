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


def _f(v):
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def shell_props(bullet) -> dict:
    """
    A weapon blk's `bullet` block as the shell's static data: `speed` (muzzle, m/s), `mass` (kg), `caliber` (mm;
    a sub-calibre shell's flight and hit calibres `ballisticCaliber`, `damageCaliber`), `Cx` (drag coefficient), `maxDistance` (m), `explosiveMass` (kg) and `explosiveType`, `bulletType` and
    `ammoType` (`ammo_type`), the presets that set its ricochet, slope effect and normalisation, its armour power
    table (`armorPower`: [[distance m, mm], ...] from `ArmorPower0m` .. `ArmorPower10000m`, the game's own
    penetration at 0 degrees, kinetic shells that state one) and its de Marre coefficients (`demarre`: k and the
    speed, mass and calibre powers, kinetic shells without a table). Values the block does not state are left out.
    """
    out: dict = {"name": str(bullet.get("bulletName") or "").lower()}
    bt = str(bullet.get("bulletType") or "")
    if bt:
        out["bulletType"] = bt
        out["ammoType"] = ammo_type(bt)
    for k in ("speed", "mass", "Cx", "maxDistance", "explosiveMass"):
        v = _f(bullet.get(k))
        if v is not None:
            out[k] = round(v, 6)
    for k in ("caliber", "ballisticCaliber", "damageCaliber"):
        cal = _f(bullet.get(k))
        if cal:
            out[k] = round(cal * 1000, 2)
    for k in ("explosiveType", "ricochetPreset", "slopeEffectPreset", "normalizationPreset"):
        v = bullet.get(k)
        if isinstance(v, str) and v:
            out[k] = v
    ap = bullet.block("armorpower")
    if ap is not None:
        rows = []
        for k, v in (ap.params.items() if isinstance(ap.params, dict) else ap.params):
            if isinstance(v, (list, tuple)) and len(v) >= 2 and str(k).lower().startswith("armorpower"):
                rows.append([round(float(v[1]), 1), round(float(v[0]), 2)])
        if rows:
            out["armorPower"] = sorted(rows)
    dmg = bullet.block("damage")
    kin = dmg.block("kinetic") if dmg is not None else None
    if kin is not None and _f(kin.get("demarrePenetrationK")) is not None:
        out["demarre"] = {"k": round(_f(kin.get("demarrePenetrationK")), 4),
                          **{n: round(_f(kin.get(f"demarre{n[0].upper()}{n[1:]}Pow")) or 0, 4)
                             for n in ("speed", "mass", "caliber")}}
    return out


#: The drag coefficient of a shell whose block states none: fitted to the recorded speeds of such shells beyond
#: 300 m on the check battles (median 0.353; AP, APCBC, APHEBC, HE, HEAT alike). Shells that state their Cx fit it
#: within 1-4% the same way.
DEFAULT_CX = 0.35


def impact_speed(props: dict, distance: float) -> float | None:
    """A shell's speed after `distance` m of flat flight: the muzzle speed less the drag of air at sea level
    (dv/ds = -k v, k = rho Cx A / 2m, A by `ballisticCaliber` where the shell states one, else `caliber`; Cx
    DEFAULT_CX where the shell states none); None without speed, mass and calibre."""
    v0, m, cal, cx = (props.get(k) for k in ("speed", "mass", "caliber", "Cx"))
    cal = props.get("ballisticCaliber") or cal
    cx = cx or DEFAULT_CX
    if not (v0 and m and cal):
        return None
    import math

    area = math.pi * (cal / 2000.0) ** 2
    return v0 * math.exp(-1.225 * cx * area / (2 * m) * max(0.0, distance))


@dataclass
class Gun:
    """One weapon of a vehicle: its blk's file name, calibre (mm), shells by name: (type, calibre mm), and each
    shell's modification (the block of the weapon blk it is in, which the vehicle buys and prices by that name; ''
    for the weapon's own, stock shell)."""

    blk: str
    calibre: float | None = None
    shells: dict[str, tuple[str, float | None]] = field(default_factory=dict)
    mods: dict[str, str] = field(default_factory=dict)
    props: dict[str, dict] = field(default_factory=dict)  # each shell's static data (`shell_props`)

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

        def walk(blk, mod: str = "") -> None:
            for c in blk.blocks:
                if c.name == "bullet" and (c.get("bulletName") or c.get("bulletType")):
                    # A machine gun's belt names its rounds by type only ("t_ball", "ap_i_ball").
                    cal = c.get("caliber")
                    cal = round(cal * 1000, 1) if isinstance(cal, float) else None
                    name = str(c.get("bulletName") or c.get("bulletType")).lower()
                    gun.shells.setdefault(name, (ammo_type(c.get("bulletType") or ""), cal))
                    gun.mods.setdefault(name, mod)
                    gun.props.setdefault(name, shell_props(c))
                    if gun.calibre is None and cal:
                        gun.calibre = cal
                if c.name not in ("sabot", "rocket"):
                    walk(c, mod if c.name == "bullet" or blk is not b else c.name)

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
