# Alcohol — evidence map and PDF list (v0.1, 2026-10-15)

All DOIs below were verified against Crossref on 2026-10-15 (metadata resolved; retraction check via the `updated-by` field: none retracted; five carry published errata/corrections, marked). Save each PDF into `PDFs/Alcohol/` with the filename given. Cross-cutting papers go in `PDFs/_Cross-cutting/`.

How this list was built: (1) landmark studies and their published critiques, replies and follow-ups (the "no safe level" debate, the cardiovascular J-curve and its Mendelian-randomization critiques, the abstainer-bias literature, the withdrawal and pharmacotherapy trials, the FASD literature); (2) systematic reviews and meta-analyses located through Crossref bibliographic and author/title queries; (3) verification of every DOI by a Crossref `works/<DOI>` fetch, or — where that endpoint was rate-limited — by the Crossref works-search record returned for that exact DOI (marked † ; these records carry the same metadata and the same `updated-by` retraction field). Crossref throttled this session heavily (HTTP 429 after every 1–10 requests for most of the day), so the discovery layer is thinner than the methamphetamine list's: 16 section queries were written but only a minority could be run (see `Alcohol_search-log.md`). The PubMed layer (strings in the search log) is still to be run and will add to this list; its results decide what is added or dropped, not this list.

**Work through the list in order. Tier A first. Tell me each time you finish a batch of ten and I will start reading.**

---

## Tier A — needed now (backbone reviews + landmark primaries with their critiques)

| # | Paper | Journal, year | DOI | Save as |
|---|---|---|---|---|
| 1 | GBD 2016 Alcohol Collaborators (Griswold et al.) — Alcohol use and burden for 195 countries and territories, 1990–2016 (the "no safe level" paper) | Lancet 2018 | 10.1016/S0140-6736(18)31310-2 | Griswold_2018_GBD2016_AlcoholBurden.pdf |
| 2 | Burton & Sheron — No level of alcohol consumption improves health (comment on #1) | Lancet 2018 | 10.1016/S0140-6736(18)31571-X | Burton_2018_NoLevelImprovesHealth.pdf |
| 3 | GBD 2020 Alcohol Collaborators (Bryazka et al.) — Population-level risks of alcohol consumption by amount, geography, age, sex, and year (revises #1; erratum published; obtain both) | Lancet 2022 | 10.1016/S0140-6736(22)00847-9 | Bryazka_2022_GBD2020_PopulationLevelRisks.pdf |
| 4 | Wood et al. — Risk thresholds for alcohol consumption: combined analysis of individual-participant data for 599 912 current drinkers in 83 prospective studies (erratum published; obtain both) | Lancet 2018 | 10.1016/S0140-6736(18)30134-X | Wood_2018_RiskThresholds83Studies.pdf |
| 5 | Stockwell et al. — Do "moderate" drinkers have reduced mortality risk? A systematic review and meta-analysis of alcohol consumption and all-cause mortality | J Stud Alcohol Drugs 2016 | 10.15288/jsad.2016.77.185 | Stockwell_2016_ModerateDrinkersMortalityMA.pdf |
| 6 | Stockwell et al. — Why do only some cohort studies find health benefits from low-volume alcohol use? SR/MA of study characteristics that may bias mortality risk estimates | J Stud Alcohol Drugs 2024 | 10.15288/jsad.23-00283 | Stockwell_2024_CohortBiasLowVolumeMA.pdf |
| 7 | Zhao et al. — Association between daily alcohol intake and risk of all-cause mortality: a systematic review and meta-analyses | JAMA Netw Open 2023 | 10.1001/jamanetworkopen.2023.6185 | Zhao_2023_DailyIntakeAllCauseMortalityMA.pdf |
| 8 | Di Castelnuovo et al. — Alcohol dosing and total mortality in men and women: an updated meta-analysis of 34 prospective studies (the J-curve meta-analysis that #5–7 critique) | Arch Intern Med 2006 | 10.1001/archinte.166.22.2437 | DiCastelnuovo_2006_AlcoholDosingTotalMortalityMA.pdf |
| 9 | Chikritzhs et al. — Has the leaning tower of presumed health benefits from 'moderate' alcohol use finally collapsed? | Addiction 2015 | 10.1111/add.12828 | Chikritzhs_2015_LeaningTower.pdf |
| 10 | Ronksley et al. — Association of alcohol consumption with selected cardiovascular disease outcomes: a systematic review and meta-analysis | BMJ 2011 | 10.1136/bmj.d671 | Ronksley_2011_AlcoholCVDOutcomesMA.pdf |
| 11 | Roerecke & Rehm — The cardioprotective association of average alcohol consumption and ischaemic heart disease: a systematic review and meta-analysis | Addiction 2012 | 10.1111/j.1360-0443.2012.03780.x | Roerecke_2012_CardioprotectiveIHDMA.pdf |
| 12 | Roerecke & Rehm — Alcohol consumption, drinking patterns, and ischemic heart disease: narrative review of meta-analyses and SR/MA of heavy drinking occasions | BMC Med 2014 | 10.1186/s12916-014-0182-6 | Roerecke_2014_DrinkingPatternsIHD.pdf |
| 13 | Holmes et al. — Association between alcohol and cardiovascular disease: Mendelian randomisation analysis based on individual participant data | BMJ 2014 | 10.1136/bmj.g4164 | Holmes_2014_AlcoholCVD_MendelianRandomisation.pdf |
| 14 | Millwood et al. — Conventional and genetic evidence on alcohol and vascular disease aetiology: a prospective study of 500 000 men and women in China | Lancet 2019 | 10.1016/S0140-6736(18)31772-0 | Millwood_2019_ChinaKadoorieGeneticEvidence.pdf |
| 15 | Biddinger et al. — Association of habitual alcohol intake with risk of cardiovascular disease (UK Biobank MR) | JAMA Netw Open 2022 | 10.1001/jamanetworkopen.2022.3849 | Biddinger_2022_HabitualIntakeCVD_MR.pdf |
| 16 | Mukamal, Stampfer & Rimm — Genetic instrumental variable analysis: time to call Mendelian randomization what it is. The example of alcohol and cardiovascular disease (critique of #13–15) | Eur J Epidemiol 2019 | 10.1007/s10654-019-00578-3 | Mukamal_2019_MRCritique.pdf |
| 16a | Larsson et al. — Alcohol consumption and cardiovascular disease: a Mendelian randomization study | Circ Genom Precis Med 2020 | 10.1161/CIRCGEN.119.002814 | Larsson_2020_AlcoholCVD_MR.pdf |
| 17 | Bagnardi et al. — Alcohol consumption and site-specific cancer risk: a comprehensive dose–response meta-analysis | Br J Cancer 2015 | 10.1038/bjc.2014.579 | Bagnardi_2015_SiteSpecificCancerDoseResponseMA.pdf |
| 18 | Rumgay et al. — Global burden of cancer in 2020 attributable to alcohol consumption: a population-based study | Lancet Oncol 2021 | 10.1016/S1470-2045(21)00279-5 | Rumgay_2021_CancerBurdenAttributable.pdf |
| 19 | Rehm et al. — Alcohol as a risk factor for liver cirrhosis: a systematic review and meta-analysis | Drug Alcohol Rev 2010 | 10.1111/j.1465-3362.2009.00153.x | Rehm_2010_CirrhosisMA.pdf |
| 20 | Roerecke et al. — Alcohol consumption and risks of liver cirrhosis: a systematic review and meta-analysis (dose–response; sex differences) | Am J Gastroenterol 2019 | 10.14309/ajg.0000000000000340 | Roerecke_2019_CirrhosisDoseResponseMA.pdf |
| 21 | Askgaard et al. — Alcohol drinking pattern and risk of alcoholic liver cirrhosis: a prospective cohort study | J Hepatol 2015 | 10.1016/j.jhep.2014.12.005 | Askgaard_2015_DrinkingPatternCirrhosisCohort.pdf |
| 22 | Grant et al. — Epidemiology of DSM-5 alcohol use disorder: results from NESARC-III | JAMA Psychiatry 2015 | 10.1001/jamapsychiatry.2015.0584 | Grant_2015_DSM5AUD_NESARC-III.pdf |
| 23 | Grant et al. — Prevalence of 12-month alcohol use, high-risk drinking, and DSM-IV alcohol use disorder in the United States, 2001–2002 to 2012–2013 | JAMA Psychiatry 2017 | 10.1001/jamapsychiatry.2017.2161 | Grant_2017_Trends2001-2013_NESARC.pdf |
| 24 | Carvalho et al. — Alcohol use disorders (Lancet seminar) | Lancet 2019 | 10.1016/S0140-6736(19)31775-1 | Carvalho_2019_LancetSeminarAUD.pdf |
| 25 | Rehm et al. — Global burden of disease and injury and economic cost attributable to alcohol use and alcohol-use disorders | Lancet 2009 | 10.1016/S0140-6736(09)60746-7 | Rehm_2009_GlobalBurdenEconomicCost.pdf |
| 26 | Schuckit — Recognition and management of withdrawal delirium (delirium tremens) | NEJM 2014 | 10.1056/NEJMra1407298 | Schuckit_2014_WithdrawalDelirium.pdf |
| 27 | Mayo-Smith — Pharmacological management of alcohol withdrawal: a meta-analysis and evidence-based practice guideline | JAMA 1997 | 10.1001/jama.1997.03550020076042 | MayoSmith_1997_WithdrawalPharmacologyMA.pdf |
| 28 | Amato et al. — Benzodiazepines for alcohol withdrawal (Cochrane) | Cochrane Database Syst Rev 2010 | 10.1002/14651858.CD005063.pub3 | Amato_2010_Cochrane_BenzodiazepinesWithdrawal.pdf |
| 29 | Jonas et al. — Pharmacotherapy for adults with alcohol use disorders in outpatient settings: a systematic review and meta-analysis | JAMA 2014 | 10.1001/jama.2014.3628 | Jonas_2014_PharmacotherapyAUD_MA.pdf |
| 30 | McPheeters et al. — Pharmacotherapy for alcohol use disorder: a systematic review and meta-analysis (update of #29) | JAMA 2023 | 10.1001/jama.2023.19761 | McPheeters_2023_PharmacotherapyAUD_MA.pdf |
| 31 | Rösner et al. — Opioid antagonists for alcohol dependence (Cochrane; naltrexone) | Cochrane Database Syst Rev 2010 | 10.1002/14651858.CD001867.pub3 | Rosner_2010_Cochrane_OpioidAntagonists.pdf |
| 32 | Rösner et al. — Acamprosate for alcohol dependence (Cochrane) | Cochrane Database Syst Rev 2010 | 10.1002/14651858.CD004332.pub2 | Rosner_2010_Cochrane_Acamprosate.pdf |
| 33 | Anton et al. — Combined pharmacotherapies and behavioral interventions for alcohol dependence: the COMBINE study | JAMA 2006 | 10.1001/jama.295.17.2003 | Anton_2006_COMBINE.pdf |
| 34 | Popova et al. — Estimation of national, regional, and global prevalence of alcohol use during pregnancy and fetal alcohol syndrome: SR/MA | Lancet Glob Health 2017 | 10.1016/S2214-109X(17)30021-9 | Popova_2017_PregnancyDrinkingFASPrevalence.pdf |
| 35 | Lange et al. — Global prevalence of fetal alcohol spectrum disorder among children and youth: SR/MA | JAMA Pediatr 2017 | 10.1001/jamapediatrics.2017.1919 | Lange_2017_GlobalFASDPrevalence.pdf |
| 36 | Jones, Smith, Ulleland & Streissguth — Pattern of malformation in offspring of chronic alcoholic mothers (first description of FAS) | Lancet 1973 | 10.1016/S0140-6736(73)91291-9 | Jones_1973_PatternOfMalformation.pdf |

## Tier B — section backbone (systematic reviews, major cohorts, trials)

| # | Paper | Journal, year | DOI | Save as |
|---|---|---|---|---|
| 37 | Vengeliene et al. — Neuropharmacology of alcohol addiction | Br J Pharmacol 2008 | 10.1038/bjp.2008.30 | Vengeliene_2008_Neuropharmacology.pdf |
| 38 | Abrahao, Salinas & Lovinger — Alcohol and the brain: neuronal molecular targets, synapses, and circuits | Neuron 2017 | 10.1016/j.neuron.2017.10.032 | Abrahao_2017_AlcoholAndTheBrain.pdf |
| 39 | Koob & Volkow — Neurobiology of addiction: a neurocircuitry analysis | Lancet Psychiatry 2016 | 10.1016/S2215-0366(16)00104-8 | _Cross-cutting/Koob_2016_NeurocircuitryAddiction.pdf |
| 40 | Jones — Evidence-based survey of the elimination rates of ethanol from blood with applications in forensic casework | Forensic Sci Int 2010 | 10.1016/j.forsciint.2010.02.021 | Jones_2010_EthanolEliminationRates.pdf |
| 41 | Paton — Alcohol in the body (ABC of alcohol) | BMJ 2005 | 10.1136/bmj.330.7482.85 | Paton_2005_AlcoholInTheBody.pdf |
| 42 | Frezza et al. — High blood alcohol levels in women: the role of decreased gastric alcohol dehydrogenase activity and first-pass metabolism | NEJM 1990 | 10.1056/NEJM199001113220205 | Frezza_1990_WomenFirstPassMetabolism.pdf |
| 43 | Chan & Anderson — Pharmacokinetic and pharmacodynamic drug interactions with ethanol (alcohol) | Clin Pharmacokinet 2014 | 10.1007/s40262-014-0190-x | Chan_2014_DrugInteractionsEthanol.pdf |
| 44 | Topiwala et al. — Moderate alcohol consumption as risk factor for adverse brain outcomes and cognitive decline: longitudinal cohort study (Whitehall II) | BMJ 2017 | 10.1136/bmj.j2353 | Topiwala_2017_ModerateAlcoholBrainOutcomes.pdf |
| 45 | Daviet et al. — Associations between alcohol consumption and gray and white matter volumes in the UK Biobank | Nat Commun 2022 | 10.1038/s41467-022-28735-5 | Daviet_2022_UKBiobankBrainVolumes.pdf |
| 46 | Mackey et al. (ENIGMA Addiction) — Mega-analysis of gray matter volume in substance dependence: general and substance-specific regional effects | Am J Psychiatry 2019 | 10.1176/appi.ajp.2018.17040415 | _Cross-cutting/Mackey_2019_ENIGMA_GrayMatterMegaAnalysis.pdf |
| 47 | Harper — The neuropathology of alcohol-related brain damage | Alcohol Alcohol 2009 | 10.1093/alcalc/agn102 | Harper_2009_NeuropathologyARBD.pdf |
| 48 | Kopelman et al. — The Korsakoff syndrome: clinical aspects, psychology and treatment | Alcohol Alcohol 2009 | 10.1093/alcalc/agn118 | Kopelman_2009_KorsakoffSyndrome.pdf |
| 49 | Rehm et al. — Alcohol use and dementia: a systematic scoping review | Alzheimers Res Ther 2019 | 10.1186/s13195-018-0453-0 | Rehm_2019_AlcoholDementiaScopingReview.pdf |
| 50 | Schwarzinger et al. — Contribution of alcohol use disorders to the burden of dementia in France 2008–13: a nationwide retrospective cohort study | Lancet Public Health 2018 | 10.1016/S2468-2667(18)30022-7 | Schwarzinger_2018_AUDDementiaFrance.pdf |
| 51 | Sabia et al. — Alcohol consumption and risk of dementia: 23 year follow-up of Whitehall II cohort study | BMJ 2018 | 10.1136/bmj.k2927 | Sabia_2018_AlcoholDementiaWhitehall.pdf |
| 52 | Mewton et al. — The relationship between alcohol use and dementia in adults aged more than 60 years: combined analysis of individual-participant data from 15 international studies (correction published; obtain both) | Addiction 2023 | 10.1111/add.16035 | Mewton_2023_AlcoholDementia15Studies.pdf |
| 53 | Dry et al. — Dose-related effects of alcohol on cognitive functioning | PLOS One 2012 | 10.1371/journal.pone.0050977 | Dry_2012_DoseRelatedCognitiveEffects.pdf |
| 54 | Zador, Krawchuk & Voas — Alcohol-related relative risk of driver fatalities and driver involvement in fatal crashes in relation to driver age and gender: an update using 1996 data | J Stud Alcohol 2000 | 10.15288/jsa.2000.61.387 | Zador_2000_DriverFatalityRelativeRisk.pdf |
| 55 | Blomberg et al. — The Long Beach/Fort Lauderdale relative risk study (BAC and crash risk) | J Safety Res 2009 | 10.1016/j.jsr.2009.07.002 | Blomberg_2009_LongBeachFortLauderdale.pdf |
| 56 | Taylor et al. — The more you drink, the harder you fall: SR/MA of how acute alcohol consumption and injury or collision risk increase together | Drug Alcohol Depend 2010 | 10.1016/j.drugalcdep.2010.02.011 | Taylor_2010_AcuteAlcoholInjuryMA.pdf |
| 57 | Wetherill & Fromme — Alcohol-induced blackouts: a review of recent clinical research with practical implications | Alcohol Clin Exp Res 2016 | 10.1111/acer.13051 | Wetherill_2016_BlackoutsReview.pdf |
| 58 | Bushman & Cooper — Effects of alcohol on human aggression: an integrative research review | Psychol Bull 1990 | 10.1037/0033-2909.107.3.341 | Bushman_1990_AlcoholAggressionReview.pdf |
| 59 | Ebrahim et al. — Alcohol and sleep I: effects on normal sleep | Alcohol Clin Exp Res 2013 | 10.1111/acer.12006 | Ebrahim_2013_AlcoholAndSleep.pdf |
| 60 | Vonghia et al. — Acute alcohol intoxication | Eur J Intern Med 2008 | 10.1016/j.ejim.2007.06.033 | Vonghia_2008_AcuteAlcoholIntoxication.pdf |
| 61 | Mayo-Smith et al. — Management of alcohol withdrawal delirium: an evidence-based practice guideline | Arch Intern Med 2004 | 10.1001/archinte.164.13.1405 | MayoSmith_2004_WithdrawalDeliriumGuideline.pdf |
| 62 | Saitz et al. — Individualized treatment for alcohol withdrawal: a randomized double-blind controlled trial (symptom-triggered dosing) | JAMA 1994 | 10.1001/jama.1994.03520070039035 | Saitz_1994_SymptomTriggeredRCT.pdf |
| 63 | Sullivan et al. — Assessment of alcohol withdrawal: the revised Clinical Institute Withdrawal Assessment for Alcohol scale (CIWA-Ar) | Br J Addict 1989 | 10.1111/j.1360-0443.1989.tb00737.x | Sullivan_1989_CIWA-Ar.pdf |
| 64 | Minozzi et al. — Anticonvulsants for alcohol withdrawal (Cochrane) | Cochrane Database Syst Rev 2010 | 10.1002/14651858.CD005064.pub3 | Minozzi_2010_Cochrane_AnticonvulsantsWithdrawal.pdf |
| 65 | Goodson et al. — Predictors of severe alcohol withdrawal syndrome: a systematic review and meta-analysis † | Alcohol Clin Exp Res 2014 | 10.1111/acer.12529 | Goodson_2014_PredictorsSevereAWS_MA.pdf |
| 65a | Eyer et al. — Risk assessment of moderate to severe alcohol withdrawal: predictors for seizures and delirium tremens in the course of withdrawal | Alcohol Alcohol 2011 | 10.1093/alcalc/agr053 | Eyer_2011_PredictorsSeizuresDT.pdf |
| 66 | Volpicelli et al. — Naltrexone in the treatment of alcohol dependence | Arch Gen Psychiatry 1992 | 10.1001/archpsyc.1992.01820110040006 | Volpicelli_1992_NaltrexoneRCT.pdf |
| 67 | O'Malley et al. — Naltrexone and coping skills therapy for alcohol dependence: a controlled study | Arch Gen Psychiatry 1992 | 10.1001/archpsyc.1992.01820110045007 | OMalley_1992_NaltrexoneCopingSkillsRCT.pdf |
| 68 | Maisel et al. — Meta-analysis of naltrexone and acamprosate for treating alcohol use disorders: when are these medications most helpful? | Addiction 2013 | 10.1111/j.1360-0443.2012.04054.x | Maisel_2013_NaltrexoneAcamprosateMA.pdf |
| 69 | Skinner et al. — Disulfiram efficacy in the treatment of alcohol dependence: a meta-analysis | PLOS One 2014 | 10.1371/journal.pone.0087366 | Skinner_2014_DisulfiramMA.pdf |
| 70 | Mann et al. — Extending the treatment options in alcohol dependence: a randomized controlled study of as-needed nalmefene (ESENSE 1) | Biol Psychiatry 2013 | 10.1016/j.biopsych.2012.10.020 | Mann_2013_NalmefeneESENSE1.pdf |
| 71 | Palpacuer et al. — Risks and benefits of nalmefene in the treatment of adult alcohol dependence: SR/MA of published and unpublished double-blind RCTs (critique of #70) | PLOS Med 2015 | 10.1371/journal.pmed.1001924 | Palpacuer_2015_NalmefeneRisksBenefitsMA.pdf |
| 72 | Palpacuer et al. — Pharmacologically controlled drinking in the treatment of alcohol dependence or AUD: SR with direct and network meta-analyses on nalmefene, naltrexone, acamprosate, baclofen and topiramate † | Addiction 2018 | 10.1111/add.13974 | Palpacuer_2018_ControlledDrinkingNetworkMA.pdf |
| 73 | Addolorato et al. — Effectiveness and safety of baclofen for maintenance of alcohol abstinence in alcohol-dependent patients with liver cirrhosis: RCT | Lancet 2007 | 10.1016/S0140-6736(07)61814-5 | Addolorato_2007_BaclofenCirrhosisRCT.pdf |
| 74 | Agabio et al. — Baclofen for alcohol use disorder (Cochrane; supersedes Minozzi 2018 pub2) | Cochrane Database Syst Rev 2023 | 10.1002/14651858.CD012557.pub3 | Agabio_2023_Cochrane_Baclofen.pdf |
| 75 | Rose & Jones — Baclofen: its effectiveness in reducing harmful drinking, craving, and negative mood. A meta-analysis | Addiction 2018 | 10.1111/add.14191 | Rose_2018_BaclofenMA.pdf |
| 76 | Johnson et al. — Topiramate for treating alcohol dependence: a randomized controlled trial | JAMA 2007 | 10.1001/jama.298.14.1641 | Johnson_2007_TopiramateRCT.pdf |
| 77 | Blodgett et al. — A meta-analysis of topiramate's effects for individuals with alcohol use disorders | Alcohol Clin Exp Res 2014 | 10.1111/acer.12411 | Blodgett_2014_TopiramateMA.pdf |
| 78 | Mason et al. — Gabapentin treatment for alcohol dependence: a randomized clinical trial | JAMA Intern Med 2014 | 10.1001/jamainternmed.2013.11950 | Mason_2014_GabapentinRCT.pdf |
| 79 | Anton et al. — Efficacy of gabapentin for the treatment of AUD in patients with alcohol withdrawal symptoms: RCT | JAMA Intern Med 2020 | 10.1001/jamainternmed.2020.0249 | Anton_2020_GabapentinWithdrawalSymptomsRCT.pdf |
| 80 | Kranzler et al. — A meta-analysis of the efficacy of gabapentin for treating alcohol use disorder | Addiction 2019 | 10.1111/add.14655 | Kranzler_2019_GabapentinMA.pdf |
| 81 | Bogenschutz et al. — Percentage of heavy drinking days following psilocybin-assisted psychotherapy vs placebo in the treatment of adult patients with AUD: RCT | JAMA Psychiatry 2022 | 10.1001/jamapsychiatry.2022.2096 | Bogenschutz_2022_PsilocybinAUD_RCT.pdf |
| 82 | Grabski et al. — Adjunctive ketamine with relapse prevention–based psychological therapy in the treatment of alcohol use disorder | Am J Psychiatry 2022 | 10.1176/appi.ajp.2021.21030277 | Grabski_2022_KetamineAUD_RCT.pdf |
| 82a | Hendershot et al. — Once-weekly semaglutide in adults with alcohol use disorder: a randomized clinical trial | JAMA Psychiatry 2025 | 10.1001/jamapsychiatry.2024.4789 | Hendershot_2025_SemaglutideAUD_RCT.pdf |
| 83 | Project MATCH Research Group — Matching alcoholism treatments to client heterogeneity: Project MATCH posttreatment drinking outcomes | J Stud Alcohol 1997 | 10.15288/jsa.1997.58.7 | ProjectMATCH_1997_PosttreatmentOutcomes.pdf |
| 84 | Kelly et al. — Alcoholics Anonymous and other 12-step programs for alcohol use disorder (Cochrane) | Cochrane Database Syst Rev 2020 | 10.1002/14651858.CD012880.pub2 | Kelly_2020_Cochrane_AA12Step.pdf |
| 85 | Kaner et al. — Effectiveness of brief alcohol interventions in primary care populations (Cochrane) | Cochrane Database Syst Rev 2018 | 10.1002/14651858.CD004148.pub4 | Kaner_2018_Cochrane_BriefInterventions.pdf |
| 86 | Mekonen et al. — Treatment rates for alcohol use disorders: a systematic review and meta-analysis | Addiction 2021 | 10.1111/add.15357 | Mekonen_2021_TreatmentRatesMA.pdf |
| 87 | Saunders et al. — Development of the Alcohol Use Disorders Identification Test (AUDIT) | Addiction 1993 | 10.1111/j.1360-0443.1993.tb02093.x | Saunders_1993_AUDIT.pdf |
| 88 | Bush et al. — The AUDIT alcohol consumption questions (AUDIT-C): an effective brief screening test for problem drinking | Arch Intern Med 1998 | 10.1001/archinte.158.16.1789 | Bush_1998_AUDIT-C.pdf |
| 89 | Penning et al. — The pathology of alcohol hangover | Curr Drug Abuse Rev 2010 | 10.2174/1874473711003020068 | Penning_2010_PathologyOfHangover.pdf |
| 90 | Verster et al. — The Alcohol Hangover Research Group consensus statement on best practice in alcohol hangover research | Curr Drug Abuse Rev 2010 | 10.2174/1874473711003020116 | Verster_2010_AHRGConsensus.pdf |
| 91 | Pittler, Verster & Ernst — Interventions for preventing or treating alcohol hangover: systematic review of randomised controlled trials | BMJ 2005 | 10.1136/bmj.331.7531.1515 | Pittler_2005_HangoverInterventionsSR.pdf |
| 92 | Roberts et al. — Efficacy and tolerability of pharmacologically active interventions for alcohol-induced hangover symptomatology: systematic review of placebo-controlled RCTs | Addiction 2022 | 10.1111/add.15786 | Roberts_2022_HangoverInterventionsSR.pdf |
| 93 | Wiese, Shlipak & Browner — The alcohol hangover | Ann Intern Med 2000 | 10.7326/0003-4819-132-11-200006060-00008 | Wiese_2000_TheAlcoholHangover.pdf |
| 94 | van der Schrier et al. — Influence of ethanol on oxycodone-induced respiratory depression: a dose-escalating study in young and elderly individuals | Anesthesiology 2017 | 10.1097/ALN.0000000000001505 | vanderSchrier_2017_EthanolOxycodoneRespiratoryDepression.pdf |
| 95 | Tanaka — Toxicological interactions between alcohol and benzodiazepines | J Toxicol Clin Toxicol 2002 | 10.1081/CLT-120002887 | Tanaka_2002_AlcoholBenzodiazepineInteractions.pdf |
| 96 | Pennings, Leccese & Wolff — Effects of concurrent use of alcohol and cocaine | Addiction 2002 | 10.1046/j.1360-0443.2002.00158.x | Pennings_2002_AlcoholCocaine.pdf |
| 97 | McKetin, Coen & Kaye — A comprehensive review of the effects of mixing caffeinated energy drinks with alcohol | Drug Alcohol Depend 2015 | 10.1016/j.drugalcdep.2015.01.047 | _Cross-cutting/McKetin_2015_EnergyDrinksAlcoholReview.pdf |
| 98 | Boden & Fergusson — Alcohol and depression | Addiction 2011 | 10.1111/j.1360-0443.2010.03351.x | Boden_2011_AlcoholAndDepression.pdf |
| 99 | Grant et al. — Prevalence and co-occurrence of substance use disorders and independent mood and anxiety disorders (NESARC) | Arch Gen Psychiatry 2004 | 10.1001/archpsyc.61.8.807 | _Cross-cutting/Grant_2004_SUD_MoodAnxietyComorbidity_NESARC.pdf |
| 100 | Borges et al. — A meta-analysis of acute use of alcohol and the risk of suicide attempt | Psychol Med 2017 | 10.1017/S0033291716002841 | Borges_2017_AcuteAlcoholSuicideAttemptMA.pdf |
| 101 | Samokhvalov, Rehm & Roerecke — Alcohol consumption as a risk factor for acute and chronic pancreatitis: SR and series of meta-analyses | EBioMedicine 2015 | 10.1016/j.ebiom.2015.11.023 | Samokhvalov_2015_PancreatitisMA.pdf |
| 102 | Julian et al. — Alcohol-related peripheral neuropathy: a systematic review and meta-analysis | J Neurol 2019 | 10.1007/s00415-018-9123-1 | Julian_2019_PeripheralNeuropathyMA.pdf |
| 103 | Knott et al. — Alcohol consumption and the risk of type 2 diabetes: SR and dose–response MA of >1.9 million individuals | Diabetes Care 2015 | 10.2337/dc15-0710 | Knott_2015_Type2DiabetesMA.pdf |
| 104 | Larsson et al. — Differing association of alcohol consumption with different stroke types: a systematic review and meta-analysis | BMC Med 2016 | 10.1186/s12916-016-0721-4 | Larsson_2016_StrokeTypesMA.pdf |
| 105 | Verhulst, Neale & Kendler — The heritability of alcohol use disorders: a meta-analysis of twin and adoption studies | Psychol Med 2015 | 10.1017/S0033291714002165 | Verhulst_2015_HeritabilityAUD_MA.pdf |
| 106 | Zhou et al. — Genome-wide meta-analysis of problematic alcohol use in 435,563 individuals | Nat Neurosci 2020 | 10.1038/s41593-020-0643-5 | Zhou_2020_GWASProblematicAlcoholUse.pdf |
| 107 | Schuckit — Low level of response to alcohol as a predictor of future alcoholism | Am J Psychiatry 1994 | 10.1176/ajp.151.2.184 | Schuckit_1994_LowLevelOfResponse.pdf |
| 108 | Squeglia et al. — Brain development in heavy-drinking adolescents | Am J Psychiatry 2015 | 10.1176/appi.ajp.2015.14101249 | Squeglia_2015_AdolescentBrainDevelopment.pdf |
| 109 | Grant & Dawson — Age at onset of alcohol use and its association with DSM-IV alcohol abuse and dependence (NLAES) | J Subst Abuse 1997 | 10.1016/S0899-3289(97)90009-2 | Grant_1997_AgeAtOnset_NLAES.pdf |

## Tier C — epidemiology, mortality, policy, harm reduction, pregnancy

| # | Paper | Journal, year | DOI | Save as |
|---|---|---|---|---|
| 110 | Hasin et al. — Prevalence, correlates, disability, and comorbidity of DSM-IV alcohol abuse and dependence in the United States (NESARC) | Arch Gen Psychiatry 2007 | 10.1001/archpsyc.64.7.830 | Hasin_2007_DSMIV_AUD_NESARC.pdf |
| 111 | Manthey et al. — Global alcohol exposure between 1990 and 2017 and forecasts until 2030: a modelling study | Lancet 2019 | 10.1016/S0140-6736(18)32744-2 | Manthey_2019_GlobalExposureForecasts.pdf |
| 112 | Rehm et al. — The relationship between different dimensions of alcohol use and the burden of disease—an update | Addiction 2017 | 10.1111/add.13757 | Rehm_2017_DimensionsBurdenUpdate.pdf |
| 113 | Shield et al. — National, regional, and global burdens of disease from 2000 to 2016 attributable to alcohol use: a comparative risk assessment study | Lancet Public Health 2020 | 10.1016/S2468-2667(19)30231-2 | Shield_2020_AttributableBurden2000-2016.pdf |
| 114 | Knott et al. — All cause mortality and the case for age specific alcohol consumption guidelines: pooled analyses of up to 10 population based cohorts | BMJ 2015 | 10.1136/bmj.h384 | Knott_2015_AgeSpecificGuidelinesMortality.pdf |
| 115 | Vaillant — A 60-year follow-up of alcoholic men | Addiction 2003 | 10.1046/j.1360-0443.2003.00422.x | Vaillant_2003_60YearFollowUp.pdf |
| 116 | Allen et al. — Moderate alcohol intake and cancer incidence in women (Million Women Study) | J Natl Cancer Inst 2009 | 10.1093/jnci/djn514 | Allen_2009_ModerateIntakeCancerWomen.pdf |
| 117 | Collaborative Group on Hormonal Factors in Breast Cancer (Hamajima et al.) — Alcohol, tobacco and breast cancer: collaborative reanalysis of individual data from 53 epidemiological studies | Br J Cancer 2002 | 10.1038/sj.bjc.6600596 | Hamajima_2002_BreastCancerReanalysis.pdf |
| 118 | Thursz et al. (EASL) — EASL Clinical Practice Guidelines: management of alcohol-related liver disease | J Hepatol 2018 | 10.1016/j.jhep.2018.03.018 | EASL_2018_AlcoholRelatedLiverDiseaseCPG.pdf |
| 119 | Wagenaar, Salois & Komro — Effects of beverage alcohol price and tax levels on drinking: a meta-analysis of 1003 estimates from 112 studies | Addiction 2009 | 10.1111/j.1360-0443.2008.02438.x | Wagenaar_2009_PriceTaxDrinkingMA.pdf |
| 120 | Wagenaar, Tobler & Komro — Effects of alcohol tax and price policies on morbidity and mortality: a systematic review | Am J Public Health 2010 | 10.2105/AJPH.2009.186007 | Wagenaar_2010_TaxPriceMorbidityMortalitySR.pdf |
| 121 | Wyper et al. — Evaluating the impact of alcohol minimum unit pricing on deaths and hospitalisations in Scotland: a controlled interrupted time series study | Lancet 2023 | 10.1016/S0140-6736(23)00497-X | Wyper_2023_MinimumUnitPricingScotland.pdf |
| 122 | Anderson, Chisholm & Fuhr — Effectiveness and cost-effectiveness of policies and programmes to reduce the harm caused by alcohol | Lancet 2009 | 10.1016/S0140-6736(09)60744-3 | Anderson_2009_PoliciesEffectiveness.pdf |
| 123 | Kalinowski & Humphreys — Governmental standard drink definitions and low-risk alcohol consumption guidelines in 37 countries | Addiction 2016 | 10.1111/add.13341 | Kalinowski_2016_StandardDrinkDefinitions.pdf |
| 124 | Podymow et al. — Shelter-based managed alcohol administration to chronically homeless people addicted to alcohol | CMAJ 2006 | 10.1503/cmaj.1041350 | Podymow_2006_ManagedAlcoholProgram.pdf |
| 125 | Day et al. — Thiamine for prevention and treatment of Wernicke-Korsakoff syndrome in people who abuse alcohol (Cochrane) | Cochrane Database Syst Rev 2013 | 10.1002/14651858.CD004033.pub3 | Day_2013_Cochrane_Thiamine.pdf |
| 126 | May et al. — Prevalence of fetal alcohol spectrum disorders in 4 US communities | JAMA 2018 | 10.1001/jama.2017.21896 | May_2018_FASDPrevalence4USCommunities.pdf |
| 127 | Hoyme et al. — Updated clinical guidelines for diagnosing fetal alcohol spectrum disorders | Pediatrics 2016 | 10.1542/peds.2015-4256 | Hoyme_2016_FASDDiagnosticGuidelines.pdf |
| 128 | Popova et al. — Fetal alcohol spectrum disorders (primer) | Nat Rev Dis Primers 2023 | 10.1038/s41572-023-00420-x | Popova_2023_FASDPrimer.pdf |
| 129 | Henderson, Gray & Brocklehurst — Systematic review of effects of low–moderate prenatal alcohol exposure on pregnancy outcome (erratum published; obtain both) | BJOG 2007 | 10.1111/j.1471-0528.2006.01163.x | Henderson_2007_LowModeratePAE_SR.pdf |
| 130 | Flak et al. — The association of mild, moderate, and binge prenatal alcohol exposure and child neuropsychological outcomes: a meta-analysis | Alcohol Clin Exp Res 2014 | 10.1111/acer.12214 | Flak_2014_PAE_NeuropsychOutcomesMA.pdf |
| 131 | Mamluk et al. — Low alcohol consumption and pregnancy and childhood outcomes: time to change guidelines indicating apparently 'safe' levels? SR/MA | BMJ Open 2017 | 10.1136/bmjopen-2016-015410 | Mamluk_2017_LowAlcoholPregnancyMA.pdf |

† = verified from the Crossref works-search record for that DOI (title, journal, year, author and `updated-by` field returned by Crossref), because the `works/<DOI>` endpoint was rate-limited at the time; a `works/<DOI>` re-check is recommended when the PubMed layer is run.

## Reports (no DOI; save the PDF of the full report)

| # | Report | Save as |
|---|---|---|
| R1 | WHO — Global status report on alcohol and health and treatment of substance use disorders (2024) | _Epidemiology/WHO_2024_GlobalStatusReportAlcohol.pdf |
| R2 | NIAAA — Alcohol Facts and Statistics / Alcohol-Related Emergencies and Deaths (latest) | _Epidemiology/NIAAA_latest_AlcoholFactsStatistics.pdf |
| R3 | SAMHSA — NSDUH 2024 detailed tables (alcohol use, binge and heavy use, AUD) | _Epidemiology/SAMHSA_2024_NSDUH_DetailedTables.pdf (shared with other substances) |
| R4 | EUDA / ESPAD — ESPAD Report 2024 (adolescent alcohol use in Europe) | _Epidemiology/ESPAD_2024_Report.pdf |
| R5 | OECD — Preventing Harmful Alcohol Use (2021) | _Epidemiology/OECD_2021_PreventingHarmfulAlcoholUse.pdf |
| R6 | IARC Monographs Vol. 100E — Personal habits and indoor combustions (alcohol consumption chapter) | _Epidemiology/IARC_2012_Monograph100E_Alcohol.pdf |
| R7 | NIAAA — Alcohol and the Hispanic Community / US Dietary Guidelines 2020–2025 (alcohol section) | _Epidemiology/USDA_2020_DietaryGuidelines_Alcohol.pdf |
| R8 | Greek data — ΕΚΤΕΠΝ/ΟΚΑΝΑ annual report (alcohol section); ΕΛΣΤΑΤ alcohol-attributable deaths | _Epidemiology/EKTEPN_latest_AnnualReport.pdf |

## Known gaps this list does not yet cover (to come from the PubMed layer)

Items recalled but not verifiable before the rate limit closed the session: Roerecke et al. 2017 Lancet Public Health (effect of reducing alcohol consumption on blood pressure, SR/MA); Fillmore et al. 2006 Addiction Research & Theory (moderate alcohol use and reduced mortality risk: systematic error in prospective studies — the original abstainer-bias paper); Wood et al. 2018 JAMA Rational Clinical Examination (will this hospitalized patient develop severe alcohol withdrawal syndrome?); Corrao et al. 1999 Addiction (dose-response meta-analysis for several alcohol-related conditions; Crossref search hit 10.1046/j.1360-0443.1999.9410155111.x, works fetch refused); Cederbaum 2012 Clin Liver Dis (alcohol metabolism); Dawson et al. 2005 Addiction (recovery from DSM-IV alcohol dependence, NESARC); Darvishi et al. 2015 PLOS One (alcohol and suicide meta-analysis); Rehm et al. 2003 Addiction (volume and patterns and burden of disease); Babor et al. 2010 Addiction (Alcohol: No Ordinary Commodity summary); Shults et al. 2001 Am J Prev Med (interventions to reduce alcohol-impaired driving); Piano 2002 Chest (alcoholic cardiomyopathy); Li, Zhao & Gelernter 2012 Hum Genet (ALDH2*2 protective effect); Kelly et al. 2009 Int J Epidemiol and Lees et al. 2020 Am J Psychiatry (light prenatal drinking cohorts); ASAM 2020 J Addict Med alcohol withdrawal management guideline; Tucker et al. 2020 Alcohol Res (epidemiology of recovery). Cross-cutting dependence-probability papers (Anthony 1994; Lopez-Quintero 2011) are already on the methamphetamine list under `_Cross-cutting/`. Not yet covered at all: alcohol and infection/immunity; atrial fibrillation meta-analyses; alcohol and tuberculosis; drink-driving legal limits by jurisdiction; Greek alcohol epidemiology; alcohol-free beverage and industry-funding critiques of the J-curve literature (beyond #5–9); older adults; sex-specific harm thresholds beyond #4 and #20; wastewater and sales data.

## Verification block

- DOIs fetched: 140 distinct DOI fetch attempts via `works/<DOI>` (including case-variant re-tries after HTTP 429 refusals or transient CLIENT_ERRORs; a refused URL was never re-fetched as written), plus 3 targeted works-search records.
- Resolved to the intended paper: 134 papers listed (132 by `works/<DOI>`; 2 by Crossref works-search record, marked †).
- Dropped (resolved to a different paper): 10.1111/acer.12504 (resolves to Monk et al. 2014, not Goodson 2014 — corrected to 10.1111/acer.12529); 10.1111/add.14058 (resolves to Rubenis et al. 2017, not Palpacuer 2018 — corrected to 10.1111/add.13974); 10.1111/j.1360-0443.2005.01010.x (resolves to a Casswell 2005 commentary, not Dawson 2005 — Dawson left in Known gaps).
- Not resolvable in this session (CLIENT_ERROR on repeat, no search possible under the rate limit): 10.1016/S2468-2667(17)30003-8 (Roerecke 2017), 10.1080/16066350600806467 (Fillmore 2006), 10.1001/jama.2018.10401 (Wood 2018 JAMA), 10.1016/j.cld.2012.08.002 (Cederbaum 2012) — all moved to Known gaps.
- Errata/corrections (keep, obtain both): #3 Bryazka 2022 (erratum 10.1016/S0140-6736(22)01389-7); #4 Wood 2018 (erratum 10.1016/S0140-6736(18)31168-1); #52 Mewton 2023 (correction 10.1111/add.16512); #129 Henderson 2007 (erratum 10.1111/j.1471-0528.2007.01431.x). Superseded version noted: Minozzi 2018 baclofen Cochrane (CD012557.pub2) is updated by Agabio 2023 (pub3), which is the one listed.
- Retractions: none found.
