---
title: "Kurulum"
nav_order: 3
lang: tr
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Kurulum {#installing}

Komut satırına yeni misiniz? Önce [Başlamadan önce](before-you-start.md) sayfasını okuyun.
Python 3.10 veya daha yeni bir sürüm gerekir; pyarrow, numpy, zstandard ve Pillow onunla
birlikte kurulur.

## Adım adım {#step-by-step}

1. Kodu alın: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`, ya da
   [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases) sayfasından bir zip
   indirip açın.
2. Bu klasörde bir terminal açın ve `pip install -e .` yazın. Bu iki komut kurar:
   `heat3d-wt-replay` (tekrarlar) ve `heat3d-wt-level` (haritalar).
3. Denetleyin: `heat3d-wt-replay --version`. `heat3d-wt-replay 0.2.0` görmelisiniz.
   `heat3d-wt-replay --help` seçenekleri listeler:

![heat3d-wt-replay --help](../assets/img/help.svg)

Kurmadan: aracın klasöründe `python -m heat3d_ext_warthunder ...` ve
`python -m heat3d_ext_warthunder.levelcli ...`.

## Kurulumunuzdan adlar {#names-from-your-install}

Araçların, silahların ve mühimmatın İngilizce adları, dönüştürme sırasında oyunun kendi
metin dosyalarından, kurulumunuzdan okunur. Kurulum Steam ya da başlatıcının varsayılan
klasörlerinde aranır; aksi halde `--game <klasör>` seçeneği ya da `HEAT3D_WT_GAME` ortam
değişkeni yerini söyler. Bu depoda oyunun metninden hiçbir şey yoktur; kurulum yoksa adlar
araç kimlikleri olarak kalır (dönüştürücü bunu bir `note:` satırıyla söyler).

## Güncellemeler {#updates}

Her başlatmada önce projenin GitHub sürümleri denetlenir (en fazla birkaç saatte bir istek;
dönüştürmeyi hiçbir zaman durdurmaz, çevrimiçi ya da çevrimdışı). Yeni bir sürüm çıktığında
komut kurmadan önce sorar: `git clone` ile alınmış kopya `git pull --ff-only` ile güncellenir
(yerel değişiklikleriniz varsa reddedilir), indirilmiş kopya ise sürümün arşivinden. 
`HEAT3D_NO_UPDATE=1` bu denetimi ve güncellemeyi kapatır.

---

[3DHeat](https://github.com/Holdi601/3DHeat) parçası ([belgeler](https://holdi601.github.io/3DHeat/)). Kaynak: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
