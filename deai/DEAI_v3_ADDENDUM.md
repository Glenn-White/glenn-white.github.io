# DEAI v3.0 Addendum (2026-10-17; §T added 2026-10-18)

Merged and adjudicated from two external reviews (ChatGPT, Claude) of v2.0.
Where this addendum and the v2.0 body disagree, this addendum wins.
§T (voice-model workflow) operationalises §S after the first two live
deployments (SMGPS PN census v1.45; technosignatures 40 pc v4.23).

## A. Test classes (supersedes all threshold-conflict clauses)

- **Class A — correctness constraints (mandatory, must pass):** scientific
  propositions preserved; numerical values and their referents preserved;
  nothing invented; no unsupported strengthening of claims; no new
  contradictions; references and equations correct; LaTeX compiles.
- **Class B — diagnostic stylistic indicators:** generate review flags.
  A manuscript may legitimately finish outside a reference band if every
  flagged instance has been examined and either fixed or given a written
  keep-reason. The stopping criterion is "every significant flag resolved or
  adjudicated", never "every statistic forced below threshold".
- Battery rows are Class B unless named in Class A above. B-22 (hedge total)
  and B-09 (reporting-verb share) are descriptive statistics only — never a
  rewrite trigger by themselves. Removing the last hedge on a claim is a
  ladder change under I-3 and goes to the author-decisions file.

## B. I-1 amended (printed precision vs quantity)

I-1 protects the underlying *quantity and its meaning*, not the exact printed
string. Rounding/precision harmonisation (1.23456±0.12 → 1.23±0.12), unit or
notation changes are allowed only with an explicit equivalence check and a
change-log entry. Changed measured values still require author approval.

## C. Semantic integrity (lightweight, bidirectional)

For every scientifically meaningful changed sentence, check before/after for:
denominator or population changes; quantifier changes (all/most/some/none);
condition and exception changes; causal-direction changes; comparison
direction; upper vs lower limits; statistical confidence; frequency/temporal
ranges; observation vs interpretation vs prediction status. Every original
proposition must appear in the revision, and no revised proposition may be
stronger than the original supports.

## D. Default-to-preserve; minimal edit; reviser self-audit

- **RV-01** Prefer, in order: delete; cut a clause; reorder; replace a word;
  rewrite the sentence; rewrite the paragraph. The default action is to
  PRESERVE the original text; revision requires evidence of a defect and
  evidence the change improves it.
- **RV-02 / B-33** Edit budget: fraction of body sentences changed
  (normalised edit distance > 0.3). Above 40% in any section, stop and
  report to the author before continuing.
- **RV-03 / B-29** New-text audit: run the full battery on the
  inserted/rewritten sentences alone; no rate may be worse than the same
  rate on unchanged sentences.
- **RV-04** Where more than one model family is available, judging tasks
  (T-02/T-03/T-06, simulated referees) go to a different family; otherwise
  the judge sees original+revised without the reviser's reasoning.

## E. Coined terminology (CT)

- **CT-01** Register every noun phrase occurring ≥3 times whose usage is not
  standard in the subfield (ADS full-text check where available; otherwise
  flag as candidate for author review).
- **CT-02** Replace a coined term with the standard term where one exists.
- **CT-03** A kept coined term is defined once at first use, in plain words,
  with no variants thereafter.
- **CT-04** No coined term in the Title; none undefined in the Abstract.
- **CT-05 / B-30** Coined terms per 1000 words, flag above 2.
- **CT-06** Flag non-standard quantitative idioms ("nine times in ten")
  where the field writes "90 per cent".

## F. Title, keywords, headings (TH)

**TH-01** Flag title formulas: colon-subtitle, "Unveiling/Towards/A
comprehensive/Insights into/Exploring", question titles, >20 words, coined
terms, unexplained acronyms. **TH-02** MNRAS keywords from the official
list only. **TH-03** Flag gerund headings, colon headings, identical
heading patterns across sections, subsections with a single paragraph.

## G. LaTeX/PDF/file hygiene (LX) — the arXiv source is public

**LX-01** Strip comments before submission; grep for model/agent/version/
TODO/FIXME mentions. **LX-02** Remove unused figures/files/packages/macros.
**LX-03** File names free of internal version strings or run identifiers.
**LX-04 / B-31** \textbf/\emph emphasis in body prose ≤1/1000 (definition
at first use exempt). **LX-05** No itemize/enumerate in Intro body/
Discussion/Conclusions (contribution list at end of Intro acceptable).
**LX-06** Flag hard-coded spacing fixes. **LX-07** PDF metadata (Title,
Author, Creator, Producer, XMP) clean and correct. Duplicate labels, unused
refs, overfull boxes, page-by-page PDF diff vs original.

## H. Figures (FG), tables (TB), equations/acronyms (EQ/AC)

- **FG-01** Every number quoted from a figure matches the plotted data
  (read from data files where available; else NOT VERIFIABLE).
- **FG-02** Flag automated-plot tells: in-plot titles, default matplotlib
  style/fonts, internal paths in labels, identical layouts across unlike
  figures. **FG-03** Axis labels carry quantity and unit consistently.
- **FG-04** Captions self-contained: what is plotted, symbols, sample; no
  interpretation ("clearly showing..."). **FG-05** Panel letters exist and
  are all referred to. **FG-06** No undeclared AI-generated images.
- **TB-01** No verdict words in table cells. **TB-02** Headers carry units;
  consistent significant figures. **TB-03** Notes define every symbol.
  **TB-04** Main-text tables ≤1 page; per-object tables to supplement.
- **EQ-01..04** Symbols defined at first use; one meaning per symbol; number
  only referenced equations; notation consistent across text/tables/figures.
- **AC-01 / B-34** Acronym register: defined once at first use, used ≥3
  times, not defined twice, not defined-and-unused; Abstract defines its own.

## I. House style (HS); editor-read statements (ST)

**HS-01** "per cent" not "%" in running text. **HS-02** Numbers <10 in
words except with units/ranges/technical lists; no numeral sentence starts.
**HS-03** One scientific-notation form. **HS-04** MNRAS reference style
(Section 3, Fig. 2, equation (4)). **HS-05** Past=done, present=shown;
flag unexplained tense switching. **HS-06** Confidence stated with
intervals; do not mix sigma and percentiles silently.
**ST-01** Facility acknowledgements verbatim from current policy pages.
**ST-02** Software cited as its authors request. **ST-03** Specific data
availability (archive, project IDs, DOIs); flag "on reasonable request"
when data are public. **ST-04** AI disclosure specific and accurate.

## J. Literature (LT); overlap (OV)

**LT-01** ADS search of last 24 months on topic/objects/method; list
expected-but-absent papers for the author (never auto-cite unread papers).
**LT-02** Cite published versions of arXiv-only cites. **LT-03** Check
"recently/to date/state of the art" claims. **LT-04** Verify quoted
instrument/survey parameters against release papers. **LT-05** Self-citation
pattern sane. **OV-01/B-35** Flag ≥12-word identical runs or >80%-overlap
sentences vs cited/own papers (where full text available; else NOT
VERIFIABLE). **OV-02** Own-paper text recycling needs a citation.

## K. Reader tests (RT); simulated referees (SR)

**RT-01** Reverse outline (first sentences of paragraphs in order must
summarise the argument). **RT-02** Stage-0 stumble log resolved.
**RT-03** Abstract stand-alone test (fresh agent: observation, measurement,
main number, meaning). **RT-04** Figures-only test. **RT-05** Length
proportions vs subfield norms (flag >P90; appendix repetition).
**RT-06 / B-32** Cross-references ≤3/1000. **SR-1..4** Four fresh referee
agents: subfield expert; statistician; 5-minute desk editor; sceptic. Every
concern answered in the audit report or escalated to author decisions.

## L. Segmentation validation (SG) — before any sentence metric is trusted

**SG-01** Astronomy abbreviation list (et al., Fig., e.g., i.e., cf., Eq.,
Sect., approx.) with the splitter. **SG-02 / B-36** Print 50 random
segmented sentences and check boundaries; >2 wrong → fix splitter first and
record the check. A metric whose parser failed is NOT RUN, never zero.

## M. Editing ≠ refereeing (new report structure)

Statistical reasoning audit (ST-01..ST-18 defect list from the ChatGPT
review), claim provenance (P1 measured / P2 derived / P3 literature / P4
interpretation / P5 speculation / P6 unsupported), reproducibility ladder
(verified / in-principle / partial / not-reproducible), and dependency-graph
change-impact checks produce findings in a **separate referee report**
(`deai_referee_report.md`) and author decisions — they are NEVER resolved by
rewriting the sentence. Only language/structure defects are edited directly.
Where the research record is not supplied, dependent checks report NOT
VERIFIABLE, never pass.

## N. Execution manifest (machine-verifiable)

Every mandatory test produces a row: Test ID | Status
(PASS/REVIEW/NOT-APPLICABLE/NOT-RUN/FAIL) | Input file+version | Method |
Result | Evidence location | Action | Verification | Reason. A missing
result is never silently a waiver; a fresh reviewing agent inspects the
manifest against the actual outputs. Final verdicts are status words, not
0–100 scores.

## O. New battery rows (append to §5.13)

| # | Metric | Threshold |
|---|--------|-----------|
| B-29 | New-text audit: rates on rewritten vs unchanged sentences | no rate worse |
| B-30 | Coined terms /1000; undefined in Abstract | ≤2; 0 |
| B-31 | Emphasis commands in body prose /1000 | ≤1 |
| B-32 | Cross-references /1000 | ≤3 |
| B-33 | Fraction of body sentences changed, per section | ≤40% or author approval |
| B-34 | Acronym anomalies (undefined / double-defined / used <3×) | 0 |
| B-35 | Text-overlap runs ≥12 words vs cited/own papers | 0 outside quotes/boilerplate |
| B-36 | Segmentation spot-check errors in 50 sentences | ≤2 |
| B-37 | Manuscript voice distance D vs author profile (§S; conditional on S-01) | within author-paper range |
| B-38 | Voice distance of changed vs unchanged sentences | not worse |

New gates T-14..T-22 per the reviews: adversarial fixtures pass; coined-term
register complete; LX/FG/TB/ST checks pass; LT-01 list delivered; OV passes;
four referees answered; B-29 passes and B-33 respected.

## P. Adversarial fixture set (AD-1..AD-10)

Kept in `astra_core/deai/adversarial/`; run before every live revision:
essential contrast kept with reason; protected terms unflagged; short
factual sentence kept; human paragraph with 2 tells not rewritten; unit
duplicates reconciled; distinct denominators not merged; fluent wrong
physics flagged; necessary hedge kept; coined term defined-and-consistent
kept and registered; number re-attachment fails the tuple diff.

## Q. Deferred (explicitly NOT RUN, not silently skipped)

False-positive calibration corpus and the three validation experiments
(human-written control papers; corrupted-manuscript detection trial; blinded
A/B/C human rating) — require a human-scored corpus and blind reviewers;
recorded as the protocol's principal outstanding validation debt. Burrows'
Delta voice modelling refinement likewise deferred.

## R. Watermark awareness (factual; NOT an evasion module)

Statistical text watermarking (SynthID-Text-style, reported deployed by
Anthropic Aug 2026) is a cryptographic signal in low-stakes token choices,
detectable only by the key-holder. It is ORTHOGONAL to every battery row in
this protocol: DEAI measures human-visible stylistic distributions and
cannot detect, measure, or certify removal of a key-based watermark. No
gate claiming "watermark removed" may ever be emitted — it would be
unverifiable by construction (protocol rule: nothing asserted without
verification). Known facts from the deploying party's own documentation:
the signal applies only to model-chosen tokens (weak where the model edits
existing author text), survives light editing, and is removed by complete
rewriting — but none of these are testable offline.

The protocol's position: the correct handling of AI-assistance
transparency is ST-04 (specific, accurate disclosure), which journal policy
requires independently of any watermark. DEAI is a prose-quality tool, not
a transparency-defeat tool, and must not be advertised or used as the
latter. The minimal-edit principle (RV-01) keeps authorship where it
belongs — the author's own words are the author's own words.

## S. Author-voice model (B-37/B-38; gate is CONDITIONAL)

`deai_voice.py` builds a stylometric profile from the author's own corpus
(pdftotext dumps of their papers) and scores any manuscript by mean |z|
distance D from that profile (Burrows'-Delta-style, extended features:
function words, hedges, punctuation, sentence-length distribution,
openers, passive mix).

- **S-01** The gate is active ONLY after `validate` mode separates: every
  held-out author paper must score closer than every control (other-author)
  paper. Until then, voice rows are REPORT-ONLY diagnostics.
- **B-37** Manuscript voice distance D (whole body). Threshold: within the
  range spanned by the author's own papers. Outside → REVIEW with the
  worst contributing features listed; never force down by rewrite alone.
- **B-38** Voice audit of edits: the changed-sentence set must not have a
  worse D than the unchanged set (generalises B-29 to the voice model).
- Voice distance is Class B: a legitimate manuscript may sit outside the
  band with a written keep-reason. §R applies in full — the voice model
  measures style, not watermark presence or absence.

## T. Voice-model workflow (operational; refines V-04, §S, B-37/B-38)

Everything needed to reproduce the 2026-10-18 voice-model revision process.
§S defines the gate; this section defines HOW the profile is built, scored
honestly, and acted on. First deployment: SMGPS PN census v1.45 (rounds 4–8)
and technosignatures 40 pc v4.23.

### T-1 Corpus construction (broad-spectrum, per author directive 2026-10-18)
- **T-1.1** The training corpus must span the author's full topic range, not
  one subfield: scrape the author's publications page (all papers count as
  the author's writing regardless of lead author; >50 permitted; aim ≥150
  usable documents). Reference build: 507 records → 186 arXiv PDFs →
  175 usable text documents (2.2 M words), in `DEAI_files/voice_corpus/`
  (`publications.json`, `selection.json`, `pdfs/`, `txt/`).
- **T-1.2** Institutional-repository PDF links (ORO etc.) are commonly
  Cloudflare-blocked (403 on record pages AND direct PDF URLs) — go straight
  to the arXiv API. Gotchas encoded in `fetch_corpus.py`: phrase queries need
  `+` between words (not `%20`); never `quote()` the already-encoded query
  (double-encoding breaks `%22`); KEEP hyphens in titles; serialise one
  process, ≥6 s between requests, 429-backoff (30×attempt s) — parallel or
  duplicate fetchers extend a rate-limit block >5 min; never `import` the
  fetch script (module import re-runs it).
- **T-1.3** Reserve 8 author holdouts + 8 other-author controls (matched
  astro-ph papers) BEFORE profile building; they are the S-01 validation set.

### T-2 Profile building (topic-robust features)
- **T-2.1** Build with `deai_voice.py build` on pdftotext dumps; then select
  features by Fisher score (author-vs-control separation) over the
  topic-robust whitelist ROBUST_KEYS (rhythm, punctuation, connectives,
  openers, hedges, Zwe/Zpassive/Zreport). Prepositions, numerals and pronoun
  rates are EXCLUDED: they track subject matter, not the hand. Deployed:
  25-feature profile (r25; r15/r45 variants kept for sensitivity).
- **T-2.2** Profile hygiene (in `build`): features present in fewer than
  max(2, n/3) documents are dropped; every feature sd floored at
  max(sd, 0.15·mean, 0.05) — without the floor, quiet features explode the
  z-distance (observed D≈3.2×10⁴ on a zero-mean feature).
- **T-2.3** Run `validate` (holdouts vs controls). Deployment result:
  means separate (0.89 vs 1.20) but tails touch ⇒ S-01 FAILED ⇒ **the voice
  gate is permanently REPORT-ONLY** for this profile; B-37/B-38 produce
  diagnostics with keep-reasons, never rewrites forced by Dr.

### T-3 Honest scoring preprocessor (mandatory before any Dr is quoted)
Raw .tex scoring is INVALID if tables or build comments are counted as
prose. Before `score`:
- **T-3.1** recursively inline every `\input{...}` (the manuscript's prose
  usually lives in section files, not the main tex);
- **T-3.2** strip comments, then `deluxetable`/`tabular`/`table`/`figure`/
  `align`/`equation`/`math`/`verbatim`/`thebibliography` environments whole;
- **T-3.3** strip macros/braces/math, then score. Symptom of skipping this
  (observed): Ssd/comma-rate/Sshort inflated ~5× by deluxetable numerals, Dr
  2.60 → 1.22 after stripping. Reference implementation:
  `deai_voice.py` + the census/technosignature strip scripts.

### T-4 LLM-tell census and adjudicated edits
- **T-4.1** Run `--tells` on the preprocessed prose. Census first, edits
  second; record before/after rates per tell in the comparison document.
- **T-4.2** Each tell instance is adjudicated on the RV-01 ladder, in
  priority order: cut inferable tail → ", not X" apposition → "instead of"
  (verb-phrase contrasts) → split clause → rewrite sentence. Deployed
  examples: "rather than" 43→3 (census) and 76→8 (technosignatures) with
  every kept instance carrying a written keep-reason (content-bearing
  contrast, documented caption wording, table terminology).
- **T-4.3** "not only" → "not just"/"not merely"/"not solely" per sense;
  watch for tell substrings surviving inside the fix (caught: "in full, not
  in summary" still matched "in summary").
- **T-4.4** Batch mechanics (trap #S40 discipline): every edit pattern must
  match its predicted occurrence count exactly or the batch aborts writing
  nothing; word-count tripwire per batch (predicted delta = edit arithmetic,
  e.g. "rather than"→", not" = −1 word each); paragraph-initial-lowercase
  scan diffed against the pre-batch snapshot; numeric AND citation multiset
  deltas vs the untouched original = NONE after every batch; compile gate
  (0 errors) after every batch.

### T-5 Build-tree acquisition (manuscripts assembled elsewhere)
- **T-5.1** If the manuscript folder lacks its class/inputs, fetch them from
  the canonical repo at the EXACT version tag; byte-compare the class file
  against any local copy; baseline compile (0 errors) BEFORE any edit.
- **T-5.2** Standalone deliverable: recursively inline all `\input`s into
  one .tex with `%% ==== inlined from ... ====` banners; bibliography must
  be inline (`thebibliography` or inlined .bbl — no .bib/bibtex dependency);
  verify identical page count and warning profile vs the fragment build.
  The document class file remains an unavoidable external (LaTeX loads
  `\documentclass` from disk).
- **T-5.3** Macro-de-expansion (numbers as literals) is offered but OFF by
  default: it breaks single-source sync and macro-keyed selftests. Only for
  final submission snapshots, on explicit author request.
- **T-5.4** A macro/`\newcommand`-dense source is build engineering
  (single-source numbers, machine-checkable gates), NOT by itself an
  AI-prose tell: DEAI scores the rendered text, never the macro layer.

### T-6 Deliverables (extend §9)
In addition to the §9 outputs, a voice-model revision leaves:
6. `deai_voice_comparison.md` — original-vs-revised table: per-tell rates
   before/after with edit counts, Dr before/after, author holdout band,
   control band, residuals with keep-reasons, honest verdict (what the edits
   did and did not achieve; §R wording rules apply — no watermark claims).
7. The preprocessed-prose dump used for scoring and the strip script, so a
   fresh agent can re-derive every number in the comparison.

### T-7 Non-duplication note
V-04 (style distance) is measured by §S/B-37 via the §T-3 preprocessor —
the free-text Burrows' Delta note in V-04 is superseded by this workflow.
B-38 (changed vs unchanged sentence distance) is computed on the same
preprocessed corpus. T-4.4 batch mechanics restate I-2/I-4 and trap #S40 in
operational form; they do not add gates.
