---
title: Warunki i licencja
nav_order: 16
lang: "pl"
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# Warunki i licencja {#terms-and-licence}

## Warunki {#the-terms}

Warunki Usługi Gaijin (zaktualizowane 2026-08-17), EULA (Załącznik 2):
3.2.2 "modify, translate, create derivative works of, reverse engineer,
disassemble, or decompile the Game(s)", 3.2.9 "mine or collect any data from
the Game(s) that is not intended to be publicly displayed"; 1.2 "are not
permitted to store, download, modify, or otherwise use any part of the Game(s)"
poza klientem. Wczytanie plików poziomów z własnej kopii gry do lokalnego widoku 3D
to decyzja użytkownika, podjęta ze świadomością tych zapisów. Zapisane poziomy zostają na Twoim
komputerze: **nigdy ich nie publikuj**, a nic tutaj nie zawiera danych gry.

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
