---
title: "Haritalar"
nav_order: 9
lang: tr
source: levels.md
source_hash: "1f750f25303d"
nav_exclude: true
search_exclude: true
---
# Haritalar (heat3d-wt-level) {#levels-heat3d-wt-level}

`heat3d-wt-level`, kendi War Thunder kurulumunuzun haritalarını görüntüleyici için `.glb` haritalarına çevirir;
tekrarların tablolarıyla aynı çerçevede.

## Adım adım {#step-by-step}

1. Kurulumunuzun haritalarını listeleyin: `heat3d-wt-level list`. Her harita için bir satır yazar: adı, arazisi
   ve haritaları, sonra sayı. Örneğin (uydurulmuş bir harita):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. Birini, birkaçını (joker karakterler serbest) ya da hepsini çıkarın:

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```

3. `levels/<level>/<level>.glb` dosyasını görüntüleyicinin Harita panelinde, o haritanın savaşlarının altında yükleyin.

Yazdığınız haritalar makinenizde kalır: bunları asla yayımlamayın (bkz. [Koşullar ve lisans](terms.md)).

## Seçenekler {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| Komut / seçenek | Ne yapar |
|---|---|
| `list [--game FOLDER]` | kurulumdaki her harita |
| `extract <levels...>` / `--all` | adı verilen haritalar (`list`in yazdığı gibi; joker karakterler serbest) ya da her harita |
| `-o`, `--out` | çıktı klasörü; her harita `<out>/<level>/` içine gider |
| `--game FOLDER` | War Thunder klasörü (varsayılan: Steam ya da başlatıcıdan bulunur; ayrıca `HEAT3D_WT_GAME`) |
| `--detail low/medium/high` | tank haritası üzerinde zemin örnekleme, zemin rengi ve nesne bütçesi (varsayılan `medium`) |
| `--max-object-triangles N` | nesne bütçesi (varsayılan: ayrıntınınki) |
| `--max-grid N` | parça başına bir kenardaki yükseklik haritası örneği (varsayılan 1024) |
| `--no-objects` | binaları, ağaçları ve diğer yerleştirilmiş nesneleri dışarıda bırakır |
| `--no-generated` | arazi sınıflarının ürettiği nesneleri (ormanlar, kasabalar) dışarıda bırakır |
| `--no-terrain-colour` | zemini arazi sınıfları yerine taktik haritayla kaplar |
| `--no-texture` | zemini dokusuz bırakır |
| `--skip-existing` | `.glb`si var olan haritaları atlar |

## Ne yazılır {#what-is-written}

Her harita `<out>/<level>/<level>.glb`, `<level>.json` (okunanlar, su seviyesi, harita dikdörtgenleri, üçgen
sayıları, süreler) ve haritanın taktik haritaları olan `<level>_map.png` (hava haritası) ve `<level>_tankmap.png`
olur; kara haritaları ayrıca `<level>_terrain.png` alır, yani tank haritasının üzerinde zeminin kendi renkleri.
glb, `<level>.glb.part` olarak yazılır ve tamamlanınca yeniden adlandırılır; bir harita yazılırken
`<out>/<level>/.<level>.lock` tutulur, böylece iki çıkarma asla aynı haritaya yazmaz (ikincisi `busy <level>`
yazar). Kurulum Steam ya da başlatıcının varsayılan klasörlerinden bulunur; aksi halde `--game <folder>` ya da
`HEAT3D_WT_GAME` yerini söyler.

| Parça | Nedir |
|---|---|
| `ground:<level>` | arazi yükseklik haritası (`HM2`) bir ızgara olarak; kara haritalarında tank haritasının ortası (genişliğinin yarısı) `--detail` adımında, arazi sınıfları, zemin çıkartmaları ve yollarla renklendirilmiş (`<level>_terrain.png`; bu yapılamıyorsa taktik harita); tank haritası olmayan haritalarda (hava haritaları), tüm yükseklik haritası tek bir adımda (`high`da kenar başına 2048 örnek, değilse 1024), hava haritasının alanı üzerinden arazi sınıflarıyla renklendirilmiş (kenarı 4096 piksel, 131 km üzerinde piksel başına yaklaşık 32 m; bu yapılamıyorsa taktik harita); yükseklik haritası olmayan haritalarda arazi ağı |
| `ground:<level> tank map` | tank haritasının kalanı, bir adım daha kaba |
| `ground:<level> heightmap surroundings` | yükseklik haritasının kalanı, daha da kaba |
| `ground:<level> land mesh` | yükseklik haritasının ulaşmadığı yerlerde arazi ağının çarpışma üçgenleri (tank haritasının çevresi, on kilometrelere kadar); yükseklik haritası olmayan haritalarda, yukarıdaki gibi renklendirilmiş zemin |
| `ground:<level> outside the map` | görüntünün kapsamadığı zemin, dokusuz |
| `water:<level>` | tüm arazinin üzerinde, haritanın `water_level` değerinde tek bir düz dikdörtgen: oyun suyu tek bir düzlem olarak çizer, altındaki alçak zemin deniz, göl ya da nehir yatağıdır |
| `water:<level> rivers` | su yükseklik haritası (`WHM`) olan haritalarda, kapladığı hücreler üzerindeki eğimli su yüzeyi |
| `structure:<level> buildings` | bitki olmayan her yerleştirilmiş nesne: evler, harabeler, duvarlar, çitler, köprüler, raylar, kayalar, dekorlar. Sabit olanlar (`RIGz`) ve tank haritası üzerinde arazi sınıflarının ürettikleri (kasaba blokları, taşlar). Her biri render ağıyla çizilir (duvarlar, çatılar, pencere açıklıkları, kirişler), üçgen bütçesinin izin verdiği LOD'da, her malzeme için difüz dokusunun ortalamasıyla renklendirilmiş |
| `structure:<level> trees` | ağaçlar ve çalılar, sabit ve üretilmiş (ormanlar, çitler): bütçe izin verirse render ağları, değilse ağacın kendi yaprak renginde bir gövde ve bir taç (iğne yapraklılar için koni), ağacın gerçek boyutunda |

Render ağı olmayan nesneler çarpışma şekline döner; ağacı olmayanlar taca. Tepe renkleri (`COLOR_0`) sRGB kodlu
değerleri tutar; 3DHeat görüntüleyicisi bunları böyle okur.

**Koordinatlar**, z aynalanmış oyun metreleridir: glb (x, y, z) = oyun (x, y, -z). Oyunun dünyası sol elli
(x doğu, y yukarı, z kuzey); glTF sağdan eldir. `heat3d-wt-replay` oyunun z'sini tutar ve görüntüleyiciye onu
aynalamasını söyler; böylece bir tekrar ile haritasının haritası hiçbir yerleştirme adımı olmadan üst üste
oturur. JSON, PNG'yi bir harita görüntüsü olarak yüklemek için her taktik haritanın dikdörtgenini oyun metresi
cinsinden ve köşelerini glb'nin uzayında verir.

**Ayrıntı.** `--detail low|medium|high` (varsayılan medium) tank haritası üzerinde şunları ayarlar:

| | tank haritasının ortası | tank haritasının kalanı | zemin rengi | nesne bütçesi | nesne başına en çok üçgen | üretilen bitkilerden tutulan |
|---|---|---|---|---|---|---|
| low | her 4. örnek | her 8. | piksel başına 4 m | 1,2 M | 1.500 | ağaçlar %35, çalılar %20 |
| medium | her 2. | her 4. | 2 m | 3,5 M | 4.000 | ağaçlar %70, çalılar %50 |
| high | her örnek (çoğu kara haritasında 2 m) | her 2. | 1 m (kenar başına en çok 4096 piksel) | 4,5 M | 12.000 | hepsi |

İki tank haritası halkası 0,3 M (low), 1 M (medium) ve 3,7 M (high) üçgende tutulur: yükseklik haritası 2 m'den
ince olan haritalarda adımlar sığana kadar iki katına çıkarılır (dış halka önce), böylece bunlar da yaklaşık 2 m
çıkar.

`high`da bir kara haritası yaklaşık 8 milyon üçgene (3,5 M zemin, 4,5 M nesne) ve 250 MB'a çıkar; `medium`da yaklaşık
4,5 M. Nesnelerin LOD'ları, oyunun tek bir görüş uzaklığından çizeceği LOD'lardır: toplamı bütçeye sığan en kısa
olan; küçük dekorlar önce kaba LOD'lara düşer, büyük binalar en son, her LOD için yapımcılarının verdiği aralıklara
göre (JSON'daki `lodDistance`); bu adımın bütçenin ötesinde kazandırdığı şey en büyük nesnelere geri gider. Kaba
zemin rengi (hava haritaları) her arazi sınıfının döşemeli dokularının ortalamasını önce piksel boyutuna indirir,
böylece döşemeler moire olarak bozulmaz. En kaba LOD'lar bile sığmazsa, en çok yer kazandıran ağaçlar tacolara
dönüşür, ardından en küçük türler dışarıda bırakılır (`leftOut`); hiçbir nesne kutu olarak çizilmez (varsa bir
çarpışma şekli, nesnenin kendisinindir).
Üretilmiş nesneler türüne (`density`) göre belirleyici olarak seyreltilir; her çalıştırmada aynı olanlar. `--max-object-triangles`
bütçeyi geçersiz kılar, `--max-grid` (varsayılan 1024) yükseklik haritasının kaba parçalarını sınırlar, `--no-objects`
nesneleri, `--no-generated` üretilenleri dışarıda bırakır, `--no-terrain-colour` zemini taktik haritayla dokular,
`--no-texture` dokusuz bırakır.

JSON'daki `parts.objects` örnekleri (sabit ve üretilmiş, türüne ve arazi sınıfına göre), kaçı hangi LOD'da çizildi
(`drawnAs`), üçgenler, LOD uzaklığı ve saniyeler; `parts.heightmap.rings` her zemin halkasının adımını ve üçgenlerini;
`parts.terrainColour` arazi sınıflarını ve renklerini, yolları ve zemin çıkartmalarını; `trianglesTotal`, `glbBytes`
ve `secondsBy` toplamları verir.

## Okunanlar ve ne kadar iyi {#what-is-read-and-how-well}

| Parça | Durum |
|---|---|
| Harita ikili dosyası (`levels/<level>.bin`, `DBLD` 3x64): blok tablosu | her harita denetlendi |
| Yükseklik haritası (`HM2`, sürüm 0-2; sürüm 2 bloklarda 8 bitlik değerler, Oodle ya da zstd parçaları) | Oodle parçalı sürüm 2 yükseklik haritası olan her harita; taktik haritalarıyla göz kararı denetlendi (nehirler, vadiler, kıyılar ve kasabalar hizalanır) |
| Arazi ağı çarpışması (`lmap`, `LTdump` arazi ışın izleyicisi) | haritanın sahip olduğu yerde okunur (Oodle paketli). Oyunun çarpışma yüzeyidir, render edilen ağ değildir; bu yüzden arazinin düz olduğu yerde daha kabadır |
| Zemin rengi (`lmap` arazi sınıfları ve ağırlık haritası, `LMp2` fizik haritası, `hspl` eğrileri) | arazi sınıflarının renk haritaları ve detay dokuları (ortalama renkleri) ağırlık haritasıyla ağırlıklandırılmış, indekslenmiş arazi sınıflarının 1 m biyom indeksi, fizik haritasının yol ve zemin çıkartma şekilleri eğrilerinin ya da malzemelerinin dokusunun rengiyle, dik yamaçlarda uçurumlar. Tank haritalarıyla denetlendi: yollar, kasabalar, göller, orman kuşakları ve kaya çıkıntıları hizalanır. War Thunder'ın kendi arazi gölgelendiricisinin renk formülü genel kaynakta yok; motorun yayımlanmış formülü (daNetGame) kullanılır, bu da taktik haritadan daha doygun çıkar |
| Su seviyesi | `aces.vromfs.bin` içindeki haritanın BLK'sinden `water_level` (yoksa 0) |
| Su yükseklik haritası (`WHM`: düz hücrelerden ve 16 bit yüksekliklerden oluşan 130x130 sayfalık bir ızgara) | haritanın sahip olduğu yerde okunur; nehirleri zeminle birlikte eğimlidir |
| Taktik haritalar | `content/base/res/locations_maps.dxp.bin` dosyasından, BLK'nin `mapCoord0/1` ve `tankMapCoord0/1` değerlerine göre yerleştirilmiş; görüntünün üstü kuzeydir |
| Yerleştirilmiş nesneler (`RIGz`: render örneği üreticisinin sabit örnekleri) | her örnek, 16 bitlik değerlerden oluşan 3x4 bir matris olarak ya da bazı haritalarda 32 bitlik (hücrenin bayt sayısı karar verir); denetlenen haritalarda her hücrenin her baytı hesaba katıldı |
| Üretilmiş nesneler (`RIGz` arazi sınıfı maskeleri ve `LandClass` kaynakları) | oyunun üreticisi, taşınmış: aynı yerler aynı sırayla, aynı rastgele sayılarla denenir; arazi sınıfı ve dışlama maskeleri, her yerde seçilen nesne, dönüşü, ölçeği ve yükseklik ofseti; döşemeli (kasaba blokları) ve dikilmiş (ormanlar, çalılar, tarlalar) varlıklar. Yalnızca tank haritası üzerinde üretilir. Yaklaşık olanlar: zemin yüksekliği ve normali (yükseklik haritasından; oyun bir ışın izler), oyunun çalışma zamanında kaydettiği dışlama kutuları ve ağaçların yaw'ı (oyun onu sahte görüntünün dönüş paletine oturtur) |
| Render ağları (`content/*/res/*.grp` içindeki `RendInst` kaynakları, `riDesc.bin` içindeki malzemeler) | her LOD'un köşeleri ve üçgenleri (kayan nokta konumlar; 16 ya da 32 bitlik indisler, düz ya da meshoptimizer paketli), her öğenin malzemesi. Çıkartma ve sahte-tabela öğeleri dışarıda kalır; saydam olanlar (cam) tutulur |
| Nesne renkleri | malzeme başına, difüz dokusunun küçük mip'inin ortalaması (yapraklar için alfa ağırlıklı), kurulumun doku paketlerinden: çoğu gölgelendirici için t0, t0 bir örtü ya da maske olduğunda ilk detay difüz. Malzeme başına bir renk: nesnelerde doku yok |
| Çarpışma şekilleri (`<object>_collision`) | akış sürüm 3 çarpışma kaynakları, bir nesnenin render ağı olmadığı yerde kullanılır. Yalnızca oyunun ışınlarının vurduğu (`TRACEABLE` düğümleri) çizilir; kutular, küreler ve kapsüller yalnızca kaynağın ağı yoksa: diğerleri nesnenin etrafında küp gibi görünecek kaba fizik vekilleridir |
| Navigasyon ağı (`Lnav`), render edilen arazi ağı, çimen, `spgz`, `stbl`, `d2co` | okunmaz |

Haritalar Oodle ile sıkıştırılır; Oodle tescilli bir kütüphanedir. Oyun bir kopyasını taşır,
`<War Thunder>\win-arm64ec\oo2core_9_win64.dll` (sıradan bir x64 derlemesi), ve yüklenen odur;
`HEAT3D_OODLE=<dll ya da klasör>` başka bir yeri gösterir. Oodle'ın hiçbir parçası burada yoktur.

## Biçimler ve nerede belgelendikleri {#formats-and-where-they-are-documented}

Gaijin, Dagor Engine'in kaynağını BSD 3-Clause lisansı altında yayımladı
(github.com/GaijinEntertainment/DagorEngine). Buradaki okuyucular ondan yazıldı; hiçbir oyun kodu
tersine derlenmedi. Her modül izlediği kaynak dosyalarını adlandırır:

- `vromfs.py`: `*.vromfs.bin` (başlık `VRFs`/`VRFx`, ilk ve son 16 baytı sabit bir anahtarla XOR'lanmış
  bir zstd gövdesi, bir ad tablosu ve bir ofset tablosu: `osApiWrappers/dag_vromfs.h`,
  `ioSys/vromfsLoad.cpp`, `supp/dag_zstdObfuscate.h`) ve ikili BLK (biçimler 1-5, arşivin ortak ad
  haritası `\xff?nm` ve zstd sözlüğüyle: `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`,
  `blk_zstd.cpp`).
- `dxp.py`: doku paketleri `DxP2` (`lib3d/texPackMgr2.cpp`) ve DDSx başlıkları
  (`sharedInclude/3d/ddsxTex.h`); DXT1/DXT5/BC7 Pillow ile çözülür.
- `dagorlevel.py`: harita ikili dosyası (`scene/loadLevel.cpp`), yükseklik haritası
  (`heightmap/heightmapPhysHandler.cpp`, `heightMapLand/compressedHeightmap.cpp`), arazi ışın izleyicisi
  (`landMesh/lmeshManager.cpp`, `landMesh/landRayTracerSoA4.cpp`) ve su yükseklik haritası
  (`fftWater/fftWater.cpp`).
- `rigen.py`: yerleştirilmiş nesneler (`rendInst/riGen/riGenData.h`, `rendInst/rendInstGen.cpp`,
  `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: üretilmiş nesneler (`rendInst/rendInstGenLand.cpp`, `riGen/landClassData.h`,
  `riGen/genObjByMask.h`, `riGen/genObjByDensGridMask.h`, `riGen/genObjUtil.h`, `riGen/riGenData.h`,
  `riGen/multiPointData.h`, `riGen/riRotationPalette.h`, `rendInstGen.cpp` (`create`, `precomputeCell`,
  `generateCell`), `gameMath/objgenPrng.h`, `util/dag_roHugeHierBitMap2d.h`,
  `util/dag_hierBitMap2d.h`, `ioSys/dag_roDataBlock.h`, `ioSys/roDataBlk.cpp`, `gameRes/grpData.h`).
- `rendinst.py`: render örnekleri (`shaders/rendInstRes.cpp`, `shaders/dag_rendInstRes.h`,
  `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`, `shaders/dag_shaderMesh.h`,
  `shaders/dag_shaderCommon.h`, `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`) ve
  meshoptimizer'ın indis kodeki (`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: zeminin rengi (`landMesh/lmeshManager.cpp`, `lmeshLandClasses.cpp`,
  `lmeshWeightAtlas*.cpp`, `lmeshRenderer.cpp`, `landMesh/shaders/land_weight_atlas.hlsli`,
  `land_weight_inc.dshl`, `biomes.dshl`, `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`,
  `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`, `levelSplines/levelSplines.cpp`).
- `collision.py`: kaynak paketleri (`gameRes/grpData.h`) ve çarpışma kaynakları
  (`sharedInclude/gameRes/collResStream.h`, `gameRes/collisionGameResLoad.cpp`); üçgenleri bir dörtlü BVH olarak
  saklanır (`daBVH/bvhIO.cpp`, `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli (Apache-2.0) aynı arşivleri okur; buna ihtiyaç yoktur ve kullanılmaz.

---

[3DHeat](https://github.com/Holdi601/3DHeat) parçası ([belgeler](https://holdi601.github.io/3DHeat/)). Kaynak: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
