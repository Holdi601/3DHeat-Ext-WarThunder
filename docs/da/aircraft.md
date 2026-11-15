---
title: Fly
nav_order: 11
lang: "da"
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Fly {#aircraft}

For dem, der vil vide, hvor flykolonnerne kommer fra, og hvor meget man kan stole på dem.
Hver kontrol nedenfor sammenligner en værdi med noget, replayet selv siger på en anden,
uafhængig måde; kun metoden og overensstemmelsen gives.

## Cockpitinstrumenter {#cockpit-instruments}

Meddelelse 0xD04A sender den optagende spillers målere som (nummer, værdi)-par: fire i
sekundet i arkadekampe, kun ændrede værdier i simulatorkampe. Numrene danner én liste på
tværs af alle cockpits, og et cockpit sender de målere, dets model har. Spillets kode
bestemmer, hvilket nummer der er hvilken måler, så hvert nummer er navngivet efter, hvad
det gør, og kontrolleret mod replayet (`convert.INSTRUMENTS` indeholder resultatet; intet
læses fra installationen):

| Nummer | Navn | Kontrolleret mod |
|---|---|---|
| 0 | indikeret lufthastighed, m/s | sporets hastighed korrigeret for lufttæthed: korrelation 0,99 |
| 39 | stigehastighed, m/s | sporets stigehastighed: korrelation over 0,99 |
| 40, 41 | højde, m; højde modulo 1000 | sporets højde, få meter fra hinanden |
| 52, 53 | kunstig horisont, rulning og pitch | minus tabellens rulning og pitch, under 1 grad fra hinanden |
| 64 | kompas | tabellens heading, under 0,1 grad fra hinanden |
| 15-20 | rorpedaler | sidekraften på flyet |
| 23, 31 | styrepind: højderor og krængeror (fortegn som cockpitmodellens) | angrebsvinklen; rullehastigheden |
| 69, 71, 73 | ur: timer (12-timers skive), minutter, sekunder | optagecomputerens lokale tid, til minuttet |
| 75 | indsugningstryk, atm | højere ved krigsnødeffekt end ved fuld gas |
| 81-86, 87-92, 93-98 | omdrejninger pr. motor, omdrejninger modulo 1000, omdrejningsmåler | hinanden nøjagtigt; motorens omdrejninger: korrelation over 0,97 |
| 195 | brændstof | falder under en udflyvning, fuld igen ved en genopstandelse |
| 228-230 | understelsben, 1 nede | nede kun nær flyvepladsernes højde og ved landingshastighed |
| 240, 241 | gas pr. motor (1,1 krigsnødeffekt eller efterbrænder) | flyveposternes gas |
| 330-332, 346-348 | ammunitionstællere (to ens sæt) | våbenforvalgets skud, faldende med flyveposternes skud |
| 135, 159 | olie- og cylindertemperatur | sandsynligt: de stiger under en udflyvning |
| 58, 61 | slipkugle, drejenål | sandsynligt: de følger sidekraften og drejehastigheden |
| 223 | luftbremse | sandsynligt: kun sat ved indflyvning |
| 490-497, 500-505 | hjulbremser | sandsynligt: kun sat, når man står på en flyveplads |

Nogle få flere numre sendes, hvis betydning ikke kendes; de gemmes i kampdokumentets
`authorInstruments.notNamed`.

Tabellens `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`,
`headTemperature` og `throttle` kommer fra disse på den optagende spillers egne rækker,
idet man tager den sidste meddelelse højst 0,2 s efter samplet.

## Flyveposter {#flight-entries}

Hvert flys flypost (pakketype 2) bærer, ud over sin position og holdning:

- **Hastighed**: et 32-bit-ord efter holdningen. Bit 31, 30 og 29 er fortegnene for x, y og
  z; derefter farten i 11 bit af 500/2047 m/s (den stopper ved 500 m/s), derefter |x| og |y|
  som brøkdele af farten i 9 bit hver, og z er det, der gør vektoren til en enhedsvektor.
  Kontrolleret mod trinnet mellem modtagne samples: retningen stemmer inden for en brøkdel af
  en grad for den optagende spiller og inden for ca. 2 grader for alle andre; farten inden
  for 0,2 %. `selfCheck.flightEntries`.
- **Skud pr. våben**: en liste før positionen, én post pr. våben, de tilbageværende skud først.
  Den optagende spillers er lig cockpittets tællere ét tick senere for næsten hver prøve.
- **Styring og gas**: 7 bytes efter hastigheden, læst som 14 nibbles. For den optagende spiller,
  hver tick: 1 højderoret, 2 krængerorene, 3 roret (8 i hvile), 11 gassen i femtendedele (15
  også for krigsnødeffekt og efterbrænder), 4 hjulbremserne, 5 luftbremsen, 8 sandsynligvis
  bremseskærmen. Andre flys nibbles ændrer sig kun få gange i et slag og er ikke deres styring
  på det tidspunkt.
- **Motorer**: pr. motor en tilstandsbyte (0 slukket; 1-6 starter; 7 kører; 8 død), en 16-bit-
  værdi kun med efterbrænder (32767 fuld), og en byte kun efter at motoren blev ramt. De fleste
  fly, hvis motor går til "død", bliver skudt ned eller ender inden for minutter.

## Reflekteringsdata {#reflection-data}

Meddelelserne 0xF02D og 0xF0AA replikerer spillets nummererede objekter: pr. objekt dets id
(de øverste 5 bit er arten, de nederste 11 et indeks) og en feltliste. Art 14 er spillerpladserne
(felt 2 bruger-id og navn, 9 holdet), art 15 holdene (indeks 1 og 2):

- En plads' felt 39 holder dens statistik på faste pladser: drab (offset 0), holddrab (2),
  dødsfald (4), sødrab (10), AI-drab (12), AI-landdrab (14), assists (20), erobringszoner (22),
  zoneskade (24, 32-bit), skadepræmie (40, 32-bit), undvigelser af missiler (50). Felt 38 starter
  med scoren, felt 42 er truppen. Ved kampens slutning er hver værdi lig resultaternes for hver
  spiller (`selfCheck.scoreboardVsResults`). Hvor landdrab gemmes, vides ikke.
- Et holds felt 7 er dets score: til sidst er det lig summen af dets spilleres scorer i resultaterne.
  Felt 3 er sandsynligvis dets billetter.
- Hver meddelelse sender kun de felter, der er ændret, så `scoreboard` i kampdokumentet lister
  hver spillers statistik og hvert holds score ved hver ændring.

## Dead reckoning og udjævneren {#dead-reckoning-and-the-smoother}

En klientreplay optager hvert fly fire gange i sekundet, som klienten tegnede det. Mellem de
opdateringer, den modtager for et fjernt fly, flytter klienten det videre efter dets sidste
hastighed og drejer det ved dets sidste rater, og ved næste opdatering springer den det hen
dertil. Læst som det er, kører et spor lige ud og springer så. Intet i flyposten markerer,
hvilke samples der blev modtaget; et dead reckoning-sample findes ud fra, hvad det er: det
fortsætter den rette linje af de to samples før det, i deres tempo, inden for 3 cm.

Hvor meget det betyder, afhænger af kampen: i arkadekampe kan ca. halvdelen af de andre flys
samples være dead reckoning, i simulatorkampe kun få procent. Udjævneren skærer trinene over
15 g ned med ca. fem gange (`selfCheck.deadReckoning`). Den optagende spillers eget fly
ekstrapoleres ikke af klienten og lades, som det er.

Som standard (`--no-smoothing` slår det fra) lægges alle enheders spor undtagen den optagende
spillers, hvor de modtagne tilstande siger, de var: et dead reckoning-sample går på en kurve
gennem de modtagne samples før og efter det, hver med sin egen hastighed; over mere end 3 s bøjes
den rette linje kun hen mod det næste modtagne sample, så intet sample flytter sig længere, end
klientens eget spring. Dets holdning drejes jævnt fra en modtaget holdning til den næste.
Modtagne samples udjævnes med højst 2 m eller 0,04 s af deres hastighed; en jævn drejning bliver,
som den er. Replayets egne værdier bliver i `Raw`-kolonnerne.

## Holdning, kontrolleret {#attitude-checked}

På den optagende spillers eget fly ligger headingen inden for en grad (median) af færdens retning,
pitch inden for få grader af stigevinklen, og i tydelige drejninger har rullen drejningens fortegn
for næsten hver prøve: flyvemodellens rulning er venstre vinge ned positiv, og tabellen drejer den
til højre vinge ned positiv (`selfCheck.aircraftAttitude`). De 10-bit vinkler trin 0,18 grader.
Landenheders holdning kontrolleres mod deres skud ([Tårne](ground.md#turrets)).

---

Del af [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
