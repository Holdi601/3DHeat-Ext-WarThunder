---
title: Aircraft
nav_order: 11
---

# Aircraft

For readers who want to know where the aircraft columns come from and how
far to trust them. Each check below compares a value with something the
replay says a second, independent way; only the method and the agreement
are given.

## Cockpit instruments

Message 0xD04A sends the recording player's gauges as (number, value)
pairs: four a second in arcade battles, only changed values in simulator
battles. The numbers form one list across all cockpits, and a cockpit sends
the gauges its model has. The game's code sets which number is which gauge,
so each number was named by what it does and checked against the replay
(`convert.INSTRUMENTS` holds the result; nothing is read from the install):

| Number | Name | Checked against |
|---|---|---|
| 0 | indicated airspeed, m/s | the track's speed corrected for air density: correlation 0.99 |
| 39 | climb rate, m/s | the track's climb rate: correlation above 0.99 |
| 40, 41 | altitude, m; altitude modulo 1000 | the track's height, a few metres apart |
| 52, 53 | artificial horizon roll and pitch | minus the table's roll and pitch, under 1 degree apart |
| 64 | compass | the table's heading, under 0.1 degree apart |
| 15-20 | rudder pedals | the side force on the aircraft |
| 23, 31 | stick: elevator and ailerons (sign as the cockpit model's) | the angle of attack; the roll rate |
| 69, 71, 73 | clock: hours (12-hour dial), minutes, seconds | the recording computer's local time, to the minute |
| 75 | manifold pressure, atm | higher at war emergency power than at full throttle |
| 81-86, 87-92, 93-98 | rpm per engine, rpm modulo 1000, rpm gauge | each other exactly; the engine rpm: correlation above 0.97 |
| 195 | fuel | falls through a sortie, full again at a respawn |
| 228-230 | landing gear legs, 1 down | down only near the airfields' height and at landing speed |
| 240, 241 | throttle per engine (1.1 war emergency power or afterburner) | the flight entry's throttle |
| 330-332, 346-348 | ammunition counters (two equal sets) | the weapon preset's rounds, falling with the flight entry's rounds |
| 135, 159 | oil and cylinder head temperature | likely: they rise over a sortie |
| 58, 61 | slip ball, turn needle | likely: they follow the side force and the turn rate |
| 223 | airbrake | likely: set only on approach |
| 490-497, 500-505 | wheel brakes | likely: set only standing on an airfield |

A few more numbers are sent whose meaning is not known; they are kept in
the match document's `authorInstruments.notNamed`.

The table's `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`,
`oilTemperature`, `headTemperature` and `throttle` come from these, on the
recording player's own rows, taking the last message at most 0.2 s after
the sample.

## Flight entries

Each aircraft's flight entry (packet type 2) carries, besides its position
and attitude:

- **Velocity**: a 32-bit word after the attitude. Bits 31, 30 and 29 are the
  signs of x, y and z; then the speed in 11 bits of 500/2047 m/s (it stops at
  500 m/s), then |x| and |y| as fractions of the speed in 9 bits each, and z
  is what makes the vector a unit vector. Checked against the step between
  received samples: the direction agrees within a fraction of a degree for
  the recording player and within about 2 degrees for everyone else; the
  speed within 0.2 %. `selfCheck.flightEntries`.
- **Rounds per weapon**: a list before the position, one item per weapon,
  the rounds left first. The recording player's equals the cockpit's
  counters one tick later for nearly every sample.
- **Controls and throttle**: 7 bytes after the velocity, read as 14 nibbles.
  For the recording player, every tick: 1 the elevator, 2 the ailerons, 3
  the rudder (8 at rest), 11 the throttle in fifteenths (15 also for war
  emergency power and afterburner), 4 the wheel brakes, 5 the airbrake, 8
  likely the brake chute. Other aircraft's nibbles change only a few times a
  battle and are not their controls at the time.
- **Engines**: per engine a state byte (0 off; 1-6 starting; 7 running; 8
  dead), a 16-bit value only with afterburner (32767 full), and a byte only
  after the engine was hit. Most aircraft whose engine goes "dead" are
  killed or end within minutes.

## Reflection data

Messages 0xF02D and 0xF0AA replicate the game's numbered objects: per object
its id (the top 5 bits the kind, the low 11 an index) and a field table.
Kind 14 is the player slots (field 2 user id and name, 9 the team), kind 15
the teams (index 1 and 2):

- A slot's field 39 holds its statistics at fixed places: kills (offset 0),
  team kills (2), deaths (4), naval kills (10), AI kills (12), AI ground
  kills (14), assists (20), capture zones (22), zone damage (24, 32-bit),
  damage award (40, 32-bit), missile evades (50). Field 38 starts with the
  score, field 42 is the squad. At the end of a battle every value equals
  the results' for every player (`selfCheck.scoreboardVsResults`). Where
  ground kills are kept is not known.
- A team's field 7 is its score: at the end it equals the sum of its
  players' scores in the results. Field 3 is likely its tickets.
- Each message sends only the fields that changed, so `scoreboard` in the
  match document lists every player's statistics and every team's score at
  each change.

## Dead reckoning, and the smoother

A client replay records every aircraft four times a second, as the client
drew it. Between the updates it receives for a distant aircraft, the client
moves it on along its last velocity and turns it on at its last rates, and
at the next update snaps it there. Read as it is, a track runs straight,
then jumps. Nothing in the flight entry marks which samples were received;
a dead-reckoned sample is found by what it is: it continues the straight
line of the two samples before it, at their pace, to within 3 cm.

How much this matters depends on the battle: in arcade battles about half
of the other aircraft's samples can be dead-reckoned, in simulator battles
only a few percent. The smoother cuts the steps over 15 g by about five
times (`selfCheck.deadReckoning`). The recording player's own aircraft is
not extrapolated by the client and is left as it is.

By default (`--no-smoothing` turns it off) the tracks of all units but the
recording player's own are put where the received states say they were: a
dead-reckoned sample goes on a curve through the received samples before
and after it, each with its own velocity; over more than 3 s the straight
line is only bent towards the next received sample, so no sample moves
further than the client's own snap. Its attitude is turned evenly from one
received attitude to the next. Received samples are smoothed by at most 2 m
or 0.04 s of their speed; a steady turn stays as it is. The replay's own
values stay in the `Raw` columns.

## Attitude, checked

On the recording player's own aircraft the heading lies within a degree
(median) of the direction of travel, the pitch within a few degrees of the
climb angle, and in clear turns the roll has the turn's sign for nearly
every sample: the flight model's roll is left wing down positive, and the
table turns it to right wing down positive (`selfCheck.aircraftAttitude`).
The 10-bit angles step 0.18 degrees. Ground units' attitude is checked
against their shots ([Turrets](ground.md#turrets)).

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
