---
title: 목표
nav_order: 15
lang: "ko"
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# 목표 {#objectives}

매치 문서의 `objectives`는 전투가 어떤 것을 두고 벌어지는지를 두 출처(`source`)에서 나열합니다.

- **리플레이**(`replay`): 0xD039이 이름 붙인 임무 객체(점령 구역 `cz_circle_NN`, 비행장, 헬기장, 기지). 이것들은 종류 3의 복제 객체(0xF02D)가 지금 놓은 위치에 있습니다. 점령 구역은 시작할 때 템플릿의 자리에서 시작해서, 이 모드의 구역 위치로 옮겨집니다(`moved`). 종류 3의 번호는 0xD039의 순서를 따르고, 옮겨지지 않은 모든 객체는 0xD039가 놓은 곳에 정확히 있습니다. 그래서 순서가 확인됩니다. 점령 구역은 그 자리의 임무 영역의 모양과 반경을 가집니다(`area`, 2 m 이내). 글자는 자기 인덱스에서 옵니다(종류 5 필드 69: 0 = A). 글자 순서는 리플레이의 것이고, 게임의 지도와 대조하지는 않았습니다.
- **임무**(`mission`): 설치본의 `mis.vromfs.bin`에 있는 임무 파일 `<mission>.blk`와 그것이 가져오는 템플릿(변환할 때만, 읽기 전용): 임무의 영역들을 이름으로 분류한 것. 스폰(스폰의 번호 붙은 지점 `..._spawnareaNN`은 하나의 `points` 스폰이 됩니다), 전투 영역, 폭격 목표(`bomb_zone`), 호송 스폰 지점(`road_NN_spawn`), 출구와 처치 영역. 같은 맵의 다른 모드(`conq_`, `dom_`, `bttl_`, ...)의 영역은 뺍니다. `_arcade` / `_realistic` / `_hardcore` 변형은 그 전투 자신의 것을 씁니다(RB는 `_realistic`, 없으면 `_hardcore`를 씁니다. 임무 스크립트가 하는 방식입니다). 브리핑 표식, 대공포 지점, 그리고 5 km보다 넓은 영역(스폰이 흩어져 있는 영역)도 뺍니다. 각 스폰에는 몇 명의 플레이어 궤적이 거기서 시작했는지 있습니다(`used`, `usedByTeam`). 임무는 무작위로 진영을 바꿀 수 있습니다(`randomSpawnTeams`). 스폰이 리플레이의 팀을 반대로 보여 주면, 모든 `team`을 바꾸고 이름의 진영은 `missionTeam`으로 남깁니다. 읽은 임무의 웨이포인트에는 호송 경로가 없습니다. 호송이 나타난 곳만 적습니다.

시간에 따른 점령 구역은 사이드카 `<match>.objectives.parquet`에 있습니다. 종류 5의 복제 객체를 구역마다 하나씩 담습니다. 필드 2는 소유자(0, 1, 2), 필드 67은 점령 진행도로, -100에서 100 사이의 부호 있는 바이트입니다(양수는 2팀 쪽). 필드 69는 인덱스입니다. 확인은 서버 리플레이의 점령과 지배 전투에서 했습니다(`selfCheck.objectives`). 소유자가 바뀔 때마다, 같은 순간(1.5초 안)에 점령한 팀의 플레이어 한 명이 매치 점수판에서 `captureZone`을 얻었고, 그 팀의 살아 있는 지상 유닛 하나가 구역 안에 있었습니다. 모든 전투의 스폰은 리플레이의 팀을 한 방향으로만 보여 줍니다(임무의 `t1_` / `t2_`와 반대인 경우가 많습니다).

## 장면 유닛: 전차와 철도 차량 {#scene-units-trams-and-rail-wagons}

레벨은 자기 유닛을 놓을 수 있습니다. 서버 리플레이의 `unit_loader+rail_wagon` 엔티티는 레벨의 장면 파일에 있는 전차입니다(`gamedata/scenes/<level>_objects.blk`, `aces.vromfs.bin` 안: `setting__unit_class`, 그 변환, `setting__isDead`). 이 엔티티들에는 읽을 수 있는 uid가 없습니다. 그래서 유닛 엔티티가 없는 지상 궤적이 있고, 그 첫 샘플이 장면 유닛에서 2 m 이내에 있으면, 그것이 그 유닛입니다. 그 클래스는 `Vehicle`, 종류 `train`, 유형 `tram`, `locomotive`, `wagon`이고, 팀은 없습니다. 장면이 죽은 상태로 놓은 유닛(불탄 전차 등)은 첫 행부터 잔해(`alive` 0)입니다. 게임에는 이것들의 영어 이름이 없습니다. 그래서 `VehicleName`은 ID를 단어로 읽은 것입니다("Railway tram A"). 이 위치는 흔들리지 않습니다. 거의 모두 전혀 움직이지 않습니다(모든 샘플이 비트 단위로 같습니다). 리플레이는 이것들을 대략 초당 10번 보냅니다. 그래서 샘플 중에서 실제로 움직이는 것(0.05 m 또는 0.1도)만 남기고, 10초마다 하나만 남깁니다(`selfCheck.sceneUnits`가 버린 샘플 수를 셉니다). 이전에는 차량 없이 `uid 8`이라는 이름의 궤적이었습니다.

---

[3DHeat](https://github.com/Holdi601/3DHeat)의 일부([문서](https://holdi601.github.io/3DHeat/)). 소스: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
