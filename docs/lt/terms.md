---
title: Sąlygos ir licencija
nav_order: 16
lang: "lt"
source: terms.md
source_hash: "01d249aa8f1b"
nav_exclude: true
search_exclude: true
---
# Sąlygos ir licencija {#terms-and-licence}

## Kas skaitoma {#what-it-reads}

Konverteris skaito įrašus, kuriuos War Thunder išsaugo jūsų kompiuteryje (arba savo mūšių įrašus, kuriuos patys atsisiuntėte iš warthunder.com), ir jūsų pačių War Thunder diegimo lygių failus. Nieko iš žaidimo čia nėra ir niekas neplatinama: jokių žaidimo išteklių, jokio žaidimo kodo, jokių DLL; Oodle įkeliamas iš jūsų pačių diegimo. Tai, ką jis įrašo, lieka jūsų kompiuteryje: **niekada neskelbkite lygių**.

3DHeat nėra susijęs su Gaijin Entertainment ir nėra jos patvirtintas. War Thunder ir susiję pavadinimai bei prekių ženklai priklauso jų savininkams.

Teisių turėtojai: sukurkite issue adresu <https://github.com/Holdi601/3DHeat-Ext-WarThunder/issues> - atsakome greitai ir paprašius pašaliname bet ką.

## Šaltiniai {#sources}

Visas čia esantis kodas parašytas šiam projektui; joks kodas nenukopijuotas iš kito analizatoriaus.
Tai, ką jis žino apie formatą, kyla iš:

- Gaijin Dagor Engine šaltinio (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` ir `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` esybių srautui (`ecs.py`), ir `net/message.cpp`
  (`MessageClass::initImpl`), kaip esybių pranešimai numeruoja savo klases. Komponentų ir tipų
  vardai atitinkami pagal jų FNV-1a maišas su žaidimo archyvų žodžiais; `ecs.py` išvardija rastus
  vardus.
- To paties šaltinio `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp`
  ir `daNet/bitStream.h`: kaip pranešimas nurodo objektą, kuriam jis skirtas (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md`, ir jo paties analizatorius
  `web/wrpl-parse.js`, skaityti dėl skrydžio modelio, žemės sinchronizavimo, skrendančių ginklų,
  id laukų pranešimų, žaidėjų vietų, kabinos reikšmių ir dvejetainio blk bitų išdėstymo. WTACRP
  kaip savo nuorodas nurodo maxsupermanhd/wrpl-inspector, wt_blk ir wrpl-acmi (AGPL-3.0); jų kodas
  čia neskaitytas.
- Autoriaus paties įrašai, skaityti kaip failai: 2025 metų skirtumai (senesnis skrydžio modelio
  išdėstymas, pokalbis be vėliavėlės baito, zlib), žemės orientacija, supakuotas aukščio poslinkis,
  ginklų paleidimo taškai ir kabinos prietaisai buvo išsiaiškinti čia, remiantis jais.

## Testai {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # also checks the public 2025 sample replays
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # steps, identities, AI flags, roll sign, the smoother, names
```

Vienetų testai niekada neskaito diegimo (nustatytas `HEAT3D_WT_NO_NAMES`); testas su jūsų
paties įrašais vardus skaito iš jūsų diegimo.

Testai sukuria įrašus kode (`tests/synth.py`: antraštė, paketai, rezultatai, esybių srautas,
skrendantys ginklai) pagal išdėstymą, kurį aprašo skaitytuvai; joks įrašas saugykloje nėra.

## Licencija {#licence}

MIT - žr. [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Naudojami pyarrow (Apache-2.0),
numpy (BSD-3-Clause), zstandard (BSD-3-Clause) ir Pillow (MIT-CMU). Lygių skaitytuvai parašyti pagal
Dagor Engine šaltinį, Copyright (c) 2023 Gaijin Entertainment, BSD 3-Clause licencija; jo kodas čia
nekopijuotas, o naudojamos formato konstantos (vromfs XOR raktas, aukščio diapazono tinklelio
poslinkiai) nurodytos ten, kur jos atsiranda.

---

Dalis [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Šaltinis: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
