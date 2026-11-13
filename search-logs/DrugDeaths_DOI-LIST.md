# DrugDeaths — evidence map and PDF list for "How drug deaths are counted" (v0.1, 2026-10-31)

Cross-cutting topic requested by the senior author (brief `docs/TOPIC-MAP-BRIEF-2026-10-31.md`, Topic 2): the research on how drug deaths are **defined, investigated, certified, coded and counted**, and how far the counts can be trusted, in **both directions**: deaths wrongly attributed to a drug, and drug deaths that are missed. Six parts: (1) definitions and coding; (2) accuracy of death certificates, deaths certified with no named drug, variation between places, and estimates of undercounting; (3) who investigates deaths; (4) what a blood level after death can and cannot show; (5) deaths attributed to particular drugs and re-examined; (6) how the media report drug deaths. Reading list only: no claims, no study cards. Run by an AI research librarian on 2026-10-31.

How this list was built: PubMed through the E-utilities interface (`esearch`, `esummary`; `efetch` for abstracts where a title did not show the design or finding, and for PubMed's comment and correction links) in a tab of the app's browser that this reader opened, 27 topic searches and 19 known-item searches, plus one Crossref bibliographic search (strings, hit counts and what was kept: `DrugDeaths_search-log.md`). Order of preference: systematic and scoping reviews; then large studies (record linkage, national data compared across sources), authoritative reports and position papers; then single-site studies and case series where nothing better exists. Each landmark is listed with its published critiques. Existing lists were checked first with a DOI index of all `search-logs/*_DOI-LIST.md` (3,534 DOIs); papers already on them are named in each section's "Already on other lists" line instead of being listed again.

**Columns.** **DOI**: every DOI was fetched from Crossref `works/<DOI>` in the browser tab on 2026-10-31 and matched to the PubMed record on title, year and first author; its `updated-by` field was read (corrections, retractions), and PubMed's own comment and correction links were read for every row. Where Crossref's year (online) and PubMed's year (print issue) differ, the print year is given with the online year in brackets. **Free?**: `PMCxxxxxxx` = free full text in PubMed Central (from the PubMed record); `publisher` = OpenAlex `open_access` shows the article free at the publisher (gold, hybrid, bronze or diamond); `—` = neither (a copy in an institutional repository, OpenAlex "green", is not counted). Free papers can be read by AI readers without the senior author saving them.

**Tiers.** A = read first: the backbone reviews, the standards that define and certify drug deaths, the studies that measured how far the counts are wrong in each direction, and each landmark with its critiques. B = further studies, critiques and context.

Save each PDF under `PDFs/` with the path given (drug folder from `docs/TIER1.md` where a paper concerns one drug, `_Cross-cutting/` otherwise; reports in `_Epidemiology/`).

**Language note (METHODS §9).** Titles are reproduced as Crossref and PubMed give them; some use "abuse" or "addicts". The editors' own text uses "drug-induced death" and "overdose death" in each source's own coding sense.

---

## 1. Definitions and coding — `PDFs/_Cross-cutting/`

ICD-10 codes, "poisoning" against "misuse" definitions, national and European definitions, and counting every drug mentioned when several are found.

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 1 | Beynon et al. — When is a drug-related death not a drug-related death? Implications for current drug-related death policies in the UK and Europe | Subst Abuse Treat Prev Policy 2007 | 10.1186/1747-597X-2-25 | PMC1976310 | _Cross-cutting/Beynon_2007_WhenIsDRDNotDRD.pdf |
| 2 | Goldberger et al. — Uniform standards and case definitions for classifying opioid-related deaths: recommendations by a SAMHSA consensus panel | J Addict Dis 2013 | 10.1080/10550887.2013.824334 | PMC3805449 | _Cross-cutting/Goldberger_2013_UniformCaseDefinitionsOpioidDeaths.pdf |
| 3 | Ossiander — Using textual cause-of-death data to study drug poisoning deaths (literal text of the certificate compared with ICD-10 codes) | Am J Epidemiol 2014 | 10.1093/aje/kwt333 | — | _Cross-cutting/Ossiander_2014_TextualCauseOfDeathData.pdf |
| 4 | Garnett, Cisewski & Ahmad — Drugs most frequently involved in drug overdose deaths: United States, 2017–2023 (NCHS National Vital Statistics Report: the ICD-10 codes used, the literal-text search, and deaths involving several drugs counted under each; Crossref record type "report") | Natl Vital Stat Rep 2026 | 10.15620/cdc/174640 | PMC12989908 | _Cross-cutting/Garnett_2026_DrugsMostFrequentlyInvolvedNVSR.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 5 | Lahti et al. — Blood-positive illicit-drug findings: implications for cause-of-death certification, classification and coding (Finland) | Forensic Sci Int 2009 | 10.1016/j.forsciint.2009.02.007 | — | _Cross-cutting/Lahti_2009_BloodPositiveFindingsCoding.pdf |
| 6 | Hill & Cook — Narrative verdicts and their impact on mortality statistics in England and Wales (ONS study of injury and poisoning deaths, coding of intent from coroners' narrative conclusions) | Health Stat Q 2011 | 10.1057/hsq.2011.4 | publisher | _Cross-cutting/Hill_2011_NarrativeVerdictsMortalityStatistics.pdf |

**Already on other lists (not repeated):** _Overdose-and-emergency #60 Wood et al. 2010 (ICD-10 coding poorly identifies recreational drug presentations to an emergency department; hospital data, not deaths), Tier B for this page.

**Also needed:** the definitions themselves are reports (R1–R6 below: ONS, National Records of Scotland, the EUDA drug-related deaths protocol, two NCHS reports on literal text, and the ICD-10 coding rules).

**Known gaps.** Peer-reviewed comparisons of the definitions are few: Beynon 2007 for the UK and Europe, Goldberger 2013 for the US; no recent paper comparing the EUDA ("Selection B"), ONS "drug poisoning" and "drug misuse", NRS and CDC definitions side by side was found in PubMed. Two studies of how countries adopted the European definition are not in English (Santos 2010, Spanish, on Spain; Janssen 2009, French, on France) and were not listed. Counting a death under every drug mentioned is described in NCHS reports (#4; R4) and literal-text studies (#3); no study was found that measures how far the sum of drug-specific counts exceeds the total in European statistics.

---

## 2. Accuracy of death certificates, deaths with no named drug, variation between places, and estimates of undercounting — `PDFs/_Cross-cutting/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 7 | Gutkind et al. — Misclassification of opioid-involvement in drug-related overdose deaths in the United States: a scoping review | Ann Epidemiol 2025 (online 2024) | 10.1016/j.annepidem.2024.12.010 | PMC11916924 | _Cross-cutting/Gutkind_2025_OpioidMisclassificationScopingReview.pdf |
| 8 | Slavova et al. — Methodological complexities in quantifying rates of fatal opioid-related overdose (review) | Curr Epidemiol Rep 2019 | 10.1007/s40471-019-00201-9 | PMC6559129 | _Cross-cutting/Slavova_2019_MethodologicalComplexitiesOpioidDeaths.pdf |
| 9 | Slavova et al. — Drug overdose deaths: let's get specific (state variation in naming the drug on the certificate) | Public Health Rep 2015 | 10.1177/003335491513000411 | PMC4547584 | _Cross-cutting/Slavova_2015_LetsGetSpecific.pdf |
| 10 | Ruhm — Corrected US opioid-involved drug poisoning deaths and mortality rates, 1999–2015 (deaths with no named drug re-assigned) | Addiction 2018 | 10.1111/add.14144 | — | _Cross-cutting/Ruhm_2018_CorrectedOpioidDeaths.pdf |
| 11 | Buchanich et al. — The effect of incomplete death certificates on estimates of unintentional opioid-related overdose deaths in the United States, 1999–2015 | Public Health Rep 2018 | 10.1177/0033354918774330 | PMC6055296 | _Cross-cutting/Buchanich_2018_IncompleteDeathCertificates.pdf |
| 12 | Horon et al. — Standard death certificates versus enhanced surveillance to identify heroin overdose-related deaths | Am J Public Health 2018 | 10.2105/AJPH.2018.304385 | PMC5944879 | _Cross-cutting/Horon_2018_EnhancedSurveillanceHeroinDeaths.pdf |
| 13 | Landen et al. — Methodological issues in the surveillance of poisoning, illicit drug overdose, and heroin overdose deaths in New Mexico | Am J Epidemiol 2003 | 10.1093/aje/kwf196 | — | _Cross-cutting/Landen_2003_SurveillanceMethodsNewMexico.pdf |
| 14 | Fugelstad et al. — Drug-related deaths: statistics based on death certificates miss one-third of cases (Sweden; mortality-register data, including the EUDA specification, compared with toxicology data) | Scand J Public Health 2020 (online 2017) | 10.1177/1403494817745187 | — | _Cross-cutting/Fugelstad_2020_DeathCertificatesMissOneThird.pdf |
| 15 | Amundsen — Lack of overlap and large discrepancies in the characteristics of the deceased in two sources of drug death: a linkage study of the Cause of Death and the Police Registries in Norway 2007–2009 | Int J Drug Policy 2017 | 10.1016/j.drugpo.2016.12.016 | — | _Cross-cutting/Amundsen_2017_TwoRegistriesNorway.pdf |
| 16 | Chen et al. — Comparison of Office for National Statistics (ONS) and National Programme on Substance Use Mortality (NPSUM) data suggests that opioid-related deaths in England & Wales have been systematically underestimated | Int J Drug Policy 2025 | 10.1016/j.drugpo.2025.104976 | publisher | _Cross-cutting/Chen_2025_ONSvsNPSUMOpioidDeaths.pdf |
| 17 | Stam et al. — An analysis of issues in the classification and reporting of heroin-related deaths (Australia; with Darke's commentary, 10.1111/add.14520, and Robertson's letter, 10.1111/add.14627, both linked in PubMed: obtain with it) | Addiction 2019 (online 2018) | 10.1111/add.14486 | — | _Cross-cutting/Stam_2019_ClassificationHeroinDeaths.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 18 | Boslett et al. — Using contributing causes of death improves prediction of opioid involvement in unclassified drug overdoses in US death records (with Ruhm's commentary, 10.1111/add.14988: obtain with it) | Addiction 2020 | 10.1111/add.14943 | PMC9745785 | _Cross-cutting/Boslett_2020_ContributingCausesUnclassified.pdf |
| 19 | Gladstone et al. — Sensitivity and specificity of administrative mortality data for identifying prescription opioid-related deaths (vital statistics against Ontario coroners' data) | CMAJ 2016 (online 2015) | 10.1503/cmaj.150349 | PMC4771548 | _Cross-cutting/Gladstone_2016_AdministrativeDataSensitivityOntario.pdf |
| 20 | Janssen — Drug-related deaths in France in 2007: estimates and implications (three official records cross-checked by capture–recapture; the author treats the estimates as upper bounds) | Subst Use Misuse 2011 | 10.3109/10826084.2011.565107 | — | _Cross-cutting/Janssen_2011_FranceCaptureRecapture.pdf |

**Already on other lists (not repeated):** none found by the DOI index for this section.

**Also needed:** Webb et al. 2003 (#27, coroners' records in England and Wales) and Lahti et al. 2009 (#5, Finland) also measure accuracy; the CDC data briefs with the coding definition are Heroin R10.

**Known gaps.** Most accuracy studies are from the United States and concern opioids, where deaths certified with no named drug ("unspecified", ICD-10 T50.9) are a known source of undercounting (#9–11, #18). Europe has register comparisons from Sweden (#14), Norway (#15), England and Wales (#16), Finland (#5) and France (#20); no study from Greece or other southern European countries in English was found. Warner et al. 2013 (*Academic Forensic Pathology*, state variation in certifying manner of death and the drugs involved) is not indexed in PubMed (0 hits) and could not be matched, so it is not listed. No study was found that measured, in either direction, how often stimulants, cannabis or new psychoactive substances are wrongly named or missed on certificates; the evidence for those drugs is case review (section 5).

---

## 3. Who investigates deaths: coroner and medical examiner systems, training and resources, autopsy and toxicology rates — `PDFs/_Cross-cutting/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 21 | Davis et al. — Position paper: recommendations for the investigation, diagnosis, and certification of deaths related to opioid and other drugs (National Association of Medical Examiners; Crossref holds the subtitle separately; earlier opioid-only version, free: Davis et al. 2014, J Med Toxicol, 10.1007/s13181-013-0323-x, PMC3951636) | Am J Forensic Med Pathol 2020 | 10.1097/PAF.0000000000000550 | publisher | _Cross-cutting/Davis_2020_NAMEPositionPaperDrugDeaths.pdf |
| 22 | Smiley-McDonald et al. — Toxicology testing in the USA: what the 2018 census of medical examiner and coroner offices tells us | J Anal Toxicol 2025 | 10.1093/jat/bkaf044 | — | _Cross-cutting/SmileyMcDonald_2025_ToxicologyTestingCensus2018.pdf |
| 23 | Lundberg et al. — Association between undetermined intent death classification and county death investigation system for drug poisoning deaths in nine US jurisdictions | Inj Prev 2026 | 10.1136/ip-2025-046028 | PMC13623016 | _Cross-cutting/Lundberg_2026_UndeterminedIntentInvestigationSystem.pdf |
| 24 | Zaychik — Improving state medicolegal death investigation: does system level reform improve public health data concerning drug-related mortality? (coroner-to-medical-examiner transitions) | J Forensic Leg Med 2024 | 10.1016/j.jflm.2024.102680 | — | _Cross-cutting/Zaychik_2024_SystemReformDrugMortalityData.pdf |
| 25 | Hancock et al. — False-positive rate for suspected drug-related deaths following full autopsy (what external examination with toxicology alone would have missed) | Am J Forensic Med Pathol 2024 | 10.1097/PAF.0000000000000936 | — | _Cross-cutting/Hancock_2024_FalsePositiveAfterFullAutopsy.pdf |
| 26 | Quesinberry et al. — Impact of a drug overdose decedent toxicology testing legislative mandate on informing coroner death investigation and certification practices (Kentucky) | Acad Forensic Pathol 2019 | 10.1177/1925362119851127 | PMC8351054 | _Cross-cutting/Quesinberry_2019_ToxicologyTestingMandateKentucky.pdf |
| 27 | Webb et al. — Cause and manner of death in drug-related fatality: an analysis of drug-related deaths recorded by coroners in England and Wales in 2000 (deaths recorded as overdose that had another cause) | Drug Alcohol Depend 2003 | 10.1016/s0376-8716(03)00191-1 | — | _Cross-cutting/Webb_2003_CauseMannerCoronersEnglandWales.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 28 | Dye et al. — Correctly identifying deaths due to drug toxicity without a forensic autopsy (read with #25) | Am J Forensic Med Pathol 2019 | 10.1097/PAF.0000000000000465 | — | _Cross-cutting/Dye_2019_DrugDeathsWithoutAutopsy.pdf |
| 29 | Rockett et al. — Variable classification of drug-intoxication suicides across US states: a partial artifact of forensics? (correction 10.1371/journal.pone.0137933, in Crossref `updated-by` and PubMed) | PLoS One 2015 | 10.1371/journal.pone.0135296 | PMC4546666 | _Cross-cutting/Rockett_2015_VariableClassificationSuicides.pdf |
| 30 | Frost et al. — Forensic autopsies in a naturalistic setting in Norway: autopsy rates and toxicological findings | Forensic Sci Int 2012 | 10.1016/j.forsciint.2012.10.023 | — | _Cross-cutting/Frost_2012_AutopsyRatesNorway.pdf |

**Already on other lists (not repeated):** none found by the DOI index for this section.

**Also needed:** R7–R9 (the US census of medical examiner and coroner offices, the National Research Council and Institute of Medicine reports on death investigation).

**Known gaps.** No study was found that measured how the training or qualifications of coroners and death investigators change drug-death counts; the evidence is a position paper (#21), a census of offices (#22), comparisons of systems (#23, #24, #29) and commentaries on workload (Davis 2023, *J Forensic Sci*; Andrew 2017 and Robinson 2017, *Acad Forensic Pathol*; found, not listed). The two system comparisons point in different directions: county coroner systems recorded more deaths of undetermined intent (#23), while switching from coroner to medical examiner systems did not improve drug-mortality data (#24). For England and Wales, no study of coroners' resources or practice and drug-death counts was found beyond #6, #16 and #27; coroner-verdict studies in PubMed concern suicide (Gunnell 2013; Palmer 2015; not listed). Autopsy rates in drug deaths are documented for Norway (#30) and the US (#22); no European comparison was found.

---

## 4. What a blood level after death can and cannot show — `PDFs/_Cross-cutting/`

Post-mortem redistribution, tolerance, overlap between levels found in deaths and in living people, and sampling site.

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 31 | Pounder & Jones — Post-mortem drug redistribution: a toxicological nightmare (landmark) | Forensic Sci Int 1990 | 10.1016/0379-0738(90)90182-x | — | _Cross-cutting/Pounder_1990_RedistributionToxicologicalNightmare.pdf |
| 32 | Ferner — Post-mortem clinical pharmacology (review; with Ritter's editorial comment, 10.1111/j.1365-2125.2008.03293.x, PMC2561124) | Br J Clin Pharmacol 2008 | 10.1111/j.1365-2125.2008.03231.x | PMC2561112 | _Cross-cutting/Ferner_2008_PostMortemClinicalPharmacology.pdf |
| 33 | Leikin & Watson — Post-mortem toxicology: what the dead can and cannot tell us | J Toxicol Clin Toxicol 2003 | 10.1081/clt-120018270 | — | _Cross-cutting/Leikin_2003_WhatTheDeadCanTellUs.pdf |
| 34 | Borra et al. — 50 years of postmortem redistribution research: what have we learned? (review) | Forensic Sci Int 2026 (online 2025) | 10.1016/j.forsciint.2025.112699 | — | _Cross-cutting/Borra_2026_FiftyYearsRedistribution.pdf |
| 35 | Launiainen & Ojanperä — Drug concentrations in post-mortem femoral blood compared with therapeutic concentrations in plasma | Drug Test Anal 2014 (online 2013) | 10.1002/dta.1507 | PMC4237191 | _Cross-cutting/Launiainen_2014_FemoralVsTherapeutic.pdf |
| 36 | Ketola & Kriikku — Drug concentrations in post-mortem specimens (meta-analysis of tissue-to-femoral-blood ratios for 50 drugs: sampling site) | Drug Test Anal 2019 | 10.1002/dta.2662 | — | _Cross-cutting/Ketola_2019_PostMortemSpecimenRatiosMA.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 37 | Druid & Holmgren — A compilation of fatal and control concentrations of drugs in postmortem femoral blood (DOI from a Crossref bibliographic search; the PubMed record has none) | J Forensic Sci 1997 | 10.1520/jfs14071j | — | _Cross-cutting/Druid_1997_FatalAndControlConcentrations.pdf |
| 38 | Pélissier-Alicot et al. — Mechanisms underlying postmortem redistribution of drugs: a review | J Anal Toxicol 2003 | 10.1093/jat/27.8.533 | — | _Cross-cutting/PelissierAlicot_2003_RedistributionMechanisms.pdf |
| 39 | Linnet — Postmortem drug concentration intervals for the non-intoxicated state: a review | J Forensic Leg Med 2012 | 10.1016/j.jflm.2012.02.010 | — | _Cross-cutting/Linnet_2012_NonIntoxicatedIntervals.pdf |
| 40 | Zilg et al. — Postmortem blood sampling: comparison of drug concentrations at different sample sites | Forensic Sci Int 2017 | 10.1016/j.forsciint.2017.07.006 | — | _Cross-cutting/Zilg_2017_SamplingSites.pdf |
| 41 | Kriikku et al. — Post-mortem oxycodone blood concentrations of hospitalized cancer and surgery patients compared with fatal poisonings (tolerance and overlap) | Int J Legal Med 2022 | 10.1007/s00414-022-02890-2 | PMC9576662 | Prescription-opioids/Kriikku_2022_OxycodoneHospitalVsPoisoning.pdf |

**Already on other lists (not repeated):** _Tolerance #334 Darke et al. 1997 (blood morphine in heroin-related deaths overlaps with that of people currently using heroin), Tier A for this page; Heroin #45 Darke et al. 2007 (fatal heroin overdose cases compared with morphine-positive homicide victims), #46 Darke et al. 2002 (hair morphine in deaths and in living users) and #6 Darke et al. 2016 (estimating survival times), Fentanyl-and-analogues #29 Palmer 2010 (fentanyl in post-mortem toxicology) and #41 Ruan et al. 2016 (norfentanyl/fentanyl ratios), GHB-GBL #23 Korb & Cooper 2014 (endogenous GHB in post-mortem blood) and #47 Busardò et al. 2014, Synthetic-cannabinoids #7 Giorgetti et al. 2020 (systematic review of post-mortem toxicology), Synthetic-cathinones #24 Ellefsen et al. 2016 and Ketamine #65 Lalonde & Wallage 2004 (post-mortem ketamine distribution), Tier B.

**Known gaps.** Redistribution and sampling site are well reviewed (#31–34, #36–38, #40). Overlap between levels in deaths and in living people is documented mainly for medicines in Nordic forensic databases (#35, #37, #39, #41), for heroin (Darke 1997, on _Tolerance) and for MDMA and fentanyl (#42, #51); for cocaine, amphetamines, cannabis and new synthetic opioids the evidence is case series. Tolerance cannot be measured after death; hair analysis (Heroin #46) is the only marker studied. Found and not listed: Prouty & Anderson 1990 and Yarema & Becker 2005 (no DOI in PubMed; covered by #31, #34 and #38), Cook et al. 2000, Gerostamoulos et al. 2012, Mantinieks et al. 2021 (a compilation of post-mortem/ante-mortem ratios) and Jones et al. 2016 (single-drug against multi-drug deaths). The search for Greek studies found two, not listed: Stefanidou et al. 2007 (a review of interpreting toxicology in drug-related cases in Greece) and Boumba et al. 2013 (fatal intoxications in Epirus, 1998–2010).

---

## 5. Deaths attributed to particular drugs and re-examined — drug folders and `PDFs/_Cross-cutting/`

MDMA, cannabis, synthetic cathinones, fentanyl and nitazenes, and "excited delirium".

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 42 | Milroy — "Ecstasy" associated deaths: what is a fatal concentration? Analysis of a case series (MDMA levels in deaths from MDMA toxicity compared with deaths from trauma) | Forensic Sci Med Pathol 2011 | 10.1007/s12024-010-9220-7 | — | MDMA/Milroy_2011_WhatIsAFatalConcentration.pdf |
| 43 | Drummer et al. — Cannabis as a cause of death: a review | Forensic Sci Int 2019 | 10.1016/j.forsciint.2019.03.007 | — | Cannabis/Drummer_2019_CannabisAsCauseOfDeath.pdf |
| 44 | Schifano et al. — Suspected and confirmed fatalities associated with mephedrone (4-methylmethcathinone, "meow meow") in the United Kingdom | J Clin Psychopharmacol 2012 | 10.1097/JCP.0b013e318266c70c | — | Synthetic-cathinones/Schifano_2012_SuspectedConfirmedMephedroneDeaths.pdf |
| 45 | Strömmer et al. — The role of restraint in fatal excited delirium: a research synthesis and pooled analysis (landmark; its published critiques are #53 and #54) | Forensic Sci Med Pathol 2020 | 10.1007/s12024-020-00291-8 | PMC7669776 | _Cross-cutting/Strommer_2020_RestraintExcitedDeliriumPooled.pdf |
| 46 | Gonçalves Dias & Cainé — Deaths in custody: physical restraint, excited delirium and medico-legal investigation: a systematic review | J Forensic Leg Med 2026 | 10.1016/j.jflm.2026.103200 | publisher | _Cross-cutting/GoncalvesDias_2026_DeathsInCustodySR.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 47 | Byard et al. — Amphetamine derivative fatalities in South Australia: is "Ecstasy" the culprit? (deaths after tablets sold as Ecstasy; PMA found in all six, MDMA in two) | Am J Forensic Med Pathol 1998 | 10.1097/00000433-199809000-00013 | — | MDMA/Byard_1998_IsEcstasyTheCulprit.pdf |
| 48 | Hartung et al. — Sudden unexpected death under acute influence of cannabis (case reports; read with #43) | Forensic Sci Int 2014 | 10.1016/j.forsciint.2014.02.001 | — | Cannabis/Hartung_2014_SuddenDeathAcuteCannabis.pdf |
| 49 | Rock et al. — Can cannabis kill? Characteristics of deaths following cannabis use in England (1998–2020) | J Psychopharmacol 2022 | 10.1177/02698811221115760 | PMC9716494 | Cannabis/Rock_2022_CanCannabisKill.pdf |
| 50 | Favretto et al. — Infant death due to cannabis ingestion (with Schirmer's critical comments, 10.1002/dta.70019, and the authors' response, 10.1002/dta.70055: obtain all three) | Drug Test Anal 2025 | 10.1002/dta.3904 | PMC12489283 | Cannabis/Favretto_2025_InfantDeathCannabisWithCritique.pdf |
| 51 | Gill et al. — Reliability of postmortem fentanyl concentrations in determining the cause of death (decedents with transdermal patches; erratum 10.1007/s13181-014-0427-y, in Crossref `updated-by` and PubMed) | J Med Toxicol 2013 (online 2012) | 10.1007/s13181-012-0253-z | PMC3576505 | Fentanyl-and-analogues/Gill_2013_PostmortemFentanylReliability.pdf |
| 52 | Chen et al. — Is nitazene-related mortality underestimated? Findings from an in vivo and ex vivo rat study and pharmacoepidemiological analysis of coroner-reported deaths (includes an animal experiment) | Clin Toxicol (Phila) 2026 | 10.1080/15563650.2025.2601141 | publisher | Fentanyl-and-analogues/Chen_2026_NitazeneDeathsUnderestimated.pdf |
| 53 | de Boer et al. — Scrutinizing the causal link between excited delirium syndrome and restraint: a commentary on Strömmer et al. (critique of #45; reply Freeman et al. 2023, 10.1007/s12024-023-00616-3, PMC10752838: obtain with it) | Forensic Sci Med Pathol 2023 | 10.1007/s12024-023-00589-3 | PMC10752912 | _Cross-cutting/deBoer_2023_CommentaryOnStrommer.pdf |
| 54 | de Boer et al. — More on: 'the role of restraint in fatal excited delirium syndrome' (second critique of #45; reply Freeman et al. 2024, 10.1007/s12024-023-00736-w: obtain with it) | Forensic Sci Med Pathol 2024 (online 2023) | 10.1007/s12024-023-00722-2 | PMC11525397 | _Cross-cutting/deBoer_2024_MoreOnRestraintExDS.pdf |
| 55 | Gonin et al. — Excited delirium: a systematic review (with the appraisal linked in PubMed, Bond et al. 2019, "Hot off the press: SGEM #218", 10.1111/acem.13487: obtain with it) | Acad Emerg Med 2018 (online 2017) | 10.1111/acem.13330 | publisher | _Cross-cutting/Gonin_2018_ExcitedDeliriumSR.pdf |
| 56 | Saadi et al. — End the use of "excited delirium" as a cause of death in police custody (comment) | Lancet 2022 | 10.1016/S0140-6736(22)00410-X | — | _Cross-cutting/Saadi_2022_EndExcitedDeliriumCauseOfDeath.pdf |

**Already on other lists (not repeated):** Ketamine #23 Corkery et al. 2021 (recreational ketamine-related deaths notified to the National Programme on Substance Abuse Deaths) and #24 Darke et al. 2021 (circumstances of ketamine-related deaths), Heroin #1 Darke & Zador 1996 (fatal heroin "overdose": a review), Tier A for this page; Ketamine #22 Schifano et al. 2008, #64 Gill & Stajic 2000 and #99 Chiappini et al. 2015 (methoxetamine deaths), MDMA #67 Gill et al. 2002 (MDMA deaths in New York City) and #34 Rigg et al. 2018, Synthetic-cathinones #23 Maskell et al. 2011 (mephedrone-related deaths) and #47 Penders et al. 2012 (excited delirium after synthetic cathinones), Cannabis #109 Calabria et al. 2010 (does cannabis use increase the risk of death?), Fentanyl-and-analogues #27 Henderson 1991 and #37 Krinsky et al. 2011 (toxicology-based review of fentanyl deaths in New Mexico), Tier B.

**Also needed:** R10–R11 (the Physicians for Human Rights report and the professional statements on "excited delirium").

**Known gaps.** Re-examinations rest on case series and national coroner-reported data (UK, Australia, US); no systematic review re-examining deaths attributed to MDMA, cathinones or ketamine was found. For cannabis, the reports of deaths and their critique are case-level (#43, #48, #50); the 2017 child myocarditis case that was widely reported as a cannabis overdose death (Nappe & Hoyte 2017, found, not listed) has no published critique in PubMed. For fentanyl, wrongly attributed deaths are discussed for transdermal patches (#51) and missed deaths for nitazenes (#52); studies of how widening toxicology panels changed fentanyl-analogue counts (Clinton et al. 2021) were found and not listed. For "excited delirium", the literature is a contested construct with a pooled analysis, two systematic reviews and an exchange of critiques; the statements withdrawing professional support for the term are reports (R11). Found and not listed: Vilke et al. 2012 (defining review), Walsh et al. 2023 (racial bias), Slocum et al. 2023 (scoping review), Schifano et al. 2003 and 2004 (MDMA deaths with polydrug use), Loi et al. 2015 (mephedrone deaths at ages 16–24), Cone et al. 2003 (classification of oxycodone-involved deaths).

---

## 6. How the media report drug deaths — `PDFs/_Cross-cutting/` and drug folders

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 57 | Forsyth — Virtually a drug scare: mephedrone and the impact of the Internet on drug news transmission (alleged mephedrone deaths in online news; the most-read proved false alarms) | Int J Drug Policy 2012 | 10.1016/j.drugpo.2011.12.003 | — | Synthetic-cathinones/Forsyth_2012_VirtuallyADrugScare.pdf |
| 58 | Sumnall et al. — Effects of media representations of drug related deaths on public stigma and support for harm reduction (randomised online experiment, UK) | Int J Drug Policy 2023 (online 2022) | 10.1016/j.drugpo.2022.103909 | publisher | _Cross-cutting/Sumnall_2023_MediaRepresentationsDRDStigma.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 59 | Fraser et al. — Grievable lives? Death by opioid overdose in Australian newspaper coverage | Int J Drug Policy 2018 | 10.1016/j.drugpo.2018.06.004 | — | _Cross-cutting/Fraser_2018_GrievableLivesNewspapers.pdf |
| 60 | Beletsky et al. — Fentanyl panic goes viral: the spread of misinformation about overdose risk from casual contact with fentanyl in mainstream and social media | Int J Drug Policy 2020 | 10.1016/j.drugpo.2020.102951 | PMC7492952 | Fentanyl-and-analogues/Beletsky_2020_FentanylPanicGoesViral.pdf |

**Already on other lists (not repeated):** none; _Language-and-stigma R5 (EUDA style conventions for reporting drug-related deaths) is a report.

**Known gaps.** A thin literature. Forsyth's earlier quantitative study of drug-death reports in the Scottish press (Forsyth 2001, *Int J Drug Policy*, "Distorted?") is not found in PubMed (0 hits) and could not be matched, so it is not listed. Found and not listed: Bammer & Sengoz 1995 (a cluster of three heroin deaths in Canberra and its press coverage), Hswen et al. 2020 and Dasgupta et al. 2009 (volume of news coverage against opioid deaths). No study was found that compared press reports of individual drug deaths with the later inquest or toxicology findings beyond the mephedrone episode (#44, #57).

---

## Reports (no DOI; save the PDF of the full report)

| # | Report | Save as |
|---|---|---|
| R1 | Office for National Statistics — *Deaths related to drug poisoning in England and Wales*: Quality and Methodology Information (the ICD-10 codes for "drug poisoning" and "drug misuse", and how substances "mentioned" on the certificate are counted); the latest registrations bulletin is _Interactions R5 | _Epidemiology/ONS_latest_DrugPoisoningQMI.pdf |
| R2 | National Records of Scotland — *Drug-related deaths in Scotland*, latest, with its annex on definitions and on the differences from the UK "drug misuse" definition (same report as Benzodiazepines R3) | _Epidemiology/NRS_latest_DrugRelatedDeathsScotland.pdf |
| R3 | EUDA (formerly EMCDDA) — *Drug-related deaths (DRD) standard protocol*, version 3.2 (2010), with the "Selection B" ICD-10 code list used for European comparisons; the European Drug Report's drug-induced deaths chapter is _Overdose-and-emergency R1 | _Epidemiology/EMCDDA_2010_DRDStandardProtocol_v3.2.pdf |
| R4 | Trinidad et al. — *Using literal text from the death certificate to enhance mortality statistics: characterizing drug involvement in deaths* (National Vital Statistics Reports 2016; PubMed 27996933, no DOI) | _Epidemiology/NCHS_2016_LiteralTextDrugInvolvement.pdf |
| R5 | Warner et al. — *Drugs most frequently involved in drug overdose deaths: United States, 2010–2014* (National Vital Statistics Reports 2016; PubMed 27996932, no DOI; the 2026 update is #4) | _Epidemiology/NCHS_2016_DrugsMostFrequentlyInvolved.pdf |
| R6 | World Health Organization — ICD-10, Volume 2 (Instruction manual): rules for selecting the underlying cause of death and coding poisonings | _Epidemiology/WHO_ICD10_Volume2_InstructionManual.pdf |
| R7 | US Bureau of Justice Statistics — *Medical Examiner and Coroner Offices, 2018* (results of the 2018 census, published 2021; analysed in #22) | _Epidemiology/BJS_2021_MedicalExaminerCoronerOffices2018.pdf |
| R8 | National Research Council — *Strengthening Forensic Science in the United States: A Path Forward* (2009), chapter on medicolegal death investigation | _Epidemiology/NRC_2009_StrengtheningForensicScience.pdf |
| R9 | Institute of Medicine — *Medicolegal Death Investigation System: Workshop Summary* (2003) | _Epidemiology/IOM_2003_MedicolegalDeathInvestigation.pdf |
| R10 | Physicians for Human Rights — *"Excited Delirium" and Deaths in Police Custody* (2022) | _Epidemiology/PHR_2022_ExcitedDeliriumDeathsInCustody.pdf |
| R11 | American College of Emergency Physicians — *White Paper Report on Excited Delirium Syndrome* (2009), with the 2023 statements of ACEP and the National Association of Medical Examiners on the term | _Epidemiology/ACEP_2009_ExcitedDeliriumWhitePaper_and_2023Statements.pdf |
| R12 | ΕΚΤΕΠΝ — annual report on the drug situation in Greece (latest; drug-induced deaths, definitions and sources), same file as Fentanyl-and-analogues R10 and Heroin R12 | _Epidemiology/EKTEPN_latest_AnnualReport.pdf |

---

## Verification block (2026-10-31)

- **Final list:** 60 new papers (Tier A 35, Tier B 25) in six sections, plus 25 papers already on other lists, named in each section's "Already on other lists" line (_Tolerance, Heroin, Fentanyl-and-analogues, GHB-GBL, Synthetic-cannabinoids, Synthetic-cathinones, Ketamine, MDMA, Cannabis, _Overdose-and-emergency), and 12 reports without a DOI. Twelve further documents are named inside rows to be obtained with them: two correction notices, nine commentaries, critiques, replies and appraisals, and the 2014 version of #21; each was fetched from Crossref.
- **DOIs fetched:** every one of the 60 listed DOIs was fetched from Crossref `works/<DOI>` in this reader's browser tab on 2026-10-31, at drafting and again in a final sweep of all 72 DOIs named in the tables; all 60 resolved to the paper named, with matching title, journal, year and first author, and the sweep found no change. Also fetched: the 12 in-row DOIs, and four DOIs verified and then removed at the final selection for scope or space (Rockett et al. 2014; Ciesluk et al. 2024; Bammer & Sengoz 1995; Goldsmith et al. 2023). No fetched DOI failed to resolve; none was dropped for resolving to another paper. No DOI was written from memory: each came from a PubMed `esummary` record or, for #37, a Crossref bibliographic search, and was then fetched.
- **Matched to PubMed:** 59 of the 60 DOIs are carried by a PubMed record (DOI lookup in PubMed, same day; first author, year and title agree). #37 Druid & Holmgren 1997 has no DOI in PubMed (PMID 8988577) and was located by Crossref bibliographic search on title, authors and year (10.1520/jfs14071j; title, journal, year and first author agree). For #21, Crossref's title field holds only "Position Paper" and the rest is in its subtitle field, which matches the PubMed title; for its 2014 version Crossref gives the expert panel as author, PubMed Davis GG.
- **Overlap with other lists:** all 72 DOIs (60 rows and 12 in-row) were checked against a local index of every DOI in `search-logs/*_DOI-LIST.md` (3,534 DOIs, parentheses in DOIs handled); none is on another list. None is in the reference library either (`data/references/*.json`, 12 files, searched by DOI).
- **Corrections and errata:** #29 Rockett et al. 2015 (correction 10.1371/journal.pone.0137933, in Crossref `updated-by` and PubMed; PMC4559469); #51 Gill et al. 2013 (erratum 10.1007/s13181-014-0427-y, in Crossref `updated-by` and PubMed; PMC4547952). Obtain each with its notice. In the final check PubMed returned all 60 records and links no other correction to them.
- **Retractions:** none of the 60 listed papers has a retraction or expression of concern in Crossref `updated-by` or in PubMed. A withdrawn duplicate record (Shah et al. 2012, *Drug Alcohol Depend*, "WITHDRAWN") appeared in one known-item search and was not relevant.
- **Published critiques and comments linked to rows:** #17 (Darke 2019 commentary; Robertson 2019 letter), #18 (Ruhm 2020 commentary), #32 (Ritter 2008 editorial), #45 (critiques #53 and #54, with replies Freeman et al. 2023 and 2024), #50 (Schirmer 2026 critique; Favretto et al. 2026 reply), #55 (Bond et al. 2019 appraisal). These are all the comment links PubMed holds for the 60 rows.
- **Metadata kept as found:** where Crossref (online) and PubMed (print) years differ, the print year is given with the online year in brackets (10 rows); no title was shortened.
- **Free to read:** 30 of the 60 new papers (23 with a PMC id from the PubMed record, 7 open at the publisher per OpenAlex `open_access`). Copies in institutional repositories (OpenAlex "green" without PMC: #34, #57, #59) are not counted.
- **Numbering:** rows are numbered in page order; the search log names papers by first author and year, not by number.
