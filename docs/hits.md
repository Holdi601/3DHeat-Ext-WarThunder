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
  slot and the rounds left. A manual loader's comes a steady reload time
  after each of its hits, an autocannon's a fraction of a second after. A
  shooter's hits are grouped by vehicle, signature and burst; a group is a
  weapon's when that weapon loads a round within 20 s after half its hits
  or more at a steady delay. `ammoSlot` is `weapon/slot`, the slot loaded
  before the hit: likely the one fired, unless the player changed the
  ammunition in between. Machine guns send no 0xF0BD.
* **The shell.** A kill's weapon is the shell's id (`125mm_3bm46`); the
  killer's last hit on the victim gives it to that shooter's slot, where
  the gun's calibre agrees. Its type and calibre are the weapon file's
  (`bulletName`, `bulletType`, `caliber`; `apds_fs_*` APFSDS, `heat_fs_*`
  HEAT-FS, `he_*` HE ...).
* **The calibre** of the rest: a slot's weapon's; a machine-gun group's the
  one machine-gun calibre its signature can have; otherwise the vehicle's
  main gun's. Without the install (`--game`) there is no type, name or
  calibre beyond `explosive` / `kinetic`.

Not found: ricochet. Several more messages carry the hit's shooter and
number (0xF0C2, likely the hit camera's path through the vehicle; 0xF117,
0xF13C, 0xF13E); they are kept in the sidecar, not decoded. A
non-penetration stays `nonpenetration`.

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
is not known, nor which part a node is. Aircraft send no such list: an
aircraft on fire is not read.

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
