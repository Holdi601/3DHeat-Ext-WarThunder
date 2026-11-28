"""
The standalone app's description of this tool (app/spec.py): the War Thunder
install it reads, the checks before a level can be extracted, the levels as
maps (new ones after a game update are found by app/manifest.py), and the
replay conversion as a task. `python -m heat3d_ext_warthunder.standalone_spec`
runs the app from a checkout; the release executables run the same.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

from . import __version__
from .app import paths
from .app.spec import Check, GameSpec, Input, MapSource, Replays, Spec, Task


def _find(given: str | None) -> Path | None:
    from .install import find_game

    return find_game(given)


#: Levels no multiplayer mission is played on, by name, where the missions cannot be read: hangar scenes, the test
#: drive and test flight ranges.
_NOT_MAPS = re.compile(r"^(hangar_|firing_range$|hvg_training_ground$)")


def _played_levels(game: Path) -> set[str] | None:
    """The levels a multiplayer mission of the install is played on (`layouts.mission_index`), or None when the
    missions cannot be read. Kept per `mis.vromfs.bin` in the tool's cache folder."""
    mis = game / "mis.vromfs.bin"
    try:
        st = mis.stat()
    except OSError:
        return None
    key = hashlib.sha1(f"{mis.resolve()}|{st.st_size}|{st.st_mtime_ns}".encode()).hexdigest()[:12]
    cache = paths.data_dir() / "cache" / f"warthunder-played-levels-{key}.json"
    try:
        return set(json.loads(cache.read_text(encoding="utf-8")))
    except (OSError, ValueError):
        pass
    try:
        from . import layouts
        from .vromfs import Vromfs

        played = set(layouts.mission_index(Vromfs(mis)))
    except Exception:  # noqa: BLE001  unreadable missions: every level stays listed
        return None
    try:
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(sorted(played)), encoding="utf-8")
    except OSError:
        pass
    return played


def _maps(game: Path) -> list[MapSource]:
    """The levels of the install that multiplayer battles are played on. Hangar scenes, test ranges, tutorial and
    unused levels (no multiplayer mission names them) are not maps a replay can be on, and are left out."""
    played = _played_levels(game)
    out = []
    for p in sorted((game / "levels").glob("*.bin")):
        if (played is not None and p.stem not in played) or (played is None and _NOT_MAPS.search(p.stem)):
            continue
        out.append(MapSource(p.stem, p.stem, [p]))
    return out


# ---------------------------------------------------------------- content beside the maps

#: Content entries: id -> (title, what it is made from, the file it writes under <levels>/warthunder).
_CONTENT = {
    "catalog": ("Vehicles, soldiers, weapons, rounds, equipment and modifications",
                ("char.vromfs.bin", "aces.vromfs.bin", "lang.vromfs.bin"), "catalog.json"),
    "ranges": ("Weapon reach, sights and sensors", ("aces.vromfs.bin", "lang.vromfs.bin"), "ranges.json"),
}
_HAS_KIND = "kind" in getattr(MapSource, "__dataclass_fields__", {})


def _contents(game: Path) -> list[MapSource]:
    out = []
    for cid, (title, files, _dest) in _CONTENT.items():
        sources = [game / f for f in files if (game / f).is_file()]
        if sources:
            out.append(MapSource(cid, title, sources, kind="catalog" if cid == "catalog" else "ranges"))
    return out


def _extract_content(game: Path, m: MapSource, out: Path, log) -> list[Path]:
    if m.id == "catalog":
        from . import catalog

        return [catalog.build(game, out, log)]
    if m.id == "ranges":
        from . import ranges

        dest = out / _CONTENT["ranges"][2]
        code = ranges.main(["-o", str(dest), "--game", str(game), "--quiet"])
        if code != 0:
            raise RuntimeError(f"heat3d-wt-ranges exited {code}")
        return [dest]
    raise ValueError(f"no content {m.id!r}")


def _existing(out: Path, m: MapSource) -> list[Path]:
    if getattr(m, "kind", "map") != "map" and m.id in _CONTENT:
        return [out / _CONTENT[m.id][2]]
    return [out / m.id / f"{m.id}.glb"]


def _catalog_items(game: Path) -> dict[str, list[str]]:
    from . import catalog

    return catalog.install_items(game)


def _extracted_items(out: Path) -> dict[str, list[str]]:
    from . import catalog

    return catalog.extracted_items(out)


#: The content hooks, where this copy of the kit has them (app/spec.py, `GameSpec.contents` ...).
_CONTENT_HOOKS = {"contents": _contents, "extract_content": _extract_content, "catalog_items": _catalog_items,
                  "extracted_items": _extracted_items} if _HAS_KIND else {}


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

def _replay_info(path: Path) -> dict:
    """`info <replay> --json`: the header only (replay_info.py)."""
    from .replay_info import info

    return info(path)


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
        existing_outputs=_existing,
        output_version="0.2.0",
        platforms=("windows-x64", "linux-x64", "macos-arm64"),
        **{k: v for k, v in _CONTENT_HOOKS.items() if k in GameSpec.__dataclass_fields__},
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
    replays=Replays("warthunder", (".wrpl",), lambda r, out: ["heat3d-wt-replay", str(r), "-o", str(out)], info=_replay_info),
    notice="Not affiliated with or endorsed by Gaijin Entertainment.",
)

if __name__ == "__main__":
    from . import update
    from .app.entry import main

    raise SystemExit(main(SPEC, apply_source=update.apply))
