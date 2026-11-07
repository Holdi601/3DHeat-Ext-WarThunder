"""Where War Thunder is installed: `--game`, `HEAT3D_WT_GAME`, Steam, or the Gaijin launcher's default."""

from __future__ import annotations

import os
import re
from pathlib import Path

_LIBRARY_PATH = re.compile(r'"path"\s*"([^"]+)"')
_STEAM_DEFAULTS = (r"C:\Program Files (x86)\Steam", r"C:\Program Files\Steam")
_LAUNCHER_DEFAULTS = (
    os.path.expandvars(r"%LOCALAPPDATA%\WarThunder"),
    r"C:\Program Files\WarThunder",
    r"C:\Program Files (x86)\WarThunder",
    r"C:\Games\WarThunder",
)


def steam_libraries() -> list[Path]:
    """Every Steam library folder this machine knows about."""
    roots: list[Path] = []
    seen: set[str] = set()
    for base in _STEAM_DEFAULTS:
        config = Path(base) / "config" / "libraryfolders.vdf"
        try:
            text = config.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for found in _LIBRARY_PATH.finditer(text):
            path = Path(found.group(1).replace("\\\\", "\\"))
            if str(path).lower() not in seen:
                seen.add(str(path).lower())
                roots.append(path)
    return roots


def is_game(path: Path) -> bool:
    return (path / "levels").is_dir() and (path / "aces.vromfs.bin").is_file()


def find_game(given: str | os.PathLike[str] | None = None) -> Path | None:
    """The first War Thunder folder found, or None."""
    candidates: list[Path] = []
    for g in (given, os.environ.get("HEAT3D_WT_GAME")):
        if g:
            candidates.append(Path(g))
    candidates += [lib / "steamapps" / "common" / "War Thunder" for lib in steam_libraries()]
    candidates += [Path(p) for p in _LAUNCHER_DEFAULTS]
    for c in candidates:
        if is_game(c):
            return c
    return None
