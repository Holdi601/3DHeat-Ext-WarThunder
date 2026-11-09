"""
`.3dheat` match containers: one file a match (the viewer's docs/container.md).

A ZIP with `manifest.json` first, then the table, the match document and the
sidecars. Parquet members are stored, not compressed (Parquet is compressed
already, and a stored member is one byte range the viewer reads in place);
text members (JSON) are deflated. Roles are open strings, every member says
its media type and, where it can, the convention it follows (`schema`);
`info` may carry `matches`, `references` and `extensions` (see the spec).
The same file is vendored into each converter, so no converter depends on
another.

    pack(table, info)   # <match>.parquet and its side files -> <match>.3dheat
"""

from __future__ import annotations

import glob
import hashlib
import json
import os
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path

FORMAT = "3dheat"
FORMAT_VERSION = "1.0"  # major.minor: readers take any minor of their major
# Sidecar words (docs/converters.md) and the converters' other side tables.
SIDE_ROLES = ("messages", "flight", "packets", "events", "entities", "props", "units", "combatlog", "strings",
              "raw", "effects", "objectives", "chat")
_SIDE = re.compile(rf"^\.({'|'.join(SIDE_ROLES)})\.parquet$", re.I)
_JSON = re.compile(r"^\.(\w+)\.json$", re.I)


def members_of(table: Path) -> list[tuple[str, Path]]:
    """The table and the files beside it that belong to it: `<match>.<role>.parquet`, `<match>.<word>.json`."""
    stem = table.name[: -len(".parquet")]
    out = [("table", table)]
    for p in sorted(table.parent.glob(glob.escape(stem) + ".*")):
        rest = p.name[len(stem):]
        m = _SIDE.match(rest) or _JSON.match(rest)
        if m and p.is_file():
            out.append((m.group(1).lower(), p))
    order = {"table": 0, "match": 1}
    return sorted(out, key=lambda rp: (order.get(rp[0], 2), rp[0]))


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


_MEDIA = {".parquet": "application/vnd.apache.parquet", ".pq": "application/vnd.apache.parquet",
          ".json": "application/json", ".csv": "text/csv", ".txt": "text/plain"}


def _table(path: Path) -> tuple[int | None, dict | None]:
    """A Parquet member's rows and the convention its footer names."""
    try:
        import pyarrow.parquet as pq

        md = pq.read_metadata(path)
        kv = md.metadata or {}
        schema = ({"id": "heat3d-acmi-table", "version": "1"} if b"acmi" in kv else
                  {"id": "heat3d-table", "version": "1"} if b"heat3d" in kv else None)
        return md.num_rows, schema
    except Exception:  # a member that is not Parquet after all is still kept whole
        return None, None


def _doc_schema(path: Path) -> dict | None:
    """A document's own `format` and `version`, from its start."""
    with path.open("rb") as f:
        head = f.read(4096).decode("utf-8", "replace")
    m = re.search(r'"format"\s*:\s*"([^"]+)"', head)
    v = re.search(r'"version"\s*:\s*"?([\w.]+)"?', head)
    return {"id": m.group(1), "version": v.group(1) if v else None} if m else None


def verify(path: Path, manifest: dict) -> None:
    """Every member read back whole: the ZIP CRC, size and sha256 as the manifest says. Raises on a mismatch."""
    with zipfile.ZipFile(path) as z:
        infos = z.infolist()
        if not infos or infos[0].filename != "manifest.json":
            raise ValueError(f"{path}: manifest.json is not the first member")
        if json.loads(z.read("manifest.json")) != manifest:
            raise ValueError(f"{path}: manifest differs")
        if len(infos) != len(manifest["members"]) + 1:
            raise ValueError(f"{path}: members not named in the manifest")
        for m in manifest["members"]:
            info = z.getinfo(m["name"])
            if (info.compress_type == zipfile.ZIP_STORED) != (m["compression"] == "stored"):
                raise ValueError(f"{path}: {m['name']} compressed the wrong way")
            h = hashlib.sha256()
            size = 0
            with z.open(info) as f:  # zipfile checks the CRC at the end
                for chunk in iter(lambda: f.read(8 << 20), b""):
                    h.update(chunk)
                    size += len(chunk)
            if size != m["bytes"] or h.hexdigest() != m["sha256"]:
                raise ValueError(f"{path}: {m['name']} differs from what was packed")


def pack(table: Path, info: dict, delete_loose: bool = True) -> Path:
    """
    `<match>.parquet` with its match document and sidecars into `<match>.3dheat`
    beside it, read back whole before the loose files are deleted (only with
    `delete_loose`). `info`: game, source, converter {name, version}, match,
    map, mode, started (each may be None). Written as `.part` and renamed.
    """
    table = Path(table)
    members = members_of(table)
    items = []
    for role, p in members:
        media = _MEDIA.get(p.suffix.lower(), "application/octet-stream")
        stored = not (media == "application/json" or media.startswith("text/"))
        it = {"name": p.name, "role": role, "media_type": media, "compression": "stored" if stored else "deflate",
              "bytes": p.stat().st_size, "sha256": _sha256(p)}
        if media == "application/vnd.apache.parquet":
            it["rows"], schema = _table(p)
        else:
            schema = _doc_schema(p) if media == "application/json" else None
        if schema:
            it["schema"] = schema
        items.append(it)
    roles: dict[str, str] = {}
    for it in items:
        roles.setdefault(it["role"], it["name"])
    manifest = {"format": FORMAT, "format_version": FORMAT_VERSION, **{k: info.get(k) for k in
                ("game", "source", "converter", "match", "map", "mode", "started")},
                **{k: info[k] for k in ("matches", "references", "extensions") if info.get(k) is not None},
                "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "roles": roles, "members": items}
    out = table.with_name(table.name[: -len(".parquet")] + ".3dheat")
    part = out.with_name(out.name + ".part")
    with zipfile.ZipFile(part, "w", allowZip64=True) as z:
        z.writestr("manifest.json", json.dumps(manifest, indent=1, ensure_ascii=False),
                   compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        for (role, p), it in zip(members, items):
            stored = it["compression"] == "stored"
            z.write(p, p.name, compress_type=zipfile.ZIP_STORED if stored else zipfile.ZIP_DEFLATED,
                    compresslevel=None if stored else 9)
    try:
        verify(part, manifest)
    except Exception:
        part.unlink(missing_ok=True)
        raise
    os.replace(part, out)
    if delete_loose:
        for _, p in members:
            p.unlink()
    return out
