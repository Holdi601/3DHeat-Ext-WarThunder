---
title: Objectives
nav_order: 15
---

# Objectives

`objectives` in the match document lists what the battle is fought over, from two sources (`source`):

- **The replay** (`replay`): the mission objects 0xD039 names (capture zones `cz_circle_NN`, airfields, helipads,
  bases), placed where the replicated objects of kind 3 (0xF02D) put them now - a capture zone starts at its
  template's place and is moved to this mode's zone at the start (`moved`). Kind 3's numbers follow 0xD039's order;
  every object that is not moved lies exactly where 0xD039 has it, which checks the order. A capture zone gets the
  shape and radius of the mission area at its place (`area`, within 2 m) and its letter from its own index (kind
  5 field 69: 0 = A); the letter order is the replay's, not checked against the game's map.
- **The mission** (`mission`): the mission file `<mission>.blk` in your install's `mis.vromfs.bin` and the
  templates it imports (read only, at conversion time): its areas, classed by name - spawns (a spawn's numbered
  points `..._spawnareaNN` as one `points` spawn), battle areas, bombing targets (`bomb_zone`), convoy spawn
  points (`road_NN_spawn`), exit and kill areas. Areas of another mode of the same map (`conq_`, `dom_`, `bttl_`,
  ...) are left out, and of `_arcade` / `_realistic` / `_hardcore` variants the battle's own (RB takes
  `_realistic`, else `_hardcore`, as the mission scripts do); briefing markers, AA gun points and areas wider than
  5 km (the areas spawns are scattered over) too. Each spawn says how many players' tracks began in it (`used`,
  `usedByTeam`). A mission may swap its sides at random (`randomSpawnTeams`): when the spawns show the replay's
  teams the other way round, every `team` is swapped and the name's side kept as `missionTeam`. Convoy routes are
  not in the missions' waypoints as read; only where convoys appear is given.

The capture zones over time are the sidecar `<match>.objectives.parquet`: the replicated objects of kind 5, one
per zone - field 2 its owner (0, 1, 2), field 67 its capture progress, a signed byte from -100 to 100 (positive
towards team 2), field 69 its index. Checked (`selfCheck.objectives`) on ground server replays of Conquest and Domination battles: every owner change
comes with a player of the capturing team gaining a `captureZone` in the scoreboard at the same moment (within
1.5 s) and with a living ground unit of that team inside the zone; every battle's spawns show the replay's teams
one way only (often swapped against the mission's `t1_` / `t2_`).

## Scene units: trams and rail wagons

A level can place units of its own: the `unit_loader+rail_wagon` entities of a server replay are the trams of the
level's scene file (`gamedata/scenes/<level>_objects.blk` in `aces.vromfs.bin`: `setting__unit_class`, its
transform and `setting__isDead`). Their entities carry no readable uid, so a ground track without a unit entity
whose first sample lies within 2 m of a scene unit is that unit: its class as `Vehicle`, kind `train`, type
`tram`, `locomotive` or `wagon`, no team; a unit the scene places dead (such as burnt-out trams) is a wreck (`alive` 0) from its first row. The game has no English name for them; `VehicleName` is the id
read as words ("Railway tram A"). Their positions do not wobble: nearly all never move (every
sample the same to the bit). The replay sends them about ten times a second
regardless, so of their samples only those that move them (0.05 m or 0.1 degrees) are kept, and one every 10 s
(`selfCheck.sceneUnits` counts the samples dropped). Before, they were tracks named `uid 8`
with no vehicle.

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
