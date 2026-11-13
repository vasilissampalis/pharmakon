# Second reading, web sources only (AI reader 62, 2026-10-18)

The browser was offline when AI readers 59 and 60 did their checks, so 49 web-only tasks remain. They cover MDMA with medicines (antidepressants and other psychiatric medicines), why MDMA's effect does not grow in step with the amount, CYP2D6, pregnancy and infants, cannabis with alcohol and driving, and GHB with alcohol. You wrote none of these anchors.

Follow the method, verdicts and rules in `data/verification/targeted-2026-10-18o/BRIEF_a.md` (sections "For each task" and "Rules"), with the changes below. Ignore its PDF table: all your sources are web pages.

**Tasks:** `data/verification/targeted-2026-10-18o/tasks_web.json` (n = 1 to 49).

**Output:** `data/verification/targeted-2026-10-18o/out_reader62.json`, with `"reader": "AI reader 62 (second reader)"` and `"date": "2026-10-18"`. Write it as you go (every 10 or so tasks).

## Sources (PubMed Central, one fetch each)

| reference | article | tasks |
|---|---|---|
| sarparast_2022 | https://pmc.ncbi.nlm.nih.gov/articles/PMC9177763/ | 16 |
| singer_2012 | https://pmc.ncbi.nlm.nih.gov/articles/PMC3367027/ | 10 |
| de-la-torre_2000 | https://pmc.ncbi.nlm.nih.gov/articles/PMC2014905/ | 6 |
| hartman_2015 | https://pmc.ncbi.nlm.nih.gov/articles/PMC4536116/ | 6 |
| schmid_2016 | https://pmc.ncbi.nlm.nih.gov/articles/PMC4949007/ | 5 |
| de-la-torre_2012 | https://pmc.ncbi.nlm.nih.gov/articles/PMC3495276/ | 2 |
| asbridge_2012 | https://pmc.ncbi.nlm.nih.gov/articles/PMC3277079/ | 2 |
| thai_2006 | https://pmc.ncbi.nlm.nih.gov/articles/PMC2766839/ | 2 |

- **Second-hand summaries.** An `extracted` that starts "Second-hand summary" reports what a review says about other studies. Check that the review says it, at the cited table or paragraph. Do not look up the primary studies.
- **Hedges' g:** for any editors' calculation of Hedges' g, use the small-sample correction, and centre the interval on g.
- **Negative numbers:** check every minus sign on the page itself.

## Browser

- Use the desktop app's built-in browser. Open your own tab with `tabs_create` (never `preview_start`), then `navigate` it. Pass that tabId on every call.
- Read each article once with `get_page_text`, which stops at 50,000 characters. Read the rest with `javascript_tool` on the same tab (for example `document.body.innerText.slice(50000, 100000)`). Save the text to `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/reader62/` and work from that copy with grep.
- For a table that comes out garbled, take one screenshot of that table.
- Do not download anything, and do not open PDF links.
- If a page is blocked or will not load, mark its tasks `not-found` and say why. Do not retry the same URL more than once.
- Close your tab at the end, and never touch, read or close any tab you did not open.

Do not open the first readers' files (`scratchpad/batch5/reader5*`), or `data/claims/`.

**Final message:** under 120 words. Give how many tasks were confirmed, corrected, wrong-location and not-found, and list the corrections that change a number.
