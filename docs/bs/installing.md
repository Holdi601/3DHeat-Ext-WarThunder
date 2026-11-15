---
title: "Instalacija"
nav_order: 3
lang: "bs"
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Instalacija {#installing}

Niste navikli na komandnu liniju? Prvo pročitajte [Prije nego počnete](before-you-start.md).
Potreban je Python 3.10 ili noviji; pyarrow, numpy, zstandard i Pillow
instaliraju se uz njega.

## Korak po korak {#step-by-step}

1. Nabavite kod: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   ili preuzmite zip sa [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   i raspakirajte ga.
2. Otvorite terminal u tom folderu i upišite `pip install -e .`. Time se instaliraju
   dvije naredbe: `heat3d-wt-replay` (replayevi) i `heat3d-wt-level` (nivoi).
3. Provjerite: `heat3d-wt-replay --version`. Trebali biste vidjeti
   `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` ispisuje opcije:

![heat3d-wt-replay --help](../assets/img/help.svg)

Bez instalacije: `python -m heat3d_ext_warthunder ...` i
`python -m heat3d_ext_warthunder.levelcli ...` u folderu alata.

## Imena iz vaše instalacije {#names-from-your-install}

Vozila, oružje i municija dobivaju svoja engleska imena iz tekstualnih datoteka same igre,
koje se čitaju iz vaše instalacije prilikom pretvaranja. Instalacija se nalazi
preko Steama ili zadanih foldera launchera; `--game <folder>` ili
varijabla okruženja `HEAT3D_WT_GAME` kažu gdje je inače. Ništa od
tekstova igre nije u ovom repozitoriju; bez instalacije imena su
id-ovi vozila (konverter to kaže u redu `note:`).

## Ažuriranja {#updates}

Svako pokretanje prvo provjerava GitHub izdanja projekta (najviše jedan zahtjev
svakih nekoliko sati; nikad ne zaustavlja pretvaranje, bilo da ste online ili ne). Kada izađe novije
izdanje, naredba pita prije instalacije: `git clone` se
ažurira sa `git pull --ff-only` (odbija se dok imate lokalne izmjene), a
preuzeta kopija iz arhive izdanja. `HEAT3D_NO_UPDATE=1` isključuje
provjeru i ažuriranje.

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
