---
title: "Tekrarı nasıl okur"
nav_order: 10
lang: "tr"
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Tekrarı nasıl okur {#how-it-reads-a-replay}

Bu sayfa, dönüştürücünün neyi okuduğunu, nasıl denetlendiğini ve buna göre her sütuna ne kadar güvenileceğini
bilmek isteyenler içindir. Tekrarları dönüştürmek için buna ihtiyacınız yoktur.

Okuma, hava arcade, hava simulator ve deniz savaşlarının istemci tekrarlarında, kara savaşlarının sunucu
tekrarlarında ve 2025 düzenleri için [wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder)
projesinin herkese açık örnek tekrarlarında denetlendi. Her denetim bir değeri, tekrarın bunu ikinci ve bağımsız
bir yolla söylediği bir şeyle karşılaştırır; burada yalnızca yöntem ve uyum verilir.

## Neyi okur ve denetimi {#what-is-read-and-the-check}

| Parça | Durum ve denetim |
|---|---|
| Başlık, harita, görev, başlangıç zamanı, oturum; sonuçlar | her dosya |
| Görev ayarları (başlıktan sonraki blk) | mod, hava, sınırlar, `stars` (tarih, saat, yer) |
| Paket akışı (2025'te zlib, 2026'da zstd) | her paket çerçevelenmiş |
| Uçak konumları ve yönelimi (2026 düzeni) | saniyede 4 örnek, okunmadan kalan paket yok; yön, hareket yönüyle uyuşur |
| Zamanından önce gelen uçuş paketleri | bir ağ takılmasından sonra, bir istemci tekrarının uçuş paketi bazen her diğer uçağı yaklaşık 0,75 s sonra olacağı yerde tutar. Öncülük paket başına ölçülür ve öncülük eden her uçağa temsil ettiği zaman verilir (`selfCheck.flightPacketsRetimed`) |
| Ölü hesaplama oturmaları | ölü hesaplanmış bir çalışmanın dışındaki bir adım, son alınan durumdan ölçülür; böylece istemcinin düzeltmeleri artık izleri kesmez ([Ölü hesaplama](aircraft.md#dead-reckoning-and-the-smoother)) |
| Işınlanmalar | bir iz, birimi gidebileceğinden daha uzağa hareket ettiğinde kesilir: önce türüne karşı (uçak 750 m/s, kara ve gemiler 40 m/s, silahlar 1800 m/s), sonra kendi hızına karşı. Her kesim, muhtemel nedeniyle birlikte `trackBreaks` içinde listelenir (yeniden doğma, oyunun oyuncuyu taşıması, uzak bir birimin düzeltilmesi). Kesimlerden sonra, bir izin satırları arasındaki hiçbir adım türünün izin verdiğinden hızlı değildir (`selfCheck.stepSpeed`) |
| Kara ve gemi konumları (0xF073 / 0xF074) | okunmadan kalan paket yok. 16 bitlik yönelimden yön, yunuslama ve yalpa: yön, hareket yönüyle yaklaşık 2 derece içinde uyuşur (medyan); yunuslama 180/65536 derecelik adımlarla sayılır; yalpanın işareti çevrildiğinde, gövde ve tarettan topun yönü neredeyse her tank atışında vurulan birimi gösterir. Gemiler su seviyesinde durur |
| Taretler | tankların taret yaw'ı ve top pitch'i: bkz. [Taretler](ground.md#turrets) |
| Paketlenmiş kara yükseklikleri | 64 bitte paketlenmiş konumlar, çoğu haritada yüksekliklerini -100 m'den, bazılarında su seviyesinden sayar; ofset her tekrarda, iki biçimde de görülen birimlerden ölçülür (`selfCheck.packedGroundHeight`) |
| Varlık akışı (oluşturma, yok etme) | her oluşturma okunur. Düzen Dagor Engine'in yayımlanmış kaynağından gelir; War Thunder'ın kendi bileşen türleri, bir sonraki bileşenin nerede başladığını bularak atlanır. Her birimin araç ve oyuncu yuvası, denetlenen her kayıtta öldürme ve isabet kayıtlarının adlandırdıklarına eşittir |
| Hangi oyuncu hangi birimi sürdü, AI birimleri, gemiler, kara hedefleri | varlık akışından: her birimin aracı ve takımı vardır, her oyuncunun birimi de oyuncusudur |
| Sonuçlara karşı öldürmeler | oyuncu başına ölümler sonuçlardakine eşittir; sonuçlar daha çok öldürme sayar, çünkü istemciye her öldürme gönderilmez. Savaş başladıktan sonra başlayan bir tekrar yalnızca ondan sonraki öldürmeleri tutar |
| Öldürmeler, kritik isabetler, ağır hasar | her dosya |
| Yok edilen modüller (0xF118) | birim ve parçanın numarası; parçanın adı aracın hasar modelini gerektirir, bu da tekrarda yoktur |
| Bırakılan silahlar (varlık akışı) | bırakma noktası, en yakın birimden yaklaşık 10-20 m (medyan) uzaktadır; o birim fırlatıcı sayılır |
| Uçuştaki silahlar (0xF0DB) | füzeler, roketler ve bombalar, her biri kendi varlığına bağlı |
| Uçuş kayıtları olmayan bombalar | bunlar olmadan bir bomba, bırakılmasından çarpmasına kadar düşüşü hesaplanır (yerçekimi ve sürükleme, her 0,1 s bir örnek, `extrapolated` true). Çarpma yüksekliğinin bilindiği denizde denetlenmiştir: hesaplanan düşüşler suya yaklaşık 15 m içinde biter. Maç belgesinde böyle bir silahın `ballisticImpact` alanı vardır; `counts.bombsBallistic` bunları sayar |
| Oyuncu yuvaları, sohbet | her dosya |
| Patlamalar, flak patlamaları, ödüller, algılamalar, hava, görev nesneleri | okunur; konumlar görüntüleyicide göz kararı denetlendi |
| Kayıt oyuncusunun göstergeleri (0xD04A) | yaptıklarına göre adlandırılmış: [Kokpit göstergeleri](aircraft.md#cockpit-instruments); geri kalanlar `notNamed` altında |
| Uçuş girdilerinin diğer alanları | hız, mermiler, kontroller, motorlar: [Uçuş girdileri](aircraft.md#flight-entries) |
| Olay satırlarının yönelimi | her olay satırı, o andaki birimin yönünü, yunuslamasını, yalpasını ve bakış vektörünü taşır |
| Oyuncu istatistikleri ve takım skorları | savaşın sonunda her istatistik, her oyuncu için sonuçlardakine eşittir: [Yansıtma verisi](aircraft.md#reflection-data) |
| Silah ve araç adları | kurulumunuzun İngilizce yerelleştirmesinden; birkaç geminin varsayılan kuşakları ve havaalanı radarlarının oyunda adı yoktur |
| Oyuncular ve AI | sonuçlardaki bir oyuncunun satırı hiçbiri AI değildir, AI olmayan her satır sonuçlardaki bir oyuncunundur (`selfCheck.identity`) |
| Enkazlar | bir birimin ölümünden sonraki örnekleri gelmeye devam eder; bir kara birimi ya da geminin enkazı, varlığı kaldırılana kadar `alive` 0'dır ve tek bir iz olarak kalır; uçaklar `alive` 0'ı en fazla 60 s tutar (`selfCheck.wrecks`) |
| Araç değiştirmeleri | aynı oyuncunun bir sonraki birimi çıktığında hâlâ yaşayan bir oyuncu birimi orada sonlandırılır (ayakta bırakılan bir araç). `selfCheck.vehicleSwitch.twoLiveVehicles` 0 olmalıdır |
| Savaş modu | [Savaş modu](ground.md#battle-mode) |
| 2026 sunucu tekrarındaki uçaklar | 2026 düzeninde okunur; yön ve yalpanın işareti dönüşlerle uyuşur; yer tutucu uçaklar ve keşif dronları veri taşımaz |
| Sunucu tekrarının oyuncuları | yuvalarda ada göre bulunur; her istatistik sonuçlardakine eşittir (`selfCheck.players`) |
| 2025 sunucu tekrarlarındaki uçaklar ve 101286 sürümü | okunmaz: uçuş paketlerinin düzeni farklıdır |

## Birimlere giden iletiler {#messages-to-units}

Her tip-4 paketi, Dagor Engine'in daNet'inin bir mpi iletisidir: alıcı nesnenin kimliği, sonra (düşük 11 bitinin
hepsi birse) nesnenin ext UID'si, ileti kimliği ve yük. Bir birime giden bir ileti, ext UID olarak birimin varlık
kimliğini, `index << 10 | generation` taşır. Denetlendi: böyle her ileti, o anda yaşayan bir varlığı adlandırır.

Uzmanlar için, okunan iletiler:

| İleti | Nedir ve denetimi |
|---|---|
| 0xF0E9 UnitHitEffects | bir merminin isabeti: atıcının uid'si ve isabet noktası birimin çerçevesinde (x ileri, y yukarı, z sola): uçaklarda ve gemilerde santimetre, kara birimlerinde adım başına 20/32768 m (tank taretlerinin boyutuna uyarlanmış). `hitLocalX/Y/Z` metre cinsinden. Bir `shot` satırı olur ([Ateş](hits.md#gunfire)). Neredeyse her isabet ve öldürme kaydının saldırganı bu atıcılar arasındadır; isabet noktaları atıcıya bakan tarafta yer alır |
| 0xF133 UnitOnExplosion | aynı atıcı uid'si |
| 0xF04B OnUnitDead | `dead` satırları: her öldürme kaydının kurbanının 2 s içinde bir tane vardır |
| 0xD047 FmwRpm | motorların devri (`rpm`); kokpitin devir göstergesiyle uyuşur |
| 0xF0B1, 0xF0A0 | `gun_shot` satırları: ağır hava savunma ve topçunun tek atışları |
| 0xF01B, 0xF01C | `fire_start`, `fire_stop` satırları: 40 mm hava savunma silahlarının patlamaları (bir silahın ateşlemesi; bir araçtaki yangın `fire_on`dur, bkz. [Araç yangınları](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` satırları |
| 0xD0FE ProjectileHitReplay | kayıt oyuncusunun kendi isabetleri ve isabet alması, silah ve mühimmatla, kurulumdan adlandırılmış (`projectileHitReplays`) |
| 0xF13E, 0xF031 | bir isabetin görsel efekti ve birimde oynatılan bir efekt; aynı birimdeki bir isabetle birlikte gelirler |
| 0xD041 | bir uçağın her savunma silahı için bir, saniyede iki kez; indisleri uçuş modelinin nişancı silahlarıyla eşleşir |
| 0xD048, 0xF117 | düzen okunur, anlamı bilinmiyor |
| geri kalanlar (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | birimleri ve alanlarıyla birlikte ileti yan dosyasında |

Adlar topluluğun adlarıdır (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Ayrıca okunanlar {#also-read}

- **Varlık akışı çoğaltması** (0x22, 0x23): varlık başına bir bileşen değerleri bloğu: gemi onarım zamanlayıcıları,
  tüketilebilirlerin sayıları, sahip ve takım değişiklikleri, motor aşırı ısınması. `counts.replicatedComponents`
  içinde sayılır; değerler ileti yan dosyasında.
- **Görev betiği eylemleri** (0xF028) ve **ipuçları** (0xF0EC): `triggers`, `hints`. **Görev ilerlemesi** (0xF07A,
  0xF07C): `missionProgress`.
- **Tekrar kamerası** (0xD043): bkz. [Kamera](ground.md#the-camera).

## Okunmayanlar ve nedeni {#not-read-and-why}

- **Varlık iletilerinin adları ve gövdeleri** (0x20, 0x21): sınıf numarası, oyuna derlenmiş bir listedeki bir yerdir;
  gönderilmez ve verisinde yoktur. İkisi okunur (bir aracın yangınları ve söndürücüleri); geri kalanlar varlıkları ve
  sınıf numaraları ile bütün olarak tutulur.
- **Diğer kopyalanmış nesneler** (oyuncu yuvaları ve takımlar dışındaki türler): okunur ve tutulur, adlandırılmaz;
  denetleyecekleri sonuçlarda bir şey yoktur.
- **Diğer uçakların kontrolleri, gazı ve mermileri**: yalnızca ara sıra yenilenir; uçuş yan dosyasında tutulur,
  tabloda değil.
- **Uçak yangınları**: hiçbir iletide bulunmadı; yanan bir uçağın `fire_on` satırı yoktur.
- **Bırakılan silahların adları**: bir bombanın ya da roketin varlığı bir ad taşımaz; öldürme kayıtları bir öldürmenin
  silahını adlandırır.
- **Kaçan atışlar**: bir tekrar yalnızca isabetleri tutar.

Her maç belgesinin `counts.messageIdsNotRead` ve `selfCheck` alanları, yeni bir tekrarın neyi tuttuğunu ve ne kadar
iyi okunduğunu söyler.

---

[3DHeat](https://github.com/Holdi601/3DHeat) parçası ([belgeler](https://holdi601.github.io/3DHeat/)). Kaynak: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
