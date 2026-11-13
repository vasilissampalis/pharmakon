# Psilocybin — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-15 before screening; re-worded re-runs of refused URLs are listed as such.

## Layer 1 — Crossref bibliographic search (run by AI co-editor, 2026-10-15)

Endpoint: `https://api.crossref.org/works?query.bibliographic=<terms>&filter=type:journal-article&rows=15&select=DOI,title,container-title,issued,is-referenced-by-count,author&sort=relevance`. Record verification used `https://api.crossref.org/works?filter=doi:A,doi:B,doi:C&select=DOI,title,container-title,issued,updated-by&rows=10`.

Environment notes, relevant to how this log reads:
- Crossref refused roughly half of all calls with HTTP 429 (shared egress). After each refusal the build paused 95–185 s and never re-fetched the refused URL; re-runs used different wording. Nine refusals occurred.
- The proxy rejects URLs longer than about 250 characters, so query strings were kept under ~75 characters. One query (P2a) was lost that way.
- Several calls returned an unexplained client error from Crossref on syntactically valid URLs; where a reworded re-run also failed the topic is recorded as a gap.
- **Batch verification works and was used**: `filter=doi:` with three DOIs per request resolved correctly and returned `updated-by`. Four DOIs per request intermittently errored and five DOIs per request silently dropped the filter and returned an unfiltered result set, so three per request is the working limit. DOIs containing parentheses (Elsevier/Lancet PII form) failed in this filter both raw and percent-encoded.
- Direct `curl` to api.crossref.org is blocked by the egress proxy; WebFetch is the only route.

### Section-level queries

| # | Query string | Result |
|---|---|---|
| P1 | psilocybin treatment-resistant depression randomized controlled trial | 15 hits, 1 retained (Gukasyan 2023 critique). Crossref relevance swamped by news items and unrelated neurostimulation trials; superseded by the title-level queries below |
| P2 | Carhart-Harris trial of psilocybin versus escitalopram for depression | 15 hits, 10 retained (Carhart-Harris 2021 NEJM; Szigeti 2024; Weiss 2023a and 2023b + corrigendum; Nayak 2023; Erritzoe 2024a and 2024b; Barba 2022; Deco 2024; Martens 2025; Henry 2025) — highest-yield query of the build |
| P2a | Goodwin single-dose psilocybin for a treatment-resistant episode of major depression | URL refused (over length), then refused (429) on the shortened re-run; Goodwin 2022 NEJM obtained instead by `filter=doi:` verification |
| P3 | COMP360 psilocybin phase II trial depression | 15 hits, 0 retained — all Neuroscience Applied conference abstracts of the same trial, plus news items |
| P4 | Raison psilocybin major depressive disorder randomized clinical trial | 15 hits, 2 retained (Davis 2021 JAMA Psychiatry; Luquiens 2025 Addiction). Raison 2023 itself not surfaced; obtained by `filter=doi:` |
| P5 | psychedelic trials blinding expectancy placebo response problem | 15 hits, 6 retained (Muthukumaraswamy 2021; Schenberg 2021; Huneke 2025; Nayak 2025; Szigeti 2024b; Vanderijst 2026) |
| P6 | psilocybin adverse events harms reporting systematic review | 15 hits, 1 retained (Roscoe 2022); the rest were harms-reporting methodology in unrelated fields |
| P6a | adverse events classic psychedelics MDMA systematic review meta-analysis | URL refused (429); re-run as P6b |
| P6b | adverse events serotonergic psychedelics treatments mixed-methods review | 15 hits, 3 retained (Breeksema 2022; Hinkle 2024; Malcolm 2021) |
| P7 | Griffiths psilocybin dose effects mystical-type experience healthy | client error; re-run as "psilocybin dose-related effects mystical-type experience volunteers" also client error; re-run as P7c |
| P7c | psilocybin dose mystical experience healthy volunteers Griffiths | 15 hits, 9 retained (Griffiths 2011; Barrett 2015; Johnson 2012; MacLean 2012; Studerus 2012; Carbonaro 2017; Garcia-Romeu 2015; and the four 2006 commentaries by Nichols, Snyder, Kleber and Schuster) |
| P8 | psilocybin psilocin pharmacokinetics oral plasma humans | client error; re-run as P8b |
| P8b | psilocin pharmacokinetics plasma concentrations oral psilocybin dose | 15 hits, 4 retained (Hasler 1997; Madsen 2020; Otto 2025 + its correction; Tai 2026) |
| P9 | acute psychological physiological effects psilocybin healthy humans dose | 15 hits, 3 retained (Hasler 2004; Studerus 2010; Burmester 2023) |
| P10 | human hallucinogen research guidelines safety Johnson Griffiths | 15 hits, 2 retained (Johnson 2008; MacLean 2011) |
| P11 | challenging experiences psilocybin mushrooms survey difficult bad trips | URL refused (429); re-run as P11b |
| P11b | challenging experiences after psilocybin mushrooms survey Carbonaro | 15 hits, 4 retained (Carbonaro 2016; Barrett 2016; Barrett 2017; Benjamin 1979). Three further Carbonaro items were DAD conference abstracts and were dropped |
| P12 | extended difficulties persisting negative effects following psychedelic use | 15 hits, 6 retained (Evans 2023; Robinson 2025; Argyri 2025; Olofsson 2026; Zhou 2025; Ehrenkranz 2026) |
| P13 | mushroom poisoning misidentification amatoxin foragers epidemiology | 15 hits, 2 retained (Trabulus 2011; Dimitrova 2026); nothing specific to psilocybin-mushroom foraging |
| P13b | magic mushroom foragers misidentified toxic species poisoning cases | 15 hits, 0 retained (1935–1975 case reports and PCR species-identification methods) — recorded as a gap |
| P14 | 4-acetoxy-DMT psilacetin tryptamine new psychoactive substance analysis | URL refused (429); re-run as P14b |
| P14b | 4-AcO-DMT O-acetylpsilocin psilocybin analogue tryptamines human | 15 hits, 4 retained (Zhai 2022; Simonsson 2026 JAMA Netw Open; Kase 2026; Hepburn 2025; plus Lancelotta 2022 noted for the 5-MeO-DMT list) |
| P15 | psilocybin brain network functional connectivity fMRI human desynchronization | URL refused (429); re-run as "psilocybin resting state functional connectivity human brain imaging": 15 hits, 0 retained (query swamped by generic neuroimaging-methods papers). Neuroimaging landmarks obtained instead by DOI verification (Carhart-Harris 2012; Siegel 2024; Daws 2022) |
| P16 | neural correlates psychedelic state psilocybin fMRI Carhart-Harris | client error; re-run as "psilocybin desynchronizes human brain precision functional mapping": 15 hits, 1 retained (Siegel 2024 Biol Psychiatry abstract — dropped as an abstract; the Nature paper was taken from DOI verification instead) |
| P17 | psilocybin exposures poison centers trends United States use prevalence | 15 hits, 1 retained (Farah 2024) |
| P18 | trends in hallucinogen psilocybin use among adults national survey | URL refused (429); re-run as "trends psilocybin hallucinogen use adults national survey epidemiology": client error — epidemiology recorded as a gap |

### Record verification (`filter=doi:`, three DOIs per request)

| Batch | DOIs | Result |
|---|---|---|
| V1 | 10.1073/pnas.1119598109, 10.1056/nejmoa2206443, 10.1001/jama.2023.14530 | total-results 3; response truncated by the fetcher because of long author lists — re-run without `author` in `select` |
| V2 | 10.1001/jama.2023.14530, 10.1007/s00213-006-0457-5, 10.1038/s41586-024-07624-5 | 3/3 resolved to the intended papers; no `updated-by` on any |
| V3 | 10.1073/pnas.1119598109, 10.1038/s41591-022-01744-z, 10.1016/s2215-0366(16)30065-7 | client error, both raw and with the parentheses percent-encoded; re-run as V4 without the Lancet DOI |
| V4 | 10.1073/pnas.1119598109, 10.1038/s41591-022-01744-z, 10.1001/jamapsychiatry.2022.2096 | 3/3 resolved; no `updated-by` |
| V5 | 10.1177/0269881116675513, 10.1177/0269881116675512, 10.1177/0269881114548296 | refused (429); re-run after 120 s, then 3/3 resolved; no `updated-by` |
| — | 10.1056/nejmoa2206443 | resolved in V1 (Goodwin 2022, NEJM, title confirmed) |

### DOI corrections and update checks
- No recalled DOI was written into the list without a `filter=doi:` check; every other DOI was copied verbatim from a Crossref search response.
- Dropped for non-verification: 10.1016/s2215-0366(16)30065-7 (Carhart-Harris 2016, Lancet Psychiatry). See the DOI list's "Known gaps".
- `updated-by`/correction records found: Weiss 2023 personality-change paper has a published CORRIGENDUM registered as its own record (10.1017/s0033291723002039); Otto 2025 psilocin pharmacokinetics review has a published Correction registered as its own record (10.1007/s40262-025-01487-3). Both parent papers are kept and marked.
- Retractions: none.
- Duplicate records noted and not listed twice: Barrett 2015 MEQ30 appears both as the J Psychopharmacol article (listed) and as a Drug Alcohol Depend conference abstract (10.1016/j.drugalcdep.2015.07.961, dropped); Carbonaro's challenging-experiences work appears as three further DAD abstracts (dropped).

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed (https://pubmed.ncbi.nlm.nih.gov). For each: **Save → Selection: All results → Format: CSV**, and save the file into `search-logs/` with the name given. Note the hit count shown next to each string and send me the numbers.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `(psilocybin[Title] OR psilocin[Title] OR "psilocybin mushrooms"[Title]) AND (systematic review[Publication Type] OR meta-analysis[Publication Type] OR "systematic review"[Title] OR "meta-analysis"[Title])` | psilocybin_pubmed_P1.csv | |
| P2 | `(psilocybin[Title]) AND (randomized controlled trial[Publication Type]) AND (humans[MeSH Terms])` | psilocybin_pubmed_P2.csv | |
| P3 | `(psilocybin[Title]) AND (blinding OR unblinding OR expectancy OR expectation OR "placebo response" OR "functional unblinding")` | psilocybin_pubmed_P3.csv | |
| P4 | `(psilocybin[Title] OR psilocin[Title]) AND (pharmacokinetic* OR bioavailability OR "plasma concentration" OR metabolism OR "4-hydroxyindole") AND (humans[MeSH Terms])` | psilocybin_pubmed_P4.csv | |
| P5 | `(psilocybin[Title]) AND (dose OR "dose-response" OR "dose-effect") AND ("healthy volunteers"[MeSH Terms] OR "healthy subjects")` | psilocybin_pubmed_P5.csv | |
| P6 | `(psilocybin[Title] OR psychedelic*[Title]) AND (adverse OR harms OR "side effects" OR safety OR tolerability) AND (humans[MeSH Terms])` | psilocybin_pubmed_P6.csv | |
| P7 | `(psilocybin[Title] OR psychedelic*[Title]) AND (cardiovascular OR "blood pressure" OR hypertension OR QT OR valvulopathy OR "heart valve" OR "5-HT2B")` | psilocybin_pubmed_P7.csv | |
| P8 | `(psychedelic*[Title] OR psilocybin[Title] OR hallucinogen*[Title]) AND ("challenging experience" OR "bad trip" OR "extended difficulties" OR "persisting" OR "prolonged")` | psilocybin_pubmed_P8.csv | |
| P9 | `(psilocybin[Title] OR hallucinogen*[Title]) AND (psychosis OR "psychotic" OR HPPD OR "perception disorder") AND (humans[MeSH Terms])` | psilocybin_pubmed_P9.csv | |
| P10 | `("psilocybe"[Title] OR "magic mushroom*"[Title] OR "psilocybin mushroom*"[Title]) AND (poisoning OR misidentification OR amatoxin OR Galerina OR Cortinarius OR Amanita)` | psilocybin_pubmed_P10.csv | |
| P11 | `("4-AcO-DMT" OR "O-acetylpsilocin" OR psilacetin OR "4-acetoxy-N,N-dimethyltryptamine")` | psilocybin_pubmed_P11.csv | |
| P12 | `(psilocybin[Title] OR hallucinogen*[Title]) AND (prevalence OR trends OR epidemiolog* OR "national survey" OR NSDUH) AND (humans[MeSH Terms])` | psilocybin_pubmed_P12.csv | |
| P13 | `(psilocybin[Title]) AND (serotonin syndrome OR "serotonin toxicity" OR SSRI OR antidepressant OR lithium OR interaction)` | psilocybin_pubmed_P13.csv | |
| P14 | `(psilocybin[Title]) AND (pregnan* OR lactation OR breastfeeding OR adolescen* OR "older adults")` | psilocybin_pubmed_P14.csv | |

## Layer 3 — grey literature (VS)

UNODC World Drug Report 2025; EUDA European Drug Report 2026 and Statistical Bulletin; SAMHSA NSDUH 2024 detailed tables; Monitoring the Future latest; Global Drug Survey latest; Oregon Health Authority Psilocybin Services annual data; ACMD advice on rescheduling psilocybin for research; WEDINOS annual report. Saved to `PDFs/_Epidemiology/` with the names in the DOI list's reports table.
