#!/usr/bin/env python3
"""P01 - forrásinventár a Sources/ mappában lévő PDF-ekből (Markdown a stdout-ra).

Személyes adatot nem ír ki. A "kulcstémák" csak olyan szavakból állnak, amelyek
legalább egyszer kisbetűvel is előfordulnak, így a tulajdonnevek kiszűrődnek.
A strukturális számok (bekezdés, táblázat, cím) PDF-ből heurisztikák: a formátum
nem hordoz szemantikus szerkezetet.

Használat:  python3 extract_inventory.py [--sources ../../Sources]
"""
import argparse
import hashlib
import re
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    sys.exit("pypdf hiányzik: pip install -r requirements.txt")

SOURCES = {
    "EING-20260930-232416051_6cd2.pdf": ("S001", "TL-A3"),
    "EING-20260930-232247732_d174.pdf": ("S002", "TL-A14"),
    "41016_N_138_2026_13-41016_N_138_2026_13_ee97.pdf": ("S003", "KO"),
}

HU_STOP = {
    "a", "az", "és", "hogy", "nem", "egy", "is", "meg", "van", "volt", "szerint",
    "alapján", "által", "részére", "napján", "között", "vagy", "mint", "még",
    "már", "csak", "kell", "ebben", "abban", "esetén", "alatt", "után", "előtt",
    "szám", "számú", "alatti", "nyilvántartott", "folytatás", "következő",
    "előző", "oldalon", "oldalról", "oldal", "bejegyző", "határozat", "érkezési",
}
EN_STOP = {"the", "and", "of", "to", "in", "is", "for", "that", "with", "this"}
WORD = re.compile(r"[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű]+")
HEADING_PATTERNS = [
    r"^(I|II|III)\. ?RÉSZ$",
    r"^(I|II|III)\.$",
    r"^TULAJDONI LAP VÉGE$",
    r"^H A G Y A T É K Á T A D Ó V É G Z É S T:?$",
    r"^I n d o k o l á s$",
]


def count_images(page) -> int:
    """Oldalszintű kép-XObjectek száma (dekódolás és Pillow nélkül)."""
    resources = page.get("/Resources")
    xobjects = resources.get_object().get("/XObject") if resources else None
    if not xobjects:
        return 0
    xobjects = xobjects.get_object()
    return sum(1 for k in xobjects if xobjects[k].get_object().get("/Subtype") == "/Image")


def extract(path: Path):
    reader = PdfReader(str(path))
    pages = [p.extract_text() or "" for p in reader.pages]
    images = sum(count_images(p) for p in reader.pages)
    return reader, "\n".join(pages), images


def topics(text: str, top: int):
    raw = WORD.findall(text)
    lowercase_seen = {t for t in raw if t == t.lower() and len(t) >= 4}
    counter = Counter(
        t.lower() for t in raw
        if t.lower() in lowercase_seen and t.lower() not in HU_STOP
    )
    return counter.most_common(top)


def language(text: str):
    toks = [t.lower() for t in WORD.findall(text)]
    hu = sum(t in HU_STOP for t in toks)
    en = sum(t in EN_STOP for t in toks)
    return ("hu", hu / (hu + en)) if hu + en else ("?", 0.0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", default=str(Path(__file__).resolve().parents[2] / "Sources"))
    args = ap.parse_args()
    src_dir = Path(args.sources)

    rows, tops = [], {}
    for name, (sid, code) in SOURCES.items():
        path = src_dir / name
        if not path.exists():
            sys.exit(f"Hiányzó forrásfájl: {path}")
        reader, text, images = extract(path)
        lines = [ln.strip() for ln in text.splitlines()]
        nonempty_lines = sum(1 for ln in lines if ln)
        blocks = [b for b in re.split(r"\n\s*\n", text) if b.strip()]
        headings = sum(
            any(re.match(p, ln) for p in HEADING_PATTERNS) for ln in lines
        )
        tables = len(re.findall(r"Rendeltetési mód\s+Terület", text))
        lang, conf = language(text)
        meta = reader.metadata or {}
        created = str(meta.get("/CreationDate", ""))[2:10] if meta else ""
        rows.append({
            "id": sid, "code": code, "file": name, "format": "PDF",
            "pages": len(reader.pages), "words": len(text.split()),
            "lines": nonempty_lines, "paragraphs": len(blocks), "tables": tables,
            "images": images,
            "headings": headings, "lang": lang, "conf": conf,
            "size_kb": round(path.stat().st_size / 1024, 1),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "created": created,
            "producer": re.sub(r"[^\x20-\x7E\u00AE].*$", "", str(meta.get("/Producer", ""))).strip() if meta else "",
        })
        tops[code] = topics(text, 40)

    print("## Forrásfájlok (automatikusan számolt)\n")
    print("| ID | Kód | Formátum | Nyelv (bizonyosság) | Oldal | Szó | Sor | Bekezdés* | Táblázat* | Kép | Cím* | KB | SHA-256 |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        print(f"| {r['id']} | {r['code']} | {r['format']} | {r['lang']} ({r['conf']:.0%}) | "
              f"{r['pages']} | {r['words']} | {r['lines']} | {r['paragraphs']} | {r['tables']} | {r['images']} | "
              f"{r['headings']} | {r['size_kb']} | `{r['sha256']}` |")
    print("\n*heurisztika (PDF-ben nincs szemantikus szerkezet); a megbízhatóan mérhető mutatók: oldal, szó, sor, kép.\n")

    print("## PDF-metaadat (csak technikai mezők)\n")
    for r in rows:
        print(f"- {r['code']}: létrehozás dátuma (PDF): {r['created'] or 'n/a'}; előállító szoftver: {r['producer'] or 'n/a'}")

    print("\n## Kulcstémák (top 5, kisbetűs szavak gyakoriság szerint)\n")
    for r in rows:
        print(f"- {r['code']}: " + ", ".join(f"{w} ({n})" for w, n in tops[r['code']][:5]))

    print("\n## Átfedési mátrix (top-40 kulcsszó Jaccard-hasonlósága)\n")
    print("| Pár | Közös témák (top 8) | Átfedés % | Elsődleges tulajdonos |")
    print("|---|---|---|---|")
    for a, b in combinations(tops, 2):
        da, db = dict(tops[a]), dict(tops[b])
        shared = set(da) & set(db)
        union = set(da) | set(db)
        pct = 100 * len(shared) / len(union) if union else 0
        ranked = sorted(shared, key=lambda w: min(da[w], db[w]), reverse=True)[:8]
        owner = a if sum(da[w] for w in shared) >= sum(db[w] for w in shared) else b
        print(f"| {a} / {b} | {', '.join(ranked)} | {pct:.0f}% | {owner} |")


if __name__ == "__main__":
    main()
