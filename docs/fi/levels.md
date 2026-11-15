---
title: Kentät (heat3d-wt-level)
nav_order: 9
lang: "fi"
source: levels.md
source_hash: "8fd5f4d94b76"
nav_exclude: true
search_exclude: true
---
# Kentät (heat3d-wt-level) {#levels-heat3d-wt-level}

`heat3d-wt-level` muuttaa asennuksesi War Thunderin kentät katselimen `.glb`-kentiksi samassa
koordinaatistossa kuin replayjen taulukot.

## Vaihe vaiheelta {#step-by-step}

1. Listaa asennuksesi kentät: `heat3d-wt-level list`. Se tulostaa yhden rivin kenttää kohden:
   sen nimen, maastonsa ja karttansa, sitten määrän. Esimerkki (keksitty kenttä):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Pura yksi, useita (jokerimerkit sallittu) tai kaikki:

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```
3. Lataa `levels/<level>/<level>.glb` katselimen Tausta / kenttä -paneeliin, sen kartan taistelujen alle.

Kirjoittamasi kentät pysyvät omalla koneellasi: älä koskaan julkaise niitä (katso
[Ehdot ja lisenssi](terms.md)).

## Valinnat {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Komento / valinta | Tekee |
|---|---|
| `list [--game FOLDER]` | jokainen kenttä asennuksessa |
| `extract <levels...>` / `--all` | nimetyt kentät (kuten `list` ne tulostaa; jokerimerkit sallittu), tai kaikki kentät |
| `-o`, `--out` | tulostuskansio; jokainen kenttä menee kansioon `<out>/<level>/` |
| `--game FOLDER` | War Thunderin kansio (oletus: löytyy Steamin tai käynnistimen kautta; myös `HEAT3D_WT_GAME`) |
| `--detail low/medium/high` | maanäytteistys, maanvärit ja objektibudjetti panssarikartan yli (oletus `medium`) |
| `--max-object-triangles N` | objektibudjetti (oletus: kentän mukainen) |
| `--max-grid N` | korkeuskartan näytteitä sivua kohden, osaa kohden (oletus 1024) |
| `--no-objects` | jätä pois rakennukset, puut ja muut sijoitetut objektit |
| `--no-generated` | jätä pois maaluokkien generoimat objektit (metsät, kaupungit) |
| `--no-terrain-colour` | pinnoita maasto taktisella kartalla, ei maaluokilla |
| `--no-texture` | jätä maasto ilman pintakuviota |
| `--skip-existing` | jätä kentät, joiden `.glb` on jo olemassa |

## Mitä kirjoitetaan {#what-is-written}

Jokaisesta kentästä tulee `<out>/<level>/<level>.glb`, `<level>.json` (mitä luettiin, veden korkeus,
karttasuorakulmiot, kolmiomäärät, ajoitukset) ja kentän taktiset kartat `<level>_map.png` (ilmakartta)
ja `<level>_tankmap.png` (panssarikartta); maakartoille tulee myös `<level>_terrain.png`, maan omat
värit panssarikartan päälle. `.glb` kirjoitetaan tiedostoon `<level>.glb.part` ja nimetään uudelleen
valmistuttua; kentän kirjoituksen ajan `<out>/<level>/.<level>.lock` on varattuna, joten kaksi
purkua ei kirjoita samaa kenttää (toinen tulostaa `busy <level>`). Asennus löytyy Steamin tai
käynnistimen oletuskansioista; `--game <kansio>` tai `HEAT3D_WT_GAME` kertovat muun sijainnin.

| Osa | Mitä se on |
|---|---|
| `ground:<level>` | maaston korkeuskartta (`HM2`) ruudukkona; maakartoilla panssarikartan keskiosa (puolet sen leveydestä) `--detail`-askeleella, värjättynä maaluokilla, maa-alueen merkinnöillä ja teillä (`<level>_terrain.png`; taktinen kartta, jos sitä ei voi tehdä); ilmakartoilla, joilla ei ole panssarikarttaa, koko korkeuskartta yhdellä askeleella (2048 näytettä sivua kohden `high`-tasolla, muuten 1024), värjättynä maaluokilla ilmakartan alueen yli (4096 pikseliä sivua kohden, noin 32 m pikseli 131 km:n alueella; taktinen kartta, jos sitä ei voi tehdä); kentillä ilman korkeuskarttaa maaverkko |
| `ground:<level> tank map` | panssarikartan loppuosa, yhden askeleen karkeampana |
| `ground:<level> heightmap surroundings` | korkeuskartan loppuosa, vielä karkeampana |
| `ground:<level> land mesh` | maaverkon törmäyskolmiot siellä, missä korkeuskartta ei yllä (panssarikartan ympäristö, kymmenien kilometrien päähän); kentillä ilman korkeuskarttaa se on maa, värjättynä kuten edellä |
| `ground:<level> outside the map` | kuvan peittämätön maa, ilman pintakuviota |
| `water:<level>` | yksi tasainen suorakulmio kentän `water_level`-korkeudella koko maaston yllä: peli piirtää veden yhtenä tasona, ja sen alla oleva matala maa on merta, järveä tai joen pohjaa |
| `water:<level> rivers` | kentillä, joilla on vesikorkeuskartta (`WHM`), kaltevat vesipinnat niiden solujen yllä, joita ne peittävät |
| `structure:<level> buildings` | jokainen sijoitettu objekti, joka ei ole kasvi: talot, rauniot, seinät, aidat, sillat, rautatiet, kivet, kalusteet. Kiinteät (`RIGz`) ja panssarikartan yllä ne, joita maaluokat generoivat (kaupunkikorttelit, kivet). Jokainen piirretään omalla renderointiverkollaan (seinät, katot, ikkuma-aukot, palkit) sillä LOD-tasolla, jonka kolmiobudjetti sallii, ja värjätään materiaaleittain sen diffuusitekstuurin keskiarvolla |
| `structure:<level> trees` | puut ja pensaat, kiinteät ja generoidut (metsät, pensasaidat): niiden renderointiverkko, kun budjetti sallii, muuten runko ja latvus (kartio havupuille) puun oman lehtiväriin, puun todellisessa koossa |

Objekteilla ilman renderointiverkkoa on törmäysmuoto; puilla ilman sitä latvus.
Kärkipisteiden värit (`COLOR_0`) ovat sRGB-koodattuja arvoja, ja juuri näin 3DHeat-katselin ne lukee.

**Koordinaatit** ovat pelin metrejä, z peilattuna: glb (x, y, z) = peli (x, y, -z). Pelin maailma on
vasenkätinen (x itään, y ylös, z pohjoiseen); glTF on oikeakätinen. `heat3d-wt-replay` säilyttää pelin
z:n ja kertoo katselimelle, että se peilataan, joten replay ja sen kartan kenttä osuvat päällekkäin
ilman sijoitusvaihetta. JSON antaa kunkin taktisen kartan suorakulmion pelin metreinä ja sen kulmat
glb-avaruudessa PNG-kuvan lataamista varten karttana.

**Yksityiskohdat.** `--detail low|medium|high` (oletus medium) asettaa panssarikartan yli:

| | panssarikartan keskiosa | panssarikartan loppuosa | maaväri | objektibudjetti | eniten kolmioita objektia kohden | säilytetyt generoidut kasvit |
|---|---|---|---|---|---|---|
| low | joka 4. näyte | joka 8. | 4 m pikseli | 1,2 M | 1 500 | puut 35 %, pensaat 20 % |
| medium | joka 2. | joka 4. | 2 m | 3,5 M | 4 000 | puut 70 %, pensaat 50 % |
| high | joka näyte (2 m useimmilla maakartoilla) | joka 2. | 1 m (enintään 4096 pikseliä sivua kohden) | 4,5 M | 12 000 | kaikki |

Kahta panssarikartan rengasta rajoitetaan kolmioihin 0,3 M (low), 1 M (medium) ja 3,7 M (high):
kartoilla, joiden korkeuskartta on tarkempi kuin 2 m, askeleet kaksinkertaistuvat (ulompi rengas
ensin), kunnes ne mahtuvat, joten nekin tulevat noin 2 m:n tarkkuuteen.

Maakartta `high`-tasolla tulee noin 8 miljoonalla kolmiolla (3,5 M maata, 4,5 M objekteja) ja 250 MB;
`medium`-tasolla noin 4,5 M. Objektien LOD-tasot ovat ne, jotka peli itse piirtäisi yhdestä
katseluetäisyydestä: lyhin, jonka kokonaismäärä mahtuu budjettiin. Pienet esineet putoavat
karkeisiin LOD-tasoihin ensin ja suuret rakennukset viimeisinä, valmistajan antamien
etäisyyksien mukaan (JSON:n `lodDistance`); mitä askel säästää budjetin ylitse, palautetaan suurimmille
objekteille. Karkea maaväri (ilmakartat) keskiarvoistaa jokaisen maaluokan kaakeloidut
tekstuurit ensin pikselikokoon, jotta kaakelit eivät aliasoi kuvioksi. Jos jopa karkeimmat LOD-tasot
eivät mahdu, eniten säästävät puut muuttuvat latvuksiksi, ja pienimmät tyypit jätetään pois
(`leftOut`); mitään objektia ei piirretä laatikkona (törmäysmuoto, jos sellainen on, on objektin oma).
Generoidut objektit harvennetaan deterministisesti tyypin mukaan (`density`), samoihin kohtiin joka
ajossa. `--max-object-triangles` ohittaa budjetin, `--max-grid` (oletus 1024) rajoittaa korkeuskartan
karkeampia osia, `--no-objects` jättää objektit pois, `--no-generated` generoidut, `--no-terrain-colour`
pinnoittaa maaston taktisella kartalla ja `--no-texture` jättää sen ilman pintakuviota.

JSON:n `parts.objects` luettelee ilmentymät (kiinteät ja generoidut, tyypin ja maaluokan mukaan), kuinka
monta piirrettiin millä LOD-tasolla (`drawnAs`), kolmiot, LOD-etäisyyden ja sekunnit; `parts.heightmap.rings`
kunkin maarenkaan askeleen ja kolmiot; `parts.terrainColour` maaluokat ja niiden värit, tiet ja
maa-alueen merkinnät; `trianglesTotal`, `glbBytes` ja `secondsBy` kokonaissummat.

## Mitä luetaan ja kuinka hyvin {#what-is-read-and-how-well}

| Osa | Tila |
|---|---|
| Kentän binääri (`levels/<level>.bin`, `DBLD` 3x64): lohkotaulukko | jokainen kenttä tarkistettu |
| Korkeuskartta (`HM2`, versiot 0-2; versio 2 on 8-bittisiä arvoja lohkoissa, Oodle- tai zstd-paloina) | jokainen kenttä, jonka korkeuskartta on versio 2 Oodle-paloin; tarkistettu silmämääräisesti taktisia karttoja vasten (joet, laaksot, rannikot ja kaupungit osuvat kohdalleen) |
| Maaverkon törmäys (`lmap`, sen `LTdump`-maasäteenjäljitin) | luetaan kentillä, joilla sellainen on (Oodle-pakattu). Se on pelin törmäyspinta, ei piirretty verkko, joten se on karkeampi tasaisella maalla |
| Maaväri (`lmap`-maaluokat ja painokartta, `LMp2`-fysiikkakartta, `hspl`-splinet) | maaluokkien värikartat ja yksityiskohtatekstuurit (niiden keskivärit) painotettuna painokartalla, indeksoitujen maaluokkien 1 m:n biomi-indeksi, fysiikkakartan tie- ja maa-alueen muodot niiden splinen tai materiaalin tekstuurin värissä, jyrkillä rinteillä rotkot. Tarkistettu panssarikarttoja vasten: tiet, kaupungit, järvet, metsävyöhykkeet ja kallioulokkeet osuvat kohdalleen. War Thunderin oman maavarjostimen värikaava ei ole julkisessa lähdekoodissa; käytetään moottorin julkaistua (daNetGame), joka on kylläisempi kuin taktinen kartta |
| Vedenpinta | `water_level` kentän BLK:sta `aces.vromfs.bin`-tiedostossa (0, jos sitä ei ole) |
| Vesikorkeuskartta (`WHM`: ruudukko tasaisia soluja ja 130x130 sivua 16-bittisiä korkeuksia) | luetaan kentillä, joilla sellainen on; sen joet kaltevat maan mukana |
| Taktiset kartat | tiedostosta `content/base/res/locations_maps.dxp.bin`, sijoitettuna BLK:n `mapCoord0/1`- ja `tankMapCoord0/1`-arvoilla; kuvan yläreuna on pohjoinen |
| Sijoitetut objektit (`RIGz`: renderointi-ilmentymien generaattorin kiinteät ilmentymät) | jokainen ilmentymä, 3x4-matriisina 16-bittisinä arvoina tai joillakin kentillä 32-bittisinä (solun tavumäärä ratkaisee); jokainen solun tavu täsmää kentillä, jotka tarkistettiin |
| Generoidut objektit (`RIGz`:n maaluokkamaskit ja `LandClass`-resurssit) | pelin generaattori, siirrettynä: samat paikat kokeillaan samassa järjestyksessä samoilla satunnaisluvuilla, maaluokka- ja poissulkemismaskit, kussakin paikassa valittu objekti, sen kierto, mittakaava ja korkeusoffset; kaakeloidut (kaupunkikorttelit) ja istutetut (metsät, pensaat, pellot) yksiköt. Generoidaan vain panssarikartan yli. Likimääräisesti: maan korkeus ja normaali (korkeuskartasta; peli jäljittää säteen), ajonaikaiset poissulkemislaatikot ja puiden kääntö (peli kohdistaa sen kuvakkeen kiertopalettiin) |
| Renderointiverkot (`RendInst`-resurssit `content/*/res/*.grp`-tiedostoissa, materiaalit `riDesc.bin`-tiedostossa) | jokaisen LOD-tason kärkipisteet ja kolmiot (liukulukusijainnit; 16- tai 32-bittiset indeksit, tavallisina tai meshoptimizer-pakattuina), jokaisen elementin materiaali. Kuvan ja impostorin laatta-elementit jätetään pois; läpinäkyvät (lasi) säilytetään |
| Objektien värit | materiaaleittain diffuusitekstuurin pienen mipin keskiarvo (alfapainotettu lehdille), asennuksen tekstuuripakkauksista: t0 useimmille varjostimille, ensimmäinen yksityiskohtadiffuusi, kun t0 on peite tai maski. Yksi väri materiaalia kohden: objekteilla ei ole tekstuuria |
| Törmäysmuodot (`<object>_collision`) | törmäysresurssit, versio 3 streamia, käytetään objektille, jolla ei ole renderointiverkkoa. Piirretään vain se, mihin pelin säteet osuvat (`TRACEABLE`-solmut), ja laatikot, pallot ja kapselit vain, kun resurssissa ei ole verkkoa: muu on karkeita fysiikkakorvikkeita, jotka näkyisivät kuutioina objektin ympärillä |
| Navigointiverkko (`Lnav`), piirretty maaverkko, ruoho, `spgz`, `stbl`, `d2co` | ei luettu |

Kentät on pakattu Oodle-pakkausohjelmalla, joka on omistusoikeudellinen. Peli toimittaa kopion,
`<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (tavallinen x64-versio), ja se ladataan. `HEAT3D_OODLE=<dll tai kansio>`
osoittaa muuhun. Mitään Oodlea ei ole mukana täällä.

## Muodot ja niiden dokumentointi {#formats-and-where-they-are-documented}

Gaijin julkaisi Dagor Enginen lähdekoodin BSD 3-Clause -lisenssillä (github.com/GaijinEntertainment/DagorEngine).
Täällä olevat lukijat on kirjoitettu siitä; pelin koodia ei ole purettu. Jokainen moduuli nimeää
lähdetiedostot, joita se seuraa:

- `vromfs.py`: `*.vromfs.bin` (otsikko `VRFs`/`VRFx`, zstd-runko, jonka ensimmäiset ja viimeiset 16 tavua
  on XOR-salattu kiinteällä avaimella, nimitaulu ja siirtymätaulu:
  `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`, `supp/dag_zstdObfuscate.h`)
  ja binäärinen BLK (muodot 1-5, arkiston yhteinen nimikartta `\xff?nm` ja zstd-sanakirja:
  `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`, `blk_zstd.cpp`).
- `dxp.py`: tekstuuripakkaukset `DxP2` (`lib3d/texPackMgr2.cpp`) ja DDSx-otsikot
  (`sharedInclude/3d/ddsxTex.h`); DXT1/DXT5/BC7 dekoodaa Pillow.
- `dagorlevel.py`: kentän binääri (`scene/loadLevel.cpp`), korkeuskartta
  (`heightmap/heightmapPhysHandler.cpp`, `heightMapLand/compressedHeightmap.cpp`),
  maasäteenjäljitin (`landMesh/lmeshManager.cpp`, `landMesh/landRayTracerSoA4.cpp`) ja
  vesikorkeuskartta (`fftWater/fftWater.cpp`).
- `rigen.py`: sijoitetut objektit (`rendInst/riGen/riGenData.h`, `rendInst/rendInstGen.cpp`,
  `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: generoidut objektit (`rendInst/rendInstGenLand.cpp`, `riGen/landClassData.h`,
  `riGen/genObjByMask.h`, `riGen/genObjByDensGridMask.h`, `riGen/genObjUtil.h`, `riGen/riGenData.h`,
  `riGen/multiPointData.h`, `riGen/riRotationPalette.h`, `rendInstGen.cpp` (`create`, `precomputeCell`,
  `generateCell`), `gameMath/objgenPrng.h`, `util/dag_roHugeHierBitMap2d.h`,
  `util/dag_hierBitMap2d.h`, `ioSys/dag_roDataBlock.h`, `ioSys/roDataBlk.cpp`, `gameRes/grpData.h`).
- `rendinst.py`: renderointi-ilmentymät (`shaders/rendInstRes.cpp`, `shaders/dag_rendInstRes.h`,
  `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`, `shaders/dag_shaderMesh.h`,
  `shaders/dag_shaderCommon.h`, `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`) ja
  meshoptimizerin indeksikoodekki (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: maan väri (`landMesh/lmeshManager.cpp`, `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`,
  `lmeshRenderer.cpp`, `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`,
  `biomes.dshl`, `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`,
  `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`, `levelSplines/levelSplines.cpp`).
- `collision.py`: resurssipaketit (`gameRes/grpData.h`) ja törmäysresurssit
  (`sharedInclude/gameRes/collResStream.h`, `gameRes/collisionGameResLoad.cpp`), joiden kolmiot on
  tallennettu neliö-BVH:na (`daBVH/bvhIO.cpp`, `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) lukee samat arkistot; sitä ei tarvita eikä käytetä.

---

Osa [3DHeatiä](https://github.com/Holdi601/3DHeat) ([dokumentaatio](https://holdi601.github.io/3DHeat/)). Lähde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
