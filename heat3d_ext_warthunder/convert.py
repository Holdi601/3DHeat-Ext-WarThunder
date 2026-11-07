"""
A replay as the 3DHeat viewer reads it: one Parquet table of every unit's
track and the kills and hits where they happened, and one match document.

The table carries its reading instructions in the Parquet footer under
`heat3d` (see 3DHeat's docs/data-formats.md): positions in the game's metres,
x east, y up, z north - so Y is up and Z is mirrored, or north would be drawn
south - the time in seconds of the replay's clock, the player, the team, the
life (a unit's track from spawn to death), the look direction as a vector,
and `Vehicle`, the game's own vehicle id, which the viewer's figures match.

A track's player comes from the replay's own records, never from a guess:
kills and hits name the uid, the player slot (pid) and the vehicle of whoever
dealt them, and the player slots name the player behind a pid. A unit that
never dealt a kill or a hit stays "uid <n>"; its vehicle stays empty unless its
player had only one vehicle of its kind (aircraft or ground) in the battle.
"""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import wrpl

#: Vehicle types in the results' crafts_info: which are aircraft.
AIR_TYPES = {"fighter", "assault", "bomber", "helicopter", "attack_helicopter", "utility_helicopter", "aircraft"}
#: A track is also cut where its unit is not seen for this long (s).
GAP = {"air": 30.0, "ground": 60.0}

#: How the viewer reads the table; see the module docstring.
HINTS = {
    "version": 1,
    "kind": "warthunder-replay",
    "game": "War Thunder",
    "axes": {"up": "y", "flipX": False, "flipY": False, "flipZ": True, "scale": 1},
    # A fighter is about 10 m long, a tank 7.
    "entity": {"size": 10},
    "columns": {
        "x": "x",
        "y": "y",
        "z": "z",
        "time": "time",
        "timeUnit": "seconds",
        "personId": "player",
        "teamId": "team",
        "sessionId": "life",
        "lookMode": "vector",
        "dirX": "dirX",
        "dirY": "dirY",
        "dirZ": "dirZ",
        "extra": ["event", "Vehicle", "kind", "uid", "other", "weapon", "heading", "pitch", "roll"],
    },
}

COLUMNS = [
    ("time", "f64"),
    ("event", "str"),
    ("player", "str"),
    ("userId", "str"),
    ("team", "str"),
    ("life", "str"),
    ("uid", "i16"),
    ("kind", "str"),
    ("Vehicle", "str"),
    ("x", "f32"),
    ("y", "f32"),
    ("z", "f32"),
    ("dirX", "f32"),
    ("dirY", "f32"),
    ("dirZ", "f32"),
    ("heading", "f32"),
    ("pitch", "f32"),
    ("roll", "f32"),
    ("other", "str"),
    ("weapon", "str"),
]


@dataclass
class Sample:
    t: float
    x: float
    y: float
    z: float
    attitude: int | None = None


@dataclass
class Life:
    uid: int
    kind: str
    n: int
    samples: list[Sample]
    pid: int | None = None
    vehicle: str = ""
    player: str = ""
    user_id: str = ""
    team: str = ""
    #: When it was killed (replay seconds); the samples after it are its wreck.
    died: float | None = None

    @property
    def id(self) -> str:
        return f"{self.uid}#{self.n}"

    @property
    def start(self) -> float:
        return self.samples[0].t

    @property
    def end(self) -> float:
        return self.samples[-1].t


@dataclass
class Replay:
    """What was read from one battle's replay file(s)."""

    files: list[str]
    header: dict[str, Any]
    results: dict[str, Any]
    slots: dict[int, dict[str, Any]]
    tracks: dict[tuple[str, int], list[Sample]]
    kills: list[dict[str, Any]]
    hits: list[dict[str, Any]]
    chat: list[dict[str, Any]]
    end_ms: int
    layout: str
    problems: Counter = field(default_factory=Counter)
    packets: Counter = field(default_factory=Counter)


def _decompress():
    try:
        import zstandard
    except ImportError:
        return None
    return lambda b: zstandard.ZstdDecompressor().stream_reader(b).read()


def read(paths: list[Path]) -> Replay:
    """
    One battle from its file or, for a server replay, its parts (every file
    must be of the same session; they are read in part order).
    """
    parts = []
    for p in paths:
        buf = Path(p).read_bytes()
        parts.append((wrpl.read_header(buf), buf, str(p)))
    sessions = {(h["sessionId"], h["server"]) for h, _, _ in parts}
    if len(sessions) > 1:
        raise wrpl.FormatError(f"files of {len(sessions)} different battles; give one battle's files at a time")
    parts.sort(key=lambda t: t[0]["part"])
    header = dict(parts[0][0])
    results: dict[str, Any] = {}
    slots: dict[int, dict[str, Any]] = {}
    tracks: dict[tuple[str, int], list[Sample]] = defaultdict(list)
    kills: list[dict[str, Any]] = []
    hits: list[dict[str, Any]] = []
    chat: list[dict[str, Any]] = []
    problems: Counter = Counter()
    seen: Counter = Counter()
    ground = wrpl.GroundReader()
    unzstd = _decompress()
    end_ms = 0
    layout = ""
    for h, buf, _ in parts:
        if 0 < h["resultsOffset"] < len(buf):
            try:
                results = wrpl.read_blk(buf[h["resultsOffset"] :]) or results
            except (wrpl.FormatError, IndexError, ValueError):
                problems["results"] += 1
        stream = list(wrpl.packets(wrpl.packet_stream(buf, h)))
        if not layout:
            flight = [p.payload for p in stream if p.type == 2][:80]
            layout = wrpl.flight_layout(flight) if flight else ""
        for pk in stream:
            end_ms = max(end_ms, pk.ms)
            t = pk.ms / 1000.0
            if pk.type == 2:
                seen["flight"] += 1
                entries, err = wrpl.read_flight(pk.payload, layout or "2026")
                if err:
                    # A list that does not parse to its end is not trusted at all.
                    problems["flight"] += 1
                    entries = []
                for uid, x, y, z, att in entries:
                    if _plausible(x, y, z):
                        tracks[("air", uid)].append(Sample(t, x, y, z, att))
            elif pk.type == 3:
                try:
                    chat.append({"t": t, **wrpl.read_chat(pk.payload)})
                except wrpl.FormatError:
                    problems["chat"] += 1
            elif pk.type == 4:
                m = pk.message
                try:
                    if m == wrpl.KILL:
                        seen["kill"] += 1
                        kills.append({"t": t, **wrpl.read_kill(pk.payload)})
                    elif m in (wrpl.CRITICAL, wrpl.SEVERE):
                        seen["hit"] += 1
                        hits.append({"t": t, "severity": "critical" if m == wrpl.CRITICAL else "severe",
                                     **wrpl.read_damage(pk.payload)})
                    elif m == wrpl.SLOTS:
                        seen["slots"] += 1
                        for k, v in wrpl.read_slots(pk.payload, unzstd).items():
                            slots.setdefault(k, {}).update(v)
                    elif m in (wrpl.GROUND_CLIENT, wrpl.GROUND_SERVER):
                        seen["ground"] += 1
                        for uid, x, y, z in ground.read(pk.payload):
                            if _plausible(x, y, z):
                                tracks[("ground", uid)].append(Sample(t, x, y, z))
                except (wrpl.FormatError, EOFError, IndexError, ValueError):
                    problems[{wrpl.KILL: "kill", wrpl.SLOTS: "slots"}.get(m, "ground" if m in (
                        wrpl.GROUND_CLIENT, wrpl.GROUND_SERVER) else "hit")] += 1
    return Replay([p for _, _, p in parts], header, results, slots, dict(tracks), kills, hits, chat, end_ms,
                  layout, problems, seen)


def _plausible(x: float, y: float, z: float) -> bool:
    return all(math.isfinite(v) for v in (x, y, z)) and abs(x) < 200_000 and abs(z) < 200_000 and -1000 < y < 40_000


# ---------------------------------------------------------------- lives and who


def lives(r: Replay) -> list[Life]:
    """
    Every uid's samples cut into lives where the unit jumps further than it
    could move (a respawn, or the uid given to a new unit) or is not seen for
    long. A kill does not cut: the game goes on sending the wreck as it falls,
    and those samples stay in the life, after `died`. A life of one sample - a
    unit seen once where it spawned, then moved - is dropped.
    """
    deaths: dict[int, list[float]] = defaultdict(list)
    for k in r.kills:
        if k.get("victimUid", wrpl.NO_UID) != wrpl.NO_UID:
            deaths[k["victimUid"]].append(k["t"])
    # When a uid deals a kill or a hit after it died, it is a new unit by then.
    acts: dict[int, list[float]] = defaultdict(list)
    for k in r.kills:
        acts[k.get("killerUid", wrpl.NO_UID)].append(k["t"])
    for h in r.hits:
        acts[h.get("uid", wrpl.NO_UID)].append(h["t"])
    out: list[Life] = []
    for (kind, uid), samples in sorted(r.tracks.items()):
        samples = sorted(samples, key=lambda s: s.t)
        runs: list[list[Sample]] = []
        for s in samples:
            if runs:
                p = runs[-1][-1]
                dt = s.t - p.t
                far, per_second = wrpl.JUMP[kind]
                if math.dist((p.x, p.y, p.z), (s.x, s.y, s.z)) > far + per_second * dt or dt > GAP[kind]:
                    runs.append([])
            else:
                runs.append([])
            runs[-1].append(s)
        n = 0
        while runs:
            run = runs.pop(0)
            if len(run) < 2:
                continue
            # Killed while this run was seen, or within a moment of its last sample.
            died = min((t for t in deaths.get(uid, []) if run[0].t <= t <= run[-1].t + 1.0), default=None)
            if died is not None and any(died + 1.0 < t <= run[-1].t + 2.0 for t in acts.get(uid, [])):
                runs.insert(0, [q for q in run if q.t > died])
                run = [q for q in run if q.t <= died]
                if len(run) < 2:
                    continue
            n += 1
            life = Life(uid, kind, n, run)
            life.died = died
            out.append(life)
    return out


def players(r: Replay) -> dict[str, dict[str, Any]]:
    """The results' player table by user id, with each player's vehicles and their kinds."""
    ui = (r.results.get("uiScriptsData") or {}).get("playersInfo") or {}
    info = {str(v.get("id")): v for v in ui.values() if isinstance(v, dict)} if isinstance(ui, dict) else {}
    rows = r.results.get("player") or []
    rows = rows if isinstance(rows, list) else [rows]
    out: dict[str, dict[str, Any]] = {}
    for p in rows:
        if not isinstance(p, dict):
            continue
        uid = str(p.get("userId", ""))
        i = info.get(uid, {})
        crafts = i.get("crafts") if isinstance(i.get("crafts"), dict) else {}
        kinds = {}
        ci = i.get("crafts_info") if isinstance(i.get("crafts_info"), dict) else {}
        for v in ci.values():
            if isinstance(v, dict) and str(v.get("slot")) in crafts:
                kinds[crafts[str(v.get("slot"))]] = "air" if v.get("type") in AIR_TYPES else "ground"
        out[uid] = {**p, "vehicles": [crafts[k] for k in sorted(crafts)], "vehicleKinds": kinds,
                    "country": i.get("country"), "name": p.get("name") or i.get("name") or ""}
    for uid, i in info.items():
        if uid not in out:
            out[uid] = {"userId": uid, "name": i.get("name", ""), "team": i.get("team"), "vehicles": [],
                        "vehicleKinds": {}}
    return out


def identify(r: Replay, all_lives: list[Life], table: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """
    Gives each life its pid, vehicle, player and team from the replay's own
    records: who dealt a kill or a hit names their uid, pid and vehicle, and a
    kill names its victim's uid and pid (0 for units no player drives, so 0 is
    not taken).
    Returns how well the pids agreed with the results (a self-check).
    """
    seen: dict[int, list[tuple[float, int | None, str]]] = defaultdict(list)
    for k in r.kills:
        if k.get("killerUid", wrpl.NO_UID) != wrpl.NO_UID:
            seen[k["killerUid"]].append((k["t"], _pid(k.get("killerPid")), k.get("killerVehicle") or ""))
        # A victim's pid is 0 for units no player drives (and for slot 0): only another pid is taken.
        if k.get("victimUid", wrpl.NO_UID) != wrpl.NO_UID and _pid(k.get("victimPid")):
            seen[k["victimUid"]].append((k["t"] - 0.01, k["victimPid"], ""))
    for h in r.hits:
        if h.get("uid", wrpl.NO_UID) != wrpl.NO_UID:
            seen[h["uid"]].append((h["t"], _pid(h.get("pid")), h.get("vehicle") or ""))
    by_uid: dict[int, list[Life]] = defaultdict(list)
    for life in all_lives:
        by_uid[life.uid].append(life)
    agree = disagree = 0
    for uid, marks in seen.items():
        for t, pid, vehicle in marks:
            life = _life_at(by_uid.get(uid, []), t)
            if life is None:
                continue
            if pid is not None and life.pid is None:
                life.pid = pid
            if vehicle and not life.vehicle:
                life.vehicle = vehicle
    for life in all_lives:
        if life.pid is None:
            continue
        slot = r.slots.get(life.pid, {})
        life.player = slot.get("name", "")
        life.user_id = slot.get("userId", "")
        p = table.get(life.user_id, {})
        life.player = life.player or p.get("name", "")
        team = slot.get("team", p.get("team"))
        life.team = str(team) if team is not None else ""
        if life.vehicle and p:
            if life.vehicle in p.get("vehicles", []):
                agree += 1
            else:
                disagree += 1
        if not life.vehicle and p:
            mine = [v for v, k in p.get("vehicleKinds", {}).items() if k == life.kind]
            if len(mine) == 1:
                life.vehicle = mine[0]
    return {"lifeVehicleInPlayersCrafts": agree, "lifeVehicleNotInPlayersCrafts": disagree}


def _pid(v: Any) -> int | None:
    return v if isinstance(v, int) and 0 <= v < 0x7FF else None


def _life_at(candidates: list[Life], t: float) -> Life | None:
    best, gap = None, math.inf
    for life in candidates:
        if life.start - 2 <= t <= life.end + 2:
            d = 0.0 if life.start <= t <= life.end else min(abs(t - life.start), abs(t - life.end))
            if d < gap:
                best, gap = life, d
    return best


def _label(life: Life) -> str:
    return life.player or f"uid {life.uid}"


def _where(life: Life | None, t: float) -> Sample | None:
    """The life's last sample at or before t, if near enough."""
    if life is None:
        return None
    best = None
    for s in life.samples:
        if s.t <= t + 0.05:
            best = s
        else:
            break
    if best is None or t - best.t > wrpl.NEAR[life.kind]:
        return None
    return best


# ---------------------------------------------------------------- the table


def _attitude(s: Sample) -> tuple[float, ...] | None:
    """
    Compass heading, pitch and roll (degrees) and the look vector in the game's
    axes. The packed heading is counted from east: compass = heading + 90 deg
    (checked against the direction of travel on real replays).
    """
    if s.attitude is None:
        return None
    h, p, roll = wrpl._euler(s.attitude)
    compass = h + math.pi / 2
    cp = math.cos(p)
    return (math.sin(compass) * cp, math.sin(p), math.cos(compass) * cp,
            math.degrees(compass) % 360, math.degrees(p), math.degrees(roll))


def rows(r: Replay, all_lives: list[Life]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    by_uid: dict[int, list[Life]] = defaultdict(list)
    for life in all_lives:
        by_uid[life.uid].append(life)
        kind = "aircraft" if life.kind == "air" else "ground"
        for s in life.samples:
            row = {"time": s.t, "event": "wreck" if life.died is not None and s.t > life.died else "position", "player": _label(life), "userId": life.user_id,
                   "team": life.team, "life": life.id, "uid": life.uid, "kind": kind, "Vehicle": life.vehicle,
                   "x": s.x, "y": s.y, "z": s.z}
            a = _attitude(s)
            if a:
                row.update(dirX=a[0], dirY=a[1], dirZ=a[2], heading=a[3], pitch=a[4], roll=a[5])
            out.append(row)

    def at(uid: int | None, t: float) -> tuple[Life | None, Sample | None]:
        if uid is None or uid == wrpl.NO_UID:
            return None, None
        life = _life_at(by_uid.get(uid, []), t)
        return life, _where(life, t)

    for k in r.kills:
        killer, ks = at(k.get("killerUid"), k["t"])
        victim, vs = at(k.get("victimUid"), k["t"])
        names = (_label(killer) if killer else _uid_label(k.get("killerUid")),
                 _label(victim) if victim else _uid_label(k.get("victimUid")))
        for event, life, s, other in (("kill", killer, ks, names[1]), ("death", victim, vs, names[0])):
            if s is None or life is None:
                continue
            out.append({"time": k["t"], "event": event, "player": _label(life), "userId": life.user_id,
                        "team": life.team, "life": life.id, "uid": life.uid,
                        "kind": "aircraft" if life.kind == "air" else "ground", "Vehicle": life.vehicle,
                        "x": s.x, "y": s.y, "z": s.z, "other": other, "weapon": k.get("weapon", "")})
    for h in r.hits:
        victim, vs = at(h.get("victimUid"), h["t"])
        if vs is None or victim is None:
            continue
        attacker, _ = at(h.get("uid"), h["t"])
        out.append({"time": h["t"], "event": f"hit_{h['severity']}", "player": _label(victim),
                    "userId": victim.user_id, "team": victim.team, "life": victim.id, "uid": victim.uid,
                    "kind": "aircraft" if victim.kind == "air" else "ground", "Vehicle": victim.vehicle,
                    "x": vs.x, "y": vs.y, "z": vs.z,
                    "other": _label(attacker) if attacker else _uid_label(h.get("uid")),
                    "weapon": h.get("vehicle", "")})
    out.sort(key=lambda row: row["time"])
    return out


def _uid_label(uid: Any) -> str:
    return "" if uid in (None, wrpl.NO_UID) else f"uid {uid}"


def table(data: list[dict[str, Any]]):
    import numpy as np
    import pyarrow as pa

    arrays, fields = [], []
    for name, kind in COLUMNS:
        values = [row.get(name) for row in data]
        if kind == "str":
            arr = pa.array(["" if v is None else str(v) for v in values], type=pa.string()).dictionary_encode()
            fields.append(pa.field(name, pa.dictionary(pa.int32(), pa.string())))
        elif kind == "i16":
            mask = np.array([v is None for v in values], dtype=bool)
            arr = pa.array(np.array([0 if v is None else v for v in values], dtype=np.int16), mask=mask)
            fields.append(pa.field(name, pa.int16()))
        else:
            t = pa.float64() if kind == "f64" else pa.float32()
            arr = pa.array(np.array([np.nan if v is None else v for v in values], dtype=float), type=t,
                           from_pandas=True)
            fields.append(pa.field(name, t))
        arrays.append(arr)
    schema = pa.schema(fields, metadata={"heat3d": json.dumps(HINTS)})
    return pa.Table.from_arrays(arrays, schema=schema)


# ---------------------------------------------------------------- the match


def match_name(h: dict[str, Any]) -> str:
    when = datetime.fromtimestamp(h["startTime"], tz=timezone.utc).strftime("%Y-%m-%d_%H-%M-%S") if h.get(
        "startTime") else "unknown"
    return f"{h['map'] or 'unknown'}_{when}_{h['sessionId']}{'_server' if h.get('server') else ''}"


def _rate(all_lives: list[Life], kind: str) -> float | None:
    """Samples per second along the tracks of one kind: the median over lives of at least 10 samples."""
    rates = sorted((len(l.samples) - 1) / (l.end - l.start) for l in all_lives
                   if l.kind == kind and len(l.samples) >= 10 and l.end > l.start)
    return round(rates[len(rates) // 2], 2) if rates else None


def summary(r: Replay, all_lives: list[Life], table_rows: list[dict[str, Any]], check: dict[str, Any]) -> dict:
    h = r.header
    roster = players(r)
    uids: dict[str, set[int]] = defaultdict(set)
    for life in all_lives:
        if life.user_id:
            uids[life.user_id].add(life.uid)
    keys = ("kills", "groundKills", "navalKills", "teamKills", "aiKills", "aiGroundKills", "aiNavalKills",
            "assists", "deaths", "captureZone", "damageZone", "score", "awardDamage", "missileEvades")
    plist = []
    for uid, p in roster.items():
        plist.append({"name": p.get("name", ""), "userId": uid, "team": str(p.get("team", "")),
                      "clanTag": p.get("clanTag", ""), "squad": p.get("squadId"), "country": p.get("country"),
                      "vehicles": p.get("vehicles", []), "uids": sorted(uids.get(uid, ())),
                      **{k: p.get(k) for k in keys if k in p}})
    plist.sort(key=lambda p: (p["team"], -(p.get("score") or 0)))
    lives_by_uid: dict[int, list[Life]] = defaultdict(list)
    for life in all_lives:
        lives_by_uid[life.uid].append(life)

    def who(uid: Any, pid: Any, t: float) -> str:
        life = _life_at(lives_by_uid.get(uid, []), t) if uid not in (None, wrpl.NO_UID) else None
        if life and life.player:
            return life.player
        pid = _pid(pid)
        # 0 is also what units no player drives get; only another pid names someone.
        if pid and r.slots.get(pid, {}).get("name"):
            return r.slots[pid]["name"]
        return _uid_label(uid)

    kills = []
    for k in r.kills:
        kills.append({"time": round(k["t"], 3), "killer": who(k.get("killerUid"), k.get("killerPid"), k["t"]),
                      "killerVehicle": k.get("killerVehicle", ""), "victim": who(k.get("victimUid"),
                                                                               k.get("victimPid"), k["t"]),
                      "weapon": k.get("weapon", ""), "killerUid": k.get("killerUid"),
                      "victimUid": k.get("victimUid"), "crash": k.get("killerUid") == wrpl.NO_UID})
    air = [l for l in all_lives if l.kind == "air"]
    gnd = [l for l in all_lives if l.kind == "ground"]
    events = Counter(row["event"] for row in table_rows)
    start = datetime.fromtimestamp(h["startTime"], tz=timezone.utc).isoformat() if h.get("startTime") else None
    return {
        "format": "heat3d-wt-replay-match",
        "version": 1,
        "match": match_name(h),
        "map": h["map"],
        "level": h["level"],
        "mission": h["battleType"],
        "missionKey": h["locName"],
        "battleClass": h["battleClass"],
        "environment": h["environment"],
        "weather": h["visibility"],
        "sessionId": h["sessionId"],
        "server": h["server"],
        "replayVersion": h["version"],
        "flightLayout": r.layout,
        "files": [Path(f).name for f in r.files],
        "started": start,
        "timePlayed": r.results.get("timePlayed"),
        "replayEnd": round(r.end_ms / 1000.0, 3),
        "author": r.results.get("author"),
        "authorUserId": r.results.get("authorUserId"),
        "teams": sorted({p["team"] for p in plist if p["team"]}),
        "players": plist,
        "kills": kills,
        "hits": [{"time": round(x["t"], 3), "severity": x["severity"],
                  "attacker": who(x.get("uid"), x.get("pid"), x["t"]), "attackerVehicle": x.get("vehicle", ""),
                  "victim": who(x.get("victimUid"), None, x["t"])} for x in r.hits],
        "chat": [{"time": round(c["t"], 3), "sender": c.get("sender", ""), "text": c.get("text", "")}
                 for c in r.chat],
        "counts": {
            "rows": len(table_rows),
            "events": dict(events),
            "aircraftUids": len({l.uid for l in air}),
            "groundUids": len({l.uid for l in gnd}),
            "lives": len(all_lives),
            "identified": sum(1 for l in all_lives if l.player),
            "withVehicle": sum(1 for l in all_lives if l.vehicle),
            "aircraftSamples": sum(len(l.samples) for l in air),
            "groundSamples": sum(len(l.samples) for l in gnd),
            "aircraftHz": _rate(all_lives, "air"),
            "groundHz": _rate(all_lives, "ground"),
            "packets": dict(r.packets),
            "unreadPackets": dict(r.problems),
        },
        "selfCheck": check,
        "conventions": {
            "axes": "metres; x east, y up, z north (the game's own); the table's hints mirror z for the viewer",
            "time": "seconds of the replay's own clock",
            "life": "uid#n: a unit's track, cut where it jumps (respawn, uid reused) or is long unseen",
            "wreck": "rows after a unit's death: the game keeps sending the wreck",
            "player": "from the replay's kill and hit records and its player slots; 'uid <n>' when never named",
            "heading": "compass degrees, clockwise from north",
            "hits": "rows at the position of the unit hit; 'other' is who hit it, 'weapon' their vehicle",
        },
    }


def convert(paths: list[Path], out: Path) -> tuple[Path, Path]:
    """One battle's replay file(s) into `<out>/<map>/<match>.parquet` and `.match.json`."""
    import pyarrow.parquet as pq

    r = read(paths)
    all_lives = lives(r)
    check = identify(r, all_lives, players(r))
    data = rows(r, all_lives)
    name = match_name(r.header)
    folder = Path(out) / (r.header["map"] or "unknown")
    folder.mkdir(parents=True, exist_ok=True)
    tpath = folder / f"{name}.parquet"
    jpath = folder / f"{name}.match.json"
    pq.write_table(table(data), tpath, compression="snappy", row_group_size=256_000)
    jpath.write_text(json.dumps(summary(r, all_lives, data, check), indent=1, ensure_ascii=False), encoding="utf-8")
    return tpath, jpath
