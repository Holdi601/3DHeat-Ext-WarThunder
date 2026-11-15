---
title: テーブル
nav_order: 6
lang: ja
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# テーブル {#the-table}

![合成リプレイのテーブル、要約](../assets/img/table.svg)

サンプルまたはイベント 1 行につき 1 行で、105 列あります（[列の一覧](../columns.md)、コードから生成）。
フッターには `heat3d` の下に、ビューアの読み方の指示が入っています。そのためビューアで入力すべき項目はありません。

| 列 | 内容 |
|---|---|
| `time` | リプレイ自身の時計での秒 |
| `event` | `position`。イベントの行は、その瞬間のトラック上に置かれます（2 つのサンプルの間では、その間の線上）。`kill`（倒した側の位置）、`death`（倒された側の位置）、`hit_critical` / `hit_severe`（命中したユニットの位置）、`module_destroyed`（ユニットの位置）、`launch`（武器を放ったユニットの位置）、`impact`（武器が取り除かれる直前の最後のサンプル）。`explosion` と `flak`（0xD08E、0xD01F）は、その位置に、種類 `effect`、トラックなしで置かれ、向きがあればその方向も入ります。`shot`（命中した発射物。射手の位置）、`gun_shot`、`fire_start`、`fire_stop`（砲の連射。車両の火災ではない）、`fire_on`、`fire_off`（火災中の車両。[車両の火災](hits.md#vehicle-fires) を参照）、`reward`（獲得したシルバーライオンと研究ポイント。[経済](economy.md) を参照）、`dead`、`bailout`、`repair`、`rearm`、`bullet_rearm`、`reload`（[ユニットへのメッセージ](how-it-reads.md#messages-to-units) を参照）。`despawn`: リプレイが終わる前にユニットが消えたトラックの最後の行（[トラックの終わり](ground.md#end-of-a-track) を参照） |
| `track` | ビューアが 1 つのものとして描くもの。ユニットの 1 回の生存、または武器 1 本の飛行: `<player or vehicle> #<hex>`（ビューアは `#` の部分を除いた名前を表示します） |
| `x`、`y`、`z` | ゲームのメートル単位: x は東、y は上、z は北（ヒントで z を反転するので、北は南に描かれません） |
| `player` | プレイヤーの名前。AI ユニットは `<VehicleName> #<uid>`（例: `F-15A #204`）。名前がないものは `uid <n>`。武器の場合は、それを放ったのが誰か |
| `userId`、`team` | プレイヤーの Gaijin ID とチーム（`1`、`2`） |
| `ai`、`isPlayer` | `ai` は、どのプレイヤーアカウントも操作していないユニットすべてで true（ミッションのユニット、AI の飛行機、地上の目標、対空砲、プレイヤーのいない艦船、ダミーの機体）。`isPlayer` はその反対: プレイヤーとは、そのエンティティがプレイヤースロットを指していて Gaijin ID を持つユニットです。武器は発射したユニットの値を持ちます。わからない場合は空欄 |
| `match` | マッチ ID（マッチドキュメントの `match`）。すべての行に入ります。ヒントはこれをセッションとして扱うため、読み込んだ 2 つのリプレイのトラックが混ざることはありません |
| `life` | `uid#n`: 1 つのユニットのトラック。その uid が別のユニットに移ったとき、ユニットが速すぎる速度で動いたとき（リスポーン、再武装、ゲームによる移動、遠くのユニットのクライアントによる補正）、または長く見えていないときに切られます（[リプレイの読み取り方](how-it-reads.md#what-is-read-and-the-check) の瞬間移動を参照）。`w<hex>` は武器の飛行（切れた後は `w<hex>#n`） |
| `uid` | リプレイ内のユニットの ID |
| `kind` | `aircraft`、`helicopter`、`tank`、`apc`、`spaa`、`truck`、`ship`、`boat`、`structure`、`train`（レベルが置く路面電車や鉄道車両。[シーンのユニット](objectives.md#scene-units-trams-and-rail-wagons) を参照）。武器は `missile`、`rocket`、`bomb`、`torpedo`、`payload`、`jettisoned`。`camera` はプレイヤーのリプレイカメラ（[カメラ](ground.md#the-camera) を参照） |
| `type` | 結果がゲーム自身の種類を示している場合はその種類（`fighter`、`assault`、`destroyer`、`gun_boat`）。それ以外は `kind` と同じ |
| `Vehicle` | ゲームの車両 ID（`f_15a`、`germ_flakpz_I_Gepard`）。ビューアの図がこれと合わせられます |
| `VehicleName`、`VehicleShortName`、`VehicleNameKey` | インストールの英語の翻訳から取った車両の英語名（`Pz.Kpfw. III Ausf. J1`、短い名前は `Pz.III J1`）と、そのキー（`germ_pzkpfw_III_ausf_J_0`）。ゲームのフォントの国のマークは除かれます。ゲームが名前を付けていない場合、またはインストールが見つからない場合は、名前が ID になり、キーは空になります |
| `mission` | ミッションの中でのユニットの名前（`t1_tank_05`、`t2_player03_0`） |
| `dirX`、`dirY`、`dirZ` | ユニットが向いている方向（向きベクトル）。飛行機は飛行モデルの姿勢から、地上のユニットと艦船は自身の姿勢から、武器は飛行の向きから |
| `heading`、`pitch`、`roll` | 同じものを度で表したもの。heading は方位（北から時計回り）、pitch は機首上げが正、roll は右翼下げが正です（飛行モデルは逆の符号で送ってきます。[姿勢の確認](aircraft.md#attitude-checked) を参照。地上のユニットは右側が下がると正）。ヒントは `conventions` の下にそれを書いています |
| `turretYaw`、`gunPitch`、`turrets` | 戦車の主砲の砲塔。プレイヤーが見ている方向ではなく、砲がどこを向いているか。リプレイの値を砲塔の旋回速度に合わせて抑え、主砲の各射撃の線に合わせたもの（[砲塔](ground.md#turrets) を参照）。車体に対する旋回角（度、真上から見て時計回りが正、正面が 0）と、砲の俯角（車体に対して、上が正）。`turrets` は、車両のすべての砲塔を自身の順番で `yaw pitch;yaw pitch;...` と並べたもの（使われていない枠は `0.00 0.00`）。戦車、SPAA、APC、トラックのもの。クライアントとサーバーのリプレイの両方。艦船は対象外（[砲塔](ground.md#turrets) を参照） |
| `turretYawRaw`、`gunPitchRaw` | リプレイが送ってきたままの主砲の砲塔。`turretYaw` / `gunPitch` は、それを砲塔の旋回速度に合わせて抑え、主砲の各射撃の線に合わせたもの（[砲塔](ground.md#turrets) を参照） |
| `viewYaw`、`viewPitch` | プレイヤーが見ている方向（カメラで狙っている方向）。世界での値: 方位（度、0 が北、時計回り）と上向きの角度（度）。`aimHeading` / `aimPitch` と同じ向きです（車体に対する相対値の `turretYaw` / `gunPitch` とは違います）。サーバーのリプレイでは、すべてのプレイヤーの戦車。クライアントのリプレイでは、録画しているプレイヤー自身の戦車。プレイヤーがどこも狙っていない場合は空欄（4 つの狙いの浮動小数点数がすべて 0）。砲塔は自身の旋回速度で追いかけるので、回っている間は 2 つの値が違います（[砲塔](ground.md#turrets) を参照） |
| `aimHeading`、`aimPitch`、`aimDistance` | 録画しているプレイヤー自身の戦車: 狙っている方向（方位の度、上向きの度、距離はメートル。照準に何もないときは 2000）。カメラの行では、プレイヤーが狙っている方向（heading、pitch） |
| `zoom` | カメラの行: カメラの倍率（[カメラ](ground.md#the-camera) を参照） |
| `difficulty`、`gameMode` | 戦闘の `AB`、`RB`、`SB`、および `ground`、`air`、`naval`。すべての行に入ります（[戦闘モード](ground.md#battle-mode) を参照） |
| `extrapolated` | クライアントの推測航法によるサンプルで、受信した状態ではない飛行機のサンプル（[推測航法](aircraft.md#dead-reckoning-and-the-smoother) を参照）。発射から計算された爆弾のサンプル（[飛行記録のない爆弾](how-it-reads.md#what-is-read-and-the-check) の「飛行記録のない爆弾」を参照） |
| `moved`、`xRaw`、`yRaw`、`zRaw`、`headingRaw`、`pitchRaw`、`rollRaw` | 補正がサンプルをどれだけ動かしたか（m）と、リプレイ自身の位置と姿勢（roll はテーブルの符号で） |
| `targetX`、`targetY`、`targetZ` | `shot` の命中点 |
| `hitOutcome`、`hitFlags` | 地上のユニットに対する `shot` の結果: `kill`、`critical`、`penetration`、`nonpenetration`（跳ね返った、または止められた。リプレイは跳弾を区別しません）。サーバーが命中とともに送るビット（生の `hitFlags`）から。送られていない場合は空欄（飛行機、艦船）。[命中の結果](hits.md#hit-outcomes) を参照 |
| `hitShell` | `shot` の弾の署名: 命中メッセージの 4 バイト（生の 16 進数）。1 つの署名が異なる弾を表すことがある（120 mm と 125 mm の APFSDS は同じ署名を共有する）ため、口径としては読まず、生のまま残します |
| `ammoType`、`ammoName`、`ammoSlot`、`calibre` | `shot` の弾薬: その種類（`APFSDS`、`APDS`、`HE`、`HEAT-FS`、`HESH`、`ATGM`...）と ID（`125mm_3bm46`）。キルが射手のスロットを名指ししている場合はそれ。それ以外は `explosive`（命中の爆発）か `kinetic`。砲の `weapon/slot` は再装填から。口径は mm で、インストールの武器ファイルから。[命中の結果](hits.md#hit-outcomes) を参照 |
| `rpm` | 飛行機のエンジンの回転数（エンジンの平均）。最後に送られてきた値で、2 秒以内のもの |
| `vx`、`vy`、`vz` | 飛行機の速度。飛行エントリが送るとおり（m/s、ゲームの軸。500 m/s を超える速度は 500 と読む） |
| `engine`、`afterburner`、`engineCondition` | 飛行機のエンジン。飛行エントリより: `off`、`starting`、`running`、`dead`（エンジンが異なるときは `/` でつなぐ）。アフターバーナーは 0〜1。エンジンが被弾した後にだけ送られる 1 バイト |
| `weaponName` | キルと死亡: インストールの英語の武器または弾薬（`AIM-120C-5 AMRAAM air-to-air missiles`、`Fragmentation incendiary tracer shell`） |
| `throttle`、`elevator`、`aileron`、`rudder`、`ammo` | 録画しているプレイヤーの飛行機だけ: スロットル 0〜1.1（コックピットから。1.1 は戦争用非常出力またはアフターバーナー。それ以外は飛行エントリの 15 分の 1 単位）、操縦桿 −1〜1（飛行エントリから。エレベーターは引くと正、エルロンは右へのロールが正）、武器ごとの残りの弾数（`250 140 170`） |
| `ias`、`vario`、`fuel`、`manifoldPressure`、`gear`、`oilTemperature`、`headTemperature` | 録画しているプレイヤーの飛行機だけ。コックピットから: 指示対気速度と上昇率（m/s）、燃料、吸気圧（atm）、降着装置（0〜1、1 が下り）、オイルとシリンダーヘッドの温度。コックピットにそのメーターがある場合のみ |
| `speed` | トラックの約 2 秒にわたる m/s（ここで計算。リプレイは他のユニットの速度を送らない） |
| `alive` | ユニットが死んだ後（残骸）のサンプルは 0。地上のユニットや艦船の場合、ゲームが取り除くまで、またはサンプルが終わるまで。飛行機の場合は最長 60 秒 |
| `otherVehicle`、`otherLife` | `shot` の被害者: その車両と、その `life` |
| `hitLocalX`、`hitLocalY`、`hitLocalZ`、`hitDirX`、`hitDirY`、`hitDirZ` | `shot` の命中点を被害者自身の座標系で（m。x は前、y は上、z は左。[ユニットへのメッセージ](how-it-reads.md#messages-to-units) を参照）、および射撃の来た方向を、そのときの被害者の姿勢でその座標系に変換したもの |
| `hitPart`、`hitFlag` | `shot` の命中メッセージ: 送られてきたままの部位の語と、その上位バイト |
| `cost_fired_sl`、`cost_lost_sl`、`earn_sl`、`earn_rp`、`rewardType`、`currency`、`econ_basis`、`won` | 戦闘でいくら使い、いくら稼いだか、そして勝者: [経済](economy.md) を参照 |
| `other`、`weapon` | キル: 相手側と武器。命中: 誰が当てたか（記録の uid から、なければプレイヤーのスロットから）、その車両。発射: 武器。破壊されたモジュール: 5 秒前までにそのユニットに最後に当てた者と、`part <n>` |

---

[3DHeat](https://github.com/Holdi601/3DHeat)（[ドキュメント](https://holdi601.github.io/3DHeat/)）の一部です。ソース: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder)。
