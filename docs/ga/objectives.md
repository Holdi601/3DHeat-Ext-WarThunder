---
title: Cuspóirí
nav_order: 15
lang: "ga"
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Cuspóirí {#objectives}

Liostaíonn `objectives` sa cháipéis chluiche an rud a throidtear air sa chath, ó dhá fhoinse (`source`):

- **An athsheinm** (`replay`): na réada misin a ainmníonn 0xD039 (criosanna gabhála `cz_circle_NN`, aerpháirceanna, héileapháirceanna, bunáiteanna), curtha san áit ina gcuireann réada macasamhlaithe de chineál 3 (0xF02D) anois iad - tosaíonn crios gabhála ag áit a theimpléid agus bogtar é go crios an mhóid seo ag an tús (`moved`). Leanann uimhreacha chineál 3 ord 0xD039; luíonn gach réad nach mbogtar go díreach san áit a bhfuil 0xD039 aige, rud a sheiceálann an t-ord. Faigheann crios gabhála cruth agus ga limistéar an mhisin ina áit (`area`, laistigh de 2 m) agus a litir óna innéacs féin (cineál 5 réimse 69: 0 = A); is é ord na litreacha ord na hathsheinme, ní seiceáilte i gcoinne léarscáil an chluiche.
- **An misean** (`mission`): an comhad misin `<mission>.blk` i `mis.vromfs.bin` do shuiteála agus na teimpléid a allmhairíonn sé (léite amháin, tráth an tiontaithe): a limistéir, aicmithe de réir ainm - spraoi (pointí uimhrithe spraoi `..._spawnareaNN` mar spraoi `points` amháin), limistéir chatha, spriocanna buamála (`bomb_zone`), pointí spraoi conmhaigh (`road_NN_spawn`), limistéir scoir agus maraithe. Fágtar ar lár limistéir mód eile den léarscáil chéanna (`conq_`, `dom_`, `bttl_`, ...), agus de leaganacha `_arcade` / `_realistic` / `_hardcore` an ceann ar leis an gcath é (glacann RB `_realistic`, nó `_hardcore` ar shlí eile, mar a dhéanann scripteanna na misean); marcóirí achomair, pointí gunna frith-aeir agus limistéir níos leithne ná 5 km (na limistéir a scaiptear spraoi orthu) freisin. Deir gach spraoi cé mhéad rian imreora a thosaigh ann (`used`, `usedByTeam`). Is féidir le misean a thaobhanna a mhalartú go randamach (`randomSpawnTeams`): nuair a thaispeánann na spraoi foirne na hathsheinme ar an mbealach eile, malartaítear gach `team` agus coinnítear taobh an ainm mar `missionTeam`. Níl bealaí conmhaigh i bpointí bealaigh na misean mar a léitear; ní thugtar ach an áit a bhfeictear conmhaigh.

Is é an comhad cliatháin `<match>.objectives.parquet` na criosanna gabhála le himeacht ama: na réada macasamhlaithe de chineál 5, ceann do gach crios - réimse 2 a úinéir (0, 1, 2), réimse 67 a dhul chun cinn gabhála, beart sínithe ó -100 go 100 (dearfach i dtreo foireann 2), réimse 69 a innéacs. Seiceáilte (`selfCheck.objectives`) ar athsheinmeanna freastalaí talún de chathanna Conquest agus Domination: tagann gach athrú úinéara le himreoir den fhoireann ghabhála ag fáil `captureZone` sa scórchlár ag an nóiméad céanna (laistigh de 1.5 s) agus le haonad talún beo den fhoireann sin istigh sa chrios; taispeánann spraoi gach catha foirne na hathsheinme ar bhealach amháin amháin (go minic malartaithe i gcoinne `t1_` / `t2_` an mhisin).

## Aonaid radhairc: tramanna agus vaigíní iarnróid {#scene-units-trams-and-rail-wagons}

Is féidir le leibhéal aonaid dá chuid féin a chur: is iad eintitis `unit_loader+rail_wagon` athsheinm freastalaí tramanna chomhad radhairc an leibhéil (`gamedata/scenes/<level>_objects.blk` i `aces.vromfs.bin`: `setting__unit_class`, a claochlú agus `setting__isDead`). Ní iompraíonn a n-eintitis aon uid inléite, mar sin is é an t-aonad sin rian talún gan eintiteas aonaid a luíonn a chéad sampla laistigh de 2 m d'aonad radhairc: a aicme mar `Vehicle`, kind `train`, type `tram`, `locomotive` nó `wagon`, gan foireann; is raic (`alive` 0) é aonad a chuireann an radharc marbh (cosúil le tramanna dóite) ó a chéad sraith. Níl aon ainm Béarla ag an gcluiche dóibh; is é `VehicleName` an id léite mar fhocail ("Railway tram A"). Ní bhíonn a suíomh ag creathadh: ní ghluaiseann beagnach gach ceann acu riamh (gach sampla mar an gcéanna go dtí an bit). Seolann an athsheinm iad thart ar deich n-uaire sa soicind ar aon nós, mar sin coinnítear de a gcuid samplaí na cinn a ghluaiseann iad amháin (0.05 m nó 0.1 chéim), agus ceann amháin gach 10 s (comhairíonn `selfCheck.sceneUnits` na samplaí a thit). Roimhe sin, bhí siad ina rianta darb ainm `uid 8` gan feithicil.

---

Cuid de [3DHeat](https://github.com/Holdi601/3DHeat) ([doiciméadúchán](https://holdi601.github.io/3DHeat/)). Foinse: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
