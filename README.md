# 3DHeat War Thunder replay converter

War Thunder replays (`.wrpl`) into the table the 3DHeat viewer opens: every
aircraft's, tank's, ship's and AI unit's track with its vehicle, team and
player, the missiles, rockets, bombs and torpedoes in flight, and the kills,
hits, destroyed modules and launches where they happened. A match document
beside it holds everything else the replay says: the mission settings and
sky, every unit and weapon the replay created, the mission's zones and
airfields, explosions, awards, the recording player's instruments, the scoreboard over time, the chat
and the whole results block.

```bash
pip install -e .                        # installs the `heat3d-wt-replay` command
heat3d-wt-replay "<War Thunder>/Replays" -o out
heat3d-wt-replay a.wrpl b.wrpl -o out   # files, folders, or both
heat3d-wt-replay ... --game "D:/Games/War Thunder"   # where the install is, if it is not found
heat3d-wt-replay ... --no-smoothing     # other units' tracks exactly as the replay has them
python -m heat3d_ext_warthunder ...     # the same, without installing
```

Vehicles get their English names from the game's own localisation
(`lang/units.csv` in `lang.vromfs.bin`), weapons and ammunition theirs from
`lang/units_weaponry.csv`, read from your install at conversion
time: the install is found through Steam or the launcher's default folders, or
`--game` / `HEAT3D_WT_GAME`. Nothing of the game's text is in this repository;
without an install the names are the vehicle ids.

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
| `event` | `position`; event rows lie on the track at their moment (between two samples, on the line between them); `kill` (at the killer), `death` (at the victim), `hit_critical` / `hit_severe` (at the unit hit), `module_destroyed` (at the unit), `launch` (at the unit that released a weapon), `impact` (a weapon's last sample when it was removed right after); `explosion` and `flak` (0xD08E, 0xD01F) at their position, kind `effect`, no track, with the explosion's direction where it has one; `shot` (a projectile that hit, at the shooter), `gun_shot`, `fire_start`, `fire_stop`, `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (see Messages to units) |
| `track` | what the viewer draws as one thing: one life of a unit, or one weapon's flight - `<player or vehicle> #<hex>` (the viewer shows the name without the `#` part) |
| `x`, `y`, `z` | the game's metres: x east, y up, z north (the hints mirror z, so north is not drawn south) |
| `player` | the player's name; an AI unit `<VehicleName> #<uid>` (`A-26B-10 #204`); `uid <n>` when nothing names it; for a weapon, who released it |
| `userId`, `team` | the player's Gaijin id and the team (`1`, `2`) |
| `ai`, `isPlayer` | `ai` true for every unit no player account drives (mission units, AI aircraft, ground targets, AA guns, ships without a player, placeholders), `isPlayer` the opposite: a player is a unit whose entity names a player slot with a Gaijin id. A weapon has its launcher's; empty when not known |
| `match` | the match id (the match document's `match`), on every row; the hints map it as the session, so two loaded replays never join tracks |
| `life` | `uid#n`: one unit's track, cut where the uid passes to another unit, the unit moves faster than it can (a respawn, a rearm, the game moving it, the client correcting a distant unit; see below) or is long unseen; `w<hex>` a weapon's flight (`w<hex>#n` after a cut) |
| `uid` | the unit's id in the replay |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`; weapons `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned` |
| `type` | the game's own type where the results name it (`fighter`, `assault`, `destroyer`, `gun_boat`), else as `kind` |
| `Vehicle` | the game's vehicle id (`f_15a`, `germ_flakpz_I_Gepard`), which the viewer's figures match |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | the vehicle's English name from your install's localisation (`Pz.Kpfw. III Ausf. J1`, short `Pz.III J1`) and its key (`germ_pzkpfw_III_ausf_J_0`); the game font's country marks are left out. Where the game names nothing, or no install is found, the name is the id and the key empty |
| `mission` | the unit's name in the mission (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | where the unit points (the look vector): aircraft from the flight model's attitude, ground units and ships from their own, weapons along their flight |
| `heading`, `pitch`, `roll` | the same in degrees; heading is the compass, clockwise from north, pitch nose up positive, roll right wing down positive (the flight model sends the opposite sign; see below). The hints say so under `conventions` |
| `extrapolated` | an aircraft sample that is the client's dead reckoning, not a state it received (see below) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | how far the smoother moved the sample (m), and the replay's own position and attitude (roll in the table's sign) |
| `targetX`, `targetY`, `targetZ` | a `shot`'s hit point |
| `rpm` | an aircraft's engine rpm (the mean over its engines) as last sent, within 2 s |
| `vx`, `vy`, `vz` | an aircraft's velocity as its flight entry sends it (m/s, the game's axes; speeds over 500 m/s read 500) |
| `engine`, `afterburner`, `engineCondition` | an aircraft's engines from its flight entry: `off`, `starting`, `running`, `dead` (`/`-joined when its engines differ); the afterburner 0-1; a byte sent only after the engine was hit |
| `weaponName` | kills and deaths: the weapon or ammunition in your install's English (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | the recording player's aircraft only: the throttle 0-1.1 from its cockpit (1.1 war emergency power or afterburner; else its flight entry's fifteenths), the controls -1..1 from its flight entry (elevator positive pulling, aileron positive rolling right), the rounds left per weapon (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | the recording player's aircraft only, from its cockpit: indicated airspeed and climb rate (m/s), fuel, manifold pressure (atm), gear (0-1, 1 down), oil and cylinder head temperature, where its cockpit has the gauge |
| `speed` | m/s over about two seconds of the track (worked out here; the replay sends no speed for other units) |
| `alive` | 0 for a unit's samples after its death (its wreck), for at most 60 s or until the game removes it |
| `other`, `weapon` | kills: the other side and the weapon; hits: who hit (from the record's uid, else its player slot), their vehicle; launches: the weapon; destroyed modules: who last hit the unit within 5 s before, and `part <n>` |

The match document (`format: heat3d-wt-replay-match`, version 2) has the map,
mission, battle class, session id, start time and author, and:

| Key | What |
|---|---|
| `settings` | the mission blk after the header: mode, environment, weather, score and time limits, countries, allowed unit types, wind, and `stars` (latitude, longitude, date, local time) |
| `sky` | the first `CustomWeatherParams`: sun and moon direction, wind, sky colours, cloud offsets |
| `players`, `slots` | the results' line per player (kills, ground kills, deaths, assists, score, captures, squad, clan, country, line-up, the uids they drove); the replay's player slots (name, user id, team) |
| `units` | every unit entity the replay created: eid, uid, template, vehicle, kind, type, team, player, mission name, when it was created and removed, where it was created, which components could not be read |
| `objects` | the mission's named objects: capture zones and airfields with their position and size, airfields' outlines as points, spawn areas |
| `kills`, `hits`, `modulesDestroyed` | with names and vehicles of both sides; kills with the weapon's English name |
| `weapons` | every rocket, missile, bomb, torpedo, drop tank and jettisoned load: when, where released (position, attitude, velocity), by which unit (the nearest within 300 m and 1.5 s), how many flight samples, where last seen, when removed |
| `explosions`, `flak` | `PlayExplosionVisual` (position, direction, kind) and `PlayFlakExplosionVisual` (position) |
| `awards` | the recording player's awards (`TextStreak`: first_blood, streaks, challenge counters) |
| `detections`, `unitStates` | `UnitDetected` pairs of units; a message (0xF093) with a unit's position, attitude and velocity whose meaning is not known |
| `authorInstruments` | the recording player's cockpit values (`ReplayCockpitParams`) by instrument number, at most one per second; `known` names each number this replay sent (name, unit, how it was checked), `notNamed` the rest |
| `scoreboard` | every player's statistics each time they changed (kills, deaths, assists, score, ai kills, naval kills, zones, damage, missile evades, squad), and each team's score and likely tickets over time (see Reflection data) |
| `entityMessages` | the entity messages (0x20) by class number: count, target templates, sizes |
| `chat` | every chat line |
| `triggers`, `hints`, `missionProgress` | the mission script's actions (RunTriggerAction), its hints, its progress messages |
| `camera` | the recording player's replay camera every 0.25 s |
| `projectileHitReplays` | the recording player's own hits and being hit, with weapon and ammunition and their English names |
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
| Dead-reckoning snaps | a step out of a dead-reckoned run (see below) is measured from the last received state when the snap is at most 300 m: the client's corrections no longer cut tracks (arcade: about 770 lives before, 485 now; one player's 24 tracks are 12, its respawns) |
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
| The recording player's instruments (0xD04A) | named (see [Cockpit instruments](#cockpit-instruments)): the numbers are one list for all cockpits, each cockpit sending the gauges it has; the candidates are the gauge names in the aircraft's flight model (`cockpit/devices` in `gamedata/flightmodels/<aircraft>.blk`) and the game's telemetry page (`webUi.vromfs.bin`), and each was matched by checking it against the replay itself. 32 of the I-185's 41 numbers and all 36 of the Eurofighter's are named; the other 9 are listed under `notNamed` |
| Flight entries' other fields | the velocity word, the rounds per weapon, the controls and throttle, the engines (see [Flight entries](#flight-entries)). The 7 bytes after the velocity start at the packet's next byte, so the converter now keeps where each entry starts (the sidecar's `phase`). Before this, every entry that did not start on a byte boundary was read 1 to 7 bits off there |
| Event rows' attitude | every event row (gunfire, hits, kills, repairs) carries its unit's heading, pitch, roll and look vector at that moment. Before, they had none, and a ship's latest row (its guns fire all the time) read as heading 0. Ships' heading against their course over ground: median 1.3 degrees (naval battle, moving at 3 m/s or more) |
| Player statistics and team scores (0xF02D, 0xF0AA) | read (see [Reflection data](#reflection-data)): at the end of the battle every statistic equals the results' for every player (32, 32, 32 and 48 players); all 8 teams' scores equal the sums of their players' |
| Weapon names | from the install's `lang/units_weaponry.csv` (weapons, ammunition) and `units_modifications.csv` (ammunition belts): all 25, 16 and 29 kill weapons of the arcade and the two simulator battles are named, 28 of 32 of the naval battle (the other 4 are ships' default belts, `*_universal`, which the game names nowhere) |
| Vehicle names | from the install's `lang/units.csv` (`<id>_0` full, `<id>_1` short; ships also `ships/<id>_0`): 62 of 62, 50 of 50, 43 of 45 and 31 of 33 vehicles of the four replays (the rest: two airfield radars the game does not name) |
| Players and AI | from the entity stream's player slot and the slot's Gaijin id: on the four replays no row of a player in the results is AI, every row not AI is a results player's, and every ground unit of the air battles is AI (`selfCheck.identity`) |
| Wrecks | a unit's samples after its death keep coming (a ship sinks 90 m over minutes): marked `alive` 0 for 60 s or until the game removes the unit; a ground unit's later samples are dropped (counted in `counts.droppedSamples`); aircraft keep theirs, as a few AI aircraft fly on after a kill names them |
| Aircraft positions, version 101286 and server replays (2025) | not read: their flight packets have a different layout |

### Messages to units

Every type-4 packet is an mpi message of the Dagor Engine's daNet
(`prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp`): the
recipient object's id (u16), then - when its low 11 bits are all set - the
object's ext UID (LEB128), the message id (u16) and the payload. The game
messages above go to objects `0x58xx`; a message to a unit carries the id
0x07FF (0x0FFF, 0x87FF, 0x8FFF) and as its ext UID the unit's ECS entity id,
`index << 10 | generation`, the entity the entity stream created. Checked: all
114,008 (arcade), 91,346 (naval), 185,561 and 295,241 (sim) such messages name
an entity alive at that moment. Read from them:

| Message | What, and the check |
|---|---|
| 0xF0E9 UnitHitEffects | one projectile's hit on the unit: the shooter's uid and the hit point in the unit's frame (int16 cm; x forward, y up, z left). Becomes a `shot` row (below). Of the hit and kill records with these messages on the victim in the 3 s before, the record's attacker is among their shooters in 147 of 148, 97 of 99, 222 of 223 and 355 of 359; shooter-to-hit range median 309 m, 99th percentile 952 m (arcade); the hit points lie on the side facing the shooter |
| 0xF133 UnitOnExplosion | the same shooter uid (used in the check) |
| 0xF04B OnUnitDead | `dead` rows: every kill record's victim has one within 2 s (97 of 97, 63 of 63, 112 of 112, 219 of 219); the others are deaths without a kill record (crashes, ground targets) |
| 0xD047 FmwRpm | the engines' rpm: the `rpm` column. The recording player's against its own cockpit instrument 93: correlation 0.973 to 0.996, median 4.6 to 8 rpm apart |
| 0xF0B1 UnitSingleShot, 0xF0A0 GmDoSingleShotUnreliable | `gun_shot` rows: single shots of heavy AA and artillery (90 mm, 88 mm, 152 mm), at the gun |
| 0xF01B, 0xF01C GmDoStopFire | `fire_start`, `fire_stop` rows: bursts of the 40 mm AA guns (pairs, 171/169) |
| 0xF050 UnitBailoutResponse, 0xF033 UnitRepair, 0xF054 UnitRearm, 0xF0BD UnitBulletRearm, 0xD046 UnitReloadGun | `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` rows |
| 0xD0FE ProjectileHitReplay | the recording player's own hits and being hit (two a battle): names, vehicles, the weapon's blk and the ammunition (`gameData/Weapons/cannonShVAKS.blk`, `frag_i_t`), named from the install (`20 mm ShVAK cannon`, `Fragmentation incendiary tracer shell`); in `projectileHitReplays`. Other players' weapons and ammunition are in no message of a client replay except the kill records |
| 0xF13E | not part damage, as was thought, but a hit's visual effect: a flag, the effect's number, its size and the point in the unit's frame. In the arcade battle 1,674 of 1,724 come with a UnitHitEffects on the same unit within 0.02 s, and all within 3 s; the point is 0.34 m (median) from that hit's. The number comes from a few runs (4303-4306, 4324-4327, 4504-4549, 4867-4873) that are the same on every vehicle and shared with 0xF031 |
| 0xF031 | an effect played on the unit: the effect's number (as in 0xF13E) and a random seed; 282 of 323 come within 0.05 s of a hit on the unit |
| 0xD041 | one per defensive gun of an aircraft, twice a second (median 0.50 s apart) for the whole flight: the gun's index and three floats (zero in all four replays). Checked: each vehicle's indices run 0 to n-1, where n is the number of gunner weapons in its flight model, for 16 of 17 bombers (the A-26B-10 has 4 indices and 12 such weapons spread over its presets) |
| 0xD048 | on aircraft (mostly the recording player's and its target): a count byte and that many 24-byte records (u32 rising, float, double, u64, the last the same in all records of a message). The length fits all 2,660 in the arcade battle; meaning not known |
| 0xF117 | to a unit just hit (all 40 within 3 s): six bytes, a small number, a float that grows; meaning not known |
| the rest (0xF09A HP, 0xD020 gun angles, 0xF015, 0xF04F, ...) | in the messages sidecar with their unit and fields; their meaning is not checked |

Names are the community's (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

### The sidecars

Next to each table, so that nothing of the replay is lost to it:

- `<match>.messages.parquet`: every message to a unit (time, message id and
  name, uid, eid, template, vehicle, its id fields as hex, `decoded` (what is
  read of it, as JSON), the payload), every replicated component value
  (packet 6, `name` the component, `fields` its value), every entity message
  (with its entity and class number), every replicated object of 0xF02D and
  0xF0AA (`ReflectionData <kind>/<index>`, its fields as hex) and every
  packet no reader here takes, whole.
- `<match>.flight.parquet`: every flight-model entry of every aircraft whole
  (its bits, and `phase`: the bit of its first byte it started at), with its
  velocity, the 14 nibbles after it (`control1-3`, `throttle`), its engines
  with their state, afterburner and condition, and its rounds per weapon
  (`ammo`; `numbers` is the whole list). Other aircraft's values are as last
  refreshed.

### Also read

- **Entity-stream replication** (0x22, 0x23; `Connection::readReplicationPacket`,
  `Object::deserializeComps`): the sent time, a sequence number (running on by
  one), per entity its eid and a block of component values. Read: ship repair
  and unwatering timers, consumables' counts (`mod__count` of toolkits,
  extinguishers, smoke), owner and team changes, tank engine overheat; War
  Thunder's own `BufferedHudData` is kept as bytes. Counted in
  `counts.replicatedComponents`; the values in the messages sidecar.
- **RunTriggerAction** (0xF028, the mission script's actions, e.g.
  `unitSetIndication`) and **MissionPlayHint** (0xF0EC): the action and the
  words of its parameters (`triggers`, `hints`); the parameter blk's layout is
  not read, its bytes are kept.
- **Mission progress** (0xF07A, 0xF07C): fields as hex (`missionProgress`).
- **The replay camera** (0xD043, about 20 a second): a quaternion and float
  triples (`camera`, every 0.25 s; all in the sidecar). Which triple is the
  camera's position is not checked.

What stays unread, and why:

- **Entity messages' names and bodies** (0x20, 0x21): the class number is
  read. It is 6 bits in all four replays, and its parity bit is right in
  every message (2,974 in the arcade battle, 32,516 in the naval one). But a
  class number is the class's place among all the game's network message
  classes sorted by their hash (DagorEngine `net/message.cpp`). That list is
  compiled into the game: it is not sent, and it is not in the game's data.
  The install's scripts declare 73 server-to-client network events, more
  than 6 bits can number, so which of them a build registers, and in what
  order, cannot be worked out. Kept whole with their entity and class number.
- **Other replicated objects** (0xF02D and 0xF0AA objects of kinds other than
  player slots and teams, e.g. 0, 1, 8, 12, 16, 25): their fields are read
  and kept (sidecar rows `ReflectionData <kind>/<index>`) but not named: the
  results hold nothing to check them against. Of the player slots, fields
  3-37 and 40-50 apart from the statistics (clan tag, title, masks) are kept,
  not named; of the teams, field 3 (likely the tickets) and field 2 are not
  checked.
- **Other aircraft's controls, throttle and rounds**: they are in their
  flight entries, but refreshed only now and then (a median of 4 and 1
  changes per aircraft in an hour's battle; their rounds fall within 3 s of
  only 41 of the 134 hits they score). They are kept in the flight sidecar
  but not put in the table. Their gear, flaps and fuel are not in the
  entries at all.
- **0xD048, 0xF117, 0xF09A, 0xD020 and the other unit messages listed above**:
  layouts read where stated, meaning not known.
- **Released weapons' names**: a bomb's or rocket's entity holds its position,
  attitude and velocity, not its name; kill records name the weapon of a kill.
- **Shots that missed**: a client replay holds the hits only (see Gunfire).

### Cockpit instruments

0xD04A sends the recording player's gauges as (number, float) pairs: four a
second in arcade (every gauge), only the values that changed in simulator.
The numbers form one list across all cockpits (rpm is 93 in the I-185 and in
the Eurofighter), and a cockpit sends the gauges its model has. The game's
own gauge names are in each aircraft's flight model (`cockpit/devices`:
`speed`, `vario`, `altitude_hour`, `compass`, `pedals1`, `ammo_counter1`, ...)
and on its telemetry page, but the number for each name is set in the game's
code. So each number was named by what it does, and checked against the
replay where something independent says the same (the converter reads
nothing of this from the install; `convert.INSTRUMENTS` holds the result):

| Number | Name | Check (I-185 in the arcade battle unless said) |
|---|---|---|
| 0 | indicated airspeed, m/s | the track's speed corrected by the ISA air density at its height: correlation 0.990, median 1.6 m/s apart |
| 39 | climb rate, m/s | the track's: correlation 0.9995, median 0.44 m/s apart |
| 40, 41 | altitude, m; altitude modulo 1000 | the track's height, median 3.8 m apart; 41 is 40 modulo 1000 exactly |
| 52, 53 | artificial horizon roll and pitch | minus the table's roll and pitch, median 0.63 and 0.16 degrees apart |
| 64 | compass | the table's heading, median 0.09 degrees apart |
| 15-20 | rudder pedals (one per pedal gauge, all alike) | the side force on the aircraft: Spearman 0.84; the flight entry's rudder 0.57 (Eurofighter 0.40) |
| 23, 31 | stick, elevator and ailerons (the sign is the cockpit model's) | the angle of attack: Spearman 0.93 (Eurofighter -0.31); the roll rate 0.65 and 0.66 |
| 69, 71, 73 | clock: hours (12-hour dial), minutes, seconds | the recording computer's local time: the header's start (UTC+1) plus the replay time, to the minute |
| 75 | manifold pressure, atm | 1.55 at war emergency power, 1.29 at 100 % (median) |
| 81-86, 87-92, 93-98 | rpm per engine, rpm modulo 1000, rpm gauge | 81 = 93 exactly; 87 is 93 modulo 1000 exactly; 93 against FmwRpm: correlation 0.973 to 0.996 |
| 195 | fuel | falls in 2,077 of 2,080 steps, full again at the respawn |
| 228-230 | landing gear legs, 1 down | Eurofighter: down only at the airfields' height and under 125 m/s (median 38), over 9 spawns and 2 landings |
| 240, 241 | throttle per engine, 1.1 war emergency power or afterburner | the flight entry's throttle: correlation 0.74 (Eurofighter); manifold pressure higher at 1.1 |
| 330-332, 346-348 | ammunition counters (the second set equal to the first) | start at the weapon preset's rounds in the install's flight model (140, 250, 170) and fall with the flight entry's rounds |
| 135, 159 | oil and cylinder head temperature | likely: they rise over a sortie; nothing to check them against |
| 58, 61 | slip ball, turn needle | likely: with the side force -0.25 and the turn rate 0.44 only |
| 223 | airbrake | likely: Eurofighter, only on approach (127-141 m/s), with flight-entry nibble 5 (0.82) |
| 490-497, 500-505 | wheel brakes | likely: Eurofighter, set only standing on the airfield (0-14 m/s), with flight-entry nibble 4 (0.93) |

Not named (I-185): 129 (1 while the engine runs, falls with it), 165
(0.833, constant), 198 (10 or 11, switching with 240), 231 (0.05, then
0.5), 239 (-0.2 to 0.2, with the angle of attack: Spearman 0.78; perhaps the
trim), 273 (1, sent 59 times), 276 (0.05 to 1 at the start), 300 (0 to 1
in 1 s, at the switches of war emergency power), 379 (0 to 1 in 2.5 s,
mostly 1 at 60-90 m/s; perhaps the flaps). The Eurofighter's 225 and 226
(0.05 to 1) are not named either.

The table's `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`,
`oilTemperature`, `headTemperature` and `throttle` come from these, on the
recording player's own rows, taking the last message at most 0.2 s after
the sample (each tick's message comes about 0.1 s before its flight packet).

### Flight entries

Each aircraft's flight entry (packet type 2) carries, besides its position
and attitude:

- **Velocity**: the u32 after the attitude. Bits 31, 30 and 29 are the signs
  of x, y and z; then the speed in 11 bits of 500/2047 m/s (it stops at
  500 m/s), then |x| and |y| as fractions of the speed in 9 bits each (/511),
  and z is what makes the vector a unit vector. Checked against the step
  between the received samples before and after: the direction is within
  0.10 to 0.17 degrees (median) on the recording player's aircraft and 0.53
  to 1.6 on everyone else's (simulator, arcade, naval); speed ratio 0.998 to
  1.000 in all four battles; track speeds above about 500 m/s all read 500.
  `selfCheck.flightEntries`.
- **Rounds per weapon**: the zigzag list before the position, one item per
  weapon, the rounds left first. The recording player's equals its cockpit's
  counters one tick later in 2,050 of 2,135 samples (arcade).
- **Controls and throttle**: the 7 bytes after the velocity as 14 nibbles.
  For the recording player, sent every tick: 1 the elevator, 2 the ailerons,
  3 the rudder (8 at rest; against the cockpit's stick and pedals 0.70, 0.38,
  0.57 on the I-185 and -0.61, 0.69, 0.40 on the Eurofighter; elevator with
  the angle of attack 0.46 and 0.28, ailerons with the roll rate 0.56 and
  0.42), 11 the throttle in fifteenths (15 also for war emergency power and
  afterburner), 4 the wheel brakes, 5 the airbrake, 8 likely the brake chute
  (15 only in the landing roll, 22-122 m/s). Other aircraft's nibbles change
  only a few times a battle and are not their controls at the time.
- **Engines**: per engine a state byte (0 off; 1-6 starting, as the rpm runs
  up from 0 to about 1,600 after a spawn on the airfield; 7 running; 8 dead),
  a u16 present only with afterburner (32767 full; the cockpit's throttle is
  1.10 at the median of the 3,841 samples with it, 0.95 without), and a byte present only after the engine was hit (on the
  Eurofighter, falling from 121 to 71 as its full-throttle rpm fell to 8,000).
  An engine "dead": of the aircraft lives with one, 29 of 110 are killed
  (median 0.1 s after) and 81 end within 2 minutes in the arcade battle;
  74 and 102 of 182 in air_afghan (6 fly on longer), 118 and 49 of 174 in
  air_denmark (7 fly on). Other aircraft's engine fields change with the
  engine (a median of 5 state changes per aircraft in an hour) and are used.

### Reflection data

0xF02D ReflectionData replicates the game's numbered objects: a compression
flag, a count, and per object its id (the top 5 bits the kind, the low 11 an
index) and a field table. 0xF0AA RedundancyReflectionData is the same list
without the flag (all 3,181 to 14,708 per replay read to their end). Kind 14
is the player slots (field 2 user id and name, 9 the team, as before), kind
15 the teams (index 1 and 2):

- A slot's field 39 holds its statistics as little-endian numbers at fixed
  places: kills (offset 0), team kills (2), deaths (4), naval kills (10), AI
  kills (12), AI ground kills (14), assists (20), capture zones (22), zone
  damage (24, u32), damage award (40, u32), missile evades (50). Field 38
  starts with the score (u32), field 42 is the squad. At the end of the
  battle every one equals the results' for every player: 32 of 32 in the
  arcade, naval and air_afghan battles, 48 of 48 in air_denmark
  (`selfCheck.scoreboardVsResults`). Each was
  found where some player had a nonzero value: assists in 10, 22 and 1
  players; AI kills in 2 and 6; AI ground kills in 6 and 3; naval kills in
  21; capture zones in 5 and 4; zone damage in 9 and 6; damage award in 30;
  team kills in 1; missile evades in 27. Ground kills had no such player in
  any of the four battles (their place is not known).
- A team's field 7 (a float) is its score: at the end it equals the sum of
  its players' results scores for all 8 teams of the four battles (13,520
  and 20,941 in the arcade battle; 14,834 and 15,837 in the naval one;
  47,911 and 43,446, 46,558 and 41,260 in the simulator battles). Field 3 (u16) is likely its tickets: lower
  for the team that lost more, and 0 for the naval battle's losing side.
- Each message sends only the fields that changed, so `scoreboard` in the
  match document lists every player's statistics and every team's score at
  each change.

### Dead reckoning, and the smoother

A client replay records every aircraft at the client's 0.25 s ticks as the
client drew it. Between the updates it receives for a distant aircraft, the
client moves it on along its last velocity and turns it on at its last rates,
and at the next update snaps it there. Read as it is, a track runs straight,
then jumps; a rolling aircraft keeps rolling until the next update (an La-7
spinning through 180 degrees at 128 deg/s while its update says it rolled half
as far). Nothing in the flight entry marks which samples were received: every
field and bit of the entries was tested against it. A dead-reckoned sample is
found by what it is: it continues the straight line of the two samples before
it, at their pace, to within 3 cm (float32 positions are exact to a few mm).

| Replay | other aircraft's samples dead-reckoned | steps over 15 g, replay -> table | 99th percentile, replay -> table |
|---|---|---|---|
| spain (air arcade) | 55 % | 12.4 % -> 1.7 % | 67 g -> 18 g |
| avn_aleutian_islands (naval) | 14 % | 8.3 % -> 1.6 % | 47 g -> 18 g |
| air_afghan (sim) | 2.3 % | 3.6 % -> 0.6 % | 20 g -> 12 g |
| air_denmark (sim) | 0.7 % | 3.0 % -> 0.4 % | 18 g -> 11 g |

(acceleration between consecutive 0.25 s samples; `selfCheck.deadReckoning`).
The recording player's own aircraft, which the client does not extrapolate,
has no step over 15 g in the arcade battle (99th percentile 10 g) and 0.2 to 4 %
of its samples on a straight line by chance (steady flight).

By default (`--no-smoothing` turns it off) the tracks of all units but the
recording player's own are put where the received states say they were:
a dead-reckoned sample goes on a cubic through the received samples before
and after it, each with its own velocity (that of the dead reckoning that
follows it); over more than 3 s the straight line is only bent over to the
next received sample by the snap the client made there, so no sample moves
further than that snap. Its attitude is turned evenly from one received
attitude to the next instead of the client's spin. Received samples come with
a few metres of scatter (90th percentile 2.8 m along the track, 4.5 m across,
in the arcade battle) and are moved to a quadratic in time over two samples
each side, by at most 2 m or 0.04 s of their speed; a quadratic keeps a
steady turn as it is. The replay's own values stay in the `Raw` columns.

### Attitude, checked

On the recording player's own aircraft: the heading lies within 0.2 to 0.8
degrees (median) of the direction of travel, the pitch within 0.3 to 2.3 degrees of
the climb angle, and in clear turns the packed roll is positive in left turns
(235 of 237 samples in the arcade battle, 262 of 263 and 190 of 194 in the
sim battles): the flight model's roll is left wing down positive, and the
table turns it to right wing down positive (`selfCheck.aircraftAttitude`).
The 10-bit angles step 0.18 degrees. Ground units' roll sense is not checked.

### Gunfire

Every projectile that hit a unit is in the replay (0xF0E9, above): a `shot`
row at the shooter's position at the moment of the hit, `targetX/Y/Z` the hit
point (the unit hit, moved by the hit point in its frame, turned by its
attitude), the direction towards it, `other` the unit hit. Shells and bullets
that missed are not sent: they are not entities, the weapons-in-flight
messages hold only rockets, missiles, bombs and torpedoes. The recording
player's rounds left (its `ammo` column) fall as it fires, so its bursts can
be told, but not where those rounds went. Heavy AA and artillery
send each single shot (`gun_shot`, no direction), 40 mm AA guns their bursts
(`fire_start`, `fire_stop`).

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
  `object.cpp`, `serialize.cpp`, `compression.h` and `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` for the entity stream (`ecs.py`), and `net/message.cpp`
  (`MessageClass::initImpl`) for how entity messages number their classes. Component and type
  names are matched by their FNV-1a hashes against words of the game's own
  archives; `ecs.py` lists the names found.
- The same source's `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp`
  and `daNet/bitStream.h`: how a message names the object it is for
  (`wrpl.read_mpi`).
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
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # steps, identities, AI flags, roll sign, the smoother, names
```

The unit tests never read an install (`HEAT3D_WT_NO_NAMES` is set); the test
with your own replays reads the names from your install.

The tests build replays in code (`tests/synth.py`: header, packets, results,
the entity stream, weapons in flight) to the layout the readers document; no
replay is in the repository.

## Licence

MIT - see [`LICENSE`](LICENSE). Uses pyarrow (Apache-2.0), numpy (BSD-3-Clause),
zstandard (BSD-3-Clause) and Pillow (MIT-CMU). The level readers were written
from the Dagor Engine's source, Copyright (c) 2023 Gaijin Entertainment, BSD
3-Clause licence; no code of it is copied here, and the format constants used
(the vromfs XOR key, the height-range grid offsets) are cited where they appear.
