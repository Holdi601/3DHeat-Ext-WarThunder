---
title: "Koşullar ve lisans"
nav_order: 16
lang: "tr"
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# Koşullar ve lisans {#terms-and-licence}

## Koşullar {#the-terms}

Gaijin'in Hizmet Koşulları (2026-08-17 güncellemesi), EULA (Ek 2):
3.2.2 "modify, translate, create derivative works of, reverse engineer,
disassemble, or decompile the Game(s)", 3.2.9 "mine or collect any data from
the Game(s) that is not intended to be publicly displayed"; 1.2 "are not
permitted to store, download, modify, or otherwise use any part of the Game(s)"
istemcinin ötesinde. Kendi kopyanızın seviye dosyalarını yerel bir 3B görünüme okumak
kullanıcının bunu bilerek verdiği bir karardır. Yazılan seviyeler makinenizde kalır:
**bunları asla yayımlamayın** ve burada hiçbir oyun verisi dağıtılmaz.

## Kaynaklar {#sources}

Buradaki tüm kod bu proje için yazılmıştır; başka bir ayrıştırıcıdan kod kopyalanmamıştır. Biçim
hakkında bildikleri şu kaynaklardan gelir:

- Gaijin'in Dagor Engine kaynağı (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause): varlık akışı için `prog/engine/daECS/net/network.cpp`, `connection.cpp`,
  `object.cpp`, `serialize.cpp`, `compression.h` ve `prog/engine/daECS/core/baseIo.cpp`,
  `componentTypes.cpp` (`ecs.py`), ve varlık iletilerinin sınıf numaralarını nasıl verdiği için
  `net/message.cpp` (`MessageClass::initImpl`). Bileşen ve tür adları, oyunun kendi
  arşivlerindeki sözcüklerle FNV-1a karmalarıyla eşleştirilir; `ecs.py` bulunan adları listeler.
- Aynı kaynağın `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp` ve
  `daNet/bitStream.h` dosyaları: bir iletinin hangi nesne için olduğunu nasıl adlandırdığı
  (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT): `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`,
  `docs/REPLAY-DECODE-ECS.md`, `docs/QUICK-REF.md` ve kendi ayrıştırıcısı
  `web/wrpl-parse.js`; uçuş modelinin, yer senkronizasyonunun, uçuştaki silahların, kimlik alanı
  iletilerinin, oyuncu yuvalarının, kokpit değerlerinin ve ikili blk'nin bit düzenleri için okundu.
  WTACRP kendi referansları olarak maxsupermanhd/wrpl-inspector, wt_blk ve wrpl-acmi (AGPL-3.0)
  adlarını verir; onların kodu burada okunmadı.
- Yazarın kendi tekrarları, dosya olarak okunarak: 2025 farkları (uçuş modelinin eski düzeni,
  bayrak baytı olmayan sohbet, zlib), yer tutumu, paketlenmiş yükseklik ofseti, silahların bırakma
  noktaları ve kokpit göstergeleri bunlar üzerinde burada çıkarıldı.

## Testler {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<folder with the sample replays> python -m pytest -q   # ayrıca herkese açık 2025 örnek tekrarlarını denetler
HEAT3D_WT_REPLAYS=<folder of your own replays> python -m pytest -q        # adımlar, kimlikler, AI bayrakları, roll işareti, yumuşatıcı, adlar
```

Birim testleri hiçbir zaman bir kurulumu okumaz (`HEAT3D_WT_NO_NAMES` ayarlanır); kendi
tekrarlarınızla yapılan test adları kurulumunuzdan okur.

Testler tekrarları kodda üretir (`tests/synth.py`: başlık, paketler, sonuçlar, varlık akışı,
uçuştaki silahlar), okuyucuların belgelediği düzende; depoda hiçbir tekrar yoktur.

## Lisans {#licence}

MIT - bkz. [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Kullanılan
kitaplıklar: pyarrow (Apache-2.0), numpy (BSD-3-Clause), zstandard (BSD-3-Clause) ve Pillow
(MIT-CMU). Seviye okuyucuları Dagor Engine kaynağından yazılmıştır, Telif (c) 2023 Gaijin
Entertainment, BSD 3-Clause lisansı; ondan hiçbir kod kopyalanmamıştır ve kullanılan biçim
sabitleri (vromfs XOR anahtarı, yükseklik aralığı ızgara ofsetleri) göründükleri yerde gösterilir.

---

[3DHeat](https://github.com/Holdi601/3DHeat) parçası ([belgeler](https://holdi601.github.io/3DHeat/)). Kaynak: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
