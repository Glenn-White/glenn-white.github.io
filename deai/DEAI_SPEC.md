# DEAI Specification — 3D Filament Letter (Is the filament width–distance relation physical?)

**Full executable spec for the de-AI protocol pass on this paper, for an AGI
agent running a similar ASTRA installation on another machine.**

- Canonical protocol (authoritative, read these first from your local
  `astra_core/deai/`): `DEAI_PAPER_PROTOCOL.md` (v3.0 body, Sections 0–10)
  and `DEAI_v3_ADDENDUM.md` (§A–§T; **the addendum wins on any conflict**).
  This file is the project-specific operating order; it does not replace the
  protocol, it instantiates it.
- Reference implementation: `astra_core/deai/deai_battery.py` (Section 5.13
  battery), `deai_voice.py` (§S/§T voice model), `adversarial/` fixtures.
- **Trigger discipline:** run ONLY on explicit author request, near paper
  end. One full run; never silently re-run.

---

## 0. The paper and its standing rules

- **Manuscript:** MNRAS Letter, `mnras.cls`, two-column, **hard limit 5 pages
  including references, appendices, everything**. Current version at the time
  this spec was written: `paper/v1.9/paper_v1_9.tex` — **always operate on
  the latest complete version directory; confirm with the author which
  version if ambiguous.**
- Source tree per version dir: `paper_vX.Y/paper_vX_Y.tex`, `figures/`,
  `paper_vX_Y.bib` (or inline bibliography — check). Compile:
  `pdflatex` + `bibtex` ×2; gate = 0 errors, 0 undefined
  citations/references, ≤ 5 pages, readable `.pdf` left behind.
- **Versioning (inviolable):** bump the version stamp FIRST (create
  `paper/v(X+1).0/` or next minor, copy the tree, edit only the copy).
  NEVER rename, delete, or overwrite a prior version's tex/pdf/scripts.
- **No referee response letters, ever** (standing directive). Referee-style
  findings go into `deai_referee_report.md` / `deai_author_decisions.md`.
- **No [[TBD]] markers may remain** in the section you process; if any are
  found, STOP and report to the author instead of guessing content (I-5).
- Author: G. J. White (ORCID 0000-0002-7126-691X) — check it appears in the
  title block correctly.
- British spelling (MNRAS); `per cent` not `%` in running text; MNRAS house
  style (Sect. 3, Fig. 2, equation (4)).

## 0.1 Project-specific protected terms (never flag/replace; extend per §2.5)

- Statistical/technical: *robust* (regression context), *significant*
  (attached to a test), *beam* terms (common beam, effective beam,
  beam-deconvolved, beam-locked, beam lock — the paper's central concept),
  *resolution ladder*, *width–distance relation*, *contrast-based selection*.
- Objects/surveys/tools: HGBS, Hi-GAL, TMC 1, Serpens, Aquila, Perseus,
  Orion A, Orion B, IC 5146, Polaris, fil_finder, DisPerSE, Edenhofer map.
- Numbers discipline is severe in this paper: medians, n counts, α values,
  beam values (0.026/0.040/0.070 pc) appear in Abstract, body, Conclusions
  and the appendix table. All are protected tokens (I-1).

---

## 1. Stage 0 — preparation (do in this order)

1. Confirm target version with the author; create the next version
   directory; bump the version stamp inside the tex FIRST. Copy, never move.
2. Baseline compile of the untouched copy: 0 errors, ≤ 5 pages. Record the
   page count and warning profile — the revised paper must not exceed it.
3. Read the rendered `.pdf` end-to-end as a reader; write the stumble log
   (RT-02). Identify the one memorable result.
4. Parse/segment the tex (Section 2.3): section/paragraph/sentence, mask
   math/citations/labels/figure+table environments, classify sections.
   **Run the SG checks first** (SG-01 abbreviation list; SG-02 print 50
   random sentences, ≤ 2 boundary errors, else fix the splitter before any
   sentence metric is trusted).
5. Build the protected-token register (every number+unit+uncertainty,
   symbol, equation, object/catalogue ID, citation key, fig/table ref,
   acronym, with location). This drives T-01.
6. Apply the protected-terms list (§0.1 above + §2.5 of the protocol).
7. Baselines: no discipline corpus is expected on the other machine — use
   the provisional thresholds and mark every flag **uncalibrated**. If the
   author's prior-paper corpus exists locally (`DEAI_files/voice_corpus/`),
   the §T voice workflow applies (see §5 below); otherwise B-37/B-38 are
   NOT-RUN with that reason recorded.

## 2. Diagnostics before edits (execution contract, binding)

Run, in order, and write `deai_battery.md` (before-values) BEFORE any edit:

1. `python3 astra_core/deai/deai_battery.py <target.tex>` → before-table.
2. Stage 1 scientific integrity audit: main-finding sentence (3.1 — one
   sentence, one number, one decisive observation; store it for T-06);
   argument graph + F-NOFUNC (3.2); E-01…E-20; epistemic ladder (3.4);
   N-01…N-07 numerical consistency (abstract vs body vs table vs captions —
   this paper quotes the same medians in four places); astronomy-specific
   correctness (3.6).
3. Stage 2 citation audit: R-01 resolve every .bib entry against ADS
   (unresolvable = severity 1, never guess-repair); R-02 claim–source
   alignment; R-03…R-11.
4. Addendum checks: §E coined-terminology register (CT-01…CT-06; expect
   candidates like "beam lock", "resolution ladder" — check ADS usage,
   keep with a written keep-reason if they are this paper's precise
   terms); §F title/keywords/headings; §G LaTeX/PDF/file hygiene
   (LX-01 strip comments, grep for model/agent/version/TODO mentions;
   LX-07 PDF metadata); §H figures/tables/equations/acronyms (FG-01:
   every number quoted from Fig. 2/3/A1 must match the plotted data files
   in `../../results/` — else NOT VERIFIABLE); §I house style + statements;
   §J literature (LT-01 24-month ADS sweep; OV-01 overlap); §K reader
   tests RT-01…RT-06.
5. **Adversarial fixtures:** run `astra_core/deai/adversarial/` (AD-1..AD-10)
   and confirm all pass BEFORE the revision pass. A fixture failure stops
   the run.
6. Write `deai_audit_report.md` with the full before-table, Stage 1–2
   findings with severity, and the §N execution manifest skeleton.

## 3. Revision pass (Stage 4, addendum §D ordering)

- **Default to preserve** (RV-01): delete > cut clause > reorder > replace
  word > rewrite sentence > rewrite paragraph. Every edit needs a defect ID
  and an improvement reason, logged in `deai_change_log.md`
  (old → new, feature/defect ID, justification, approval status).
- Order: science-wording defects → structure (only if the main-finding
  test failed) → paragraphs (F-NOFUNC, closing glosses G-03) → sentences →
  words. Construction-level before word-level (execution contract #5).
- **Invariants I-1…I-7 hold absolutely.** Note I-1 as amended by §B
  (protects the quantity, not the printed string; precision harmonisation
  allowed with equivalence check + change-log entry; changed measured
  values need author approval).
- **§C semantic check** on every scientifically meaningful changed sentence
  (denominators, quantifiers, conditions, causality, limits, O/I/C status).
- **§M separation:** statistical/provenance/reproducibility findings go to
  `deai_referee_report.md` + `deai_author_decisions.md`; NEVER fix a science
  defect by rewording.
- **Batch mechanics (T-4.4, trap #S40):** scripted edit patterns must match
  predicted occurrence counts exactly or abort writing nothing; word-count
  tripwire per batch; numeric AND citation multiset deltas vs the original
  = NONE after every batch; compile gate after every batch.
- **Edit budget B-33:** > 40% of body sentences changed in any section →
  stop and report to the author.
- **Page budget:** the Letter must stay ≤ 5 pages. Deleting is preferred to
  rewriting (W-02); if a fix would add length, find an equal cut.
- Watch for this paper's known exposures (§5.12 pipeline habits):
  contrastive reframes ("not X but Y" style), short dramatic closers,
  trailing ", suggesting" clauses, over-compressed noun phrases holding
  several numbers (width/beam values), numbers drifting between sections,
  defensive process narration in the main text (move to appendix if it is
  not already there).

## 4. Convergence loop

Re-run the battery with the ORIGINAL tex as second argument
(`deai_battery.py <edited.tex> <original.tex>`) so B-26 is a measured delta.
Every row: before, after, verdict (fixed / in-range / kept-with-reason /
waived-with-reason / NOT-RUN-with-reason). A row may never be blank.
Resolve out-of-range rows by fix or quoted waiver (I-7: never make the text
worse to move a metric). Re-measure replacement constructions after any
dominant-feature removal (relocation guard). **Class A rows must PASS;
Class B rows end resolved-or-adjudicated** (§A). Max three cycles; then hand
residuals to the author.

## 5. Voice model (§S/§T) — conditional

- If the author-paper corpus exists: preprocess per §T-3 (inline `\input`s,
  strip tables/comments/environments/math — raw-tex scoring is INVALID),
  `build` + `validate`. Unless validation separates holdouts from controls
  (S-01 PASS), voice rows are REPORT-ONLY.
- §T-4 LLM-tell census ("rather than", "not only", etc.): census first,
  adjudicate each instance on the RV-01 ladder, keep-reasons for every kept
  instance, record before/after rates.
- If no corpus: B-37/B-38 = NOT-RUN, reason recorded in the manifest.

## 6. Verification gates (fresh agent context, not the reviser)

Run T-00 first (battery table complete with before AND after). Then T-01…T-13
plus T-14…T-22 (addendum): protected-token diff empty; proposition map;
epistemic ladder never climbed; N-checks; citations; clean compile ≤ 5 pages;
T-06 fresh-agent main-finding test vs the stored 3.1 sentence; hard-zero
features zero; no C-01 window; over-correction absent; adversarial fixtures;
coined-term register; hygiene/figure/table/statement checks; LT-01 list
delivered; overlap; four simulated referees (§K SR-1..4: subfield expert,
statistician, desk editor, sceptic) answered or escalated; B-29/B-33 pass.
Manifest (§N) rows carry status words — never 0–100 scores, never an
"AI probability", never any watermark claim (§R).

## 7. Outputs (into the NEW version directory)

1. Revised `paper_vX_Y.tex` + fresh `.pdf` (0 errors, ≤ 5 pages).
2. `deai_change_log.md` 3. `deai_audit_report.md` (with merged before/after
   battery table verbatim) 4. `deai_author_decisions.md`
5. `deai_invariant_check.md` 6. `deai_referee_report.md` (§M findings)
7. `deai_battery.md` (after-pass) 8. `deai_voice_comparison.md` (if §5 ran)
9. The execution manifest (§N) as `deai_manifest.md`.

End of run: report to the author — what was fixed, what was waived with
reasons, what needs author decisions (especially any severity-1 item, which
blocks submission until resolved), and the honest verdict (no watermark
language, §R).
