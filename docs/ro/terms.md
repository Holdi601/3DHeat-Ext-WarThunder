---
title: Termeni și licență
nav_order: 16
lang: ro
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# Termeni și licență {#terms-and-licence}

## Termenii {#the-terms}

Termenii de serviciu Gaijin (actualizați 2026-08-17), EULA (Anexa 2):
3.2.2 „modify, translate, create derivative works of, reverse engineer,
disassemble, or decompile the Game(s)” (a modifica, traduce, crea opere derivate, a face inginerie inversă,
a dezasambla sau a decompila Jocul/Jocurile), 3.2.9 „mine or collect any data from
the Game(s) that is not intended to be publicly displayed” (a extrage sau colecta orice date din Joc/Jocuri care nu sunt destinate să fie afișate public); 1.2 „are not
permitted to store, download, modify, or otherwise use any part of the Game(s)”
(nu aveți voie să stocați, descărcați, modificați sau folosiți în alt fel vreo parte din Joc/Jocuri) dincolo de client. Citirea fișierelor de nivel ale propriei dumneavoastră copii într-o vedere 3D locală
este decizia utilizatorului, luată cunoscând asta. Nivelurile scrise rămân pe
calculatorul dumneavoastră: **nu le publicați niciodată**, iar nimic de aici nu livrează date ale jocului.

## Surse {#sources}

Tot codul de aici este scris pentru acest proiect; niciun cod nu a fost copiat din alt parser. Ce
știe despre format vine din:

- Codul sursă Dagor Engine al Gaijin (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` și `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` pentru fluxul de entități (`ecs.py`), și `net/message.cpp`
  (`MessageClass::initImpl`) pentru felul în care mesajele de entitate își numerotează clasele. Numele componentelor și ale tipurilor sunt potrivite prin hash-urile lor FNV-1a cu cuvinte din arhivele
  proprii ale jocului; `ecs.py` listează numele găsite.
- `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp` și `daNet/bitStream.h`
  din același cod sursă: cum numește un mesaj obiectul pentru care este (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md`, și propriul său parser
  `web/wrpl-parse.js`, citite pentru aranjamentele pe biți ale modelului de zbor, sincronizării terestre, armelor în zbor, mesajelor cu câmpuri de id, sloturilor de jucători, valorilor cabinei și blk-ului binar. WTACRP numește ca propriile referințe maxsupermanhd/wrpl-inspector,
  wt_blk și wrpl-acmi (AGPL-3.0); codul lor nu a fost citit aici.
- Replay-urile autorului, citite ca fișiere: diferențele din 2025 (aranjamentul mai vechi al modelului de zbor, chat fără octet de steag, zlib), atitudinea terestră, decalajul înălțimii împachetate, punctele de eliberare ale armelor și indicatoarele cabinei au fost stabilite pe ele aici.

## Teste {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # verifică și replay-urile publice de exemplu din 2025
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # pași, identități, marcaje IA, semnul rulării, netezirea, nume
```

Testele unitare nu citesc niciodată o instalare (`HEAT3D_WT_NO_NAMES` este setat); testul
cu replay-urile dumneavoastră citește numele din instalarea dumneavoastră.

Testele construiesc replay-uri în cod (`tests/synth.py`: antet, pachete, rezultate,
fluxul de entități, arme în zbor) după aranjamentul documentat de cititori; niciun
replay nu se află în depozit.

## Licență {#licence}

MIT - vedeți [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Folosește pyarrow (Apache-2.0), numpy (BSD-3-Clause),
zstandard (BSD-3-Clause) și Pillow (MIT-CMU). Cititorii de niveluri au fost scriși
după codul sursă al Dagor Engine, Copyright (c) 2023 Gaijin Entertainment, licența BSD
3-Clause; niciun cod al acestuia nu este copiat aici, iar constantele de format folosite
(cheia XOR a vromfs, decalajele grilei intervalelor de înălțime) sunt citate acolo unde apar.

---

Parte din [3DHeat](https://github.com/Holdi601/3DHeat) ([documentație](https://holdi601.github.io/3DHeat/)). Sursă: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
