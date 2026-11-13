# Redesign 2 (preview), 13 November 2026: less like school, more like the sites people love

The senior author's words: the site "has so much info it is like the user gets tested in school"; a visitor would say
"okay nice try", use it a little and leave; "we have to be based on websites that users really love and like to use".

The editor's diagnosis (phone, 390 px): the content is strong but every answer has the same four parts (question, short
answer, "But", evidence bars), repeated 20 to 40 times a page; the cannabis page is about 11 phone screens; nothing says
where to start or what is surprising; the quiz is called "Test yourself". Research already on file:
`docs/REDESIGN-RESEARCH.md` (people read about a fifth of the words; attention stays on the first two screens; groups of
at most four; progressive disclosure, but not beyond two levels; numbers as natural frequencies and icon arrays; real
photos help low literacy).

Models (what each does well, and what we take): Examine.com (a one-glance table of outcomes and how sure the research
is, before any text); Wikipedia (each page invites the next click); Duolingo (tiny bites with instant feedback, playful;
we take the bites and the feedback, never streaks, nagging, points or notifications); Our World in Data and the New York
Times (one picture makes a number obvious); "myth or fact" cards people share.

## What the preview changes

1. **Home: "Myth or fact?" deck as the first thing below the search box.** Cards built from the existing true-or-false
   items (`simple.json` `tf`: `statement`, `answer`, `why`, `claim`, `v`; only items whose claim is published and whose `v`
   matches, exactly as the quiz does today). A card shows the statement and two buttons, **Myth** and **Fact** (answer
   false = myth, true = fact). Tapping flips it in place: the verdict ("Myth" or "Fact"), the `why` line, the answer's
   evidence bars and label, and a link to the full answer on its page. Then **Next**. A deck is 10 cards in a new order
   each visit, then "Another 10". A plain count is fine ("4 of 10"); no score shame, no streaks, no timers. Prefer short,
   surprising items: statements of at most 20 words first. The three utility doors (Is it safe to mix? / Test what you
   have / Someone is unwell) stay on the home page, right below the deck; the search box stays at the top.
2. **Drug pages start "At a glance".** Directly below the header photo and the emergency line: a single screen of at most
   8 tiles, in at most 4 labelled groups (the page's own topics, preferring Stay safer, What it does / feels like, Myths
   and facts, As a medicine). Each tile: the question (short form allowed if the data has one; otherwise the question as
   written), the first clause of the short answer (cut at a clause boundary, never mid-number, at most about 60
   characters, with an ellipsis), and the evidence bars. Tapping a tile scrolls to and opens that answer. Below it, the
   existing topic sections stay (they are the full list), with the topic chips as now.
3. **Lighter answer cards.** Closed card: the question, the short answer and the evidence bars with their label (the
   bars must stay visible: they carry how sure we are). The "But" line moves into the opened card, at the top, before
   "How do we know?". Opening is one tap; the second level ("The evidence") stays a link. No third level.
4. **Numbers as pictures.** When a short answer contains a natural frequency "N in 100" (N a whole number 1 to 99), the
   opened card shows a 10 × 10 grid of dots with N filled, labelled in words ("N in 100"), `aria-hidden` on the dots and the
   words read out instead. Only for "in 100"; nothing for ranges ("43 to 49 in 100") in this preview.
5. **Read next.** At the end of an opened answer, up to 3 links to other answers: first the next answers in the same
   topic, then one from a "Myths and facts" topic on any page. Titles only.
6. **Names.** "Test yourself" becomes "Myth or fact?" wherever it appears (home, menu, page title). The quiz page keeps
   working as now under the new name.

## What must not change

The evidence one tap away; the emergency access; the legal box; every safety note; the citations. (The draft notice was removed on 13 November at the senior author's instruction; METHODS 0.3.2.) No
dosing, administration or potentiation content anywhere. No manipulative patterns (no streaks, points, badges, timers,
infinite feeds, notifications, guilt copy). Phone first (390 px, no horizontal scroll, 16 px gutters), keyboard
reachable with visible focus, `prefers-reduced-motion` respected (the flip becomes a fade or nothing), colour contrast
AA, light and dark themes as now. The single-file build (`node site/build.js`, `python3 -I site/build_public.py`) keeps
working, and the existing tests pass (`scratchpad/ux/smoke.js`, `newq_check.js`, `quiz_test.js`).

## Writing

Use only text that already exists in the data (questions, short answers, `why` lines, topic names). New interface words
only for controls and labels, in plain sentence case: "Myth or fact?", "Myth", "Fact", "Next", "Another 10", "At a
glance", "Read next", "Read the answer". No new claims.
