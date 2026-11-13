# _Interactions (drug–drug combinations) — evidence map and PDF list (v0.1, 2026-10-15)

Cross-cutting topic: the evidence base for a drug–drug combination matrix (opioid + sedative mortality cohorts; serotonin toxicity; stimulant + alcohol; GHB and ketamine with depressants; cannabis + alcohol driving; lithium + psychedelics; CYP2D6 pharmacokinetic interactions; polysubstance overdose epidemiology). Save each PDF into `PDFs/_Cross-cutting/` with the filename given.

How this list was built: (1) landmark studies and their published critiques, replies and follow-ups; (2) Crossref bibliographic searches on the pre-registered section queries (`_Interactions_search-log.md`); (3) OpenAlex title searches to locate DOIs for recalled landmarks (Crossref's search endpoint was rate-limited for most of the session; see the log). The PubMed layer (strings in the log) is still to be run and will add to this list.

**Verification status of each DOI (column "V")** — every DOI below was fetched on 2026-10-15 and resolved to the paper named; the fetch route differs because the Crossref API was shared with other co-editors and throttled:
- `CR` = Crossref `works/<DOI>` (or `works?filter=doi:` batch) record fetched: title, journal, year, first author and `updated-by` checked. This is the METHODS §4.2 standard.
- `OA` = OpenAlex record for the DOI fetched (title, year, `is_retracted` = false); Crossref re-fetch still pending. OpenAlex metadata is derived from Crossref, so the DOI is registered and resolves, but `updated-by` (errata) has not been read from Crossref.
- `CS` = DOI, title, journal and year returned by the Crossref search endpoint itself; the `works/<DOI>` record (errata field) not yet fetched.
- `PP` = DOI resolved through doi.org to the publisher's page, which shows the title/journal/year (no retraction field read).
Items marked other than `CR` should be re-checked with `works/<DOI>` before the reference record is created (§4.2); none of them is retracted according to the source consulted.

---

## Tier A — needed first (serotonin toxicity core; opioid + sedative cohorts; psychedelic and stimulant combination reviews)

| # | Paper | Journal, year | DOI | V | Save as |
|---|---|---|---|---|---|
| 1 | Boyer & Shannon — The serotonin syndrome | N Engl J Med 2005 | 10.1056/NEJMra041867 | CR | _Cross-cutting/Boyer_2005_SerotoninSyndrome.pdf |
| 2 | Dunkley et al. — The Hunter Serotonin Toxicity Criteria: simple and accurate diagnostic decision rules for serotonin toxicity | QJM 2003 | 10.1093/qjmed/hcg109 | CR | _Cross-cutting/Dunkley_2003_HunterCriteria.pdf |
| 3 | Sternbach — The serotonin syndrome (original criteria; Crossref record lacks author field, title/volume/pages match) | Am J Psychiatry 1991 | 10.1176/ajp.148.6.705 | CR | _Cross-cutting/Sternbach_1991_SerotoninSyndrome.pdf |
| 4 | Werneke et al. — Conundrums in neurology: diagnosing serotonin syndrome – a meta-analysis of cases (performance of Sternbach/Hunter/Radomski criteria) | BMC Neurology 2016 | 10.1186/s12883-016-0616-1 | CR | _Cross-cutting/Werneke_2016_DiagnosingSerotoninSyndromeMetaAnalysis.pdf |
| 5 | Isbister, Buckley & Whyte — Serotonin toxicity: a practical approach to diagnosis and treatment | Med J Aust 2007 | 10.5694/j.1326-5377.2007.tb01282.x | CR | _Cross-cutting/Isbister_2007_SerotoninToxicityPracticalApproach.pdf |
| 6 | Buckley, Dawson & Isbister — Serotonin syndrome | BMJ 2014 | 10.1136/bmj.g1626 | CR | _Cross-cutting/Buckley_2014_SerotoninSyndromeBMJ.pdf |
| 7 | Gillman — Monoamine oxidase inhibitors, opioid analgesics and serotonin toxicity (which opioids are serotonergic) | Br J Anaesth 2005 | 10.1093/bja/aei210 | CR | _Cross-cutting/Gillman_2005_MAOIOpioidsSerotoninToxicity.pdf |
| 8 | Halman et al. — Drug–drug interactions involving classic psychedelics: a systematic review | J Psychopharmacol 2024 | 10.1177/02698811231211219 | CR | _Cross-cutting/Halman_2024_PsychedelicDDISystematicReview.pdf |
| 9 | Sarparast et al. — Drug-drug interactions between psychiatric medications and MDMA or psilocybin: a systematic review | Psychopharmacology 2022 | 10.1007/s00213-022-06083-y | CR | _Cross-cutting/Sarparast_2022_PsychiatricMedsMDMAPsilocybinSR.pdf |
| 10 | Nayak et al. — Classic psychedelic coadministration with lithium, but not lamotrigine, is associated with seizures: an analysis of online psychedelic experience reports | Pharmacopsychiatry 2021 | 10.1055/a-1524-2794 | CR | _Cross-cutting/Nayak_2021_LithiumPsychedelicsSeizures.pdf |
| 11 | Park et al. — Benzodiazepine prescribing patterns and deaths from drug overdose among US veterans receiving opioid analgesics: case-cohort study | BMJ 2015 | 10.1136/bmj.h2698 | CR | _Cross-cutting/Park_2015_BenzodiazepineOpioidOverdoseVeterans.pdf |
| 12 | Sun et al. — Association between concurrent use of prescription opioids and benzodiazepines and overdose: retrospective analysis | BMJ 2017 | 10.1136/bmj.j760 | CR | _Cross-cutting/Sun_2017_ConcurrentOpioidBenzodiazepineOverdose.pdf |
| 13 | Dasgupta et al. — Cohort study of the impact of high-dose opioid analgesics on overdose mortality (benzodiazepine co-prescription) | Pain Medicine 2016 | 10.1111/pme.12907 | OA | _Cross-cutting/Dasgupta_2016_HighDoseOpioidOverdoseMortalityCohort.pdf |
| 14 | Jones & McAninch — Emergency department visits and overdose deaths from combined use of opioids and benzodiazepines | Am J Prev Med 2015 | 10.1016/j.amepre.2015.03.040 | CR | _Cross-cutting/Jones_2015_OpioidBenzodiazepineEDVisitsDeaths.pdf |
| 15 | Gomes et al. — Gabapentin, opioids, and the risk of opioid-related death: a population-based nested case–control study | PLOS Medicine 2017 | 10.1371/journal.pmed.1002396 | CR | _Cross-cutting/Gomes_2017_GabapentinOpioidDeath.pdf |
| 16 | Gomes et al. — Pregabalin and the risk for opioid-related death: a nested case–control study | Ann Intern Med 2018 | 10.7326/M18-1136 | CR | _Cross-cutting/Gomes_2018_PregabalinOpioidDeath.pdf |
| 17 | Macleod et al. — Prescription of benzodiazepines, z-drugs, and gabapentinoids and mortality risk in people receiving opioid agonist treatment (UK CPRD) | PLOS Medicine 2019 | 10.1371/journal.pmed.1002965 | OA | _Cross-cutting/Macleod_2019_SedativesMortalityOAT.pdf |
| 18 | Tori, Larochelle & Naimi — Alcohol or benzodiazepine co-involvement with opioid overdose deaths in the United States, 1999–2017 | JAMA Netw Open 2020 | 10.1001/jamanetworkopen.2020.2361 | CR | _Cross-cutting/Tori_2020_AlcoholBenzoCoinvolvementOpioidDeaths.pdf |
| 19 | Hickman et al. — Does alcohol increase the risk of overdose death: the need for a translational approach | Addiction 2008 | 10.1111/j.1360-0443.2008.02134.x | OA | _Cross-cutting/Hickman_2008_AlcoholOverdoseDeathTranslational.pdf |
| 20 | White & Irvine — Mechanisms of fatal opioid overdose | Addiction 1999 | 10.1046/j.1360-0443.1999.9479612.x | OA | _Cross-cutting/White_1999_MechanismsFatalOpioidOverdose.pdf |
| 21 | Pennings, Leccese & de Wolff — Effects of concurrent use of alcohol and cocaine | Addiction 2002 | 10.1046/j.1360-0443.2002.00158.x | CR | _Cross-cutting/Pennings_2002_AlcoholCocaineConcurrent.pdf |
| 22 | McCance-Katz, Kosten & Jatlow — Concurrent use of cocaine and alcohol is more potent and potentially more toxic than use of either alone — a multiple-dose study | Biol Psychiatry 1998 | 10.1016/S0006-3223(97)00426-5 | CR | _Cross-cutting/McCanceKatz_1998_CocaineAlcoholMultipleDose.pdf |
| 23 | Thai, Dyer, Benowitz & Haller — Gamma-hydroxybutyrate and ethanol effects and interactions in humans | J Clin Psychopharmacol 2006 | 10.1097/01.jcp.0000237944.57893.28 | CR | _Cross-cutting/Thai_2006_GHBEthanolInteractions.pdf |
| 24 | Galicia et al. — Clinical relevance of ethanol coingestion in patients with GHB/GBL intoxication (Euro-DEN) | Toxicol Lett 2019 | 10.1016/j.toxlet.2019.07.001 | CR | _Cross-cutting/Galicia_2019_EthanolCoingestionGHB.pdf |
| 25 | Asbridge, Hayden & Cartwright — Acute cannabis consumption and motor vehicle collision risk: systematic review of observational studies and meta-analysis | BMJ 2012 | 10.1136/bmj.e536 | OA | _Cross-cutting/Asbridge_2012_CannabisCollisionRiskSRMA.pdf |
| 26 | Rogeberg & Elvik — The effects of cannabis intoxication on motor vehicle collision revisited and revised (correction published 2018, 10.1111/add.14140; obtain both) | Addiction 2016 | 10.1111/add.13347 | OA | _Cross-cutting/Rogeberg_2016_CannabisCollisionRevisited.pdf |
| 27 | Hartman et al. — Cannabis effects on driving lateral control with and without alcohol | Drug Alcohol Depend 2015 | 10.1016/j.drugalcdep.2015.06.015 | OA | _Cross-cutting/Hartman_2015_CannabisAlcoholDrivingLateralControl.pdf |
| 28 | Dubois et al. — The combined effects of alcohol and cannabis on driving: impact on crash risk | Forensic Sci Int 2015 | 10.1016/j.forsciint.2014.12.018 | OA | _Cross-cutting/Dubois_2015_AlcoholCannabisCrashRisk.pdf |
| 29 | Compton, Valentino & DuPont — Polysubstance use in the U.S. opioid crisis | Mol Psychiatry 2021 | 10.1038/s41380-020-00949-3 | OA | _Cross-cutting/Compton_2021_PolysubstanceUseOpioidCrisis.pdf |
| 30 | Karamouzian et al. — Latent patterns of polysubstance use among people who use opioids: a systematic review | Int J Drug Policy 2022 | 10.1016/j.drugpo.2022.103584 | OA | _Cross-cutting/Karamouzian_2022_PolysubstancePatternsSR.pdf |
| 31 | Gladden et al. — Changes in opioid-involved overdose deaths by opioid type and presence of benzodiazepines, cocaine, and methamphetamine — 25 states, 2017–2018 | MMWR 2019 | 10.15585/mmwr.mm6834a2 | OA | _Cross-cutting/Gladden_2019_MMWROpioidDeathsCoinvolvement.pdf |
| 32 | de la Torre, Yubero-Lahoz, Pardo-Lozano & Farré — MDMA, methamphetamine, and CYP2D6 pharmacogenetics: what is clinically relevant? | Front Genet 2012 | 10.3389/fgene.2012.00235 | CR | _Cross-cutting/delaTorre_2012_CYP2D6Pharmacogenetics.pdf |
| 33 | O'Mathúna et al. — The consequences of 3,4-methylenedioxymethamphetamine induced CYP2D6 inhibition in humans | J Clin Psychopharmacol 2008 | 10.1097/JCP.0b013e318184ff6e | CR | _Cross-cutting/OMathuna_2008_MDMACYP2D6Inhibition.pdf |
| 34 | Schmid et al. — CYP2D6 function moderates the pharmacokinetics and pharmacodynamics of MDMA in a controlled study in healthy individuals | Pharmacogenet Genomics 2016 | 10.1097/FPC.0000000000000231 | OA | _Cross-cutting/Schmid_2016_CYP2D6MDMAControlledStudy.pdf |
| 35 | Gasche et al. — Codeine intoxication associated with ultrarapid CYP2D6 metabolism | N Engl J Med 2004 | 10.1056/NEJMoa041888 | CR | _Cross-cutting/Gasche_2004_CodeineUltrarapidCYP2D6.pdf |

## Tier B — section backbone (case series, human laboratory interaction studies, class reviews, cohorts)

| # | Paper | Journal, year | DOI | V | Save as |
|---|---|---|---|---|---|
| 36 | Smilkstein, Smolinske & Rumack — A case of MAO inhibitor/MDMA interaction: agony after ecstasy | J Toxicol Clin Toxicol 1987 | 10.3109/15563658708992620 | CR | _Cross-cutting/Smilkstein_1987_MAOIMDMAInteraction.pdf |
| 37 | Vuori et al. — Death following ingestion of MDMA (ecstasy) and moclobemide | Addiction 2003 | 10.1046/j.1360-0443.2003.00292.x | CR | _Cross-cutting/Vuori_2003_MDMAMoclobemideDeaths.pdf |
| 38 | Callaway & Grob — Ayahuasca preparations and serotonin reuptake inhibitors: a potential combination for severe adverse interactions | J Psychoactive Drugs 1998 | 10.1080/02791072.1998.10399712 | CR | _Cross-cutting/Callaway_1998_AyahuascaSSRIs.pdf |
| 39 | Silins, Copeland & Dillon — Qualitative review of serotonin syndrome, ecstasy (MDMA) and the use of other serotonergic substances: hierarchy of risk | Aust N Z J Psychiatry 2007 | 10.1080/00048670701449237 | CR | _Cross-cutting/Silins_2007_SerotoninSyndromeMDMAHierarchyOfRisk.pdf |
| 40 | Pilgrim et al. — Deaths involving MDMA and the concomitant use of pharmaceutical drugs | J Anal Toxicol 2011 | 10.1093/anatox/35.4.219 | OA | _Cross-cutting/Pilgrim_2011_MDMADeathsPharmaceuticals.pdf |
| 41 | Liechti et al. — Acute psychological effects of MDMA ("ecstasy") are attenuated by the serotonin uptake inhibitor citalopram | Neuropsychopharmacology 2000 | 10.1016/S0893-133X(99)00148-7 | CR | _Cross-cutting/Liechti_2000_CitalopramAttenuatesMDMA.pdf |
| 42 | Farré et al. — Pharmacological interaction between MDMA (ecstasy) and paroxetine: pharmacological effects and pharmacokinetics | J Pharmacol Exp Ther 2007 | 10.1124/jpet.107.129056 | CR | _Cross-cutting/Farre_2007_MDMAParoxetineInteraction.pdf |
| 43 | Becker et al. — Acute effects of psilocybin after escitalopram or placebo pretreatment in a randomized, double-blind, placebo-controlled, crossover study in healthy subjects | Clin Pharmacol Ther 2022 | 10.1002/cpt.2487 | CR | _Cross-cutting/Becker_2022_PsilocybinEscitalopramPretreatment.pdf |
| 44 | Bonson, Buckholtz & Murphy — Chronic administration of serotonergic antidepressants attenuates the subjective effects of LSD in humans | Neuropsychopharmacology 1996 | 10.1016/0893-133X(95)00145-4 | CR | _Cross-cutting/Bonson_1996_AntidepressantsAttenuateLSD.pdf |
| 45 | Hassamal et al. — Tramadol: understanding the risk of serotonin syndrome and seizures | Am J Med 2018 | 10.1016/j.amjmed.2018.04.025 | OA | _Cross-cutting/Hassamal_2018_TramadolSerotoninSyndromeSeizures.pdf |
| 46 | Gillman — Triptans, serotonin agonists, and serotonin syndrome (serotonin toxicity): a review | Headache 2010 | 10.1111/j.1526-4610.2009.01575.x | OA | _Cross-cutting/Gillman_2010_TriptansSerotoninToxicity.pdf |
| 47 | Jones, Mogali & Comer — Polydrug abuse: a review of opioid and benzodiazepine combination use | Drug Alcohol Depend 2012 | 10.1016/j.drugalcdep.2012.07.004 | CR | _Cross-cutting/Jones_2012_OpioidBenzodiazepineCombinationReview.pdf |
| 48 | Bohnert et al. — Association between opioid prescribing patterns and opioid overdose-related deaths | JAMA 2011 | 10.1001/jama.2011.370 | CR | _Cross-cutting/Bohnert_2011_OpioidPrescribingOverdoseDeaths.pdf |
| 49 | Hernandez et al. — Exposure-response association between concurrent opioid and benzodiazepine use and risk of opioid-related overdose in Medicare Part D beneficiaries | JAMA Netw Open 2018 | 10.1001/jamanetworkopen.2018.0919 | CS | _Cross-cutting/Hernandez_2018_OpioidBenzoExposureResponseMedicare.pdf |
| 50 | Bharat et al. — Prescription opioid use among people with opioid dependence and concurrent benzodiazepine and gabapentinoid exposure: an analysis of overdose and all-cause mortality | Int J Drug Policy 2024 | 10.1016/j.drugpo.2023.104287 | CS | _Cross-cutting/Bharat_2024_OpioidDependenceBenzoGabapentinoidMortality.pdf |
| 51 | Lyndon et al. — Risk to heroin users of polydrug use of pregabalin or gabapentin | Addiction 2017 | 10.1111/add.13843 | OA | _Cross-cutting/Lyndon_2017_HeroinPregabalinGabapentin.pdf |
| 52 | Evoy et al. — Abuse and misuse of pregabalin and gabapentin: a systematic review update (comment 10.1007/s40265-021-01494-1 and authors' reply 10.1007/s40265-021-01495-0; obtain all three) | Drugs 2021 | 10.1007/s40265-020-01432-7 | OA | _Cross-cutting/Evoy_2021_GabapentinoidMisuseSRUpdate.pdf |
| 53 | Baird, Fox & Colvin — Gabapentinoid abuse in order to potentiate the effect of methadone: a survey among substance misusers | Eur Addict Res 2014 | 10.1159/000355268 | OA | _Cross-cutting/Baird_2014_GabapentinoidsPotentiateMethadone.pdf |
| 54 | Bachhuber et al. — Increasing benzodiazepine prescriptions and overdose mortality in the United States, 1996–2013 | Am J Public Health 2016 | 10.2105/AJPH.2016.303061 | OA | _Cross-cutting/Bachhuber_2016_BenzodiazepinePrescriptionsOverdoseMortality.pdf |
| 55 | Hearn et al. — Cocaethylene: a unique cocaine metabolite displays high affinity for the dopamine transporter | J Neurochem 1991 | 10.1111/j.1471-4159.1991.tb08205.x | CR | _Cross-cutting/Hearn_1991_CocaethyleneDAT.pdf |
| 56 | Farré et al. — Alcohol and cocaine interactions in humans | J Pharmacol Exp Ther 1993 | 10.1016/S0022-3565(25)39392-4 | CR | _Cross-cutting/Farre_1993_AlcoholCocaineInteractionsHumans.pdf |
| 57 | Jones — Forensic drug profile: cocaethylene | J Anal Toxicol 2019 | 10.1093/jat/bkz007 | OA | _Cross-cutting/Jones_2019_CocaethyleneForensicProfile.pdf |
| 58 | Miró et al. — Intoxication by gamma hydroxybutyrate and related analogues: clinical characteristics and comparison between pure intoxication and that combined with other substances of abuse (Euro-DEN) | Toxicol Lett 2017 | 10.1016/j.toxlet.2017.05.030 | OA | _Cross-cutting/Miro_2017_GHBPureVsCombinedIntoxication.pdf |
| 59 | Liechti et al. — Clinical features of gamma-hydroxybutyrate and gamma-butyrolactone toxicity and concomitant drug and alcohol use | Drug Alcohol Depend 2006 | 10.1016/j.drugalcdep.2005.07.010 | OA | _Cross-cutting/Liechti_2006_GHBGBLToxicityConcomitantUse.pdf |
| 60 | Krystal et al. — Interactive effects of subanesthetic ketamine and subhypnotic lorazepam in humans | Psychopharmacology 1998 | 10.1007/s002130050503 | OA | _Cross-cutting/Krystal_1998_KetamineLorazepamInteractive.pdf |
| 61 | Darke et al. — Characteristics and circumstances of death related to the self-administration of ketamine | Addiction 2021 | 10.1111/add.15154 | OA | _Cross-cutting/Darke_2021_KetamineDeathsCircumstances.pdf |
| 62 | Schifano et al. — Trapped in the "K-hole": overview of deaths associated with ketamine misuse in the UK (1993–2006) | J Clin Psychopharmacol 2008 | 10.1097/JCP.0b013e3181612cdc | OA | _Cross-cutting/Schifano_2008_KetamineDeathsUK.pdf |
| 63 | Hartman & Huestis — Cannabis effects on driving skills | Clin Chem 2013 | 10.1373/clinchem.2012.194381 | OA | _Cross-cutting/Hartman_2013_CannabisDrivingSkills.pdf |
| 64 | Sewell, Poling & Sofuoglu — The effect of cannabis compared with alcohol on driving | Am J Addict 2009 | 10.1080/10550490902786934 | OA | _Cross-cutting/Sewell_2009_CannabisVsAlcoholDriving.pdf |
| 65 | Bramness, Khiabani & Mørland — Impairment due to cannabis and ethanol: clinical signs and additive effects | Addiction 2010 | 10.1111/j.1360-0443.2010.02911.x | OA | _Cross-cutting/Bramness_2010_CannabisEthanolAdditiveImpairment.pdf |
| 66 | Hels et al. — Risk of severe driver injury by driving with psychoactive substances (DRUID) | Accid Anal Prev 2013 | 10.1016/j.aap.2013.06.003 | OA | _Cross-cutting/Hels_2013_DRUIDSevereDriverInjury.pdf |
| 67 | Tanaka — Toxicological interactions between alcohol and benzodiazepines | J Toxicol Clin Toxicol 2002 | 10.1081/CLT-120002887 | OA | _Cross-cutting/Tanaka_2002_AlcoholBenzodiazepineInteractions.pdf |
| 68 | Koski, Ojanperä & Vuori — Interaction of alcohol and drugs in fatal poisonings | Hum Exp Toxicol 2003 | 10.1191/0960327103ht324oa | OA | _Cross-cutting/Koski_2003_AlcoholDrugsFatalPoisonings.pdf |
| 69 | de la Torre et al. — Non-linear pharmacokinetics of MDMA ("ecstasy") in humans | Br J Clin Pharmacol 2000 | 10.1046/j.1365-2125.2000.00121.x | OA | _Cross-cutting/delaTorre_2000_NonlinearPKMDMA.pdf |
| 70 | de la Torre et al. — Human pharmacology of MDMA: pharmacokinetics, metabolism, and disposition | Ther Drug Monit 2004 | 10.1097/00007691-200404000-00009 | CR | _Cross-cutting/delaTorre_2004_HumanPharmacologyMDMA.pdf |
| 71 | Vizeli et al. — Pharmacogenetics of ecstasy: CYP1A2, CYP2C19, and CYP2B6 polymorphisms moderate pharmacokinetics of MDMA in healthy subjects | Eur Neuropsychopharmacol 2017 | 10.1016/j.euroneuro.2017.01.008 | CR | _Cross-cutting/Vizeli_2017_MDMAPharmacogeneticsCYP.pdf |
| 72 | Zawertailo et al. — Psychotropic effects of dextromethorphan are altered by the CYP2D6 polymorphism | J Clin Psychopharmacol 1998 | 10.1097/00004714-199808000-00014 | CR | _Cross-cutting/Zawertailo_1998_DextromethorphanCYP2D6.pdf |
| 73 | Crews et al. — Clinical Pharmacogenetics Implementation Consortium guidelines for CYP2D6 genotype and codeine therapy: 2014 update | Clin Pharmacol Ther 2014 | 10.1038/clpt.2013.254 | CR | _Cross-cutting/Crews_2014_CPICCodeineCYP2D6.pdf |

## Tier C — epidemiology of polysubstance overdose, context

| # | Paper | Journal, year | DOI | V | Save as |
|---|---|---|---|---|---|
| 74 | O'Donnell et al. — Trends in and characteristics of drug overdose deaths involving illicitly manufactured fentanyls — United States, 2019–2020 | MMWR 2021 | 10.15585/mmwr.mm7050e3 | OA | _Cross-cutting/ODonnell_2021_MMWRFentanylDeaths.pdf |
| 75 | Jones, Einstein & Compton — Changes in synthetic opioid involvement in drug overdose deaths in the United States, 2010–2016 | JAMA 2018 | 10.1001/jama.2018.2844 | OA | _Cross-cutting/Jones_2018_SyntheticOpioidInvolvementDeaths.pdf |
| 76 | Hoots, Vivolo-Kantor & Seth — The rise in non-fatal and fatal overdoses involving stimulants with and without opioids in the United States | Addiction 2020 | 10.1111/add.14878 | OA | _Cross-cutting/Hoots_2020_StimulantOverdosesWithWithoutOpioids.pdf |
| 77 | Palis et al. — Concurrent use of opioids and stimulants and risk of fatal overdose: a cohort study (British Columbia) | BMC Public Health 2022 | 10.1186/s12889-022-14506-w | OA | _Cross-cutting/Palis_2022_OpioidStimulantFatalOverdoseCohort.pdf |
| 78 | Warner-Smith, Darke, Lynskey & Hall — Heroin overdose: causes and consequences | Addiction 2001 | 10.1046/j.1360-0443.2001.96811135.x | OA | _Cross-cutting/WarnerSmith_2001_HeroinOverdoseCausesConsequences.pdf |
| 79 | Garg et al. — Patterns of opioid use and risk of opioid overdose death among Medicaid patients | Med Care 2017 | 10.1097/MLR.0000000000000738 | CS | _Cross-cutting/Garg_2017_OpioidPatternsOverdoseDeathMedicaid.pdf |
| 80 | Dutton et al. — Harm reduction practises for users of psychedelic drugs: a scoping review (covers online resources such as TripSit/PsychonautWiki as harm-reduction practice) | Harm Reduction Journal 2025 | 10.1186/s12954-025-01264-2 | OA, PP | _Cross-cutting/Dutton_2025_PsychedelicHarmReductionScopingReview.pdf |

## Reports (no DOI; save the PDF of the full report)

| # | Report | Save as |
|---|---|---|
| R1 | EUDA — European Drug Report 2026: Trends and Developments (polysubstance use section; drug-induced deaths with toxicology) | _Epidemiology/EUDA_2026_EuropeanDrugReport.pdf |
| R2 | EMCDDA — Polydrug use: health and social responses (mini guide, Health and social responses to drug problems: a European guide 2021) | _Epidemiology/EMCDDA_2021_PolydrugUseResponses.pdf |
| R3 | CDC — SUDORS (State Unintentional Drug Overdose Reporting System) dashboard/data brief, most recent year (co-involved substances) | _Epidemiology/CDC_SUDORS_latest.pdf |
| R4 | UNODC — World Drug Report 2025 (polydrug use and synthetic opioids booklets) | _Epidemiology/UNODC_2025_WorldDrugReport.pdf |
| R5 | ONS — Deaths related to drug poisoning in England and Wales, latest registrations (substances mentioned together on death certificates) | _Epidemiology/ONS_latest_DrugPoisoningDeaths.pdf |
| R6 | TripSit combination chart and PsychonautWiki "Dangerous/Unsafe/Caution" combination tables (archived copies with access date; community resources, not evidence; needed to document what they claim) | _Cross-cutting/TripSit_PsychonautWiki_CombinationCharts_accessed2026.pdf |

## Known gaps this list does not yet cover (to come from the PubMed layer)

- No peer-reviewed appraisal of the TripSit or PsychonautWiki combination charts was found (Crossref and OpenAlex searches; web search). Dutton et al. 2025 (item 80) is the closest: a scoping review of psychedelic harm-reduction practices that includes online resources. Treat the charts as community claims to be checked against the papers above.
- Benzodiazepine + methadone/buprenorphine clinical management (Lintzeris & Nielsen 2010, Am J Addict, "Benzodiazepines, methadone and buprenorphine: interactions and clinical management") — DOI not located this session.
- Abrahamsson et al. 2017 (Drug Alcohol Depend; benzodiazepine, z-drug and pregabalin prescriptions and mortality in Swedish OMT) and Cho et al. 2020 (J Gen Intern Med; overdose with opioids, benzodiazepines and z-drugs) — recalled but not verified; add after PubMed run.
- Darke & Hall 2003 (J Urban Health, "Heroin overdose: research and evidence-based intervention") — the recalled DOI resolved to a different paper; relocate by title.
- Ketamine + alcohol: only one human laboratory interaction study was located (Krystal 1998 ketamine–lorazepam; the ketamine "ethanol-like effects" study, Arch Gen Psychiatry 1998, 10.1001/archpsyc.55.4.354, was located in OpenAlex by title but not resolved). The literature on ketamine with depressants is thin and mostly case series/death reviews.
- GHB + alcohol toxicokinetic review (Metabolites 2023, "Interaction between γ-hydroxybutyric acid and ethanol") — DOI not located.
- Stimulant + opioid ("speedball") pharmacodynamics in human laboratory studies (Foltin & Fischman series) — not searched this session.
- Nitrous oxide, inhalants and alcohol; cannabis + tobacco; cannabis + opioids (opioid-sparing claims and critiques); MAOI-containing ayahuasca + stimulants — not yet covered.
- The psychedelic-seizure scoping review ("Do classic psychedelics increase the risk of seizures? A scoping review") — the DOI first assumed for it resolved to a case report; relocate by title.
- Serotonin-toxicity criteria critiques beyond Werneke 2016 (e.g., Prakash et al. on diagnostic criteria) — not located.

## Verification block (2026-10-15)

- DOIs fetched this session for this topic: 82 (Crossref `works/<DOI>` or `works?filter=doi:` records: 39 resolved; OpenAlex DOI records: 52 resolved, of which 15 duplicate Crossref-verified items; Crossref search-hit records: 3; publisher page via doi.org: 1).
- Final list: 80 papers. Crossref-verified (CR): 39. OpenAlex-resolved pending Crossref re-check (OA): 37. Crossref search-hit (CS): 3. Publisher page (PP) in addition to OA: 1.
- Dropped after fetching (resolved to a different paper than intended): 10.1080/02791072.1998.10399709 (resolved to Metzner 1998, not Callaway & Grob — corrected to 10.1080/02791072.1998.10399712); 10.1046/j.1360-0443.2003.00272.x (resolved to Demers 2003, not Vuori 2003 — corrected to 10.1046/j.1360-0443.2003.00292.x); 10.1080/00048670701579027 (did not resolve; Silins 2007 corrected to 10.1080/00048670701449237); 10.1093/jurban/jtg024 (resolved to a Russian Federation opiate-overdose paper, not Darke & Hall 2003 — excluded, see gaps); 10.3389/fneur.2023.1214969 (resolved to a Front Neurol 2023 case report of psychedelic-induced seizures, not the scoping review — excluded).
- Errata/corrections found: Rogeberg & Elvik 2016 has a published correction (10.1111/add.14140, 2018); Evoy et al. 2021 has a published comment and authors' reply (10.1007/s40265-021-01494-1; 10.1007/s40265-021-01495-0). None of the 39 Crossref records carries an `updated-by` field.
- Retractions: none found (Crossref `updated-by` for the 39 CR items; OpenAlex `is_retracted` = false for all OA items).
