---
title: "Умовы і ліцэнзія"
nav_order: 16
lang: "be"
source: terms.md
source_hash: "01d249aa8f1b"
nav_exclude: true
search_exclude: true
---
# Умовы і ліцэнзія {#terms-and-licence}

## Што чытаецца {#what-it-reads}

Канвертар чытае запісы, якія War Thunder захоўвае на вашым камп'ютары (або запісы вашых баёў, якія вы самі спампавалі з warthunder.com), і файлы ўзроўняў вашай уласнай усталёўкі War Thunder. Нічога з гульні тут не ўключана і не распаўсюджваецца: ні рэсурсаў гульні, ні кода гульні, ні DLL; Oodle загружаецца з вашай уласнай усталёўкі. Тое, што ён запісвае, застаецца на вашым камп'ютары: **ніколі не публікуйце ўзроўні**.

3DHeat не звязаны з кампаніяй Gaijin Entertainment і не адобраны ёю. War Thunder і звязаныя назвы і гандлёвыя маркі належаць іх уладальнікам.

Праваўладальнікам: адкрыйце issue на <https://github.com/Holdi601/3DHeat-Ext-WarThunder/issues> - мы хутка адказваем і выдаляем што заўгодна па запыце.

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
