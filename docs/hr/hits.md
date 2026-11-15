---
title: Pogoci, paljba i požari
nav_order: 13
lang: "hr"
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Pogoci, paljba i požari {#hits-gunfire-and-fires}

Za čitatelje koji žele znati odakle dolaze stupci pogodaka, streljiva i požara. Provjere daju samo metodu
i slaganje.

## Paljba {#gunfire}

Svaki projektil koji je pogodio jedinicu nalazi se u snimci (poruka 0xF0E9): redak `shot` na položaju
strijelca u trenutku pogotka, `targetX/Y/Z` točka pogotka (pogođena jedinica, pomaknuta za točku pogotka u
njezinu okviru, zakrenuta njezinim stavom), smjer prema njoj, `other` pogođena jedinica. Granate i meci koji
su promašili nisu poslani: nisu entiteti, a poruke o oružju u letu nose samo rakete, projektile, bombe i
torpeda. Preostali meci igrača koji snima (njegov stupac `ammo`) padaju dok puca, pa se njegovi rafali mogu
razlučiti, ali ne i kamo su ti meci otišli. Teški protuzračni i topništvo šalju svaki pojedinačni hitac
(`gun_shot`, bez smjera), a 40 mm protuzračni topovi svoje rafale (`fire_start`, `fire_stop`).

## Ishodi pogodaka {#hit-outcomes}

Uz svaki pogodak projektilom na kopnenu jedinicu poslužitelj šalje jedinici poruku 0xF144 (UnitOnHit): četiri
jednobajtna polja, četvrto su bitovi onoga što je pogodak učinio (`selfCheck.unitMessages.outcome_*`):

| Bit | Značenje | Dokaz |
|---|---|---|
| 0x20 | vlastiti pogodak projektila | gotovo sve dolaze s pogotkom 0xF0E9 na jedinicu unutar 5 ms; bez njega, s eksplozijom (rasprskavanje) |
| 0x01 | prošao je (probijanje) | svaka poruka s 0x02, 0x04 ili 0x08 također ga ima |
| 0x02 | kritični pogodak | većina zapisa kritičnih pogodaka ga ima, znatno češće nego slučajno |
| 0x04 | uništeno | većina dolazi sa zapisom ubojstva i smrću jedinice unutar sekunde |
| 0x08 | teška šteta | neki zapisi kritičnih pogodaka ga imaju; inače rijetko |

`hitOutcome` uzima najgori: `kill` (0x04), `critical` (0x02 ili 0x08), `penetration` (0x01),
`nonpenetration` (samo 0x20). Pogodak se spaja s najbližim nesparenim 0xF144 s 0x20 za njegovu jedinicu unutar
5 ms. Igrina kamera pogodaka razlikuje odbijanje od neprobijanja, ali nijedan bit ni polje ovdje nađeno to
ne čini: prva tri bajta mijenjaju se od pogotka do pogotka i nisu poznata. Snimke klijenta šalju 0xF144 samo
za zrakoplov igrača koji snima, svi bitovi čisti: pogoci zrakoplova i brodova nemaju ishod.

## Streljivo {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Eksplozivno ili ne.** Granata koja se rasprsne šalje 0xF133 (UnitOnExplosion) s uid-om strijelca i brojem
  pogotka; pogodak s njom je `explosive`, ostali `kinetic`.
* **Top i njegov utor.** 0xF0BD (UnitBulletRearm) je sljedeći metak koji je ubačen: indeks oružja na popisu
  oružja vozila, utor streljiva i broj preostalih metaka. Ručni punjač šalje ga stalno vrijeme punjenja nakon
  svakog svojeg pogotka, automatski top djelić sekunde nakon. Pogoci strijelca grupiraju se po vozilu,
  potpisu i rafalu; grupa pripada oružju kad to oružje ubaci metak unutar 20 s nakon polovice ili više njezinih
  pogodaka, pri stalnom razmaku. `ammoSlot` je `weapon/slot`, utor ubačen prije pogotka: vjerojatno onaj
  ispaljen, osim ako je igrač u međuvremenu promijenio streljivo. Mitraljezi ne šalju 0xF0BD.
* **Granata.** Oznaka ubojstva je id granate (`125mm_3bm46`); posljednji pogodak ubojice na žrtvu dodjeljuje
  to tom utoru tog strijelca, gdje kalibar topa odgovara. Njezina vrsta i kalibar su iz datoteke oružja
  (`bulletName`, `bulletType`, `caliber`; `apds_fs_*` APFSDS, `heat_fs_*` HEAT-FS, `he_*` HE ...).
* **Kalibar ostalih:** oružja utora; za skupinu mitraljeza jedini kalibar mitraljeza koji njezin potpis može
  imati; inače glavni top vozila. Bez instalacije (`--game`) nema vrste, naziva ni kalibra osim
  `explosive` / `kinetic`.

Nije nađeno: odbijanje. Nekoliko drugih poruka nosi strijelca i broj pogotka (0xF0C2, vjerojatno put kamere
pogotka kroz vozilo; 0xF117, 0xF13C, 0xF13E); čuvaju se u pomoćnoj datoteci, ne dekodiraju se. Neprobijanje
ostaje `nonpenetration`.

## Požari vozila {#vehicle-fires}

Vozilo u plamenu prikazuje se svakom klijentu: poslužitelj šalje vozilu poruku entiteta (događaj `0a519c58`)
s popisom požara koji gore na njemu, pri svakoj promjeni popisa. Po požaru: dva 16-bitna id (drugi je čvor
modela oštećenja), njegova vrsta, i -1 dok požar ne uhvati. Požar koji je zapalio pogodak dobiva i poruku s
točkom gdje gori, u okviru vozila (x naprijed, y gore, z lijevo).

Retci: `fire_on` kad se požar pojavi na popisu, `fire_off` kad nestane, na vozilu, s `fireId` (`first:node`),
`fireKind` i, za požare koje je zapalio pogodak, `fireLocalX/Y/Z` (naprijed, gore, desno). Kad je vozilo
mrtvo, njegov popis se često više ne šalje: njegovi požari završe s njegovom olupinom, inače s njegovim
entitetom, inače sa snimkom (`selfCheck.fires`).

Provjereno: svaki put kad je broj gasila tenka pao, požar je nestao s popisa unutar djelića sekunde; većina
točaka požara leži s iste strane vozila kao pogodak koji ga je zapalio. Vrste su brojevi; nije poznato što
imenuju, kao ni koji je dio čvor. Zrakoplovi ne šalju takav popis: zrakoplov u plamenu se ne čita.

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
