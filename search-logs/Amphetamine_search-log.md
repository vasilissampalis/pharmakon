# Amphetamine — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-16 before screening; not altered during screening. Scope note: prescribed amphetamine salts and lisdexamfetamine, plus non-medical and illicit amphetamine. Methamphetamine is covered by its own log; pooled "amphetamine-type stimulant" papers are logged in both.

## Layer 1 — Crossref bibliographic search (run by AI, 2026-10-16)

Endpoint: `https://api.crossref.org/works?query.bibliographic=<terms>&filter=type:journal-article&rows=<n>&select=DOI,title,container-title,issued,author`, relevance order. Hits screened by title and journal; 50 journal articles retained from this layer (38 from the queries below, plus 12 amphetamine-relevant papers returned by the cocaine and MDMA queries of this session), plus 20 carried over from `methamphetamine_DOI-LIST.md` (verified 2026-10-14), giving 70 in `Amphetamine_DOI-LIST.md`.

| # | Query string (`query.bibliographic=`) | Rows | Retained |
|---|---|---|---|
| A1 | psychosis with methylphenidate or amphetamine in patients with ADHD | 30 | 5 |
| A2 | ADHD medications cardiovascular disease risk cohort adults amphetamine | 30 | 3 |
| A3 | ADHD medications and long-term risk of cardiovascular diseases | 25 | 1 |
| A4 | amphetamine enantiomers pharmacokinetics lisdexamfetamine humans dose | 30 | 7 |
| A5 | d-amphetamine subjective effects abuse liability human laboratory | 30 | 7 |
| A6 | non-medical use of prescription stimulants students prevalence review | 30 | 7 |
| A7 | amphetamine treatment therapeutic doses neurotoxicity brain behavior review | 30 | 4 |
| A8 | comparative efficacy tolerability medications ADHD network meta-analysis | 25 | 1 |

Eight queries were run rather than the twelve planned, because of the rate limiting described under "Operational notes" in `Cocaine_search-log.md` (the same constraint applied throughout). Two further planned queries — on amphetamine withdrawal, and on childhood stimulant treatment and later substance use disorder — were not run and are carried into the PubMed layer.

**Screening decisions.** Excluded at title/venue stage: trade-press digests (*Brown University Psychopharmacology Update*, *Inpharma Weekly*, *Reactions Weekly*, *AAP Grand Rounds*); JAMA Medical News items (including the 2023 news piece whose subject is the cohort study retained as item 4); letters, replies and commentary in JAMA and *Lancet Psychiatry*; the *Schizophrenia Bulletin* conference abstract of Moran et al. 2019 in favour of the NEJM paper; ClinicalTrials.gov registry stubs; three identical reprints of one *Pediatric Annals*/*Psychiatric Annals* review; a duplicate Crossref record of Krishnan & Zhang 2008 carrying a different publication year; opinion pieces and predatory venues; and animal-only pharmacology from the neurotoxicity query, except where the animal study is itself the subject of the contested claim.

**Corrections, retractions and flags.** Two retained papers carry published errata and both parts are listed: Berman et al. 2009, *Molecular Psychiatry* (erratum `10.1038/mp.2010.39`) and Lee et al. 2018 (erratum recorded on 2026-10-14). One retracted paper was encountered and excluded: Che et al., "Comparative efficacy and acceptability of nonpharmacotherapy in the treatment of inattention for ADHD: a network meta-analysis", *Complexity* 2021 (`10.1155/2021/9435262`), retracted 2023 (`10.1155/2023/9762653`); it concerns non-pharmacological treatment and is not needed for this monograph. No DOI was written from memory, so none needed correcting.

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed (https://pubmed.ncbi.nlm.nih.gov). For each: **Save → Selection: All results → Format: CSV**, and save the file into `search-logs/` with the name given. Note the hit count PubMed shows next to each string and send me the numbers.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `(amphetamine[Title] OR dexamphetamine[Title] OR dextroamphetamine[Title] OR lisdexamfetamine[Title]) AND (systematic review[Publication Type] OR meta-analysis[Publication Type])` | amphetamine_pubmed_P1.csv | |
| P2 | `(Cortese S[Author]) AND (ADHD) AND (network meta-analysis OR meta-analysis[Publication Type])` | amphetamine_pubmed_P2.csv | |
| P3 | `(amphetamine[Title] OR "prescription stimulant"[Title]) AND (cardiovascular OR "myocardial infarction" OR stroke OR hypertension OR "sudden death") AND (cohort OR "case-control" OR "self-controlled")` | amphetamine_pubmed_P3.csv | |
| P4 | `(Habel LA[Author] OR Westover AN[Author]) AND (stimulant* OR amphetamine)` | amphetamine_pubmed_P4.csv | |
| P5 | `(amphetamine[Title]) AND (psychosis OR psychotic) AND (humans[MeSH Terms])` | amphetamine_pubmed_P5.csv | |
| P6 | `(Ricaurte GA[Author]) AND (amphetamine) AND (nonhuman primates OR baboon OR squirrel monkey OR striatum)` | amphetamine_pubmed_P6.csv | |
| P7 | `(amphetamine[Title] OR lisdexamfetamine[Title]) AND (pharmacokinetic* OR bioavailability OR enantiomer* OR "d-amphetamine") AND (humans[MeSH Terms])` | amphetamine_pubmed_P7.csv | |
| P8 | `(amphetamine[Title] OR "mixed amphetamine salts"[Title]) AND ("abuse liability" OR "subjective effects" OR self-administration OR "drug discrimination") AND (humans[MeSH Terms])` | amphetamine_pubmed_P8.csv | |
| P9 | `("prescription stimulant*"[Title] OR amphetamine[Title]) AND (nonmedical OR "non-medical" OR misuse OR diversion) AND (prevalence OR survey OR cohort)` | amphetamine_pubmed_P9.csv | |
| P10 | `(amphetamine[Title]) AND (withdrawal OR dependence OR "use disorder") AND (humans[MeSH Terms])` | amphetamine_pubmed_P10.csv | |
| P11 | `(stimulant*[Title]) AND (childhood OR adolescen*) AND ("substance use disorder" OR "later substance use") AND (meta-analysis[Publication Type] OR cohort)` | amphetamine_pubmed_P11.csv | |
| P12 | `(amphetamine[Title]) AND (pregnan* OR prenatal OR neonatal)` | amphetamine_pubmed_P12.csv | |
| P13 | `(amphetamine[Title]) AND (purity OR adulterant* OR "drug checking" OR caffeine) AND (Europe OR seizure*)` | amphetamine_pubmed_P13.csv | |
| P14 | `(amphetamine[Title]) AND (inject* ) AND (mortality OR "blood-borne" OR HIV OR "hepatitis C")` | amphetamine_pubmed_P14.csv | |

## Layer 3 — Cochrane Library (to be run by VS)

Search `amphetamine` and `lisdexamfetamine` in Cochrane Reviews; export the result lists as CSV → `amphetamine_cochrane.csv`.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of items 1, 4, 5, 8, 10, 13, 25, 26. Forward: Google Scholar "cited by" on Moran et al. 2019 (item 1) — the replication and critique literature on the amphetamine-versus-methylphenidate psychosis difference is the core of a contested-questions box — and on Berman et al. 2009 (item 8). Logged here with seed DOI and counts.

## PRISMA counts

To be completed after Layers 2–4: records identified per source; duplicates removed; screened; excluded with reasons; included.
