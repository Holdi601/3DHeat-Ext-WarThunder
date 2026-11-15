---
title: リプレイの変換
nav_order: 4
lang: ja
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# リプレイの変換 {#converting-replays}

出力は、戦闘ごとに 1 つの `.3dheat` ファイル（既定）か、`--loose` を付けた場合はばらばらのファイルです。

## 手順 {#step-by-step}

1. **リプレイを有効にする。** War Thunder は、ゲームのオプションでリプレイの保存をオンにしていると、
   ゲームの `Replays` フォルダーにクライアントのリプレイを保存します。たとえば
   `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays` です。
   ゲームのリプレイページから保存したサーバーのリプレイ（`0000.wrpl`、`0001.wrpl`、... を含む zip）も変換できます。
2. **ターミナルを開く。** 結果を置いてもよいフォルダーで開いてください（[始める前に](before-you-start.md)）。
3. **変換する:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # ファイル、フォルダー、またはその両方
   heat3d-wt-replay battle.zip -o out              # サーバーのリプレイの zip
   heat3d-wt-replay a.wrpl -o out --loose          # 1 つの .3dheat ではなく、別々のファイル
   ```

   `out` はターミナルのいるフォルダーに作られます。
4. **表示された内容を読む。** 戦闘ごとに 1 行が表示されるはずです。
5. **開く:** `out/<map>/<match>.3dheat` を 3DHeat ビューアで読み込みます
   （[ファイルを開く](https://holdi601.github.io/3DHeat/container.html#loading-one)）。

![合成リプレイでの実行: .3dheat が 1 つ、--loose、壊れたファイル、空のフォルダー](../assets/img/convert.svg)

この図は、テストがコードの中で作ったリプレイ（実際のリプレイもゲームのインストールも使わない）で実行した結果です:

- `ok <file>`: 戦闘を変換できた（`--loose` のときは `ok <table> <match document>`）。
- `failed <file>: <why>`: ファイルを読めなかった（終了ステータス 1。ほかのファイルは引き続き変換されます）。
- `no .wrpl files given`: 変換するものがない（終了ステータス 2）。
- `note: ...`: たとえば、車両の名前のために War Thunder のインストールが見つからなかった、など。

## オプション {#options}

| オプション | 既定 | 働き |
|---|---|---|
| `replays`（1 つ以上） | - | `.wrpl` ファイル、その入ったフォルダー（サブフォルダーは含まず、そのフォルダー自身のみ）、またはそれらの zip（サーバーのリプレイ: `.wrpl` の部分が一時フォルダーに展開されます） |
| `-o`、`--out` | 必須 | 書き込み先。中にマップごとのフォルダーが作られます |
| `--game FOLDER` | 自動検出 | 車両、武器、弾薬の名前を読む War Thunder のフォルダー。その価格表で[経済](economy.md)も計算されます。`HEAT3D_WT_GAME` でも指定できます |
| `--no-smoothing` | オフ | ほかのユニットの推測航法によるサンプルと受信したサンプルを、リプレイにあるままに残す（[推測航法](aircraft.md#dead-reckoning-and-the-smoother)） |
| `--container` | オン | 戦闘ごとに 1 つの `.3dheat` ファイルにまとめる |
| `--loose` | オフ | 戦闘ごとに、別々のファイル（テーブル、マッチドキュメント、サイドカー）として残す |
| `--version` | - | `heat3d-wt-replay <version>` を表示して終了する |
| `-h`、`--help` | - | オプションを表示して終了する |

変換済みの戦闘をもう一度変換すると、書き直されます。プログラムが表示するとおりのオプション:
[コマンドリファレンス](../cli-reference.md)。

## どのファイルが 1 つの戦闘か {#which-files-are-one-battle}

戦闘は 1 つずつ、
`out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat` になります。
AB、RB、SB は、ゲームでそれぞれアーケード、リアリスティック、シミュレーター戦闘を示す短い形です。
`<mode>` は、ゲームがミッションに付けている形式のモードです（`Conq4` は Conquest #4、`Dom` は Domination、
`Bttl` は Battle。[戦闘モード](ground.md#battle-mode) を参照）。どちらの部分も、リプレイに名前がなければ省かれます。
サーバーのリプレイの部分（`0000.wrpl`、`0001.wrpl`、...）は 1 つの戦闘として一緒に読まれます。
クライアントのリプレイと、同じ戦闘のサーバー側の部分は、2 つの記録として別々に残ります。

## 終了ステータス {#exit-status}

すべての戦闘が変換できたら `0`、1 つでも失敗したら `1`（残りは変換されます）、
引数の中にリプレイファイルが 1 つも見つからなければ `2` です。

---

[3DHeat](https://github.com/Holdi601/3DHeat)（[ドキュメント](https://holdi601.github.io/3DHeat/)）の一部です。ソース: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder)。
