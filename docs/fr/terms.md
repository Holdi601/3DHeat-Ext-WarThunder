---
title: Termes et licence
nav_order: 16
lang: fr
source: terms.md
source_hash: "87615c2f7602"
nav_exclude: true
search_exclude: true
---
# Termes et licence {#terms-and-licence}

## Les conditions {#the-terms}

Conditions d'utilisation de Gaijin (mises à jour le 2026-08-17), EULA (annexe 2) :
3.2.2 « modify, translate, create derivative works of, reverse engineer, disassemble, or decompile the
Game(s) », 3.2.9 « mine or collect any data from the Game(s) that is not intended to be publicly
displayed » ; 1.2 « are not permitted to store, download, modify, or otherwise use any part of the
Game(s) » au-delà du client. Charger les fichiers de niveau de votre propre copie du jeu dans une vue 3D
locale est la décision de l'utilisateur, prise en connaissance de cause. Les niveaux écrits restent sur
votre machine : **ne les publiez jamais**, et rien ici ne livre de données du jeu.

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
