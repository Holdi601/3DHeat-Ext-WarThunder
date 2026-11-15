---
title: Objectius
nav_order: 15
lang: ca
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Objectius {#objectives}

`objectives` al document de partida llista el que es disputa a la batalla, de dues fonts (`source`):

- **La repetició** (`replay`): els objectes de missió que nomena 0xD039 (zones de captura `cz_circle_NN`,
  aeròdroms, helipunts, bases), col·locats on els objectes replicats de tipus 3 (0xF02D) els posen ara: una
  zona de captura comença al lloc de la seva plantilla i es mou a la zona d'aquest mode a l'inici (`moved`).
  Els números del tipus 3 segueixen l'ordre de 0xD039; cada objecte que no es mou està exactament on el té
  0xD039, cosa que comprova l'ordre. Una zona de captura rep la forma i el radi de l'àrea de la missió al seu
  lloc (`area`, dins de 2 m) i la seva lletra segons el seu propi índex (camp 69 del tipus 5: 0 = A); l'ordre
  de lletres és el de la repetició, no es comprova amb el mapa del joc.
- **La missió** (`mission`): el fitxer de missió `<missió>.blk` del teu `mis.vromfs.bin` i les plantilles que
  importa (només lectura, en el moment de la conversió): les seves àrees, classificades pel nom: apareixements
  (els punts numerats d'un apareixement `..._spawnareaNN` com un sol apareixement `points`), àrees de batalla,
  objectius de bombardeig (`bomb_zone`), punts d'aparició de convois (`road_NN_spawn`), àrees de sortida i de
  mort. Les àrees d'un altre mode del mateix mapa (`conq_`, `dom_`, `bttl_`, ...) es deixen fora, i de les
  variants `_arcade` / `_realistic` / `_hardcore` es pren la de la pròpia batalla (RB pren `_realistic`, si no
  `_hardcore`, com fan els guions de la missió); també es deixen fora els marcadors d'informació, els punts de
  canons antiaeris i les àrees de més de 5 km (on estan escampats els apareixements). Cada apareixement indica
  quantes trajectòries de jugadors hi van començar (`used`, `usedByTeam`). Una missió pot intercanviar els seus
  bàndols a l'atzar (`randomSpawnTeams`): quan els apareixements mostren que els equips de la repetició van
  al revés, cada `team` s'intercanvia i el bàndol del nom es guarda com a `missionTeam`. Les rutes dels convois
  no són als punts de pas de les missions tal com es llegeixen; només s'indica on apareixen els convois.

Les zones de captura al llarg del temps són el fitxer annex `<partida>.objectives.parquet`: els objectes
replicats de tipus 5, un per zona: camp 2 el seu propietari (0, 1, 2), camp 67 el seu progrés de captura, un
byte amb signe de -100 a 100 (positiu cap a l'equip 2), camp 69 el seu índex. Comprovat
(`selfCheck.objectives`) a les repeticions de servidor terrestres de batalles de Conquesta i de Dominació:
cada canvi de propietari va acompanyat d'un jugador de l'equip que captura que guanya una `captureZone` al
marcador en el mateix moment (dins d'1,5 s) i d'una unitat terrestre viva d'aquell equip dins la zona; els
apareixements de cada batalla mostren els equips de la repetició només en una direcció (sovint al revés
respecte als `t1_` / `t2_` de la missió).

## Unitats d'escena: tramvies i vagons de tren {#scene-units-trams-and-rail-wagons}

Un nivell pot col·locar unitats pròpies: les entitats `unit_loader+rail_wagon` d'una repetició de servidor són
els tramvies del fitxer d'escena del nivell (`gamedata/scenes/<nivell>_objects.blk` a `aces.vromfs.bin`:
`setting__unit_class`, la seva transformació i `setting__isDead`). Les seves entitats no porten cap uid
llegible, de manera que una trajectòria terrestre sense entitat d'unitat, la primera mostra de la qual és dins
de 2 m d'una unitat d'escena, és aquella unitat: la seva classe com a `Vehicle`, tipus `train`, tipus `tram`,
`locomotive` o `wagon`, sense equip; una unitat que l'escena col·loca morta (com els tramvies cremats) és una
resta (`alive` 0) des de la seva primera fila. El joc no té un nom en anglès per a ells; `VehicleName` és
l'identificador llegit com a paraules («Railway tram A»). Les seves posicions no tremolen: gairebé totes no es
mouen mai (cada mostra igual, fins al bit). La repetició els envia unes deu vegades per segon igualment, de
manera que de les seves mostres només es guarden les que els mouen (0,05 m o 0,1 graus), i una cada 10 s
(`selfCheck.sceneUnits` compta les mostres descartades). Abans, eren trajectòries amb el nom `uid 8` i sense
vehicle.

---

Part de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentació](https://holdi601.github.io/3DHeat/)). Font: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
