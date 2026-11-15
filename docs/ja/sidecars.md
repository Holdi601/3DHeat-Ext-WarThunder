---
title: サイドカーと完全性
nav_order: 8
lang: "ja"
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# サイドカーと完全性 {#sidecars-and-completeness}

リプレイの中身は何も捨てられません。変換ツールが読んだものはテーブルとマッチドキュメントに入ります。
それ以外のものは、テーブルのそばにある 3 つのサイドカーファイルに丸ごと残されます（`.3dheat` ファイルの中、
または `--loose` のときは別々に）。これは、すべての 3DHeat 変換ツールに共通のルールです:
[変換ツールはすべてを残す](https://holdi601.github.io/3DHeat/converters.html)。

## サイドカー {#the-sidecars}

- `<match>.messages.parquet`: ユニットへのすべてのメッセージ（時刻、メッセージの ID と名前、uid、eid、テンプレート、車両、その ID の欄を 16 進数で、`decoded`（そこから読み取った内容、JSON 形式）、ペイロード）、すべての複製されたコンポーネントの値（`name` はコンポーネント、`fields` はその値）、すべてのエンティティのメッセージ（エンティティとクラス番号つき）、すべての複製されたオブジェクト（`ReflectionData <kind>/<index>`、その欄を 16 進数で）、そしてここで読まれないすべてのパケット（丸ごと）。
- `<match>.objectives.parquet`: 時間ごとの占領地点。サーバーが送った変化 1 つにつき 1 行: `time`、`event`（`state`、`progress`、`captured`、`neutralised`）、`zone`（その文字）、`zoneId`、`object`、`owner`（0 なし、1、2）、`progress`（−100〜100、チーム 2 へ向かう方向が正）、ゾーンの `x`、`y`、`z`、そしてそのオブジェクトのすべての `fields` を 16 進数で（[目的](objectives.md) を参照）。
- `<match>.flight.parquet`: すべての飛行機のすべての飛行モデルのエントリを丸ごと（そのビット、および `phase`: 最初のバイトのどのビットから始まったか）。速度、14 個の操縦のニブル（`control1-3`、`throttle`）、そのエンジンと状態、アフターバーナーと状態、武器ごとの残りの弾数（`ammo`。`numbers` は一覧全体）を含みます。ほかの飛行機の値は、最後に更新されたときのものです。

## 数が保証すること {#what-the-counts-guarantee}

マッチドキュメントの `counts` は、リプレイが何を持っていて、それがどうなったかを示します:

| キー | 内容 |
|---|---|
| `packets`、`unreadPackets` | 出会ったすべてのパケットの種類と、どの読み取りも取らないもの（メッセージのサイドカーに丸ごと残る） |
| `messageIds`、`messageIdsNotRead` | 出会ったすべてのメッセージ ID とその回数、および残すだけで読まないもの |
| `replicatedComponents`、`replicatedNotRead` | 読んだコンポーネントの値、および残すだけのもの |
| `entities`、`entityTemplates`、`entityMessages` | エンティティのストリームが作ったものと送ったもの |
| `droppedSamples` | 意図的に除いたサンプル（エンティティがなくなった後の地上ユニットの残骸）。理由別 |

ほかに抜けるものはありません。リプレイのどの項目も、テーブルかマッチドキュメントに読み込まれるか、
サイドカーに丸ごと残されるかのどちらかです。マッチドキュメントの `selfCheck` には、読んだ内容の確認が入っています
（[リプレイの読み取り方](how-it-reads.md) を参照）。

---

[3DHeat](https://github.com/Holdi601/3DHeat)（[ドキュメント](https://holdi601.github.io/3DHeat/)）の一部です。ソース: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder)。
