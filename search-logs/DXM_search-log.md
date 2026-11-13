# Dextromethorphan (DXM) — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-15 before screening; not altered during screening. Where a URL was refused the string was re-worded and re-run; both forms are shown.

## Layer 1 — Crossref bibliographic search (run by AI co-editor, 2026-10-15/16)

Endpoint and parameter notes as in `Nitrous-oxide_search-log.md`: `&sort=relevance` must be omitted (it makes the request fail from this environment, and omitting it is what allows `select` to be used), `select=DOI,title,container-title,issued,author` keeps records small enough for `rows=25`, and direct `curl` to api.crossref.org is refused by the egress proxy.

Rate limiting: Crossref/proxy returned HTTP 429 on 6 of 20 attempts in this block, with two consecutive refusals twice; waits of 120–300 s were used. Five further attempts returned a non-429 target error (and one a spurious robots error) and were re-run with different wording.

Screening rules (METHODS §3): retained human laboratory studies, poison-centre and surveillance series, dependence reports, interaction reports in serious journals, authoritative pharmacology reviews, and the registration-level therapeutic trials. Excluded: *Reactions Weekly* and *Inpharma Weekly* (which dominate every dextromethorphan hit list — more than 30 records across these searches), trade news outlets, conference abstracts in journal supplements, analytical-chemistry assay papers, and two venues that could not be confirmed in DOAJ/Scopus/MEDLINE.

### Section-level and targeted queries

| # | Query string (query.bibliographic) | Rows | Result |
|---|---|---|---|
| D1 | dextromethorphan pharmacokinetics CYP2D6 phenotype poor metabolizer dextrorphan | 25 | target error; re-run as D1b |
| D1b | dextromethorphan CYP2D6 polymorphism pharmacokinetics dextrorphan humans | 25 | refused (429); re-run as D1c |
| D1c | dextromethorphan CYP2D6 genotype metabolism dextrorphan plasma | 25 | target error; re-run as D1d |
| D1d | dextromethorphan O-demethylation debrisoquine phenotype pharmacokinetics | 20 | refused (429); re-run as D1e |
| D1e | dextromethorphan pharmacokinetics extensive poor metabolizers CYP2D6 | 20 | 20 hits, 2 retained (Pope 2004, Takashima 2005); the rest are studies using dextromethorphan as a CYP2D6 probe for other drugs |
| D2 | dextromethorphan abuse recreational use review pharmacology dissociative | 25 | 24 hits, 4 retained (Stanciu 2016, Taylor 2016, Bobo 2005, Bates 2021) |
| D3 | dextromethorphan poison center exposures adolescents trends United States | 25 | 25 hits, 2 retained (Ngo 2025, Brass 2018); the query drew the general US poison-centre literature rather than dextromethorphan |
| D4 | monitoring trends dextromethorphan abuse National Poison Data System | 20 | refused (429); re-run as D4b |
| D4b | dextromethorphan abuse poison control center cases adolescent trends | 20 | refused (429); covered instead by D8 |
| D5 | dextromethorphan serotonin syndrome toxicity SSRI monoamine oxidase inhibitor | 25 | 25 hits, 4 retained (NEJM 1988, Gillman 2005, Singh 2024, Sinclair 1973) |
| D6 | dextromethorphan dependence withdrawal case report psychosis chronic use | 25 | 25 hits, 1 retained (Miller 2005a); 20 of the 25 hits were *Reactions Weekly* |
| D7 | dextromethorphan intoxication overdose clinical effects emergency department case series | 25 | 25 hits, 1 retained (Harada 2025); 19 of the 25 were *Reactions Weekly* |
| D8 | dextromethorphan abuse adolescence increasing trend Coricidin cough cold tablets poison | 25 | 25 hits, 7 retained (Banerji 2001, Karami 2017, Bryner 2006, Miller 2005b, Wilson 2011, Graudins 1996, Paul 2004) — the highest-yield query of the set |
| D9 | high doses of dextromethorphan NMDA antagonist produce effects similar classic hallucinogens | 25 | refused (robots error from the target); re-run as D9b |
| D9b | dextromethorphan hallucinogen like subjective effects healthy volunteers Reissig Zawertailo | 25 | 25 hits, 5 retained (Zawertailo 1998, Zawertailo 2009, Hildebrand 1989, Caruso 1999, Fleckenstein 1996, Karttunen 2009, Faruqi 2014); Reissig 2012 not surfaced |
| D10 | Reissig Carbonaro dextromethorphan psilocybin dose effects ratings hallucinogens | 25 | refused (429); re-run as D10b |
| D10b | dextromethorphan psilocybin triazolam dose effects hallucinogen healthy participants | 25 | 25 hits, 2 retained (Barrett 2018, Mathai 2023); Reissig 2012 and Carbonaro 2018 still not surfaced — see "Known gaps" in the DOI list |
| D11 | dextromethorphan bupropion quinidine randomized trial depression pseudobulbar affect | 25 | 25 hits, 6 retained (Brooks 2004, Panitch 2006, Pioro 2014, Schoedel 2014, Yang 2014, Zorowitz 2019); the GEMINI/ASCEND depression trials were not surfaced by this string |
| D12 | dextromethorphan abuse toxicity CYP2D6 — with `filter=type:journal-article,has-update:true` (retraction/erratum screen) | 10 | refused (429) |
| D12b | dextromethorphan misuse toxicity serotonin — with `filter=type:journal-article,has-update:true` | 10 | refused (429) |
| D12c | dextromethorphan dextrorphan abuse poisoning — with `filter=type:journal-article,has-update:true` | 10 | target error |
| D12d | dextromethorphan cough abuse CYP2D6 serotonin toxicity — with `filter=type:journal-article,has-update:true` | 10 | target error — **screen not completed after four attempts; re-run before publication, or rely on PubMed string P13 below** |

Queries D8, D9b and D2 between them supplied two thirds of the retained records. The two queries aimed at the poison-centre literature by name (D3, D4/D4b) were the least productive, because "poison center" as a phrase matches the whole American clinical-toxicology corpus; the productive route was to name the product (Coricidin) instead.

### DOI corrections and update checks
- No recalled DOI was written into the list; every DOI was copied from a Crossref response in this session.
- No `works/<DOI>` verification fetch was needed (no DOI came from memory).
- `updated-by`: no erratum, correction or retraction was found among the 40 retained records. This rests on the records returned by the searches above; the dedicated `has-update:true` screen was refused twice and remains outstanding.

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed. For each: **Save → Selection: All results → Format: CSV** into `search-logs/` with the name given; note the hit count.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `(dextromethorphan[Title] OR DXM[Title] OR "robotripping"[Title/Abstract]) AND (abuse OR misuse OR nonmedical OR recreational OR dependence) AND (humans[MeSH Terms])` | dxm_pubmed_P1.csv | |
| P2 | `(dextromethorphan[Title/Abstract]) AND ("cytochrome P-450 CYP2D6"[MeSH Terms] OR CYP2D6 OR dextrorphan OR "poor metabolizer" OR pharmacogenetic*) AND (humans[MeSH Terms])` | dxm_pubmed_P2.csv | |
| P3 | `(dextromethorphan[Title/Abstract]) AND (pharmacokinetic* OR bioavailability OR "half-life" OR metabolite*) AND (humans[MeSH Terms])` | dxm_pubmed_P3.csv | |
| P4 | `(dextromethorphan[Title/Abstract]) AND ("serotonin syndrome"[MeSH Terms] OR "serotonin toxicity" OR SSRI OR "selective serotonin reuptake inhibitor" OR "monoamine oxidase inhibitor" OR MAOI)` | dxm_pubmed_P4.csv | |
| P5 | `(dextromethorphan[Title/Abstract]) AND (chlorpheniramine OR chlorphenamine OR acetaminophen OR paracetamol OR "combination product" OR Coricidin) AND (toxicity OR overdose OR poisoning)` | dxm_pubmed_P5.csv | |
| P6 | `(dextromethorphan[Title/Abstract]) AND ("poison control centers"[MeSH Terms] OR "National Poison Data System" OR surveillance OR "exposure calls" OR DAWN)` | dxm_pubmed_P6.csv | |
| P7 | `(dextromethorphan[Title/Abstract]) AND (adolescen* OR teenager* OR "high school" OR youth) AND (abuse OR misuse OR nonmedical OR prevalence)` | dxm_pubmed_P7.csv | |
| P8 | `(dextromethorphan[Title/Abstract]) AND (dependence OR withdrawal OR craving OR "use disorder" OR "self-administration" OR "abuse liability")` | dxm_pubmed_P8.csv | |
| P9 | `(dextromethorphan[Title/Abstract]) AND (hallucinogen* OR dissociative OR psychotomimetic OR "subjective effects") AND (humans[MeSH Terms])` | dxm_pubmed_P9.csv | |
| P10 | `(dextromethorphan[Title/Abstract]) AND (death OR deaths OR fatal* OR postmortem OR "driving under the influence" OR DUID)` | dxm_pubmed_P10.csv | |
| P11 | `(dextromethorphan[Title/Abstract]) AND (quinidine OR bupropion OR Nuedexta OR Auvelity) AND (randomized controlled trial[Publication Type])` | dxm_pubmed_P11.csv | |
| P12 | `(dextromethorphan[Title/Abstract]) AND ("out-of-hospital management" OR "consensus guideline" OR "clinical practice guideline" OR management OR treatment) AND (poisoning OR overdose)` | dxm_pubmed_P12.csv | |
| P13 | `(dextromethorphan[Title/Abstract]) AND (retracted publication[Publication Type] OR "retraction of publication"[Publication Type] OR published erratum[Publication Type])` | dxm_pubmed_P13.csv | |

P13 substitutes for the Crossref `has-update:true` screen that was refused; run it even if it returns nothing.

## Layer 3 — Cochrane Library (to be run by VS)

Search `dextromethorphan` in Cochrane Reviews (expect: cough in children and adults; neuropathic pain; nothing on non-medical use). Export → `dxm_cochrane.csv`.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of items 1, 2, 3 and 13 — items 1 and 3 are the only reviews in the list with substantial reference lists, and the papers missing from "Known gaps" (Reissig 2012, Chyka 2007, Romanelli & Smith 2009, Boyer 2004) will almost certainly be found in them. Forward: Google Scholar "cited by" on items 4, 8, 11 and 12. Logged here with seed DOI and counts.

## PRISMA counts

To be completed after Layers 2–4. Layer 1 so far: 20 Crossref requests attempted, 12 completed, 8 refused or errored; approximately 290 records screened by title and journal; 40 retained. The exclusion that dominates this substance is *Reactions Weekly*: roughly a third of all records screened.
