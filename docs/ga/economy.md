---
title: Geilleagar
nav_order: 14
lang: ga
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Geilleagar {#economy}

An méid a chosain agus a thuill an cath, mar cholúin ar a shraitheanna imeachta, léite ó **do shuiteáil tráth an tiontaithe** (`char.vromfs.bin`: `config/wpcost.blk` do gach feithicil, `config/warpoints.blk` agus `config/rank.blk`; deir blks arm `aces.vromfs.bin` cén módúchán é gach sliogán). Níl aon uimhir de chuid an chluiche sa stóras seo: téann na luachanna isteach i d'aschur féin amháin. Gan `char.vromfs.bin` na suiteála ní scríobhtar aon gheilleagar (`economy.available` bréagach). Is iad na praghsanna sin deacracht an chatha (`repairCostHistorical` do RB, `...Arcade` AB, `...Simulation` SB).

| Colún | Sraitheanna | Cad é |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (babhta a tógadh tar éis lámhaigh, feithiclí talún), `launch` (aerárthaigh, héileacaptair) | SL a chosain an babhta, an roicéad, an diúracán nó an buama |
| `cost_lost_sl` | `death` feithicle imreora | costas deisithe na feithicle (stock; an ceann uasghrádaithe go hiomlán sa bhloc) |
| `earn_sl`, `earn_rp` | `reward` (imeacht nua, in áit agus am an tuilleora) | SL agus RP a thuill |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | gach sraith le `cost_*` nó `earn_sl` | `SL` (is pointí taighde é `earn_rp`) |
| `econ_basis` | an rud céanna | `install` (praghas léite ón suiteáil) nó `inferred` (ríofa, thíos) |

**Cé a bhuaigh.** `won` (0/1) ar gach sraith d'fhoireann, nuair a deir an athsheinm é: iompraíonn torthaí athsheinme cliaint toradh an údair féin (`status`: `success` nó `fail`), mar sin bhuaigh nó chaill foireann an údair agus an fhoireann eile a mhalairt; deir `result` sa cháipéis chluiche cé acu (`winner`, `status`, `authorTeam`). Ní iompraíonn athsheinmeanna freastalaí agus athsheinmeanna a fágadh roimh an deireadh aon toradh (bíonn `status` athsheinme freastalaí i gcónaí `success` agus ní ainmníonn sé aon údar), agus ní choinníonn aon chineál acu módúcháin suiteáilte: liostaíonn na torthaí feithiclí gach imreora de réir ainm agus cineál amháin. Ansin fanann `won` folamh.

Léann samhail costais na faire na colúin `cost_*` (agus `earn_*`) le `currency`; tugann suimiú `cost_fired_sl + cost_lost_sl` an áit ar caitheadh agus ar cailleadh Silver Lions, `earn_sl` an áit ar thuill siad (tá luach saothair maruithe ar a shraith `reward`, ní ar an tsraith `kill`, mar sin ní chomhairítear aon rud faoi dhó).

- **Babhtaí** (`install` nuair is eol sliogán an tsliotáin - d'ainmnigh marú é, féach [Torthaí buillí](hits.md#hit-outcomes) - nó `inferred`: meánphraghas na sliogán a fhéadann an gunna sin a lámhach ar an bhfeithicil sin; saor in aisce is ea sliogán stock; ní chomhairíonn an athsheinm gunnaí meaisín agus ní chosnaíonn siad faic).
- **Scaoileadh** (`inferred`): praghsálann an cluiche réamhshocrú arm aerárthaigh in aghaidh an sortie, ní in aghaidh míre; is é mír amháin an airmheán thar réamhshocruithe praghsáilte na feithicle de phraghas / míreanna (`sum_weapons`, frithbhearta agus umair titim fágtha ar lár); 0 nuair atá a réamhshocruithe saor in aisce.
- **Luach saothair** (`inferred` ar fad): níl aon taifead luach saothair san athsheinm - níl sa bhloc torthaí ach scóir agus comhaireamh, ní iompraíonn aon teachtaireacht Silver Lions (seiceáilte ar athsheinmeanna cliaint agus freastalaí). Tuilleann `kill` `aKill` x `rewardMul<mode>` an mharfóra x meáchan aicme an íobartaigh (`units` i warpoints.blk, de réir a `unitClass`; aonaid AI de réir a gcineáil) x `aiKillK` d'íobartach AI x `groundKillMul` d'aerárthach a mharaíonn aonad talún; RP mar an gcéanna le `expMul` agus meáchain rank.blk. Is luach saothair é gach céim eile de scór imreora sa scórchlár macasamhlaithe, fiúntach a phointí ag SL an chatha an pointe (SL maruithe thar airmheán pointí chéimeanna na maruithe, an `pointsPerKill` den bhloc); is é a chineál an cuntar a d'ardaigh leis (cúnaimh, criosanna gafa, damáiste crios, dámhachtain damáiste, seachaintí diúracán), nó buille criticiúil / trom an imreora sin laistigh de 3 s, nó aimsiú aonaid an imreora laistigh de 2 s (`scouting`), nó `other`. Is é `battle_end` `winK` (buaite) nó `defeatK` (caillte) de thuilleamh an imreora sa chath, an buaiteoir de réir ticéid na bhfoirne fágtha, ansin a scór. Ní fheictear am préimhe, borradh, criú ná módúcháin agus ní chuirtear i bhfeidhm iad; ní shamhlaítear buiséid mharaithe na gcathanna talún (`def_ground_kill_wp_budget*`).

Coinníonn `economy` na cáipéise cluiche (agus, i gcoimeádán `.3dheat`, `extensions["heat3d/economy"]` an mhainifest) `currency` `SL`, `researchCurrency` `RP`, `difficulty`, `totals` (`firedSl`, `lostSl`, `earnedSl`, `earnedRp`), `players` (an rud céanna in aghaidh an imreora, le `netSl`), `vehicles` (in aghaidh feithicle imreora: `repairSl`, `repairFullUpgradedSl`, `purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`, `rewardMul`, `expMul`, `groundKillMul`, `battleTimeAwardSl`, `rank`, `economicRank`, `unitClass`), `multipliers` (`aKill`, `aiKillK`, `winK`, `defeatK`, `wpMultiplier`), `winnerTeam`, `pointsPerKill` agus `check` (cé mhéad sraith de gach cineál a praghsáladh, a mheastar nó nár praghsáladh).

---

Cuid de [3DHeat](https://github.com/Holdi601/3DHeat) ([doiciméadúchán](https://holdi601.github.io/3DHeat/)). Foinse: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
