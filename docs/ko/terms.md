---
title: 약관과 라이선스
nav_order: 16
lang: "ko"
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# 약관과 라이선스 {#terms-and-licence}

## 약관 {#the-terms}

Gaijin의 서비스 약관(2026-08-17 갱신), EULA(부록 2):
3.2.2 "modify, translate, create derivative works of, reverse engineer, disassemble, or decompile the Game(s)"(게임을 수정, 번역, 파생 저작물 작성, 리버스 엔지니어링, 분해, 디컴파일하는 것); 3.2.9 "mine or collect any data from the Game(s) that is not intended to be publicly displayed"(공개 표시를 의도하지 않은 게임 데이터를 채굴하거나 수집하는 것); 1.2 "are not permitted to store, download, modify, or otherwise use any part of the Game(s)"(클라이언트 이외의 목적으로 게임의 어떤 부분도 저장, 내려받기, 수정 또는 달리 사용하는 것이 허용되지 않음). 여러분 자신의 사본의 레벨 파일을 지역 3D 보기로 읽는 것은, 이것을 알고 내리는 사용자의 결정입니다. 만들어진 레벨은 여러분의 컴퓨터에만 두세요. **절대 공개하지 마세요.** 이 저장소는 게임 데이터를 하나도 담지 않습니다.

## 출처 {#sources}

이 저장소의 모든 코드는 이 프로젝트를 위해 쓰였습니다. 다른 파서에서 가져온 코드는 없습니다. 형식에 대해 아는 내용은 다음에서 왔습니다:

- Gaijin의 Dagor Engine 소스(github.com/GaijinEntertainment/DagorEngine, BSD 3-Clause): 엔티티 스트림을 위한 `prog/engine/daECS/net/network.cpp`, `connection.cpp`, `object.cpp`, `serialize.cpp`, `compression.h`와 `prog/engine/daECS/core/baseIo.cpp`, `componentTypes.cpp`(`ecs.py`), 엔티티 메시지가 클래스 번호를 매기는 방법을 위한 `net/message.cpp`(`MessageClass::initImpl`). 컴포넌트와 타입 이름은 FNV-1a 해시로 게임 자체 보관소의 단어와 맞춰 찾았습니다. `ecs.py`는 찾은 이름을 나열합니다.
- 같은 소스의 `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp`, `daNet/bitStream.h`: 메시지가 자신이 향하는 객체를 이름 붙이는 방법(`wrpl.read_mpi`).
- ShioUmiusi/WTACRP(MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`, `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md`, 그리고 자기 파서 `web/wrpl-parse.js`. 비행 모델, 지상 동기화, 비행 중인 무기, id 필드 메시지, 플레이어 슬롯, 조종석 값, 바이너리 blk의 비트 배치를 읽었습니다. WTACRP는 maxsupermanhd/wrpl-inspector, wt_blk, wrpl-acmi(AGPL-3.0)를 자기 참고 자료로 꼽는데, 그 코드는 여기서 읽지 않았습니다.
- 저자 자신의 리플레이를 파일로 읽은 것: 2025년 차이(비행 모델의 옛 레이아웃, 플래그 바이트가 없는 채팅, zlib), 지상 자세, 압축된 높이의 오프셋, 무기의 발사 지점, 조종석 계기는 여기서 이 리플레이들로 알아냈습니다.

## 테스트 {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<샘플 리플레이 폴더> python -m pytest -q   # 공개된 2025년 샘플 리플레이도 확인
HEAT3D_WT_REPLAYS=<내 리플레이 폴더> python -m pytest -q        # 단계, 식별, AI 표시, 롤 부호, 평활화, 이름
```

단위 테스트는 설치본을 전혀 읽지 않습니다(`HEAT3D_WT_NO_NAMES`가 설정됩니다). 여러분의 리플레이로 하는 테스트는 설치본에서 이름을 읽습니다.

테스트는 `tests/synth.py`에서 리플레이를 코드로 만듭니다. 헤더, 패킷, 결과, 엔티티 스트림, 비행 중인 무기를 리더가 설명하는 레이아웃대로 만듭니다. 저장소에는 리플레이가 하나도 없습니다.

## 라이선스 {#licence}

MIT - [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE)를 보세요. pyarrow(Apache-2.0), numpy(BSD-3-Clause), zstandard(BSD-3-Clause), Pillow(MIT-CMU)를 씁니다. 레벨 리더는 Dagor Engine의 소스에서 쓰였고, 저작권은 Copyright (c) 2023 Gaijin Entertainment, BSD 3-Clause 라이선스입니다. 그 소스의 코드는 여기에 복사하지 않았습니다. 쓰인 형식 상수(vromfs XOR 키, 높이 범위 격자 오프셋)는 나오는 곳에 출처를 적었습니다.

---

[3DHeat](https://github.com/Holdi601/3DHeat)의 일부([문서](https://holdi601.github.io/3DHeat/)). 소스: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
