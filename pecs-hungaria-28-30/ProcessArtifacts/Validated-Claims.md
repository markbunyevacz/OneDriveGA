# Validated-Claims — P03 forrás-validálás

Ellenőrzés napja: 2026-09-30. Az ellenőrzött állítások forrása a megadott ingatlan-adatlap (S004, „F0”).
Forráskódok: lásd `Source-Registry.md`. Hozzáférési szintek: L1 hivatalos, L2 iparági/szakmai, L3 szervezeti dokumentáció, L4 hír/közösségi, L5 nem ellenőrizhető.

**Státuszok (módszertan szerint):** VERIFIED · CORRECTED · OUTDATED · UNVERIFIABLE · REFUTED.

**Alkalmazott döntések** (részletek: `Process-History.md`, D-03): a VERIFIED státuszhoz vagy egy L1 nyilvántartási forrás,
vagy legalább két egymást megerősítő forrás szükséges; az összetett állításokat részállításokra bontottuk;
a nem tényállítás jellegű hasznosítási ötletek (F0 „Potenciális felhasználás”) nem ellenőrizendők, ezért nem szerepelnek a táblázatban.

## A. Az F0 állításainak validálása

| ID | Állítás (F0) | Típus | Státusz | Ellenőrző forrás(ok) | Megjegyzés | Deliverable-frissítés |
|---|---|---|---|---|---|---|
| C01 | Cím: Pécs, Hungária utca 28–30., 1. emelet | Technical Spec | VERIFIED | S001 fejléc (A. ép. 1. em. 1. ajtó, hrsz. 4464/A/3); S003 hivatkozás; S009, S010 (hrsz. 4464) | Pontosítás: 7624, A. épület, 1. ajtó, hrsz. | adatlap §1; index hero, 01 |
| C02 | Belváros-közeli prémium lokáció, Pécs egyik legjobb utcája | Market Data | UNVERIFIABLE | — | Minősítő vélemény, nem mérhető | adatlap §2 (MEGADOTT) |
| C03a | Zöld kapu projekt: a Hungária u. – Nagy Jenő u. – Petőfi u. által határolt terület megújítása | Date/Deadline | VERIFIED | S005, S006 | A projekt létezik; azonosító és hely a forrásokban | adatlap §2; index 01 |
| C03b | „2023-ban megújult” | Date/Deadline | CORRECTED | S005, S006 | Vállalkozói szerződés 2023.09.27.; projektzáró esemény 2024.03.28. (park hivatalos megnyitója 2024 áprilisára tervezve); a projektoldal tervezett zárása: 2023.12.31. | lásd B. tábla |
| C03c | Az *utca* (az ingatlan környezete) újult meg | Technical Spec | CORRECTED | S005, S006, S012 | Közösségi tér (Steinmetz kapitány tér), az épülettől kb. 660 m légvonalban (OSM geokódolt pont, közelítő); az ingatlan közvetlen utcaszakaszának megújulása nem igazolt | lásd B. tábla |
| C03d | Új sétányok, parkosítás, EV-töltők | Technical Spec | VERIFIED | S005, S006 | Akadálymentes sétányok és járdák; ~2000 m² füvesítés, 50+ fa; 2 elektromos autótöltő (4 gépjármű) | adatlap §2; index 01 |
| C03e | Új kerékpárutak | Technical Spec | CORRECTED | S005, S006 | Kerékpárutat a megnyitott források nem említenek; 13 kerékpártárolót igen | lásd B. tábla |
| C04a | 143 méterre tömegközlekedési megálló | Statistic | UNVERIFIABLE | S012 (ellenpróba) | A legközelebbi feltérképezett megálló kb. 221 m légvonalban; a 143 m nem reprodukálható; a mérés pontja ismeretlen; az OSM nem hivatalos forrás, ezért nem REFUTED | adatlap §2, §8; index 01, 06; analysis §1 |
| C04b | Közvetlen PTE-összeköttetés | Technical Spec | UNVERIFIABLE | S005, S006 (kontextus) | A Zöld kapu-terület a „Kelet-nyugati közösségi közlekedési tengely” végállomásához kapcsolódik, cél a Belváros–Campus összekötés; konkrét járat nem igazolt | adatlap §2 |
| C05a | 100+ éves épület | Date/Deadline | VERIFIED | S001 I.2 (műemlék); S009, S010 (kora eklektikus, 19. sz. második fele) | Az életkor egy külső adatbázisból ered, konzisztens a hivatalos műemléki jelleggel | adatlap §2; index 01 |
| C05b | Téglaépület | Technical Spec | UNVERIFIABLE | — | Az építőanyag egyik forrásban sem szerepel | adatlap §2 |
| C06 | Utcafront felújításra szorul; közös területek használtak, de takarítottak | Technical Spec | UNVERIFIABLE | S009, S010 (2010-es állapotjelentés, kontextus) | A 2010-es közösségi állapotjelentés („elhanyagolt, tatarozni kellene”) 16 éves; a mai állapotot nem igazolja | adatlap §2, §8 |
| C07a | PTE közvetlen közelében | Technical Spec | UNVERIFIABLE | — | Távolság nem ellenőrzött | adatlap §2 |
| C07b | 4000+ külföldi hallgató | Statistic | OUTDATED | S007 (5553, 2025-11), S008 (több mint 5600, 146 ország, dátum nélkül) | A „4000+” igaz alsó becslés, de elavult | lásd B. tábla |
| C07c | Aktív bérlői/vevői kereslet | Market Data | UNVERIFIABLE | S007 (kontextus: kollégiumi kapacitásbővítés sürgős feladat) | A hallgatói létszám nem azonos a magánbérleti kereslettel | adatlap §2; analysis §2–3 |
| C08 | Társasházi lakás | Technical Spec | VERIFIED | S001 I.1, I.3 | Rendeltetés: lakás; jogi jelleg: társasház | adatlap §1, §3 |
| C09 | 1. emelet | Technical Spec | VERIFIED | S001 fejléc | — | adatlap §1, §3 |
| C10 | Alapterület: 114 m² | Statistic | VERIFIED | S001 I.1; S003 (hivatkozás) | Két L1 forrás egyezik | adatlap §1, §3; index stats |
| C11a | Tetőtér: 100 m² | Statistic | CORRECTED | S001 I.4 („95 nm padlástér”) | A nyilvántartás szerint 95 m² (−5 m², −5,0%); a bejegyzés régi, felmérés szükséges | lásd B. tábla |
| C11b | Nyers, beépítetlen állapot | Technical Spec | UNVERIFIABLE | — | Fizikai állapot, helyszíni szemle kell | adatlap §3, §6 |
| C11c | Engedély megszerezhető; szinte falig/tetőig beépíthető | Legal Requirement | UNVERIFIABLE | S001 I.2, S009, S010, S011 (kontextus) | Az épület műemlék; az örökségvédelmi engedély szükségessége a védelem fokától és a nevesített értékektől függ; alapító okirat és építési hatóság is releváns | adatlap §6, §8; index 05; analysis §1, §5, §7 |
| C12 | Összes potenciális terület: ~214 m² | Statistic | CORRECTED | S001 I.4 (számított) | 114 + 95 = 209 m² (az F0 belső számítása 114 + 100 = 214 konzisztens volt) | lásd B. tábla |
| C13 | Déli tájolás | Technical Spec | UNVERIFIABLE | — | Nem dokumentált | adatlap §3 |
| C14 | Nincs erkély/terasz | Technical Spec | UNVERIFIABLE | — | A nyilvántartás nem tünteti fel; a hiány nem bizonyíték | adatlap §3 |
| C15 | Saját gázkazán (önálló szabályozás) | Technical Spec | UNVERIFIABLE | — | Nem dokumentált | adatlap §4 |
| C16 | Modern, jó állapotú nyílászárók, csere nem szükséges | Technical Spec | UNVERIFIABLE | S011 (kontextus) | Műemléknél a nyílászárók felújítása/cseréje engedélyköteles lehet | adatlap §4 |
| C17 | Energetikai besorolás: A osztály | Performance Claim | UNVERIFIABLE | — | Tanúsítvány nem áll rendelkezésre | adatlap §4; index 03 |
| C18 | 2006-ban felújított, azóta egyetlen személy lakta, közepes-jó állapot | Date/Deadline | UNVERIFIABLE | — | A dokumentumokból nem állapítható meg | adatlap §4 |
| C19 | Zárt belső udvari parkoló | Technical Spec | UNVERIFIABLE | S002 (kontextus) | A nyilvántartásban külön önálló ingatlan a garázs (13 m²); a kapcsolat ismeretlen | adatlap §5; index 04 |
| C20 | Közös költség ~20 000 Ft/hó | Cost Estimate | UNVERIFIABLE | — | Társasházi kimutatás nincs | adatlap §5 |
| C21a | A lakáshoz lépcsőház tartozik | Technical Spec | VERIFIED | S001 I.4 („10.44 nm lépcsőházzal”) | 10,44 m² | adatlap §1, §5; index 02 |
| C21b | Saját, privát lépcsőház, nem osztott más lakással | Legal Requirement | UNVERIFIABLE | S001 I.3–I.4 (konzisztens) | Az alapító okirat nem áll rendelkezésre | adatlap §3, §5 |
| C22 | A lakáshoz hatalmas, közös pince tartozik | Technical Spec | UNVERIFIABLE | S004 (kiegészítés, 2026.10.01.); S001 nem tartalmaz pinceterületet | Tulajdonosi közlés. Méret, jogcím és bejárat hiányzik | adatlap §5; index 04; ugynoki-ertekesitesi-tajekoztato.md |

**Összesítés:** VERIFIED: 8 · CORRECTED: 5 · OUTDATED: 1 · UNVERIFIABLE: 19 · REFUTED: 0 · Összesen: 33

## B. A CORRECTED / OUTDATED állítások részletei (módszertani kötelezettség)

| ID | original_claim | correction | correction_source | deliverable_updated | update_description |
|---|---|---|---|---|---|
| C03b | „2023-ban megújult utca” | A munkák 2023 szeptemberében indultak (vállalkozói szerződés 2023.09.27.), a projektzáró esemény 2024.03.28. | S005, S006 | adatlap.md §2; index.html 01 | „2023–2024” időzítés, dátumokkal |
| C03c | „megújult utca” (az ingatlan utcaszakasza) | A megújított tér a Hungária u. – Nagy Jenő u. – Petőfi u. által határolt Steinmetz kapitány tér, az épülettől kb. 660 m-re (légvonal, közelítő) | S005, S006, S012 | adatlap.md §2, §7; index.html 01, 06; befektetesi-elemzes.md §2 | A tér megnevezése és a távolság; „az ingatlan közvetlen utcaszakaszának megújulása nem igazolt” |
| C03e | „kerékpárutak” | A források 13 kerékpártárolót említenek, kerékpárutat nem | S005, S006 | adatlap.md §2; index.html 01 | A kerékpárút törölve a beruházás elemei közül, a megadott szöveg „Megadott:” idézetként megmaradt |
| C07b | „4000+ külföldi hallgató” | 5553 külföldi hallgató (2025. nov.); a PTE oldala „több mint 5600” | S007, S008 | adatlap.md §2, §7; index.html 01, 06; befektetesi-elemzes.md §1, §3 | Aktuális szám, a régi érték „elavult alsó becslés”-ként jelölve |
| C11a | „Tetőtér: 100 m²” | 95 m² | S001 I.4 | adatlap.md fejléc, §1, §3, §6, §7, §8; index.html hero, stats, 02, 05; befektetesi-elemzes.md §1, §3, §5, §6, §9 | A hivatalos 95 m² szerepel, a megadott 100 m² „megadott:” jelöléssel mellette |
| C12 | „~214 m²” | ~209 m² (114 + 95) | S001 I.4 (számított) | adatlap.md fejléc, §3; index.html hero, stats, 02; befektetesi-elemzes.md §1, §3, §5, §9 | A potenciál újraszámolva; a megadott érték jelölve; a 10,44 m² lépcsőház nem része az összegnek |

## C. Korábbi (az AI által írt) leszállítandók forrás nélküli állításai — korrekció

Az első változat (git `9fe05c5`) az alábbi, sem az F0-ban, sem a forrásokban nem szereplő állításokat tartalmazta. A módszertan szerint ezek
„nem megengedett, forrás nélküli” állítások; javításuk az `Error Log` E-01 bejegyzésében is szerepel.

| ID | Korábbi állítás | Probléma | Intézkedés |
|---|---|---|---|
| A01 | „kiváló akusztika és termikus inercia” (index.html) | forrás nélküli | REMOVED |
| A02 | „PTE-hez közvetlen, gyalogos elérés” (index.html) | az F0 a tömegközlekedésnél írt „közvetlen PTE-összeköttetés”-t; a „gyalogos” kitalált | REMOVED; az F0 szöveg státusszal szerepel |
| A03 | „magas belmagasságú tér” (galériás kialakítás) | forrás nélküli | REMOVED |
| A04 | „kihasználtsági ráta (hosszú táv: 95 %+, közepes táv: 70–85 %)” | kitalált statisztika | REMOVED; a ráta piaci adatból határozandó meg `[ASSUMPTION]` |
| A05 | „Pécs nem tipikus Airbnb-város, de vannak szezonális események (konferenciák, fesztiválok, PTE nyitási időszakok)” | forrás nélküli | REPLACED: hipotézis + S007 (nyári-téli egyetemek) |
| A06 | „szűk kínálati szegmens … jobb megtartja értékét”, „strukturálisan kínálathiányos”, „Pécs piacán ritka” | forrás nélküli piaci állítások | REMOVED; hipotézisként, piaci adat hiányában jelölve |
| A07 | Csillagos súlyozás; „a belvárosi átlag fölött” | forrás nélküli szubjektív értékelés | REMOVED; irány-oszlop hipotézisként |
| A08 | „az önálló gázkazán miatt a fűtés nincs benne közösként” | következtetés, nem forrás | REMOVED |
| A09 | „a fejlesztés után eladás … jellemzően a legnagyobb abszolút értéknövekedést adja” | forrás nélküli | REMOVED |
| A10 | „a lokáció és adottságok tompítják a volatilitást” | forrás nélküli | REMOVED |
| A11 | „2006 óta felújítás nem történt” | az F0 csak a 2006-os felújítást állítja | REWRITTEN: „A felújítás 2006-ban történt (MEGADOTT)” |
| A12 | „rendkívül ritka társasházi adottság, diszkréció és biztonság”, „szinte önálló ház” | forrás nélküli / vélemény | REMOVED |
| A13 | „Zárt udvari parkoló — belvárosban erősen értéknövelő tényező” | vélemény | REMOVED |
| A14 | „Engedélyezés (társasházi hozzájárulás + építési engedély)” | hiányos: a műemléki eljárás nem szerepelt | REWRITTEN: örökségvédelmi + építési hatósági eljárás, alapító okirat `[NEEDS VERIFICATION]` |
