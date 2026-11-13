# Two new cross-cutting topics: evidence maps and PDF lists (31 October 2026)

The senior author asked for two new parts of the site. You build the evidence map and PDF list for one of them, exactly
as `search-logs/DayAfter_DOI-LIST.md` and `search-logs/DayAfter_search-log.md` were built (read both first: they are
the model for method, columns, tiers and the verification block). Also read `docs/METHODS.md` §2–§3 and §9 (language).

## Topic 1: Before, during and after (output `search-logs/BeforeDuring_DOI-LIST.md` and `..._search-log.md`)

For each drug in `data/site/substances.json`, the research on what people do **before and during** use to reduce harms
or to make the experience go better, and whether it works. "The day after" already has its list
(`DayAfter_DOI-LIST.md`): do not repeat its papers; add only after-effect remedies it missed.

- Preparation and state: sleep, food, hydration, mood and expectations ("set"), the place and the people ("setting"),
  having a sober or experienced person present, preparation in psychedelic research.
- During use: water and cooling (heat illness), rest and breaks, what studies found about taking more during a session
  (redosing) as a risk, eating, music and guidance in psychedelic sessions.
- Supplements and medicines people take before or with a drug to prevent harm or an after-effect (for example
  "preloading" or "postloading" with 5-HTP, antioxidants or magnesium around MDMA; hangover-prevention products taken
  before or while drinking; CBD taken with THC), and their risks and interactions.
- What predicts a good or a difficult experience (for example challenging experiences with psychedelics).

Out of scope: dose amounts, timing advice, routes compared (section 7, the senior author's own), mixing drugs (the
interactions page has it), drug checking (it has its page), and anything about making a drug's effects stronger.

## Topic 2: How drug deaths are counted (output `search-logs/DrugDeaths_DOI-LIST.md` and `..._search-log.md`)

The research on how drug deaths are defined, investigated, certified, coded and counted, and how far the counts can be
trusted, in both directions (deaths wrongly blamed on a drug, and drug deaths missed):

- Definitions and coding: ICD-10 codes, "poisoning" against "misuse" definitions, national and European definitions
  (ONS, CDC, EUDA), counting every drug "mentioned" when several are found.
- Accuracy of death certificates for drug deaths; deaths certified with no named drug; variation between places.
- Who investigates deaths: coroner and medical examiner systems, their training and resources, autopsy and toxicology
  rates, and studies of the effect on the counts.
- What a blood level after death can and cannot show: post-mortem redistribution, tolerance, overlap between levels
  found in deaths and in living people, sampling site.
- Deaths attributed to particular drugs and re-examined (for example MDMA, cannabis, ketamine, synthetic cathinones,
  fentanyl, "excited delirium"), and estimates of undercounting.
- How the media report drug deaths, where studied.

## Method and rules

PubMed through E-utilities and Crossref `works/<DOI>` in one tab of your own in the app's browser (load the tools once
with ToolSearch, query `mcp__remote-devices__Claude_Browser__`, max_results 20; `tabs_create`, its tabId on every call,
closed at the end; never `preview_start`; never touch another tab; no search engines, no PDFs or downloads; stop at any
check page). Every DOI must come from a Crossref record fetched in your tab and match the PubMed record on title, year
and first author; read `updated-by` (corrections, retractions). Prefer systematic reviews and meta-analyses, then
large studies and authoritative reports; include each landmark paper's published critiques. Target: topic 1, 60 to 90
papers; topic 2, 40 to 60. Tier A = read first (25 to 35), B = the rest. Free full texts: give the PMC id. Reports
without a DOI go in their own table. Write files as you go. No claims, cards or site text: lists and logs only.

Final message under 200 words: counts per tier, DOIs verified and dropped, corrections or retractions found, gaps.
