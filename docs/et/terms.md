---
title: Tingimused ja litsents
nav_order: 16
lang: "et"
source: terms.md
source_hash: "01d249aa8f1b"
nav_exclude: true
search_exclude: true
---
# Tingimused ja litsents {#terms-and-licence}

## Mida loetakse {#what-it-reads}

Konverter loeb kordusi, mille War Thunder sinu arvutisse salvestab (või sinu lahingute kordusi, mille sa ise warthunder.com-ist alla laadisid), ja sinu enda War Thunderi paigalduse tasemefaile. Mängust ei ole siin midagi kaasas ega levitata edasi: ei mänguvarasid, ei mängukoodi ega DLL-e; Oodle laaditakse sinu enda paigaldusest. See, mida ta kirjutab, jääb sinu arvutisse: **ära avalda tasemeid kunagi**.

3DHeat ei ole seotud ettevõttega Gaijin Entertainment ega selle poolt heaks kiidetud. War Thunder ja sellega seotud nimed ning kaubamärgid kuuluvad nende omanikele.

Õiguste omajad: avage issue aadressil <https://github.com/Holdi601/3DHeat-Ext-WarThunder/issues> - vastame kiiresti ja eemaldame soovi korral kõik.

## Allikad {#sources}

Kogu siinne kood on kirjutatud selle projekti jaoks; ühtegi koodi ei ole kopeeritud
teisest parserist. Formaadi kohta teatakse see järgmistest allikatest:

- Gaijini Dagor Engine'i lähtekood (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` ja `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` olemi voo jaoks (`ecs.py`), ning `net/message.cpp`
  (`MessageClass::initImpl`) selle kohta, kuidas olemi sõnumid oma klassid
  nummerdavad. Komponentide ja tüüpide nimed sobitatakse nende FNV-1a räsidega
  mängu enda arhiivide sõnadega; `ecs.py` loetleb leitud nimed.
- Sama lähtekoodi `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp`
  ja `daNet/bitStream.h`: kuidas sõnum nimetab objekti, kellele ta on
  (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md` ja tema enda parser
  `web/wrpl-parse.js`, loetud lennumudeli, maapealse sünkroonimise, rakettide
  lennu, ID-väljadega sõnumite, mängijaslotide, kabiini väärtuste ja binaarse blk
  bitipaigutuste jaoks. WTACRP nimetab oma viidetena maxsupermanhd/wrpl-inspector,
  wt_blk ja wrpl-acmi (AGPL-3.0); nende koodi siin ei loetud.
- Autori enda kordused, loetud failidena: 2025. aasta erinevused (lennumudeli vanem
  paigutus, vestlus ilma lipubaidita, zlib), maapealse asendi, pakitud kõrguse nihke,
  relvade vabastuspunktide ja kabiini instrumentide tööd tehti nende peal siin.

## Testid {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # also checks the public 2025 sample replays
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # steps, identities, AI flags, roll sign, the smoother, names
```

Üksustestid ei loe kunagi installatsiooni (`HEAT3D_WT_NO_NAMES` on seatud); test
sinu enda kordustega loeb nimed sinu installatsioonist.

Testid koostavad kordused koodis (`tests/synth.py`: päis, paketid, tulemused,
olemi voog, rakettide lend) lugejate dokumenteeritud paigutuse järgi; hoidlas ei ole
ühtegi kordust.

## Litsents {#licence}

MIT - vt [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Kasutab pyarrow'd (Apache-2.0), numpy'd (BSD-3-Clause),
zstandardi (BSD-3-Clause) ja Pillow'd (MIT-CMU). Tasemelugejad on kirjutatud Dagor Engine'i
lähtekoodi järgi, Copyright (c) 2023 Gaijin Entertainment, BSD 3-Clause litsents;
selle koodi ei ole siia kopeeritud, ja kasutatud formaadikonstandid (vromfs XOR-võti,
kõrguste vahemiku ruudustiku nihked) on tsiteeritud seal, kus need esinevad.

---

Osa [3DHeatist](https://github.com/Holdi601/3DHeat) ([dokumentatsioon](https://holdi601.github.io/3DHeat/)). Lähtekood: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
