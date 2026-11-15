---
title: 사이드카와 완전성
nav_order: 8
lang: "ko"
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# 사이드카와 완전성 {#sidecars-and-completeness}

리플레이에서 버리는 것은 없습니다. 변환기가 읽는 것은 테이블과 매치 문서에 들어갑니다. 그 밖의 모든 것은 테이블 옆에 있는 사이드카 파일 세 개에 통째로 보관됩니다(`.3dheat` 파일 안에, 또는 `--loose`일 때 낱개로). 이것은 모든 3DHeat 변환기가 함께 따르는 규칙입니다: [변환기는 모든 것을 보관합니다](https://holdi601.github.io/3DHeat/converters.html).

## 사이드카 {#the-sidecars}

- `<match>.messages.parquet`: 유닛에 보내진 모든 메시지(시각, 메시지 id와 이름, uid, eid, 템플릿, 차량, id 필드를 16진수로, `decoded`(읽은 내용을 JSON으로), 페이로드), 모든 복제 컴포넌트 값(`name`은 컴포넌트, `fields`는 그 값), 모든 엔티티 메시지(엔티티와 클래스 번호 포함), 모든 복제 객체(`ReflectionData <kind>/<index>`, 필드를 16진수로), 그리고 여기 어떤 읽기도 맡지 않은 패킷 전부를 통째로.
- `<match>.objectives.parquet`: 서버가 보낸 변화마다 한 행으로, 시간에 따른 점령 구역. `time`, `event`(`state`, `progress`, `captured`, `neutralised`), `zone`(글자), `zoneId`, `object`, `owner`(0 없음, 1, 2), `progress`(-100..100, 양수는 2팀 쪽), 구역의 `x`, `y`, `z`, 그리고 객체의 모든 `fields`를 16진수로([목표](objectives.md) 참고).
- `<match>.flight.parquet`: 모든 항공기의 모든 비행 모델 항목을 통째로(그 비트들, 그리고 항목이 시작한 첫 바이트의 비트인 `phase`), 속도, 14개의 조종 니블(`control1-3`, `throttle`), 엔진의 상태, 애프터버너와 상태, 무기별 발사 수(`ammo`; `numbers`는 목록 전체). 다른 항공기의 값은 마지막으로 갱신된 값입니다.

## 개수가 보장하는 것 {#what-the-counts-guarantee}

매치 문서의 `counts`는 리플레이가 무엇을 담고 있었고 그것이 어떻게 되었는지 말해 줍니다:

| 키 | 내용 |
|---|---|
| `packets`, `unreadPackets` | 만난 모든 패킷 종류, 그리고 어떤 리더도 맡지 않는 것들(메시지 사이드카에 통째로 보관) |
| `messageIds`, `messageIdsNotRead` | 만난 모든 메시지 id와 그 횟수, 그리고 보관만 하고 읽지 않은 것 |
| `replicatedComponents`, `replicatedNotRead` | 읽은 컴포넌트 값, 그리고 보관만 한 것 |
| `entities`, `entityTemplates`, `entityMessages` | 엔티티 스트림이 만들고 보낸 것 |
| `droppedSamples` | 일부러 뺀 샘플(엔티티가 사라진 뒤의 지상 유닛 잔해), 이유별 |

그 밖에 뺀 것은 없습니다. 리플레이의 항목 하나는 테이블이나 매치 문서로 읽히거나, 사이드카에 통째로 보관되거나 둘 중 하나입니다. 매치 문서의 `selfCheck`는 읽은 것의 확인을 담습니다([리플레이를 읽는 법](how-it-reads.md)).

---

[3DHeat](https://github.com/Holdi601/3DHeat)의 일부([문서](https://holdi601.github.io/3DHeat/)). 소스: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
