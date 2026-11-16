---
title: Impacts, tirs et incendies
nav_order: 13
lang: "fr"
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Impacts, tirs et incendies {#hits-gunfire-and-fires}

Pour les lecteurs qui veulent savoir d'où viennent les colonnes d'impact, de munition et d'incendie.
Les contrôles ne donnent que la méthode et l'accord.

## Tirs {#gunfire}

Chaque projectile qui a touché une unité est dans le replay (message 0xF0E9) : une ligne `shot` à la
position du tireur au moment de l'impact, `targetX/Y/Z` le point d'impact (l'unité touchée, déplacée
du point d'impact dans son repère, tournée selon son attitude), la direction vers elle, `other` l'unité
touchée. Les obus et balles qui ont manqué ne sont pas envoyés : ce ne sont pas des entités, et les
messages des armes en vol ne contiennent que les roquettes, missiles, bombes et torpilles. Les coups
restants du joueur qui enregistre (sa colonne `ammo`) baissent à mesure qu'il tire, de sorte que ses
rafales peuvent être distinguées, mais on ne sait pas où ces coups sont allés. La DCA lourde et
l'artillerie envoient chaque coup unique (`gun_shot`, sans direction), les canons DCA de 40 mm leurs
rafales (`fire_start`, `fire_stop`).

## Issues des impacts {#hit-outcomes}

Pour chaque impact de projectile sur une unité au sol, le serveur envoie le message 0xF144
(UnitOnHit) à l'unité : quatre champs d'un octet, le quatrième contient les bits de ce que l'impact a
produit (`selfCheck.unitMessages.outcome_*`) :

| Bit | Signification | Preuve |
|---|---|---|
| 0x20 | l'impact propre du projectile | presque tous arrivent avec un impact 0xF0E9 sur l'unité dans les 5 ms ; sans lui, avec une explosion (éclatement) |
| 0x01 | il a traversé (pénétration) | chaque message avec 0x02, 0x04 ou 0x08 l'a aussi |
| 0x02 | coup critique | la plupart des enregistrements de coup critique l'ont, bien plus souvent que par hasard |
| 0x04 | détruit | la plupart arrivent avec un enregistrement de destruction et la mort de l'unité dans la seconde |
| 0x08 | dégâts lourds | certains enregistrements de coup critique l'ont ; rare sinon |

`hitOutcome` prend le pire : `kill` (0x04), `critical` (0x02 ou 0x08), `penetration` (0x01),
`nonpenetration` (0x20 seul). Un impact est associé au 0xF144 non associé le plus proche, avec 0x20,
sur son unité, dans les 5 ms. La caméra d'impact du jeu distingue un ricochet d'une non-pénétration,
mais aucun bit ni aucun champ trouvé ici ne le fait : les trois premiers octets varient d'un impact à
l'autre et ne sont pas connus. Les replays client n'envoient 0xF144 que pour l'avion propre du joueur
qui enregistre, tous bits à zéro : les impacts sur avions et navires n'ont pas d'issue.

## Munitions {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Explosif ou non.** Un obus qui éclate envoie 0xF133 (UnitOnExplosion) avec l'identifiant uid du
  tireur et le numéro de l'impact ; un impact qui en a un est `explosive`, les autres `kinetic`.
* **Le canon et son logement.** 0xF0BD (UnitBulletRearm) est le prochain coup chargé : l'index de
  l'arme dans la liste d'armes du véhicule, le logement de munition et les coups restants. Le temps
  de rechargement d'un chargeur manuel arrive un temps de rechargement régulier après chacun de ses
  impacts, celui d'un canon automatique une fraction de seconde après. Les impacts d'un tireur sont
  regroupés par véhicule, signature et rafale ; un groupe est celui d'une arme lorsque cette arme
  charge un coup dans les 20 s après la moitié de ses impacts ou plus, à un délai régulier. `ammoSlot`
  est `weapon/slot`, le logement chargé avant l'impact : probablement celui qui a tiré, sauf si le
  joueur a changé de munition entre-temps. Les mitrailleuses n'envoient pas de 0xF0BD.
* **L'obus.** L'arme d'un kill est l'identifiant de l'obus (`125mm_3bm46`) ; le dernier impact du tueur
  sur la victime l'attribue au logement de ce tireur, lorsque le calibre du canon concorde. Son type et
  son calibre sont ceux du fichier d'arme (`bulletName`, `bulletType`, `caliber` ; `apds_fs_*` APFSDS,
  `heat_fs_*` HEAT-FS, `he_*` HE ...).
* **Le calibre** du reste : celui de l'arme d'un logement ; celui d'un groupe de mitrailleuses, l'unique
  calibre de mitrailleuse que sa signature peut avoir ; sinon celui du canon principal du véhicule. Sans
  l'installation (`--game`), il n'existe ni type, ni nom, ni calibre au-delà de `explosive` / `kinetic`.

Non trouvé : le ricochet. Plusieurs autres messages portent le tireur et le numéro de l'impact (0xF0C2,
probablement le trajet de la caméra d'impact à travers le véhicule ; 0xF117, 0xF13C, 0xF13E) ; ils sont
conservés dans le fichier annexe, sans être décodés. Une non-pénétration reste `nonpenetration`.

## Incendies des véhicules {#vehicle-fires}

Un véhicule en feu est montré à tous les clients : le serveur envoie au véhicule un message d'entité
(événement `0a519c58`) listant les feux qui brûlent sur lui, à chaque changement de la liste. Par feu : deux
identifiants sur 16 bits (le second est un nœud du modèle de dégâts), son genre, et -1 tant que le feu ne
prend pas. Un feu allumé par un impact reçoit aussi un message avec le point où il brûle, dans le repère du
véhicule (x avant, y haut, z gauche).

Lignes : `fire_on` lorsqu'un feu apparaît dans la liste, `fire_off` lorsqu'il a disparu, sur le véhicule,
avec `fireId` (`first:node`), `fireKind` et, pour les feux allumés par un impact, `fireLocalX/Y/Z` (avant,
haut, droite). Une fois le véhicule mort, sa liste n'est souvent plus envoyée : ses feux se terminent avec
son épave, sinon avec son entité, sinon avec le replay (`selfCheck.fires`).

Vérifié : chaque fois que le nombre d'extincteurs d'un char a baissé, un feu a quitté sa liste dans une
fraction de seconde ; la plupart des points de feu se trouvent du même côté du véhicule que l'impact qui
l'a allumé. Les genres sont des nombres ; ce qu'ils désignent n'est pas connu, ni quelle partie correspond à
un nœud. Les avions n'envoient aucune liste de ce type : un avion en feu n'est pas lu.

---

Une partie de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source : [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
