---
title: The match document
nav_order: 7
---

# The match document

![The start of a synthetic match document, and its keys](assets/img/match-document.svg)

`<match>.match.json` holds everything the replay says that is not a row of
the table. The viewer's Match tab reads it.

## The battle

| Key | What |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | the match id (as in the file name); the map's id; the level file it uses |
| `mission`, `missionKey` | the mission's name and its key in the game's text files |
| `battleClass`, `environment`, `weather` | as the header gives them |
| `sessionId`, `server` | the battle's session id; the server |
| `replayVersion`, `flightLayout` | the replay format's version; the flight-packet layout read (`2025` or `2026`) |
| `files` | the replay files read (one, or a server replay's parts) |
| `started`, `timePlayed`, `replayEnd` | start time (ISO, UTC); seconds played, from the results; seconds of the replay's last packet |
| `author`, `authorUserId` | the recording player and their Gaijin id (client replays) |
| `teams` | the teams in the battle (`1`, `2`) |
| `result` | `winner`, `status` (`success` or `fail`, the author's outcome), `authorTeam`, `teams` ([Economy](economy.md)) |
| `vehicleNames` | where the vehicle names came from (your install) and their language |
| `conventions` | the units and signs of the table: axes, time, life, track, alive, roll, and more |

## Everything else


| Key | What |
|---|---|
| `battle`, `difficulty`, `gameMode` | the battle mode: `difficulty` `AB` / `RB` / `SB` (and its name, and the header byte), `gameMode` `ground` / `air` / `naval`, the mission's mode (`Dom`, `Conq`, `Bttl`, `I2M`, ...) and its English name from your install (`Domination`, `Enduring Confrontation`), the allowed unit types (see [Battle mode](ground.md#battle-mode)) |
| `settings` | the mission blk after the header: mode, environment, weather, score and time limits, countries, allowed unit types, wind, and `stars` (latitude, longitude, date, local time) |
| `sky` | the first `CustomWeatherParams`: sun and moon direction, wind, sky colours, cloud offsets |
| `players`, `slots` | the results' line per player (kills, ground kills, deaths, assists, score, captures, squad, clan, country, line-up, the uids they drove); the replay's player slots (name, user id, team) |
| `units` | every unit entity the replay created: eid, uid, template, vehicle, kind, type, team, player, mission name, when it was created and removed, where it was created, which components could not be read |
| `objects` | the mission's named objects: capture zones and airfields with their position and size, airfields' outlines as points, spawn areas |
| `objectives` | the battle's objectives, each `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (the replay's 1 or 2, empty for both), `name` (a capture zone its letter, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) with `position`, `radius` / `height` / `size` and `heading`, `source` (`replay` or `mission`) and what else is known (see [Objectives](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | with names and vehicles of both sides; kills with the weapon's English name |
| `weapons` | every rocket, missile, bomb, torpedo, drop tank and jettisoned load: when, where released (position, attitude, velocity), by which unit (the nearest within 300 m and 1.5 s), how many flight samples, where last seen, when removed |
| `explosions`, `flak` | `PlayExplosionVisual` (position, direction, kind) and `PlayFlakExplosionVisual` (position) |
| `awards` | the recording player's awards (`TextStreak`: first_blood, streaks, challenge counters) |
| `detections`, `unitStates` | `UnitDetected` pairs of units; a message (0xF093) with a unit's position, attitude and velocity whose meaning is not known |
| `authorInstruments` | the recording player's cockpit values (`ReplayCockpitParams`) by instrument number, at most one per second; `known` names each number this replay sent (name, unit, how it was checked), `notNamed` the rest |
| `scoreboard` | every player's statistics each time they changed (kills, deaths, assists, score, ai kills, naval kills, zones, damage, missile evades, squad), and each team's score and likely tickets over time (see [Reflection data](aircraft.md#reflection-data)) |
| `economy` | the battle's Silver Lions and research points (see [Economy](economy.md)): totals, per player, per vehicle, the multipliers, the winner, the checks |
| `entityMessages` | the entity messages (0x20) by class number: count, target templates, sizes |
| `chat` | every chat line |
| `triggers`, `hints`, `missionProgress` | the mission script's actions (RunTriggerAction), its hints, its progress messages |
| `camera` | the recording player's replay camera's fields every 0.25 s as sent (the table has it as a track) |
| `projectileHitReplays` | the recording player's own hits and being hit, with weapon and ammunition and their English names |
| `results` | the whole results blk as the game wrote it |
| `counts` | rows, events, lives, kinds, samples, entities by template, weapons, packets read and not read, every message id seen and those not read, samples dropped |
| `trackBreaks` | every cut of a track for a step faster than the unit can go: where, how far, how fast, and what it most likely is |
| `selfCheck` | the checks listed in [How it reads a replay](how-it-reads.md), computed on every conversion; `stepSpeed` gives per kind the speed between consecutive rows of a track as the viewer joins them (median, 99th percentile, highest, and steps faster than possible, which must be 0) |

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
