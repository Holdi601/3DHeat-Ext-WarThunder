---
title: Kuidas tööriist kordust loeb
nav_order: 10
lang: "et"
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Kuidas tööriist kordust loeb {#how-it-reads-a-replay}

See leht on inimestele, kes tahavad teada, mida konverter loeb, kuidas seda kontrolliti ja kui palju
usaldada iga veergu. Konverteerimiseks seda vaja ei ole.

Lugemist kontrolliti kliendi kordustel õhu-arcade, õhu-simulaatori ja merelahingutes, serveri
kordustel maapealsetes lahingutes ning 2025. aasta paigutustel avalikel näidiskordustel
([wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder)). Iga kontroll võrdleb väärtust
millegagi, mida kordus ütleb teisel, sõltumatul viisil; siin antakse ainult meetod ja kokkulangevus.

## Mida loetakse ja mille kohta kontroll {#what-is-read-and-the-check}

| Osa | Staatus ja kontroll |
|---|---|
| Päis, kaart, missioon, algusaeg, sessioon; tulemused | iga fail |
| Missiooni seaded (päise järel olev blk) | režiim, ilm, piirangud, `stars` (kuupäev, kellaaeg, koht) |
| Paketivoog (2025 zlib, 2026 zstd) | iga pakett raamitud |
| Lennukite asukohad ja asend (2026 paigutus) | 4 näidist sekundis, ükski pakett loetamata; suund kokkulangeb sõidusuunaga |
| Lennupaketid enne oma aega | pärast võrgu viivitust hoiab kliendi kordusel lennupakett mõnikord iga teist lennukit seal, kus see on umbes 0,75 s hiljem. Ees olek mõõdetakse paketi kaupa ning iga ees olev lennuk saab aja, mida ta tähistab (`selfCheck.flightPacketsRetimed`) |
| Hinnangulise asukoha hüpped | samm hinnangulisest jooksust mõõdetakse viimasest vastuvõetud olekust, nii et kliendi parandused ei lõika enam radu ([Hinnanguline asukoht](aircraft.md#dead-reckoning-and-the-smoother)) |
| Teleporteerumised | rada lõigatakse, kui selle üksus liigub kaugemale, kui suudab: esmalt oma liigi järgi (lennuk 750 m/s, maapealne ja laevad 40 m/s, relvad 1800 m/s), seejärel oma tempo järgi. Iga lõige on loetletud `trackBreaks`-is koos tõenäolise põhjusega (uuestitekitamine, mäng liigutas mängijat, kauge üksuse parandus). Pärast lõikeid ei ole ühegi raja ridade vaheline samm kiirem, kui tema liik lubab (`selfCheck.stepSpeed`) |
| Maapealsed ja laevade asukohad (0xF073 / 0xF074) | ükski pakett loetamata. Suund, pitš ja rull 16-bitisest asendist: suund kokkulangeb sõidusuunaga umbes 2 kraadi täpsusega (mediaan); pitš loetakse 180/65536 kraadi sammudena; rulli märgi pööramisel osutab korpuse ja torni püssi suund peaaegu iga tanki lasu korral tabatud üksusele. Laevad on veetasemel |
| Tornid | tankide torni pööre ja püssi tõus: vt [Tornid](ground.md#turrets) |
| Pakitud maapealsed kõrgused | 64 bitti pakitud asukohad loevad kõrguse −100 m pealt enamikul tasemetel ja veetasemelt mõnel; nihe mõõdetakse igal kordusel üksustelt, mida nähakse mõlemas vormis (`selfCheck.packedGroundHeight`) |
| Olemi voog (loomine, hävitamine) | iga loomine loetud. Paigutus tuleb Dagor Engine'i avaldatud lähtekoodist; War Thunderi enda komponentide tüübid jäetakse vahele, leides, kust järgmine komponent algab. Iga üksuse sõiduk ja mängijakoht võrduvad need, mida tapmise ja tabamuse kirjed nimetavad, iga kontrollitud kirje puhul |
| Kes millist üksust juhtis, AI üksused, laevad, maapealsed sihtmärgid | olemi voost: igal üksusel on oma sõiduk ja meeskond, iga mängija üksusel oma mängija |
| Tapmised tulemuste vastu | mängija kohta surmad võrduvad tulemustega; tulemused loevad rohkem tapmisi, sest kliendile ei saadeta iga tapmist. Kordus, mis algab pärast lahingu algust, sisaldab ainult pärast seda toimunud tapmisi |
| Tapmised, kriitilised tabamused, raske kahju | iga fail |
| Hävitatud moodulid (0xF118) | üksus ja osa number; osa nimi vajab sõiduki kahjumudelit, mida korduses ei ole |
| Vabastatud relvad (olemi voog) | vabastuspunkt on umbes 10-20 m (mediaan) lähimast üksusest, mida peetakse käivitajaks |
| Lendavad relvad (0xF0DB) | rakettid, raketid ja pommid, igaüks seotud oma olemiga |
| Pommid ilma lennukirjeteta | pomm ilma nendeta saab oma languse arvutatud vabastusest tabamuseni (raskus ja takistus, näidis iga 0,1 s, `extrapolated` tõene). Kontrollitud merel, kus tabamuse kõrgus on teada: arvutatud langused lõpevad umbes 15 m piires veepinnast. Mängu dokumendis on selline relv `ballisticImpact`; `counts.bombsBallistic` loeb neid |
| Mängijakohad, vestlus | iga fail |
| Plahvatused, õhutõrjepursud, autasud, tuvastamised, ilm, missiooni objektid | loetud; asukohti kontrollitakse vaaturis silmaga |
| Salvestajamängija näidikud (0xD04A) | nimetatud selle järgi, mida need teevad: [Kabiini instrumendid](aircraft.md#cockpit-instruments); ülejäänud `notNamed` all |
| Lennukirjete muud väljad | kiirus, laskemoon, juhtimine, mootorid: [Lennukirjed](aircraft.md#flight-entries) |
| Sündmuste ridade asend | iga sündmuse rida kannab oma üksuse suunda, pitši, rulli ja vaatevektorit sel hetkel |
| Mängijate statistika ja meeskondade skoorid | lahingu lõpus võrdub iga statistika tulemustes oleva väärtusega iga mängija kohta: [Peegelduse andmed](aircraft.md#reflection-data) |
| Relvade ja sõidukite nimed | sinu installatsiooni inglisekeelsest lokaadist; mõnel laeva vaikevööl ja lennuvälja radaril mängus nime ei ole |
| Mängijad ja AI | ükski tulemuste mängija rida ei ole AI, iga mitte-AI rida on tulemuste mängija (`selfCheck.identity`) |
| Vrakid | üksuse näidised pärast surma jätkuvad; maapealse üksuse või laeva vrak on `alive` 0, kuni tema olem eemaldatakse, ja jääb üheks rajaks; lennukid jätavad `alive` 0 kuni 60 s (`selfCheck.wrecks`) |
| Sõidukivahetused | mängija üksus, mis on veel elus, kui sama mängija järgmine üksus ilmub, lõpetatakse seal (sõiduk jäi seisma). `selfCheck.vehicleSwitch.twoLiveVehicles` peab olema 0 |
| Lahingurežiim | [Lahingurežiim](ground.md#battle-mode) |
| Lennukid 2026 serveri kordusel | loetud 2026 paigutuses; suund ja rulli märk kokkulangevad pööretega; kohahoidja-lennukid ja luurelennukid ei kanna andmeid |
| Serveri korduse mängijad | leitud nime järgi kohtadest; iga statistika võrdub tulemustega (`selfCheck.players`) |
| Lennukid 2025 serveri kordustes ja versioonis 101286 | ei loeta: nende lennupakettidel on teine paigutus |

## Sõnumid üksustele {#messages-to-units}

Iga tüübi-4 pakett on Dagor Engine'i daNet mpi-sõnum: adressaadi objekti ID, seejärel (kui selle
madalad 11 bitti on kõik seatud) objekti laiendatud UID, sõnumi ID ja sisu. Üksusele saadetud sõnum
kannab laiendatud UID-ina üksuse olemi ID-d, `index << 10 | generation`. Kontrollitud: iga selline sõnum
nimetab olemit, mis sel hetkel elas.

Spetsialistidele: loetud sõnumid on:

| Sõnum | Mis see on ja kuidas kontrolliti |
|---|---|
| 0xF0E9 UnitHitEffects | ühe projektili tabamus: laskja uid ja tabamuspunkt üksuse raamistikus (x ees, y üles, z vasakule): sentimeetrid lennukitel ja laevadel, 20/32768 m samm maapealsetel üksustel (sobitatud tankitornide suurusele). `hitLocalX/Y/Z` meetrites. Muutub reaks `shot` ([Tulistamine](hits.md#gunfire)). Peaaegu iga tabamuse ja tapmise kirje ründaja on nende laskjate hulgas; tabamuspunktid asuvad laskja poole näival küljel |
| 0xF133 UnitOnExplosion | sama laskja uid |
| 0xF04B OnUnitDead | `dead` read: iga tapmiskirje ohvril on see 2 s jooksul |
| 0xD047 FmwRpm | mootorite pöörded (`rpm`); kokkulangeb kabiini pöörete näidikuga |
| 0xF0B1, 0xF0A0 | `gun_shot` read: raske õhutõrje ja suurtükiväe üksikud lasud |
| 0xF01B, 0xF01C | read `fire_start`, `fire_stop`: 40 mm õhutõrjekahurite pursud (kahur tulistab; sõidukil põlev tulekahju on `fire_on`, vt [Sõiduki tulekahjud](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` read |
| 0xD0FE ProjectileHitReplay | salvestajamängija enda tabamused ja temale tabamused, koos relva ja laskemooniga, nimetatud installatsioonist (`projectileHitReplays`) |
| 0xF13E, 0xF031 | tabamuse visuaalne efekt ja üksusel mängitud efekt; need tulevad samal üksusel tabamusega |
| 0xD041 | üks iga lennuki kaitserelva kohta, kaks korda sekundis; tema indeksid kattuvad lennukimudeli tulistajarelvadega |
| 0xD048, 0xF117 | paigutus loetud, tähendus teadmata |
| ülejäänud (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | sõnumite lisafailis koos oma üksuse ja väljadega |

Nimed on kogukonna omad (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Veel loetud {#also-read}

- **Olemi voo replikatsioon** (0x22, 0x23): iga olemi kohta komponentide väärtuste plokk: laeva
  remondiajastid, kulumaterjalide kogused, omaniku ja meeskonna muutused, mootori ülekuumenemine.
  Loendatud `counts.replicatedComponents`-is; väärtused sõnumite lisafailis.
- **Missiooniskripti tegevused** (0xF028) ja **vihjed** (0xF0EC): `triggers`, `hints`.
  **Missiooni edenemine** (0xF07A, 0xF07C): `missionProgress`.
- **Kordusekaamera** (0xD043): vt [Kaamera](ground.md#the-camera).

## Ei loeta, ja miks {#not-read-and-why}

- **Olemi sõnumite nimed ja sisu** (0x20, 0x21): klassi number on koha loendis, mis on mängu sisse
  koostatud; seda ei saadeta ega ole selle andmetes. Kaks loetakse (sõiduki tulekahjud ja nende
  kustutajad); ülejäänud hoitakse tervena koos oma olemi ja klassi numbriga.
- **Muud replitseeritud objektid** (muud liigid kui mängijakohad ja meeskonnad): loetud ja hoitud,
  nimetamata; tulemustes ei ole midagi, mille vastu neid kontrollida.
- **Teiste lennukite juhtimine, gaas ja laskemoon**: värskendatakse ainult aeg-ajalt; hoitakse lennu
  lisafailis, mitte tabelis.
- **Lennukite tulekahjud**: ei leitud üheski sõnumis; põlev lennuk ei saa `fire_on` rida.
- **Vabastatud relvade nimed**: pommi või raketi olem ei hoia nime; tapmiskirjed nimetavad tapmise relva.
- **Mööda läinud lasud**: kordus hoiab ainult tabamusi.

Iga mängu dokumendi `counts.messageIdsNotRead` ja `selfCheck` ütlevad, mida uus kordus sisaldab ja kui
hästi see loeti.

---

Osa [3DHeatist](https://github.com/Holdi601/3DHeat) ([dokumentatsioon](https://holdi601.github.io/3DHeat/)). Lähtekood: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
