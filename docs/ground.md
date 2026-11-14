---
title: Ground units and camera
nav_order: 10
---

# Ground units and camera

## Turrets

A tank's ground state (16-bit attitude) holds, after its position, 141 bits not read, then per turret 62 bits:
the turret's yaw (u16), the gun's pitch (u16), both 360/65536 degrees a step and signed, and 30 bits not read;
then 8 bits, the padding to the byte, and on some states 200 bits more. The turret count is the byte the batch
sends before the state. A state whose length does not fit this gives no turrets (static units send a shorter
state). The yaw is relative to the hull and clockwise positive, 0 straight ahead; the pitch relative to the
hull, up positive. An unused weapon's slot reads 0 and 0 exactly. Checked:

- **The shots**: for every projectile hit (0xF0E9) by a tank, its main gun's world direction (the hull's attitude
  turned by the turret's yaw and the gun's pitch, at the sample at or just before the hit) against the line from
  the shooter to the unit hit, at least 30 m away: of 61,296 such shots in the 100 ground battles, per battle a
  median of 98 % within 3 degrees in heading and 99 % in elevation (no battle under 81 % and 88 %; medians of the
  angles 0.13-0.19 degrees; `selfCheck.turretsVsShots`; the rest are mostly hits by a machine gun in another
  turret). Before the hull pitch was halved and its roll turned, the
  elevation agreed for under half of them.
- **The recording player's aim**: its own tank sends four floats after its state: its aim's world angle (counted
  anticlockwise from east, so the compass heading is 90 degrees less it), the aim's pitch and its distance
  twice (2000 m when nothing is in the sight). The hull's heading plus the turret's yaw lies within 0.44
  degrees (median) of that heading over 4,870 samples (an air-to-ground battle's M8).

**Server replays** (0xF074) send every tank's state in the same layout, followed by data of their own (ammunition
counts and more), so the state's length no longer fits the client's and before this every server-replay tank but a
few came without turrets (2 % of tank rows in the first ground test battle). Every turret whose two angles lie
inside the state is now read (at least the main one: 98 % of tank rows). It is the turret, not the camera:

- **The shots**: the main gun's world direction at each hit against the line to the unit hit (as above): over the
  ten ground server test battles, 15,508 shots, per battle 91-98 % within 3 degrees in heading and 99-100 % in
  elevation (`selfCheck.turretsVsShots`).
- **The view**: a server replay sends every player's aim (`viewYaw`, `viewPitch`; turned into the hull's frame
  for this check). The turret's yaw lies within 0.14-0.41 degrees (median per battle) of the view's, but not
  while it turns: over half a second the view swings at up to 294-357 degrees a second (99th percentile 95-130),
  the turret at most 71-224 (99th percentile 31-73, which includes the hull's own turn of up to 50-85 degrees a
  second; the vehicles' turret drives in the install turn 24-45 degrees a second before crew skills). A turret
  that copied the camera would turn as fast as the camera (`selfCheck.turretVsView`, on the turret as held to its
  drive, below).
- **But not always at a drive's speed**: sample by sample (relative to the hull, so no hull turn in it; every
  0.041 s; angles unwrapped; only while the unit lives) the value as sent turns at 122 degrees a second at the 99th
  percentile and up to 1,072 (the first battle). It is no decoding slip: the same value moves at its drive's speed
  while the player's aim is far from the gun (a BMPT-72: 1.55 degrees every 0.041 s, 38 degrees a second, for
  seconds) and jumps onto the aim when it is near (5-11 degrees in one step, the gun's world heading then within
  0.3 degrees of the aim). No wrap, life change, death, timing or hull turn is in these steps.

So the table holds the turret **held to its drive** (`limit_turrets`): `turretYaw` / `gunPitch` move towards the
value as sent at no more than the main gun's `speedYaw` / `speedPitch` from the install's vehicle file
(`gamedata/units/tankmodels/<vehicle>.blk`, its first `commonWeapons` weapon) times 1.3 for crew skills and
modifications (45 and 20 degrees a second where the install names none), and take that value wherever it is within
reach (89 % of samples in the first battle). At every hit of the main gun (a `shot` row whose line lies within 10
degrees of the turret as sent, at the sample nearest it) the turret is set exactly to the shot's line and a backward
pass brings it there in time; of two shots the drive cannot turn between, the later is not taken
(`selfCheck.turretLimit`: steps over the drive 0, the rates before and after). The `shot` row carries that
`turretYaw` / `gunPitch` too. The shot rows stand at the moment of the hit, not of the firing, so a turret moving
during the shell's flight is set to the line it hit along. The value as sent stays in `turretYawRaw` /
`gunPitchRaw` and `turrets`; `selfCheck.turretsVsShotsRaw` checks it as `turretsVsShots` checks the held one. A tank
whose state carries no turret has empty turret columns (the viewer may fall back to `viewYaw`). `gunPitch` lies a
little above `viewPitch` at range (median 1.9 degrees apart in the first battle): the gun's elevation for the
shell's drop, which the view does not have.



Ships' states have another layout after the position; their turrets are not read (the tank layout fits some of
their states by length, and its "main gun" points 63 degrees away from their shots, so ships get no turret
columns). Other units' look directions: aircraft send no head or view direction; the AA guns' 0xD020
(`GmSetGunAngles`) stays unread.

## The camera

0xD043 ReplayCameraParams, about 20 a second, is the recording player's own replay camera: field 1 a quaternion
(x, y, z, w) turning the camera's (0, 0, 1) to where it looks; 2 the camera's place from the vehicle it follows, in
the game's axes (m); 4 the same offset in the vehicle's own frame (x forward, y up, z left); 5 where the player
aims (a unit vector); 3 the zoom (1.19 in a tank's third-person view, about 1.0 in an aircraft, 2.75 and 5.4 in a
gunner's sight, about 3.7 through binoculars); 6 and 7 the same in every replay. Checked: field 4 is field 2
turned into the frame of the recording player's vehicle at that moment, within 0.5 m for 375,107 of 393,053
messages over the 104 replays (95 %; 72 to 100 % per replay; median 0.00 m); the quaternion's forward has the aim's heading (median 0.01 degrees apart) and, in a
sight, its pitch, while in a tank's third-person view it looks 12 degrees below the aim (the view from above and
behind). The replay sends no field of view in degrees, only the zoom.

The table has the camera as a track of its own: kind `camera`, track `<player> camera #ca`, life `camera`, a row
at most every 0.1 s, at the followed vehicle's place plus field 2, looking along the quaternion (`dirX/Y/Z`,
`heading`, `pitch`, `roll`), with `zoom`, `aimHeading` and `aimPitch`, and `otherLife` the life it follows (where
two of the player's lives have a sample, the one whose frame gives field 4). `selfCheck.camera` counts the rows
and the frame check.

## End of a track

A track is drawn from its first row to its last. When its unit is gone before the replay ends, its last row is a
`despawn` row at its last place: at the time the game removed its entity, when that came within 6 s of its last
sample, else at its last sample (its data ends there: a living enemy no longer sent, or a track cut). A track
without one lasts to the end of the replay. Rows of one track can be far apart (a distant unit or a wreck is
refreshed every 5.5 s, a wreck sometimes not for minutes; a living unit's track goes on over gaps of up to 60 s):
its last state holds until its next row.

## Battle mode

The header's byte at offset 688 holds the difficulty in its low four bits: 0 arcade (AB), 5 realistic (RB), 10
simulator (SB). Checked on the 104 replays: the two air simulator battles read 10, the air arcade battle 0, of
the 100 ground battles 99 read 5 and one 0 - and that one alone names the arcade killstreak aircraft in the
header's `killStreaks` (`killStreaksAircraftOrHelicopter_1`; the realistic ones leave it empty). The game mode is `ground` when the mission lets tanks
spawn, else `naval` when it lets ships, else `air` (`allowedUnitTypes`); the mission's own mode comes from its
key (`missions/_Dom`), named from your install's `lang/missions_versus.csv`. The same key is the `<mode>` part of
the file names and the match id (`Conq4`, `Dom`), left out where the header has none.

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
