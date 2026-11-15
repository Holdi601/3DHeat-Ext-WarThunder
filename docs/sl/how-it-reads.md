---
title: Kako bere posnetek
nav_order: 10
lang: "sl"
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Kako bere posnetek {#how-it-reads-a-replay}

Ta stran je za ljudi, ki želijo vedeti, kaj pretvornik prebere, kako je bilo to preverjeno in s tem, kako zaupanja
vredna je vsak stolpec. Za pretvarjanje posnetkov je ne potrebujete.

Branje je bilo preverjeno na posnetkih odjemalca arkadnih in simulatorskih letalskih bitk ter pomorskih bitk, na
strežniških posnetkih kopenskih bitk in, za postavitve iz leta 2025, na javnih vzorčnih posnetkih
[wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder). Vsako preverjanje primerja vrednost z nečim,
kar posnetek pove na drugi, neodvisen način; tukaj sta podani samo metoda in skladnost.

## Kaj se bere in preverjanje {#what-is-read-and-the-check}

| Del | Stanje in preverjanje |
|---|---|
| Glava, zemljevid, misija, čas začetka, seja; rezultati | vsaka datoteka |
| Nastavitve misije (blk za glavo) | način, vreme, omejitve, `stars` (datum, čas, kraj) |
| Tok paketov (zlib v 2025, zstd v 2026) | vsak paket uokviren |
| Položaji letal in drža (postavitev 2026) | 4 vzorci na sekundo, noben paket ni neprebran; smer se ujema s smerjo leta |
| Paketi letenja pred svojim časom | po mrežni zatiki vsebuje paket letenja posnetka odjemalca včasih vsako drugo letalo tam, kjer bo okoli 0,75 s pozneje. Prednost se meri na vsakem paketu, vsako letalo, ki prehiteva, pa dobi čas, ki ga predstavlja (`selfCheck.flightPacketsRetimed`) |
| Skoki mrtvega računanja | korak iz teka z mrtvim računanjem se meri od zadnjega prejetega stanja, zato odjemalčni popravki ne prekinjajo več poti ([Mrtvo računanje](aircraft.md#dead-reckoning-and-the-smoother)) |
| Teleportacije | pot se prekine tam, kjer se njena enota premakne dlje, kot lahko: najprej glede na njeno vrsto (letala 750 m/s, kopenske enote in ladje 40 m/s, orožja 1800 m/s), nato glede na lastni tempo. Vsak prerez je naveden v `trackBreaks` z verjetnim vzrokom (ponovni pojav, igra premakne igralca, popravek oddaljene enote). Po prerezih noben korak med vrsticami poti ni hitrejši, kot ga dovoli njena vrsta (`selfCheck.stepSpeed`) |
| Položaji kopenskih enot in ladij (0xF073 / 0xF074) | noben paket ni neprebran. Smer, naklon in zvitek iz 16-bitne drže: smer se ujema s smerjo leta znotraj približno 2 stopinj (mediana); naklon šteje 180/65536 stopinje na korak; ob obrnjenem predznaku zvitka smer topa glede na trup in stolp kaže na enoto, ki je zadeta, pri skoraj vsakem strelu tanka. Ladje ležijo na nivoju vode |
| Stolpi | vodoravni kot stolpa tankov in naklon topa: glejte [Strelski stolpi](ground.md#turrets) |
| Zapakirane višine na kopnem | položaji, zapakirani v 64 bitov, štejejo višino od -100 m na večini zemljevidov in od nivoja vode na nekaterih; odmik se izmeri na vsakem posnetku z enotami, ki so vidne v obeh oblikah (`selfCheck.packedGroundHeight`) |
| Tok entitet (nastanek, uničenje) | vsak nastanek prebran. Postavitev izhaja iz objavljene izvorne kode Dagor Engine; lastne vrste komponent War Thunder se preskočijo z iskanjem, kje se začne naslednja komponenta. Vozilo in reža igralca vsake enote sta enaka tistima, ki ju navajajo zapisi ubijanj in zadetkov, za vsak preverjen zapis |
| Kdo je vozil katero enoto, enote AI, ladje, tarče na kopnem | iz toka entitet: vsaka enota ima svoje vozilo in ekipo, enota vsakega igralca pa svojega igralca |
| Ubijanja glede na rezultate | smrti na igralca so enake tistim iz rezultatov; rezultati štejejo več ubijanj, ker odjemalcu ni poslano vsako ubijanje. Posnetek, ki se začne po začetku bitke, vsebuje samo ubijanja po tem |
| Ubijanja, kritični zadetki, huda poškodba | vsaka datoteka |
| Uničeni moduli (0xF118) | enota in številka dela; ime dela potrebuje model poškodb vozila, ki ni v posnetku |
| Izpuščena orožja (tok entitet) | točka izpusta je približno 10-20 m (mediana) od najbližje enote, ki se vzame kot izstreljevalec |
| Orožja v letu (0xF0DB) | rakete, izstrelki vodenega orožja in bombe, vsako povezano z njegovo entiteto |
| Bombe brez zapisov leta | bomba brez njih dobi svoj padec izračunan od izpusta do udarca (gravitacija in upor, vzorec na 0,1 s, `extrapolated` true). Preverjeno nad morjem, kjer je višina udarca znana: izračunani padci končajo znotraj približno 15 m od vode. V dokumentu tekme ima tako orožje `ballisticImpact`; `counts.bombsBallistic` jih šteje |
| Vnosi igralcev, klepet | vsaka datoteka |
| Eksplozije, rafali protiletalskih topov, nagrade, zaznavanja, vreme, predmeti misije | prebrani; položaji preverjeni z očesom v pregledovalniku |
| Instrumenti igralca, ki je snemal (0xD04A) | poimenovani po tem, kaj počnejo: [Instrumenti v kabini](aircraft.md#cockpit-instruments); ostali pod `notNamed` |
| Ostala polja vnosov letenja | hitrost, naboji, krmiljenje, motorji: [Vnosi letenja](aircraft.md#flight-entries) |
| Drža v vrsticah dogodkov | vsaka vrstica dogodka nosi smer, naklon, zvitek in vektor pogleda svoje enote v tistem trenutku |
| Statistika igralcev in rezultati ekip | ob koncu bitke je vsaka statistika za vsakega igralca enaka tisti iz rezultatov: [Podatki o refleksiji](aircraft.md#reflection-data) |
| Imena orožij in vozil | iz angleške lokalizacije vaše namestitve; nekateri privzeti pasovi ladij in radarji letališč nimajo imena v igri |
| Igralci in AI | nobena vrstica igralca iz rezultatov ni AI, vsaka vrstica, ki ni AI, pa je igralca iz rezultatov (`selfCheck.identity`) |
| Olupine | vzorci enote po njeni smrti še naprej prihajajo; olupina kopenske enote ali ladje je `alive` 0, dokler ji entiteta ni odstranjena, in ostane ena pot; letala ohranijo `alive` 0 največ 60 s (`selfCheck.wrecks`) |
| Menjave vozil | enota igralca, ki je še živa, ko se pojavi naslednja enota istega igralca, se tam konča (vozilo, ki je ostalo stati). `selfCheck.vehicleSwitch.twoLiveVehicles` mora biti 0 |
| Način bitke | [Način bitke](ground.md#battle-mode) |
| Letala v strežniškem posnetku iz leta 2026 | prebrana v postavitvi 2026; smer in predznak zvitka se ujemata z zavoji; nadomestna letala in izvidniški droni ne nosijo podatkov |
| Igralci strežniškega posnetka | najdeni po imenu v režah; vsaka statistika je enaka tisti iz rezultatov (`selfCheck.players`) |
| Letala v strežniških posnetkih iz leta 2025 in različici 101286 | niso prebrana: njihovi paketi letenja imajo drugačno postavitev |

## Sporočila enotam {#messages-to-units}

Vsak paket tipa 4 je sporočilo mpi iz daNet Dagor Engine: id predmeta prejemnika, nato (kadar so vsi njegovi spodnji
11 bitov nastavljeni) razširjeni UID predmeta, id sporočila in tovor. Sporočilo enoti nosi kot svoj razširjeni UID
identifikator entitete enote, `index << 10 | generation`. Preverjeno: vsako tako sporočilo navaja entiteto, ki je
živa v tistem trenutku.

Za strokovnjake sporočila, ki se preberejo:

| Sporočilo | Kaj in preverjanje |
|---|---|
| 0xF0E9 UnitHitEffects | zadetek enega izstrelka: uid strelca in točka zadetka v okviru enote (x naprej, y gor, z levo): centimetri pri letalih in ladjah, 20/32768 m na korak pri kopenskih enotah (prilagojeno velikosti stolpov tankov). `hitLocalX/Y/Z` v metrih. Postane vrstica `shot` ([Streljanje](hits.md#gunfire)). Strelec skoraj vsakega zapisa zadetka in ubijanja je med temi strelci; točke zadetkov ležijo na strani, obrnjeni proti strelcu |
| 0xF133 UnitOnExplosion | isti uid strelca |
| 0xF04B OnUnitDead | vrstice `dead`: vsak zapis ubijanja ima žrtev z eno v 2 s |
| 0xD047 FmwRpm | vrtljaji motorjev (`rpm`); ujema se z merilnikom vrtljajev v kabini |
| 0xF0B1, 0xF0A0 | vrstice `gun_shot`: posamezni streli težkih protiletalskih in artilerijskih topov |
| 0xF01B, 0xF01C | vrstice `fire_start`, `fire_stop`: rafali 40 mm protiletalskih topov (top streljanje; ogenj na vozilu je `fire_on`, glejte [Požari vozil](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | vrstice `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` |
| 0xD0FE ProjectileHitReplay | lastni zadetki igralca, ki je snemal, in zadetki nanj, z orožjem in strelivom, poimenovani iz namestitve (`projectileHitReplays`) |
| 0xF13E, 0xF031 | vizualni učinek zadetka in učinek, predvajan na enoti; prideta z zadetkom na isto enoto |
| 0xD041 | eno za vsak obrambni top letala, dvakrat na sekundo; njegovi indeksi ustrezajo strelskim orožjem modela leta |
| 0xD048, 0xF117 | postavitev prebrana, pomen ni znan |
| ostalo (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | v spremljevalni datoteki sporočil z njihovo enoto in polji |

Imena so skupnosti (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Prav tako prebrano {#also-read}

- **Replikacija toka entitet** (0x22, 0x23): za entiteto blok vrednosti komponent: časovniki popravil ladij, števci
  potrošnega materiala, spremembe lastnika in ekipe, pregrevanje motorja. Šteje se v `counts.replicatedComponents`;
  vrednosti so v spremljevalni datoteki sporočil.
- **Dejanja skripte misije** (0xF028) in **namigi** (0xF0EC): `triggers`, `hints`. **Napredek misije** (0xF07A, 0xF07C):
  `missionProgress`.
- **Nadomestna kamera** (0xD043): glejte [Kamera](ground.md#the-camera).

## Ni prebrano in zakaj {#not-read-and-why}

- **Imena in telesa sporočil entitet** (0x20, 0x21): številka razreda je mesto na seznamu, sestavljenem v igri; ni
  poslana in ni v njenih podatkih. Dva se prebereta (ogenj vozila in njegovi gasilniki); ostali se ohranijo celi z
  njihovo entiteto in številko razreda.
- **Drugi replicirani predmeti** (vrste, razen rež igralcev in ekip): prebrani in ohranjeni, neimenovani; v rezultatih ni
  ničesar, s čimer bi jih preverili.
- **Druge kontrole, plin in naboji letal drugih**: osvežujejo se le občasno; shranjeni so v spremljevalni datoteki letenja,
  ne v tabeli.
- **Požari letal**: v nobenem sporočilu niso najdeni; letalo v ognju nima vrstice `fire_on`.
- **Imena izpuščenih orožij**: entiteta bombe ali rakete nima imena; zapisi ubijanj imenujejo orožje ubijanja.
- **Streli, ki so zgrešili**: posnetek hrani samo zadetke.

Vsak `counts.messageIdsNotRead` in `selfCheck` dokumenta tekme povesta, kaj vsebuje nov posnetek in kako dobro je bil
prebran.

---

Del [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Vir: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
