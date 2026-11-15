---
title: Rungtynių dokumentas
nav_order: 7
lang: lt
source: match-document.md
source_hash: "665622673174"
nav_exclude: true
search_exclude: true
---
# Rungtynių dokumentas {#the-match-document}

![The start of a synthetic match document, and its keys](../assets/img/match-document.svg)

`<match>.match.json` laiko viską, ką įrašas sako ir kas nėra lentelės eilutė. Žiūryklės Rungtynių skirtukas
skaito jį.

## Mūšis {#the-battle}

| Raktas | Ką reiškia |
|---|---|
| `format`, `version` | `heat3d-wt-replay-match`, `2` |
| `match`, `map`, `level` | rungtynių id (kaip failo vardas); žemėlapio id; lygio failas, kurį jis naudoja |
| `mission`, `missionKey` | misijos vardas ir jos raktas žaidimo teksto failuose |
| `battleClass`, `environment`, `weather` | kaip jas nurodo antraštė |
| `sessionId`, `server` | mūšio sesijos id; serveris |
| `replayVersion`, `flightLayout` | įrašo formato versija; perskaitytas skrydžio paketų išdėstymas (`2025` arba `2026`) |
| `files` | perskaityti įrašų failai (vienas arba serverio įrašo dalys) |
| `started`, `timePlayed`, `replayEnd` | pradžios laikas (ISO, UTC); sužaisti sekundės, pagal rezultatus; įrašo paskutinio paketo sekundės |
| `author`, `authorUserId` | įrašantis žaidėjas ir jo Gaijin id (kliento įrašai) |
| `teams` | mūšio komandos (`1`, `2`) |
| `result` | `winner`, `status` (`success` arba `fail`, autoriaus baigtis), `authorTeam`, `teams` ([Ekonomika](economy.md)) |
| `vehicleNames` | iš kur paimti technikos vardai (jūsų diegimas) ir jų kalba |
| `conventions` | lentelės vienetai ir ženklai: ašys, laikas, gyvybė, trajektorija, `alive`, posūkis ir dar |

## Viskas kita {#everything-else}

| Raktas | Ką reiškia |
|---|---|
| `battle`, `difficulty`, `gameMode` | mūšio režimas: `difficulty` `AB` / `RB` / `SB` (ir jo pavadinimas bei antraštės baitas), `gameMode` `ground` / `air` / `naval`, misijos režimas (`Dom`, `Conq`, `Bttl`, `I2M`, ...) ir jo angliškas pavadinimas iš diegimo (`Domination`, `Enduring Confrontation`), leidžiami techninių vienetų tipai (žr. [Mūšio režimas](ground.md#battle-mode)) |
| `settings` | misijos blk po antraštės: režimas, aplinka, oras, taškų ir laiko ribos, šalys, leidžiami techninių vienetų tipai, vėjas ir `stars` (platuma, ilguma, data, vietinis laikas) |
| `sky` | pirmasis `CustomWeatherParams`: saulės ir mėnulio kryptis, vėjas, dangaus spalvos, debesų poslinkiai |
| `players`, `slots` | rezultatų eilutė kiekvienam žaidėjui (nužudymai, sausumos nužudymai, mirtys, pagalbos, taškai, užimtos zonos, būrys, klanas, šalis, sudėtis, uid, kuriais jie vairavo); įrašo žaidėjų lizdai (vardas, vartotojo id, komanda) |
| `units` | kiekvienas vieneto esybė, kurią įrašas sukūrė: eid, uid, šablonas, technika, rūšis, tipas, komanda, žaidėjas, misijos vardas, kada sukurta ir pašalinta, kur sukurta, kurių komponentų nepavyko perskaityti |
| `objects` | pavadinti misijos objektai: kapitalo zonos ir aerodromai su jų pozicija ir dydžiu, aerodromų kontūrai kaip taškai, atgimimo zonos |
| `objectives` | mūšio tikslai, kiekvienas su `type` (`capture_zone`, `airfield`, `helipad`, `base`, `spawn`, `convoy_spawn`, `battle_area`, `bombing_target`, `exit_zone`, `kill_area`, `rearm_zone`), `team` (įrašo 1 ar 2, tuščias - abiems), `name` (kapitalo zonos raidė, `A`), `shape` (`sphere`, `cylinder`, `box`, `point`, `points`, `outline`) su `position`, `radius` / `height` / `size` ir `heading`, `source` (`replay` arba `mission`) ir kas dar žinoma (žr. [Tikslai](objectives.md)) |
| `kills`, `hits`, `modulesDestroyed` | su abiejų pusių vardais ir technika; nužudymai su ginklo angliškais vardais |
| `weapons` | kiekviena raketa, raketa su valdymu, bomba, torpeda, papildomas bakas ir numestas krovinys: kada, kur paleista (pozicija, orientacija, greitis), kieno (artimiausias per 300 m ir 1,5 s), kiek skrydžio pavyzdžių, kur paskutinį kartą matyta, kada pašalinta |
| `explosions`, `flak` | `PlayExplosionVisual` (pozicija, kryptis, rūšis) ir `PlayFlakExplosionVisual` (pozicija) |
| `awards` | įrašančiojo žaidėjo apdovanojimai (`TextStreak`: first_blood, serijos, iššūkių skaitikliai) |
| `detections`, `unitStates` | `UnitDetected` vienetų poros; pranešimas (0xF093) su vieneto pozicija, orientacija ir greičiu, kurio prasmė nežinoma |
| `authorInstruments` | įrašančiojo žaidėjo kabinos reikšmės (`ReplayCockpitParams`) pagal prietaiso numerį, ne daugiau kaip po vieną per sekundę; `known` įvardija kiekvieną numerį, kurį šis įrašas siuntė (vardas, vienetas, kaip patikrinta), `notNamed` - likusius |
| `scoreboard` | kiekvieno žaidėjo statistika kiekvieną kartą, kai ji pasikeitė (nužudymai, mirtys, pagalbos, taškai, DI nužudymai, jūrų nužudymai, zonos, žala, vengimai raketoms, būrys), ir kiekvienos komandos taškai bei tikėtini bilietai laikui bėgant (žr. [Atspindžio duomenys](aircraft.md#reflection-data)) |
| `economy` | mūšio Sidabro liūtai ir tyrimų taškai (žr. [Ekonomika](economy.md)): sumos, pagal žaidėją, pagal techniką, daugikliai, laimėtojas, patikrinimai |
| `entityMessages` | esybių pranešimai (0x20) pagal klasės numerį: kiekis, taikinių šablonai, dydžiai |
| `chat` | kiekviena pokalbio eilutė |
| `triggers`, `hints`, `missionProgress` | misijos scenarijaus veiksmai (RunTriggerAction), jos patarimai, jos eigos pranešimai |
| `camera` | įrašančiojo žaidėjo įrašo kameros laukai kas 0,25 s, kaip jie buvo siųsti (lentelėje ji yra trajektorija) |
| `projectileHitReplays` | įrašančiojo žaidėjo paties pataikymai ir jo pataikymai į jį, su ginklu ir šaudmenimis bei jų angliškais vardais |
| `results` | visas rezultatų blk, kaip jį įrašė žaidimas |
| `counts` | eilutės, įvykiai, gyvybės, rūšys, pavyzdžiai, esybės pagal šabloną, ginklai, perskaityti ir neperskaityti paketai, kiekvienas matytas pranešimo id ir tie, kurių neskaitoma, praleisti pavyzdžiai |
| `trackBreaks` | kiekvienas trajektorijos pjūvis žingsniui, greitesniam nei vienetas gali eiti: kur, kiek toli, kaip greitai ir kas tai greičiausiai yra |
| `selfCheck` | patikrinimai, išvardyti [Kaip įrankis skaito įrašą](how-it-reads.md), skaičiuojami kiekvieno konvertavimo metu; `stepSpeed` pagal rūšį pateikia greitį tarp gretimų trajektorijos eilučių, kaip jas jungia žiūryklė (mediana, 99 procentilis, didžiausias, ir žingsniai, greitesni nei įmanoma, kurių turi būti 0) |

---

Dalis [3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentacija](https://holdi601.github.io/3DHeat/)). Šaltinis: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
