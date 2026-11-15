---
title: "Objettivi"
nav_order: 15
lang: "mt"
source: objectives.md
source_hash: "ed52ae9e8231"
nav_exclude: true
search_exclude: true
---
# Objettivi {#objectives}

L-`objectives` fid-dokument tal-partita jelenka dak li dwaru tiġi miġġielda l-battalja, minn żewġ sorsi (`source`):

- **Ir-ripetizzjoni** (`replay`): l-oġġetti tal-missjoni li 0xD039 isemmi (żoni tal-qbid `cz_circle_NN`, ajrudromi, helipads,
  bażijiet), imqiegħda fejn jqegħduhom l-oġġetti replikati tat-tip 3 (0xF02D) issa - żona tal-qbid tibda fil-post
  tat-template tagħha u titqiegħed fiż-żona ta' din il-modalità fil-bidu (`moved`). In-numri tat-tip 3 isegwu l-ordni ta' 0xD039;
  kull oġġett li ma jiġix imċaqlaq jinsab eżatt fejn 0xD039 għandu, li jikkontrolla l-ordni. Żona tal-qbid tieħu
  il-forma u r-raġġ taż-żona tal-missjoni f'postha (`area`, fi ħdan 2 m) u l-ittra tagħha mill-indiċi tagħha stess (tip
  5 kamp 69: 0 = A); l-ordni tal-ittri huwa tar-ripetizzjoni, mhux ikkontrollat mal-mappa tal-logħba.
- **Il-missjoni** (`mission`): il-fajl tal-missjoni `<mission>.blk` fil-`mis.vromfs.bin` tal-installazzjoni tiegħek u t-
  templates li jimporta (moqri biss, fil-ħin tal-konverżjoni): iż-żoni tiegħu, klassifikati bl-isem - spawns (il-punti
  nnumerati ta' spawn `..._spawnareaNN` bħala spawn wieħed `points`), żoni tal-battalja, miri tal-bombi (`bomb_zone`), punti ta' spawn
  tal-konvojs (`road_NN_spawn`), żoni tal-ħruġ u tal-qtil. Żoni ta' modalità oħra tal-istess mappa (`conq_`, `dom_`, `bttl_`,
  ...) jitħallew barra, u mill-varjanti `_arcade` / `_realistic` / `_hardcore` dik tal-battalja stess (RB jieħu
  `_realistic`, inkella `_hardcore`, kif jagħmlu l-iscripts tal-missjoni); markers tal-briefing, punti tal-kanuni AA u żoni
  usa' minn 5 km (iż-żoni li fuqhom jinxterdu l-spawns) ukoll. Kull spawn jgħid kemm mogħdijiet ta' plejers bdew fih (`used`,
  `usedByTeam`). Missjoni tista' tibdel in-nahat tagħha b'xorti (`randomSpawnTeams`): meta l-ispawns juru t-timijiet
  tar-ripetizzjoni bil-maqlub, kull `team` jinbidel u n-naħa tal-isem tinżamm bħala `missionTeam`. Ir-rotot tal-konvojs
  mhumiex fil-waypoints tal-missjonijiet kif moqrija; jingħata biss fejn jidhru l-konvojs.

Iż-żoni tal-qbid maż-żmien huma s-sidecar `<match>.objectives.parquet`: l-oġġetti replikati tat-tip 5, wieħed għal kull
żona - il-kamp 2 is-sid tagħha (0, 1, 2), il-kamp 67 il-progress tal-qbid tagħha, byte bis-sinjal minn -100 sa 100 (pożittiv
lejn it-tim 2), il-kamp 69 l-indiċi tagħha. Ikkontrollat (`selfCheck.objectives`) fuq ripetizzjonijiet tas-server tal-art ta' battaljiet Conquest u Domination: kull bidla ta' sid
tiġi b'plejer tat-tim li qabad li jikseb `captureZone` fl-scoreboard fl-istess mument (fi ħdan
1.5 s) u b'unità tal-art ħajja ta' dak it-tim ġewwa ż-żona; l-ispawns ta' kull battalja juru t-timijiet tar-ripetizzjoni
b'mod wieħed biss (spiss maqlubin kontra t-`t1_` / `t2_` tal-missjoni).

## Scene units: trams u vagun tal-ferrovija {#scene-units-trams-and-rail-wagons}

Livell jista' jpoġġi unitajiet tiegħu: l-entitajiet `unit_loader+rail_wagon` ta' ripetizzjoni tas-server huma t-trams tal-fajl
tax-xena tal-livell (`gamedata/scenes/<level>_objects.blk` f'`aces.vromfs.bin`: `setting__unit_class`, it-trasformazzjoni
tiegħu u `setting__isDead`). L-entitajiet tagħhom ma jġorru ebda uid li jinqara, għalhekk mogħdija tal-art mingħajr entità
ta' unità li l-ewwel kampjun tagħha jinsab fi ħdan 2 m minn unità tax-xena hija dik l-unità: il-klassi tagħha bħala `Vehicle`, kind `train`, type
`tram`, `locomotive` jew `wagon`, ebda tim; unità li x-xena tpoġġi mejta (bħal trams maħruqin) hija wreck (`alive` 0) mill-ewwel ringiela tagħha. Il-logħba m'għandha ebda isem Ingliż għalihom; `VehicleName` huwa l-id
moqri bħala kliem ("Railway tram A"). Il-pożizzjonijiet tagħhom ma jitħarrkux: kważi kollha qatt ma jiċċaqalqu (kull
kampjun l-istess sal-bit). Ir-ripetizzjoni tibgħathom madwar għaxar darbiet fis-sekonda
bla ma jimporta, għalhekk mill-kampjuni tagħhom jinżammu biss dawk li jċaqalquhom (0.05 m jew 0.1 grad), u wieħed kull 10 s
(`selfCheck.sceneUnits` jgħodd il-kampjuni mwarrba). Qabel, kienu mogħdijiet bl-isem `uid 8`
mingħajr vettura.

---

Parti mid-[3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentazzjoni](https://holdi601.github.io/3DHeat/)). Sors: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
