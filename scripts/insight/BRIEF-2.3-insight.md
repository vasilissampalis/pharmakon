# Insight 2.3: understand the question, answer exactly, or say we can't yet (builder brief, 15 November 2026)

Pharmakon (`/home/claude/pharmakon`; read `CLAUDE.md` first, then `scripts/insight/MODELS.md` and
`site/src/app.insight.js`) has a search box that understands questions in people's own words on their own device
("Insight", site 2.2.0). It never writes text: it only finds answers the editors have checked. The senior author used
it and it disappointed him. You make it behave like an assistant that understands what was asked. A second builder is
rebuilding the pages (drug page with one section at a time, "If it gets too much", test kits) in another worktree at the
same time: see "Borders".

Work in your own worktree and branch: `git -C /home/claude/pharmakon worktree add /home/claude/ins23 -b ins23 origin/main`.
Commit and push your branch after every step (`git push -q origin ins23`); never push to `main`; never run
`scripts/snapshot_published.py`; deliver nothing to the senior author.

## What the senior author said (his words; they are the brief)

- "pharmakon insight should be as smart as possible ... currently it's a bit stupid for example i asked 'how can you die
  from alcohol' and the result was 'How many deaths does alcohol cause worldwide?' ... which is close but not the same to
  what i ask ... it has a high error rate". (The site has no checked answer on how alcohol kills. The right behaviour was
  to say so and offer the nearest things as nearest things.)
- "'give me the full evidence about how can i die from ketamine' the response should be 100% accurate right now this is
  the answer that pops up 'How many UK deaths were linked to ketamine, and what were they? First, a guess: myth or fact?
  ... Skip to the answer' and it's terrible".
- "it's your assistant in the website so it should be everywhere for example in the drug pages it should be there too
  and you should be able to use it to find everything you want. it should have the feel that information is coming
  through you from the inside and not to you from the outside ... like a fairy that can help you everywhere. the website
  should come to life through pharmakon insight so it should have a more primary role".
- About the quiz: "i clicked 'Read the answer' in Myth or fact ... i jumped on another page with different questions! if i
  wanted to stay on myth and facts then i have to go to the previous page. our site is not ergonomic!! ... you are like
  'where the fuck did i pop up where was i at where are the questions why am i on the cannabis page'".
- "'Someone unwell? What to do · Emergency numbers' should be cut because we are stigmatizing drugs".
- On a cannabis answer, "Read next" offered "Do most US dollar bills carry traces of cocaine?".
- "the website should be completely readable and digestible by casual users".

## What to build

### 1. An answer opens at once
Remove the "First, a guess: myth or fact?" step from the answer sheet everywhere. Someone who asked a question gets the
answer. (Myth or fact stays in its own decks.)

### 2. One ranking function with honest tiers
All matching goes through one function, e.g. `insRank(query, ctx)` → `{routes: [...], best: [...], related: [...]}`:
- `best`: answers we are confident answer the question as asked (0 to 2). `related`: near answers (up to 3).
- For now the tiers come from the present score with two thresholds read from `data/insight.json`
  (`tiers: {best: 0.72, related: 0.58}`, written by `scripts/insight/build_index.py`, so the editor can tune them and
  later replace the score by a trained judge without touching the page code). Keep the scoring in one small function
  with one clear input (the query's numbers, the candidate's rows) so a second scoring step can be added there.
- When the question names a drug (aliases), an answer that is on none of the named drugs' pages can never be `best`; it
  may be `related`, labelled with its own drug.
- `ctx.drug`: on a drug's page, a question that names no drug is understood as about this drug (boost that drug's
  answers; the box's placeholder there reads "Ask about cannabis", set from the route in JavaScript, no template edit).

### 3. What the person sees while typing
- A route row first when the question is really a request for something else (see 5).
- "Best match": the checked question, and the short answer in full underneath (not cut to one line), with its rating.
- "Related": up to three, as today's rows.
- When there is no best match: one calm line, "We haven't checked exactly this yet.", with "Ask us to check it" (today's
  Ask us, carrying the words typed), then Related if any. Never present a related answer as the answer.
- Keep the quiet line "Runs on your phone/computer. Nothing you type leaves it." and the word search below, as now.

### 4. Enter opens the answer to *their* question
Pressing Enter (or the search key on a phone) opens the answer sheet for the question as asked:
- Heading: the person's own question, as they typed it (trimmed, first letter capital). Their words, not ours.
- Then each `best` answer in full, one under the other (short answer, But, its number picture when it has one, "How do
  we know?" closed), each with a quiet label naming the checked question it answers, its rating, "The evidence" and
  "See it on the … page".
- No best match: "We haven't checked exactly this yet." + "Ask us to check it" + the related questions as links.
- Then "People also ask": up to three next questions (see 6).
- Depth words are understood and removed before matching: "full evidence", "all the evidence", "the studies",
  "sources", "in detail", "scientific", "explain" open each answer with "How do we know?" open and "The evidence" given
  as a button; "short", "simple", "simply", "tl;dr", "eli5", "in a sentence" show only the short answer and But.
Tapping one row in the list opens the sheet with that one answer, as now.

### 5. Routes: understand what kind of request it is (small ordered table, each with a test)
- **Two drugs** named (aliases) → first row "MDMA + alcohol: what's known about mixing them", opening the mixing tool
  with both chosen (find its route in `app.views.js`); the checked mixing answers still appear under it.
- **A dose question** ("how much … take", "dose", "dosage", "how many mg/pills/tabs/lines/hits", "safe amount") → a row
  "We don't list doses. These harm reduction groups do", opening that drug's Doses block. Never any amount from us;
  answers that match still show.
- **An emergency in progress** ("not breathing", "won't wake up", "passed out", "having a seizure/fit", "overdosing",
  "what do i do", "too high", "greening out", "bad trip help", "freaking out") → first row "If it gets too much: what
  helps", opening that drug's (or the page's) "If it gets too much" section; this row, and only emergency answers, show
  the local emergency number line.
- **"what is X" / a drug's name alone** → the drug's page (the word search already lists it; make it the first row).
- **Testing a sample** ("test kit", "is my … real/pure/cut/laced", "how do i test") → the drug's "Test kits" section.
- Anything about getting drugs, hiding use or beating a drug test: no route, no answer; the ordinary "We haven't checked
  exactly this yet" without the Ask us button.
Section anchors are changing in the pages build: link by the hash routes that exist today (`#d-help`, the Doses and test
blocks' ids) through one small helper so the editor can adjust them at merge.

### 6. Next questions that follow from this one
At build (`build_index.py`), for every answer keep its three nearest answers by meaning (same drug first, never
itself). Use them for the sheet's "People also ask" and for the drug page's "Read next" block (replace how that block
picks its questions; a cannabis answer must not offer a cocaine question). Skip answers already opened in this visit.

### 7. The sheet is how an answer opens when you are not on its page
- Myth or fact → "Read the answer" opens the answer sheet over the deck; Back (button, Esc, browser Back) returns to the
  same card of the same deck, scrolled as it was.
- The same for answer links on the start page, in "Read next", and anywhere else an answer is linked from outside its
  own drug page. On a drug's own page, questions open in place as they do now.
- "See it on the … page" stays in the sheet for those who want the page.

### 8. No emergency line by default
Remove "Someone unwell? …" from the sheet, except as 5 says.

## Checks (`scripts/ux/insight_check.js`; all must pass, plus `parity.js`, `redesign_check.js`, `smoke.js`,
`speed_check.js`, `python3 -I scripts/validate.py`)
Replace the guess-first checks. Add: "how can you die from alcohol" shows "We haven't checked exactly this yet" and
no best match, with "How many deaths does alcohol cause worldwide?" under Related at most; "give me the full evidence
about how can i die from ketamine" + Enter opens a sheet headed with those words (depth words understood), with no
guess step and "How do we know?" open; "does ecstasy damage your brain permanently" has its answer as best match with
the short answer readable in the list; "can i mix molly and alcohol" shows the mixing row first; "how much mdma should
i take" shows the Doses row and no amount; on the cannabis page "does it kill brain cells" does not show the alcohol
answer as best match; Myth or fact → Read the answer → Back returns to the same card; next questions of a cannabis
answer are about cannabis; nothing typed leaves the page; no "AI" words; no console errors; start page fetches none of
Insight's files; speed printed (median and slowest).

## Borders with the pages builder (branch `pages23`)
You own `site/src/app.insight.js`, `scripts/insight/*`, `scripts/ux/insight_check.js`, the Insight step of
`site/build.js`, the quiz's "Read the answer" link and the "Read next" block (touch only those lines in
`app.simple.js` / `app.views.js`; the pages builder is rewriting much of those files, so keep your edits there minimal
and clearly marked `// 2.3 insight`). `site/src/styles.css` is shared: keep your new rules in one block marked
`/* 2.3 insight */` at the end; do not reformat the file. Do not edit `index.template.html`.

## Rules
Plain words; no "AI" words anywhere on the site; no analytics, cookies or outside requests; nothing typed is stored or
sent; keyboard and screen reader work (announce results and tiers); reduced motion respected; no sideways scroll at 390;
no console errors. If an automatic filter stops a step, do not retry or reword it: note it and go on.

## Report (under 350 words)
What changed, check results (numbers), speed, anything you decided that the editor should confirm, and screenshots
(`--shots`, 390 and 1280: the list for a matched question, the list for an unmatched one, the sheet after Enter with
depth words, the mixing row, the doses row, the quiz with the sheet open).
