---
title: 테이블
nav_order: 6
lang: ko
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# 테이블 {#the-table}

![합성 리플레이의 테이블, 요약](../assets/img/table.svg)

샘플이나 이벤트 하나당 한 행이고, 열은 105개예요([열 목록](../columns.md), 코드에서 생성됨). 바닥글에는 `heat3d` 아래에 뷰어의 읽는 방법이 적혀 있어서, 뷰어가 따로 설정할 것이 없어요.

| 열 | 내용 |
|---|---|
| `time` | 리플레이 자신의 시계로 잰 초 |
| `event` | `position`. 이벤트 행은 그 순간의 궤적 위에 놓여요(두 샘플 사이에서는 그 사이의 선 위에). `kill`(공격자 위치), `death`(피해자 위치), `hit_critical` / `hit_severe`(맞은 유닛 위치), `module_destroyed`(유닛 위치), `launch`(무기를 발사한 유닛 위치), `impact`(무기가 바로 지워질 때의 마지막 샘플). `explosion`과 `flak`(0xD08E, 0xD01F)은 그 위치에, 종류 `effect`, 궤적은 없어요. 방향이 있으면 폭발의 방향도 붙어요. `shot`(명중한 발사체, 사수 위치), `gun_shot`, `fire_start`, `fire_stop`(포의 연사, 불이 붙은 차량이 아니에요), `fire_on`, `fire_off`(불이 붙은 차량, [차량 화재](hits.md#vehicle-fires) 참고), `reward`(번 실버 라이온과 연구 포인트, [경제](economy.md) 참고), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload`([유닛에 보내는 메시지](how-it-reads.md#messages-to-units) 참고); `despawn`: 리플레이가 끝나기 전에 유닛이 사라진 궤적의 마지막 행([궤적의 끝](ground.md#end-of-a-track) 참고) |
| `track` | 뷰어가 하나로 그리는 것: 유닛 하나의 한 수명, 또는 무기 하나의 비행 - `<플레이어 또는 차량> #<hex>`(뷰어는 `#` 부분을 뺀 이름을 보여 줘요) |
| `x`, `y`, `z` | 게임의 미터 단위: x 동, y 위, z 북(힌트가 z를 뒤집으므로 북쪽이 남쪽으로 그려지지 않아요) |
| `player` | 플레이어의 이름. AI 유닛은 `<VehicleName> #<uid>`(예: `F-15A #204`); 아무도 이름을 대지 않으면 `uid <n>`; 무기는 발사한 사람 |
| `userId`, `team` | 플레이어의 Gaijin ID와 팀(`1`, `2`) |
| `ai`, `isPlayer` | `ai`는 플레이어 계정이 운전하지 않는 모든 유닛에 대해 true(임무 유닛, AI 항공기, 지상 목표, 대공포, 플레이어가 없는 함선, 자리표시자). `isPlayer`는 반대예요. 엔티티가 Gaijin ID를 가진 플레이어 슬롯을 가리키는 유닛이 플레이어예요. 무기는 발사대의 값을 가지고, 알 수 없으면 비어 있어요 |
| `match` | 매치 ID(매치 문서의 `match`), 모든 행에 있어요. 힌트는 이것을 세션으로 보므로, 두 리플레이를 불러와도 궤적이 섞이지 않아요 |
| `life` | `uid#n`: 한 유닛의 궤적. uid가 다른 유닛으로 넘어가는 곳, 유닛이 가능한 것보다 빠르게 움직이는 곳(리스폰, 재장전, 게임이 옮긴 것, 멀리 있는 유닛에 대한 클라이언트 보정; [리플레이를 읽는 법](how-it-reads.md#what-is-read-and-the-check)의 순간이동 참고), 또는 오래 보이지 않는 곳에서 끊어요. `w<hex>`는 무기의 비행(끊긴 뒤에는 `w<hex>#n`) |
| `uid` | 리플레이에서의 유닛 ID |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train`(레벨이 놓은 전차나 철도 차량, [장면 유닛](objectives.md#scene-units-trams-and-rail-wagons) 참고). 무기는 `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`. `camera`는 녹화한 플레이어의 리플레이 카메라([카메라](ground.md#the-camera) 참고) |
| `type` | 결과가 이름을 대는 경우 게임 고유의 유형(`fighter`, `assault`, `destroyer`, `gun_boat`), 아니면 `kind`와 같음 |
| `Vehicle` | 게임의 차량 ID(`f_15a`, `germ_flakpz_I_Gepard`). 뷰어의 그림이 이것과 맞아요 |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | 설치본의 현지화에서 온 차량의 영어 이름(`Pz.Kpfw. III Ausf. J1`, 짧은 이름 `Pz.III J1`)과 그 키(`germ_pzkpfw_III_ausf_J_0`). 게임 글꼴의 국가 표시는 뺐어요. 게임이 이름을 대지 않거나 설치본이 없으면 이름은 ID이고, 키는 비어 있어요 |
| `mission` | 임무에서 그 유닛의 이름(`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | 유닛이 향하는 방향(바라보는 벡터): 항공기는 비행 모델의 자세에서, 지상 유닛과 함선은 자기 자세에서, 무기는 비행 방향을 따라요 |
| `heading`, `pitch`, `roll` | 같은 값을 도 단위로. 방위는 나침반이에요. 북에서 시계 방향. 피치는 기수가 위인 것이 양수. 롤은 오른쪽 날개가 내려간 것이 양수예요(비행 모델은 반대 부호를 보내요. [자세 확인](aircraft.md#attitude-checked) 참고; 지상 유닛은 오른쪽 면이 내려간 것). 힌트가 `conventions`에 이것을 적어요 |
| `turretYaw`, `gunPitch`, `turrets` | 전차의 주포탑. 플레이어가 보는 곳이 아니라 포가 가리키는 곳이에요. 리플레이의 값을 포탑 구동 장치의 속도에 맞추고, 주포의 각 사격선에 맞춘 것([포탑](ground.md#turrets) 참고). 차체 기준 방위각(도, 위에서 봤을 때 시계 방향이 양수, 정면이 0)과 차체 기준 포신 피치(도, 위가 양수). `turrets`는 차량의 모든 포탑을 `yaw pitch;yaw pitch;...`로 자기 순서대로 나열해요(쓰지 않는 슬롯은 `0.00 0.00`). 클라이언트와 서버 리플레이의 전차, 대공 자주포, 장갑차, 트럭에 있고, 함선에는 없어요([포탑](ground.md#turrets) 참고) |
| `turretYawRaw`, `gunPitchRaw` | 리플레이가 보낸 그대로의 주포탑. `turretYaw` / `gunPitch`는 이것을 포탑 구동 장치의 속도에 맞추고, 각 주포 사격선에 맞춘 값이에요([포탑](ground.md#turrets) 참고) |
| `viewYaw`, `viewPitch` | 플레이어가 세계에서 보는 곳(카메라로 조준하는 곳): 나침반 도(0이 북, 시계 방향)와 위쪽 도. `aimHeading` / `aimPitch`와 같은 방식이에요(차체에 상대적인 `turretYaw` / `gunPitch`와 달리요). 서버 리플레이의 모든 플레이어 전차, 클라이언트 리플레이에서는 녹화한 플레이어 자신의 전차. 플레이어가 아무 곳도 조준하지 않으면 비어 있어요(네 개의 조준 실수 값이 모두 0). 포탑은 자기 회전 속도로 이것을 따라가므로, 회전하는 동안에는 둘이 달라요([포탑](ground.md#turrets) 참고) |
| `aimHeading`, `aimPitch`, `aimDistance` | 녹화한 플레이어 자신의 전차: 조준하는 곳(나침반 도, 위쪽 도, 조준 거리 m; 조준선에 아무것도 없으면 2000). 카메라 행: 플레이어가 조준하는 곳(방위, 피치) |
| `zoom` | 카메라 행: 카메라의 배율([카메라](ground.md#the-camera) 참고) |
| `difficulty`, `gameMode` | 전투의 `AB`, `RB`, `SB`, 그리고 `ground`, `air`, `naval`. 모든 행에 있어요([전투 모드](ground.md#battle-mode) 참고) |
| `extrapolated` | 받은 상태가 아니라 클라이언트의 추측 항법인 항공기 샘플([추측 항법](aircraft.md#dead-reckoning-and-the-smoother) 참고). 발사부터 계산한 폭탄의 샘플([비행 기록이 없는 폭탄](how-it-reads.md#what-is-read-and-the-check) 참고) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | 평활화가 샘플을 얼마나 옮겼는지(m), 그리고 리플레이 자신의 위치와 자세(롤은 테이블의 부호) |
| `targetX`, `targetY`, `targetZ` | `shot`의 명중 지점 |
| `hitOutcome`, `hitFlags` | 지상 유닛에 대한 `shot`의 결과: `kill`, `critical`, `penetration`, `nonpenetration`(튕기거나 막힌 것: 리플레이는 튕김과 구별하지 않아요). 서버가 명중과 함께 보내는 비트로(`hitFlags`, 원본), 보내지 않은 곳(항공기, 함선)은 비어 있어요. [명중 결과](hits.md#hit-outcomes) 참고 |
| `hitShell` | `shot`의 탄 시그니처: 명중 메시지의 4바이트(원본 16진수). 한 시그니처가 다른 탄을 나타낼 수 있어서(120 mm와 125 mm APFSDS는 같은 시그니처를 써요), 구경으로 읽지 않고 그대로 보관해요 |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | `shot`의 탄약: 종류(`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...)와 ID(`125mm_3bm46`)는 처치가 사수의 슬롯을 알려 줄 때 쓰고, 아니면 `explosive`(명중 폭발)나 `kinetic`이에요. 포의 `weapon/slot`은 재장전에서 와요. 구경은 설치본의 무기 파일에서 mm 단위로 와요. [명중 결과](hits.md#hit-outcomes) 참고 |
| `rpm` | 항공기의 엔진 rpm(엔진들의 평균), 마지막으로 보내진 값, 2초 이내 |
| `vx`, `vy`, `vz` | 비행 항목이 보내는 항공기의 속도(m/s, 게임의 축; 500 m/s를 넘는 속도는 500으로 읽혀요) |
| `engine`, `afterburner`, `engineCondition` | 비행 항목에서 온 항공기의 엔진: `off`, `starting`, `running`, `dead`(엔진이 서로 다르면 `/`로 이어요); 애프터버너 0-1; 엔진이 맞은 뒤에만 보내지는 바이트 |
| `weaponName` | 처치와 사망: 여러분의 설치본에 있는 영어 무기나 탄약 이름(`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | 녹화한 플레이어의 항공기에만: 조종석의 스로틀 0-1.1(1.1은 전투 비상 출력이나 애프터버너; 그 밖에는 비행 항목의 15분의 1 단위), 비행 항목에서 온 조종 -1..1(승강타는 당기면 양수, 보조익은 오른쪽으로 구르면 양수), 무기별 남은 발사 수(`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | 녹화한 플레이어의 항공기에만, 조종석에서: 지시 대기속도와 상승률(m/s), 연료, 흡기 압력(atm), 착륙 장치(0-1, 1은 내림), 오일과 실린더 헤드 온도. 조종석에 그 게이지가 있는 경우에 한해요 |
| `speed` | 궤적의 약 2초 동안의 m/s(여기서 계산해요. 리플레이는 다른 유닛의 속도를 보내지 않아요) |
| `alive` | 유닛이 죽은 뒤의 샘플(잔해)에서 0. 지상 유닛이나 함선은 게임이 지우거나 샘플이 끝날 때까지, 항공기는 최대 60초 동안 0이에요 |
| `otherVehicle`, `otherLife` | `shot`의 피해자: 그 차량과 그 `life` |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | `shot`의 명중 지점을 피해자 자신의 좌표로(m; x 앞, y 위, z 왼쪽. [유닛에 보내는 메시지](how-it-reads.md#messages-to-units) 참고)와, 그때 피해자의 자세로 그 좌표에 돌린, 사격이 온 방향 |
| `hitPart`, `hitFlag` | `shot`의 명중 메시지: 보내진 그대로의 부품 워드와 그 상위 바이트 |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | 전투에 든 비용과 번 것, 그리고 누가 이겼는지. [경제](economy.md) 참고 |
| `other`, `weapon` | 처치: 상대 진영과 무기. 명중: 누가 맞혔는지(기록의 uid, 아니면 플레이어 슬롯에서), 그 차량. 발사: 무기. 파괴된 모듈: 5초 안에 그 유닛을 마지막으로 맞힌 사람, 그리고 `part <n>` |

---

[3DHeat](https://github.com/Holdi601/3DHeat)의 일부([문서](https://holdi601.github.io/3DHeat/)). 소스: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
