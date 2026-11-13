# AI reader 20 (first reader), batch 3b: methamphetamine currency update, papers read in the browser, 2026-10-17

Cards written (all pass `check_card.py` with no warnings; `rob_vocab.py` no problems; status first-pass): `data/study-cards/_incoming/methamphetamine/sc_huang_2022.json`, `sc_tanz_2025.json`, `sc_dean_2018.json`.
Patch: `reader20_patch.json` (3 claims, 8 new anchors, all `ai-located`); `claim_patch.py --dry-run` passes; **not applied**.
Not readable: none. All three were read in full in my own tab of the app's browser (no other tab touched; tab closed at the end). No reference files were edited and no lines were appended to `data/references/_incoming/`.

## Papers

**Huang et al. 2022** (retrospective registry cohort, Taiwan; PMC10231478; ROBINS-E very high, from confounding). The cohort covers 2007–2016. It compares 74,601 adults followed from their first arrest for an amphetamine-type substance (urine-confirmed) with 298,404 insured adults with no drug record, matched on age, sex and index year; people with an earlier psychosis diagnosis were excluded. A first psychosis diagnosis was recorded at 4.68 vs 0.77 per 1,000 person-years (10-year cumulative incidence 3.75% vs 0.63%). The HR was 5.28 (4.90–5.70), adjusted only for age, sex and five comorbidity codes; those codes were recorded at any time in the study, including after the arrest. Limits the abstract does not give:
- "Amphetamine" covers 23 substances, including MDMA, with no breakdown.
- Other drug and alcohol use, socio-economic position and family history were not measured.
- The outcome code list omits the drug-induced psychosis codes that the text says were included.
- The arrest gradient (4.49 to 6.25) uses arrests counted over the whole follow-up.
- The authors call the analysis exploratory and not preregistered.

The discussion infers "a direct effect of amphetamine" from the smaller HR with comorbidity, but the rate difference is in fact larger with comorbidity (12.6 vs 3.3 per 1,000). It infers "a preventive effect of psychotherapy" from rehabilitation that prosecutors offered to about 10% judged to have good prospects.

**Tanz et al. 2025** (CDC MMWR report; publisher HTML; JBI moderate). It draws on two systems:
- SUDORS, January 2021–June 2024: 49 states and DC, four of them for only part of the period; drugs named by medical examiners, coroners and toxicology. Methamphetamine was involved in 96,614 of 309,274 overdose deaths (31.2%); 68.8% of these also involved opioids and 30,139 did not. Decedents without opioids were older (64% vs 39% aged 45 or over, editors' calculation) and more often had a history of cardiovascular disease (39.3% vs 19.8%).
- NVSS: the age-adjusted T43.6 death rate rose from 3.9 per 100,000 in 2018 to 10.4 in 2023.

The report also gives 34,855 deaths for T43.6 in 2023, the same number that Zhu 2025 labels methamphetamine-involved. Three discussion inferences go beyond the report's own data:
- intentional co-use, from drug-checking studies;
- a potency or access explanation, from survey tables;
- long-term use as the reason for the cardiovascular history, compared with all US adults without age standardization.

**Dean et al. 2018** (cross-sectional, with school records as a premorbid proxy; ROBINS-E high). The nature.com page showed only the abstract without signing in. PubMed linked to the publisher's version in PMC (PMC6006320), and I read that.
- 37 people with methamphetamine dependence (tested after about a week of abstinence) and 41 controls.
- Grade point average before first use was already lower in the methamphetamine group (2.1 vs 2.5).
- Adult scores were below a prediction made from grades, parental income, age and smoking with a model fitted in the controls (R² 0.41): overall d 0.61, attention 0.69, memory 0.46, executive function not below.
- Scores were standardized to the controls, not to norms. The paired tests ignore the model's own uncertainty. Other substance use disorders were far more common in the methamphetamine group.
- The abstract's "support the view that ... causes a decline" is hedged by the authors' own limitations section.

## Claims

**cl_meth_psychosis_association** (built on 0.7.0, after AI reader 18's adjudication). Adds three Huang anchors (one supports, two qualify). The statement, magnitude, population, exposure, comparator, outcome and plain text add the Taiwan cohort with its limits. The statement also says that the cohort orders arrest before the first recorded diagnosis, not use before onset.
- GRADE: unchanged (low). Same direction; not counted as inconsistency, because exposure, comparator and outcome differ.
- No large-effect upgrade: the remaining biases (no adjustment for other drugs or socio-economic position, a drug-free comparison group, more contact with services after arrest) all run away from the null.
- No dose–response upgrade: arrests are counted over the whole follow-up, and the trend p comes from five group rates.
- The rehabilitation comparison is not used. Status stays replicated.

**cl_meth_us_trends** (built on 0.4.2). Adds three Tanz anchors (two support, one qualifies). The statement, magnitude and plain text now give:
- the opioid share that the claim lacked (68.8% of methamphetamine-involved deaths in 2021–2024), with a note that it comes from a different system and period than Han's 2019 share;
- the age-adjusted T43.6 rates for 2018 and 2023;
- the matching 2023 count, which suggests that Zhu's series is T43.6 (editors' inference);
- the age and cardiovascular profile of deaths without opioids, and the expected undercount.

Rating (low) and status (single-study) are unchanged: the trend comes from the same national death records. The reasoning notes, as the editors' reading, that the undercount may fall more on deaths without opioids, so the opioid share may be somewhat overstated.

**cl_meth_cognition_normal_range** (built on 0.4.2). Adds two Dean anchors (both qualify). The statement used to say that no study measured a starting point. It now says that no study tested people before use, but one estimated a starting point from pre-use school grades, with the result and its limits; it notes that the study comes from the same laboratory as the percentile study. The magnitude, comparator, outcome, plain text and reasoning are updated. Rating (very low) and status (replicated) are unchanged: the study bears on decline from a higher starting point, not on whether means lie within norms.

All three claims are ai-anchored now; `claim_patch.py` will move them to metadata-verified until the new anchors are checked.

## Reporting errors noticed (details and anchors on the cards)

- **Huang:**
  - The outcome code list omits the drug-induced psychosis codes (292.1x) that the text says were counted.
  - The comorbidity covariates were recorded during 2007–2016, yet Table 1 is labelled baseline. The depression codes include 296.24 and 296.34, which are also outcome codes.
  - The printed p for trend, 0.038, is reproduced exactly by a regression of the five category incidence rates on the number of arrests (3 df). The HRs for one and for five or more arrests have non-overlapping intervals.
  - The age bands in the Methods (18–35, 35–49, 50+) differ from those in the tables (18–29, 30–44, 45+).
  - Rates per person-year are called "annual cumulative incidence". The control rate (77 per 100,000) is called "slightly higher" than incidences of psychotic disorders that it exceeds 2.4 to 2.9 times.
  - "Times more likely" is used for both the crude ratio (6.08) and the adjusted HR (5.28).
- **Tanz:**
  - In the HTML Table, men among methamphetamine deaths without opioids are printed as 2,236; the column implies 22,236.
  - The any-stimulant American Indian or Alaska Native total is printed as 2,819, but its cells sum to 2,891.
  - The denominator of "14.5% involved only stimulants" is ambiguous.
  - The abstract calls T43.6 "primarily methamphetamine" without giving a share.
- **Dean:**
  - Abstinence is given as a mean of 6.9 days (SD 2.7) with a range of 3–30 in 37 people, which is impossible: a single value of 30 alone would make the SD at least 3.9.
  - For executive function, the printed d of −0.27 does not fit t(36) = −0.169, which gives about −0.03.
  - The grade-matched subgroup (28 per group) is printed with t(36).
  - The correlations with grams per day fit about 26 participants, not 37; the n is not stated.
  - The ethnicity counts sum to 39 of 41 and 32 of 37.

## Notes for the editor

1. The adjudication patch (AI reader 18) and the merge of the batch-3 cards were applied while I was reading. I re-read the three claims afterwards and built the patch on their current versions. The patch expects the version and the full current value of every field it changes, so it will refuse if any of them moves again. Text changes are `replace` operations on passages that each occur once.
2. Simulation in a scratch copy (`batch3b/reader20_sim/`): I merged my three cards with `merge_cards.py`, applied the patch, and ran `validate.py`. Result: 0 hard failures; warnings went from 417 to 425, which are the 8 expected warnings for anchors that are not senior-verified.
3. `check_anchor_numbers.py` checks PDF anchors only. In its place, I searched each page's text in my tab for every number of two or more digits in the key findings and the new anchors (editors' calculations excluded). All were found.
4. Not read: the Tanz Supplementary Figure (a separate file; it holds the overall trends with and without opioids) and Dean's Supplementary Table 1. Huang has no supplement. Figures in all three are images; no values were taken from them.
5. The `dean_2018` record has no PMCID. PMC6006320 could be added by the reference build (I added no reference line, as instructed).
6. Not assigned to me, but Dean 2018 bears on `cl_meth_cognition_causal` (contested), on both sides:
   - lower pre-use grades: a premorbid weakness;
   - adult scores below prediction, and a shortfall related to grams per day (about 26 people, not years or frequency of use), which qualifies "scores are mostly unrelated to how much ... people used".
7. The `data/site/simple.json` entries for the three claims will need rewriting when the patch is applied (WRITING-RULES).
