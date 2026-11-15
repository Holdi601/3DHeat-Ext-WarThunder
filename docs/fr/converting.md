---
title: Convertir les replays
nav_order: 4
lang: "fr"
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Convertir les replays {#converting-replays}

Résultat : un fichier `.3dheat` par bataille (par défaut), ou des fichiers séparés avec
`--loose`.

## Étape par étape {#step-by-step}

1. **Activer les replays.** War Thunder enregistre les replays client dans le dossier
   `Replays` du jeu, lorsque l'enregistrement des replays est activé dans ses options.
   Par exemple : `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   Un replay serveur, sauvegardé depuis la page des replays du jeu (un zip contenant
   `0000.wrpl`, `0001.wrpl`, ...), peut aussi être converti.
2. **Ouvrir un terminal** dans un dossier où les résultats peuvent être écrits
   ([Avant de commencer](before-you-start.md)).
3. **Convertir :**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # fichiers, dossiers, ou les deux
   heat3d-wt-replay battle.zip -o out              # le zip d'un replay serveur
   heat3d-wt-replay a.wrpl -o out --loose          # fichiers séparés au lieu d'un seul .3dheat
   ```

   `out` est créé dans le dossier où se trouve votre terminal.
4. **Lire ce que la commande affiche.** Vous devez voir une ligne par bataille.
5. **Ouvrir le résultat :** chargez `out/<map>/<match>.3dheat` dans la visionneuse 3DHeat
   ([Charger un fichier](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![Un essai sur un replay synthétique : un .3dheat, --loose, un fichier cassé, un dossier vide](../assets/img/convert.svg)

L'image montre un essai sur un replay que les tests construisent dans le code (aucun vrai
replay, aucune installation nécessaire) :

- `ok <file>` : une bataille convertie (avec `--loose` : `ok <table> <match document>`) ;
- `failed <file>: <why>` : un fichier qui n'a pas pu être lu (code de sortie 1 ; les
  autres sont tout de même convertis) ;
- `no .wrpl files given` : rien à convertir (code de sortie 2) ;
- `note: ...` : par exemple qu'aucune installation de War Thunder n'a été trouvée pour
  nommer les véhicules.

## Options {#options}

| Option | Par défaut | Rôle |
|---|---|---|
| `replays` (un ou plusieurs) | - | fichiers `.wrpl`, dossiers qui en contiennent (le dossier lui-même, pas ses sous-dossiers), ou zips de ceux-ci (un replay serveur : ses parties `.wrpl` sont décompressées dans un dossier temporaire) |
| `-o`, `--out` | obligatoire | où écrire : un dossier par carte, à l'intérieur |
| `--game FOLDER` | trouvé | le dossier de War Thunder dont les textes donnent les noms des véhicules, des armes et des munitions, et dont les tables donnent le prix de l'[économie](economy.md) ; aussi `HEAT3D_WT_GAME` |
| `--no-smoothing` | désactivé | garder les échantillons recalculés et reçus des autres unités tels que le replay les contient ([Recalcul de position](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | activé | regrouper chaque bataille dans un seul fichier `.3dheat` |
| `--loose` | désactivé | garder chaque bataille en fichiers séparés (table, document de match, fichiers annexes) |
| `--version` | - | afficher `heat3d-wt-replay <version>` et s'arrêter |
| `-h`, `--help` | - | afficher les options et s'arrêter |

Une bataille convertie à nouveau est réécrite. Les options telles que le programme les
affiche : [Référence des commandes](../cli-reference.md).

## Quels fichiers forment une bataille {#which-files-are-one-battle}

Chaque bataille devient un fichier
`out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat`. AB, RB et SB sont les
abréviations du jeu pour les batailles arcade, réalistes et simulateur ; `<mode>` est le
mode de la mission tel que le jeu le désigne (`Conq4` Conquest n° 4, `Dom` Domination,
`Bttl` Battle ; voir [Mode de bataille](ground.md#battle-mode)). L'un des deux éléments est omis
lorsque le replay n'en indique aucun. Les parties d'un replay serveur (`0000.wrpl`,
`0001.wrpl`, ...) sont lues ensemble comme une seule bataille ; un replay client et les
parties du serveur pour la même bataille sont deux enregistrements et restent deux.

## Code de sortie {#exit-status}

`0` quand toutes les batailles ont été converties, `1` quand l'une d'elles a échoué (les
autres sont tout de même converties), `2` quand aucun fichier de replay n'a été trouvé
parmi les arguments.

---

Une partie de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source : [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
