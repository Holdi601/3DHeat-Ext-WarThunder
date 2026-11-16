---
title: Avions
nav_order: 11
lang: "fr"
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Avions {#aircraft}

Pour les lecteurs qui veulent savoir d'où viennent les colonnes des avions et dans quelle
mesure leur faire confiance. Chaque contrôle compare une valeur à quelque chose que le
replay indique d'une seconde manière, indépendante ; seuls la méthode et l'accord sont
donnés.

## Instruments du cockpit {#cockpit-instruments}

Le message 0xD04A envoie les jauges du joueur qui enregistre sous forme de paires (numéro,
valeur) : quatre par seconde dans les batailles arcade, seulement les valeurs modifiées dans
les batailles simulateur. Les numéros forment une seule liste pour tous les cockpits, et un
cockpit envoie les jauges que son modèle possède. Le code du jeu définit quel numéro
correspond à quelle jauge ; chaque numéro a donc été nommé d'après ce qu'il fait, puis
vérifié sur le replay (`convert.INSTRUMENTS` contient le résultat ; rien n'est lu dans
l'installation) :

| Numéro | Nom | Vérifié par |
|---|---|---|
| 0 | vitesse indiquée, m/s | la vitesse de la trajectoire corrigée pour la densité de l'air : corrélation 0,99 |
| 39 | vitesse verticale, m/s | la vitesse verticale de la trajectoire : corrélation supérieure à 0,99 |
| 40, 41 | altitude, m ; altitude modulo 1000 | la hauteur de la trajectoire, à quelques mètres près |
| 52, 53 | roulis et tangage de l'horizon artificiel | moins le roulis et le tangage de la table, à moins de 1 degré près |
| 64 | compas | le cap de la table, à moins de 0,1 degré près |
| 15-20 | palonniers | la force latérale sur l'avion |
| 23, 31 | manche : profondeur et ailerons (signe selon le modèle de cockpit) | l'angle d'attaque ; la vitesse de roulis |
| 69, 71, 73 | horloge : heures (cadran à 12 heures), minutes, secondes | l'heure locale de l'ordinateur d'enregistrement, à la minute près |
| 75 | pression d'admission, atm | plus haute en puissance de guerre d'urgence qu'à pleins gaz |
| 81-86, 87-92, 93-98 | régime par moteur, régime modulo 1000, jauge de régime | identiques entre eux ; le régime moteur : corrélation supérieure à 0,97 |
| 195 | carburant | baisse pendant une sortie, remonte à plein à la réapparition |
| 228-230 | jambes du train d'atterrissage, 1 = sorti | sorti seulement près de la hauteur des aérodromes et à la vitesse d'atterrissage |
| 240, 241 | manette par moteur (1,1 en puissance de guerre d'urgence ou postcombustion) | la manette de l'entrée de vol |
| 330-332, 346-348 | compteurs de munitions (deux jeux égaux) | les coups du préréglage d'armes, en baisse avec les coups de l'entrée de vol |
| 135, 159 | température d'huile et de culasse | probablement : elles montent pendant une sortie |
| 58, 61 | bille de dérapage, aiguille de virage | probablement : elles suivent la force latérale et la vitesse de virage |
| 223 | aérofrein | probablement : mis seulement à l'approche |
| 490-497, 500-505 | freins de roue | probablement : mis seulement à l'arrêt sur un aérodrome |

Quelques autres numéros sont envoyés sans que leur sens soit connu ; ils sont conservés dans
`authorInstruments.notNamed` du document de partie.

Les colonnes `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`,
`headTemperature` et `throttle` de la table viennent de ces numéros, sur les lignes du joueur
qui enregistre, en prenant le dernier message au plus 0,2 s après l'échantillon.

## Entrées de vol {#flight-entries}

L'entrée de vol de chaque avion (type de paquet 2) contient, en plus de sa position et de
son attitude :

- **Vitesse** : un mot de 32 bits après l'attitude. Les bits 31, 30 et 29 sont les signes de
  x, y et z ; puis la vitesse sur 11 bits de 500/2047 m/s (elle s'arrête à 500 m/s), puis
  |x| et |y| en fractions de la vitesse sur 9 bits chacun, et z est ce qui fait du vecteur un
  vecteur unitaire. Vérifié par rapport au pas entre les échantillons reçus : la direction
  concorde à une fraction de degré près pour le joueur qui enregistre, et à environ 2 degrés
  près pour les autres ; la vitesse à 0,2 % près. `selfCheck.flightEntries`.
- **Coups par arme** : une liste avant la position, un élément par arme, les coups restants
  en premier. Celle du joueur qui enregistre est égale aux compteurs du cockpit un tick plus
  tard, pour presque chaque échantillon.
- **Commandes et manette** : 7 octets après la vitesse, lus comme 14 demi-octets. Pour le
  joueur qui enregistre, à chaque tick : 1 la profondeur, 2 les ailerons, 3 la direction (8 au
  repos), 11 la manette en quinzièmes (15 aussi pour la puissance de guerre d'urgence et la
  postcombustion), 4 les freins de roue, 5 l'aérofrein, 8 probablement le parachute de
  freinage. Les demi-octets des autres avions ne changent que quelques fois par bataille et
  ne sont pas leurs commandes au moment considéré.
- **Moteurs** : par moteur, un octet d'état (0 éteint ; 1-6 en démarrage ; 7 en marche ; 8
  mort), une valeur de 16 bits seulement avec la postcombustion (32767 à fond), et un octet
  seulement après que le moteur a été touché. La plupart des avions dont le moteur passe à
  « mort » sont abattus ou finissent en quelques minutes.

## Données de réflexion {#reflection-data}

Les messages 0xF02D et 0xF0AA répliquent les objets numérotés du jeu : pour chaque objet, son
identifiant (les 5 bits de tête le genre, les 11 bits de poids faible un index) et une table
de champs. Le genre 14 correspond aux emplacements de joueurs (champ 2 identifiant utilisateur
et nom, 9 l'équipe), le genre 15 aux équipes (index 1 et 2) :

- Le champ 39 d'un emplacement contient ses statistiques à des places fixes : kills (décalage
  0), kills d'équipe (2), morts (4), kills navals (10), kills d'IA (12), kills d'IA au sol (14),
  assistances (20), zones de capture (22), dégâts de zone (24, sur 32 bits), prime de dégâts
  (40, sur 32 bits), esquives de missiles (50). Le champ 38 commence par le score, le champ 42
  est l'escadron. À la fin d'une bataille, chaque valeur est égale à celle des résultats pour
  chaque joueur (`selfCheck.scoreboardVsResults`). On ne sait pas où sont gardés les kills
  au sol.
- Le champ 7 d'une équipe est son score : à la fin, il est égal à la somme des scores de ses
  joueurs dans les résultats. Le champ 3 correspond probablement à ses tickets.
- Chaque message n'envoie que les champs qui ont changé ; `scoreboard` dans le document de partie liste donc les statistiques de chaque joueur et le score de chaque équipe à chaque
  changement.

## Recalcul de position, et le lisseur {#dead-reckoning-and-the-smoother}

Un replay client enregistre chaque avion quatre fois par seconde, tel que le client le
dessinait. Entre les mises à jour qu'il reçoit pour un avion éloigné, le client fait avancer
celui-ci selon sa dernière vitesse et le fait tourner selon ses derniers taux, puis, à la
mise à jour suivante, il le recale à cette position. Lu tel quel, une trajectoire est droite,
puis saute. Rien dans l'entrée de vol n'indique quels échantillons ont été reçus ; un
échantillon recalculé se reconnaît à ce qu'il est : il prolonge la ligne droite des deux
échantillons qui le précèdent, à leur allure, à 3 cm près.

L'importance de cela dépend de la bataille : dans les batailles arcade, environ la moitié des
échantillons des autres avions peuvent être recalculés ; dans les batailles simulateur, seulement
quelques pour cent. Le lisseur réduit d'environ cinq fois les sauts de plus de 15 g
(`selfCheck.deadReckoning`). L'avion du joueur qui enregistre n'est pas extrapolé par le
client et reste tel quel.

Par défaut (`--no-smoothing` le désactive), les trajectoires de toutes les unités sauf celle du
joueur qui enregistre sont placées là où les états reçus disent qu'elles étaient : un
échantillon recalculé passe sur une courbe qui relie les échantillons reçus avant et après,
chacun avec sa propre vitesse ; au-delà de 3 s, la ligne droite est seulement infléchie vers le
prochain échantillon reçu, de sorte qu'aucun échantillon ne se déplace plus loin que le recalage
du client lui-même. Son attitude tourne régulièrement d'une attitude reçue à la suivante. Les
échantillons reçus sont lissés d'au plus 2 m ou 0,04 s de leur vitesse ; un virage régulier reste
tel quel. Les valeurs propres au replay restent dans les colonnes `Raw`.

## Attitude, vérifiée {#attitude-checked}

Sur l'avion du joueur qui enregistre, le cap est à un degré près (médiane) de la direction de
déplacement, le tangage à quelques degrés près de l'angle de montée, et dans les virages nets,
le roulis a le signe du virage pour presque chaque échantillon : le roulis du modèle de vol est
positif aile gauche basse, et la table le donne positif aile droite basse
(`selfCheck.aircraftAttitude`). Les angles sur 10 bits avancent par pas de 0,18 degré. L'attitude
des unités au sol est vérifiée par rapport à leurs tirs ([Tourelles](ground.md#turrets)).

---

Une partie de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source : [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
