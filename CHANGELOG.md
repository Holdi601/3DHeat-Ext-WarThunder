# Changelog

## 0.6.0

- Levels of game builds 2.61 and later: their land is read from the rendered land mesh (the finest LOD of every
  cell), as the levels no longer carry the land ray tracer the extractor read until now. Air maps, naval maps
  and the older ground maps without a heightmap failed with "no heightmap and no land mesh"; they extract again,
  and the heightmap's surroundings out to tens of kilometres are back on the others.
- Maps: only the levels a multiplayer mission is played on (from the install's missions). Hangar scenes, the test
  drive and test flight ranges, tutorial and unused levels are no longer listed as new maps.
- Content beside the maps (`status` / `extract --content`, where the tool's kit has them): the catalogue
  (`catalog.json`: vehicles, soldier squads, weapons, rounds, soldier equipment such as drones, grenades, launchers
  and supply boxes, and modifications such as scopes, vests, belts and upgrades) and the ranges catalogue
  (`ranges.json`). `status` reports the install's items that the catalogue does not have yet, by kind.
- `plugin.json`: the manifest 3DHeat's Games page reads to know what this tool does, which games it is
  for and how to call it. The release archive carries it and the tool's icon (`icon-64.png`) beside the
  program.
- The shared app (3DHeat extractor kit) with new-content detection: `status --json` reports content
  entries and the install's new items beside the maps, and `check-new [--json] [--auto-extract]` is the
  unattended check that skips the game while it runs or updates and extracts only what is new (never
  replaces files).
- Outputs made before the extract record (`.heat3d-extract.json`) existed are no longer all called
  outdated: when every output is newer than the game files it was made from it counts as current
  (`"untracked": true` in `status --json`), otherwise outdated.
- Matches converted by 0.5.0 stay current (`currentFrom` in `plugin.json`): this release does not
  change the converted output, so 3DHeat does not convert them again.

## 0.5.0

- Aircraft and ship hits get their ammunition (the killing round, missile, bomb or torpedo by name, the calibre of
  the others, the belt an aircraft's gun fired) and the modules each hit destroyed; replays of game version 101404
  name the parts they hit.
- An aircraft's weapons are read from its flight model's weapon slots, a ship's from its unit file: a kill names
  its round (`ap_i_ball_M8`, `frag_i_t`) or its missile, bomb or torpedo (`su_r_77_1`, `de_sc500`), which names
  the killing hit; other hits get a calibre from their signature among the unit's guns, from its guns that fire
  bursting rounds (a burst hit when the unit launched nothing in the two minutes before) or from its one calibre
  of guns. `ammoBelt`: the belt (`default`, `50cal_universal` ...) where the rounds the shooter's kills name are
  in one belt only. See [Ammunition](docs/hits.md#ammunition).
- The modules a hit destroyed (0xF118) go on the hit: `destroyedParts`. A unit that gets no lists of damaged
  parts (aircraft) has them as its `damagedParts`, `damagedGroups`, `crewDamaged` too (`damagedFrom`
  `destroyed`); new part groups `airframe`, `controls`, `rotor`, `gear` for aircraft parts.
- Older game versions' part numbering: replays of game 101404 number the game's parts lower than today's install
  (names were put in between since). Such a replay is now named by a kept copy of that version's
  `aces.vromfs.bin` where this machine has one (the converter keeps one per game version in
  `~/.cache/heat3d-wt/archives`, `HEAT3D_WT_ARCHIVES`), else by the table of where the names were put in; the
  fires tell which fits (`selfCheck.damageParts.gameNumbering`: `named`, `numbering`, `tried`). `hitPartNumber`
  is the struck part's place in your install's list.
- Files converted before 0.5.0 need converting again for these columns.


## 0.4.0

- Its own icon: the 3DHeat cube with a text badge for its game (letters in 3DHeat's colours), as the
  program, window, taskbar and docs icon.
- A new window: the 3DHeat look in dark and light (follows the system, switchable), the logo and
  icon, sharp at any display scaling. Four steps: find the game (each requirement with its fix),
  choose (maps ticked when there is something to do, filters, search; jobs with their fields
  inline), work (progress, time left, cancel), done (open in 3DHeat, open the output folder, and
  for a failure what went wrong and what to do, copy details, report a problem).
- No console window on Windows: the program is a window program. From a terminal it still prints
  as before; `heat3d-warthunder-cli.cmd` beside it waits for it in a terminal and passes its exit code.
- The update offer in the same look: Update now / Later / Skip this version, and "Update
  automatically" from the dialog.
- CI draws every page and dialog of the window (on Linux under a virtual display) and checks the
  Windows build is a window program.
- `heat3d-warthunder convert <replay>... -o <out> [--progress-json]` and `heat3d-warthunder info <replay> --json` (what the
  replay says about its match, read from its header without converting it), the same verbs in every
  3DHeat replay reader; the old command lines work as before.
## 0.3.1

- Hits are keyed: `hitKey` (`shooter:kind:number`) names a hit in every message about it. See
  [Hits](docs/hits.md#hit-keys).
- The projectile at the hit, for hits that went into the vehicle: `shellSpeed` (m/s, recorded), `shellPointX/Y/Z`
  and `shellDirX/Y/Z` (world), `shellLocalX/Y/Z` and `shellLocalDirX/Y/Z` (the vehicle's frame), `shellValue` (raw).
- What came after a hit: `after_hit` rows (`afterHitMessage`, `afterHitFlags`, `afterHitValue`, `afterHitCount`),
  kept as sent; the first is also on the shot row.
- The parts each hit damaged: `damagedPartIds`, `damagedParts` (crew members, ammunition racks, engine, breech,
  tracks ...), `damagedGroups`, `crewDamaged`, `ammoDamaged`; a list without a hit is a `parts_damaged` row. The
  names come from the vehicle's unit file and damage model in your install, read while converting. Fires get
  `firePart` and `fireNode`, destroyed modules `partName` and `partGroup`, hits `hitPartName`. The game's names
  (`hitPartName`, `fireNode`, `partName`) are written only where the replay's fires show it numbers the parts as
  the install does (an older game version does not; `selfCheck.damageParts.gameNumbering`).
- Ammunition: `ammoSource` (`recorded`, `slot`, `speed`, `slot-speed`, `candidate`, `speed-calibre`, `calibre`,
  `default`) and `ammoConfidence` say where `ammoName`, `ammoType` and `calibre` come from. The killing hit is named
  by its kill even without a loaded slot; a hit's recorded speed picks the one shell of the weapon that fits it
  (`ammoSpeedError`), and names its slot when its slot's hits agree; a weapon with one shell of what the hit did
  names it. Machine-gun belts' rounds are listed by type.
- The ranges catalogue lists every shell of a weapon, its modifications' too, with its static data: mass, calibres,
  drag, explosive, presets, armour power table, de Marre coefficients.
- Files converted before 0.3.1 need converting again for these columns.

## 0.3.0

- A standalone program for Windows, Linux and macOS (no Python needed), built by CI with a `SHA256SUMS` file.
  Without arguments it opens a window: what is found and what is missing (install, Oodle library, disk space),
  the levels folder, the levels as new / changed by a game update / extracted by an older version / up to date,
  extraction of the picked ones one at a time, replay conversion, and updates.
- Each extracted level is recorded in `<levels>/warthunder/.heat3d-extract.json` (extractor version, game build,
  size and SHA-256 of its game file), so new levels from a game update are found and only those extracted:
  `status --json`, `extract --new` / `--changed` / `--outdated` / `<level>...`, `--progress-json`.
- Updates ask first (update now / later / skip this version) unless automatic updates were chosen
  (`--auto-update`, the window's checkbox, or `HEAT3D_AUTO_UPDATE=1`).
- The install is also found in Steam libraries on Linux (native, flatpak, Steam Deck) and macOS, and in the
  launcher's folders there; a native Oodle library from such an install is used for levels.

## 0.2.6

- 0.2.5 stopped a conversion when a level file was there but could not be decoded (no Oodle library, as on
  Linux). A level that cannot be read is now skipped, and the packed heights' offset comes from the replay alone.
- A level's heightmap is decoded once and kept (16-bit steps over the level's height range) in the folder
  `HEAT3D_WT_HEIGHTS` names, by default `~/.cache/heat3d-wt/heights`, named by the level and its file size. Kept
  heightmaps are read without decoding, so a machine without the Oodle library can use those decoded elsewhere.

## 0.2.5

- Ground units' packed heights: the offset that places them (a level whose packed heights count from its water
  level, by 7, -10, 25, -100 or -1,493 m, for example) is now measured against the level's heightmap from your
  install: the median of the ground height less the packed height over the battle's packed ground samples, taken
  when at least half of them agree with it within 1 m. On 15 server battles of 9 levels the packed samples lie on
  the heightmap within 0.1 m (10th to 90th percentile) once it is added. Only the heightmap's block of the level
  file is read.
- Without the level (or when its heightmap does not agree), the offset from units seen both as floats and packed
  is taken only when at least five such pairs agree within 2 m. Before, three pairs were enough whatever their
  spread, so a battle could be placed several metres above or below the ground, or left 1,493 m off where too few
  pairs were seen.
- `selfCheck.packedGroundHeight` says how the offset was found (`method`: `heightmap`, `pairs` or `none`) and holds
  the heightmap's measurement (`heightmap`: samples, median, share that agrees).
- Files converted before 0.2.5 may need converting again for their ground units' heights.

## 0.2.4

- Server replays of game versions before 101421 (before about 11 November 2026): a ground unit's hit point is a
  16-bit fraction of 20 m there, not 50 m. 0.2.3 read every replay at 50 m, so on these older replays the points
  lay 2.5 times too far from the vehicle's origin. The range now follows the replay's game version: 20 m before
  101421, 50 m from 101421 on. Replays of 101421 and later convert as in 0.2.3.
- Files of replays before game version 101421 converted with 0.2.3 need converting again for their hit points.

## 0.2.3

- Server replays: hits on a damage-model part with a one-byte number (parts 0-63, about one hit in ten, most of them
  hull front, side and top plates) had their hit point read one byte late, so `hitLocalX/Y/Z`, `targetX/Y/Z`
  and the shot direction of those hits were wrong. The part is now read as one or two bytes and the point after
  it. `hitPart` holds the part as sent: one byte for those hits, so `hitFlag` is 0 there. See
  [Gunfire](docs/hits.md#gunfire).
- Server replays: a ground unit's hit point is a 16-bit fraction of 50 m, not 20 m (a step of 1.5 mm). Read at
  20 m, the points lay 2.5 times too close to the vehicle's origin. Checked against the vehicles' own damage-model
  parts, which each hit names: on six sample ground battles the points now lie on the surface of the part hit
  (median distance 1 mm). Within 0.5 m of the part hit: one-byte hits 0 % before, 99.8 % now; two-byte hits 6 %
  before, 67 % now. Ground hits kept in the vehicle's frame are still those within 6 m of its origin.
- Files converted before 0.2.3 need converting again for their hit points.

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
