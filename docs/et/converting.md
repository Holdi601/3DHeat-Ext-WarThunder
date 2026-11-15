---
title: Kordustete konverteerimine
nav_order: 4
lang: "et"
source: converting.md
source_hash: "43232a83420d"
nav_exclude: true
search_exclude: true
---
# Kordustete konverteerimine {#converting-replays}

Väljund: üks `.3dheat` fail lahingu kohta (vaikimisi) või eraldi failid
valikuga `--loose`.

## Samm-sammult {#step-by-step}

1. **Lülita kordused sisse.** War Thunder salvestab kliendi kordused mängu kausta
   `Replays`, kui kordustesalvestus on seadetes sisse lülitatud, näiteks
   `C:\Program Files (x86)\Steam\steamapps\common\War Thunder\Replays`.
   Serveri kordust, mille salvestasid mängu kordustelehelt (zip, kus on `0000.wrpl`,
   `0001.wrpl` ...), saab samuti konverteerida.
2. **Ava terminal** kaustas, kuhu tohib tulemusi kirjutada
   ([Enne alustamist](before-you-start.md)).
3. **Konverteeri:**

   ```bash
   heat3d-wt-replay "<War Thunder>/Replays" -o out
   heat3d-wt-replay a.wrpl b.wrpl -o out           # failid, kaustad või mõlemad
   heat3d-wt-replay battle.zip -o out              # serveri kordus zip-failina
   heat3d-wt-replay a.wrpl -o out --loose          # eraldi failid ühe .3dheat asemel
   ```

   `out` luuakse terminali kaustas.
4. **Loe, mida see ütleb.** Peaksid nägema ühte rida lahingu kohta.
5. **Ava see:** lae `out/<map>/<match>.3dheat` 3DHeat vaaturisse
   ([Faili laadimine](https://holdi601.github.io/3DHeat/container.html#loading-one)).

![Käivitus sünteetilise kordusega: üks .3dheat, --loose, katkine fail, tühi kaust](../assets/img/convert.svg)

Pilt on käivitus kordusel, mille testid koostavad koodis (päris kordust ega
installatsiooni ei ole):

- `ok <file>`: lahing konverteeritud (valikuga `--loose`: `ok <table> <match document>`);
- `failed <file>: <why>`: faili ei õnnestunud lugeda (väljumisolek 1; teised
  konverteeritakse siiski);
- `no .wrpl files given`: konverteerida pole midagi (väljumisolek 2);
- `note: ...`: näiteks et sõidukite nimede jaoks ei leitud War Thunderi
  installatsiooni.

## Valikud {#options}

| Valik | Vaikimisi | Mida teeb |
|---|---|---|
| `replays` (üks või mitu) | - | `.wrpl` failid, nende kaustad (kaust ise, mitte alamkaustad) või nende zip-failid (serveri kordus: selle `.wrpl` osad pakitakse lahti ajutisse kausta) |
| `-o`, `--out` | nõutav | kuhu kirjutada: kaust iga kaardi kohta sees |
| `--game KAUST` | leitakse | War Thunderi kaust, mille tekst nimetab sõidukid, relvad ja laskemoona ning mille tabelid hindavad [majandust](economy.md); ka `HEAT3D_WT_GAME` |
| `--no-smoothing` | väljas | hoia teiste üksuste hinnangulise asukoha arvutuse ja vastuvõetud näidised sellisena, nagu kordus need annab ([Hinnanguline asukoht ja silumine](aircraft.md#dead-reckoning-and-the-smoother)) |
| `--container` | sees | paki iga lahing üheks `.3dheat` failiks |
| `--loose` | väljas | hoia iga lahing eraldi failidena (tabel, mängu dokument, lisafailid) |
| `--version` | - | prindi `heat3d-wt-replay <version>` ja lõpeta |
| `-h`, `--help` | - | prindi valikud ja lõpeta |

Lahing, mis konverteeritakse uuesti, kirjutatakse uuesti. Valikud nii, nagu
programm need prindib: [Käskude viide](../cli-reference.md).

## Mis failid on üks lahing {#which-files-are-one-battle}

Iga lahing muutub üheks failiks
`out/<map>/<map>_<AB|RB|SB>_<mode>_<start, UTC>_<session id>.3dheat`. AB, RB ja SB
on mängu lühikujud lahingutüüpidele arcade, realistic ja simulator; `<mode>` on
missiooni režiim nii, nagu mäng seda märgib (`Conq4` Conquest #4, `Dom` Domination,
`Bttl` Battle; vt [Lahingurežiim](ground.md#battle-mode)); kumbki osa jääb välja,
kui kordus seda ei nimeta. Serveri kordus osad (`0000.wrpl`, `0001.wrpl` ...)
loetakse koos üheks lahinguks; kliendi kordus ja sama lahingu serveri osad on
kaks salvestust ja jäävad kaheks.

## Väljumisolek {#exit-status}

`0`, kui iga lahing konverteeriti, `1`, kui mõni ebaõnnestus (ülejäänud
konverteeritakse siiski), `2`, kui argumentide hulgast ei leitud ühtegi kordusfaili.

---

Osa [3DHeatist](https://github.com/Holdi601/3DHeat) ([dokumentatsioon](https://holdi601.github.io/3DHeat/)). Lähtekood: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
