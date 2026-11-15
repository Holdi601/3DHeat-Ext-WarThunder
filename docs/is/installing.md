---
title: "Uppsetning"
nav_order: 3
lang: is
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Uppsetning {#installing}

Hefurðu aldrei notað skipanalínu? Lestu fyrst [Áður en þú byrjar](before-you-start.md).
Þarf Python 3.10 eða nýrra; pyarrow, numpy, zstandard og Pillow eru sett upp
með því.

## Skref fyrir skref {#step-by-step}

1. Náðu í kóðann: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   eða sæktu zip úr [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   og pakkaðu því upp.
2. Opnaðu skipanalínu í þeirri möppu og skrifaðu `pip install -e .`. Þetta
   setur upp tvær skipanir: `heat3d-wt-replay` (upptökur) og `heat3d-wt-level`
   (borð).
3. Athugaðu það: `heat3d-wt-replay --version`. Þú ættir að sjá
   `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` sýnir valkostina:

![heat3d-wt-replay --help](../assets/img/help.svg)

Án uppsetningar: `python -m heat3d_ext_warthunder ...` og
`python -m heat3d_ext_warthunder.levelcli ...` í möppu verkfærisins.

## Nöfn úr þinni uppsetningu {#names-from-your-install}

Farartæki, vopn og skotfæri fá ensku nöfnin sín úr eigin textaskrám leiksins,
lesnum úr þinni uppsetningu þegar breytt er. Uppsetningin finnst í gegnum
Steam eða sjálfgefnar möppur ræsiforritsins; `--game <folder>` eða
umhverfisbreytan `HEAT3D_WT_GAME` segja til um hvar hún er annars. Ekkert af
texta leiksins er í þessari geymslu; án uppsetningar eru nöfnin auðkenni
farartækjanna (umbreytirinn segir frá því í `note:` línu).

## Uppfærslur {#updates}

Við hverja ræsingu er fyrst athugað með útgáfur verkefnisins á GitHub (í mesta
lagi ein beiðni á nokkurra klukkustunda fresti; það stöðvar aldrei breytingu,
hvort sem þú ert nettengdur eða ekki). Þegar nýrri útgáfa er komin spyr
skipunin áður en hún setur hana upp: `git clone` er uppfært með
`git pull --ff-only` (hafnað meðan þú ert með staðbundnar breytingar),
niðurhalað afrit úr safnskrá útgáfunnar. `HEAT3D_NO_UPDATE=1` slekkur á
athuguninni og uppfærslunni.

---

Hluti af [3DHeat](https://github.com/Holdi601/3DHeat) ([skjölun](https://holdi601.github.io/3DHeat/)). Frumkóði: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
