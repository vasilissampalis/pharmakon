# _Harm-reduction — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-15 before screening; not altered during screening. Cross-cutting topic treated as a substance for the purposes of the evidence-map brief.

## Layer 1 — Crossref bibliographic search (run by AI co-editor, 2026-10-15)

All queries run against `https://api.crossref.org/works?query.bibliographic=<terms>&filter=type:journal-article&rows=<n>&select=DOI,title,container-title,issued,author` (relevance-sorted). DOIs were taken verbatim from the returned records together with title, container-title, year and first author; no DOI was typed from memory, so no `works/<DOI>` re-fetch was needed (evidence-map brief, "Working economically" §3). After the throttling described below, `rows` was raised from 20 to 40 so that each surviving request returned more candidates.

| # | Query | rows | Status / hits retained |
|---|---|---|---|
| H1 | drug checking services systematic review people who use drugs | 20 | **Not run** — HTTP 429, not re-fetched. |
| H1b | drug checking service evaluation systematic review harm reduction | 20 | Run (substitute): 20 returned, 11 retained (Hungerbuehler 2011; Olsen 2022; Karamouzian 2018; Larnder 2021 **with its correction**; Rose 2023 ×2; Scarfone 2022; Fabresse 2024 **with its correction**; Measham 2021; Beaulieu 2021; Carroll 2022; Magnolini 2025). Dropped: two *CrimRxiv* preprints, an African medical-injection review, two 2026 service descriptions of marginal relevance. |
| H2 | take-home naloxone distribution programmes overdose mortality systematic review | 20 | **Not run** — HTTP 429, not re-fetched. |
| H2b | take-home naloxone programmes opioid overdose deaths systematic review | 20 | **Not run** — upstream fetch error, then HTTP 429 on a third formulation. Not re-fetched. |
| H2c | take-home naloxone distribution opioid overdose mortality review | 40 | Run (substitute; first query at rows=40): 40 returned, 22 retained, including the **Clark 2014 / Orkin 2015 systematic-review-and-critique pair** and the full take-home-naloxone backbone (McDonald & Strang 2017; Moustaqim-Barrette 2021; Sajwani 2022; Strang 1996 and 2019; Stam 2018; Håkansson 2024; Dowd 2023; Katzman 2020; Green 2008; Williams 2013; Marino 2019; Samuels 2018; Papp 2019; Noveloso 2020; Kim 2019; Dahlem 2020; Nielsen 2017; Black 2022; Blandthorn 2017; Duska 2022; Pasman 2025; Fleißner 2025 and 2026; Bennett 2014 comment). Dropped: *Reactions Weekly*, *Clinical Pharmacist*, *CMAJ* and *Evidence Based Nursing* news/digest items; a *Lancet* editorial; two conference abstracts; a *Clinical Practice in Athletic Training* item; a *Case Medical Research* registration. |
| H3 | supervised injection facility consumption room overdose evaluation review | 40 | Run: 40 returned, 21 retained, including the **Christian 2012 critique and the Marshall 2012 authors' reply** on the Vancouver mortality study, the Gareipy 2025 systematic review **with its 2026 corrigendum**, and the cost-effectiveness pair Bayoumi 2008 / Pinkerton 2010. Dropped: advocacy and legal-news items in *Harm Reduction Journal* and *CMAJ*, an *Urban Geography* essay, a *PharmacoEconomics & Outcomes News* digest, a *Drug and Alcohol Dependence* conference forum, an ethics reflection piece. **Marshall et al. 2011 (*Lancet*) itself was not returned.** |
| H4 | needle syringe programme opioid substitution treatment HIV hepatitis C mortality systematic review | 40 | Run: 40 returned, 18 retained (Platt 2017 Cochrane and the Addiction companion; Sordo 2017; Gowing 2011 Cochrane; Sawangjit 2016; Larney 2010; van Santen 2021 and 2023; Vickerman 2012; Des Jarlais 2013; Thanki 2021; Hall 2021; O'Connor 2020; Dennis 2014; Hestevik 2024; Nosyk 2015; Lindqvist 2023; Alavi 2013). Dropped: a *Cochrane Clinical Answers* digest of Platt 2017; prison-syringe and TB/HIV papers outside the question; conference abstracts (*Annals of Emergency Medicine*, *Journal of Hepatology*, *Journal of Virus Eradication*, *Open Forum Infectious Diseases*); *BMJ* news items; a predatory-looking *MOJ Addiction Medicine & Therapy* review; an unrelated Ethiopian ART mortality paper. |
| H5 | fentanyl test strips accuracy drug checking spectrometry point of care | 40 | **Not run** — upstream fetch error, then HTTP 429 on the reformulated version. Not re-fetched. |
| H5b | fentanyl test strips drug checking accuracy behaviour change people who use drugs | 40 | Run (substitute): 40 returned, 17 retained (Bergh 2021 selectivity and sensitivity — the accuracy study; Sisco 2024; Krieger 2018 ×2; Goldman 2019; Zibbell 2024 and Erickson 2026 SAFTSS; Tilhou 2023 ×2; Reed 2021, 2022 ×2, 2024; McCrae 2020; Rammohan 2022; Bardwell 2019; Piercey 2025; Allen 2020; Bailey 2024; Sutherland 2025; Maghsoudi 2021 systematic review). Dropped: a *Canadian Journal of Health Technologies* rapid report, a *Primary Care Companion* commentary, an unrelated Iranian prison qualitative study, several near-duplicate Rhode Island prevalence papers. |
| H6 | peer delivered harm reduction safer smoking pipe distribution injection transition | 40 | **Not run** — upstream fetch error. Not re-fetched. |
| H6b | peer delivered harm reduction intervention safer smoking equipment distribution | 40 | Run (substitute): 40 returned, 18 retained (Tapper 2023 narrative synthesis; Frankeberger 2019; Shannon 2006; Hunter 2012; Kielhold 2025; Ashton 2026; Parkes 2022 and Dumbrell 2024 SHARPS; Ashford 2018; Wilson 2025; Peng 2025; Chayama 2023; Treloar 2016; Scow 2023; Haines 2023; Rife-Pennington 2026; Skogen 2025; Herrera 2025; Fast 2008; Wood 2008). Dropped: the whole tobacco/e-cigarette/snus "harm reduction" block (about 12 records) and two gambling-harm-reduction reviews, which are out of this topic's scope; an SSRN preprint; a *Safer Communities* enforcement essay. |
| H7 | chemsex sexualised drug use intervention men who have sex with men review | 30 | **Not run** — HTTP 429, not re-fetched. |
| H7b | chemsex sexualised drug use harm reduction intervention systematic review | 30 | Run (substitute): 30 returned, 12 retained (Íncera-Fernández 2025 systematic review; Wang 2023 systematic review and meta-analysis; Bourne 2015; Hibbert 2021; Freestone 2025; Papamichail 2026; Choi 2021; Ma 2015; O'Reilly 2018; Zhang 2025; Ti 2014; Byrne 2024). Dropped: sociological and cultural-studies essays, country-overview pieces returned because they sit in *Harm Reduction Journal*, and a *Sri Lanka Journal of Medicine* commentary. |

**Note on the search endpoint.** The Crossref API was shared with several co-editor sessions behind one egress address. Of 13 requests, 7 returned results; 4 were refused with HTTP 429 and 2 returned an upstream fetch error. No refused URL was re-fetched; substitutes were written and are logged above with a `b`/`c` suffix. Spacing of 90–300 s between requests reduced but did not eliminate the refusals; raising `rows` from 20 to 40 roughly doubled the yield per surviving request and is the adaptation that saved this topic.

### DOI verification outcomes

- 138 DOIs entered the list; all 138 came verbatim from the Crossref search records above, with title, journal, year and first author echoed into the DOI list for checking against the PDF (METHODS §4.2).
- 0 DOIs failed to resolve; 0 resolved to a different paper; no recalled DOI needed correcting, because none was recalled.
- Corrections found: Gareipy 2025 (corrigendum 10.24095/hpcdp.46.2.04), Larnder 2021 (correction 10.1186/s12954-021-00548-7), Fabresse 2024 (correction 10.1186/s12954-024-01120-9). All marked "erratum published" in the list.
- Retractions found: none. The per-DOI `updated-by` check of METHODS §4.3 has **not** been run item by item and must be done when the reference records are created.
- Published critique clusters captured (METHODS §2.3(3)): Clark 2014 ↔ Orkin 2015; Marshall 2011 ↔ Christian 2012 ↔ Marshall 2012 reply (the 2011 original still to be located); Bayoumi 2008 ↔ Pinkerton 2010; take-home naloxone effectiveness ↔ Stam 2018.

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed (https://pubmed.ncbi.nlm.nih.gov). For each: **Save → Selection: All results → Format: CSV**, and save the file into `search-logs/` with the name given. Note the hit count PubMed shows for each string and send me the numbers. P1 is the priority: it is the string that recovers Marshall et al. 2011.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `("supervised inject*"[Title] OR "safer injecting facilit*"[Title] OR "drug consumption room*"[Title] OR "overdose prevention site*"[Title] OR "supervised consumption"[Title]) AND (mortality OR overdose OR "deaths") AND (humans[MeSH Terms])` | _HarmReduction_pubmed_P1.csv | |
| P2 | `("drug checking"[Title] OR "pill testing"[Title] OR "drug-checking") AND (service* OR evaluation OR accuracy OR behaviour OR behavior OR "systematic review") AND (humans[MeSH Terms])` | _HarmReduction_pubmed_P2.csv | |
| P3 | `("fentanyl test strip*" OR "immunoassay test strip*" OR "reagent test*" OR "FTIR" OR "infrared spectroscop*") AND ("drug checking" OR "point-of-care" OR adulterant* OR detection) AND (sensitivity OR specificity OR accuracy OR validation)` | _HarmReduction_pubmed_P3.csv | |
| P4 | `("take-home naloxone" OR "overdose education and naloxone distribution" OR "naloxone distribution") AND (mortality OR "overdose death*" OR effectiveness OR "systematic review" OR meta-analysis[Publication Type])` | _HarmReduction_pubmed_P4.csv | |
| P5 | `("needle exchange" OR "syringe exchange" OR "needle and syringe program*" OR "syringe services program*") AND (HIV OR "hepatitis C" OR HCV OR incidence OR "injecting risk") AND (review[Publication Type] OR "systematic review" OR cohort)` | _HarmReduction_pubmed_P5.csv | |
| P6 | `("opioid agonist" OR methadone OR buprenorphine OR "opioid substitution" OR "opioid maintenance") AND (mortality[Title] OR "all-cause mortality" OR "overdose death*") AND (cohort OR "systematic review" OR meta-analysis[Publication Type])` | _HarmReduction_pubmed_P6.csv | |
| P7 | `("heroin-assisted treatment" OR "supervised injectable" OR diamorphine OR "injectable opioid agonist treatment") AND (randomized controlled trial[Publication Type] OR trial OR "systematic review")` | _HarmReduction_pubmed_P7.csv | |
| P8 | `("safer smoking" OR "crack pipe*" OR "safer inhalation" OR "pipe distribution" OR "transition to injecting") AND ("harm reduction" OR intervention OR distribution) AND (humans[MeSH Terms])` | _HarmReduction_pubmed_P8.csv | |
| P9 | `("peer-delivered" OR "peer-led" OR "peer worker*" OR "lived experience") AND ("harm reduction" OR "people who use drugs" OR "people who inject drugs") AND (intervention OR trial OR evaluation OR "systematic review")` | _HarmReduction_pubmed_P9.csv | |
| P10 | `(chemsex OR "sexualised drug use" OR "sexualized drug use" OR "party and play") AND (intervention OR "harm reduction" OR service* OR treatment) AND (humans[MeSH Terms])` | _HarmReduction_pubmed_P10.csv | |
| P11 | `("hepatitis C" AND ("treatment as prevention" OR "test and treat" OR elimination)) AND ("people who inject drugs" OR PWID OR "injecting drug use") AND (model* OR trial OR cohort OR "systematic review")` | _HarmReduction_pubmed_P11.csv | |
| P12 | `("music festival*" OR "nightlife" OR "electronic dance music" OR "rave") AND ("harm reduction" OR "medical services" OR "drug checking" OR overdose OR hyperthermia) AND (humans[MeSH Terms])` | _HarmReduction_pubmed_P12.csv | |
| P13 | `("Good Samaritan law*" OR "911 Good Samaritan" OR "naloxone access law*") AND (overdose OR mortality OR "calling 911" OR "emergency medical services")` | _HarmReduction_pubmed_P13.csv | |
| P14 | `("safer supply" OR "safe supply" OR "prescribed alternatives" OR "pharmaceutical alternatives") AND ("people who use drugs" OR "unregulated drug" OR overdose) AND (evaluation OR cohort OR qualitative OR "systematic review")` | _HarmReduction_pubmed_P14.csv | |

## Layer 3 — Cochrane Library (to be run by VS)

Search `needle exchange`, `opioid substitution treatment mortality`, `naloxone`, `supervised injection`, and `drug checking` in Cochrane Reviews; export the result lists as CSV → `_Harm-reduction_cochrane.csv`. Cochrane is decisive for items 1 and 4 and is the correct AMSTAR 2 anchor for this topic.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of Platt 2017 (Cochrane), Sordo 2017, Maghsoudi 2021, Moustaqim-Barrette 2021, Gareipy 2025, Íncera-Fernández 2025. Forward (Google Scholar "cited by"): items 7–8 (Clark/Orkin), 12–14 (the Vancouver cluster), 16–17 (cost-effectiveness pair), 25–26 (Strang 1996 and the Stam counter-case), 29 (Bergh). Logged here with seed DOI and counts.

## PRISMA counts

To be completed after Layers 2–4: records identified per source; duplicates removed; screened; excluded with reasons; included. Layer 1 so far: 250 records returned across 7 executed Crossref queries; 138 included.
