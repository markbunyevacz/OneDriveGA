#!/usr/bin/env python3
"""P03/P10 - a nyilvános anyagokban szereplő, ingatlanra vonatkozó tények
gépi visszaellenőrzése a forrás-PDF-ekből (Sources/), valamint a fájlazonosság
(SHA-256) ellenőrzése.

Személyes adatot nem tartalmaz és nem ír ki: csak az ingatlan jellemzőit
(helyrajzi szám, terület, szobaszám, jogi jelleg, szöveges bejegyzések) ellenőrzi.
A tulajdonviszonyokra és terhekre vonatkozó ellenőrzések a privát szkriptben vannak.

Használat:  python3 verify_sources.py [--sources ../../Sources]
Kilépési kód: 0 = minden ellenőrzés PASS, 1 = legalább egy FAIL.
"""
import argparse
import hashlib
import re
import sys
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    sys.exit("pypdf hiányzik: pip install -r requirements.txt")

FILES = {
    "TL-A3": ("S001", "EING-20260930-232416051_6cd2.pdf",
              "d4e14cc45ba91a56a8f0ffc7a62d717d15405cbbc5a8229477c8743befa6c536"),
    "TL-A14": ("S002", "EING-20260930-232247732_d174.pdf",
               "d7af2eb3ab395ca88fa952193a90a16e6e056da6ac33c1d6d42878c85b106996"),
    "KO": ("S003", "41016_N_138_2026_13-41016_N_138_2026_13_ee97.pdf",
           "01dbc7a4e41e389749403a163e68610f1b270121e771f71b8266f47ab41daf94"),
}

# (ellenőrzés-azonosító, dokumentum, leírás, reguláris kifejezés, minimális előfordulás)
CHECKS = [
    ("V01", "TL-A3", "helyrajzi szám: Pécs 4464/A/3", r"4464/A/3", 1),
    ("V02", "TL-A3", "cím: A. ép., 1. em., 1. ajtó", r"HUNGÁRIA UTCA 28-30\. A\. ÉP\. 1 EM\. 1\. AJTÓ", 1),
    ("V03", "TL-A3", "lakás, 114 m2, 3 szoba, 0 félszoba, eszmei hányad 11414/77157",
     r"lakás 114 3 0 11414/77157", 1),
    ("V04", "TL-A3", "jogi jelleg: Műemlék", r"Jogi jelleg: Műemlék", 1),
    ("V05", "TL-A3", "jogi jelleg: Társasház", r"Jogi jelleg: Társasház", 1),
    ("V06", "TL-A3", "önálló szöveges bejegyzés: 10.44 nm lépcsőház", r"10\.44 nm lépcsőházzal", 1),
    ("V07", "TL-A3", "önálló szöveges bejegyzés: 95 nm padlástér", r"95 nm padlástér", 1),
    ("V08", "TL-A3", "III. rész: nem tartalmaz bejegyzést", r"III\. RÉSZ\s+NEM TARTALMAZ BEJEGYZÉST", 1),
    ("V09", "TL-A14", "helyrajzi szám: Pécs 4464/A/14", r"4464/A/14", 1),
    ("V10", "TL-A14", "cím: B. ép. 14. ajtó", r"HUNGÁRIA UTCA 28-30\. B\. ÉP\. 14\. AJTÓ", 1),
    ("V11", "TL-A14", "garázs, 13 m2, eszmei hányad 1276/77157", r"garázs 13 0 0 1276/77157", 1),
    ("V12", "TL-A14", "jogi jelleg: Műemlék", r"Jogi jelleg: Műemlék", 1),
    ("V13", "TL-A14", "III. rész: teherbejegyzés(ek) szerepelnek (típus: jelzálogjog)", r"Jelzálogjog", 1),
    ("V14", "KO", "hivatkozás: 114 m2 területű, lakás megnevezésű ingatlan", r"114 m ?2 területű, lakás megnevezésű", 1),
    ("V15", "KO", "hivatkozás: 13 m2 területű, garázs megnevezésű ingatlan", r"13 m ?2 területű, garázs megnevezésű", 1),
    ("V16", "TL-A3", "kiállítás dátuma: 2026.09.30", r"2026\.09\.30", 1),
    ("V17", "TL-A14", "kiállítás dátuma: 2026.09.30", r"2026\.09\.30", 1),
    ("V18", "TL-A3", "másolat típusa: szemle", r"Tulajdonilap-másolat\s*\(szemle\)", 1),
    ("V19", "TL-A14", "másolat típusa: szemle", r"Tulajdonilap-másolat\s*\(szemle\)", 1),
    ("V20", "TL-A3", "kinyomtatva nem hiteles bizonyító erejű", r"nem\s+minősül hiteles bizonyító erejű dokumentumnak", 1),
]


def normalised_text(path: Path) -> str:
    reader = PdfReader(str(path))
    text = "\n".join((p.extract_text() or "") for p in reader.pages)
    return re.sub(r"\s+", " ", text)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", default=str(Path(__file__).resolve().parents[2] / "Sources"))
    src_dir = Path(ap.parse_args().sources)

    texts, failures = {}, 0
    print("## Fájlazonosság (SHA-256)\n")
    print("| Kód | Fájl | Eredmény |")
    print("|---|---|---|")
    for code, (sid, name, digest) in FILES.items():
        path = src_dir / name
        if not path.exists():
            print(f"| {code} | {name} | FAIL (hiányzik) |")
            failures += 1
            continue
        ok = hashlib.sha256(path.read_bytes()).hexdigest() == digest
        failures += not ok
        print(f"| {code} ({sid}) | {name} | {'PASS' if ok else 'FAIL (eltérő hash)'} |")
        texts[code] = normalised_text(path)

    print("\n## Tartalmi ellenőrzések\n")
    print("| ID | Dok. | Ellenőrzött tény | Találat | Eredmény |")
    print("|---|---|---|---|---|")
    for cid, code, desc, pattern, minimum in CHECKS:
        found = len(re.findall(pattern, texts.get(code, "")))
        ok = found >= minimum
        failures += not ok
        print(f"| {cid} | {code} | {desc} | {found} | {'PASS' if ok else 'FAIL'} |")

    total = len(CHECKS) + len(FILES)
    print(f"\nÖsszesen: {total - failures}/{total} PASS")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
