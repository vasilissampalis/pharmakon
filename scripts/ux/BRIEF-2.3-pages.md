# Site 2.3: pages people can use (builder brief, 15 November 2026)

Pharmakon (`/home/claude/pharmakon`; read `CLAUDE.md` first) is a drug encyclopedia for people who use drugs and people
curious about them. The senior author and his brother used version 2.2.0 and found it tiring: too much on screen, links
that throw you somewhere else, lines nobody needs. You rebuild the pages so that **less shows, one thing at a time, in
people's order of interest**. A second builder is changing Insight (search, the answer sheet, the quiz's "Read the
answer", "Read next") in another worktree at the same time: see "Borders" below.

Work in your own worktree and branch: `git -C /home/claude/pharmakon worktree add /home/claude/pages23 -b pages23 origin/main`.
Commit and push your branch after every step (`git push -q origin pages23`); never push to `main`; never run
`scripts/snapshot_published.py`; deliver nothing to the senior author. Build with `node site/build.js && python3 -I
site/build_public.py`; the checks are `scripts/ux/redesign_check.js`, `smoke.js`, `speed_check.js`,
`insight_check.js`, `scripts/insight/parity.js` (update the first three to the new design; they must all pass at the end).

## What the senior author said (his words; they are the brief)

- "the cut you see in the picture when you click on a link and can't see the question / the upper sentence happens in
  general for whichever link you click ... i want to see where the section or question starts this is a generalized bug
  whenever you click on a link on the website!"
- "'Approved by our editor; sources checked by a second AI reader · version 0.2.2 · 3 findings from 1 source' this should
  be removed when i click on 'The evidence', in general if an info will not benefit a viewer it should be removed
  otherwise it creates visual clutter. we have already written the 'How we check facts' section ... don't intertwine
  sections"; "don't write these '4 related studies listed for reading)' and 'Approved by our editor; sources checked by a
  second AI reader · v0.5.0' in the answers they are not useful they create visual clutter".
- "in 'How to read this site' the example should be removed you could give only what's very basic about how to use the
  website (the users are not stupid) and probably it would be more useful how to read as a scientist for example this
  ''Linked to' is not 'causes'' ... is nice".
- "at the top of the drug page this 'Someone unwell? What to do · Emergency numbers' should be cut because we are
  stigmatizing drugs if in the top we are writing that somebody is unwell. we want to give objective knowledge".
- On "If it gets too much": "the sources should be apparent for each respective fact without creating visual clutter and
  also we should not just write about what to do if it is too much for another person but what to do yourself if it's too
  much for you. going or calling the hospital should be the last on the list like a last resort ... we have to begin with
  what users find most useful"; "'First aid while you wait for help' i think this is extreme as a different section ...
  we don't want to freak people out"; "the emergency numbers are almost completely useless and either we remove it from
  the website or we make it a hidden section".
- "i think each drug page should have a description for each drug that makes you understand what it is and its sources
  are validated".
- "either nothing shows or only the description of the drug shows ... you should be able to choose from the menu the
  section you want to read ... my brother who used the website told me that ... when he clicked on a section in the menu
  he would like then the section to pop up and when he clicks on another section the previous to close and the new to
  pop up so as not to get lost in all that info because then he won't want to read it. and i don't know if we should add
  subsections ... or if then we would make the website too complicated".
- On test kits: "each respective fact about the test kits should be cited"; "the test kits are low priority and should be
  very discreetly kept inside the website so probably it should not also be apparent in the menu on the top of the
  website like emergency numbers. and the test kits should be individualized for each drug ... if a user wants to buy
  something they should be able to buy it immediately and it should be at the top" (of the test-kit block).
- "it is strange that in each drug page we have the Quick and Full version this is confusing and the full version is
  UNREADABLE each drug page should be one perfectly organized".
- "the website should be completely readable and digestible by casual users".
- About Myth or fact: "less than half of them are interesting for most users. they feel a lot like an academic test".

## What to build

### 1. Every jump lands on the start of what it points to (site-wide)
Wherever the site scrolls to something (a hash route, a link to a section or question, a tab or question opening), the
heading or question it points to must be fully visible just under whatever is stuck to the top (header, section menu),
at 390 and 1280 wide, also after late layout (photos, data arriving, fonts). Fix it once, in one place, not per link:
measure the stuck bars, keep the offset in one CSS variable, give every target `scroll-margin-top`, and re-apply the
scroll when layout settles. Add a check to `redesign_check.js` that follows at least six kinds of link (a question link
from the start page, a "Read the answer"-style link to `#s-<drug>/q-<claim>`, a section link such as `#d-help`, a
section-menu tap, opening a question, a link from the menu) and fails if the target's top edge is hidden or not near the
top.

### 2. The drug page: a description, a menu, one section at a time
- **Top:** the name, its other names (as now, quiet), and the description: `data/site/descriptions.json` when it has
  the drug (shape below; a content round is writing it now), otherwise today's family line. Remove the "Someone unwell?"
  line. Remove the Quick/Full switch: the page is one page. Whatever "Full" shows that is not reachable from an answer's
  "The evidence" must be listed in your report (do not delete data); the long precise text stays reachable per answer
  through "The evidence". Leave the senior author's doses text and the Doses block as they are.
- **The section menu** is the page. At first nothing else shows: the sections are a list of large rows (name in people's
  words, how many answers, one quiet line of what is inside). Choosing one opens that section alone; the list becomes the
  row of chips stuck under the header; choosing another closes the first and opens the new one, scrolled to its start;
  choosing the open one again closes it and brings the list back. A deep link (`#s-<drug>/q-<claim>`, `#d-help`, …)
  opens the right section with the question open and in view. Back and Forward work; the open section is in the URL.
- **Order:** by what people ask most, the same order on every drug page so it can be learned: work it out once from
  `data/site/demand.json` (sum of the demand scores of the answers in each kind of section across all drugs), then put
  the utility sections last in this order: If it gets too much, Test kits, Doses. Say the order in your report.
- **Inside a section:** topic headings stay as plain headings (no extra level to tap). Question cards stay as they are
  (question, short answer line, rating); one question open at a time, opened in place and scrolled to its start. Do not
  change the "Read next" block (the other builder owns it).
- **No subsections to click.** Two levels only: section, then question.

### 3. "If it gets too much" (data: `data/site/stay-safer.json` → `signs` by family)
New order, top to bottom:
1. **For you**: lines from `signs.<family>.self` when present (a content round is writing them; same line/anchors shape
   as the other lists). Show nothing for "you" until the data exists; never write a line yourself.
2. **For a friend → What helps:** the `while_waiting` lines of kind `calm` and `help`, then those of kind `aid` (first
   aid folded in here; no separate "First aid while you wait" disclosure). For Opioids the list is the aid lines in data
   order (naloxone first).
3. **What not to do:** the `do_not` lines.
4. **Last, as a last resort:** "Call an ambulance if" + the `call_now` signs + one line with the local emergency number
   when the reader's country is known, and a quiet link to the numbers by country. Not a red box, not at the top, not
   repeated elsewhere on the page.
- **Sources per line, without clutter:** after each line one or more small chips with the publisher's short name
  (the acronym in brackets when the publisher has one, e.g. HSE, ADF, CDC, WHO, FRANK; otherwise a short form), in the
  style of the reference chips on answers ("Anthony 1994"); a tap or hover shows publisher, page title and the link.
  Remove the "Sources (n)" list at the end and the line "From official and non-profit health pages … Our editor has not
  checked them yet" (how these lines are checked belongs to "How we check facts"; if it is not said there, add one
  sentence there).

### 4. Test kits (data: `stay-safer.json` → `tests`, `kits-for.json`, `tests-world.json`, and soon `kit-links.json`)
- Its own section named "Test kits", near the end of the section order (see 2), not the first thing on the page.
- **Buying comes first inside it:** "Test kits for <drug>" with one row per seller that ships to the reader's country
  (today's logic), each linking straight to that seller's page for this drug when `data/site/kit-links.json` has it
  (shape below; being written now), otherwise to the seller's shop as today. Then the facts about the tests, then what
  tests cannot tell, then drug-checking services.
- Every fact line gets its source chips as in 3; remove the "Sources (26)" list.
- Out of the top menu: remove the menu's doors to drug checking and to emergency numbers (keep "Is it safe to mix?").
  Both pages stay, linked from the footer and from these sections only.

### 5. The evidence view and the answers: only what helps a reader
Remove from every answer and from "The evidence": the line "Approved by our editor; sources checked by a second AI
reader · version … · n findings from m sources", the line "Searched for newer research on …" with its "(titles and
abstracts screened; n related studies listed for reading)", and the closing "Approved by our editor … · v…". Keep one
quiet line only inside the deepest fold ("Precise statement, study details and sources"): "Version 0.5.0 · last search
for newer research 16 Oct 2026" (people who cite an answer need the version; nobody else has to see it). Look for other
lines of the same kind (status notes, counts, process remarks) on answers, cards and sections, remove those that tell a
reader nothing they can use, and list each in your report.

### 6. "How to read this site" and "How we check facts"
- "How to read this site": remove "A real example" entirely. Keep three or four plain lines on using the site (tap a
  question for its answer; "The evidence" shows the studies; what the bars mean), then the short items on reading like a
  scientist that the page already has ("'Linked to' is not 'causes'" and its siblings). Nothing else.
- "How we check facts": leave "Seven questions to ask about any drug story" as it is for now (its sources are being
  collected; it will be cited in a later version). Do not add citations yourself.

### 7. Myth or fact: only the interesting cards, best first
`data/site/tf-interest.json` (being written now) will hold `{"cut": {"interest": 3.5, "clear": 4.0}, "items":
{"<key>": {"interest": 4.5, "clear": 5.0}}}`, where `<key>` is the first 12 hex characters of the SHA-1 of the card's
statement (UTF-8). In `site/build.js`: when the file exists, leave out of every deck the cards whose scores fall under
the cut, and order each deck by interest, highest first (ties: as now); cards with no entry are shown as now. Print how
many cards were left out. Until the file exists nothing changes.

## Data shapes arriving from the content rounds (render when present, fall back when absent)
- `data/site/descriptions.json`: `{"_note": "...", "drugs": {"<slug>": {"lines": [{"line": "...", "anchors":
  [{"publisher": "...", "title": "...", "url": "...", "where": "...", "quote": "...", "read_on": "...", "check":
  "confirmed"}]}]}}}`: two to four short lines, shown as one short paragraph, each line with its source chips (as in 3).
- `signs.<family>.self`: a list like `while_waiting` (`line`, `anchors`).
- `data/site/kit-links.json`: `{"_note": "...", "sellers": {"<key>": {"name": "DanceSafe", "home": "https://…",
  "drugs": {"<slug>": {"url": "https://…", "label": "MDMA test kits", "read_on": "2026-11-15", "check":
  "confirmed"}}}}}`; match sellers to today's seller rows by name.
Put a tiny sample of each shape in a scratch copy to test the rendering; do not commit sample data.

## Borders with the Insight builder (branch `ins23`)
You own: `site/src/app.simple.js`, `site/src/app.views.js`, `site/src/index.template.html`, `site/build.js` (except its
Insight step), `scripts/ux/redesign_check.js`, `smoke.js`, `speed_check.js`. The Insight builder owns
`site/src/app.insight.js`, `scripts/insight/*`, `scripts/ux/insight_check.js`, the quiz's "Read the answer" link, and
the "Read next" / "Next questions" blocks (it will touch a few lines of your files for those two; leave them alone).
`site/src/styles.css` is shared: keep your new rules in one block marked `/* 2.3 pages */`; do not reformat the file.
Hash routes are the contract between you: `#s-<drug>/q-<claim>` must open that drug's page with the right section and
the question open and in view; the answer sheet's "See it on the … page" link relies on it.

## Design rules
Keep the site's look (type, colours, dark and light themes); calm, few things on screen; no new banners, badges or
notes; sentence case; plain words a person who did not finish school understands; nothing that reads like a warning
label. Works with keyboard and screen reader (the section menu is a real tablist or disclosure set; state is announced);
reduced motion respected; no sideways scroll at 390; no console errors. The start page still fetches none of Insight's
files. Do not add analytics, cookies or outside requests. If an automatic filter stops a step, do not retry or reword
it: note it and go on.

## Report (under 350 words)
What changed, the section order you derived, what "Full" held that is no longer reachable (if anything), every line you
removed as clutter, check results (numbers), and screenshots saved with `--shots` in a folder you name (390 and 1280:
drug page first view, a section open, a question open after a deep link, "If it gets too much", "Test kits", the
evidence view, "How to read this site").
