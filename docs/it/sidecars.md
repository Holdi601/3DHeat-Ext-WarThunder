---
title: "File accessori e completezza"
nav_order: 8
lang: it
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# File accessori e completezza {#sidecars-and-completeness}

Nulla di un replay viene buttato via. Ciò che il convertitore legge va nella tabella e nel documento della partita; tutto il resto viene conservato intero in tre
file accessori accanto alla tabella (dentro il file `.3dheat`, oppure separati con
`--loose`). Questa è la regola che condividono tutti i convertitori 3DHeat:
[I convertitori conservano tutto](https://holdi601.github.io/3DHeat/converters.html).

## I file accessori {#the-sidecars}

- `<match>.messages.parquet`: ogni messaggio a un'unità (tempo, id e nome del messaggio, uid, eid, modello, veicolo, i suoi campi id in esadecimale, `decoded` (ciò che ne viene letto, come JSON), il carico), ogni valore di componente replicato (`name` il componente, `fields` il suo valore), ogni messaggio di entità (con il suo numero di entità e di classe), ogni oggetto replicato (`ReflectionData
  <kind>/<index>`, i suoi campi in esadecimale) e ogni pacchetto che nessun lettore qui prende, intero.
- `<match>.objectives.parquet`: le zone di cattura nel tempo, una riga per
  cambiamento inviato dal server: `time`, `event` (`state`, `progress`, `captured`,
  `neutralised`), `zone` (la sua lettera), `zoneId`, `object`, `owner` (0 nessuno,
  1, 2), `progress` (-100..100, positivo verso la squadra 2), le `x`,
  `y`, `z` della zona, e tutti i `fields` dell'oggetto in esadecimale (vedi
  [Obiettivi](objectives.md)).
- `<match>.flight.parquet`: ogni voce del modello di volo di ogni aereo, intera (i suoi bit, e `phase`: il bit del primo byte da cui è iniziata), con la sua velocità, i 14 nibble di comando (`control1-3`, `throttle`), i suoi motori
  con il loro stato, postbruciatore e condizione, e i suoi colpi per arma
  (`ammo`; `numbers` è l'intera lista). I valori degli altri aerei sono quelli dell'ultimo aggiornamento.

## Cosa garantiscono i conteggi {#what-the-counts-guarantee}

I `counts` del documento della partita dicono cosa conteneva il replay e che fine ha fatto:

| Chiave | Cosa |
|---|---|
| `packets`, `unreadPackets` | ogni tipo di pacchetto incontrato, e quelli che nessun lettore prende (conservati interi nel file accessorio dei messaggi) |
| `messageIds`, `messageIdsNotRead` | ogni id di messaggio incontrato e quante volte, e quelli solo conservati, non letti |
| `replicatedComponents`, `replicatedNotRead` | valori di componente letti, e quelli solo conservati |
| `entities`, `entityTemplates`, `entityMessages` | cosa ha creato e inviato il flusso delle entità |
| `droppedSamples` | campioni lasciati fuori di proposito (il relitto di un'unità di terra dopo che la sua entità è sparita), per motivo |

Nient'altro viene lasciato fuori: un elemento del replay è o letto nella
tabella o nel documento della partita, oppure conservato intero in un file accessorio. Il
`selfCheck` del documento della partita contiene le verifiche di ciò che è stato letto
([Come legge un replay](how-it-reads.md)).

---

Parte di [3DHeat](https://github.com/Holdi601/3DHeat) ([documentazione](https://holdi601.github.io/3DHeat/)). Fonte: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
