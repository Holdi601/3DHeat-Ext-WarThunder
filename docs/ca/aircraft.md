---
title: Avions
nav_order: 11
lang: "ca"
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Avions {#aircraft}

Per a qui vol saber d'on venen les columnes dels avions i com de fiable és cadascuna. Cada
comprovació de sota compara un valor amb una altra cosa que la repetició diu d'una segona
manera independent; aquí només es donen el mètode i l'acord.

## Instruments de cabina {#cockpit-instruments}

El missatge 0xD04A envia els indicadors del jugador que grava com a parells (número, valor):
quatre per segon en batalles arcade, només els valors canviats en batalles de simulador. Els
números formen una sola llista per a totes les cabines, i una cabina envia els indicadors que
té el seu model. El codi del joc fixa quin número és quin indicador, de manera que cada número
s'ha nomenat per allò que fa i s'ha comprovat amb la repetició (`convert.INSTRUMENTS` guarda el
resultat; no es llegeix res de la instal·lació):

| Número | Nom | Comprovat amb |
|---|---|---|
| 0 | velocitat indicada de l'aire, m/s | la velocitat de la trajectòria corregida per la densitat de l'aire: correlació 0,99 |
| 39 | velocitat de pujada, m/s | la velocitat de pujada de la trajectòria: correlació per sobre de 0,99 |
| 40, 41 | altitud, m; altitud mòdul 1000 | l'alçada de la trajectòria, a pocs metres de diferència |
| 52, 53 | roll i pitch de l'horitzó artificial | menys el roll i pitch de la taula, a menys de 1 grau de diferència |
| 64 | brúixola | el heading de la taula, a menys de 0,1 grau de diferència |
| 15-20 | pedals del timó | la força lateral sobre l'avió |
| 23, 31 | palanca: elevador i alerons (signe com el del model de cabina) | l'angle d'atac; la velocitat de roll |
| 69, 71, 73 | rellotge: hores (esfera de 12 hores), minuts, segons | l'hora local de l'ordinador de gravació, al minut |
| 75 | pressió del col·lector, atm | més alta a la potència d'emergència de guerra que a l'accelerador màxim |
| 81-86, 87-92, 93-98 | rpm per motor, rpm mòdul 1000, indicador de rpm | entre ells exactament; les rpm del motor: correlació per sobre de 0,97 |
| 195 | combustible | baixa al llarg d'una sortida, plena de nou en reaparèixer |
| 228-230 | les cames del tren d'aterratge, 1 baixat | baixat només a prop de l'alçada dels aeròdroms i a la velocitat d'aterratge |
| 240, 241 | accelerador per motor (1.1 potència d'emergència de guerra o postcombustor) | l'accelerador de l'entrada de vol |
| 330-332, 346-348 | comptadors de munició (dos conjunts iguals) | les rondes del preajust d'armes, que baixen amb les rondes de l'entrada de vol |
| 135, 159 | temperatura de l'oli i del cap de cilindres | probable: pugen al llarg d'una sortida |
| 58, 61 | bola de lliscament, agulla de gir | probable: segueixen la força lateral i la velocitat de gir |
| 223 | aerofrè | probable: només activat durant l'aproximació |
| 490-497, 500-505 | frens de roda | probable: només activats quan està aturat en un aeròdrom |

Encara s'envien alguns números més el significat dels quals no es coneix; es guarden a
`authorInstruments.notNamed` del document de partida.

Les columnes `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`,
`headTemperature` i `throttle` de la taula surten d'aquests, a les files del propi jugador que
grava, agafant l'últim missatge com a molt 0,2 s després de la mostra.

## Entrades de vol {#flight-entries}

L'entrada de vol de cada avió (tipus de paquet 2) porta, a més de la seva posició i actitud:

- **Velocitat**: una paraula de 32 bits després de l'actitud. Els bits 31, 30 i 29 són els
  signes de x, y i z; després la velocitat en 11 bits de 500/2047 m/s (s'atura als 500 m/s), i
  després |x| i |y| com a fraccions de la velocitat en 9 bits cadascun, i z és el que fa que el
  vector sigui un vector unitari. Comprovat amb el pas entre mostres rebudes: la direcció
  coincideix dins d'una fracció de grau per al jugador que grava i dins d'uns 2 graus per a la
  resta; la velocitat, dins del 0,2 %. `selfCheck.flightEntries`.
- **Rondes per arma**: una llista abans de la posició, un element per arma, primer les rondes que
  queden. Les del jugador que grava són iguals als comptadors de la cabina un tick després per a
  gairebé totes les mostres.
- **Comandaments i accelerador**: 7 bytes després de la velocitat, llegits com 14 quartets. Per al
  jugador que grava, a cada tick: 1 l'elevador, 2 els alerons, 3 el timó (8 en repòs), 11 l'accelerador
  en quinzenes (15 també per a la potència d'emergència de guerra i el postcombustor), 4 els frens de
  roda, 5 l'aerofrè, 8 probablement el paracaigudes de frenada. Els quartets dels altres avions canvien
  només algunes vegades en una batalla i no són els seus comandaments en aquell moment.
- **Motors**: per motor, un byte d'estat (0 apagat; 1-6 arrancant; 7 en marxa; 8 mort), un valor de 16
  bits només amb postcombustor (32767 a ple), i un byte només després que el motor rebi un impacte. La
  majoria dels avions el motor dels quals passa a «mort» són abatuts o acaben en pocs minuts.

## Dades de reflexió {#reflection-data}

Els missatges 0xF02D i 0xF0AA repliquen els objectes numerats del joc: per objecte, el seu
identificador (els 5 bits alts el tipus, els 11 baixos un índex) i una taula de camps. El tipus 14
són les ranures de jugador (camp 2 l'identificador d'usuari i el nom, 9 l'equip), el tipus 15 els
equips (índex 1 i 2):

- El camp 39 d'una ranura conté les seves estadístiques en llocs fixos: morts (desplaçament 0),
  morts d'equip (2), morts pròpies (4), morts navals (10), morts a la IA (12), morts a terra a la IA
  (14), assistències (20), zones de captura (22), dany a zones (24, de 32 bits), premi per dany (40,
  de 32 bits), evasions de míssils (50). El camp 38 comença amb la puntuació, el camp 42 és
  l'esquadra. Al final d'una batalla cada valor és igual al dels resultats per a cada jugador
  (`selfCheck.scoreboardVsResults`). On es guarden les morts a terra no es coneix.
- El camp 7 d'un equip és la seva puntuació: al final és igual a la suma de les puntuacions dels seus
  jugadors als resultats. El camp 3 probablement són els seus tiquets.
- Cada missatge només envia els camps que han canviat, de manera que `scoreboard` al document de
  partida llista les estadístiques de cada jugador i la puntuació de cada equip a cada canvi.

## Estimació per navegació i l'alisador {#dead-reckoning-and-the-smoother}

Una repetició de client grava cada avió quatre cops per segon, tal com el client el va dibuixar.
Entre les actualitzacions que rep per a un avió llunyà, el client el mou seguint la seva última
velocitat i el fa girar a les seves últimes velocitats de gir, i a l'actualització següent el
salta a la posició real. Llegida tal com és, una trajectòria va recta i després salta. La
entrada de vol no marca quines mostres s'han rebut; una mostra estimada per navegació es troba
pel que és: continua la línia recta de les dues mostres anteriors, al seu ritme, dins de 3 cm.

Quant importa això depèn de la batalla: en batalles arcade, uns la meitat de les mostres dels
altres avions es poden estimar per navegació; en batalles de simulador, només un parell de
percentatges. L'alisador redueix els salts per sobre de 15 g unes cinc vegades (`selfCheck.deadReckoning`).
L'avió propi del jugador que grava no l'extrapola el client i es deixa tal com és.

Per defecte (`--no-smoothing` ho desactiva) les trajectòries de totes les unitats excepte les del
jugador que grava es col·loquen on diuen els estats rebuts que eren: una mostra estimada per
navegació va en una corba que passa per les mostres rebudes abans i després, cadascuna amb la seva
pròpia velocitat; després de més de 3 s la línia recta només es corba cap a la següent mostra rebuda,
de manera que cap mostra no es mou més enllà del salt propi del client. La seva actitud es gira
uniformement d'una actitud rebuda a la següent. Les mostres rebudes s'alisen com a màxim 2 m o 0,04 s
de la seva velocitat; un gir constant es queda tal com és. Els valors propis de la repetició es
mantenen a les columnes `Raw`.

## Actitud, comprovada {#attitude-checked}

Al propi avió del jugador que grava, el heading està dins d'un grau (mediana) de la direcció de
moviment, el pitch dins de pocs graus de l'angle de pujada, i en girs clars el roll té el signe del
gir per a gairebé cada mostra: el roll del model de vol és positiu amb l'ala esquerra avall, i la
taula el gira perquè sigui positiu amb l'ala dreta avall (`selfCheck.aircraftAttitude`). Els angles
de 10 bits avancen de 0,18 graus. L'actitud de les unitats terrestres es comprova amb els seus trets
([Torretes](ground.md#turrets)).

---

Part de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentació](https://holdi601.github.io/3DHeat/)). Font: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
