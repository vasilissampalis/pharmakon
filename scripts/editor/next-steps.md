# The editor's next steps (a working note, kept in the repository so that it survives a reset)

Written 17 November 2026, 10:35 UTC (12:35 Athens), brought up to date 12:00 UTC (site 2.9.2), by the AI co-editor for itself. Not a decision of the senior
author; nothing here lets anything out. The state it starts from is the newest entry of `docs/STATUS.md` and
decision 26 of `docs/AUTOMATION.md`.

Rules that stand: nothing new of the system's is shown (`hold_new` true, `amounts` false, the lane's clock paused,
`show_from_lane` 9) until the editor has read it and it reads clean. Requests go one after the other. Commit and push
after every step. `mkdir -p data/auto/requests` before writing a request.


## What the senior author asked for on 17 November, 16:33 to 17:26 (decisions 28 and 29 of `docs/AUTOMATION.md`), in this order

Done: places by meaning (2.13.0); figures by question (2.14.0); the lane's pause, retry and finder; site 2.15.0 (every
citation a link, a source in place, plain first, shorter cards, topics, the same Insight on every page, the place and
the way back in the bar).

00000. **When the site does not have the answer, and when it only thinks it has (decision 33; site 2.22.0, 18 November, 22:15).** Done: a part of
   the Big questions page is never the answer; who uses more is drug talk; an answer silent on dying, or about a narrower case than the question,
   never answers a question about dying; the unsure best match (under 0.8) gets research and official pages under it; "Not what you asked? Search
   wider" (the question read as not answered, sent with which answer it was); one layout for an unanswered question (line, jumps, figures, closest
   answers, research, official pages); research by title for questions of fact about dying; official pages as links (`OFFICIAL`). In the lane: a
   stand-by reader without room no longer ends the day; the finder asks for the place a question names. Next, in this order:
   (1) **Trial 14** (`data/auto/instant/`): read every line of the death questions' titles (are they about the question? is any title an
   instruction or an amount?) and of the general ones (women and men; overdose with no drug). Tighten key words where a list is off.
   (2) **PubMed as a second index**: his words of 22:15 ("access to all scientific paper platforms"). Read on 18 November 2026 on NCBI's own page
   (https://www.ncbi.nlm.nih.gov/books/NBK25497/): without a key, three requests a second from one address (more gets an error, "API rate limit
   exceeded"); with a key, ten; NCBI asks for `tool` and `email` on every request (the site's public address, contact@pharmakon.world) and blocks an
   address that breaks its rules. The site's server shares its outgoing addresses with other sites, so "three a second" may be used up by others: a
   refusal there is "the index did not answer", never "nothing found", and Europe PMC stays beside it. A key is free and would be his to make (a
   secret at Cloudflare, never pasted to the editor); start without one. A search is two requests (esearch for the numbers, esummary for titles,
   journals and years). Design: the page asks `/api/find` once per index (`src`), each request with its own budget of fifty outgoing calls, the
   lists joined on the device by DOI or PMID as they come; titles only from a new index until a trial of the words has been read; the Privacy text,
   the Methods text and the rule in CLAUDE.md name the index BEFORE it is asked.
   **OpenAlex** (wider than medicine: social science, policy) needs a key since 13 February 2026, with a free daily allowance (read on its own
   pages on 18 November 2026): his to make, like the others; only where its free plan can never bill. **Crossref** (free, no key) after PubMed.
   (3) **The scout reads `x`** (the answer a reader said is not theirs): such a question is not "answered" for the scout even where the judge says so;
   it gets an item of its own (our wording), and the item records which answer it is not. Then the page: a listed question that is nearer than the
   best match wins over it.
   (4) **A sent question that an existing answer does answer becomes a wording of that answer** (our wording of it, never the visitor's): the lane's
   model reads the question against the nearest answers. Measure on the gold set what it adds; this is also how the pair model gets its examples.
   (5) **The pair model** (`scripts/insight/pair.py`): teach it first on an open set of questions that mean the same (on GitHub's machines), then on
   ours; ship only if, on the gold set, it keeps at least 20 of the 23 full best matches while taking away the partial and the wrong ones.
   (6) **Free model calls that need no key: none found.** GitHub's own Models service was the candidate (a workflow's own token, no key to make):
   its page says it was retired on 30 July 2026 (read 18 November 2026). So more answers a day come only from the services already in use (their
   days turn at 02:00 Athens for Cloudflare, 10:00 for Google) or from a further free service whose key he makes. What the lane can do by itself:
   spend less a question (the reader took most of the neurons), and never lose a day to a stand-by (mended).
   **Read on the services' own pages on 19 November 2026 (01:00 Athens), for the keys he could make:**
   - **Mistral** (already wired: `llm.SERVICES`, the secret `MISTRAL_API_KEY`, in every workflow). Its help page: the "Experiment" plan is free, "No
     credit card is required", "All you need is a verified phone number", and requests under it "may be used to train Mistral's models" (we send only
     our own wording and passages of public papers and pages: never a visitor's words). Its documentation: "a free API tier with restrictive rate
     limits"; the numbers stand in the console (console.mistral.ai/limits) and are his to read out, as he did for Google's table. No model of it may
     work in the lane before it has sat the exam for its role (`scripts/auto/exam_models.py`; `data/auto/requests/exam-*.json`).
   - **SambaNova** (not wired yet: an entry in `llm.SERVICES`, a secret, the workflows). Its documentation (docs.sambanova.ai, Rate Limits Policy): a
     free tier that is "Applied when there is no payment method linked with your account": for each model 20 requests a minute, 20 requests a day and
     200,000 tokens a day; among them `gpt-oss-120b` (the lane's best second reader: what runs out first every day), `DeepSeek-V3.1`,
     `Meta-Llama-3.3-70B-Instruct`, and as previews `DeepSeek-V3.2` and `gemma-4-31B-it`. Twenty calls a day of gpt-oss-120b is the second reader
     and the planner for four to six more answers; the DeepSeek models are candidates for the strong further reader's place, after an exam.
   - **Cerebras: no.** Its own rate-limits page: access stays inactive until a verified payment method is added (a "Free Trial" with credits). That is
     against his rule ("no billing, paid subscriptions, credit purchases or unexpected charges").
   (7) His question of 22:10 (`w_a0015`, deaths from heroin in one country): the finder now asks for the country; read what the next run finds. A
   figure for one country belongs to the statistics page, from the body that counts it: that needs readers ("use readers").

0000. **Answered by itself, within minutes (decision 32; lane 19; site 2.21.0, 18 November).** Done: the lane tries again by itself and parks
   nothing for a reader; the stricter bar for questions where a wrong word can hurt, in the place of a person; the look every five minutes
   with a first pass for sent questions that is published in the middle of the run; the server's own start of the work (needs his key);
   "Your questions" behind one line, the panel, past searches kept by themselves; research by title for pregnancy, children and questions
   that name no single drug. Next, in this order:
   (0) **The key: done and tested** (18 November 2026). He said "done, no expiration" at 20:34: the key (`pharmakon-start`) does not run
   out by a date; GitHub takes away a key that was not used for a year, and this one is used whenever a question arrives. Tested at 20:50:
   a new question started a run four seconds later (decision 32). A key that GitHub no longer takes shows in the publishing's notes
   as "GITHUB DID NOT TAKE IT AT THE LAST START (refused 401)": then he makes a new one the same way, same names. Never ask him for the
   key, never have it pasted anywhere but the Cloudflare field.
   (a) **Read the first real answers that went through the stricter bar** (the state says "passed every gate, and the stricter bar for an
   answer about ..."; `gates.stakes` in the record). Every one, sentence by sentence, against the words it rests on. If one plays a danger
   down or tells a reader what to do: hold it (`data/auto/held.json`, with "lane" and "say"), find which of the four looks let it through,
   and tighten that look; if two do in the first ten, set that kind back to "person" (`policy.json`, stakes) and tell him.
   Read so far: `au_w_a0011` (mothers and their children's drug use; it stays; decision 32). What it showed, to mend: a "How do we know"
   line that breaks a rule (the source's own word "abuse") is left out, and the short answer's sentence that rests on that source then
   stands without its line: write such a line again (as the short answer is), and where it still cannot stand, take the sentence that rests
   only on that source out of the short answer.
   Also read (decision 32): `au_w_a0010` (kanna and anxiety: stays) and `au_w_a0013` (kratom: held, written again). Rules they call for,
   each measured on the lane's own sentences before it is switched on: an opening that PROMISES a benefit ("It can help", "Yes" to "does X
   help with Y") only where a source read in full studied people who have Y (the mirror of the rule for an opening that denies a danger); a
   But that speaks of a study must have that study's line beside it.
   (b0) **Read first, 19 November:** `data/auto/lane/_last-auto-run.txt` now carries each step's time: where did a run's minutes go? And
   `w_a0014` ("Does caffeine affect growth?", the first question that started a run by itself): written after the allowance came back? If it
   is published, read it as the editor (it is about children's growth: the stricter bar). The six questions whose searches were mended are
   searched again by themselves: look at what their new searches hold (`data/auto/papers/w_a00*.json`).
   (b) **Measure the times and only then let the page promise them.** For each question a person sent: when it arrived (the store's day is
   too coarse: use the run that first listed it), when its answer was kept, when it was published (`data/auto/deploy/`). `policy.loop` goes
   true, and the page says "usually within N minutes", only when twenty sent questions in a row kept that N. Until then the page promises
   no time.
   (c) **Make a run shorter now that the key is there** (he asked for seconds; the start is seconds, the writing minutes). Done on 18
   November: a working run gives way to a run that waits (decision 32). Read in `data/auto/lane/_last-auto-run.txt` whether it did ("left to
   the run that is waiting"). Not done, and the next real gain: two runs at once (a lane of its own for a question that just came) needs
   question numbers that two runs cannot give twice (`ask.py` counts them: make the number from the fingerprint). In order of what else
   saves time: the look and the work as one job for a run the server started (some 45 s); the Python packages kept between runs
   (`actions/cache`, some 20 s); the scout's build only where the site's sources changed since the kept index; the publishing run without
   fetching a browser when only the lane's answers changed (the smoke check is then the one thing skipped: decide with the numbers).
   (d) **The further readers.** Gemini 3.6 Flash read every answer of the first runs and refused, with reasons, six sentences that said a
   little more than their source: it is the strong reader now (20 calls a day; 3 Flash stands behind it). Watch `panel` in the records for
   "could not be asked ... it began:" (the first 90 characters of a reply that could not be read are kept now). If the day's calls of both
   run out before the writers' allowance does, ask for one more key of another free service rather than a weaker reader.
   (e) **The two new kinds of question** (titles only now). The eleventh and twelfth trials are read (decision 32). Words under the
   titles of these kinds: only after a trial that reads every line; for pregnancy and children titles only stays, unless he says otherwise.
   From the twelfth and thirteenth trials (both read; decision 32): the key words are done (site 2.21.2). Still beside the question, each
   to be changed with a trial behind it: (1) the name "addiction" still lets "oncogene addiction" through beside the word "drug": name the
   titles to leave out (oncogene, oncogenic, tumour, tumor, cancer, food, internet, smartphone, gaming) in the server's search for that
   name; (2) for a question that names no drug, a key word with other senses ("creative", "cognitive") found anywhere in a review brings
   reviews on anything: try both searches with the key word in the TITLE; (3) "smarter" as "cognitive": a better word, or none. Run the
   next trial when Europe PMC is fast again (a morning), so that its times mean something. Add "does caffeine stunt your growth" to it:
   on the live site its list held a paper on tumours and one on prostate cancer ("growth"), beside two that were on it.
   (e2) **A second index for the hours when Europe PMC is slow** (18 November, afternoon: 25 seconds a search; site 2.21.1 made the page
   patient and truthful about it, not fast). PubMed's own interface (NCBI E-utilities: no key needed at a few requests a second; search,
   then the records with their summaries) asked beside Europe PMC, the first that answers gives the list; no "most cited" order there, so
   the order needs thought (reviews first, then PubMed's best match). The rule that picks a paper's own words reads the end of a summary:
   PubMed's summaries have the same labelled parts, but a trial on our own questions comes before any word from them is shown
   (`scripts/auto/instant_trial.mjs` takes a second source easily: it calls the worker). Read NCBI's usage rules first.
   (f) **His own question "Does cannabis cause cancer?"** waits on his word "approve" for `cl_can_smoked_cancer` (Section 7). Do not
   adjudicate that disagreement in `agreed.json`: the claim is under his gate.
   (g) **The exam of the lane's own sentences** has the six answers the editor read on 18 November and did not let out (the reasons are
   in `held.json`): judge their sentences in `scripts/editor/label_auto.py` so that the rate of lane 18 is on file before lane 19's.

000. **By itself, at once, understood (decision 31; sites 2.16.1 to 2.20.0, 18 November).** Done: research by itself; the place a count
   names; the calm line while Insight starts and the warm start; "Insight" alone under the bar; the question sent by itself with the reader
   told, its words kept out of the repository; and, since 2.20.0, each paper's own words on the question by FIXED RULE under its title, with
   NO LANGUAGE MODEL anywhere in it (two trials with the real model and seven without: `data/auto/instant/`), and a list that comes within
   about a second although Europe PMC lets one request in three hang. Nothing waits on him for this: the Workers AI binding is not needed.
   Next, in this order:
   (a) **Read the publishing's own lines after every publishing** (`data/auto/deploy/_last-run.txt`, "server:", `scripts/auto/live_check.py`):
   twelve of our questions on the real site, each with its time, each search's time at Europe PMC, which asking answered, and whether the
   list was given without the most cited; then the first question once more ("from what was kept"). With 2.20.1 (05:36): 0.3 to 1.2 s, the
   middle one 0.9 s, about 0.3 s of it the publishing machine's own connection. If that drifts, the timings in `findPapers` (`FIND_A`,
   `FIND_B`, `FIND_GRACE`, `FIND_SOON`) are the place, with a trial before and after.
   (b) **Faster still, if he wants it.** What is left is Europe PMC's own time for a search nobody asked before (0.6 to 0.7 s from the
   site). Two ways, each at a price: ask Europe PMC twice from the start (two more requests to a public service for every question); or
   let the page ask 0.3 s after the last key instead of 0.7 s and show the list when the question still stands (more searches for
   half-typed questions). Neither is done.
   (b2) **More papers with words, without saying more.** Most sentences are lost to the limit of 15 words (trial 8 holds the shapes of 157
   of them, never their text). What can still be mended is in those shapes: a run that ends before "and suggests that ..." without a comma;
   "X, daily use is also associated with ..." (a list at the start). One class at a time: a test, then a trial, then read every line.
   Never the limit itself, and never a gate (`CLAUDE.md`).
   (b3) **The lines that are true and beside the point** ("The correct therapy for cocaine cardiotoxicity is not known", under "does
   cocaine damage the heart"): a rule cannot tell. Count them in the next trial; if they are more than one in ten, show words only where
   the paper's TITLE holds the question's key word.
   (c) **The United States' figures.** "how many heroin deaths in america" is now told the truth (no figure for the United States here), but the
   figures are still missing: the site's US file holds the household survey only. Deaths by drug are in the CDC's own tables (NCHS data briefs,
   CDC WONDER). They enter like every figure: read at the source by one reader, checked by another. That needs his "use readers", or the
   machine lane's official finder, which holds a question about dying for a person. Ask him.
   (d) **The same on a started page and behind "See what we have so far"**: the papers, each with its own words, for a question that waits.
   (e) The lane's writer gave "no JSON" for kanna twice on 17 November: read its raw reply in the answer's record and let the lane ask once more
   in the form.
0. **His sent questions (19:38: "they are hours pending this is disappointing").** Kanna is first in line with 12 papers that can
   be read: read what the lane writes (`data/auto/answers/au_w_a0002.json`). *Mitragyna javanica*: nothing that can be read was
   found; the two papers the finder saw are in `data/auto/papers/w_a0003.json`: if he can save them, ask him with the full APA 7
   references. Cocaethylene: the lane's own answer (`au_w_a0005`, waiting for a person) says "25-fold higher risk of sudden
   cardiac death": read its sources against our checked answer before anything is shown. The scout should know that a question
   about two drugs together is answered by the checked answer on the pair (the page does from 2.15.2; the build's ranker does
   not), so that such a question is not listed again.
1. **The lane, when the allowances are new (00:00 UTC).** Read what it wrote for kanna and *Mitragyna javanica* and for
   the 46 questions never tried (`data/auto/lane/_last-auto-run.txt`, `data/auto/lane/state.json`). Compare team I (a
   free reader) with team H: does "rests on too few sources" come more often? If so, team I goes behind team H. Try
   team K by name on two questions (`data/auto/requests/trial-*.json`, `"team": "team K"`): Gemma reads, plans and
   writes. If its drafts pass as often as qwen's, put it second. Measure a rule for "an effect said where the source
   reports what people say" on the exams before adding it (an earlier, wider rule stopped 12 good cards for 2 wrong
   ones); then let the lane rewrite `w_0048`.
2. **The school** is built and runs every day (decision 28; `data/auto/language/report.json` is its own account). Next
   lessons, in this order: (a) **everyday words with a letter wrong**: "is ketmine adictive" finds nothing, because only
   drug names are corrected. **Measured on 17 November, 19:50 (a trial, nothing shipped):** the plain rule (a word the
   model's word list does not hold, five letters or more, with exactly one word of that list one letter away) reads
   "overdoze", "adiction", "withdrawl", "tolerence", "paranoya", "anxeity", "dangrous", "simptoms", "posible" rightly,
   but it also changed 7 good words in the 1,021 forum questions, because the list of 30,000 words lacks them: "inhale"
   to "inhaled", "irritate" to "irritated", "airway" to "airways", "purer" to "pure", "purify" to "purity", and
   "salivation" to "salvation". So it must not ship as it is. Two guards to build and measure: (1) never a change at the
   end of the word (an ending is not a typo: this stops the first five); (2) only toward a word the site itself uses (its
   questions and short answers: the word index of the answers), and never away from a word that real questions use (the
   school can keep the words it has seen three times or more: a new table, "words"). It missed "adictive" and
   "halucination" (the drug-talk pattern takes them before the rule is asked: let the rule read them first). Then
   measure again on the forum questions and on the school's real questions: no good word changed. Page and build must
   read the same (parity). (b) **more language**: the web client reads the first 6 MB of a file, so the same
   61,898 questions every day: read the rest (a larger room for this one reader, or a part of a file), and add open
   collections whose licence has been read (`data/auto/language/sources.json`). (c) the two smaller errors its report
   names ("which drug?" for a question of everyday words that is about something else; a last word taken for one still
   being typed).
3. **The two sides of the 32 debates in plain words** (`data/site/simple.json`, a claim's `sides`: `yes`, `no`, `read`,
   `yes_src`, `no_src`; the page shows them when `yes` and `no` are there). One line each, from the checked debate
   text only; every line read blind (`scripts/auto/blind_lines.py` reads a claim's statement: it needs a small change
   to read the debate's parts); the editor adjudicates. Until then the box says "Studies point different ways on this."
4. **A plain line for what a source found**, for sources that no plain line of the answer rests on (now such a source
   shows its kind of study and its link, and the findings only under "Scientific detail").
5. **Four citations code cannot decide**: "Hollander et al., 1995" in `cl_coc_chest_pain_mi` (three works of that year:
   which letter?); "Harris et al. (2003)" in `cl_mix_cocaine_alcohol_drunkenness`; "Strickland et al. (2021)" in
   `cl_xc_mindset_before`; "Ruberto et al., 2021, as described" in `cl_can_chs_dopamine_antagonists`. Through the
   checks, not by hand.
6. **Old phones**: done in 2.15.1 (no look-behind in the page's script; the build refuses one). Not tried on a real
   phone with iOS 15: if one is at hand, open the site on it.
7. **The bar on a phone** takes 58 px for Insight and the way back, above a drug page's 60 px of parts. If that proves
   too much, let it slide away on the way down and come back on the way up (the jump code must then know its height).
8. **The pictures fetched at 15:33 UTC** (`pictures-0004`): look, hold or pass; then a judge of pictures in code.
9. The older queue below: step f (Myth or fact cards by the system), step c (one list on phone and desktop), step e.

## Waiting for the senior author (asked 17 November, 12:30 Athens)

1. **"approve"** for the Section 7 answer `cl_can_smoked_cancer` (*Does smoking cannabis cause lung cancer?*), the
   checked answer to his own question "does cannabis cause cancer". Only on his word: at 12:37 he wrote "do a perfect
   job i don't need to approve anything if it's the best possible development"; the editor's attempt to write that
   into the rules as passing the Section 7 gate by itself was stopped by an automatic safety filter, twice, and by the
   project's rule was not retried or reworded. The gate stands. His approval of an answer is his word "approve" for
   that answer. Its nine plain lines are read again and all hold (`data/auto/blind/cl_can_smoked_cancer.json`). Then:
   - the plain lines he had on his to-do page are in `data/verification/s7-review-2026-11-13/s7_on_todo_page.json`
     (its `v` 0.5.3, `rewritten`); the claim in `data/claims/cannabis.json` is 0.5.2. Check in `data/verification/`
     that those plain lines were blind-checked; if they were not, they are checked before anything is shown;
   - bring the lines into `data/site/simple.json`, the claim to the version he reviewed with a changelog line, and
     record his approval in `data/verification/senior-gate.json` with his words and the time he gave them;
   - `scripts/snapshot_published.py`, `python3 -I scripts/validate.py`, build, the page checks, a deploy request;
   - 37 more Section 7 answers wait the same way (the list: every claim of section 7 whose version is not in the gate).
2. **The PDF** of the 2026 meta-analysis that the system found and the checked answer does not know yet (ask after
   step 1, one step at a time): Karimi, M., Kazemi, K., Pourhanifeh, M. H., Irajian, P., & Asbaghi, O. (2026).
   Marijuana (cannabis) smoking increases the risk of lung cancer: Evidence from a systematic review and
   meta-analysis. *Addiction and Health, 18*, 1710. https://doi.org/10.34172/ahj.1710 (reference from Crossref).
3. **"keep them private"** (asked again on 17 November, 14:55; no answer yet; the editor's own note of 12:55 UTC to do it
   without his word is withdrawn: it is his to weigh, because the plain report of what people ask in their own words,
   which "demand first" rests on, would leave the repository with them): the scout's files with the questions people sent (`data/auto/questions.json`,
   `data/auto/report.json`, `docs/MISSING.md`) are in this public repository. If he says so: the words stay in the
   store alone; the repository keeps our wording, the counts and a fingerprint (scout.py, look.py, ask.py, and the
   three files taken out of the repository's history is his call too).
4. Still open from before: "no Google"; whether the system may change a checked claim (now: never).

5. **"use readers"**: the second reader for `MDMA/Vrolijk_2017_OnlinePillReportsSafety.pdf` (saved 17 November) and for any
   other paper of the checked lane. Readers on his plan run only when he asks.

## What the senior author asked for on 17 November, 12:56 to 13:45 (decision 27 of `docs/AUTOMATION.md`), in this order

Done since: step a (names looked up and kept, site 2.9.3; watch `data/auto/names/learned.json` after each half-hourly
run and read every learned name), a first step of d (the first screen is Insight, site 2.10.0), every place can be asked
for (2.11.0), and step b (site 2.12.0: pages people asked about in a drug page's form, with pictures). Next: f, then c,
then e.

Step b, what is left (in this order):
1. **Look at every newly fetched picture** (`data/auto/pictures.json`: a "file" without "looked_by_editor" is not shown).
   `python3 -I scripts/auto/pictures.py looked <day> <names…>` and `… hold <name> "<why>"`, against docs/WRITING-RULES.md
   "Photos" (never people or hands; the thing itself; nothing else that takes the eye; no writing over it). A fetch was
   asked for on 17 November in place of the six held ones (`pictures-0003.json`).
2. **A judge of pictures, so that this runs without the editor**: a free model that takes pictures (Google's free tier
   through `llm.py`, or a Cloudflare one), asked for JSON only (people or hands? writing or a mark over the picture? is one
   plant or fungus the clear subject?), on the web copies (made by Pillow in the job without keys, so no outside bytes
   are decoded where a key is held). Measured first on pictures the editor has judged (the 12 of 17 November are too few:
   fetch and judge more), with the numbers written down; a picture is shown without the editor only if the judge is
   seen to let no held picture through. Until then the editor's look is the gate.
3. **The system's own list in the page's index of listed questions** (so that "can i get high with kanna" is told
   "Not answered yet. A question like yours is on our list: Does kanna have psychoactive effects?"): `site/build.js`
   gives the index only `data/site/wanted.json`; adding `data/auto/wanted-auto.json` changes what Insight says, so
   measure first (`build_index.py --eval`). Today only the same words are matched, on the started page's own list.
4. **A question asked on a started page is about that page** ("is it addictive" on the kanna page): the box's context
   is a checked drug page only. Needs the page's name carried with the question to the store and the scout.
5. **Page and species held together by a source**: the species under a filed page's name is the filing's own title;
   GBIF's common names for the species (`species/<key>/vernacularNames`) could confirm it by code.
6. **Other forms and other pages**: GBIF holds the living plant only. Pictures of a dried plant, a powder or a capsule,
   and pictures for pages that are not a plant or a fungus, need a store that allows a program (none of those probed
   does) or the editor's own search with each licence read at its source, as for `data/site/photos.json`.
7. **Pictures on file are never looked for again** (`find` skips a species it has): when every picture of a species is
   held, find has to ask GBIF again, past the records it already saw.

Done in site 2.9.2: the readings "open" and "verb", short forms, a name of two words we do not know, the routes by
country (the law, emergency numbers, drug checking), the line for a question not in English, two-word beginnings, a
question already sent, the newest of the reader's questions first.

a. **Names the system does not know, looked up online and kept** ("mytragina javanica" is *Mitragyna javanica*; "hardcode
   is not enough"). In `scripts/auto/names_open.py` (the job that holds no key; robots.txt obeyed through
   `official.Web`; a probe first, as for RxNorm): for each unknown word or pair of words that the scout saw in a sent
   question, ask the open name services that allow it. Candidates to probe: GBIF's species match
   (`api.gbif.org/v1/species/match?name=…&verbose=true`, fuzzy, for plant and fungus names), RxNorm's approximate term
   (`rxnav.nlm.nih.gov/REST/approximateTerm.json`), PubChem's autocomplete and synonyms (`pubchem.ncbi.nlm.nih.gov/rest/`),
   NCBI's spelling suggestion (`eutils … espell.fcgi`). Keep what is found in `data/auto/names/learned.json`: what was
   typed, the name, its kind, the service and its record, how sure. The build reads the table: the name counts as a drug
   we do not cover yet (scope), the typed form is read as the name ("We read “mytragina javanica” as Mitragyna
   javanica"), and the name is a candidate for a page to start. Only a visitor's unknown WORDS go to a name service
   (a word or two, never the question), and only words that are not in the model's word list. Measure before it is
   switched on: no word of the 1,021 forum questions may be "learned" as a name.
b. **Pages for drugs without one** (kanna, *Mitragyna javanica*), "in a perfect coherent format to the rest of the
   website", with pictures. What the probe of 17 November found for pictures: Wikimedia Commons' search, iNaturalist's
   and Openverse's addresses are not allowed by their robots.txt (not asked, not gone around); **GBIF's records with
   pictures are allowed** (`api.gbif.org/v1/occurrence/search?mediaType=StillImage&scientificName=…`: 169 records for
   *Sceletium tortuosum*), each picture with its own licence, creator and source in the record: take only CC0 and
   CC BY (never NC, never ND, never SA), fetch the file only if its host's robots.txt allows it, keep the record
   beside the file as `data/site/photos.json` does, and show "Picture not yet checked by a person" until the editor
   has looked. Plants and fungi only; pills and powders have no such source yet. A learned name needs its filing
   (`data/auto/filing.json`: by kind, plants and fungi under "Other plants", medicines under "Medicines") so that
   `scripts/auto/place.py` starts its page. Seen at 12:07 UTC: the run listed his questions by itself
   (`w_a0001` *What is the legal status of drugs in Greece?*, `w_a0002` *Does kanna have psychoactive effects?*), found
   papers, and the lane wrote nothing that passed (kanna: "no source that can be read gave a finding"): the page
   shell and the pictures can come before the answers do. The system's pages exist (site 2.8: `AUTO_PAGES`, `#auto/p-<slug>`, decision 22); what is
   missing is the site's own page form for them (what it is, forms, effects, risks, the law, each from the system's
   answers under their label) and pictures: Wikimedia Commons through its API only if its robots.txt allows the
   address (else not), licence read from the file's own record (public domain, CC0, CC BY; never CC BY-SA unless the
   site's photo rule is changed by him), with a line "Picture not yet checked by a person" until the editor has looked.
   Pictures also for existing pages that lack them (`data/site/photos.json` says which have one). `hold_new` stays
   true until the lane's answers read clean; the page shell and the pictures do not depend on it.
c. **One list on phone and desktop without an account**, "as easy as it is now". A private link and a QR code made on
   the device: a random key in the address's fragment (never sent to a server), the list encrypted with it in the
   browser (WebCrypto AES-GCM), the store keeps only the ciphertext under a name derived from the key
   (`site/worker/_worker.js`: `api/list`, a size limit, kept 180 days). Opening the link on the other device joins the
   two lists. The text under "Your questions" then says so in plain words. The QR code is drawn by a small encoder
   kept in the repository (no outside script).
d. **Insight looks like what it is**: "it should be apparent visually that pharmakon insight IS the way to use and
   develop the site … it has to feel different look different our search engine has to feel like a drug". The start
   page's first screen becomes Insight itself (its own name, its own surface, what it can do in its own words:
   answers, the law by country, emergency numbers, drug checking, mixing), designed with the frontend-design guidance
   and looked at in screenshots at 390 and 1280 before it ships.
e. **What the site needs, found by itself**: a standing report made by the half-hourly run (pages without pictures,
   drugs asked about without a page, sections no question reaches, questions that end at "we haven't checked"), from
   which the system starts work without being told.

f. **The system makes Myth or fact cards by itself** (the senior author, 17 November, 15:25: "our ai has to make new myth
   or fact questions based on what real users search online constantly --- the myth or drug claims have to be perfectly
   incorporated to the drug pages and in all other relevant pages … if there are no such pages they should be created. but
   the format of the website should be as easy to use as possible"). To design before building: (1) where a card comes
   from: only from an answer that already stands (a checked claim without a card, or an answer the lane published), chosen
   by what people ask most (`data/site/demand.json`, the counts of the list, the sent questions); never from a model's own
   knowledge; (2) the rules for cards stand as written (useful, surprising research facts; never amounts, doses, timing,
   routes compared for strength, or reaching or strengthening effects; mixing only as risk facts): as code, like the
   lane's gates; (3) every card is read against its answer by readers who wrote none of it (`scripts/auto/blind_lines.py`
   is the pattern), and a card made by the system carries the system's label until a person has checked it; (4) where it
   shows: the drug's own deck, the start page's deck, the answer's own page ("Read the answer"), and the page the system
   started for a drug without one; (5) measured before it is switched on: the system's cards for answers that already
   have a checked card, compared with those cards.

Step e and the site's navigation: done in part by site 2.11.0 (every place can be asked for). Still to do for "navigate
the site perfectly": the parts of the statistics and methods pages by name, a country's emergency numbers and drug
checking from one question about the country ("greece"), and the reader's own country remembered across questions.

Also from the fresh measure: a line of its own for greetings and for "who are you" (now the line for a question that
is not about drugs); emoji that stand for a drug; the trained reader of decision 26 (c).

## In flight (17 November, 10:35 UTC; brought up to date 11:10 UTC)

- **`w_0048`** (*Does cannabis make sex better?*): five runs on 17 November (lanes 15 to 18), no clean answer; lane 18's
  was read and not released (a cause where its sources report links; one side of "On the one hand"). Next: a rule for a
  quote that is one half of a contrast ("on the one hand", "although", "while"): the sentence gives both halves or
  neither; then again when the allowances are new. The exam of the lane's sentences holds 108 (73 good, 35 not good).
- **`au_w_0041`** (*Does cannabis cause cancer?*, lane 17): five sentences, all good, held because it disagrees with
  the checked claim above. It stays held. If he approves the checked answer, the system's answer is not needed.
- **The table of medicine names from RxNorm** is home: `data/auto/names/rxnorm.json` (14,748 ingredients, 5,114 brand
  names, 475 ingredients of the nervous system with 829 brand names). Wikidata and MeSH do not allow their query
  addresses (robots.txt): not asked, not gone around. Step a of decision 26 uses it next.
- **Lessons** (`teach-0005` after the long run ends) and, with 800 lessons or more at home, a real training run
  (`train-*.json`; the path was proved today with `pharmakon-check-1-try`, which is not adopted).

## Decision 26, in this order

a. **Names.** From `rxnorm.json`: the ingredients of the nervous system (ATC group N) and their brand names become
   names the page knows as "a medicine we do not cover yet" (scope) and candidates for pages to start
   (`scripts/auto/place.py`, `data/auto/filing.json`); other medicines get their own line ("a medicine, not a drug
   this site covers") only after it is measured on real questions. The table is too large for the index as a pattern:
   a file of its own, loaded with Insight's files, read as a set. Street names are not in RxNorm: look for an open
   source that allows it (a probe first, as for these three).
b. **Misspelt names**: done (site 2.9.1). Watch what real visitors type; grow `spell.map` and `spell.keep`.
c. **Real language in bulk and a trained reader for the page.** Open collections of what people typed, only under a
   licence that allows it, fetched in the job that holds no key; never a visitor's words. Classes: about drugs or not,
   finished or not, which drug. The words rule stays as a second check.
d. **Fresh test sets** of thousands of real questions for each class; the measured error rate goes into
   `docs/AUTOMATION.md`. "1 in 1,000" is said only after about 3,000 fresh questions with no error.

## The lane, when the allowances are new (Cloudflare 00:00 UTC, Google 08:00 UTC)

- A further reader that answers: today none of the three Gemini models named did (a time-out, no verdict, "high
  demand"); Gemini 4 Hydrogen answers but has 18 calls a day. Try the marks reader (`gemini-3.5-flash-lite#marks`)
  in a team whose first reader is another model, and measure it on the exam first.
- The trial on unseen questions about amounts with team F (the request is in git history: `next-steps.md` of 17
  November, 05:00 UTC), then the rest of ten; `amounts` stays false until ten unseen questions read clean.
- `w_0043`, `w_0045`, `w_0044`, `w_0001`, `w_0002`.
