---
title: "Slik leser den en replay"
nav_order: 10
lang: no
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Slik leser den en replay {#how-it-reads-a-replay}

Denne siden er for folk som vil vite hva konverteren leser, hvordan det ble
kontrollert, og dermed hvor mye hver kolonne kan stoles på. Du trenger den ikke for
å konvertere replayer.

Lesingen ble kontrollert på klientreplayer fra luftarkade-, luftsimulator- og
sjøslag, på serverreplayer fra bakkeslag, og, for 2025-oppsettene, på de offentlige
eksempelreplayene til [wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder).
Hver kontroll sammenligner en verdi med noe replayen sier på en annen, uavhengig måte;
bare metoden og samsvaret er oppgitt her.

## Hva som leses, og kontrollen {#what-is-read-and-the-check}

| Del | Status, og kontrollen |
|---|---|
| Header, kart, oppdrag, starttid, økt; resultater | hver fil |
| Oppdragsinnstillinger (blk-en etter headeren) | modus, vær, grenser, `stars` (dato, tid, sted) |
| Pakkestrømmen (zlib i 2025, zstd i 2026) | hver pakke rammet inn |
| Flyposisjoner og holdning (2026-oppsettet) | 4 samples i sekundet, ingen pakke ulest; retningen stemmer med bevegelsesretningen |
| Flygepakker foran sin tid | etter en nettverkshikke har en klientreplays flygepakke noen ganger hvert annet fly der det vil være ca. 0,75 s senere. Forspranget måles per pakke, og hvert fly som går foran får tidspunktet det står for (`selfCheck.flightPacketsRetimed`) |
| Dead reckoning-hopp | et steg ut av en dead reckoning-kjøring måles fra siste mottatte tilstand, så klientens korreksjoner kutter ikke lenger spor ([Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)) |
| Teleporteringer | et spor kuttes der enheten flytter seg lenger enn den kan: først mot sin type (fly 750 m/s, bakke og skip 40 m/s, våpen 1800 m/s), deretter mot sitt eget tempo. Hvert kutt listes i `trackBreaks` med sin sannsynlige årsak (gjenoppstandelse, spillet flytter spilleren, en korreksjon av en fjern enhet). Etter kuttene er intet steg mellom rader i et spor raskere enn dets type tillater (`selfCheck.stepSpeed`) |
| Bakke- og skipsposisjoner (0xF073 / 0xF074) | ingen pakke ulest. Retning, stigning og rull fra 16-bits holdningen: retningen stemmer med bevegelsesretningen innen ca. 2 grader (median); stigningen teller 180/65536 grader per steg; med rullens fortegn snudd, peker kanonens retning fra skrog og tårn mot enheten som ble truffet for nesten hvert tankskudd. Skip ligger på vannlinjen |
| Tårn | stridsvognenes tårngir og kanonstigning: se [Tårn](ground.md#turrets) |
| Pakkede bakkehøyder | posisjoner pakket i 64 bits teller høyden fra -100 m på de fleste nivåer og fra vannlinjen på noen; forskyvningen måles på hver replay fra enheter sett i begge former (`selfCheck.packedGroundHeight`) |
| Entitetsstrømmen (opprettelse, fjerning) | hver opprettelse leses. Oppsettet kommer fra Dagor Engines publiserte kilde; War Thunders egne komponenttyper hoppes over ved å finne hvor neste komponent begynner. Kjøretøyet og spillerplassen til hver enhet er lik dem drap- og treffpostene nevner, for hver post som ble kontrollert |
| Hvem som kjørte hvilken enhet, KI-enheter, skip, bakkemål | fra entitetsstrømmen: hver enhet har sitt kjøretøy og lag, hver spillers enhet sin spiller |
| Drap mot resultatene | dødsfallene per spiller er lik resultatenes; resultatene teller flere drap, for klienten får ikke hvert drap. En replay som starter etter at slaget begynte, holder bare drapene etter det |
| Drap, kritiske treff, alvorlig skade | hver fil |
| Ødelagte moduler (0xF118) | enheten og delens nummer; delens navn krever kjøretøyets skademodell, som ikke er i replayen |
| Våpen sluppet (entitetsstrømmen) | slippunktet er ca. 10-20 m (median) fra nærmeste enhet, som tas som avfyreren |
| Våpen i flukt (0xF0DB) | missiler, raketter og bomber, hver knyttet til sin entitet |
| Bomber uten flygeposter | en bombe uten dem får sitt fall regnet ut fra slipp til nedslag (tyngdekraft og luftmotstand, en sample hvert 0,1 s, `extrapolated` true). Kontrollert over havet, der nedslagshøyden er kjent: de regnede fallene ender innen ca. 15 m fra vannet. I kampdokumentet har et slikt våpen `ballisticImpact`; `counts.bombsBallistic` teller dem |
| Spillerplasser, chat | hver fil |
| Eksplosjoner, luftvernsprengninger, utmerkelser, oppdagelser, vær, oppdragsobjekter | lest; posisjonene kontrollert med øyet i visningsprogrammet |
| Opptakspilotens instrumenter (0xD04A) | navngitt etter hva de gjør: [Cockpit-instrumenter](aircraft.md#cockpit-instruments); resten under `notNamed` |
| Flyinngangenes andre felt | hastighet, runder, kontroller, motorer: [Flyinngangene](aircraft.md#flight-entries) |
| Hendelsesrader sin holdning | hver hendelsesrad bærer sin enhets retning, stigning, rull og sikteretning på det øyeblikket |
| Spillerstatistikk og lagpoengsummer | ved slutten av slaget er hver statistikk lik resultatenes for hver spiller: [Refleksjonsdata](aircraft.md#reflection-data) |
| Våpen- og kjøretøynavn | fra din installasjons engelske lokalisering; noen skips standardbelter og flyplassradarer har ingen navn i spillet |
| Spillere og KI | ingen rad for en resultatspiller er KI, hver rad som ikke er KI er en resultatspillers (`selfCheck.identity`) |
| Vrak | et enhetssampl etter dens død fortsetter å komme; et bakkeenhets eller skips vrak er `alive` 0 til dens entitet fjernes, og forblir ett spor; fly beholder `alive` 0 i høyst 60 s (`selfCheck.wrecks`) |
| Kjøretøybytter | en spillers enhet som fortsatt lever når spillerens neste enhet dukker opp, avsluttes der (et kjøretøy som står igjen). `selfCheck.vehicleSwitch.twoLiveVehicles` må være 0 |
| Kampmodus | [Kampmodus](ground.md#battle-mode) |
| Fly i en 2026-serverreplay | leses i 2026-oppsettet; retningen og rullens fortegn stemmer med svingene; plassholderfly og rekognoseringsdroner bærer ingen data |
| Spillere i en serverreplay | funnet med navn i plassene; hver statistikk er lik resultatenes (`selfCheck.players`) |
| Fly i 2025-serverreplayer og versjon 101286 | ikke lest: deres flygepakker har et annet oppsett |

## Meldinger til enheter {#messages-to-units}

Hver type-4-pakke er en mpi-melding fra Dagor Engines daNet: id-en til mottakerens objekt,
deretter (når dens lave 11 bits alle er satt) objektets ext-UID, meldings-ID-en og nyttelasten.
En melding til en enhet bærer som sin ext-UID enhetens entitets-ID, `index << 10 | generation`.
Kontrollert: hver slik melding navngir en entitet som var levende i det øyeblikket.

For spesialister leses meldingene slik:

| Melding | Hva, og kontrollen |
|---|---|
| 0xF0E9 UnitHitEffects | ett prosjektils treff: skytterens uid og treffpunktet i enhetens ramme (x forover, y opp, z venstre): centimeter på fly og skip, 20/32768 m per steg på bakkeenheter (tilpasset størrelsen på stridsvogntårn). `hitLocalX/Y/Z` i meter. Blir til en `shot`-rad ([Skuddild](hits.md#gunfire)). Skytteren til nesten hver treff- og drapspost er blant disse skytterne; treffpunktene ligger på siden som vender mot skytteren |
| 0xF133 UnitOnExplosion | samme skytter-uid |
| 0xF04B OnUnitDead | `dead`-rader: hver drapspost sitt offer har en innen 2 s |
| 0xD047 FmwRpm | motorenes omdreininger (`rpm`); stemmer med cockpitens turteller |
| 0xF0B1, 0xF0A0 | `gun_shot`-rader: enkeltskudd fra tung luftvern og artilleri |
| 0xF01B, 0xF01C | `fire_start`, `fire_stop`-rader: skuddserier fra 40 mm luftvernkanoner (en kanon som skyter; en brann på et kjøretøy er `fire_on`, se [Kjøretøybranner](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload`-rader |
| 0xD0FE ProjectileHitReplay | opptakspilotens egne treff og treff mot seg, med våpen og ammunisjon, navngitt fra installasjonen (`projectileHitReplays`) |
| 0xF13E, 0xF031 | et treffs visuelle effekt og en effekt spilt på enheten; de kommer med et treff på samme enhet |
| 0xD041 | én per defensiv kanon på et fly, to ganger i sekundet; dens indekser stemmer med flymodellens skyttervåpen |
| 0xD048, 0xF117 | oppsettet lest, betydningen ikke kjent |
| resten (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | i meldingssidefilen med deres enhet og felt |

Navnene er fellesskapets (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Også lest {#also-read}

- **Replikering i entitetsstrømmen** (0x22, 0x23): per entitet en blokk med komponentverdier:
  skipenes reparasjonstimere, forbruksvarers antall, eier- og lagendringer, motoroverhetning. Telles i
  `counts.replicatedComponents`; verdiene i meldingssidefilen.
- **Handlinger i oppdragsskriptet** (0xF028) og **hint** (0xF0EC): `triggers`,
  `hints`. **Oppdragsfremdrift** (0xF07A, 0xF07C): `missionProgress`.
- **Replay-kameraet** (0xD043): se [Kameraet](ground.md#the-camera).

## Ikke lest, og hvorfor {#not-read-and-why}

- **Entitetsmeldingenes navn og innhold** (0x20, 0x21): klassenummeret er en plass i en liste
  kompilert inn i spillet, ikke sendt og ikke i dets data. To leses (et kjøretøys branner og
  dets slukkere); resten beholdes helt med sin entitet og klassenummer.
- **Andre replikerte objekter** (typer andre enn spillerplasser og lag): lest og beholdt, ikke
  navngitt; ingenting i resultatene å kontrollere dem mot.
- **Andre flys kontroller, gass og runder**: oppdateres bare nå og da; beholdt i flysidefilen, ikke i tabellen.
- **Flybranner**: ikke funnet i noen melding; et fly i brann har ingen `fire_on`-rad.
- **Navnene på sluppede våpen**: en bombes eller rakets entitet har ikke noe navn; drapspostene navngir våpenet i et drap.
- **Skudd som bommet**: en replay holder bare treffene.

Hver kampdokuments `counts.messageIdsNotRead` og `selfCheck` sier hva en ny replay
holder og hvor godt den ble lest.

---

Del av [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentasjon](https://holdi601.github.io/3DHeat/)). Kilde: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
