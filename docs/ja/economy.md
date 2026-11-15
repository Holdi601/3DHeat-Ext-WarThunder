---
title: 経済
nav_order: 14
lang: "ja"
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# 経済 {#economy}

戦闘でいくら使い、いくら稼いだかを、その戦闘の出来事の行の列として示します。値は**変換の時点でお使いのインストール**（`char.vromfs.bin`: 車両ごとの `config/wpcost.blk`、`config/warpoints.blk` と `config/rank.blk`。`aces.vromfs.bin` の武器の blk が、各砲弾がどの改造かを示します）から読まれます。ゲームの数値はこのリポジトリには含まれていません。値はお使いの出力にだけ入ります。インストールの `char.vromfs.bin` がなければ、経済は書かれません（`economy.available` が false）。価格は、その戦闘の難易度のものです（RB は `repairCostHistorical`、AB は `...Arcade`、SB は `...Simulation`）。

| 列 | 行 | 内容 |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm`（射撃の後に取る弾。地上の車両）、`launch`（飛行機、ヘリコプター） | 1 発、ロケット、ミサイル、爆弾のシルバーライオンでの費用 |
| `cost_lost_sl` | プレイヤーの車両の `death` | その車両の修理費（標準のもの。または、ブロックにある最大まで改造したもの） |
| `earn_sl`、`earn_rp` | `reward`（新しい出来事。稼いだ人の位置と時刻で） | 獲得したシルバーライオンと研究ポイント |
| `rewardType` | `reward` | `kill`、`assist`、`capture`、`base_damage`、`damage`、`missile_evade`、`critical_hit`、`severe_damage`、`scouting`、`other`、`battle_end` |
| `currency` | `cost_*` または `earn_sl` を持つすべての行 | `SL`（`earn_rp` は研究ポイント） |
| `econ_basis` | 同じ | `install`（インストールから読んだ価格）または `inferred`（下のとおり計算したもの） |

**勝ったのはどちらか。** リプレイが示している場合は、チームのすべての行に `won`（0/1）が入ります。クライアントのリプレイの結果には、録画者自身の結果（`status`: `success` または `fail`）が入るので、録画者のチームが勝ったか負けたか、もう一方のチームはその逆がわかります。マッチドキュメントの `result` がそれを示します（`winner`、`status`、`authorTeam`）。サーバーのリプレイと、終わる前に途中で止まったリプレイは結果を持たず（サーバーのリプレイの `status` は常に `success` で、録画者の名前も入りません）、どちらも改造したインストールの情報を持ちません。結果は各プレイヤーの車両を名前と種類だけで挙げるからです。その場合、`won` は空のままです。

ビューアの費用モデルは、`currency` と一緒に `cost_*`（と `earn_*`）の列を読みます。`cost_fired_sl + cost_lost_sl` を合計すると、シルバーライオンをどこで使い、どこで失ったかがわかり、`earn_sl` はどこで稼いだかを示します（キルの報酬はその `reward` の行にあり、`kill` の行にはないので、二重に数えられることはありません）。

- **弾** （`install`: スロットの砲弾がわかっている場合。キルがそれを挙げた場合。[命中の結果](hits.md#hit-outcomes) を参照。それ以外は `inferred`: その砲がその車両で撃てる砲弾の平均価格。標準の砲弾は無料。機関銃はリプレイでは数えられず、費用はゼロ）。
- **発射** （`inferred`）: ゲームは飛行機の武器のプリセットを、1 発ずつではなく出撃ごとに価格付けします。1 つの項目は、その車両の価格のあるプリセットの、価格を項目数で割った値の中央値です（`sum_weapons`。対抗手段と落下式燃料タンクは除く）。無料のプリセットは 0。
- **報酬**（すべて `inferred`）: リプレイには報酬の記録がありません。結果のブロックにはスコアと数しかなく、どのメッセージもシルバーライオンを運びません（クライアントとサーバーのリプレイで確認済み）。`kill` は、キラーの `rewardMul<mode>` × 被害者の種類の重み（warpoints.blk の `units`。その `unitClass` で。AI のユニットはその種類で）× AI の被害者の `aiKillK` × 航空機が地上のユニットを倒す場合の `groundKillMul` の、`aKill` 倍を獲得します。RP も同じで、`expMul` と rank.blk の重みを使います。マッチドキュメントの複製されたスコアボードにあるプレイヤーのそのほかのスコアの各ステップは、戦闘のシルバーライオン 1 ポイント分の価値の報酬です（キルのシルバーライオンを、キルのステップの点数の中央値で割ったもの。ブロックの `pointsPerKill`）。その種類は、それとともに上がったカウンターです（アシスト、占領したゾーン、ゾーンへのダメージ、ダメージの報酬、ミサイル回避）。それ以外で 3 秒以内にそのプレイヤーの致命的な命中または重大な命中があればそれ、それ以外でプレイヤーのユニットが 2 秒以内に発見されていれば `scouting`、それ以外は `other`。`battle_end` は、プレイヤーの戦闘中の稼ぎの `winK`（勝ち）または `defeatK`（負け）です。勝者はチームに残ったチケットで決まり、その後にスコアで決まります。プレミアム時間、ブースター、クルー、改造は、わかっておらず、適用されていません。地上の戦闘のキルの予算（`def_ground_kill_wp_budget*`）はモデル化されていません。

マッチドキュメントの `economy`（`.3dheat` コンテナーの中では、マニフェストの `extensions["heat3d/economy"]`）には、`currency` の `SL`、`researchCurrency` の `RP`、`difficulty`、`totals`（`firedSl`、`lostSl`、`earnedSl`、`earnedRp`）、`players`（同じものをプレイヤーごとに。`netSl` つき）、`vehicles`（プレイヤーの車両ごとに: `repairSl`、`repairFullUpgradedSl`、`purchaseSl`、`researchRp`、`crewSl`、`crewExpertSl`、`rewardMul`、`expMul`、`groundKillMul`、`battleTimeAwardSl`、`rank`、`economicRank`、`unitClass`）、`multipliers`（`aKill`、`aiKillK`、`winK`、`defeatK`、`wpMultiplier`）、`winnerTeam`、`pointsPerKill`、そして `check`（種類ごとに、価格が付けられた、推定された、価格がつかなかった行の数）が入ります。

---

[3DHeat](https://github.com/Holdi601/3DHeat)（[ドキュメント](https://holdi601.github.io/3DHeat/)）の一部です。ソース: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder)。
