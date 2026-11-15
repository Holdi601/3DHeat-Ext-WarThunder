---
title: "Pogoci, paljba i požari"
nav_order: 13
lang: "bs"
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Pogoci, paljba i požari {#hits-gunfire-and-fires}

Za čitaoce koji žele znati odakle dolaze kolone pogodaka, municije i požara.
Provjere daju samo metodu i slaganje.

## Paljba {#gunfire}

Svaki projektil koji je pogodio jedinicu nalazi se u replayu (poruka 0xF0E9): red `shot`
na poziciji strijelca u trenutku pogotka, `targetX/Y/Z`
tačka pogotka (pogođena jedinica, pomjerena za tačku pogotka u njenom okviru, okrenuta njenim
stavom), smjer prema njoj, `other` pogođena jedinica. Granate i
meci koji su promašili ne šalju se: nisu entiteti, a
poruke oružja u letu drže samo rakete, projektile, bombe i torpeda.
Preostali meci igrača koji snima (njegova kolona `ammo`) padaju dok puca,
pa se njegovi rafali mogu razlikovati, ali ne i kamo su ti meci otišli. Teška protivavionska artiljerija i
artiljerija šalju svaki pojedinačni hitac (`gun_shot`, bez smjera), protivavionski topovi od 40 mm
svoje rafale (`fire_start`, `fire_stop`).

## Ishodi pogodaka {#hit-outcomes}

Uz svaki pogodak projektila na kopnenu jedinicu server šalje poruku 0xF144
(UnitOnHit) jedinici: četiri jednobajtna polja, četvrto su bitovi onoga što je
pogodak učinio (`selfCheck.unitMessages.outcome_*`):

| Bit | Značenje | Dokaz |
|---|---|---|
| 0x20 | vlastiti pogodak projektila | gotovo svi dolaze s pogotkom 0xF0E9 na jedinici unutar 5 ms; bez njega, s eksplozijom (rasprskavanje) |
| 0x01 | prošao je (penetracija) | svaka poruka s 0x02, 0x04 ili 0x08 ima i njega |
| 0x02 | kritični pogodak | većina zapisa kritičnih pogodaka ga ima, mnogo češće nego slučajno |
| 0x04 | uništen | većina dolazi sa zapisom ubistva i smrću jedinice unutar sekunde |
| 0x08 | teško oštećenje | neki zapisi kritičnih pogodaka ga imaju; inače rijetko |

`hitOutcome` uzima najgore: `kill` (0x04), `critical` (0x02 ili 0x08),
`penetration` (0x01), `nonpenetration` (samo 0x20). Pogodak se uparuje s
najbližim neuparenim 0xF144 s 0x20 za njegovu jedinicu unutar 5 ms. Kamera
pogodaka igre razlikuje rikošet od nepenetracije, ali nijedan ovdje pronađen bit ili polje to ne
čini: prva tri bajta variraju od pogotka do pogotka i nisu
poznata. Klijentski replayevi šalju 0xF144 samo za vlastiti
avion igrača koji snima, sa svim očišćenim bitovima: pogoci aviona i brodova nemaju ishod.

## Municija {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Eksplozivna ili ne.** Granata koja eksplodira šalje 0xF133 (UnitOnExplosion)
  s uid-om strijelca i brojem pogotka; pogodak s njom je
  `explosive`, ostali `kinetic`.
* **Top i njegov slot.** 0xF0BD (UnitBulletRearm) je sljedeći napunjeni
  metak: indeks oružja na listi oružja vozila, slot municije
  i preostali meci. Poruka ručnog punjača dolazi nakon stalnog vremena punjenja
  poslije svakog njegovog pogotka, automatskog topa djelić sekunde poslije. Pogoci
  jednog strijelca grupišu se po vozilu, potpisu i rafalu; grupa je
  oružja kad to oružje napuni metak unutar 20 s poslije polovine njenih pogodaka
  ili više uz stalno kašnjenje. `ammoSlot` je `weapon/slot`, slot napunjen
  prije pogotka: vjerovatno onaj iz kojeg je pucano, osim ako je igrač u međuvremenu promijenio
  municiju. Mitraljezi ne šalju 0xF0BD.
* **Granata.** Oružje ubistva je id granate (`125mm_3bm46`);
  zadnji pogodak ubice na žrtvu daje je slotu tog strijelca, gdje se
  kalibar topa slaže. Njen tip i kalibar su iz datoteke oružja
  (`bulletName`, `bulletType`, `caliber`; `apds_fs_*` APFSDS, `heat_fs_*`
  HEAT-FS, `he_*` HE ...).
* **Kalibar** ostalih: kalibar oružja slota; za grupu mitraljeza
  jedini kalibar mitraljeza koji njen potpis može imati; inače kalibar
  glavnog topa vozila. Bez instalacije (`--game`) nema tipa, imena ili
  kalibra osim `explosive` / `kinetic`.

Nije pronađeno: rikošet. Nekoliko drugih poruka nosi strijelca i broj pogotka
(0xF0C2, vjerovatno putanja kamere pogodaka kroz vozilo; 0xF117,
0xF13C, 0xF13E); čuvaju se u sidecar datoteci, nisu dekodirane.
Nepenetracija ostaje `nonpenetration`.

## Požari vozila {#vehicle-fires}

Vozilo koje gori prikazuje se svakom klijentu: server šalje poruku entiteta
vozilu (događaj `0a519c58`) s listom požara koji na njemu gore,
svaki put kad se lista promijeni. Po požaru: dva 16-bitna id-a (drugi je
čvor modela oštećenja), njegova vrsta i -1 dok se požar ne primi. Požar koji
je zapaljen pogotkom dobiva i poruku s tačkom gdje gori, u okviru
vozila (x naprijed, y gore, z lijevo).

Redovi: `fire_on` kad se požar pojavi na listi, `fire_off` kad nestane,
na vozilu, sa `fireId` (`first:node`), `fireKind` i, za požare koje je
pogodak zapalio, `fireLocalX/Y/Z` (naprijed, gore, desno). Kad je vozilo mrtvo, njegova
lista se često ne šalje ponovo: njegovi požari završavaju s njegovom olupinom, inače s njegovim
entitetom, inače s replayom (`selfCheck.fires`).

Provjereno: svaki put kad je pao broj aparata za gašenje tenka, požar je napustio njegovu
listu unutar djelića sekunde; većina tačaka požara leži na istoj strani
vozila kao pogodak koji ih je zapalio. Vrste su brojevi; šta imenuju
nije poznato, niti koji je dio čvor. Avioni ne šalju takvu listu: avion
koji gori ne čita se.

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
