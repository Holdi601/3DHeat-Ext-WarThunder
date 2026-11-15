---
title: Ottelun asiakirja
nav_order: 7
lang: fi
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# Ottelun asiakirja {#the-match-document}

![Synteettisen ottelun asiakirjan alku ja sen avaimet](../assets/img/match-document.svg)

`<match>.match.json` sisältää kaiken, minkä replay kertoo ja joka ei ole taulukon rivi.
Katselimen Ottelu-välilehti lukee sen.

## Taistelu {#the-battle}

| Avain | Mitä se on |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | ottelun tunnus (kuten tiedostonimessä); kartan tunnus; kenttätiedosto, jota se käyttää |
| `mission`, `missionKey` | tehtävän nimi ja sen avain pelin tekstitiedostoissa |
| `battleClass`, `environment`, `weather` | sellaisina kuin otsikko ne antaa |
| `sessionId`, `server` | taistelun istuntotunnus; palvelin |
| `replayVersion`, `flightLayout` | replay-muodon versio; luettu lentopakettien asettelu (`2025` tai `2026`) |
| `files` | luetut replay-tiedostot (yksi, tai palvelimen replayn osat) |
| `started`, `timePlayed`, `replayEnd` | aloitusaika (ISO, UTC); pelatut sekunnit, tuloksista; replayn viimeisen paketin sekunnit |
| `author`, `authorUserId` | tallentava pelaaja ja hänen Gaijin-tunnuksensa (asiakasreplayt) |
| `teams` | taistelun joukkueet (`1`, `2`) |
| `result` | `winner`, `status` (`success` tai `fail`, tekijän lopputulos), `authorTeam`, `teams` ([Talous](economy.md)) |
| `vehicleNames` | mistä ajoneuvojen nimet tulivat (asennuksesi) ja niiden kieli |
| `conventions` | taulukon yksiköt ja merkit: akselit, aika, elämä, rata, `alive`, roll ja muuta |

## Kaikki muu {#everything-else}

| Avain | Mitä se on |
|---|---|
| `battle`, `difficulty`, `gameMode` | taistelutila: `difficulty` `AB` / `RB` / `SB` (sekä sen nimi ja otsikkotavu), `gameMode` `ground` / `air` / `naval`, tehtävän tila (`Dom`, `Conq`, `Bttl`, `I2M`, ...) ja sen englanninkielinen nimi asennuksestasi (`Domination`, `Enduring Confrontation`), sallitut yksikkötyypit (katso [Taistelutila](ground.md#battle-mode)) |
| `settings` | tehtävän blk otsikon jälkeen: tila, ympäristö, sää, pistemäärä- ja aikarajat, maat, sallitut yksikkötyypit, tuuli ja `stars` (leveyspiiri, pituuspiiri, päivämäärä, paikallinen aika) |
| `sky` | ensimmäinen `CustomWeatherParams`: auringon ja kuun suunta, tuuli, taivaan värit, pilvien siirtymät |
| `players`, `slots` | tulosten rivi pelaajaa kohden (tapot, maatappot, kuolemat, avustukset, pisteet, valloitukset, ryhmä, klaani, maa, kokoonpano, ajetut uidit); replayn pelaajapaikat (nimi, käyttäjätunnus, joukkue) |
| `units` | jokainen yksikkökokonaisuus, jonka replay loi: eid, uid, malli, ajoneuvo, tyyppi, joukkue, pelaaja, tehtävän nimi, milloin se luotiin ja poistettiin, missä se luotiin, mitkä komponentit eivät olleet luettavissa |
| `objects` | tehtävän nimetyt kohteet: valloitusalueet ja lentokentät sijaintinsa ja kokonsa kanssa, lentokenttien ääriviivat pisteinä, lähtöalueet |
| `objectives` | taistelun tavoitteet, kukin `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (replayn 1 tai 2, tyhjä molemmille), `name` (valloitusalueella sen kirjain, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) kohdissa `position`, `radius` / `height` / `size` ja `heading`, `source` (`replay` tai `mission`) ja muu tunnettu tieto (katso [Tavoitteet](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | nimineen ja ajoneuvoineen molemmilta puolilta; tapot aseen englanninkielisellä nimellä |
| `weapons` | jokainen raketti, ohjus, pommi, torpedo, pudotuspolttoainesäiliö ja irrotettu kuorma: milloin, mistä irrotettiin (sijainti, asento, nopeus), mikä yksikkö (lähin 300 m:n ja 1,5 s:n sisällä), kuinka monta lentonäytettä, missä viimeksi nähtiin, milloin poistettiin |
| `explosions`, `flak` | `PlayExplosionVisual` (sijainti, suunta, tyyppi) ja `PlayFlakExplosionVisual` (sijainti) |
| `awards` | tallentavan pelaajan palkinnot (`TextStreak`: first_blood, putket, haastelaskurit) |
| `detections`, `unitStates` | `UnitDetected`-parit yksiköistä; viesti (0xF093), jossa on yksikön sijainti, asento ja nopeus ja jonka merkitystä ei tunneta |
| `authorInstruments` | tallentavan pelaajan ohjaamon arvot (`ReplayCockpitParams`) mittarinumeron mukaan, enintään yksi sekunnissa; `known` nimeää jokaisen numeron, jonka tämä replay lähetti (nimi, yksikkö, miten se tarkistettiin), `notNamed` loput |
| `scoreboard` | jokaisen pelaajan tilastot aina, kun ne muuttuivat (tapot, kuolemat, avustukset, pisteet, tekoälytapot, laivatapot, alueet, vahinko, ohjusten väistöt, ryhmä), ja jokaisen joukkueen pistemäärä ja arvioidut lipun paikat ajan yli (katso [Heijastustiedot](aircraft.md#reflection-data)) |
| `economy` | taistelun Silver Lions ja tutkimuspisteet (katso [Talous](economy.md)): summat, pelaajittain, ajoneuvoittain, kertoimet, voittaja, tarkistukset |
| `entityMessages` | kokonaisuusviestit (0x20) luokkanumeron mukaan: määrä, kohdemallit, koot |
| `chat` | jokainen keskusteluviesti |
| `triggers`, `hints`, `missionProgress` | tehtävän käsikirjoituksen toiminnot (RunTriggerAction), sen vihjeet, sen edistymisviestit |
| `camera` | tallentavan pelaajan replay-kameran kentät 0,25 s välein sellaisina kuin ne lähetettiin (taulukossa se on rata) |
| `projectileHitReplays` | tallentavan pelaajan omat osumat ja osumat hänen itseensä, aseen ja ammuksen sekä niiden englanninkielisten nimien kanssa |
| `results` | koko tulosten blk sellaisena kuin peli sen kirjoitti |
| `counts` | rivit, tapahtumat, elämät, tyypit, näytteet, kokonaisuudet mallin mukaan, aseet, paketit luettu ja lukematta, jokainen nähty viestitunnus ja ne, joita ei luettu, pudotetut näytteet |
| `trackBreaks` | jokainen radan katkaisu, jossa yksikkö liikkuisi liian nopeasti: missä, kuinka pitkälle, kuinka nopeasti ja mitä se todennäköisimmin on |
| `selfCheck` | sivulla [Miten replay luetaan](how-it-reads.md) luetellut tarkistukset, laskettuna jokaisessa muunnoksessa; `stepSpeed` antaa tyypeittäin radan peräkkäisten rivien nopeuden, sellaisena kuin katselin ne yhdistää (mediaani, 99. prosenttipiste, suurin, ja liian nopeat askeleet, joiden on oltava 0) |

---

Osa [3DHeatiä](https://github.com/Holdi601/3DHeat) ([dokumentaatio](https://holdi601.github.io/3DHeat/)). Lähde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
