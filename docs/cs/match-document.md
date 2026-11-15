---
title: "Dokument zápasu"
nav_order: 7
lang: "cs"
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# Dokument zápasu {#the-match-document}

![Začátek syntetického dokumentu zápasu a jeho klíče](../assets/img/match-document.svg)

`<match>.match.json` drží vše, co replay říká a co není řádkem tabulky. Čte ho záložka Zápas prohlížeče.

## Bitva {#the-battle}

| Klíč | Co |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | id zápasu (jako v názvu souboru); id mapy; soubor úrovně, který používá |
| `mission`, `missionKey` | název mise a její klíč v textových souborech hry |
| `battleClass`, `environment`, `weather` | tak, jak je uvádí hlavička |
| `sessionId`, `server` | id relace bitvy; server |
| `replayVersion`, `flightLayout` | verze formátu replaye; přečtené rozložení letových paketů (`2025` nebo `2026`) |
| `files` | přečtené soubory replaye (jeden, nebo části serverového replaye) |
| `started`, `timePlayed`, `replayEnd` | čas začátku (ISO, UTC); odehrané vteřiny z výsledků; vteřiny posledního paketu replaye |
| `author`, `authorUserId` | hráč, který nahrával, a jeho id Gaijin (replaye klienta) |
| `teams` | týmy v bitvě (`1`, `2`) |
| `result` | `winner`, `status` (`success` nebo `fail`, výsledek autora), `authorTeam`, `teams` ([Ekonomika](economy.md)) |
| `vehicleNames` | odkud pocházejí názvy vozidel (vaše instalace) a jejich jazyk |
| `conventions` | jednotky a znaménka tabulky: osy, čas, život, trať, živý, náklon a další |

## Vše ostatní {#everything-else}

| Klíč | Co |
|---|---|
| `battle`, `difficulty`, `gameMode` | režim bitvy: `difficulty` `AB` / `RB` / `SB` (a její název, a bajt hlavičky), `gameMode` `ground` / `air` / `naval`, režim mise (`Dom`, `Conq`, `Bttl`, `I2M`, ...) a jeho anglický název z vaší instalace (`Domination`, `Enduring Confrontation`), povolené typy jednotek (viz [Režim bitvy](ground.md#battle-mode)) |
| `settings` | blk mise za hlavičkou: režim, prostředí, počasí, limity skóre a času, země, povolené typy jednotek, vítr a `stars` (zeměpisná šířka, délka, datum, místní čas) |
| `sky` | první `CustomWeatherParams`: směr slunce a měsíce, vítr, barvy oblohy, posuny mraků |
| `players`, `slots` | řádek výsledků na hráče (zabití, pozemní zabití, smrti, asistence, skóre, dobytí, squad, klan, země, sestava, uid, které řídili); sloty hráčů v replayi (jméno, user id, tým) |
| `units` | každá entita jednotky, kterou replay vytvořil: eid, uid, šablona, vozidlo, druh, typ, tým, hráč, název v misi, kdy byla vytvořena a odstraněna, kde byla vytvořena, které komponenty se nepodařilo přečíst |
| `objects` | pojmenované objekty mise: zóny dobytí a letiště s pozicí a velikostí, obrysy letišť jako body, oblasti spawnu |
| `objectives` | cíle bitvy, každý `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (1 nebo 2 z replaye, prázdné pro oba), `name` (zóna dobytí své písmeno, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) s `position`, `radius` / `height` / `size` a `heading`, `source` (`replay` nebo `mission`) a co dalšího je známo (viz [Cíle](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | se jmény a vozidly obou stran; zabití s anglickým názvem zbraně |
| `weapons` | každá raketa, řízená střela, bomba, torpédo, odhozená přídavná nádrž a shozený náklad: kdy, kde byl vypuštěn (pozice, postoj, rychlost), kterou jednotkou (nejbližší do 300 m a 1,5 s), kolik letových vzorků, kde byl naposledy spatřen, kdy byl odstraněn |
| `explosions`, `flak` | `PlayExplosionVisual` (pozice, směr, druh) a `PlayFlakExplosionVisual` (pozice) |
| `awards` | ocenění hráče, který nahrával (`TextStreak`: first_blood, série, počítadla výzev) |
| `detections`, `unitStates` | dvojice `UnitDetected` jednotek; zpráva (0xF093) s pozicí, postojem a rychlostí jednotky, jejíž význam není znám |
| `authorInstruments` | hodnoty kokpitu hráče, který nahrával (`ReplayCockpitParams`) podle čísla přístroje, nejvýš jedna za vteřinu; `known` pojmenovává každé číslo, které tento replay poslal (název, jednotka, jak bylo ověřeno), `notNamed` zbytek |
| `scoreboard` | statistiky každého hráče pokaždé, když se změnily (zabití, smrti, asistence, skóre, zabití AI, námořní zabití, zóny, poškození, uniknuté střely, squad), a skóre každého týmu a pravděpodobné body (tickets) v čase (viz [Data odrazu](aircraft.md#reflection-data)) |
| `economy` | Stříbrné lvy a výzkumné body bitvy (viz [Ekonomika](economy.md)): součty, na hráče, na vozidlo, násobitele, vítěz, kontroly |
| `entityMessages` | zprávy entit (0x20) podle čísla třídy: počet, cílové šablony, velikosti |
| `chat` | každý řádek chatu |
| `triggers`, `hints`, `missionProgress` | akce skriptu mise (RunTriggerAction), její nápovědy, její zprávy o postupu |
| `camera` | pole kamery replaye hráče, který nahrával, každých 0,25 s tak, jak byla poslána (tabulka ji má jako trať) |
| `projectileHitReplays` | vlastní zásahy hráče, který nahrával, a zásahy na něj, se zbraní a municí a jejich anglickými názvy |
| `results` | celý blk výsledků, tak, jak ho hra zapsala |
| `counts` | řádky, události, životy, druhy, vzorky, entity podle šablony, zbraně, pakety přečtené a nepřečtené, každé id zprávy, které se vidělo, a ty nepřečtené, zahozené vzorky |
| `trackBreaks` | každé přerušení tratě kvůli kroku rychlejšímu, než jednotka může jít: kde, jak daleko, jak rychle, a co je nejpravděpodobnější |
| `selfCheck` | kontroly uvedené v [Jak se replay čte](how-it-reads.md), počítané při každém převodu; `stepSpeed` dává podle druhu rychlost mezi po sobě jdoucími řádky tratě tak, jak je prohlížeč spojuje (medián, 99. percentil, nejvyšší, a kroky rychlejší, než je možné, což musí být 0) |

---

Součást [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentace](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
