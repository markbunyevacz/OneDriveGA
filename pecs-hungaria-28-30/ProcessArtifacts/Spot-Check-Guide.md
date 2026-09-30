# Spot-Check-Guide — 12 ellenőrizhető tény az emberi átvizsgáláshoz

Cél: egy emberi ellenőr a források megnyitásával, percek alatt ellenőrizhesse a leszállítandók kulcsadatait.
Az „Ügynök újraellenőrzése” oszlop a futás során mért eredményt mutatja; a „Felülvizsgáló” oszlop üres, az ellenőr tölti ki.

**Küszöb:** ≥ 80% PASS elfogadható minőség (a módszertan 10 tételes skáláján ≥ 8/10; itt 12 tétel, tehát ≥ 10/12). Ha kevesebb, az összes leszállítandót újra kell ellenőrizni.

| # | Dokumentum | Szakasz | Állítás / tény | Ellenőrzési módszer | Várt eredmény | Ügynök újraellenőrzése | Ügynök | Felülvizsgáló |
|---|---|---|---|---|---|---|---|---|
| 1 | S001 (TL-A3) | fejléc | Helyrajzi szám és cím | TL-A3 első oldal fejléce | „Pécs, Belterület, 4464/A/3”; „HUNGÁRIA UTCA 28-30. A. ÉP. 1 EM. 1. AJTÓ” | `verify_sources.py` V01, V02: megtalálva | PASS | ☐ |
| 2 | S001 | I.1 | Lakás: 114 m², 3 szoba, 0 félszoba, eszmei hányad | TL-A3 I. rész 1. pont táblázata | „lakás 114 3 0 11414/77157” | V03: megtalálva | PASS | ☐ |
| 3 | S001 | I.2 | Jogi jelleg: Műemlék | TL-A3 I. rész 2. pont | „Jogi jelleg: Műemlék” | V04: megtalálva | PASS | ☐ |
| 4 | S001 | I.4 | 10,44 m² lépcsőház és 95 m² padlástér | TL-A3 I. rész 4. pont, önálló szöveges bejegyzés | „10.44 nm lépcsőházzal, 95 nm padlástérrel” | V06, V07: megtalálva | PASS | ☐ |
| 5 | S001 | III. | A lakás különlapján nincs teherbejegyzés | TL-A3 III. rész | „NEM TARTALMAZ BEJEGYZÉST” | V08: megtalálva | PASS | ☐ |
| 6 | S002 (TL-A14) | I.1 | Garázs: 13 m², eszmei hányad 1276/77157; hrsz. 4464/A/14; B. ép. 14. ajtó | TL-A14 első oldal | „garázs 13 0 0 1276/77157”; „4464/A/14”; „B. ÉP. 14. AJTÓ” | V09–V11: megtalálva | PASS | ☐ |
| 7 | S003 (KO) | I. pont | A közjegyzői okirat is 114 m²-t (lakás) és 13 m²-t (garázs) említ | az okirat rendelkező része | „114 m² területű, lakás megnevezésű”; „13 m² területű, garázs megnevezésű” | V14, V15: megtalálva (a PDF-ben a „m²” szétválik: „m 2”) | PASS | ☐ |
| 8 | S009 | adatlap | Hungária u. 28.: törzsszám 22, „Műemléki védelem”, „kora eklektikus, 19. sz. második fele” | https://muemlekem.hu/muemlek/show/1695 megnyitása | törzsszám: 22; védettség: Műemléki védelem; leírás: kora eklektikus, 19. sz. második fele | a futás közben megnyitva, az értékek egyeznek | PASS | ☐ |
| 9 | S005 | szöveg | Zöld kapu: projektzáró 2024.03.28.; 13 kerékpártároló; 2 elektromos autótöltő (4 gépjármű); kerékpárút nincs említve | a cikk megnyitása (S005) és keresés a „kerékpár” szóra | „2024. március 28”; „13 kerékpártárolót”; „2 elektromos autótöltőt … 4 gépjármű”; kerékpárút szó nincs | a futás közben megnyitva, az értékek egyeznek | PASS | ☐ |
| 10 | S007, S008 | szöveg | PTE külföldi hallgatók: 5553 (2025.11.21.), „több mint 5600”, 146 ország | a két oldal megnyitása | „ma 5553-nál tartunk”; „több mint 5600 külföldi diák”; „146 ország” | a futás közben megnyitva, az értékek egyeznek | PASS | ☐ |
| 11 | S012 | `osm_proximity_check.py` | Legközelebbi feltérképezett megálló és a Zöld kapu-terület távolsága | a szkript újrafuttatása (hálózat kell) | megálló ≈ 221 m; terület ≈ 661 m légvonalban (időfüggő, ±) | 221 m és 661 m (2026-09-30 21:47 UTC) | PASS | ☐ |
| 12 | számított | `plan_vs_content.py` | 114 + 95 = 209; (95 − 100) / 100 = −5,0% | a szkript aritmetika-sora, vagy kézi számolás | minden sor OK | minden sor OK | PASS | ☐ |

**Ügynök-önellenőrzés:** 12/12 PASS. Az önellenőrzés nem helyettesíti az emberi felülvizsgálatot; a 8–10. és a 11. tétel külső, időfüggő forrásra épül.
