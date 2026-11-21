"""
The standalone app's description of this tool (app/spec.py): the War Thunder
install it reads, the checks before a level can be extracted, the levels as
maps (new ones after a game update are found by app/manifest.py), and the
replay conversion as a task. `python -m heat3d_ext_warthunder.standalone_spec`
runs the app from a checkout; the release executables run the same.
"""

from __future__ import annotations

import sys
from pathlib import Path

from . import __version__
from .app import paths
from .app.spec import Check, GameSpec, Input, MapSource, Spec, Task


def _find(given: str | None) -> Path | None:
    from .install import find_game

    return find_game(given)


def _maps(game: Path) -> list[MapSource]:
    return [MapSource(p.stem, p.stem, [p]) for p in sorted((game / "levels").glob("*.bin"))]


def _extract(game: Path, m: MapSource, out: Path, log) -> list[Path]:
    from . import levelcli

    code = levelcli.main(["extract", m.id, "-o", str(out), "--game", str(game)])
    if code != 0:
        raise RuntimeError(f"heat3d-wt-level extract exited {code}")
    # Game-mode layouts where the level has missions; a level without any is not an error.
    levelcli.main(["layouts", m.id, "-o", str(out), "--game", str(game)])
    folder = out / m.id
    return sorted(p for p in folder.iterdir() if p.is_file() and not p.name.startswith("."))


def _build(game: Path) -> str | None:
    for name in ("content/pkg_main.ver", "version"):
        try:
            text = (game / name).read_text(encoding="utf-8", errors="replace").strip()
        except OSError:
            continue
        if text:
            return text.splitlines()[0][:40]
    return None


def _checks(found: dict, levels: Path) -> list[Check]:
    from .oodle import find_oodle

    game = found.get("warthunder")
    lib = find_oodle(game) if game else None
    return [Check(
        "oodle", "Oodle library (from your own War Thunder install)", lib is not None,
        str(lib) if lib else "not found; levels need it (replays do not). Set HEAT3D_OODLE to the file in your install.",
    )]


SPEC = Spec(
    id="heat3d-warthunder",
    name="3DHeat War Thunder",
    repo="Holdi601/3DHeat-Ext-WarThunder",
    version=__version__,
    tools={
        "heat3d-wt-replay": "heat3d_ext_warthunder.cli:main",
        "heat3d-wt-level": "heat3d_ext_warthunder.levelcli:main",
        "heat3d-wt-ranges": "heat3d_ext_warthunder.ranges:main",
    },
    default_tool="heat3d-wt-replay",
    description="War Thunder replays and levels for the 3DHeat viewer",
    module="heat3d_ext_warthunder.standalone_spec",
    games=[GameSpec(
        key="warthunder", label="War Thunder", find=_find, subdir="warthunder", build=_build,
        maps=_maps, extract=_extract,
        existing_outputs=lambda out, m: [out / m.id / f"{m.id}.glb"],
        output_version="0.2.0",
        platforms=("windows-x64", "linux-x64", "macos-arm64"),
    )],
    checks=_checks,
    tasks=[Task(
        "replays", "Convert replays",
        [Input("src", "Folder with .wrpl replays", "folder"),
         Input("out", "Where the matches go", "folder", default=lambda levels: str(paths.data_dir() / "matches" / "warthunder"))],
        lambda v, levels: ["heat3d-wt-replay", v["src"], "-o", v["out"]],
        help="each battle becomes one .3dheat file the viewer opens",
    )],
    min_free_gb=5.0,
    notice="Not affiliated with or endorsed by Gaijin Entertainment.",
)

if __name__ == "__main__":
    from . import update
    from .app.entry import main

    raise SystemExit(main(SPEC, apply_source=update.apply))
