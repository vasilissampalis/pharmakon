# AI reader 13 (first reader), batch 3: methamphetamine currency update, 2026-10-17

Cards written (all pass `check_card.py`; status first-pass): `data/study-cards/_incoming/methamphetamine/sc_sibanda_2019.json`, `sc_marel_2019.json`, `sc_foulds_2020.json`, `sc_zhu_2025.json`.
Patch: `reader13_patch.json` (4 claims, 11 new anchors, all `ai-located`); `claim_patch.py --dry-run` passes; **not applied**.
Not readable: **tanz_2025** (CDC MMWR). The desktop app's browser was not reachable (three attempts, two at the start and one at the end); no card, no anchors. No reference files were edited; no lines were appended to `data/references/_incoming/` (the records already exist).

## Papers

**Sibanda et al. 2019** (systematic review and meta-analysis; PDF pp. 1–12, the online-first pages; AMSTAR 2 critically low). 23 emergency-department, psychiatric-emergency and trauma-centre studies (searches 1990–2017; 17 from the USA, 7 of them from one centre). Unlike what the currency check expected, it pools **no clinical feature**: the authors say the studies measured them inconsistently. It lists study-level figures instead (tachycardia 42% and 85%, hypertension 6.4% and 69%, psychosis 12% to 80%, agitation 13% to 48%, aggression 18% to 50%, suicidal thoughts or behaviour 6% to 50%, acute coronary syndrome in 9 of 36 chest-pain patients), mostly without denominators, and reports **no deaths**. Only three things are pooled: the share of methamphetamine-positive attendees (11.3%, 6.3–19.7; 22.8% with toxicology against 5.7% with self-report), sex and age. The prevalence pool mixes denominators that cannot be compared and counts one data set twice. One of its studies (Gray et al. 2007, Perth) is also a source of the narrative review the claim rested on.

**Marel et al. 2019** (2007 Australian national survey, 8,841 people aged 16–85, response 60%; PDF pp. 136–142; JBI moderate). For 579 people who had used stimulants (the paper never says which drugs count as stimulants), 45.7% (39.5–51.8) had ever met DSM-IV criteria for stimulant **abuse or dependence** at the interview. A survival analysis estimated a cumulative probability of 50.4% (no interval) within 14 years of first use, 12.2% in the first year. The abstract gives only the 50.4%. Its "lifetime" figure stops at 14 years, and the diagnostic questions were asked only of people who had used at least five times.

**Foulds et al. 2020** (Christchurch birth cohort, interviewed at 21–35; PDF pp. 1–7; ROBINS-E high overall, with no single domain high). Any use in a period went with violence in the same period after very wide adjustment. Fully adjusted odds ratios: perpetration 1.60 (1.01–2.54), victimisation 1.57 (1.00–2.47), intimate-partner perpetration 1.55 (1.04–2.30), intimate-partner victimisation 1.09 (0.80–1.49). With at least weekly use (51 people) the odds were higher, for example perpetration 4.84 (2.48–9.46), but that analysis was adjusted for childhood factors only. Use and violence were reported for the same periods, all by self-report, and other illicit drugs were not adjusted for. These estimates agree with the review's pooled adjusted 1.4 (0.8–2.4); they do not "run against" it, as the currency check suggested. The abstract's "independent risk factor" and the discussion's "substantial role" go further than the data.

**Zhu et al. 2025** (research note, CDC WONDER death records, all ages; PDF pp. 1946–1949; JBI moderate). Overdose deaths involving methamphetamine rose from 547 (1999) to 34,855 (2023), a crude rate of 0.20 to 10.41 per 100,000. The rise was steepest in 2018–2021 (+37.4% a year) and slowed to +3.4% a year (0.2–6.8) in 2021–2023, on provisional 2023 data. Deaths with fentanyl grew fastest (+76% a year in 2012–2021); deaths with other opioids fell in 2021–2023. The ICD-10 codes are given only in a supplement, so the series cannot be matched to the T43.6 proxy from the article itself. The note does not give the share of methamphetamine deaths that also involved opioids.

## Claims

**cl_meth_acute_toxicity.** Adds three Sibanda anchors (two supports, one qualifies, with an 8-word quotation). Statement, plain text and magnitude are rewritten: both reviews are second-hand; the systematic review's study-level ranges are added; neither review gives a case fatality; the two reviews share a primary series. GRADE: inconsistency −1 is added (frequencies differ several-fold without explanation), alongside risk of bias −1 and indirectness −1, so certainty stays very low. Status single-study → **mixed**: the features recur across series, but their frequencies are inconsistent ("replicated" for the mere presence of features is the alternative, which I think overstates). Verification **draft → metadata-verified**, because the claim no longer rests only on a narrative review (§6.3, §12).

**cl_meth_dependence_baserate.** Adds two Marel anchors (qualifies). The statement and plain text keep the two measures apart:
- Anthony 1994: the share of everyone who had ever used, even once, who had already been **dependent** by the day of the interview.
- Marel 2019: a survival-analysis estimate of how many would develop **abuse or dependence within 14 years of first use**, allowing for people who started only recently; plus 45.7% already affected at the interview.

Different outcome, measure, class, country and decade, so the two cannot be compared directly. GRADE: risk of bias −1 for the Australian figures only (60% response, recalled timing, unclear denominator); inconsistency not downgraded (they are different quantities); indirectness −2; certainty stays very low. Status single-study → **mixed** (figures four- to five-fold apart, with explanations that have not been tested). The reasoning notes that the Anthony quotation ("perhaps a vast majority…") depends on the measure. No second quotation was added (the claim already has one).

**cl_meth_violence.** Adds three Foulds anchors (qualifies, one with an 11-word quotation of the authors' conclusion). The statement adds the cohort's fully adjusted estimates, the at-least-weekly odds with their weaker adjustment, and the cohort's limits. "Not established" becomes "not settled". Relation (insufficient evidence), status (mixed) and rating (very low: risk of bias −1, imprecision −1) are unchanged. The dose-response upgrade was considered and not applied: it is adjusted for childhood factors only, rests on 51 people, and confounding that grows with frequency of use could produce it. Domain notes added. **McKetin et al. 2020** (not available): the reasoning places it beside the birth cohort as a second longitudinal source, on violent crime. It shares three authors with Foulds (McKetin, Boden, Foulds), and Foulds and McKetin are also authors of the 2019 review, so check overlap of authors and data before counting it as independent replication.

**cl_meth_us_trends.** Adds three Zhu anchors (one supports, two qualify). The statement, plain text and magnitude extend the death series to 2023 for all ages, with its limits: codes only in a supplement, provisional 2023 data, two 2023 counts, crude rates. Rating (low) and status (single-study) are unchanged: Zhu draws on the same national death records as Han 2021, so it extends the series rather than replicating it. **Tanz 2025** would fit here, as the source for opioid co-involvement and stimulant deaths without opioids after 2019; the reasoning records it as not yet read.

**cl_meth_mortality.** None of the four papers bears on it. Zhu gives population death rates with no denominator of people who use methamphetamine, so it cannot inform standardized or crude mortality in cohorts of people who use. Sibanda reports no deaths. No change proposed.

Three of the claims are now ai-anchored, and `claim_patch.py` will move them to metadata-verified until the new anchors are checked.

## Reporting errors noticed (details and anchors on the cards)

- **Sibanda:**
  - Turnipseed 2003 has 36 patients in the text but 171 in Table 1.
  - "Nine" toxicology studies in the text against 8 in the subgroup analysis.
  - Table 1 prints Marshall 2012 as 30/133 = 45.3% (it is 22.6%, as Figure 2 shows) and London 2009 as 9.3% (it is 9.0%).
  - Men are printed as 23,434 in the sex analysis; Figure 3 sums to 28,434.
  - The "pooled variance" of 57.1% men cannot be reproduced; in Figure 3 men are 72% of methamphetamine-positive cases.
  - I² 50.16 and p = 0.029 fit Q ≈ 20.06, not the printed 20.66.
  - Hendrickson 2008 and 2010 (same data set) are pooled separately.
  - Pasic 2007: 12 of 60 is printed as 23% (it is 20%).
  - Szuster's percentages imply 14 people, not 32.
  - The search section says reference lists added no study; the flow diagram adds one.
  - 18, not 17, studies appear across the forest plots.
  - Sensitivity analyses are said to have been run but are not reported.
  - Horyniak 2014 (ecstasy and related drugs) is pooled as amphetamine-related.
- **Marel:**
  - Two figures for the same transition (45.7% and 50.4%) are never reconciled.
  - The "lifetime" probability stops at 14 years.
  - The stimulant class is never defined.
  - It is unclear whether people who used fewer than five times are in the denominator.
  - The rules for coding age of first use conflict (13 against 12).
  - Table 1's "weighted prevalence" row is undefined. It appears to be the prevalence of the disorder, not of use (3.3% ÷ 45.7% ≈ 7.2%, close to the 6.5% unweighted share).
  - The discussion says "regular use", while the analysis starts at first use.
  - Odds ratios are called "risk".
- **Foulds:**
  - Two Table 3 cells are identical: 1.89 (1.15–3.11).
  - The interaction terms make the main-effect odds ratios hard to read; for victimisation the sex interaction was significant.
  - The "% pooled" row in Table 1 is inconsistent with the counts.
  - The lowest exposure category is defined two ways.
  - The text says Table 3 shows percentages; it shows odds ratios only.
  - The Model 2 covariates are listed inconsistently.
  - "Role of funding source: None", although the acknowledgements name an HRC grant.
- **Zhu:**
  - 2023 counts: 34,855 against 35,126 (cocaine: 29,449 against 29,692).
  - In Table 1, the AAPCs for women (methamphetamine, 8.54) and men (cocaine, 18.61) are **transposed**. Recomputing from the printed segments reproduces every other AAPC exactly and swaps these two.
  - The cocaine segment label for Black people should be 2006–2012.
  - The "roughly one-third" combines two shares that overlap.

## Notes for the editor

1. Merge the four cards before applying the patch: `validate.py` refuses anchors that point to cards it cannot find. In a scratch copy with the cards merged and the patch applied, `validate.py` gives 0 hard failures and adds only the 11 expected warnings for anchors that are not senior-verified.
2. `check_anchor_numbers.py` will report 47 false misses on the three Sibanda anchors. Its reference record gives the print range 567–578, while the PDF has a cover page followed by online-first pages 1–12 (cited as METHODS §6.2 requires). With the PDF's own page numbering, all 217 numbers in the 11 new anchors are found on the stated pages (`r13scripts/check_numbers_r13.py`).
3. On AMSTAR 2 item 4 I applied the instrument strictly ("no": the English-only limit is not justified). `sc_mcketin_2019` rated the same situation "partial-yes". The overall rating is critically low either way.
