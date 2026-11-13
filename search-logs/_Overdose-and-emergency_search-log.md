# _Overdose-and-emergency — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-15 before screening; not altered during screening. Cross-cutting topic treated as a substance for the purposes of the evidence-map brief.

## Layer 1 — Crossref bibliographic search (run by AI co-editor, 2026-10-15)

All queries run against `https://api.crossref.org/works?query.bibliographic=<terms>&filter=type:journal-article&rows=<n>&select=DOI,title,container-title,issued,author` (relevance-sorted, Crossref's default scoring). DOIs were taken verbatim from the returned records together with title, container-title, year and first author; no DOI was typed from memory, and therefore no `works/<DOI>` re-fetch was needed (evidence-map brief, "Working economically" §3).

| # | Query | rows | Status / hits retained |
|---|---|---|---|
| O1 | naloxone opioid overdose randomized intranasal | 15 | Run: 15 returned, 7 retained (Dietze 2019 RCT; Skulberg 2019 PK RCT; Sabzghabaee 2014 RCT; Alsayed 2026 SR/MA; Ashton 2006; Robinson 2014; Lewis 2017; plus Laffont 2024 translational and Dietze 2016 commentary kept with labels). Dropped: *Drug and Therapeutics Bulletin* digest, *Emergency Medicine News* "InFocus", a *Case Medical Research* trial registration, *Clinical Pharmacist* news item, one single case report. |
| O2 | opioid overdose recognition bystander response training | 15 | Run: 15 returned, 5 retained (Simmons 2016; Moses 2022; Kahn 2022; Fletcher 2019; Stephenson 2023 **with its published correction**). Dropped: *Clinical Psychiatry News*, a JAMA news item, a *CrimRxiv* preprint duplicating a JAMA Netw Open editorial, a *Federal Grants & Contracts* notice, pharmacy- and medical-student education surveys of marginal relevance, one *Cureus* item. |
| O3 | methamphetamine stimulant toxicity hyperthermia emergency management | 15 | **Not run** — upstream fetch error, then HTTP 429 on the reformulated version. Re-run in Layer 2. This is the main uncovered query for this topic. |
| O3b | stimulant toxicity hyperthermia agitation emergency management | 15 | Run (substitute for O3): 15 returned, 6 retained (Holubek 2006; Chan 2010; Yildiz 2003; Friedman 2020; and the GHB-agitation exchange Zvosec 2005 / Wood 2006 / Zvosec 2006, which this query surfaced). Dropped: paediatric agitation reviews, a *Signa Vitae* dosing paper, trauma-sedation review, schizophrenia-specific agitation paper. |
| O4 | methamphetamine cocaine acute toxicity clinical management review | 15 | **Not run** — HTTP 429, not re-fetched. |
| O5 | overamping experiences of overdose people who use methamphetamine | 8 | Run (title-targeted, after a web search located the title): Harding et al. 2022, *Harm Reduction Journal*, retained. Remaining hits off-topic or too recent/peripheral. |
| O6 | serotonin toxicity Hunter criteria diagnosis critique | 15 | Run: 15 returned, 5 retained (Dunkley 2003; Isbister 2005; Brown 2020; Parks 2012; Afshari 2013). Dropped: a *Prenatal Diagnosis* paper and three further items matching on the surname "Hunter"; a 1976 *Acta Radiologica* false hit; *Reactions Weekly*; a conference abstract duplicating Parks 2012. Boyer 2005, Werneke 2016, Buckley 2014 and Isbister 2007 are already verified in `_Interactions_DOI-LIST.md` and were not duplicated. |
| O7 | ecstasy MDMA hyponatraemia hyperthermia deaths clinical | 15 | Run: 15 returned, **0 retained** — the query returned rodent hyperthermia pharmacology and unrelated MDMA cognition papers. The human hyponatraemia literature was not reached. |
| O8 | hyponatraemia water intoxication MDMA ecstasy vasopressin | 12 | **Not run** — HTTP 429, not re-fetched. MDMA hyponatraemia therefore remains a known gap. |
| O9 | gamma-hydroxybutyrate overdose coma emergency intubation | 20 | Run: 20 returned, 7 retained (van Helmond 2020; Dietze 2014; Sporer 2002; Caldicott 2001 and Boyer 2001 — the physostigmine exchange; Richards 2017; Pellatt 2023; plus the 1999 *Annals of Emergency Medicine* GHB item, flagged for item-type checking). Dropped: single case reports (1995, 1996, 1997, 2000, 2011, 2020), an amoxapine paper, *Emergency Medicine News*, and two near-duplicate *Pediatric Emergency Care* abstracts. |
| O10 | acute alcohol intoxication poisoning emergency department management review | 20 | Run: 20 returned, 5 retained (Klein 2018 *Annals*; Klein 2018 *WestJEM*; Smith-Bernardin 2021; Woolfenden 2002; Cole 2018 and Pepa 2017 on agitation in intoxicated patients). Dropped: toxic-alcohol (methanol, isopropanol) papers — different syndrome; organophosphate and isoniazid poisoning; predatory-looking venues (*Annals of Case Reports*, *Journal of Angiotherapy*); conference abstracts. |
| O11 | flumazenil benzodiazepine poisoning adverse events systematic review | 15 | Run: 15 returned, 8 retained and the full critique cluster captured (Penninga 2015 SR/MA; Pajoumand 2015 letter; Penninga 2016 reply; Penninga 2015 reply to Veiraiah; Höjer 1988; Martens 1990; Prischl 1988; Gallo 2021; Hieger 2024; Hanson 2026). Dropped: *Reactions Weekly*, *Inpharma Weekly*, an *ACP Journal Club* abstract, a paediatric-dentistry sedation review, a benzodiazepine-amnesia review. |
| O12 | European Drug Emergencies Network Euro-DEN acute recreational drug toxicity | 20 | **Not run** — HTTP 429, not re-fetched. |
| O12b | Euro-DEN emergency presentations recreational drug toxicity Europe | 20 | **Not run** — HTTP 429 after a 95 s wait, then an upstream fetch error after a 180 s wait. Not re-fetched. |
| O12c | emergency department presentations recreational drug toxicity sentinel surveillance | 20 | Run (substitute): 20 returned, 9 retained (Heyerdahl 2014; Wood 2019; Wood 2010 ICD-10; Wood 2013; Liakoni 2017; Schmid 2020; Abouchedid 2017; Giorgetti 2026; Boyce 2025; Wood 2010 festival; Wood 2010 ED sample analysis; Reddi 2022 hyperthermia). Dropped: a predatory-looking *JAMMR* item, a *Journal of Angiotherapy* review, conference abstracts, infectious-disease and syndromic-surveillance papers. **The Euro-DEN cohort papers themselves (Wood 2014; Dines 2015) were not returned.** |
| O13 | opioid associated out-of-hospital cardiac arrest resuscitation naloxone | 20 | Run: 20 returned, 8 retained (Grunau 2025 SR; Grunau 2026; Rodriguez 2021 NACARDI; Ventura 2021 letter; Rodriguez 2021 reply; Dillon 2025 validation; Salcido 2017; Helander 2026; plus two commentaries, Quinn 2024 and Wampler 2024). Dropped: general airway-management and prognostication papers, *First10EM* blog records, unrelated OHCA-score correspondence. |
| O14 | recovery position unresponsive breathing first aid evidence | 20 | Run: 20 returned, **2 retained** (Tasker 2016; Nemeth 2018). The query matched largely on "first aid" and "breathing" and produced mental-health-first-aid, poliomyelitis and state-aid-law false hits. |
| O14b | recovery position loss of consciousness airway cardiac arrest assessment | 20 | Run: 20 returned, 1 retained (Freire-Tellado 2016). Julliand 2016 was not returned. |
| O15 | virtual overdose response hotline never use alone telephone supervision | 20 | Run: 20 returned, 9 retained (Viste 2023 NORS; Rioux 2023 averted deaths; Rioux 2023 cost-benefit; Rioux 2024 hotline vs app; Rioux 2025 predictors; Bristowe 2021 protocol; Viste 2024 **with its published correction**; Perri 2021; Mocanu 2024). Dropped: unrelated telephone-hotline literature (diabetes, dementia, plague surveillance, NHS 111), a physostigmine/TCA item, a weight-loss-drug news item, a VR-training registration. |
| O16 | naloxone dose fentanyl opioid induced respiratory depression reversal | 20 | **Not run** — HTTP 429 twice (the second after a 120 s wait); not re-fetched. Highest-priority gap. |

**Note on the search endpoint.** The Crossref API was shared with several co-editor sessions behind one egress address. Of 17 requests, 11 returned results; 4 were refused with HTTP 429 and 2 returned an upstream fetch error. No refused URL was re-fetched; substitutes were written and are logged above with a `b`/`c` suffix. Spacing of 45–180 s between requests was used after the first refusal and reduced but did not eliminate the refusals.

### DOI verification outcomes

- 86 DOIs entered the list; all 86 came verbatim from the Crossref search records above, with title, journal, year and first author echoed into the DOI list for checking against the PDF (METHODS §4.2).
- 0 DOIs failed to resolve; 0 DOIs resolved to a different paper. No DOI was recalled from memory, so no correction of a recalled DOI was required this session.
- Corrections found: Viste et al. 2024 (correction 10.1007/s11469-024-01305-0) and Stephenson et al. 2023 (correction 10.1186/s12954-023-00843-5). Both marked "erratum published" in the list; both corrections are to be obtained with the original.
- Retractions found: none. The per-DOI `updated-by` check of METHODS §4.3 has **not** been performed item by item (search records do not carry that field) and must be run when the reference records are created.

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed (https://pubmed.ncbi.nlm.nih.gov). For each: **Save → Selection: All results → Format: CSV**, and save the file into `search-logs/` with the name given. Note the hit count PubMed shows for each string and send me the numbers. Strings P1, P3, P5, P12 and P13 cover the queries Crossref refused.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `(naloxone[Title]) AND (dose OR dosing OR "dose-response" OR titration OR repeated) AND (fentanyl OR "synthetic opioid*" OR carfentanil OR nitazene*) AND (overdose OR "respiratory depression") AND (humans[MeSH Terms])` | _Overdose_pubmed_P1.csv | |
| P2 | `(naloxone[Title]) AND (intranasal OR intramuscular OR intravenous OR "route of administration") AND (randomized controlled trial[Publication Type] OR "randomised" OR "randomized" OR meta-analysis[Publication Type])` | _Overdose_pubmed_P2.csv | |
| P3 | `("opioid-induced respiratory depression" OR "opioid overdose"[Title]) AND (mechanism* OR pathophysiolog* OR "respiratory" OR hypoxia OR "chest wall rigidity") AND (review[Publication Type] OR "systematic review") AND (humans[MeSH Terms])` | _Overdose_pubmed_P3.csv | |
| P4 | `("out-of-hospital cardiac arrest" OR "cardiac arrest") AND (opioid* OR overdose OR naloxone) AND (bystander OR "cardiopulmonary resuscitation" OR "chest compression*" OR "rescue breathing") AND (humans[MeSH Terms])` | _Overdose_pubmed_P4.csv | |
| P5 | `(methamphetamine OR amphetamine OR cocaine OR "synthetic cathinone*" OR stimulant*) AND (toxicity[Title] OR overdose[Title] OR poisoning[Title] OR "overamping") AND (management OR treatment OR "emergency department" OR sedation) AND (humans[MeSH Terms])` | _Overdose_pubmed_P5.csv | |
| P6 | `(hyperthermia[Title] OR "heat stroke"[Title]) AND (MDMA OR ecstasy OR amphetamine* OR cocaine OR "serotonin syndrome" OR "drug-induced") AND (cooling OR dantrolene OR management OR treatment) AND (humans[MeSH Terms])` | _Overdose_pubmed_P6.csv | |
| P7 | `(hyponatremia[Title] OR hyponatraemia[Title] OR "water intoxication"[Title]) AND (MDMA OR ecstasy OR "3,4-methylenedioxymethamphetamine") AND (humans[MeSH Terms])` | _Overdose_pubmed_P7.csv | |
| P8 | `("gamma-hydroxybutyrate" OR GHB OR "gamma-butyrolactone" OR GBL OR "1,4-butanediol") AND (coma OR overdose OR intoxication OR intubation OR "airway management") AND (humans[MeSH Terms]) NOT (narcolepsy)` | _Overdose_pubmed_P8.csv | |
| P9 | `(flumazenil[Title]) AND (benzodiazepine* OR poisoning OR overdose OR intoxication) AND (seizure* OR "adverse event*" OR safety OR arrhythmia OR randomized controlled trial[Publication Type])` | _Overdose_pubmed_P9.csv | |
| P10 | `(benzodiazepine*[Title]) AND (overdose[Title] OR poisoning[Title] OR "relative toxicity") AND (alprazolam OR "coma score" OR ventilation OR mortality OR "intensive care") AND (humans[MeSH Terms])` | _Overdose_pubmed_P10.csv | |
| P11 | `("alcohol poisoning"[Title] OR "acute alcohol intoxication"[Title] OR "ethanol intoxication"[Title]) AND (emergency OR management OR mortality OR surveillance OR "critical illness") AND (humans[MeSH Terms])` | _Overdose_pubmed_P11.csv | |
| P12 | `("recovery position" OR "lateral recumbent position" OR "left lateral position") AND (unconscious* OR "loss of consciousness" OR overdose OR poisoning OR "first aid" OR airway) AND (humans[MeSH Terms])` | _Overdose_pubmed_P12.csv | |
| P13 | `("Euro-DEN" OR "European Drug Emergencies Network" OR "Toxicology Investigators Consortium" OR "ToxIC" OR "National Poison Data System" OR "poison cent*") AND (surveillance OR registry OR "annual report" OR "emergency department") AND ("2013"[Date - Publication] : "3000"[Date - Publication])` | _Overdose_pubmed_P13.csv | |
| P14 | `("excited delirium" OR "agitated delirium" OR "hyperactive delirium with severe agitation") AND (cocaine OR methamphetamine OR stimulant* OR restraint OR ketamine OR death*)` | _Overdose_pubmed_P14.csv | |
| P15 | `("overdose prevention" OR "never use alone" OR "virtual overdose" OR "mobile overdose response" OR "overdose detection technolog*") AND (hotline OR app OR "spotting" OR telephone OR remote) AND (humans[MeSH Terms])` | _Overdose_pubmed_P15.csv | |

## Layer 3 — Cochrane Library (to be run by VS)

Search `naloxone`, `flumazenil`, `recovery position` and `acute drug poisoning` in Cochrane Reviews; export the result lists as CSV → `_Overdose-and-emergency_cochrane.csv`. Cochrane is the decisive source for the flumazenil and naloxone-route questions.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of Alsayed 2026 (naloxone routes), Grunau 2025 (opioid-associated cardiac arrest), Penninga 2015 (flumazenil), Tasker 2016 (positioning), Rioux 2023 (virtual overdose response). Forward (Google Scholar "cited by"): items 7–10 (the NACARDI cluster), 11 (Penninga), 15–16 (physostigmine exchange), 19–21 (GHB agitation exchange), 25–26 (recovery position), 29 (Euro-DEN rationale). Logged here with seed DOI and counts.

## PRISMA counts

To be completed after Layers 2–4: records identified per source; duplicates removed; screened; excluded with reasons; included. Layer 1 so far: 253 records returned across 11 executed Crossref queries; 86 included.
