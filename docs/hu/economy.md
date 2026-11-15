---
title: "Gazdaság"
nav_order: 14
lang: hu
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Gazdaság {#economy}

Mibe került a csata, és mennyit keresett, oszlopokként az eseménysorainál. Ezt a
**konvertáláskor a saját telepítésedből** olvassuk ki (`char.vromfs.bin`: `config/wpcost.blk`
járművenként, `config/warpoints.blk` és `config/rank.blk`; az `aces.vromfs.bin` fegyver-blokkjai
mondják meg, melyik módosítás melyik lövedék). A játék egyetlen száma sincs ebben a
tárolóban: az értékek csak a saját kimenetedbe kerülnek. A telepítés `char.vromfs.bin`
fájlja nélkül nem készül gazdaság (`economy.available` hamis). Az árak a csata
nehézségi szintjéhez tartoznak (`repairCostHistorical` RB-hez, `...Arcade` AB-hez,
`...Simulation` SB-hez).

| Oszlop | Sorok | Mi |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (a lövés után felvett lőszer, földi járművek), `launch` (repülőgépek, helikopterek) | a lövedék, rakéta vagy bomba ezüstoroszlán (SL) mért ára |
| `cost_lost_sl` | `death` egy játékos járműve | a jármű javítási költsége (alap; a blokkban a teljesen fejlesztett) |
| `earn_sl`, `earn_rp` | `reward` (új esemény, a kereső helyén és idejében) | a megszerzett SL és RP |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | minden `cost_*` vagy `earn_sl` sor | `SL` (az `earn_rp` kutatási pont) |
| `econ_basis` | ugyanez | `install` (a telepítésből olvasott ár) vagy `inferred` (kiszámolt, lent) |

**Ki nyert.** A `won` (0/1) egy csapat minden során ott szerepel, ahol a visszajátszás
ezt megmondja: a kliens-visszajátszás eredményei a szerző saját kimenetelét tartalmazzák
(`status`: `success` vagy `fail`), így a szerző csapata nyert vagy vesztett, a másik csapat
fordítva. Hogy melyik csapat nyert, azt a meccsdokumentum `result` mezője mondja meg
(`winner`, `status`, `authorTeam`). A szerver-visszajátszások és a vége előtt abbahagyott
visszajátszások nem tartalmaznak kimenetelt (a szerver-visszajátszás `status` mezője mindig
`success`, és nem nevez meg szerzőt), és egyik fajta sem tartalmazza a telepített
módosításokat: az eredmények játékosonként csak a járművek nevét és típusát sorolják fel.
Ezeknél a `won` üres marad.

A nézegető költségmodellje a `cost_*` (és `earn_*`) oszlopokat olvassa a `currency` mellett;
a `cost_fired_sl + cost_lost_sl` összege azt mutatja, hol költöttek el és vesztettek el
ezüstoroszlánokat, az `earn_sl` pedig azt, hol szereztek őket (egy ölés jutalma a saját
`reward` során áll, nem a `kill` soron, így semmi sem számolódik kétszer).

- **Lőszer** (`install`, ha a rekesz lövedékét ismerjük - egy ölés megnevezte, lásd
  [Találatok kimenetele](hits.md#hit-outcomes) -, különben `inferred`: annak a fegyvernek a
  lövedékeinek átlagos ára azon a járművön, amelyet kilőhet; egy alap lövedék ingyenes;
  a géppuskákat a visszajátszás nem számolja, ezek nem kerülnek semmibe).
- **Indítások** (`inferred`): a játék egy repülőgép fegyverkészletét bevetésenként árazza,
  nem tételenként; egy tétel a jármű árazott készleteinél az ár / tételek medián értéke
  (`sum_weapons`; az ellenintézkedések és a ledobható tartályok kimaradnak); 0, ahol a
  készlet ingyenes.
- **Jutalmak** (mind `inferred`): a visszajátszás nem tartalmaz jutalom-rekordot - az
  eredmények blokkja csak pontokat és számlálókat tartalmaz, egyetlen üzenet sem visz
  ezüstoroszlánt (ellenőrizve kliens- és szerver-visszajátszásokon). Egy `kill` `aKill`-t
  szerez, szorozva a gyilkos `rewardMul<mode>` értékével, az áldozat osztályának súlyával
  (`units` a warpoints.blk-ban, a `unitClass` szerint; a MI-egységeket a fajtájuk szerint),
  szorozva `aiKillK`-val MI-áldozat esetén, és `groundKillMul`-lal, ha repülőgép öl földi
  egységet; az RP ugyanígy, `expMul`-lal és a rank.blk súlyaival. A replikált eredménytáblában
  a játékos pontszámának minden más lépése annyi SL-t ér, ahány pontot ér a csata SL-pontja
  (egy ölés SL-je az ölések lépéseinek medián pontjára osztva, a blokk `pointsPerKill` értéke);
  típusa az a számláló, amely ezzel együtt nőtt (asszisztok, elfoglalt zónák, zónasebzés,
  sebzési jutalom, rakétakitérések), különben a játékos kritikus / súlyos találata 3 s-on belül,
  különben a játékos egységének felderítése 2 s-on belül (`scouting`), különben `other`.
  A `battle_end` a játékos csatabeli keresetének `winK` (nyert) vagy `defeatK` (vesztett)
  értéke; a győztest a csapatok hátralévő jegyei, utána a pontszám dönti el. A prémiumidő,
  a bónuszok, a legénység és a módosítások nem ismertek, és nincsenek alkalmazva; a földi
  csaták ölési költségkeretei (`def_ground_kill_wp_budget*`) nincsenek modellezve.

A meccsdokumentum `economy` mezője (egy `.3dheat` tárolóban pedig a manifest
`extensions["heat3d/economy"]` mezője) tartalmazza a `currency` `SL` értéket, a
`researchCurrency` `RP` értéket, a `difficulty` mezőt, a `totals` mezőt (`firedSl`, `lostSl`,
`earnedSl`, `earnedRp`), a `players` mezőt (ugyanez játékosonként, `netSl`-lel), a `vehicles`
mezőt (játékosonként a járműveik: `repairSl`, `repairFullUpgradedSl`, `purchaseSl`, `researchRp`,
`crewSl`, `crewExpertSl`, `rewardMul`, `expMul`, `groundKillMul`, `battleTimeAwardSl`, `rank`,
`economicRank`, `unitClass`), a `multipliers` mezőt (`aKill`, `aiKillK`, `winK`, `defeatK`,
`wpMultiplier`), a `winnerTeam`, a `pointsPerKill` és a `check` mezőt (minden fajta hány sort
árazott, becsült vagy nem árazott).

---

A [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentáció](https://holdi601.github.io/3DHeat/)) része. Forrás: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
