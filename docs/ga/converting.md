---
title: Athsheinmeanna a thiontú
nav_order: 4
lang: "ga"
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Athsheinmeanna a thiontú {#converting-replays}

Aschur: comhad `.3dheat` amháin do gach cath (an réamhshocrú), nó comhaid scaoilte le `--loose`.

## Céim ar chéim {#step-by-step}

1. **Cuir athsheinmeanna ar siúl.** Sábhálann War Thunder athsheinmeanna cliaint i bhfillteán `Replays` an chluiche nuair atá sábháil athsheinm ar siúl ina roghanna, mar shampla `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`. Is féidir athsheinm freastalaí a shábháil ó leathanach athsheinm an chluiche (zip le `0000.wrpl`, `0001.wrpl`, ...) a thiontú freisin.
2. **Oscail teirminéal** i bhfillteán inar féidir na torthaí a chur ([Sula dtosaíonn tú](before-you-start.md)).
3. **Tiontaigh:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # files, folders, or both
   heat3d-wt-replay battle.zip -o out              # a server replay's zip
   heat3d-wt-replay a.wrpl -o out --loose          # separate files instead of one .3dheat
   ```

   Déantar `out` sa fhillteán a bhfuil do theirminéal ann.
4. **Léigh an méid a deir sé.** Ba cheart duit líne amháin a fheiceáil do gach cath.
5. **Oscail é:** luchtaigh `out/<map>/<match>.3dheat` in amharcán 3DHeat ([Ceann amháin a luchtú](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![Rith ar athsheinm shintéiseach: .3dheat amháin, --loose, comhad briste, fillteán folamh](../assets/img/convert.svg)

Is rith é an pictiúr ar athsheinm a thógann na tástálacha sa chód (gan athsheinm fíor, gan suiteáil):

- `ok <file>`: cath tiontaithe (le `--loose`: `ok <table> <match document>`);
- `failed <file>: <why>`: comhad nárbh fhéidir a léamh (stádas scoir 1; tiontaítear na cinn eile ar aon nós);
- `no .wrpl files given`: níl aon rud le tiontú (stádas scoir 2);
- `note: ...`: mar shampla nár aimsíodh aon suiteáil War Thunder chun na feithiclí a ainmniú.

## Roghanna {#options}

| Rogha | Réamhshocrú | Cad a dhéanann sí |
|---|---|---|
| `replays` (ceann amháin nó níos mó) | - | comhaid `.wrpl`, fillteáin díobh (an fillteán féin, ní a fho-fhillteáin), nó zips díobh (athsheinm freastalaí: díphacáiltear a codanna `.wrpl` go fillteán sealadach) |
| `-o`, `--out` | riachtanach | cá scríobhfar: fillteán do gach léarscáil istigh |
| `--game FOLDER` | aimsithe | fillteán War Thunder a bhfuil a théacs ag ainmniú feithiclí, arm agus lón catha, agus a bhfuil a tháblaí ag praghsáil an [gheilleagair](economy.md); `HEAT3D_WT_GAME` freisin |
| `--no-smoothing` | as | coinnigh samplaí a ríomhadh trí dead reckoning agus samplaí a fuarthas d'aonaid eile mar atá siad san athsheinm ([Dead reckoning](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | air | pacáil gach cath i gcomhad `.3dheat` amháin |
| `--loose` | as | coinnigh gach cath mar chomhaid ar leith (tábla, cáipéis chluiche, comhaid chliatháin) |
| `--version` | - | priontáil `heat3d-wt-replay <version>` agus stop |
| `-h`, `--help` | - | priontáil na roghanna agus stop |

Scríobhtar cath a tiontaíodh arís arís. Na roghanna mar a phriontálann an clár iad: [Tagairt orduithe](../cli-reference.md).

## Cad iad na comhaid atá ina gcath amháin {#which-files-are-one-battle}

Éiríonn comhad amháin as gach cath, `out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat`. Is iad AB, RB agus SB foirmeacha gearra an chluiche ar chathanna arcáide, réalaíocha agus insamhalta; is é `<mode>` mód an mhisin mar a eochraíonn an cluiche é (`Conq4` Conquest #4, `Dom` Domination, `Bttl` Battle; féach [Mód catha](ground.md#battle-mode)); fágtar ceachtar cuid ar lár nuair nach ainmníonn an athsheinm ceann. Léitear codanna athsheinm freastalaí (`0000.wrpl`, `0001.wrpl`, ...) le chéile mar chath amháin; is dhá thaifead iad athsheinm cliaint agus codanna an fhreastalaí den chath céanna agus fanann siad ina dhá cheann.

## Stádas scoir {#exit-status}

`0` nuair a tiontaíodh gach cath, `1` nuair a theip ar aon cheann (tiontaítear an chuid eile ar aon nós), `2` nuair nár aimsíodh aon chomhad athsheinm i measc na n-argóintí.

---

Cuid de [3DHeat](https://github.com/Holdi601/3DHeat) ([doiciméadúchán](https://holdi601.github.io/3DHeat/)). Foinse: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
