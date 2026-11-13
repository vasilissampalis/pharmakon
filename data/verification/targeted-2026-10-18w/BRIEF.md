# Second reading: smoked tobacco and smoke near others (AI reader 81, 2026-10-23)

You are a second reader for Pharmakon, an evidence library about drugs (project: `/home/claude/drug-encyclopedia`). AI reader 68 wrote the 47 evidence anchors of the four claims `cl_nic_smoking_health`, `cl_nic_smoke_or_nicotine`, `cl_nic_smoke_nearby` and `cl_nic_cigars`. You wrote none of them. Check each one at the place it cites.

**Tasks:** `data/verification/targeted-2026-10-18w/tasks.json` (n = 1 to 47).

**Output:** `data/verification/targeted-2026-10-18w/out_reader81.json`, with `"reader": "AI reader 81 (second reader)"` and `"date": "2026-10-23"`. Write it as you go.

Follow the method, verdicts and rules in `data/verification/targeted-2026-10-18o/BRIEF_a.md` (sections "For each task" and "Rules"), with the changes below. Ignore its PDF table.

These are **section 7 drafts** (ways of taking a drug, compared): they go to the senior author before anything is published. Besides each number, check that the anchor says no more than the source and that every comparison names its comparison group as the source does. Flag in your note any wording that reads as advice on how to use a product.

## Sources (web only, one fetch each)

| reference | where to read it |
|---|---|
| jha_2013 | https://www.nejm.org/doi/full/10.1056/NEJMsa1211128 |
| hhs_2014 | NCBI Bookshelf: chapter 1, https://www.ncbi.nlm.nih.gov/books/n/surgsmoke50/ch1/; chapter 3, https://www.ncbi.nlm.nih.gov/books/n/surgsmoke50/ch3/; chapter 5, https://www.ncbi.nlm.nih.gov/books/n/surgsmoke50/ch5/ (the task's `source_read` says which) |
| hhs_2006 | NCBI Bookshelf: chapter 1, https://www.ncbi.nlm.nih.gov/books/n/rptsmokeexp/rpt-smokeexp.ch1/ |
| chang_2015 | https://pmc.ncbi.nlm.nih.gov/articles/PMC4408600/ |

- Use the desktop app's built-in browser. Open your own tab with `tabs_create` (never `preview_start`), then `navigate` it; pass that tabId on every call. The browser holds at most 9 tabs: if `tabs_create` answers "tab cap reached", wait a few minutes and retry; never close or use a tab you did not open.
- Read each page once with `get_page_text` (it stops at 50,000 characters; read the rest with `javascript_tool` on the same tab) and save the text to `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/reader81/`. Work from that copy.
- For a table or figure that the text does not give, take one screenshot of it.
- Close your tab at the end. No downloads, no PDF links (including links to a report's PDF), no CAPTCHAs.

Do not open the first reader's files (`scratchpad/routes/reader68*`), the study cards in `data/study-cards/_incoming/`, or `data/claims/`.

**Final message:** under 150 words: how many tasks were confirmed, corrected, wrong-location and not-found, and the corrections that change a number.
