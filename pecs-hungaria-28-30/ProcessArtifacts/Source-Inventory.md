# Source-Inventory — P01 forrás-ingesztió

Mérés: `BuildScripts/extract_inventory.py` (PDF-ek) és egy egyszeri számlálás az F0 szövegére (2026-09-30).
A szám-jellegű mutatók közül a megbízhatóan mérhetők: oldal, szó, sor, kép. A bekezdés, táblázat és cím PDF-nél
heurisztika (a formátum nem hordoz szemantikus szerkezetet).

## 1. Forrásfájlok

| ID | Kód | Fájl / forma | Formátum | Nyelv | Oldal | Szó | Sor | Bekezdés* | Táblázat* | Kép | Cím* | KB |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S001 | TL-A3 | `EING-20260930-232416051_6cd2.pdf` | PDF | hu (100%) | 2 | 352 | 91 | 1 | 1 | 2 | 4 | 175,0 |
| S002 | TL-A14 | `EING-20260930-232247732_d174.pdf` | PDF | hu (100%) | 3 | 537 | 145 | 1 | 1 | 3 | 4 | 182,1 |
| S003 | KO | `41016_N_138_2026_13-41016_N_138_2026_13_ee97.pdf` | PDF | hu (100%) | 4 | 1164 | 129 | 14 | 0 | 1 | 4 | 305,8 |
| S004 | F0 | a megadott adatlap (chat-szöveg, Markdown) | szöveg | hu | – | 222 | – | 11 blokk | 0 | 0 | 6 (1 H1 + 5 H2) | – |

\*heurisztika. Az F0 25 felsorolási tételt tartalmaz. A képek a hivatalos címer/hitelesítési sáv (vizuális ellenőrzéssel megnézve: információtartalmat nem hordoznak). A nyelvfelismerés bizonyossága 100% (HU/EN stopszó-arány), így felhasználói megerősítés nem kellett.

SHA-256 értékek: `Sources/README.md`. A fájlazonosság gépi ellenőrzése: `BuildScripts/verify_sources.py` (3/3 PASS).

## 2. Metaadatok

| ID | Cím | Kelt | Kiállító / szerző | PDF-metaadat (technikai) |
|---|---|---|---|---|
| S001 | Tulajdonilap-másolat (szemle), Pécs 4464/A/3 | 2026.09.30. (elektronikusan hitelesítve ugyanazon a napon) | Baranya Vármegyei Kormányhivatal Földhivatali Főosztály Földhivatali Osztály 3. (Pécs) | létrehozás: 2026-09-30; előállító: OpenPDF 2.0.3 |
| S002 | Tulajdonilap-másolat (szemle), Pécs 4464/A/14 | 2026.09.30. | ugyanaz a hatóság | létrehozás: 2026-09-30; előállító: OpenPDF 2.0.3 |
| S003 | Közjegyzői okirat (Pécs) | 2026.09.22. | közjegyzői iroda (Pécs) | létrehozás dátuma: nincs; előállító: Microsoft Word 2016 |
| S004 | Pécs, Hungária utca 28-30. – Ingatlan Adatlap | 2026-09-30 (chat) | a megadó (szerző nem megnevezett) | – |

## 3. Kulcstémák (top 5, gyakoriság szerint)

| ID | Kulcstémák |
|---|---|
| S001 | másolat (5), hányad (5), neve (4), címe (4), tulajdonilap (3) — mezőcímkék, a szerkezetet tükrözik |
| S002 | címe (9), másolat (6), utca (6), neve (5), azaz (5) — mezőcímkék, a szerkezetet tükrözik |
| S003 | *nem részletezve*: a leggyakoribb szavak az ügy jellegét és személyes adatokat fednének fel (adatvédelmi döntés, lásd `Process-History.md` D-05) |
| S004 | utca (3), épület (3), emelet (3), közös (3), saját (3) — azonos módszerrel mérve; tematikusan: lokáció, paraméterek, műszaki, egyéb, tetőtér |

## 4. Átfedési mátrix

**Automatikus (lexikai) mérés** — a top-40 kulcsszó Jaccard-hasonlósága, csak a szerkezeti szavakat méri:

| Pár | Közös témák (top 8) | Átfedés % | Elsődleges tulajdonos |
|---|---|---|---|
| S001 / S002 | másolat, hányad, neve, címe, utca, szemle, tulajdonilap, jelleg | 54% | S002 |
| S001 / S003 | neve, utca | 3% | S003 |
| S002 / S003 | neve, utca | 3% | S002 |

**Kézi (szemantikus) elemzés** — ez a döntő az ellentmondás-keresésnél:

| Pár | Közös témák | Ellentmondás (db) | Átfedés | Elsődleges tulajdonos |
|---|---|---|---|---|
| S001 – S002 | ugyanaz az épületegyüttes és cím; műemléki és társasházi jelleg; azonos dokumentumtípus | 0 | magas | S001 (lakás), S002 (garázs) |
| S001 – S003 | a lakás: helyrajzi szám, 114 m² | 0 | közepes | S001 |
| S002 – S003 | a garázs: helyrajzi szám, 13 m² | 0 | közepes | S002 |
| S004 – S001 | cím, alapterület, emelet, lépcsőház, padlástér/tetőtér, jogi jelleg | **2** (padlástér 100 vs. 95 m²; származtatott potenciál 214 vs. 209 m²) | magas | S001 |
| S004 – S002 | parkolás | 0 (a kapcsolat ismeretlen) | alacsony | S002 |
| S004 – S003 | — | 0 | alacsony | — |

## 5. Metaadat-ellentmondások

- **Dátumok:** a tulajdoni lapok 2026.09.30-i állapotot mutatnak, az okirat 2026.09.22-i; időrendi ellentmondás nincs. A lapok a kiadást megelőző napig érvényes állapotot tükrözik, ezért a későbbi változások nem láthatók.
- **Verziók/szerzők:** nincs ütköző verzió vagy szerző.
- **Személyes adatok:** a két dokumentumtípus személyi (lakcím-jellegű) adatai eltérnek. Ez nem érinti az ingatlan adatait, ezért adatvédelmi okból nem részletezzük.
- **Dokumentumjelleg:** mindkét tulajdoni lap *szemle*-másolat (csak a fennálló bejegyzések); a dokumentum szerint kinyomtatva nem hiteles bizonyító erejű.

## 6. Kapu-állapot

G1 (forrásleltár megerősítése): **nincs felhasználói jóváhagyás** — a futás nem interaktív; lásd `Process-History.md`, Gate-napló.
