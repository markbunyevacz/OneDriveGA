# Process-History — folyamatnapló

> **Megjegyzés a vezetésről.** A módszertan szerint a napló élőben, fázisonként frissül. Ez a napló a futás végén készült, az
> események tényleges sorrendjéből; az időpontok közelítő UTC-értékek a parancs- és commit-időbélyegekből. Ez eltérés a
> live-update szabálytól, amelyet a hibanapló E-10 tétele rögzít.

## 0. Domain-profil (P00)

| Elem | Érték |
|---|---|
| Domain | ingatlan-adatlap és -elemzés, magyar hivatalos dokumentumok alapján (általános profil) |
| Projekt | `pecs-hungaria-28-30` |
| Felülvizsgálati dimenziók | Technical · Business · Regulatory · Strategic · Financial · Operational |
| Kimeneti nyelv / forrásnyelv | magyar / magyar |
| L1 hatósági források | ingatlan-nyilvántartás (földhivatal), közjegyzői okirat, kormányzati tájékoztatók, jogszabálytár |
| Módszertani alkalmazás | teljes P00–P10 csővezeték (3+ forrásdokumentum; döntéstámogató tartalom) |

## 1. Fázisnapló

| Fázis | Név | Időablak (UTC, ~) | Állapot | Bemenetek | Kimenetek | Hibák |
|---|---|---|---|---|---|---|
| P00 | Bootstrap | 21:30–21:50 | kész; G0 nincs jóváhagyva | felhasználói kérés, módszertan | domain-profil, `Deliverables/` · `ProcessArtifacts/` · `Sources/`, `.gitignore`; commit `b960356` | E-04, E-12 |
| P01 | Forrás-ingesztió | 21:38–21:47 | kész; G1 nincs jóváhagyva | S001–S003, S004 | `Source-Inventory.md`, `extract_inventory.py` | E-02 |
| P02 | Kritikai átvilágítás | 21:40–22:10 | kész; G2 nincs jóváhagyva | leltár, S004 | `Gap-List.md` | — |
| P03 | Forrás-validálás | 21:40–22:10 | kész | 32 részállítás, S001–S003, webes és térképi ellenőrzés | `Validated-Claims.md`, `Source-Registry.md`, `verify_sources.py`, `osm_proximity_check.py` | E-03, E-05, E-06, E-07, E-08 |
| P04 | Prioritás | 22:10 | kész; G3 nincs jóváhagyva | hiánylista | 2. szakasz | — |
| P05 | Leszállítandók | 21:55–22:17 | kész; G4 nincs jóváhagyva | VCT, források | három leszállítandó frissítése; commit `1a8530f` | E-01, E-05 |
| P06 | Terv–tartalom ellenőrzés | 22:14–22:17 | kész; a mért lefedettség a `Plan-vs-Content.md`-ben | leszállítandók, VCT, forrásjegyzék | `Plan-vs-Content.md`, mutációs teszt | — |
| P07 | Hiánypótlás | — | nem kellett: az első teljes futás 100% volt | — | — | — |
| P08 | Fordítás | — | nem alkalmazható (forrás és kimenet magyar); Verification-Report nem készül | — | — | — |
| P09 | Fúzió | — | nem alkalmazható (nincs összefésülés) | — | — | — |
| P10 | Konszolidáció | 22:18–22:35 | kész | minden artefaktum | `Traceability-Matrix.md`, `Spot-Check-Guide.md`, `Process-History.md`, `Manifest.md`, csomag-README | E-09, E-10, E-11, E-13, E-14, E-15 |

## 2. Munkacsomagok (P04)

| WP | Szint | Hiányok | Leírás | Kimenet |
|---|---|---|---|---|
| WP-1 | P0 | G-01 | Adatvédelmi védelem: a forrás-PDF-ek kizárása a repóból, a személyes és pénzügyi részletek elválasztása a nyilvános anyagoktól | `.gitignore`, `Sources/README.md`, privát elemzés (a repón kívül) |
| WP-2 | P0 | G-02, G-03, G-04, G-05, G-06, G-07, G-08, G-09, G-10, G-12 | A hivatalos és külső adatok beépítése a leszállítandókba, korrekciókkal és státuszjelöléssel | `adatlap.md`, `index.html`, `befektetesi-elemzes.md` |
| WP-3 | P1 | G-11 | Az első változat forrás nélküli állításainak eltávolítása vagy hipotézisként jelölése | Validated-Claims C. tábla |
| WP-4 | P1 | G-03, G-08, G-09, G-10 | Külső ellenőrzés: Zöld kapu, PTE, műemléki szabályok, megállótávolság | `Source-Registry.md`, `osm_proximity_check.py` |
| WP-5 | P2 | — | Módszertani artefaktumok és reprodukálható szkriptek | `ProcessArtifacts/` |

## 3. Gate-napló

A futás nem interaktív (felhő-ügynök), ezért felhasználói jóváhagyás **egyik kapunál sem** érkezett. A módszertan szerint ilyenkor nem szabad
jóváhagyottnak tekinteni a kaput; ezért minden kapu NEM JÓVÁHAGYOTT, a leszállítandók DRAFT státuszúak, és a munka visszafordítható
(külön commitok, draft pull request, nincs merge).

| Kapu | Kérdés | Állapot | Megjegyzés |
|---|---|---|---|
| G0 | A domain-profil és a szerkezet helyes? | NEM JÓVÁHAGYOTT | profil: 0. szakasz |
| G1 | A forrásleltár teljes? | NEM JÓVÁHAGYOTT | `Source-Inventory.md` |
| G2 | Megerősíti a hiánylistát? | NEM JÓVÁHAGYOTT | `Gap-List.md` |
| G3 | Jóváhagyja a munkacsomagokat? | NEM JÓVÁHAGYOTT | 2. szakasz |
| G4 | Jóváhagyja a tervet? | NEM JÓVÁHAGYOTT | a terv a `Plan-vs-Content.md` tételei |
| G5 | A csomag lezárható? | NEM JÓVÁHAGYOTT | felhasználói felülvizsgálat és PR-jóváhagyás kell |
| G6 | A fúzió jóváhagyható? | nem alkalmazható | nincs fúzió |

## 4. Döntésnapló

| ID | Fázis | Döntés | Megfontolt lehetőségek | Választás és indok | Felhasználó jóváhagyta |
|---|---|---|---|---|---|
| D-01 | P00 | A módszertan alkalmazási szintje | teljes csővezeték · könnyített részhalmaz | teljes: 3 forrásdokumentum, döntéstámogató tartalom | N |
| D-02 | P00 | Kapuk kezelése nem interaktív futásban | megállás a kapunál · továbblépés jóváhagyottnak tekintve · továbblépés nem jóváhagyott státusszal | továbblépés NEM JÓVÁHAGYOTT státusszal, DRAFT leszállítandókkal, draft PR-rel: a kérdések nem válaszolhatók meg futás közben, a munka visszafordítható | N |
| D-03 | P03 | A VERIFIED küszöb értelmezése | kétforrás-kötelezettség minden állításra · L1 egyforrás + két egymást megerősítő alsóbb forrás | VERIFIED = egy L1 nyilvántartási forrás vagy legalább két egymást megerősítő forrás; az összetett állításokat részállításokra bontottuk | N |
| D-04 | P02 | A teljesség kifejezése | százalék · minőségi szint | minőségi szint (FULL/PARTIAL/NONE): a százalék megalapozatlan pontosságot sugallna | N |
| D-05 | P00–P10 | Adatvédelem (a repó nyilvános) | minden dokumentum és adat commitolása · anonimizálás · a részletek kizárása a repóból | a forrás-PDF-ek nem kerülnek a repóba (`.gitignore`); a nyilvános anyagok csak az ingatlan jellemzőit tartalmazzák; a tulajdonviszonyokra, terhekre, értékekre és személyes adatokra vonatkozó elemzés a repón kívül van; a harmadik dokumentum kulcstémái nincsenek felsorolva; a nyilvános fájlokban semleges kód (`KO`) szerepel | N |
| D-06 | P10 | A módszertan „eredeti fájlok másolása a Sources/ mappába” lépése | commitolás · helyi másolat hash-listával | helyi másolat, a hash-lista a `Sources/README.md`-ben: a fájlazonosság igazolható, a tartalom nem nyilvános | N |
| D-07 | P05 | A részletes jogi elemzés helye | nyilvános repó · privát repó · az ügynök privát tára | az ügynök privát tára (a repón kívül); a felhasználó a futás végén kapott összefoglalóból éri el | N |
| D-08 | P03 | Külső források elfogadása | minden találat · csak megnyitott és elolvasott oldal | csak megnyitott oldalak; a keresőeszköz automatikus összegzése nem elsődleges forrás; az elavult időállapotú jogszabályoldal nem alkalmazott | N |
| D-09 | P05 | Az első változat forrás nélküli állításai | hallgatólagos törlés · jelölt törlés és naplózás | törlés vagy átírás, a Validated-Claims C. táblában és az E-01 hibanaplóban naplózva | N |
| D-10 | P05 | A korrigált megadott értékek | csere a hivatalos értékre · a régi érték elrejtése · mindkettő láthatóan | mindkettő: a hivatalos érték szerepel, mellette „megadott: …” (a módszertan szerint a korrigált állítás nem tűnhet el hallgatólagosan) | N |
| D-11 | P10 | Git-kezelés | új ág és új PR · a meglévő ág és PR frissítése | a meglévő ág és draft PR frissítése, logikai egységenként külön commit; nincs amend és nincs force push | N |
| D-12 | P03 | Hasznosítási ötletek ellenőrzése | bevonás a VCT-be · kizárás | kizárás: nem tényállítások | N |
| D-13 | P03 | A műemlékadatbázis szintje | L2 · L3 · L4 | L3 (a rövid leírás); a közösségi állapotjelentés L4 | N |

## 5. Hibanapló

| ID | Fázis | Típus (taxonómia) | Leírás | Eszkaláció | Megoldás | Időráfordítás |
|---|---|---|---|---|---|---|
| E-01 | P05 (1. kör) | Hallucinated Data | Az első változat forrás nélküli állításokat tartalmazott (kitalált kihasználtsági arányok, piaci ritkaság és árprémium, „gyalogos elérés”, „termikus inercia” stb.) | nincs szükség újrapróbálkozásra; közvetlen javítás | törlés vagy hipotézis-jelölés; 14 tétel a Validated-Claims C. táblában; 15 tiltott állítás hiányát a `plan_vs_content.py` ellenőrzi; commit `1a8530f` | nem mért |
| E-02 | P01 | API Mismatch | A `pypdf` képszámlálása Pillow nélkül hibát adott | 1. lépés: javítási kísérlet nem volt, azonnali váltás | az oldalszintű kép-XObjectek számlálása dekódolás nélkül | nem mért |
| E-03 | P03 | Silent Verification (téves FAIL) | A `verify_sources.py` V14/V15 ellenőrzése hamisan FAIL-t adott: a PDF-ből kinyert szövegben a „m²” szétválik („m 2”) | újrapróbálkozás tűrő reguláris kifejezéssel | 23/23 PASS | nem mért |
| E-04 | P00 | Batch Processing Failure | Párhuzamosan indított hívások közül egy `git add` a célfájl létrejötte előtt futott („pathspec did not match”) | újrapróbálkozás a fájl létrejötte után | sikeres; a függő lépések nem indíthatók párhuzamosan | nem mért |
| E-05 | P05 | Silent Verification (kockázat) | A headless Chrome nem lépett ki, a képernyőkép-leírás pontatlan részleteket tartalmazott | váltás: PDF-nyomtatás időkorláttal, a kinyert szöveg ellenőrzése | a képleírás nem szolgált tényellenőrzésre; a kulcsadatok jelenléte és a törölt állítások hiánya szöveges ellenőrzéssel igazolt | nem mért |
| E-06 | P03 | Hallucinated Data (eszköz-összegzés) | A keresőeszköz összegzése szerint a műemléki tetőtér-beépítés „minden esetben” engedélyköteles; ez a megnyitott források alapján nem igazolható ilyen élesen | váltás az elsődleges forrásra | a leszállítandók az S011 megfogalmazását követik (a védelem fokától és a nevesített értékektől függ) | nem mért |
| E-07 | P03 | Outdated Data | Az NJT 393/2012 oldala 2014-es időállapotot mutat (kétszer ellenőrizve) | váltás az S011 kormányhivatali tájékoztatóra | S013 „nem alkalmazott”; a hatályos szöveg ellenőrzése `[NEEDS VERIFICATION]` | nem mért |
| E-08 | P03 | API Mismatch | Az Overpass elsődleges végpont 406-os hibát adott | váltás tükörszerverre | az eredmény megszületett; a szkript mindkét végpontot próbálja | nem mért |
| E-09 | P10 | Silent Verification | A privát ellenőrző szkript eredményének darabszáma tévesen szerepelt (26 a valós 23 helyett) | újramérés | javítva: 23/23 | nem mért |
| E-10 | P10 | (folyamat) | A napló nem élőben, hanem a futás végén készült | — | utólagos összeállítás, megjegyzéssel a napló elején | — |
| E-11 | P10 | Batch Processing Failure | Egy gyorsítótár-fájl (`__pycache__`) a commitolható fájlok közé került | észlelés commit előtt | `.gitignore` bővítése, a mappa törlése | nem mért |
| E-12 | P00 | (adatvédelem) | A `Sources/README.md` első commitja (`b960356`) a harmadik dokumentum típusát részletesebben nevezte meg; a csúcson (`0dc9fe1` óta) semleges szöveg áll. A git-előzményt nem írtam át (a szabályok tiltják az amend-et), ezért a korábbi szöveg az ág közzétételével az előzményben nyilvános lesz | döntés: az előzmény átírása a git-szabályok miatt nem történt meg | a csúcson semleges; az érintett szöveg nem tartalmaz nevet, azonosítót vagy összeget | — |
| E-13 | P10 | Batch Processing Failure | A `build_manifest.py` első futása 0 fájlt listázott (hibás útvonal-összefűzés a git-kimenet relatív útjaival), a kimenet hibajelzés nélkül üres volt | észlelés a kimenet átolvasásakor; javítási kísérlet | az útvonalak a csomag gyökeréhez viszonyítva; védőellenőrzés: üres leltárnál a szkript hibával lép ki | nem mért |
| E-14 | P10 | Silent Verification (téves riasztás) | Az adatvédelmi lint érzékeny kifejezést jelzett a folyamatnaplóban: a „megszületett” szó tartalmazza a keresett alsztringet | újrapróbálkozás | a minta szóhatárra igazítva (a ragozott alakokat továbbra is elkapja); a mutációs teszt érzékenysége nem romlott | nem mért |
| E-15 | P10 | Silent Verification (téves riasztás) | A manifest 15 „ellenőrzési problémát” jelzett: a „nincs helykitöltő” üzenet tartalmazza a „helykitöltő” szót | újrapróbálkozás | a problémaüzenetek pontos egyezéssel vizsgálva; 0 probléma | nem mért |

## 6. Ellenőrzések mért eredményei

| Ellenőrzés | Eredmény | Eszköz |
|---|---|---|
| Fájlazonosság és tartalmi tények a PDF-ekből | 23/23 PASS | `verify_sources.py` |
| Terv–tartalom lefedettség | lásd `Plan-vs-Content.md` | `plan_vs_content.py` |
| **Mutációs teszt** (megrongított másolat: hiányzó érték, beszúrt tiltott állítások, beszúrt azonosító- és e-mail-minta) | 44/48 = 91,7% (PARTIAL 1, DIVERGED 3), adatvédelmi lint FAIL, kilépési kód 1: az ellenőrző érzékeny | egyszeri, nem mentett futás |
| Helyi névkereső átvizsgálás (nevek, címek, hitelezők, összegek és tulajdoni hányadok mintái; a minták nem kerültek a repóba) | 0 találat | egyszeri, nem mentett futás |
| A privát elemzés számellenőrzése | 23/23 PASS | privát szkript (a repón kívül) |

## 7. Fájl-idővonal

| Fájl | Létrehozva | Módosítva | Állapot |
|---|---|---|---|
| `Deliverables/adatlap.md`, `index.html`, `befektetesi-elemzes.md` | 1. kör (`9fe05c5`) | P00 (áthelyezés), P05 (`1a8530f`) | DRAFT |
| `README.md` | 1. kör | P10 | DRAFT |
| `.gitignore`, `Sources/README.md` | P00 (`b960356`) | P01 (`0dc9fe1`) | OK |
| `ProcessArtifacts/BuildScripts/*` | P01–P10 (`0dc9fe1`) | `plan_vs_content.py`, `build_manifest.py`: P10-ben javítva (E-13–E-15) | TESTED |
| `Source-Inventory.md`, `Gap-List.md`, `Validated-Claims.md`, `Source-Registry.md` | P01–P03 (`589631e`) | — | DRAFT |
| `Plan-vs-Content.md`, `Traceability-Matrix.md`, `Spot-Check-Guide.md`, `Process-History.md`, `Manifest.md` | P06, P10 | — | DRAFT |

## 8. Felhasználói döntést igénylő pontok

1. **G0–G5 jóváhagyása:** a domain-profil, a forrásleltár, a hiánylista, a munkacsomagok és a terv megerősítése (a kapuk jelenleg NEM JÓVÁHAGYOTT állapotúak).
2. **Padlástér-terület:** a nyilvántartási 95 m² vagy a megadott 100 m² az irányadó; helyszíni felmérés kell.
3. **Cél:** hirdetés vagy belső elemzés. Hirdetés előtt a tulajdonjogi helyzet és a terhek jogi ellenőrzése szükséges.
4. **Adatvédelmi szétválasztás elfogadása:** a részletes jogi elemzés a repón kívül van; ha másképp kéri, jelezze.
5. **Nem igazolt adatok pontosítása:** A osztály (tanúsítvány), a 143 m-es megállótávolság, a parkoló és a garázs kapcsolata.
6. **A repó láthatósága nyilvános.** Érdemes megfontolni, hogy az ilyen csomag privát tárolóba kerüljön.

## 9. Kiegészítés, 2026.10.01. — ügynöki tájékoztató

A kérés: professzionális leírás, amely az értékesítőt a pécsi viszonyok között előnyös pozíció felé viszi, és ahol a tény kérdéses, ott kérdez. Új közlés: a lakáshoz hatalmas, közös pince tartozik.

| Döntés | Választás |
|---|---|
| D-14 | A meggyőzés a mért méretkülönbségre és két vevői körre épül (család / befektető), nem kitalált „legjobb utca” vagy hozam állításra |
| D-15 | A pince megadott adat. A 209 m²-be nem számoljuk, amíg nincs területe. A hirdetésbe „saját pinceként” nem kerül, amíg a jogcím nincs meg |
| D-16 | A kínálati ár vetítése (kb. 108 M Ft) nagyságrend, nem kikiáltási ár. Az ár a 8. fejezet válaszai előtt nem publikálandó |

A 13 kérdés a `Deliverables/ugynoki-ertekesitesi-tajekoztato.md` 8. fejezetében van. Válasz nélkül a tájékoztató tervezet marad.

A 12,9%-os lakásállomány-arány az S014 oldal saját számainak olvasata (2026.10.01., WebFetch). Az oldal egy mondatban lakóépületnek nevezi a 72 077-et; a fejléc „összes lakás”, és az épületeket külön, 24 819-ként számolja. A KSH-tábla továbbra sincs megnyitva. A Hungária utcai 29,9 M Ft-os, 1 szobás hirdetés ugyanazon az oldalon másik ingatlan, áralapnak nem használtuk.

## 10. Kiegészítés, 2026.10.01. — tulajdonosi válaszok

A 8. fejezet 13 kérdésére válasz érkezett. Státuszuk megadott: okirat, tanúsítványmásolat és társasházi kimutatás nem került a csomagba.

| Döntés | Választás |
|---|---|
| D-17 | A 80 m²-es, 4–5 m belmagasságú pince a ház közös pincéje. A 114 m²-hez és a 209 m²-hez nem adódik hozzá, a hirdetésben saját pinceként nem szerepel |
| D-18 | A zárt udvari parkoló a tulajdonos szerint a 4464/A/14 garázs, és az eladási ár része. A tulajdoni lapon lévő teher miatt tehermentes átruházás nincs ígérve |
| D-19 | A padlás helyszíni mérete a tulajdonos szerint 95 m², gerinc 4,5 m, térdfal 1,3 m. A 100 m²-es korábbi közlés lezárható. Állómagasságú nettó területet nem számolunk |
| D-20 | Az A osztály a tulajdonos szerint tanúsítvánnyal igazolt, de azonosító és kelte nélkül a hirdetésben csak a tulajdonosra hivatkozva szerepelhet. A „max 7-7 éves” kazánközlést egy készüléknek értjük |
| D-21 | A kikiáltási ár továbbra sem a 108 M Ft-os vetítés. A termék már leírható; az árat 3–5 szigeti, garázsos hirdetéshez kell tenni, és a tulajdonos hagyja jóvá |

Nyitva: a tanúsítvány kelte és hiteles azonosítója, a járat neve, és hogy a kazán egy készülék-e.
