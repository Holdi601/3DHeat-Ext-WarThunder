---
title: Buillí, tine ghunnaí agus tinte
nav_order: 13
lang: "ga"
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Buillí, tine ghunnaí agus tinte {#hits-gunfire-and-fires}

Do léitheoirí ar mhaith leo a fháil amach cá dtagann na colúin bhuillí, lón catha agus tinte astu. Ní thugann seiceálacha ach an modh agus an comhaontú.

## Tine ghunnaí {#gunfire}

Tá gach teilgeán a bhuail aonad san athsheinm (teachtaireacht 0xF0E9): sraith `shot` ag suíomh an lámhachóra ag nóiméad an bhuille, `targetX/Y/Z` pointe an bhuille (an t-aonad a bualadh, bogtha ag pointe an bhuille ina fhráma, casta ag a dhearcadh), an treo ina threo, `other` an t-aonad a bualadh. Ní sheoltar sliogáin agus piléir a chaill: ní eintitis iad, agus ní choinníonn na teachtaireachtaí airm ag eitilt ach roicéid, diúracáin, buamaí agus torpéidí. Titeann babhtaí fágtha an imreora taifeadta (a cholún `ammo`) agus é ag lámhach, mar sin is féidir a phléasca a aithint, ach ní cá ndeachaigh na babhtaí sin. Seolann gunnaí frith-aeir troma agus airtléire gach lámhaigh aonair (`gun_shot`, gan treo), gunnaí frith-aeir 40 mm a bpléasca (`fire_start`, `fire_stop`).

## Torthaí buillí {#hit-outcomes}

Le gach buille teilgin ar aonad talún seolann an freastalaí teachtaireacht 0xF144 (UnitOnHit) chuig an aonad: ceithre réimse haon-bheart, an ceathrú ina bhitéanna den rud a rinne an buille (`selfCheck.unitMessages.outcome_*`):

| Bit | Brí | Fianaise |
|---|---|---|
| 0x20 | buille teilgin féin | tagann beagnach gach ceann le buille 0xF0E9 ar an aonad laistigh de 5 ms; ar shlí eile, le pléasc (splancadh) |
| 0x01 | chuaigh sé tríd (treá) | tá sé ag gach teachtaireacht le 0x02, 0x04 nó 0x08 freisin |
| 0x02 | buille criticiúil | tá sé ag formhór na dtaifead buille criticiúil, i bhfad níos minice ná seans |
| 0x04 | scriosta | tagann formhór le taifead maruithe agus bás an aonaid laistigh de shoicind |
| 0x08 | damáiste trom | tá sé ag roinnt taifead buille criticiúil; annamh ar shlí eile |

Glacann `hitOutcome` an ceann is measa: `kill` (0x04), `critical` (0x02 nó 0x08), `penetration` (0x01), `nonpenetration` (0x20 amháin). Péireáiltear buille leis an 0xF144 neamhphéireáilte is gaire le 0x20 dá aonad laistigh de 5 ms. Insíonn ceamara buillí an chluiche ricochet ó neamhthreá, ach ní dhéanann aon bhit ná réimse a fuarthas anseo: athraíonn na chéad trí bheart ó bhuille go buille agus níl siad ar eolas. Ní sheolann athsheinmeanna cliaint 0xF144 ach d'aerárthach an imreora taifeadta féin, gach bit glan: níl aon toradh ag buillí aerárthaigh agus long.

## Lón catha {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Pléascach nó nach ea.** Seolann sliogán a phléascann 0xF133 (UnitOnExplosion) le uid an lámhachóra agus uimhir an bhuille; is `explosive` buille leis, `kinetic` an chuid eile.
* **An gunna agus a shliotán.** Is é 0xF0BD (UnitBulletRearm) an chéad bhabhta eile luchtaithe: innéacs an airm i liosta arm na feithicle, an sliotán lón catha agus na babhtaí fágtha. Tagann ceann luchtaitheora láimhe am athluchtaithe seasta tar éis gach ceann dá bhuillí, ceann autocannon cuid de shoicind ina dhiaidh. Grúpáiltear buillí lámhachóra de réir feithicle, sínithe agus pléasc; is arm grúpa nuair a luchtaíonn an t-arm sin babhta laistigh de 20 s tar éis leath a bhuillí nó níos mó ag moill sheasta. Is é `ammoSlot` `weapon/slot`, an sliotán a luchtaíodh roimh an mbuille: is dócha an ceann a lámhachadh, mura bhfuil lón catha athraithe ag an imreoir idir an dá linn. Ní sheolann gunnaí meaisín 0xF0BD.
* **An sliogán.** Is é arm marú id an tsligéin (`125mm_3bm46`); tugann buille deireanach an mharfóra ar an íobartach é do shliotán an lámhachóra sin, nuair a aontaíonn caighdeán an ghunna. Is iad a chineál agus a chaighdeán na gcinn de chuid an chomhaid airm (`bulletName`, `bulletType`, `caliber`; `apds_fs_*` APFSDS, `heat_fs_*` HEAT-FS, `he_*` HE ...).
* **An caighdeán** den chuid eile: caighdeán airm an tsliotáin; caighdeán an ghunna mheaisín amháin is féidir lena shíniú a bheith ag grúpa gunna meaisín; ar shlí eile caighdeán phríomhghunna na feithicle. Gan an tsuiteáil (`--game`) níl aon chineál, ainm ná caighdeán thar `explosive` / `kinetic`.

Gan aimsiú: ricochet. Iompraíonn roinnt teachtaireachtaí eile lámhachóir agus uimhir an bhuille (0xF0C2, is dócha cosán cheamara buillí tríd an bhfeithicil; 0xF117, 0xF13C, 0xF13E); coinnítear iad sa chomhad cliatháin, gan díchódú. Fanann neamhthreá `nonpenetration`.

## Tinte feithiclí {#vehicle-fires}

Taispeántar feithicil trí thine do gach cliant: seolann an freastalaí teachtaireacht eintitis chuig an bhfeithicil (imeacht `0a519c58`) a liostaíonn na tinte atá ag dó uirthi, gach uair a athraíonn an liosta. In aghaidh an tine: dhá id 16-bit (an dara ceann nód samhla damáiste), a cineál, agus -1 go dtí go dtógann an tine. Faigheann tine a las buille teachtaireacht freisin leis an bpointe ina ndóitear í, i bhfráma na feithicle (x ar aghaidh, y suas, z ar chlé).

Sraitheanna: `fire_on` nuair a thagann tine isteach sa liosta, `fire_off` nuair atá sí imithe, ag an bhfeithicil, le `fireId` (`first:node`), `fireKind` agus, do thinte a las buille, `fireLocalX/Y/Z` (ar aghaidh, suas, ar dheis). Nuair atá feithicil marbh ní sheoltar a liosta arís go minic: críochnaíonn a tinte lena raic, nó lena heintiteas, nó leis an athsheinm (`selfCheck.fires`).

Seiceáilte: gach uair a thit líon múchtóirí tine tanc, d'fhág tine a liosta laistigh de chuid de shoicind; luíonn formhór pointí tine ar an taobh céanna den fheithicil leis an mbuille a las iad. Is uimhreacha na cineálacha; níl a fhios cad a ainmníonn siad, ná cén chuid is nód ann. Ní sheolann aerárthaigh aon liosta mar sin: ní léitear aerárthach trí thine.

---

Cuid de [3DHeat](https://github.com/Holdi601/3DHeat) ([doiciméadúchán](https://holdi601.github.io/3DHeat/)). Foinse: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
