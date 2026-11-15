---
title: "Come legge un replay"
nav_order: 10
lang: "it"
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Come legge un replay {#how-it-reads-a-replay}

Questa pagina è per chi vuole sapere cosa legge il convertitore, come è stata verificata la lettura, e quindi quanto fidarsi di ogni colonna. Non ti serve per convertire i replay.

La lettura è stata verificata su replay del client di battaglie arcade aeree, simulatore aereo e navali, su replay di server di battaglie di terra e, per i layout del 2025, sui replay di esempio pubblici di
[wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder).
Ogni controllo confronta un valore con qualcosa che il replay dice in un secondo modo, indipendente; qui sono dati solo il metodo e l'accordo.

## Cosa viene letto, e il controllo {#what-is-read-and-the-check}

| Parte | Stato, e il controllo |
|---|---|
| Intestazione, mappa, missione, ora di inizio, sessione; risultati | ogni file |
| Impostazioni della missione (il blk dopo l'intestazione) | modalità, meteo, limiti, `stars` (data, ora, luogo) |
| Flusso dei pacchetti (zlib nel 2025, zstd nel 2026) | ogni pacchetto incorniciato |
| Posizioni e assetto degli aerei (layout 2026) | 4 campioni al secondo, nessun pacchetto lasciato non letto; il rilevamento concorda con la direzione di marcia |
| Pacchetti di volo in anticipo sul loro tempo | dopo un intoppo di rete, il pacchetto di volo di un replay del client a volte contiene ogni altro aereo dove sarà circa 0,75 s dopo. L'anticipo viene misurato per pacchetto, e a ogni aereo che è in anticipo viene assegnato il tempo che rappresenta (`selfCheck.flightPacketsRetimed`) |
| Scatti della stima della posizione (dead reckoning) | un salto da una corsa stimata viene misurato dall'ultimo stato ricevuto, così le correzioni del client non tagliano più le tracce ([Stima della posizione](aircraft.md#dead-reckoning-and-the-smoother)) |
| Teletrasporti | una traccia viene tagliata dove la sua unità si sposta più di quanto possa: prima rispetto al suo tipo (aereo 750 m/s, terra e navi 40 m/s, armi 1800 m/s), poi rispetto al proprio passo. Ogni taglio è elencato in `trackBreaks` con la sua probabile causa (rinascita, il gioco che sposta il giocatore, una correzione di un'unità lontana). Dopo i tagli, nessun passo tra le righe di una traccia è più veloce di quanto il suo tipo consenta (`selfCheck.stepSpeed`) |
| Posizioni di terra e navi (0xF073 / 0xF074) | nessun pacchetto lasciato non letto. Rilevamento, beccheggio e rollio dall'assetto a 16 bit: il rilevamento concorda con la direzione di marcia entro circa 2 gradi (mediana); il beccheggio conta 180/65536 gradi a passo; con il segno del rollio girato, la direzione del cannone dallo scafo e dalla torretta punta all'unità colpita per quasi ogni colpo di carro. Le navi stanno al livello dell'acqua |
| Torrette | imbardata della torretta e beccheggio del cannone dei carri: vedi [Torrette](ground.md#turrets) |
| Altezze di terra compresse | le posizioni compresse in 64 bit contano la loro altezza da -100 m sulla maggior parte dei livelli e dal livello dell'acqua su alcuni; lo scostamento viene misurato su ogni replay dalle unità viste in entrambe le forme (`selfCheck.packedGroundHeight`) |
| Flusso delle entità (creazione, distruzione) | ogni creazione letta. Il layout viene dal codice sorgente pubblicato del Dagor Engine; i tipi di componente propri di War Thunder vengono saltati trovando dove inizia il componente successivo. Il veicolo e lo slot giocatore di ogni unità coincidono con quelli che i record di uccisione e di colpo nominano, per ogni record controllato |
| Chi guidava quale unità, unità IA, navi, bersagli di terra | dal flusso delle entità: ogni unità ha il suo veicolo e la sua squadra, l'unità di ogni giocatore il suo giocatore |
| Uccisioni rispetto ai risultati | le morti per giocatore sono uguali a quelle dei risultati; i risultati contano più uccisioni, perché il client non riceve ogni uccisione. Un replay che inizia dopo l'inizio della battaglia contiene solo le uccisioni successive a quel momento |
| Uccisioni, colpi critici, danno grave | ogni file |
| Moduli distrutti (0xF118) | l'unità e il numero della parte; il nome della parte richiede il modello di danno del veicolo, che non è nel replay |
| Armi rilasciate (flusso delle entità) | il punto di rilascio è a circa 10-20 m (mediana) dall'unità più vicina, che viene presa come lanciatore |
| Armi in volo (0xF0DB) | missili, razzi e bombe, ciascuno collegato alla sua entità |
| Bombe senza record di volo | una bomba senza di essi ha la sua caduta calcolata dal rilascio all'impatto (gravità e resistenza, un campione ogni 0,1 s, `extrapolated` vero). Verificato sul mare, dove l'altezza d'impatto è nota: le cadute calcolate finiscono entro circa 15 m dall'acqua. Nel documento della partita un'arma così ha `ballisticImpact`; `counts.bombsBallistic` le conta |
| Slot dei giocatori, chat | ogni file |
| Esplosioni, scoppi della contraerea, premi, rilevamenti, meteo, oggetti della missione | letti; posizioni controllate a occhio nel visualizzatore |
| Gli strumenti del giocatore che registra (0xD04A) | nominati in base a ciò che fanno: [Strumenti di cabina](aircraft.md#cockpit-instruments); il resto sotto `notNamed` |
| Altri campi delle voci di volo | velocità, colpi, comandi, motori: [Voci di volo](aircraft.md#flight-entries) |
| Assetto nelle righe di evento | ogni riga di evento porta il rilevamento, il beccheggio, il rollio e il vettore di vista della sua unità in quel momento |
| Statistiche dei giocatori e punteggi di squadra | alla fine della battaglia ogni statistica è uguale a quella dei risultati per ogni giocatore: [Dati di riflessione](aircraft.md#reflection-data) |
| Nomi di armi e veicoli | dalla localizzazione inglese della tua installazione; alcune cinture predefinite di navi e radar di aeroporto non hanno nome nel gioco |
| Giocatori e IA | nessuna riga di un giocatore dei risultati è IA, ogni riga non IA è un giocatore dei risultati (`selfCheck.identity`) |
| Relitti | i campioni di un'unità dopo la sua morte continuano ad arrivare; il relitto di un'unità di terra o di una nave è `alive` 0 finché la sua entità non viene rimossa, e resta una sola traccia; gli aerei mantengono `alive` 0 per al massimo 60 s (`selfCheck.wrecks`) |
| Cambi di veicolo | un'unità del giocatore ancora viva quando compare la prossima unità dello stesso giocatore viene chiusa lì (un veicolo lasciato in piedi). `selfCheck.vehicleSwitch.twoLiveVehicles` deve essere 0 |
| Modalità di battaglia | [Modalità di battaglia](ground.md#battle-mode) |
| Aerei in un replay di server del 2026 | letti nel layout 2026; il rilevamento e il segno del rollio concordano con le virate; gli aerei segnaposto e i droni di ricognizione non portano dati |
| Giocatori di un replay di server | trovati per nome negli slot; ogni statistica è uguale a quella dei risultati (`selfCheck.players`) |
| Aerei nei replay di server del 2025 e nella versione 101286 | non letti: i loro pacchetti di volo hanno un layout diverso |

## Messaggi alle unità {#messages-to-units}

Ogni pacchetto di tipo 4 è un messaggio mpi del daNet del Dagor Engine: l'id dell'oggetto destinatario, poi (quando i suoi 11 bit bassi sono tutti a uno) l'UID esteso dell'oggetto, l'id del messaggio e il carico. Un messaggio a un'unità porta come UID esteso l'id dell'entità dell'unità, `index << 10 | generation`. Verificato: ogni messaggio così nomina un'entità viva in quel momento.

Per gli specialisti, i messaggi letti:

| Messaggio | Cosa, e il controllo |
|---|---|
| 0xF0E9 UnitHitEffects | il colpo di un proiettile: l'uid del tiratore e il punto di colpo nel sistema dell'unità (x avanti, y su, z sinistra): centimetri su aerei e navi, 20/32768 m a passo su unità di terra (adattato alla dimensione delle torrette dei carri). `hitLocalX/Y/Z` in metri. Diventa una riga `shot` ([Fuoco sparato](hits.md#gunfire)). Il tiratore di quasi ogni record di colpo e di uccisione è tra questi; i punti di colpo stanno dal lato rivolto al tiratore |
| 0xF133 UnitOnExplosion | lo stesso uid del tiratore |
| 0xF04B OnUnitDead | righe `dead`: il bersaglio di ogni record di uccisione ne ha una entro 2 s |
| 0xD047 FmwRpm | i giri dei motori (`rpm`); concorda con l'indicatore dei giri della cabina |
| 0xF0B1, 0xF0A0 | righe `gun_shot`: colpi singoli dell'antiaerea pesante e dell'artiglieria |
| 0xF01B, 0xF01C | righe `fire_start`, `fire_stop`: raffiche dei cannoni antiaerei da 40 mm (un cannone che spara; un incendio su un veicolo è `fire_on`, vedi [Incendi dei veicoli](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | righe `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` |
| 0xD0FE ProjectileHitReplay | i colpi del giocatore che registra e quelli che subisce, con arma e munizione, nominati dall'installazione (`projectileHitReplays`) |
| 0xF13E, 0xF031 | l'effetto visivo di un colpo e un effetto riprodotto sull'unità; arrivano con un colpo sulla stessa unità |
| 0xD041 | uno per ogni cannone difensivo di un aereo, due volte al secondo; i suoi indici corrispondono ai cannonieri del modello di volo |
| 0xD048, 0xF117 | layout letto, significato non noto |
| il resto (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | nel file accessorio dei messaggi con la loro unità e i loro campi |

I nomi sono quelli della comunità (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Letto anche {#also-read}

- **Replicazione dal flusso delle entità** (0x22, 0x23): per entità un blocco di valori di componente: timer di riparazione delle navi, conteggi dei consumabili, cambi di proprietario e squadra, surriscaldamento del motore. Contati in `counts.replicatedComponents`; i valori nel file accessorio dei messaggi.
- **Azioni dello script di missione** (0xF028) e **suggerimenti** (0xF0EC): `triggers`, `hints`. **Avanzamento della missione** (0xF07A, 0xF07C): `missionProgress`.
- **La telecamera di replay** (0xD043): vedi [La telecamera](ground.md#the-camera).

## Non letto, e perché {#not-read-and-why}

- **Nomi e corpi dei messaggi di entità** (0x20, 0x21): il numero di classe è un posto in un elenco compilato nel gioco, non inviato e non nei suoi dati. Due vengono letti (gli incendi di un veicolo e i suoi estintori); il resto viene conservato intero con la sua entità e il numero di classe.
- **Altri oggetti replicati** (tipi diversi da slot dei giocatori e squadre): letti e conservati, non nominati; nei risultati non c'è nulla con cui verificarli.
- **Comandi, gas e colpi degli altri aerei**: aggiornati solo ogni tanto; conservati nel file accessorio di volo, non nella tabella.
- **Incendi degli aerei**: non trovati in nessun messaggio; un aereo in fiamme non ha una riga `fire_on`.
- **Nomi delle armi rilasciate**: l'entità di una bomba o di un razzo non contiene un nome; i record di uccisione nominano l'arma di un'uccisione.
- **Colpi andati a vuoto**: un replay contiene solo i colpi andati a segno.

I `counts.messageIdsNotRead` e il `selfCheck` di ogni documento della partita dicono cosa contiene un nuovo replay e quanto bene è stato letto.

---

Parte di [3DHeat](https://github.com/Holdi601/3DHeat) ([documentazione](https://holdi601.github.io/3DHeat/)). Fonte: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
