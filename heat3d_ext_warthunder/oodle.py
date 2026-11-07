"""
Oodle decompression, through the library War Thunder itself ships.

The game's level files and texture packs are mostly Oodle-compressed. Oodle is
proprietary (RAD Game Tools, now Epic) and has no redistributable build, so
this module finds a copy that is already on the machine and never carries one.
War Thunder puts `oo2core_9_win64.dll` in its `win-arm64ec` folder, which is an
ordinary x64 build; that is the first place looked.

Order: an explicit path, `HEAT3D_OODLE` (the file or a folder holding it), the
game's own folders, then a shallow look through every Steam library.
"""

from __future__ import annotations

import ctypes
import os
from pathlib import Path

_DLL_NAMES = tuple(f"oo2core_{v}_win64.dll" for v in range(9, 2, -1))

_library: ctypes.CDLL | None = None
_library_path: Path | None = None


class OodleUnavailable(Exception):
    """No usable Oodle library, or a block that did not decompress."""


def _candidates(game: Path | None, extra: str | os.PathLike[str] | None) -> list[Path]:
    out: list[Path] = []
    for given in (extra, os.environ.get("HEAT3D_OODLE")):
        if not given:
            continue
        p = Path(given)
        out += [p / n for n in _DLL_NAMES] if p.is_dir() else [p]
    roots: list[Path] = []
    if game:
        roots += [game / "win-arm64ec", game / "win64", game]
    from .install import steam_libraries

    for lib in steam_libraries():
        common = lib / "steamapps" / "common"
        roots.append(common / "War Thunder" / "win-arm64ec")
        try:
            roots += [c for c in common.iterdir() if c.is_dir()]
        except OSError:
            pass
    for r in roots:
        out += [r / n for n in _DLL_NAMES]
    return out


def find_oodle(game: Path | None = None, extra: str | os.PathLike[str] | None = None) -> Path | None:
    for c in _candidates(game, extra):
        if c.is_file():
            return c
    return None


def load_oodle(game: Path | None = None) -> ctypes.CDLL:
    """Load the library once and keep it; raise `OodleUnavailable` if there is none."""
    global _library, _library_path
    if _library is not None:
        return _library
    errors: list[str] = []
    for found in _candidates(game, None):
        if not found.is_file():
            continue
        try:
            library = ctypes.CDLL(str(found))
            fn = library.OodleLZ_Decompress
        except (OSError, AttributeError) as e:  # an Arm64EC-only build, or not Oodle at all
            errors.append(f"{found}: {e}")
            continue
        fn.restype = ctypes.c_ssize_t
        fn.argtypes = [
            ctypes.c_void_p, ctypes.c_ssize_t, ctypes.c_void_p, ctypes.c_ssize_t,
            ctypes.c_int, ctypes.c_int, ctypes.c_int,
            ctypes.c_void_p, ctypes.c_ssize_t, ctypes.c_void_p, ctypes.c_void_p,
            ctypes.c_void_p, ctypes.c_ssize_t, ctypes.c_int,
        ]
        _library, _library_path = library, found
        return library
    raise OodleUnavailable(
        "no Oodle library found. War Thunder's level files are Oodle-compressed.\n"
        "  The game ships one as <War Thunder>\\win-arm64ec\\oo2core_9_win64.dll; point at it (or any\n"
        "  other oo2core_*_win64.dll) with HEAT3D_OODLE=<path>. It is proprietary, so this tool does not include it."
        + ("\n  tried: " + "; ".join(errors) if errors else "")
    )


def library_path() -> Path | None:
    return _library_path


def decompress(payload: bytes, expected: int) -> bytes:
    """One Oodle block of known output length (Oodle cannot infer it)."""
    library = load_oodle()
    out = ctypes.create_string_buffer(expected)
    written = library.OodleLZ_Decompress(
        payload, len(payload), out, expected,
        1,  # fuzz safe: the input is untrusted
        0, 0, None, 0, None, None, None, 0,
        3,  # unthreaded
    )
    if written != expected:
        raise OodleUnavailable(f"Oodle returned {written} bytes where {expected} were expected")
    return out.raw[:expected]
