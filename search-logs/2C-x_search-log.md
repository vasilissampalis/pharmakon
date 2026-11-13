# 2C-x (2C-series phenethylamines and NBOMe derivatives) — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-16 before screening; re-worded re-runs of refused or errored URLs are listed as such.

## Layer 1 — Crossref bibliographic search (run by AI co-editor, 2026-10-16)

Endpoint: `https://api.crossref.org/works?query.bibliographic=<terms>&filter=type:journal-article&rows=15&select=DOI,title,container-title,issued,is-referenced-by-count,author&sort=relevance`.

Environment: about half of all Crossref calls in this build were refused with HTTP 429 or returned an unexplained client error; each refusal was followed by a 65–185 s pause and the refused URL was never re-fetched.

Search note worth recording for the next co-editor: **Crossref's bibliographic index does not handle "2C-B" as a token.** A query containing it returns pharmacology papers about healthy volunteers with no relation to the compound (see X1). Queries must either spell the compound out ("4-bromo-2,5-dimethoxyphenethylamine"), use the series name ("2C-series"), or pair "2C-B" with a distinctive co-term such as an author group or a comparator drug (X3 worked this way).

### Section-level queries

| # | Query string | Result |
|---|---|---|
| X1 | 2C-B human pharmacology healthy volunteers clinical trial Papaseit | 15 hits, 0 retained — every hit was an unrelated healthy-volunteer pharmacology paper (rifabutin, esomeprazole, trazodone). "2C-B" was not matched as a term |
| X1b | 4-bromo-2,5-dimethoxyphenethylamine 2C-B human pharmacology subjective effects | client error |
| X2 | human pharmacology of 2C-B psychedelic phenethylamine oral doses | 15 hits, 7 retained (Theobald 2007; Forrester 2013; Dean 2013; Zuba 2012; Wagmann 2018; de Boer 2004; Wagmann 2019) |
| X2b | 2C-B controlled administration humans pharmacokinetics Papaseit Farre | URL refused (429). **The Spanish 2C-B human studies were never surfaced** — the largest gap in this map |
| X3 | 2C-B acute effects randomized crossover healthy participants Liechti | 15 hits, 2 retained (Holze 2026 Biol Psychiatry; Arikci 2026 Neuropsychopharmacology) — the only two controlled human administration studies of any 2C compound. The query also surfaced the Basel group's mescaline and psilocybin safety-pharmacology abstracts, noted for the Mescaline list |
| X4 | 25I-NBOMe fatalities deaths intoxication case series toxicology | 15 hits, 9 retained (Rose 2013; Hill 2013; Hermanns-Clausen 2017; Shanks 2015; Poklis 2015; Lowe 2015; Kueppers 2015; Stellpflug 2013; Kamińska 2020) |
| X5 | NBOMe sold as LSD blotter drug checking samples misrepresented | 15 hits, 7 retained (Poklis 2015 [already held]; Lützen 2020; Remy 2015; Magalhães 2019; Grafinger 2018; Bodeau 2017; Suzuki 2014; Coney 2017) |
| X6 | NBOMe vasoconstriction ischemia rhabdomyolysis seizures clinical toxicity | 15 hits, 3 retained (Gee 2015; Wood 2015; Waldman 2018). **No vasoconstriction or limb-ischaemia case report surfaced** — recorded as a gap; the term appears to be indexed under "vasospasm" or in case reports without it in the title |
| X7 | 2C-T-7 deaths Curtis fatal phenethylamine | **Not run** (window closed) |
| X8 | 25I-NBOMe receptor pharmacology 5-HT2A binding in vitro Rickli | **Not run** (window closed) |

### DOI corrections and update checks
- No DOI in this list was recalled from memory; all were copied verbatim from Crossref search responses, so no `works/<DOI>` re-fetch was required.
- Duplicate record noted and not listed twice: Hill et al.'s 25I-NBOMe case series is registered both in Clinical Toxicology (10.3109/15563650.2013.802795, listed) and as a J Emerg Med reprint abstract (10.1016/j.jemermed.2013.10.018, dropped).
- Erratum found on an excluded item: Kawahara et al. 2017, "The psychoactive drug 25B-NBOMe recapitulates rhabdomyolysis in zebrafish larvae" (Forensic Toxicol) has an erratum at 10.1007/s11419-017-0383-8; both were excluded as preclinical.
- Venue exclusions logged under METHODS §3.2: Lipow 2022 in *Transformative Medicine* and "25I-NBOMe N-bomb" in *Drug Designing: Open Access* — neither is in DOAJ/MEDLINE and neither could be checked from here.
- Retractions: none.

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed (https://pubmed.ncbi.nlm.nih.gov). For each: **Save → Selection: All results → Format: CSV**, and save the file into `search-logs/` with the name given. Note the hit count shown next to each string and send me the numbers. P1 and P2 are the two that matter most — they should recover the Spanish 2C-B human studies that Crossref would not surface.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `("2C-B"[Title/Abstract] OR "4-bromo-2,5-dimethoxyphenethylamine"[Title/Abstract] OR nexus[Title/Abstract]) AND (humans[MeSH Terms])` | 2cx_pubmed_P1.csv | |
| P2 | `("2C-B" OR "2C-I" OR "2C-E" OR "2C-T-2" OR "2C-T-7" OR "2C-P" OR "2C series" OR "2C-series")` | 2cx_pubmed_P2.csv | |
| P3 | `(NBOMe[Title/Abstract] OR "25I-NBOMe" OR "25B-NBOMe" OR "25C-NBOMe" OR "N-bomb"[Title/Abstract]) AND (humans[MeSH Terms])` | 2cx_pubmed_P3.csv | |
| P4 | `(NBOMe OR "25I-NBOMe" OR "25B-NBOMe") AND (death OR deaths OR fatal* OR mortality OR postmortem OR "post-mortem")` | 2cx_pubmed_P4.csv | |
| P5 | `(NBOMe OR "2C-B" OR "2C-I" OR phenethylamine) AND (vasoconstrict* OR vasospasm OR ischemi* OR ischaemi* OR "limb ischemia")` | 2cx_pubmed_P5.csv | |
| P6 | `(NBOMe OR "2C-B" OR "2C series") AND (seizure* OR rhabdomyolysis OR hyperthermia OR agitation OR "excited delirium")` | 2cx_pubmed_P6.csv | |
| P7 | `("drug checking" OR "drug-checking" OR "pill testing" OR blotter) AND (NBOMe OR LSD OR "2C-B") AND (adulterant* OR mis-sold OR substitution OR misrepresent*)` | 2cx_pubmed_P7.csv | |
| P8 | `("2C-B" OR "2C-I" OR NBOMe) AND (pharmacokinetic* OR metabolism OR "in vitro" OR CYP OR "monoamine oxidase")` | 2cx_pubmed_P8.csv | |
| P9 | `("2C-B" OR NBOMe OR "2C series") AND (receptor OR "5-HT2A" OR binding OR affinity OR agonist)` | 2cx_pubmed_P9.csv | |
| P10 | `(NBOMe OR "2C-B" OR "2C series" OR "novel psychoactive") AND ("emergency department" OR "Euro-DEN" OR presentations OR poison*)` | 2cx_pubmed_P10.csv | |
| P11 | `(NBOH OR "25I-NBOH" OR "25B-NBOH" OR "NBOH")` | 2cx_pubmed_P11.csv | |
| P12 | `("2C-B" OR "2C-I" OR NBOMe) AND (prevalence OR trends OR survey OR epidemiolog*)` | 2cx_pubmed_P12.csv | |

## Layer 3 — grey literature (VS)

This substance leans on grey literature more than most: the EMCDDA risk-assessment reports and the WHO ECDD critical reviews are the only systematic syntheses of the European and global case data. Obtain R1–R9 as listed in the DOI list's reports table, into `PDFs/_Epidemiology/`.
