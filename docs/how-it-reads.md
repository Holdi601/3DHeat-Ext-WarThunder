---
title: How it reads a replay
nav_order: 8
---

# How it reads a replay

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
| Ground and ship positions (0xF073 / 0xF074) | all 104, no packet left unread. Heading, pitch and roll from the 16-bit attitude: the heading is within 1.4 to 2 degrees (median) of the direction of travel of moving ships and tanks. The pitch counts 180/65536 degrees a step, not 360/65536: read at 360/65536 it was twice the climb of the track (slope 1.99 over 20,612 steps of tanks driving forward in five ground battles, correlation 0.961); now 0.994. The roll's sign is the table's turned (it was read with the left side down positive): with both fixed, the gun's world direction from hull and turret lies within 3 degrees of the line to the unit hit for 95-99 % of tanks' shots, and the replay camera's offset turned into the vehicle's frame equals the offset the game sends in that frame (median 0.00 m; see The camera). Some ships send a quaternion instead; its heading is within 2.5 degrees. Ships sit at the water level (median height 0.0 to 0.4 m on the two maps with sea) |
| Turrets (in the ground state) | tanks' turret yaw and gun pitch per turret (see [Turrets](ground.md#turrets)); checked against the shots and the recording player's aim |
| Packed ground heights | positions packed in 64 bits count their height from -100 m on three maps and from 1405 m on air_afghan (its water level 1505 m less 100): measured on each replay from units seen in both forms and from their creation points, and added (`selfCheck.packedGroundHeight`; air_afghan: 20 pairs, spread 8 m) |
| Entity stream (packet type 6: creation, destruction) | all four: 857 to 11,544 entities each, every creation read. The daECS layout comes from the Dagor Engine's published source; War Thunder's own component types (unit storage, part lists, the HUD buffer, projectile state) are skipped by finding where the next component starts, and only a reading that uses the rest of the block exactly is taken. Checked: the vehicle the kill and hit records name for a uid equals the unit entity's vehicle in 960 of 960 records, and the entity's player slot equals the slot those records name in 938 of 938 (`selfCheck`) |
| Who drove which unit, AI units, ships, ground targets | from the entity stream: every unit has its vehicle and team, every player's unit its player (the slot's name); 111 to 825 lives a replay, all with a vehicle |
| Kills against the results | per player, the deaths the kill records give equal the results' deaths for 32 of 32 players in the arcade and the naval battle; the kills for 26 and 23 of 32 (the results also count kills the client was not sent). The sim replays start when the recording player joined the running session (air_afghan at 30 min, air_denmark at 5 min), so they hold only part of the session's kills |
| Kills, critical hits, severe damage | all files. The kill's field 0xB, called "victim pid" in community notes, is not the victim's slot (it matched in 2 of 66 kills); it is not used |
| Destroyed modules (0xF118) | the unit and the part's number in its damage model; the part's name needs the vehicle's damage model, which is not in the replay |
| Weapons released (entity stream) | 201 to 9,144 a replay; the release point is 13 to 22 m (median) from the nearest unit at that moment, which is taken as the launcher |
| Weapons in flight (0xF0DB) | the sim replays: 638 and 1,244 flights of missiles, rockets and bombs, each tied to its entity by the record's entity number (its eid << 10); the arcade replay sends none |
| Bombs without flight records | the arcade replay sends no weapons-in-flight messages, and the simulator ones none for some bombs (16 of 75 in one), so such a bomb was its `launch` event alone: no track, no fall, no impact. Its fall is now worked out from the release (position and velocity, from its entity) to its removal (the impact): gravity and drag (`-k |v| v`, k 4e-5 per metre, a terminal speed near 500 m/s), a sample every 0.1 s, `extrapolated` true, the last one `impact`. Not for a fall over 90 s or ending more than 150 m below the sea (a glide bomb, whose minutes the release does not tell). Checked over the sea, where the impact height is known: the naval replay's 13 such bombs dropped from the air end 6 m below to 14 m above it where the replay removes them (in vacuum up to 38 m below); 4 depth charges rolled off boats fall on through the water to 68-98 m below. In the match document such a weapon keeps `flightSamples` 0 and has `ballisticImpact`; `counts.bombsBallistic` counts them (341 of 351 bombs in the arcade air replay, 13 of 14 in a realistic ground battle) |
| Player slots, chat | all files (2026 chat lines end in ten bytes not read) |
| Explosions (0xD08E), flak bursts (0xD01F), awards (0xF078), detections (0xF037), weather (0xF0DF), mission objects (0xD039) | read; positions only checked by eye in the viewer |
| The recording player's instruments (0xD04A) | named (see [Cockpit instruments](aircraft.md#cockpit-instruments)): the numbers are one list for all cockpits, each cockpit sending the gauges it has; the candidates are the gauge names in the aircraft's flight model (`cockpit/devices` in `gamedata/flightmodels/<aircraft>.blk`) and the game's telemetry page (`webUi.vromfs.bin`), and each was matched by checking it against the replay itself. 32 of the I-185's 41 numbers and all 36 of the Eurofighter's are named; the other 9 are listed under `notNamed` |
| Flight entries' other fields | the velocity word, the rounds per weapon, the controls and throttle, the engines (see [Flight entries](aircraft.md#flight-entries)). The 7 bytes after the velocity start at the packet's next byte, so the converter now keeps where each entry starts (the sidecar's `phase`). Before this, every entry that did not start on a byte boundary was read 1 to 7 bits off there |
| Event rows' attitude | every event row (gunfire, hits, kills, repairs) carries its unit's heading, pitch, roll and look vector at that moment. Before, they had none, and a ship's latest row (its guns fire all the time) read as heading 0. Ships' heading against their course over ground: median 1.3 degrees (naval battle, moving at 3 m/s or more) |
| Player statistics and team scores (0xF02D, 0xF0AA) | read (see [Reflection data](aircraft.md#reflection-data)): at the end of the battle every statistic equals the results' for every player (32, 32, 32 and 48 players); all 8 teams' scores equal the sums of their players' |
| Weapon names | from the install's `lang/units_weaponry.csv` (weapons, ammunition) and `units_modifications.csv` (ammunition belts): all 25, 16 and 29 kill weapons of the arcade and the two simulator battles are named, 28 of 32 of the naval battle (the other 4 are ships' default belts, `*_universal`, which the game names nowhere) |
| Vehicle names | from the install's `lang/units.csv` (`<id>_0` full, `<id>_1` short; ships also `ships/<id>_0`): 62 of 62, 50 of 50, 43 of 45 and 31 of 33 vehicles of the four replays (the rest: two airfield radars the game does not name) |
| Players and AI | from the entity stream's player slot and the slot's Gaijin id: on the four replays no row of a player in the results is AI, every row not AI is a results player's, and every ground unit of the air battles is AI (`selfCheck.identity`) |
| Wrecks | a unit's samples after its death keep coming (a ship sinks 90 m over minutes, a burnt-out tank is sent until the game removes it): a ground unit's or ship's wreck is `alive` 0 until its entity is removed or its samples end, and stays one track across gaps (a distant wreck is refreshed every 5.5 s or not for minutes); its death is the entity's first kill record or OnUnitDead. Before, a wreck seen again after a minute became a new track that read as alive: the vehicle a player left for an aircraft seemed to stand there alive. Aircraft keep `alive` 0 for at most 60 s, as a few AI aircraft fly on after a kill names them (`selfCheck.wrecks`: how many, how long they stay) |
| Vehicle switches | a player's unit still alive when the same player's next unit (another entity, created no earlier, first seen later) appears is ended there: a vehicle left standing, which the game may go on sending where it stands to the end (3 in the 100 ground battles, each never moving and without the spawn's UnitRepair). A killstreak bomber (`*_killstreak`, an AI aircraft the player calls in, in arcade and realistic battles) flies beside the player's tank and ends nothing. `selfCheck.vehicleSwitch.twoLiveVehicles` (one player's two different units alive at the same moment for over a second) is 0 in all 104 replays; before the wrecks were read as above, 6 of the ground battles sampled had 25 such pairs |
| Tank wrecks | `selfCheck.wrecks`: 5,614 wrecks in the 104 replays, staying a median of 268 s (per battle); a tank's wreck moves at most 58 m (99th percentile per battle, median 7 m) from where it was first seen dead |
| Battle mode | difficulty from the header, game and mission mode from the mission (see [Battle mode](ground.md#battle-mode)) |
| Aircraft in a 2026 server replay (version 101404) | the flight packets are in the 2026 layout and parse to their end (the bytes after the list are zero padding): the test battle (a ground battle) has the two aircraft that flew, a helicopter and a jet, 4 samples a second; on every aircraft (a server replay has no recording player) the heading is 2.2 deg (median) from the direction of travel and the roll's sign is the turn's in 105 of 105 clear turns (`selfCheck.aircraftAttitude`); the sent velocity is within 0.13 deg (median) and 0.1 % of the step between samples (`selfCheck.flightEntries`). The flight list also names every player's placeholder aircraft (`dummy_plane`, one per player, never flown) and the tanks' recon drones, all with "no data" in every packet: the drones' positions are not in the flight packets, the ground packets or the unit states, and stay unread |
| Players of a server replay | the results list every player with an empty user id: each is found by name in the slots (32 of 32 in the test battle), its vehicles are its line-up from the results' matchingInfo; every statistic of the scoreboard equals the results' for 32 of 32 (`selfCheck.players`, `selfCheck.scoreboardVsResults`) |
| Aircraft positions, version 101286 and server replays (2025) | not read: their flight packets have a different layout |

## Messages to units

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
| 0xF0E9 UnitHitEffects | one projectile's hit on the unit: the shooter's uid and the hit point in the unit's frame (three int16; x forward, y up, z left): cm on aircraft and ships, on ground units a fraction of 20 m (20/32768 m a step: fitted on the ten ground test battles, the hits' top lies 1,520-1,640 steps above the origin for turret roofs 2.2-2.7 m high and their sides 1,620-1,930 steps out for half-widths of 1.75-1.88 m, five tank families; 1,638 steps a metre. Read as mm, as before, the points lay 1.6 times too far out). `hitLocalX/Y/Z` in m. Becomes a `shot` row (below). Of the hit and kill records with these messages on the victim in the 3 s before, the record's attacker is among their shooters in 147 of 148, 97 of 99, 222 of 223 and 355 of 359; shooter-to-hit range median 309 m, 99th percentile 952 m (arcade); the hit points lie on the side facing the shooter |
| 0xF133 UnitOnExplosion | the same shooter uid (used in the check) |
| 0xF04B OnUnitDead | `dead` rows: every kill record's victim has one within 2 s (97 of 97, 63 of 63, 112 of 112, 219 of 219); the others are deaths without a kill record (crashes, ground targets) |
| 0xD047 FmwRpm | the engines' rpm: the `rpm` column. The recording player's against its own cockpit instrument 93: correlation 0.973 to 0.996, median 4.6 to 8 rpm apart |
| 0xF0B1 UnitSingleShot, 0xF0A0 GmDoSingleShotUnreliable | `gun_shot` rows: single shots of heavy AA and artillery (90 mm, 88 mm, 152 mm), at the gun |
| 0xF01B, 0xF01C GmDoStopFire | `fire_start`, `fire_stop` rows: bursts of the 40 mm AA guns (pairs, 171/169); a gun firing, not a fire on the vehicle (that is `fire_on`, below) |
| 0xF050 UnitBailoutResponse, 0xF033 UnitRepair, 0xF054 UnitRearm, 0xF0BD UnitBulletRearm, 0xD046 UnitReloadGun | `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` rows |
| 0xD0FE ProjectileHitReplay | the recording player's own hits and being hit (two a battle): names, vehicles, the weapon's blk and the ammunition (`gameData/Weapons/cannonShVAKS.blk`, `frag_i_t`), named from the install (`20 mm ShVAK cannon`, `Fragmentation incendiary tracer shell`); in `projectileHitReplays`. Other players' weapons and ammunition are in no message of a client replay except the kill records |
| 0xF13E | not part damage, as was thought, but a hit's visual effect: a flag, the effect's number, its size and the point in the unit's frame. In the arcade battle 1,674 of 1,724 come with a UnitHitEffects on the same unit within 0.02 s, and all within 3 s; the point is 0.34 m (median) from that hit's. The number comes from a few runs (4303-4306, 4324-4327, 4504-4549, 4867-4873) that are the same on every vehicle and shared with 0xF031 |
| 0xF031 | an effect played on the unit: the effect's number (as in 0xF13E) and a random seed; 282 of 323 come within 0.05 s of a hit on the unit |
| 0xD041 | one per defensive gun of an aircraft, twice a second (median 0.50 s apart) for the whole flight: the gun's index and three floats (zero in all four replays). Checked: each vehicle's indices run 0 to n-1, where n is the number of gunner weapons in its flight model, for 16 of 17 bombers (the A-26B-10 has 4 indices and 12 such weapons spread over its presets) |
| 0xD048 | on aircraft (mostly the recording player's and its target): a count byte and that many 24-byte records (u32 rising, float, double, u64, the last the same in all records of a message). The length fits all 2,660 in the arcade battle; meaning not known |
| 0xF117 | to a unit just hit (all 40 within 3 s): six bytes, a small number, a float that grows; meaning not known |
| the rest (0xF09A HP, 0xD020 gun angles, 0xF015, 0xF04F, ...) | in the messages sidecar with their unit and fields; their meaning is not checked |

Names are the community's (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Also read

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
- **The replay camera** (0xD043, about 20 a second): read, see
  [The camera](ground.md#the-camera); the fields as sent are also in `camera` (every
  0.25 s) and all in the sidecar.

What stays unread, and why:

- **Entity messages' names and bodies** (0x20, 0x21): the class number is
  read, and the two that carry a vehicle's fires (see
  [Vehicle fires](hits.md#vehicle-fires)); of the hashed events (a LEB128 bit
  count, then a 32-bit hash) the fires list is read, the extinguisher's
  (`ca468bcc`: three floats and the extinguishers left) and the others are
  kept. It is 6 bits in all four replays, and its parity bit is right in
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
  layouts read where stated, meaning not known. Not fires either: 0xF0CB
  (DvmDamageDataForReferee, a vehicle's whole damage state, a bit string that
  grows with damage) and 0xF09A change with every hit, but the fires come
  from the entity event above; 0xD0AD (UnitDelayedStatusChange) is two fixed
  bodies sent at spawn.
- **Aircraft fires**: not found in any message read; an aircraft on fire
  has no `fire_on` row.
- **Released weapons' names**: a bomb's or rocket's entity holds its position,
  attitude and velocity, not its name; kill records name the weapon of a kill.
- **Shots that missed**: a client replay holds the hits only (see Gunfire).

## What is needed to check the rest

A server replay of a battle, downloaded by hand from warthunder.com, to see
whether server replays hold everyone's movements and use the same layouts;
a helicopter battle; a ground battle's server replay.
Each match document's `counts.messageIdsNotRead` and `selfCheck` say what
a new replay holds and how well it was read.

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
