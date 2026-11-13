# Independent source notes - reader417

Date: 2026-11-10. Scope: all nine frozen tasks in `tasks_reader417.json`.

I used the assigned brief/tasks/claims for context and only the exact supplied primary source paths. I did not read cards, earlier reader results, plans, logs, ledgers or calculations. I did not browse or obtain substitute full texts. I wrote only this assigned directory and `/workspace/scratch/d1ee8d93ce58/tmp/pdfs/reader417/`.

Result: 5 confirmed, 2 corrected, 1 wrong-location, 1 not-found. Corrections are complete in `out_reader417.json`. No ratings or claim/card files were changed.

## Source and page mapping

| Supplied source | Tasks | Page mapping / access |
| --- | --- | --- |
| Slavova 2019, saved article text, PMC6559129 | 1, 5 | No PDF supplied. Relevant section and references available as saved article text. |
| Hancock 2024 original PDF | 2 | PDF pages 1-4 = printed 189-192. |
| Davis 2020 original PDF | 3 | PDF pages 1-8 = printed 152-159. |
| Smiley-McDonald 2025 original PDF | 4 | PDF pages 1-9 = printed 542-550. |
| Lundberg 2026 / PMC13623016 | 6 | Explicit source_available=false and source_path=null. Primary full text unavailable in supplied files. |
| Gutkind 2025, saved article text, PMC11916924 | 7 | No PDF supplied. Methods, Table 1 text, definitions, limitations and references available. |
| Zaychik 2024 original PDF | 8 | PDF pages 1-7 = article pages 1-7. |
| Sumnall 2023 original PDF | 9 | PDF pages 1-12 = article pages 1-12. |

Own PDF text extractions and page renders are under the allowed temporary directory. All original PDFs were independently extracted using `pdftotext -layout`. Body pages were rendered at 150 dpi; pages containing the relevant numeric tables/figure were also rendered at 300 dpi.

Visually inspected relevant images include Hancock PDF 1, 3, 4 at 150 dpi and PDF 2 at 300 dpi; Davis PDF 2 and 7 at 150 dpi; Smiley-McDonald PDF 2, 5, 6, 7 at 150 dpi and PDF 3 at 300 dpi; Zaychik PDF 3, 4 at 150 dpi and PDF 2, 5 at 300 dpi; Sumnall PDF 3, 4, 5, 9 at 150 dpi and PDF 6 at 300 dpi. Generated but uninspected other page images were not used as independent visual evidence.

## Per-task source checks

1. **Slavova / testing change - confirmed as review reporting.** The third paragraph of Methodologic Considerations (saved-text line 73) explicitly describes routine Kentucky gabapentin testing beginning July 2014, the 2.9% (2013) and 17% (2014) prevalence figures, and the warning about gradual procedural improvements. Reference 45 identifies Hargrove et al. 2018. No underlying case counts are present to recalculate the percentages. This is detected gabapentin among people who died of overdose, not proof that gabapentin caused their deaths. The Hargrove paper itself was not read.

2. **Hancock / toxicology and other studies - confirmed.** Methods paragraph 5 on printed 190 defines the false-negative group using toxicology and absence of significant autopsy findings. Its phrase "very low or suspicion" is a source typo, while the Results and Table 1 clearly describe no suspicion for the 115 cases. The Discussion first paragraph on printed 191 continues across columns and reports the majority-correct narrative, 11%-13% negative-toxicology/other-cause summary, and three pathologists assessing 60 selected cases from 629 with 75%-80% correct cause and manner. Original studies cited there were not supplied or read. The source's first Results paragraph mistakenly labels the 2569/387 final margins as preliminary suspicion; Table 1 and the case descriptions support preliminary totals 2719/237. A negative toxicology result is part of the false-positive definition, so 265/2719 cannot quantify the incremental value of internal examination alone. Assigned-pathologist correctness and contribution of any illicit drug except catastrophic findings are acknowledged assumptions on printed 192.

3. **Davis / accuracy and delayed deaths - confirmed, with surrounding wording caveat.** Printed 153 Question 1 paragraph 1 cites Dye 2019 for reduced accuracy even where scene findings suggest overdose; no accuracy percentage is supplied for that citation. Paragraph 5 allows deferral in a selected delayed-death subset, still requiring postmortem investigation, hospital-record review and efforts to seek admission samples. The 20%-30% statement has a different reference set, 6 and 8-13. Reference 15 on printed 158 is the same Dye study summarized in Hancock, not an additional independent primary accuracy study read in this check. Any surrounding shorthand should preserve the possibility of deferral in selected delayed deaths rather than a universal exception.

4. **Smiley-McDonald / access qualifications - confirmed.** Discussion paragraph 1 starts at printed 546 bottom right and continues at printed 547 top left. The authors distinguish possible processing elsewhere for offices reporting no access from a rural/frontier low-caseload explanation for offices saying services are not necessary. The roughly 300 offices with five or fewer deaths are an author-reported analysis without underlying case-level office data in this PDF. Table 1 independently supports about 83% access and over one in ten reporting none. Printed 548 says the annual number of suspected overdoses receiving toxicology is unknown and discusses non-response imputation and interpretation/skip-pattern concerns. These are office capability shares, not shares of deaths lacking toxicology.

5. **Slavova / undetermined intent - wrong-location.** All quoted intent figures and the policy explanation are in the fourth paragraph of Methodologic Considerations (line 75). The first paragraph (line 69) concerns drugs named, not the intent figures. The corrected locator retains the fourth paragraph only and names references 10, 31 and 44. The review does not identify the individual states' system types in this paragraph. The original Warner analysis and WONDER data were not read. Warner 2013 is also summarized in Gutkind Table 1; these summaries are not independent underlying studies.

6. **Lundberg - not-found/pending.** Primary full text unavailable in supplied files. I did not check a substitute source. Definitions, states' systems, fixed state indicators, no-within-state-contrast inference and significance of recorded testing cannot be confirmed or disproved here. All source-dependent surrounding Lundberg assertions remain pending.

7. **Gutkind / Warner row - confirmed as scoping-review reporting.** Table 1's Warner row (saved-text lines 103-108) gives national NVSS multiple-cause-of-death data, 2008-2010; undetermined death specification varied by state but not system; drug specification varied by both. The table definition (line 111) distinguishes undetermined intent from an unspecified drug. The Methods describe two independent reviewers and no formal risk-of-bias assessment. No underlying Warner full text was supplied or read, and no causal or correctness conclusion follows from these review statements.

8. **Zaychik / system mix, pooled model and graph - corrected.** Table 1 lists nine switch states; Methods exclude Delaware and Florida. The retained seven give 2 justices-of-peace systems, 2 coroners, 1 physician coroner, 1 locally appointed physician and 1 magistrate coroner. The single DID equation is fitted over three windows; the paper does not state a within-state repeated-observation error adjustment. Figure 1 shows differing relative levels and descriptive trajectories, not estimated state-specific reform effects. New Jersey is above New York after its switch. New Mexico is below Idaho after the switch; West Virginia is below Indiana in most later post-switch years but briefly above just after the switch. Massachusetts is already below Pennsylvania before reform. Arizona/Nevada move broadly together. Results paragraph 1 attributes the sharp shared first-four-pair drops to ICD-9 coding, not reform. These facts warrant qualifying the inference that a pooled estimate has averaged different causal effects. No test of such effect heterogeneity is reported.

9. **Sumnall / reversed means and F interpretation - corrected.** Table 1 at 300 dpi confirms the cell values transcribed in the calculation script. The narrative's older-younger direction is consistent with the table and reversed relative to the printed mean order. All proposed approximate F numbers are reproducible with a conventional contrast calculation. That does not identify the exact printed F=4.8: the table header counts sum to 1248, while a full eight-cell model with residual df=1230 would imply 1238 observations. The article does not resolve the discrepancy; a df error is also possible, so ten exclusions should not be assumed as established. Rounded descriptive summaries and unmatched sample sizes cannot replace raw analytic output. An interaction-label error is plausible, but must stay an editorial diagnostic. The age contrast also changes use history. Supplementary S1/S2 and underlying individual data were not supplied/read. The page 9 discussion itself also has an inconsistent reference to heroin before saying the interaction was only evident in ecstasy stories.

## Independent calculations

The reproducible script and machine-readable values are `calculations_reader417.py` and `calculations_reader417.json`. Inputs were transcribed from my own page images, not an existing ledger.

### Hancock Table 1

| Preliminary suspicion | Final drug cause | Final other cause | Total |
| --- | ---: | ---: | ---: |
| Suspected | 2454 | 265 | 2719 |
| Not suspected | 115 | 122 | 237 |
| Total | 2569 | 387 | 2956 |

- 265/2719 = 9.74623%; Wilson 95% interval 8.68757%-10.91847%.
- 115/237 = 48.52321%; Wilson 95% interval 42.23478%-54.85875%.
- Sensitivity 2454/2569 = 95.52355%; specificity 122/387 = 31.52455%.
- The source's false-negative fraction uses 115/2569 = 4.47645%, a different denominator from the 48.5% editorial calculation.

### Smiley-McDonald Table 1

Access is (78+1012)/1320 = 82.57576%; no access 148/1320 = 11.21212%; not necessary 82/1320 = 6.21212%. The separate screening/confirmation text gives 715/1326 = 53.92157% and 674/709 = 95.06347%. No office totals can be turned into a death-level testing proportion.

### Zaychik Table 4

Normal approximate 95% intervals using the rounded estimate and SE, estimate +/- 1.959964*SE:

| Window | DID | SE | Editorial approximate interval |
| --- | ---: | ---: | --- |
| 31 years | -0.02 | 0.04 | -0.09840 to 0.05840 |
| 10 years post | -0.03 | 0.05 | -0.12800 to 0.06800 |
| 5 years post | -0.02 | 0.06 | -0.13760 to 0.09760 |

These reproduce the rounded intervals in the surrounding claim. They condition on the printed SEs. No corrected variance for repeated state observations can be computed from this PDF, and its direction is not established solely by noting the missing adjustment.

### Sumnall Table 1

Header n: 158, 155, 155, 154, 155, 158, 156, 157 (sum 1248).

Harm-support means: 22.9, 22.4, 23.1, 23.5, 24.0, 23.8, 22.9, 23.6.

Harm-support SDs: 5.1, 5.7, 5.4, 4.0, 4.6, 4.7, 5.2, 4.5.

| Weighted collapse | Younger mean | Older mean |
| --- | ---: | ---: |
| All drugs | 22.973794 | 23.575080 |
| Ecstasy | 22.652396 | 23.899042 |
| Heroin | 23.299353 | 23.251118 |

Within-cell SSE = sum((n_i-1)*SD_i^2) = 30102.64; nominal df from header counts = 1240; MSE = 24.27632258; pooled within-cell SD = 4.92710083.

For any contrast c across the eight cell means, F = (sum(c_i*mean_i))^2 / (MSE*sum(c_i^2/n_i)). Equal weighting across the relevant gender cells gives:

| Contrast | Estimate | Approximate F |
| --- | ---: | ---: |
| Older minus younger, averaged across drug/gender | 0.60 | 4.626351 |
| Difference of the ecstasy and heroin age contrasts | 1.30 | 5.429537 |
| Older minus younger within ecstasy | 1.25 | 10.071904 |
| Older minus younger within heroin | -0.05 | 0.016013 |

These are approximate diagnostics using rounded values and table header n. They do not reproduce the unexplained analytic sample. The source's F=4.8 is numerically nearer the reconstructed interaction; the exact test identity is pending analytic data/output.

The older-younger harm-support d from the weighted collapses is 0.121919. Approximate stigma d values from the printed marginal means and equal-weight pooled marginal SDs are 0.17810 (man/woman), 0.35894 (older/younger), and 0.39450 (heroin/ecstasy). Table 2 stigma regression df imply 17+850+1 = 868 observations, and the R-squared increments sum .068+.016+.234+.251 = .569. These confirm the stated editorial magnitudes without extending the randomized interpretation to participant-trait associations.
