---
title: How it reads a replay
nav_order: 10
---

# How it reads a replay

This page is for people who want to know what the converter reads, how it
was checked, and so how far to trust each column. You do not need it to
convert replays.

The reading was checked on client replays of air arcade, air simulator and
naval battles, on server replays of ground battles, and, for the 2025
layouts, on the public sample replays of
[wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder).
Each check compares a value with something the replay says a second,
independent way; only the method and the agreement are given here.

## What is read, and the check

| Part | Status, and the check |
|---|---|
| Header, map, mission, start time, session; results | every file |
| Mission settings (the blk after the header) | mode, weather, limits, `stars` (date, time, place) |
| Packet stream (zlib in 2025, zstd in 2026) | every packet framed |
| Aircraft positions and attitude (2026 layout) | 4 samples a second, no packet left unread; the heading agrees with the direction of travel |
| Flight packets ahead of their time | after a network hitch, a client replay's flight packet sometimes holds every other aircraft where it will be about 0.75 s later. The lead is measured per packet, and each aircraft that leads is given the time it stands for (`selfCheck.flightPacketsRetimed`) |
| Dead-reckoning snaps | a step out of a dead-reckoned run is measured from the last received state, so the client's corrections no longer cut tracks ([Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)) |
| Teleports | a track is cut where its unit moves further than it can: first against its kind (aircraft 750 m/s, ground and ships 40 m/s, weapons 1800 m/s), then against its own pace. Each cut is listed in `trackBreaks` with its likely cause (respawn, the game moving the player, a correction of a distant unit). After the cuts, no step between rows of a track is faster than its kind allows (`selfCheck.stepSpeed`) |
| Ground and ship positions (0xF073 / 0xF074) | no packet left unread. Heading, pitch and roll from the 16-bit attitude: the heading agrees with the direction of travel within about 2 degrees (median); the pitch counts 180/65536 degrees a step; with the roll's sign turned, the gun's direction from hull and turret points at the unit hit for nearly every tank shot. Ships sit at the water level |
| Turrets | tanks' turret yaw and gun pitch: see [Turrets](ground.md#turrets) |
| Packed ground heights | positions packed in 64 bits count their height from -100 m on most levels and from the water level on some; the offset is measured on each replay from units seen in both forms (`selfCheck.packedGroundHeight`) |
| Entity stream (creation, destruction) | every creation read. The layout comes from the Dagor Engine's published source; War Thunder's own component types are skipped by finding where the next component starts. The vehicle and player slot of each unit equal those the kill and hit records name, for every record checked |
| Who drove which unit, AI units, ships, ground targets | from the entity stream: every unit has its vehicle and team, every player's unit its player |
| Kills against the results | the deaths per player equal the results'; the results count more kills, as the client is not sent every kill. A replay that starts after the battle began holds only the kills after that |
| Kills, critical hits, severe damage | every file |
| Destroyed modules (0xF118) | the unit and the part's number; the part's name needs the vehicle's damage model, which is not in the replay |
| Weapons released (entity stream) | the release point is some 10-20 m (median) from the nearest unit, which is taken as the launcher |
| Weapons in flight (0xF0DB) | missiles, rockets and bombs, each tied to its entity |
| Bombs without flight records | a bomb without them gets its fall worked out from release to impact (gravity and drag, a sample every 0.1 s, `extrapolated` true). Checked over the sea, where the impact height is known: the worked-out falls end within about 15 m of the water. In the match document such a weapon has `ballisticImpact`; `counts.bombsBallistic` counts them |
| Player slots, chat | every file |
| Explosions, flak bursts, awards, detections, weather, mission objects | read; positions checked by eye in the viewer |
| The recording player's instruments (0xD04A) | named by what they do: [Cockpit instruments](aircraft.md#cockpit-instruments); the rest under `notNamed` |
| Flight entries' other fields | velocity, rounds, controls, engines: [Flight entries](aircraft.md#flight-entries) |
| Event rows' attitude | every event row carries its unit's heading, pitch, roll and look vector at that moment |
| Player statistics and team scores | at the end of the battle every statistic equals the results' for every player: [Reflection data](aircraft.md#reflection-data) |
| Weapon and vehicle names | from your install's English localisation; a few ships' default belts and airfield radars have no name in the game |
| Players and AI | no row of a results player is AI, every row not AI is a results player's (`selfCheck.identity`) |
| Wrecks | a unit's samples after its death keep coming; a ground unit's or ship's wreck is `alive` 0 until its entity is removed, and stays one track; aircraft keep `alive` 0 for at most 60 s (`selfCheck.wrecks`) |
| Vehicle switches | a player's unit still alive when the same player's next unit appears is ended there (a vehicle left standing). `selfCheck.vehicleSwitch.twoLiveVehicles` must be 0 |
| Battle mode | [Battle mode](ground.md#battle-mode) |
| Aircraft in a 2026 server replay | read in the 2026 layout; the heading and the roll's sign agree with the turns; placeholder aircraft and recon drones carry no data |
| Players of a server replay | found by name in the slots; every statistic equals the results' (`selfCheck.players`) |
| Aircraft in 2025 server replays and version 101286 | not read: their flight packets have a different layout |

## Messages to units

Every type-4 packet is an mpi message of the Dagor Engine's daNet: the
recipient object's id, then (when its low 11 bits are all set) the object's
ext UID, the message id and the payload. A message to a unit carries as its
ext UID the unit's entity id, `index << 10 | generation`. Checked: every
such message names an entity alive at that moment.

For specialists, the messages read:

| Message | What, and the check |
|---|---|
| 0xF0E9 UnitHitEffects | one projectile's hit: the shooter's uid, the damage-model part hit (one or two bytes) and the hit point in the unit's frame (x forward, y up, z left): centimetres on aircraft and ships, on ground units 50/32768 m a step in replays of game version 101421 on and 20/32768 m in older ones (fitted to the vehicles' damage-model parts: the points lie on the part hit). `hitLocalX/Y/Z` in metres. Becomes a `shot` row ([Gunfire](hits.md#gunfire)). The attacker of nearly every hit and kill record is among these shooters; the hit points lie on the side facing the shooter |
| 0xF133 UnitOnExplosion | the same shooter uid |
| 0xF04B OnUnitDead | `dead` rows: every kill record's victim has one within 2 s |
| 0xD047 FmwRpm | the engines' rpm (`rpm`); agrees with the cockpit's rpm gauge |
| 0xF0B1, 0xF0A0 | `gun_shot` rows: single shots of heavy AA and artillery |
| 0xF01B, 0xF01C | `fire_start`, `fire_stop` rows: bursts of 40 mm AA guns (a gun firing; a fire on a vehicle is `fire_on`, see [Vehicle fires](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` rows |
| 0xD0FE ProjectileHitReplay | the recording player's own hits and being hit, with weapon and ammunition, named from the install (`projectileHitReplays`) |
| 0xF13E, 0xF031 | a hit's visual effect and an effect played on the unit; they come with a hit on the same unit |
| 0xD041 | one per defensive gun of an aircraft, twice a second; its indices match the gunner weapons of the flight model |
| 0xD048, 0xF117 | layout read, meaning not known |
| the rest (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | in the messages sidecar with their unit and fields |

Names are the community's (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Also read

- **Entity-stream replication** (0x22, 0x23): per entity a block of
  component values: ship repair timers, consumables' counts, owner and team
  changes, engine overheat. Counted in `counts.replicatedComponents`; the
  values in the messages sidecar.
- **Mission script actions** (0xF028) and **hints** (0xF0EC): `triggers`,
  `hints`. **Mission progress** (0xF07A, 0xF07C): `missionProgress`.
- **The replay camera** (0xD043): see [The camera](ground.md#the-camera).

## Not read, and why

- **Entity messages' names and bodies** (0x20, 0x21): the class number is a
  place in a list compiled into the game, not sent and not in its data. Two
  are read (a vehicle's fires and its extinguishers); the rest are kept
  whole with their entity and class number.
- **Other replicated objects** (kinds other than player slots and teams):
  read and kept, not named; nothing in the results to check them against.
- **Other aircraft's controls, throttle and rounds**: refreshed only now and
  then; kept in the flight sidecar, not in the table.
- **Aircraft fires**: not found in any message; an aircraft on fire has no
  `fire_on` row.
- **Released weapons' names**: a bomb's or rocket's entity holds no name;
  kill records name the weapon of a kill.
- **Shots that missed**: a replay holds the hits only.

Each match document's `counts.messageIdsNotRead` and `selfCheck` say what a
new replay holds and how well it was read.

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
