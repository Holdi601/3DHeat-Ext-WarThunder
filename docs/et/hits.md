---
title: Tabamused, tulistamine ja tulekahjud
nav_order: 13
lang: "et"
source: hits.md
source_hash: "201975b2f443"
nav_exclude: true
search_exclude: true
---
# Tabamused, tulistamine ja tulekahjud {#hits-gunfire-and-fires}

Lugejatele, kes tahavad teada, kust tabamuste, laskemoona ja tulekahjude veerud pärinevad.
Kontrollid annavad ainult meetodi ja kokkulangevuse.

## Tulistamine {#gunfire}

Iga üksust tabanud projektil on kordusest olemas (sõnum 0xF0E9): rida `shot` laskja asukohas
tabamuse hetkel, `targetX/Y/Z` tabamuspunkt (tabatud üksus, nihutatud tabamispunkti võrra selle
raamistikus, pööratud tema asendi järgi), suund sinna, `other` tabatud üksus. Mööda läinud mürske
ja kuule ei saadeta: need ei ole olemid, ja lendavate relvade sõnumid hoiavad ainult rakette, juhitavaid rakette, pomme ja torpeedosid. Salvestajamängija lastud laskemoon (tema veerg `ammo`) kahaneb tema
tulistamisel, nii et tema pursud saab eristada, kuid mitte seda, kuhu need laskemoonad läksid.
Raske õhutõrje ja suurtükivägi saadavad iga üksiku lasu (`gun_shot`, suunata ei ole), 40 mm
õhutõrjekahuritel nende pursud (`fire_start`, `fire_stop`).

## Tabamuste tulemused {#hit-outcomes}

Iga projektili tabamuse korral maapealsele üksusele saadab server sõnumi 0xF144 (UnitOnHit) üksusele:
neli ühebaidist välja, neljas neist bitid, mida tabamus tegi (`selfCheck.unitMessages.outcome_*`):

| Bit | Tähendus | Tõend |
|---|---|---|
| 0x20 | projektili enda tabamus | peaaegu kõik tulevad 0xF0E9 tabamusega üksusele 5 ms jooksul; ilma selleta plahvatusega (plahvatuskahju) |
| 0x01 | läbistas (läbitung) | iga sõnum koos 0x02, 0x04 või 0x08-ga kannab ka seda |
| 0x02 | kriitiline tabamus | enamikul kriitilise tabamuse kirjetel on see, palju sagedamini kui juhuslikult |
| 0x04 | hävitatud | enamik tuleb tapmiskirjega ja üksuse surmaga sekundi jooksul |
| 0x08 | raske kahju | mõnel kriitilise tabamuse kirjel on see; muidu harva |

`hitOutcome` võtab halvima: `kill` (0x04), `critical` (0x02 või 0x08), `penetration` (0x01),
`nonpenetration` (ainult 0x20). Tabamus paaritatakse lähima paaritamata 0xF144-ga, millel on 0x20
ja mis on tema üksusele 5 ms jooksul. Mängu tabamuskaamera eristab rikošetti mitteläbitungist, kuid
ükski siin leitud bit ega väli seda ei tee: esimesed kolm baiti muutuvad tabamusest tabamusse ega ole
teada. Kliendi kordused saadavad 0xF144 ainult salvestajamängija enda lennukile, kõik bitid puhtad:
lennuki ja laeva tabamustel ei ole tulemust.

## Laskemoon {#ammunition}

(`selfCheck.unitMessages.ammunition`)

* **Plahvatav või mitte.** Kest, mis lõhkeb, saadab 0xF133 (UnitOnExplosion) laskja uid ja
  tabamuse numbriga; tabamus koos sellega on `explosive`, ülejäänud `kinetic`.
* **Relv ja tema pesa.** 0xF0BD (UnitBulletRearm) on järgmine laetud kuul: relva indeks sõiduki
  relvaloendis, laskemoonapesa ja järelejäänud laskemoon. Käsilaadija kordus tuleb püsiva laadimisaja
  järel iga tema tabamuse järel, automaatkahuri oma sekundi murdosa pärast. Laskja tabamused
  grupeeritakse sõiduki, signatuuri ja pursu järgi; grupp on relva oma, kui see relv laeb kuuli 20 s
  jooksul pärast poolt või enamat tema tabamustest püsiva viivitusega. `ammoSlot` on `relv/pesa`,
  pesa, mis oli enne tabamust laetud: tõenäoliselt see, mida tulistati, kui mängija ei muutnud
  laskemoona vahepeal. Kuulipildujad 0xF0BD ei saada.
* **Kest.** Tapmise relv on kesta ID (`125mm_3bm46`); tapja viimane tabamus ohvrile annab selle
  sellele laskja pesale, kus relva kaliiber sobib. Tema tüüp ja kaliiber tulevad relvafailist
  (`bulletName`, `bulletType`, `caliber`; `apds_fs_*` APFSDS, `heat_fs_*` HEAT-FS, `he_*` HE ...).
* **Ülejäänute kaliiber:** pesa relva oma; kuulipildujagrupi puhul ainus kuulipildujakaliiber, mis
  selle signatuuril võib olla; muidu sõiduki peamise püssi oma. Ilma installatsioonita (`--game`)
  ei ole tüüpi, nime ega kaliibrit peale `explosive` / `kinetic`.

Ei leitud: rikošett. Mitu veel sõnumit kannavad tabamuse laskjat ja numbrit (0xF0C2, tõenäoliselt
tabamuskaamera tee läbi sõiduki; 0xF117, 0xF13C, 0xF13E); need hoitakse lisafailis, mitte ei dekodeerita.
Mitteläbitung jääb `nonpenetration`.

## Sõiduki tulekahjud {#vehicle-fires}

Tulel olevat sõidukit näevad kõik kliendid: server saadab sõidukile olemi sõnumi (sündmus `0a519c58`),
mis loetleb tema peal põlevad tulekahjud, iga kord, kui nimekiri muutub. Iga tulekahju kohta: kaks
16-bitist ID-d (teine on kahjumudeli sõlm), tema liik ning -1, kuni tulekahju võtab. Tabamuse süüdatud
tulekahjule tuleb veel sõnum punktiga, kus see põleb, sõiduki raamistikus (x ees, y üles, z vasakule).

Read: `fire_on`, kui tulekahju ilmub nimekirja, `fire_off`, kui see on kadunud, sõidukil, koos
`fireId` (`first:node`), `fireKind` ja tabamuse süüdatud tulekahjude puhul `fireLocalX/Y/Z`
(ees, üles, paremale). Kui sõiduk on surnud, ei saadeta tema nimekirja sageli enam: tema tulekahjud
lõpevad tema vrakiga, muidu tema olemiga, muidu kordusega (`selfCheck.fires`).

Kontrollitud: iga kord, kui tanki tulekustutite arv vähenes, lahkus tulekahju nimekirjast murdosa
sekundi jooksul; enamik tulekahjupunkte asub sõiduki samal küljel kui tabamus, mis selle süütas. Liigid
on numbrid; mida need nimetavad, ei ole teada, samuti ei ole teada, millist osa sõlm tähistab.
Lennukid ei saada sellist nimekirja: tulel olevat lennukit ei loeta.

---

Osa [3DHeatist](https://github.com/Holdi601/3DHeat) ([dokumentatsioon](https://holdi601.github.io/3DHeat/)). Lähtekood: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
