# BuildScripts — a csomag ellenőrző és leltározó szkriptjei

Reprodukálhatóság (módszertan P10): minden mért szám és minden ellenőrzés újrafuttatható.
Futtatási környezet: Python 3.10+, `pip install -r requirements.txt` (pypdf). Hálózat csak az `osm_proximity_check.py`-hoz kell.

## Előkészítés

Másold a három forrás-PDF-et a `../../Sources/` mappába, az eredeti fájlnéven (a nevek és a SHA-256 értékek a
`Sources/README.md`-ben vannak). A PDF-ek személyes adatokat tartalmaznak, ezért a `.gitignore` kizárja őket a repóból.

## Futtatási sorrend

| # | Szkript | Mit csinál | Várt kimenet |
|---|---|---|---|
| 1 | `verify_sources.py` | fájlazonosság (SHA-256) és az ingatlanra vonatkozó tények visszaellenőrzése a PDF-ekből | `23/23 PASS`, kilépési kód 0 |
| 2 | `extract_inventory.py` | forrásleltár-számok (oldal, szó, sor, kép, kulcstémák, átfedés) | a `Source-Inventory.md` 1. és 4. szakaszának számai |
| 3 | `osm_proximity_check.py` | a megállótávolság és a Zöld kapu-terület távolsága nyílt térképadatból (élő lekérdezés) | a legközelebbi megálló ≈ 221 m, a terület ≈ 661 m légvonalban (időfüggő) |
| 4 | `plan_vs_content.py [--write]` | terv-tartalom lefedettség, VCT-, forráskód-, adatvédelmi, aritmetikai és HTML-lint | `Lefedettség: 100%`, minden lint PASS, kilépési kód 0; `--write` frissíti a `Plan-vs-Content.md`-t |
| 5 | `build_manifest.py [--write]` | a fájlleltár mérete, szószáma, állapota | `Manifest.md` |

## Megjegyzések

- **Adatvédelem:** a tulajdonviszonyokra, terhekre és értékekre vonatkozó elemzés és a hozzá tartozó ellenőrző szkript szándékosan nem része a nyilvános repónak.
- **Élő szolgáltatások:** az `osm_proximity_check.py` a Nominatim és az Overpass nyilvános szolgáltatást hívja egyszeri, kis terhelésű lekérdezéssel; az eredmény az OSM-adat frissülésével változhat. Forrásmegjelölés: © OpenStreetMap contributors (ODbL 1.0).
- **Mutációs teszt:** a `plan_vs_content.py` érzékenységét a megrongított másolaton ellenőriztük (PARTIAL és DIVERGED tételek, adatvédelmi FAIL, kilépési kód 1); lásd `Process-History.md`.
