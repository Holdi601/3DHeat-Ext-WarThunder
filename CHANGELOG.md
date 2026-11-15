# Changelog

## Unreleased

- `heat3d-wt-level extract --help`: the object budget's fallback is named
  as it works (a crown or the collision shape, then left out; never a box).
- Documentation: a page for beginners, plain openers, the match document's
  battle keys, a completeness section, generated reference pages, no real
  level names or replay figures; the README is a short overview.

## 0.2.0

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
| Gaijin's terms, sources, tests, licence | [Terms and licence](docs/terms.md) |
| releasing | [Maintaining](docs/maintaining.md) |
