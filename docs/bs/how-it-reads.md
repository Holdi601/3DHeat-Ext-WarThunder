---
title: "Kako čita replay"
nav_order: 10
lang: "bs"
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Kako čita replay {#how-it-reads-a-replay}

Ova stranica je za ljude koji žele znati šta konverter čita, kako je to
provjereno, a time i koliko vjerovati svakoj koloni. Ne trebate je da biste
pretvarali replayeve.

Čitanje je provjereno na klijentskim replayevima zračnih arkadnih, zračnih simulatorskih i
pomorskih bitaka, na serverskim replayevima kopnenih bitaka i, za rasporede
iz 2025., na javnim uzorcima replayeva iz
[wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder).
Svaka provjera upoređuje vrijednost s nečim što replay kaže na drugi,
nezavisan način; ovdje se daju samo metoda i slaganje.

## Šta se čita i provjera {#what-is-read-and-the-check}

| Dio | Status i provjera |
|---|---|
| Zaglavlje, mapa, misija, vrijeme početka, sesija; rezultati | svaka datoteka |
| Postavke misije (blk poslije zaglavlja) | način, vrijeme, ograničenja, `stars` (datum, vrijeme, mjesto) |
| Tok paketa (zlib u 2025., zstd u 2026.) | svaki paket uokviren |
| Pozicije i stav aviona (raspored iz 2026.) | 4 uzorka u sekundi, nijedan paket nepročitan; heading se slaže sa smjerom kretanja |
| Paketi leta ispred svog vremena | poslije mrežnog zastoja, paket leta klijentskog replaya ponekad drži svaki drugi avion tamo gdje će biti oko 0,75 s kasnije. Prednost se mjeri po paketu, a svaki avion koji prednjači dobiva vrijeme koje predstavlja (`selfCheck.flightPacketsRetimed`) |
| Dead-reckoning skokovi | korak iz dead-reckoned niza mjeri se od zadnjeg primljenog stanja, pa ispravke klijenta više ne režu staze ([Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)) |
| Teleporti | staza se reže tamo gdje se njena jedinica pomjeri dalje nego što može: prvo prema njenoj vrsti (avioni 750 m/s, kopnene jedinice i brodovi 40 m/s, oružja 1800 m/s), zatim prema njenom vlastitom tempu. Svaki rez je naveden u `trackBreaks` s vjerovatnim uzrokom (respawn, igra pomjera igrača, ispravka udaljene jedinice). Poslije rezova nijedan korak između redova staze nije brži nego što njena vrsta dozvoljava (`selfCheck.stepSpeed`) |
| Pozicije kopnenih jedinica i brodova (0xF073 / 0xF074) | nijedan paket nepročitan. Heading, pitch i roll iz 16-bitnog stava: heading se slaže sa smjerom kretanja unutar oko 2 stepena (medijan); pitch broji 180/65536 stepeni po koraku; s okrenutim predznakom rolla, smjer topa iz trupa i kupole pokazuje na pogođenu jedinicu za gotovo svaki hitac tenka. Brodovi stoje na nivou vode |
| Kupole | yaw kupole i pitch topa tenkova: vidi [Kupole](ground.md#turrets) |
| Pakirane visine tla | pozicije pakirane u 64 bita broje visinu od -100 m na većini nivoa, a na nekima od nivoa vode; pomak se mjeri na svakom replayu iz jedinica viđenih u oba oblika (`selfCheck.packedGroundHeight`) |
| Tok entiteta (stvaranje, uništenje) | svako stvaranje pročitano. Raspored potiče iz objavljenog izvora Dagor Enginea; vlastiti tipovi komponenti War Thundera preskaču se nalaženjem gdje počinje sljedeća komponenta. Vozilo i igrački slot svake jedinice jednaki su onima koje imenuju zapisi ubistava i pogodaka, za svaki provjereni zapis |
| Ko je vozio koju jedinicu, AI jedinice, brodovi, kopnene mete | iz toka entiteta: svaka jedinica ima svoje vozilo i tim, jedinica svakog igrača svog igrača |
| Ubistva prema rezultatima | smrti po igraču jednake su onima iz rezultata; rezultati broje više ubistava, jer klijentu nije poslano svako ubistvo. Replay koji počinje poslije početka bitke sadrži samo ubistva poslije toga |
| Ubistva, kritični pogoci, teška oštećenja | svaka datoteka |
| Uništeni moduli (0xF118) | jedinica i broj dijela; ime dijela traži model oštećenja vozila, kojeg nema u replayu |
| Ispuštena oružja (tok entiteta) | tačka ispuštanja je oko 10-20 m (medijan) od najbliže jedinice, koja se uzima kao lanser |
| Oružja u letu (0xF0DB) | rakete, projektili i bombe, svaki vezan za svoj entitet |
| Bombe bez zapisa leta | bombi bez njih se izračuna pad od ispuštanja do udara (gravitacija i otpor, uzorak svakih 0,1 s, `extrapolated` tačno). Provjereno nad morem, gdje je visina udara poznata: izračunati padovi završavaju unutar oko 15 m od vode. U dokumentu meča takvo oružje ima `ballisticImpact`; `counts.bombsBallistic` ih broji |
| Igrački slotovi, čet | svaka datoteka |
| Eksplozije, rafali flaka, nagrade, detekcije, vrijeme, objekti misije | pročitano; pozicije provjerene okom u pregledniku |
| Instrumenti igrača koji snima (0xD04A) | imenovani prema onome što rade: [Instrumenti kokpita](aircraft.md#cockpit-instruments); ostalo pod `notNamed` |
| Ostala polja unosa leta | brzina, meci, komande, motori: [Unosi leta](aircraft.md#flight-entries) |
| Stav redova događaja | svaki red događaja nosi heading, pitch, roll i vektor pogleda svoje jedinice u tom trenutku |
| Statistike igrača i rezultati timova | na kraju bitke svaka statistika jednaka je onoj iz rezultata za svakog igrača: [Podaci refleksije](aircraft.md#reflection-data) |
| Imena oružja i vozila | iz engleske lokalizacije vaše instalacije; nekoliko zadanih pojaseva brodova i aerodromskih radara nema imena u igri |
| Igrači i AI | nijedan red igrača iz rezultata nije AI, svaki red koji nije AI pripada igraču iz rezultata (`selfCheck.identity`) |
| Olupine | uzorci jedinice poslije njene smrti i dalje dolaze; olupina kopnene jedinice ili broda ima `alive` 0 dok se njen entitet ne ukloni, i ostaje jedna staza; avioni zadržavaju `alive` 0 najviše 60 s (`selfCheck.wrecks`) |
| Promjene vozila | igračeva jedinica koja je još živa kad se pojavi sljedeća jedinica istog igrača tu se završava (vozilo ostavljeno da stoji). `selfCheck.vehicleSwitch.twoLiveVehicles` mora biti 0 |
| Način bitke | [Način bitke](ground.md#battle-mode) |
| Avioni u serverskom replayu iz 2026. | čitaju se u rasporedu iz 2026.; heading i predznak rolla slažu se sa zavojima; avioni rezervirana mjesta i izviđački dronovi ne nose podatke |
| Igrači serverskog replaya | nalaze se po imenu u slotovima; svaka statistika jednaka je onoj iz rezultata (`selfCheck.players`) |
| Avioni u serverskim replayevima iz 2025. i verzije 101286 | ne čitaju se: njihovi paketi leta imaju drugačiji raspored |

## Poruke jedinicama {#messages-to-units}

Svaki paket tipa 4 je mpi poruka daNet-a Dagor Enginea: id objekta
primaoca, zatim (kad su njegovih nižih 11 bitova svi postavljeni) ext UID
objekta, id poruke i payload. Poruka jedinici nosi kao ext UID id
entiteta jedinice, `index << 10 | generation`. Provjereno: svaka
takva poruka imenuje entitet koji je u tom trenutku živ.

Za stručnjake, poruke koje se čitaju:

| Poruka | Šta i provjera |
|---|---|
| 0xF0E9 UnitHitEffects | pogodak jednog projektila: uid strijelca i tačka pogotka u okviru jedinice (x naprijed, y gore, z lijevo): centimetri na avionima i brodovima, 20/32768 m po koraku na kopnenim jedinicama (prilagođeno veličini kupola tenkova). `hitLocalX/Y/Z` u metrima. Postaje red `shot` ([Paljba](hits.md#gunfire)). Napadač gotovo svakog zapisa pogotka i ubistva nalazi se među tim strijelcima; tačke pogotka leže na strani okrenutoj strijelcu |
| 0xF133 UnitOnExplosion | isti uid strijelca |
| 0xF04B OnUnitDead | redovi `dead`: žrtva svakog zapisa ubistva ima jedan unutar 2 s |
| 0xD047 FmwRpm | okretaji motora (`rpm`); slaže se s mjeračem okretaja u kokpitu |
| 0xF0B1, 0xF0A0 | redovi `gun_shot`: pojedinačni hici teške protivavionske artiljerije i artiljerije |
| 0xF01B, 0xF01C | redovi `fire_start`, `fire_stop`: rafali protivavionskih topova od 40 mm (top koji puca; požar na vozilu je `fire_on`, vidi [Požari vozila](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | redovi `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` |
| 0xD0FE ProjectileHitReplay | vlastiti pogoci igrača koji snima i pogoci po njemu, s oružjem i municijom, imenovani iz instalacije (`projectileHitReplays`) |
| 0xF13E, 0xF031 | vizualni efekat pogotka i efekat odigran na jedinici; dolaze uz pogodak na istoj jedinici |
| 0xD041 | jedan po odbrambenom topu aviona, dvaput u sekundi; njegovi indeksi odgovaraju naoružanju strijelaca u modelu leta |
| 0xD048, 0xF117 | raspored pročitan, značenje nije poznato |
| ostalo (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | u sidecar datoteci poruka sa svojom jedinicom i poljima |

Imena su zajednice (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Također se čita {#also-read}

- **Replikacija toka entiteta** (0x22, 0x23): po entitetu blok
  vrijednosti komponenti: mjerači vremena popravka brodova, brojevi potrošnog materijala, promjene vlasnika i tima,
  pregrijavanje motora. Broji se u `counts.replicatedComponents`; vrijednosti
  su u sidecar datoteci poruka.
- **Akcije skripte misije** (0xF028) i **napomene** (0xF0EC): `triggers`,
  `hints`. **Napredak misije** (0xF07A, 0xF07C): `missionProgress`.
- **Replay kamera** (0xD043): vidi [Kamera](ground.md#the-camera).

## Ne čita se, i zašto {#not-read-and-why}

- **Imena i tijela poruka entiteta** (0x20, 0x21): broj klase je
  mjesto na listi kompajliranoj u igru, ne šalje se i nije u njenim podacima. Dvije
  se čitaju (požari vozila i njegovi aparati za gašenje); ostale se čuvaju
  cijele s njihovim entitetom i brojem klase.
- **Ostali replicirani objekti** (vrste osim igračkih slotova i timova):
  čitaju se i čuvaju, ne imenuju; u rezultatima nema ničega s čim bi se provjerili.
- **Komande, gas i meci drugih aviona**: osvježavaju se samo
  povremeno; čuvaju se u sidecar datoteci leta, ne u tabeli.
- **Požari aviona**: ne nalaze se ni u jednoj poruci; avion koji gori nema
  red `fire_on`.
- **Imena ispuštenih oružja**: entitet bombe ili rakete ne sadrži ime;
  zapisi ubistava imenuju oružje ubistva.
- **Promašeni hici**: replay sadrži samo pogotke.

`counts.messageIdsNotRead` i `selfCheck` svakog dokumenta meča kažu šta
novi replay sadrži i koliko je dobro pročitan.

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
