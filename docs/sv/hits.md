---
title: "Träffar, beskjutning och bränder"
nav_order: 13
lang: "sv"
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Träffar, beskjutning och bränder {#hits-gunfire-and-fires}

För läsare som vill veta var träff-, ammunitions- och brandkolumnerna kommer ifrån.
Kontrollerna anger bara metoden och överensstämmelsen.

## Beskjutning {#gunfire}

Varje projektil som träffade en enhet finns i repriset (meddelande 0xF0E9): en `shot`-rad på
skyttens position i träffögonblicket, `targetX/Y/Z` träffpunkten (den träffade enheten, flyttad
med träffpunkten i dess system, vriden med dess attityd), riktningen mot den, `other` den träffade
enheten. Granater och kulor som missade skickas inte: de är inga entiteter, och meddelandena för
vapen i luften bär bara raketer, robotar, bomber och torpeder. Den inspelande spelarens skott kvar
(dess kolumn `ammo`) sjunker när den skjuter, så dess skurar kan urskiljas, men inte vart de skotten
tog vägen. Tung luftvärn och artilleri skickar varje enskilt skott (`gun_shot`, utan riktning),
40 mm luftvärnskanoner sina skurar (`fire_start`, `fire_stop`).

## Träffutfall {#hit-outcomes}

Med varje projektilträff på en markenhet skickar servern meddelande 0xF144 (UnitOnHit) till enheten:
fyra ettbyte-fält, det fjärde är bitarna för vad träffen gjorde (`selfCheck.unitMessages.outcome_*`):

| Bit | Betydelse | Belägg |
|---|---|---|
| 0x20 | en projektils egen träff | nästan alla kommer med en 0xF0E9-träff på enheten inom 5 ms; utan den, med en explosion (splitter) |
| 0x01 | den gick igenom (genomslag) | varje meddelande med 0x02, 0x04 eller 0x08 har den också |
| 0x02 | kritisk träff | de flesta kritiska träffposter har den, betydligt oftare än slumpen |
| 0x04 | förstörd | de flesta kommer med en dödspost och enhetens död inom en sekund |
| 0x08 | svår skada | några kritiska träffposter har den; annars sällan |

`hitOutcome` tar det värsta: `kill` (0x04), `critical` (0x02 eller 0x08), `penetration` (0x01),
`nonpenetration` (0x20 ensamt). En träff paras med den närmaste oparade 0xF144 med 0x20 till sin
enhet inom 5 ms. Spelets träffkamera skiljer en rikoschett från ett icke-genomslag, men ingen bit eller
något fält som hittats här gör det: de tre första byten varierar från träff till träff och är inte
kända. Klientrepriser skickar 0xF144 bara för den inspelande spelarens egna flygplan, med alla bitar
släckta: flygplan- och fartygsträffar har inget utfall.

## Ammunition {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Sprängämne eller inte.** En granat som spricker skickar 0xF133 (UnitOnExplosion) med skyttens uid
  och träffens nummer; en träff med en sådan är `explosive`, resten `kinetic`.
* **Kanonen och dess plats.** 0xF0BD (UnitBulletRearm) är nästa laddade runda: vapnets index i
  fordonets vapenlista, ammunitionsplatsen och rundorna kvar. En manuell laddares kommer en stadig
  laddningstid efter varje av dess träffar, en autokanons en bråkdel av en sekund efter. En skyttes
  träffar grupperas efter fordon, signatur och skur; en grupp är ett vapens när det vapnet laddar en
  runda inom 20 s efter hälften eller fler av träffarna med en stadig fördröjning. `ammoSlot` är
  `weapon/slot`, platsen som laddats före träffen: troligen den som avfyrades, om inte spelaren bytte
  ammunition emellan. Kulsprutor skickar ingen 0xF0BD.
* **Granaten.** En döds vapen är granatens id (`125mm_3bm46`); dödarens sista träff på offret ger det
  till den skyttens plats, där kanonens kaliber stämmer. Dess typ och kaliber är vapenfilens
  (`bulletName`, `bulletType`, `caliber`; `apds_fs_*` APFSDS, `heat_fs_*` HEAT-FS, `he_*` HE ...).
* **Kalibern** för resten: en platss vapens; en kulsprutegrupps den enda kulsprutekalibern dess
  signatur kan ha; annars huvudkanonens i fordonet. Utan installationen (`--game`) finns ingen typ,
  inget namn och ingen kaliber utöver `explosive` / `kinetic`.

Inte hittat: rikoschetter. Flera andra meddelanden bär träffens skytt och nummer (0xF0C2, troligen
träffkamerans väg genom fordonet; 0xF117, 0xF13C, 0xF13E); de behålls i sidofilen, inte avkodade.
Ett icke-genomslag förblir `nonpenetration`.

## Fordonsbränder {#vehicle-fires}

Ett fordon i brand visas för varje klient: servern skickar ett entitetsmeddelande till fordonet
(händelse `0a519c58`) som listar de bränder som brinner på det, varje gång listan ändras. Per brand:
två 16-bitars id (det andra en skademodellsnod), dess slag, och -1 tills branden tar. En brand som
tänts av en träff får också ett meddelande med platsen där den brinner, i fordonets system (x framåt,
y upp, z vänster).

Rader: `fire_on` när en brand dyker upp i listan, `fire_off` när den är borta, på fordonet, med
`fireId` (`first:node`), `fireKind` och, för bränder som en träff tände, `fireLocalX/Y/Z` (framåt,
upp, höger). När ett fordon är dött skickas dess lista ofta inte igen: dess bränder slutar med dess
vrak, annars med dess entitet, annars med repriset (`selfCheck.fires`).

Kontrollerat: varje gång en stridsvagns antal brandsläckare sjönk, lämnade en brand listan inom en
bråkdel av en sekund; de flesta brandpunkter ligger på samma sida av fordonet som träffen som tände dem.
Slagen är siffror; vad de namnger är inte känt, inte heller vilken del en nod är. Flygplan skickar ingen
sådan lista: ett flygplan i brand läses inte.

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Källa: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
