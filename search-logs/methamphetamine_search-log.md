# Methamphetamine — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-14 before screening; not to be altered during screening.

## Layer 1 — Crossref bibliographic search (run by AI, 2026-10-14)

14 section-level queries, 15–20 results each, `type:journal-article`, relevance-sorted; plus 10 targeted author/title queries to resolve landmark DOIs. Hits screened by title; 86 journal articles retained into `methamphetamine_DOI-LIST.md`. Two recalled DOIs were found to be wrong on verification (Marshall & Werb 2010; Herbeck 2015) and corrected from Crossref; one recalled DOI resolved to an editorial rather than the trial (Roll et al. 2006) and was corrected. Two retained papers carry published errata (Degenhardt et al. 2018; Lee et al. 2018); none is retracted.

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed (https://pubmed.ncbi.nlm.nih.gov). For each: **Save → Selection: All results → Format: CSV**, and save the file into `search-logs/` with the name given. Note the hit count shown by PubMed next to each string below and send me the numbers.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `(methamphetamine[Title]) AND (systematic review[Publication Type] OR meta-analysis[Publication Type] OR "systematic review"[Title] OR "meta-analysis"[Title])` | methamphetamine_pubmed_P1.csv | |
| P2 | `(methamphetamine[Title]) AND (cognit* OR neuropsycholog* OR memory OR executive) AND (humans[MeSH Terms]) AND ("2017"[Date - Publication] : "3000"[Date - Publication])` | methamphetamine_pubmed_P2.csv | |
| P3 | `(methamphetamine[Title]) AND (PET OR "positron emission" OR MRI OR "magnetic resonance" OR neuroimaging OR "dopamine transporter") AND (humans[MeSH Terms])` | methamphetamine_pubmed_P3.csv | |
| P4 | `(methamphetamine[Title]) AND (psychosis OR psychotic OR schizophrenia) AND (humans[MeSH Terms]) AND ("2015"[Date - Publication] : "3000"[Date - Publication])` | methamphetamine_pubmed_P4.csv | |
| P5 | `(methamphetamine[Title]) AND (cardiomyopathy OR "heart failure" OR stroke OR cardiovascular OR "pulmonary hypertension") AND (humans[MeSH Terms]) AND ("2015"[Date - Publication] : "3000"[Date - Publication])` | methamphetamine_pubmed_P5.csv | |
| P6 | `(methamphetamine[Title] OR amphetamine[Title]) AND (mortality OR death OR "cause of death") AND (cohort OR registry OR "record linkage") AND (humans[MeSH Terms])` | methamphetamine_pubmed_P6.csv | |
| P7 | `(methamphetamine[Title]) AND (randomized controlled trial[Publication Type]) AND (humans[MeSH Terms])` | methamphetamine_pubmed_P7.csv | |
| P8 | `(methamphetamine[Title]) AND (pharmacokinetic* OR bioavailability OR "half-life" OR metabolism) AND (humans[MeSH Terms])` | methamphetamine_pubmed_P8.csv | |
| P9 | `(methamphetamine[Title]) AND ("harm reduction" OR "drug checking" OR "safer smoking" OR pipe OR overamping OR naloxone) AND (humans[MeSH Terms])` | methamphetamine_pubmed_P9.csv | |
| P10 | `(methamphetamine[Title]) AND (prevalence OR epidemiolog* OR trends OR "wastewater") AND ("2019"[Date - Publication] : "3000"[Date - Publication]) AND (humans[MeSH Terms])` | methamphetamine_pubmed_P10.csv | |
| P11 | `(methamphetamine[Title]) AND (withdrawal OR abstinence OR craving) AND (humans[MeSH Terms]) AND ("2010"[Date - Publication] : "3000"[Date - Publication])` | methamphetamine_pubmed_P11.csv | |
| P12 | `(methamphetamine[Title]) AND (Parkinson* OR parkinsonism) AND (humans[MeSH Terms])` | methamphetamine_pubmed_P12.csv | |
| P13 | `(methamphetamine[Title]) AND (pregnan* OR prenatal OR neonatal) AND (humans[MeSH Terms]) AND ("2015"[Date - Publication] : "3000"[Date - Publication])` | methamphetamine_pubmed_P13.csv | |
| P14 | `(methamphetamine[Title]) AND (toxicity OR overdose OR hyperthermia OR "emergency department") AND (humans[MeSH Terms]) AND ("2015"[Date - Publication] : "3000"[Date - Publication])` | methamphetamine_pubmed_P14.csv | |

## Layer 3 — Cochrane Library (to be run by VS)

Search `methamphetamine` in Cochrane Reviews; export the result list as CSV → `methamphetamine_cochrane.csv`.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of every Tier-A review. Forward: Google Scholar "cited by" on items 1, 7, 8, 14, 18, 19, 29, 32 (landmarks). Logged here with seed DOI and counts.

## PRISMA counts

To be completed after Layers 2–4: records identified per source; duplicates removed; screened; excluded with reasons; included.
