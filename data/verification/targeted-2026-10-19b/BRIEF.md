# Second reading: vapes, what reaches the body, and heart and lung disease (AI reader 88, 2026-10-23)

You are a second reader for Pharmakon, an evidence library about drugs (project: `/home/claude/drug-encyclopedia`). AI reader 71 wrote the 38 evidence anchors of the two claims `cl_nic_vapes_exposure` and `cl_nic_vapes_disease`. You wrote none of them. Check each one at the place it cites.

**Tasks:** `data/verification/targeted-2026-10-19b/tasks.json` (n = 1 to 38).

**Output:** `data/verification/targeted-2026-10-19b/out_reader88.json`, with `"reader": "AI reader 88 (second reader)"` and `"date": "2026-10-23"`. Write it as you go.

Follow the method, verdicts and rules in `data/verification/targeted-2026-10-18o/BRIEF_a.md` (sections "For each task" and "Rules"), with the changes below. Ignore its PDF table.

These are **section 7 drafts** (ways of taking a drug, compared): they go to the senior author before anything is published. Besides each number, check that the anchor says no more than the source and that every comparison names its comparison group as the source does. Flag in your note any wording that reads as advice on how to use a product.

## Sources (web only, one fetch each)

| reference | where to read it |
|---|---|
| goniewicz_2018 | https://pmc.ncbi.nlm.nih.gov/articles/PMC6324349/ |
| hartmann-boyce_2023 | https://pmc.ncbi.nlm.nih.gov/articles/PMC10092879/ |
| berlowitz_2022 | https://pmc.ncbi.nlm.nih.gov/articles/PMC9362726/ |
| xie_2020 | https://pmc.ncbi.nlm.nih.gov/articles/PMC7662143/ |
| banks_2023 | https://pmc.ncbi.nlm.nih.gov/articles/PMC10952413/ |
| nasem_2018 | NCBI Bookshelf: Summary, https://www.ncbi.nlm.nih.gov/books/n/nap24952/Sum1/; Summary Annex, https://www.ncbi.nlm.nih.gov/books/n/nap24952/Sum1_Annex/; chapter 2, https://www.ncbi.nlm.nih.gov/books/n/nap24952/ch2/; chapter 9, https://www.ncbi.nlm.nih.gov/books/n/nap24952/ch9/; chapter 11, https://www.ncbi.nlm.nih.gov/books/n/nap24952/ch11/ (the task's `source_read` says which) |
| mcneill_2022 | GOV.UK: summary, https://www.gov.uk/government/publications/nicotine-vaping-in-england-2022-evidence-update/nicotine-vaping-in-england-2022-evidence-update-summary; main findings, https://www.gov.uk/government/publications/nicotine-vaping-in-england-2022-evidence-update/nicotine-vaping-in-england-2022-evidence-update-main-findings |

Save each page's text to your folder as soon as you have read it: the browser can disconnect mid-task.

- Use the desktop app's built-in browser. Open your own tab with `tabs_create` (never `preview_start`), then `navigate` it; pass that tabId on every call. The browser holds at most 9 tabs: if `tabs_create` answers "tab cap reached", wait a few minutes and retry; never close or use a tab you did not open.
- Read each page once with `get_page_text` (it stops at 50,000 characters; read the rest with `javascript_tool` on the same tab) and save the text to `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/reader88/`. Work from that copy.
- For a table or figure that the text does not give, take one screenshot of it.
- Close your tab at the end. No downloads, no PDF links (including links to a report's PDF), no CAPTCHAs.

Do not open the first reader's files (`scratchpad/routes/reader71*`), the study cards in `data/study-cards/_incoming/`, or `data/claims/`.

**Final message:** under 150 words: how many tasks were confirmed, corrected, wrong-location and not-found, and the corrections that change a number.
