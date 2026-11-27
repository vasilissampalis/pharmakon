# Expansion plan: a site that grows by itself, within the month's money (Claude Fable 5.2, 27 November 2026)

For the senior author's review. **A plan only: nothing here is built, switched on or changed.** No code, setting, workflow
or gate was touched to write it. Read with `docs/EXPANSION-NOTES-2026-11-27.md` (the editor's notes of the night) and
`docs/OPENROUTER.md`.

His words this plan answers (26 November 2026): the system "should create new pages ... if there is not an already
predicated page/section for what people search", "automatically find pictures", "enrichen every existing section too ...
Even myth and facts", "understand what is missing in the best token-saving manner", "last the whole month with user
questions always being answered the best way possible", "People don't like waiting at all and want outmost accuracy", "the
myth and fact questions have to be based on actual searches", "tokens to reach their limit when the month absolutely ends
not before that".

## One page: what I propose

**The finding that shapes everything.** Money is not what limits the site today. Quality is. Of the 98 answers the system
has published, the editor's readers held 56 (`data/auto/held.json`; the notes, "The editor's reading of everything"). Of 321
tries on record, 58 were published (`data/auto/answers/`, counted today). So of what the system tries, about one in eight
ends as an answer that stands. Writing more with the same machine would mostly write more answers to hold. The plan therefore
makes the system **better first, then bigger**, and lets how much it writes follow how well it writes.

1. **One map of what is missing, made by code alone** (no model, no money): a new `scripts/auto/missing.py` joins what
   already exists (demand scores, the lists of questions, where each question belongs, which answers are held, which are
   never found, which cards exist) into one ranked list of five kinds of gap: a page, a section, an answer, an answer to
   improve, a myth-or-fact card. The lane works from the top of it.
2. **No thin pages.** A page the system starts appears in the menus only when it holds at least three shown answers, one of
   them "what is it". Until then a person who searches for it still lands on something useful, but it is not presented as
   a page. Topic pages (drug tests first) are started the same way as drug pages.
3. **Enriching what exists**, by demand: answers people marked "not what I asked", held answers, answers nobody can find
   because no ways of asking were written, sections with questions and no answers.
4. **Myth-or-fact cards written by the system**, only from a question people really ask that already has an answer which
   stands, through nine gates in code, labelled, and only after an exam and after the editor has read the first twenty.
5. **Money that ends with the month.** One change in `llm.pay_share`: instead of a fixed share a day that is lost when not
   used, the list may spend up to a straight line from the month's first day to its last. A quiet day is caught up; the
   line is never overtaken; visitors come first at every hour. Counted from OpenRouter's own figures, not from our ledger
   (which lost spending last night).
6. **Money left over goes to checking, never to writing with weaker checks**: both second readers together, then a third
   reader before publishing.
7. **Faster for a person who waits**: the paid, fast team first for a sent question; sources fetched before any model is
   asked; the time each step took is measured and shown to him weekly.
8. **Five phases**, the first costing nothing and publishing nothing. **Ten decisions are his**; they are listed at the end.

What a month buys, honestly (arithmetic in section 5): at today's quality about 70 answers that stand from the $9.50, plus
what the free services give; at the quality phase 1 aims for, about 110 to 150.

## How I read what was unclear

- "Never an empty or thin page" is the editor's brief, not his words; I took it as a rule for display (stricter), not a
  reason to write faster.
- "Tokens reach their limit when the month ends" I read as: the paid money (OpenRouter) is used up at the month's end,
  within about one day's share ($0.30), and each free service's daily allowance is used each day where quality allows.
  Exactly zero is not possible; going over is worse than staying a little under, because unused credit is not lost (it
  stays in the account for a year, `docs/OPENROUTER.md`, "Expected costs").
- "Best and fastest" where they pull apart: accuracy wins for anything published; speed wins only in what is tried first.
- "Automatically find pictures": finding is automatic already; showing still needs the editor's look
  (`site/build.js`, the comment above `okPic`: "No program can judge that yet"). I keep that until an exam says otherwise.

## 1. Finding what is missing, cheaply

**What exists** (all code, no model): `data/site/demand.json` (how much each theme is asked, from his Reddit pages and seven
forums); `data/site/wanted.json` (52 questions, counted by number on visitors' devices) and `data/auto/wanted-auto.json`
(272, our wording); `scripts/auto/place.py` (`Placer.place`: every question gets a home; `pages()` writes
`data/auto/pages.json`, 57 pages to start, ranked by listed questions, forum questions, Wikipedia views);
`scripts/auto/grow.py` (`candidates`, `run`: asks the most-asked themes about each page, never twice, nearness 0.80);
`scripts/auto/scout.py` (`groups_of`: groups questions by meaning); `data/auto/topics.json` (where an answer stands on its
page); Insight's "Not what you asked? Search wider", which sends the id of the answer that did not answer (decision 33).

**What is missing** is one place where these are weighed against each other. Today each script has its own queue, so the
lane cannot tell whether its next dollar is better spent on a new page, a held answer or a card.

**Proposal: `scripts/auto/missing.py` writes `data/auto/missing.json`.** Code only. For every gap, one line: kind, where,
our wording's id, and a score.

| Kind of gap | How code sees it (no model) | Built on |
|---|---|---|
| A page | questions whose home is `new:<name>`; ranked as now | `place.pages`, `pages.json` |
| A topic page (not a drug) | a group of 5 or more listed questions (`scout.groups_of`) whose home is a general page or none, and that no page's sections are near | `place.TOPIC`, `GENERAL`; new file `data/auto/topic-pages.json` |
| A section of a page | 3 or more questions homed on a page, none near a topic the page has (`build_index.py`, `auto_place`) | `topics.json` |
| An answer | a listed question with no shown answer; a theme of `grow.json` a page lacks | `grow.candidates` |
| An answer to improve | held (`held.json`); marked "not what I asked" three times or more; `complete: false` in its record; no ways of asking (109 such, the notes); written by an older lane | answer records, `/api/ask` counts |
| A card | an answered, much-asked yes-or-no question with no card in the page's deck | `data/site/simple.json` (`tf`), section 4 |

**The score** = demand × chance × stakes ÷ cost, each from files:
- demand: the theme's score in `demand.json`, plus the device counts for a listed question, plus 1 for each time a person
  sent it (a sent question is always first and is not ranked at all: see section 5);
- chance: 1 where sources are already on file for it (`lane.found_now`), 0.3 where its last try ended "no source that can be
  read", 0 while a source could not be fetched today (a fault of the moment, tried again by the existing rules,
  `SOFT_FETCH_A_DAY`);
- cost: 1 for a card (one short call and checks), 3 for an answer, 12 for a page (four answers).

**Where tokens are saved.** Of 119 tries that gave no answer on 24 to 26 November, 43 failed on sources (35 with none that
gave a finding, 23 of those because nothing could be fetched; 8 with too few) (the notes). A try that will fail on sources
should cost nothing: **before any paid model is asked, the lane counts what it fetched; below the floor (one review in full,
or one official page, or two studies) it stops and writes down why.** In `lane.make` the fetching already comes first
(`Begun`, sources read at once); the change is that team choice (`lane.team`) happens after the count, not before. To
confirm in the code when building. Nothing is loosened: the floor is the present one.

A model is used in this whole section for one thing only: naming a new topic page or section (one call, kept), and the
name must pass code (at most four words, every word taken from the group's own questions, none of the lane's refused
words, `lane.RULES`). The editor confirms a topic page's name before it is listed (see decision 9).

**Measured before it steers anything:** `missing.py --eval` on the 447 real questions `place.py --eval` already uses: the
editor judges 60 gaps drawn at random (is this really missing? is the kind right?). Bar: 55 of 60, as `place.py` met (57 of
60, decision 15). Until then `missing.json` is written and read by nobody.

## 2. New pages and sections

**What exists.** `place.py` and `data/auto/filing.json` name drug pages; `grow.py` asks a new page's first four themes
(`grow.json`, "first": 4, "the first four make a page worth opening"); `scripts/auto/pictures.py` finds pictures (GBIF,
Wikimedia Commons; `OPEN`, `free_licence`, `RULE` for CC BY-SA) and `pictures.editor` records the editor's look;
`site/build.js` shows a started page as soon as one listed question exists, even with no answer (`AUTO_SHELL`; its own log
line: "pages people asked about are shown as started, with no answer yet").

**Proposals.**

1. **The opening rule (stricter than now; `site/build.js`, where `startedPages` is filled).** A started page is listed
   under "All drugs" and in search engines only when it has three shown answers, one of them the "what" theme. Below that
   it stays reachable from a search on the site as a plain landing: the name, "questions being answered: N", the official
   bodies' pages (`OFFICIAL`) and the papers by title (`/api/find`), with `noindex`. Nothing of ours that is thin.
   A page that falls back under three (answers held) leaves the menu by itself.
2. **Topic pages.** New file `data/auto/topic-pages.json`: name, the words that send a question there (as `place.TOPIC`
   does for the six general pages), the Commons categories for its pictures, its own order of themes. First candidate, by
   the demand files: **drug tests** (how long a drug shows, which tests, false positives); the existing "checking" page is
   about checking a drug, not testing a person. `place.py` gets one more home kind (`new:topic:<name>`); `grow.py` asks its
   themes; the lane writes them as any answer. Themes about beating a test stay refused (`ask.NOT_ANSWERED` already
   refuses "cheat, beat, fake").
3. **Sections.** When `missing.json` shows a section gap, the answers already carry their place (`topics.json`,
   `auto_place`); the build makes the section heading from the kept name. A section is shown from two answers.
4. **Pictures.** As now for drug pages. For topic pages `pictures.commons_category` is given the categories of
   `topic-pages.json`. The licence rules and the editor's look stay. To make the look automatic later, phase 4 proposes
   an exam: `data/auto/pictures.json` holds every picture the editor accepted or held, which is a ready test set for a
   model that sees pictures (Google's free Flash models do). Not before he says so (decision 10).
5. **Class.** A started page shows no class until a person confirms it (decision 22 of `docs/AUTOMATION.md`); unchanged.

**Measured:** after one week, how many started pages reached three answers, how many tries each took, and the editor reads
every answer of the first three pages that open.

## 3. Enriching every existing section

One queue, from `missing.json`, kind "answer to improve" and "answer", for the 30 checked pages and the started ones alike.
Order within equal demand:

1. **Held answers** (56 now). Each hold carries what to say to the next writer (`held.json`, "say"; `lane.held_say`). They
   are the cheapest good work: the question is known to be wanted and the sources are on file.
2. **Answers people said did not answer** ("Search wider", three times or more for one answer id). The lane writes the
   question that was really asked as a new item (our wording, never the visitor's), not a longer old answer.
3. **Answers nobody can find**: no ways of asking. `scripts/insight/teachers.py` writes them from our words with free
   models; proposal: an answer is not counted as "published" in the weekly numbers until its ways exist, and the Auto run
   does the newest first.
4. **Themes a page lacks** (`grow.candidates`, line b), as now, but taking its order from `missing.json`.
5. **Cards** (section 4).

**How he wants it written** applies to every one of these (his comments of 12 and 13 November, the notes): short, the
answer first, the drug named, nothing nobody needs. Three of these become code in the lane's gates, each stricter:
- the short answer, its But and points together at most 140 words (now `LIMITS`: short 50, but 40; no total);
- every drug or thing named in the question is named in the short answer (catches "the question narrowed": only cocaine for
  "cocaine and alcohol");
- the words the readers marked as jargon at the top are added to `lane.CLINICAL`.

**The checked lane is never edited by the system** (CLAUDE.md). For a checked section the system does two things only: it
places its own labelled answers under the section's topic (as now), and it adds the papers a much-asked gap needs to
`data/auto/papers-wanted.json` for him and the editor's readers.

## 4. Myth-or-fact cards written by the system

**Today:** 531 checked cards in `data/site/simple.json` (`tf`: deck, claim, statement, answer, why), written from checked
answers, blind-checked, shown by interest (`data/site/tf-interest.json`, cut 4.0 for interest and for clarity).

**Where a system card comes from (demand, by code).** A card is proposed only when all three hold:
- the question is one people ask: on a wanted list with a demand score at or above the median of `demand.json`, or sent
  or counted by visitors at least three times;
- it is a yes-or-no question (`lane.YES_NO`) or a belief ("is it true that", "I heard"), found by pattern;
- it has an answer that stands: a checked claim, or a machine answer that is shown, not held, of the present lane, whose
  short answer opens with a plain Yes or No (`lane.opener_of`). "Sometimes" and "It depends" give no card.

Then one free model writes the statement (the belief, in people's words, at most 20 words) and the why (at most 30 words,
from the answer's own short line and But). It is told the key; it does not choose it.

**The gates (all in code, in a new `scripts/auto/cards.py`; a card that fails one is dropped, not mended by hand):**

| # | Gate | Reuses |
|---|---|---|
| 1 | Source stands: shown, not held, present lane; never from an answer about amounts | `lane.is_held`, `shown_from`, `is_amounts` |
| 2 | Never from, or about, dying, overdose, pregnancy, children, suicide or self-harm, an emergency | `lane.STAKES`, `NEVER_ALONE`, `place.OVERDOSE` |
| 3 | No amount, dose, timing, redosing, way of taking compared, or reaching or strengthening an effect, in the statement or the why; no number at all unless it stands in the source's passage | `lane.AMT`, `PER_KG`, `TIMING`, `REDOSE`, `RULES`, `FORMS`, `numbers` |
| 4 | Mixing only as a risk: a card that `place.MIX` matches must state a risk and must not reassure | `lane.REASSURES`, `POINTS_HIGH` |
| 5 | The key is right, blind: two models of different families are shown the source's passages and the statement, not the key, and say true, false or cannot tell; both must give the key | as `scripts/auto/blind_lines.py` does for plain lines |
| 6 | The why says no more than the answer: each sentence passes the lane's own checks against the same passages | `lane.check`, `says_more`, `hedge_dropped`, `copied_run`, `second_hand` |
| 7 | Worth reading: two raters, blind to each other, interest and clarity both 4 or more | the method of `tf-interest.json` |
| 8 | Not a card we have: nearness under 0.80 to every statement in the deck | `grow.SAME` |
| 9 | The label and its place: kept in `data/auto/cards/`, never in `simple.json`; shown with "Drafted automatically from …" and no certainty bars; a card whose source is later held leaves by itself | CLAUDE.md, decision 42 |

**The exam, before one card is shown** (`data/auto/exam/cards.json`, built from our own records): the 531 checked cards as
good ones; faulty ones made from them in four ways, at least 40 each: the key turned round; a why that says more than its
claim (taken from the plain-lines exam's refused lines, `exam_lines.py`); a card breaking a content rule (written by the
editor); a dull or unclear card (those under the cut in `tf-interest.json`). Bars: gates 3 and 4 catch every rule-breaking
card (code, so 100%); of the cards the whole chain lets through, at most 2 in 100 wrong (the bar `docs/OPENROUTER.md`
names for a checker trusted alone); at most half of the good ones stopped. Then the editor reads the first 20 real cards in
full; then cards go live a deck at a time. If the bar is not met, no card goes live and the plan says so.

**Cost:** about 6 short calls a card on free models; with the paid second reader for gate 5, about $0.001. Two hundred
cards a month: $0.20.

## 5. Money and tokens over a month

**As it is** (`scripts/auto/llm.py`, `pay_share`; `data/auto/lane/pay.json`): a person's question may spend at any hour
while the pot holds; the list may spend, a day, the lesser of (what is above the visitors' floor ÷ days left) and
(`even`: the pot ÷ the month's days), and what a day does not use is not carried. `follow_credit` (`credit_left`) keeps the
pot within what the account holds.

**What was measured** (`data/auto/lane/usage.json`, read today): 27 November: the list spent $0.315, which is the whole
day's share (9.50 ÷ 30 = $0.317), visitors' questions $0.25; 63 tries, 9 published; the credit left is $9.05. So:
- a try costs about $0.57 ÷ 63 ≈ **$0.009** (more than the $0.006 foreseen: GPT-6 Luna reasons before each verdict, and
  stops about 1 good sentence in 4, so drafts are written again);
- a published answer about $0.57 ÷ 9 ≈ **$0.06**; an answer that stands, at today's rate of holds (56 of 98), about
  **$0.13**; so $9.50 buys about **70** a month. If the new gates bring holds to 1 in 4 and the sources check saves the
  tries that cannot succeed (a third of them), about $0.06 ÷ 0.75 × 0.75 ≈ $0.06 to $0.08: **110 to 150** a month.

**Three faults in the present pacing, against his wish.**
1. `even` loses what a day does not spend. A day with no sources, an outage or a quiet night leaves money over at the
   month's end.
2. The count comes from a shared ledger that overlapping runs overwrite: last night it showed $0.02 where $0.43 had been
   spent (the notes). Pacing to the cent needs a count that cannot be lost.
3. Exams spend from the list's day ($0.35 of November's first $0.41), so an exam day writes no answers.

**The change, exactly.**

*a. Count from OpenRouter itself.* `credit_left` already reads `total_credits` and `total_usage` from OpenRouter. Keep
`total_usage` as read on the month's first run in a small file of its own, written once (`data/auto/lane/month.json`:
month, usage at its start). Spent this month = usage now − usage at start. A purchase in mid-month changes nothing in this
sum. Our ledger stays for the split by day and kind, written as one file a run (`data/auto/lane/usage/<run>.json`), so no
run can overwrite another.

*b. A line instead of a daily share* (new key `"line": true` in `pay.json`; `even` stays in the code so that one word
switches back). For the list, at time *t* of a month that runs from *t0* to *T*:

    may have spent by now = (pot − kept for visitors − kept for exams) × (t − t0) ÷ (T − t0)

- pot = the lesser of `usd_a_month` and (spent + credit left), as now;
- kept for visitors = what they spent so far + (their busiest day of the last seven, at least `visitors_least_a_day`) ×
  `margin` × the days left, counted in hours, so it falls to nothing by the last hour;
- kept for exams = a new `exams_a_month` ($0.50), spent only by exams;
- *t0* = the month's first day, or the day the pot was first there (so a month begun late is spread from that day).

A list call is allowed while list spending + its cost stays under the line. What this gives: a day that spent little is
made up on the next days by itself; spending can never run ahead of the calendar, so the money cannot end before the
month; at the last hour the line equals the pot. One more guard, `day_most`: 3 times an even day, so a bad day cannot
spend a week's catching-up at once.

December, in numbers. Bought every month: pot $9.50, line $0.29 a day after $0.50 for exams, about 32 tries a day. Bought
once: November may still spend at most 4 × $0.317 = $1.27, so about $7.80 to $9.05 enters December: $0.24 to $0.28 a day.

*c. A person's question* is as now: any hour, while the pot holds, never waiting for the line.

*d. Where there is more money than work.* If list spending is more than one day behind the line, the lane does not write
lower-demand answers. It buys more checking, in this order: both second readers together on every answer (they catch 51 of
60 faults where Luna alone catches 47; exam-0027); the third reader on the oldest answers still shown; a paid reader for
sources the free readers could not read (`reader_last`, built on 27 November).

*e. The self-tests* (`llm.pay_selftest`, `or_selftest`) get made-up months: a quiet week, a week of many visitors, a month
begun on the 26th, credit bought on the 15th, OpenRouter refusing (402), two runs at once. Each must end between the pot
minus one day's share and the pot, and never above it.

**Bought every month, or once.**
- **Every month** ($10.80 charged): everything above, each month. This is what I recommend, for a reason beyond volume: the
  second reader that makes answers right (Luna: about 5 wrong in 100 let through) exists only while there is credit. Without
  it each team falls back to its own second reader (gpt-oss-120b: about 20 in 100; `models.json`, the note of
  `checker_first`).
- **Once**, two ways, and he chooses: (i) *spend it all by 31 December*, as his words say; from January the free models
  alone, with the weaker second reader, and the "volume follows quality" rule of section 6 will slow the list by itself;
  (ii) *keep it for accuracy and for people who wait*: paid money only for the second reader and for sent questions;
  writing and reading stay on the free services. A check costs about $0.0007 (measured: $0.57 ÷ 869 calls); 60 checks a
  day is about $1.30 a month; the credit then lasts about six months. If he does not buy monthly, I recommend (ii).

**The free services, used fully first.** Read from `usage.json` and `data/auto/lane/free-limits.json`:

| Service | A day allows | Used | Proposal |
|---|---|---|---|
| Cloudflare | 10,000 neurons (9,000 for the lane) | 27 Nov: 8,922 by 00:55 UTC, 7,445 of them by the reader | kept for questions people send (it is fast); the list reads elsewhere |
| Google, Gemma 26B and 31B | 14,400 calls each | 26 Nov: 295 | the list's reading goes here first (`models.json`, "readers" order); it is slow and sometimes refuses (503), which the 7-minute clock already bounds |
| Google, Flash-Lite ×2 | 500 calls each | 26 Nov: 904 | as now: the further second readers |
| Groq | 200,000 tokens a model | most of it, daily | as now: planner and writers |
| OpenRouter free models | 900 calls | unused by teams | exam first, then card raters (gate 7) |

A reader only copies and code checks every quote (`lane.read_gate`), so moving the reading changes how much is found, not
what is true. Measured first: the same 20 questions read both ways, findings counted.

## 6. Quality: nothing loosened, and how it is watched

**No gate is loosened anywhere in this plan.** Every change to a gate here adds a refusal.

1. **Gates the readers' catches ask for** (the notes: code can catch the first three kinds). Some exist since last night
   (`lane.hedge_dropped`, `intro_hand`, `second_hand`, `copied_run`, `repute_as_fact`, `is_case`). To add: a passage from a
   methods section or an abstract's opening may not carry "found"; an animal finding may not lead; the question's things all
   named (section 3); the 140-word total. **Each is measured before it is on:** the 35 answers held on 27 November and the
   42 still shown are the test set (`data/verification/auto-read-2026-11-27/`); a gate goes live if it catches held ones
   and stops at most 1 in 10 of the shown.
2. **Every hold becomes an exam sentence** (`scripts/auto/exam.py`, build step): the exam grows with each fault (it grew
   from 108 to 287 sentences this week), and a second reader keeps its place only by sitting the grown exam monthly
   (cost about $0.05 a sitting).
3. **A third reader before publishing** (a new gate, so stricter): one strong model reads the whole answer with its
   passages by the editor's eight rules (`data/verification/auto-read-2026-11-27/BRIEF.md`). Its exam is ready: the 54
   answers the readers judged (35 held). Bar: it holds at least 30 of the 35 and at most 4 of the 19. Which model: the one
   the exam shows, within a ceiling of $0.003 an answer (150 answers: $0.45 a month). Until it passes, the editor's
   readers go on reading everything published, as last night.
4. **Volume follows quality** (`data/auto/lane/policy.json`, a new number beside `pause`): of the last 30 answers
   published and read, if more than 6 were held, the list writes at half the line; more than 12, the list stops and only
   sent questions and held answers are worked on. It rises again by the same count. The money not spent goes to checking
   (5d).
5. **Five numbers a week** in `data/auto/report.json` and on his to-do page: the share held of what was published (now 57
   in 100; the aim before volume is raised: under 10); what the second readers catch on the exam; Insight's gold set
   (`scripts/insight/build_index.py --eval`); minutes from a sent question to its answer (median, and the slowest tenth);
   dollars for an answer that stands.

## 7. Speed for a person who waits

What exists: the server starts a run when a question is sent (`GH_RUN_TOKEN`), seven minutes at most a question
(`lane.QUESTION_SECONDS`), sources read six at once (`AT_ONCE`), the waiting page fed by `data/auto/live.json`, papers shown
at once (`/api/find`). What slows it, from the records: free services that queue or refuse (Gemma's 503s; one reading step
of 34 minutes on 20 November, `docs/STATUS.md`), a team chosen that then cannot read, and an answer sent back by the second
reader.

1. **The fast team first for a sent question** (`models.json`: a `teams_sent` order; `lane.team(only=…)` exists). Paid
   reader, writer and second reader at OpenRouter, with `provider.sort: throughput` as set. Free teams after it, not before.
   Cost at $0.009 to $0.02 a question: 10 questions a day is $3 to $6 a month, inside the pot and ahead of the list by rule
   (5c). If visitors grow beyond that, the floor in the line makes room for them by itself.
2. **Sources before models** (section 1): a question with nothing to read says so in seconds, and the page already shows
   the papers by title.
3. **Both second readers at the same moment** for a sent question about dying, overdose or mixing (the `strict_lacks`
   kinds): no added wait, more caught. For other sent questions Luna alone, to keep rewrites few.
4. **One rewrite, at once, by the fix the reader named** (as now, `writer_prompt`, `fix`), inside the same seven minutes.
5. **The best speed is an answer that is already there**: the whole of sections 1 to 3. Each week the report says what
   share of sent questions Insight answered at once from the site.
6. **Measure, then promise.** Each record already holds its run's notes; add the seconds of each step in one shape, and
   report the median and the slowest tenth. `policy.json` "loop" stays false until the numbers keep the promise.

## 8. Phases

| Phase | What | Publishes? | Costs | Measured before the next |
|---|---|---|---|---|
| 0 | The count from OpenRouter and one ledger file a run; the line in `pay_share` with its self-tests; `missing.py` (read by nobody); holds into the exam | nothing | $0 | self-tests pass; the editor judges 60 gaps (55 right) |
| 1 | The new code gates; sources before models; the third reader's exam; the opening rule for pages; "volume follows quality" | as now, fewer and better | exams about $0.30 | held share of the next 30 answers; the third reader's bars |
| 2 | The lane takes its order from `missing.json`; held answers and unfound answers first; the fast team for sent questions; reading moved to Gemma for the list | answers, as now | within the line | minutes to an answer; dollars for an answer that stands; held share under 10 in 100 |
| 3 | Topic pages (drug tests first) and sections; cards: the exam, the editor's first 20, then a deck at a time | new kinds, each after its measure | cards about $0.20 a month | the editor reads the first three pages and 20 cards in full |
| 4 | A model's look at pictures (exam on the editor's past looks); more free services when he makes keys (Mistral, SambaNova) | only on his word | free | the exam's result, shown to him |

Phase 0 can be built tomorrow with no risk to the site: it changes no gate, publishes nothing, and its money change can
only spend more slowly than now on any single day unless a day was missed.

## Decisions that are his alone

Each can be answered yes or no. My recommendation is in brackets.

1. **Will you buy $10 of OpenRouter credit every month?** [Yes. The accurate second reader exists only while there is credit.]
2. **If not: should the rest be spent by 31 December** (then free models only, with the weaker checker), **or kept for
   checking and for people's sent questions only**, lasting about six months? [Kept.]
3. **May a page the system starts stay out of the menus until it has three answers that stand?** [Yes.]
4. **May the system slow its own writing by itself when too many of its answers are held?** [Yes.]
5. **May money that is left over buy more checking** (both second readers, a third reader before publishing) **instead of
   more answers?** [Yes.]
6. **For a question a person sent: may the paid, fast team be tried first**, at about $3 to $6 of the month's $9.50 if ten
   people a day send one? [Yes.]
7. **May the system write myth-or-fact cards, labelled "Drafted automatically from …", once the exam is passed and the
   editor has read the first twenty?** [Yes.]
8. **May such a card rest on an answer the system wrote** (shown and not held), **or only on checked answers?** [Both; cards
   from system answers leave by themselves if the answer is held.]
9. **May the system start pages that are not drugs, beginning with drug tests, with the editor confirming each page's
   name?** [Yes.]
10. **May a model's look replace the editor's look at pictures after an exam?** [Not yet; decide when the exam's result
    is in front of you.]

Nothing in this plan changes until he answers; phase 0 touches no gate and can be built on his word "go".
