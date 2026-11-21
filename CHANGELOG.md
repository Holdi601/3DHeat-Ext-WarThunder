# Changelog

## 0.2.2

- `heat3d-wt-level layouts`: each level's game-mode layouts from the multiplayer missions of your install, as
  `<level>.layouts.json` beside the level: capture zones, battle areas, excluded ground and spawn kill areas (out
  of bounds), spawn points, airfields, helipads, bases and bombing targets, per mission and difficulty, with
  battle-rating tiers as stages. Docs: [Levels](docs/levels.md#game-mode-layouts).

## 0.2.1

- Server replays of game version 101421 on (November 2026): tank turrets are read one bit later in the ground
  state. Read at the old place, every turret's yaw was unrelated to where its player aimed (a median of 88
  degrees apart), and held to its drive the turrets kept turning. Now they follow the aim as on older replays
  (median under 1.3 degrees on the samples, every hit's shot line within 3 degrees for 99 % of hits or more).
  Older replays are read as before. Files of such replays converted before 0.2.1 need converting again.
- Server replays: `viewYaw` / `viewPitch` for every unit whose player sends a camera (0xF0CC), not only tanks:
  aircraft, helicopters, ships, and a scout's drone. In a targeting camera (mode 21) the camera's own
  direction, which follows what the drone's or pod's camera looks at (within half a degree of the sight point);
  `selfCheck.unitCameras.withDirection` counts them.

## 0.2.0

- Server replays: each player's camera per unit (0xF0CC): `zoom` and `cameraMode` on unit rows (the gunner's
  sight steps, a targeting camera). Aircraft and helicopters: their sensors from each flight entry - `sensors`
  (slots on or off), `sensorModes` (raw), `sensorContacts`, `sensorLocks`, the optical sensor's tracked point
  (`opticX/Y/Z`), the locked target's (`lockX/Y/Z`) and where the sight or pod looks (`sightX/Y/Z`).
- `heat3d-wt-ranges` (also `heat3d-wt-replay ranges`) builds a catalogue from your own installation: each
  weapon's least, best and most range (shells, missiles with their launch tables, bombs, torpedoes), each
  vehicle's weapons, sights (zoom, thermal generation, night vision) and sensors (radars, IRST, warners,
  laser rangefinders), for the viewer's engagement ranges, view cones and sensor sectors.
- Server replays say who won: the team whose tickets are 0 at the end lost (checked against every client
  replay with a status). Every row carries the viewer's outcome columns: `won`, `matchWon`, `round` (1) and
  `roundEndReason` (`destruction`, `capture`, `tickets`, `time`); the match document's `result` adds
  `source` and `endReason`.
- `heat3d-wt-level extract --help`: the object budget's fallback is named
  as it works (a crown or the collision shape, then left out; never a box).
- Documentation: a page for beginners, plain openers, the match document's
  battle keys, a completeness section, generated reference pages, no real
  level names or replay figures; the README is a short overview.

- One `.3dheat` file a battle by default; `--loose` for separate files.
- Who won, where the replay says; Silver Lions and research points per
  event, priced from your install.
- Bombs without flight records fall from their release to their impact.
- Turrets held to their drive and set to each main-gun shot.
- Server replays: every player named, real turrets, game modes,
  objectives, trams; zips read.
- Ammunition, hit outcomes and calibres on shot rows; vehicle fires.
- Hits in the victim's own frame; the recorded camera; clean ends of
  tracks; AB/RB/SB in file names.
- Levels: render meshes, generated forests and towns, land-class colours.
- Installs with one pip line from the release zip, no Git needed; a pip install knows its version and updates itself with pip when a newer release is out.
- README: a quick start for new users.

## 0.1.0

- Every unit's track with vehicle, team and player; weapons in flight;
  kills, hits, destroyed modules and launches where they happened.
- Cockpit instruments, flight entries, player statistics, weapon names; the
  dead-reckoning smoother; each unit held to its own pace.
- Levels from your install (`heat3d-wt-level`).
- Nothing lost: every message and packet not read is kept in a sidecar.

## Docs

Where each feature is documented:

| Feature | Page |
|---|---|
| installing, names from your install, updates | [Installing](docs/installing.md), [Before you start](docs/before-you-start.md) |
| converting, options, `--loose`, messages, exit status | [Converting replays](docs/converting.md), [Command reference](docs/cli-reference.md) |
| `.3dheat` file, file names, coordinates | [Output files](docs/output-files.md) |
| every column | [The table](docs/table.md), [Column list](docs/columns.md) |
| mission, players, units, kills, weapons, scoreboard, results, who won | [The match document](docs/match-document.md) |
| sidecars, counts | [Sidecars and completeness](docs/sidecars.md) |
| levels (`heat3d-wt-level`) | [Levels](docs/levels.md) |
| what is read and how it was checked; track cuts, bombs without flight records | [How it reads a replay](docs/how-it-reads.md) |
| cockpit instruments, flight entries, statistics, smoother, attitude | [Aircraft](docs/aircraft.md) |
| turrets, camera, ends of tracks, battle mode | [Ground units and camera](docs/ground.md) |
| gunfire, hit outcomes, ammunition, vehicle fires | [Hits, gunfire and fires](docs/hits.md) |
| Silver Lions, research points, who won | [Economy](docs/economy.md) |
| capture zones, airfields, spawns, trams | [Objectives](docs/objectives.md) |
| what it reads, sources, tests, licence | [Terms and licence](docs/terms.md) |
| releasing | [Maintaining](docs/maintaining.md) |
