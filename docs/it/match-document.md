---
title: "Il documento della partita"
nav_order: 7
lang: it
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# Il documento della partita {#the-match-document}

![L'inizio di un documento di partita sintetico, e le sue chiavi](../assets/img/match-document.svg)

`<match>.match.json` contiene tutto ciò che il replay dice e che non è una riga della tabella. La scheda Partita del
visualizzatore lo legge.

## La battaglia {#the-battle}

| Chiave | Cosa |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | l'id della partita (come nel nome del file); l'id della mappa; il file del livello che usa |
| `mission`, `missionKey` | il nome della missione e la sua chiave nei file di testo del gioco |
| `battleClass`, `environment`, `weather` | come li dà l'intestazione |
| `sessionId`, `server` | l'id di sessione della battaglia; il server |
| `replayVersion`, `flightLayout` | la versione del formato del replay; il layout dei pacchetti di volo letto (`2025` o `2026`) |
| `files` | i file di replay letti (uno, oppure le parti di un replay del server) |
| `started`, `timePlayed`, `replayEnd` | ora di inizio (ISO, UTC); secondi giocati, dai risultati; secondi dell'ultimo pacchetto del replay |
| `author`, `authorUserId` | il giocatore che registra e il suo id Gaijin (replay del client) |
| `teams` | le squadre della battaglia (`1`, `2`) |
| `result` | `winner`, `status` (`success` o `fail`, l'esito dell'autore), `authorTeam`, `teams` ([Economia](economy.md)) |
| `vehicleNames` | da dove vengono i nomi dei veicoli (la tua installazione) e la loro lingua |
| `conventions` | le unità e i segni della tabella: assi, tempo, vita, traccia, vivo, rollio, e altro |

## Tutto il resto {#everything-else}

| Chiave | Cosa |
|---|---|
| `battle`, `difficulty`, `gameMode` | la modalità di battaglia: `difficulty` `AB` / `RB` / `SB` (e il suo nome, e il byte dell'intestazione), `gameMode` `ground` / `air` / `naval`, la modalità della missione (`Dom`, `Conq`, `Bttl`, `I2M`, ...) e il suo nome inglese dalla tua installazione (`Domination`, `Enduring Confrontation`), i tipi di unità consentiti (vedi [Modalità di battaglia](ground.md#battle-mode)) |
| `settings` | il blk della missione dopo l'intestazione: modalità, ambiente, meteo, limiti di punteggio e tempo, paesi, tipi di unità consentiti, vento, e `stars` (latitudine, longitudine, data, ora locale) |
| `sky` | il primo `CustomWeatherParams`: direzione del sole e della luna, vento, colori del cielo, scostamenti delle nuvole |
| `players`, `slots` | la riga dei risultati per giocatore (uccisioni, uccisioni a terra, morti, assistenze, punteggio, catture, squadra, clan, paese, formazione, gli uid guidati); gli slot dei giocatori del replay (nome, id utente, squadra) |
| `units` | ogni entità unità creata dal replay: eid, uid, modello, veicolo, tipo, squadra, giocatore, nome della missione, quando è stata creata e rimossa, dove è stata creata, quali componenti non si sono potuti leggere |
| `objects` | gli oggetti nominati della missione: zone di cattura e aeroporti con posizione e dimensione, contorni degli aeroporti come punti, aree di comparsa |
| `objectives` | gli obiettivi della battaglia, ciascuno con `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (la 1 o 2 del replay, vuoto per entrambe), `name` (per una zona di cattura la sua lettera, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) con `position`, `radius` / `height` / `size` e `heading`, `source` (`replay` o `mission`) e ciò che altro si conosce (vedi [Obiettivi](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | con nomi e veicoli di entrambe le parti; uccisioni con il nome inglese dell'arma |
| `weapons` | ogni razzo, missile, bomba, siluro, serbatoio sganciabile e carico gettato: quando, dove rilasciato (posizione, assetto, velocità), da quale unità (la più vicina entro 300 m e 1,5 s), quanti campioni di volo, dove visto per l'ultima volta, quando rimosso |
| `explosions`, `flak` | `PlayExplosionVisual` (posizione, direzione, tipo) e `PlayFlakExplosionVisual` (posizione) |
| `awards` | i premi del giocatore che registra (`TextStreak`: first_blood, serie, contatori delle sfide) |
| `detections`, `unitStates` | coppie `UnitDetected` di unità; un messaggio (0xF093) con posizione, assetto e velocità di un'unità il cui significato non è noto |
| `authorInstruments` | i valori di cabina del giocatore che registra (`ReplayCockpitParams`) per numero di strumento, al massimo uno al secondo; `known` nomina ogni numero che questo replay ha inviato (nome, unità, come è stato verificato), `notNamed` il resto |
| `scoreboard` | le statistiche di ogni giocatore ogni volta che sono cambiate (uccisioni, morti, assistenze, punteggio, uccisioni di IA, uccisioni navali, zone, danno, evasioni di missili, squadra), e il punteggio di ogni squadra e i biglietti probabili nel tempo (vedi [Dati di riflessione](aircraft.md#reflection-data)) |
| `economy` | gli Argento Leoni e i punti di ricerca della battaglia (vedi [Economia](economy.md)): totali, per giocatore, per veicolo, i moltiplicatori, il vincitore, i controlli |
| `entityMessages` | i messaggi di entità (0x20) per numero di classe: conteggio, modelli bersaglio, dimensioni |
| `chat` | ogni riga di chat |
| `triggers`, `hints`, `missionProgress` | le azioni dello script di missione (RunTriggerAction), i suoi suggerimenti, i suoi messaggi di avanzamento |
| `camera` | i campi della telecamera di replay del giocatore che registra ogni 0,25 s come inviati (la tabella li ha come traccia) |
| `projectileHitReplays` | i colpi del giocatore che registra e quelli che subisce, con arma e munizione e i loro nomi inglesi |
| `results` | l'intero blk dei risultati così come lo ha scritto il gioco |
| `counts` | righe, eventi, vite, tipi, campioni, entità per modello, armi, pacchetti letti e non letti, ogni id di messaggio visto e quelli non letti, campioni scartati |
| `trackBreaks` | ogni taglio di una traccia per un passo più veloce di quanto l'unità possa andare: dove, di quanto, quanto veloce, e che cosa è più probabile che sia |
| `selfCheck` | i controlli elencati in [Come legge un replay](how-it-reads.md), calcolati a ogni conversione; `stepSpeed` dà per tipo la velocità tra righe consecutive di una traccia come le unisce il visualizzatore (mediana, 99° percentile, massima, e i passi più veloci del possibile, che deve essere 0) |

---

Parte di [3DHeat](https://github.com/Holdi601/3DHeat) ([documentazione](https://holdi601.github.io/3DHeat/)). Fonte: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
