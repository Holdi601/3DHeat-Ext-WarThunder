---
title: Træf, skud og brande
nav_order: 13
lang: "da"
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Træf, skud og brande {#hits-gunfire-and-fires}

For dem, der vil vide, hvor træf-, ammunitions- og brandkolonnerne kommer fra. Kontroller giver kun
metoden og overensstemmelsen.

## Skud {#gunfire}

Hvert projektil, der ramte en enhed, er i replayet (meddelelse 0xF0E9): en `shot`-række ved skytten
på det tidspunkt, hvor træffet skete, `targetX/Y/Z` ramtepunktet (den ramte enhed, flyttet med
ramtepunktet i dens ramme, drejet efter dens holdning), retningen hen imod den, og `other` den ramte
enhed. Granater og kugler, der missede, sendes ikke: de er ikke entiteter, og meddelelserne om våben i
flugt rummer kun raketter, missiler, bomber og torpedoer. Den optagende spillers resterende skud (dens
`ammo`-kolonne) falder, efterhånden som den skyder, så dens skudserier kan skelnes, men ikke hvor de
skud tog hen. Tung luftværn og artilleri sender hvert enkelt skud (`gun_shot`, uden retning), 40 mm
luftværnskanoner deres skudserier (`fire_start`, `fire_stop`).

## Udfald af træf {#hit-outcomes}

Ved hvert projektiltræf på en landenhed sender serveren meddelelse 0xF144 (UnitOnHit) til enheden: fire
ét-byte-felter, hvor det fjerde er bittene for, hvad træffet gjorde (`selfCheck.unitMessages.outcome_*`):

| Bit | Betydning | Belæg |
|---|---|---|
| 0x20 | et projektils eget træf | næsten alle kommer med et 0xF0E9-træf på enheden inden for 5 ms; uden det, med en eksplosion (stænk) |
| 0x01 | det trængte igennem (gennemslag) | hver meddelelse med 0x02, 0x04 eller 0x08 har den også |
| 0x02 | kritisk træf | de fleste kritiske træfrekorder har den, langt oftere end tilfældigt |
| 0x04 | ødelagt | de fleste kommer med et drabsrekord og enhedens død inden for et sekund |
| 0x08 | tung skade | nogle kritiske træfrekorder har den; ellers sjældent |

`hitOutcome` tager det værste: `kill` (0x04), `critical` (0x02 eller 0x08), `penetration` (0x01),
`nonpenetration` (kun 0x20). Et træf parres med det nærmeste uparrede 0xF144 med 0x20 på dets enhed
inden for 5 ms. Spillets træfkamera skelner en afprallen fra et ikke-gennemslag, men ingen bit eller felt,
der er fundet her, gør det: de tre første bytes varierer fra træf til træf og er ikke kendt. Klientreplays
sender kun 0xF144 for den optagende spillers eget fly, med alle bit slukket: fly- og skibstræf har intet
udfald.

## Ammunition {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Eksplosiv eller ej.** En granat, der springer, sender 0xF133 (UnitOnExplosion) med skyderens uid og
  træffets nummer; et træf med en sådan er `explosive`, resten `kinetic`.
* **Kanonen og dens plads.** 0xF0BD (UnitBulletRearm) er den næste patron, der lægges i: våbnets indeks i
  køretøjets våbenliste, ammunitionspladsen og de tilbageværende skud. En manuel lader kommer en fast
  genladningstid efter hvert af dens træf, en automatkanons en brøkdel af et sekund efter. En skyders træf
  grupperes efter køretøj, signatur og skudserie; en gruppe hører til et våben, når det våben lægger en
  patron i inden for 20 s efter halvdelen eller mere af gruppens træf med en fast forsinkelse. `ammoSlot` er
  `weapon/slot`, den plads der var lagt i før træffet: sandsynligvis den, der blev skudt, medmindre spilleren
  skiftede ammunition undervejs. Maskinpistoler sender ingen 0xF0BD.
* **Granaten.** Et drabs våben er granatens id (`125mm_3bm46`); skyderens sidste træf på offeret giver
  det til den skyderes plads, hvor kanonens kaliber stemmer. Dens type og kaliber er våbenfilens
  (`bulletName`, `bulletType`, `caliber`; `apds_fs_*` APFSDS, `heat_fs_*` HEAT-FS, `he_*` HE ...).
* **Kaliberen** for resten: en plads' våbens; en maskinpistolgruppes den ene maskinpistolkaliber dens
  signatur kan have; ellers hovedkanonens på køretøjet. Uden installationen (`--game`) findes ingen type,
  intet navn og ingen kaliber ud over `explosive` / `kinetic`.

Ikke fundet: afprallen. Flere andre meddelelser bærer skyderen og nummeret på træffet (0xF0C2, sandsynligvis
træfkameraets vej gennem køretøjet; 0xF117, 0xF13C, 0xF13E); de gemmes i sidecaren, ikke afkodet. Et
ikke-gennemslag forbliver `nonpenetration`.

## Brande i køretøjer {#vehicle-fires}

Et køretøj i brand vises for hver klient: serveren sender en entitetsmeddelelse til køretøjet (begivenhed
`0a519c58`), der lister de brande, der brænder på det, hver gang listen ændrer sig. Pr. brand: to 16-bit-id'er
(det andet en skademodel-node), dens art, og -1, indtil ilden tager. En brand, et træf tændte, får også en
meddelelse med det punkt, hvor den brænder, i køretøjets ramme (x fremad, y op, z venstre).

Rækker: `fire_on`, når en brand dukker op på listen, `fire_off`, når den er væk, på køretøjet, med `fireId`
(`first:node`), `fireKind` og, for brande et træf tændte, `fireLocalX/Y/Z` (fremad, op, højre). Når et køretøj
er dødt, sendes dets liste ofte ikke igen: dets brande ender med dets vrag, ellers med dets entitet, ellers
med replayet (`selfCheck.fires`).

Kontrolleret: hver gang en tanks antal brandslukkere faldt, forsvandt en brand fra dens liste inden for en
brøkdel af et sekund; de fleste brandpunkter ligger på samme side af køretøjet som det træf, der tændte dem.
Arterne er tal; hvad de navngiver, vides ikke, og heller ikke hvilken del en node er. Fly sender ingen sådan
liste: et fly i brand læses ikke.

---

Del af [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
