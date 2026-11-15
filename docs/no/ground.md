---
title: "Bakkeenheter og kamera"
nav_order: 12
lang: "no"
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Bakkeenheter og kamera {#ground-units-and-camera}

For lesere som vil vite hvor tårn-, kamera- og kampmodus-kolonnene kommer fra, og
hvor mye de kan stole på. Kontroller gir bare metoden og samsvaret.

## Tårn {#turrets}

En stridsvogns bakketilstand (16-bits holdning) holder, etter posisjonen, 141 bits som
ikke leses, og deretter per tårn 62 bits: tårnets gir og kanonens stigning (16 bits
hver, 360/65536 grader per steg, med fortegn), og 30 bits som ikke leses; så
utfylling, og i noen tilstander 200 bits til. Antallet tårn er byten som sendes
før tilstanden. En tilstand hvis lengde ikke passer, gir ingen tårn (statiske
enheter sender en kortere tilstand). Girvinkelen er relativ til skroget, positiv
med klokken, 0 rett frem; stigningen er relativ til skroget, opp positiv.

Slik ble det kontrollert:

- **Mot skuddene:** for hvert treff fra en stridsvogn, dens hovedkanons verdensretning
  (skrogets holdning dreid med tårnets gir og kanonens stigning) mot linjen fra
  skytteren til enheten som ble truffet, minst 30 m unna: per slag en median på
  ca. 98 % innen 3 grader i retning og 99 % i høyde (`selfCheck.turretsVsShots`).
  Resten er stort sett treff fra en maskingevær i et annet tårn.
- **Mot opptakspilotens sikting:** hans egen stridsvogn sender sin siktings verdensvinkel
  (mot klokken fra øst), stigning og avstand. Skrogets retning pluss tårnets gir
  ligger innen en halv grad (median) fra sikten.

**Serverreplayer** (0xF074) sender hver stridsvogns tilstand i samme oppsett, etterfulgt
av data av sin egen, så hvert tårn hvis to vinkler ligger innenfor tilstanden
leses (minst hovedtårnet for nesten hver tankrad). Det er tårnet, ikke kameraet:

- **Mot skuddene**, som over: per slag over 90 % innen 3 grader i retning og 99 % i
  høyde.
- **Mot sikten:** en serverreplay sender hver spillers sikte (`viewYaw`,
  `viewPitch`). Tårnet følger sikten innen en halv grad (median), men dreier mye
  saktere enn sikten svinger, slik et tårndrev gjør (`selfCheck.turretVsView`).
- **Men ikke alltid i et drevs fart:** sample for sample hopper verdien slik den
  sendes noen ganger rett på sikten når sikten er nær kanonen, raskere enn noe drev
  dreier.

Derfor holder tabellen tårnet **holdt til sitt drev**: `turretYaw` /
`gunPitch` beveger seg mot verdien slik den sendes, med høyst hovedkanonens
dreiehastighet fra installasjonens kjøretøyfil (ganger 1,3 for mannskapets
ferdigheter og modifikasjoner; 45 og 20 grader per sekund der installasjonen ikke
oppgir noen). Ved hvert treff fra hovedkanonen settes tårnet nøyaktig til skuddets
linje, og et tilbakegående pass får det dit i tide (`selfCheck.turretLimit`).
`shot`-raden bærer også `turretYaw` / `gunPitch`. Verdien slik den sendes, står
i `turretYawRaw` / `gunPitchRaw`. En stridsvogn hvis tilstand ikke har noe tårn, har
tomme tårnkolonner (visningsprogrammet kan falle tilbake til `viewYaw`).
`gunPitch` ligger litt over `viewPitch` på lang avstand: kanonens hevning for
prosjektilets fall.

Skipenes tilstander har et annet oppsett; deres tårn leses ikke. Fly sender ingen
hode- eller sikteretning; luftvernkanonenes melding 0xD020 forblir ulest.

## Kameraet {#the-camera}

Melding 0xD043, ca. 20 i sekundet, er opptakspilotens egne replay-kamera: felt 1 en
kvaternion som dreier kameraets forside dit det ser; 2 kameraets plass fra
kjøretøyet det følger (m); 4 den samme forskyvningen i kjøretøyets egen ramme (x
forover, y opp, z venstre); 5 hvor spilleren sikter (en enhetsvektor); 3 zoomen
(ca. 1,2 i en stridsvogns tredjepersonsvisning, ca. 1,0 i et fly, høyere i en skytters
sikte eller gjennom kikkert). Kontrollert: felt 4 er felt 2 dreiet inn i kjøretøyets
ramme, innen 0,5 m for nesten hver melding; kameraets forside har sikteretningen.
Replayen sender ikke noe synsfelt i grader, bare zoomen.

Tabellen har kameraet som et eget spor: type `camera`, spor `<spiller> camera #ca`,
en rad høyst hvert 0,1 s, på det fulgte kjøretøyets plass pluss felt 2, med utsikt
langs kvaternionen (`dirX/Y/Z`, `heading`, `pitch`, `roll`), med `zoom`,
`aimHeading` og `aimPitch`, og `otherLife` livet det følger. `selfCheck.camera`
teller radene og kontrollen.

## Slutten av et spor {#end-of-a-track}

Et spor tegnes fra sin første rad til sin siste. Når enheten er borte før replayen
slutter, er den siste raden en `despawn`-rad på dens siste plass: på det tidspunktet
spillet fjernet dens entitet (når det kom innen 6 s etter dens siste sample), ellers
på dens siste sample. Et spor uten en slik rad varer til slutten av replayen. Rader i
ett spor kan ligge langt fra hverandre (en fjern enhet eller et vrak oppdateres hvert
par sekund, et vrak noen ganger ikke på flere minutter): dens siste tilstand gjelder
til neste rad.

## Kampmodus {#battle-mode}

Headerens byte på forskyvning 688 holder vanskelighetsgraden i sine fire lave bits:
0 arkade (AB), 5 realistisk (RB), 10 simulator (SB). Kontrollert mot
slagtypene replayene var kjent for å være. Spillmodusen er `ground` når oppdraget
lar stridsvogner spawne, ellers `naval` når det lar skip, ellers `air`
(`allowedUnitTypes`); oppdragets egen modus kommer fra nøkkelen (`missions/_Dom`),
og navngis fra installasjonens `lang/missions_versus.csv`. Den samme nøkkelen er
`<modus>`-delen i filnavnene og kamp-ID-en (`Conq4`, `Dom`), utelatt der headeren
ikke har noen.

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentasjon](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
