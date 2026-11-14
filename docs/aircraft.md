---
title: Aircraft
nav_order: 9
---

# Aircraft

## Cockpit instruments

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

## Flight entries

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

## Reflection data

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

## Dead reckoning, and the smoother

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

## Attitude, checked

On the recording player's own aircraft: the heading lies within 0.2 to 0.8
degrees (median) of the direction of travel, the pitch within 0.3 to 2.3 degrees of
the climb angle, and in clear turns the packed roll is positive in left turns
(235 of 237 samples in the arcade battle, 262 of 263 and 190 of 194 in the
sim battles): the flight model's roll is left wing down positive, and the
table turns it to right wing down positive (`selfCheck.aircraftAttitude`).
The 10-bit angles step 0.18 degrees. Ground units' attitude is checked against their shots (see Turrets).

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
