---
title: Sådan læses et replay
nav_order: 10
lang: da
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Sådan læses et replay {#how-it-reads-a-replay}

Denne side er for dem, der vil vide, hvad konverteren læser, hvordan det blev
kontrolleret, og dermed hvor meget man kan stole på hver kolonne. Du behøver den ikke
for at konvertere replays.

Læsningen blev kontrolleret på klientreplays af arkade-luftkampe, luftsimulator- og
søslag, på serverreplays af landkampe, og, for 2025-layouterne, på de offentlige
eksempelreplays fra [wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder).
Hver kontrol sammenligner en værdi med noget, replayet selv siger på en anden, uafhængig
måde; kun metoden og overensstemmelsen gives her.

## Hvad der læses, og kontrollen {#what-is-read-and-the-check}

| Del | Status, og kontrollen |
|---|---|
| Header, kort, mission, starttidspunkt, session; resultater | hver fil |
| Missionsindstillinger (blk'en efter headeren) | tilstand, vejr, grænser, `stars` (dato, tid, sted) |
| Pakkestrøm (zlib i 2025, zstd i 2026) | hver pakke indrammet |
| Flyenheders positioner og holdning (2026-layout) | 4 samples i sekundet, ingen pakke læst forkert; headingen stemmer med færdens retning |
| Flypakker, der er foran deres tid | efter et netværkshik indeholder en klientreplays flypakke nogle gange hvert andet fly, hvor det vil stå ca. 0,75 s senere. Forspringet måles pr. pakke, og hvert fly, der er foran, får den tid, det står for (`selfCheck.flightPacketsRetimed`) |
| Dead reckoning-spring | et spring ud af en dead reckoning-kørsel måles fra den sidst modtagne tilstand, så klientens korrektioner ikke længere skærer spor over ([Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)) |
| Teleportering | et spor skæres, hvor dets enhed flytter sig længere, end den kan: først mod dens art (fly 750 m/s, landenheder og skibe 40 m/s, våben 1800 m/s), derefter mod dens eget tempo. Hvert snit listes i `trackBreaks` med sin sandsynlige årsag (genopstandelse, spillet flytter spilleren, en korrektion af en fjern enhed). Efter snittene er intet spring mellem rækker i et spor hurtigere, end dets art tillader (`selfCheck.stepSpeed`) |
| Landenheders og skibes positioner (0xF073 / 0xF074) | ingen pakke læst forkert. Heading, pitch og roll fra den 16-bit holdning: headingen stemmer med færdens retning inden for ca. 2 grader (median); pitch tæller 180/65536 grader pr. trin; med rullens fortegn vendt peger kanonens retning fra skrog og tårn på den ramte enhed for næsten hvert stridsvognsskud. Skibe ligger på vandets niveau |
| Tårne | stridsvognes tårndrejning og kanonhævning: se [Tårne](ground.md#turrets) |
| Pakkede jordhøjder | positioner pakket i 64 bit tæller deres højde fra -100 m på de fleste baner og fra vandets niveau på nogle; forskydningen måles i hvert replay ud fra enheder set i begge former (`selfCheck.packedGroundHeight`) |
| Entitetsstrøm (oprettelse, nedlæggelse) | hver oprettelse læst. Layoutet kommer fra Dagor Engines offentliggjorte kildekode; War Thunders egne komponenttyper springes over ved at finde, hvor den næste komponent starter. Hver enheds køretøjs- og spillerplads er lig dem, drab- og træfrekorderne nævner, for hver rekord kontrolleret |
| Hvem der kørte hvilken enhed, AI-enheder, skibe, landmål | fra entitetsstrømmen: hver enhed har sit køretøj og hold, hver spillers enhed sin spiller |
| Drab mod resultaterne | dødsfaldene pr. spiller er lig resultaternes; resultaterne tæller flere drab, da klienten ikke får sendt hvert drab. Et replay, der starter, efter kampen er begyndt, indeholder kun drabene efter det |
| Drab, kritiske træf, alvorlig skade | hver fil |
| Ødelagte moduler (0xF118) | enheden og delens nummer; delens navn kræver køretøjets skademodel, som ikke er i replayet |
| Våben udløst (entitetsstrøm) | udløsningspunktet ligger ca. 10-20 m (median) fra den nærmeste enhed, som tages for at være affyreren |
| Våben i flugt (0xF0DB) | missiler, raketter og bomber, hver knyttet til sin entitet |
| Bomber uden flyvedata | en bombe uden dem får sit fald beregnet fra udløsning til nedslag (tyngdekraft og modstand, en prøve hver 0,1 s, `extrapolated` sand). Kontrolleret over havet, hvor nedslagshøjden er kendt: de beregnede fald ender inden for ca. 15 m af vandet. I kampdokumentet har sådant et våben `ballisticImpact`; `counts.bombsBallistic` tæller dem |
| Spillerpladser, chat | hver fil |
| Eksplosioner, flak-udbrud, priser, detektioner, vejr, missionsobjekter | læst; positioner kontrolleret med øjnene i vieweren |
| Den optagende spillers instrumenter (0xD04A) | navngivet efter, hvad de gør: [Cockpitinstrumenter](aircraft.md#cockpit-instruments); resten under `notNamed` |
| Flyveposters andre felter | hastighed, skud, styring, motorer: [Flyveposter](aircraft.md#flight-entries) |
| Begivenhedsrækkers holdning | hver begivenhedsrække bærer sin enheds heading, pitch, roll og kigvektor på det tidspunkt |
| Spillerstatistik og holdscorer | ved kampens slutning er hver statistik lig resultaternes for hver spiller: [Reflekteringsdata](aircraft.md#reflection-data) |
| Våben- og køretøjsnavne | fra din installations engelske lokalisering; nogle skibes standardbælter og flyvepladsradarer har intet navn i spillet |
| Spillere og AI | ingen række for en resultatspiller er AI, hver række, der ikke er AI, er en resultatspillers (`selfCheck.identity`) |
| Vrag | en enheds samples efter dens død fortsætter med at komme; en landenheds eller et skibs vrag er `alive` 0, til dens entitet fjernes, og forbliver ét spor; fly holder `alive` 0 i højst 60 s (`selfCheck.wrecks`) |
| Køretøjsskift | en spillers enhed, der stadig lever, når spillerens næste enhed dukker op, afsluttes der (et køretøj, der står tilbage). `selfCheck.vehicleSwitch.twoLiveVehicles` skal være 0 |
| Kampens tilstand | [Kamptilstand](ground.md#battle-mode) |
| Fly i et 2026-serverreplay | læst i 2026-layoutet; headingen og rullens fortegn stemmer med svingene; pladsholderfly og rekognoscerings-droner bærer ingen data |
| Spillere i et serverreplay | fundet efter navn i pladserne; hver statistik er lig resultaternes (`selfCheck.players`) |
| Fly i 2025-serverreplays og version 101286 | ikke læst: deres flypakker har et andet layout |

## Meddelelser til enheder {#messages-to-units}

Hver type-4-pakke er en mpi-meddelelse fra Dagor Engines daNet: modtagerobjektets id,
derefter (når dets lave 11 bit alle er sat) objektets ext-UID, meddelelsens id og
nyttelasten. En meddelelse til en enhed bærer som sit ext-UID enhedens entitets-id,
`index << 10 | generation`. Kontrolleret: hver sådan meddelelse angiver en entitet, der
var i live på det tidspunkt.

For specialister læses meddelelserne således:

| Meddelelse | Hvad, og kontrollen |
|---|---|
| 0xF0E9 UnitHitEffects | ét projektils træf: skyderens uid og ramtepunktet i enhedens ramme (x fremad, y op, z venstre): centimeter på fly og skibe, 20/32768 m pr. trin på landenheder (tilpasset størrelsen af stridsvognstårne). `hitLocalX/Y/Z` i meter. Bliver til en `shot`-række ([Skud](hits.md#gunfire)). Angriberen i næsten hvert træf- og drabsrekord er blandt disse skytter; ramtepunkterne ligger på den side, der vender mod skytten |
| 0xF133 UnitOnExplosion | den samme skyde-uid |
| 0xF04B OnUnitDead | `dead`-rækker: hver drabsrekords offer har en inden for 2 s |
| 0xD047 FmwRpm | motorernes omdrejninger (`rpm`); stemmer med cockpittets omdrejningsmåler |
| 0xF0B1, 0xF0A0 | `gun_shot`-rækker: enkeltskud fra tung luftværn og artilleri |
| 0xF01B, 0xF01C | `fire_start`, `fire_stop`-rækker: skudserier fra 40 mm luftværnskanoner (en kanon, der skyder; en brand på et køretøj er `fire_on`, se [Brande i køretøjer](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload`-rækker |
| 0xD0FE ProjectileHitReplay | den optagende spillers egne træf og det at blive ramt, med våben og ammunition, navngivet fra installationen (`projectileHitReplays`) |
| 0xF13E, 0xF031 | et træfs visuelle effekt og en effekt afspillet på enheden; de kommer med et træf på samme enhed |
| 0xD041 | én pr. defensiv kanon på et fly, to gange i sekundet; dens indeks passer med flyvemodellens skytte-våben |
| 0xD048, 0xF117 | layout læst, betydning ukendt |
| resten (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | i meddelelses-sidecaren med deres enhed og felter |

Navnene er fællesskabets (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Også læst {#also-read}

- **Entitetsstrømsreplikering** (0x22, 0x23): pr. entitet en blok med komponentværdier:
  skibes reparationstimere, forbrugsvarers antal, ejer- og holdskift, motoroverophedning.
  Talt i `counts.replicatedComponents`; værdierne i meddelelses-sidecaren.
- **Missionsscriptets handlinger** (0xF028) og **hints** (0xF0EC): `triggers`, `hints`.
  **Missionsfremskridt** (0xF07A, 0xF07C): `missionProgress`.
- **Replay-kameraet** (0xD043): se [Kameraet](ground.md#the-camera).

## Ikke læst, og hvorfor {#not-read-and-why}

- **Entitetsmeddelelsers navne og indhold** (0x20, 0x21): klassenummeret er en plads på
  en liste, der er indbygget i spillet; det sendes ikke og står ikke i dets data. To
  læses (en enheds brande og dens slukkere); resten gemmes helt med sin entitet og
  klassenummer.
- **Andre replikerede objekter** (andre slags end spillerpladser og hold): læst og gemt,
  ikke navngivet; resultaterne har intet, de kan kontrolleres mod.
- **Andre flys styring, gas og skud**: kun opdateret nu og da; gemt i flyve-sidecaren,
  ikke i tabellen.
- **Fly i brand**: ikke fundet i nogen meddelelse; et fly i brand har ingen `fire_on`-række.
- **Udløste våbens navne**: en bombes eller raketts entitet har intet navn; drabsrekorder
  navngiver et drabs våben.
- **Skud, der missede**: et replay indeholder kun træfene.

Hver kampdokuments `counts.messageIdsNotRead` og `selfCheck` siger, hvad et nyt replay
indeholder, og hvor godt det blev læst.

---

Del af [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentation](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
