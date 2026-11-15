---
title: Diegimas
nav_order: 3
lang: "lt"
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Diegimas {#installing}

Nesate dirbę su komandine eilute? Pirma perskaitykite [Prieš pradedant](before-you-start.md).
Reikia Python 3.10 ar naujesnės versijos; pyarrow, numpy, zstandard ir Pillow įdiegiami kartu su juo.

## Žingsnis po žingsnio {#step-by-step}

1. Gaukite kodą: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`
   arba atsisiųskite zip failą iš [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   ir išskleiskite.
2. Atidarykite terminalą tame aplanke ir įrašykite `pip install -e .`. Tai įdiegia dvi komandas:
   `heat3d-wt-replay` (įrašams) ir `heat3d-wt-level` (lygiams).
3. Patikrinkite: `heat3d-wt-replay --version`. Turėtumėte matyti
   `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` parodo parametrus:

![heat3d-wt-replay --help](../assets/img/help.svg)

Be diegimo: `python -m heat3d_ext_warthunder ...` ir `python -m heat3d_ext_warthunder.levelcli ...`
įrankio aplanke.

## Vardai iš jūsų diegimo {#names-from-your-install}

Technika, ginklai ir šaudmenys gauna savo angliškus vardus iš žaidimo teksto failų, kuriuos
konvertavimo metu skaito iš jūsų diegimo. Diegimas randamas per Steam ar paleidiklio numatytuosius
aplankus; kitu atveju tai nurodo `--game <folder>` arba aplinkos kintamasis `HEAT3D_WT_GAME`.
Jokio žaidimo teksto šioje saugykloje nėra; be diegimo vardai yra techninės įrangos id (konverteris
apie tai praneša `note:` eilute).

## Atnaujinimai {#updates}

Kiekvieno paleidimo metu pirmiausia tikrinami projekto GitHub leidimai (ne dažniau kaip kartą per
kelias valandas; tai niekada nesustabdo konvertavimo, prisijungus ar neprisijungus). Kai išleidžiama
naujesnė versija, komanda prieš diegdama klausia: `git clone` kopija atnaujinama su
`git pull --ff-only` (atsisakoma, jei turite vietinių pakeitimų), atsisiųsta kopija - iš leidimo
archyvo. `HEAT3D_NO_UPDATE=1` išjungia ir tikrinimą, ir atnaujinimą.

---

Dalis [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Šaltinis: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
