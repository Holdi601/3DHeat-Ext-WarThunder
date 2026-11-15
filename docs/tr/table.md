---
title: "Tablo"
nav_order: 6
lang: "tr"
source: table.md
source_hash: "eb510866a208"
nav_exclude: true
search_exclude: true
---
# Tablo {#the-table}

![Sentetik bir tekrarın tablosu, özet](../assets/img/table.svg)

Örnek ya da olay başına bir satır, 105 sütun ([Sütun listesi](../columns.md), koddan üretilmiştir); altbilgide, `heat3d`
altında, görüntüleyicinin okuma talimatları, böylece görüntüleyicinin doldurulacak bir form gerekmez.

| Sütun | Ne |
|---|---|
| `time` | tekrarın kendi saatindeki saniye |
| `event` | `position`; olay satırları anlarında izin üzerinde durur (iki örnek arasında, aralarındaki çizgide); `kill` (öldürenin yerinde), `death` (kurbanın yerinde), `hit_critical` / `hit_severe` (vurulan birimde), `module_destroyed` (birimde), `launch` (bir silahı bırakan birimde), `impact` (bir silahın hemen ardından kaldırıldığında son örneği); `explosion` ve `flak` (0xD08E, 0xD01F) konumlarında, tür `effect`, iz yok, patlamanın yönüyle varsa; `shot` (isabet eden bir mermi, atıcıda), `gun_shot`, `fire_start`, `fire_stop` (bir topun patlaması, yanan bir araç değil), `fire_on`, `fire_off` (yanan bir araç, bkz. [Araç yangınları](hits.md#vehicle-fires)), `reward` (kazanılan Gümüş Aslanlar ve araştırma puanları, bkz. [Ekonomi](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (bkz. [Birimlere giden iletiler](how-it-reads.md#messages-to-units)); `despawn`: tekrar bitmeden birimi yok olan bir izin son satırı (bkz. [Bir izin sonu](ground.md#end-of-a-track)) |
| `track` | görüntüleyicinin tek bir şey olarak çizdiği: bir birimin bir yaşamı ya da bir silahın bir uçuşu - `<player or vehicle> #<hex>` (görüntüleyici adı `#` kısmı olmadan gösterir) |
| `x`, `y`, `z` | oyunun metreleri: x doğu, y yukarı, z kuzey (ipuçları z'yi aynalar, böylece kuzey güney olarak çizilmez) |
| `player` | oyuncunun adı; bir AI birimi `<VehicleName> #<uid>` (örneğin `F-15A #204`); onu adlandıran bir şey yoksa `uid <n>`; bir silah için, onu bırakan |
| `userId`, `team` | oyuncunun Gaijin kimliği ve takımı (`1`, `2`) |
| `ai`, `isPlayer` | `ai`, hiçbir oyuncu hesabının sürmediği her birim için true (görev birimleri, AI uçaklar, kara hedefleri, hava savunma silahları, oyuncusu olmayan gemiler, yer tutucular), `isPlayer` tersidir: bir oyuncu, varlığı bir Gaijin kimliğiyle bir oyuncu yuvasını adlandıran birimdir. Bir silahın fırlatıcınınki vardır; bilinmiyorsa boş |
| `match` | maç kimliği (maç belgesinin `match`i), her satırda; ipuçları bunu oturum olarak eşler, böylece iki yüklü tekrar asla iz birleştirmez |
| `life` | `uid#n`: bir birimin izi, uid başka bir birime geçtiğinde, birim gidebileceğinden hızlı hareket ettiğinde (yeniden doğma, yeniden silahlanma, oyunun onu taşıması, istemcinin uzak bir birimi düzeltmesi; bkz. [Tekrarı nasıl okur](how-it-reads.md#what-is-read-and-the-check) içindeki Işınlanmalar) ya da uzun süre görülmediğinde kesilir; `w<hex>` bir silahın uçuşu (bir kesimden sonra `w<hex>#n`) |
| `uid` | tekrardaki birimin kimliği |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (haritanın yerleştirdiği bir tramvay ya da raylı vagon, bkz. [Sahne birimleri](objectives.md#scene-units-trams-and-rail-wagons)); silahlar `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned`; `camera` kayıt oyuncusunun tekrar kamerası (bkz. [Kamera](ground.md#the-camera)) |
| `type` | sonuçların adlandırdığı oyunun kendi türü (`fighter`, `assault`, `destroyer`, `gun_boat`), yoksa `kind` gibi |
| `Vehicle` | oyunun araç kimliği (`f_15a`, `germ_flakpz_I_Gepard`); görüntüleyicinin figürleri bununla eşleşir |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | aracın kurulumunuzun yerelleştirmesindeki İngilizce adı (`Pz.Kpfw. III Ausf. J1`, kısa `Pz.III J1`) ve anahtarı (`germ_pzkpfw_III_ausf_J_0`); oyun yazı tipinin ülke işaretleri dışarıda bırakılır. Oyunun hiçbir ad vermediği ya da hiçbir kurulumun bulunmadığı yerlerde ad kimliktir ve anahtar boştur |
| `mission` | birimin görevdeki adı (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | birimin baktığı yer (bakış vektörü): uçaklar uçuş modelinin yönelimiyle, kara birimleri ve gemiler kendi yönelimleriyle, silahlar uçuşları boyunca |
| `heading`, `pitch`, `roll` | aynısı derece cinsinden; heading pusuladır, kuzeyden saat yönünde, pitch burun yukarı pozitif, roll sağ kanat aşağı pozitif (uçuş modeli tersi işaret gönderir, bkz. [Yönelim, denetlenmiş](aircraft.md#attitude-checked); bir kara biriminin sağ tarafı aşağıda). İpuçları bunu `conventions` altında söyler |
| `turretYaw`, `gunPitch`, `turrets` | bir tankın ana tareti - kayıt oyuncusunun baktığı yer değil, topun gösterdiği yer; tekrarın değeri taret sürücüsünün hızına tutulmuş ve her ana top atışının çizgisine konmuş (bkz. [Taretler](ground.md#turrets)): gövdeye göre yaw (derece, yukarıdan bakıldığında saat yönünde pozitif, 0 tam öndedir) ve topun gövdeye göre pitch'i (derece, yukarı pozitif); `turrets` aracın her tareti kendi sırasıyla `yaw pitch;yaw pitch;...` olarak (kullanılmayan bir yuva `0.00 0.00` okunur). İstemci ve sunucu tekrarlarında tanklar, SPAA, APC'ler ve kamyonlar; gemiler değil (bkz. [Taretler](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | ana taret tekrarın gönderdiği haliyle; `turretYaw` / `gunPitch` onun taret sürücüsünün hızına tutulmuş ve her ana top atışının çizgisine konmuş hali (bkz. [Taretler](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | oyuncunun dünyada baktığı yer (kamerayla nişan alır): pusula dereceleri (0 kuzey, saat yönünde) ve yukarı derece, `aimHeading` / `aimPitch` ile aynı kural (gövdeye göre kalan `turretYaw` / `gunPitch`ın aksine). Bir sunucu tekrarında her oyuncunun tankı, bir istemci tekrarında kayıt oyuncunun kendisi; oyuncunun hiçbir yere nişan almadığı yerde boş (dört nişan şamandırası 0). Taret, kendi dönüş hızında bunu izler, bu yüzden dönerken ikisi farklıdır (bkz. [Taretler](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | kayıt oyuncusunun kendi tankı: nereye nişan aldığı (pusula dereceleri, yukarı derece, m cinsinden mesafe; görüşte bir şey yoksa 2000); kamera satırları: oyuncunun nişan aldığı yer (heading, pitch) |
| `zoom` | kamera satırları: kameranın büyütmesi (bkz. [Kamera](ground.md#the-camera)) |
| `difficulty`, `gameMode` | savaşın `AB`, `RB` ya da `SB`si ve `ground`, `air` ya da `naval`ı, her satırda (bkz. [Savaş modu](ground.md#battle-mode)) |
| `extrapolated` | istemcinin ölü hesaplaması olan, alınmış bir durum olmayan bir uçak örneği (bkz. [Ölü hesaplama](aircraft.md#dead-reckoning-and-the-smoother)); bırakılmasından hesaplanan bir bombanın örneği (bkz. [Tekrarı nasıl okur](how-it-reads.md#what-is-read-and-the-check) içindeki Uçuş kayıtları olmayan bombalar) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | yumuşatıcının örneği ne kadar taşıdığı (m) ve tekrarın kendi konumu ve yönelimi (tablonun işaretiyle roll) |
| `targetX`, `targetY`, `targetZ` | bir `shot`'ın isabet noktası |
| `hitOutcome`, `hitFlags` | bir `shot`'ın kara birimindeki sonucu: `kill`, `critical`, `penetration` ya da `nonpenetration` (sekmiş ya da durdurulmuş: tekrar bir ricochet'i ayırt etmez), sunucunun isabetle gönderdiği bitlerden (`hitFlags`, ham); hiçbiri gönderilmiyorsa boş (uçaklar, gemiler). Bkz. [İsabet sonuçları](hits.md#hit-outcomes) |
| `hitShell` | bir `shot`'ın mermi imzası: isabet iletisinin dört baytı (ham onaltılık); bir imza farklı mermileri temsil edebilir (120 ve 125 mm APFSDS aynısını paylaşır), bu yüzden ham tutulur, kalibre olarak okunmaz |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | bir `shot`'ın mühimmatı: türü (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) ve kimliği (`125mm_3bm46`), bir öldürmenin atıcının yuvasını adlandırdığı yerde, yoksa `explosive` (isabet patlaması) ya da `kinetic`; topun yeniden yüklemelerinden `weapon/slot`; kurulumun silah dosyalarından mm cinsinden kalibre. Bkz. [İsabet sonuçları](hits.md#hit-outcomes) |
| `rpm` | bir uçağın motor devri (motorlarının ortalaması), son gönderildiği gibi, 2 s içinde |
| `vx`, `vy`, `vz` | bir uçağın hızı, uçuş girdisinin gönderdiği gibi (m/s, oyunun eksenleri; 500 m/s'nin üzerindeki hızlar 500 okunur) |
| `engine`, `afterburner`, `engineCondition` | bir uçağın motorları uçuş girdisinden: `off`, `starting`, `running`, `dead` (motorları farklıysa `/` ile birleştirilmiş); yakıcı 0-1; yalnızca motor vurulduktan sonra gönderilen bir bayt |
| `weaponName` | öldürmeler ve ölümler: kurulumunuzun İngilizcesindeki silah ya da mühimmat (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | yalnızca kayıt oyuncusunun uçağı: kokpitinden gaz 0-1,1 (1,1 savaş acil gücü ya da yakıcı; aksi halde uçuş girdisinin on beşte birleri), uçuş girdisinden kontroller -1..1 (yükseklik sağa çekerken pozitif, kanatçık sağa yalparken pozitif), silah başına kalan mermi (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | yalnızca kayıt oyuncusunun uçağı, kokpitinden: gösterilen hava hızı ve tırmanış hızı (m/s), yakıt, manifold basıncı (atm), iniş takımı (0-1, 1 aşağıda), yağ ve silindir kafası sıcaklığı; kokpitinde gösterge varsa |
| `speed` | izin yaklaşık iki saniyesi üzerinden m/s (burada hesaplanır; tekrar diğer birimler için hız göndermez) |
| `alive` | bir birimin ölümünden sonraki örnekleri için 0 (enkazı): bir kara birimi ya da geminin, oyun onu kaldırana ya da örnekleri bitene kadar; bir uçağın en fazla 60 s |
| `otherVehicle`, `otherLife` | bir `shot`'ın kurbanı: aracı ve onun `life`'ı |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | bir `shot`'ın isabet noktası kurbanın kendi çerçevesinde (m; x ileri, y yukarı, z sola; bkz. [Birimlere giden iletiler](how-it-reads.md#messages-to-units)) ve atışın geldiği yön, kurbanın o andaki yönelimiyle o çerçeveye çevrilmiş |
| `hitPart`, `hitFlag` | bir `shot`'ın isabet iletisi: gönderildiği gibi parça sözcüğü ve yüksek baytı |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won` | savaşın neye mal olduğu ve neler kazandırdığı ve kimin kazandığı: bkz. [Ekonomi](economy.md) |
| `other`, `weapon` | öldürmeler: diğer taraf ve silah; isabetler: kimin vurduğu (kaydın uid'sinden, yoksa oyuncu yuvasından), aracı; ateşlemeler: silah; yok edilen modüller: 5 s içinde birimi son vuran kişi ve `part <n>` |

---

[3DHeat](https://github.com/Holdi601/3DHeat) parçası ([belgeler](https://holdi601.github.io/3DHeat/)). Kaynak: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
