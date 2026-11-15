---
title: Asennus
nav_order: 3
lang: "fi"
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Asennus {#installing}

Uusi komentoriviltä? Lue ensin [Ennen aloittamista](before-you-start.md).
Tarvitaan Python 3.10 tai uudempi; pyarrow, numpy, zstandard ja Pillow
asennetaan sen mukana.

## Vaihe vaiheelta {#step-by-step}

1. Hae koodi: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   tai lataa zip-tiedosto [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)-sivulta
   ja pura se.
2. Avaa pääte kyseisessä kansiossa ja kirjoita `pip install -e .`. Tämä asentaa
   kaksi komentoa: `heat3d-wt-replay` (replayt) ja `heat3d-wt-level` (kentät).
3. Tarkista: `heat3d-wt-replay --version`. Sinun pitäisi nähdä
   `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` luettelee valinnat:

![heat3d-wt-replay --help](../assets/img/help.svg)

Ilman asennusta: `python -m heat3d_ext_warthunder ...` ja
`python -m heat3d_ext_warthunder.levelcli ...` työkalun kansiossa.

## Nimet asennuksestasi {#names-from-your-install}

Ajoneuvot, aseet ja ammukset saavat englanninkieliset nimensä pelin omista
tekstitiedostoista, jotka luetaan asennuksestasi muunnoksen aikana. Asennus
löytyy Steamin tai käynnistimen oletuskansioista; `--game <kansio>` tai
ympäristömuuttuja `HEAT3D_WT_GAME` kertovat muun sijainnin. Tässä
tietovarastossa ei ole pelin tekstejä; ilman asennusta nimet ovat ajoneuvojen
tunnuksia (muunnin kertoo tämän `note:`-rivillä).

## Päivitykset {#updates}

Jokainen käynnistys tarkistaa ensin projektin GitHub-julkaisut (enintään yksi
pyyntö muutaman tunnin välein; se ei koskaan pysäytä muunnosta, verkossa tai
ilman verkkoa). Kun uudempi julkaisu on ilmestynyt, komento kysyy ennen sen
asentamista: `git clone` -kopio päivitetään komennolla `git pull --ff-only`
(hylätään, jos sinulla on paikallisia muutoksia), ladattu kopio päivitetään
julkaisun arkistosta. `HEAT3D_NO_UPDATE=1` kytkee tarkistuksen ja päivityksen pois.

---

Osa [3DHeatiä](https://github.com/Holdi601/3DHeat) ([dokumentaatio](https://holdi601.github.io/3DHeat/)). Lähde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
