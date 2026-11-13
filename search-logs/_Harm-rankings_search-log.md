# _Harm-rankings — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-15 before screening; not altered during screening. Searches executed 2026-10-16. Cross-cutting topic treated as a substance for the purposes of the evidence-map brief.

## Layer 1 — Crossref bibliographic search (run by AI co-editor)

All queries run against `https://api.crossref.org/works?query.bibliographic=<terms>&filter=type:journal-article&rows=<n>&select=DOI,title,container-title,issued,author` (relevance-sorted). DOIs taken verbatim from the returned records; none typed from memory, so no `works/<DOI>` re-fetch was needed (evidence-map brief, "Working economically" §3).

A general problem with this topic's queries: the phrase "multicriteria decision analysis" belongs mainly to operations research, so every MCDA query returns a majority of engineering, finance and environmental-science records. The useful signal is in the first few hits and in the drug-journal container names; `rows` was kept at 30–40 so the drug papers would not be crowded out.

| # | Query | rows | Status / hits retained |
|---|---|---|---|
| K1 | drug harms multicriteria decision analysis Nutt ranking misuse classification | 40 | **Not run** — HTTP 429, not re-fetched. |
| K1b | drug harms multicriteria decision analysis ranking classification of harm | 40 | Run (substitute, after a 420 s wait): 40 returned, 6 retained (Nutt 2010; Rolles & Measham 2011; Broman 2025; Wong 2017 and 2018; the Bonomo corrigendum, which led to the article in K2b). Dropped: ~25 non-drug MCDA methods papers, an SSRN preprint, two *Drug Safety* medication-error classification papers, and several harm-reduction papers unrelated to ranking. |
| K2 | European rating of drug harms expert Australian drug harms ranking study | 40 | **Not run** — HTTP 429 twice (the second after a 420 s wait). Not re-fetched. |
| K2b | rating of drug harms experts Europe Australia ranking study psychopharmacology | 40 | Run (substitute, after a 600 s wait): 40 returned, 4 retained (van Amsterdam 2015; Bonomo 2019 **with its corrigendum**; Nutt 2009 "Equasy"; Rolles 2011 again). Dropped: a long run of "Question the Experts" correspondence in the *Journal of Clinical Psychopharmacology* (14 records) that matched on "experts", German actuarial "rating, ranking, scoring" papers, *BMJ* news items, and a *Theoretical Economics* paper. |
| K3 | rational scale to assess the harm of drugs of potential misuse scheduling harmfulness | 30 | Run: 30 returned, 5 retained (Nutt 2007 — the founding paper; Caulkins 2011 — the principal critique; Kalant 1999; Novin 2024; Potter 2021). Dropped: general harm-reduction essays in *Substance Use & Misuse* and *Drugs: Education, Prevention and Policy* that matched on "harm" and "misuse", prescription-opioid perception studies, a doping paper. |
| K4 | comparative risk assessment alcohol tobacco cannabis illicit drugs margin of exposure | 30 | Run: 30 returned, 6 retained (Lachenmeier & Rehm 2015; Baumung 2016; Rehm 2006; Johnstad 2022; Ritter & Cameron 2006; Single 1998). Dropped: prenatal-exposure, gateway-hypothesis, adolescent-twin and medical-cannabis-substitution papers that matched on the substance list; a *BMJ* news item; a correction notice for an unrelated Australian emergency-department paper. |
| K5 | global burden of disease attributable to alcohol and drug use 195 countries territories | 30 | Run: 30 returned, 6 retained (Degenhardt & Hall 2013; Rehm 2009; Wu 2025; Chen 2022; Liu 2026; Dávila-Cervantes 2026). Dropped: ~20 non-substance GBD papers (breast cancer, dementia, chronic kidney disease, air pollution, preterm birth and so on) and alcohol-attributable single-cancer-site papers that do not bear on cross-substance comparison. **Degenhardt et al. 2018 (*Lancet Psychiatry*) was not returned.** |
| — | *(no new request)* Degenhardt et al. 2018 recovered from inside the project rather than by search: the DOI `10.1016/S2215-0366(18)30337-7` already appears in the Methamphetamine, Cocaine, Cannabis and MDMA DOI lists and resolved in the lead co-editor's independent Crossref sweep of 2026-10-15 (`_VERIFICATION-SWEEP_2026-10-15.md`, 609/609 DOIs resolved), which also recorded its linked erratum. Entered as item 19 with its verification route stated in the row. | — | Added without a Crossref request. |

**Note on the search endpoint.** The Crossref API was shared with several co-editor sessions behind one egress address, and this topic ran during the worst of the throttling: of 11 requests, 6 returned results and 5 were refused with HTTP 429. Waits of 240 s, 420 s and 600 s were used between requests. No refused URL was re-fetched; substitutes were written and are logged above with a `b` suffix.

### DOI verification outcomes

- 32 DOIs entered the list; 31 came verbatim from the Crossref search records above, with title, journal, year and first author echoed into the DOI list for checking against the PDF (METHODS §4.2). The 32nd (item 19, Degenhardt 2018) came from the project's own verified lists and the 2026-10-15 sweep, as logged in the row above.
- 0 DOIs failed to resolve; 0 resolved to a different paper; no recalled DOI needed correcting, because none was recalled.
- Corrections found: Degenhardt et al. 2018 has an erratum linked in Crossref; Bonomo et al. 2019 has a published corrigendum (10.1177/0269881119877724). Crossref returned the corrigendum before the article in both K1b and K2b, which is a useful reminder that the corrigendum alters reported values; the DOI list marks the pair.
- Retractions found: none. The per-DOI `updated-by` check of METHODS §4.3 has not been run item by item.
- Published critique clusters captured (METHODS §2.3(3)): Nutt 2007 / Nutt 2010 ↔ Caulkins 2011 ↔ Rolles & Measham 2011 ↔ Kalant 1999 (anticipatory). **Not captured:** published critiques of van Amsterdam 2015 and Bonomo 2019, if they exist. Forward citation (Layer 4) must settle this before either is cited.

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed (https://pubmed.ncbi.nlm.nih.gov). For each: **Save → Selection: All results → Format: CSV**, and save the file into `search-logs/` with the name given. Note the hit count PubMed shows and send me the numbers. P1 recovers the missing GBD paper; P4 is the critique sweep.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `(Degenhardt L[Author]) AND ("global burden" OR "burden of disease") AND (alcohol OR "drug use") AND ("2016"[Date - Publication] : "2020"[Date - Publication])` | _HarmRankings_pubmed_P1.csv | |
| P2 | `("multicriteria decision analysis" OR "multi-criteria decision analysis" OR MCDA) AND (drug* OR alcohol OR "substance") AND (harm*[Title] OR ranking[Title] OR classification[Title])` | _HarmRankings_pubmed_P2.csv | |
| P3 | `(Nutt DJ[Author] OR "van Amsterdam J"[Author] OR Bonomo Y[Author]) AND (harm*[Title]) AND (rank* OR scale OR assess*)` | _HarmRankings_pubmed_P3.csv | |
| P4 | `("drug harm*"[Title] OR "harm ranking"[Title] OR "harmfulness"[Title]) AND (critique OR criticism OR comment[Publication Type] OR letter[Publication Type] OR "methodological")` | _HarmRankings_pubmed_P4.csv | |
| P5 | `("margin of exposure" OR "comparative risk assessment" OR "benchmark dose") AND (alcohol OR tobacco OR cannabis OR "illicit drug*" OR nicotine OR MDMA OR heroin)` | _HarmRankings_pubmed_P5.csv | |
| P6 | `("Global Burden of Disease") AND ("drug use disorder*" OR "substance use disorder*" OR "illicit drug*") AND (attributable OR DALY* OR "years of life lost")` | _HarmRankings_pubmed_P6.csv | |
| P7 | `("no safe level" OR "safe level of drinking" OR "alcohol use and burden") AND (critique OR correspondence OR comment[Publication Type] OR "J-shaped" OR "abstainer bias")` | _HarmRankings_pubmed_P7.csv | |
| P8 | `("drug scheduling" OR "drug classification" OR "controlled substance* schedul*") AND (evidence OR harm* OR "scientific basis") AND (policy OR law OR legislation)` | _HarmRankings_pubmed_P8.csv | |
| P9 | `("social cost*" OR "economic cost*" OR "cost of illness") AND (alcohol OR tobacco OR "illicit drug*") AND (estimate* OR methodology OR comparison)` | _HarmRankings_pubmed_P9.csv | |
| P10 | `("risk environment" OR "structural determinants") AND ("drug-related harm*" OR "drug harm*") AND (people who use drugs OR "injecting drug use")` | _HarmRankings_pubmed_P10.csv | |

## Layer 3 — Cochrane Library (to be run by VS)

Cochrane holds nothing directly relevant: harm ranking is not an intervention question. Skip Cochrane for this topic and instead check **PROSPERO** for any registered systematic review of drug-harm ranking methods, and the **IHME GBD results tool** for the data extract listed as R3.

## Layer 4 — Snowballing (AI, after PDFs arrive) — the decisive layer for this topic

Because the critique layer is the point of this list, forward citation matters more here than anywhere else in the project.

- Forward (Google Scholar "cited by"), screened for critiques, replies and re-analyses: item 1 (Nutt 2007), item 2 (Nutt 2010), item 6 (van Amsterdam 2015), item 7 (Bonomo 2019), item 9 (Lachenmeier 2015). Record, for each, whether a published critique exists; if none is found for items 6, 7 or 9, say so explicitly in the monograph rather than leaving the question open.
- Backward: reference lists of items 3, 4, 8 and 11 — the critiques and the newest MCDA — to pick up the older ranking attempts (Dutch 2010; UK Home Office Drug Harm Index) that the searches missed.
- Logged here with seed DOI and counts.

## PRISMA counts

To be completed after Layers 2–4: records identified per source; duplicates removed; screened; excluded with reasons; included. Layer 1 so far: 210 records returned across 6 executed Crossref queries; 31 included. The low inclusion rate (15%) is expected: the MCDA and GBD queries both return mostly out-of-domain literature.
