---
title: "Inštalácia"
nav_order: 3
lang: "sk"
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Inštalácia {#installing}

Ste noví v príkazovom riadku? Najskôr si prečítajte [Než začnete](before-you-start.md).
Potrebujete Python 3.10 alebo novší; pyarrow, numpy, zstandard a Pillow sa
nainštalujú spolu s ním.

## Krok za krokom {#step-by-step}

1. Získajte kód: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   alebo stiahnite zip z [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   a rozbaľte ho.
2. Otvorte terminál v tomto priečinku a napíšte `pip install -e .`. Nainštalujú sa
   dva príkazy: `heat3d-wt-replay` (replaye) a `heat3d-wt-level` (levely).
3. Skontrolujte to: `heat3d-wt-replay --version`. Mali by ste vidieť
   `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` vypíše možnosti:

![heat3d-wt-replay --help](../assets/img/help.svg)

Bez inštalácie: `python -m heat3d_ext_warthunder ...` a
`python -m heat3d_ext_warthunder.levelcli ...` v priečinku nástroja.

## Názvy z vašej inštalácie {#names-from-your-install}

Vozidlá, zbrane a munícia dostanú anglické názvy z textových súborov samotnej hry,
ktoré sa pri konverzii čítajú z vašej inštalácie. Inštalácia sa hľadá cez Steam
alebo predvolené priečinky spúšťača; inak to povie `--game <priečinok>` alebo
premenná prostredia `HEAT3D_WT_GAME`. Žiadny text hry nie je v tomto repozitári;
bez inštalácie sú názvy identifikátory vozidiel (konverzor to oznámi riadkom `note:`).

## Aktualizácie {#updates}

Každé spustenie najskôr skontroluje GitHub releases projektu (najviac jedna
požiadavka každých pár hodín; konverziu nikdy nezastaví, či ste online alebo
nie). Keď je vydaná novšia verzia, príkaz sa pred inštaláciou opýta: `git clone`
sa aktualizuje cez `git pull --ff-only` (odmietne sa, ak máte lokálne zmeny),
stiahnutá kópia z archívu vydania. `HEAT3D_NO_UPDATE=1` kontrolu aj aktualizáciu vypne.

---

Súčasť [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentácia](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
