"""
`heat3d-wt-replay <replay, folder or zip>... -o <folder>`

Each battle becomes one file, `<folder>/<map>/<match>.3dheat` (container.py):
the table `<match>.parquet`, `<match>.match.json` and the sidecars packed
together; `--loose` keeps them as separate files.
Files of one battle (a server replay's parts) are read together; files of
different battles are converted one battle at a time. A .zip (a server
replay as downloaded) is read for the .wrpl files in it. Prints one line per
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
import json
import shutil
import sys
import tempfile
import zipfile
from collections import defaultdict
from pathlib import Path

from . import __version__, names
from .container import pack
from .convert import convert
from .wrpl import FormatError, read_header


def unzip(archive: Path, into: Path) -> list[Path]:
    """
    The .wrpl members of a zip, written flat into `into` (a folder of its own per zip: the
    member's file name only, never its path; a name met twice gets the folder's number).
    """
    out: list[Path] = []
    with zipfile.ZipFile(archive) as z:
        for info in z.infolist():
            name = Path(info.filename.replace("\\", "/")).name
            if info.is_dir() or not name.lower().endswith(".wrpl"):
                continue
            target = into / name
            if target.exists():
                target = into / f"{len(out)}_{name}"
            with z.open(info) as src, target.open("wb") as dst:
                shutil.copyfileobj(src, dst)
            out.append(target)
    return sorted(out)


def battles(inputs: list[Path], scratch: Path | None = None) -> tuple[dict[str, list[Path]], list[tuple[Path, str]]]:
    """
    The .wrpl files given (folders: the .wrpl files in them; zips: the .wrpl files in them,
    unpacked into `scratch`), grouped by battle.
    """
    files: list[Path] = []
    bad: list[tuple[Path, str]] = []
    for n, p in enumerate(inputs):
        if p.is_dir():
            files += sorted(p.glob("*.wrpl"))
        elif p.suffix.lower() == ".zip":
            if scratch is None:
                bad.append((p, "a zip needs a folder to unpack into"))
                continue
            into = scratch / str(n)
            into.mkdir(parents=True, exist_ok=True)
            try:
                found = unzip(p, into)
            except (OSError, zipfile.BadZipFile) as e:
                bad.append((p, f"not a readable zip: {e}"))
                continue
            if not found:
                bad.append((p, "no .wrpl file in the zip"))
            files += found
        else:
            files.append(p)
    groups: dict[str, list[Path]] = defaultdict(list)
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


def _info(doc: Path) -> dict:
    """What the container's manifest says of the battle, from its match document."""
    d = json.loads(doc.read_text(encoding="utf-8"))
    return {"game": "warthunder", "source": "server replay" if d.get("server") else "client replay",
            "converter": {"name": "heat3d-wt-replay", "version": __version__}, "match": d.get("match"),
            "map": d.get("map"), "mode": " ".join(x for x in (d.get("difficulty"), d.get("gameMode")) if x) or None,
            "started": d.get("started")}


def main(argv: list[str] | None = None) -> int:
    # A newer release is offered, and installed only if the user says yes (notified only when nobody can be asked).
    try:
        import heat3d_update

        heat3d_update.startup("heat3d_ext_warthunder")
    except Exception:  # an update check never stops a conversion
        pass
    ap = argparse.ArgumentParser(prog="heat3d-wt-replay", description="War Thunder replays (.wrpl) into 3DHeat tables")
    ap.add_argument("replays", nargs="+", type=Path, help=".wrpl files, folders of them, or zips of them")
    ap.add_argument("-o", "--out", type=Path, required=True, help="where to write <map>/<match>.parquet and .match.json")
    ap.add_argument("--game", help="the War Thunder folder whose localisation names the vehicles (found if not given)")
    ap.add_argument("--no-smoothing", action="store_true",
                    help="keep other units' dead-reckoned and received samples where the replay has them")
    ap.add_argument("--container", action="store_true",
                    help="pack each battle into one .3dheat file (the default)")
    ap.add_argument("--loose", action="store_true",
                    help="keep each battle as separate files (table, match.json, sidecars), not one .3dheat container")
    ap.add_argument("--version", action="version", version=f"heat3d-wt-replay {__version__}")
    args = ap.parse_args(argv)
    scratch = Path(tempfile.mkdtemp(prefix="heat3d-wt-"))
    try:
        return _run(args, scratch)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def _run(args: argparse.Namespace, scratch: Path) -> int:
    groups, bad = battles(args.replays, scratch)
    if not groups and not bad:
        print("no .wrpl files given", file=sys.stderr)
        return 2
    for f, why in bad:
        print(f"failed {f}: {why}")
    vehicle_names = names.load(args.game) if groups else names.Names()
    weapon_names = names.load_weapons(args.game) if groups else names.Weapons()
    if groups and not vehicle_names:
        print("note: no War Thunder install found to name the vehicles; the table names them by their ids")
    for files in groups.values():
        try:
            table, doc = convert(files, args.out, smoothing=not args.no_smoothing, names=vehicle_names,
                                 weapon_names=weapon_names)
        except (OSError, FormatError, EOFError, ValueError, IndexError) as e:
            print(f"failed {files[0]}: {type(e).__name__}: {e}")
            bad.append((files[0], str(e)))
            continue
        if args.loose:
            print(f"ok {table} {doc}")
            continue
        try:
            print(f"ok {pack(table, _info(doc))}")
        except (OSError, ValueError, zipfile.BadZipFile) as e:
            print(f"failed {files[0]}: packing {table.name}: {e} (the loose files are kept)")
            bad.append((files[0], str(e)))
    return 1 if bad else 0
