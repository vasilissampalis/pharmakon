# MDMA batch 1 second reading (2026-10-17): anchors at the stated place, cards, and the claims

You are an independent second reader for Pharmakon's MDMA page (the second drug page; methamphetamine is the model). Two first readers (AI readers 24 and 25) read eleven papers in full and wrote one study card each; the editor joined their work into nine claims, placing anchors from reader 24's cards. You did not write any of this work. Your job is to check it against the sources. The source decides; no reader is presumed right.

Read first, in `/home/claude/drug-encyclopedia`:
- `docs/VERIFICATION-BRIEF.md`: "Step 2" (card check), "Output", "Rules (hard)", "Targeted checks". Skip Step 1 (no blind extraction this round).
- `docs/METHODS.md` §5 (study cards, risk of bias), §6 (claims, status labels, GRADE), §7 (contested questions) and §9 (language), as needed.
- The first readers' reports: `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/mdma1/reader25_report.md` (reader 24 wrote no report; its final notes are in this brief's last section).

## Sources
PDFs: `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/MDMA/` (file names in each card's `verification.source_read`). Extract text with `pdftotext -layout` into your own folder `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/mdma1/<your reader name>/`, and render pages with `pdftoppm -r 110` for tables. Page conventions: Parrott 2013 is an in-press proof numbered 1 to 19 (anchors say "of the in-press PDF"); Barnett 2021 is an online-first PDF (pages counted from its first page, "of the online-first PDF"); Ung 2026 and the others use their printed page numbers. Web sources: Halpern 2011 (PubMed Central, PMC3053129), Lyvers 2011 (publisher HTML, https://doi.org/10.1111/j.1360-0443.2010.03344.x) and Cowan 2012 (PubMed Central, PMC3280662): read them in the desktop app's browser, in a tab you open yourself (the `mcp__remote-devices__Claude_Browser__*` tools; load them with ToolSearch, query "mcp__remote-devices__Claude_Browser__", max_results 64). Never touch, read or close any other tab, and close yours when you finish.

## Assignment
- **AI reader 31**: mccann_1994, schilt_2007, halpern_2011, ung_2026, murphy_2009 (reader 24's cards).
- **AI reader 32**: parrott_2013, parrott_2011, lyvers_2011, cowan_2012, mithoefer_2003, barnett_2021 (reader 25's cards).

## Task 1: the anchors
`data/verification/targeted-2026-10-17h/tasks.json` lists the 88 anchors; check those whose `checker` is you, one by one, at the stated page and locator, as "Targeted checks" says: `confirmed`, `corrected` (the corrected page, locator or extracted text in your own words, numbers exact), `wrong-location` (give the right place) or `not-found`. Check every number, the role (supports, qualifies, contradicts) against the claim's statement, and any quotation (verbatim, at most 15 words). Write `data/verification/targeted-2026-10-17h/out_<your reader name>.json`:
```json
{"reader": "AI reader 31 (targeted check at the stated place)", "date": "2026-10-17",
 "results": [{"n": 1, "claim_id": "…", "anchor_index": 0, "verdict": "confirmed", "corrected": {}, "note": "what you compared"}]}
```
`corrected` holds only the fields you would change (`page`, `locator`, `extracted`, `role`, `quote`).

## Task 2: the cards
The cards are in `data/study-cards/_incoming/mdma/sc_<reference>.json` (first-pass). For each of yours, do "Step 2" of the verification brief: every key finding and every reporting issue `confirmed` / `corrected` / `wrong-location` / `not-found`; agree or disagree with the design label, the risk-of-bias instrument, every domain and the overall judgment, and the interpretation-gap assessment; list what the card missed that matters. Write one file per paper, `data/verification/cardcheck-2026-10-17d/out/<reference>.json`, in the format "Output" gives.

## Task 3: the claims
The joined claims are in `data/claims/_incoming/mdma_joined.json` (nine claims; ids cl_mdma_*). For every claim that cites your papers, read it whole (statement, plain, magnitude, grade with its reasons, status, verification, debate box where there is one) and give your view on:
1. **Wording**: do the statement, plain text and magnitude say exactly what your sources show, no more? Name every sentence that does not.
2. **Status label** (METHODS §6.4): replicated, replicated by the same team, single study, mixed or contested.
3. **GRADE**: each domain and the overall certainty.
4. **Verification step**: draft or metadata-verified (a claim resting only on narrative reviews or commentaries stays draft).
5. **The debate boxes** (`cl_mdma_dopamine_human`, `cl_mdma_neurotoxicity_contested`): is each side's strongest evidence fairly stated from your sources, and is anything in the editors' reading unsupported?
Questions from the first readers and the editor: reader 24 classed Murphy 2009 as a systematic review (AMSTAR 2) following the `sc_lappin_2017` precedent; is that right, or is it a narrative review? Halpern 2011 says a medium effect could be excluded on "many" measures; the claim says 6 of 14: check Table 4.

Write `data/verification/cardcheck-2026-10-17d/claims_<your reader name>.json`:
```json
[{"claim_id": "…", "wording": {"verdict": "agree|disagree", "proposed": "…", "reason": "…"},
  "status": {"verdict": "agree|disagree", "proposed": "…", "reason": "…"},
  "grade": {"verdict": "agree|disagree", "proposed": "…", "reason": "…"},
  "verification": {"verdict": "agree|disagree", "reason": "…"},
  "debate": {"verdict": "agree|disagree|n/a", "reason": "…"},
  "note": "…"}]
```

## Rules
- The hard rules of `docs/VERIFICATION-BRIEF.md` apply. Quotations at most 15 words; person-first language; no dosing, administration or potentiation guidance (amounts of use only as study conditions).
- Never download files, never open PDF links in the browser, never use shadow libraries, never attempt a CAPTCHA or bot check.
- Do not edit any project file other than your own output files named above. Validate each JSON file with `python3 -c "import json,sys; json.load(open(sys.argv[1]))" <file>`.
- If an automatic safety filter stops one of your responses, do not retry or reword that content: save what is done and say in your report what was not done.
- Write files as you go.
- Final report, under 250 words: anchors not confirmed (with the correction), card findings corrected or not found, risk-of-bias disagreements, and your view on each claim question where you disagree.

## Reader 24's final notes (the first reader of the primary studies)
McCann: the Discussion says the groups were matched for education and other drug use, which Tables 1 and 3 contradict (cocaine 80% vs 29%, no adjustment); the 5-HIAA difference is clear only in women; the usual-amount row is misprinted; alienation is printed as F = 4.4, p = .004 (should be about .04). Ung: the abstract states a longer-abstinence result the Results say was not tested; the text calls the verbal subtests significant though every interval includes zero; the abstinent-group total is 218 against 208 by arithmetic; Table 2 has errors, including the Wareing 2004a/b samples swapped against Murphy's table. Schilt: the abstract says the groups were matched on other substances (Methods: sex, age, IQ only); recognition B (1.77) is printed next to the odds ratio's interval; the duration row is impossible. Halpern: "medium effect excluded on many measures" holds for 6 of 14.
