# Mescaline (and peyote / San Pedro) — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-16 before screening; re-worded re-runs of refused or errored URLs are listed as such.

## Layer 1 — Crossref bibliographic search (run by AI co-editor, 2026-10-16)

Endpoint: `https://api.crossref.org/works?query.bibliographic=<terms>&filter=type:journal-article&rows=15&select=DOI,title,container-title,issued,is-referenced-by-count,author&sort=relevance`.

Environment: about half of all Crossref calls were refused with HTTP 429 or returned an unexplained client error; each refusal was followed by a 65–185 s pause and the refused URL was never re-fetched. One URL was refused for length and shortened.

### Carried forward from other substances' searches

Four mescaline papers surfaced while searching for LSD, DMT and 5-MeO-DMT and were carried into this map rather than re-queried:

| Source query | Paper retained |
|---|---|
| LSD query L1b ("acute dose-dependent effects LSD healthy subjects Holze Liechti") | Klaiber et al. 2024, acute dose-dependent effects of mescaline (Transl Psychiatry, 10.1038/s41398-024-03116-2) |
| DMT query D6 ("acute effects intravenous DMT healthy participants randomized placebo") | Ley et al. 2023, comparative acute effects of mescaline, LSD and psilocybin (Neuropsychopharmacology, 10.1038/s41386-023-01607-2) |
| 5-MeO-DMT query M1 ("5-MeO-DMT naturalistic use survey subjective effects Davis Uthaug") | Uthaug et al. 2021, epidemiology of mescaline use (J Psychopharmacol, 10.1177/02698811211013583); Agin-Liebes et al. 2021, naturalistic mescaline use (ACS Pharmacol Transl Sci, 10.1021/acsptsci.1c00018) |

### Section-level queries

| # | Query string | Result |
|---|---|---|
| Me1 | mescaline pharmacokinetics acute effects healthy subjects Ley Liechti | 15 hits, 4 retained (Mueller 2025 Clin Pharmacokinet; Klaiber 2024b BJCP safety pharmacology; Klaiber 2024a [already held]; Ley 2023 [already held]). Six Neuroscience Applied abstracts from the same programme were dropped |
| Me2 | peyote Native American Church psychological neuropsychological Halpern | 15 hits, 3 retained (Halpern 2005 Biol Psychiatry; Jones 2007; Pascarosa 1976). Nine of the fifteen were law-review articles and book reviews of *The Peyote Road* |
| Me3 | mescaline peyote San Pedro cactus toxicity intoxication case report | 15 hits, 5 retained (Engel 2023; Engel 2025 + its corrigendum; Casado 2008; LeBlanc 2021; Cengisiz 2016) |
| Me4 | mescaline pharmacology review history hallucinogen receptor clinical | 15 hits, 1 retained (Klaiber 2024b, already held). The query returned rodent drug-discrimination and head-twitch pharmacology from 1973–2018 — no modern human pharmacology review surfaced here |
| Me5 | dark classics chemical neuroscience mescaline peyote forensic repercussions | client error; re-run as "mescaline pharmacokinetics pharmacodynamics peyote clinical forensic repercussions" — refused (429), then refused for URL length; shortened and re-run as Me5c |
| Me5c | mescaline pharmacokinetics peyote clinical forensic repercussions | 15 hits, 6 retained (Dinis-Oliveira 2019; Carstairs 2010; Gambelunghe 2012; Doesburg-van Kleffens 2023; Kirschner 2023; Bloom 1975; Chao 1978). **The single most productive query for this substance** — it recovered both the pharmacology review and the only toxicity series |
| Me6 | Hermle mescaline PET model psychosis healthy volunteers 1992 | **Not run** (window closed) — the pre-Basel controlled human administrations are therefore missing |
| Me7 | San Pedro Echinopsis Trichocereus pachanoi mescaline alkaloid content | **Not run** (window closed) — no verified source on San Pedro alkaloid content |

### DOI corrections and update checks
- No DOI in this list was recalled from memory; all were copied verbatim from Crossref search responses, so no `works/<DOI>` re-fetch was required.
- Corrigendum found and marked: Engel et al. 2025, "The trouble with psychedelic cacti" (Contemp Drug Probl) has a corrigendum registered as its own record (10.1177/00914509251345098). The parent paper is kept and marked.
- Duplicate/abstract records noted and not listed: Klaiber 2024 safety pharmacology appears both as the BJCP article (listed) and as a Neuroscience Applied abstract (10.1016/j.nsa.2024.105143, dropped); the Basel empathy study exists only as an abstract (10.1016/j.nsa.2025.106577) and was excluded pending full publication.
- Retractions: none.

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed (https://pubmed.ncbi.nlm.nih.gov). For each: **Save → Selection: All results → Format: CSV**, and save the file into `search-logs/` with the name given. Note the hit count shown next to each string and send me the numbers. P6 and P7 target the two gaps Crossref would not close: the 1990s German controlled studies and the San Pedro alkaloid-content literature.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `(mescaline[Title] OR peyote[Title] OR "Lophophora"[Title]) AND (humans[MeSH Terms])` | mescaline_pubmed_P1.csv | |
| P2 | `(mescaline[Title]) AND (pharmacokinetic* OR "plasma concentration" OR bioavailability OR "urinary recovery" OR metabolism)` | mescaline_pubmed_P2.csv | |
| P3 | `(mescaline[Title]) AND (dose OR "dose-response" OR "dose-dependent") AND ("healthy volunteers"[MeSH Terms] OR "healthy subjects" OR "healthy participants")` | mescaline_pubmed_P3.csv | |
| P4 | `(peyote[Title/Abstract] OR mescaline[Title/Abstract]) AND ("Native American" OR "Indians, North American"[MeSH Terms] OR "Native American Church" OR ceremon*)` | mescaline_pubmed_P4.csv | |
| P5 | `(mescaline OR peyote OR "San Pedro cactus" OR Trichocereus OR Echinopsis) AND (toxicity OR poisoning OR overdose OR "emergency department" OR death OR fatal*)` | mescaline_pubmed_P5.csv | |
| P6 | `(mescaline) AND (PET OR "positron emission" OR SPECT OR EEG OR neuroimaging OR "model psychosis") AND (humans[MeSH Terms])` | mescaline_pubmed_P6.csv | |
| P7 | `("San Pedro" OR Trichocereus OR "Echinopsis pachanoi" OR "Echinopsis peruviana" OR wachuma) AND (mescaline OR alkaloid*)` | mescaline_pubmed_P7.csv | |
| P8 | `(mescaline[Title]) AND (receptor OR "5-HT2A" OR binding OR affinity OR "structure-activity")` | mescaline_pubmed_P8.csv | |
| P9 | `(mescaline OR peyote) AND (prevalence OR trends OR survey OR epidemiolog* OR NSDUH)` | mescaline_pubmed_P9.csv | |
| P10 | `(mescaline OR peyote) AND (dependence OR tolerance OR withdrawal OR "use disorder")` | mescaline_pubmed_P10.csv | |
| P11 | `(mescaline OR peyote) AND (pregnan* OR teratogen* OR chromosom* OR genotoxic*)` | mescaline_pubmed_P11.csv | |
| P12 | `(peyote OR "Lophophora williamsii") AND (conservation OR sustainab* OR harvest* OR population*)` | mescaline_pubmed_P12.csv | |

## Layer 3 — grey literature (VS)

UNODC World Drug Report 2025; EUDA European Drug Report 2026 and Statistical Bulletin; the US American Indian Religious Freedom Act Amendments 1994 and DEA guidance on the peyote exemption; Texas DPS peyote distributor and harvest statistics; IUCN Red List assessment of *Lophophora williamsii*; Indigenous Peyote Conservation Initiative report; SAMHSA NSDUH 2024 detailed tables; Global Drug Survey latest. Saved to `PDFs/_Epidemiology/` with the names in the DOI list's reports table.
