# Ketamine — evidence map and PDF list (v0.1, 2026-10-15)

All DOIs below come from Crossref API responses retrieved on 2026-10-15 (never from memory). Each row's DOI, title, journal, year, first author and `updated-by` field (retraction/erratum check) were returned by Crossref for that record; the DOIs marked ◆ were additionally re-fetched one by one at `works/<DOI>` (see Verification block). Retraction check: none retracted; three carry published errata/corrigenda (items 17, 31, 77) and one has an unconfirmed erratum flag (item 3), all marked. Save each PDF into `PDFs/Ketamine/` with the filename given; cross-cutting papers go in `PDFs/_Cross-cutting/`.

How this list was built: (1) landmark studies and their published critiques, replies and follow-ups; (2) systematic reviews, meta-analyses, major cohorts and trials found by Crossref bibliographic search on the 18 pre-registered section-level queries and 38 targeted author/title queries (all strings in `Ketamine_search-log.md`); (3) screening by title and journal. The PubMed layer (strings in the search log) is still to be run and will add to this list; its results decide what is added or dropped, not this list.

Context note for the senior author: Crossref was heavily rate-limited during this build (shared egress; see search log), so individual `works/<DOI>` re-fetches were completed for all of Tier A; Tier B and C rows rest on the Crossref search record that returned them (same metadata source, same `updated-by` field).

**Work through the list in order. Tier A first.**

---

## Tier A — needed now (backbone reviews, landmark primaries and their critiques)

| # | Paper | Journal, year | DOI | Save as |
|---|---|---|---|---|
| 1 | Morgan & Curran (ISCD) — Ketamine use: a review ◆ | Addiction 2012 | 10.1111/j.1360-0443.2011.03576.x | Morgan_2012_KetamineUseReview.pdf |
| 2 | Peltoniemi et al. — Ketamine: a review of clinical pharmacokinetics and pharmacodynamics in anesthesia and pain therapy ◆ | Clin Pharmacokinet 2016 | 10.1007/s40262-016-0383-6 | Peltoniemi_2016_ClinicalPKPDReview.pdf |
| 3 | Zanos et al. — Ketamine and ketamine metabolite pharmacology: insights into therapeutic mechanisms ◆ (Crossref search record reports an erratum; individual re-fetch showed none — check journal correction notice) | Pharmacol Rev 2018 | 10.1124/pr.117.015198 | Zanos_2018_MetabolitePharmacologyReview.pdf |
| 4 | Clements, Nimmo & Grant — Bioavailability, pharmacokinetics, and analgesic activity of ketamine in humans ◆ | J Pharm Sci 1982 | 10.1002/jps.2600710516 | Clements_1982_BioavailabilityPK.pdf |
| 5 | Yanagihara et al. — Plasma concentration profiles of ketamine and norketamine after administration of various ketamine preparations to healthy Japanese volunteers ◆ | Biopharm Drug Dispos 2003 | 10.1002/bdd.336 | Yanagihara_2003_PKByPreparation.pdf |
| 6 | Krystal et al. — Subanesthetic effects of the noncompetitive NMDA antagonist, ketamine, in humans: psychotomimetic, perceptual, cognitive, and neuroendocrine responses ◆ | Arch Gen Psychiatry 1994 | 10.1001/archpsyc.1994.03950030035004 | Krystal_1994_SubanestheticEffectsHumans.pdf |
| 7 | Malhotra et al. — NMDA receptor function and human cognition: the effects of ketamine in healthy volunteers ◆ | Neuropsychopharmacology 1996 | 10.1016/0893-133x(95)00137-3 | Malhotra_1996_NMDAHumanCognition.pdf |
| 8 | Newcomer et al. — Ketamine-induced NMDA receptor hypofunction as a model of memory impairment and psychosis ◆ | Neuropsychopharmacology 1999 | 10.1016/s0893-133x(98)00067-0 | Newcomer_1999_NMDAHypofunctionModel.pdf |
| 9 | Vollenweider et al. — Differential psychopathology and patterns of cerebral glucose utilisation produced by (S)- and (R)-ketamine in healthy volunteers using PET ◆ | Eur Neuropsychopharmacol 1997 | 10.1016/s0924-977x(96)00042-9 | Vollenweider_1997a_SRKetaminePET.pdf |
| 10 | Vollenweider et al. — Metabolic hyperfrontality and psychopathology in the ketamine model of psychosis using PET and [18F]FDG ◆ | Eur Neuropsychopharmacol 1997 | 10.1016/s0924-977x(96)00039-9 | Vollenweider_1997b_HyperfrontalityPET.pdf |
| 11 | Lahti et al. — Subanesthetic doses of ketamine stimulate psychosis in schizophrenia ◆ | Neuropsychopharmacology 1995 | 10.1016/0893-133x(94)00131-i | Lahti_1995_KetaminePsychosisSchizophrenia.pdf |
| 12 | Ait Bentaleb et al. — A meta-analysis of functional neuroimaging studies of ketamine administration in healthy volunteers ◆ | J Psychoactive Drugs 2024 | 10.1080/02791072.2023.2190758 | AitBentaleb_2023_NeuroimagingMetaAnalysis.pdf |
| 13 | Curran & Morgan — Cognitive, dissociative and psychotogenic effects of ketamine in recreational users on the night of drug use and 3 days later ◆ | Addiction 2000 | 10.1046/j.1360-0443.2000.9545759.x | Curran_2000_RecreationalUsersNightAnd3Days.pdf |
| 14 | Curran & Monaghan — In and out of the K-hole: a comparison of the acute and residual effects of ketamine in frequent and infrequent ketamine users ◆ | Addiction 2001 | 10.1046/j.1360-0443.2001.96574910.x | Curran_2001_InAndOutOfTheKHole.pdf |
| 15 | Morgan et al. — Beyond the K-hole: a 3-year longitudinal investigation of the cognitive and subjective effects of ketamine in recreational users who have substantially reduced their use ◆ | Addiction 2004 | 10.1111/j.1360-0443.2004.00879.x | Morgan_2004a_BeyondTheKHole3Year.pdf |
| 16 | Morgan, Muetzelfeldt & Curran — Ketamine use, cognition and psychological wellbeing: a comparison of frequent, infrequent and ex-users with polydrug and non-using controls ◆ | Addiction 2009 | 10.1111/j.1360-0443.2008.02394.x | Morgan_2009_FrequentInfrequentExUsers.pdf |
| 17 | Morgan, Muetzelfeldt & Curran — Consequences of chronic ketamine self-administration upon neurocognitive function and psychological wellbeing: a 1-year longitudinal study ◆ (erratum published; obtain both) | Addiction 2010 | 10.1111/j.1360-0443.2009.02761.x | Morgan_2010_OneYearLongitudinal.pdf |
| 18 | Shahani et al. — Ketamine-associated ulcerative cystitis: a new clinical entity ◆ | Urology 2007 | 10.1016/j.urology.2007.01.038 | Shahani_2007_UlcerativeCystitisNewEntity.pdf |
| 19 | Chu et al. — The destruction of the lower urinary tract by ketamine abuse: a new syndrome? ◆ | BJU Int 2008 | 10.1111/j.1464-410x.2008.07920.x | Chu_2008_LowerUrinaryTractDestruction.pdf |
| 20 | Winstock et al. — The prevalence and natural history of urinary symptoms among recreational ketamine users ◆ | BJU Int 2012 | 10.1111/j.1464-410x.2012.11028.x | Winstock_2012_UrinarySymptomsPrevalence.pdf |
| 21 | Chan et al. — Systematic review and meta-analysis of ketamine-associated uropathy ◆ | Hong Kong Med J 2022 | 10.12809/hkmj209194 | Chan_2022_UropathySRMA.pdf |
| 22 | Schifano et al. — Trapped in the "K-hole": overview of deaths associated with ketamine misuse in the UK (1993–2006) ◆ | J Clin Psychopharmacol 2008 | 10.1097/jcp.0b013e3181612cdc | Schifano_2008_KHoleDeathsUK.pdf |
| 23 | Corkery et al. — Recreational ketamine-related deaths notified to the National Programme on Substance Abuse Deaths, England, 1997–2019 ◆ | J Psychopharmacol 2021 | 10.1177/02698811211021588 | Corkery_2021_NPSADKetamineDeaths.pdf |
| 24 | Darke et al. — Characteristics and circumstances of death related to the self-administration of ketamine ◆ | Addiction 2021 | 10.1111/add.15154 | Darke_2021_KetamineDeathsAustralia.pdf |
| 25 | Berman et al. — Antidepressant effects of ketamine in depressed patients ◆ | Biol Psychiatry 2000 | 10.1016/s0006-3223(99)00230-9 | Berman_2000_AntidepressantEffects.pdf |
| 26 | Zarate et al. — A randomized trial of an N-methyl-D-aspartate antagonist in treatment-resistant major depression ◆ | Arch Gen Psychiatry 2006 | 10.1001/archpsyc.63.8.856 | Zarate_2006_NMDAAntagonistTRDRCT.pdf |
| 27 | Daly et al. — Efficacy and safety of intranasal esketamine adjunctive to oral antidepressant therapy in treatment-resistant depression: a randomized clinical trial ◆ | JAMA Psychiatry 2018 | 10.1001/jamapsychiatry.2017.3739 | Daly_2018_IntranasalEsketamineRCT.pdf |
| 28 | Popova et al. — Efficacy and safety of flexibly dosed esketamine nasal spray combined with a newly initiated oral antidepressant in TRD (TRANSFORM-2) ◆ | Am J Psychiatry 2019 | 10.1176/appi.ajp.2019.19020172 | Popova_2019_TRANSFORM2.pdf |
| 29 | Turner — Esketamine for treatment-resistant depression: seven concerns about efficacy and FDA approval (critique) ◆ | Lancet Psychiatry 2019 | 10.1016/s2215-0366(19)30394-3 | Turner_2019_EsketamineSevenConcerns.pdf |
| 30 | Schatzberg — A word to the wise about intranasal esketamine (critique) ◆ | Am J Psychiatry 2019 | 10.1176/appi.ajp.2019.19040423 | Schatzberg_2019_WordToTheWise.pdf |
| 31 | Horowitz & Moncrieff — Are we repeating mistakes of the past? A review of the evidence for esketamine ◆ (critique; corrigendum 10.1192/bjp.2021.40 published, obtain both) | Br J Psychiatry 2021 | 10.1192/bjp.2020.89 | Horowitz_2021_RepeatingMistakesEsketamine.pdf |
| 32 | Dean et al. — Ketamine and other glutamate receptor modulators for depression in adults with unipolar major depressive disorder (Cochrane) ◆ | Cochrane Database Syst Rev 2021 | 10.1002/14651858.cd011612.pub3 | Dean_2021_CochraneUnipolar.pdf |
| 33 | Nikolin et al. — Ketamine for the treatment of major depression: a systematic review and meta-analysis ◆ | eClinicalMedicine 2023 | 10.1016/j.eclinm.2023.102127 | Nikolin_2023_DepressionSRMA.pdf |
| 34 | Short et al. — Side-effects associated with ketamine use in depression: a systematic review ◆ | Lancet Psychiatry 2018 | 10.1016/s2215-0366(17)30272-9 | Short_2018_SideEffectsSR.pdf |
| 35 | Anand et al. — Ketamine versus ECT for nonpsychotic treatment-resistant major depression (ELEKT-D) ◆ | NEJM 2023 | 10.1056/nejmoa2302399 | Anand_2023_KetamineVsECT.pdf |
| 35a | Murrough et al. — Antidepressant efficacy of ketamine in treatment-resistant major depression: a two-site randomized controlled trial ◆ | Am J Psychiatry 2013 | 10.1176/appi.ajp.2013.13030392 | Murrough_2013_TwoSiteRCT.pdf |
| 35b | Beck et al. — Association of ketamine with psychiatric symptoms and implications for its therapeutic use and for understanding schizophrenia: a systematic review and meta-analysis ◆ | JAMA Netw Open 2020 | 10.1001/jamanetworkopen.2020.4693 | Beck_2020_PsychiatricSymptomsSRMA.pdf |

## Tier B — section backbone (systematic reviews, human laboratory studies, cohorts, trials)

| # | Paper | Journal, year | DOI | Save as |
|---|---|---|---|---|
| 36 | Clements & Nimmo — Pharmacokinetics and analgesic effect of ketamine in man | Br J Anaesth 1981 | 10.1093/bja/53.1.27 | Clements_1981_PKAnalgesicMan.pdf |
| 37 | Grant, Nimmo & Clements — Pharmacokinetics and analgesic effects of i.m. and oral ketamine | Br J Anaesth 1981 | 10.1093/bja/53.8.805 | Grant_1981_IMOralPK.pdf |
| 38 | Zanos & Gould — Mechanisms of ketamine action as an antidepressant | Mol Psychiatry 2018 | 10.1038/mp.2017.255 | Zanos_2018b_MechanismsAntidepressant.pdf |
| 39 | Olney, Newcomer & Farber — NMDA receptor hypofunction model of schizophrenia | J Psychiatr Res 1999 | 10.1016/s0022-3956(99)00029-1 | Olney_1999_NMDAHypofunctionSchizophrenia.pdf |
| 40 | Lahti et al. — Effects of ketamine in normal and schizophrenic volunteers | Neuropsychopharmacology 2001 | 10.1016/s0893-133x(01)00243-3 | Lahti_2001_NormalAndSchizophrenicVolunteers.pdf |
| 41 | Adler et al. — Comparison of ketamine-induced thought disorder in healthy volunteers and thought disorder in schizophrenia | Am J Psychiatry 1999 | 10.1176/ajp.156.10.1646 | Adler_1999_ThoughtDisorder.pdf |
| 42 | Malhotra et al. — Clozapine blunts N-methyl-D-aspartate antagonist-induced psychosis: a study with ketamine | Biol Psychiatry 1997 | 10.1016/s0006-3223(96)00546-x | Malhotra_1997_ClozapineBluntsKetaminePsychosis.pdf |
| 43 | Vollenweider et al. — Effects of (S)-ketamine on striatal dopamine: a [11C]raclopride PET study of a model psychosis in humans | J Psychiatr Res 2000 | 10.1016/s0022-3956(99)00031-x | Vollenweider_2000_StriatalDopamineRaclopride.pdf |
| 44 | Parwani et al. — The effects of a subanesthetic dose of ketamine on verbal memory in normal volunteers | Psychopharmacology 2005 | 10.1007/s00213-005-0177-2 | Parwani_2005_VerbalMemory.pdf |
| 45 | Hong et al. — Gamma and delta neural oscillations and association with clinical symptoms under subanesthetic ketamine | Neuropsychopharmacology 2010 | 10.1038/npp.2009.168 | Hong_2010_GammaDeltaOscillations.pdf |
| 46 | McMillan et al. — Temporal dynamics of the pharmacological MRI response to subanaesthetic ketamine in healthy volunteers: a simultaneous EEG/fMRI study | J Psychopharmacol 2019 | 10.1177/0269881118822263 | McMillan_2019_phMRIEEG.pdf |
| 47 | Blagrove et al. — The incidence of unpleasant dreams after sub-anaesthetic ketamine | Psychopharmacology 2009 | 10.1007/s00213-008-1377-3 | Blagrove_2009_UnpleasantDreams.pdf |
| 48 | Mason, Morgan, Stefanovic & Curran — The Psychotomimetic States Inventory (PSI): measuring psychotic-type experiences from ketamine and cannabis | Schizophr Res 2008 | 10.1016/j.schres.2008.02.020 | Mason_2008_PSI.pdf |
| 49 | Muetzelfeldt et al. — Journey through the K-hole: phenomenological aspects of ketamine use | Drug Alcohol Depend 2008 | 10.1016/j.drugalcdep.2008.01.024 | Muetzelfeldt_2008_JourneyThroughTheKHole.pdf |
| 50 | Morgan & Curran — Acute and chronic effects of ketamine upon human memory: a review | Psychopharmacology 2006 | 10.1007/s00213-006-0572-3 | Morgan_2006_MemoryReview.pdf |
| 51 | Morgan, Riccelli, Maitland & Curran — Long-term effects of ketamine: evidence for a persisting impairment of source memory in recreational users | Drug Alcohol Depend 2004 | 10.1016/j.drugalcdep.2004.03.006 | Morgan_2004b_SourceMemory.pdf |
| 52 | Morgan et al. — Attentional bias to incentive stimuli in frequent ketamine users | Psychol Med 2008 | 10.1017/s0033291707002450 | Morgan_2008_AttentionalBias.pdf |
| 53 | Morgan et al. — Neurocognitive function and schizophrenia-proneness in individuals dependent on ketamine, on high-potency cannabis or on cocaine | Pharmacopsychiatry 2012 | 10.1055/s-0032-1306310 | Morgan_2012b_SchizophreniaProneness.pdf |
| 54 | Liao et al. — Frontal white matter abnormalities following chronic ketamine use: a diffusion tensor imaging study | Brain 2010 | 10.1093/brain/awq131 | Liao_2010_FrontalWhiteMatterDTI.pdf |
| 55 | Liao et al. — Reduced dorsal prefrontal gray matter after chronic ketamine use | Biol Psychiatry 2011 | 10.1016/j.biopsych.2010.08.030 | Liao_2011_PrefrontalGrayMatter.pdf |
| 56 | Roberts et al. — Abnormalities in white matter microstructure associated with chronic ketamine use | Neuropsychopharmacology 2014 | 10.1038/npp.2013.195 | Roberts_2014_WhiteMatterMicrostructure.pdf |
| 57 | Liang et al. — Striatal and white matter volumes in chronic ketamine users with or without recent regular stimulant use | Drug Alcohol Depend 2020 | 10.1016/j.drugalcdep.2020.108063 | Liang_2020_StriatalWhiteMatterVolumes.pdf |
| 58 | Narendran et al. — Altered prefrontal dopaminergic function in chronic recreational ketamine users | Am J Psychiatry 2005 | 10.1176/appi.ajp.162.12.2352 | Narendran_2005_PrefrontalDopaminergicPET.pdf |
| 59 | Jansen — A review of the nonmedical use of ketamine: use, users and consequences | J Psychoactive Drugs 2000 | 10.1080/02791072.2000.10400244 | Jansen_2000_NonmedicalUseReview.pdf |
| 60 | Critchlow — A case of ketamine dependence with discontinuation symptoms | Addiction 2006 | 10.1111/j.1360-0443.2006.01494.x | Critchlow_2006_DependenceDiscontinuation.pdf |
| 61 | Fitzgerald et al. — Test-retest reliability and cross-cultural applicability of DSM-5 adopted diagnostic criteria for ketamine use disorders | Drug Alcohol Depend 2021 | 10.1016/j.drugalcdep.2021.109056 | Fitzgerald_2021_DSM5KetamineUseDisorder.pdf |
| 62 | Weiner et al. — Ketamine abusers presenting to the emergency department: a case series | J Emerg Med 2000 | 10.1016/s0736-4679(00)00162-1 | Weiner_2000_EDCaseSeries.pdf |
| 63 | Lee et al. — A retrospective survey on the clinical presentation of ketamine abusers in a Hong Kong emergency department | Hong Kong J Emerg Med 2011 | 10.1177/102490791101800404 | Lee_2011_HongKongEDPresentation.pdf |
| 64 | Gill & Stajic — Ketamine in non-hospital and hospital deaths in New York City ◆ | J Forensic Sci 2000 | 10.1520/jfs14742j | Gill_2000_NYCDeaths.pdf |
| 65 | Lalonde & Wallage — Postmortem blood ketamine distribution in two fatalities | J Anal Toxicol 2004 | 10.1093/jat/28.1.71 | Lalonde_2004_PostmortemDistribution.pdf |
| 66 | Jhang, Hsu & Kuo — Possible pathophysiology of ketamine-related cystitis and associated treatment strategies | Int J Urol 2015 | 10.1111/iju.12841 | Jhang_2015_CystitisPathophysiology.pdf |
| 67 | Jhang et al. — Pathophysiology, clinical presentation, and management of ketamine-induced cystitis | Tzu Chi Med J 2023 | 10.4103/tcmj.tcmj_94_23 | Jhang_2023_CystitisManagement.pdf |
| 68 | Chang et al. — Ketamine-induced uropathy: a new clinical entity causing lower urinary tract symptoms | LUTS 2011 | 10.1111/j.1757-5672.2011.00101.x | Chang_2011_UropathyLUTS.pdf |
| 69 | Chen et al. — Risk factors of lower urinary tract syndrome among ketamine users | LUTS 2017 | 10.1111/luts.12178 | Chen_2017_LUTSRiskFactors.pdf |
| 70 | Chen et al. — Vascular fibrinoid necrosis in the urinary bladder of ketamine abusers: a clue to the pathogenesis of ketamine-induced vesicopathy | LUTS 2018 | 10.1111/luts.12221 | Chen_2018_FibrinoidNecrosis.pdf |
| 71 | Sihra et al. — The effects of recreational ketamine cystitis on urinary tract reconstruction: a surgical challenge | BJU Int 2018 | 10.1111/bju.14094 | Sihra_2018_UrinaryTractReconstruction.pdf |
| 72 | Hung et al. — Surgical treatment of ketamine-associated ulcerative cystitis: 8-year experience and review of series | Urol Sci 2015 | 10.1016/j.urols.2015.06.070 | Hung_2015_SurgicalTreatmentSeries.pdf |
| 73 | Schifano et al. — Is medicinal ketamine associated with urinary dysfunction issues? EMA and UK Yellow Card pharmacovigilance reports | LUTS 2020 | 10.1111/luts.12355 | Schifano_2020_MedicinalKetamineUrinaryPV.pdf |
| 74 | Diazgranados et al. — A randomized add-on trial of an N-methyl-D-aspartate antagonist in treatment-resistant bipolar depression | Arch Gen Psychiatry 2010 | 10.1001/archgenpsychiatry.2010.90 | Diazgranados_2010a_BipolarAddOnRCT.pdf |
| 75 | DiazGranados et al. — Rapid resolution of suicidal ideation after a single infusion of an N-methyl-D-aspartate antagonist in patients with TRD | J Clin Psychiatry 2010 | 10.4088/jcp.09m05327blu | Diazgranados_2010b_SuicidalIdeation.pdf |
| 76 | Wilkinson et al. — The effect of a single dose of intravenous ketamine on suicidal ideation: a systematic review and individual participant data meta-analysis | Am J Psychiatry 2018 | 10.1176/appi.ajp.2017.17040472 | Wilkinson_2018_SuicidalIdeationIPDMA.pdf |
| 77 | Bahji, Vazquez & Zarate — Comparative efficacy of racemic ketamine and esketamine for depression: a systematic review and meta-analysis (erratum published; obtain both) | J Affect Disord 2021 | 10.1016/j.jad.2020.09.071 | Bahji_2021_RacemicVsEsketamineSRMA.pdf |
| 78 | Bahji et al. — Efficacy and safety of racemic ketamine and esketamine for depression: a systematic review and meta-analysis | Expert Opin Drug Saf 2022 | 10.1080/14740338.2022.2047928 | Bahji_2022_EfficacySafetySRMA.pdf |
| 79 | Dean et al. — Ketamine and other glutamate receptor modulators for depression in adults with bipolar disorder (Cochrane) | Cochrane Database Syst Rev 2021 | 10.1002/14651858.cd011611.pub3 | Dean_2021_CochraneBipolar.pdf |
| 80 | Shafiee et al. — Ketamine versus electroconvulsive therapy for treatment-resistant depression: an updated meta-analysis of randomized clinical trials | Asian J Psychiatry 2023 | 10.1016/j.ajp.2023.103720 | Shafiee_2023_KetamineVsECTMA.pdf |
| 81 | An et al. — Intranasal ketamine for depression in adults: a systematic review and meta-analysis of randomized, double-blind, placebo-controlled trials | Front Psychol 2021 | 10.3389/fpsyg.2021.648691 | An_2021_IntranasalKetamineSRMA.pdf |
| 82 | Chen et al. — Relationship between dissociation and antidepressant effects of esketamine nasal spray in patients with TRD | Int J Neuropsychopharmacol 2022 | 10.1093/ijnp/pyab084 | Chen_2022_DissociationAndResponse.pdf |
| 83 | Morrison et al. — Effect of esketamine nasal spray on cognition in patients with TRD: results from four phase 3 studies | Int J Neuropsychopharmacol 2024 | 10.1093/ijnp/pyae046 | Morrison_2024_EsketamineCognition.pdf |
| 84 | Drevets et al. — Comment on "A word to the wise about intranasal esketamine" (reply to Schatzberg) | Am J Psychiatry 2019 | 10.1176/appi.ajp.2019.19070688 | Drevets_2019_ReplyToSchatzberg.pdf |
| 84a | Daly et al. — Efficacy of esketamine nasal spray plus oral antidepressant treatment for relapse prevention in patients with TRD (SUSTAIN-1) | JAMA Psychiatry 2019 | 10.1001/jamapsychiatry.2019.1189 | Daly_2019_SUSTAIN1RelapsePrevention.pdf |
| 85 | Li et al. — Ketamine for depression, but at what cost? A review of ketamine's neurotoxic effects from preclinical and human studies | Am J Psychiatry 2025 | 10.1176/appi.ajp.20250276 | Li_2025_NeurotoxicEffectsReview.pdf |
| 86 | Bayes et al. — Safety outcomes of ketamine for treatment-resistant depression in clinical settings and development of the Ketamine Side Effect Tool-Revised (KSET-R) | Psychiatry Res 2025 | 10.1016/j.psychres.2024.116334 | Bayes_2025_SafetyOutcomesKSETR.pdf |
| 87 | Zarate & Niciu — Ketamine for depression: evidence, challenges and promise | World Psychiatry 2015 | 10.1002/wps.20269 | Zarate_2015_EvidenceChallengesPromise.pdf |
| 88 | Zarate et al. — The development of ketamine for depression: a long and winding road from inception to implementation | Biol Psychiatry 2024 | 10.1016/j.biopsych.2024.02.122 | Zarate_2024_DevelopmentOfKetamineForDepression.pdf |
| 89 | Grabski et al. — Ketamine as a mental health treatment: are acute psychoactive effects associated with outcomes? A systematic review | Behav Brain Res 2020 | 10.1016/j.bbr.2020.112629 | Grabski_2020_AcuteEffectsAndOutcomesSR.pdf |

## Tier C — epidemiology, deaths, NPS analogues, interactions, harm reduction, policy context

| # | Paper | Journal, year | DOI | Save as |
|---|---|---|---|---|
| 90 | Dillon, Copeland & Jansen — Patterns of use and harms associated with non-medical ketamine use | Drug Alcohol Depend 2003 | 10.1016/s0376-8716(02)00243-0 | Dillon_2003_PatternsOfUseHarms.pdf |
| 91 | Copeland & Dillon — The health and psycho-social consequences of ketamine use | Int J Drug Policy 2005 | 10.1016/j.drugpo.2004.12.003 | Copeland_2005_HealthPsychosocialConsequences.pdf |
| 92 | Jansen — Non-medical use of ketamine | BMJ 1993 | 10.1136/bmj.306.6878.601 | Jansen_1993_NonMedicalUseBMJ.pdf |
| 93 | Palamar et al. — Trends in ketamine use, exposures, and seizures in the United States up to 2019 | Am J Public Health 2021 | 10.2105/ajph.2021.306486 | Palamar_2021_USTrendsTo2019.pdf |
| 94 | Palamar et al. — Trends in nonmedical ketamine use, poisonings, related deaths, pharmaceutical diversions, and law enforcement seizures (US) | Lancet Reg Health Am 2025 | 10.1016/j.lana.2025.101230 | Palamar_2025a_USTrendsDeathsDiversions.pdf |
| 95 | Palamar et al. — Trends in poisonings involving ketamine in the United States, 2019–2023 | Drug Alcohol Depend 2025 | 10.1016/j.drugalcdep.2025.112549 | Palamar_2025b_USPoisonings.pdf |
| 96 | Palamar et al. — Trends in ketamine use among nightclub attendees in New York City, 2017–2024 | Int J Drug Policy 2025 | 10.1016/j.drugpo.2025.104825 | Palamar_2025c_NYCNightclubTrends.pdf |
| 97 | Yang et al. — Trends and characteristics in ketamine use among US adults with and without depression, 2015–2022 | J Affect Disord 2025 | 10.1016/j.jad.2024.12.108 | Yang_2025_USAdultsWithWithoutDepression.pdf |
| 98 | Palamar — Tusi: a new ketamine concoction complicating the drug landscape | Am J Drug Alcohol Abuse 2023 | 10.1080/00952990.2023.2207716 | Palamar_2023_Tusi.pdf |
| 99 | Chiappini et al. — Methoxetamine-related deaths in the UK: an overview | Hum Psychopharmacol 2015 | 10.1002/hup.2422 | Chiappini_2015_MethoxetamineDeathsUK.pdf |
| 100 | Morris & Wallach — From PCP to MXE: a comprehensive review of the non-medical use of dissociative drugs | Drug Test Anal 2014 | 10.1002/dta.1620 | _Cross-cutting/Morris_2014_FromPCPToMXE.pdf |
| 101 | Dickerson et al. — Ethanol-like effects of thiopental and ketamine in healthy humans | J Psychopharmacol 2010 (online 2008) | 10.1177/0269881108098612 | Dickerson_2010_EthanolLikeEffects.pdf |
| 102 | Ma et al. — Burden of ketamine cystitis in Chinese society | Urol Sci 2015 | 10.1016/j.urols.2015.07.007 | Ma_2015_BurdenKetamineCystitisChina.pdf |
| 103 | Chang et al. — Ketamine cystitis following ketamine therapy for treatment-resistant depression: case report | BMC Psychiatry 2024 | 10.1186/s12888-023-05468-3 | Chang_2024_CystitisAfterTherapeuticUse.pdf |
| 104 | Singh et al. — Ketamine treatment for depression: opportunities for clinical innovation and ethical foresight | Lancet Psychiatry 2017 | 10.1016/s2215-0366(17)30102-5 | Singh_2017_EthicalForesight.pdf |
| 105 | Winstock et al. — Ketamine: reclassification alone will not reduce harms | BMJ 2026 | 10.1136/bmj.s222 | Winstock_2026_ReclassificationBMJ.pdf |
| 106 | Cheng et al. — Roadside detection of impairment under the influence of ketamine: impairment symptoms with reference to oral fluid and urine concentrations | Forensic Sci Int 2007 | 10.1016/j.forsciint.2006.09.001 | Cheng_2007_RoadsideImpairment.pdf |
| 107 | Lucuta et al. — Ketamine in DUID cases in the greater Cologne area | Forensic Sci Int 2024 | 10.1016/j.forsciint.2023.111905 | Lucuta_2024_DUIDCologne.pdf |

## Reports (no DOI; save the PDF of the full report)

| # | Report | Save as |
|---|---|---|
| R1 | UNODC — World Drug Report 2025 (full report; the section on ketamine/NPS in the stimulants-and-NPS booklet) | _Epidemiology/UNODC_2025_WorldDrugReport.pdf |
| R2 | EUDA — European Drug Report 2026: Trends and Developments (ketamine section) | _Epidemiology/EUDA_2026_EuropeanDrugReport.pdf |
| R3 | EUDA — Statistical Bulletin 2026 (NPS/ketamine seizures, wastewater, hospital presentations) | _Epidemiology/EUDA_2026_StatisticalBulletin_Ketamine.pdf |
| R4 | UK ACMD — Ketamine: a review of use and harm (2013) and ACMD advice on ketamine reclassification (2025) | _Epidemiology/ACMD_2013_KetamineReview.pdf; _Epidemiology/ACMD_2025_KetamineAdvice.pdf |
| R5 | UK ONS — Deaths related to drug poisoning in England and Wales (latest; ketamine table) | _Epidemiology/ONS_latest_DrugPoisoningDeaths.pdf |
| R6 | UK Home Office — Drug misuse in England and Wales, Crime Survey (latest; ketamine prevalence tables) | _Epidemiology/HomeOffice_latest_CSEW_DrugMisuse.pdf |
| R7 | SAMHSA — NSDUH 2024 detailed tables (ketamine) | _Epidemiology/SAMHSA_2024_NSDUH_DetailedTables.pdf |
| R8 | Global Drug Survey — most recent key findings report (ketamine: urinary symptoms, K-cramps) | _Epidemiology/GDS_latest_KeyFindings.pdf |
| R9 | WEDINOS — annual drug-checking report (latest; ketamine samples and 2-FDCK findings) | _Epidemiology/WEDINOS_latest_AnnualReport.pdf |
| R10 | Hong Kong Narcotics Division — Central Registry of Drug Abuse, latest report (ketamine) | _Epidemiology/HK_CRDA_latest.pdf |

## Known gaps this list does not yet cover (to come from the PubMed layer and later Crossref passes)

Human laboratory landmarks whose DOIs were not surfaced within the rate-limited Crossref window: Breier et al. 1997 (Am J Psychiatry, ketamine-induced psychosis and prefrontal activation), Deakin et al. 2008 (Arch Gen Psychiatry, pharmaco-MRI of subjective effects), Driesen et al. 2013 (Mol Psychiatry, resting hyperconnectivity), Beck et al. 2020 (JAMA Netw Open, SR/MA of ketamine-induced psychiatric symptoms), Strous et al. 2022 (Front Neuroanat, SR of brain changes in long-term use); the pivotal trials Murrough et al. 2013 (Am J Psychiatry), Fedgchin et al. 2019 (TRANSFORM-1) and Daly et al. 2019 (SUSTAIN-1, JAMA Psychiatry); Grabski et al. 2022 (Am J Psychiatry, ketamine for alcohol use disorder); Ng et al. 2010 (Hong Kong Med J, 233 ED cases). Sections with no verified source yet: pharmacokinetics by nasal/intravenous route beyond items 4–5 and 36–37; hepatobiliary harm and "K-cramps" (Wong et al. 2014, Hong Kong Med J; Seto et al. 2018); 2-fluorodeschloroketamine and other arylcyclohexylamines beyond items 99–100 (Tang et al. 2020; Zawilska 2014 on methoxetamine); driving impairment (Cheng et al. 2005, Hong Kong roadside study); pregnancy (no controlled human data identified); drug-checking purity/adulterant data (reports R9 and EUDA); interactions beyond alcohol (benzodiazepines, opioids, stimulants in deaths — covered partly by items 22–24); ketamine-assisted psychotherapy trials; Greek data (OKANA/ΕΚΤΕΠΝ).

## Verification block

- DOIs in the list: 110 (items 1–35, 35a, 35b, 36–84, 84a, 85–107). All 110 were returned by Crossref API search responses on 2026-10-15 together with title, container-title, issued year, first author and the `updated-by` field; each row's title above is the Crossref title (shortened).
- DOIs additionally re-fetched individually at `works/<DOI>` (◆): 38 attempted → 38 resolved to the intended paper: every Tier-A item (1–35, 35a, 35b) plus item 64. Two of those attempts first drew HTTP 429 and were completed with an equivalent URL spelling (case/percent-encoding) after the wait.
- Dropped: 0 (no DOI in the retained set failed to resolve or resolved to a different paper). One duplicate Crossref DOI noted for item 51 (Elsevier PII-form 10.1016/s0376-8716(04)00071-7 points to the same article); the current-form DOI is listed.
- Errata/corrections (keep, marked): item 17 (Morgan 2010, erratum 10.1111/j.1360-0443.2010.02984.x — confirmed on individual fetch), item 31 (Horowitz & Moncrieff 2021, correction 10.1192/bjp.2021.40 — confirmed), item 77 (Bahji 2021, erratum 10.1016/j.jad.2020.11.103 — from search record), item 3 (Zanos 2018 — erratum flagged in the search record but absent on individual fetch; verify on the journal site).
- Retractions: none found.
