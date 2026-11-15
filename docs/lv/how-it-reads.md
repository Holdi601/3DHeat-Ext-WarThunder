---
title: Kā tas nolasa atkārtojumu
nav_order: 10
lang: lv
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Kā tas nolasa atkārtojumu {#how-it-reads-a-replay}

Šī lappuse ir paredzēta cilvēkiem, kuri grib zināt, ko konvertētājs nolasa, kā tas pārbaudīts un tādēļ cik lielā mērā var uzticēties katrai
kolonnai. Lai pārvērstu atkārtojumus, tā nav vajadzīga.

Lasīšana pārbaudīta uz klientu atkārtojumiem gaisa arkādes, gaisa simulatora un jūras kaujām, uz servera atkārtojumiem sauszemes kaujām un —
2025. gada izkārtojumiem — uz publiskajiem paraugu atkārtojumiem no [wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder).
Katra pārbaude salīdzina vērtību ar kaut ko, ko atkārtojums saka otrā, neatkarīgā veidā; šeit dota tikai metode un atbilstība.

## Kas tiek nolasīts un pārbaude {#what-is-read-and-the-check}

| Daļa | Statuss un pārbaude |
|---|---|
| Galvene, karte, misija, sākuma laiks, sesija; rezultāti | katrs fails |
| Misijas iestatījumi (blk aiz galvenes) | režīms, laika apstākļi, robežas, `stars` (datums, laiks, vieta) |
| Pakešu plūsma (zlib 2025., zstd 2026.) | katra pakete ir izšķirta |
| Lidmašīnu pozīcijas un orientācija (2026. izkārtojums) | 4 paraugi sekundē, nav atstāta neviena nelasīta pakete; virziens atbilst kustības virzienam |
| Lidojuma paketes, kas ir priekšā savam laikam | pēc tīkla traucējuma klienta atkārtojuma lidojuma pakete dažreiz satur katru citu lidmašīnu, kur tā būs apmēram pēc 0,75 s. Apsteigšana tiek mērīta katrai paketei, un katrai apsteidzošajai lidmašīnai tiek dots laiks, ko tā pārstāv (`selfCheck.flightPacketsRetimed`) |
| Lēcieni no novērtētas kustības | solis no novērtētas kustības ir mērīts no pēdējā saņemtā stāvokļa, tāpēc klienta korekcijas vairs nelauž trajektorijas ([Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)) |
| Teleportācijas | trajektorija tiek pārtraukta, kad vienība pārvietojas tālāk, nekā tā var: vispirms pret tās veidu (lidmašīna 750 m/s, sauszemes un kuģi 40 m/s, ieroči 1800 m/s), tad pret tās pašas gaitu. Katrs pārtraukums ir uzskaitīts `trackBreaks` ar tā iespējamo cēloni (atdzimšana, spēles pārvietots spēlētājs, tālas vienības korekcija). Pēc pārtraukumiem neviens solis starp vienas trajektorijas rindām nav ātrāks, nekā tā veids atļauj (`selfCheck.stepSpeed`) |
| Sauszemes un kuģu pozīcijas (0xF073 / 0xF074) | nav atstāta neviena nelasīta pakete. Virziens, pacēlums un sānu sašķiebums no 16 bitu orientācijas: virziens atbilst kustības virzienam ar nobīdi apmēram 2 grādi (mediāna); pacēlums skaita 180/65536 grādus solī; ar pagrieztu sānu sašķiebuma zīmi lielgabala virziens no korpusa un torņa lielākajai daļai tanku šāvienu norāda uz trāpīto vienību. Kuģi atrodas ūdens līmenī |
| Torņi | tanku torņa virziens un lielgabala pacēlums: skat. [Torņi](ground.md#turrets) |
| Iepakotie augstumi virs zemes | pozīcijas, kas iepakotas 64 bitos, augstumu skaita no -100 m lielākajā daļā līmeņu un no ūdens līmeņa dažos; nobīde tiek izmērīta katrā atkārtojumā no vienībām, kas redzētas abos veidos (`selfCheck.packedGroundHeight`) |
| Entītiju plūsma (izveide, iznīcināšana) | katra izveide ir nolasīta. Izkārtojums nāk no Dagor Engine publicētā koda; War Thunder pašu komponenšu tipi tiek izlaisti, atrodot, kur sākas nākamā komponente. Katras vienības transportlīdzeklis un spēlētāja slots ir vienādi ar to, ko nosauc nogalināšanas un trāpījumu ieraksti, katram pārbaudītajam ierakstam |
| Kas vadīja kuru vienību, MI vienības, kuģi, sauszemes mērķi | no entītiju plūsmas: katrai vienībai ir savs transportlīdzeklis un komanda, katra spēlētāja vienībai — tās spēlētājs |
| Nogalināšanas pret rezultātiem | katra spēlētāja nāves ir vienādas ar rezultātu nāvēm; rezultāti skaita vairāk nogalinājumu, jo klientam nav sūtīts katrs nogalinājums. Atkārtojums, kas sākas pēc kaujas sākuma, satur tikai nogalinājumus pēc tā |
| Nogalinājumi, kritiskie trāpījumi, smags bojājums | katrs fails |
| Iznīcinātie moduļi (0xF118) | vienība un daļas numurs; daļas nosaukums prasa transportlīdzekļa bojājumu modeli, kas atkārtojumā nav |
| Izlaistie ieroči (entītiju plūsma) | izlaišanas punkts ir kādus 10–20 m (mediāna) no tuvākās vienības, un to uzskata par palaidēju |
| Ieroči lidojumā (0xF0DB) | raķetes, raķetes un bumbas, katra saistīta ar savu entītiju |
| Bumbas bez lidojuma ierakstiem | bumba bez tiem tiek aprēķināta no izlaišanas līdz triecienam (gravitācija un pretestība, paraugs ik 0,1 s, `extrapolated` true). Pārbaudīts pār jūru, kur trieciena augstums ir zināms: aprēķinātie krituma beigas ir apmēram 15 m robežās no ūdens. Mača dokumentā šādam ieroču ir `ballisticImpact`; `counts.bombsBallistic` tos skaita |
| Spēlētāju slots, tērzēšana | katrs fails |
| Sprādzieni, pretgaisa šāvienu sprādzieni, balvas, atklāšanas, laika apstākļi, misijas objekti | nolasīti; pozīcijas pārbaudītas acīm skatītājā |
| Ieraksta spēlētāja instrumenti (0xD04A) | nosaukti pēc to darbības: [Kabīnes instrumenti](aircraft.md#cockpit-instruments); pārējie zem `notNamed` |
| Lidojuma ierakstu citi lauki | ātrums, munīcija, vadība, dzinēji: [Lidojuma ieraksti](aircraft.md#flight-entries) |
| Notikumu rindu orientācija | katra notikuma rindā ir tās vienības virziens, pacēlums, sānu sašķiebums un skata vektors tajā brīdī |
| Spēlētāju statistika un komandu punkti | kaujas beigās katra statistika ir vienāda ar rezultātu katram spēlētājam: [Refleksijas dati](aircraft.md#reflection-data) |
| Ieroču un transportlīdzekļu nosaukumi | no tavas instalācijas angļu lokalizācijas; dažiem kuģu noklusējuma jostām un aerodromu radariem spēlē nav nosaukuma |
| Spēlētāji un MI | neviena rezultātu spēlētāja rinda nav MI, katra rinda, kas nav MI, ir rezultātu spēlētāja (`selfCheck.identity`) |
| Vraki | vienības paraugi pēc tās nāves turpinās nākt; sauszemes vienības vai kuģa vraks ir `alive` 0, līdz tā entītija tiek noņemta, un paliek viena trajektorija; lidmašīnas saglabā `alive` 0 ne ilgāk par 60 s (`selfCheck.wrecks`) |
| Transportlīdzekļu maiņa | spēlētāja vienība, kas vēl ir dzīva, kad parādās tā paša spēlētāja nākamā vienība, tiek tur izbeigta (transportlīdzeklis, kas palicis stāvam). `selfCheck.vehicleSwitch.twoLiveVehicles` jābūt 0 |
| Kaujas režīms | [Kaujas režīms](ground.md#battle-mode) |
| Lidmašīnas 2026. gada servera atkārtojumā | nolasītas 2026. gada izkārtojumā; virziens un sānu sašķiebuma zīme atbilst pagriezieniem; vietturu lidmašīnas un izlūkdroni neko nenes |
| Servera atkārtojuma spēlētāji | atrasti pēc vārda slotos; katra statistika ir vienāda ar rezultātu (`selfCheck.players`) |
| Lidmašīnas 2025. gada servera atkārtojumos un versijā 101286 | nav nolasītas: to lidojuma paketēm ir cits izkārtojums |

## Ziņojumi vienībām {#messages-to-units}

Katra 4. tipa pakete ir mpi ziņojums Dagor Engine daNet: saņēmēja objekta ID, tad (kad tā zemākie 11 biti ir visi uzstādīti) objekta ext UID,
ziņojuma ID un saturs. Ziņojumam vienībai kā ext UID ir vienības entītijas ID, `index << 10 | generation`. Pārbaudīts: katrs šāds ziņojums
nosauc entītiju, kas ir dzīva šajā brīdī.

Speciālistiem ziņojumi nolasās šādi:

| Ziņojums | Ko tas ir, un pārbaude |
|---|---|
| 0xF0E9 UnitHitEffects | viens lidojuma trāpījums: šāvēja uid un trāpījuma punkts vienības koordinātu sistēmā (x uz priekšu, y uz augšu, z pa kreisi): centimetri uz lidmašīnām un kuģiem, 20/32768 m solī uz sauszemes vienībām (pielāgots tanku torņu izmēram). `hitLocalX/Y/Z` metros. Kļūst par `shot` rindu ([Šaušana](hits.md#gunfire)). Gandrīz katra trāpījuma un nogalināšanas ieraksta uzbrucējs ir starp šiem šāvējiem; trāpījumu punkti atrodas šāvējam pretējā pusē |
| 0xF133 UnitOnExplosion | tas pats šāvēja uid |
| 0xF04B OnUnitDead | `dead` rindas: katram nogalināšanas ieraksta upuram ir viena 2 s laikā |
| 0xD047 FmwRpm | dzinēju apgriezieni (`rpm`); sakrīt ar kabīnes apgriezienu skaitītāju |
| 0xF0B1, 0xF0A0 | `gun_shot` rindas: atsevišķi smagās pretgaisa un artilērijas šāvieni |
| 0xF01B, 0xF01C | `fire_start`, `fire_stop` rindas: 40 mm pretgaisa lielgabalu sērijas (lielgabals šauj; uguns uz transportlīdzekļa ir `fire_on`, skat. [Transportlīdzekļu ugunsgrēki](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` rindas |
| 0xD0FE ProjectileHitReplay | ieraksta spēlētāja paša trāpījumi un trāpīšana, ar ieroci un munīciju, nosaukti no instalācijas (`projectileHitReplays`) |
| 0xF13E, 0xF031 | trāpījuma vizuālais efekts un efekts, kas parādīts uz vienības; tie nāk kopā ar trāpījumu uz to pašu vienību |
| 0xD041 | viens katram aizsardzības lielgabalam lidmašīnā, divas reizes sekundē; tā indeksi atbilst lidojuma modeļa ložmetēja ieročiem |
| 0xD048, 0xF117 | izkārtojums nolasīts, nozīme nav zināma |
| pārējie (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | papildfailā ar to vienību un laukiem |

Nosaukumi ir kopienas (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Vēl nolasīts {#also-read}

- **Entītiju plūsmas replikācija** (0x22, 0x23): katrai entītijai bloks ar komponenšu vērtībām: kuģu remonta taimeri, patēriņa priekšmetu
  skaits, īpašnieka un komandas maiņa, dzinēja pārkaršana. Skaitīts `counts.replicatedComponents`; vērtības papildfailā.
- **Misijas skripta darbības** (0xF028) un **padomi** (0xF0EC): `triggers`, `hints`. **Misijas progress** (0xF07A, 0xF07C): `missionProgress`.
- **Atkārtojuma kamera** (0xD043): skat. [Kamera](ground.md#the-camera).

## Nav nolasīts un kāpēc {#not-read-and-why}

- **Entītiju ziņojumu nosaukumi un saturs** (0x20, 0x21): klases numurs ir vieta sarakstā, kas ieprogrammēts spēlē; tas netiek sūtīts un nav
  tā datos. Divi tiek nolasīti (transportlīdzekļa ugunis un tā ugunsdzēsēji); pārējie tiek paturēti pilnībā ar savu entītiju un klases numuru.
- **Citi replicētie objekti** (kas nav spēlētāju slots vai komandas): nolasīti un paturēti, bet nav nosaukti; rezultātos nav, ar ko tos pārbaudīt.
- **Citu lidmašīnu vadība, dross un šāvieni**: atjaunināti tikai reizēm; paturēti lidojuma papildfailā, nevis tabulā.
- **Lidmašīnu ugunsgrēki**: nekur ziņojumos nav atrasti; lidmašīnai, kas deg, nav `fire_on` rindas.
- **Izlaisto ieroču nosaukumi**: bumbas vai raketes entītijai nav nosaukuma; nogalināšanas ieraksti nosauc ieroci, ar ko tika nogalināts.
- **Šāvieni, kas netrāpīja**: atkārtojums satur tikai trāpījumus.

`counts.messageIdsNotRead` un `selfCheck` katrā mača dokumentā saka, ko jauns atkārtojums satur un cik labi tas nolasīts.

---

Daļa no [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentācija](https://holdi601.github.io/3DHeat/)). Avots: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
