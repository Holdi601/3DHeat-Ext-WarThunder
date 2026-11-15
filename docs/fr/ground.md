---
title: Unités au sol et caméra
nav_order: 12
lang: fr
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Unités au sol et caméra {#ground-units-and-camera}

Pour les lecteurs qui veulent savoir d'où viennent les colonnes de tourelle, de caméra et de mode
de bataille, et dans quelle mesure leur faire confiance. Les contrôles ne donnent que la méthode
et l'accord.

## Tourelles {#turrets}

L'état au sol d'un char (attitude sur 16 bits) contient, après sa position, 141 bits non lus, puis
pour chaque tourelle 62 bits : le lacet de la tourelle et le tangage du canon (16 bits chacun,
360/65536 degré par pas, signés) et 30 bits non lus ; puis du remplissage, et sur certains états
200 bits de plus. Le nombre de tourelles est l'octet envoyé avant l'état. Un état dont la longueur
ne correspond pas ne donne aucune tourelle (les unités statiques envoient un état plus court). Le
lacet est relatif à la coque, positif dans le sens horaire, 0 droit devant ; le tangage est relatif
à la coque, positif vers le haut.

Comment cela a été vérifié :

- **Par rapport aux tirs :** pour chaque impact d'un char, la direction mondiale de son canon
  principal (attitude de la coque tournée par le lacet de la tourelle et le tangage du canon) par
  rapport à la ligne allant du tireur à l'unité touchée, à au moins 30 m : par bataille, une médiane
  d'environ 98 % à moins de 3 degrés en cap et 99 % en élévation (`selfCheck.turretsVsShots`). Les
  autres sont surtout des impacts de mitrailleuse depuis une autre tourelle.
- **Par rapport à la visée du joueur qui enregistre :** son propre char envoie l'angle mondial de sa
  visée (sens inverse des aiguilles d'une montre depuis l'est), son tangage et sa distance. Le cap de
  la coque plus le lacet de la tourelle est à moins d'un demi-degré (médiane) de la visée.

**Les replays serveur** (0xF074) envoient l'état de chaque char dans la même disposition, suivi de
données propres, de sorte que chaque tourelle dont les deux angles se trouvent dans l'état est lue
(au moins la principale pour presque chaque ligne de char). C'est la tourelle, non la caméra :

- **Par rapport aux tirs**, comme ci-dessus : par bataille, plus de 90 % à moins de 3 degrés en cap
  et 99 % en élévation.
- **Par rapport à la vue :** un replay serveur envoie la visée de chaque joueur (`viewYaw`,
  `viewPitch`). La tourelle suit la vue à moins d'un demi-degré (médiane), mais tourne beaucoup plus
  lentement que la vue ne balaie, comme le fait un entraînement de tourelle (`selfCheck.turretVsView`).
- **Mais pas toujours à la vitesse d'un entraînement :** échantillon par échantillon, la valeur telle
  qu'envoyée saute parfois sur la visée lorsque la visée est proche du canon, plus vite que tout
  entraînement ne tourne.

La table contient donc la tourelle **retenue par son entraînement** : `turretYaw` / `gunPitch` se
déplacent vers la valeur telle qu'envoyée, à une vitesse maximale égale à la vitesse de rotation du
canon principal selon le fichier de véhicule de l'installation (multipliée par 1,3 pour les
compétences d'équipage et les modifications ; 45 et 20 degrés par seconde là où l'installation n'en
nomme aucun). À chaque impact du canon principal, la tourelle est fixée exactement sur la ligne du
tir, et un passage à rebours l'y amène à temps (`selfCheck.turretLimit`). La ligne `shot` porte aussi
ces `turretYaw` / `gunPitch`. La valeur telle qu'envoyée reste dans `turretYawRaw` / `gunPitchRaw`.
Un char dont l'état ne contient aucune tourelle a des colonnes de tourelle vides (la visionneuse peut
alors se rabattre sur `viewYaw`). `gunPitch` est un peu au-dessus de `viewPitch` à longue portée :
c'est l'élévation du canon pour la chute de l'obus.

Les états des navires ont une autre disposition ; leurs tourelles ne sont pas lues. Les avions
n'envoient ni direction de tête ni direction de vue ; le message 0xD020 des canons antiaériens reste
non lu.

## La caméra {#the-camera}

Le message 0xD043, environ 20 par seconde, est la caméra de replay du joueur qui enregistre : champ 1
un quaternion qui tourne l'avant de la caméra vers ce qu'elle regarde ; 2 la place de la caméra par
rapport au véhicule qu'elle suit (m) ; 4 le même décalage dans le repère du véhicule (x avant, y haut,
z gauche) ; 5 l'endroit visé par le joueur (vecteur unitaire) ; 3 le zoom (environ 1,2 dans la vue à
la troisième personne d'un char, environ 1,0 dans un avion, plus haut dans la lunette d'un mitrailleur
ou aux jumelles). Vérifié : le champ 4 est le champ 2 tourné dans le repère du véhicule, à 0,5 m près
pour presque chaque message ; l'avant de la caméra a le cap de la visée. Le replay n'envoie aucun champ
de vision en degrés, seulement le zoom.

La table contient la caméra comme une trajectoire à part : genre `camera`, trajectoire
`<player> camera #ca`, une ligne au plus toutes les 0,1 s, à la place du véhicule suivi plus le champ 2,
regardant selon le quaternion (`dirX/Y/Z`, `heading`, `pitch`, `roll`), avec `zoom`, `aimHeading` et
`aimPitch`, et `otherLife`, la vie qu'elle suit. `selfCheck.camera` compte les lignes et le contrôle.

## Fin d'une trajectoire {#end-of-a-track}

Une trajectoire est dessinée de sa première ligne à sa dernière. Lorsque son unité a disparu avant la
fin du replay, sa dernière ligne est une ligne `despawn` à sa dernière place : au moment où le jeu a
retiré son entité (lorsque cela est arrivé dans les 6 s de son dernier échantillon), sinon à son dernier
échantillon. Une trajectoire sans cela dure jusqu'à la fin du replay. Les lignes d'une même trajectoire
peuvent être très espacées (une unité lointaine ou une épave est rafraîchie toutes les quelques secondes,
une épave parfois pas pendant plusieurs minutes) : son dernier état reste valable jusqu'à sa ligne
suivante.

## Mode de bataille {#battle-mode}

L'octet de l'en-tête au décalage 688 contient la difficulté dans ses quatre bits de poids faible :
0 arcade (AB), 5 réaliste (RB), 10 simulateur (SB). Vérifié par rapport aux types de batailles dont on
savait qu'ils étaient ceux des replays. Le mode de jeu est `ground` lorsque la mission permet l'apparition
de chars, sinon `naval` lorsqu'elle permet celle de navires, sinon `air` (`allowedUnitTypes`) ; le mode
propre à la mission vient de sa clé (`missions/_Dom`), nommé d'après le `lang/missions_versus.csv` de
votre installation. Cette même clé est la partie `<mode>` des noms de fichiers et l'identifiant du match
(`Conq4`, `Dom`), omise là où l'en-tête n'en a pas.

---

Une partie de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source : [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
