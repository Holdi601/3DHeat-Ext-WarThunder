---
title: Ground units and camera
nav_order: 12
---

# Ground units and camera

For readers who want to know where the turret, camera and battle-mode
columns come from and how far to trust them. Checks give the method and the
agreement only.

## Turrets

A tank's ground state (16-bit attitude) holds, after its position, 141 bits
not read, then per turret 62 bits: the turret's yaw and the gun's pitch
(16 bits each, 360/65536 degrees a step, signed) and 30 bits not read; then
padding, and on some states 200 bits more. The turret count is the byte sent
before the state. A state whose length does not fit gives no turrets (static
units send a shorter state). The yaw is relative to the hull, clockwise
positive, 0 straight ahead; the pitch relative to the hull, up positive.

How it was checked:

- **Against the shots:** for every hit by a tank, its main gun's world
  direction (hull attitude turned by turret yaw and gun pitch) against the
  line from the shooter to the unit hit, at least 30 m away: per battle a
  median of about 98 % within 3 degrees in heading and 99 % in elevation
  (`selfCheck.turretsVsShots`). The rest are mostly hits by a machine gun in
  another turret.
- **Against the recording player's aim:** its own tank sends its aim's world
  angle (anticlockwise from east), pitch and distance. The hull's heading
  plus the turret's yaw lies within half a degree (median) of the aim.

**Server replays** (0xF074) send every tank's state in the same layout,
followed by data of their own, so every turret whose two angles lie inside
the state is read (at least the main one for nearly every tank row). It is
the turret, not the camera:

- **Against the shots**, as above: per battle above 90 % within 3 degrees in
  heading and 99 % in elevation.
- **Against the view:** a server replay sends every player's aim
  (`viewYaw`, `viewPitch`). The turret follows the view within half a degree
  (median), but turns far slower than the view swings, as a turret drive
  does (`selfCheck.turretVsView`).
- **But not always at a drive's speed:** sample by sample, the value as sent
  sometimes jumps onto the aim when the aim is near the gun, faster than any
  drive turns.

So the table holds the turret **held to its drive**: `turretYaw` /
`gunPitch` move towards the value as sent at no more than the main gun's
turning speed from the install's vehicle file (times 1.3 for crew skills
and modifications; 45 and 20 degrees a second where the install names
none). At every hit of the main gun the turret is set exactly to the shot's
line, and a backward pass brings it there in time (`selfCheck.turretLimit`).
The `shot` row carries that `turretYaw` / `gunPitch` too. The value as sent
stays in `turretYawRaw` / `gunPitchRaw`. A tank whose state carries no
turret has empty turret columns (the viewer may fall back to `viewYaw`).
`gunPitch` lies a little above `viewPitch` at range: the gun's elevation for
the shell's drop.

Ships' states have another layout; their turrets are not read. Aircraft
send no head or view direction; the AA guns' message 0xD020 stays unread.

## The camera

Message 0xD043, about 20 a second, is the recording player's own replay
camera: field 1 a quaternion turning the camera's forward to where it looks;
2 the camera's place from the vehicle it follows (m); 4 the same offset in
the vehicle's own frame (x forward, y up, z left); 5 where the player aims
(a unit vector); 3 the zoom (about 1.2 in a tank's third-person view, about
1.0 in an aircraft, higher in a gunner's sight or through binoculars).
Checked: field 4 is field 2 turned into the vehicle's frame, within 0.5 m
for nearly every message; the camera's forward has the aim's heading. The
replay sends no field of view in degrees, only the zoom.

The table has the camera as a track of its own: kind `camera`, track
`<player> camera #ca`, a row at most every 0.1 s, at the followed vehicle's
place plus field 2, looking along the quaternion (`dirX/Y/Z`, `heading`,
`pitch`, `roll`), with `zoom`, `aimHeading` and `aimPitch`, and `otherLife`
the life it follows. `selfCheck.camera` counts the rows and the check.

## End of a track

A track is drawn from its first row to its last. When its unit is gone
before the replay ends, its last row is a `despawn` row at its last place:
at the time the game removed its entity (when that came within 6 s of its
last sample), else at its last sample. A track without one lasts to the end
of the replay. Rows of one track can be far apart (a distant unit or a wreck
is refreshed every few seconds, a wreck sometimes not for minutes): its last
state holds until its next row.

## Battle mode

The header's byte at offset 688 holds the difficulty in its low four bits:
0 arcade (AB), 5 realistic (RB), 10 simulator (SB). Checked against the
battle types the replays were known to be. The game mode is `ground` when
the mission lets tanks spawn, else `naval` when it lets ships, else `air`
(`allowedUnitTypes`); the mission's own mode comes from its key
(`missions/_Dom`), named from your install's `lang/missions_versus.csv`. The
same key is the `<mode>` part of the file names and the match id (`Conq4`,
`Dom`), left out where the header has none.

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
