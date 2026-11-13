# AI reader 5: first reading of four PDFs (2026-10-16)

Cards (all pass `check_card.py`, no warnings) are in `data/study-cards/_incoming/methamphetamine/`: `sc_ersche_2012.json`, `sc_callaghan_2012.json`, `sc_cruickshank_2009.json`, `sc_anthony_1994.json`. The claim patch is `reader5_patch.json` in this folder. It passes `claim_patch.py --dry-run` and has not been applied. It was also simulated on a scratch copy of the claims: schema, GRADE arithmetic, language and the one-quotation rule are clean, and `check_anchor_numbers.py` found all 81 numbers in the four anchors on the stated pages.

## Ersche et al. 2012 (Science 335, 601–604)
**What it shows.** The study compared 50 sibling pairs (one sibling with DSM-IV stimulant dependence, the other with no chronic drug or alcohol abuse) with 50 controls matched for age and IQ. Both siblings had longer stop-signal reaction times (F(2,141) = 9.9) and lower white-matter FA (F(2,141) = 26.3) than the controls. They also shared three grey-matter clusters: a larger left amygdala, a larger left putamen, and smaller volume across the left postcentral gyrus, superior temporal gyrus and posterior insula. Permutation tests found FA, the putamen and the insula more alike within families than in random pairs; the amygdala was not.

**Design limits.** Nothing was measured before drug use began. Siblings share environment as well as genes. Sex, education and other drug use are not reported in the main text, and smoking was more common in both sibling groups. The degrees of freedom imply 144 of 150 participants were analysed. The two siblings are never compared directly.

**What it changes.** I appraised it with ROBINS-E: high overall, provisionally, because the Supporting Online Material is not in the PDF and was not read. The claim's hippocampal, orbitofrontal and anterior insular findings come from London et al. (2015), not from the main report. My wording attributes them to that review and adds the shared reductions that the claim left out. I recorded the design as cross-sectional rather than case-control. Risk of bias is now downgraded one level; certainty stays very low. **The editor needs the Supporting Online Material PDF (tables S1–S3, figs. S1–S2) to finish the card.**

## Callaghan et al. 2012 (Drug Alcohol Depend 120, 35–40)
**What it shows.** This is a California record-linkage cohort, 1990–2005, of people aged 30 or over, excluding anyone with an alcohol, other drug or HIV code. Against 40,358 matched appendicitis patients: 51 vs 29 Parkinson's diagnoses, HR 1.76 (1.12–2.76 in the Results and Table 4; the abstract prints 1.12–2.75). Against cocaine: HR 2.41 (abstract 2.44). Cocaine against appendicitis: HR 1.04 (0.56–1.93). Diagnoses came at a younger median age in the exposed cohort (57.2 vs 63.8). In absolute terms, about 0.13% vs 0.07% over about 6 years (editors' calculation).

**Design limits.** Exposure and outcome are unvalidated codes. Smoking and antipsychotic exposure are not recorded. The cohorts were matched on later admissions, a post-exposure variable. The numbers excluded are not reported. ROBINS-E: high.

**What it changes.** The California data in `cl_meth_parkinson` now come from the primary paper rather than through Kish et al. (2017), which carries the abstract's interval. The patch adds counts, absolute risks, the cocaine comparisons and the younger age at diagnosis, and labels the Utah-only sentences as such. Status stays replicated (two independent cohorts); certainty stays very low.

## Cruickshank & Dyer 2009 (Addiction 104, 1085–1099)
**What it shows.** A narrative review based on a documented PubMed search, with selection by the authors' judgment and no appraisal of what it cites. Its overdose section (p. 1088) lists common features from case reports: agitation, dilated pupils, tachycardia, hypertension and rapid respiration. Hyperpyrexia appears only among the less common features and among causes of death. For non-fatal presentations it gives second-hand frequencies without denominators: agitation about 20%, suicidal ideation 6–12%, psychosis 7–12%, rhabdomyolysis up to 14%, seizures 3–4%. Several of its sources concern amphetamine. It reports no case fatality. It cites forensic series suggesting that many methamphetamine-related deaths are accidents, suicide or homicide.

**Design limits.** Editors' narrative-review checklist: high.

**What it changes.** The claim said its description came from the abstract, but the abstract does not mention overdose. Hyperthermia was listed among the main presenting features and the claim described a progression the review does not describe. The patch rewords this, adds the second-hand frequencies and the forensic point, and downgrades indirectness one level for second-hand evidence (METHODS §6.3). Certainty stays very low and the claim stays at draft.

## Anthony, Warner & Kessler 1994 (Exp Clin Psychopharmacol 2, 244–268)
**What it shows.** The National Comorbidity Survey, 1990–1992: n = 8,098, response rate 82.4%, lay-administered CIDI, DSM-III-R criteria. Of people who had ever used psychostimulants other than cocaine extramedically (examples given: dextroamphetamine, methamphetamine), 11.2% (SE 1.6) had ever been dependent. The comparable figures are 31.9% for tobacco (no SE, a different method), 15.4% for alcohol, 16.7% for cocaine, 23.1% for heroin and 9.1% for cannabis. The stimulant proportion was 6.5–7.7% at ages 35–54. I checked every value against the page images, because the PDF's text layer is OCR.

**Design limits.** The figure is a snapshot among everyone who had ever used, not a risk after starting. The class is not methamphetamine. The frame excludes institutionalized and unhoused people. JBI: low.

**What it changes.** The claim's only figure was a direction "according to its abstract", but the abstract gives no stimulant figure. The patch restores the Table 2 figures and adds the authors' 14-word conclusion as the claim's one quotation. It removes the provisional risk-of-bias downgrade; that is a judgment for the senior author, and certainty stays very low because indirectness takes two levels.

## Reporting errors noticed in the papers
1. Ersche: F(2,141) for SSRT and FA implies 144 of 150 participants analysed, and the exclusions are unexplained (p. 602).
2. Ersche: r = 0.24 is printed without its sign, although the relation described is negative (p. 602).
3. Ersche: the abstract's "fronto-striatal" summary is broader than the shared clusters (pp. 601–603).
4. Ersche: the six familiality permutation tests are uncorrected; three would fail a Bonferroni threshold (editors' calculation).
5. Callaghan: the abstract and the Results/Table 4 disagree on the appendicitis HR's interval and p value (2.75 and 0.017 vs 2.76 and 0.014) and on the cocaine HR (2.44 vs 2.41) (pp. 35, 38–39).
6. Callaghan: in Table 1 the matched exposed cohort has 29,940 White members, more than the 29,578 in the full cohort, and its race counts sum to 40,808, not 40,358. The digits are probably transposed from 29,490 (p. 37).
7. Callaghan: the exclusion counts and the method behind the 10-year projection are not given (pp. 36, 38).
8. Cruickshank: dopamine-transporter deficits are printed as "20–30% of normal levels"; the argument needs reductions of 20–30% (p. 1093).
9. Cruickshank, Table 1: footnote a is misplaced on the intranasal half-life, and the intravenous Tmax is printed as 6 ± 11 min (p. 1087).
10. Cruickshank: the text gives 4 h for intranasal Tmax, Table 1 gives 169 min (p. 1087).
11. Cruickshank, Table 3: the blood-pressure mechanism repeats the heart-rate text (p. 1089).
12. Cruickshank: one source cited for clinical frequencies (Derlet et al., 1990) is titled as a study of protection against d-amphetamine toxicity (p. 1088).
13. Anthony: "20–40%" for drugs with known dependence liability conflicts with Table 2's 16.7% for cocaine (p. 263).
14. Anthony: heroin use prevalences (2.7% vs 0.7%) are called dependence (p. 261).
15. Anthony: analgesic figures are cited to Table 3 instead of Table 2 (p. 255).
16. Anthony: the text says sex differences were found "only for alcohol and cannabis", which contradicts the anxiolytic figures on p. 255 and in Table 5; the stimulant difference (9.7% vs 13.3%) is never discussed (p. 264).
17. Anthony: the threshold for asking the dependence questions is described two ways (pp. 247–248).
18. Anthony: the tobacco footnote's n = 4,414 can be misread, and Tables 2 and 4 order their columns differently.

## Notes for the editor
- **Anchor-number check.** The Ersche PDF has a one-page reprint cover sheet before p. 601. `check_anchor_numbers.py` therefore reads every page one off unless the cover page is dropped from the text extraction. With it left in, three correct numbers are reported missing. I ran the check with `pdftotext -f 2`.
- **Units in Cruickshank.** The text layer renders µg/l as "mg/l". The printed pages show µg/l, and the card says so.
- **Not changed.** I did not alter the Utah-based sentences of `cl_meth_parkinson`, apart from labelling them as Utah and the two cross-cohort clauses. I did not restore the stop-signal finding to `cl_meth_siblings`, whose outcome is brain structure. The longer SSRT shared by both siblings is on the card if the editor wants it back.
