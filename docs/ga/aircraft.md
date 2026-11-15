---
title: Aerárthaigh
nav_order: 11
lang: ga
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Aerárthaigh {#aircraft}

Do léitheoirí ar mhaith leo a fháil amach cá dtagann na colúin aerárthaigh astu agus cé chomh mór is féidir muinín a bheith acu astu. Cuireann gach seiceáil thíos luach i gcomparáid le rud a deir an athsheinm an dara huair, ar bhealach neamhspleách; ní thugtar ach an modh agus an comhaontú.

## Uirlisí cábáin {#cockpit-instruments}

Seolann teachtaireacht 0xD04A tomhaiseáin an imreora taifeadta mar phéirí (uimhir, luach): ceithre cinn sa soicind i gcathanna arcáide, luachanna athraithe amháin i gcathanna insamhalta. Cruthaíonn na huimhreacha liosta amháin thar gach cábán, agus seolann cábán na tomhaiseáin atá ag a mhúnla. Socraíonn cód an chluiche cén uimhir cén tomhaiseán é, mar sin ainmníodh gach uimhir de réir a dhéanann sí agus seiceáladh i gcoinne na hathsheinme é (coinníonn `convert.INSTRUMENTS` an toradh; ní léitear aon rud ón suiteáil):

| Uimhir | Ainm | Seiceáilte i gcoinne |
|---|---|---|
| 0 | aer-luas léirithe, m/s | luas an rian ceartaithe do dhlús aeir: comhghaol 0.99 |
| 39 | ráta dreapadh, m/s | ráta dreapadh an rian: comhghaol os cionn 0.99 |
| 40, 41 | airde, m; airde modulo 1000 | airde an rian, cúpla méadar óna chéile |
| 52, 53 | roll agus pitch na spéirlíne shaorga | lúide roll agus pitch an tábla, faoi bhun 1 chéim óna chéile |
| 64 | compás | heading an tábla, faoi bhun 0.1 chéim óna chéile |
| 15-20 | troitheáin rudair | an fórsa taobh ar an aerárthach |
| 23, 31 | maide: elevator agus ailerons (comhartha mar a mhúnla cábáin) | uillinn ionsaithe; ráta roll |
| 69, 71, 73 | clog: uaireanta (aghaidh 12 uair), nóiméid, soicindí | am áitiúil an ríomhaire taifeadta, go dtí an nóiméad |
| 75 | brú iomadúcháin, atm | níos airde ag cumhacht éigeandála cogaidh ná ag sprocaire iomlán |
| 81-86, 87-92, 93-98 | rpm in aghaidh an innill, rpm modulo 1000, tomhaiseán rpm | a chéile go beacht; rpm an innill: comhghaol os cionn 0.97 |
| 195 | breosla | titeann i rith sortie, lán arís ag athspraoi |
| 228-230 | cosa na gcosa tuirlingthe, 1 síos | síos in aice le hairde na n-aerpháirceanna agus ag luas tuirlingthe amháin |
| 240, 241 | sprocaire in aghaidh an innill (1.1 cumhacht éigeandála cogaidh nó tar-dóite) | sprocaire iontráil eitilte |
| 330-332, 346-348 | cuntair lón catha (dhá thacar cothrom) | babhtaí an réamhshocraithe airm, ag titim le babhtaí na hiontrála eitilte |
| 135, 159 | teocht ola agus ceann sorcóra | dóchúil: ardaíonn siad thar sortie |
| 58, 61 | liathróid sleamhnaithe, snáthaid chasta | dóchúil: leanann siad an fórsa taobh agus ráta an chasta |
| 223 | brat aeir | dóchúil: socraithe ag druidim amháin |
| 490-497, 500-505 | coscáin rothaí | dóchúil: socraithe ina seasamh ar aerpháirc amháin |

Seoltar cúpla uimhir eile nach eol a mbrí; coinnítear iad i `authorInstruments.notNamed` na cáipéise cluiche.

Tagann `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` agus `throttle` an tábla uathu, ar shraitheanna an imreora taifeadta féin, agus glactar an teachtaireacht dheireanach 0.2 s ar a mhéad tar éis an tsampla.

## Iontrálacha eitilte {#flight-entries}

Iompraíonn iontráil eitilte gach aerárthaigh (cineál paicéid 2), seachas a shuíomh agus a dhearcadh:

- **Treoluas**: focal 32-bit tar éis an dearcaidh. Is iad bitéanna 31, 30 agus 29 comharthaí x, y agus z; ansin an luas i 11 bhit de 500/2047 m/s (stopann sé ag 500 m/s), ansin |x| agus |y| mar chodáin den luas i 9 mbit an ceann, agus is é z an rud a fhágann gur veicteoir aonaid é an veicteoir. Seiceáilte i gcoinne an chéim idir samplaí a fuarthas: tá an treo ag teacht leis laistigh de chodán de chéim don imreoir taifeadta agus laistigh de thart ar 2 chéim do gach duine eile; an luas laistigh de 0.2 %. `selfCheck.flightEntries`.
- **Babhtaí in aghaidh an airm**: liosta roimh an suíomh, mír amháin in aghaidh an airm, na babhtaí fágtha ar dtús. Is ionann ceann an imreora taifeadta agus cuntair an chábáin tic ina dhiaidh sin do bheagnach gach sampla.
- **Rialuithe agus sprocaire**: 7 mbeart tar éis an treoluas, léite mar 14 nibble. Don imreoir taifeadta, gach tic: 1 an elevator, 2 na ailerons, 3 an rudar (8 ag an scíth), 11 an sprocaire i bpunanna cúig déag (15 freisin do chumhacht éigeandála cogaidh agus tar-dóite), 4 coscáin rothaí, 5 an brat aeir, 8 is dócha paraisiút coiscthe. Ní athraíonn nibbles aerárthach eile ach cúpla uair i gcath agus ní hiad a rialuithe ag an am.
- **Innill**: in aghaidh an innill beart staide (0 as; 1-6 ag tosú; 7 ag rith; 8 marbh), luach 16-bit le tar-dóite amháin (32767 lán), agus beart tar éis an t-inneall a bhualadh amháin. Maraítear formhór na n-aerárthach a bhfuil a n-inneall "marbh" nó críochnaíonn siad laistigh de nóiméid.

## Sonraí machnaimh {#reflection-data}

Macasamhlaíonn teachtaireachtaí 0xF02D agus 0xF0AA réada uimhrithe an chluiche: in aghaidh an réada a id (na 5 bhit is airde an cineál, na 11 is ísle innéacs) agus tábla réimsí. Is é cineál 14 sliotáin imreoirí (réimse 2 id úsáideora agus ainm, 9 an fhoireann), cineál 15 na foirne (innéacs 1 agus 2):

- Coinníonn réimse 39 sliotáin a staitisticí in áiteanna seasta: maruithe (fritháireamh 0), maruithe foirne (2), básanna (4), maruithe cabhlaigh (10), maruithe AI (12), maruithe talún AI (14), cúnaimh (20), criosanna gabhála (22), damáiste crios (24, 32-bit), dámhachtain damáiste (40, 32-bit), seachaintí diúracán (50). Tosaíonn réimse 38 leis an scór, is é réimse 42 an scuad. Ag deireadh catha is ionann gach luach agus na torthaí do gach imreoir (`selfCheck.scoreboardVsResults`). Níl a fhios cá gcoinnítear maruithe talún.
- Is é réimse 7 foirne a scór: ag an deireadh is ionann é agus suim scór a himreoirí sna torthaí. Is dócha gurb é réimse 3 a ticéid.
- Ní sheolann gach teachtaireacht ach na réimsí a d'athraigh, mar sin liostaíonn `scoreboard` sa cháipéis chluiche staitisticí gach imreora agus scór gach foirne ag gach athrú.

## Dead reckoning, agus an mhínitheoir {#dead-reckoning-and-the-smoother}

Taifeadann athsheinm cliaint gach aerárthach ceithre huaire sa soicind, mar a tharraing an cliant é. Idir na nuashonruithe a fhaigheann sé d'aerárthach i bhfad uaidh, gluaiseann an cliant ar aghaidh é feadh a threoluais dheireanaigh agus casann sé ar aghaidh é ag a rátaí deireanacha, agus ag an gcéad nuashonrú eile gliogann sé ansin é. Léite mar atá, ritheann rian díreach, ansin léimeann sé. Ní mharcálann aon rud san iontráil eitilte cé na samplaí a fuarthas; aimsítear sampla dead-reckoned de réir an rud é: leanann sé líne dhíreach an dá shampla roimhe, ag a luas, laistigh de 3 cm.

Braitheann an tábhacht atá leis seo ar an gcath: i gcathanna arcáide is féidir thart ar leath de shamplaí aerárthach eile a bheith dead-reckoned, i gcathanna insamhalta cúpla faoin gcéad amháin. Gearrann an mhínitheoir na céimeanna os cionn 15 g thart ar cúig huaire (`selfCheck.deadReckoning`). Ní dhéanann an cliant aerárthach an imreora taifeadta féin a eachtarshuíomh agus fágtar mar atá sé.

Go réamhshocraithe (cuireann `--no-smoothing` as é) cuirtear rianta gach aonaid ach amháin ceann an imreora taifeadta féin san áit a deir na stáit a fuarthas go raibh siad: téann sampla dead-reckoned ar chuar trí na samplaí a fuarthas roimhe agus ina dhiaidh, gach ceann lena threoluas féin; thar 3 s níl an líne dhíreach ach lúbtha i dtreo an chéad sampla fuarthas eile, mar sin ní ghluaiseann aon sampla níos faide ná gliogán an chliaint féin. Casann a dhearcadh go cothrom ó dhearcadh fuarthas amháin go dtí an chéad cheann eile. Mínítear samplaí fuarthas 2 m nó 0.04 s dá luas ar a mhéad; fanann casadh seasta mar atá sé. Fanann luachanna féin na hathsheinme sna colúin `Raw`.

## Dearcadh, seiceáilte {#attitude-checked}

Ar aerárthach an imreora taifeadta féin luíonn an heading laistigh de chéim (airmheán) de threo an taistil, an pitch laistigh de chúpla céim d'uillinn an dreapadh, agus i gcasadh soiléir tá comhartha an chasta ag an roll do bheagnach gach sampla: tá roll an mhúnla eitilte sciathán clé síos dearfach, agus casann an tábla é go sciathán deas síos dearfach (`selfCheck.aircraftAttitude`). Céimníonn na huillinneacha 10-bit 0.18 céim. Seiceáiltear dearcadh aonad talún i gcoinne a lámhaigh ([Tuirlingtí](ground.md#turrets)).

---

Cuid de [3DHeat](https://github.com/Holdi601/3DHeat) ([doiciméadúchán](https://holdi601.github.io/3DHeat/)). Foinse: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
