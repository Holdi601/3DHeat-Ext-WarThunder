---
title: "Flugvélar"
nav_order: 11
lang: is
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Flugvélar {#aircraft}

Fyrir lesendur sem vilja vita hvaðan dálkar flugvéla koma og hversu mikið má
treysta þeim. Hver athugun hér að neðan ber gildi saman við eitthvað sem
upptakan segir á annan, óháðan hátt; aðeins aðferðin og samræmið er gefið.

## Mælar í stjórnklefa {#cockpit-instruments}

Skilaboð 0xD04A senda mæla upptökumannsins sem pör (númer, gildi): fjórum
sinnum á sekúndu í arcade-bardögum, aðeins breytt gildi í simulator-bardögum.
Númerin mynda einn lista yfir alla stjórnklefa og stjórnklefi sendir þá mæla
sem módel hans hefur. Kóði leiksins ákveður hvaða númer er hvaða mælir, svo
hvert númer var nefnt eftir því sem það gerir og athugað gegn upptökunni
(`convert.INSTRUMENTS` geymir niðurstöðuna; ekkert er lesið úr uppsetningunni):

| Númer | Nafn | Athugað gegn |
|---|---|---|
| 0 | sýndur lofthraði (indicated airspeed), m/s | hraða ferilsins leiðréttum fyrir loftþéttleika: fylgni 0,99 |
| 39 | klifurhraði, m/s | klifurhraða ferilsins: fylgni yfir 0,99 |
| 40, 41 | hæð, m; hæð modulo 1000 | hæð ferilsins, nokkra metra frá |
| 52, 53 | veltun og halli gervihimins | mínus roll og pitch töflunnar, innan við 1 gráðu frá |
| 64 | áttaviti | heading töflunnar, innan við 0,1 gráðu frá |
| 15-20 | fótstig hliðarstýris | hliðarkrafturinn á flugvélina |
| 23, 31 | stýripinni: hæðarstýri og hallastýri (formerki eins og í módeli stjórnklefans) | árásarhornið; veltuhraðinn |
| 69, 71, 73 | klukka: klukkustundir (12 tíma skífa), mínútur, sekúndur | staðartími tölvunnar sem tók upp, upp á mínútu |
| 75 | hleðsluþrýstingur, atm | hærri við neyðarafl en við fulla inngjöf |
| 81-86, 87-92, 93-98 | snúningar á mínútu á hreyfil, snúningar modulo 1000, snúningsmælir | hver annan nákvæmlega; snúningar hreyfils: fylgni yfir 0,97 |
| 195 | eldsneyti | fellur yfir leiðangur, fullt aftur við endurkomu |
| 228-230 | fætur lendingarbúnaðar, 1 niðri | niðri aðeins nálægt hæð flugvalla og á lendingarhraða |
| 240, 241 | inngjöf á hreyfil (1,1 neyðarafl eða eftirbrennari) | inngjöf færslu flugmódelsins |
| 330-332, 346-348 | skotateljarar (tvö jöfn sett) | skot vopnaforstillingarinnar, falla með skotum færslu flugmódelsins |
| 135, 159 | hiti olíu og strokkhauss | líklegt: þeir hækka yfir leiðangur |
| 58, 61 | rennikúla, beygjunál | líklegt: þeir fylgja hliðarkraftinum og beygjuhraðanum |
| 223 | loftbremsa | líklegt: aðeins stillt í aðflugi |
| 490-497, 500-505 | hjólabremsur | líklegt: aðeins stillt þegar staðið er á flugvelli |

Nokkur númer til viðbótar eru send sem merking er ekki þekkt; þau eru
geymd í `authorInstruments.notNamed` í leikjaskjalinu.

`ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`,
`headTemperature` og `throttle` í töflunni koma héðan, á eigin röðum
upptökumannsins, með því að taka síðustu skilaboðin í mesta lagi 0,2 s eftir
sýninu.

## Færslur flugmódels {#flight-entries}

Færsla flugmódels hverrar flugvélar (pakkategund 2) ber, auk stöðu og afstöðu:

- **Hraði**: 32 bita orð á eftir afstöðunni. Bitar 31, 30 og 29 eru formerki
  x, y og z; svo hraðinn í 11 bitum af 500/2047 m/s (hann stoppar við
  500 m/s), svo |x| og |y| sem brot af hraðanum í 9 bitum hvort, og z er það
  sem gerir vigurinn að einingarvigri. Athugað gegn skrefinu milli móttekinna
  sýna: stefnan stemmir innan brots úr gráðu fyrir upptökumanninn og innan
  um 2 gráða fyrir alla aðra; hraðinn innan 0,2 %. `selfCheck.flightEntries`.
- **Skot á vopn**: listi á undan stöðunni, eitt atriði á vopn, skotin eftir
  fyrst. Listi upptökumannsins er jafn teljurum stjórnklefans einu slagi
  síðar fyrir nær öll sýni.
- **Stýri og inngjöf**: 7 bæti á eftir hraðanum, lesin sem 14 nibbles. Fyrir
  upptökumanninn, í hverju slagi: 1 hæðarstýri, 2 hallastýri, 3 hliðarstýri
  (8 í hvíld), 11 inngjöfin í fimmtándu hlutum (15 líka fyrir neyðarafl og
  eftirbrennara), 4 hjólabremsurnar, 5 loftbremsan, 8 líklega bremsufallhlífin.
  Nibbles annarra flugvéla breytast aðeins nokkrum sinnum í bardaga og eru
  ekki stýri þeirra á þeim tíma.
- **Hreyflar**: á hreyfil stöðubæti (0 slökkt; 1-6 ræsist; 7 í gangi; 8
  dauður), 16 bita gildi aðeins með eftirbrennara (32767 fullt), og bæti
  aðeins eftir að hreyfillinn varð fyrir höggi. Flestar flugvélar sem hreyfill
  verður "dauður" á eru drepnar eða enda innan nokkurra mínútna.

## Speglunargögn {#reflection-data}

Skilaboð 0xF02D og 0xF0AA afrita númeraða hluti leiksins: fyrir hvern hlut
auðkenni hans (efstu 5 bitarnir tegundin, lægstu 11 vísir) og reitatafla.
Tegund 14 eru spilararaufarnar (reitur 2 notandaauðkenni og nafn, 9 liðið),
tegund 15 liðin (vísir 1 og 2):

- Reitur 39 í rauf geymir tölfræði hennar á föstum stöðum: dráp (offset 0),
  liðsdráp (2), dauðsföll (4), sjódráp (10), AI-dráp (12), AI-landdráp (14),
  aðstoðir (20), handtökusvæði (22), skaði á svæði (24, 32 bita), skaðaverðlaun
  (40, 32 bita), flugskeytum forðað (50). Reitur 38 byrjar á stigunum, reitur
  42 er flokkurinn (squad). Í lok bardaga er hvert gildi jafnt niðurstöðunum
  fyrir hvern spilara (`selfCheck.scoreboardVsResults`). Hvar landdráp eru
  geymd er ekki vitað.
- Reitur 7 í liði eru stig þess: í lokin jafnast hann á við summu stiga
  spilara þess í niðurstöðunum. Reitur 3 eru líklega miðar (tickets) þess.
- Hver skilaboð senda aðeins reitina sem breyttust, svo `scoreboard` í
  leikjaskjalinu telur upp tölfræði hvers spilara og stig hvers liðs við hverja
  breytingu.

## Ágiskun á stöðu (dead reckoning) og sléttarinn {#dead-reckoning-and-the-smoother}

Biðlaraupptaka skráir hverja flugvél fjórum sinnum á sekúndu, eins og
biðlarinn teiknaði hana. Milli uppfærslna sem hann fær fyrir fjarlæga flugvél
færir biðlarinn hana áfram eftir síðasta hraða hennar og snýr henni áfram á
síðustu hraðabreytingum hennar, og við næstu uppfærslu kippir hann henni
þangað. Lesinn eins og hann er rennur ferill beint, svo stekkur hann. Ekkert
í færslu flugmódelsins merkir hvaða sýni voru móttekin; sýni sem er ágiskun
þekkist á því hvað það er: það heldur áfram beinu línunni úr tveimur sýnum á
undan því, á þeirra hraða, innan 3 cm.

Hversu miklu þetta skiptir fer eftir bardaganum: í arcade-bardögum geta um
helmingur sýna annarra flugvéla verið ágiskanir, í simulator-bardögum aðeins
fáein prósent. Sléttarinn minnkar skref yfir 15 g um fimmfalt
(`selfCheck.deadReckoning`). Flugvél upptökumannsins er ekki framreiknuð af
biðlaranum og er látin vera eins og hún er.

Sjálfgefið (`--no-smoothing` slekkur á því) eru ferlar allra eininga nema
upptökumannsins settir þangað sem móttekin ástönd segja að þær hafi verið:
sýni sem er ágiskun fer á feril í gegnum móttekin sýni á undan og eftir því,
hvert með sinn hraða; yfir meira en 3 s er beina línan aðeins sveigð í átt að
næsta móttekna sýni, svo ekkert sýni færist lengra en eigin kipp biðlarans.
Afstaða þess er snúin jafnt frá einni mótteknri afstöðu til næstu. Móttekin
sýni eru slétt um í mesta lagi 2 m eða 0,04 s af hraða þeirra; stöðug beygja
helst eins. Eigin gildi upptökunnar haldast í `Raw` dálkunum.

## Afstaða, athuguð {#attitude-checked}

Á eigin flugvél upptökumannsins liggur heading innan gráðu (miðgildi) frá
stefnu ferðar, pitch innan fárra gráða frá klifurhorninu, og í skýrum
beygjum hefur roll formerki beygjunnar fyrir nær öll sýni: roll flugmódelsins
er vinstri vængur niður jákvætt og taflan snýr því í hægri væng niður
jákvætt (`selfCheck.aircraftAttitude`). 10 bita hornin stíga 0,18 gráður.
Afstaða landeininga er athuguð gegn skotum þeirra ([Turnar](ground.md#turrets)).

---

Hluti af [3DHeat](https://github.com/Holdi601/3DHeat) ([skjölun](https://holdi601.github.io/3DHeat/)). Frumkóði: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
