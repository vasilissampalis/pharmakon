# Psilocybin — evidence map and PDF list (v0.1, 2026-10-15)

All DOIs below come from Crossref API responses retrieved on 2026-10-15 (never from memory). Each row's DOI, title, journal and year were returned by Crossref for that record. DOIs marked ◆ were additionally confirmed by a `filter=doi:` record fetch that also returned the `updated-by` field (retraction/erratum check); the remaining rows come from Crossref bibliographic *search* responses in the same session, which is the same metadata source. Retraction check: none retracted. Two items carry published corrections (items 8 and 36) and are marked. Save each PDF into `PDFs/Psilocybin/` with the filename given; cross-cutting papers go in `PDFs/_Cross-cutting/`.

How this list was built: (1) the four depression RCTs named in the brief and their published critiques, reanalyses and secondary papers; (2) section-level Crossref bibliographic searches (strings in `Psilocybin_search-log.md`); (3) screening by title and journal — conference abstracts (Neuroscience Applied, Eur Neuropsychopharmacol, Biol Psychiatry supplements), news items, predatory-looking venues and preclinical-only papers dropped.

Context note for the senior author: Crossref answered roughly half of all calls in this build with HTTP 429 on the shared egress. Per the brief, each refusal was followed by a 95–185 s pause and the refused URL was never re-fetched. One landmark could not be verified at all and is listed under "Known gaps" instead of in the table.

**Work through the list in order. Tier A first.**

---

## Tier A — needed now (landmark trials, their critiques, backbone reviews, dose–response and safety)

| # | Paper | Journal, year | DOI | Save as |
|---|---|---|---|---|
| 1 | Carhart-Harris et al. — Trial of psilocybin versus escitalopram for depression | NEJM 2021 | 10.1056/nejmoa2032994 | CarhartHarris_2021_PsilocybinVsEscitalopram.pdf |
| 2 | Goodwin et al. — Single-dose psilocybin for a treatment-resistant episode of major depression (COMP360 phase IIb) ◆ | NEJM 2022 | 10.1056/nejmoa2206443 | Goodwin_2022_SingleDoseTRD.pdf |
| 3 | Raison et al. — Single-dose psilocybin treatment for major depressive disorder ◆ | JAMA 2023 | 10.1001/jama.2023.14530 | Raison_2023_SingleDoseMDD.pdf |
| 4 | Davis et al. — Effects of psilocybin-assisted therapy on major depressive disorder | JAMA Psychiatry 2021 | 10.1001/jamapsychiatry.2020.3285 | Davis_2021_PsilocybinAssistedTherapyMDD.pdf |
| 5 | Szigeti et al. — Assessing expectancy and suggestibility in a trial of escitalopram v. psilocybin for depression (critique) | Psychol Med 2024 | 10.1017/s0033291723003653 | Szigeti_2024_ExpectancySuggestibility.pdf |
| 6 | Weiss et al. — A critical evaluation of QIDS-SR-16 using data from a trial of psilocybin therapy versus escitalopram (critique) | J Psychopharmacol 2023 | 10.1177/02698811231167848 | Weiss_2023a_QIDSCritique.pdf |
| 7 | Nayak et al. — A Bayesian reanalysis of a trial of psilocybin versus escitalopram for depression (reanalysis) | Psychedelic Med 2023 | 10.1089/psymed.2022.0002 | Nayak_2023_BayesianReanalysis.pdf |
| 8 | Gukasyan et al. — On blinding and suicide risk in a recent trial of psilocybin-assisted therapy for treatment-resistant depression (critique of item 2) | Med 2023 | 10.1016/j.medj.2022.12.003 | Gukasyan_2023_BlindingAndSuicideRisk.pdf |
| 9 | Muthukumaraswamy, Forsyth & Lumley — Blinding and expectancy confounds in psychedelic randomized controlled trials | Expert Rev Clin Pharmacol 2021 | 10.1080/17512433.2021.1933434 | Muthukumaraswamy_2021_BlindingExpectancyConfounds.pdf |
| 10 | Schenberg et al. — Who is blind in psychedelic research? (letter replying to item 9) | Expert Rev Clin Pharmacol 2021 | 10.1080/17512433.2021.1951473 | Schenberg_2021_WhoIsBlindLetter.pdf |
| 11 | Szigeti & Heifets — Expectancy effects in psychedelic trials | Biol Psychiatry Cogn Neurosci Neuroimaging 2024 | 10.1016/j.bpsc.2024.02.004 | Szigeti_2024b_ExpectancyEffects.pdf |
| 12 | Huneke et al. — Expectancy effects, failure of blinding integrity, and placebo response in trials of treatments for psychiatric disorders | JAMA Psychiatry 2025 | 10.1001/jamapsychiatry.2025.0085 | Huneke_2025_BlindingIntegrityPlacebo.pdf |
| 13 | Nayak et al. — Out of control: blinding, dose response, and psychosocial controls in psychedelic trials | J Psychopharmacol 2025 | 10.1177/02698811251368367 | Nayak_2025_OutOfControl.pdf |
| 14 | Hinkle et al. — Adverse events in studies of classic psychedelics: a systematic review and meta-analysis | JAMA Psychiatry 2024 | 10.1001/jamapsychiatry.2024.2546 | Hinkle_2024_AdverseEventsSRMA.pdf |
| 15 | Breeksema et al. — Adverse events in clinical treatments with serotonergic psychedelics and MDMA: a mixed-methods systematic review | J Psychopharmacol 2022 | 10.1177/02698811221116926 | _Cross-cutting/Breeksema_2022_AdverseEventsMixedMethods.pdf |
| 16 | Roscoe & Lozy — Can psilocybin be safely administered under medical supervision? A systematic review of adverse event reporting | Drug Sci Policy Law 2022 | 10.1177/20503245221085222 | Roscoe_2022_AdverseEventReportingSR.pdf |
| 17 | Johnson, Richards & Griffiths — Human hallucinogen research: guidelines for safety | J Psychopharmacol 2008 | 10.1177/0269881108093587 | _Cross-cutting/Johnson_2008_SafetyGuidelines.pdf |
| 18 | Griffiths et al. — Psilocybin can occasion mystical-type experiences having substantial and sustained personal meaning and spiritual significance ◆ | Psychopharmacology 2006 | 10.1007/s00213-006-0457-5 | Griffiths_2006_MysticalTypeExperiences.pdf |
| 19 | Griffiths et al. — Psilocybin occasioned mystical-type experiences: immediate and persisting dose-related effects | Psychopharmacology 2011 | 10.1007/s00213-011-2358-5 | Griffiths_2011_DoseRelatedEffects.pdf |
| 20 | Hasler et al. — Acute psychological and physiological effects of psilocybin in healthy humans: a double-blind, placebo-controlled dose–effect study | Psychopharmacology 2004 | 10.1007/s00213-003-1640-6 | Hasler_2004_DoseEffectHealthyHumans.pdf |
| 21 | Hasler et al. — Determination of psilocin and 4-hydroxyindole-3-acetic acid in plasma by HPLC-ECD and pharmacokinetic profiles of oral and intravenous psilocybin in man | Pharm Acta Helv 1997 | 10.1016/s0031-6865(97)00014-9 | Hasler_1997_OralIVPharmacokinetics.pdf |
| 22 | Otto et al. — Clinical pharmacokinetics of psilocin after psilocybin administration: a systematic review and post-hoc analysis (correction published; obtain both) | Clin Pharmacokinet 2025 | 10.1007/s40262-024-01454-4 | Otto_2025_PsilocinPKSystematicReview.pdf |
| 23 | Studerus, Kometer, Hasler & Vollenweider — Acute, subacute and long-term subjective effects of psilocybin in healthy humans: a pooled analysis of experimental studies | J Psychopharmacol 2010 | 10.1177/0269881110382466 | Studerus_2010_PooledAnalysisSubjectiveEffects.pdf |
| 24 | Studerus, Gamma, Kometer & Vollenweider — Prediction of psilocybin response in healthy volunteers | PLoS ONE 2012 | 10.1371/journal.pone.0030800 | Studerus_2012_PredictionOfResponse.pdf |
| 25 | Johnson et al. — Psilocybin dose-dependently causes delayed, transient headaches in healthy volunteers | Drug Alcohol Depend 2012 | 10.1016/j.drugalcdep.2011.10.029 | Johnson_2012_DelayedHeadaches.pdf |
| 26 | Carbonaro et al. — Survey study of challenging experiences after ingesting psilocybin mushrooms: acute and enduring positive and negative consequences | J Psychopharmacol 2016 | 10.1177/0269881116662634 | Carbonaro_2016_ChallengingExperiencesSurvey.pdf |
| 27 | Barrett, Bradstreet, Leoutsakos, Johnson & Griffiths — The Challenging Experience Questionnaire: characterization of challenging experiences with psilocybin mushrooms | J Psychopharmacol 2016 | 10.1177/0269881116678781 | Barrett_2016_ChallengingExperienceQuestionnaire.pdf |
| 28 | Evans et al. — Extended difficulties following the use of psychedelic drugs: a mixed methods study | PLOS ONE 2023 | 10.1371/journal.pone.0293349 | Evans_2023_ExtendedDifficulties.pdf |
| 29 | Simonsson et al. — Adverse health outcomes of psilocybin, LSD, MDMA, ibogaine and 5-MeO-DMT | JAMA Netw Open 2026 | 10.1001/jamanetworkopen.2026.36756 | _Cross-cutting/Simonsson_2026_AdverseHealthOutcomes.pdf |
| 30 | Malcolm & Thomas — Serotonin toxicity of serotonergic psychedelics | Psychopharmacology 2021 | 10.1007/s00213-021-05876-x | _Cross-cutting/Malcolm_2021_SerotoninToxicity.pdf |

## Tier B — section backbone (mechanism, neuroimaging, secondary analyses, therapeutic trials in other indications)

| # | Paper | Journal, year | DOI | Save as |
|---|---|---|---|---|
| 31 | Carhart-Harris et al. — Neural correlates of the psychedelic state as determined by fMRI studies with psilocybin ◆ | PNAS 2012 | 10.1073/pnas.1119598109 | CarhartHarris_2012_NeuralCorrelatesPsychedelicState.pdf |
| 32 | Siegel et al. — Psilocybin desynchronizes the human brain ◆ | Nature 2024 | 10.1038/s41586-024-07624-5 | Siegel_2024_PsilocybinDesynchronizesBrain.pdf |
| 33 | Daws et al. — Increased global integration in the brain after psilocybin therapy for depression ◆ | Nat Med 2022 | 10.1038/s41591-022-01744-z | Daws_2022_GlobalIntegration.pdf |
| 34 | Deco et al. — Different hierarchical reconfigurations in the brain by psilocybin and escitalopram for depression | Nat Ment Health 2024 | 10.1038/s44220-024-00298-y | Deco_2024_HierarchicalReconfigurations.pdf |
| 35 | Madsen et al. — Plasma psilocin critically determines behavioral and neurobiological effects of psilocybin | Neuropsychopharmacology 2020 | 10.1038/s41386-020-00823-4 | Madsen_2020_PlasmaPsilocinDeterminesEffects.pdf |
| 36 | Weiss et al. — Personality change in a trial of psilocybin therapy v. escitalopram treatment for depression (corrigendum 10.1017/s0033291723002039 published; obtain both) | Psychol Med 2023 | 10.1017/s0033291723001514 | Weiss_2023b_PersonalityChange.pdf |
| 37 | Erritzoe et al. — Effect of psilocybin versus escitalopram on depression symptom severity: observational 6-month follow-up of a phase 2 trial | eClinicalMedicine 2024 | 10.1016/j.eclinm.2024.102799 | Erritzoe_2024a_SixMonthFollowUp.pdf |
| 38 | Erritzoe et al. — Effects of discontinuation of serotonergic antidepressants prior to psilocybin therapy versus escitalopram for major depression | J Psychopharmacol 2024 | 10.1177/02698811241237870 | Erritzoe_2024b_AntidepressantDiscontinuation.pdf |
| 39 | Barba et al. — Effects of psilocybin versus escitalopram on rumination and thought suppression in depression | BJPsych Open 2022 | 10.1192/bjo.2022.565 | Barba_2022_RuminationThoughtSuppression.pdf |
| 40 | Martens et al. — Negative affective bias in depression following treatment with psilocybin or escitalopram | Transl Psychiatry 2025 | 10.1038/s41398-025-03693-w | Martens_2025_NegativeAffectiveBias.pdf |
| 41 | Henry et al. — The effects of psilocybin therapy versus escitalopram on cognitive bias | Eur Neuropsychopharmacol 2025 | 10.1016/j.euroneuro.2025.06.003 | Henry_2025_CognitiveBias.pdf |
| 42 | Griffiths et al. — Psilocybin produces substantial and sustained decreases in depression and anxiety in patients with life-threatening cancer: a randomized double-blind trial ◆ | J Psychopharmacol 2016 | 10.1177/0269881116675513 | Griffiths_2016_CancerAnxietyDepressionRCT.pdf |
| 43 | Ross et al. — Rapid and sustained symptom reduction following psilocybin treatment for anxiety and depression in patients with life-threatening cancer ◆ | J Psychopharmacol 2016 | 10.1177/0269881116675512 | Ross_2016_CancerAnxietyDepressionRCT.pdf |
| 44 | Johnson et al. — Pilot study of the 5-HT2A-receptor agonist psilocybin in the treatment of tobacco addiction ◆ | J Psychopharmacol 2014 | 10.1177/0269881114548296 | Johnson_2014_TobaccoPilot.pdf |
| 45 | Garcia-Romeu, Griffiths & Johnson — Psilocybin-occasioned mystical experiences in the treatment of tobacco addiction | Curr Drug Abuse Rev 2015 | 10.2174/1874473708666150107121331 | GarciaRomeu_2015_MysticalExperiencesTobacco.pdf |
| 46 | Bogenschutz et al. — Percentage of heavy drinking days following psilocybin-assisted psychotherapy vs placebo in adults with alcohol use disorder ◆ | JAMA Psychiatry 2022 | 10.1001/jamapsychiatry.2022.2096 | Bogenschutz_2022_AlcoholUseDisorderRCT.pdf |
| 47 | Luquiens et al. — Psilocybin in alcohol use disorder and comorbid depressive symptoms: results from a feasibility randomized clinical trial | Addiction 2025 | 10.1111/add.70152 | Luquiens_2025_AUDFeasibilityRCT.pdf |
| 48 | Kase et al. — Effects of LSD, DMT and psilocybin on cognitive and psychological functions: a systematic review | J Psychopharmacol 2026 | 10.1177/02698811251412012 | _Cross-cutting/Kase_2026_CognitivePsychologicalSR.pdf |
| 49 | Barrett, Johnson & Griffiths — Validation of the revised Mystical Experience Questionnaire in experimental sessions with psilocybin | J Psychopharmacol 2015 | 10.1177/0269881115609019 | Barrett_2015_MEQ30Validation.pdf |
| 50 | MacLean, Leoutsakos, Johnson & Griffiths — Factor analysis of the Mystical Experience Questionnaire | J Sci Study Relig 2012 | 10.1111/j.1468-5906.2012.01685.x | MacLean_2012_MEQFactorAnalysis.pdf |
| 51 | MacLean, Johnson & Griffiths — Mystical experiences occasioned by psilocybin lead to increases in the personality domain of openness | J Psychopharmacol 2011 | 10.1177/0269881111420188 | MacLean_2011_OpennessIncrease.pdf |
| 52 | Barrett, Johnson & Griffiths — Neuroticism is associated with challenging experiences with psilocybin mushrooms | Pers Individ Dif 2017 | 10.1016/j.paid.2017.06.004 | Barrett_2017_NeuroticismChallengingExperiences.pdf |
| 53 | Carbonaro, Johnson, Hurwitz & Griffiths — Double-blind comparison of the two hallucinogens psilocybin and dextromethorphan: similarities and differences in subjective experiences | Psychopharmacology 2017 | 10.1007/s00213-017-4769-4 | Carbonaro_2017_PsilocybinVsDextromethorphan.pdf |
| 54 | Nichols — Commentary on: Psilocybin can occasion mystical-type experiences (critique of item 18) | Psychopharmacology 2006 | 10.1007/s00213-006-0458-4 | Nichols_2006_CommentaryOnGriffiths.pdf |
| 55 | Snyder — Commentary on: Psilocybin can occasion mystical-type experiences (critique of item 18) | Psychopharmacology 2006 | 10.1007/s00213-006-0459-3 | Snyder_2006_CommentaryOnGriffiths.pdf |
| 56 | Kleber — Commentary on: Psilocybin can occasion mystical-type experiences (critique of item 18) | Psychopharmacology 2006 | 10.1007/s00213-006-0461-9 | Kleber_2006_CommentaryOnGriffiths.pdf |
| 57 | Schuster — Commentary on: Psilocybin can occasion mystical-type experiences (critique of item 18) | Psychopharmacology 2006 | 10.1007/s00213-006-0460-x | Schuster_2006_CommentaryOnGriffiths.pdf |
| 58 | Tai et al. — A randomized crossover trial comparing the acute physiological and psychological effects of botanical oral psilocybin, oral psilocin and sublingual psilocin | J Psychopharmacol 2026 | 10.1177/02698811261478603 | Tai_2026_OralVsSublingualPsilocin.pdf |

## Tier C — prolonged difficulties, epidemiology, poisonings, analogues, interactions, measurement

| # | Paper | Journal, year | DOI | Save as |
|---|---|---|---|---|
| 59 | Robinson et al. — An investigation into the varieties of extended difficulties following psychedelic drug use | J Psychedelic Stud 2025 | 10.1556/2054.2024.00420 | Robinson_2025_VarietiesOfExtendedDifficulties.pdf |
| 60 | Argyri et al. — Practitioner perspectives on extended difficulties and optimal support strategies | Harm Reduct J 2025 | 10.1186/s12954-025-01347-0 | Argyri_2025_PractitionerPerspectives.pdf |
| 61 | Olofsson et al. — Difficulties following naturalistic psychedelic use and associations with adverse childhood experiences | Int J Drug Policy 2026 | 10.1016/j.drugpo.2025.105105 | Olofsson_2026_DifficultiesAndACEs.pdf |
| 62 | Zhou et al. — Prediction of hallucinogen persisting perception disorder and thought disturbance symptoms following psychedelic use | PNAS Nexus 2025 | 10.1093/pnasnexus/pgae560 | _Cross-cutting/Zhou_2025_HPPDPrediction.pdf |
| 63 | Benjamin — Persistent psychiatric symptoms after eating psilocybin mushrooms | BMJ 1979 | 10.1136/bmj.1.6174.1319 | Benjamin_1979_PersistentPsychiatricSymptoms.pdf |
| 64 | Farah et al. — Psilocybin exposures reported to U.S. poison centers: national trends over a decade | J Adolesc Health 2024 | 10.1016/j.jadohealth.2024.01.027 | Farah_2024_PoisonCentreExposures.pdf |
| 65 | Trabulus & Altiparmak — Clinical features and outcome of patients with amatoxin-containing mushroom poisoning | Clin Toxicol 2011 | 10.3109/15563650.2011.565772 | Trabulus_2011_AmatoxinPoisoningOutcomes.pdf |
| 66 | Dimitrova et al. — Amatoxin intoxication and wild mushroom poisoning: current advances in diagnosis, risk stratification and clinical management | Toxins 2026 | 10.3390/toxins18050216 | Dimitrova_2026_AmatoxinPoisoningReview.pdf |
| 67 | Zhai et al. — Tentative identification of in vitro metabolites of O-acetylpsilocin (psilacetin, 4-AcO-DMT) by UHPLC-Q-Orbitrap MS | Drug Test Anal 2022 | 10.1002/dta.3255 | Zhai_2022_4AcODMTMetabolites.pdf |
| 68 | Hepburn et al. — Interactions between psilocybin, LSD and serotonergic antidepressants: a qualitative analysis of user reports | Psychedelics 2025 | 10.1016/j.psyche.2025.100005 | Hepburn_2025_PsychedelicAntidepressantInteractions.pdf |
| 69 | Burmester et al. — Subacute effects of a single dose of psilocybin on biomarkers of inflammation in healthy humans | Compr Psychoneuroendocrinol 2023 | 10.1016/j.cpnec.2022.100163 | Burmester_2023_InflammationBiomarkers.pdf |
| 70 | Vanderijst et al. — Redefining the real problem in psychedelic trials: why fighting the Lessebo matters more than blinding integrity | Int J Drug Policy 2026 | 10.1016/j.drugpo.2026.105423 | Vanderijst_2026_LesseboEffect.pdf |
| 71 | Ehrenkranz et al. — Validating and creating a short form of the Persisting Effects Questionnaire | J Psychopharmacol 2026 | 10.1177/02698811261473405 | Ehrenkranz_2026_PEQShortForm.pdf |

## Reports (no DOI; save the PDF of the full report)

| # | Report | Save as |
|---|---|---|
| R1 | UNODC — World Drug Report 2025 (hallucinogens section) | _Epidemiology/UNODC_2025_WorldDrugReport.pdf |
| R2 | EUDA — European Drug Report 2026: Trends and Developments (hallucinogens/psilocybin) | _Epidemiology/EUDA_2026_EuropeanDrugReport.pdf |
| R3 | SAMHSA — NSDUH 2024 detailed tables (hallucinogens; psilocybin item) | _Epidemiology/SAMHSA_2024_NSDUH_DetailedTables.pdf |
| R4 | Monitoring the Future — latest national survey results (hallucinogens other than LSD) | _Epidemiology/MTF_latest_NationalResults.pdf |
| R5 | Global Drug Survey — most recent key findings report (psilocybin mushrooms, microdosing) | _Epidemiology/GDS_latest_KeyFindings.pdf |
| R6 | Health Canada / FDA — psilocybin special access and breakthrough-therapy documentation (latest) | _Epidemiology/Regulators_latest_PsilocybinAccess.pdf |
| R7 | Oregon Health Authority — Psilocybin Services annual data report (latest) | _Epidemiology/OHA_latest_PsilocybinServices.pdf |
| R8 | ACMD (UK) — advice on psilocybin rescheduling for research (latest) | _Epidemiology/ACMD_latest_PsilocybinAdvice.pdf |
| R9 | WEDINOS — annual drug-checking report (latest; psilocybin and 4-AcO-DMT samples) | _Epidemiology/WEDINOS_latest_AnnualReport.pdf |

## Known gaps this list does not yet cover

Could not be verified in this build and therefore left out of the tables: **Carhart-Harris et al. 2016, "Psilocybin with psychological support for treatment-resistant depression: an open-label feasibility study", Lancet Psychiatry** — the DOI contains parentheses and every Crossref request for it returned a client error; obtain it by title. Also not yet surfaced with a verified DOI: Goodwin et al.'s phase 3 COMP005/COMP006 results; Griffiths et al. 2008 and 2018 (14-month follow-up; psilocybin with meditation); Gukasyan et al. 2022 (12-month follow-up of Davis 2021); Carhart-Harris et al. 2018 (psilocybin for TRD, 6-month follow-up); Vollenweider et al. 1997–1998 (PET psilocybin model psychosis and ketanserin blockade); Preller et al. 2017–2020 (5-HT2A dependence of psilocybin effects); Yerubandi et al. 2024 (JAMA Netw Open, adverse effects meta-analysis).

Sections still thin: **mushroom misidentification poisonings** — two Crossref passes returned only general amatoxin series, none specific to people foraging psilocybin-containing species; items 65–66 are the general clinical backbone and the species-confusion literature (Galerina, Conocybe, Cortinarius) remains to be found, probably in mycology and regional toxicology journals. **Epidemiology** — the prevalence-trend query was refused twice; US and European prevalence rests on reports R1–R5 until the PubMed layer runs. **Physiological safety** beyond items 20, 23 and 25: no verified source yet on cardiac valvulopathy and 5-HT2B signalling with repeated dosing, on psilocybin in people with cardiovascular disease, or on QT effects. **Pregnancy**: no human data identified. **4-AcO-DMT**: only one analytical paper (item 67); no human pharmacology exists. **Psychosis and HPPD risk specific to psilocybin** is covered only through the cross-cutting items 29 and 62. **Greek data** (ΕΚΤΕΠΝ/OKANA): none.

## Verification block

- DOIs in the list: 71 (items 1–71), plus two correction DOIs cited inside rows (10.1017/s0033291723002039 for item 36; 10.1007/s40262-025-01487-3 for item 22).
- All 71 were returned by Crossref API responses on 2026-10-15 with title, container-title and issued year.
- DOIs additionally fetched individually at `filter=doi:<DOI>` with `select=...,updated-by` (◆): 12 attempted → 12 resolved to the intended paper (items 2, 3, 18, 31, 32, 33, 42, 43, 44, 46, plus the two batch-confirmed Nature/JAMA records counted among them). No `updated-by` entry on any of the twelve.
- Dropped: 1 — **10.1016/s2215-0366(16)30065-7** (Carhart-Harris 2016, Lancet Psychiatry, open-label TRD feasibility study): three attempts, both raw and percent-encoded, returned a client error from Crossref; it is listed under "Known gaps" and must be obtained by title, not from this DOI.
- Errata/corrections (keep, marked): item 36 (Weiss 2023, Psychol Med — corrigendum 10.1017/s0033291723002039, returned as its own Crossref record); item 22 (Otto 2025, Clin Pharmacokinet — correction 10.1007/s40262-025-01487-3, returned as its own Crossref record).
- Retractions: none found.
