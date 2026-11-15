---
title: "Treff, skuddild og branner"
nav_order: 13
lang: "no"
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Treff, skuddild og branner {#hits-gunfire-and-fires}

For lesere som vil vite hvor treff-, ammunisjons- og brann-kolonnene kommer fra.
Kontroller gir bare metoden og samsvaret.

## Skuddild {#gunfire}

Hvert prosjektil som traff en enhet finnes i replayen (melding 0xF0E9): en `shot`-rad
på skytterens posisjon i det øyeblikket det traff, `targetX/Y/Z` treffpunktet (enheten
som ble truffet, flyttet med treffpunktet i dens ramme, dreiet med dens holdning),
retningen mot den, `other` enheten som ble truffet. Granater og kuler som bommet, sendes
ikke: de er ikke entiteter, og meldingene om våpen i flukt holder bare raketter, missiler,
bomber og torpedoer. Opptakspilotens gjenværende runder (`ammo`-kolonnen) synker når
den skyter, så dens skuddserier kan skilles, men ikke hvor disse rundene gikk. Tung
luftvern og artilleri sender hvert enkelt skudd (`gun_shot`, ingen retning), 40 mm
luftvernkanoner sine skuddserier (`fire_start`, `fire_stop`).

## Utfall av treff {#hit-outcomes}

Ved hvert prosjektiltreff mot en bakkeenhet sender serveren melding 0xF144
(UnitOnHit) til enheten: fire ett-byte-felt, det fjerde er bitene for hva treffet
gjorde (`selfCheck.unitMessages.outcome_*`):

| Bit | Betydning | Belegg |
|---|---|---|
| 0x20 | et prosjektils eget treff | nesten alle kommer med et 0xF0E9-treff på enheten innen 5 ms; uten det, med en eksplosjon (splash) |
| 0x01 | det gikk gjennom (gjennomslag) | hver melding med 0x02, 0x04 eller 0x08 har den også |
| 0x02 | kritisk treff | de fleste kritisk-treff-poster har den, langt oftere enn tilfeldig |
| 0x04 | ødelagt | de fleste kommer med en drapspost og enhetens død innen ett sekund |
| 0x08 | tungt skadet | noen kritisk-treff-poster har den; ellers sjelden |

`hitOutcome` tar det verste: `kill` (0x04), `critical` (0x02 eller 0x08),
`penetration` (0x01), `nonpenetration` (0x20 alene). Et treff paires med det nærmeste
ikke-parede 0xF144 med 0x20 til sin enhet innen 5 ms. Spillets treffkamera skiller en
rikosjett fra et ikke-gjennomslag, men ingen bit eller felt som er funnet her gjør det:
de tre første byteene varierer fra treff til treff og er ikke kjent. Klientreplayer
sender 0xF144 bare for opptakspilotens eget fly, alle bits av: fly- og skipstreff har
ingen utfall.

## Ammunisjon {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Eksplosiv eller ikke.** En granat som brister, sender 0xF133 (UnitOnExplosion) med
  skytterens uid og treffets nummer; et treff med en slik er `explosive`, resten
  `kinetic`.
* **Kanonen og dens plass.** 0xF0BD (UnitBulletRearm) er neste runde som lastes:
  våpenets indeks i kjøretøyets våpenliste, ammunisjonsplassen og gjenværende runder.
  En manuell lasters kommer et fast omladningstid etter hvert av dens treff, en
  automatkanons et brøkdels sekund etter. En skytters treff grupperes etter kjøretøy,
  signatur og skuddserie; en gruppe er et våpens når dette våpenet laster en runde
  innen 20 s etter halvparten av treffene eller mer, med en jevn forsinkelse.
  `ammoSlot` er `våpen/plass`, plassen som var lastet før treffet: sannsynligvis den
  som ble skutt, med mindre spilleren byttet ammunisjon i mellomtiden. Maskingevær
  sender ingen 0xF0BD.
* **Granaten.** Et drapsvåpens ID er granatens ID (`125mm_3bm46`); drepernes siste treff
  på offeret gir den til den skytterens plass, der kanonens kaliber stemmer. Dens type
  og kaliber er våpenfilens (`bulletName`, `bulletType`, `caliber`; `apds_fs_*` APFSDS,
  `heat_fs_*` HEAT-FS, `he_*` HE ...).
* **Kaliberen** for resten: en plass sitt våpens; en maskingevær-gruppes den ene
  maskingeværkaliberen dens signatur kan ha; ellers kjøretøyets hovedkanons. Uten
  installasjonen (`--game`) finnes ingen type, navn eller kaliber utover `explosive` /
  `kinetic`.

Ikke funnet: rikosjett. Flere meldinger bærer treffets skytter og nummer (0xF0C2,
sannsynligvis treffkameraets vei gjennom kjøretøyet; 0xF117, 0xF13C, 0xF13E); de
beholdes i sidefilen, men er ikke dekodet. Et ikke-gjennomslag forblir `nonpenetration`.

## Kjøretøybranner {#vehicle-fires}

Et kjøretøy i brann vises for alle klienter: serveren sender en entitetsmelding til
kjøretøyet (hendelse `0a519c58`) som lister brannene som brenner på det, hver gang
listen endrer seg. Per brann: to 16-bits ID-er (den andre en skademodellnode), dens
type, og -1 til branen tar. En brann tent av et treff får også en melding med punktet
der den brenner, i kjøretøyets ramme (x forover, y opp, z venstre).

Rader: `fire_on` når en brann dukker opp i listen, `fire_off` når den er borte, på
kjøretøyet, med `fireId` (`første:node`), `fireKind` og, for branner et treff tente,
`fireLocalX/Y/Z` (forover, opp, høyre). Når et kjøretøy er dødt, sendes listen ofte
ikke igjen: dets branner ender med vraket, ellers med dens entitet, ellers med
replayen (`selfCheck.fires`).

Kontrollert: hver gang en stridsvogns antall brannslukkere falt, forsvant en brann fra listen
innen en brøkdel av et sekund; de fleste brannpunkter ligger på samme side av kjøretøyet
som treffet som tente dem. Typene er tall; hva de betegner, er ikke kjent, og heller
ikke hvilken del en node er. Fly sender ingen slik liste: et fly i brann leses ikke.

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentasjon](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
