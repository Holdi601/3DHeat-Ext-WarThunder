---
title: "Ajruplani"
nav_order: 11
lang: "mt"
source: aircraft.md
source_hash: "2073f74a8bad"
nav_exclude: true
search_exclude: true
---
# Ajruplani {#aircraft}

Għal min irid jaf minn fejn jiġu l-kolonni tal-ajruplani u kemm wieħed jista' jafdahom.
Kull kontroll hawn taħt iqabbel valur ma' xi ħaġa li r-ripetizzjoni tgħid b'mod ieħor,
indipendenti; jingħataw biss il-metodu u l-qbil.

## Strumenti tal-cockpit {#cockpit-instruments}

Il-messaġġ 0xD04A jibgħat il-gauges tal-plejer li rreġistra bħala pari (numru, valur):
erba' fis-sekonda fil-battaljiet arcade, il-valuri mibdula biss fil-battaljiet simulator.
In-numri jiffurmaw lista waħda fuq il-cockpits kollha, u cockpit jibgħat il-gauges li
għandu l-mudell tiegħu. Il-kodiċi tal-logħba jiddeċiedi liema numru huwa liema gauge, għalhekk
kull numru ngħata isem skont dak li jagħmel u kien ikkontrollat mar-ripetizzjoni
(`convert.INSTRUMENTS` iżomm ir-riżultat; xejn ma jinqara mill-installazzjoni):

| Numru | Isem | Ikkontrollat kontra |
|---|---|---|
| 0 | veloċità indikata, m/s | il-veloċità tal-mogħdija korretta għad-densità tal-arja: korrelazzjoni 0.99 |
| 39 | rata ta' tlugħ, m/s | ir-rata ta' tlugħ tal-mogħdija: korrelazzjoni 'il fuq minn 0.99 |
| 40, 41 | altitudni, m; altitudni modulu 1000 | l-għoli tal-mogħdija, ftit metri bogħod |
| 52, 53 | roll u pitch tal-orizzont artifiċjali | il-minus tar-roll u tal-pitch tat-tabella, inqas minn grad bogħod |
| 64 | kumpass | il-heading tat-tabella, inqas minn 0.1 grad bogħod |
| 15-20 | pedali tar-rudder | il-forza laterali fuq l-ajruplan |
| 23, 31 | stick: elevator u ailerons (sinjal kif tal-mudell tal-cockpit) | l-angolu tal-attakk; ir-rata tar-roll |
| 69, 71, 73 | arloġġ: sigħat (kwadrant ta' 12-il siegħa), minuti, sekondi | il-ħin lokali tal-kompjuter li rreġistra, sal-minuta |
| 75 | manifold pressure, atm | ogħla b'war emergency power milli b'full throttle |
| 81-86, 87-92, 93-98 | rpm għal kull magna, rpm modulu 1000, gauge tal-rpm | bejniethom eżatt; ir-rpm tal-magna: korrelazzjoni 'il fuq minn 0.97 |
| 195 | fjuwil | jaqa' matul sortie, jerġa' jimtela f'respawn |
| 228-230 | riġlejn tal-landing gear, 1 'l isfel | 'l isfel biss ħdejn l-għoli tal-ajrudromi u b'veloċità ta' inżul |
| 240, 241 | throttle għal kull magna (1.1 war emergency power jew afterburner) | it-throttle tad-daħla tat-titjira |
| 330-332, 346-348 | kontaturi tal-munizzjon (żewġ settijiet ugwali) | ir-rawnds tal-preset tal-armi, jaqgħu mar-rawnds tad-daħla tat-titjira |
| 135, 159 | temperatura taz-zejt u tar-ras tas-silindru | probabbli: jogħlew matul sortie |
| 58, 61 | ballun tal-iżlitt, labra tal-iduru | probabbli: isegwu l-forza laterali u r-rata tal-iduru |
| 223 | airbrake | probabbli: mixgħul biss waqt l-approċċ |
| 490-497, 500-505 | brejkijiet tar-roti | probabbli: mixgħula biss waqt li wieqaf fuq ajrudrom |

Jintbagħtu ftit numri oħra li t-tifsira tagħhom mhix magħrufa; jinżammu fil-
`authorInstruments.notNamed` tad-dokument tal-partita.

Il-`ias`, `vario`, `fuel`, `manifoldPressure`, `gear`, `oilTemperature`, `headTemperature` u
`throttle` tat-tabella jiġu minn dawn, fuq ir-ringieli proprji tal-plejer li rreġistra, billi jittieħed
l-aħħar messaġġ l-iktar 0.2 s wara l-kampjun.

## Daħliet tat-titjira {#flight-entries}

Id-daħla tat-titjira ta' kull ajruplan (tip ta' pakkett 2) iġġorr, minbarra l-pożizzjoni u
l-attitudni tiegħu:

- **Veloċità**: kelma ta' 32 bit wara l-attitudni. Il-bits 31, 30 u 29 huma s-sinjali ta' x, y u z;
  imbagħad il-veloċità f'11-il bit ta' 500/2047 m/s (tieqaf f'500 m/s), imbagħad |x| u |y| bħala
  frazzjonijiet tal-veloċità f'9 bits kull wieħed, u z huwa dak li jagħmel il-vettur vettur unità.
  Ikkontrollata kontra l-pass bejn kampjuni riċevuti: id-direzzjoni taqbel fi ħdan frazzjoni ta' grad
  għall-plejer li rreġistra u fi ħdan madwar 2 gradi għall-oħrajn kollha; il-veloċità fi ħdan 0.2 %.
  `selfCheck.flightEntries`.
- **Rawnds għal kull arma**: lista qabel il-pożizzjoni, element għal kull arma, ir-rawnds li fadal
  l-ewwel. Dik tal-plejer li rreġistra tkun ugwali għall-kontaturi tal-cockpit tick wara għal kważi
  kull kampjun.
- **Kontrolli u throttle**: 7 bytes wara l-veloċità, moqrija bħala 14-il nibble. Għall-plejer li
  rreġistra, kull tick: 1 l-elevator, 2 l-ailerons, 3 ir-rudder (8 fil-mistrieħ), 11 it-throttle
  f'ħmistax-il parti (15 ukoll għal war emergency power u afterburner), 4 il-brejkijiet tar-roti,
  5 l-airbrake, 8 probabbilment il-brake chute. In-nibbles ta' ajruplani oħra jinbidlu ftit drabi
  f'battalja u mhumiex il-kontrolli tagħhom dak il-ħin.
- **Magni**: għal kull magna byte tal-istat (0 mitfija; 1-6 qed tibda; 7 taħdem; 8 mejta), valur ta'
  16-il bit biss bl-afterburner (32767 sħiħ), u byte biss wara li l-magna nħabtet. Il-biċċa l-kbira
  tal-ajruplani li l-magna tagħhom issir "dead" jinqatlu jew jispiċċaw fi ftit minuti.

## Reflection data {#reflection-data}

Il-messaġġi 0xF02D u 0xF0AA jirreplikaw l-oġġetti nnumerati tal-logħba: għal kull oġġett l-id tiegħu
(l-ogħla 5 bits it-tip, l-aktar baxxi 11-il bit indiċi) u tabella ta' kampi. It-tip 14 huwa s-slots
tal-plejers (kamp 2 id tal-utent u isem, 9 it-tim), it-tip 15 it-timijiet (indiċi 1 u 2):

- Il-kamp 39 ta' slot iżomm l-istatistika tiegħu f'postijiet fissi: qtil (offset 0), qtil tat-tim (2),
  imwiet (4), qtil navali (10), qtil ta' AI (12), qtil ta' AI fuq l-art (14), assists (20), żoni tal-qbid
  (22), ħsara fiż-żoni (24, 32-bit), premju tal-ħsara (40, 32-bit), missili evaded (50). Il-kamp 38 jibda
  bil-punti, il-kamp 42 huwa s-squad. Fi tmiem battalja kull valur huwa ugwali għal dak tar-riżultati
  għal kull plejer (`selfCheck.scoreboardVsResults`). Fejn jinżammu l-qtil fuq l-art mhux magħruf.
- Il-kamp 7 ta' tim huwa l-punti tiegħu: fl-aħħar huwa ugwali għas-somma tal-punti tal-plejers tiegħu
  fir-riżultati. Il-kamp 3 huwa probabbilment it-tickets tiegħu.
- Kull messaġġ jibgħat biss il-kampi li nbidlu, għalhekk `scoreboard` fid-dokument tal-partita jelenka
  l-istatistika ta' kull plejer u l-punti ta' kull tim f'kull bidla.

## Dead reckoning, u s-smoother {#dead-reckoning-and-the-smoother}

Ripetizzjoni tal-klijent tirrekordja kull ajruplan erba' darbiet fis-sekonda, kif irsimha l-klijent.
Bejn l-aġġornamenti li jirċievi għal ajruplan 'l bogħod, il-klijent iċaqlqu 'l quddiem tul l-aħħar
veloċità tiegħu u jdawru bl-aħħar rati tiegħu, u fl-aġġornament li jmiss iqiegħdu hemm f'daqqa. Moqrija kif inhi,
mogħdija taħdem dritta, imbagħad taqbeż. Xejn fid-daħla tat-titjira ma jimmarka liema kampjuni ġew
riċevuti; kampjun dead-reckoned jinstab minn dak li hu: ikompli l-linja dritta taż-żewġ kampjuni
ta' qablu, bil-pass tagħhom, fi ħdan 3 cm.

Kemm dan jimporta jiddependi mill-battalja: fil-battaljiet arcade madwar nofs il-kampjuni ta' ajruplani
oħra jistgħu jkunu dead-reckoned, fil-battaljiet simulator ftit fil-mija biss. Is-smoother inaqqas
il-passi 'l fuq minn 15 g b'madwar ħames darbiet (`selfCheck.deadReckoning`). L-ajruplan proprju
tal-plejer li rreġistra ma jiġix estrapolat mill-klijent u jitħalla kif inhu.

B'mod default (`--no-smoothing` itfiha) il-mogħdijiet tal-unitajiet kollha ħlief dik tal-plejer li
rreġistra jitqiegħdu fejn jgħidu l-istati riċevuti li kienu: kampjun dead-reckoned jitqiegħed fuq kurva
mal-kampjuni riċevuti qabel u wara, kull wieħed bil-veloċità tiegħu stess; fuq aktar minn 3 s il-linja
dritta titgħawweġ biss lejn il-kampjun riċevut li jmiss, biex ebda kampjun ma jiċċaqlaq iktar minn kemm iqiegħdu l-klijent stess f'daqqa. L-attitudni tiegħu tiġi mdawra b'mod uniformi minn attitudni riċevuta għal oħra.
Il-kampjuni riċevuti jiġu mlaqqma b'mhux aktar minn 2 m jew 0.04 s tal-veloċità tagħhom; dawra
kostanti tibqa' kif inhi. Il-valuri proprji tar-ripetizzjoni jibqgħu fil-kolonni `Raw`.

## Attitudni, ikkontrollata {#attitude-checked}

Fuq l-ajruplan proprju tal-plejer li rreġistra l-heading jinsab fi ħdan grad (medjan) mid-direzzjoni
tal-vjaġġ, il-pitch fi ħdan ftit gradi mill-angolu tat-tlugħ, u f'dawriet ċari r-roll għandu s-sinjal
tad-dawra għal kważi kull kampjun: ir-roll tal-flight model huwa ġewnaħ ix-xellug 'l isfel pożittiv, u
t-tabella ddawru għal ġewnaħ il-lemin 'l isfel pożittiv (`selfCheck.aircraftAttitude`). L-angoli ta'
10 bits jimxu 0.18 grad. L-attitudni ta' unitajiet tal-art hija kkontrollata kontra s-sparaturi
tagħhom ([Turrets](ground.md#turrets)).

---

Parti mid-[3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentazzjoni](https://holdi601.github.io/3DHeat/)). Sors: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
