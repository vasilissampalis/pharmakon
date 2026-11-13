# Evidence-map brief (for co-editors building a substance's DOI list)

Read `docs/METHODS.md` §2–§3 first, then `search-logs/methamphetamine_DOI-LIST.md` and `search-logs/methamphetamine_search-log.md`, which are the model outputs. Produce the same two files for each substance assigned to you.

## Goal
A numbered, tiered list of the papers a monograph needs, every DOI verified, so the senior author can save the PDFs one by one.

## Sources you can use
Follow `docs/WORKFLOW.md`, "What the AI can and cannot reach", for endpoints, URL limits and pacing (it supersedes the
first version of this brief):
- **Crossref through WebFetch.** Search with `query.bibliographic` (and `query.container-title` where useful) and
  `select=DOI,title,container-title,issued,author,updated-by`; never `&sort=relevance` (requests fail); keep URLs under
  about 250 characters and never put a literal comma in a query term. One Crossref agent at a time; 90–130 s between
  calls and 150–300 s after a refusal (HTTP 429); never re-fetch a refused URL at once.
- **OpenAlex through WebFetch** is reachable (`filter=doi:` with at most three DOIs joined by `%7C`; pace with
  `scratchpad/openalex_pace.sh`).
- WebSearch, for locating landmark papers' titles when needed.

## Method per substance (follow in order)
1. Write 12–16 section-level Crossref queries covering the monograph sections (METHODS §8): pharmacology/pharmacokinetics; neuroscience/neuroimaging; acute effects (human laboratory studies); acute toxicity/overdose; interactions; dependence/withdrawal; long-term physical, psychiatric and cognitive outcomes; epidemiology/mortality; harm-reduction interventions; therapeutic trials; pregnancy; route of administration harms; policy/legal where a peer-reviewed source exists. Add substance-specific topics (e.g., serotonergic neurotoxicity for MDMA; psychosis for cannabis; cardiomyopathy for cocaine; bladder for ketamine; B12/myeloneuropathy for nitrous oxide).
2. Run them. Screen hits by title and journal: keep systematic reviews, meta-analyses, landmark primary studies, major cohorts, RCTs, authoritative reviews in serious journals. Drop conference abstracts, supplements, letters, off-topic hits, predatory-looking venues.
3. Add the landmark studies you know for this substance AND their published critiques, replies, replications and follow-ups (the protocol requires that a landmark is never cited without its critiques). Recall their titles, then find the DOI through a Crossref search on title+author. Never write a DOI from memory into the list.
4. Every DOI in the list must come from a Crossref record: a `works/<DOI>` fetch, or verbatim from a search fetched with `select=…,updated-by` (which carries the retraction and correction links); a DOI taken from a search without `updated-by` needs a `works/<DOI>` check for retractions and corrections. Never write a DOI from memory. Echo the Crossref title into the table (shortened is fine). Drop any DOI that does not resolve or resolves to a different paper. Mark any with `updated-by` of type retraction (exclude it, note it), erratum/correction (keep, mark "erratum published").
5. Tier the list: **A** (needed first: the backbone systematic reviews and the landmark primaries with their critiques; 25–35 papers), **B** (section backbone; 40–60), **C** (epidemiology, routes, harm reduction, pregnancy, policy; 20–40). Target 90–130 papers for a Tier-1 substance. Fewer is acceptable for substances with thin literatures (e.g., salvia, 5-MeO-DMT, 2C-x): say so.
6. Add a "Reports (no DOI)" table for UNODC/EUDA/WHO/national reports relevant to the substance, and a "Known gaps" paragraph.
7. Write the search log: every query string you ran, hits retained, DOIs corrected, errata/retractions found; then 10–14 PubMed strings the senior author will run (same style as the methamphetamine log).

## Output files (exact names)
- `search-logs/<Folder>_DOI-LIST.md` — `<Folder>` is the PDFs folder name from `docs/TIER1.md` (e.g., `MDMA`, `GHB-GBL`, `Synthetic-cathinones`). Same structure as the methamphetamine list: header with date and method; Tier A/B/C tables with columns `# | Paper | Journal, year | DOI | Save as`; reports table; known gaps; and a final **Verification block**: number of DOIs fetched, resolved, dropped (list the dropped ones), errata, retractions.
- `search-logs/<Folder>_search-log.md`.

Filename convention for "Save as": `FirstAuthor_Year_ShortTitle.pdf`; cross-cutting papers go to `_Cross-cutting/...`; reports to `_Epidemiology/...`.

## Rules
- Nothing enters the list unverified. If you cannot verify a DOI, leave the paper out and mention it under "Known gaps" with its title.
- Use the language rules of METHODS §9 in your own text (people who use drugs; no "abuse" outside quoted titles).
- Do not write monograph content, claims or study cards. Lists and logs only.
- Report back with: substances done, counts per tier, number of DOIs verified/dropped, anything unusual (retractions, thin literature, rate-limit problems).

## Working economically (added 2026-10-15, after a first run exhausted its budget)

A first run of this brief spent its whole session budget on seven substances. Work to this budget instead:

1. **Write files as you go.** The moment one substance's two files are written, move to the next. Never hold several substances' results in memory. If you stop early, everything finished is already saved.
2. **About 10–12 Crossref searches per substance**, not 16. Combine outcome domains into one query where the literature allows (e.g. "cardiovascular stroke cardiomyopathy" as one).
3. **Verify in batches, not one at a time.** After drafting a substance's table, verify its DOIs in a single pass at the pace above, and record fetched/resolved/dropped. A DOI copied verbatim from a Crossref search fetched with `updated-by` in this session needs no further fetch; a DOI recalled from memory, or from a search without `updated-by`, needs a `works/<DOI>` check.
4. **Target 70–110 papers per Tier-1 substance** (Tier A 25–35, B 30–50, C 15–30). Thin literatures (salvia, 5-MeO-DMT, mescaline, 2C-x, PCP) are smaller and should say so in "Known gaps".
5. **Keep your own reporting short.** No long thinking out loud between tool calls; the files are the deliverable.
