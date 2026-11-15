---
title: Unitats terrestres i càmera
nav_order: 12
lang: ca
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Unitats terrestres i càmera {#ground-units-and-camera}

Per a qui vol saber d'on venen les columnes de torreta, càmera i mode de batalla, i com de
fiables són. Les comprovacions donen només el mètode i l'acord.

## Torretes {#turrets}

L'estat terrestre d'un tanc (actitud de 16 bits) conté, després de la seva posició, 141 bits
no llegits; després, per torreta, 62 bits: el guinyol de la torreta i el pitch del canó (16 bits
cadascun, 360/65536 graus per pas, amb signe), i 30 bits no llegits; després el farciment, i en
alguns estats 200 bits més. El nombre de torretes és el byte enviat abans de l'estat. Un estat la
longitud del qual no encaixa no dona cap torreta (les unitats estàtiques envien un estat més
curt). El guinyol és relatiu al casc, positiu en sentit horari, 0 tot endavant; el pitch és relatiu
al casc, positiu amunt.

Com es va comprovar:

- **Contra els trets:** per a cada impacte d'un tanc, la direcció mundial del seu canó principal
  (l'actitud del casc girada pel guinyol de la torreta i el pitch del canó) contra la línia des del
  tirador fins a la unitat impactada, a almenys 30 m: per batalla, una mediana d'uns 98 % dins de 3
  graus en heading i 99 % en elevació (`selfCheck.turretsVsShots`). La resta són sobretot impactes
  d'una metralladora en una altra torreta.
- **Contra la mira del jugador que grava:** el seu propi tanc envia l'angle mundial de la seva mira
  (en sentit antihorari des de l'est), el pitch i la distància. El heading del casc més el guinyol de
  la torreta està dins de mig grau (mediana) de la mira.

**Les repeticions de servidor** (0xF074) envien l'estat de cada tanc amb la mateixa disposició,
seguit de dades pròpies, de manera que es llegeix cada torreta els dos angles de la qual són dins de
l'estat (almenys la principal per a gairebé cada fila de tanc). És la torreta, no la càmera:

- **Contra els trets**, com s'ha dit: per batalla, per sobre del 90 % dins de 3 graus en heading i
  99 % en elevació.
- **Contra la vista:** una repetició de servidor envia la mira de cada jugador (`viewYaw`,
  `viewPitch`). La torreta segueix la vista dins de mig grau (mediana), però gira molt més lentament
  del que la vista es mou, com ho fa un accionament de torreta (`selfCheck.turretVsView`).
- **Però no sempre a la velocitat d'un accionament:** mostra a mostra, el valor tal com s'envia de
  vegades salta a la mira quan la mira és a prop del canó, més ràpid del que gira cap accionament.

Per tant, la taula conté la torreta **subjectada al seu accionament**: `turretYaw` / `gunPitch`
s'acosten al valor tal com s'envia a una velocitat no més gran que la de gir del canó principal del
fitxer de vehicle de la instal·lació (per 1,3 per als talents i modificacions de la tripulació; 45 i
20 graus per segon quan la instal·lació no n'indica cap). A cada impacte del canó principal, la
torreta es fixa exactament a la línia del tret, i una passada enrere la hi porta a temps
(`selfCheck.turretLimit`). La fila `shot` també porta aquests `turretYaw` / `gunPitch`. El valor
tal com s'envia es manté a `turretYawRaw` / `gunPitchRaw`. Un tanc l'estat del qual no porta cap
torreta té les columnes de torreta buides (el visualitzador pot recórrer a `viewYaw`).
`gunPitch` és una mica per sobre de `viewPitch` a distància: l'elevació del canó per la caiguda del
projectil.

Els estats dels vaixells tenen una altra disposició; les seves torretes no es llegeixen. Els avions no
envien cap direcció de cap ni de vista; el missatge 0xD020 dels canons antiaeris no es llegeix.

## La càmera {#the-camera}

El missatge 0xD043, uns 20 per segon, és la càmera de repetició del propi jugador que grava: el camp 1
és un quaternió que gira el davant de la càmera cap a on mira; 2 és el lloc de la càmera respecte al
vehicle que segueix (m); 4 el mateix desplaçament en el marc propi del vehicle (x endavant, y amunt, z
esquerra); 5 cap on apunta el jugador (un vector unitari); 3 el zoom (uns 1,2 en la vista de tercera
persona d'un tanc, uns 1,0 en un avió, més alt en la mira d'un artiller o a través de binoculars).
Comprovat: el camp 4 és el camp 2 girat al marc del vehicle, dins de 0,5 m per gairebé cada missatge;
el davant de la càmera té el heading de la mira. La repetició no envia cap camp de visió en graus,
només el zoom.

La taula té la càmera com una trajectòria pròpia: tipus `camera`, trajectòria `<jugador> camera #ca`,
una fila com a molt cada 0,1 s, al lloc del vehicle seguit més el camp 2, mirant al llarg del
quaternió (`dirX/Y/Z`, `heading`, `pitch`, `roll`), amb `zoom`, `aimHeading` i `aimPitch`, i
`otherLife`, la vida que segueix. `selfCheck.camera` compta les files i la comprovació.

## Final d'una trajectòria {#end-of-a-track}

Una trajectòria es dibuixa des de la seva primera fila fins a la seva última. Quan la seva unitat
desapareix abans que acabi la repetició, la seva última fila és una fila `despawn` al seu últim lloc:
al moment en què el joc va eliminar la seva entitat (quan va arribar dins de 6 s de la seva última
mostra), si no, a la seva última mostra. Una trajectòria sense una així dura fins al final de la
repetició. Les files d'una mateixa trajectòria poden estar molt separades (una unitat llunyana o una
resta es refresca cada pocs segons, i una resta a vegades no durant minuts): el seu últim estat es
manté fins a la següent fila.

## Mode de batalla {#battle-mode}

El byte de la capçalera al desplaçament 688 guarda la dificultat als seus quatre bits baixos: 0
arcade (AB), 5 realista (RB), 10 simulador (SB). Comprovat amb els tipus de batalla que se sabia que
tenien les repeticions. El mode de joc és `ground` quan la missió deixa aparèixer tancs, si no
`naval` quan deixa aparèixer vaixells, si no `air` (`allowedUnitTypes`); el mode propi de la missió
surt de la seva clau (`missions/_Dom`), nomenat des de `lang/missions_versus.csv` de la teva
instal·lació. La mateixa clau és la part `<mode>` dels noms de fitxer i de l'identificador de la
partida (`Conq4`, `Dom`), que es deixa fora quan la capçalera no en té cap.

---

Part de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentació](https://holdi601.github.io/3DHeat/)). Font: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
