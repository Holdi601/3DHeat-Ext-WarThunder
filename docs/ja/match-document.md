---
title: マッチドキュメント
nav_order: 7
lang: "ja"
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# マッチドキュメント {#the-match-document}

![合成したマッチドキュメントの冒頭と、そのキー](../assets/img/match-document.svg)

`<match>.match.json` には、テーブルの行にはならない、リプレイが伝えるすべてのことが入っています。
ビューアの マッチ タブがこれを読みます。

## 戦闘 {#the-battle}

| キー | 内容 |
|---|---|
| `format`、`version` | `heat3d-wt-replay-match`、`2` |
| `match`、`map`、`level` | マッチ ID（ファイル名と同じ）。マップの ID。使っているレベルファイル |
| `mission`、`missionKey` | ミッションの名前と、ゲームの文字データでのそのキー |
| `battleClass`、`environment`、`weather` | ヘッダーが示すとおり |
| `sessionId`、`server` | 戦闘のセッション ID。サーバー |
| `replayVersion`、`flightLayout` | リプレイ形式のバージョン。読み取った飛行パケットの形式（`2025` または `2026`） |
| `files` | 読み取ったリプレイファイル（1 つ。またはサーバーのリプレイの部分） |
| `started`、`timePlayed`、`replayEnd` | 開始時刻（ISO、UTC）。結果から得た、プレイした秒数。リプレイの最後のパケットの秒数 |
| `author`、`authorUserId` | 録画しているプレイヤーと、その Gaijin ID（クライアントのリプレイ） |
| `teams` | 戦闘のチーム（`1`、`2`） |
| `result` | `winner`、`status`（`success` または `fail`。録画者の結果）、`authorTeam`、`teams`（[経済](economy.md)） |
| `vehicleNames` | 車両の名前の出どころ（インストール）と、その言語 |
| `conventions` | テーブルの単位と符号: 軸、時間、生存、トラック、alive、roll など |

## そのほかすべて {#everything-else}

| キー | 内容 |
|---|---|
| `battle`、`difficulty`、`gameMode` | 戦闘モード。`difficulty` は `AB` / `RB` / `SB`（その名前と、ヘッダーのバイト）。`gameMode` は `ground` / `air` / `naval`。ミッションのモード（`Dom`、`Conq`、`Bttl`、`I2M`...）と、インストールから得たその英語の名前（`Domination`、`Enduring Confrontation`）。許可された車両の種類（[戦闘モード](ground.md#battle-mode) を参照） |
| `settings` | ヘッダーの後にあるミッションの blk: モード、環境、天候、スコアと時間の制限、国、許可された車両の種類、風、そして `stars`（緯度、経度、日付、現地時刻） |
| `sky` | 最初の `CustomWeatherParams`: 太陽と月の方向、風、空の色、雲のずれ |
| `players`、`slots` | 結果のプレイヤーごとの 1 行（キル、地上でのキル、死亡、アシスト、スコア、占領、分隊、クラン、国、編成、操縦した uid）。リプレイのプレイヤースロット（名前、user ID、チーム） |
| `units` | リプレイが作ったすべてのユニットのエンティティ: eid、uid、テンプレート、車両、種類、型、チーム、プレイヤー、ミッション名、作られた時刻と取り除かれた時刻、作られた場所、読めなかったコンポーネント |
| `objects` | ミッションの名前付きオブジェクト: 位置と大きさのある占領地点と飛行場、点としての飛行場の輪郭、スポーンエリア |
| `objectives` | 戦闘の目的。それぞれ `type`（`capture_zone`、`airfield`、`helipad`、`base`、`spawn`、`convoy_spawn`、`battle_area`、`bombing_target`、`exit_zone`、`kill_area`、`rearm_zone`）、`team`（リプレイの 1 または 2。両方なら空）、`name`（占領地点はその文字、`A` など）、`shape`（`sphere`、`cylinder`、`box`、`point`、`points`、`outline`）と `position`、`radius` / `height` / `size`、`heading`、`source`（`replay` または `mission`）、そしてほかに分かっていること（[目的](objectives.md) を参照） |
| `kills`、`hits`、`modulesDestroyed` | 両陣営の名前と車両つき。キルには武器の英語名がつく |
| `weapons` | すべてのロケット、ミサイル、爆弾、魚雷、落下式燃料タンク、投棄された積荷: いつ、どこで放たれたか（位置、姿勢、速度）、どのユニットが放ったか（300 m 以内かつ 1.5 秒以内で最も近いもの）、飛行サンプルの数、最後に見られた場所、いつ取り除かれたか |
| `explosions`、`flak` | `PlayExplosionVisual`（位置、方向、種類）と `PlayFlakExplosionVisual`（位置） |
| `awards` | 録画しているプレイヤーの表彰（`TextStreak`: first_blood、連続記録、チャレンジの数） |
| `detections`、`unitStates` | `UnitDetected` のユニットの組。ユニットの位置、姿勢、速度を持つメッセージ（0xF093）。その意味は不明 |
| `authorInstruments` | 録画しているプレイヤーのコックピットの値（`ReplayCockpitParams`）を計器の番号ごとに、1 秒に 1 つまで。`known` はこのリプレイが送った各番号の名前（名前、ユニット、確かめ方）。`notNamed` はそれ以外 |
| `scoreboard` | 変わるたびの、すべてのプレイヤーの統計（キル、死亡、アシスト、スコア、AI キル、海上キル、ゾーン、ダメージ、ミサイル回避、分隊）。各チームのスコアと、時間ごとの推定チケット（[リプレイの内部データ](aircraft.md#reflection-data) を参照） |
| `economy` | 戦闘のシルバーライオンと研究ポイント（[経済](economy.md) を参照）: 合計、プレイヤーごと、車両ごと、倍率、勝者、確認 |
| `entityMessages` | クラス番号ごとのエンティティメッセージ（0x20）: 数、対象のテンプレート、サイズ |
| `chat` | すべてのチャットの行 |
| `triggers`、`hints`、`missionProgress` | ミッションスクリプトの動作（RunTriggerAction）、そのヒント、その進行のメッセージ |
| `camera` | 録画しているプレイヤーのリプレイカメラの項目を、送られてきたとおりに 0.25 秒ごと（テーブルではトラックとして入っています） |
| `projectileHitReplays` | 録画しているプレイヤー自身の命中と被弾。武器と弾薬、およびその英語名つき |
| `results` | ゲームが書いたままの、結果の blk すべて |
| `counts` | 行、イベント、生存、種類、サンプル、テンプレート別のエンティティ、武器、読んだパケットと読まなかったパケット、見たメッセージ ID と読まなかったもの、捨てたサンプル |
| `trackBreaks` | ユニットが進める速さを超えるステップで切られたトラックのすべての箇所: どこで、どれだけ、どれほど速く、そして最も可能性の高い原因 |
| `selfCheck` | [リプレイの読み取り方](how-it-reads.md) に挙げた確認。変換のたびに計算されます。`stepSpeed` は、ビューアがつなぐトラックの連続する行の間の速度を種類ごとに示します（中央値、99 パーセンタイル、最高、そして不可能な速さのステップ数。これは 0 でなければなりません） |

---

[3DHeat](https://github.com/Holdi601/3DHeat)（[ドキュメント](https://holdi601.github.io/3DHeat/)）の一部です。ソース: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder)。
