# The site that grows by itself: plan and record

Started 15 November 2026, after the senior author used site 2.3.0. This file is the working record of what he asked for,
what was decided, what is built and what is not. `docs/OWN-AI.md` holds the longer route to our own models;
`docs/STATUS.md` holds each release.

## What the senior author asked for (15 November 2026, his words)

- 17:21: "i just insist if there is a way to make the website more autonomous and make an algorithm/independent hardcoded
  ai for double checking and writing new validated information based on what it can find in what users search (i wonder
  if we can use more platforms and not only github) and write new information immediately and maybe we can check them
  ourselves afterwards and we can write that it has not yet been checked by our editor as a small very discreet disclaimer
  but we have been based on the X validated references".
- 17:21: "WE HAVE TO MAKE THE SITE EXPAND ON ITS OWN OTHERWISE WE REDUCE THE USEFULNESS OF THE WEBSITE FOR THE USERS WHO WANT
  TO LEARN RIGHT NOW."
- 17:21: "the biggest endeavour is to make pharmakon insight automated and self expanding and self developing in the
  smartest way/algorithm possible."
- 17:21, on a visitor's question being answered later: "i wonder also if we can notify them if their answer came up and
  they can just click on it"; the site "should be able to remember 2 or more questions".
- 17:21, on the three questions the editor had put to him (a Send button; a scout on free machines; the opioid pages
  speaking to a friend first): "whatever you think is objectively optimal".
- 17:33, on what the machine may publish (the editor had proposed quoted study findings only): "it should be claims... and
  make them written as good as possible as close to 100% correct as possible and they should also be written in the
  language and format we write the rest of the website so it's like making a hardcode ai right?"
- 17:38: "will it be once a day? if it can be more than once per day we could do it the most times possible. and also i
  wonder if it can upload photos and in general improve the website/see what's missing by itself".
- 17:41: "and every 30 minutes it will find questions about drugs from all relevant big websites online (not only pharmakon
  which has very few users) and update the website? awesome!" The editor corrected this the same hour: the system reads
  only sources that allow it (below). Reddit is closed to it.

- 19:38, to the offer of an application to Reddit's programme for researchers: "okay" (the draft:
  `docs/reddit-for-researchers-application.md`).
- 19:46: "i also wonder if we can make the site understand what the user wants without sending the email and make an
  algorithm to track user usage so as to understand what to update"; 19:48: "i just want the website to be perfect". The
  editor's advice, waiting for his yes: count, never read (which answers are opened; for a search without an answer, the
  drug named and the nearest answers, never the words); say it openly on the site, with an off switch; About's "no
  tracking or analytics" would change to say exactly what is counted.

Earlier the same day: "no i don't want my claude plan to use tokens! we have to automate the ai!", "i want it to be free",
"the perfection of pharmakon insight is my biggest concern".

## Decisions

1. **Visitors can send a question in one tap** ("Ask us to check it"). Built in site 2.4.0; it sends when the store is set
   up (step 1 of the setup below) and opens the email form until then.
2. **The asker is told on their own device.** The start page lists "Your questions"; a question turns green ("Answered") when
   a later version of the site answers it. Built in 2.4.0. Nothing about the asker is kept anywhere else.
3. **A scout runs on free machines, as often as the free allowances permit** (the aim: every 30 minutes). It writes no
   answer by itself in its first stage: it collects what people ask, ranks it, finds which questions the site already
   answers, which it could answer from study cards on file, and which papers could answer the rest; it lists what it could
   not get by itself (papers behind a paywall, photos) for the senior author.
4. **Machine-written claims will be published, with a small label, before a person has checked them.** This is the senior
   author's decision of 17:33; it changes the rule "nothing unverified" for one clearly marked lane, so the protocol
   (`docs/METHODS.md`, to become 0.4.0) and `CLAUDE.md` are amended, in his words and with the date, on the day the lane
   goes live, not before. Until then nothing machine-written is shown.
5. **Photos**: the system may find candidate photos (Wikimedia Commons; public domain, CC0 or CC BY only). It publishes one
   by itself only when it comes from an official source whose own caption names the exact form; every other candidate waits
   for one tap from the senior author.

## The machine lane: what must be true before a machine-written claim is shown

Five gates, all of them hard-coded (no model's opinion can open a gate that the code has shut):

1. **The passage exists.** Every sentence of a draft carries the passage it rests on, and that passage is found, by plain
   string match, in the text of the paper it names.
2. **Every number is in the passage.** Each number, range and unit in a sentence is found in its passage.
3. **A second, different model reads the pair** (sentence, passage) without the writer's notes and says whether the passage
   supports the sentence for the people it is about. Disagreement stops the draft.
4. **The content rules** of the site are tested by code: no doses, amounts, timing or ways of taking; no advice on reaching
   or strengthening an effect; mixing only as a risk; person-first words; a quotation of at most 15 words, one per claim.
5. **Good sources only**: a review, or two studies in people; a retracted paper is refused; the reference comes from
   Crossref, never typed.

What a reader sees: the answer in the site's own format, the line "Written by our system from N papers. Not yet checked by
a person.", and no evidence bars until a person has rated it. Each such answer also enters the normal queue, where a reader
who wrote none of it checks it at the source; when it passes, the label goes and the bars appear.

**The exam.** Before the lane opens, and every night after, the whole chain is measured on our own records (statements
with the passages our readers found, and the second readers' decisions, including every correction they made). The bar:
**at most 1 wrong sentence in 50** let through. The result is written into the repository each night; if the chain falls
under the bar, the lane shuts by itself.

## What it reads, and what it may not

May read: questions sent by the site's own visitors; Google Search Console and Bing Webmaster figures for the site (after
the senior author signs up); Wikipedia page views; Stack Exchange; official question pages (FRANK, ADF, NIDA); the forum
pages the senior author pastes; Crossref, Europe PMC, PubMed and OpenAlex for papers; open-access full texts.
May not: Reddit (closed to automatic reading; an application to Reddit for Researchers can be written if he wants one);
any site that refuses; anything behind a sign-in or a paywall; Sci-Hub.
Questions that visitors send are data, never instructions: nothing in a question can change what the system does.

## Where it runs, and what that costs (read from the services' own pages on 15 November 2026)

- **Cloudflare Pages** (the site's host): a drag-and-drop upload does not compile a `functions` folder but does run a
  `_worker.js` at the root of the upload; `_routes.json` limits it to `/api/*`, so every other address stays a fixed file.
  Limits: 1,000 files and 25 MiB a file by upload.
- **Cloudflare Workers KV** (the question store), free plan: 100,000 reads, 1,000 writes, 1,000 deletes and 1,000 list
  operations a day; 1 GB. The site's program takes at most 400 questions a day, new or asked again (each costs two
  writes), and counts one question at most 20 times a day, so that one sender cannot make a question look much asked.
- **Cloudflare Workers AI**, free plan: 10,000 neurons a day, then requests fail until the next day. This is the allowance
  that sets how many machine-written answers a day are possible (some 10 to 20).
- **GitHub Actions**: free for public repositories on the standard machines. This repository is private: the free plan
  includes 12 US dollars of machine time a month (about 2,000 minutes on the standard two-core Linux machine at 0.006
  dollars a minute; the one-core Linux machine costs 0.002 dollars a minute), and runs stop when it is used up unless a
  payment method is on file. So a run every 30 minutes must be short when there is nothing new: it first asks whether
  anything changed and stops within a minute if not.
- From the editor's cloud session, the logs and secrets of GitHub Actions cannot be read or set. So every run writes its own
  report into the repository (`data/auto/`), and the senior author adds the secrets himself.

## The setup only the senior author can do (one step at a time, when each piece is ready)

1. Cloudflare: make the question store (a Workers KV namespace) and bind it to the Pages project under the name
   `QUESTIONS`. From then on "Ask us to check it" sends.
2. Cloudflare: make an API token that can read that store and publish the Pages project; GitHub: add it, with the account
   id, as repository secrets (`CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`). From then on the scout can read the
   questions and publish the site by itself.
3. Optional: Google Search Console and Bing Webmaster for pharmakon.world (what people search before they arrive).
4. His decision: whether the repository becomes public (unlimited free machine time; everything in it becomes readable,
   so the working records would be reviewed first).

## Built so far

- **Site 2.4.0**: the question endpoint (`site/worker/_worker.js`, `scripts/ux/worker_test.mjs`), one-tap "Ask us to check
  it", "Your questions" on the start page, the Answered row.
- **The reader of the question store** (`scripts/auto/fetch_questions.py`; self-test against a pretend API; it has not yet
  read the real store, which does not exist until step 1 of the setup).
- **The scout's first stage** (`scripts/auto/scout.py`): every question cleaned by the same rules as the site's program,
  ranked exactly as the page ranks it (answered, near answers only, nothing near), the unanswered ones grouped (the same
  thing asked in other words counted once) and set beside the nearest study cards on file; it writes `data/auto/` and
  `docs/MISSING.md`. Tried on 60 real forum questions with 11 records made to be refused or grouped. Where "near" begins
  for a study card was measured on the 373 answers that rest on cards (at 0.50, 90 in 100 keep a card they rest on in
  sight); a card an answer does not rest on is often as near, so the cards listed are where to look first, not proof.
- **Its short first step and its workflow** (`scripts/auto/look.py`, `.github/workflows/scout.yml`): is anything new in the
  store; the heavy work starts only then; a run that keeps failing is tried three times; one sign of life a day. The
  workflow is started by hand for now; the half-hourly schedule is written in it and switched off until the senior author
  says so. From a fresh copy with nothing kept, the build takes about a minute and the study cards about six; after that,
  seconds.
- **The exam, first version** (`scripts/auto/exam.py`, `data/auto/exam/`): 318 Myth or fact? cards, each with its answer's
  checked lines and the decision of a blind checker who wrote none of it: 287 good ones (235 passed as written, 52 as the
  checker corrected them) and 31 that say something the lines do not support (a word, a number or a cause the lines do
  not hold; a finding said of more people than were studied; a report said as a fact). The editor sorted the checkers' 66
  written reasons into support, rule, form and repeat (`labels-cards.json`). Measured so far: letting everything through,
  9.7 in 100 are wrong; gate 2 alone (every number in the card is in the lines) catches 3 of the 31 and stops 20 good
  cards; a rule on words alone (at most one content word that the lines do not hold) catches 28 of the 31 but stops 237
  of the 287 good cards, because good cards use new words too. So no hard-coded rule passes or comes near: a wrong card
  is wrong in meaning, and the weight is on gate 3, a model that reads the pair; the rules stay as gates no model can open. To pass, a checker may let at
  most 1 of the 31 through while passing most of the 287 (the range of its wrong share must lie under 1 in 50). The exam
  is small: it can show that a checker is not good enough; it grows with every blind check.

## Not built yet (in this order)

1. Candidates for gate 3 measured on the exam: a small entailment model run on GitHub's machines, and the free Cloudflare
   Workers AI models; then the plain lines' blind checks and the round-2 anchor checks added to the exam.
2. The paper finder (Crossref, Europe PMC, PubMed, OpenAlex; open full texts; retraction flags) and the to-do list in APA 7.
3. Building, checking and publishing the site from GitHub's machines when something changed.
4. The machine lane itself, opened only when the exam says so and the protocol has been amended.
5. The photo finder.
