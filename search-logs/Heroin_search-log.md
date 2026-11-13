# Heroin (diacetylmorphine) — search log (PRISMA 2020)

Protocol: `docs/METHODS.md` §2. Section-level strings were written on 2026-10-15 before screening and are not altered during screening; where a string had to be re-worded because the proxy refused the URL (HTTP 429, HTTP 403 for URL length, or a transient target error), the re-worded re-run is recorded as such. Date searched: 2026-10-15.

## Layer 1 — Crossref bibliographic search (run by AI co-editor, 2026-10-15)

Endpoint: `https://api.crossref.org/works?query.bibliographic=<terms>&filter=type:journal-article&rows=15–20&select=DOI,title,container-title,issued,is-referenced-by-count,author&sort=relevance`.

Screening rules applied to every result set: keep systematic reviews, meta-analyses, landmark primary studies, major cohorts, RCTs and authoritative reviews in serious journals; keep published critiques, replies and corrections of anything kept; drop conference abstracts, supplement items, trade newsletters (*Reactions Weekly*, *Alcoholism & Drug Abuse Weekly*, *Brown University Psychopharmacology Update*), news and magazine pieces, book reviews, animal-only studies where human data exist, analytical-chemistry method papers, and off-topic hits.

Access conditions: the shared egress proxy rate-limited Crossref heavily throughout this window. Of 32 attempted calls, 15 returned records, 8 were refused with HTTP 429, 7 returned a transient target error, and 2 were refused with HTTP 403 because the URL exceeded the fetchable length (query strings were shortened to ≤75 characters thereafter). No refused URL was re-fetched; pacing was 55–120 s between calls.

### Section-level and targeted queries

| # | Query string (terms passed to `query.bibliographic`) | Result |
|---|---|---|
| H1 | heroin diacetylmorphine pharmacokinetics 6-monoacetylmorphine humans | 15 hits, 6 retained (Gyr 2000; Guessoum 2025; Hutchinson 2002; Volavka 1970; Rop 1997; Dole 1965 noted but not retained — historical, covered under Methadone) |
| H2 | pharmacokinetics pharmacodynamics high doses pharmaceutically prepared heroin intravenous inhaled Rook | refused (HTTP 403, URL too long) — gap (Rook 2006) |
| H3 | pharmacokinetics pharmaceutically prepared heroin inhaled Rook | refused (429) — gap (Rook 2006) |
| H4 | heroin overdose mortality risk factors prison release cohort | 15 hits, 8 retained (Binswanger 2011, 2013; Bukten 2017, 2024; Forsyth 2017; O'Connor 2022; Hartung 2023; Hickman 2003; Dietze 2006) |
| H5 | take-home naloxone distribution opioid overdose deaths systematic review | refused (429); re-run as H6 |
| H6 | naloxone distribution programmes opioid overdose death prevention review | 20 hits, 6 retained (Clark 2014; Orkin 2015 critique; Winstanley 2015 reply; Green 2008; Zang 2021; Dowd 2023; Davidson 2015) |
| H7 | mortality risk during and after opioid substitution treatment cohort studies meta-analysis Sordo | refused (HTTP 403, URL too long) |
| H8 | opioid substitution treatment mortality cohort studies meta-analysis | refused (429) |
| H9 | methadone buprenorphine retention all-cause overdose mortality review | 20 hits, 3 retained for this map (Bell 2009 ×2; Larney 2020 noted and carried to the Prescription-opioids map) |
| H10 | Sordo mortality during after opioid substitution treatment BMJ | transient target error |
| H11 | mortality during and after opioid substitution treatment systematic review | transient target error — **Sordo 2017 not located; recorded under Known gaps** |
| H12 | opioid agonist treatment all-cause overdose mortality cohort review | 20 hits, 6 retained (Santo 2021; Pearce 2020; Rogeberg 2021; Domzaridou 2022; Larney 2023; Holmén 2026) |
| H13 | heroin assisted treatment injectable diacetylmorphine randomised trial | transient target error; re-run as H14 |
| H14 | supervised injectable heroin diacetylmorphine maintenance clinical trial | 20 hits, 7 retained (Strang 2010 RIOTT; Strang 2000; Strang 2004; Hartnoll 1980; Bell 2016; Dürsteler-MacFarland 2010; Halbsguth 2008) |
| H15 | Oviedo-Joekes diacetylmorphine hydromorphone chronic opioid addiction | refused (429); re-run as H16 |
| H16 | diacetylmorphine versus methadone opioid addiction NAOMI SALOME trial | 20 hits, 5 retained (Oviedo-Joekes 2009 NAOMI; NEJM 2009 correspondence; Nosyk 2012; Marchand 2011; Oviedo-Joekes 2010, 2015). SALOME main results (2016) not surfaced |
| H17 | supervised injection facility drug consumption room evaluation overdose | transient target error; re-run as H18 |
| H18 | supervised consumption sites systematic review overdose Vancouver Insite | 20 hits, 8 retained (Gariépy 2025 **+ 2026 corrigendum**; Panagiotoglou 2022; Kinshella 2018; Cho 2022; Notta 2019; Kennedy 2017; Boyd 2018; Olding 2023; Kennedy 2019 Soc Sci Med; Barry 2018) |
| H19 | Hser 33-year follow-up narcotics addicts natural history heroin use | 20 hits, 10 retained (Hser 1993, 1994, 2001, 2007 ×2; Oppenheimer 1994; Stimson 1978; Oppenheimer 1979; Wille 1981; Goldstein 1995; Vaillant 1966; Smyth 2007) |
| H20 | mortality among people who inject drugs opioid dependence meta-analysis | refused (429); re-run as H21 |
| H21 | global burden mortality cohort studies people who inject drugs Degenhardt | 20 hits, 9 retained (Mathers 2013, 2014; Nelson 2011, 2023; Larney 2017; Kennedy 2019 PLOS Med; Degenhardt 2010; Gibson 2011; Hill 2022; Kimber 2018; Sarker 2023; Morgan 2024) |
| H22 | mortality regular dependent users heroin other opioids cohort studies | 20 hits, 5 retained (Degenhardt 2011 SR/MA; Darke 1995; Shand 2011; Lopez-Quintero 2015; Huang 2013; Lee 2013; Stogner 2014) |
| H23 | illicitly manufactured fentanyl heroin supply overdose deaths epidemiology | transient target error — covered in the Fentanyl-and-analogues map |
| H24 | opioid induced respiratory depression mechanisms naloxone reversal review | refused (429) |
| H25 | opioid respiratory depression pathophysiology Dahan naloxone limitations | transient target error |
| H26 | opioid induced respiratory depression mechanisms clinical review | transient target error |
| H27 | respiratory depression opioids ventilatory control humans pharmacology | refused (429) — **overdose respiratory physiology not covered by Crossref in this session; recorded under Known gaps** |
| H28 | heroin smoking chasing the dragon route transition injecting | 20 hits, 7 retained (Strang 1997; Gossop 1988; De La Fuente 1997; Gervin 2001; Hendriks 2001; Dubois 2013; Morgan 2019; Gupta 2009) |
| H29 | fatal heroin overdose mechanisms review Darke Zador White Irvine | refused (429); re-run as H30 |
| H30 | fatal heroin overdose toxicology circumstances review Darke | 20 hits, 12 retained (Darke & Zador 1996; Darke 2003 + Neale 2003 reply; Warner-Smith 2002; Darke 2016 ×2; Darke 1999; Darke 1996 Sydney I and II; Darke 2002, 2005, 2007, 2010 ×2; McGregor 1998; Stam 2018) |
| H31 | heroin users cognitive impairment neuropsychological performance review | 20 hits, 0 retained (returned dementia and MCI literature); re-run as H32 |
| H32 | neuropsychological consequences chronic opioid use meta-analysis Baldacchino | 20 hits, 7 retained (Baldacchino 2012; Baldacchino 2017; Baldacchino 2014 **+ 2015 erratum**; Hemmati 2022; Delorme 2023; Kakko 2019; Schofield 2025) |

### DOI corrections and update checks

- No DOI was written from memory; every DOI in the list was copied from a Crossref response in this session. No DOI therefore needed a `works/<DOI>` re-fetch, and none was dropped for resolving to a different paper.
- Crossref holds duplicate DOI records for four Addiction articles of the 1990s (Darke & Zador 1996; Darke 1996 Sydney I and II; Strang 1997; De La Fuente 1997). The more heavily cited `10.1111/j.1360-0443...` record was listed in each case.
- Corrections found in the search records: Gariépy et al. 2025 supervised-consumption-site systematic review has a 2026 corrigendum (10.24095/hpcdp.46.2.04); Baldacchino et al. 2014 intrauterine opioid exposure meta-analysis has a 2015 erratum (10.1186/s12888-015-0438-5). Both are listed as separate items and both documents are to be obtained.
- Retraction field (`updated-by`) was not read, because no `works/<DOI>` fetches were made. The Retraction Watch check (METHODS §4.3) is therefore still outstanding for all 119 items.

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed. For each: **Save → Selection: All results → Format: CSV** into `search-logs/` with the name given; note the hit count.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `(heroin[Title] OR diacetylmorphine[Title] OR diamorphine[Title]) AND (pharmacokinetic* OR bioavailability OR "6-monoacetylmorphine" OR metabolism) AND humans[MeSH Terms]` | heroin_pubmed_P1.csv | |
| P2 | `(heroin[Title/Abstract] OR "opioid overdose"[Title]) AND ("respiratory depression" OR "mechanism of death" OR hypoxia OR "chest wall rigidity") AND humans[MeSH Terms]` | heroin_pubmed_P2.csv | |
| P3 | `(heroin[Title] OR opioid*[Title]) AND overdose[Title] AND (risk factor* OR tolerance OR polydrug OR benzodiazepine* OR alcohol) AND humans[MeSH Terms]` | heroin_pubmed_P3.csv | |
| P4 | `(naloxone[Title]) AND ("take-home" OR distribution OR "overdose education" OR community OR bystander) AND (mortality OR death* OR outcome* OR "systematic review"[Publication Type])` | heroin_pubmed_P4.csv | |
| P5 | `("opioid substitution"[Title/Abstract] OR "opioid agonist treatment"[Title/Abstract] OR methadone[Title] OR buprenorphine[Title]) AND mortality[Title] AND (cohort OR "meta-analysis"[Publication Type])` | heroin_pubmed_P5.csv | |
| P6 | `("supervised injection" OR "supervised consumption" OR "drug consumption room" OR "overdose prevention site"[Title/Abstract]) AND (overdose OR mortality OR evaluation OR "systematic review"[Publication Type])` | heroin_pubmed_P6.csv | |
| P7 | `(heroin[Title] OR diamorphine[Title] OR diacetylmorphine[Title]) AND (prescribing OR maintenance OR "assisted treatment") AND (randomized controlled trial[Publication Type] OR "systematic review"[Publication Type])` | heroin_pubmed_P7.csv | |
| P8 | `(heroin[Title] OR "opioid dependence"[Title]) AND ("natural history" OR remission OR recovery OR trajector* OR "follow-up studies"[MeSH Terms]) AND humans[MeSH Terms]` | heroin_pubmed_P8.csv | |
| P9 | `("people who inject drugs" OR "injecting drug use*") AND (HIV OR "hepatitis C" OR endocarditis OR "skin and soft tissue infection" OR botulism) AND (prevalence OR incidence OR "systematic review"[Publication Type])` | heroin_pubmed_P9.csv | |
| P10 | `(heroin[Title]) AND (smoking OR inhalation OR "chasing the dragon" OR route) AND (transition OR pharmacokinetic* OR leukoencephalopathy OR outcome*)` | heroin_pubmed_P10.csv | |
| P11 | `(heroin[Title] OR "opioid use disorder"[Title]) AND (cognit* OR neuropsycholog* OR neuroimaging OR MRI) AND (chronic OR "long-term" OR abstinen*) AND humans[MeSH Terms]` | heroin_pubmed_P11.csv | |
| P12 | `(heroin OR opioid*) AND (pregnan* OR prenatal OR "neonatal abstinence syndrome" OR "neonatal opioid withdrawal") AND (outcome* OR "systematic review"[Publication Type])` | heroin_pubmed_P12.csv | |
| P13 | `(heroin[Title]) AND (fentanyl OR adulterant* OR purity OR "drug checking" OR "drug supply") AND (death* OR overdose OR market)` | heroin_pubmed_P13.csv | |
| P14 | `(heroin[Title] OR "opioid dependence"[Title]) AND (prison OR incarcerat* OR "post-release") AND (mortality OR overdose OR treatment)` | heroin_pubmed_P14.csv | |

## Layer 3 — Cochrane Library (to be run by VS)

Search, in Cochrane Reviews: `heroin`; `heroin maintenance OR diamorphine prescribing`; `opioid detoxification`; `naloxone overdose`; `needle and syringe programmes`. Export each result set → `heroin_cochrane_<topic>.csv`. Expected core reviews: Ferri, Davoli & Perucci (heroin maintenance); Gowing et al. (opioid withdrawal management; alpha-2 adrenergic agonists; buprenorphine for withdrawal); Amato et al. (psychosocial plus agonist treatment).

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of items 1, 2, 11, 12, 13, 15, 27 and 33 (the reviews and meta-analyses). Forward: "cited by" on items 8, 11, 19, 20, 23, 27 and 29 — in particular to recover Sordo 2017, Marshall 2011 and their critiques, which the Crossref layer failed to surface. Logged here with seed DOI and counts.

## PRISMA counts

To be completed after Layers 2–4. Layer 1 so far: 32 Crossref calls attempted, 15 result sets screened (approximately 290 records), 119 records retained.
