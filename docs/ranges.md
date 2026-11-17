---
title: Ranges catalogue
nav_order: 10
---

# Ranges catalogue (heat3d-wt-ranges)

`heat3d-wt-ranges` builds a catalogue from your own installation: how far each
weapon reaches, what each vehicle carries, its sights and its sensors. The
3DHeat viewer uses it for the engagement ranges, view cones and sensor sectors
of a War Thunder battle, in place of its general figures. The file stays on
your machine.

## Step by step

1. Install the converter (see [Installing](installing.md)).
2. Run:

   ```
   heat3d-wt-ranges -o ranges.json
   ```

   or, the same, `heat3d-wt-replay ranges -o ranges.json`. The game is found
   through Steam or the launcher's folders; `--game <folder>` or the
   `HEAT3D_WT_GAME` environment variable say where it is otherwise.
3. Tell the viewer where the file is: in the viewer's `tools/local-data.json`,
   add

   ```json
   "ranges": { "wt": "C:/path/to/ranges.json" }
   ```

   and reload the viewer. The ranges panel then marks these values
   "from your installation".

It takes a minute or two and prints `ok <file> <n> weapons, <n> sensors, <n> units`.
`--quiet` leaves out the progress lines. Exit codes: 0 written, 2 the game
was not found.

## What is in it

| Part | What it holds |
|---|---|
| Weapons | per weapon: its class (machine gun, cannon, gun, missile, bomb, rocket, torpedo), its least, best and most range in metres; for shells their speed and flight distance and the gun's sight range; for missiles the guidance, seeker, lock distance, G limit and launch tables; the names a replay may use for it |
| Units | per ground vehicle, aircraft, helicopter and ship: its weapons, its sensors, and its sights |
| Sights | gunner, commander and driver (aircraft: the gun sight and the targeting pod): widest and narrowest field of view, thermal imager and its generation, night vision, and whether the sight turns with the gun, the turret or the hull |
| Sensors | radars (reach for their reference target size, search sector, modes including ground and sea), infrared search and track, passive receivers, radar warning receivers, missile and laser warners, laser rangefinders |

Where the game states no best range (a machine gun without a sight range, a
bomb), a class value is used and the entry says so in its `detail`. A bomb's
real reach is worked out by the viewer from the height and speed it is
dropped at.

## The file

One JSON file, `version` 1:

- `weapons`: a list of `{ id, cls, name, range: [least, best, most], shape, cone, alt, labels, detail }`
- `sensors`: by id, `{ kind, name, range, az, el, rcsRef, modes, mount, detail }`
- `units`: a list of `{ names, weapons, sensors, optics }`, `names` being the
  vehicle's id and its names in the game's English localisation

Build it again after a game update to follow the game's changes.
