---
title: Fichiers annexes et complétude
nav_order: 8
lang: "fr"
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Fichiers annexes et complétude {#sidecars-and-completeness}

Rien dans un replay n'est jeté. Ce que le convertisseur lit va dans la table et le document de match ;
tout le reste est conservé en entier dans trois fichiers annexes à côté de la table (à l'intérieur du
fichier `.3dheat`, ou séparés avec `--loose`). C'est la règle que partagent tous les convertisseurs de
3DHeat : [Les convertisseurs gardent tout](https://holdi601.github.io/3DHeat/converters.html).

## Les fichiers annexes {#the-sidecars}

- `<match>.messages.parquet` : chaque message adressé à une unité (heure, identifiant et nom du message,
  uid, eid, modèle, véhicule, ses champs d'identifiant en hexadécimal, `decoded` (ce qui en est lu, en
  JSON), la charge utile), chaque valeur de composant répliqué (`name` le composant, `fields` sa valeur),
  chaque message d'entité (avec son entité et son numéro de classe), chaque objet répliqué (`ReflectionData
  <kind>/<index>`, ses champs en hexadécimal) et chaque paquet qu'aucun lecteur ici ne prend, en entier.
- `<match>.objectives.parquet` : les zones de capture au fil du temps, une ligne par changement envoyé
  par le serveur : `time`, `event` (`state`, `progress`, `captured`, `neutralised`), `zone` (sa lettre),
  `zoneId`, `object`, `owner` (0 aucun, 1, 2), `progress` (-100..100, positif vers l'équipe 2), les `x`,
  `y`, `z` de la zone, et tous les `fields` de l'objet en hexadécimal (voir [Objectifs](objectives.md)).
- `<match>.flight.parquet` : chaque entrée du modèle de vol de chaque avion, en entier (ses bits, et
  `phase` : le bit de son premier octet où elle a commencé), avec sa vitesse, les 14 demi-octets de
  commande (`control1-3`, `throttle`), ses moteurs avec leur état, la postcombustion et leur condition, et
  ses coups par arme (`ammo` ; `numbers` est la liste entière). Les valeurs des autres avions sont celles
  de leur dernier rafraîchissement.

## Ce que garantissent les compteurs {#what-the-counts-guarantee}

Les `counts` du document de match disent ce que le replay contenait et ce qu'il est devenu :

| Clé | Contenu |
|---|---|
| `packets`, `unreadPackets` | chaque type de paquet rencontré, et ceux qu'aucun lecteur ne prend (conservés en entier dans le fichier annexe des messages) |
| `messageIds`, `messageIdsNotRead` | chaque identifiant de message rencontré et combien de fois, et ceux seulement conservés, non lus |
| `replicatedComponents`, `replicatedNotRead` | valeurs de composants lues, et celles seulement conservées |
| `entities`, `entityTemplates`, `entityMessages` | ce que le flux d'entités a créé et envoyé |
| `droppedSamples` | échantillons laissés de côté volontairement (l'épave d'une unité au sol, une fois son entité disparue), par raison |

Rien d'autre n'est laissé de côté : un élément du replay est soit lu dans la table ou le document de
match, soit conservé en entier dans un fichier annexe. Le `selfCheck` du document de match contient les
contrôles de ce qui a été lu ([Comment le replay est lu](how-it-reads.md)).

---

Une partie de [3DHeat](https://github.com/Holdi601/3DHeat) ([documentation](https://holdi601.github.io/3DHeat/)). Source : [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
