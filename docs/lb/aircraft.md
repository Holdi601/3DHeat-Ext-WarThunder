---
title: "Fliger"
nav_order: 11
lang: "lb"
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Fliger {#aircraft}

Fir Lieser, déi wëllen wëssen, vu wou d'Fliger-Kolonnen kommen a wéi wäit ee
hinnen däerf trauen. All Kontroll hei ënnendrënner vergläicht e Wäert mat eppes, wat de
Replay op eng zweet, onofhängeg Manéier seet; nëmmen d'Method an d'Iwwereneestëmmung
ginn ugi.

## Cockpit-Instrumenter {#cockpit-instruments}

D'Message 0xD04A schéckt d'Instrumenter vum opuelende Spiller als (Nummer, Wäert)-
Pairen: véier pro Sekonn a Arcade-Gefechter, nëmmen geännert Wäerter a Simulator-
Gefechter. D'Nummere bilden eng Lëscht iwwer all Cockpiten, an e Cockpit schéckt
d'Instrumenter, déi säi Modell huet. Dem Spill säi Code leet fest, wéi eng Nummer wéi en Instrument ass,
dofir gouf all Nummer no deem benannt, wat se mécht, a géint de Replay gepréift
(`convert.INSTRUMENTS` hält d'Resultat; aus der Installatioun gëtt näischt gelies):

| Nummer | Numm | Gepréift géint |
|---|---|---|
| 0 | ugewisen Loftgeschwindegkeet, m/s | d'Geschwindegkeet vun der Spur, fir d'Loftdichtheet korrigéiert: Korrelatioun 0.99 |
| 39 | Steigrate, m/s | d'Steigrate vun der Spur: Korrelatioun iwwer 0.99 |
| 40, 41 | Héicht, m; Héicht modulo 1000 | d'Héicht vun der Spur, e puer Meter ausenee |
| 52, 53 | kënschtlechen Horizont Roll a Pitch | minus dem Roll a Pitch vun der Tabell, ënner 1 Grad ausenee |
| 64 | Kompass | dem Heading vun der Tabell, ënner 0.1 Grad ausenee |
| 15-20 | Rudderpedaler | d'Säitekraaft um Fliger |
| 23, 31 | Steierknüppel: Héichteruder a Querruder (Virzeechen wéi dat vum Cockpit-Modell) | de Ugrëffswénkel; d'Rollrate |
| 69, 71, 73 | Auer: Stonnen (12-Stonne-Zifferblat), Minutten, Sekonnen | d'Ortszäit vum opuelende Computer, op d'Minutt |
| 75 | Luedduck, atm | méi héich bei Kriichsnuetfall-Leeschtung wéi bei Vollgas |
| 81-86, 87-92, 93-98 | Dréizuel pro Motor, Dréizuel modulo 1000, Dréizuelinstrument | openeen genee; d'Motordréizuel: Korrelatioun iwwer 0.97 |
| 195 | Brennstoff | fält während engem Asaz, beim Respawn erëm voll |
| 228-230 | Fahrwierk-Been, 1 ausgefuer | nëmmen ausgefuer an der Héicht vun de Fluchhäfen a bei der Landungsgeschwindegkeet |
| 240, 241 | Gashiewel pro Motor (1.1 Kriichsnuetfall-Leeschtung oder Nobrenner) | de Gashiewel vum Fluchentrée |
| 330-332, 346-348 | Munitiounszieler (zwee gläich Sätz) | d'Schëss vum Waffepreset, déi mat de Schëss vum Fluchentrée falen |
| 135, 159 | Ueleg- an Zylinderkäpptemperatur | wahrscheinlech: si klammen iwwer en Asaz |
| 58, 61 | Rutschkugel, Wendezeiger | wahrscheinlech: si follegen der Säitekraaft an der Wenderate |
| 223 | Loftbrems | wahrscheinlech: nëmmen am Landungsusaz gesat |
| 490-497, 500-505 | Radbremsen | wahrscheinlech: nëmmen gesat, wann ee stoe bleift op engem Fluchhafen |

E puer weider Nummere ginn geschéckt, där hir Bedeitung net bekannt ass; si ginn am
`authorInstruments.notNamed` vum Match-Dokument behalen.

D'`ias`, `vario`, `fuel`, `manifoldPressure`, `gear`,
`oilTemperature`, `headTemperature` an `throttle` vun der Tabell kommen vun hinnen, op den
eegene Zeile vum opuelende Spiller, wou déi lescht Message héchstens 0.2 s nom
Echantillon geholl gëtt.

## Fluchentréeën {#flight-entries}

Dem Fliger säin Fluchentrée (Pakettyp 2) dréit, nieft senger Positioun
a Lag:

- **Geschwindegkeet**: e 32-Bit-Wuert nom Lag. D'Bits 31, 30 an 29 sinn d'
  Virzeeche vun x, y an z; dann d'Geschwindegkeet a 11 Bits vun 500/2047 m/s (si hält bei
  500 m/s op), dann |x| an |y| als Bruchdeeler vun der Geschwindegkeet a jeeweils 9 Bits, an z
  ass dat, wat de Vecteur zum Eenheetsvecteur mécht. Géint de Schrëtt tëscht
  empfaangenen Echantillone gepréift: d'Richtung stëmmt bannent engem Bruchdeel vun engem Grad fir
  den opuelende Spiller a bannent ongeféier 2 Grad fir all aner; d'Geschwindegkeet
  bannent 0.2 %. `selfCheck.flightEntries`.
- **Schëss pro Waff**: eng Lëscht virun der Positioun, een Element pro Waff,
  d'iwwreg Schëss als éischt. Dem opuelende Spiller seng ass gläich wéi dem Cockpit seng
  Zieler een Tick méi spéit bei bal all Echantillon.
- **Rudere a Gashiewel**: 7 Bytes nom Geschwindegkeet, als 14 Nibbles gelies.
  Fir den opuelende Spiller, all Tick: 1 d'Héichteruder, 2 d'Querruder, 3
  d'Säiteruder (8 an Rou), 11 de Gashiewel a Fofzéntel (15 och fir Kriichsnuetfall-
  Leeschtung an Nobrenner), 4 d'Radbremsen, 5 d'Loftbrems, 8
  wahrscheinlech de Bremsfallschiermer. D'Nibbles vun anere Fliger änneren sech nëmmen e puermol am
  Gefecht a sinn net hir Rudere zu där Zäit.
- **Motoren**: pro Motor e Zoustandsbyte (0 aus; 1-6 start; 7 leeft; 8
  dout), e 16-Bit-Wäert nëmmen mat Nobrenner (32767 voll), an e Byte nëmmen
  nodeem de Motor getraff gouf. Déi meescht Fliger, där hire Motor "dout" geet, ginn
  ofgeschoss oder héieren bannent Minutten op.

## Reflection-Daten {#reflection-data}

D'Messagen 0xF02D an 0xF0AA replizéieren dem Spill seng nummeréiert Objeten: pro Objet
seng ID (déi uewescht 5 Bits d'Aart, déi ënnescht 11 en Index) an eng Feldtabell.
Aart 14 sinn d'Spiller-Slots (Feld 2 User-ID an Numm, 9 d'Team), Aart 15
d'Teams (Index 1 an 2):

- Dem Slot säi Feld 39 hält seng Statistiken op feste Plazen: Kills (Offset 0),
  Team-Kills (2), Doudeger (4), Marine-Kills (10), KI-Kills (12), KI-Buedem-
  Kills (14), Assists (20), Eroberungszonen (22), Zonenschued (24, 32 Bit),
  Schuedauszeechnung (40, 32 Bit), Rakéiteausweichungen (50). Feld 38 fänkt mam
  Score un, Feld 42 ass de Squad. Um Enn vun engem Gefecht ass all Wäert gläich wéi dee
  vun de Resultater fir all Spiller (`selfCheck.scoreboardVsResults`). Wou
  Buedem-Kills gehale ginn, ass net bekannt.
- Dem Team säi Feld 7 ass säi Score: um Enn ass en gläich wéi d'Zomm vun de
  Scoren vu sengem Spiller an de Resultater. Feld 3 ass wahrscheinlech seng Tickets.
- Jidd Message schéckt nëmmen d'Felder, déi sech geännert hunn, dofir lëscht `scoreboard` am
  Match-Dokument d'Statistike vun all Spiller an de Score vun all Team bei
  all Ännerung op.

## Dead Reckoning, an de Glätter {#dead-reckoning-and-the-smoother}

E Client-Replay hält all Fliger véiermol d'Sekonn op, wéi de Client en gezeechent huet. Tëscht
den Updates, déi en fir e wäite Fliger kritt, beweegt de Client en laanscht seng
leschte Geschwindegkeet weider an dréit en mat sengen leschte Rate weider, a
beim nächsten Update setzt en en do hin. Wéi se ass gelies, leeft eng Spur riicht,
dann sprangt se. Näischt am Fluchentrée markéiert, wéi eng Echantillone empfaange goufen;
en dead-reckoned Echantillon gëtt un deem erkannt, wat et ass: et setzt déi riicht
Linn vun den zwee Echantillonen virun him fort, an hirem Tempo, bis op 3 cm.

Wéi vill dat ausmécht, hänkt vum Gefecht of: a Arcade-Gefechter kënne ronn d'Hallschent
vun den Echantillone vun anere Fliger dead-reckoned sinn, a Simulator-Gefechter
nëmmen e puer Prozent. De Glätter schneit d'Schrëtt iwwer 15 g ongeféier fënnefmol erof
(`selfCheck.deadReckoning`). De Fliger vum opuelende Spiller gëtt
vum Client net extrapoléiert a bleift, wéi e ass.

Standardméisseg (`--no-smoothing` schalt et aus) ginn d'Spuren vun alle Eenheeten ausser der
vum opuelende Spiller dohin gesat, wou d'empfaange Zoustänn soen, datt si waren: en
dead-reckoned Echantillon geet op eng Kéier duerch d'empfaange Echantillonen virun
an no him, jidderee mat senger eegener Geschwindegkeet; iwwer méi wéi 3 s gëtt déi riicht
Linn nëmmen a Richtung nächst empfaangent Echantillon gebéit, sou datt kee Echantillon
méi wäit geet wéi dem Client säi Snap. Seng Lag gëtt gläichméisseg vun enger
empfaangener Lag zur nächster gedréint. Empfaangen Echantillone ginn héchstens ëm 2 m
oder 0.04 s vun hirer Geschwindegkeet geglat; eng stänneg Kéier bleift, wéi se ass. Dem Replay seng eege
Wäerter bleiwe an de `Raw`-Kolonnen.

## Lag, gepréift {#attitude-checked}

Um Fliger vum opuelende Spiller läit d'Heading bannent engem Grad (Median) vun der
Beweegungsrichtung, d'Pitch bannent e puer Grad vum Steigwénkel, an a kloere Kéiere
huet d'Roll d'Virzeechen vun der Kéier bei bal all Echantillon: dem Flugmodell seng Roll ass lénke Flilleck
erof positiv, an d'Tabell dréit se op riets Flilleck erof positiv (`selfCheck.aircraftAttitude`).
D'10-Bit-Wénkel sprange ëm 0.18 Grad. D'Lag vun de Buedemeenheeten gëtt géint hir Schëss
gepréift ([Tierm](ground.md#turrets)).

---

Deel vun [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentatioun](https://holdi601.github.io/3DHeat/)). Quell: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
