---
title: Kaip įrankis skaito įrašą
nav_order: 10
lang: "lt"
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Kaip įrankis skaito įrašą {#how-it-reads-a-replay}

Šis puslapis skirtas žmonėms, norintiems žinoti, ką konverteris skaito, kaip tai patikrinta, ir kiek
pasitikėti kiekvienu stulpeliu. Jo nereikia, norint konvertuoti įrašus.

Skaitymas patikrintas su kliento įrašais oro arkadiniuose, oro simuliatoriaus ir jūrų mūšiuose, su
serverio įrašais sausumos mūšiuose, o 2025 m. formatams - su viešais pavyzdiniais įrašais iš
[wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder). Kiekvienas patikrinimas lygina
reikšmę su kitu, nepriklausomu būdu, kuriuo įrašas tai sako; čia nurodytas tik metodas ir sutapimas.

## Kas nuskaitoma ir patikrinimas {#what-is-read-and-the-check}

| Dalis | Būsena ir patikrinimas |
|---|---|
| Antraštė, žemėlapis, misija, pradžios laikas, sesija; rezultatai | kiekvienas failas |
| Misijos nustatymai (blk po antraštės) | režimas, oras, ribos, `stars` (data, laikas, vieta) |
| Paketų srautas (zlib 2025 m., zstd 2026 m.) | kiekvienas paketas įrėmintas |
| Orlaivių pozicijos ir orientacija (2026 m. išdėstymas) | 4 pavyzdžiai per sekundę, joks paketas neskaitomas; kryptis sutampa su judėjimo kryptimi |
| Skrydžio paketai prieš laiką | po tinklo sutrikimo kliento įrašo skrydžio paketas kartais rodo visus kitus orlaivius ten, kur jie bus maždaug po 0,75 s. Pirmavimas matuojamas kiekvienam paketui, ir kiekvienas pirmaujantis orlaivis gauna laiką, kurį jis reiškia (`selfCheck.flightPacketsRetimed`) |
| Įvertinto nuvažiavimo peršokimai | žingsnis iš įvertinto nuvažiavimo matuojamas nuo paskutinės gautos būsenos, todėl kliento pataisos nebepjauna trajektorijų ([Įvertinimas pagal nuvažiavimą](aircraft.md#dead-reckoning-and-the-smoother)) |
| Teleportacijos | trajektorija nupjaunama, kur jos vienetas nuvažiuoja toliau, nei gali: pirmiausia pagal jo rūšį (orlaiviai 750 m/s, sausuma ir laivai 40 m/s, ginklai 1800 m/s), tada pagal jo paties tempą. Kiekvienas pjūvis įrašomas `trackBreaks` su tikėtina priežastimi (atgimimas, žaidimas perkelia žaidėją, tolimo vieneto pataisa). Po pjūvių jokis trajektorijos eilučių tarpas nėra greitesnis, nei leidžia jos rūšis (`selfCheck.stepSpeed`) |
| Sausumos ir laivų pozicijos (0xF073 / 0xF074) | joks paketas neskaitomas. Kryptis, kėlimas ir posūkis iš 16 bitų orientacijos: kryptis sutampa su judėjimo kryptimi per maždaug 2 laipsnius (mediana); kėlimas žingsniuoja po 180/65536 laipsnio; su apverstu posūkio ženklu patrankos kryptis iš korpuso ir bokštelio beveik kiekvienam tanko šūviui rodo į pataikytą vienetą. Laivai stovi vandens lygyje |
| Bokšteliai | tankų bokštelio posūkis ir patrankos kampas: žr. [Bokšteliai](ground.md#turrets) |
| Supakuotos žemės aukščiai | pozicijos, supakuotos į 64 bitus, skaičiuoja aukštį nuo -100 m daugumoje lygių ir nuo vandens lygio kai kuriuose; poslinkis matuojamas kiekviename įraše pagal vienetus, matomus abiem formomis (`selfCheck.packedGroundHeight`) |
| Esybių srautas (sukūrimas, sunaikinimas) | kiekvienas sukūrimas perskaitytas. Išdėstymas paimtas iš Dagor Engine paskelbto šaltinio; War Thunder savus komponentų tipus praleidžiame surasdami, kur prasideda kitas komponentas. Kiekvieno vieneto technika ir žaidėjo lizdas sutampa su tais, kuriuos nurodo nužudymo ir pataikymo įrašai, kiekvienam patikrintam įrašui |
| Kas vairavo kurį vienetą, DI vienetai, laivai, sausumos taikiniai | iš esybių srauto: kiekvienas vienetas turi savo techniką ir komandą, kiekvieno žaidėjo vienetas - savo žaidėją |
| Nužudymai pagal rezultatus | mirtys kiekvienam žaidėjui sutampa su rezultatų; rezultatai skaičiuoja daugiau nužudymų, nes klientui ne kiekvienas nužudymas siunčiamas. Įrašas, prasidedantis jau po mūšio pradžios, turi tik po to įvykusius nužudymus |
| Nužudymai, kritiniai pataikymai, didelis sugadinimas | kiekvienas failas |
| Sunaikinti moduliai (0xF118) | vienetas ir dalies numeris; dalies vardui reikia technikos pažeidimo modelio, kuris įraše nėra |
| Paleisti ginklai (esybių srautas) | paleidimo taškas yra maždaug 10-20 m (mediana) nuo artimiausio vieneto, kuris laikomas paleidėju |
| Skrendantys ginklai (0xF0DB) | raketos, raketos su valdymu ir bombos, kiekviena susieta su savo esybe |
| Bombos be skrydžio įrašų | bombai be jų kritimas apskaičiuojamas nuo paleidimo iki smūgio (gravitacija ir pasipriešinimas, pavyzdys kas 0,1 s, `extrapolated` true). Patikrinta virš jūros, kur žinomas smūgio aukštis: apskaičiuoti kritimai baigiasi maždaug 15 m atstumu nuo vandens. Rungtynių dokumente toks ginklas turi `ballisticImpact`; `counts.bombsBallistic` juos suskaičiuoja |
| Žaidėjų lizdai, pokalbis | kiekvienas failas |
| Sprogimai, priešlėktuviniai sprogimai, apdovanojimai, aptikimai, oras, misijos objektai | perskaityta; pozicijos patikrintos akimi žiūryklėje |
| Įrašančiojo žaidėjo prietaisai (0xD04A) | pavadinti pagal tai, ką jie daro: [Kabinos prietaisai](aircraft.md#cockpit-instruments); kiti - `notNamed` |
| Kiti skrydžio įrašų laukai | greitis, šoviniai, valdikliai, varikliai: [Skrydžio įrašai](aircraft.md#flight-entries) |
| Įvykių eilučių orientacija | kiekviena įvykių eilutė nurodo savo vieneto kryptį, kėlimą, posūkį ir žvilgsnio vektorių tą akimirką |
| Žaidėjų statistika ir komandų rezultatai | mūšiui pasibaigus kiekviena statistika kiekvienam žaidėjui lygi rezultatų: [Atspindžio duomenys](aircraft.md#reflection-data) |
| Ginklų ir technikos vardai | iš jūsų diegimo angliškos lokalizacijos; kai kurių laivų numatytųjų juostų ir aerodromų radarų žaidime vardo nėra |
| Žaidėjai ir DI | nė viena rezultatų žaidėjo eilutė nėra DI, kiekviena ne DI eilutė priklauso rezultatų žaidėjui (`selfCheck.identity`) |
| Griuvėsiai | vieneto pavyzdžiai po jo mirties ir toliau ateina; sausumos vieneto ar laivo griuvėsiai yra `alive` 0, kol jo esybė pašalinama, ir lieka viena trajektorija; orlaiviai turi `alive` 0 ne ilgiau kaip 60 s (`selfCheck.wrecks`) |
| Technikos keitimai | žaidėjo vienetas, dar gyvas, kai to paties žaidėjo kitas vienetas pasirodo, ten nutraukiamas (palikta stovėti technika). `selfCheck.vehicleSwitch.twoLiveVehicles` turi būti 0 |
| Mūšio režimas | [Mūšio režimas](ground.md#battle-mode) |
| Orlaiviai 2026 m. serverio įraše | skaitomi pagal 2026 m. išdėstymą; kryptis ir roll ženklas sutampa su posūkiais; vietos laikikliai orlaiviai ir žvalgybos dronai neturi duomenų |
| Serverio įrašo žaidėjai | surandami pagal vardą lizduose; kiekviena statistika lygi rezultatų (`selfCheck.players`) |
| Orlaiviai 2025 m. serverio įrašuose ir versijos 101286 | neskaityti: jų skrydžio paketai turi kitokį išdėstymą |

## Pranešimai vienetams {#messages-to-units}

Kiekvienas 4 tipo paketas yra Dagor Engine daNet mpi pranešimas: gavėjo objekto id, tada (kai jo žemieji 11
bitų visi vienetai) objekto ext UID, pranešimo id ir turinys. Pranešimas vienetui turi kaip ext UID vieneto
esybės id, `index << 10 | generation`. Patikrinta: kiekvienas toks pranešimas nurodo tą akimirką gyvą esybę.

Specialistams: skaitomi pranešimai:

| Pranešimas | Ką reiškia ir patikrinimas |
|---|---|
| 0xF0E9 UnitHitEffects | vieno sviedinio pataikymas: šaulio uid ir pataikymo taškas vieneto rėmelyje (x - pirmyn, y - aukštyn, z - kairėn): centimetrais orlaiviams ir laivams, 20/32768 m žingsniu sausumos vienetams (pritaikyta prie tankų bokštelių dydžio). `hitLocalX/Y/Z` metrais. Tampa `shot` eilute ([Šaudymas](hits.md#gunfire)). Beveik kiekvieno pataikymo ir nužudymo įrašo atakuotojas yra tarp šių šaulių; pataikymo taškai yra šaulio pusėje |
| 0xF133 UnitOnExplosion | tas pats šaulio uid |
| 0xF04B OnUnitDead | `dead` eilutės: kiekvienas nužudymo įrašo auka turi vieną per 2 s |
| 0xD047 FmwRpm | variklių sūkiai (`rpm`); sutampa su kabinos sūkių rodykle |
| 0xF0B1, 0xF0A0 | `gun_shot` eilutės: atskiri sunkiosios PAB ir artilerijos šūviai |
| 0xF01B, 0xF01C | `fire_start`, `fire_stop` eilutės: 40 mm PAB patrankų serijos (patranka šaudo; gaisras technikoje yra `fire_on`, žr. [Technikos gaisrai](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` eilutės |
| 0xD0FE ProjectileHitReplay | įrašančiojo žaidėjo paties pataikymai ir jo pataikymai, su ginklu ir šaudmenimis, įvardyti iš diegimo (`projectileHitReplays`) |
| 0xF13E, 0xF031 | pataikymo vizualinis efektas ir efektas, paleistas ant vieneto; jie ateina kartu su pataikymu į tą patį vienetą |
| 0xD041 | po vieną kiekvienai orlaivio gynybinei patrankai, du kartus per sekundę; jų indeksai atitinka skrydžio modelio šaulių ginklus |
| 0xD048, 0xF117 | išdėstymas perskaitytas, prasmė nežinoma |
| likusieji (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | pranešimų papildomame faile su savo vienetu ir laukais |

Vardai - bendruomenės (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Dar skaitoma {#also-read}

- **Esybių srauto replikacija** (0x22, 0x23): kiekvienai esybei komponentų reikšmių blokas: laivų remonto
  laikmačiai, sunaudojamų priemonių kiekis, savininko ir komandos pasikeitimai, variklio perkaitimas. Skaičiuojama
  `counts.replicatedComponents`; reikšmės - pranešimų papildomame faile.
- **Misijos scenarijaus veiksmai** (0xF028) ir **patarimai** (0xF0EC): `triggers`, `hints`. **Misijos eiga**
  (0xF07A, 0xF07C): `missionProgress`.
- **Įrašo kamera** (0xD043): žr. [Kamera](ground.md#the-camera).

## Neskaitoma ir kodėl {#not-read-and-why}

- **Esybių pranešimų pavadinimai ir turinys** (0x20, 0x21): klasės numeris yra vieta sąraše, sudarytame žaidime,
  jis neatsiunčiamas ir nėra jo duomenyse. Du skaitomi (technikos gaisrai ir jų gesintuvai); kiti išsaugomi pilnai
  su savo esybe ir klasės numeriu.
- **Kiti replikuoti objektai** (rūšys, kitos nei žaidėjų lizdai ir komandos): perskaityti ir išsaugoti, bet
  nepavadinti; rezultatuose nėra, su kuo juos patikrinti.
- **Kitų orlaivių valdikliai, droselis ir šoviniai**: atnaujinami tik retkarčiais; išsaugomi skrydžio papildomame
  faile, o ne lentelėje.
- **Orlaivių gaisrai**: nerasti jokiuose pranešimuose; degantis orlaivis neturi `fire_on` eilutės.
- **Paleistų ginklų vardai**: bombos ar raketos esybė nieko nepavadina; nužudymo įrašai įvardija nužudymo ginklą.
- **Pataikymai, kurie nepataikė**: įraše yra tik pataikymai.

Kiekvieno rungtynių dokumento `counts.messageIdsNotRead` ir `selfCheck` pasako, ką naujas įrašas turi ir kaip gerai jis
perskaitytas.

---

Dalis [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Šaltinis: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
