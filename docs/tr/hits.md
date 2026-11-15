---
title: "İsabetler, ateş ve yangınlar"
nav_order: 13
lang: tr
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# İsabetler, ateş ve yangınlar {#hits-gunfire-and-fires}

İsabet, mühimmat ve yangın sütunlarının nereden geldiğini bilmek isteyenler içindir. Denetimler yalnızca yöntemi
ve uyumu verir.

## Ateş {#gunfire}

Bir birime isabet eden her mermi tekrardadır (0xF0E9 iletisi): isabet anında atıcının konumunda bir `shot` satırı,
`targetX/Y/Z` isabet noktası (vurulan birim, kendi çerçevesinde isabet noktasıyla kaydırılmış, yönelimiyle
döndürülmüş), ona doğru yön, `other` vurulan birim. Isabet etmeyen mermiler ve kurşunlar gönderilmez: onlar
varlık değildir ve uçuştaki silah iletileri yalnızca roketleri, füzeleri, bombaları ve torpidoları tutar. Kayıt
oyuncusunun kalan mermileri (`ammo` sütunu) ateş ettikçe düşer; bu yüzden patlamaları ayırt edilebilir, ama bu
mermilerin nereye gittiği bilinmez. Ağır hava savunma ve topçu her tek atışı gönderir (`gun_shot`, yönü yok), 40 mm
hava savunma silahları ise patlamalarını (`fire_start`, `fire_stop`).

## İsabet sonuçları {#hit-outcomes}

Kara birimine her mermi isabetinde sunucu birime 0xF144 (UnitOnHit) iletisini gönderir: dört tek baytlık alan,
dördüncüsü isabetin ne yaptığının bitleri (`selfCheck.unitMessages.outcome_*`):

| Bit | Anlamı | Kanıt |
|---|---|---|
| 0x20 | merminin kendi isabeti | neredeyse hepsi, 5 ms içinde birimdeki bir 0xF0E9 isabetiyle gelir; onsuz, bir patlamayla (sıçrama) |
| 0x01 | nüfuz etti (penetrasyon) | 0x02, 0x04 ya da 0x08 içeren her ileti bunu da taşır |
| 0x02 | kritik isabet | kritik isabet kayıtlarının çoğunda var, şansın çok üzerinde |
| 0x04 | yok edildi | çoğu bir öldürme kaydı ve birimin bir saniye içinde ölümüyle gelir |
| 0x08 | ağır hasar | bazı kritik isabet kayıtlarında var; başka yerde nadir |

`hitOutcome` en kötüsünü alır: `kill` (0x04), `critical` (0x02 ya da 0x08), `penetration` (0x01),
`nonpenetration` (yalnız 0x20). Bir isabet, 5 ms içinde birimine en yakın eşleşmemiş, 0x20 içeren 0xF144 ile
eşleştirilir. Oyunun isabet kamerası bir sekmeyi bir nüfuz etmemeden ayırt eder, ama burada bulunan hiçbir bit ya
da alan bunu yapmaz: ilk üç bayt isabetten isabete değişir ve ne olduğu bilinmez. Kayıt istemcileri 0xF144'ü
yalnızca kayıt oyuncunun kendi uçağı için gönderir, tüm bitleri temiz: uçak ve gemi isabetlerinin sonucu yoktur.

## Mühimmat {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Patlayıcı mı değil mi.** Patlayan bir mermi, atıcının uid'si ve isabetin numarasıyla 0xF133 (UnitOnExplosion)
  gönderir; bununla gelen bir isabet `explosive`, diğerleri `kinetic`tir.
* **Top ve yuvası.** 0xF0BD (UnitBulletRearm) bir sonraki yüklenen mermidir: silahın araç silah listesindeki
  dizini, mühimmat yuvası ve kalan mermi. Elle yükleyicinin mermisi her isabetinden sonra sabit bir yeniden
  yükleme süresi sonra gelir, bir otomatik topunki ise saniyenin bir kesri sonra. Bir atıcının isabetleri araca,
  imzaya ve patlamaya göre gruplanır; bir grup, bir silahın, isabetlerinin yarısı ya da daha fazlasından sonra 20 s
  içinde, sabit bir gecikmeyle bir mermi yüklediği zaman o silahındır. `ammoSlot` `silah/yuva`dır, isabetten önce
  yüklenen yuva: büyük olasılıkla ateşlenen, oyuncu arada mühimmatı değiştirmediyse. Makineli tüfekler 0xF0BD
  göndermez.
* **Mermi.** Bir öldürmenin silahı mermi kimliğidir (`125mm_3bm46`); öldürenin kurbana son isabeti bunu o atıcının
  yuvasına verir, topun kalibresi tutarsa. Türü ve kalibresi silah dosyasınındır (`bulletName`, `bulletType`,
  `caliber`; `apds_fs_*` APFSDS, `heat_fs_*` HEAT-FS, `he_*` HE ...).
* **Diğerlerinin kalibresi:** bir yuvanın silahınınki; bir makineli tüfek grubunun, imzasının olabileceği tek
  makineli tüfek kalibresi; aksi halde aracın ana topununki. Kurulum olmadan (`--game`) `explosive` / `kinetic`in
  ötesinde tür, ad ya da kalibre yoktur.

Bulunamadı: mermi sekmesi (ricochet). Birkaç iletide daha isabetin atıcısı ve numarası vardır (0xF0C2, büyük olasılıkla
isabet kamerasının aracın içinden geçen yolu; 0xF117, 0xF13C, 0xF13E); bunlar yan dosyada tutulur, çözülmez. Nüfuz
etmeyen isabet `nonpenetration` olarak kalır.

## Araç yangınları {#vehicle-fires}

Yanan bir araç her istemciye gösterilir: sunucu araca bir varlık iletisi gönderir (olay `0a519c58`) ve listesi her
değiştiğinde üzerinde yanan yangınları listeler. Her yangın için: iki 16 bitlik kimlik (ikincisi bir hasar modeli
düğümü), türü ve yangın tutuşana kadar -1. Bir isabetle tutuşan yangın ayrıca, aracın çerçevesinde (x ileri, y
yukarı, z sola) yandığı noktayı içeren bir ileti alır.

Satırlar: yangın listede göründüğünde `fire_on`, gittiğinde `fire_off`, araçta, `fireId` (`first:node`), `fireKind`
ve bir isabetin tutuşturduğu yangınlar için `fireLocalX/Y/Z` (ileri, yukarı, sağ) ile. Bir araç öldüğünde listesi
genellikle bir daha gönderilmez: yangınları enkazıyla, yoksa varlığıyla, yoksa tekrarla biter
(`selfCheck.fires`).

Denetlendi: bir tankın yangın söndürücü sayısı her düştüğünde, bir yangın bir saniyenin kesri içinde listesinden
çıktı; yangın noktalarının çoğu, onları tutuşturan isabetle aynı tarafta. Türler sayılardır; neyi adlandırdıkları
bilinmez, bir düğümün hangi parça olduğu da. Uçaklar böyle bir liste göndermez: yanan bir uçak okunmaz.

---

[3DHeat](https://github.com/Holdi601/3DHeat) parçası ([belgeler](https://holdi601.github.io/3DHeat/)). Kaynak: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
