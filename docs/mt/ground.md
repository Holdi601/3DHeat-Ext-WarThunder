---
title: "Unitajiet tal-art u kamera"
nav_order: 12
lang: "mt"
source: ground.md
source_hash: "b5eb495b1d3a"
nav_exclude: true
search_exclude: true
---
# Unitajiet tal-art u kamera {#ground-units-and-camera}

Għal min irid jaf minn fejn jiġu l-kolonni tat-turret, tal-kamera u tal-modalità tal-battalja u
kemm wieħed jista' jafdahom. Il-kontrolli jagħtu biss il-metodu u l-qbil.

## Turrets {#turrets}

L-istat tal-art ta' tank (attitudni ta' 16-il bit) iżomm, wara l-pożizzjoni tiegħu, 141 bit mhux
moqrija, imbagħad għal kull turret 62 bit: il-yaw tat-turret u l-pitch tal-kanun (16-il bit kull
wieħed, 360/65536 grad għal pass, bis-sinjal) u 30 bit mhux moqrija; imbagħad padding, u fuq xi
stati 200 bit oħra. Għadd it-turrets huwa l-byte mibgħut qabel l-istat. Stat li t-tul tiegħu ma
jaqbilx ma jagħtix turrets (unitajiet statiċi jibagħtu stat iqsar). Il-yaw huwa relattiv għall-iskoss,
'l quddiem mal-arloġġ pożittiv, 0 dritt 'il quddiem; il-pitch relattiv għall-iskoss, 'il fuq pożittiv.

Kif ġie kkontrollat:

- **Kontra s-sparaturi:** għal kull daqqa ta' tank, id-direzzjoni fid-dinja tal-kanun ewlieni tiegħu
  (attitudni tal-iskoss mdawra bil-yaw tat-turret u bil-pitch tal-kanun) kontra l-linja mix-xutter
  sal-unità li nħabtet, għall-inqas 30 m 'il bogħod: għal kull battalja medjan ta' madwar 98 % fi
  ħdan 3 gradi fl-heading u 99 % fl-elevazzjoni (`selfCheck.turretsVsShots`). Il-bqija
  huma l-aktar daqqiet ta' magna gun f'turret oħra.
- **Kontra l-aim tal-plejer li rreġistra:** it-tank proprju tiegħu jibgħat l-angolu tal-aim tiegħu
  fid-dinja (kontra l-arloġġ mil-lvant), il-pitch u d-distanza. L-heading tal-iskoss flimkien
  mal-yaw tat-turret jinsab fi ħdan nofs grad (medjan) mill-aim.

**Ripetizzjonijiet tas-server** (0xF074) jibagħtu l-istat ta' kull tank bl-istess layout, segwit
minn dejta tagħhom stess, għalhekk kull turret li ż-żewġ angoli tagħha jinsabu ġewwa l-istat tinqara
(għall-inqas dik ewlenija għal kważi kull ringiela ta' tank). Hija t-turret, mhux il-kamera:

- **Kontra s-sparaturi**, kif hawn fuq: għal kull battalja 'l fuq minn 90 % fi ħdan 3 gradi
  fl-heading u 99 % fl-elevazzjoni.
- **Kontra l-ħarsa:** ripetizzjoni tas-server tibgħat l-aim ta' kull plejer (`viewYaw`,
  `viewPitch`). It-turret issegwi l-ħarsa fi ħdan nofs grad (medjan), imma ddur ħafna aktar bil-mod
  milli tiċċaqlaq il-ħarsa, kif jagħmel drive ta' turret (`selfCheck.turretVsView`).
- **Imma mhux dejjem bil-veloċità ta' drive:** kampjun b'kampjun, il-valur kif intbagħat xi drabi
  jaqbeż fuq l-aim meta l-aim ikun qrib il-kanun, aktar malajr minn kull drive li jdur.

Għalhekk it-tabella żżomm it-turret **miżmuma mad-drive tagħha**: `turretYaw` / `gunPitch`
jimxu lejn il-valur kif intbagħat b'mhux aktar mill-veloċità tad-dawra tal-kanun ewlieni mill-fajl
tal-vettura tal-installazzjoni (darbiet 1.3 għall-ħiliet tal-ekwipaġġ u l-modifiki; 45 u 20 grad
fis-sekonda fejn l-installazzjoni ma tagħti l-ebda waħda). F'kull daqqa tal-kanun ewlieni t-turret
titqiegħed eżatt fuq il-linja tas-sparatura, u pass lura jġibha hemm fil-ħin (`selfCheck.turretLimit`).
Ir-ringiela `shot` iġġorr dak it-`turretYaw` / `gunPitch` ukoll. Il-valur kif intbagħat jibqa' f'
`turretYawRaw` / `gunPitchRaw`. Tank li l-istat tiegħu ma jġorr ebda turret għandu kolonni tat-turret
vojta (il-viewer jista' jerġa' lura għal `viewYaw`). Il-`gunPitch` jinsab ftit 'il fuq minn
`viewPitch` fil-bogħod: l-elevazzjoni tal-kanun għall-waqgħa tal-qoxra.

L-istati tal-vapuri għandhom layout ieħor; it-turrets tagħhom ma jinqrawx. L-ajruplani ma jibagħtu
ebda direzzjoni tar-ras jew tal-ħarsa; il-messaġġ 0xD020 tal-kanuni AA jibqa' mhux moqri.

## Il-kamera {#the-camera}

Il-messaġġ 0xD043, madwar 20 fis-sekonda, huwa l-kamera proprja tar-ripetizzjoni tal-plejer li
rreġistra: il-kamp 1 kwaternjon li jdawwar il-quddiem tal-kamera lejn fejn thares; 2 il-post tal-kamera
mill-vettura li tgħaqqab (m); 4 l-istess offset fil-qafas proprju tal-vettura (x 'il quddiem, y 'il
fuq, z lejn ix-xellug); 5 fejn jimmira l-plejer (vettur unità); 3 iz-zoom (madwar 1.2 fil-ħarsa tal-
persuna terza ta' tank, madwar 1.0 f'ajruplan, ogħla f'sight ta' gunner jew permezz ta' binokli).
Ikkontrollat: il-kamp 4 huwa l-kamp 2 imdawwar fil-qafas tal-vettura, fi ħdan 0.5 m għal kważi kull
messaġġ; il-quddiem tal-kamera għandu l-heading tal-aim. Ir-ripetizzjoni ma tibgħat ebda field of view
f'gradi, biss iz-zoom.

It-tabella għandha l-kamera bħala mogħdija għaliha: tip `camera`, mogħdija `<player> camera #ca`,
ringiela l-iktar kull 0.1 s, fil-post tal-vettura segwita flimkien mal-kamp 2, tħares tul il-kwaternjon
(`dirX/Y/Z`, `heading`, `pitch`, `roll`), bi `zoom`, `aimHeading` u `aimPitch`, u `otherLife` il-ħajja
li tsegwi. `selfCheck.camera` jgħodd ir-ringieli u l-kontroll.

## It-tmiem ta' mogħdija {#end-of-a-track}

Mogħdija tiġi mżebgħa mill-ewwel ringiela tagħha sal-aħħar waħda. Meta l-unità tagħha tkun marret
qabel it-tmiem tar-ripetizzjoni, l-aħħar ringiela tagħha hija ringiela `despawn` fl-aħħar post tagħha:
fil-ħin li l-logħba neħħiet l-entità tagħha (meta dan ġie fi ħdan 6 s mill-aħħar kampjun tagħha),
inkella fl-aħħar kampjun tagħha. Mogħdija mingħajrha ddum sa tmiem ir-ripetizzjoni. Ir-ringieli ta'
mogħdija waħda jistgħu jkunu 'il bogħod minn xulxin (unità 'l bogħod jew wreck jiġi aġġornat kull
ftit sekondi, wreck xi drabi mhux għal minuti): l-aħħar stat tiegħu jibqa' sakemm tiġi r-ringiela li jmiss.

## Battle mode {#battle-mode}

Il-byte tal-header f'offset 688 iżomm id-difficulty fl-erba' bits baxxi tiegħu: 0 arcade (AB),
5 realistic (RB), 10 simulator (SB). Ikkontrollat kontra t-tipi ta' battalji li kienu magħrufa
r-ripetizzjonijiet. Il-modalità tal-logħba hija `ground` meta l-missjoni tħalli tankijiet jispawnjaw,
inkella `naval` meta tħalli vapuri, inkella `air` (`allowedUnitTypes`); il-modalità proprja tal-missjoni
tiġi miċ-ċavetta tagħha (`missions/_Dom`), bl-isem mill-`lang/missions_versus.csv` tal-installazzjoni
tiegħek. Dik iċ-ċavetta stess hija l-parti `<mode>` tal-ismijiet tal-fajls u tal-id tal-partita (`Conq4`,
`Dom`), titħalla barra fejn il-header m'għandu l-ebda waħda.

---

Parti mid-[3DHeat](https://github.com/Holdi601/3DHeat) ([dokumentazzjoni](https://holdi601.github.io/3DHeat/)). Sors: [3DHeat-Ext-WarThunder](https://github.com/Holdi601/3DHeat-Ext-WarThunder).
