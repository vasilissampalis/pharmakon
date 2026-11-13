# Batch 3c second reading (2026-10-17): McKetin 2020 and the Ersche 2012 supplement

You are an independent second reader (AI reader 33) for Pharmakon's methamphetamine page. The first reader (AI reader 29) read two PDFs in full: McKetin et al. (2020), a within-person analysis of methamphetamine use and crime in an Australian cohort, and the Supporting Online Material of Ersche et al. (2012), on brain structure in people dependent on stimulants and their siblings. Reader 29 wrote a new card (`sc_mcketin_2020`), rewrote `sc_ersche_2012` from the supplement, added 7 anchors to two claims and changed them, and drafted wording for a new claim on crime. You did not write any of this. Check it against the sources. The source decides.

Read first, in `/home/claude/drug-encyclopedia`: `docs/VERIFICATION-BRIEF.md` ("Step 2", "Output", "Rules (hard)", "Targeted checks"; skip Step 1); `docs/METHODS.md` §5, §6 and §9 as needed; reader 29's report, `data/verification/batch3c-2026-10-17/reader29_report.md`.

## Sources
`/mnt/user-data/uploads/DrugEncyclopedia/PDFs/Methamphetamine/McKetin_2020_ContributionMethamphetamineUseCrime.pdf` (6 pages), `Ersche_2012_Supplement.pdf` (12 pages) and, for the claim's other anchors, `Ersche_2012_AbnormalBrainStructureSiblings.pdf` (a cover page, then pp. 601–604). Extract text with `pdftotext -layout` into `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/batch3c/reader33/`; render pages with `pdftoppm -r 110` for tables and figures. No browser is needed.

## Task 1: the anchors
`data/verification/targeted-2026-10-17i/tasks.json` lists the 7 new anchors. Check each at the stated page and locator ("Targeted checks"): `confirmed`, `corrected` (the corrected page, locator or extracted text in your own words, numbers exact), `wrong-location` or `not-found`; check every number, the role and any quotation. Write `data/verification/targeted-2026-10-17i/out_reader33.json` in the format of `data/verification/targeted-2026-10-17g/out_reader21.json`.

## Task 2: the cards
`sc_mcketin_2020` and `sc_ersche_2012` are in `data/study-cards/methamphetamine.json` (first-pass). Do "Step 2" for each: every key finding and reporting issue `confirmed` / `corrected` / `wrong-location` / `not-found`; the design, the risk-of-bias instrument, every domain and the overall; the interpretation-gap assessment; what the card missed. For Ersche, check every logged change against the supplement and the main article. Write `data/verification/cardcheck-2026-10-17e/out/<reference>.json`.

## Task 3: the claims
Read `cl_meth_violence` and `cl_meth_siblings` in `data/claims/methamphetamine.json` as they now stand (with today's changelog entries), and reader 29's proposed crime claim in the report. Give your view on wording (no more than the sources show), status label, relation, GRADE and verification step, and on these questions:
- `cl_meth_violence`: reader 29 proposes relation "insufficient evidence" → "is associated with" and status "mixed" → "replicated by the same team" (two longitudinal cohorts with adjusted associations, which share three authors; the MATES cohort is already inside the review's pooled estimate, whose adjusted range includes no association). Which relation and status fit? The report also gives an alternative that keeps the relation.
- The crime claim: is a separate claim justified, and is the proposed wording exact?
- `cl_meth_siblings`: is withdrawing "fits an additional effect of use" right (years of use appear only as maps)?
Write `data/verification/cardcheck-2026-10-17e/claims_reader33.json` in the format of `data/verification/cardcheck-2026-10-17c/claims_reader21.json` (add an entry `"claim_id": "new: crime"` for the proposed claim).

## Rules
The hard rules of `docs/VERIFICATION-BRIEF.md` apply: quotations at most 15 words, at most one per claim; person-first language; no dosing or administration guidance. Do not edit any project file other than your own output files. Validate each JSON file. If an automatic safety filter stops one of your responses, do not retry or reword that content: save what is done and say what was not done. Final report, under 250 words: anchors not confirmed, card findings corrected, risk-of-bias disagreements, and your view on each question.
