---
title: Lennukid
nav_order: 11
lang: et
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Lennukid {#aircraft}

Lugejatele, kes tahavad teada, kust lennukeveerud pärinevad ja kui palju neid usaldada.
Iga kontroll allpool võrdleb väärtust millegagi, mida kordus ütleb teisel, sõltumatul
viisil; antakse ainult meetod ja kokkulangevus.

## Kabiini instrumendid {#cockpit-instruments}

Sõnum 0xD04A saadab salvestajamängija näidikud paaridena (number, väärtus): arcade-lahingutes
neli sekundis, simulaatori-lahingutes ainult muutunud väärtused. Numbrid moodustavad ühe
loendi kõigi kabiinide üle ning kabiin saadab näidikud, mis tema mudelil on. Mängu kood
määrab, milline number milline näidik on; seega iga number nimetati selle järgi, mida ta
teeb, ja kontrolliti kordust vastu (`convert.INSTRUMENTS` hoiab tulemust; installatsioonist
ei loeta midagi):

| Number | Nimi | Kontrollitud vastu |
|---|---|---|
| 0 | näidatud õhkiirus, m/s | raja kiirus õhutiheduse järgi parandatuna: korrelatsioon 0,99 |
| 39 | tõusukiirus, m/s | raja tõusukiirus: korrelatsioon üle 0,99 |
| 40, 41 | kõrgus, m; kõrgus modulo 1000 | raja kõrgus, mõne meetri täpsusega |
| 52, 53 | tehisliku horisondi rull ja pitš | miinus tabeli rull ja pitš, alla 1 kraadi täpsusega |
| 64 | kompass | tabeli suund, alla 0,1 kraadi täpsusega |
| 15-20 | pedaalid | külgjõud lennukil |
| 23, 31 | sidemik: kõrguser ja rullid (märk kabiinimudeli oma) | rünnakunurk; rullkiirus |
| 69, 71, 73 | kell: tunnid (12-tunnine ring), minutid, sekundid | salvestusarvuti kohalik aeg, minuti täpsusega |
| 75 | sisselaskerõhk, atm | kõrgem sõjalise hädavõimsuse korral kui täisgaasil |
| 81-86, 87-92, 93-98 | pöörded mootori kohta, pöörded modulo 1000, pöörete näidik | üksteisega täpselt; mootori pöörded: korrelatsioon üle 0,97 |
| 195 | kütus | langeb lennu jooksul, täitub taas taasilmumisel |
| 228-230 | maandumisrataste jalad, 1 = all | all ainult lennuväljade kõrguse lähedal ja maandumiskiirusel |
| 240, 241 | gaas mootori kohta (1,1 sõjaline hädavõimsus või järelpõletaja) | lennukirje gaas |
| 330-332, 346-348 | laskemoonaloendurid (kaks võrdset komplekti) | relvaeelsiste laskemoon, kahanedes lennukirje laskemooniga |
| 135, 159 | õli ja silindripea temperatuur | tõenäoliselt: tõusevad lennu jooksul |
| 58, 61 | libisemispall, pöördenõel | tõenäoliselt: järgivad külgjõudu ja pöördekiirust |
| 223 | õhupidur | tõenäoliselt: seatud ainult maandumisel |
| 490-497, 500-505 | rattapidurid | tõenäoliselt: seatud ainult lennuväljal seistes |

Mõned veel numbrid saadetakse, mille tähendus on teadmata; need hoitakse mängu dokumendi
`authorInstruments.notNamed` all.

Tabeli `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature`
ja `throttle` tulevad neist, salvestajamängija enda ridadel, võttes viimase sõnumi kuni
0,2 s enne näidist.

## Lennukirjed {#flight-entries}

Iga lennuki lennukirje (paketitüüp 2) sisaldab lisaks asukohale ja asendile:

- **Kiirus**: 32-bitine sõna pärast asendit. Bitid 31, 30 ja 29 on x, y ja z märgid; siis
  kiirus 11 bitis 500/2047 m/s (peatub 500 m/s juures), seejärel |x| ja |y| kui murdosad
  kiirusest, 9 bitti kumbki, ja z on see, mis teeb vektorist ühikvektori. Kontrollitud
  vastu vastuvõetud näidiste vahelist sammu: suund kokkulangeb salvestajamängija puhul
  kraadi murdosa täpsusega ja teiste puhul umbes 2 kraadi täpsusega; kiirus 0,2 %
  täpsusega. `selfCheck.flightEntries`.
- **Laskemoon relva kohta**: nimekiri enne asukohta, üks kirje iga relva kohta, esimesena
  alles jäänud laskemoon. Salvestajamängija oma võrdub peaaegu iga näidise puhul kabiini
  loendurite omaga ühe takti hiljem.
- **Juhtimine ja gaas**: 7 baiti pärast kiirust, loetuna 14 nibblina. Salvestajamängija
  puhul igal taktil: 1 kõrgusroor, 2 rullid, 3 roolid (8 seisus), 11 gaas viiteistkümnendikes
  (15 ka sõjalise hädavõimsuse ja järelpõletaja korral), 4 rattapidurid, 5 õhupidur, 8
  tõenäoliselt pidurivarjund. Teiste lennukite nibblid muutuvad lahingu jooksul ainult mõned
  korrad ja ei ole nende juhtimine sel hetkel.
- **Mootorid**: mootori kohta olekubait (0 väljas; 1-6 käivitub; 7 töötab; 8 seisab),
  16-bitine väärtus ainult järelpõletajaga (32767 täis), ja bait ainult pärast mootori
  tabamust. Enamik lennukeid, mille mootor läheb "dead" olekusse, hukkub või lõpeb
  minutite jooksul.

## Peegelduse andmed {#reflection-data}

Sõnumid 0xF02D ja 0xF0AA replitseerivad mängu nummerdatud objekte: iga objekti kohta selle
ID (ülemised 5 bitti liik, madalad 11 indeks) ja väljade tabel. Liik 14 on mängijate kohad
(väli 2 kasutaja ID ja nimi, 9 meeskond), liik 15 meeskonnad (indeks 1 ja 2):

- Koha väli 39 hoiab tema statistikat kindlates kohtades: tapmised (nihe 0), meeskonnakaaslaste
  tapmised (2), surmad (4), merel tapmised (10), AI tapmised (12), AI maapealsed tapmised (14),
  abistamised (20), vallutussoonid (22), soonekahju (24, 32-bitine), kahjupreemia (40, 32-bitine),
  rakettidest kõrvalehoidmised (50). Väli 38 algab skoorist, väli 42 on rühm. Lahingu lõpus
  võrdub iga väärtus iga mängija tulemustes oleva väärtusega (`selfCheck.scoreboardVsResults`).
  Kus maapealsed tapmised hoitakse, ei ole teada.
- Meeskonna väli 7 on tema skoor: lõpus võrdub see tema mängijate skooride summaga tulemustes.
  Väli 3 on tõenäoliselt tema piletid.
- Iga sõnum saadab ainult muutunud väljad, seega mängu dokumendi `scoreboard` loetleb iga
  mängija statistika ja iga meeskonna skoori igal muutusel.

## Hinnanguline asukoht ja silur {#dead-reckoning-and-the-smoother}

Kliendi kordus salvestab iga lennuki neli korda sekundis, nii nagu klient seda joonistas.
Kaugema lennuki värskenduste vahel, mida klient saab, liigutab klient seda edasi tema viimase
kiiruse järgi ja pöörab viimase kiiruse järgi, ning järgmise värskenduse korral hüppab ta
sinna. Loetuna nii, nagu see on, joonis jookseb sirgelt ja siis hüppab. Miski lennukirjes ei
märgi, millised näidised on vastu võetud; hinnanguline näidis leitakse selle järgi, mis ta on:
ta jätkab kahe eelmise näidise sirget joont nende tempos 3 cm täpsusega.

See, kui palju see loeb, sõltub lahingust: arcade-lahingutes võib umbes pool teiste lennukite
näidistest olla hinnangulised, simulaatori-lahingutes ainult mõni protsent. Silur lõikab
15 g ületavad sammud umbes viis korda (`selfCheck.deadReckoning`). Salvestajamängija enda
lennukit klient ei ekstrapoleeri ja seda jäetakse nii, nagu on.

Vaikimisi (`--no-smoothing` lülitab selle välja) asetatakse kõigi üksuste rajad, välja arvatud
salvestajamängija oma, sinna, kus vastuvõetud olekud ütlevad, et nad olid: hinnanguline näidis
läheb kõvera peale, mis läbib seda ümbritsevad vastuvõetud näidised, igaüks oma kiirusega;
üle 3 s läheb sirge joon ainult järgmise vastuvõetud näidise poole painutatult, nii et ükski
näidis ei liigu kaugemale kui kliendi enda hüpe. Asend pöörab ühtlaselt ühest vastuvõetud
asendist järgmiseni. Vastuvõetud näidised silutakse kuni 2 m või 0,04 s nende kiiruse ulatuses;
ühtlane pööre jääb nii nagu on. Kordusega antud väärtused jäävad veergudesse `Raw`.

## Asend, kontrollitud {#attitude-checked}

Salvestajamängija enda lennukil langeb suund mediaanina kraadi täpsusega sõidusuunaga, pitš
mõne kraadi täpsusega tõusunurgaga, ja selgetes pööretes on rulli märk pöörde märgiga peaaegu
iga näidise puhul: lennumudeli rull on vasak tiib alla positiivne, ja tabel pöörab selle
parem tiib alla positiivseks (`selfCheck.aircraftAttitude`). 10-bitised nurgad astuvad 0,18
kraadi kaupa. Maapealsete üksuste asendit kontrollitakse nende laskude järgi
([Tornid](ground.md#turrets)).

---

Osa [3DHeatist](https://github.com/Holdi601/3DHeat) ([dokumentatsioon](https://holdi601.github.io/3DHeat/)). Lähtekood: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
