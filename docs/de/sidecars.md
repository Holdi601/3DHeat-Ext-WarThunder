---
title: Sidecars und Vollständigkeit
nav_order: 8
lang: de
source: sidecars.md
source_hash: "e9982dbb930b"
nav_exclude: true
search_exclude: true
---
# Sidecars und Vollständigkeit {#sidecars-and-completeness}

Nichts aus einem Replay wird weggeworfen. Was der Umwandler liest, geht in die Tabelle
und das Match-Dokument; alles andere wird vollständig in drei Sidecar-Dateien neben der
Tabelle aufbewahrt (in der Datei `.3dheat` oder einzeln mit `--loose`). Das ist die Regel,
die alle 3DHeat-Umwandler teilen:
[Umwandler behalten alles](https://holdi601.github.io/3DHeat/converters.html).

## Die Sidecars {#the-sidecars}

- `<match>.messages.parquet`: jede Nachricht an eine Einheit (Zeit, Nachrichten-ID und
  Name, uid, eid, template, vehicle, ihre ID-Felder als Hex, `decoded` (was davon gelesen
  wird, als JSON), die Nutzdaten), jeder replizierte Komponentenwert (`name` die
  Komponente, `fields` ihr Wert), jede Entitätsnachricht (mit ihrer Entität und
  Klassennummer), jedes replizierte Objekt (`ReflectionData <kind>/<index>`, seine Felder
  als Hex) und jedes Paket, das kein Leser hier nimmt, vollständig.
- `<match>.objectives.parquet`: die Eroberungszonen im Zeitverlauf, eine Zeile je Änderung,
  die der Server gesendet hat: `time`, `event` (`state`, `progress`, `captured`,
  `neutralised`), `zone` (ihr Buchstabe), `zoneId`, `object`, `owner` (0 keiner,
  1, 2), `progress` (-100..100, positiv in Richtung Team 2), die Koordinaten `x`,
  `y`, `z` der Zone und alle `fields` des Objekts als Hex (siehe
  [Ziele](objectives.md)).
- `<match>.flight.parquet`: jeder Flugeintrag jedes Flugzeugs vollständig (seine Bits und
  `phase`: das Bit seines ersten Bytes, bei dem er begann), mit seiner Geschwindigkeit, den
  14 Steuer-Halbbytes (`control1-3`, `throttle`), seinen Triebwerken mit Zustand, Nachbrenner
  und Zustand und seiner Munition je Waffe (`ammo`; `numbers` ist die ganze Liste). Die Werte
  anderer Flugzeuge stehen so, wie sie zuletzt aufgefrischt wurden.

## Was die Zählungen garantieren {#what-the-counts-guarantee}

Die `counts` des Match-Dokuments sagen, was das Replay enthielt und was daraus wurde:

| Schlüssel | Was |
|---|---|
| `packets`, `unreadPackets` | jeder Pakettyp, der vorkam, und die, die kein Leser nimmt (vollständig im Nachrichten-Sidecar aufbewahrt) |
| `messageIds`, `messageIdsNotRead` | jede Nachrichten-ID, die vorkam, und wie oft, und die, die nur aufbewahrt, aber nicht gelesen werden |
| `replicatedComponents`, `replicatedNotRead` | gelesene Komponentenwerte und die, die nur aufbewahrt werden |
| `entities`, `entityTemplates`, `entityMessages` | was der Entitätsstrom erzeugt und gesendet hat |
| `droppedSamples` | absichtlich weggelassene Messwerte (das Wrack einer Bodeneinheit, nachdem ihre Entität weg ist), nach Grund |

Sonst fehlt nichts: Ein Teil des Replays ist entweder in die Tabelle oder das
Match-Dokument gelesen oder vollständig in einem Sidecar aufbewahrt. Das `selfCheck`
des Match-Dokuments enthält die Prüfungen dessen, was gelesen wurde
([So liest es ein Replay](how-it-reads.md)).

---

Teil von [3DHeat](https://github.com/Holdi601/3DHeat) ([Dokumentation](https://holdi601.github.io/3DHeat/)). Quelle: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
