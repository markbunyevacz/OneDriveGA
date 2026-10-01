# Source-Registry — a felhasznált források nyilvántartása

Hozzáférési dátum minden külső forrásnál: **2026-09-30**. Szintek: L1 hivatalos/kormányzati · L2 szakmai/iparági jelentés ·
L3 szervezeti (hivatalos) dokumentáció · L4 hír/közösségi adat · L5 nem ellenőrizhető / önbevallott.

Csak olyan URL szerepel, amelyet ténylegesen megnyitottam (WebFetch, letöltés vagy API-lekérdezés). A keresési
találatok közül, amelyeket csak kivonatként láttam, egyiket sem hivatkozom.

| ID | Forrás | Típus | Szint | Hozzáférés | Felhasználva |
|---|---|---|---|---|---|
| S001 | Tulajdonilap-másolat (szemle), Pécs 4464/A/3 (lakás), 2026.09.30., elektronikusan hitelesítve; fájl: `EING-20260930-232416051_6cd2.pdf` | hivatalos nyilvántartás | L1 | feltöltött fájl (SHA-256: `Sources/README.md`) | adatlap.md, index.html, befektetesi-elemzes.md |
| S002 | Tulajdonilap-másolat (szemle), Pécs 4464/A/14 (garázs), 2026.09.30.; fájl: `EING-20260930-232247732_d174.pdf` | hivatalos nyilvántartás | L1 | feltöltött fájl (SHA-256: `Sources/README.md`) | adatlap.md, index.html, befektetesi-elemzes.md |
| S003 | Közjegyzői okirat (Pécs), 2026.09.22.; fájl: `41016_N_138_2026_13-41016_N_138_2026_13_ee97.pdf` | hivatalos okirat | L1 | feltöltött fájl (SHA-256: `Sources/README.md`) | adatlap.md (csak a 114 m² / 13 m² keresztellenőrzése) |
| S004 | A megadott ingatlan-adatlap („F0”), chat-szöveg; alapváltozata a git `9fe05c5` `adatlap.md` | önbevallott közlés | L5 | 2026-09-30 | minden leszállítandó (MEGADOTT jelöléssel, ahol nem igazolt) |
| S005 | Pécsi Városfejlesztési Zrt.: „Megtörtént a Zöld kapu projekt műszaki átadása, megújult a Hungária utca – Nagy Jenő utca – Petőfi utca által határolt terület” (közzétéve 2024.03.28.) — https://pvfzrt.hu/megtortent-a-zold-kapu-projekt-muszaki-atadasa-megujult-a-hungaria-utca-nagy-jeno-utca-petofi-utca-altal-hatarolt-terulet/ | megvalósító szervezet közleménye | L3 | WebFetch | adatlap.md, index.html, befektetesi-elemzes.md |
| S006 | Pécs Megyei Jogú Város: „Zöld kapu projekt” — https://pecs.hu/zold-kapu-projekt/ | önkormányzati oldal | L1 | WebFetch | adatlap.md, index.html |
| S007 | bama.hu, 2025.11.21.: „Így lett a PTE Magyarország legdiverzebb egyeteme” — https://www.bama.hu/helyi-kozelet/2025/11/egyetem-nemzetkozi-igazgatosag | hírcikk (a PTE Nemzetközi Igazgatóságának vezetőjét idézi) | L4 | WebFetch | adatlap.md, index.html, befektetesi-elemzes.md |
| S008 | PTE: „Nemzetközi képzések” — http://pte.hu/hu/oktatas/nemzetkozi-kepzesek | az egyetem hivatalos oldala, dátum nélkül | L3 | WebFetch | adatlap.md, index.html |
| S009 | Műemlékem.hu, Hungária u. 28. (azonosító 1695, törzsszám 22) — https://muemlekem.hu/muemlek/show/1695 | műemléki adatbázis; az állapotjelentések közösségiek | L3 (állapotjelentés: L4) | WebFetch | adatlap.md, index.html |
| S010 | Műemlékem.hu, Hungária u. 30. (azonosító 1696, törzsszám 23) — https://www.muemlekem.hu/muemlek/show/1696 | műemléki adatbázis; az állapotjelentések közösségiek | L3 (állapotjelentés: L4) | WebFetch | adatlap.md, index.html |
| S011 | Kormányhivatalok: „Tájékoztatás az örökségvédelmi engedélyezési eljárásról – műemlékvédelem” (feltöltés: 2024-06) — https://kormanyhivatalok.hu/sites/default/files/2024-06/1.-tajekoztatas-az-oroksegvedelmi-engedelyezesi-eljarasrol-muemlekvedelem.pdf | kormányhivatali tájékoztató | L1 | letöltve és szövegként elolvasva | adatlap.md, index.html, befektetesi-elemzes.md |
| S012 | © OpenStreetMap contributors (ODbL 1.0): Nominatim geokódolás és Overpass lekérdezés (OSM-adat időbélyege: 2026-05-06); szkript: `BuildScripts/osm_proximity_check.py` | közösségi térképadat | L4 | API-lekérdezés, 2026-09-30 21:47 UTC | adatlap.md, index.html, befektetesi-elemzes.md |
| S013 | 393/2012. (XII. 20.) Korm. rendelet, Nemzeti Jogszabálytár — https://njt.jog.gov.hu/jogszabaly/2012-393-20-22 | jogszabály, **2014.09.05-i időállapot** | L1, de elavult | WebFetch | **nem alkalmazott**: a hatályos (2026-os) szöveg nem ellenőrzött; csak a tájékozódást szolgálta |
| S014 | Költözzbe: „Pécs ingatlanárak” — https://koltozzbe.hu/ingatlan-statisztikak/pecs | kínálatiár-összesítő; a lakásállományt KSH-ra hivatkozva közli. A 72 077-et egy mondat lakóépületnek írja; a fejléc „összes lakás”, és az épületszám külön 24 819 | L4 (ár), L1 a KSH-idézetre, de a tábla külön nincs megnyitva | WebFetch, 2026.10.01. | ugynoki-ertekesitesi-tajekoztato.md, adatlap.md |
| S015 | bama.hu, 2026.05.17.: medián bérleti díj Pécsen — https://www.bama.hu/helyi-gazdasag/2026/05/pecsen-170-ezer-forint-a-median-berleti-dij | hír, a KSH–ingatlan.com lakbérindexet idézi | L4 | WebFetch, 2026.10.01. | ugynoki-ertekesitesi-tajekoztato.md, adatlap.md |
| S016 | bama.hu, 2026.02.18.: albérletárak és helyi értékesítői nyilatkozat — https://www.bama.hu/helyi-kozelet/2026/02/alberlet-pecsen-szeged-nyiregyhaza | hír | L4 | WebFetch, 2026.10.01. | ugynoki-ertekesitesi-tajekoztato.md, adatlap.md |

## Megjegyzések a források megbízhatóságáról

- **S011 és S013:** a műemléki engedélyezési szabályok tartalma időfüggő. Az S013 oldala 2014-es időállapotot mutat, ezért nem támaszkodtunk rá; az S011 2024-es feltöltésű tájékoztató. A hatályos állapot ellenőrzése `[NEEDS VERIFICATION]`.
- **S012:** a távolságok légvonalbeliek és közelítők (az épületet és a Steinmetz kapitány teret egy-egy geokódolt pont képviseli); az OSM-adat nem hivatalos, ezért az eltérés nem minősül „REFUTED”-nek.
- **S007:** a hallgatói létszám egy vezetői nyilatkozatból származik; az S008 (dátum nélkül) nagyságrendileg megerősíti.
- **S009, S010:** az életkor-jellemzés („kora eklektikus, 19. sz. második fele”) az adatbázis rövid leírásából származik; az állapotjelentés 2010-es.
- **Keresési összegzések:** a keresőeszköz automatikus összegzései közül egy (a műemléki tetőtér-beépítés „minden esetben” engedélyköteles voltáról) a megnyitott elsődleges források alapján **nem** igazolható ilyen élesen; a leszállítandók kizárólag az S011 megfogalmazását követik (a védelem fokától és a nevesített értékektől függ).
