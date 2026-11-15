---
title: 리플레이 변환하기
nav_order: 4
lang: "ko"
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# 리플레이 변환하기 {#converting-replays}

결과물: 전투 하나당 `.3dheat` 파일 하나(기본값). `--loose`를 쓰면 낱개 파일들이 나옵니다.

## 단계별 안내 {#step-by-step}

1. **리플레이 저장을 켜세요.** 게임 옵션에서 리플레이 저장을 켜면 워 썬더는 게임 폴더의 `Replays` 폴더에 클라이언트 리플레이를 저장합니다. 예: `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`. 게임의 리플레이 페이지에서 저장한 서버 리플레이(`0000.wrpl`, `0001.wrpl`, ...이 든 zip)도 변환할 수 있습니다.
2. **터미널을 여세요.** 결과물을 써도 되는 폴더에서 여세요([시작하기 전에](before-you-start.md)).
3. **변환하세요:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # 파일, 폴더, 또는 둘 다
   heat3d-wt-replay battle.zip -o out              # 서버 리플레이의 zip
   heat3d-wt-replay a.wrpl -o out --loose          # .3dheat 하나 대신 낱개 파일
   ```

   `out`은 터미널이 있는 폴더 안에 만들어집니다.
4. **출력된 내용을 읽으세요.** 전투마다 한 줄씩 보여야 합니다.
5. **여세요:** 3DHeat 뷰어에서 `out/<map>/<match>.3dheat`를 불러오세요([파일 불러오기](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![합성 리플레이 실행: .3dheat 하나, --loose, 깨진 파일, 빈 폴더](../assets/img/convert.svg)

그림은 테스트가 코드로 만든 합성 리플레이에 대한 실행 결과입니다(실제 리플레이도 설치본도 쓰지 않았습니다).

- `ok <파일>`: 전투 하나가 변환되었습니다(`--loose`일 때: `ok <테이블> <매치 문서>`);
- `failed <파일>: <이유>`: 읽을 수 없었던 파일입니다(종료 상태 1; 나머지는 계속 변환됩니다);
- `no .wrpl files given`: 변환할 것이 없습니다(종료 상태 2);
- `note: ...`: 예를 들어 차량 이름을 붙일 워 썬더 설치본을 찾지 못했다는 뜻입니다.

## 옵션 {#options}

| 옵션 | 기본값 | 역할 |
|---|---|---|
| `replays`(하나 이상) | - | `.wrpl` 파일, 그런 파일이 든 폴더(폴더 자체만, 하위 폴더는 제외), 또는 그런 파일의 zip(서버 리플레이: `.wrpl` 조각을 임시 폴더에 풉니다) |
| `-o`, `--out` | 필수 | 쓸 위치: 그 안에 맵마다 폴더가 만들어집니다 |
| `--game FOLDER` | 자동 찾기 | 차량, 무기, 탄약의 이름이 적힌 텍스트를 가진 워 썬더 폴더이자, [경제](economy.md) 가격표를 가진 폴더; `HEAT3D_WT_GAME`도 같은 역할 |
| `--no-smoothing` | 꺼짐 | 다른 유닛의 추측 항법 샘플과 받은 샘플을 리플레이에 있는 그대로 유지([추측 항법과 평활화](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | 켜짐 | 전투마다 `.3dheat` 파일 하나로 묶습니다 |
| `--loose` | 꺼짐 | 전투마다 따로 파일(테이블, 매치 문서, 사이드카)로 남깁니다 |
| `--version` | - | `heat3d-wt-replay <버전>`을 출력하고 멈춥니다 |
| `-h`, `--help` | - | 옵션을 출력하고 멈춥니다 |

같은 전투를 다시 변환하면 다시 씁니다. 프로그램이 출력하는 옵션: [명령 참조](../cli-reference.md).

## 어떤 파일이 전투 하나인가요 {#which-files-are-one-battle}

전투 하나가 파일 하나가 됩니다. `out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat`. AB, RB, SB는 게임이 쓰는 아케이드, 리얼리스틱, 시뮬레이터 전투의 짧은 이름입니다. `<mode>`는 게임이 임무에 붙인 모드 키입니다(`Conq4` 점령 #4, `Dom` 지배, `Bttl` 전투; [전투 모드](ground.md#battle-mode) 참고). 리플레이가 이름을 적지 않은 부분은 뺍니다. 서버 리플레이의 조각(`0000.wrpl`, `0001.wrpl`, ...)은 하나의 전투로 함께 읽습니다. 클라이언트 리플레이와 같은 전투의 서버 조각은 서로 다른 두 기록이라서 두 파일로 남습니다.

## 종료 상태 {#exit-status}

모든 전투가 변환되면 `0`, 하나라도 실패하면 `1`(나머지는 계속 변환됩니다), 인자에서 리플레이 파일을 하나도 찾지 못하면 `2`입니다.

---

[3DHeat](https://github.com/Holdi601/3DHeat)의 일부([문서](https://holdi601.github.io/3DHeat/)). 소스: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
