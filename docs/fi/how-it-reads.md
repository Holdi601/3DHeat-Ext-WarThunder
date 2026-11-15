---
title: Miten replay luetaan
nav_order: 10
lang: fi
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Miten replay luetaan {#how-it-reads-a-replay}

Tämä sivu on tarkoitettu ihmisille, jotka haluavat tietää, mitä muunnin lukee, miten
se tarkistettiin ja siksi kuinka paljon kutakin saraketta voi luottaa. Sivu ei ole
tarpeen replayjen muuntamiseen.

Lukeminen tarkistettiin ilmataisteluiden asiakasreplayillä (arcade ja simulator) ja
laivataisteluilla, maataisteluiden palvelinreplayillä, ja 2025-asetteluille
[wt_replay_decoderin](https://github.com/llama-for3ver/wt_replay_decoder) julkisilla
esimerkkireplayillä. Jokainen tarkistus vertaa arvoa johonkin, minkä replay kertoo
toisella, riippumattomalla tavalla; tässä annetaan vain menetelmä ja yhteneväisyys.

## Mitä luetaan, ja tarkistus {#what-is-read-and-the-check}

| Osa | Tila ja tarkistus |
|---|---|
| Otsikko, kartta, tehtävä, aloitusaika, istunto; tulokset | jokainen tiedosto |
| Tehtävän asetukset (otsikon jälkeinen blk) | tila, sää, rajat, `stars` (päivämäärä, aika, paikka) |
| Pakettivirta (zlib vuonna 2025, zstd vuonna 2026) | jokainen paketti kehystetty |
| Lentokoneiden sijainnit ja asento (2026-asettelu) | 4 näytettä sekunnissa, ei yhtään pakettia lukematta; suunta vastaa liikkeen suuntaa |
| Lentopaketit ennen omaa aikaansa | verkkohäiriön jälkeen asiakasreplayn lentopaketti pitää joskus jokaista muuta lentokonetta siellä, missä se on noin 0,75 s myöhemmin. Ennakko mitataan paketti kohtaisesti, ja jokainen ennakoiva lentokone saa ajan, jota se edustaa (`selfCheck.flightPacketsRetimed`) |
| Laskennallisen liikkeen hypyt | askel laskennallisesta jaksosta mitataan viimeksi vastaanotetusta tilasta, joten asiakkaan korjaukset eivät enää katkaise ratoja ([Laskennallinen liike](aircraft.md#dead-reckoning-and-the-smoother)) |
| Teleporttaukset | rata katkaistaan, kun sen yksikkö liikkuu pidemmälle kuin voi: ensin lajinsa mukaan (lentokone 750 m/s, maayksiköt ja laivat 40 m/s, aseet 1800 m/s), sitten omaa vauhtiaan vastaan. Jokainen katkaisu luetellaan kohdassa `trackBreaks` todennäköisine syineen (uudelleensyntyminen, pelin siirtämä pelaaja, kaukaisen yksikön korjaus). Katkaisujen jälkeen mikään askel radan rivien välillä ei ole nopeampi kuin sen laji sallii (`selfCheck.stepSpeed`) |
| Maa- ja laivasijainnit (0xF073 / 0xF074) | ei yhtään pakettia lukematta. Heading, pitch ja roll 16-bittisestä asennosta: heading vastaa liikkeen suuntaa noin 2 asteen tarkkuudella (mediaani); pitch laskee 180/65536 astetta askeleelta; kun rollin merkki käännetään, rungon ja tornin antama tykin suunta osoittaa osumakohtaan lähes jokaiselle säiliön laukaukselle. Laivat ovat veden pinnan tasolla |
| Tornit | säiliöiden tornin kääntö ja tykin kallistus: katso [Tornit](ground.md#turrets) |
| Pakatut maakorkeudet | pakatuista 64 bitistä sijainneista korkeus lasketaan -100 m:stä useimmilla kentillä ja vedenpinnasta joillakin; siirtymä mitataan kullakin replaylla yksiköistä, jotka nähdään molemmissa muodoissa (`selfCheck.packedGroundHeight`) |
| Kokonaisuusvirta (luonti, tuhoutuminen) | jokainen luonti luettu. Asettelu tulee Dagor Enginen julkaistusta lähdekoodista; War Thunderin omat komponenttityypit ohitetaan etsimällä, mistä seuraava komponentti alkaa. Jokaisen yksikön ajoneuvo ja pelaajapaikka vastaavat niitä, jotka tappo- ja osumatietueet nimeävät, jokaiselle tarkistetulle tietueelle |
| Kuka ajoi mitäkin yksikköä, tekoälyyksiköt, laivat, maakohteet | kokonaisuusvirrasta: jokaisella yksiköllä on ajoneuvonsa ja joukkueensa, jokaisen pelaajan yksiköllä hänen pelaajansa |
| Tapot tulosten mukaan | pelaajakohtaiset kuolemat ovat yhtä suuret kuin tuloksissa; tulokset laskevat enemmän tappoja, koska asiakas ei saa jokaista tappoa. Replay, joka alkaa taistelun alettua, sisältää vain sen jälkeiset tapot |
| Tapot, kriittiset osumat, vakava vahinko | jokainen tiedosto |
| Tuhoutuneet moduulit (0xF118) | yksikkö ja osan numero; osan nimi vaatisi ajoneuvon vaurio-mallin, jota replayssa ei ole |
| Irrotetut aseet (kokonaisuusvirta) | irrotuspiste on noin 10-20 m (mediaani) lähimmästä yksiköstä, joka otetaan laukaisijaksi |
| Lennossa olevat aseet (0xF0DB) | ohjukset, raketit ja pommit, kukin sidottuna omaan kokonaisuuteensa |
| Pommit ilman lentotietueita | pommin lento lasketaan irrotuksesta osumaan (painovoima ja vastus, näyte 0,1 s välein, `extrapolated` tosi). Tarkistettu merellä, jossa osumakorkeus tunnetaan: lasketut lennot päättyvät noin 15 m:n sisään vedestä. Ottelun asiakirjassa tällaisella aseella on `ballisticImpact`; `counts.bombsBallistic` laskee ne |
| Pelaajapaikat, keskustelu | jokainen tiedosto |
| Räjähdykset, ilmatorjunnan purkaukset, palkinnot, havainnot, sää, tehtävän kohteet | luettu; sijainnit tarkistettu silmämääräisesti katselimessa |
| Tallentavan pelaajan mittarit (0xD04A) | nimetty sen mukaan, mitä ne tekevät: [Ohjaamon mittarit](aircraft.md#cockpit-instruments); loput kohdassa `notNamed` |
| Lentomerkintöjen muut kentät | nopeus, laukaukset, ohjaimet, moottorit: [Lentomerkinnät](aircraft.md#flight-entries) |
| Tapahtumarivien asento | jokainen tapahtumarivi kantaa yksikkönsä headingin, pitchin, rollin ja katselusuuntavektorin sillä hetkellä |
| Pelaajatilastot ja joukkueiden pisteet | taistelun lopussa jokainen tilasto on yhtä suuri kuin tuloksissa jokaiselle pelaajalle: [Heijastustiedot](aircraft.md#reflection-data) |
| Aseiden ja ajoneuvojen nimet | asennuksesi englanninkielisestä lokalisoinnista; muutamilla laivojen oletusvöillä ja lentokenttien tutkilla ei ole nimeä pelissä |
| Pelaajat ja tekoäly | yksikään tulospelaaja ei ole tekoälyä, jokainen ei-tekoälyyksikkö on tulospelaajan (`selfCheck.identity`) |
| Hylyt | yksikön näytteet kuoleman jälkeen jatkuvat; maayksikön tai laivan hylky on `alive` 0, kunnes sen kokonaisuus poistetaan, ja se on yksi rata; lentokoneet pitävät `alive` 0:n enintään 60 s (`selfCheck.wrecks`) |
| Ajoneuvon vaihdot | pelaajan yksikkö, joka on yhä elossa, kun saman pelaajan seuraava yksikkö ilmestyy, päättyy siihen (jätetty seisomaan). `selfCheck.vehicleSwitch.twoLiveVehicles` on oltava 0 |
| Taistelutila | [Taistelutila](ground.md#battle-mode) |
| Lentokoneet 2026 palvelinreplayssa | luetaan 2026-asettelulla; heading ja rollin merkki vastaavat käännöksiä; paikkamerkkilentokoneet ja tiedustelu-droonit eivät kanna tietoa |
| Palvelinreplayn pelaajat | löytyvät nimellä paikoista; jokainen tilasto on yhtä suuri kuin tuloksissa (`selfCheck.players`) |
| Lentokoneet 2025 palvelinreplayissa ja versiossa 101286 | ei luettu: niiden lentopaketeilla on eri asettelu |

## Viestit yksiköille {#messages-to-units}

Jokainen tyypin 4 paketti on Dagor Enginen daNetin mpi-viesti: vastaanottajaobjektin tunnus,
sitten (kun sen 11 alimmaista bittiä ovat kaikki ykkösiä) objektin ext-UID, viestitunnus ja
hyötykuorma. Yksikölle menevässä viestissä ext-UID on yksikön kokonaisuustunnus, `index << 10 | generation`.
Tarkistettu: jokainen tällainen viesti nimeää kokonaisuuden, joka on elossa juuri silloin.

Asiantuntijoille: luetut viestit:

| Viesti | Mitä, ja tarkistus |
|---|---|
| 0xF0E9 UnitHitEffects | yhden ammuksen osuma: ampujan uid ja osumapiste yksikön koordinaatistossa (x eteen, y ylös, z vasemmalle): senttimetrejä lentokoneille ja laivoille, 20/32768 m askeleelta maayksiköille (sovitettu säiliön tornien kokoon). `hitLocalX/Y/Z` metreinä. Tulee `shot`-riviksi ([Tulitus](hits.md#gunfire)). Lähes jokaisen osuman ja tappotietueen hyökkääjä on näiden ampujien joukossa; osumapisteet ovat ampujaa vasten olevalla puolella |
| 0xF133 UnitOnExplosion | sama ampujan uid |
| 0xF04B OnUnitDead | `dead`-rivit: jokaisen tappotietueen uhrilla on sellainen 2 s:n sisällä |
| 0xD047 FmwRpm | moottorien kierrosluku (`rpm`); vastaa ohjaamon kierroslukumittaria |
| 0xF0B1, 0xF0A0 | `gun_shot`-rivit: raskaan ilmatorjunnan ja tykistön yksittäiset laukaukset |
| 0xF01B, 0xF01C | `fire_start`, `fire_stop`-rivit: 40 mm:n ilmatorjuntatykkien purskeet (tykki ampuu; palo ajoneuvossa on `fire_on`, katso [Ajoneuvojen palot](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload`-rivit |
| 0xD0FE ProjectileHitReplay | tallentavan pelaajan omat osumat ja hänen itseensä osuneet, aseen ja ammuksen kanssa, nimetty asennuksesta (`projectileHitReplays`) |
| 0xF13E, 0xF031 | osuman visuaalinen efekti ja yksikköön toistettu efekti; ne tulevat saman yksikön osuman mukana |
| 0xD041 | yksi lentokoneen kutakin puolustavaa asetta kohden, kaksi kertaa sekunnissa; sen indeksit vastaavat lentomallin tykkimiehen aseita |
| 0xD048, 0xF117 | asettelu luettu, merkitys ei tunneta |
| loput (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | viestisivutiedostossa yksikkönsä ja kenttiensä kanssa |

Nimet ovat yhteisön (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Myös luettu {#also-read}

- **Kokonaisuusvirran replikointi** (0x22, 0x23): jokaiselle kokonaisuudelle lohko komponentin arvoja:
  laivojen korjausajastimet, kulutustavaroiden määrät, omistajan ja joukkueen muutokset,
  moottorin ylikuumeneminen. Lasketaan kohdassa `counts.replicatedComponents`; arvot
  viestisivutiedostossa.
- **Tehtävän käsikirjoituksen toiminnot** (0xF028) ja **vihjeet** (0xF0EC): `triggers`,
  `hints`. **Tehtävän edistyminen** (0xF07A, 0xF07C): `missionProgress`.
- **Replay-kamera** (0xD043): katso [Kamera](ground.md#the-camera).

## Ei luettu, ja miksi {#not-read-and-why}

- **Kokonaisuusviestien nimet ja sisällöt** (0x20, 0x21): luokkanumero on paikka pelin sisään
  käännetyssä luettelossa; sitä ei lähetetä eikä se ole sen tiedoissa. Kaksi luetaan (ajoneuvon palot
  ja sammuttimet); loput säilytetään kokonaisina kokonaisuutensa ja luokkanumeronsa kanssa.
- **Muut replikoidut objektit** (muut tyypit kuin pelaajapaikat ja joukkueet): luettu ja säilytetty,
  ei nimetty; tuloksissa ei ole mitään, mihin niitä verrata.
- **Muiden lentokoneiden ohjaimet, kaasu ja laukaukset**: päivitetään vain silloin tällöin;
  säilytetään lentosivutiedostossa, ei taulukossa.
- **Lentokoneiden palot**: eivät löydy yhdestäkään viestistä; palavalla lentokoneella ei ole
  `fire_on`-riviä.
- **Irrotettujen aseiden nimet**: pommin tai raketin kokonaisuudessa ei ole nimeä; tappotietueet
  nimeävät tappavan aseen.
- **Ohi menneet laukaukset**: replay sisältää vain osumat.

Jokaisen ottelun asiakirjan `counts.messageIdsNotRead` ja `selfCheck` kertovat, mitä uusi replay
sisältää ja kuinka hyvin se luettiin.

---

Osa [3DHeatiä](https://github.com/Holdi601/3DHeat) ([dokumentaatio](https://holdi601.github.io/3DHeat/)). Lähde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
