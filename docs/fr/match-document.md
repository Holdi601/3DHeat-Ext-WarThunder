---
title: Le document de match
nav_order: 7
lang: fr
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# Le document de match {#the-match-document}

![Le début d'un document de match synthétique, et ses clés](../assets/img/match-document.svg)

`<match>.match.json` contient tout ce que dit le replay et qui n'est pas une ligne de la table.
L'onglet Match de la visionneuse le lit.

## La bataille {#the-battle}

| Clé | Contenu |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | l'identifiant du match (comme dans le nom du fichier) ; l'identifiant de la carte ; le fichier de niveau qu'elle utilise |
| `mission`, `missionKey` | le nom de la mission et sa clé dans les fichiers de texte du jeu |
| `battleClass`, `environment`, `weather` | tels que donnés par l'en-tête |
| `sessionId`, `server` | l'identifiant de session de la bataille ; le serveur |
| `replayVersion`, `flightLayout` | la version du format du replay ; la disposition des paquets de vol lue (`2025` ou `2026`) |
| `files` | les fichiers de replay lus (un seul, ou les parties d'un replay serveur) |
| `started`, `timePlayed`, `replayEnd` | heure de début (ISO, UTC) ; secondes jouées, d'après les résultats ; secondes du dernier paquet du replay |
| `author`, `authorUserId` | le joueur qui enregistre et son identifiant Gaijin (replays client) |
| `teams` | les équipes de la bataille (`1`, `2`) |
| `result` | `winner`, `status` (`success` ou `fail`, l'issue de l'auteur), `authorTeam`, `teams` ([Économie](economy.md)) |
| `vehicleNames` | d'où viennent les noms des véhicules (votre installation) et leur langue |
| `conventions` | les unités et les signes de la table : axes, temps, vie, trajectoire, vivant, roulis, et plus |

## Tout le reste {#everything-else}

| Clé | Contenu |
|---|---|
| `battle`, `difficulty`, `gameMode` | le mode de bataille : `difficulty` `AB` / `RB` / `SB` (et son nom, et l'octet de l'en-tête), `gameMode` `ground` / `air` / `naval`, le mode de la mission (`Dom`, `Conq`, `Bttl`, `I2M`, ...) et son nom anglais d'après votre installation (`Domination`, `Enduring Confrontation`), les types d'unités autorisés (voir [Mode de bataille](ground.md#battle-mode)) |
| `settings` | le blk de la mission après l'en-tête : mode, environnement, météo, limites de score et de temps, pays, types d'unités autorisés, vent, et `stars` (latitude, longitude, date, heure locale) |
| `sky` | le premier `CustomWeatherParams` : direction du soleil et de la lune, vent, couleurs du ciel, décalages des nuages |
| `players`, `slots` | la ligne des résultats par joueur (frags, frags au sol, morts, assistances, score, captures, escadron, clan, pays, composition, les uid qu'ils ont conduits) ; les emplacements de joueurs du replay (nom, identifiant d'utilisateur, équipe) |
| `units` | chaque entité d'unité que le replay a créée : eid, uid, modèle, véhicule, genre, type, équipe, joueur, nom de mission, moment de sa création et de sa suppression, lieu de sa création, quels composants n'ont pas pu être lus |
| `objects` | les objets nommés de la mission : zones de capture et aérodromes avec leur position et leur taille, contours des aérodromes sous forme de points, zones d'apparition |
| `objectives` | les objectifs de la bataille, chacun avec son `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (1 ou 2 du replay, vide pour les deux), `name` (pour une zone de capture sa lettre, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) avec `position`, `radius` / `height` / `size` et `heading`, `source` (`replay` ou `mission`) et ce qui est encore connu (voir [Objectifs](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | avec les noms et les véhicules des deux camps ; les frags avec le nom anglais de l'arme |
| `weapons` | chaque roquette, missile, bombe, torpille, réservoir largable et charge larguée : quand, où elle a été lâchée (position, attitude, vitesse), par quelle unité (la plus proche dans 300 m et 1,5 s), combien d'échantillons de vol, où elle a été vue en dernier, quand elle a été retirée |
| `explosions`, `flak` | `PlayExplosionVisual` (position, direction, genre) et `PlayFlakExplosionVisual` (position) |
| `awards` | les récompenses du joueur qui enregistre (`TextStreak` : first_blood, séries, compteurs de défis) |
| `detections`, `unitStates` | paires `UnitDetected` d'unités ; un message (0xF093) avec la position, l'attitude et la vitesse d'une unité, dont le sens n'est pas connu |
| `authorInstruments` | les valeurs du cockpit du joueur qui enregistre (`ReplayCockpitParams`) par numéro d'instrument, au plus une par seconde ; `known` nomme chaque numéro que ce replay a envoyé (nom, unité, comment il a été vérifié), `notNamed` le reste |
| `scoreboard` | les statistiques de chaque joueur à chaque changement (frags, morts, assistances, score, frags d'IA, frags navals, zones, dégâts, esquives de missiles, escadron), et le score de chaque équipe ainsi que ses tickets probables au fil du temps (voir [Données de réflexion](aircraft.md#reflection-data)) |
| `economy` | les Lions d'argent et points de recherche de la bataille (voir [Économie](economy.md)) : totaux, par joueur, par véhicule, les multiplicateurs, le vainqueur, les contrôles |
| `entityMessages` | les messages d'entité (0x20) par numéro de classe : nombre, modèles visés, tailles |
| `chat` | chaque ligne du chat |
| `triggers`, `hints`, `missionProgress` | les actions du script de mission (RunTriggerAction), ses indications, ses messages de progression |
| `camera` | les champs de la caméra de replay du joueur qui enregistre toutes les 0,25 s, tels qu'envoyés (la table en a une trajectoire) |
| `projectileHitReplays` | les impacts portés et subis par le joueur qui enregistre, avec l'arme et la munition et leurs noms anglais |
| `results` | le blk des résultats entier, tel que le jeu l'a écrit |
| `counts` | lignes, événements, vies, genres, échantillons, entités par modèle, armes, paquets lus et non lus, chaque identifiant de message vu et ceux non lus, échantillons écartés |
| `trackBreaks` | chaque coupure d'une trajectoire pour un pas plus rapide que l'unité ne peut aller : où, de combien, à quelle vitesse, et ce qu'elle est le plus probablement |
| `selfCheck` | les contrôles listés dans [Comment le replay est lu](how-it-reads.md), calculés à chaque conversion ; `stepSpeed` donne par genre la vitesse entre les lignes consécutives d'une trajectoire telle que la visionneuse les relie (médiane, 99e centile, la plus haute, et les pas plus rapides que possible, qui doivent valoir 0) |

---

Une partie de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source : [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
