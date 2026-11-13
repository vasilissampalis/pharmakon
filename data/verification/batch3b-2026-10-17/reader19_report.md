# AI reader 19 (first reader), batch 3b: methamphetamine psychosis treatment and course, papers read in the browser, 2026-10-17

Cards written (all pass `check_card.py` with no warnings; `rob_vocab.py` 0 problems; status first-pass): `data/study-cards/_incoming/methamphetamine/sc_fluyau_2019.json`, `sc_chung_2026.json`, `sc_hall_2026.json`, `sc_murrie_2020.json`.
Patch: `reader19_patch.json` (2 claims, 12 new anchors, all `ai-located`; one quotation, on the course claim). `claim_patch.py --dry-run` passes; **not applied**. Every field the patch changes carries an `expect` with its current value (treatment claim 0.6.0, course claim 0.8.0, both as adjudicated earlier today).
Not readable: none. All four papers were read in full in my own tab of the app's browser; no other tab was touched. No reference files were edited and no lines were appended to `data/references/_incoming/`.
- Murrie 2020: the publisher's page showed a Cloudflare security check, which I did not touch. PubMed linked a PMC copy (PMC7147575), and I read that.
- Chung 2026: I also read the ClinicalTrials.gov record (NCT03485417) and its record history (versions 7, 13, 14 and 15).

## Papers

**Fluyau et al. 2019** (systematic review without meta-analysis; publisher HTML, Frontiers; AMSTAR 2 critically low). Searches ran to November 2018, with amphetamine keywords only. The review found six randomized trials with 314 participants: five head-to-head and one placebo-controlled (aripiprazole vs placebo, 19 vs 18, 8 weeks). Five of the six are also in the network meta-analysis. Nothing is pooled.
- The claim that antipsychotics "seem to be efficacious" rests on improvement within each arm.
- The per-trial SMDs in Table 3 do not say what they compare, and four intervals have lost minus signs.
- The review describes the Farnia trial in opposite directions in its text and its table.
- The abstract's "no adverse event" contradicts the akathisia and dystonia reported, and the extrapyramidal discontinuations.
- What it adds: the placebo-controlled trial, and the olanzapine–haloperidol trial at 29 + 29 = 58 participants, matching the narrative reviews' Cochrane figure.

**Chung et al. 2026** (24-month randomized trial, Hong Kong; publisher HTML; RoB 2 high). 165 people with stimulant-induced psychosis (89.7% had used methamphetamine; mostly mildly ill, CGI-S 3.3) were randomized 1:1:2 to aripiprazole, paliperidone or usual care. In the usual-care arm 55% were antipsychotic-free at baseline and 24% at 24 months.
- CGI-S against usual care: aripiprazole −0.55 (−1.03 to −0.07; d −0.31) at 12 months and −0.65 at 24 months, when ratings were unblinded. Paliperidone: −0.40 (−0.86 to 0.06) and −0.02.
- BPRS-24 symptom scores showed no consistent difference.

What the abstract does not say:
- The registered primary outcome, relapse over 36 months, was changed after the trial ended: to the BPRS-24 in November 2025, then to the CGI in March 2026. Relapse is not reported.
- 28 participants (17%) already had a schizophrenia or schizoaffective diagnosis, although the registry excludes schizophrenia. Without them, the 12-month CGI-S difference was not significant (p = 0.12).
- Only 54% were assessed at 24 months.
- There was one suicide in the aripiprazole arm.
- 7 of 137 people (5.1%) converted to schizophrenia within 24 months, with no difference between arms.

**Hall et al. 2026** (systematic review without meta-analysis; publisher HTML, SAGE OnlineFirst; AMSTAR 2 low). The review is registered and searched to 25 March 2026. It found eight randomized trials in amphetamine-induced psychosis (514 participants): the network's six plus two placebo-controlled trials.
- Aripiprazole for 8 weeks: p = 0.032.
- Paliperidone extended-release for 84 days in people stabilised before discharge (baseline PANSS about 37): p = 0.006; 28% vs 55% lost to follow-up.
- Its "huge" effect sizes (d = 3.4 to 5.5) are changes from baseline within each arm. The two largest (Samiei 2016) assume an end-point SD of zero.
- No study followed participants after the antipsychotic was stopped.
- Trial-level tolerability: extrapyramidal symptoms in 15 of 29 on haloperidol vs 0 of 29 on olanzapine; discontinuation for adverse events in 7 of 21 on aripiprazole vs 0 of 21 on risperidone.
- The abstract's "found support for the effectiveness" goes further than its own Conclusion section.

**Murrie et al. 2020** (meta-analysis of proportions; PMC HTML; AMSTAR 2 low, provisional: item 7 is in the unopened supplement). 25 cohorts of substance-induced psychosis:
- Later schizophrenia: 25% (18–35%), I² 99%.
- Amphetamines: 22% (14–34%), 5 estimates, 2284 people, I² 96%.
- Cannabis 34%; alcohol 9%.
- No moderator was significant at the review's threshold.

Limits:
- The five amphetamine studies are not named in the article.
- The methods group cocaine with methamphetamine and amphetamine as stimulants.
- The Thai cohort (Kittirattanapaiboon 2010, 1,116 people) appears as 39% after 5 years, with only 40% of the cohort followed up.

## Claims

**cl_meth_psychosis_treatment** (0.6.0 → 0.7.0; 8 anchors: Fluyau 2 supports or qualifies, Hall 3, Chung 3 including one registry anchor). The statement keeps the network meta-analysis text, with two changes:
- the network's statement that "each trial found no significant difference" is attributed to it, with the other reviews' conflicting reading of one trial;
- the narrative reviews' side-effect sentence is replaced by trial-level figures.

Added to the statement:
- the two overlapping reviews;
- that their effect sizes are within-arm changes;
- the two placebo-controlled trials, framed as continued treatment after the acute phase;
- the usual-care trial, with its changed outcome, its ineligible participants and its attrition;
- that no trial followed people after stopping.

Other fields:
- Plain text rewritten (64 words). Population, comparator, outcome and magnitude are extended.
- GRADE levels are unchanged (very low): risk of bias −1, indirectness −1, imprecision −2. The usual-care comparison alone would deserve −2 for risk of bias; this is stated in the domain notes.
- Status **single-study → mixed** (proposed). The adjudicator's reason, that the claim rests on one network meta-analysis, no longer holds. The trials against placebo or usual care favour the drug on some outcomes and not on others, in different populations and with serious flaws. "Replicated" (three independent trials pointing the same way) is recorded as the alternative reading.
- claim_patch moves verification to metadata-verified.

**cl_meth_psychosis_course** (0.8.0 → 0.9.0; 4 anchors: Murrie 3, one with the 11-word quotation "because of convention and not because of a presumed causal link"; Chung 1, conversion 5.1%).
- The transition sentence now leads with the pooled 22% (14–34%, I² 96%) and its caveats.
- The 'if the same cohort' uncertainty is resolved: there is one Thai cohort, reported four ways by four reviews.
- The sentence saying the meta-analysis is unread is removed.
- GRADE (very low; risk of bias −1, inconsistency −1) and status (mixed) are unchanged; the reasons and domain notes are updated.

## Reporting errors that matter (details and anchors on the cards)

- **Fluyau:**
  - Table 3 confidence intervals lack minus signs (Verachai 0.2914 with 0.1514–0.7341; Farnia upper limits 0.3801 and 0.1686).
  - Farnia's direction is reversed between the text and Table 3.
  - SMDs are undefined and some exclude zero where the trial found no difference.
  - Verachai's side-effect percentages fit the arm sizes only with the drug labels swapped (2.3% = 1/44 attributed to quetiapine, n = 36).
  - Leelahanaj's side-effect denominators are 26/27, against 29/29 for completion; the text calls it a comparison with risperidone.
  - "Mean 26.16 (SD 7.61) per trial" is the per-arm figure.
  - In the placebo trial, p < 0.005 in the text vs < 0.05 in Table 3; the "dropout" figures read like retention; the side-effect scales are mismatched.
  - 'About 85%' of six trials.
  - A 2018 RCT cited in the discussion is neither included nor listed as excluded.
- **Chung:**
  - The primary outcome was switched after the trial ended and the switch is undisclosed.
  - 17% of participants were ineligible.
  - The CGI-I responder rate 15/24 is printed as 71.43% (it is 62.5%).
  - The 'Bonferroni-corrected' p (0.0009) is smaller than the uncorrected one (0.004).
  - The urine OR 14.51 (2.07–101.74) implies p ≈ 0.007, not < 0.001.
  - The sensitivity paragraph contradicts itself.
  - Sex imbalance at baseline (45% vs 83% vs 76% men; editors' χ² p < 0.001).
  - The CGI-E is undefined for unmedicated participants.
  - The BPRS-24 halving criterion does not fit a scale with a floor of 24.
  - The rater identity is ambiguous.
- **Hall:**
  - The Samiei d values assume an end-point SD of zero.
  - Farnia is described three ways.
  - Wang 2019: a 'Cox regression' on PANSS, with similar falls in the printed means.
  - Murrie's interval is misprinted as 14–24%.
  - Retention SDs of 0.40 and 0.50 days.
  - The Herbst OR of 1.29 does not match the counts (crude about 3.4).
  - A dissertation is included despite the peer-review rule, and it may overlap with Sulaiman 2013: its end PANSS (51.6) equals that trial's entry PANSS in the network meta-analysis (editors' inference).
  - Leelahanaj's d values are swapped between arms.
- **Murrie:**
  - 34,244 people in the text vs 34,224 in Table 2.
  - The 'Amphetamines' label sits beside a stimulant category that includes cocaine.
  - The follow-up range is given as '1–20 years', but entries of 0.5 and 0.0 appear (Rahm: age 0, 0% male).
  - Table 1 years differ from the reference list (Medhus 2016 vs 2015); Medhus has 29 people here vs 28 in Voce.
  - Table 1 sample sizes are whole-cohort sizes.
  - The age moderator (P = .0286) is reported despite the P < .01 threshold.

## Notes for the editor

1. Merge the four cards before applying the patch, because `validate.py` refuses anchors to unknown cards. In a scratch copy (`r19sim`), merging the cards and applying the patch gave 0 hard failures, and warnings rose by exactly 12, one per new anchor (425 → 437).
2. `check_anchor_numbers.py` does not apply to HTML anchors. A script of mine (`r19scripts/check_numbers_r19.py`) found every two-or-more-digit number in the 11 HTML anchors and all key findings in the saved page texts. The only numbers not in the source text are labelled editors' calculations or cross-references. The registry anchor was checked against the record versions in the browser.
3. **Status proposal on the treatment claim** reverses the "single-study" set by AI reader 18 earlier today, for the reason given above. If the adjudicator prefers, the patch can be applied with `status` removed from `set` and `expect`.
4. The Chung anchor on **cl_meth_psychosis_course** goes beyond the claim the table assigned to that paper (conversion 7/137 within 24 months). The editor may drop it, together with the matching sentence in the statement and magnitude.
5. AMSTAR 2 judgment calls:
   - Murrie item 4: partial-yes (the language limit is explained by resources). A strict reading gives "no"; the overall stays low either way.
   - Murrie item 7: no-information, so the overall is provisional. It would be moderate if the supplement lists the 141 excluded full texts with reasons.
   - Hall item 13: yes. The abstract is less cautious than the Conclusion; if judged "no", Hall becomes critically low.
6. Two remarks are flags, not findings:
   - In Fluyau, one peer reviewer shares the name and initial of an included trial's first author.
   - Two Hall authors have honoraria from, or employer funding by, antipsychotic manufacturers; Chung declares no conflicts (government-funded).
7. The eight shorter trial reports (Verachai, Wang 2016, Farnia, Sulaiman 2013, Samiei, Leelahanaj, Wang 2019, Wang 2020) remain unread. Farnia 2014 and Sulaiman 2013 matter most: the reviews disagree on them.
