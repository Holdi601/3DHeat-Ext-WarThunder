---
title: Dokument tekme
nav_order: 7
lang: "sl"
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# Dokument tekme {#the-match-document}

![Začetek sintetičnega dokumenta tekme in njegovi ključi](../assets/img/match-document.svg)

`<match>.match.json` hrani vse, kar posnetek pove in ni vrstica tabele. Zavihek Tekma v pregledovalniku ga bere.

## Bitka {#the-battle}

| Ključ | Kaj |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | identifikator tekme (kot v imenu datoteke); identifikator zemljevida; datoteka ravni, ki jo uporablja |
| `mission`, `missionKey` | ime misije in njen ključ v besedilnih datotekah igre |
| `battleClass`, `environment`, `weather` | kot jih poda glava |
| `sessionId`, `server` | identifikator seje bitke; strežnik |
| `replayVersion`, `flightLayout` | različica formata posnetka; prebrana postavitev paketov letenja (`2025` ali `2026`) |
| `files` | prebrane datoteke posnetka (ena, ali deli strežniškega posnetka) |
| `started`, `timePlayed`, `replayEnd` | čas začetka (ISO, UTC); odigrane sekunde iz rezultatov; sekunde zadnjega paketa posnetka |
| `author`, `authorUserId` | igralec, ki je snemal, in njegov Gaijin id (posnetki odjemalca) |
| `teams` | ekipe v bitki (`1`, `2`) |
| `result` | `winner`, `status` (`success` ali `fail`, izid avtorja), `authorTeam`, `teams` ([Gospodarstvo](economy.md)) |
| `vehicleNames` | od kod prihajajo imena vozil (vaša namestitev) in njihov jezik |
| `conventions` | enote in predznaki tabele: osi, čas, življenje, pot, živ, zvitek in več |

## Vse ostalo {#everything-else}

| Ključ | Kaj |
|---|---|
| `battle`, `difficulty`, `gameMode` | način bitke: `difficulty` `AB` / `RB` / `SB` (in njeno ime ter bajt glave), `gameMode` `ground` / `air` / `naval`, način misije (`Dom`, `Conq`, `Bttl`, `I2M`, ...) in njeno angleško ime iz vaše namestitve (`Domination`, `Enduring Confrontation`), dovoljene vrste enot (glejte [Način bitke](ground.md#battle-mode)) |
| `settings` | blk misije za glavo: način, okolje, vreme, omejitve rezultata in časa, države, dovoljene vrste enot, veter in `stars` (zemljepisna širina, dolžina, datum, lokalni čas) |
| `sky` | prvi `CustomWeatherParams`: smer sonca in lune, veter, barve neba, zamiki oblakov |
| `players`, `slots` | vrstica rezultatov na igralca (ubijanja, kopenska ubijanja, smrti, pomoči, rezultat, zajemi, odred, klan, država, postava, uid-ji, s katerimi so vozili); reže igralcev posnetka (ime, uporabniški id, ekipa) |
| `units` | vsaka enota, ki jo je posnetek ustvaril: eid, uid, predloga, vozilo, vrsta, tip, ekipa, igralec, ime misije, kdaj je bila ustvarjena in odstranjena, kje je bila ustvarjena, kateri deli se niso dali prebrati |
| `objects` | poimenovani predmeti misije: območja zajema in letališča s položajem in velikostjo, obrisi letališč kot točke, območja pojavov |
| `objectives` | cilji bitke, vsak `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (1 ali 2 iz posnetka, prazno za oba), `name` (območje zajema njegova črka, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) s `position`, `radius` / `height` / `size` in `heading`, `source` (`replay` ali `mission`) in kar je še znano (glejte [Cilji](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | z imeni in vozili obeh strani; ubijanja z angleškim imenom orožja |
| `weapons` | vsaka raketa, izstrelek vodenega orožja, bomba, torpedo, odvržen rezervoar in odvržen tovor: kdaj, kje je bil izpuščen (položaj, drža, hitrost), s katero enoto (najbližja v 300 m in 1,5 s), koliko vzorcev leta, kje je bil nazadnje viden, kdaj je bil odstranjen |
| `explosions`, `flak` | `PlayExplosionVisual` (položaj, smer, vrsta) in `PlayFlakExplosionVisual` (položaj) |
| `awards` | nagrade igralca, ki je snemal (`TextStreak`: first_blood, nizi, števci izzivov) |
| `detections`, `unitStates` | pari `UnitDetected` enot; sporočilo (0xF093) s položajem, držo in hitrostjo enote, katerega pomen ni znan |
| `authorInstruments` | vrednosti kabine igralca, ki je snemal (`ReplayCockpitParams`) po številki instrumenta, največ ena na sekundo; `known` našteva vsako številko, ki jo je ta posnetek poslal (ime, enota, kako je bila preverjena), `notNamed` ostale |
| `scoreboard` | statistika vsakega igralca ob vsaki spremembi (ubijanja, smrti, pomoči, rezultat, ubijanja AI, pomorska ubijanja, območja, poškodbe, izogibanja raketam, odred) ter rezultat in verjetne vstopnice vsake ekipe skozi čas (glejte [Podatki o refleksiji](aircraft.md#reflection-data)) |
| `economy` | Silver Lions in točke raziskav bitke (glejte [Gospodarstvo](economy.md)): skupaj, na igralca, na vozilo, množitelji, zmagovalec, preverjanja |
| `entityMessages` | sporočila entitet (0x20) po številki razreda: število, ciljne predloge, velikosti |
| `chat` | vsaka vrstica klepeta |
| `triggers`, `hints`, `missionProgress` | dejanja skripte misije (RunTriggerAction), njeni namigi, njena sporočila o napredku |
| `camera` | polja nadomestne kamere igralca, ki je snemal, vsakih 0,25 s, kot so bila poslana (tabela jo ima kot pot) |
| `projectileHitReplays` | lastni zadetki igralca, ki je snemal, in zadetki nanj, z orožjem in strelivom ter njunimi angleškimi imeni |
| `results` | ves blk rezultatov, kot ga je zapisala igra |
| `counts` | vrstice, dogodki, življenja, vrste, vzorci, entitete po predlogi, orožja, paketi prebrani in neprebrani, vsak viden identifikator sporočila in tisti, ki niso bili prebrani, izpuščeni vzorci |
| `trackBreaks` | vsak prerez poti za korak, hitrejši, kot lahko enota gre: kje, za kolikor, kako hitro in kaj je najverjetneje |
| `selfCheck` | preverjanja, navedena v [Kako bere posnetek](how-it-reads.md), izračunana ob vsaki pretvorbi; `stepSpeed` daje po vrsti hitrost med zaporednima vrsticama poti, kot jih pregledovalnik povezuje (mediana, 99. percentil, najvišja in koraki, hitrejši od mogočega, ki morajo biti 0) |

---

Del [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Vir: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
