---
title: 利用条件とライセンス
nav_order: 16
lang: "ja"
source: terms.md
source_hash: "01d249aa8f1b"
nav_exclude: true
search_exclude: true
---
# 利用条件とライセンス {#terms-and-licence}

## 読み取るもの {#what-it-reads}

この変換ツールが読むのは、War Thunder があなたのコンピュータに保存したリプレイ（またはあなた自身が warthunder.com からダウンロードした自分の戦闘のリプレイ）と、あなた自身の War Thunder のインストールにあるレベルファイルです。ゲームのものはここには何も含まれず、再配布もされません。ゲームのアセットも、ゲームのコードも、DLL もありません。Oodle はあなた自身のインストールから読み込まれます。書き出したものはあなたのマシンに残ります。**レベルは決して公開しないでください**。

3DHeat は Gaijin Entertainment とは提携しておらず、Gaijin Entertainment の承認も受けていません。War Thunder および関連する名称と商標は、それぞれの所有者に帰属します。

権利者の方へ: <https://github.com/Holdi601/3DHeat-Ext-WarThunder/issues> で Issue を開いてください。迅速に対応し、ご要望があれば何でも削除します。

## 出典 {#sources}

ここにあるコードはすべて、このプロジェクトのために書かれたものです。他のパーサーからコードはコピーしていません。
フォーマットについて知っていることは、次の出典から得ています:

- Gaijin の Dagor Engine のソース（github.com/GaijinEntertainment/DagorEngine、BSD 3-Clause）: `prog/engine/daECS/net/network.cpp`、`connection.cpp`、`object.cpp`、`serialize.cpp`、`compression.h`、`prog/engine/daECS/core/baseIo.cpp`、エンティティのストリームのための `componentTypes.cpp`（`ecs.py`）、そしてエンティティのメッセージがそのクラスに番号を振る方法のための `net/message.cpp`（`MessageClass::initImpl`）。コンポーネントと型の名前は、ゲームの文書の単語との FNV-1a ハッシュで照合されました。`ecs.py` は見つかった名前を挙げています。
- 同じソースの `prog/dagorInclude/daNet/mpi.h`、`prog/engine/daNet/ext/mpi.cpp`、`daNet/bitStream.h`: メッセージが、それが宛てられたオブジェクトをどう名指しするか（`wrpl.read_mpi`）。
- ShioUmiusi/WTACRP（MIT）: `docs/REPLAY-FORMAT.md`、`docs/REPLAY-DECODE.md`、`docs/REPLAY-DECODE-ECS.md`、`docs/QUICK-REF.md`、そして自身のパーサー `web/wrpl-parse.js`。飛行モデル、地上の同期、飛行中の武器、ID 欄のメッセージ、プレイヤースロット、コックピットの値、バイナリの blk のビットの配置を読むために参照しました。WTACRP は、自身の参考として maxsupermanhd/wrpl-inspector、wt_blk、wrpl-acmi（AGPL-3.0）を挙げていますが、そのコードはここでは読んでいません。
- 著者自身のリプレイを、ファイルとして読んだもの: 2025 年の違い（飛行モデルの古い形式、フラグのバイトのないチャット、zlib）、地上の姿勢、詰められた高さのずれ、武器の放出地点、コックピットの計器は、ここで自分たちのリプレイを使って明らかにしました。

## テスト {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # 公開されている 2025 年のサンプルのリプレイも確認
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # 手順、同一性、AI の旗、ロールの符号、平滑化、名前
```

ユニットテストはインストールを一切読みません（`HEAT3D_WT_NO_NAMES` が設定されます）。自分自身のリプレイを使うテストは、インストールから名前を読みます。

テストは、`tests/synth.py`（ヘッダー、パケット、結果、エンティティのストリーム、飛行中の武器）で、読み取りのページに記載された形式に合わせてコードの中でリプレイを作ります。リポジトリにはリプレイは入っていません。

## ライセンス {#licence}

MIT。[`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE) を参照してください。pyarrow（Apache-2.0）、numpy（BSD-3-Clause）、zstandard（BSD-3-Clause）、Pillow（MIT-CMU）を使用しています。レベルの読み取りは、Dagor Engine のソースから書かれました。著作権は (c) 2023 Gaijin Entertainment、BSD 3-Clause ライセンスです。そのコードはここにはコピーされていません。使われているフォーマットの定数（vromfs の XOR キー、高さの範囲のグリッドのオフセット）は、それが現れる箇所で引用されています。

---

[3DHeat](https://github.com/Holdi601/3DHeat)（[ドキュメント](https://holdi601.github.io/3DHeat/)）の一部です。ソース: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder)。
