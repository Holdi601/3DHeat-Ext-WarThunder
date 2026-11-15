---
title: Lidmašīnas
nav_order: 11
lang: lv
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Lidmašīnas {#aircraft}

Lappuse lasītājiem, kuri grib zināt, no kurienes nāk lidmašīnu kolonnas un cik tām var uzticēties. Katra pārbaude zemāk salīdzina vērtību ar kaut ko, ko atkārtojums saka otrā, neatkarīgā veidā; dota tikai metode un atbilstība.

## Kabīnes instrumenti {#cockpit-instruments}

Ziņojums 0xD04A nosūta ieraksta spēlētāja mērinstrumentus kā (numurs, vērtība) pārus: četrus sekundē arkādes kaujās, tikai mainītās vērtības simulatora kaujās. Numuri veido vienu sarakstu visām kabīnēm, un kabīne sūta tos mērinstrumentus, kādus tās modelis satur. Spēles kods nosaka, kurš numurs ir kurš mērinstruments, tāpēc katrs numurs tika nosaukts pēc tā, ko tas dara, un pārbaudīts pret atkārtojumu (`convert.INSTRUMENTS` satur rezultātu; neko nenolasa no instalācijas):

| Numurs | Nosaukums | Pārbaudīts pret |
|---|---|---|
| 0 | indicētais gaisa ātrums, m/s | celiņa ātrums, koriģēts pēc gaisa blīvuma: korelācija 0,99 |
| 39 | kāpšanas ātrums, m/s | celiņa kāpšanas ātrums: korelācija virs 0,99 |
| 40, 41 | augstums, m; augstums modulo 1000 | celiņa augstums, dažu metru atšķirībā |
| 52, 53 | mākslīgā horizonta sašķiebums un pacēlums | mīnus tabulas roll un pitch, mazāk nekā 1 grāds atšķirībā |
| 64 | kompass | tabulas heading, mazāk nekā 0,1 grāds atšķirībā |
| 15–20 | kāju pedāļi | sānu spēks uz lidmašīnu |
| 23, 31 | stick: elevator un ailerons (zīme kā kabīnes modelim) | uzbrukuma leņķis; sašķiebuma ātrums |
| 69, 71, 73 | pulkstenis: stundas (12 stundu ciparnīca), minūtes, sekundes | ierakstošā datora vietējais laiks, līdz minūtei |
| 75 | ieplūdes spiediens, atm | augstāks kara avārijas jaudā nekā pilnā gāzē |
| 81–86, 87–92, 93–98 | apgriezieni katram dzinējam, apgriezieni modulo 1000, apgriezienu mērinstruments | viens otram precīzi; dzinēja apgriezieni: korelācija virs 0,97 |
| 195 | degviela | krītas visa lidojuma laikā, atkal pilna atdzimstot |
| 228–230 | šasijas kājas, 1 nolaista | nolaista tikai tuvu aerodromu augstumam un nolaišanās ātrumā |
| 240, 241 | gāze katram dzinējam (1,1 kara avārijas jauda vai pēcdedzinātājs) | lidojuma ieraksta gāze |
| 330–332, 346–348 | munīcijas skaitītāji (divi vienādi komplekti) | ieroču komplekta šāvieni, krītas kopā ar lidojuma ieraksta šāviniem |
| 135, 159 | eļļas un cilindru galvas temperatūra | iespējams: tās paaugstinās visa lidojuma laikā |
| 58, 61 | slīdes bumba, pagriezienu adata | iespējams: tās seko sānu spēkam un pagriešanās ātrumam |
| 223 | gaisa bremze | iespējams: tiek iestatīta tikai pieejā |
| 490–497, 500–505 | riteņu bremzes | iespējams: tiek iestatītas tikai stāvot uz aerodroma |

Vēl dažus numurus sūta, kuru nozīme nav zināma; tie paturēti mača dokumenta `authorInstruments.notNamed`.

Tabulas `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` un `throttle` nāk no šiem, ieraksta spēlētāja paša rindās, ņemot pēdējo ziņojumu ne vairāk kā 0,2 s pēc paraugs.

## Lidojuma ieraksti {#flight-entries}

Katra lidmašīnas lidojuma ieraksts (paketes tips 2) satur, papildus tās pozīcijai un orientācijai:

- **Ātrums**: 32 bitu vārds pēc orientācijas. Biti 31, 30 un 29 ir x, y un z zīmes; tad ātrums 11 bitos ar soli 500/2047 m/s (apstājas pie 500 m/s), tad |x| un |y| kā ātruma daļas 9 bitos katrs, un z ir tas, kas padara vektoru par vienības vektoru. Pārbaudīts pret soli starp saņemtajiem paraugiem: virziens atbilst daļas grāda robežās ieraksta spēlētājam un apmēram 2 grādu robežās visiem pārējiem; ātrums 0,2 % robežās. `selfCheck.flightEntries`.
- **Šāvieni katrā ieročā**: saraksts pirms pozīcijas, viens vienums katram ieročam, vispirms atlikušie šāvieni. Ieraksta spēlētāja saraksts vienāds ar kabīnes skaitītājiem vienu tiku vēlāk gandrīz katram paraugam.
- **Vadība un gāze**: 7 baiti pēc ātruma, nolasīti kā 14 nibbles. Ieraksta spēlētājam — katrā tikā: 1 elevator, 2 ailerons, 3 rudder (8 miera stāvoklī), 11 gāze piecpadsmitdaļās (15 arī kara avārijas jaudai un pēcdedzinātājam), 4 riteņu bremzes, 5 gaisa bremze, 8 iespējams bremzes padebesis. Citu lidmašīnu nibbles mainās tikai dažas reizes kaujā un nav to vadība tajā brīdī.
- **Dzinēji**: katram dzinējam stāvokļa baits (0 izslēgts; 1–6 startē; 7 darbojas; 8 miris), 16 bitu vērtība tikai ar pēcdedzinātāju (32767 pilns), un baits tikai pēc tam, kad dzinējs tika trāpīts. Vairums lidmašīnu, kuru dzinējs kļūst "miris", tiek nogalinātas vai beidzas minūšu laikā.

## Refleksijas dati {#reflection-data}

Ziņojumi 0xF02D un 0xF0AA replicē spēles numurētos objektus: katram objektam tā ID (augšējie 5 biti veids, zemākie 11 — indekss) un lauku tabula. Veids 14 ir spēlētāju slots (2. lauks lietotāja ID un vārds, 9 — komanda), veids 15 — komandas (indekss 1 un 2):

- Slota 39. lauks satur tā statistiku fiksētās vietās: nogalinājumi (nobīde 0), komandas nogalinājumi (2), nāves (4), jūras nogalinājumi (10), MI nogalinājumi (12), MI sauszemes nogalinājumi (14), palīdzības (20), kapitāla zonas (22), zonas bojājumi (24, 32 bitu), bojājumu balva (40, 32 bitu), raķešu izvairīšanās (50). 38. lauks sākas ar punktiem, 42. lauks ir vienība. Kaujas beigās katra vērtība ir vienāda ar rezultātu katram spēlētājam (`selfCheck.scoreboardVsResults`). Kur tiek glabāti sauszemes nogalinājumi, nav zināms.
- Komandas 7. lauks ir tās punkti: beigās tas ir vienāds ar tās spēlētāju punktu summu rezultātos. 3. lauks, visticamāk, ir tās biļetes.
- Katrs ziņojums sūta tikai mainītos laukus, tāpēc `scoreboard` mača dokumentā uzskaita katra spēlētāja statistiku un katras komandas punktus katrā izmaiņā.

## Novērtēta kustība un izlīdzinātājs {#dead-reckoning-and-the-smoother}

Klienta atkārtojums ieraksta katru lidmašīnu četras reizes sekundē, kā to klients zīmēja. Starp atjauninājumiem, ko tas saņem tālai lidmašīnai, klients tās pārvieto tālāk pa tās pēdējo ātrumu un pagriež pēc pēdējiem ātrumiem, un nākamajā atjauninājumā uzmet to tur. Nolasīts kā tas ir, celiņš iet taisni, tad lec. Nekas lidojuma ierakstā neatzīmē, kuri paraugi tika saņemti; novērtētu paraugu atrod pēc tā, kas tas ir: tas turpina taisno līniju no divām iepriekšējām paraugiem ar to tempu, 3 cm robežās.

Cik tas svarīgi, atkarīgs no kaujas: arkādes kaujās apmēram puse citu lidmašīnu paraugu var būt novērtēti, simulatora kaujās — tikai dažas procenti. Izlīdzinātājs samazina soļus virs 15 g apmēram piecas reizes (`selfCheck.deadReckoning`). Ieraksta spēlētāja paša lidmašīna nav klienta ekstrapolēta, un tā paliek kā ir.

Pēc noklusējuma (`--no-smoothing` to izslēdz) visu vienību, izņemot ieraksta spēlētāja paša, celiņi tiek novietoti tur, kur saņemtie stāvokļi saka, ka tie bija: novērtēts paraugs iet pa līkni caur saņemtajiem paraugiem pirms un pēc tā, katrs ar savu ātrumu; virs 3 s taisnā līnija tikai tiek saliekta uz nākamo saņemto paraugu, tāpēc neviens paraugs nepārvietojas tālāk nekā klienta pašas korekcijas. Tā orientācija tiek vienmērīgi pagriezta no vienas saņemtās orientācijas uz nākamo. Saņemtie paraugi tiek izlīdzināti ne vairāk kā par 2 m vai 0,04 s to ātruma; stabils pagrieziens paliek tāds, kāds ir. Atkārtojuma paša vērtības paliek `Raw` kolonnās.

## Orientācija, pārbaudīta {#attitude-checked}

Ieraksta spēlētāja paša lidmašīnā virziens atrodas grāda robežās (mediāna) no kustības virziena, pacēlums — dažu grādu robežās no kāpuma leņķa, un skaidros pagriezienos sašķiebums ir pagrieziena zīmē gandrīz katram paraugam: lidojuma modeļa sašķiebums ir kreisais spārns uz leju pozitīvs, un tabula to pagriež uz labo spārnu uz leju pozitīvu (`selfCheck.aircraftAttitude`). 10 bitu leņķi sola 0,18 grādus. Sauszemes vienību orientācija tiek pārbaudīta pret to šāvieniem ([Torņi](ground.md#turrets)).

---

Daļa no [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentācija](https://holdi601.github.io/3DHeat/)). Avots: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
