---
title: "Ekonomi"
nav_order: 14
lang: tr
source: economy.md
source_hash: "870b7f982c6d"
nav_exclude: true
search_exclude: true
---
# Ekonomi {#economy}

Savaşın neye mal olduğu ve neyi kazandırdığı, olay satırlarında sütunlar olarak; **dönüştürme sırasında kendi
kurulumunuzdan** okunur (`char.vromfs.bin`: araç başına `config/wpcost.blk`, `config/warpoints.blk` ve
`config/rank.blk`; `aces.vromfs.bin`in silah blk'leri her mermunin hangi modifikasyon olduğunu söyler). Bu
depoda oyunun hiçbir sayısı yoktur: değerler yalnızca kendi çıktınıza girer. Kurulumun `char.vromfs.bin` dosyası
yoksa hiçbir ekonomi yazılmaz (`economy.available` false). Fiyatlar savaşın zorluğunun fiyatlarıdır
(RB için `repairCostHistorical`, AB için `...Arcade`, SB için `...Simulation`).

| Sütun | Satırlar | Ne |
|---|---|---|
| `cost_fired_sl` | `bullet_rearm` (bir atıştan sonra alınan mermi, kara araçları), `launch` (uçaklar, helikopterler) | SL: mermi, roket, füze ya da bombanın maliyeti |
| `cost_lost_sl` | bir oyuncunun aracının `death` satırı | aracın onarım maliyeti (stok; bloktaki tam yükseltilmiş olan) |
| `earn_sl`, `earn_rp` | `reward` (yeni olay, kazananın yerinde ve zamanında) | kazanılan SL ve RP |
| `rewardType` | `reward` | `kill`, `assist`, `capture`, `base_damage`, `damage`, `missile_evade`, `critical_hit`, `severe_damage`, `scouting`, `other`, `battle_end` |
| `currency` | bir `cost_*` ya da `earn_sl` içeren her satır | `SL` (`earn_rp` araştırma puanıdır) |
| `econ_basis` | aynısı | `install` (kurulumdan okunan bir fiyat) ya da `inferred` (aşağıda hesaplanmış) |

**Kim kazandı.** Bir takımın her satırında `won` (0/1), tekrarın söylediği yerde: bir istemci tekrarının
sonuçları yazarın kendi sonucunu taşır (`status`: `success` ya da `fail`), yani yazarın takımı kazandı ya da
kaybetti ve diğer takım tersi; maç belgesindeki `result` hangisi olduğunu söyler (`winner`, `status`,
`authorTeam`). Sunucu tekrarları ve sonundan önce bırakılan tekrarlar bir sonuç taşımaz (bir sunucu tekrarının
`status` değeri her zaman `success`tir ve yazarı adlandırmaz); ve iki tür de kurulu modifikasyonları taşımaz:
sonuçlar her oyuncunun araçlarını yalnızca ad ve tür olarak listeler. Orada `won` boş kalır.

Görüntüleyicinin maliyet modeli `cost_*` (ve `earn_*`) sütunlarını `currency` ile okur; `cost_fired_sl +
cost_lost_sl` toplamı SL'nin nerede harcandığını ve kaybedildiğini, `earn_sl` nerede kazanıldığını gösterir (bir
öldürmenin ödülü `kill` satırında değil kendi `reward` satırındadır, bu yüzden hiçbir şey iki kez sayılmaz).

- **Mermiler** (slot mermisi bilindiğinde `install`: bir öldürme adlandırmıştır, bkz. [İsabet sonuçları](hits.md#hit-outcomes);
  aksi halde `inferred`: o topun o araçta ateşleyebileceği mermilerin ortalama fiyatı; stok bir mermi bedavadır;
  makineli tüfekler tekrar tarafından sayılmaz ve bir şeye mal olmaz).
- **Ateşlemeler** (`inferred`): oyun bir uçağın silah ön ayarını sortiye göre fiyatlandırır, öğe başına değil; bir
  öğe, aracın fiyatlandırılmış ön ayarlarının fiyat / öğe sayısının medyanıdır (`sum_weapons`, karşı önlemler ve
  düşen tanklar dışarıda; ücretsiz ön ayarlar için 0).
- **Ödüller** (hepsi `inferred`): tekrar bir ödül kaydı taşımaz; sonuç bloğu yalnızca skor ve sayıları taşır, hiçbir
  ileti Gümüş Aslanları taşımaz (istemci ve sunucu tekrarlarında denetlendi). Bir `kill`, öldürenin `rewardMul<mode>`
  değeri çarpı kurbanın sınıf ağırlığı (warpoints.blk'deki `units`, `unitClass`'ına göre; AI birimleri türüne göre)
  çarpı bir AI kurbanı için `aiKillK` çarpı bir uçağın bir kara birimini öldürmesi için `groundKillMul` kadar
  kazandırır; RP aynı şekilde `expMul` ve rank.blk'nin ağırlıklarıyla. Oyuncunun çoğaltılmış skor tablosundaki
  skorunun diğer her adımı, puanlarınca, savaşın SL'si puan başına değerinde bir ödüldür (bir öldürmenin SL'si, öldürme
  adımlarının medyan puanına bölünmüş; bloktaki `pointsPerKill`). Türü, onunla birlikte artan sayaçtır (yardımlar,
  ele geçirilen bölgeler, bölge hasarı, hasar ödülü, füze kaçışları); yoksa o oyuncunun 3 s içindeki kritik / ağır
  isabeti; yoksa oyuncunun birimini 2 s içinde fark etme (`scouting`); yoksa `other`. `battle_end`, oyuncunun savaş
  içi kazançlarının `winK` (kazandı) ya da `defeatK` (kaybetti) değeridir; kazanan, takımların kalan biletleriyle,
  sonra skorlarıyla belirlenir. Prim süresi, güçlendiriciler, mürettebat ve modifikasyonlar bilinmez ve uygulanmaz;
  kara savaşlarının öldürme bütçeleri (`def_ground_kill_wp_budget*`) modellenmez.

Maç belgesinin `economy` alanı (ve bir `.3dheat` paketinde manifestin `extensions["heat3d/economy"]`) şunları tutar:
`currency` `SL`, `researchCurrency` `RP`, `difficulty`, `totals` (`firedSl`, `lostSl`, `earnedSl`, `earnedRp`),
`players` (oyuncu başına aynısı, `netSl` ile), `vehicles` (oyuncu aracı başına: `repairSl`, `repairFullUpgradedSl`,
`purchaseSl`, `researchRp`, `crewSl`, `crewExpertSl`, `rewardMul`, `expMul`, `groundKillMul`, `battleTimeAwardSl`,
`rank`, `economicRank`, `unitClass`), `multipliers` (`aKill`, `aiKillK`, `winK`, `defeatK`, `wpMultiplier`),
`winnerTeam`, `pointsPerKill` ve `check` (her türden kaç satırın fiyatlandırıldığı, tahmin edildiği ya da
fiyatlandırılamadığı).

---

[3DHeat](https://github.com/Holdi601/3DHeat) parçası ([belgeler](https://holdi601.github.io/3DHeat/)). Kaynak: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
