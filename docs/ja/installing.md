---
title: インストール
nav_order: 3
lang: "ja"
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# インストール {#installing}

コマンドラインは初めてですか？ 先に [始める前に](before-you-start.md) を読んでください。
Python 3.10 以降が必要です。pyarrow、numpy、zstandard、Pillow はこれと一緒に入ります。

## 手順 {#step-by-step}

1. コードを入手します: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`。
   または [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases) から zip をダウンロードして展開します。
2. そのフォルダーでターミナルを開き、`pip install -e .` と入力します。これで 2 つのコマンドが入ります:
   `heat3d-wt-replay`（リプレイ）と `heat3d-wt-level`（レベル）。
3. 確かめます: `heat3d-wt-replay --version`。`heat3d-wt-replay 0.2.0` と表示されるはずです。
   `heat3d-wt-replay --help` でオプションの一覧が出ます:

![heat3d-wt-replay --help](../assets/img/help.svg)

インストールせずに使うには、ツールのフォルダーで `python -m heat3d_ext_warthunder ...` と
`python -m heat3d_ext_warthunder.levelcli ...` を実行します。

## インストール先からの名前 {#names-from-your-install}

車両、武器、弾薬の英語の名前は、変換のときにゲームの文字データから読み取られます。
そのファイルは、Steam またはランチャーの標準のフォルダーからインストール先を探して読みます。
別の場所を指定するには `--game <フォルダー>`、または環境変数 `HEAT3D_WT_GAME` を使います。
ゲームの文字データはこのリポジトリには含まれていません。インストールがなければ、名前の代わりに
車両の ID が使われます（変換ツールは `note:` の行でそれを知らせます）。

## 更新 {#updates}

起動するたびに、まずプロジェクトの GitHub リリースを確認します（数時間に 1 回までの問い合わせです。
変換を止めることはなく、オンラインでもオフラインでも動きます）。新しいリリースがあると、
コマンドはインストールする前に確認を求めます。`git clone` で入れたものは `git pull --ff-only` で
更新されます（手元に変更があるときは拒否されます）。ダウンロードしたものは、リリースのアーカイブから更新されます。
`HEAT3D_NO_UPDATE=1` を設定すると、確認と更新の両方を止められます。

---

[3DHeat](https://github.com/Holdi601/3DHeat)（[ドキュメント](https://holdi601.github.io/3DHeat/)）の一部です。ソース: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder)。
