# MDMA batch 2 second reading (2026-10-17): the MDMA-assisted therapy trials, anchors, cards and claims

You are an independent second reader for Pharmakon's MDMA page. Two first readers (AI readers 27 and 28) read the two phase 3 trials of MDMA-assisted therapy for PTSD (MAPP1, MAPP2, with their registry records and MAPP2's correction), a systematic review, two critiques and a reply, two commentaries, a qualitative study, a cost-effectiveness critique, a BMJ news report and three retraction notices, and wrote one study card each; the editor joined their claims into six. You did not write any of this work. Check it against the sources. The source decides; no reader is presumed right.

Read first, in `/home/claude/drug-encyclopedia`: `docs/VERIFICATION-BRIEF.md` ("Step 2", "Output", "Rules (hard)", "Targeted checks"; skip Step 1); `docs/METHODS.md` §5, §6, §7 and §9 as needed; the first readers' reports, `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/mdma2/reader27_report.md` and `reader28_report.md`.

## Sources
PDFs in `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/MDMA/` (file names in each card's `verification.source_read`); extract text with `pdftotext -layout` into `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/mdma2/<your reader name>/` and render pages with `pdftoppm -r 110` for tables. Web sources (the two trials at nature.com, their ClinicalTrials.gov records, MAPP2's correction, and the three retraction notices at link.springer.com): read them in the desktop app's browser, in a tab you open yourself (the `mcp__remote-devices__Claude_Browser__*` tools; load them with ToolSearch, query "mcp__remote-devices__Claude_Browser__", max_results 64). Never touch, read or close any other tab; close yours when you finish. Never open a PDF link in the browser (the trials' supplements are PDFs: they are not part of this check).

## Assignment
- **AI reader 34**: mitchell_2021, mitchell_2023, brett_2025, halvorsen_2021, mitchell_2021b (reader 27's cards).
- **AI reader 35**: nutt_2021, madero_2023, earleywine_2025, marseille_2025, mahase_2024, feduccia_2024, jerome_2024, mithoefer_2024 (reader 28's cards).

## Task 1: the anchors
`data/verification/targeted-2026-10-17j/tasks.json` lists the 102 anchors; check those whose `checker` is you, one by one, at the stated page and locator: `confirmed`, `corrected` (the corrected page, locator or extracted text in your own words, numbers exact), `wrong-location` (give the right place) or `not-found`; check every number, the role against the claim's statement, and any quotation (verbatim, at most 15 words). Write `data/verification/targeted-2026-10-17j/out_<your reader name>.json` in the format of `data/verification/targeted-2026-10-17h/out_reader31.json`.

## Task 2: the cards
The cards are in `data/study-cards/_incoming/mdma/sc_<reference>.json` (first-pass). For each of yours, do "Step 2": every key finding and every reporting issue `confirmed` / `corrected` / `wrong-location` / `not-found`; the design label, the risk-of-bias instrument, every domain and the overall; the interpretation-gap assessment; what the card missed that matters. Write `data/verification/cardcheck-2026-10-17f/out/<reference>.json`.

## Task 3: the claims
The joined claims are in `data/claims/_incoming/mdma2_joined.json`. For every claim citing your papers, read it whole and give your view on wording (no more than the sources show; name each sentence that says more), status label, relation, GRADE (each domain and the certainty) and verification step, and on the debate box of `cl_mdma_therapy_contested`. Questions from the first readers and the editor:
- `cl_mdma_ptsd_efficacy`: reader 27 rates certainty moderate (low on a strict reading), down one level for risk of bias. Most participants could tell their group, expectancy was not measured, the outcome rests on participants' reports, and both trials share one sponsor: is one level enough, and is "reduces" the right relation?
- `cl_mdma_ptsd_adverse_events`: moderate certainty for the increase in common adverse events, while the recording methods (expected effects not recorded; site staff collecting events) are limits: fair?
- `cl_mdma_regulatory_2024`: the editor set metadata-verified because the retraction facts rest on the notices; the FDA part rests on a news report. Is that right, and is anything said beyond the sources?
- `cl_mdma_ptsd_cost`: draft, resting on a critique and a commentary; is the wording exact?
Write `data/verification/cardcheck-2026-10-17f/claims_<your reader name>.json` in the format of `data/verification/cardcheck-2026-10-17d/claims_reader31.json`.

## Rules
The hard rules of `docs/VERIFICATION-BRIEF.md` apply. Quotations at most 15 words; person-first language; no dosing, administration or potentiation guidance (the trials' doses only as study conditions, on the cards). Never download files, never open PDF links in the browser, never use shadow libraries, never attempt a CAPTCHA or bot check. Do not edit any project file other than your own output files; validate each JSON file. If an automatic safety filter stops one of your responses, do not retry or reword that content: save what is done and say what was not done. Write files as you go. Final report, under 250 words: anchors not confirmed (with the correction), card findings corrected, risk-of-bias disagreements, and your view on each claim question.
