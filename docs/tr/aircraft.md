---
title: "Uçaklar"
nav_order: 11
lang: "tr"
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Uçaklar {#aircraft}

Uçak sütunlarının nereden geldiğini ve onlara ne kadar güvenilebileceğini bilmek isteyenler içindir.
Aşağıdaki her denetim bir değeri, tekrarın bunu ikinci ve bağımsız bir yolla söylediği bir şeyle
karşılaştırır; yalnızca yöntem ve uyum verilir.

## Kokpit göstergeleri {#cockpit-instruments}

0xD04A iletisi kayıt yapan oyuncunun göstergelerini (sayı, değer) çiftleri olarak gönderir: arcade
savaşlarında saniyede dört, simulator savaşlarında yalnızca değişen değerler. Sayılar tüm kokpitler
üzerinde tek bir liste oluşturur ve bir kokpit, modelinin sahip olduğu göstergeleri gönderir. Oyunun
kodu hangi sayının hangi gösterge olduğunu belirler; bu yüzden her sayı yaptığı işe göre adlandırıldı ve
tekrara karşı denetlendi (`convert.INSTRUMENTS` sonucu tutar; kurulumdan hiçbir şey okunmaz):

| Sayı | Ad | Karşılaştırıldığı |
|---|---|---|
| 0 | gösterilen hava hızı, m/s | hava yoğunluğuna göre düzeltilmiş izin hızı: korelasyon 0,99 |
| 39 | tırmanış hızı, m/s | izin tırmanış hızı: korelasyon 0,99'un üzerinde |
| 40, 41 | irtifa, m; irtifa modulo 1000 | izin yüksekliği, birkaç metre farkla |
| 52, 53 | yapay ufuk yalpası ve yunuslaması | tablonun yalpasının ve yunuslamasının eksi hali, 1 dereceden az farkla |
| 64 | pusula | tablonun yönü (heading), 0,1 dereceden az farkla |
| 15-20 | dümen pedalları | uçağa etki eden yan kuvvet |
| 23, 31 | kumanda: yükseklik ve kanatçıklar (işaret kokpit modelininki gibi) | hücum açısı; yalpa hızı |
| 69, 71, 73 | saat: saat (12 saatlik kadran), dakika, saniye | kayıt bilgisayarının yerel zamanı, dakikaya kadar |
| 75 | manifold basıncı, atm | savaş acil gücünde tam gazdakinden daha yüksek |
| 81-86, 87-92, 93-98 | motor başına devir, devir modulo 1000, devir göstergesi | birbirleriyle birebir; motor devri: korelasyon 0,97'nin üzerinde |
| 195 | yakıt | bir sefer boyunca düşer, yeniden doğunca yeniden dolar |
| 228-230 | iniş takımı bacakları, 1 aşağıda | yalnızca havaalanlarının yüksekliğinde ve iniş hızında aşağıda |
| 240, 241 | motor başına gaz (1.1 savaş acil gücü ya da yakıcı) | uçuş girdisinin gazı |
| 330-332, 346-348 | mühimmat sayaçları (eşit iki küme) | silah ön ayarının mermileri, uçuş girdisinin mermileriyle birlikte düşer |
| 135, 159 | yağ ve silindir kafası sıcaklığı | olası: bir sefer boyunca yükselirler |
| 58, 61 | kayma topu, dönüş iğnesi | olası: yan kuvveti ve dönüş hızını izlerler |
| 223 | hava freni | olası: yalnızca yaklaşmada ayarlanır |
| 490-497, 500-505 | tekerlek frenleri | olası: yalnızca bir havaalanında dururken ayarlanır |

Anlamı bilinmeyen birkaç sayı daha gönderilir; bunlar maç belgesinin
`authorInstruments.notNamed` alanında tutulur.

Tablonun `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` ve
`throttle` sütunları bunlardan gelir: kayıt oyuncunun kendi satırlarında, örneğe en fazla 0,2 s kala
gelen son ileti alınarak.

## Uçuş girdileri {#flight-entries}

Her uçağın uçuş girdisi (paket türü 2), konumu ve yönelimi yanında şunları taşır:

- **Hız**: yönelimden sonra 32 bitlik bir sözcük. 31, 30 ve 29. bitler x, y ve z'nin işaretleridir; sonra
  hız 500/2047 m/s'lik 11 bitte (500 m/s'de durur), ardından |x| ve |y| hızın kesirleri olarak 9'ar bitte,
  ve z vektörü birim vektör yapan değerdir. Alınan örnekler arasındaki adımla denetlenir: yön, kayıt
  oyuncusu için derecenin kesrinde, diğerleri için yaklaşık 2 derece içinde uyuşur; hız %0,2 içinde.
  `selfCheck.flightEntries`.
- **Silah başına mermi**: konumdan önce bir liste, her silah için bir öğe, kalan mermi önce. Kayıt
  oyuncunun listesi, neredeyse her örnekte bir tık sonra kokpit sayaçlarına eşittir.
- **Kontroller ve gaz**: yüksekliğden sonra 14 nibble olarak okunan 7 bayt. Kayıt oyuncusu için her tikte:
  1 yükseklik, 2 kanatçıklar, 3 dümen (dinlenirken 8), 11 gaz on beşte birler olarak (savaş acil gücü ve
  yakıcıda da 15), 4 tekerlek frenleri, 5 hava freni, 8 olası fren paraşütü. Diğer uçakların nibble'ları bir
  savaşta yalnızca birkaç kez değişir ve o anki kontrolleri değildir.
- **Motorlar**: motor başına bir durum baytı (0 kapalı; 1-6 çalışıyor; 7 çalışır; 8 ölü), yalnızca yakıcıda
  16 bitlik bir değer (tam için 32767) ve motor vurulduktan sonra bir bayt. "Ölü" olan motorlu çoğu uçak ya
  öldürülür ya da birkaç dakika içinde biter.

## Yansıtma verisi {#reflection-data}

0xF02D ve 0xF0AA iletileri oyunun numaralı nesnelerini kopyalar: her nesne için kimliği (üst 5 bit tür,
alt 11 bit bir dizin) ve bir alan tablosu. Tür 14 oyuncu yuvalarıdır (alan 2 kullanıcı kimliği ve adı, 9
takım), tür 15 takımlardır (dizin 1 ve 2):

- Bir yuvanın 39 numaralı alanı istatistiklerini sabit yerlerde tutar: öldürmeler (ofset 0), takım
  öldürmeleri (2), ölümler (4), deniz öldürmeleri (10), AI öldürmeleri (12), AI kara öldürmeleri (14),
  yardımlar (20), ele geçirme bölgeleri (22), bölge hasarı (24, 32 bit), hasar ödülü (40, 32 bit), füze
  kaçışları (50). 38 numaralı alan skorla başlar, 42 numaralı alan birliktir. Bir savaşın sonunda her değer,
  her oyuncu için sonuçlardakine eşittir (`selfCheck.scoreboardVsResults`). Yerdeki öldürmelerin nerede
  tutulduğu bilinmiyor.
- Bir takımın 7 numaralı alanı skorudur: sonunda sonuçlardaki oyuncu skorlarının toplamına eşittir. 3
  numaralı alan olası biletleridir.
- Her ileti yalnızca değişen alanları gönderir; bu yüzden maç belgesindeki `scoreboard`, her değişiklikte
  her oyuncunun istatistiklerini ve her takımın skorunu listeler.

## Ölü hesaplama ve yumuşatıcı {#dead-reckoning-and-the-smoother}

Bir istemci tekrarı her uçağı, istemcinin çizdiği gibi saniyede dört kez kaydeder. Uzak bir uçak için
aldığı güncellemeler arasında istemci uçağı son hızı boyunca ileri taşır ve son oranlarında döndürür; bir
sonraki güncellemede onu oraya oturtur. Olduğu gibi okunan bir iz düz gider, sonra zıplar. Uçuş girdisinde
hangi örneklerin alındığını gösteren bir şey yoktur; ölü hesaplanmış bir örnek ne olduğuyla bulunur: ondan
önceki iki örneğin düz çizgisini, onların hızında, 3 cm içinde sürdürür.

Bunun ne kadar önemli olduğu savaşa bağlıdır: arcade savaşlarında diğer uçakların örneklerinin yaklaşık
yarısı ölü hesaplanmış olabilir, simulator savaşlarında yalnızca birkaç yüzde. Yumuşatıcı 15 g'yi aşan
adımları yaklaşık beş kez keser (`selfCheck.deadReckoning`). Kayıt oyuncunun kendi uçağı istemci tarafından
ekstrapole edilmez ve olduğu gibi bırakılır.

Varsayılan olarak (`--no-smoothing` kapatır), kayıt oyuncunun kendisi dışındaki tüm birimlerin izleri, alınan
durumların onları nerede gösterdiği yere konur: ölü hesaplanmış bir örnek, önündeki ve arkasındaki alınan
örnekler üzerinden geçen bir eğriye konur ve her birinin kendi hızı vardır; 3 s'den uzun sürelerde düz
çizgi yalnızca bir sonraki alınan örneğe doğru bükülür, böylece hiçbir örnek istemcinin kendi oturtmasından
daha uzağa gitmez. Yönelimi, bir alınan yönelimden bir sonrakine eşit biçimde döndürülür. Alınan örnekler,
hızlarının en fazla 2 m ya da 0,04 s'si kadar yumuşatılır; düzgün bir dönüş olduğu gibi kalır. Tekrarın kendi
değerleri `Raw` sütunlarında kalır.

## Yönelim, denetlenmiş {#attitude-checked}

Kayıt oyuncunun kendi uçağında yön, hareket yönünün (medyan) bir derece içindedir, yunuslama tırmanış açısının
birkaç derece içindedir ve açık dönüşlerde yalpa, neredeyse her örnekte dönüşün işaretine sahiptir: uçuş
modelinin yalpası sol kanat aşağıdayken pozitiftir, tablo bunu sağ kanat aşağıdayken pozitif olacak şekilde
çevirir (`selfCheck.aircraftAttitude`). 10 bitlik açılar 0,18 derecelik adımlarla ilerler. Kara birimlerinin
yönelimi, attıkları atışlarla denetlenir ([Taretler](ground.md#turrets)).

---

[3DHeat](https://github.com/Holdi601/3DHeat) parçası ([belgeler](https://holdi601.github.io/3DHeat/)). Kaynak: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
