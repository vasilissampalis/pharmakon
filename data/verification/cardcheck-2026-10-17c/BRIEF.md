# Batch 3b second reading (2026-10-17): anchors at the stated place, cards, and the claims they change

You are an independent second reader for Pharmakon's methamphetamine page. The first readers (AI readers 19 and 20) read seven newer papers in full on the web (publisher pages and PubMed Central), wrote one study card per paper and 20 new evidence anchors, and proposed changes to five claims. Those changes are now in the project files, marked as first-pass. You did not write any of this work. Your job is to check it against the sources. The source decides; neither reader is presumed right.

Read these first, in the project at `/home/claude/drug-encyclopedia`:
- `docs/VERIFICATION-BRIEF.md`: "Step 2" (card check), "Output", "Rules (hard)", "Targeted checks". Skip Step 1 (no blind extraction this round). Every source here is a web full text: follow the brief's browser instructions and `docs/STUDY-CARD-BRIEF.md` §"How to get the full text" (your own tab only; never touch another tab; no downloads, no PDF links, no CAPTCHAs).
- `docs/METHODS.md` §5 (study cards, risk of bias), §6 (claims, status labels, GRADE) and §9 (language), as needed.

## Your papers
The editor gives your assignment in the task prompt (a list of reference ids). Read each paper at the web address named in its card's `verification.source_read` (in `data/study-cards/methamphetamine.json`, id `sc_<reference>`): the publisher's HTML page, or the PubMed Central copy where the card says so. Anchors cite "publisher HTML" or "PMC HTML" with a section and paragraph locator; count paragraphs as the locator convention in `docs/VERIFICATION-BRIEF.md` says. Figures that are images: check only what the text and legends say, as the first readers did.

## Task 1: the anchors
`data/verification/targeted-2026-10-17g/tasks.json` lists the 20 new anchors. Check those of your papers one by one at the stated page and locator, as "Targeted checks" says: `confirmed`, `corrected` (give the corrected page, locator or extracted text, in your own words, numbers exact), `wrong-location` (give the right place) or `not-found`. Check every number, the role (supports, qualifies, contradicts) and any quotation (verbatim, at most 15 words). Values from figures that are only images cannot be checked: say so.

Write `data/verification/targeted-2026-10-17g/out_<your reader name, e.g. reader21>.json`:
```json
{"reader": "AI reader 21 (targeted check at the stated place, web full texts)", "date": "2026-10-17",
 "results": [{"n": 1, "claim_id": "…", "anchor_index": 0, "verdict": "confirmed", "corrected": {}, "note": "what you compared"}]}
```
`corrected` holds only the fields you would change (`page`, `locator`, `extracted`, `role`, `quote`).

## Task 2: the cards
The seven cards are in `data/study-cards/methamphetamine.json` (ids `sc_<reference>`, status first-pass). For each of your cards, do "Step 2" of the verification brief: every key finding and every reporting issue `confirmed` / `corrected` / `wrong-location` / `not-found`; agree or disagree with the risk-of-bias judgment (instrument, every domain, overall) and the interpretation-gap assessment; list what the card missed that matters. Write one file per paper, `data/verification/cardcheck-2026-10-17c/out/<reference>.json`, in the format of the brief's "Output" section, with `"claims": []`.

## Task 3: the claims your papers change
For each claim that cites your papers, read the claim as it now stands in `data/claims/methamphetamine.json` (statement, plain, magnitude, grade with its reasons, status, verification) and its changelog entry for today. Give your view on:
1. **Status label** (METHODS §6.4; glossary "Status"): is the label right? Replicated needs at least two independent studies agreeing in direction; studies that share investigators, site or sample are "replicated by the same team"; "mixed" means inconsistent findings with no adequate explanation.
2. **GRADE**: each domain and the overall certainty, with reasons.
3. **Plain text**: does it say more than the statement or the evidence?
4. **Verification step**: is the move from draft to metadata-verified right (METHODS §6.3 and §12: a claim resting only on narrative reviews stays draft)?

The first readers flagged these questions; give your view on those in your papers:
- `cl_meth_psychosis_treatment`: reader 19 proposes status "mixed" (now that a placebo-controlled trial, a trial against usual care and a 2026 review are added); the adjudicator had set "single study" this morning, before these papers were read. Which label fits the evidence as it now stands, and is the wording fair to Chung 2026 (its registered primary outcome changed after the trial ended)?
- `cl_meth_psychosis_course`: Murrie 2020's pooled 22% transition to schizophrenia now leads; is that fair given I² 96% and unnamed studies?
- `cl_meth_psychosis_association`: Huang 2022 (Taiwan registry, HR 5.28) added without an upgrade for a large effect.
- `cl_meth_us_trends`: Tanz 2025's opioid share added; status kept single study.
- `cl_meth_cognition_normal_range`: Dean 2018's estimated starting point from school grades.

Write `data/verification/cardcheck-2026-10-17c/claims_<your reader name>.json`:
```json
[{"claim_id": "…", "status": {"verdict": "agree|disagree", "proposed": "…", "reason": "…"},
  "grade": {"verdict": "agree|disagree", "proposed": "…", "reason": "…"},
  "plain": {"verdict": "agree|disagree", "proposed": "…", "reason": "…"},
  "verification": {"verdict": "agree|disagree", "reason": "…"},
  "note": "…"}]
```

## Rules
- The hard rules of `docs/VERIFICATION-BRIEF.md` apply. Use only the browser tab you created; close it when you finish.
- Do not edit any project file other than your own output files named above.
- Validate each JSON file with `python3 -c "import json,sys; json.load(open(sys.argv[1]))" <file>`.
- Final report, under 250 words: anchors not confirmed (with the correction), card findings corrected or not found, risk-of-bias disagreements, and your view on each status, GRADE or plain-text question where you disagree.
