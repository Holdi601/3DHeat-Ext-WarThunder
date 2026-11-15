---
title: 매치 문서
nav_order: 7
lang: ko
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# 매치 문서 {#the-match-document}

![합성 매치 문서의 시작 부분과 그 키들](../assets/img/match-document.svg)

`<match>.match.json`에는 리플레이가 테이블의 행이 아닌 것으로 말하는 모든 것이 들어 있어요. 뷰어의 매치 탭이 이 파일을 읽어요.

## 전투 {#the-battle}

| 키 | 내용 |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | 매치 ID(파일 이름과 같음); 맵의 ID; 쓰는 레벨 파일 |
| `mission`, `missionKey` | 임무의 이름과 게임 텍스트 파일에서의 키 |
| `battleClass`, `environment`, `weather` | 헤더가 주는 그대로 |
| `sessionId`, `server` | 전투의 세션 ID; 서버 |
| `replayVersion`, `flightLayout` | 리플레이 형식의 버전; 읽은 비행 패킷 레이아웃(`2025` 또는 `2026`) |
| `files` | 읽은 리플레이 파일(하나, 또는 서버 리플레이의 조각들) |
| `started`, `timePlayed`, `replayEnd` | 시작 시각(ISO, UTC); 결과에서 가져온 플레이 시간(초); 리플레이의 마지막 패킷의 시간(초) |
| `author`, `authorUserId` | 녹화한 플레이어와 그 Gaijin ID(클라이언트 리플레이) |
| `teams` | 전투의 팀(`1`, `2`) |
| `result` | `winner`, `status`(`success` 또는 `fail`, 녹화자의 결과), `authorTeam`, `teams`([경제](economy.md)) |
| `vehicleNames` | 차량 이름이 어디서 왔는지(여러분의 설치본)와 그 언어 |
| `conventions` | 테이블의 단위와 부호: 축, 시간, 수명, 궤적, alive, roll 등 |

## 나머지 전부 {#everything-else}

| 키 | 내용 |
|---|---|
| `battle`, `difficulty`, `gameMode` | 전투 모드: `difficulty`는 `AB` / `RB` / `SB`(이름과 헤더 바이트 포함), `gameMode`는 `ground` / `air` / `naval`, 임무의 모드(`Dom`, `Conq`, `Bttl`, `I2M`, ...)와 설치본에서 가져온 영어 이름(`Domination`, `Enduring Confrontation`), 허용된 유닛 종류([전투 모드](ground.md#battle-mode) 참고) |
| `settings` | 헤더 뒤의 임무 blk: 모드, 환경, 날씨, 점수와 시간 제한, 국가, 허용된 유닛 종류, 바람, 그리고 `stars`(위도, 경도, 날짜, 현지 시각) |
| `sky` | 첫 `CustomWeatherParams`: 태양과 달의 방향, 바람, 하늘색, 구름 위치 |
| `players`, `slots` | 결과의 플레이어마다 한 줄(처치, 지상 처치, 사망, 어시스트, 점수, 점령, 분대, 클랜, 국가, 편성, 운전한 uid); 리플레이의 플레이어 슬롯(이름, 사용자 ID, 팀) |
| `units` | 리플레이가 만든 모든 유닛 엔티티: eid, uid, 템플릿, 차량, 종류, 유형, 팀, 플레이어, 임무 이름, 만들어지고 지워진 시각, 만들어진 위치, 읽지 못한 컴포넌트 |
| `objects` | 임무의 이름 붙은 객체: 위치와 크기가 있는 점령 구역과 비행장, 비행장의 외곽선(점들), 스폰 구역 |
| `objectives` | 전투의 목표. 각각 `type`(`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team`(리플레이의 1 또는 2; 양쪽이면 빈 값), `name`(점령 구역은 글자, 예: `A`), `shape`(`sphere`, `cylinder`, `box`, `point`, `points`, `outline`)와 `position`, `radius` / `height` / `size`, `heading`, `source`(`replay` 또는 `mission`), 그리고 알려진 나머지 내용([목표](objectives.md) 참고) |
| `kills`, `hits`, `modulesDestroyed` | 양쪽 진영의 이름과 차량을 포함; 무기의 영어 이름이 있는 처치 |
| `weapons` | 발사된 모든 로켓, 미사일, 폭탄, 어뢰, 보조 연료탱크, 버린 짐: 언제, 어디서 발사했는지(위치, 자세, 속도), 어느 유닛이(300 m와 1.5초 안에서 가장 가까운 것), 비행 샘플 수, 마지막으로 본 곳, 언제 지워졌는지 |
| `explosions`, `flak` | `PlayExplosionVisual`(위치, 방향, 종류)과 `PlayFlakExplosionVisual`(위치) |
| `awards` | 녹화한 플레이어의 보상(`TextStreak`: first_blood, 연속 처치, 도전 과제 카운터) |
| `detections`, `unitStates` | `UnitDetected` 유닛 쌍; 유닛의 위치, 자세, 속도를 담은 메시지(0xF093)인데 그 뜻은 알 수 없어요 |
| `authorInstruments` | 녹화한 플레이어의 조종석 값(`ReplayCockpitParams`)을 계기 번호별로, 초당 최대 한 번. `known`은 이 리플레이가 보낸 번호마다 이름(이름, 유닛, 확인 방법)을, `notNamed`는 나머지를 담아요 |
| `scoreboard` | 바뀔 때마다 모든 플레이어의 통계(처치, 사망, 어시스트, 점수, AI 처치, 해전 처치, 구역, 피해, 미사일 회피, 분대), 그리고 시간에 따른 각 팀의 점수와 추정 티켓 수([리플렉션 데이터](aircraft.md#reflection-data) 참고) |
| `economy` | 전투의 실버 라이온과 연구 포인트([경제](economy.md) 참고): 합계, 플레이어별, 차량별, 배수, 승자, 확인 |
| `entityMessages` | 클래스 번호별 엔티티 메시지(0x20): 개수, 대상 템플릿, 크기 |
| `chat` | 모든 채팅 줄 |
| `triggers`, `hints`, `missionProgress` | 임무 스크립트의 동작(RunTriggerAction), 힌트, 진행 메시지 |
| `camera` | 녹화한 플레이어의 리플레이 카메라의 필드를 0.25초마다, 보내온 그대로(테이블에는 궤적으로 있어요) |
| `projectileHitReplays` | 녹화한 플레이어가 명중시킨 것과 맞은 것, 무기와 탄약, 영어 이름 포함 |
| `results` | 게임이 쓴 결과 blk 전체 |
| `counts` | 행, 이벤트, 수명, 종류, 샘플, 템플릿별 엔티티, 무기, 읽은 것과 읽지 않은 패킷, 본 메시지 ID와 읽지 않은 것, 버린 샘플 |
| `trackBreaks` | 유닛이 갈 수 있는 것보다 빠른 단계를 보인 궤적의 모든 끊김: 어디서, 얼마나 멀리, 얼마나 빨랐는지, 가장 가능성 높은 원인 |
| `selfCheck` | [리플레이를 읽는 법](how-it-reads.md)에 있는 확인들. 변환할 때마다 계산돼요. `stepSpeed`는 뷰어가 궤적을 잇는 방식대로, 한 궤적의 연속 행 사이 속도를 종류별로 보여 줘요(중앙값, 99번째 백분위수, 최댓값, 그리고 가능한 것보다 빠른 단계의 수. 이 수는 0이어야 해요) |

---

[3DHeat](https://github.com/Holdi601/3DHeat)의 일부([문서](https://holdi601.github.io/3DHeat/)). 소스: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
