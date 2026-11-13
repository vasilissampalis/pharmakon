# DayAfter — evidence map and PDF list for "The day after", every drug page (v0.1, 2026-10-25)

Cross-cutting topic requested by the senior author: for each of the 30 drugs in `data/site/substances.json`, the evidence on (1) **after-effects** in the hours and days after use (hangover, comedown, crash, low mood in the following days, poor sleep, tiredness, next-day impairment, rebound anxiety) and (2) **what people do about them and whether it works** (supplements and vitamins, foods and drinks, water and electrolytes, sleep, exercise, over-the-counter and prescribed medicines, and using another drug to come down): helped, harmed, or never tested, with its risks. Findings only: the list serves a page that will never give amounts, timings or regimens, and papers whose aim is to make a drug's wanted effects stronger were skipped unless they report harms. Reading list only: no claims, no study cards. Run by AI reader 103 (brief `scratchpad/dayafter/BRIEF-reader103.md`).

How this list was built: PubMed through the E-utilities interface (`esearch`, `esummary`; `efetch` abstracts where a title did not show the design) in a tab of the app's browser that this reader opened, 2–6 searches per drug plus known-item checks (strings, hit counts and what was kept: `DayAfter_search-log.md`). Order of preference: systematic reviews and meta-analyses (Cochrane first); randomised trials; large observational and naturalistic studies; human laboratory studies; authoritative reviews. Animal studies only where nothing human exists, marked as such. A popular remedy with no human study is recorded as a finding under that drug's **Known gaps**. Each drug's existing list (`search-logs/<Folder>_DOI-LIST.md`) and the cross-cutting lists were checked first; papers already on them are named in an "Already on other lists" line instead of being listed again.

**Columns.** **DOI**: every DOI was fetched from Crossref `works/<DOI>` in the browser tab on 2026-10-25 and matched to the PubMed record on title, year and first author; its `updated-by` field was read (corrections, retractions). Where Crossref's year (online) and PubMed's year (print issue) differ, the print year is given with the online year in brackets. **Free?**: `PMCxxxxxxx` = free full text in PubMed Central (from the PubMed record or OpenAlex); `publisher` = OpenAlex `open_access` shows the article free at the publisher (gold, hybrid, bronze or diamond); `—` = neither (a copy in an institutional repository, OpenAlex "green", is not counted). Free papers can be read by AI readers without the senior author saving them.

**Tiers.** A = read first: the backbone review or best study of each drug's after-effects, and the best evidence on each remedy that has been tested. B = further human studies, reviews and risk evidence.

Save each PDF under `PDFs/` with the path given (drug folder from `docs/TIER1.md`, or `_Cross-cutting/` for papers that span several drugs).

---

## 1. Alcohol (ethanol) — `PDFs/Alcohol/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 1 | Gunn et al. — A systematic review of the next-day effects of heavy alcohol consumption on cognitive performance | Addiction 2018 | 10.1111/add.14404 | PMC6282576 | Alcohol/Gunn_2018_NextDayCognitionSR.pdf |
| 2 | Rothman et al. — A systematic review of the impact of the alcohol hangover upon negative affect | Drug Alcohol Rev 2026 (online 2025) | 10.1111/dar.70052 | publisher | Alcohol/Rothman_2026_HangoverNegativeAffectSR.pdf |
| 3 | Gardiner et al. — The effect of alcohol on subsequent sleep in healthy adults: a systematic review and meta-analysis | Sleep Med Rev 2025 | 10.1016/j.smrv.2024.102030 | publisher | Alcohol/Gardiner_2025_AlcoholSubsequentSleepMA.pdf |
| 4 | Mackus et al. — Alcohol hangover versus dehydration revisited: the effect of drinking water to prevent or alleviate the alcohol hangover | Alcohol 2024 | 10.1016/j.alcohol.2024.07.006 | publisher | Alcohol/Mackus_2024_HangoverDehydrationWater.pdf |
| 5 | Imai et al. — Water intake during drinking does not alleviate hangover symptoms | Front Pharmacol 2026 | 10.3389/fphar.2026.1852528 | PMC13311531 | Alcohol/Imai_2026_WaterDuringDrinkingTrial.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 6 | Verster et al. — Effects of alcohol hangover on simulated highway driving performance | Psychopharmacology (Berl) 2014 | 10.1007/s00213-014-3474-9 | — | Alcohol/Verster_2014_HangoverSimulatedDriving.pdf |
| 7 | Alford et al. — The impact of alcohol hangover on simulated driving performance during a 'commute to work' — zero and residual alcohol effects compared | J Clin Med 2020 | 10.3390/jcm9051435 | PMC7291334 | Alcohol/Alford_2020_HangoverCommuteDriving.pdf |
| 8 | Rantakömi et al. — Hangover and the risk of stroke in middle-aged men | Acta Neurol Scand 2013 (online 2012) | 10.1111/j.1600-0404.2012.01696.x | — | Alcohol/Rantakomi_2013_HangoverStrokeRisk.pdf |
| 9 | Jayawardena et al. — Interventions for treatment and/or prevention of alcohol hangover: systematic review | Hum Psychopharmacol 2017 | 10.1002/hup.2600 | publisher | Alcohol/Jayawardena_2017_HangoverInterventionsSR.pdf |
| 10 | Coppersmith et al. — The use of N-acetylcysteine in the prevention of hangover: a randomized trial (author correction 10.1038/s41598-021-94669-5) | Sci Rep 2021 | 10.1038/s41598-021-92676-0 | PMC8238992 | Alcohol/Coppersmith_2021_NACHangoverRCT.pdf |
| 11 | Eriksson et al. — L-cysteine containing vitamin supplement which prevents or alleviates alcohol-related hangover symptoms: nausea, headache, stress and anxiety (corrigendum 10.1093/alcalc/agaa088, from PubMed; not in Crossref updated-by) | Alcohol Alcohol 2020 | 10.1093/alcalc/agaa082 | — | Alcohol/Eriksson_2020_LCysteineVitaminRCT.pdf |
| 12 | Rohsenow et al. — Effects of caffeinated vs. non-caffeinated alcoholic beverage on next-day hangover incidence and severity, perceived sleep quality, and alertness | Addict Behav 2014 | 10.1016/j.addbeh.2013.09.008 | PMC3864634 | Alcohol/Rohsenow_2014_CaffeinatedAlcoholHangoverRCT.pdf |
| 13 | Köchling et al. — Grape or grain but never the twain? A randomized controlled multiarm matched-triplet crossover trial of beer and wine | Am J Clin Nutr 2019 | 10.1093/ajcn/nqy309 | PMC6410559 | Alcohol/Kochling_2019_BeerWineOrderRCT.pdf |
| 14 | Morley et al. — Daily experiences of hangover severity and food consumption in young adults | Br J Health Psychol 2022 (online 2021) | 10.1111/bjhp.12555 | — | Alcohol/Morley_2022_HangoverFoodDiary.pdf |
| 15 | Verster — Editorial: the "hair of the dog": a useful hangover remedy or a predictor of future problem drinking? | Curr Drug Abuse Rev 2009 | 10.2174/1874473710902010001 | — | Alcohol/Verster_2009_HairOfTheDog.pdf |
| 16 | Verster et al. — Unknown safety and efficacy of alcohol hangover treatments puts consumers at risk | Addict Behav 2021 | 10.1016/j.addbeh.2021.107029 | publisher | Alcohol/Verster_2021_HangoverProductsSafety.pdf |
| 17 | Han et al. — Association of over the counter "hangover remedy" use with alcohol use problems and consumption patterns among young adults | Alcohol Alcohol 2024 (online 2023) | 10.1093/alcalc/agad081 | PMC10794163 | Alcohol/Han_2024_HangoverRemedyUseProblems.pdf |
| 18 | McGregor — Pueraria lobata (kudzu root) hangover remedies and acetaldehyde-associated neoplasm risk | Alcohol 2007 | 10.1016/j.alcohol.2007.07.009 | — | Alcohol/McGregor_2007_KudzuAcetaldehydeRisk.pdf |
| 19 | Rumack et al. — Effect of therapeutic doses of acetaminophen on serum alanine aminotransferase levels in subjects consuming ethanol: systematic review and meta-analysis (title shortened) | Pharmacotherapy 2012 | 10.1002/j.1875-9114.2012.01122.x | PMC3561770 | Alcohol/Rumack_2012_AcetaminophenEthanolALT_MA.pdf |
| 20 | Kaufman et al. — The risk of acute major upper gastrointestinal bleeding among users of aspirin and ibuprofen at various levels of alcohol consumption | Am J Gastroenterol 1999 | 10.1111/j.1572-0241.1999.01517.x | — | Alcohol/Kaufman_1999_AspirinIbuprofenAlcoholGIBleeding.pdf |

**Already on other lists (not repeated):** Alcohol #91 Pittler, Verster & Ernst 2005 (systematic review of RCTs of hangover interventions; PMC1322250) and #92 Roberts et al. 2022 (systematic review of placebo-controlled RCTs; publisher), both Tier A for this page; Alcohol #89 Penning et al. 2010 (pathology of hangover), #90 Verster et al. 2010 (Alcohol Hangover Research Group consensus; PMC3827719) and #93 Wiese et al. 2000 (review), Tier B for this page.

**Also needed:** Waddell et al. 2022 (alcohol hangovers when cannabis is used at the same time) under Cannabis; Angarita et al. 2016 (sleep abnormalities across drugs) in Cross-cutting. Pennings et al. 2002 (alcohol used to temper the cocaine comedown) is already Alcohol #96.

**Known gaps.** The after-effects themselves are well covered (next-day cognition, mood, sleep, driving). Remedy evidence is thin: the three systematic reviews (Pittler 2005 and Roberts 2022, already listed; Jayawardena 2017) rest on small, mostly single trials, and the many recent trials of supplements sold in East Asia (red ginseng, Hovenia dulcis, Korean pear juice, probiotics, glutathione, hydrogen) were not listed one by one. Water has one small crossover trial (Imai 2026, 13 men) and a review. Food has only a daily-diary study. No human trial was found of electrolyte drinks or oral rehydration solutions, intravenous 'drip' hydration, exercise, extra sleep or coffee the morning after; minerals (magnesium, zinc) have only a preliminary review (Min 2010, not listed). 'Hair of the dog' has an editorial and survey data, no trial. The risks of painkillers rest on a meta-analysis of paracetamol in people who drink and an older case-control study of aspirin and ibuprofen; no study of painkiller use specifically during hangover was found.

---

## 2. Benzodiazepines — `PDFs/Benzodiazepines/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 21 | Vermeeren — Residual effects of hypnotics: epidemiology and clinical implications | CNS Drugs 2004 | 10.2165/00023210-200418050-00003 | — | Benzodiazepines/Vermeeren_2004_ResidualEffectsHypnotics.pdf |
| 22 | Fornaro et al. — Residual effects of medications for sleep disorders on driving performance: a systematic review and network meta-analysis of randomized controlled trials | Eur Neuropsychopharmacol 2024 | 10.1016/j.euroneuro.2024.01.011 | — | Benzodiazepines/Fornaro_2024_ResidualDrivingNMA.pdf |
| 23 | Johnson et al. — Benzodiazepines and caffeine: effect on daytime sleepiness, performance, and mood | Psychopharmacology (Berl) 1990 | 10.1007/BF02244120 | — | Benzodiazepines/Johnson_1990_MorningCaffeineAfterHypnotic.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 24 | Verster et al. — Residual effects of sleep medication on driving ability | Sleep Med Rev 2004 | 10.1016/j.smrv.2004.02.001 | — | Benzodiazepines/Verster_2004_ResidualDrivingReview.pdf |
| 25 | Glass et al. — Sedative hypnotics in older people with insomnia: meta-analysis of risks and benefits | BMJ 2005 | 10.1136/bmj.38623.768588.47 | PMC1285093 | Benzodiazepines/Glass_2005_OlderPeopleRisksBenefitsMA.pdf |
| 26 | Kales et al. — Rebound insomnia after only brief and intermittent use of rapidly eliminated benzodiazepines | Clin Pharmacol Ther 1991 | 10.1038/clpt.1991.55 | — | Benzodiazepines/Kales_1991_ReboundInsomniaBriefUse.pdf |
| 27 | Power et al. — Controlled study of withdrawal symptoms and rebound anxiety after six week course of diazepam for generalised anxiety | BMJ 1985 | 10.1136/bmj.290.6477.1246 | PMC1415890 | Benzodiazepines/Power_1985_ReboundAnxietyDiazepam.pdf |
| 28 | Mattila et al. — Caffeine moderately antagonizes the effects of triazolam and zopiclone on the psychomotor performance of healthy subjects | Pharmacol Toxicol 1992 | 10.1111/j.1600-0773.1992.tb00473.x | — | Benzodiazepines/Mattila_1992_CaffeineTriazolamZopiclone.pdf |

**Already on other lists (not repeated):** _Tolerance #34 Soldatos et al. 1999 (rebound insomnia meta-analysis; Tier A for this page); Benzodiazepines #25 Donnelly et al. 2017 (hip fracture meta-analysis; publisher), #44 Morera-Fumero et al. 2020 (melatonin for hypnotic withdrawal), #80 Gustavsen et al. 2008 (road traffic accidents), and #26 Penninga et al. (flumazenil adverse events), Tier B for this page.

**Also needed:** Rigg & Sharp 2018 (benzodiazepines used to ease the MDMA comedown) under MDMA.

**Known gaps.** The evidence on next-day effects comes almost entirely from people taking benzodiazepines as prescribed sleeping pills; no study was found of the day after non-prescribed or recreational use, of street or 'designer' benzodiazepines, or of using benzodiazepines to come down from stimulants (see the stimulant pages). The only remedy tested for next-day sedation is caffeine: one controlled trial of caffeine the morning after (Johnson 1990) and laboratory studies of caffeine taken at the same time. No study was found of stimulants such as modafinil, or of exercise, bright light, naps or cold water, for next-day sedation. Rebound insomnia and anxiety are documented in older sleep-laboratory and clinical trials; nothing was found on what helps after a single night's use.

---

## 3. GHB / GBL — `PDFs/GHB-GBL/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 29 | van Amsterdam et al. — Cognitive impairment following clinical or recreational use of gammahydroxybutyric acid (GHB): a systematic review | Curr Neuropharmacol 2022 | 10.2174/1570159X19666210610094352 | PMC9878963 | GHB-GBL/vanAmsterdam_2022_CognitiveImpairmentSR.pdf |
| 30 | Liakoni et al. — Effect of γ-hydroxybutyrate (GHB) on driving as measured by a driving simulator | Psychopharmacology (Berl) 2018 | 10.1007/s00213-018-5025-2 | PMC6457903 | GHB-GBL/Liakoni_2018_DrivingSimulatorRecovery.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 31 | Dornbierer et al. — Nocturnal gamma-hydroxybutyrate reduces cortisol-awakening response and morning kynurenine pathway metabolites in healthy volunteers | Int J Neuropsychopharmacol 2019 | 10.1093/ijnp/pyz047 | PMC6822136 | GHB-GBL/Dornbierer_2019_MorningAfterNocturnalGHB.pdf |
| 32 | Floyd et al. — Baclofen in gamma-hydroxybutyrate withdrawal: patterns of use and online availability | Eur J Clin Pharmacol 2018 (online 2017) | 10.1007/s00228-017-2387-z | PMC5808054 | GHB-GBL/Floyd_2018_BaclofenSelfManagedWithdrawal.pdf |

**Already on other lists (not repeated):** GHB-GBL #9 McDonough et al. 2004 (withdrawal: clinical features and management) and the other withdrawal papers on that list (#4, #8, #10, #11), Tier B for this page.

**Known gaps.** No study was found of after-effects the day after occasional recreational GHB or GBL use (people's reports of next-day tiredness or low mood have not been measured), and no study of any remedy for them. Controlled studies give doses at night or in the laboratory and follow people for hours, not days. The evidence on self-treatment concerns withdrawal in people who use around the clock: baclofen bought online is documented by case reports and an internet survey, with no trial outside hospital.

---

## 4. Caffeine — `PDFs/Caffeine/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 33 | Gardiner et al. — The effect of caffeine on subsequent sleep: a systematic review and meta-analysis | Sleep Med Rev 2023 | 10.1016/j.smrv.2023.101764 | publisher | Caffeine/Gardiner_2023_CaffeineSubsequentSleepMA.pdf |
| 34 | Hampl et al. — Perioperative administration of caffeine tablets for prevention of postoperative headaches | Can J Anaesth 1995 | 10.1007/BF03011178 | publisher | Caffeine/Hampl_1995_PerioperativeCaffeineHeadacheRCT.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 35 | Clark & Landolt — Coffee, caffeine, and sleep: a systematic review of epidemiological studies and randomized controlled trials | Sleep Med Rev 2017 | 10.1016/j.smrv.2016.01.006 | publisher | Caffeine/Clark_2017_CoffeeCaffeineSleepSR.pdf |
| 36 | Sin et al. — Systematic review on the effectiveness of caffeine abstinence on the quality of sleep | J Clin Nurs 2009 (online 2008) | 10.1111/j.1365-2702.2008.02375.x | — | Caffeine/Sin_2009_CaffeineAbstinenceSleepSR.pdf |
| 37 | Weber et al. — Prophylactic intravenous administration of caffeine and recovery after ambulatory surgical procedures | Mayo Clin Proc 1997 | 10.1016/S0025-6196(11)63567-2 | — | Caffeine/Weber_1997_ProphylacticCaffeineSurgeryRCT.pdf |
| 38 | Agritelley et al. — Caffeine supplementation in the hospital: potential role for the treatment of caffeine withdrawal | Food Chem Toxicol 2021 | 10.1016/j.fct.2021.112228 | — | Caffeine/Agritelley_2021_HospitalCaffeineWithdrawal.pdf |

**Already on other lists (not repeated):** Caffeine #3 Juliano & Griffiths 2004 (critical review of caffeine withdrawal; Tier A for this page); Caffeine #9 Chang et al. 2025 (meta-analysis of caffeine and sleep) and the withdrawal-reversal papers #4–8 and #27–39, Tier B for this page.

**Known gaps.** Caffeine's after-effects (sleep loss and next-day withdrawal) are well studied and mostly already on the Caffeine list. Remedies are thin: cutting caffeine for sleep has one older systematic review; preventing withdrawal headache with caffeine has two small RCTs, both around surgery. No trial was found of painkillers for caffeine-withdrawal headache outside surgery, of anything for the 'crash' after energy drinks, or of L-theanine for caffeine's after-effects (its trials study combined effects on alertness, which this page does not cover).

---

## 5. Nicotine and tobacco — `PDFs/Nicotine/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 39 | Hughes — Effects of abstinence from tobacco: valid symptoms and time course | Nicotine Tob Res 2007 | 10.1080/14622200701188919 | — | Nicotine/Hughes_2007_AbstinenceSymptomsTimeCourse.pdf |
| 40 | Haasova et al. — The acute effects of physical activity on cigarette cravings: systematic review and meta-analysis with individual participant data | Addiction 2013 (online 2012) | 10.1111/j.1360-0443.2012.04034.x | — | Nicotine/Haasova_2013_PhysicalActivityCravingsIPD_MA.pdf |
| 41 | West & Shiffman — Effect of oral nicotine dosing forms on cigarette withdrawal symptoms and craving: a systematic review | Psychopharmacology (Berl) 2001 | 10.1007/s002130100712 | — | Nicotine/West_2001_OralNicotineWithdrawalSR.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 42 | Roberts et al. — The acute effects of exercise on cigarette cravings, withdrawal symptoms, affect, and smoking behaviour: systematic review update and meta-analysis | Psychopharmacology (Berl) 2012 | 10.1007/s00213-012-2731-z | — | Nicotine/Roberts_2012_ExerciseWithdrawalSR_MA.pdf |
| 43 | Jaehne et al. — Effects of nicotine on sleep during consumption, withdrawal and replacement therapy | Sleep Med Rev 2009 | 10.1016/j.smrv.2008.12.003 | — | Nicotine/Jaehne_2009_NicotineSleepReview.pdf |
| 44 | McRobbie et al. — Effect of glucose on tobacco withdrawal symptoms in recent quitters using bupropion or nicotine replacement | Hum Psychopharmacol 2004 | 10.1002/hup.535 | — | Nicotine/McRobbie_2004_GlucoseWithdrawalRCT.pdf |

**Already on other lists (not repeated):** Cessation treatments (nicotine replacement, varenicline, cytisine, e-cigarettes) are on the Nicotine list (#9–22, #39–43); they concern stopping, not day-to-day withdrawal relief.

**Known gaps.** For nicotine, 'the day after' is mostly withdrawal between uses, which is well described, and two remedies are well tested (exercise; nicotine replacement). No study was found of a next-day 'hangover' after occasional or social smoking or vaping, which is often reported informally. None of the six papers here is free to read (Haasova 2013 has a repository copy).

---

## 6. Cocaine — `PDFs/Cocaine/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 45 | Gawin & Kleber — Abstinence symptomatology and psychiatric diagnosis in cocaine abusers: clinical observations (landmark three-phase 'crash' model; read with Weddington 1990) | Arch Gen Psychiatry 1986 | 10.1001/archpsyc.1986.01800020013003 | — | Cocaine/Gawin_1986_AbstinenceSymptomatologyCrash.pdf |
| 46 | Weddington et al. — Changes in mood, craving, and sleep during short-term abstinence reported by male cocaine addicts: a controlled, residential study (controlled test of the crash model) | Arch Gen Psychiatry 1990 | 10.1001/archpsyc.1990.01810210069010 | — | Cocaine/Weddington_1990_ShortTermAbstinenceControlled.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 47 | Pace-Schott et al. — Sleep quality deteriorates over a binge–abstinence cycle in chronic smoked cocaine users | Psychopharmacology (Berl) 2005 | 10.1007/s00213-004-2088-z | — | Cocaine/PaceSchott_2005_SleepBingeAbstinence.pdf |
| 48 | Morgan et al. — Normalizing effects of modafinil on sleep in chronic cocaine users | Am J Psychiatry 2010 | 10.1176/appi.ajp.2009.09050613 | PMC5857958 | Cocaine/Morgan_2010_ModafinilSleepRCT.pdf |
| 49 | Kampman et al. — A double-blind, placebo-controlled trial of amantadine, propranolol, and their combination for the treatment of cocaine dependence in patients with severe cocaine withdrawal symptoms | Drug Alcohol Depend 2006 | 10.1016/j.drugalcdep.2006.04.002 | — | Cocaine/Kampman_2006_AmantadinePropranololWithdrawalRCT.pdf |

**Already on other lists (not repeated):** Alcohol #96 Pennings, Leccese & de Wolff 2002 (effects of concurrent alcohol and cocaine use, including use of alcohol to temper the comedown; also _Interactions #21), Tier A for this page; Cocaine #18 Harris et al. 2003, #19 Jatlow et al. 1991, #20 Hart et al. 2000 and #41 McCance-Katz et al. 1993 (cocaethylene, the compound formed when cocaine and alcohol are combined), Tier B.

**Also needed:** Angarita et al. 2016 (sleep abnormalities with alcohol, cannabis, cocaine and opiates) in Cross-cutting.

**Known gaps.** The crash is described in clinical studies of people who use heavily; no study was found of the day after occasional or recreational cocaine use (for example a night out), or of what helps it. Medicines have been tested only in treatment-seeking people with dependence: amantadine and propranolol with cocaine use as the main outcome (Kampman 2006), modafinil for sleep (Morgan 2010). No trial was found of sleeping pills or melatonin for the nights after a binge, or of food, vitamins or supplements for the crash. Using alcohol, benzodiazepines, opioids or cannabis to come down is documented only in reviews of combined use and in qualitative studies. No systematic review of treatments for cocaine withdrawal was found.

---

## 7. Amphetamine — `PDFs/Amphetamine/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 50 | Shoptaw, Kao, Heinzerling & Ling — Treatment for amphetamine withdrawal (Cochrane review) | Cochrane Database Syst Rev 2009 | 10.1002/14651858.CD003021.pub2 | PMC7138250 | _Cross-cutting/Shoptaw_2009_AmphetamineWithdrawalCochrane.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 51 | Cox et al. — Rebound effects with long-acting amphetamine or methylphenidate stimulant medication preparations among adolescent male drivers with attention-deficit/hyperactivity disorder | J Child Adolesc Psychopharmacol 2008 | 10.1089/cap.2006.0141 | — | _Cross-cutting/Cox_2008_StimulantReboundAdolescentDrivers.pdf |

**Already on other lists (not repeated):** Amphetamine #52 Acheson et al. 2023 (meta-analysis of medicines for methamphetamine withdrawal; PMC10083934), Tier A for this page and for Methamphetamine.

**Also needed:** Kidwell et al. 2015 (stimulant medicines and sleep in young people) in Cross-cutting; Perez et al. 2008 (next-day effects of methamphetamine) under Methamphetamine.

**Known gaps.** Almost all evidence on the amphetamine crash comes from methamphetamine studies (see that section) and from one Cochrane review whose trials are small and old. No study was found of the day after non-prescribed amphetamine use at parties or for studying, of supplements sold for the crash (such as tyrosine or 5-HTP), or of using sleeping pills, melatonin or cannabis to sleep afterwards.

---

## 8. Methamphetamine — `PDFs/Methamphetamine/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 52 | Perez et al. — Residual effects of intranasal methamphetamine on sleep, mood, and performance | Drug Alcohol Depend 2008 | 10.1016/j.drugalcdep.2007.10.011 | PMC2267907 | Methamphetamine/Perez_2008_ResidualEffectsSleepMood.pdf |
| 53 | Xu et al. — Effects of exercise interventions on negative emotions, cognitive performance and drug craving in methamphetamine addiction | Front Psychiatry 2024 | 10.3389/fpsyt.2024.1402533 | PMC11140390 | Methamphetamine/Xu_2024_ExerciseNegativeEmotionsSR.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 54 | Cruickshank et al. — A placebo-controlled trial of mirtazapine for the management of methamphetamine withdrawal | Drug Alcohol Rev 2008 | 10.1080/09595230801935672 | publisher | Methamphetamine/Cruickshank_2008_MirtazapineWithdrawalRCT.pdf |
| 55 | Lee et al. — A pilot randomised controlled trial of modafinil during acute methamphetamine withdrawal: feasibility, tolerability and clinical outcomes | Drug Alcohol Rev 2013 (online 2012) | 10.1111/j.1465-3362.2012.00473.x | — | Methamphetamine/Lee_2013_ModafinilWithdrawalPilotRCT.pdf |
| 56 | Rawson et al. — The impact of exercise on depression and anxiety symptoms among abstinent methamphetamine-dependent individuals in a residential treatment setting | J Subst Abuse Treat 2015 | 10.1016/j.jsat.2015.04.007 | PMC4560957 | Methamphetamine/Rawson_2015_ExerciseDepressionAnxietyRCT.pdf |

**Already on other lists (not repeated):** Methamphetamine #58 McGregor et al. 2005 (nature and time course of withdrawal) and #61 Acheson et al. 2023 (meta-analysis of medicines for withdrawal; PMC10083934), Tier A for this page; Methamphetamine #59 Zorick et al. 2010 (withdrawal symptoms), #102 Palmer et al. 2020 (motivations for methamphetamine–opioid co-use, including easing the comedown) and _Tolerance #165 Kirkpatrick et al. 2012 (acute and residual effects with alcohol; PMC3220757), Tier B. The mirtazapine trials on the Methamphetamine list (#79–81, U18) concern use disorder, not withdrawal. (The Methamphetamine list is the file `search-logs/methamphetamine_DOI-LIST.md`.)

**Also needed:** Shoptaw et al. 2009 (Cochrane, amphetamine withdrawal) under Amphetamine.

**Known gaps.** Next-day effects of a single dose have one laboratory study (Perez 2008). Withdrawal medicines have been tested in small trials of people with dependence; none has clear support in the meta-analysis already listed. Exercise trials come mostly from Chinese residential rehabilitation centres and measure mood and craving over weeks. No study was found of using sleeping pills, melatonin or cannabis to sleep after use, or of supplements or vitamins for the crash. Using opioids or GHB to come down is described only in qualitative work; its overdose risk is covered on the opioid and GHB pages.

---

## 9. Methylphenidate — `PDFs/Methylphenidate/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 57 | Faraone et al. — Sleep-associated adverse events during methylphenidate treatment of attention-deficit/hyperactivity disorder: a meta-analysis | J Clin Psychiatry 2019 | 10.4088/JCP.18r12210 | PMC8074661 | Methylphenidate/Faraone_2019_SleepAdverseEventsMA.pdf |
| 58 | Weiss et al. — Sleep hygiene and melatonin treatment for children and adolescents with ADHD and initial insomnia (DOI from a Crossref search; the PubMed record has none) | J Am Acad Child Adolesc Psychiatry 2006 | 10.1097/01.chi.0000205706.78818.ef | — | Methylphenidate/Weiss_2006_MelatoninSleepHygieneRCT.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 59 | Carlson & Kelly — Stimulant rebound: how common is it and what does it mean? | J Child Adolesc Psychopharmacol 2003 | 10.1089/104454603322163853 | — | Methylphenidate/Carlson_2003_StimulantRebound.pdf |

**Already on other lists (not repeated):** None: the Methylphenidate list covers cognitive enhancement and non-prescribed use, not after-effects.

**Also needed:** Kidwell et al. 2015 (stimulant medicines and sleep) in Cross-cutting; Cox et al. 2008 (evening rebound and driving) under Amphetamine.

**Known gaps.** All evidence concerns children and adults taking methylphenidate as prescribed for ADHD. No study was found of after-effects of non-prescribed use (for studying or at parties), of a 'comedown' after high or repeated doses, or of what people take afterwards to sleep (alcohol, cannabis, sleeping pills). Evening rebound is described in small, older observational studies.

---

## 10. Synthetic cathinones — `PDFs/Synthetic-cathinones/`

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 60 | Gunderson et al. — Intranasal substituted cathinone "bath salts" psychosis potentially exacerbated by diphenhydramine | J Addict Med 2013 | 10.1097/ADM.0b013e31829084d5 | — | Synthetic-cathinones/Gunderson_2013_BathSaltsPsychosisDiphenhydramine.pdf |

**Already on other lists (not repeated):** Synthetic-cathinones #58 Homman et al. 2018 (sub-acute effects of mephedrone on mood, cognition, sleep and physical problems; PMC6132682), Tier A for this page; #28 Winstock et al. 2011 (use, subjective effects and health risks) and #29 Freeman et al. 2012 (cognitive and subjective effects), Tier B.

**Also needed:** Matthews et al. 2017 (negative after-effects of new psychoactive substances rated against traditional drugs) in Cross-cutting.

**Known gaps.** A thin literature: one naturalistic study of the mephedrone comedown (already listed) and surveys. Nothing was found on the newer cathinones now sold in Europe (3-MMC, 3-CMC, 4-CMC) beyond market data, and no study of any remedy for the comedown; using sleeping pills, cannabis or alcohol to come down is undocumented except for one case report of an antihistamine taken for sleep during a binge.

---

## 11. MDMA — `PDFs/MDMA/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 61 | Curran & Travill — Mood and cognitive effects of ±3,4-methylenedioxymethamphetamine (MDMA, 'ecstasy'): week-end 'high' followed by mid-week low (landmark; Crossref holds a duplicate record 10.1046/j.1360-0443.1997.9278215.x; PubMed has no DOI) | Addiction 1997 | 10.1111/j.1360-0443.1997.tb02951.x | — | MDMA/Curran_1997_WeekendHighMidweekLow.pdf |
| 62 | Scott et al. — Subacute effects of ecstasy on mood: an exploration of associated risk factors | J Psychopharmacol 2013 (online 2012) | 10.1177/0269881112463467 | — | MDMA/Scott_2013_SubacuteMoodRiskFactors.pdf |
| 63 | Randall et al. — Effects of acute 3,4-methylenedioxymethamphetamine on sleep and daytime sleepiness in MDMA users: a preliminary study | Sleep 2009 | 10.1093/sleep/32.11.1513 | PMC2768958 | MDMA/Randall_2009_AcuteMDMASleepDaytimeSleepiness.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 64 | Parrott & Lasky — Ecstasy (MDMA) effects upon mood and cognition: before, during and after a Saturday night dance | Psychopharmacology (Berl) 1998 | 10.1007/s002130050714 | — | MDMA/Parrott_1998_SaturdayNightDance.pdf |
| 65 | Pirona & Morgan — An investigation of the subacute effects of ecstasy on neuropsychological performance, sleep and mood in regular ecstasy users | J Psychopharmacol 2010 (online 2009) | 10.1177/0269881109102780 | — | MDMA/Pirona_2010_SubacuteSleepMood.pdf |
| 66 | Rigg & Sharp — Nonmedical prescription drug use among African Americans who use MDMA (ecstasy/molly): implications for risk reduction | Addict Behav 2018 | 10.1016/j.addbeh.2017.12.024 | — | MDMA/Rigg_2018_PrescriptionDrugsComedown.pdf |
| 67 | Dobry et al. — Ecstasy use and serotonin syndrome: a neglected danger to adolescents and young adults prescribed selective serotonin reuptake inhibitors | Int J Adolesc Med Health 2013 | 10.1515/ijamh-2013-0052 | — | MDMA/Dobry_2013_EcstasySSRISerotoninSyndrome.pdf |

**Already on other lists (not repeated):** MDMA #50 Huxster et al. 2006 (controlled study of sub-acute effects), Tier A for this page; MDMA #49 Verheyden et al. 2003 (acute, sub-acute and long-term consequences in 430 users), #29 Vizeli & Liechti 2017 (safety pharmacology, including adverse effects up to 24 hours) and #55 Liechti et al. 2000 (citalopram blunts MDMA's effects), Tier B.

**Also needed:** Basedow et al. 2024 (subacute cognitive effects of psychedelics and MDMA) in Cross-cutting; serotonin toxicity with SSRIs and other serotonergic drugs is on the _Interactions list.

**Known gaps.** The mid-week low is documented in naturalistic studies of people who use recreationally, with known confounds (sleep loss, other drugs, alcohol); Huxster 2006 (already listed) controls for some of them. No human trial was found of any remedy people use for the comedown: 5-HTP, antioxidants (vitamin C, alpha-lipoic acid) and other supplements, magnesium for jaw clenching, cannabis, or rest, food and fluids. SSRIs taken afterwards ('post-loading') have only laboratory evidence that they blunt MDMA's effects when taken before, plus case-based reviews of serotonin syndrome; benzodiazepines for the comedown appear only in surveys. Harm-reduction sites that recommend these remedies show that they are popular, not that they work. None of the seven new papers is free at the publisher or in PMC except Randall 2009.

---

## 12. LSD — `PDFs/LSD/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 68 | Wießner et al. — LSD, afterglow and hangover: increased episodic memory and verbal fluency, decreased cognitive flexibility | Eur Neuropsychopharmacol 2022 | 10.1016/j.euroneuro.2022.01.114 | — | LSD/Wiessner_2022_AfterglowHangoverCognition24h.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 69 | Allen et al. — LSD increases sleep duration the night after microdosing | Transl Psychiatry 2024 | 10.1038/s41398-024-02900-4 | PMC11018829 | LSD/Allen_2024_MicrodoseSleepNightAfter.pdf |

**Already on other lists (not repeated):** LSD #3 Holze et al. 2021 (safety pharmacology of LSD, including adverse effects in the hours after and the next day; correction published), Tier A for this page; LSD #18 Neven et al. 2025 (medicines for HPPD) and #19 Litjens et al. 2014 (HPPD review), Tier B.

**Also needed:** Evens et al. 2023 (afterglow systematic review), Müller et al. 2022 (flashbacks in controlled studies), Basedow et al. 2024 and Evens et al. 2026, in Cross-cutting.

**Known gaps.** Next-day effects of full doses are reported as adverse effects in controlled studies (already listed) and in one trial of next-day cognition (Wießner 2022); no study was found of the day after recreational use, where sleep loss, alcohol and other drugs are common. No trial was found of any remedy for next-day headache or tiredness, of sleep aids the night after, or of cannabis or alcohol used to come down or sleep. Persisting perceptual changes have a systematic review of medicines (already listed) based on case reports.

---

## 13. Psilocybin — `PDFs/Psilocybin/`

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 70 | Dudysová et al. — The effects of daytime psilocybin administration on sleep: implications for antidepressant action | Front Pharmacol 2020 | 10.3389/fphar.2020.602590 | PMC7744693 | Psilocybin/Dudysova_2020_DaytimePsilocybinSleep.pdf |

**Already on other lists (not repeated):** Psilocybin #25 Johnson et al. 2012 (delayed headaches) and #23 Studerus et al. 2011 (online 2010) (acute, subacute and long-term effects, pooled), Tier A for this page; #14 Hinkle et al. 2024 (adverse events meta-analysis, also on other psychedelic lists) and #69 Burmester et al. 2023 (subacute inflammation markers), Tier B.

**Also needed:** Evens et al. 2023, Müller et al. 2022, Basedow et al. 2024 and Evens et al. 2026 in Cross-cutting.

**Known gaps.** After-effects are well described in controlled studies (headache, afterglow, subacute effects; mostly already listed), but not after recreational use of mushrooms, where dose, setting and other drugs vary. No trial was found of any remedy for the delayed headache (controlled studies report it resolving on its own), of sleep aids, or of cannabis or alcohol used afterwards.

---

## 14. DMT and ayahuasca — `PDFs/DMT-Ayahuasca/`

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 71 | Barbanoj et al. — Daytime ayahuasca administration modulates REM and slow-wave sleep in healthy volunteers | Psychopharmacology (Berl) 2008 (online 2007) | 10.1007/s00213-007-0963-0 | publisher | DMT-Ayahuasca/Barbanoj_2008_AyahuascaSleep.pdf |

**Already on other lists (not repeated):** DMT-Ayahuasca #11 Bouso et al. 2022 (adverse effects in the Global Ayahuasca Survey), Tier A for this page; #13 Durante et al. 2021 (adverse effects in religious use), Tier B.

**Also needed:** Evens et al. 2023 and Evens et al. 2026 in Cross-cutting; drug interactions with the MAO-inhibiting brew are on the _Interactions list.

**Known gaps.** After-effects of ayahuasca are known mainly from large surveys (already listed); smoked or vaped DMT has no study of after-effects at all. No study was found of any remedy for tiredness, nausea or low mood in the days after a ceremony, or of sleep aids afterwards, some of which interact with the MAO-inhibiting brew (see the _Interactions list).

---

## 15. 5-MeO-DMT — `PDFs/5-MeO-DMT/`

**Already on other lists (not repeated):** 5-MeO-DMT #8 Uthaug et al. 2020 (reactivations after vaporised versus injected use), Tier A for this page; #5 Davis et al. 2018 (epidemiology, benefits and consequences) and #13 Ortiz Bernal et al. 2025 (reactivations among Spanish speakers), Tier B. No new paper was found.

**Also needed:** Evens et al. 2023 and Evens et al. 2026 in Cross-cutting.

**Known gaps.** The only after-effect studied is 'reactivations', in surveys already on the 5-MeO-DMT list; no controlled study has measured next-day effects, and no remedy has been studied. Thin literature: nothing new was added for this page.

---

## 16. Mescaline — `PDFs/Mescaline/`

**Already on other lists (not repeated):** Mescaline #2 Ley et al. 2023 (controlled comparison of mescaline, LSD and psilocybin), Tier A for this page; #8 Uthaug et al. 2021 and #9 Agin-Liebes et al. 2021 (naturalistic use), Tier B. No new paper was found.

**Also needed:** Evens et al. 2023, Hinkle et al. 2024 (on the psychedelic lists) and Evens et al. 2026 in Cross-cutting.

**Known gaps.** Thin literature: one controlled study and two surveys (all already listed). Nothing was found on the day after peyote or San Pedro use in ceremonial settings, or on any remedy.

---

## 17. 2C-x phenethylamines — `PDFs/2C-x/`

**Already on other lists (not repeated):** 2C-x #1 Holze et al. 2026 (2C-B compared with psilocybin and MDMA in a controlled study), Tier A for this page. No new paper was found.

**Also needed:** Matthews et al. 2017 (after-effects of new psychoactive substances, including phenethylamines) and Evens et al. 2023 in Cross-cutting.

**Known gaps.** Thin literature: controlled 2C-B studies follow people for hours (Arikci et al. 2026, a second trial, measured effects up to 9 hours and was not listed), and no study was found of next-day effects of any 2C drug or NBOMe after recreational use, or of any remedy.

---

## 18. Ketamine — `PDFs/Ketamine/`

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 72 | Harding et al. — The landscape of ketamine use disorder: patient experiences and perspectives on current treatment options | Addiction 2025 | 10.1111/add.70073 | PMC12426348 | Ketamine/Harding_2025_KetamineUseDisorderExperiences.pdf |

**Already on other lists (not repeated):** Ketamine #13 Curran & Morgan 2000 (effects on the night of use and three days later) and #34 Short et al. 2018 (side-effects of ketamine for depression, systematic review), Tier A for this page; #14 Curran & Monaghan 2001 (acute and residual effects), #47 Blagrove et al. 2009 (unpleasant dreams) and #21 Chan et al. 2022 (uropathy meta-analysis), Tier B.

**Known gaps.** The day after recreational ketamine is described by one naturalistic study (already listed). No study was found of any remedy for it, or for 'K-cramps'; using more ketamine to dull bladder pain is reported informally but not studied. Clinical side-effect data come from single supervised doses for depression.

---

## 19. Phencyclidine — `PDFs/PCP/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 73 | Rainey & Crowder — Prolonged psychosis attributed to phencyclidine: report of three cases (Crossref gives no author; authors from PubMed) | Am J Psychiatry 1975 | 10.1176/ajp.132.10.1076 | — | PCP/Rainey_1975_ProlongedPsychosisThreeCases.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 74 | Erard, Luisada & Peele — The PCP psychosis: prolonged intoxication or drug-precipitated functional illness? | J Psychedelic Drugs 1980 | 10.1080/02791072.1980.10471432 | — | PCP/Erard_1980_PCPPsychosisProlonged.pdf |

**Already on other lists (not repeated):** PCP #19 Fauman et al. 1975 (psychosis induced by phencyclidine), Tier B for this page.

**Known gaps.** Thin and old literature: after-effects of PCP are known from 1970s–80s case series of prolonged psychosis; no study was found of the day after use in people who use it today (for example in 'fry' or 'wet' cigarettes), or of any remedy outside hospital.

---

## 20. Dextromethorphan — `PDFs/DXM/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 75 | Reissig et al. — High doses of dextromethorphan, an NMDA antagonist, produce effects similar to classic hallucinogens (named as a gap on the DXM list) | Psychopharmacology (Berl) 2012 | 10.1007/s00213-012-2680-6 | PMC3652430 | DXM/Reissig_2012_HighDoseDXMHallucinogen.pdf |

**Already on other lists (not repeated):** DXM #8 Miller 2005 (psychosis, dependence and physical withdrawal) and _Tolerance #269 Mutschler et al. 2010 (withdrawal and dependence syndrome; PMC2925345), Tier B for this page.

**Also needed:** Serotonin toxicity when dextromethorphan is combined with antidepressants or MDMA is on the _Interactions list.

**Known gaps.** No study was found of the day after recreational dextromethorphan use (people report next-day tiredness and nausea informally), or of any remedy. Products that also contain paracetamol, antihistamines or decongestants add their own next-day risks; these are covered on the DXM list.

---

## 21. Nitrous oxide — `PDFs/Nitrous-oxide/`

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 76 | Mair et al. — Nitrous oxide-induced myeloneuropathy: a case series | J Neurol Neurosurg Psychiatry 2023 | 10.1136/jnnp-2023-331131 | PMC10447413 | Nitrous-oxide/Mair_2023_MyeloneuropathyCaseSeries119.pdf |

**Already on other lists (not repeated):** Nitrous-oxide #9 Brunt et al. 2024 (peripheral neurotoxicity review, including B12 treatment; PMC11986278), Tier A for this page; #6 Kaar et al. 2016 (Global Drug Survey of nitrous oxide use), #22 Ménétrier et al. 2023 (B12 status systematic review), #5 Winstock & Ferris 2019 (dose-dependent neuropathy) and #55 Leslie et al. 2008 (nausea and vomiting after nitrous oxide anaesthesia), Tier B.

**Known gaps.** No study was found that measured next-day effects of recreational use, such as headache or nausea; the large survey reports persistent numbness and injuries. Vitamin B12 is used as treatment once nerve damage has occurred, alongside stopping; no study was found showing that taking B12 or methionine while continuing to use prevents damage, though the practice is popular.

---

## 22. Cannabis (THC, CBD) — `PDFs/Cannabis/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 77 | McCartney et al. — Determining the magnitude and duration of acute Δ9-tetrahydrocannabinol (Δ9-THC)-induced driving and cognitive impairment: a systematic and meta-analytic review | Neurosci Biobehav Rev 2021 | 10.1016/j.neubiorev.2021.01.003 | publisher | Cannabis/McCartney_2021_THCImpairmentDurationMA.pdf |
| 78 | Velzeboer et al. — Cannabis and sleep architecture: a systematic review and meta-analysis | Sleep Med Rev 2025 | 10.1016/j.smrv.2025.102164 | publisher | Cannabis/Velzeboer_2025_SleepArchitectureMA.pdf |
| 79 | Sabbineni et al. — SAEM GRACE: dopamine antagonists and topical capsaicin for cannabis hyperemesis syndrome in the emergency department: a systematic review of direct evidence | Acad Emerg Med 2024 | 10.1111/acem.14770 | publisher | Cannabis/Sabbineni_2024_CHSCapsaicinDopamineAntagonistsSR.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 80 | Chait — 'Hangover' effects the morning after marijuana smoking | Drug Alcohol Depend 1985 | 10.1016/0376-8716(85)90002-x | — | Cannabis/Chait_1985_MorningAfterHangover.pdf |
| 81 | Chait — Subjective and behavioral effects of marijuana the morning after smoking (follow-up of Chait 1985) | Psychopharmacology (Berl) 1990 | 10.1007/BF02244601 | — | Cannabis/Chait_1990_MorningAfterFollowUp.pdf |
| 82 | Suraev et al. — Evaluating possible 'next day' impairment in insomnia patients administered an oral medicinal cannabis product by night: a pilot randomized controlled trial | Psychopharmacology (Berl) 2024 | 10.1007/s00213-024-06595-9 | PMC11339085 | Cannabis/Suraev_2024_NextDayImpairmentMedicinalOilRCT.pdf |
| 83 | Waddell et al. — Indirect and direct effects of simultaneous alcohol and cannabis use on alcohol hangovers | Addict Behav 2022 | 10.1016/j.addbeh.2022.107420 | PMC10290518 | _Cross-cutting/Waddell_2022_AlcoholCannabisHangovers.pdf |
| 84 | Ruberto et al. — Intravenous haloperidol versus ondansetron for cannabis hyperemesis syndrome (HaVOC): a randomized, controlled trial | Ann Emerg Med 2021 | 10.1016/j.annemergmed.2020.08.021 | — | Cannabis/Ruberto_2021_HaVOC_RCT.pdf |

**Already on other lists (not repeated):** Cannabis #28 Sorensen et al. 2017 (hyperemesis systematic review; PMC5330965), #27 Bahji et al. 2020 (withdrawal meta-analysis), #108 Angulo et al. 2024 (hyperemesis review) and the CBD trials #67–69, Tier B for this page.

**Also needed:** Angarita et al. 2016 (sleep abnormalities across drugs) in Cross-cutting.

**Known gaps.** Morning-after effects of a single occasion have two small, old laboratory studies with mixed results, a pilot trial of medicinal oil and a meta-analysis of how long impairment lasts; no study was found of the day after recreational use of today's high-potency products or edibles. No trial was found of anything people use for morning-after grogginess (coffee, food, exercise) or of CBD taken the next day. Relief from hot showers in hyperemesis is reported in case series and surveys (already listed), not trials; topical capsaicin, which acts on the same heat-sensing receptor, has small trials.

---

## 23. Synthetic cannabinoids — `PDFs/Synthetic-cannabinoids/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 85 | Winstock & Barratt — Synthetic cannabis: a comparison of patterns of use and effect profile with natural cannabis in a large global sample (named as a gap on the Synthetic-cannabinoids list) | Drug Alcohol Depend 2013 | 10.1016/j.drugalcdep.2012.12.011 | — | Synthetic-cannabinoids/Winstock_2013_SyntheticVsNaturalGlobalSample.pdf |

**Already on other lists (not repeated):** _Tolerance #312 Craft et al. 2022 (withdrawal compared with high-potency cannabis; PMC9110517) and #313 Sharma & Weinstein 2025 (withdrawal: systematic review of case reports), and Synthetic-cannabinoids #3 Cooper 2016 (management of acute toxicity and withdrawal; PMC4923337), Tier B for this page.

**Known gaps.** After-effects of single occasions are known only from one large survey; withdrawal from case series and case reports. No study was found of any remedy for the day after, or of using natural cannabis to ease withdrawal, though both are reported informally.

---

## 24. Heroin — `PDFs/Heroin/`

For people who use heroin daily, 'the day after' is withdrawal, which starts within hours. The opioid-withdrawal papers here also serve the Fentanyl, Prescription-opioids, Methadone-Buprenorphine and Kratom pages and are saved under `_Cross-cutting/`.

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 86 | Gowing, Farrell, Ali & White — Alpha2-adrenergic agonists for the management of opioid withdrawal (Cochrane review) | Cochrane Database Syst Rev 2016 | 10.1002/14651858.CD002024.pub5 | PMC7081129 | _Cross-cutting/Gowing_2016_Alpha2AgonistsOpioidWithdrawalCochrane.pdf |
| 87 | Gowing, Ali, White & Mbewe — Buprenorphine for managing opioid withdrawal (Cochrane review) | Cochrane Database Syst Rev 2017 | 10.1002/14651858.CD002025.pub5 | PMC6464315 | _Cross-cutting/Gowing_2017_BuprenorphineOpioidWithdrawalCochrane.pdf |
| 88 | Lee et al. — Loperamide misuse to avoid opioid withdrawal and to achieve a euphoric effect: high doses and high risk | Clin Toxicol (Phila) 2019 (online 2018) | 10.1080/15563650.2018.1510128 | — | _Cross-cutting/Lee_2019_LoperamideMisuseWithdrawal.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 89 | Gorodetzky et al. — A phase III, randomized, multi-center, double blind, placebo controlled study of safety and efficacy of lofexidine for relief of symptoms in individuals undergoing inpatient opioid withdrawal | Drug Alcohol Depend 2017 | 10.1016/j.drugalcdep.2017.02.020 | publisher | _Cross-cutting/Gorodetzky_2017_LofexidinePhase3RCT.pdf |
| 90 | Padhan et al. — Efficacy and safety of tramadol in the treatment of opioid withdrawal: a meta-analysis of randomized controlled trials | Addict Behav 2023 | 10.1016/j.addbeh.2023.107815 | — | _Cross-cutting/Padhan_2023_TramadolOpioidWithdrawalMA.pdf |
| 91 | Jones et al. — The effects of vaped cannabis on the severity of naloxone-precipitated opioid withdrawal | Exp Clin Psychopharmacol 2026 | 10.1037/pha0000796 | PMC12590582 | _Cross-cutting/Jones_2026_VapedCannabisPrecipitatedWithdrawal.pdf |

**Already on other lists (not repeated):** _Interactions #15 Gomes et al. 2017 (gabapentin with opioids and the risk of opioid death; PMC5626029), Tier B for this page. Nothing on the Heroin list concerns withdrawal; the Methadone-Buprenorphine list names the Gowing Cochrane reviews and lofexidine as gaps, which this list fills.

**Also needed:** Angarita et al. 2016 (sleep abnormalities with alcohol, cannabis, cocaine and opiates) in Cross-cutting.

**Known gaps.** Medicines for withdrawal are well tested, but in clinics, not in the self-managed withdrawal many people go through. What people use at home has little or no evidence: loperamide has poison-centre data showing serious heart risks; gabapentin has evidence of harm (raised risk of opioid death) rather than benefit outside trials; cannabis has one laboratory study; benzodiazepines and alcohol used to get through withdrawal, herbal 'detox' products and home remedies (hot baths, sports drinks) have no trial. No study was found of the day after occasional, non-daily heroin use.

---

## 25. Fentanyl and analogues — `PDFs/Fentanyl-and-analogues/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 92 | Sharma et al. — Examining the severity and progression of illicitly manufactured fentanyl withdrawal: a quasi-experimental comparison | J Addict Med 2025 (online 2024) | 10.1097/ADM.0000000000001395 | PMC12429306 | Fentanyl-and-analogues/Sharma_2025_FentanylWithdrawalSeverity.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 93 | D'Onofrio et al. — Incidence of precipitated withdrawal during a multisite emergency department-initiated buprenorphine clinical trial in the era of fentanyl | JAMA Netw Open 2023 | 10.1001/jamanetworkopen.2023.6108 | PMC10064247 | Fentanyl-and-analogues/DOnofrio_2023_PrecipitatedWithdrawalEDTrial.pdf |
| 94 | Isoardi et al. — Acute opioid withdrawal following intramuscular administration of naloxone: a prospective out-of-hospital series (title shortened) | Ann Emerg Med 2022 | 10.1016/j.annemergmed.2022.03.004 | — | Fentanyl-and-analogues/Isoardi_2022_NaloxonePrecipitatedWithdrawal.pdf |
| 95 | Alexander et al. — Withdrawal signs and symptoms among patients positive for fentanyl with and without xylazine | J Addict Med 2025 (online 2024) | 10.1097/ADM.0000000000001423 | PMC11895813 | Fentanyl-and-analogues/Alexander_2025_FentanylXylazineWithdrawal.pdf |

**Already on other lists (not repeated):** Methadone-Buprenorphine #18 Varshneya et al. 2021 (buprenorphine-precipitated withdrawal in people who use fentanyl), Tier A for this page; #19 Spadaro et al. 2022 (Reddit discussions of precipitated withdrawal) and Fentanyl-and-analogues #13 Dahan et al. 2026 (naloxone reversal versus precipitated withdrawal, a model), Tier B.

**Also needed:** The opioid-withdrawal papers under Heroin (Gowing 2016 and 2017, Lee 2019, Gorodetzky 2017, Padhan 2023, Jones 2026) and _Interactions #15 Gomes et al. 2017.

**Known gaps.** Evidence on fentanyl withdrawal comes from hospital and treatment settings. No study was found of how people self-manage fentanyl withdrawal at home, or of remedies for withdrawal when fentanyl is mixed with xylazine or medetomidine outside hospital. The withdrawal that follows naloxone after an overdose is described in emergency series; what helps people afterwards is not studied.

---

## 26. Prescription opioids — `PDFs/Prescription-opioids/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 96 | Nee et al. — Efficacy of treatments for opioid-induced constipation: systematic review and meta-analysis | Clin Gastroenterol Hepatol 2018 | 10.1016/j.cgh.2018.01.021 | — | Prescription-opioids/Nee_2018_OpioidConstipationTreatmentsMA.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 97 | Kistemaker et al. — Pharmacological prevention and treatment of opioid-induced constipation in cancer patients: a systematic review and meta-analysis (erratum 10.1016/j.ctrv.2024.102738) | Cancer Treat Rev 2024 | 10.1016/j.ctrv.2024.102704 | publisher | Prescription-opioids/Kistemaker_2024_OpioidConstipationPreventionMA.pdf |

**Already on other lists (not repeated):** Prescription-opioids #28 Hassamal et al. 2018 (tramadol: serotonin syndrome and seizures) with its critique #29 Mégarbane & Vodovar 2018, Tier B for this page.

**Also needed:** The opioid-withdrawal papers under Heroin.

**Known gaps.** Constipation remedies are well tested as medicines; fibre, fluids and exercise have not been tested on their own for opioid-induced constipation. No study was found of next-day impairment after a bedtime dose in people without long-term use, or of over-the-counter sleep aids or alcohol taken with opioids to sleep, beyond the interaction and overdose evidence on other lists.

---

## 27. Methadone and buprenorphine — `PDFs/Methadone-Buprenorphine/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 98 | Dyer et al. — Steady-state pharmacokinetics and pharmacodynamics in methadone maintenance patients: comparison of those who do and do not experience withdrawal and concentration-effect relationships | Clin Pharmacol Ther 1999 | 10.1016/S0009-9236(99)90090-5 | — | Methadone-Buprenorphine/Dyer_1999_InterdoseWithdrawalPKPD.pdf |

**Already on other lists (not repeated):** Methadone-Buprenorphine #18 Varshneya et al. 2021 and #19 Spadaro et al. 2022 (precipitated withdrawal; see Fentanyl), and #74 Silverstein et al. 2020 (self-treatment with non-prescribed buprenorphine), Tier B for this page.

**Also needed:** The opioid-withdrawal papers under Heroin.

**Known gaps.** Inter-dose withdrawal is described in older pharmacology studies; no study was found of what people on methadone or buprenorphine do about it themselves (extra opioids, benzodiazepines, alcohol) or whether split dosing helps, beyond clinical guidance.

---

## 28. Kratom — `PDFs/Kratom/`

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 99 | Calicdan et al. — Liver injury associated with kratom (Mitragyna speciosa): a systematic review | J Addict Med 2026 | 10.1097/ADM.0000000000001663 | — | Kratom/Calicdan_2026_LiverInjurySR.pdf |

**Already on other lists (not repeated):** Kratom #10 Singh et al. 2014 (dependence, withdrawal and craving in regular users), Tier A for this page; #6 Grundmann 2017 and #7 Garcia-Romeu et al. 2020 (surveys including self-treatment of opioid withdrawal) and _Tolerance #421 Rogers et al. 2024 (physical dependence by dose amount and frequency; PMC11493341), Tier B.

**Also needed:** The opioid-withdrawal papers under Heroin.

**Known gaps.** Kratom's use as a home remedy for opioid withdrawal rests on surveys of people who use it; no controlled trial was found. Kratom withdrawal itself has surveys and case reports, and no study of what helps outside treatment.

---

## 29. Alkyl nitrites and inhalants — `PDFs/Alkyl-nitrites-and-inhalants/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 100 | Bartolo et al. — 'Poppers maculopathy' and the adverse ophthalmic outcomes from the recreational use of alkyl nitrate inhalants: a systematic review | Semin Ophthalmol 2023 (online 2022) | 10.1080/08820538.2022.2108717 | — | Alkyl-nitrites-and-inhalants/Bartolo_2023_PoppersMaculopathySR.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 101 | Romanelli et al. — Poppers: epidemiology and clinical management of inhaled nitrite abuse | Pharmacotherapy 2004 | 10.1592/phco.24.1.69.34801 | — | Alkyl-nitrites-and-inhalants/Romanelli_2004_PoppersEpidemiologyManagement.pdf |

**Already on other lists (not repeated):** Alkyl-nitrites-and-inhalants #4 Davies et al. 2012 (poppers maculopathy case series; PMC3496104), #7 Hui et al. 2020 (long-term follow-up) and the other maculopathy reports (#5–6, #38–40), and the nitrite–PDE5-inhibitor mechanism #34, Tier B for this page.

**Known gaps.** After-effects of poppers are known from case series and reviews (vision, methaemoglobinaemia); the common next-day headache has no study. For solvents, gases and aerosols, no study was found of next-day effects after a single occasion or of any remedy.

---

## 30. Salvia divinorum — `PDFs/Salvia-divinorum/`

**Already on other lists (not repeated):** Salvia-divinorum #13 Addy 2012 (acute and post-acute effects, with interviews 8 weeks later), Tier A for this page; #22 Baggott et al. 2010 (internet survey of self-reported effects, including after-effects) and #11 MacLean et al. 2013 (controlled dose-effect study), Tier B. No new paper was found.

**Known gaps.** Thin literature: one controlled study with follow-up and surveys, all already on the Salvia list. Effects are brief, and no study was found of next-day effects or of any remedy.

---

## 31. Cross-cutting (several drugs) — `PDFs/_Cross-cutting/`

Papers that span several drug pages; each drug section names the ones it needs in its "Also needed" line.

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 102 | Angarita et al. — Sleep abnormalities associated with alcohol, cannabis, cocaine, and opiate use: a comprehensive review | Addict Sci Clin Pract 2016 | 10.1186/s13722-016-0056-7 | PMC4845302 | _Cross-cutting/Angarita_2016_SleepAbnormalitiesFourDrugsReview.pdf |
| 103 | Kidwell, Van Dyk, Lundahl & Nelson — Stimulant medications and sleep for youth with ADHD: a meta-analysis | Pediatrics 2015 | 10.1542/peds.2015-1708 | — | _Cross-cutting/Kidwell_2015_StimulantSleepYouthMA.pdf |
| 104 | Evens et al. — The psychedelic afterglow phenomenon: a systematic review of subacute effects of classic serotonergic psychedelics | Ther Adv Psychopharmacol 2023 | 10.1177/20451253231172254 | PMC10240558 | _Cross-cutting/Evens_2023_PsychedelicAfterglowSR.pdf |
| 105 | Müller et al. — Flashback phenomena after administration of LSD and psilocybin in controlled studies with healthy participants | Psychopharmacology (Berl) 2022 | 10.1007/s00213-022-06066-z | PMC9166883 | _Cross-cutting/Muller_2022_FlashbacksLSDPsilocybinControlled.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 106 | Matthews et al. — I like the old stuff better than the new stuff? Subjective experiences of new psychoactive substances | Int J Drug Policy 2017 | 10.1016/j.drugpo.2016.11.004 | — | _Cross-cutting/Matthews_2017_NPSSubjectiveExperiences.pdf |
| 107 | Basedow et al. — Cognitive functioning associated with acute and subacute effects of classic psychedelics and MDMA — a systematic review and meta-analysis | Sci Rep 2024 | 10.1038/s41598-024-65391-9 | PMC11208433 | _Cross-cutting/Basedow_2024_SubacuteCognitionPsychedelicsMA.pdf |
| 108 | Evens et al. — Managing psychological challenges in the subacute ("afterglow") window of psychedelic drug effects | Curr Top Behav Neurosci 2026 (online 2025) | 10.1007/7854_2025_612 | — | _Cross-cutting/Evens_2026_ManagingSubacuteChallenges.pdf |

**Known gaps.** See each drug section.

---

## Verification block (2026-10-25)

- **Final list:** 108 new papers (Tier A 43, Tier B 65) across the 30 drug sections and Cross-cutting, plus 74 papers already on other lists, named in each section's "Already on other lists" line and recorded in `scratchpad/dayafter/map.json` with `already_listed`. Further related rows on other lists are named by number in those lines without being counted.
- **DOIs fetched:** every one of the 108 listed DOIs was fetched from Crossref `works/<DOI>` in this reader's browser tab on 2026-10-25 in a final sweep after drafting (each had also been fetched once at drafting); all 108 resolved to the paper named, with matching title, journal, year and first author. Also fetched: the 10 DOIs moved to "already listed" (see below), the two correction notices (10.1038/s41598-021-94669-5; 10.1093/alcalc/agaa088) and a duplicate Crossref record (10.1046/j.1360-0443.1997.9278215.x). No fetched DOI failed to resolve; none was dropped for resolving to another paper. No DOI was written from memory: each came from a PubMed `esummary` record or a Crossref bibliographic search and was then fetched.
- **Matched to PubMed:** 106 of the 108 DOIs are carried by a PubMed record (DOI lookup in PubMed, same day). Two have no DOI in PubMed and were located by Crossref bibliographic search on title, first author and journal: Curran & Travill 1997 (#61; Crossref holds two records for it, 10.1111/j.1360-0443.1997.tb02951.x listed and 10.1046/j.1360-0443.1997.9278215.x, both resolving, neither with `updated-by`) and Weiss et al. 2006 (#58; the search also returned a truncated duplicate record "10.1097/01", not used).
- **Moved to "already listed" at the final overlap check** (DOI index of all `search-logs/*_DOI-LIST.md`): Pennings 2002 (Alcohol #96, _Interactions #21), Palmer 2020 (Methamphetamine #102), Short 2018 (Ketamine #34), Mutschler 2010 (_Tolerance #269), Brunt 2024 (Nitrous-oxide #9), Kaar 2016 (Nitrous-oxide #6), Craft 2022 (_Tolerance #312), Sharma & Weinstein 2025 (_Tolerance #313), Gomes 2017 (_Interactions #15), Rogers 2024 (_Tolerance #421). None of the 108 new DOIs is on another list.
- **Corrections and errata:** #10 Coppersmith et al. 2021 (author correction 10.1038/s41598-021-94669-5, in Crossref `updated-by`); #11 Eriksson et al. 2020 (corrigendum 10.1093/alcalc/agaa088, linked in PubMed but not in Crossref `updated-by`; the corrigendum record was fetched); #97 Kistemaker et al. 2024 (erratum 10.1016/j.ctrv.2024.102738, in Crossref `updated-by`). Obtain each with its notice. Among already-listed papers, LSD #3 Holze et al. has a correction noted on the LSD list.
- **Retractions:** none of the 108 listed papers, and none of the 74 already-listed papers named here, has a retraction in Crossref `updated-by` or PubMed. Seen in search results and not listed: a lofexidine trial in children with tics (Niederhofer 2003; PubMed "Retracted Publication"), the withdrawn 2010 version of the Cochrane review of antidepressants for cocaine dependence, and an MDMA-assisted therapy sleep paper with an expression of concern (Ponte 2021).
- **Metadata kept as found:** where Crossref (online) and PubMed (print) years differ, the print year is given with the online year in brackets (17 rows); Crossref gives no author for #73 (Rainey & Crowder 1975; authors from PubMed); two titles were shortened (#19, #94) and are marked.
- **Free to read:** 53 of the 108 new papers (38 with a PMC id from the PubMed record, 15 open at the publisher per OpenAlex `open_access`); 39 of the 74 already-listed papers (34 PMC, 5 publisher). Copies in institutional repositories (OpenAlex "green" without PMC) are not counted.
- **Numbering:** rows are numbered in page order by the build script; the search log names papers by first author and year, not by number.
