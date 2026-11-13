# PCP (phencyclidine) — evidence map and PDF list (v0.1, 2026-10-15)

All DOIs below come from Crossref API responses retrieved on 2026-10-15 (never from memory). Each row's DOI, title, journal, year, first author and `updated-by` field (retraction/erratum check) were returned by Crossref for that record; the DOIs marked ◆ were additionally re-fetched one by one at `works/<DOI>`. Retraction check: none retracted; no errata found. Save each PDF into `PDFs/PCP/` with the filename given; cross-cutting papers go in `PDFs/_Cross-cutting/`.

How this list was built: (1) landmark studies (Luby 1959; McCarron 1981; Jentsch & Roth 1999) and the critical reviews around them; (2) case series, forensic series and the 3-MeO-PCP literature found by Crossref bibliographic search on the pre-registered section-level queries and targeted author/title queries (strings in `PCP_search-log.md`); (3) screening by title and journal. **The PCP literature is thin and old**: most primary clinical data are 1975–1990 case series from US emergency departments and medical examiners; the modern literature is on PCP analogues (3-MeO-PCP, 4-MeO-PCP) and on the PCP/NMDA model of schizophrenia (largely preclinical, cited here only through reviews). The list is therefore shorter than a Tier-1 target; the PubMed layer (strings in the search log) will add to it.

Context note: Crossref was heavily rate-limited during this build (shared proxy egress), so fewer targeted queries could be run than planned; the known gaps paragraph lists the landmarks still to be resolved.

**Work through the list in order. Tier A first.**

---

## Tier A — needed now (landmarks, classic case series, backbone reviews)

| # | Paper | Journal, year | DOI | Save as |
|---|---|---|---|---|
| 1 | Luby et al. — Study of a new schizophrenomimetic drug: Sernyl ◆ | AMA Arch Neurol Psychiatry 1959 | 10.1001/archneurpsyc.1959.02340150095011 | Luby_1959_Sernyl.pdf |
| 2 | Johnson & Jones — Neuropharmacology of phencyclidine: basic mechanisms and therapeutic potential | Annu Rev Pharmacol Toxicol 1990 | 10.1146/annurev.pa.30.040190.003423 | Johnson_1990_NeuropharmacologyReview.pdf |
| 3 | Jentsch & Roth — The neuropsychopharmacology of phencyclidine: from NMDA receptor hypofunction to the dopamine hypothesis of schizophrenia | Neuropsychopharmacology 1999 | 10.1016/s0893-133x(98)00060-8 | Jentsch_1999_NMDAHypofunctionDopamine.pdf |
| 4 | McCarron et al. — Acute phencyclidine intoxication: incidence of clinical findings in 1,000 cases ◆ | Ann Emerg Med 1981 | 10.1016/s0196-0644(81)80047-9 | McCarron_1981a_1000Cases.pdf |
| 5 | McCarron et al. — Acute phencyclidine intoxication: clinical patterns, complications, and treatment ◆ | Ann Emerg Med 1981 | 10.1016/s0196-0644(81)80118-7 | McCarron_1981b_PatternsComplicationsTreatment.pdf |
| 6 | Morris & Wallach — From PCP to MXE: a comprehensive review of the non-medical use of dissociative drugs | Drug Test Anal 2014 | 10.1002/dta.1620 | _Cross-cutting/Morris_2014_FromPCPToMXE.pdf |
| 7 | Bäckberg et al. — Phencyclidine analog use in Sweden: intoxication cases involving 3-MeO-PCP and 4-MeO-PCP from the STRIDA project | Clin Toxicol 2015 | 10.3109/15563650.2015.1079325 | Backberg_2015_STRIDA3MeOPCP.pdf |
| 8 | Johansson et al. — A non-fatal intoxication and seven deaths involving the dissociative drug 3-MeO-PCP | Forensic Sci Int 2017 | 10.1016/j.forsciint.2017.02.034 | Johansson_2017_SevenDeaths3MeOPCP.pdf |
| 9 | Poklis et al. — Phencyclidine and violent deaths in St. Louis, Missouri: a survey of medical examiners' cases from 1977 through 1986 | Am J Drug Alcohol Abuse 1990 | 10.3109/00952999009001588 | Poklis_1990_ViolentDeathsStLouis.pdf |
| 10 | Brecher et al. — Phencyclidine and violence: clinical and legal issues | J Clin Psychopharmacol 1988 | 10.1097/00004714-198812000-00003 | Brecher_1988_PCPAndViolence.pdf |

## Tier B — section backbone

| # | Paper | Journal, year | DOI | Save as |
|---|---|---|---|---|
| 11 | Zukin & Zukin — Specific [3H]phencyclidine binding in rat central nervous system | PNAS 1979 | 10.1073/pnas.76.10.5372 | Zukin_1979_PCPBindingPNAS.pdf |
| 12 | Javitt — Twenty-five years of glutamate in schizophrenia: are we there yet? | Schizophr Bull 2012 | 10.1093/schbul/sbs100 | Javitt_2012_TwentyFiveYearsGlutamate.pdf |
| 13 | Akmal et al. — Rhabdomyolysis with and without acute renal failure in patients with phencyclidine intoxication | Am J Nephrol 1981 | 10.1159/000166498 | Akmal_1981_Rhabdomyolysis.pdf |
| 14 | Walberg et al. — Quantitation of phencyclidine in serum by enzyme immunoassay: results in 405 patients | J Anal Toxicol 1983 | 10.1093/jat/7.2.106 | Walberg_1983_SerumPCP405Patients.pdf |
| 15 | Fauman & Fauman — Chronic phencyclidine (PCP) abuse: a psychiatric perspective | J Psychedelic Drugs 1980 | 10.1080/02791072.1980.10471442 | Fauman_1980_ChronicAbusePsychiatric.pdf |
| 16 | Fauman et al. — Psychiatric sequelae of phencyclidine abuse | Clin Toxicol 1976 | 10.3109/15563657608988154 | Fauman_1976_PsychiatricSequelae.pdf |
| 17 | Bakota et al. — Fatal intoxication involving 3-MeO-PCP: a case report and validated method | J Anal Toxicol 2016 | 10.1093/jat/bkw056 | Bakota_2016_Fatal3MeOPCP.pdf |
| 18 | Copeland et al. — The first fatal intoxication with 3-MeO-PCP in the UK and a review of the literature | J Anal Toxicol 2022 | 10.1093/jat/bkac015 | Copeland_2022_FirstUKFatal3MeOPCPReview.pdf |

## Tier C — deaths, case reports, analogues, policy context

| # | Paper | Journal, year | DOI | Save as |
|---|---|---|---|---|
| 19 | Fauman et al. — Psychosis induced by phencyclidine | JACEP 1975 | 10.1016/s0361-1124(75)80109-2 | Fauman_1975_PsychosisInduced.pdf |
| 20 | Fauman & Fauman — Treatment of phencyclidine overdose | Ann Emerg Med 1981 | 10.1016/s0196-0644(81)80389-7 | Fauman_1981_TreatmentOverdose.pdf |
| 21 | de Jong et al. — The risk of emerging new psychoactive substances: the first fatal 3-MeO-PCP intoxication in the Netherlands | J Forensic Leg Med 2019 | 10.1016/j.jflm.2019.05.011 | deJong_2019_FirstFatalNetherlands.pdf |
| 22 | Bertol et al. — 3-MeO-PCP intoxication in two young men: first in vivo detection in Italy | Forensic Sci Int 2017 | 10.1016/j.forsciint.2016.12.028 | Bertol_2017_ItalyTwoCases.pdf |
| 23 | Berar et al. — Intoxication with 3-MeO-PCP alone | Medicine 2019 | 10.1097/md.0000000000018295 | Berar_2019_3MeOPCPAlone.pdf |
| 24 | Castro et al. — Intoxication by 3-MeO-PCP and O-desmethyltramadol: an unusual NPS mix | Int J Legal Med 2022 | 10.1007/s00414-022-02818-w | Castro_2022_3MeOPCPTramadolMix.pdf |

## Reports (no DOI; save the PDF of the full report)

| # | Report | Save as |
|---|---|---|
| R1 | SAMHSA/DAWN — Emergency department visits involving phencyclidine (PCP) (The DAWN Report, 2013) | _Epidemiology/SAMHSA_2013_DAWN_PCP.pdf |
| R2 | SAMHSA — NSDUH 2024 detailed tables (PCP lifetime/past-year use) | _Epidemiology/SAMHSA_2024_NSDUH_DetailedTables.pdf |
| R3 | NIDA Monitoring the Future — latest national survey results (PCP items, 12th grade) | _Epidemiology/MTF_latest_NationalResults.pdf |
| R4 | DEA — Drug Enforcement Administration drug fact sheet / NFLIS annual report (PCP identifications) | _Epidemiology/DEA_NFLIS_latest.pdf |
| R5 | EUDA/EMCDDA — risk assessment or technical reports on arylcyclohexylamines (methoxetamine 2014; 3-MeO-PCP in EU Early Warning System briefings) | _Epidemiology/EMCDDA_2014_MethoxetamineRiskAssessment.pdf |
| R6 | UNODC — World Drug Report 2025 (NPS booklet: dissociatives) | _Epidemiology/UNODC_2025_WorldDrugReport.pdf |

## Known gaps this list does not yet cover (to come from the PubMed layer and later Crossref passes)

Landmarks whose DOIs were not surfaced in the rate-limited Crossref window: Javitt & Zukin 1991 (Am J Psychiatry, "Recent advances in the phencyclidine model of schizophrenia" — three queries, not indexed by author); Anis et al. 1983 (Br J Pharmacol, ketamine and phencyclidine selectively reduce NMDA excitation); Lodge & Mercier 2015 (Br J Pharmacol, "Ketamine and phencyclidine: the good, the bad and the unexpected"); Roth et al. 2013 (PLoS One, methoxetamine and 3-/4-MeO-PCP as NMDA ligands); Cook et al. 1982 (Clin Pharmacol Ther, phencyclidine disposition after IV and oral doses); Allen & Young 1978 and Yesavage & Freman 1978 (phencyclidine-induced psychosis series); Barton et al. 1980 (27 cases confirmed by urine assay); Dominici et al. 2015 (J Med Toxicol case series); Bey & Patel 2007 (Cal J Emerg Med review); Burns & Lerner 1978 and Noguchi & Nakamura 1978 (PCP-related deaths); Golden et al. 1987 (phencyclidine use during pregnancy); Cosgrove & Newell 1991 (recovery of neuropsychological function). Sections with no verified peer-reviewed source: epidemiology and trends (only reports R1–R4); dependence and withdrawal in humans; cognitive outcomes of chronic use; pregnancy; driving; harm reduction; legal status by jurisdiction.

## Verification block

- DOIs in the list: 24. All were returned by Crossref API search responses on 2026-10-15 together with title, container-title, issued year, first author and the `updated-by` field.
- DOIs additionally re-fetched individually at `works/<DOI>` (◆): 3 attempted → 3 resolved (items 1, 4, 5). One attempt (item 2) was refused by the proxy (HTTP 429) and rests on its search record.
- Dropped: 0. Note that Crossref's `issued` date for item 13 (Akmal) is the 2008 online date; the print year 1981 is given.
- Errata/corrections: none found. Retractions: none found.
