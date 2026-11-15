---
title: "Installéieren"
nav_order: 3
lang: lb
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Installéieren {#installing}

Nei op der Kommandozeil? Liest fir d'éischt [Ier Dir ufänkt](before-you-start.md).
Brauch Python 3.10 oder méi nei; pyarrow, numpy, zstandard a Pillow ginn
domat installéiert.

## Schrëtt fir Schrëtt {#step-by-step}

1. Hollt de Code: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   oder luet eng Zip vun [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   erof a packt se aus.
2. Mécht en Terminal an deem Dossier op an tippt `pip install -e .`. Dat installéiert
   zwee Befehler: `heat3d-wt-replay` (Replays) an `heat3d-wt-level` (Levelen).
3. Préift et: `heat3d-wt-replay --version`. Dir sollt
   `heat3d-wt-replay 0.2.0` gesinn. `heat3d-wt-replay --help` list d'Optiounen op:

![heat3d-wt-replay --help](../assets/img/help.svg)

Ouni Installatioun: `python -m heat3d_ext_warthunder ...` an
`python -m heat3d_ext_warthunder.levelcli ...` am Dossier vum Tool.

## Nimm aus Ärer Installatioun {#names-from-your-install}

Gefierer, Waffen a Munitioun kréie hir englesch Nimm aus de Textdateien vum Spill selwer,
déi beim Émwandele aus Ärer Installatioun gelies ginn. D'Installatioun gëtt
iwwer Steam oder d'Standarddossiere vum Launcher fonnt; `--game <folder>` oder d'
Émfeldvariabel `HEAT3D_WT_GAME` soen, wou se soss ass. Näischt vum Text vum Spill
ass an dësem Repository; ouni Installatioun sinn d'Nimm d'Gefier-IDen
(de Konverter seet dat an enger `note:`-Zeil).

## Updates {#updates}

All Start kuckt fir d'éischt an de GitHub-Releases vum Projet no (héchstens eng Ufro
all puer Stonnen; et stoppt ni eng Émwandlung, online oder net). Wann e méi neie
Release do ass, freet de Befehl, ier en en installéiert: e `git clone` gëtt
mat `git pull --ff-only` aktualiséiert (verweigert, wann Dir lokal Ännerunge hutt), eng
erofgeluede Kopie aus dem Archiv vum Release. `HEAT3D_NO_UPDATE=1` schalt d'
Kontroll an d'Update aus.

---

Deel vun [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentatioun](https://holdi601.github.io/3DHeat/)). Quell: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
