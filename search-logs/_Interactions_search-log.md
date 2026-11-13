# _Interactions — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-15 before screening; not altered during screening.

## Layer 1 — Crossref bibliographic search and DOI verification (run by AI, 2026-10-15)

### Pre-registered section queries (Crossref `works?query.bibliographic=`, `type:journal-article`, relevance-sorted)

| # | Query | Status / hits retained |
|---|---|---|
| I1 | opioid benzodiazepine concurrent use overdose death cohort | Run (15 rows): 15 hits, 3 retained (Hernandez 2018; Bharat 2024; Garg 2017); dropped news digests (Pharm J, Reactions Weekly, Brown Univ Update, DTB), a conference abstract (Value in Health), an SSRN preprint, a trial registration, and two off-topic items. |
| T1 | Park benzodiazepine prescribing deaths overdose veterans opioid analgesics | Run (8 rows): Park 2015 BMJ found; Bohnert 2011 JAMA retained. |
| I2 | opioid alcohol co-use overdose mortality | Not run (endpoint throttled, see note) — covered by DOI resolution of Tori 2020, Hickman 2008, Koski 2003. |
| I3 | gabapentin pregabalin opioid co-prescription overdose death | Not run — covered by Gomes 2017/2018, Lyndon 2017, Macleod 2019, Evoy 2021, Baird 2014. |
| I4 | serotonin syndrome diagnostic criteria Hunter | Not run — covered by Boyer 2005, Dunkley 2003, Sternbach 1991, Werneke 2016, Isbister 2007, Buckley 2014. |
| I5 | MAOI MDMA serotonin toxicity ayahuasca interaction | Not run — covered by Smilkstein 1987, Vuori 2003, Callaway 1998, Silins 2007, Pilgrim 2011, Gillman 2005. |
| I6 | tramadol serotonin syndrome antidepressant | Not run — covered by Hassamal 2018; Gillman 2010 (triptans). |
| I7 | cocaethylene cocaine ethanol toxicity humans | Not run — covered by Hearn 1991, Farré 1993, McCance-Katz 1998, Pennings 2002, Jones 2019. |
| I8 | GHB ethanol co-ingestion intoxication | Not run — covered by Thai 2006, Liechti 2006, Miró 2017, Galicia 2019. |
| I9 | ketamine ethanol combined effects humans | Not run — Krystal 1998 (lorazepam), Darke 2021, Schifano 2008 located by title. Thin literature. |
| I10 | cannabis alcohol combined driving crash risk | Not run — covered by Asbridge 2012, Rogeberg & Elvik 2016 (+ correction), Hartman 2013/2015, Dubois 2015, Sewell 2009, Bramness 2010, Hels 2013. |
| I11 | lithium psychedelic seizures psilocybin LSD | Not run — covered by Nayak 2021, Halman 2024, Sarparast 2022, Becker 2022, Bonson 1996, Liechti 2000, Farré 2007. |
| I12 | CYP2D6 MDMA pharmacokinetics genotype | Not run — covered by de la Torre 2000/2004/2012, O'Mathúna 2008, Schmid 2016, Vizeli 2017, Zawertailo 1998, Gasche 2004, Crews 2014. |
| I13 | polysubstance overdose deaths fentanyl stimulants epidemiology | Not run — covered by Gladden 2019, O'Donnell 2021, Jones 2018, Hoots 2020, Palis 2022, Compton 2021, Karamouzian 2022. |
| I14 | psychedelic drug-drug interactions systematic review | Not run — Halman 2024; Sarparast 2022. |
| I15 | harm reduction drug combination information websites evaluation | Run as web search (no Crossref): no peer-reviewed appraisal of TripSit/PsychonautWiki charts found; Dutton 2025 scoping review retained. |
| I16 | benzodiazepine alcohol interaction impairment mortality | Not run — Tanaka 2002, Koski 2003 located by title; Linnoila 1990 not located. |

**Note on the search endpoint.** The Crossref API was shared with several co-editor sessions behind one egress address and returned HTTP 429 (rate limited) on most calls after the first two queries; the queries marked "not run" must be run in Layer 2 (PubMed strings below) and, when Crossref recovers, as written above. DOIs for recalled landmarks were located with OpenAlex `title.search` and with web search, then fetched one by one (Crossref `works/<DOI>`, or Crossref `works?filter=doi:` in pairs, or the OpenAlex DOI record when Crossref was throttled). The route used for each DOI is in column V of the DOI list.

### DOI verification outcomes

- 39 DOIs resolved on Crossref (`works/<DOI>` or `works?filter=doi:`), none with an `updated-by` field.
- 37 DOIs resolved on OpenAlex only (`is_retracted` = false for all); 3 DOIs taken from Crossref search-hit records; 1 DOI additionally resolved through doi.org to the Springer page (Dutton 2025).
- Recalled DOIs found to be wrong on verification and corrected: Callaway & Grob 1998 (10.1080/02791072.1998.10399709 → 10.1080/02791072.1998.10399712); Vuori 2003 (10.1046/j.1360-0443.2003.00272.x → 10.1046/j.1360-0443.2003.00292.x); Silins 2007 (10.1080/00048670701579027 → 10.1080/00048670701449237); Bramness 2010 located as 10.1111/j.1360-0443.2010.02911.x (the recalled 02928.x was never fetched).
- Recalled DOIs that resolved to a different paper and were excluded: 10.1093/jurban/jtg024 (not Darke & Hall 2003); 10.3389/fneur.2023.1214969 (a case report, not the psychedelic-seizure scoping review).
- Errata/corrections: Rogeberg & Elvik 2016 (correction 10.1111/add.14140); Evoy 2021 (comment and reply). Retractions: none.

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed (https://pubmed.ncbi.nlm.nih.gov). For each: **Save → Selection: All results → Format: CSV**, and save the file into `search-logs/` with the name given. Note the hit count shown by PubMed next to each string and send me the numbers.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `(opioid* OR heroin OR fentanyl OR methadone OR buprenorphine) AND (benzodiazepine* OR alcohol OR ethanol OR gabapentin* OR pregabalin OR "z-drug*") AND (overdose OR "drug-related death*" OR mortality) AND (cohort OR "case-control" OR registry) AND (humans[MeSH Terms])` | _Interactions_pubmed_P1.csv | |
| P2 | `("serotonin syndrome"[Title] OR "serotonin toxicity"[Title]) AND (criteria OR diagnosis OR Hunter OR Sternbach OR review[Publication Type] OR "systematic review")` | _Interactions_pubmed_P2.csv | |
| P3 | `("serotonin syndrome" OR "serotonin toxicity") AND (MDMA OR ecstasy OR ayahuasca OR DMT OR "monoamine oxidase inhibitor*" OR tramadol OR dextromethorphan OR LSD OR psilocybin) AND (humans[MeSH Terms])` | _Interactions_pubmed_P3.csv | |
| P4 | `(psychedelic* OR psilocybin OR LSD OR MDMA) AND ("drug interaction*"[Title] OR "drug-drug interaction*"[Title] OR lithium[Title] OR antidepressant*[Title] OR SSRI*[Title]) AND (humans[MeSH Terms])` | _Interactions_pubmed_P4.csv | |
| P5 | `(cocaethylene[Title] OR ("cocaine"[Title] AND ("alcohol"[Title] OR "ethanol"[Title]))) AND (humans[MeSH Terms])` | _Interactions_pubmed_P5.csv | |
| P6 | `("gamma-hydroxybutyrate" OR GHB OR "gamma-butyrolactone" OR GBL) AND (alcohol OR ethanol OR benzodiazepine* OR "co-ingestion" OR polydrug) AND (intoxication OR overdose OR coma OR toxicity) AND (humans[MeSH Terms])` | _Interactions_pubmed_P6.csv | |
| P7 | `(ketamine[Title]) AND (alcohol OR ethanol OR benzodiazepine* OR opioid* OR polydrug OR "co-use") AND (humans[MeSH Terms]) AND (interaction OR death* OR overdose OR impairment)` | _Interactions_pubmed_P7.csv | |
| P8 | `(cannabis OR marijuana OR THC OR cannabinoid*) AND (alcohol OR ethanol) AND (driving OR "motor vehicle" OR crash* OR collision* OR "simulated driving") AND (humans[MeSH Terms])` | _Interactions_pubmed_P8.csv | |
| P9 | `(CYP2D6 OR "cytochrome P-450 CYP2D6"[MeSH Terms]) AND (MDMA OR ecstasy OR methamphetamine OR dextromethorphan OR codeine OR tramadol) AND (pharmacokinetic* OR genotype OR "ultrarapid" OR "poor metabolizer*") AND (humans[MeSH Terms])` | _Interactions_pubmed_P9.csv | |
| P10 | `(polysubstance OR polydrug OR "multiple drug*" OR "co-involvement" OR "co-use") AND (overdose[Title] OR "drug overdose"[MeSH Terms] OR "drug-related death*") AND ("2015"[Date - Publication] : "3000"[Date - Publication]) AND (humans[MeSH Terms])` | _Interactions_pubmed_P10.csv | |
| P11 | `(stimulant* OR methamphetamine OR cocaine) AND (opioid* OR fentanyl OR heroin) AND ("co-use" OR concurrent OR speedball OR "co-involved") AND (overdose OR mortality OR death*) AND ("2015"[Date - Publication] : "3000"[Date - Publication])` | _Interactions_pubmed_P11.csv | |
| P12 | `(benzodiazepine*[Title]) AND (alcohol[Title] OR ethanol[Title]) AND (interaction* OR poisoning* OR "fatal" OR impairment OR pharmacokinetic*) AND (humans[MeSH Terms])` | _Interactions_pubmed_P12.csv | |
| P13 | `("harm reduction" OR "drug checking" OR "online" OR website* OR "PsychonautWiki" OR "TripSit" OR Erowid OR "Bluelight") AND ("drug combination*" OR "combination chart*" OR polydrug OR "drug interaction*") AND (humans[MeSH Terms])` | _Interactions_pubmed_P13.csv | |
| P14 | `(nitrous oxide OR inhalant* OR "volatile substance*") AND (alcohol OR benzodiazepine* OR opioid* OR polydrug) AND (death* OR toxicity OR interaction) AND (humans[MeSH Terms])` | _Interactions_pubmed_P14.csv | |

## Layer 3 — Cochrane Library (to be run by VS)

Search `benzodiazepine AND opioid`, `serotonin syndrome`, and `polydrug` in Cochrane Reviews; export the result lists as CSV → `_Interactions_cochrane.csv`.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of Halman 2024, Sarparast 2022, Jones 2012, Karamouzian 2022, Pennings 2002, Asbridge 2012. Forward: Google Scholar "cited by" on items 1, 2, 10, 11, 12, 15, 21, 22, 25, 26 (landmarks and their critiques). Logged here with seed DOI and counts.

## PRISMA counts

To be completed after Layers 2–4: records identified per source; duplicates removed; screened; excluded with reasons; included.
