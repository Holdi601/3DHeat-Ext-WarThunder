---
title: Sidecars
nav_order: 7
---

# Sidecars

Next to each table, so that nothing of the replay is lost to it:

- `<match>.messages.parquet`: every message to a unit (time, message id and
  name, uid, eid, template, vehicle, its id fields as hex, `decoded` (what is
  read of it, as JSON), the payload), every replicated component value
  (packet 6, `name` the component, `fields` its value), every entity message
  (with its entity and class number), every replicated object of 0xF02D and
  0xF0AA (`ReflectionData <kind>/<index>`, its fields as hex) and every
  packet no reader here takes, whole.
- `<match>.objectives.parquet`: the capture zones over time, one row per change the server sent: `time`,
  `event` (`state`, `progress`, `captured`, `neutralised`), `zone` (its letter), `zoneId`, `object`, `owner`
  (0 none, 1, 2), `progress` (-100..100, positive towards team 2), the zone's `x`, `y`, `z`, and all `fields`
  of the object as hex (see [Objectives](objectives.md)).
- `<match>.flight.parquet`: every flight-model entry of every aircraft whole
  (its bits, and `phase`: the bit of its first byte it started at), with its
  velocity, the 14 nibbles after it (`control1-3`, `throttle`), its engines
  with their state, afterburner and condition, and its rounds per weapon
  (`ammo`; `numbers` is the whole list). Other aircraft's values are as last
  refreshed.

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
