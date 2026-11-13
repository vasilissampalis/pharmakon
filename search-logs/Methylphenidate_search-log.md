# Methylphenidate — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-15 before screening (the plan in the co-editors' scratch file `methylphenidate_queries.md`, 16 section-level and ~45 targeted strings); not altered during screening. Ten of them could be run (see "Operational notes").

## Layer 1 — Crossref bibliographic search (run by AI, 2026-10-16)

Endpoint: `https://api.crossref.org/works?query.bibliographic=<terms>&filter=type:journal-article&rows=<n>&select=DOI,title,container-title,issued,author,updated-by`, relevance order. Every query below returned Crossref's `updated-by` field for each hit, so those hits were checked for retractions and corrections in the same call. Hits screened by title and journal; 59 journal articles retained from these queries, plus 19 methylphenidate-relevant papers returned by the amphetamine and cocaine queries of this session (marked *(amph/coc query)* in the list), giving 78 in `Methylphenidate_DOI-LIST.md`.

| # | Query string (`query.bibliographic=`) | Rows | Retained |
|---|---|---|---|
| MPH1 | methylphenidate cognitive enhancement healthy adults systematic review meta-analysis | 30 | 2 |
| MPH2 | neuroenhancement healthy methylphenidate modafinil prescription stimulants working memory | 30 | 12 |
| MPH3 | methylphenidate dopamine transporter occupancy human brain PET cocaine Volkow | 30 | 12 (+4 cocaine-only PET papers added to `Cocaine_DOI-LIST.md` as items 103–106) |
| MPH4 | comparing the abuse potential of methylphenidate versus other stimulants | 30 | 7 |
| MPH5 | methylphenidate cardiovascular events risk children adults cohort self-controlled | 30 | 4 |
| MPH6 | methylphenidate children adolescents ADHD systematic review Storebo trials adverse | 30 | 5 |
| MPH7 | Storebo methylphenidate Cochrane systematic review meta-analyses randomised clinical trials | 25 | 2 |
| MPH8 | misuse diversion of stimulant medication college students comprehensive review meta-analysis | 30 | 9 |
| MPH9 | methylphenidate pharmacokinetics enantiomers formulations clinical pharmacokinetics review | 30 | 4 |
| MPH10 | long-term outcomes methylphenidate ADHD MTA follow-up ADDUCE safety | 30 | 2 |

Two further queries were refused by the proxy with HTTP 429 and were not re-sent (a refused URL is never re-fetched): "abuse potential of methylphenidate versus other stimulants review Kollins" (replaced by MPH4) and "methylphenidate for ADHD in children and adolescents Cochrane trial sequential analyses" (replaced by MPH7).

**Screening decisions.** Excluded at title/venue stage: *Evidence-Based Mental Health* synopses and *Cochrane Clinical Answers* summaries (secondary digests; the Cochrane review itself is report R1 and its BMJ version is list item 25); news items (*Pharmaceutical Journal*, *BMJ* news, *Alcoholism & Drug Abuse Weekly*); conference abstracts (*European Neuropsychopharmacology*, *JAACAP*, *Pharmacopsychiatry*, *European Psychiatry*, *Endocrine Abstracts* and *Toxicologie Analytique et Clinique* supplements); single case reports; a *Yearbook of Pediatrics* summary; a *Lancet Psychiatry* 2023 comment on the ADDUCE study, held back until the primary ADDUCE article is verified; predatory or non-indexed venues; `Reactions Weekly`, `Inpharma Weekly`, *AAP Grand Rounds* and *Pediatric Neurology Briefs* items; registry stubs; off-topic hits (non-pharmacological cognitive training, other drugs' pharmacokinetics).

**Corrections, retractions and flags.** Two corrections were found through `updated-by` and both parts of each are listed: Shin et al. 2016, *BMJ* (`10.1136/bmj.i2550`, corrected by `10.1136/bmj.i3123`) and Swanson & Volkow 2008, *Nature* (`10.1038/453586a`, corrected by `10.1038/454159c`). No retraction was found among any hit of MPH1–MPH10. No DOI was written from memory, so none needed correcting. Titles in the list echo Crossref's stored titles; where Crossref truncated a title in the response (e.g. Roberts et al. 2020), the table stops where the response stopped.

**Operational notes.** As for the other stimulant logs: `api.crossref.org` is reachable only through WebFetch; HTTP 429 on roughly one call in three at 200–235 s spacing, with the limit shared with other co-editor agents (see the shared `ratelog.txt`); URLs longer than ~250 characters and query terms containing commas or slashes are refused, so "attention-deficit/hyperactivity disorder" was searched as "ADHD".

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed (https://pubmed.ncbi.nlm.nih.gov). For each: **Save → Selection: All results → Format: CSV**, and save the file into `search-logs/` with the name given. Note the hit count PubMed shows next to each string and send me the numbers.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `(methylphenidate[Title] OR dexmethylphenidate[Title]) AND (systematic review[Publication Type] OR meta-analysis[Publication Type])` | methylphenidate_pubmed_P1.csv | |
| P2 | `(methylphenidate[Title] OR "prescription stimulant*"[Title]) AND (healthy OR "cognitive enhancement" OR neuroenhancement OR "smart drug*") AND (humans[MeSH Terms])` | methylphenidate_pubmed_P2.csv | |
| P3 | `(Linssen AM[Author] OR Bagot KS[Author] OR Marraccini ME[Author] OR Repantis D[Author]) AND (methylphenidate OR stimulant*)` | methylphenidate_pubmed_P3.csv | |
| P4 | `(methylphenidate[Title]) AND ("abuse liability" OR "abuse potential" OR self-administration OR "drug discrimination" OR "drug liking") AND (humans[MeSH Terms])` | methylphenidate_pubmed_P4.csv | |
| P5 | `(Kollins SH[Author]) AND (methylphenidate) AND (abuse OR reinforcing OR liability)` | methylphenidate_pubmed_P5.csv | |
| P6 | `(methylphenidate[Title]) AND (cardiovascular OR "myocardial infarction" OR stroke OR arrhythmia OR "sudden death" OR "blood pressure") AND (cohort OR "case-control" OR "self-controlled" OR meta-analysis[Publication Type])` | methylphenidate_pubmed_P6.csv | |
| P7 | `(Cooper WO[Author] OR Habel LA[Author]) AND (ADHD) AND (cardiovascular)` | methylphenidate_pubmed_P7.csv | |
| P8 | `(methylphenidate[Title]) AND (psychosis OR psychotic OR hallucination*) AND (cohort OR "self-controlled" OR "case-control")` | methylphenidate_pubmed_P8.csv | |
| P9 | `("MTA Cooperative Group"[Corporate Author] OR (MTA AND "multimodal treatment") ) AND (follow-up OR "long-term" OR adult)` | methylphenidate_pubmed_P9.csv | |
| P10 | `(ADDUCE OR "Attention Deficit Hyperactivity Disorder Drugs Use Chronic Effects") AND (methylphenidate)` | methylphenidate_pubmed_P10.csv | |
| P11 | `(methylphenidate[Title]) AND (pharmacokinetic* OR enantiomer* OR "d-threo" OR bioavailability OR formulation*) AND (humans[MeSH Terms])` | methylphenidate_pubmed_P11.csv | |
| P12 | `("prescription stimulant*"[Title] OR methylphenidate[Title]) AND (misuse OR "non-medical" OR nonmedical OR diversion) AND (student* OR college OR university OR adolescen*)` | methylphenidate_pubmed_P12.csv | |
| P13 | `(stimulant*[Title] OR methylphenidate[Title]) AND (childhood OR adolescen*) AND ("substance use disorder" OR "later substance use") AND (meta-analysis[Publication Type] OR cohort)` | methylphenidate_pubmed_P13.csv | |
| P14 | `(methylphenidate[Title]) AND (overdose OR poisoning OR "poison center" OR "poison centre" OR intranasal OR intravenous OR injection) ` | methylphenidate_pubmed_P14.csv | |

## Layer 3 — Cochrane Library (to be run by VS)

Search `methylphenidate` in Cochrane Reviews; export the result list as CSV → `methylphenidate_cochrane.csv`. Save the full PDF of the most recent Storebø et al. review as report R1.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of items 1–4, 25, 28 and of the Cochrane review (R1). Forward: Google Scholar "cited by" on Storebø et al. 2015 (item 25) to collect the published exchanges with its critics beyond item 26, on Volkow et al. 1995 and 1998 (items 7–8), and on Moran et al. 2019 (item 23). Logged here with seed DOI and counts.

## PRISMA counts

To be completed after Layers 2–4: records identified per source; duplicates removed; screened; excluded with reasons; included.
