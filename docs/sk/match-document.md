---
title: "Dokument zápasu"
nav_order: 7
lang: sk
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# Dokument zápasu {#the-match-document}

![Začiatok syntetického dokumentu zápasu a jeho kľúče](../assets/img/match-document.svg)

`<match>.match.json` drží všetko, čo replay hovorí a nie je riadkom tabuľky. Karta Zápas v prehliadači ho číta.

## Bitka {#the-battle}

| Kľúč | Čo |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | id zápasu (ako v názve súboru); id mapy; súbor levelu, ktorý používa |
| `mission`, `missionKey` | názov misie a jej kľúč v textových súboroch hry |
| `battleClass`, `environment`, `weather` | tak, ako ich dáva hlavička |
| `sessionId`, `server` | id relácie bitky; server |
| `replayVersion`, `flightLayout` | verzia formátu replaye; prečítané rozloženie letových paketov (`2025` alebo `2026`) |
| `files` | čítané súbory replaye (jeden, alebo časti serverového replaye) |
| `started`, `timePlayed`, `replayEnd` | čas začiatku (ISO, UTC); odohrané sekundy, z výsledkov; sekundy posledného paketu replaye |
| `author`, `authorUserId` | hráč, ktorý replay nahral, a jeho Gaijin id (klientské replaye) |
| `teams` | tímy v bitke (`1`, `2`) |
| `result` | `winner`, `status` (`success` alebo `fail`, výsledok autora), `authorTeam`, `teams` ([Ekonomika](economy.md)) |
| `vehicleNames` | odkiaľ pochádzajú názvy vozidiel (vaša inštalácia) a ich jazyk |
| `conventions` | jednotky a znamienka tabuľky: osi, čas, život, stopa, alive, náklon a ďalšie |

## Všetko ostatné {#everything-else}

| Kľúč | Čo |
|---|---|
| `battle`, `difficulty`, `gameMode` | režim bitky: `difficulty` `AB` / `RB` / `SB` (a jeho názov, a bajt hlavičky), `gameMode` `ground` / `air` / `naval`, režim misie (`Dom`, `Conq`, `Bttl`, `I2M`, ...) a jeho anglický názov z vašej inštalácie (`Domination`, `Enduring Confrontation`), povolené typy jednotiek (pozri [Režim bitky](ground.md#battle-mode)) |
| `settings` | blk misie za hlavičkou: režim, prostredie, počasie, limity skóre a času, krajiny, povolené typy jednotiek, vietor a `stars` (zemepisná šírka, dĺžka, dátum, miestny čas) |
| `sky` | prvý `CustomWeatherParams`: smer slnka a mesiaca, vietor, farby oblohy, posuny oblakov |
| `players`, `slots` | riadok výsledkov na hráča (zabitia, pozemné zabitia, smrti, asistencie, skóre, dobytia, eskadra, klan, krajina, zostava, uid, ktoré riadili); sloty hráčov replaye (meno, user id, tím) |
| `units` | každá entita jednotky, ktorú replay vytvoril: eid, uid, šablóna, vozidlo, druh, typ, tím, hráč, názov v misii, kedy bola vytvorená a odstránená, kde bola vytvorená, ktoré komponenty sa nedali prečítať |
| `objects` | pomenované objekty misie: zóny dobytia a letiská s ich polohou a veľkosťou, obrysy letísk ako body, oblasti spawnu |
| `objectives` | ciele bitky, každý `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (1 alebo 2 z replaye, prázdne pre oboch), `name` (zóna dobytia svoje písmeno, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) s `position`, `radius` / `height` / `size` a `heading`, `source` (`replay` alebo `mission`) a čo ešte je známe (pozri [Ciele](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | s menami a vozidlami oboch strán; zabitia s anglickým názvom zbrane |
| `weapons` | každá raketa, strela, bomba, torpédo, odhadzovacia nádrž a odhodený náklad: kedy, kde vypustené (poloha, postoj, rýchlosť), ktorou jednotkou (najbližšia do 300 m a 1,5 s), koľko vzoriek letu, kde naposledy videné, kedy odstránené |
| `explosions`, `flak` | `PlayExplosionVisual` (poloha, smer, druh) a `PlayFlakExplosionVisual` (poloha) |
| `awards` | ocenenia hráča, ktorý replay nahral (`TextStreak`: first_blood, série, počítadlá výziev) |
| `detections`, `unitStates` | dvojice `UnitDetected` jednotiek; správa (0xF093) s polohou, postojom a rýchlosťou jednotky, ktorej význam nie je známy |
| `authorInstruments` | hodnoty kokpitu hráča, ktorý replay nahral (`ReplayCockpitParams`), podľa čísla prístroja, najviac jedna za sekundu; `known` pomenúva každé číslo, ktoré tento replay poslal (názov, jednotka, ako bolo overené), `notNamed` zvyšok |
| `scoreboard` | štatistiky každého hráča vždy, keď sa zmenili (zabitia, smrti, asistencie, skóre, zabitia AI, námorné zabitia, zóny, poškodenie, úniky pred raketami, eskadra), a skóre každého tímu a pravdepodobné tikety v čase (pozri [Údaje odrazu](aircraft.md#reflection-data)) |
| `economy` | Silver Lions a výskumné body bitky (pozri [Ekonomika](economy.md)): súčty, na hráča, na vozidlo, násobitele, víťaz, kontroly |
| `entityMessages` | entitné správy (0x20) podľa čísla triedy: počet, cieľové šablóny, veľkosti |
| `chat` | každý riadok chatu |
| `triggers`, `hints`, `missionProgress` | akcie skriptu misie (RunTriggerAction), jej nápovedy, jej správy o priebehu |
| `camera` | polia kamery replaye hráča, ktorý replay nahral, každých 0,25 s tak, ako boli poslané (tabuľka ich má ako stopu) |
| `projectileHitReplays` | vlastné zásahy hráča, ktorý replay nahral, a jeho zásahy, so zbraňou a muníciou a ich anglickými názvami |
| `results` | celý blk výsledkov tak, ako ho hra zapísala |
| `counts` | riadky, udalosti, životy, druhy, vzorky, entity podľa šablóny, zbrane, pakety prečítané a neprečítané, každé stretnuté id správy a tie neprečítané, zahodené vzorky |
| `trackBreaks` | každý rez stopy pre krok rýchlejší, než môže jednotka ísť: kde, o koľko, ako rýchlo a čo je najpravdepodobnejšie |
| `selfCheck` | kontroly uvedené v [Ako sa replay číta](how-it-reads.md), počítané pri každej konverzii; `stepSpeed` dáva podľa druhu rýchlosť medzi po sebe idúcimi riadkami stopy tak, ako ich prehliadač spája (medián, 99. percentil, najvyššia, a kroky rýchlejšie, než je možné, ktoré musia byť 0) |

---

Súčasť [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentácia](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
