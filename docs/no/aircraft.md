---
title: "Fly"
nav_order: 11
lang: no
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Fly {#aircraft}

For lesere som vil vite hvor flykolonnene kommer fra, og hvor mye de kan stole
på. Hver kontroll nedenfor sammenligner en verdi med noe replayen sier på en
annen, uavhengig måte; bare metoden og samsvaret er oppgitt.

## Cockpit-instrumenter {#cockpit-instruments}

Melding 0xD04A sender opptakspillerens målere som par (nummer, verdi): fire i
sekundet i arkadeslag, bare endrede verdier i simulatorslag. Nummerne danner én
liste for alle cockpitene, og en cockpit sender de målerne modellen har. Spillets
kode setter hvilket nummer som er hvilken måler, så hvert nummer ble navngitt etter
hva det gjør og kontrollert mot replayen (`convert.INSTRUMENTS` holder resultatet;
ingenting leses fra installasjonen):

| Nummer | Navn | Kontrollert mot |
|---|---|---|
| 0 | indikert lufthastighet, m/s | sporets fart korrigert for lufttetthet: korrelasjon 0,99 |
| 39 | stigehastighet, m/s | sporets stigehastighet: korrelasjon over 0,99 |
| 40, 41 | høyde, m; høyde modulo 1000 | sporets høyde, noen meter fra hverandre |
| 52, 53 | kunstig horisont, rull og stigning | minus tabellens rull og stigning, under 1 grad fra hverandre |
| 64 | kompass | tabellens retning, under 0,1 grad fra hverandre |
| 15-20 | rorpedaler | sidekraften på flyet |
| 23, 31 | styrespak: høyderor og krengeror (fortegn som cockpitmodellens) | angrepsvinkelen; rullehastigheten |
| 69, 71, 73 | klokke: timer (12-timers skive), minutter, sekunder | opptaksdatamaskinens lokale tid, til minuttet |
| 75 | ladetrykk, atm | høyere ved krigsnødeffekt enn ved full gass |
| 81-86, 87-92, 93-98 | omdreininger per motor, omdreininger modulo 1000, turtellermåler | hverandre nøyaktig; motorens omdreininger: korrelasjon over 0,97 |
| 195 | drivstoff | synker gjennom en utflyging, full igjen ved en gjenoppstandelse |
| 228-230 | landingsstell, 1 nede | nede bare nær flyplassenes høyde og ved landingsfart |
| 240, 241 | gass per motor (1,1 for krigsnødeffekt eller etterbrenner) | flyinngangens gass |
| 330-332, 346-348 | ammunisjonstellere (to like sett) | våpenforvalgets runder, som synker med flyinngangens runder |
| 135, 159 | olje- og sylinderhodetemperatur | sannsynlig: de stiger over en utflyging |
| 58, 61 | slirkule, svingnål | sannsynlig: de følger sidekraften og svingraten |
| 223 | luftbrems | sannsynlig: satt bare ved innflyging |
| 490-497, 500-505 | hjulbremser | sannsynlig: satt bare når den står på en flyplass |

Noen få flere nummer sendes der betydningen ikke er kjent; de beholdes i
kampdokumentets `authorInstruments.notNamed`.

Tabellens `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`,
`oilTemperature`, `headTemperature` og `throttle` kommer fra disse, på
opptakspillerens egne rader, og tar den siste meldingen høyst 0,2 s etter
samplen.

## Flyinngangene {#flight-entries}

Hvert flys flyinngang (pakketype 2) bærer, i tillegg til posisjon og holdning:

- **Hastighet**: et 32-bits ord etter holdningen. Bitene 31, 30 og 29 er fortegnene
  for x, y og z; deretter farten i 11 bits av 500/2047 m/s (den stopper ved
  500 m/s), så |x| og |y| som brøkdeler av farten i 9 bits hver, og z er det som
  gjør vektoren til en enhetsvektor. Kontrollert mot steget mellom mottatte samples:
  retningen stemmer innen en brøkdel av en grad for opptakspilotens fly og innen
  ca. 2 grader for alle andre; farten innen 0,2 %. `selfCheck.flightEntries`.
- **Runder per våpen**: en liste før posisjonen, ett element per våpen, de
  gjenværende rundene først. Opptakspillerens er lik cockpitens tellere ett tikk
  senere for nesten hvert samplet.
- **Kontroller og gass**: 7 byte etter hastigheten, lest som 14 halvbyte. For
  opptakspilleren, hvert tikk: 1 høyderoret, 2 krengeroret, 3 roret (8 i hvile),
  11 gassen i femtendedeler (15 også for krigsnødeffekt og etterbrenner), 4
  hjulbremsene, 5 luftbremsen, 8 sannsynligvis bremseskjermen. Andre flys
  halvbyte endrer seg bare noen få ganger i et slag, og er ikke deres kontroller
  på det tidspunktet.
- **Motorer**: per motor en tilstandsbyte (0 av; 1-6 starter; 7 går; 8 død), en
  16-bits verdi bare med etterbrenner (32767 full), og en byte bare etter at
  motoren ble truffet. De fleste fly der motoren går til «død» blir skutt ned
  eller avslutter innen minutter.

## Refleksjonsdata {#reflection-data}

Meldingene 0xF02D og 0xF0AA replikerer spillets nummererte objekter: per objekt
dets ID (de øverste 5 bitene er typen, de nederste 11 en indeks) og en felttabell.
Type 14 er spillerplassene (felt 2 bruker-ID og navn, 9 laget), type 15 lagene
(indeks 1 og 2):

- En plass sitt felt 39 holder statistikken på faste plasser: drap (forskyvning 0),
  lagdrap (2), dødsfall (4), sjødrap (10), KI-drap (12), KI-bakkedrap (14), assists
  (20), erobringssoner (22), sonskade (24, 32-bit), skadepremie (40, 32-bit),
  unndratte missiler (50). Felt 38 starter med poengsummen, felt 42 er tropp. Ved
  slutten av et slag er hver verdi lik resultatenes for hver spiller
  (`selfCheck.scoreboardVsResults`). Hvor bakkedrap føres, er ikke kjent.
- Et lags felt 7 er poengsummen: til slutt er det lik summen av spillerpoengene i
  resultatene. Felt 3 er sannsynligvis billettene.
- Hver melding sender bare feltene som endret seg, så `scoreboard` i
  kampdokumentet lister hver spillers statistikk og hvert lags poengsum ved hver
  endring.

## Dead reckoning og utjevneren {#dead-reckoning-and-the-smoother}

En klientreplay tar opp hvert fly fire ganger i sekundet, slik klienten tegnet
det. Mellom oppdateringene den mottar for et fjernt fly, flytter klienten det
videre langs sin siste hastighet og snur det etter sine siste rater, og ved neste
oppdatering hopper den dit. Leses slik den er, går et spor rett og så hopper det.
Ingenting i flyinngangen markerer hvilke samples som ble mottatt; et dead
reckoning-sample gjenkjennes på hva det er: det fortsetter den rette linjen av de
to samplene før det, i deres tempo, innen 3 cm.

Hvor mye dette betyr, avhenger av slaget: i arkadeslag kan omtrent halvparten av
de andre flyenes samples være dead reckoning, i simulatorslag bare noen få
prosent. Utjevneren kutter stegene over 15 g med omtrent fem ganger
(`selfCheck.deadReckoning`). Opptakspilotens eget fly ekstrapoleres ikke av
klienten og lar seg stå som det er.

Som standard (`--no-smoothing` slår det av) settes sporene til alle enheter
unntatt opptakspilotens der de mottatte tilstandene sier de var: et dead
reckoning-sample går på en kurve gjennom de mottatte samplene før og etter, hver
med sin egen hastighet; over mer enn 3 s bøyes den rette linjen bare mot neste
mottatte sample, så ingen sample flytter seg lenger enn klientens egen
korreksjon. Holdningen dreies jevnt fra én mottatt holdning til neste. Mottatte
samples jevnes med høyst 2 m eller 0,04 s av deres fart; en jevn sving forblir
som den er. Replayens egne verdier står i kolonnene `Raw`.

## Holdning, kontrollert {#attitude-checked}

På opptakspilotens eget fly ligger retningen innen en grad (median) fra
bevegelsesretningen, stigningen innen noen få grader fra stigningsvinkelen, og i
tydelige svinger har rullen svingens fortegn for nesten hvert samplet: flymodellens
rull er venstre vinge ned positiv, og tabellen snur den til høyre vinge ned
positiv (`selfCheck.aircraftAttitude`). De 10-bits vinklene går 0,18 grader om
gangen. Bakkeenheters holdning kontrolleres mot deres skudd
([Tårn](ground.md#turrets)).

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentasjon](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
