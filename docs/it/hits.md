---
title: "Colpi, fuoco sparato e incendi"
nav_order: 13
lang: "it"
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Colpi, fuoco sparato e incendi {#hits-gunfire-and-fires}

Per chi vuole sapere da dove vengono le colonne di colpi, munizioni e incendi. I controlli danno solo il metodo e l'accordo.

## Fuoco sparato {#gunfire}

Ogni proiettile che ha colpito un'unità è nel replay (messaggio 0xF0E9): una riga `shot` nella posizione del tiratore nel momento del colpo, `targetX/Y/Z` il punto colpito (l'unità colpita, spostata dal punto di colpo nel suo sistema, ruotata dal suo assetto), la direzione verso di essa, `other` l'unità colpita. Proiettili e pallottole che hanno mancato non vengono inviati: non sono entità, e i messaggi delle armi in volo contengono solo razzi, missili, bombe e siluri. I colpi rimasti del giocatore che registra (la sua colonna `ammo`) calano mentre spara, quindi le sue raffiche si possono distinguere, ma non dove sono andati quei colpi. L'antiaerea pesante e l'artiglieria inviano ogni singolo colpo (`gun_shot`, senza direzione), i cannoni antiaerei da 40 mm le loro raffiche (`fire_start`, `fire_stop`).

## Esiti dei colpi {#hit-outcomes}

Con ogni colpo di proiettile su un'unità di terra il server invia il messaggio 0xF144 (UnitOnHit) all'unità: quattro campi di un byte, il quarto con i bit di ciò che il colpo ha fatto (`selfCheck.unitMessages.outcome_*`):

| Bit | Significato | Prova |
|---|---|---|
| 0x20 | il colpo stesso del proiettile | quasi tutti arrivano con un colpo 0xF0E9 sull'unità entro 5 ms; senza di esso, con un'esplosione (spruzzo) |
| 0x01 | è passato (perforazione) | ogni messaggio con 0x02, 0x04 o 0x08 ce l'ha anche lui |
| 0x02 | colpo critico | la maggior parte dei record di colpo critico ce l'ha, molto più spesso del caso |
| 0x04 | distrutto | la maggior parte arriva con un record di uccisione e la morte dell'unità entro un secondo |
| 0x08 | danno pesante | alcuni record di colpo critico ce l'hanno; altrimenti raramente |

`hitOutcome` prende il peggiore: `kill` (0x04), `critical` (0x02 o 0x08), `penetration` (0x01), `nonpenetration` (0x20 da solo). Un colpo viene abbinato al 0xF144 non abbinato più vicino con 0x20 sulla sua unità entro 5 ms. La telecamera del colpo del gioco distingue un rimbalzo da una non-perforazione, ma nessun bit o campo trovato qui lo fa: i primi tre byte variano da colpo a colpo e non sono noti. I replay del client inviano 0xF144 solo per il proprio aereo del giocatore che registra, con tutti i bit a zero: i colpi su aerei e navi non hanno esito.

## Munizioni {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Esplosiva o no.** Un proiettile che esplode invia 0xF133 (UnitOnExplosion) con l'uid del tiratore e il numero del colpo; un colpo con esso è `explosive`, gli altri `kinetic`.
* **Il cannone e il suo slot.** 0xF0BD (UnitBulletRearm) è il colpo successivo caricato: l'indice dell'arma nella lista armi del veicolo, lo slot di munizione e i colpi rimasti. Quello di un caricatore manuale arriva un tempo di ricarica costante dopo ciascuno dei suoi colpi, quello di un cannone automatico una frazione di secondo dopo. I colpi di un tiratore vengono raggruppati per veicolo, firma e raffica; un gruppo appartiene a un'arma quando quell'arma carica un colpo entro 20 s dopo metà dei suoi colpi o più, con un ritardo costante. `ammoSlot` è `weapon/slot`, lo slot caricato prima del colpo: probabilmente quello sparato, a meno che il giocatore non abbia cambiato munizione nel frattempo. Le mitragliatrici non inviano 0xF0BD.
* **Il proiettile.** L'arma di un'uccisione è l'id del proiettile (`125mm_3bm46`); l'ultimo colpo dell'assassino sulla vittima lo assegna allo slot di quel tiratore, dove il calibro del cannone corrisponde. Il suo tipo e calibro sono quelli del file dell'arma (`bulletName`, `bulletType`, `caliber`; `apds_fs_*` APFSDS, `heat_fs_*` HEAT-FS, `he_*` HE ...).
* **Il calibro** del resto: quello dell'arma di uno slot; per un gruppo di mitragliatrici l'unico calibro di mitragliatrice che la sua firma può avere; altrimenti quello del cannone principale del veicolo. Senza l'installazione (`--game`) non c'è tipo, nome o calibro oltre a `explosive` / `kinetic`.

Non trovato: il rimbalzo. Diversi altri messaggi portano il tiratore e il numero del colpo (0xF0C2, probabilmente il percorso della telecamera del colpo attraverso il veicolo; 0xF117, 0xF13C, 0xF13E); sono conservati nel file accessorio, non decodificati. Un colpo non perforante resta `nonpenetration`.

## Incendi dei veicoli {#vehicle-fires}

Un veicolo in fiamme è mostrato a ogni client: il server invia un messaggio di entità al veicolo (evento `0a519c58`) con l'elenco degli incendi che bruciano su di esso, ogni volta che l'elenco cambia. Per incendio: due id a 16 bit (il secondo un nodo del modello di danno), il suo tipo, e -1 finché l'incendio non attecchisce. Un incendio acceso da un colpo riceve anche un messaggio con il punto in cui brucia, nel sistema del veicolo (x avanti, y su, z sinistra).

Righe: `fire_on` quando un incendio compare nell'elenco, `fire_off` quando non c'è più, sul veicolo, con `fireId` (`first:node`), `fireKind` e, per gli incendi accesi da un colpo, `fireLocalX/Y/Z` (avanti, su, destra). Una volta morto un veicolo, il suo elenco spesso non viene più inviato: i suoi incendi finiscono con il suo relitto, altrimenti con la sua entità, altrimenti con il replay (`selfCheck.fires`).

Verificato: ogni volta che il numero di estintori di un carro è diminuito, un incendio è uscito dal suo elenco entro una frazione di secondo; la maggior parte dei punti di incendio si trova dallo stesso lato del veicolo del colpo che lo ha acceso. I tipi sono numeri; non si sa cosa indichino, né quale parte sia un nodo. Gli aerei non inviano un elenco del genere: un aereo in fiamme non viene letto.

---

Parte di [3DHeat](https://github.com/Holdi601/3DHeat) ([documentazione](https://holdi601.github.io/3DHeat/)). Fonte: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
