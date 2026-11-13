# W3 report: drug-checking services around the world

Checked on 2026-10-17. Output file: `/home/claude/drug-encyclopedia/data/site/drug-checking.json`.

**Result:** 72 services in 20 countries. 42 are `ai-checked` and 30 are `draft`. 52 are `active: yes` and 20 are `unclear`. 16 countries were searched and none was found.

**Important limit:** the shared WebSearch budget (200 searches per turn) ran out partway through Canada. After that I used WebFetch only, on pages already known or linked. So the United States, Latin America, Asia, Africa and the Middle East were covered only through overview reports and a few known pages, not searched country by country (see section 6). A follow-up run with a fresh search budget should cover them.

## 1. How it was read

- Every fact comes from a page read today with WebFetch (no browser, no shell downloads). WebFetch answers through a summarising model, so each `says` field paraphrases what it returned.
- `ai-checked`: the service's own page plus at least one independent source of an accepted type (government, EUDA, TEDI, a peer-reviewed paper or a reputable news report), and the two agree. Everything else is `draft`: only one source, no own page that could be read, or an independent source of another type (academic briefs, NGO reports).
- `active: unclear`: the newest sign is older than 2024, there is no dated sign, or funding ended or closures nearby make the status doubtful. The `note` gives the reason.
- No staff names, phone numbers or e-mail addresses are stored. Quotations are under 15 words (checked with `scripts/quote_limits.js`'s `longQuotes`: 0 found).
- Wikipedia and directories were used only to find services. Wikipedia's "Drug checking" article named almost nothing outside Europe.

## 2. Network and official overviews read (WebFetch)

- TEDI: `https://tedinetwork.org/?p=19` (About: member organisations) and `https://tedinetwork.org/` (member logos).
- EUDA: European Drug Report 2026, harm reduction (11 European countries reported drug checking in 2025, 12 in 2024; none named); EDR 2025 (twelve countries); Spotlight on drug checking (2023); TEDI data pages and factsheet; EUDA document-library entry on DIMS; EUDA webinar "International drug checking day" (30 Mar 2026: Energy Control, Trimbos, Kosmicare, Croatia's National Institute of Public Health).
- Switzerland: Federal Council report on Postulate Molina 22.4047 (24 Jun 2026); Infodrog NPS situation report 2025; FOPH page.
- Canada: CCSA *Environmental Scan of Drug-Checking Services in Canada* (11 Dec 2024; 30 organisations, 73 sites); HealthLink BC; BC HelpStartsHere; Island Health; Vancouver Coastal Health; Fraser, Interior and Northern Health; City of Toronto; CIUSSS Centre-Sud Montréal listing; Government of Saskatchewan (2023).
- Australia and New Zealand: Victoria Department of Health; NSW Health (Your Room); NZ Ministry of Health licensing page (5 licensed providers); UNSW evidence brief (Nov 2024).
- Germany: Berlin Senate press release (Feb 2025); Thuringian Landtag document.
- United States: NYC Health Department drug-checking implementation guide; Mathematica/ASPE environmental scan (2021, which names no current public services).
- Finding aids only: HRI *Global State of Harm Reduction 2024* regional chapters (Latin America & Caribbean, Asia, Eurasia, MENA, Eastern & Southern Africa, West & Central Africa, Oceania); NDARC *Profiles of drug checking services in 2017*.

## 3. Searches run (WebSearch, until the budget ran out)

- **English:** TEDI members; EUDA drug checking 2025/2026; Health Canada list; global surveys and reviews; The Loop; WEDINOS; Scotland/Glasgow; HSE Ireland; Ukraine; Bulgaria/Romania/Lithuania/Latvia (one combined query); Malta/Cyprus (combined); Sweden/Iceland/Estonia (combined); Greece; Genesis Act (five variants, including one extended search); Canadian provinces (Alberta, Saskatchewan, Manitoba, Ontario, Toronto, Yukon).
- **German:** Austria (Z6, Triptalks, taktisch klug, Vorarlberg, Kärnten/Klagenfurt); Switzerland (Infodrog, saferparty/DIZ, DIBS/Safer Dance, dib Bern/Biel, DILU/Tragwerk); Germany (Berlin, Länder model projects, Thüringen/SubCheck, NRW, Schleswig-Holstein, Mecklenburg-Vorpommern/Rostock/Fusion, Baden-Württemberg, Hessen, legal-high-inhaltsstoffe).
- **French:** Nuit Blanche (Geneva), NightLife Vaud, Modus Vivendi, Analyse ton prod', Quebec services.
- **Spanish:** Energy Control, Ai Laket!!. **Portuguese:** Kosmicare. **Italian:** drug checking Italia, Neutravel, Borgorete, Bologna/Milano/Roma.
- **Other languages:** Slovenian (DrogArt); Czech (testování drog, Progressive); Polish (testowanie substancji); Hungarian (drug checking, fesztivál); Danish (stoftest); Norwegian (rusmiddeltesting, Tryggere Ruspolitikk); Swedish (narkotikatestning, Riksdag); Finnish (huumeiden testaus, A-klinikka); Croatian (HZJZ, Terra, Štampar); Serbian (Re Generation); Slovak (Odyseus); Estonian (TAI); Greek (έλεγχος ουσιών; μείωση βλάβης φεστιβάλ).
- **After the budget ran out:** WebFetch of service sites and the overviews above (Montréal services, Ottawa, Winnipeg, Yukon, Alberta, PEI, US services, Australia, New Zealand, Colombia, Mexico, Argentina, Chile, Uruguay, Ukraine, Lithuania, France).

## 4. Per-country counts

| Country | Services | ai-checked | draft |
|---|---|---|---|
| Australia | 3 | 2 | 1 |
| Austria | 5 | 3 | 2 |
| Belgium | 1 | 1 | 0 |
| Canada | 28 | 10 | 18 |
| Colombia | 1 | 0 | 1 |
| Czechia | 1 | 1 | 0 |
| Estonia | 1 | 0 | 1 |
| France | 2 | 1 | 1 |
| Germany | 4 | 1 | 3 |
| Greece | 1 | 1 | 0 |
| Italy | 2 | 2 | 0 |
| Luxembourg | 1 | 1 | 0 |
| Netherlands | 1 | 1 | 0 |
| New Zealand | 3 | 2 | 1 |
| Portugal | 1 | 1 | 0 |
| Slovenia | 1 | 1 | 0 |
| Spain | 3 | 3 | 0 |
| Switzerland | 7 | 7 | 0 |
| United Kingdom | 3 | 3 | 0 |
| United States | 3 | 1 | 2 |
| **Total** | **72** | **42** | **30** |

Networks are one entry each: DIMS (33 testing facilities), Analyse ton prod' (200+ collection points), and the BC health authorities (Fraser, Interior, Northern, Vancouver Coastal). The note on each entry says where the site list is. Eleven Canadian entries rest only on the 2024 CCSA scan, and four only on the Montréal CIUSSS listing (with or without CCSA). They are `draft` and `unclear`.

## 5. Countries searched, none found (`countries_searched_none_found`)

- **Bulgaria, Romania, Latvia:** one combined English query, plus the HRI 2024 Eurasia chapter, which does not count them among the nine Eurasian countries with any drug checking. This was a shallow search.
- **Croatia:** Terra/Tripsitters (Rijeka) was still waiting for permission (Nov 2024), and a 2023 article says drug checking does not exist yet. The Štampar institute's free analysis for parents (Zagreb) appears only on a 2019 archived city page.
- **Cyprus, Malta:** one combined English query. Malta news says testing kits are needed; no service was found.
- **Denmark:** Danish searches found only parliamentary answers on drugging tests and street-drug monitoring.
- **Finland:** A-Clinic Foundation is a TEDI member, but no public service was found. A city initiative appears only as a proposal.
- **Hungary, Slovakia:** HRI 2024 reports only reagent-kit distribution by NGOs, which is not a service under this brief.
- **Iceland:** nothing found.
- **Ireland:** the HSE runs "back of house" checking at Electric Picnic (fourth year in 2025). Festival-goers can surrender drugs, but results feed alerts and no individual result is stated, so it is left out.
- **Norway:** the only service, run by Foreningen Tryggere Ruspolitikk/Rusopplysningen in Oslo since 2022, closed indefinitely in June 2026 for lack of funding. A 13 Oct 2026 headline, "Analysetjenesten i ny drakt!", hints at a relaunch; it is unsettled.
- **Poland:** OKO.press (29 Jul 2025) says there is no drug checking. SIN now refers people to test kits, and HRI 2024 mentions event work with kits and a kit business (PRO Test).
- **Serbia:** a 2018 report says drug checking is not allowed.
- **Sweden:** a Riksdag motion lists drug-checking countries, and Sweden is not among them.

## 6. Regions not searched country by country (WebSearch budget exhausted)

These countries are **not** in `countries_searched_none_found`.

- **United States:** only three services were checked (OnPoint NYC, the UNC Street Drug Analysis Lab, DanceSafe). Many state and city programmes probably exist, such as the NYC Health Department's checking at five syringe-service sites, named in the city guide.
- **Latin America:** HRI 2024 says peer-led colorimetric drug checking by civil society runs in Argentina, Brazil, Chile, Uruguay, Peru, Colombia and Mexico. Only Échele Cabeza (Colombia) is listed, as `draft`.
  - Mexico: Verter's page does not mention drug checking. ReverdeSer's domain now carries unrelated content.
  - Argentina: Intercambios' page does not mention drug checking.
  - Chile: Reduciendo Daño sells reagents and does field work, but no public testing is described.
  - Uruguay: the Imaginario 9 site blocks automated reading, and the service is profiled only in 2017.
  - Brazil and Peru: not checked.
- **Eurasia:**
  - Ukraine: HRI 2024 says the Drugstore project offers drug checking and online counselling through a website and the Free2Ask app. The page read did not confirm it.
  - Georgia: HRI 2024 mentions kits in syringe vending machines in Tbilisi and walk-in facilities.
  - Lithuania: Young Wave did reagent testing according to 2020 sources. Its 2026 site does not mention it.
- **Asia, Middle East and North Africa, East and Southern Africa, West and Central Africa:** the HRI 2024 chapters do not mention drug checking at all. No country-level searches were possible.

## 7. Services left out and why

- **Closed:**
  - CheQpoint (QuIHN, Queensland): no longer operating after legislative changes.
  - Prairie Harm Reduction (Saskatoon): site closed; drug checking unavailable in Saskatoon as of Apr 2026.
  - Rusopplysningen (Oslo): closed June 2026.
- **Not yet open:**
  - Glasgow (Hunter Street): due 5 Oct 2026 but postponed with no new date (Pharmaceutical Journal, 14 Oct 2026). Aberdeen and Dundee hold licences.
  - Hessen/Frankfurt (regulation in consultation, Aug 2026), Baden-Württemberg (not permitted, Feb 2026), North Rhine-Westphalia (regulation of Dec 2025, no running site found), Schleswig-Holstein (ordinance due end June 2026, no service found).
  - Nuremberg EviDriN (a research study).
  - PEERS Alliance (PEI): "anticipated" in the CCSA scan.
- **Not a qualifying service:**
  - HSE Ireland: back-of-house only.
  - legal-high-inhaltsstoffe.de: its own page says it offers no general drug checking; NPS are analysed case by case.
  - DrugsData/Erowid: not accepting samples, no change expected before 2027.
  - Techno+ (France): points to other services.
  - Reagent-kit sellers and distributors: SIN/PRO Test, Reduciendo Daño, DanceSafe's shop.
  - PHF Science (NZ laboratory partner) and the University of Auckland mushroom project (research).
  - Vernon Medicine Shoppe (CCSA: interview only).
- **Evidence too old or unreadable:**
  - Lab57 Bologna (2022 article only).
  - Hegoak Elkartea (Spain), DÁT2 Psy Help (Hungary), Imaginario 9 (Uruguay), ReverdeSer (Mexico) and BAONPS (Italy): 2017 profiles only.
  - Sydney Medically Supervised Injecting Centre: drug checking mentioned only in HRI 2024; Uniting's page does not confirm it.
- **Folded into other entries:**
  - Jellinek and GGD Amsterdam into DIMS.
  - Safer Dance Basel into DIBS.
  - Sunshine House and Nine Circles into Street Connections.
  - ANKORS and UBC HaRT into Interior Health.
  - Island partner sites into Substance.
  - Zurich's Kaserne mobile lab into Saferparty/DIZ.
  - The NYC Health Department programme into OnPoint NYC.

## 8. What I could not settle

1. **"Genesis Act" (Greece) was not found under that name** in English or Greek searches, including an extended search. The likely match is **Generation Act** (`generationact.gr`): a Greek harm-reduction organisation founded in late 2021 that offers reagent-based drug checking in nightlife, confirmed by LiFO (10 Feb 2025). It is listed as `ai-checked`. Please confirm with the senior author that this is what he meant.
2. **CanTEST (Canberra)** is `draft` because the only independent source is a UNSW evidence brief; the ACT Government page could not be fetched.
3. **The UNC lab, Rostock (Gesundheitsamt and Fusion), SubCheck and NorWest** have news or partner sources but no own page read, or no independent source.
4. **DanceSafe:** its own page describes free on-site checking, but no dated 2025–2026 event was found. The mail-in Transparency Testing service was not read.
5. **Canadian CCSA-only entries:** setting, method and current status were not checked. Ontario closed consumption sites in 2025 and Saskatchewan defunded Prairie Harm Reduction, so some may have stopped.
6. **Conflicting details between sources:**
   - Get Your Drugs Tested: 880 vs 649 East Hastings.
   - The Loop Bristol: 1 vs 11 Brunswick Square.
   - Spectre de rue: 1278 vs 1280 rue Ontario Est.
   - Fraser Health: 28 vs 35 locations.
   - dib Biel: start in 2020 vs 2022.
   - Kosmicare: fixed-site address and hours come from 2021.
   - dib Bern: details come from 2020.
7. **EUDA counts 11 European countries** with drug checking in 2025 without naming them. This list has 15 European countries with at least one service; the difference is not explained by the sources read.
8. **Estonia's TAI pilot** tests residues on drug-contaminated items, not drug samples. The editors should decide whether it belongs.
9. **Open status questions:** which NSW festivals take part from October 2026; whether Norway's service relaunches; whether Glasgow opens.
10. **WebFetch summaries** can be wrong in detail. Spot-check addresses and hours before publishing.
