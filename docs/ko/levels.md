---
title: 레벨
nav_order: 9
lang: ko
source: levels.md
source_hash: "1f750f25303d"
nav_exclude: true
search_exclude: true
---
# 레벨 (heat3d-wt-level) {#levels-heat3d-wt-level}

`heat3d-wt-level`은 여러분의 워 썬더 설치본에 있는 레벨을 뷰어용 `.glb` 레벨로 바꿔요. 리플레이 테이블과 같은 좌표계로요.

## 단계별 안내 {#step-by-step}

1. 설치본의 레벨 목록을 봐요: `heat3d-wt-level list`. 레벨마다 한 줄씩 나와요. 이름, 지형, 맵, 그리고 마지막에 개수가 나와요. 예를 들면(가상의 레벨):

   ```text
   99_testmap    heightmap 2048x2048 @ 2 m, land mesh    maps: 99_testmap_map, 99_testmap_tankmap
   1 levels in C:\Games\War Thunder
   ```
2. 하나, 여러 개(와일드카드 가능), 또는 전부를 꺼내요:

   ```bash
   heat3d-wt-level extract <level> -o levels
   heat3d-wt-level extract --all -o levels
   heat3d-wt-level extract <level> -o levels --detail high
   ```

3. `levels/<level>/<level>.glb`를 뷰어의 레벨 패널에서 불러와요. 그 맵의 전투 아래에 올라가요.

변환해서 만든 레벨은 여러분의 컴퓨터에만 두세요. 절대 공개하지 마세요([용어와 라이선스](terms.md) 참고).

## 옵션 {#options}

![heat3d-wt-level extract --help](../assets/img/level-help.svg)

| 명령 / 옵션 | 역할 |
|---|---|
| `list [--game FOLDER]` | 설치본의 모든 레벨 |
| `extract <levels...>` / `--all` | 적은 레벨들(`list`가 보여 주는 이름대로; 와일드카드 가능), 또는 모든 레벨 |
| `-o`, `--out` | 출력 폴더; 레벨마다 `<out>/<level>/` 안에 들어가요 |
| `--game FOLDER` | 워 썬더 폴더(기본값: Steam이나 런처를 통해 찾음; `HEAT3D_WT_GAME`도 가능) |
| `--detail low/medium/high` | 큰 맵 위의 지상 샘플링, 지면 색, 오브젝트 예산(기본값 `medium`) |
| `--max-object-triangles N` | 오브젝트 예산(기본값: detail 값) |
| `--max-grid N` | 부분마다 한 변의 높이맵 샘플 수(기본값 1024) |
| `--no-objects` | 건물, 나무, 그 밖에 배치된 오브젝트를 뺌 |
| `--no-generated` | 지형 클래스가 만든 오브젝트(숲, 마을)를 뺌 |
| `--no-terrain-colour` | 지형 클래스 대신 전술 지도로 지면에 질감을 입힘 |
| `--no-texture` | 지면에 질감을 입히지 않음 |
| `--skip-existing` | `.glb`가 있는 레벨은 건너뜀 |

## 무엇이 쓰이나 {#what-is-written}

각 레벨은 `<out>/<level>/<level>.glb`, `<level>.json`(읽은 내용, 물의 높이, 맵 사각형, 삼각형 수, 시간), 그리고 레벨의 전술 지도인 `<level>_map.png`(공중 지도)와 `<level>_tankmap.png`가 돼요. 지상 맵은 `<level>_terrain.png`도 만들어요. 지면 자체의 색을 전차 지도 위에 올린 그림이에요. glb는 `<level>.glb.part`로 쓰고, 끝나면 이름을 바꿔요. 레벨을 쓰는 동안 `<out>/<level>/.<level>.lock` 잠금 파일이 유지돼서, 두 추출이 같은 레벨을 동시에 쓰지 못해요(두 번째는 `busy <level>`을 출력해요). 설치본은 Steam이나 런처의 기본 폴더에서 찾아요. 다른 곳에 있다면 `--game <폴더>`나 `HEAT3D_WT_GAME`으로 알려 주세요.

| 부분 | 내용 |
|---|---|
| `ground:<level>` | 지형 높이맵(`HM2`)을 격자로. 지상 맵에서는 전차 지도의 가운데(폭의 절반)를 `--detail`의 간격으로, 지층 클래스, 지면 데칼, 도로로 색을 입혀요(`<level>_terrain.png`; 그럴 수 없으면 전술 지도). 전차 지도가 없는 공중 맵에서는 높이맵 전체를 한 간격으로(`high`에서는 한 변 2048 샘플, 나머지는 1024), 공중 지도의 영역 위에 지층 클래스로 색을 입혀요(한 변 4096 픽셀, 131 km에 걸쳐 픽셀당 약 32 m; 그럴 수 없으면 전술 지도). 높이맵이 없는 레벨은 지면 메시 |
| `ground:<level> tank map` | 전차 지도의 나머지 부분을 한 단계 성기게 |
| `ground:<level> heightmap surroundings` | 높이맵의 나머지를 더 성기게 |
| `ground:<level> land mesh` | 높이맵이 닿지 않는 곳의 지면 메시 충돌 삼각형(전차 지도 주변, 수십 km까지). 높이맵이 없는 레벨에서는 위와 같은 색을 입힌 지면 |
| `ground:<level> outside the map` | 이미지가 덮지 않는 지면, 질감 없음 |
| `water:<level>` | 모든 지형 위에 레벨의 `water_level` 높이에 놓인 평평한 사각형 하나. 게임은 물을 평면 하나로 그리고, 그 아래의 낮은 땅은 바다, 호수, 강바닥이에요 |
| `water:<level> rivers` | 물 높이맵(`WHM`)이 있는 레벨에서, 그 칸을 덮는 경사진 물 표면 |
| `structure:<level> buildings` | 식물이 아닌 배치된 모든 오브젝트: 집, 폐허, 벽, 울타리, 다리, 철로, 바위, 소품. 고정된 것(`RIGz`)과, 전차 지도 위에서 지형 클래스가 만든 것(마을 블록, 돌)을 포함해요. 각각 렌더 메시(벽, 지붕, 창문 구멍, 보)로 그리고, 예산이 허락하는 LOD로 그려요. 재질마다 확산 질감의 평균으로 색을 입혀요 |
| `structure:<level> trees` | 나무와 덤불, 고정된 것과 만들어진 것(숲, 생울타리). 예산이 허락하면 렌더 메시로, 아니면 나무 고유의 잎 색으로 된 줄기와 수관(침엽수는 원뿔)으로, 나무의 실제 크기에 맞춰서요 |

렌더 메시가 없는 오브젝트는 충돌 형상으로 대신하고, 메시가 없는 나무는 수관으로 대신해요. 정점 색(`COLOR_0`)은 sRGB로 인코딩된 값을 담아요. 3DHeat 뷰어는 그 값을 그렇게 읽어요.

**좌표**는 게임의 미터 단위이고 z는 뒤집혀 있어요: glb (x, y, z) = 게임 (x, y, -z). 게임 세계는 왼손 좌표계예요(x 동, y 위, z 북). glTF는 오른손 좌표계예요. `heat3d-wt-replay`는 게임의 z를 그대로 두고, 뷰어에게 z를 뒤집으라고 알려 줘요. 그래서 리플레이와 그 맵의 레벨은 위치를 옮기지 않아도 정확히 겹쳐요. JSON에는 각 전술 지도의 사각형이 게임의 미터 단위로 있고, 모서리는 glb 공간에 있어요. 그래서 PNG를 지도 이미지로 불러올 수 있어요.

**세부 수준.** `--detail low|medium|high`(기본값 medium)은 전차 지도 위에서 다음을 정해요:

| | 전차 지도 가운데 | 전차 지도의 나머지 | 지면 색 | 오브젝트 예산 | 오브젝트당 가장 많은 삼각형 | 만들어진 식물 유지 |
|---|---|---|---|---|---|---|
| low | 4번째 샘플마다 | 8번째마다 | 픽셀당 4 m | 1.2 M | 1,500 | 나무 35 %, 덤불 20 % |
| medium | 2번째마다 | 4번째마다 | 2 m | 3.5 M | 4,000 | 나무 70 %, 덤불 50 % |
| high | 모든 샘플(대부분의 지상 맵에서 2 m) | 2번째마다 | 1 m(한 변 최대 4096 픽셀) | 4.5 M | 12,000 | 전부 |

두 전차 지도 고리는 low에서 0.3 M, medium에서 1 M, high에서 3.7 M 삼각형으로 맞춰요. 높이맵이 2 m보다 촘촘한 맵에서는 간격을 두 배씩 늘려서(바깥 고리부터) 맞춰요. 그래서 그 맵들도 약 2 m가 돼요.

`high`에서 지상 맵은 약 800만 삼각형(지면 350만, 오브젝트 450만)과 250 MB가 나와요. `medium`에서는 약 450만 삼각형이에요. 오브젝트의 LOD는 게임이 한 거리에서 그리는 것과 같아요. 예산 안에 맞는 가장 짧은 것이에요. 작은 소품은 가장 먼저 거친 LOD로 내려가고, 큰 건물은 마지막에 내려가요. 기준은 제작자가 LOD마다 준 범위(JSON의 `lodDistance`)예요. 예산을 넘어서 줄어든 만큼은 가장 큰 오브젝트로 되돌려요. 공중 맵의 거친 지면 색은 먼저 지층 클래스마다 타일 질감을 픽셀 크기로 평균내서, 타일이 모아레를 만들지 않게 해요. 가장 거친 LOD로도 맞지 않으면, 가장 많이 줄여 주는 나무가 수관이 되고, 그다음 가장 작은 종류는 빠져요(`leftOut`). 어떤 오브젝트도 상자로 그리지 않아요(충돌 형상이 있다면 그 오브젝트 자신의 것이에요). 만들어진 오브젝트는 종류(`density`)별로 결정론적으로 솎아 내요. 그래서 실행할 때마다 같은 것들이 남아요. `--max-object-triangles`는 예산을 덮어쓰고, `--max-grid`(기본값 1024)는 높이맵의 성긴 부분에 상한을 두고, `--no-objects`는 오브젝트를 빼고, `--no-generated`는 만들어진 것을 빼고, `--no-terrain-colour`는 지면에 전술 지도 질감을 입히고, `--no-texture`는 지면에 질감을 입히지 않아요.

JSON의 `parts.objects`에는 인스턴스(고정된 것과 만들어진 것, 종류와 지층 클래스별)가 있고, 각각 어떤 LOD로 몇 개를 그렸는지(`drawnAs`), 삼각형, LOD 거리, 걸린 초가 있어요. `parts.heightmap.rings`에는 지면 고리마다 간격과 삼각형이 있어요. `parts.terrainColour`에는 지층 클래스와 그 색, 도로와 지면 데칼이 있어요. `trianglesTotal`, `glbBytes`, `secondsBy`는 전체 합계예요.

## 무엇을 읽고, 얼마나 잘 읽나 {#what-is-read-and-how-well}

| 부분 | 상태 |
|---|---|
| 레벨 바이너리(`levels/<level>.bin`, `DBLD` 3x64): 블록 표 | 모든 레벨 확인 |
| 높이맵(`HM2`, 버전 0-2; 버전 2는 블록 안의 8비트 값, Oodle 또는 zstd 청크) | 버전 2이고 Oodle 청크를 쓰는 모든 레벨; 전술 지도와 눈으로 대조했어요(강, 계곡, 해안, 마을이 맞아요) |
| 지면 메시 충돌(`lmap`, 그 `LTdump` 지면 광선 추적기) | 레벨에 있는 곳에서 읽어요(Oodle로 압축). 렌더링되는 메시가 아니라 게임의 충돌 표면이라서, 평평한 땅에서는 더 거칠어요 |
| 지면 색(`lmap` 지층 클래스와 가중치 맵, `LMp2` 물리 맵, `hspl` 스플라인) | 지층 클래스의 색 지도와 세부 질감(평균 색)을 가중치 맵으로 섞어요. 가중치 맵은 인덱스된 지층 클래스의 1 m 생물군 인덱스예요. 물리 맵의 도로와 지면 데칼 모양은 스플라인이나 재질의 질감 색으로 칠해요. 가파른 비탈에는 절벽을 그려요. 전차 지도와 대조했어요: 도로, 마을, 호수, 숲띠, 바위 노두가 맞아요. 워 썬더 자체 지형 셰이더의 색 공식은 공개 소스에 없어요. 그래서 엔진의 공개 공식(daNetGame)을 써요. 이것은 전술 지도보다 더 채도가 높게 나와요 |
| 물 높이 | 레벨의 BLK에 있는 `water_level`(`aces.vromfs.bin`). 없으면 0 |
| 물 높이맵(`WHM`: 평평한 칸의 격자와, 16비트 높이로 된 130x130 페이지) | 레벨에 있는 곳에서 읽어요. 강은 지면을 따라 경사져요 |
| 전술 지도 | `content/base/res/locations_maps.dxp.bin`에서. BLK의 `mapCoord0/1`과 `tankMapCoord0/1`로 놓아요. 이미지의 위쪽은 북쪽이에요 |
| 배치된 오브젝트(`RIGz`: 렌더 인스턴스 생성기의 고정 인스턴스) | 모든 인스턴스. 16비트 값의 3x4 행렬이고, 일부 레벨에서는 32비트 값이에요(셀의 바이트 수로 정해요). 확인한 레벨에서는 모든 셀의 모든 바이트를 설명할 수 있어요 |
| 만들어진 오브젝트(`RIGz` 지층 마스크와 `LandClass` 리소스) | 게임의 생성기를 옮긴 것이에요. 같은 자리를 같은 순서로, 같은 난수로 시도하고, 지층과 제외 마스크, 그 자리에서 고르는 오브젝트, 회전, 크기, 높이 오프셋을 같게 해요. 타일로 깔린(마을 블록) 것과 심어진(숲, 덤불, 들판) 엔티티가 있어요. 전차 지도 위에서만 만들어요. 근사치인 부분: 지면 높이와 법선(높이맵에서; 게임은 광선을 쏴요), 게임이 실행 중에 등록하는 제외 상자, 나무의 요(게임은 임포스터 회전 팔레트에 맞춰요) |
| 렌더 메시(`content/*/res/*.grp`의 `RendInst` 리소스, `riDesc.bin`의 재질) | 모든 LOD의 정점과 삼각형(실수 위치, 16 또는 32비트 인덱스, 일반 또는 meshoptimizer 압축), 요소마다 재질. 데칼과 임포스터 빌보드 요소는 뺐어요. 투명한 것(유리)은 남겼어요 |
| 오브젝트 색 | 재질마다, 설치본의 질감 팩에 있는 확산 질감의 작은 밉맵 평균(잎은 알파 가중). 대부분의 셰이더는 t0에서, t0이 오버레이나 마스크인 경우 첫 번째 세부 확산에서 가져와요. 재질당 색 하나: 오브젝트에 질감은 없어요 |
| 충돌 형상(`<object>_collision`) | 스트림 버전 3의 충돌 리소스. 오브젝트에 렌더 메시가 없을 때 써요. 게임의 광선이 맞히는 것(`TRACEABLE` 노드)만 그리고, 상자, 구, 캡슐은 리소스에 메시가 없을 때만 그려요. 나머지는 물리적인 거친 대역이라서 오브젝트 주변에 큐브처럼 보일 거예요 |
| 내비게이션 메시(`Lnav`), 렌더링되는 지면 메시, 풀, `spgz`, `stbl`, `d2co` | 읽지 않아요 |

레벨은 Oodle로 압축되어 있어요. Oodle은 독점 소프트웨어예요. 게임은 복사본을 가지고 있어요. `<War Thunder>\win-arm64ec\oo2core_9_win64.dll`(일반 x64 빌드)이고, 그것을 불러와 써요. `HEAT3D_OODLE=<dll 또는 폴더>`로 다른 것을 가리킬 수 있어요. Oodle은 이 저장소에 들어 있지 않아요.

## 형식과 문서가 있는 곳 {#formats-and-where-they-are-documented}

Gaijin은 Dagor Engine의 소스를 BSD 3-Clause 라이선스로 공개했어요(github.com/GaijinEntertainment/DagorEngine). 여기의 리더는 그것을 보고 쓰였어요. 게임 코드는 디컴파일하지 않았어요. 각 모듈은 따라간 소스 파일을 적어 두었어요:

- `vromfs.py`: `*.vromfs.bin`(헤더 `VRFs`/`VRFx`, 첫 16바이트와 마지막 16바이트가 고정된 키와 XOR되는 zstd 본문, 이름 표, 오프셋 표: `osApiWrappers/dag_vromfs.h`, `ioSys/vromfsLoad.cpp`, `supp/dag_zstdObfuscate.h`)와 바이너리 BLK(형식 1-5, 보관소의 공유 이름 맵 `\xff?nm`과 zstd 사전 포함: `ioSys/dataBlock/blk_serialize.cpp`, `blk_parser.cpp`, `blk_zstd.cpp`).
- `dxp.py`: 질감 팩 `DxP2`(`lib3d/texPackMgr2.cpp`)와 DDSx 헤더(`sharedInclude/3d/ddsxTex.h`). DXT1/DXT5/BC7은 Pillow가 디코딩해요.
- `dagorlevel.py`: 레벨 바이너리(`scene/loadLevel.cpp`), 높이맵(`heightmap/heightmapPhysHandler.cpp`, `heightMapLand/compressedHeightmap.cpp`), 지면 광선 추적기(`landMesh/lmeshManager.cpp`, `landMesh/landRayTracerSoA4.cpp`), 물 높이맵(`fftWater/fftWater.cpp`).
- `rigen.py`: 배치된 오브젝트(`rendInst/riGen/riGenData.h`, `rendInst/rendInstGen.cpp`, `rendInst/riGen/genObjUtil.h`).
- `landgen.py`: 만들어진 오브젝트(`rendInst/rendInstGenLand.cpp`, `riGen/landClassData.h`, `riGen/genObjByMask.h`, `riGen/genObjByDensGridMask.h`, `riGen/genObjUtil.h`, `riGen/riGenData.h`, `riGen/multiPointData.h`, `riGen/riRotationPalette.h`, `rendInstGen.cpp`(`create`, `precomputeCell`, `generateCell`), `gameMath/objgenPrng.h`, `util/dag_roHugeHierBitMap2d.h`, `util/dag_hierBitMap2d.h`, `ioSys/dag_roDataBlock.h`, `ioSys/roDataBlk.cpp`, `gameRes/grpData.h`).
- `rendinst.py`: 렌더 인스턴스(`shaders/rendInstRes.cpp`, `shaders/dag_rendInstRes.h`, `shaders/matVdataLoad.cpp`, `shaders/shaderMesh.cpp`, `shaders/dag_shaderMesh.h`, `shaders/dag_shaderCommon.h`, `drv/3d/dag_consts_base.h`, `gameRes/gameResDescBin.cpp`)와 meshoptimizer의 인덱스 코덱(`3rdPartyLibs/meshoptimizer/src/indexcodec.cpp`, MIT).
- `terrain.py`: 지면 색(`landMesh/lmeshManager.cpp`, `lmeshLandClasses.cpp`, `lmeshWeightAtlas*.cpp`, `lmeshRenderer.cpp`, `landMesh/shaders/land_weight_atlas.hlsli`, `land_weight_inc.dshl`, `biomes.dshl`, `daNetGame/shaders/land_aces.dshl`, `make_clipmap.dshl`, `physMap/physMapLoad.cpp`, `baseUtil/treeBitmap.cpp`, `levelSplines/levelSplines.cpp`).
- `collision.py`: 리소스 팩(`gameRes/grpData.h`)과 충돌 리소스(`sharedInclude/gameRes/collResStream.h`, `gameRes/collisionGameResLoad.cpp`). 삼각형은 쿼드 BVH로 저장돼요(`daBVH/bvhIO.cpp`, `daBVH/dag_swBLAS_leaf.h`, `swBLASLeafDefs.hlsli`).

wt_ext_cli(Apache-2.0)도 같은 보관소를 읽어요. 여기서는 필요하지 않아서 쓰지 않았어요.

---

[3DHeat](https://github.com/Holdi601/3DHeat)의 일부([문서](https://holdi601.github.io/3DHeat/)). 소스: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
