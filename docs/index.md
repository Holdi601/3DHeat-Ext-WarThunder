---
title: Home
nav_order: 1
---

# 3DHeat War Thunder replays

**What is it?** War Thunder can record a battle as a replay file. This tool
turns the recording into a file you can watch from above in the
[3DHeat viewer](https://holdi601.github.io/3DHeat/), with every plane, tank
and ship, every missile and bomb, and every hit where it happened. A second
command turns the levels of your own game install into 3D levels to show the
battles on.

**Why would I use it?** For a debrief of a battle in 3D; for heatmaps of
where you and others fly, drive, fight and die over many battles; to see
where hits landed on a vehicle; to see what a battle cost and earned. The
output is plain Parquet and JSON, so other tools can read it too.

**Example:** one `.wrpl` replay in, one `<match>.3dheat` file out:

![From a replay to the 3DHeat viewer](assets/img/pipeline.svg)

## Quick start

You need Windows, Python 3.10 or later ("Add python.exe to PATH" ticked in its
installer), War Thunder installed and replay saving switched on in the game's
options (your battles then land as `.wrpl` files in its `Replays` folder); no Git.
New to the command line? Read [Before you start](before-you-start.md) first.

```bash
python -m pip install https://github.com/Holdi601/3DHeat-Ext-WarThunder/archive/refs/tags/v0.2.6.zip
heat3d-wt-replay "C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays" -o out
heat3d-wt-level list                              # the levels of your install
heat3d-wt-level extract <level> -o levels         # one level as a 3D model
```

The game's folder is found by itself; `--game "<folder>"` names it otherwise.
You should see one line per battle: `ok out/<map>/<match>.3dheat`. A level
lands in `levels\<level>\<level>.glb` (up to about 250 MB with `--detail high`).

Then open the files in the [3DHeat viewer](https://github.com/Holdi601/3DHeat#quick-start):
download it (**Code -> Download ZIP**, unpack), double-click `start.bat` (it
offers to install Node.js when it is missing and opens `http://127.0.0.1:5273`),
then **Source -> Files...** and pick the `.3dheat` (or drop it on the Source
panel) for the Heatmap tab; for the battle itself, the **Match** tab's
**Load match files...** and the same `.3dheat`
([loading one](https://holdi601.github.io/3DHeat/container.html#loading-one)).
For the level, **Background / level -> 3D model...** and pick the `.glb`.
Everything stays on your machine.

When a new release is out, the tool says so when it starts and offers to
update itself.

## This documentation

| Page | What it covers |
|---|---|
| [Before you start](before-you-start.md) | Python, a terminal, and what success looks like |
| [Installing](installing.md) | install, names from your install, updates |
| [Converting replays](converting.md) | `heat3d-wt-replay` step by step, every option, messages |
| [Output files](output-files.md) | the `.3dheat` file, `--loose` files, names |
| [The table](table.md) | every column and event |
| [The match document](match-document.md) | every key of `<match>.match.json` |
| [Sidecars and completeness](sidecars.md) | what is kept whole besides the table, and the counts |
| [Levels](levels.md) | `heat3d-wt-level`: levels from your install as `.glb` |
| [Ranges catalogue](ranges.md) | `heat3d-wt-ranges`: weapons' reach, sights and sensors from your install |
| [How it reads a replay](how-it-reads.md) | what is read, and how it was checked |
| [Aircraft](aircraft.md), [Ground units and camera](ground.md), [Hits, gunfire and fires](hits.md) | the details behind the columns |
| [Economy](economy.md), [Objectives](objectives.md) | Silver Lions and research points; capture zones, airfields |
| [Terms and licence](terms.md) | what it reads, sources, tests, licence |
| [Command reference](cli-reference.md), [Column list](columns.md) | generated from the code |

## Part of 3DHeat

This converter is one of the tools of [3DHeat](https://github.com/Holdi601/3DHeat),
a realtime 3D telemetry and replay viewer ([documentation](https://holdi601.github.io/3DHeat/)).
The viewer opens the `.3dheat` file: the table in its Heatmap tab, the match
document in its Match tab ([One file a match](https://holdi601.github.io/3DHeat/container.html)).
What every converter must keep: [Converters keep everything](https://holdi601.github.io/3DHeat/converters.html).

Each game reader is its own small project with its own licence file, releases and issue
tracker, so it can be installed, updated, maintained - or withdrawn on a rights holder's
request - on its own, without affecting the viewer or the other tools.
The 3DHeat Watcher runs this converter on new replays when it is installed,
and works without it.

| Tool | What it does | Source | Documentation |
|---|---|---|---|
| 3DHeat viewer | shows the data in 3D: heatmaps, replays, race analysis | [3DHeat](https://github.com/Holdi601/3DHeat) | [site](https://holdi601.github.io/3DHeat/) |
| GameFiles | courses and levels out of the files games ship | [3DHeat-GameFiles](https://github.com/Holdi601/3DHeat-GameFiles) | [site](https://holdi601.github.io/3DHeat-GameFiles/) |
| GameCapture | lap telemetry, and levels rebuilt from gameplay video | [3DHeat-GameCapture](https://github.com/Holdi601/3DHeat-GameCapture) | [site](https://holdi601.github.io/3DHeat-GameCapture/) |
| Unreal Exporter | an Unreal Editor plugin that exports a level | [3DHeat-UnrealExporter](https://github.com/Holdi601/3DHeat-UnrealExporter) | [site](https://holdi601.github.io/3DHeat-UnrealExporter/) |
| CS2 | Counter-Strike 2 demos and maps | [3DHeat-CS2](https://github.com/Holdi601/3DHeat-CS2) | [site](https://holdi601.github.io/3DHeat-CS2/) |
| Watcher | records what games publish while you play | [3DHeat-Watcher](https://github.com/Holdi601/3DHeat-Watcher) | [site](https://holdi601.github.io/3DHeat-Watcher/) |
| War Thunder replays | `.wrpl` replays and War Thunder levels | [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder) | [site](https://holdi601.github.io/3DHeat-Ext-WarThunder/) |
| World of Tanks replays | `.wotreplay` replays | [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT) | [site](https://holdi601.github.io/3DHeat-Ext-WoT/) |
| World of Warships replays | `.wowsreplay` replays | [3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs) | [site](https://holdi601.github.io/3DHeat-Ext-WoWs/) |
| Squad demos | Squad server demos | [3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad) | [site](https://holdi601.github.io/3DHeat-Ext-Squad/) |
| DCS maps | DCS World maps as 3D levels | [3DHeat-Ext-DCS](https://github.com/Holdi601/3DHeat-Ext-DCS) | [site](https://holdi601.github.io/3DHeat-Ext-DCS/) |
| IL-2 maps | IL-2 Great Battles maps as 3D levels | [3DHeat-Ext-IL2](https://github.com/Holdi601/3DHeat-Ext-IL2) | [site](https://holdi601.github.io/3DHeat-Ext-IL2/) |
| Dota 2 map | the Dota 2 map from your own install as a 3D level | [3DHeat-Ext-Dota](https://github.com/Holdi601/3DHeat-Ext-Dota) | [site](https://holdi601.github.io/3DHeat-Ext-Dota/) |
| Dota 2 replays | Dota 2 replays | [3DHeat-Ext-DotaReplay](https://github.com/Holdi601/3DHeat-Ext-DotaReplay) | [site](https://holdi601.github.io/3DHeat-Ext-DotaReplay/) |
| Riot replays | League of Legends and VALORANT replays (what they carry unencrypted) | [3DHeat-Ext-Riot](https://github.com/Holdi601/3DHeat-Ext-Riot) | [site](https://holdi601.github.io/3DHeat-Ext-Riot/) |
| Forza maps | Forza courses, races and cars from your own install | [3DHeat-Ext-Forza](https://github.com/Holdi601/3DHeat-Ext-Forza) | [site](https://holdi601.github.io/3DHeat-Ext-Forza/) |
| Battlefield maps | Battlefield levels (Frostbite) as 3D levels | [3DHeat-Ext-Battlefield](https://github.com/Holdi601/3DHeat-Ext-Battlefield) | [site](https://holdi601.github.io/3DHeat-Ext-Battlefield/) |
| BeamNG maps | BeamNG.drive courses | [3DHeat-Ext-BeamNG](https://github.com/Holdi601/3DHeat-Ext-BeamNG) | [site](https://holdi601.github.io/3DHeat-Ext-BeamNG/) |
| AC Rally maps | Assetto Corsa Rally stages as courses | [3DHeat-Ext-ACRally](https://github.com/Holdi601/3DHeat-Ext-ACRally) | [site](https://holdi601.github.io/3DHeat-Ext-ACRally/) |
| Reforger maps | Arma Reforger worlds (Enfusion) as 3D levels | [3DHeat-Ext-Reforger](https://github.com/Holdi601/3DHeat-Ext-Reforger) | [site](https://holdi601.github.io/3DHeat-Ext-Reforger/) |
| R6 replays | Rainbow Six Siege match replays | [3DHeat-Ext-R6](https://github.com/Holdi601/3DHeat-Ext-R6) | [site](https://holdi601.github.io/3DHeat-Ext-R6/) |

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
