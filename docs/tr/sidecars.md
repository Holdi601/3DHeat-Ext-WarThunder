---
title: "Yan dosyalar ve tamlık"
nav_order: 8
lang: tr
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Yan dosyalar ve tamlık {#sidecars-and-completeness}

Tekrarda hiçbir şey atılmaz. Dönüştürücünün okuduğu şeyler tabloya ve maç belgesine girer;
geri kalan her şey üç yan dosyada bütün olarak tutulur, tablonun yanında (`.3dheat`
dosyasının içinde ya da `--loose` ile ayrı). Bu, tüm 3DHeat dönüştürücülerinin ortak
kuralıdır: [Dönüştürücüler her şeyi tutar](https://holdi601.github.io/3DHeat/converters.html).

## Yan dosyalar {#the-sidecars}

- `<match>.messages.parquet`: bir birime giden her ileti (zaman, ileti kimliği ve adı, uid,
  eid, şablon, araç, onaltılık olarak kimlik alanları, `decoded` (okunabilen kısım, JSON
  olarak), yük), her kopyalanmış bileşen değeri (`name` bileşen, `fields` değeri), her varlık
  iletisi (varlığı ve sınıf numarasıyla), her kopyalanmış nesne (`ReflectionData
  <kind>/<index>`, alanları onaltılık olarak) ve burada hiçbir okuyucunun almadığı her paket,
  bütün olarak.
- `<match>.objectives.parquet`: sunucunun gönderdiği her değişiklik için bir satır olmak üzere
  zamana göre ele geçirme bölgeleri: `time`, `event` (`state`, `progress`, `captured`,
  `neutralised`), `zone` (harfi), `zoneId`, `object`, `owner` (0 yok, 1, 2), `progress`
  (-100..100, takım 2 yönünde pozitif), bölgenin `x`, `y`, `z` değerleri ve nesnenin tüm
  `fields` alanları onaltılık olarak (bkz. [Hedefler](objectives.md)).
- `<match>.flight.parquet`: her uçağın her uçuş modeli girdisi bütün olarak (bitleri ve
  `phase`: başladığı ilk baytın biti), hızıyla, 14 kontrol nibble'ı (`control1-3`,
  `throttle`), motorlarıyla ve durumlarıyla, son yakıcısı ve koşuluyla, silah başına mermisiyle
  (`ammo`; `numbers` tüm listedir). Diğer uçakların değerleri son yenilenişlerindeki gibidir.

## Sayıların garanti ettikleri {#what-the-counts-guarantee}

Maç belgesinin `counts` alanı tekrarda ne olduğunu ve ona ne olduğunu söyler:

| Anahtar | Ne |
|---|---|
| `packets`, `unreadPackets` | karşılaşılan her paket türü ve hiçbir okuyucunun almadığı paketler (ileti yan dosyasında bütün olarak tutulur) |
| `messageIds`, `messageIdsNotRead` | karşılaşılan her ileti kimliği ve kaç kez geçtiği; yalnızca tutulan, okunmayanlar |
| `replicatedComponents`, `replicatedNotRead` | okunan bileşen değerleri ve yalnızca tutulanlar |
| `entities`, `entityTemplates`, `entityMessages` | varlık akışının oluşturduğu ve gönderdiği şeyler |
| `droppedSamples` | bilerek dışarıda bırakılan örnekler (varlığı yok olduktan sonra bir kara biriminin enkazı), nedenlerine göre |

Başka hiçbir şey dışarıda bırakılmaz: tekrarın bir öğesi ya tabloya ya da maç belgesine
okunur, ya da bir yan dosyada bütün olarak tutulur. Maç belgesinin `selfCheck` alanı okunanın
denetimlerini tutar ([Tekrarı nasıl okur](how-it-reads.md)).

---

[3DHeat](https://github.com/Holdi601/3DHeat) parçası ([belgeler](https://holdi601.github.io/3DHeat/)). Kaynak: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
