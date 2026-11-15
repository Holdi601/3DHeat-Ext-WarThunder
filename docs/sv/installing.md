---
title: "Installera"
nav_order: 3
lang: "sv"
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Installera {#installing}

Ny i kommandoraden? Läs [Innan du börjar](before-you-start.md) först.
Kräver Python 3.10 eller senare; pyarrow, numpy, zstandard och Pillow installeras
tillsammans med det.

## Steg för steg {#step-by-step}

1. Hämta koden: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   eller ladda ner en zip-fil från [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   och packa upp den.
2. Öppna en terminal i mappen och skriv `pip install -e .`. Det installerar
   två kommandon: `heat3d-wt-replay` (repriser) och `heat3d-wt-level` (nivåer).
3. Kontrollera det: `heat3d-wt-replay --version`. Du bör se
   `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` listar alternativen:

![heat3d-wt-replay --help](../assets/img/help.svg)

Utan installation: `python -m heat3d_ext_warthunder ...` och
`python -m heat3d_ext_warthunder.levelcli ...` i verktygets mapp.

## Namn från din installation {#names-from-your-install}

Fordon, vapen och ammunition får sina engelska namn från spelets egna textfiler,
lästa från din installation vid konvertering. Installationen hittas via Steam
eller startprogrammets standardmappar; `--game <mapp>` eller miljövariabeln
`HEAT3D_WT_GAME` anger var den finns annars. Ingen av spelets text finns i
det här arkivet; utan installation är namnen fordonens id:n (konverteraren säger
det på en `note:`-rad).

## Uppdateringar {#updates}

Varje start kontrollerar först projektets GitHub-releaser (högst en förfrågan
var några timmar; det stoppar aldrig en konvertering, online eller inte). När en
nyare release finns frågar kommandot innan den installeras: en `git clone`
uppdateras med `git pull --ff-only` (vägras om du har lokala ändringar), en
nedladdad kopia från releasens arkiv. `HEAT3D_NO_UPDATE=1` stänger av kontrollen
och uppdateringen.

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Källa: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
