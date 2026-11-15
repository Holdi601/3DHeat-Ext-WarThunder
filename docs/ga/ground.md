---
title: Aonaid talún agus ceamara
nav_order: 12
lang: ga
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Aonaid talún agus ceamara {#ground-units-and-camera}

Do léitheoirí ar mhaith leo a fháil amach cá dtagann na colúin tuirlinge, ceamara agus móid chatha astu agus cé chomh mór is féidir muinín a bheith acu astu. Ní thugann seiceálacha ach an modh agus an comhaontú.

## Tuirlingtí {#turrets}

Coinníonn stát talún tanc (dearcadh 16-bit), tar éis a shuímh, 141 bit nach léitear, ansin in aghaidh na tuirlinge 62 bit: yaw na tuirlinge agus pitch an ghunna (16 bit an ceann, 360/65536 céim sa chéim, sínithe) agus 30 bit nach léitear; ansin stuáil, agus ar roinnt stát 200 bit eile. Is é líon na dtuirlingtí an beart a sheoltar roimh an stát. Ní thugann stát nach n-oireann a fhad aon tuirlingt (seolann aonaid statacha stát níos giorra). Tá an yaw i gcoibhneas leis an gcorp, deiseal dearfach, 0 díreach romhat; an pitch i gcoibhneas leis an gcorp, suas dearfach.

Conas a seiceáladh é:

- **I gcoinne na lámhaigh:** do gach buille ó thanc, treo domhanda a phríomhghunna (dearcadh an choirp casta ag yaw na tuirlinge agus pitch an ghunna) i gcoinne na líne ón lámhachóir go dtí an t-aonad a bualadh, 30 m ar a laghad ar shiúl: in aghaidh an chatha airmheán de thart ar 98 % laistigh de 3 chéim i heading agus 99 % in ardú (`selfCheck.turretsVsShots`). Is buillí den chuid is mó ó ghunna meaisín i dtuirlingt eile an chuid eile.
- **I gcoinne aim an imreora taifeadta:** seolann a thanc féin uillinn dhomhanda a aim (tuathalach ó thoir), pitch agus fad. Luíonn heading an choirp móide yaw na tuirlinge laistigh de leathchéim (airmheán) den aim.

Seolann **athsheinmeanna freastalaí** (0xF074) stát gach tanc sa leagan amach céanna, agus sonraí dá gcuid féin ina dhiaidh, mar sin léitear gach tuirlingt a luíonn a dhá uillinn laistigh den stát (an phríomhcheann ar a laghad do bheagnach gach sraith tanc). Is í an tuirlingt é, ní an ceamara:

- **I gcoinne na lámhaigh**, mar thuas: in aghaidh an chatha os cionn 90 % laistigh de 3 chéim i heading agus 99 % in ardú.
- **I gcoinne an radhairc:** seolann athsheinm freastalaí aim gach imreora (`viewYaw`, `viewPitch`). Leanann an tuirlingt an radharc laistigh de leathchéim (airmheán), ach casann sí i bhfad níos moille ná mar a luascann an radharc, mar a dhéanann tiomána tuirlinge (`selfCheck.turretVsView`).
- **Ach ní i gcónaí ag luas tiomána:** sampla ar shampla, léimeann an luach mar a seoladh é uaireanta ar an aim nuair a bhíonn an aim in aice leis an ngunna, níos tapúla ná mar a chasann aon tiomáint.

Mar sin coinníonn an tábla an tuirlingt **coinnithe ag a tiomáint**: bogann `turretYaw` / `gunPitch` i dtreo an luacha mar a seoladh é ag luas casta an phríomhghunna ar a mhéad ó chomhad feithicle na suiteála (méadaithe faoi 1.3 do scileanna criú agus módúcháin; 45 agus 20 céim sa soicind nuair nach n-ainmníonn an tsuiteáil aon cheann). Ag gach buille den phríomhghunna socraítear an tuirlingt go díreach ar líne na lámhaigh, agus tugann pas siar ansin in am í (`selfCheck.turretLimit`). Iompraíonn an tsraith `shot` an `turretYaw` / `gunPitch` sin freisin. Fanann an luach mar a seoladh é i `turretYawRaw` / `gunPitchRaw`. Tá colúin tuirlinge folamh ag tanc nach n-iompraíonn a stát aon tuirlingt (b'fhéidir go dtitfidh an fhaire siar ar `viewYaw`). Luíonn `gunPitch` beagán os cionn `viewPitch` ag raon: ardú an ghunna do thitim an tsligéin.

Tá leagan amach eile ag stáit long; ní léitear a dtuirlingtí. Ní sheolann aerárthaigh aon treo cinn ná radhairc; fanann teachtaireacht 0xD020 na ngunnaí frith-aeir gan léamh.

## An ceamara {#the-camera}

Is é teachtaireacht 0xD043, thart ar 20 sa soicind, ceamara athsheinme an imreora taifeadta féin: réimse 1 ceathrún a chasann ar aghaidh an cheamara go dtí an áit a bhféachann sé; 2 áit an cheamara ón bhfeithicil a leanann sé (m); 4 an fritháireamh céanna i bhfráma féin na feithicle (x ar aghaidh, y suas, z ar chlé); 5 an áit a ndíríonn an t-imreoir (veicteoir aonaid); 3 an formhéadú (thart ar 1.2 i radharc tríú duine tanc, thart ar 1.0 in aerárthach, níos airde i radharc gunnaire nó trí largadóirí). Seiceáilte: is é réimse 4 réimse 2 casta isteach i bhfráma na feithicle, laistigh de 0.5 m do bheagnach gach teachtaireacht; tá heading aim ag ar aghaidh an cheamara. Ní sheolann an athsheinm aon réimse radhairc i gcéimeanna, an formhéadú amháin.

Tá an ceamara ag an tábla mar rian dá chuid féin: kind `camera`, track `<player> camera #ca`, sraith gach 0.1 s ar a mhéad, in áit na feithicle a leantar móide réimse 2, ag féachaint feadh na ceathrún (`dirX/Y/Z`, `heading`, `pitch`, `roll`), le `zoom`, `aimHeading` agus `aimPitch`, agus `otherLife` an `life` a leanann sé. Comhairíonn `selfCheck.camera` na sraitheanna agus an tseiceáil.

## Deireadh rian {#end-of-a-track}

Tarraingítear rian óna chéad sraith go dtí a shraith dheireanach. Nuair atá a aonad imithe sula gcríochnaíonn an athsheinm, is sraith `despawn` í a shraith dheireanach ina áit dheireanach: ag an am a bhain an cluiche a eintiteas (nuair a tháinig sin laistigh de 6 s dá shampla deireanach), nó ag a shampla deireanach ar shlí eile. Maireann rian gan ceann go deireadh na hathsheinme. Is féidir sraitheanna rian amháin a bheith i bhfad óna chéile (athnuaitear aonad i bhfad uaidh nó raic gach cúpla soicind, raic uaireanta ní ar feadh nóiméad): fanann a stát deireanach go dtí a chéad sraith eile.

## Mód catha {#battle-mode}

Coinníonn beart an cheanntáisc ag fritháireamh 688 an deacracht ina cheithre bhit íseal: 0 arcáid (AB), 5 réalaíoch (RB), 10 insamhalta (SB). Seiceáilte i gcoinne cineálacha cathanna a raibh a fhios gurbh iad na hathsheinmeanna. Is é an mód cluiche `ground` nuair a ligeann an misean do thancanna spraoi, `naval` nuair a ligeann do longa, `air` ar shlí eile (`allowedUnitTypes`); tagann mód an mhisin féin óna eochair (`missions/_Dom`), ainmnithe ó `lang/missions_versus.csv` do shuiteála. Is é an eochair chéanna an chuid `<mode>` d'ainmneacha comhad agus id an chluiche (`Conq4`, `Dom`), fágtha ar lár nuair nach bhfuil aon cheann sa cheanntásc.

---

Cuid de [3DHeat](https://github.com/Holdi601/3DHeat) ([doiciméadúchán](https://holdi601.github.io/3DHeat/)). Foinse: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
