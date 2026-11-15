---
title: Instalare
nav_order: 3
lang: "ro"
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Instalare {#installing}

Sunteți nou cu linia de comandă? Citiți mai întâi [Înainte de început](before-you-start.md).
Are nevoie de Python 3.10 sau mai nou; pyarrow, numpy, zstandard și Pillow se instalează odată cu el.

## Pas cu pas {#step-by-step}

1. Luați codul: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   sau descărcați un zip din [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   și dezarhivați-l.
2. Deschideți un terminal în acel folder și scrieți `pip install -e .`. Aceasta instalează
   două comenzi: `heat3d-wt-replay` (replay-uri) și `heat3d-wt-level` (niveluri).
3. Verificați: `heat3d-wt-replay --version`. Ar trebui să vedeți
   `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` listează opțiunile:

![heat3d-wt-replay --help](../assets/img/help.svg)

Fără instalare: `python -m heat3d_ext_warthunder ...` și
`python -m heat3d_ext_warthunder.levelcli ...` în folderul instrumentului.

## Nume din instalarea dumneavoastră {#names-from-your-install}

Vehiculele, armele și muniția primesc numele lor în engleză din fișierele de text ale jocului,
citite din instalarea dumneavoastră la conversie. Instalarea este găsită prin Steam sau prin
folderele implicite ale launcher-ului; `--game <folder>` sau variabila de mediu
`HEAT3D_WT_GAME` arată unde se află altfel. Niciun text al jocului nu este în acest depozit; fără o
instalare, numele sunt id-urile vehiculelor (convertorul spune asta într-o linie `note:`).

## Actualizări {#updates}

Fiecare pornire verifică mai întâi versiunile publicate ale proiectului pe GitHub (cel mult o cerere
la câteva ore; nu oprește niciodată o conversie, fie că sunteți online, fie că nu). Când apare o versiune mai nouă,
comanda întreabă înainte de a o instala: un `git clone` se actualizează cu `git pull --ff-only` (refuzat cât timp aveți
modificări locale), o copie descărcată din arhiva versiunii. `HEAT3D_NO_UPDATE=1` oprește
verificarea și actualizarea.

---

Parte din [3DHeat](https://github.com/Holdi601/3DHeat) ([documentație](https://holdi601.github.io/3DHeat/)). Sursă: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
