---
title: Sidecars and completeness
nav_order: 8
---

# Sidecars and completeness

Nothing in a replay is thrown away. What the converter reads goes into the
table and the match document; everything else is kept whole in three
sidecar files next to the table (inside the `.3dheat` file, or loose with
`--loose`). This is the rule all 3DHeat converters share:
[Converters keep everything](https://holdi601.github.io/3DHeat/converters.html).

## The sidecars

- `<match>.messages.parquet`: every message to a unit (time, message id and
  name, uid, eid, template, vehicle, its id fields as hex, `decoded` (what
  is read of it, as JSON), the payload), every replicated component value
  (`name` the component, `fields` its value), every entity message (with its
  entity and class number), every replicated object (`ReflectionData
  <kind>/<index>`, its fields as hex) and every packet no reader here takes,
  whole.
- `<match>.objectives.parquet`: the capture zones over time, one row per
  change the server sent: `time`, `event` (`state`, `progress`, `captured`,
  `neutralised`), `zone` (its letter), `zoneId`, `object`, `owner` (0 none,
  1, 2), `progress` (-100..100, positive towards team 2), the zone's `x`,
  `y`, `z`, and all `fields` of the object as hex (see
  [Objectives](objectives.md)).
- `<match>.flight.parquet`: every flight-model entry of every aircraft whole
  (its bits, and `phase`: the bit of its first byte it started at), with its
  velocity, the 14 control nibbles (`control1-3`, `throttle`), its engines
  with their state, afterburner and condition, and its rounds per weapon
  (`ammo`; `numbers` is the whole list). Other aircraft's values are as last
  refreshed.

## What the counts guarantee

The match document's `counts` say what the replay held and what became of
it:

| Key | What |
|---|---|
| `packets`, `unreadPackets` | every packet type met, and those no reader takes (kept whole in the messages sidecar) |
| `messageIds`, `messageIdsNotRead` | every message id met and how often, and those only kept, not read |
| `replicatedComponents`, `replicatedNotRead` | component values read, and those only kept |
| `entities`, `entityTemplates`, `entityMessages` | what the entity stream created and sent |
| `droppedSamples` | samples left out on purpose (a ground unit's wreck after its entity is gone), by reason |

Nothing else is left out: an item of the replay is either read into the
table or the match document, or kept whole in a sidecar. The match
document's `selfCheck` holds the checks of what was read
([How it reads a replay](how-it-reads.md)).

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
