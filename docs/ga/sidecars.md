---
title: Comhaid chliatháin agus iomláine
nav_order: 8
lang: ga
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Comhaid chliatháin agus iomláine {#sidecars-and-completeness}

Ní chaitear aon rud in athsheinm uait. Téann an méid a léann an tiontaire isteach sa tábla agus sa cháipéis chluiche; coinnítear gach rud eile iomlán i dtrí chomhad chliatháin le hais an tábla (istigh sa chomhad `.3dheat`, nó scaoilte le `--loose`). Is é seo an riail a roinneann gach tiontaire 3DHeat: [Coimeádann tiontairí gach rud](https://holdi601.github.io/3DHeat/converters.html).

## Na comhaid chliatháin {#the-sidecars}

- `<match>.messages.parquet`: gach teachtaireacht chuig aonad (am, id agus ainm teachtaireachta, uid, eid, teimpléad, feithicil, a réimsí id mar heics, `decoded` (an méid atá léite de, mar JSON), an pálasta), gach luach comhpháirte macasamhlaithe (`name` an chomhpháirt, `fields` a luach), gach teachtaireacht eintitis (lena eintiteas agus uimhir ranga), gach réad macasamhlaithe (`ReflectionData <kind>/<index>`, a réimsí mar heics) agus gach paicéad nach nglacann léitheoir ar bith anseo leis, iomlán.
- `<match>.objectives.parquet`: na criosanna gabhála le himeacht ama, sraith amháin do gach athrú a sheol an freastalaí: `time`, `event` (`state`, `progress`, `captured`, `neutralised`), `zone` (a litir), `zoneId`, `object`, `owner` (0 aon cheann, 1, 2), `progress` (-100..100, dearfach i dtreo foireann 2), `x`, `y`, `z` an chrios, agus gach `fields` den réad mar heics (féach [Cuspóirí](objectives.md)).
- `<match>.flight.parquet`: gach iontráil den mhúnla eitilte de gach aerárthach iomlán (a bhiteanna, agus `phase`: an bit dá chéad bheart inar thosaigh sé), lena threoluas, na 14 nibble rialaithe (`control1-3`, `throttle`), a innill lena stát, tar-dóite agus riocht, agus a chruinn in aghaidh an airm (`ammo`; is é `numbers` an liosta iomlán). Tá luachanna aerárthach eile mar a nuashonraíodh go deireanach iad.

## An méid a ráthaíonn na comhaireamh {#what-the-counts-guarantee}

Deir `counts` na cáipéise cluiche cad a bhí san athsheinm agus cad a tharla dó:

| Eochair | Cad é |
|---|---|
| `packets`, `unreadPackets` | gach cineál paicéid a casadh, agus iad siúd nach nglacann léitheoir ar bith leo (coinnithe iomlán sa chomhad chliatháin teachtaireachtaí) |
| `messageIds`, `messageIdsNotRead` | gach id teachtaireachta a casadh agus cé chomh minic, agus iad siúd nár coinníodh ach nár léadh |
| `replicatedComponents`, `replicatedNotRead` | luachanna comhpháirte a léadh, agus iad siúd nár coinníodh ach |
| `entities`, `entityTemplates`, `entityMessages` | an méid a chruthaigh agus a sheol an sruth eintiteas |
| `droppedSamples` | samplaí a fágadh ar lár d'aon turas (raic aonaid talún tar éis dá eintiteas imeacht), de réir cúise |

Ní fhágtar aon rud eile ar lár: tá gach mír den athsheinm léite isteach sa tábla nó sa cháipéis chluiche, nó coinnithe iomlán i gcomhad cliatháin. Coinníonn `selfCheck` na cáipéise cluiche seiceálacha an méid a léadh ([Conas a léann sé athsheinm](how-it-reads.md)).

---

Cuid de [3DHeat](https://github.com/Holdi601/3DHeat) ([doiciméadúchán](https://holdi601.github.io/3DHeat/)). Foinse: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
