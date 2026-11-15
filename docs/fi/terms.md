---
title: Ehdot ja lisenssi
nav_order: 16
lang: "fi"
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# Ehdot ja lisenssi {#terms-and-licence}

## Ehdot {#the-terms}

Gaijinin käyttöehdot (päivitetty 2026-08-17), EULA (liite 2):
3.2.2 "modify, translate, create derivative works of, reverse engineer,
disassemble, or decompile the Game(s)", 3.2.9 "mine or collect any data from
the Game(s) that is not intended to be publicly displayed"; 1.2 "are not
permitted to store, download, modify, or otherwise use any part of the Game(s)"
pelin asiakasohjelman lisäksi. Oman pelikopion kenttätiedostojen lukeminen paikalliseksi 3D-näkymäksi on
käyttäjän päätös, joka tehdään tietäen tämän. Kirjoitetut kentät pysyvät koneellasi: **älä koskaan julkaise niitä**,
eikä tästä mikään toimita pelin dataa.

## Lähteet {#sources}

Kaikki täällä oleva koodi on kirjoitettu tätä projektia varten; mitään koodia ei ole kopioitu toisesta jäsentäjästä. Se, mitä
se tietää formaatista, tulee seuraavista:

- Gaijinin Dagor Engine -lähdekoodi (github.com/GaijinEntertainment/DagorEngine, BSD 3-Clause):
  `prog/engine/daECS/net/network.cpp`, `connection.cpp`, `object.cpp`, `serialize.cpp`, `compression.h` ja
  `prog/engine/daECS/core/baseIo.cpp`, `componentTypes.cpp` kokonaisuusvirralle (`ecs.py`), sekä `net/message.cpp`
  (`MessageClass::initImpl`) sille, miten kokonaisuusviestit numeroivat luokkansa. Komponenttien ja tyyppien nimet
  täsmäytetään niiden FNV-1a-tiivisteisiin pelin omien arkistojen sanoista; `ecs.py` luettelee löydetyt nimet.
- Saman lähdekoodin `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp` ja `daNet/bitStream.h`: miten viesti
  nimeää kohteen, jolle se on (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`, `docs/REPLAY-DECODE-ECS.md`,
  `docs/QUICK-REF.md` ja sen oma jäsentäjä `web/wrpl-parse.js`, luettu lentomallin, maasynkronoinnin, lennossa olevien
  aseiden, tunnuskenttäviestien, pelaajapaikkojen, ohjaamon arvojen ja binäärisen blk:n bittiasetteluihin. WTACRP nimeää
  omiksi viitteikseen maxsupermanhd/wrpl-inspector, wt_blk ja wrpl-acmi (AGPL-3.0); niiden koodia ei ole luettu täällä.
- Tekijän omat replayt, luettuina tiedostoina: vuoden 2025 erot (lentomallin vanhempi asettelu, chat ilman merkkitavua,
  zlib), maan asento, pakattu korkeuden siirtymä, aseiden irrotuspisteet ja ohjaamon mittarit selvitettiin niistä täällä.

## Testit {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # tarkistaa myös julkiset vuoden 2025 esimerkkireplayt
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # askeleet, identiteetit, tekoälyliput, rollin merkki, tasoittaja, nimet
```

Yksikkötestit eivät lue asennusta (`HEAT3D_WT_NO_NAMES` on asetettu); testi omilla replayillä lukee nimet asennuksestasi.

Testit rakentavat replayt koodissa (`tests/synth.py`: otsikko, paketit, tulokset, kokonaisuusvirta, lennossa olevat aseet)
lukijoiden dokumentoimaan asetteluun; tietovarastossa ei ole yhtään replayta.

## Lisenssi {#licence}

MIT - katso [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Käyttää pyarrow (Apache-2.0),
numpy (BSD-3-Clause), zstandard (BSD-3-Clause) ja Pillow (MIT-CMU). Kentän lukijat on kirjoitettu Dagor Enginen lähdekoodin
perusteella, Copyright (c) 2023 Gaijin Entertainment, BSD 3-Clause -lisenssi; mitään sen koodia ei ole kopioitu tänne, ja
käytetyt formaattivakiot (vromfs-XOR-avain, korkeusalueruudukon siirtymät) on mainittu siellä, missä ne esiintyvät.

---

Osa [3DHeatiä](https://github.com/Holdi601/3DHeat) ([dokumentaatio](https://holdi601.github.io/3DHeat/)). Lähde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
