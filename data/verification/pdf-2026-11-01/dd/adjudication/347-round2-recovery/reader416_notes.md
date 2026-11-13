# Reader416 independent source notes

Date: 2026-11-10. Fresh isolated check of all 19 frozen tasks. These notes were created from the supplied primary files and my own new extractions, renders and calculations, not from cards, earlier outputs or calculations. No claim/card files were changed. The only unavailable primary full text was task 4 (Goldberger/PMC3805449); no external retrieval was attempted.

## Source access and page mapping

All nine supplied PDFs were independently extracted with `pdftotext -layout`. All 81 PDF pages were rendered at 150 dpi. Body pages were visually checked at 150 dpi; 20 selected pages were independently rendered and inspected at 300 dpi for numerical tables/figures or their surrounding evidence. Files are under `/workspace/scratch/d1ee8d93ce58/tmp/pdfs/reader416/` in source-specific subdirectories. The complete numerical rederivations are in `reader416_calculations.json` alongside the output.

| Source | Tasks | PDF-to-printed mapping | 300 dpi PDF pages inspected |
| --- | --- | --- | --- |
| Ossiander | 1 | PDF 1–11 = printed 884–894 | 9 (Table 5) |
| Amundsen | 2 | PDF 1–6 = printed 74–79 | 3 (Fig. 2), 4 (Table 1), 5 (Table 2) |
| Landen | 3, 9 | PDF 1–6 = printed 273–278 | 4 (Table 1 and discordant cases) |
| Ruhm | 5 | PDF 1–6 = printed 1339–1344 | 3 (Table 1), 4 (Table 2) |
| Fugelstad | 8, 13 | Online-first PDF pages 1–9 are the page labels; different from version-of-record pagination | 3 (Table I), 5 (Table III and Results), 6 (Figs. 1–2) |
| Chen | 10, 15 | PDF pages 1–6 match article page labels | 2 (Methods/Results numbers), 3 (Fig. 1), 4 (Table 1) |
| Webb | 11 | PDF 1–8 = printed 67–74 | 2 (Methods), 3 (Results), 4 (Table 1) |
| Stam | 14, 18 | Accepted manuscript, 21 PDF pages; use PDF pages, not version-of-record pagination | 19 (Table 1), 20 (Table 2) |
| Davis | 17 | PDF 1–8 = printed 152–159 | 5 (marker/ratio paragraph), 8 (references 44–46) |

Gutkind and Slavova are saved primary review-article text files. I checked the Methods, relevant Results, table text, limitations and reference entries as needed. Missing figure images/supplements were not treated as read. A reference title or a review's summary is not an independently read underlying empirical study.

## Independently checked findings

### Task 1: Ossiander

Methods printed p. 885 explains verbatim entry by staff and automated WHO coding. Table 5 p. 892 gives T40.2 = 2,725 with oxycodone 1,047, morphine 648, hydrocodone 563, opiate 543, hydromorphone 269 and codeine 148. Sum = 3,218; counts cannot be exclusive. The table is a most-common-names table. Its footnote excludes generic opiate counting when a specific opiate was named. T40.4 = 521 with fentanyl 198, tramadol 153 and propoxyphene 141 (these sum to 492, demonstrating no exhaustive distribution). Confirmed.

### Task 2: Amundsen

Fig. 2 and Results: CDR/EMCDDA 822, police 562, both 455, CDR-only 367, police with CDR cause outside definition 74, no CDR match 33. Union = 929; shares = 48.98%, 39.50%, 7.97%, 3.55%. The residency versus citizenship concepts are not interchangeable: Methods says CDR covered residents; Results says 39% of unmatched people were not citizens. The proposal keeps that distinction. Table 2 odds ratios and 715/822 autopsies match. Table 1 autopsy cells for the CDR/EMCDDA population also sum to 715. The mean ages 42.7 versus 35.3 and rounded 33% versus 8% dependence/suicide match the Results. Source says neither is the correct figure, while judging CDR broader and more complete; no causal truth standard is implied. Confirmed.

### Tasks 3 and 9: Landen

Methods p. 274 has broad poisoning codes including code 305 and non-drug agents. Table 1 p. 276 gives each source 1,046, both 987, union 1,105. Computed each-source coverage 94.6606% and overlap 89.3213%; 59 discordant each way. For vital-statistics-only poisonings: 24 out of state, 13 not reported to OMI, 15 natural in OMI but 305 in vital statistics, 2 OMI coding errors, 3 undetermined-category differences, 2 other classification differences; sum 59. For OMI-only poisonings: 4 missing from vital statistics, 1 revised but not recoded, 17 other-injury, 37 natural; sum 59. Sixteen of 37 natural-coded deaths were heart-disease codes. The use/abuse wording mechanism is a Methods rule, not individual text printed for the 15 deaths. Both tasks confirmed.

### Task 4: Goldberger

No full text or source_path supplied. Access-limited not-found: **primary full text unavailable in supplied files**. I did not verify the definitions, Case 3 or cocaine coding example through another article's references or quotations. This does not establish that any of them are false or absent from an available source.

### Task 5: Ruhm

Methods p. 1340 fits separate year-specific probit models among deaths with at least one drug category specified and imputes among deaths with only T50.9. I independently transcribed all 17 any-opioid Table 1 pairs and recomputed percentage increases. Minimum = 20.8758% (2015), maximum = 35.6705% (2008); the printed 21–35% is approximate. Key pairs: 1999 8,050→10,232; 2015 33,091→39,999; heroin/synthetic 2015 19,884→23,857. Discussion says total overdose deaths do not change, only category assignments; no confidence intervals computed; missing-at-random assumption and other coding errors acknowledged. Supporting-information code/data were not available. Confirmed.

### Tasks 6, 12, 16, 19: Gutkind saved review

Methods explicitly omits study risk-of-bias appraisal. Results identifies 17 studies; search covers publications 2013–2022, data through 2019. No pooling is presented.

- Task 6: Table 2 gives Ruhm 2016 1999–2012, 2017 2008–2014 and 2018 1999–2015; all use NVSS MCOD. Buchanich is a fourth national analysis with overlapping records. These are overlapping analyses with different periods/adjustments, not independent samples or one identical estimate.
- Task 12: Quast row matches Florida 2003–2017, smaller MCOD than FMEC counts, sizeable benzodiazepine/opioid differences, smaller amphetamine differences, large end-period cocaine difference and narrowed methadone gap. The review provides no independent universal causal miss rate.
- Task 16: Mertz row gives 112 morphine-not-heroin deaths, 66% meeting heroin criteria; heroin 171→245, morphine 132→41, codeine 34→5. Arithmetic: heroin +74 versus morphine/codeine total decreases 120. No exclusive one-to-one transfer is established. Gill row gives 84/118 = 71.1864% in 2006–2010 NYC.
- Task 19: Results 2.3.1 gives morphine-only certificate wording in 44.2% of probable and 52.6% of suspected heroin classifications; heroin share 80.2→93.3%. Table 3 and ref. 38 give 38 states plus DC and January 2018–December 2019. Change = 13.1 percentage points (16.33% relative). All these are verified as review statements only.

All four tasks confirmed within those access limits; the underlying Quast, Mertz, Gill and O'Donnell empirical texts were not supplied or read.

### Task 7: Slavova saved review

Named third paragraph explicitly prints South Carolina rate 4.7→9.3 per 100,000 and specific-drug certificates 57.7→94.4% after January 2014 process changes, attributed to personal correspondence. Surrounding discussion distinguishes T40.4 and illicitly manufactured fentanyl. The explanation is not a separate empirical decomposition. Confirmed only as the saved review's report; underlying correspondence/data not supplied.

### Tasks 8 and 13: Fugelstad

Table I and Methods: inventory 1985–1996 (1,061 forensic +151 hospital =1,212), including people with a personal history of drug use problems independent of acute-poisoning causation. NMR/Stockholm Table I =1,181; Results overlap 761 plus NMR-only 419 =1,180. Results forensic overlap 734 gives inferred hospital overlap 27/151 =17.8808%, inconsistent with printed 28%. Inventory absent from NMR =451. Thirty NMR-only deaths were confirmed inventory omissions (21 residents dying elsewhere plus 9 administrative omissions); other NMR-only =389. Only 49 other cases and 7 with no cause are described; not all 389 are independently established false drug-caused deaths.

The printed sensitivity/PPV labels are reversed under simple inventory-membership denominators: 761/1,212 =62.7888% versus 761/1,180 =64.4915%, while source calls sensitivity 64.5% and PPV 62.8%. Counts are also internally inconsistent and the inventory is incomplete, so this is an apparent label reversal under a stated reference definition, not validated causal accuracy. Toxreg prose is contradictory: 317 of 454 inventory cases, followed by 43 of those 317 not in the inventory. 317/454=69.8238%; the alternative 317/(317+43)=88.0556% numerically explains the other printed accuracy measure but is not justified as a unique count reconstruction. Corrected task 8 removes the prior-card appeal and states the independent reasoning explicitly.

Task 13 Table III: amphetamine 770/1,381 =55.7567%, cocaine 53/122=43.4426%, THC 158/700=22.5714%. Capture means appearance in NMR's cause-code selection, not drug-specific naming or proof of causation. Toxreg uses ages 10–60 except both morphine/6-MAM at any age; NMR has no equivalent age limit. Table III has no period; Methods general-characteristics text says 1997–2012 but Table I gives underlying datasets 1994–2012, and Table III's Toxreg rows sum to 5,831, neither 6,448 nor 6,648. Do not infer an unambiguous Table III period. Task 13 confirmed. Fig. 2 separately gives 1994–2012 union 9,707, overlap 4,238, Toxreg-only 2,210 and NMR-only 3,259; those reconcile.

### Tasks 10 and 15: Chen

Main paper states voluntary reports from over 90% of coroners and acknowledges incomplete NPSUM case coverage. It describes the consulting toxicologist evaluating detected substances in full toxicology reports for likely involvement, and unlinked national projection from NPSUM proportions. It does not explicitly address the separate Record of Inquest conclusion entry, and does not state the toxicologist's employment status. Those unsupported details are removed or explicitly left unverified in the complete corrections.

Table 1 aggregate ONS/projected: heroin/morphine 13,471/20,323; methadone 5,752/9,444; tramadol 2,455/3,865; dihydrocodeine 1,201/1,854; codeine 1,886/2,859; fentanyl 599/887. Computed missing shares =33.7155%, 39.0936%, 36.4812%, 35.2211%, 34.0329%, 32.4690%; missing shares use projection as denominator. Heroin/morphine projection is 50.8648% above ONS. Multiple-drug detection 16,101/16,628=96.8306%.

2011 NPSUM n=416, ambiguous k=122, named n=294: ambiguous share 29.3269%; exact projection 574/(294/416)=812.1905, while source prints 813. I retain 813 as a source-reported estimate, not an exactly reproduced result. Wilson z=1.95996398454 on k/n gives ambiguous-share bounds .2515719657 to .3387495798; transform 574/(1−bound) to 766.9408–868.0524, rounding to Table 1/Results 767–868. Abstract instead prints 765–866. For 2022 source Table 1 gives 1,980 (1,894–2,074), while Results gives 1,895–2,075. Aggregate printed interval =19,382–21,358. Annual NPSUM denominators needed to regenerate other years/aggregate were not supplied, so those intervals were transcribed rather than independently validated. They omit representation/causal uncertainty.

Other internal Table 1 checks, outside the narrow endpoint claims: annual heroin/morphine point counts sum correctly to 20,323 and ONS to 13,471. The 2015 upper interval is visibly printed 2,803 despite estimate 1,727; summing the annual printed lower endpoints gives 19,384 and uppers 22,360, not the aggregate endpoints. Even replacing 2,803 with an unverified hypothetical 1,803 would give 21,360, two above the printed aggregate upper. I have not silently corrected these source values; raw data/unrounded calculations are missing. Annual undercount shares from Table 1 point estimates span approximately 28.08% (2015) to 36.87% (2018), confirming that 29%/36% are endpoints rather than the range.

Fig. 1A supports median drugs detected four→six for the combined heroin/morphine group; this does not prove each detected drug caused death or measure heroin-versus-morphine misnaming. Both tasks corrected with full replacement extraction/page/locator.

### Task 11: Webb

Methods default to accidental direct overdose after recent drug use if no evidence suggests another cause, with exclusion of intentional/no-verdict/insufficient-information cases. Researchers independently categorized cases and a medical consultant confirmed them. Counts: 802,31,40,72,18,74 sum to 1,037; 802/1,037=77.3385%; medical-condition groups total112. Aspiration mentions total42+22=64 among74 physical events, so mostly, not all, aspiration.

The supplied paper does **not** call 77% an upper limit. The Methods assumption supports a classification caveat, not an author-attributed or validated bound. Final Discussion on printed p.73 states that unreported toxicology substances may be absent or untested; this is outside the initial pp.68–70 locator. Corrected extraction and locator include that caveat and remove the unsupported upper-limit attribution. No linked official-statistics false-positive rate is established.

### Tasks 14 and 18: Stam

Accepted manuscript Methods PDF p.8 defines attribution using cause-of-death **or NCIS object-causing-death** fields. Table2 counts180,11,39,5,8 total243; coded146,8,5,0,2 total161. Heroin-attributed180+11=191, coded146+8=154, missing37. Non-heroin-attributed toxicity39+5=44, coded5. Thirty-seven wording/coding cases are described but not cross-tabulated against20 entirely uncoded cases, so separate quantitative mechanisms cannot be recovered.

National comparison Methods p.7 lists poisoning codes with T40.1, plus F11/F19 with T40.1 before2013, registrations inVictoria and occurrence2012–2013. Model includes235 toxicity+8 misadventure=243; the latter are broader than the selected underlying-cause definition even though2 have associatedT40.1. NationalT40.1 count165 includes161 model cases and4 model-excluded coincidental cases; missing82 versus net difference78. 82/243=33.7449%; net78/243=32.0988%; model count47.2727% above165. Twenty entirely uncoded cases: author judges delayed initial reporting/noABS assessment most reasonable, not an independent audit. PDFp.14 says later associated-cause toxicity-code revisions limit extrapolation. No independent causal validation of the applied model is presented. Both tasks confirmed.

### Task 17: Davis

Printed p.156 single paragraph begins “Determination of the cause of death should account for pathways of drug metabolism.” The 6-AM sentence has no attached citation. Later in the **same paragraph** ratio evidence cites44–45, with46 attached after scene-paraphernalia context. References p.159 match the three described empirical topics, but only their citations were read. The paper gives no diagnostic-accuracy estimate for the rule. Complete correction changes following-paragraph to same-paragraph and preserves the validation limitation.

## Final disposition

13 confirmed; 5 corrected (8,10,11,15,17); 0 wrong-location-only; 1 not-found (4, full text unavailable). Full results are in `out_reader416.json`, with complete replacement extracted/page/locator for each correction. No ratings, statements, cards or other project files were edited.
