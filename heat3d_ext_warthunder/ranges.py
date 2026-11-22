"""
`heat3d-wt-ranges [-o ranges.json] [--game <folder>]` (also `heat3d-wt-replay ranges ...`)

Builds a catalogue of weapon reach, sights and sensors from your own War
Thunder installation, for the 3DHeat viewer's engagement ranges, view cones
and sensor sectors. Everything is read from the install's `aces.vromfs.bin`
(and the localisation for names) on your machine; the file written stays on
your machine.

What is read (binary BLK, see vromfs.py):

- units: `gamedata/units/tankmodels/*.blk` (ground), `gamedata/flightmodels/*.blk`
  (aircraft and helicopters), `gamedata/units/ships/*.blk`: every `Weapon`
  block naming a weapon blk (also inside weapon slots, presets and
  modifications), every `sensor` block naming a sensor blk, the sights
  (`cockpit`, `commanderView`: zoom out/in field of view; aircraft `sightOutFov`,
  `sightInFov`, `targetingPodFov`) and `nightVision` blocks (`*Thermal`: a
  thermal imager, its resolution giving the generation; `*Ir`: image
  intensifier), and laser rangefinder modifications (`rangefinderMounted`,
  `isLaser`).
- weapons: a weapon blk's `bullet`, `rocket`, `bomb` and `torpedo` blocks (a
  container's inner `blk` followed): shell `maxDistance` and speed, the gun's
  `aimMaxDist`; a missile's `minDistance`, `maxDistance`/`rangeMax`,
  `loadFactorMax`, `guidanceType`, its seeker's `angleMax`/`lockAngleMax` and
  `lockDistance`, and its launch tables (`rangeMin`/`rangeMax` per altitude).
- sensors: `gamedata/sensors/*.blk` - `type` radar (transceivers' `range`
  for their reference `rcs`, scan patterns' azimuth and elevation limits;
  a transceiver of `visibilityType` infraRed is an IRST, radarIntercept a
  passive receiver), rwr (`range`, receivers' sectors), mlws, lws.

The file follows the viewer's local catalogue layout (`version` 1):
`weapons` (id, cls, name, range [least, best, most] in metres, shape, cone,
alt, labels, detail), `sensors` by id, and `units` (names, weapons, sensors,
optics). Values the files do not state are left out; a best range the game
does not state is the gun's sight range or a class value, marked in `detail`.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from . import __version__, install

#: Where the viewer's local data lives by default (beside the user's levels).
DEFAULT_OUT = Path("ranges.json")

_PROJECTILES = ("bullet", "rocket", "bomb", "torpedo")
_SEEKERS = ("radarSeeker", "irSeeker", "opticalSeeker", "laserSeeker", "beamRiding", "semiActiveRadarSeeker")
#: Bullet types and weapon files that are not weapons: countermeasures, smoke.
_NOT_WEAPONS = ("flare", "chaff", "countermeasure", "smoke", "decoy")
#: A best range for guns the game gives no sight range for, by class, metres.
_GUN_BEST = {"mg": 800.0, "cannon": 1200.0, "gun": 2000.0}


def _num(v, d=None):
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else d


def _r(x: float | None, nd: int = 0):
    if x is None:
        return None
    return round(x, nd) if nd else int(round(x))


def _walk(b, name: str):
    """Every block called `name` under `b`, depth first."""
    for c in b.blocks:
        if c.name == name:
            yield c
        yield from _walk(c, name)


def _all(b, key: str) -> list:
    return [v for k, v in b.params if k == key]


def thermal_gen(resolution) -> int | None:
    """The thermal imager's generation by its resolution, as the game draws them: 500x300 first, 800x600 second, wider third."""
    if not isinstance(resolution, (list, tuple)) or not resolution:
        return None
    w = resolution[0]
    return 1 if w <= 520 else 2 if w <= 880 else 3


class Catalogue:
    """The catalogue being built from one archive (`Vromfs`), with the localisation's names if given."""

    def __init__(self, archive, names=None, weapon_names=None) -> None:
        self.a = archive
        self.names = names
        self.wnames = weapon_names
        self.weapons: dict[str, dict] = {}
        self._weapon_of: dict[str, list[str]] = {}
        self.sensors: dict[str, dict] = {}
        self._sensor_of: dict[str, str | None] = {}
        self._blk: dict[str, object] = {}

    def blk(self, path: str):
        key = path.lower().replace("\\", "/")
        if key not in self._blk:
            try:
                self._blk[key] = self.a.blk(key)
            except Exception:  # absent or unreadable: nothing from it
                self._blk[key] = None
        return self._blk[key]

    # Weapons ---------------------------------------------------------------

    def _labels(self, *ids: str) -> list[str]:
        out: list[str] = []
        for i in ids:
            if not i:
                continue
            for s in (i, *(self.wnames.lookup(i) if self.wnames else ())):
                if s and s not in out:
                    out.append(s)
        return out

    def weapon(self, path: str, air: bool, depth: int = 0) -> list[str]:
        """The catalogue ids of what a weapon blk fires (a container's contents followed)."""
        key = path.lower().replace("\\", "/")
        memo = f"{key}|{int(air)}"
        if memo in self._weapon_of:
            return self._weapon_of[memo]
        self._weapon_of[memo] = []
        b = self.blk(key)
        out: list[str] = []
        if b is not None and "dummy" not in key:
            shells = [c for c in b.blocks if c.name in _PROJECTILES]
            if shells:
                e = self._entry(key, b, shells, air)
                if e:
                    self.weapons.setdefault(e["id"], e)
                    out.append(e["id"])
            elif depth < 3:
                for inner in _all(b, "blk"):
                    out += self.weapon(str(inner), air, depth + 1)
        self._weapon_of[memo] = out
        return out

    @staticmethod
    def _shells(b) -> list[dict]:
        """
        Every shell the weapon can fire, its stock ones and those of its modifications (a block holding a `bullet`
        block, named as the vehicle buys it: `mod`): name, `type` (bulletType), speed and maxDistance as before,
        and the static data of arsenal.shell_props (ammunition type, mass, calibre, drag, explosive, presets,
        armour power table, de Marre coefficients). A belt's rounds without a name of their own are listed by type.
        """
        from .arsenal import shell_props

        out: list[dict] = []
        seen: set[str] = set()

        def add(bullet, mod: str) -> None:
            name = str(bullet.get("bulletName") or "")
            props = shell_props(bullet)
            key = (name or props.get("bulletType") or "").lower()
            if not key or key in seen:
                return
            seen.add(key)
            props.pop("name", None)
            entry = {"name": name, "type": str(bullet.get("bulletType") or ""), "speed": _r(_num(bullet.get("speed"))),
                     "maxDistance": _r(_num(bullet.get("maxDistance"))), **props}
            if mod:
                entry["mod"] = mod
            out.append({k: v for k, v in entry.items() if v not in (None, "")})

        for c in b.blocks:
            if c.name == "bullet":
                add(c, "")
            elif c.name not in _PROJECTILES:
                for inner in c.blocks:
                    if inner.name == "bullet":
                        add(inner, c.name)
        return out

    def _entry(self, key: str, b, shells: list, air: bool) -> dict | None:
        base = key.rpartition("/")[2].removesuffix(".blk")
        first = shells[0]
        kind = first.name
        bt = str(first.get("bulletType") or "").lower()
        if any(k in bt or k in key for k in _NOT_WEAPONS):
            return None
        if kind == "bullet" and first.block("rocket") is not None:
            # A ground launcher's missile: a shell whose flight is a rocket's.
            first, kind = first.block("rocket"), "rocket"
            bt = bt or str(first.get("bulletType") or "").lower()
        guidance = str(first.get("guidanceType") or "")
        names = [str(s.get("bulletName")) for s in shells if s.get("bulletName")]
        display = (self.wnames.lookup(base)[0] if self.wnames else "") or (
            self.wnames.lookup(names[0])[0] if self.wnames and names else "") or base
        detail: dict = {"blk": base}
        shape, cone, alt = "sphere", None, None
        if kind == "bullet":
            cal = _num(first.get("caliber"))
            mm = cal * 1000 if cal else None
            low = key.lower()
            cls = "mg" if "machinegun" in low or (mm is not None and round(mm) < 20) else "cannon" if mm is not None and mm <= 57 else "gun"
            most = max((_num(s.get("maxDistance"), 0) for s in shells), default=0)
            sight = _num(b.get("aimMaxDist"))
            best = sight if sight and sight > 0 else _GUN_BEST[cls]
            if not sight:
                detail["bestFrom"] = "class value"
            if not most:
                most = max(best, best * 2)
                detail["mostFrom"] = "class value"
            least = 0.0
            detail["calibre"] = _r(mm, 1)
            detail["shells"] = self._shells(b)
            if air:
                shape, cone = "cone", 10.0
        elif kind == "bomb":
            cls, shape, cone = "strike", "drop", 40.0
            least, best, most = 0.0, (5000.0 if guidance else 1000.0), (14000.0 if guidance else 6000.0)
            detail["rangeFrom"] = "class value (a bomb's throw is worked out from height and speed)"
            if guidance:
                detail["guidance"] = guidance
            m = _num(first.get("mass"))
            if m:
                detail["mass"] = _r(m)
        elif kind == "torpedo":
            cls = "torpedo"
            most = _num(first.get("maxDistance")) or _num(first.get("distToLive")) or 0.0
            if not most:
                return None
            least, best = 0.0, most * 0.6
            detail["bestFrom"] = "0.6 of the most"
            if _num(first.get("maxSpeedInWater")):
                detail["speed"] = _r(_num(first.get("maxSpeedInWater")), 1)
        else:  # rocket or missile
            g = first.block("guidance")
            cls = ("sam" if "sam" in bt or ("aam" in bt and not air) else "aam" if "aam" in bt else "atgm" if "atgm" in bt
                   else "strike" if air or not guidance else "atgm")
            least = _num(first.get("minDistance"), 0.0) or 0.0
            most = _num(first.get("maxDistance")) or _num(first.get("rangeMax")) or 0.0
            if not most:
                life, speed = _num(first.get("timeLife")), _num(first.get("endSpeed"))
                most = life * speed * 0.5 if life and speed else 0.0
                detail["mostFrom"] = "half its flight time at its end speed"
            if not most:
                return None
            lock = _num(g.get("lockDistance")) if g is not None else None
            tables = []
            for t in sorted((c for c in (g.blocks if g is not None else []) if c.name.startswith("table")), key=lambda c: c.name):
                rmax = t.get("rangeMax")
                if isinstance(rmax, list):
                    tables.append({"altitude": _r(_num(t.get("altitude"))), "rangeMin": [_r(x) for x in (t.get("rangeMin") or [])],
                                   "rangeMax": [_r(x) for x in rmax]})
            if tables:
                detail["launchTables"] = tables
                vals = sorted(x for t in tables for x in t["rangeMax"] if x)
                best = vals[len(vals) // 2] if vals else most * 0.6
                detail["bestFrom"] = "the middle of its launch tables"
            elif lock and lock < most:
                best = lock
                detail["bestFrom"] = "the seeker's lock distance"
            else:
                best = most * 0.6
                detail["bestFrom"] = "0.6 of the most"
            if guidance:
                detail["guidance"] = guidance
            for k in ("loadFactorMax", "machMax", "endSpeed", "timeLife"):
                if _num(first.get(k)) is not None:
                    detail[k] = _r(_num(first.get(k)), 2)
            if lock:
                detail["lockDistance"] = _r(lock)
            seeker = next((g.block(s) for s in _SEEKERS if g is not None and g.block(s) is not None), None)
            if seeker is not None:
                detail["seeker"] = seeker.name
                ang = _num(seeker.get("angleMax")) or _num(seeker.get("lockAngleMax"))
                if ang:
                    detail["seekerAngle"] = _r(ang, 1)
                    cone = ang
            mina = _num(first.get("minimalAltitude")) or _num(shells[0].get("minimalAltitude")) or _num(b.get("minimalAltitude"))
            if cls == "sam" and mina is not None:
                alt = [_r(mina), _r(most)]
            if air or cls == "atgm":
                shape = "cone"
                cone = cone or 30.0
        best = min(most, max(least, best))
        e = {"id": f"local-wt-{base}", "cls": cls, "name": display, "range": [_r(least), _r(best), _r(most)], "shape": shape,
             "labels": self._labels(base, *names), "detail": {k: v for k, v in detail.items() if v not in (None, [], "")}}
        if cone:
            e["cone"] = _r(min(180.0, cone), 1)
        if alt:
            e["alt"] = alt
        return e

    # Sensors ---------------------------------------------------------------

    def sensor(self, path: str) -> str | None:
        key = path.lower().replace("\\", "/")
        if key in self._sensor_of:
            return self._sensor_of[key]
        self._sensor_of[key] = None
        b = self.blk(key)
        spec = self._sensor_spec(key, b) if b is not None else None
        if spec:
            self.sensors[spec["id"]] = spec
            self._sensor_of[key] = spec["id"]
        return self._sensor_of[key]

    @staticmethod
    def _receivers(b) -> tuple[list[float], list[float]]:
        """Azimuth and elevation limits covered by a warning receiver's `receivers`."""
        az, el = [], []
        for r in _walk(b, "receiver"):
            a, w = _num(r.get("azimuth"), 0.0), _num(r.get("azimuthWidth"))
            e, h = _num(r.get("elevation"), 0.0), _num(r.get("elevationWidth"))
            if w:
                az += [a - w / 2, a + w / 2]
            if h:
                el += [e - h / 2, e + h / 2]
        return az, el

    def _sensor_spec(self, key: str, b) -> dict | None:
        base = key.rpartition("/")[2].removesuffix(".blk")
        t = str(b.get("type") or "")
        name = str(b.get("name") or base)
        spec: dict = {"id": f"local-wt-{base}", "name": name, "mount": "hull"}
        detail: dict = {"blk": base}
        if t == "radar":
            tx = b.block("transivers")
            ranges, vis, modes = [], set(), []
            for c in (tx.blocks if tx is not None else []):
                rng = _num(c.get("range")) or (_num(c.block("receiver").get("range")) if c.block("receiver") is not None else None)
                rcs = _num(c.get("rcs")) or (_num(c.block("receiver").get("rcs")) if c.block("receiver") is not None else None)
                v = str(c.get("visibilityType") or "radar")
                vis.add(v)
                modes.append(c.name)
                if rng and rng >= 200:
                    ranges.append((c.name, rng, rcs, _num(c.get("rangeMax")), v))
            if not ranges:
                return None
            air = [x for x in ranges if x[0] not in ("gtm", "sea", "gmti", "ground")] or ranges
            nm, rng, rcs, rmax, v = max(air, key=lambda x: x[1])
            kind = {"infraRed": "irst", "optic": "camera", "radarIntercept": "esm"}.get(v, "radar")
            az, el = [], []
            sp = b.block("scanPatterns")
            pats = sp.blocks if sp is not None else []
            search = [p for p in pats if "search" in p.name.lower()] or pats
            for p in search:
                a, e = p.get("azimuthLimits"), p.get("elevationLimits")
                if isinstance(a, list):
                    az += a
                if isinstance(e, list):
                    el += e
            spec.update(kind=kind, range=_r(rng), rcsRef=_r(rcs, 2) if rcs else None)
            if az:
                spec["az"] = [_r(min(az), 1), _r(max(az), 1)]
            if el:
                spec["el"] = [_r(max(-90.0, min(el)), 1), _r(min(90.0, max(el)), 1)]
            low = {m.lower() for m in modes} | {p.name.lower() for p in pats}
            spec["modes"] = sorted({"search" if "search" in m else "tws" if "tws" in m else "track" if "track" in m or "lock" in m
                                    else "gmti" if m in ("gtm", "gmti") else "sea" if m == "sea" else "" for m in low} - {""})
            detail["transceivers"] = [{"name": n, "range": _r(r_), "rcs": _r(c_, 2) if c_ else None, "rangeMax": _r(m_), "visibility": v_}
                                      for n, r_, c_, m_, v_ in ranges]
            if rmax:
                detail["rangeMax"] = _r(rmax)
        elif t in ("rwr", "mlws", "lws"):
            rng = _num(b.get("range")) or _num(b.get("rangeTargetToSpot"))
            if not rng:
                return None
            az, el = self._receivers(b)
            spec.update(kind=t, range=_r(rng))
            spec["az"] = [-180, 180] if not az or max(az) - min(az) >= 359 else [_r(min(az), 1), _r(max(az), 1)]
            if el:
                spec["el"] = [_r(max(-90.0, min(el)), 1), _r(min(90.0, max(el)), 1)]
            tr = b.get("targetRange")
            if isinstance(tr, list):
                detail["targetRange"] = [_r(x) for x in tr]
        else:
            return None
        spec["detail"] = detail
        return spec

    # Units -----------------------------------------------------------------

    def _optics(self, b, air: bool) -> list[dict]:
        out: list[dict] = []
        nv: dict[str, dict] = {}

        def note_nv(block, mod: str = "") -> None:
            for c in block.blocks:
                low = c.name.lower()
                who = ("tgp" if "tpod" in low else "commander" if "commander" in low else "driver" if "driver" in low
                       else "pilot" if "pilot" in low else "gunner")
                d = nv.setdefault(who, {})
                if "thermal" in low:
                    d["thermal"] = {"gen": thermal_gen(c.get("resolution")), "resolution": c.get("resolution"), **({"mod": mod} if mod else {})}
                elif low.endswith("ir"):
                    d["nv"] = True

        for blk in [b.block("nightVision")] + [m.block("effects").block("nightVision") for m in (b.block("modifications").blocks if b.block("modifications") else [])
                                                if m.block("effects") is not None and m.block("effects").block("nightVision") is not None]:
            if blk is not None:
                mod = ""
                for m in (b.block("modifications").blocks if b.block("modifications") else []):
                    e = m.block("effects")
                    if e is not None and e.block("nightVision") is blk:
                        mod = m.name
                note_nv(blk, mod)
        ck, cv = b.block("cockpit"), b.block("commanderView")
        if air:
            if ck is not None and _num(ck.get("sightOutFov")):
                out.append({"who": "gunner", "fov": [_r(_num(ck.get("sightOutFov")), 2), _r(_num(ck.get("sightInFov"), _num(ck.get("sightOutFov"))), 2)], "mount": "hull"})
            tp = ck.get("targetingPodFov") if ck is not None else None
            if isinstance(tp, list) and len(tp) == 2:
                out.append({"who": "tgp", "fov": [_r(tp[0], 2), _r(tp[1], 2)], "mount": "turret"})
        else:
            if ck is not None and _num(ck.get("zoomOutFov")):
                out.append({"who": "gunner", "fov": [_r(_num(ck.get("zoomOutFov")), 2), _r(_num(ck.get("zoomInFov"), _num(ck.get("zoomOutFov"))), 2)], "mount": "gun"})
            if cv is not None and _num(cv.get("zoomOutFov")):
                out.append({"who": "commander", "fov": [_r(_num(cv.get("zoomOutFov")), 2), _r(_num(cv.get("zoomInFov"), _num(cv.get("zoomOutFov"))), 2)], "mount": "turret"})
        for o in out:
            o.update({"thermal": None, "nv": False, **nv.pop(o["who"], {})})
        for who, d in nv.items():  # night sights without a zoom of their own (a driver's)
            out.append({"who": who, "fov": None, "thermal": d.get("thermal"), "nv": bool(d.get("nv")),
                        "mount": "hull" if who in ("driver", "pilot") else "turret"})
        return out

    def unit(self, path: str, air: bool) -> dict | None:
        b = self.blk(path)
        if b is None:
            return None
        vid = path.rpartition("/")[2].removesuffix(".blk")
        weapons: list[str] = []
        for w in _walk(b, "Weapon"):
            if w.get("blk") and not w.get("dummy"):
                for i in self.weapon(str(w.get("blk")), air):
                    if i not in weapons:
                        weapons.append(i)
        for pr in _walk(b, "preset"):
            pb = self.blk(str(pr.get("blk"))) if pr.get("blk") else None
            for w in (_walk(pb, "Weapon") if pb is not None else []):
                if w.get("blk") and not w.get("dummy"):
                    for i in self.weapon(str(w.get("blk")), air):
                        if i not in weapons:
                            weapons.append(i)
        sensors: list[str] = []
        pods = {id(s) for p in _walk(b, "WeaponPreset") if p.get("hasTargetingPod") for s in _walk(p, "sensor")}
        for s in _walk(b, "sensor"):
            if not s.get("blk"):
                continue
            sid = self.sensor(str(s.get("blk")))
            if not sid:
                continue
            node = " ".join(str(x) for x in (_all(s, "node") + _all(s, "dmPart"))).lower()
            mount = "turret" if any(k in node for k in ("turret", "gun", "optic", "tower")) else "hull"
            az = self.sensors[sid].get("az")
            if not air and mount == "hull" and self.sensors[sid]["kind"] in ("radar", "irst", "camera") and az and az[1] - az[0] < 359:
                # A ground vehicle's tracking radar or sight that does not search all round turns with the turret.
                mount = "turret"
            kind = "tgp" if id(s) in pods else self.sensors[sid]["kind"]
            if mount != self.sensors[sid].get("mount") or kind != self.sensors[sid]["kind"]:
                # The same sensor mounted differently on this unit: its own entry.
                vid_sid = f"{sid}@{mount}{'-tgp' if kind == 'tgp' else ''}"
                if vid_sid not in self.sensors:
                    self.sensors[vid_sid] = {**self.sensors[sid], "id": vid_sid, "mount": mount, "kind": kind}
                sid = vid_sid
            if sid not in sensors:
                sensors.append(sid)
        # Laser rangefinders (a modification or the vehicle's own): a narrow beam along the gun.
        for e in [b] + [m.block("effects") for m in (b.block("modifications").blocks if b.block("modifications") else []) if m.block("effects") is not None]:
            if e.get("rangefinderMounted") and e.get("isLaser"):
                th = e.get("distanceThresholdMax")
                rng = max(th) if isinstance(th, list) and th else None
                if rng:
                    sid = f"local-wt-lrf-{_r(rng)}"
                    self.sensors.setdefault(sid, {"id": sid, "kind": "lrf", "name": "Laser rangefinder", "range": _r(rng),
                                                  "az": [-0.5, 0.5], "el": [-0.5, 0.5], "mount": "gun", "rcsRef": None, "detail": {}})
                    if sid not in sensors:
                        sensors.append(sid)
                    break
        names = [vid]
        if self.names:
            for n in self.names.lookup(vid)[:2]:
                if n and n not in names:
                    names.append(n)
        u = {"names": names, "weapons": weapons, "sensors": sensors, "optics": self._optics(b, air)}
        return u if weapons or sensors or u["optics"] else None


def build(archive, names=None, weapon_names=None, progress=None) -> dict:
    """The catalogue of one install's archive."""
    cat = Catalogue(archive, names, weapon_names)
    units: list[dict] = []
    files = sorted(archive.files)
    groups = (("gamedata/units/tankmodels/", False), ("gamedata/flightmodels/", True), ("gamedata/units/ships/", False))
    for prefix, air in groups:
        paths = [f for f in files if f.startswith(prefix) and f.endswith(".blk") and "/" not in f[len(prefix):]]
        for n, f in enumerate(paths):
            if progress and n % 200 == 0:
                progress(f"{prefix} {n}/{len(paths)}")
            try:
                u = cat.unit(f, air)
            except Exception as e:  # one unreadable unit never stops the catalogue
                if progress:
                    progress(f"skipped {f}: {type(e).__name__}")
                continue
            if u:
                units.append(u)
    return {"version": 1, "game": "wt", "name": "War Thunder", "source": "your installation",
            "built": time.strftime("%Y-%m-%dT%H:%M:%S"), "tool": f"heat3d-wt-replay {__version__}",
            "weapons": sorted(cat.weapons.values(), key=lambda w: w["id"]), "sensors": dict(sorted(cat.sensors.items())), "units": units}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="heat3d-wt-ranges",
                                 description="Builds a catalogue of weapon reach, sights and sensors from your own War Thunder installation")
    ap.add_argument("-o", "--out", type=Path, default=DEFAULT_OUT, help="the catalogue file to write (default ranges.json)")
    ap.add_argument("--game", help="the War Thunder folder (found if not given)")
    ap.add_argument("--quiet", action="store_true", help="no progress lines")
    args = ap.parse_args(argv)
    root = install.find_game(args.game)
    if root is None:
        print("War Thunder not found: pass --game <folder> or set HEAT3D_WT_GAME", file=sys.stderr)
        return 2
    from . import names
    from .vromfs import Vromfs

    archive = Vromfs(Path(root) / "aces.vromfs.bin")
    log = None if args.quiet else (lambda s: print(s, file=sys.stderr, flush=True))
    doc = build(archive, names.load(str(root)), names.load_weapons(str(root)), log)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    tmp = args.out.with_suffix(args.out.suffix + ".tmp")
    tmp.write_text(json.dumps(doc, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    tmp.replace(args.out)
    print(f"ok {args.out} {len(doc['weapons'])} weapons, {len(doc['sensors'])} sensors, {len(doc['units'])} units")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
