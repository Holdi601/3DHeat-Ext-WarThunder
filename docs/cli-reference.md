---
title: Command reference
nav_order: 90
---

# Command reference

This page is generated from the code by `tools/gen_docs_reference.py`; do not edit it by hand.
The other pages explain each command step by step.

## `heat3d-wt-replay`

```text
usage: heat3d-wt-replay [-h] -o OUT [--game GAME] [--no-smoothing] [--container]
                        [--loose] [--version]
                        replays [replays ...]

War Thunder replays (.wrpl) into 3DHeat tables

positional arguments:
  replays         .wrpl files, folders of them, or zips of them

options:
  -h, --help      show this help message and exit
  -o, --out OUT   where to write <map>/<match>.parquet and .match.json
  --game GAME     the War Thunder folder whose localisation names the vehicles (found
                  if not given)
  --no-smoothing  keep other units' dead-reckoned and received samples where the
                  replay has them
  --container     pack each battle into one .3dheat file (the default)
  --loose         keep each battle as separate files (table, match.json, sidecars),
                  not one .3dheat container
  --version       show program's version number and exit
```

## `heat3d-wt-level`

```text
usage: heat3d-wt-level [-h] [--version] {list,extract} ...

War Thunder levels into 3DHeat .glb levels

positional arguments:
  {list,extract}
    list          list the levels in the install
    extract       extract levels

options:
  -h, --help      show this help message and exit
  --version       show program's version number and exit
```

### `heat3d-wt-level list`

```text
usage: heat3d-wt-level list [-h] [--game GAME]

options:
  -h, --help   show this help message and exit
  --game GAME  War Thunder folder (default: found through Steam or the launcher)
```

### `heat3d-wt-level extract`

```text
usage: heat3d-wt-level extract [-h] [--all] -o OUT [--game GAME] [--max-grid MAX_GRID]
                               [--no-objects] [--detail {low,medium,high}]
                               [--max-object-triangles MAX_OBJECT_TRIANGLES]
                               [--no-generated] [--no-terrain-colour] [--no-texture]
                               [--skip-existing]
                               [levels ...]

positional arguments:
  levels                level names (as `list` prints them; wildcards allowed)

options:
  -h, --help            show this help message and exit
  --all                 every level
  -o, --out OUT         output folder; each level goes in <out>/<level>/
  --game GAME           War Thunder folder
  --max-grid MAX_GRID   heightmap samples a side, per part (default 1024)
  --no-objects          leave out buildings, trees and other placed objects
  --detail {low,medium,high}
                        ground sampling, ground colour and object budget over the tank
                        map (default medium; low: 1,200,000 object triangles, medium:
                        3,500,000 object triangles, high: 4,500,000 object triangles)
  --max-object-triangles MAX_OBJECT_TRIANGLES
                        budget for objects (default: the --detail's): over it, costly
                        types step down a LOD, then to a crown or their collision
                        shape, then are left out
  --no-generated        leave out the objects the land classes generate (forests,
                        towns)
  --no-terrain-colour   texture the ground with the tactical map, not the land classes
  --no-texture          do not texture the ground with the tactical map
  --skip-existing       leave levels whose .glb exists
```
