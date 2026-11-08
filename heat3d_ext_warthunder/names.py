"""
Vehicles' display names from the game's own localisation, read from your install at conversion time.

The game names a vehicle in `lang/units.csv` (inside `lang.vromfs.bin`, or as a
plain file in `<War Thunder>/lang/` when the game was told to use local
localisation files): one line per key, `;`-separated and quoted, the key first
and then one column per language (`<English>`, `<French>`, ...). A vehicle id
has up to four keys: `<id>_0` the full name ("Pz.Kpfw. III Ausf. J1"),
`<id>_1` and `<id>_shop` short ones ("Pz.III J1"), `<id>_2` its class. Ships
are also keyed by their folder (`ships/<id>_0`).

The names start with a glyph of the game's font that draws a country or event
mark (a block or geometric symbol, a control picture, a private-use code
point); those are dropped, as the viewer's fonts would draw them as boxes.

Nothing of the game's text is kept in this repository: the table written for
you carries the names, and only on your machine.
"""

from __future__ import annotations

import csv
import io
import os
import unicodedata

from . import install

#: The English column of the localisation table.
LANGUAGE = "<English>"


def _clean(text: str) -> str:
    """The name without the game font's mark glyphs; no-break spaces become spaces."""
    out = []
    for ch in text.replace(" ", " "):
        o = ord(ch)
        if 0xE000 <= o <= 0xF8FF or 0x2400 <= o <= 0x243F or 0x2580 <= o <= 0x25FF or 0x2600 <= o <= 0x26FF:
            continue
        if unicodedata.category(ch) == "Sm" and o > 0x7F:
            continue
        out.append(ch)
    return " ".join("".join(out).split())


def read_table(raw: bytes, language: str = LANGUAGE) -> dict[str, str]:
    """A localisation csv's keys (lower case) and their text in one language."""
    text = raw.decode("utf-8-sig", errors="replace")
    rows = csv.reader(io.StringIO(text), delimiter=";")
    head = next(rows, [])
    try:
        col = head.index(language)
    except ValueError:
        col = 1
    out: dict[str, str] = {}
    for row in rows:
        if len(row) > col and row[0]:
            out[row[0].lower()] = row[col]
    return out


class Names:
    """The vehicle names of one install (empty when none is found)."""

    def __init__(self, table: dict[str, str] | None = None, source: str = "") -> None:
        self.table = table or {}
        self.source = source

    @classmethod
    def from_game(cls, game: str | os.PathLike[str] | None = None, language: str = LANGUAGE) -> "Names":
        """The install's `units.csv`: a loose `lang/units.csv` if the game uses one, else the one in `lang.vromfs.bin`."""
        root = install.find_game(game)
        if root is None:
            return cls(source="")
        loose = root / "lang" / "units.csv"
        try:
            if loose.is_file():
                return cls(read_table(loose.read_bytes(), language), str(loose))
            archive = root / "lang.vromfs.bin"
            if archive.is_file():
                from .vromfs import Vromfs

                files = Vromfs(archive).files
                raw = files.get("lang/units.csv")
                if raw:
                    return cls(read_table(raw, language), f"{archive}:lang/units.csv")
        except (OSError, ValueError, KeyError):
            pass
        return cls(source="")

    def __bool__(self) -> bool:
        return bool(self.table)

    def lookup(self, vehicle: str, folder: str = "") -> tuple[str, str, str]:
        """(full name, short name, key) of a vehicle id; ("", "", "") when the game does not name it."""
        if not vehicle or not self.table:
            return "", "", ""
        low = vehicle.lower()
        prefixes = [""] + ([folder.lower().rstrip("/") + "/"] if folder else []) + ["ships/"]
        for p in prefixes:
            key = f"{p}{low}"
            full = self.table.get(key + "_0")
            if full:
                short = self.table.get(key + "_1") or self.table.get(key + "_shop") or full
                return _clean(full), _clean(short), f"{p}{vehicle}_0"
        return "", "", ""


class Weapons:
    """
    Weapons' and ammunition's display names from the install's
    `lang/units_weaponry.csv` and, for ammunition belts, `units_modifications.csv`: a weapon or bomb or missile by `weapons/<id>`
    ("20 mm ShVAK cannon", short `weapons/<id>/short` "ShVAK"), an
    ammunition type by `<id>/name` ("Fragmentation incendiary tracer shell",
    short `<id>/name/short` "FI-T"). Ids come as the replay names them: an
    ammunition (`frag_i_t`), a weapon (`us_aim_120c_5`, with or without
    `_default`), or a weapon's blk path (`gameData/Weapons/cannonShVAKS.blk`).
    """

    def __init__(self, table: dict[str, str] | None = None, source: str = "") -> None:
        self.table = table or {}
        self.source = source

    #: The localisation files read: weapons and ammunition, then ammunition belts (`<belt>/name`, "30 mm HE").
    FILES = ("units_weaponry.csv", "units_modifications.csv")

    @classmethod
    def from_game(cls, game: str | os.PathLike[str] | None = None, language: str = LANGUAGE) -> "Weapons":
        root = install.find_game(game)
        if root is None:
            return cls()
        table: dict[str, str] = {}
        sources = []
        try:
            files = None
            for name in cls.FILES:
                loose = root / "lang" / name
                if loose.is_file():
                    raw = loose.read_bytes()
                    sources.append(str(loose))
                else:
                    if files is None:
                        from .vromfs import Vromfs

                        archive = root / "lang.vromfs.bin"
                        files = Vromfs(archive).files if archive.is_file() else {}
                    raw = files.get(f"lang/{name}")
                    if raw:
                        sources.append(f"lang.vromfs.bin:lang/{name}")
                if raw:
                    for k, v in read_table(raw, language).items():
                        table.setdefault(k, v)
        except (OSError, ValueError, KeyError):
            pass
        return cls(table, "; ".join(sources))

    def __bool__(self) -> bool:
        return bool(self.table)

    def lookup(self, ident: str) -> tuple[str, str]:
        """(name, short name) of a weapon or ammunition id; ("", "") when the game does not name it."""
        if not ident or not self.table:
            return "", ""
        low = ident.lower().rpartition("/")[2]
        if low.endswith(".blk"):
            low = low[:-4]
        if low.endswith("_default"):
            low = low[: -len("_default")]
        for full, short in ((f"{low}/name", f"{low}/name/short"), (f"weapons/{low}", f"weapons/{low}/short"),
                            (low, f"weapons/{low}/short")):
            text = self.table.get(full)
            if text:
                return _clean(text), _clean(self.table.get(short) or text)
        return "", ""


class Missions(Weapons):
    """
    Battle modes' display names from the install's `lang/missions_versus.csv`: the mission key's mode
    (`missions/_Dom` "Domination", `missions/_I2M` "Enduring Confrontation"), without the brackets the
    game puts around them.
    """

    FILES = ("missions_versus.csv",)

    def lookup(self, ident: str) -> tuple[str, str]:
        text = self.table.get(ident.lower()) if ident and self.table else None
        if not text:
            return "", ""
        # The game font's mode marks (box-drawing and private-use characters) are left out.
        text = "".join(c for c in _clean(text) if not (0x2500 <= ord(c) <= 0x25FF or 0xE000 <= ord(c) <= 0xF8FF))
        return text.strip("[] "), ""


def load_missions(game: str | os.PathLike[str] | None = None) -> Missions:
    """The battle modes' names of the install found; `HEAT3D_WT_NO_NAMES=1` turns them off."""
    if os.environ.get("HEAT3D_WT_NO_NAMES"):
        return Missions()
    return Missions.from_game(game)


def load_weapons(game: str | os.PathLike[str] | None = None) -> Weapons:
    """The weapon names of the install found; `HEAT3D_WT_NO_NAMES=1` turns them off."""
    if os.environ.get("HEAT3D_WT_NO_NAMES"):
        return Weapons()
    return Weapons.from_game(game)


def load(game: str | os.PathLike[str] | None = None) -> Names:
    """The names of the install found (see `install.find_game`); `HEAT3D_WT_NO_NAMES=1` turns them off."""
    if os.environ.get("HEAT3D_WT_NO_NAMES"):
        return Names()
    return Names.from_game(game)


__all__ = ["Names", "Weapons", "Missions", "load", "load_weapons", "load_missions", "read_table", "LANGUAGE"]
