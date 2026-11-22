"""
What a War Thunder replay says about its battle, without converting it.

Reads only the fixed header, the mission settings blk right after it and
the results blk at the end of the file (see wrpl.py for the layout); the
packet stream in between is never decompressed. A server replay's part
(`0000.wrpl`, ...) or a zip of them reads the same: the header of the
lowest part, the results of whichever part carries them.

Everything is what the file holds; what it does not say is None or [].
"""

from __future__ import annotations

import struct
import zipfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from . import convert, wrpl

#: Bytes to read past the header for the settings blk and the gap after it.
_SETTINGS_SLACK = 64


def _parts(path: Path) -> list[tuple[str, Any]]:
    """(name, opener) of each .wrpl in `path`: the file itself, or the .wrpl members of a zip."""
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as z:
            names = [i.filename for i in z.infolist() if not i.is_dir() and i.filename.lower().endswith(".wrpl")]
        if not names:
            raise ValueError("not a War Thunder replay (a zip without .wrpl files)")
        return [(n, lambda n=n: _member(path, n)) for n in sorted(names)]
    return [(path.name, lambda: path.open("rb"))]


@contextmanager
def _member(archive: Path, name: str):
    with zipfile.ZipFile(archive) as z, z.open(name) as fh:
        yield fh


def _read_part(opener) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """One part's header, settings blk and results blk, each read on its own."""
    with opener() as fh:
        head = fh.read(wrpl.HEADER_SIZE)
        h = wrpl.read_header(head)
        settings: dict[str, Any] = {}
        if h["settingsSize"]:
            raw = head + fh.read(h["settingsSize"] + _SETTINGS_SLACK)
            try:
                settings = wrpl.read_settings(raw)
            except (wrpl.FormatError, IndexError, ValueError, struct.error):
                settings = {}
        results: dict[str, Any] = {}
        if h["resultsOffset"] > wrpl.HEADER_SIZE:
            try:
                fh.seek(h["resultsOffset"])
                results = wrpl.read_blk(fh.read()) or {}
            except (OSError, wrpl.FormatError, IndexError, ValueError, struct.error):
                results = {}
    return h, settings, results


def _num(v: Any) -> float | None:
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0 else None


def info(path: Path) -> dict:
    """The battle's map, mode, start, length, players, teams, outcome and replay version, from the header and results."""
    path = Path(path)
    try:
        parts = [_read_part(opener) for _, opener in _parts(path)]
    except wrpl.FormatError:
        raise ValueError("not a War Thunder replay") from None
    except (OSError, zipfile.BadZipFile, EOFError) as e:
        raise ValueError(f"not a readable War Thunder replay: {e}") from None
    if len({(h["sessionId"], h["server"]) for h, _, _ in parts}) > 1:
        raise ValueError("files of more than one battle")
    parts.sort(key=lambda p: p[0]["part"])
    h, settings, _ = parts[0]
    results = next((r for _, _, r in reversed(parts) if r), {})

    r = SimpleNamespace(header=h, settings=settings, results=results, slots={})
    roster = convert.players(r)
    mode = convert.battle_mode(r)
    players = []
    for uid, p in roster.items():
        row: dict[str, Any] = {"name": p.get("name") or "", "team": str(p["team"]) if p.get("team") not in (None, "")
                               else None}
        if p.get("clanTag"):
            row["clan"] = p["clanTag"]
        if p.get("vehicles"):
            row["vehicles"] = list(p["vehicles"])
        if p.get("country"):
            row["country"] = p["country"]
        if uid and not uid.startswith("name:"):
            row["userId"] = uid
        players.append(row)
    team_ids = sorted({p["team"] for p in players if p["team"] not in (None, "", "0")})

    outcome = None
    if results:
        res = convert.battle_result(r, roster)
        status = res.get("status")
        if res.get("winner") is not None or status:
            outcome = {"winner": res.get("winner"), "result": status}

    start = h.get("startTime")
    return {
        "map": h["map"] or None,
        "map_title": None,  # the header names the level by its id only
        "mode": " ".join(x for x in (mode["difficulty"], mode["gameMode"]) if x) or None,
        "mission_mode": mode["missionMode"] or None,
        "date": datetime.fromtimestamp(start, tz=timezone.utc).isoformat() if start else None,
        "duration_s": _num(results.get("timePlayed")),
        "players": players,
        "teams": [{"id": t} for t in team_ids],
        "outcome": outcome,
        "game_version": str(h["version"]) if h.get("version") else None,
        "session_id": h["sessionId"],
        "server_replay": bool(h.get("server")),
        "author": results.get("author") or None,
    }
