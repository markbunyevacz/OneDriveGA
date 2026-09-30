# Gap-List — P02 kritikai átvilágítás

Domain-profil (P00): általános profil — Technical · Business · Regulatory · Strategic · Financial · Operational
(az anyagok ingatlan-adatlap és -elemzés; a hivatalos dokumentumok a Regulatory dimenzióba esnek).

## 1. Lefedettség dokumentumonként és dimenziónként

A teljesség **minőségi szinttel** szerepel (FULL / PARTIAL / NONE), nem százalékkal: egy százalékos érték
itt megalapozatlan pontosságot sugallna (döntés: Process-History D-04).

| Dimenzió | S001 (TL-A3) | S002 (TL-A14) | S003 (KO) | S004 (F0) |
|---|---|---|---|---|
| Technical | PARTIAL — terület, szobák, tartozékok | PARTIAL — terület | PARTIAL — terület-hivatkozás | FULL tartalom, **nem igazolt** |
| Business | NONE | NONE | NONE | PARTIAL — kereslet, pozicionálás, **nem igazolt** |
| Regulatory | FULL — jogi jelleg, helyrajzi szám | FULL | PARTIAL | NONE |
| Strategic | NONE | NONE | NONE | PARTIAL — lokáció, PTE, **nem igazolt** |
| Financial | NONE | PARTIAL — teherbejegyzések (nem részletezve) | PARTIAL (nem részletezve) | PARTIAL — közös költség |
| Operational | NONE | NONE | PARTIAL | PARTIAL — állapot, **nem igazolt** |

## 2. Dokumentumok közti következetesség

- S001 ↔ S003: a lakás helyrajzi száma és területe egyezik (114 m²). S002 ↔ S003: a garázs helyrajzi száma és területe egyezik (13 m²). Számszaki ellentmondás a hivatalos dokumentumok között: **0**.
- S004 ↔ S001: **2** számszaki eltérés — padlástér 100 vs. 95 m² (−5,0%); származtatott potenciál 214 vs. 209 m².
- Külső benchmark: az épület műemléki nyilvántartásban is szerepel (S009, S010), konzisztens a hivatalos jogi jelleggel. A műemléki engedélyezési szabályok benchmarkja az S011; a hatályos állapot nem ellenőrzött.

## 3. Hiánylista

| ID | Forrás | Dimenzió | Leírás | Súlyosság | Bizonyíték |
|---|---|---|---|---|---|
| G-01 | S004 vs. S001–S003 | Regulatory / Risk | Az F0 nem tartalmaz tulajdonjogi és értékesíthetőségi információt; a hivatalos dokumentumok szerint a tulajdonjogi helyzet nem tekinthető lezártnak, ezért hirdetés vagy értékesítés előtt jogi ellenőrzés szükséges. A részletek személyes adatokat tartalmaznak, ezért privát anyagban vannak. | CRITICAL | S001, S003 (részletek nem a repóban) |
| G-02 | S004 vs. S001 | Technical | Padlástér: 100 m² (F0) vs. 95 m² (nyilvántartás); a 10,44 m² lépcsőház az F0-ban nem szerepel | HIGH | S001 I.4 (ellenőrzés V06, V07) |
| G-03 | S004 vs. S001, S002 | Regulatory | A műemléki jogi jelleg az F0-ból hiányzik; az „engedély megszerezhető” állítás nem igazolt, a műemléki jelleg érinti | HIGH | S001 I.2, S002 I.2; S009, S010, S011 |
| G-04 | S004 vs. S002 | Risk / Financial | A garázs külön önálló ingatlan, tulajdoni lapján teherbejegyzésekkel; a „zárt udvari parkoló” kapcsolata ismeretlen | HIGH | S002 I.1, III. (ellenőrzés V09–V13) |
| G-05 | S004 | Technical | A szobaszám (3), a helyrajzi szám és az eszmei hányad az F0-ban nem szerepel | MEDIUM | S001 I.1 (V03) |
| G-06 | S004 | Regulatory | A társasházi alapító okirat nem áll rendelkezésre: a padlástér hasznosítási jogosultsága és a lépcsőház kizárólagossága nem igazolható | MEDIUM | S001 I.3, I.4 |
| G-07 | S004 | Technical | Az A osztály, a gázkazán, a nyílászárók, a tájolás, az erkély hiánya és a közös költség dokumentummal nem igazolt | MEDIUM | — |
| G-08 | S004 vs. külső | Strategic | Zöld kapu: időzítés (2023–2024, nem 2023), helye (Steinmetz kapitány tér, kb. 660 m), kerékpárút helyett kerékpártároló | HIGH | S005, S006, S012 |
| G-09 | S004 vs. külső | Strategic | A „4000+ külföldi hallgató” elavult (5553, 2025. nov.) | LOW | S007, S008 |
| G-10 | S004 vs. külső | Operational | A 143 m-es megállótávolság nem reprodukálható (kb. 221 m légvonalban) | MEDIUM | S012 |
| G-11 | korábbi leszállítandók | Compliance (folyamat) | Az első változat forrás nélküli állításokat tartalmazott (kihasználtsági arányok, piaci ritkaság, „gyalogos elérés” stb.) | HIGH | Validated-Claims C. tábla; Process-History E-01 |
| G-12 | S001, S002 | Operational | A rendelkezésre álló tulajdoni lapok szemle-másolatok, kinyomtatva nem hitelesek; tranzakcióhoz hiteles másolat javasolt | LOW | S001, S002 (ellenőrzés V18–V20) |

## 4. Állítások a P03-hoz

Az F0 32 részállítása átment a validáláson; az eredmény: `Validated-Claims.md`.
A gap-lista G-02, G-03, G-08, G-09, G-10 tételei ebből a validálásból származnak.

## 5. Kapu-állapot

G2 (hiánylista megerősítése): **nincs felhasználói jóváhagyás** — lásd `Process-History.md`, Gate-napló.
