---
title: Taulukko
nav_order: 6
lang: "fi"
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# Taulukko {#the-table}

![Synteettisen replayn taulukko, tiivistettynä](../assets/img/table.svg)

Yksi rivi näytettä tai tapahtumaa kohden, 105 saraketta ([Sarakeluettelo](../columns.md), luotu koodista);
alatunnisteessa, kohdassa `heat3d`, katselimen lukuohjeet, joten katselin ei tarvitse
mitään täytettävää lomaketta.

| Sarake | Mitä se on |
|---|---|
| `time` | sekunteina replayn omalla kellolla |
| `event` | `position`; tapahtumarivit ovat radalla hetkellään (kahden näytteen välissä, niiden välisellä viivalla); `kill` (tappajan kohdalla), `death` (uhrin kohdalla), `hit_critical` / `hit_severe` (osuman saaneen yksikön kohdalla), `module_destroyed` (yksikön kohdalla), `launch` (yksikön kohdalla, joka laukaisi aseen), `impact` (aseen viimeinen näyte, kun se poistettiin heti sen jälkeen); `explosion` ja `flak` (0xD08E, 0xD01F) omassa paikassaan, tyyppi `effect`, ei rataa, ja räjähdyksen suunta, jos sillä on sellainen; `shot` (osunut ammus, ampujan kohdalla), `gun_shot`, `fire_start`, `fire_stop` (tykin purske, ei ajoneuvo tulessa), `fire_on`, `fire_off` (ajoneuvo tulessa, katso [Ajoneuvojen palot](hits.md#vehicle-fires)), `reward` (ansaitut Silver Lions ja tutkimuspisteet, katso [Talous](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (katso [Viestit yksiköille](how-it-reads.md#messages-to-units)); `despawn`: radan viimeinen rivi, kun sen yksikkö on poistunut ennen replayn loppua (katso [Radan loppu](ground.md#end-of-a-track)) |
| `track` | se, minkä katselin piirtää yhtenä asiana: yhden yksikön yksi elämä tai yhden aseen lento - `<pelaaja tai ajoneuvo> #<hex>` (katselin näyttää nimen ilman `#`-osaa) |
| `x`, `y`, `z` | pelin metrit: x itään, y ylös, z pohjoiseen (vihjeet peilaavat z:n, joten pohjoinen ei piirry etelään) |
| `player` | pelaajan nimi; tekoälyyksikkö `<VehicleName> #<uid>` (esimerkiksi `F-15A #204`); `uid <n>`, kun mikään ei nimeä sitä; aseelle se, joka laukaisi sen |
| `userId`, `team` | pelaajan Gaijin-tunnus ja joukkue (`1`, `2`) |
| `ai`, `isPlayer` | `ai` on tosi jokaiselle yksikölle, jota mikään pelaajatili ei ohjaa (tehtävän yksiköt, tekoälylentokoneet, maakohteet, ilmatorjuntatykit, pelaajattomat laivat, paikanpitäjät), `isPlayer` on päinvastainen: pelaaja on yksikkö, jonka kokonaisuus nimeää pelaajapaikan Gaijin-tunnuksella. Aseella on laukaisijansa arvo; tyhjä, kun se ei ole tiedossa |
| `match` | ottelun tunnus (ottelun asiakirjan `match`), jokaisella rivillä; vihjeet kartoittavat sen istuntona, joten kaksi ladattua replayta ei koskaan yhdistä ratoja |
| `life` | `uid#n`: yhden yksikön rata, katkaistuna kun uid siirtyy toiselle yksikölle, yksikkö liikkuu nopeammin kuin voi (uudelleensyntyminen, uudelleen aseistus, peli siirtää sitä, asiakas korjaa kaukaista yksikköä; katso Teleports kohdassa [Miten replay luetaan](how-it-reads.md#what-is-read-and-the-check)) tai se on pitkään näkemättä; `w<hex>` aseen lento (`w<hex>#n` katkaisun jälkeen) |
| `uid` | yksikön tunnus replayssa |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (raitiovaunu tai junanvaunu, jonka kenttä sijoittaa, katso [Kohtauksen yksiköt](objectives.md#scene-units-trams-and-rail-wagons)); aseet `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` tallentavan pelaajan replay-kamera (katso [Kamera](ground.md#the-camera)) |
| `type` | pelin oma tyyppi, kun tulokset sen nimeävät (`fighter`, `assault`, `destroyer`, `gun_boat`), muuten sama kuin `kind` |
| `Vehicle` | pelin oma ajoneuvotunnus (`f_15a`, `germ_flakpz_I_Gepard`), johon katselimen hahmot täsmäävät |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | ajoneuvon englanninkielinen nimi asennuksesi lokalisoinnista (`Pz.Kpfw. III Ausf. J1`, lyhyt `Pz.III J1`) ja sen avain (`germ_pzkpfw_III_ausf_J_0`); pelin fontin maamerkit jätetään pois. Kun peli ei nimeä mitään tai asennusta ei löydy, nimi on tunnus ja avain tyhjä |
| `mission` | yksikön nimi tehtävässä (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | mihin suuntaan yksikkö osoittaa (katselusuuntavektori): lentokoneet lentomallin asennosta, maayksiköt ja laivat omistaan, aseet lentonsa suuntaan |
| `heading`, `pitch`, `roll` | samat asteina; heading on kompassi, myötäpäivään pohjoisesta, pitch positiivinen kun nokka ylös, roll positiivinen kun oikea siipi alas (lentomallin merkki on päinvastainen, katso [Asento, tarkistettu](aircraft.md#attitude-checked); maayksikön oikea puoli alas). Vihjeet kertovat tämän kohdassa `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | säiliön pääterret - mihin tykki osoittaa, ei minne pelaaja katsoo; replayn arvo pidettynä tornin käyttömoottorin nopeudessa ja asetettuna jokaisen pääaseen laukauksen linjalle (katso [Tornit](ground.md#turrets)): sen kääntö rungon suhteen (asteina, myötäpäivään ylhäältä katsottuna positiivinen, 0 suoraan edessä) ja tykin kallistus rungon suhteen (asteina, ylös positiivinen); `turrets` kaikki ajoneuvon tornit muodossa `yaw pitch;yaw pitch;...` omassa järjestyksessään (käyttämätön paikka lukee `0.00 0.00`). Säiliöt, SPAA, APC:t ja kuorma-autot, asiakas- ja palvelinreplayissa; ei laivat (katso [Tornit](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | pääterret sellaisena kuin replay sen lähettää; `turretYaw` / `gunPitch` ovat sen pidettynä tornin käyttömoottorin nopeudessa ja asetettuna jokaisen pääaseen laukauksen linjalle (katso [Tornit](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | minne pelaaja katsoo (tähtää kameralla) maailmassa: kompassiasteet (0 pohjoinen, myötäpäivään) ja ylös kohoavat asteet, samassa merkintätavassa kuin `aimHeading` / `aimPitch` (toisin kuin `turretYaw` / `gunPitch`, jotka pysyvät suhteessa runkoon). Jokaisen pelaajan säiliö palvelinreplayssa, tallentavan pelaajan oma asiakasreplayssa; tyhjä, kun pelaaja ei tähtää mihinkään (kaikki neljä tähtäysliukulukua 0). Torni seuraa sitä omalla kääntönopeudellaan, joten ne eroavat, kun se kääntyy (katso [Tornit](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | tallentavan pelaajan oma säiliö: minne se tähtää (kompassiasteet, ylös kohoavat asteet, etäisyys metreinä; 2000, kun tähtäimessä ei ole mitään); kamerarivit: minne pelaaja tähtää (heading, pitch) |
| `zoom` | kamerarivit: kameran suurennus (katso [Kamera](ground.md#the-camera)) |
| `difficulty`, `gameMode` | taistelun `AB`, `RB` tai `SB`, ja `ground`, `air` tai `naval`, jokaisella rivillä (katso [Taistelutila](ground.md#battle-mode)) |
| `extrapolated` | lentokoneen näyte, joka on asiakkaan laskennallinen liike, ei vastaanotettu tila (katso [Laskennallinen liike](aircraft.md#dead-reckoning-and-the-smoother)); pommin näyte, joka on laskettu sen irrotuksesta (katso Bombs without flight records kohdassa [Miten replay luetaan](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | kuinka paljon tasoittaja siirsi näytettä (m), ja replayn oma sijainti ja asento (roll taulukon merkillä) |
| `targetX`, `targetY`, `targetZ` | `shot`-rivin osumapiste |
| `hitOutcome`, `hitFlags` | `shot`-rivin lopputulos maayksikössä: `kill`, `critical`, `penetration` tai `nonpenetration` (kimpoaminen tai pysäytys: replay ei erota ricochet-osumaa), palvelimen osuman mukana lähettämistä biteistä (`hitFlags`, raakana); tyhjä, kun mitään ei lähetetä (lentokoneet, laivat). Katso [Osuman lopputulokset](hits.md#hit-outcomes) |
| `hitShell` | `shot`-rivin ammuksen tunniste: neljä tavua osumaviestistä (raaka hex); yksi tunniste voi tarkoittaa eri ammuksia (120 ja 125 mm APFSDS jakavat yhden), joten se säilytetään raakana, ei luettuna kaliiperina |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | `shot`-rivin ammus: sen tyyppi (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) ja tunnus (`125mm_3bm46`), kun tappo nimeää ampujan paikan, muuten `explosive` (osumapurkaus) tai `kinetic`; tykin `weapon/slot` uudelleenlatauksistaan; kaliiperi mm asennuksen aseen tiedostoista. Katso [Osuman lopputulokset](hits.md#hit-outcomes) |
| `rpm` | lentokoneen moottorin kierrosluku (moottorien keskiarvo) viimeksi lähetettynä, 2 s:n sisällä |
| `vx`, `vy`, `vz` | lentokoneen nopeusvektori sellaisena kuin sen lentomerkintä sen lähettää (m/s, pelin akselit; yli 500 m/s:n nopeudet luetaan 500:ksi) |
| `engine`, `afterburner`, `engineCondition` | lentokoneen moottorit lentomerkinnästä: `off`, `starting`, `running`, `dead` (`/`-erotettuna, kun moottorit eroavat); jälkipoltin 0-1; tavu, joka lähetetään vain sen jälkeen, kun moottoriin osui |
| `weaponName` | tappot ja kuolemat: ase tai ammus asennuksesi englanniksi (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | vain tallentavan pelaajan lentokone: kaasu 0-1,1 ohjaamosta (1,1 sotatilan hätävoima tai jälkipoltin; muuten sen lentomerkinnän kuudesosat), ohjaimet -1..1 sen lentomerkinnästä (hissi positiivinen vedettäessä, aileron positiivinen kallistuttaessa oikealle), jäljellä olevat laukaukset aseittain (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | vain tallentavan pelaajan lentokone, ohjaamosta: mittaristonopeus ja nousunopeus (m/s), polttoaine, imupaine (atm), vaunut (0-1, 1 alhaalla), öljyn ja sylinterikannen lämpötila, kun ohjaamossa on kyseinen mittari |
| `speed` | m/s radan noin kahden sekunnin ajalta (laskettu täällä; replay ei lähetä nopeutta muille yksiköille) |
| `alive` | 0 yksikön näytteille sen kuoleman jälkeen (sen hylky): maayksikön tai laivan kunnes peli poistaa sen tai sen näytteet loppuvat, lentokoneen enintään 60 s |
| `otherVehicle`, `otherLife` | `shot`-rivin uhri: sen ajoneuvo ja sen `life` |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | `shot`-rivin osumapiste uhrin omassa koordinaatistossa (m; x eteen, y ylös, z vasemmalle; katso [Viestit yksiköille](how-it-reads.md#messages-to-units)) ja laukauksen tulosuunta, käännettynä uhrin koordinaatistoon uhrin silloisen asennon mukaan |
| `hitPart`, `hitFlag` | `shot`-rivin osumaviesti: sen osasana sellaisena kuin se lähetettiin, ja sen korkein tavu |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | mitä taistelu maksoi ja tuotti ja kuka voitti: katso [Talous](economy.md) |
| `other`, `weapon` | tappot: toinen puoli ja ase; osumat: kuka osui (tietueen uid:stä, muuten pelaajapaikasta), heidän ajoneuvonsa; laukaisut: ase; tuhoutuneet moduulit: kuka osui yksikköön viimeksi 5 s ennen sitä, ja `part <n>` |

---

Osa [3DHeatiä](https://github.com/Holdi601/3DHeat) ([dokumentaatio](https://holdi601.github.io/3DHeat/)). Lähde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
