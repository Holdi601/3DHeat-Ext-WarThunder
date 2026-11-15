---
title: Lygiai
nav_order: 9
lang: lt
source: levels.md
source_hash: "8fd5f4d94b76"
nav_exclude: true
search_exclude: true
---
# Lygiai (heat3d-wt-level) {#levels-heat3d-wt-level}

`heat3d-wt-level` paverčia jūsų paties War Thunder diegimo lygius `.glb` lygiais žiūryklei tokioje pačioje
koordinačių sistemoje kaip įrašų lentelės.

## Žingsnis po žingsnio {#step-by-step}

1. Išvardykite savo diegimo lygius: `heat3d-wt-level list`. Jis išveda po vieną eilutę kiekvienam lygiui:
   jo vardą, reljefą ir žemėlapius, tada skaičių. Pavyzdžiui (išgalvotas lygis):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Išskleiskite vieną, kelis (galima naudoti pakaitos ženklus) arba visus:

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```

3. Įkelkite `levels/<level>/<level>.glb` žiūryklės Fono / lygio skydelyje, po to žemėlapio mūšiais.

Lygiai, kuriuos įrašote, lieka jūsų kompiuteryje: niekada jų neskelbkite (žr.
[Sąlygos ir licencija](terms.md)).

## Parametrai {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Komanda / parametras | Ką daro |
|---|---|
| `list [--game FOLDER]` | kiekvienas lygis diegime |
| `extract <levels...>` / `--all` | nurodyti lygiai (taip, kaip juos rodo `list`; galima pakaitos ženklai) arba visi lygiai |
| `-o`, `--out` | išvesties aplankas; kiekvienas lygis eina į `<out>/<level>/` |
| `--game FOLDER` | War Thunder aplankas (numatytasis: randamas per Steam ar paleidiklį; taip pat `HEAT3D_WT_GAME`) |
| `--detail low/medium/high` | žemės matavimo žingsnis, žemės spalva ir objektų biudžetas virš tankų žemėlapio (numatytasis `medium`) |
| `--max-object-triangles N` | objektų biudžetas (numatytasis: detalės lygio) |
| `--max-grid N` | aukščio žemėlapio matavimų skaičius viena kryptimi, kiekvienai daliai (numatytasis 1024) |
| `--no-objects` | be pastatų, medžių ir kitų išdėstytų objektų |
| `--no-generated` | be objektų, kuriuos generuoja žemės klasės (miškai, miestai) |
| `--no-terrain-colour` | žemę apteksturuoti taktiniu žemėlapiu, o ne žemės klasėmis |
| `--no-texture` | žemę palikti be tekstūros |
| `--skip-existing` | praleisti lygius, kurių `.glb` jau yra |

## Ką įrašoma {#what-is-written}

Kiekvienas lygis tampa `<out>/<level>/<level>.glb`, `<level>.json` (kas buvo nuskaityta, vandens lygis,
žemėlapių stačiakampiai, trikampių skaičiai, laikai) ir lygio taktiniais žemėlapiais `<level>_map.png` (oro
žemėlapis) ir `<level>_tankmap.png`; sausumos žemėlapiams taip pat sukuriamas `<level>_terrain.png` - žemės
paties spalvos ant tankų žemėlapio. glb rašomas į `<level>.glb.part` ir pervadinamas, kai baigiamas; kol lygis
rašomas, laikomas `<out>/<level>/.<level>.lock`, todėl du išskleidimai niekada nerašo to paties lygio (antrasis
išveda `busy <level>`). Diegimas randamas per Steam ar paleidiklio numatytuosius aplankus; kitu atveju tai
nurodo `--game <folder>` arba `HEAT3D_WT_GAME`.

| Dalis | Ką tai yra |
|---|---|
| `ground:<level>` | reljefo aukščio žemėlapis (`HM2`) kaip tinklelis; sausumos žemėlapiuose - tankų žemėlapio vidurys (pusė jo pločio) su `--detail` žingsniu, nuspalvintas žemės klasėmis, žemės dekalais ir keliais (`<level>_terrain.png`; taktinis žemėlapis, jei to padaryti negalima); žemėlapiuose be tankų žemėlapio (oro žemėlapiai) - visas aukščio žemėlapis vienu žingsniu (`high` - 2048 matavimai viena kryptimi, kitais atvejais - 1024), nuspalvintas žemės klasėmis oro žemėlapio plote (4096 pikseliai viena kryptimi, maždaug 32 m pikselis per 131 km; taktinis žemėlapis, jei to padaryti negalima); lygiuose be aukščio žemėlapio - žemės tinklas |
| `ground:<level> tank map` | likusi tankų žemėlapio dalis, vienu žingsniu retesnė |
| `ground:<level> heightmap surroundings` | likusi aukščio žemėlapio dalis, dar retesnė |
| `ground:<level> land mesh` | žemės tinklo susidūrimo trikampiai, kur aukščio žemėlapis nepasiekia (tankų žemėlapio apylinkės, iki dešimčių kilometrų); lygiuose be aukščio žemėlapio tai yra žemė, nuspalvinta kaip aukščiau |
| `ground:<level> outside the map` | žemė, kurios paveikslėlis nepadengia, be tekstūros |
| `water:<level>` | vienas plokščias stačiakampis lygio `water_level` aukštyje virš viso reljefo: žaidimas vandenį piešia kaip vieną plokštumą, o žemuma po ja yra jūra, ežeras ar upės dugnas |
| `water:<level> rivers` | lygiuose su vandens aukščio žemėlapiu (`WHM`) - nuožulnus vandens paviršius per langelius, kuriuos jis dengia |
| `structure:<level> buildings` | kiekvienas išdėstytas objektas, kuris nėra augalas: namai, griuvėsiai, sienos, tvoros, tiltai, bėgiai, uolos, rekvizitai. Fiksuoti (`RIGz`) ir, tankų žemėlapyje, tie, kuriuos generuoja žemės klasės (miesto kvartalai, akmenys). Kiekvienas piešiamas pagal savo atvaizdavimo tinklą (sienos, stogai, langų angos, sijos), LOD, kurį leidžia trikampių biudžetas, ir spalvinamas pagal medžiagą pagal vidutinę jo difuzinės tekstūros spalvą |
| `structure:<level> trees` | medžiai ir krūmai, fiksuoti ir generuoti (miškai, gyvatvorės): jų atvaizdavimo tinklas, kur leidžia biudžetas, kitu atveju kamienas ir vainikas (kūgis spygliuočiams) jo paties lapų spalva, tikru dydžiu |

Objektai be atvaizdavimo tinklo grįžta prie susidūrimo formos; medžiai be jo - prie vainiko. Viršūnių spalvos
(`COLOR_0`) laiko sRGB koduotas reikšmes, o tokias skaito 3DHeat žiūryklė.

**Koordinatės** - žaidimo metrai su apverstu z: glb (x, y, z) = žaidimas (x, y, -z). Žaidimo pasaulis yra
kairiarankis (x - į rytus, y - aukštyn, z - į šiaurę); glTF - dešiniarankis. `heat3d-wt-replay` palieka
žaidimo z ir nurodo žiūryklei jį apversti, todėl įrašas ir jo žemėlapio lygis sutampa be jokio
išdėstymo žingsnio. JSON nurodo kiekvieno taktinio žemėlapio stačiakampį žaidimo metrais ir jo kampus glb
erdvėje, kad PNG būtų galima įkelti kaip žemėlapio paveikslėlį.

**Detalė.** `--detail low|medium|high` (numatytasis medium) nustato, virš tankų žemėlapio:

| | tankų žemėlapio vidurys | likusi tankų žemėlapio dalis | žemės spalva | objektų biudžetas | daugiausia trikampių viename objekte | išlaikomi generuoti augalai |
|---|---|---|---|---|---|---|
| low | kas 4-as matavimas | kas 8-as | 4 m pikselis | 1,2 M | 1 500 | medžiai 35 %, krūmai 20 % |
| medium | kas 2-as | kas 4-as | 2 m | 3,5 M | 4 000 | medžiai 70 %, krūmai 50 % |
| high | kiekvienas matavimas (2 m daugumoje žemėlapių) | kas 2-as | 1 m (ne daugiau kaip 4096 pikseliai viena kryptimi) | 4,5 M | 12 000 | visi |

Abu tankų žemėlapio žiedai laikomi 0,3 M (low), 1 M (medium) ir 3,7 M (high) trikampių ribose: žemėlapiuose,
kurių aukščio žemėlapis smulkesnis nei 2 m, žingsniai dvigubėja (pirmiausia išorinis žiedas), kol telpa, todėl
jie išeina maždaug 2 m.

Žemės žemėlapis `high` lygiu išeina maždaug 8 milijonų trikampių (3,5 M žemės, 4,5 M objektų) ir 250 MB;
`medium` - maždaug 4,5 M. Objektų LOD yra tie, kuriuos žaidimas pats pieštų iš vieno žiūrėjimo atstumo -
trumpiausias, kurio bendras kiekis telpa biudžete: maži rekvizitai pirmiausia virsta grubiais LOD, o dideli
pastatai - paskutiniai, pagal atstumus, kuriuos jų kūrėjai nurodė kiekvienam LOD (JSON lauke `lodDistance`);
ką tas žingsnis sutaupo viršijant biudžetą, grįžta didžiausiems objektams. Grubi žemės spalva (oro žemėlapiai)
pirmiausia vidutina kiekvienos žemės klasės išklotas tekstūras iki pikselio dydžio, todėl plytelės
nesukuria muarinio raštu. Jei net grubiausi LOD netelpa, medžiai, kurie sutaupo daugiausia, virsta
vainikais, o tada išbraukiami mažiausi tipai (`leftOut`); joks objektas nepiešiamas kaip dėžė (susidūrimo
forma, jei yra, yra paties objekto).
Generuoti objektai retinami deterministiškai pagal rūšį (`density`) - tuos pačius kiekvieną kartą. `--max-object-triangles`
perrašo biudžetą, `--max-grid` (numatytasis 1024) riboja retesnes aukščio žemėlapio dalis, `--no-objects` palieka objektus,
`--no-generated` - generuotus, `--no-terrain-colour` apteksturuoja žemę taktiniu žemėlapiu, `--no-texture` palieka ją be tekstūros.

JSON `parts.objects` išvardija egzempliorius (fiksuotus ir generuotus, pagal rūšį ir žemės klasę), kiek jų
nupiešta kokiu LOD (`drawnAs`), trikampius, LOD atstumą ir sekundes; `parts.heightmap.rings` - kiekvieno žemės
žiedo žingsnį ir trikampius; `parts.terrainColour` - žemės klases ir jų spalvas, kelius ir žemės dekalus;
`trianglesTotal`, `glbBytes` ir `secondsBy` - bendras kiekis.

## Kas nuskaitoma ir kaip gerai {#what-is-read-and-how-well}

| Dalis | Būsena |
|---|---|
| Lygio dvejetainis failas (`levels/<level>.bin`, `DBLD` 3x64): blokų lentelė | patikrinti visi lygiai |
| Aukščio žemėlapis (`HM2`, versijos 0-2; 2 versija - 8 bitų reikšmės blokuose, Oodle ar zstd gabalėliai) | kiekvienas lygis, kurio aukščio žemėlapis yra 2 versijos su Oodle gabalėliais; patikrinta akimi pagal jų taktinius žemėlapius (upės, slėniai, pakrantės ir miestai sutampa) |
| Žemės tinklo susidūrimas (`lmap`, jo `LTdump` žemės spindulių sekiklis) | nuskaitomas, kur lygis jį turi (Oodle supakuotas). Tai žaidimo susidūrimo paviršius, o ne atvaizduojamas tinklas, todėl jis grubesnis, kur žemė lygi |
| Žemės spalva (`lmap` žemės klasės ir svorio žemėlapis, `LMp2` fizikos žemėlapis, `hspl` splainai) | žemės klasių spalvų žemėlapiai ir detalių tekstūros (jų vidutinės spalvos), pasvertos svorio žemėlapiu, 1 m biomo indeksas indeksuotoms žemės klasėms, kelių ir žemės dekalų formos iš fizikos žemėlapio su jų splaino ar medžiagos tekstūros spalva, uolos ant stačių šlaitų. Patikrinta su tankų žemėlapiais: keliai, miestai, ežerai, miškų juostos ir uolų atodangos sutampa. War Thunder reljefo šešėliuotojo spalvos formulė viešame šaltinyje nepateikta; naudojama variklio paskelbta formulė (daNetGame), kuri išeina sodresnė nei taktinis žemėlapis |
| Vandens lygis | `water_level` iš lygio BLK `aces.vromfs.bin` (0, kur jo nėra) |
| Vandens aukščio žemėlapis (`WHM`: plokščių langelių tinklelis ir 130x130 puslapiai su 16 bitų aukščiais) | nuskaitomas, kur lygis jį turi; jo upės nuožulnėja kartu su žeme |
| Taktiniai žemėlapiai | iš `content/base/res/locations_maps.dxp.bin`, išdėstyti pagal BLK `mapCoord0/1` ir `tankMapCoord0/1`; paveikslėlio viršus yra šiaurė |
| Išdėstyti objektai (`RIGz`: fiksuotų egzempliorių generatoriaus fiksuoti egzemplioriai) | kiekvienas egzempliorius, kaip 3x4 matrica iš 16 bitų reikšmių arba, kai kuriuose lygiuose, 32 bitų (langelio baitų skaičius lemia); kiekvienas langelio baitas paskaičiuotas patikrintuose lygiuose |
| Generuoti objektai (`RIGz` žemės klasių kaukės ir `LandClass` ištekliai) | žaidimo generatorius, perkeltas: tos pačios vietos bandomos ta pačia tvarka su tais pačiais atsitiktiniais skaičiais, žemės klasės ir išskyrimo kaukės, objektas, parinktas kiekvienoje vietoje, jo posūkis, mastelis ir aukščio poslinkis; plytelėmis (miesto kvartalai) ir sodinami (miškai, krūmai, laukai) esybės. Generuojama tik virš tankų žemėlapio. Apytiksliai: žemės aukštis ir normalė (iš aukščio žemėlapio; žaidimas spindulį seka), išskyrimo dėžės, kurias žaidimas registruoja veikimo metu, ir medžių posūkis (žaidimas jį prisukia prie atvaizdo rotacijos paletės) |
| Atvaizdavimo tinklai (`RendInst` ištekliai `content/*/res/*.grp`, medžiagos `riDesc.bin`) | kiekvieno LOD viršūnės ir trikampiai (plaukiojantys pozicijų skaičiai; 16 ar 32 bitų indeksai, paprasti ar meshoptimizer supakuoti), kiekvieno elemento medžiaga. Dekalų ir impostorių elementai išbraukiami; permatomi (stiklas) paliekami |
| Objektų spalvos | pagal medžiagą - vidutinė difuzinės tekstūros mažos mip kopijos spalva (alfa svertinė lapams), iš diegimo tekstūrų paketų: t0 daugumai šešėliuotojų, pirmoji detalės difuzinė, kai t0 yra perdanga ar kaukė. Viena spalva kiekvienai medžiagai: objektai be tekstūros |
| Susidūrimo formos (`<object>_collision`) | 3 versijos srauto susidūrimo ištekliai, naudojami, kai objektas neturi atvaizdavimo tinklo. Piešiama tik tai, ką žaidimo spinduliai pataiko (`TRACEABLE` mazgai), o dėžės, sferos ir kapsulės - tik kai ištekliuje nėra tinklo: kita dalis yra grubūs fizikos pakaitalai, kurie atrodytų kaip kubai aplink objektą |
| Navigacijos tinklas (`Lnav`), atvaizduojamas žemės tinklas, žolė, `spgz`, `stbl`, `d2co` | nenuskaitoma |

Lygiai suspausti Oodle, kuris yra nuosavybinis. Žaidimas pateikia savo kopiją,
`<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (įprasta x64 versija), ir ji įkeliama; `HEAT3D_OODLE=<dll or folder>`
nurodo kitą. Oodle čia neįtrauktas.

## Formatai ir kur jie aprašyti {#formats-and-where-they-are-documented}

Gaijin paskelbė Dagor Engine šaltinį pagal BSD 3-Clause licenciją (github.com/GaijinEntertainment/DagorEngine).
Čia esantys skaitytuvai parašyti pagal jį; žaidimo kodas nebuvo dekompiliuotas. Kiekvienas modulis nurodo, kokius
šaltinio failus jis seka:

- `vromfs.py`: `*.vromfs.bin` (antraštė `VRFs`/`VRFx`, zstd turinys, kurio pirmi ir paskutiniai 16 baitų
  XOR-uojami su fiksuotu raktu, vardų lentelė ir poslinkių lentelė:
  `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`, `supp/dag_zstdObfuscate.h`) ir dvejetainis BLK (formos 1-5,
  su archyvo bendru vardų žemėlapiu `\xff?nm` ir zstd žodynu: `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`,
  `blk_zstd.cpp`).
- `dxp.py`: tekstūrų paketai `DxP2` (`lib3d/texPackMgr2.cpp`) ir DDSx antraštės (`sharedInclude/3d/ddsxTex.h`);
  DXT1/DXT5/BC7 dekoduoja Pillow.
- `dagorlevel.py`: lygio dvejetainis failas (`scene/loadLevel.cpp`), aukščio žemėlapis
  (`heightmap/heightmapPhysHandler.cpp`, `heightMapLand/compressedHeightmap.cpp`), žemės spindulių sekiklis
  (`landMesh/lmeshManager.cpp`, `landMesh/landRayTracerSoA4.cpp`) ir vandens aukščio žemėlapis (`fftWater/fftWater.cpp`).
- `rigen.py`: išdėstyti objektai (`rendInst/riGen/riGenData.h`, `rendInst/rendInstGen.cpp`,
  `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: generuoti objektai (`rendInst/rendInstGenLand.cpp`, `riGen/landClassData.h`,
  `riGen/genObjByMask.h`, `riGen/genObjByDensGridMask.h`, `riGen/genObjUtil.h`, `riGen/riGenData.h`,
  `riGen/multiPointData.h`, `riGen/riRotationPalette.h`, `rendInstGen.cpp` (`create`, `precomputeCell`,
  `generateCell`), `gameMath/objgenPrng.h`, `util/dag_roHugeHierBitMap2d.h`, `util/dag_hierBitMap2d.h`,
  `ioSys/dag_roDataBlock.h`, `ioSys/roDataBlk.cpp`, `gameRes/grpData.h`).
- `rendinst.py`: atvaizdavimo egzemplioriai (`shaders/rendInstRes.cpp`, `shaders/dag_rendInstRes.h`,
  `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`, `shaders/dag_shaderMesh.h`, `shaders/dag_shaderCommon.h`,
  `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`) ir meshoptimizer indeksų kodekas
  (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: žemės spalva (`landMesh/lmeshManager.cpp`, `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`,
  `lmeshRenderer.cpp`, `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`, `biomes.dshl`,
  `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`, `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`,
  `levelSplines/levelSplines.cpp`).
- `collision.py`: išteklių paketai (`gameRes/grpData.h`) ir susidūrimo ištekliai
  (`sharedInclude/gameRes/collResStream.h`, `gameRes/collisionGameResLoad.cpp`), kurių trikampiai saugomi kaip
  keturkampių BVH (`daBVH/bvhIO.cpp`, `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) skaito tuos pačius archyvus; jis nereikalingas ir čia nenaudojamas.

---

Dalis [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Šaltinis: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
