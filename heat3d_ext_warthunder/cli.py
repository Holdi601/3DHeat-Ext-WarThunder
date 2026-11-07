"""
`heat3d-wt-replay <replay or folder>... -o <folder>`

Each battle becomes `<folder>/<map>/<match>.parquet` and `<match>.match.json`.
Files of one battle (a server replay's parts) are read together; files of
different battles are converted one battle at a time. Prints one line per
battle, `ok <table> <summary>` or `failed <file>: <why>`; exits 1 when any
failed, 2 when nothing was given.

Vehicles are named from the game's own localisation in your install (found
through Steam or the launcher's folders; `--game` or `HEAT3D_WT_GAME` say
where it is otherwise); without an install the names are the vehicle ids.
`--no-smoothing` leaves other units' tracks as the replay has them (the
client's dead reckoning is still marked; see convert.py).
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

from . import __version__, names
from .convert import convert
from .wrpl import FormatError, read_header


def battles(inputs: list[Path]) -> tuple[dict[str, list[Path]], list[tuple[Path, str]]]:
    """The .wrpl files given (folders: the .wrpl files in them), grouped by battle."""
    files: list[Path] = []
    for p in inputs:
        files += sorted(p.glob("*.wrpl")) if p.is_dir() else [p]
    groups: dict[str, list[Path]] = defaultdict(list)
    bad: list[tuple[Path, str]] = []
    for f in files:
        try:
            with f.open("rb") as fh:
                head = fh.read(2048)
            h = read_header(head)
            # A client replay and the server's parts of the same battle are two recordings.
            groups[f"{h['sessionId']}-{'server' if h['server'] else 'client'}"].append(f)
        except (OSError, FormatError) as e:
            bad.append((f, str(e)))
    return dict(groups), bad


def main(argv: list[str] | None = None) -> int:
    # A newer release is offered, and installed only if the user says yes (notified only when nobody can be asked).
    try:
        import heat3d_update

        heat3d_update.startup("heat3d_ext_warthunder")
    except Exception:  # an update check never stops a conversion
        pass
    ap = argparse.ArgumentParser(prog="heat3d-wt-replay", description="War Thunder replays (.wrpl) into 3DHeat tables")
    ap.add_argument("replays", nargs="+", type=Path, help=".wrpl files or folders of them")
    ap.add_argument("-o", "--out", type=Path, required=True, help="where to write <map>/<match>.parquet and .match.json")
    ap.add_argument("--game", help="the War Thunder folder whose localisation names the vehicles (found if not given)")
    ap.add_argument("--no-smoothing", action="store_true",
                    help="keep other units' dead-reckoned and received samples where the replay has them")
    ap.add_argument("--version", action="version", version=f"heat3d-wt-replay {__version__}")
    args = ap.parse_args(argv)
    groups, bad = battles(args.replays)
    if not groups and not bad:
        print("no .wrpl files given", file=sys.stderr)
        return 2
    for f, why in bad:
        print(f"failed {f}: {why}")
    vehicle_names = names.load(args.game) if groups else names.Names()
    if groups and not vehicle_names:
        print("note: no War Thunder install found to name the vehicles; the table names them by their ids")
    for files in groups.values():
        try:
            table, doc = convert(files, args.out, smoothing=not args.no_smoothing, names=vehicle_names)
        except (OSError, FormatError, EOFError, ValueError, IndexError) as e:
            print(f"failed {files[0]}: {type(e).__name__}: {e}")
            bad.append((files[0], str(e)))
            continue
        print(f"ok {table} {doc}")
    return 1 if bad else 0
