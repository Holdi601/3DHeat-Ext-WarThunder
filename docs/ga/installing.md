---
title: Suiteáil
nav_order: 3
lang: ga
source: installing.md
source_hash: "3a4218d952bc"
nav_exclude: true
search_exclude: true
---
# Suiteáil {#installing}

Nua leis an líne ordaithe? Léigh [Sula dtosaíonn tú](before-you-start.md) ar dtús. Teastaíonn Python 3.10 nó níos déanaí; suiteáiltear pyarrow, numpy, zstandard agus Pillow leis.

## Céim ar chéim {#step-by-step}

1. Faigh an cód: `git clone https://github.com/Holdi601/3DHeat-Ext-WarThunder.git`, nó íoslódáil zip ó [Releases](https://github.com/Holdi601/3DHeat-Ext-WarThunder/releases) agus díphacáil é.
2. Oscail teirminéal sa fhillteán sin agus clóscríobh `pip install -e .`. Suiteálann sé seo dhá ordú: `heat3d-wt-replay` (athsheinmeanna) agus `heat3d-wt-level` (leibhéil).
3. Seiceáil é: `heat3d-wt-replay --version`. Ba cheart duit `heat3d-wt-replay 0.2.0` a fheiceáil. Liostaíonn `heat3d-wt-replay --help` na roghanna:

![heat3d-wt-replay --help](../assets/img/help.svg)

Gan suiteáil: `python -m heat3d_ext_warthunder ...` agus `python -m heat3d_ext_warthunder.levelcli ...` i bhfillteán na huirlise.

## Ainmneacha ó do shuiteáil {#names-from-your-install}

Faigheann feithiclí, airm agus lón catha a n-ainmneacha Béarla ó chomhaid téacs an chluiche féin, a léitear ó do shuiteáil nuair a thiontaítear. Aimsítear an tsuiteáil trí Steam nó trí réamhfhillteáin an tseoltóra; deir `--game <folder>` nó an athróg timpeallachta `HEAT3D_WT_GAME` cá bhfuil sí ar shlí eile. Níl aon téacs de chuid an chluiche sa stóras seo; gan suiteáil is iad aitheantais na bhfeithiclí na hainmneacha (deir an tiontaire é sin i líne `note:`).

## Nuashonruithe {#updates}

Seiceálann gach tús ar dtús eisiúintí GitHub an tionscadail (ceann amháin ar a mhéad gach cúpla uair an chloig; ní stopann sé tiontú choíche, ar líne nó as líne). Nuair a bhíonn eisiúint níos nuaí amuigh, fiafraíonn an t-ordú sula suiteálann sé í: nuashonraítear `git clone` le `git pull --ff-only` (diúltaítear dó cé go bhfuil athruithe áitiúla agat), cóip íoslódáilte ó chartlann na heisiúna. Cuireann `HEAT3D_NO_UPDATE=1` an seiceáil agus an nuashonrú as.

---

Cuid de [3DHeat](https://github.com/Holdi601/3DHeat) ([doiciméadúchán](https://holdi601.github.io/3DHeat/)). Foinse: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
