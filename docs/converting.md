---
title: Converting replays
nav_order: 3
---

# Converting replays

## Step by step

### 1. Switch replays on

War Thunder saves client replays to `<War Thunder>/Replays/*.wrpl` when replay
saving is on in the game's options. A server replay of every battle can be
downloaded from warthunder.com's replay pages; that needs a signed-in account,
and nothing here downloads it.

### 2. Convert

```bash
heat3d-wt-replay "<War Thunder>/Replays" -o out
heat3d-wt-replay a.wrpl b.wrpl -o out        # files, folders, or both
heat3d-wt-replay battle.zip -o out           # a server replay's zip as downloaded
heat3d-wt-replay ... --game "D:/Games/War Thunder"   # where the install is, if not found
heat3d-wt-replay ... --no-smoothing          # other units' tracks exactly as the replay has them
heat3d-wt-replay ... --loose                 # separate files instead of one .3dheat
```

### 3. Read what it says

One line per battle: `ok <file>` (with `--loose`: `ok <table> <match document>`)
or `failed <file>: <why>`.

![A run on a synthetic replay, as one .3dheat and with --loose](assets/img/convert.svg)

The picture is a run on a replay built in code by the tests (no real replay
and no install, hence the `note:`).

### 4. Open it

Load `out/<map>/<match>.3dheat` in the 3DHeat viewer; see
[Loading one](https://holdi601.github.io/3DHeat/container.html#loading-one) in the viewer's documentation.

## Options

| Option | Default | Does |
|---|---|---|
| `replays` (one or more) | - | `.wrpl` files, folders of them (the folder itself, not below it), or zips of them (a server replay as downloaded: its `.wrpl` parts are unpacked to a temporary folder) |
| `-o`, `--out` | required | where to write: a folder per map inside |
| `--game FOLDER` | found | the War Thunder folder whose localisation names vehicles, weapons and ammunition, and whose tables price the economy; also `HEAT3D_WT_GAME` |
| `--no-smoothing` | off | keep other units' dead-reckoned and received samples where the replay has them (the client's dead reckoning is still marked; see [Aircraft](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | on | pack each battle into one `.3dheat` file |
| `--loose` | off | keep each battle as separate files (table, match document, sidecars) |
| `--version` | - | print the version and exit |
| `-h`, `--help` | - | print the options and exit |

A battle converted again is written again.

## Which files are one battle

Each battle becomes one file, `out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat`, holding
the table `.parquet`, the `.match.json` and the three sidecars named alike ([One file a match](https://holdi601.github.io/3DHeat/container.html));
with `--loose` they are written as those separate files: AB, RB and SB are the game's own short forms of arcade,
realistic and simulator battles, `<mode>` the mission's mode as the game keys it (`Conq4` Conquest #4, `Dom`
Domination, `Bttl` Battle; see [Battle mode](ground.md#battle-mode)); either part is left out where the header
names none. A server replay's parts (`0000.wrpl`, `0001.wrpl`, ...) are read
together as one battle; a client replay and the server's parts of the same
battle are two recordings and stay two. The command prints `ok <file>` (with `--loose`, `ok <table> <summary>`)
or `failed <file>: <why>` per battle, and exits 1 when any failed, 2 when no replay was given.
Every start first checks the project's GitHub releases for a newer version and asks before installing it;
`HEAT3D_NO_UPDATE=1` switches that off.

## Exit status

`0` when every battle was converted, `1` when any failed (the rest are still
converted), `2` when no replay was given.

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
