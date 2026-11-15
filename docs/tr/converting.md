---
title: "Tekrarları çevirme"
nav_order: 4
lang: tr
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Tekrarları çevirme {#converting-replays}

Çıktı varsayılan olarak her savaş için bir `.3dheat` dosyası, `--loose` ile ise ayrı dosyalardır.

## Adım adım {#step-by-step}

1. **Tekrar kaydını açın.** War Thunder, oyunun seçeneklerinde tekrar kaydı açıkken istemci
   tekrarlarını oyunun `Replays` klasörüne kaydeder, örneğin
   `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   Oyunun tekrar sayfasından kaydedilen sunucu tekrarı (`0000.wrpl`, `0001.wrpl`, ... içeren
   bir zip) da çevrilebilir.
2. **Bir terminal açın.** Sonuçların yazılabileceği bir klasörde olun
   ([Başlamadan önce](before-you-start.md)).
3. **Çevirin:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # dosyalar, klasörler ya da ikisi
   heat3d-wt-replay battle.zip -o out              # bir sunucu tekrarının zip'i
   heat3d-wt-replay a.wrpl -o out --loose          # tek .3dheat yerine ayrı dosyalar
   ```

   `out`, terminalinizin bulunduğu klasörde oluşturulur.
4. **Ne dediğini okuyun.** Her savaş için bir satır görmelisiniz.
5. **Açın:** `out/<map>/<match>.3dheat` dosyasını 3DHeat görüntüleyicisine yükleyin
   ([Yükleme](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![Sentetik bir tekrar üzerinde çalıştırma: bir .3dheat, --loose, bozuk bir dosya, boş bir klasör](../assets/img/convert.svg)

Resim, testlerin kodda ürettiği bir tekrar üzerinde yapılan çalıştırmadır (gerçek tekrar ve
kurulum yok):

- `ok <file>`: bir savaş çevrildi (`--loose` ile: `ok <table> <match document>`);
- `failed <file>: <why>`: okunamayan bir dosya (çıkış durumu 1; diğerleri yine çevrilir);
- `no .wrpl files given`: çevrilecek bir şey yok (çıkış durumu 2);
- `note: ...`: örneğin araçları adlandırmak için bir War Thunder kurulumu bulunamadığı.

## Seçenekler {#options}

| Seçenek | Varsayılan | Ne yapar |
|---|---|---|
| `replays` (bir ya da daha fazla) | - | `.wrpl` dosyaları, bunların klasörleri (klasörün kendisi, alt klasörleri değil) ya da zipleri (sunucu tekrarı: `.wrpl` parçaları geçici bir klasöre açılır) |
| `-o`, `--out` | zorunlu | nereye yazılacağı: içinde her harita için bir klasör |
| `--game FOLDER` | bulunur | araçları, silahları ve mühimmatı adlandıran War Thunder klasörü; tabloları [ekonomiyi](economy.md) fiyatlandırır; ayrıca `HEAT3D_WT_GAME` |
| `--no-smoothing` | kapalı | diğer birimlerin ölü hesaplamalı ve alınmış örneklerini tekrarda olduğu gibi tutar ([Ölü hesaplama](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | açık | her savaşı tek bir `.3dheat` dosyasına paketler |
| `--loose` | kapalı | her savaşı ayrı dosyalar olarak tutar (tablo, maç belgesi, yan dosyalar) |
| `--version` | - | `heat3d-wt-replay <version>` yazar ve durur |
| `-h`, `--help` | - | seçenekleri yazar ve durur |

Bir savaş yeniden çevrilirse yeniden yazılır. Program seçenekleri nasıl yazdırıyorsa:
[Komut başvurusu](../cli-reference.md).

## Hangi dosyalar bir savaştır {#which-files-are-one-battle}

Her savaş bir dosya olur:
`out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat`. AB, RB ve SB oyunun
arcade, realistic ve simulator savaşları için kullandığı kısa adlardır; `<mode>` oyunun
görevin modunu tuşladığı biçimdir (`Conq4` Conquest #4, `Dom` Domination, `Bttl` Battle; bkz.
[Savaş modu](ground.md#battle-mode)); tekrar hiçbirini adlandırmıyorsa iki kısım da atlanır.
Bir sunucu tekrarının parçaları (`0000.wrpl`, `0001.wrpl`, ...) birlikte tek bir savaş olarak
okunur; aynı savaşın istemci tekrarı ve sunucu parçaları ise iki kayıttır ve iki olarak kalır.

## Çıkış durumu {#exit-status}

Her savaş çevrildiyse `0`, herhangi biri başarısız olduysa `1` (diğerleri yine çevrilir),
argümanlar arasında hiç tekrar dosyası bulunamadıysa `2`.

---

[3DHeat](https://github.com/Holdi601/3DHeat) parçası ([belgeler](https://holdi601.github.io/3DHeat/)). Kaynak: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
