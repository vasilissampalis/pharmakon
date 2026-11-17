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

1. **The lane, when the allowances are new (00:00 UTC).** Read what it wrote for kanna and *Mitragyna javanica* and for
   the 46 questions never tried (`data/auto/lane/_last-auto-run.txt`, `data/auto/lane/state.json`). Compare team I (a
   free reader) with team H: does "rests on too few sources" come more often? If so, team I goes behind team H. Try
   team K by name on two questions (`data/auto/requests/trial-*.json`, `"team": "team K"`): Gemma reads, plans and
   writes. If its drafts pass as often as qwen's, put it second. Measure a rule for "an effect said where the source
   reports what people say" on the exams before adding it (an earlier, wider rule stopped 12 good cards for 2 wrong
   ones); then let the lane rewrite `w_0048`.
2. **The school** is built and runs every day (decision 28; `data/auto/language/report.json` is its own account). Next
   lessons, in this order: (a) **everyday words with a letter wrong**: "is ketmine adictive" finds nothing, because only
   drug names are corrected. Rule to measure first: a word the model's word list does not hold, five letters or more,
   with exactly one word of the list one letter away (a letter dropped, added, changed, or two swapped), is read as that
   word; measure on the 1,021 forum questions and the school's real questions that no good word is changed; page and
   build must read the same (parity). (b) **more language**: the web client reads the first 6 MB of a file, so the same
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
