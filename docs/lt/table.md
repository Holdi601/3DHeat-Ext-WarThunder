---
title: Lentelė
nav_order: 6
lang: lt
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# Lentelė {#the-table}

![The table of a synthetic replay, summarised](../assets/img/table.svg)

Viena eilutė kiekvienam pavyzdžiui ar įvykiui, 105 stulpeliai ([Stulpelių sąrašas](../columns.md), sugeneruotas iš kodo); poraštėje, po `heat3d`, - žiūryklės skaitymo nurodymai, todėl žiūryklei nereikia jokios formos pildyti.

| Stulpelis | Ką reiškia |
|---|---|
| `time` | sekundės pagal įrašo paties laikrodį |
| `event` | `position`; įvykių eilutės guli ant trajektorijos savo akimirkoje (tarp dviejų pavyzdžių, ant linijos tarp jų); `kill` (ties žudiku), `death` (ties auka), `hit_critical` / `hit_severe` (ties pataikytu vienetu), `module_destroyed` (ties vienetu), `launch` (ties vienetu, kuris paleido ginklą), `impact` (paskutinis ginklo pavyzdys, kai jis pašalintas iš karto po to); `explosion` ir `flak` (0xD08E, 0xD01F) savo pozicijoje, rūšis `effect`, be trajektorijos, su sprogimo kryptimi, kur ji yra; `shot` (sviedinys, kuris pataikė, prie šaulio), `gun_shot`, `fire_start`, `fire_stop` (patrankos serija, ne degantis vienetas), `fire_on`, `fire_off` (degantis vienetas, žr. [Technikos gaisrai](hits.md#vehicle-fires)), `reward` (uždirbti Sidabro liūtai ir tyrimų taškai, žr. [Ekonomika](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (žr. [Pranešimai vienetams](how-it-reads.md#messages-to-units)); `despawn`: paskutinė trajektorijos eilutė, kai jos vienetas dingsta prieš įrašui pasibaigiant (žr. [Trajektorijos pabaiga](ground.md#end-of-a-track)) |
| `track` | ką žiūryklė piešia kaip vieną dalyką: vieno vieneto gyvenimą arba vieno ginklo skrydį - `<player or vehicle> #<hex>` (žiūryklė rodo vardą be `#` dalies) |
| `x`, `y`, `z` | žaidimo metrai: x - į rytus, y - aukštyn, z - į šiaurę (užuominos apverčia z, todėl šiaurė nepiešiama į pietus) |
| `player` | žaidėjo vardas; DI vienetas `<VehicleName> #<uid>` (pavyzdžiui `F-15A #204`); `uid <n>`, kai nieko jo nevadina; ginklui - kas jį paleido |
| `userId`, `team` | žaidėjo Gaijin id ir komanda (`1`, `2`) |
| `ai`, `isPlayer` | `ai` true kiekvienam vienetui, kurio nevairuoja joks žaidėjo paskyra (misijos vienetai, DI orlaiviai, sausumos taikiniai, priešlėktuviniai patrankos, laivai be žaidėjo, vietos laikikliai), `isPlayer` - priešingai: žaidėjas yra vienetas, kurio esybė nurodo žaidėjo lizdą su Gaijin id. Ginklas turi savo paleidėjo; tuščias, kai nežinoma |
| `match` | rungtynių id (rungtynių dokumento `match`) kiekvienoje eilutėje; užuominos jį priima kaip sesiją, todėl du įkelti įrašai niekada nesijungia į vieną trajektoriją |
| `life` | `uid#n`: vieno vieneto trajektorija, nupjauta, kai uid pereina į kitą vienetą, vienetas juda greičiau, nei gali (atgimimas, papildymas, žaidimas perkelia vienetą, klientas pataiso tolimą vienetą; žr. Teleportacijos [Kaip įrankis skaito įrašą](how-it-reads.md#what-is-read-and-the-check)), arba jis ilgai nematomas; `w<hex>` - ginklo skrydis (`w<hex>#n` po pjūvio) |
| `uid` | vieneto id įraše |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (tramvajus ar geležinkelio vagonas, kurį lygis vietoje patalpina, žr. [Scenos vienetai](objectives.md#scene-units-trams-and-rail-wagons)); ginklai - `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` - įrašantį žaidėją replėjaus kamera (žr. [Kamera](ground.md#the-camera)) |
| `type` | paties žaidimo tipas, kai rezultatai jį nurodo (`fighter`, `assault`, `destroyer`, `gun_boat`), kitu atveju kaip `kind` |
| `Vehicle` | žaidimo technikos id (`f_15a`, `germ_flakpz_I_Gepard`), su kuriuo sutampa žiūryklės figūros |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | technikos angliškas vardas iš jūsų diegimo lokalizacijos (`Pz.Kpfw. III Ausf. J1`, trumpas `Pz.III J1`) ir jos raktas (`germ_pzkpfw_III_ausf_J_0`); žaidimo šrifto šalių ženklai praleisti. Kai žaidimas nieko nepavadina arba diegimo nerasta, vardas yra id, o raktas tuščias |
| `mission` | vieneto vardas misijoje (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | kur nukreiptas vienetas (žiūrėjimo vektorius): orlaiviams - iš skrydžio modelio orientacijos, sausumos vienetams ir laivams - iš jų pačių, ginklams - išilgai jų skrydžio |
| `heading`, `pitch`, `roll` | tas pats laipsniais; kryptis - kompasas, pagal laikrodžio rodyklę nuo šiaurės, kėlimas teigiamas nosį aukštyn, posūkis teigiamas dešinysis sparnas žemyn (skrydžio modelis siunčia priešingą ženklą, žr. [Orientacija, patikrinta](aircraft.md#attitude-checked); sausumos vieneto dešinysis šonas žemyn). Užuominos tai nurodo `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | tanko pagrindinis bokštelis - kur nukreipta patranka, o ne kur žiūri jo žaidėjas; įrašo reikšmė, sulaikyta iki bokštelio pavaros greičio ir nustatyta į kiekvieno pagrindinės patrankos šūvio liniją (žr. [Bokšteliai](ground.md#turrets)): jo posūkis, palyginti su korpusu (laipsniais, pagal laikrodžio rodyklę matant iš viršaus teigiamas, 0 - tiesiai į priekį), ir jo patrankos kampas, palyginti su korpusu (laipsniais, aukštyn teigiamas); `turrets` - kiekvienas technikos bokštelis kaip `yaw pitch;yaw pitch;...` jo paties eilės tvarka (nenaudojamas lizdas rodo `0.00 0.00`). Tankai, SPAA, APC ir sunkvežimiai, kliento ir serverio įrašuose; ne laivai (žr. [Bokšteliai](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | pagrindinis bokštelis, kaip jį siunčia įrašas; `turretYaw` / `gunPitch` - tai jis, sulaikytas iki bokštelio pavaros greičio ir nustatytas į kiekvieno pagrindinės patrankos šūvio liniją (žr. [Bokšteliai](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | kur žaidėjas žiūri (taikosi su kamera) pasaulyje: kompaso laipsniai (0 - šiaurė, pagal laikrodžio rodyklę) ir laipsniai aukštyn, ta pati konvencija kaip `aimHeading` / `aimPitch` (skirtingai nei `turretYaw` / `gunPitch`, kurie lieka santykiniai su korpusu). Kiekvieno žaidėjo tankas serverio įraše, įrašantį žaidėją - jo paties kliento įraše; ten, kur žaidėjas nieko netaiko (visi keturi taikymo plaukiantieji 0), tuščia. Bokštelis seka jį savo posūkio greičiu, todėl jie skiriasi, kol sukasi (žr. [Bokšteliai](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | įrašantį žaidėją tankas: kur jis taikosi (kompaso laipsniai, laipsniai aukštyn, atstumas m; 2000, kai taikiklyje nieko nėra); kameros eilutės: kur žaidėjas taikosi (kryptis, kėlimas) |
| `zoom` | kameros eilutės: kameros padidinimas (žr. [Kamera](ground.md#the-camera)) |
| `difficulty`, `gameMode` | mūšio `AB`, `RB` arba `SB`, ir `ground`, `air` arba `naval`, kiekvienoje eilutėje (žr. [Mūšio režimas](ground.md#battle-mode)) |
| `extrapolated` | orlaivio pavyzdys, kuris yra kliento nuvažiavimas, o ne gauta būsena (žr. [Įvertinimas pagal nuvažiavimą](aircraft.md#dead-reckoning-and-the-smoother)); bombos pavyzdys, apskaičiuotas nuo jos paleidimo (žr. Bombos be skrydžio įrašų [Kaip įrankis skaito įrašą](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | kiek glotnintuvas perkėlė pavyzdį (m), ir paties įrašo pozicija bei orientacija (posūkis lentelės ženklu) |
| `targetX`, `targetY`, `targetZ` | `shot` pataikymo taškas |
| `hitOutcome`, `hitFlags` | `shot` rezultatas sausumos vienete: `kill`, `critical`, `penetration` arba `nonpenetration` (atmesta ar sustabdyta: įrašas nepasako, kuris yra rikošetas), iš bitų, kuriuos serveris siunčia su pataikymu (`hitFlags`, neapdorota); tuščia, kai nieko nesiunčiama (orlaiviai, laivai). Žr. [Pataikymo rezultatai](hits.md#hit-outcomes) |
| `hitShell` | `shot` sviedinio parašas: keturi pataikymo pranešimo baitai (neapdorotas šešioliktainis); vienas parašas gali reikšti skirtingus sviedinius (120 ir 125 mm APFSDS turi bendrą), todėl jis saugomas neapdorotas, o ne skaitomas kaip kalibras |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | `shot` šaudmenys: jų tipas (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) ir id (`125mm_3bm46`), kai nužudymas nurodo šaulio lizdą, kitu atveju `explosive` (pataikymo sprogimas) arba `kinetic`; patrankos `weapon/slot` iš jos perkrovimų; kalibras mm iš diegimo ginklų failų. Žr. [Pataikymo rezultatai](hits.md#hit-outcomes) |
| `rpm` | orlaivio variklio sūkiai (vidurkis per jo variklius), kaip paskutinį kartą siųsta, per 2 s |
| `vx`, `vy`, `vz` | orlaivio greitis, kaip jį siunčia jo skrydžio įrašas (m/s, žaidimo ašys; greičiai virš 500 m/s rodomi kaip 500) |
| `engine`, `afterburner`, `engineCondition` | orlaivio varikliai iš jo skrydžio įrašo: `off`, `starting`, `running`, `dead` (`/`-jungti, kai jo varikliai skiriasi); degiklis 0-1; baitas, siunčiamas tik po to, kai variklis buvo pataikytas |
| `weaponName` | nužudymai ir mirtys: ginklas ar šaudmenys jūsų diegimo angliškai (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | tik įrašančiojo žaidėjo orlaivis: droselis 0-1,1 iš jo kabinos (1,1 - karo avarinė galia ar degiklis; kitu atveju jo skrydžio įrašo penkioliktosios dalys), valdikliai -1..1 iš jo skrydžio įrašo (aukštumos valdiklis teigiamas traukiant, posūkio valdiklis teigiamas, sukant į dešinę), likę šoviniai pagal ginklą (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | tik įrašančiojo žaidėjo orlaivis, iš jo kabinos: indikuotas oro greitis ir kilimo greitis (m/s), kuras, įleidimo vamzdžio slėgis (atm), važiuoklė (0-1, 1 - nuleista), alyvos ir cilindrų galvutės temperatūra, kur kabina turi tą rodyklę |
| `speed` | m/s per maždaug dvi trajektorijos sekundes (apskaičiuota čia; įrašas kitiems vienetams greičio nesiunčia) |
| `alive` | 0 vieneto pavyzdžiams po jo mirties (jo griuvėsiams): sausumos vieneto ar laivo - kol žaidimas jį pašalina arba baigiasi jo pavyzdžiai, orlaivio - ne ilgiau kaip 60 s |
| `otherVehicle`, `otherLife` | `shot` auka: jos technika ir jos `life` |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | `shot` pataikymo taškas aukos paties rėmelyje (m; x - pirmyn, y - aukštyn, z - kairėn; žr. [Pranešimai vienetams](how-it-reads.md#messages-to-units)) ir kaip šūvis atskrido, pasukta į tą rėmelį pagal aukos orientaciją tuo metu |
| `hitPart`, `hitFlag` | `shot` pataikymo pranešimas: jo dalies žodis, kaip jis siųstas, ir jo aukštesnysis baitas |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | kiek mūšis kainavo ir uždirbo ir kas laimėjo: žr. [Ekonomika](economy.md) |
| `other`, `weapon` | nužudymai: kita pusė ir ginklas; pataikymai: kas pataikė (iš įrašo uid, kitu atveju iš žaidėjo lizdo), jų technika; paleidimai: ginklas; sunaikinti moduliai: kas paskutinis pataikė į vienetą per 5 s prieš tai, ir `part <n>` |

---

Dalis [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Šaltinis: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
