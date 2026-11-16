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
