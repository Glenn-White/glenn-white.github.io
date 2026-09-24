#!/usr/bin/env python3
"""
make_publications_pdf.py — build the downloadable publication list.

Reads the cached publications.json (the site's publication database)
and writes publications.pdf in the website root. The PDF is generated
data, not a hand-edited file: refresh the JSON (tools/update_publications.py)
and re-run this script — or just let the GitHub Action do it — and the
download always matches the database.

    python3 tools/make_publications_pdf.py

Standard library only; no dependencies. The PDF uses the built-in
Helvetica fonts (no embedding), groups entries by year and makes each
ORO link clickable.
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IN_FILE = ROOT / "publications.json"
OUT_FILE = ROOT / "publications.pdf"

# ---------- page geometry (PDF points, A4 portrait) ----------
PAGE_W, PAGE_H = 595.28, 841.89
MARGIN_X = 56
MARGIN_TOP = 56
MARGIN_BOTTOM = 58
CONTENT_W = PAGE_W - 2 * MARGIN_X

# palette (matches the website: navy ink, gold accent, muted grey)
NAVY = (0.047, 0.110, 0.188)
GOLD = (0.851, 0.643, 0.255)
INK = (0.20, 0.22, 0.25)
MUTED = (0.42, 0.45, 0.50)
LINK = (0.125, 0.333, 0.541)

# ---------- approximate Helvetica character widths (fraction of font size).
# Good enough to wrap lines without overflowing; the exact AFM metrics are
# not needed for a text list.
def _char_width(ch):
    if ch == " ":
        return 0.28
    if ch in "iljI.,;:'!|":
        return 0.30
    if ch in "ftr()[]{}/\\-":
        return 0.36
    if ch in "mwMW@":
        return 0.85
    if ch in "%&":
        return 0.78
    if ch.isupper() or ch.isdigit():
        return 0.66
    return 0.52

def text_width(s, size):
    return sum(_char_width(ch) for ch in s) * size

def wrap(text, size, width):
    """Greedy word wrap. Returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w) if cur else w
        if text_width(trial, size) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

# ---------- text encoding: WinAnsi (cp1252), with graceful fallbacks ----
TRANSLIT = {
    "‑": "-", "​": "", " ": " ", "‐": "-",
    "œ": "oe", "Œ": "OE", "Ÿ": "Y", "ß": "ss",
    "ı": "i", "ȷ": "j",
    "α": "alpha", "β": "beta", "γ": "gamma", "λ": "lambda",
    "μ": "mu", "π": "pi", "σ": "sigma", "τ": "tau",
    "χ": "chi", "ω": "omega", "Λ": "Lambda", "Σ": "Sigma",
    "−": "-", "⁄": "/", "→": "->", "×": "x", "≈": "~",
}

def to_winansi(s):
    out = []
    for ch in s:
        if ch in TRANSLIT:
            out.append(TRANSLIT[ch])
            continue
        try:
            ch.encode("cp1252")
            out.append(ch)
        except UnicodeEncodeError:
            out.append("?")
    return "".join(out)

def pdf_string(s):
    """Escape a WinAnsi string for a PDF literal string and encode it."""
    s = to_winansi(s).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    return s.encode("cp1252", errors="replace")

def fmt(rgb):
    return "{:.3f} {:.3f} {:.3f}".format(*rgb)

# ---------- page builder ----------
class Doc:
    def __init__(self):
        self.pages = []          # each: {"ops": [bytes], "annots": [bytes]}

    def page(self):
        p = {"ops": [], "annots": []}
        self.pages.append(p)
        return p

    def text(self, page, x, y, s, font, size, rgb):
        page["ops"].append(
            "BT /{} {} Tf {} rg {} {} Td (".format(font, size, fmt(rgb), x, round(y, 1)).encode()
            + pdf_string(s)
            + b") Tj ET"
        )

    def rect(self, page, x, y, w, h, rgb):
        page["ops"].append(
            "q {} rg {} {} {} {} re f Q".format(fmt(rgb), round(x, 1), round(y, 1),
                                                round(w, 1), round(h, 1)).encode()
        )

    def link(self, page, x, y, w, h, url):
        page["annots"].append(
            "<< /Subtype /Link /Rect [{} {} {} {}] /Border [0 0 0] /A << /S /URI /URI (".format(
                round(x, 1), round(y - 2, 1), round(x + w, 1), round(y + h, 1)
            ).encode()
            + pdf_string(url)
            + b") >> >>"
        )


def build_pdf(data):
    pubs = data["publications"]
    meta = data.get("meta", {})
    total = len(pubs)
    years = sorted({p["year"] for p in pubs}, reverse=True)
    as_of = (meta.get("fetched") or "") or datetime.now().strftime("%Y-%m-%d")

    doc = Doc()
    page = doc.page()
    y = PAGE_H - MARGIN_TOP

    # ---- first-page title block ----
    doc.text(page, MARGIN_X, y, "Glenn J. White", "F2", 21, NAVY); y -= 20
    doc.text(page, MARGIN_X, y, "Publications", "F2", 14, GOLD); y -= 16
    doc.text(page, MARGIN_X, y,
             "{} publications, {} – {} · list generated from the publication database ({}), each entry linked to ORO.".format(
                 total, years[-1], years[0], as_of),
             "F1", 8.5, MUTED)
    y -= 8
    doc.rect(page, MARGIN_X, y, CONTENT_W, 1.2, GOLD)
    y -= 22

    BOTTOM = MARGIN_BOTTOM + 14

    def new_page():
        nonlocal page, y
        page = doc.page()
        y = PAGE_H - MARGIN_TOP + 6
        doc.text(page, MARGIN_X, y, "Glenn J. White — Publications", "F1", 8, MUTED)
        y -= 18

    def ensure(h):
        nonlocal page, y
        if y - h < BOTTOM:
            new_page()

    for year in years:
        entries = [p for p in pubs if p["year"] == year]
        # year heading: keep with the first lines of its first entry
        ensure(24 + 3 * 11)
        y -= 4
        doc.text(page, MARGIN_X, y, str(year), "F2", 12.5, NAVY)
        doc.rect(page, MARGIN_X, y - 4.5, 26, 2.2, GOLD)
        y -= 19

        for p in entries:
            title_lines = wrap(p["title"], 9.5, CONTENT_W)
            cit_lines = wrap(p["citation"], 8.8, CONTENT_W - 10)
            url = p.get("url", "")
            need = 6 + len(title_lines) * 11.5 + len(cit_lines) * 10.5 + (11 if url else 0) + 8
            ensure(min(need, 60))
            y -= 5

            for ln in title_lines:
                ensure(11.5)
                doc.text(page, MARGIN_X, y, ln, "F2", 9.5, INK)
                y -= 11.5
            for ln in cit_lines:
                ensure(10.5)
                doc.text(page, MARGIN_X + 10, y, ln, "F1", 8.8, MUTED)
                y -= 10.5
            if url:
                ensure(11)
                doc.text(page, MARGIN_X + 10, y, url, "F1", 8.3, LINK)
                doc.link(page, MARGIN_X + 10, y, min(text_width(url, 8.3), CONTENT_W - 10), 9, url)
                y -= 11
            y -= 4.5

    # ---- footers (need the final page count) ----
    n = len(doc.pages)
    for i, p in enumerate(doc.pages, 1):
        doc.text(p, PAGE_W / 2 - 40, MARGIN_BOTTOM - 26,
                 "page {} of {}".format(i, n), "F1", 8, MUTED)
    return doc


def emit(doc, data):
    """Serialise the laid-out document to PDF bytes."""
    objects = []  # (obj number, payload bytes); index == obj number - 1

    def add(payload):
        objects.append(payload)
        return len(objects)

    # 1: catalog, 2: pages tree, 3: F1, 4: F2  (numbers fixed for reference)
    add(b"")  # placeholder 1
    add(b"")  # placeholder 2
    fonts = [
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>",
    ]
    add(fonts[0])  # 3
    add(fonts[1])  # 4
    info_num = add(b"")  # 5, filled below

    page_nums = []
    for p in doc.pages:
        stream = b"\n".join(p["ops"])
        contents_num = add(b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n"
                           + stream + b"\nendstream")
        annots = b"[" + b" ".join(p["annots"]) + b"]" if p["annots"] else b""
        annots_ref = b"/Annots " + annots if p["annots"] else b""
        page_nums.append(add(
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 "
            + "{:.2f} {:.2f}".format(PAGE_W, PAGE_H).encode()
            + b"] /Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents "
            + str(contents_num).encode() + b" 0 R" + annots_ref + b" >>"
        ))

    kids = b"[" + b" ".join("{} 0 R".format(n_).encode() for n_ in page_nums) + b"]"
    objects[0] = b"<< /Type /Catalog /Pages 2 0 R >>"
    objects[1] = b"<< /Type /Pages /Count " + str(len(page_nums)).encode() + b" /Kids " + kids + b" >>"
    now = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    objects[info_num - 1] = (
        b"<< /Title (" + pdf_string("Glenn J. White — Publications")
        + b") /Author (" + pdf_string("Glenn J. White")
        + b") /Subject (" + pdf_string("Complete publication list, generated from publications.json")
        + b") /Producer (tools/make_publications_pdf.py) /CreationDate (D:" + now.encode() + b") >>"
    )

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0] * (len(objects) + 1)
    for i, payload in enumerate(objects, 1):
        offsets[i] = len(out)
        out += str(i).encode() + b" 0 obj\n" + payload + b"\nendobj\n"
    xref_at = len(out)
    out += b"xref\n0 " + str(len(objects) + 1).encode() + b"\n"
    out += b"0000000000 65535 f \n"
    for off in offsets[1:]:
        out += "{:010d} 00000 n \n".format(off).encode()
    out += (b"trailer\n<< /Size " + str(len(objects) + 1).encode()
            + b" /Root 1 0 R /Info " + str(info_num).encode() + b" 0 R >>\n"
            + b"startxref\n" + str(xref_at).encode() + b"\n%%EOF\n")
    return bytes(out)


def main():
    if not IN_FILE.exists():
        raise SystemExit("publications.json not found — run tools/update_publications.py first.")
    data = json.loads(IN_FILE.read_text(encoding="utf-8"))
    doc = build_pdf(data)
    pdf = emit(doc, data)
    OUT_FILE.write_bytes(pdf)
    n_pages = len(doc.pages)
    print(f"Wrote {OUT_FILE.name}: {len(data['publications'])} publications, "
          f"{n_pages} pages, {len(pdf) / 1024:.0f} KiB.")


if __name__ == "__main__":
    main()
