# _Dependence-epidemiology — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-15 before screening; not altered during screening. Searches executed 2026-10-15 and 2026-10-16. Cross-cutting topic treated as a substance for the purposes of the evidence-map brief.

## Layer 1 — Crossref bibliographic search and DOI verification (run by AI co-editor)

Searches run against `https://api.crossref.org/works?query.bibliographic=<terms>&filter=type:journal-article&rows=<n>&select=DOI,title,container-title,issued,author`. Verifications run against `https://api.crossref.org/works?filter=doi:<a>,doi:<b>,doi:<c>&select=DOI,title,container-title,issued,author&rows=5`. DOIs taken verbatim from search records need no further fetch (evidence-map brief, "Working economically" §3); DOIs recalled from memory were verified with the filter endpoint, and those that could not be verified were left out of the list.

| # | Query | rows | Status / hits retained |
|---|---|---|---|
| E1 | probability of transition to dependence cannabis cocaine alcohol tobacco national survey | 40 | Run: 40 returned, 14 retained — the NESARC conditional-probability set (Lopez-Quintero 2011 and 2010; Flórez-Salamanca 2013 ×2; Wagner & Anthony 2007; Cougle 2016) plus measurement papers (Compton 2013; Blanco 2007; Swift 2001; Agrawal 2007 and 2009). Dropped: a large block of cannabis–tobacco co-use papers that matched on substance names, pregnancy and adolescent papers, and one NIDA priorities statement. |
| E2 | Anthony comparative epidemiology dependence tobacco alcohol controlled substances National Comorbidity Survey | 30 | Run but **0 relevant hits**: the query returned 30 entirely unrelated records (veterinary, mathematics, geology), i.e. Crossref's bibliographic index did not match the 1994 *Experimental and Clinical Psychopharmacology* paper on these terms. Recovered instead by DOI verification (V1). |
| V1 | `filter=doi:` — Anthony 1994; Wagner & Anthony 2002; Leshner 1997 | 5 | Run: `total-results` = 3, all three records returned with matching titles, journals, years and first authors. Verified. |
| E3 | natural recovery remission without treatment addiction maturing out longitudinal | 40 | Run: 40 returned, 16 retained (Slutske 2010; Bischof 2001 and 2005; Moos 2006; Blomqvist 2002; Cunningham 2005; Snow 1973; Hertzman 1995; Searby 2015; Heather 1990; Edwards 1984 and 2000; Najman 2012; Kelly 2017; Mudry 2018; Dwyer 2023; Kosgolla 2026). Dropped: gambling and video-gaming "maturing out" papers (out of scope), *Journal of Ministry in Addiction & Recovery* items, residential-treatment process studies, a duplicate 1984 Edwards record under a second DOI. |
| E4 | brain disease model of addiction evidence critique promises | 40 | Run: 40 returned, 21 retained — the entire *Lancet Psychiatry* exchange (Hall 2015; Trujols 2015 critique; Hall 2015 authors' reply; Volkow & Koob 2015; Hall 2015 rejoinder; Blithikioti 2025) plus Becoña 2018, Heather 2017, Davies 2017, Snoek 2017 ×2, Bell 2013, Meurk 2014, O'Mahony 2025, Racine 2017, Ricardo 2022, Liu 2025, Egerer 2025, Bogren 2019, Grigson 2018, Heyman 2021, Kuorikoski 2018, Carreno 2019, Stockwell 1995, Drucker 1974, Wilbanks 1989, Dagher 2012. Dropped: two Turkish press interviews in *üha*, a *Cultural Critique* false hit on "promises", a *Brain* correction about Parkinson's microbiota, two book reviews, a supplemental-material record, a predatory-looking narrative review, a *Revista Española de Drogodependencias* item. |
| V2 | `filter=doi:` — Volkow 2016 (NEJM); Heilig 2021; Hart 2017; Lewis 2017 | 6 | **Filter silently dropped** by the server: `total-results` ≈ 1.87 × 10⁸ and the six records returned were unrelated (veterinary dentistry, differential geometry, a master's thesis). Nothing verified; not re-fetched at the same URL. |
| V2b | `filter=doi:` — Volkow 2016 (lowercased DOI); Heilig 2021; Hart 2017 | 5 | Run (Lewis 2017 dropped from the set): `total-results` = 3, all three returned with matching metadata. Verified. **Lewis 2017 remains unverified and is excluded from the list.** |
| V3 | `filter=doi:` — Robins 1975 (*Arch Gen Psychiatry*); Robins 1993; Alexander 1978 | 5 | **Filter silently dropped** again (`total-results` ≈ 1.86 × 10⁸, unrelated records). Nothing verified; not re-fetched. Robins 1993 and Alexander 1978 were subsequently recovered by search (E5, E6); **Robins 1975 was not** and is listed under Known gaps. |
| E5 | Vietnam veterans narcotic use Southeast Asia heroin addiction remission Robins | 30 | **Not run** — the request was refused with ROBOTS_DISALLOWED, then HTTP 429 on the reformulated version. Not re-fetched. |
| E5b | Vietnam veterans heroin addiction rapid recovery narcotic use after return | 30 | Run (substitute): 30 returned, 5 retained (Robins 1993; Robins 2003; Robins 2010; Helzer 1976; Hall 2016 appraisal). Dropped: *Heroin Addiction and Related Clinical Problems* items, a *Labour Economics* paper on veterans' labour-market outcomes, a *Third Text* visual-culture essay, a psychodrama item in a predatory-looking venue, clinical case reports, and opioid-pharmacology papers that matched on "narcotic". |
| E6 | Rat Park housing environment morphine self-administration rats enrichment | 25 | Run: 25 returned, **2 retained** (Alexander 1978 — the Rat Park paper itself; Marks-Kaufman 1984). The remaining 23 were unrelated rodent morphine-self-administration pharmacology (lesion, ascorbic-acid, nitric-oxide and nanocurcumin studies). **No published critique or replication of Rat Park was returned**; see Known gaps. |
| E7 | prevalence correlates DSM-5 drug use disorder National Epidemiologic Survey Alcohol Related Conditions III | 40 | **Not run** — HTTP 429, not re-fetched. |
| E7b | epidemiology DSM-5 drug use disorder prevalence NESARC-III national survey | 40 | Run (substitute): 40 returned, 12 retained (Grant 2016 and 2015; Hasin 2016; Kerridge 2018 and 2015; Fan 2019; Hochheimer 2020; Bailey 2024; Grant 1996; Hasin 1996; Cottler 1991; Lynskey 2007; Blanco 2008). Dropped: PTSD-, anxiety-, eating-disorder- and bipolar-comorbidity papers using the same survey but answering a different question; veteran-specific subsamples; a *Medical Research Archives* item; a duplicate *Journal of Sleep Research* abstract. |

**Note on the search endpoint.** The Crossref API was shared with several co-editor sessions behind one egress address. Of 13 requests, 9 produced usable output. Spacing of 150–300 s between requests was used throughout.

**Warning for future sessions — the multi-DOI filter can fail silently.** `works?filter=doi:A,doi:B,doi:C` returned the correct records on V1 and V2b, but on V2 and V3 the filter was ignored and the API returned the whole corpus (`total-results` ≈ 1.87 × 10⁸) with arbitrary records, which at a glance looks like a normal response. Always read `total-results`: it must equal the number of DOIs requested. A figure in the hundreds of millions means nothing was verified. Two landmark DOIs (Lewis 2017; Robins 1975) were left out of the list for exactly this reason rather than being entered on the strength of a failed check.

### DOI verification outcomes

- 82 DOIs entered the list: 76 taken verbatim from Crossref search records (title, journal, year and first author echoed into the DOI list for checking against the PDF, METHODS §4.2) and 6 verified by `works?filter=doi:`.
- 2 recalled DOIs could not be verified and were excluded: `10.1007/s12152-017-9293-z` (Lewis 2017) and `10.1001/archpsyc.1975.01760260019001` (Robins 1975). Both appear under Known gaps with their titles.
- Corrections/errata found: none for this topic. Retractions: none. The per-DOI `updated-by` check of METHODS §4.3 still has to be run item by item.
- Published critique clusters captured (METHODS §2.3(3)): Hall 2015 ↔ Trujols 2015 ↔ Hall reply ↔ Volkow & Koob 2015 ↔ Hall rejoinder ↔ Blithikioti 2025; Robins 1993/2003/2010 ↔ Hall 2016 ↔ Becoña 2018; Leshner 1997 ↔ Hart 2017 ↔ Heilig 2021. **Not captured:** critiques of Alexander 1978 (Rat Park) and of Volkow 2016.

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed (https://pubmed.ncbi.nlm.nih.gov). For each: **Save → Selection: All results → Format: CSV**, and save the file into `search-logs/` with the name given. Note the hit count PubMed shows and send me the numbers. P1 and P6 are the priorities: they recover the two landmarks this list is missing.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `(Robins LN[Author]) AND (Vietnam OR narcotic* OR heroin)` | _Dependence_pubmed_P1.csv | |
| P2 | `("conditional probability" OR "transition to dependence" OR "cumulative probability") AND (dependence OR "use disorder") AND (cannabis OR cocaine OR alcohol OR nicotine OR heroin OR "extra-medical") AND (survey OR epidemiolog*)` | _Dependence_pubmed_P2.csv | |
| P3 | `(Anthony JC[Author]) AND (dependence OR "drug dependence" OR epidemiolog*)` | _Dependence_pubmed_P3.csv | |
| P4 | `("natural recovery" OR "remission without treatment" OR "untreated remission" OR "spontaneous remission" OR "self-change") AND (alcohol OR drug* OR "substance use disorder") AND (humans[MeSH Terms])` | _Dependence_pubmed_P4.csv | |
| P5 | `("maturing out" OR "aging out" OR "desistance") AND (drug* OR alcohol OR heroin OR "substance use") AND (humans[MeSH Terms])` | _Dependence_pubmed_P5.csv | |
| P6 | `("rat park" OR (housing[Title] AND (morphine OR opioid) AND (self-administration OR consumption))) AND (rats OR rodent*)` | _Dependence_pubmed_P6.csv | |
| P7 | `("brain disease model" OR "brain disease of addiction" OR "addiction is a brain disease") AND (critique OR evidence OR stigma OR debate OR commentary OR reply)` | _Dependence_pubmed_P7.csv | |
| P8 | `(Volkow ND[Author] AND "brain disease") OR (Heilig M[Author] AND addiction AND "brain disease") OR (Hart CL[Author] AND addiction)` | _Dependence_pubmed_P8.csv | |
| P9 | `("NESARC" OR "National Epidemiologic Survey on Alcohol and Related Conditions") AND (prevalence[Title] OR epidemiology[Title]) AND ("use disorder"[Title] OR dependence[Title])` | _Dependence_pubmed_P9.csv | |
| P10 | `("DSM-5"[Title] OR "DSM-IV"[Title] OR "ICD-11"[Title] OR "ICD-10"[Title]) AND ("substance use disorder*"[Title] OR dependence[Title]) AND (criteria OR concordance OR crosswalk OR comparability OR prevalence)` | _Dependence_pubmed_P10.csv | |
| P11 | `(remission[Title] OR recovery[Title]) AND ("substance use disorder*" OR "drug dependence") AND (systematic review[Publication Type] OR meta-analysis[Publication Type] OR "prospective")` | _Dependence_pubmed_P11.csv | |
| P12 | `(Hser YI[Author] OR Vaillant GE[Author]) AND (follow-up OR "natural history" OR longitudinal) AND (narcotic* OR heroin OR alcohol)` | _Dependence_pubmed_P12.csv | |
| P13 | `("treatment gap" OR "treatment utilization" OR "help-seeking") AND ("substance use disorder" OR "drug dependence") AND (population OR survey OR epidemiolog*) AND (humans[MeSH Terms])` | _Dependence_pubmed_P13.csv | |

## Layer 3 — Cochrane Library and registries (to be run by VS)

Cochrane holds little that is directly relevant to this topic (it is an epidemiology and concepts topic, not an intervention one). Search `remission substance use disorder` in Cochrane Reviews and export → `_Dependence-epidemiology_cochrane.csv`. Also check PROSPERO for registered but unpublished systematic reviews of remission rates.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of Anthony 1994, Lopez-Quintero 2011, Slutske 2010, Hall 2016, Heilig 2021. Forward (Google Scholar "cited by"): items 1, 2, 11, 17, 19, 26 — the six landmarks. The forward search on item 26 (Rat Park) is the designated route to its missing critiques. Logged here with seed DOI and counts.

## PRISMA counts

To be completed after Layers 2–4: records identified per source; duplicates removed; screened; excluded with reasons; included. Layer 1 so far: 245 records returned across 7 executed Crossref searches (plus 3 DOI-verification fetches); 82 included.
