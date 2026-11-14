---
title: Hits, gunfire and fires
nav_order: 11
---

# Hits, gunfire and fires

## Gunfire

Every projectile that hit a unit is in the replay (0xF0E9, above): a `shot`
row at the shooter's position at the moment of the hit, `targetX/Y/Z` the hit
point (the unit hit, moved by the hit point in its frame, turned by its
attitude), the direction towards it, `other` the unit hit. Shells and bullets
that missed are not sent: they are not entities, the weapons-in-flight
messages hold only rockets, missiles, bombs and torpedoes. The recording
player's rounds left (its `ammo` column) fall as it fires, so its bursts can
be told, but not where those rounds went. Heavy AA and artillery
send each single shot (`gun_shot`, no direction), 40 mm AA guns their bursts
(`fire_start`, `fire_stop`).

## Hit outcomes

With every projectile hit on a ground unit the server sends 0xF144
(UnitOnHit) to the unit: four one-byte fields, the fourth bits of what the
hit did. Found on the ground test battle (1,745 messages, 1,619 hits; the
check below is `selfCheck.unitMessages.outcome_*`):

| Bit | Meaning | Evidence |
|---|---|---|
| 0x20 | a projectile's own hit | 98-100% come with a 0xF0E9 hit on the unit within 5 ms; without it 99% come with an explosion (0xF133): splash, not a shot row |
| 0x01 | it got through (penetration) | every message with 0x02, 0x04 or 0x08 has it too; 0x20 alone (464) never has a kill or crit record within 0.2 s more often than chance |
| 0x02 | critical hit | 11 of the 15 critical hit records have it, against 13% of all messages |
| 0x04 | destroyed | 64% have a kill record on the unit within 0.2 s and 66% its death within 1 s, against 2-3% without it; 25 of the 36 killing hits found |
| 0x08 | heavy damage | 4 of the 15 critical hit records, 0.5% of all messages |

`hitOutcome` takes the worst: `kill` (0x04), `critical` (0x02 or 0x08),
`penetration` (0x01), `nonpenetration` (0x20 alone). A hit is paired with the
nearest unpaired 0xF144 with 0x20 to its unit within 5 ms (1,510 of 1,619).
The game's hit camera tells a ricochet from a non-penetration
(`hitcamera/result/ricochet`, `hitcamera/result/bounce` in `menu.csv`), but
no bit or field found here does: the first three bytes vary from hit to hit
and are not known. Client replays (the air test battles) send 0xF144 only
for the recording player's own aircraft, all bits clear: aircraft and ship
hits have no outcome. 0xF13E's effect numbers (5 in the ground battle) are
too few to say more.

The ammunition (`selfCheck.unitMessages.ammunition`; numbers from the ground
test battle, 1,619 hits):

* **Explosive or not.** A shell that bursts sends 0xF133 (UnitOnExplosion)
  with the shooter's uid and the hit's number; a hit whose number has one is
  `explosive` (165 hits), the rest `kinetic`. Certain: the number is the
  hit's own.
* **The gun and its slot.** 0xF0BD (UnitBulletRearm) is the next round
  loaded: the weapon's index in the vehicle's weapon list
  (`gamedata/units/tankmodels/<vehicle>.blk`: `commonWeapons`, then its
  weapon preset's), the ammunition slot and the rounds left. A manual
  loader's comes a steady 7.6 s after each of its hits (its reload), an
  autocannon's 0.1 s after. A shooter's hits are grouped by vehicle,
  signature and burst; a group is a weapon's when that weapon loads a round
  within 20 s after half its hits or more at a steady delay (median absolute
  deviation 1 s or less). `ammoSlot` is `weapon/slot`, the slot loaded
  before the hit (1,003 hits). Likely: the slot is the one loaded, which is
  the one fired unless the player changed the ammunition in between.
  Machine guns send no 0xF0BD.
* **The shell.** A kill's weapon is the shell's id (`125mm_3bm46`); the
  killer's last hit on the victim gives it to that shooter's slot (the
  player chose what each slot holds, so it is never carried to another
  player), where the gun's calibre agrees (26 of 28 kills; the other two name
  nothing). Its type and
  calibre are the weapon blk's (`bullet` blocks: `bulletName`, `bulletType`,
  `caliber`; `apds_fs_*` APFSDS, `heat_fs_*` HEAT-FS, `he_*` HE...): 720
  hits named, 12 slots.
* **The calibre** of the rest: a slot's weapon's; a machine-gun group's the
  one machine-gun calibre the signature can have on every vehicle that
  fires it, after the calibres other signatures took (`00c01f20` 7.62,
  `01401400` 12.7); an explosive or gun-signature hit without a slot the
  vehicle's main gun's. 1,611 of 1,619 hits have one. Without the install
  (`--game`) there is no type, name or calibre beyond `explosive`/`kinetic`.

Not found: ricochet. Checked on the ground battle: the three unknown bytes
of 0xF144 (spread alike over penetrations and non-penetrations, no value or
bit only on the 470 non-penetrations); the 0xF0E9 rest after the hit point
(the signature goes with the shell's class, not the outcome; the bit stream
shifts by whole fields from hit to hit and is not decoded); 0xF0C2, sent
for 850 hits with the hit's shooter and number and a long bit stream of
one to nineteen records (likely the hit camera's path through the vehicle:
1 record for most non-penetrations, more for penetrations), not decoded;
0xF117 and 0xF13C (carry the hit's shooter and number, nearly all on
penetrations); 0xF13E (5 messages). A non-penetration stays
`nonpenetration`.

## Vehicle fires

A vehicle on fire is shown to every client, and the server sends it to them
as an entity message (0x20) to the vehicle: the hashed event `0a519c58`
lists the fires burning on it as they are, each time the list changes. After
the hash: one bit, the number of 32-bit words that follow (8 bits), then per
fire three words: two u16 that name it (the second a damage-model node; the
pair is the vehicle's own), a u32 its kind, a u32 that is -1 until the fire
takes. A fire lit by a hit also gets a 33-byte entity message with its two
ids, a u16, the kind, -1, the hit (as in 0xF0E9) and the point where it burns
in the vehicle's frame (three floats; x forward, y up, z left).

Rows: `fire_on` when a fire appears in the list, `fire_off` when it is gone,
at the vehicle, with `fireId` (`first:node`), `fireKind` and, for the fires a
hit lit, `fireLocalX/Y/Z` (forward, up, right). Once a vehicle is dead its
list is often not sent again: its fires end with its wreck (the track's last
sample), else with its entity, else with the replay (`selfCheck.fires`:
`endedWithWreck`, `endedWithEntity`, `burningAtEnd`, `burnedAfterDeath`).

Checked on the tank server replay (102 lists, all read; 34 fires, 21 with a
point) and the naval battle (198 lists; 54 fires, 50 with a point):
extinguishers agree: each of the three times a tank's `extinguisher_ecs`
count fell (2 to 1, 2 to 1, 1 to 0), a fire left its list within 0.05 s of
the extinguisher's own event (`ca468bcc`, the extinguishers left one fewer).
Of the 15 points whose lighting hit has a point on the hull, 12 lie on the
same side of the vehicle as that hit when z is read as left, like the hit's. The kinds are
numbers (on tanks 26, 27 and 1 the most; on ships 4 and 12); what they name
is not known, nor which part a node is. Aircraft send no such list: an
aircraft on fire is not read.

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
