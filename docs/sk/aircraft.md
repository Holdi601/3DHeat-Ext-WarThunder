---
title: "Lietadlá"
nav_order: 11
lang: "sk"
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Lietadlá {#aircraft}

Pre čitateľov, ktorí chcú vedieť, odkiaľ pochádzajú stĺpce lietadiel a nakoľko im dôverovať. Každá kontrola nižšie porovnáva
hodnotu s niečím, čo replay hovorí iným, nezávislým spôsobom; uvádza sa len metóda a zhoda.

## Prístroje v kokpite {#cockpit-instruments}

Správa 0xD04A posiela prístroje hráča, ktorý replay nahral, ako dvojice (číslo, hodnota): štyrikrát za sekundu v arkádových
bitkách, len zmenené hodnoty v simulátorových bitkách. Čísla tvoria jeden zoznam pre všetky kokpity a kokpit posiela
prístroje, ktoré má jeho model. Kód hry určuje, ktoré číslo je ktorý prístroj, takže každé číslo bolo pomenované podľa toho,
čo robí, a overené oproti replayu (`convert.INSTRUMENTS` drží výsledok; nič sa nečíta z inštalácie):

| Číslo | Názov | Overené oproti |
|---|---|---|
| 0 | indikovaná vzdušná rýchlosť, m/s | rýchlosť stopy opravená o hustotu vzduchu: korelácia 0,99 |
| 39 | rýchlosť stúpania, m/s | rýchlosť stúpania stopy: korelácia nad 0,99 |
| 40, 41 | výška, m; výška modulo 1000 | výška stopy, niekoľko metrov rozdiel |
| 52, 53 | umelý horizont, náklon a sklon | mínus náklon a sklon z tabuľky, do 1 stupňa rozdiel |
| 64 | kompas | smer z tabuľky, do 0,1 stupňa rozdiel |
| 15-20 | pedále kormidla | bočná sila na lietadlo |
| 23, 31 | páka: výškovka a krídelká (znamienko ako v modeli kokpitu) | uhol nábehu; rýchlosť náklonu |
| 69, 71, 73 | hodiny: hodiny (12-hodinový ciferník), minúty, sekundy | miestny čas nahrávacieho počítača, na minútu presne |
| 75 | tlak v sacom potrubí, atm | vyšší pri bojovom núdzovom výkone než pri plnom plyne |
| 81-86, 87-92, 93-98 | otáčky na motor, otáčky modulo 1000, ciferník otáčok | navzájom presne; otáčky motora: korelácia nad 0,97 |
| 195 | palivo | klesá počas výletu, pri novom odrode znova plné |
| 228-230 | nohy podvozku, 1 spustené | spustené len pri výške letísk a pristávacej rýchlosti |
| 240, 241 | plyn na motor (1,1 bojový núdzový výkon alebo prepaľovanie) | plyn zo záznamu letu |
| 330-332, 346-348 | počítadlá munície (dve rovnaké sady) | náboje z prednastavenia zbraní, klesajúce s nábojmi zo záznamu letu |
| 135, 159 | teplota oleja a hlavy valcov | pravdepodobne: stúpajú počas výletu |
| 58, 61 | guľa sklzu, ihla zákruty | pravdepodobne: nasledujú bočnú silu a rýchlosť zatáčania |
| 223 | vzduchové brzdy | pravdepodobne: nastavené len pri priblížení |
| 490-497, 500-505 | kolesové brzdy | pravdepodobne: nastavené len stojac na letisku |

Niekoľko ďalších čísel sa posiela, ktorých význam nie je známy; sú uchované v `authorInstruments.notNamed` dokumentu zápasu.

`ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` a `throttle` v tabuľke pochádzajú
z týchto, na riadkoch hráča, ktorý replay nahral: berie sa posledná správa najviac 0,2 s po vzorke.

## Záznamy letu {#flight-entries}

Každý záznam letu lietadla (typ paketu 2) nesie okrem svojej polohy a postoja:

- **Rýchlosť**: 32-bitové slovo za postojom. Bity 31, 30 a 29 sú znamienka x, y a z; potom rýchlosť v 11 bitoch po
  500/2047 m/s (zastaví sa pri 500 m/s), potom |x| a |y| ako zlomky rýchlosti po 9 bitoch, a z je to, čo robí z vektora
  jednotkový vektor. Overené oproti kroku medzi prijatými vzorkami: smer sa zhoduje do zlomku stupňa pre hráča, ktorý replay
  nahral, a do asi 2 stupňov pre ostatných; rýchlosť do 0,2 %. `selfCheck.flightEntries`.
- **Náboje na zbraň**: zoznam pred polohou, jedna položka na zbraň, najprv zostávajúce náboje. Pri hráčovi, ktorý replay
  nahral, sa rovná počítadlám kokpitu o jeden takt neskôr pri takmer každej vzorke.
- **Ovládanie a plyn**: 7 bajtov za rýchlosťou, čítané ako 14 štvorbitov. Pre hráča, ktorý replay nahral, každý takt:
  1 výškovka, 2 krídelká, 3 kormidlo (8 v pokoji), 11 plyn v pätnástinách (15 aj pre bojový núdzový výkon a
  prepaľovanie), 4 kolesové brzdy, 5 vzduchové brzdy, 8 pravdepodobne brzdový padák. Štvorbity iných lietadiel sa menia
  len niekoľkokrát za bitku a nie sú ich ovládaním v danom čase.
- **Motory**: pre každý motor stavový bajt (0 vypnutý; 1-6 štartuje; 7 beží; 8 mŕtvy), 16-bitová hodnota len pri prepaľovaní
  (32767 plný), a bajt len potom, čo bol motor zasiahnutý. Väčšina lietadiel, ktorých motor prejde do stavu „mŕtvy“, je
  zostrelená alebo skončí do niekoľkých minút.

## Údaje odrazu {#reflection-data}

Správy 0xF02D a 0xF0AA replikujú očíslované objekty hry: pri každom objekte jeho id (horných 5 bitov druh, nižších 11 index)
a tabuľka polí. Druh 14 sú sloty hráčov (pole 2 user id a meno, 9 tím), druh 15 sú tímy (index 1 a 2):

- Pole 39 slotu drží jeho štatistiky na pevných miestach: zabitia (posun 0), zabitia spojencov (2), smrti (4), námorné
  zabitia (10), zabitia AI (12), zabitia AI pozemných jednotiek (14), asistencie (20), zóny dobytia (22), poškodenie zóny
  (24, 32-bitové), odmena za poškodenie (40, 32-bitové), úniky pred raketami (50). Pole 38 začína skóre, pole 42 je
  eskadra. Na konci bitky sa každá hodnota rovná hodnote z výsledkov pre každého hráča (`selfCheck.scoreboardVsResults`).
  Kde sa držia pozemné zabitia, nie je známe.
- Pole 7 tímu je jeho skóre: na konci sa rovná súčtu skóre jeho hráčov vo výsledkoch. Pole 3 je pravdepodobne jeho tikety.
- Každá správa posiela len polia, ktoré sa zmenili, takže `scoreboard` v dokumente zápasu uvádza štatistiky každého hráča
  a skóre každého tímu pri každej zmene.

## Odhad polohy a vyhladzovač {#dead-reckoning-and-the-smoother}

Klientský replay zaznamenáva každé lietadlo štyrikrát za sekundu, tak, ako ho klient vykreslil. Medzi aktualizáciami, ktoré
dostane pre vzdialené lietadlo, klient posúva lietadlo ďalej podľa jeho poslednej rýchlosti a otáča ho pri jeho posledných
rýchlostiach, a pri ďalšej aktualizácii ho tam preskočí. Čítané tak, ako je, stopa ide rovno, potom skočí. Nič v zázname
letu neoznačuje, ktoré vzorky boli prijaté; vzorka odhadnutá klientom sa nájde podľa toho, čím je: pokračuje v priamke
dvoch vzoriek pred ňou, v ich tempe, do 3 cm.

Koľko to znamená, závisí od bitky: v arkádových bitkach môže byť asi polovica vzoriek iných lietadiel odhadnutá, v simulátorových
bitkách len pár percent. Vyhladzovač znižuje skoky nad 15 g asi päťkrát (`selfCheck.deadReckoning`). Vlastné lietadlo hráča,
ktorý replay nahral, klient neextrapoluje a nechá sa tak, ako je.

Predvolene (`--no-smoothing` to vypne) sa stopy všetkých jednotiek okrem vlastnej jednotky hráča, ktorý replay nahral, umiestnia
tam, kde ich prijaté stavy hovoria, že boli: vzorka odhadnutá klientom ide po krivke cez prijaté vzorky pred ňou a za ňou, každá
so svojou rýchlosťou; nad 3 s sa priamka len ohne smerom k ďalšej prijatej vzorke, takže žiadna vzorka sa nepohne ďalej než
klientský preskok. Jej postoj sa otáča rovnomerne od jedného prijatého postoja k ďalšiemu. Prijaté vzorky sa vyhladia najviac
o 2 m alebo 0,04 s ich rýchlosti; ustálená zákruta ostane, aká je. Hodnoty replaye ostanú v stĺpcoch `Raw`.

## Postoj, overený {#attitude-checked}

Na vlastnom lietadle hráča, ktorý replay nahral, sa smer hlavy zhoduje do stupňa (medián) so smerom letu, sklon do niekoľkých
stupňov so stúpavým uhlom a pri jasných zákrutách má náklon znamienko zákruty pri takmer každej vzorke: náklon z modelu letu
je ľavé krídlo nižšie kladné, tabuľka ho prevádza na pravé krídlo nižšie kladné (`selfCheck.aircraftAttitude`).
Uhly po 10 bitoch sa menia po 0,18 stupňa. Postoj pozemných jednotiek sa overuje oproti ich výstrelom ([Veže](ground.md#turrets)).

---

Súčasť [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentácia](https://holdi601.github.io/3DHeat/)). Zdroj: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
