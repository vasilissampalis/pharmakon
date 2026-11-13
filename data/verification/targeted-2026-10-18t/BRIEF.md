# Second reading: nicotine products and stopping smoking, the Cochrane reviews (AI reader 78, 2026-10-18)

You are a second reader for Pharmakon, an evidence library about drugs (project: `/home/claude/drug-encyclopedia`). AI reader 70 wrote the 49 evidence anchors of the seven claims `cl_nic_nrt`, `cl_nic_nrt_forms`, `cl_nic_nrt_harms`, `cl_nic_vapes_stopping`, `cl_nic_vapes_stopping_support`, `cl_nic_vapes_harms` and `cl_nic_pouches_stopping`. You wrote none of them. Check each one at the place it cites.

**Tasks:** `data/verification/targeted-2026-10-18t/tasks.json` (n = 1 to 49).

**Output:** `data/verification/targeted-2026-10-18t/out_reader78.json`, with `"reader": "AI reader 78 (second reader)"` and `"date": "2026-10-18"`. Write it as you go.

Follow the method, verdicts and rules in `data/verification/targeted-2026-10-18o/BRIEF_a.md` (sections "For each task" and "Rules"), with the changes below. Ignore its PDF table.

These are **section 7 drafts** (ways of taking a drug, compared): they go to the senior author before anything is published. Besides each number, check that the anchor says no more than the source and that every comparison names its comparison group as the source does. Flag in your note any wording that reads as advice on how to use a product.

## Sources (web only, one fetch each)

| reference | where to read it |
|---|---|
| hartmann-boyce_2018 | https://pmc.ncbi.nlm.nih.gov/articles/PMC6353172/ |
| theodoulou_2023 | https://pmc.ncbi.nlm.nih.gov/articles/PMC10278922/ |
| lindson_2026 | https://pmc.ncbi.nlm.nih.gov/articles/PMC13506250/ |
| hartmann-boyce_2025 | https://pmc.ncbi.nlm.nih.gov/articles/PMC12549188/ |

Cochrane reviews are long: read the Summary of findings tables, Results and the analyses the task cites; every absolute number ("N more in 100") must be checked against the summary-of-findings table, and every certainty rating against Cochrane's own GRADE row.

- Use the desktop app's built-in browser. Open your own tab with `tabs_create` (never `preview_start`), then `navigate` it; pass that tabId on every call. The browser holds at most 9 tabs: if `tabs_create` answers "tab cap reached", wait a few minutes and retry; never close or use a tab you did not open.
- Read each page once with `get_page_text` (it stops at 50,000 characters; read the rest with `javascript_tool` on the same tab) and save the text to `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/reader78/`. Work from that copy.
- For a table or figure that the text does not give, take one screenshot of it.
- Close your tab at the end. No downloads, no PDF links (including links to a report's PDF), no CAPTCHAs.

Do not open the first reader's files (`scratchpad/routes/reader70*`), the study cards in `data/study-cards/_incoming/`, or `data/claims/`.

**Final message:** under 150 words: how many tasks were confirmed, corrected, wrong-location and not-found, and the corrections that change a number.
