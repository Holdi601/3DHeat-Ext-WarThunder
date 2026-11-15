---
title: Impactes, trets i focs
nav_order: 13
lang: "ca"
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Impactes, trets i focs {#hits-gunfire-and-fires}

Per a qui vol saber d'on venen les columnes d'impacte, munició i foc. Les comprovacions donen només
el mètode i l'acord.

## Trets {#gunfire}

Cada projectil que ha impactat una unitat és a la repetició (missatge 0xF0E9): una fila `shot` a la
posició del tirador en el moment de l'impacte, `targetX/Y/Z` el punt d'impacte (la unitat impactada,
desplaçada pel punt d'impacte en el seu marc, girada per la seva actitud), la direcció cap a ella,
`other` la unitat impactada. Les obusos i bales que han fallat no s'envien: no són entitats, i els
missatges d'armes en vol només porten coets, míssils, bombes i torpedes. Les rondes que queden al
jugador que grava (la seva columna `ammo`) baixen a mesura que dispara, de manera que es poden distingir
les seves ràfegues, però no on van anar aquestes rondes. L'antiaeri pesant i l'artilleria envien cada
tret individual (`gun_shot`, sense direcció), els canons antiaeris de 40 mm les seves ràfegues
(`fire_start`, `fire_stop`).

## Resultats dels impactes {#hit-outcomes}

A cada impacte de projectil sobre una unitat terrestre, el servidor envia el missatge 0xF144 (UnitOnHit)
a la unitat: quatre camps d'un byte, el quart els bits del que ha fet l'impacte
(`selfCheck.unitMessages.outcome_*`):

| Bit | Significat | Evidència |
|---|---|---|
| 0x20 | l'impacte propi d'un projectil | gairebé tots arriben amb un impacte 0xF0E9 a la unitat dins de 5 ms; sense ell, amb una explosió (esquitx) |
| 0x01 | ha travessat (penetració) | cada missatge amb 0x02, 0x04 o 0x08 també el té |
| 0x02 | impacte crític | la majoria dels registres d'impacte crític el tenen, molt més sovint que per atzar |
| 0x04 | destruït | la majoria arriben amb un registre de mort i la mort de la unitat dins d'un segon |
| 0x08 | dany greu | alguns registres d'impacte crític el tenen; rarament en altres casos |

`hitOutcome` pren el pitjor: `kill` (0x04), `critical` (0x02 o 0x08), `penetration` (0x01),
`nonpenetration` (0x20 sol). Un impacte s'aparella amb el 0xF144 amb 0x20 no aparellat més proper a la
seva unitat dins de 5 ms. La càmera d'impacte del joc distingeix un rebot d'una no penetració, però cap
bit ni camp trobat aquí ho fa: els tres primers bytes varien d'impacte a impacte i no se sap què són.
Les repeticions de client només envien 0xF144 per a l'avió propi del jugador que grava, tots els bits
a zero: els impactes sobre avions i vaixells no tenen resultat.

## Munició {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Explosiva o no.** Un obús que explota envia 0xF133 (UnitOnExplosion) amb l'uid del tirador i el
  número de l'impacte; un impacte amb un és `explosive`, la resta `kinetic`.
* **El canó i la seva ranura.** 0xF0BD (UnitBulletRearm) és la següent ronda carregada: l'índex de l'arma
  a la llista d'armes del vehicle, la ranura de munició i les rondes que queden. La recàrrega d'un carregador
  manual arriba un temps de recàrrega constant després de cada un dels seus impactes, la d'un canó
  automàtic una fracció de segon després. Els impactes d'un tirador s'agrupen per vehicle, signatura i
  ràfega; un grup és el d'una arma quan aquella arma carrega una ronda dins de 20 s després de la meitat
  dels seus impactes o més, amb un retard constant. `ammoSlot` és `weapon/slot`, la ranura carregada abans
  de l'impacte: probablement la disparada, tret que el jugador canviés la munició entremig. Les
  metralladores no envien 0xF0BD.
* **L'obús.** L'arma d'una mort és l'identificador de l'obús (`125mm_3bm46`); l'últim impacte de l'assassí
  sobre la víctima el dona a la ranura d'aquell tirador, on el calibre del canó coincideix. El seu tipus i
  calibre són els del fitxer d'arma (`bulletName`, `bulletType`, `caliber`; `apds_fs_*` APFSDS, `heat_fs_*`
  HEAT-FS, `he_*` HE ...).
* **El calibre** de la resta: el de l'arma d'una ranura; el d'un grup de metralladora, l'únic calibre de
  metralladora que pot tenir la seva signatura; en cas contrari, el del canó principal del vehicle. Sense la
  instal·lació (`--game`) no hi ha tipus, nom ni calibre més enllà de `explosive` / `kinetic`.

No trobat: el rebot. Diversos missatges més porten el tirador i el número de l'impacte (0xF0C2, probablement
el camí de la càmera d'impacte a través del vehicle; 0xF117, 0xF13C, 0xF13E); es guarden a l'annex, no
es desxifren. Una no penetració es queda com a `nonpenetration`.

## Focs als vehicles {#vehicle-fires}

Un vehicle en flames es mostra a tots els clients: el servidor envia un missatge d'entitat al vehicle
(esdeveniment `0a519c58`) que llista els focs que hi cremen, cada vegada que la llista canvia. Per foc:
dos identificadors de 16 bits (el segon un node del model de danys), el seu tipus, i -1 fins que el foc
agafa. Un foc encès per un impacte també rep un missatge amb el punt on crema, en el marc del vehicle
(x endavant, y amunt, z esquerra).

Files: `fire_on` quan apareix un foc a la llista, `fire_off` quan ja no hi és, al vehicle, amb `fireId`
(`first:node`), `fireKind` i, per als focs que ha encès un impacte, `fireLocalX/Y/Z` (endavant, amunt,
dreta). Un cop un vehicle és mort, la seva llista sovint no es torna a enviar: els seus focs acaben amb la
seva resta, si no amb la seva entitat, si no amb la repetició (`selfCheck.fires`).

Comprovat: cada vegada que el nombre d'extintors d'un tanc baixava, un foc sortia de la seva llista dins
d'una fracció de segon; la majoria dels punts de foc són al mateix costat del vehicle que l'impacte que
l'havia encès. Els tipus són números; no se sap què designen, ni quina part és cada node. Els avions no
envien cap llista així: un avió en flames no es llegeix.

---

Part de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentació](https://holdi601.github.io/3DHeat/)). Font: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
