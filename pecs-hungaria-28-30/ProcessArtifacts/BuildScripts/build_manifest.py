#!/usr/bin/env python3
"""P10 - a csomag fájlleltára (Manifest.md): fájlnév, könyvtár, méret, szószám, állapot,
teljességi ellenőrzés. A leltár a verziókövetésbe kerülő fájlokat sorolja fel
(git által követett vagy nem ignorált új fájlok); a helyi, nem verziózott forrás-PDF-ek
külön szakaszban, csak méret és SHA-256 alapján szerepelnek.

Használat:  python3 build_manifest.py [--write]
"""
import argparse
import hashlib
import py_compile
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SELF_NAME = "Manifest.md"
PLACEHOLDER = re.compile(r"\b(TODO|TBD|FIXME|XXX)\b")
PROBLEMS = {"ÜRES", "helykitöltő szöveg maradt", "HTML-szerkezet HIBÁS", "Python-fordítás HIBÁS"}


class TagChecker(HTMLParser):
    VOID = {"meta", "link", "br", "img", "hr", "input", "source", "area", "base", "col", "embed", "param", "track", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors, self.text = [], [], []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("style", "script"):
            self._skip += 1
        if tag not in self.VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in ("style", "script"):
            self._skip -= 1
        if tag in self.VOID:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.errors.append(tag)

    def handle_data(self, data):
        if not self._skip:
            self.text.append(data)


def package_files():
    def git(*args):
        result = subprocess.run(["git", *args, "--", "."], capture_output=True, text=True, cwd=ROOT)
        return result.stdout.split("\n")
    names = {n for n in git("ls-files") + git("ls-files", "--others", "--exclude-standard") if n}
    return sorted(ROOT / n for n in names if (ROOT / n).is_file())


def inspect(path: Path):
    text = path.read_text(encoding="utf-8")
    suffix = path.suffix
    if suffix == ".html":
        tc = TagChecker()
        tc.feed(text)
        words = len(" ".join(tc.text).split())
        ok = not tc.stack and not tc.errors
        return words, "HTML-szerkezet rendben" if ok else "HTML-szerkezet HIBÁS"
    words = len(text.split())
    if suffix == ".py":
        try:
            with tempfile.TemporaryDirectory() as tmp:
                py_compile.compile(str(path), cfile=str(Path(tmp) / "x.pyc"), doraise=True)
            return words, "Python-fordítás rendben"
        except py_compile.PyCompileError:
            return words, "Python-fordítás HIBÁS"
    if not text.strip():
        return words, "ÜRES"
    if PLACEHOLDER.search(text):
        return words, "helykitöltő szöveg maradt"
    return words, "nem üres, nincs helykitöltő"


def status_for(rel: Path):
    top = rel.parts[0] if rel.parts else ""
    if top == "Deliverables":
        return "DRAFT (felhasználói jóváhagyásra vár)"
    if top == "ProcessArtifacts" and "BuildScripts" in rel.parts:
        return "TESTED"
    if top == "ProcessArtifacts":
        return "DRAFT"
    return "OK"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    write = ap.parse_args().write

    rows, total_kb, total_words, problems = [], 0.0, 0, 0
    for path in package_files():
        rel = path.relative_to(ROOT)
        if rel.name == SELF_NAME:
            continue
        words, check = inspect(path)
        size_kb = path.stat().st_size / 1024
        total_kb += size_kb
        total_words += words
        problems += check in PROBLEMS
        rows.append((rel.name, str(rel.parent) if str(rel.parent) != "." else "(gyökér)", f"{size_kb:.1f}", words, status_for(rel), check))

    if not rows:
        sys.exit("Hiba: a leltár üres; a git-lista nem adott fájlokat.")

    out = ["# Manifest — a csomag fájlleltára\n",
           f"Generálva: {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC · szkript: `BuildScripts/build_manifest.py`. "
           f"A leltár a saját fájlját (`{SELF_NAME}`) nem tartalmazza.\n",
           "## Verziókövetésbe kerülő fájlok\n",
           "| Fájl | Könyvtár | KB | Szó | Állapot | Teljességi ellenőrzés |",
           "|---|---|---|---|---|---|"]
    out += [f"| `{n}` | {d} | {kb} | {w} | {st} | {chk} |" for n, d, kb, w, st, chk in rows]
    out.append(f"\n**Összesen:** {len(rows)} fájl · {total_kb:.1f} KB · {total_words} szó · ellenőrzési probléma: {problems}\n")

    sources = ROOT / "Sources"
    pdfs = sorted(sources.glob("*.pdf")) if sources.exists() else []
    out.append("## Helyi, nem verziózott forrásfájlok (`.gitignore` kizárja)\n")
    if pdfs:
        out += ["| Fájl | KB | SHA-256 |", "|---|---|---|"]
        for p in pdfs:
            out.append(f"| `{p.name}` | {p.stat().st_size / 1024:.1f} | `{hashlib.sha256(p.read_bytes()).hexdigest()}` |")
    else:
        out.append("Nincs helyi forrásfájl ezen a gépen; a várt azonosítók a `Sources/README.md`-ben vannak.")
    text = "\n".join(out) + "\n"
    print(text)
    if write:
        (ROOT / "ProcessArtifacts" / SELF_NAME).write_text(text, encoding="utf-8")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
