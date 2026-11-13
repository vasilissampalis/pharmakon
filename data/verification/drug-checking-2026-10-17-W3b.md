# W3b report: drug-checking services, regions not yet searched

Checked on 2026-10-17. Output file: `/home/claude/drug-encyclopedia/data/site/drug-checking.json`. The version before this pass is kept at `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/w3b/drug-checking.before-W3b.json`.

**Result:** 100 services in 24 countries (was 72 in 20).
- 59 are `ai-checked` and 41 `draft`.
- 82 are `active: yes` and 18 `unclear`.
- 28 services were added. 23 existing entries got new sources or corrections: the 18 Canadian drafts, plus UNC, DanceSafe, OnPoint NYC, Échele Cabeza and Generation Act.
- `countries_searched_none_found` now has 71 countries (55 added).
- No entry was deleted.

## 1. How it was read

- The W3 rules are unchanged:
  - Every fact comes from a page read today with WebFetch (no browser, no shell downloads), and each `says` field paraphrases what WebFetch returned.
  - About 111 WebSearch calls were used. The budget was not exhausted.
- `ai-checked` means the service's own page (or its own description) plus at least one agreeing independent source. I kept the first reader's convention: a service with no own page read stays `draft`, even when two independent sources agree.
- Where a health department runs the service, its page counts as the own page, and a second publisher was still required.
- Privacy and quotations:
  - No staff names, phone numbers or e-mail addresses are stored. A regex screen found 0.
  - Quotations were checked with `scripts/quote_limits.js` `longQuotes` on every text field: 0 over 15 words.
- The JSON was validated:
  - It parses in Node and Python.
  - All required keys and enumerations are present.
  - It has no duplicates and nothing was deleted.
  - It is sorted by country, then name: lowercase code-point order, the convention the existing file used.

## 2. Per-country counts

| Country | Services | ai-checked | draft | Change |
|---|---|---|---|---|
| Argentina | 1 | 0 | 1 | new |
| Australia | 3 | 2 | 1 | |
| Austria | 5 | 3 | 2 | |
| Belgium | 1 | 1 | 0 | |
| Brazil | 1 | 0 | 1 | new |
| Canada | 35 | 14 | 21 | +7; 18 drafts re-checked |
| Chile | 1 | 1 | 0 | new |
| Colombia | 1 | 1 | 0 | upgraded |
| Czechia | 1 | 1 | 0 | |
| Estonia | 1 | 0 | 1 | |
| France | 2 | 1 | 1 | |
| Germany | 4 | 1 | 3 | |
| Greece | 2 | 1 | 1 | +1 |
| Italy | 2 | 2 | 0 | |
| Luxembourg | 1 | 1 | 0 | |
| Mexico | 2 | 1 | 1 | new |
| Netherlands | 1 | 1 | 0 | |
| New Zealand | 3 | 2 | 1 | |
| Portugal | 1 | 1 | 0 | |
| Slovenia | 1 | 1 | 0 | |
| Spain | 3 | 3 | 0 | |
| Switzerland | 7 | 7 | 0 | |
| United Kingdom | 3 | 3 | 0 | |
| United States | 18 | 11 | 7 | +15 |
| **Total** | **100** | **59** | **41** | |

## 3. United States

**National sources read:**
- RTI International, *Advanced Drug Checking Services* (CDC-funded, 2026)
- NACCHO landscape article (Nov 2025)
- Network for Public Health Law practitioner webinar slides (Sept 2025)
- NDEWS harm-reduction-organisation report (Spring 2025)
- MIT Technology Review on NIST RaDAR (Apr 2025)
- DrugsData's list of testing resources
- The Harm Reduction Innovation Lab's North American directory, which needs a login and could not be read

**Added (15):**
- NYC Health Department drug checking at syringe service programmes: ai-checked.
- New York State Department of Health community drug checking (14 sites): ai-checked, though the only independent source is a student newspaper.
- Massachusetts MADDS/StreetCheck: ai-checked.
- SCOPE (San Francisco AIDS Foundation): ai-checked.
- Drug Checking Los Angeles: ai-checked, unclear.
- Washington State Community Drug Checking Network: draft.
- Outside In (Portland): ai-checked.
- Maryland Rapid Analysis of Drugs: ai-checked.
- Check It van (Johns Hopkins, Baltimore): ai-checked.
- Vermont Community Drug-Checking Program: ai-checked.
- Grand Rapids Red Project: draft, unclear. The only report is from 2023, and the organisation's 2026 pages do not mention drug checking.
- Chicago Recovery Alliance: draft, unclear (2019).
- New Mexico adulterant checking programme: draft.
- Southside Harm Reduction Services (Minneapolis): draft. The only source is a job posting.
- Transparency Testing (paid mail-in service, DanceSafe's partner): draft.

**Updated:**
- UNC Street Drug Analysis Lab is now ai-checked (Filter 2022; RTI 2026).
- DanceSafe is still unclear:
  - Its events page was last updated June 2024 and lists no events.
  - A Feb 2026 notice covers only leadership changes.
- OnPoint NYC gets the city's site and day listing.

**Searched one state at a time (21):** NY, MA, RI, CT, VT, ME, NH, CA, WA, OR, MD, PA, MI, IL, WI, MN, NM, CO, NV, NC, FL.

**Searched only together with other states (11):** NJ, DE, VA, OH, TX, AZ, GA, HI, AK, UT, LA. These were combined queries, so shallow. DC and Puerto Rico were also searched.

**Not searched (18):** AL, AR, ID, IN, IA, KS, KY, MS, MO, MT, NE, ND, OK, SC, SD, TN, WV, WY.

**NIST RaDAR** analyses residue for about 65 sites in 14 states (April 2025). Its partner sites are not named, so it is described in the Maryland note rather than listed separately.

## 4. Canada

**Main new source:** the CCSA Drug Checking Working Group *2025 Symposium Report* (French edition, May 2025). It covers the national days in Montréal, 24–25 February 2025, and names services that presented or hosted site visits. Being named there is a 2025 sign of activity. It does not prove the service runs today.

**The 18 drafts:**

| Entry | Now | Second source? | Basis |
|---|---|---|---|
| AAWEAR (Calgary) | unclear, draft | no | no sign after early 2024 |
| Be Safe (SK) | unclear, draft | no | nothing found |
| Blood Ties Four Directions (Whitehorse) | yes, **ai-checked** | yes | own page lists the programme; Government of Yukon (Oct 2024); CATIE (FTIR + strips); CBC (undated) |
| CIPTO (Outaouais) | yes, draft | CCSA only | 2025 symposium |
| Dopamine (Montréal) | yes, draft | CCSA + CIUSSS | 2025 symposium |
| Ensemble (NB) | unclear, draft | no | Health Canada grant record does not mention drug checking |
| Four Counties (ON) | unclear, draft | no | nothing found |
| GRIP Montréal | yes, draft | CCSA + CIUSSS | own page does not mention analysis |
| L'Anonyme (Montréal) | yes, **ai-checked** | yes | own page (Aug 2026): spectrometer on the mobile supervised injection service |
| Mountainside (BC) | yes, draft | CCSA + BCCSU blog | mobile FTIR, Fraser-Salish region |
| Newo Yotina (Regina) | yes, draft | yes, no own page | CBC, 20 Jun 2025: free drug testing after reopening |
| NorWest (Thunder Bay) | yes, draft | no new source | June 2025 news stands |
| Ottawa Inner City Health | unclear, draft | CBC (undated) added | no 2025–26 sign |
| SABSA (Québec City) | yes, draft | CCSA | own page does not mention analysis |
| Sandy Hill CHC – Oasis (Ottawa) | unclear, draft | CBC, uOttawa 2020 added | own site unreadable |
| Sub Check (PACT de rue) | yes, draft | CCSA + CIUSSS | 211 Québec listing (Jul 2026) used only as a finding aid |
| Wahkohtowin (SK) | unclear, draft | no | nothing found |
| Yukon EMS | unclear, draft | no | the only Yukon service found is Blood Ties' supervised consumption site |

**Added (7):**
- Spectrum Drug Testing (Edmonton): ai-checked.
- Avenue B mobile drug checking (Saint John): ai-checked.
- Tla'amin Nation drug checking (qathet, BC): draft.
- BRAS Outaouais: draft.
- Nomade, L'Oasis's mobile unit (Laval): draft.
- Travail de rue de Chicoutimi: draft.
- Ontario's Drug Checking Community, which includes the Kingston Integrated Care Hub: draft.

**Provinces finished:**
- Nova Scotia: none found. A June 2026 news report mentions no service.
- Newfoundland and Labrador, Northwest Territories and Nunavut: none found.
- Other Ontario and Québec cities: searched.
- Kitchener: a supervised consumption site's machine had uncertain funding in Aug 2024. It was not added.

## 5. Latin America and the Caribbean

**Added:**
- Mexico:
  - Checa tu Sustancia (Instituto RIA): ai-checked. Its own description is a Harm Reduction International 2025 conference page; there are three news reports (2024–2026).
  - ReverdeSer: draft, unclear. The only source is a 2023 peer-reviewed paper.
- Chile: Reduciendo Daño's event checking: ai-checked. A peer-reviewed case study describes 22 events in 2024; the first reader had left this out.
- Argentina: Intercambios' PAF!: draft, unclear. The only source is an undated article, and a 2023 report says no testing at parties.
- Brazil: Senta: draft, unclear (2022).

**Upgraded:** Colombia's Échele Cabeza is now ai-checked (Publimetro, 28 Mar 2025). It also does weekend analysis in Medellín and Cali.

**None found:**
- Peru.
- Uruguay: only roadside police testing (2023).
- Costa Rica, Ecuador, Guatemala, Paraguay and Bolivia: one combined Spanish query.
- Jamaica, Trinidad and Tobago, Dominican Republic, Barbados and Bahamas: one combined query.
- Puerto Rico: the 2023 ASSMCA notes recommend tools, which implies no service.

**Not searched:** Venezuela, Cuba, Central American states other than those above, Haiti and smaller Caribbean states.

## 6. Asia, the Middle East and Africa

Nothing qualifying was found. Searches were in:
- Japanese, Korean, Traditional and Simplified Chinese, Thai, Indonesian and Vietnamese
- Hebrew, Turkish, Arabic and Persian
- English for the rest

**Near misses:**
- Thailand: a 2023 government list of harm-reduction services includes "drug checking" without details (Raks Thai presentation, June 2024).
- Israel: Time Out (2022) says only reagent kits are sold, and people are pointed to Energy Control abroad.
- South Africa: a TB HIV Care job posting (Mar 2026) mentions drug surveillance, including testing residue in returned needles. That is not a public service.

**Added to none-found:**
- Asia: Japan, South Korea, China, Hong Kong, Taiwan, Thailand, India, Indonesia, Philippines, Vietnam, Malaysia, Singapore, Nepal, Kazakhstan
- Middle East: Israel, Türkiye, Lebanon, Iran, Jordan
- Africa: Egypt, Morocco, South Africa, Kenya, Nigeria, Tanzania, Ghana, Senegal

Several of these were covered by one combined query only.

## 7. European countries not searched before

**None found:**
- Ukraine: the Drugstore project's PartyBox includes reagents for self-testing. That is a kit, not a service.
- Lithuania: the 2025 national monitoring report does not mention drug checking.
- Georgia: reagents and strips are sold in syringe vending machines for self-testing (2023 study).
- Albania, Bosnia and Herzegovina, Kosovo, Montenegro and North Macedonia: one combined query.
- Russia, Belarus, Moldova and Armenia: one Russian query.
- Andorra, Liechtenstein, Monaco and San Marino: one combined query.

**Not searched:** Azerbaijan and Vatican City.

**Norway:** one search did not settle the possible relaunch.

## 8. Greece

**Generation Act:**
- No second independent source was found in Greek or English. The two LiFO URLs are the same article (10 Feb 2025). A Resident Advisor listing (26 Oct 2024) shows only a harm-reduction workshop.
- The entry stays ai-checked on its own page plus LiFO, as the first reader set it.
- "Genesis Act" was not found under that name.

**New: STEKI 46**, OKANA's supervised consumption space at Kapodistriou 46, Athens:
- Parapolitika (5 Apr 2024) reports a "drug checking machine" for clients.
- *Harm Reduction Journal* (Jan 2026) says on-site drug checking is now offered.
- It is draft because OKANA's own page does not mention it.

## 9. Left out and why

- **Research studies or not yet running:**
  - Rhode Island CUTS: a research cohort; locations are not public.
  - Maine Project DHARMA: still working out how to deliver results.
  - Wisconsin NOCAP (Madison): proposed, not open (June 2025).
  - Michigan's first FTIR service: pre-implementation study, 2025.
  - Clinical trials in California.
- **Stopped or not a public service:**
  - Philadelphia's health department programme: a respondent in the NDEWS 2025 report says it was discontinued.
  - CFSRE: publishes laboratory reports only.
- **Unclear access:** Kykeon Analytics. Its country and its access for the public are unclear.
- **Self-test kits only:**
  - Drugstore (Ukraine)
  - Georgia's syringe vending machines
  - ReageSheep (Israel)
  - REAJA (Brazil)
  - Reduciendo Daño's kit shop (its event checking is listed)
- **Not specific enough:**
  - The Thai "drug checking" listing
  - TB HIV Care surveillance (South Africa)
  - Kitchener's machine (no sign after Aug 2024)
  - NIST RaDAR as a separate entry

## 10. What is still unsettled

1. **Canada:**
   - 8 entries remain `unclear` and 21 Canadian entries are `draft`.
   - Ten are active only on the strength of the 2025 CCSA symposium report: CIPTO, Dopamine, GRIP, SABSA, Sub Check, Mountainside, Tla'amin, BRAS Outaouais, Nomade and Travail de rue de Chicoutimi.
   - Blood Ties' `yes` rests on an undated own page and an Oct 2024 statement.
2. **United States:**
   - 18 states were not searched.
   - The Washington network has no independent source.
   - These entries rest on one or two thin sources: Southside (a job posting only), Transparency Testing (no independent source; eligibility and law vary) and DCLA (no sign after 2023).
   - The Red Project and the Chicago Recovery Alliance may have stopped.
3. **Thin evidence elsewhere:**
   - Instituto RIA's own description is a conference page, not a website.
   - The Argentina, Brazil and second Mexico entries are old.
4. **Greece:** Generation Act still has a single independent source. STEKI 46 needs a page from its operator.
5. **Conflicting details between sources:**
   - Spectrum: downtown on Mondays and Fridays (2023) vs the Pride Centre on Fridays (current profile).
   - L'Anonyme: hours differ between its own page and the CIUSSS listing.
   - Outside In: mass spectrometry (own page) vs FTIR (2025 slides).
   - NYC: five vs six syringe service programmes.
   - NYS: 14 listed sites vs "15 locations".
6. **Shallow searches:** many none-found countries rest on one combined query (see sections 5–7).
7. **WebFetch summaries** can be wrong in detail. Spot-check addresses and hours before publishing.
