# BeforeDuring — evidence map and PDF list for "Before, during and after", every drug page (v0.1, 2026-10-31)

Cross-cutting topic requested by the senior author (brief `docs/TOPIC-MAP-BRIEF-2026-10-31.md`, Topic 1): for each of the 30 drugs in `data/site/substances.json`, the research on what people do **before and during** use to reduce harms or to make the experience go better, and whether it works: (1) **preparation and state** (sleep, food, hydration, mood and expectations or "set", the place and the people or "setting", having a sober or experienced person present, preparation in psychedelic research); (2) **during use** (water and cooling against heat illness, rest and breaks, taking more during a session as a risk, eating, music and guidance in psychedelic sessions); (3) **supplements and medicines** taken before or with a drug to prevent a harm or an after-effect, with their risks and interactions; (4) **what predicts a good or a difficult experience**. Findings only: out of scope, and skipped, were dose amounts, timing advice, routes compared (section 7, the senior author's own), mixing drugs (the interactions page), drug checking (its own page) and anything about making a drug's effects stronger. "The day after" has its own list (`DayAfter_DOI-LIST.md`): none of its papers is repeated here; papers on it that serve this page are named in the "Already on other lists" lines, and after-effect remedies it missed were added where found. Reading list only: no claims, no study cards.

How this list was built: PubMed through the E-utilities interface (`esearch`, `esummary`; `efetch` for abstracts where a title did not show the design, and for PubMed's comment and correction links) in a tab of the app's browser that this reader opened, 1–6 searches per drug or theme plus known-item checks (strings, hit counts and what was kept: `BeforeDuring_search-log.md`). Order of preference: systematic reviews and meta-analyses; randomised and controlled human studies; large observational and naturalistic studies; authoritative reviews; landmark papers with their published critiques. Animal studies only where nothing human exists, marked as such. A practice with no study is recorded as a finding under that drug's **Known gaps**. Every candidate was checked against all existing lists first (`search-logs/*_DOI-LIST.md`, including `DayAfter_DOI-LIST.md`); papers already on them are named in an "Already on other lists" line instead of being listed again.

**Columns.** **DOI**: every DOI was fetched from Crossref `works/<DOI>` in the browser tab on 2026-10-31 and matched to the PubMed record on title, year and first author; its `updated-by` field was read (corrections, retractions). Where Crossref's year (online) and PubMed's year (print issue) differ, the print year is given with the online year in brackets. **Free?**: `PMCxxxxxxx` = free full text in PubMed Central (from the PubMed record or OpenAlex); `publisher` = OpenAlex `open_access` shows the article free at the publisher (gold, hybrid, bronze or diamond); `—` = neither (a copy in an institutional repository, OpenAlex "green", is not counted). Free papers can be read by AI readers without the senior author saving them.

**Tiers.** A = read first: the backbone review or best study of what people do before and during use of each drug and whether it works, and the best evidence on what predicts a good or difficult experience. B = further human studies, reviews, published critiques and risk evidence.

Save each PDF under `PDFs/` with the path given (drug folder from `docs/TIER1.md`, or `_Cross-cutting/` for papers that span several drugs).

---

## 1. Alcohol (ethanol) — `PDFs/Alcohol/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 1 | Van Nhat et al. — The effectiveness of protective behavioral strategies for reducing alcohol use and alcohol-related harms among adults: a systematic review and meta-analysis of randomized controlled trials | Psychiatry Res 2026 | 10.1016/j.psychres.2026.117430 | — | Alcohol/VanNhat_2026_ProtectiveStrategiesMA.pdf |
| 2 | Pearson — Use of alcohol protective behavioral strategies among college students: a critical review | Clin Psychol Rev 2013 | 10.1016/j.cpr.2013.08.006 | PMC3844112 | Alcohol/Pearson_2013_ProtectiveStrategiesReview.pdf |
| 3 | Jones et al. — Effect of high-fat, high-protein, and high-carbohydrate meals on the pharmacokinetics of a small dose of ethanol | Br J Clin Pharmacol 1997 | 10.1046/j.1365-2125.1997.t01-1-00620.x | PMC2042884 | Alcohol/Jones_1997_MealsEthanolPharmacokinetics.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 4 | Ramchandani et al. — Effect of food and food composition on alcohol elimination rates in healthy men and women | J Clin Pharmacol 2001 | 10.1177/00912700122012814 | — | Alcohol/Ramchandani_2001_FoodAlcoholElimination.pdf |
| 5 | Roehrs et al. — Sleepiness and ethanol effects on simulated driving | Alcohol Clin Exp Res 1994 | 10.1111/j.1530-0277.1994.tb00896.x | — | Alcohol/Roehrs_1994_SleepinessEthanolDriving.pdf |
| 6 | Corbin et al. — Contextual influences on subjective and behavioral responses to alcohol | Exp Clin Psychopharmacol 2015 | 10.1037/a0038760 | — | Alcohol/Corbin_2015_ContextAlcoholResponses.pdf |
| 7 | Ditter et al. — Effectiveness of designated driver programs for reducing alcohol-impaired driving (systematic review) | Am J Prev Med 2005 | 10.1016/j.amepre.2005.02.013 | — | Alcohol/Ditter_2005_DesignatedDriverSR.pdf |

**Already on other lists (not repeated):** DayAfter #4 Mackus et al. 2024 (drinking water to prevent or alleviate hangover) and #5 Imai et al. 2026 (water intake during drinking; PMC13311531), Tier A for this page; DayAfter #10 Coppersmith et al. 2021 (N-acetylcysteine taken while drinking; PMC8238992), #11 Eriksson et al. 2020 (L-cysteine supplement), #12 Rohsenow et al. 2014 (caffeinated alcoholic drinks; PMC3864634), #13 Köchling et al. 2019 (order of beer and wine; PMC6410559), #9 Jayawardena et al. 2017 (systematic review of prevention and treatment), #16 Verster et al. 2021 (unknown safety of hangover products), #17 Han et al. 2024 (use of over-the-counter hangover remedies; PMC10794163) and #18 McGregor 2007 (kudzu remedies and acetaldehyde risk), and Alcohol #91 Pittler, Verster & Ernst 2005 and #92 Roberts et al. 2022 (systematic reviews of hangover interventions, including products taken before drinking), Tier B for this page.

**Known gaps.** Protective behavioural strategies (pacing, alternating with non-alcoholic drinks, eating, staying with friends, planning a way home) are studied mostly as bundles of self-reported strategies in college students; one recent meta-analysis pools randomised trials (Van Nhat 2026), and no trial was found of any single strategy on its own. Food before drinking has controlled pharmacokinetic studies (fed against fasted) but no naturalistic study; the two 2000 symposium reviews on food (Gentry; Kalant) are two-page summaries and were not listed. Sleep loss before drinking has laboratory driving studies only. Setting has laboratory "bar" studies. Designated drivers have one systematic review (2005) and nothing newer was found. Hangover-prevention products taken before or while drinking are covered on the DayAfter list; the many single trials of East Asian products were not listed. Exposure to heat or cold while drinking was not searched separately.

---

## 2. Benzodiazepines — `PDFs/Benzodiazepines/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 8 | Morrison et al. — Harm reduction approaches for the use of benzodiazepines: a scoping review | Harm Reduct J 2025 | 10.1186/s12954-025-01310-z | PMC12502574 | Benzodiazepines/Morrison_2025_HarmReductionScopingReview.pdf |

**Already on other lists (not repeated):** None found that concern practices before or during use; the overdose risk of combining benzodiazepines with opioids or alcohol is on the _Interactions list.

**Known gaps.** One scoping review. No study was found of what people who use street or 'designer' benzodiazepines (etizolam, bromazolam) do before or during use, such as having someone present or avoiding taking more when the effect seems weak, or of whether any such practice works.

---

## 3. GHB / GBL — `PDFs/GHB-GBL/`

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 9 | Grund et al. — Going knock: recurrent comatose GHB intoxication in the Netherlands & Flanders (Belgium) | Int J Drug Policy 2018 | 10.1016/j.drugpo.2018.06.010 | — | GHB-GBL/Grund_2018_GoingKnockRecurrentComa.pdf |

**Already on other lists (not repeated):** GHB-GBL #46 Freestone et al. 2023 (understandings, attitudes, practices and responses to GHB overdose among people who use GHB; PMC10475182), Tier A for this page; GHB-GBL #17 Degenhardt, Darke & Dillon 2003 (prevalence and correlates of GHB overdose), Tier B.

**Also needed:** Herrijgers et al. 2020 (harm-reduction practices in chemsex) in Cross-cutting.

**Known gaps.** What people do to avoid 'going under' (measuring, spacing, having a sober friend present) is described in qualitative and survey work only (Freestone 2023; Grund 2018); no study tested any of it. Taking more during a session as a cause of coma appears in these studies and in case series, not in a controlled study.

---

## 4. Caffeine — `PDFs/Caffeine/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 10 | Klevebrant & Frick — Effects of caffeine on anxiety and panic attacks in patients with panic disorder: a systematic review and meta-analysis | Gen Hosp Psychiatry 2022 | 10.1016/j.genhosppsych.2021.11.005 | publisher | Caffeine/Klevebrant_2022_CaffeinePanicDisorderMA.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 11 | Rogers et al. — Time for tea: mood, blood pressure and cognitive performance effects of caffeine and theanine administered alone and together | Psychopharmacology (Berl) 2008 (online 2007) | 10.1007/s00213-007-0938-1 | — | Caffeine/Rogers_2008_TheanineCaffeineBloodPressure.pdf |
| 12 | Payne et al. — Effects of tea (Camellia sinensis) or its bioactive compounds l-theanine or l-theanine plus caffeine on cognition, sleep, and mood in healthy participants: a systematic review and meta-analysis of randomized controlled trials (sleep and mood outcomes for this page) | Nutr Rev 2025 | 10.1093/nutrit/nuaf054 | PMC12422004 | Caffeine/Payne_2025_TheanineCaffeineSR_MA.pdf |

**Already on other lists (not repeated):** None: the Caffeine list and the DayAfter caffeine section cover withdrawal and sleep after use.

**Known gaps.** L-theanine is the only supplement taken with caffeine that has trials, and most of those trials measure attention and alertness (making effects stronger, out of scope); blood pressure, mood and sleep have small trials. Panic disorder predicts panic attacks after caffeine in a meta-analysis of challenge studies; genetic predictors of caffeine's effects have a systematic review (Fulton et al. 2018) that was not listed. No study was found of food or water taken with caffeine or energy drinks to prevent jitteriness or palpitations.

---

## 5. Nicotine and tobacco — `PDFs/Nicotine/`

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 13 | Palmer & Brandon — Nicotine or expectancies? Using the balanced-placebo design to test immediate outcomes of vaping | Addict Behav 2019 | 10.1016/j.addbeh.2019.04.026 | PMC6629028 | Nicotine/Palmer_2019_VapingExpectanciesBalancedPlacebo.pdf |

**Known gaps.** Practices before and during nicotine use are hardly studied: one balanced-placebo study of expectancy with vaping. No study was found of nausea or 'nicotine sickness' in people new to pouches or vapes, or of what helps it.

---

## 6. Cocaine — `PDFs/Cocaine/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 14 | Marzuk et al. — Ambient temperature and mortality from unintentional cocaine overdose (landmark; read with Kilbourne 1998; Crossref lists only the first author, authors from PubMed) | JAMA 1998 | 10.1001/jama.279.22.1795 | — | Cocaine/Marzuk_1998_AmbientTemperatureCocaineDeaths.pdf |
| 15 | Crandall et al. — Mechanism of cocaine-induced hyperthermia in humans (read with Schier 2002) | Ann Intern Med 2002 | 10.7326/0003-4819-136-11-200206040-00006 | — | Cocaine/Crandall_2002_CocaineHyperthermiaMechanism.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 16 | Kilbourne — Cocaine use and death during heat waves (editorial on Marzuk 1998) | JAMA 1998 | 10.1001/jama.279.22.1828 | — | Cocaine/Kilbourne_1998_HeatWavesEditorial.pdf |
| 17 | Schier et al. — Cocaine and body temperature regulation (letter on Crandall 2002, with the authors' reply) | Ann Intern Med 2002 | 10.7326/0003-4819-137-10-200211190-00017 | — | Cocaine/Schier_2002_LetterOnCrandall.pdf |
| 18 | Auger et al. — Association of elevated ambient temperature with death from cocaine overdose | Drug Alcohol Depend 2017 | 10.1016/j.drugalcdep.2017.04.019 | — | Cocaine/Auger_2017_TemperatureCocaineDeaths.pdf |

**Already on other lists (not repeated):** None.

**Also needed:** Bohnert et al. 2010, Henderson et al. 2023 and Chang et al. 2023 (heat and drug deaths or emergency visits) and Palamar & Sönmez 2022 (festival environments) in Cross-cutting.

**Known gaps.** Deaths rise with ambient temperature in population studies, and a laboratory study shows impaired sweating and skin blood flow under heat; no study tested cooling, rest or water during cocaine use. No study was found of sleep or food before use, or of what people do during a binge to limit harm.

---

## 7. Amphetamine — `PDFs/Amphetamine/`

**Already on other lists (not repeated):** None. No new paper was found.

**Also needed:** Henderson et al. 2023 and Chang et al. 2023 (hot weather and amphetamine-related deaths and emergency visits) in Cross-cutting.

**Known gaps.** No study was found of what people do before or during non-prescribed amphetamine use (for studying or at parties): sleep, food, water or rest. Heat evidence comes from population time-series that combine stimulants.

---

## 8. Methamphetamine — `PDFs/Methamphetamine/`

**Already on other lists (not repeated):** methamphetamine #101 Harding et al. 2022 (experiences of 'overamping' and the strategies people use to avoid it; PMC8762891; also _Overdose-and-emergency #27), Tier A for this page; methamphetamine #70 Matsumoto et al. 2014 (hyperthermia review), Tier B. No new paper was found.

**Also needed:** Henderson et al. 2023 and Chang et al. 2023 (heat) and Herrijgers et al. 2020 (chemsex practices) in Cross-cutting.

**Known gaps.** Sleep, food and water during binges are described in qualitative work only. No study was found of sleep loss during a binge as a predictor of psychosis that met the brief, or of any practice tested for whether it works.

---

## 9. Methylphenidate — `PDFs/Methylphenidate/`

**Already on other lists (not repeated):** None. No new paper was found.

**Known gaps.** No study was found of what people do before or during non-prescribed methylphenidate use (sleep, food, combining with caffeine to stay awake), or of whether any practice reduces side-effects.

---

## 10. Synthetic cathinones — `PDFs/Synthetic-cathinones/`

**Already on other lists (not repeated):** None. No new paper was found.

**Also needed:** Herrijgers et al. 2020 (harm-reduction practices in chemsex) in Cross-cutting.

**Known gaps.** No study was found of practices before or during cathinone use outside chemsex research (sleep, food, water, rest, taking more during a session), or of whether any works.

---

## 11. MDMA — `PDFs/MDMA/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 19 | Faria et al. — Drinking to death: hyponatraemia induced by synthetic phenethylamines | Drug Alcohol Depend 2020 | 10.1016/j.drugalcdep.2020.108045 | — | MDMA/Faria_2020_HyponatraemiaReview.pdf |
| 20 | Henry et al. — Toxicity and deaths from 3,4-methylenedioxymethamphetamine ("ecstasy") (landmark; two Lancet letters in reply, see search log) | Lancet 1992 | 10.1016/0140-6736(92)91469-o | — | MDMA/Henry_1992_ToxicityDeathsEcstasy.pdf |
| 21 | Allott & Redman — Patterns of use and harm reduction practices of ecstasy users in Australia (focus on preloading and postloading) | Drug Alcohol Depend 2006 | 10.1016/j.drugalcdep.2005.09.009 | — | MDMA/Allott_2006_HarmReductionPreloading.pdf |
| 22 | Studerus et al. — Prediction of MDMA response in healthy humans: a pooled analysis of placebo-controlled studies | J Psychopharmacol 2021 | 10.1177/0269881121998322 | PMC8155734 | MDMA/Studerus_2021_PredictionMDMAResponse.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 23 | Freedman et al. — Thermoregulatory effects of 3,4-methylenedioxymethamphetamine (MDMA) in humans | Psychopharmacology (Berl) 2005 | 10.1007/s00213-005-0149-6 | — | MDMA/Freedman_2005_ThermoregulationAmbient.pdf |
| 24 | Parrott et al. — Dancing hot on Ecstasy: physical activity and thermal comfort ratings are associated with the memory and other psychobiological problems reported by recreational MDMA users | Hum Psychopharmacol 2006 | 10.1002/hup.773 | — | MDMA/Parrott_2006_DancingHot.pdf |
| 25 | Wolff et al. — Vasopressin and oxytocin secretion in response to the consumption of ecstasy in a clubbing population | J Psychopharmacol 2006 | 10.1177/0269881106061514 | — | MDMA/Wolff_2006_VasopressinClubbers.pdf |
| 26 | Matthai et al. — Cerebral oedema after ingestion of MDMA ("ecstasy") and unrestricted intake of water (case report; read with Finch 1996) | BMJ 1996 | 10.1136/bmj.312.7042.1359b | PMC2351042 | MDMA/Matthai_1996_CerebralOedemaWater.pdf |
| 27 | Finch et al. — Drug workers emphasise that water is not an antidote to drug (letter on Matthai 1996; two further letters discuss treatment, see search log) | BMJ 1996 | 10.1136/bmj.313.7058.690 | PMC2351959 | MDMA/Finch_1996_WaterNotAntidoteLetter.pdf |
| 28 | Copeland et al. — Ecstasy and the concomitant use of pharmaceuticals | Addict Behav 2006 | 10.1016/j.addbeh.2005.05.025 | — | MDMA/Copeland_2006_PharmaceuticalsWithEcstasy.pdf |
| 29 | Kelly — Mediating MDMA-related harm: preloading and post-loading among ecstasy-using youth | J Psychoactive Drugs 2009 | 10.1080/02791072.2009.10400671 | — | MDMA/Kelly_2009_PreloadingPostloading.pdf |
| 30 | Sprague et al. — Attenuation of 3,4-methylenedioxymethamphetamine (MDMA) induced neurotoxicity with the serotonin precursors tryptophan and 5-hydroxytryptophan (animal study, rats) | Life Sci 1994 | 10.1016/0024-3205(94)00658-x | — | MDMA/Sprague_1994_5HTPTryptophanRats.pdf |
| 31 | Aguirre et al. — α-Lipoic acid prevents 3,4-methylenedioxy-methamphetamine (MDMA)-induced neurotoxicity (animal study, rats) | Neuroreport 1999 | 10.1097/00001756-199911260-00039 | — | MDMA/Aguirre_1999_AlphaLipoicAcidRats.pdf |

**Already on other lists (not repeated):** MDMA #31 Parrott 2012 (review of MDMA's thermal effects in humans), Tier A for this page; _Tolerance #188 Farré et al. 2004 (also MDMA #28), #189 Peiró et al. 2013, #192 Farré et al. 2015 and #193 Humbert-Droz et al. 2026 (a second or supplemental dose during a session; PMC13451183), Tier B; MDMA #55 Liechti et al. 2000 (citalopram taken beforehand blunts MDMA's effects; also _Interactions #41) and DayAfter #67 Dobry et al. 2013 (SSRIs and serotonin syndrome), Tier B; _Overdose-and-emergency #57 Reddi et al. 2022 (severe hyperthermia at a festival) and #82 Wood et al. (festival medical cover and hospital transfers), Tier B.

**Also needed:** Palamar & Sönmez 2022 (why festivals are risky environments), Wadds et al. 2023 (peer-led safe spaces) and the heat papers in Cross-cutting.

**Known gaps.** Water: the evidence is case reports, physiology (vasopressin secretion measured in clubbers) and reviews; no study was found that tested drinking advice. Heat and dancing: one laboratory study of room temperature, field surveys and reviews; no trial of cooling, rest or 'chill-out' areas. Supplements: preloading and postloading (5-HTP, antioxidants, vitamins, SSRIs) are documented by surveys and interviews (Allott 2006; Copeland 2006; Kelly 2009); evidence that they protect comes only from rat studies (Sprague 1994; Aguirre 1999), and no human study was found of 5-HTP, antioxidants or magnesium taken before or after MDMA, or of their risks in combination with MDMA beyond case-based reviews of serotonin syndrome. Taking more during a session is covered by controlled studies on the _Tolerance list. Predictors of response come from pooled laboratory studies only.

---

## 12. LSD — `PDFs/LSD/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 32 | Vizeli et al. — Pharmacological and non-pharmacological predictors of the LSD experience in healthy participants | Transl Psychiatry 2024 | 10.1038/s41398-024-03074-9 | PMC11374807 | LSD/Vizeli_2024_PredictorsLSDExperience.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 33 | Kopra et al. — Adverse experiences resulting in emergency medical treatment seeking following the use of lysergic acid diethylamide (LSD) | J Psychopharmacol 2022 | 10.1177/02698811221099650 | PMC9353972 | LSD/Kopra_2022_EmergencyTreatmentLSD.pdf |
| 34 | Baxter et al. — Tripping into the unknown: exploring the experiences of first-time LSD users through Global Drug Survey insights | J Psychopharmacol 2024 | 10.1177/02698811241254837 | PMC11311902 | LSD/Baxter_2024_FirstTimeLSDUsers.pdf |

**Already on other lists (not repeated):** LSD #9 Szigeti et al. 2021 (self-blinding microdosing: expectancy; PMC7925122), #28 Muthukumaraswamy et al. 2021 (blinding and expectancy confounds) and #61 Szigeti & Heifets 2024 (expectancy effects in psychedelic trials), Tier B for this page; LSD #57 Evans et al. 2023 (extended difficulties; PMC10597511), Tier B.

**Also needed:** Psilocybin #17 Johnson, Richards & Griffiths 2008 (safety guidelines) and the psychedelic papers in Cross-cutting (#61–#82).

**Known gaps.** Predictors of the LSD experience come from pooled laboratory studies (Vizeli 2024) and survey data (Global Drug Survey); no study was found of preparation, sitters, eating or rest during recreational LSD use, or of taking more during a session.

---

## 13. Psilocybin — `PDFs/Psilocybin/`

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 35 | Kopra et al. — Adverse experiences resulting in emergency medical treatment seeking following the use of magic mushrooms | J Psychopharmacol 2022 | 10.1177/02698811221084063 | PMC9353971 | Psilocybin/Kopra_2022_EmergencyTreatmentMushrooms.pdf |
| 36 | Russ et al. — Replication and extension of a model predicting response to psilocybin (replication of Psilocybin #24 Studerus et al. 2012) | Psychopharmacology (Berl) 2019 | 10.1007/s00213-019-05279-z | — | Psilocybin/Russ_2019_ReplicationPredictionModel.pdf |
| 37 | Strickland et al. — Set and setting: a randomized study of different musical genres in supporting psychedelic therapy (correction 10.1021/acsptsci.1c00119, from PubMed; not in Crossref `updated-by`) | ACS Pharmacol Transl Sci 2021 (online 2020) | 10.1021/acsptsci.0c00187 | PMC8033606 | Psilocybin/Strickland_2021_MusicGenresRCT.pdf |
| 38 | Murphy et al. — Therapeutic alliance and rapport modulate responses to psilocybin assisted therapy for depression | Front Pharmacol 2022 (vol. 12, 2021) | 10.3389/fphar.2021.788155 | PMC9009076 | Psilocybin/Murphy_2022_TherapeuticAlliance.pdf |
| 39 | Earleywine et al. — How important is a guide who has taken psilocybin in psilocybin-assisted therapy for depression? | J Psychoactive Drugs 2023 (online 2022) | 10.1080/02791072.2022.2047842 | — | Psilocybin/Earleywine_2023_GuideOwnExperience.pdf |
| 40 | Leary et al. — Reactions to psilocybin administered in a supportive environment (historical; Crossref title misspells "psilocybin", title from PubMed) | J Nerv Ment Dis 1963 | 10.1097/00005053-196312000-00007 | — | Psilocybin/Leary_1963_SupportiveEnvironment.pdf |

**Already on other lists (not repeated):** Psilocybin #17 Johnson, Richards & Griffiths 2008 (safety guidelines: screening, preparation, monitors and setting; PMC3056407), #24 Studerus et al. 2012 (prediction of psilocybin response; PMC3281871) and #26 Carbonaro et al. 2016 (challenging experiences after psilocybin mushrooms; PMC5551678), Tier A for this page; #27 Barrett et al. 2016 (Challenging Experience Questionnaire; PMC5549781), #52 Barrett, Johnson & Griffiths 2017 (neuroticism and challenging experiences; PMC5540159), #5 Szigeti et al. 2024, #9 Muthukumaraswamy et al. 2021, #11 Szigeti & Heifets 2024 and #12 Huneke et al. 2025 (expectancy), and #28 Evans et al. 2023 (extended difficulties; PMC10597511), Tier B.

**Also needed:** the psychedelic papers in Cross-cutting (#61–#82).

**Known gaps.** Setting, music, guides and the therapeutic relationship are studied in clinical trials, with one randomised comparison of music (Strickland 2021); in recreational use, the evidence is surveys of challenging experiences and emergency presentations. No study was found of eating or fasting before mushrooms (nausea), of sitters in non-clinical use, or of taking more during a session.

---

## 14. DMT and ayahuasca — `PDFs/DMT-Ayahuasca/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 41 | Perkins et al. — Influence of context and setting on the mental health and wellbeing outcomes of ayahuasca drinkers: results of a large international survey | Front Pharmacol 2021 | 10.3389/fphar.2021.623979 | PMC8097729 | DMT-Ayahuasca/Perkins_2021_ContextSettingSurvey.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 42 | Gómez-Sousa et al. — Acute psychological adverse reactions in first-time ritual ayahuasca users: a prospective case series | J Clin Psychopharmacol 2021 | 10.1097/jcp.0000000000001343 | — | DMT-Ayahuasca/GomezSousa_2021_FirstTimeRitualAdverse.pdf |
| 43 | Houle et al. — Ayahuasca and the traveller: a scoping review of risks and possible benefits | Travel Med Infect Dis 2021 | 10.1016/j.tmaid.2021.102206 | — | DMT-Ayahuasca/Houle_2021_AyahuascaTravellerScoping.pdf |

**Already on other lists (not repeated):** DMT-Ayahuasca #35 Pontual et al. 2022 (ceremonial settings and mystical and challenging experiences; PMC9335152) and #28 Uthaug et al. 2021 (ayahuasca, set and setting in group retreats; PMC8233273), Tier A for this page; #11 Bouso et al. 2022 (adverse effects in the Global Ayahuasca Survey), #13 Durante et al. 2021 (self-reported risk factors in religious use; PMC8352742), #30 Perkins et al. 2024 (naturalistic settings and mental health) and #45 Evans et al. 2023 (extended difficulties), Tier B.

**Also needed:** the psychedelic papers in Cross-cutting (#61–#82); drug interactions with the MAO-inhibiting brew are on the _Interactions list.

**Known gaps.** Context is studied through large surveys and retreat cohorts; no study was found of the traditional diet before ceremonies (low-tyramine 'dieta') in humans, of what facilitators do and whether it helps, or of smoked or vaped DMT in non-laboratory settings beyond an EEG study (Pallavicini 2021, not listed).

---

## 15. 5-MeO-DMT — `PDFs/5-MeO-DMT/`

**Already on other lists (not repeated):** 5-MeO-DMT #12 Lancelotta & Davis 2020 (benefit-enhancement strategies, such as preparation, intention and a safe setting, and their associations with mystical and challenging effects; PMC7415524), Tier A for this page; #6 Davis et al. 2019 (use in a naturalistic group setting; PMC6430661), #7 Uthaug et al. 2019 (naturalistic setting; PMC6695371) and #28 Evans et al. 2023, Tier B. No new paper was found.

**Known gaps.** One survey of preparation and setting strategies (already listed). No study was found of sitters or facilitators, or of whether any practice prevents the loss of consciousness and 'reactivations' reported after use.

---

## 16. Mescaline — `PDFs/Mescaline/`

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 44 | Prince et al. — Examination of recreational and spiritual peyote use among American Indian youth | J Stud Alcohol Drugs 2019 | 10.15288/jsad.2019.80.366 | PMC6614926 | Mescaline/Prince_2019_PeyoteRecreationalSpiritual.pdf |

**Already on other lists (not repeated):** Mescaline #11 Doesburg-van Kleffens et al. 2023 (peyote: the importance of context, ceremony and culture; PMC10746114), Tier A for this page; #27 Evans et al. 2023, Tier B.

**Known gaps.** Thin literature: ceremonial context is described in reviews and one survey of young people; no study was found of preparation, fasting or practices during San Pedro or synthetic mescaline use.

---

## 17. 2C-x phenethylamines — `PDFs/2C-x/`

**Already on other lists (not repeated):** 2C-x #16 Hermanns-Clausen et al. 2017 (a 'bad trip' after 25I-NBOMe, case report), Tier B for this page. No new paper was found.

**Known gaps.** No study was found of practices before or during 2C-B or NBOMe use, or of predictors of a difficult experience; the main protective practice discussed in this literature is drug checking (out of scope).

---

## 18. Ketamine — `PDFs/Ketamine/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 45 | Kheirkhah et al. — Exploring the impact of music on response to ketamine/esketamine: a scoping review | Neurosci Biobehav Rev 2024 | 10.1016/j.neubiorev.2024.105693 | PMC13179047 | Ketamine/Kheirkhah_2024_MusicKetamineScoping.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 46 | Greenway et al. — Music as an intervention to improve the hemodynamic response of ketamine in depression: a randomized clinical trial | JAMA Netw Open 2024 | 10.1001/jamanetworkopen.2023.54719 | PMC10845001 | Ketamine/Greenway_2024_MusicKetamineRCT.pdf |
| 47 | Aust et al. — Anxiety during ketamine infusions is associated with negative treatment responses in major depressive disorder | Eur Neuropsychopharmacol 2019 | 10.1016/j.euroneuro.2019.02.005 | — | Ketamine/Aust_2019_AnxietyDuringInfusion.pdf |

**Already on other lists (not repeated):** None that concern practices before or during use.

**Known gaps.** All evidence comes from supervised clinical infusions (music, anxiety during the session). No study was found of setting, company, preparation or rest in recreational ketamine use, of predictors of a frightening 'K-hole', or of taking more during a session.

---

## 19. Phencyclidine — `PDFs/PCP/`

**Already on other lists (not repeated):** None. No new paper was found.

**Known gaps.** No study was found of practices before or during PCP or 3-MeO-PCP use.

---

## 20. Dextromethorphan — `PDFs/DXM/`

**Already on other lists (not repeated):** DXM #4 Zawertailo et al. 1998 (psychotropic effects altered by the CYP2D6 polymorphism, a predictor of a stronger and more difficult experience; also _Interactions #72), Tier A for this page. No new paper was found.

**Known gaps.** No study was found of practices before or during recreational use; products that combine dextromethorphan with paracetamol or antihistamines carry their own risks (DXM list).

---

## 21. Nitrous oxide — `PDFs/Nitrous-oxide/`

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 48 | Temple & Horowitz — Nitrous oxide abuse induced subacute combined degeneration despite patient initiated B12 supplementation (case report) | Clin Toxicol (Phila) 2022 | 10.1080/15563650.2022.2046772 | — | Nitrous-oxide/Temple_2022_B12SupplementationDespiteUse.pdf |

**Already on other lists (not repeated):** Nitrous-oxide #9 Brunt et al. (peripheral neurotoxicity review, including vitamin B12; PMC11986278) and #22 Ménétrier et al. 2023 (vitamin B12 status in people who use nitrous oxide, systematic review), Tier B for this page.

**Known gaps.** Taking vitamin B12 or methionine while continuing to use is popular, but the only evidence found is a case report of nerve damage despite self-started B12 (Temple 2022); no study tested it. No study was found of sitting down, breaks between inhalations or having someone present.

---

## 22. Cannabis (THC, CBD) — `PDFs/Cannabis/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 49 | Freeman et al. — How does cannabidiol (CBD) influence the acute effects of delta-9-tetrahydrocannabinol (THC) in humans? A systematic review | Neurosci Biobehav Rev 2019 | 10.1016/j.neubiorev.2019.09.036 | — | Cannabis/Freeman_2019_CBDInfluenceTHC_SR.pdf |
| 50 | Zamarripa et al. — Assessment of orally administered Δ9-tetrahydrocannabinol when coadministered with cannabidiol on Δ9-tetrahydrocannabinol pharmacokinetics and pharmacodynamics in healthy adults: a randomized clinical trial | JAMA Netw Open 2023 | 10.1001/jamanetworkopen.2022.54752 | PMC9926328 | Cannabis/Zamarripa_2023_OralCBDTHCInteractionRCT.pdf |
| 51 | Freeman et al. — Does variation in trait schizotypy and frequency of cannabis use influence the acute subjective, cognitive and psychotomimetic effects of delta-9-tetrahydrocannabinol? A mega-analysis | J Psychopharmacol 2021 | 10.1177/0269881120959601 | — | Cannabis/Freeman_2021_SchizotypyFrequencyMegaAnalysis.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 52 | Chester et al. — Does co-administration of cannabidiol (CBD) influence the plasma availability of delta-9-tetrahydrocannabinol (THC) and its active metabolite in humans? A systematic review and meta-analysis | Neurosci Biobehav Rev 2026 | 10.1016/j.neubiorev.2026.106910 | publisher | Cannabis/Chester_2026_CBDTHCPlasmaMA.pdf |
| 53 | Arkell et al. — Effect of cannabidiol and Δ9-tetrahydrocannabinol on driving performance: a randomized clinical trial (an editorial and three letters in JAMA, see search log) | JAMA 2020 | 10.1001/jama.2020.21218 | PMC7709000 | Cannabis/Arkell_2020_CBDTHCDrivingRCT.pdf |
| 54 | Lawn et al. — The acute effects of cannabis with and without cannabidiol in adults and adolescents: a randomised, double-blind, placebo-controlled, crossover experiment | Addiction 2023 | 10.1111/add.16154 | PMC10481756 | Cannabis/Lawn_2023_CBDAdultsAdolescents.pdf |
| 55 | Solowij et al. — A randomised controlled trial of vaporised Δ9-tetrahydrocannabinol and cannabidiol alone and in combination in frequent and infrequent cannabis users: acute intoxication effects | Eur Arch Psychiatry Clin Neurosci 2019 | 10.1007/s00406-019-00978-2 | — | Cannabis/Solowij_2019_VaporisedTHCCBDRCT.pdf |
| 56 | Haney et al. — Oral cannabidiol does not alter the subjective, reinforcing or cardiovascular effects of smoked cannabis | Neuropsychopharmacology 2016 (online 2015) | 10.1038/npp.2015.367 | PMC4908634 | Cannabis/Haney_2016_OralCBDSmokedCannabis.pdf |

**Already on other lists (not repeated):** Cannabis #67 Englund et al. 2013 (CBD and THC-elicited paranoia) and #68 Englund et al. 2023 (does cannabidiol make cannabis safer?; PMC10156730), Tier A for this page; #69 Morgan et al. 2010 (CBD content and acute effects, naturalistic) and #70 Bhattacharyya et al. 2010 (opposite effects of THC and CBD), Tier B.

**Known gaps.** CBD taken with THC has controlled trials with mixed results, and one trial shows oral CBD raising THC levels and effects (Zamarripa 2023); no study was found of CBD products taken by people who use cannabis outside the laboratory. Predictors of a difficult experience (paranoia, anxiety) come from pooled laboratory data. No study was found of setting, company, food or hydration with cannabis, or of edibles and taking more before the first dose has acted.

---

## 23. Synthetic cannabinoids — `PDFs/Synthetic-cannabinoids/`

**Already on other lists (not repeated):** None. No new paper was found.

**Known gaps.** No study was found of practices before or during synthetic cannabinoid use; the protective practice most discussed in this literature is drug checking (out of scope).

---

## 24. Heroin — `PDFs/Heroin/`

The papers here concern using alone and the people present, and also serve the Fentanyl, Prescription-opioids, Methadone-Buprenorphine and Kratom pages; they are saved under `_Cross-cutting/`.

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 57 | Papamihali et al. — Convenience and comfort: reasons reported for using drugs alone among clients of harm reduction sites in British Columbia, Canada | Harm Reduct J 2020 | 10.1186/s12954-020-00436-6 | PMC7682134 | _Cross-cutting/Papamihali_2020_ReasonsUsingAlone.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 58 | Rosen et al. — Safety in solitude? Competing risks and drivers of solitary drug use among women who inject drugs and implications for overdose detection | Addiction 2023 (online 2022) | 10.1111/add.16103 | PMC10073256 | _Cross-cutting/Rosen_2023_SolitaryDrugUseWomen.pdf |
| 59 | Ataiants et al. — Circumstances of overdose among street-involved, opioid-injecting women: drug, set, and setting | Int J Drug Policy 2020 | 10.1016/j.drugpo.2020.102691 | PMC7302961 | _Cross-cutting/Ataiants_2020_OverdoseDrugSetSetting.pdf |

**Already on other lists (not repeated):** Heroin #48 Darke et al. 1996 (responses to overdose by others present) and #49 McGregor et al. 1998 (circumstances of non-fatal overdose), _Overdose-and-emergency #70 Perri et al. 2021 (how to spot someone using alone) and #69 Bristowe et al. 2021 (virtual overdose response for people who use alone, protocol), and _Harm-reduction #74 McCrae et al. 2020 (injecting alone), Tier B for this page.

**Known gaps.** Using alone is well described (how common, why, for whom), but no trial was found of buddy systems, phone lines or apps that spot someone using alone beyond protocols and pilot reports. Lower tolerance after a break is on the _Tolerance list; 'tester' amounts are dosing and out of scope.

---

## 25. Fentanyl and analogues — `PDFs/Fentanyl-and-analogues/`

**Already on other lists (not repeated):** None beyond those named under Heroin. No new paper was found.

**Also needed:** the papers under Heroin (#57–#59).

**Known gaps.** As for Heroin; no study was found that is specific to fentanyl.

---

## 26. Prescription opioids — `PDFs/Prescription-opioids/`

**Already on other lists (not repeated):** DayAfter #96 Nee et al. 2018 and #97 Kistemaker et al. 2024 (medicines to prevent and treat opioid-induced constipation), Tier B for this page. No new paper was found.

**Also needed:** the papers under Heroin.

**Known gaps.** No study was found of practices before or during non-prescribed use of opioid tablets.

---

## 27. Methadone and buprenorphine — `PDFs/Methadone-Buprenorphine/`

**Already on other lists (not repeated):** None. No new paper was found.

**Also needed:** the papers under Heroin.

**Known gaps.** No study was found of practices before or during non-prescribed use.

---

## 28. Kratom — `PDFs/Kratom/`

**Already on other lists (not repeated):** None. No new paper was found.

**Known gaps.** No study was found of practices before or during kratom use (taking it with food, fluids), or of whether any reduces nausea or other side-effects.

---

## 29. Alkyl nitrites and inhalants — `PDFs/Alkyl-nitrites-and-inhalants/`

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 60 | Bass — Sudden sniffing death (landmark: deaths after exertion or fright during solvent inhalation; DOI from a Crossref bibliographic search, the PubMed record has none) | JAMA 1970 | 10.1001/jama.1970.03170250031004 | — | Alkyl-nitrites-and-inhalants/Bass_1970_SuddenSniffingDeath.pdf |

**Known gaps.** Thin and old literature: the landmark case series and later death series (Darke et al. 2023, not listed). No study was found of practices during inhalant or poppers use (resting, not running, having someone present), or of whether any works.

---

## 30. Salvia divinorum — `PDFs/Salvia-divinorum/`

**Already on other lists (not repeated):** Salvia-divinorum #23 Sumnall et al. (online survey of use and phenomenology), Tier B for this page. No new paper was found.

**Known gaps.** Having a sober 'sitter' is the practice most often recommended for salvia, but no study was found that measured how often it is used or whether it prevents injury.

---

## 31. Cross-cutting (several drugs) — `PDFs/_Cross-cutting/`

Papers that span several drug pages: set and setting, preparation, predictors and challenging experiences with psychedelics (#61–#82), heat (#83–#85), and nightlife settings and peer support (#86–#88). Each drug section names the ones it needs.

### Tier A
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 61 | Carhart-Harris et al. — Psychedelics and the essential importance of context | J Psychopharmacol 2018 | 10.1177/0269881118754710 | — | _Cross-cutting/CarhartHarris_2018_ImportanceOfContext.pdf |
| 62 | Aday et al. — Predicting reactions to psychedelic drugs: a systematic review of states and traits related to acute drug effects | ACS Pharmacol Transl Sci 2021 | 10.1021/acsptsci.1c00014 | PMC8033773 | _Cross-cutting/Aday_2021_PredictingReactionsSR.pdf |
| 63 | Haijen et al. — Predicting responses to psychedelics: a prospective study | Front Pharmacol 2018 | 10.3389/fphar.2018.00897 | PMC6225734 | _Cross-cutting/Haijen_2018_PredictingResponsesProspective.pdf |
| 64 | Estric et al. — Set and setting of psychedelics for therapeutic use in psychiatry: a systematic review | J Psychopharmacol 2025 | 10.1177/02698811251338214 | — | _Cross-cutting/Estric_2025_SetSettingTherapeuticSR.pdf |
| 65 | Simonsson et al. — Prevalence and associations of challenging, difficult or distressing experiences using classic psychedelics | J Affect Disord 2023 | 10.1016/j.jad.2023.01.073 | PMC9974873 | _Cross-cutting/Simonsson_2023_ChallengingExperiencesPrevalence.pdf |
| 66 | Wood et al. — Strategies for resolving challenging psychedelic experiences: insights from a mixed-methods study | Sci Rep 2024 | 10.1038/s41598-024-79931-w | PMC11582610 | _Cross-cutting/Wood_2024_ResolvingChallengingExperiences.pdf |
| 67 | Piercey et al. — Protective behavioral strategies for psychedelic use: a mini review of the evidence | Psychedelic Med (New Rochelle) 2024 | 10.1089/psymed.2023.0052 | PMC11658379 | _Cross-cutting/Piercey_2024_ProtectiveStrategiesPsychedelics.pdf |
| 68 | Palmer & Maynard — Are you tripping comfortably? Investigating the relationship between harm reduction and the psychedelic experience | Harm Reduct J 2022 | 10.1186/s12954-022-00662-0 | PMC9310449 | _Cross-cutting/Palmer_2022_HarmReductionPsychedelicExperience.pdf |
| 69 | Kaelen et al. — The hidden therapist: evidence for a central role of music in psychedelic therapy (correction 10.1007/s00213-018-4886-8; read with Nader 2025) | Psychopharmacology (Berl) 2018 | 10.1007/s00213-017-4820-5 | PMC5893695 | _Cross-cutting/Kaelen_2018_HiddenTherapistMusic.pdf |

### Tier B
| # | Paper | Journal, year | DOI | Free? | Save as |
|---|---|---|---|---|---|
| 70 | Golden et al. — Effects of setting on psychedelic experiences, therapies, and outcomes: a rapid scoping review of the literature | Curr Top Behav Neurosci 2022 | 10.1007/7854_2021_298 | publisher | _Cross-cutting/Golden_2022_SettingScopingReview.pdf |
| 71 | Hartogsohn — Set and setting for psychedelic harm reduction | Curr Top Behav Neurosci 2026 (online 2024) | 10.1007/7854_2024_509 | — | _Cross-cutting/Hartogsohn_2026_SetSettingHarmReduction.pdf |
| 72 | Thal et al. — Therapeutic (sub)stance: current practice and therapeutic conduct in preparatory sessions in substance-assisted psychotherapy — a systematized review | J Psychopharmacol 2022 | 10.1177/02698811221127954 | — | _Cross-cutting/Thal_2022_PreparatorySessionsReview.pdf |
| 73 | Borkel et al. — Set and setting predict psychopathology, wellbeing and meaningfulness of psychedelic experiences: a correlational study | Expert Rev Clin Pharmacol 2024 (online 2023) | 10.1080/17512433.2023.2295997 | — | _Cross-cutting/Borkel_2024_SetSettingPredict.pdf |
| 74 | Kettner et al. — Psychedelic communitas: intersubjective experience during psychedelic group sessions predicts enduring changes in psychological wellbeing and social connectedness | Front Pharmacol 2021 | 10.3389/fphar.2021.623985 | PMC8114773 | _Cross-cutting/Kettner_2021_PsychedelicCommunitas.pdf |
| 75 | Low & Earleywine — Intention-setting among recreational psychedelic users: associated acute effects and changes in well-being | J Psychoactive Drugs 2026 | 10.1080/02791072.2026.2673844 | — | _Cross-cutting/Low_2026_IntentionSetting.pdf |
| 76 | Olson et al. — Tripping on nothing: placebo psychedelics and contextual factors | Psychopharmacology (Berl) 2020 | 10.1007/s00213-020-05464-5 | — | _Cross-cutting/Olson_2020_PlaceboPsychedelicsContext.pdf |
| 77 | Marrocu et al. — Psychiatric risks for worsened mental health after psychedelic use | J Psychopharmacol 2024 | 10.1177/02698811241232548 | PMC10944581 | _Cross-cutting/Marrocu_2024_PsychiatricRisks.pdf |
| 78 | Yates & Melon — Trip-killers: a concerning practice associated with psychedelic drug use (medicines taken during a difficult experience to end it) | Emerg Med J 2024 (online 2023) | 10.1136/emermed-2023-213377 | publisher | _Cross-cutting/Yates_2024_TripKillers.pdf |
| 79 | O'Callaghan et al. — Experience of music used with psychedelic therapy: a rapid review and implications | J Music Ther 2020 | 10.1093/jmt/thaa006 | — | _Cross-cutting/OCallaghan_2020_MusicPsychedelicTherapyReview.pdf |
| 80 | Nader — Psychedelic minimalism: the case against music in psychedelic therapy settings (critique; read with Kaelen 2018) | Front Psychiatry 2025 | 10.3389/fpsyt.2025.1652568 | PMC12417490 | _Cross-cutting/Nader_2025_CaseAgainstMusic.pdf |
| 81 | Carvalho et al. — Crisis intervention related to the use of psychoactive substances in recreational settings: evaluating the Kosmicare project at Boom Festival | Curr Drug Abuse Rev 2014 (published 2015) | 10.2174/1874473708666150107115515 | — | _Cross-cutting/Carvalho_2014_KosmicareCrisisIntervention.pdf |
| 82 | Robinson et al. — Coming back together: a qualitative survey study of coping and support strategies used by people to cope with extended difficulties after the use of psychedelic drugs (an after-effect remedy not on the DayAfter list) | Front Psychol 2024 | 10.3389/fpsyg.2024.1369715 | PMC11166081 | _Cross-cutting/Robinson_2024_CopingExtendedDifficulties.pdf |
| 83 | Bohnert et al. — Ambient temperature and risk of death from accidental drug overdose in New York City, 1990–2006 | Addiction 2010 | 10.1111/j.1360-0443.2009.02887.x | PMC2898915 | _Cross-cutting/Bohnert_2010_TemperatureOverdoseNYC.pdf |
| 84 | Henderson et al. — Hot weather and death related to acute cocaine, opioid and amphetamine toxicity in British Columbia, Canada: a time-stratified case-crossover study | CMAJ Open 2023 | 10.9778/cmajo.20210291 | PMC10310343 | _Cross-cutting/Henderson_2023_HotWeatherToxicityDeaths.pdf |
| 85 | Chang et al. — Associations between short-term ambient temperature exposure and emergency department visits for amphetamine, cocaine, and opioid use in California from 2005 to 2019 | Environ Int 2023 | 10.1016/j.envint.2023.108233 | PMC10712015 | _Cross-cutting/Chang_2023_TemperatureEDVisits.pdf |
| 86 | Palamar & Sönmez — A qualitative investigation exploring why dance festivals are risky environments for drug use and potential adverse outcomes | Harm Reduct J 2022 | 10.1186/s12954-022-00598-5 | PMC8817488 | _Cross-cutting/Palamar_2022_FestivalRiskEnvironments.pdf |
| 87 | Wadds et al. — "It's like a safety net for when things go wrong": key stakeholder and program user perspectives on a peer-led safe space program in Sydney, Australia | Harm Reduct J 2023 | 10.1186/s12954-023-00854-2 | PMC10492353 | _Cross-cutting/Wadds_2023_PeerLedSafeSpace.pdf |
| 88 | Herrijgers et al. — Harm reduction practices and needs in a Belgian chemsex context: findings from a qualitative study | Int J Environ Res Public Health 2020 | 10.3390/ijerph17239081 | PMC7730975 | _Cross-cutting/Herrijgers_2020_ChemsexHarmReduction.pdf |

**Already on other lists (not repeated):** _Interactions #80 Dutton et al. 2025 (harm-reduction practices for people who use psychedelics, scoping review; PMC12495836), Tier A for this page; for the time after use, DayAfter #104 Evens et al. 2023 (afterglow systematic review) and #108 Evens et al. 2026 (managing psychological challenges in the afterglow window), Tier B.

**Known gaps.** Set and setting are studied mostly in clinical trials and cross-sectional surveys of people who used psychedelics, with few prospective studies (Haijen 2018) and no trial that varied the setting of recreational use; music has one randomised comparison (Strickland 2021, under Psilocybin) and a published case against its use (Nader 2025). Sitters and guides outside clinics are recommended by harm-reduction guides but were not found studied; crisis services at festivals have evaluations without comparison groups (Carvalho 2014; Wadds 2023). Heat: population studies link high temperatures to drug deaths and emergency visits, but no study tested cooling, water or rest. Grey-literature guidance (for example 'safer dancing' guidelines, EUDA nightlife and festival guides, and psychedelic crisis-support manuals) could not be searched with this method; see the search log.

---

## Reports and records without a DOI

No report without a DOI was verified in this build: the method allowed only PubMed and Crossref, so grey literature (EUDA nightlife and festival guidance, national 'safer dancing' guidelines, psychedelic crisis-support manuals) was not reached. Relevant PubMed records that carry no DOI, and were therefore not listed, are named in the search log (for example Jones & Jönsson 1994 on food and blood alcohol; Watkins & Adler 1993; Pittler et al. 2003, artichoke extract taken before drinking; Martinez et al. 2002, drug-associated heat stroke; Calafat et al. 2009, nightlife prevention review).

---

## Verification block (2026-10-31)

- **Final list:** 88 new papers (Tier A 28, Tier B 60) across 16 drug sections and Cross-cutting; the other 14 drug sections have no new paper and say so. Papers already on other lists are named in each section's "Already on other lists" line and are not counted.
- **DOIs fetched:** every one of the 88 listed DOIs was fetched from Crossref `works/<DOI>` in this reader's browser tab on 2026-10-31, once at drafting and again in a final sweep; all 88 resolved to the paper named, with matching title, year and first author. Also fetched: the two correction notices (10.1007/s00213-018-4886-8; 10.1021/acsptsci.1c00119), the editorial and three letters on Arkell et al. 2020, a Lancet letter on Henry et al. 1992, two further BMJ letters on Matthai et al. 1996 and a commentary on Rosen et al. 2023 (DOIs in the search log). No fetched DOI failed to resolve; none was dropped for resolving to another paper. No DOI was written from memory: each came from a PubMed `esummary` record or, for Bass 1970, from a Crossref bibliographic search, and was then fetched.
- **Matched to PubMed:** 87 of the 88 DOIs are carried by a PubMed record. Bass 1970 (#60) has no DOI in PubMed; a Crossref bibliographic search on title, author and journal returned one matching record (10.1001/jama.1970.03170250031004), which was fetched and matched on title, year and author.
- **Moved to "already listed" at the overlap check** (DOI index of all `search-logs/*_DOI-LIST.md`, 3,252 DOIs): Johnson 2008, Studerus 2012, Carbonaro 2016, Barrett 2016 and 2017 (Psilocybin #17, #24, #26, #27, #52), Szigeti 2021 (LSD #9), Pontual 2022 and Uthaug 2021 (DMT-Ayahuasca #35, #28), Lancelotta 2020 (5-MeO-DMT #12), Doesburg-van Kleffens 2023 (Mescaline #11), Evans 2023 (five psychedelic lists), Dutton 2025 (_Interactions #80), Parrott 2012 (MDMA #31), Farré 2004, Peiró 2013, Farré 2015 and Humbert-Droz 2026 (_Tolerance #188, #189, #192, #193), Harding 2022 (methamphetamine #101), Freestone 2023 (GHB-GBL #46), Zawertailo 1998 (DXM #4), Englund 2013 and 2023 (Cannabis #67, #68). None of the 88 new DOIs is on another list, including the DayAfter list.
- **Corrections and errata:** #69 Kaelen et al. 2018 (correction 10.1007/s00213-018-4886-8, in Crossref `updated-by`); #37 Strickland et al. 2021 (correction 10.1021/acsptsci.1c00119, linked in PubMed but not in Crossref `updated-by`; the correction record was fetched). Obtain each with its notice.
- **Retractions:** none of the 88 listed papers has a retraction in Crossref `updated-by` or in PubMed's correction links. Seen in search results and not listed: a ketamine trial report in Br J Psychiatry 2025 (Mills et al., marked "Retracted Publication" in PubMed; not on this topic).
- **Metadata kept as found:** where Crossref (online) and PubMed (print) years differ, the print year is given with the online year in brackets (8 rows). Of these, #11 Rogers 2008 also has a 2007 print date in Crossref for an issue PubMed dates 2008, and #71 Hartogsohn is a book chapter dated 2024 (online and print) in Crossref and 2026 in PubMed. Two further rows: #38 Murphy 2022 (online only, 2022, in volume 12, which PubMed dates 2021) and #81 Carvalho (issue dated 2014, published 2015 per Crossref). Crossref lists only the first author for #14 Marzuk 1998 (authors from PubMed) and misspells the title of #40 Leary 1963 (title from PubMed).
- **Free to read:** 46 of the 88 new papers (42 with a PMC id from the PubMed record, 4 open at the publisher per OpenAlex `open_access`). Copies in institutional repositories (OpenAlex "green" without PMC) are not counted.
- **Numbering:** rows are numbered in page order; the search log names papers by first author and year, not by number.
