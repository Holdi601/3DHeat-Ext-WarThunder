---
title: "Leikjaskjalið"
nav_order: 7
lang: is
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# Leikjaskjalið {#the-match-document}

![Upphaf tilbúins leikjaskjals og lyklar þess](../assets/img/match-document.svg)

`<match>.match.json` geymir allt sem upptakan segir og er ekki röð í töflunni.
Flipinn Leikur í skoðaranum les það.

## Bardaginn {#the-battle}

| Lykill | Hvað |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | auðkenni leiksins (eins og í skráarnafninu); auðkenni kortsins; borðsskráin sem það notar |
| `mission`, `missionKey` | nafn verkefnisins og lykill þess í textaskrám leiksins |
| `battleClass`, `environment`, `weather` | eins og hausinn gefur þau |
| `sessionId`, `server` | lotuauðkenni bardagans; þjónninn |
| `replayVersion`, `flightLayout` | útgáfa upptökusniðsins; útlit flugpakkans sem var lesið (`2025` eða `2026`) |
| `files` | upptökuskrárnar sem voru lesnar (ein, eða hlutar þjónsupptöku) |
| `started`, `timePlayed`, `replayEnd` | upphafstími (ISO, UTC); sekúndur spilaðar, úr niðurstöðunum; sekúndur síðasta pakka upptökunnar |
| `author`, `authorUserId` | spilarinn sem tók upp og Gaijin-auðkenni hans (biðlaraupptökur) |
| `teams` | liðin í bardaganum (`1`, `2`) |
| `result` | `winner`, `status` (`success` eða `fail`, útkoma upptökumannsins), `authorTeam`, `teams` ([Hagkerfi](economy.md)) |
| `vehicleNames` | hvaðan nöfn farartækjanna komu (þín uppsetning) og tungumál þeirra |
| `conventions` | einingar og formerki töflunnar: ásar, tími, líf (life), ferill (track), alive, roll, og fleira |

## Allt annað {#everything-else}


| Lykill | Hvað |
|---|---|
| `battle`, `difficulty`, `gameMode` | bardagahamurinn: `difficulty` `AB` / `RB` / `SB` (og nafn þess, og hausbætið), `gameMode` `ground` / `air` / `naval`, hamur verkefnisins (`Dom`, `Conq`, `Bttl`, `I2M`, ...) og enska nafnið hans úr þinni uppsetningu (`Domination`, `Enduring Confrontation`), leyfðar einingategundir (sjá [Bardagahamur](ground.md#battle-mode)) |
| `settings` | verkefnis-blk eftir hausinn: hamur, umhverfi, veður, stiga- og tímamörk, lönd, leyfðar einingategundir, vindur, og `stars` (breiddargráða, lengdargráða, dagsetning, staðartími) |
| `sky` | fyrstu `CustomWeatherParams`: stefna sólar og tungls, vindur, litir himins, skýjafærslur |
| `players`, `slots` | lína niðurstaðnanna fyrir hvern spilara (dráp, landdráp, dauðsföll, aðstoðir, stig, handtökur, flokkur (squad), ætt (clan), land, uppröðun, uid-in sem þeir óku); spilararaufar upptökunnar (nafn, notandaauðkenni, lið) |
| `units` | hver einingarhlutur sem upptakan bjó til: eid, uid, sniðmát, farartæki, tegund, gerð, lið, spilari, verkefnisnafn, hvenær hann var búinn til og fjarlægður, hvar hann var búinn til, hvaða íhluti var ekki hægt að lesa |
| `objects` | nefndir hlutir verkefnisins: handtökusvæði og flugvellir með stöðu og stærð, útlínur flugvalla sem punktar, endurkomusvæði |
| `objectives` | markmið bardagans, hvert með `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (1 eða 2 upptökunnar, tómt fyrir bæði), `name` (handtökusvæði bókstaf sinn, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) með `position`, `radius` / `height` / `size` og `heading`, `source` (`replay` eða `mission`) og hvað annað er vitað (sjá [Markmið](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | með nöfnum og farartækjum beggja aðila; dráp með enska nafni vopnsins |
| `weapons` | hver eldflaug, flugskeyti, sprengja, tundurskeyti, aukageymir og varpað farmur: hvenær, hvar sleppt (staða, stefna, hraði), af hvaða einingu (þeirri næstu innan 300 m og 1,5 s), hversu mörg flugsýni, hvar sást síðast, hvenær fjarlægt |
| `explosions`, `flak` | `PlayExplosionVisual` (staða, stefna, tegund) og `PlayFlakExplosionVisual` (staða) |
| `awards` | verðlaun upptökumannsins (`TextStreak`: first_blood, runur, áskorunarteljarar) |
| `detections`, `unitStates` | `UnitDetected` pör eininga; skilaboð (0xF093) með stöðu, stefnu og hraða einingar sem merking er ekki þekkt |
| `authorInstruments` | gildi stjórnklefa upptökumannsins (`ReplayCockpitParams`) eftir númeri mælis, í mesta lagi eitt á sekúndu; `known` nefnir hvert númer sem þessi upptaka sendi (nafn, eining, hvernig það var athugað), `notNamed` hin |
| `scoreboard` | tölfræði hvers spilara í hvert sinn sem hún breyttist (dráp, dauðsföll, aðstoðir, stig, ai kills, naval kills, svæði, skaði, flugskeytum forðað, squad), og stig hvers liðs og líklegir miðar (tickets) yfir tíma (sjá [Speglunargögn](aircraft.md#reflection-data)) |
| `economy` | Silver Lions og rannsóknarstig bardagans (sjá [Hagkerfi](economy.md)): heildir, eftir spilara, eftir farartæki, margfaldarar, sigurvegarinn, athuganirnar |
| `entityMessages` | einingarskilaboðin (0x20) eftir flokksnúmeri: fjöldi, markmiðssniðmát, stærðir |
| `chat` | hver spjalllína |
| `triggers`, `hints`, `missionProgress` | aðgerðir verkefnisskriftunnar (RunTriggerAction), ábendingar hennar, framvinduskilaboð hennar |
| `camera` | reitir upptökumyndavélar upptökumannsins á 0,25 s fresti eins og þeir voru sendir (taflan hefur þá sem feril) |
| `projectileHitReplays` | eigin högg upptökumannsins og þegar hann var sleginn, með vopni og skotfærum og ensku nöfnum þeirra |
| `results` | allt niðurstöðu-blk eins og leikurinn skrifaði það |
| `counts` | raðir, atburðir, líf, tegundir, sýni, einingar eftir sniðmáti, vopn, pakkar lesnir og ólesnir, hvert skilaboðaauðkenni sem sást og þau sem ekki voru lesin, sýni felld niður |
| `trackBreaks` | hver skurður ferils vegna skrefs hraðara en eining kemst: hvar, hversu langt, hversu hratt, og hvað það er líklegast |
| `selfCheck` | athuganirnar sem taldar eru upp í [Hvernig upptaka er lesin](how-it-reads.md), reiknaðar við hverja breytingu; `stepSpeed` gefur fyrir hverja tegund hraðann milli samliggjandi raða ferils eins og skoðarinn tengir þær (miðgildi, 99. hundraðshluti, hæsta gildi, og skref hraðari en mögulegt er, sem verða að vera 0) |

---

Hluti af [3DHeat](https://github.com/Holdi601/3DHeat) ([skjölun](https://holdi601.github.io/3DHeat/)). Frumkóði: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
