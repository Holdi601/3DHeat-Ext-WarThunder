---
title: "Dokument meča"
nav_order: 7
lang: bs
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# Dokument meča {#the-match-document}

![Početak sintetičkog dokumenta meča i njegovi ključevi](../assets/img/match-document.svg)

`<match>.match.json` sadrži sve što replay kaže a nije red
tabele. Kartica Meč preglednika ga čita.

## Bitka {#the-battle}

| Ključ | Šta |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | id meča (kao u imenu datoteke); id mape; datoteka nivoa koju koristi |
| `mission`, `missionKey` | ime misije i njen ključ u tekstualnim datotekama igre |
| `battleClass`, `environment`, `weather` | kako ih daje zaglavlje |
| `sessionId`, `server` | id sesije bitke; server |
| `replayVersion`, `flightLayout` | verzija formata replaya; pročitani raspored paketa leta (`2025` ili `2026`) |
| `files` | pročitane datoteke replaya (jedna, ili dijelovi serverskog replaya) |
| `started`, `timePlayed`, `replayEnd` | vrijeme početka (ISO, UTC); odigrane sekunde, iz rezultata; sekunde zadnjeg paketa replaya |
| `author`, `authorUserId` | igrač koji snima i njegov Gaijin id (klijentski replayevi) |
| `teams` | timovi u bitci (`1`, `2`) |
| `result` | `winner`, `status` (`success` ili `fail`, ishod autora), `authorTeam`, `teams` ([Ekonomija](economy.md)) |
| `vehicleNames` | odakle su imena vozila došla (vaša instalacija) i njihov jezik |
| `conventions` | jedinice i predznaci tabele: osi, vrijeme, life, track, alive, roll i još mnogo toga |

## Sve ostalo {#everything-else}


| Ključ | Šta |
|---|---|
| `battle`, `difficulty`, `gameMode` | način bitke: `difficulty` `AB` / `RB` / `SB` (i njegovo ime, i bajt zaglavlja), `gameMode` `ground` / `air` / `naval`, način misije (`Dom`, `Conq`, `Bttl`, `I2M`, ...) i njegovo englesko ime iz vaše instalacije (`Domination`, `Enduring Confrontation`), dozvoljeni tipovi jedinica (vidi [Način bitke](ground.md#battle-mode)) |
| `settings` | blk misije poslije zaglavlja: način, okruženje, vrijeme, ograničenja rezultata i vremena, države, dozvoljeni tipovi jedinica, vjetar i `stars` (geografska širina, dužina, datum, lokalno vrijeme) |
| `sky` | prvi `CustomWeatherParams`: smjer sunca i mjeseca, vjetar, boje neba, pomaci oblaka |
| `players`, `slots` | red rezultata po igraču (ubistva, kopnena ubistva, smrti, asistencije, bodovi, zauzimanja, odred, klan, država, sastav, uid-ovi koje su vozili); igrački slotovi replaya (ime, id korisnika, tim) |
| `units` | svaki entitet jedinice koji je replay napravio: eid, uid, šablon, vozilo, kind, type, tim, igrač, ime u misiji, kada je napravljen i uklonjen, gdje je napravljen, koje komponente nisu mogle biti pročitane |
| `objects` | imenovani objekti misije: zone zauzimanja i aerodromi s pozicijom i veličinom, obrisi aerodroma kao tačke, zone pojavljivanja |
| `objectives` | ciljevi bitke, svaki sa `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (1 ili 2 iz replaya, prazno za oba), `name` (zona zauzimanja njeno slovo, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) s `position`, `radius` / `height` / `size` i `heading`, `source` (`replay` ili `mission`) i ostalo što je poznato (vidi [Ciljevi](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | s imenima i vozilima obje strane; ubistva s engleskim imenom oružja |
| `weapons` | svaka raketa, projektil, bomba, torpedo, odbacivi rezervoar i odbačeni teret: kada, gdje je ispušten (pozicija, stav, brzina), od koje jedinice (najbliža unutar 300 m i 1,5 s), koliko uzoraka leta, gdje je zadnji put viđen, kada je uklonjen |
| `explosions`, `flak` | `PlayExplosionVisual` (pozicija, smjer, vrsta) i `PlayFlakExplosionVisual` (pozicija) |
| `awards` | nagrade igrača koji snima (`TextStreak`: first_blood, nizovi, brojači izazova) |
| `detections`, `unitStates` | parovi jedinica `UnitDetected`; poruka (0xF093) s pozicijom, stavom i brzinom jedinice čije značenje nije poznato |
| `authorInstruments` | vrijednosti kokpita igrača koji snima (`ReplayCockpitParams`) po broju instrumenta, najviše jedna u sekundi; `known` imenuje svaki broj koji je ovaj replay poslao (ime, jedinica, kako je provjereno), `notNamed` ostale |
| `scoreboard` | statistika svakog igrača svaki put kad se promijenila (ubistva, smrti, asistencije, bodovi, AI ubistva, pomorska ubistva, zone, šteta, izbjegnute rakete, odred), te rezultat svakog tima i vjerovatni tiketi kroz vrijeme (vidi [Podaci refleksije](aircraft.md#reflection-data)) |
| `economy` | Silver Lions i bodovi istraživanja bitke (vidi [Ekonomija](economy.md)): ukupno, po igraču, po vozilu, množioci, pobjednik, provjere |
| `entityMessages` | poruke entiteta (0x20) po broju klase: broj, ciljni šabloni, veličine |
| `chat` | svaki red četa |
| `triggers`, `hints`, `missionProgress` | akcije skripte misije (RunTriggerAction), njene napomene, njene poruke o napretku |
| `camera` | polja replay kamere igrača koji snima svakih 0,25 s kako su poslana (tabela je ima kao stazu) |
| `projectileHitReplays` | vlastiti pogoci igrača koji snima i pogoci po njemu, s oružjem i municijom i njihovim engleskim imenima |
| `results` | cijeli blk rezultata onako kako ga je igra napisala |
| `counts` | redovi, događaji, životi, vrste, uzorci, entiteti po šablonu, oružja, pročitani i nepročitani paketi, svaki viđeni id poruke i oni koji nisu pročitani, odbačeni uzorci |
| `trackBreaks` | svaki rez staze zbog koraka bržeg nego što jedinica može ići: gdje, koliko daleko, koliko brzo i šta je to najvjerovatnije |
| `selfCheck` | provjere navedene u [Kako čita replay](how-it-reads.md), izračunate pri svakom pretvaranju; `stepSpeed` daje po vrsti brzinu između uzastopnih redova staze onako kako ih preglednik spaja (medijan, 99. percentil, najviša i koraci brži nego što je moguće, koji moraju biti 0) |

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
