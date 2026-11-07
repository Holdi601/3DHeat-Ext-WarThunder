# 3DHeat War Thunder replay converter

War Thunder replays (`.wrpl`) into the table the 3DHeat viewer opens: every
aircraft's, tank's, ship's and AI unit's track with its vehicle, team and
player, the missiles, rockets, bombs and torpedoes in flight, and the kills,
hits, destroyed modules and launches where they happened. A match document
beside it holds everything else the replay says: the mission settings and
sky, every unit and weapon the replay created, the mission's zones and
airfields, explosions, awards, the recording player's instruments, the chat
and the whole results block.

```bash
pip install -e .                        # installs the `heat3d-wt-replay` command
heat3d-wt-replay "<War Thunder>/Replays" -o out
heat3d-wt-replay a.wrpl b.wrpl -o out   # files, folders, or both
python -m heat3d_ext_warthunder ...     # the same, without installing
```

Each battle becomes `out/<map>/<map>_<start, UTC>_<session id>.parquet` and
`.match.json`. A server replay's parts (`0000.wrpl`, `0001.wrpl`, ...) are read
together as one battle; a client replay and the server's parts of the same
battle are two recordings and stay two. The command prints `ok <table> <summary>`
or `failed <file>: <why>` per battle and exits 1 when any failed.

A second command turns the game's own levels into 3D levels for the viewer,
read from your install (see [Levels](#levels-heat3d-wt-level)):

```bash
heat3d-wt-level list                              # every level, its terrain and its maps
heat3d-wt-level extract <level> -o levels         # one level (names as `list` prints them, wildcards allowed)
heat3d-wt-level extract --all -o levels           # all of them
python -m heat3d_ext_warthunder.levelcli ...      # the same, without installing
```

## Why it is apart

The `.wrpl` format is undocumented, and Gaijin's EULA (3.2.2, 3.2.9) forbids
reverse engineering the game and mining data not meant to be shown; nothing
there names replays, which the game itself shows the player. The user decided
to read them. So that a licence question or a takedown touches only this
converter, it lives outside the 3DHeat Watcher: the watcher runs this command
on new replays when it is installed, imports nothing of it, and works without
it.

## Switching replays on

War Thunder saves client replays to `<War Thunder>/Replays/*.wrpl` when replay
saving is on in the game's options. A server replay of every battle can be
downloaded from warthunder.com's replay pages; that needs a signed-in account,
and nothing here downloads it.

## The table

One row per sample or event; in the footer, under `heat3d`, the viewer's
reading instructions, so the viewer needs no form filled in.

| Column | What |
|---|---|
| `time` | seconds on the replay's own clock |
| `event` | `position`; event rows lie on the track at their moment (between two samples, on the line between them); `kill` (at the killer), `death` (at the victim), `hit_critical` / `hit_severe` (at the unit hit), `module_destroyed` (at the unit), `launch` (at the unit that released a weapon), `impact` (a weapon's last sample when it was removed right after) |
| `track` | what the viewer draws as one thing: one life of a unit, or one weapon's flight - `<player or vehicle> #<hex>` (the viewer shows the name without the `#` part) |
| `x`, `y`, `z` | the game's metres: x east, y up, z north (the hints mirror z, so north is not drawn south) |
| `player` | the player's name; an AI unit `<vehicle> #<uid>`; `uid <n>` when nothing names it; for a weapon, who released it |
| `userId`, `team` | the player's Gaijin id and the team (`1`, `2`) |
| `life` | `uid#n`: one unit's track, cut where the uid passes to another unit, the unit moves faster than it can (a respawn, a rearm, the game moving it, the client correcting a distant unit; see below) or is long unseen; `w<hex>` a weapon's flight (`w<hex>#n` after a cut) |
| `uid` | the unit's id in the replay |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`; weapons `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned` |
| `type` | the game's own type where the results name it (`fighter`, `assault`, `destroyer`, `gun_boat`), else as `kind` |
| `Vehicle` | the game's vehicle id (`f_15a`, `germ_flakpz_I_Gepard`), which the viewer's figures match |
| `mission` | the unit's name in the mission (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | where the unit points (the look vector): aircraft from the flight model's attitude, ground units and ships from their own, weapons along their flight |
| `heading`, `pitch`, `roll` | the same in degrees; heading is the compass, clockwise from north |
| `speed` | m/s over about two seconds of the track (worked out here; the replay sends no speed for other units) |
| `alive` | 0 for a unit's samples after its death (its wreck), for at most 60 s or until the game removes it |
| `other`, `weapon` | kills: the other side and the weapon; hits: who hit, their vehicle; launches: the weapon; destroyed modules: the part's number |

The match document (`format: heat3d-wt-replay-match`, version 2) has the map,
mission, battle class, session id, start time and author, and:

| Key | What |
|---|---|
| `settings` | the mission blk after the header: mode, environment, weather, score and time limits, countries, allowed unit types, wind, and `stars` (latitude, longitude, date, local time) |
| `sky` | the first `CustomWeatherParams`: sun and moon direction, wind, sky colours, cloud offsets |
| `players`, `slots` | the results' line per player (kills, ground kills, deaths, assists, score, captures, squad, clan, country, line-up, the uids they drove); the replay's player slots (name, user id, team) |
| `units` | every unit entity the replay created: eid, uid, template, vehicle, kind, type, team, player, mission name, when it was created and removed, where it was created, which components could not be read |
| `objects` | the mission's named objects: capture zones and airfields with their position and size, airfields' outlines as points, spawn areas |
| `kills`, `hits`, `modulesDestroyed` | with names and vehicles of both sides |
| `weapons` | every rocket, missile, bomb, torpedo, drop tank and jettisoned load: when, where released (position, attitude, velocity), by which unit (the nearest within 300 m and 1.5 s), how many flight samples, where last seen, when removed |
| `explosions`, `flak` | `PlayExplosionVisual` (position, direction, kind) and `PlayFlakExplosionVisual` (position) |
| `awards` | the recording player's awards (`TextStreak`: first_blood, streaks, challenge counters) |
| `detections`, `unitStates` | `UnitDetected` pairs of units; a message (0xF093) with a unit's position, attitude and velocity whose meaning is not known |
| `authorInstruments` | the recording player's cockpit values (`ReplayCockpitParams`) by instrument number, at most one per second; `known` says which were checked |
| `chat` | every chat line |
| `results` | the whole results blk as the game wrote it |
| `counts` | rows, events, lives, kinds, samples, entities by template, weapons, packets read and not read, every message id seen and those not read, samples dropped |
| `trackBreaks` | every cut of a track for a step faster than the unit can go: where, how far, how fast, and what it most likely is |
| `selfCheck` | the checks below, computed on every conversion; `stepSpeed` gives per kind the speed between consecutive rows of a track as the viewer joins them (median, 99th percentile, highest, and steps faster than possible, which must be 0) |

## What is read, and how well it is known

Checked on real files means four client replays of this machine (2026-11-07,
replay version 101404): an air arcade battle on `spain` (10 min), a naval
battle on `avn_aleutian_islands` (10 min), and two air simulator battles on
`air_afghan` and `air_denmark` (an hour each); and, for the 2025 layouts, the
three public sample replays of github.com/llama-for3ver/wt_replay_decoder.

| Part | Status, and the check |
|---|---|
| Header, map, mission, start time, session; results | all files |
| Mission settings (the blk after the header) | all four 2026 replays: mode, weather, limits, `stars` (date, time, place) |
| Packet stream (zlib in 2025, zstd in 2026) | all files, every packet framed |
| Aircraft positions and attitude (flight model, 2026 layout) | all four: 4 samples a second, no packet left unread; the heading checked against the direction of travel |
| Flight packets ahead of their time | now and then a client replay's flight packet holds every other aircraft where it will be about 0.75 s later (the client's extrapolation after a network hitch; the recording player's own aircraft is not ahead), and the next packet is back on time - read at the packet's time each aircraft leaps forward and back at up to 30,000 km/h. The lead is measured per packet (each aircraft's step along its velocity against the time elapsed, from its last on-time samples); when most moving aircraft agree, each one that leads is given the time it stands for. air_afghan has 4 such packets, air_denmark 5. Single aircraft samples that lead the same way are re-timed too. A re-timed sample that then lands within 0.2 s of the sample the game sent for that moment is left out (counted). The packets' own bytes (entries, the tail with the recording player's position) carry no mark of it |
| Teleports | a track is cut where its unit moves further than it can: first against its kind (aircraft 750 m/s, ground and ships 40 m/s, weapons 1800 m/s, above a slack of 60, 8 and 40 m), then against its own pace - 1.6 times the 95th percentile of its own steps (0.2 to 5 s long) over all its samples under one entity, no less than 250 m/s for aircraft (a piston fighter's dive) and 15 m/s on the ground, no more than the kind's limit - so a piston fighter's client correction is caught although a jet could fly it. Each cut is listed in `trackBreaks` with its likely cause and, for a pace cut, the unit's limit: a point several cuts lead to (respawn or rearm at a spawn), the recording player's own aircraft moved by the game (its own position in the packet tail moves the same way; once in air_afghan, 2.4 km in mid-air), or a distant unit corrected after the client extrapolated it. Checked on the recording player's own aircraft, which the client does not extrapolate: its own pace cuts it nowhere in the three air replays (only respawns do), its fastest kept steps are 226 m/s (I-185, limit 315) and 569-577 m/s (Eurofighter), and at its one arcade respawn the cockpit altitude runs on at the new spawn. Cuts per replay: 61 to 607 (spain's 387 pace cuts are corrections of distant piston aircraft). After the fixes no step between consecutive rows of any track is faster than its kind or its own pace allows in the four replays (`selfCheck.stepSpeed`; spain's aircraft at most 388 m/s, the jets' at most 739). Ships and boats still show up to 108 m/s between samples 0.02-0.08 s apart: the recording player's own ship comes 25 times a second, stamped at frame times, and steps of under 8 m over such short times read fast; their 99th percentile is 34-36 m/s |
| Ground and ship positions (0xF073 / 0xF074) | all four, no packet left unread. Heading, pitch and roll from the 16-bit attitude: the heading is within 1.4 to 2 degrees (median) of the direction of travel of moving ships and tanks, the pitch follows the slope (correlation 0.94). Some ships send a quaternion instead; its heading is within 2.5 degrees. Ships sit at the water level (median height 0.0 to 0.4 m on the two maps with sea) |
| Packed ground heights | positions packed in 64 bits count their height from -100 m on three maps and from 1405 m on air_afghan (its water level 1505 m less 100): measured on each replay from units seen in both forms and from their creation points, and added (`selfCheck.packedGroundHeight`; air_afghan: 20 pairs, spread 8 m) |
| Entity stream (packet type 6: creation, destruction) | all four: 857 to 11,544 entities each, every creation read. The daECS layout comes from the Dagor Engine's published source; War Thunder's own component types (unit storage, part lists, the HUD buffer, projectile state) are skipped by finding where the next component starts, and only a reading that uses the rest of the block exactly is taken. Checked: the vehicle the kill and hit records name for a uid equals the unit entity's vehicle in 960 of 960 records, and the entity's player slot equals the slot those records name in 938 of 938 (`selfCheck`) |
| Who drove which unit, AI units, ships, ground targets | from the entity stream: every unit has its vehicle and team, every player's unit its player (the slot's name); 111 to 825 lives a replay, all with a vehicle |
| Kills against the results | per player, the deaths the kill records give equal the results' deaths for 32 of 32 players in the arcade and the naval battle; the kills for 26 and 23 of 32 (the results also count kills the client was not sent). The sim replays start when the recording player joined the running session (air_afghan at 30 min, air_denmark at 5 min), so they hold only part of the session's kills |
| Kills, critical hits, severe damage | all files. The kill's field 0xB, called "victim pid" in community notes, is not the victim's slot (it matched in 2 of 66 kills); it is not used |
| Destroyed modules (0xF118) | the unit and the part's number in its damage model; the part's name needs the vehicle's damage model, which is not in the replay |
| Weapons released (entity stream) | 201 to 9,144 a replay; the release point is 13 to 22 m (median) from the nearest unit at that moment, which is taken as the launcher |
| Weapons in flight (0xF0DB) | the sim replays: 638 and 1,244 flights of missiles, rockets and bombs, each tied to its entity by the record's entity number (its eid << 10); the arcade replay sends none |
| Player slots, chat | all files (2026 chat lines end in ten bytes not read) |
| Explosions (0xD08E), flak bursts (0xD01F), awards (0xF078), detections (0xF037), weather (0xF0DF), mission objects (0xD039) | read; positions only checked by eye in the viewer |
| The recording player's instruments (0xD04A) | read by number. Checked against the author's own track on the arcade battle: instrument 40 is the altitude in metres (ratio 1.0007, correlation 0.999), 64 the compass heading (correlation 0.95). The numbers differ between cockpits (the sim jets send another set); the rest are not named |
| Wrecks | a unit's samples after its death keep coming (a ship sinks 90 m over minutes): marked `alive` 0 for 60 s or until the game removes the unit; a ground unit's later samples are dropped (counted in `counts.droppedSamples`); aircraft keep theirs, as a few AI aircraft fly on after a kill names them |
| Aircraft positions, version 101286 and server replays (2025) | not read: their flight packets have a different layout |

What stays unread, and why:

- **Unit-addressed messages** (`ff07 81 ...` / `ff0f 81 ...`, by far the most
  packets: engine RPM 0xD047, 0xD041, hit effects 0xF0E9, single shots 0xF0B1,
  gun fire 0xF0A0, unit death 0xF04B, ...): a bit-packed object address comes
  before the message id, and how it names the unit (it is not the uid) was
  not worked out; their bodies are game-specific. Counted by id in
  `counts.messageIdsNotRead`.
- **Entity messages and component replication** (packet type 6, kinds 0x20 to
  0x23): component updates over time (scores, repair, fire). Their layout is
  in the Dagor source, but most values are War Thunder's own types, and the
  message classes are numbered at run time.
- **ReflectionData** (0xF02D) beyond the player slots: per-object tables of
  numbered fields (units, mission state, scores) without names.
- **The replay camera** (0xD043), **RunTriggerAction** (0xF028),
  **RedundancyReflectionData** (0xF0AA), mission progress (0xF07A/0xF07C),
  hints (0xF0EC): not read.
- **Fuel, ammunition, throttle, gear and flaps of other units**: the flight
  model's entries hold engines, sensors and countermeasures, whose sizes are
  read and skipped; their meaning is not known. The recording player's
  instruments include them, but unnamed.
- **Projectile names**: the weapon's id (e.g. `us_aim_120d`) is only in kill
  records; a released weapon's entity holds its state, not its name.
- **Shells and bullets**: not sent as entities or flights.

Client replays show distant aircraft flying straight on between updates and
then corrected; a correction the aircraft could not have flown cuts its track
(see Teleports), smaller ones stay as the replay has them.

## Levels (`heat3d-wt-level`)

Each level becomes `<out>/<level>/<level>.glb`, `<level>.json` (what was read,
the water level, the map rectangles, triangle counts) and the level's tactical
maps as `<level>_map.png` (the air map) and `<level>_tankmap.png`. The glb is
written to `<level>.glb.part` and renamed when complete. The install is found
through Steam or the launcher's default folders; `--game <folder>` or
`HEAT3D_WT_GAME` say where it is otherwise.

| Part | What it is |
|---|---|
| `ground:<level>` | the terrain heightmap (`HM2`) as a grid, at full detail over the tank map's area (the air map's when there is no tank map), textured with the tactical map where it covers it; on levels without a heightmap, the land mesh |
| `ground:<level> heightmap surroundings` | the rest of the heightmap, coarser |
| `ground:<level> land mesh` | the land mesh's collision triangles where the heightmap does not reach (the surroundings of a tank map, out to tens of kilometres) |
| `ground:<level> outside the map` | ground the tactical map does not cover, untextured |
| `water:<level>` | one flat rectangle at the level's `water_level` over all the terrain: the game draws water as one plane, and low ground under it is sea, lake or river bed |
| `water:<level> rivers` | on levels with a water heightmap (`WHM`), the sloping water surface over the cells it covers |
| `structure:<level> buildings` | the level's placed objects (buildings, hangars, piers, cranes, walls, fences, rocks), each by its own collision shape, placed by its transform |
| `structure:<level> trees` | placed trees and bushes, each as a four-sided double cone over its collision box (a tree's collision is only its trunk) |

**Coordinates** are the game's metres with z mirrored: glb (x, y, z) = game
(x, y, -z). The game's world is left-handed (x east, y up, z north); glTF is
right-handed. `heat3d-wt-replay` keeps the game's z and tells the viewer to
mirror it, so a replay and the level of its map land on top of each other with
no placement step. The JSON gives each tactical map's rectangle in game metres
and its corners in the glb's space, for loading the PNG as a map image.

**Size.** `--max-grid` (default 1024) caps each heightmap part at that many
samples a side; a 4 km tank map at 2 m comes out at 2 to 4 million triangles,
an air map's 131 km at 32 m at about 2 million. Placed objects stay within
`--max-object-triangles` (default 4 million): over it, the object types that cost
most are drawn as their boxes, and if that is not enough the smallest objects
are left out; the JSON lists both. `--no-objects` leaves objects out,
`--no-texture` leaves the ground untextured.

### What is read, and how well

| Part | Status |
|---|---|
| Level binary (`levels/<level>.bin`, `DBLD` 3x64): block table | all 164 levels of this machine's install |
| Heightmap (`HM2`, versions 0-2; version 2 is 8-bit values in blocks, Oodle or zstd chunks) | 90 of the 164 levels have one, all version 2 with Oodle chunks; seven levels extracted and checked by eye against their tactical maps (rivers, valleys, coasts and towns line up) |
| Land mesh collision (`lmap`, its `LTdump` land ray tracer) | 116 levels have one, all Oodle-packed; read on the extracted ones. It is the game's collision surface, not the rendered mesh, so it is coarser where the land is flat |
| Water level | `water_level` from the level's BLK in `aces.vromfs.bin` (0 where it has none) |
| Water heightmap (`WHM`: a grid of flat cells and 130x130 pages of 16-bit heights) | the one level of this install that has one; its rivers come out 0 to 15 m, sloping with the ground |
| Tactical maps | from `content/base/res/locations_maps.dxp.bin`, placed by the BLK's `mapCoord0/1` and `tankMapCoord0/1`; the image's top is north (checked on four levels against the terrain) |
| Placed objects (`RIGz`: the render-instance generator's fixed instances) | every instance, as a 3x4 matrix of 16-bit values or, on some levels, 32-bit ones (the cell's byte count decides); on the replay levels every byte of every cell is accounted for. Positions checked by eye on five levels: buildings along an island's runways, a harbour's piers and cranes, a city's riverbanks against its tank map |
| Object shapes (`<object>_collision` in `content/*/res/*.grp`) | collision resources of stream version 3: box, sphere and capsule nodes as their boxes, mesh and convex nodes as their triangles. 739 of 800 sampled resources read; the rest hold no usable shape (empty boxes) and the object is counted as without a shape. The collision shape is coarser than the rendered model (a hangar is a few boxes) |
| Objects the land classes generate at run time (most forests, fields and towns of air maps, some city blocks) | **not placed**: they need the land-class assets and the game's generator. The JSON lists the land classes |
| Navigation mesh (`Lnav`), splines, wires, the rendered land mesh and its textures | not read |

Levels are compressed with Oodle, which is proprietary. The game ships a copy,
`<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (an ordinary x64 build), and
that is what is loaded; `HEAT3D_OODLE=<dll or folder>` points at another.
Nothing of Oodle is included here.

### Formats, and where they are documented

Gaijin published the Dagor Engine's source under the BSD 3-Clause licence
(github.com/GaijinEntertainment/DagorEngine). The readers here were written from
it; no game code was decompiled. Each module names the source files it follows:

- `vromfs.py`: `*.vromfs.bin` (header `VRFs`/`VRFx`, a zstd body whose first and
  last 16 bytes are XORed with a fixed key, a name table and an offset table:
  `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`, `supp/dag_zstdObfuscate.h`)
  and binary BLK (forms 1-5, with the archive's shared name map `\xff?nm` and
  zstd dictionary: `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`,
  `blk_zstd.cpp`).
- `dxp.py`: texture packs `DxP2` (`lib3d/texPackMgr2.cpp`) and DDSx headers
  (`sharedInclude/3d/ddsxTex.h`); DXT1/DXT5/BC7 are decoded by Pillow.
- `dagorlevel.py`: the level binary (`scene/loadLevel.cpp`), the heightmap
  (`heightmap/heightmapPhysHandler.cpp`, `heightMapLand/compressedHeightmap.cpp`),
  the land ray tracer (`landMesh/lmeshManager.cpp`,
  `landMesh/landRayTracerSoA4.cpp`) and the water heightmap
  (`fftWater/fftWater.cpp`).
- `rigen.py`: the placed objects (`rendInst/riGen/riGenData.h`,
  `rendInst/rendInstGen.cpp`, `rendInst/riGen/genObjUtil.h`).
- `collision.py`: resource packs (`gameRes/grpData.h`) and collision resources
  (`sharedInclude/gameRes/collResStream.h`, `gameRes/collisionGameResLoad.cpp`),
  whose triangles are stored as a quad BVH (`daBVH/bvhIO.cpp`,
  `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) reads the same archives; it is not needed and not used.

### The terms

Gaijin's Terms of Service (updated 2026-08-17), EULA (Annex 2):
3.2.2 "modify, translate, create derivative works of, reverse engineer,
disassemble, or decompile the Game(s)", 3.2.9 "mine or collect any data from
the Game(s) that is not intended to be publicly displayed"; 1.2 "are not
permitted to store, download, modify, or otherwise use any part of the Game(s)"
beyond the client. Reading your own copy's level files into a local 3D view is
the user's decision, taken knowing this. The levels written stay on your
machine: **never publish them**, and nothing here ships any game data.

## What is needed to check the rest

A server replay of a battle, downloaded by hand from warthunder.com, to see
whether server replays hold everyone's movements and use the same layouts;
a ground battle (the four replays are air and naval); a helicopter battle.
Each match document's `counts.messageIdsNotRead` and `selfCheck` say what
a new replay holds and how well it was read.

## Sources

All code here is written for it; no code was copied from another parser. What
it knows of the format comes from:

- Gaijin's Dagor Engine source (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `serialize.cpp`, `compression.h` and `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` for the entity stream (`ecs.py`). Component and type
  names are matched by their FNV-1a hashes against words of the game's own
  archives; `ecs.py` lists the names found.
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md`, and its own parser
  `web/wrpl-parse.js`, read for the bit layouts of the flight model, ground
  sync, weapons in flight, id-field messages, player slots, the cockpit
  values and the binary blk. WTACRP names maxsupermanhd/wrpl-inspector,
  wt_blk and wrpl-acmi (AGPL-3.0) as its own references; their code was not
  read here.
- SMOKE-19/WarThunderReplayDownloader's README: how server replays are fetched.
- The replays above, as files: the 2025 differences (the flight model's older
  layout, chat without a flag byte, zlib), the ground attitude, the packed
  height offset, the weapons' release points and the cockpit instruments were
  worked out on them here.

## Tests

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # also checks the real 2025 air battle
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # no step faster than possible or than the unit's own pace, entity identities
```

The tests build replays in code (`tests/synth.py`: header, packets, results,
the entity stream, weapons in flight) to the layout the readers document; no
replay is in the repository.

## Licence

MIT - see [`LICENSE`](LICENSE). Uses pyarrow (Apache-2.0), numpy (BSD-3-Clause),
zstandard (BSD-3-Clause) and Pillow (MIT-CMU). The level readers were written
from the Dagor Engine's source, Copyright (c) 2023 Gaijin Entertainment, BSD
3-Clause licence; no code of it is copied here, and the format constants used
(the vromfs XOR key, the height-range grid offsets) are cited where they appear.
