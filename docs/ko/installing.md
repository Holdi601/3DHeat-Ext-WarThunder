---
title: 설치
nav_order: 3
lang: ko
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# 설치 {#installing}

명령줄이 처음이라면 먼저 [시작하기 전에](before-you-start.md)를 읽어 주세요. Python 3.10 이상이 필요해요. pyarrow, numpy, zstandard, Pillow는 함께 설치돼요.

## 단계별 설치 {#step-by-step}

1. 코드를 받아요: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`. 또는 [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)에서 zip을 받아 압축을 풀어요.
2. 그 폴더에서 터미널을 열고 `pip install -e .`을 입력해요. 명령 두 개가 설치돼요: `heat3d-wt-replay`(리플레이)와 `heat3d-wt-level`(레벨).
3. 확인해요: `heat3d-wt-replay --version`. `heat3d-wt-replay 0.2.0`이 보이면 돼요. `heat3d-wt-replay --help`는 옵션 목록을 보여 줘요:

![heat3d-wt-replay --help](../assets/img/help.svg)

설치하지 않고 쓰려면 도구 폴더에서 `python -m heat3d_ext_warthunder ...`와 `python -m heat3d_ext_warthunder.levelcli ...`를 실행해요.

## 설치본의 이름 {#names-from-your-install}

차량, 무기, 탄약의 영어 이름은 변환할 때 여러분의 설치본에 든 게임 자체 텍스트 파일에서 읽어 와요. 설치본은 Steam이나 런처의 기본 폴더에서 찾아요. 다른 곳에 있다면 `--game <폴더>`나 환경 변수 `HEAT3D_WT_GAME`으로 알려 주세요. 이 저장소에는 게임의 텍스트가 하나도 없어요. 설치본이 없으면 이름 대신 차량 ID가 나와요. 변환기가 `note:` 줄로 그렇게 알려 줘요.

## 업데이트 {#updates}

실행할 때마다 먼저 이 프로젝트의 GitHub 릴리스를 확인해요(최대 몇 시간에 한 번씩 요청해요). 인터넷이 없어도 변환은 멈추지 않아요. 새 릴리스가 나오면 명령이 설치 전에 먼저 물어봐요. `git clone`으로 받은 것은 `git pull --ff-only`로 업데이트하고(로컬 변경이 있으면 거부해요), 내려받은 복사본은 릴리스의 압축 파일로 업데이트해요. `HEAT3D_NO_UPDATE=1`로 확인과 업데이트를 모두 끌 수 있어요.

---

[3DHeat](https://github.com/Holdi601/3DHeat)의 일부([문서](https://holdi601.github.io/3DHeat/)). 소스: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
