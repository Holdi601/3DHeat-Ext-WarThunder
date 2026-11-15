---
title: "Kif taqra ripetizzjoni"
nav_order: 10
lang: mt
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Kif taqra ripetizzjoni {#how-it-reads-a-replay}

Din il-paġna hija għal min irid jaf x'jaqra l-konvertitur, kif ġie kkontrollat, u għalhekk
kemm wieħed jista' jafda kull kolonna. M'għandekx bżonnha biex tikkonverti ripetizzjonijiet.

Il-qari ġie kkontrollat fuq ripetizzjonijiet tal-klijent ta' battaljiet arcade tal-ajru, simulator
tal-ajru u navali, fuq ripetizzjonijiet tas-server ta' battaljiet tal-art, u, għal-layouts tal-2025,
fuq ir-ripetizzjonijiet tal-kampjun pubbliċi ta'
[wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder).
Kull kontroll iqabbel valur ma' xi ħaġa li r-ripetizzjoni tgħid b'mod ieħor, indipendenti;
hawn jingħataw biss il-metodu u l-qbil.

## X'jinqara, u l-kontroll {#what-is-read-and-the-check}

| Parti | Stat, u l-kontroll |
|---|---|
| Header, mappa, missjoni, ħin tal-bidu, sessjoni; riżultati | kull fajl |
| Settings tal-missjoni (il-blk wara l-header) | modalità, temp, limiti, `stars` (data, ħin, post) |
| Fluss tal-pakketti (zlib fl-2025, zstd fl-2026) | kull pakkett iffrejmjat |
| Pożizzjonijiet u attitudni tal-ajruplani (layout 2026) | 4 kampjuni fis-sekonda, ebda pakkett mhux moqri; l-heading jaqbel mad-direzzjoni tal-vjaġġ |
| Pakketti tat-titjira bil-quddiem fil-ħin | wara intoppu fin-netwerk, pakkett tat-titjira ta' ripetizzjoni tal-klijent xi drabi jżomm kull ajruplan ieħor fejn se jkun madwar 0.75 s wara. Il-quddiem (lead) jitkejjel għal kull pakkett, u kull ajruplan li jmexxi jingħata l-ħin li jirrappreżenta (`selfCheck.flightPacketsRetimed`) |
| Qbiżiet tad-dead-reckoning | pass minn serje dead-reckoned jitkejjel mill-aħħar stat riċevut, biex il-korrezzjonijiet tal-klijent ma jaqtgħux aktar il-mogħdijiet ([Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)) |
| Teleports | mogħdija tinqata' fejn l-unità tagħha titlaq 'il bogħod aktar milli tista': l-ewwel kontra t-tip tagħha (ajruplani 750 m/s, art u vapuri 40 m/s, armi 1800 m/s), imbagħad kontra l-pass proprju tagħha. Kull qtugħ jinkiteb f'`trackBreaks` bil-kawża probabbli tiegħu (respawn, il-logħba tċaqlaq il-plejer, korrezzjoni ta' unità 'l bogħod). Wara l-qtugħ, ebda pass bejn ir-ringieli ta' mogħdija m'huwa aktar mgħaġġel minn dak li jippermetti t-tip tagħha (`selfCheck.stepSpeed`) |
| Pożizzjonijiet tal-art u tal-vapuri (0xF073 / 0xF074) | ebda pakkett mhux moqri. Heading, pitch u roll mill-attitudni ta' 16-il bit: l-heading jaqbel mad-direzzjoni tal-vjaġġ fi ħdan madwar 2 gradi (medjan); il-pitch jgħodd 180/65536 grad għal pass; bis-sinjal tar-roll mdawwar, id-direzzjoni tal-kanun mill-iskoss u t-turret tipponta lejn l-unità li nħabtet għal kważi kull sparatura ta' tank. Il-vapuri joqogħdu fil-livell tal-ilma |
| Turrets | yaw tat-turret u pitch tal-kanun tat-tankijiet: ara [Turrets](ground.md#turrets) |
| Għoli tal-art ippakkjat | pożizzjonijiet ippakkjati f'64 bit ibatu l-għoli tagħhom minn -100 m fuq il-biċċa l-kbira tal-livelli u mil-livell tal-ilma fuq xi wħud; l-offset jitkejjel fuq kull ripetizzjoni minn unitajiet li dehru fiż-żewġ forom (`selfCheck.packedGroundHeight`) |
| Fluss tal-entitajiet (ħolqien, qerda) | kull ħolqien moqri. Il-layout jiġi mis-sors ippubblikat tad-Dagor Engine; it-tipi ta' komponenti proprji ta' War Thunder jinqabżu billi jinstab fejn jibda l-komponent li jmiss. Il-vettura u s-slot tal-plejer ta' kull unità huma ugwali għal dawk li jsemmu r-records tal-qtil u tad-daqqiet, għal kull record ikkontrollat |
| Min saq liema unità, unitajiet AI, vapuri, miri tal-art | mill-fluss tal-entitajiet: kull unità għandha l-vettura u t-tim tagħha, kull unità ta' plejer il-plejer tagħha |
| Qtil kontra r-riżultati | l-imwiet għal kull plejer huma ugwali għal dawk tar-riżultati; ir-riżultati jgħoddu aktar qtil, għax il-klijent ma jiġix mibgħut kull qtil. Ripetizzjoni li tibda wara li bdiet il-battalja żżomm biss il-qtil minn dak il-mument |
| Qtil, daqqiet kritiċi, ħsara severa | kull fajl |
| Moduli meqruda (0xF118) | l-unità u n-numru tal-parti; l-isem tal-parti jeħtieġ il-mudell tal-ħsara tal-vettura, li mhux fir-ripetizzjoni |
| Armi rilaxxati (fluss tal-entitajiet) | il-punt tar-rilaxx huwa madwar 10-20 m (medjan) mill-eqreb unità, li tittieħed bħala l-launcher |
| Armi fit-titjira (0xF0DB) | missili, rokits u bombi, kull waħda marbuta mal-entità tagħha |
| Bombi mingħajr records tat-titjira | bomba mingħajrhom tieħu l-waqgħa tagħha kkalkulata mir-rilaxx sal-impatt (gravità u drag, kampjun kull 0.1 s, `extrapolated` veru). Ikkontrollat fuq il-baħar, fejn l-għoli tal-impatt huwa magħruf: il-waqgħat ikkalkulati jispiċċaw fi ħdan madwar 15 m mill-ilma. Fid-dokument tal-partita arma bħal din għandha `ballisticImpact`; `counts.bombsBallistic` jgħoddhom |
| Slots tal-plejers, chat | kull fajl |
| Splużjonijiet, bursts tal-flak, premjijiet, detezzjonijiet, temp, oġġetti tal-missjoni | moqrija; il-pożizzjonijiet ikkontrollati bl-għajn fil-viewer |
| L-istrumenti tal-plejer li rreġistra (0xD04A) | imsemmija skont dak li jagħmlu: [Strumenti tal-cockpit](aircraft.md#cockpit-instruments); il-bqija taħt `notNamed` |
| Kampi oħra tad-daħliet tat-titjira | veloċità, rawnds, kontrolli, magni: [Daħliet tat-titjira](aircraft.md#flight-entries) |
| Attitudni tar-ringieli tal-avvenimenti | kull ringiela ta' avveniment iġġorr l-heading, il-pitch, ir-roll u l-vettur tal-ħarsa tal-unità tagħha f'dak il-mument |
| Statistika tal-plejers u punti tat-timijiet | fi tmiem il-battalja kull statistika hija ugwali għal dik tar-riżultati għal kull plejer: [Reflection data](aircraft.md#reflection-data) |
| Ismijiet tal-armi u tal-vetturi | mil-lokalizzazzjoni Ingliża tal-installazzjoni tiegħek; ftit belts default ta' vapuri u radars ta' ajrudromi m'għandhomx isem fil-logħba |
| Plejers u AI | ebda ringiela ta' plejer tar-riżultati mhi AI, kull ringiela mhux AI hija ta' plejer tar-riżultati (`selfCheck.identity`) |
| Wrecks | il-kampjuni ta' unità wara l-mewt tagħha jibqgħu jiġu; wreck ta' unità tal-art jew vapur huwa `alive` 0 sakemm tinqered l-entità tiegħu, u jibqa' mogħdija waħda; l-ajruplani jżommu `alive` 0 għal mhux aktar minn 60 s (`selfCheck.wrecks`) |
| Bidliet ta' vettura | unità ta' plejer li għadha ħajja meta tidher l-unità li jmiss tal-istess plejer tispiċċa hemm (vettura mħallija wieqfa). `selfCheck.vehicleSwitch.twoLiveVehicles` irid ikun 0 |
| Battle mode | [Battle mode](ground.md#battle-mode) |
| Ajruplani f'ripetizzjoni tas-server tal-2026 | moqrija fil-layout tal-2026; l-heading u s-sinjal tar-roll jaqblu mad-dawriet; ajruplani placeholder u drones tar-rikonoxximent ma jġorru ebda dejta |
| Plejers ta' ripetizzjoni tas-server | misjuba bl-isem fis-slots; kull statistika hija ugwali għal dik tar-riżultati (`selfCheck.players`) |
| Ajruplani f'ripetizzjonijiet tas-server tal-2025 u verżjoni 101286 | mhux moqrija: il-pakketti tat-titjira tagħhom għandhom layout differenti |

## Messaġġi lil unitajiet {#messages-to-units}

Kull pakkett tat-tip 4 huwa messaġġ mpi tad-daNet tad-Dagor Engine: l-id tal-oġġett riċevitur, imbagħad
(meta l-11-il bit baxx tiegħu huma kollha mqiegħda) l-ext UID tal-oġġett, l-id tal-messaġġ u l-payload.
Messaġġ lil unità iġorr bħala ext UID tiegħu l-id tal-entità tal-unità, `index << 10 | generation`. Ikkontrollat:
kull messaġġ bħal dan isemmi entità ħajja f'dak il-mument.

Għall-ispeċjalisti, il-messaġġi moqrija:

| Messaġġ | X'inhu, u l-kontroll |
|---|---|
| 0xF0E9 UnitHitEffects | daqqa ta' projettil wieħed: l-uid tax-xutter u l-punt tad-daqqa fil-qafas tal-unità (x 'il quddiem, y 'il fuq, z lejn ix-xellug): ċentimetri fuq ajruplani u vapuri, 20/32768 m għal pass fuq unitajiet tal-art (imqabbad mad-daqs tat-turrets tat-tankijiet). `hitLocalX/Y/Z` f'metri. Isir ringiela `shot` ([Sparar](hits.md#gunfire)). L-attakkant ta' kważi kull record ta' daqqa u ta' qtil huwa fost dawn ix-xutters; il-punti tad-daqqa jinsabu fuq in-naħa li tħares lejn ix-xutter |
| 0xF133 UnitOnExplosion | l-istess uid tax-xutter |
| 0xF04B OnUnitDead | ringieli `dead`: il-vittma ta' kull record ta' qtil għandha waħda fi ħdan 2 s |
| 0xD047 FmwRpm | ir-rpm tal-magni (`rpm`); jaqbel mal-gauge tar-rpm tal-cockpit |
| 0xF0B1, 0xF0A0 | ringieli `gun_shot`: sparaturi singli ta' AA tqila u artillerija |
| 0xF01B, 0xF01C | ringieli `fire_start`, `fire_stop`: sensiliet ta' kanuni AA ta' 40 mm (kanun qed jispara; nar fuq vettura huwa `fire_on`, ara [Nirien tal-vetturi](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | ringieli `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` |
| 0xD0FE ProjectileHitReplay | id-daqqiet tal-plejer li rreġistra stess u meta ġie milqut, bl-arma u l-munizzjon, bl-ismijiet mill-installazzjoni (`projectileHitReplays`) |
| 0xF13E, 0xF031 | effett viżiv ta' daqqa u effett imdoqq fuq l-unità; jiġu b'daqqa fuq l-istess unità |
| 0xD041 | wieħed għal kull kanun difensiv ta' ajruplan, darbtejn fis-sekonda; l-indiċi tiegħu jaqblu mal-armi tal-gunners tal-flight model |
| 0xD048, 0xF117 | layout moqri, tifsira mhux magħrufa |
| il-bqija (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | fis-sidecar tal-messaġġi bl-unità u l-kampi tagħhom |

L-ismijiet huma tal-komunità (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Moqri wkoll {#also-read}

- **Replikazzjoni tal-fluss tal-entitajiet** (0x22, 0x23): għal kull entità blokk ta' valuri ta'
  komponenti: timers tat-tiswija tal-vapuri, għadd ta' consumables, bidliet ta' sid u ta' tim,
  sħana żejda tal-magna. Għadd f'`counts.replicatedComponents`; il-valuri fis-sidecar tal-messaġġi.
- **Azzjonijiet tal-iscript tal-missjoni** (0xF028) u **hints** (0xF0EC): `triggers`,
  `hints`. **Progress tal-missjoni** (0xF07A, 0xF07C): `missionProgress`.
- **Il-kamera tar-ripetizzjoni** (0xD043): ara [Il-kamera](ground.md#the-camera).

## Mhux moqri, u għaliex {#not-read-and-why}

- **Ismijiet u korpi ta' messaġġi tal-entitajiet** (0x20, 0x21): in-numru tal-klassi huwa
  post f'lista kkumpilata fil-logħba, mhux mibgħut u mhux fid-dejta tagħha. Tnejn
  jinqraw (in-nirien ta' vettura u l-estinguituri tagħha); il-bqija jinżammu
  sħaħ bl-entità u n-numru tal-klassi tagħhom.
- **Oġġetti replikati oħra** (tipi għajr slots tal-plejers u timijiet):
  moqrija u miżmuma, mhux imsemmija; xejn fir-riżultati biex jiġu kkontrollati miegħu.
- **Kontrolli, throttle u rawnds ta' ajruplani oħra**: jiġu aġġornati biss kultant;
  miżmuma fis-sidecar tat-titjira, mhux fit-tabella.
- **Nirien ta' ajruplani**: ma nstabu f'ebda messaġġ; ajruplan fin-nar m'għandu
  ebda ringiela `fire_on`.
- **Ismijiet ta' armi rilaxxati**: l-entità ta' bomba jew rokit ma żżomm ebda isem;
  ir-records tal-qtil isemmu l-arma ta' qtil.
- **Sparaturi li tilfu**: ripetizzjoni żżomm id-daqqiet biss.

Il-`counts.messageIdsNotRead` u s-`selfCheck` ta' kull dokument tal-partita jgħidu x'iżomm
ripetizzjoni ġdida u kemm ġiet moqrija tajjeb.

---

Parti mid-[3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentazzjoni](https://holdi601.github.io/3DHeat/)). Sors: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
