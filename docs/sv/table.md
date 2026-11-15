---
title: "Tabellen"
nav_order: 6
lang: "sv"
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# Tabellen {#the-table}

![Tabellen för en syntetisk repris, sammanfattad](../assets/img/table.svg)

En rad per mätpunkt eller händelse, 105 kolumner ([Kolumnlista](../columns.md), genererad från
koden); i sidfoten, under `heat3d`, visarens läsanvisningar, så visaren behöver inget formulär ifyllt.

| Kolumn | Vad |
|---|---|
| `time` | sekunder på repriets egen klocka |
| `event` | `position`; händelserader ligger på banan vid sitt ögonblick (mellan två mätpunkter, på linjen mellan dem); `kill` (vid dödaren), `death` (vid offret), `hit_critical` / `hit_severe` (vid den träffade enheten), `module_destroyed` (vid enheten), `launch` (vid enheten som släppte ett vapen), `impact` (ett vapens sista mätpunkt när det togs bort direkt efter); `explosion` och `flak` (0xD08E, 0xD01F) vid deras position, slag `effect`, ingen bana, med explosionens riktning där en finns; `shot` (en projektil som träffade, vid skytten), `gun_shot`, `fire_start`, `fire_stop` (en kanons skur, inte ett fordon i brand), `fire_on`, `fire_off` (ett fordon i brand, se [Fordonsbränder](hits.md#vehicle-fires)), `reward` (Silver Lions och forskningspoäng intjänade, se [Ekonomi](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (se [Meddelanden till enheter](how-it-reads.md#messages-to-units)); `despawn`: den sista raden i en bana vars enhet är borta innan repriset tar slut (se [Slutet på en bana](ground.md#end-of-a-track)) |
| `track` | det visaren ritar som en enda sak: ett liv för en enhet, eller ett vapens flygning - `<player or vehicle> #<hex>` (visaren visar namnet utan `#`-delen) |
| `x`, `y`, `z` | spelets meter: x öster, y upp, z norr (tipsen speglar z, så norr ritas inte söder) |
| `player` | spelarens namn; en AI-enhet `<VehicleName> #<uid>` (till exempel `F-15A #204`); `uid <n>` när inget namnger den; för ett vapen, vem som släppte det |
| `userId`, `team` | spelarens Gaijin-id och laget (`1`, `2`) |
| `ai`, `isPlayer` | `ai` sant för varje enhet som inget spelarkonto kör (uppdragsenheter, AI-flygplan, markmål, luftvärnskanoner, fartyg utan spelare, platshållare), `isPlayer` tvärtom: en spelare är en enhet vars entitet namnger en spelarplats med ett Gaijin-id. Ett vapen har sin avfyrares; tomt när det inte är känt |
| `match` | matchens id (matchdokumentets `match`), på varje rad; tipsen kopplar det som session, så två inlästa repriser aldrig sammanfogar banor |
| `life` | `uid#n`: en enhets bana, klippt där uid:t går över till en annan enhet, enheten rör sig snabbare än den kan (en återuppståndelse, en ompålastning, spelet flyttar den, klienten korrigerar en avlägsen enhet; se Teleporteringar i [Så läser den en repris](how-it-reads.md#what-is-read-and-the-check)) eller är länge osedd; `w<hex>` ett vapens flygning (`w<hex>#n` efter ett klipp) |
| `uid` | enhetens id i repriset |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (en spårvagn eller järnvägsvagn som nivån placerar, se [Scenenheter](objectives.md#scene-units-trams-and-rail-wagons)); vapen `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` den inspelande spelarens repriskamera (se [Kameran](ground.md#the-camera)) |
| `type` | spelets egen typ där resultaten anger den (`fighter`, `assault`, `destroyer`, `gun_boat`), annars som `kind` |
| `Vehicle` | spelets eget fordons-id (`f_15a`, `germ_flakpz_I_Gepard`), som visarens figurer matchar |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | fordonets engelska namn ur din installations lokalisering (`Pz.Kpfw. III Ausf. J1`, kort `Pz.III J1`) och dess nyckel (`germ_pzkpfw_III_ausf_J_0`); spelets typsnitts landsmärken utelämnas. Där spelet inte namnger något, eller ingen installation hittas, är namnet id:t och nyckeln tom |
| `mission` | enhetens namn i uppdraget (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | vart enheten pekar (blickvektorn): flygplan från flygmodellens attityd, markenheter och fartyg från sina egna, vapen längs deras flygning |
| `heading`, `pitch`, `roll` | samma i grader; kurs är kompassen, medurs från norr, stigning nos uppåt positiv, rulle höger vinge nedåt positiv (flygmodellen skickar motsatt tecken, se [Attityd, kontrollerad](aircraft.md#attitude-checked); en markenhets högra sida nedåt). Tipsen säger det under `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | en stridsvagns huvudtorn - dit kanonen pekar, inte dit spelaren tittar; repriets värde hållet till tornmotorns hastighet och satt till varje huvudkanonskotts linje (se [Torn](ground.md#turrets)): dess gir relativt skrovet (grader, medurs sett uppifrån positivt, 0 rakt fram) och dess kanons höjd relativt skrovet (grader, uppåt positiv); `turrets` varje torn på fordonet som `yaw pitch;yaw pitch;...` i dess egen ordning (en oanvänd plats läses `0.00 0.00`). Stridsvagnar, SPAA, pansarfordon och lastbilar, i klient- och serverrepriser; inte fartyg (se [Torn](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | huvudtornet så som repriset skickar det; `turretYaw` / `gunPitch` är det hållet till tornmotorns hastighet och satt till varje huvudkanonskotts linje (se [Torn](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | vart spelaren tittar (siktar med kameran) i världen: kompassgrader (0 norr, medurs) och grader uppåt, samma konvention som `aimHeading` / `aimPitch` (till skillnad från `turretYaw` / `gunPitch`, som förblir relativa skrovet). Varje spelares stridsvagn i en serverrepris, den inspelande spelarens egen i en klientrepris; tomt där spelaren inte siktar någonstans (alla fyra siktflyttalen 0). Tornet följer det med sin egen tvärhastighet, så de två skiljer sig medan det vrider sig (se [Torn](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | den inspelande spelarens egen stridsvagn: vart den siktar (kompassgrader, grader uppåt, avståndet i m; 2000 när inget är i sikte); kamerarader: vart spelaren siktar (kurs, stigning) |
| `zoom` | kamerarader: kamerans förstoring (se [Kameran](ground.md#the-camera)) |
| `difficulty`, `gameMode` | striden `AB`, `RB` eller `SB`, och `ground`, `air` eller `naval`, på varje rad (se [Stridsläge](ground.md#battle-mode)) |
| `extrapolated` | en flygplansmätpunkt som är klientens dead reckoning, inte ett tillstånd den tog emot (se [Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)); en bombs mätpunkt uträknad från dess släpp (se Bomber utan flygposter i [Så läser den en repris](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | hur långt utjämnaren flyttade mätpunkten (m), och repriets egen position och attityd (rulle i tabellens tecken) |
| `targetX`, `targetY`, `targetZ` | en `shot`s träffpunkt |
| `hitOutcome`, `hitFlags` | en `shot`s utfall på en markenhet: `kill`, `critical`, `penetration` eller `nonpenetration` (studsad eller stoppad: repriset kan inte skilja en rikoschett från den), ur bitarna servern skickar med träffen (`hitFlags`, råa); tomt där ingen skickas (flygplan, fartyg). Se [Träffutfall](hits.md#hit-outcomes) |
| `hitShell` | en `shot`s granatsignatur: fyra byte ur träffmeddelandet (rått hex); en signatur kan stå för olika granater (120 och 125 mm APFSDS delar en), så den behålls rå, inte läst som en kaliber |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | en `shot`s ammunition: dess typ (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) och id (`125mm_3bm46`) där ett dödsfall namnger skyttens plats, annars `explosive` (träffskuren) eller `kinetic`; kanonens `weapon/slot` från dess omladdningar; kalibern i mm ur installationens vapenfiler. Se [Träffutfall](hits.md#hit-outcomes) |
| `rpm` | ett flygplans motorvarvtal (medelvärdet för dess motorer) så som senast skickat, inom 2 s |
| `vx`, `vy`, `vz` | ett flygplans hastighet så som dess flygpost skickar den (m/s, spelets axlar; hastigheter över 500 m/s läses 500) |
| `engine`, `afterburner`, `engineCondition` | ett flygplans motorer ur dess flygpost: `off`, `starting`, `running`, `dead` (sammanfogat med `/` när dess motorer skiljer sig); efterbrännaren 0-1; en byte som bara skickas efter att motorn träffats |
| `weaponName` | dödsfall och förluster: vapnet eller ammunitionen på din installations engelska (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | endast den inspelande spelarens flygplan: gasen 0-1,1 ur dess cockpit (1,1 vid krigsnödeffekt eller efterbrännare; annars flygpostens femtondelar), reglagen -1..1 ur dess flygpost (höjdroder positivt när det drar upp, skevroder positivt när det rullar höger), skotten kvar per vapen (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | endast den inspelande spelarens flygplan, ur dess cockpit: visad lufthastighet och stigningshastighet (m/s), bränsle, laddtryck (atm), ställ (0-1, 1 nere), olje- och cylinderhuvudtemperatur, där dess cockpit har mätaren |
| `speed` | m/s över ungefär två sekunder av banan (uträknat här; repriset skickar ingen fart för andra enheter) |
| `alive` | 0 för en enhets mätpunkter efter dess död (dess vrak): en markenhets eller fartygs tills spelet tar bort den eller dess mätpunkter tar slut, ett flygplans högst 60 s |
| `otherVehicle`, `otherLife` | en `shot`s offer: dess fordon och dess `life` |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | en `shot`s träffpunkt i offrets egna system (m; x framåt, y upp, z vänster; se [Meddelanden till enheter](how-it-reads.md#messages-to-units)) och skottets väg, vriden in i det systemet av offrets attityd då |
| `hitPart`, `hitFlag` | en `shot`s träffmeddelande: dess delord så som det skickades, och dess höga byte |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | vad striden kostade och gav, och vem som vann: se [Ekonomi](economy.md) |
| `other`, `weapon` | dödsfall: den andra sidan och vapnet; träffar: vem som träffade (ur postens uid, annars spelarplatsen), deras fordon; uppskjutningar: vapnet; förstörda moduler: vem som sist träffade enheten inom 5 s före, och `part <n>` |

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Källa: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
