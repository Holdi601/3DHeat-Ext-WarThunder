"""
`heat3d-wt-level list` and `heat3d-wt-level extract <level>... | --all -o <folder>`

Reads War Thunder's level files from the user's own install and writes each
level as `<folder>/<level>/<level>.glb`, `.json` and the tactical map PNGs.
Prints `ok <glb> <triangles>` or `failed <level>: <why>` per level; exits 1 when
any failed, 2 when the game was not found or nothing was asked for.
"""

from __future__ import annotations

import argparse
import fnmatch
import sys
import traceback
from pathlib import Path

from . import __version__
from .install import find_game
from .level import DEFAULT_MAX_GRID, DEFAULT_MAX_OBJECT_TRIANGLES, Game, build, describe


def _game(args) -> Game | None:
    root = find_game(args.game)
    if root is None:
        print("War Thunder not found: pass --game <folder> or set HEAT3D_WT_GAME", file=sys.stderr)
        return None
    from . import oodle

    oodle.load_oodle(root)
    return Game(root)


def main(argv: list[str] | None = None) -> int:
    try:
        import heat3d_update

        heat3d_update.startup("heat3d_ext_warthunder")
    except Exception:  # an update check never stops a conversion
        pass
    ap = argparse.ArgumentParser(prog="heat3d-wt-level", description="War Thunder levels into 3DHeat .glb levels")
    ap.add_argument("--version", action="version", version=f"heat3d-wt-level {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)
    ls = sub.add_parser("list", help="list the levels in the install")
    ls.add_argument("--game", help="War Thunder folder (default: found through Steam or the launcher)")
    ex = sub.add_parser("extract", help="extract levels")
    ex.add_argument("levels", nargs="*", help="level names (as `list` prints them; wildcards allowed)")
    ex.add_argument("--all", action="store_true", help="every level")
    ex.add_argument("-o", "--out", type=Path, required=True, help="output folder; each level goes in <out>/<level>/")
    ex.add_argument("--game", help="War Thunder folder")
    ex.add_argument("--max-grid", type=int, default=DEFAULT_MAX_GRID,
                    help=f"heightmap samples a side, per part (default {DEFAULT_MAX_GRID})")
    ex.add_argument("--no-objects", action="store_true", help="leave out buildings, trees and other placed objects")
    ex.add_argument("--max-object-triangles", type=int, default=DEFAULT_MAX_OBJECT_TRIANGLES,
                    help=f"budget for placed objects (default {DEFAULT_MAX_OBJECT_TRIANGLES:,}): over it, costly types become boxes")
    ex.add_argument("--no-texture", action="store_true", help="do not texture the ground with the tactical map")
    ex.add_argument("--skip-existing", action="store_true", help="leave levels whose .glb exists")
    args = ap.parse_args(argv)

    try:
        game = _game(args)
    except Exception as e:
        print(f"failed: {e}", file=sys.stderr)
        return 2
    if game is None:
        return 2
    levels = game.levels()
    if args.cmd == "list":
        for p in levels:
            try:
                d = describe(game, p)
            except Exception as e:
                print(f"{p.stem}\tunreadable: {e}")
                continue
            terrain = []
            if "heightmap" in d:
                hm = d["heightmap"]
                terrain.append(f"heightmap {hm['samples'][0]}x{hm['samples'][1]} @ {hm['cell']:g} m")
            if d.get("landTracer"):
                terrain.append("land mesh")
            print(f"{p.stem}\t{', '.join(terrain) or 'no terrain'}\tmaps: {', '.join(d['maps']) or '-'}")
        print(f"{len(levels)} levels in {game.root}", file=sys.stderr)
        return 0

    wanted = [p for p in levels if args.all or any(fnmatch.fnmatch(p.stem, w) for w in args.levels)]
    if not wanted:
        print("no level matches (see `heat3d-wt-level list`)", file=sys.stderr)
        return 2
    failed = 0
    for p in wanted:
        dest = args.out / p.stem
        if args.skip_existing and (dest / f"{p.stem}.glb").exists():
            print(f"skip {dest / (p.stem + '.glb')}")
            continue
        try:
            rec = build(game, p, dest, max_grid=args.max_grid, textures=not args.no_texture, objects=not args.no_objects, max_object_triangles=args.max_object_triangles,
                        log=lambda s: print(s, flush=True))
            print(f"ok {dest / (p.stem + '.glb')} {sum(rec['triangles'].values())} triangles", flush=True)
        except Exception as e:
            failed += 1
            print(f"failed {p.stem}: {type(e).__name__}: {e}", flush=True)
            if "HEAT3D_DEBUG" in __import__("os").environ:
                traceback.print_exc()
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
