# 5-MeO-DMT — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-16 before screening; re-worded re-runs of refused or errored URLs are listed as such.

## Layer 1 — Crossref bibliographic search (run by AI co-editor, 2026-10-16)

Endpoint: `https://api.crossref.org/works?query.bibliographic=<terms>&filter=type:journal-article&rows=15&select=DOI,title,container-title,issued,is-referenced-by-count,author&sort=relevance`.

Environment: about half of all Crossref calls were refused with HTTP 429 or returned an unexplained client error; each refusal was followed by a 65–185 s pause and the refused URL was never re-fetched.

Search note: unlike "2C-B", the token "5-MeO-DMT" is matched well by Crossref's bibliographic index, and the spelled-out form "5-methoxy-N,N-dimethyltryptamine" retrieves the forensic literature that the abbreviation misses (compare M1 and M4).

### Section-level queries

| # | Query string | Result |
|---|---|---|
| M1 | 5-MeO-DMT naturalistic use survey subjective effects Davis Uthaug | 15 hits, 9 retained (Uthaug 2020; Davis 2018; Reckweg 2022; Lancelotta 2020; Uthaug 2019; Ortiz Bernal 2025; Lancelotta 2022; Ortiz Bernal 2026; Davis 2019; Griffiths 2019). Also surfaced, and carried forward to the Mescaline list: **Uthaug et al. 2021, epidemiology of mescaline use (J Psychopharmacol, 10.1177/02698811211013583)** and **Agin-Liebes et al. 2021, naturalistic mescaline use (ACS Pharmacol Transl Sci, 10.1021/acsptsci.1c00018)**; and for the DMT list, Cakic et al. 2010 (Drug Alcohol Depend, 10.1016/j.drugalcdep.2010.03.015) |
| M2 | vaporized 5-MeO-DMT GH001 phase 1 dose-ranging safety psychoactive | client error; re-run as M2b |
| M2b | 5-MeO-DMT inhalation clinical trial healthy volunteers Reckweg Ramaekers | 15 hits, 2 retained (Reckweg 2021 Front Pharmacol; Reckweg 2025 Front Psychol). The Neuroscience Applied and European Psychiatry abstract duplicates of the phase 1 trial were dropped; Rucker 2023 (Biol Psychiatry abstract, intranasal 5-MeO-DMT safety and PK) was noted as an abstract whose full publication should be sought |
| M3 | 5-MeO-DMT toxicity death seizure unconsciousness case report fatal | URL refused (429); re-run as M3b |
| M3b | 5-methoxy-N,N-dimethyltryptamine fatal intoxication toxicology case | 15 hits, 2 retained (Sklerov 2005; Jurowski 2026). The remaining thirteen were fatal intoxications with unrelated substances — **no case report of seizure or loss of consciousness after 5-MeO-DMT surfaced**, which is recorded as the most important gap in this map |
| M4 | Bufo Incilius alvarius toad secretion bufotenine 5-MeO-DMT conservation | 15 hits, 3 retained (Wilkins 2026 veterinary intoxication series; Hayes 2025; Ortiz Bernal 2026 [already held]). The rest were amphibian ecology, conservation and anatomy |
| M5 | 5-MeO-DMT 5-HT1A 5-HT2A receptor pharmacology metabolism humans | client error. **Not re-run** — the receptor-pharmacology question is therefore covered only narratively inside Reckweg 2022 (item 1); recorded as a gap |
| M6 | 5-MeO-DMT depression treatment open label trial therapeutic potential | 15 hits, 4 retained (Seynaeve 2026 CNS Drugs; Marsden 2025 Addiction; Kargbo 2021; Kargbo 2024) |
| M7 | 5-MeO-DMT pharmacokinetics plasma concentration humans | **Not run** (window closed) — no human PK source in this list |

### DOI corrections and update checks
- No DOI in this list was recalled from memory; all were copied verbatim from Crossref search responses, so no `works/<DOI>` re-fetch was required.
- Duplicate records noted and not listed twice: Reckweg's GH001 phase 1 trial appears as the Front Pharmacol article (10.3389/fphar.2021.760671, listed), a Neuroscience Applied abstract (10.1016/j.nsa.2022.100703, dropped) and a European Psychiatry abstract (10.1192/j.eurpsy.2022.1846, dropped).
- Retractions: none. Errata: none on any retained item.

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed (https://pubmed.ncbi.nlm.nih.gov). For each: **Save → Selection: All results → Format: CSV**, and save the file into `search-logs/` with the name given. Note the hit count shown next to each string and send me the numbers. **P4 is the priority** — it targets the seizure and loss-of-consciousness literature that Crossref would not surface.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `("5-MeO-DMT" OR "5-methoxy-N,N-dimethyltryptamine" OR "5-methoxy-DMT")` | 5meodmt_pubmed_P1.csv | |
| P2 | `("5-MeO-DMT" OR "5-methoxy-N,N-dimethyltryptamine") AND (humans[MeSH Terms]) AND (trial OR "clinical trial"[Publication Type] OR "phase 1" OR "phase 2")` | 5meodmt_pubmed_P2.csv | |
| P3 | `("5-MeO-DMT" OR "5-methoxy-N,N-dimethyltryptamine") AND (pharmacokinetic* OR "plasma concentration" OR metabolism OR CYP2D6 OR bioavailability)` | 5meodmt_pubmed_P3.csv | |
| P4 | `("5-MeO-DMT" OR "5-methoxy-N,N-dimethyltryptamine" OR "toad venom" OR "Bufo alvarius" OR "Incilius alvarius") AND (seizure* OR convulsion* OR "loss of consciousness" OR unresponsive* OR apnea OR apnoea OR "respiratory arrest" OR "emergency department")` | 5meodmt_pubmed_P4.csv | |
| P5 | `("5-MeO-DMT" OR "5-methoxy-N,N-dimethyltryptamine") AND (death OR deaths OR fatal* OR postmortem OR "post-mortem" OR toxicity)` | 5meodmt_pubmed_P5.csv | |
| P6 | `("5-MeO-DMT" OR "5-methoxy-N,N-dimethyltryptamine" OR bufotenin*) AND (MAOI OR "monoamine oxidase inhibitor" OR harmine OR ayahuasca OR "serotonin syndrome" OR "serotonin toxicity")` | 5meodmt_pubmed_P6.csv | |
| P7 | `("5-MeO-DMT" OR "5-methoxy-N,N-dimethyltryptamine") AND ("5-HT1A" OR "5-HT2A" OR receptor OR binding OR affinity OR agonist)` | 5meodmt_pubmed_P7.csv | |
| P8 | `("Bufo alvarius" OR "Incilius alvarius" OR "Sonoran Desert toad" OR "Colorado River toad") AND (5-MeO-DMT OR bufotenin* OR secretion OR venom)` | 5meodmt_pubmed_P8.csv | |
| P9 | `("5-MeO-DMT" OR "5-methoxy-N,N-dimethyltryptamine") AND (naturalistic OR ceremon* OR retreat OR survey OR epidemiolog*)` | 5meodmt_pubmed_P9.csv | |
| P10 | `("5-MeO-DMT" OR "5-methoxy-N,N-dimethyltryptamine") AND (depression OR "alcohol use disorder" OR anxiety OR "treatment-resistant")` | 5meodmt_pubmed_P10.csv | |
| P11 | `("5-MeO-DMT") AND (reactivation* OR "persisting" OR "extended difficulties" OR HPPD OR psychosis)` | 5meodmt_pubmed_P11.csv | |
| P12 | `(bufotenin* OR "5-OH-DMT") AND (humans[MeSH Terms])` | 5meodmt_pubmed_P12.csv | |

## Layer 3 — grey literature (VS)

UNODC Early Warning Advisory (tryptamines) and World Drug Report 2025 NPS booklet; EUDA EDND notifications and EWS alerts for 5-MeO-DMT; WHO ECDD review documentation; US DEA Schedule I final rule (2011); IUCN Red List and Arizona/New Mexico wildlife-agency assessments of *Incilius alvarius*; Global Drug Survey latest. Saved to `PDFs/_Epidemiology/` with the names in the DOI list's reports table.
