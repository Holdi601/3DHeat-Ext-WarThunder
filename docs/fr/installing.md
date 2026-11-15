---
title: Installation
nav_order: 3
lang: "fr"
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Installation {#installing}

Vous ne connaissez pas la ligne de commande ? Lisez d'abord [Avant de commencer](before-you-start.md).
Il faut Python 3.10 ou plus récent ; pyarrow, numpy, zstandard et Pillow sont installés avec lui.

## Étape par étape {#step-by-step}

1. Récupérez le code : `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`,
   ou téléchargez un zip depuis [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases)
   et décompressez-le.
2. Ouvrez un terminal dans ce dossier et tapez `pip install -e .`. Cela installe deux
   commandes : `heat3d-wt-replay` (replays) et `heat3d-wt-level` (niveaux).
3. Vérifiez : `heat3d-wt-replay --version`. Vous devez voir
   `heat3d-wt-replay 0.2.0`. `heat3d-wt-replay --help` liste les options :

![heat3d-wt-replay --help](../assets/img/help.svg)

Sans installation : `python -m heat3d_ext_warthunder ...` et
`python -m heat3d_ext_warthunder.levelcli ...` dans le dossier de l'outil.

## Noms tirés de votre installation {#names-from-your-install}

Les véhicules, armes et munitions reçoivent leurs noms anglais depuis les fichiers de texte du
jeu lui-même, lus dans votre installation pendant la conversion. L'installation est trouvée
grâce à Steam ou aux dossiers par défaut du lanceur ; `--game <dossier>` ou la variable
d'environnement `HEAT3D_WT_GAME` indiquent où elle se trouve sinon. Aucun texte du jeu ne se
trouve dans ce dépôt ; sans installation, les noms sont les identifiants des véhicules (le
convertisseur le signale par une ligne `note:`).

## Mises à jour {#updates}

Chaque démarrage consulte d'abord les versions publiées du projet sur GitHub (au plus une
requête toutes les quelques heures ; cela n'arrête jamais une conversion, en ligne ou non).
Lorsqu'une version plus récente est disponible, la commande demande avant de l'installer : un
`git clone` est mis à jour avec `git pull --ff-only` (refusé tant que vous avez des modifications
locales), une copie téléchargée depuis l'archive de la version. `HEAT3D_NO_UPDATE=1` désactive
la vérification et la mise à jour.

---

Une partie de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source : [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
