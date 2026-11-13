# Drug checking: the supplements (AI readers 150, 151 and 152), 27 October 2026

You are an independent reader and adjudicator for Pharmakon, an evidence library about drugs for the public and for
people who use drugs. Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/` (`scratchpad/` below); your own
folder is `scratchpad/ux1026/suppl/r<N>/`.

The drug-checking answers ("Do home test kits work?", 19 claims in `data/claims/drug-checking.json`, 21 cards in
`data/study-cards/drug-checking.json`) went through first reading, blind second reading and adjudication on 26 and 27
October. Three sources had supplementary files that nobody had read; the cards and claims say so ("not read"). The senior
author has now saved them. You read one source's supplement, with its paper, and bring the card and the claims up to
date: **the source decides**. You did not write these cards or claims and took no part in the earlier rounds.

## Read first

1. `docs/METHODS.md` version 0.3.1: §4.5, §5.3–5.6, §6 (all of it), §7, §8 (section 11), §9, §12.
2. `docs/WRITING-RULES.md`: Rule 0, Rule 0b, "One page, three depths", "The answer format", "Sentence rules".
3. `docs/REVIEW-BRIEF-2.md`, "What to check, claim by claim" (A to F).
4. `docs/ADJUDICATION-BRIEF.md` Part B (how to correct a card and log it).
5. `scripts/claim_patch.py` (its docstring): your patch format.
6. `data/verification/dc-2026-10-26/adjudication/148_log.json` and `149_log.json`: what the adjudicators decided and
   left open (search them for your source).

## Your source

| Reader | Supplement (senior author's folder `/mnt/user-data/uploads/DrugEncyclopedia/`) | Text (in `scratchpad/ux1026/suppl/`) | Paper read with it | Card | Claims that cite the source |
|---|---|---|---|---|---|
| 150 | `PDFs/_Cross-cutting/Bhai_2025_AppendixA.docx` (Online Appendix A, "The Coding of Fentanyl Test Strip Legalization", added by the 2026 corrigendum) | `Bhai_2025_AppendixA.txt` | `PDFs/_Cross-cutting/Bhai_2025_FTSDrugMortality.pdf` and `PDFs/_Cross-cutting/Bhai_2026_Corrigendum..pdf` | `sc_bhai_2025` | `cl_dc_law_deaths` (8 anchors) |
| 151 | `PDFs/_Cross-cutting/Kutscher_2024_Appendix1.docx` (complete reference list, 1–95) and `Kutscher_2024_Suppl1.docx`, `Suppl2.docx`, `Suppl3.docx` (Supplemental Tables 1–3: uptake, satisfaction, behaviour change) | `Kutscher_2024_Appendix1.txt`, `Kutscher_2024_Suppl1.txt` to `Suppl3.txt` | `PDFs/_Cross-cutting/Kutscher_2024_FTSScopingReview.pdf` (author manuscript; "AM p. N" = PDF page) | `sc_kutscher_2024` | 15 anchors in 12 claims (find them by `"reference": "kutscher_2024"`) |
| 152 | `PDFs/_Cross-cutting/VickersSmith_2025_Supplement.pdf` (22 pages: eMethods, eTables 1–5, eFigures 1–5) | `VickersSmith_2025_Supplement.txt` (layout) and `.plain.txt`, pages separated by form feeds | the paper itself is a web source (JAMA Network Open, open access): the second reader's saved text `scratchpad/ux1026/dc/s147/vickers_smith_2025_page1.txt`, `scratchpad/vickers_page.txt` and the notes in `scratchpad/ux1026/dc/s147/` | `sc_vickers_smith_2025` | 8 anchors in 4 claims (`"reference": "vickers-smith_2025"`) |

Text extractions of the papers (pages separated by form feeds; printed page = the article's first page + index) are in
`scratchpad/ux1026/dc/numtext/`. Render a page or a figure with `pdftoppm` and look at it when a table or figure matters.
A .docx can be checked against its text with `pandoc -t plain`.

Points already known to matter (check them; do not take them from here):
- **150.** The card and claim say the authors' changes to the legal dates are documented only in an appendix "not read",
  and that six states shaded legal on the paper's map (Alaska, Massachusetts, Michigan, New York, Vermont, Wyoming) have
  no date in Table 1 and no stated coding. Say what the appendix documents, whether its dates agree with Table 1, what it
  leaves undocumented, what kind of evidence the coding choices rest on and from when, and whether any analysis with the
  source database's own dates is reported. Then decide whether the ROBINS-I judgment for classification of interventions
  (and the overall judgment) stands, with reasons; the card marks it provisional until the appendix is read.
- **151.** The manuscript prints references 1–50 only, so figures cited to references 51–95 could not be traced (for
  example the overdose odds ratios, ref. 69; the Rhode Island cohort, ref. 70; the five-fold higher positivity at home,
  ref. 66). Identify each such figure our claims use and its primary study. Several are studies the claims also cite
  directly (Krieger 2018, Karamouzian 2018, Klaire 2022; check others): apply METHODS §6.4 (overlapping studies counted
  once) to the status flags and to any count of studies. Check every range or count our claims take from the review
  against Supplemental Tables 1–3, and what each table actually measures (for example, Table 1's "uptake" column is built
  from reported prior use of strips). Note duplicate entries in the complete reference list if they affect a count.
- **152.** The card was built from the web article; check its design, exposure and outcome measurement, follow-up,
  missing data, models, covariates and risk-of-bias notes against the eMethods, eTables and eFigures (eFigure 4: daily
  share reporting a nonfatal overdose; eFigure 5: modification by age). Say whether any claim's number or wording needs
  a qualifier or is contradicted.

## What to do

1. **Card.** Start from the current card in `data/study-cards/drug-checking.json` (print it by id; never edit that
   file). Replace every "not read" statement about your supplement with what it says, correct what the supplement shows
   to be wrong, add what matters, and keep everything else. Write the card in full to
   `data/study-cards/_incoming/drug-checking/<card id>.json`; log every change in `verification.disagreements` (what the
   card said, what the supplement shows, where); add the supplement to the card's source-read description; set
   `verification.checked_by` to the card's current value followed by "; supplement read by AI reader <N> (27 October
   2026)" and `checked_on` to today; keep `verification.status` `ai-checked` only if no risk-of-bias judgment changed,
   otherwise set it to `first-pass` and say why in your log. Run `python3 -I scripts/check_card.py <file>` until it
   passes.
2. **Claims.** Review each claim that cites your source (REVIEW-BRIEF-2 A to F), as far as the supplement bears on it:
   numbers against anchors and sources; wording against the design (laboratory results never as real-life accuracy;
   intended or self-reported behaviour never as observed behaviour; association never as effect; one brand, lot,
   festival, programme or state never as all); GRADE and status flags (§6.3, §6.4). Write the claim patch
   (`claim_patch.py` format, one object per claim you change, with a `change` line beginning "Supplement reading, 27
   October 2026:"). Every number you put into a claim must be in an anchor's `extracted` text or be an editors'
   calculation you have recomputed. A needed number or fact that no anchor carries goes in a new anchor (`evidence_add`):
   `reference` the paper's id (`bhai_2025`, `kutscher_2024` or `vickers-smith_2025`), `study_card` its card, `page` and
   `locator` per §6.2 and the precedents below, `role`, `located_by` "AI reader <N> (supplement reader)", `located_on`
   today, and `source_read` naming the file. Precedents: a Word supplement, page "Supplementary material 1 (DOCX),
   Supplemental Table 1", source_read "DOCX PDFs/Cannabis/Callaghan_2013_Supplement.docx"; a PDF supplement, page
   "supplement p. 16" (PDF page), locator "eTable 4 (PDFs/…)", source_read "PDF supplement (PDFs/…pdf)". New anchors
   enter as ai-located; another reader checks them next (say so in your log). Change an existing anchor only to correct
   it, and log why. Check with `python3 -I scripts/claim_patch.py <your patch> --dry-run` until it passes.
3. **Plain lines.** For every claim you change, write its plain lines as they should read after your patch, starting
   from the current ones in `data/site/simple.json` (`claims.<id>`: `short`, `but`, `how` 2 to 4 points, `freq` if
   present): reading age 8 to 11; `short` about 14 words; `but` the main limit; name the comparison group; never more
   than the claim says; numbers as counts out of 100 (or 1,000 for rare things). Leave out `v`; the editor sets it.
4. **For the senior author**: anything that is a judgment for him (a change of certainty, a debate, a domain-level
   disagreement with the earlier readers) goes in your log under `for_senior_author`.

## Output (in `data/verification/suppl-2026-10-27/`)

- `<N>_log.json`: `{"reader": "AI reader <N> (supplement reader)", "date": "2026-10-27", "source": "<reference id>",
  "items": [{"claim_id" or "card", "finding": "...", "verdict": "changed | confirmed | for senior author", "reason":
  "what you checked and found", "evidence": "file, table or page", "patch_ref": "index in your patch or null"}],
  "new_anchors": [{"claim_id", "evidence_index_after_patch", "page", "locator"}], "for_senior_author": ["..."]}`
- `<N>_patch.json` (an empty list if no claim changes), `<N>_simple.json` (`{}` if none).
- The corrected card in `data/study-cards/_incoming/drug-checking/`.

## Rules (hard)

- Never edit `data/claims/`, `data/study-cards/drug-checking.json`, `data/site/`, `docs/`, `scripts/` or `site/`: you
  write proposals and corrected copies; the editor applies them.
- Browser: 150 and 151 do not need it. 152 may open the article itself if the saved texts cannot settle a point: the
  app's built-in browser tools (load them with ToolSearch, query `mcp__remote-devices__Claude_Browser__`), one tab of
  your own made with `preview_start` at https://pmc.ncbi.nlm.nih.gov/articles/PMC12076174/, its tabId on every call,
  `get_page_text` to read; never touch any other tab, never open a PDF or download link, never a check page; close your
  tab when done. If the browser cannot be reached, settle the point from the saved texts or leave it open in your log.
- No dosing, administration or potentiation guidance; no instructions on how to test; findings only. Person-first words;
  no words of alarm or reassurance. Quotations at most 15 words, at most one per claim, word for word.
- Final message under 200 words: what the supplement settled; claims changed (certainty or status changes: from → to,
  rule); new anchors; card changes and status; what the senior author must decide.
