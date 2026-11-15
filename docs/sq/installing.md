---
title: "Instalimi"
nav_order: 3
lang: sq
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Instalimi {#installing}

Je i ri me rreshtin e komandave? Lexo së pari [Para se të fillosh](before-you-start.md).
Ka nevojë për Python 3.10 ose më të ri; pyarrow, numpy, zstandard dhe Pillow
instalohen bashkë me të.

## Hap pas hapi {#step-by-step}

1. Merr kodin: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   ose shkarko një zip nga [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   dhe shpaketoje.
2. Hap një terminal në atë dosje dhe shkruaj `pip install -e .`. Kjo instalon
   dy komanda: `heat3d-wt-replay` (riluajtjet) dhe `heat3d-wt-level` (nivelet).
3. Kontrolloje: `heat3d-wt-replay --version`. Duhet të shohësh
   `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` liston opsionet:

![heat3d-wt-replay --help](../assets/img/help.svg)

Pa instalim: `python -m heat3d_ext_warthunder ...` dhe
`python -m heat3d_ext_warthunder.levelcli ...` në dosjen e mjetit.

## Emrat nga instalimi yt {#names-from-your-install}

Mjetet, armët dhe municionet marrin emrat e tyre në anglisht nga skedarët e tekstit
të vetë lojës, të lexuar nga instalimi yt gjatë konvertimit. Instalimi gjendet
përmes Steam ose dosjeve të paracaktuara të nisësit; përndryshe `--game <folder>` ose
ndryshorja e mjedisit `HEAT3D_WT_GAME` tregojnë ku është. Asgjë nga teksti i lojës
nuk është në këtë depo; pa instalim emrat janë ID-të e mjeteve (konvertuesi e thotë këtë
në një rresht `note:`).

## Përditësimet {#updates}

Çdo nisje kontrollon së pari botimet e projektit në GitHub (më shumë se një kërkesë
çdo disa orë nuk bën; nuk e ndalon kurrë një konvertim, me internet apo pa). Kur ka dalë një
botim më i ri, komanda pyet përpara se ta instalojë: një `git clone` përditësohet
me `git pull --ff-only` (refuzohet derisa ke ndryshime lokale), një kopje e shkarkuar
nga arkivi i botimit. `HEAT3D_NO_UPDATE=1` e çaktivizon kontrollin dhe përditësimin.

---

Pjesë e [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacioni](https://holdi601.github.io/3DHeat/)). Burimi: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
