---
title: "Obiettivi"
nav_order: 15
lang: it
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Obiettivi {#objectives}

`objectives` nel documento della partita elenca ciò per cui si combatte la battaglia, da due fonti (`source`):

- **Il replay** (`replay`): gli oggetti di missione che 0xD039 nomina (zone di cattura `cz_circle_NN`, aeroporti, eliporti,
  basi), collocati dove gli oggetti replicati di tipo 3 (0xF02D) li mettono ora - una zona di cattura parte dal posto
  del suo modello e all'inizio viene spostata nella zona di questa modalità (`moved`). I numeri del tipo 3 seguono l'ordine di 0xD039;
  ogni oggetto che non viene spostato si trova esattamente dove lo ha 0xD039, il che verifica l'ordine. Una zona di cattura riceve la
  forma e il raggio dell'area di missione nel suo punto (`area`, entro 2 m) e la sua lettera dal proprio indice (campo 69
  del tipo 5: 0 = A); l'ordine delle lettere è quello del replay, non verificato con la mappa del gioco.
- **La missione** (`mission`): il file di missione `<mission>.blk` nel `mis.vromfs.bin` della tua installazione e i modelli
  che importa (solo lettura, al momento della conversione): le sue aree, classificate per nome - punti di comparsa (i punti numerati
  di una comparsa `..._spawnareaNN` come un'unica comparsa `points`), aree di battaglia, bersagli di bombardamento (`bomb_zone`), punti di
  comparsa delle colonne (`road_NN_spawn`), aree di uscita e di uccisione. Le aree di un'altra modalità della stessa mappa (`conq_`, `dom_`, `bttl_`,
  ...) sono escluse, e tra le varianti `_arcade` / `_realistic` / `_hardcore` quella della battaglia (RB prende
  `_realistic`, altrimenti `_hardcore`, come fanno gli script di missione); lo sono anche i marcatori del briefing, i punti dei cannoni antiaerei e le aree
  più larghe di 5 km (quelle su cui sono sparsi i punti di comparsa). Ogni comparsa indica quante tracce di giocatori
  sono iniziate in essa (`used`, `usedByTeam`). Una missione può scambiare i lati a caso (`randomSpawnTeams`): quando le comparse mostrano
  le squadre del replay al contrario, ogni `team` viene scambiata e il lato del nome viene conservato come `missionTeam`. Le rotte delle colonne
  non sono nei waypoint delle missioni così come letti; si indica solo dove compaiono le colonne.

Le zone di cattura nel tempo sono il file accessorio `<match>.objectives.parquet`: gli oggetti replicati di tipo 5, uno
per zona - campo 2 il suo proprietario (0, 1, 2), campo 67 il suo avanzamento di cattura, un byte con segno da -100 a 100 (positivo
verso la squadra 2), campo 69 il suo indice. Verificato (`selfCheck.objectives`) sui replay di server di terra delle battaglie Conquista e Dominio: ogni cambio di proprietario
arriva con un giocatore della squadra che cattura che guadagna una `captureZone` nel tabellone nello stesso momento (entro
1,5 s) e con un'unità di terra viva di quella squadra dentro la zona; le comparse di ogni battaglia mostrano le squadre
del replay in un solo verso (spesso scambiato rispetto a `t1_` / `t2_` della missione).

## Unità della scena: tram e vagoni ferroviari {#scene-units-trams-and-rail-wagons}

Un livello può collocare unità proprie: le entità `unit_loader+rail_wagon` di un replay di server sono i tram del
file di scena del livello (`gamedata/scenes/<level>_objects.blk` in `aces.vromfs.bin`: `setting__unit_class`, la sua
trasformazione e `setting__isDead`). Le loro entità non portano un uid leggibile, quindi una traccia di terra senza entità unità
il cui primo campione sta entro 2 m da un'unità di scena è quella unità: la sua classe come `Vehicle`, tipo `train`, tipo
`tram`, `locomotive` o `wagon`, nessuna squadra; un'unità che la scena colloca morta (come i tram bruciati) è un relitto (`alive` 0) dalla sua prima riga. Il gioco non ha un nome inglese per loro; `VehicleName` è l'id
letto come parole ("Railway tram A"). Le loro posizioni non oscillano: quasi tutte non si muovono mai (ogni
campione uguale al bit). Il replay le invia comunque una decina di volte al secondo, quindi dei loro campioni si tengono solo quelli che le
muovono (0,05 m o 0,1 gradi), e uno ogni 10 s (`selfCheck.sceneUnits` conta i campioni scartati).
Prima, erano tracce chiamate `uid 8` senza veicolo.

---

Parte di [3DHeat](https://github.com/Holdi601/3DHeat) ([documentazione](https://holdi601.github.io/3DHeat/)). Fonte: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
