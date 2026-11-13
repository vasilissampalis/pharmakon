# Methadone and buprenorphine — search log (PRISMA 2020)

Protocol: `docs/METHODS.md` §2. Section-level strings were written on 2026-10-15 before screening; re-worded re-runs of refused URLs are recorded as such. Date searched: 2026-10-16.

## Layer 1 — Crossref bibliographic search (run by AI co-editor)

Endpoint and screening rules as in `Heroin_search-log.md`. Additional exclusions here: *Cochrane Clinical Answers* items (derivative summaries of the Cochrane reviews already included), trade digests, and conference abstracts.

Access conditions: of 11 attempted calls, 8 returned records, 2 were refused with HTTP 429 and 2 returned a transient target error (one of those strings was re-worded and then succeeded). Pacing 150 s between calls. A further 22 records in the DOI list were surfaced by searches run earlier in this session for Heroin, Fentanyl-and-analogues and Prescription-opioids; those strings are logged in the respective files and are cross-referenced below.

### Section-level and targeted queries

| # | Query string | Result |
|---|---|---|
| M1 | methadone maintenance versus buprenorphine retention Cochrane review Mattick | 20 hits, 10 retained (Mattick 2014 Cochrane; Mattick 2009 Cochrane; Mattick 2003 RCT; Doran 2003; Dean 2004; Breen 2003; Ahmadi 2003; Ward 1994; Hall 1993; Burns 2015; Sadek 2022; Bell 2006; Newman 2011) |
| M2 | methadone QTc prolongation torsades de pointes cardiac arrhythmia | transient target error; re-run as M3 |
| M3 | methadone QT interval prolongation torsade cardiac safety review | 20 hits, 1 retained (Perrin-Terrin 2010). The result set was almost entirely *Reactions Weekly* single-case notices — **the methadone QTc literature is not covered; recorded under Known gaps** |
| M4 | methadone induction first weeks treatment mortality risk cohort study | refused (429) — **induction-period mortality only partly covered (via Bell 2009 and Cornish 2010); recorded under Known gaps** |
| M5 | buprenorphine precipitated withdrawal fentanyl low dose induction | 20 hits, 8 retained (Varshneya 2021; Spadaro 2022; Quattlebaum 2021; Bormann 2022/2023; Alexander 2025; Montalvo 2021; Kuhlman 1998; Kinasz 2020) |
| M6 | extended release injectable buprenorphine depot opioid use disorder trial | transient target error; re-run as M7 |
| M7 | depot buprenorphine monthly injection opioid dependence randomised | 20 hits, 10 retained (Ling 2019 **+ 2020 corrigendum**; Jones 2020; Larance 2020; Lancaster 2022; Schmith 2019; Guillery 2023; Ramage 2025; Sobel 2004; Allikmets 2019) |
| M8 | buprenorphine diversion non-prescribed use motivations injection review | 20 hits, 14 retained (Yokell 2011; Rubel 2023; Allen 2016; Silverstein 2020; McLean 2019; Hayes 2021; Winstock 2009 ×2; Jenkinson 2005; Bach 2022; Daniulaityte 2019, 2023; Johnson 2019; Öhlin 2015; Parkin 2023). Also surfaced Smith 2019 on non-prescribed buprenorphine, heroin and kratom, carried to the Kratom map |
| M9 | methadone buprenorphine pregnancy neonatal abstinence syndrome MOTHER trial | 20 hits, 3 retained (Lemon 2018; Kushnir 2023; Winhusen 2014). **The MOTHER trial itself was not surfaced; recorded under Known gaps** |
| M10 | mortality risk during after opioid substitution treatment BMJ 2017 | 20 hits, 6 retained — **this call located Sordo et al. 2017 (10.1136/bmj.j1550), the item four earlier strings had failed to reach**; also Manhapra 2017 editorial; Cornish 2010; Hickman 2015; Eide 2024; and Gowing 2012 (noted, not retained) |
| M11 | opioid agonist treatment prisons implementation outcomes systematic review | 20 hits, 14 retained (Komalasari 2021 ×2; Larney 2009, 2010, 2018; Nielsen 2016 Cochrane; Amato 2011 Cochrane; Pani 2010 Cochrane; Hestevik 2024; Matheson 2024; Li 2025; Chetty 2017; Samsó Jofra 2022; Schwarz 2024; Day 2022; Conway 2023) |

Records carried in from this session's other substance searches: Bell 2009 ×2, Larney 2020 (Pain Med), Kleinman 2026, Cataldo 2016, Zamani 2020, Naren 2024, Wikner 2014, Mattick 2003, Fischer 1999, Beck 2014, Mitchell 2004, Zhou 2026, McCance-Katz 2011, Noble 2019, Krabbe 2003, Ellerbroek 2022, Dole 1965 (from the heroin-maintenance strings); van Dorp 2006, Yassen 2007, Gal 1989 (from the opioid-respiratory-depression string); Santo 2021 and Bukten 2024 (from the OAT-mortality strings).

### DOI corrections and update checks

- No DOI was written from memory; all 95 were copied from Crossref responses in this session. No `works/<DOI>` re-fetch was needed; nothing was dropped.
- Correction found: Ling et al. 2019 (Subst Abuse Rehabil) has a 2020 corrigendum, 10.2147/sar.s247083.
- Two Crossref records exist for the Bormann et al. F1000Research case report (versions 1 and 2); version 2 is listed. Two records exist for Kuhlman et al. 1998 in Addiction; the more heavily cited one is listed.
- Retraction field (`updated-by`) not read; Retraction Watch check outstanding for all items.
- **Note for the Heroin map:** Sordo et al. 2017 was listed there under Known gaps after four failed attempts. String M10 located it; it has been added to the Heroin Tier A table and the gap entry amended.

## Layer 2 — PubMed (to be run by VS)

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `(methadone[Title] OR buprenorphine[Title]) AND (maintenance OR "agonist treatment" OR "substitution treatment") AND (mortality OR death*) AND (cohort OR "meta-analysis"[Publication Type])` | oat_pubmed_P1.csv | |
| P2 | `(methadone[Title] OR buprenorphine[Title]) AND retention[Title/Abstract] AND (randomized controlled trial[Publication Type] OR "systematic review"[Publication Type])` | oat_pubmed_P2.csv | |
| P3 | `(methadone[Title]) AND (QT OR QTc OR "torsade de pointes" OR arrhythmi*) AND humans[MeSH Terms]` | oat_pubmed_P3.csv | |
| P4 | `(methadone[Title] OR buprenorphine[Title]) AND (induction OR initiation OR "first four weeks" OR "treatment entry") AND (mortality OR death* OR overdose)` | oat_pubmed_P4.csv | |
| P5 | `(buprenorphine[Title]) AND ("precipitated withdrawal" OR "low-dose induction" OR microdosing OR macrodosing) AND (fentanyl OR "opioid use disorder")` | oat_pubmed_P5.csv | |
| P6 | `(buprenorphine[Title]) AND ("extended-release" OR depot OR injectable OR implant OR CAM2038 OR RBP-6000) AND (randomized controlled trial[Publication Type] OR cohort OR "systematic review"[Publication Type])` | oat_pubmed_P6.csv | |
| P7 | `(buprenorphine[Title] OR methadone[Title]) AND (diversion OR "non-prescribed" OR "nonmedical use" OR misuse) AND humans[MeSH Terms]` | oat_pubmed_P7.csv | |
| P8 | `(methadone OR buprenorphine OR "opioid agonist treatment") AND (prison* OR incarcerat* OR jail) AND (mortality OR retention OR HIV OR implementation)` | oat_pubmed_P8.csv | |
| P9 | `(methadone[Title] OR buprenorphine[Title]) AND (pregnan* OR "neonatal abstinence syndrome" OR "neonatal opioid withdrawal") AND (randomized controlled trial[Publication Type] OR cohort OR "systematic review"[Publication Type])` | oat_pubmed_P9.csv | |
| P10 | `(buprenorphine[Title]) AND ("ceiling effect" OR "respiratory depression" OR "partial agonist") AND humans[MeSH Terms]` | oat_pubmed_P10.csv | |
| P11 | `(naltrexone[Title]) AND ("extended-release" OR injectable) AND (buprenorphine OR methadone) AND (randomized controlled trial[Publication Type] OR comparative)` | oat_pubmed_P11.csv | |
| P12 | `(methadone[Title]) AND (pharmacokinetic* OR CYP3A4 OR CYP2B6 OR interaction* OR enantiomer*) AND humans[MeSH Terms]` | oat_pubmed_P12.csv | |
| P13 | `("take-home" OR "take home doses" OR "telehealth" OR "COVID-19 flexibilities") AND (methadone OR buprenorphine) AND (outcome* OR retention OR overdose OR diversion)` | oat_pubmed_P13.csv | |
| P14 | `("opioid agonist treatment" OR "opioid substitution treatment") AND (coverage OR access OR Greece OR Europe) AND (estimate* OR survey OR waiting list*)` | oat_pubmed_P14.csv | |

## Layer 3 — Cochrane Library (to be run by VS)

Search and export: `methadone maintenance`; `buprenorphine maintenance`; `opioid withdrawal management` (Gowing reviews); `maintenance agonist treatments for opiate-dependent pregnant women` (Minozzi); `psychosocial interventions plus agonist`; `naltrexone for opioid dependence`. Save each → `oat_cochrane_<topic>.csv`.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of items 1, 3, 5, 6, 21, 23 and 25. Forward: "cited by" on items 1, 5, 15 and 18 — in particular to recover the MOTHER trial, the Lofwall and Haight depot trials, the Krantz methadone-QTc papers and the X:BOT naltrexone comparison.

## PRISMA counts

To be completed after Layers 2–4. Layer 1 so far: 11 Crossref calls attempted for this substance, 8 result sets screened (approximately 160 records) plus 22 records carried from other substances' searches; 95 records retained.
