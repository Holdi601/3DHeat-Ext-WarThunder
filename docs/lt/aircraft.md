---
title: Orlaiviai
nav_order: 11
lang: "lt"
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Orlaiviai {#aircraft}

Skirta skaitytojams, norintiems žinoti, iš kur ateina orlaivių stulpeliai ir kiek jiems pasitikėti.
Kiekvienas patikrinimas lygina reikšmę su kitu, nepriklausomu būdu, kuriuo įrašas tai sako; čia
nurodytas tik metodas ir sutapimas.

## Kabinos prietaisai {#cockpit-instruments}

Pranešimas 0xD04A siunčia įrašančiojo žaidėjo prietaisų rodmenis kaip poras (numeris, reikšmė): keturis
per sekundę arkadiniuose mūšiuose, tik pasikeitusias reikšmes simuliatoriaus mūšiuose. Numeriai sudaro
vieną sąrašą visoms kabinoms, o kabina siunčia tuos prietaisus, kuriuos turi jos modelis. Žaidimo kodas
nustato, koks numeris yra koks prietaisas, todėl kiekvienas numeris buvo įvardytas pagal tai, ką jis
daro, ir patikrintas su įrašu (`convert.INSTRUMENTS` saugo rezultatą; iš diegimo nieko nenuskaitoma):

| Numeris | Vardas | Patikrinta su |
|---|---|---|
| 0 | indikuotas oro greitis, m/s | trajektorijos greitis, pataisytas pagal oro tankį: koreliacija 0,99 |
| 39 | kilimo greitis, m/s | trajektorijos kilimo greitis: koreliacija virš 0,99 |
| 40, 41 | aukštis, m; aukštis modulo 1000 | trajektorijos aukštis, kelių metrų tikslumu |
| 52, 53 | dirbtinio horizonto posūkis ir kėlimas | minus lentelės posūkis ir kėlimas, mažiau nei 1 laipsnis skirtumo |
| 64 | kompasas | lentelės kryptis, mažiau nei 0,1 laipsnio skirtumo |
| 15-20 | pedalai | šoninė jėga orlaiviui |
| 23, 31 | lazdė: aukštumos ir posūkio valdikliai (ženklas pagal kabinos modelį) | kampas į srautą; posūkio greitis |
| 69, 71, 73 | laikrodis: valandos (12 valandų ciferblatas), minutės, sekundės | įrašymo kompiuterio vietinis laikas, iki minutės |
| 75 | įleidimo vamzdžio slėgis, atm | aukštesnis esant karo avariniam galiai nei pilnam droseliui |
| 81-86, 87-92, 93-98 | sūkiai kiekviename variklyje, sūkiai modulo 1000, sūkių rodyklė | tiksliai tarpusavyje; variklio sūkiai: koreliacija virš 0,97 |
| 195 | kuras | krenta per skrydį, vėl pilnas atgimus |
| 228-230 | tūpimo įrenginio kojos, 1 - nuleista | nuleista tik netoli aerodromų aukščio ir tūpimo greičiu |
| 240, 241 | droselis kiekviename variklyje (1,1 karo avarinė galia ar degiklis) | skrydžio įrašo droselis |
| 330-332, 346-348 | šaudmenų skaitikliai (du vienodi rinkiniai) | ginklo nustatymo šoviniai, mažėjantys kartu su skrydžio įrašo šoviniais |
| 135, 159 | alyvos ir cilindrų galvutės temperatūra | tikėtina: kyla per skrydį |
| 58, 61 | slydimo kamuolys, posūkio adata | tikėtina: seka šoninę jėgą ir posūkio greitį |
| 223 | oro stabdis | tikėtina: įjungiamas tik artėjant tūpti |
| 490-497, 500-505 | ratų stabdžiai | tikėtina: įjungiami tik stovint aerodrome |

Dar kai kurie numeriai siunčiami, kurių reikšmė nežinoma; jie išsaugomi rungtynių dokumento
`authorInstruments.notNamed` skiltyje.

Lentelės `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` ir
`throttle` gaunami iš šių prietaisų, įrašančiojo žaidėjo eilutėse, imant paskutinį pranešimą ne daugiau
kaip 0,2 s po pavyzdžio.

## Skrydžio įrašai {#flight-entries}

Kiekvieno orlaivio skrydžio įrašas (paketo tipas 2) be pozicijos ir orientacijos turi:

- **Greitis**: 32 bitų žodis po orientacijos. Bitai 31, 30 ir 29 yra x, y ir z ženklai; tada greitis 11
  bitų, 500/2047 m/s žingsniu (sustoja ties 500 m/s), tada |x| ir |y| kaip greičio dalys, po 9 bitus, o z
  yra tai, kas daro vektorių vienetiniu. Patikrinta pagal žingsnį tarp gautų pavyzdžių: kryptis sutampa
  per dalį laipsnio įrašančiajam žaidėjui ir apie 2 laipsnius visiems kitiems; greitis - 0,2 % tikslumu.
  `selfCheck.flightEntries`.
- **Šoviniai kiekvienam ginklui**: sąrašas prieš poziciją, po vieną elementą kiekvienam ginklui, pirmiausia
  likę šoviniai. Įrašančiojo žaidėjo sutampa su kabinos skaitikliais vienu taktu vėliau beveik kiekvienam
  pavyzdžiui.
- **Valdikliai ir droselis**: 7 baitai po greičio, skaitomi kaip 14 pusbaiščių. Įrašančiajam žaidėjui -
  kiekvieną taktą: 1 - aukštumos valdiklis, 2 - posūkio valdiklis, 3 - posūkio ratas (8 ramybėje), 11 -
  droselis penkioliktosiomis dalimis (15 ir karo avarinei galiai, ir degikliui), 4 - ratų stabdžiai, 5 -
  oro stabdis, 8 tikriausiai - stabdymo parašiutas. Kitų orlaivių pusbaiščiai keičiasi tik kelis kartus per
  mūšį ir nėra jų valdikliai tuo metu.
- **Varikliai**: kiekvienam varikliui būsenos baitas (0 - išjungtas; 1-6 - įsijungia; 7 - veikia; 8 -
  sugedęs), 16 bitų reikšmė tik su degikliu (32767 - pilnai), ir baitas tik tada, kai variklis buvo
  pataikytas. Dauguma orlaivių, kurių variklis tampa "sugedęs", būna sunaikinti arba baigia per kelias
  minutes.

## Atspindžio duomenys {#reflection-data}

Pranešimai 0xF02D ir 0xF0AA replikuoja žaidimo numeruotus objektus: kiekvienam objektui jo id (viršutiniai
5 bitai - rūšis, žemieji 11 - indeksas) ir lentelė su laukais. 14 rūšis - žaidėjų lizdai (laukas 2 - vartotojo
id ir vardas, 9 - komanda), 15 rūšis - komandos (indeksas 1 ir 2):

- Lizdo laukas 39 laiko jo statistiką fiksuotose vietose: nužudymai (poslinkis 0), komandos nužudymai (2),
  mirtys (4), jūrų nužudymai (10), DI nužudymai (12), DI sausumos nužudymai (14), pagalbos (20), kapitalo
  zonos (22), zonos žala (24, 32 bitų), žalos apdovanojimas (40, 32 bitų), vengimai raketoms (50). Laukas 38
  prasideda rezultatu, laukas 42 - būrys. Mūšiui pasibaigus, kiekviena reikšmė lygi rezultatų reikšmei
  kiekvienam žaidėjui (`selfCheck.scoreboardVsResults`). Nežinoma, kur laikomi sausumos nužudymai.
- Komandos laukas 7 yra jos rezultatas: pabaigoje jis lygus jos žaidėjų rezultatų sumai rezultatuose. Laukas
  3 tikriausiai yra jos bilietai.
- Kiekvienas pranešimas siunčia tik pasikeitusius laukus, todėl rungtynių dokumento `scoreboard` pateikia
  kiekvieno žaidėjo statistiką ir kiekvienos komandos rezultatą kiekvieno pokyčio metu.

## Įvertinimas pagal nuvažiavimą ir glotnintuvas {#dead-reckoning-and-the-smoother}

Kliento įrašas įrašo kiekvieną orlaivį keturis kartus per sekundę, kaip jį nupiešė klientas. Tarp
atnaujinimų, kuriuos jis gauna tolimam orlaiviui, klientas perkelia jį toliau pagal paskutinį greitį ir
pasuka pagal paskutinius sukimosi greičius, o kitame atnaujinime peršoka į vietą. Nuskaitytas kaip yra,
trajektorija eina tiesiai, paskui peršoka. Skrydžio įraše nieko nežymi, kurie pavyzdžiai buvo gauti;
įvertintas pavyzdys atpažįstamas pagal tai, koks jis yra: jis tęsia dviejų prieš jį esančių pavyzdžių
tiesę, jų tempu, 3 cm tikslumu.

Kiek tai svarbu, priklauso nuo mūšio: arkadiniuose mūšiuose apie pusė kitų orlaivių pavyzdžių gali būti
įvertinti nuvažiavimu, simuliatoriuje - tik keli procentai. Glotnintuvas perpjauna per 15 g žingsnius
maždaug penkis kartus (`selfCheck.deadReckoning`). Paties įrašančiojo žaidėjo orlaivis kliento
neekstrapoliuojamas ir paliekamas kaip yra.

Pagal numatytuosius nustatymus (`--no-smoothing` tai išjungia) visų vienetų, išskyrus įrašančiojo žaidėjo,
trajektorijos dedamos ten, kur gauti būsenų duomenys sako, kad jie buvo: įvertintas pavyzdys patenka į
kreivę per prieš ir po jo gautus pavyzdžius, kiekvienas su savo greičiu; per daugiau nei 3 s tiesi linija
tik nulenkiama link kito gauto pavyzdžio, todėl joks pavyzdys nejuda toliau nei kliento paties peršokimas.
Jo orientacija pasukama tolygiai nuo vienos gautos orientacijos iki kitos. Gauti pavyzdžiai išlyginami ne
daugiau kaip 2 m arba 0,04 s jų greičio atstumu; pastovus posūkis lieka toks, koks yra. Įrašo paties
duomenys lieka `Raw` stulpeliuose.

## Orientacija, patikrinta {#attitude-checked}

Įrašančiojo žaidėjo orlaivyje kryptis yra per laipsnį (mediana) nuo judėjimo krypties, kėlimas - per kelis
laipsnius nuo kilimo kampo, o aiškiuose posūkiuose posūkis turi posūkio ženklą beveik kiekvienam pavyzdžiui:
skrydžio modelio posūkis yra kairysis sparnas žemyn teigiamas, o lentelė jį pasuka į dešinįjį sparną žemyn
teigiamą (`selfCheck.aircraftAttitude`). 10 bitų kampai žingsniuoja po 0,18 laipsnio. Sausumos vienetų
orientacija tikrinama pagal jų šūvius ([Bokšteliai](ground.md#turrets)).

---

Dalis [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Šaltinis: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
