---
title: Trāpījumi, šaušana un ugunsgrēki
nav_order: 13
lang: lv
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Trāpījumi, šaušana un ugunsgrēki {#hits-gunfire-and-fires}

Lappuse lasītājiem, kuri grib zināt, no kurienes nāk trāpījumu, munīcijas un ugunsgrēku kolonnas. Pārbaudes dod tikai metodi un atbilstību.

## Šaušana {#gunfire}

Katrs lidojums, kas trāpīja vienību, ir atkārtojumā (ziņojums 0xF0E9): `shot` rinda šāvēja pozīcijā trāpījuma brīdī, `targetX/Y/Z` ir trāpījuma
punkts (trāpītā vienība, pārvietota par trāpījuma punktu tās koordinātu sistēmā, pagriezta pēc tās orientācijas), virziens uz to un `other` —
trāpītā vienība. Šāviņi un lodes, kas nepieskārās, nav sūtītas: tās nav vienības, un ziņojumi par lidojumā esošajiem ieročiem satur tikai
raķetes, rakešu, bumbas un torpēdas. Spēlētāja atlikušie šāvieni (tā kolonna `ammo`) krītas, kad tas šauj, tāpēc viņa šāviena sērijas var tikt
atpazītas, bet ne tas, kurp šie šāvieni gāja. Smagie pretgaisa un artilērijas ieroči sūta katru atsevišķu šāvienu (`gun_shot`, bez virziena),
40 mm pretgaisa lielgabali — savas sērijas (`fire_start`, `fire_stop`).

## Trāpījumu iznākumi {#hit-outcomes}

Katram trāpījumam sauszemes vienībā serveris sūta ziņojumu 0xF144 (UnitOnHit) šai vienībai: četri vienu baitu lauki, ceturtais — bitu
kopums, kas parāda, ko trāpījums izdarīja (`selfCheck.unitMessages.outcome_*`):

| Bits | Nozīme | Pierādījums |
|---|---|---|
| 0x20 | paša šāviņa trāpījums | gandrīz visiem ir 0xF0E9 trāpījums uz vienības 5 ms laikā; bez tā — ar sprādzienu (šķembas) |
| 0x01 | tas caurdurās (penetrācija) | katrs ziņojums ar 0x02, 0x04 vai 0x08 to arī satur |
| 0x02 | kritisks trāpījums | vairums kritiskā trāpījuma ierakstu to satur, daudz biežāk nekā nejauši |
| 0x04 | iznīcināts | vairums nāk ar nogalināšanas ierakstu un vienības nāvi sekundes laikā |
| 0x08 | smags bojājums | daži kritiskā trāpījuma ieraksti; citādi reti |

`hitOutcome` ņem sliktāko: `kill` (0x04), `critical` (0x02 vai 0x08), `penetration` (0x01), `nonpenetration` (tikai 0x20). Trāpījums tiek
savienots ar tuvāko nesavienoto 0xF144 ar 0x20 uz tās vienību 5 ms laikā. Spēles trāpījuma kamera atšķir rikošetu no neiekļūšanas, bet
nevienš šeit atrastais bits vai lauks to nedara: pirmie trīs baiti mainās no trāpījuma uz trāpījumu un nav zināmi. Klientu atkārtojumi sūta
0xF144 tikai paša ieraksta spēlētāja lidmašīnai, visi biti notīrīti: lidmašīnu un kuģu trāpījumiem iznākuma nav.

## Munīcija {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Sprāgstošs vai nē.** Šāviņš, kas sprāgst, sūta 0xF133 (UnitOnExplosion) ar šāvēja uid un trāpījuma numuru; trāpījums ar to ir
  `explosive`, pārējie `kinetic`.
* **Lielgabals un tā slots.** 0xF0BD (UnitBulletRearm) ir nākamais ielādētais šāviņš: ieroča indekss transportlīdzekļa ieroču sarakstā,
  munīcijas slots un atlikušie šāvieni. Manuāla lādētāja ielāde nāk noteiktu pārlādēšanas laiku pēc katra tā trāpījuma, autopuškas — daļu
  sekundes pēc. Šāvēja trāpījumi tiek grupēti pēc transportlīdzekļa, paraksta un sērijas; grupa pieder ieroci, ja tas ielādē šāviņu 20 s laikā
  pēc pusei vai vairāk tās trāpījumu ar nemainīgu aizkavi. `ammoSlot` ir `weapon/slot`, slots, kas ielādēts pirms trāpījuma: visticamāk tas,
  kas tika izšauts, ja vien spēlētājs starplaikā nemainīja munīciju. Ložmetēji nesūta 0xF0BD.
* **Šāviņš.** Nogalināšanas ierocis ir šāviņa ID (`125mm_3bm46`); slēdzējs pēdējais trāpījums uz upuri piešķir to šāvēja slotam, ja
  lielgabala kalibrs sakrīt. Tā tips un kalibrs ir ieroča faila (`bulletName`, `bulletType`, `caliber`; `apds_fs_*` APFSDS, `heat_fs_*`
  HEAT-FS, `he_*` HE ...).
* **Pārējo kalibrs:** slota ieroča; ložmetēja grupas — viens ložmetēja kalibrs, ko tā paraksts var būt; citādi transportlīdzekļa galvenā
  lielgabala. Bez instalācijas (`--game`) nav tipa, nosaukuma vai kalibra, izņemot `explosive` / `kinetic`.

Nav atrasts: rikošets. Vairāki citi ziņojumi nes trāpījuma šāvēju un numuru (0xF0C2, visticamāk trāpījuma kameras ceļš caur transportlīdzekli;
0xF117, 0xF13C, 0xF13E); tie tiek paturēti papildfailā, bet nav atšifrēti. Neiekļūšana paliek `nonpenetration`.

## Transportlīdzekļu ugunsgrēki {#vehicle-fires}

Transportlīdzeklis, kas deg, ir redzams katram klientam: serveris sūta vienības ziņojumu transportlīdzeklim (notikums `0a519c58`), kurā ir
uz tā degošās ugunis, katru reizi, kad saraksts mainās. Katrai ugunij: divi 16 bitu ID (otrais — bojājumu modeļa mezgls), tās veids un -1,
kamēr uguns neiedegas. Uguns, ko iedegis trāpījums, saņem arī ziņojumu ar punktu, kur tā deg, transportlīdzekļa koordinātu sistēmā (x uz
priekšu, y uz augšu, z pa kreisi).

Rindas: `fire_on`, kad uguns parādās sarakstā, `fire_off`, kad tā ir pazudusi, pie transportlīdzekļa, ar `fireId` (`first:node`),
`fireKind` un, ugunīm, ko iedegusi trāpījums, `fireLocalX/Y/Z` (uz priekšu, uz augšu, pa labi). Kad transportlīdzeklis ir miris, tā saraksts
bieži vairs netiek sūtīts: tā ugunis beidzas kopā ar vraku, citādi kopā ar tā vienību, citādi kopā ar atkārtojumu (`selfCheck.fires`).

Pārbaudīts: ikreiz, kad tanka ugunsdzēsēju skaits samazinājās, uguns pazuda no saraksta sekundes daļas laikā; vairums ugunsgrēku punktu atrodas
tajā pašā transportlīdzekļa pusē kā trāpījums, kas to iedegis. Veidi ir skaitļi; nav zināms, ko tie nozīmē, kā arī kura daļa ir mezgls. Lidmašīnas
nesūta šādu sarakstu: lidmašīna, kas deg, nav nolasāma.

---

Daļa no [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentācija](https://holdi601.github.io/3DHeat/)). Avots: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
