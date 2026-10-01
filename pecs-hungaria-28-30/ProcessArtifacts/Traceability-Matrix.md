# Traceability-Matrix — minden leszállítandó és tény eredete

## 1. Leszállítandók

| Deliverable | Triggered By | Source Docs | External Sources | Verified By | Status |
|---|---|---|---|---|---|
| `Deliverables/adatlap.md` | 1. kör: az ingatlan-adatlap megadása; 2. kör: a három forrásdokumentum feltöltése (G-01–G-12) | S001, S002, S003, S004 | S005–S012 | P06: `Plan-vs-Content.md` (lefedettség a fájl szerinti táblázatban), `verify_sources.py` 23/23 PASS | DRAFT — P06 szerint teljes; felhasználói jóváhagyásra vár |
| `Deliverables/index.html` | ugyanaz | S001, S002, S004 | S005–S012 | P06 + HTML-szerkezet lint PASS | DRAFT — felhasználói jóváhagyásra vár |
| `Deliverables/befektetesi-elemzes.md` | ugyanaz | S001, S002, S004 | S005–S012 | P06 | DRAFT — felhasználói jóváhagyásra vár |
| `Deliverables/ugynoki-ertekesitesi-tajekoztato.md` | 2026.10.01., értékesítési felkészítő kérés; ugyanaznap a 13 kérdésre tulajdonosi válasz | S001, S004, S007, S008, S009, S012, S014–S016 | S014, S015, S016 | a válaszok megadottak; a tanúsítvány száma és a járat neve nyitott; piaci számok a megnyitott oldalakról | DRAFT |

A részletes tétel-szintű lefedettség (33 terv-tétel és 15 tiltott állítás hiánya) a `Plan-vs-Content.md`-ben van.

## 2. Tények és állítások nyomon követése

Jelölés: szakaszok az `adatlap.md` (AD), az `index.html` (HT) és a `befektetesi-elemzes.md` (EL) szerint. A részállítások azonosítói a `Validated-Claims.md`-ből valók.

| Állítás / tény | AD | HT | EL | Forrás (helyrögzítés) |
|---|---|---|---|---|
| C01 cím, helyrajzi szám | §1 | fejléc, 01 | — | S001 fejléc; S009, S010 (hrsz. 4464) |
| C03a–e Zöld kapu | §2 | 01 | §1 (utalás), §2 | S005, S006; távolság: S012 |
| C04a megállótávolság | §2, §8 | 01, 06 | §1, §8 | S012 (`osm_proximity_check.py`) |
| C05a kor; műemléki jelleg | §1, §2 | 01, 02 | §1 | S001 I.2; S009, S010 |
| C07b PTE-létszám | §2, §7 | 01, 06 | §1, §3 | S007, S008 |
| C10 alapterület 114 m² | §1, §3 | fejléc, statisztika, 02 | §1 | S001 I.1; S003 (hivatkozás) |
| új: 3 szoba, eszmei hányad | §1 | fejléc (szobaszám) | §1 (szobaszám) | S001 I.1 |
| C11a padlástér 95 m² | fejléc, §1, §3, §6 | fejléc, statisztika, 02, 05 | §1, §3, §5 | S001 I.4 |
| C12 potenciál ~209 m² | fejléc, §3 | fejléc, statisztika, 02 | §1, §3, §5 | S001 I.4 (számított: 114 + 95) |
| C21a lépcsőház 10,44 m² | §1, §5 | 02 | §1 | S001 I.4 |
| C19 parkoló és garázs | §5, §8 | 04, 06 | §1, §7, §8 | S002 I.1; S004 |
| C22 közös pince, 80 m² | §5 | 04 | — | tulajdonosi közlés, 2026.10.01.; közös, a 209 m²-ben nincs benne |
| C23 gyalogidő, lift, homlokzat, eladás köre | §2, §8 | 04, 06 | §1, §7, §8 | tulajdonosi közlés, 2026.10.01. |
| új: lakás különlapján nincs teherbejegyzés | §1, §7 | 06 | §1 | S001 III. |
| C11c engedély / műemléki hatás | §6, §8 | 05, 06 | §1, §5 (S3), §7, §9 | S001 I.2; S011 |
| MEGADOTT adatok: C02, C05b, C06, C13–C18, C20, C21b | §2–§5 | 01–04 | §1, §4 | S004 (nem igazolt) |
| Képletek és forgatókönyvek (CAPEX, hozam, ROI) | — | — | §3, §5, §6 | elemzői módszer; nem forrásolt tény, bemenetei piaci adatból pótolandók |

## 3. Nem a repóban szereplő, de a munkát megalapozó anyag

A forrásdokumentumokból származó, személyes vagy pénzügyi adatot tartalmazó elemzés (tulajdonviszonyok, terhek, értékek, teendők) és
az ahhoz tartozó ellenőrző szkript az ügynök privát tárában van, nem a nyilvános repóban (lásd `Process-History.md`, D-05, D-07).
A nyilvános anyagok ezekre csak azzal az általános megállapítással utalnak, hogy a tulajdonjogi helyzet és a terhek jogi ellenőrzése szükséges.
