---
title: Pataikymai, šaudymas ir gaisrai
nav_order: 13
lang: "lt"
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Pataikymai, šaudymas ir gaisrai {#hits-gunfire-and-fires}

Skirta skaitytojams, norintiems žinoti, iš kur ateina pataikymo, šaudmenų ir gaisro stulpeliai.
Patikrinimai nurodo tik metodą ir sutapimą.

## Šaudymas {#gunfire}

Kiekvienas sviedinys, pataikęs į vienetą, yra įraše (pranešimas 0xF0E9): `shot` eilutė šaulio
pozicijoje tą akimirką, kai įvyko pataikymas, `targetX/Y/Z` - pataikymo taškas (pataikytas vienetas,
perkeltas per pataikymo tašką jo rėmelyje, pasuktas pagal jo orientaciją), kryptis į jį, `other` -
pataikytas vienetas. Sviediniai ir kulkos, kurie nepataikė, neįrašomi: jie nėra esybės, o pranešimai
apie skrendančius ginklus apima tik raketas, raketas su valdymu, bombas ir torpedas. Žaidėjo likę
šaudmenys (jo `ammo` stulpelis) krenta, kai jis šaudo, todėl jo serijos gali būti atpažįstamos, bet
ne tai, kur tie šaudmenys nuskrido. Sunkūs priešlėktuviniai ir artilerija siunčia kiekvieną
atskirą šūvį (`gun_shot`, be krypties), 40 mm priešlėktuviniai patrankos - savo serijas
(`fire_start`, `fire_stop`).

## Pataikymo rezultatai {#hit-outcomes}

Kiekvienam pataikymui į sausumos vienetą serveris siunčia pranešimą 0xF144 (UnitOnHit) tam
vienetui: keturi vieno baito laukai, ketvirtasis - bitai to, ką pataikymas padarė
(`selfCheck.unitMessages.outcome_*`):

| Bitas | Reikšmė | Įrodymas |
|---|---|---|
| 0x20 | sviedinio savas pataikymas | beveik visi ateina su 0xF0E9 pataikymu į vienetą per 5 ms; be jo - su sprogimu (skeveldros) |
| 0x01 | prasiskverbė (penetration) | kiekvienas pranešimas su 0x02, 0x04 ar 0x08 turi ir jį |
| 0x02 | kritinis pataikymas | dauguma kritinio pataikymo įrašų jį turi, daug dažniau nei atsitiktinai |
| 0x04 | sunaikinta | dauguma ateina su žudymo įrašu ir vieneto mirtimi per sekundę |
| 0x08 | didelis sugadinimas | kai kurie kritinio pataikymo įrašai jį turi; kitu atveju retai |

`hitOutcome` paima blogiausią: `kill` (0x04), `critical` (0x02 arba 0x08), `penetration` (0x01),
`nonpenetration` (vien 0x20). Pataikymas poruojamas su artimiausiu neporuotu 0xF144 su 0x20 jo
vienetui per 5 ms. Žaidimo pataikymo kamera atskiria rikošetą nuo neprasiskverbimo, bet joks čia
rastas bitas ar laukas to neatskiria: pirmieji trys baitai kiekvieną kartą skiriasi ir jų reikšmė
nežinoma. Kliento įrašai siunčia 0xF144 tik paties žaidėjo orlaiviui, visi bitai išjungti: orlaivių
ir laivų pataikymai neturi rezultato.

## Šaudmenys {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Sprogstamasis ar ne.** Sviedinys, kuris sprogsta, siunčia 0xF133 (UnitOnExplosion) su šaulio uid ir
  pataikymo numeriu; pataikymas su juo yra `explosive`, likusieji - `kinetic`.
* **Patranka ir jos lizdas.** 0xF0BD (UnitBulletRearm) yra kitas įkrautas šovinys: ginklo indeksas
  technikos ginklų sąraše, šaudmenų lizdas ir likę šoviniai. Rankinio pakrovėjo pakrovimas ateina
  pastovų perkrovimo laiką po kiekvieno jo pataikymo, automatinės patrankos - po kelių dešimtųjų
  sekundės. Šaulio pataikymai grupuojami pagal techniką, parašą ir seriją; grupė yra ginklo, jei tas
  ginklas įkrauna šovinį per 20 s po pusės ar daugiau jos pataikymų su pastoviu delsimu. `ammoSlot` yra
  `weapon/slot` - lizdas, įkrautas prieš pataikymą: greičiausiai tas, kuris iššautas, nebent žaidėjas
  tuo tarpu pakeitė šaudmenis. Kulkosvaidžiai 0xF0BD nesiunčia.
* **Sviedinys.** Žudymo ginklas yra sviedinio id (`125mm_3bm46`); paskutinis žudiko pataikymas į auką
  priskiria jį to šaulio lizdui, kai patrankos kalibras sutampa. Jo tipas ir kalibras paimti iš ginklo
  failo (`bulletName`, `bulletType`, `caliber`; `apds_fs_*` - APFSDS, `heat_fs_*` - HEAT-FS, `he_*` - HE
  ir t. t.).
* **Likusiųjų kalibras:** lizdo ginklo; kulkosvaidžių grupės - vienas kulkosvaidžio kalibras, kurį jos
  parašas gali turėti; kitu atveju pagrindinės technikos patrankos. Be diegimo (`--game`) nėra tipo, vardo
  ar kalibro, išskyrus `explosive` / `kinetic`.

Nerasta: rikošetas. Keletas kitų pranešimų neša pataikymo šaulį ir numerį (0xF0C2, greičiausiai
pataikymo kameros kelias per techniką; 0xF117, 0xF13C, 0xF13E); jie išsaugomi papildomame faile, bet
neiššifruojami. Neprasiskverbimas lieka `nonpenetration`.

## Technikos gaisrai {#vehicle-fires}

Gaisre esanti technika rodoma kiekvienam klientui: serveris siunčia esybės pranešimą technikai (įvykis
`0a519c58`), kuriame išvardyti jai degantys gaisrai, kai tik sąrašas pasikeičia. Kiekvienam gaisrui: du
16 bitų id (antrasis - pažeidimo modelio mazgas), jo rūšis, ir -1, kol gaisras neįsijungia. Gaisras,
užkurtas pataikymo, gauna ir pranešimą su tašku, kur jis dega, technikos rėmelyje (x - pirmyn, y -
aukštyn, z - kairėn).

Eilutės: `fire_on`, kai gaisras atsiranda sąraše, `fire_off`, kai jo nebėra, technikoje, su `fireId`
(`first:node`), `fireKind` ir, gaisrams, kuriuos užkūrė pataikymas, `fireLocalX/Y/Z` (pirmyn, aukštyn,
dešinėn). Kai technika jau negyva, jos sąrašas dažnai nebesiunčiamas: jos gaisrai baigiasi su jos griuvėsiais,
arba su esybe, arba su įrašu (`selfCheck.fires`).

Patikrinta: kiekvieną kartą, kai tanko gaisrų gesinimo priemonių skaičius sumažėjo, gaisras per trumpą
laiką dingo iš sąrašo; dauguma gaisro taškų yra toje pačioje technikos pusėje kaip pataikymas, kuris jį
užkūrė. Rūšys yra skaičiai; kas jos reiškia, nežinoma, kaip ir tai, kuri dalis yra mazgas. Orlaiviai
tokių sąrašų nesiunčia: degantis orlaivis neskaitomas.

---

Dalis [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Šaltinis: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
