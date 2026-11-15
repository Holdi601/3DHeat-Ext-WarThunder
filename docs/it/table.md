---
title: "La tabella"
nav_order: 6
lang: "it"
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# La tabella {#the-table}

![La tabella di un replay sintetico, riassunta](../assets/img/table.svg)

Una riga per campione o evento, 105 colonne ([Elenco delle colonne](../columns.md), generato dal codice); nel piè di pagina, sotto `heat3d`, le istruzioni di lettura per il visualizzatore, così il visualizzatore non ha bisogno di nessun modulo da compilare.

| Colonna | Cosa |
|---|---|
| `time` | secondi sull'orologio del replay stesso |
| `event` | `position`; le righe di evento stanno sulla traccia nel loro momento (tra due campioni, sulla retta che li unisce); `kill` (sull'assassino), `death` (sulla vittima), `hit_critical` / `hit_severe` (sull'unità colpita), `module_destroyed` (sull'unità), `launch` (sull'unità che ha rilasciato un'arma), `impact` (l'ultimo campione di un'arma quando è stata rimossa subito dopo); `explosion` e `flak` (0xD08E, 0xD01F) nella loro posizione, tipo `effect`, nessuna traccia, con la direzione dell'esplosione dove ne ha una; `shot` (un proiettile che ha colpito, sul tiratore), `gun_shot`, `fire_start`, `fire_stop` (la raffica di un cannone, non un veicolo in fiamme), `fire_on`, `fire_off` (un veicolo in fiamme, vedi [Incendi dei veicoli](hits.md#vehicle-fires)), `reward` (Argento Leoni e punti di ricerca guadagnati, vedi [Economia](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (vedi [Messaggi alle unità](how-it-reads.md#messages-to-units)); `despawn`: l'ultima riga di una traccia la cui unità scompare prima della fine del replay (vedi [Fine di una traccia](ground.md#end-of-a-track)) |
| `track` | ciò che il visualizzatore disegna come un'unica cosa: una vita di un'unità, oppure il volo di un'arma - `<giocatore o veicolo> #<hex>` (il visualizzatore mostra il nome senza la parte `#`) |
| `x`, `y`, `z` | i metri del gioco: x est, y su, z nord (i suggerimenti invertono z, così il nord non viene disegnato a sud) |
| `player` | il nome del giocatore; un'unità IA `<VehicleName> #<uid>` (per esempio `F-15A #204`); `uid <n>` quando nulla la nomina; per un'arma, chi l'ha rilasciata |
| `userId`, `team` | l'id Gaijin del giocatore e la squadra (`1`, `2`) |
| `ai`, `isPlayer` | `ai` vero per ogni unità che nessun account giocatore guida (unità di missione, aerei IA, bersagli di terra, cannoni antiaerei, navi senza giocatore, segnaposto), `isPlayer` il contrario: un giocatore è un'unità la cui entità nomina uno slot giocatore con un id Gaijin. Un'arma ha quelli del suo lanciatore; vuoto quando non è noto |
| `match` | l'id della partita (il `match` del documento della partita), su ogni riga; i suggerimenti lo mappano come sessione, così due replay caricati non uniscono mai le tracce |
| `life` | `uid#n`: la traccia di un'unità, tagliata dove l'uid passa a un'altra unità, l'unità si sposta più in fretta di quanto possa (una rinascita, un riarmo, il gioco che la sposta, il client che corregge un'unità lontana; vedi Teletrasporti in [Come legge un replay](how-it-reads.md#what-is-read-and-the-check)) oppure è a lungo non visto; `w<hex>` il volo di un'arma (`w<hex>#n` dopo un taglio) |
| `uid` | l'id dell'unità nel replay |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (un tram o un vagone ferroviario che il livello colloca, vedi [Unità della scena](objectives.md#scene-units-trams-and-rail-wagons)); armi `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` la telecamera di replay del giocatore che registra (vedi [La telecamera](ground.md#the-camera)) |
| `type` | il tipo proprio del gioco dove i risultati lo nominano (`fighter`, `assault`, `destroyer`, `gun_boat`), altrimenti come `kind` |
| `Vehicle` | l'id del veicolo del gioco (`f_15a`, `germ_flakpz_I_Gepard`), con cui corrispondono le figure del visualizzatore |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | il nome inglese del veicolo dalla localizzazione della tua installazione (`Pz.Kpfw. III Ausf. J1`, breve `Pz.III J1`) e la sua chiave (`germ_pzkpfw_III_ausf_J_0`); i marchi di paese del carattere del gioco sono esclusi. Dove il gioco non nomina nulla, o non si trova alcuna installazione, il nome è l'id e la chiave vuota |
| `mission` | il nome dell'unità nella missione (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | dove punta l'unità (il vettore di vista): gli aerei dall'assetto del modello di volo, le unità di terra e le navi dal proprio, le armi lungo il loro volo |
| `heading`, `pitch`, `roll` | lo stesso in gradi; il rilevamento è la bussola, in senso orario dal nord, il beccheggio positivo con il muso in su, il rollio positivo con l'ala destra in basso (il modello di volo invia il segno opposto, vedi [Assetto, verificato](aircraft.md#attitude-checked); un'unità di terra con il lato destro in basso). I suggerimenti lo dicono sotto `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | la torretta principale di un carro - dove punta il cannone, non dove guarda il suo giocatore; il valore del replay tenuto alla velocità del comando della torretta e impostato sulla linea di ogni colpo del cannone principale (vedi [Torrette](ground.md#turrets)): la sua imbardata rispetto allo scafo (gradi, in senso orario visto dall'alto positivo, 0 dritto davanti) e il beccheggio del suo cannone rispetto allo scafo (gradi, positivo verso l'alto); `turrets` ogni torretta del veicolo come `yaw pitch;yaw pitch;...` nel suo ordine (uno slot non usato legge `0.00 0.00`). Carri, SPAA, APC e camion, nei replay del client e del server; non le navi (vedi [Torrette](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | la torretta principale come la invia il replay; `turretYaw` / `gunPitch` sono quelli tenuti alla velocità del comando della torretta e impostati sulla linea di ogni colpo del cannone principale (vedi [Torrette](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | dove guarda il giocatore (mira con la telecamera) nel mondo: gradi di bussola (0 nord, in senso orario) e gradi in alto, la stessa convenzione di `aimHeading` / `aimPitch` (a differenza di `turretYaw` / `gunPitch`, che restano relativi allo scafo). Il carro di ogni giocatore in un replay del server, quello del giocatore che registra nel replay del client; vuoto dove il giocatore non mira da nessuna parte (tutti e quattro i valori di mira a 0). La torretta lo segue alla propria velocità di brandeggio, quindi i due differiscono mentre ruota (vedi [Torrette](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | il carro del giocatore che registra: dove mira (gradi di bussola, gradi in alto, la distanza in m; 2000 quando nulla è nel mirino); righe della telecamera: dove mira il giocatore (rilevamento, beccheggio) |
| `zoom` | righe della telecamera: l'ingrandimento della telecamera (vedi [La telecamera](ground.md#the-camera)) |
| `difficulty`, `gameMode` | le `AB`, `RB` o `SB` della battaglia, e `ground`, `air` o `naval`, su ogni riga (vedi [Modalità di battaglia](ground.md#battle-mode)) |
| `extrapolated` | un campione di aereo che è la stima della posizione del client, non uno stato ricevuto (vedi [Stima della posizione](aircraft.md#dead-reckoning-and-the-smoother)); un campione di bomba calcolato dal suo rilascio (vedi Bombe senza record di volo in [Come legge un replay](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | di quanto lo smussamento ha spostato il campione (m), e la posizione e l'assetto propri del replay (il rollio con il segno della tabella) |
| `targetX`, `targetY`, `targetZ` | il punto di colpo di un `shot` |
| `hitOutcome`, `hitFlags` | l'esito di un `shot` su un'unità di terra: `kill`, `critical`, `penetration` o `nonpenetration` (rimbalzato o fermato: il replay non distingue un rimbalzo), dai bit che il server invia con il colpo (`hitFlags`, grezzi); vuoto dove non ne viene inviato nessuno (aerei, navi). Vedi [Esiti dei colpi](hits.md#hit-outcomes) |
| `hitShell` | la firma del proiettile di un `shot`: quattro byte del messaggio di colpo (esadecimale grezzo); una firma può valere per proiettili diversi (120 e 125 mm APFSDS ne condividono una), quindi viene conservata grezza, non letta come calibro |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | le munizioni di un `shot`: il suo tipo (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) e id (`125mm_3bm46`) dove un'uccisione nomina lo slot del tiratore, altrimenti `explosive` (la raffica del colpo) o `kinetic`; il `weapon/slot` del cannone dai suoi ricaricamenti; il calibro in mm dai file delle armi dell'installazione. Vedi [Esiti dei colpi](hits.md#hit-outcomes) |
| `rpm` | i giri del motore di un aereo (la media dei suoi motori) come inviati per ultimi, entro 2 s |
| `vx`, `vy`, `vz` | la velocità di un aereo come la invia la sua voce di volo (m/s, gli assi del gioco; le velocità sopra 500 m/s leggono 500) |
| `engine`, `afterburner`, `engineCondition` | i motori di un aereo dalla sua voce di volo: `off`, `starting`, `running`, `dead` (uniti da `/` quando i suoi motori differiscono); il postbruciatore 0-1; un byte inviato solo dopo che il motore è stato colpito |
| `weaponName` | uccisioni e morti: l'arma o la munizione nell'inglese della tua installazione (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | solo l'aereo del giocatore che registra: il gas 0-1,1 dalla sua cabina (1,1 potenza di emergenza di guerra o postbruciatore; altrimenti i quindicesimi della sua voce di volo), i comandi -1..1 dalla sua voce di volo (equilibratore positivo in tiro, alettone positivo che rolla a destra), i colpi rimasti per arma (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | solo l'aereo del giocatore che registra, dalla sua cabina: velocità indicata e velocità di salita (m/s), carburante, pressione del collettore (atm), carrello (0-1, 1 abbassato), temperatura dell'olio e della testa dei cilindri, dove la sua cabina ha lo strumento |
| `speed` | m/s su circa due secondi della traccia (calcolato qui; il replay non invia velocità per le altre unità) |
| `alive` | 0 per i campioni di un'unità dopo la sua morte (il suo relitto): quello di un'unità di terra o di una nave finché il gioco non la rimuove o i suoi campioni finiscono, quello di un aereo per al massimo 60 s |
| `otherVehicle`, `otherLife` | la vittima di un `shot`: il suo veicolo e la sua `life` |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | il punto di colpo di un `shot` nel sistema proprio della vittima (m; x avanti, y su, z sinistra; vedi [Messaggi alle unità](how-it-reads.md#messages-to-units)) e la direzione da cui è arrivato il colpo, ruotata in quel sistema dall'assetto della vittima in quel momento |
| `hitPart`, `hitFlag` | il messaggio di colpo di un `shot`: la sua parola di parte come inviata, e il suo byte alto |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | quanto è costata e quanto ha reso la battaglia, e chi ha vinto: vedi [Economia](economy.md) |
| `other`, `weapon` | uccisioni: l'altra parte e l'arma; colpi: chi ha colpito (dall'uid del record, altrimenti dallo slot giocatore), il loro veicolo; lanci: l'arma; moduli distrutti: chi ha colpito l'unità per ultimo entro i 5 s precedenti, e `part <n>` |

---

Parte di [3DHeat](https://github.com/Holdi601/3DHeat) ([documentazione](https://holdi601.github.io/3DHeat/)). Fonte: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
