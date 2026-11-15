---
title: "Så läser den en repris"
nav_order: 10
lang: "sv"
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Så läser den en repris {#how-it-reads-a-replay}

Den här sidan är för dem som vill veta vad konverteraren läser, hur det
kontrollerades, och därmed hur mycket var kolumn kan lita på. Du behöver den inte
för att konvertera repriser.

Läsningen kontrollerades på klientrepriser av luftarkad-, luftsimulator- och
sjöstrider, på serverrepriser av markstrider, och, för 2025-layouterna, på de
publika exempelrepriserna i
[wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder).
Varje kontroll jämför ett värde med något som repriserna säger på ett andra,
oberoende sätt; här anges bara metoden och överensstämmelsen.

## Vad som läses, och kontrollen {#what-is-read-and-the-check}

| Del | Status, och kontrollen |
|---|---|
| Huvud, karta, uppdrag, starttid, session; resultat | varje fil |
| Uppdragsinställningarna (blk:en efter huvudet) | läge, väder, gränser, `stars` (datum, tid, plats) |
| Paketströmmen (zlib 2025, zstd 2026) | varje paket inramat |
| Flygplanens positioner och attityd (2026-layouten) | 4 mätpunkter per sekund, inget paket oläst; kursen stämmer med färdriktningen |
| Flygpaket före sin tid | efter ett nätverkshack innehåller ett klientrepris-flygpaket ibland varje annat flygplan där det kommer att vara ungefär 0,75 s senare. Försprånget mäts per paket, och varje flygplan som ligger före får den tid den står för (`selfCheck.flightPacketsRetimed`) |
| Dead reckoning-hopp | ett steg ur en dead reckoning-körning mäts från det sista mottagna tillståndet, så klientens korrigeringar inte längre klipper banor ([Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)) |
| Teleporteringar | en bana klipps där dess enhet rör sig längre än den kan: först mot sitt slag (flygplan 750 m/s, mark och fartyg 40 m/s, vapen 1800 m/s), sedan mot sin egen takt. Varje klipp listas i `trackBreaks` med sin sannolika orsak (återuppståndelse, spelet flyttar spelaren, en korrigering av en avlägsen enhet). Efter klippen är inget steg mellan rader i en bana snabbare än dess slag tillåter (`selfCheck.stepSpeed`) |
| Mark- och fartygspositioner (0xF073 / 0xF074) | inget paket oläst. Kurs, stigning och rulle från den 16-bitars attityden: kursen stämmer med färdriktningen inom ungefär 2 grader (median); stigningen räknas i 180/65536 grader per steg; med rullens tecken vänt pekar kanonens riktning från skrov och torn på den enhet som träffades för nästan varje stridsvagnsskott. Fartyg sitter på vattenhöjden |
| Torn | stridsvagnars tornvridning och kanonens höjd: se [Torn](ground.md#turrets) |
| Packade markhöjder | positioner packade i 64 bitar räknar sin höjd från -100 m på de flesta nivåer och från vattenhöjden på några; förskjutningen mäts på varje repris från enheter som synts i båda formerna (`selfCheck.packedGroundHeight`) |
| Entitetsströmmen (skapande, förstörelse) | varje skapande läst. Layouten kommer från Dagor Engines publicerade källkod; War Thunders egna komponenttyper hoppas över genom att hitta var nästa komponent börjar. Varje enhets fordons- och spelarplats är lika med dem som döds- och träffposterna anger, för varje post som kontrollerats |
| Vem som körde vilken enhet, AI-enheter, fartyg, markmål | ur entitetsströmmen: varje enhet har sitt fordon och lag, varje spelares enhet sin spelare |
| Dödsfall mot resultaten | dödsfallen per spelare är lika med resultatens; resultaten räknar fler dödsfall, eftersom klienten inte får varje dödsfall. En repris som startar efter att striden började håller bara dödsfallen efter det |
| Dödsfall, kritiska träffar, svår skada | varje fil |
| Förstörda moduler (0xF118) | enheten och delens nummer; delens namn kräver fordonets skademodell, som inte finns i repriser |
| Avfyrade vapen (entitetsströmmen) | släppunkten ligger ungefär 10-20 m (median) från närmaste enhet, som tas för avfyraren |
| Vapen i luften (0xF0DB) | robotar, raketer och bomber, var och en kopplad till sin entitet |
| Bomber utan flygposter | en bomb utan dem får sitt fall uträknat från släpp till nedslag (gravitation och luftmotstånd, ett prov var 0,1 s, `extrapolated` sant). Kontrollerat över havet, där nedslagshöjden är känd: de uträknade fallen slutar inom ungefär 15 m från vattnet. I matchdokumentet har ett sådant vapen `ballisticImpact`; `counts.bombsBallistic` räknar dem |
| Spelarplatser, chatt | varje fil |
| Explosioner, flak-sprängningar, utmärkelser, upptäckter, väder, uppdragsobjekt | lästa; positionerna kontrollerade för ögat i visaren |
| Den inspelande spelarens instrument (0xD04A) | namngivna efter vad de gör: [Instrument i cockpiten](aircraft.md#cockpit-instruments); resten under `notNamed` |
| Flygposternas övriga fält | hastighet, skott, reglage, motorer: [Flygposter](aircraft.md#flight-entries) |
| Händelseradernas attityd | varje händelserad bär sin enhets kurs, stigning, rulle och siktvektor just då |
| Spelarstatistik och lagpoäng | i slutet av striden är varje statistik lika med resultatens för varje spelare: [Reflektionsdata](aircraft.md#reflection-data) |
| Vapen- och fordonsnamn | från din installations engelska översättning; några fartygs standardbälten och flygfältsradarer har inget namn i spelet |
| Spelare och AI | ingen rad för en resultatspelare är AI, varje rad som inte är AI är en resultatspelares (`selfCheck.identity`) |
| Vrak | en enhets mätpunkter efter dess död fortsätter komma; en markenhets eller fartygs vrak är `alive` 0 tills dess entitet tas bort, och förblir en bana; flygplan håller `alive` 0 i högst 60 s (`selfCheck.wrecks`) |
| Fordonsbyten | en spelares enhet som fortfarande lever när samma spelares nästa enhet dyker upp avslutas där (ett fordon som står kvar). `selfCheck.vehicleSwitch.twoLiveVehicles` måste vara 0 |
| Stridsläge | [Stridsläge](ground.md#battle-mode) |
| Flygplan i en 2026-serverrepris | läst i 2026-layouten; kursen och rullens tecken stämmer med svängarna; platshållarflygplan och spaningsdrönare bär inga data |
| Spelare i en serverrepris | hittade med namn i platserna; varje statistik är lika med resultatens (`selfCheck.players`) |
| Flygplan i 2025-serverrepriser och version 101286 | inte lästa: deras flygpaket har en annan layout |

## Meddelanden till enheter {#messages-to-units}

Varje paket av typ 4 är ett mpi-meddelande i Dagor Engines daNet: mottagarobjektets
id, sedan (när dess låga 11 bitar alla är ettor) objektets ext-UID, meddelande-id:t
och nyttolasten. Ett meddelande till en enhet bär som ext-UID enhetens entitets-id,
`index << 10 | generation`. Kontrollerat: varje sådant meddelande anger en entitet
som lever i just det ögonblicket.

För specialister läses meddelandena så här:

| Meddelande | Vad, och kontrollen |
|---|---|
| 0xF0E9 UnitHitEffects | en projektils träff: skyttens uid och träffpunkten i enhetens system (x framåt, y upp, z vänster): centimeter på flygplan och fartyg, 20/32768 m per steg på markenheter (anpassat till stridsvagnstorn). `hitLocalX/Y/Z` i meter. Blir en `shot`-rad ([Beskjutning](hits.md#gunfire)). Angriparen till nästan varje träff- och dödspost är bland dessa skyttar; träffpunkterna ligger på den sida som vetter mot skytten |
| 0xF133 UnitOnExplosion | samma skyttes uid |
| 0xF04B OnUnitDead | `dead`-rader: varje dödspostens offer har en inom 2 s |
| 0xD047 FmwRpm | motorernas varvtal (`rpm`); stämmer med cockpitens varvmätare |
| 0xF0B1, 0xF0A0 | `gun_shot`-rader: enstaka skott från tung luftvärn och artilleri |
| 0xF01B, 0xF01C | `fire_start`, `fire_stop`-rader: skurar från 40 mm luftvärnskanoner (ett eldande kanon; en eld på ett fordon är `fire_on`, se [Fordonsbränder](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload`-rader |
| 0xD0FE ProjectileHitReplay | den inspelande spelarens egna träffar och att bli träffad, med vapen och ammunition, namngivna ur installationen (`projectileHitReplays`) |
| 0xF13E, 0xF031 | en träffs visuella effekt och en effekt spelad på enheten; de kommer med en träff på samma enhet |
| 0xD041 | en per defensivt kanon på ett flygplan, två gånger per sekund; dess index stämmer med flygmodellens skyttevapen |
| 0xD048, 0xF117 | layouten läst, betydelsen okänd |
| resten (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | i meddelandesidofilen med sin enhet och sina fält |

Namnen är gemenskapens (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Även lästa {#also-read}

- **Entitetsströmmens replikering** (0x22, 0x23): per entitet ett block med
  komponentvärden: fartygens reparationstimers, förbrukningsartiklars antal, ägar- och
  lagbyten, motoröverhettning. Räknas i `counts.replicatedComponents`; värdena i
  meddelandesidofilen.
- **Uppdragsskriptets åtgärder** (0xF028) och **tips** (0xF0EC): `triggers`,
  `hints`. **Uppdragsförlopp** (0xF07A, 0xF07C): `missionProgress`.
- **Repriskameran** (0xD043): se [Kameran](ground.md#the-camera).

## Inte lästa, och varför {#not-read-and-why}

- **Entitetsmeddelandens namn och innehåll** (0x20, 0x21): klassnumret är en plats
  i en lista som är kompilerad i spelet, inte skickad och inte i dess data. Två
  läses (ett fordons bränder och dess släckare); resten behålls helt med sin entitet
  och sitt klassnummer.
- **Andra replikerade objekt** (andra slag än spelarplatser och lag): lästa och
  behållna, inte namngivna; resultaten har inget att kontrollera dem mot.
- **Andra flygplans reglage, gas och skott**: uppfriskade bara då och då; behållna
  i flygsidofilen, inte i tabellen.
- **Flygplanbränder**: hittas inte i något meddelande; ett flygplan i brand har ingen
  `fire_on`-rad.
- **Namn på avfyrade vapen**: en bombs eller raketens entitet bär inget namn;
  dödsposterna anger vilket vapen som gav en död.
- **Skott som missade**: en repris håller bara träffarna.

Varje matchdokuments `counts.messageIdsNotRead` och `selfCheck` säger vad en ny
repris innehåller och hur väl den lästes.

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Källa: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
