---
title: "Taflan"
nav_order: 6
lang: is
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# Taflan {#the-table}

![Tafla tilbúinnar upptöku, í samantekt](../assets/img/table.svg)

Ein röð fyrir hvert sýni eða atburð, 105 dálkar ([Dálkalisti](../columns.md), búinn til úr kóðanum); í fætinum, undir `heat3d`, eru lestrarleiðbeiningar skoðarans, svo skoðarinn þarf ekkert eyðublað útfyllt.

| Dálkur | Hvað |
|---|---|
| `time` | sekúndur á eigin klukku upptökunnar |
| `event` | `position`; atburðaraðir liggja á ferlinum á sinni stundu (milli tveggja sýna, á línunni milli þeirra); `kill` (hjá drápsmanni), `death` (hjá fórnarlambi), `hit_critical` / `hit_severe` (hjá einingunni sem varð fyrir höggi), `module_destroyed` (hjá einingunni), `launch` (hjá einingunni sem sleppti vopni), `impact` (síðasta sýni vopns þegar það var fjarlægt rétt á eftir); `explosion` og `flak` (0xD08E, 0xD01F) á stöðu sinni, tegund `effect`, enginn ferill, með stefnu sprengingarinnar þar sem hún hefur eina; `shot` (skot sem hitti, hjá skyttunni), `gun_shot`, `fire_start`, `fire_stop` (skothríð úr byssu, ekki farartæki í ljósum logum), `fire_on`, `fire_off` (farartæki í ljósum logum, sjá [Eldar í farartækjum](hits.md#vehicle-fires)), `reward` (Silver Lions og rannsóknarstig unnin, sjá [Hagkerfi](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (sjá [Skilaboð til eininga](how-it-reads.md#messages-to-units)); `despawn`: síðasta röð ferils þar sem einingin er horfin áður en upptakan endar (sjá [Endir ferils](ground.md#end-of-a-track)) |
| `track` | það sem skoðarinn teiknar sem einn hlut: eitt líf einingar, eða flug eins vopns - `<player or vehicle> #<hex>` (skoðarinn sýnir nafnið án `#` hlutans) |
| `x`, `y`, `z` | metrar leiksins: x austur, y upp, z norður (ábendingarnar spegla z, svo norður er ekki teiknað í suður) |
| `player` | nafn spilarans; gervigreindareining `<VehicleName> #<uid>` (til dæmis `F-15A #204`); `uid <n>` þegar ekkert nefnir hana; fyrir vopn, hver sleppti því |
| `userId`, `team` | Gaijin-auðkenni spilarans og liðið (`1`, `2`) |
| `ai`, `isPlayer` | `ai` satt fyrir hverja einingu sem enginn spilarareikningur stýrir (verkefniseiningar, gervigreindarflugvélar, skotmörk á landi, loftvarnabyssur, skip án spilara, staðgenglar), `isPlayer` andstæðan: spilari er eining sem einingin nefnir spilararauf með Gaijin-auðkenni. Vopn hefur gildi þess sem sleppti því; tómt þegar það er ekki vitað |
| `match` | auðkenni leiksins (`match` í leikjaskjalinu), á hverri röð; ábendingarnar varpa því sem lotu (session), svo tvær hlaðnar upptökur tengja aldrei ferla |
| `life` | `uid#n`: ferill einnar einingar, skorinn þar sem uid færist til annarrar einingar, einingin hreyfist hraðar en hún getur (endurkoma, endurhleðsla, leikurinn flytur hana, biðlarinn leiðréttir fjarlæga einingu; sjá Teleports í [Hvernig upptaka er lesin](how-it-reads.md#what-is-read-and-the-check)) eða er lengi ósýnd; `w<hex>` flug vopns (`w<hex>#n` eftir skurð) |
| `uid` | auðkenni einingarinnar í upptökunni |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (sporvagn eða járnbrautarvagn sem borðið setur, sjá [Senueiningar](objectives.md#scene-units-trams-and-rail-wagons)); vopn `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` upptökumyndavél upptökumannsins (sjá [Myndavélin](ground.md#the-camera)) |
| `type` | eigin gerð leiksins þar sem niðurstöðurnar nefna hana (`fighter`, `assault`, `destroyer`, `gun_boat`), annars eins og `kind` |
| `Vehicle` | auðkenni farartækis í leiknum (`f_15a`, `germ_flakpz_I_Gepard`), sem fígúrur skoðarans passa við |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | enska nafn farartækisins úr staðfæringu þinnar uppsetningar (`Pz.Kpfw. III Ausf. J1`, stutt `Pz.III J1`) og lykill þess (`germ_pzkpfw_III_ausf_J_0`); landamerki leturgerðar leiksins eru felld niður. Þar sem leikurinn nefnir ekkert, eða engin uppsetning finnst, er nafnið auðkennið og lykillinn tómur |
| `mission` | nafn einingarinnar í verkefninu (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | hvert einingin vísar (sjónstefnuvigurinn): flugvélar úr afstöðu flugmódelsins, landeiningar og skip úr sinni eigin, vopn eftir flugi sínu |
| `heading`, `pitch`, `roll` | hið sama í gráðum; heading er áttavitinn, réttsælis frá norðri, pitch nef upp er jákvætt, roll hægri vængur niður er jákvætt (flugmódelið sendir öfugt formerki, sjá [Afstaða, athuguð](aircraft.md#attitude-checked); hægri hlið landeiningar niður). Ábendingarnar segja það undir `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | aðalturn skriðdreka - hvert byssan vísar, ekki hvert spilari hans lítur; gildi upptökunnar haldið við hraða turndrifsins og stillt á línu hvers aðalbyssuskots (sjá [Turnar](ground.md#turrets)): snúningur hans miðað við skrokkinn (gráður, réttsælis séð að ofan er jákvætt, 0 beint áfram) og halli byssunnar miðað við skrokkinn (gráður, upp er jákvætt); `turrets` hver turn farartækisins sem `yaw pitch;yaw pitch;...` í sinni eigin röð (ónotuð rauf les `0.00 0.00`). Skriðdrekar, SPAA, APC og vörubílar, í biðlara- og þjónsupptökum; ekki skip (sjá [Turnar](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | aðalturninn eins og upptakan sendir hann; `turretYaw` / `gunPitch` eru hann haldinn við hraða turndrifsins og stilltur á línu hvers aðalbyssuskots (sjá [Turnar](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | hvert spilarinn lítur (miðar með myndavélinni) í heiminum: áttavitagráður (0 norður, réttsælis) og gráður upp, sama venja og `aimHeading` / `aimPitch` (ólíkt `turretYaw` / `gunPitch`, sem haldast miðað við skrokkinn). Skriðdreki hvers spilara í þjónsupptöku, sá eigin hjá upptökumanni í biðlaraupptöku; tómt þar sem spilarinn miðar hvergi (allar fjórar miðunartölur 0). Turninn fylgir því á eigin snúningshraða, svo þetta tvennt er ólíkt meðan hann snýst (sjá [Turnar](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | skriðdreki upptökumannsins sjálfs: hvert hann miðar (áttavitagráður, gráður upp, fjarlægðin í m; 2000 þegar ekkert er í sjónaukanum); myndavélaraðir: hvert spilarinn miðar (heading, pitch) |
| `zoom` | myndavélaraðir: stækkun myndavélarinnar (sjá [Myndavélin](ground.md#the-camera)) |
| `difficulty`, `gameMode` | `AB`, `RB` eða `SB` bardagans, og `ground`, `air` eða `naval`, á hverri röð (sjá [Bardagahamur](ground.md#battle-mode)) |
| `extrapolated` | flugvélarsýni sem er ágiskun (dead reckoning) biðlarans, ekki ástand sem hann tók á móti (sjá [Ágiskun á stöðu](aircraft.md#dead-reckoning-and-the-smoother)); sýni sprengju reiknað út frá losun hennar (sjá Bombs without flight records í [Hvernig upptaka er lesin](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | hversu langt sléttarinn færði sýnið (m), og eigin staða og afstaða upptökunnar (roll með formerki töflunnar) |
| `targetX`, `targetY`, `targetZ` | höggpunktur `shot` |
| `hitOutcome`, `hitFlags` | útkoma `shot` á landeiningu: `kill`, `critical`, `penetration` eða `nonpenetration` (skaust af eða stöðvað: upptakan greinir ekki ricochet frá), úr bitunum sem þjónninn sendir með högginu (`hitFlags`, hrátt); tómt þar sem enginn er sendur (flugvélar, skip). Sjá [Útkoma högga](hits.md#hit-outcomes) |
| `hitShell` | skeljarundirskrift `shot`: fjögur bæti höggskilaboðanna (hrátt hex); ein undirskrift getur staðið fyrir ólíkar skeljar (120 og 125 mm APFSDS deila einni), svo hún er varðveitt hrá, ekki lesin sem kaliber |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | skotfæri `shot`: tegund þess (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) og auðkenni (`125mm_3bm46`) þar sem dráp nefnir rauf skyttunnar, annars `explosive` (höggsprengingin) eða `kinetic`; `weapon/slot` byssunnar úr endurhleðslum hennar; kaliberið í mm úr vopnaskrám uppsetningarinnar. Sjá [Útkoma högga](hits.md#hit-outcomes) |
| `rpm` | snúningar á mínútu hreyfils flugvélar (meðaltal hreyfla hennar) eins og síðast sent, innan 2 s |
| `vx`, `vy`, `vz` | hraði flugvélar eins og færsla hennar sendir hann (m/s, ásar leiksins; hraði yfir 500 m/s les 500) |
| `engine`, `afterburner`, `engineCondition` | hreyflar flugvélar úr færslu hennar: `off`, `starting`, `running`, `dead` (tengt með `/` þegar hreyflar hennar eru ólíkir); eftirbrennarinn 0-1; bæti sem er aðeins sent eftir að hreyfillinn varð fyrir höggi |
| `weaponName` | dráp og dauðsföll: vopnið eða skotfærin á ensku þinnar uppsetningar (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | aðeins flugvél upptökumannsins: inngjöfin 0-1,1 úr stjórnklefa hennar (1,1 neyðarafl eða eftirbrennari; annars fimmtándu hlutar færslunnar), stýrin -1..1 úr færslu hennar (hæðarstýri jákvætt að toga, hallastýri jákvætt að rúlla til hægri), skotin eftir í hverju vopni (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | aðeins flugvél upptökumannsins, úr stjórnklefa hennar: sýndur lofthraði og klifurhraði (m/s), eldsneyti, hleðsluþrýstingur (atm), hjól (0-1, 1 niðri), hiti olíu og strokkhauss, þar sem stjórnklefi hennar hefur mælinn |
| `speed` | m/s yfir um tvær sekúndur ferilsins (reiknað hér; upptakan sendir engan hraða fyrir aðrar einingar) |
| `alive` | 0 fyrir sýni einingar eftir dauða hennar (flak hennar): landeiningar eða skips þar til leikurinn fjarlægir það eða sýni þess enda, flugvélar í mesta lagi 60 s |
| `otherVehicle`, `otherLife` | fórnarlamb `shot`: farartæki þess og `life` þess |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | höggpunktur `shot` í eigin ramma fórnarlambsins (m; x fram, y upp, z vinstri; sjá [Skilaboð til eininga](how-it-reads.md#messages-to-units)) og leiðin sem skotið kom, snúin í þann ramma með afstöðu fórnarlambsins þá |
| `hitPart`, `hitFlag` | höggskilaboð `shot`: hlutaorð þess eins og sent, og hábæti þess |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | hvað bardaginn kostaði og gaf af sér, og hver vann: sjá [Hagkerfi](economy.md) |
| `other`, `weapon` | dráp: hinn aðilinn og vopnið; högg: hver sló (úr uid færslunnar, annars úr spilararauf hans), farartæki hans; losun: vopnið; eyðilagðir hlutar: hver sló eininguna síðast innan 5 s áður, og `part <n>` |

---

Hluti af [3DHeat](https://github.com/Holdi601/3DHeat) ([skjölun](https://holdi601.github.io/3DHeat/)). Frumkóði: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
