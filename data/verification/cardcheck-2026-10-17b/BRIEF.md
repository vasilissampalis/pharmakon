# Batch 3 second reading (2026-10-17): anchors at the stated place, cards, and the claims they change

You are an independent second reader for Pharmakon's methamphetamine page. The first readers (AI readers 12, 13 and 14) read ten newer papers from PDFs, wrote one study card per paper and 47 new evidence anchors, and proposed changes to ten claims. Those changes are now in the project files, marked as first-pass. You did not write any of this work. Your job is to check it against the PDFs. The source decides; neither reader is presumed right.

Read these first, in the project at `/home/claude/drug-encyclopedia`:
- `docs/VERIFICATION-BRIEF.md`: "Step 2" (card check), "Output", "Rules (hard)", "Targeted checks". Skip Step 1 (no blind extraction this round) and ignore its browser instructions: every source here is a PDF.
- `docs/METHODS.md` §5 (study cards, risk of bias), §6 (claims, status labels, GRADE) and §9 (language), as needed.

## Your papers
The editor gives your assignment in the task prompt (a list of reference ids). The PDFs are in `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/Methamphetamine/`:
Srisurapanont_2021_EfficacyDropoutRatesAntipsychotic.pdf · Voce_2019_SystematicReviewSymptomProfile.pdf · CohenLaroque_2024_PositiveNegativeSymptomsMethamphetamine.pdf · Boden_2023_MethamphetamineUsePsychoticSymptoms.pdf · Sibanda_2019_PrevalenceRiskFactorsEmergency.pdf · Marel_2019_ConditionalProbabilitiesSubstanceUse.pdf · Foulds_2020_MethamphetamineUseViolenceFindings.pdf · Zhu_2025_MethamphetamineCocaineOverdoseDeaths.pdf · McKetin_2026_MirtazapineMethamphetamineUseDisorder.pdf · Bakouni_2023_BupropionTreatmentAmphetamineType.pdf

Extract text with `pdftotext -layout` into your own scratch folder under `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/batch3-check/<your reader name>/`. Render pages with `pdftoppm -r 110` and look at them for every table and figure value you check.

**Page numbers.** Anchors cite the page number printed on the PDF's pages. Three PDFs are online-first versions whose printed numbers differ from the reference record; their anchors say "of the online-first PDF": `voce_2019` and `sibanda_2019` (an unnumbered publisher's cover page, then article pages 1–11 and 1–12) and `boden_2023` (pages 1–8). Articles in *Drug and Alcohol Dependence* with article numbers (`foulds_2020`, `srisurapanont_2021`, `bakouni_2023`) are numbered 1–n in the PDF.

## Task 1: the anchors
`data/verification/targeted-2026-10-17f/tasks.json` lists the 47 new anchors. Check those of your papers one by one at the stated page and locator, as "Targeted checks" says: `confirmed`, `corrected` (give the corrected page, locator or extracted text, in your own words, numbers exact), `wrong-location` (give the right place) or `not-found`. Check every number, the role (supports, qualifies, contradicts) and any quotation (verbatim, at most 15 words). Values read from figures are checked on the rendered page.

Write `data/verification/targeted-2026-10-17f/out_<your reader name, e.g. reader15>.json`:
```json
{"reader": "AI reader 15 (targeted check at the stated place, PDFs)", "date": "2026-10-17",
 "results": [{"n": 1, "claim_id": "…", "anchor_index": 0, "verdict": "confirmed", "corrected": {}, "note": "what you compared"}]}
```
`corrected` holds only the fields you would change (`page`, `locator`, `extracted`, `role`, `quote`).

## Task 2: the cards
The ten cards are in `data/study-cards/methamphetamine.json` (ids `sc_<reference>`, status first-pass). For each of your cards, do "Step 2" of the verification brief: every key finding and every reporting issue `confirmed` / `corrected` / `wrong-location` / `not-found`; agree or disagree with the risk-of-bias judgment (instrument, every domain, overall) and the interpretation-gap assessment; list what the card missed that matters. Write one file per paper, `data/verification/cardcheck-2026-10-17b/out/<reference>.json`, in the format of the brief's "Output" section, with `"claims": []`.

## Task 3: the claims your papers change
For each claim that cites your papers, read the claim as it now stands in `data/claims/methamphetamine.json` (statement, plain, magnitude, grade with its reasons, status, verification) and its changelog entry for today. Give your view on:
1. **Status label** (METHODS §6.4; glossary "Status"): is the label right? Replicated needs at least two independent studies agreeing in direction; studies that share investigators, site or sample are "replicated by the same team"; "mixed" means inconsistent findings with no adequate explanation.
2. **GRADE**: each domain and the overall certainty, with reasons.
3. **Plain text**: does it say more than the statement or the evidence?
4. **Verification step**: is the move from draft to metadata-verified right (METHODS §6.3 and §12: a claim resting only on narrative reviews stays draft)?

The first readers flagged these questions; give your view on those in your papers:
- `cl_meth_mirtazapine`: "replicated" (new Australian trial) against "replicated by the same team" (one shared author, Shoptaw, with Colfax 2011) or "mixed" (the Australian trial's drug-test outcome did not differ).
- `cl_meth_acute_toxicity`: status "mixed"; inconsistency rated down; draft → metadata-verified.
- `cl_meth_dependence_baserate`: status "mixed", although the two studies measure different things and inconsistency is not rated down.
- `cl_meth_violence`: wording "not settled"; no dose-response upgrade.
- `cl_meth_us_trends`: Zhu 2025 extends the series but uses the same death records (single-study kept).
- `cl_meth_psychosis_treatment`: single study → replicated; draft → metadata-verified.
- `cl_meth_psychosis_course` and `cl_meth_psychosis_vs_schizophrenia`: draft → metadata-verified.
- `cl_meth_psychosis_association`: Boden 2023 added (adjusted OR 1.33).
- Cohen-Laroque 2024: reader 12 could not reproduce the positive-symptom pooled null from the paper's Table 1. Check the arithmetic yourself.

Write `data/verification/cardcheck-2026-10-17b/claims_<your reader name>.json`:
```json
[{"claim_id": "…", "status": {"verdict": "agree|disagree", "proposed": "…", "reason": "…"},
  "grade": {"verdict": "agree|disagree", "proposed": "…", "reason": "…"},
  "plain": {"verdict": "agree|disagree", "proposed": "…", "reason": "…"},
  "verification": {"verdict": "agree|disagree", "reason": "…"},
  "note": "…"}]
```

## Rules
- The hard rules of `docs/VERIFICATION-BRIEF.md` apply. No browser is needed or allowed this round.
- Do not edit any project file other than your own output files named above.
- Validate each JSON file with `python3 -c "import json,sys; json.load(open(sys.argv[1]))" <file>`.
- Final report, under 250 words: anchors not confirmed (with the correction), card findings corrected or not found, risk-of-bias disagreements, and your view on each status, GRADE or plain-text question where you disagree.
