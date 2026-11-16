---
title: Termes et licence
nav_order: 16
lang: "fr"
source: terms.md
source_hash: "01d249aa8f1b"
nav_exclude: true
search_exclude: true
---
# Termes et licence {#terms-and-licence}

## Ce qui est lu {#what-it-reads}

Le convertisseur lit les replays que War Thunder enregistre sur votre ordinateur (ou les replays de vos batailles que vous avez vous-même téléchargés sur warthunder.com) et les fichiers de niveaux de votre propre installation de War Thunder. Rien du jeu n'est inclus ni redistribué ici : aucun asset du jeu, aucun code du jeu, aucune DLL ; Oodle est chargé depuis votre propre installation. Ce qu'il écrit reste sur votre machine : **ne publiez jamais les niveaux**.

3DHeat n'est ni affilié à Gaijin Entertainment ni approuvé par Gaijin Entertainment. War Thunder ainsi que les noms et marques associés appartiennent à leurs propriétaires.

Ayants droit : ouvrez un ticket sur <https://github.com/Holdi601/3DHeat-Ext-WarThunder/issues> - nous répondons rapidement et retirons tout ce qui est demandé.

## Sources {#sources}

Tout le code d'ici a été écrit pour ce projet ; aucun code n'a été copié d'un autre analyseur. Ce qu'il
sait du format vient de :

- Le code source du Dagor Engine de Gaijin (github.com/GaijinEntertainment/DagorEngine,
  BSD 3-Clause) : `prog/engine/daECS/net/network.cpp`, `connection.cpp`, `object.cpp`, `serialize.cpp`,
  `compression.h` et `prog/engine/daECS/core/baseIo.cpp`, `componentTypes.cpp` pour le flux d'entités
  (`ecs.py`), et `net/message.cpp` (`MessageClass::initImpl`) pour la façon dont les messages d'entité
  numérotent leurs classes. Les noms de composants et de types sont rapprochés de leurs empreintes
  FNV-1a à partir des mots des archives du jeu ; `ecs.py` liste les noms trouvés.
- Les fichiers `prog/dagorInclude/daNet/mpi.h`, `prog/engine/daNet/ext/mpi.cpp` et `daNet/bitStream.h` du
  même code source : comment un message nomme l'objet auquel il est destiné (`wrpl.read_mpi`).
- ShioUmiusi/WTACRP (MIT) : `docs/REPLAY-FORMAT.md`, `docs/REPLAY-DECODE.md`, `docs/REPLAY-DECODE-ECS.md`,
  `docs/QUICK-REF.md`, et son propre analyseur `web/wrpl-parse.js`, lus pour les dispositions de bits du
  modèle de vol, de la synchronisation au sol, des armes en vol, des messages à champs d'identifiant, des
  emplacements de joueurs, des valeurs du cockpit et du blk binaire. WTACRP cite maxsupermanhd/wrpl-inspector,
  wt_blk et wrpl-acmi (AGPL-3.0) comme ses propres références ; leur code n'a pas été lu ici.
- Les replays de l'auteur, lus comme des fichiers : les différences de 2025 (l'ancienne disposition du modèle
  de vol, le chat sans octet d'indicateur, zlib), l'attitude au sol, le décalage de hauteur compacté, les points
  de lâcher des armes et les instruments du cockpit ont été établis sur eux ici.

## Tests {#tests}

```bash
python -m pytest -q
HEAT3D_WT_SAMPLES=<dossier avec les replays d'exemple> python -m pytest -q   # vérifie aussi les replays d'exemple publics de 2025
HEAT3D_WT_REPLAYS=<dossier de vos replays> python -m pytest -q        # pas, identités, indicateurs IA, signe du roulis, le lisseur, noms
```

Les tests unitaires ne lisent jamais une installation (`HEAT3D_WT_NO_NAMES` est défini) ; le test avec vos
propres replays lit les noms dans votre installation.

Les tests construisent des replays dans le code (`tests/synth.py` : en-tête, paquets, résultats, flux
d'entités, armes en vol) selon la disposition décrite par les modules de lecture ; aucun replay ne se trouve dans le
dépôt.

## Licence {#licence}

MIT - voir [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WarThunder/blob/main/LICENSE). Utilise pyarrow
(Apache-2.0), numpy (BSD-3-Clause), zstandard (BSD-3-Clause) et Pillow (MIT-CMU). Les modules de lecture des niveaux ont
été écrits à partir du code source du Dagor Engine, Copyright (c) 2023 Gaijin Entertainment, licence BSD
3-Clause ; aucun code de celui-ci n'est copié ici, et les constantes de format utilisées (la clé XOR des
vromfs, les décalages de grille des plages de hauteur) sont citées là où elles apparaissent.

---

Une partie de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source : [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
