---
title: Instalacija
nav_order: 3
lang: hr
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Instalacija {#installing}

Nikad nisi koristio naredbeni redak? Prvo pročitaj [Prije početka](before-you-start.md).
Treba Python 3.10 ili noviji; pyarrow, numpy, zstandard i Pillow se instaliraju uz njega.

## Korak po korak {#step-by-step}

1. Preuzmi kod: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   ili preuzmi zip s [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   i raspakiraj ga.
2. Otvori terminal u toj mapi i upiši `pip install -e .`. Ovo instalira dvije
   naredbe: `heat3d-wt-replay` (snimke) i `heat3d-wt-level` (razine).
3. Provjeri: `heat3d-wt-replay --version`. Trebao bi vidjeti
   `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` ispisuje opcije:

![heat3d-wt-replay --help](../assets/img/help.svg)

Bez instalacije: `python -m heat3d_ext_warthunder ...` i
`python -m heat3d_ext_warthunder.levelcli ...` u mapi alata.

## Nazivi iz tvoje instalacije {#names-from-your-install}

Vozila, oružje i streljivo dobivaju svoje engleske nazive iz tekstualnih datoteka same igre,
koje se čitaju iz tvoje instalacije pri pretvaranju. Instalacija se traži preko Steama ili
zadanih mapa launchera; `--game <mapa>` ili varijabla okoline `HEAT3D_WT_GAME` govore gdje
je inače. Tekst igre nije u ovom repozitoriju; bez instalacije nazivi su identifikatori vozila
(pretvarač to kaže u retku `note:`).

## Ažuriranja {#updates}

Svako pokretanje prvo provjerava GitHub izdanja projekta (najviše jedan zahtjev svakih nekoliko
sati; nikad ne zaustavlja pretvaranje, online ili offline). Kad je izašlo novije izdanje,
naredba pita prije instaliranja: `git clone` se ažurira s `git pull --ff-only` (odbija se dok imaš
lokalne promjene), a preuzeta kopija iz arhive izdanja. `HEAT3D_NO_UPDATE=1` isključuje
provjeru i ažuriranje.

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
