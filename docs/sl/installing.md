---
title: Namestitev
nav_order: 3
lang: sl
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Namestitev {#installing}

Ste novi v ukazni vrstici? Najprej preberite [Preden začnete](before-you-start.md).
Potrebujete Python 3.10 ali novejši; pyarrow, numpy, zstandard in Pillow se namestijo
skupaj z njim.

## Korak za korakom {#step-by-step}

1. Pridobite kodo: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   ali prenesite zip iz [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   in ga razpakirajte.
2. Odprite ukazno vrstico v tej mapi in vpišite `pip install -e .`. Namestitev doda dva
   ukaza: `heat3d-wt-replay` (posnetki) in `heat3d-wt-level` (zemljevidi).
3. Preverite: `heat3d-wt-replay --version`. Videti bi morali
   `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` izpiše možnosti:

![heat3d-wt-replay --help](../assets/img/help.svg)

Brez namestitve: `python -m heat3d_ext_warthunder ...` in
`python -m heat3d_ext_warthunder.levelcli ...` v mapi orodja.

## Imena iz vaše namestitve {#names-from-your-install}

Vozila, orožja in streliva dobijo angleška imena iz besedilnih datotek same igre, ki se
preberejo iz vaše namestitve med pretvorbo. Namestitev se najde prek Steam ali privzetih
map zaganjalnika; sicer povesta `--game <mapa>` ali spremenljivka okolja `HEAT3D_WT_GAME`,
kje je. Nobeno besedilo igre ni v tem repozitoriju; brez namestitve so imena kar
identifikatorji vozil (pretvornik to pove v vrstici `note:`).

## Posodobitve {#updates}

Vsak zagon najprej preveri GitHub izdaje projekta (največ en zahtevek vsaki nekaj ur; nikoli
ne ustavi pretvorbe, ne glede na to, ali ste na spletu). Ko je na voljo novejša izdaja, ukaz
pred namestitvijo vpraša: `git clone` se posodobi z `git pull --ff-only` (zavrnjeno, dokler
imate lokalne spremembe), prenesena kopija pa iz arhiva izdaje. `HEAT3D_NO_UPDATE=1`
izklopi preverjanje in posodabljanje.

---

Del [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Vir: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
