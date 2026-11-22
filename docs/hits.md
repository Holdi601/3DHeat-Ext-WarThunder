---
title: Hits, gunfire and fires
nav_order: 13
---

# Hits, gunfire and fires

For readers who want to know where the hit, ammunition and fire columns come
from. Checks give the method and the agreement only.

## Gunfire

Every projectile that hit a unit is in the replay (message 0xF0E9): a `shot`
row at the shooter's position at the moment of the hit, `targetX/Y/Z` the
hit point (the unit hit, moved by the hit point in its frame, turned by its
attitude), the direction towards it, `other` the unit hit. Shells and
bullets that missed are not sent: they are not entities, and the
weapons-in-flight messages hold only rockets, missiles, bombs and torpedoes.
The recording player's rounds left (its `ammo` column) fall as it fires, so
its bursts can be told, but not where those rounds went. Heavy AA and
artillery send each single shot (`gun_shot`, no direction), 40 mm AA guns
their bursts (`fire_start`, `fire_stop`).

Each hit names the damage-model part it struck (`hitPart`, as sent). The
part is a number of one or two bytes: in the first byte bit 0 is a flag and
bits 1-6 are the number's low six bits; when its bit 7 is set, a second
byte follows with the bits above (its low seven). Parts 0-63 take one
byte, the rest two. The number is the part's place in the game's list of
part names, built from `config/damagemodelparts.blk` of your install. The
hit point follows the part, so its place depends on the part's length.

## Hit outcomes

With every projectile hit on a ground unit the server sends message 0xF144
(UnitOnHit) to the unit: four one-byte fields, the fourth the bits of what
the hit did (`selfCheck.unitMessages.outcome_*`):

| Bit | Meaning | Evidence |
|---|---|---|
| 0x20 | a projectile's own hit | nearly all come with a 0xF0E9 hit on the unit within 5 ms; without it, with an explosion (splash) |
| 0x01 | it got through (penetration) | every message with 0x02, 0x04 or 0x08 has it too |
| 0x02 | critical hit | most critical-hit records have it, far more often than chance |
| 0x04 | destroyed | most come with a kill record and the unit's death within a second |
| 0x08 | heavy damage | some critical-hit records have it; rare otherwise |

`hitOutcome` takes the worst: `kill` (0x04), `critical` (0x02 or 0x08),
`penetration` (0x01), `nonpenetration` (0x20 alone). A hit is paired with
the nearest unpaired 0xF144 with 0x20 to its unit within 5 ms. The game's
hit camera tells a ricochet from a non-penetration, but no bit or field
found here does: the first three bytes vary from hit to hit and are not
known. Client replays send 0xF144 only for the recording player's own
aircraft, all bits clear: aircraft and ship hits have no outcome.

## Ammunition

(`selfCheck.unitMessages.ammunition`)

* **Explosive or not.** A shell that bursts sends 0xF133 (UnitOnExplosion)
  with the shooter's uid and the hit's number; a hit with one is
  `explosive`, the rest `kinetic`.
* **The gun and its slot.** 0xF0BD (UnitBulletRearm) is the next round
  loaded: the weapon's index in the vehicle's weapon list, the ammunition
  slot and the rounds left. It is also what tells a change of ammunition: the
  slot loaded changes. A manual loader's comes a steady reload time after
  each of its hits, an autocannon's a fraction of a second after. A
  shooter's hits are grouped by vehicle, signature and burst; a group is a
  weapon's when that weapon loads a round within 20 s after half its hits
  or more at a steady delay. `ammoSlot` is `weapon/slot`, the slot loaded
  before the hit: likely the one fired, unless the player changed the
  ammunition in between. Machine guns send no 0xF0BD.
* **The shell**, in this order (`ammoSource`, `ammoConfidence`):
  * `recorded` (1.0): the killing hit; its kill names the shell
    (`125mm_3bm46`).
  * `slot` (0.9): another hit of the slot a kill named, where the gun's
    calibre agrees.
  * `speed` (0.85): the hit's recorded speed (`shellSpeed`) fits one shell
    of the weapon alone: the weapon file's muzzle speed less the drag over
    the distance (mass, `Cx`, the flight calibre) within 3 %, the next-best
    at least 1 % further off. `ammoSpeedError` is observed / expected - 1.
  * `slot-speed` (0.75): another hit of a slot whose hits with a speed
    agree on one shell.
  * `candidate` (0.6): the weapon has one shell of what the hit did (burst
    or not).
  * `speed-calibre` (0.6): several shells fit the speed; their calibre (and
    type) where they share it.
  * `calibre` / `default` (0.4): only the calibre: the slot's weapon's, a
    machine-gun group's one calibre its signature can have, else the main
    gun's; the type `explosive` or `kinetic`.

  Its type and calibre are then the weapon file's (`bulletName`,
  `bulletType`, `caliber`; `apds_fs_*` APFSDS, `heat_fs_*` HEAT-FS, `he_*`
  HE ...). Without the install (`--game`) there is no type, name or calibre
  beyond `explosive` / `kinetic`.
* **The signature** (`hitShell`) is not a shell's id: one signature can
  stand for several shells, and one shell can come with several signatures.
  It is kept raw.
* **Aircraft and ships** fire from the weapons of their own files: an
  aircraft's flight model (`gamedata/flightmodels/<vehicle>.blk`) puts them
  in slots, each slot's presets naming their weapon files, and a ship's unit
  file lists them like a tank's. A kill names the round that made it: a
  gun's by the round's type (`ap_i_ball_M8`, `frag_i_t`), a rocket's,
  missile's, bomb's or torpedo's by its own name (`su_r_77_1`, `de_sc500`);
  that names the killing hit (`recorded`). The other hits get a calibre where
  the replay tells it: the one calibre of the unit's guns its signature can
  have (an aircraft's signatures are read among all its guns, its cannons
  too); a hit that burst, from a unit that launched no rocket, missile, bomb
  or torpedo in the two minutes before, by its guns that fire bursting rounds
  when they share a calibre; a hit that did not burst, from a unit whose guns
  have one calibre, that one.
* **The belt** (`ammoBelt`). An aircraft's gun (and a machine gun) loads a
  belt: a set of rounds in order, the gun's own (`default`) or one the
  vehicle buys (`50cal_universal`, `mg151_stealth`). Where the rounds a
  shooter's kills name with one calibre are all in one belt of its guns of
  that calibre and in no other, that belt is every hit's of the shooter's
  vehicle with that calibre. The round of a hit by a belt is not in the
  replay: only the killing round is named.

Not found: ricochet; the shell's own id in the hit message; the speed of a
hit on an aircraft (0xF15F comes with hits that went into an armoured unit).

## Hit keys

The first six bytes of a hit (the shooter's uid, a byte, the hit's number, a
byte) also open the other messages about the same hit. `hitKey` is
`shooter:kind:number`; the `after_hit` rows carry it too, so a hit and what
followed it can be joined. A shooter's hit numbers rise by four from one shot
to the next.

## The projectile at the hit

For hits that went into the vehicle (penetrations, critical hits, kills) the
server also sends 0xF15F: the projectile's last simulation step before the
hit. On the shot row:

| Column | What |
|---|---|
| `shellSpeed` | the projectile's speed at the hit, m/s (recorded) |
| `shellPointX/Y/Z` | where that last step began, world (m); on the line from the shooter to the hit |
| `shellDirX/Y/Z` | the projectile's direction then, world (unit vector): its descent and the true firing line |
| `shellLocalX/Y/Z`, `shellLocalDirX/Y/Z` | the same point and direction in the vehicle's own frame (x forward, y up, z right) |
| `shellValue` | one more number of the message (raw; what it is is not known) |

Checked: the local direction is the hit's own direction (`hitDir`), the
point lies on the shot line, and the speed is the shell's muzzle speed from
the weapon file less the drag over the distance (see the checks below).
Hits that did not get through have no such message: their speed is not in
the replay.

## After the hit

0xF117 and 0xF13C name a hit by its key and follow penetrations, critical
hits and kills: one at the hit, often another about a third of a second
later. Each is an `after_hit` row at the vehicle hit, with `hitKey`,
`afterHitMessage` (`F117` or `F13C`), `afterHitFlags` (a byte of bits),
`afterHitValue` (a number that grows with the shell's size; likely the
damage done) and, for 0xF13C, `afterHitCount` (1-3). The first 0xF117 of a
hit is also on its shot row. These values are kept as sent: what the bits
and numbers mean is not known.

## Damaged parts

A hit that damages parts of a vehicle sends one 0xF13A per part, at the
moment of the hit, to the vehicle: the part's number in the vehicle's own
list. The message has no key; the list goes to the hit on that vehicle at
that moment (within 0.05 s) that did most (kill, then critical, then
penetration). A list with no such hit (an explosion near the vehicle) is a
`parts_damaged` row of its own.

| Column | What |
|---|---|
| `damagedPartIds` | the numbers as sent, comma-separated |
| `damagedParts` | their names (`driver_dm`, `ammo_turret_03_dm`, `engine_dm` ...); `#<number>` where the install does not tell |
| `damagedGroups` | what kinds of part: `crew`, `ammo`, `fuel`, `engine`, `transmission`, `gun`, `turret_drive`, `tracks`, `optics`, `armour`, `equipment`; an aircraft's also `airframe` (fuselage, wings, spars, tail), `controls` (control surfaces, flaps, airbrakes), `rotor`, `gear` |
| `crewDamaged`, `ammoDamaged` | how many crew members, how many ammunition racks |
| `destroyedParts` | the modules the hit destroyed (0xF118, `module_destroyed` rows at the same moment), the game's names |
| `damagedFrom` | `destroyed` where the damaged parts are the destroyed modules (below) |

Aircraft get no 0xF13A. What a hit did to one is the modules it destroyed:
the game sends 0xF118 (`module_destroyed`) for each, by the game's part
numbering, and those of a unit at the moment of a hit go to that hit like a
list of damaged parts (`destroyedParts`). A unit that gets no 0xF13A in the
replay has them as its `damagedParts` too (`fuse1_dm`, `wing_l_dm`,
`pilot_dm`, `tank2_dm` ...; `damagedFrom` is then `destroyed` and
`damagedPartIds` the game's numbers), so a pilot killed, a wing or an engine
shot off shows the same way as a tank's crew.

The vehicle's own list: the parts of its unit file's `DamageParts`
(`gamedata/units/tankmodels/<vehicle>.blk`, its groups in order, depth
first) that its damage model has (a node of that name in the vehicle's
collision model, `content/base/res`). The unit file lists many parts a
vehicle may not have (75 turret ammunition racks for every tank); the model
has those it has. Both are read from your install while converting; nothing
of them is written into the files the converter makes, and nothing of them
is part of this program.

A machine without the resource packs (a copy of `aces.vromfs.bin` only)
can use the parts kept by a conversion that had them: each run keeps the
parts of the vehicles it read in `~/.cache/heat3d-wt/part-orders.json`
(`HEAT3D_WT_PARTS` names another file), and
`python -m heat3d_ext_warthunder.damage_parts` keeps those of every vehicle
of the install. A file `heat3d-part-orders.json` beside such a copy's
`aces.vromfs.bin` is read too. The kept parts are put in the order of the
vehicle's unit file as that machine has it.

The game's own part numbering (that of `hitPart` and of the fires' nodes,
`config/damagemodelparts.blk`) names the part a hit struck: `hitPartName`,
and `hitPartNumber` its place in your install's list (where the replay's
game version numbers it otherwise, the number to look it up by). This list
grows with game updates: a newer list has the older one's names in their
order, with new ones put in between, so a replay of an older game version
numbers many parts lower than a newer install. Each fire names its part both
ways, so the fires tell which lists a replay goes by
(`selfCheck.damageParts.gameNumbering`: `numbering`, `by`, `firesAgree`,
`firesDisagree`, `tried`):

1. Your install's, where three or more fires are named both ways and nine in
   ten agree (`matches`: the replay numbers parts as the install does).
2. Else an older game version's own archive, where this machine keeps one
   and nine in ten fires agree with its lists: the converter keeps a copy of
   the install's `aces.vromfs.bin` once per game version (about 20 MB, in
   `~/.cache/heat3d-wt/archives`, `HEAT3D_WT_ARCHIVES` names another
   folder), so replays of today's version still name their parts after the
   next update; an `aces.vromfs.bin.*` copy beside the install is read too.
3. Else the table of the replay's game version: where the names were put in
   between since (game version 101404: from its part 903 on six places
   later, from 933 on eight, from 2363 on thirty-two, against the archive of
   2.61.0.37), with your install's vehicle lists; taken where eight in ten
   fires agree.

A replay with fewer than three such fires goes by its game version: the
install's from 101421 on, else that version's kept archive, else its table.
Where none fits, `hitPartName`, `fireNode` and `partName` stay empty and the
numbers are kept. The vehicles' own lists change less between updates; their
names (`damagedParts`, `firePart`) come from the same lists (an older
archive's where one is taken) and may be off for some vehicles in a replay
older than the install otherwise.

Fires name their part both ways: `fire_on` and `fire_off` rows have
`firePart` (the vehicle's own number, the first of `fireId`) and `fireNode`
(the game's number, the second). A destroyed module (`module_destroyed`)
is numbered the game's way: `partName` and `partGroup`.

## Vehicle fires

A vehicle on fire is shown to every client: the server sends an entity
message to the vehicle (event `0a519c58`) listing the fires burning on it,
each time the list changes. Per fire: two 16-bit ids (the second a
damage-model node), its kind, and -1 until the fire takes. A fire lit by a
hit also gets a message with the point where it burns, in the vehicle's
frame (x forward, y up, z left).

Rows: `fire_on` when a fire appears in the list, `fire_off` when it is gone,
at the vehicle, with `fireId` (`first:node`), `fireKind` and, for fires a
hit lit, `fireLocalX/Y/Z` (forward, up, right). Once a vehicle is dead its
list is often not sent again: its fires end with its wreck, else with its
entity, else with the replay (`selfCheck.fires`).

Checked: each time a tank's fire extinguisher count fell, a fire left its
list within a fraction of a second; most fire points lie on the same side of
the vehicle as the hit that lit them. The kinds are numbers; what they name
is not known. The two ids name the part that burns: the first by the
vehicle's own list, the second by the game's (see
[Damaged parts](#damaged-parts)). Aircraft send no such list: an
aircraft on fire is not read.

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
