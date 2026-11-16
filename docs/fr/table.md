---
title: La table
nav_order: 6
lang: "fr"
source: table.md
source_hash: "9fd198ff79e6"
nav_exclude: true
search_exclude: true
---
# La table {#the-table}

![La table d'un replay synthétique, résumée](../assets/img/table.svg)

Une ligne par échantillon ou événement, 105 colonnes ([Liste des colonnes](../columns.md), générée à partir du
code) ; dans le pied de page, sous `heat3d`, les consignes de lecture du visualiseur, de sorte que la
visualiseur n'a aucun formulaire à remplir.

| Colonne | Contenu |
|---|---|
| `time` | secondes sur l'horloge propre du replay |
| `event` | `position` ; les lignes d'événement se trouvent sur la trajectoire à leur instant (entre deux échantillons, sur la droite qui les relie) ; `kill` (chez le tueur), `death` (chez la victime), `hit_critical` / `hit_severe` (chez l'unité touchée), `module_destroyed` (chez l'unité), `launch` (chez l'unité qui a lâché une arme), `impact` (le dernier échantillon d'une arme lorsqu'elle a été retirée juste après) ; `explosion` et `flak` (0xD08E, 0xD01F) à leur position, genre `effect`, sans trajectoire, avec la direction de l'explosion lorsqu'elle en a une ; `shot` (un projectile qui a touché, chez le tireur), `gun_shot`, `fire_start`, `fire_stop` (la rafale d'un canon, non un véhicule en feu), `fire_on`, `fire_off` (un véhicule en feu, voir [Incendies des véhicules](hits.md#vehicle-fires)), `reward` (Lions d'argent et points de recherche gagnés, voir [Économie](economy.md)), `dead`, `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` (voir [Messages aux unités](how-it-reads.md#messages-to-units)) ; `despawn` : la dernière ligne d'une trajectoire dont l'unité a disparu avant la fin du replay (voir [Fin d'une trajectoire](ground.md#end-of-a-track)) |
| `track` | ce que le visualiseur dessine comme une seule chose : une vie d'unité, ou le vol d'une arme - `<joueur ou véhicule> #<hex>` (le visualiseur montre le nom sans la partie `#`) |
| `x`, `y`, `z` | les mètres du jeu : x vers l'est, y vers le haut, z vers le nord (les indications retournent z, de sorte que le nord n'est pas dessiné au sud) |
| `player` | le nom du joueur ; pour une unité d'IA `<VehicleName> #<uid>` (par exemple `F-15A #204`) ; `uid <n>` lorsque rien ne la nomme ; pour une arme, qui l'a lâchée |
| `userId`, `team` | l'identifiant Gaijin du joueur et son équipe (`1`, `2`) |
| `ai`, `isPlayer` | `ai` vaut vrai pour chaque unité que ne conduit aucun compte joueur (unités de mission, avions d'IA, cibles au sol, canons DCA, navires sans joueur, substituts), `isPlayer` l'inverse : un joueur est une unité dont l'entité nomme un emplacement de joueur avec un identifiant Gaijin. Une arme a celui de son lanceur ; vide lorsqu'il est inconnu |
| `match` | l'identifiant du match (`match` du document de partie), sur chaque ligne ; les indications en font la session, de sorte que deux replays chargés ne se mélangent jamais dans leurs trajectoires |
| `life` | `uid#n` : la trajectoire d'une unité, coupée lorsque l'uid passe à une autre unité, que l'unité se déplace plus vite qu'elle ne le peut (une réapparition, un réarmement, un déplacement par le jeu, une correction du client pour une unité lointaine ; voir Téléportations dans [Comment le replay est lu](how-it-reads.md#what-is-read-and-the-check)) ou qu'elle n'est pas vue depuis longtemps ; `w<hex>` le vol d'une arme (`w<hex>#n` après une coupure) |
| `uid` | l'identifiant de l'unité dans le replay |
| `kind` | `aircraft`, `helicopter`, `tank`, `apc`, `spaa`, `truck`, `ship`, `boat`, `structure`, `train` (un tramway ou un wagon que place le niveau, voir [Unités de scène](objectives.md#scene-units-trams-and-rail-wagons)) ; armes `missile`, `rocket`, `bomb`, `torpedo`, `payload`, `jettisoned` ; `camera`, la caméra de replay du joueur qui enregistre (voir [La caméra](ground.md#the-camera)) |
| `type` | le type propre au jeu lorsque les résultats le nomment (`fighter`, `assault`, `destroyer`, `gun_boat`), sinon comme `kind` |
| `Vehicle` | l'identifiant du véhicule dans le jeu (`f_15a`, `germ_flakpz_I_Gepard`), que les figurines du visualiseur reconnaissent |
| `VehicleName`, `VehicleShortName`, `VehicleNameKey` | le nom anglais du véhicule tiré de la localisation de votre installation (`Pz.Kpfw. III Ausf. J1`, court `Pz.III J1`) et sa clé (`germ_pzkpfw_III_ausf_J_0`) ; les marques de pays de la police du jeu sont omises. Lorsque le jeu ne nomme rien, ou qu'aucune installation n'est trouvée, le nom est l'identifiant et la clé est vide |
| `mission` | le nom de l'unité dans la mission (`t1_tank_05`, `t2_player03_0`) |
| `dirX`, `dirY`, `dirZ` | vers où pointe l'unité (le vecteur de regard) : avions à partir de l'attitude du modèle de vol, unités au sol et navires à partir de leur propre attitude, armes le long de leur vol |
| `heading`, `pitch`, `roll` | la même chose en degrés ; le cap est la boussole, dans le sens horaire depuis le nord, le tangage positif le nez vers le haut, le roulis positif aile droite basse (le modèle de vol envoie le signe inverse, voir [Attitude, vérifiée](aircraft.md#attitude-checked) ; côté droit d'une unité au sol vers le bas). Les indications le précisent sous `conventions` |
| `turretYaw`, `gunPitch`, `turrets` | la tourelle principale d'un char - là où pointe le canon, non là où regarde son joueur ; la valeur du replay retenue à la vitesse d'entraînement de la tourelle et fixée sur la ligne de chaque tir du canon principal (voir [Tourelles](ground.md#turrets)) : son lacet par rapport à la coque (degrés, positif dans le sens horaire vu d'en haut, 0 droit devant) et le tangage de son canon par rapport à la coque (degrés, positif vers le haut) ; `turrets` chaque tourelle du véhicule sous la forme `yaw pitch;yaw pitch;...` dans son ordre propre (un emplacement inutilisé vaut `0.00 0.00`). Chars, SPAA, transports de troupes et camions, dans les replays client et serveur ; non les navires (voir [Tourelles](ground.md#turrets)) |
| `turretYawRaw`, `gunPitchRaw` | la tourelle principale telle que le replay l'envoie ; `turretYaw` / `gunPitch` sont celles-ci retenues à la vitesse d'entraînement de la tourelle et fixées sur la ligne de chaque tir du canon principal (voir [Tourelles](ground.md#turrets)) |
| `viewYaw`, `viewPitch` | là où le joueur regarde (vise avec la caméra) dans le monde : degrés de boussole (0 nord, sens horaire) et degrés vers le haut, la même convention que `aimHeading` / `aimPitch` (contrairement à `turretYaw` / `gunPitch`, qui restent relatifs à la coque). Le char de chaque joueur dans un replay serveur, celui du joueur qui enregistre dans un replay client ; vide là où le joueur ne vise nulle part (les quatre flottants de visée à 0). La tourelle le suit à sa propre vitesse de rotation, de sorte que les deux diffèrent pendant qu'elle tourne (voir [Tourelles](ground.md#turrets)) |
| `aimHeading`, `aimPitch`, `aimDistance` | le char propre du joueur qui enregistre : où il vise (degrés de boussole, degrés vers le haut, la distance en m ; 2000 lorsque rien n'est dans le viseur) ; lignes de caméra : où le joueur vise (cap, tangage) |
| `zoom` | lignes de caméra : le grossissement de la caméra (voir [La caméra](ground.md#the-camera)) |
| `difficulty`, `gameMode` | le `AB`, `RB` ou `SB` de la bataille, et `ground`, `air` ou `naval`, sur chaque ligne (voir [Mode de bataille](ground.md#battle-mode)) |
| `extrapolated` | un échantillon d'avion qui est le recalcul de position du client, non un état reçu (voir [Recalcul de position](aircraft.md#dead-reckoning-and-the-smoother)) ; un échantillon de bombe calculé à partir de son lâcher (voir Bombes sans enregistrements de vol dans [Comment le replay est lu](how-it-reads.md#what-is-read-and-the-check)) |
| `moved`, `xRaw`, `yRaw`, `zRaw`, `headingRaw`, `pitchRaw`, `rollRaw` | de combien le lisseur a déplacé l'échantillon (m), et la position et l'attitude propres au replay (roulis dans le signe de la table) |
| `targetX`, `targetY`, `targetZ` | le point d'impact d'un `shot` |
| `hitOutcome`, `hitFlags` | l'issue d'un `shot` sur une unité au sol : `kill`, `critical`, `penetration` ou `nonpenetration` (rebondi ou arrêté : le replay ne distingue pas un ricochet), à partir des bits que le serveur envoie avec l'impact (`hitFlags`, brut) ; vide là où rien n'est envoyé (avions, navires). Voir [Issues des impacts](hits.md#hit-outcomes) |
| `hitShell` | la signature d'obus d'un `shot` : quatre octets du message d'impact (hexadécimal brut) ; une même signature peut correspondre à différents obus (les APFSDS de 120 et 125 mm en partagent une), elle est donc conservée brute, non lue comme un calibre |
| `ammoType`, `ammoName`, `ammoSlot`, `calibre` | les munitions d'un `shot` : leur type (`APFSDS`, `APDS`, `HE`, `HEAT-FS`, `HESH`, `ATGM`...) et identifiant (`125mm_3bm46`) lorsqu'un kill nomme le logement du tireur, sinon `explosive` (la rafale d'impact) ou `kinetic` ; le `weapon/slot` du canon à partir de ses rechargements ; le calibre en mm à partir des fichiers d'armes de l'installation. Voir [Issues des impacts](hits.md#hit-outcomes) |
| `rpm` | le régime moteur d'un avion (la moyenne de ses moteurs) tel qu'envoyé en dernier, dans les 2 s |
| `vx`, `vy`, `vz` | la vitesse d'un avion telle que son entrée de vol l'envoie (m/s, les axes du jeu ; les vitesses au-delà de 500 m/s valent 500) |
| `engine`, `afterburner`, `engineCondition` | les moteurs d'un avion d'après son entrée de vol : `off`, `starting`, `running`, `dead` (séparés par `/` lorsque ses moteurs diffèrent) ; la postcombustion de 0 à 1 ; un octet envoyé seulement après que le moteur a été touché |
| `weaponName` | kills et morts : l'arme ou la munition dans l'anglais de votre installation (`AIM-120C-5 AMRAAM air-to-air missiles`, `Fragmentation incendiary tracer shell`) |
| `throttle`, `elevator`, `aileron`, `rudder`, `ammo` | l'avion du seul joueur qui enregistre : la manette de 0 à 1,1 d'après son cockpit (1,1 en puissance de guerre d'urgence ou postcombustion ; sinon les quinzièmes de son entrée de vol), les commandes de -1 à 1 d'après son entrée de vol (profondeur positive en tirant, ailerons positifs en roulant à droite), les coups restants par arme (`250 140 170`) |
| `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` | l'avion du seul joueur qui enregistre, d'après son cockpit : vitesse indiquée et vitesse verticale (m/s), carburant, pression d'admission (atm), train (de 0 à 1, 1 sorti), températures d'huile et de culasse, lorsque son cockpit a la jauge |
| `speed` | m/s sur environ deux secondes de la trajectoire (calculé ici ; le replay n'envoie aucune vitesse pour les autres unités) |
| `alive` | 0 pour les échantillons d'une unité après sa mort (son épave) : celle d'une unité au sol ou d'un navire jusqu'à ce que le jeu la retire ou que ses échantillons s'arrêtent, celle d'un avion pendant 60 s au plus |
| `otherVehicle`, `otherLife` | la victime d'un `shot` : son véhicule et sa `life` |
| `hitLocalX`, `hitLocalY`, `hitLocalZ`, `hitDirX`, `hitDirY`, `hitDirZ` | le point d'impact d'un `shot` dans le repère propre de la victime (m ; x avant, y haut, z gauche ; voir [Messages aux unités](how-it-reads.md#messages-to-units)) et le sens d'arrivée du tir, transformé dans ce repère par l'attitude de la victime à ce moment |
| `hitPart`, `hitFlag` | le message d'impact d'un `shot` : son mot de pièce tel qu'envoyé, et son octet de poids fort |
| `cost_fired_sl`, `cost_lost_sl`, `earn_sl`, `earn_rp`, `rewardType`, `currency`, `econ_basis`, `won`, `matchWon`, `round`, `roundEndReason` | ce que la bataille a coûté et rapporté, qui a gagné et comment elle s'est terminée : voir [Économie](economy.md) |
| `other`, `weapon` | kills : l'autre camp et l'arme ; impacts : qui a touché (d'après l'uid de l'enregistrement, sinon son emplacement de joueur), leur véhicule ; lancers : l'arme ; modules détruits : qui a touché l'unité en dernier dans les 5 s précédentes, et `part <n>` |

---

Une partie de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source : [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
