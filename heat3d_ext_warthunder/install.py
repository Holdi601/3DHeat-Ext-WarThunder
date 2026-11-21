"""Where War Thunder is installed: `--game`, `HEAT3D_WT_GAME`, Steam (any system), or the Gaijin launcher's folders."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from .app import paths


def _launcher_defaults() -> list[Path]:
    home = Path.home()
    if sys.platform == "win32":
        return [Path(os.path.expandvars(r"%LOCALAPPDATA%\WarThunder")), Path(r"C:\Program Files\WarThunder"),
                Path(r"C:\Program Files (x86)\WarThunder"), Path(r"C:\Games\WarThunder")]
    if sys.platform == "darwin":
        return [home / "Library" / "Application Support" / "WarThunder", home / "WarThunder",
                Path("/Applications/WarThunder.app/Contents/Resources/game")]
    return [home / "WarThunder", home / ".local" / "share" / "WarThunder", home / "Games" / "WarThunder"]


def steam_libraries() -> list[Path]:
    """Every Steam library folder this machine knows about (Windows, Linux incl. flatpak and Steam Deck, macOS)."""
    return paths.steam_libraries()


def is_game(path: Path) -> bool:
    return (path / "levels").is_dir() and (path / "aces.vromfs.bin").is_file()


def find_game(given: str | os.PathLike[str] | None = None) -> Path | None:
    """The first War Thunder folder found, or None."""
    candidates: list[Path | str | None] = [given, os.environ.get("HEAT3D_WT_GAME")]
    candidates += paths.steam_game_dirs("War Thunder")
    candidates += _launcher_defaults()
    return paths.first(candidates, is_game)
