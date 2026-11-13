# Salvia divinorum / salvinorin A — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-16 before screening; not altered during screening. Where a URL was refused the string was re-worded and re-run; both forms are shown.

## Layer 1 — Crossref bibliographic search (run by AI co-editor, 2026-10-16)

Endpoint and parameter notes as in `Nitrous-oxide_search-log.md`: omit `&sort=relevance` (it makes the request fail from this environment, and omitting it is what allows `select` to be used), use `select=DOI,title,container-title,issued,author` with `rows=25`, and note that direct `curl` to api.crossref.org is refused by the egress proxy.

Rate limiting: in this block Crossref/proxy returned HTTP 429 on 0 of 9 attempts and a non-429 target error on 2; waits of 130 s between calls were enough. This was the cleanest block of the four-substance run.

Screening rules (METHODS §3): retained every controlled human study without exception (there are only seven), the kappa-opioid pharmacology landmarks, the single systematic review, population surveys, the dependence case series, legal-status analyses, and the forensic-identity papers the monograph's "Identity and nomenclature" section needs. Excluded: *ChemInform* abstracting records; conference abstracts in journal supplements (including the ECNP abstract of the Johns Hopkins human study and the ASCPT abstract of the Baggott web survey, both of which appear in the list as their full papers); trade and single-case venues; and the large synthetic-analogue medicinal-chemistry series in *Planta Medica* and *Bioorg Med Chem Lett*, which is a drug-discovery programme rather than evidence about a substance people use.

### Section-level and targeted queries

| # | Query string (query.bibliographic) | Rows | Result |
|---|---|---|---|
| V1 | salvinorin A kappa opioid receptor agonist Salvia divinorum Roth | 25 | 25 hits, 10 retained (Johnson 2011, Chavkin 2004, Yan 2004, Cruz 2017, Butelman 2015 + its corrigendum, Sheffler 2003, Siebert 1994, Munro 2004, Kane 2006, McCurdy 2006); Roth 2002 itself not surfaced by this string — see V2 |
| V2 | salvinorin A potent naturally occurring nonnitrogenous kappa opioid selective agonist | 15 | 15 hits, 4 retained (Roth 2002, Cunningham 2011, Mendelson 2011, Freeman 2014). Naming the exact title was the only way to surface the landmark: a query carrying the author name "Roth" does not return it, because B. L. Roth is a co-author on dozens of higher-scoring analogue papers |
| V3 | salvinorin A inhaled humans subjective effects mystical dissociative controlled study | 25 | target error; re-run as V3b |
| V3b | salvinorin A humans mystical experience dissociative effects interoception | 25 | 25 hits, 8 retained (MacLean 2013, Maqueda 2015, Addy 2012, Johnson 2016, Doss 2020, Ranganathan 2012, Hooker 2008, Zürrer 2026) — this one query returned six of the seven controlled human studies plus the only systematic review. The word "interoception" did the work; "mystical experience" pulled in a large theology literature that had to be screened out |
| V4 | Salvia divinorum use prevalence epidemiology survey legal status legislation | 25 | 25 hits, 15 retained (Currie 2013, Wu 2011, Sumnall 2010, Ford 2011, Baggott 2010, Wheeler 2026, Przekop 2009, Griffin 2008, Babu 2008, Kelly 2011, Khey 2008, Casselman 2011, Prisinzano 2005, Moreira 2014, Nyi 2010, Miller 2012, Meyer 2012, Lin 2024) |
| V5 | Salvia divinorum salvinorin dependence abuse liability adverse effects toxicity | 25 | target error; re-run as V5b |
| V5b | Salvia divinorum addiction potential reinforcing effects safety review | 25 | 25 hits, 9 retained (El-Khoury 2018, Calado 2025, Dalgarno 2007, Albertson 2009, Lange 2010, Hanes 2001, Appel 2007, Scherbaum 2021, Braida 2009, Martinho 2016, González-Trujano 2016) |
| V6 | Salvia divinorum salvinorin kappa opioid hallucinogen — with `filter=type:journal-article,has-update:true` (retraction/erratum screen) | 10 | 5 hits; one **retraction** found (10.1007/s00044-013-0866-z, *Med Chem Res*, a salvinorin A analogue selectivity paper — not in the list, recorded in the Verification block so it is not re-admitted), one erratum on a paper subsequently added to the list as item 46, and three corrections on papers outside the list |

Six completed queries produced the whole list. For a substance this small that is the right number; a seventh and eighth query were not run because V4 and V5b were already returning the same records.

### DOI corrections and update checks
- No recalled DOI was written into the list; every DOI was copied from a Crossref response in this session.
- No `works/<DOI>` verification fetch was needed (no DOI came from memory).
- Year discrepancies to expect when matching PDFs: Crossref `issued` is the online-first year for MacLean (2012 vs print 2013), Addy (2011 vs print 2012) and Mendelson (2010 vs print 2011). The DOI list carries the print year in the "Journal, year" column and the discrepancy is noted in its Verification block.
- Updates found: Butelman & Kreek 2015 → corrigendum 10.3389/fphar.2015.00285; Bodnar Willard 2020 → erratum 10.1016/j.forc.2021.100322; one retraction in the wider literature (above).

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed. For each: **Save → Selection: All results → Format: CSV** into `search-logs/` with the name given; note the hit count. Because the whole literature is small, several of these will return under 100 records — export them all rather than narrowing.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `("Salvia divinorum"[Title/Abstract] OR "salvinorin"[Title/Abstract] OR "ska maria pastora"[Title/Abstract] OR "diviner's sage"[Title/Abstract])` | salvia_pubmed_P1.csv | |
| P2 | `("salvinorin A"[Title/Abstract]) AND (humans[MeSH Terms]) AND (administration OR inhal* OR vaporiz* OR sublingual OR "dose-effect" OR subjective)` | salvia_pubmed_P2.csv | |
| P3 | `("salvinorin A"[Title/Abstract] OR "Salvia divinorum"[Title/Abstract]) AND ("receptors, opioid, kappa"[MeSH Terms] OR "kappa opioid" OR KOR)` | salvia_pubmed_P3.csv | |
| P4 | `("salvinorin A"[Title/Abstract]) AND (pharmacokinetic* OR "plasma concentration" OR "half-life" OR metabolism OR bioavailability)` | salvia_pubmed_P4.csv | |
| P5 | `("Salvia divinorum"[Title/Abstract]) AND (prevalence OR epidemiolog* OR survey OR NSDUH OR "Monitoring the Future" OR adolescen* OR "college student*")` | salvia_pubmed_P5.csv | |
| P6 | `("Salvia divinorum"[Title/Abstract]) AND (dependence OR addiction OR withdrawal OR "use disorder" OR "abuse liability" OR "self-administration")` | salvia_pubmed_P6.csv | |
| P7 | `("Salvia divinorum"[Title/Abstract] OR "salvinorin"[Title/Abstract]) AND (psychosis OR psychotic OR mania OR "adverse effect*" OR toxicity OR "case report"[Publication Type])` | salvia_pubmed_P7.csv | |
| P8 | `("Salvia divinorum"[Title/Abstract]) AND (legal OR legislation OR scheduling OR "controlled substance" OR policy OR regulation)` | salvia_pubmed_P8.csv | |
| P9 | `("Salvia divinorum"[Title/Abstract]) AND (ethnopharmacolog* OR Mazatec OR Oaxaca OR traditional OR ritual)` | salvia_pubmed_P9.csv | |
| P10 | `("Salvia divinorum"[Title/Abstract] OR "salvinorin"[Title/Abstract]) AND (extract* OR potency OR "5x" OR fortified OR "drug checking" OR adulterant OR smartshop)` | salvia_pubmed_P10.csv | |
| P11 | `("salvinorin A"[Title/Abstract]) AND (neuroimaging OR fMRI OR "functional connectivity" OR EEG OR PET)` | salvia_pubmed_P11.csv | |
| P12 | `("Salvia divinorum"[Title/Abstract] OR "salvinorin"[Title/Abstract]) AND (retracted publication[Publication Type] OR published erratum[Publication Type])` | salvia_pubmed_P12.csv | |

## Layer 3 — Cochrane Library (to be run by VS)

Search `Salvia divinorum` and `salvinorin` in Cochrane Reviews. Expect nothing; record the nil result, because the monograph's therapeutic section will need to state that no Cochrane review exists. Export → `salvia_cochrane.csv`.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of items 6, 9 and 21 — item 6 (Pharmacological Reviews) and item 9 (the 2026 systematic review) between them should contain everything in the "Known gaps" paragraph, including the Valdés ethnopharmacology papers of 1983–1984. Forward: Google Scholar "cited by" on items 1, 10, 11 and 15; the forward citations of item 15 (the null sublingual trial) are the ones that matter for the route question. Logged here with seed DOI and counts.

## PRISMA counts

To be completed after Layers 2–4. Layer 1 so far: 9 Crossref requests attempted, 7 completed, 2 errored; approximately 165 records screened by title and journal; 53 retained. The retained fraction is far higher than for the other substances in this batch, because the literature is small enough that most records returned were genuinely on topic.
