---
title: "Hvernig upptaka er lesin"
nav_order: 10
lang: is
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Hvernig upptaka er lesin {#how-it-reads-a-replay}

Þessi síða er fyrir fólk sem vill vita hvað breytirinn les, hvernig það var
athugað, og þar með hversu mikið má treysta hverjum dálki. Þú þarft hana ekki
til að breyta upptökum.

Lesturinn var athugaður á biðlaraupptökum af loft-arcade-, loft-simulator- og
sjóbardögum, á þjónsupptökum af landbardögum, og, fyrir 2025 útlitið, á
opinberu sýnishornsupptökunum frá
[wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder).
Hver athugun ber gildi saman við eitthvað sem upptakan segir á annan, óháðan
hátt; aðeins aðferðin og samræmið er gefið hér.

## Hvað er lesið, og athugunin {#what-is-read-and-the-check}

| Hluti | Staða, og athugunin |
|---|---|
| Haus, kort, verkefni, upphafstími, lota; niðurstöður | hver skrá |
| Verkefnisstillingar (blk á eftir hausnum) | hamur, veður, mörk, `stars` (dagsetning, tími, staður) |
| Pakkastraumur (zlib í 2025, zstd í 2026) | hver pakki rammaður |
| Staða og afstaða flugvéla (2026 útlit) | 4 sýni á sekúndu, enginn pakki ólesinn; heading stemmir við stefnu ferðar |
| Flugpakkar á undan tíma sínum | eftir nethökt geymir flugpakki biðlaraupptöku stundum hverja aðra flugvél þar sem hún verður um 0,75 s síðar. Forskotið er mælt fyrir hvern pakka, og hver flugvél sem er á undan fær þann tíma sem hún stendur fyrir (`selfCheck.flightPacketsRetimed`) |
| Kippir vegna ágiskunar (dead reckoning) | skref út úr runu ágiskana er mælt frá síðasta móttekna ástandi, svo leiðréttingar biðlarans skera ekki lengur ferla ([Ágiskun á stöðu](aircraft.md#dead-reckoning-and-the-smoother)) |
| Fjarflutningar (teleports) | ferill er skorinn þar sem eining hans færist lengra en hún getur: fyrst gegn tegund hennar (flugvélar 750 m/s, land og skip 40 m/s, vopn 1800 m/s), svo gegn eigin hraða hennar. Hver skurður er talinn upp í `trackBreaks` með líklegri orsök (endurkoma, leikurinn færir spilarann, leiðrétting fjarlægrar einingar). Eftir skurðina er ekkert skref milli raða ferils hraðara en tegundin leyfir (`selfCheck.stepSpeed`) |
| Staða lands og skipa (0xF073 / 0xF074) | enginn pakki ólesinn. Heading, pitch og roll úr 16 bita afstöðu: heading stemmir við stefnu ferðar innan um 2 gráða (miðgildi); pitch telur 180/65536 gráður á skref; með formerki roll snúið bendir stefna byssunnar úr skrokki og turni á eininguna sem varð fyrir höggi fyrir nær hvert skriðdrekaskot. Skip sitja í sjávarmáli |
| Turnar | snúningur turns og halli byssu skriðdreka: sjá [Turnar](ground.md#turrets) |
| Pökkuð landhæð | stöður pakkaðar í 64 bita telja hæð sína frá -100 m á flestum borðum og frá sjávarmáli á sumum; frávikið er mælt á hverri upptöku úr einingum sem sjást í báðum myndum (`selfCheck.packedGroundHeight`) |
| Einingastraumur (sköpun, eyðing) | hver sköpun lesin. Útlitið kemur úr útgefnum frumkóða Dagor Engine; eigin íhlutategundir War Thunder eru sniðgengnar með því að finna hvar næsti íhlutur byrjar. Farartæki og spilararauf hverrar einingar eru þau sömu og dráps- og höggfærslur nefna, fyrir hverja færslu sem var athuguð |
| Hver stýrði hvaða einingu, AI-einingar, skip, skotmörk á landi | úr einingastraumnum: hver eining hefur farartæki sitt og lið, eining hvers spilara spilara sinn |
| Dráp gegn niðurstöðunum | dauðsföll á spilara eru jöfn niðurstöðunum; niðurstöðurnar telja fleiri dráp, þar sem biðlaranum eru ekki send öll dráp. Upptaka sem byrjar eftir að bardaginn hófst geymir aðeins drápin eftir það |
| Dráp, krítísk högg, mikill skaði | hver skrá |
| Eyðilagðir hlutar (0xF118) | einingin og númer hlutans; nafn hlutans krefst skaðamódels farartækisins, sem er ekki í upptökunni |
| Vopnum sleppt (einingastraumur) | losunarpunkturinn er um 10-20 m (miðgildi) frá næstu einingu, sem er tekin sem sú sem skaut |
| Vopn á flugi (0xF0DB) | flugskeyti, eldflaugar og sprengjur, hvert bundið einingu sinni |
| Sprengjur án flugfærslna | sprengja án þeirra fær fall sitt reiknað frá losun til höggs (þyngdarafl og viðnám, sýni á 0,1 s fresti, `extrapolated` satt). Athugað yfir sjó, þar sem hæð höggsins er þekkt: útreiknuð föll enda innan um 15 m frá vatninu. Í leikjaskjalinu hefur slíkt vopn `ballisticImpact`; `counts.bombsBallistic` telur þau |
| Spilararaufar, spjall | hver skrá |
| Sprengingar, flak-sprengingar, verðlaun, greiningar, veður, verkefnishlutir | lesið; stöður athugaðar með auga í skoðaranum |
| Mælar upptökumannsins (0xD04A) | nefndir eftir því sem þeir gera: [Mælar í stjórnklefa](aircraft.md#cockpit-instruments); hitt undir `notNamed` |
| Aðrir reitir flugfærslna | hraði, skot, stýri, hreyflar: [Færslur flugmódels](aircraft.md#flight-entries) |
| Afstaða atburðaraða | hver atburðarröð ber heading, pitch, roll og sjónstefnuvigur einingar sinnar á þeirri stundu |
| Tölfræði spilara og stig liða | í lok bardaga er hver tölfræði jöfn niðurstöðunum fyrir hvern spilara: [Speglunargögn](aircraft.md#reflection-data) |
| Nöfn vopna og farartækja | úr ensku staðfæringu þinnar uppsetningar; sjálfgefin skotbelti sumra skipa og ratsjár flugvalla hafa ekkert nafn í leiknum |
| Spilarar og AI | engin röð spilara úr niðurstöðunum er AI, hver röð sem er ekki AI er spilara úr niðurstöðunum (`selfCheck.identity`) |
| Flök | sýni einingar eftir dauða hennar halda áfram að berast; flak landeiningar eða skips er `alive` 0 þar til eining þess er fjarlægð, og helst einn ferill; flugvélar halda `alive` 0 í mesta lagi 60 s (`selfCheck.wrecks`) |
| Skipti á farartækjum | eining spilara sem er enn lifandi þegar næsta eining sama spilara birtist er endað þar (farartæki skilið eftir standandi). `selfCheck.vehicleSwitch.twoLiveVehicles` verður að vera 0 |
| Bardagahamur | [Bardagahamur](ground.md#battle-mode) |
| Flugvélar í 2026 þjónsupptöku | lesnar í 2026 útlitinu; heading og formerki roll stemma við beygjurnar; staðgengilsflugvélar og könnunardrónar bera engin gögn |
| Spilarar þjónsupptöku | fundnir eftir nafni í raufunum; hver tölfræði er jöfn niðurstöðunum (`selfCheck.players`) |
| Flugvélar í 2025 þjónsupptökum og útgáfu 101286 | ekki lesnar: flugpakkar þeirra hafa annað útlit |

## Skilaboð til eininga {#messages-to-units}

Hver pakki af gerð 4 eru mpi-skilaboð úr daNet í Dagor Engine: auðkenni
viðtökuhlutarins, svo (þegar lægstu 11 bitar hans eru allir stilltir) ext UID
hlutarins, auðkenni skilaboða og farmurinn. Skilaboð til einingar bera sem ext
UID hennar einingarauðkenni einingarinnar, `index << 10 | generation`.
Athugað: hver slík skilaboð nefna einingu sem er lifandi á þeirri stundu.

Fyrir sérfræðinga, skilaboðin sem eru lesin:

| Skilaboð | Hvað, og athugunin |
|---|---|
| 0xF0E9 UnitHitEffects | högg eins skots: uid skyttunnar og höggpunkturinn í ramma einingarinnar (x fram, y upp, z vinstri): sentímetrar á flugvélum og skipum, 20/32768 m á skref á landeiningum (aðlagað stærð turna skriðdreka). `hitLocalX/Y/Z` í metrum. Verður `shot` röð ([Skothríð](hits.md#gunfire)). Árásarmaður nær hverrar högg- og drápsfærslu er meðal þessara skytta; höggpunktarnir liggja þeim megin sem snýr að skyttunni |
| 0xF133 UnitOnExplosion | sama uid skyttunnar |
| 0xF04B OnUnitDead | `dead` raðir: fórnarlamb hverrar drápsfærslu hefur eina innan 2 s |
| 0xD047 FmwRpm | snúningar hreyfla á mínútu (`rpm`); stemmir við snúningsmæli stjórnklefans |
| 0xF0B1, 0xF0A0 | `gun_shot` raðir: stök skot þungra loftvarnabyssna og stórskotaliðs |
| 0xF01B, 0xF01C | `fire_start`, `fire_stop` raðir: hrinur 40 mm loftvarnabyssna (byssa að skjóta; eldur á farartæki er `fire_on`, sjá [Eldar í farartækjum](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` raðir |
| 0xD0FE ProjectileHitReplay | eigin högg upptökumannsins og þegar hann var sleginn, með vopni og skotfærum, nefnd úr uppsetningunni (`projectileHitReplays`) |
| 0xF13E, 0xF031 | sjónræn áhrif höggs og áhrif spiluð á eininguna; þau koma með höggi á sömu einingu |
| 0xD041 | ein fyrir hverja varnarbyssu flugvélar, tvisvar á sekúndu; vísar þess passa við skyttuvopn flugmódelsins |
| 0xD048, 0xF117 | útlit lesið, merking ekki þekkt |
| hin (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | í skilaboðahliðarskránni með einingu sinni og reitum |

Nöfnin eru samfélagsins (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Einnig lesið {#also-read}

- **Afritun einingastraums** (0x22, 0x23): fyrir hverja einingu blokk af
  íhlutagildum: viðgerðartímar skipa, fjöldi birgða, eigenda- og liðabreytingar,
  ofhitnun hreyfils. Talið í `counts.replicatedComponents`; gildin í
  skilaboðahliðarskránni.
- **Aðgerðir verkefnisskriftu** (0xF028) og **ábendingar** (0xF0EC): `triggers`,
  `hints`. **Framvinda verkefnis** (0xF07A, 0xF07C): `missionProgress`.
- **Upptökumyndavélin** (0xD043): sjá [Myndavélin](ground.md#the-camera).

## Ekki lesið, og hvers vegna {#not-read-and-why}

- **Nöfn og efni einingarskilaboða** (0x20, 0x21): flokksnúmerið er staður í
  lista sem er þýddur inn í leikinn, ekki sendur og ekki í gögnum hans. Tvö eru
  lesin (eldar farartækis og slökkvitæki þess); hin eru geymd í heild með
  einingu sinni og flokksnúmeri.
- **Aðrir afritaðir hlutir** (aðrar tegundir en spilararaufar og lið): lesnir og
  geymdir, ekki nefndir; ekkert í niðurstöðunum til að athuga þá gegn.
- **Stýri, inngjöf og skot annarra flugvéla**: endurnýjað aðeins öðru hverju;
  geymt í flughliðarskránni, ekki í töflunni.
- **Eldar í flugvélum**: finnast ekki í neinum skilaboðum; flugvél í ljósum
  logum hefur enga `fire_on` röð.
- **Nöfn vopna sem var sleppt**: eining sprengju eða eldflaugar geymir ekkert
  nafn; drápsfærslur nefna vopn drápsins.
- **Skot sem geiguðu**: upptaka geymir aðeins höggin.

`counts.messageIdsNotRead` og `selfCheck` í hverju leikjaskjali segja hvað ný
upptaka geymir og hversu vel hún var lesin.

---

Hluti af [3DHeat](https://github.com/Holdi601/3DHeat) ([skjölun](https://holdi601.github.io/3DHeat/)). Frumkóði: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
