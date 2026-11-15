---
title: "Flygplan"
nav_order: 11
lang: "sv"
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Flygplan {#aircraft}

För läsare som vill veta var flygplanskolumnerna kommer ifrån och hur mycket de
kan lita på. Varje kontroll nedan jämför ett värde med något som repriserna säger
på ett andra, oberoende sätt; här anges bara metoden och överensstämmelsen.

## Instrument i cockpiten {#cockpit-instruments}

Meddelande 0xD04A skickar den inspelande spelarens mätare som par av (nummer, värde):
fyra per sekund i arkadstrider, bara ändrade värden i simulatorstrider. Numren bildar
en enda lista för alla cockpits, och en cockpit skickar de mätare dess modell har.
Spelets kod bestämmer vilket nummer som är vilken mätare, så varje nummer namngavs
efter vad det gör och kontrollerades mot repriserna (`convert.INSTRUMENTS` innehåller
resultatet; ingenting läses ur installationen):

| Nummer | Namn | Kontrollerat mot |
|---|---|---|
| 0 | visad lufthastighet, m/s | fartygets hastighet korrigerad för lufttäthet: korrelation 0,99 |
| 39 | stigningshastighet, m/s | banans stigningshastighet: korrelation över 0,99 |
| 40, 41 | höjd, m; höjd modulo 1000 | banans höjd, med några meter skillnad |
| 52, 53 | konstgjord horisonts rulle och stigning | minus tabellens rulle och stigning, under 1 grad skillnad |
| 64 | kompass | tabellens kurs, under 0,1 grad skillnad |
| 15-20 | roderpedaler | sidokraften på flygplanet |
| 23, 31 | spak: höjdroder och skevroder (tecken som cockpitmodellens) | anfallsvinkeln; rullningshastigheten |
| 69, 71, 73 | klocka: timmar (12-timmarsvisare), minuter, sekunder | inspelningsdatorns lokala tid, till minuten |
| 75 | laddtryck, atm | högre vid krigsnödeffekt än vid full gas |
| 81-86, 87-92, 93-98 | varvtal per motor, varvtal modulo 1000, varvmätare | varandra exakt; motorns varvtal: korrelation över 0,97 |
| 195 | bränsle | sjunker under ett flyguppdrag, full igen vid en återuppståndelse |
| 228-230 | landningsställens ben, 1 nere | nere bara nära flygfältens höjd och vid landningsfart |
| 240, 241 | gas per motor (1,1 vid krigsnödeffekt eller efterbrännare) | flygpostens gas |
| 330-332, 346-348 | ammunitionsräknare (två lika uppsättningar) | vapenförinställningens skott, som sjunker med flygpostens skott |
| 135, 159 | olje- och cylinderhuvudtemperatur | troligt: de stiger under ett flyguppdrag |
| 58, 61 | slirkula, svängnål | troligt: de följer sidokraften och svängningshastigheten |
| 223 | luftbroms | troligt: bara satt vid inflygning |
| 490-497, 500-505 | hjulbromsar | troligt: bara satt när flygplanet står på ett flygfält |

Några fler nummer skickas vars betydelse inte är känd; de behålls i matchdokumentets
`authorInstruments.notNamed`.

Tabellens `ias`, `vario`, `fuel`, `manifoldPressure`, `gear`,
`oilTemperature`, `headTemperature` och `throttle` kommer från dessa, på den
inspelande spelarens egna rader, med det sista meddelandet högst 0,2 s före provet.

## Flygposter {#flight-entries}

Varje flygplans flygpost (paketsort 2) bär, utöver sin position och attityd:

- **Hastighet**: ett 32-bitars ord efter attityden. Bitarna 31, 30 och 29 är tecknen
  för x, y och z; sedan farten i 11 bitar av 500/2047 m/s (den stannar vid
  500 m/s), sedan |x| och |y| som bråkdelar av farten i 9 bitar vardera, och z är det
  som gör vektorn till en enhetsvektor. Kontrollerat mot steget mellan mottagna
  mätpunkter: riktningen stämmer inom en bråkdel av en grad för den inspelande
  spelaren och inom ungefär 2 grader för alla andra; farten inom 0,2 %.
  `selfCheck.flightEntries`.
- **Skott per vapen**: en lista före positionen, ett objekt per vapen, skotten kvar
  först. Den inspelande spelarens är lika med cockpitens räknare ett tick senare för
  nästan varje mätpunkt.
- **Reglage och gas**: 7 byte efter hastigheten, lästa som 14 halvbyte. För den
  inspelande spelaren, varje tick: 1 höjdrodret, 2 skevrodret, 3 rodret (8 i vila),
  11 gasen i femtondelar (15 även för krigsnödeffekt och efterbrännare), 4 hjulbromsarna,
  5 luftbromsen, 8 troligen bromsfallskärmen. Andra flygplans halvbyte ändras bara
  några gånger under en strid och är inte deras reglage i det ögonblicket.
- **Motorer**: per motor en tillståndsbyte (0 av; 1-6 startar; 7 går; 8 död), ett
  16-bitars värde bara med efterbrännare (32767 full), och en byte bara efter att
  motorn träffats. De flesta flygplan vars motor blir "dead" dödas eller tar slut
  inom några minuter.

## Reflektionsdata {#reflection-data}

Meddelandena 0xF02D och 0xF0AA replikerar spelets numrerade objekt: per objekt dess
id (de övre 5 bitarna slaget, de låga 11 ett index) och en fälttabell. Slag 14 är
spelarplatserna (fält 2 användar-id och namn, 9 laget), slag 15 lagen (index 1 och 2):

- En platss fält 39 håller dess statistik på fasta platser: dödsfall (offset 0),
  lagkamratdödsfall (2), egna dödsfall (4), sjödödsfall (10), AI-dödsfall (12),
  AI-markdödsfall (14), assists (20), erövringszoner (22), zonskada (24, 32-bitars),
  skadeutmärkelse (40, 32-bitars), undvikna robotar (50). Fält 38 börjar med poängen,
  fält 42 är truppen. I slutet av en strid är varje värde lika med resultatens för
  varje spelare (`selfCheck.scoreboardVsResults`). Var markdödsfallen förs är inte känt.
- Ett lags fält 7 är dess poäng: i slutet är den lika med summan av dess spelares
  poäng i resultaten. Fält 3 är troligen dess biljetter.
- Varje meddelande skickar bara de fält som ändrats, så `scoreboard` i
  matchdokumentet listar varje spelares statistik och varje lags poäng vid varje ändring.

## Dead reckoning och utjämnaren {#dead-reckoning-and-the-smoother}

En klientrepris spelar in varje flygplan fyra gånger per sekund, så som klienten
ritade det. Mellan de uppdateringar den tar emot för ett avlägset flygplan flyttar
klienten det vidare längs dess senaste hastighet och vrider det med dess senaste
hastigheter, och vid nästa uppdatering ryckar den dit det. Läst som det är går en
bana rakt, och hoppar sedan. Ingenting i flygposten markerar vilka mätpunkter som
togs emot; en dead reckoning-mätpunkt känns igen på vad den är: den fortsätter den
räta linjen från de två mätpunkterna före den, i deras takt, inom 3 cm.

Hur mycket detta spelar roll beror på striden: i arkadstrider kan ungefär hälften
av de andra flygplanens mätpunkter vara dead reckoning, i simulatorstrider bara några
procent. Utjämnaren skär stegen över 15 g till ungefär en femtedel
(`selfCheck.deadReckoning`). Den inspelande spelarens eget flygplan extrapoleras inte
av klienten och lämnas som det är.

Som standard (`--no-smoothing` stänger av det) läggs banorna för alla enheter utom den
inspelande spelarens där de mottagna tillstånden säger att de var: en dead
reckoning-mätpunkt hamnar på en kurva genom de mottagna mätpunkterna före och efter
den, var och en med sin egen hastighet; över mer än 3 s böjs den räta linjen bara mot
nästa mottagna mätpunkt, så ingen mätpunkt flyttas längre än klientens egen ryckning.
Dess attityd vrids jämnt från en mottagen attityd till nästa. Mottagna mätpunkter
jämnas ut med högst 2 m eller 0,04 s av deras fart; en jämn sväng förblir som den är.
Repriens egna värden finns kvar i kolumnerna `Raw`.

## Attityd, kontrollerad {#attitude-checked}

På den inspelande spelarens eget flygplan ligger kursen inom en grad (median) från
färdriktningen, stigningen inom några grader från klättervinkeln, och i tydliga svängar
har rullen svängens tecken för nästan varje mätpunkt: flygmodellens rulle är vänster
vinge nedåt positiv, och tabellen vänder den till höger vinge nedåt positiv
(`selfCheck.aircraftAttitude`). De 10-bitars vinklarna ger steg om 0,18 grader.
Markenheternas attityd kontrolleras mot deras skott ([Torn](ground.md#turrets)).

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Källa: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
