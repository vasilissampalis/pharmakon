# Identity second reading — brief for AI reader 2

Written 2026-10-16. Identity sections (monograph section 2) are sourced facts (METHODS §10.3): names, CAS numbers,
formulas, molar masses, forms and street names, each with its source. They were compiled by a first AI reader through
WebFetch, which answers through a summarizing model (§12.1), so they stay `draft` until **confirmed by a second reader**.
This brief is that second reading. You never edit project files; the editor applies your results.

Working folder: `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/identity2nd/` (below: `W/`).

## Phase 1 — blind extraction

Until Phase 1 is complete for every page, do **not** open `data/identity/`, `data/verification/identity*`, the
scratchpad folders `identity3/` or `identity2nd/out/`, or any transcript of the first reader. Your extraction must not be
steered by what the first reader wrote.

- Input: `W/tasks.json` — one task per page (120): URL, publisher, the substance pages that cite it, and what it is
  cited for. Tasks with a `skip` reason (PubChem pages) are not fetched.
- For each other task, one WebFetch with an **open** prompt: name the substance(s) and what to look for, and ask for the
  items **exactly as printed** — numbers digit by digit, names in the page's spelling, lists complete and in page order,
  with the region or date the page gives for street names. Never put an expected value in the prompt.
- Save `W/extract/<n>.json`: `{"n", "url", "fetched_at", "prompt", "answer", "status"}` where `answer` is the WebFetch
  answer (only the part that concerns the task) and `status` is `read`, `truncated`, `refused` or `error`.
- A long page (a PDF, a long list) whose answer looks cut off may get **one** more fetch with a narrower prompt (for
  example only the street-name list, or only the identifiers); save it as `<n>b.json`.
- Pace: at least **60 seconds between two calls to the same domain** (another reader may be using the same sites);
  rotate domains. On a refusal, an error, a CAPTCHA or a 429: record it, do not retry, move on.

## Phase 2 — comparison

Only now open `data/identity/<substance>.json`, one substance at a time. For every item, compare with your extraction
from the source(s) the item cites (`source_ids` → `sources[].url` → your task number):

- `names`: each CAS number (all digits), the formula, the molar mass (all digits), the INN (and ATC code where given),
  the IUPAC or systematic name, each synonym. The same for each entry of `members`, if any.
- `forms`: each factual element of each detail (for example "white or off-white powder", "CAS 60-13-9", a product name).
- `street_names`: each name in each list, and the region and period as the page gives them.

Verdicts: `confirmed` (your extraction has it as written), `corrected` (your extraction differs: give the page's
version), `not-found` (your extraction lacks it; one targeted re-fetch naming the item is allowed — save it as
`<n>c.json` — and if it is still absent the verdict stays `not-found`), `not-rechecked` (the source was skipped or could
not be read). An item that cites two sources is confirmed if either has it; say which. Text in parentheses that only
reports how the first reader read the page ("read twice", "NIST", "as given by EUDA") is attribution, not an item.

Write `W/out/<substance>.json`:

```json
{"substance": "ketamine", "checker": "AI reader 2 (identity second reading)", "checked_on": "2026-10-16",
 "items": [{"path": "names.cas[0]", "item": "6740-88-1", "source_id": "nist-6740-88-1", "verdict": "confirmed",
            "evidence": "the page's wording, at most 15 words", "note": ""}],
 "summary": {"confirmed": 0, "corrected": 0, "not_found": 0, "not_rechecked": 0},
 "for_editor": ["…"]}
```

Paths use the file's structure (`names.synonyms[3]`, `forms[2].detail`, `street_names[1].names[4]`,
`members[0].cas[0]`). Keep `item` and `evidence` short.

## Rules (hard)

- WebFetch and WebSearch only. No browser, no downloads, no CAPTCHAs or bot checks, no PubChem, no sci-hub or similar.
- No quotation longer than 15 words. Nothing that reads as advice on obtaining, preparing, dosing or combining a drug.
- Do not edit anything under `data/`, `docs/`, `schema/`, `scripts/` or `site/`. Do not use local cron tools.
- Never send the user's email address or any personal data to a website.

Final report: per substance, the counts of each verdict and every item corrected or not found (path, item, the page's
version); pages that could not be read.
