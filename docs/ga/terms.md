---
title: Téarmaí agus ceadúnas
nav_order: 16
lang: ga
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# Téarmaí agus ceadúnas {#terms-and-licence}

## Na téarmaí {#the-terms}

Téarmaí Seirbhíse Gaijin (nuashonraithe 2026-08-17), EULA (Iarscríbhinn 2): 3.2.2 "modify, translate, create derivative works of, reverse engineer, disassemble, or decompile the Game(s)", 3.2.9 "mine or collect any data from the Game(s) that is not intended to be publicly displayed"; 1.2 "are not permitted to store, download, modify, or otherwise use any part of the Game(s)" lasmuigh den chliant. Is cinneadh an úsáideora é comhaid leibhéil do chóipe féin a léamh isteach i radharc 3T áitiúil, a ghlactar agus fios aige é seo. Fanann na leibhéil a scríobhtar ar do mheaisín: **ná foilsigh choíche iad**, agus ní sheolann aon rud anseo aon sonraí cluiche.

## Foinsí {#sources}

Scríobhadh an cód ar fad anseo don tionscadal seo; níor cóipeáladh aon chód ó pharsálaí eile. An méid atá ar eolas aige faoin bhformáid, tagann sé ó:

- Foinse Dagor Engine de chuid Gaijin (github.com/GaijinEntertainment/DagorEngine, BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`, `object.cpp`, `serialize.cpp`, `compression.h` agus `prog/engine/daECS/core/baseIo.cpp`, `componentTypes.cpp` don sruth eintiteas (`ecs.py`), agus `net/message.cpp` (`MessageClass::initImpl`) maidir leis an gcaoi a n-uimhríonn teachtaireachtaí eintitis a ranganna. Meaitseáiltear ainmneacha comhpháirteanna agus cineálacha lena hashanna FNV-1a i gcoinne focal i gcartlanna féin an chluiche; liostaíonn `ecs.py` na hainmneacha a fuarthas.
- `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp` agus `daNet/bitStream.h` den fhoinse chéanna: conas a ainmníonn teachtaireacht an réad dá bhfuil sí (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`, `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md`, agus a pharsálaí féin `web/wrpl-parse.js`, léite le haghaidh leaganacha amach bhiteanna an mhúnla eitilte, sioncronú talún, airm ag eitilt, teachtaireachtaí réimsí id, sliotáin imreoirí, luachanna cábáin agus an blk dénártha. Ainmníonn WTACRP maxsupermanhd/wrpl-inspector, wt_blk agus wrpl-acmi (AGPL-3.0) mar a thagairtí féin; níor léadh a gcód anseo.
- Athsheinmeanna an údair féin, léite mar chomhaid: oibríodh amach orthu anseo difríochtaí 2025 (leagan amach níos sine an mhúnla eitilte, comhrá gan beart bratach, zlib), dearcadh na talún, an fhritháireamh airde pacáilte, pointí scaoilte na n-arm agus uirlisí an chábáin.

## Tástálacha {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # also checks the public 2025 sample replays
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # steps, identities, AI flags, roll sign, the smoother, names
```

Ní léann na tástálacha aonaid suiteáil riamh (socraítear `HEAT3D_WT_NO_NAMES`); léann an tástáil le d'athsheinmeanna féin na hainmneacha ó do shuiteáil.

Tógann na tástálacha athsheinmeanna sa chód (`tests/synth.py`: ceanntásc, paicéid, torthaí, an sruth eintiteas, airm ag eitilt) de réir an leagan amach a dhoiciméadaíonn na léitheoirí; níl aon athsheinm sa stóras.

## Ceadúnas {#licence}

MIT - féach [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Úsáideann sé pyarrow (Apache-2.0), numpy (BSD-3-Clause), zstandard (BSD-3-Clause) agus Pillow (MIT-CMU). Scríobhadh léitheoirí na leibhéal ó fhoinse Dagor Engine, Copyright (c) 2023 Gaijin Entertainment, ceadúnas BSD 3-Clause; níor cóipeáladh aon chód de anseo, agus luaitear na tairisigh fhormáide a úsáidtear (eochair XOR vromfs, fritháireamh greille raon airde) san áit a bhfuil siad le feiceáil.

---

Cuid de [3DHeat](https://github.com/Holdi601/3DHeat) ([doiciméadúchán](https://holdi601.github.io/3DHeat/)). Foinse: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
