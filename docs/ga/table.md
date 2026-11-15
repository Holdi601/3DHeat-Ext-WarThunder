---
title: An tábla
nav_order: 6
lang: "ga"
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# An tábla {#the-table}

![Tábla athsheinm sintéisigh, achoimrithe](../assets/img/table.svg)

Sraith amháin do gach sampla nó imeacht, 105 colún ([Liosta colún](../columns.md), ginte ón gcód); sa bhuntásc, faoi `heat3d`, treoracha léitheoireachta an amharcáin, mar sin ní gá d'fhoirm ar bith a líonadh don amharcán.

| Colún | Cad é |
|---|---|
| `time` | soicindí ar chlog féin na hathsheinme |
| `event` | `position`; luíonn sraitheanna imeachta ar an rian ag a n-nóiméad (idir dhá shampla, ar an líne eatarthu); `kill` (ag an marfóir), `death` (ag an íobartach), `hit_critical` / `hit_severe` (ag an aonad a bualadh), `module_destroyed` (ag an aonad), `launch` (ag an aonad a scaoil arm), `impact` (sampla deiridh arm nuair a baineadh é díreach ina dhiaidh); `explosion` agus `flak` (0xD08E, 0xD01F) ag a suíomh, cineál `effect`, gan rian, le treo an phléasctha nuair atá ceann aige; `shot` (teilgeán a bhuail, ag an lámhachóir), `gun_shot`, `fire_start`, `fire_stop` (pléasc ghunna, ní feithicil trí thine), `fire_on`, `fire_off` (feithicil trí thine, féach [Tinte feithiclí](hits.md#vehicle-fires)), `reward` (Silver Lions agus pointí taighde a thuill, féach [Geilleagar](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (féach [Teachtaireachtaí chuig aonaid](how-it-reads.md#messages-to-units)); `despawn`: an tsraith dheireanach de rian a bhfuil a aonad imithe sula gcríochnaíonn an athsheinm (féach [Deireadh rian](ground.md#end-of-a-track)) |
| `track` | an rud a tharraingíonn an t-amharcán mar rud amháin: saol amháin aonaid, nó eitilt arm amháin - `<player or vehicle> #<hex>` (taispeánann an t-amharcán an t-ainm gan an chuid `#`) |
| `x`, `y`, `z` | méadair an chluiche: x soir, y suas, z ó thuaidh (scáthánaíonn na leideanna z, mar sin ní tharraingítear an tuaisceart ó dheas) |
| `player` | ainm an imreora; aonad AI `<VehicleName> #<uid>` (mar shampla `F-15A #204`); `uid <n>` nuair nach ainmníonn aon rud é; d'arm, an té a scaoil é |
| `userId`, `team` | id Gaijin an imreora agus an fhoireann (`1`, `2`) |
| `ai`, `isPlayer` | `ai` fíor do gach aonad nach dtiomáineann cuntas imreora (aonaid mhisin, aerárthaigh AI, spriocanna talún, gunnaí frith-aeir, longa gan imreoir, áitchoinneálaithe), `isPlayer` a mhalairt: is imreoir é aonad a n-ainmníonn a eintiteas sliotán imreora le hid Gaijin. Tá an chuid dá lainseálaí ag arm; folamh nuair nach eol é |
| `match` | id an chluiche (`match` na cáipéise cluiche), ar gach sraith; mapálann na leideanna é mar an seisiún, mar sin ní cheanglaíonn dhá athsheinm luchtaithe rianta choíche |
| `life` | `uid#n`: rian aonaid amháin, gearrtha nuair a théann an uid go haonad eile, nuair a ghluaiseann an t-aonad níos tapúla ná mar is féidir leis (athspraoi, athfhorlíonadh, an cluiche á bhogadh, an cliant ag ceartú aonaid i bhfad uaidh; féach Teleports in [Conas a léann sé athsheinm](how-it-reads.md#what-is-read-and-the-check)) nó nach bhfeictear ar feadh i bhfad é; `w<hex>` eitilt arm (`w<hex>#n` tar éis gearradh) |
| `uid` | id an aonaid san athsheinm |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (tram nó vaigín iarnróid a chuireann an leibhéal, féach [Aonaid radhairc](objectives.md#scene-units-trams-and-rail-wagons)); airm `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` ceamara athsheinme an imreora taifeadta (féach [An ceamara](ground.md#the-camera)) |
| `type` | cineál an chluiche féin nuair a ainmníonn na torthaí é (`fighter`, `assault`, `destroyer`, `gun_boat`), nó mar `kind` ar shlí eile |
| `Vehicle` | id feithicle an chluiche (`f_15a`, `germ_flakpz_I_Gepard`), a mheaitseálann figiúirí an amharcáin |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | ainm Béarla na feithicle ó logánú do shuiteála (`Pz.Kpfw. III Ausf. J1`, gearr `Pz.III J1`) agus a heochair (`germ_pzkpfw_III_ausf_J_0`); fágtar comharthaí tíre chló an chluiche ar lár. Nuair nach n-ainmníonn an cluiche aon rud, nó nuair nach bhfaightear aon suiteáil, is é an id an t-ainm agus an eochair folamh |
| `mission` | ainm an aonaid sa mhisean (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | an áit a dtreoraíonn an t-aonad (veicteoir na súl): aerárthaigh ó dhearcadh an mhúnla eitilte, aonaid talún agus longa ó dhearcadh féin, airm feadh a n-eitilte |
| `heading`, `pitch`, `roll` | an rud céanna i gcéimeanna; is é `heading` an compás, deiseal ó thuaidh, pitch srón suas dearfach, roll sciathán deas síos dearfach (seolann an múnla eitilte an tsraith eile, féach [Dearcadh, seiceáilte](aircraft.md#attitude-checked); taobh deas aonaid talún síos). Deir na leideanna é faoi `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | príomhthuirlingt tanc - an áit a dtreoraíonn an gunna, ní an áit a bhféachann a imreoir; luach na hathsheinme coinnithe ag luas tiomána na tuirlinge agus socraithe ar líne gach seat den phríomhghunna (féach [Tuirlingtí](ground.md#turrets)): a yaw i gcoibhneas leis an gcorp (céimeanna, deiseal ó thuas dearfach, 0 díreach romhat) agus pitch a ghunna i gcoibhneas leis an gcorp (céimeanna, suas dearfach); `turrets` gach tuirlingt den fheithicil mar `yaw pitch;yaw pitch;...` ina hord féin (léitear sliotán gan úsáid mar `0.00 0.00`). Tancanna, SPAA, APCanna agus trucailí, in athsheinmeanna cliaint agus freastalaí; ní longa (féach [Tuirlingtí](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | an phríomhthuirlingt mar a sheolann an athsheinm í; is é `turretYaw` / `gunPitch` í coinnithe ag luas tiomána na tuirlinge agus socraithe ar líne gach seat den phríomhghunna (féach [Tuirlingtí](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | an áit a bhféachann an t-imreoir (díríonn leis an gceamara) sa saol: céimeanna compáis (0 ó thuaidh, deiseal) agus céimeanna suas, an coinbhinsiún céanna le `aimHeading` / `aimPitch` (murab ionann agus `turretYaw` / `gunPitch`, a fhanann i gcoibhneas leis an gcorp). Tanc gach imreora in athsheinm freastalaí, tanc an imreora taifeadta féin in athsheinm cliaint; folamh nuair nach ndíríonn an t-imreoir áit ar bith (na ceithre shnámhán aim ar fad 0). Leanann an tuirlingt é ag a luas trasnaithe féin, mar sin bíonn an dá cheann difriúil agus í ag casadh (féach [Tuirlingtí](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | tanc an imreora taifeadta féin: an áit a ndíríonn sé (céimeanna compáis, céimeanna suas, an fad i m; 2000 nuair nach bhfuil aon rud sa radharc); sraitheanna ceamara: an áit a ndíríonn an t-imreoir (heading, pitch) |
| `zoom` | sraitheanna ceamara: formhéadú an cheamara (féach [An ceamara](ground.md#the-camera)) |
| `difficulty`, `gameMode` | `AB`, `RB` nó `SB` an chatha, agus `ground`, `air` nó `naval`, ar gach sraith (féach [Mód catha](ground.md#battle-mode)) |
| `extrapolated` | sampla aerárthaigh is dead reckoning an chliaint é, ní stát a fuarthas (féach [Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)); sampla buama a ríomhadh óna scaoileadh (féach Bombs without flight records in [Conas a léann sé athsheinm](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | cé chomh fada a bhog an mhínitheoir an sampla (m), agus suíomh agus dearcadh féin na hathsheinme (roll i gcomhartha an tábla) |
| `targetX`, `targetY`, `targetZ` | pointe buille `shot` |
| `hitOutcome`, `hitFlags` | toradh `shot` ar aonad talún: `kill`, `critical`, `penetration` nó `nonpenetration` (preabadh nó stoptha: ní insíonn an athsheinm ricochet óna chéile), ó na bitéanna a sheolann an freastalaí leis an mbuille (`hitFlags`, amh); folamh nuair nach seoltar aon cheann (aerárthaigh, longa). Féach [Torthaí buillí](hits.md#hit-outcomes) |
| `hitShell` | síniú sliogáin `shot`: ceithre bheart de theachtaireacht an bhuille (heics amh); is féidir le síniú amháin sliogáin éagsúla a léiriú (roinneann APFSDS 120 agus 125 mm ceann), mar sin coinnítear amh é, ní léitear mar chaighdeán é |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | lón catha `shot`: a chineál (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) agus id (`125mm_3bm46`) nuair a ainmníonn marú sliotán an lámhachóra, nó `explosive` (an pléasc bhuille) nó `kinetic` ar shlí eile; `weapon/slot` an ghunna óna athluchtuithe; an caighdeán i mm ó chomhaid arm na suiteála. Féach [Torthaí buillí](hits.md#hit-outcomes) |
| `rpm` | rpm inneall aerárthaigh (an meán thar a innill) mar a seoladh go deireanach, laistigh de 2 s |
| `vx`, `vy`, `vz` | treoluas aerárthaigh mar a sheolann a iontráil eitilte é (m/s, aiseanna an chluiche; léitear luasanna os cionn 500 m/s mar 500) |
| `engine`, `afterburner`, `engineCondition` | innill aerárthaigh óna iontráil eitilte: `off`, `starting`, `running`, `dead` (nasctha le `/` nuair a bhíonn a innill difriúil); an tar-dóite 0-1; beart a sheoltar ach tar éis an t-inneall a bhualadh |
| `weaponName` | maruithe agus básanna: an t-arm nó an lón catha i mBéarla do shuiteála (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | aerárthach an imreora taifeadta amháin: an sprocaire 0-1.1 óna chábán (1.1 cumhacht éigeandála cogaidh nó tar-dóite; nó cúig cinn déag a iontrála eitilte), na rialuithe -1..1 óna iontráil eitilte (elevator dearfach ag tarraingt, aileron dearfach ag rolladh ar dheis), na babhtaí fágtha in aghaidh an airm (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | aerárthach an imreora taifeadta amháin, óna chábán: aer-luas léirithe agus ráta dreapadh (m/s), breosla, brú iomadúcháin (atm), gear (0-1, 1 síos), teocht ola agus ceann sorcóra, nuair atá an tomhaiseán ag a chábán |
| `speed` | m/s thar thart ar dhá shoicind den rian (ríofa anseo; ní sheolann an athsheinm aon luas d'aonaid eile) |
| `alive` | 0 do shamplaí aonaid tar éis a bháis (a raic): aonad talún nó long go dtí go mbaineann an cluiche é nó go dtagann deireadh lena shamplaí, aerárthach ar feadh 60 s ar a mhéad |
| `otherVehicle`, `otherLife` | íobartach `shot`: a fheithicil agus a `life` |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | pointe buille `shot` i bhfráma féin an íobartaigh (m; x ar aghaidh, y suas, z ar chlé; féach [Teachtaireachtaí chuig aonaid](how-it-reads.md#messages-to-units)) agus an bealach a tháinig an lámhaigh, iompaithe isteach sa fhráma sin ag dearcadh an íobartaigh ansin |
| `hitPart`, `hitFlag` | teachtaireacht bhuille `shot`: a focal páirte mar a seoladh é, agus a ard-bheart |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | an méid a chosain agus a thuill an cath, agus cé a bhuaigh: féach [Geilleagar](economy.md) |
| `other`, `weapon` | maruithe: an taobh eile agus an t-arm; buillí: cé a bhuail (ó uid an taifid, nó ó a shliotán imreora), a bhfeithicil; scaoileadh: an t-arm; modúil scriosta: cé a bhuail an t-aonad go deireanach laistigh de 5 s roimhe sin, agus `part <n>` |

---

Cuid de [3DHeat](https://github.com/Holdi601/3DHeat) ([doiciméadúchán](https://holdi601.github.io/3DHeat/)). Foinse: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
