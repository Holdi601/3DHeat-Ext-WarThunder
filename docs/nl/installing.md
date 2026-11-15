---
title: "Installeren"
nav_order: 3
lang: "nl"
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Installeren {#installing}

Nieuw met de opdrachtregel? Lees eerst [Voordat je begint](before-you-start.md).
Je hebt Python 3.10 of nieuwer nodig; pyarrow, numpy, zstandard en Pillow worden
er automatisch bij geïnstalleerd.

## Stap voor stap {#step-by-step}

1. Haal de code op: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   of download een zip-bestand via [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   en pak het uit.
2. Open een terminal in die map en typ `pip install -e .`. Dit installeert
   twee commando's: `heat3d-wt-replay` (replays) en `heat3d-wt-level` (levels).
3. Controleer het: `heat3d-wt-replay --version`. Je ziet
   `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` laat de opties zien:

![heat3d-wt-replay --help](../assets/img/help.svg)

Zonder installeren: `python -m heat3d_ext_warthunder ...` en
`python -m heat3d_ext_warthunder.levelcli ...` in de map van de tool.

## Namen uit je installatie {#names-from-your-install}

Voertuigen, wapens en munitie krijgen hun Engelse namen uit de tekstbestanden van het
spel zelf, die bij het omzetten uit je installatie gelezen worden. De installatie
wordt gevonden via Steam of de standaardmappen van de launcher; `--game <map>` of de
omgevingsvariabele `HEAT3D_WT_GAME` geven anders aan waar die staat. Er staat geen
enkele tekst van het spel in deze repository; zonder installatie zijn de namen de
voertuig-id's (de converter meldt dat in een `note:`-regel).

## Updates {#updates}

Bij elke start wordt eerst de GitHub-release van het project gecontroleerd (hooguit
één verzoek per paar uur; het stopt nooit een omzetting, online of offline). Is er een
nieuwere release, dan vraagt de opdracht eerst of hij die mag installeren: een
`git clone` wordt bijgewerkt met `git pull --ff-only` (geweigerd zolang je lokale
wijzigingen hebt), een gedownloade kopie uit het archief van de release.
`HEAT3D_NO_UPDATE=1` zet de controle en de update uit.

---

Onderdeel van [3DHeat](https://github.com/Holdi601/3DHeat) ([documentatie](https://holdi601.github.io/3DHeat/)). Bron: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
