#!/usr/bin/env python3
"""P06/P07 - terv-tartalom ellenőrzés (plan-vs-content) mért lefedettséggel,
valamint adatvédelmi, forráshivatkozási, aritmetikai és HTML-szerkezeti lint.

A "terv": minden validált állításnak (Validated-Claims.md) és minden új hivatalos
ténynek szerepelnie kell a leszállítandókban, a megadott státusszal. Az állapot
tétel-szinten FULL (minden előírt fájlban megvan), PARTIAL, MISSING vagy DIVERGED
(tiltott, forrás nélküli állítás megjelent). Lefedettség = FULL / ÖSSZES * 100.

A reguláris kifejezések jelenlétet mérnek; a tartalmi helyességet a verify_sources.py
és a kézi átolvasás egészíti ki.

Használat:  python3 plan_vs_content.py [--write]
  --write   a ProcessArtifacts/Plan-vs-Content.md frissítése
Kilépési kód: 0 = 100% lefedettség és minden lint PASS, 1 = egyébként.
"""
import argparse
import re
import subprocess
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "ProcessArtifacts"
FILES = {
    "md": ROOT / "Deliverables" / "adatlap.md",
    "html": ROOT / "Deliverables" / "index.html",
    "an": ROOT / "Deliverables" / "befektetesi-elemzes.md",
}
LABEL = {"md": "adatlap.md", "html": "index.html", "an": "befektetesi-elemzes.md"}

PLAN = [
    ("P01", "Cím, hrsz., A. épület / 1. em. / 1. ajtó", "C01",
     {"md": [r"4464/A/3", r"A\. épület, 1\. emelet 1\. ajtó"], "html": [r"A\. ép\. 1\. em\. 1\."]}),
    ("P02", "Városrész (megadott)", "C02",
     {"md": [r"Belváros-közeli prémium lokáció"], "html": [r"Belváros-közeli"], "an": [r"Belváros-közeli lokáció"]}),
    ("P03", "Zöld kapu: hely és dátumok", "C03a-c",
     {"md": [r"Steinmetz kapitány tér", r"2023\.09\.27", r"2024\.03\.28"],
      "html": [r"Steinmetz", r"2023\.09\.27", r"2024\.03\.28"], "an": [r"Zöld kapu"]}),
    ("P04", "Zöld kapu elemei; kerékpárút helyett kerékpártároló", "C03d-e",
     {"md": [r"13 kerékpártároló", r"kerékpárutat nem említenek"],
      "html": [r"13 kerékpártároló", r"Kerékpárutat a források nem említenek"]}),
    ("P05", "Távolság a beruházástól (~660 m)", "C03c",
     {"md": [r"660 m"], "html": [r"660 m"], "an": [r"660 m"]}),
    ("P06", "Tömegközlekedés: 143 m (megadott) vs. ~221 m (OSM)", "C04a",
     {"md": [r"143 méterre", r"221 m"], "html": [r"143 m", r"221 m"], "an": [r"221 m"]}),
    ("P07", "Közvetlen PTE-összeköttetés (megadott)", "C04b",
     {"md": [r"PTE-összeköttetés"], "html": [r"PTE elérés"]}),
    ("P08", "Épület kora és építőanyaga", "C05a-b",
     {"md": [r"19\. sz\. második fele", r"téglaszerkezet"], "html": [r"19\. sz\. második fele", r"téglaszerkezet"],
      "an": [r"19\. sz\.-i"]}),
    ("P09", "Műemléki jogi jelleg", "új",
     {"md": [r"Műemlék"], "html": [r"Műemlék"], "an": [r"Műemléki jogi jelleg"]}),
    ("P10", "Épület állapota (megadott)", "C06",
     {"md": [r"Utcafront felújításra szorul"], "html": [r"utcafront felújításra szorul"], "an": [r"utcafront-homlokzat"]}),
    ("P11", "PTE: 5553 külföldi hallgató; a 4000+ elavult", "C07a-c",
     {"md": [r"5553", r"4000\+"], "html": [r"5553", r"4000\+"], "an": [r"5553"]}),
    ("P12", "Társasházi lakás, 1. emelet, 114 m²", "C08-C10",
     {"md": [r"114 m²"], "html": [r"114 m²"], "an": [r"114 m²"]}),
    ("P13", "Szobák száma: 3", "új",
     {"md": [r"3 / 0", r"3 szoba"], "html": [r"3 szoba"], "an": [r"3 szoba"]}),
    ("P14", "Eszmei hányad 11414/77157", "új", {"md": [r"11414/77157"]}),
    ("P15", "Padlástér: 95 m² (megadott: 100 m²)", "C11a",
     {"md": [r"95 m²", r"100 m²"], "html": [r"95 m²", r"100 m²"], "an": [r"95 m²", r"100 m²"]}),
    ("P16", "Potenciál: ~209 m² (megadott: ~214 m²)", "C12",
     {"md": [r"~209 m²", r"~214 m²"], "html": [r"~209 m²", r"~214 m²"], "an": [r"~209 m²"]}),
    ("P17", "Tájolás (megadott)", "C13",
     {"md": [r"Déli, napsütéses"], "html": [r"Déli, napsütéses"], "an": [r"Déli tájolás"]}),
    ("P18", "Erkély / terasz: nincs (megadott)", "C14",
     {"md": [r"Erkély / terasz\*\* \| Nincs"], "html": [r"Erkély / terasz</dt><dd>Nincs"]}),
    ("P19", "Saját gázkazán (megadott)", "C15",
     {"md": [r"Saját gázkazán"], "html": [r"Saját gázkazán"], "an": [r"gázkazán"]}),
    ("P20", "Nyílászárók (megadott)", "C16",
     {"md": [r"Modern, jó állapotú"], "html": [r"Modern, jó állapotú"], "an": [r"Nyílászárók: csere nem szükséges"]}),
    ("P21", "A osztály — ellenőrizendő", "C17",
     {"md": [r"A osztály \| \*\*MEGADOTT\*\* — \*\*ELLENŐRIZENDŐ\*\*"], "html": [r"A osztály — ellenőrizendő"],
      "an": [r"A energetikai osztály"]}),
    ("P22", "2006-os felújítás (megadott)", "C18",
     {"md": [r"2006-ban felújított"], "html": [r"2006-ban felújított"], "an": [r"2006"]}),
    ("P23", "Parkoló és a nyilvántartott garázs (4464/A/14)", "C19",
     {"md": [r"Zárt belső udvari parkoló", r"4464/A/14"], "html": [r"Zárt belső udvari parkoló", r"4464/A/14"],
      "an": [r"4464/A/14"]}),
    ("P24", "Közös költség (megadott)", "C20",
     {"md": [r"~20 000 Ft/hó"], "html": [r"20 000 Ft/hó"], "an": [r"20 000 Ft/hó"]}),
    ("P25", "Lépcsőház: 10,44 m² tartozék; kizárólagosság megadott", "C21a-b",
     {"md": [r"10,44 m²", r"kizárólagosság"], "html": [r"10,44 m²", r"kizárólagosság"], "an": [r"10,44 m²"]}),
    ("P26", "Tetőtér: engedély és beépíthetőség ellenőrizendő", "C11b-c",
     {"md": [r"fal/tető határáig", r"\[NEEDS VERIFICATION\]"], "html": [r"fal/tető határáig", r"ellenőrizendő"],
      "an": [r"\[NEEDS VERIFICATION\]"]}),
    ("P27", "Hasznosítási ötletek (F0)", "F0",
     {"md": [r"galériás kialakítás"], "html": [r"Galériás kialakítás"]}),
    ("P28", "A lakás különlapján nincs teherbejegyzés", "új",
     {"md": [r"nincs bejegyzés"], "html": [r"nincs teherbejegyzés"], "an": [r"nincs teherbejegyzés"]}),
    ("P29", "Szemle-másolat, hiteles másolat javasolt", "új",
     {"md": [r"szemle-másolat", r"hiteles"], "html": [r"hiteles tulajdoni lap"]}),
    ("P30", "Státusz-jelmagyarázat", "módszertan",
     {"md": [r"\*\*IGAZOLT\*\*", r"\*\*KORRIGÁLT\*\*", r"\*\*MEGADOTT\*\*", r"\*\*ELLENŐRIZENDŐ\*\*"],
      "html": [r'class="legend"', r"korrigált", r"megadott", r"ellenőrizendő", r"hivatalos"],
      "an": [r"\*\*IGAZOLT\*\*", r"\*\*HIPOTÉZIS\*\*"]}),
    ("P31", "Forráskódok és forrásjegyzék", "módszertan",
     {"md": [r"\| S012 \|"], "html": [r"S012"], "an": [r"S011"]}),
    ("P32", "Jogi ellenőrzés az értékesítés előtt", "G-01",
     {"md": [r"jogi ellenőrzése szükséges"], "html": [r"jogi ellenőrzése szükséges"], "an": [r"Jogi ellenőrzés"]}),
    ("P33", "TERVEZET-jelölés", "módszertan",
     {"md": [r"TERVEZET"], "html": [r"TERVEZET"], "an": [r"TERVEZET"]}),
]

FORBIDDEN = [
    ("X01", r"termikus inercia", "A01 - forrás nélküli"),
    ("X02", r"gyalogos elérés", "A02 - kitalált"),
    ("X03", r"magas belmagasságú", "A03 - forrás nélküli"),
    ("X04", r"95 ?%\+|70[–-]85 ?%", "A04 - kitalált kihasználtsági arány"),
    ("X05", r"strukturálisan kínálathiányos", "A06 - forrás nélküli piaci állítás"),
    ("X06", r"★", "A07 - forrás nélküli súlyozás"),
    ("X07", r"Airbnb", "A05 - forrás nélküli"),
    ("X08", r"ritka adottság|rendkívül ritka", "A12 - vélemény"),
    ("X09", r"szegmens-felár", "A06 - forrás nélküli"),
    ("X10", r"jobb megtartja", "A06 - forrás nélküli"),
    ("X11", r"kiváló akusztika|kiváló hőtechnika", "A01 - forrás nélküli"),
    ("X12", r"214 m² (potenciál|használható|hasznos)", "C12 - korrigált érték"),
    ("X13", r"\+100 m²", "C11a - korrigált érték"),
    ("X14", r"2006 óta felújítás nem történt", "A11 - átírt állítás"),
    ("X15", r"tompítják a volatilitást", "A10 - forrás nélküli"),
]

SENSITIVE_TERMS = (r"örökhagyó|hagyatékátadó|hagyatéki|özvegyi|végrehajtási|anyja neve|"
                   r"személyi azonosító|született|bankszámla|értékpapír")
STRUCTURED_PII = [
    ("L01", r"\b[1-8]-\d{6}-\d{4}\b", "személyi azonosító-minta"),
    ("L02", r"\b\d{8}-\d{8}(-\d{8})?\b", "bankszámlaszám-minta"),
]
ALLOWED_STATUS = {"VERIFIED", "CORRECTED", "OUTDATED", "UNVERIFIABLE", "REFUTED"}


class TagChecker(HTMLParser):
    VOID = {"meta", "link", "br", "img", "hr", "input", "source", "area", "base", "col", "embed", "param", "track", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.errors.append(tag)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def table_rows(text: str, header_prefix: str):
    lines, rows, on = text.splitlines(), [], False
    for i, line in enumerate(lines):
        if not on and line.startswith(header_prefix):
            on = True
            continue
        if on:
            if line.startswith("|---"):
                continue
            if line.startswith("|"):
                rows.append([c.strip() for c in line.strip().strip("|").split("|")])
            else:
                break
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    write = ap.parse_args().write

    texts = {k: read(p) for k, p in FILES.items()}
    out, failures = [], 0

    # ---- 1. terv-tartalom lefedettség
    results = []
    for pid, title, claims, per_file in PLAN:
        marks, ok_count = {}, 0
        for key in FILES:
            pats = per_file.get(key)
            if pats is None:
                marks[key] = "-"
                continue
            ok = all(re.search(p, texts[key], re.S) for p in pats)
            marks[key] = "OK" if ok else "HIÁNYZIK"
            ok_count += ok
        required = len(per_file)
        status = "FULL" if ok_count == required else ("PARTIAL" if ok_count else "MISSING")
        results.append((pid, title, claims, marks, status))
    for xid, pattern, reason in FORBIDDEN:
        hits = {k: len(re.findall(pattern, t)) for k, t in texts.items()}
        status = "FULL" if not any(hits.values()) else "DIVERGED"
        marks = {k: ("nincs" if not v else f"{v} találat") for k, v in hits.items()}
        results.append((xid, f"Tiltott állítás hiánya: {pattern} ({reason})", "-", marks, status))

    total = len(results)
    counts = {s: sum(1 for r in results if r[4] == s) for s in ("FULL", "PARTIAL", "MISSING", "DIVERGED")}
    coverage = 100 * counts["FULL"] / total
    plan_ok = counts["FULL"] == total
    failures += not plan_ok

    # ---- 2. VCT lint
    vct = read(ART / "Validated-Claims.md")
    rows_a = [r for r in table_rows(vct, "| ID | Állítás (F0)") if re.match(r"C\d{2}[a-z]?$", r[0])]
    rows_b = {r[0]: r for r in table_rows(vct, "| ID | original_claim")}
    status_counts = {s: 0 for s in ALLOWED_STATUS}
    vct_problems = []
    for r in rows_a:
        st = r[3].split()[0] if r[3] else ""
        if st not in ALLOWED_STATUS:
            vct_problems.append(f"{r[0]}: érvénytelen státusz '{r[3]}'")
            continue
        status_counts[st] += 1
        if st in ("CORRECTED", "OUTDATED", "REFUTED"):
            detail = rows_b.get(r[0])
            if not detail or len(detail) < 6 or any(not c or c == "—" for c in detail[:6]):
                vct_problems.append(f"{r[0]}: hiányos korrekció-részletezés (B. tábla)")
    m = re.search(r"VERIFIED: (\d+) · CORRECTED: (\d+) · OUTDATED: (\d+) · UNVERIFIABLE: (\d+) · REFUTED: (\d+) · Összesen: (\d+)", vct)
    if not m:
        vct_problems.append("hiányzik az Összesítés sor")
    else:
        declared = dict(zip(("VERIFIED", "CORRECTED", "OUTDATED", "UNVERIFIABLE", "REFUTED"), map(int, m.groups()[:5])))
        if declared != status_counts or int(m.group(6)) != len(rows_a):
            vct_problems.append(f"az Összesítés ({declared}, {m.group(6)}) eltér a táblázattól ({status_counts}, {len(rows_a)})")
    vct_ok = not vct_problems and len(rows_a) > 0
    failures += not vct_ok

    # ---- 3. forráshivatkozás-lint
    registry = read(ART / "Source-Registry.md")
    registered = set(re.findall(r"^\| (S\d{3}) \|", registry, re.M))
    used = set()
    for t in list(texts.values()) + [vct]:
        used |= set(re.findall(r"\bS0\d{2}\b", t))
    unknown = sorted(used - registered)
    unused = sorted((registered - used) - {"S013"})
    src_ok = not unknown and not unused and bool(registered)
    failures += not src_ok

    # ---- 4. adatvédelmi lint
    scan_all = [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts
                and p.suffix in {".md", ".html", ".py", ".txt"} and p.name != "plan_vs_content.py"]
    scan_docs = [p for p in scan_all if p.suffix in {".md", ".html"}]
    pii_hits = []
    for pid, pattern, what in STRUCTURED_PII:
        for p in scan_all:
            if re.search(pattern, read(p)):
                pii_hits.append(f"{pid} {what}: {p.relative_to(ROOT)}")
    for p in scan_docs:
        if re.search(SENSITIVE_TERMS, read(p), re.I):
            pii_hits.append(f"érzékeny kifejezés: {p.relative_to(ROOT)}")
    for p in scan_docs:
        if re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", read(p)):
            pii_hits.append(f"e-mail-minta: {p.relative_to(ROOT)}")
    try:
        tracked = subprocess.run(["git", "ls-files", "--", str(ROOT)], capture_output=True, text=True, cwd=ROOT).stdout
        if re.search(r"\.pdf$", tracked, re.M | re.I):
            pii_hits.append("PDF van a verziókövetett fájlok között")
    except OSError:
        pass
    pii_ok = not pii_hits
    failures += not pii_ok

    # ---- 5. aritmetika
    arithmetic = [
        ("114 + 95 = 209", 114 + 95 == 209),
        ("114 + 100 = 214 (az F0 belső számítása)", 114 + 100 == 214),
        ("(95 - 100) / 100 = -5,0%", round((95 - 100) / 100 * 100, 1) == -5.0),
        ("95 / 114 ≈ 83% (adatlap: ~83%)", round(95 / 114 * 100) == 83),
    ]
    arith_ok = all(ok for _, ok in arithmetic)
    failures += not arith_ok

    # ---- 6. HTML-szerkezet
    tc = TagChecker()
    tc.feed(texts["html"])
    html_ok = not tc.stack and not tc.errors
    failures += not html_ok

    now = f"{datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC"
    out.append("# Plan-vs-Content — P06 terv-tartalom ellenőrzés\n")
    out.append(f"Futás: {now} · szkript: `BuildScripts/plan_vs_content.py` (a kimenet `--write`-tal frissül).\n")
    out.append(f"**Lefedettség: {counts['FULL']}/{total} = {coverage:.1f}%** — FULL: {counts['FULL']} · "
               f"PARTIAL: {counts['PARTIAL']} · MISSING: {counts['MISSING']} · DIVERGED: {counts['DIVERGED']}\n")
    out.append("## 1. Tétel-szintű eredmény\n")
    out.append("| ID | Tétel | Állítások | adatlap.md | index.html | befektetesi-elemzes.md | Állapot |")
    out.append("|---|---|---|---|---|---|---|")
    for pid, title, claims, marks, status in results:
        out.append(f"| {pid} | {title} | {claims} | {marks['md']} | {marks['html']} | {marks['an']} | {status} |")
    out.append("\n## 2. Lint-ellenőrzések\n")
    out.append("| Ellenőrzés | Eredmény | Részlet |")
    out.append("|---|---|---|")
    out.append(f"| Validated-Claims táblázat | {'PASS' if vct_ok else 'FAIL'} | {len(rows_a)} állítás; státuszok: "
               + ", ".join(f"{k} {v}" for k, v in sorted(status_counts.items())) + (" · " + "; ".join(vct_problems) if vct_problems else "") + " |")
    out.append(f"| Forráskódok (S0xx) | {'PASS' if src_ok else 'FAIL'} | {len(registered)} regisztrált, {len(used)} hivatkozott"
               + (f"; ismeretlen: {unknown}" if unknown else "") + (f"; használatlan: {unused}" if unused else "") + " |")
    out.append(f"| Adatvédelmi lint | {'PASS' if pii_ok else 'FAIL'} | {len(scan_all)} fájl átvizsgálva (azonosító-, számlaszám-, e-mail-minta; érzékeny kifejezések; PDF a verziókövetésben)"
               + (" · " + "; ".join(pii_hits) if pii_hits else "") + " |")
    out.append(f"| Aritmetika | {'PASS' if arith_ok else 'FAIL'} | " + "; ".join(f"{d}: {'OK' if ok else 'HIBA'}" for d, ok in arithmetic) + " |")
    out.append(f"| index.html szerkezet | {'PASS' if html_ok else 'FAIL'} | nyitva maradt: {tc.stack or '-'}; hibás zárás: {tc.errors or '-'} |")
    out.append("")
    text = "\n".join(out)
    print(text)
    if write:
        (ART / "Plan-vs-Content.md").write_text(text + "\n", encoding="utf-8")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
