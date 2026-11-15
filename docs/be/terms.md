---
title: "Умовы і ліцэнзія"
nav_order: 16
lang: "be"
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# Умовы і ліцэнзія {#terms-and-licence}

## Умовы {#the-terms}

Умовы выкарыстання Gaijin (абноўлены 2026-08-17), EULA (Дадатак 2):
3.2.2 "modify, translate, create derivative works of, reverse engineer,
disassemble, or decompile the Game(s)", 3.2.9 "mine or collect any data from
the Game(s) that is not intended to be publicly displayed"; 1.2 "are not
permitted to store, download, modify, or otherwise use any part of the Game(s)"
за межамі кліента. Чытанне файлаў узроўняў вашай уласнай копіі ў лакальны
3D-від - рашэнне карыстальніка, прынятае з ведамі пра гэта. Запісаныя
ўзроўні застаюцца на вашай машыне: **ніколі іх не публікуйце**, і нічога
тут не пастаўляе дадзеных гульні.

## Крыніцы {#sources}

Увесь код тут напісаны для гэтага праекта; ніякі код не капіраваўся з іншага
парсера. Тое, што ён ведае пра фармат, паходзіць з:

- Крыніцы Dagor Engine ад Gaijin (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` і `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` для струменя сутнасцей (`ecs.py`) і `net/message.cpp`
  (`MessageClass::initImpl`) для таго, як паведамленні сутнасцей нумаруюць свае
  класы. Назвы кампанентаў і тыпаў супастаўляюцца па іх хэшах FNV-1a са словамі
  уласных архіваў гульні; `ecs.py` пералічвае знойдзеныя назвы.
- Той жа крыніцы `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp`
  і `daNet/bitStream.h`: як паведамленне называе аб'ект, для якога яно
  (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md` і ўласны парсер
  `web/wrpl-parse.js`, чытаныя дзеля бітавых раскладак лётнай мадэлі,
  сінхранізацыі зямлі, зброі ў палёце, паведамленняў з палямі id, слотаў
  гульцоў, значэнняў кабіны і бінарнага blk. WTACRP называе maxsupermanhd/wrpl-inspector,
  wt_blk і wrpl-acmi (AGPL-3.0) сваімі крыніцамі; іх код тут не чытаўся.
- Уласныя запісы аўтара, чытаныя як файлы: адрозненні 2025 (старэйшая
  раскладка лётнай мадэлі, чат без байта-сцяга, zlib), арыентацыя зямлі,
  зрушэнне запакаванай вышыні, пункты выпуску зброі і прыборы кабіны былі
  высветлены на іх тут.

## Тэсты {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # also checks the public 2025 sample replays
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # steps, identities, AI flags, roll sign, the smoother, names
```

Модульныя тэсты ніколі не чытаюць усталёўку (`HEAT3D_WT_NO_NAMES`
усталёўваецца); тэст з вашымі ўласнымі запісамі чытае назвы з вашай
усталёўкі.

Тэсты будуюць запісы ў кодзе (`tests/synth.py`: загаловак, пакеты, вынікі,
струмень сутнасцей, зброя ў палёце) па раскладцы, якую дакументуюць чытачы;
ніводнага запісу ў рэпазіторыі няма.

## Ліцэнзія {#licence}

MIT - гл. [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Выкарыстоўвае pyarrow (Apache-2.0), numpy (BSD-3-Clause),
zstandard (BSD-3-Clause) і Pillow (MIT-CMU). Чытачы ўзроўняў напісаны
паводле крыніцы Dagor Engine, Copyright (c) 2023 Gaijin Entertainment, ліцэнзія BSD
3-Clause; ніводнага яе кода тут не капіравана, а выкарыстаныя канстанты фармату
(XOR-ключ vromfs, зрушэнні сеткі дыяпазонаў вышыні) цытуюцца там, дзе яны з'яўляюцца.

---

Частка [3DHeat](https://github.com/Holdi601/3DHeat) ([дакументацыя](https://holdi601.github.io/3DHeat/)). Крыніца: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
