---
title: Installation
nav_order: 3
lang: da
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Installation {#installing}

Ny til kommandolinjen? Læs [Før du går i gang](before-you-start.md) først.
Kræver Python 3.10 eller nyere; pyarrow, numpy, zstandard og Pillow installeres
sammen med det.

## Trin for trin {#step-by-step}

1. Hent koden: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   eller download en zip fra [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   og pak den ud.
2. Åbn en terminal i den mappe og skriv `pip install -e .`. Det installerer to
   kommandoer: `heat3d-wt-replay` (replays) og `heat3d-wt-level` (baner).
3. Tjek det: `heat3d-wt-replay --version`. Du bør se
   `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` viser valgmulighederne:

![heat3d-wt-replay --help](../assets/img/help.svg)

Uden installation: `python -m heat3d_ext_warthunder ...` og
`python -m heat3d_ext_warthunder.levelcli ...` i værktøjets mappe.

## Navne fra din installation {#names-from-your-install}

Køretøjer, våben og ammunition får deres engelske navne fra spillets egne
tekstfiler, som læses fra din installation under konverteringen. Installationen
findes via Steam eller launcherens standardmapper; `--game <mappe>` eller
miljøvariablen `HEAT3D_WT_GAME` angiver den ellers. Intet af spillets tekst ligger
i dette repository; uden en installation er navnene køretøjernes id'er (konverteren
siger det i en `note:`-linje).

## Opdateringer {#updates}

Hver start tjekker først projektets GitHub-releases (højst én forespørgsel hver
få timer; det stopper aldrig en konvertering, hverken online eller offline). Når
en nyere release er udgivet, spørger kommandoen, før den installerer den: en
`git clone` opdateres med `git pull --ff-only` (afvist, mens du har lokale
ændringer), en downloadet kopi fra releasens arkiv. `HEAT3D_NO_UPDATE=1` slår
tjekket og opdateringen fra.

---

Del af [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
