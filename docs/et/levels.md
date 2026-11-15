---
title: Tasemed
nav_order: 9
lang: et
source: levels.md
source_hash: "1f750f25303d"
nav_exclude: true
search_exclude: true
---
# Tasemed (heat3d-wt-level) {#levels-heat3d-wt-level}

`heat3d-wt-level` muudab sinu enda War Thunderi installatsiooni tasemed vaaturile sobivateks
`.glb` tasemeteks, samas raamistikus nagu kordusete tabelid.

## Samm-sammult {#step-by-step}

1. Loetle oma installatsiooni tasemed: `heat3d-wt-level list`. See prindib ühe rea taseme kohta:
   selle nimi, maastik ja kaardid, seejärel arv. Näiteks (väljamõeldud tase):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Eralda üks, mitu (jokkersümbolid lubatud) või kõik:

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```
3. Lae `levels/<level>/<level>.glb` vaaturi paneeli **Taust / tase** alla, selle kaardi lahingute alla.

Tasemed, mille kirjutad, jäävad sinu masinasse: ära neid kunagi avalda (vt
[Tingimused ja litsents](terms.md)).

## Valikud {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Käsk / valik | Mida teeb |
|---|---|
| `list [--game FOLDER]` | iga installatsiooni tase |
| `extract <levels...>` / `--all` | nimetatud tasemed (nii, nagu `list` need prindib; jokkersümbolid lubatud) või kõik tasemed |
| `-o`, `--out` | väljundkaust; iga tase läheb kausta `<out>/<level>/` |
| `--game FOLDER` | War Thunderi kaust (vaikimisi leitakse Steamist või käivitajast; ka `HEAT3D_WT_GAME`) |
| `--detail low/medium/high` | maapinna proovivõtt, maapinna värv ja objektieelarve paagikaardi kohal (vaikimisi `medium`) |
| `--max-object-triangles N` | objektieelarve (vaikimisi detaili oma) |
| `--max-grid N` | kõrguskaardi näidised ühel küljel, osa kohta (vaikimisi 1024) |
| `--no-objects` | jäta välja hooned, puud ja muud paigutatud objektid |
| `--no-generated` | jäta välja objektid, mida maastikuklassid genereerivad (metsad, linnad) |
| `--no-terrain-colour` | kata maapind taktikalise kaardiga, mitte maastikuklassidega |
| `--no-texture` | jäta maapind tekstuurita |
| `--skip-existing` | jäta vahele tasemed, mille `.glb` on olemas |

## Mis kirjutatakse {#what-is-written}

Iga tase muutub failideks `<out>/<level>/<level>.glb`, `<level>.json` (mis loeti, veetase, kaardi ristkülikud,
kolmnurkade arvud, ajad) ja taseme taktikalisteks kaartideks `<level>_map.png` (õhukaart) ja
`<level>_tankmap.png`; maapealsed kaardid saavad ka `<level>_terrain.png`, maapinna enda värvid paagikaardi
peal. Glb kirjutatakse faili `<level>.glb.part` ja nimetatakse ümber, kui see on valmis; taseme kirjutamise
ajal on kinni `<out>/<level>/.<level>.lock`, nii et kaks eraldamist ei kirjuta kunagi sama taset (teine
prindib `busy <level>`). Installatsioon leitakse Steami või käivitaja vaikekaustadest; `--game <folder>` või
`HEAT3D_WT_GAME` ütlevad, kus see muidu on.

| Osa | Mis see on |
|---|---|
| `ground:<level>` | maastiku kõrguskaart (`HM2`) ruudustikuna; maapealsetel kaartidel paagikaardi keskosa (pool selle laiusest) `--detail` sammuga, värvitud maastikuklassidega, maapinna dekaalide ja teedega (`<level>_terrain.png`; taktikaline kaart, kui seda ei saa teha); kaartidel ilma paagikaardita (õhukaardid) kogu kõrguskaart ühe sammuga (2048 näidist küljel `high`-l, muidu 1024), värvitud maastikuklassidega õhukaardi ala kohal (4096 pikslit küljel, umbes 32 m piksel 131 km kohta; taktikaline kaart, kui seda ei saa teha); tasemetel ilma kõrguskaardita maastikumaili |
| `ground:<level> tank map` | paagikaardi ülejäänud osa, üks samm jämedam |
| `ground:<level> heightmap surroundings` | kõrguskaardi ülejäänud osa, veel jämedam |
| `ground:<level> land mesh` | maastikumaili kokkupõrkekolmnurgad seal, kus kõrguskaart ei ulatu (paagikaardi ümbrus, kümnete kilomeetrite kaugusel); tasemetel ilma kõrguskaardita on see maapind, värvitud nagu ülal |
| `ground:<level> outside the map` | maapind, mida pilt ei kata, tekstuurita |
| `water:<level>` | üks lame ristkülik taseme `water_level` kõrgusel kogu maastiku kohal: mäng joonistab vee ühe tasapinnana ja madal maa selle all on meri, järv või jõesäng |
| `water:<level> rivers` | tasemetel veekõrguskaardiga (`WHM`) kaldus veepind lahtritel, mida see katab |
| `structure:<level> buildings` | iga paigutatud objekt, mis ei ole taim: majad, varemed, seinad, aiad, sillad, rööpad, kivid, rekvisiit. Fikseeritud (`RIGz`) ja paagikaardi kohal need, mida maastikuklassid genereerivad (linnaplokid, kivid). Igaüks joonistatakse oma renderdusvõrguga (seinad, katused, aknaavad, talad), LOD-iga, mida kolmnurkade eelarve lubab, värvitud materjali kaupa oma difuusse tekstuuri keskmise järgi |
| `structure:<level> trees` | puud ja põõsad, fikseeritud ja genereeritud (metsad, hekid): nende renderdusvõrk, kus eelarve lubab, muidu tüvi ja võra (koonus okaspuudel) puu enda lehevärvis, puu tegeliku suuruse järgi |

Objektid ilma renderdusvõrguta langevad tagasi oma kokkupõrkekujule; puud ilma selleta võrale. Tipu värvid
(`COLOR_0`) hoiavad sRGB-kodeeritud väärtusi, nii nagu 3DHeati vaatur neid loeb.

**Koordinaadid** on mängu meetrid, z peegeldatud: glb (x, y, z) = mäng (x, y, -z). Mängu maailm on
vasakukäeline (x ida, y üles, z põhja); glTF on parempoolne. `heat3d-wt-replay` hoiab mängu z ja ütleb
vaaturile, et see peegeldada, nii et kordus ja tema kaardi tase langevad üksteisele peale ilma
paigutussammuta. JSON annab iga taktikalise kaardi ristkülikut mängu meetrites ja selle nurki glb ruumis,
PNG laadimiseks kaardipildina.

**Detail.** `--detail low|medium|high` (vaikimisi medium) seab paagikaardi kohal:

| | paagikaardi keskosa | paagikaardi ülejäänud osa | maapinna värv | objektieelarve | kõige rohkem kolmnurki objekti kohta | genereeritud taimed alles |
|---|---|---|---|---|---|---|
| low | iga 4. näidis | iga 8. | 4 m piksel | 1,2 M | 1500 | puud 35%, põõsad 20% |
| medium | iga 2. | iga 4. | 2 m | 3,5 M | 4000 | puud 70%, põõsad 50% |
| high | iga näidis (enamikul maapealsetel kaartidel 2 m) | iga 2. | 1 m (kõige rohkem 4096 pikslit küljel) | 4,5 M | 12 000 | kõik |

Kaks paagikaardi rõngast peetakse 0,3 M (low), 1 M (medium) ja 3,7 M (high) kolmnurga juures: kaartidel, mille
kõrguskaart on peenem kui 2 m, sammud kahekordistuvad (välimine rõngas esimesena), kuni need mahuvad, nii et
need tulevad välja umbes 2 m juures.

Maapealne kaart `high` režiimis tuleb välja umbes 8 miljoni kolmnurgaga (3,5 M maapind, 4,5 M objektid) ja
250 MB; `medium` režiimis umbes 4,5 M. Objektide LOD-id on needsamad, mida mäng ise joonistaks ühest
vaatekaugusest: lühim, mille kogusumma mahub eelarvesse; väikesed rekvisiidid langevad esimesena jämedatele
LOD-idele ja suured hooned viimasena, selle järgi, mis vahemikud nende tegijad igale LOD-ile andsid (JSON-i
`lodDistance`); mis samm eelarvest üle säästab, läheb tagasi suurimatele objektidele. Jäme maapinna värv
(õhukaardid) keskmistab iga maastikuklassi kahhelda tekstuurid esmalt pikslisuuruseks, nii et kahheldused ei
moire'i. Kui isegi kõige jämedamad LOD-id ei mahu, muutuvad kõige rohkem säästvad puud võradeks ja siis
jäetakse välja kõige väiksemad tüübid (`leftOut`); ühtegi objekti ei joonistata kastina (kokkupõrkekuju, kui
see on, on objekti enda oma).
Genereeritud objektid hõrendatakse tüübi järgi (`density`) deterministlikult, samad igal käivitusel.
`--max-object-triangles` ületab eelarve, `--max-grid` (vaikimisi 1024) piirab kõrguskaardi jämedamaid osi,
`--no-objects` jätab objektid välja, `--no-generated` genereeritud objektid, `--no-terrain-colour`
katab maapinna taktikalise kaardiga, `--no-texture` jätab selle tekstuurita.

JSON-i `parts.objects` loetleb eksemplarid (fikseeritud ja genereeritud, liigi ja maastikuklassi järgi), mitu
joonistati mis LOD-iga (`drawnAs`), kolmnurgad, LOD-i kaugus ja sekundid; `parts.heightmap.rings` iga maapinna
rõnga samm ja kolmnurgad; `parts.terrainColour` maastikuklassid ja nende värvid, teed ja maapinna dekaalid;
`trianglesTotal`, `glbBytes` ja `secondsBy` kogusummad.

## Mida loetakse ja kui hästi {#what-is-read-and-how-well}

| Osa | Staatus |
|---|---|
| Taseme binaarfail (`levels/<level>.bin`, `DBLD` 3x64): plokitabel | iga tase kontrollitud |
| Kõrguskaart (`HM2`, versioonid 0-2; versioon 2 on 8-bitised väärtused plokkides, Oodle või zstd tükid) | iga tase, mille kõrgusakaart on versioon 2 Oodle tükkidega; kontrollitud silmaga nende taktikaliste kaartide vastu (jõed, orud, rannikud ja linnad langevad kokku) |
| Maastikumaili kokkupõrge (`lmap`, selle `LTdump` maastiku kiiresjälgija) | loetud seal, kus tasemel on see (Oodle-pakitud). See on mängu kokkupõrkepind, mitte renderdatud võrk, seega on see jämedam seal, kus maa on tasane |
| Maapinna värv (`lmap` maastikuklassid ja kaalukaart, `LMp2` füüsikakaart, `hspl` splainid) | maastikuklasside värvikaardid ja detailitekstuurid (nende keskmised värvid), kaalutud kaalukaardiga, 1 m biomi indeks indekseeritud maastikuklassidel, füüsikakaardi tee- ja maapinnadekaalide kujud nende splaini või materjali tekstuuri värvis, kaljud järsul nõlvadel. Kontrollitud paagikaartide vastu: teed, linnad, järved, metsavööndid ja kivipaljandid langevad kokku. War Thunderi enda maastikušeideri värvivalemit ei ole avalikus lähtekoodis; kasutatakse mootori avaldatud (daNetGame) valemit, mis tuleb välja küllastunumana kui taktikaline kaart |
| Veetase | `water_level` taseme BLK-st `aces.vromfs.bin`-is (0, kui seal seda ei ole) |
| Veekõrguskaart (`WHM`: lamedate lahtrite ruudustik ja 130x130 lehekülge 16-bitiste kõrgustega) | loetud seal, kus tasemel see on; selle jõed kalduvad koos maaga |
| Taktikalised kaardid | failist `content/base/res/locations_maps.dxp.bin`, paigutatud BLK `mapCoord0/1` ja `tankMapCoord0/1` järgi; pildi ülaosa on põhi |
| Paigutatud objektid (`RIGz`: renderdusinstantsi generaatori fikseeritud eksemplarid) | iga eksemplar, 3x4 maatriksina 16-bitiste väärtustena või mõnel tasemel 32-bitistena (lahtri baitide arv otsustab); iga lahtri iga bait arvestatud kontrollitud tasemetel |
| Genereeritud objektid (`RIGz` maastikuklasside maskid ja `LandClass` ressursid) | mängu generaator, üle viidud: samad kohad proovitakse samas järjekorras samade juhuslike arvudega, maastikuklassi ja välistusmaskid, iga koha juures valitud objekt, selle pööre, skaala ja kõrgusenihe; kahhelda (linnaplokid) ja istutatud (metsad, põõsad, põllud) olemid. Genereeritud ainult paagikaardi kohal. Ligikaudsed: maapinna kõrgus ja normaal (kõrgusakaardist; mäng jälgib kiirt), välistuskastid, mida mäng registreerib jooksuajal, ja puude pööre (mäng klapib selle impostori pööramispalitrasse) |
| Renderdusvõrgud (`RendInst` ressursid failides `content/*/res/*.grp`, materjalid `riDesc.bin`-is) | iga LOD-i tipud ja kolmnurgad (ujukomapositsioonid; 16- või 32-bitised indeksid, tavalised või meshoptimizer-pakitud), iga elemendi materjal. Dekaali- ja impostor-kuulutuse elemendid jäetakse välja; läbipaistvad (klaas) jäetakse alles |
| Objektide värvid | materjali kaupa, difuusse tekstuuri väike mip-keskmine (lehtedel alfa-kaalutud), paigalduspakkidest: t0 enamikul shaderitel, esimene detailidifuus, kui t0 on kate või mask. Üks värv materjali kohta: objektidel ei ole tekstuuri |
| Kokkupõrkekujud (`<object>_collision`) | voo versiooni 3 kokkupõrkeressursid, kasutatud seal, kus objektil ei ole renderdusvõrku. Joonistatakse ainult see, mida mängu kiired tabavad (`TRACEABLE` sõlmed), ja kaste, sfääre ja kapsleid ainult siis, kui ressursil ei ole võrku: ülejäänud on jämedad füüsikalised asendajad, mis näitaksid objekti ümber kuubikuid |
| Navigatsioonivõrk (`Lnav`), renderdatud maastikuvõrk, rohi, `spgz`, `stbl`, `d2co` | ei loeta |

Tasemed on pakitud Oodle'iga, mis on omanikuõigusega. Mäng sisaldab oma koopiat,
`<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (tavaline x64 versioon), ja see laaditakse;
`HEAT3D_OODLE=<dll või kaust>` osutab mujale. Siin ei ole Oodle'it kaasas.

## Formaadid ja kus need on dokumenteeritud {#formats-and-where-they-are-documented}

Gaijin avaldas Dagor Engine'i lähtekoodi BSD 3-Clause litsentsi all (github.com/GaijinEntertainment/DagorEngine).
Siinsed lugejad kirjutati selle järgi; ühtegi mängu koodi ei ole dekompileeritud. Iga moodul nimetab
lähtefailid, mida ta järgib:

- `vromfs.py`: `*.vromfs.bin` (päis `VRFs`/`VRFx`, zstd keha, mille esimesed ja viimased 16 baiti on XOR-itud
  fikseeritud võtmega, nimetabel ja nihketabel: `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`,
  `supp/dag_zstdObfuscate.h`) ja binaarne BLK (vormid 1-5, arhiivi jagatud nimekaardiga `\xff?nm` ja zstd
  sõnastikuga: `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`, `blk_zstd.cpp`).
- `dxp.py`: tekstuuripakid `DxP2` (`lib3d/texPackMgr2.cpp`) ja DDSx päised (`sharedInclude/3d/ddsxTex.h`);
  DXT1/DXT5/BC7 dekodeerib Pillow.
- `dagorlevel.py`: taseme binaarfail (`scene/loadLevel.cpp`), kõrguskaart
  (`heightmap/heightmapPhysHandler.cpp`, `heightMapLand/compressedHeightmap.cpp`), maastiku kiirejälgija
  (`landMesh/lmeshManager.cpp`, `landMesh/landRayTracerSoA4.cpp`) ja veekõrguskaart (`fftWater/fftWater.cpp`).
- `rigen.py`: paigutatud objektid (`rendInst/riGen/riGenData.h`, `rendInst/rendInstGen.cpp`,
  `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: genereeritud objektid (`rendInst/rendInstGenLand.cpp`, `riGen/landClassData.h`,
  `riGen/genObjByMask.h`, `riGen/genObjByDensGridMask.h`, `riGen/genObjUtil.h`, `riGen/riGenData.h`,
  `riGen/multiPointData.h`, `riGen/riRotationPalette.h`, `rendInstGen.cpp` (`create`, `precomputeCell`,
  `generateCell`), `gameMath/objgenPrng.h`, `util/dag_roHugeHierBitMap2d.h`,
  `util/dag_hierBitMap2d.h`, `ioSys/dag_roDataBlock.h`, `ioSys/roDataBlk.cpp`, `gameRes/grpData.h`).
- `rendinst.py`: renderdusinstantsid (`shaders/rendInstRes.cpp`, `shaders/dag_rendInstRes.h`,
  `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`, `shaders/dag_shaderMesh.h`,
  `shaders/dag_shaderCommon.h`, `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`) ja
  meshoptimizeri indeksikodek (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: maapinna värv (`landMesh/lmeshManager.cpp`, `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`,
  `lmeshRenderer.cpp`, `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`, `biomes.dshl`,
  `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`, `physMap/physMapLoad.cpp`,
  `baseUtil/treeBitmap.cpp`, `levelSplines/levelSplines.cpp`).
- `collision.py`: ressursipakid (`gameRes/grpData.h`) ja kokkupõrkeressursid
  (`sharedInclude/gameRes/collResStream.h`, `gameRes/collisionGameResLoad.cpp`), mille kolmnurgad on hoitud
  nelinurkse BVH-na (`daBVH/bvhIO.cpp`, `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) loeb samu arhiive; seda ei ole vaja ega kasutata.

---

Osa [3DHeatist](https://github.com/Holdi601/3DHeat) ([dokumentatsioon](https://holdi601.github.io/3DHeat/)). Lähtekood: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
