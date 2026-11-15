---
title: "Unità di terra e telecamera"
nav_order: 12
lang: it
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Unità di terra e telecamera {#ground-units-and-camera}

Per chi vuole sapere da dove vengono le colonne di torretta, telecamera e modalità di battaglia, e quanto fidarsi di loro. I controlli danno solo il metodo e l'accordo.

## Torrette {#turrets}

Lo stato di terra di un carro (assetto a 16 bit) contiene, dopo la posizione, 141 bit non letti, poi per ogni torretta 62 bit: l'imbardata della torretta e il beccheggio del cannone (16 bit ciascuno, 360/65536 gradi a passo, con segno) e 30 bit non letti; poi il riempimento, e in alcuni stati altri 200 bit. Il numero di torrette è il byte inviato prima dello stato. Uno stato la cui lunghezza non corrisponde non dà torrette (le unità statiche inviano uno stato più corto). L'imbardata è relativa allo scafo, positiva in senso orario, 0 dritto davanti; il beccheggio è relativo allo scafo, positivo verso l'alto.

Come è stato verificato:

- **Contro i colpi:** per ogni colpo di un carro, la direzione nel mondo del cannone principale (assetto dello scafo ruotato dall'imbardata della torretta e dal beccheggio del cannone) contro la linea dal tiratore all'unità colpita, a non meno di 30 m: per battaglia una mediana di circa il 98 % entro 3 gradi in rilevamento e il 99 % in elevazione (`selfCheck.turretsVsShots`). I restanti sono per lo più colpi di una mitragliatrice in un'altra torretta.
- **Contro la mira del giocatore che registra:** il suo carro invia l'angolo di mira nel mondo (antiorario da est), il beccheggio e la distanza. Il rilevamento dello scafo più l'imbardata della torretta sta entro mezzo grado (mediana) dalla mira.

**I replay dei server** (0xF074) inviano lo stato di ogni carro nello stesso formato, seguito da dati propri, quindi viene letta ogni torretta i cui due angoli stanno dentro lo stato (almeno quella principale per quasi ogni riga di carro). È la torretta, non la telecamera:

- **Contro i colpi**, come sopra: per battaglia oltre il 90 % entro 3 gradi in rilevamento e il 99 % in elevazione.
- **Contro la vista:** un replay del server invia la mira di ogni giocatore (`viewYaw`, `viewPitch`). La torretta segue la vista entro mezzo grado (mediana), ma gira molto più lentamente di quanto la vista oscilla, come fa un comando di torretta (`selfCheck.turretVsView`).
- **Ma non sempre alla velocità di un comando:** campione per campione, il valore così come inviato a volte salta sulla mira quando la mira è vicina al cannone, più in fretta di qualsiasi comando.

Quindi la tabella contiene la torretta **tenuta al proprio comando**: `turretYaw` / `gunPitch` si spostano verso il valore inviato a una velocità non superiore a quella di rotazione del cannone principale dal file del veicolo dell'installazione (moltiplicato per 1,3 per le abilità dell'equipaggio e le modifiche; 45 e 20 gradi al secondo dove l'installazione non ne indica nessuno). A ogni colpo del cannone principale la torretta viene impostata esattamente sulla linea del colpo, e un passaggio all'indietro la porta lì in tempo (`selfCheck.turretLimit`). La riga `shot` contiene anch'essa `turretYaw` / `gunPitch`. Il valore come inviato resta in `turretYawRaw` / `gunPitchRaw`. Un carro il cui stato non contiene torretta ha colonne di torretta vuote (il visualizzatore può ripiegare su `viewYaw`).
`gunPitch` sta un po' sopra `viewPitch` a distanza: l'elevazione del cannone per la caduta del proiettile.

Gli stati delle navi hanno un altro formato; le loro torrette non vengono lette. Gli aerei non inviano direzione della testa o della vista; il messaggio 0xD020 dei cannoni antiaerei resta non letto.

## La telecamera {#the-camera}

Il messaggio 0xD043, circa 20 al secondo, è la telecamera di replay del giocatore che registra: campo 1 un quaternione che ruota l'avanti della telecamera verso dove guarda; 2 il posto della telecamera rispetto al veicolo che segue (m); 4 lo stesso scostamento nel sistema del veicolo (x avanti, y su, z sinistra); 5 dove il giocatore mira (un vettore unitario); 3 lo zoom (circa 1,2 nella vista in terza persona di un carro, circa 1,0 in un aereo, più alto nel mirino di un cannoniere o con il binocolo). Verificato: il campo 4 è il campo 2 ruotato nel sistema del veicolo, entro 0,5 m per quasi ogni messaggio; l'avanti della telecamera ha il rilevamento della mira. Il replay non invia un campo visivo in gradi, solo lo zoom.

La tabella ha la telecamera come traccia propria: tipo `camera`, traccia `<player> camera #ca`, una riga al massimo ogni 0,1 s, nel punto del veicolo seguito più il campo 2, guardando lungo il quaternione (`dirX/Y/Z`, `heading`, `pitch`, `roll`), con `zoom`, `aimHeading` e `aimPitch`, e `otherLife` la vita che segue. `selfCheck.camera` conta le righe e la verifica.

## Fine di una traccia {#end-of-a-track}

Una traccia viene disegnata dalla sua prima riga all'ultima. Quando la sua unità scompare prima della fine del replay, la sua ultima riga è una riga `despawn` nel suo ultimo punto: nel momento in cui il gioco ha rimosso la sua entità (quando questo è avvenuto entro 6 s dal suo ultimo campione), altrimenti al suo ultimo campione. Una traccia senza una di queste righe dura fino alla fine del replay. Le righe di una traccia possono essere lontane tra loro (un'unità lontana o un relitto viene aggiornato ogni pochi secondi, un relitto a volte non per minuti): il suo ultimo stato vale fino alla riga successiva.

## Modalità di battaglia {#battle-mode}

Il byte dell'intestazione all'offset 688 contiene la difficoltà nei suoi quattro bit bassi: 0 arcade (AB), 5 realistica (RB), 10 simulatore (SB). Verificato con i tipi di battaglia noti per i replay. La modalità di gioco è `ground` quando la missione permette di far comparire i carri, altrimenti `naval` quando permette le navi, altrimenti `air` (`allowedUnitTypes`); la modalità propria della missione viene dalla sua chiave (`missions/_Dom`), con il nome preso da `lang/missions_versus.csv` della tua installazione. La stessa chiave è la parte `<mode>` dei nomi dei file e dell'id della partita (`Conq4`, `Dom`), omessa dove l'intestazione non ne ha una.

---

Parte di [3DHeat](https://github.com/Holdi601/3DHeat) ([documentazione](https://holdi601.github.io/3DHeat/)). Fonte: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
