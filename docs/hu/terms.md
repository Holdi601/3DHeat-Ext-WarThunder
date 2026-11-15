---
title: "Feltételek és licenc"
nav_order: 16
lang: hu
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# Feltételek és licenc {#terms-and-licence}

## A feltételek {#the-terms}

Gaijin Szolgáltatási Feltételek (frissítve: 2026-08-17), EULA (2. melléklet):
3.2.2 "modify, translate, create derivative works of, reverse engineer,
disassemble, or decompile the Game(s)", 3.2.9 "mine or collect any data from
the Game(s) that is not intended to be publicly displayed"; 1.2 "are not
permitted to store, download, modify, or otherwise use any part of the Game(s)"
a kliensen túl. Hogy a saját példányod pályafájljait egy helyi 3D-s nézetbe
olvasod be, az a felhasználó döntése, amelyet ennek ismeretében hoz meg. Az
elkészült pályák a gépeden maradnak: **soha ne tedd közzé őket**, és ez a
tároló semmilyen játékadatot nem szállít.

## Források {#sources}

Minden kód itt ehhez a projekthez készült; semmilyen kódot nem másoltunk más
elemzőből. Hogy mit tud a formátumról, az a következőkből származik:

- A Gaijin Dagor Engine forráskódja (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` és `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` az entitásfolyamhoz (`ecs.py`), és a `net/message.cpp`
  (`MessageClass::initImpl`) arra, hogyan számozzák az entitásüzenetek az osztályaikat.
  A komponens- és típusneveket FNV-1a hash-ük alapján párosítjuk a játék saját
  archívumainak szavaival; az `ecs.py` felsorolja a megtalált neveket.
- Ugyanennek a forrásnak a `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp`
  és `daNet/bitStream.h` fájljai: hogyan nevezi meg egy üzenet azt az objektumot, akinek szól
  (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): a `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md`, és a saját elemzője, a
  `web/wrpl-parse.js`, amelyet a repülési modell, a földi szinkron, a repülő fegyverek,
  az azonosító-mezős üzenetek, a játékos-helyek, a fedélzeti értékek és a bináris blk bitelrendezéséhez
  olvastunk. A WTACRP a maxsupermanhd/wrpl-inspector, a wt_blk és a wrpl-acmi (AGPL-3.0)
  projekteket nevezi meg a saját hivatkozásaiként; ezek kódját itt nem olvastuk.
- A szerző saját visszajátszásai, fájlként olvasva: a 2025-ös különbségek (a repülési modell
  régebbi elrendezése, a chat jelzőbájt nélkül, zlib), a földi állás, a tömörített magasság
  eltolása, a fegyverek kilövési pontjai és a fedélzeti műszerek ezeken készültek el.

## Tesztek {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # also checks the public 2025 sample replays
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # steps, identities, AI flags, roll sign, the smoother, names
```

Az egységtesztek soha nem olvasnak telepítést (a `HEAT3D_WT_NO_NAMES` be van állítva); a saját
visszajátszásokkal futó teszt a neveket a telepítésedből olvassa.

A tesztek kódban építik fel a visszajátszásokat (`tests/synth.py`: fejléc, csomagok, eredmények,
az entitásfolyam, repülő fegyverek) a leírt olvasók elrendezése szerint; visszajátszás nincs a
tárolóban.

## Licenc {#licence}

MIT – lásd a [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE)
fájlt. Használja a pyarrow (Apache-2.0), a numpy (BSD-3-Clause), a zstandard (BSD-3-Clause) és
a Pillow (MIT-CMU) csomagokat. A pályaolvasókat a Dagor Engine forráskódja alapján írtuk, Copyright
(c) 2023 Gaijin Entertainment, BSD 3-Clause licenc; ebből kódot nem másoltunk, a használt
formátumállandók (a vromfs XOR-kulcs, a magasságtartomány-rács eltolásai) ott vannak megjelölve,
ahol előfordulnak.

---

A [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentáció](https://holdi601.github.io/3DHeat/)) része. Forrás: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
