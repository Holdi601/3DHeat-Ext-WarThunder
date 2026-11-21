---
title: Installing
nav_order: 3
---

# Installing

New to the command line? Read [Before you start](before-you-start.md) first.

## The standalone program (no Python needed)

Each [release](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases/latest)
has a ready-to-run program for Windows (`heat3d-warthunder-<version>-windows-x64.zip`),
Linux (`...-linux-x64.tar.gz`, also for Steam Deck) and macOS (`...-macos-arm64.tar.gz`),
with a `SHA256SUMS` file to check the download. Unpack it anywhere and start
`heat3d-warthunder` (on macOS the first start may need *Open* from the
right-click menu, as the program is not notarised).

Started without arguments it opens a window that:

- finds your War Thunder install (Steam on any system, the Gaijin launcher's
  folders), or lets you choose its folder;
- says what is missing: the game, the Oodle library levels need (it comes from
  your own install), free disk space;
- lists the game's levels as new, changed by a game update, extracted by an
  older version, or up to date, and extracts the ones you pick, one at a time,
  into the 3DHeat levels folder (`HEAT3D_LEVELS`, by default
  `%LOCALAPPDATA%\3DHeat\levels` on Windows and `~/.local/share/3dheat/levels`
  elsewhere), where the viewer finds them;
- converts a folder of replays;
- checks for updates and asks before installing one, unless you tick
  *Update automatically*.

The same program runs every command below: `heat3d-warthunder heat3d-wt-level list`,
`heat3d-warthunder heat3d-wt-replay <replays> -o <folder>`. For scripts:
`heat3d-warthunder status --json` reports the levels' state,
`heat3d-warthunder extract --new` extracts only the new and
`heat3d-warthunder --check --json` what is found and missing.
The 3DHeat app's Extractors panel installs, updates and starts it for you.

## From the source (Python)

Needs Python 3.10 or later; pyarrow, numpy, zstandard and Pillow are
installed with it.

### Step by step

1. Get the code: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   or download a zip from [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   and unpack it.
2. Open a terminal in that folder and type `pip install -e .`. This installs
   two commands: `heat3d-wt-replay` (replays) and `heat3d-wt-level` (levels).
3. Check it: `heat3d-wt-replay --version`. You should see
   `heat3d-wt-replay 0.2.1`. `heat3d-wt-replay --help` lists the options:

![heat3d-wt-replay --help](assets/img/help.svg)

Without installing: `python -m heat3d_ext_warthunder ...` and
`python -m heat3d_ext_warthunder.levelcli ...` in the tool's folder.

`python -m heat3d_ext_warthunder.standalone_spec` opens the same window from the source.

## Names from your install

Vehicles, weapons and ammunition get their English names from the game's own
text files, read from your install when converting. The install is found
through Steam or the launcher's default folders; `--game <folder>` or the
environment variable `HEAT3D_WT_GAME` say where it is otherwise. Nothing of
the game's text is in this repository; without an install the names are the
vehicle ids (the converter says so in a `note:` line).

## Updates

Every start first checks the project's GitHub releases (at most one request
every few hours; it never stops a conversion, online or not). When a newer
release is out, the command shows its notes and asks: update now, later, or
skip this version. It updates without asking only when you chose that:
`--auto-update` (this run), the window's *Update automatically*, or
`HEAT3D_AUTO_UPDATE=1`. A `git clone` is updated with `git pull --ff-only`
(refused while you have local changes), a pip install with pip, a downloaded
copy from the release's archive, and the standalone program from the
release's file for your system after its SHA-256 matched `SHA256SUMS`.
`HEAT3D_NO_UPDATE=1` switches the check and the update off.

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
