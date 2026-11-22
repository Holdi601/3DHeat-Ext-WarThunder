---
title: The table
nav_order: 6
---

# The table

![The table of a synthetic replay, summarised](assets/img/table.svg)

One row per sample or event, 155 columns ([Column list](columns.md), generated from the code); in the footer, under `heat3d`, the viewer's
reading instructions, so the viewer needs no form filled in.

| Column | What |
|---|---|
| `time` | seconds on the replay's own clock |
| `event` | `position`; event rows lie on the track at their moment (between two samples, on the line between them); `kill` (at the killer), `death` (at the victim), `hit_critical` / `hit_severe` (at the unit hit), `module_destroyed` (at the unit), `launch` (at the unit that released a weapon), `impact` (a weapon's last sample when it was removed right after); `explosion` and `flak` (0xD08E, 0xD01F) at their position, kind `effect`, no track, with the explosion's direction where it has one; `shot` (a projectile that hit, at the shooter), `gun_shot`, `fire_start`, `fire_stop` (a gun's burst, not a vehicle on fire), `fire_on`, `fire_off` (a vehicle on fire, see [Vehicle fires](hits.md#vehicle-fires)), `after_hit` (what followed a hit, at the unit hit, see [After the hit](hits.md#after-the-hit)), `parts_damaged` (parts damaged with no hit to put them on, see [Damaged parts](hits.md#damaged-parts)), `reward` (Silver Lions and research points earned, see [Economy](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (see [Messages to units](how-it-reads.md#messages-to-units)); `despawn`: the last row of a track whose unit is gone before the replay ends (see [End of a track](ground.md#end-of-a-track)) |
| `track` | what the viewer draws as one thing: one life of a unit, or one weapon's flight - `<player or vehicle> #<hex>` (the viewer shows the name without the `#` part) |
| `x`, `y`, `z` | the game's metres: x east, y up, z north (the hints mirror z, so north is not drawn south) |
| `player` | the player's name; an AI unit `<VehicleName> #<uid>` (for example `F-15A #204`); `uid <n>` when nothing names it; for a weapon, who released it |
| `userId`, `team` | the player's Gaijin id and the team (`1`, `2`) |
| `ai`, `isPlayer` | `ai` true for every unit no player account drives (mission units, AI aircraft, ground targets, AA guns, ships without a player, placeholders), `isPlayer` the opposite: a player is a unit whose entity names a player slot with a Gaijin id. A weapon has its launcher's; empty when not known |
| `match` | the match id (the match document's `match`), on every row; the hints map it as the session, so two loaded replays never join tracks |
| `life` | `uid#n`: one unit's track, cut where the uid passes to another unit, the unit moves faster than it can (a respawn, a rearm, the game moving it, the client correcting a distant unit; see Teleports in [How it reads a replay](how-it-reads.md#what-is-read-and-the-check)) or is long unseen; `w<hex>` a weapon's flight (`w<hex>#n` after a cut) |
| `uid` | the unit's id in the replay |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (a tram or rail wagon the level places, see [Scene units](objectives.md#scene-units-trams-and-rail-wagons)); weapons `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` the recording player's replay camera (see [The camera](ground.md#the-camera)) |
| `type` | the game's own type where the results name it (`fighter`, `assault`, `destroyer`, `gun_boat`), else as `kind` |
| `Vehicle` | the game's vehicle id (`f_15a`, `germ_flakpz_I_Gepard`), which the viewer's figures match |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | the vehicle's English name from your install's localisation (`Pz.Kpfw. III Ausf. J1`, short `Pz.III J1`) and its key (`germ_pzkpfw_III_ausf_J_0`); the game font's country marks are left out. Where the game names nothing, or no install is found, the name is the id and the key empty |
| `mission` | the unit's name in the mission (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | where the unit points (the look vector): aircraft from the flight model's attitude, ground units and ships from their own, weapons along their flight |
| `heading`, `pitch`, `roll` | the same in degrees; heading is the compass, clockwise from north, pitch nose up positive, roll right wing down positive (the flight model sends the opposite sign, see [Attitude, checked](aircraft.md#attitude-checked); a ground unit's right side down). The hints say so under `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | a tank's main turret - where the gun points, not where its player looks; the replay's value held to the turret drive's speed and set to each main-gun shot's line (see [Turrets](ground.md#turrets)): its yaw relative to the hull (degrees, clockwise seen from above positive, 0 straight ahead) and its gun's pitch relative to the hull (degrees, up positive); `turrets` every turret of the vehicle as `yaw pitch;yaw pitch;...` in its own order (an unused slot reads `0.00 0.00`). Tanks, SPAA, APCs and trucks, in client and server replays; not ships (see [Turrets](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | the main turret as the replay sends it; `turretYaw` / `gunPitch` are it held to the turret drive's speed and set to each main-gun shot's line (see [Turrets](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | where the player looks (aims with the camera) in the world: compass degrees (0 north, clockwise) and degrees up, the same convention as `aimHeading` / `aimPitch` (unlike `turretYaw` / `gunPitch`, which stay relative to the hull). Every player's tank in a server replay, the recording player's own in a client replay; empty where the player aims nowhere (all four aim floats 0). Server replays: every other unit (aircraft, helicopters, drones, ships) from its player's camera, a targeting camera's own direction (see [Every player's camera](ground.md#every-players-camera-server-replays)). The turret follows it at its own traverse speed, so the two differ while it turns (see [Turrets](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | the recording player's own tank: where it aims (compass degrees, degrees up, the distance in m; 2000 when nothing is in the sight); camera rows: where the player aims (heading, pitch) |
| `zoom` | camera rows: the camera's magnification (see [The camera](ground.md#the-camera)) |
| `difficulty`, `gameMode` | the battle's `AB`, `RB` or `SB`, and `ground`, `air` or `naval`, on every row (see [Battle mode](ground.md#battle-mode)) |
| `extrapolated` | an aircraft sample that is the client's dead reckoning, not a state it received (see [Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)); a bomb's sample worked out from its release (see Bombs without flight records in [How it reads a replay](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | how far the smoother moved the sample (m), and the replay's own position and attitude (roll in the table's sign) |
| `targetX`, `targetY`, `targetZ` | a `shot`'s hit point |
| `hitOutcome`, `hitFlags` | a `shot`'s outcome on a ground unit: `kill`, `critical`, `penetration` or `nonpenetration` (bounced or stopped: the replay does not tell a ricochet apart), from the bits the server sends with the hit (`hitFlags`, raw); empty where none is sent (aircraft, ships). See [Hit outcomes](hits.md#hit-outcomes) |
| `hitShell` | a `shot`'s shell signature: four bytes of the hit message (raw hex); one signature can stand for different shells (120 and 125 mm APFSDS share one), so it is kept raw, not read as a calibre |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | a `shot`'s ammunition: its type (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) and id (`125mm_3bm46`) where it is known, else `explosive` (the hit burst) or `kinetic`; the gun's `weapon/slot` from its reloads; the calibre in mm from the install's weapon files. See [Ammunition](hits.md#ammunition) |
| `ammoSource`, `ammoConfidence`, `ammoSpeedError` | where a `shot`'s ammunition is known from (`recorded`: its kill names it; `slot`; `speed`; `slot-speed`; `candidate`; `speed-calibre`; `calibre` / `default`), how sure that is (0-1), and how far its recorded speed lies from the shell's expected one (observed / expected - 1). See [Ammunition](hits.md#ammunition) |
| `hitKey` | a hit's key, `shooter:kind:number`: on `shot` and `after_hit` rows. See [Hit keys](hits.md#hit-keys) |
| `hitPartName` | the part a `shot` struck, by the game's part list (`hitPart`'s number) |
| `shellSpeed`, `shellPointX/Y/Z`, `shellDirX/Y/Z`, `shellLocalX/Y/Z`, `shellLocalDirX/Y/Z`, `shellValue` | the projectile at a `shot` that went into the vehicle: its speed (m/s), where its last step began and its direction (world; and in the vehicle's frame: x forward, y up, z right), one raw value. See [The projectile at the hit](hits.md#the-projectile-at-the-hit) |
| `afterHitMessage`, `afterHitFlags`, `afterHitValue`, `afterHitCount` | an `after_hit` row (and the first on its `shot`): the message (`F117`, `F13C`), its bits, its number, its count; raw |
| `damagedPartIds`, `damagedParts`, `damagedGroups`, `crewDamaged`, `ammoDamaged`, `damagedFlags` | the parts a `shot` damaged (or a `parts_damaged` row's): their numbers in the vehicle's own list, their names (`#<number>` where the install does not tell), their kinds (`crew`, `ammo`, `fuel`, `engine` ...), how many crew members and ammunition racks, the flag bytes where any is set. See [Damaged parts](hits.md#damaged-parts) |
| `firePart`, `fireNode` | a fire's part: by the vehicle's own number (`fireId`'s first) and by the game's (its second) |
| `partName`, `partGroup` | a `module_destroyed` row's part and its kind |
| `rpm` | an aircraft's engine rpm (the mean over its engines) as last sent, within 2 s |
| `vx`, `vy`, `vz` | an aircraft's velocity as its flight entry sends it (m/s, the game's axes; speeds over 500 m/s read 500) |
| `engine`, `afterburner`, `engineCondition` | an aircraft's engines from its flight entry: `off`, `starting`, `running`, `dead` (`/`-joined when its engines differ); the afterburner 0-1; a byte sent only after the engine was hit |
| `weaponName` | kills and deaths: the weapon or ammunition in your install's English (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | the recording player's aircraft only: the throttle 0-1.1 from its cockpit (1.1 war emergency power or afterburner; else its flight entry's fifteenths), the controls -1..1 from its flight entry (elevator positive pulling, aileron positive rolling right), the rounds left per weapon (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | the recording player's aircraft only, from its cockpit: indicated airspeed and climb rate (m/s), fuel, manifold pressure (atm), gear (0-1, 1 down), oil and cylinder head temperature, where its cockpit has the gauge |
| `speed` | m/s over about two seconds of the track (worked out here; the replay sends no speed for other units) |
| `alive` | 0 for a unit's samples after its death (its wreck): a ground unit's or ship's until the game removes it or its samples end, an aircraft's for at most 60 s |
| `otherVehicle`, `otherLife` | a `shot`'s victim: its vehicle and its `life` |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | a `shot`'s hit point in the victim's own frame (m; x forward, y up, z left; see [Messages to units](how-it-reads.md#messages-to-units)) and the way the shot came, turned into that frame by the victim's attitude then |
| `hitPart`, `hitFlag` | a `shot`'s hit message: the damage-model part hit as sent (one or two bytes, little-endian; see [Gunfire](hits.md#gunfire)), and its second byte (0 for a one-byte part) |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won`, `matchWon`, `round`, `roundEndReason` | what the battle cost and earned, who won and how it ended: see [Economy](economy.md) |
| `other`, `weapon` | kills: the other side and the weapon; hits: who hit (from the record's uid, else its player slot), their vehicle; launches: the weapon; destroyed modules: who last hit the unit within 5 s before, and `part <n>` |

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
