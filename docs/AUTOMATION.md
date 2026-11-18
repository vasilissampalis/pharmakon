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

- 20:13, on the scout reading only the papers on file: "not only the papers we hold but whatever it can find online. i want
  the site to grow itself perfectly, we have to make this a masterpiece, genius. and i tell you there is room for growth if
  we don't depend on the users' emails but make the site understand on its own what the users want added in the website
  in-app and not via email. what's the perfect way to design this?" (Built the same evening as site 2.5.0: "On our list".)
- 20:13, on Reddit for Researchers, after pasting its rules (a university affiliation, an institutional email address, proof
  of ethical review and institutional sponsorship): "i am not affiliated to a university so fuck this". That door is closed.
- 20:29: "pharmakon insight should understand trolling because when i wrote this \"can i die from mosquito bites\" the
  response was ... \"We haven't checked exactly this yet. Ask us to check it\" ... this is a drug website there should be no
  mistakes". (Site 2.5.0: the rule for what is a question about drugs.)
- 20:41: "have you made perfect not only how it understands what users who use the website want but also what drug users and
  people interested in drugs search for online? does it find all legit evidence online? is this as smart as it could be?
  does this work like a perfect ai algorithm that we can depend on?" The editor answered: not yet, part by part.
- 20:58, to the editor's "Until a checker passes that exam, nothing machine-written is published": "no it should be
  published and automatically deployed with a very discreet disclaimer and we should just be able to access everything that
  was automatically written and deployed to check whenever we want".
- 20:58, on finding papers: "yes whatever it can find and if there are paywalled papers and the info for an answer is not
  full we should be able to access which papers pharmakon insight wants to make a complete answer and if the automatic
  answer is not complete it should have a small discreet disclaimer".
- 20:58, on what people search online: "everything we can find automated and free so as to give answers and info every 30
  minutes when github will be regenerated right?! this is TOP OF THE WORLD".
- 20:58: "i want no false negatives"; "if in general we make errors like 1 in 1000 the site would be awesome".
- 21:07: "yes and for the responses it should find more than one sources if they are relevant, whatever is relevant, the
  algorithm has to mimick completely how claude writes answers".

- 21:30: "why did you even stop. don't stop until our drug ai works perfectly and expands the site on its own and thinks
  for itself and the algorithm is perfect and expanding and perfectly written and validated and automatically deployed and
  coherent with the rest of the website and automatically deployed every 30 minutes".
- 22:18, his own account of the system (in Greek): every half hour it searches what people ask about drugs on popular sites
  and forums, finds open-access papers and information from valid sites, writes answers that fit the rest of the site,
  tells him which paywalled papers to send, and publishes by itself, and he polishes. The editor corrected two points the
  same minute: it cannot read the popular forums by itself (Reddit and Google do not allow it), and it read papers only.
- 22:24: "I want it to read official websites too where it can get access and also I like that it reads what people ask on
  pharmakon but it should also search every forum page and in general relevant page that it can learn what people want and
  what interests them wherever it can get access to. We have to make it work, get as much info as possible to build the
  site --- and also if the user asks a question we should like have a small notification that their answer will be
  answered in the following hour and when it automatically gets answered their question should turn green or show that it
  has been answered and this should happen with every pending answered question they have. We have to design everything
  perfectly I tell you: top of the world".
- 22:31: "We have to do everything we can do it finds at least part of the answer like 999/1000 times we have to make it as
  smart as we can. Also users can ask lots of things some parts of the answers could come from official sites like NHS and
  EVERYTHING similar it's so many official sites worldwide. --- for example if I ask \"what dosage is safe in MDMA\" I want
  it to find every protocol of dosages from studies that have written about normal dosages or official websites etc
  everything that answers every drug question the user may have".
- 22:40, to the editor's "the page always points to the nearest part of what we already have, and official pages make many
  more questions answerable": "I think technology is so developed that we can make everything answerable perfectly even
  with paywalled articles and some blocked valid websites". The editor's answer: the limit there is permission, not
  technology; the system does not go around a paywall or a site that refuses it. What it may do: read the summary
  (abstract) of a paywalled paper, which is free to read, and say so on the answer.
- 22:40, to the editor's rule that an answer with amounts waits for his tap: "I want it to appear if it is cited by a valid
  website or scientific articles". 22:46, to the one hold the editor kept (opioids and GHB/GBL, whose treatment amounts
  are written for people with tolerance): "disclaimer then man our site has critical thinking towards drugs from the
  beginning". (Decision 11.)
- 22:54: "pharmakon insight should be able to update or criticize answers and are conflicting with other findings or they
  are wrong and either adjust, delete or add new claims". 22:55: "It should not only add but change towards being
  complete". (Decision 12.)

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
   **20:58, his decision on the exam:** the lane does not wait for a checker to pass the exam. What passes the hard-coded
   gates is published and deployed by itself, with a very discreet label; the exam stays as the measure of how often such
   an answer is wrong, written into the repository every night and shown on the page below. His goal: 1 wrong in 1,000.
5. **Photos**: the system may find candidate photos (Wikimedia Commons; public domain, CC0 or CC BY only). It publishes one
   by itself only when it comes from an official source whose own caption names the exact form; every other candidate waits
   for one tap from the senior author.
6. **One page lists everything the system wrote and published** (20:58: "we should just be able to access everything that
   was automatically written and deployed to check whenever we want"): each answer, its sources, the day, and whether a
   person has checked it since; one tap takes an answer down.
7. **An answer that is not complete says so, discreetly, and the papers the system still wants for it are listed** for the
   senior author (20:58), in APA 7, as the to-do page lists papers today.
8. **More than one source wherever more are relevant, and the same steps as the checked lane** (21:07: "the algorithm has
   to mimick completely how claude writes answers"): a reader per paper writes a study card; a writer writes the claim from
   the cards; a second reader who wrote none of it checks every passage at the source; the plain lines are checked blind.
   The steps are the protocol's own and can be run by any model. How well they are done depends on the model that runs
   them: with free models the writing and the checking are weaker than Claude's, which is what the label, the page of
   decision 6 and the nightly measure are for.

9. **Official bodies are sources too** (22:24, 22:31). The list is `data/auto/official/sources.json`: health services, health
   ministries and agencies, UN and EU bodies (tier 1), and information services a government pays for (tier 2). The system
   reads a body's pages only where that site's own robots.txt allows a reader that is not a browser, slowly, under the
   site's name; a refusal is never gone around (`scripts/auto/official.py`). A page's reference is made by code from the
   page itself, in APA 7 (a "last reviewed" date is not a date of publication: such a page is n.d. with the day it was
   read). An answer names the body in its text ("The NHS says"), so a reader always knows whose statement it is. Pages of
   law-enforcement bodies are not health sources and are not on the list. English first.
10. **The summary of a paywalled paper may be read** (22:40): it is free to read, the answer says that the paper was read in
   summary only, stays "not complete", and the paper stays on the list of papers wanted. Nothing goes around a paywall or
   a site that refuses: no Sci-Hub, no sign-in, no cache, no mirror. A page that refuses the system can be opened by the
   senior author and sent, as a PDF is.
11. **Amounts** (his decisions of 22:40 and 22:46; before them no machine-written answer could hold an amount, and the
   editor's first rule was that such an answer waits for him). An answer to a question about amounts is published by the
   system when every amount in it is stated by an official page or by a study in people. It gives each amount in its
   source's own words (at most 15 words), with who received it and under what care, and its reference; it is never a
   recommendation and never says how to take a drug, how to make an effect stronger, or which way of taking is stronger.
   Written by code, not by a model, on every such answer: "Amounts reported by studies and official pages, in their own
   words. Not a recommendation." For opioids, first: "These amounts were for people whose bodies were already used to
   opioids, under medical care. The same amount can kill a person who is not used to them." For GHB and GBL, first: "With
   GHB and GBL, the gap between an amount that has an effect and an amount that stops breathing is small. Amounts from
   medical treatment were reached step by step, under care." (He was shown the three lines at 22:46 and may change them.)
   What stays with a person, by the editor's rule: a question that asks which amount kills (the rule for questions about
   dying), and amounts for pregnancy or children. Answers to other questions still hold no amounts. The quiz is unchanged.
   *What the editor's reading of the first real batches added (17 November 2026; lanes 11 and 12, each rule with a test
   in `scripts/auto/lane.py`).* None of it changes what may be shown; it makes the rows exact. Who an amount is for: a
   sentence that states one amount for women and another for men gives a row for each, and each row carries the one
   sex its own part names; an amount is never shown under the other's name; the words that lead into a part ("For
   women, ...") belong to that part. What an amount is called: "low-risk", "safe", "recommended", "a limit" stand in
   a row only where the passage, its heading or the page's title says so; where the system's reader borrowed such a
   word from the question, the code writes what the shown words say and no more ("an amount for a week"). Never
   shown: an amount for each kilogram of body weight, however it is written, and a part that stops just before
   "per". A table is read row by row, and a bare cell ("400 mg") is widened to its row where it stands in one place
   only. The same amount for the same people twice from one source is one row. Abbreviations in who received it are
   written out as the source itself writes them out (or from ten that have one meaning in this field). Up to six
   official pages are read; the second reader is asked about the 20 amounts nearest the question. The record keeps
   every amount the second reader refused, with its reason, and every amount its room did not hold.
12. **The second look** (22:54, 22:55). Its own answers: the system goes back to them. When new papers, summaries or
   official pages can be read for a question, when a source is retracted, or when an answer is "not complete", the answer
   is written again towards being complete, or taken down; what it was before is kept in the record. The checked answers:
   the system criticises, it does not edit. Where it finds research that conflicts with a checked claim it writes the
   conflict down with the sentences on both sides and a proposed change; a checked claim changes only through the checks
   of the checked lane (the editor's decision: an unseen edit by a free model would undo what "checked" means).
13. **What the page promises a reader who sends a question** (22:24): "Our system starts on it within half an hour. If it
   finds research it can read, the answer is usually here within the hour: your question then turns green under “Your
   questions” on the start page." A page says this only once the half-hourly run is on and has been seen to keep it
   (`data/auto/lane/policy.json`, `loop`); until then it says the plain truth ("Sent. We will check it …"). Every kept
   question is asked again at every publishing (each has a stamp of its own, `data/build.json`), and an open page that
   holds a waiting question learns of a newer site and offers to load it.
14. **"At least part of an answer"** (22:31: "like 999/1000 times"). Measured, not promised: how often a real question
   leaves a visitor with nothing is counted on the questions on file before and after each change
   (`scripts/insight/build_index.py --eval`), and the number is written here.

15. **The system decides where new information belongs, and starts the pages that are missing** (16 November 2026,
    13:52, his words: "this way it could also start adding information about other drugs too and make other drug
    categories or taxinomize where the new information belongs, in which drug page, or if it belongs in the statistics
    page, the test kit page, the emergency number, the general drug facts page all the pages that already exist and the
    new pages it understands it should develop"). Built the same hour, as code without a model
    (`scripts/auto/place.py`): every question and answer gets a home (a drug's page; a page to start; mixing;
    statistics; drug checking; law; big questions about drugs) and the other pages that list it. The editor filed each
    of the 272 names the site knew as drug words on a page that exists or on one of 54 pages to start, each under one of
    the site's classes or a new category (`data/auto/filing.json`); a research chemical is filed by the shape of its
    name. `data/auto/pages.json` ranks the pages to start by the questions that ask about them: demand first, a page is
    started because people ask. The editor's limits: the emergency page stays the senior author's own, so the system
    never writes there (a question about an overdose lives on the drug's page, waits for a person and points to that
    page); a number on the statistics page keeps the source rules of METHODS §10; a page the system starts shows a class
    only in a source's own words, and until a person has confirmed the class of a new drug, an answer about its amounts
    waits (the fixed line for opioids depends on the class). Measured on 447 real questions: 325 on a drug's page, 67
    general, 27 on a page to start, 18 mixing, 8 drug checking, 2 statistics; of 60 drawn at random the editor judged
    57 placed right, and the three kinds of miss have a rule now. Not built: the site showing an answer on its home page
    when that is not a drug's page, and the pages the system starts.
16. **A second free model service** (13:53, of the editor's offer of a free Groq key: "let's do whatever is optimal";
    14:05: he will add the key a little later). Looked up the same hour: GitHub's own free models, which would have
    needed no key, were retired on 30 July 2026 (docs.github.com); Groq's free plan, by its own page, still gives
    gpt-oss-120b, gpt-oss-20b and qwen3.8-27b 200,000 tokens a day each. So Groq it is. The lane is ready for the key
    (`team()` in `scripts/auto/lane.py`, `data/auto/lane/models.json`): team A lets the better writer of the trial write
    (gpt-oss-120b at Groq) with a second reader of another family; team B is the pair of lanes 4 to 6 with its second
    reader at Groq; the reader moves to Groq when Cloudflare's day is used up. Which team stands first is decided by
    the exam, which Groq's free tokens can pay for.
17. **"It should work as well as Fable 5.2"** (13:55: "we should make an algorithm so as to make our ai understand how
    to detect what it needs to give answers for questions and how to write these questions perfectly. it should work as
    well as fable 5.2. we can do it"; 13:56: "don't stop until it's finished ... have to be as perfect as absolutely
    possible i don't want limitations"). What the editor holds to: the free models are weaker readers and writers than
    the editor, and no rule makes them equal; what rules can do is make sure that what is shown is right and plain, by
    doing in small steps what the editor does in one, and by measuring against the editor's own reading. The steps, in
    order: (a) a plan before the search: what a question needs answered (for "can you get addicted to ketamine?":
    whether it happens, how often, tolerance, withdrawal, for whom), so that the search, the reading and the writing
    are held to it and the answer is complete when each need is met; (b) the editor's own worked answers as the
    writer's examples; (c) each real batch read by the editor, every fault a rule with a test (lanes 4 to 6 were made so);
    (d) the system's sentences compared with the checked claims of the same page before they are shown; (e) the exam
    for every second reader. The measure the senior author is given: of the sentences shown, how many the editor would
    not have written.

18. **YouTube as a place to learn what people ask** (16 November 2026, 18:56, his words: "also our site could see all drug
    questions and drug themed videos on youtube to get every idea possible! it's an open platform right?" and "or we
    can get access to it through a third site maybe"). Not built, and the editor's answer was no, from YouTube's own
    rules as read that hour (developers.google.com/youtube/terms/developer-policies): YouTube may not be scraped
    "directly or indirectly", so a third site is the same thing and a refusal is never gone around; the official free
    door (the YouTube Data API: 100 searches and 10,000 other units a day) forbids keeping what it returns for more
    than 30 days and using it "to create new or derived data or metrics", which is what a list of questions made from
    titles and comments would be, and it would oblige the site to carry YouTube's terms. What stays open: the senior
    author, as a person, may watch and read anything and paste titles and questions he sees (as with the Reddit pages),
    and the editor lists them the same day; and an open count the system may read by itself, with no key: Wikipedia's
    public page views (which drug articles people read most), to rank the pages to start. That is next after the
    batch of 17 November.

19. **How often people look a drug up** (16 November 2026; the open count named in decision 18). `scripts/auto/wiki_views.py`
    asks two public services of the Wikimedia Foundation (the article a title leads to; that article's views by
    people over the last twelve full months; the counts are CC0) for the titles `data/auto/filing.json` lists under
    "wiki", and writes `data/auto/demand-wiki.json`. Nothing of an article is read. It is used for one thing: the
    order of the pages to start among those our own evidence does not tell apart (`place.py --pages`). For nutmeg the
    article about its active substance is counted, not the spice's.
20. **The system asks by itself** (16 November 2026, 19:04: "site to think and expand"; 13:52: "the new pages it
    understands it should develop"). `scripts/auto/grow.py` lists questions without a model: the questions people ask
    about every drug (`data/auto/grow.json`: each from a ranked theme of `data/verification/demand-themes.md`, in
    people's words, with six true rewordings), for the pages the system should start and for the pages the site has
    where no answer is near. Demand first holds: no question exists because a paper does; themes that wait for a
    person have no template. Never twice, six a run, none while twelve of its own wait (`data/auto/grown.json`). A
    question about a drug without a page carries the page and the names papers use, and both finders search by them.
    Listing a question publishes nothing.
21. **"As Fable 5.2 would generate answers"** (16 November 2026, 21:11; and 13:55, decision 17). What was measured that
    evening (the exam, `data/auto/exam/`): the free second reader, asked with the right effort, catches about half of
    the small faults a careful reader catches; rules in code add a little; asked piece by piece it stops everything.
    The editor's answer: the route stays rules and measurement, and the step that is left is a stronger model that
    checks (and writes), free ones first (Mistral's free mode, Google's free tier, OpenRouter's free models: three
    keys asked of the senior author), then, if he chooses to pay, a top model through its API (prices read that hour
    and given to him). Every candidate sits the exam before it writes or checks anything. Open until he answers.
22. **The pages the system starts are shown as such** (site 2.8.0). An answer whose home is a page to start stands on
    that page, at an address of its own, listed under "All drugs" apart from the 30 checked pages and on "Written by
    our system". The page's first line says that our system started it and that a person has not checked it. A class
    is not shown on such a page (a class is a person's judgment, or a source's own words; neither is there yet). The
    emergency page is never written by the system.

23. **Our own models** (16 November 2026, 22:04: "this is why i wanted us to make our own ai. can we make the algorithm
    to read and write and that can be automated? ... if we can make our own ai we should that's what i was trying to do
    from the beginning, our own autonomous self expanding ai"; 22:15, of the editor's three steps: "make this perfect
    and finalized i want us to start this and it to work with no errors and outmost smartness"). He chose this over a
    paid key for an outside model. What it is: small models of our own for the steps where correctness is decided, run
    on GitHub's machines with no key and no service, like the search model (Pharmakon Insight).
    1. *A checker* ("does this passage support this sentence?"): first the open models made for that question sit the
       whole exam (`scripts/auto/nli.py`: MiniCheck, LettuceDetect); the best joins the lane as a second judge that
       must also accept every sentence; then it is trained on our own checked record (the cards our blind checkers
       passed, stopped and corrected; the editor's readings of the lane's own sentences; made-up wrong sentences of the
       kinds we have seen).
    2. *A reader* (which sentences of a source answer the question, word for word), measured and trained on our own
       claims and the passages they rest on.
    3. *A writer* (a source's sentences into our plain style), trained on our checked answers and on drafts of the free
       models that our own checker accepted; until it is good enough the free open models write.
    The rule that holds for every one of them, in code: a model replaces the one in use only if it does better on the
    exam (fewer wrong sentences let through, no more good ones stopped), and every trial's numbers are kept in the
    repository. What the editor told him is not possible: a model built from nothing that writes as the editor does;
    and "no errors" is not promised by anyone: the error rate is measured, shown and pushed down. Things fetched from
    outside (open models, their packages) run only in a job that may read the repository and holds no key
    (`.github/workflows/own.yml`, "Workshop": the job `make` reads and runs, the job `keep` writes and runs nothing from
    outside).
    How it is built (16 November 2026): a model of our own is a file of numbers (ONNX, 8-bit weights) with its
    tokenizer's table, kept among this repository's release files (`own-models`) and named with its SHA-256 and its
    numbers on the exams in `data/auto/own/candidates/`; the lane refuses a file whose SHA-256 is not the one written
    down (`scripts/auto/own.py`). A candidate is made in the workshop (`scripts/auto/workshop.py`), sits the exams as
    that very file with the lane's own code, and becomes the model in use (`data/auto/own/models.json`) only through
    `own.py adopt`, by the rule above. In the lane it is one more judge: every sentence a model wrote must score at
    least the candidate's threshold against the words it rests on (`lane.own_word`; a How line that fails is dropped,
    a short answer or a But is written again). If the model in use cannot be run, the lane publishes nothing by itself.
    Step one, measured the same evening (`data/auto/exam/nli-*.json`): the open models as they are tell a faulty
    sentence from a good one poorly (MiniCheck on RoBERTa: 65 times in 100, where 50 is chance; on Flan-T5, on the part
    it sat: 72). Where such a model earns a place is at a very low threshold: at 0.05 MiniCheck on RoBERTa caught 3 of
    the 22 faulty sentences and stopped 4 of 742 good ones; at 0.5 it caught 5 and stopped 78. So our own checker gets a
    small budget (it may stop one good card in twelve at most), because it is one judge of several and what each judge
    wrongly stops adds up. The gain has to come from step two, the training on our own record.
24. **Only free models, and two more free services** (16 November 2026, 22:34, with the keys he made from the
    editor's prompt: "Keys done: MISTRAL no, GEMINI yes, OPENROUTER yes ... Important: Pharmakon must use only free API
    models, with no billing, paid subscriptions, credit purchases or unexpected charges"). In code, not in a setting:
    at OpenRouter a model whose name does not end in ":free" is never asked, whatever a file names
    (`llm.never_paid`); a model of Google's whose free allowance is not written in `data/auto/lane/free-limits.json` is
    never asked; the paid interface in the client (`claude:`) has no key and no price file. What he read on Google AI
    Studio's own page is in that file, model by model: the two Gemma 4 models 30 calls a minute and 14,400 a day each;
    Gemini 3.1 and 3.5 Flash Lite 15 and 500; the other Flash models and Gemini 4 Hydrogen 5 and 20. We stop at nine
    tenths of a day's calls; Google's refusals for a minute are waited out, and its word that a day is used up is
    believed. OpenRouter's free models share about 50 calls a day (we stop at 45). Mistral gives no free access to its
    interface now: not used. What may be sent to these services is what may be sent to Groq: our own wording of a
    question and passages of public sources, never a visitor's words. Google's terms for the free tier (read on 16
    November 2026) say that paid services must be used "when making API Clients available to users" in the European
    Economic Area, Switzerland or the United Kingdom. The editor's reading, which is not a lawyer's: the lane is a
    program the senior author runs for himself; no visitor of the site ever reaches Google's interface, and what the
    lane sends is public text. He was told this in plain words and can end the use of Google's models with one word.
    Nothing of these services is used by the lane until a model has sat the exams.
25. **Three exams, and a panel of judges** (16 November 2026; decisions 17, 21 and 23). No single judge we have is good
    enough, so they are measured, alone and together, on our own checked work, and a sentence is kept only if every
    judge of the team accepts it.
    - *The cards* (`data/auto/exam/cards.json`, since 15 November): 318 quiz cards beside the lines they were written
      from, 31 of them wrong by a blind checker's word. `cards-where.json` (the editor, from each checker's words):
      in 21 of the 31 the fault sits in a sentence of the card's true part; in 10 it does not (a myth's own statement,
      the card as a whole, or a sentence that stands word for word in the lines), and a reader of sentences cannot see
      it.
    - *The lane's own sentences* (`lane-sentences.json`; `scripts/editor/label_auto.py`): every sentence the system
      wrote that the editor has read against the words it rests on, by the blind checkers' standard. 29 so far: 20
      good, 9 not (lanes 1 to 8: 9 of 25; lane 9: 0 of 4). It grows with every batch the editor reads; a verdict is
      never changed silently, and a rewritten sentence is a new item.
    - *Plain lines* (`lines.json`; `scripts/auto/exam_lines.py`; `labels-lines.json`): 488 plain lines beside the
      checked claims they were written from, with the blind checkers' verdicts: 432 good, and 56 that a checker changed
      because they said something the claim does not carry (the editor sorted every changed line from the checker's
      reason; 33 changed for form only are left out). This is the lane's own kind of task: a technical source, a plain
      line.
    The judges: the rules in code; the open models at the free services, each asked the lane's own question
    (`scripts/auto/exam_models.py`, `"exam": "cards" | "lane" | "lines" | "both" | "all"`); our own models. What every
    panel of them would have done on the items all its judges saw is counted from the results on file, with no model
    asked (`scripts/auto/panel.py`). A team may name further second readers (`"also"` in
    `data/auto/lane/models.json`): each is another model than the writer and than the second reader, needs a key and
    room, and its word counts like the second reader's; a team that names them is that team only with all of them.
    What the lane's own sentences asked of the rules in code the same evening: "causes" had stopped two good sentences
    and caught nothing (it now knows more of the ways a source says that one thing brings another); a ceiling said as
    the size ("by as much as 2 to 5 times" written as "2 to 5 times") is a kind of its own; "statistically
    significant" is a term; a denied word of sureness claims less. On the plain lines the rules catch 1 of 56: with a
    long source nearly every word is carried somewhere, so there the judges must be readers.
    *17 November 2026.* What the lane does NOT keep is on file from lane 11 on: every draft that was written again
    (each sentence with who refused it and why), every line that was dropped, every amount that was refused. The
    editor judges those sentences for the exam as well, so the exam can say two things about the lane as a whole
    (`python3 -I scripts/editor/label_auto.py rate`): of the sentences a lane KEPT, how many are not good (what a
    reader would have been shown wrong before the editor's reading: lane 10, 1 of 5), and of the ones it did not keep,
    how many were good (what it lost). A reader whose free plan gives 20 calls a day sits the lane's exam an answer
    at a time, in the lane's own call (`"how": ["together"]`: about seven calls for 34 sentences). Our own checker is
    asked in the lane with the passage around each quote; the exam keeps no passage (no page's text is kept), so the
    record now holds its score against the quotes alone as well, and the two are compared on real answers.
    A fourth exam, of ROWS: every row of an answer about amounts that the editor has read, with a verdict
    (`data/auto/exam/lane-rows.json`; `scripts/editor/label_rows.py`, which can read the records as they stood at a
    commit). After the night of 17 November: 90 rows, 9 not good; by lane 10 to 14: 2 of 19, 0 of 19, 5 of 28, 2 of
    14, 0 of 10. Lane 11 read clean and lane 12 did not on the same three questions, because the reader copies
    differently each time: a clean batch on questions the rules were mended on proves little, and the switch for
    publishing answers about amounts by themselves waits for a clean batch of questions the lane has never seen.
    For that the lane has a trial (lane 15): a request may hold questions that are NOT on the site's list
    (`"trial": [{"id": "t_...", "q": "...", "drugs": ["lsd"]}]` in a `lane-*.json`); the lane finds, reads, writes and
    checks them like any other, and what it makes is written to `data/auto/trial/` and can never be shown, placed or
    counted as an answer. The editor reads those records like the others (`read_auto.py --trial`,
    `label_rows.py --trial`), and their rows go into the exam of rows.
    - *Lane 16* (17 November 2026, after the editor read what lane 15 wrote for the senior author's own two questions; 22
      sentences judged, 18 good, 4 not good). Three faults, each with its rule and test. (1) The second reader refused
      the opening word "It depends." as "not stated in any passage"; the writer then left the word out and broke the
      rule that asks for it: no answer, and a good draft lost. The opening word is now taken out of the sentence the
      readers set beside the passages (`opener_of`) and judged apart, as the answer to the question (the checker's
      "opening"). (2) "A 2026 review found ... long-term use and testicular tumors": the review only cites an earlier
      meta-analysis for that, and the second reader accepted it twice. `second_hand()` reads from the passage whether a
      finding is reported from another study ("A meta-analysis in 2019 ... found", "According to a study", "However,
      ..." after such a sentence); the writer is told, and a sentence that says its source found such a thing breaks a
      rule. (3) "wax and flower forms linked to higher satisfaction": true to its source, and a comparison of the forms
      of a drug for a wanted effect, which the site keeps for the section the senior author approves; a rule stops it.
      Also: where a team names several models for one further reader and the first cannot be asked (its day's free
      calls used up), the next is asked in the same answer instead of leaving the answer to wait.

26. **The page reads a question in more ways, and the aim is one error in a thousand** (17 November 2026, 10:39 to
    11:11, his words: "it should understand and correctly diagnoze every instance and meaning of human language"; of
    "We have no answer to this. Pharmakon answers questions about drugs" under his unfinished "can i die from " and
    under "can a gay man go to the court": "this is pathetic it has to have 1/1000 error rate"; "ignore some questions
    as irrelevant to drugs at a 1000 to 1 accuracy rate"; "if a user makes a question about a different drug our ai
    should create that drug page"; "i want us to invlolve everything human language can consist of taken from every
    instance of how people actually write on the internet"; and of his two sent questions: "i cannot click on them to
    see the answer").
    - *What site 2.9.0 does* (words only, the same on the page and in the build; `site/insight/scope.json`,
      "unfinished"; `insUnfinished`, `Ranker.unfinished`). A question is read as **not finished** when its last word
      cannot end a question ("can i die from"), when a drug is named and only function words are said of it ("is
      cocaine"), when no drug is named and every word could be asked of any drug ("is it addictive", off a drug's
      page), or when its last word is the beginning of a drug's name or of a known word ("can i die from coc"). It gets
      no verdict and no way to send it: "Which drug do you mean? Finish your question with its name and we will look."
      or "Go on. Finish your question about cocaine and we will look.", and what was found stands under "You may mean"
      (never as a best match). `scripts/auto/ask.py` never lists such a question. A question that is **not about
      drugs** by its words is told what the page read: "This does not look like a question about drugs. ... If yours is
      about one, name the drug, or send it to us."; where one word the model does not know stands among words that
      could be asked of any drug ("is tusi dangerous"): "We do not know “tusi” as a drug. If it is one, send us your
      question and we will look into it." Both keep the way to send, because the rule reads words and a drug question
      in everyday words must not be lost ("no false negatives"). In "Your questions" a question that waits can be
      opened (it is asked again in the box), and a sent question that is now on our list says so.
    - *Measured* (`python3 -I scripts/insight/build_index.py --words`, no model needed; on the questions the lists
      were written with, so this is not a fresh measure): of 1,021 real forum questions none is called unfinished; of
      165 questions about other things, 1 ("why is this not working"); of forum questions cut after a word that cannot
      end a question, 1,119 of 1,176 are caught (the others are finished: "What is tramadol like"); cut just before
      the drug's name, 276 of 399 (the rest end on a word of content: "Is smoking or snorting"); cut in the middle of
      the name, 331 of 474. `scripts/insight/parity.js` holds the page to the build on 1,325 cut questions.
    - *What "one in a thousand" asks, and where we are.* The scope rule (is it about drugs?) took 94 in 100 fresh
      forum questions before their misses were added and none of 165 questions about other things. To say "at most 1
      wrong in 1,000" for a class needs about 3,000 fresh questions of that class with no error. So the number is
      measured and stated, never promised, and the firm line ("This is not a question about drugs", with no way to
      send) waits for it.
    - *The plan, in this order.* (a) A large open table of drug and medicine names with their other names (open data,
      fetched on GitHub's machines), so that an unknown name is recognised and gets its page to start (decision 15).
      (b) Misspelt names read as the drug they mean, where the word is not a word of its own and stands one letter from
      a name. (c) Real language in bulk: open collections of what people actually typed (search questions, forum
      questions), only where a licence allows it, fetched in the job that holds no key; never a visitor's words. A
      small reader trained on them for the page (about drugs or not, finished or not, which drug), on top of the model,
      with the words rule kept as a second check. (d) Fresh test sets of thousands of real questions for each class,
      and the measured error rate written here. "Every instance" of how people write cannot be had; millions of real
      examples and a measured error rate can.
    - *What stays as it is.* Free models only; a visitor's words are never shown on the site as typed (the list is in
      our own words) and go to no model service but Cloudflare's; the system starts pages and writes, rewrites and
      takes down its own answers, and never edits a checked claim.
    - *An open point, put to the senior author on 17 November 2026.* The scout keeps the questions people sent, cleaned
      of links, addresses and long numbers, in its working files (`data/auto/questions.json`, `data/auto/report.json`,
      `docs/MISSING.md`), and this repository is public. So far those files hold two questions, both his own tests. The
      privacy text says what is sent and kept, not that the kept words can be read in a public repository. Either the
      text says so, or the words stay in the store alone and the repository keeps our wording, the counts and a
      fingerprint. Not changed until he decides.

27. **Insight answers from every section, and every circumstance has its response** (17 November 2026, 12:56 to
    13:45. The senior author typed "do gay people", was told "This does not look like a question about drugs", sent it,
    and wrote: "we have to include our site responding perfectly to every circumstance this is what smartness is
    about". Then: "are drugs legal in greece" got "We haven't checked exactly this yet" while the site has the answer
    on its page of treaties: "pharmakon insight has to incorporate all information from the website from all
    sections"; "it should be apparent that the best way to use the website is Pharmakon Insight"; of "what is mytragina
    javanica": "hardcode is not enough our ai has to correct and update itself with all possible relevant online
    searches"; "i want the site to work perfectly without us"; "our search engine has to feel like a drug".)
    - *Site 2.9.2.* (1) Two more ways a question is not finished, by grammar and not by topic
      (`site/insight/scope.json`, "unfinished"): **open**, nothing but function words and words for people ("do gay
      people", "why do women"); **verb**, a helper verb and no main verb after it ("does smoking weed", "how long does
      the high", "can dogs"). Both are told "Go on. Finish your question and we will look." and have nothing to send;
      "Which drug do you mean?" is kept for a question that calls for a drug ("is it addictive", "can i die from").
      (2) The short forms people type are read as their words ("u", "ppl", "wat", "gonna"). (3) A name of two or three
      words that we do not know is named ("We do not know “mytragina javanica” as a drug"), not called "not about
      drugs". (4) **Routes to the site's other sections, by country**: the law ("are drugs legal in greece" opens
      Greece on the page of treaties and says what it has joined; "is weed legal in greece" opens cannabis' law part
      for Greece, without changing the reader's own country), the emergency numbers ("In Greece, call 112"), drug
      checking ("3 drug checking services in Spain"). A question of the law that the law part does not answer by itself
      keeps the line and the way to send it. (5) A question that is not in the Latin alphabet is asked for in English
      (and in Greek, for Greek). (6) An entry of one or two words that is a beginning ("can i") is told to go on, in
      place of "No match … Ask us". (7) A question already sent says so when opened again; a beginning that was sent
      is listed as "Not a whole question"; the list of the reader's questions shows the newest first.
    - *Measured* (`python3 -I scripts/insight/build_index.py --words`). The two new readings call none of the 1,021
      forum questions unfinished, none of the 165 questions about other things, and none of **2,324 question sentences
      the rules were not written with** (the first fresh measure of step d). On those 2,324 the older readings erred
      before this version (32 called unfinished) and were corrected with what the fresh set showed (stranded endings:
      "what do you use it for", "…looked down on", "…kick in", "tried this before"); 18 are still called unfinished, 13
      of them the site's own questions that are asked on a drug's page ("How do people take it?": off the page "which
      drug?" is the right reading). Questions cut as a reader who is still typing leaves them: before the name 292 of
      399 (2.9.1: 276), inside the name 350 of 474 (331), after a word that cannot end a question 1,115 of 1,176
      (1,119; four that end "…days after" now read as finished). The page and the build read 1,370 cut questions the
      same way (`scripts/insight/parity.js`). Not yet a fresh measure of the new readings' misses: fragments are made
      by cutting, and a cut is not always a fragment.
    - *What he asked for next, in this order* (`scripts/editor/next-steps.md`). (a) **Names the system does not
      know**: looked up in open name services that allow it (species, medicines, chemicals), on GitHub's machines in
      the job that holds no key, and kept in a table the build reads, so that "mytragina javanica" becomes *Mitragyna
      javanica* without a list written by hand. (b) **Pages for drugs without one** (kanna, *Mitragyna javanica*):
      the system's pages of decision 22, in the form of the site's own pages, with pictures only under an open licence
      and a line where a picture was not checked by a person; pictures also where an existing page lacks them. (c)
      **One list on phone and desktop without an account**: a private link or QR code, the list encrypted on the
      device so that the store holds what it cannot read; "as easy as it is now". (d) **Insight looks like what it is**:
      the way to use the site, not a search box. (e) **What the site needs, found by itself** ("it has to think about
      what the site needs objectively even before us").
    - *Step a, built (site 2.9.3, 17 November).* What the probe found (`data/auto/names/probe.json`): GBIF's species
      matcher, RxNorm's approximate match and PubChem's name completion allow programs and answer ("Mytragina javanica"
      came back as *Mitragyna javanica*, a plant; "xanex" as Xanax; "mesembrin" as Mesembrine). NCBI's spelling
      suggestion, Wikipedia's search, Wikimedia Commons' search, iNaturalist's and Openverse's addresses are not allowed
      by their robots.txt and were not asked. GBIF's records with pictures are allowed (for step b). The lookup
      (`scripts/auto/names_open.py`, learn) runs in the half-hourly run after the scout: only the unknown word or words
      of a sent question go out (`build_index.stranger`; from a file of the run, never the repository, never the
      question); two words go to GBIF (plants and fungi), one word to RxNorm and then PubChem; an answer is taken only
      when it is the typed words with a letter or two wrong. A species or a chemical counts as a drug when Europe PMC
      holds two papers or more that name it with a word of drug use, a medicine when RxNorm puts it in the nervous
      system group. `data/auto/names/learned.json` keeps the name, its kind, the service's record and what was typed
      for it; a word that led nowhere is kept only as a mark made from it. The build reads the table: a learned drug's
      name is the name of a drug the site does not cover yet, and what was typed for it is read as the name on the page
      and in the run alike ("We read “mytragina javanica” as Mitragyna javanica"); a question set aside as not about
      drugs is looked at again once its name is known (`scripts/auto/ask.py`), and a new name is a reason to publish
      (`scripts/auto/tick.py`). The privacy text says so. Not measured yet on real traffic: how often a service's answer
      is wrong although it is close; every learned name is in the table to be read by the editor.
    - *Step b, built (site 2.12.0, protocol 0.5.4, 17 November).* **Pages people asked about are shown before there is
      an answer, in the form of a drug's page.** A page the system should start (`data/auto/pages.json`) is shown as soon
      as a listed question belongs to it: six on this day (kanna and *Mitragyna javanica*, which he asked about;
      nootropics and supplements, anabolic steroids, NBOMes and ketamine analogues, from the forums' questions and the
      system's own). The page (`site/src/app.insight.js`, autoPageHtml; `#auto/p-kanna`, its parts
      `#auto/p-kanna/part-p-looks`) has a drug page's header and a drug page's menu of parts: what it looks like, what
      people ask (each listed question in our words, "Not answered yet", "Tell me when it is answered"), and what our
      system wrote. Its first line: "People asked about kanna, and the site had no page. Our system started this one by
      itself. It has not written an answer yet. A person has not checked this page." It shows no class; for a plant or a
      fungus, the species' name and the word "Plant" or "Fungus", where GBIF matches the name exactly. **Pictures**
      (`scripts/auto/pictures.py`, in the job that holds no key): from GBIF's records of what people saw, only CC0 and
      CC BY, each with its maker, licence and record (49 on file for 11 pages; 12 fetched, web copies in
      `site/photos-auto/`); under them: "Our system found these pictures by itself. They come from GBIF, an open record
      of plants and fungi that people saw and named. A person here has not checked them yet. A picture cannot tell you
      what you have."; each is also named among the site's photo credits. The editor looked at the twelve
      (`looked_by_editor`): kanna's three are shown; six are held with their reasons (a dead winter plant, one leaf on
      the ground, two plants in one picture, a pale cap that does not show the look people know) and a fetch was asked
      for in their place; three wait for their pages. The site's rules for photos stand for these pictures too
      (`docs/WRITING-RULES.md`, his words of 18 October: never people or hands, the thing itself as people meet it,
      nothing else that takes the eye), and no program can judge that yet: so a fetched picture is shown only after the
      editor has looked at it, and carries the line he asked for ("if the pictures have not been verified … a small
      disclaimer") until a person has. A judge of pictures that is measured first is what would let this run without
      the editor.
      **Insight**: a question that names such a drug is shown the way to its page first ("can i get high with kanna":
      "A page our system started · Kanna: pictures and what people ask"), keeps "We haven't checked exactly this yet"
      and the way to send it, and is no longer shown answers about other drugs that the word search found by a stray
      word; the very question a page lists is told "Not answered yet. A question like yours is on our list"; "what
      does kanna look like" goes to the pictures; the name alone finds the page, also with a letter wrong. The
      half-hourly run publishes when the pages, their listed questions or the pictures change (`scripts/auto/tick.py`).
      Checks: auto 96, insight 157, site24 108 (a started page is walked through like every page), parity, smoke 9;
      they go by whatever pages the build shows that day. *Not built*: pictures of other forms (the dried plant, a
      powder, capsules: GBIF holds the living plant, and the other open picture stores do not allow a program);
      pictures for pages that are not a plant or a fungus; a judge of what a picture shows (today the editor looks);
      a question on a started page's list found by meaning (today only by the same words: the system's own list is
      not in the page's index of listed questions; to be measured first); a question asked on a started page read as
      a question about that page.
    - *What stays.* Free models only. A refusal by a site is never gone around. The Section 7 gate and the rule on
      amounts stand as written. Nothing new that the lane writes is shown until it reads clean (`hold_new`); a started
      page's questions and pictures are shown by their own rules, each with its line.
28. **Places by meaning, figures by question, the lane running again, and a school for the system's language**
    (17 November 2026, 16:33 to 17:26 Athens). His words: "our ai system has to always improve how it understands human
    language by learning from the language people use online and from the language people use in our website. it has to
    always improve by itself"; "it should not depend on us to get better"; "like the best apis in the world". Of "how
    can i use test kits at home", which got "We haven't checked exactly this yet" above a list of rows: "i think i should
    be answered and be given links etc and i think we already have info about that on the website. man we have to
    incorporate every instance of human language it is still stupid". With a picture of Chrome offering his saved
    addresses over the box: "i don't want any browser specific recommended choices only what the site recommends". Of the
    rows under "How many people die from methamphetamine": "completely irrelevant ... this creates visual clutter". Of
    "How many people die from heroin": "it should be much easier to find what I want this is so confusing I read so many
    things I don't want to read"; the Statistics page it sent him to showed "irrelevant" figures; "this is such a simple
    question ... our site is very lacking". Of his own sent questions still waiting: "why aren't they being automaatically
    answered? this should be done as fast and good as possible"; "the site should be as full as it gets as soon as possible
    it has not got answers for very basic questions it should develop so much".
    - *A place of the site is found by the meaning of a question* (site 2.13.0). The routes were patterns of words:
      "how can i use test kits at home" matched none. Now every place of the site (28 of them; `site/insight/places.json`)
      is described by questions it truly holds something on (344 ways), each read by the same small model that reads a
      visitor's question, on the visitor's device. Near enough (0.80), the place is the answer; nearer than 0.66, it is
      offered as a place to look; a drug page's own part (test kits, the law, doses, looks, mixing) where one drug is
      named. Measured (`build_index.py --places`): of 89 questions written apart from the ways
      (`data/verification/insight/places-gold.json`) 79 are sent to the right place and none to a wrong one; of 1,021
      forum questions 43 are sent to a place and 85 held back; of 165 questions about other things, none. Rows found by
      words alone stay only when near in meaning (0.4), and the rest wait behind "More results (N)". The box says in
      every way a browser and a password manager read that it is a search box with its own list; this could not be
      tried here (a browser without a window has no saved addresses): his own look decides.
    - *A question that asks for a count is answered from the official figures* (site 2.14.0). "How many people die
      from heroin" now gets, first, the figures for that drug and that kind of count (deaths, treatment, use, disorder,
      harm) from the checked rows of the Statistics page, the lowest and the highest as one line with place and year, and
      the link opens the Statistics page on that drug and that kind. Only rows whose own label names the drug; deaths
      only where the row counts deaths.
    - *The lane.* It had been paused by the editor since 16 November; a question without an answer was tried again after
      a week; kanna and *Mitragyna javanica*, which have no page, were searched without their own names as a required
      word. All three changed at 15:59 UTC: the pause is lifted, a question is tried again the next day, a drug without a
      page is searched by its names (`papers.page_names`). "Does cannabis make sex better?" passed the models and waited
      for a further reader; the editor read it: it said as an effect what its sources report as people's own accounts, so
      it is held (`data/auto/held.json`). "Does cannabis cause cancer?" disagrees with a checked answer that is a Section
      7 answer and is not shown: it waits for his "approve". **What limits a day is the free allowance**: on 17 November
      14 questions could be tried, and by 16:15 UTC no team had room (Cloudflare 8,781 of 9,000 neurons, 6,770 of them
      the reader's; Groq's strongest model 178,071 of 200,000 tokens). The allowances are new at 00:00 UTC (Google's at
      08:00). Of 64 listed questions 46 had never been tried. So: team I, first in `data/auto/lane/models.json`, lets
      Google's free Gemini 3.5 Flash Lite read (500 calls a day), so that Cloudflare's day goes to the second reader; no
      gate changes (a reader only copies, and code checks every quote against its passage). Team K (Google's Gemma 4
      reads, plans and writes; the second reader stays) stands last and is to be tried by name. Read on the services'
      own pages the same evening: Cerebras gives its free trial "after adding a verified payment method": not used
      (decision 24); Mistral as before. The two small jobs of the half-hourly run (the look, the start of a publishing)
      ran on GitHub's small runner, which did not start twice within an hour (16:15 and 16:33 UTC; both runs were
      cancelled): they run on the usual runner now.
    - *The school: the design.* A daily run without any key (`scripts/auto/language.py`, in the Official
      workflow): it fetches open collections of questions people really typed (first: Natural Questions "open", the
      questions of Google Search users that Google published under CC BY-SA 3.0, 3,610 and 87,925 questions, from
      raw.githubusercontent.com, which has no robots.txt), asks the page's own reading of each (is it a whole question?),
      and counts how many finished questions per thousand it calls unfinished. What it may learn by itself, by evidence
      only: a verb it does not know (seen as a base form after "to" or a helper verb at least three times, and in at
      least two other forms), kept in `data/auto/language/learned.json` and read by the next build; nothing is kept
      unless the measure on the site's own sets (`measure_words`) is no worse. The same frame is to take the site's own
      questions next (a sent question that the site answered only after a second wording: the wording is learned, in our
      words), then spellings and street names. Each lesson: a source, a measure, a rule for what may be learned, a gate,
      a report. It needs no editor.
    - *The school: built the same evening, and its first two days* (`scripts/auto/language.py`; every day at 03:23 UTC in
      the Official workflow, which holds no key; `data/auto/language/`: `sources.json`, `learned.json`, `report.json`).
      It read 65,508 questions that people typed into Google (Natural Questions "open", CC BY-SA 3.0; the web client
      reads the first 6 MB of the large file) and let the page's own reader read each. **What it found was not what the
      design expected**: no finished question was called unfinished for want of a verb (one verb was learned: "snow");
      2,019 were called unfinished because they end on a word a question "cannot end on" ("how many super bowl games
      has the patriots played in"). So the same evening it got a third lesson, endings: two last words that end at
      least five different real questions which begin as a question does, the last a preposition. The pairs join the
      reader's own patterns as one pattern, the same string for the page and the build (`ending_pattern`). The measure
      now counts only what begins as a question does (57,973 of the 65,508): a search query that is a sentence to be
      completed ("the outer layer of the skin is the") is rightly called unfinished. **Second run: 19.9 of every
      thousand finished questions were called unfinished before, 13.4 after**; 31 endings learned ("stand for", "named
      after", "come from", "known as", "come on", "made of" ...); one refused by the gate ("made from": four cut-off
      drug questions of the site's own set would have passed as finished). On the site's own sets nothing moved (no
      whole forum question called unfinished; the cut-off ones caught as before). "what does thc stand for" and "how
      long until shrooms come on" are now read as finished; "can you die from" and "is it safe to mix weed with" are
      still read as unfinished. The questions visitors send (`data/auto/questions.json`) and the site's own question
      texts count as evidence beside the open collections; a visitor's question is only counted, never kept by this
      tool, never part of the measure. What it cannot learn yet, by its own report: 63 questions made only of everyday
      words that it takes for "which drug?" ("who has the most number one single hits"), 14 whose last word it takes
      for a word still being typed ("... on psych"), and the endings seen fewer than five times. Next lessons, in this
      order: everyday words with a letter wrong ("is ketmine adictive" finds nothing: only drug names are corrected
      now), the rest of the large file and further open collections (each needs its licence read first), the two
      smaller errors above.
29. **Simple first, the science one quiet tap away** (17 November 2026, 17:04 to 17:20 Athens). His words, of an
    answer's "Researchers disagree" box: "I think the users should get much faster answers to these with citations
    still but the answers for researchers should be very discreet and hidden our website should first be able to answer
    to every common simple human in a sense that makes the users it's easy and fast to understand the information";
    "the (Launiainen & Ojanperä, 2014) citation in the 'strongest evidence for no' has not a link to it every citation
    should have a link to it"; "when I click on the links of the in text citations I get lost because I can't find
    easily where I was before I shouldn't just scroll down I should continue being in the point where I was reading
    at"; of the list of sources: "the information that comes up is too research based and it's difficult for the casual
    user to find this interesting users should be able to find quick simple answers and only if they are crazy they
    should click to the scientific details"; "**This is how our website should be designed in general and what
    principles our ai should use**". Of a drug page's part: "I feel like all questions look the same and I don't want to
    read none this is an endless sea of questions ... find exactly what you want without reading so many words". Of
    Insight: "the search engine should be more apparent not only in the landing page but in all other pages of the
    website too, it should not just be a search engine"; "more consistent throughout the website"; "when you jump to
    another page because of a search while navigating it should be super easy to go back"; "the user should never feel
    lost and 'where am i' in the website".
    - *The principle, for every page and for everything the system writes* (also `docs/WRITING-RULES.md`, "Simple
      first"): (1) what a reader sees first answers the question in plain words, in a line or two, and says where it
      comes from; (2) the research (methods, numbers with their intervals, page numbers, quotations, references in full,
      the researchers' own arguments) is always there, one tap further, behind a quiet label, and never between a reader
      and the answer; (3) nothing opens somewhere else when it can open where the reader is, and a reader can always see
      where they are and how to go back; (4) a long list is led by its signposts (topics, counts), and each row shows only
      what tells it from the others; (5) the same thing looks and works the same on every page. Nothing checked is
      removed or reworded for this: only its place and its order change.
    - *Site 2.15.0, the evidence of an answer.* **Every citation is a link.** The text was escaped before it was read
      and the list in brackets was cut at every semicolon, also at the one that ends "&amp;": no citation of two authors
      in brackets was ever a link, on any answer. Now a reference is found in every form the checked texts use ("Hall &
      Degenhardt, 2009", "Hall and Degenhardt (2009)", "Zhao et al. 2023", "Poole et al. (2017, corrected in 2018)", the
      second year of "(Hughes & Stevens, 2010, 2012)", "Volkow 2014" where one source of the answer fits, "de la
      Torre" for "De La Torre"). Counted over the 2,768 texts the evidence shows for the 374 answers: 2,251 linked
      mentions before, 2,725 now; none of an answer's own sources is left unlinked in its canonical forms (a check now).
      Four mentions are left that code cannot decide (two works of the same authors and year named without their letter:
      "Hollander et al., 1995"; a relayed study; two whose anchors were removed): the editor's to settle in the text. A
      study we know only through another source ("Mittleman et al., 2001, as relayed by ...") has no reference of ours:
      the source that relays it is its link. A study card's own number in the researchers' text ("sc_...") opens that
      card. **A source opens where the reader is**: its card unfolds under the line being read, the line does not move,
      a second tap folds it away. **A source says in plain words** what it adds to this answer (the checked plain lines
      that rest on it) and what kind of study it is (twenty plain names for the study cards' designs), then "Open the
      paper"; the findings as recorded, with their places, the quotation, the APA reference and the study card are under
      "Scientific detail". **"Researchers disagree"** starts in plain words; the researchers' question and the five full
      texts are under one fold, "Both sides in full, for researchers". Where the two sides are written in plain words
      and blind-checked (`data/site/simple.json`, a claim's "sides": yes, no, read, and their sources), the box shows one
      line for each side with its sources and one for our reading: the place is ready, none is written yet (32 debates).
    - *Site 2.15.0, the pages.* **A closed answer is its question and the first line of its answer**, with the bars
      (their words are read aloud and shown when it opens): the cards of a part are half as tall. The topics of a part
      are its signposts, each with its count, and a part with eight answers or more and three topics or more starts with
      its topics in a row, each a jump to its answers. **Insight looks the same on every page**: the capsule of the
      start page, smaller, in the top bar, and it says so ("Ask Insight about cannabis"); before a word is typed it
      offers what people ask most about the drug whose page it is on. **The bar says where the reader is** ("Heroin ›
      Risks"). **The way back is always in reach**: at the top of a page it is the Back line, as before; once that line
      is out of sight the bar holds a Back button, named ("Back to Cannabis"). On a phone the bar's first row scrolls
      away and its second row stays: Insight and the way back, 58 px. The Menu button keeps its place.
    - *What a reader gave up.* A closed answer no longer shows its whole short answer: one tap opens it. This changes
      "redesign 2" of 13 November at his word.
    - *Not done yet.* The plain lines for the two sides of the 32 debates (to be written from the checked texts, read
      blind by readers that wrote none of them, and adjudicated: the checked lane's rule for plain lines). A plain line
      for what each source found, where no plain line of the answer rests on it. The same order on the old research
      page of an answer.
    - *Site 2.15.1, old phones.* Safari before 16.4 (every iPhone that stopped at iOS 15, and those not updated since
      early 2023) cannot read a look-behind in a pattern. Two were written as literals in the page's script, and a
      literal the browser cannot read stops the whole script: such a phone showed nothing at all, since before this
      version. Now no pattern of the page has one (`insNb` asks the browser first and uses the plain word edge where it
      cannot; the spelling pass takes the character before a word with it); `liveCites`, no longer called, is gone; the
      build refuses a look-behind anywhere else. Tried with every look-behind refused, as such a phone refuses it:
      Insight answers the same. Not tried on a real old phone: none is at hand.

30. **Something real within seconds for a question the site does not know** (17 November 2026, 22:11 and 22:14
    Athens). His words: "a big problem is that answers take too long to get responses and people are used to get
    responses instantly. We have to make an ai which is able to do that for questions it does not know"; "it feels
    stupid and slow our ai should be able to find answers almost instantly". With three pictures from his phone: "I
    asked 'how many people die from heroin' and it was 'answered' I got sent into the statistics and no statistic is
    about deaths from heroin... Our ai is stupid"; "'Statistics' with the back arrow is in front of the menu and covers
    a word behind it that I may want to read"; "I may want to read the history of questions I made somewhere although
    it has to be discreet"; of the kanna row on his list: "has words in front of its text too ... bad design"; "when I
    click on 'see the evidence' I see the answer again and I have to scroll down to see the sources the sources should
    just come down and when I click on 'See the evidence' again they should hide. That way I would not feel lost";
    "these should be removed from the landing page 'Try is ketamine addictive ...'".
    - *Site 2.15.3, the faults.* A figure has its own address (`#numbers/part-n-europe/f-death-heroin`): it opens the
      place on that drug at that kind of count however it is reached (the "Answered" row of his list held only the
      place). The page's name at the start of a row of parts no longer stays in front of the row. A waiting row is one
      flow of words. "The evidence" on an answer unfolds the sources under it, plain words first; a second tap folds
      them; "All the scientific detail" opens the whole research view. No example questions on the start page. Past
      searches: the last thirty, on the device only, folded under one quiet line, **off until the reader turns it on**
      (the site keeps nothing typed unless the reader chooses so, and a phone is often shared; a list of questions about
      drugs is not for everyone who picks it up); turning it off clears it. Found on the way: in the results a
      machine-written answer's line squeezed the drug's name into a column one letter wide on a phone.
    - *Site 2.16.0, at once.* An answer of ours takes a day or two, because papers have to be found, read and checked.
      What has been published on a question can be looked up in seconds. When a reader sends a question, the page asks
      the site's own server (`/api/find` in `site/worker/_worker.js`) for the papers on its drug and its key words in
      Europe PMC, the open index of medical research, and shows up to six under the "Sent" line: title, kind of paper,
      year, journal, free to read or not, and the link. With them: "We have not read these yet, and a title is not a
      finding. Our own answer follows." What leaves the device for it: the drug's names (a page's names; a started
      page's names; a word the model's list does not hold, for a drug we do not know) and up to five plain key words;
      never the sentence. What the server sends on: those terms, from itself. Nothing is kept or logged; Cloudflare may
      keep Europe PMC's reply for a day. **No model reads anything, so nothing is said that is not a record of a
      paper**, and it costs none of the free model allowance. Not looked up: a question about dying, overdose, amounts,
      pregnancy, children or an emergency (the lane's own list of what waits for a person), in the page and again in
      the server; a question that names no drug. Checks: the server's own test 57 (10 new), layout 137, Insight 177.
    - *What it is not, and what a written answer within seconds would take.* It is the sources, not an answer in plain
      words. A written answer at once means a model reading those papers while the reader waits. Two things stand in
      the way, and both are his to decide. (1) **The server has no model**: Cloudflare's Workers AI has to be bound to
      the site (in Cloudflare: Workers & Pages, pharmakon, Settings, Bindings, Add, Workers AI, variable name `AI`). (2)
      **The checks**: the lane's answer passes a reader, a writer, a second reader, further readers and our own checker,
      about 1,200 neurons and several minutes; the free day leaves about 1,000 neurons beside the lane, so a few answers
      a day at that price, or many with fewer checks. The step the editor proposes, which loosens nothing: with the
      binding, the server asks the model for **one fragment of each paper's own summary, at most 15 words, that bears on
      the question**, and code checks that every fragment stands word for word in that summary before it is shown. The
      reader then sees within seconds what the research says in its own words, with its link; nothing is written by a
      model that a reader could take for our finding. About 50 neurons a question.

31. **By itself, at once, and understood** (17 November 2026, 23:17 to 23:57 Athens). His words, in the order he wrote
    them. Of the line under the box on the start page ("Insight answers on your own device, from research we checked,
    each country's law, emergency numbers, drug checking and what is known about mixing"): "this is limiting Pharmakon
    insight ... it's about everything there are no limits". With a picture of unrelated rows under "does kanna help with
    anxiety": "did you make insight more stupid?"; then: "oh it loaded"; "for a few seconds it didn't and i thought it
    was stupid". Of the answer within seconds (decision 30): "we have to make instant as good as getting answers from a
    very good claude api. whatever it takes. you can give me a prompt with steps that i can do with chatgpt". Of the
    research list that came only after "Send": "it should automatically search the user should not even have to click
    it"; and, typing a question he had already sent: "now when i type it again the sites do not show". With a picture
    of "how many heroin deaths in america" answered by the figure for the European Union: "the ai should understand
    what i mean! it should send the question immediately in every instance and the user should be notified make it
    ... smart always". And: "Pharmakon Insight under Pharmakon is a bit redundant it is the same logo and the same
    first word. although i like the name Pharmakon Insight i don't know ... how we should include it".
    - *Site 2.16.1 (18 November, 00:12 Athens).*
      **The research comes by itself, every time.** Whenever Insight has no answer of ours to a whole question about a
      drug (not answered; a question like it on our list; a word we do not know as a drug), in the results and in the
      sheet, sent or not, the page looks the published research up (`insAuto`, `/api/find`) and puts it under the line
      that says so. In the results it waits 0.7 s so that nothing is asked while the reader types; on Enter at once;
      what it found is kept for the visit, so the same question is not asked twice. What leaves the device is what
      left it in 2.16.0: the drug's names and up to five plain key words, never the sentence. The quiet line at the
      head of the results now says exactly that ("With no answer of ours, only the drug's name and a few key words go
      out, to look up research"), and About us, Privacy has a switch for it on the reader's own device
      (`pk-auto`): off, one quiet button looks it up on a tap. The page learns from its one question to the server
      (`GET /api/ask`: `find`) whether research can be looked up at all, so a copy of the site without the server asks
      nothing.
      **The place a count names is read.** "how many heroin deaths in america" was answered with the EU's 1,600: the
      figures were chosen by drug and kind and the place asked for was not read. `insFigPlace` reads it (the world,
      Europe, a country by any of its names, "americans", "here" for the reader's own country) and `insFigures` marks
      the figures from it. The site has no count of heroin deaths in the United States; so the page now says "We have
      no checked figure on this for the United States yet", the question stays open (it can be sent, and the reader's
      list does not call it answered), and the EU's figure stands under "Figures from other places", never as the
      answer. "heroin deaths in the us", "cocaine statistics in europe": a few words with the place after them are a
      count too.
      **The seconds while Insight gets ready.** The unrelated rows were the plain word search, shown while Insight was
      starting (it has to be started on every opening of the page). A device that has fetched Insight before now starts
      it when the page opens (`pk-ins-had`; nothing is downloaded for it: the files are in the browser's cache; a first
      visit still fetches them on first use, and a connection that saves data only when asked). While it gets ready a
      whole question gets one calm line, "One moment: Insight is getting ready to read your question…", and no row
      found by a word in common (a drug's own page stays; a name alone keeps its rows); on a slow first download the
      rows come back after eight seconds under a line that says what they are. When Insight cannot start, the page
      says so and offers to try again: it no longer fails without a word.
      **The start page.** The line under the box is "In your own words. No judgement." (the box itself says "Ask
      anything about drugs"): nothing lists what Insight is "about". Under the bar that already says Pharmakon, with
      the mark, the name is said by its own word alone, "Insight", in the site's colour: no second mark and no second
      "Pharmakon". The whole name stands where nothing around says Pharmakon (the box's label for a screen reader,
      "This is Pharmakon Insight.", About us).
    - *Site 2.17.0 (18 November, 00:49 Athens): the question, sent by itself, and the reader told.* His words: "it
      should send the question immediately in every instance and the user should be notified".
      **What the reader sees.** A whole question about a drug that Insight has no answer to no longer has a button.
      Once it has stood unchanged for 2.5 seconds in the results (so that a sentence still being typed is not sent
      piece by piece), or at once on Enter, the page sends it and says so in the same place: "Sent to our system, so
      that it gets answered. It turns green under 'Your questions' on the start page when it is." with one quiet way
      out beside it, "Don't send mine", which switches it off on that device. The question is put on the reader's own
      list like one they sent themselves; a beginning that went out a moment before the whole question leaves that
      list; a question the reader took off the list is not put back in that visit. The line at the head of the results
      says what is true now: "A question we have no answer to is sent to our system by itself, so that it gets
      answered: no name, no address." A count asked for a place we hold no figure for is sent in the same way (so the
      system learns that the United States' figures are wanted).
      **What is not sent by itself.** A beginning; a question that is not about drugs (its quiet "send it to us"
      stays); what the site does not answer; a question Insight answers. A word we do not know as a drug is sent by
      itself only when research is published under that name (the lookup found papers): then it is most likely a drug
      the system has yet to learn. For a question like one on our list nothing of the reader's is sent: the device
      counts the listed question by its number, as before, and the LISTED question (the list's words) is put on the
      reader's list by itself, so that they are told when it is answered.
      **The editor's own rule for these, which he did not ask for and which stands unless he says otherwise.** Nobody
      pressed anything to send such a question, so its words are never written into the public repository. The server
      keeps it apart (`aq:` keys, 180 days; counted with the question somebody chose to send when it is the very same
      one; at most 250 a day, so that such questions can never crowd out one that somebody sent). The half-hourly run
      reads them into a file of the run's own temporary folder (`fetch_questions.py --auto`), the scout's second pass
      writes everything there (`--out`, `--report`), and `ask.py --report` makes the item on the system's list from
      it: OUR wording, and a fingerprint of the visitor's words in its state, as for every question. The questions
      people chose to send before are still in `data/auto/questions.json`, `data/auto/report.json` and
      `docs/MISSING.md`: whether those stay public is still his to say ("keep them private").
      **The switch.** About us, Privacy: "Send unanswered questions and look up research by themselves" (`pk-auto`).
      Off: the button to send by hand is back, saying what it sends, and one quiet button looks research up.
      **Not tied to the browser's "do not track" wish**, unlike the counting of listed questions: nothing here follows
      a person (no name, no address, no cookie, no number for the device), and a reader whose browser sends that wish
      would otherwise meet a site that looks broken. The notice and its own way out are what the reader gets.
    - *The written answer within seconds (site 2.18; the server's part is in 2.17 and does nothing until the binding
      exists).* `POST /api/answer` in `site/worker/_worker.js`: for a question about a drug that the site has no
      answer to, the summaries of the papers Europe PMC finds are read by one model run by Cloudflare itself (Workers
      AI: `@cf/meta/llama-3.3-70b-instruct-fp8-fast`, the lane's writer, which keeps to a form), which writes one to
      three sentences, each saying what ONE paper found, each with that paper's own words (at most 15, copied) and
      its link. The code decides what is shown, not the model; a sentence that fails any of these is thrown away:
      its quoted words stand in its paper's summary, character for character; it names the kind of paper it rests on
      as Europe PMC files it, and no other year; every number in it is in that summary; no amount, dose or timing, no
      advice, nothing on making an effect stronger, no way of taking compared with another; a word that makes a
      finding bigger or surer only where the summary has that word; a summary about animals or cells says so; it
      bears on the question. Not answered there: dying, overdose, amounts, pregnancy, children, suicide (they wait for
      a person, as in the lane), and what research summaries cannot answer (the law, prices, drug tests).
      It is shown under its own label and is never an answer of ours: nothing of it enters the site's data; the
      question still goes to the lane, which reads the papers themselves.
      **Why not the lane's own checks.** The lane's exam (decision 23) measured the free models as judges: the best of
      them let through as many wrong cards as chance. What worked there was a model that copies the source's words and
      code that decides. The answer within seconds is built on exactly that and on nothing a model judges.
      **What it costs.** Cloudflare's free allowance is 10,000 neurons a day for the whole account. The answer within
      seconds stops by itself at 3,500 a day and 60 new answers (`IA` in the worker; counted in the store under
      `ian:<day>`); the lane now stops at 6,000 (`OUR_LIMIT` in `scripts/auto/llm.py`, was 9,000). About 100 neurons
      an answer: some 30 new questions a day; an answer once written is kept for 30 days and given again without a
      model. On the free plan a used-up day ends in an error, never in a charge (Cloudflare's pricing page, read on
      18 November 2026: "further operations will fail with an error"); the page then shows the papers as before.
      **What is kept.** The drug's names, the key words, the sentences that passed with their papers, the model and
      the time (`ia:` keys, 30 days); never the reader's sentence: so that the editors can read everything the system
      wrote this way. Reading them into the editors' view is the next step (`scripts/editor/next-steps.md`).
      **His step.** Cloudflare, Workers & Pages, pharmakon, Settings, Production, Bindings, Add, Workers AI, variable
      name `AI`; then one publishing. Given to him on 17 November at 23:45 with a prompt for ChatGPT that asks for no
      token, key or account number.
    - *Site 2.18.0 (18 November): the page's part.* Where the server says it can (`GET /api/ask`: `quick`, asked once
      on every opening of the page now, not once per tab, so that a tab left open learns of the binding), a question
      that is sent by itself also gets its few sentences: asked for 1.2 s after the result stands (at once on Enter),
      once per question per visit, shown right under the line that says we have no answer of ours and above the list
      of papers, as "In short, from the papers' own summaries": each sentence, then its paper as a link (kind, year,
      journal) and "The paper's own words: ...". Last, the line that says who wrote it and what was not read: "Written
      just now by our system from the summaries of these papers. It has not read the papers themselves, and no person
      has checked it. Our own answer follows when it is ready." (an answer given again from the store says the day it
      was written). With the reader's switch off, one quiet button asks for it. The site says how it is made under
      "Answers written by our system" (Methods) and what goes where under Privacy.
      **How the editor sees it work.** The workspace cannot reach the site, so every publishing run now asks the live
      server three things and writes the replies into its notes (`scripts/auto/live_check.py`; lines that begin
      "server:" in `data/auto/deploy/_last-run.txt`): what the server can do, the research it finds for the editor's
      own test question ("does kanna help with anxiety"), and the answer within seconds with every sentence that
      passed. No key, no visitor's words; the server keeps an answer for 30 days, so the test costs the free allowance
      once.
      **What it is not, said plainly.** It reads summaries, not papers; it says what single papers found, not what the
      evidence as a whole shows; a free model writes it and rules in code decide what may be shown, so it will often
      show one sentence, or none, where a strong model with the papers in hand would write a rounded answer. That
      rounded answer is the lane's, and the checked one is the editors'. The free allowance holds some 30 new
      questions a day; beyond that the reader gets the papers, as in 2.16.
      **Tried with the real model before a reader meets it (site 2.18.1).** The editor's workspace can reach neither
      the site nor the model, and on the site the model answers only once he has bound it. `scripts/auto/instant_trial.mjs`
      (the lane's workflow, a request `instant-*.json`) runs the very file the site's server runs, on GitHub's machine,
      with the model asked through Cloudflare's own API with the repository's key (the same model, account and free
      day; what it uses is written into the lane's ledger) and the real Europe PMC, on the editor's own questions. It
      writes `data/auto/instant/trial-*.json`: the sentences kept, the ones the checks refused with the reason, the
      model's raw words, the time taken. The server now keeps the refused sentences with their reasons beside each
      answer too (`drop`; never given to the page), and a number the summary writes as a word counts for its figure.
      **What is looked up, made more exact (site 2.18.2).** The editor printed what twenty real questions sent to the
      lookup and found five faults, mended in `insFindTerms` and `findQueries`: a question about a drug we do not know
      took a second everyday word as a drug's name ("is tianeptine addictive" searched for every paper with
      "addictive"): now only the first word that is no everyday word, nor made from one; the name the reader wrote was
      lost where a page stands for several drugs ("xanax" searched as benzodiazepines only): it now goes first, unless
      it is an everyday word ("weed", "acid", "speed" would find every paper that holds them); "GHB / GBL" was one name
      and found nothing: two names; a street name's own word counted as a key word ("magic" of "magic mushrooms"): the
      key words are read with the names taken out; words that stand in every summary were key words ("cause",
      "study", "time", "same"): left out. An everyday word now goes with the word papers use ("hungry": appetite;
      "nosebleeds": epistaxis; "concentrate": attention), and a key word is asked for in its one and its many
      ("migraines", "migraine").
      **Two small things with it.** "us heroin deaths": "us" is read as the country where it stands first or last in
      a few words that ask for a count ("how many of us use heroin" is not). The heading over the figures of other
      places is now "Figures we do have": for a country inside the EU, the EU's figure is not from another place.
      **What the papers say, in their own words (site 2.19.0, 18 November 2026).** The first trial with the real
      model ran at 02:05 (Athens) on 18 of the editor's own questions (`data/auto/instant/trial-20261118T0005-0001.json`:
      1,472 neurons; 4 to 17 seconds a question, of which the model took 4 to 13). Read line by line by the editor:
      (a) of 19 sentences that passed the rules of 2.18, about six said more than their paper: "may ameliorate
      laboratory stress/anxiety responding" became "ameliorates anxiety"; "GHB/GBL" became "GHB and GBL are used
      together"; a review of microdosing became "LSD caused no lasting personality benefits"; what a paper said of
      one benzodiazepine was said of them all. That is the rate the lane's exam found for free models (decision 23),
      and it is not one this site shows a reader, under any label;
      (b) 18 of the 52 quotations were one to three words: copied words that prove nothing;
      (c) the rule "bears on the question" refused true findings ("antidepressant" for depression, "dependence" for
      addiction);
      (d) the search was the weakest part: it asked for papers with ANY key word, the newest first, so "does
      modafinil improve memory" read reviews of sleepiness and of stroke.
      So 2.19 changes what the thing is. **The reader is shown the paper's own words, not the model's.** The model
      chooses up to three papers and, in each, the sentence that carries the finding, and points to words in it. Code
      then chooses at most 15 words of that sentence, in a row, that hold the words pointed to (`iaWindow`): from the
      start of the sentence or of a part of it to its end where that fits, and never leaving out a word the sentence
      turns on. "There was no evidence that the extract reduced anxiety" is shown with its "no evidence", or not at
      all; the same holds for a question or an aim before the words ("we examined whether"), for what sellers say
      ("is claimed to"), for a "may" that the 15 words do not hold themselves, and for a "no", a question or a "but"
      after them. "No" is read widely: not, never, without, fail, lack, non-significant, insufficient, unproven,
      little, few, weak, rarely, only, contrary, myth, false. Where 15 words cannot hold such a word together with
      the words pointed to, nothing of that sentence is shown. A sentence is not cut after "vs.", "e.g." or "et al."
      (cut there, a "no" could fall into another piece than the words it governs). No link is ever shown. Words that hold an amount, or dying, overdose, pregnancy or children, are never shown. A sentence that
      speaks of animals and of people at once is not shown in part. A line says "in animals or cells, not in people"
      where its sentence or its whole summary is about those, and "its summary covers work in animals or cells too"
      where a summary covers both and the sentence does not say which. The label of a summary's section ("RESULTS:")
      is not part of the paper's words.
      **The model's own sentence** is still written, and kept beside the line (`plain`: the sentence, the code's
      verdict, the reason; never given to the page), under a far stricter rule than 2.18's (`iaPlain`): every word of
      it must stand in the very sentence it rests on or in the paper's title, a "may" is kept, a "no" is neither
      gained nor lost. It is shown only where `IA.plain` is set, and that is set only after an exam: the editor reads
      the sentences this rule calls sound, from trials with the real model, against the papers' words, and counts.
      Until then the reader gets the papers' words, which cannot say more than the paper.
      **The search** (`findQueries`, `findPapers`): every key word must stand in a paper's title or summary; a key
      word and the word papers use for it are one thing asked two ways ("appetite|hungry"); a word is asked for in
      its one and its many and in its other spelling ("colour", "color"; "-ise", "-ize"); the most cited reviews on
      the very question come first, then the papers Europe PMC ranks first, then the other reviews; the wider
      searches (any one key word; reviews of the drug itself) only where that found fewer than three papers. Words
      every question holds are no key words ("improve", "lower", "change", "affect", "damage", "loss"); a few short
      ones are ("eye", "gut", "eat"); an organ goes with the word papers use ("heart": cardiac; "kidneys": renal).
      On a page that stands for several things ("Cannabis (THC, CBD)") the search is for the one the reader named
      ("does cbd help with sleep" is about CBD), and for all of them where the reader named none ("weed"). "Bears on the question" is now asked of the paper: a key word, or a word papers use for it
      (`IA_NEAR`), stands in the sentence, in the title or elsewhere in the summary; which of the three is kept, so
      that the editor can read how the lines found by title or summary alone look.
      **What a reader sees:** the heading "What the papers say, in their own words"; each line the paper's words in
      quotation marks, and under them the kind of paper, its year and its journal as the link; then "Chosen just now
      by our system from the summaries of these papers: the words are the papers' own. It has not read the papers
      themselves, and no person has checked its choice. Our own answer follows when it is ready."
      **Checks:** `scripts/ux/worker_test.mjs` (156: the choice of the 15 words on hard sentences, the model's
      sentence one fault at a time, the search) and `scripts/ux/site24_check.js` (the page, with a stand-in model).
      The trial script now writes, for each line, the shape of the rest of its sentence (little words only, every
      other word a "_"), so that a turning word left outside the 15 can be seen without copying a summary into the
      repository. A second trial follows this publishing (`data/auto/requests/instant-0002.json`).
      **Said plainly to the senior author.** He asked for "instant as good as getting answers from a very good claude
      api". For WRITTEN answers that is not reachable with free models at this site's bar: the trial measured it.
      What is reachable, and built: within seconds the reader gets the most cited papers on the question and their
      own words on it, with nothing of the system's said in between, and the written answer follows from the lane. A
      fluent instant answer at the site's bar needs a strong model, and those are paid: his rule ("only free") stands
      until he changes it.
      **No model: each paper's own words by fixed rule (site 2.20.0, 18 November 2026, 03:15 to 05:30).** The
      second trial ran right after 2.19 was published (`data/auto/instant/trial-20261118T0112-0002.json`: 26 of the
      editor's questions, the real model, 1,941 neurons, five seconds at the median). The paper's own words could no
      longer say more than the paper; what the model added was still wrong:
      (a) it chose sentences about aims and methods ("Comprehensive literature reviews of ... have been conducted"
      was shown as "evidence supporting cannabis/cannabinoids in the treatment of pain") and lists of what a
      questionnaire asked ("better able to concentrate ... after EC use") as if they were findings;
      (b) words were cut loose from what they were about: under "does cocaine cause nosebleeds", "Bleeding occurred
      in 32 patients receiving cocaine (60.4%)", from a trial of cocaine as a medicine against bleeding at
      intubation; "improvements in appetite", from a case report on a horse;
      (c) of its own 18 sentences that the strict rule of 2.19 called sound (every word in the source sentence), the
      editor found eight that said more or other than their source ("Preclinical research has generally supported
      anecdotal claims that ibogaine ..." became "A 2013 review says ibogaine attenuates withdrawal symptoms");
      (d) the most cited papers that only MENTION a drug read as answers: for "GHB", a meta-analysis on diabetes
      (GHb is glycated haemoglobin); for amphetamine, the phencyclidine model of schizophrenia.
      So the model is taken out. **What a paper found stands at the end of its summary, in words that hold the
      question's key word: a rule can find that**, in a fraction of a second, for nothing, the same every time, and
      with the reader's sentence sent to nobody. `/api/find` now gives each paper with, where the rules find them,
      at most 15 of its own words (`iaPick`, `iaWindow` in `site/worker/_worker.js`); `/api/answer` answers that it
      is off; the page shows the words in quotation marks under the paper's title (so they are always read in their
      paper's frame: the cocaine trial's words stand under "Cocaine versus xylometazoline to prevent epistaxis after
      nasotracheal intubation"), and the separate block of 2.18 and 2.19 is gone.
      **The rule, as it stands after seven trials without a model** (trials 3 to 9, on GitHub's machines with the
      real Europe PMC, free; 44 and then 56 of the editor's own questions each; every line read, the rule mended,
      a test written; `data/auto/instant/trial-*-0003.json` to `-0009.json`; `iaPick`, `iaWindow`):
      which sentence: one under a label for results or conclusions, or, in a summary without labels, in its later
      half; that holds a key word of the question or a word papers use for it (`IA_NEAR`: "5-HT" for serotonin,
      "dependence" for addiction); with every key word in the sentence or the title; that NAMES THE DRUG, or, in a
      paper about the drug, says "the extract", "this compound", "its use", "regular consumption" (trial 6: of
      twelve shown sentences that named neither, ten were about something else: "Chronic METH use was ..." in a
      paper on MDMA and methamphetamine, "His epistaxis was successfully treated", "Genetic testing ... was also
      undertaken"). Never a sentence about aims or methods ("We also review ...", "We then estimated ..."), one
      that says what should be looked at next ("may be warranted", "are pending", "is critical", "highlight
      potential intervention targets"), an editors' note, or any sentence of a paper whose title is about what
      waits for a person;
      which words: a whole part of that sentence, at most 15 words. The run ends where the sentence ends, or at a
      comma after which the sentence only adds something (", with ...", ", which ...", ", suggesting ...", a new
      clause after ", and"), or before brackets after which it ends or only adds (never "... 40 of 52 | (76.9%) of
      cases"); it begins where the sentence or a part of it begins (also after ", but"), or after words that only
      lead in ("We found | no evidence that ...", "there was | no ..."), never after the words that say whom it is
      about ("Carriers of the allele were | most likely to ... if they used cannabis"), never with a word that
      hangs on what was cut ("which", "characterized by", a preposition) nor inside a part that begins with a
      preposition ("..., for | the prevention of epistaxis ..."), never with the items of a list or cut inside
      one, never after brackets in the middle of what the sentence is about. THE RUN ITSELF NAMES THE DRUG or
      says "the extract" (trial 7: "... these results suggest that | some panic disorder patients may have
      abnormalities in neuronal systems involving adenosine", of a sentence that named caffeine elsewhere); the
      name counts inside a joined word ("MDMA-assisted therapy"). No word the sentence turns on is left outside
      the run (as in 2.19, and the kind of evidence before it: "in case reports", "an open-label pilot"), nor the
      part that says of whom or when the sentence holds ("Among adults with treatment-resistant depression, |
      ...", "When used daily, | ...", "During withdrawal, | ..."; not the study itself, "In this trial of sixty
      adults, ...", nor "After the drug, ..."), nor words that point back to another sentence ("these effects",
      "in this context"). A clause that opens the sentence with "Although ..." does not govern what follows its
      comma;
      never shown: a sentence that holds an amount, a dose or timing, how strong a product is ("high in
      cannabidiol", "potency"), dying, overdose, pregnancy, children, taking drugs together, making an effect
      stronger, or ways of taking compared (such a word often carries the condition or the people a finding is
      about: cut around it, the rest would say more); advice and promises of safety ("should", "avoid", "safe",
      "well tolerated": the words go around them, and nothing after them is shown); links; statistics in signs or
      in brackets; half a bracket;
      animals: "in animals or cells, not in people" where the sentence says so, where the title does and names no
      people (a study in rats writes "naive individuals"), or where the whole summary does; "its summary covers
      work in animals or cells too" where it covers both and the sentence does not say which; a sentence that
      names animals and people at once is not shown ("adult rats" is animals);
      "what is X": the sentence that says what the drug is, from the start of a summary of a paper about it.
      **The search**: the drug's name must stand in a paper's TITLE; a short name that means other things in
      medicine counts only beside a word that settles it (`FIND_CTX`: "LSD" beside "lysergic" or "psychedelic",
      "GHB" beside "hydroxybutyrate", "benzo" beside "benzodiazepine"); names in their one and their many. Three
      searches are asked together: the most cited papers that hold every key word in their title, or are reviews
      that hold it; the newest with drug and key words in the title; and the papers that hold both anywhere. Of
      the most cited, those with the key words in their very title come first. The first drug a question names is
      what it is about, a second one is a key word ("does kratom help with opioid withdrawal"); the name the reader
      wrote is asked for first ("xanax", with "alprazolam"), and what its page is called ("benzodiazepines") only
      where that finds fewer than three papers; a word for a whole class ("psychedelics") stands for itself. On
      the page: "help you study", "for exams" is asked as what papers call it (academic, cognitive, students:
      "study" stands in every summary); "suppress", "boost", "treat", "find", "drug" are no key words.
      **Time (trials 6 to 9).** The server's own computing for a question is 2 to 4 thousandths of a second; the
      time is Europe PMC's. It answers a search in a fifth to a half of a second, but about one request in three
      HANGS for two to ten seconds, whatever is asked (trial 6: the median question waited 2.6 s; the publishing
      of 04:41 showed the same from the real site: 2 papers for kanna and anxiety where there are 6). It is not
      the search that is slow: the same search asked again at that moment came back at once 39 times of 54 (trial
      7). So (`findPapers`):
      a search that is not back after 0.45 s is asked a second time, and after 0.95 s a third (each asking with
      its first words in another order, so that it is a request of its own); the first reply counts;
      the list is given as soon as the most cited AND the newest are back; after 1.4 s whatever three papers
      there are, with "more": 1 when a search is still out; after 2.6 s whatever there is;
      a search that is still out finishes behind the reply (Cloudflare keeps Europe PMC's replies for a day);
      the page, told "more", shows the list with "Still looking for the most cited papers on this…", asks once
      more half a second later (and once again two seconds after that), and puts the whole list in its place.
      What that gave, first list after (median; share under 1 s; under 1.5 s; lists given with a search still
      out): trial 6 (waiting): 2.60 s; 8 of 44; 9 of 44; none said so. Trial 7 (second asking; the newest waited
      for a quarter of a second): 0.36 s; 48 of 56; 54 of 56; 12. Trial 8 (three askings; the newest waited for):
      0.53 s; 47 of 56; 55 of 56; 3, whole after 1.9 to 2.5 s. Trial 9 (the same; Europe PMC hung more): 0.66 s;
      41 of 56; 54 of 56; 9, whole after 2.1 to 2.7 s (one 5.5 s). On top of it, while a reader types, the page
      waits 0.7 s after the last key before it asks (on Enter it asks at once).
      **The first publishing, and 2.20.1 (05:23 to 06:00).** The publishing's own check asked the real site six of
      our questions (`data/auto/deploy/`): 0.8 to 1.5 s each, the middle one 1.1 to 1.4 s, slower than the trials.
      From the site's own server a search takes a half to nine tenths of a second where the trial machine took a
      fifth to a half (it opens a new connection to Europe PMC each time), so the second asking at 0.45 s came
      nearly always and for nothing ("3 asked again" of 3). And the question asked a second time still went to
      Europe PMC (0.2 to 0.3 s a search): the setting that should have kept its replies did not. So, in 2.20.1:
      the most cited papers are asked for again after 0.6 s and 1.3 s, the two other searches only after 0.9 s
      and 1.7 s; the list is given as soon as the most cited are in, with the newest if they come within three
      tenths of a second (the newest are one paper of the six: nobody waits for them longer, the list is not
      changed for them afterwards, and they are kept for the next reader); after two seconds without the most
      cited, what the other searches found, with "more"; a search is not asked again once its list has gone out;
      and every reply of Europe PMC is kept for a day in Cloudflare's cache by the server itself, under the
      search's address (checked before each asking). The reply now also says which asking answered and how long
      that asking took, and the publishing's check asks twelve questions, so that the next run shows what a
      search costs from the real site.
      **What the real site gave with 2.20.1** (publishing of 05:36, `data/auto/deploy/`; twelve of our questions
      that nobody had asked before, as timed from the publishing machine, which opens its own connection to the
      site each time, about 0.3 s of every figure): 0.3 to 1.2 s each, the middle one 0.9 s, three in four under
      1.0 s; a search itself 0.2 to 0.9 s, mostly 0.6 to 0.7 s (0.2 to 0.3 s where Europe PMC had been asked the
      same not long before); the most cited needed their second asking about every other time and never their
      third; no list was given without the most cited. A question asked a second time: its searches 0.0 s, "from
      what was kept", 0.3 s in all. In a reader's browser, whose connection to the site is open, that is about
      a tenth to nine tenths of a second after the page asks; while typing, the page asks 0.7 s after the last key.
      The tenth trial (the same server on the trial machine): first list after 0.50 s at the median, 44 of 56
      under a second, all under 2.1 s; 3 given without the most cited, whole after 2.5 to 2.9 s; 198 requests to
      Europe PMC where the ninth made 265; 45 lines for 29 questions, the same lines as before.
      **What the trials gave in words** (lines shown, of papers listed; questions with at least one line):
      trial 3: 147 of 253, many of them pieces of sentences. Trial 4: 66 of 252. Trial 5: 54 of 236; 27 of 44.
      Trial 6: 55 of 234; 30 of 44; about fifteen of them beside the point or about something else. Trial 7: 48 of
      323; 31 of 56. Trial 8: 41 of 323; 28 of 56. Trial 9: 46 of 323; 30 of 56; the editor found none that says
      more or other than its paper, and a handful beside the reader's point but true ("The correct therapy for
      cocaine cardiotoxicity is not known", under "does cocaine damage the heart"). Lines as they stand:
      "Tianeptine misuse is associated with opioid-like dependence, withdrawal, and toxicity"; "…MDMA-assisted
      therapy is highly efficacious in individuals with severe PTSD…"; "…using cannabis could increase their risk
      of developing a psychotic illness later in life"; "Ketamine impaired attention, working memory, and delayed
      recall"; "However, it is unclear if cannabis use increases the risk of developing long-lasting anxiety
      disorders"; "Our results suggest that modafinil does not possess an addictive potential in naive
      individuals" (in animals or cells, not in people). Most papers get no words: of 157 sentences that stood in
      the right place and gave none (their shapes are in trial 8, never their text), most were lost to the limit
      of 15 words, which is the site's rule for quoting. A paper without words is still listed with its title.
      **What it is not.** Not an answer: a list of papers with a sentence each, picked by rule, unread by us, under
      a line that says so. A rule cannot tell that a trial of cocaine as a medicine is beside the reader's point;
      the title under which the words stand can, and the reader can. The written answer is the lane's, and the
      checked one the editors'.
      **For him.** Nothing to do at Cloudflare: the step he was asked for (binding Workers AI) is not needed. The
      lane has its 9,000 neurons a day back (`OUR_LIMIT`). Open, his to say: asking Europe PMC twice from the
      start would bring the first list to about 0.3 s at the median and leave fewer lists to complete, at the cost
      of two more requests to a public service for every question; not done.
      **Checks:** `scripts/ux/worker_test.mjs` (133), `scripts/ux/site24_check.js` (154: the list in two steps, in
      a real browser), and before any change to a rule: a trial (`data/auto/requests/instant-*.json`), read line
      by line.

32. **Answered by itself, within minutes, and tried again; the reader's own list behind one line** (18 November 2026,
    13:34 to 13:40 Athens; lane 19; site 2.21.0). His words, in the order he wrote them, of the questions he had sent
    ("Tried. No answer passed our checks yet · sent 14 hours ago", "Written. A person has to check it first · sent 3
    days ago"): "why are these still pending and they have not been answered yet? ... this is a bug. and also the
    questions should be automatically answered no 'Written. A person has to check it first' --- this should happen for
    every pending question not only the ones on the list.... why is our ai not working"; of "Your past searches (0) ...
    Nothing yet: a question is kept when you ask it": "this is bad design you should be able to see your past searches
    in a discreet past searches history in your device that you can click on and return easily back. it should be below
    the pending questions and it should be beautiful maybe ... a window gets open in the right ... (a similar format to
    when you click on the evidence of a particular question, it has to be completely coherent to the rest of the
    website) and their answers if we have answered them and not that ugly up and down arrow. and it should be easy and
    clear that you can delete your search history"; "'and some then wait for a person.' this should be removed from the
    landing page"; "can the answers get ... answered by themselves? and can they get answered almost instantly? one day
    or two is too ... much and slow our ai is ... ancient this is bad people want answers now"; 13:35, with a picture
    of the start page: "this format of questions is ugly you cannot even see the website"; 13:36: "our ai becoming
    perfect is our first priority. i like the quick searches but our site's answers have to be given much faster";
    13:38 and 13:40, of a question about mothers and their children's drug use that got two related answers and no
    research: "related questions are useful in this instance just not exactly what i was looking for ... so we have to
    give instant search on this instance too --- but a very big priority is still making our ai answer questions inside
    the website much more efficiently and fast".
    **What the records showed.** (a) GitHub started the half-hourly look about once in 60 to 85 minutes (asked for at
    :07 and :37; its own run list of that day), and a run that worked took 7 to 22 minutes. (b) A question was tried
    once and then left for a day or two (`turn_of`). (c) A try was lost to faults that were not the answer's: a number
    that stood in another item of the same source ("16 healthy participants": the writer named the finding, not the
    item that says who was studied), three drafts running; "the source gives this for men" where the word "male"
    stood beside animals; one writer's reply that was no JSON, twice; "the lane itself failed on it (HTTPError)". (d)
    Finished answers were parked: five for a further reader that "could not be asked", three answers about amounts
    and others for the editor's reading, six for their topic, four for disagreeing with a checked claim. (e) Why the
    further readers "could not be asked": the two that stood first never answered (Gemini 4 Hydrogen: no verdict on
    30 of 34 sentences asked together; Gemini 3.8 Flash: nothing within 170 seconds), and, found in the first run of
    lane 19, a reader that answers with the list of its verdicts alone (186 characters, ended in order) was read as
    having given none, because the lane took the outermost braces of a reply. (f) Found in the afternoon's runs: a
    question lost every try it had to ONE paper whose full text Europe PMC failed to give (HTTP 500 on that paper,
    each time): the fetch of a full text was the one call of the lane that was not guarded ("the lane itself failed
    on it (HTTPError)"). Such a paper is now passed over, with a note in the record (`looked`, "fault"), and the
    question is written from the other sources. (g) A question that was tried again was written afresh by a writer
    that had not been told why the last draft fell, and the same kind of sentence fell again (his "is sex better with
    weed": three drafts that day said more than the "potential" their source spoke of, each refused by a reader).
    The writer of the next draft is now told what a reader or our own checker said of the last draft's short answer
    or But (`last_refusal`: only of an answer of this lane that ended with none; the record says so under `gates`,
    "told"); it stays bound by every rule and is read by every reader as before.
    **The index of papers was slow that afternoon, and the site said something false** (site 2.21.1, 15:40 to 16:30
    Athens). The first publishing of 2.21.0 asked the live server twelve questions and none of the most cited came back
    within three seconds. Asked from the senior author's own computer, Europe PMC took 24 to 27 seconds for every
    search, sorted or not (a search with 78 papers; in the morning: half a second). What that did: (a) the site's
    server gave a search up after 20 seconds, so no reply was ever kept, and each later asking of the page asked every
    search anew, up to nine requests a question to a service that was struggling; (b) the page asked three times in
    eleven seconds and then wrote "We looked in Europe PMC ... nothing was found on these words" of a question with
    78 papers: a false statement; the same where Europe PMC says no or cannot be reached (the server called that
    "found nothing"); (c) in the lane, one paper whose full text could not be fetched cost the try (above), and a
    question whose sources could not be fetched would have been written down as "no source that can be read" and left
    for a day, and on the reader's list as "Searched. Nothing we can read is published on it yet". **What is
    different now.** The server lets a search finish for 28 seconds behind its reply (Cloudflare allows 30) and keeps
    the reply; a later request does not ask Europe PMC again for a search that is still out but waits for the reply
    where it will be kept (a note in the cache, read and written only for a question's first three searches:
    Cloudflare counts every call to its cache with the requests, 50 in all for one request); a search that failed is
    told apart from one that found nothing (`down`). The page asks on for some forty seconds (seven askings), says
    "Still looking. Europe PMC ... is answering slowly right now", and where it stops, or the index said no: "Europe
    PMC ... did not answer just now, so we cannot say yet what is published on this. Look again". "Nothing was found"
    stands only where the searches came back empty. A word we do not know as a drug is sent to the system on the whole
    list, not on a first thin one. In the lane a source that could not be FETCHED is no longer a source that says
    nothing: such a try is a fault of the moment ("soft": the next run, three times a day; from the seventh try in all
    the question waits as any other), the finder searches again a question whose searches did not all come back, and
    the reader's list says "Working on it by itself" for it. Checks: 147 server tests (a search that is out is not
    asked twice and is given when it is kept; the index says no), three more in the browser (the slow index from the
    first line to "Look again", some forty seconds), the lane's own. **Not solved by this:** while Europe PMC is slow,
    the list is slow. A second index for such hours (PubMed's own interface, which gives summaries too) is the next
    step; its words would need a trial of their own.
    **The first answer that went out under the stricter bar, read by the editor** (16:05 Athens; `au_w_a0011`, "Do
    mothers worry about their children taking drugs?", his own question of 13:38 in our words; written by team L in
    the run GitHub's clock started at 15:40, published 15:56; held to the bar because it is about children). "Yes,
    the NHS says parents of people who use drugs may feel worried. One study found mother overprotection links to
    youth substance use." The first sentence is the NHS page's own ("If you're the parent, partner, child or carer of
    someone who uses drugs, you may feel worried, frustrated and alone"), said as the NHS's. The second is one study
    of five in a scoping review, whose passage says that overprotection by mothers "correlates positively with all
    substances and negatively with alcohol abuse": "links to" is true and thinner than the passage. The But is the
    code's own and true (a nearer paper could not be fetched: Europe PMC, that afternoon). Nothing in it plays a
    danger down or tells a reader what to do. It stays. Two things it showed: the line of "How do we know" for the
    study was left out for a rule (the source's own word "abuse"), so the short answer's second sentence stands
    without its line (the reference is there): a line that breaks a rule should be written again, not left out, where
    the short answer rests on that source; and the reader that reads the sources was out of reach (503) and its
    stand-in read on, as built.
    **Lane 19** (`scripts/auto/lane.py`). No gate is taken away. What code can mend is mended before a rule judges:
    a number of a sentence that stands in another item of a source the sentence already rests on puts that item
    under the sentence too, so that every reader reads the sentence beside it (`mend_uses`; never an item of another
    source, never a year); only the words "men" and "women" say that a result was for one sex (the exam's result is
    the same before and after: 3 of 31 wrong cards caught, 5 of 287 good ones stopped). A writer that gives no answer
    in the form asked for, or cannot be reached, has a stand-in (`writer_2`). The further readers that answer stand
    first (Gemini 3.6 Flash, then 3 Flash), each with 5,000 tokens more room; a reply that was cut off is asked for
    again with twice the room; a reader's verdicts are read however it gave them (`verdicts_json`); how a reply that
    could not be read ended, and how it began, is written into the record. **It tries again by itself**
    (`turn_of`): at once, in the next run, after a fault that was not the answer's (six times a day at most); the
    same day with another team of models after an answer that did not pass (twice for the system's own question,
    three times for one a person sent); then daily, then further apart (`wait_days`), and at once when the finders
    hold more. Nothing is parked for a reader that could not be asked: such an answer is kept, not shown, and
    worked on again in the next run. A second look at an answer that is shown leaves it shown if the second look
    does not pass. What the editor finds in an answer it holds goes to the writer of the next one
    (`data/auto/held.json`, "say"); the editor's word on a disagreement with a checked claim that the second
    reader called for the wrong reason is kept in `data/auto/lane/agreed.json` and that claim no longer stops the
    next answer to that question; a hold is of the version the editor read (`site/build.js`).
    **Questions where a wrong word can hurt** (the editor's rule of 15 November made every one of them wait for a
    person; his words above ask that none does). What each kind does is now a setting
    (`data/auto/lane/policy.json`, "stakes"), in force from site 2.21.0, whose pages say what it does. Dying,
    overdose or an emergency, mixing drugs, pregnancy or children: "strict": published by the system only where the
    answer meets a bar higher than every other answer's, all of it code (`strict_lacks`): its short answer rests on
    an official body's page (tier 1) or on a review read in full; a further reader read it and none was out of
    reach; no word of its first two sentences can be read as a promise of safety (`REASSURES`: safe, harmless,
    unlikely, rare unless "rare but", no risk, well tolerated ...); its opening word does not say that a danger is
    absent ("No" to a question about a danger) or that a thing may be done ("Yes" to "can I", "is it safe"); and the
    second reader and every further reader, each asked that very question ("plays_down"), said that it does not play
    a danger down (no clear word counts as yes). An answer that does not meet the bar is not parked: there is no
    answer yet and the system tries again. Under every such answer the page shows the way to the emergency numbers,
    in the words the footer has always had. **Still waiting for an editor, whatever the setting:** suicide and
    self-harm ("person"); what to do in an emergency (`NEVER_ALONE`: emergency guidance is the senior author's own
    text); an amount that kills; an answer that disagrees with a checked claim; and every answer about amounts
    (`hold_new.amounts`: on the exam of the lane's own rows 9 of 90 were not good). He can change any of it in that
    file. Tested in the lane's own check with a scripted team; no real answer has gone through the stricter bar yet:
    the editor reads the first ones in the next session.
    **The editor's reading of everything that waited** (14:13 Athens, sentence by sentence against the sources' words
    in the records). Let out: `au_w_0030`, `au_w_0031` (they waited only for a reader that could not be asked) and
    `au_w_0046` (amounts: eight rows, each a health body's own words for the people it names; `amounts` is true from
    now on so that it shows; new ones stay held). Not let out, written again by themselves with what was found:
    `au_w_0004` and `au_w_0005` (damage to nerve cells said as a fact about people where the review's findings are
    from laboratory animals; both rightly stopped by the comparison with the checked claims), `au_w_0009` ("combined
    with psychotherapy" left out), `au_w_0017` (the half-lives of two young children given as how long cannabis
    stays in an adult), `au_w_0044` (an amount an analysis worked out), `au_w_0047` ("except pregnant women" left
    out of who an amount is for), `au_w_0048` (as before). `au_w_0008`: the disagreement was a false alarm (what
    happens while the drug acts, beside a difference found in people who had used it many times): written into
    `agreed.json`, and written again. Not the editor's to let out, and left for him: `au_w_0041` (Does cannabis cause
    cancer?: it disagrees with `cl_can_smoked_cancer`, a claim of Section 7 that waits for his word), `au_w_0012`
    (after naloxone), `au_w_0010` (suicidal thoughts).
    **The first runs of lane 19** (14:21 and 14:36 Athens, the three questions of his list that an answer could be
    written for). "Does kanna have psychoactive effects?": published, read by the second reader and by both further
    readers. "Does cannabis make sex better?": written as the editor's note asked ("People who use cannabis report
    benefits like longer intercourse and better orgasms. Use has been linked to higher satisfaction in men and
    women."), accepted by the second reader and by Gemini 3.6 Flash, kept back only for the list of verdicts that was
    not read (mended the same hour). "Does kanna help with anxiety?": refused twice more for "men" (mended the same
    hour). Gemini 3.6 Flash read all three and refused, with its reason, six sentences that said a little more than
    their source.
    **The look** (`.github/workflows/auto.yml`, `scripts/auto/tick.py`). Asked for every five minutes (the shortest
    GitHub allows; it starts a scheduled run when it has a machine free). A question a person sent is searched and
    written first and alone (`--sent`), and what was written for it is kept and published in the middle of the run,
    before the system's own questions (`keep_now`, `tick.py publish`); a lane request publishes at once
    (`lane.yml`). Ceilings: 240 writing runs and 96 publishings a day; what limits a day is the models' free
    allowances (some fifteen answers). **At once, with his key** (`site/worker/_worker.js`, `startWork`): where the
    site's server holds a key that may only start workflows of this one repository (`GH_RUN_TOKEN`), a NEW question
    starts the work the moment it arrives: at most once in twenty seconds from one of Cloudflare's places, with no
    word of the question (the request names the workflow and the branch). Without the key nothing runs. His words
    when told of the five minutes (14:44): "if it can be every minute or 30 seconds or even a few seconds it would be
    even better. if it can be better than 5 minutes it's okay, whatever is best". What is best is not a faster clock
    but no clock: GitHub starts no scheduled run more often than every five minutes, and in the first hour after the
    five minutes were asked for (14:21 to 15:21 Athens) its clock started no run at all (every run of that hour was
    asked for by the editor); a run that kept looking every few seconds would hold one of GitHub's machines all day
    to look at nothing, and GitHub's terms for Actions speak against that use ("don't use Actions ... as part of a
    serverless application"; read on 18 November 2026:
    https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features). A start
    by the question itself is seconds, and costs nothing while nobody asks. Until the key is there the look comes when GitHub's clock does (about hourly on
    that day). The page still promises no time (`loop` stays false until the times have been measured on questions
    people sent).
    **The reader's list** (site 2.21.0; `site/src/app.insight.js`, askedBox, youHtml). The start page shows one quiet
    line, "Your questions", with how many were answered and how many are in progress, and no question's own words;
    it turns green when one is answered. A tap opens a panel at the right, in the frame of the evidence of an answer
    (the same sheet, bar and Back button; the phone's Back closes it): the questions that wait or were answered, each
    with what the system has done with it ("Working on it by itself", "No answer passed our checks yet. It tries
    again", "Searched. Nothing we can read is published on it yet", "Written. An editor reads this kind first"),
    then the past searches. **Past searches** are kept by themselves on the device (a question that stays in the box
    for two and a half seconds with its result, or Enter), the last thirty, each with the answer the site gave;
    until 2.20 they were off until switched on and were kept only on Enter, so the list said 0. One plain button,
    "Delete my search history", clears them; "Don't keep my searches" clears them and stops it, and the same switch
    stands on About us, Privacy, which says what is kept. An open page looks every minute whether a newer site
    exists while a question waits.
    **Research at once for two more kinds of question** (`insFindTerms`; the server's `FIND_TITLES`, `noq`). A
    question about pregnancy or children, and a question about drugs that names no single drug (its "name" is what
    research calls the subject: "drug use", "substance use"; "addiction" where it is about that; at least one key
    word is needed), are looked up now and listed BY TITLE ONLY: no words of a paper are shown for them. Until 2.20
    neither was looked up. The rule that picks a paper's own words is unchanged, and it was tried on questions that
    name a drug; words for these wait for a trial of their own. Dying, overdose, suicide and amounts are still not
    looked up. **The eleventh trial** (14:49, twelve questions that name no single drug, the key words written by the
    editor, the plan of 2.20): the titles were on the question for most ("Parental and peer influences on the risk of
    adolescent drug use", "Understanding reasons for drug use amongst young people: a functional perspective",
    "Familial transmission of substance use disorders"); beside the point where the key word has another sense
    ("creative" teaching, "potential" candidates) or stood far from the subject (poverty in a paper about pregnancy);
    one question with three key words found nothing; and it was slow: the first list after 3.0 s every time, the
    whole list after 3.8 to 11.6 s, because "drug use" in a title is a very large set and Europe PMC orders it slowly.
    **The plan for such a question since then** (`roundGen`): two searches, each asked once, both for the most cited:
    reviews with the subject in the title that hold every key word, and papers with the subject and every key word in
    the very title; one reply within five seconds in the place of a quick thin one; at most three key words; titles
    only. **The twelfth trial** (asked for with this publishing, `instant-0012.json`): the same questions and ten
    more, among them five about pregnancy or children that name a drug, this time with the names and key words the
    page itself makes for them (`insFindTerms`, read off the built page), to be read for its titles and its times.
    **Checks:** the lane's own (the mends, the stand-in, the retry rules, the stricter bar and what never goes out
    alone, the verdicts in every form, a paper that cannot be fetched), `scripts/ux/worker_test.mjs` (143: the start
    of the work with and without the key and not twice in twenty seconds; a question about suicide not looked up;
    titles only for pregnancy and for a question that names no drug, with two searches asked once each),
    `scripts/ux/site24_check.js` (162, in a real browser: the line, the panel, Back, past searches kept and deleted
    and still there after a reload, the general lookup), `scripts/ux/auto_check.js` (96), `scripts/ux/insight_check.js`
    (183; its check of what the device keeps now says what the Privacy text says: past searches, whole questions the
    reader typed, thirty at most), parity, smoke, the tick's, the finders', the validator.
    **For him.** (1) One word for his own question "Does cannabis cause cancer?": "approve" shows the checked answer
    on smoked cannabis and lung cancer (Section 7), and the system's own answer can then stand beside it. (2) If he
    wants the work to start the second a question is sent: one key, made at GitHub and pasted at Cloudflare, never
    to the editor (steps in the editor's message of that day). (3) Unchanged: "use readers" (CDC death figures),
    "keep them private" (the questions people chose to send).

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

**The exam.** Every night the whole chain is measured on our own records (statements with the passages our readers found,
and the second readers' decisions, including every correction they made), and the result is written into the repository.
The editor's first bar was at most 1 wrong sentence in 50, with the lane shutting by itself under it; the senior author
decided otherwise on 15 November at 20:58 (above): the lane publishes what passes the gates, and the exam is the measure,
with 1 in 1,000 as the goal. The gates themselves are not his to waive by that decision and stay: they are the site's
content rules and source rules.

## What it reads, and what it may not

May read: questions sent by the site's own visitors; Google Search Console and Bing Webmaster figures for the site (after
the senior author signs up); Wikipedia page views; Stack Exchange; official question pages (FRANK, ADF, NIDA); the forum
pages the senior author pastes; Crossref, Europe PMC, PubMed and OpenAlex for papers; open-access full texts.
May not: Reddit (closed to automatic reading; its programme for researchers needs a university affiliation, so it is
closed to an independent researcher: the draft in `docs/reddit-for-researchers-application.md` is kept and cannot be used);
any site that refuses; anything behind a sign-in or a paywall; Sci-Hub. Google gives nobody the questions people type: it
gives the searches that lead to one's own site (Search Console) and how often a word is searched.
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

- **Site 2.5.0: the site learns what people want without email** (`docs/STATUS.md` has the measurements). A public list of
  questions not answered yet (`data/site/wanted.json`, the page "On our list"); a typed question like a listed one is
  recognised on the visitor's device and counted by the item's number alone (`POST /api/want`; said on the card; off by a
  switch, by the browser's own wish, and where the store is off); "Tell me when it is answered"; the scout reads the counts
  and orders the list by them, and marks which sent questions are a listed one. And the rule for what is a question about
  drugs (`site/insight/scope.json`): a question that is not gets no promise of a check and keeps a quiet way to be sent;
  the scout lists every question sent that way, which is how the rule's words grow.
- **The paper finder** (`scripts/auto/papers.py`, `.github/workflows/papers.yml`; 15 November): for each question on the
  list, five searches of Europe PMC written down as they were sent, the papers that can be read in the order of reading
  (by meaning, reviews and studies in people first), and the reviews that cannot be read, listed with their Crossref
  references for the senior author (`data/auto/papers/`, `data/auto/papers-wanted.json`). No abstract and no passage is
  kept. Run for the 42 questions; a question searched by an older finder is searched again.
- **The models, and what they cost** (`scripts/auto/llm.py`): open models on Cloudflare Workers AI inside its free daily
  allowance (10,000 neurons; the lane stops by itself at 9,000 and goes on the next day), every call counted in
  `data/auto/lane/usage.json`. GitHub's own free models were retired on 30 July 2026. One answer costs some 550 to 850
  neurons, so the allowance writes about a dozen answers a day.
- **The lane** (`scripts/auto/lane.py`, `.github/workflows/lane.yml`): find, read (quotes that must stand in the passage,
  numbers that must stand in the quote), write, check by another model, the content rules in code, the gate on sources,
  the questions that wait for a person. Its first real run (15 November, 20:27 UTC) wrote four answers. The editor read
  them and found: papers named by a letter, words the site does not use, a But resting on a limit about something else,
  an opinion paper used as a source, and a checker that accepted too easily. So the lane got a number (2), the faults
  became rules, and the first four are not shown (`data/auto/lane/policy.json`): they are written again.
- **The exam of the checkers** (`scripts/auto/exam_models.py`, `data/auto/exam/model-*.json`): 31 cards known to be wrong
  and 50 known to be right. llama-3.3-70b caught 8 of the 31 and stopped 14 of the 50 (of 100 answers it lets through, 10
  are wrong: no better than no checker); mistral-small-3.1 caught 22 and stopped 34 (8.9 in 100); gpt-oss-120b gave no
  verdict within the room it was given. The senior author's goal is 1 in 1,000. A free checker of another kind (inference
  models run on GitHub's machine, `scripts/auto/nli.py`) is sitting the whole exam.
- **The site publishes itself** (`.github/workflows/deploy.yml`): build, the validator (no hard failure), the public build,
  the site's own program's tests, a real browser, and only then Cloudflare Pages. First done on 15 November at 20:28 UTC
  (`data/auto/deploy/deployed.json`). The senior author no longer uploads a zip.
- **The half-hourly look** (`scripts/auto/tick.py`, `.github/workflows/auto.yml`): is there anything to do, the work, the
  publishing. On its clock since 15 November 2026, 21:51 UTC (7 and 37 minutes past every hour). Its first work run read
  the question store, ran the scout and the item writer, and wrote its notes (`data/auto/lane/_last-auto-run.txt`). What
  it showed and what was mended the same hour: the publishing, called as a part of that workflow, did not publish and left
  no note (it is now a run of its own, started through GitHub's API); the lane began a question with too little of the
  day's allowance left and lost 563 neurons (it now begins a question only with room for one); the lane was started
  although no question had been listed.
- **Official pages** (`scripts/auto/official.py`, `data/auto/official/sources.json`, `.github/workflows/official.yml`): 22
  bodies listed; whether each can be read is found out on the machine that reads (`_probe.json`). Fifteen can be read, three
  refused and are left alone, four give nothing to a reader that is not a browser or did not answer (`docs/STATUS.md`,
  2.7.0). The index holds addresses and titles only; for each listed question the pages that speak about it are named.
- **Site 2.6.0** (`docs/STATUS.md`): answers written by the system as a visitor meets them, each publishing with a stamp of
  its own, kept questions asked again at every publishing.
- **Lane 3 and site 2.7.0** (15 to 16 November): official pages and the summaries of paywalled reviews as sources; answers
  about amounts (decision 11); the second look's first part (an answer that is not complete is written again; its history
  is kept); the item writer (`scripts/auto/ask.py`: a visitor's question becomes a question on the system's own list, in
  our words); the half-hourly clock is on (`.github/workflows/auto.yml`). None of these has run with a real model yet.
- **The first real answers of lanes 3 to 5, read by the editor (16 November 2026, 00:46 to 01:54 UTC).** All numbers are from the runs' own notes and the day's ledger (`data/auto/lane/usage.json`).
  - *Lane 3* (00:46): three questions, no answer, 3,382 neurons. The writer (gpt-oss-120b) reasons for some 1,300 tokens before it writes and had room for 1,400: its answer was cut off before it began, three times for each of two questions; the third draft held an amount. The editor paused the lane (`pause` in `data/auto/lane/policy.json`).
  - *A trial of writers* on that very prompt (`scripts/auto/trial.py`, `data/auto/exam/writer-trial.json`): llama-3.3-70b gave a draft in the right form in 174 tokens (112 neurons) and named each source properly; gpt-oss-120b, given room for 3,000 tokens, wrote the fullest answer and named papers by a letter; mistral-small-3.1 invented a limit. So llama-3.3-70b writes and gpt-oss-120b, which reasons, is the second reader, with room for both its reasoning and its answer.
  - *Lane 4* (01:27): the reader's third gate (a sentence must be carried by its quote and passage), two papers in full and a third only where needed, three findings of a source to the writer. Three questions, three answers, 2,049 neurons, six minutes. Read: "Can you get addicted to ketamine?" was true in every sentence and did not say yes ("People with ketamine use disorder experience abstinence symptoms ..."), with a But about how well treatments are studied. Psilocybin amounts: one row was a weight of dried mushrooms worked out from a study's amount, and two rows showed the weeks between two sessions. Alcohol amounts: a level in the blood stood as an amount, and 27 items had been thrown away with no record of why. The second reader refused six misattributed rows, each with an exact reason.
  - *Lane 5* (01:48): rules for each of those, and every item thrown away kept with its reason (`looked` in each record; `python3 -I scripts/editor/read_auto.py --all`). The same three questions, three answers, 2,285 neurons. Read: the ketamine answer begins "Yes, people who use ketamine can become dependent."; the writer's But was about treatments three times, the second reader said so each time, and the code wrote the But. The reasons showed what the alcohol answer had lost: the NHS's 14 units and Ireland's 11 and 17 standard drinks (the reader had called them "the weekly low-risk guideline", words that are not in the passage, and a gate held that against it); the CDC's and NIAAA's amounts, written as words ("two drinks or less in a day"); Canada's amounts for men (a limit of three rows a source). Psilocybin: eight rows, each true to its source's words; one trial's very low amount stood without its high one (the same limit).
  - *Lane 6* has a rule for each of these and has not run: 480 of the day's 9,000 neurons were left. Nothing of lanes 4 to 6 is shown (`show_from_lane` 7, `amounts` false), and the lane's clock stays paused until the editor has read lane 6's answers.
  - *Not measured*: gpt-oss-120b as second reader on the exam. It had been given 220 and then 700 tokens and gave no verdict on any of 81 cards; the exam now gives it the room the lane gives it, goes on where it stopped and leaves 700 neurons a day for the site (`scripts/auto/exam_models.py`). At about 70 neurons a card it costs more than half a day's allowance.
- **The second free service at work (16 November 2026, from 16:00 UTC).** The senior author added the key (`GROQ_API_KEY`); the first run answered a question with no Cloudflare neurons. Teams as they stand (`data/auto/lane/models.json`): team C: llama-4-scout reads at Cloudflare (gpt-oss-20b at Groq when Cloudflare's day is used up), gpt-oss-120b plans and is the second reader at Groq, qwen3.8-27b writes at Groq; team B: llama-3.3-70b writes at Cloudflare. Lanes 6 to 9 were each run for real and read (see `docs/STATUS.md`); lane 9 adds the plan (`make_plan`): the planner chooses the items, writes no sentence, and the writer gets only those items. `show_from_lane` is 9 and one answer is shown; `amounts` and the clock wait for a batch read after 00:00 UTC.
- **GitHub's clock is late or silent** (measured 16 November, 00:00 to 01:30 UTC): of the looks due at 00:07, 00:37 and 01:07, the first two never ran and the third ran at 01:20. A look started by a request file ran within a minute each time. A page must not promise "within the hour" on such a clock (`loop` stays false). Two ways out, both the senior author's to decide because each needs his hands once: the site's own program starts a look when a question arrives (it needs a GitHub token kept as a secret in Cloudflare), or the repository is made public (GitHub then gives unlimited machine time, so looks can be scheduled four times as often).
- **Other free services for models, looked up on 15 November 2026.** Groq, from its own page
  (console.groq.com/docs/rate-limits, read 15 November 2026): `openai/gpt-oss-120b`, `openai/gpt-oss-20b` and
  `qwen/qwen3.8-27b`, each 30 requests a minute, 1,000 requests a day, 8,000 tokens a minute and 200,000 tokens a day, for
  an organization; no card according to klymentiev.com (checked 11 September 2026; Groq's own page does not say). Mistral: no card; its free mode publishes
  no limits; texts may be used for training unless switched off (aifreeapi.com, 9 October 2026). Cerebras: a card is
  required since 2026 (toolfreebie.com, 9 October 2026), so it is not free in the senior author's sense. With Groq and
  Mistral the lane would have about three times the room and a checker of another family; both need the senior author
  to open an account and add a secret, which is his to decide.

## Not built yet (in this order, after the senior author's words of 22:24 to 22:55)

1. Lane 6's first real answers read by the editor (after 00:00 UTC on 17 November, when the day's allowance is new, or
   the same day once the Groq key is there); then `show_from_lane` 6, `amounts` true and the pause taken off, each only
   if what was read is right. With the key: first the exam of the second readers at Groq, which decides the team.
1a. Built on 16 November 2026: the plan step (lane 9); the comparison with the checked claims of the same page (lane 10,
   not yet run for real); the site showing each answer on its home page and the pages the system starts (site 2.8.0,
   decision 22); the system's own questions (decision 20); the exam made of the lane's own sentences, judged by the
   editor, and the exam of plain lines (decision 25). Still open: the editor's worked answers as examples for the
   writer (decision 17).
2. A checker good enough for the goal. Sat on 16 November 2026: gpt-oss-120b at Groq (5 of 31 wrong cards with the
   faulty low effort; 5 of 11 with medium, 2 of 11 good ones stopped). Next, in this order: the same reader with high
   effort and with a short list of yes-or-no questions (same people? same thing counted? a cause where the source
   links?) instead of one verdict; two different readers that must both accept (built: a team's further readers,
   decision 25; which readers, the exams say); the models of the two free services he opened on 16 November (Google AI
   Studio, OpenRouter: decision 24). No paid model: he chose our own (decision 23).
2a. Our own checker, step two: training on our own record. The material: the three exams' real faults (22 faulty
   sentences on the cards, 56 plain lines, the lane's own sentences), the good sentences beside them (some 1,200), and
   made-up wrong sentences of the kinds our checkers have named, written by the free open models from our good ones
   and kept apart from the real ones, which alone are the measure. Then our own reader, then our own writer.
3. The loop seen to work for a question a visitor sent (sent, listed, answered, published, green on the visitor's device),
   and its time measured; then the page may promise it (decision 13, `loop`).
4. "At least part of an answer" measured (decision 14), and the page pointing to the nearest part of a drug's page when it
   has no answer.
5. The second look's other parts (decision 12): a source retracted since; the system's criticism of checked claims.
6. More official bodies: the ones that give nothing to a plain reader, and pages in other languages.
7. The page for the senior author: everything the system wrote, each taken down or released in one tap, and the papers it
   wants (decisions 6 and 7).
8. What people look for elsewhere, from every free source that allows reading: Wikipedia's page views by drug (built,
   decision 19), official question pages, the site's own searches through Google Search Console and Bing (after the
   senior author signs up).
9. The photo finder.
