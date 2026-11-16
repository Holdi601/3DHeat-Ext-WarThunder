---
title: Objectifs
nav_order: 15
lang: "fr"
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Objectifs {#objectives}

`objectives` dans le document de partie liste ce pour quoi la bataille se joue, à partir de deux sources
(`source`) :

- **Le replay** (`replay`) : les objets de mission que nomme le message 0xD039 (zones de capture
  `cz_circle_NN`, aérodromes, héliports, bases), placés là où les objets répliqués de genre 3 (0xF02D) les
  mettent maintenant - une zone de capture commence à la place de son modèle et est déplacée vers la zone
  de ce mode au départ (`moved`). Les numéros du genre 3 suivent l'ordre de 0xD039 ; chaque objet qui n'est
  pas déplacé se trouve exactement où 0xD039 le place, ce qui vérifie l'ordre. Une zone de capture reçoit la
  forme et le rayon de la zone de mission à sa place (`area`, à 2 m près) et sa lettre à partir de son propre
  index (genre 5, champ 69 : 0 = A) ; l'ordre des lettres est celui du replay, non vérifié par rapport à la
  carte du jeu.
- **La mission** (`mission`) : le fichier de mission `<mission>.blk` de `mis.vromfs.bin` de votre installation
  et les modèles qu'il importe (lecture seule, au moment de la conversion) : ses zones, classées d'après leur
  nom - apparitions (les points numérotés d'une apparition `..._spawnareaNN` forment une seule apparition
  `points`), zones de bataille, cibles de bombardement (`bomb_zone`), points d'apparition de convois
  (`road_NN_spawn`), zones de sortie et de destruction. Les zones d'un autre mode de la même carte (`conq_`,
  `dom_`, `bttl_`, ...) sont laissées de côté, et parmi les variantes `_arcade` / `_realistic` / `_hardcore`,
  celle de la bataille (RB prend `_realistic`, sinon `_hardcore`, comme le font les scripts de mission) ; les
  repères de briefing, les points de canons DCA et les zones de plus de 5 km de large (celles où les
  apparitions sont dispersées) sont aussi laissés de côté. Chaque apparition indique combien de trajectoires
  de joueurs y ont commencé (`used`, `usedByTeam`). Une mission peut échanger ses camps au hasard
  (`randomSpawnTeams`) : lorsque les apparitions montrent les équipes du replay dans l'autre sens, chaque
  `team` est échangée et le camp du nom est conservé comme `missionTeam`. Les itinéraires des convois ne
  figurent pas dans les points de passage des missions tels qu'ils sont lus ; seul l'endroit où apparaissent
  les convois est donné.

Les zones de capture au fil du temps forment le fichier annexe `<match>.objectives.parquet` : les objets
répliqués de genre 5, un par zone - champ 2 son propriétaire (0, 1, 2), champ 67 sa progression de capture,
un octet signé de -100 à 100 (positif vers l'équipe 2), champ 69 son index. Vérifié (`selfCheck.objectives`)
sur les replays serveur au sol des batailles Conquest et Domination : chaque changement de propriétaire
s'accompagne d'un joueur de l'équipe qui capture gagnant une `captureZone` au tableau de bord au même instant
(à 1,5 s près) et d'une unité au sol vivante de cette équipe dans la zone ; les apparitions de chaque bataille
ne montrent les équipes du replay que dans un seul sens (souvent inversé par rapport aux `t1_` / `t2_` de la
mission).

## Unités de scène : tramways et wagons {#scene-units-trams-and-rail-wagons}

Un niveau peut placer des unités à lui : les entités `unit_loader+rail_wagon` d'un replay serveur sont les
tramways du fichier de scène du niveau (`gamedata/scenes/<level>_objects.blk` dans `aces.vromfs.bin` :
`setting__unit_class`, sa transformation et `setting__isDead`). Leurs entités ne portent aucun uid lisible ;
une trajectoire au sol sans entité d'unité dont le premier échantillon se trouve à 2 m près d'une unité de
scène est donc cette unité : sa classe devient `Vehicle`, genre `train`, type `tram`, `locomotive` ou
`wagon`, sans équipe ; une unité que la scène place morte (comme les tramways incendiés) est une épave
(`alive` 0) dès sa première ligne. Le jeu n'a pas de nom anglais pour eux ; `VehicleName` est l'identifiant lu
comme des mots (« Railway tram A »). Leurs positions ne vacillent pas : presque tous ne bougent jamais (chaque
échantillon identique au bit près). Le replay les envoie environ dix fois par seconde quoi qu'il arrive ; donc,
parmi leurs échantillons, seuls ceux qui les déplacent (0,05 m ou 0,1 degré) sont conservés, et un par 10 s
(`selfCheck.sceneUnits` compte les échantillons écartés). Auparavant, c'étaient des trajectoires nommées
`uid 8`, sans véhicule.

---

Une partie de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source : [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
