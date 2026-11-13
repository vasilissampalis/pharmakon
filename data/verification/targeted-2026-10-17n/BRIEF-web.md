# Second reading, web sources only (AI reader 53, 2026-10-18)

The browser was offline when AI readers 49 and 50 did their checks, so 13 web-only tasks remain. Follow the method, verdicts, output format and rules in `data/verification/targeted-2026-10-17n/BRIEF.md`, with these changes.

**Tasks:**
- In `data/verification/targeted-2026-10-17n/tasks.json`: n = 5, 9, 12, 16, 19, 24, 26, 31, 33, 39. These cite PMC3327851 (Urban et al., 2012) and PMC5021729 (Vegting et al., 2016). Write `data/verification/targeted-2026-10-17n/out_reader53.json`.
- In `data/verification/targeted-2026-10-17m/tasks.json`: n = 46, 47, 48. These cite PMC5626029 (Gomes et al., 2017), Figure 2. Write `data/verification/targeted-2026-10-17m/out_reader53.json`.

**Output:** in both files, `"reader": "AI reader 53 (second reader)"` and `"date": "2026-10-18"`.

**Browser:**
- Open your own tab with `tabs_create` (never `preview_start`), check with `tabs_context` that it is yours, and pass that tabId on every call.
- `get_page_text` stops at 50,000 characters; read the rest with `javascript_tool` on the same tab.
- For a figure, take one screenshot of it.
- Close your tab at the end, and never touch any other tab.

**Hedges' g:** for any editors' calculation of Hedges' g, use the small-sample correction, and centre the interval on g.

**Final message:** under 100 words.
