---
title: Converting replays
nav_order: 4
---

# Converting replays

Output: one `.3dheat` file a battle (the default), or loose files with
`--loose`.

## Step by step

1. **Switch replays on.** War Thunder saves client replays in the `Replays`
   folder of the game when replay saving is on in its options, for example
   `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   A server replay saved from the game's replay page (a zip with `0000.wrpl`,
   `0001.wrpl`, ...) can be converted too.
2. **Open a terminal** in a folder where the results may go
   ([Before you start](before-you-start.md)).
3. **Convert:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # files, folders, or both
   heat3d-wt-replay battle.zip -o out              # a server replay's zip
   heat3d-wt-replay a.wrpl -o out --loose          # separate files instead of one .3dheat
   ```

   `out` is made in the folder your terminal is in.
4. **Read what it says.** You should see one line per battle.
5. **Open it:** load `out/<map>/<match>.3dheat` in the 3DHeat viewer
   ([Loading one](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![A run on a synthetic replay: one .3dheat, --loose, a broken file, an empty folder](assets/img/convert.svg)

The picture is a run on a replay the tests build in code (no real replay,
no install):

- `ok <file>`: a battle converted (with `--loose`: `ok <table> <match document>`);
- `failed <file>: <why>`: a file that could not be read (exit status 1; the
  others are still converted);
- `no .wrpl files given`: nothing to convert (exit status 2);
- `note: ...`: for example that no War Thunder install was found to name the
  vehicles.

## Options

| Option | Default | Does |
|---|---|---|
| `replays` (one or more) | - | `.wrpl` files, folders of them (the folder itself, not its subfolders), or zips of them (a server replay: its `.wrpl` parts are unpacked to a temporary folder) |
| `-o`, `--out` | required | where to write: a folder per map inside |
| `--game FOLDER` | found | the War Thunder folder whose text names vehicles, weapons and ammunition, and whose tables price the [economy](economy.md); also `HEAT3D_WT_GAME` |
| `--no-smoothing` | off | keep other units' dead-reckoned and received samples as the replay has them ([Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | on | pack each battle into one `.3dheat` file |
| `--loose` | off | keep each battle as separate files (table, match document, sidecars) |
| `--version` | - | print `heat3d-wt-replay <version>` and stop |
| `-h`, `--help` | - | print the options and stop |

A battle converted again is written again. The options as the program
prints them: [Command reference](cli-reference.md).

## Which files are one battle

Each battle becomes one file,
`out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat`. AB, RB
and SB are the game's short forms of arcade, realistic and simulator
battles; `<mode>` is the mission's mode as the game keys it (`Conq4`
Conquest #4, `Dom` Domination, `Bttl` Battle; see
[Battle mode](ground.md#battle-mode)); either part is left out where the
replay names none. A server replay's parts (`0000.wrpl`, `0001.wrpl`, ...)
are read together as one battle; a client replay and the server's parts of
the same battle are two recordings and stay two.

## Exit status

`0` when every battle was converted, `1` when any failed (the rest are still
converted), `2` when no replay file was found among the arguments.

---

Part of [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
