---
title: Uzstādīšana
nav_order: 3
lang: lv
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Uzstādīšana {#installing}

Jauns komandrindā? Vispirms izlasiet [Pirms sākat](before-you-start.md).
Nepieciešams Python 3.10 vai jaunāks; pyarrow, numpy, zstandard un Pillow tiek
uzstādīti kopā ar to.

## Soli pa solim {#step-by-step}

1. Iegūstiet kodu: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   vai lejupielādējiet zip failu no [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   un izpakojiet to.
2. Atveriet termināli šajā mapē un ierakstiet `pip install -e .`. Tiek uzstādītas divas
   komandas: `heat3d-wt-replay` (atkārtojumi) un `heat3d-wt-level` (līmeņi).
3. Pārbaudiet: `heat3d-wt-replay --version`. Vajadzētu redzēt
   `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` parāda iespējas:

![heat3d-wt-replay --help](../assets/img/help.svg)

Bez uzstādīšanas: `python -m heat3d_ext_warthunder ...` un
`python -m heat3d_ext_warthunder.levelcli ...` rīka mapē.

## Nosaukumi no jūsu instalācijas {#names-from-your-install}

Transportlīdzekļi, ieroči un munīcija saņem angļu nosaukumus no spēles pašas
teksta failiem, ko konvertēšanas laikā nolasa no jūsu instalācijas. Instalāciju
atrod caur Steam vai launcher noklusētajām mapēm; `--game <mape>` vai vides
mainīgais `HEAT3D_WT_GAME` norāda, kur tā atrodas citādi. Šajā repozitorijā nav
nekāda spēles teksta; bez instalācijas nosaukumi ir transportlīdzekļu ID
(konvertētājs to parāda rindā `note:`).

## Atjauninājumi {#updates}

Katrs starts vispirms pārbauda projekta GitHub izlaidumus (ne vairāk kā vienu
pieprasījumu ik pēc dažām stundām; tas nekad nepārtrauc konvertēšanu, ar
internetu vai bez tā). Kad ir jaunāks izlaidums, komanda pirms uzstādīšanas
jautā: `git clone` kopiju atjauno ar `git pull --ff-only` (atsakās, ja ir vietējas
izmaiņas), lejupielādētu kopiju — no izlaiduma arhīva. `HEAT3D_NO_UPDATE=1`
izslēdz pārbaudi un atjaunināšanu.

---

Daļa no [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentācija](https://holdi601.github.io/3DHeat/)). Avots: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
