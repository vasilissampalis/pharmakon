#!/usr/bin/env python3
"""lane.py: the machine lane. Answers written by the system from papers and official pages it found and read (docs/AUTOMATION.md).

The senior author, 15 November 2026. 17:33: "it should be claims... written as good as possible as close to 100% correct
as possible and ... in the language and format we write the rest of the website". 20:58: "it should be published and
automatically deployed with a very discreet disclaimer and we should just be able to access everything that was
automatically written and deployed to check whenever we want"; "if the automatic answer is not complete it should have a
small discreet disclaimer". 21:07: "it should find more than one sources if they are relevant ... the algorithm has to
mimick completely how claude writes answers".

    python3 -I scripts/auto/lane.py run [--max N] [--ids w_0027,...] [--again]
    python3 -I scripts/auto/lane.py requests          (the requests waiting in data/auto/requests/lane-*.json)
    python3 -I scripts/auto/lane.py --selftest

The same steps as the checked lane, each done by a model that did not do the one before, and each followed by a gate that
is code (no model's opinion can open a gate the code has shut):

  1 find     scripts/auto/papers.py: the searches, the papers in the order of reading, the papers that cannot be read.
             scripts/auto/official.py: the pages of official bodies that speak about the question (lane 3).
             What is read: up to three papers whose full text is open; up to two official pages; and, where that is not
             yet enough, the summaries (abstracts) of up to two reviews behind a paywall (free to read; the answer then
             says so and stays "not complete").
  2 read     a READER model reads one paper at a time: the passages nearest the question (a paragraph each). It may only
             copy: every finding comes with the passage's number and a part of it copied word for word.
             GATE the quote is found in that passage of the paper, letter for letter (spaces and dash shapes aside);
             GATE every number in a finding is in its quote. A finding that fails is thrown away.
             An introduction is not read in a single study (it reports other people's findings, not the paper's own).
  3 write    a WRITER model writes the answer from the findings only, in the site's format (short answer, But, How do
             we know?), and names for every sentence the findings it rests on. The site's own checked answers are its
             examples of the format.
  4 check    a CHECKER model, another model than the writer, reads each sentence beside the passages it rests on, without
             the writer's notes: do the passages say this, of the same people, with the same numbers, no stronger?
             A How-do-we-know line it does not accept is dropped; a short answer or a But it does not accept is written
             once more and checked once more, and if it is still not accepted there is no answer.
  5 rules    GATE the site's content rules, by code: no amounts, doses, re-dosing, ways of taking compared for strength,
             no making an effect stronger, no advice, person-first words, no quotation marks, lengths, and every number
             in the answer is in the quotes it rests on.
  6 sources  GATE at least one review or meta-analysis read in full, or one page of an official body (tier 1), or two
             of: a study in people, a review read in summary only, a page of a government-paid service (tier 2). Papers
             carry a Crossref record made by scripts/build_references.py, pages a reference made from the page itself;
             a retracted paper, or one under an expression of concern, is never used.
  7 stakes   A question about dying, overdose, an emergency, mixing two drugs, pregnancy, children or suicide is written
             and then WAITS FOR A PERSON: it is not published by the system (the editor's rule; emergency guidance is the
             senior author's own domain). Everything else that passed is published with the label.

A question about AMOUNTS (the senior author's decisions of 15 November 2026, 22:40 and 22:46; decision 11) goes another way,
with no writer: the reader copies each amount stated for people, with who received it and under what care; code keeps
only quotes that stand in the source, hold a number with its unit, name no animal and no amount that harmed or killed;
the checker reads each row beside its passage; code cuts each quote to 15 words at most and puts the fixed lines of
data/auto/lane/lines.json on the answer. Amounts come only from an official body of tier 1, a medicine's label, or a study
in people. Answers to other questions hold no amounts.

The second look (decision 12): an answer that is not complete, or was written by an older lane, or whose sources have
grown since, is written again; what it was before is kept in its "history".

What it writes: data/auto/answers/<id>.json (the answer; every sentence with the passages it rests on, kept short, for the
person who checks; the papers; the models; what each gate said; "published", "waiting" or "none", and why), the papers it
still wants (data/auto/papers-wanted.json, in APA 7), and data/auto/lane/state.json. The site shows only "published"
answers (site/build.js), each with "Written by our system from N papers. Not yet checked by a person." and, where papers
were missing, "Not complete yet".
"""
import sys, os, re, json, hashlib, pathlib, datetime, unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); sys.path.insert(0, str(ROOT / "scripts" / "insight"))
import papers as P, llm, official as O

OUT = ROOT / "data" / "auto" / "answers"
STATE = ROOT / "data" / "auto" / "lane" / "state.json"
MODELS_FILE = ROOT / "data" / "auto" / "lane" / "models.json"
WANTED = ROOT / "data" / "auto" / "papers-wanted.json"
MODELS = {"reader": "@cf/meta/llama-4-scout-17b-16e-instruct", "writer": "@cf/meta/llama-3.3-70b-instruct-fp8-fast", "checker": "@cf/openai/gpt-oss-120b"}
LINES_FILE = ROOT / "data" / "auto" / "lane" / "lines.json"
FOUND_OFFICIAL = ROOT / "data" / "auto" / "official" / "found"
LANE = 6                # the lane's own number: an answer written by an older lane is not shown (data/auto/lane/policy.json) and is written again
N_PAPERS = 2            # papers read in full for one answer (a third where the sources read are not yet enough)
N_TO_WRITER = 3         # findings of one source that go to the writer: the nearest to the question (and one limit)
N_OFFICIAL = 2          # official pages read for one answer (four for a question about amounts)
N_SUMMARIES = 2         # reviews behind a paywall read in summary, where the rest is not enough
ROOM = 1100             # neurons that must be left of today's allowance before a question is begun
N_PASSAGES = 7          # passages of a paper shown to the reader
PASSAGE_CHARS = 1400    # a passage is shown up to this length
TODAY = datetime.date.today().isoformat()


# ---------- words as they are compared ----------
def norm(t):
    """A text for finding a quote in it: Unicode forms folded, every quote mark and dash one shape, one space."""
    t = unicodedata.normalize("NFKC", t or "")
    t = re.sub(r"[‘’‚′`]", "'", t); t = re.sub(r"[“”„″]", '"', t); t = re.sub(r"[‐‑‒–—−]", "-", t)
    return re.sub(r"\s+", " ", t).strip()


def found_in(quote, text):
    q = norm(quote).strip(' ."\'…')
    return len(q) >= 20 and q in norm(text)


words = lambda t: len(re.findall(r"[A-Za-z0-9'’-]+", t or ""))
NUMWORD = {"half": "half", "twice": "twice", "double": "double", "doubled": "double", "doubles": "double", "triple": "triple", "tripled": "triple", "third": "third", "thirds": "third", "quarter": "quarter", "quarters": "quarter"}
WORDNUM = dict(zip("one two three four five six seven eight nine ten".split(), "1 2 3 4 5 6 7 8 9 10".split()))


NAMES_WITH_FIGURES = re.compile(r"\b(?:k2|cb[12]|5-?ht\w*|2c-[a-z]\w*|5-meo\w*|4-(?:aco|ho|meo|mmc|fa)\w*|3-(?:mmc|meo|ho|fpm)\w*|25[a-z]-nbo\w*|mk-801|1c?p-lsd|al-lad|delta-?[89]|d[89]-thc|thc-?[oph]|a-pvp|u-47700|w-18|covid-19)\b")


def numbers(text):
    """The numbers a sentence states: every figure ("2,405" and "2405" are one number), the words for a share (half, twice,
    a third), and a number word where it counts something measured ("one in five", "three times"). Not "one study" or
    "two reviews": those count the sources, which the gate on sources counts itself."""
    t = (text or "").lower(); t = re.sub(r"(?<=\d),(?=\d{3}\b)", "", t)
    t = NAMES_WITH_FIGURES.sub(" ", t)                                  # K2, 2C-B, CB1: names, not numbers (on 16 November 2026 a draft was refused for the 2 of "K2")
    out = set(re.findall(r"\d+(?:\.\d+)?", t)) | {NUMWORD[w] for w in re.findall(r"[a-z]+", t) if w in NUMWORD}
    n = r"(\d+|one|two|three|four|five|six|seven|eight|nine|ten)"
    for m in re.finditer(r"\b" + n + r"\s+(?:in|out of)\s+(?:every\s+)?" + n + r"\b", t): out.update(WORDNUM.get(x, x) for x in m.groups())     # "one in five", "3 out of 10"
    for m in re.finditer(r"\b(one|two|three|four|five|six|seven|eight|nine|ten)[\s-]+(?:times|fold)\b", t): out.add(WORDNUM[m.group(1)])               # "three times"
    return out


# ---------- 2 read ----------
INTRO = re.compile(r"^(introduction|background|rationale|overview)\b", re.I)


def pick_passages(question, ways, passages, enc, kind, k=N_PASSAGES):
    """The passages of a paper nearest the question, in the paper's own order: the abstract's, then the k nearest of the
    body. In a single study the introduction is left out (it reports what others found)."""
    body = [p for p in passages if p["where"] != "Abstract" and not (kind != "review" and INTRO.match(p["where"].split(" › ")[0]))]
    ab = [p for p in passages if p["where"] == "Abstract"][:2]
    if body:
        Q = enc([question] + list(ways or [])[:6]); S = enc([p["text"][:1200] for p in body]) @ Q.T
        best = S.max(1)
        for i, p in enumerate(body):
            sec = p["where"].split(" › ")[0].lower()
            p["near"] = float(best[i]) + (0.03 if re.match(r"(results?|findings|conclusions?|discussion|summary)", sec) else -0.02 if re.match(r"(methods?|materials)", sec) else 0)
        body = sorted(sorted(body, key=lambda p: -p["near"])[:k], key=lambda p: p["n"])
    return ab + body


READER_SYS = ("You read one source for Pharmakon, a drug encyclopedia for the public: a research paper, or a page of an official health body. You only copy what the source itself says. "
              "You never add anything you know from elsewhere, and you never guess. You answer with JSON only.")


def source_head(src):
    """How a source is named to a model: what it is, never more."""
    if src["read"] == "page": return f'OFFICIAL PAGE: "{src["title"]}", a page of {src["name"]} for the public' + (f' ({src["year"]})' if src.get("year") else "") + "."
    return f"PAPER{' (only its summary could be read)' if src['read'] == 'summary' else ''}: {src['title']} ({src.get('year') or 'n.d.'}), {src.get('journal') or ''}."


def shown(picked): return "\n".join(f"[{p['n']}] ({p['where']}) {p['text'][:PASSAGE_CHARS]}" for p in picked)


def reader_prompt(question, src, picked):
    page = src["read"] == "page"; what = "page" if page else "paper"
    return (f"QUESTION that people ask: {question}\n\n{source_head(src)}\n\n"
            f"PASSAGES of this {what} (each is one paragraph, with its number and where it stands):\n{shown(picked)}\n\n"
            "TASK. From these passages only:\n"
            + ("" if page else '1. "design": what kind of paper this is and who or what was studied, in one short phrase, with "quote": a part of ONE passage copied exactly, word for word (6 to 40 words), that shows it, and "passage": that passage\'s number.\n')
            + f'2. "findings": up to 4 things this {what} {"says" if page else "found or concluded"} that answer the QUESTION itself or a part of it (not a neighbouring question: when the question asks whether something happens, how it is treated is not an answer). The ones that answer it most directly first. '
            'For each: "passage" (its number), "quote" (a part of that passage copied exactly, word for word, 8 to 40 words, that states it), '
            '"finding" (the same thing in one plain sentence that stays close to the quote: no new facts, no reason or result the quote does not state, every number exactly as in the quote, and say "in rats", "in a laboratory" or "in one survey" when the quote does. '
            'Write "people who use ketamine", never "users", "abusers" or "addicts"; "use", never "abuse" or "misuse").\n'
            f'3. "limits": up to 2 limits or uncertainties that the passages themselves state about these findings (who was not studied, how the studies were done, what is not yet known), each with "passage", "quote" (copied exactly) and "limit" (one plain sentence that stays close to the quote). '
            f'That the {what} says nothing about something is never a limit: leave it out.\n'
            'Copy quotes exactly: do not correct, shorten in the middle or join two places. If nothing in the passages helps answer the question, return {"findings": []}.\n'
            'JSON only, in this form: {' + ("" if page else '"design": {"text": "...", "quote": "...", "passage": 3}, ') + '"findings": [{"passage": 7, "quote": "...", "finding": "..."}], "limits": [{"passage": 9, "quote": "...", "limit": "..."}]}')


STOP = set("the and for with from that this these those than then also can could may might will would should does did has have had not nor but into over under about after before between during among per "
           "more most less least very such some any each other their there which who whom whose what when where how are was were been being its it's they them some many much often".split())


def carried(text, quote, passage, least_quote=0.3, least_passage=0.6):
    """GATE 3 (lane 4): is what our plain sentence says carried by the source? Of the sentence's content words (four letters
    or more, compared by their first five), at least 30 in 100 must stand in the quote and 60 in 100 in the passage it was
    taken from. A sentence about something else than its quote ("the page does not say ...", an added reason) fails."""
    stems = lambda t: [w[:5] for w in re.findall(r"[a-z]+", norm(t).lower()) if len(w) >= 4 and w not in STOP]
    tw = stems(text)
    if len(tw) < 2: return True
    q, p = set(stems(quote)), set(stems(passage))
    return sum(w in q for w in tw) / len(tw) >= least_quote and sum(w in p for w in tw) / len(tw) >= least_passage


def read_gate(out, picked, amounts_ok=True):
    """What of a reader's answer may be used: each item's quote must stand in a passage that was shown (GATE 1), every
    number in its plain sentence must be in its quote (GATE 2), and the sentence must be carried by the quote and its
    passage (GATE 3). amounts_ok False (an ordinary answer): an item whose sentence holds an amount of a drug or a time
    between uses is not passed on, since no sentence of such an answer may hold one. Returns (design or None, findings,
    limits, what was thrown away and why)."""
    out = out if isinstance(out, dict) else {}
    by = {p["n"]: p for p in picked}; dropped = []
    def place(item):
        q = str(item.get("quote") or "").strip()
        if not (3 <= words(q) <= 70): return None
        p = by.get(item.get("passage")) if isinstance(item.get("passage"), int) else None
        if not p or not found_in(q, p["text"][:PASSAGE_CHARS]): p = next((x for x in picked if found_in(q, x["text"][:PASSAGE_CHARS])), None)
        return (p, q) if p else None
    def one(item, key):
        if not isinstance(item, dict): dropped.append({"why": "not an item"}); return None
        text = re.sub(r"\s+", " ", str(item.get(key) or "")).strip(); got = place(item)
        no = lambda why: dropped.append({"kind": key, "text": text[:200], "quote": str(item.get("quote") or "")[:200], "why": why})
        if not text: no("no sentence"); return None
        if not got: no("its quote does not stand in a passage that was shown (or is shorter than 3 words or 20 letters)"); return None
        if not numbers(text) <= numbers(got[1]): no("a number of the sentence is not in its quote"); return None
        if not carried(text, got[1], got[0]["text"], *((0.2, 0.4) if key == "text" else ())): no("the sentence is not carried by its quote and passage"); return None          # (what kind of paper it is may be said more freely)
        if not amounts_ok and key != "text" and any(rx.search(text) for name, rx in RULES[:2]): no("it holds an amount or a time between uses"); return None
        return {"passage": got[0]["n"], "where": got[0]["where"], "quote": got[1], "text": text}
    d = out.get("design"); design = one(d, "text") if isinstance(d, dict) else None
    fs = [x for x in (one(f, "finding") for f in (out.get("findings") or [])[:6]) if x]
    ls = [x for x in (one(l, "limit") for l in (out.get("limits") or [])[:3]) if x]
    return design, fs, ls, dropped


def ask_json(chat, model, system, prompt, room):
    for attempt in range(2):
        out = llm.as_json(chat(model, [{"role": "system", "content": system}, {"role": "user", "content": prompt + ("" if not attempt else "\n\nYour last answer was not valid JSON. Answer with the JSON object only.")}], room))
        if out is not None: return out
    return None


def read_source(chat, model, question, src, picked):
    out = ask_json(chat, model, READER_SYS, reader_prompt(question, src, picked), 900)
    return read_gate(out, picked, amounts_ok=False) if out is not None else (None, [], [], [{"why": "the reader gave no JSON"}])


# ---------- 2b read, for a question about amounts (decision 11) ----------
AMOUNT_Q = re.compile(r"\b(?:dos(?:e|es|age|ages|ing)|milligrams?|micrograms?|mg|mcg|standard drinks?|units? of alcohol"
                      r"|how (?:much|many)\b[^?]{0,60}\b(?:safe|too much|take|taken|takes|use|used|drink|smoke|normal|typical|usual|common|average|a day|per day|daily|a week|per week|weekly|at once|is (?:ok|okay|fine|enough|a lot))"
                      r"|(?:safe|normal|typical|usual|common|average|recommended|standard|maximum|max|starting|low|high|threshold)\s+(?:amounts?|quantit(?:y|ies))|(?:what|which)\s+amounts?)\b", re.I)
NUM = r"(?:\d+(?:[.,]\d+)?|(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|twenty-one)(?=(?:\s*(?:to|-|or)\s*[\w-]+)?\s+(?:or\s+(?:more|less|fewer)\s+)?(?:standard\s+)?(?:drinks?|units?)\b))"
AMT = re.compile(r"(?<![\w.,/])" + NUM + r"(?:\s*(?:to|-|or)\s*" + NUM + r")?(?:\s+or\s+(?:more|less|fewer))?\s?(?:mg|milligrams?|µg|μg|ug|mcg|micrograms?|g|grams?|ml|millilit(?:re|er)s?|units?|standard drinks?|drinks?)\b(?!\s*/\s*(?:m?l|dl|kg|day·kg)\b)(?!\s*(?:of\s+[\w-]+\s+)?per\s+(?:kilo|kg|m?l|dl|litre|liter|decilit(?:er|re)|100\s?m?l)\b)", re.I)
TIMING = re.compile(r"\b(?:wait|space)\w*\s+(?:at least\s+)?\d|\bevery\s+\d+(?:\s*(?:to|-|or)\s*\d+)?\s+(?:minutes?|hours?)\b|\b\d+(?:\.\d+)?(?:\s*(?:to|-|or)\s*\d+(?:\.\d+)?)?\s+(?:minutes?|hours?)\s+(?:before|after|apart|later)\b|\b(?:\d+(?:\.\d+)?|one|two|three|four|five|six|seven|eight)(?:\s*(?:to|-|or)\s*\d+(?:\.\d+)?)?\s+(?:days?|weeks?|months?)\s+(?:apart|later)\b", re.I)   # never shown: the time between two uses
REDOSE = re.compile(r"\bre-?dos\w*|\bsupplement\w*|\bbooster\b|\btop-?up\b|\b(?:second|third|additional|further|extra|repeat(?:ed)?|half)[\s-]dos(?:e|es|ing)\b", re.I)                                                                                # never taken: an amount added in the same session
NOT_AN_AMOUNT_FOR_PEOPLE = re.compile(r"\b(?:rats?|mice|mouse|rodents?|monkeys?|primates?|dogs?|zebrafish|in vitro|animals?)\b|\b(?:lethal|fatal\w*|death|deaths|died|dying|kill\w*|overdos\w*|toxic\w*|poison\w*|ld50|seiz(?:ed|ure)\w*|street|tablets? (?:sold|seized|contain\w*)|pills? (?:sold|seized|contain\w*))\b|\b(?:dried|mushrooms?|truffles?|cubensis|fruiting|flowers?|buds?|joints?|herbal|plant material|leaves|blotters?|crystals?|powder|edibles?|brownies?|gumm\w+|equivalent\w*|corresponding to|equal to|estimated weight|converted|convert\w*|blood|plasma|serum|urine|breath|concentration\w*|bac|per decilit(?:er|re)|g/dl|mg/dl|abv|pints?|glass(?:es)?|cans?|bottles?|measures? of|shots?|cups?|servings?|optimal|optimum|predict\w*|estimat\w*|model(?:l)?ed|simulat\w*|extrapolat\w*|dose-response|meta-regression|hypothetical\w*)\b", re.I)


def is_amounts(question): return bool(AMOUNT_Q.search(question or ""))


def amounts_prompt(question, src, picked, drug_names):
    what = "page" if src["read"] == "page" else "paper"
    return (f"QUESTION that people ask: {question}\n\n{source_head(src)}\n\n"
            f"PASSAGES of this {what} (each is one paragraph, with its number and where it stands):\n{shown(picked)}\n\n"
            f"TASK. From these passages only, list the AMOUNTS of {', '.join(drug_names[:4]) or 'the drug'} that were given to PEOPLE or are stated for people: in a study, in treatment, on a medicine's label, in official guidance. For each amount give:\n"
            '"passage": its number; "quote": the whole sentence or clause of that passage that states the amount, copied exactly, word for word (8 to 40 words, with the number, its unit, and the words that say whom it is for when they stand there);\n'
            '"who": the PEOPLE who received it or whom it is stated for, and under what care, in one plain phrase, using the passage\'s own words (for example: adults with PTSD in a clinical trial, with two therapists present; men; women; healthy adults). Never add care or a setting that the passage does not state;\n'
            '"what": what kind of amount it is, in a few words, using the passage\'s own words (for example: the amount in one session; the starting amount on the label; a daily amount in long-term treatment; the weekly low-risk guideline).\n'
            "If one sentence states amounts for several groups (for men and for women), give ONE item and quote the sentence whole. "
            "Leave out: amounts given to animals; amounts that harmed or killed someone; amounts of a plant or a product (dried mushrooms, cannabis flower, what a tablet contains) and amounts found in products that were sold or seized; "
            "an amount worked out from another (\"equivalent to\", \"corresponding to\"); levels in blood, breath or urine; what a standard drink or a unit contains; amounts for each kilogram of body weight; an amount added later in the same session. "
            'Do not compute, convert or add anything, and give no advice. If the passages state no such amount, return {"amounts": []}.\n'
            'JSON only, in this form: {"amounts": [{"passage": 4, "quote": "...", "who": "...", "what": "..."}]}')


HANGS = re.compile(r"(?:every|each|to|of|and|or|with|for|at|in|on|a|an|the|by|from|as|than|per|was|were|is|are|be|been|being|it|its|their|that|which|who|whose|those|these|this|not|no|never|more|less|fewer|if|when|while|but|because|although|though"
                   r"|can|may|might|should|must|will|would|could|has|have|had|also|about|around|approximately|roughly|over|under|after|before|during|between|into|up|such|any|some|only|then|so|they|we|he|she|his|her|our|your|you|do|does|did"
                   r"|other|another|both|either|neither|nor|yet|via|within|without|against|among|plus|versus|vs|e\.g|i\.e|once|until|since|where|whereas|whether|upon|like|unlike|including|despite|towards?|across|through|throughout|along|onto|off|out|above|below|near|very|most|many|much|several|few|all"
                   r"|\d+(?:[.,]\d+)?)", re.I)   # a word a quotation must not end on (when words follow it in the source)
LIMITS_IT = re.compile(r"(?:not|no|never|less|fewer|more|up|least|most|max\w*|minim\w*|exceed\w*|under|over|below|above|within|between|only|than|rather|limit\w*|from|beyond|approximately|about|around|roughly|nearly|almost|average|mean|median)", re.I)   # a word that says what an amount is a limit, a range or an average OF: never cut away from it
NEG = re.compile(r"(?:not|no|never|without|neither|nor|cannot|unless|except|rarely|seldom|hardly|few|little|lack\w*|absence|fail\w*|non|un\w*ly|\w+n't)", re.I)                          # a word that turns a meaning round
UNIT = r"(?:mg|milligrams?|µg|μg|ug|mcg|micrograms?|g|grams?|ml|millilit(?:re|er)s?|units?|standard drinks?|drinks?)"
AFTER_AMOUNT = re.compile(r"^(?:\s*/\s*\d+(?:[.,]\d+)?\s*kg\b)?(?:\s+(?:or|to|and)\s+\d+(?:[.,]\d+)?\s?" + UNIT + r"\b(?:\s*/\s*\d+(?:[.,]\d+)?\s*kg\b)?)*(?:\s+of\s+[\w-]+)?(?:\s+(?:or\s+(?:less|more|fewer|under|over)|at\s+(?:most|least)|and\s+(?:above|over|under|below)))?"
                          r"(?:\s+(?:(?:once|twice|thrice|(?:two|three|four|\d+)\s+times)\s+)?(?:(?:a|per|each|every)\s+(?:day|week|month|night|session|occasion|sitting)|daily|weekly|monthly|(?:in|on)\s+(?:a|any|one|each|any\s+one|any\s+single|a\s+single)\s+(?:day|week|session|occasion|sitting)))?", re.I)   # "or 84 mg", "of caffeine", "or less", "a day", "twice weekly": words that belong to the amount
GROUP_AFTER = re.compile(r"^(?:\s*\([^)]{0,48}\))?(?:\s+(?:per|a|each|every)\s+(?:drinking\s+)?(?:day|week|occasion|session))?,?\s+(?:for|in|among|if\s+you\s+are|if\s+you're)\s+(?:(?:a|an|the|most|all|healthy|adult|older|younger|both)\s+){0,3}"
                         r"(?:men|man|women|woman|adults?|people|males?|females?|patients?|participants?|those|everyone)\b", re.I)   # "(7.1 standard drinks) per drinking day for men", ", if you are a woman": whom the amount is for
RESTRICTS = ("for", "in", "among", "if", "when", "unless", "except", "provided", "only", "aged", "under", "during", "after", "before")   # a word after which the source says whom or when the amount is for


def bare(w): return w.lower().strip(".,;:()[]%\"'")


BETWEEN = frozenset("once and or but while whereas although though because which who whose that when where if unless among in on at for with without by from to of as than after before during since until through throughout across between into over under including such however according compared despite via per versus so yet nor".split())   # a word that begins a new phrase: a cut just before it stops between two phrases


def neg_before(ws, a, reach=None):
    """Is there a word that turns the meaning round before a cut's start, in the same sentence (or, with reach, within
    that many words)? Then the cut would say the opposite of its source ("were not | associated with ...", "Neither the
    seller nor the buyer | can predict ...")."""
    for j in range(a - 1, -1 if reach is None else max(-1, a - reach - 1), -1):
        if re.search(r"[.;:]$", ws[j]): return False
        if NEG.fullmatch(bare(ws[j])): return True
    return False


FRAME_NOUN = re.compile(r"(?:dose|doses|dosage|dosages|amount|amounts|limit|limits|total|intake|maximum|minimum)", re.I)
FRAME_WORD = re.compile(r"(?:a|an|the|one|two|three|four|five|six|single|separate|daily|weekly|oral|total|initial|starting|maximum|minimum|maintenance|recommended|fixed|flexible|mean|median|average|usual|typical|low|lower|high|higher|moderate|first|second|third|each|subsequent|later|further|next|following|previous)", re.I)


def window15(quote, k=0, span=False):
    """The part of a quote, 15 words at most, that holds its amount (the k-th of the quote) and no time between two uses:
    the quotation the site shows (its rule: 15 words at most). Hard rules, so that a cut never changes what the source
    says: the words that limit the amount stay with it ("not more than", "up to", "between", "about": within five words
    before it, in the same clause), and so do a word that turns the meaning round within eight words before it ("were not
    given ...") and the words that belong to the amount after it ("or 84 mg", "of caffeine", "or less", "a day"); a cut
    never starts just after a word that turns the meaning round, never ends on a word that hangs ("... as an amount not"),
    never goes through another amount or stops between another amount and the words that belong to it. Among the parts
    that keep these rules: one that starts and ends where a clause does, or with the amount's own words ("two separate
    doses of 25 mg of psilocybin"), and the longer. None where no such part exists. span: also the first and last word."""
    ws = norm(quote).strip(' "\'').split(" "); text = " ".join(ws); ms = list(AMT.finditer(text))
    if k >= len(ms): return None
    m = ms[k]
    word_at = lambda i: len(text[:i].split(" ")) - 1
    def phrase(x):                                                     # an amount with the words that belong to it: (first word, last word of the amount, last word of the phrase)
        more = AFTER_AMOUNT.match(text[x.end():]); return word_at(x.start()), word_at(x.end() - 1), (word_at(x.end() + more.end() - 1) if more and more.end() else word_at(x.end() - 1))
    first, last, least = phrase(m)
    times = [(word_at(t.start()), word_at(t.end() - 1)) for t in TIMING.finditer(text)]        # the words that state a time between uses: no part of them is shown
    if any(t0 <= least and first <= t1 for t0, t1 in times): least = last
    else:
        more = AFTER_AMOUNT.match(text[m.end():]); end = m.end() + (more.end() if more else 0); grp = GROUP_AFTER.match(text[end:])
        if grp and not any(t0 <= word_at(end + grp.end() - 1) and least < t1 for t0, t1 in times): least = word_at(end + grp.end() - 1)   # whom it is for stays with the amount
    if any(t0 <= last and first <= t1 for t0, t1 in times): return None
    others = [o for o in (phrase(x) for x in ms if x is not m) if not first <= o[0] <= least]   # the other amounts in the same words
    others = [(o0, o1, o1 if any(t0 <= o2 and o1 < t1 for t0, t1 in times) else o2) for o0, o1, o2 in others]
    must, far = first, False
    for j in range(first - 1, max(-1, first - 9), -1):                 # the words that limit the amount, or turn it round, stay with it
        if re.search(r"[.;:]$", ws[j]): break
        if first - j <= 5 and LIMITS_IT.fullmatch(bare(ws[j])): must = j
        elif NEG.fullmatch(bare(ws[j])): must = j; far = True
    frame = must                                                       # "two separate doses of" 25 mg: the amount's own words
    if not far:
        j = must - 1
        for _ in range(2):                                              # "doses of", "dose is", "doses may be"
            if j >= 0 and re.fullmatch(r"(?:of|at|is|was|were|are|to|be|may|can|should|must|will|would)", bare(ws[j])) and not re.search(r"[.;:,]$", ws[j]): j -= 1
        if j >= 0 and FRAME_NOUN.fullmatch(bare(ws[j])) and not re.search(r"[.;:,]$", ws[j]):
            frame = j
            while frame > 0 and FRAME_WORD.fullmatch(bare(ws[frame - 1])) and not re.search(r"[.;:,]$", ws[frame - 1]): frame -= 1
        elif must > 0 and re.fullmatch(r"(?:a|an|the)", bare(ws[must - 1])): frame = must - 1
        if neg_before(ws, frame, 8): frame = must
    if least - must + 1 > 15: return None
    best = None
    for a in range(max(0, least - 14), must + 1):
        if a and a not in (must, frame) and neg_before(ws, a, 8): continue
        if k and a and not (re.search(r"[.;:,]$", ws[a - 1]) or bare(ws[a - 1]) in ("and", "or", "but", "while", "whereas")): continue   # a further amount is shown from where its own clause begins, so that whom it is for comes with it
        for b in range(least + 1, min(len(ws), a + 15) + 1):
            if any(a <= t1 and t0 < b for t0, t1 in times): continue
            part = " ".join(ws[a:b])
            if part.count("(") != part.count(")"): continue
            ends = b == len(ws) or bool(re.search(r"[.;:]$", ws[b - 1])); comma = ws[b - 1].endswith(",")       # (a comma may stand inside a list: half a clause's end)
            if not ends and HANGS.fullmatch(bare(ws[b - 1])) and not any(b - 1 == o2 for o0, o1, o2 in others): continue
            if any(o0 < b <= o2 or o0 < a <= o2 for o0, o1, o2 in others): continue              # never through the middle of another amount, or between it and the words that belong to it
            clean = any(b - 1 == o2 for o0, o1, o2 in others)                                    # it stops just where another amount's own words stop
            half = any(a <= o0 and o2 < b - 1 and b - 1 - o2 < 4 and not ends and not comma for o0, o1, o2 in others)   # another amount whose sentence is cut short
            nxt = bare(ws[b]) if b < len(ws) else ""
            score = ((2 if a == 0 or re.search(r"[.;:]$", ws[a - 1]) else 1 if ws[a - 1].endswith(",") else 0.8 if a in (must, frame) and not far else -0.5 if (HANGS.fullmatch(bare(ws[a])) and not ws[a][0].isdigit()) or ws[a].startswith("(") else 0)   # (the amount's own words are a safe start; a start elsewhere may leave a word behind that the rest needs)
                     - (1 if a and NEG.fullmatch(bare(ws[a])) and not LIMITS_IT.fullmatch(bare(ws[a])) else 0) - (0.6 if a and bare(ws[a]) in ("and", "or", "but", "while", "whereas") else 0)
                     + (2 if ends else (1.5 if b - 1 == least and least > last else (1 if nxt in BETWEEN else 0.4) if comma else 1.0 if clean else 0) + (0.7 if nxt in ("and", "but", "while", "whereas", "although", "because", "which") else -1.5 if nxt in RESTRICTS and not comma else 0))
                     + 0.05 * (b - a) - (1.5 if half else 0))
            if best is None or score > best[0]: best = (score, part, a, b)
    if not best: return None
    show = best[1].strip(" ,;:.")
    return (show, best[2], best[3]) if span else show


def windows15(quote, most=3, clauses=False):
    """A part for each amount of a quote (the first three), in their order: an amount that already stands inside an earlier
    part gets none of its own. clauses: each part with the stretch of the quote it belongs to (from where it begins, or
    from the quote's start for the first, to where the next part begins), so that what is said about whom the amount is
    for can be looked at even where the part itself had to leave it out."""
    ws = norm(quote).strip(' "\'').split(" "); text = " ".join(ws); out = []
    for k, m in enumerate(list(AMT.finditer(text))[:6]):
        at = len(text[:m.start()].split(" ")) - 1
        if any(a <= at < b for _, a, b in out): continue
        got = window15(quote, k, span=True)
        if not got or any(got[0] == o[0] for o in out): continue
        out = [o for o in out if not (got[1] <= o[1] and o[2] <= got[2])] + [got]        # a part that holds an earlier part whole takes its place
        if len(out) >= most: break
    if not clauses: return [o[0] for o in out]
    starts = [0] + [o[1] for o in out[1:]] + [len(ws)]
    return [(o[0], " ".join(ws[starts[i]:starts[i + 1]])) for i, o in enumerate(out)]


NOT_SHOWN = ("an amount of a drug", "timing between uses", "a way of taking compared for strength", "how to prepare or take a drug", "making an effect stronger", "words that are not person-first")


SAYS = re.compile(r"(?:is|are|was|were|be|been|has|have|had|can|cannot|may|might|will|would|could|should|must|do|does|did|(?!(?:weed|seed|speed|indeed|hundred|breed|sacred|naked|aged)$)[a-z]{2,}ed|found|finds?|shows?|shown|means?|meant|led|leads?|rose|rises?|fell|falls?|grew|grows?|became|becomes?|remains?|seems?|appears?|suggests?"
                  r"|reports?|causes?|increases?|decreases?|reduces?|raises?|lowers?|binds?|acts?|lasts?|occurs?|happens?|varies|vary|depends?|includes?|contains?|met|meets?|took|takes?|taken|saw|seen|sees?|got|gets?|gave|gives?|given|made|makes?|knew|knows?|known|felt|feels?|kept|keeps?|held|holds?|said|says?|went|goes|came|comes?"
                  r"|ran|runs?|drank|drinks?|ate|eats?|lost|loses?|uses?|dies?|needs?|helps?|works?|affects?|differs?|exists?|carr(?:y|ies)|tends?|begins?|began|ends?|stops?|starts?|wears? off|builds?|develops?|experiences?|describes?|states?|advises?|recommends?|warns?|notes?)", re.I)   # a word that makes a part of a sentence say something


def words15(quote, text=""):
    """The part of a source's words, 15 at most, that says most of what a sentence of ours says: the quotation shown under
    a How-do-we-know line, so that a reader can compare the two (the site's rule: 15 words at most, one for each line).
    None where the words hold what the site never shows (an amount in an answer that is not about amounts, a time between
    uses, a way of taking, words that are not person-first)."""
    ws = norm(quote).strip(' "\'').split(" ")
    if len(ws) > 15:
        key = {w.lower() for w in re.findall(r"[A-Za-z0-9'’-]+", text or "") if len(w) > 3}; best = None
        for a in range(len(ws)):                                       # every part of 6 to 15 words; one that starts and ends where a clause does stands first
            if a and neg_before(ws, a): continue                         # never a part that starts just after "not", "no", "without": it would say the opposite
            for b in range(a + 6, min(len(ws), a + 15) + 1):
                w = ws[a:b]; plain = [bare(x) for x in w]
                ends = b == len(ws) or bool(re.search(r"[.;:]$", w[-1])); comma = w[-1].endswith(",")
                if not ends and not comma and HANGS.fullmatch(plain[-1]): continue      # never ending on a word that hangs ("... was not")
                if " ".join(w).count("(") != " ".join(w).count(")"): continue
                if not ends and not any(SAYS.fullmatch(x) for x in plain): continue       # a part that says nothing (a subject cut from its verb) is not a quotation
                nxt = bare(ws[b]) if b < len(ws) else ""
                score = (sum(1 for x in plain if x in key) + sum(0.5 for x in w if re.search(r"\d", x))
                         + (0.5 if a == 0 or re.search(r"[.;:,]$", ws[a - 1]) else 0.4 if bare(ws[a - 1]) == "that" else -0.5 if HANGS.fullmatch(plain[0]) and not plain[0][:1].isdigit() and not NEG.fullmatch(plain[0]) else 0)   # (after "showed that" the source's own statement begins)
                         + (1.0 if ends else (1.0 if nxt in BETWEEN else 0.4) if comma else 0) - (0.5 if nxt in key else 0)                # (a comma before "with", "and", "which" ends a clause; elsewhere it may stand in a list. A cut just before a word our own line uses is a cut in the middle of what is said)
                         - (1.5 if not ends and not comma and any(x.endswith(",") for x in w[-4:-1]) else 0)                               # (a clause that has only just begun: "..., so the rates")
                         + 0.03 * (b - a))
                if best is None or score > best[0]: best = (score, w)
        if best is None: return None
        ws = best[1]
    show = " ".join(ws).strip(" ,;:.")
    if words(show) >= 4 and not any(rx.search(show) for name, rx in RULES if name in NOT_SHOWN) and not re.search(r'["“”]', show): return show
    return None


CARE = re.compile(r"(?:medic|staff|super|thera|hospi|docto|physi|nurse|monit|presc|psych|suppo|couns|train|profe)")   # the stems of words that say under what care an amount was given
OF_ITS_KIND = {"page": {"offic", "guida", "guide", "advic", "page", "body", "healt"}, "label": {"label", "medic", "presc", "patie"}, "paper": {"study", "studi", "resea", "paper", "parti"}}


def row_carried(who, what, passage, around, src):
    """Are the reader's words for WHO received an amount, and under WHAT CARE, the source's own? Of the content words of
    who (four letters or more, compared by their first five; "women" and "woman" are one word), six in ten must stand in the amount's own
    passage, its heading or the source's title (for a single study also in the other passages shown: its summary says who
    took part; a review or a page speaks of different people from one passage to the next), and every word about care
    ("medical", "supervised", "therapists") must: the care an amount was given under is never the reader's to add. Words
    that only name the kind of source (a study, a label, official guidance) and the plain words for an amount are let be."""
    one = {"women": "woman", "men": "man", "females": "female", "males": "male", "persons": "person", "people": "person"}
    stems = lambda t: [one.get(w, w)[:5] for w in re.findall(r"[a-z]+", norm(t).lower()) if (len(w) >= 4 or w in ("men", "man")) and w not in STOP]
    base = set(stems(passage + " " + around))
    free = {"amoun", "perso", "given", "recei", "state", "adult", "publi", "gener", "every", "anyon", "indiv", "singl"} | OF_ITS_KIND["label" if src.get("label") else "page" if src.get("read") == "page" else "paper"]
    if any(CARE.match(w) and w not in base for w in stems(who + " " + what)): return False      # care is never ours to add, in who or in what
    tw = [w for w in stems(who) if w not in free]                                               # (what kind of amount it is may be said in our words: "the weekly low-risk guideline")
    return not tw or sum(w in base for w in tw) / len(tw) >= 0.6


PEOPLE = re.compile(r"\b(?:people|person|persons|adults?|men|man|women|woman|patients?|participants?|volunteers?|individuals?|subjects|those|anyone|everyone|public|population|males?|females?|veterans?|students?|workers?|drivers?|athletes?|you)\b", re.I)
QUOTE_NEVER = ("timing between uses", "a way of taking compared for strength", "how to prepare or take a drug", "making an effect stronger", "advice or a promise of safety")   # what a source's own words must not hold to be shown beside an amount


def amount_gate(out, picked, src, dwords):
    """The rows of a reader's answer that may be used: (rows, what was thrown away and why). A row is kept when its quote
    stands in a passage that was shown, holds a number with its unit, is about people and not about harm, a product or a
    level in the blood, when the passage or the source's title names the drug, when who received it and under what care
    are the source's own words (not the reader's), and when a part of 15 words at most can be shown. A quote that holds
    several amounts ("11 standard drinks per week, if you are a woman; 17 ..., if you are a man") gives a row for each."""
    out = out if isinstance(out, dict) else {}; by = {p["n"]: p for p in picked}; rows, dropped = [], []
    for item in (out.get("amounts") or [])[:8]:
        if not isinstance(item, dict): dropped.append({"why": "not an item"}); continue
        q = re.sub(r"\s+", " ", str(item.get("quote") or "")).strip(); who = re.sub(r"\s+", " ", str(item.get("who") or "")).strip(" ."); what = re.sub(r"\s+", " ", str(item.get("what") or "")).strip(" .")
        p = by.get(item.get("passage")) if isinstance(item.get("passage"), int) else None
        if not p or not found_in(q, p["text"][:PASSAGE_CHARS]): p = next((x for x in picked if found_in(q, x["text"][:PASSAGE_CHARS])), None)
        ours = who + " " + what
        if p:                                                          # (the reader often quotes a list's item without the words that govern it)
            t = norm(p["text"][:PASSAGE_CHARS]); i = t.find(norm(q).strip(' ."\'…'))
            before = re.split(r"(?<=[.;!?])\s+", t[:i].rstrip())[-1].split(" ")[-5:] if i > 0 else []
            lim = lambda w: LIMITS_IT.fullmatch(bare(w)) and bare(w) not in ("from", "about", "around", "average", "mean", "median", "most", "only", "within", "between")
            if any(lim(w) for w in before[-3:]):
                j = next(k for k, w in enumerate(before) if lim(w) or NEG.fullmatch(bare(w)))
                if j and NEG.fullmatch(bare(before[j])) and re.fullmatch(r"(?:should|must|do|does|did|can|could|may|is|are|was|were|will|would)", bare(before[j - 1])): j -= 1
                q = (" ".join(before[j:]) + " " + norm(q).strip(' ."\'…')).strip()
        why = ("its quote does not stand in a passage that was shown (or is shorter than 20 letters)" if not p else
               "the quote is shorter than 4 words or longer than 70" if not 4 <= words(q) <= 70 else
               "no amount with its unit in the quote" if not AMT.search(q) else
               "who or what is missing, or too long" if not (who and what and words(who) <= 30 and words(what) <= 20) else
               "an animal's amount, an amount that harmed, a product's amount, an amount worked out from another, or a level in the blood" if NOT_AN_AMOUNT_FOR_PEOPLE.search(q) or NOT_AN_AMOUNT_FOR_PEOPLE.search(ours) else
               "an amount added in the same session" if REDOSE.search(q + " " + ours) else
               "who names no people" if not PEOPLE.search(who) else
               "an amount in our own words for who or what" if AMT.search(ours) else
               "a number in who or what that is not in the passage" if not numbers(ours) <= numbers(p["text"]) else
               "who received it, or under what care, is not in the source's words" if not row_carried(who, what, p["text"], " ".join([src.get("title") or "", p.get("where") or ""] + ([x["text"] for x in picked] if src.get("read") != "page" and src.get("kind") == "study" else [])), src) else
               "the passage and the title do not name the drug" if dwords and not O.has_word(O.flat(src["title"] + " " + p["text"]), dwords) else
               next(("our own words break a rule: " + name for name, rx in RULES if name not in ("an amount of a drug", "a quotation or a source in brackets", "a sign instead of a word") and rx.search(ours)), ""))
        shows = [] if why else [(w, c) for w, c in windows15(q, clauses=True) if not any(rx.search(w) for name, rx in RULES if name in QUOTE_NEVER) and not any(r["show"] == w for r in rows)]
        if not why and not shows: why = "no part of 15 words can be shown without changing what it says (or it was shown already, or it holds what is never shown)"
        if why: dropped.append({"quote": q[:200], "who": who[:120], "what": what[:120], "why": why}); continue
        for w, c in shows: rows.append({"passage": p["n"], "where": p["where"], "quote": q, "show": w, "clause": c, "who": who, "what": what})
    return rows, dropped


def read_amounts(chat, model, question, src, picked, dwords):
    out = ask_json(chat, model, READER_SYS, amounts_prompt(question, src, picked, list(dwords)), 900)
    return amount_gate(out, picked, src, dwords) if out is not None else ([], [{"why": "the reader gave no JSON"}])


# ---------- 3 write ----------
WRITER_SYS = ("You write one answer for Pharmakon, a free drug encyclopedia that tells the public what research found, without judging. "
              "You write ONLY from the findings you are given: nothing from memory. You answer with JSON only.\n"
              "The rules of the site:\n"
              "- Plain words a 14-year-old can read. Short sentences. Lead the short answer with what people want to know.\n"
              "- If the question can be answered with yes or no, the short answer begins with 'Yes', 'No', 'It can', 'Sometimes', 'It depends' or 'Not known', and then says why.\n"
              "- Everyday words: 'addicted' or 'dependent', 'withdrawal symptoms', 'the heart', 'the gut', 'works', 'stopping'. Not 'abstinence symptoms', 'withdrawal syndrome', 'pharmacological', 'cardiovascular', 'efficacy', 'cessation'.\n"
              "- Say who was studied when the findings say it (how many people, where, or that it was animals or a laboratory).\n"
              "- Keep every number exactly as the finding has it. Never claim more than the findings do: a link is not a cause; one study is not proof.\n"
              "- Never give amounts, doses, timing between uses, or ways of taking a drug. Never say how to make an effect stronger. No advice: never 'you should'. Never call anything 'safe'.\n"
              "- Person-first words: 'people who use cannabis', 'people with an alcohol use disorder'. Never 'users', 'addicts', 'abusers', 'abuse', 'alcoholics', 'clean'.\n"
              "- No quotation marks, no brackets with sources, no mention of 'findings', 'passages' or 'the paper says F1'. Never write 'Paper A': say what it is, for example 'A 2024 review of case reports' or 'A survey of 278 people'.\n"
              "- Write 'times', never the sign ×. Write 'people who microdose', 'people who smoke', 'people who drink', never 'microdosers', 'smokers', 'drinkers'. Write 'use' or 'use disorder', never 'abuse' or 'misuse'.\n"
              "- The But must be a limit of THIS answer: who was not studied, how the studies were done, or what is not known about the question itself. Never borrow a limit that the paper states about something else.\n"
              "- The short answer answers every part of the question, in the order it was asked.\n"
              "- An official page is a statement by that body, not a study. Say whose it is: 'The NHS says ...'. Never write 'studies show' for it.\n"
              "- Where only a paper's summary could be read, say so: 'The summary of a 2021 review says ...'.\n"
              "- If the findings do not answer the question, say plainly what they do show, and set \"complete\" to false.")


def writer_prompt(question, sources, examples, fix=""):
    lines = []
    for s in sources:
        if s["read"] == "page": lines.append(f"OFFICIAL PAGE {s['tag']}: \"{s['title']}\", a page of {s['name']}" + (f" ({s['year']})" if s.get("year") else "") + f". When you use it, name the body: \"{s['short'][0].upper() + s['short'][1:]} says\".")
        else: lines.append(f"PAPER {s['tag']}{' (ONLY ITS SUMMARY COULD BE READ)' if s['read'] == 'summary' else ''}: {s['title']} ({s.get('year') or 'n.d.'}). {('A review or meta-analysis.' if s['kind'] == 'review' else 'A case report: one person or a few.' if s['kind'] == 'case' else 'A single study.')}")
        if s.get("design"): lines.append(f"  [D{s['tag']}] what it is and who was studied: {s['design']['text']} (the paper's words: {s['design']['quote']})")
        for f in s["findings"]: lines.append(f"  [{f['id']}] {f['text']} (the paper's words: {f['quote']})")
        for l in s["limits"]: lines.append(f"  [{l['id']}] a limit the paper states: {l['text']} (the paper's words: {l['quote']})")
    ex = "\n\n".join(f"Question: {e['q']}\nshort: {e['short']}\nbut: {e['but']}\nhow: " + " | ".join(e["how"][:3]) for e in examples)
    return (f"QUESTION that people ask: {question}\n\nWHAT THE SOURCES SAY (each item has a label in square brackets):\n" + "\n".join(lines) + "\n\n"
            "HOW THE SITE WRITES (three answers from the site, for the form only, not for their facts):\n" + ex + "\n\n"
            "TASK. Write the answer to the QUESTION from the labelled items only:\n"
            '- "short": the answer itself, 1 or 2 sentences, at most 45 words.\n'
            '- "but": the main limit or doubt, 1 sentence, at most 35 words. It must rest on a limit item or on what kind of study it was.\n'
            '- "how": 2 to 4 lines, one for each source used, each at most 35 words: what kind of study and who was studied, or whose page it is, and what it found or says.\n'
            'For "short", for "but" and for every line of "how", give "uses": the labels of the items that sentence rests on (at least one).\n'
            '- "complete": true if the items answer the question, false if they answer only a part or a neighbouring question; "missing": in a few words, what is not answered.\n'
            + (f"\nYOUR LAST ANSWER BROKE THESE RULES, write it again without them: {fix}\n" if fix else "") +
            'JSON only, in this form: {"short": {"text": "...", "uses": ["F1"]}, "but": {"text": "...", "uses": ["L1"]}, "how": [{"text": "...", "uses": ["DA", "F1"]}], "complete": true, "missing": ""}')


def draft_of(out, labels):
    """A writer's answer as parts [(name, text, uses)], or (None, why)."""
    if not isinstance(out, dict): return None, "no JSON"
    parts = []
    for name, v in [("short", out.get("short")), ("but", out.get("but"))] + [(f"how{i + 1}", h) for i, h in enumerate((out.get("how") or [])[:4])]:
        if not isinstance(v, dict): return None, f"{name} is missing"
        text = re.sub(r"\s+", " ", str(v.get("text") or "")).strip(); uses = [u.strip("[] ") for u in (v.get("uses") or []) if isinstance(u, str)]
        uses = [u for u in dict.fromkeys(uses) if u in labels]
        if not text: return None, f"{name} is empty"
        if not uses: return None, f"{name} names no item it rests on"
        parts.append({"part": name, "text": text, "uses": uses})
    if len(parts) < 3: return None, "fewer than one How-do-we-know line"
    return {"parts": parts, "complete": out.get("complete") is True, "missing": re.sub(r"\s+", " ", str(out.get("missing") or "")).strip()[:160]}, ""


# ---------- 4 check ----------
CHECKER_SYS = ("You check sentences against the passages of research papers they are said to rest on. You are strict and you use only the passages: "
               "nothing you know from elsewhere counts. You answer with JSON only.")


def checker_prompt(parts, labels, question=None, each=None):
    blocks = []
    for n, p in enumerate(parts, 1):
        ps = "\n".join(f"   PASSAGE ({labels[u]['paper']}; {labels[u]['where']}): {labels[u]['passage_text'][:PASSAGE_CHARS]}" for u in p["uses"])
        blocks.append(f"{n}. SENTENCE: {p['text']}\n{ps}")
    return ("For each numbered SENTENCE below, decide whether its PASSAGES support it. Supported means ALL of this: everything the sentence says is stated in its passages; "
            "it is about the same people, animals or setting; every number is the same; it is not stronger or more certain than the passages; it does not say one thing causes another "
            "where the passages only report a link; it does not turn what one study found into a general fact. If any part of the sentence is not in the passages, it is not supported.\n\n"
            + "\n\n".join(blocks)
            + (f"\n\nThen judge the answer as a whole. QUESTION that was asked: {question}\n"
               '"answers_question": does sentence 1 answer that QUESTION itself, directly (true), or does it answer a neighbouring question or only talk around it (false)?\n'
               '"but_fits": is sentence 2 a limit or a doubt about what sentence 1 says (true), or is it about something else, for example about a treatment when the question is whether something happens (false)?'
               '\n\nJSON only, one verdict for every sentence, in this form: {"verdicts": [{"n": 1, "supported": true, "problem": ""}, {"n": 2, "supported": false, "problem": "what the passages do not say"}], "answers_question": true, "but_fits": true, "why": ""}' if question else
               f"\n\nQUESTION that was asked: {each}\nFor every sentence also give \"on_question\": is the amount it states an amount of the kind the QUESTION asks for (true), or of another kind, for example an amount called high-risk when the question asks what is called low-risk, or what a drink contains when the question asks how much people drink (false)?"
               '\n\nJSON only, one verdict for every sentence, in this form: {"verdicts": [{"n": 1, "supported": true, "on_question": true, "problem": ""}, {"n": 2, "supported": false, "on_question": true, "problem": "what the passages do not say"}]}' if each else
               '\n\nJSON only, one verdict for every sentence, in this form: {"verdicts": [{"n": 1, "supported": true, "problem": ""}, {"n": 2, "supported": false, "problem": "what the passages do not say"}]}'))


def room_for(model, plain):
    """How many tokens a model may answer with. One that reasons before it writes needs room for both: on 16 November 2026
    gpt-oss-120b used all of 1,400 tokens reasoning and wrote nothing, three times for each of two questions; with 3,000 it
    reasoned for some 1,300 and then wrote its answer (data/auto/exam/writer-trial.json)."""
    return plain + 2200 if "gpt-oss" in model else plain


def check(chat, model, parts, labels, question=None, whole=None, each=None):
    """[(supported?, problem)] for the parts, in order. A sentence without a clear verdict is not supported. With a
    question, the second reader also says whether the short answer answers it and whether the But is about that answer
    (written into whole: "answers", "but_fits", "why"; None where it gave no clear word)."""
    for attempt in range(2):
        out = llm.as_json(chat(model, [{"role": "system", "content": CHECKER_SYS}, {"role": "user", "content": checker_prompt(parts, labels, question, each)}], room_for(model, 120) + 90 * len(parts) + (80 if question else 0)))
        vs = {v.get("n"): v for v in (out or {}).get("verdicts") or [] if isinstance(v, dict)}
        if out is not None and all(isinstance(vs.get(n, {}).get("supported"), bool) for n in range(1, len(parts) + 1)):
            if whole is not None:
                whole.update(answers=out.get("answers_question") if isinstance(out.get("answers_question"), bool) else None, but_fits=out.get("but_fits") if isinstance(out.get("but_fits"), bool) else None, why=re.sub(r"\s+", " ", str(out.get("why") or ""))[:240])
            return [(vs[n]["supported"] is True and not (each and vs[n].get("on_question") is False),
                     re.sub(r"\s+", " ", str(vs[n].get("problem") or "") or ("not an amount of the kind the question asks for" if each and vs[n].get("on_question") is False else ""))[:240]) for n in range(1, len(parts) + 1)]
    return [(False, "the checker gave no clear verdict")] * len(parts)


# ---------- 5 rules ----------
RULES = [
    ("an amount of a drug", re.compile(r"\b\d+(?:[.,]\d+)?\s?(?:mg|milligrams?|µg|ug|mcg|micrograms?|g|grams?|ml|millilit(?:re|er)s?|mg/kg|iu|ounces?|oz)\b|\b\d+(?:[.,]\d+)?\s?(?:pills?|tablets?|tabs?|capsules?|lines?|hits?|drops?|puffs?|joints?|shots?|bumps?|blotters?)\b", re.I)),
    ("timing between uses", re.compile(r"\bre-?dos\w*|\b(?:wait|space)\w*\s+(?:at least\s+)?\d|\bevery\s+\d+\s+(?:minutes?|hours?)\b|\b\d+\s+(?:minutes?|hours?)\s+(?:before|after|apart)\s+(?:taking|using|the (?:first|last|next))", re.I)),
    ("a way of taking compared for strength", re.compile(r"\b(?:snort\w*|inject\w*|smok\w*|swallow\w*|plugg\w*|boof\w*|vap\w*|eaten|eating)\b[^.]{0,70}\b(?:stronger|faster|harder|more intense|more potent|better high)\b|\b(?:stronger|faster|more intense|more potent)\b[^.]{0,50}\b(?:when|if)\s+(?:snorted|injected|smoked|swallowed|vaped|eaten)\b", re.I)),
    ("how to prepare or take a drug", re.compile(r"\b(?:crush(?:ed|ing)?|dissolv\w*|cook(?:ed|ing)? (?:it|the)|extract\w* (?:it|the)|filter\w* (?:it|the)|hold (?:it )?under the tongue|on an empty stomach)\b", re.I)),
    ("making an effect stronger", re.compile(r"\bpotentiat\w*|\b(?:boost|enhanc|intensif|strengthen)\w*\s+(?:the\s+)?(?:high|effects?|trip)\b|\bmak\w+\s+(?:it|the high|the effects?|the trip)\s+(?:stronger|last longer|more intense)\b", re.I)),
    ("advice or a promise of safety", re.compile(r"\byou\s+(?:should|must|need to|ought to|can safely|had better)\b|\b(?:it is|it's|is|are)\s+(?:completely |totally |perfectly |generally |relatively )?safe\b|\bsafe to\s+(?:take|use|mix|combine|drink|smoke)\b|\bharmless\b|\brisk-free\b|\bno risk\b|\bwe (?:recommend|advise|suggest)\b", re.I)),
    ("words that are not person-first", re.compile(r"\b(?:addicts?|junkies?|abusers?|misusers?|alcoholics?|druggies?|crackheads?|stoners?|potheads?|users?|microdosers?|smokers?|drinkers?|injectors?)\b|\babus(?:e|es|ed|ing|ive)\b|\bmisus(?:e|es|ed|ing)\b|\bclean\s+(?:from|for|since)\b", re.I)),
    ("a quotation or a source in brackets", re.compile(r'["“”]|\[[A-Z]{0,2}\d*\]|\(\s*(?:[A-Z][a-z]+ et al\.?|[A-Z][a-z]+,? \d{4})')),
    ("words about the lane itself", re.compile(r"\b(?:passages?|the (?:provided|given) (?:text|items?|findings)|findings? [FDL]?\d|item [FDL]\d|as an ai|language model)\b|\b(?:Papers?|Official pages?|Sources?) [A-H]\b|\b[FDL][A-H]?\d*\]", re.I)),
    ("a sign instead of a word", re.compile(r"[×≥≤±]|\b\d+x\b")),
]
LIMITS = {"short": 50, "but": 40}
CLINICAL = re.compile(r"\b(?:pharmacolog\w+|pharmacokinetic\w*|pharmacodynamic\w*|abstinence symptoms?|withdrawal syndrome|cessation|efficacy|tolerability|(?:a)?etiolog\w+|comorbid\w+|prevalence|cardiovascular|gastrointestinal|neurocognitive|psychopatholog\w+|sequelae|morbidity|contraindicat\w+|intoxication|symptomatolog\w+|adverse events?)\b", re.I)   # words the lead of an answer does not use: a plain word exists
YES_NO = re.compile(r"^(?:can|could|is|are|was|were|do|does|did|will|would|should|has|have|may|might)\b", re.I)
DIRECT = re.compile(r"^(?:yes|no|not|sometimes|probably|possibly|rarely|usually|often|it can|it may|it might|it could|it depends|it does|it is not known|it is possible|nobody knows|we do not know|for some|in some|only|partly|mostly|likely|unlikely|the sources)\b", re.I)


def lead(question, parts):
    """What the site's way of answering has against a draft's first two sentences: [(part, what)]. A question that can be
    answered with yes or no is answered so, first; the short answer and the But use everyday words."""
    bad = []
    for p in parts:
        if p["part"] not in ("short", "but"): continue
        m = CLINICAL.search(p["text"])
        if m: bad.append((p["part"], f"a clinical word where an everyday one exists (“{m.group(0)}”): say it plainly"))
        if p["part"] == "short" and YES_NO.search(question.strip()) and not DIRECT.search(p["text"].strip()):
            bad.append(("short", "the question can be answered with yes or no: begin the short answer with Yes, No, It can, Sometimes, It depends or Not known, then say why in plain words"))
    return bad


def own_but(sources, wanted_nearer):
    """A But the code writes itself, true by what the record holds: what this answer rests on, and that more exists. It
    stands in where the writer's But was not accepted (not supported by its source, or about something else)."""
    cn = counts(sources); n = lambda k, one, many: f"{k} {one if k == 1 else many}"
    kinds = [x for x in (n(cn["reviews"], "review", "reviews") if cn["reviews"] else "", n(cn["studies in people"], "study in people", "studies in people") if cn["studies in people"] else "",
                         n(cn["case reports"], "case report", "case reports") if cn["case reports"] else "", n(cn["official"], "official page", "official pages") if cn["official"] else "",
                         ("the summary of " + n(cn["summaries"], "paper", "papers")) if cn["summaries"] else "") if x]
    what = kinds[0] if len(kinds) == 1 else ", ".join(kinds[:-1]) + " and " + kinds[-1]
    return f"This rests on {what} that our system could read. " + ("A paper that stands nearer the question could not be read." if wanted_nearer else "It has not read every study on this question.")


def rules(parts, labels, years=()):
    """What the site's content rules have against a draft: [(part, what)]. Empty when nothing. years: the years the papers
    were published, which a sentence may name ("a 2022 review")."""
    bad = []
    for p in parts:
        for what, rx in RULES:
            m = rx.search(p["text"])
            if m: bad.append((p["part"], f"{what} (“{m.group(0)}”)"))
        if words(p["text"]) > LIMITS.get(p["part"], 40): bad.append((p["part"], f"too long ({words(p['text'])} words)"))
        have = set().union(*[numbers(labels[u]["quote"]) for u in p["uses"]])
        extra = numbers(p["text"]) - have - {str(y) for y in years}
        if extra: bad.append((p["part"], "a number that is not in the paper's words it rests on (" + ", ".join(sorted(extra)) + ")"))
    return bad


# ---------- 7 stakes ----------
STAKES = [("dying", re.compile(r"\b(?:die|dies|died|dying|death|deaths|deadly|fatal\w*|lethal\w*|kill|kills|killed|killing)\b", re.I)),
          ("overdose or an emergency", re.compile(r"\boverdos\w*|\bod(?:'?ing|'?ed)?\b|\bemergenc\w*|\bnaloxone\b|\bnarcan\b|\bpoisoning\b|\bunconscious\w*|\bnot breathing\b|\bseizures?\b|\boveramp\w*", re.I)),
          ("mixing drugs", re.compile(r"\b(?:mix|mixing|mixed|combin\w*|together with|at the same time|on top of|interact\w*)\b", re.I)),
          ("pregnancy or children", re.compile(r"\bpregnan\w*|\bbreast-?feed\w*|\bf(?:o)?etus\b|\bf(?:o)?etal\b|\bbab(?:y|ies)\b|\bbirth defects?\b|\bnewborns?\b|\bchild(?:ren)?\b|\bkids?\b|\bteen\w*|\badolescen\w*|\bminors?\b|\byouths?\b|\byoung people\b|\bp(?:a)?ediatric\w*|\binfants?\b|\btoddlers?\b|\bunderage\b|\bunder\s+(?:the\s+age\s+of\s+)?(?:1[0-8]|[1-9])\b|\bboys?\b|\bgirls?\b|\bschool\w*|\blactat\w*|\bnursing (?:mothers?|women)\b", re.I)),
          ("suicide or self-harm", re.compile(r"\bsuicid\w*|\bself-harm\w*", re.I))]


def stakes(question, parts):
    """Why this answer waits for a person, or "". The question decides first; then the answer's own words."""
    text = question + " " + " ".join(p["text"] for p in parts)
    for what, rx in STAKES:
        if rx.search(question) or (what != "mixing drugs" and rx.search(text)): return what
    return ""


# ---------- one answer ----------
def examples():
    S = json.load(open(ROOT / "data" / "site" / "simple.json", encoding="utf-8"))["claims"]
    out = [dict(S[i], q=S[i].get("q") or "") for i in ("cl_can_motivation", "cl_lsd_chromosomes", "cl_ket_bladder") if i in S and S[i].get("how") and S[i].get("but") and S[i].get("q")]
    if len(out) < 3: out += [v for k, v in sorted(S.items()) if v.get("how") and v.get("but") and v.get("q") and v not in out][:3 - len(out)]
    return [{"q": e["q"], "short": e["short"], "but": e["but"], "how": e["how"]} for e in out[:3]]


def lines():
    """The lines the code writes itself on an answer about amounts (data/auto/lane/lines.json)."""
    return json.load(open(LINES_FILE, encoding="utf-8"))


_web = []


def official_page(o):
    """An official page as it is now, read where it stands: (page, its reference), or None. o: what official.py wrote for it."""
    if not _web: _web.append(O.Web())
    src = next(iter(O.sources([o["body"]])), None)
    if not src: return None
    if o.get("label"):
        got = O.fda_label(o["label"], _web[0], src)
        return (got[0], got[2]) if got else None
    got = _web[0].get(o["address"])
    if not got or got[0][:5] == b"%PDF-": return None
    page = O.extract(O.text_of(got[0]), got[1])
    return page, O.reference(src, page, got[1])


def summary_of(doi):
    """The summary (abstract) of a paper whose full text cannot be read, as Europe PMC holds it: (the record, passages), or None."""
    got, _ = P.epmc_search(f'DOI:"{doi}"', 3)
    p = next((x for x in got if (x.get("doi") or "").lower() == doi.lower()), None)
    if not p or len(p.get("abstract") or "") < 200: return None
    parts, acc = [], ""
    for t in P.sentences(p["abstract"]) or [p["abstract"]]:
        if acc and len(acc) + len(t) > 900: parts.append(acc); acc = t
        else: acc = (acc + " " + t).strip()
    if acc: parts.append(acc)
    return p, [{"n": i + 1, "where": "Summary", "text": t} for i, t in enumerate(parts)]


def weight(s):
    """What a source counts for at the gate on sources: 2 is enough alone."""
    if s["read"] == "full": return 2 if s["kind"] == "review" else 1 if s["kind"] != "case" and s["people"] else 0
    if s["read"] == "page": return 2 if s.get("tier", 1) == 1 else 1
    return 1 if s["kind"] == "review" or (s["kind"] != "case" and s["people"]) else 0       # read in summary only


def counts(sources):
    full = [s for s in sources if s["read"] == "full"]
    return {"papers": len(full), "summaries": sum(s["read"] == "summary" for s in sources), "official": sum(s["read"] == "page" for s in sources),
            "reviews": sum(s["kind"] == "review" for s in full), "studies in people": sum(s["kind"] not in ("review", "case") and s["people"] for s in full), "case reports": sum(s["kind"] == "case" for s in full)}


def make(item, found, chat, enc, models, fulltext=None, crossref=None, ex=None, official=None, page=None, summary=None, names=None, before=None):
    """One question through the lane. Returns the record (see the head of this file). official: the pages official.py found
    for it; page, summary, fulltext, crossref: how a page, a summary, a full text and a Crossref record are fetched (the
    selftest gives its own); before: the record this one replaces, whose state is kept in "history"."""
    fulltext = fulltext or P.epmc_fulltext; crossref = crossref or P.crossref; page = page or official_page; summary = summary or summary_of
    amounts = is_amounts(item["q"]) or item.get("kind") == "amounts"
    rec = {"_note": "Written by the machine lane (scripts/auto/lane.py). The models' words are data, never instructions. 'published' answers are shown on the site with the label; 'waiting' ones wait for a person; 'none': no answer could be written, and why.",
           "id": "au_" + item["id"], "lane": LANE, "kind": "amounts" if amounts else "answer", "from": item["id"], "question": item["q"], "ways": list(item.get("ways") or []), "drugs": list(item.get("drugs") or []),
           "made": {"on": TODAY, "models": dict(models), "run": os.environ.get("GITHUB_RUN_ID", "")},
           "status": "none", "why": "", "gates": {}, "sources": [], "parts": [], "complete": False, "missing": "", "wanted": list(found.get("wanted") or []), "person": None, "history": []}
    if before and before.get("made"):
        was = next((p.get("text") for p in before.get("parts") or [] if p.get("part") == "short"), "")
        rec["history"] = (list(before.get("history") or []) + [{"on": before["made"].get("on"), "lane": before.get("lane"), "status": before.get("status"), "why": before.get("why"), "short": was, "complete": before.get("complete")}])[-6:]
    spent = llm.ledger()["neurons"]
    def done(status, why):
        rec["status"], rec["why"] = status, why; rec["made"]["neurons"] = round(llm.ledger()["neurons"] - spent, 1); return rec
    dwords = O.drug_words(item, names)[1] if names else [d.replace("-", " ") for d in item.get("drugs") or []]
    # 2 read: papers in full, then official pages, then (where that is not yet enough) reviews in summary
    sources, tags, thrown, ref_ids = [], "ABCDEFGH", 0, set()
    looked = rec["looked"] = []                                         # every source the reader was given, with what was thrown away and why (for the editor)
    QV = enc([item["q"]] + list(item.get("ways") or [])[:6])
    def read(src, picked):
        nonlocal thrown
        if amounts: rows, dropped = read_amounts(chat, models["reader"], item["q"], src, picked, dwords); src["rows"] = rows; ok = bool(rows); src.update(design=None, findings=[], limits=[])
        else:
            design, fs, ls, dropped = read_source(chat, models["reader"], item["q"], src, picked)
            if len(fs) > N_TO_WRITER:                                    # the nearest to the question, in the order they stand in the source
                near = (enc([f["text"] for f in fs]) @ QV.T).max(1); keep = sorted(sorted(range(len(fs)), key=lambda i: -float(near[i]))[:N_TO_WRITER]); fs = [fs[i] for i in keep]
            if len(ls) > 1: ls = [ls[int((enc([l["text"] for l in ls]) @ QV.T).max(1).argmax())]]      # one limit: the one nearest the question
            src.update(design=design, findings=fs, limits=ls[:1]); ok = bool(fs)
        thrown += len(dropped)
        looked.append({"title": src.get("title"), "read": src["read"], "kind": src.get("kind"), "at": src.get("address") or src.get("doi"), "kept": len(src.get("rows") or []) if amounts else len(src.get("findings") or []), "thrown": dropped[:12]})
        if not ok: return False
        ref = src["ref"]
        while ref["id"] in ref_ids: ref["id"] = ref["id"] + "b" if not re.search(r"[b-z]$", ref["id"]) else ref["id"][:-1] + chr(ord(ref["id"][-1]) + 1)
        ref_ids.add(ref["id"]); src["tag"] = tags[len(sources)]; src["_text"] = {p["n"]: p["text"] for p in picked}; sources.append(src)
        return True
    paper_ref = lambda doi, pmcid=None: (lambda cr: P.reference(doi, cr[0], pmcid) if cr[0] else None)(crossref(doi))
    def paper(c):
        """One paper read in full: True when it gave something."""
        if not c.get("doi"): return False
        if c["kind"] not in ("review", "study", "case") and not c.get("people"): return False   # an editorial, an opinion, a paper on animals or cells alone: not a source for an answer
        ref = paper_ref(c["doi"], c.get("pmcid"))
        if not ref or P.retraction(ref) in ("retracted", "concern"): return False      # GATE 6, first half: never a retracted paper
        xml = fulltext(c.get("pmcid"))
        if not xml: return False
        doc = P.jats_passages(xml)
        if len(doc["passages"]) < 4: return False
        picked = pick_passages(item["q"], item.get("ways"), doc["passages"], enc, c["kind"])
        return read({"read": "full", "ref": ref, "doi": c["doi"], "pmcid": c.get("pmcid"), "title": c["title"], "year": c.get("year"), "journal": c.get("journal"), "kind": c["kind"], "people": bool(c.get("people")), "near": c.get("near"), "money": doc["money"][:3]}, picked)
    n = 0; later = []
    for c in found.get("can_read") or []:
        if n >= N_PAPERS: later.append(c); continue
        n += paper(c)
    n = 0
    for o in official or []:
        if n >= (4 if amounts else N_OFFICIAL) or len(sources) >= len(tags) - 1: break
        if amounts and o.get("tier", 1) != 1: continue                                  # amounts only from a body of tier 1 or a medicine's label
        try: got = page(o)
        except (P.Refused, IOError, ValueError): continue
        if not got or len(got[0]["passages"]) < 2: continue
        pg, ref = got
        picked = pick_passages(item["q"], item.get("ways"), [dict(p, n=p["n"] + 1, where=p["where"] or "Top of the page") for p in pg["passages"]], enc, "review", k=7)
        n += read({"read": "page", "ref": ref, "title": pg["title"] or o.get("title") or "", "year": ((ref.get("issued") or {}).get("date-parts") or [[]])[0][:1] and ref["issued"]["date-parts"][0][0] or None, "kind": "official", "people": True,
                   "near": o.get("near"), "name": o["name"], "short": o.get("short") or o["name"], "tier": o.get("tier", 1), "address": ref.get("URL"), "money": [], "label": bool(o.get("label"))}, picked)
    for c in later:                                                     # a third paper (and no more) where what was read is not yet enough to rest on
        if (bool(sources) if amounts else sum(weight(s) for s in sources) >= 2) or len(sources) >= len(tags) - 1: break
        if paper(c): break
    if amounts or sum(weight(s) for s in sources) < 2 or not any(s["kind"] == "review" for s in sources):
        n = 0
        for w in found.get("wanted") or []:
            if n >= N_SUMMARIES or len(sources) >= len(tags): break
            if not w.get("doi"): continue
            ref = paper_ref(w["doi"])
            if not ref or P.retraction(ref) in ("retracted", "concern"): continue
            try: got = summary(w["doi"])
            except (P.Refused, IOError, ValueError): continue
            if not got: continue
            pp, passages = got
            n += read({"read": "summary", "ref": ref, "doi": w["doi"], "title": pp["title"], "year": pp.get("year"), "journal": pp.get("journal"), "kind": pp["kind"] if pp.get("kind") in ("review", "study", "case") else "review",
                       "people": bool(P.HUMAN.search(pp["title"] + " " + (pp.get("abstract") or ""))), "near": w.get("near"), "money": []}, passages)
    cn = counts(sources); rec["made"]["from"] = {k: cn[k] for k in ("papers", "summaries", "official")}
    rec["gates"]["read"] = (f"{sum(len(s.get('rows') or []) for s in sources)} amounts" if amounts else f"{sum(len(s['findings']) for s in sources)} findings") + f" kept from {len(sources)} sources ({cn['papers']} papers read in full, {cn['official']} official pages, {cn['summaries']} papers read in summary); {thrown} thrown away (the quote was not in the passage, or a number was not in the quote)"
    def keep_sources():
        rec["sources"] = [{k: v for k, v in s.items() if k != "_text"} for s in sources]
        cn = counts(sources); rec["made"]["from"] = {k: cn[k] for k in ("papers", "summaries", "official")}
    keep_sources()
    if not sources: return done("none", "no source that can be read " + ("states an amount for people" if amounts else "gave a finding") + " for this question")
    paper_name = lambda s: (f"{s['name']}: {s['title']}" if s["read"] == "page" else f"{s['title']} ({s['year']})")
    if amounts: return make_amounts(item, rec, sources, chat, models, done, keep_sources, paper_name)
    # GATE 6: enough to rest on
    said = lambda: f"{cn['reviews']} review(s) or meta-analyses, {cn['studies in people']} single studies in people, {cn['case reports']} case report(s) (which do not count), {cn['official']} official page(s), {cn['summaries']} paper(s) read in summary only"
    rec["gates"]["sources"] = said()
    labels, n_f, n_l = {}, 0, 0
    for s in sources:
        if s["design"]: labels["D" + s["tag"]] = dict(s["design"], paper=paper_name(s), ref=s["ref"]["id"], passage_text=s["_text"][s["design"]["passage"]])
        for f in s["findings"]: n_f += 1; f["id"] = f"F{n_f}"; labels[f["id"]] = dict(f, paper=paper_name(s), ref=s["ref"]["id"], passage_text=s["_text"][f["passage"]])
        for l in s["limits"]: n_l += 1; l["id"] = f"L{n_l}"; labels[l["id"]] = dict(l, paper=paper_name(s), ref=s["ref"]["id"], passage_text=s["_text"][l["passage"]])
    keep_sources()
    if sum(weight(s) for s in sources) < 2: return done("none", "not enough sources: an answer needs one review or meta-analysis read in full, or one official page, or two of: a study in people, a review read in summary, a page of a government-paid service")
    ex = ex if ex is not None else examples()
    # 3 write, 5 rules (one more try when a rule is broken), 4 check (one more try for the short answer or the But)
    fix, draft, verdicts = "", None, []
    for attempt in range(3):
        out = llm.as_json(chat(models["writer"], [{"role": "system", "content": WRITER_SYS}, {"role": "user", "content": writer_prompt(item["q"], sources, ex, fix)}], room_for(models["writer"], 900)))
        draft, why = draft_of(out, labels)
        if not draft:
            rec["gates"]["writer"] = (rec["gates"].get("writer", "") + f" try {attempt + 1}: {why}" + (f" (how the reply ended: {llm.LAST.get('finish')}; reasoned {llm.LAST.get('reasoned')} characters, wrote {llm.LAST.get('wrote')})" if llm.LAST else "")).strip()
            if fix.startswith("the form was wrong") and why == "no JSON": break       # the same call would fail the same way: not paid for a third time
            fix = "the form was wrong: " + why; continue
        bad = rules(draft["parts"], labels, [s["year"] for s in sources if s.get("year")] + sorted(numbers(item["q"]))) + lead(item["q"], draft["parts"])   # (a year a source was published in, or a number of the question itself, may be named)
        lines_bad = {p for p, _ in bad if p.startswith("how")}
        if bad and all(p.startswith("how") for p, _ in bad) and sum(p["part"].startswith("how") for p in draft["parts"]) > len(lines_bad):
            draft["parts"] = [p for p in draft["parts"] if p["part"] not in lines_bad]          # (lane 4) the line goes, the answer stays
            rec["gates"]["rules"] = f"{len(lines_bad)} How-do-we-know line(s) left out for a rule (" + "; ".join(f"{p}: {w}" for p, w in bad)[:300] + ")"; bad = []
        if bad: rec["gates"]["rules"] = "broken at try " + str(attempt + 1) + ": " + "; ".join(f"{p}: {w}" for p, w in bad); fix = "; ".join(f"in {p}: {w}" for p, w in bad); draft = None; continue
        whole = {}
        verdicts = check(chat, models["checker"], draft["parts"], labels, question=item["q"], whole=whole)
        # the second reader's word on the answer as a whole counts like its word on a sentence: a short answer that answers
        # another question, or a But about something else, is not accepted
        verdicts = [((v[0] and not (p["part"] == "short" and whole.get("answers") is False) and not (p["part"] == "but" and whole.get("but_fits") is False)),
                     v[1] if not v[0] else ("it does not answer the question itself" if p["part"] == "short" and whole.get("answers") is False else "it is about something else than the short answer" if p["part"] == "but" and whole.get("but_fits") is False else "") + (f" ({whole.get('why')})" if whole.get("why") and p["part"] in ("short", "but") and (whole.get("answers") is False or whole.get("but_fits") is False) else ""))
                    for p, v in zip(draft["parts"], verdicts)]
        head_bad = [(p["part"], v[1]) for p, v in zip(draft["parts"], verdicts) if not v[0] and p["part"] in ("short", "but")]
        if head_bad and attempt < 2:
            fix = "a second reader did not accept " + "; ".join(f"{p} ({w})" for p, w in head_bad) + ". Say only what the items say, answer the question itself, and let the But be a limit of that answer."
            rec["gates"]["check"] = "not accepted at try " + str(attempt + 1) + ": " + fix; draft = None; continue
        break
    if not draft:
        return done("none", "no draft passed: " + (rec["gates"].get("check") or rec["gates"].get("rules") or fix))
    by_part = {p["part"]: v for p, v in zip(draft["parts"], verdicts)}
    if by_part["short"][0] and not by_part["but"][0] and sum(v[0] for p, v in zip(draft["parts"], verdicts) if p["part"].startswith("how")) >= 1:
        # (lane 4) the short answer stands and only its But does not: the But is written by the code, from what the record
        # itself holds, and the answer is not thrown away for it
        used = {s["ref"]["id"] for s in sources if any(labels[u]["ref"] == s["ref"]["id"] for p, v in zip(draft["parts"], verdicts) if v[0] and p["part"] != "but" for u in p["uses"])}
        rest = [s for s in sources if s["ref"]["id"] in used]
        nearer = max([w.get("near") or 0 for w in rec["wanted"]] or [0]) > max([s.get("near") or 0 for s in rest if s["read"] != "summary"] or [0])
        i = next(i for i, p in enumerate(draft["parts"]) if p["part"] == "but")
        rec["gates"]["but"] = "the writer's But was not accepted (" + by_part["but"][1][:160] + "): the code wrote the But itself, from what this answer rests on"
        draft["parts"][i] = {"part": "but", "text": own_but(rest, nearer), "uses": [next(u for u in labels if labels[u]["ref"] == s["ref"]["id"]) for s in rest], "fixed": True}
        verdicts[i] = (True, "")
    kept = [(p, v) for p, v in zip(draft["parts"], verdicts) if v[0]]
    dropped_how = [p["part"] for p, v in zip(draft["parts"], verdicts) if not v[0] and p["part"].startswith("how")]
    if any(not v[0] for p, v in zip(draft["parts"], verdicts) if p["part"] in ("short", "but")) or sum(p["part"].startswith("how") for p, _ in kept) < 1:
        rec["gates"]["check"] = "; ".join(f"{p['part']}: {'accepted' if v[0] else 'NOT accepted: ' + v[1]}" for p, v in zip(draft["parts"], verdicts))
        return done("none", "the second reader did not accept the answer")
    rec["gates"]["check"] = f"every sentence kept was accepted by the second reader ({models['checker']})" + (f"; {len(dropped_how)} How-do-we-know line(s) dropped" if dropped_how else "") + ("; it also found that the short answer answers the question and that the But is about that answer" if whole.get("answers") and whole.get("but_fits") else "")
    rec["gates"].setdefault("rules", "nothing against it")
    if rec["gates"]["rules"].startswith("broken"): rec["gates"]["rules"] += "; written again, then nothing against it"
    parts = [p for p, _ in kept]; used_refs = []
    for p in parts:
        p["rests_on"] = [{"label": u, "ref": labels[u]["ref"], "where": labels[u]["where"], "quote": labels[u]["quote"], "sha": hashlib.sha256(norm(labels[u]["passage_text"]).encode("utf-8")).hexdigest()[:16]} for u in p["uses"]]
        for u in p["uses"]:
            if labels[u]["ref"] not in used_refs: used_refs.append(labels[u]["ref"])
        if p["part"].startswith("how"):                                # the source's own words under the line (the finding's, before the design's)
            for u in sorted(p["uses"], key=lambda u: (0 if u.startswith("F") else 1 if u.startswith("L") else 2)):
                show = words15(labels[u]["quote"], p["text"])
                if show: p["quote"], p["quote_ref"] = show, labels[u]["ref"]; break
    sources[:] = [s for s in sources if s["ref"]["id"] in used_refs]; keep_sources(); cn = counts(sources); rec["gates"]["sources"] = said() + " (the ones the answer rests on)"
    if sum(weight(s) for s in sources) < 2: return done("none", "after the second reader's check the answer rests on too few sources")
    rec["parts"] = parts
    best_wanted = max([w.get("near") or 0 for w in rec["wanted"] if w.get("doi") not in {s.get("doi") for s in sources}] or [0]); best_read = max([s.get("near") or 0 for s in sources if s["read"] != "summary"] or [0])
    in_summary = [s for s in sources if s["read"] == "summary"]
    rec["complete"] = bool(draft["complete"]) and not in_summary and not best_wanted > best_read
    rec["missing"] = draft["missing"] if not draft["complete"] else (f"{len(in_summary)} paper(s) could be read in summary only" if in_summary else "a paper that stands nearer the question could not be read" if not rec["complete"] else "")
    why = stakes(item["q"], parts)
    if why: return done("waiting", "about " + why + ": written, and waiting for a person before it is published")
    return done("published", "passed every gate")


def make_amounts(item, rec, sources, chat, models, done, keep_sources, paper_name):
    """An answer to a question about amounts (decision 11): rows in the sources' own words, each read by the second reader
    beside its passage, under the lines the code writes. No writer model."""
    # an amount stated for pregnancy, for children or about suicide is not the system's to publish: that row is left out
    # (a person's part); the question itself is looked at below
    for s in sources: s["rows"] = [r for r in s["rows"] if not any(rx.search(r["who"] + " " + r["what"] + " " + (r.get("clause") or r["quote"])) for what, rx in STAKES if what in ("pregnancy or children", "suicide or self-harm"))]
    L = lines(); rows = [(s, r) for s in sorted(sources, key=lambda s: 0 if s["read"] == "page" else 1 if s["read"] == "full" else 2) for r in s["rows"][:6]][:12]   # (official pages first, then papers read in full, then summaries)
    solid = lambda s: (s["read"] == "page" and s.get("tier", 1) == 1) or (s["read"] in ("full", "summary") and s["people"] and s["kind"] in ("review", "study"))
    rows = [(s, r) for s, r in rows if solid(s)]
    rec["gates"]["sources"] = f"{len(rows)} amounts from {len({s['ref']['id'] for s, _ in rows})} sources that count for amounts (an official body of tier 1, a medicine's label, a study in people)"
    if not rows: return done("none", "no official page and no study in people states an amount for this question")
    labels, parts = {}, []
    for i, (s, r) in enumerate(rows, 1):
        labels[f"R{i}"] = {"paper": paper_name(s), "where": r["where"], "passage_text": s["_text"][r["passage"]], "quote": r["quote"], "ref": s["ref"]["id"]}
        parts.append({"part": f"row{i}", "text": f"This amount was {r['what']}, for {r['who']}: {r['show']}", "uses": [f"R{i}"]})
    verdicts = check(chat, models["checker"], parts, labels, each=item["q"])
    kept = [(s, r, f"R{i}") for i, ((s, r), v) in enumerate(zip(rows, verdicts), 1) if v[0]]
    rec["gates"]["check"] = f"{len(kept)} of {len(rows)} amounts accepted by the second reader ({models['checker']})" + "".join(f"; not accepted: {v[1]}" for v in verdicts if not v[0])[:400]
    rec["gates"]["rules"] = "every quote stands in its source, holds a number with its unit and is cut to 15 words at most; no animal, no amount that harmed, no timing between uses"
    if not kept: return done("none", "the second reader did not accept any amount")
    used = {s["ref"]["id"] for s, _, _ in kept}; sources[:] = [s for s in sources if s["ref"]["id"] in used]; keep_sources()
    first = next((v["text"] for k, v in L["first"].items() if set(v["drugs"]) & set(item.get("drugs") or [])), "")
    guidance = bool(L.get("amounts_but_guidance")) and all(s["read"] == "page" and not s.get("label") for s in sources)     # every amount is an official body's guidance (no medicine's label, no study): the But that is true of that
    out = ([{"part": "first", "text": first, "fixed": True, "rests_on": []}] if first else []) + [{"part": "short", "text": L["amounts"], "fixed": True, "rests_on": []}, {"part": "but", "text": L["amounts_but_guidance" if guidance else "amounts_but"], "fixed": True, "rests_on": []}]
    for n, (s, r, lab) in enumerate(kept, 1):
        who = r["who"][0].upper() + r["who"][1:]
        out.append({"part": f"row{n}", "text": f"{who}; {r['what']}.", "who": who, "what": r["what"], "quote": r["show"], "source": s["ref"]["id"], "read": s["read"], "uses": [lab],
                    "rests_on": [{"label": lab, "ref": s["ref"]["id"], "where": r["where"], "quote": r["quote"], "sha": hashlib.sha256(norm(s["_text"][r["passage"]]).encode("utf-8")).hexdigest()[:16]}]})
    rec["parts"] = out
    rec["complete"] = len(used) >= 2 and not any(s["read"] == "summary" for s in sources)
    rec["missing"] = "" if rec["complete"] else ("a paper could be read in summary only" if any(s["read"] == "summary" for s in sources) else "only one source states an amount")
    why = stakes(item["q"], [{"text": p.get("who", "") + " " + p.get("what", "")} for p in out if p["part"].startswith("row")])
    if why: return done("waiting", "about " + why + ": written, and waiting for a person before it is published")
    return done("published", "passed every gate (an answer about amounts: decision 11)")


# ---------- the run ----------
def _searched(path):
    """The day a finder last searched for a question ("" where it has not)."""
    try: return str(json.load(open(path, encoding="utf-8")).get("searched_on") or "")
    except (OSError, ValueError): return ""


def turn_of(w, done):
    """When a question's turn comes (the smaller, the sooner), or None when there is nothing to do for it: a question never
    tried (0); one whose answer an older lane wrote (1); the second look: an answer that is not complete, or no answer, for
    which the finders have found something since it was written (2); no answer for a week (3). done: the lane's state."""
    s = done.get(w["id"]) or {}
    if not s: return 0
    if int(s.get("lane") or 1) < LANE: return 1
    newer = max([_searched(ROOT / "data" / "auto" / "papers" / (w["id"] + ".json")), _searched(FOUND_OFFICIAL / (w["id"] + ".json"))])
    if (s.get("status") == "none" or s.get("complete") is False) and newer > s.get("last", ""): return 2
    if s.get("status") == "none" and s.get("last", "") < (datetime.date.today() - datetime.timedelta(days=7)).isoformat(): return 3
    return None


def load_state():
    try: return json.load(open(STATE, encoding="utf-8"))
    except (OSError, ValueError): return {"items": {}}


def wanted_list():
    """Every paper the lane wants and cannot read, with the questions it is wanted for (for the senior author's list)."""
    by = {}
    for f in sorted(OUT.glob("au_*.json")):
        a = json.load(open(f, encoding="utf-8"))
        if a["status"] == "published" and a["complete"]: continue
        for w in a.get("wanted") or []:
            x = by.setdefault(w["doi"], dict(w, **{"for": []}))
            if a["question"] not in x["for"]: x["for"].append(a["question"])
    return sorted(by.values(), key=lambda w: (-len(w["for"]), -(w.get("near") or 0), w["doi"]))


def run(ids=None, limit=3, again=False, chat=None, enc=None):
    models = dict(MODELS)
    stand_in = {}
    if MODELS_FILE.exists():
        mf = json.load(open(MODELS_FILE, encoding="utf-8")); models.update({k: v for k, v in mf.items() if k in MODELS and isinstance(v, str)})
        # where a second free service's key exists (llm.has), the roles named for it are done there; when its free day is used up or it
        # cannot be reached, the role goes back to the model named above for the rest of the call
        for role, m in (mf.get("with_groq") or {}).items() if chat is None and isinstance(mf.get("with_groq"), dict) else []:
            if role in MODELS and isinstance(m, str) and llm.has(m) and m != models.get(role): stand_in[m] = models[role]; models[role] = m
    if chat is None and stand_in:
        def chat(model, messages, room=700):
            try: return llm.chat(model, messages, room)
            except (llm.Budget, llm.Unavailable) as e:
                if model not in stand_in: raise
                print(f"lane: {model} could not be used ({str(e)[:120]}): {stand_in[model]} stands in"); return llm.chat(stand_in[model], messages, room)
        chat.real = True
    chat = chat or llm.chat
    items = P.listed()
    st = load_state(); order = []
    rep = ROOT / "data" / "auto" / "report.json"
    asked = {w["id"]: w.get("asked", 0) + w.get("sent_too", 0) for w in (json.load(open(rep, encoding="utf-8")).get("wanted") or [])} if rep.exists() else {}
    turn = lambda w: turn_of(w, st["items"])
    # a question a visitor sent comes first (it was promised), then what the most people wait for
    for w in sorted(items, key=lambda w: (0 if w.get("from") == "a question visitors sent" else 1, -(asked.get(w["id"], 0) + int(w.get("asked") or 0)), w["id"])):
        if ids:
            if w["id"] in ids: order.append(w)
        elif again or turn(w) is not None: order.append(w)
    if not ids and not again: order.sort(key=lambda w: turn(w))                    # (a stable sort: within one turn, the most asked first)
    enc = enc or P.General(); import build_index as bi; names = bi.names_table(); made = []
    OUT.mkdir(parents=True, exist_ok=True); STATE.parent.mkdir(parents=True, exist_ok=True)
    for w in order[:limit]:
        if (chat is llm.chat or getattr(chat, "real", False)) and llm.left() < ROOM: print(f"lane: today's free allowance has {llm.left():.0f} neurons left, not enough for one more answer: it goes on tomorrow"); break   # (an answer begun and not finished is lost, and its neurons with it: on 15 November 563 went that way)
        pf = ROOT / "data" / "auto" / "papers" / (w["id"] + ".json"); of = FOUND_OFFICIAL / (w["id"] + ".json"); af = OUT / ("au_" + w["id"] + ".json")
        try:
            found = json.load(open(pf, encoding="utf-8")) if pf.exists() and not again else P.find(w, names, enc)
            if not pf.exists() or again: pf.parent.mkdir(parents=True, exist_ok=True); json.dump(found, open(pf, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            try: official = json.load(open(of, encoding="utf-8"))["pages"]
            except (OSError, ValueError, KeyError): official = []               # (official.py has not searched for this question yet, or found nothing)
            try: before = json.load(open(af, encoding="utf-8"))
            except (OSError, ValueError): before = None
            rec = make(w, found, chat, enc, models, official=official, names=names, before=before)
        except llm.Budget as e: print("lane: stopped for today:", e); break
        except llm.Unavailable as e: print("lane: the models cannot be used now:", e); break
        except P.Refused as e: print("lane: a source said no:", e); break
        except Exception as e:                                           # a fault of the lane itself on this question: written down, and the question is not tried again by this lane (it would fail the same way and spend the day's allowance)
            import traceback
            print(f"lane: {w['id']}: the lane itself failed ({type(e).__name__}: {str(e)[:200]})"); print("".join(traceback.format_exc().splitlines(True)[-6:]))
            st["items"][w["id"]] = {"status": "none", "why": f"the lane itself failed on it ({type(e).__name__})", "last": TODAY, "lane": LANE, "kind": "", "complete": False, "tries": int((st["items"].get(w["id"]) or {}).get("tries") or 0) + 1}
            json.dump(st, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1); continue
        try:                                                           # where the answer belongs on the site (scripts/auto/place.py): a drug's page, a page to start, or one of the general pages
            import place; pl = place.Placer(names).place(w["q"], w.get("ways") or []); rec["place"] = {k: pl[k] for k in ("home", "also", "cls", "why")}
        except Exception as e: rec["place"] = {"home": None, "why": "the place could not be worked out: " + str(e)[:120]}
        json.dump(rec, open(OUT / (rec["id"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        st["items"][w["id"]] = {"status": rec["status"], "why": rec["why"], "last": TODAY, "lane": LANE, "kind": rec["kind"], "complete": rec["complete"], "tries": int((st["items"].get(w["id"]) or {}).get("tries") or 0) + 1}
        json.dump(st, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1); made.append(rec)
        f = rec["made"].get("from") or {}
        print(f"lane: {w['id']} {w['q'][:56]!r}: {rec['status']} ({rec['why']}); {f.get('papers', 0)} papers, {f.get('official', 0)} official pages, {f.get('summaries', 0)} summaries; {rec['made'].get('neurons', 0)} neurons")
    json.dump({"_note": "Papers the machine lane wants and cannot read (their full text is not open), with the questions they are wanted for. References from Crossref, made by scripts/build_references.py. For the senior author's list of papers to save.",
               "made_on": TODAY, "papers": wanted_list()}, open(WANTED, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"lane: {len(made)} questions worked on: " + ", ".join(f"{k} {sum(r['status'] == k for r in made)}" for k in ("published", "waiting", "none")) + f"; today {llm.ledger()['neurons']:.0f} of {llm.OUR_LIMIT} neurons used")
    return made


def selftest():
    import tempfile, numpy as np
    global OUT, STATE, WANTED
    tmp = pathlib.Path(tempfile.mkdtemp()); llm.LEDGER = tmp / "usage.json"
    passages = ["Ketamine use has risen in several countries and many clinicians now see people who use it often, which is why this review was written for them.",
                "Across 12 studies of 2,405 people who used ketamine regularly, between 9% and 27% met criteria for dependence, with higher rates among those using it daily.",
                "Tolerance developed quickly in frequent use, and many participants described cravings and difficulty stopping despite bladder symptoms.",
                "Most included studies were cross-sectional surveys of volunteers recruited online, so the rates may not hold for everyone who uses ketamine.",
                "Withdrawal symptoms such as anxiety, shaking and sweating were reported by 28 of 30 daily users in one small study from Hong Kong.",
                "The authors thank the staff of the library for their help with the searches that were done for this review of the literature."]
    xml = "<article><front><article-meta><abstract><p>" + passages[0] + "</p></abstract></article-meta></front><body><sec><title>Results</title>" + "".join(f"<p>{p}</p>" for p in passages[1:3]) + "</sec><sec><title>Discussion</title><sec><title>Limitations</title><p>" + passages[3] + "</p></sec><p>" + passages[4] + "</p></sec><sec><title>Acknowledgments</title><p>" + passages[5] + "</p></sec></body></article>"
    found = {"can_read": [{"doi": "10.1000/k.1", "pmcid": "PMC1", "title": "Ketamine dependence: a systematic review", "year": 2022, "journal": "Addiction", "kind": "review", "people": True, "near": 0.71},
                          {"doi": "10.1000/k.9", "pmcid": "PMC9", "title": "A retracted paper", "year": 2020, "journal": "X", "kind": "study", "people": True, "near": 0.6}],
             "wanted": [{"doi": "10.1000/w.1", "apa": "Wanted, A. (2021). A review behind a paywall. Journal, 1, 1–2. https://doi.org/10.1000/w.1", "near": 0.5, "why": "x", "file": "wanted_2021_w_1.pdf"}]}
    def crossref(doi):
        if doi.endswith("k.9"): return {"DOI": doi, "type": "journal-article", "title": "A retracted paper", "au": [["Bad", "B."]], "ct": "X", "issued": [2020], "upd": ["retraction:10.1000/r"]}, None
        return {"DOI": doi, "type": "journal-article", "title": "Ketamine Dependence: A Systematic Review", "au": [["Lee", "Min"], ["Chan", "Kit"]], "ct": "Addiction", "vol": "117", "iss": "2", "pg": "300-312", "issued": [2022], "print": [2022], "upd": []}, None
    class Enc:
        def __call__(self, texts):
            ws = "ketamine addicted addictive dependence tolerance cravings withdrawal stopping studies review".split()
            M = np.array([[1.0 if w in t.lower() else 0.0 for w in ws] + [0.05] for t in texts], np.float32); return M / np.linalg.norm(M, axis=1, keepdims=True)
    good_reader = {"design": {"text": "A review of 12 studies of 2,405 people who used ketamine regularly", "quote": "Across 12 studies of 2,405 people who used ketamine regularly", "passage": 2},
                   "findings": [{"passage": 2, "quote": "between 9% and 27% met criteria for dependence, with higher rates among those using it daily", "finding": "Between 9% and 27% of people who used ketamine regularly met criteria for dependence."},
                                {"passage": 3, "quote": "Tolerance developed quickly in frequent use, and many participants described cravings and difficulty stopping", "finding": "With frequent use, tolerance came quickly and many people described cravings and trouble stopping."},
                                {"passage": 2, "quote": "half of all people who ever try ketamine become dependent within a year", "finding": "Half of people who try ketamine become dependent."},          # not in the paper: thrown away
                                {"passage": 3, "quote": "Tolerance developed quickly in frequent use, and many participants described cravings", "finding": "Tolerance developed in 80% of people."}],  # a number not in the quote: thrown away
                   "limits": [{"passage": 4, "quote": "Most included studies were cross-sectional surveys of volunteers recruited online, so the rates may not hold for everyone who uses ketamine", "limit": "Most studies were online surveys of volunteers, so the rates may not hold for everyone who uses ketamine."}]}
    script = {"writer": [], "checker": [], "amounts": []}; calls = []
    def chat(model, messages, max_tokens=0):
        sysm = messages[0]["content"]; role = "reader" if sysm.startswith("You read") else "writer" if sysm.startswith("You write") else "checker"; calls.append((role, model, messages[1]["content"]))
        llm.spend(model, 1000, 100, save=True)
        if role == "reader" and "list the AMOUNTS" in messages[1]["content"]: return json.dumps(script["amounts"].pop(0))
        if role == "reader": return "<think>reading</think>" + json.dumps(good_reader)
        return json.dumps(script[role].pop(0))
    W = lambda short, but="Most studies were online surveys of volunteers, so the rates may not hold for everyone who uses ketamine.", how=None: {
        "short": {"text": short, "uses": ["F1"]}, "but": {"text": but, "uses": ["L1"]},
        "how": how or [{"text": "A review of 12 studies of 2,405 people who used ketamine regularly found that between 9% and 27% met criteria for dependence.", "uses": ["DA", "F1"]},
                       {"text": "With frequent use, tolerance came quickly and many people described cravings and trouble stopping.", "uses": ["F2"]}], "complete": True, "missing": ""}
    ok_short = "Yes. In a review of studies, between 9% and 27% of people who used ketamine regularly met criteria for dependence."
    V = lambda *xs: {"verdicts": [{"n": i + 1, "supported": x is True, "problem": "" if x is True else x} for i, x in enumerate(xs)]}
    item = {"id": "w_0024", "q": "Can you get addicted to ketamine?", "ways": ["is ketamine addictive"]}
    ex = [{"q": "Q?", "short": "S.", "but": "B.", "how": ["H1.", "H2."]}] * 3
    mk = lambda it=item: make(it, found, chat, Enc(), MODELS, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex)
    # 1. the straight way: published; the retracted paper never read; two bad findings thrown away; not complete (a nearer paper... is not nearer: complete)
    script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True)]
    r = mk()
    assert r["status"] == "published" and r["id"] == "au_w_0024" and len(r["sources"]) == 1 and r["sources"][0]["ref"]["id"] == "lee_2022" and r["complete"] is True, (r["status"], r["why"], r["gates"])
    assert "2 thrown away" in r["gates"]["read"] and [p["part"] for p in r["parts"]] == ["short", "but", "how1", "how2"] and r["parts"][0]["rests_on"][0]["quote"].startswith("between 9% and 27%"), r["gates"]
    # under each How-do-we-know line: the source's own words, 15 at most, found in the quote the record keeps; none under the short answer or the But
    hq = [(p.get("quote"), p.get("quote_ref")) for p in r["parts"]]
    assert hq[0] == (None, None) and hq[1] == (None, None) and hq[2] == ("between 9% and 27% met criteria for dependence", "lee_2022") and words(hq[2][0]) <= 15 and hq[3][0] and hq[3][0] in good_reader["findings"][1]["quote"], hq
    assert words15("In this cohort the participants who were daily users of the drug reported more cravings than the others did across all waves", "People who used it daily reported more cravings.") is None      # the paper's word "users": not shown
    w15 = words15("Across the whole sample and in every wave of the survey that was run, many participants described cravings and difficulty stopping despite symptoms", "Many people described cravings and trouble stopping.")
    assert w15 == "many participants described cravings and difficulty stopping despite symptoms", w15
    assert sum(c[0] == "reader" for c in calls) == 1 and "A retracted paper" not in " ".join(c[2] for c in calls)                       # the retracted paper was not read
    assert "[1]" in calls[0][2] and "[6]" not in calls[0][2] and "library" not in calls[0][2]                                              # the acknowledgments are not a passage
    assert calls[1][1] == MODELS["writer"] and calls[2][1] == MODELS["checker"] and MODELS["writer"] != MODELS["checker"] and "PASSAGE (Ketamine dependence: a systematic review (2022); Results)" in calls[2][2]
    # 2. a rule broken (an amount, and a word that is not person-first), written again; a How line the checker refuses is dropped
    calls.clear(); script["writer"] = [W("Yes: users who took 50 mg a day got addicted."), W(ok_short)]; script["checker"] = [V(True, True, True, "the passage does not say trouble stopping was common")]
    r = mk(); assert r["status"] == "published" and len(r["parts"]) == 3 and "broken at try 1" in r["gates"]["rules"] and "1 How-do-we-know line(s) dropped" in r["gates"]["check"], r["gates"]
    assert "YOUR LAST ANSWER BROKE THESE RULES" in [c for c in calls if c[0] == "writer"][1][2]
    # 3. a number that is not in the paper's words: refused by code even though the checker would not be asked
    script["writer"] = [W("Yes. About 40% of people who used ketamine regularly met criteria for dependence.")] * 3; script["checker"] = []
    r = mk(); assert r["status"] == "none" and "a number that is not in the paper's words" in r["why"], r["why"]
    # 4. the checker refuses the short answer twice: no answer
    script["writer"] = [W(ok_short)] * 3; script["checker"] = [V("stronger than the passage", True, True, True)] * 3
    r = mk(); assert r["status"] == "none" and r["why"] == "the second reader did not accept the answer" or "no draft passed" in r["why"], r["why"]
    # (lane 4) a question that can be answered with yes or no is answered so, first, and in everyday words: written again when it is not
    assert len(lead(item["q"], [{"part": "short", "text": "People with ketamine use disorder experience abstinence symptoms."}])) == 2 and not lead("What is synthetic weed like?", [{"part": "short", "text": "Synthetic weed is riskier."}]) and not lead(item["q"], [{"part": "short", "text": ok_short}])
    calls.clear(); script["writer"] = [W("People who use ketamine regularly can become dependent on it."), W(ok_short)]; script["checker"] = [V(True, True, True, True)]
    r = mk(); assert r["status"] == "published" and "yes or no" in r["gates"]["rules"] and "begin the short answer with Yes" in [c for c in calls if c[0] == "writer"][1][2], r["gates"]
    # the second reader also judges the answer as a whole. A But about something else, three times: the code writes the But from what the answer rests on, and the answer stands
    off = dict(V(True, True, True, True), answers_question=True, but_fits=False, why="it is about a treatment")
    calls.clear(); script["writer"] = [W(ok_short)] * 3; script["checker"] = [off] * 3
    r = mk(); assert r["status"] == "published" and r["parts"][1]["text"] == "This rests on 1 review that our system could read. It has not read every study on this question." and r["parts"][1]["rests_on"] and "the code wrote the But itself" in r["gates"]["but"], (r["status"], r["why"], r["parts"][1:2], r["gates"])
    assert "QUESTION that was asked: Can you get addicted to ketamine?" in [c for c in calls if c[0] == "checker"][0][2] and "a second reader did not accept but (it is about something else than the short answer" in [c for c in calls if c[0] == "writer"][1][2]
    # a short answer that answers another question, three times: no answer
    script["writer"] = [W(ok_short)] * 3; script["checker"] = [dict(V(True, True, True, True), answers_question=False, but_fits=True, why="it says how it is treated")] * 3
    r = mk(); assert r["status"] == "none" and "it does not answer the question itself" in r["gates"]["check"], (r["status"], r["why"], r["gates"])
    assert own_but([{"read": "full", "kind": "review", "people": True}, {"read": "full", "kind": "study", "people": True}, {"read": "page", "kind": "official", "people": True}, {"read": "page", "kind": "official", "people": True}], True) == "This rests on 1 review, 1 study in people and 2 official pages that our system could read. A paper that stands nearer the question could not be read."
    # 5. a question about dying: written, checked, and it waits for a person
    script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True)]
    r = mk({"id": "w_0027", "q": "Can ketamine kill you?", "ways": []}); assert r["status"] == "waiting" and "dying" in r["why"], (r["status"], r["why"])
    # 6. a single study alone is not enough
    found1 = {"can_read": [dict(found["can_read"][0], kind="study")], "wanted": []}
    script["writer"] = []; r = make(item, found1, chat, Enc(), MODELS, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex); assert r["status"] == "none" and "not enough sources" in r["why"], r["why"]
    # 7. a wanted paper that stands nearer than the ones read: published, and not complete
    found2 = dict(found, wanted=[dict(found["wanted"][0], near=0.9)]); script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True)]
    r = make(item, found2, chat, Enc(), MODELS, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex); assert r["status"] == "published" and r["complete"] is False and "could not be read" in r["missing"], r
    # lane 4. GATE 3: a sentence about something else than its quote is thrown away; a name with a figure is not a number; an item with an amount never reaches the writer of an ordinary answer
    assert not carried("The page does not provide information on what is in fake Xanax bars.", "Developing tolerance means that, over time, you need more of the drug to get the same effect.", "Developing tolerance means that, over time, you need more of the drug to get the same effect.")
    assert not carried("Mixing synthetic cannabinoids with alcohol and other drugs can increase the risk of serious effects or overdose.", "Avoid mixing synnies with alcohol and other drugs.", "Avoid mixing synnies with alcohol and other drugs.")
    assert carried("The risk of inducing psychosis is higher with SCs than with natural cannabis.", "In 2015, Van Amsterdam et al showed that psychosis-inducing risk is higher with SCs than with natural cannabis.", "In 2015, Van Amsterdam et al showed that psychosis-inducing risk is higher with SCs than with natural cannabis.")
    assert numbers("Spice, K2 and 2C-B act on CB1") == set() and numbers("K2 was used by 11.4% of seniors") == {"11.4"}
    pk = [{"n": 1, "where": "Results", "text": "Counterfeit tablets held etizolam, ranging from 0.7 to 8.3 mg per tablet, and etizolam was the most frequently detected compound in the tablets."}]
    g = read_gate({"findings": [{"passage": 1, "quote": "ranging from 0.7 to 8.3 mg per tablet", "finding": "Etizolam in counterfeit tablets ranged from 0.7 to 8.3 mg per tablet."},
                                {"passage": 1, "quote": "etizolam was the most frequently detected compound in the tablets", "finding": "Etizolam was the compound most often detected in the tablets."}]}, pk, amounts_ok=False)
    assert [f["text"] for f in g[1]] == ["Etizolam was the compound most often detected in the tablets."] and len(g[3]) == 1 and "amount" in g[3][0]["why"], g
    assert len(read_gate({"findings": [{"passage": 1, "quote": "ranging from 0.7 to 8.3 mg per tablet", "finding": "Etizolam in counterfeit tablets ranged from 0.7 to 8.3 mg per tablet."}]}, pk)[1]) == 1     # (for an answer about amounts it stays)
    # a How-do-we-know line that breaks a rule is left out and the answer stays
    script["writer"] = [W(ok_short, how=[{"text": "A review of 12 studies of 2,405 people who used ketamine regularly found that between 9% and 27% met criteria for dependence.", "uses": ["DA", "F1"]},
                                         {"text": "In one study people were given 50 mg of it.", "uses": ["F2"]}])]; script["checker"] = [V(True, True, True)]
    r = make(item, found, chat, Enc(), MODELS, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex)
    assert r["status"] == "published" and [x["part"] for x in r["parts"]] == ["short", "but", "how1"] and r["gates"]["rules"].startswith("1 How-do-we-know line(s) left out for a rule"), (r["status"], r["why"], r["gates"])
    assert room_for("@cf/openai/gpt-oss-120b", 900) == 3100 and room_for("@cf/meta/llama-3.3-70b-instruct-fp8-fast", 900) == 900
    # 8. an official page alone (a body of tier 1) is enough; the answer names the body; its reference is the page's own
    page_ps = [{"n": i, "where": "The risks" if i else "", "text": t} for i, t in enumerate(passages[1:5])]
    nhs = {"body": "nhs", "name": "NHS", "short": "the NHS", "tier": 1, "address": "https://nhs.test/ketamine", "title": "Ketamine", "near": 0.6}
    web_ref = lambda who="NHS": {"id": "nhs_ketamine", "type": "webpage", "title": "Ketamine", "author": [{"literal": who, "short": "the NHS"}], "issued": {"date-parts": [[2025, 3, 2]]}, "URL": "https://nhs.test/ketamine", "accessed": {"date-parts": [[2026, 11, 15]]}}
    page = lambda o: ({"title": "Ketamine", "passages": page_ps}, web_ref())
    nhs_short = "Yes. The NHS says that between 9% and 27% of people who used ketamine regularly met criteria for dependence."
    calls.clear(); script["writer"] = [W(nhs_short)]; script["checker"] = [V(True, True, True, True)]
    r = make(item, {"can_read": [], "wanted": []}, chat, Enc(), MODELS, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex, official=[nhs], page=page)
    assert r["status"] == "published" and r["made"]["from"] == {"papers": 0, "summaries": 0, "official": 1} and r["sources"][0]["ref"]["type"] == "webpage" and r["sources"][0]["read"] == "page", (r["status"], r["why"], r["gates"])
    assert 'OFFICIAL PAGE: "Ketamine", a page of NHS for the public (2025).' in calls[0][2] and '"design"' not in calls[0][2] and 'OFFICIAL PAGE A: "Ketamine", a page of NHS (2025). When you use it, name the body: "The NHS says".' in calls[1][2], calls[1][2][:600]
    assert "PASSAGE (NHS: Ketamine; The risks)" in calls[2][2]
    # a page of a government-paid service (tier 2) alone is not enough; with one study in people it is
    lvl = dict(nhs, body="thelevel", name="NZ Drug Foundation", short="the NZ Drug Foundation", tier=2)
    r = make(item, {"can_read": [], "wanted": []}, chat, Enc(), MODELS, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex, official=[lvl], page=page); assert r["status"] == "none" and "not enough sources" in r["why"], r["why"]
    two = W(ok_short, how=[{"text": "A study of 2,405 people who used ketamine regularly found that between 9% and 27% met criteria for dependence.", "uses": ["DA", "F1"]}, {"text": "The NZ Drug Foundation says tolerance comes quickly with frequent use.", "uses": ["F4"]}])
    script["writer"] = [two]; script["checker"] = [V(True, True, True, True)]
    r = make(item, found1, chat, Enc(), MODELS, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex, official=[lvl], page=page); assert r["status"] == "published" and r["made"]["from"] == {"papers": 1, "summaries": 0, "official": 1}, (r["status"], r["why"])
    # 9. a review behind a paywall is read in summary where the rest is not enough: published, said, and never complete
    summ = lambda doi: ({"title": "A review behind a paywall", "year": 2021, "journal": "Journal", "kind": "review", "abstract": " ".join(passages[1:4])}, [{"n": 1, "where": "Summary", "text": passages[1]}, {"n": 2, "where": "Summary", "text": passages[2] + " " + passages[3]}])
    calls.clear(); script["writer"] = [W(ok_short, how=[{"text": "A study of 2,405 people who used ketamine regularly found that between 9% and 27% met criteria for dependence.", "uses": ["DA", "F1"]},
                                                         {"text": "The summary of a 2021 review says that tolerance came quickly with frequent use.", "uses": ["F4"]}])]; script["checker"] = [V(True, True, True, True)]
    r = make(item, dict(found1, wanted=found["wanted"]), chat, Enc(), MODELS, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex, summary=summ)
    assert r["status"] == "published" and r["complete"] is False and "summary only" in r["missing"] and r["made"]["from"] == {"papers": 1, "summaries": 1, "official": 0} and [x["read"] for x in r["sources"]] == ["full", "summary"], (r["status"], r["why"], r["missing"])
    assert "PAPER (only its summary could be read): A review behind a paywall (2021)" in calls[1][2] and "PAPER B (ONLY ITS SUMMARY COULD BE READ)" in [c for c in calls if c[0] == "writer"][0][2]
    assert sum(c[0] == "reader" for c in calls) == 2                                              # with a review read in full, no summary is fetched (tests 1 to 7 never called summary)
    # the answer it replaces is kept in its history
    r2 = make(item, found, chat.__class__ and chat, Enc(), MODELS, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex, before=r) if (script["writer"].append(W(ok_short)) or script["checker"].append(V(True, True, True, True)) or True) else None
    assert r2["history"] and r2["history"][-1]["short"] == ok_short and r2["history"][-1]["complete"] is False and r2["history"][-1]["status"] == "published", r2["history"]
    # 10. a question about amounts (decision 11): rows in the source's own words, no writer; an animal's amount, an amount that killed, an amount with its timing and a quote that is not there are thrown away
    assert is_amounts("What amounts of MDMA have studies given to people?") and is_amounts("what dosage is safe in MDMA") and is_amounts("How much alcohol is too much?") and not is_amounts("How much does cannabis affect memory?") and not is_amounts("How long does ketamine stay in your system?") and not is_amounts("Is microdosing LSD safe?")
    assert window15("Participants received 80 to 120 mg of MDMA in each of three sessions, with two trained therapists present throughout") == "Participants received 80 to 120 mg of MDMA in each of three sessions"
    assert window15("Initiate treatment with 5 to 15 mg every 4 to 6 hours as needed for pain") == "Initiate treatment with 5 to 15 mg" and window15("no amount here at all, only words that go on") is None
    assert REDOSE.search("A supplemental half-dose of 40 to 60 mg was offered") and REDOSE.search("redosing after an hour") and not REDOSE.search("a daily dose of 20 mg")
    # (lane 4) a cut never changes what the source says: the words that limit an amount, or turn it round, and the words that belong to it stay with it
    for q, want in [("men and women are advised not to drink more than 14 units a week on a regular basis", "men and women are advised not to drink more than 14 units a week"),
                    ("2 drinks or less in a day for men and 1 drink or less in a day for women", "2 drinks or less in a day for men"),
                    ("For healthy adults, the FDA has cited 400 milligrams a day as an amount not generally associated with dangerous, negative effects", "For healthy adults, the FDA has cited 400 milligrams a day"),
                    ("Healthy adults who are not pregnant should have no more than 400 mg of caffeine a day, which is about three cups of brewed coffee", "who are not pregnant should have no more than 400 mg of caffeine a day"),
                    ("A total of 59 patients were randomly assigned to receive two separate doses of 25 mg of psilocybin 3 weeks apart plus 6 weeks of daily placebo", "two separate doses of 25 mg of psilocybin"),
                    ("Women who were not given the 25 mg dose of psilocybin in the first session received it later in the study", "Women who were not given the 25 mg dose of psilocybin in the first session"),
                    ("Esketamine nasal spray was given at 56 mg or 84 mg twice weekly during a four-week induction phase, in addition to a newly started oral antidepressant", "Esketamine nasal spray was given at 56 mg or 84 mg twice weekly"),
                    ("Low-risk drinking for women was defined as no more than 3 drinks on any single day and no more than 7 drinks per week", "no more than 3 drinks on any single day"),
                    ("Patients in maintenance treatment are commonly stabilized at 80 to 120 mg a day once tolerance to methadone has developed", "Patients in maintenance treatment are commonly stabilized at 80 to 120 mg a day")]:
        assert window15(q) == want, (q, window15(q))
    assert words15("In this cohort, regular cannabis use was not associated with a higher risk of psychosis once tobacco smoking and family history were taken into account in the final model", "Regular cannabis use was not linked to a higher risk of psychosis.") == "In this cohort, regular cannabis use was not associated with a higher risk of psychosis"
    assert words15("The authors found no evidence that occasional use of psilocybin under supervised conditions led to lasting psychotic symptoms among the 110 healthy volunteers who took part", "No evidence was found that occasional supervised use led to lasting psychotic symptoms.") == "no evidence that occasional use of psilocybin under supervised conditions led to lasting psychotic symptoms"
    assert words15("Neither the seller nor the consumer of herbal mixtures, such as Spice, K2, or Black Mumba, can predict their content.", "Neither sellers nor buyers can know what is in them.") is None     # (no part of 15 words keeps both the "neither" and what is denied: no quotation, rather than half of one)
    # a quote with an amount for each of two groups gives two rows, each with the stretch it belongs to; what is not an amount for people is thrown away with its reason
    pg = [{"n": 1, "where": "Guidelines", "text": "The weekly low-risk guideline is 11 standard drinks per week, if you are a woman; 17 standard drinks per week, if you are a man. A typical adult reaches 0.08 grams of alcohol per deciliter after several drinks. "
                                                   "One estimate is 2.5 grams of dried Psilocybe cubensis mushroom for an adult. Up to 400 mg of caffeine a day appears to be safe for most healthy adults, while pregnant women are advised to limit intake to 200 mg a day. One standard drink contains 14 grams of pure alcohol in this country."}]
    got, out = amount_gate({"amounts": [{"passage": 1, "quote": "11 standard drinks per week, if you are a woman; 17 standard drinks per week, if you are a man", "who": "adults", "what": "the weekly low-risk guideline"},
                                         {"passage": 1, "quote": "0.08 grams of alcohol per deciliter after several drinks", "who": "a typical adult", "what": "after several drinks"},
                                         {"passage": 1, "quote": "2.5 grams of dried Psilocybe cubensis mushroom for an adult", "who": "an adult", "what": "one estimate"},
                                         {"passage": 1, "quote": "Up to 400 mg of caffeine a day appears to be safe for most healthy adults, while pregnant women are advised to limit intake to 200 mg a day", "who": "healthy adults", "what": "a daily amount"},
                                         {"passage": 1, "quote": "One standard drink contains 14 grams of pure alcohol in this country", "who": "one standard drink", "what": "what it contains"}]}, pg, {"read": "page", "kind": "official", "title": "Alcohol and caffeine"}, [])
    assert [x["show"] for x in got] == ["11 standard drinks per week, if you are a woman", "17 standard drinks per week, if you are a man", "Up to 400 mg of caffeine a day", "while pregnant women are advised to limit intake to 200 mg a day"], [x["show"] for x in got]
    assert "pregnant" in got[3]["clause"] and "pregnant" not in got[2]["clause"] and [("no amount" in o["why"], "product" in o["why"], "no people" in o["why"]) for o in out] == [(True, False, False), (False, True, False), (False, False, True)], out
    assert windows15("10 mg psilocybin session, with 25 mg 2 weeks later") == ["10 mg psilocybin session, with 25 mg"] and windows15("20 mg/70 kg, followed by 30 mg/70 kg 1.6 weeks later") == ["20 mg/70 kg, followed by 30 mg/70 kg"]     # (the time between two sessions is never shown)
    assert windows15("In the first study adults received 10 mg and in the second study volunteers who had used psychedelics before were given a higher amount of 25 mg") == ["In the first study adults received 10 mg"]   # (a further amount whose own clause does not fit gets no part: whom it was for would be lost)
    # (lane 6) amounts of drinks in words; whom an amount is for stays with it; a limit that stands just before the reader's quote comes with it; a drink's container is not an amount
    assert windows15("For men—two drinks or less in a day. For women—one drink or less in a day.") == ["For men-two drinks or less in a day", "For women-one drink or less in a day"] and not AMT.search("one study found that two reviews agree")
    assert windows15("The highest risk level (very-high-risk) corresponds to more than 100 g of ethanol (7.1 standard drinks) per drinking day for men and more than 60 g of ethanol (4.3 standard drinks) for women.") == ["more than 100 g of ethanol (7.1 standard drinks) per drinking day for men", "more than 60 g of ethanol (4.3 standard drinks) for women"]
    pg2 = [{"n": 1, "where": "The guidelines", "text": "If you are a woman, limit alcohol to no more than: 2 standard drinks per day; 10 standard drinks per week; 3 standard drinks on special occasions. Adults should not have more than 6 standard drinks on any 1 occasion. A standard drink is a single measure of spirits (35.5ml, 40% ABV). The optimal amount was estimated at 30 mg in adults."}]
    got, out = amount_gate({"amounts": [{"passage": 1, "quote": "2 standard drinks per day", "who": "women", "what": "the daily low-risk guideline"}, {"passage": 1, "quote": "6 standard drinks on any 1 occasion", "who": "adults", "what": "the amount on one occasion"},
                                         {"passage": 1, "quote": "a single measure of spirits (35.5ml, 40% ABV)", "who": "adults", "what": "a standard drink"}, {"passage": 1, "quote": "The optimal amount was estimated at 30 mg in adults", "who": "adults", "what": "an estimate"}]}, pg2, {"read": "page", "kind": "official", "title": "Low-risk alcohol drinking guidelines"}, [])
    assert [x["show"] for x in got] == ["no more than: 2 standard drinks per day", "should not have more than 6 standard drinks on any 1 occasion"] and len(out) == 2 and all("product" in o["why"] for o in out), ([x["show"] for x in got], out)
    pgs = {"read": "page", "kind": "official"}
    assert row_carried("men and women", "the weekly low-risk guideline", "men and women are advised not to drink more than 14 units a week on a regular basis", "Alcohol units", pgs) and row_carried("women, men", "weekly low-risk guidelines", "11 standard drinks per week, if you are a woman; 17 standard drinks per week, if you are a man", "Weekly low-risk alcohol guidelines", pgs)
    assert not row_carried("adults under medical supervision", "the weekly guideline", "men and women are advised not to drink more than 14 units a week", "Alcohol units", pgs) and not row_carried("people with liver disease", "the weekly guideline", "men and women are advised not to drink more than 14 units a week", "Alcohol units", pgs)
    # who received an amount, and under what care, are the source's own words, never the reader's
    st, ar = {"read": "full", "kind": "study"}, "MDMA-assisted therapy for severe PTSD. MDMA-assisted therapy was tested in adults with severe PTSD in a randomized, placebo-controlled phase 3 trial at fifteen sites."
    ps = "Participants received 80 to 120 mg of MDMA in each of three sessions, with two trained therapists present throughout."
    assert row_carried("adults with severe PTSD in a clinical trial, with two trained therapists present", "the amount in one session", ps, ar, st)
    assert not row_carried("adults with severe PTSD, under medical supervision in a hospital", "the amount in one session", ps, ar, st) and not row_carried("healthy young volunteers at a festival", "a recreational amount", ps, ar, st)
    assert AMT.search("a dose of 0.5 mg/kg") is None and AMT.search("levels of 200 ng/mL") is None and AMT.search("14 units a week").group(0) == "14 units"
    mp = ["MDMA-assisted therapy was tested in adults with severe PTSD in a randomized, placebo-controlled phase 3 trial at fifteen sites in three countries.",
          "Participants received 80 to 120 mg of MDMA in each of three sessions, with two trained therapists present throughout.",
          "In earlier work, rats were given 10 mg of MDMA twice daily to study neurotoxicity in the serotonin system of the brain.",
          "A supplemental half-dose of 40 to 60 mg was offered 1.5 to 2 hours later in each session, according to the protocol of the trial.",
          "One fatal case in the literature involved an estimated 500 mg taken at a party, with hyperthermia and failure of several organs."]
    mxml = "<article><front><article-meta><abstract><p>" + mp[0] + "</p></abstract></article-meta></front><body><sec><title>Methods</title>" + "".join(f"<p>{t}</p>" for t in mp[1:]) + "</sec></body></article>"
    mfound = {"can_read": [{"doi": "10.1000/m.1", "pmcid": "PMC2", "title": "MDMA-assisted therapy for severe PTSD", "year": 2021, "journal": "Nature Medicine", "kind": "study", "people": True, "near": 0.7}], "wanted": []}
    mrows = {"amounts": [{"passage": 2, "quote": mp[1].rstrip("."), "who": "adults with severe PTSD in a clinical trial, with two trained therapists present", "what": "the amount in one session"},
                         {"passage": 3, "quote": "rats were given 10 mg of MDMA twice daily", "who": "rats", "what": "a daily amount"},
                         {"passage": 4, "quote": "A supplemental half-dose of 40 to 60 mg was offered 1.5 to 2 hours later in each session", "who": "the same adults", "what": "a second amount in the session"},
                         {"passage": 5, "quote": "One fatal case in the literature involved an estimated 500 mg taken at a party", "who": "one person at a party", "what": "an amount that killed"},
                         {"passage": 2, "quote": "Participants received 90 mg of MDMA in every session of the trial", "who": "adults", "what": "the amount in one session"}]}
    nm = [["methadone", ["methadone-buprenorphine"]], ["mdma", ["mdma"]]]
    mitem = {"id": "w_m", "q": "What dosage of MDMA is used in studies?", "ways": [], "drugs": ["mdma"]}
    calls.clear(); script["amounts"] = [mrows]; script["writer"] = []; script["checker"] = [V(True)]
    r = make(mitem, mfound, chat, Enc(), MODELS, fulltext=lambda pmcid: mxml, crossref=crossref, ex=ex, names=nm)
    L = lines(); rows = [x for x in r["parts"] if x["part"].startswith("row")]
    assert r["status"] == "published" and r["kind"] == "amounts" and [x["part"] for x in r["parts"]] == ["short", "but", "row1"] and r["parts"][0]["text"] == L["amounts"] and r["parts"][1]["text"] == L["amounts_but"], (r["status"], r["why"], r["gates"])
    assert rows[0]["quote"] == "Participants received 80 to 120 mg of MDMA in each of three sessions" and words(rows[0]["quote"]) <= 15 and rows[0]["who"].startswith("Adults with severe PTSD") and rows[0]["rests_on"][0]["quote"] == mp[1].rstrip("."), rows
    assert "4 thrown away" in r["gates"]["read"] and not any(c[0] == "writer" for c in calls) and r["complete"] is False and "only one source" in r["missing"], (r["gates"], r["missing"])
    assert "This amount was the amount in one session, for adults with severe PTSD" in calls[-1][2] and "list the AMOUNTS of mdma" in calls[0][2]
    # the second reader says of each amount whether it is of the kind the question asks for: one that is not is left out
    script["amounts"] = [mrows]; script["checker"] = [{"verdicts": [{"n": 1, "supported": True, "on_question": False, "problem": ""}]}]
    r = make(mitem, mfound, chat, Enc(), MODELS, fulltext=lambda pmcid: mxml, crossref=crossref, ex=ex, names=nm); assert r["status"] == "none" and "not an amount of the kind the question asks for" in r["gates"]["check"] and "QUESTION that was asked: What dosage of MDMA is used in studies?" in calls[-1][2], (r["status"], r["gates"])
    # the second reader refuses the row: no answer. A single study in animals or a case report states no amount for people: no answer
    script["amounts"] = [mrows]; script["checker"] = [V("the passage does not say who received it")]
    r = make(mitem, mfound, chat, Enc(), MODELS, fulltext=lambda pmcid: mxml, crossref=crossref, ex=ex, names=nm); assert r["status"] == "none" and "did not accept any amount" in r["why"], r["why"]
    script["amounts"] = [mrows]; script["checker"] = []
    r = make(mitem, {"can_read": [dict(mfound["can_read"][0], kind="case")], "wanted": []}, chat, Enc(), MODELS, fulltext=lambda pmcid: mxml, crossref=crossref, ex=ex, names=nm); assert r["status"] == "none" and "no official page and no study in people" in r["why"], r["why"]
    # an opioid: the line about tolerance stands first, written by code; amounts from a page of tier 2 are not taken
    lab_ps = [{"n": 0, "where": "Dosage and administration", "text": "For detoxification and maintenance treatment of opioid addiction, the initial methadone dose should not exceed 30 mg, given under supervision."},
              {"n": 1, "where": "Dosage and administration", "text": "Patients in maintenance treatment are commonly stabilized at 80 to 120 mg a day once tolerance to methadone has developed."}]
    lab = {"body": "fda", "name": "U.S. Food and Drug Administration", "short": "the US label for methadone", "tier": 1, "address": "https://dailymed.test/x", "title": "Methadone Hydrochloride", "near": 0.7, "label": "methadone hydrochloride"}
    lab_ref = {"id": "label_methadone-hydrochloride", "type": "webpage", "genre": "Drug label", "title": "Methadone Hydrochloride", "author": [{"literal": "A Maker", "short": "the US label for methadone"}], "issued": {"date-parts": [[2026, 9, 9]]}, "URL": "https://dailymed.test/x", "publisher": "DailyMed"}
    orows = {"amounts": [{"passage": 1, "quote": "the initial methadone dose should not exceed 30 mg, given under supervision", "who": "people starting treatment for opioid addiction, under supervision", "what": "the first amount on the label"},
                         {"passage": 2, "quote": "Patients in maintenance treatment are commonly stabilized at 80 to 120 mg a day once tolerance to methadone has developed", "who": "patients in maintenance treatment, once tolerance has developed", "what": "a daily amount in long-term treatment"}]}
    oitem = {"id": "w_o", "q": "What is the usual dose of methadone?", "ways": [], "drugs": ["methadone-buprenorphine"]}
    script["amounts"] = [orows]; script["checker"] = [V(True, True)]
    r = make(oitem, {"can_read": [], "wanted": []}, chat, Enc(), MODELS, fulltext=lambda pmcid: None, crossref=crossref, ex=ex, names=nm, official=[dict(lab, tier=2, body="thelevel"), lab], page=lambda o: ({"title": "Methadone Hydrochloride", "passages": lab_ps}, dict(lab_ref)))
    assert r["status"] == "published" and [x["part"] for x in r["parts"]] == ["first", "short", "but", "row1", "row2"] and r["parts"][0]["text"] == L["first"]["opioids"]["text"] and r["parts"][0]["text"].endswith("can kill a person who is not used to them."), (r["status"], r["why"], [x["part"] for x in r["parts"]])
    assert len(r["sources"]) == 1 and r["sources"][0]["tier"] == 1 and all(words(x["quote"]) <= 15 and AMT.search(x["quote"]) for x in r["parts"] if x["part"].startswith("row")), r["parts"]
    # a question about the amount that kills is a question about dying: whatever is written waits for a person
    script["amounts"] = [orows]; script["checker"] = [V(True, True)]
    r = make(dict(oitem, q="What dose of methadone is lethal?"), {"can_read": [], "wanted": []}, chat, Enc(), MODELS, fulltext=lambda pmcid: None, crossref=crossref, ex=ex, names=nm, official=[lab], page=lambda o: ({"title": "Methadone Hydrochloride", "passages": lab_ps}, dict(lab_ref)))
    assert r["status"] == "waiting" and "dying" in r["why"], (r["status"], r["why"])
    assert stakes("Is ketamine addictive?", [{"text": "Some people who use it become dependent."}]) == "" and stakes("Do psychedelics and antidepressants interact?", []) == "mixing drugs" and stakes("x", [{"text": "It can be fatal."}]) == "dying"
    assert not rules([{"part": "short", "text": "Between 9% and 27% of people met criteria for dependence.", "uses": ["F1"]}], {"F1": {"quote": "between 9% and 27% met criteria"}})
    for bad in ("Take it 2 hours after the first dose.", "It is generally safe.", "Snorting it hits faster and stronger.", "Addicts relapse.", 'The paper says "yes".', "You should wait.", "It potentiates the high.", "Passages show a link."):
        assert rules([{"part": "short", "text": bad, "uses": ["F1"]}], {"F1": {"quote": "2"}}), bad
    print("lane selftest: ok (published with every sentence tied to the paper's own words; a retracted paper never read; quotes that are not in the paper and numbers that are not in the quote thrown away; "
          "a broken rule written again; a refused line dropped; a refused short answer means no answer; a question about dying waits for a person; one study alone is not enough; a nearer paper that cannot be read means not complete; "
          "an official body's page is a source and is named; a review behind a paywall is read in summary and the answer says so; an answer about amounts holds only the sources' own words, 15 at most, under the lines the code writes, "
          "with the line about tolerance first for an opioid, and nothing from animals, harm or timing; the answer it replaces is kept in its history)")


if __name__ == "__main__":
    if "--selftest" in sys.argv: selftest()
    elif len(sys.argv) > 1 and sys.argv[1] == "requests":
        # the requests waiting in data/auto/requests (lane-*.json: {"ids": [...], "max": N, "again": true}), each taken off when read.
        # A request is a file in the repository, written by the editor: read as data, never run.
        ids, limit, again, any_req = [], 3, False, False
        for f in sorted((ROOT / "data" / "auto" / "requests").glob("lane-*.json")):
            try: r = json.load(open(f, encoding="utf-8"))
            except ValueError: r = {}
            any_req = True; ids += [x for x in (r.get("ids") or []) if isinstance(x, str) and re.fullmatch(r"w_[a-z0-9_]{1,40}", x)]
            if isinstance(r.get("max"), int): limit = max(1, min(20, r["max"]))
            again = again or r.get("again") is True
            f.unlink()
        if any_req: run(ids=ids or None, limit=max(limit, len(ids)) if ids else limit, again=again)
        else: print("lane: no request waiting")
    elif len(sys.argv) > 1 and sys.argv[1] == "run":
        a = sys.argv[2:]; opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
        run(ids=[x for x in (opt("--ids") or "").split(",") if x] or None, limit=int(opt("--max", "3")), again="--again" in a)
    else: sys.exit(__doc__)
