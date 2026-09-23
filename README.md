# Glenn White — academic website

A hand-editable, dependency-free static website for a university professor's personal
page. Structure and look inspired by well-regarded academic sites (notably
saraseager.com — the design here is original; no code was copied). Plain HTML + one
CSS file: no frameworks, no build step, no trackers, no external fonts.

## What's here

```
website/
  index.html           Home — hero, intro, news, research highlights, recent papers
  about.html           Biography, career timeline, awards, CV download
  research.html        Research themes (one section per theme)
  projects.html        Named projects / missions / surveys / instruments
  publications.html    Publications page — renders the cached JSON below
  outreach.html        Public talks, media, writing & resources
  contact.html         Address, office hours, map embed, notes for correspondents
  publications.json    All 500+ publication records, cached locally (data file)
  js/publications.js   Renders publications.json onto the page (filter + search)
  tools/update_publications.py   Re-downloads the OU profile and refreshes the cache
  css/style.css        The entire design — colours set once in :root at the top
  images/              portrait.jpg (your OU profile photo) + placeholder SVGs
  cv/cv.pdf            Placeholder CV (replace with your real one)
  .nojekyll            Tells GitHub Pages to serve files as-is
  .gitignore           Keeps macOS noise out of the repo
```

## Publications cache

The publications page does **not** call any university server: all records live in
`publications.json`, a snapshot of the OU Profiles page
(profiles.open.ac.uk/glenn-joseph-white) taken on 2026-09-23 — 507 records
(1975–2026), each linking out to its ORO repository entry. The page renders
them with a type filter and text search via `js/publications.js`.

To refresh the cache after new papers appear on the OU profile:

```bash
cd website
python3 tools/update_publications.py
git add -A && git commit -m "Refresh publication cache" && git push
```

Note: `publications.json` is loaded with `fetch()`, which browsers block on
`file://` addresses — preview via `python3 -m http.server` rather than
double-clicking the file.

## Published — GitHub Pages

The site is **live** at <https://glenn-white.github.io/> — a GitHub *user page*,
served from the `glenn-white/glenn-white.github.io` repository (renamed from
`Website` on 2026-09-23). This folder is that repository's working copy, with
`origin` pointing at it. Every internal link is relative, so the tree also
works unchanged at any subpath if it is ever moved.

To publish an edit: change a file here, then
```bash
git add -A && git commit -m "..." && git push
```
GitHub serves the static files as-is (`.nojekyll`), so updates appear
near-instantly after the push.

Note: this folder currently lives inside the SAPIENS repository's directory. It is
excluded from SAPIENS git via `.git/info/exclude` (local-only), so SAPIENS commits
can never pick it up — but treat `website/` as its own project and init git here
as above.

## Editing

- **Text**: open any `.html` file in a text editor. Everything editable sits
  between `<!-- ==== ... ==== -->` comment banners, and placeholders look like
  `[Your University]`, `[Month Year]`, `[Paper title]`. Search for `[` to find
  every placeholder in a file. Edits appear the moment you save and push.
- **Add a news item** (home page): copy one `<li>…</li>` inside the news `<ul>`
  and edit it. Keep 4–6 newest; delete old ones.
- **Add a publication**: copy one `<div class="pub">…</div>` block under the
  right year heading. To start a new year, copy a `<h2 class="year-head">` line.
- **Add a research theme / project / group member / course**: copy the whole
  marked `<section>` / `<article>` / `.person` / `.course` block and edit it.
- **Images**: replace the files in `images/` with your own (keeping the names,
  e.g. drop in `hero.jpg` and change `hero.svg` → `hero.jpg` in the one place
  it's referenced — the top of `css/style.css` — or just overwrite with an SVG of
  your own). Astronomy tip: NASA and ESA imagery is generally public domain /
  free to use with credit — put the credit in the image caption or `alt` text.
- **Colours and fonts**: edit the variables in the `:root { … }` block at the
  top of `css/style.css` — change `--navy` and `--accent` and the whole site
  re-themes (hero, buttons, timeline, footer, everything).
- **Your CV**: replace `cv/cv.pdf` with your real CV PDF, same filename.

## Preview locally

Double-click `index.html`, or for a proper local server:

```bash
cd website
python3 -m http.server 8000
# then open http://localhost:8000
```

## Good practice (from studying the best academic sites)

- Keep a **short plain-language bio above the fold**; write for an interested
  undergraduate, not a committee.
- Link publications to **ADS / arXiv / ORCID / Google Scholar** rather than
  duplicating the full record — this page groups by year and lets ADS be the
  archive of record.
- Keep a **"latest" strip alive**: even a twice-yearly news update signals a
  maintained site.
- Give something: open lecture notes, datasets, explainers. The most-visited
  professor pages give, not just show.
- Ask the university to make your departmental profile page **redirect** (or at
  least link) to this site — a stable personal address outlives any university
  CMS migration.

## Licence suggestion

Your content is yours. If you want to mark the template itself as freely
reusable, add a CC0/MIT licence file — but that's entirely optional.
