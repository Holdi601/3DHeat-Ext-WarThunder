---
title: Installing
nav_order: 2
---

# Installing

Needs Python 3.10 or later; pyarrow, numpy, zstandard and Pillow are
installed with it.

## Step by step

1. Get the code: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git` (or a release zip from
   [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases), unpacked).
2. In that folder: `pip install -e .`. This installs two commands,
   `heat3d-wt-replay` (replays) and `heat3d-wt-level` (levels).
3. Check it: `heat3d-wt-replay --version`, and `--help` for the options:

![heat3d-wt-replay --help](assets/img/help.svg)

Without installing: `python -m heat3d_ext_warthunder ...` and
`python -m heat3d_ext_warthunder.levelcli ...` in the repository folder.

## Names from your install

Vehicles, weapons and ammunition get their English names from the game's own
localisation, read from your install when converting. The install is found
through Steam or the launcher's default folders; `--game <folder>` or the
environment variable `HEAT3D_WT_GAME` say where it is otherwise. Nothing of
the game's text is in this repository; without an install the names are the
vehicle ids (the converter says so in a `note:` line).

## Updates

Every start first checks the project's GitHub releases (one request at most
every few hours, cached; it never stops a conversion, offline or not). When a
newer release is out, the command asks before installing it: a `git clone` is
updated with `git pull --ff-only` (refused while you have local changes), a
downloaded copy from the release's source archive. `HEAT3D_NO_UPDATE=1`
switches the check and the update off. Code: `heat3d_update`
(`startup("heat3d_ext_warthunder")`).

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
