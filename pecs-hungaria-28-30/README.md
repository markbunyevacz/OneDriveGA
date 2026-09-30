# Pécs, Hungária utca 28–30., 1. emelet

Forrás-ellenőrzött ingatlan-adatlap csomag. **Állapot: TERVEZET** — a leszállítandók felhasználói jóváhagyásra várnak
(a módszertani kapuk nem interaktív futásban nem hagyhatók jóvá; lásd `ProcessArtifacts/Process-History.md`).

## Tartalom

| Mappa / fájl | Célja |
|---|---|
| [`Deliverables/index.html`](./Deliverables/index.html) | Reszponzív, egyoldalas, **nyomtatásbarát** adatlap státuszjelölésekkel; külső függőség nélkül megnyitható, böngészőből PDF-be menthető |
| [`Deliverables/adatlap.md`](./Deliverables/adatlap.md) | Strukturált adatlap: minden sor státusszal és forrással, forrásjegyzékkel |
| [`Deliverables/befektetesi-elemzes.md`](./Deliverables/befektetesi-elemzes.md) | Hasznosítási forgatókönyvek, CAPEX-szcenáriók, képletek, kockázatok, due diligence lépések |
| [`ProcessArtifacts/`](./ProcessArtifacts/) | Forrásleltár, hiánylista, validált állítások, forrásjegyzék, nyomon követés, terv–tartalom ellenőrzés, spot-check útmutató, folyamatnapló, fájlleltár és a reprodukáló szkriptek |
| [`Sources/`](./Sources/) | A forrásdokumentumok jegyzéke hash-ekkel; a PDF-ek **nem** kerülnek a repóba |

## Mit igazolnak a hivatalos dokumentumok?

| Adat | Érték | Forrás |
|---|---|---|
| Helyrajzi szám | Pécs, belterület 4464/A/3 | tulajdoni lap (2026.09.30.) |
| Alapterület, szobák | 114 m², 3 szoba | tulajdoni lap |
| Lépcsőház és padlástér | 10,44 m² lépcsőház, **95 m² padlástér** (a megadott 100 m² helyett) | tulajdoni lap |
| Potenciális terület | ~**209 m²** (a megadott ~214 m² helyett) | számított |
| Jogi jelleg | társasház; **műemlék** | tulajdoni lap; műemléki adatbázis |
| Terhek (lakás) | a különlapon nincs bejegyzés | tulajdoni lap |
| Garázs | külön önálló ingatlan (13 m², hrsz. 4464/A/14), tulajdoni lapján teherbejegyzésekkel | tulajdoni lap |

## Az ellenőrzés eredménye

A megadott adatlap 32 részállítását ellenőriztük (`ProcessArtifacts/Validated-Claims.md`):
**8 VERIFIED · 5 CORRECTED · 1 OUTDATED · 18 UNVERIFIABLE · 0 REFUTED.**

Fő korrekciók: a padlástér 95 m² (nem 100 m²); a Zöld kapu beruházás 2023–2024-ben valósult meg egy közösségi téren, amely az
épülettől kb. 660 m-re van, és kerékpártárolót (nem kerékpárutat) tartalmaz; a PTE külföldi hallgatóinak száma 5553 (nem 4000+); a megadott
143 m-es megállótávolság nem reprodukálható (legközelebbi feltérképezett megálló kb. 221 m). Az A energetikai osztály, a gázkazán, a
nyílászárók, a tájolás, a közös költség és a parkoló dokumentummal nem igazolt, ezért **MEGADOTT** jelölést kapott.

## Az első változathoz képest

Az első változat több forrás nélküli állítást tartalmazott (többek között kitalált kihasználtsági arányokat, piaci ritkasági és árprémium-állításokat,
„gyalogos elérést”, „termikus inerciát”); ezeket töröltük vagy hipotézisként jelöltük (`Validated-Claims.md` C. tábla, `Process-History.md` E-01).
Az eredetileg megadott értékek a korrigált értékek mellett láthatóan megmaradtak („megadott: …”).

## Adatvédelem

A repó nyilvános, a forrás-PDF-ek viszont személyes és pénzügyi adatokat tartalmaznak, ezért:

- a PDF-ek nem kerülnek a repóba (`.gitignore`), csak a hash-ük (`Sources/README.md`);
- a nyilvános anyagok csak az **ingatlan jellemzőit** idézik;
- a tulajdonviszonyokra, terhekre, értékekre és teendőkre vonatkozó részletes elemzés a repón kívül van;
- a csomag adatvédelmi lintje (`plan_vs_content.py`) azonosító-, számlaszám- és e-mail-mintákat, valamint érzékeny kifejezéseket keres.

**Hirdetés vagy értékesítés előtt a tulajdonjogi helyzet és a teherbejegyzések jogi ellenőrzése szükséges.** Ez az anyag nem jogi tanács.

## Használat

```bash
xdg-open Deliverables/index.html   # Linux
open Deliverables/index.html       # macOS
start Deliverables/index.html      # Windows
```

PDF-be mentéshez használd a böngésző **Print → Save as PDF** funkcióját — az oldal nyomtatásra optimalizált stílussal rendelkezik.

Az ellenőrzések újrafuttatása: `ProcessArtifacts/BuildScripts/README.md`.
