---
title: "Treffer, Schéiss a Brand"
nav_order: 13
lang: lb
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Treffer, Schéiss a Brand {#hits-gunfire-and-fires}

Fir Lieser, déi wëllen wëssen, vu wou d'Kolonnen fir Treffer, Munitioun a Brand
kommen. D'Kontrolle ginn nëmmen d'Method an d'Iwwereneestëmmung un.

## Schéiss {#gunfire}

All Projektil, dat eng Eenheet getraff huet, ass am Replay (Message 0xF0E9): eng `shot`-
Zeil op der Positioun vum Schëtze am Moment vum Treffer, `targetX/Y/Z` den
Treffpunkt (d'getraff Eenheet, ëm de Treffpunkt a sengem System verréckelt, mat senger
Lag gedréint), d'Richtung dohin, `other` d'getraff Eenheet. Granaten an
Kugelen, déi verfeelt hunn, ginn net geschéckt: si sinn keng Entitéiten, an d'
Waffen-am-Fluch-Messagen halen nëmme Rakéiten, Rakéitegeschosser, Bommen an Torpedoen.
D'Schëss, déi dem opuelende Spiller bleiwen (seng `ammo`-Kolonn), falen, wéi en schéisst,
dofir kann een seng Stéiss erkennen, awer net, wouhin dës Schëss gaange sinn. Schwéier Fligerofwier
an Artillerie schécken all eenzele Schoss (`gun_shot`, keng Richtung), 40-mm-Fligerofwier-Kanounen
hir Stéiss (`fire_start`, `fire_stop`).

## Treffer-Ausgäng {#hit-outcomes}

Mat all Projektiltreffer op eng Buedemeenheet schéckt de Server d'Message 0xF144
(UnitOnHit) un d'Eenheet: véier Ee-Byte-Felder, dat véiert d'Bits vun deem, wat de
Treffer gemaach huet (`selfCheck.unitMessages.outcome_*`):

| Bit | Bedeitung | Beleeg |
|---|---|---|
| 0x20 | dem Projektil säin eegenen Treffer | bal all kommen mat engem 0xF0E9-Treffer op d'Eenheet bannent 5 ms; ouni en, mat enger Explosioun (Splitter) |
| 0x01 | et ass duerchkomm (Duerschlag) | all Message mat 0x02, 0x04 oder 0x08 huet et och |
| 0x02 | kritesche Treffer | déi meescht kritesch-Treffer-Enregistrementer hunn et, vill méi dacks wéi Zoufall |
| 0x04 | zerstéiert | déi meescht kommen mat engem Kill-Enregistrement an dem Doud vun der Eenheet bannent enger Sekonn |
| 0x08 | schwéiere Schued | e puer kritesch-Treffer-Enregistrementer hunn et; soss selten |

`hitOutcome` hëlt dat Schlëmmst: `kill` (0x04), `critical` (0x02 oder 0x08),
`penetration` (0x01), `nonpenetration` (0x20 eleng). E Treffer gëtt mat dem
nootste onpaarte 0xF144 mat 0x20 un seng Eenheet bannent 5 ms gepaart. Dem Spill seng
Treffer-Kamera ennerscheet en Ofpraller vun enger Nonpenetration, awer kee Bit oder Feld,
dat hei fonnt gouf, mécht dat: déi éischt dräi Bytes variéieren vun Treffer zu Treffer a sinn net
bekannt. Client-Replays schécken 0xF144 nëmmen fir dem opuelende Spiller säi
Fliger, all Bits fräi: Fliger- a Schëfftreffer hunn keen Ausgang.

## Munitioun {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Explosiv oder net.** Eng Granat, déi explodéiert, schéckt 0xF133 (UnitOnExplosion)
  mat der uid vum Schëtze an der Nummer vum Treffer; en Treffer mat enger ass
  `explosive`, de Rescht `kinetic`.
* **D'Kanoun a säi Slot.** 0xF0BD (UnitBulletRearm) ass déi nächst Patroun, déi
  gelueden ass: den Index vun der Waff an der Waffelëscht vum Gefier, de Munitiouns-
  slot an d'iwwreg Schëss. Bei engem manuelle Lueder kënnt se eng stänneg Nuelueschzäit
  no all senge Treffer, bei enger Autokanoun e Bruchdeel vun enger Sekonn duerno. D'
  Treffer vun engem Schëtze ginn no Gefier, Signatur a Stouss gruppéiert; eng Grupp ass
  vun enger Waff, wann déi Waff bannent 20 s no der Hallschent vun hiren Treffer
  oder méi mat enger stännegen Verzögerung eng Patroun luet. `ammoSlot` ass `weapon/slot`, de Slot, dee
  virum Treffer gelueden war: wahrscheinlech deen, dee geschoss gouf, ausser de Spiller huet d'
  Munitioun dertëschent gewiesselt. Maschinnegewierer schécken keen 0xF0BD.
* **D'Granat.** Dem Kill seng Waff ass d'ID vun der Granat (`125mm_3bm46`); dem
  Killer säi leschten Treffer op d'Affer gëtt se dem Slot vun deem Schëtze, wou
  d'Kaliber vun der Kanoun passt. Säin Typ a Kaliber sinn déi vun der Waffendatei
  (`bulletName`, `bulletType`, `caliber`; `apds_fs_*` APFSDS, `heat_fs_*`
  HEAT-FS, `he_*` HE ...).
* **D'Kaliber** vum Rescht: dat vun der Waff vum Slot; bei enger Maschinnegewier-Grupp dat
  eent Maschinnegewier-Kaliber, dat hir Signatur ka hunn; soss dat vun der Haaptkanoun
  vum Gefier. Ouni d'Installatioun (`--game`) gëtt et kee Typ, Numm oder Kaliber
  iwwer `explosive` / `kinetic` eraus.

Net fonnt: Ofpraller. Verschidde weider Messagen droen de Schëtze vum Treffer an
d'Nummer (0xF0C2, wahrscheinlech de Wee vun der Treffer-Kamera duerch d'Gefier; 0xF117,
0xF13C, 0xF13E); si ginn an der Niewendatei behalen, net decodéiert. Eng
Nonpenetration bleift `nonpenetration`.

## Gefierbränn {#vehicle-fires}

E brennend Gefier gëtt all Client gewisen: de Server schéckt dem Gefier eng Entitéit-
Message (Evenement `0a519c58`), déi d'Bränn opleescht, déi drop brennen,
all Kéier wann d'Lëscht sech ännert. Pro Brand: zwou 16-Bit-IDen (déi zweet e
Schuedmodell-Knuet), seng Aart, an -1 bis de Brand hält. E Brand, deen en Treffer ugezunn huet,
kritt och eng Message mam Punkt, wou en brennt, am System vum Gefier
(x no vir, y erop, z no lénks).

Zeilen: `fire_on`, wann e Brand an der Lëscht opdaucht, `fire_off`, wann en fort ass,
um Gefier, mat `fireId` (`first:node`), `fireKind` an, fir Bränn, déi en
Treffer ugezunn huet, `fireLocalX/Y/Z` (no vir, erop, no riets). Soubal e Gefier dout ass, gëtt seng
Lëscht dacks net nach eng Kéier geschéckt: seng Bränn héieren mat sengem Wrack op, soss mat senger
Entitéit, soss mam Replay (`selfCheck.fires`).

Gepréift: all Kéier wann d'Zuel vun de Feierläscher vun engem Panzer gefall ass, huet e Brand seng
Lëscht bannent engem Bruchdeel vun enger Sekonn verlooss; déi meescht Brandpunkte leien op der selwechter Säit vum
Gefier wéi den Treffer, deen se ugezunn huet. D'Aarte si Zuelen; wat se nennen, ass net
bekannt, och net, wéi en Deel e Knuet ass. Fliger schécken keng sou Lëscht: e
brennende Fliger gëtt net gelies.

---

Deel vun [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentatioun](https://holdi601.github.io/3DHeat/)). Quell: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
