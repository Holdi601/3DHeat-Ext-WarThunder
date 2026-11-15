---
title: "Maç belgesi"
nav_order: 7
lang: tr
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# Maç belgesi {#the-match-document}

![Sentetik bir maç belgesinin başı ve anahtarları](../assets/img/match-document.svg)

`<match>.match.json`, tekrarın tablonun bir satırı olmayan her şeyini tutar. Görüntüleyicinin Maç sekmesi
onu okur.

## Savaş {#the-battle}

| Anahtar | Ne |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | maç kimliği (dosya adındaki gibi); haritanın kimliği; kullandığı harita dosyası |
| `mission`, `missionKey` | görevin adı ve oyunun metin dosyalarındaki anahtarı |
| `battleClass`, `environment`, `weather` | başlığın verdiği gibi |
| `sessionId`, `server` | savaşın oturum kimliği; sunucu |
| `replayVersion`, `flightLayout` | tekrar biçiminin sürümü; okunan uçuş paketi düzeni (`2025` ya da `2026`) |
| `files` | okunan tekrar dosyaları (bir tane ya da bir sunucu tekrarının parçaları) |
| `started`, `timePlayed`, `replayEnd` | başlangıç zamanı (ISO, UTC); sonuçlardan oynanan saniye; tekrarın son paketinin saniyesi |
| `author`, `authorUserId` | kayıt oyuncusu ve onun Gaijin kimliği (istemci tekrarları) |
| `teams` | savaştaki takımlar (`1`, `2`) |
| `result` | `winner`, `status` (`success` ya da `fail`, yazarın sonucu), `authorTeam`, `teams` ([Ekonomi](economy.md)) |
| `vehicleNames` | araç adlarının nereden geldiği (kurulumunuz) ve dilleri |
| `conventions` | tablonun birimleri ve işaretleri: eksenler, zaman, yaşam, iz, canlı, yalpa ve daha fazlası |

## Geri kalan her şey {#everything-else}

| Anahtar | Ne |
|---|---|
| `battle`, `difficulty`, `gameMode` | savaş modu: `difficulty` `AB` / `RB` / `SB` (adı ve başlık baytı), `gameMode` `ground` / `air` / `naval`, görevin modu (`Dom`, `Conq`, `Bttl`, `I2M`, ...) ve kurulumunuzdan İngilizce adı (`Domination`, `Enduring Confrontation`), izin verilen birim türleri (bkz. [Savaş modu](ground.md#battle-mode)) |
| `settings` | başlıktan sonraki görev blk'si: mod, ortam, hava, puan ve süre sınırları, ülkeler, izin verilen birim türleri, rüzgar ve `stars` (enlem, boylam, tarih, yerel saat) |
| `sky` | ilk `CustomWeatherParams`: güneş ve ay yönü, rüzgar, gökyüzü renkleri, bulut ofsetleri |
| `players`, `slots` | sonuçların oyuncu başına satırı (öldürmeler, zemin öldürmeleri, ölümler, yardımlar, skor, ele geçirmeler, birlik, klan, ülke, kadro, sürdükleri uid'ler); tekrarın oyuncu yuvaları (ad, kullanıcı kimliği, takım) |
| `units` | tekrarın oluşturduğu her birim varlığı: eid, uid, şablon, araç, tür, tip, takım, oyuncu, görev adı, oluşturulduğu ve kaldırıldığı zaman, oluşturulduğu yer, okunamayan bileşenler |
| `objects` | görevin adlandırılmış nesneleri: konumu ve boyutuyla ele geçirme bölgeleri ve hava alanları, hava alanlarının dış hatları noktalar olarak, doğma alanları |
| `objectives` | savaşın hedefleri, her biri `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (tekrarın 1 ya da 2'si; ikisi için boş), `name` (bir ele geçirme bölgesinin harfi, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) ile `position`, `radius` / `height` / `size` ve `heading`, `source` (`replay` ya da `mission`) ve bilinen diğer şeyler (bkz. [Hedefler](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | iki tarafın adları ve araçlarıyla; öldürmeler silahın İngilizce adıyla |
| `weapons` | her roket, füze, bomba, torpido, düşen tank ve atılan yük: ne zaman, nerede bırakıldığı (konum, yönelim, hız), hangi birim tarafından (300 m ve 1,5 s içindeki en yakın), kaç uçuş örneği, en son nerede görüldüğü, ne zaman kaldırıldığı |
| `explosions`, `flak` | `PlayExplosionVisual` (konum, yön, tür) ve `PlayFlakExplosionVisual` (konum) |
| `awards` | kayıt oyuncusunun ödülleri (`TextStreak`: first_blood, seriler, meydan okuma sayaçları) |
| `detections`, `unitStates` | birimlerin `UnitDetected` çiftleri; anlamı bilinmeyen, bir birimin konumunu, yönelimini ve hızını taşıyan bir ileti (0xF093) |
| `authorInstruments` | kayıt oyuncusunun kokpit değerleri (`ReplayCockpitParams`) gösterge numarasına göre, saniyede en fazla bir tane; `known` bu tekrarın gönderdiği her numarayı adlandırır (ad, birim, nasıl denetlendiği), `notNamed` gerisini |
| `scoreboard` | her oyuncunun istatistikleri değiştiğinde (öldürmeler, ölümler, yardımlar, skor, AI öldürmeleri, deniz öldürmeleri, bölgeler, hasar, füze kaçışları, birlik), ve her takımın skoru ve zamana göre olası biletleri (bkz. [Yansıtma verisi](aircraft.md#reflection-data)) |
| `economy` | savaşın Gümüş Aslanları ve araştırma puanları (bkz. [Ekonomi](economy.md)): toplamlar, oyuncu başına, araç başına, çarpanlar, kazanan, denetimler |
| `entityMessages` | sınıf numarasına göre varlık iletileri (0x20): sayı, hedef şablonlar, boyutlar |
| `chat` | her sohbet satırı |
| `triggers`, `hints`, `missionProgress` | görev betiğinin eylemleri (RunTriggerAction), ipuçları, ilerleme iletileri |
| `camera` | kayıt oyuncusunun tekrar kamerasının alanları, gönderildiği gibi her 0,25 s (tabloda bir iz olarak var) |
| `projectileHitReplays` | kayıt oyuncusunun kendi isabetleri ve isabet alması, silah ve mühimmat ile İngilizce adları |
| `results` | oyunun yazdığı sonuç blk'sinin tamamı |
| `counts` | satırlar, olaylar, yaşamlar, türler, örnekler, varlıklar (şablona göre), silahlar, okunan ve okunmayan paketler, görülen her ileti kimliği ve okunmayanlar, bırakılan örnekler |
| `trackBreaks` | birimin gidebileceğinden hızlı bir adım için bir izin her kesimi: nerede, ne kadar uzak, ne kadar hızlı ve en olası ne olduğu |
| `selfCheck` | [Tekrarı nasıl okur](how-it-reads.md) sayfasında listelenen denetimler, her dönüştürmede hesaplanır; `stepSpeed` görüntüleyicinin birleştirdiği gibi, bir izin ardışık satırları arasındaki hızı türe göre verir (medyan, 99. yüzdelik, en yüksek ve mümkün olandan hızlı adımlar, ki bu 0 olmalıdır) |

---

[3DHeat](https://github.com/Holdi601/3DHeat) parçası ([belgeler](https://holdi601.github.io/3DHeat/)). Kaynak: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
