---
title: Dokument meča
nav_order: 7
lang: "hr"
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# Dokument meča {#the-match-document}

![Početak sintetičkog dokumenta meča, i njegovi ključevi](../assets/img/match-document.svg)

`<match>.match.json` drži sve što snimka kaže, a što nije redak tablice. Kartica Meč
preglednika ga čita.

## Bitka {#the-battle}

| Ključ | Što |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | id meča (kao u nazivu datoteke); id karte; datoteka razine koju koristi |
| `mission`, `missionKey` | naziv misije i njezin ključ u tekstualnim datotekama igre |
| `battleClass`, `environment`, `weather` | kako ih daje zaglavlje |
| `sessionId`, `server` | id sesije bitke; poslužitelj |
| `replayVersion`, `flightLayout` | verzija formata snimke; pročitani raspored paketa leta (`2025` ili `2026`) |
| `files` | pročitane datoteke snimke (jedna, ili dijelovi poslužiteljske snimke) |
| `started`, `timePlayed`, `replayEnd` | vrijeme početka (ISO, UTC); odigrane sekunde, iz rezultata; sekunde zadnjeg paketa snimke |
| `author`, `authorUserId` | igrač koji snima i njegov Gaijin id (snimke klijenta) |
| `teams` | timovi u bitci (`1`, `2`) |
| `result` | `winner`, `status` (`success` ili `fail`, ishod autora), `authorTeam`, `teams` ([Ekonomija](economy.md)) |
| `vehicleNames` | odakle dolaze nazivi vozila (tvoja instalacija) i njihov jezik |
| `conventions` | jedinice i predznaci tablice: osi, vrijeme, život, putanja, živ, valjanje, i više |

## Sve ostalo {#everything-else}

| Ključ | Što |
|---|---|
| `battle`, `difficulty`, `gameMode` | način bitke: `difficulty` `AB` / `RB` / `SB` (i njegov naziv, i bajt zaglavlja), `gameMode` `ground` / `air` / `naval`, način misije (`Dom`, `Conq`, `Bttl`, `I2M`, ...) i njegov engleski naziv iz tvoje instalacije (`Domination`, `Enduring Confrontation`), dopuštene vrste jedinica (vidi [Način bitke](ground.md#battle-mode)) |
| `settings` | blk misije iza zaglavlja: način, okruženje, vrijeme, ograničenja bodova i vremena, države, dopuštene vrste jedinica, vjetar, i `stars` (geografska širina, dužina, datum, lokalno vrijeme) |
| `sky` | prvi `CustomWeatherParams`: smjer sunca i mjeseca, vjetar, boje neba, pomaci oblaka |
| `players`, `slots` | redak rezultata po igraču (ubojstva, ubojstva na kopnu, smrti, asistencije, bodovi, zauzimanja, odred, klan, država, postava, uid-ovi kojima je upravljao); utori igrača snimke (ime, user id, tim) |
| `units` | svaka jedinica entiteta koju je snimka stvorila: eid, uid, predložak, vozilo, vrsta, tip, tim, igrač, naziv u misiji, kad je stvorena i uklonjena, gdje je stvorena, koje komponente nisu mogle biti pročitane |
| `objects` | imenovani objekti misije: zone zauzimanja i aerodromi s položajem i veličinom, obrisi aerodroma kao točke, područja pojavljivanja |
| `objectives` | ciljevi bitke, svaki `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (1 ili 2 iz snimke, prazno za oba), `name` (zona zauzimanja svoje slovo, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) s `position`, `radius` / `height` / `size` i `heading`, `source` (`replay` ili `mission`) i što je još poznato (vidi [Ciljevi](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | s imenima i vozilima obiju strana; ubojstva s engleskim nazivom oružja |
| `weapons` | svaka raketa, projektil, bomba, torpedo, odbačeni spremnik i odbačeni teret: kad, gdje je ispušten (položaj, stav, brzina), od koje jedinice (najbliže unutar 300 m i 1,5 s), koliko uzoraka leta, gdje je zadnji put viđen, kad je uklonjen |
| `explosions`, `flak` | `PlayExplosionVisual` (položaj, smjer, vrsta) i `PlayFlakExplosionVisual` (položaj) |
| `awards` | nagrade igrača koji snima (`TextStreak`: first_blood, nizovi, brojači izazova) |
| `detections`, `unitStates` | parovi `UnitDetected` jedinica; poruka (0xF093) s položajem, stavom i brzinom jedinice čije značenje nije poznato |
| `authorInstruments` | vrijednosti kabine igrača koji snima (`ReplayCockpitParams`) po broju instrumenta, najviše jedna po sekundi; `known` imenuje svaki broj koji je ova snimka poslala (naziv, jedinica, kako je provjeren), `notNamed` ostale |
| `scoreboard` | statistika svakog igrača svaki put kad se promijenila (ubojstva, smrti, asistencije, bodovi, ubojstva AI-ja, pomorska ubojstva, zone, šteta, izbjegnute rakete, odred), i bodovi svakog tima i vjerojatni tiketi kroz vrijeme (vidi [Podaci o refleksiji](aircraft.md#reflection-data)) |
| `economy` | Silver Lions i bodovi za istraživanje bitke (vidi [Ekonomija](economy.md)): zbrojevi, po igraču, po vozilu, množitelji, pobjednik, provjere |
| `entityMessages` | poruke entiteta (0x20) po broju klase: broj, ciljni predlošci, veličine |
| `chat` | svaki red razgovora |
| `triggers`, `hints`, `missionProgress` | radnje skripte misije (RunTriggerAction), njezini savjeti, njezine poruke napretka |
| `camera` | polja replay kamere igrača koji snima svakih 0,25 s kako su poslana (tablica je ima kao putanju) |
| `projectileHitReplays` | vlastiti pogoci igrača koji snima i pogoci koje prima, s oružjem i streljivom te njihovim engleskim nazivima |
| `results` | cijeli blk rezultata kako ga je igra zapisala |
| `counts` | redci, događaji, životi, vrste, uzorci, entiteti po predlošku, oružja, paketi pročitani i nepročitani, svaki id poruke viđen i oni nepročitani, odbačeni uzorci |
| `trackBreaks` | svaki rez putanje zbog koraka bržeg nego što jedinica može: gdje, koliko daleko, koliko brzo, i što je najvjerojatnije |
| `selfCheck` | provjere navedene u [Kako se snimka čita](how-it-reads.md), izračunate pri svakom pretvaranju; `stepSpeed` daje po vrsti brzinu između uzastopnih redaka putanje kako ih preglednik spaja (medijan, 99. percentil, najveća, i koraci brži nego što je moguće, što mora biti 0) |

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
