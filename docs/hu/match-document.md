---
title: "A meccsdokumentum"
nav_order: 7
lang: "hu"
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# A meccsdokumentum {#the-match-document}

![Egy szintetikus meccsdokumentum eleje és kulcsai](../assets/img/match-document.svg)

A `<match>.match.json` mindent tartalmaz, amit a visszajátszás elmond, és ami nem a táblázat
egy sora. A megjelenítő Meccs fülje ezt olvassa.

## A csata {#the-battle}

| Kulcs | Mi |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | a meccs azonosítója (ahogy a fájlnévben); a térkép azonosítója; a pályafájl, amelyet használ |
| `mission`, `missionKey` | a küldetés neve és a kulcsa a játék szövegfájljaiban |
| `battleClass`, `environment`, `weather` | ahogy a fejléc megadja őket |
| `sessionId`, `server` | a csata munkamenet-azonosítója; a szerver |
| `replayVersion`, `flightLayout` | a visszajátszás formátumának verziója; a beolvasott repülési csomag-elrendezés (`2025` vagy `2026`) |
| `files` | a beolvasott visszajátszás-fájlok (egy, vagy egy szerver-visszajátszás részei) |
| `started`, `timePlayed`, `replayEnd` | kezdési idő (ISO, UTC); a lejátszott másodpercek, az eredményekből; a visszajátszás utolsó csomagjának másodperce |
| `author`, `authorUserId` | a felvevő játékos és a Gaijin-azonosítója (kliens-visszajátszásnál) |
| `teams` | a csata csapatai (`1`, `2`) |
| `result` | `winner`, `status` (`success` vagy `fail`, a szerző kimenetele), `authorTeam`, `teams` ([Gazdaság](economy.md)) |
| `vehicleNames` | honnan származnak a járműnevek (a telepítésed) és azok nyelve |
| `conventions` | a táblázat egységei és jelei: tengelyek, idő, élet, pálya, élő állapot, dőlés, és még több |

## Minden más {#everything-else}

| Kulcs | Mi |
|---|---|
| `battle`, `difficulty`, `gameMode` | a csatamód: a `difficulty` `AB` / `RB` / `SB` (és a neve, és a fejléc bájtja), a `gameMode` `ground` / `air` / `naval`, a küldetés módja (`Dom`, `Conq`, `Bttl`, `I2M`, ...) és az angol neve a telepítésedből (`Domination`, `Enduring Confrontation`), a megengedett egységtípusok (lásd [Csatamód](ground.md#battle-mode)) |
| `settings` | a fejléc utáni küldetés-blk: mód, környezet, időjárás, pontszám- és időkorlátok, országok, megengedett egységtípusok, szél, és a `stars` (szélesség, hosszúság, dátum, helyi idő) |
| `sky` | az első `CustomWeatherParams`: a nap és a hold iránya, szél, égszínek, felhőeltolások |
| `players`, `slots` | az eredmények sora játékosonként (ölések, földi ölések, halálok, asszisztok, pontszám, elfoglalások, raj, klán, ország, felállás, az általuk vezetett uid-ek); a visszajátszás játékos-helyei (név, felhasználói azonosító, csapat) |
| `units` | minden egységentitás, amelyet a visszajátszás létrehozott: eid, uid, sablon, jármű, fajta, típus, csapat, játékos, küldetésbeli név, mikor jött létre és távolították el, hol jött létre, és mely komponenseit nem lehetett olvasni |
| `objects` | a küldetés nevesített objektumai: elfoglalható zónák és repülőterek a helyükkel és méretükkel, a repülőterek körvonalai pontokként, kezdőterületek |
| `objectives` | a csata célkitűzései, mindegyik `type` szerint (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (a visszajátszás 1 vagy 2, mindkettőnél üres), `name` (egy elfoglalható zónánál a betűjele, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) a `position`, `radius` / `height` / `size` és `heading` mezőkkel, `source` (`replay` vagy `mission`), és minden más, ami ismert (lásd [Célok](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | mindkét oldal neveivel és járműveivel; az ölések a fegyver angol nevével |
| `weapons` | minden rakéta, rakéta, bomba, torpedó, ledobható tartály és ledobott rakomány: mikor, hol lett kilőve (pozíció, állás, sebesség), melyik egység által (a legközelebbi 300 m-en és 1,5 s-on belül), hány repülési mintája volt, hol látták utoljára, mikor távolították el |
| `explosions`, `flak` | `PlayExplosionVisual` (pozíció, irány, fajta) és `PlayFlakExplosionVisual` (pozíció) |
| `awards` | a felvevő játékos kitüntetései (`TextStreak`: first_blood, sorozatok, kihívás-számlálók) |
| `detections`, `unitStates` | `UnitDetected` egységpárok; egy üzenet (0xF093) egy egység helyzetével, állásával és sebességével, amelynek jelentése nem ismert |
| `authorInstruments` | a felvevő játékos fedélzeti értékei (`ReplayCockpitParams`) műszerszám szerint, másodpercenként legfeljebb egy; a `known` nevezi meg az egyes számokat, amelyeket ez a visszajátszás küldött (név, egység, hogyan ellenőrizték), a `notNamed` a többit |
| `scoreboard` | minden játékos statisztikái, valahányszor változtak (ölések, halálok, asszisztok, pontszám, MI-ölések, tengeri ölések, zónák, sebzés, rakétakitérések, raj), és minden csapat pontszáma és valószínű jegyei időben (lásd [Tükrözési adatok](aircraft.md#reflection-data)) |
| `economy` | a csata ezüstoroszlánjai és kutatási pontjai (lásd [Gazdaság](economy.md)): összesítések, játékosonként, járművenként, a szorzók, a győztes, az ellenőrzések |
| `entityMessages` | az entitásüzenetek (0x20) osztályszám szerint: darabszám, célsablonok, méretek |
| `chat` | minden chat-sor |
| `triggers`, `hints`, `missionProgress` | a küldetésszkript műveletei (RunTriggerAction), tippjei, előrehaladási üzenetei |
| `camera` | a felvevő játékos visszajátszás-kamerájának mezői 0,25 másodpercenként, ahogy küldték (a táblázatban pályaként szerepel) |
| `projectileHitReplays` | a felvevő játékos saját találatai és az ő találatai, fegyverrel és lőszerrel, angol nevükkel |
| `results` | a teljes eredmény-blk, ahogy a játék írta |
| `counts` | sorok, események, életek, fajták, minták, entitások sablonként, fegyverek, beolvasott és nem beolvasott csomagok, minden látott üzenetazonosító és a nem beolvasottak, kihagyott minták |
| `trackBreaks` | minden pályavágás egy olyan lépésnél, amely gyorsabb, mint amire az egység képes: hol, mennyire messze, milyen gyorsan, és mi a valószínű oka |
| `selfCheck` | a [Hogyan olvassa a visszajátszást](how-it-reads.md) oldalon felsorolt ellenőrzések, minden konvertáláskor kiszámolva; a `stepSpeed` fajtánként megadja a pálya egymást követő sorai közötti sebességet, ahogy a megjelenítő összeköti őket (medián, 99. percentilis, legnagyobb, és a lehetetlenül gyors lépések, amelyeknek 0-nak kell lenniük) |

---

A [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentáció](https://holdi601.github.io/3DHeat/)) része. Forrás: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
