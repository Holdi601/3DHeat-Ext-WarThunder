---
title: Mängu dokument
nav_order: 7
lang: "et"
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# Mängu dokument {#the-match-document}

![Synteetilise mängu dokumendi algus ja selle võtmed](../assets/img/match-document.svg)

`<match>.match.json` hoiab kõike, mida kordus ütleb ja mis ei ole tabeli rida. Vaaturi Matš-vahekaart
loeb seda.

## Lahing {#the-battle}

| Võti | Mis see on |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | lahingu ID (nagu failinimes); kaardi ID; tase-fail, mida see kasutab |
| `mission`, `missionKey` | missiooni nimi ja tema võti mängu tekstifailides |
| `battleClass`, `environment`, `weather` | nii, nagu päis need annab |
| `sessionId`, `server` | lahingu sessiooni ID; server |
| `replayVersion`, `flightLayout` | kordusformaadi versioon; loetud lennupaketi paigutus (`2025` või `2026`) |
| `files` | loetud kordusefailid (üks või serveri korduse osad) |
| `started`, `timePlayed`, `replayEnd` | algusaeg (ISO, UTC); mängitud sekundid tulemustest; sekundid korduse viimase paketini |
| `author`, `authorUserId` | salvestajamängija ja tema Gaijini ID (kliendi kordused) |
| `teams` | lahingus olevad meeskonnad (`1`, `2`) |
| `result` | `winner`, `status` (`success` või `fail`, autori tulemus), `authorTeam`, `teams` ([Majandus](economy.md)) |
| `vehicleNames` | kust sõidukite nimed tulid (sinu installatsioon) ja nende keel |
| `conventions` | tabeli ühikud ja märgid: teljed, aeg, eluiga, rada, elus, rull ja veel |

## Kõik muu {#everything-else}

| Võti | Mis see on |
|---|---|
| `battle`, `difficulty`, `gameMode` | lahingurežiim: `difficulty` `AB` / `RB` / `SB` (ja tema nimi ning päise bait), `gameMode` `ground` / `air` / `naval`, missiooni režiim (`Dom`, `Conq`, `Bttl`, `I2M`, ...) ja tema inglisekeelne nimi sinu installatsioonist (`Domination`, `Enduring Confrontation`), lubatud üksusetüübid (vt [Lahingurežiim](ground.md#battle-mode)) |
| `settings` | missiooni blk pärast päist: režiim, keskkond, ilm, skoori ja aja piirangud, riigid, lubatud üksusetüübid, tuul ja `stars` (laiuskraad, pikkuskraad, kuupäev, kohalik aeg) |
| `sky` | esimene `CustomWeatherParams`: päikese ja kuu suund, tuul, taevavärvid, pilvede nihked |
| `players`, `slots` | tulemuste rida mängija kohta (tapmised, maapealsed tapmised, surmad, abistamised, skoor, vallutused, rühm, klann, riik, koosseis, sõidukid, mida nad juhtisid uid-idega); korduse mängijakohad (nimi, kasutaja ID, meeskond) |
| `units` | iga üksuse olem, mille kordus lõi: eid, uid, mall, sõiduk, liik, tüüp, meeskond, mängija, missiooni nimi, millal loodi ja eemaldati, kus loodi, millised komponendid ei olnud loetavad |
| `objects` | missiooni nimega objektid: vallutussoonid ja lennuväljad koos asukoha ja suurusega, lennuväljade piirjooned punktidena, tekitamisalad |
| `objectives` | lahingu eesmärgid, igaüks oma `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (kordusest 1 või 2, mõlema jaoks tühi), `name` (vallutussoonil tema täht, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) koos `position`, `radius` / `height` / `size` ja `heading`, `source` (`replay` või `mission`) ja muu, mis on teada (vt [Eesmärgid](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | mõlema poole nimede ja sõidukitega; tapmised relva inglisekeelse nimega |
| `weapons` | iga raketi, rakett, pomm, torpeedo, kukutatav paak ja maha visatud koormus: millal, kust vabastati (asukoht, asend, kiirus), millise üksuse poolt (lähim 300 m ja 1,5 s piires), mitme lennunäidise järgi, kus viimati nähti, millal eemaldati |
| `explosions`, `flak` | `PlayExplosionVisual` (asukoht, suund, liik) ja `PlayFlakExplosionVisual` (asukoht) |
| `awards` | salvestajamängija autasud (`TextStreak`: first_blood, streaks, väljakutsete loendurid) |
| `detections`, `unitStates` | `UnitDetected` üksuste paarid; sõnum (0xF093) üksuse asukoha, asendi ja kiirusega, mille tähendus ei ole teada |
| `authorInstruments` | salvestajamängija kabiiniväärtused (`ReplayCockpitParams`) näidiku numbri järgi, kõige rohkem üks sekundis; `known` nimetab iga numbri, mille see kordus saatis (nimi, üksus, kuidas kontrolliti), `notNamed` ülejäänud |
| `scoreboard` | iga mängija statistika iga kord, kui see muutus (tapmised, surmad, abistamised, skoor, AI tapmised, merel tapmised, soonad, kahju, rakettidest kõrvalehoidmised, rühm), ja iga meeskonna skoor ning tõenäolised piletid ajas (vt [Peegelduse andmed](aircraft.md#reflection-data)) |
| `economy` | lahingu Silver Lions ja uurimispunktid (vt [Majandus](economy.md)): kokkuvõtted, mängija kohta, sõiduki kohta, kordajad, võitja, kontrollid |
| `entityMessages` | olemi sõnumid (0x20) klassi numbri järgi: arv, sihtmallid, suurused |
| `chat` | iga vestlusrida |
| `triggers`, `hints`, `missionProgress` | missiooniskripti tegevused (RunTriggerAction), tema vihjed, tema edenemise sõnumid |
| `camera` | salvestajamängija kordusekaamera väljad iga 0,25 s järel, nii nagu need saadeti (tabelil on see rajana) |
| `projectileHitReplays` | salvestajamängija enda tabamused ja tabamused temale, koos relva ja laskemoonaga ning nende inglisekeelsete nimedega |
| `results` | kogu tulemuste blk, nii nagu mäng selle kirjutas |
| `counts` | read, sündmused, elud, liigid, näidised, olemid malli järgi, relvad, loetud ja mitteloetud paketid, iga nähtud sõnumi ID ja mitteloetud, langetatud näidised |
| `trackBreaks` | iga raja katkestus sammu puhul, mille läbimiseks üksus ei suuda liikuda: kus, kui kaugele, kui kiiresti ja mis see kõige tõenäolisemalt on |
| `selfCheck` | [Kuidas tööriist kordust loeb](how-it-reads.md) loendis olevad kontrollid, arvutatud igal konverteerimisel; `stepSpeed` annab liigi kohta raja järjestikuste ridade vahelise kiiruse, nagu vaatur need ühendab (mediaan, 99. protsentiil, kõrgeim ja sammud, mis on kiiremad kui võimalik, mis peab olema 0) |

---

Osa [3DHeatist](https://github.com/Holdi601/3DHeat) ([dokumentatsioon](https://holdi601.github.io/3DHeat/)). Lähtekood: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
