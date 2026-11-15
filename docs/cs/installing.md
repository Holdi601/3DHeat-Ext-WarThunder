---
title: "Instalace"
nav_order: 3
lang: "cs"
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Instalace {#installing}

Nikdy jste nepracovali s příkazovým řádkem? Nejdříve si přečtěte [Než začnete](before-you-start.md).
Potřebuje Python 3.10 nebo novější; pyarrow, numpy, zstandard a Pillow se nainstalují spolu s ním.

## Krok za krokem {#step-by-step}

1. Získejte kód: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   nebo stáhněte zip z [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   a rozbalte ho.
2. Otevřete terminál v té složce a napište `pip install -e .`. Nainstalují se dva příkazy:
   `heat3d-wt-replay` (replaye) a `heat3d-wt-level` (úrovně).
3. Ověřte to: `heat3d-wt-replay --version`. Měli byste vidět
   `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` vypíše volby:

![heat3d-wt-replay --help](../assets/img/help.svg)

Bez instalace: `python -m heat3d_ext_warthunder ...` a
`python -m heat3d_ext_warthunder.levelcli ...` ve složce nástroje.

## Názvy z vaší instalace {#names-from-your-install}

Vozidla, zbraně a munice dostanou své anglické názvy z textových souborů hry, které se při převodu čtou z vaší
instalace. Instalace se najde přes Steam nebo výchozí složky spouštěče; jinak řekne, kde je, `--game <folder>` nebo
proměnná prostředí `HEAT3D_WT_GAME`. Žádný text hry není v tomto repozitáři; bez instalace jsou názvy id vozidel
(převodník to oznámí řádkem `note:`).

## Aktualizace {#updates}

Každé spuštění nejdřív zkontroluje GitHub vydání projektu (nejvýš jeden dotaz každých pár hodin; převod nikdy
nezastaví, ať je online, nebo ne). Když je vydána novější verze, příkaz se před instalací zeptá: `git clone` se
aktualizuje příkazem `git pull --ff-only` (odmítne se, pokud máte lokální změny), stažená kopie z archivu vydání.
`HEAT3D_NO_UPDATE=1` kontrolu i aktualizaci vypne.

---

Součást [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentace](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
