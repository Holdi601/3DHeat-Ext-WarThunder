---
title: "Kara birimleri ve kamera"
nav_order: 12
lang: "tr"
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Kara birimleri ve kamera {#ground-units-and-camera}

Taret, kamera ve savaş modu sütunlarının nereden geldiğini ve onlara ne kadar güvenilebileceğini bilmek
isteyenler içindir. Denetimler yalnızca yöntemi ve uyumu verir.

## Taretler {#turrets}

Bir tankın kara durumu (16 bit yönelim), konumundan sonra okunmayan 141 bit, sonra taret başına 62 bit
tutar: taretin yaw'ı ve topun pitch'i (her biri 16 bit, adım başına 360/65536 derece, işaretli) ve okunmayan
30 bit; sonra dolgu, ve bazı durumlarda 200 bit daha. Taret sayısı, durumdan önce gönderilen bayttır. Uzunluğu
uymayan bir durum taret vermez (sabit birimler daha kısa bir durum gönderir). Yaw gövdeye göredir, saat yönünde
pozitif, 0 tam öndedir; pitch gövdeye göredir, yukarısı pozitif.

Nasıl denetlendi:

- **Atışlara karşı:** bir tankın vurduğu her isabet için, ana topunun dünya yönü (gövde yönelimi taret yaw'ı
  ve top pitch'i kadar döndürülmüş) ile atıcıdan vurulan birime giden çizgi, en az 30 m uzaklıkta: savaş başına
  yönde 3 derece ve yükseklikte 99 % içinde medyan yaklaşık %98 (`selfCheck.turretsVsShots`). Kalanlar çoğunlukla
  başka bir tarette bulunan makineli tüfeğin isabetleridir.
- **Kayıt oyuncunun nişanına karşı:** kendi tankı nişanının dünya açısını (doğudan saat yönünün tersine), pitch'ini
  ve mesafesini gönderir. Gövde yönü artı taret yaw'ı, nişanın yarım derece içindedir (medyan).

**Sunucu tekrarları** (0xF074) her tankın durumunu aynı düzende gönderir, arkasından kendi verileriyle; bu yüzden
iki açısı durumun içinde kalan her taret okunur (neredeyse her tank satırında en azından ana taret). Bu taret,
kamera değil:

- **Atışlara karşı**, yukarıdaki gibi: savaş başına yönde 3 derecenin ve yükseklikte 99 %'ün üzerinde %90.
- **Görüşe karşı:** bir sunucu tekrarı her oyuncunun nişanını gönderir (`viewYaw`, `viewPitch`). Taret görüşü yarım
  derece içinde izler (medyan), ama görüş salınımından çok daha yavaş döner, bir taret sürücüsünün döndüğü gibi
  (`selfCheck.turretVsView`).
- **Ama her zaman bir sürücünün hızında değil:** örnek örnek, gönderilen değer nişan topa yakınken bazen nişanın
  üzerine atlar; bu, herhangi bir sürücünün döndüğünden hızlıdır.

Bu yüzden tabloda taret **sürücüsüne bağlı** tutulur: `turretYaw` / `gunPitch` gönderilen değere, ana topun
döndüğü hızdan (kurulumun araç dosyasından; mürettebat becerileri ve modifikasyonlar için 1,3 ile çarpılmış; adı
verilmemişse saniyede 45 ve 20 derece) daha hızlı olmadan yaklaşır. Ana topun her isabetinde taret tam olarak
atışın çizgisine konur ve geriye dönük bir geçiş onu zamanında oraya getirir (`selfCheck.turretLimit`). `shot`
satırı da bu `turretYaw` / `gunPitch` değerlerini taşır. Gönderilen değer `turretYawRaw` / `gunPitchRaw` içinde
kalır. Taret taşımayan bir tankın taret sütunları boştur (görüntüleyici `viewYaw`a dönebilir).
`gunPitch`, menzilde `viewPitch`in biraz üstündedir: merminin düşüşü için topun yükselmesi.

Gemi durumları başka bir düzene sahiptir; onların tareti okunmaz. Uçaklar baş ya da görüş yönü göndermez; uçak
savunma silahlarının 0xD020 iletisi okunmadan kalır.

## Kamera {#the-camera}

Saniyede yaklaşık yirmi kez gelen 0xD043 iletisi, kayıt oyuncusunun kendi tekrar kamerasıdır: alan 1, kameranın
önünü baktığı yere çeviren bir kuaterniyon; 2, takip ettiği araçtan kameranın yeri (m); 4, aynı ofset aracın
kendi çerçevesinde (x ileri, y yukarı, z sola); 5, oyuncunun nişan aldığı yer (birim vektör); 3, yakınlaştırma
(bir tankın üçüncü şahıs görünümünde yaklaşık 1,2, bir uçakta yaklaşık 1,0, bir topçunun dürbününde ya da
dürbünle bakıldığında daha yüksek). Denetlendi: alan 4, neredeyse her ileti için aracın çerçevesine çevrilmiş
alan 2'dir, 0,5 m içinde; kameranın önü nişanın yönüne sahiptir. Tekrar derece cinsinden görüş alanı göndermez,
yalnızca yakınlaştırmayı.

Tablo kamerayı kendi izi olarak tutar: tür `camera`, iz `<player> camera #ca`, en fazla 0,1 s'de bir satır, takip
edilen aracın yerinde artı alan 2, kuaterniyon boyunca bakan (`dirX/Y/Z`, `heading`, `pitch`, `roll`), `zoom`,
`aimHeading` ve `aimPitch` ile ve takip ettiği yaşam `otherLife`. `selfCheck.camera` satırları ve denetimi sayar.

## Bir izin sonu {#end-of-a-track}

Bir iz ilk satırından son satırına kadar çizilir. Tekrar bitmeden birimi yok olursa, son satırı son yerindeki bir
`despawn` satırıdır: oyunun varlığını kaldırdığı anda (son örneğinden 6 s içinde geldiyse), aksi halde son
örneğinde. Bunsuz bir iz tekrarın sonuna kadar sürer. Bir izin satırları birbirinden çok uzak olabilir (uzak bir
birim ya da bir enkaz birkaç saniyede bir tazelenir, bazen bir enkaz dakikalarca tazelenmez): son durumu bir
sonraki satırına kadar geçerlidir.

## Savaş modu {#battle-mode}

Başlığın 688. ofsetindeki bayt zorluğu alt dört bitinde tutar: 0 arcade (AB), 5 realistic (RB), 10 simulator
(SB). Tekrarların bilindiği savaş türlerine karşı denetlenir. Oyun modu, görev tanklara doğmaya izin veriyorsa
`ground`, değilse gemilere izin veriyorsa `naval`, aksi halde `air` (`allowedUnitTypes`); görevin kendi modu
anahtarından gelir (`missions/_Dom`), kurulumunuzdaki `lang/missions_versus.csv` dosyasından adlandırılır. Aynı
anahtar dosya adlarının ve maç kimliğinin `<mode>` kısmıdır (`Conq4`, `Dom`); başlıkta yoksa atlanır.

---

[3DHeat](https://github.com/Holdi601/3DHeat) parçası ([belgeler](https://holdi601.github.io/3DHeat/)). Kaynak: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
