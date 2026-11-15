---
title: "Telepítés"
nav_order: 3
lang: hu
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Telepítés {#installing}

Új vagy a parancssorban? Olvasd el előbb a [Mielőtt elkezded](before-you-start.md) oldalt.
Python 3.10 vagy újabb kell hozzá; a pyarrow, numpy, zstandard és Pillow csomagok vele
együtt települnek.

## Lépésről lépésre {#step-by-step}

1. Szerezd meg a kódot: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   vagy töltsd le a zip-et a [Kiadások](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   oldalról, és csomagold ki.
2. Nyiss egy terminált ebben a mappában, és írd be: `pip install -e .`. Ez két parancsot
   telepít: `heat3d-wt-replay` (visszajátszások) és `heat3d-wt-level` (pályák).
3. Ellenőrizd: `heat3d-wt-replay --version`. Ezt kell látnod:
   `heat3d-wt-replay 0.2.0`. A `heat3d-wt-replay --help` felsorolja a kapcsolókat:

![heat3d-wt-replay --help](../assets/img/help.svg)

Telepítés nélkül: `python -m heat3d_ext_warthunder ...` és
`python -m heat3d_ext_warthunder.levelcli ...` az eszköz mappájában.

## Nevek a telepítésedből {#names-from-your-install}

A járművek, fegyverek és lőszerek angol neveit a játék saját szövegfájljai adják, amelyeket
konvertáláskor a telepítésedből olvasunk be. A telepítést a Steamen vagy az indító
alapértelmezett mappáin keresztül találjuk meg; ha másutt van, a `--game <folder>` kapcsoló
vagy a `HEAT3D_WT_GAME` környezeti változó mondja meg, hol. A játék szövegei nincsenek
ebben a tárolóban; telepítés nélkül a nevek a jármű-azonosítók lesznek (a konverter ezt
egy `note:` sorban jelzi).

## Frissítések {#updates}

Minden indításkor először ellenőrzi a projekt GitHub-kiadásait (legfeljebb néhány óránként
egy kérés; soha nem állítja le a konvertálást, online vagy offline). Ha újabb kiadás van,
a parancs a telepítés előtt megkérdezi: a `git clone` másolatot a `git pull --ff-only`
paranccsal frissíti (megtagadja, ha van helyi módosításod), a letöltött másolatot pedig a
kiadás archívumából. A `HEAT3D_NO_UPDATE=1` kikapcsolja az ellenőrzést és a frissítést.

---

A [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentáció](https://holdi601.github.io/3DHeat/)) része. Forrás: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
