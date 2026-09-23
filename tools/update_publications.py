#!/usr/bin/env python3
"""
update_publications.py — refresh the local publication cache.

Downloads the OU Profiles page for Glenn Joseph White, parses every
publication entry, and rewrites publications.json in this website folder.
The website then serves the cached records — it never calls the OU server.

Run from the website root:
    python3 tools/update_publications.py

Standard library only; no dependencies.
"""

import json
import re
import urllib.request
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

PROFILE_URL = "https://profiles.open.ac.uk/glenn-joseph-white"
USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
              "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15")
OUT_FILE = Path(__file__).resolve().parent.parent / "publications.json"


class PubParser(HTMLParser):
    """Extracts publication entries from the OU Profiles HTML."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.type_map = {}
        self.pubs = []
        self.cur_type = None
        self.cur = None
        self.capture = None
        self.buf = []
        self.pending_href = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "section" and "citation-section" in a.get("class", ""):
            self.cur_type = a.get("id")
        elif tag == "h3" and self.cur_type:
            self.capture, self.buf = "h3", []
        elif tag == "div" and "data-publicationyear" in a:
            self.cur = {"type": self.cur_type,
                        "year": int(a["data-publicationyear"]),
                        "title": "", "url": "", "citation": ""}
        elif tag == "a" and self.cur is not None:
            self.capture, self.buf, self.pending_href = "a", [], a.get("href", "")
        elif tag == "p" and self.cur is not None:
            self.capture, self.buf = "p", []

    def handle_endtag(self, tag):
        if tag == "h3" and self.capture == "h3":
            self.type_map[self.cur_type] = " ".join("".join(self.buf).split())
            self.capture = None
        elif tag == "a" and self.capture == "a" and self.cur is not None:
            self.cur["title"] = " ".join("".join(self.buf).split())
            self.cur["url"] = self.pending_href
            self.capture = None
        elif tag == "p" and self.capture == "p" and self.cur is not None:
            self.cur["citation"] = " ".join("".join(self.buf).split())
            self.capture = None
        elif tag == "div" and self.cur is not None:
            if self.cur["title"] and self.cur["url"]:
                self.pubs.append(self.cur)
            self.cur = None
        elif tag == "section" and self.cur_type:
            self.cur_type = None

    def handle_data(self, data):
        if self.capture:
            self.buf.append(data)


def main():
    print(f"Downloading {PROFILE_URL} …")
    req = urllib.request.Request(PROFILE_URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        html = resp.read().decode("utf-8", errors="replace")

    parser = PubParser()
    parser.feed(html)
    pubs = [r for r in parser.pubs if r["title"] and r["url"]]
    if not pubs:
        raise SystemExit("No publications found — the page layout may have changed. "
                         "Nothing was written.")

    # the profile page mixes http:// and https:// ORO links — normalise to https
    for r in pubs:
        if r["url"].startswith("http://oro.open.ac.uk"):
            r["url"] = "https://" + r["url"][len("http://"):]

    pubs.sort(key=lambda r: (-r["year"], r["title"]))
    from collections import Counter
    data = {
        "meta": {
            "person": "Glenn J. White",
            "source_url": PROFILE_URL,
            "source_note": ("Cached snapshot of the OU Profiles publication list; "
                            "per-record links point to ORO (oro.open.ac.uk), the Open "
                            "University's research repository."),
            "fetched": date.today().isoformat(),
            "counts": {"total": len(pubs),
                       "by_type": dict(Counter(r["type"] for r in pubs))},
            "type_names": parser.type_map,
        },
        "publications": pubs,
    }
    OUT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=1),
                        encoding="utf-8")
    print(f"Wrote {len(pubs)} records to {OUT_FILE}")
    print("By type:", data["meta"]["counts"]["by_type"])


if __name__ == "__main__":
    main()
