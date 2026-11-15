---
title: "Installazzjoni"
nav_order: 3
lang: mt
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Installazzjoni {#installing}

Ġdid mal-linja tal-kmandi? Aqra [Qabel ma tibda](before-you-start.md) l-ewwel.
Teħtieġ Python 3.10 jew aktar ġdid; pyarrow, numpy, zstandard u Pillow jiġu
installati miegħu.

## Pass b'pass {#step-by-step}

1. Ġib il-kodiċi: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   jew niżżel zip minn [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   u ħollu.
2. Iftaħ terminal f'dak il-folder u ikteb `pip install -e .`. Dan jinstalla żewġ
   kmandi: `heat3d-wt-replay` (ripetizzjonijiet) u `heat3d-wt-level` (livelli).
3. Iċċekkjah: `heat3d-wt-replay --version`. Għandek tara
   `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` jelenka l-għażliet:

![heat3d-wt-replay --help](../assets/img/help.svg)

Mingħajr installazzjoni: `python -m heat3d_ext_warthunder ...` u
`python -m heat3d_ext_warthunder.levelcli ...` fil-folder tal-għodda.

## Ismijiet mill-installazzjoni tiegħek {#names-from-your-install}

Il-vetturi, l-armi u l-munizzjon jieħdu l-ismijiet Ingliżi tagħhom mill-fajls tat-test
proprji tal-logħba, moqrija mill-installazzjoni tiegħek meta tikkonverti. L-installazzjoni
tinstab permezz ta' Steam jew tal-folders default tal-launcher; `--game <folder>` jew
il-varjabbli tal-ambjent `HEAT3D_WT_GAME` jgħidu fejn tinsab inkella. Xejn mit-test tal-logħba
mhu f'dan ir-repożitorju; mingħajr installazzjoni l-ismijiet huma l-ids tal-vetturi (il-konvertitur
jgħid hekk f'linja `note:`).

## Aġġornamenti {#updates}

Kull bidu l-ewwel jiċċekkja r-releases tal-proġett fuq GitHub (l-iktar talba
waħda kull ftit sigħat; qatt ma twaqqaf konverżjoni, online jew le). Meta toħroġ
release ġdida, il-kmand jistaqsi qabel jinstallaha: `git clone` jiġi aġġornat
b'`git pull --ff-only` (miċħud waqt li jkollok bidliet lokali), kopja niżżelta
mill-arkivju tar-release. `HEAT3D_NO_UPDATE=1` ixolji ċ-ċekk u l-aġġornament.

---

Parti mid-[3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentazzjoni](https://holdi601.github.io/3DHeat/)). Sors: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
