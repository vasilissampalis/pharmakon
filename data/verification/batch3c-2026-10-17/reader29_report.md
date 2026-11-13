# AI reader 29 (first reader), batch 3c: McKetin 2020 and the Ersche 2012 supplement, 2026-10-17

Cards written (both pass `check_card.py` with no warnings; status first-pass):
- `data/study-cards/_incoming/methamphetamine/sc_mcketin_2020.json` (new): 14 key findings, 7 reporting issues.
- `data/study-cards/_incoming/methamphetamine/sc_ersche_2012.json` (the whole card, updated from the supplement): 11 key findings added (22 in all), 5 reporting issues added and 5 rewritten (12 in all). Each change has its own `verification.disagreements` entry (64 new entries). Status goes from ai-checked to **first-pass**, because the content from the supplement has not been checked yet. The earlier check of the main-report content is kept in `checked_by`.

Patch: `reader29_patch.json` (2 claims, 7 new anchors, all `ai-located`, no quotation). Every field it changes carries an `expect` copied from the claim as it stands. `claim_patch.py --dry-run` passes. **Not applied.**
Simple lines: `reader29_simple.json`. They start from the entries as revised by the 17 October simple-layer check (applied at 18:48, after this batch began) and keep its fixes. For violence the file also gives an alternative set, in case the senior author keeps the relation as insufficient evidence. For the siblings claim, the "How we know" point "Some differences were bigger the longer people had used" is dropped. No reference files were edited, and no lines were added to `data/references/_incoming/`.

## Papers

**McKetin et al. 2020** (Drug and Alcohol Dependence 216, 108262; PDF pp. 1–6, all read; Table 1 and Fig. 1 checked on rendered pages; ROBINS-E high overall, with no single domain high). The paper is a within-person analysis of the MATES cohort: 469 people dependent on methamphetamine, mostly entering treatment in Sydney and Brisbane, and mostly injecting. Each person reported on the past month at entry, 3 months, 1 year and 3 years (2006–2010), giving 1,513–1,518 person-months. All crime was self-reported on the OTI scale. Each type of crime was more common in months with use than in the same person's months without use:
- violent crime: 12% against 3% of months; odds ratio 8.2 (4.2–15.9) unadjusted, and **3.4 (1.5–8.0)** after adjustment for age, income, employment, housing and other drugs;
- any crime 4.7, dealing 5.9, property crime 5.5;
- fraud 1.7 (0.8–3.3), not significant.

Limits:
- Adjusting for other drugs halved the estimates.
- The "dose related" result rests on unadjusted pooled percentages (Fig. 1, which prints no values; I measured the bars). The adjusted dose results are in a supplement, which is not available (Tables S1–S3).
- The analysis was exploratory. Use and crime come from the same month and the same interview. Treatment and imprisonment are not taken into account.
- The methods describe the model ambiguously: a random intercept, but also the fixed-effects option. The number of people who contribute to each estimate is not reported.
- The abstract's "likely social consequence" is a causal reading. "Five times more likely" reads an odds ratio as a risk ratio; for any crime the raw ratio is 3.2.

**Ersche et al. 2012, Supporting Online Material** (12 pages, all read; Tables S1–S3 and Figs. S1–S2 on rendered pages). The main report had already been read. The supplement:
- **Which stimulants:** 94% of the dependent siblings were dependent on cocaine and 6% on amphetamines (3 of 50), with the amphetamines not named. Methamphetamine is not mentioned anywhere.
- **Testing state and other drugs:** the dependent siblings were still using when tested (urine positive in all but three). Most were also dependent on another substance: opiates 55%, alcohol 26%, cannabis 9%.
- **Enrolment criterion for the siblings:** no personal history of substance dependence except nicotine. The main report says "chronic abuse" instead.
- **Sample and confounders (Table S1):** men 64%, 51% and 92% (controls, siblings, dependent siblings); current smokers 12%, 55% and 94%; education is reported. 146 people were analysed for grey matter and 145 for white matter.
- **Analyses:**
  - Grey-matter maps were thresholded to allow one false-positive cluster per map. The "shared" clusters are where two comparisons against the same control group overlap.
  - The FA values come from voxels selected because they differed between groups.
  - The familiality tests are one-tailed.
  - Smoking was checked for grey matter only, without statistics.
  - The correlations with years of use are maps only, with no statistics and no adjustment for age.
- **Labels:** the supplement calls the medial temporal cluster "amygdala/hippocampus" in places. It names no orbitofrontal or anterior insular cluster.

## Claims

**cl_meth_violence.** I add three McKetin anchors (one supports, two qualify).
- **Relation:** insufficient evidence → **is associated with**. The adjusted association now appears in two longitudinal cohorts, one in the general population and one in people dependent on methamphetamine. The intervals of both exclude no association, and the review's adjusted pooled estimate points the same way. The statement still says that whether use causes violence is not settled.
- **Status:** mixed → **replicated by the same team**. The two cohort papers share three authors (McKetin, Boden, Foulds). The MATES paper shares four authors with the review (McKetin, Foulds, Degenhardt, Farrell). MATES is also inside the review's pooled estimate through its 2014 hostility paper. The unadjusted split between violent behaviour and violent offending in the review is kept in the reasoning, as heterogeneity that is noted but not rated down, because the rating rests on adjusted estimates.
- **GRADE:** unchanged at very low (risk of bias −1, imprecision −1). Dose-response and large effect were considered and not applied.
- **Anchor role:** the birth-cohort anchor with the fully adjusted estimates now supports instead of qualifying.
- **Alternative**, if the senior author gives more weight to the shared authorship and to the review's null adjusted pool: keep insufficient evidence and mixed, and add the McKetin anchors as "qualifies".

**A separate crime claim is justified**, as a single-study claim at very low certainty. It should not be folded into the violence claim. Proposed wording: "In people dependent on methamphetamine (one Australian cohort, 469 people, 2006–2010), months with use, compared with the same people's months without, are associated with more self-reported crime, mostly drug dealing and property crime: any crime in 56% against 17.5% of months; adjusted within-person odds ratios 4.7 (2.8–8.0) for any crime, 5.9 (3.0–11.9) for dealing, 5.5 (2.8–10.8) for property crime and 1.7 (0.8–3.3) for fraud."
- Relation: is associated with. Status: single study. Section 9.
- GRADE: starts low; risk of bias −1 (same-month self-report, changes around treatment entry, an exploratory analysis); very low.
- No upgrade for large effect: the remaining biases, including reverse causation (dealing brings money and drugs), run away from the null.
- No upgrade for dose-response: the adjusted dose results are only in the unread supplement.
- I could not write it as a patch, because `claim_patch.py` changes existing claims only.

**cl_meth_siblings.** I add four supplement anchors (three qualify, one supports).
- **Stimulants:** the review's account is replaced by the study's own figures (94% cocaine, 6% amphetamines). The claim's line "most of the dependent people used cocaine" is confirmed. "Not known whether any used meth" still holds: the paper never says.
- **Updated in the statement:** the siblings' criterion; the analysed numbers, sex and smoking; the cluster threshold; and the hippocampus, orbitofrontal and anterior insula points. The orbitofrontal and anterior insular statements cannot be traced to the study.
- **Duration of use:** "fits an additional effect of use" is withdrawn, because the maps have no statistics and do not separate years of use from age or from opiate and alcohol dependence. The matching "How we know" point is dropped.
- **Magnitude:** adds the Table S2 values, with my standardized differences (0.7–1.3), flagged as inflated by voxel selection. It drops the "144 of 150" calculation, which the supplement explains.
- **Main-report anchor:** its closing clause "supplement not read" is removed.
- **GRADE:** the notes are no longer provisional. Certainty (very low), relation and status are unchanged.

## Reporting errors noticed (details and anchors on the cards)

- **McKetin:**
  - The model is described ambiguously (random intercept, or the fixed-effects option), and the number of people contributing to each estimate is not given.
  - Odds ratios are called "times more likely".
  - "Dose related" rests on an unadjusted figure; the adjusted results are only in the supplement.
  - The text says "16+ against 0–15 days", while the methods compare 1–15 and 16+ days with no use.
  - Table 1 percentages are on 1,520 months, not on the 1,513–1,518 analysed; 17.5% is printed as 17%.
  - "469 met DSM-IV criteria" should be 484.
  - "Role of funding source: Nothing declared", beside named funders.
- **Ersche supplement:**
  - SSRT: Table S1 gives F = 8.9 against F(2,141) = 9.9 in the report, and neither matches its 146 participants. FA's F(2,141) fits 145 participants with sex as a covariate.
  - A wording error inverts the smoking conclusion (p. 6).
  - A heading names white matter, but white matter was never checked for smoking.
  - Table S3 lists tobacco-related findings in the superior temporal gyrus, postcentral gyrus and insula, against the text's argument; some coordinates are mislabelled.
  - The duration maps have no statistics.
  - DAST-20 is not given for the dependent group.

## Notes for the editor

1. **Merge the two cards before applying the patch:** `validate.py` refuses anchors that point to unknown cards. I checked this in a scratch copy with both cards merged and the patch applied. `validate.py` then gives 1 hard failure, which was there before my changes and is unrelated: the reference id `mitchell_2021_reply` fails the id pattern. The only new warnings are the 7 new anchors, which are not senior-verified.
2. **`mcketin_2020` has no `pdf_path`.** `check_anchor_numbers.py` prints NO TEXT until `verification.pdf_path` = `PDFs/Methamphetamine/McKetin_2020_ContributionMethamphetamineUseCrime.pdf` is added. With it added in the scratch copy, all 37 numbers are found.
3. **One reference record, two PDFs.**
   - **Supplement anchors:** the checker can read only one PDF per reference, so on the real data all four supplement anchors will show as misses. Pointed at the supplement (first page 1), all 91 numbers are found.
   - **Main report:** the PDF has a download cover page before p. 601, so the checker is off by one page for this file. This was already true before my patch: 3 false misses on p. 603. `data/access/pdf-page-basis.json` needs `"ersche_2012": {"first_page": 600}`; with it, all 9 numbers are found.
   - **Fix needed:** these two settings conflict for one reference id. A PDF file named on each anchor, or a separate reference for the supplement, would solve it. Scripts: `reader29_scripts/run_anchor_checks.py`.
4. **Applying the patch moves both claims to metadata-verified** until the new anchors are checked.
