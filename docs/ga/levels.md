---
title: Leibhéil
nav_order: 9
lang: ga
source: levels.md
source_hash: "1f750f25303d"
nav_exclude: true
search_exclude: true
---
# Leibhéil (heat3d-wt-level) {#levels-heat3d-wt-level}

Tiontaíonn `heat3d-wt-level` leibhéil do shuiteála War Thunder féin ina leibhéil `.glb` don fhaire, sa fhráma céanna le táblaí na n-athsheinmeanna.

## Céim ar chéim {#step-by-step}

1. Liostaigh leibhéil do shuiteála: `heat3d-wt-level list`. Priontálann sé líne amháin do gach leibhéal: a ainm, a thír-raon agus a léarscáileanna, ansin an líon. Mar shampla (leibhéal cumtha):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Asbhain ceann amháin, roinnt (ceadaítear saoróga) nó iad ar fad:

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```

3. Luchtaigh `levels/<level>/<level>.glb` i bpainéal Leibhéal na faire, faoi na cathanna den léarscáil sin.

Fanann na leibhéil a scríobhann tú ar do mheaisín: ná foilsigh choíche iad (féach [Téarmaí agus ceadúnas](terms.md)).

## Roghanna {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Ordú / rogha | Cad a dhéanann sí |
|---|---|
| `list [--game FOLDER]` | gach leibhéal sa tsuiteáil |
| `extract <levels...>` / `--all` | na leibhéil ainmnithe (mar a phriontálann `list` iad; ceadaítear saoróga), nó gach leibhéal |
| `-o`, `--out` | fillteán aschuir; téann gach leibhéal i `<out>/<level>/` |
| `--game FOLDER` | fillteán War Thunder (réamhshocrú: aimsithe trí Steam nó trí sheoltóir; `HEAT3D_WT_GAME` freisin) |
| `--detail low/medium/high` | samplú talún, dath talún agus buiséad réad thar léarscáil na dtancanna (réamhshocrú `medium`) |
| `--max-object-triangles N` | buiséad na réad (réamhshocrú: ceann an mhíniúcháin) |
| `--max-grid N` | samplaí heightmap an taobh, in aghaidh na coda (réamhshocrú 1024) |
| `--no-objects` | fág foirgnimh, crainn agus réada cuirthe eile ar lár |
| `--no-generated` | fág ar lár na réada a ghineann na haicmí talún (foraoisí, bailte) |
| `--no-terrain-colour` | uigeacht an talamh leis an léarscáil thaicticiúil, ní leis na haicmí talún |
| `--no-texture` | fág an talamh gan uigeacht |
| `--skip-existing` | fág leibhéil a bhfuil a `.glb` ann |

## Cad a scríobhtar {#what-is-written}

Éiríonn `<out>/<level>/<level>.glb`, `<level>.json` (an méid a léadh, leibhéal an uisce, dronuilleoga na léarscáileanna, comhaireamh triantán, amanna) as gach leibhéal, agus léarscáileanna taicticiúla an leibhéil mar `<level>_map.png` (léarscáil an aeir) agus `<level>_tankmap.png`; faigheann léarscáileanna talún `<level>_terrain.png` freisin, dathanna féin an talaimh thar léarscáil na dtancanna. Scríobhtar an glb chuig `<level>.glb.part` agus athainmnítear é nuair atá sé críochnaithe; fad a scríobhtar leibhéal, coinnítear `<out>/<level>/.<level>.lock`, mar sin ní scríobhann dhá asbhaint an leibhéal céanna riamh (priontálann an dara ceann `busy <level>`). Aimsítear an tsuiteáil trí Steam nó trí réamhfhillteáin an tseoltóra; deir `--game <folder>` nó `HEAT3D_WT_GAME` cá bhfuil sí ar shlí eile.

| Cuid | Cad é |
|---|---|
| `ground:<level>` | heightmap an tír-raoin mar ghreille; ar léarscáileanna talún lár léarscáil na dtancanna (leath a leithid) ag céim an `--detail`, daite leis na haicmí talún, decals talún agus bóithre (`<level>_terrain.png`; an léarscáil thaicticiúil nuair nach féidir sin a dhéanamh); ar léarscáileanna gan léarscáil tancanna (léarscáileanna aeir), an heightmap ar fad ag céim amháin (2048 sampla an taobh ag `high`, 1024 ar shlí eile), daite leis na haicmí talún thar limistéar léarscáil an aeir (4096 picteilín an taobh, thart ar 32 m an picteilín thar 131 km; an léarscáil thaicticiúil nuair nach féidir sin a dhéanamh); ar leibhéil gan heightmap, an mogall talún |
| `ground:<level> tank map` | an chuid eile de léarscáil na dtancanna, céim amháin níos garbhaí |
| `ground:<level> heightmap surroundings` | an chuid eile den heightmap, níos garbhaí fós |
| `ground:<level> land mesh` | triantáin imbhuailte an mhogaill talún nuair nach sroicheann an heightmap (timpeallacht léarscáil tancanna, amach go deich gciliméadar); ar leibhéil gan heightmap is é an talamh é, daite mar thuas |
| `ground:<level> outside the map` | talamh nach gclúdaíonn an íomhá, gan uigeacht |
| `water:<level>` | dronuilleog chothrom amháin ag `water_level` an leibhéil thar an tír-raon ar fad: tarraingíonn an cluiche uisce mar phlána amháin, agus is farraige, loch nó leaba aibhneach é talamh íseal faoina bhun |
| `water:<level> rivers` | ar leibhéil le heightmap uisce (`WHM`), dromchla an uisce fána thar na cealla a chlúdaíonn sé |
| `structure:<level> buildings` | gach réad cuirthe nach planda é: tithe, fothracha, ballaí, fálta, droichid, iarnróid, carraigeacha, props. Na cinn seasta (`RIGz`) agus, thar léarscáil na dtancanna, iad siúd a ghineann na haicmí talún (bloic bhailte, clocha). Tarraingítear gach ceann lena mhogall rindreála (ballaí, díonta, oscailtí fuinneoige, bíomaí), ag an LOD a cheadaíonn an buiséad triantán, daite in aghaidh an ábhair ag meán a uigeachta scaipthe |
| `structure:<level> trees` | crainn agus tomóga, seasta agus ginte (foraoisí, fálta sceach): a mogall rindreála nuair a cheadaíonn an buiséad, ar shlí eile stoc agus coróin (cón do chonaipéir) i ndath duille féin an chrainn, thar fhíormhéid an chrainn |

Titeann réada gan mogall rindreála siar ar a gcruth imbhuailte; crainn gan ceann ar an gcoróin. Coinníonn dathanna rinn (`COLOR_0`) luachanna ionchódaithe sRGB, rud a léann faire 3DHeat.

**Comhordanáidí** is iad méadair an chluiche le z scáthánaithe: glb (x, y, z) = cluiche (x, y, -z). Tá saol an chluiche láimh chlé (x soir, y suas, z ó thuaidh); tá glTF láimh dheas. Coinníonn `heat3d-wt-replay` z an chluiche agus deir leis an bhfaire é a scáthánú, mar sin luíonn athsheinm agus leibhéal a léarscáile ar a chéile gan aon chéim socraithe. Tugann an JSON dronuilleog gach léarscáile taicticiúla i méadair an chluiche agus a coirnéil i spás an ghlb, chun an PNG a luchtú mar íomhá léarscáile.

**Mionsonraí.** Socraíonn `--detail low|medium|high` (réamhshocrú medium), thar léarscáil na dtancanna:

| | lár léarscáil na dtancanna | an chuid eile de léarscáil na dtancanna | dath talún | buiséad réad | triantáin is mó in aghaidh an réada | plandaí ginte coinnithe |
|---|---|---|---|---|---|---|
| low | gach 4ú sampla | gach 8ú | 4 m an picteilín | 1.2 M | 1,500 | crainn 35 %, tomóga 20 % |
| medium | gach 2ú | gach 4ú | 2 m | 3.5 M | 4,000 | crainn 70 %, tomóga 50 % |
| high | gach sampla (2 m ar fhormhór na léarscáileanna talún) | gach 2ú | 1 m (4096 picteilín an taobh ar a mhéad) | 4.5 M | 12,000 | iad ar fad |

Coinnítear an dá fháinne léarscáile tancanna ag 0.3 M (low), 1 M (medium) agus 3.7 M (high) triantán: ar léarscáileanna a bhfuil a heightmap níos míne ná 2 m, dúblaíonn na céimeanna (an fáinne seachtrach ar dtús) go dtí go n-oireann siad, mar sin éiríonn thart ar 2 m astu siúd freisin.

Éiríonn thart ar 8 milliún triantán (3.5 M talún, 4.5 M réad) agus 250 MB as léarscáil talún ag `high`; thart ar 4.5 M ag `medium`. Is iad LODanna na réad na cinn a tharraingeodh an cluiche féin ó achar amhairc amháin, an ceann is giorra a n-oireann a iomlán don bhuiséad: titeann props bheaga go LODanna garbha ar dtús agus foirgnimh mhóra is déanaí, de réir na raonta a thug a ndéantóirí do gach LOD (`lodDistance` an JSON); téann an méid a shábhálann an chéim sin thar an mbuiséad ar ais chuig na réada is mó. Déanann dath garbh talún (léarscáileanna aeir) meán d'uigeachtaí tíleáilte gach aicme talún síos go méid an phicteilín ar dtús, mar sin ní dhéanann na tíleanna aliasing isteach i moiré. Mura n-oireann na LODanna is garbha féin, éiríonn na crainn is mó a shábhálann coróin, agus ansin fágtar na cineálacha is lú ar lár (`leftOut`); ní tharraingítear aon réad mar bhosca (is é cruth imbhuailte, más ann dó, an réad féin). Tanaítear réada ginte go cinntitheach de réir cineáil (`density`), na cinn chéanna gach rith. Sáraíonn `--max-object-triangles` an buiséad, cuireann `--max-grid` (réamhshocrú 1024) caipín ar chodanna níos garbha den heightmap, fágann `--no-objects` réada ar lár, `--no-generated` na cinn ghinte, uigeachtaíonn `--no-terrain-colour` an talamh leis an léarscáil thaicticiúil, fágann `--no-texture` gan uigeacht é.

Liostaíonn `parts.objects` an JSON cásanna (seasta agus ginte, de réir cineáil agus aicme talún), cé mhéad a tarraingíodh ag cén LOD (`drawnAs`), na triantáin, an t-achar LOD agus na soicindí; `parts.heightmap.rings` céim agus triantáin gach fáinne talún; `parts.terrainColour` na haicmí talún agus a ndathanna, bóithre agus decals talún; `trianglesTotal`, `glbBytes` agus `secondsBy` na hiomláin.

## Cad a léitear, agus cé chomh maith {#what-is-read-and-how-well}

| Cuid | Stádas |
|---|---|
| Dénártha leibhéil (`levels/<level>.bin`, `DBLD` 3x64): tábla bloc | gach leibhéal seiceáilte |
| Heightmap (`HM2`, leaganacha 0-2; is luachanna 8-bit i mbloic iad leagan 2, píosaí Oodle nó zstd) | gach leibhéal a bhfuil a heightmap leagan 2 le píosaí Oodle; seiceáilte leis an tsúil i gcoinne a léarscáileanna taicticiúla (luíonn aibhneacha, gleannta, cóstaí agus bailte ar a chéile) |
| Imbhualadh mogaill talún (`lmap`, a ghathrianaire talún `LTdump`) | léite nuair atá ceann ag leibhéal (pacáilte le Oodle). Is é dromchla imbhuailte an chluiche é, ní an mogall rindreáilte, mar sin tá sé níos garbhaí nuair atá an talamh cothrom |
| Dath talún (aicmí talún `lmap` agus léarscáil mheáchain, léarscáil fhisice `LMp2`, splines `hspl`) | léarscáileanna datha agus uigeachtaí mionsonraí na n-aicmí talún (a meándathanna) ualaithe ag an léarscáil mheáchain, innéacs bithnimhe 1 m na n-aicmí talún innéacsaithe, cruthanna bóithre agus decals talún na léarscáile fisice i ndath uigeacht a splíne nó a n-ábhair, aille ar fhánaí géara. Seiceáilte i gcoinne léarscáileanna na dtancanna: luíonn bóithre, bailte, lochanna, creasa foraoise agus carraigeacha ar a chéile. Níl foirmle datha scáthaitheora tír-raoin féin War Thunder san fhoinse phoiblí; úsáidtear ceann foilsithe an einsin (daNetGame), a thagann amach níos sáithithe ná an léarscáil thaicticiúil |
| Leibhéal uisce | `water_level` ó BLK an leibhéil i `aces.vromfs.bin` (0 nuair nach bhfuil ceann aige) |
| Heightmap uisce (`WHM`: greille de chealla cothroma agus leathanaigh 130x130 d'airdí 16-bit) | léite nuair atá ceann ag leibhéal; fánaíonn a aibhneacha leis an talamh |
| Léarscáileanna taicticiúla | ó `content/base/res/locations_maps.dxp.bin`, curtha ag `mapCoord0/1` agus `tankMapCoord0/1` an BLK; is é barr na híomhá an tuaisceart |
| Réada cuirthe (`RIGz`: cásanna seasta ghineadóir cásanna rindreála) | gach cás, mar mhaitrís 3x4 de luachanna 16-bit nó, ar roinnt leibhéal, cinn 32-bit (socraíonn líon bheart na cille); gach beart de gach cill cuntasaithe ar na leibhéil a seiceáladh |
| Réada ginte (maisc aicme talún `RIGz` agus acmhainní `LandClass`) | ginteoir an chluiche, portáilte: na spotaí céanna triailte san ord céanna leis na huimhreacha randamacha céanna, na maisc aicme talún agus eisiaimh, an réad a roghnaíodh ag gach spota, a rothlú, scála agus fritháireamh airde; eintitis tíleáilte (bloic bhailte) agus curtha (foraoisí, tomóga, páirceanna). Ginte thar léarscáil na dtancanna amháin. Comhfhogasaithe: airde agus normalach an talaimh (ón heightmap; leanann an cluiche gathanna), na boscaí eisiaimh a chlárú an cluiche ag am rite, agus yaw crann (sáinníonn an cluiche é le pailéad rothlaithe an impostor). |
| Mogaill rindreála (acmhainní `RendInst` i `content/*/res/*.grp`, ábhair i `riDesc.bin`) | rinn agus triantáin gach LOD (suímh snámhphointe; innéacsanna 16 nó 32-bit, simplí nó pacáilte le meshoptimizer), ábhar gach eilimint. Fágtar eilimintí decal agus impostor-billboard ar lár; coinnítear na cinn trédhearcacha (gloine) |
| Dathanna réad | in aghaidh an ábhair, meán mip bheag a uigeachta scaipthe (ualaithe alfa do dhuilleoga), ó phacáin uigeachta na suiteála: t0 d'fhormhór scáthaitheoirí, an chéad scaipeadh mionsonraí nuair is forleagan nó masc é t0. Dath amháin in aghaidh an ábhair: gan uigeacht ar na réada |
| Cruthanna imbhuailte (`<object>_collision`) | acmhainní imbhuailte de leagan sreafa 3, a úsáidtear nuair nach bhfuil aon mhogall rindreála ag réad. Ní tharraingítear ach an méid a bhuaileann gathanna an chluiche (nóid `TRACEABLE`), agus boscaí, sféir agus capsúil nuair nach bhfuil aon mhogall san acmhainn amháin: is ionadaithe garbha fisice an chuid eile a thaispeánfadh mar chiúbanna thart ar an réad |
| Mogall nascleanúna (`Lnav`), an mogall talún rindreáilte, féar, `spgz`, `stbl`, `d2co` | gan léamh |

Comhbhrúitear leibhéil le Oodle, atá dílseánaigh. Seolann an cluiche cóip, `<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (tógáil x64 choitianta), agus is é sin a luchtaítear; díríonn `HEAT3D_OODLE=<dll or folder>` ar cheann eile. Níl aon rud de Oodle san áireamh anseo.

## Formáidí, agus cá bhfuil siad doiciméadaithe {#formats-and-where-they-are-documented}

D'fhoilsigh Gaijin foinse Dagor Engine faoi cheadúnas BSD 3-Clause (github.com/GaijinEntertainment/DagorEngine). Scríobhadh na léitheoirí anseo uaidh; níor dhícheapadh aon chód cluiche. Ainmníonn gach modúl na comhaid fhoinse a leanann sé:

- `vromfs.py`: `*.vromfs.bin` (ceanntásc `VRFs`/`VRFx`, corp zstd a bhfuil a chéad 16 bheart agus a 16 beart dheireanacha XORáilte le heochair sheasta, tábla ainmneacha agus tábla fritháireamh: `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`, `supp/dag_zstdObfuscate.h`) agus BLK dénártha (foirmeacha 1-5, le léarscáil ainmneacha roinnte na cartlainne `\xff?nm` agus foclóir zstd: `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`, `blk_zstd.cpp`).
- `dxp.py`: pacáin uigeachta `DxP2` (`lib3d/texPackMgr2.cpp`) agus ceanntásca DDSx (`sharedInclude/3d/ddsxTex.h`); díchódaíonn Pillow DXT1/DXT5/BC7.
- `dagorlevel.py`: dénártha an leibhéil (`scene/loadLevel.cpp`), an heightmap (`heightmap/heightmapPhysHandler.cpp`, `heightMapLand/compressedHeightmap.cpp`), an gathrianaire talún (`landMesh/lmeshManager.cpp`, `landMesh/landRayTracerSoA4.cpp`) agus an heightmap uisce (`fftWater/fftWater.cpp`).
- `rigen.py`: na réada cuirthe (`rendInst/riGen/riGenData.h`, `rendInst/rendInstGen.cpp`, `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: na réada ginte (`rendInst/rendInstGenLand.cpp`, `riGen/landClassData.h`, `riGen/genObjByMask.h`, `riGen/genObjByDensGridMask.h`, `riGen/genObjUtil.h`, `riGen/riGenData.h`, `riGen/multiPointData.h`, `riGen/riRotationPalette.h`, `rendInstGen.cpp` (`create`, `precomputeCell`, `generateCell`), `gameMath/objgenPrng.h`, `util/dag_roHugeHierBitMap2d.h`, `util/dag_hierBitMap2d.h`, `ioSys/dag_roDataBlock.h`, `ioSys/roDataBlk.cpp`, `gameRes/grpData.h`).
- `rendinst.py`: cásanna rindreála (`shaders/rendInstRes.cpp`, `shaders/dag_rendInstRes.h`, `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`, `shaders/dag_shaderMesh.h`, `shaders/dag_shaderCommon.h`, `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`) agus códóir innéacs meshoptimizer (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: dath an talaimh (`landMesh/lmeshManager.cpp`, `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`, `lmeshRenderer.cpp`, `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`, `biomes.dshl`, `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`, `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`, `levelSplines/levelSplines.cpp`).
- `collision.py`: pacáin acmhainní (`gameRes/grpData.h`) agus acmhainní imbhuailte (`sharedInclude/gameRes/collResStream.h`, `gameRes/collisionGameResLoad.cpp`), a stóráiltear a dtriantáin mar BVH ceathair (`daBVH/bvhIO.cpp`, `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

Léann wt_ext_cli (Apache-2.0) na cartlanna céanna; níl sé ag teastáil agus ní úsáidtear é.

---

Cuid de [3DHeat](https://github.com/Holdi601/3DHeat) ([doiciméadúchán](https://holdi601.github.io/3DHeat/)). Foinse: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
