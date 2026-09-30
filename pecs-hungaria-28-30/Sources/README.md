# Sources — a forrásdokumentumok jegyzéke

**A forrás-PDF-ek nem kerülnek a repóba.** A repó nyilvános, a dokumentumok pedig személyes adatokat
tartalmaznak (nevek, születési és anyja-név adatok, lakcímek, azonosítók, számlaadatok, tartozások).
A `.gitignore` ennek a mappának a tartalmát kizárja (kivéve ezt a fájlt). A módszertan P10 lépése
(„eredeti fájlok másolása a Sources/ mappába”) ezért **csak helyi másolatként** valósul meg; a fájlok
azonosságát az alábbi SHA-256 értékek igazolják.

Helyi futtatáshoz másold a PDF-eket ide az eredeti fájlnéven, majd futtasd a
`ProcessArtifacts/BuildScripts/` szkriptjeit (lásd az ottani README-t).

| ID | Kód | Fájlnév | SHA-256 | Oldal | Típus |
|---|---|---|---|---|---|
| S001 | TL-A3 | `EING-20260930-232416051_6cd2.pdf` | `d4e14cc45ba91a56a8f0ffc7a62d717d15405cbbc5a8229477c8743befa6c536` | 2 | Tulajdonilap-másolat (szemle), Pécs 4464/A/3 (lakás), 2026.09.30. |
| S002 | TL-A14 | `EING-20260930-232247732_d174.pdf` | `d7af2eb3ab395ca88fa952193a90a16e6e056da6ac33c1d6d42878c85b106996` | 3 | Tulajdonilap-másolat (szemle), Pécs 4464/A/14 (garázs), 2026.09.30. |
| S003 | HV | `41016_N_138_2026_13-41016_N_138_2026_13_ee97.pdf` | `01dbc7a4e41e389749403a163e68610f1b270121e771f71b8266f47ab41daf94` | 4 | Közjegyzői hagyatékátadó végzés (Pécs), 2026.09.22. |
| S004 | F0 | *(nincs fájl)* | – | – | A megadott ingatlan-adatlap szövege (chat); alapváltozat: git `9fe05c5`, `adatlap.md` |

A dokumentumok tartalmát a nyilvános anyagok csak az **ingatlan jellemzőire** vonatkozóan idézik
(helyrajzi szám, terület, szobaszám, jogi jelleg, szöveges bejegyzések). A tulajdonviszonyokra,
hagyatéki adatokra, terhekre és értékekre vonatkozó részletek szándékosan nincsenek a repóban.
