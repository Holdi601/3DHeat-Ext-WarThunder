---
title: Sauszemes vienības un kamera
nav_order: 12
lang: "lv"
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Sauszemes vienības un kamera {#ground-units-and-camera}

Lappuse lasītājiem, kuri grib zināt, no kurienes nāk tanku torņa, kameras un kaujas režīma kolonnas un cik tām var uzticēties. Pārbaudes
dod tikai metodi un atbilstību.

## Torņi {#turrets}

Tanka sauszemes stāvoklī (16 bitu orientācija) pēc pozīcijas ir 141 bits, kas nav nolasīti, un pēc tam katram tornim 62 biti: torņa
virziens (yaw) un lielgabala pacēlums (pitch) (katrs 16 bitu, 360/65536 grādi solī, ar zīmi), un 30 biti, kas nav nolasīti; tad
izlīdzināšana, un dažos stāvokļos vēl 200 biti. Torņu skaits ir baits, kas nosūtīts pirms stāvokļa. Stāvoklis, kura garums neiederas,
nedod torņus (statiskās vienības sūta īsāku stāvokli). Virziens ir attiecībā pret korpusu, pulksteņrādītāja virzienā pozitīvs, 0 tieši
uz priekšu; pacēlums ir attiecībā pret korpusu, uz augšu pozitīvs.

Kā tas pārbaudīts:

- **Pret šāvieniem:** katram tanka galvenā lielgabala trāpījumam tā pasaules virziens (korpusa orientācija pagriezta ar torņa yaw un
  lielgabala pitch) pret līniju no šāvēja līdz trāpītajai vienībai, vismaz 30 m attālumā: katrā kaujā mediāna ap 98 % 3 grādu robežās
  virzienā un 99 % pacēlumā (`selfCheck.turretsVsShots`). Pārējie galvenokārt ir trāpījumi no ložmetēja citā tornī.
- **Pret ieraksta spēlētāja tēmēšanu:** tā paša tanka spēlētājs sūta tēmēšanas pasaules leņķi (pretēji pulksteņrādītājam no austrumiem),
  pacēlumu un attālumu. Korpusa virziens plus torņa yaw atrodas pusgrāda robežās (mediāna) no tēmēšanas.

**Servera atkārtojumi** (0xF074) sūta katra tanka stāvokli tādā pašā izkārtojumā, kam seko citi dati, tāpēc nolasa katru torni, kura
divi leņķi atrodas stāvoklī (vismaz galveno nolasa gandrīz katrai tanka rindai). Tas ir tornis, nevis kamera:

- **Pret šāvieniem**, kā iepriekš: katrā kaujā virs 90 % 3 grādu robežās virzienā un 99 % pacēlumā.
- **Pret skatu:** servera atkārtojums sūta katra spēlētāja tēmēšanu (`viewYaw`, `viewPitch`). Tornis seko skatam pusgrāda robežās
  (mediāna), bet griežas daudz lēnāk nekā skats šūpojas, kā to dara torņa piedziņa (`selfCheck.turretVsView`).
- **Bet ne vienmēr piedziņas ātrumā:** paraugs pēc parauga nosūtītā vērtība dažreiz lec uz tēmēšanu, kad tēmēšana ir tuvu lielgabalam —
  ātrāk, nekā jebkura piedziņa pagriežas (`selfCheck.turretLimit`).

Tāpēc tabulā tornis ir **turēts pie savas piedziņas**: `turretYaw` / `gunPitch` virzās uz nosūtīto vērtību ne ātrāk par galvenā
lielgabala griešanās ātrumu no instalācijas transportlīdzekļa faila (reizināts ar 1,3 apkalpes prasmēm un modifikācijām; 45 un 20 grādi
sekundē, kur instalācijā nekas nav minēts). Katrā galvenā lielgabala trāpījumā tornis ir iestatīts tieši uz šāviena līniju, un atpakaļgaitas
pārbaude to laikus nogādā tur (`selfCheck.turretLimit`). `shot` rinda nes arī šos `turretYaw` / `gunPitch`. Nosūtītā vērtība paliek
`turretYawRaw` / `gunPitchRaw`. Tankam, kura stāvoklī nav torņa, torņa kolonnas ir tukšas (skatītājs var atkrist atpakaļ uz `viewYaw`).
`gunPitch` lielākoties ir nedaudz virs `viewPitch` tālumā: lielgabala pacēlums šāviņa kritumam.

Kuģu stāvokļiem ir cits izkārtojums; to torņi netiek nolasīti. Lidmašīnas nesūta galvas vai skata virzienu; pretgaisa lielgabalu ziņojums
0xD020 paliek nenolasīts.

## Kamera {#the-camera}

Ziņojums 0xD043, apmēram 20 reizes sekundē, ir paša ieraksta spēlētāja atkārtojuma kamera: 1. lauks — kvaterniona, kas pagriež kameras
priekšpusi uz to, kur tā skatās; 2 — kameras vieta no transportlīdzekļa, ko tā seko (m); 4 — tā pati nobīde transportlīdzekļa pašā
koordinātu sistēmā (x uz priekšu, y uz augšu, z pa kreisi); 5 — kur spēlētājs tēmē (vienības vektors); 3 — tālummaiņa (ap 1,2 tanka trešās
personas skatā, ap 1,0 lidmašīnā, lielāka ieroču tēmeklī vai caur binokli). Pārbaudīts: 4. lauks ir 2. lauks, pagriezts transportlīdzekļa
koordinātu sistēmā, 0,5 m robežās gandrīz katram ziņojumam; kameras priekšpuse atbilst tēmēšanas virzienam. Atkārtojums nesūta lauka
platumu grādos, tikai tālummaiņu.

Tabulā kamera ir atsevišķs celiņš: veids `camera`, celiņš `<spēlētājs> camera #ca`, rinda ne retāk kā ik pēc 0,1 s, sekotā
transportlīdzekļa vietā plus 2. lauks, skatoties pa kvaternionu (`dirX/Y/Z`, `heading`, `pitch`, `roll`), ar `zoom`, `aimHeading` un
`aimPitch`, un `otherLife` — dzīve, ko tā seko. `selfCheck.camera` skaita rindas un pārbaudi.

## Celiņa beigas {#end-of-a-track}

Celiņš tiek zīmēts no pirmās rindas līdz pēdējai. Ja tā vienība ir pazudusi, pirms atkārtojums beidzas, tās pēdējā rinda ir `despawn`
rinda pēdējā vietā: tajā laikā, kad spēle noņēma tās vienību (ja tas notika 6 s laikā pēc tās pēdējā paraugu), citādi pēdējā paraugā. Celiņš
bez tā ilgst līdz atkārtojuma beigām. Viena celiņa rindas var būt tālu viena no otras (tāls objekts vai vraks tiek atjaunināts ik pēc dažām
sekundēm, vraks dažreiz pat ik pēc dažām minūtēm); tā pēdējais stāvoklis paliek spēkā līdz nākamajai rindai.

## Kaujas režīms {#battle-mode}

Galvenes baits pozīcijā 688 satur grūtības režīmu zemākajos četros bitos: 0 arkāde (AB), 5 reālistisks (RB), 10 simulators (SB). Pārbaudīts
pret kaujas tipiem, par kuriem atkārtojumi bija zināmi. Spēles režīms ir `ground`, ja misija ļauj tankiem parādīties, citādi `naval`, ja
ļauj kuģiem, citādi `air` (`allowedUnitTypes`); misijas pašas režīms nāk no tās atslēgas (`missions/_Dom`), un to nosaka no jūsu instalācijas
`lang/missions_versus.csv`. Tā pati atslēga ir faila nosaukuma daļa `<mode>` un mača ID (`Conq4`, `Dom`), izlaista, ja galvenē tādas nav.

---

Daļa no [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentācija](https://holdi601.github.io/3DHeat/)). Avots: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
