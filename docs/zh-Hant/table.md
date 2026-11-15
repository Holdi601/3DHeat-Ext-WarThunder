---
title: "表格"
nav_order: 6
lang: zh-Hant
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# 表格 {#the-table}

![一個合成回放的表格，已摘要](../assets/img/table.svg)

每個取樣或事件一列，共 105 個欄位（[欄位清單](../columns.md)，由程式碼產生）；在結尾的 `heat3d` 下方有檢視器的讀取說明，因此檢視器不需要填寫任何表單。

| 欄位 | 內容 |
|---|---|
| `time` | 回放自身時鐘的秒數 |
| `event` | `position`；事件列位於其時刻的航跡上（位於兩個取樣之間，即它們之間的連線上）；`kill`（位於擊殺者處）、`death`（位於受害者處）、`hit_critical` / `hit_severe`（位於被命中的單位處）、`module_destroyed`（位於單位處）、`launch`（位於釋放武器的單位處）、`impact`（武器被移除前的最後一個取樣，若緊接在其後被移除）；`explosion` 與 `flak`（0xD08E、0xD01F）位於其位置，種類為 `effect`，沒有航跡，若有爆炸方向則附上；`shot`（命中的彈丸，位於射手處）、`gun_shot`、`fire_start`、`fire_stop`（火砲的連發，並非起火的載具）、`fire_on`、`fire_off`（起火的載具，見[載具火勢](hits.md#vehicle-fires)）、`reward`（獲得的銀獅幣與研究點數，見[經濟](economy.md)）、`dead`、`bailout`、`repair`、`rearm`、`bullet_rearm`、`reload`（見[送往單位的訊息](how-it-reads.md#messages-to-units)）；`despawn`：單位在回放結束前消失的航跡的最後一列（見[軌跡的結束](ground.md#end-of-a-track)） |
| `track` | 檢視器畫成一個東西的部分：單位的一個生命，或一枚武器的飛行——`<player or vehicle> #<hex>`（檢視器會顯示不含 `#` 部分的名稱） |
| `x`、`y`、`z` | 遊戲的公尺：x 朝東、y 向上、z 朝北（提示會將 z 鏡像，因此北方不會被畫到南方） |
| `player` | 玩家的名稱；AI 單位為 `<VehicleName> #<uid>`（例如 `F-15A #204`）；若沒有任何名稱，則為 `uid <n>`；對武器而言，為釋放它的人 |
| `userId`、`team` | 玩家的 Gaijin id，以及隊伍（`1`、`2`） |
| `ai`、`isPlayer` | 對於沒有任何玩家帳號駕駛的每個單位（任務單位、AI 飛機、地面目標、防空砲、沒有玩家的船艦、佔位單位），`ai` 為 true；`isPlayer` 則相反：玩家是指其實體命名了一個帶有 Gaijin id 的玩家槽位的單位。武器與其發射者相同；不明時為空 |
| `match` | 對戰 id（對戰文件中的 `match`），每一列都有；提示會將其對應為工作階段，因此兩個載入的回放不會把航跡接在一起 |
| `life` | `uid#n`：一個單位的航跡，在 uid 轉移到另一個單位時切斷、單位移動速度超過其可能（重生、重新裝填、遊戲移動它、客戶端修正遠處單位；見[讀取回放的方式](how-it-reads.md#what-is-read-and-the-check)中的瞬移）或長時間未被看到時也會切斷；`w<hex>` 為一枚武器的飛行（切斷後為 `w<hex>#n`） |
| `uid` | 該單位在回放中的 id |
| `kind` | `aircraft`、`helicopter`、`tank`、`apc`、`spaa`、`truck`、`ship`、`boat`、`structure`、`train`（地圖所放置的電車或鐵路車廂，見[場景單位](objectives.md#scene-units-trams-and-rail-wagons)）；武器為 `missile`、`rocket`、`bomb`、`torpedo`、`payload`、`jettisoned`；`camera` 為錄製玩家的回放攝影機（見[攝影機](ground.md#the-camera)） |
| `type` | 結算中遊戲自己命名的類型（`fighter`、`assault`、`destroyer`、`gun_boat`），否則與 `kind` 相同 |
| `Vehicle` | 遊戲自己的載具 id（`f_15a`、`germ_flakpz_I_Gepard`），檢視器的模型依此配對 |
| `VehicleName`、`VehicleShortName`、`VehicleNameKey` | 你安裝目錄中在地化的載具英文名稱（`Pz.Kpfw. III Ausf. J1`，簡稱 `Pz.III J1`）及其鍵（`germ_pzkpfw_III_ausf_J_0`）；遊戲字型中的國家標記會被略去。若遊戲未命名，或找不到安裝目錄，名稱即為 id，鍵為空 |
| `mission` | 任務中該單位的名稱（`t1_tank_05`、`t2_player03_0`） |
| `dirX`、`dirY`、`dirZ` | 單位所朝的方向（視線向量）：飛機取自飛行模型的姿態，地面單位與船艦取自其自身，武器則沿其飛行方向 |
| `heading`、`pitch`、`roll` | 以度為單位的相同資料；航向為羅盤，從北方順時針；俯仰機頭向上為正；橫滾右翼向下為正（飛行模型送出的符號相反，見[姿態核對](aircraft.md#attitude-checked)；地面單位則為右側向下）。提示在 `conventions` 下說明此事 |
| `turretYaw`、`gunPitch`、`turrets` | 坦克的主砲塔——砲口指向的方向，而非其駕駛者所看的方向；回放的數值受砲塔驅動器速度限制，並設定為每次主砲射擊的連線（見[砲塔](ground.md#turrets)）：其相對於車體的偏航角（度，從上方看順時針為正，0 為正前方），以及其砲管相對於車體的俯仰角（度，向上為正）；`turrets` 為該載具的每座砲塔，依其自身順序以 `yaw pitch;yaw pitch;...` 表示（未使用的槽位為 `0.00 0.00`）。適用於客戶端與伺服器回放中的坦克、防空車、裝甲運兵車與卡車；不適用於船艦（見[砲塔](ground.md#turrets)） |
| `turretYawRaw`、`gunPitchRaw` | 回放送出的主砲塔原始數值；`turretYaw` / `gunPitch` 則是其受砲塔驅動器速度限制、並設定為每次主砲射擊連線後的數值（見[砲塔](ground.md#turrets)） |
| `viewYaw`、`viewPitch` | 玩家在世界中所看的方向（用攝影機瞄準）：羅盤度數（0 為北，順時針）與向上的度數，與 `aimHeading` / `aimPitch` 的慣例相同（不同於保持相對於車體的 `turretYaw` / `gunPitch`）。伺服器回放中每位玩家的坦克，客戶端回放中則為錄製玩家自己的坦克；玩家未瞄準任何地方時為空（四個瞄準浮點數皆為 0）。砲塔以自己的旋轉速度跟隨它，因此兩者在砲塔轉動時會有差異（見[砲塔](ground.md#turrets)） |
| `aimHeading`、`aimPitch`、`aimDistance` | 錄製玩家自己的坦克：其瞄準的位置（羅盤度數、向上的度數、距離（公尺）；瞄準鏡中沒有任何東西時為 2000）；攝影機列：玩家瞄準的位置（航向、俯仰） |
| `zoom` | 攝影機列：攝影機的放大倍率（見[攝影機](ground.md#the-camera)） |
| `difficulty`、`gameMode` | 每一列都有：戰鬥的 `AB`、`RB` 或 `SB`，以及 `ground`、`air` 或 `naval`（見[戰鬥模式](ground.md#battle-mode)） |
| `extrapolated` | 屬於客戶端航位推算、而非其收到狀態的飛機取樣（見[航位推算](aircraft.md#dead-reckoning-and-the-smoother)）；由炸彈釋放推算出的炸彈取樣（見[讀取回放的方式](how-it-reads.md#what-is-read-and-the-check)中的沒有飛行紀錄的炸彈） |
| `moved`、`xRaw`、`yRaw`、`zRaw`、`headingRaw`、`pitchRaw`、`rollRaw` | 平滑器移動該取樣的距離（公尺），以及回放自己的位置與姿態（橫滾採用表格的符號） |
| `targetX`、`targetY`、`targetZ` | `shot` 的命中點 |
| `hitOutcome`、`hitFlags` | `shot` 對地面單位的結果：`kill`、`critical`、`penetration` 或 `nonpenetration`（彈開或被擋下：回放無法區分跳彈），依伺服器隨命中送出的位元（`hitFlags`，原始值）；若未送出（飛機、船艦），則為空。見[擊中結果](hits.md#hit-outcomes) |
| `hitShell` | `shot` 的砲彈特徵：命中訊息中的四個位元組（原始十六進位）；一個特徵可能代表不同的砲彈（120 與 125 公厘 APFSDS 共用一個），因此保留原始值，不解讀為口徑 |
| `ammoType`、`ammoName`、`ammoSlot`、`calibre` | `shot` 的彈藥：其類型（`APFSDS`、`APDS`、`HE`、`HEAT-FS`、`HESH`、`ATGM`...）與 id（`125mm_3bm46`），若擊殺命名了射手的槽位即為此，否則為 `explosive`（命中的爆炸）或 `kinetic`；火砲的 `weapon/slot` 來自其裝填；口徑為安裝目錄武器檔案中的公厘數。見[擊中結果](hits.md#hit-outcomes) |
| `rpm` | 飛機的引擎轉速（其各引擎的平均值），為最後送出的數值，於 2 秒內有效 |
| `vx`、`vy`、`vz` | 飛機的速度，即其飛行紀錄項目所送出的數值（公尺/秒，遊戲的座標軸；超過 500 m/s 的速度讀為 500） |
| `engine`、`afterburner`、`engineCondition` | 飛機的引擎，來自其飛行紀錄項目：`off`、`starting`、`running`、`dead`（引擎不同時以 `/` 連接）；加力燃燒室 0-1；僅在引擎被命中後送出的位元組 |
| `weaponName` | 擊殺與死亡：安裝目錄中的英文武器或彈藥名稱（`AIM-120C-5 AMRAAM air-to-air missiles`、`Fragmentation incendiary tracer shell`） |
| `throttle`、`elevator`、`aileron`、`rudder`、`ammo` | 僅限錄製玩家的飛機：來自座艙的油門 0-1.1（1.1 為戰爭緊急動力或加力燃燒室；否則為其飛行紀錄項目的十五分之一）；來自其飛行紀錄項目的操縱 -1 到 1（升降舵正值為拉起，副翼正值為向右橫滾）；每種武器剩餘的發數（`250 140 170`） |
| `ias`、`vario`、`fuel`、`manifoldPressure`、`gear`、`oilTemperature`、`headTemperature` | 僅限錄製玩家的飛機，來自其座艙：指示空速與爬升率（m/s）、燃油、進氣歧管壓力（atm）、起落架（0-1，1 為放下）、機油與汽缸頭溫度，前提是其座艙有該儀表 |
| `speed` | 航跡約兩秒內的速度（m/s，由此處算出；回放不為其他單位送出速度） |
| `alive` | 單位死亡後（其殘骸）的取樣為 0：地面單位或船艦的，直到遊戲將其移除或其取樣結束；飛機的最多 60 秒 |
| `otherVehicle`、`otherLife` | `shot` 的受害者：其載具與其 `life` |
| `hitLocalX`、`hitLocalY`、`hitLocalZ`、`hitDirX`、`hitDirY`、`hitDirZ` | `shot` 在受害者自身座標系中的命中點（公尺；x 向前、y 向上、z 向左；見[送往單位的訊息](how-it-reads.md#messages-to-units)），以及射擊來的方向，經受害者當時的姿態轉入該座標系 |
| `hitPart`、`hitFlag` | `shot` 的命中訊息：其送出的部位字，以及其高位元組 |
| `cost_fired_sl`、`cost_lost_sl`、`earn_sl`、`earn_rp`、`rewardType`、`currency`、`econ_basis`、`won` | 這場戰鬥花費與獲得多少，以及誰獲勝：見[經濟](economy.md) |
| `other`、`weapon` | 擊殺：另一方與武器；命中：誰擊中（來自紀錄的 uid，否則為其玩家槽位）與其載具；發射：武器；被摧毀的模組：在此之前 5 秒內最後擊中該單位的人，以及 `part <n>` |

---

屬於 [3DHeat](https://github.com/Holdi601/3DHeat)（[說明文件](https://holdi601.github.io/3DHeat/)）的一部分。來源：[3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder)。
