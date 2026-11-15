---
title: "Condizioni e licenza"
nav_order: 16
lang: it
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# Condizioni e licenza {#terms-and-licence}

## Le condizioni {#the-terms}

Condizioni di servizio di Gaijin (aggiornate il 2026-08-17), EULA (Allegato 2):
3.2.2 "modify, translate, create derivative works of, reverse engineer,
disassemble, or decompile the Game(s)" (modificare, tradurre, creare opere derivate, eseguire il reverse engineering,
smontare o decompilare il/i Gioco/i), 3.2.9 "mine or collect any data from
the Game(s) that is not intended to be publicly displayed" (estrarre o raccogliere dati dal/dai Gioco/i che non sono destinati
a essere mostrati pubblicamente); 1.2 "are not
permitted to store, download, modify, or otherwise use any part of the Game(s)"
(non è consentito memorizzare, scaricare, modificare o in altro modo usare alcuna parte del/dei Gioco/i)
oltre il client. Leggere i file dei livelli della propria copia del gioco in una vista 3D locale è una
decisione dell'utente, presa sapendolo. I livelli scritti restano sul tuo computer: **non pubblicarli mai**, e nulla qui distribuisce dati del gioco.

## Fonti {#sources}

Tutto il codice qui è scritto per questo progetto; nessun codice è stato copiato da un altro parser. Ciò che
sa del formato viene da:

- Il codice sorgente del Dagor Engine di Gaijin (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` e `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` per il flusso delle entità (`ecs.py`), e `net/message.cpp`
  (`MessageClass::initImpl`) per come i messaggi di entità numerano le loro classi. I nomi di componenti e tipi sono abbinati
  per i loro hash FNV-1a alle parole degli archivi del gioco; `ecs.py` elenca i nomi trovati.
- Lo stesso codice sorgente `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp`
  e `daNet/bitStream.h`: come un messaggio indica l'oggetto a cui è destinato
  (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md`, e il suo parser
  `web/wrpl-parse.js`, letti per i layout dei bit del modello di volo, sincronizzazione di terra, armi in volo, messaggi con campi id, slot dei giocatori, i valori di cabina
  e il blk binario. WTACRP cita come propri riferimenti maxsupermanhd/wrpl-inspector,
  wt_blk e wrpl-acmi (AGPL-3.0); il loro codice non è stato letto qui.
- I replay dell'autore, letti come file: le differenze del 2025 (il vecchio layout del modello di volo, chat senza byte di flag, zlib), l'assetto di terra, lo
  scostamento dell'altezza compresso, i punti di rilascio delle armi e gli strumenti di cabina sono stati ricavati su di essi qui.

## Test {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<cartella con i replay di esempio> python -m pytest -q   # verifica anche i replay di esempio pubblici del 2025
HEAT3D_WT_REPLAYS=<cartella dei tuoi replay> python -m pytest -q        # passi, identità, flag IA, segno del rollio, lo smussamento, nomi
```

I test unitari non leggono mai un'installazione (`HEAT3D_WT_NO_NAMES` è impostato); il test
con i tuoi replay legge i nomi dalla tua installazione.

I test costruiscono i replay nel codice (`tests/synth.py`: intestazione, pacchetti, risultati,
il flusso delle entità, armi in volo) con il layout che descrivono i lettori; nessun replay è nel repository.

## Licenza {#licence}

MIT - vedi [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Usa pyarrow (Apache-2.0), numpy (BSD-3-Clause),
zstandard (BSD-3-Clause) e Pillow (MIT-CMU). I lettori dei livelli sono stati scritti
a partire dal codice sorgente del Dagor Engine, Copyright (c) 2023 Gaijin Entertainment, licenza BSD
3-Clause; nessun suo codice è copiato qui, e le costanti di formato usate
(la chiave XOR dei vromfs, gli scostamenti della griglia degli intervalli di altezza) sono citate dove compaiono.

---

Parte di [3DHeat](https://github.com/Holdi601/3DHeat) ([documentazione](https://holdi601.github.io/3DHeat/)). Fonte: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
