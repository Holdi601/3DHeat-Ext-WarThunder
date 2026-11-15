---
title: "Buedemeenheeten a Kamera"
nav_order: 12
lang: lb
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Buedemeenheeten a Kamera {#ground-units-and-camera}

Fir Lieser, déi wëllen wëssen, vu wou d'Kolonnen fir Turm, Kamera a Gefechtsmodus
kommen a wéi wäit ee hinnen däerf trauen. D'Kontrolle ginn nëmmen d'Method an
d'Iwwereneestëmmung un.

## Tierm {#turrets}

Dem Panzer säi Buedemzoustand (16-Bit-Lag) hält, no senger Positioun, 141 Bits,
déi net gelies ginn, dann pro Turm 62 Bits: dem Turm säi Yaw an dem Kanounpitch
(16 Bits jiddwer, 360/65536 Grad de Schrëtt, signéiert) an 30 Bits, déi net gelies ginn; dann
Padding, an op e puer Zoustänn nach 200 Bits. D'Turmzuel ass dat Byte, dat
virum Zoustand geschéckt gëtt. E Zoustand, deem seng Längt net passt, gëtt keng Tierm (statesch
Eenheeten schécken e méi kuerzen Zoustand). De Yaw ass relativ zum Rumpf, am Auerzäigersënn
positiv, 0 grad no vir; d'Pitch relativ zum Rumpf, erop positiv.

Wéi et gepréift gouf:

- **Géint d'Schëss:** fir all Treffer vun engem Panzer seng Haaptkanoun hir Welt-
  Richtung (Rumpflag, gedréint vum Turm-Yaw a Kanounpitch) géint d'Linn
  vum Schëtze zu der getraffener Eenheet, op d'mannst 30 m ewech: pro Gefecht e
  Median vu ronn 98 % bannent 3 Grad am Heading a 99 % an der Elevatioun
  (`selfCheck.turretsVsShots`). De Rescht sinn meeschtens Treffer vun engem Maschinnegewier
  an engem anere Turm.
- **Géint dem opuelende Spiller säin Zil:** säi Panzer schéckt dem Zil säi Welt-
  Wénkel (géint den Auerzäigersënn vun Osten), Pitch an Distanz. Dem Rumpf säin Heading
  plus dem Turm säi Yaw läit bannent engem hallwe Grad (Median) vum Zil.

**Server-Replays** (0xF074) schécke vun all Panzer den Zoustand an der selwechter Layout,
gefollegt vun eegenen Daten, dofir gëtt all Turm gelies, deem seng zwee Wénkel am
Zoustand leien (op d'mannst den Haaptturm bei bal all Panzerzeil). Et ass
den Turm, net d'Kamera:

- **Géint d'Schëss**, wéi uewen: pro Gefecht iwwer 90 % bannent 3 Grad am
  Heading a 99 % an der Elevatioun.
- **Géint d'Usiicht:** e Server-Replay schéckt dem Zil vun all Spiller
  (`viewYaw`, `viewPitch`). Den Turm follegt der Usiicht bannent engem hallwe Grad
  (Median), dréit awer vill méi lues, wéi d'Usiicht schwenkt, wéi en Turmantrieb
  et mécht (`selfCheck.turretVsView`).
- **Awer net émmer mat der Geschwindegkeet vun engem Antrieb:** Echantillon fir Echantillon
  sprangt de geschécktene Wäert heiansdo op d'Zil, wann d'Zil bei der Kanoun ass, méi séier wéi iergendeen
  Antrieb dréit.

Dofir hält d'Tabell den Turm **un säin Antrieb gehalen**: `turretYaw` /
`gunPitch` beweege sech Richtung geschéckte Wäert mat héchstens der Dréigeschwindegkeet vun der Haaptkanoun
aus der Gefierdatei vun der Installatioun (mal 1.3 fir Besatzungsfäegkeeten
a Modifikatiounen; 45 an 20 Grad d'Sekonn, wou d'Installatioun keng
nennt). Bei all Treffer vun der Haaptkanoun gëtt den Turm genau op d'Linn vum
Schoss gesat, an e Réckwärtsduerchgang bréngt en rechtzäiteg dohin (`selfCheck.turretLimit`).
D'`shot`-Zeil dréit dat `turretYaw` / `gunPitch` och. De geschéckte Wäert
bleift an `turretYawRaw` / `gunPitchRaw`. E Panzer, deem säi Zoustand keen
Turm dréit, huet eidel Turmkolonnen (de Viewer kann op `viewYaw` zréckfalen).
`gunPitch` läit op Distanz e bësse méi héich wéi `viewPitch`: d'Elevatioun vun der Kanoun
fir de Fall vun der Granat.

D'Zoustänn vu Schëff hunn eng aner Layout; hir Tierm ginn net gelies. Fliger
schécken keng Kapp- oder Usiichtsrichtung; d'Message 0xD020 vun de Fligerofwier-Kanounen bleift ongelies.

## D'Kamera {#the-camera}

D'Message 0xD043, ongeféier 20 d'Sekonn, ass dem opuelende Spiller seng eege Replay-
Kamera: Feld 1 e Quaternion, deen dem Kamera säi Vir dohin dréit, wou se kuckt;
2 dem Kamera seng Plaz vum Gefier, dat se follegt, aus (m); 4 datselwecht Offset
am Koordinatesystem vum Gefier (x no vir, y erop, z no lénks); 5 wouhin de Spiller ziilt
(en Eenheetsvecteur); 3 de Zoom (ongeféier 1.2 an der Third-Person-Usiicht vun engem Panzer, ongeféier
1.0 an engem Fliger, méi héich am Visier vun engem Schëtze oder duerch e Fernglas).
Gepréift: Feld 4 ass Feld 2, an dem Gefier säi System gedréint, bannent 0.5 m
bei bal all Message; dem Kamera säi Vir huet dem Zil säin Heading. De
Replay schéckt kee Gesiichtsfeld a Grad, nëmmen de Zoom.

D'Tabell huet d'Kamera als eegen Spur: kind `camera`, track
`<player> camera #ca`, eng Zeil héchstens all 0.1 s, op der Plaz vum gefollegte Gefier
plus Feld 2, mat Bléck laanscht de Quaternion (`dirX/Y/Z`, `heading`,
`pitch`, `roll`), mat `zoom`, `aimHeading` an `aimPitch`, an `otherLife`
dem Liewen, dat se follegt. `selfCheck.camera` zielt d'Zeilen an d'Kontroll.

## Enn vun enger Spur {#end-of-a-track}

Eng Spur gëtt vu senger éischter bis zu senger lescht Zeil gezeechent. Wann hir Eenheet fort ass,
ier de Replay ophält, ass hir lescht Zeil eng `despawn`-Zeil op hirer leschter Plaz:
zu der Zäit, wou d'Spill hir Entitéit ewechgeholl huet (wann dat bannent 6 s no hirem
leschte Echantillon koum), soss um leschte Echantillon. Eng Spur ouni déi hält bis zum Enn
vum Replay. Zeile vun enger Spur kënne wäit ausenee sinn (eng wäit Eenheet oder e Wrack
gëtt all puer Sekonne rafraîchéiert, e Wrack heiansdo Minutte laang net): säin lëschten
Zoustand hält bis zu senger nächster Zeil.

## Battle-Modus {#battle-mode}

Dem Header säi Byte bei Offset 688 hält d'Schwieregkeet a senge ënneschte véier Bits:
0 Arcade (AB), 5 Realistic (RB), 10 Simulator (SB). Gepréift géint d'
Gefechtsarten, vun deenen een wousst, datt d'Replays se waren. De Spillmodus ass `ground`, wann
d'Mission Panzer spawnen léisst, soss `naval`, wann se Schëff léisst, soss `air`
(`allowedUnitTypes`); dem Mission säin eegene Modus kënnt vu sengem Schlëssel
(`missions/_Dom`), benannt aus der `lang/missions_versus.csv` vun denger Installatioun. Dee
selwechte Schlëssel ass den `<mode>`-Deel vun den Dateinimm an der Match-ID (`Conq4`,
`Dom`), ewechgelooss, wou den Header keen huet.

---

Deel vun [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentatioun](https://holdi601.github.io/3DHeat/)). Quell: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
