---
title: "Aerei"
nav_order: 11
lang: it
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Aerei {#aircraft}

Per chi vuole sapere da dove vengono le colonne degli aerei e quanto fidarsi di loro. Ogni controllo qui sotto confronta un valore con qualcosa che il replay dice in un secondo modo, indipendente; sono dati solo il metodo e l'accordo.

## Strumenti di cabina {#cockpit-instruments}

Il messaggio 0xD04A invia gli indicatori della cabina del giocatore che registra come coppie (numero, valore): quattro al secondo nelle battaglie arcade, solo i valori cambiati nelle battaglie simulatore. I numeri formano un'unica lista per tutte le cabine, e una cabina invia gli indicatori che il suo modello possiede. Il codice del gioco stabilisce quale numero è quale indicatore, quindi ogni numero è stato nominato in base a ciò che fa e verificato con il replay (`convert.INSTRUMENTS` contiene il risultato; nulla viene letto dall'installazione):

| Numero | Nome | Verificato con |
|---|---|---|
| 0 | velocità indicata, m/s | la velocità della traccia corretta per la densità dell'aria: correlazione 0,99 |
| 39 | velocità di salita, m/s | la velocità di salita della traccia: correlazione sopra 0,99 |
| 40, 41 | altitudine, m; altitudine modulo 1000 | l'altezza della traccia, a pochi metri di differenza |
| 52, 53 | rollio e beccheggio dell'orizzonte artificiale | meno il rollio e il beccheggio della tabella, a meno di 1 grado di differenza |
| 64 | bussola | il rilevamento della tabella, a meno di 0,1 grado di differenza |
| 15-20 | pedali del timone | la forza laterale sull'aereo |
| 23, 31 | barra: equilibratore e alettoni (segno come nel modello di cabina) | l'angolo di attacco; la velocità di rollio |
| 69, 71, 73 | orologio: ore (quadrante a 12 ore), minuti, secondi | l'ora locale del computer di registrazione, al minuto |
| 75 | pressione del collettore, atm | più alta con la potenza di emergenza di guerra che a tutto gas |
| 81-86, 87-92, 93-98 | giri per motore, giri modulo 1000, indicatore dei giri | tra loro esattamente; i giri del motore: correlazione sopra 0,97 |
| 195 | carburante | cala durante una sortita, di nuovo pieno a ogni rinascita |
| 228-230 | gambe del carrello, 1 abbassato | abbassato solo vicino all'altezza degli aeroporti e alla velocità di atterraggio |
| 240, 241 | gas per motore (1,1 potenza di emergenza di guerra o postbruciatore) | il gas della voce di volo |
| 330-332, 346-348 | contatori delle munizioni (due serie uguali) | i colpi della preselezione dell'armamento, che calano con i colpi della voce di volo |
| 135, 159 | temperatura dell'olio e della testa dei cilindri | probabile: salgono durante una sortita |
| 58, 61 | pallina di scivolamento, ago di virata | probabile: seguono la forza laterale e la velocità di virata |
| 223 | aerofreno | probabile: impostato solo in avvicinamento |
| 490-497, 500-505 | freni delle ruote | probabile: impostati solo da fermi su un aeroporto |

Vengono inviati anche alcuni altri numeri il cui significato non è noto; sono conservati nel
`authorInstruments.notNamed` del documento della partita.

`ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` e `throttle` della tabella derivano da questi, sulle righe del giocatore che registra, prendendo l'ultimo messaggio al massimo 0,2 s dopo il campione.

## Voci di volo {#flight-entries}

La voce di volo di ogni aereo (tipo di pacchetto 2) porta, oltre alla posizione e all'assetto:

- **Velocità**: una parola a 32 bit dopo l'assetto. I bit 31, 30 e 29 sono i segni di x, y e z; poi la velocità in 11 bit di 500/2047 m/s (si ferma a 500 m/s), poi |x| e |y| come frazioni della velocità in 9 bit ciascuno, e z è ciò che rende il vettore un vettore unitario. Verificato con il passo tra campioni ricevuti: la direzione concorda entro una frazione di grado per il giocatore che registra e entro circa 2 gradi per tutti gli altri; la velocità entro lo 0,2 %. `selfCheck.flightEntries`.
- **Colpi per arma**: una lista prima della posizione, un elemento per arma, prima i colpi rimasti. Quella del giocatore che registra è uguale ai contatori della cabina un tick dopo, per quasi ogni campione.
- **Comandi e gas**: 7 byte dopo la velocità, letti come 14 nibble. Per il giocatore che registra, a ogni tick: 1 l'equilibratore, 2 gli alettoni, 3 il timone (8 a riposo), 11 il gas in quindicesimi (15 anche per la potenza di emergenza di guerra e il postbruciatore), 4 i freni delle ruote, 5 l'aerofreno, 8 probabilmente il paracadute di frenata. I nibble degli altri aerei cambiano solo poche volte in una battaglia e non sono i loro comandi in quel momento.
- **Motori**: per motore un byte di stato (0 spento; 1-6 in avviamento; 7 in funzione; 8 morto), un valore a 16 bit solo con il postbruciatore (32767 pieno), e un byte solo dopo che il motore è stato colpito. La maggior parte degli aerei il cui motore diventa "morto" viene abbattuta o finisce entro pochi minuti.

## Dati di riflessione {#reflection-data}

I messaggi 0xF02D e 0xF0AA replicano gli oggetti numerati del gioco: per oggetto il suo id (i 5 bit alti il tipo, gli 11 bassi un indice) e una tabella di campi. Il tipo 14 sono gli slot dei giocatori (campo 2 id utente e nome, 9 la squadra), il tipo 15 le squadre (indice 1 e 2):

- Il campo 39 di uno slot contiene le sue statistiche in posizioni fisse: abbattimenti (offset 0), abbattimenti di squadra (2), morti (4), abbattimenti navali (10), abbattimenti di IA (12), abbattimenti di IA a terra (14), assistenze (20), zone di cattura (22), danno alle zone (24, 32 bit), premio per il danno (40, 32 bit), evasioni di missili (50). Il campo 38 inizia con il punteggio, il campo 42 è la squadra di appartenenza. Alla fine di una battaglia ogni valore è uguale a quello dei risultati per ogni giocatore (`selfCheck.scoreboardVsResults`). Non si sa dove siano conservati gli abbattimenti a terra.
- Il campo 7 di una squadra è il suo punteggio: alla fine è uguale alla somma dei punteggi dei suoi giocatori nei risultati. Il campo 3 sono probabilmente i suoi biglietti.
- Ogni messaggio invia solo i campi cambiati, quindi `scoreboard` nel documento della partita elenca le statistiche di ogni giocatore e il punteggio di ogni squadra a ogni cambiamento.

## Stima della posizione (dead reckoning) e lo smussamento {#dead-reckoning-and-the-smoother}

Un replay del client registra ogni aereo quattro volte al secondo, come il client lo disegnava. Tra un aggiornamento e l'altro che riceve per un aereo lontano, il client lo sposta avanti lungo l'ultima velocità e lo fa girare secondo gli ultimi tassi, e al successivo aggiornamento lo rimette lì di colpo. Letta così com'è, una traccia va dritta, poi salta. Nulla nella voce di volo indica quali campioni sono stati ricevuti; un campione stimato si riconosce da ciò che è: prosegue la retta dei due campioni precedenti, alla loro stessa velocità, entro 3 cm.

Quanto conta dipende dalla battaglia: nelle battaglie arcade circa la metà dei campioni degli altri aerei può essere stimata, nelle battaglie simulatore solo qualche percento. Lo smussamento riduce di circa cinque volte i salti superiori a 15 g (`selfCheck.deadReckoning`). L'aereo del giocatore che registra non viene estrapolato dal client e resta com'è.

Per impostazione predefinita (`--no-smoothing` lo disattiva) le tracce di tutte le unità tranne quella del giocatore che registra vengono messe dove gli stati ricevuti dicono che fossero: un campione stimato va su una curva che passa per i campioni ricevuti prima e dopo, ciascuno con la propria velocità; oltre i 3 s la retta viene solo piegata verso il campione ricevuto successivo, così nessun campione si sposta più dello scatto del client stesso. L'assetto viene fatto ruotare in modo uniforme da un assetto ricevuto al successivo. I campioni ricevuti vengono lisciati di al massimo 2 m o 0,04 s della loro velocità; una virata costante resta com'è. I valori propri del replay restano nelle colonne `Raw`.

## Assetto, verificato {#attitude-checked}

Sull'aereo del giocatore che registra, il rilevamento sta entro un grado (mediana) della direzione di marcia, il beccheggio entro pochi gradi dell'angolo di salita, e nelle virate nette il rollio ha il segno della virata per quasi ogni campione: il rollio del modello di volo è ala sinistra in basso positivo, e la tabella lo converte in ala destra in basso positiva (`selfCheck.aircraftAttitude`). Gli angoli a 10 bit cambiano a passi di 0,18 gradi. L'assetto delle unità a terra viene verificato sui loro colpi ([Torrette](ground.md#turrets)).

---

Parte di [3DHeat](https://github.com/Holdi601/3DHeat) ([documentazione](https://holdi601.github.io/3DHeat/)). Fonte: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
