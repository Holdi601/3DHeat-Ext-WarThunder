---
title: Tabel
nav_order: 6
lang: et
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# Tabel {#the-table}

![Synteetilise kordase tabel, kokkuvõttena](../assets/img/table.svg)

Üks rida iga näidise või sündmuse kohta, 105 veergu ([Veergude loend](../columns.md), koodist genereeritud);
jaluses, jaotises `heat3d`, on vaaturi lugemisjuhised, nii et vaaturile ei pea midagi täitma.

| Veerg | Mis see on |
|---|---|
| `time` | sekundid kordusa enda kella järgi |
| `event` | `position`; sündmuste read asuvad rajal oma hetkes (kahe näidise vahel, nendevahelisel joonel); `kill` (tapjal), `death` (ohvril), `hit_critical` / `hit_severe` (tabatud üksusel), `module_destroyed` (üksusel), `launch` (üksusel, mis vabastas relva), `impact` (relva viimane näidis, kui see eemaldati kohe pärast); `explosion` ja `flak` (0xD08E, 0xD01F) oma asukohas, liik `effect`, ilma rajata, koos plahvatuse suunaga, kui sellel on see; `shot` (tabanud projektil, laskjal), `gun_shot`, `fire_start`, `fire_stop` (kahuri pursu, mitte põlev sõiduk), `fire_on`, `fire_off` (põlev sõiduk, vt [Sõiduki tulekahjud](hits.md#vehicle-fires)), `reward` (teenitud Silver Lions ja uurimispunktid, vt [Majandus](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (vt [Sõnumid üksustele](how-it-reads.md#messages-to-units)); `despawn`: raja viimane rida, mille üksus on kadunud enne kordusa lõppu (vt [Raja lõpp](ground.md#end-of-a-track)) |
| `track` | see, mida vaatur joonistab ühe asjana: ühe üksuse üks elu või ühe relva lend - `<player or vehicle> #<hex>` (vaatur näitab nime ilma `#` osata) |
| `x`, `y`, `z` | mängu meetrid: x ida, y üles, z põhja (vihjed peegeldavad z, nii et põhi ei joonistu lõunasse) |
| `player` | mängija nimi; AI üksus `<VehicleName> #<uid>` (näiteks `F-15A #204`); `uid <n>`, kui miski seda ei nimeta; relva puhul see, kes selle vabastas |
| `userId`, `team` | mängija Gaijini ID ja meeskond (`1`, `2`) |
| `ai`, `isPlayer` | `ai` tõene igale üksusele, mida ükski mängijakonto ei juhi (missiooni üksused, AI lennukid, maapealsed sihtmärgid, õhutõrjekahurid, mängijata laevad, kohahoidjad), `isPlayer` vastupidi: mängija on üksus, mille olem nimetab mängijakohta Gaijini ID-ga. Relval on oma käivitaja oma; tühi, kui ei ole teada |
| `match` | lahingu ID (mängu dokumendi `match`) igal real; vihjed seovad selle sessiooniks, nii et kaks laaditud kordust ei ühenda rajad |
| `life` | `uid#n`: ühe üksuse rada, lõigatud, kui uid läheb teisele üksusele, üksus liigub kiiremini kui suudab (taasilmumine, uuesti relvastamine, mäng liigutas teda, klient parandas kaugema üksuse; vt Teleporteerumised [Kuidas tööriist kordust loeb](how-it-reads.md#what-is-read-and-the-check)) või on kaua nägemata; `w<hex>` relva lend (`w<hex>#n` pärast lõiget) |
| `uid` | üksuse ID kordusel |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (tramm või raudteevagun, mille tase paigutab, vt [Stseeni üksused](objectives.md#scene-units-trams-and-rail-wagons)); relvad `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` salvestajamängija kordusekaamera (vt [Kaamera](ground.md#the-camera)) |
| `type` | mängu enda tüüp, kui tulemused seda nimetavad (`fighter`, `assault`, `destroyer`, `gun_boat`), muidu nagu `kind` |
| `Vehicle` | mängu sõiduki ID (`f_15a`, `germ_flakpz_I_Gepard`), millele vaaturi kujud vastavad |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | sõiduki inglisekeelne nimi sinu installatsiooni lokaadist (`Pz.Kpfw. III Ausf. J1`, lühike `Pz.III J1`) ja selle võti (`germ_pzkpfw_III_ausf_J_0`); mängu fondi riigimärgid jäetakse välja. Kus mäng midagi ei nimeta või installatsiooni ei leita, on nimi ID ja võti tühi |
| `mission` | üksuse nimi missioonis (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | kuhu üksus osutab (vaatevektor): lennukid lennumudeli asendist, maapealsed üksused ja laevad oma asendist, relvad mööda oma lendu |
| `heading`, `pitch`, `roll` | sama kraadides; suund on kompass, päripäeva põhjast, pitš ninaga üles positiivne, rull parem tiib alla positiivne (lennumudel saadab vastupidise märgi, vt [Asend, kontrollitud](aircraft.md#attitude-checked); maapealse üksuse parem külg alla). Vihjed ütlevad seda jaotises `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | tanki peamine torn - kuhu püss sihib, mitte kuhu mängija vaatab; kordusest saadud väärtus, mida hoitakse torni ajami kiiruse piires ja seatud iga peamise püssi lasu joonele (vt [Tornid](ground.md#turrets)): pööre korpuse suhtes (kraadides, päripäeva ülevalt vaadatuna positiivne, 0 otse ees) ja püssi tõus korpuse suhtes (kraadides, üles positiivne); `turrets` iga sõiduki torn kujul `yaw pitch;yaw pitch;...` oma järjekorras (kasutamata pesa loeb `0.00 0.00`). Tankid, SPAA, APC-d ja veokid, kliendi ja serveri kordustel; mitte laevad (vt [Tornid](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | peamine torn nii, nagu kordus seda saadab; `turretYaw` / `gunPitch` on see, hoitud torni ajami kiiruse piires ja seatud iga peamise püssi lasu joonele (vt [Tornid](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | kuhu mängija vaatab (sihib kaameraga) maailmas: kompassi kraadid (0 põhi, päripäeva) ja kraadid üles, sama kokkulepe mis `aimHeading` / `aimPitch` (erinevalt `turretYaw` / `gunPitch`-ist, mis jäävad korpuse suhtes). Iga mängija tank serveri kordusel, salvestajamängija oma kliendi kordusel; tühi, kus mängija ei sihi kuhugi (kõik neli sihi ujukomaarvu 0). Torn järgib seda oma pöördekiirusega, nii et need kaks erinevad, kui see pöördub (vt [Tornid](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | salvestajamängija enda tank: kuhu see sihib (kompassi kraadid, kraadid üles, kaugus m-des; 2000, kui sihikus ei ole midagi); kaamera read: kuhu mängija sihib (suund, pitš) |
| `zoom` | kaamera read: kaamera suurendus (vt [Kaamera](ground.md#the-camera)) |
| `difficulty`, `gameMode` | lahingu `AB`, `RB` või `SB`, ja `ground`, `air` või `naval`, igal real (vt [Lahingurežiim](ground.md#battle-mode)) |
| `extrapolated` | lennuki näidis, mis on kliendi hinnanguline asukoht, mitte vastuvõetud olek (vt [Hinnanguline asukoht](aircraft.md#dead-reckoning-and-the-smoother)); pommi näidis, mis arvutati selle vabastusest (vt Pommid ilma lennukirjeteta [Kuidas tööriist kordust loeb](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | kui kaugele silur näidist liigutas (m), ja kordusa enda asukoht ja asend (rull tabeli märgiga) |
| `targetX`, `targetY`, `targetZ` | `shot` tabamuspunkt |
| `hitOutcome`, `hitFlags` | `shot` tulemus maapealsel üksusel: `kill`, `critical`, `penetration` või `nonpenetration` (põrkas või peatus: kordus ei ütle rikošetti eraldi), serveri tabamusega saadetud bittidest (`hitFlags`, toorelt); tühi, kus ühtegi ei saadeta (lennukid, laevad). Vt [Tabamuste tulemused](hits.md#hit-outcomes) |
| `hitShell` | `shot` kesta signatuur: tabamuse sõnumi neli baiti (toorel kuueteistkümnendsüsteemis); üks signatuur võib tähistada erinevaid kestasid (120 ja 125 mm APFSDS jagavad ühte), seega hoitakse seda toorelt, mitte ei loeta kaliibrina |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | `shot` laskemoon: tema tüüp (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) ja ID (`125mm_3bm46`), kus tapmine nimetab laskja pesa, muidu `explosive` (tabamuse pursk) või `kinetic`; püssi `weapon/slot` tema laadimistest; kaliiber mm-des installatsiooni relvafailidest. Vt [Tabamuste tulemused](hits.md#hit-outcomes) |
| `rpm` | lennuki mootori pöörded (keskmine tema mootorite üle) viimati saadetuna, 2 s piires |
| `vx`, `vy`, `vz` | lennuki kiirus, nagu tema lennukirje seda saadab (m/s, mängu teljed; üle 500 m/s kiirused loevad 500) |
| `engine`, `afterburner`, `engineCondition` | lennuki mootorid tema lennukirjest: `off`, `starting`, `running`, `dead` (`/`-ga ühendatud, kui tema mootorid erinevad); järelpõletaja 0-1; bait, mis saadetakse ainult pärast mootori tabamust |
| `weaponName` | tapmised ja surmad: relv või laskemoon sinu installatsiooni inglise keeles (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | ainult salvestajamängija lennuk: gaas 0-1,1 tema kabiinist (1,1 sõjaline hädavõimsus või järelpõletaja; muidu tema lennukirje viiteistkümnendikud), juhtimine −1..1 tema lennukirjest (kõrgusroor positiivne tõmbamisel, rullid positiivne paremale rullimisel), järelejäänud laskemoon relva kohta (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | ainult salvestajamängija lennuk, tema kabiinist: näidatud õhkiirus ja tõusukiirus (m/s), kütus, sisselaskerõhk (atm), maandumisrattad (0-1, 1 all), õli ja silindripea temperatuur, kus kabiinis on näidik |
| `speed` | m/s raja umbes kahe sekundi jooksul (arvutatud siin; kordus ei saada kiirust teistele üksustele) |
| `alive` | 0 üksuse näidistele pärast tema surma (tema vrakk): maapealse üksuse või laeva oma, kuni mäng eemaldab selle või kuni tema näidised lõpevad; lennuki oma kuni 60 s |
| `otherVehicle`, `otherLife` | `shot` ohver: tema sõiduk ja tema `life` |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | `shot` tabamuspunkt ohvri enda raamistikus (m; x ees, y üles, z vasakule; vt [Sõnumid üksustele](how-it-reads.md#messages-to-units)) ja see, kuidas lask tuli, pööratuna sellesse raamistikku ohvri asendi järgi tol ajal |
| `hitPart`, `hitFlag` | `shot` tabamuse sõnum: tema osa sõna nii, nagu see saadeti, ja selle ülemine bait |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | mis lahing maksis ja teenis ning kes võitis: vt [Majandus](economy.md) |
| `other`, `weapon` | tapmised: teine pool ja relv; tabamused: kes tabas (kirje uid-ist, muidu tema mängijakohast), nende sõiduk; käivitused: relv; hävitatud moodulid: kes viimati tabas üksust 5 s jooksul enne seda, ja `part <n>` |

---

Osa [3DHeatist](https://github.com/Holdi601/3DHeat) ([dokumentatsioon](https://holdi601.github.io/3DHeat/)). Lähtekood: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
