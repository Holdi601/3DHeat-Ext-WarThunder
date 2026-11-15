---
title: Conas a léann sé athsheinm
nav_order: 10
lang: ga
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Conas a léann sé athsheinm {#how-it-reads-a-replay}

Tá an leathanach seo do dhaoine ar mhaith leo a fháil amach cad a léann an tiontaire, conas a seiceáladh é, agus mar sin cé chomh mór is féidir muinín a bheith acu as gach colún. Níl sé ag teastáil uait chun athsheinmeanna a thiontú.

Seiceáladh an léamh ar athsheinmeanna cliaint de chathanna arcáide aeir, insamhalta aeir agus cabhlaigh, ar athsheinmeanna freastalaí de chathanna talún, agus, do leaganacha amach 2025, ar athsheinmeanna samplacha poiblí [wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder). Cuireann gach seiceáil luach i gcomparáid le rud a deir an athsheinm an dara huair, ar bhealach neamhspleách; ní thugtar anseo ach an modh agus an comhaontú.

## Cad a léitear, agus an tseiceáil {#what-is-read-and-the-check}

| Cuid | Stádas, agus an tseiceáil |
|---|---|
| Ceanntásc, léarscáil, misean, am tosaigh, seisiún; torthaí | gach comhad |
| Socruithe misin (an blk tar éis an cheanntáisc) | mód, aimsir, teorainneacha, `stars` (dáta, am, áit) |
| Sruth paicéad (zlib in 2025, zstd in 2026) | gach paicéad frámaithe |
| Suíomhanna agus dearcadh aerárthaigh (leagan amach 2026) | 4 shampla sa soicind, gan aon phaicéad gan léamh; aontaíonn an heading le treo an taistil |
| Paicéid eitilte romhainn a ham | tar éis hiccup líonra, coinníonn paicéad eitilte athsheinme cliaint uaireanta gach aerárthach eile san áit a mbeidh sé thart ar 0.75 s ina dhiaidh sin. Tomhaistear an tosaíocht in aghaidh an phaicéid, agus tugtar don aerárthach a bhfuil sé chun tosaigh an t-am a sheasann sé ar a shon (`selfCheck.flightPacketsRetimed`) |
| Gliogáin dead-reckoning | tomhaistear céim as rith dead-reckoned ón stát fuarthas deireanach, mar sin ní ghearrann ceartúcháin an chliaint rianta a thuilleadh ([Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)) |
| Teleports | gearrtar rian san áit a ngluaiseann a aonad níos faide ná mar is féidir leis: ar dtús i gcoinne a chineáil (aerárthaigh 750 m/s, talamh agus longa 40 m/s, airm 1800 m/s), ansin i gcoinne a luas féin. Liostaítear gach gearradh i `trackBreaks` lena chúis is dóichí (athspraoi, an cluiche ag bogadh an imreora, ceartú aonaid i bhfad uaidh). Tar éis na ngearrthaí, níl aon chéim idir sraitheanna rian níos tapúla ná mar a cheadaíonn a chineál (`selfCheck.stepSpeed`) |
| Suíomhanna talún agus long (0xF073 / 0xF074) | gan aon phaicéad gan léamh. Heading, pitch agus roll ón dearcadh 16-bit: aontaíonn an heading le treo an taistil laistigh de thart ar 2 chéim (airmheán); comhairíonn an pitch 180/65536 céim sa chéim; le comhartha an roll casta, díríonn treo an ghunna ón gcorp agus ón tuirlingt ar an aonad a bualadh do bheagnach gach lámhaigh tanc. Suíonn longa ag leibhéal an uisce |
| Tuirlingtí | yaw tuirlinge agus pitch gunna tancanna: féach [Tuirlingtí](ground.md#turrets) |
| Airde talún pacáilte | cuntar suíomhanna pacáilte i 64 bit a n-airde ó -100 m ar fhormhór na leibhéal agus ó leibhéal an uisce ar chuid acu; tomhaistear an fritháireamh ar gach athsheinm ó aonaid a chonacthas sa dá fhoirm (`selfCheck.packedGroundHeight`) |
| Sruth eintiteas (cruthú, scriosadh) | gach cruthú léite. Tagann an leagan amach ó fhoinse fhoilsithe Dagor Engine; scipeáiltear cineálacha comhpháirteanna féin War Thunder trí a aimsiú cá dtosaíonn an chéad chomhpháirt eile. Is ionann feithicil agus sliotán imreora gach aonaid agus iad siúd a ainmníonn na taifid mharaithe agus bhuillí, do gach taifead a seiceáladh |
| Cé a thiomáin cén t-aonad, aonaid AI, longa, spriocanna talún | ón sruth eintiteas: tá a fheithicil agus a fhoireann ag gach aonad, a imreoir ag aonad gach imreora |
| Maruithe i gcoinne na dtorthaí | is ionann básanna in aghaidh an imreora agus na dtorthaí; comhairíonn na torthaí níos mó maruithe, mar ní sheoltar gach marú chuig an gcliant. Ní choinníonn athsheinm a thosaíonn tar éis tús an chatha ach na maruithe ina dhiaidh sin |
| Maruithe, buillí criticiúla, damáiste trom | gach comhad |
| Modúil scriosta (0xF118) | an t-aonad agus uimhir na páirte; teastaíonn samhail damáiste na feithicle ó ainm na páirte, nach bhfuil san athsheinm |
| Airm scaoilte (sruth eintiteas) | tá an pointe scaoilte thart ar 10-20 m (airmheán) ón aonad is gaire, a glactar mar lainseálaí |
| Airm ag eitilt (0xF0DB) | diúracáin, roicéid agus buamaí, gach ceann ceangailte lena eintiteas |
| Buamaí gan taifid eitilte | oibrítear amach titim buama gan iad ón scaoileadh go dtí an tionchar (domhantarraingt agus tarraingt, sampla gach 0.1 s, `extrapolated` fíor). Seiceáilte thar an bhfarraige, áit a bhfuil airde an tionchair ar eolas: críochnaíonn na titimeanna oibrithe amach laistigh de thart ar 15 m den uisce. Sa cháipéis chluiche tá `ballisticImpact` ag arm den sórt sin; comhairíonn `counts.bombsBallistic` iad |
| Sliotáin imreoirí, comhrá | gach comhad |
| Pléascanna, pléasca flak, dámhachtainí, aimsiú, aimsir, réada misin | léite; suíomhanna seiceáilte leis an tsúil san fhaire |
| Uirlisí an imreora taifeadta (0xD04A) | ainmnithe de réir a ndéanann siad: [Uirlisí cábáin](aircraft.md#cockpit-instruments); an chuid eile faoi `notNamed` |
| Réimsí eile iontrálacha eitilte | treoluas, babhtaí, rialuithe, innill: [Iontrálacha eitilte](aircraft.md#flight-entries) |
| Dearcadh sraitheanna imeachta | iompraíonn gach sraith imeachta heading, pitch, roll agus veicteoir súl a haonaid ag an nóiméad sin |
| Staitisticí imreoirí agus scóir foirne | ag deireadh an chatha is ionann gach staitistic agus na torthaí do gach imreoir: [Sonraí machnaimh](aircraft.md#reflection-data) |
| Ainmneacha arm agus feithiclí | ó logánú Béarla do shuiteála; níl aon ainm sa chluiche ag crios réamhshocraithe cúpla long ná radair aerpháirce |
| Imreoirí agus AI | níl sraith imreora torthaí ar bith AI, is imreoir torthaí gach sraith nach AI í (`selfCheck.identity`) |
| Raic | leanann samplaí aonaid tar éis a bháis ag teacht; tá raic aonaid talún nó long `alive` 0 go dtí go mbaintear a eintiteas, agus fanann ina rian amháin; coinníonn aerárthaigh `alive` 0 ar feadh 60 s ar a mhéad (`selfCheck.wrecks`) |
| Malartuithe feithicle | cuirtear deireadh le haonad imreora atá beo fós nuair a thaispeánann aonad eile an imreora chéanna (feithicil fágtha ina seasamh). Ní mór `selfCheck.vehicleSwitch.twoLiveVehicles` a bheith 0 |
| Mód catha | [Mód catha](ground.md#battle-mode) |
| Aerárthaigh in athsheinm freastalaí 2026 | léite sa leagan amach 2026; aontaíonn an heading agus comhartha an roll leis na casadh; ní iompraíonn aerárthaigh áitchoinneálaithe agus drónaí taiscéalaíochta aon sonraí |
| Imreoirí athsheinm freastalaí | aimsithe de réir ainm sna sliotáin; is ionann gach staitistic agus na torthaí (`selfCheck.players`) |
| Aerárthaigh in athsheinmeanna freastalaí 2025 agus leagan 101286 | gan léamh: tá leagan amach difriúil ag a bpaicéid eitilte |

## Teachtaireachtaí chuig aonaid {#messages-to-units}

Is teachtaireacht mpi de chuid daNet Dagor Engine gach paicéad cineál-4: id an réada faighteora, ansin (nuair atá a 11 bhit íseal ar fad socraithe) UID sínte an réada, id na teachtaireachta agus an pálasta. Iompraíonn teachtaireacht chuig aonad mar UID sínte id eintitis an aonaid, `index << 10 | generation`. Seiceáilte: ainmníonn gach teachtaireacht den sórt sin eintiteas beo ag an nóiméad sin.

Do speisialtóirí, na teachtaireachtaí a léitear:

| Teachtaireacht | Cad é, agus an tseiceáil |
|---|---|
| 0xF0E9 UnitHitEffects | buille teilgin amháin: uid an lámhachóra agus pointe an bhuille i bhfráma an aonaid (x ar aghaidh, y suas, z ar chlé): ceintimeadair ar aerárthaigh agus long, 20/32768 m sa chéim ar aonaid talún (feistithe do mhéid tuirlingtí tanc). `hitLocalX/Y/Z` i méadair. Éiríonn sraith `shot` as ([Tine ghunnaí](hits.md#gunfire)). Tá ionsaitheoir beagnach gach taifead buille agus maruithe i measc na lámhachóirí seo; luíonn pointí buille ar an taobh atá os comhair an lámhachóra |
| 0xF133 UnitOnExplosion | an uid lámhachóra chéanna |
| 0xF04B OnUnitDead | sraitheanna `dead`: tá ceann ag íobartach gach taifead maruithe laistigh de 2 s |
| 0xD047 FmwRpm | rpm na n-inneall (`rpm`); aontaíonn le tomhaiseán rpm an chábáin |
| 0xF0B1, 0xF0A0 | sraitheanna `gun_shot`: lámhaigh aonair d'airtléire agus gunnaí frith-aeir troma |
| 0xF01B, 0xF01C | sraitheanna `fire_start`, `fire_stop`: pléasca gunnaí frith-aeir 40 mm (gunna ag lámhach; is `fire_on` tine ar fheithicil, féach [Tinte feithiclí](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | sraitheanna `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` |
| 0xD0FE ProjectileHitReplay | buillí an imreora taifeadta féin agus é á bhualadh, le hairm agus lón catha, ainmnithe ón tsuiteáil (`projectileHitReplays`) |
| 0xF13E, 0xF031 | éifeacht amhairc buille agus éifeacht a seinneadh ar an aonad; tagann siad le buille ar an aonad céanna |
| 0xD041 | ceann do gach gunna cosanta aerárthaigh, faoi dhó sa soicind; meaitseálann a n-innéacsanna airm ghunnadóra an mhúnla eitilte |
| 0xD048, 0xF117 | leagan amach léite, brí anaithnid |
| an chuid eile (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | sa chomhad cliatháin teachtaireachtaí lena n-aonad agus réimsí |

Is iad ainmneacha an phobail iad na hainmneacha (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Léite freisin {#also-read}

- **Macasamhlú sruth eintiteas** (0x22, 0x23): in aghaidh an eintitis bloc luachanna comhpháirte: amadóirí deisithe long, comhaireamh earraí inchaite, athruithe úinéara agus foirne, róthéamh inneall. Comhairítear in `counts.replicatedComponents`; na luachanna sa chomhad cliatháin teachtaireachtaí.
- **Gníomhartha script misin** (0xF028) agus **leideanna** (0xF0EC): `triggers`, `hints`. **Dul chun cinn misin** (0xF07A, 0xF07C): `missionProgress`.
- **An ceamara athsheinme** (0xD043): féach [An ceamara](ground.md#the-camera).

## Gan léamh, agus cén fáth {#not-read-and-why}

- **Ainmneacha agus coirp teachtaireachtaí eintitis** (0x20, 0x21): is áit i liosta tiomsaithe isteach sa chluiche é uimhir an ranga, gan seoladh agus gan a bheith ina shonraí. Léitear dhá cheann (tinte feithicle agus a múchtóirí); coinnítear an chuid eile iomlán lena n-eintiteas agus uimhir ranga.
- **Réada macasamhlaithe eile** (cineálacha seachas sliotáin imreoirí agus foirne): léite agus coinnithe, gan ainmniú; níl aon rud sna torthaí le seiceáil ina gcoinne.
- **Rialuithe, sprocaire agus babhtaí aerárthach eile**: athnuaite anois is arís amháin; coinnithe sa chomhad cliatháin eitilte, ní sa tábla.
- **Tinte aerárthaigh**: gan aimsiú in aon teachtaireacht; níl aon sraith `fire_on` ag aerárthach trí thine.
- **Ainmneacha arm scaoilte**: ní choinníonn eintiteas buama ná roicéid aon ainm; ainmníonn taifid mharaithe arm marú.
- **Lámhaigh a chaill**: ní choinníonn athsheinm ach na buillí.

Deir `counts.messageIdsNotRead` agus `selfCheck` gach cáipéise cluiche cad atá in athsheinm nua agus cé chomh maith a léadh í.

---

Cuid de [3DHeat](https://github.com/Holdi601/3DHeat) ([doiciméadúchán](https://holdi601.github.io/3DHeat/)). Foinse: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
