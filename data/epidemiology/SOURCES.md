# Epidemiology layer — sources fetched (verification log)

Compiled 2026-10-15 by the AI co-editor. Every figure in `europe.json`, `greece.json`, `global.json` and `us.json` was checked against the text of the page or CSV listed below as fetched on that date; the sentence or CSV row used is stored in each record's `page_or_table`. No PDF was used. Pages were read through the WebFetch proxy (direct HTTPS to euda.europa.eu is blocked from this environment), which caps each page at roughly 100–120k characters of text and returns quotations in fragments; where a page was longer, the remainder was read with an offset.

## Pages and files fetched

| # | URL | Title (as shown) | Last update / date shown | Figures taken | Notes |
|---|---|---|---|---|---|
| 1 | https://euda.europa.eu/publications/european-drug-report/2026/drug-induced-deaths_en | Drug-induced deaths – the current situation in Europe (European Drug Report 2026) | Last update: 9 June 2026 | 13 (europe) | Read twice (two offsets). A third verification fetch was refused by the proxy with HTTP 429 and an instruction not to fetch the page again; figures taken only from the first two reads. |
| 2 | https://www.euda.europa.eu/publications/european-drug-report/2026_en | European Drug Report 2026: Trends and Developments | no "last update" field; states the report was launched 9 June 2026 and that "many of the annual national data sets included here are from the reference year January to December 2024" | 0 (chapter list only) | |
| 3 | https://www.euda.europa.eu/publications/european-drug-report/2026/cannabis_en | Cannabis – the current situation in Europe (European Drug Report 2026) | Last update: 9 June 2026 | 21 (europe) | Price figures are chart-only on the page and were not taken. |
| 4 | https://www.euda.europa.eu/publications/european-drug-report/2026/drug-situation-in-europe-up-to-2026_en | Understanding Europe's drug situation in 2026 – key developments (European Drug Report 2026) | Last update: 9 June 2026 | 0 | "At a glance" block is an image; its data were taken from the two CSVs (#6, #7) linked in its Source data section. |
| 5 | https://www.euda.europa.eu/publications/european-drug-report/2026/annex-tables_en | Annex tables to the European Drug Report 2026 | Last update: 9 June 2026 | 0 | Table cells render by script (blank in fetched text); the CSV versions (#19–#25) were used instead. |
| 6 | https://www.euda.europa.eu/sites/default/files/data/data-nodes/33313/versions/56/edr2026-at-a-glance-table-1_en.csv | Table EDR26-At-a-glance-1. Drug use in the EU in 2024, at a glance (amphetamines, cannabis, cocaine, MDMA) | (CSV; publication date of the source-data page 09.06.2026) | 19 (europe) | Verbatim CSV, 8 rows. |
| 7 | https://www.euda.europa.eu/sites/default/files/data/data-nodes/33313/versions/56/edr2026-at-a-glance-table-2_en.csv | Table EDR26-At-a-glance-2. Heroin and other opioids in the EU in 2024, at a glance | (CSV) | 0 directly (values cited inside opioid records: 855 000; 505000; 21; 66; 79; 34) | |
| 8 | https://www.euda.europa.eu/data/source-data/edr/2026/complete_en | European Drug Report 2026: Trends and Developments: source data | Publication date: 09.06.2026 | 0 | Source of the table titles and of the note "Graphics showing the most recent country-level data are based on studies carried out between 2015 and 2024". |
| 9 | https://www.euda.europa.eu/publications/european-drug-report/2026/cocaine_en | Cocaine – the current situation in Europe (European Drug Report 2026) | Last update: 9 June 2026 | 15 (europe) + 3 (greece: ESCAPE city values) | The page gives no total of all cocaine treatment entrants (first-time and crack only). |
| 10 | https://www.euda.europa.eu/publications/european-drug-report/2026/synthetic-stimulants_en | Synthetic stimulants – the current situation in Europe (European Drug Report 2026) | Last update: 9 June 2026 | 28 (europe) | Amphetamine, methamphetamine and synthetic cathinones. |
| 11 | https://www.euda.europa.eu/publications/european-drug-report/2026/mdma_en | MDMA – the current situation in Europe (European Drug Report 2026) | Last update: 9 June 2026 | 13 (europe) | No price values in the page text. |
| 12 | https://www.euda.europa.eu/publications/european-drug-report/2026/heroin-and-other-opioids_en | Heroin and other opioids – the current situation in Europe (European Drug Report 2026) | Last update: 9 June 2026 | 14 (europe) | |
| 13 | https://www.euda.europa.eu/publications/european-drug-report/2026/new-psychoactive-substances_en | New psychoactive substances – the current situation in Europe (European Drug Report 2026) | Last update: 9 June 2026 | 14 (europe) | Includes synthetic cannabinoids, cathinones, nitazenes/orphines. |
| 14 | https://www.euda.europa.eu/publications/european-drug-report/2026/other-drugs_en | Other drugs – the current situation in Europe (European Drug Report 2026) | Last update: 9 June 2026 | 32 (europe) | Ketamine, GHB/GBL, LSD, hallucinogenic mushrooms, DMT, new benzodiazepines. No nitrous oxide figures on the page. GHB/GBL seizure sentence has no year and was not taken. |
| 15 | https://www.euda.europa.eu/publications/european-drug-report/2026/opioid-agonist-treatment_en | Opioid agonist treatment – the current situation in Europe (European Drug Report 2026) | Last update: 9 June 2026 | 6 (europe) | |
| 16 | https://www.euda.europa.eu/publications/european-drug-report/2026/injecting-drug-use_en | Injecting drug use in Europe – the current situation (European Drug Report 2026) | Last update: 9 June 2026 | 6 (europe) + 2 (greece) | |
| 17 | https://www.euda.europa.eu/publications/european-drug-report/2026/drug-supply-production-and-precursors_en | Drug supply, production and precursors – the current situation in Europe (European Drug Report 2026) | Last update: 9 June 2026 | 7 (europe) | |
| 18 | https://www.euda.europa.eu/sites/default/files/data/data-nodes/33313/versions/56/edr2026-deaths-table-1_en.csv | Table EDR26-DRD-1. Characteristics of drug-induced deaths: numbers, 2024 or most recent year | (CSV) | 2 (europe) | Single row: 78,22,42,44,7589,8319,66. |
| 19 | https://www.euda.europa.eu/sites/default/files/data/data-nodes/33313/versions/56/edr2026-deaths-table-1c_en.csv | Table EDR26-DRD-1 (first listing) | (CSV) | 0 | Gives EU 7598 / EU+2 8328, which differs from #18 (7589 / 8319); noted, not used. |
| 20 | https://www.euda.europa.eu/sites/default/files/data/data-nodes/33313/versions/56/edr2026-gps-current-table-1_en.csv | Table EDR26-GPS-1. Prevalence of drug use in Europe, based on most recent general population surveys (2024 or most recent year) | (CSV) | 21 (greece) | All Greece rows are from the 2015 survey (n = 1519 adults, 464 young adults). File is truncated by the proxy after ~100k characters (ends inside Portugal); Greece rows complete. |
| 21 | https://www.euda.europa.eu/sites/default/files/data/data-nodes/33313/versions/56/edr2026-tdi-characteristics-table-1_en.csv | Table EDR26-TDI-1. Treatment demand indicator (TDI) source data, client characteristics, 2024 or most recent year | (CSV) | 0 | EU rows only (no Greece row); counts of first-time / previously treated entrants by primary drug kept for reference, not loaded. |
| 22 | https://www.euda.europa.eu/sites/default/files/data/data-nodes/33313/versions/56/edr2026-annex-table-1a-opioids-hr-estimate_en.csv | Table EDR26-Annex-table-1a. High-risk opioid use estimates for population aged 15–64 years, 2024 or most recent year | (CSV) | 1 (greece) | Greece: 2024, 0.8-1.2 per 1 000. |
| 23 | https://www.euda.europa.eu/sites/default/files/data/data-nodes/33313/versions/56/edr2026-annex-table-1d-opioids-oat_en.csv | Table EDR26-Annex-table-1d. Number of clients in opioid agonist treatment, 2024 or most recent year | (CSV) | 1 (greece) | Greece 8349; EU 504615; EU+Türkiye+Norway 516597. |
| 24 | https://www.euda.europa.eu/sites/default/files/data/data-nodes/33313/versions/56/edr2026-annex-table-1b-opioids-treatment_en.csv | Table EDR26-Annex-table-1b. Entrants into treatment during the year: opioids clients as a proportion of treatment demands, 2024 or most recent year | (CSV) | 2 (greece) | Greece 38.4% (1393); EU 21.2% (63003); EU+2 21.5% (67532). |
| 25 | https://www.euda.europa.eu/sites/default/files/data/data-nodes/33313/versions/56/edr2026-injecting-table-1a_en.csv and …/edr2026-injecting-table-1b_en.csv | Tables EDR26-INJ-1a/1b. Estimated number and prevalence of people who inject drugs, by country (latest available data for each country) | (CSV) | 2 (greece) | Greece 2056 persons; 0.31 per 1 000. Year not given in the CSV. |
| 26 | https://reliefweb.int/report/world/unodc-world-drug-report-2025 | UNODC World Drug Report 2025: Global instability compounding social, economic and security costs of the world drug problem | Vienna, 26 June 2025 (press release dateline) | 13 (global; 1 of them draft) | Verification source for the UNODC release; `url` in the records points to the UNODC report page (unodc.org is not reachable from here). |
| 27 | https://www.samhsa.gov/data/sites/default/files/reports/rpt56287/2024-nsduh-annual-national/2024-nsduh-annual-national-html-071425-edited/2024-nsduh-annual-national.htm | Key Substance Use and Mental Health Indicators in the United States: Results from the 2024 National Survey on Drug Use and Health (HHS Publication No. PEP25-07-007, NSDUH Series H-60) | Released 2025 (report page: publication date July 28, 2025) | 18 (us) | The proxy delivered only ~117k characters (through the "Opioid Misuse" section); the Substance Use Disorders and Treatment chapters were beyond the cut and were taken from the detailed tables (#28) instead. |
| 28 | https://www.samhsa.gov/data/sites/default/files/reports/rpt56484/NSDUHDetailedTabs2024/NSDUHDetailedTabs2024/2024-nsduh-detailed-tables-sect5pe.htm | 2024 NSDUH Detailed Tables, Section 5: Substance Use Disorder and Treatment Tables (Tables 5.1A/5.1B) | (table pages carry no date) | 30 (us) | Only the first ~190k characters were delivered (through Table 5.9A); the treatment-receipt tables were not reachable. |
| 29 | https://www.samhsa.gov/data/sites/default/files/reports/rpt56484/NSDUHDetailedTabs2024/NSDUHDetailedTabs2024/2024-nsduh-detailed-tables-toc.htm | 2024 NSDUH Detailed Tables — table of contents | — | 0 | Used to locate Section 5. |
| 30 | https://www.samhsa.gov/data/report/2024-nsduh-annual-national-report | 2024 NSDUH Annual National Report (CBHSQ Data) | Publication Date July 28, 2025 | 0 | Links only; also lists a "2025 NSDUH Annual National Report" (not fetched; outside the brief). |
| 31 | https://www.euda.europa.eu/countries/greece_en (redirects to the Reitox focal-point page) | Greek national focal point | — | 0 | No statistics; links to Statistical Bulletin 2026 pages whose tables load by script. |
| 32 | https://www.euda.europa.eu/data/stats2026/gps_en | Statistical Bulletin 2026 — prevalence of drug use | — | 0 | Tables load by script ("Tables will appear here"); nothing extractable. |
| 33 | https://www.euda.europa.eu/drugs-library/greek-report-drugs-alcohol-2024_en | Greek Report on Drugs & Alcohol 2024 (EKTEPN; Greek) | Publication date 5/06/2025 | 0 | Library entry only; the report is a PDF (not used). |
| 34 | https://www.ektepn.gr/publications/2024/ee2024 | ΕΚΤΕΠΝ — Ετήσια Έκθεση 2024 | not stated (says most data refer to 2022) | 0 | No figures in HTML; PDF only (not used). |

## Pages that could not be fetched

| URL | Result |
|---|---|
| https://www.euda.europa.eu/countries/drug-reports/2025/greece_en | Fetch error (page does not exist). No EUDA country drug report page for Greece was found for 2019–2025; the Greece figures in `greece.json` therefore come from the EDR 2026 source-data CSVs and chapter pages. |
| https://www.euda.europa.eu/countries/drug-reports/2019/greece_en | Fetch error (not found). |
| https://www.euda.europa.eu/node/2621_en ("Greece country overview") | Fetch error (not found). |
| https://www.samhsa.gov/newsroom/press-announcements/20250728/samhsa-releases-annual-national-survey-on-drug-use-and-health | Loaded without the press-release body (navigation only); no figures. |
| https://www.samhsa.gov/blog/release-2024-nsduh-leveraging-latest-substance-use-mental-health-data-make-america-healthy-again | Loaded without the article body; no figures. |
| https://www.samhsa.gov/data/release/2024-national-survey-drug-use-and-health-nsduh-releases | Fetch error. |
| https://euda.europa.eu/publications/european-drug-report/2026/drug-induced-deaths_en (third request) | Proxy HTTP 429 rate limit with "do not fetch again"; obeyed. |
| https://www.unodc.org/… | unodc.org is not reachable from this environment (not attempted; ReliefWeb reproduction used, as instructed). |

Not fetched by choice (lower priority for the monographs): EDR 2026 "Harm reduction" and "Drug-related infectious diseases" chapters; EDR 2025 pages were not needed because every 2026 chapter requested exists.

## Status summary

| File | Records | verified | draft |
|---|---|---|---|
| europe.json | 190 | 187 | 3 (fentanyl deaths 208/129/95; drug-induced deaths among women and men aged 50–64 — figures read from the drug-induced-deaths page by the extractor, but the sentence was not captured before the proxy rate-limited the page; re-check against the page before display) |
| greece.json | 32 | 32 | 0 |
| global.json | 13 | 12 | 1 (UNODC cocaine seizures 2,275 — unit word missing in the ReliefWeb reproduction) |
| us.json | 48 | 48 | 0 |

Overlaps with `landing.json`: `ep_global_any_drug_pastyear_users_2023` and `ep_global_treatment_coverage_2023` restate the two landing UNODC figures; `ep_eu_drug_induced_deaths_min_2024` restates `ep_eu_overdose_deaths_2024`. Ids differ, so the site must de-duplicate by figure when it merges files.

## Known discrepancies inside the sources

- EU drug-induced deaths 2024: page and Table EDR26-DRD-1 give 7 589 (EU) / 8 319 (EU+2); the CSV labelled "Table EDR26-DRD-1 (first listing)" gives 7 598 / 8 328; the page's narrative says "almost 7 600" (provisional overall estimate) versus the "minimum estimate of 7 589". Records use 7 589 / 8 319.
- Methamphetamine laboratories dismantled in 2023: 251 (synthetic stimulants page) versus 250 (drug supply page).
- Opioid agonist treatment clients: pages say 505 000 / 517 000; Annex table 1d CSV gives 504615 / 516597.
- Ketamine drug-checking samples containing only the expected substance, 2025: 82% (1 306) in the key-data section versus 83% in the narrative (not loaded).
- UNODC cocaine seizures 2023: the ReliefWeb reproduction prints "2,275–" without the unit word; recorded as draft pending the UNODC primary.
- The "at a glance" EU prevalence estimates carry no survey year in the CSV; the year basis used in the records is the table title ("Drug use in the EU in 2024") plus the source-data page note that country-level graphics are based on studies carried out between 2015 and 2024; the amphetamine and MDMA chapter sentences themselves give "2018 and 2024" and "2015 and 2024".
