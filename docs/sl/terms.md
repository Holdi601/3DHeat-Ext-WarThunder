---
title: Pogoji in licenca
nav_order: 16
lang: "sl"
source: terms.md
source_hash: "01d249aa8f1b"
nav_exclude: true
search_exclude: true
---
# Pogoji in licenca {#terms-and-licence}

## Kaj se bere {#what-it-reads}

Pretvornik bere posnetke, ki jih War Thunder shrani v vaš računalnik (ali posnetke vaših bitk, ki ste jih sami prenesli z warthunder.com), in datoteke ravni iz vaše lastne namestitve War Thunderja. Nič iz igre tu ni vključeno ali naprej razširjano: nobenih sredstev igre, nobene kode igre, nobenih DLL-jev; Oodle se naloži iz vaše lastne namestitve. Kar zapiše, ostane na vašem računalniku: **ravni nikoli ne objavljajte**.

3DHeat ni povezan z družbo Gaijin Entertainment in ga ta ni odobrila. War Thunder ter povezana imena in blagovne znamke pripadajo njihovim lastnikom.

Imetniki pravic: odprite issue na <https://github.com/Holdi601/3DHeat-Ext-WarThunder/issues> - odgovorimo hitro in na zahtevo odstranimo karkoli.

## Viri {#sources}

Vsa koda tukaj je napisana za ta projekt; nobena koda ni bila kopirana iz drugega
razčlenjevalnika. Kar se ve o formatu, izhaja iz:

- Gaijinova izvorna koda Dagor Engine (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` in `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` za tok entitet (`ecs.py`), ter `net/message.cpp`
  (`MessageClass::initImpl`) za to, kako sporočila entitet oštevilčijo razrede. Imena komponent
  in tipov se ujemajo po njihovih zgoščenih vrednostih FNV-1a z besedami iz arhivov same igre;
  `ecs.py` našteva najdena imena.
- Iste izvorne kode `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp`
  in `daNet/bitStream.h`: kako sporočilo navede predmet, za katerega je (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md` in njegov lasten razčlenjevalnik
  `web/wrpl-parse.js`, prebrani za bitne postavitve modela leta, sinhronizacije tal, orožij v
  letu, polj z identifikatorji sporočil, mest igralcev, vrednosti kabine in binarnega blk.
  WTACRP kot svoje reference navaja maxsupermanhd/wrpl-inspector, wt_blk in wrpl-acmi
  (AGPL-3.0); njihova koda tukaj ni bila prebrana.
- Lastni posnetki avtorja, prebrani kot datoteke: razlike iz leta 2025 (starejša postavitev
  modela leta, klepet brez bajta zastavice, zlib), položaj tal, zapakirani odmik višine,
  točke izpusta orožij in kabinski instrumenti so bili tukaj izdelani na njih.

## Testi {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<mapa s posnetki za vzorec> python -m pytest -q   # preveri tudi javne vzorčne posnetke iz leta 2025
HEAT3D_WT_REPLAYS=<mapa vaših posnetkov> python -m pytest -q        # koraki, identitete, zastavice AI, predznak zvitka, zglajevalnik, imena
```

Enotni testi nikoli ne berejo namestitve (`HEAT3D_WT_NO_NAMES` je nastavljen); test z
vašimi posnetki bere imena iz vaše namestitve.

Testi sestavijo posnetke v kodi (`tests/synth.py`: glava, paketi, rezultati, tok entitet,
orožja v letu) po postavitvi, ki jo opisujejo bralniki; v repozitoriju ni nobenega posnetka.

## Licenca {#licence}

MIT - glejte [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Uporablja pyarrow (Apache-2.0), numpy (BSD-3-Clause),
zstandard (BSD-3-Clause) in Pillow (MIT-CMU). Bralniki zemljevidov so bili napisani po
izvorni kodi Dagor Engine, Copyright (c) 2023 Gaijin Entertainment, licenca BSD
3-Clause; nobena njena koda tukaj ni kopirana, uporabljene konstante formata
(ključ XOR za vromfs, odmiki mreže višinskega obsega) pa so navedene tam, kjer se
pojavijo.

---

Del [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Vir: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
