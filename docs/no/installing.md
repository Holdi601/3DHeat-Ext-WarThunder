---
title: "Installere"
nav_order: 3
lang: no
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Installere {#installing}

Ny på kommandolinjen? Les [Før du starter](before-you-start.md) først.
Krever Python 3.10 eller nyere; pyarrow, numpy, zstandard og Pillow installeres
sammen med det.

## Steg for steg {#step-by-step}

1. Hent koden: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   eller last ned en zip fra [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   og pakk den ut.
2. Åpne en terminal i den mappen og skriv `pip install -e .`. Dette installerer
   to kommandoer: `heat3d-wt-replay` (replayer) og `heat3d-wt-level` (nivåer).
3. Sjekk det: `heat3d-wt-replay --version`. Du bør se
   `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` lister valgene:

![heat3d-wt-replay --help](../assets/img/help.svg)

Uten å installere: `python -m heat3d_ext_warthunder ...` og
`python -m heat3d_ext_warthunder.levelcli ...` i verktøyets mappe.

## Navn fra installasjonen din {#names-from-your-install}

Kjøretøy, våpen og ammunisjon får sine engelske navn fra spillets egne
tekstfiler, lest fra installasjonen din under konvertering. Installasjonen
finnes gjennom Steam eller startprogrammets standardmapper; `--game <mappe>` eller
miljøvariabelen `HEAT3D_WT_GAME` sier hvor den ligger ellers. Ingen av spillets
tekst ligger i dette depotet; uten installasjon er navnene kjøretøy-ID-ene
(konverteren sier fra om dette i en `note:`-linje).

## Oppdateringer {#updates}

Hver oppstart sjekker først prosjektets GitHub-utgivelser (høyst én forespørsel
hvert par timer; den stopper aldri en konvertering, enten du er på nett eller
ikke). Når en nyere utgivelse finnes, spør kommandoen før den installeres: en
`git clone` oppdateres med `git pull --ff-only` (avvist mens du har lokale
endringer), en nedlastet kopi fra utgivelsens arkiv. `HEAT3D_NO_UPDATE=1` slår
av sjekken og oppdateringen.

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentasjon](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
