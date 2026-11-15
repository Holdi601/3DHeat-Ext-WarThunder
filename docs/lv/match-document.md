---
title: Mača dokuments
nav_order: 7
lang: lv
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# Mača dokuments {#the-match-document}

`<match>.match.json` satur visu, ko atkārtojums saka un kas nav tabulas rinda. Skatītāja Mača cilne to nolasa.

![Mača dokumenta sākums un tā atslēgas (sintētisks)](../assets/img/match-document.svg)

## Kauja {#the-battle}

| Atslēga | Ko tā nozīmē |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | mača ID (kā failu nosaukumā); kartes ID; līmeņa fails, ko tā lieto |
| `mission`, `missionKey` | misijas nosaukums un tā atslēga spēles teksta failos |
| `battleClass`, `environment`, `weather` | kā tos dod galvene |
| `sessionId`, `server` | kaujas sesijas ID; serveris |
| `replayVersion`, `flightLayout` | atkārtojuma formāta versija; nolasītais lidojuma paketes izkārtojums (`2025` vai `2026`) |
| `files` | nolasītie atkārtojuma faili (viens, vai servera atkārtojuma daļas) |
| `started`, `timePlayed`, `replayEnd` | sākuma laiks (ISO, UTC); nospēlētās sekundes, no rezultātiem; atkārtojuma pēdējās paketes sekundes |
| `author`, `authorUserId` | ieraksta spēlētājs un viņa Gaijin ID (klienta atkārtojumi) |
| `teams` | kaujas komandas (`1`, `2`) |
| `result` | `winner`, `status` (`success` vai `fail`, autora iznākums), `authorTeam`, `teams` ([Ekonomika](economy.md)) |
| `vehicleNames` | no kurienes nākuši transportlīdzekļu nosaukumi (tava instalācija) un to valoda |
| `conventions` | tabulas vienības un zīmes: asis, laiks, dzīve, celiņš, `alive`, sānu sašķiebums un vēl |

## Viss pārējais {#everything-else}

| Atslēga | Ko tā nozīmē |
|---|---|
| `battle`, `difficulty`, `gameMode` | kaujas režīms: `difficulty` `AB` / `RB` / `SB` (un tā nosaukums un galvenes baits), `gameMode` `ground` / `air` / `naval`, misijas režīms (`Dom`, `Conq`, `Bttl`, `I2M`, ...) un tā angļu nosaukums no tavas instalācijas (`Domination`, `Enduring Confrontation`), atļautie vienību tipi (skat. [Kaujas režīms](ground.md#battle-mode)) |
| `settings` | misijas blk aiz galvenes: režīms, vide, laika apstākļi, punktu un laika robežas, valstis, atļautie vienību tipi, vējš un `stars` (platums, garums, datums, vietējais laiks) |
| `sky` | pirmais `CustomWeatherParams`: saules un mēness virziens, vējš, debesu krāsas, mākoņu nobīdes |
| `players`, `slots` | rezultātu rinda katram spēlētājam (nogalinājumi, sauszemes nogalinājumi, nāves, palīdzības, punkti, iekarotās zonas, komanda, klans, valsts, sastāvs, uid, ar kuriem tie vadīja); atkārtojuma spēlētāju slots (vārds, lietotāja ID, komanda) |
| `units` | katra vienības entītija, ko atkārtojums izveidoja: eid, uid, šablons, transportlīdzeklis, veids, tips, komanda, spēlētājs, misijas nosaukums, kad izveidota un noņemta, kur izveidota, kuras komponentes nevarēja nolasīt |
| `objects` | misijas nosauktie objekti: kapitāla zonas un aerodromi ar pozīciju un izmēru, aerodromu kontūras kā punkti, dzimšanas zonas |
| `objectives` | kaujas mērķi, katrs ar `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (atkārtojuma 1 vai 2, tukšs abiem), `name` (kapitāla zonai tās burts, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) ar `position`, `radius` / `height` / `size` un `heading`, `source` (`replay` vai `mission`) un ko vēl zina (skat. [Mērķi](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | ar abu pušu nosaukumiem un transportlīdzekļiem; nogalinājumi ar ieroča angļu nosaukumu |
| `weapons` | katra raķete, rakete, bumba, torpēda, nomešanas tvertne un atmests krava: kad, kur izlaista (pozīcija, orientācija, ātrums), ar kuru vienību (tuvākā 300 m un 1,5 s laikā), cik lidojuma paraugu, kur pēdējo reizi redzēta, kad noņemta |
| `explosions`, `flak` | `PlayExplosionVisual` (pozīcija, virziens, veids) un `PlayFlakExplosionVisual` (pozīcija) |
| `awards` | ieraksta spēlētāja balvas (`TextStreak`: first_blood, sērijas, izaicinājumu skaitītāji) |
| `detections`, `unitStates` | `UnitDetected` vienību pāri; ziņojums (0xF093) ar vienības pozīciju, orientāciju un ātrumu, kura nozīme nav zināma |
| `authorInstruments` | ieraksta spēlētāja kabīnes vērtības (`ReplayCockpitParams`) pēc instrumenta numura, ne vairāk kā viena sekundē; `known` nosauc katru numuru, ko šis atkārtojums sūtīja (nosaukums, vienība, kā pārbaudīts), `notNamed` — pārējos |
| `scoreboard` | katra spēlētāja statistika, ik reiz, kad tā mainījās (nogalinājumi, nāves, palīdzības, punkti, MI nogalinājumi, jūras nogalinājumi, zonas, bojājumi, raķešu izvairīšanās, vienība), un katras komandas punkti un iespējamās biļetes laika gaitā (skat. [Refleksijas dati](aircraft.md#reflection-data)) |
| `economy` | kaujas Sudraba lauvas un pētniecības punkti (skat. [Ekonomika](economy.md)): kopsummas, pa spēlētājiem, pa transportlīdzekļiem, reizinātāji, uzvarētājs, pārbaudes |
| `entityMessages` | entītiju ziņojumi (0x20) pēc klases numura: skaits, mērķa šabloni, izmēri |
| `chat` | katra tērzēšanas rinda |
| `triggers`, `hints`, `missionProgress` | misijas skripta darbības (RunTriggerAction), tās padomi, tās misijas progresa ziņojumi |
| `camera` | ieraksta spēlētāja atkārtojuma kameras lauki ik pēc 0,25 s, kā tie nosūtīti (tabulā tā ir kā celiņš) |
| `projectileHitReplays` | ieraksta spēlētāja paša trāpījumi un trāpīšana, ar ieroci un munīciju un to angļu nosaukumiem |
| `results` | viss rezultātu blk, kā to uzrakstīja spēle |
| `counts` | rindas, notikumi, dzīves, veidi, paraugi, entītijas pēc šablona, ieroči, nolasītās un nenolasītās paketes, katrs redzētais ziņojuma ID un tie, kas nav nolasīti, izmestie paraugi |
| `trackBreaks` | katrs celiņa pārtraukums ātrākam solim, nekā vienība var iet: kur, cik tālu, cik ātri un kas tas visticamāk ir |
| `selfCheck` | pārbaudes, kas uzskaitītas [Kā tas nolasa atkārtojumu](how-it-reads.md), aprēķinātas katrā pārvēršanā; `stepSpeed` dod katram veidam ātrumu starp blakus rindām celiņā, kā skatītājs tās savieno (mediāna, 99. procentile, augstākā un soļi, kas ātrāki par iespējamo, kuru jābūt 0) |

---

Daļa no [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentācija](https://holdi601.github.io/3DHeat/)). Avots: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
