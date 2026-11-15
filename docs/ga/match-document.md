---
title: An cháipéis chluiche
nav_order: 7
lang: ga
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# An cháipéis chluiche {#the-match-document}

![Tús cáipéise cluiche sintéisigh, agus a heochracha](../assets/img/match-document.svg)

Coinníonn `<match>.match.json` gach rud a deir an athsheinm nach sraith den tábla é. Léann cluaisín Cluiche an amharcáin é.

## An cath {#the-battle}

| Eochair | Cad é |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | id an chluiche (mar atá in ainm an chomhaid); id na léarscáile; an comhad leibhéil a úsáideann sé |
| `mission`, `missionKey` | ainm an mhisin agus a eochair i gcomhaid téacs an chluiche |
| `battleClass`, `environment`, `weather` | mar a thugann an ceanntásc iad |
| `sessionId`, `server` | id seisiúin an chatha; an freastalaí |
| `replayVersion`, `flightLayout` | leagan fhormáid na hathsheinme; leagan amach an phaicéid eitilte a léadh (`2025` nó `2026`) |
| `files` | na comhaid athsheinme a léadh (ceann amháin, nó codanna athsheinm freastalaí) |
| `started`, `timePlayed`, `replayEnd` | am tosaigh (ISO, UTC); soicindí imeartha, ó na torthaí; soicindí an phaicéid dheireanaigh den athsheinm |
| `author`, `authorUserId` | an t-imreoir taifeadta agus a id Gaijin (athsheinmeanna cliaint) |
| `teams` | na foirne sa chath (`1`, `2`) |
| `result` | `winner`, `status` (`success` nó `fail`, toradh an údair), `authorTeam`, `teams` ([Geilleagar](economy.md)) |
| `vehicleNames` | cá as a tháinig ainmneacha na bhfeithiclí (do shuiteáil) agus a dteanga |
| `conventions` | aonaid agus comharthaí an tábla: aiseanna, am, life, track, alive, roll, agus níos mó |

## Gach rud eile {#everything-else}


| Eochair | Cad é |
|---|---|
| `battle`, `difficulty`, `gameMode` | mód an chatha: `difficulty` `AB` / `RB` / `SB` (agus a ainm, agus beart an cheanntáisc), `gameMode` `ground` / `air` / `naval`, mód an mhisin (`Dom`, `Conq`, `Bttl`, `I2M`, ...) agus a ainm Béarla ó do shuiteáil (`Domination`, `Enduring Confrontation`), na cineálacha aonad a cheadaítear (féach [Mód catha](ground.md#battle-mode)) |
| `settings` | blk an mhisin tar éis an cheanntáisc: mód, timpeallacht, aimsir, teorainneacha scóir agus ama, tíortha, cineálacha aonad ceadaithe, gaoth, agus `stars` (domhanleithead, domhanfhad, dáta, am áitiúil) |
| `sky` | an chéad `CustomWeatherParams`: treo na gréine agus na gealaí, gaoth, dathanna spéire, díorthaigh scamall |
| `players`, `slots` | líne na dtorthaí do gach imreoir (maruithe, maruithe talún, básanna, cúnaimh, scór, gabhálacha, scuad, clan, tír, line-up, na uids a thiomáin siad); sliotáin imreoirí na hathsheinme (ainm, id úsáideora, foireann) |
| `units` | gach eintiteas aonaid a chruthaigh an athsheinm: eid, uid, teimpléad, feithicil, kind, type, foireann, imreoir, ainm misin, cathain a cruthaíodh agus a baineadh é, cá háit a cruthaíodh é, cé na comhpháirteanna nárbh fhéidir a léamh |
| `objects` | réada ainmnithe an mhisin: criosanna gabhála agus aerpháirceanna lena suíomh agus méid, imlínte aerpháirceanna mar phointí, limistéir spraoi |
| `objectives` | cuspóirí an chatha, gach `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (1 nó 2 na hathsheinme, folamh don dá cheann), `name` (litir crios gabhála, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) le `position`, `radius` / `height` / `size` agus `heading`, `source` (`replay` nó `mission`) agus cad eile atá ar eolas (féach [Cuspóirí](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | le hainmneacha agus feithiclí an dá thaobh; maruithe le hainm Béarla an airm |
| `weapons` | gach roicéad, diúracán, buama, torpéido, umar titim agus ualach caite: cathain, cá scaoileadh (suíomh, dearcadh, treoluas), ag cén aonad (an ceann is gaire laistigh de 300 m agus 1.5 s), cé mhéad sampla eitilte, cá bhfacthas go deireanach é, cathain a baineadh é |
| `explosions`, `flak` | `PlayExplosionVisual` (suíomh, treo, kind) agus `PlayFlakExplosionVisual` (suíomh) |
| `awards` | dámhachtainí an imreora taifeadta (`TextStreak`: first_blood, streaks, comhairleoirí dúshláin) |
| `detections`, `unitStates` | péirí `UnitDetected` d'aonaid; teachtaireacht (0xF093) le suíomh, dearcadh agus treoluas aonaid nach eol a bhrí |
| `authorInstruments` | luachanna cábáin an imreora taifeadta (`ReplayCockpitParams`) de réir uimhir uirlise, ceann amháin ar a mhéad in aghaidh an tsoicind; ainmníonn `known` gach uimhir a sheol an athsheinm seo (ainm, aonad, conas a seiceáladh é), `notNamed` an chuid eile |
| `scoreboard` | staitisticí gach imreora gach uair a d'athraigh siad (maruithe, básanna, cúnaimh, scór, maruithe ai, maruithe cabhlaigh, criosanna, damáiste, seachaintí diúracán, scuad), agus scór agus ticéid dhóchúla gach foirne le himeacht ama (féach [Sonraí machnaimh](aircraft.md#reflection-data)) |
| `economy` | Silver Lions agus pointí taighde an chatha (féach [Geilleagar](economy.md)): iomláin, in aghaidh an imreora, in aghaidh na feithicle, na hiolraitheoirí, an buaiteoir, na seiceálacha |
| `entityMessages` | na teachtaireachtaí eintitis (0x20) de réir uimhir ranga: líon, teimpléid sprice, méideanna |
| `chat` | gach líne comhrá |
| `triggers`, `hints`, `missionProgress` | gníomhartha script an mhisin (RunTriggerAction), a leideanna, a theachtaireachtaí dul chun cinn |
| `camera` | réimsí cheamara athsheinme an imreora taifeadta gach 0.25 s mar a seoladh iad (tá sé ag an tábla mar rian) |
| `projectileHitReplays` | buillí an imreora taifeadta féin agus é á bhualadh, le hairm agus lón catha agus a n-ainmneacha Béarla |
| `results` | an blk torthaí ar fad mar a scríobh an cluiche é |
| `counts` | sraitheanna, imeachtaí, lives, kinds, samplaí, eintitis de réir teimpléid, airm, paicéid léite agus nár léadh, gach id teachtaireachta a chonacthas agus iad nár léadh, samplaí a thit |
| `trackBreaks` | gach gearradh rian le haghaidh céim níos tapúla ná mar is féidir leis an aonad dul: cá háit, cé chomh fada, cé chomh tapa, agus cad is dóichí é |
| `selfCheck` | na seiceálacha atá liostaithe in [Conas a léann sé athsheinm](how-it-reads.md), ríofa ar gach tiontú; tugann `stepSpeed` de réir kind an luas idir sraitheanna as a chéile de rian mar a cheanglaíonn an t-amharcán iad (airmheán, 99ú ceatadán, an ceann is airde, agus céimeanna níos tapúla ná is féidir, ar gá 0 a bheith ann) |

---

Cuid de [3DHeat](https://github.com/Holdi601/3DHeat) ([doiciméadúchán](https://holdi601.github.io/3DHeat/)). Foinse: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
