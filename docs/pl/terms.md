---
title: Warunki i licencja
nav_order: 16
lang: "pl"
source: terms.md
source_hash: "01d249aa8f1b"
nav_exclude: true
search_exclude: true
---
# Warunki i licencja {#terms-and-licence}

## Co jest odczytywane {#what-it-reads}

Konwerter odczytuje replaye, które War Thunder zapisuje na twoim komputerze (albo replaye twoich bitew, które sam pobrałeś z warthunder.com), oraz pliki poziomów z twojej własnej instalacji War Thunder. Nic z gry nie jest tu dołączone ani rozpowszechniane: żadnych zasobów gry, żadnego kodu gry, żadnych bibliotek DLL; Oodle jest wczytywany z twojej własnej instalacji. To, co zapisuje, zostaje na twoim komputerze: **nigdy nie publikuj poziomów**.

3DHeat nie jest powiązany z Gaijin Entertainment ani zatwierdzony przez Gaijin Entertainment. War Thunder oraz powiązane nazwy i znaki towarowe należą do ich właścicieli.

Posiadacze praw: otwórzcie zgłoszenie (issue) na <https://github.com/Holdi601/3DHeat-Ext-WarThunder/issues> - odpowiadamy szybko i na prośbę usuwamy wszystko.

## Źródła {#sources}

Cały kod tutaj został napisany na potrzeby tego projektu; żaden kod nie został skopiowany z innego parsera. To, co
projekt wie o formacie, pochodzi z:

- Kodu Dagor Engine Gaijin (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` i `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` dla strumienia obiektów (`ecs.py`), oraz `net/message.cpp`
  (`MessageClass::initImpl`) dla tego, jak komunikaty obiektów numerują swoje klasy. Nazwy komponentów i typów
  są dopasowane przez ich hasze FNV-1a do słów z archiwów samej gry; `ecs.py` wypisuje znalezione nazwy.
- `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp`
  i `daNet/bitStream.h` z tego samego kodu: jak komunikat nazywa obiekt, do którego jest
  (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md` oraz jego własny parser
  `web/wrpl-parse.js`, czytane pod kątem układów bitów modelu lotu, synchronizacji
  naziemnej, broni w locie, komunikatów z polami identyfikatorów, slotów graczy, wartości
  kabiny i binarnego blk. WTACRP wskazuje jako własne odniesienia maxsupermanhd/wrpl-inspector,
  wt_blk i wrpl-acmi (AGPL-3.0); ich kodu tutaj nie czytano.
- Replaye autora, czytane jako pliki: różnice z 2025 (starszy układ modelu lotu,
  czat bez bajtu flagi, zlib), postawa naziemna, przesunięcie upakowanej wysokości,
  punkty zrzutu broni i wskaźniki kabiny zostały tutaj wyliczone właśnie na nich.

## Testy {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # also checks the public 2025 sample replays
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # steps, identities, AI flags, roll sign, the smoother, names
```

Testy jednostkowe nigdy nie czytają instalacji (ustawione jest `HEAT3D_WT_NO_NAMES`);
test na własnych replayach czyta nazwy z Twojej instalacji.

Testy budują replaye w kodzie (`tests/synth.py`: nagłówek, pakiety, wyniki,
strumień obiektów, broń w locie) w układzie opisanym przez czytniki; żaden replay
nie znajduje się w repozytorium.

## Licencja {#licence}

MIT – zob. [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Używa pyarrow (Apache-2.0), numpy (BSD-3-Clause),
zstandard (BSD-3-Clause) i Pillow (MIT-CMU). Czytniki poziomów zostały napisane
na podstawie kodu Dagor Engine, Copyright (c) 2023 Gaijin Entertainment, licencja BSD
3-Clause; żaden jego kod nie jest tu skopiowany, a stałe formatu użyte
(klucz XOR vromfs, przesunięcia siatki zakresu wysokości) są podane tam, gdzie się pojawiają.

---

Część [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacja](https://holdi601.github.io/3DHeat/)). Źródło: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
