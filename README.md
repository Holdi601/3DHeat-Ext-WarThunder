# 3DHeat War Thunder replay converter

War Thunder replays (`.wrpl`) into the table the 3DHeat viewer opens: every
aircraft's track, the kills and hits where they happened, and who was who
where the replay says so. A match document beside it holds the battle, the
players' results, every kill and the chat.

```bash
pip install -e .                        # installs the `heat3d-wt-replay` command
heat3d-wt-replay "<War Thunder>/Replays" -o out
heat3d-wt-replay a.wrpl b.wrpl -o out   # files, folders, or both
python -m heat3d_ext_warthunder ...     # the same, without installing
```

Each battle becomes `out/<map>/<map>_<start, UTC>_<session id>.parquet` and
`.match.json`. A server replay's parts (`0000.wrpl`, `0001.wrpl`, ...) are read
together as one battle; a client replay and the server's parts of the same
battle are two recordings and stay two. The command prints `ok <table> <summary>`
or `failed <file>: <why>` per battle and exits 1 when any failed.

## Why it is apart

The `.wrpl` format is undocumented, and Gaijin's EULA (3.2.2, 3.2.9) forbids
reverse engineering the game and mining data not meant to be shown; nothing
there names replays, which the game itself shows the player. The user decided
to read them. So that a licence question or a takedown touches only this
converter, it lives outside the 3DHeat Watcher: the watcher runs this command
on new replays when it is installed, imports nothing of it, and works without
it.

## Switching replays on

War Thunder saves client replays to `<War Thunder>/Replays/*.wrpl` when replay
saving is on in the game's options. A server replay of every battle can be
downloaded from warthunder.com's replay pages; that needs a signed-in account,
and nothing here downloads it.

## The table

One row per sample or event; in the footer, under `heat3d`, the viewer's
reading instructions, so the viewer needs no form filled in.

| Column | What |
|---|---|
| `time` | seconds on the replay's own clock |
| `event` | `position`, `wreck` (the unit after its death: the game keeps sending the falling wreck), `kill` (at the killer), `death` (at the victim), `hit_critical` / `hit_severe` (at the unit hit) |
| `x`, `y`, `z` | the game's metres: x east, y up, z north (the hints mirror z, so north is not drawn south) |
| `player` | the player's name, or `uid <n>` when the replay never names the unit |
| `userId`, `team` | the player's Gaijin id and team (`1`, `2`) |
| `life` | `uid#n`: one unit's track, cut where it jumps kilometres (a respawn, or the uid given to a new unit) or is long unseen |
| `uid`, `kind` | the unit's id in the replay; `aircraft` or `ground` |
| `Vehicle` | the game's vehicle id (`f_15a`, `germ_flakpanzer_gepard`), which the viewer's figures match |
| `dirX`, `dirY`, `dirZ` | where an aircraft points, from its attitude (the look vector) |
| `heading`, `pitch`, `roll` | the same in degrees; heading is the compass, clockwise from north |
| `other`, `weapon` | for kills: the other side and the weapon; for hits: who hit, and their vehicle |

The match document (`format: heat3d-wt-replay-match`) has the map, mission,
battle class, session id, start time, the replay's author, every player's
results line (kills, ground kills, deaths, assists, score, captures, vehicles,
and the uids they drove), every kill with names, every hit, the chat, and
`counts` (units, samples, samples per second, packets read and not read) and
`selfCheck` (how many kill-named vehicles appear in that player's own vehicle
list, and how many do not).

## What is read, and how well it is known

Checked on real files means the three public sample replays of
github.com/llama-for3ver/wt_replay_decoder (`tests/replays`, 2025, game
versions 101286 and 101301): a client replay of an air battle, a client replay
of a mixed ground battle, and one part of a server replay. No replay of this
machine's was available.

| Part | Status |
|---|---|
| Header, map, mission, start time, session | read on all three samples |
| Packet stream (zlib in 2025, zstd in 2026) | zlib read on all three samples (every packet framed); zstd only on built replays |
| Results: players, teams, vehicles, kills, deaths, score | read on all three samples (32, 19 and 2 players) |
| Player slots (pid to name and team) | read on the client samples (32 and 18 slots) |
| Kills, critical hits, severe damage | read on all three samples (42, 29, 1 kills); in the air battle 11 of 11 vehicles a kill or hit names are in that player's own vehicle list |
| Chat | read on all three samples (19, 11, 3 lines) |
| Aircraft positions, 2025 layout | the air battle: 30 aircraft uids, 38,982 samples, 3.9 per second, 34 of 2,261 packets not read; the attitude checked against the direction of travel (median 5.9 degrees off) and the climb (3.3 degrees) |
| Aircraft positions, 2026 layout | built to WTACRP's description of version 101404 (October 2026) and tested on built packets only. **Unverified on a real file.** The layout a file uses is chosen by which one its packets parse with |
| Aircraft positions, version 101286 and server replays | not read: their flight packets have a different layout (the mixed battle gives no aircraft; the server part 44 samples) |
| Ground unit positions (0xF073 / 0xF074) | built to WTACRP's description of 2026 replays, tested on built packets. **Unverified on a real file.** The 2025 samples use an older form (states not compressed) that is not read, so they give no ground tracks |
| Who drove which unit | from the replay's own records only: a kill or hit names the uid, slot and vehicle of who dealt it, and a kill its victim's uid and slot. In the air battle 20 of 41 lives are named; units that never dealt or took a named kill or hit stay `uid <n>`, AI units always do |
| Captures, zones, missiles, bombs, ECS entities, the replay's own camera | not read |

Client replays show distant aircraft flying straight on between updates and
then corrected by a few hundred metres; those steps are in the tracks as the
replay has them.

## What is needed to check the rest

Replays from the current game version, from this machine: turn on saving
replays in War Thunder's options, play one ground battle (realistic or
arcade, with some aircraft about) and one air battle, then run
`heat3d-wt-replay "<War Thunder>/Replays" -o out` and look at each match
document's `counts`, `flightLayout` and `selfCheck`. A server replay of the
same battle, downloaded by hand from warthunder.com, shows whether server
replays hold everyone's movements.

## Sources

All code here is written for it; no code was copied from another parser. What
it knows of the format comes from:

- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/QUICK-REF.md`, and its own parser `web/wrpl-parse.js`, read for the bit
  layouts of the flight model, ground sync, id-field messages, player slots and
  the binary blk. WTACRP names maxsupermanhd/wrpl-inspector and wt_blk (both
  AGPL-3.0) as its own references; their code was not read here.
- SMOKE-19/WarThunderReplayDownloader's README: how server replays are fetched.
- The sample replays above, as files: the 2025 differences (the flight model's
  older layout, chat without a flag byte, zlib) were worked out on them here.

## Tests

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # also checks the real 2025 air battle
```

The tests build replays in code (`tests/synth.py`) to the layout the reader
documents; no replay is in the repository.

## Licence

MIT - see [`LICENSE`](LICENSE). Uses pyarrow (Apache-2.0), numpy (BSD-3-Clause)
and zstandard (BSD-3-Clause).
