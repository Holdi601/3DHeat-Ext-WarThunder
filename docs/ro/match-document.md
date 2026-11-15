---
title: Documentul meciului
nav_order: 7
lang: ro
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# Documentul meciului {#the-match-document}

![Începutul unui document de meci sintetic și cheile sale](../assets/img/match-document.svg)

`<match>.match.json` ține tot ce spune replay-ul și care nu este un rând al tabelului. Fila Meci a
vizualizatorului îl citește.

## Bătălia {#the-battle}

| Cheie | Ce este |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | id-ul meciului (ca în numele fișierului); id-ul hărții; fișierul de nivel pe care îl folosește |
| `mission`, `missionKey` | numele misiunii și cheia sa din fișierele de text ale jocului |
| `battleClass`, `environment`, `weather` | așa cum le dă antetul |
| `sessionId`, `server` | id-ul sesiunii bătăliei; serverul |
| `replayVersion`, `flightLayout` | versiunea formatului de replay; aranjamentul pachetului de zbor citit (`2025` sau `2026`) |
| `files` | fișierele de replay citite (unul, sau părțile unui replay de server) |
| `started`, `timePlayed`, `replayEnd` | ora de start (ISO, UTC); secundele jucate, din rezultate; secundele ultimului pachet al replay-ului |
| `author`, `authorUserId` | jucătorul care înregistrează și id-ul său Gaijin (replay-uri de client) |
| `teams` | echipele din bătălie (`1`, `2`) |
| `result` | `winner`, `status` (`success` sau `fail`, rezultatul autorului), `authorTeam`, `teams` ([Economie](economy.md)) |
| `vehicleNames` | de unde vin numele vehiculelor (instalarea dumneavoastră) și limba lor |
| `conventions` | unitățile și semnele tabelului: axele, timpul, viața, traseul, alive, rularea și altele |

## Restul {#everything-else}

| Cheie | Ce este |
|---|---|
| `battle`, `difficulty`, `gameMode` | modul bătăliei: `difficulty` `AB` / `RB` / `SB` (și numele său, și octetul din antet), `gameMode` `ground` / `air` / `naval`, modul misiunii (`Dom`, `Conq`, `Bttl`, `I2M`, ...) și numele său în engleză din instalarea dumneavoastră (`Domination`, `Enduring Confrontation`), tipurile de unități permise (vedeți [Modul de bătălie](ground.md#battle-mode)) |
| `settings` | blk-ul misiunii de după antet: mod, mediu, vreme, limitele de scor și de timp, țările, tipurile de unități permise, vântul și `stars` (latitudine, longitudine, data, ora locală) |
| `sky` | primul `CustomWeatherParams`: direcția soarelui și a lunii, vântul, culorile cerului, decalajele norilor |
| `players`, `slots` | linia din rezultate pentru fiecare jucător (uciderile, uciderile la sol, morțile, asistențele, scorul, capturile, escadrila, clanul, țara, componența, uid-urile pe care le-au condus); sloturile de jucător ale replay-ului (nume, id utilizator, echipă) |
| `units` | fiecare entitate de unitate creată de replay: eid, uid, șablon, vehicul, fel, tip, echipă, jucător, numele din misiune, când a fost creată și scoasă, unde a fost creată, ce componente n-au putut fi citite |
| `objects` | obiectele numite ale misiunii: zonele de capturare și aerodromurile cu poziția și dimensiunea lor, contururile aerodromurilor ca puncte, zonele de apariție |
| `objectives` | obiectivele bătăliei, fiecare `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (1 sau 2 din replay, gol pentru ambele), `name` (o zonă de capturare litera sa, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) cu `position`, `radius` / `height` / `size` și `heading`, `source` (`replay` sau `mission`) și ce altceva se știe (vedeți [Obiective](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | cu numele și vehiculele ambelor tabere; uciderile cu numele în engleză al armei |
| `weapons` | fiecare rachetă, rachetă ghidată, bombă, torpilă, rezervor de pe aripi și încărcătură aruncată: când, de unde a fost eliberată (poziția, atitudinea, viteza), de către ce unitate (cea mai apropiată în 300 m și 1,5 s), câte eșantioane de zbor, unde a fost văzută ultima oară, când a fost scoasă |
| `explosions`, `flak` | `PlayExplosionVisual` (poziția, direcția, felul) și `PlayFlakExplosionVisual` (poziția) |
| `awards` | premiile jucătorului care înregistrează (`TextStreak`: first_blood, serii, contoare de provocări) |
| `detections`, `unitStates` | perechile `UnitDetected` de unități; un mesaj (0xF093) cu poziția, atitudinea și viteza unei unități al cărui sens nu este cunoscut |
| `authorInstruments` | valorile cabinei jucătorului care înregistrează (`ReplayCockpitParams`) după numărul indicatorului, cel mult una pe secundă; `known` numește fiecare număr pe care l-a trimis acest replay (nume, unitate, cum a fost verificat), `notNamed` restul |
| `scoreboard` | statisticile fiecărui jucător de fiecare dată când s-au schimbat (uciderile, morțile, asistențele, scorul, uciderile de IA, uciderile navale, zonele, daunele, evitările de rachete, escadrila), și scorul fiecărei echipe și biletele probabile în timp (vedeți [Date de reflecție](aircraft.md#reflection-data)) |
| `economy` | Silver Lions și punctele de cercetare ale bătăliei (vedeți [Economie](economy.md)): totaluri, pe jucător, pe vehicul, multiplicatorii, câștigătorul, verificările |
| `entityMessages` | mesajele de entitate (0x20) după numărul clasei: numărul, șabloanele țintă, dimensiunile |
| `chat` | fiecare linie de chat |
| `triggers`, `hints`, `missionProgress` | acțiunile scriptului misiunii (RunTriggerAction), indiciile sale, mesajele sale de progres |
| `camera` | câmpurile camerei de replay a jucătorului care înregistrează, la fiecare 0,25 s, așa cum sunt trimise (tabelul le are ca traseu) |
| `projectileHitReplays` | loviturile proprii ale jucătorului care înregistrează și loviturile primite, cu arma și muniția și numele lor în engleză |
| `results` | tot blk-ul rezultatelor, așa cum l-a scris jocul |
| `counts` | rânduri, evenimente, vieți, feluri, eșantioane, entități după șablon, arme, pachete citite și necitite, fiecare id de mesaj văzut și cele necitite, eșantioanele lăsate |
| `trackBreaks` | fiecare tăiere a unui traseu pentru un pas mai rapid decât poate merge unitatea: unde, cât de departe, cât de repede și ce este cel mai probabil |
| `selfCheck` | verificările listate în [Cum citește un replay](how-it-reads.md), calculate la fiecare conversie; `stepSpeed` dă pe fel viteza dintre rânduri consecutive ale unui traseu, cum le unește vizualizatorul (mediana, percentila 99, cea mai mare, și pașii mai rapizi decât este posibil, care trebuie să fie 0) |

---

Parte din [3DHeat](https://github.com/Holdi601/3DHeat) ([documentație](https://holdi601.github.io/3DHeat/)). Sursă: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
