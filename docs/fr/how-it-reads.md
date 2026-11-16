---
title: Comment le replay est lu
nav_order: 10
lang: "fr"
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Comment le replay est lu {#how-it-reads-a-replay}

Cette page s'adresse aux personnes qui veulent savoir ce que le convertisseur lit, comment cela a été
vérifié, et donc dans quelle mesure faire confiance à chaque colonne. Vous n'en avez pas besoin pour
convertir des replays.

La lecture a été vérifiée sur des replays client de batailles arcade aériennes, simulateur aériennes et
navales, sur des replays serveur de batailles terrestres, et, pour les dispositions de 2025, sur les
replays d'exemple publics de
[wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder). Chaque contrôle compare une
valeur à quelque chose que le replay indique d'une seconde manière, indépendante ; seuls la méthode et
l'accord sont donnés ici.

## Ce qui est lu, et le contrôle {#what-is-read-and-the-check}

| Partie | État, et le contrôle |
|---|---|
| En-tête, carte, mission, heure de début, session ; résultats | chaque fichier |
| Réglages de la mission (le blk après l'en-tête) | mode, météo, limites, `stars` (date, heure, lieu) |
| Flux de paquets (zlib en 2025, zstd en 2026) | chaque paquet encadré |
| Positions et attitude des avions (disposition 2026) | 4 échantillons par seconde, aucun paquet non lu ; le cap concorde avec la direction de déplacement |
| Paquets de vol en avance sur leur temps | après un à-coup réseau, le paquet de vol d'un replay client contient parfois chaque autre avion là où il sera environ 0,75 s plus tard. L'avance est mesurée par paquet, et chaque avion en avance reçoit le temps qu'il représente (`selfCheck.flightPacketsRetimed`) |
| Recalages de recalcul de position | un saut hors d'une course recalculée est mesuré à partir du dernier état reçu, de sorte que les corrections du client ne coupent plus les trajectoires ([Recalcul de position](aircraft.md#dead-reckoning-and-the-smoother)) |
| Téléportations | une trajectoire est coupée là où son unité se déplace plus loin qu'elle ne le peut : d'abord selon son genre (avion 750 m/s, sol et navires 40 m/s, armes 1800 m/s), puis selon sa propre allure. Chaque coupure est listée dans `trackBreaks` avec sa cause probable (réapparition, déplacement du joueur par le jeu, correction d'une unité lointaine). Après les coupures, aucun pas entre les lignes d'une trajectoire n'est plus rapide que son genre ne le permet (`selfCheck.stepSpeed`) |
| Positions au sol et des navires (0xF073 / 0xF074) | aucun paquet non lu. Cap, tangage et roulis à partir de l'attitude sur 16 bits : le cap concorde avec la direction de déplacement à environ 2 degrés près (médiane) ; le tangage compte 180/65536 degré par pas ; avec le signe du roulis retourné, la direction du canon depuis la coque et la tourelle pointe sur l'unité touchée pour presque chaque tir de char. Les navires reposent au niveau de l'eau |
| Tourelles | lacet de tourelle et tangage du canon des chars : voir [Tourelles](ground.md#turrets) |
| Hauteurs de terrain compactées | les positions compactées sur 64 bits comptent leur hauteur à partir de -100 m sur la plupart des niveaux, et à partir du niveau de l'eau sur certains ; le décalage est mesuré sur chaque replay à partir des unités vues sous les deux formes (`selfCheck.packedGroundHeight`) |
| Flux d'entités (création, destruction) | chaque création est lue. La disposition vient du code source publié du Dagor Engine ; les types de composants propres à War Thunder sont sautés en repérant où commence le composant suivant. Le véhicule et l'emplacement de joueur de chaque unité sont égaux à ceux que nomment les enregistrements de destruction et d'impact, pour chaque enregistrement contrôlé |
| Qui a conduit quelle unité, unités d'IA, navires, cibles au sol | depuis le flux d'entités : chaque unité a son véhicule et son équipe, l'unité de chaque joueur son joueur |
| Destructions par rapport aux résultats | les morts par joueur sont égales à celles des résultats ; les résultats comptent davantage de kills, car le client ne reçoit pas chaque kill. Un replay qui commence après le début de la bataille ne contient que les kills postérieurs à ce moment |
| Kills, coups critiques, dégâts graves | chaque fichier |
| Modules détruits (0xF118) | l'unité et le numéro de la pièce ; le nom de la pièce demande le modèle de dégâts du véhicule, qui ne figure pas dans le replay |
| Armes lâchées (flux d'entités) | le point de lâcher se trouve à 10-20 m environ (médiane) de l'unité la plus proche, qui est prise pour le lanceur |
| Armes en vol (0xF0DB) | missiles, roquettes et bombes, chacun rattaché à son entité |
| Bombes sans enregistrements de vol | une bombe sans eux voit sa chute calculée depuis le lâcher jusqu'à l'impact (gravité et traînée, un échantillon toutes les 0,1 s, `extrapolated` à vrai). Vérifié au-dessus de la mer, où la hauteur d'impact est connue : les chutes calculées finissent à environ 15 m de l'eau près. Dans le document de partie, une telle arme porte `ballisticImpact` ; `counts.bombsBallistic` les compte |
| Emplacements de joueurs, chat | chaque fichier |
| Explosions, éclatements de DCA, prix, détections, météo, objets de mission | lus ; positions vérifiées à l'œil dans le visualiseur |
| Instruments du joueur qui enregistre (0xD04A) | nommés d'après ce qu'ils font : [Instruments du cockpit](aircraft.md#cockpit-instruments) ; le reste sous `notNamed` |
| Autres champs des entrées de vol | vitesse, coups, commandes, moteurs : [Entrées de vol](aircraft.md#flight-entries) |
| Attitude des lignes d'événements | chaque ligne d'événement porte le cap, le tangage, le roulis et le vecteur de regard de son unité à cet instant |
| Statistiques des joueurs et scores d'équipe | à la fin de la bataille, chaque statistique est égale à celle des résultats pour chaque joueur : [Données de réflexion](aircraft.md#reflection-data) |
| Noms des armes et des véhicules | depuis la localisation anglaise de votre installation ; quelques navires, leurs ceintures par défaut et les radars d'aérodrome n'ont pas de nom dans le jeu |
| Joueurs et IA | aucune ligne d'un joueur des résultats n'est IA, chaque ligne non IA est celle d'un joueur des résultats (`selfCheck.identity`) |
| Épaves | les échantillons d'une unité après sa mort continuent d'arriver ; l'épave d'une unité au sol ou d'un navire reste `alive` 0 jusqu'à la suppression de son entité, et reste une seule trajectoire ; les avions gardent `alive` 0 pendant 60 s au plus (`selfCheck.wrecks`) |
| Changements de véhicule | une unité encore vivante d'un joueur, lorsque la suivante du même joueur apparaît, est terminée à cet instant (un véhicule laissé sur place). `selfCheck.vehicleSwitch.twoLiveVehicles` doit valoir 0 |
| Mode de bataille | [Mode de bataille](ground.md#battle-mode) |
| Avions dans un replay serveur de 2026 | lus dans la disposition de 2026 ; le cap et le signe du roulis concordent avec les virages ; les avions de substitution et les drones de reconnaissance ne portent aucune donnée |
| Joueurs d'un replay serveur | trouvés par nom dans les emplacements ; chaque statistique est égale à celle des résultats (`selfCheck.players`) |
| Avions dans les replays serveur de 2025 et la version 101286 | non lus : leurs paquets de vol ont une autre disposition |

## Messages aux unités {#messages-to-units}

Chaque paquet de type 4 est un message mpi du daNet du Dagor Engine : l'identifiant de l'objet
destinataire, puis (lorsque ses 11 bits de poids faible sont tous à 1) l'UID ext de l'objet, l'identifiant
du message et la charge utile. Un message adressé à une unité porte comme UID ext l'identifiant d'entité de
l'unité, `index << 10 | generation`. Vérifié : chaque message de ce type nomme une entité vivante à cet
instant.

Pour les spécialistes, les messages lus :

| Message | Ce que c'est, et le contrôle |
|---|---|
| 0xF0E9 UnitHitEffects | l'impact d'un projectile : l'uid du tireur et le point d'impact dans le repère de l'unité (x avant, y haut, z gauche) : centimètres sur avions et navires, 20/32768 m par pas sur les unités au sol (ajusté à la taille des tourelles de char). `hitLocalX/Y/Z` en mètres. Devient une ligne `shot` ([Tirs](hits.md#gunfire)). Le tireur de presque chaque enregistrement d'impact et de destruction figure parmi ces tireurs ; les points d'impact se trouvent du côté qui fait face au tireur |
| 0xF133 UnitOnExplosion | le même uid de tireur |
| 0xF04B OnUnitDead | lignes `dead` : chaque victime d'un enregistrement de kill en a une dans les 2 s |
| 0xD047 FmwRpm | les régimes des moteurs (`rpm`) ; concorde avec la jauge de régime du cockpit |
| 0xF0B1, 0xF0A0 | lignes `gun_shot` : coups uniques de la DCA lourde et de l'artillerie |
| 0xF01B, 0xF01C | lignes `fire_start`, `fire_stop` : rafales des canons DCA de 40 mm (un canon qui tire ; un feu sur un véhicule est `fire_on`, voir [Incendies des véhicules](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | lignes `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` |
| 0xD0FE ProjectileHitReplay | les impacts portés et subis par le joueur qui enregistre, avec l'arme et la munition, nommées d'après l'installation (`projectileHitReplays`) |
| 0xF13E, 0xF031 | l'effet visuel d'un impact et un effet joué sur l'unité ; ils accompagnent un impact sur la même unité |
| 0xD041 | un par canon défensif d'un avion, deux fois par seconde ; ses index correspondent aux armes de mitrailleur du modèle de vol |
| 0xD048, 0xF117 | disposition lue, sens inconnu |
| le reste (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | dans le fichier annexe des messages, avec leur unité et leurs champs |

Les noms sont ceux de la communauté (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Également lu {#also-read}

- **Réplication du flux d'entités** (0x22, 0x23) : par entité, un bloc de valeurs de composants :
  minuteries de réparation des navires, compteurs de consommables, changements de propriétaire et
  d'équipe, surchauffe moteur. Compté dans `counts.replicatedComponents` ; les valeurs dans le fichier
  annexe des messages.
- **Actions de script de mission** (0xF028) et **indications** (0xF0EC) : `triggers`, `hints`.
  **Progression de mission** (0xF07A, 0xF07C) : `missionProgress`.
- **La caméra de replay** (0xD043) : voir [La caméra](ground.md#the-camera).

## Non lu, et pourquoi {#not-read-and-why}

- **Noms et contenus des messages d'entités** (0x20, 0x21) : le numéro de classe est une place dans une
  liste compilée dans le jeu, non envoyée et absente de ses données. Deux sont lus (les feux d'un véhicule
  et ses extincteurs) ; le reste est conservé entier avec son entité et son numéro de classe.
- **Autres objets répliqués** (genres autres que les emplacements de joueurs et les équipes) : lus et
  conservés, non nommés ; rien dans les résultats pour les contrôler.
- **Commandes, manette et coups des autres avions** : rafraîchies seulement de temps en temps ; conservées
  dans le fichier annexe de vol, non dans la table.
- **Incendies d'avions** : introuvables dans tous les messages ; un avion en feu n'a pas de ligne
  `fire_on`.
- **Noms des armes lâchées** : l'entité d'une bombe ou d'une roquette ne porte aucun nom ; les
  enregistrements de kill nomment l'arme d'un kill.
- **Tirs manqués** : un replay ne contient que les impacts.

Le `counts.messageIdsNotRead` et le `selfCheck` de chaque document de partie indiquent ce qu'un nouveau
replay contient et à quel point il a été bien lu.

---

Une partie de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source : [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
