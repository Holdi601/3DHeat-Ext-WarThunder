---
title: Lentokoneet
nav_order: 11
lang: "fi"
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Lentokoneet {#aircraft}

Tämä sivu on tarkoitettu ihmisille, jotka haluavat tietää, mistä lentokonesarakkeet tulevat ja
kuinka paljon niihin voi luottaa. Jokainen tarkistus alla vertaa arvoa johonkin, minkä replay
kertoo toisella, riippumattomalla tavalla; annetaan vain menetelmä ja yhteneväisyys.

## Ohjaamon mittarit {#cockpit-instruments}

Viesti 0xD04A lähettää tallentavan pelaajan mittarit (numero, arvo) -pareina: neljä sekunnissa
arcade-taisteluissa, vain muuttuneet arvot simulator-taisteluissa. Numerot muodostavat yhden
luettelon kaikille ohjaamoille, ja ohjaamo lähettää ne mittarit, jotka sen malli sisältää. Pelin
koodi määrää, mikä numero on mikäkin mittari, joten jokainen numero nimettiin sen mukaan, mitä se
tekee, ja tarkistettiin replayta vastaan (`convert.INSTRUMENTS` sisältää tuloksen; mitään ei
lueta asennuksesta):

| Numero | Nimi | Tarkistettu vastaan |
|---|---|---|
| 0 | mittaristonopeus, m/s | radan nopeus ilmantiheyden mukaan korjattuna: korrelaatio 0,99 |
| 39 | nousunopeus, m/s | radan nousunopeus: korrelaatio yli 0,99 |
| 40, 41 | korkeus, m; korkeus modulo 1000 | radan korkeus, muutaman metrin tarkkuudella |
| 52, 53 | keinotekoisen horisontin kallistus ja pitch | miinus taulukon roll ja pitch, alle 1 asteen tarkkuudella |
| 64 | kompassi | taulukon heading, alle 0,1 asteen tarkkuudella |
| 15-20 | sauvat (polkimet) | sivuvoima lentokoneeseen |
| 23, 31 | sauva: hissi ja aileronit (merkki kuten ohjaamomallin) | hyökkäyskulma; kallistusnopeus |
| 69, 71, 73 | kello: tunnit (12 tunnin taulu), minuutit, sekunnit | tallennustietokoneen paikallinen aika, minuutin tarkkuudella |
| 75 | imupaine, atm | korkeampi sotatilan hätävoimalla kuin täydellä kaasulla |
| 81-86, 87-92, 93-98 | kierrosluku moottoria kohden, kierrosluku modulo 1000, kierroslukumittari | toisiaan tarkalleen; moottorin kierrosluku: korrelaatio yli 0,97 |
| 195 | polttoaine | laskee lennon aikana, täyttyy taas uudelleensyntymisessä |
| 228-230 | laskutelineen jalat, 1 alhaalla | alhaalla vain lentokenttien korkeudella ja laskunopeudella |
| 240, 241 | kaasu moottoria kohden (1,1 sotatilan hätävoima tai jälkipoltin) | lentomerkinnän kaasu |
| 330-332, 346-348 | ammuslaskurit (kaksi yhtä suurta sarjaa) | aseasetuksen laukaukset, jotka laskevat lentomerkinnän laukausten mukaan |
| 135, 159 | öljyn ja sylinterikannen lämpötila | todennäköisesti: nousevat lennon aikana |
| 58, 61 | liukupallo, kääntönuoli | todennäköisesti: seuraavat sivuvoimaa ja kääntönopeutta |
| 223 | ilmajarru | todennäköisesti: asetetaan vain lähestymisessä |
| 490-497, 500-505 | pyörien jarrut | todennäköisesti: asetetaan vain lentokentällä seistessä |

Muutamia muita numeroita lähetetään, joiden merkitystä ei tunneta; ne säilytetään ottelun
asiakirjan kohdassa `authorInstruments.notNamed`.

Taulukon `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` ja
`throttle` tulevat näistä, tallentavan pelaajan omilla riveillä, ottaen viimeisen viestin enintään
0,2 s näytteen jälkeen.

## Lentomerkinnät {#flight-entries}

Jokaisen lentokoneen lentomerkintä (pakettityyppi 2) kantaa sijainnin ja asennon lisäksi:

- **Nopeus**: 32-bittinen sana asennon jälkeen. Bitit 31, 30 ja 29 ovat x:n, y:n ja z:n merkit; sitten
  nopeus 11 bitissä 500/2047 m/s (pysähtyy 500 m/s:iin), sitten |x| ja |y| nopeuden osina 9 bitissä
  kumpikin, ja z tekee vektorista yksikkövektorin. Tarkistettu vastaanotettujen näytteiden välistä
  askelta vasten: suunta vastaa murto-asteen tarkkuudella tallentavalle pelaajalle ja noin 2 asteen
  tarkkuudella muille; nopeus 0,2 %:n tarkkuudella. `selfCheck.flightEntries`.
- **Laukaukset aseittain**: luettelo ennen sijaintia, yksi kohta asetta kohden, ensin jäljellä olevat
  laukaukset. Tallentavan pelaajan vastaa ohjaamon laskureita yhden tikin myöhemmin lähes jokaisella näytteellä.
- **Ohjaimet ja kaasu**: 7 tavua nopeuden jälkeen, luettuina 14 nibbleinä. Tallentavalle pelaajalle
  joka tikillä: 1 hissi, 2 aileronit, 3 peräsin (8 levossa), 11 kaasu kuudesosina (15 myös sotatilan
  hätävoimalle ja jälkipoltolle), 4 pyörien jarrut, 5 ilmajarru, 8 todennäköisesti jarrulaskuvarjo.
  Muiden lentokoneiden nibbleet muuttuvat vain muutaman kerran taistelun aikana, eivätkä ne ole niiden
  ohjaimia sillä hetkellä.
- **Moottorit**: moottoria kohden tila-tavu (0 pois; 1-6 käynnistyy; 7 käy; 8 kuollut), 16-bittinen arvo
  vain jälkipolttimella (32767 täysi), ja tavu vain sen jälkeen, kun moottoriin osui. Useimmat
  lentokoneet, joiden moottori menee tilaan "dead", tuhoutuvat tai päättyvät minuuteissa.

## Heijastustiedot {#reflection-data}

Viestit 0xF02D ja 0xF0AA replikoivat pelin numeroidut objektit: jokaiselle objektille sen tunnus
(5 ylintä bittiä tyyppi, 11 alinta indeksi) ja kenttätaulukko. Tyyppi 14 ovat pelaajapaikat (kenttä 2
käyttäjätunnus ja nimi, 9 joukkue), tyyppi 15 joukkueet (indeksi 1 ja 2):

- Pelaajapaikan kenttä 39 sisältää sen tilastot kiinteissä paikoissa: tapot (offset 0), joukkuetapot (2),
  kuolemat (4), laivatapot (10), tekoälytapot (12), tekoälyn maatapot (14), avustukset (20),
  valloitusalueet (22), alueen vahinko (24, 32-bittinen), vahinkopalkkio (40, 32-bittinen), ohjusten
  väistöt (50). Kenttä 38 alkaa pistemäärästä, kenttä 42 on ryhmä. Taistelun lopussa jokainen arvo on
  yhtä suuri kuin tulosten jokaiselle pelaajalle (`selfCheck.scoreboardVsResults`). Sitä, missä maatapot
  pidetään, ei tunneta.
- Joukkueen kenttä 7 on sen pistemäärä: lopussa se on yhtä suuri kuin sen pelaajien pisteiden summa
  tuloksissa. Kenttä 3 on todennäköisesti sen lippu-paikat.
- Jokainen viesti lähettää vain muuttuneet kentät, joten ottelun asiakirjan `scoreboard` luettelee
  jokaisen pelaajan tilastot ja jokaisen joukkueen pistemäärän jokaisessa muutoksessa.

## Laskennallinen liike ja tasoittaja {#dead-reckoning-and-the-smoother}

Asiakasreplay tallentaa jokaisen lentokoneen neljä kertaa sekunnissa, sellaisena kuin asiakas sen piirsi.
Kaukaisen lentokoneen päivitysten välissä, joita se ei saa, asiakas siirtää sitä eteenpäin viimeisen
nopeutensa mukaan ja kääntää sitä viimeisillä kulmanopeuksillaan, ja seuraavassa päivityksessä se
loikkaa sinne. Luettuna sellaisenaan rata kulkee suoraan ja hyppää sitten. Lentomerkinnässä ei ole mitään,
mikä merkitsisi, mitkä näytteet vastaanotettiin; laskennallinen näyte löydetään sen perusteella, mitä se
on: se jatkaa kahden sitä edeltävän näytteen suoraa viivaa niiden vauhdilla 3 cm:n tarkkuudella.

Kuinka paljon tällä on väliä, riippuu taistelusta: arcade-taisteluissa noin puolet muiden lentokoneiden
näytteistä voi olla laskennallisia, simulator-taisteluissa vain muutama prosentti. Tasoittaja leikkaa
yli 15 g:n askeleet noin viisi kertaa (`selfCheck.deadReckoning`). Tallentavan pelaajan oma lentokone
ei ole asiakkaan ekstrapoloima, ja se jätetään ennalleen.

Oletuksena (`--no-smoothing` kytkee sen pois) kaikkien muiden kuin tallentavan pelaajan radat asetetaan
sinne, missä vastaanotetut tilat sanovat niiden olleen: laskennallinen näyte menee käyrälle vastaanotettujen
näytteiden välille ennen sitä ja sen jälkeen, kumpikin omalla nopeudellaan; yli 3 s:n suora viiva vain
taipuu kohti seuraavaa vastaanotettua näytettä, joten yksikään näyte ei liiku pidemmälle kuin asiakkaan
oma loikkaus. Sen asento käännetään tasaisesti yhdestä vastaanotetusta asennosta seuraavaan. Vastaanotetut
näytteet tasoitetaan enintään 2 m tai 0,04 s niiden nopeudella; tasainen käännös pysyy ennallaan. Replayn
omat arvot pysyvät `Raw`-sarakkeissa.

## Asento, tarkistettu {#attitude-checked}

Tallentavan pelaajan omalla lentokoneella heading on 1 asteen sisällä (mediaani) liikkeen suunnasta,
pitch muutaman asteen sisällä nousukulmasta, ja selvissä käännöksissä roll on käännöksen merkkinen lähes
jokaisella näytteellä: lentomallin roll on vasen siipi alas positiivinen, ja taulukko kääntää sen oikea
siipi alas positiiviseksi (`selfCheck.aircraftAttitude`). 10-bittiset kulmat askeltavat 0,18 astetta.
Maayksiköiden asentoa tarkistetaan niiden laukauksia vasten ([Tornit](ground.md#turrets)).

---

Osa [3DHeatiä](https://github.com/Holdi601/3DHeat) ([dokumentaatio](https://holdi601.github.io/3DHeat/)). Lähde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
