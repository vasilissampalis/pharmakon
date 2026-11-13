# MDMA as a medicine beyond PTSD — evidence map and PDF list (v0.1, 2026-10-17)

For section 12 of the MDMA page (treatment and therapeutic research): every clinical population other than PTSD in which MDMA or MDMA-assisted therapy has been studied, the PTSD-trial analyses of other outcomes and the long-term follow-ups, the cross-indication systematic reviews with their critiques, the history of clinical use before scheduling, and the safety of MDMA given in clinical trials. Reading list only: no claims, no study cards. Nothing in this file describes doses, administration or trial arms.

How this list was built (2026-10-17, AI reader 41): (1) 23 PubMed strings run through the E-utilities interface in the app's browser (esearch + esummary; strings, hit counts and retained records in `MDMA-therapy-beyond-PTSD_search-log.md`); 1,413 hits, 941 unique records screened by title, journal and, where scope was unclear, abstract; (2) ClinicalTrials.gov API v2 (125 records with MDMA as an intervention); (3) every DOI checked with a Crossref `works/<DOI>` call in the browser in this session, reading title, journal, year, first author and `updated-by` (retractions, corrections, expressions of concern) in the same call. Registration numbers in the tables come from the PubMed records (DataBank field or abstract), not from matching titles.

Columns: **V** = verification. `CR` = Crossref `works/<DOI>` record fetched on 2026-10-17; title, journal, year and first author agree with PubMed; `updated-by` read. `CR†` = PubMed's DOI string was not registered at Crossref (HTTP 404, twice); the Crossref DOI was found by a Crossref search and then fetched with `works/<DOI>`. **PMC** = PubMed Central id from the PubMed record (no embargo date listed). Save each PDF under `PDFs/` with the path given; rows marked "already listed" are on another list and must not be saved twice.

**Two retracted papers, two expressions of concern and four corrections were found** (verification block). The retracted papers are in their own table and are never cited as evidence (METHODS §3.2).

---

## Papers already on `MDMA_DOI-LIST.md` that belong to this question (not repeated below)

| MDMA list # | Paper | Where it fits here |
|---|---|---|
| 72 | Danforth et al. 2018 — social anxiety in autistic adults, randomized pilot (Psychopharmacology) | §2, the trial report (Tier A for this question) |
| 74 | Brewerton et al. 2022 — eating-disorder symptoms in the phase 3 PTSD trial (J Psychiatr Res) | §4 and §8 (Tier A for this question) |
| 75 | Nicholas et al. 2022 — alcohol and substance use in the phase 3 PTSD trial (Drug Alcohol Depend) | §1 and §8 (Tier A for this question) |
| 73 | Ching et al. 2022 — ethnoracial differences in efficacy and safety, pooled PTSD trials (J Psychopharmacol) | §8 and §10 |
| 29 | Vizeli & Liechti 2017 — safety pharmacology of acute MDMA in healthy subjects (J Psychopharmacol) | §10, the healthy-volunteer safety backbone the trials cite |
| 82 | Passie 2018 — the early use of MDMA in psychotherapy, 1977–1985 (Drug Sci Policy Law) | §11 (Tier A for this question) |
| 25 | Mahase 2024 — three papers retracted as FDA rejects the PTSD application (BMJ news) | §8 and the retracted table: the three retractions are now all identified (R-1 to R-4 below, with the main list's R-3/R-4) |
| R-3, R-4 | Mithoefer et al. 2019 (retracted) and its retraction note | Retracted table: the third of the three retractions |

---

## 1. Alcohol use disorder and other substance use disorders

#### Tier A

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 1 | Sessa et al. — First study of safety and tolerability of 3,4-methylenedioxymethamphetamine-assisted psychotherapy in patients with alcohol use disorder (open-label, Bristol) | J Psychopharmacol 2021 | 10.1177/0269881121991792 | 33601929 | — | CR | MDMA/Sessa_2021_AUDSafetyTolerability.pdf |
| 2 | Thurgur et al. — MDMA-assisted psychotherapy for AUD: Bayesian analysis of WHO drinking risk level and exploratory analysis of drinking behavior and psychosocial functioning at 3 months follow-up (registration NCT04158778) | Alcohol Alcohol 2025 | 10.1093/alcalc/agaf031 | 40492610 | PMC12148347 | CR | MDMA/Thurgur_2025_AUDBayesianDrinkingRisk.pdf |

#### Tier B

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 3 | Sessa et al. — Debunking the myth of 'Blue Mondays': no evidence of affect drop after taking clinical MDMA | J Psychopharmacol 2022 | 10.1177/02698811211055809 | 34894842 | — | CR | MDMA/Sessa_2022_BlueMondays.pdf |
| 4 | Piper et al. — Psychedelic-assisted treatment for substance use disorder: a narrative systematic review | Addiction 2025 | 10.1111/add.16762 | 39887551 | — | CR | MDMA/Piper_2025_PsychedelicSUDNarrativeSR.pdf |
| 5 | Wittenkeller et al. — Psychedelics as pharmacotherapeutics for substance use disorders: a scoping review on clinical trials and perspectives on underlying neurobiology | Br J Pharmacol 2026 | 10.1111/bph.70181 | 40891276 | — | CR | MDMA/Wittenkeller_2026_PsychedelicsSUDScopingReview.pdf |

#### Tier C

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 6 | Sessa — Why MDMA therapy for alcohol use disorder? And why now? | Neuropharmacology 2018 | 10.1016/j.neuropharm.2017.11.004 | 29126911 | — | CR | MDMA/Sessa_2018_WhyMDMAForAUD.pdf |
| 7 | Gully et al. — Treating posttraumatic stress disorder and alcohol use disorder comorbidity: current pharmacological therapies and the future of MDMA-integrated psychotherapy | J Psychopharmacol 2023 | 10.1177/02698811231200880 | 38009477 | PMC11549959 | CR | MDMA/Gully_2023_PTSDAUDComorbidityReview.pdf |
| 8 | Eaton et al. — Design and methodology of the first open-label trial of MDMA-assisted therapy for veterans with PTSD and alcohol use disorder (protocol; NCT05943665) | Contemp Clin Trials Commun 2024 | 10.1016/j.conctc.2024.101333 | 39262902 | PMC11387902 | CR | MDMA/Eaton_2024_VeteransPTSDAUDProtocol.pdf |
| 9 | Morley et al. — MDMA-assisted PTSD and Alcohol Therapy Trial (MPATHY): study protocol for a double-blind, randomised, controlled outpatient trial (NCT05709353) | BMJ Open 2026 | 10.1136/bmjopen-2025-114896 | 42409408 | PMC13343076 | CR | MDMA/Morley_2026_MPATHYProtocol.pdf |
| 10 | Jerome et al. — Can MDMA play a role in the treatment of substance abuse? | Curr Drug Abuse Rev 2013 | 10.2174/18744737112059990005 | 23627786 | — | CR | MDMA/Jerome_2013_MDMAInSubstanceUseTreatment.pdf |
| 11 | Srivastava & Gold — A tragedy of errors: the state of psychedelic research in the treatment of alcohol use disorder (critique) | Brain Sci 2025 | 10.3390/brainsci15111190 | 41300197 | PMC12650486 | CR | MDMA/Srivastava_2025_TragedyOfErrorsAUD.pdf |
| 12 | Roberts — Hype or hope? The developing evidence base for psychedelic treatment of addiction disorders (editorial) | Br J Psychiatry 2025 | 10.1192/bjp.2025.19 | 40114513 | — | CR | MDMA/Roberts_2025_HypeOrHopeAddiction.pdf |

## 2. Social anxiety in autistic adults; social anxiety disorder

The trial report itself (Danforth et al. 2018) is on the MDMA list (#72).

#### Tier B

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 13 | Danforth et al. — MDMA-assisted therapy: a new treatment model for social anxiety in autistic adults (rationale and design; NCT02008396) | Prog Neuropsychopharmacol Biol Psychiatry 2016 | 10.1016/j.pnpbp.2015.03.011 | 25818246 | — | CR | MDMA/Danforth_2016_SocialAnxietyAutisticAdultsModel.pdf |
| 14 | Chaliha et al. — A systematic review of the MDMA model to address social impairment in autism | Curr Neuropharmacol 2021 | 10.2174/1570159x19666210101130258 | 33388021 | PMC8686313 | CR | MDMA/Chaliha_2021_MDMAAutismSR.pdf |

#### Tier C

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 15 | Lear et al. — Social anxiety and MDMA-assisted therapy investigation: a novel clinical trial protocol (social anxiety disorder; NCT05138068) | Front Psychiatry 2023 | 10.3389/fpsyt.2023.1083354 | 37520237 | PMC10379654 | CR | MDMA/Lear_2023_SAMATIProtocol.pdf |
| 16 | Luoma & Lear — MDMA-assisted therapy as a means to alter affective, cognitive, behavioral, and neurological systems underlying social dysfunction in social anxiety disorder | Front Psychiatry 2021 | 10.3389/fpsyt.2021.733893 | 34646176 | PMC8502812 | CR | MDMA/Luoma_2021_SocialAnxietyDisorderSystems.pdf |
| 17 | Luoma et al. — Potential processes of change in MDMA-assisted therapy for social anxiety disorder | Hum Psychopharmacol 2022 | 10.1002/hup.2824 | 34739165 | PMC9285360 | CR | MDMA/Luoma_2022_ProcessesOfChangeSAD.pdf |
| 18 | Danforth — Psychedelic-assisted therapy for social adaptability in autistic adults (book chapter) | Curr Top Behav Neurosci 2022 (online 2021) | 10.1007/7854_2021_269 | 34761363 | — | CR | MDMA/Danforth_2022_SocialAdaptabilityAutisticAdults.pdf |
| 19 | Claudino dos Santos et al. — Psychedelics and autism spectrum disorder: mechanistic insights, translational evidence and ethical challenges | J Psychiatr Res 2026 | 10.1016/j.jpsychires.2026.06.035 | 42385294 | — | CR | MDMA/ClaudinoDosSantos_2026_PsychedelicsAutismReview.pdf |

## 3. Anxiety and distress with a life-threatening illness

#### Tier A

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 20 | Wolfson et al. — MDMA-assisted psychotherapy for treatment of anxiety and other psychological distress related to life-threatening illnesses: a randomized pilot study (NCT02427568) | Sci Rep 2020 | 10.1038/s41598-020-75706-1 | 33235285 | PMC7686344 | CR | MDMA/Wolfson_2020_LifeThreateningIllnessRCT.pdf |
| 21 | Schipper et al. — Psychedelic-assisted therapy for treating anxiety, depression, and existential distress in people with life-threatening diseases (Cochrane review, pub2) | Cochrane Database Syst Rev 2024 | 10.1002/14651858.cd015383.pub2 | 39260823 | PMC11390284 | CR | already listed (LSD list): LSD/Schipper_2024_CochranePsychedelicAssisted.pdf |

#### Tier B

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 22 | Barone et al. — Facing death, returning to life: a qualitative analysis of MDMA-assisted therapy for anxiety associated with life-threatening illness | Front Psychiatry 2022 | 10.3389/fpsyt.2022.944849 | 36238946 | PMC9552520 | CR | MDMA/Barone_2022_FacingDeathQualitative.pdf |
| 23 | Schimmers et al. — Psychedelics for the treatment of depression, anxiety, and existential distress in patients with a terminal illness: a systematic review (**correction published; obtain both**) | Psychopharmacology 2022 | 10.1007/s00213-021-06027-y | 34812901 | — | CR | MDMA/Schimmers_2022_TerminalIllnessSR.pdf |
| 24 | Schimmers et al. — Correction to: Psychedelics for the treatment of depression, anxiety, and existential distress in patients with a terminal illness | Psychopharmacology 2023 | 10.1007/s00213-023-06406-7 | — | — | CR | MDMA/Schimmers_2023_Correction.pdf |
| 25 | Schuman et al. — Psychedelic-assisted therapies for psychosocial symptoms in cancer: a systematic review and meta-analysis | Curr Oncol 2025 | 10.3390/curroncol32070380 | 40710191 | PMC12293737 | CR | MDMA/Schuman_2025_CancerPsychosocialSRMA.pdf |

#### Tier C

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 26 | Bhagavan et al. — Effect of MDMA-assisted therapy on mood and anxiety symptoms in advanced-stage cancer (EMMAC): study protocol for a double-blind, randomised controlled trial (ACTRN12619001334190) | Trials 2024 | 10.1186/s13063-024-08174-x | 38773523 | PMC11110200 | CR | MDMA/Bhagavan_2024_EMMACProtocol.pdf |
| 27 | Jing et al. — Psychedelic medicines for end-of-life care: pipeline clinical trial review 2022 | Palliat Support Care 2023 | 10.1017/s147895152300069x | 37334486 | — | CR | MDMA/Jing_2023_EndOfLifePipelineReview.pdf |

## 4. Eating disorders

No trial in a primary eating-disorder population has been published; the one controlled dataset is the PTSD-trial secondary analysis (Brewerton et al. 2022, MDMA list #74). Registered trials: §12 below.

#### Tier B

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 28 | Harkhoe et al. — Exploring MDMA assisted therapy in eating disorders: mechanisms, clinical evidence, and future directions | J Eat Disord 2025 | 10.1186/s40337-025-01409-5 | 41466432 | PMC12751933 | CR | MDMA/Harkhoe_2025_MDMAEatingDisordersReview.pdf |

#### Tier C

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 29 | Brewerton et al. — The potential use of N-methyl-3,4-methylenedioxyamphetamine (MDMA) assisted psychotherapy in the treatment of eating disorders comorbid with PTSD (hypothesis paper) | Med Hypotheses 2021 | 10.1016/j.mehy.2020.110367 | 33203569 | — | CR | MDMA/Brewerton_2021_EatingDisordersComorbidPTSD.pdf |
| 30 | Calder et al. — Psychedelics in the treatment of eating disorders: rationale and potential mechanisms | Eur Neuropsychopharmacol 2023 | 10.1016/j.euroneuro.2023.05.008 | 37352816 | — | CR | MDMA/Calder_2023_PsychedelicsEatingDisorders.pdf |
| 31 | van Beers et al. — Biological treatments for co-occurring eating disorders and psychological trauma: a systematic review | Front Psychiatry 2025 | 10.3389/fpsyt.2025.1523269 | 40104330 | PMC11914888 | CR | MDMA/vanBeers_2025_EatingDisordersTraumaSR.pdf |

## 5. Couples and relationship (conjoint) therapy

All published conjoint trials enrolled dyads in which one partner has PTSD; they are listed here because the intervention and the relational outcomes are the point.

#### Tier A

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 32 | Monson et al. — MDMA-facilitated cognitive-behavioural conjoint therapy for posttraumatic stress disorder: an uncontrolled trial | Eur J Psychotraumatol 2020 | 10.1080/20008198.2020.1840123 | 33408811 | PMC7748057 | CR | MDMA/Monson_2020_MDMACBCTUncontrolledTrial.pdf |
| 33 | Wagner et al. — Relational and growth outcomes following couples therapy with MDMA for PTSD | Front Psychiatry 2021 | 10.3389/fpsyt.2021.702838 | 34262496 | PMC8273271 | CR | MDMA/Wagner_2021a_CouplesRelationalOutcomes.pdf |
| 34 | Morland et al. — Healing together: results from a pilot trial of 3,4-methylenedioxymethamphetamine-enhanced cognitive-behavioral conjoint therapy for posttraumatic stress disorder | J Trauma Stress 2026 | 10.1002/jts.70126 | 42693902 | — | CR | MDMA/Morland_2026_HealingTogetherPilot.pdf |

#### Tier C

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 35 | Morland et al. — MDMA-assisted brief cognitive behavioral conjoint therapy for PTSD: study protocol for a pilot study (NCT05979844) | Contemp Clin Trials Commun 2024 | 10.1016/j.conctc.2024.101314 | 38994348 | PMC11237689 | CR | MDMA/Morland_2024_BriefCBCTProtocol.pdf |
| 36 | Wagner — Couple therapy with MDMA: proposed pathways of action | Front Psychol 2021 | 10.3389/fpsyg.2021.733456 | 34858270 | PMC8631777 | CR | MDMA/Wagner_2021b_CoupleTherapyPathways.pdf |

## 6. Depression

#### Tier A

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 37 | Kvam et al. — MDMA-assisted therapy as a treatment for major depressive disorder: proof of principle study (open-label; EudraCT 2021-000805-26; **corrigendum published; obtain both**) | Br J Psychiatry 2025 | 10.1192/bjp.2025.10320 | 40641116 | PMC12550655 | CR | MDMA/Kvam_2025_MDDProofOfPrinciple.pdf |
| 38 | Kvam et al. — MDMA-assisted therapy as a treatment for major depressive disorder: proof of principle study — CORRIGENDUM | Br J Psychiatry 2026 | 10.1192/bjp.2026.10579 | 41664469 | PMC13051208 | CR | MDMA/Kvam_2026a_Corrigendum.pdf |
| 39 | Kvam et al. — MDMA-assisted therapy for major depressive disorder: a seven-month follow-up proof of principle trial | J Psychiatr Res 2026 | 10.1016/j.jpsychires.2025.11.030 | 41344230 | — | CR | MDMA/Kvam_2026b_SevenMonthFollowUp.pdf |
| 40 | Ai et al. — MDMA-assisted psychotherapy in major depression: critical considerations for clinical translation (commentary on item 37) | Br J Psychiatry 2026 | 10.1192/bjp.2025.10474 | 41367211 | — | CR | MDMA/Ai_2026_MDDCriticalConsiderations.pdf |
| 41 | Kvam et al. — MDMA-assisted psychotherapy in major depression: critical considerations for clinical translation (authors' commentary in reply) | Br J Psychiatry 2026 | 10.1192/bjp.2026.10551 | 41787762 | — | CR | MDMA/Kvam_2026c_ReplyCommentary.pdf |
| 42 | Hsu et al. — Comparative oral monotherapy of psilocybin, LSD, MDMA, ayahuasca, and escitalopram for depressive symptoms: systematic review and Bayesian network meta-analysis | BMJ 2024 | 10.1136/bmj-2023-078607 | 39168500 | PMC11337322 | CR | MDMA/Hsu_2024_DepressionNetworkMetaAnalysis.pdf |

#### Tier C

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 43 | Kvam et al. — Study protocol for "MDMA-assisted therapy as a treatment for major depressive disorder: a proof of principle study" | Front Psychiatry 2022 | 10.3389/fpsyt.2022.954388 | 36386973 | PMC9645093 | CR | MDMA/Kvam_2022_MDDProtocol.pdf |
| 44 | Patel & Titheradge — MDMA for the treatment of mood disorder: all talk no substance? | Ther Adv Psychopharmacol 2015 | 10.1177/2045125315583786 | 26199721 | PMC4502590 | CR | MDMA/Patel_2015_MoodDisorderAllTalk.pdf |
| 45 | Riedlinger & Riedlinger — Psychedelic and entactogenic drugs in the treatment of depression | J Psychoactive Drugs 1994 | 10.1080/02791072.1994.10472600 | 7913128 | — | CR | MDMA/Riedlinger_1994_EntactogensDepression.pdf |

## 7. Other clinical populations

Tinnitus (one proof-of-principle trial); arginine vasopressin deficiency (MDMA as a diagnostic stimulation test, not a treatment); the Swiss limited medical use programme (mixed indications); and conditions with registered trials or proposals but no published trial (obsessive-compulsive disorder, chronic neuropathic pain, fibromyalgia, borderline personality disorder, schizophrenia, pathological narcissism, specific phobia, prolonged grief, moral injury, sexual dysfunction, older adults).

#### Tier A

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 46 | Searchfield et al. — A proof-of-principle study of the short-term effects of 3,4-methylenedioxymethamphetamine (MDMA) on tinnitus and neural connectivity (randomized, double-blind, placebo-controlled crossover) | Int J Neurosci 2020 | 10.1080/00207454.2019.1702544 | 31814488 | — | CR | MDMA/Searchfield_2020_TinnitusProofOfPrinciple.pdf |

#### Tier B

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 47 | Atila et al. — Oxytocin in response to MDMA provocation test in patients with arginine vasopressin deficiency (central diabetes insipidus): a single-centre, case-control study with nested, randomised, double-blind, placebo-controlled crossover trial (NCT04648137) | Lancet Diabetes Endocrinol 2023 | 10.1016/s2213-8587(23)00120-1 | 37192642 | — | CR | MDMA/Atila_2023_AVPDeficiencyProvocationTest.pdf |
| 48 | Liechti et al. — Implementing psychedelic-assisted therapy: history and characteristics of the Swiss limited medical use program | Neurosci Appl 2025 | 10.1016/j.nsa.2025.105525 | 40800003 | PMC12341733 | CR | MDMA/Liechti_2025_SwissLimitedMedicalUse.pdf |
| 49 | Oehen & Gasser — Using a MDMA- and LSD-group therapy model in clinical practice in Switzerland and highlighting the treatment of trauma-related disorders | Front Psychiatry 2022 | 10.3389/fpsyt.2022.863552 | 35546928 | PMC9082273 | CR | MDMA/Oehen_2022_SwissGroupTherapyModel.pdf |
| 50 | Schmid et al. — Acute subjective effects in LSD- and MDMA-assisted psychotherapy (patients treated in Switzerland) | J Psychopharmacol 2021 | 10.1177/0269881120959604 | 33853422 | — | CR | MDMA/Schmid_2021_SwissPatientsAcuteEffects.pdf |
| 51 | Saade & Keuroghlian — Transdiagnostic use of 3,4-methylenedioxymethamphetamine-assisted therapy to treat obsessive-compulsive disorder | Br J Psychiatry 2025 | 10.1192/bjp.2024.277 | 40001303 | — | CR | MDMA/Saade_2025_MDMAOCD.pdf |

#### Tier C

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 52 | Brakoulias & Rossell — commentary on item 51 (MDMA-assisted therapy for OCD) | Br J Psychiatry 2025 | 10.1192/bjp.2025.76 | 40685910 | — | CR | MDMA/Brakoulias_2025_OCDCommentary.pdf |
| 53 | Lu et al. — Prospective preference assessment for the Ecstasy for Alleviating Severe Chronic Neuropathic Pain (EASE-Pain) trial | Can J Anaesth 2025 | 10.1007/s12630-025-03031-0 | 40750953 | — | CR | MDMA/Lu_2025_EASEPainPreference.pdf |
| 54 | Kasiviswanathan et al. — Making a case for using MDMA-assisted psychotherapy for borderline personality disorder and complex PTSD: a descriptive systematic review of the literature | Ther Adv Psychopharmacol 2026 | 10.1177/20451253251408626 | 42422592 | PMC13342383 | CR | MDMA/Kasiviswanathan_2026_BPDComplexPTSDReview.pdf |
| 55 | Traynor et al. — MDMA-assisted psychotherapy for borderline personality disorder | Focus (Am Psychiatr Publ) 2022 | 10.1176/appi.focus.20220056 | 37200873 | PMC10187385 | CR | MDMA/Traynor_2022_MDMABorderlinePD.pdf |
| 56 | Arnovitz et al. — MDMA for the treatment of negative symptoms in schizophrenia | J Clin Med 2022 | 10.3390/jcm11123255 | 35743326 | PMC9225098 | CR | MDMA/Arnovitz_2022_SchizophreniaNegativeSymptoms.pdf |
| 57 | Albert & Back — Psychoanalytically informed MDMA-assisted therapy for pathological narcissism: a novel theoretical approach | Front Psychiatry 2025 | 10.3389/fpsyt.2025.1529427 | 40256160 | PMC12006724 | CR | MDMA/Albert_2025_PathologicalNarcissism.pdf |
| 58 | Ahari & Fonzo — A biopsychosocial model of MDMA-assisted therapy in application: dyadic one session treatment for specific phobia | Front Psychiatry 2025 | 10.3389/fpsyt.2025.1665770 | 40980037 | PMC12446348 | CR | MDMA/Ahari_2025_SpecificPhobiaDyadic.pdf |
| 59 | Ehrenkranz et al. — Narrative review of the potential for psychedelics to treat prolonged grief disorder | Int Rev Psychiatry 2024 | 10.1080/09540261.2024.2357668 | 39980217 | — | CR | MDMA/Ehrenkranz_2024_ProlongedGriefReview.pdf |
| 60 | Kurkova et al. — Exploring the potential of psychedelic-assisted psychotherapy for moral injury: a scoping review | Prog Neuropsychopharmacol Biol Psychiatry 2025 | 10.1016/j.pnpbp.2025.111333 | 40113127 | — | CR | MDMA/Kurkova_2025_MoralInjuryScopingReview.pdf |
| 61 | Wexler et al. — Does MDMA have treatment potential in sexual dysfunction? A systematic review of outcomes across the female and male sexual response cycles | Sex Med Rev 2023 | 10.1093/sxmrev/qead046 | 37888490 | — | CR | MDMA/Wexler_2023_SexualDysfunctionSR.pdf |
| 62 | Johnston et al. — The safety and efficacy of psychedelic-assisted therapies for older adults: knowns and unknowns | Am J Geriatr Psychiatry 2023 | 10.1016/j.jagp.2022.08.007 | 36184377 | — | CR | MDMA/Johnston_2023_OlderAdults.pdf |
| 63 | Bouchet et al. — Older adults in psychedelic-assisted therapy trials: a systematic review | J Psychopharmacol 2024 | 10.1177/02698811231215420 | 38240068 | — | CR | MDMA/Bouchet_2024_OlderAdultsTrialsSR.pdf |
| 64 | Beichmann et al. — Psychedelic-assisted therapy: a survey on the clinical methods of Swiss physicians | Ther Adv Psychopharmacol 2026 | 10.1177/20451253261448745 | 42179908 | PMC13191117 | CR | MDMA/Beichmann_2026_SwissPhysiciansSurvey.pdf |
| 65 | Gasser — Psychedelic group therapy (book chapter) | Curr Top Behav Neurosci 2022 (online 2021) | 10.1007/7854_2021_268 | 35091980 | — | CR | MDMA/Gasser_2022_PsychedelicGroupTherapy.pdf |

## 8. PTSD trials: analyses of other outcomes, and long-term follow-up

On the MDMA list already: Brewerton 2022 (#74, eating-disorder symptoms), Nicholas 2022 (#75, alcohol and substance use), Ching 2022 (#73). The pooled long-term follow-up of the phase 2 trials (Jerome et al. 2020) is **retracted** (table below). **Two of the other-outcome analyses carry expressions of concern** (items 67 and 70).

#### Tier A

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 66 | Mithoefer et al. — Durability of improvement in post-traumatic stress disorder symptoms and absence of harmful effects or drug dependency after 3,4-methylenedioxymethamphetamine-assisted psychotherapy: a prospective long-term follow-up study | J Psychopharmacol 2013 | 10.1177/0269881112456611 | 23172889 | PMC3573678 | CR | MDMA/Mithoefer_2013_LongTermFollowUp.pdf |
| 67 | Ponte et al. — Sleep quality improvements after MDMA-assisted psychotherapy for the treatment of posttraumatic stress disorder (**expression of concern and correction published 2024–2025; obtain all three**) | J Trauma Stress 2021 | 10.1002/jts.22696 | 34114250 | PMC8453707 | CR | MDMA/Ponte_2021_SleepQuality.pdf |
| 68 | Expression of Concern: Sleep quality improvements after MDMA-assisted psychotherapy for the treatment of posttraumatic stress disorder | J Trauma Stress 2025 (online 2024) | 10.1002/jts.23117 | 39627875 | PMC12416979 | CR | MDMA/JTS_2025_ExpressionOfConcern_Ponte.pdf |
| 69 | Correction to Sleep quality improvements after MDMA-assisted psychotherapy for the treatment of posttraumatic stress disorder | J Trauma Stress 2025 (online 2024) | 10.1002/jts.23098 | — | — | CR | MDMA/JTS_2025_Correction_Ponte.pdf |

#### Tier B

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 70 | Gorman et al. — Posttraumatic growth after MDMA-assisted psychotherapy for posttraumatic stress disorder (**expression of concern and correction published 2024–2025; obtain all three**) | J Trauma Stress 2020 | 10.1002/jts.22479 | 32073177 | PMC7216948 | CR | MDMA/Gorman_2020_PosttraumaticGrowth.pdf |
| 71 | Expression of Concern: Posttraumatic growth after MDMA-assisted psychotherapy for posttraumatic stress disorder | J Trauma Stress 2025 (online 2024) | 10.1002/jts.23116 | 39627911 | PMC12416983 | CR | MDMA/JTS_2025_ExpressionOfConcern_Gorman.pdf |
| 72 | Correction to Posttraumatic growth after MDMA-assisted psychotherapy for posttraumatic stress disorder | J Trauma Stress 2025 (online 2024) | 10.1002/jts.23097 | — | — | CR | MDMA/JTS_2025_Correction_Gorman.pdf |
| 73 | Christie et al. — MDMA-assisted therapy is associated with a reduction in chronic pain among people with post-traumatic stress disorder (NCT03282123) | Front Psychiatry 2022 | 10.3389/fpsyt.2022.939302 | 36405923 | PMC9669702 | CR | MDMA/Christie_2022_ChronicPain.pdf |
| 74 | Agin-Liebes et al. — Self-compassion mediates treatment effects in MDMA-assisted therapy for posttraumatic stress disorder | Eur J Psychotraumatol 2025 | 10.1080/20008066.2025.2485513 | 40331914 | PMC12064107 | CR | MDMA/AginLiebes_2025_SelfCompassion.pdf |
| 75 | van der Kolk et al. — Effects of MDMA-assisted therapy for PTSD on self-experience (NCT03537014) | PLoS One 2024 | 10.1371/journal.pone.0295926 | 38198456 | PMC10781106 | CR | MDMA/vanderKolk_2024_SelfExperience.pdf |
| 76 | Wagner et al. — Therapeutic effect of increased openness: investigating mechanism of action in MDMA-assisted psychotherapy | J Psychopharmacol 2017 | 10.1177/0269881117711712 | 28635375 | PMC5544120 | CR | MDMA/Wagner_2017_IncreasedOpenness.pdf |
| 77 | Green et al. — MDMA-assisted therapy may decrease PTSD symptoms, dissociation, depression, and functional disability: a systematic review and meta-analysis | Harv Rev Psychiatry 2026 | 10.1097/hrp.0000000000000478 | 42708350 | — | CR | MDMA/Green_2026_SecondaryOutcomesSRMA.pdf |
| 78 | Tabaac et al. — MDMA-assisted psychotherapy phase 3 trial publication retractions (commentary documenting the 2024 retractions) | Am J Ther 2025 | 10.1097/mjt.0000000000001847 | 40208968 | — | CR | MDMA/Tabaac_2025_PublicationRetractions.pdf |

#### Tier C

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 79 | Zeifman et al. — Preliminary evidence for the importance of therapeutic alliance in MDMA-assisted psychotherapy for posttraumatic stress disorder (NCT00090064) | Eur J Psychotraumatol 2024 | 10.1080/20008066.2023.2297536 | 38174611 | PMC10769553 | CR | MDMA/Zeifman_2024_TherapeuticAlliance.pdf |
| 80 | Bostoen et al. — The occurrence and potential role of mystical experiences in MDMA-assisted therapy for PTSD: a secondary analysis | J Psychopharmacol 2026 | 10.1177/02698811261464502 | 42563131 | — | CR | MDMA/Bostoen_2026_MysticalExperiences.pdf |
| 81 | Lewis et al. — Pilot study suggests DNA methylation of the glucocorticoid receptor gene (NR3C1) is associated with MDMA-assisted therapy treatment response for severe PTSD (NCT03537014) | Front Psychiatry 2023 | 10.3389/fpsyt.2023.959590 | 36815187 | PMC9939628 | CR | MDMA/Lewis_2023_NR3C1Methylation.pdf |
| 82 | Kachmarik et al. — Inflammatory biomarker outcomes associated with MDMA-assisted therapy: an open-label exploratory study (NCT05961527) | Front Neurosci 2026 | 10.3389/fnins.2026.1716817 | 41947855 | PMC13050828 | CR | MDMA/Kachmarik_2026_InflammatoryBiomarkers.pdf |
| 83 | Barone et al. — Perceived benefits of MDMA-assisted psychotherapy beyond symptom reduction: qualitative follow-up study of a clinical trial for individuals with treatment-resistant PTSD | J Psychoactive Drugs 2019 | 10.1080/02791072.2019.1580805 | 30849288 | — | CR | MDMA/Barone_2019_BeyondSymptomReduction.pdf |

## 9. Systematic reviews and meta-analyses across indications, and their critiques

#### Tier A

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 84 | Højlund et al. — Efficacy, all-cause discontinuation, and safety of serotonergic psychedelics and MDMA to treat mental disorders: a living systematic review with meta-analysis | Eur Neuropsychopharmacol 2025 | 10.1016/j.euroneuro.2025.09.011 | 41205366 | — | CR | MDMA/Hojlund_2025_LivingSRMA.pdf |
| 85 | Kisely et al. — A systematic literature review and meta-analysis of the effect of psilocybin and methylenedioxymethamphetamine on mental, behavioural or developmental disorders | Aust N Z J Psychiatry 2023 | 10.1177/00048674221083868 | 35285280 | — | CR | MDMA/Kisely_2023_PsilocybinMDMASRMA.pdf |
| 86 | Yao et al. — Efficacy and safety of psychedelics for the treatment of mental disorders: a systematic review and meta-analysis | Psychiatry Res 2024 | 10.1016/j.psychres.2024.115886 | 38574699 | — | CR | MDMA/Yao_2024_PsychedelicsMentalDisordersSRMA.pdf |
| 87 | Humphreys et al. — Therapeutic potential of psychedelic drugs: navigating high hopes, strong claims, weak evidence, and big money (critical review) | Annu Rev Psychol 2025 | 10.1146/annurev-psych-020124-023532 | 39094057 | PMC11890197 | CR | MDMA/Humphreys_2025_HighHopesWeakEvidence.pdf |
| 88 | Parrott — The potential dangers of using MDMA for psychotherapy (critique) | J Psychoactive Drugs 2014 | 10.1080/02791072.2014.873690 | 24830184 | — | CR | MDMA/Parrott_2014a_DangersOfMDMAPsychotherapy.pdf |
| 89 | Orsini et al. — Blinding integrity in psychedelic randomized clinical trials: a systematic review (includes 11 MDMA RCTs) | JAMA Psychiatry 2026 | 10.1001/jamapsychiatry.2026.0255 | 41984443 | — | CR | MDMA/Orsini_2026_BlindingIntegritySR.pdf |
| 90 | Muthukumaraswamy et al. — Blinding and expectancy confounds in psychedelic randomized controlled trials (abstract does not name MDMA; confirm scope on reading) | Expert Rev Clin Pharmacol 2021 | 10.1080/17512433.2021.1933434 | 34038314 | — | CR | already listed (LSD and Psilocybin lists): _Cross-cutting/Muthukumaraswamy_2021_BlindingExpectancyConfounds.pdf |
| 91 | Szigeti et al. — Too big to fail? Comparing effect sizes of MDMA assisted therapy to unmasking bias (letter) | Psychopharmacology 2026 | 10.1007/s00213-025-06886-9 | 40906191 | — | CR | MDMA/Szigeti_2026_TooBigToFail.pdf |

#### Tier B

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 92 | Luoma et al. — A meta-analysis of placebo-controlled trials of psychedelic-assisted therapy | J Psychoactive Drugs 2020 | 10.1080/02791072.2020.1769878 | 32529966 | PMC7736164 | CR | MDMA/Luoma_2020_PlaceboControlledMA.pdf |
| 93 | Dominiak et al. — Efficacy and safety of psychedelics in mental disorder cases: an umbrella review of meta-analyses of randomized controlled trials | J Clin Med 2025 | 10.3390/jcm15010253 | 41517502 | PMC12786876 | CR | MDMA/Dominiak_2025_UmbrellaReview.pdf |
| 94 | Bahji et al. — Efficacy and safety of four psychedelic-assisted therapies for adults with symptoms of depression, anxiety, and posttraumatic stress disorder: a systematic review and meta-analysis | J Psychoactive Drugs 2025 (online 2023) | 10.1080/02791072.2023.2278586 | 37968944 | PMC12129050 | CR | MDMA/Bahji_2025_FourPsychedelicTherapiesSRMA.pdf |
| 95 | Li et al. — The association between study design and antidepressant effects in psychedelic-assisted therapy: a meta-analysis | J Affect Disord 2025 | 10.1016/j.jad.2024.10.016 | 39389119 | — | CR | MDMA/Li_2025_StudyDesignAntidepressantEffects.pdf |
| 96 | Wolfgang et al. — MDMA and MDMA-assisted therapy (review) | Am J Psychiatry 2025 | 10.1176/appi.ajp.20230681 | 39741438 | — | CR | MDMA/Wolfgang_2025_MDMAAssistedTherapyReview.pdf |
| 97 | Sessa et al. — A review of 3,4-methylenedioxymethamphetamine (MDMA)-assisted psychotherapy | Front Psychiatry 2019 | 10.3389/fpsyt.2019.00138 | 30949077 | PMC6435835 | CR | MDMA/Sessa_2019_MDMAATReview.pdf |
| 98 | Mithoefer et al. — Novel psychopharmacological therapies for psychiatric disorders: psilocybin and MDMA | Lancet Psychiatry 2016 | 10.1016/s2215-0366(15)00576-3 | 27067625 | — | CR | MDMA/Mithoefer_2016_PsilocybinMDMANovelTherapies.pdf |
| 99 | Parrott — The psychotherapeutic potential of MDMA (3,4-methylenedioxymethamphetamine): an evidence-based review | Psychopharmacology 2007 | 10.1007/s00213-007-0703-5 | 17297639 | — | CR | MDMA/Parrott_2007_PsychotherapeuticPotential.pdf |
| 100 | Jacobs et al. — Psychedelic medicine: mechanisms, evidence, and translation to practice | BMJ 2026 | 10.1136/bmj-2024-081723 | 41730563 | — | CR | MDMA/Jacobs_2026_PsychedelicMedicineBMJ.pdf |
| 101 | Doblin et al. — A reconsideration and response to Parrott AC (2013) "Human psychobiology of MDMA or 'Ecstasy': an overview of 25 years of empirical research" | Hum Psychopharmacol 2014 | 10.1002/hup.2389 | 24590541 | — | CR | MDMA/Doblin_2014_ResponseToParrott.pdf |
| 102 | Parrott — MDMA is certainly damaging after 25 years of empirical research: a reply and refutation of Doblin et al. (2014) | Hum Psychopharmacol 2014 | 10.1002/hup.2390 | 24590542 | — | CR | MDMA/Parrott_2014b_ReplyToDoblin.pdf |
| 103 | Aday et al. — Great expectations: recommendations for improving the methodological rigor of psychedelic clinical trials | Psychopharmacology 2022 | 10.1007/s00213-022-06123-7 | 35359159 | PMC10184717 | CR | MDMA/Aday_2022_GreatExpectations.pdf |
| 104 | Szigeti & Heifets — Expectancy effects in psychedelic trials | Biol Psychiatry Cogn Neurosci Neuroimaging 2024 | 10.1016/j.bpsc.2024.02.004 | 38387698 | — | CR | already listed (LSD and Psilocybin lists): _Cross-cutting/Szigeti_2024b_ExpectancyEffects.pdf |
| 105 | Flameling et al. — Expectancy effects cannot be neglected in MDMA-assisted therapy research | ACS Chem Neurosci 2023 | 10.1021/acschemneuro.3c00692 | 37967550 | PMC10704460 | CR | MDMA/Flameling_2023_ExpectancyEffectsMDMAAT.pdf |
| 106 | McNamee et al. — Studying harms is key to improving psychedelic-assisted therapy — participants call for changes to research landscape | JAMA Psychiatry 2023 | 10.1001/jamapsychiatry.2023.0099 | 36988924 | — | CR | MDMA/McNamee_2023_StudyingHarms.pdf |
| 107 | Ghaznavi et al. — Primum non nocere: the onus to characterize the potential harms of psychedelic treatment | Am J Psychiatry 2025 | 10.1176/appi.ajp.20230914 | 39741443 | — | CR | MDMA/Ghaznavi_2025_PrimumNonNocere.pdf |
| 108 | Soliman et al. — In the new era of psychedelic assisted therapy: a systematic review of study methodology in randomized controlled trials | Psychopharmacology 2024 | 10.1007/s00213-024-06598-6 | 38683460 | PMC11529604 | CR | MDMA/Soliman_2024_RCTMethodologySR.pdf |
| 109 | Seybert et al. — Quality of reporting on psychological interventions in psychedelic treatments: a systematic review | Lancet Psychiatry 2025 | 10.1016/s2215-0366(24)00333-x | 39667373 | — | CR | MDMA/Seybert_2025_ReportingPsychologicalInterventionsSR.pdf |

#### Tier C

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 110 | Hsu et al. — Blinding integrity and psychedelic drug trials (letter on item 89) | JAMA Psychiatry 2026 | 10.1001/jamapsychiatry.2026.2290 | 42555027 | — | CR | MDMA/Hsu_2026_BlindingIntegrityLetter.pdf |
| 111 | Elliott & Chernoloz — Blinding integrity and psychedelic drug trials (letter on item 89) | JAMA Psychiatry 2026 | 10.1001/jamapsychiatry.2026.2293 | 42555000 | — | CR | MDMA/Elliott_2026_BlindingIntegrityLetter.pdf |
| 112 | Cubała et al. — Blinding integrity and psychedelic drug trials — reply (authors of item 89) | JAMA Psychiatry 2026 | 10.1001/jamapsychiatry.2026.2296 | 42555020 | — | CR | MDMA/Cubala_2026_BlindingIntegrityReply.pdf |
| 113 | Schenberg — Who is blind in psychedelic research? Letter to the editor regarding item 90 | Expert Rev Clin Pharmacol 2021 | 10.1080/17512433.2021.1951473 | 34227438 | — | CR | already listed (Psilocybin list): Psilocybin/Schenberg_2021_WhoIsBlindLetter.pdf |
| 114 | Nayak & Zahid — Out of control: blinding, dose response, and psychosocial controls in psychedelic trials (trial-design critique) | J Psychopharmacol 2026 (online 2025) | 10.1177/02698811251368367 | 40888563 | — | CR | already listed (LSD and Psilocybin lists): _Cross-cutting/Nayak_2025_OutOfControl.pdf |
| 115 | Siegel et al. — Registered clinical studies investigating psychedelic drugs for psychiatric disorders | J Psychiatr Res 2021 | 10.1016/j.jpsychires.2021.05.019 | 34048997 | — | CR | MDMA/Siegel_2021_RegisteredPsychedelicStudies.pdf |

## 10. Safety of MDMA given in clinical trials: adverse events, psychiatric adverse events, dependence and non-medical-use liability

The healthy-volunteer safety backbone (Vizeli & Liechti 2017) is on the MDMA list (#29).

#### Tier A

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 116 | Colcott et al. — Side-effects of MDMA-assisted psychotherapy: a systematic review and meta-analysis (across indications) | Neuropsychopharmacology 2024 | 10.1038/s41386-024-01865-8 | 38654146 | PMC11224236 | CR | MDMA/Colcott_2024_SideEffectsSRMA.pdf |
| 117 | Breeksema et al. — Adverse events in clinical treatments with serotonergic psychedelics and MDMA: a mixed-methods systematic review | J Psychopharmacol 2022 | 10.1177/02698811221116926 | 36017784 | PMC9548934 | CR | already listed (several lists): _Cross-cutting/Breeksema_2022_AdverseEventsMixedMethods.pdf |

#### Tier B

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 118 | Murray — Common side effects of MDMA-assisted psychotherapy (commentary on item 116) | Neuropsychopharmacology 2024 | 10.1038/s41386-024-01873-8 | 38740900 | PMC11224309 | CR | MDMA/Murray_2024_CommonSideEffects.pdf |
| 119 | Baldo — The entactogen 3,4-methylenedioxymethamphetamine (MDMA; ecstasy) as a treatment aid in psychotherapy and its safety concerns | Arch Toxicol 2024 | 10.1007/s00204-024-03765-8 | 38743292 | — | CR | MDMA/Baldo_2024_SafetyConcerns.pdf |
| 120 | Bradberry et al. — Toward risk-benefit assessments in psychedelic- and MDMA-assisted therapies | JAMA Psychiatry 2022 | 10.1001/jamapsychiatry.2022.0665 | 35476015 | PMC10039620 | CR | MDMA/Bradberry_2022_RiskBenefitAssessments.pdf |
| 121 | Sabé et al. — Reconsidering evidence for psychedelic-induced psychosis: an overview of reviews, a systematic review, and meta-analysis of human studies (protocol covered MDMA) | Mol Psychiatry 2025 | 10.1038/s41380-024-02800-5 | 39592825 | PMC11835720 | CR | MDMA/Sabe_2025_PsychedelicPsychosisSRMA.pdf |
| 122 | Eskinazi et al. — Psychedelic-induced hypomania and mania: a systematic review and meta-analysis (includes MDMA) | Mol Psychiatry 2026 | 10.1038/s41380-026-03657-6 | 42215638 | PMC13658036 | CR | MDMA/Eskinazi_2026_HypomaniaManiaSRMA.pdf |
| 123 | Henningfield et al. — Psychedelic drug abuse potential assessment for new drug applications and controlled substance scheduling: a United States perspective | J Psychopharmacol 2023 | 10.1177/02698811221140004 | 36588452 | — | CR | MDMA/Henningfield_2023_LiabilityAssessmentUS.pdf |
| 124 | Henningfield et al. — Psychedelic drug abuse potential assessment research for new drug applications and Controlled Substances Act scheduling | Neuropharmacology 2022 | 10.1016/j.neuropharm.2022.109220 | 35987353 | — | CR | MDMA/Henningfield_2022_LiabilityAssessmentResearch.pdf |
| 125 | Heal et al. — Evaluating the abuse potential of psychedelic drugs as part of the safety pharmacology assessment for medical use in humans | Neuropharmacology 2018 | 10.1016/j.neuropharm.2018.01.049 | 29427652 | — | CR | MDMA/Heal_2018_LiabilitySafetyPharmacology.pdf |

#### Tier C

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 126 | Meshkat et al. — Psychedelics and suicide-related outcomes: a systematic review (includes MDMA trials) | J Clin Med 2025 | 10.3390/jcm14051416 | 40094838 | PMC11900607 | CR | MDMA/Meshkat_2025_SuicideOutcomesSR.pdf |
| 127 | Colcott et al. — Development of the MDMA-Assisted Psychotherapy Side Effects Tool (M-SET): a Delphi study | BMJ Open 2026 | 10.1136/bmjopen-2025-105630 | 42114863 | PMC13182389 | CR | MDMA/Colcott_2026_MSETDelphi.pdf |
| 128 | Calder & Hasler — Validation of the Swiss Psychedelic Side Effects Inventory: standardized assessment of adverse effects in studies of psychedelics and MDMA | J Affect Disord 2024 | 10.1016/j.jad.2024.08.091 | 39168165 | — | CR | MDMA/Calder_2024_SwissSideEffectsInventory.pdf |
| 129 | Atila et al. — Oxytocin and MDMA-induced hyponatremia: a secondary analysis of 4 randomized clinical trials (healthy volunteers; title shortened) | JAMA Netw Open 2024 | 10.1001/jamanetworkopen.2024.45278 | 39546312 | PMC11568463 | CR | MDMA/Atila_2024_HyponatremiaSecondaryAnalysis.pdf |
| 130 | Ramaekers et al. — Subjective and neurocognitive profiling of MDMA in healthy volunteers: implications for therapeutic use (review; title shortened) | Mol Psychiatry 2026 | 10.1038/s41380-026-03602-7 | 41951837 | PMC13364663 | CR | MDMA/Ramaekers_2026_HealthyVolunteerProfiling.pdf |
| 131 | Kelly et al. — Subacute and long-term changes in cognitive functioning after administration of classic psychedelics, MDMA and ketamine: a systematic review of clinical and preclinical evidence | Neurosci Biobehav Rev 2026 | 10.1016/j.neubiorev.2026.106911 | 42600962 | — | CR | MDMA/Kelly_2026_CognitiveChangesSR.pdf |
| 132 | Le et al. — The serotonin 2B (5-HT2B) receptor: a narrative review of preclinical and clinical evidence on the safety considerations and therapeutic potential for the treatment of depression | Clin Pharmacol Ther 2026 | 10.1002/cpt.70344 | 42209433 | PMC13339163 | CR | MDMA/Le_2026_5HT2BSafetyReview.pdf |

## 11. History of therapeutic use before scheduling (1970s to 1985)

The MDMA list already holds Passie 2018 on the early psychotherapeutic use, 1977–1985 (#82). Items 133–134 and 140–145 are primary documents from 1985–1986, the years of the scheduling decision.

#### Tier A

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 133 | Greer & Tolbert — Subjective reports of the effects of MDMA in a clinical setting | J Psychoactive Drugs 1986 | 10.1080/02791072.1986.10472364 | 2880946 | — | CR | MDMA/Greer_1986_SubjectiveReportsClinicalSetting.pdf |

#### Tier B

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 134 | Grinspoon & Bakalar — Can drugs be used to enhance the psychotherapeutic process? | Am J Psychother 1986 | 10.1176/appi.psychotherapy.1986.40.3.393 | 2876654 | — | CR | MDMA/Grinspoon_1986_EnhancePsychotherapeuticProcess.pdf |
| 135 | Freudenmann et al. — The origin of MDMA (ecstasy) revisited: the true story reconstructed from the original documents | Addiction 2006 | 10.1111/j.1360-0443.2006.01511.x | 16911722 | — | CR | MDMA/Freudenmann_2006_OriginRevisited.pdf |
| 136 | Benzenhöfer & Passie — Rediscovering MDMA (ecstasy): the role of the American chemist Alexander T. Shulgin | Addiction 2010 | 10.1111/j.1360-0443.2010.02948.x | 20653618 | — | CR | MDMA/Benzenhofer_2010_RediscoveringShulgin.pdf |
| 137 | Passie & Benzenhöfer — The history of MDMA as an underground drug in the United States, 1960–1979 | J Psychoactive Drugs 2016 | 10.1080/02791072.2015.1128580 | 26940772 | — | CR | MDMA/Passie_2016_UndergroundDrugUS1960to1979.pdf |
| 138 | Greer & Tolbert — A method of conducting therapeutic sessions with MDMA (historical document describing their 1980s practice) | J Psychoactive Drugs 1998 | 10.1080/02791072.1998.10399713 | 9924843 | — | CR | MDMA/Greer_1998_TherapeuticSessionsHistorical.pdf |
| 139 | Casey & Heifets — History, pharmacology and therapeutic mechanisms of 3,4-methylenedioxymethamphetamine (MDMA) | Br J Pharmacol 2026 | 10.1111/bph.70225 | 41121647 | PMC12873472 | CR | MDMA/Casey_2026_HistoryPharmacologyMechanisms.pdf |

#### Tier C

| # | Paper | Journal, year | DOI | PMID | PMC | V | Save as |
|---|---|---|---|---|---|---|---|
| 140 | Riedlinger — The scheduling of MDMA: a pharmacist's perspective | J Psychoactive Drugs 1985 | 10.1080/02791072.1985.10472337 | 2865343 | — | CR | MDMA/Riedlinger_1985_SchedulingPharmacist.pdf |
| 141 | Greer & Strassman — Information on "Ecstasy" (letter) | Am J Psychiatry 1985 | 10.1176/ajp.142.11.1391 | 2865906 | — | CR† | MDMA/Greer_1985_InformationOnEcstasyLetter.pdf |
| 142 | Wolfson — Meetings at the edge with Adam: a man for all seasons? (case reports) | J Psychoactive Drugs 1986 | 10.1080/02791072.1986.10472365 | 2880947 | — | CR | MDMA/Wolfson_1986_MeetingsAtTheEdge.pdf |
| 143 | Nichols — Differences between the mechanism of action of MDMA, MBDB, and the classic hallucinogens. Identification of a new therapeutic class: entactogens | J Psychoactive Drugs 1986 | 10.1080/02791072.1986.10472362 | 2880944 | — | CR | MDMA/Nichols_1986_Entactogens.pdf |
| 144 | Shulgin — The background and chemistry of MDMA | J Psychoactive Drugs 1986 | 10.1080/02791072.1986.10472361 | 2880943 | — | CR | MDMA/Shulgin_1986_BackgroundChemistry.pdf |
| 145 | Downing — The psychological and physiological effects of MDMA on normal volunteers (pre-scheduling human study) | J Psychoactive Drugs 1986 | 10.1080/02791072.1986.10472366 | 2880948 | — | CR | MDMA/Downing_1986_NormalVolunteers.pdf |
| 146 | Gibb et al. — MDMA: historical perspectives | Ann N Y Acad Sci 1990 | 10.1111/j.1749-6632.1990.tb16913.x | 1979213 | — | CR | MDMA/Gibb_1990_HistoricalPerspectives.pdf |
| 147 | Pentney — An exploration of the history and controversies surrounding MDMA and MDA | J Psychoactive Drugs 2001 | 10.1080/02791072.2001.10400568 | 11718314 | — | CR | MDMA/Pentney_2001_HistoryControversies.pdf |
| 148 | Benzenhöfer & Passie — Zur Frühgeschichte von „Ecstasy" [The early history of "Ecstasy"] (in German) | Nervenarzt 2006 | 10.1007/s00115-005-2001-y | 16397805 | — | CR | MDMA/Benzenhofer_2006_EarlyHistoryEcstasy.pdf |
| 149 | Dunlap et al. — Dark classics in chemical neuroscience: 3,4-methylenedioxymethamphetamine | ACS Chem Neurosci 2018 | 10.1021/acschemneuro.8b00155 | 30001118 | PMC6197894 | CR | MDMA/Dunlap_2018_DarkClassicsMDMA.pdf |

## Retracted — obtain for documentation only, never cite as evidence (METHODS §3.2)

With Mithoefer et al. 2019 (MDMA list R-3, R-4), these are the three *Psychopharmacology* papers retracted in August 2024 that the BMJ news item (MDMA list #25) reports.

| # | Paper | Journal, year | DOI | PMID | PMC | V | Status | Save as |
|---|---|---|---|---|---|---|---|---|
| R-1 | Jerome et al. — RETRACTED ARTICLE: Long-term follow-up outcomes of MDMA-assisted psychotherapy for treatment of PTSD: a longitudinal pooled analysis of six phase 2 trials | Psychopharmacology 2020 | 10.1007/s00213-020-05548-2 | 32500209 | PMC7351848 | CR | **Retracted 2024-08-10**; Crossref `updated-by` type retraction → 10.1007/s00213-024-06665-y | _Retracted/Jerome_2020_RETRACTED_LongTermFollowUp.pdf |
| R-2 | Jerome et al. — Retraction Note (of R-1) | Psychopharmacology 2024 | 10.1007/s00213-024-06665-y | 39126500 | PMC11513715 | CR | the retraction notice | _Retracted/Jerome_2024_RetractionNote.pdf |
| R-3 | Feduccia et al. — RETRACTED ARTICLE: Discontinuation of medications classified as reuptake inhibitors affects treatment response of MDMA-assisted psychotherapy | Psychopharmacology 2021 | 10.1007/s00213-020-05710-w | 33221932 | PMC7826309 | CR | **Retracted 2024-08-10**; Crossref `updated-by` type retraction → 10.1007/s00213-024-06671-0 | _Retracted/Feduccia_2021_RETRACTED_ReuptakeInhibitorDiscontinuation.pdf |
| R-4 | Feduccia et al. — Retraction Note (of R-3) | Psychopharmacology 2024 | 10.1007/s00213-024-06671-0 | 39126502 | PMC11513749 | CR | the retraction notice | _Retracted/Feduccia_2024_RetractionNote.pdf |

## 12. Registered trials (ClinicalTrials.gov API v2, read 2026-10-17)

Clinical populations other than PTSD, the conjoint (couples) trials, and the PTSD registrations that the other-outcome papers above name. "Linked items" come from registration numbers printed in the PubMed records, except where marked "by trial name". Trial arms and doses are deliberately not reproduced.

| NCT number | Condition (as registered) | Phase | Status | Results posted | Linked items on this list |
|---|---|---|---|---|---|
| NCT04158778 | Alcohol use disorder (Bristol–Imperial study) | Phase 1 | Unknown | No | 2 (registration in its PubMed record); 1 and 3 report Bristol work by the same group — confirm on reading |
| NCT05943665 | Alcohol use disorder with PTSD (veterans) | Phase 2 | Completed | No | 8 (protocol) |
| NCT05709353 | Alcohol use disorder with PTSD (MPATHY) | Phase 2 | Unknown | No | 9 (protocol) |
| NCT07118839 | PTSD with alcohol use disorder (veterans) | Phase 2/3 | Recruiting | No | — |
| NCT05219175 | PTSD with opioid use disorder after childbirth | Phase 2 | Recruiting | No | — |
| NCT02008396 | Social anxiety in autistic adults | Phase 2 | Completed | **Yes** (2020-10-14) | 13; MDMA list #72 |
| NCT04053036 | Autism spectrum disorder; healthy comparison group (laboratory study) | Early phase 1 | Completed | **Yes** (2024-11-25) | — (no publication identified) |
| NCT07303907 | Autism spectrum disorder (R-enantiomer of MDMA) | Phase 2 | Recruiting | No | — |
| NCT07555132 | Autism spectrum disorder (oxytocin response) | Not applicable | Not yet recruiting | No | — |
| NCT05138068 | Social anxiety disorder | Phase 2 | Completed | No | 15 (protocol) |
| NCT00252174 | Anxiety with advanced-stage cancer | Phase 2 | Terminated | **Yes** (2017-05-05) | — (no publication identified) |
| NCT02427568 | Anxiety with a life-threatening illness | Phase 2 | Completed | **Yes** (2021-08-02) | 20 |
| NCT05584826 | Adjustment disorder in dyads of patients with cancer and a concerned significant other | Phase 2 | Recruiting | No | — |
| NCT04454684 | Anorexia nervosa (restricting type); binge-eating disorder | Phase 2 | Withdrawn | No | — |
| NCT07542145 | Bulimia nervosa | Phase 1 | Recruiting | No | — |
| NCT02876172 | PTSD, conjoint therapy in dyads | Phase 1/2 | Completed | **Yes** (2021-07-19) | — (PubMed records of 32–33 give no registration number) |
| NCT05979844 | PTSD; relational problems (brief conjoint therapy) | Phase 3 (as registered) | Completed | No | 35 (protocol) |
| NCT06044675 | PTSD, conjoint therapy with and without MDMA (RCT) | Phase 2 | Recruiting | No | — |
| NCT05455996 | PTSD and adjustment disorders in healthcare workers and first responders | Phase 2 | Not yet recruiting | No | — |
| NCT05783817 | Obsessive-compulsive disorder (with CBT) | Phase 2 | Recruiting | No | — |
| NCT07301632 | Chronic neuropathic pain (EASE-Pain) | Phase 2 | Recruiting | No | 53 (by trial name) |
| NCT06066853 | Fibromyalgia | Early phase 1 | Recruiting | No | — |
| NCT06683014 | Borderline personality disorder | Phase 2 | Recruiting | No | — |
| NCT05770375 | Schizophrenia (tolerability) | Phase 1/2 | Recruiting | No | — |
| NCT06565494 | Pathological narcissism | Early phase 1 | Active, not recruiting | No | — |
| NCT04648137 | Arginine vasopressin deficiency (diagnostic test) | Not applicable | Completed | No | 47 |
| NCT06789705 | Arginine vasopressin deficiency (diagnostic test) | Not applicable | Recruiting | No | — |
| NCT03606538 | Hepatic impairment (pharmacokinetics) | Phase 1 | Not yet recruiting | No | — |
| NCT05066282 | PTSD, long-term safety and effectiveness follow-up (observational) | Not applicable | Completed | No | — (no publication identified) |
| NCT03282123 | PTSD (open-label) | Phase 2 | Completed | Yes | 73 |
| NCT03537014 | PTSD (phase 3, MAPP1) | Phase 3 | Completed | Yes | 75, 81 |
| NCT00090064 | PTSD (phase 2) | Phase 2 | Completed | Yes | 79 |
| NCT05961527 | PTSD, group therapy for veterans | Phase 1/2 | Completed | No | 82 |

Registered outside ClinicalTrials.gov (numbers from the PubMed records; registries not searched): the depression trial (items 37–39, 43), EudraCT 2021-000805-26; EMMAC (item 26), ACTRN12619001334190. The tinnitus trial's PubMed record gives no registration number.

Non-PTSD registrations with posted results: **4** (NCT02008396, NCT02427568, NCT00252174, NCT04053036); with the PTSD-dyad conjoint trial NCT02876172, **5**.

## Known gaps

Published trials in clinical populations other than PTSD are few and small: one open-label alcohol use disorder study with a secondary Bayesian analysis; one randomized pilot each in autistic adults with social anxiety (MDMA list #72) and in anxiety with a life-threatening illness; two uncontrolled or pilot conjoint-therapy trials (PTSD dyads); one open-label proof-of-principle trial in major depressive disorder with a seven-month follow-up and a published critique; one small randomized crossover proof-of-principle study in tinnitus; and one diagnostic randomized crossover study in arginine vasopressin deficiency. For eating disorders, obsessive-compulsive disorder, chronic neuropathic pain, fibromyalgia, borderline personality disorder, schizophrenia, pathological narcissism, bulimia nervosa and adjustment disorder there are registered trials but no published results; for specific phobia, prolonged grief, moral injury and sexual dysfunction there are only reviews or proposals. Two registrations have posted results with no publication found (NCT00252174, NCT04053036), and the long-term PTSD follow-up NCT05066282 is completed with neither results nor a paper; the only peer-reviewed long-term follow-up that is not retracted is Mithoefer et al. 2013 (one phase 2 trial). Registries other than ClinicalTrials.gov (EU CTR/CTIS, ANZCTR, ISRCTN) were not searched. Not entered because it has no DOI in PubMed: Bernschneider-Reif et al. 2006, "The origin of MDMA ('ecstasy') — separating the facts from the myth", *Pharmazie* (PMID 17152992); a Crossref title search could verify it if a DOI exists. Single case reports were screened out (listed in the log: neuropathic pain, OCD, palliative care, a Bristol participant, a conjoint-therapy case, and one case of unsupervised self-treatment). Healthy-volunteer laboratory studies of reinforcing effects were not added because this brief limits dependence liability to trial settings; the trial-setting evidence here is the follow-up in item 66 and the regulatory reviews in items 123–125, while the sponsor's own liability data sit in the FDA briefing document (MDMA list R6). Whether item 90 (and the umbrella review, item 93) covers MDMA trials is to be confirmed on reading: item 90's abstract does not name MDMA. Seen during screening but outside this brief and not on the MDMA list: several PTSD-only meta-analyses and PTSD primary trials (PMIDs in the log, for whoever maintains the MDMA list). The 2024 FDA and ICER reports on the MDMA list (R6, R7) are PTSD-specific; no report-level source for other indications was found.

## Verification block (2026-10-17)

- Crossref `works/<DOI>` calls made in the app's browser: **163** — 159 DOIs from the PubMed records of the 160 screened candidates (one candidate has no DOI), 3 correction notices read from `updated-by`, and 1 replacement DOI; plus 1 Crossref bibliographic search (to find the replacement).
- Resolved to the paper named (title words, journal, year and first author agree with PubMed): **162**. The one with a German title in Crossref (item 148) matched on author, journal and year; PubMed carries the English translation.
- Did not resolve: **1** — `10.1176/ajp.142.11.aj142111391` (PubMed's DOI for Greer & Strassman 1985; HTTP 404 twice). Replaced by `10.1176/ajp.142.11.1391`, found by Crossref search and fetched with `works/<DOI>` (item 141, `CR†`).
- Verified but not retained after final screening (listed in the log): 9 (Doblin 2002, Sessa 2007, Emerson 2014, Feduccia 2018, Hughes 2024, Roseman 2025, Sznitman 2024, Schenberg 2025, Matvey 2025).
- In this file: **149** papers in tiers (Tier A **29**, Tier B **56**, Tier C **64**) and **4** rows in the retracted table. Six tiered rows are already on other lists and point to the existing files (items 21, 90, 104, 113, 114, 117).
- **Retractions: 2** — Jerome et al. 2020 and Feduccia et al. 2021 (*Psychopharmacology*, both retracted 2024-08-10, `updated-by` type retraction), with their retraction notes. The third retraction of the set (Mithoefer et al. 2019) is on the MDMA list.
- **Expressions of concern: 2** — Ponte et al. 2021 and Gorman et al. 2020 (*J Trauma Stress*; notices `10.1002/jts.23117` and `10.1002/jts.23116`, dated 2024-12-03 in `updated-by`); each also has a correction (`10.1002/jts.23098`, `10.1002/jts.23097`).
- **Corrections/errata: 4** — the two above, Kvam et al. 2025 (corrigendum `10.1192/bjp.2026.10579`, item 38) and Schimmers et al. 2022 (correction `10.1007/s00213-023-06406-7`, item 24).
- Other `updated-by`/`update-to` links: Schipper et al. 2024 (item 21) is version pub2 of Cochrane review CD015383 (`update-to` type new_version). No other record carried an update.
- Free full text: 83 entries in `scratchpad/mdma2/beyond_free.json` — 70 with a PubMed Central id (PubMed record, no embargo listed) and 13 whose Crossref record carries a Creative Commons licence for the published version (`pmcid` empty; 8 of these are Elsevier journals on ScienceDirect, which the app's browser cannot open, so they go to VS's list).
