---
title: "Hedefler"
nav_order: 15
lang: tr
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Hedefler {#objectives}

Maç belgesindeki `objectives`, savaşın üzerinde yapıldığı şeyleri iki kaynaktan (`source`) listeler:

- **Tekrar** (`replay`): 0xD039'un adlandırdığı görev nesneleri (ele geçirme bölgeleri `cz_circle_NN`,
  hava alanları, helikopter pedleri, üsler); bunlar kind 3 (0xF02D) kopyalanmış nesnelerin şimdi
  koyduğu yerde durur: bir ele geçirme bölgesi şablonunun yerinde başlar ve başlangıçta bu modun
  bölgesine taşınır (`moved`). Kind 3'ün numaraları 0xD039'un sırasını izler; taşınmayan her nesne
  tam olarak 0xD039'un koyduğu yerdedir, bu da sırayı denetler. Bir ele geçirme bölgesi, bulunduğu
  yerdeki görev alanının şeklini ve yarıçapını alır (`area`, 2 m içinde) ve harfini kendi dizininden
  alır (kind 5 alanı 69: 0 = A); harf sırası tekrarınkidir, oyunun haritasıyla karşılaştırılmaz.
- **Görev** (`mission`): kurulumunuzun `mis.vromfs.bin` dosyasındaki `<mission>.blk` görev dosyası
  ve içe aktardığı şablonlar (yalnızca okunur, dönüştürme sırasında): alanları, adlarına göre
  sınıflanmış: doğma noktaları (bir doğma noktasının numaralı noktaları `..._spawnareaNN` tek bir
  `points` doğma noktası olarak), savaş alanları, bombalama hedefleri (`bomb_zone`), konvoy doğma
  noktaları (`road_NN_spawn`), çıkış ve öldürme alanları. Aynı haritanın başka bir modunun alanları
  (`conq_`, `dom_`, `bttl_`, ...) dışarıda bırakılır; `_arcade` / `_realistic` / `_hardcore`
  varyantlarından savaşın kendisininki alınır (RB `_realistic`'i, yoksa `_hardcore`'u alır, görev
  betiklerinin yaptığı gibi); brifing işaretçileri, hava savunma silahı noktaları ve 5 km'den geniş
  alanlar (doğma noktalarının dağıldığı alanlar) da dışarıda kalır. Her doğma noktası, kaç oyuncunun
  izinin orada başladığını söyler (`used`, `usedByTeam`). Bir görev tarafları rastgele değiştirebilir
  (`randomSpawnTeams`): doğma noktaları tekrarın takımlarını ters yönde gösterdiğinde her `team`
  değiştirilir ve adın tarafı `missionTeam` olarak korunur. Konvoy rotaları okunduğu haliyle görevlerin
  waypoint'lerinde yer almaz; yalnızca konvoyların göründüğü yerde verilir.

Zamana göre ele geçirme bölgeleri, `<match>.objectives.parquet` yan dosyasındadır: her bölge için bir
tane olmak üzere kind 5 kopyalanmış nesneler; alan 2 sahibi (0, 1, 2), alan 67 ele geçirme ilerlemesi,
-100 ile 100 arasında işaretli bir bayt (takım 2 yönünde pozitif), alan 69 dizini. Denetlenir
(`selfCheck.objectives`), Ele Geçirme ve Hakimiyet savaşlarının gerçek zamanlı sunucu tekrarlarında:
sahip her değişikliğe, aynı anda (1,5 s içinde), ele geçiren takımdan bir oyuncunun skor tablosunda
bir `captureZone` kazanması ve o takımdan bölgenin içinde yaşayan bir kara birimi eşlik eder; her
savaşın doğma noktaları, tekrarın takımlarını yalnızca bir yönde gösterir (çoğu zaman görevin
`t1_` / `t2_` takımlarına göre ters).

## Sahne birimleri: tramvaylar ve raylı vagonlar {#scene-units-trams-and-rail-wagons}

Bir harita kendi birimlerini de yerleştirebilir: bir sunucu tekrarındaki `unit_loader+rail_wagon`
varlıkları, haritanın sahne dosyasının tramvaylarıdır (`gamedata/scenes/<level>_objects.blk`,
`aces.vromfs.bin` içinde: `setting__unit_class`, dönüşümü ve `setting__isDead`). Bu varlıklar okunabilir
bir uid taşımaz; bu yüzden ilk örneği bir sahne biriminin 2 m içinde olan, birim varlığı olmayan bir kara
izi o birimdir: sınıfı `Vehicle`, türü `train`, tipi `tram`, `locomotive` ya da `wagon`, takımı yoktur;
sahnenin ölü yerleştirdiği bir birim (yanmış tramvaylar gibi) ilk satırından itibaren bir enkazdır
(`alive` 0). Oyunun onlar için İngilizce adı yoktur; `VehicleName`, kimliğin sözcüklere ayrılmış hali
("Railway tram A")dır. Konumları titreşmez: neredeyse hiçbiri hiç hareket etmez (her örnek bitine kadar
aynıdır). Tekrar onları yaklaşık on saniyede bir gönderir, bu yüzden örneklerinden yalnızca onları hareket
ettirenler (0,05 m ya da 0,1 derece) tutulur ve 10 saniyede bir tane (`selfCheck.sceneUnits` bırakılan
örnekleri sayar). Önceden bunlar, araçsız `uid 8` adlı izler olarak tutuluyordu.

---

[3DHeat](https://github.com/Holdi601/3DHeat) parçası ([belgeler](https://holdi601.github.io/3DHeat/)). Kaynak: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
