---
title: "Economia"
nav_order: 14
lang: it
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Economia {#economy}

Quanto è costata e quanto ha reso la battaglia, come colonne sulle sue righe di evento, lette dalla **tua installazione al momento della conversione** (`char.vromfs.bin`: `config/wpcost.blk` per veicolo, `config/warpoints.blk` e `config/rank.blk`; i blk delle armi di `aces.vromfs.bin` dicono quale modifica è ogni proiettile). Nessun numero del gioco è in questo repository: i valori finiscono solo nel tuo output. Senza il `char.vromfs.bin` dell'installazione non viene scritta alcuna economia (`economy.available` falso). I prezzi sono quelli della difficoltà della battaglia (`repairCostHistorical` per RB, `...Arcade` per AB, `...Simulation` per SB).

| Colonna | Righe | Cosa |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (un colpo preso dopo uno sparo, veicoli di terra), `launch` (aerei, elicotteri) | costo in SL del colpo, razzo, missile o bomba |
| `cost_lost_sl` | `death` del veicolo di un giocatore | il costo di riparazione del veicolo (di serie; quello completamente potenziato nel blk) |
| `earn_sl`, `earn_rp` | `reward` (nuovo evento, nel luogo e nel tempo di chi ha guadagnato) | SL e RP guadagnati |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | ogni riga con un `cost_*` o `earn_sl` | `SL` (`earn_rp` sono punti di ricerca) |
| `econ_basis` | lo stesso | `install` (un prezzo letto dall'installazione) o `inferred` (calcolato, vedi sotto) |

**Chi ha vinto.** `won` (0/1) su ogni riga di una squadra, dove il replay lo dice: i risultati di un replay
del client portano l'esito dell'autore (`status`: `success` o `fail`), quindi la squadra dell'autore ha vinto
o perso e l'altra squadra il contrario; `result` nel documento della partita
dice quale (`winner`, `status`, `authorTeam`). I replay dei server e i replay interrotti prima della
fine non portano alcun esito (lo `status` di un replay del server è sempre `success` e non nomina l'autore),
e nessuno dei due tipi contiene le modifiche installate: i risultati elencano i veicoli di ogni giocatore
solo per nome e tipo. In questi casi `won` resta vuoto.

Il modello dei costi del visualizzatore legge le colonne `cost_*` (e `earn_*`) con `currency`; sommando `cost_fired_sl +
cost_lost_sl` si ottiene dove sono stati spesi e persi gli Argento Leoni, `earn_sl` dove sono stati guadagnati (il premio di un'uccisione è
sulla sua riga `reward`, non sulla riga `kill`, così nulla viene contato due volte).

- **Colpi** (`install` dove il proiettile dello slot è noto - un'uccisione l'ha nominato, vedi [Esiti dei colpi](hits.md#hit-outcomes) -
  altrimenti `inferred`: il prezzo medio dei proiettili che quel cannone può sparare su quel veicolo; un proiettile di serie è gratuito; le
  mitragliatrici non vengono contate dal replay e non costano nulla).
- **Lanci** (`inferred`): il gioco prezza la preselezione d'armamento di un aereo per sortita, non per oggetto; un oggetto è la
  mediana delle preselezioni prezzate del veicolo, prezzo / oggetti (`sum_weapons`, contromisure e serbatoi sganciabili esclusi);
  0 dove le sue preselezioni sono gratuite.
- **Premi** (tutti `inferred`): il replay non contiene alcun record di premio - il blocco dei risultati ha solo punteggi e conteggi,
  nessun messaggio porta Argento Leoni (verificato su replay del client e del server). Un `kill` guadagna `aKill` x il
  `rewardMul<mode>` dell'assassino x il peso della classe della vittima (`units` in warpoints.blk, tramite il suo `unitClass`; per le unità IA
  il loro tipo) x `aiKillK` per una vittima IA x `groundKillMul` per un aereo che uccide un'unità di terra; RP allo stesso modo con
  `expMul` e i pesi di rank.blk. Ogni altro passo del punteggio di un giocatore nel tabellone replicato è un premio
  che vale i suoi punti agli SL per punto della battaglia (gli SL di un'uccisione sui punti mediani dei passi delle uccisioni, il
  `pointsPerKill` del blocco); il suo tipo è il contatore che è salito con esso (assistenze, zone catturate, danno alle zone,
  premio per il danno, evasioni di missili), altrimenti il colpo critico o grave di quel giocatore entro 3 s, altrimenti un
  rilevamento dell'unità del giocatore entro 2 s (`scouting`), altrimenti `other`. `battle_end` è `winK` (vinta) o `defeatK` (persa) dei
  guadagni in battaglia del giocatore, il vincitore dai biglietti rimasti alle squadre, poi dal punteggio. Il tempo premium, i potenziatori,
  l'equipaggio e le modifiche non sono noti e non vengono applicati; i budget di uccisione delle battaglie di terra
  (`def_ground_kill_wp_budget*`) non sono modellati.

L'`economy` del documento della partita (e, in un container `.3dheat`, `extensions["heat3d/economy"]` del manifesto)
contiene `currency` `SL`, `researchCurrency` `RP`, `difficulty`, `totals` (`firedSl`, `lostSl`, `earnedSl`,
`earnedRp`), `players` (lo stesso per giocatore, con `netSl`), `vehicles` (per veicolo di ogni giocatore: `repairSl`,
`repairFullUpgradedSl`, `purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`, `rewardMul`, `expMul`,
`groundKillMul`, `battleTimeAwardSl`, `rank`, `economicRank`, `unitClass`), `multipliers` (`aKill`, `aiKillK`,
`winK`, `defeatK`, `wpMultiplier`), `winnerTeam`, `pointsPerKill` e `check` (quante righe di ogni tipo sono state
prezzate, stimate o non prezzate).

---

Parte di [3DHeat](https://github.com/Holdi601/3DHeat) ([documentazione](https://holdi601.github.io/3DHeat/)). Fonte: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
