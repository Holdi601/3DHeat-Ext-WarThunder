---
title: Kako se snimka čita
nav_order: 10
lang: hr
source: how-it-reads.md
source_hash: "ff0f78605bd1"
nav_exclude: true
search_exclude: true
---
# Kako pretvarač čita snimku {#how-it-reads-a-replay}

Ova stranica je za ljude koji žele znati što pretvarač čita, kako je to provjereno, i koliko vjerovati
svakom stupcu. Za pretvaranje snimki ne treba.

Čitanje je provjereno na snimkama klijenta zračnih arkadnih, zračnih simulacijskih i pomorskih bitaka, na
snimkama poslužitelja kopnenih bitaka i, za rasporede iz 2025., na javnim uzorcima snimki iz
[wt_replay_decoder](https://github.com/llama-for3ver/wt_replay_decoder). Svaka provjera uspoređuje vrijednost
s nečim što snimka kaže na drugi, neovisan način; ovdje su dani samo metoda i slaganje.

## Što se čita, i provjera {#what-is-read-and-the-check}

| Dio | Status i provjera |
|---|---|
| Zaglavlje, karta, misija, vrijeme početka, sesija; rezultati | svaka datoteka |
| Postavke misije (blk iza zaglavlja) | način, vrijeme, ograničenja, `stars` (datum, vrijeme, mjesto) |
| Niz paketa (zlib 2025., zstd 2026.) | svaki paket uokviren |
| Položaji i stav zrakoplova (raspored 2026.) | 4 uzorka u sekundi, nijedan nepročitan paket; smjer se slaže sa smjerom kretanja |
| Paketi leta ispred svojeg vremena | nakon zastoja mreže, paket leta snimke klijenta ponekad drži svaki drugi zrakoplov tamo gdje će biti oko 0,75 s kasnije. Prednost se mjeri po paketu, a svaki zrakoplov koji prednjači dobiva vrijeme koje predstavlja (`selfCheck.flightPacketsRetimed`) |
| Skokovi mrtvog računa | korak iz pokrenutog mrtvog računa mjeri se od zadnjeg primljenog stanja, pa klijentove korekcije više ne presijecaju putanje ([Mrtvi račun](aircraft.md#dead-reckoning-and-the-smoother)) |
| Teleportacije | putanja se presijeca tamo gdje se jedinica pomakne dalje nego što može: prvo prema svojoj vrsti (zrakoplov 750 m/s, kopno i brodovi 40 m/s, oružje 1800 m/s), zatim prema vlastitom tempu. Svaki rez je naveden u `trackBreaks` s vjerojatnim uzrokom (ponovno pojavljivanje, igra je pomaknula igrača, korekcija udaljene jedinice). Nakon rezova nijedan korak između redaka putanje nije brži nego što njegova vrsta dopušta (`selfCheck.stepSpeed`) |
| Položaji kopnenih i brodova (0xF073 / 0xF074) | nijedan paket nepročitan. Smjer, nagib i valjanje iz 16-bitnog stava: smjer se slaže sa smjerom kretanja unutar otprilike 2 stupnja (medijan); nagib broji 180/65536 stupnjeva po koraku; uz okrenut predznak valjanja, smjer topa iz trupa i tornja pokazuje na pogođenu jedinicu za gotovo svaki hitac tenka. Brodovi stoje na razini vode |
| Tornjevi | zakret tornja i nagib topa tenkova: vidi [Tornjevi](ground.md#turrets) |
| Zapakirane visine tla | položaji zapakirani u 64 bita broje visinu od -100 m na većini razina, a od razine vode na nekima; pomak se mjeri na svakoj snimci iz jedinica viđenih u oba oblika (`selfCheck.packedGroundHeight`) |
| Tok entiteta (stvaranje, uništenje) | svako stvaranje pročitano. Raspored dolazi iz objavljenog izvornog koda Dagor Enginea; vlastite vrste komponenti War Thundera preskaču se pronalaženjem gdje počinje sljedeća komponenta. Vozilo i utor igrača svake jedinice jednaki su onima koje imenuju zapisi ubojstava i pogodaka, za svaki provjereni zapis |
| Tko je vozio koju jedinicu, AI jedinice, brodovi, kopnene mete | iz toka entiteta: svaka jedinica ima svoje vozilo i tim, svaka jedinica igrača svog igrača |
| Ubojstva prema rezultatima | smrti po igraču jednake su onima iz rezultata; rezultati broje više ubojstava, jer klijent ne dobije svako ubojstvo. Snimka koja počinje nakon početka bitke drži samo ubojstva nakon toga |
| Ubojstva, kritični pogoci, teška šteta | svaka datoteka |
| Uništeni moduli (0xF118) | jedinica i broj dijela; ime dijela treba model oštećenja vozila, a njega nema u snimci |
| Ispaljeno oružje (tok entiteta) | točka ispaljivanja je oko 10-20 m (medijan) od najbliže jedinice, koja se uzima kao lanser |
| Oružje u letu (0xF0DB) | rakete, projektili i bombe, svaki vezan za svoj entitet |
| Bombe bez zapisa leta | bomba bez njih dobiva pad izračunat od ispuštanja do udara (gravitacija i otpor, uzorak svakih 0,1 s, `extrapolated` true). Provjereno nad morem, gdje je visina udara poznata: izračunati padovi završavaju unutar oko 15 m od vode. U dokumentu meča takvo oružje ima `ballisticImpact`; `counts.bombsBallistic` ih broji |
| Unosi igrača, razgovor | svaka datoteka |
| Eksplozije, rasprsnuća protuzračne vatre, nagrade, otkrivanja, vrijeme, objekti misije | pročitano; položaji provjereni okom u pregledniku |
| Instrumenti igrača koji snima (0xD04A) | imenovani prema tome što rade: [Instrumenti u kabini](aircraft.md#cockpit-instruments); ostali pod `notNamed` |
| Ostala polja unosa leta | brzina, metci, upravljanje, motori: [Unosi leta](aircraft.md#flight-entries) |
| Stav redaka događaja | svaki redak događaja nosi smjer, nagib, valjanje i vektor pogleda svoje jedinice u tom trenutku |
| Statistika igrača i bodovi timova | na kraju bitke svaka statistika jednaka je onoj iz rezultata za svakog igrača: [Podaci o refleksiji](aircraft.md#reflection-data) |
| Nazivi oružja i vozila | iz engleske lokalizacije tvoje instalacije; nekim brodovima zadani pojasevi i radari aerodroma nemaju naziv u igri |
| Igrači i AI | nijedan igrač iz rezultata nije AI, svaki redak koji nije AI je igrač iz rezultata (`selfCheck.identity`) |
| Olupine | uzorci jedinice nakon njezine smrti i dalje pristižu; olupina kopnene jedinice ili broda je `alive` 0 dok joj se entitet ne ukloni, i ostaje jedna putanja; zrakoplovi drže `alive` 0 najviše 60 s (`selfCheck.wrecks`) |
| Promjene vozila | ako je jedinica igrača još živa kad se pojavi sljedeća jedinica istog igrača, završava se tamo (ostavljeno vozilo koje stoji). `selfCheck.vehicleSwitch.twoLiveVehicles` mora biti 0 |
| Način bitke | [Način bitke](ground.md#battle-mode) |
| Zrakoplovi u poslužiteljskoj snimci 2026. | čitani u rasporedu 2026.; smjer i predznak valjanja slažu se sa zaokretima; zrakoplovi-zamjenici i izviđački dronovi nemaju podatke |
| Igrači poslužiteljske snimke | nađeni po imenu u utorima; svaka statistika jednaka je onoj iz rezultata (`selfCheck.players`) |
| Zrakoplovi u poslužiteljskim snimkama 2025. i u verziji 101286 | nepročitani: njihovi paketi leta imaju drugi raspored |

## Poruke jedinicama {#messages-to-units}

Svaki paket vrste 4 je mpi poruka Dagor Enginea daNet: id objekta primatelja, zatim (kad su mu donjih 11
bitova sve postavljeni) ext UID objekta, id poruke i teret. Poruka jedinici kao ext UID nosi id entiteta
jedinice, `index << 10 | generation`. Provjereno: svaka takva poruka imenuje entitet koji je u tom trenutku
živ.

Za stručnjake, poruke se čitaju ovako:

| Poruka | Što, i provjera |
|---|---|
| 0xF0E9 UnitHitEffects | jedan pogodak projektila: uid strijelca i točka pogotka u okviru jedinice (x naprijed, y gore, z lijevo): centimetri za zrakoplove i brodove, 20/32768 m po koraku za kopnene jedinice (prilagođeno veličini tornjeva tenkova). `hitLocalX/Y/Z` u metrima. Postaje redak `shot` ([Paljba](hits.md#gunfire)). Strijelac gotovo svakog zapisa pogotka i ubojstva nalazi se među ovima; točke pogotka leže s one strane koja gleda na strijelca |
| 0xF133 UnitOnExplosion | isti uid strijelca |
| 0xF04B OnUnitDead | retci `dead`: svaka žrtva zapisa ubojstva ima jedan unutar 2 s |
| 0xD047 FmwRpm | okretaji motora (`rpm`); slaže se s brojčanikom okretaja u kabini |
| 0xF0B1, 0xF0A0 | retci `gun_shot`: pojedinačni hici teške protuzračne vatre i topništva |
| 0xF01B, 0xF01C | retci `fire_start`, `fire_stop`: rafali 40 mm protuzračnih topova (top koji puca; požar na vozilu je `fire_on`, vidi [Požari vozila](hits.md#vehicle-fires)) |
| 0xF050, 0xF033, 0xF054, 0xF0BD, 0xD046 | retci `bailout`, `repair`, `rearm`, `bullet_rearm`, `reload` |
| 0xD0FE ProjectileHitReplay | vlastiti pogoci igrača koji snima i pogoci koje prima, s oružjem i streljivom, imenovani iz instalacije (`projectileHitReplays`) |
| 0xF13E, 0xF031 | vizualni efekt pogotka i efekt pušten na jedinici; dolaze uz pogodak na istu jedinicu |
| 0xD041 | jedna po obrambenom topu zrakoplova, dva puta u sekundi; njezini indeksi odgovaraju strijelčevim oružjima iz modela leta |
| 0xD048, 0xF117 | raspored pročitan, značenje nepoznato |
| ostalo (0xF09A, 0xD020, 0xF015, 0xF04F, ...) | u pomoćnoj datoteci poruka, s jedinicom i poljima |

Nazivi su zajednički (ShioUmiusi/WTACRP, `tools/wrpl_mpi_names.py`).

## Također se čita {#also-read}

- **Replikacija toka entiteta** (0x22, 0x23): po entitetu blok vrijednosti komponenti: tajmeri popravka brodova,
  brojevi potrošnih predmeta, promjene vlasnika i tima, pregrijavanje motora. Broji se u `counts.replicatedComponents`;
  vrijednosti su u pomoćnoj datoteci poruka.
- **Radnje skripte misije** (0xF028) i **savjeti** (0xF0EC): `triggers`, `hints`. **Napredak misije** (0xF07A, 0xF07C):
  `missionProgress`.
- **Replay kamera** (0xD043): vidi [Kamera](ground.md#the-camera).

## Nije pročitano, i zašto {#not-read-and-why}

- **Imena i tijela poruka entiteta** (0x20, 0x21): broj klase je mjesto na popisu sastavljenom u igri, nije
  poslan i nije u njezinim podacima. Dvije se čitaju (požari vozila i njihovi gasioci); ostale se čuvaju cijele
  s entitetom i brojem klase.
- **Ostali replicirani objekti** (vrste osim utora igrača i timova): pročitani i sačuvani, nenazvani; u
  rezultatima nema s čime provjeriti.
- **Kontrole, gas i metci drugih zrakoplova**: osvježavaju se samo povremeno; čuvaju se u pomoćnoj datoteci
  leta, ne u tablici.
- **Požari zrakoplova**: nisu nađeni ni u jednoj poruci; zrakoplov u plamenu nema redak `fire_on`.
- **Imena ispuštenog oružja**: entitet bombe ili rakete ne nosi ime; zapisi ubojstava imenuju oružje ubojstva.
- **Promašeni hici**: snimka drži samo pogotke.

`counts.messageIdsNotRead` i `selfCheck` svakog dokumenta meča kažu što nova snimka sadrži i koliko je dobro
pročitana.

---

Dio [3DHeata](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Izvor: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
