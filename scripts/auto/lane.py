#!/usr/bin/env python3
"""lane.py: the machine lane. Answers written by the system from papers and official pages it found and read (docs/AUTOMATION.md).

The senior author, 15 November 2026. 17:33: "it should be claims... written as good as possible as close to 100% correct
as possible and ... in the language and format we write the rest of the website". 20:58: "it should be published and
automatically deployed with a very discreet disclaimer and we should just be able to access everything that was
automatically written and deployed to check whenever we want"; "if the automatic answer is not complete it should have a
small discreet disclaimer". 21:07: "it should find more than one sources if they are relevant ... the algorithm has to
mimick completely how claude writes answers".

    python3 -I scripts/auto/lane.py run [--max N] [--minutes M] [--sent] [--ids w_0027,...] [--again]
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
  7 stakes   A question about dying, overdose, an emergency, mixing two drugs, pregnancy, children or suicide: what each
             kind does is a setting (data/auto/lane/policy.json, "stakes"; lane 19, the senior author's words of 18 November
             2026: "the questions should be automatically answered ... for every pending question"). "strict": published by
             the system only where it meets a bar higher than every other answer's (strict_lacks: an official page or a
             review read in full under the short answer; a further reader; no word that plays a danger down, by code and
             by every reader); "person", or a kind the setting does not name: written, and it WAITS FOR AN EDITOR. What to
             do in an emergency, an amount that kills and an answer that disagrees with a checked claim always wait
             (emergency guidance is the senior author's own domain). Everything else that passed is published with the label.

A question about AMOUNTS (the senior author's decisions of 15 November 2026, 22:40 and 22:46; decision 11) goes another way,
with no writer: the reader copies each amount stated for people, with who received it and under what care; code keeps
only quotes that stand in the source, hold a number with its unit, name no animal and no amount that harmed or killed;
the checker reads each row beside its passage; code cuts each quote to 15 words at most and puts the fixed lines of
data/auto/lane/lines.json on the answer. Amounts come only from an official body of tier 1, a medicine's label, or a study
in people. Answers to other questions hold no amounts. (Lane 11, after the editor's reading of the first real batch of lane
10: six official pages may be read; a bare cell of a table is widened to its row; a row is given the one sex its own part
names; the same amount for the same people twice from one source is one row; an amount for each kilogram of body weight is
never shown; who received it has its abbreviations written out.)

What did not stand is kept too (lane 11): "tries" (every draft that was written again, each sentence with who refused it and
why), "dropped" (every line that was left out, with who dropped it), "refused_rows" (the amounts the second reader did not
accept). None of it is shown on the site. The editor reads it (scripts/editor/read_auto.py) and judges those sentences
for the exam of the lane's own sentences as well (scripts/editor/label_auto.py): was each rightly refused?

The second look (decision 12): an answer that is not complete, or was written by an older lane, or whose sources have
grown since, is written again; what it was before is kept in its "history".

What it writes: data/auto/answers/<id>.json (the answer; every sentence with the passages it rests on, kept short, for the
person who checks; the papers; the models; what each gate said; "published", "waiting" or "none", and why), the papers it
still wants (data/auto/papers-wanted.json, in APA 7), and data/auto/lane/state.json. The site shows only "published"
answers (site/build.js), each with "Written by our system from N papers. Not yet checked by a person." and, where papers
were missing, "Not complete yet".
"""
import sys, os, re, json, time, hashlib, pathlib, datetime, unicodedata, threading

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
TRIAL = ROOT / "data" / "auto" / "trial"                                # (17 November 2026) questions that are not on the site's list, written to try the lane on what it has never seen: never shown, never placed
LANE = 19               # the lane's own number: an answer written by an older lane is not shown (data/auto/lane/policy.json) and is written again
# Lane 19 (18 November 2026). The senior author, 13:34 Athens, of the questions he had sent: "this is a bug. and also the questions should be automatically
# answered no 'Written. A person has to check it first' --- this should happen for every pending question not only the ones on the list"; "can the answers
# get ... answered by themselves? ... one day or two is too ... much"; 13:36: "our ai becoming perfect is our first priority ... our site's answers have to be
# given much faster". What the records showed (docs/AUTOMATION.md, decision 32): a question was tried once and then left for a day or two; a try was lost to
# small faults that code can mend (a number that stood in another item of the same source; "male rats" read as a result for men; one writer's malformed
# reply; a fault of the network); and finished answers were parked for a reader that could not be asked. Lane 19 mends what code can mend before a rule
# judges, gives a writer that cannot keep the form a stand-in, asks the further readers that answer first, tries again by itself (the same day with another
# team; at once after a fault that was not the answer's), and parks nothing for a reader: it asks that reader again. No gate is taken away.
N_PAPERS = 2            # papers read in full for one answer (a third where the sources read are not yet enough)
N_TO_WRITER = 3         # findings of one source that go to the writer: the nearest to the question (and one limit)
N_OFFICIAL = 2          # official pages read for one answer (four for a question about amounts)
N_ROWS = 30             # amounts of one answer that the second reader is asked about (the nearest the question; amounts that stand together in a source stay together)
N_SUMMARIES = 2         # reviews behind a paywall read in summary, where the rest is not enough
ROOM = 1100             # neurons that must be left of today's allowance before a question is begun
N_PASSAGES = 7          # passages of a paper shown to the reader
# A run's clock (19 November 2026; the senior author, 18 November, 23:42 Athens: "like 5 minutes pass and i don't have an answer ... it should be answered almost
# immediately"; the notes of that evening's runs: 34 minutes on one question, and a run that sat on one step until GitHub stopped it after 40).
AT_ONCE = 6             # sources fetched and read at the same time
READ_SECONDS = 100      # what one question's reading may take: a source not read by then is written down as not read, and the answer is written from the rest
READ_SECONDS_SENT = 150 # (20 November 2026) for a question a person sent: eleven tries of such questions since 19 November ended with nothing read "for want of time", and
                        # each sent its person to wait for another run; fifty seconds more within the same seven minutes (QUESTION_SECONDS) cost less than that
QUESTION_SECONDS = 420  # what one question may take in all: past it no model is asked or waited for (llm.STOP_AT), and the question is tried again in the next run. (A last stop,
                        # not what an answer takes: with the fast models about two minutes; where only Google's slower ones have room, four to six. On the clock a strong
                        # further reader with 20 calls a day is waited for 80 seconds, not 170: one that does not answer is "could not be asked", as before.)
BEGIN_WITH = 240        # a question is begun only where the pass still has this many seconds
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
        if not carried(text, got[1], got[0]["text"], *((0.2, 0.4) if key == "text" else (0.5, 0.6) if key == "limit" else ())): no("the sentence is not carried by its quote and passage"); return None          # (what kind of paper it is may be said more freely; a limit must stay close to its quote: a reader that says the limit is about something the quote does not name is not followed)
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
    out = ask_json(chat, model, READER_SYS, reader_prompt(question, src, picked), room_for(model, 900))
    return read_gate(out, picked, amounts_ok=False) if out is not None else (None, [], [], [{"why": "the reader gave no JSON"}])


# ---------- 2b read, for a question about amounts (decision 11) ----------
AMOUNT_Q = re.compile(r"\b(?:dos(?:e|es|age|ages|ing)|milligrams?|micrograms?|mg|mcg|standard drinks?|units? of alcohol"
                      r"|how (?:much|many)\b[^?]{0,60}\b(?:safe|too much|take|taken|takes|use|used|drink|smoke|normal|typical|usual|common|average|a day|per day|daily|a week|per week|weekly|at once|is (?:ok|okay|fine|enough|a lot))"
                      r"|(?:safe|normal|typical|usual|common|average|recommended|standard|maximum|max|starting|low|high|threshold)\s+(?:amounts?|quantit(?:y|ies))|(?:what|which)\s+amounts?)\b", re.I)
NUM = r"(?:\d+(?:[.,]\d+)?|(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|twenty-one)(?=(?:\s*(?:to|-|or)\s*[\w-]+)?\s+(?:or\s+(?:more|less|fewer)\s+)?(?:standard\s+)?(?:drinks?|units?)\b))"
AMT = re.compile(r"(?<![\w.,/])" + NUM + r"(?:\s*(?:to|-|or)\s*" + NUM + r")?(?:\s+or\s+(?:more|less|fewer))?\s?(?:mg|milligrams?|µg|μg|ug|mcg|micrograms?|g|grams?|ml|millilit(?:re|er)s?|units?|standard drinks?|drinks?)\b(?!\s*/\s*(?:m?l|dl|kg|day·kg)\b)(?!\s*[·.]?\s*kg\b)(?!\s*(?:of\s+[\w-]+\s+)?per\s+(?:kilo(?:gram(?:me)?s?)?|kg|m?l|dl|litre|liter|decilit(?:er|re)|100\s?m?l)\b)", re.I)
PER_KG = re.compile(r"\d\s?(?:mg|milligrams?|µg|μg|ug|mcg|micrograms?|g|grams?|ml)\s*(?:/\s*(?:kg\b|kilo)|[·.]?\s*kg\b|\s+(?:of\s+[\w-]+\s+)?(?:per|for\s+each|for\s+every|a|each)\s+(?:kg\b|kilo))", re.I)   # (lane 11) an amount for each kilogram of body weight: never shown, not even inside another amount's part (lane 13: also as a summary writes it, "6 mg kg(-1)")
ODD_SIGNS = re.compile(r"\(-?\d\)|[<>]\s?/?\s?=|\^\s?-?\d|=\s?/?[<>]")                 # (lane 13) a summary's flattened notation ("mg day(-1)", "</=300 mg"): not words that can be shown
TIMING = re.compile(r"\b(?:wait|space)\w*\s+(?:at least\s+)?\d|\bevery\s+\d+(?:\s*(?:to|-|or)\s*\d+)?\s+(?:minutes?|hours?)\b|\b\d+(?:\.\d+)?(?:\s*(?:to|-|or)\s*\d+(?:\.\d+)?)?\s+(?:minutes?|hours?)\s+(?:before|after|apart|later)\b|\b(?:\d+(?:\.\d+)?|one|two|three|four|five|six|seven|eight)(?:\s*(?:to|-|or)\s*\d+(?:\.\d+)?)?\s+(?:days?|weeks?|months?)\s+(?:apart|later)\b", re.I)   # never shown: the time between two uses
REDOSE = re.compile(r"\bre-?dos\w*|\bsupplement\w*|\bbooster\b|\btop-?up\b|\b(?:second|third|additional|further|extra|repeat(?:ed)?|half)[\s-]dos(?:e|es|ing)\b", re.I)                                                                                # never taken: an amount added in the same session
NOT_AN_AMOUNT_FOR_PEOPLE = re.compile(r"\b(?:rats?|mice|mouse|rodents?|monkeys?|primates?|dogs?|zebrafish|in vitro|animals?)\b|\b(?:lethal\w*|fatal\w*|deadly|mortal\w*|death|deaths|died|dying|kill\w*|overdos\w*|toxic\w*|poison\w*|ld50|seiz(?:ed|ure)\w*|street|tablets? (?:sold|seized|contain\w*)|pills? (?:sold|seized|contain\w*))\b|\b(?:dried|mushrooms?|truffles?|cubensis|fruiting|flowers?|buds?|joints?|herbal|plant material|leaves|blotters?|crystals?|powder|edibles?|brownies?|gumm\w+|equivalent\w*|corresponding to|equal to|estimated weight|converted|convert\w*|blood|plasma|serum|urine|breath|concentration\w*|bac|per decilit(?:er|re)|g/dl|mg/dl|abv|pints?|glass(?:es)?|cans?|bottles?|measures? of|shots?|cups?|servings?|oz|ounces?|energy drinks?|optimal|optimum|predict\w*|estimat\w*|model(?:l)?ed|simulat\w*|extrapolat\w*|dose-response|meta-regression|hypothetical\w*)\b", re.I)


def is_amounts(question): return bool(AMOUNT_Q.search(question or ""))


def amounts_prompt(question, src, picked, drug_names):
    what = "page" if src["read"] == "page" else "paper"
    return (f"QUESTION that people ask: {question}\n\n{source_head(src)}\n\n"
            f"PASSAGES of this {what} (each is one paragraph, with its number and where it stands):\n{shown(picked)}\n\n"
            f"TASK. From these passages only, list the AMOUNTS of {', '.join(drug_names[:4]) or 'the drug'} that were given to PEOPLE or are stated for people: in a study, in treatment, on a medicine's label, in official guidance. For each amount give:\n"
            '"passage": its number; "quote": the whole sentence or clause of that passage that states the amount, copied exactly, word for word (8 to 40 words, with the number, its unit, and the words that say whom it is for when they stand there);\n'
            '"who": the PEOPLE who received it or whom it is stated for, and under what care, in one plain phrase, using the passage\'s own words (for example: adults with PTSD in a clinical trial, with two therapists present; men; women; healthy adults). Never add care or a setting that the passage does not state;\n'
            '"what": what kind of amount it is, in a few words, using the passage\'s own words (for example: the amount in one session; the starting amount on the label; a daily amount in long-term treatment; the weekly low-risk guideline). '
            'Call an amount low-risk, safe, moderate, recommended, a limit or a guideline ONLY if the passage itself calls it so; never borrow such a word from the QUESTION.\n'
            "Begin with the amounts that answer the QUESTION most directly; ten items at most. "
            "If one sentence states amounts for several groups (for men and for women), give ONE item and quote the sentence whole. If the groups stand in separate sentences or separate lists, give one item for each group, with that group as who, and quote no more than 40 words. "
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
GROUP_AFTER = re.compile(r"^(?:\s*\([^)]{0,48}\))?(?:\s+(?:per|a|each|every)\s+(?:drinking\s+)?(?:day|week|occasion|session))?(?:\s+(?!(?:and|or|but|while|whereas|per)\b)[A-Za-z][A-Za-z-]*){0,3}?,?\s+(?:for|in|among|if\s+you\s+are|if\s+you're)\s+(?:(?:a|an|the|most|all|healthy|adult|older|younger|both)\s+){0,3}"
                         r"(?:men|man|women|woman|adults?|people|males?|females?|patients?|participants?|those|everyone)\b", re.I)   # "(7.1 standard drinks) per drinking day for men", ", if you are a woman", (lane 12) "containing alcohol for females": whom the amount is for, up to three plain words after it
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


def window15(quote, k=0, span=False, lo=0):
    """The part of a quote, 15 words at most, that holds its amount (the k-th of the quote) and no time between two uses:
    the quotation the site shows (its rule: 15 words at most). Hard rules, so that a cut never changes what the source
    says: the words that limit the amount stay with it ("not more than", "up to", "between", "about": within five words
    before it, in the same clause), and so do a word that turns the meaning round within eight words before it ("were not
    given ...") and the words that belong to the amount after it ("or 84 mg", "of caffeine", "or less", "a day"); a cut
    never starts just after a word that turns the meaning round, never ends on a word that hangs ("... as an amount not"),
    never goes through another amount or stops between another amount and the words that belong to it. Among the parts
    that keep these rules: one that starts and ends where a clause does, or with the amount's own words ("two separate
    doses of 25 mg of psilocybin"), and the longer. None where no such part exists. span: also the first and last word.
    lo: the first word the part may begin with (the parts of one quote never overlap). (Lane 13) Where the amount stands
    after a comparison ("..., which is less than the two drinks and five drinks suggested for men"), the comparing words
    say something about the sentence's subject, not about this amount: the part begins after "than", and only where the
    amount carries whom it is for; otherwise there is none ("doses were lower than 25 mg" cannot be cut to "25 mg")."""
    ws = norm(quote).strip(' "\'').split(" "); text = " ".join(ws); ms = list(AMT.finditer(text))
    if k >= len(ms): return None
    m = ms[k]
    word_at = lambda i: len(text[:i].split(" ")) - 1
    def phrase(x, group=False):                                        # an amount with the words that belong to it: (first word, last word of the amount, last word of the phrase)
        more = AFTER_AMOUNT.match(text[x.end():]); end = x.end() + (more.end() if more else 0)
        grp = GROUP_AFTER.match(text[end:]) if group else None           # (lane 12) for another amount of the same words, whom it is for belongs to it too: "... for males or four or more drinks | containing alcohol for females" was cut there, and the females' amount stood under "males"
        return word_at(x.start()), word_at(x.end() - 1), (word_at(end + grp.end() - 1) if grp else word_at(end - 1) if more and more.end() else word_at(x.end() - 1))
    first, last, least = phrase(m)
    times = [(word_at(t.start()), word_at(t.end() - 1)) for t in TIMING.finditer(text)]        # the words that state a time between uses: no part of them is shown
    if any(t0 <= least and first <= t1 for t0, t1 in times): least = last
    else:
        more = AFTER_AMOUNT.match(text[m.end():]); end = m.end() + (more.end() if more else 0); grp = GROUP_AFTER.match(text[end:])
        if grp and not any(t0 <= word_at(end + grp.end() - 1) and least < t1 for t0, t1 in times): least = word_at(end + grp.end() - 1)   # whom it is for stays with the amount
    if any(t0 <= last and first <= t1 for t0, t1 in times): return None
    others = [o for o in (phrase(x, group=True) for x in ms if x is not m) if not first <= o[0] <= least]   # the other amounts in the same words
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
    cmp = [c for c in re.finditer(r"(?:\b(?:is|are|was|were|be|been|being)\s+(?:(?!no\b|not\b)\w+\s+)?|^)(?:less|more|fewer|higher|lower|greater|smaller|larger)\s+than\b(?=\s+(?:the|these|those)\b)|\b(?:is|are|was|were|be|been|being)\s+(?:(?!no\b|not\b)\w+\s+)?(?:less|more|fewer|higher|lower|greater|smaller|larger)\s+than\b", text[:m.start()], re.I)
           if not re.search(r"[.;:]\s", text[c.end():m.start()]) and len(text[c.end():m.start()].split()) <= 8]      # ("is less than ...", and a quote that itself begins "less than the ...": the reader cut it there)
    after_cmp = None
    if cmp:
        run, own = m, False                                              # the amounts joined to this one by "and", "or": "the two drinks and five drinks suggested for men"
        for x in [m] + [x for x in ms if x.start() > m.start()]:
            if x is not m and not re.fullmatch(r"\s*,?\s*(?:and|or)\s+(?:the\s+)?", text[run.end():x.start()]): break
            run = x; more = AFTER_AMOUNT.match(text[x.end():])
            if GROUP_AFTER.match(text[x.end() + (more.end() if more else 0):]): own = True; break
        if not own: return None
        lo = max(lo, word_at(cmp[-1].end()) + 1); must = max(must, lo); frame = max(frame, lo); after_cmp = lo
    if least - must + 1 > 15 or must < lo: return None
    best = None
    for a in range(max(lo, 0, least - 14), must + 1):
        if a and a not in (must, frame) and neg_before(ws, a, 8): continue
        if k and a and a != after_cmp and not (re.search(r"[.;:,]$", ws[a - 1]) or bare(ws[a - 1]) in ("and", "or", "but", "while", "whereas")): continue   # a further amount is shown from where its own clause begins, so that whom it is for comes with it
        for b in range(least + 1, min(len(ws), a + 15) + 1):
            if any(a <= t1 and t0 < b for t0, t1 in times): continue
            part = " ".join(ws[a:b])
            if part.count("(") != part.count(")"): continue
            if PER_KG.search(part) or (b < len(ws) and bare(ws[b]) == "per"): continue             # (lane 11) no amount for each kilogram inside a part, and no stop just before "per": "about 3 mg | per kilogram of body weight" was shown as "about 3 mg"
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
    show = re.sub(r"^(?:-\s+)+|(?:\s+-)+$", "", best[1].strip(" ,;:.")).strip(" ,;:.")           # (a dash that stands alone at an end is punctuation, not a word)
    for d in re.finditer(r"(\w+)([–—])(\w+)", unicodedata.normalize("NFKC", quote or "")):            # (lane 13) a long dash between two words is the source's own sign, not a hyphen: "For men—two drinks" was shown as "men-two"
        show = show.replace(d.group(1) + "-" + d.group(3), d.group(1) + d.group(2) + d.group(3))
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
        if got and any(got[1] < o[2] for o in out) and not any(got[1] <= o[1] and o[2] <= got[2] for o in out):      # (lane 13) a part that would begin inside an earlier one begins after it instead: "10 standard drinks per week" stood in two parts
            got = window15(quote, k, span=True, lo=max(o[2] for o in out))
        if not got or any(got[0] == o[0] for o in out): continue
        out = [o for o in out if not (got[1] <= o[1] and o[2] <= got[2])] + [got]        # a part that holds an earlier part whole takes its place
        if len(out) >= most: break
    if not clauses: return [o[0] for o in out]
    # (lane 12) the words that lead into a further part belong to THAT part ("...15 or more per week; For women, consuming four or more..."):
    # its stretch begins after the last full stop, semicolon or colon before it, else at the first "and", "or", "but" between the
    # two parts. Lane 11 gave "For women," to the part before it, and the men's amount was labelled for women.
    out = sorted(out, key=lambda o: o[1]); starts = [0]
    for prev, o in zip(out, out[1:]):
        lo, hi = max(prev[2] - 1, 0), o[1]
        stop = next((j + 1 for j in range(hi - 1, lo - 1, -1) if re.search(r"[.;:]$", ws[j])), None)
        if stop is None: stop = next((j for j in range(prev[2], hi) if bare(ws[j]) in ("and", "or", "but", "while", "whereas")), hi)
        starts.append(min(stop, hi))
    starts.append(len(ws))
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
    key = {w.lower() for w in re.findall(r"[A-Za-z0-9'’-]+", text or "") if len(w) > 3}
    sents = [x for x in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9“\"(])", norm(quote).strip(' "\'')) if x.strip()]
    if len(sents) > 1:                                                  # one sentence of the source, the one that shares most words with our line: never the end of one and the start of the next
        quote = max(sents, key=lambda x: (sum(1 for w in re.findall(r"[A-Za-z0-9'’-]+", x.lower()) if w in key), -sents.index(x)))
    ws = norm(quote).strip(' "\'').split(" ")
    if len(ws) > 15:
        best = None
        for a in range(len(ws)):                                       # every part of 6 to 15 words; one that starts and ends where a clause does stands first
            if a and neg_before(ws, a): continue                         # never a part that starts just after "not", "no", "without": it would say the opposite
            for b in range(a + 6, min(len(ws), a + 15) + 1):
                w = ws[a:b]; plain = [bare(x) for x in w]
                ends = b == len(ws) or bool(re.search(r"[.;:]$", w[-1])); comma = w[-1].endswith(",")
                if not ends and not comma and (HANGS.fullmatch(plain[-1]) or re.fullmatch(r"[a-z]{3,}ing", plain[-1])): continue      # never ending on a word that hangs ("... was not", "... over the past decade highlighting")
                if " ".join(w).count("(") != " ".join(w).count(")"): continue
                if not ends and not any(SAYS.fullmatch(x) for x in plain): continue       # a part that says nothing (a subject cut from its verb) is not a quotation
                nxt = bare(ws[b]) if b < len(ws) else ""
                score = (sum(1 for x in plain if x in key) + sum(0.5 for x in w if re.search(r"\d", x))
                         + (0.5 if a == 0 or re.search(r"[.;:,]$", ws[a - 1]) else 0.4 if bare(ws[a - 1]) == "that" else -1.1 if HANGS.fullmatch(plain[0]) and not plain[0][:1].isdigit() and not NEG.fullmatch(plain[0]) else -0.6)   # (after "showed that" the source's own statement begins)
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


CALLS_IT = re.compile(r"\b(low(?:er)?[- ]?risk|high(?:er)?[- ]?risk|safe(?:ly|ty)?|moderate|recommended|maximum|minimum|limits?|guidelines?|guidance|heavy|binge|harmful|hazardous|excessive|normal|typical|usual|optimal|acceptable|tolerable)\b", re.I)


def plain_what(what, show, text):
    """(lane 12) What kind of amount a row states, as it may be shown. The reader is asked for the passage's own words and
    sometimes gives the question's: "the weekly low-risk level" for an amount whose page never calls it low-risk. A word that
    CALLS the amount something (low-risk, safe, moderate, recommended, a limit, a guideline, heavy) must stand in the passage,
    its heading or the source's title. Where one does not, the row is not lost for it: what is then said by the code from
    the shown words alone ("an amount for a week"), which claims nothing; whether the amount belongs to the question is the
    second reader's to say from the passage."""
    base = norm(text).lower().replace("-", " ")
    def carried(w):
        w = w.lower().replace("-", " ")
        if "risk" in w: return bool(re.search(w[:3] + r"\w*\s*risk", base))
        if w.startswith("safe"): return bool(re.search(r"\bsafe(?:ly)?\b", base))          # (lane 14) "do not raise safety concerns" does not call the amount safe
        return ("guid" if w.startswith("guid") else w[:5]) in base
    if all(carried(m.group(1)) for m in CALLS_IT.finditer(what)): return what
    r = {m.group(0).lower()[:3] for m in RATE.finditer(show)}
    return "an amount for a day" if r & {"day", "dai"} else "an amount for a week" if "wee" in r else "an amount for a month" if "mon" in r else "an amount for one occasion" if r & {"occ", "ses", "sit", "sin", "onc"} else "an amount"


SEXES = (("women", re.compile(r"\b(?:women|woman|females?)\b", re.I)), ("men", re.compile(r"\b(?:men|man|males?)\b", re.I)))


def who_of_shown(who, show, clause):
    """(lane 11) Whom ONE amount of a sentence is for. A sentence that states an amount for women and another for men gives a
    row for each, and the reader's words for who name both ("Women, men"): each row gets the one sex that its own part (or
    the stretch of the sentence that belongs to it) names. A part that names one sex under a who that names only the other
    is no row at all (None): an amount is never shown under the wrong people. Everything else stays as the reader gave it."""
    named = next((n for n in ([name for name, rx in SEXES if rx.search(x or "")] for x in (show, clause)) if len(n) == 1), None)
    if not named: return who
    mine, other = (SEXES[0][1], SEXES[1][1]) if named[0] == "women" else (SEXES[1][1], SEXES[0][1])
    if not other.search(who): return who
    if not mine.search(who): return None
    kept = [x.strip() for x in re.split(r"\s*(?:[,/&;]|\band\b|\bor\b)\s*", who) if x.strip() and (mine.search(x) or not other.search(x))]
    out = ", ".join(kept)
    return out if out and out.count("(") == out.count(")") and mine.search(out) and not other.search(out) else named[0]


def sentence_around(text, q):
    """The sentence (or the item of a list, the row of a table) of a passage that a quote stands in: from the full stop, question
    mark or semicolon before it to the one after it. The quote itself where it is not found."""
    t = norm(text); s = norm(q).strip(' ."\'…'); i = t.find(s)
    if i < 0 or not s: return s
    a = max([e.end() for e in re.finditer(r"[.!?;]\s+", t[:i])] or [0]); e = re.search(r"[.!?;](?:\s|$)", t[i + len(s):])
    return t[a:i + len(s) + (e.start() if e else len(t))].strip()


# (lane 16) A source often reports what ANOTHER study found. On 17 November 2026 a review of cannabis and lung cancer said in its
# discussion "A meta-analysis in 2019 ... found no significant association ... However, long-term marijuana use (over 10 years) was
# associated with ... testicular germ cell tumors", and the lane wrote "A 2026 review found a potential link between ... long-term use
# over 10 years and testicular tumors": true to the quoted words, wrong about who found it; the second reader accepted it twice.
CITED = re.compile(r"\b(?:a|an|another|one|two|three|several|some|many|most|recent|previous|earlier|prior|other|these|those)\s+(?:[\w-]+\s+){0,3}(?:meta-analys[ie]s|systematic reviews?|reviews?|stud(?:y|ies)|trials?|surveys?|reports?|analys[ie]s|cohorts?|investigations?|experiments?|authors?|researchers?)\b[^.;]{0,90}\b(?:found|showed|shown|reported|observed|evaluated|concluded|suggested|demonstrated|indicated|noted|described|examined|revealed)\b"
                   r"|\baccording to\s+(?:a|an|one|the|another|recent|earlier|some|several)\b"
                   r"|(?-i:\b[A-Z][a-z]+(?:\s+et al|\s+and\s+[A-Z][a-z]+|\s+and colleagues))\s*(?:\(\d{4}\)|\[\d+\])?,?\s+(?:found|showed|reported|observed|concluded|suggested|demonstrated|noted|described)\b"
                   r"|\b(?:reports|studies|data|evidence|findings|research)\s+(?:suggests?|shows?|indicates?|have shown|has shown|have found|found|report)\b", re.I)
OWN_FRAME = re.compile(r"\b(?:we|our|ours)\b|\b(?:this|the present|the current|present|current)\s+(?:systematic\s+|narrative\s+|scoping\s+|literature\s+)?(?:study|review|meta-analysis|analysis|survey|trial|paper|work|report|article|investigation)\b|\bin this (?:study|review|paper|article|work)\b", re.I)
CONTINUES = re.compile(r"^(?:however|moreover|furthermore|in addition|additionally|also|similarly|likewise|conversely|in contrast|by contrast|they|the authors|it also|these|those|evidence|nevertheless|notably|specifically|in particular|but|and|yet)\b", re.I)
OWN_FIND = re.compile(r"\b(?:a|the|this|one)\s+(?:\d{4}\s+)?(?:systematic\s+|literature\s+|narrative\s+|recent\s+|large\s+|small\s+|online\s+)?(?:review|meta-analysis|study|survey|trial|paper|analysis|report)\b(?:\s+of\s+[^.,;]{0,50})?\s+(?:found|finds|showed|shows|concluded|concludes|observed|observes|demonstrated|established|confirmed|proved)\b", re.I)
SECOND_SAID = re.compile(r"\b(?:reports?|reported|notes?|noted|mentions?|mentioned|describes?|described|cit(?:es|ed|ing)|earlier|previous|prior|another|other (?:stud(?:y|ies)|analys[ie]s|reviews?|research)|in (?:one|a|an|some|several|a few|recent|earlier|other|two|three) (?:[\w-]+ )?(?:stud(?:y|ies)|analys[ie]s|reviews?|surveys?|trials?|reports?)|studies (?:in|of|that|which|it)|reports? (?:that )?(?:an?|one|some|several|earlier|other)\s+(?:[\w-]+ )?(?:stud|analys|review|survey|trial|meta))", re.I)
_ABBR_DOT = re.compile(r"\b(et al|e\.g|i\.e|vs|cf|approx|fig|no)\.", re.I)


def second_hand(text, q):
    """Does the source report these words from another study, by the passage they stand in? "" when not; else the sentence
    that names the other study (lane 17: the writer is shown it, so that it can name the earlier work as the passage does:
    told only "from another study", it wrote "cites one study" of a meta-analysis and was rightly refused). It does when the sentence of the
    quote names another study as the finder ("A meta-analysis in 2019 ... found", "According to a study of ...", "Kipping
    and Lynn found"), or goes on from such a sentence ("However, ...", "Evidence for ..."), up to three sentences back. No
    when a sentence on the way speaks of the source's own work ("we", "this review", "the present study")."""
    undot = lambda x: _ABBR_DOT.sub(lambda m: m.group(0)[:-1], x)
    t = undot(norm(text)); s = undot(norm(q)).strip(' ."\'…'); i = t.find(s)
    if i < 0 or not s: return ""
    spans = [(m.start(), m.end()) for m in re.finditer(r"[^.!?]+(?:[.!?]+|$)", t)]
    k = next((n for n, (a, b) in enumerate(spans) if a <= i < b), None)
    if k is None: return ""
    for _ in range(4):
        x = t[spans[k][0]:spans[k][1]].strip()
        if OWN_FRAME.search(x): return ""
        if CITED.search(x): return x[:180]
        if k == 0 or not CONTINUES.match(x): return ""
        k -= 1
    return ""


def widen(q, among):
    """(lane 11) A quote too short to be found for sure (a cell of a table: "400 mg") is widened to the clause it stands in
    (a row of the table, a sentence), when it stands in ONE place of the passages it may come from and that clause is short:
    (the clause, its passage), or None. The words are the source's own, in their order; nothing is added."""
    s = norm(q).strip(' ."\'…')
    if len(s) < 3 or not AMT.search(s): return None
    hits = [(p, x, m) for p in among for x in [norm(p["text"][:PASSAGE_CHARS])] for m in re.finditer(r"(?<![\w.,/-])" + re.escape(s) + r"(?![\w/-])", x)]
    if len(hits) != 1: return None
    p, x, m = hits[0]
    a = max([e.end() for e in re.finditer(r"[.!?;]\s+", x[:m.start()])] or [0]); e = re.search(r"[.!?;](?:\s|$)", x[m.end():])
    clause = x[a:m.end() + (e.start() if e else len(x) - m.end())].strip()
    return (clause, p) if len(clause) >= 20 and 3 <= words(clause) <= 30 else None


RATE = re.compile(r"\b(?:days?|daily|weeks?|weekly|months?|monthly|sessions?|occasions?|sittings?|single|once)\b", re.I)


def one_of_each(rows):
    """(lane 11) Two rows of ONE source that state the same amount for the same people are one row: the one whose shown words
    carry the limit ("up to", "no more than"), else the longer. rows: [(source, row)], kept in their order. Two reviews that
    state the same amount stay two rows (two sources that agree is worth seeing); so do the same amount for different
    people, for a day and for a week, or of a different kind (a single amount, a daily amount)."""
    stem = lambda x: frozenset(w[:5] for w in re.findall(r"[a-z]+", norm(x).lower()) if len(w) >= 4 and w not in STOP)
    amts = lambda r: (frozenset(re.sub(r"\s+", "", m.group(0).lower()) for m in AMT.finditer(norm(r["show"]))), frozenset(m.group(0).lower()[:3] for m in RATE.finditer(r["show"])))
    rank = lambda r: (any(LIMITS_IT.fullmatch(bare(w)) for w in r["show"].split()), len(r["show"]))
    out = []
    for s, r in rows:
        twin = next((i for i, (s2, r2) in enumerate(out) if s2 is s and stem(r2["who"]) == stem(r["who"]) and amts(r2) == amts(r) and (stem(r2["what"]) <= stem(r["what"]) or stem(r["what"]) <= stem(r2["what"]))), None)
        if twin is None: out.append((s, r))
        elif rank(r) > rank(out[twin][1]): out[twin] = (s, r)
    # (lane 13) and a row that states no amount which the rows of the same source for the same people do not state already is left out,
    # whatever it is called: the reader copied one list twice, once whole and once from "Women:", and "2 standard drinks per day" stood
    # in two rows. The rows that state most are looked at first.
    def each(r):                                                       # every amount of a row with what it is for a time (a day, a week, one occasion): the words after it up to the next amount, else the words before it
        t = norm(r["show"]); ms = list(AMT.finditer(t)); out = set()
        for j, m in enumerate(ms):
            q = {x.group(0).lower()[:3] for x in RATE.finditer(t[m.end():ms[j + 1].start() if j + 1 < len(ms) else len(t)])}
            if not q: q = {x.group(0).lower()[:3] for x in RATE.finditer(re.split(r"[;,.]", t[ms[j - 1].end() if j else 0:m.start()])[-1])}
            out.add((re.sub(r"\s+", "", m.group(0).lower()), frozenset(q)))
        return frozenset(out)
    groups, keep = {}, set()
    for i, (s, r) in enumerate(out): groups.setdefault((id(s), stem(r["who"])), []).append(i)
    for idxs in groups.values():                                        # for the same people from the same source: the row that states most that is new, with least said again, until nothing new is left
        seen, left = frozenset(), list(idxs)
        while left:
            b = max(left, key=lambda i: (len(each(out[i][1]) - seen), -len(each(out[i][1]) & seen), -i)); left.remove(b)
            if each(out[b][1]) and not each(out[b][1]) - seen: continue
            keep.add(b); seen |= each(out[b][1])
    return [x for i, x in enumerate(out) if i in keep]


ABBR = {"TRD": "treatment-resistant depression", "MDD": "major depressive disorder", "PTSD": "post-traumatic stress disorder", "AUD": "alcohol use disorder", "OUD": "opioid use disorder", "SUD": "substance use disorder",
        "CUD": "cannabis use disorder", "GAD": "generalized anxiety disorder", "OCD": "obsessive-compulsive disorder", "ADHD": "attention deficit hyperactivity disorder"}   # ten that have one meaning in this field


def abbreviations(text):
    """The abbreviations a source writes out itself ("treatment-resistant depression (TRD)"): {"TRD": "treatment-resistant
    depression"}. Only where the words before the brackets begin with the abbreviation's letters, one word for each letter
    and in their order (a hyphen parts two words); so a drug's name ("cannabidiol (CBD)") is never taken apart."""
    out = {}
    for m in re.finditer(r"((?:[A-Za-z][\w'-]*[ -]){1,8}[A-Za-z][\w'-]*)\s*\(([A-Z]{2,6})s?\)", norm(text)):
        ab = m.group(2); toks = list(re.finditer(r"[A-Za-z][A-Za-z0-9']*", m.group(1)))
        if ab in out or len(toks) < len(ab): continue
        tail = toks[-len(ab):]
        if not all(x.group(0)[0].upper() == c for x, c in zip(tail, ab)): continue
        full = m.group(1)[tail[0].start():].strip()
        if all(w[:1].isupper() for w in re.findall(r"[A-Za-z][\w']*", full)) or (full[:1].isupper() and full[1:] == full[1:].lower()):
            full = " ".join(w if "'" in w else w.lower() for w in full.split(" "))     # (a name's capital stays: "Parkinson's disease")
        out[ab] = full
    return out


def spelled(who, known=None):
    """(lane 11) Who received an amount, with its abbreviations written out ("12 subjects with moderate-to-severe TRD" is not
    plain language): as the source itself writes each out, or, for ten that have one meaning in this field, from the list.
    An abbreviation that neither knows stays as it is: its meaning is not guessed."""
    def full(m):
        f = (known or {}).get(m.group(1)) or ABBR.get(m.group(1))
        return f if f else m.group(0)
    return re.sub(r"\b([A-Z]{2,6})s?\b", full, who)


POINTS_LOW = re.compile(r"\blow(?:er)?[- ]risks?\b|\bsafe(?:ly)?\b|\bmoderate\w*|\bto a low level\b|\bdo(?:es)? not (?:raise|give rise to)\b|\bavoid\w*\s+(?:[\w-]+\s+){0,2}(?:consequences|harms?)\b", re.I)
POINTS_HIGH = re.compile(r"\bhigh(?:er)?[- ]risks?\b|\bincreasingly high\b|\bheavy\b|\bbinge\b|\bharmful\b|\bhazardous\b|\bexcessive\b|\bincreas\w+\s+(?:the\s+|your\s+)?risks?\b|\brisks?\b[^.;]{0,60}\bincreas\w+", re.I)


def other_way(question, sentence):
    """(lane 14) Does the amount's own sentence point the other way than the question asks? A question about what is called low-risk,
    safe or moderate is not answered by a sentence about high risk, heavy or binge drinking that has no word of the question's
    kind, and the reverse: "6 or fewer drinks/wk helps avoid increasingly high risks" was shown under "How much do health bodies
    call low-risk drinking?" (the page calls 1 to 2 low risk and 3 to 6 moderate). The second reader judges this too (its
    "on_question"); here the plain case is refused in code. Returns why, or ""."""
    q_low, q_high = bool(POINTS_LOW.search(question or "")), bool(POINTS_HIGH.search(question or ""))
    s_low, s_high = bool(POINTS_LOW.search(sentence or "")), bool(POINTS_HIGH.search(sentence or ""))
    if q_low and not q_high and s_high and not s_low: return "its sentence speaks of high risk, and the question asks what is called low-risk, safe or moderate"
    if q_high and not q_low and s_low and not s_high: return "its sentence speaks of what is low-risk or safe, and the question asks about high risk"
    return ""


def amount_gate(out, picked, src, dwords, question=None):
    """The rows of a reader's answer that may be used: (rows, what was thrown away and why). A row is kept when its quote
    stands in a passage that was shown, holds a number with its unit, is about people and not about harm, a product or a
    level in the blood, when the passage or the source's title names the drug, when who received it and under what care
    are the source's own words (not the reader's), and when a part of 15 words at most can be shown. A quote that holds
    several amounts ("11 standard drinks per week, if you are a woman; 17 ..., if you are a man") gives a row for each."""
    out = out if isinstance(out, dict) else {}; by = {p["n"]: p for p in picked}; rows, dropped = [], []
    for item in (out.get("amounts") or [])[:10]:
        if not isinstance(item, dict): dropped.append({"why": "not an item"}); continue
        q = re.sub(r"\s+", " ", str(item.get("quote") or "")).strip(); who = re.sub(r"\s+", " ", str(item.get("who") or "")).strip(" ."); what = re.sub(r"\s+", " ", str(item.get("what") or "")).strip(" .")
        p = by.get(item.get("passage")) if isinstance(item.get("passage"), int) else None
        if not p or not found_in(q, p["text"][:PASSAGE_CHARS]):
            named = p; p = next((x for x in picked if found_in(q, x["text"][:PASSAGE_CHARS])), None)
            if not p and len(norm(q).strip(' ."\'…')) < 20:           # (lane 11) a cell of a table: the row it stands in
                got = widen(q, [named] if named else picked)
                if got: q, p = got
        ours = who + " " + what
        sent = sentence_around(p["text"][:PASSAGE_CHARS], q) if p else q   # (lane 13) the passage's own sentence around the quote: the reader chooses where its quote begins and ends, and what the sentence says of the amount (that it is worked out from another, that it is the best by a model) may stand outside it
        if p:                                                          # (the reader often quotes a list's item without the words that govern it)
            t = norm(p["text"][:PASSAGE_CHARS]); i = t.find(norm(q).strip(' ."\'…'))
            pre = re.split(r"(?<=[.;!?])\s+|(?<=:)\s+(?=[A-Z])", t[:i])[-1].split() if i > 0 else []; before = pre[-5:]      # (a colon before a capital letter opens a list: what stands before it is another clause)       # (lane 11: only words of the quote's own clause; where the quote begins a clause, the clause before it governs nothing)
            lim = lambda w: LIMITS_IT.fullmatch(bare(w)) and bare(w) not in ("from", "about", "around", "average", "mean", "median", "most", "only", "within", "between")
            if any(lim(w) for w in before[-3:]):
                j = next(k for k, w in enumerate(before) if lim(w) or NEG.fullmatch(bare(w)))
                if j and NEG.fullmatch(bare(before[j])) and re.fullmatch(r"(?:should|must|do|does|did|can|could|may|is|are|was|were|will|would)", bare(before[j - 1])): j -= 1
                q = (" ".join(before[j:]) + " " + norm(q).strip(' ."\'…')).strip(); pre = pre[:len(pre) - len(before) + j]
            # (lane 12) "For men, | consuming five or more drinks ...": the reader's quote began after the words that say whose amount it is.
            # (lane 13) They are taken whole or not at all: everything that stands before the quote in its clause, where that is four words
            # at most and ends on the people's name with a comma or a colon ("Pregnant women: | habitual ..." must not become "women: ...").
            if 0 < len(pre) <= 4 and re.search(r"\b(?:men|women|males?|females?|adults?|people)\s*[,:]$", pre[-1], re.I): q = " ".join(pre) + " " + norm(q).strip(' ."\'…')
        why = ("its quote does not stand in a passage that was shown (or is shorter than 20 letters)" if not p else
               "the quote is shorter than 4 words or longer than 70" if not 4 <= words(q) <= 70 else
               "no amount with its unit in the quote" if not AMT.search(q) else
               "who or what is missing, or too long" if not (who and what and words(who) <= 30 and words(what) <= 20) else
               "an animal's amount, an amount that harmed, a product's amount, an amount worked out from another, or a level in the blood" if NOT_AN_AMOUNT_FOR_PEOPLE.search(q) or NOT_AN_AMOUNT_FOR_PEOPLE.search(ours) or NOT_AN_AMOUNT_FOR_PEOPLE.search(sent) else
               "an amount added in the same session" if REDOSE.search(q + " " + ours + " " + sent) else
               other_way(question, sent) if question and other_way(question, sent) else
               "who names no people" if not PEOPLE.search(who) else
               "an amount in our own words for who or what" if AMT.search(ours) else
               "a number in who or what that is not in the passage" if not numbers(ours) <= numbers(p["text"]) else
               "who received it, or under what care, is not in the source's words" if not row_carried(who, what, p["text"], " ".join([src.get("title") or "", p.get("where") or ""] + ([x["text"] for x in picked] if src.get("read") != "page" and src.get("kind") == "study" else [])), src) else
               "the passage and the title do not name the drug" if dwords and not O.has_word(O.flat(src["title"] + " " + p["text"]), dwords) else
               next(("our own words break a rule: " + name for name, rx in RULES if name not in ("an amount of a drug", "a quotation or a source in brackets", "a sign instead of a word") and rx.search(ours)), ""))
        shows = [] if why else [(w, c) for w, c in windows15(q, clauses=True) if not any(rx.search(w) for name, rx in RULES if name in QUOTE_NEVER) and not any(r["show"] == w for r in rows) and not ODD_SIGNS.search(w) and not PER_KG.search(w)]
        if not why and not shows: why = "no part of 15 words can be shown without changing what it says (or it was shown already, or it holds what is never shown)"
        if why: dropped.append({"quote": q[:200], "who": who[:120], "what": what[:120], "why": why}); continue
        for w, c in shows:
            whom = who_of_shown(who, w, c)                              # (lane 11) "Women, men" over an amount for one of them
            if whom is None: dropped.append({"quote": w[:200], "who": who[:120], "what": what[:120], "why": "this amount is for one sex and who names only the other"}); continue
            said = plain_what(what, w, " ".join([sent, p.get("where") or "", src.get("title") or ""]))        # (lane 12) what the amount is called must be the source's word; (lane 13) a word of the amount's own sentence, its heading or the title: a page that names "the low-risk guidelines" elsewhere in the passage does not call THIS amount low-risk
            rows.append({"passage": p["n"], "where": p["where"], "quote": q, "show": w, "clause": c, "who": whom, "what": said, **({"what_read": what} if said != what else {})})
    return rows, dropped


def read_amounts(chat, model, question, src, picked, dwords):
    out = ask_json(chat, model, READER_SYS, amounts_prompt(question, src, picked, list(dwords)), room_for(model, 1200))
    return amount_gate(out, picked, src, dwords, question) if out is not None else ([], [{"why": "the reader gave no JSON"}])


# ---------- 3 write ----------
WRITER_SYS = ("You write one answer for Pharmakon, a free drug encyclopedia that tells the public what research found, without judging. "
              "You write ONLY from the findings you are given: nothing from memory. You answer with JSON only.\n"
              "The rules of the site:\n"
              "- Plain words a 14-year-old can read. Short sentences. Lead the short answer with what people want to know.\n"
              "- Never surer than the item: where it says 'can' or 'may', you say 'can' or 'may', not 'often' or 'usually'; where it says 'usually in people who ...' or 'in some people', keep those words.\n"
              "- If the question can be answered with yes or no, the short answer begins with 'Yes', 'No', 'It can', 'Sometimes', 'It depends' or 'Not known', and then says why.\n"
              "- Everyday words: 'addicted' or 'dependent', 'withdrawal symptoms', 'the heart', 'the gut', 'works', 'stopping'. Not 'abstinence symptoms', 'withdrawal syndrome', 'pharmacological', 'cardiovascular', 'efficacy', 'cessation'.\n"
              "- Say who was studied when the findings say it (how many people, where, or that it was animals or a laboratory).\n"
              "- Keep every number exactly as the finding has it. Never claim more than the findings do: a link is not a cause; one study is not proof.\n"
              "- Never give amounts, doses, timing between uses, or ways of taking a drug. Never say how to make an effect stronger, or how much is needed to feel an effect. No advice: never 'you should'. Never call anything 'safe'.\n"
              "- Person-first words: 'people who use cannabis', 'people with an alcohol use disorder'. Never 'users', 'addicts', 'abusers', 'abuse', 'alcoholics', 'clean'.\n"
              "- No quotation marks, no brackets with sources, no mention of 'findings', 'passages' or 'the paper says F1'. Never write 'Paper A': say what it is, for example 'A 2024 review of case reports' or 'A survey of 278 people'.\n"
              "- Write 'times', never the sign ×. Write 'people who microdose', 'people who smoke', 'people who drink', never 'microdosers', 'smokers', 'drinkers'. Write 'use' or 'use disorder', never 'abuse' or 'misuse'.\n"
              "- The But must be a limit of THIS answer. The best But is a finding that says for whom, or under what conditions, the answer holds (for example: it was reported after frequent use over a long time; mostly in people who also used other drugs). "
              "Otherwise: who was not studied, how the studies were done, or what a source itself says is not known about the question. Never borrow a limit that a source states about something else, "
              "and never say what the sources do not say or do not tell: you have not read all of them.\n"
              "- The short answer answers every part of the question, in the order it was asked.\n"
              "- An official page is a statement by that body, not a study. Say whose it is: 'The NHS says ...'. Never write 'studies show' for it.\n"
              "- Where only a paper's summary could be read, say so: 'The summary of a 2021 review says ...'.\n"
              "- If the findings do not answer the question, say plainly what they do show, and set \"complete\" to false.")


PLANNER_SYS = ("You plan an answer for Pharmakon, a drug encyclopedia in plain words for everyone. You do not write the answer. You choose which labelled ITEMS it will be written from, "
               "as a careful editor does before writing: what answers the question itself, and what honestly limits that answer. JSON only.")


def plan_prompt(question, sources):
    lines = []
    for s in sources:
        lines.append(f"SOURCE {s['tag']}: " + (f"a page of {s['name']}, an official body" if s["read"] == "page" else ("the summary of " if s["read"] == "summary" else "") + ("a review" if s["kind"] == "review" else "a case report" if s["kind"] == "case" else "a single study") + f" ({s.get('year') or 'n.d.'})") + f": {s['title'][:120]}")
        if s.get("design"): lines.append(f"  [D{s['tag']}] what it is: {s['design']['text']}")
        for f in s["findings"]: lines.append(f"  [{f['id']}] {f['text']}")
        for l in s["limits"]: lines.append(f"  [{l['id']}] a limit it states: {l['text']}")
    return (f"QUESTION that people ask: {question}\n\nITEMS (each has a label in square brackets):\n" + "\n".join(lines) + "\n\nChoose, by label:\n"
            '"short": the 1 to 4 items that together answer the QUESTION itself, the most direct first. A plain statement of an official body and a review\'s finding are the best. Leave out items about a neighbouring question.\n'
            '"direct": if the QUESTION can be answered with yes or no, the words the answer should begin with, as those items show: "Yes", "No", "It can", "Sometimes", "It depends" or "Not known". Otherwise "".\n'
            '"but": the ONE item that best limits that answer: a finding or a limit that says for whom, how often or under what conditions it holds (for example: reported after frequent use over a long time), '
            'or what a source says is not known about the very same thing. Never an item about another subject (a review of treatments saying its treatment studies were weak does not limit an answer about whether something happens). [] if no item limits the answer.\n'
            '"how": for each source worth naming (2 to 4 sources, the strongest first; official bodies and reviews before single studies), the items of THAT source that support the answer, the D item first where it has one.\n'
            '"unanswered": the part of the QUESTION that no item answers, in a few plain words, or "".\n'
            'JSON only, in this form: {"short": ["F5", "F1"], "direct": "Yes", "but": ["F8"], "how": [["F5", "F6"], ["DA", "F1"]], "unanswered": ""}')


def make_plan(chat, model, question, sources, labels):
    """The plan of an answer, or None where the planner gave none that can be used: {"short": [labels], "direct": words or
    "", "but": [one label] or [], "how": [[labels of one source], ...], "unanswered": words}. Only labels that exist; a
    How group holds the items of one source."""
    out = ask_json(chat, model, PLANNER_SYS, plan_prompt(question, sources), room_for(model, 500))
    if not isinstance(out, dict): return None
    known = lambda xs: [x for x in (xs if isinstance(xs, list) else []) if isinstance(x, str) and x in labels]
    short = known(out.get("short"))[:4]; but = known(out.get("but"))[:1]; how = []
    for g in out.get("how") if isinstance(out.get("how"), list) else []:
        g = known(g)
        if g:
            g = [x for x in g if labels[x]["ref"] == labels[g[0]]["ref"]][:4]
            if not any(labels[h[0]]["ref"] == labels[g[0]]["ref"] for h in how): how.append(g)
    if not short or not how: return None
    direct = str(out.get("direct") or "").strip()[:20]
    return {"short": short, "direct": direct if DIRECT.search(direct) else "", "but": but, "how": how[:4], "unanswered": re.sub(r"\s+", " ", str(out.get("unanswered") or ""))[:160]}


def writer_prompt(question, sources, examples, fix="", plan=None, note="", last=""):
    lines = []; chosen = set(plan["short"] + plan["but"] + [x for g in plan["how"] for x in g]) if plan else None
    if plan: sources = [dict(s, design=s.get("design") if "D" + s["tag"] in chosen else None, findings=[f for f in s["findings"] if f["id"] in chosen], limits=[l for l in s["limits"] if l["id"] in chosen]) for s in sources]
    if plan: sources = [s for s in sources if s.get("design") or s["findings"] or s["limits"]]
    for s in sources:
        if s["read"] == "page": lines.append(f"OFFICIAL PAGE {s['tag']}: \"{s['title']}\", a page of {s['name']}" + (f" ({s['year']})" if s.get("year") else "") + f". When you use it, name the body: \"{s['short'][0].upper() + s['short'][1:]} says\".")
        else: lines.append(f"PAPER {s['tag']}{' (ONLY ITS SUMMARY COULD BE READ)' if s['read'] == 'summary' else ''}: {s['title']} ({s.get('year') or 'n.d.'}). {('A review or meta-analysis.' if s['kind'] == 'review' else 'A case report: one person or a few.' if s['kind'] == 'case' else 'A single study.')}")
        if s.get("design"): lines.append(f"  [D{s['tag']}] what it is and who was studied: {s['design']['text']} (the paper's words: {s['design']['quote']})")
        other = lambda x: (" (IT REPORTS THIS FROM ANOTHER STUDY" + (f", in the passage's words: “{x['second_hand']}”" if isinstance(x.get("second_hand"), str) else "") + ": never say that this source found it; say that it reports or cites that earlier work, called what the passage calls it)") if x.get("second_hand") else ""
        for f in s["findings"]: lines.append(f"  [{f['id']}] {f['text']} (the paper's words: {f['quote']})" + other(f))
        for l in s["limits"]: lines.append(f"  [{l['id']}] a limit the paper states: {l['text']} (the paper's words: {l['quote']})" + other(l))
    ex = "\n\n".join(f"Question: {e['q']}\nshort: {e['short']}\nbut: {e['but']}\nhow: " + " | ".join(e["how"][:3]) for e in examples)
    return (f"QUESTION that people ask: {question}\n\nWHAT THE SOURCES SAY (each item has a label in square brackets):\n" + "\n".join(lines) + "\n\n"
            "HOW THE SITE WRITES (three answers from the site, for the form only, not for their facts):\n" + ex + "\n\n"
            + ("THE PLAN (an editor chose the items; follow it exactly):\n"
               f'- "short": write it from {", ".join(plan["short"])}' + (f', and begin it with "{plan["direct"]}"' if plan["direct"] else "") + ".\n"
               + (f'- "but": write it from {plan["but"][0]} and nothing else: say for whom, how often or under what conditions the answer holds, as that item says.\n' if plan["but"] else '- "but": no item limits the answer: write "but" from the D item of the first source (what kind of source it is).\n')
               + "".join(f'- a line of "how" from {", ".join(g)}.\n' for g in plan["how"]) + "\n" if plan else "") +
            "TASK. Write the answer to the QUESTION from the labelled items only:\n"
            '- "short": the answer itself, 1 or 2 sentences, at most 45 words.\n'
            '- "but": the main limit or doubt, 1 sentence, at most 35 words. It must rest on a limit item or on what kind of study it was.\n'
            '- "how": 2 to 4 lines, one for each source used, each at most 35 words: what kind of study and who was studied, or whose page it is, and what it found or says.\n'
            'For "short", for "but" and for every line of "how", give "uses": the labels of the items that sentence rests on (at least one).\n'
            '- "complete": true if the items answer the question, false if they answer only a part or a neighbouring question; "missing": in a few words, what is not answered.\n'
            + (f"\nAN EDITOR READ AN EARLIER ANSWER TO THIS QUESTION AND DID NOT LET IT OUT. Mind what the editor found: {note}\n" if note else "")      # (lane 19) data/auto/held.json, \"say\": what the editor found goes to the writer, so that the answer is written again by itself
            + (f"\nAN ANSWER TO THIS QUESTION WAS WRITTEN BEFORE AND ITS READERS DID NOT ACCEPT IT. What they said of it: {last}\nDo not write those sentences again. Say only what the items say, in their own measure: what an item calls possible or reported, say as possible or reported; what it found in some people, say of some people.\n" if last else "")      # (lane 19) last_refusal: what the readers said of the draft that fell in the last run
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


OPENER = re.compile(r"^(Yes|No)\s*[.,:;]\s+|^(Sometimes|It depends|Not known|It is not known|Nobody knows|We do not know|It can|It may|Probably|Possibly|Rarely|Usually|Often|Partly|Mostly|Likely|Unlikely)\s*[.:;]\s+", re.I)


def opener_of(text):
    """(the word a short answer opens with, the rest as a sentence) where that word stands apart from what follows ("It
    depends. Cannabis smoke has ...", "Yes, it can ..."), else ("", the text). Lane 16: on 17 November 2026 the second
    reader refused "It depends." as "not stated in any passage", though it had been told that the word answers the
    question; the writer then left the word out and broke the rule that asks for it, and no answer was written for the
    senior author's own question (Does cannabis cause cancer?). The word is no longer part of the sentence the readers set
    beside the passages: it is judged apart, as the answer to the question (checker_prompt, "opening")."""
    t = str(text).strip(); m = OPENER.match(t)
    if not m: return "", text
    rest = t[m.end():]
    if len(rest.split()) < 4: return "", text
    return (m.group(1) or m.group(2)), rest[:1].upper() + rest[1:]


def checker_prompt(parts, labels, question=None, each=None, risk=""):
    # (lane 19) risk: the answer is about dying, overdose, mixing, pregnancy or children. Every reader is then also asked whether its first two sentences can be
    # read as saying that a danger is small or absent ("plays_down"); the code publishes such an answer by itself only where every reader said no (strict_lacks)
    more = ("\n\nThis answer is about " + risk + ", where a wrong word can hurt a reader. Add one more field to your JSON, beside \"verdicts\": \"plays_down\": true if sentence 1 or sentence 2 says or suggests that "
            "something is safe or harmless, or that a danger is small, rare, unlikely or absent, or if it tells the reader what to do; false if they do neither.") if risk else ""
    return _checker_prompt(parts, labels, question, each) + more


def _checker_prompt(parts, labels, question=None, each=None):
    blocks = []; opening = ""
    for n, p in enumerate(parts, 1):
        ps = "\n".join(f"   PASSAGE ({labels[u]['paper']}; {labels[u]['where']}): {labels[u]['passage_text'][:PASSAGE_CHARS]}" for u in p["uses"])
        text = p["text"]
        if n == 1 and not each and p.get("part", "short") == "short": opening, text = opener_of(text)
        blocks.append(f"{n}. SENTENCE: {text}\n{ps}")
    return ("For each numbered SENTENCE below, decide whether its PASSAGES support it. Supported means ALL of this: everything the sentence says is stated in its passages; "
            "it is about the same people, animals or setting; every number is the same; it is not stronger or more certain than the passages; it does not say one thing causes another "
            "where the passages only report a link; it does not turn what one study found into a general fact; where the passages say \"can\" or \"may\" it does not say \"often\" or \"usually\", and it does not leave out words that narrow the passage (\"usually in those already susceptible\", \"in some people\", \"after long use\"). If any part of the sentence is not in the passages, it is not supported. "
            "Each passage is named with its source's title: when a passage speaks of \"the studies\", \"the evidence\" or \"the articles\", it means the ones that source looked at (see its title), "
            "so a sentence that makes it about something else is not supported.\n\n"
            + "\n\n".join(blocks)
            + ((f"\n\nOn the site the answer opens with the word “{opening}”, before sentence 1: a yes-or-no question is answered that way. That word is not part of sentence 1 and is not a claim to look for in the passages: it is the answer to the QUESTION. "
                f"\"opening\": is “{opening}” a fair answer to the QUESTION, given what the passages of sentences 1 and 2 say (true)? It is not (false) when they point another way, or are less sure or more sure than that word; then say in \"why\" which word would be fair."
                if opening else
                "\n\nSentence 1 may open with one of the words Yes, No, It can, Sometimes, It depends or Not known: the site answers a yes-or-no question that way. That word is the answer to the QUESTION, "
                "not a claim to look for in the passages: accept it when what the passages say bears that answer out; refuse it, and say what the passages say instead, only when they point another way or are less sure than the word.")
               if question else "")
            + (f"\n\nThen judge the answer as a whole. QUESTION that was asked: {question}\n"
               '"answers_question": does ' + (f"the answer (the opening word “{opening}” followed by sentence 1)" if opening else "sentence 1") + ' answer that QUESTION itself, directly (true), or does it answer a neighbouring question or only talk around it (false)?\n'
               '"but_fits": is sentence 2 a limit or a doubt about what sentence 1 says (true), or is it about something else (false)? It is about something else when its source states the limit about ITS OWN subject and that subject is not what sentence 1 says: '
               'for example, a review of treatments says that the studies of those treatments were weak; that is no limit of an answer about whether dependence happens.'
               '\n\nJSON only, one verdict for every sentence, in this form: {"verdicts": [{"n": 1, "supported": true, "problem": ""}, {"n": 2, "supported": false, "problem": "what the passages do not say"}], ' + ('"opening": true, ' if opening else "") + '"answers_question": true, "but_fits": true, "why": ""}' if question else
               f"\n\nQUESTION that was asked: {each}\nFor every sentence also give \"on_question\": is the amount it states an amount of the kind the QUESTION asks for (true), or of another kind, for example an amount called high-risk when the question asks what is called low-risk, or what a drink contains when the question asks how much people drink (false)? A limit for one day or for one occasion that the same guidance gives beside its weekly amount is of the kind asked."
               '\n\nJSON only, one verdict for every sentence, in this form: {"verdicts": [{"n": 1, "supported": true, "on_question": true, "problem": ""}, {"n": 2, "supported": false, "on_question": true, "problem": "what the passages do not say"}]}' if each else
               '\n\nJSON only, one verdict for every sentence, in this form: {"verdicts": [{"n": 1, "supported": true, "problem": ""}, {"n": 2, "supported": false, "problem": "what the passages do not say"}]}'))


# ---------- the second reader, piece by piece (tried on the exam first: scripts/auto/exam_models.py, "how": "pieces") ----------
# On 16 November 2026 the second reader (gpt-oss-120b at Groq) sat the exam with the question above, "do the passages support
# the sentence?", and caught 5 of 31 wrong cards while it stopped 5 of 30 good ones: no better than chance. The faults it let
# through are small ones: a describing word the lines do not hold, what is counted changed (deaths, not pills), a proposed
# mechanism said as the cause, emergency patients said as everyone. A model asked for one verdict on a whole sentence reads it
# as a whole and says yes. So the same reader is asked something it cannot answer with a yes: to take the sentence apart and
# to copy, for every piece, the passage's own words that say it. The verdict is the code's: a piece with no words, or with
# words that are not in the passages, stops the sentence; so does a list of pieces that leaves words of the sentence out.
PIECES_SYS = ("You compare a sentence with the passages it was written from, piece by piece. You never judge the sentence as a whole, and what you know yourself does not count: "
              "only the words of the passages do. You answer with JSON only.")


def pieces_prompt(sentence, passages, denies=False):
    ps = "\n".join("   PASSAGE: " + t for t in passages if t)
    return ("Take the SENTENCE below apart into its pieces and look for each piece in the PASSAGES.\n"
            "A piece is one thing the sentence says: who or what it is about (which people, animals, place, year, study or body); each thing it names; each number; what is counted or measured; "
            "each describing or grading word (well-known, most, often, only, first, usually, strong, rare); each comparison; each cause; and how sure it sounds (is, may, was linked to, causes). "
            "List EVERY piece, also the small words that change the meaning. Do not skip a piece because it seems harmless.\n"
            "For each piece give \"passage_words\": the exact words of a passage that say the same thing, copied letter for letter. Write NONE when the passages do not say it, or say it only of other people or "
            "another setting, of another thing counted, with another number, less surely, or as a link and not as a cause."
            + (" The sentence says that something is NOT true. For the piece that the passages deny, copy the passage words that deny it and give \"denied\": true.\n" if denies else "\n")
            + f"\nSENTENCE: {sentence}\n{ps}\n\n"
            'JSON only, in this form: {"pieces": [{"says": "one piece, in the sentence\'s own words", "passage_words": "exact words of a passage, or NONE"' + (', "denied": false' if denies else "") + "}]}")


def pieces_verdict(out, sentence, passages, denies=False):
    """The code's verdict on what the second reader copied: {"through", "clear", "pieces", "missing": [...], "not_there": [...], "left_out": [...]}.
    through: every piece has passage words, those words stand in the passages, and the pieces leave out no more than one
    in five of the sentence's content words. clear: the reader gave a list of pieces at all."""
    ps = out.get("pieces") if isinstance(out, dict) else None
    if not isinstance(ps, list) or not ps or not all(isinstance(p, dict) for p in ps): return {"through": False, "clear": False, "pieces": 0, "missing": [], "not_there": [], "left_out": []}
    flatten = lambda t: " " + " ".join(re.findall(r"[a-z0-9]+", norm(str(t or "")).lower())) + " "
    whole = flatten(" ".join(passages)); missing, not_there, said, denied = [], [], "", 0
    for p in ps[:40]:
        says = re.sub(r"\s+", " ", str(p.get("says") or ""))[:120]; w = str(p.get("passage_words") or "").strip(); said += " " + says
        if p.get("denied") is True: denied += 1
        if not w or re.fullmatch(r"(?i)\W*none\W*", w): missing.append(says); continue
        bits = [b for b in (flatten(x).strip() for x in re.split(r"\.{3,}|…|\s/\s|\s\|\s", w)) if b]
        if not bits or not all(" " + b + " " in whole for b in bits): not_there.append(says)
    stems = lambda t: [x[:5] for x in re.findall(r"[a-z]+", norm(t).lower()) if len(x) >= 4 and x not in STOP]
    tw, have = stems(sentence), set(stems(said)); left_out = sorted({x for x in tw if x not in have})
    ok = not missing and not not_there and len(ps) >= 2 and (not tw or len(left_out) / len(set(tw)) <= 0.2) and (denied <= 1 if denies else denied == 0)
    return {"through": ok, "clear": True, "pieces": len(ps), "missing": missing[:6], "not_there": not_there[:6], "left_out": left_out[:8]}


# ---------- the second reader asked for marks, not for a verdict (16 November 2026; measured first: exam_models.py, "how": "marks") ----------
# Asked "do the passages support the sentence?", a reader says yes to sentences that are nearly right; asked to copy the source's
# words for every piece, it ran out of room. The faults our blind checkers find are of a few kinds (data/auto/exam: the cards, the
# plain lines, the lane's own sentences): a word of measure the source does not carry, a report said as a fact, a wider group or
# another thing counted, a cause or a reason added, a detail from elsewhere. So the reader is asked five small questions, one for
# each kind, and copies the source's words only for the words of measure. The verdict is the code's: every word of measure must
# have words of the source that really stand there, and none of the four other faults may be marked.
# Its first sitting (Gemini 3.5 Flash Lite, 16 November 2026) caught 7 of the lane's 9 faulty sentences where one verdict caught 3 or 4, and
# stopped 8 of 20 good ones: 7 of those 8 for naming their source ("a 2020 review", "The NZ Drug Foundation says"), and on the cards for words
# worked out from the lines' numbers ("most", "fewer") and for plain rewordings. The question now says that none of the three is a fault.
MARKS_SYS = ("You compare one sentence with the passages it was written from. You do not judge whether the sentence is true, and what you know yourself does not count: "
             "only the passages do. You answer the questions you are asked, exactly, with JSON only.")


def marks_prompt(sentence, passages):
    ps = "\n".join("   PASSAGE: " + x for x in passages if x)
    return ("Answer five questions about the SENTENCE, from its PASSAGES only.\n"
            "A PASSAGE may begin, in brackets, with the name of its source (a body such as Health Canada, or a paper's title with its year) and the place in it. The SENTENCE may name that source in its own words "
            "(\"Health Canada says\", \"a 2024 review found\", \"one survey\"): naming the source is never a fault, and what the bracket says of the source counts as stated. "
            "A plain rewording of what a passage says is never a fault either: only what the passages do not say is.\n\n"
            f"SENTENCE: {sentence}\n{ps}\n\n"
            '1. "measure": list every word or phrase of the SENTENCE that says how often, how many, how much, how big, how sure or how good something is '
            '(for example: often, usually, most, all, both, never, always, clearly, proven, severe, slightly, far more, the most common, the riskiest, famous, trained, only). '
            'For each one copy the words of a PASSAGE that say the same measure, exactly as they stand there, or write NONE when no passage says it. A measure that the SENTENCE works out fairly from a passage\'s own numbers '
            '("most" for 62 of 64; "fewer" for 10 against 28; "about a third" for 33 in 100) is said by those numbers: copy them. Leave out small words that measure nothing (also, what, a while). A sentence with no word of measure gets an empty list.\n'
            '2. "report_as_fact": true when the SENTENCE states as a plain fact something the PASSAGES give only as what people said, reported, rated or recalled, or as what the authors suggest, propose, think or could not rule out. Else false.\n'
            '3. "wider": true when the SENTENCE is about more, or about something else, than the PASSAGES: people in general where the passages speak of men, of patients or of one study\'s volunteers; '
            'every study where it was one; another place, time or thing counted (deaths where pills were counted). Else false.\n'
            '4. "cause_added": true when the SENTENCE says or implies that one thing causes, explains or follows from another ("because", "so", "leads to", "which is why") where the PASSAGES only put the two side by side or report a link. Else false.\n'
            '5. "extra": true when anything else in the SENTENCE (a number, a name, a detail, a whole clause) is not stated in the PASSAGES. Else false.\n'
            'For 2 to 5, when true, say which words of the SENTENCE in "which".\n\n'
            'JSON only, in this form: {"measure": [{"word": "often", "passage_words": "NONE"}], "report_as_fact": false, "wider": false, "cause_added": false, "extra": false, "which": ""}')


def marks_verdict(out, passages):
    """The code's verdict on the reader's marks: {"through", "clear", "problem"}. through: every word of measure has words of a
    passage that really stand in the passages, and none of the four faults is marked. clear: the reader answered all five."""
    if not isinstance(out, dict) or not isinstance(out.get("measure"), list) or not all(isinstance(out.get(k), bool) for k in ("report_as_fact", "wider", "cause_added", "extra")):
        return {"through": False, "clear": False, "problem": "the reader did not answer the five questions"}
    flatten = lambda x: " " + " ".join(re.findall(r"[a-z0-9]+", norm(str(x or "")).lower())) + " "
    whole = flatten(" ".join(passages)); bad = []
    for m in out["measure"][:20]:
        if not isinstance(m, dict): continue
        word = re.sub(r"\s+", " ", str(m.get("word") or ""))[:60]; w = str(m.get("passage_words") or "").strip()
        if not w or re.fullmatch(r"(?i)\W*none\W*", w): bad.append(f"“{word}”: no passage says it"); continue
        bits = [b for b in (flatten(x).strip() for x in re.split(r"\.{3,}|…|\s/\s|\s\|\s", w)) if b]
        if not bits or not all(" " + b + " " in whole for b in bits): bad.append(f"“{word}”: the words given for it are not in the passages")
    names = {"report_as_fact": "a report or a suggestion said as a fact", "wider": "it is about more, or about something else, than the passages", "cause_added": "a cause or a reason the passages do not give", "extra": "something the passages do not state"}
    which = re.sub(r"\s+", " ", str(out.get("which") or ""))[:120]
    bad += [names[k] + (f" ({which})" if which else "") for k in names if out[k]]
    return {"through": not bad, "clear": True, "problem": "; ".join(bad)[:300]}


def check_marks(chat, model, parts, labels):
    """[(supported?, problem)] for the parts, in order: the reader is asked the five small questions about each sentence, one
    call a sentence, and the code gives the verdict (marks_verdict). A team names such a reader as "<model>#marks"."""
    out = []
    for p in parts:
        passages = [f"({labels[u]['paper']}; {labels[u]['where']}) {labels[u]['passage_text'][:PASSAGE_CHARS]}" for u in p["uses"]]
        v = marks_verdict(llm.as_json(chat(model, [{"role": "system", "content": MARKS_SYS}, {"role": "user", "content": marks_prompt(p["text"], passages)}], room_for(model, 420))), passages)
        out.append((v["through"], v["problem"] if v["clear"] else "the reader gave no clear answer to the five questions"))
    return out


# ---------- our own checker (decision 23) ----------
def own_word(parts, labels, chk, passage=True):
    """Our own checker's score for every sentence a model wrote, against the words it rests on (the quotes and the passages they
    stand in): {part: score from 0 to 1}. A sentence the code wrote ("fixed") is not asked about. passage=False: against the
    quotes alone, with their sources' names, as the exam of the lane's sentences is sat (workshop.sit_lane: the exam keeps no
    passage); the record keeps that score too, so that the two ways can be compared on real answers (lane 11)."""
    ask = [(p["part"], " ".join(((labels[u].get("paper") + ". " if labels[u].get("paper") else "") + labels[u]["quote"] + (" " + (labels[u].get("passage_text") or "")[:PASSAGE_CHARS] if passage else "")).strip() for u in p["uses"]), p["text"]) for p in parts if not p.get("fixed") and p.get("uses")]      # (the source's name stands with its words: a sentence may say "Health Canada says" only because of it)
    return dict(zip([a[0] for a in ask], chk.score([(src, text) for _, src, text in ask]))) if ask else {}


def room_for(model, plain):
    """How many tokens a model may answer with. One that reasons before it writes needs room for both: on 16 November 2026
    gpt-oss-120b used all of 1,400 tokens reasoning and wrote nothing, three times for each of two questions; with 3,000 it
    reasoned for some 1,300 and then wrote its answer (data/auto/exam/writer-trial.json)."""
    svc, name = llm.service_of(model)
    # (lane 19) Google's stronger models think before they write and their thinking is counted in the room: on 17 and 18 November 2026 Gemini 4 Hydrogen gave
    # no verdict on 30 of 34 sentences asked together, and Gemini 3 Flash "no verdict, twice" on real answers, with some 2,000 tokens. Room costs nothing on a
    # free plan that counts calls (20 a day for each of these models), a call that returns nothing costs one of them.
    if svc == "gemini" and not re.search(r"flash-lite|gemma", name): return plain + 5000
    if svc: return plain + 1500                         # (a model of another service may reason before it writes: room for both until a trial says how much it needs)
    return plain + (1200 if "gpt-oss-20b" in model else 2200 if "gpt-oss" in model else 0)      # (the small gpt-oss only reads, with little reasoning; qwen3 at Groq answers without reasoning: its free plan gives it 1,000 output tokens a minute)


LAST_REPLY = {"head": ""}       # the first characters of the last reader's reply that held no verdict (for the record: how a reply that could not be read looked)


def verdicts_json(text):
    """(lane 19) A reader's reply as {"verdicts": [...], ...}, or None. A reader may answer with the list alone ([{"n": 1, ...}, {"n": 2, ...}]), with one
    object for one sentence, with the number or the verdict as a word ("1", "true"), or with no numbers at all (then in the order given). On 17 and 18
    November 2026 Gemini's readers answered real answers so (186 characters, ended in order: four verdicts in a bare list), were counted as having given no
    verdict, twice each, and five answers were parked for them. What a reader said is read as it said it; nothing is added to it."""
    out = llm.as_json(text)
    if isinstance(out, dict) and isinstance(out.get("verdicts"), list): pass
    elif isinstance(out, dict) and "supported" in out: out = {"verdicts": [out]}
    else:
        s = text or ""; a, b = s.find("["), s.rfind("]"); v = None
        if 0 <= a < b:
            for cand in (s[a:b + 1], re.sub(r",\s*([}\]])", r"\1", s[a:b + 1])):
                try: v = json.loads(cand); break
                except ValueError: continue
        out = {"verdicts": v} if isinstance(v, list) and v and all(isinstance(x, dict) for x in v) else out if isinstance(out, dict) else None
    if not isinstance(out, dict): return None
    vs = [v for v in out.get("verdicts") or [] if isinstance(v, dict)]
    for v in vs:
        if isinstance(v.get("n"), str) and v["n"].strip().isdigit(): v["n"] = int(v["n"].strip())
        if isinstance(v.get("supported"), str) and v["supported"].strip().lower() in ("true", "false", "yes", "no"): v["supported"] = v["supported"].strip().lower() in ("true", "yes")
    if vs and all(v.get("n") is None for v in vs):
        for i, v in enumerate(vs, 1): v["n"] = i
    return out


def check(chat, model, parts, labels, question=None, whole=None, each=None, risk=""):
    """[(supported?, problem)] for the parts, in order. A sentence without a clear verdict is not supported. With a
    question, the second reader also says whether the short answer answers it and whether the But is about that answer
    (written into whole: "answers", "but_fits", "why"; None where it gave no clear word)."""
    room = room_for(model, 120) + 90 * len(parts) + (80 if question else 0) + (40 if risk else 0)
    for attempt in range(2):
        if attempt and llm.LAST.get("finish") == "length": room = min(2 * room, 12000)        # (lane 19) a reply that was cut off before its verdicts is asked for again with twice the room, not the same way
        reply = chat(model, [{"role": "system", "content": CHECKER_SYS}, {"role": "user", "content": checker_prompt(parts, labels, question, each, risk)}], room)
        out = verdicts_json(reply); LAST_REPLY["head"] = re.sub(r"\s+", " ", str(reply or ""))[:90]
        vs = {v.get("n"): v for v in (out or {}).get("verdicts") or [] if isinstance(v, dict)}
        # (lane 16) the opening word of the short answer was judged apart, as the answer to the question: its verdict must be there too
        opening = opener_of(parts[0]["text"])[0] if question and parts and not each and parts[0].get("part", "short") == "short" else ""
        if out is not None and all(isinstance(vs.get(n, {}).get("supported"), bool) for n in range(1, len(parts) + 1)) and (not opening or isinstance(out.get("opening"), bool)):
            if whole is not None and risk: whole["plays_down"] = out.get("plays_down") if isinstance(out.get("plays_down"), bool) else None
            if whole is not None and question:
                whole.update(answers=out.get("answers_question") if isinstance(out.get("answers_question"), bool) else None, but_fits=out.get("but_fits") if isinstance(out.get("but_fits"), bool) else None, why=re.sub(r"\s+", " ", str(out.get("why") or ""))[:240])
                if opening: whole["opening"] = [opening, out["opening"]]
            got = [(vs[n]["supported"] is True and not (each and vs[n].get("on_question") is False),
                    re.sub(r"\s+", " ", str(vs[n].get("problem") or "") or ("not an amount of the kind the question asks for" if each and vs[n].get("on_question") is False else ""))[:240]) for n in range(1, len(parts) + 1)]
            if opening and out["opening"] is False and got[0][0]:
                got[0] = (False, (f"the word it opens with (“{opening}”) is not the answer the passages bear out" + (": " + re.sub(r"\s+", " ", str(out.get("why") or "")) if out.get("why") else ""))[:240])
            return got
    return [(False, NO_VERDICT)] * len(parts)


NO_VERDICT = "the checker gave no clear verdict"
# ---------- 5 rules ----------
FORMS = r"wax|shatter|dabs?|concentrates?|flower|buds?|edibles?|gummies|tinctures?|oils?|hash(?:ish)?|resin|cartridges?|carts|vapes?|joints?|blunts?|bongs?|powder|crystals?|rocks?|pills?|tablets?|capsules?|blotters?|liquid|patch(?:es)?|lozenges?|sprays?"
WANTED = r"satisfaction|pleasure|high|euphoria|enjoyment|effects?|functioning|function|arousal|orgasms?|libido|desire|energy|focus|creativity|relaxation|buzz|rush|trip"
RULES = [
    ("an amount of a drug", re.compile(r"\b\d+(?:[.,]\d+)?\s?(?:mg|milligrams?|µg|ug|mcg|micrograms?|g|grams?|ml|millilit(?:re|er)s?|mg/kg|iu|ounces?|oz)\b|\b\d+(?:[.,]\d+)?\s?(?:pills?|tablets?|tabs?|capsules?|lines?|hits?|drops?|puffs?|joints?|shots?|bumps?|blotters?)\b", re.I)),
    ("timing between uses", re.compile(r"\bre-?dos\w*|\b(?:wait|space)\w*\s+(?:at least\s+)?\d|\bevery\s+\d+\s+(?:minutes?|hours?)\b|\b\d+\s+(?:minutes?|hours?)\s+(?:before|after|apart)\s+(?:taking|using|the (?:first|last|next))", re.I)),
    ("a way of taking compared for strength", re.compile(r"\b(?:snort\w*|inject\w*|smok\w*|swallow\w*|plugg\w*|boof\w*|vap\w*|eaten|eating)\b[^.]{0,70}\b(?:stronger|faster|harder|more intense|more potent|better high)\b|\b(?:stronger|faster|more intense|more potent)\b[^.]{0,50}\b(?:when|if)\s+(?:snorted|injected|smoked|swallowed|vaped|eaten)\b", re.I)),
    # (lane 16) 17 November 2026: "with wax and flower forms linked to higher satisfaction" passed every reader. The forms of a drug
    # compared for an effect people want is what the site keeps for the section the senior author approves himself (Section 7).
    ("a form of a drug compared for a wanted effect", re.compile(r"\b(?:" + FORMS + r")\b[^.]{0,80}\b(?:higher|increased|greater|better|stronger|improved|more|most|best)\b[^.]{0,30}\b(?:" + WANTED + r")\b|\b(?:higher|increased|greater|better|stronger|improved|more|most|best)\b[^.]{0,30}\b(?:" + WANTED + r")\b[^.]{0,60}\b(?:with|from|for|using|after|on)\s+(?:the\s+)?(?:" + FORMS + r")\b", re.I)),
    ("how to prepare or take a drug", re.compile(r"\b(?:crush(?:ed|ing)?|dissolv\w*|cook(?:ed|ing)? (?:it|the)|extract\w* (?:it|the)|filter\w* (?:it|the)|hold (?:it )?under the tongue|on an empty stomach)\b", re.I)),
    ("making an effect stronger", re.compile(r"\bpotentiat\w*|\b(?:boost|enhanc|intensif|strengthen)\w*\s+(?:the\s+)?(?:high|effects?|trip)\b|\bmak\w+\s+(?:it|the high|the effects?|the trip)\s+(?:stronger|last longer|more intense)\b", re.I)),
    ("advice or a promise of safety", re.compile(r"\byou\s+(?:should|must|need to|ought to|can safely|had better)\b|\b(?:it is|it's|is|are)\s+(?:completely |totally |perfectly |generally |relatively )?safe\b|\bsafe to\s+(?:take|use|mix|combine|drink|smoke)\b|\bharmless\b|\brisk-free\b|\bno risk\b|\bwe (?:recommend|advise|suggest)\b", re.I)),
    ("words that are not person-first", re.compile(r"\b(?:addicts?|junkies?|abusers?|misusers?|alcoholics?|druggies?|crackheads?|stoners?|potheads?|users?|microdosers?|smokers?|drinkers?|injectors?)\b|\babus(?:e|es|ed|ing|ive)\b|\bmisus(?:e|es|ed|ing)\b|\bclean\s+(?:from|for|since)\b", re.I)),
    ("a quotation or a source in brackets", re.compile(r'["“”]|\[[A-Z]{0,2}\d*\]|\(\s*(?:[A-Z][a-z]+ et al\.?|[A-Z][a-z]+,? \d{4})')),
    ("words about the lane itself", re.compile(r"\b(?:passages?|the (?:provided|given) (?:text|items?|findings)|findings? [FDL]?\d|item [FDL]\d|as an ai|language model)\b|\b(?:Papers?|Official pages?|Sources?) [A-H]\b|\b[FDL][A-H]?\d*\]", re.I)),
    ("a sign instead of a word", re.compile(r"[×≥≤±]|\b\d+x\b")),
]
ABOUT_SOURCES = re.compile(r"\b(?:the|these|our|both|all|most)?\s*(?:sources?|studies|papers|pages|reviews?|research)\s+(?:do(?:es)? not|don'?t|doesn'?t|did not|didn'?t|never)\s+(?:say|state|tell|report|give|show|mention|address|specify|explain|cover)\b|\b(?:the|these|our)\s+sources\s+(?:lack|are missing|have no|contain no|give no|offer no|are silent)\b|\bnone of the (?:sources|studies|papers|pages)\b|\bno (?:source|study|paper|page) (?:says|states|tells|reports|gives|shows|mentions)\b|\bis not (?:stated|reported|given|mentioned|covered) in the sources\b", re.I)   # a sentence about what was NOT found: the system has not read every source in full, so it cannot say so
LIMITS = {"short": 50, "but": 40}
CLINICAL = re.compile(r"\b(?:pharmacolog\w+|pharmacokinetic\w*|pharmacodynamic\w*|abstinence symptoms?|withdrawal syndrome|cessation|efficacy|tolerability|(?:a)?etiolog\w+|comorbid\w+|prevalence|cardiovascular|gastrointestinal|neurocognitive|psychopatholog\w+|sequelae|morbidity|contraindicat\w+|intoxication|symptomatolog\w+|adverse events?)\b", re.I)   # words the lead of an answer does not use: a plain word exists
YES_NO = re.compile(r"^(?:can|could|is|are|was|were|do|does|did|will|would|should|has|have|may|might)\b", re.I)
DIRECT = re.compile(r"^(?:yes|no|not|sometimes|probably|possibly|rarely|usually|often|it can|it may|it might|it could|it depends|it does|it is not known|it is possible|nobody knows|we do not know|for some|in some|only|partly|mostly|likely|unlikely|the sources)\b", re.I)


HOW_OFTEN = [   # (the word in our sentence, the words of a source that carry it). "can", "may", "sometimes", "has been reported" need no leave: they claim less.
    ("often", r"often|frequent\w*|common\w*|regular\w*|many|a lot|widespread|typical\w*|usual\w*|most\w*|majority|general\w*|main\w*|large\w*|normal\w*|always|consistent\w*|repeated\w*"),
    ("usually", r"usual\w*|typical\w*|general\w*|most\w*|majority|main\w*|large\w*|normal\w*|always|nearly all|almost all|predominant\w*|primar\w*"),
    ("always", r"always|every\w*|all|invariab\w*|inevitab\w*|without exception"),
    ("never", r"never|no one|nobody|none|not .{0,20}\bany\b|cannot|impossib\w*|no (?:known|reported|evidence|cases?)"),
    ("certainly", r"certain\w*|definite\w*|clear\w*|prove[sdn]?|proof|established|confirmed|undoubted\w*|well[- ]known|strong evidence"),
]
SAYS_OFTEN = {"often": r"\b(?:often|frequently|commonly|regularly|a lot of the time)\b", "usually": r"\b(?:usually|typically|generally|mostly|normally|in most cases|most of the time|the majority)\b", "always": r"\b(?:always|invariably|inevitably|every time|in all cases)\b",
              "never": r"\b(?:never|no one|nobody|impossible)\b", "certainly": r"\b(?:certainly|definitely|clearly|proves?|proven|undoubtedly|without doubt|is known to)\b"}


def hedges(parts, labels):
    """What a draft says more surely or more often than its sources: [(part, what)]. A sentence may say "often",
    "usually", "always", "never" or "certainly" only where the words it rests on say as much; "can", "may", "sometimes"
    and "has been reported" are always open to it. (The second reader is asked the same; this is the part of it that code
    can see, after a real answer said "often stronger" where its source said "can also be stronger".)"""
    bad = []
    for p in parts:
        if p.get("fixed"): continue
        src = " ".join(labels[u]["quote"] + " " + (labels[u].get("passage_text") or "")[:PASSAGE_CHARS] for u in p["uses"]).lower()      # (the passage a quote stands in counts: "people who used it regularly" may stand just before the quoted words)
        for word, carried_by in HOW_OFTEN:
            m = re.search(SAYS_OFTEN[word], p["text"], re.I)
            if m and re.search(r"(?:\b(?:no|not|never|without|lacks?|neither|nor|cannot)\b|n't\b)[^.;]{0,30}$", p["text"][:m.start()], re.I): continue      # "no clear, proven boost", "not always": a word of sureness that is denied claims less, not more
            if m and not re.search(r"\b(?:" + carried_by + r")\b", src): bad.append((p["part"], f"it says “{m.group(0)}”, and the words it rests on do not: say it as the source does (“can”, “may”, “has been reported”), or rest it on the item that says so")); break
    return bad


# ---------- words that say more than their source (lane 10) ----------
# The second reader sat the exam (data/auto/exam) and let through small faults that a blind human reader caught: a praising word
# the lines do not hold ("famous"), "the most common" and "riskiest" where no rank was given, "most" where the lines give no
# share, "slightly" where they give two numbers, "had" where they say "reported", "people" where the result was for men,
# "causes" where the lines link. These are the faults code can see. Each kind below names the words of OUR sentence and what
# the words it rests on must hold to carry them; a sentence that fails is written again with the reason. Measured on the same
# exam (scripts/auto/exam.py run says-more), kind by kind, before it was put here: on the true part of the 318 cards these
# kinds catch 3 of the 31 wrong cards and stop 5 of the 287 good ones. Small, and honest: most of the exam's faults are in the
# meaning, where only a reader can see them. They are kept because each is a thing a sentence must never do.
# On the exam of the lane's OWN sentences (data/auto/exam/lane-sentences.json: the editor's verdict on each sentence the system
# wrote, 29 so far) the kinds catch 2 of the 9 that are not good and stop none of the 20 good ones, after the mends this exam
# asked for (16 November 2026): "causes" knows more of the ways a source says that one thing brings another (it had stopped two
# good sentences and caught nothing); a ceiling said as the size is a kind of its own; "statistically significant" is a term, not
# a word that makes a thing bigger; and a word of sureness that is denied ("no proven boost") claims less, not more. The last two
# had "caught" two sentences for a reason that was not their fault: a reason goes back to the writer, so it has to be the true one.
def over_half(src):
    """Does a source give a share above half (so that "most" is its own word)? "55 in 100", "62%", "62 of 64", "two thirds"."""
    t = src.lower().replace(",", "")
    if re.search(r"\b(?:two[- ]thirds|three[- ]quarters|four[- ]fifths|nine in ten|four in five|three in four|two in three|more than half|over half|majority)\b", t): return True
    for m in re.finditer(r"(\d+(?:\.\d+)?)\s*(?:%|percent|per cent|in 100|out of 100|of 100|in every 100)", t):
        if 50 < float(m.group(1)) <= 100: return True
    for m in re.finditer(r"\b(\d+)\s+(?:of|out of|in)\s+(?:the\s+)?(\d+)\b", t):
        a, b = float(m.group(1)), float(m.group(2))
        if b > 0 and a <= b and a / b > 0.5: return True
    return False


MORE = [  # (kind, the words in our sentence, what the source's words must hold: a pattern, None for "the same word", or a function of the source's text)
    ("a praising word", r"\b(?:famous\w*|well[- ]known|renowned|landmark|notorious|prestigious|respected|pioneering|ground-?breaking|seminal|influential|celebrated|world[- ]leading|leading (?:expert|scientist|researcher|journal|authorit\w+)s?|trained)\b", None),
    ("a rank", r"\b(?:the|its|their|one of the)\s+(?:single\s+|very\s+)?(?:most|least)\s+[a-z]+|\b(?:best|worst)\b|\bthe\s+(?:top|biggest|largest|greatest|highest|lowest|strongest|safest|main|leading)\b|\b(?:riskiest|deadliest|commonest|safest)\b",
     r"most|least|best|worst|top|main\w*|primar\w*|chief\w*|leading|predominant\w*|highest|lowest|greatest|largest|biggest|strongest|safest|riskiest|deadliest|commonest|first|above all|more than any|number one|rank\w*"),
    ("“most”", r"\bmost(?:\s+of)?\s+(?!common|likely|often|important|dangerous|harmful|frequent|recent|used|studied|reported|widely|commonly|frequently|people who|of all)[a-z]+|\bthe majority\b|\bmostly\b|\bmainly\b|\blargely\b",
     lambda src: bool(re.search(r"\b(?:most\w*|majority|main\w*|large\w*|predominant\w*|primar\w*|nearly all|almost all|usual\w*|typical\w*|general\w*|common\w*|chief\w*|principal\w*)\b", src, re.I)) or over_half(src)),
    ("“all” or “every”", r"(?<!at )(?<!after )(?<!not )(?<!in )\b(?:all|every|everyone|everybody)\b(?!\s+(?:in all|the same|other|year|day|week|month|night|time|\d))|\beach\b(?!\s+(?:other|year|day|week|month|night|time))",
     r"all|every\w*|each|both|entire\w*|whole|universal\w*|without exception|any|100\s*(?:%|per ?cent|in 100)|consistent\w*|always"),
    ("“both”", r"\bboth\b", r"both|two|2|each|either|neither|as well as|and also|respectively"),
    ("a word that makes it bigger", r"\b(?:severe(?:ly)?|serious(?:ly)?|heav(?:y|ily)|huge(?:ly)?|massive(?:ly)?|major|great(?:ly)?|sharp(?:ly)?|dramatic(?:ally)?|extreme(?:ly)?|highly|substantial(?:ly)?|(?<!statistically )significant(?:ly)?|rapid(?:ly)?|quick(?:ly)?|easily|intense(?:ly)?|powerful(?:ly)?|big|far (?:more|less|higher|lower|greater|stronger|worse)|much (?:more|less|higher|lower|greater|stronger|worse))\b",
     r"sever\w*|serious\w*|heav\w*|huge\w*|massiv\w*|major\w*|great\w*|sharp\w*|dramatic\w*|extrem\w*|high\w*|substantial\w*|significan\w*|rapid\w*|quick\w*|eas(?:y|ily)|intens\w*|powerful\w*|big\w*|large\w*|strong\w*|marked\w*|considerabl\w*|profound\w*|pronounced|robust\w*|potent\w*|acute\w*|notabl\w*|striking\w*|importan\w*|danger\w*|life-threatening|critical\w*|fast\w*|sudden\w*|steep\w*|"
     r"far (?:more|less|higher|lower|greater)|much (?:more|less|higher|lower|greater)|\d+(?:\.\d+)?[- ]?(?:fold|times)|double\w*|triple\w*|twice|times (?:the|as|more|higher)"),
    ("a word that makes it smaller", r"\b(?:slight(?:ly)?|mild(?:ly)?|minor|weak(?:ly)?|modest(?:ly)?|barely|marginal(?:ly)?|a little|a bit|hardly)\b",
     r"slight\w*|mild\w*|minor\w*|weak\w*|modest\w*|small\w*|little|low\w*|marginal\w*|limited|minimal\w*|negligib\w*|subtle|few|rare\w*|transient|moderate\w*|barely|hardly|not (?:clearly|significantly|statistically)|no (?:clear|significant)"),
    ("“causes”", r"\bcaus(?:e|es|ed|ing)\b|\bleads? to\b|\bled to\b|\bresults? in\b|\bresulted in\b|\btriggers?\b|\btriggered\b|\bbrings? on\b|\bbrought on\b",
     r"caus\w+|lead\w* to|led to|result\w* (?:in|from)|induc\w*|produc\w*|trigger\w*|due to|because|responsible|mediat\w*|attribut\w*|precipitat\w*|provok\w*|elicit\w*|evok\w*|bring\w* (?:on|about)|brought (?:on|about)|by (?:blocking|activating|binding|increasing|reducing|inhibiting|releasing|stimulating|acting)|effects? of|consequence\w*|"
     r"(?:increas|decreas|reduc|rais|lower|impair|damag|depress|suppress|slow|worsen|improv)\w*|"
     r"degenerat\w* into|turn\w* into|develop\w* into|progress\w* to|giv\w+ rise|becom\w+|became|mak(?:e|es|ing)|made|follow\w+|from (?:using|taking|drinking|smoking)|"
     r"after (?:frequent|regular|heavy|long|prolonged|repeated|chronic)|if you\b[^.]{0,80}\b(?:may|can|will|might|could)"),
]
# An upper bound said as the size (lane 10, after the editor's reading of 16 November 2026: a source said "by as much as 2–5 times" and
# our sentence said "2–5 times"). Where a source gives a number as a ceiling, our sentence gives it as a ceiling too.
BOUND = r"(?:as (?:much|many|high|long|often|great|large) as|up to|at most|no more than|not more than|a maximum of|maximum of|or (?:less|fewer|lower)|at the most|reach(?:es|ed|ing)?)"
NUM_OR_RANGE = r"(\d+(?:[.,]\d+)?)(?:\s?(?:[–-]|to)\s?(\d+(?:[.,]\d+)?))?"


def ceiling_as_size(ours, src):
    """The source's words for a number it gives as a ceiling and that our sentence gives without one, or None."""
    for m in re.finditer(r"\b" + BOUND + r"\s+(?:about\s+|approximately\s+|nearly\s+|around\s+|roughly\s+)?" + NUM_OR_RANGE, src, re.I):
        nums = [x for x in m.groups() if x]
        for mo in re.finditer(NUM_OR_RANGE, ours):
            if [x for x in mo.groups() if x] == nums and not re.search(r"\b" + BOUND + r"\b", ours[max(0, mo.start() - 40):mo.end() + 14], re.I): return m.group(0)
    return None
# (lane 19) Only the words "men" and "women" say that a result was for one sex. "Male" and "female" stand beside a word for people that the second pattern
# holds anyway ("20 healthy male volunteers": volunteers), or beside animals, or alone of animals ("in males, the extract decreased anxiety-like behavior"):
# on 17 and 18 November 2026 an answer to a question the senior author had sent (Does kanna help with anxiety?) was refused six times as "a result for men"
# where the study was of 16 healthy participants. Measured on the exam before the change and after it (scripts/auto/exam.py run says-more): the same cards
# caught and the same cards stopped.
ONE_SEX = [(re.compile(r"\bmen\b", re.I), re.compile(r"\b(?:women|females?|both sexes|men and women|people|participants|adults|persons|individuals|volunteers|patients|users|students|respondents|subjects)\b", re.I), re.compile(r"\b(?:men|males?)\b", re.I), "men"),
           (re.compile(r"\bwomen\b", re.I), re.compile(r"\b(?:\bmen\b|\bmales?\b|both sexes|people|participants|adults|persons|individuals|volunteers|patients|users|students|respondents|subjects)\b", re.I), re.compile(r"\b(?:women|females?)\b", re.I), "women")]
ANYBODY = re.compile(r"\b(?:people|everyone|anyone|adults|persons|those who|the public)\b", re.I)
# (lane 19) "male Wistar rats", "female mice": the sex of animals is no result for men or for women. On 17 November 2026 an answer to a question the senior
# author had sent (Does kanna help with anxiety?) was refused three times for "the source gives this for men" where the study was of 16 healthy participants
# and the word "male" stood beside animals in the review's passage.
ANIMAL_SEX = re.compile(r"\b(?:fe)?males?\s+(?:(?!and\b|or\b)[\w-]+\s+){0,3}?(?:rats?|mice|mouse|rodents?|animals?|monkeys?|macaques?|primates?|dogs?|pigs?|piglets?|rabbits?|zebrafish|hamsters?|gerbils?|guinea pigs?|offspring|pups?)\b|\b(?:rats?|mice|animals?|rodents?)\s+of\s+(?:both|either)\s+sex(?:es)?\b", re.I)


def says_more_text(ours, src):
    """What one sentence says that the words it rests on do not carry: [(kind, the words, how to mend it)]."""
    out = []
    for kind, mine, carried in MORE:
        m = re.search(mine, ours, re.I)
        if not m: continue
        w = m.group(0)
        ok = (carried(src) if callable(carried) else bool(re.search(r"\b(?:" + carried + r")\b", src, re.I)) if carried else bool(re.search(r"\b" + re.escape(w.split()[0][:6]), src, re.I)))
        if not ok: out.append((kind, w, f"it says “{w}”, and the words it rests on carry no such word: say what the source says, in its own measure, or leave the word out"))
    # (tried and not put to work: "the source gives what people reported; our sentence says it was so". On the exam it stopped 12 good cards
    # for 2 wrong ones: "reported" stands near too many things. The second reader is asked about it instead.)
    c = ceiling_as_size(ours, src)
    if c: out.append(("a ceiling said as the size", c, f"the source says “{c}”: that is the most it found, not the size. Say “up to” or “as much as”, as the source does"))
    people_src = ANIMAL_SEX.sub(" ", src)
    for only, others, in_ours, name in ONE_SEX:
        if only.search(people_src) and not others.search(people_src) and ANYBODY.search(ours) and not in_ours.search(ours):
            out.append((f"a result for {name}, said of people", "", f"the source gives this for {name}: say “{name}”, not people in general")); break
    return out


# (lane 18) What people perceive or say of themselves, said as what is. On 17 November 2026 a survey's "positive influence on perceived
# sexual functioning and satisfaction" became "tends to positively influence sexual functioning and satisfaction" in eight sentences of
# four runs, and the second reader accepted most of them. The rule is narrow on purpose (an earlier, wider one on "reported" stopped 12
# good cards for 2 wrong ones and was not put to work): the source's own quoted words say "perceived", "self-reported", "self-rated",
# "self-assessed" or "subjective" of a thing, our sentence names that thing, and nothing in our sentence says that people said, felt or
# rated it. Measured before it was put here: on the exam of the lane's own sentences (104 judged) it catches 8 of the 34 that are not
# good (all eight are the sentences it was written for, so this is not a fresh measure) and stops none of the 70 good ones; on the 318
# cards it stops 1 good card ("self-rated depression fell") and catches no wrong one.
SELF_SEEN = re.compile(r"\b(perceived|self-reported|self-rated|self-assessed|subjective)\s+((?:[a-z-]+\s+){0,2}[a-z-]+)", re.I)
SELF_SAID = re.compile(r"\b(?:perceiv\w+|self-\w+|subjective\w*|said|say|says|saying|felt|feel|feels|feeling|rated|rate|rating|see|saw|seen|describ\w+|experienc\w+|told|(?:people|men|women|adults|participants|respondents|they|who)\s+(?:also\s+)?report\w*)\b", re.I)


def as_was(ours, quotes):
    """The source's words for what people perceive or say of themselves, where our sentence names the same thing as what is; else None."""
    if SELF_SAID.search(ours): return None
    for m in SELF_SEEN.finditer(quotes):
        if any(re.search(r"\b" + re.escape(h), ours, re.I) for h in re.findall(r"[a-z]+", m.group(2).lower()) if len(h) >= 6): return m.group(0)
    return None


def says_more(parts, labels):
    """What a draft says that its sources do not carry (the kinds in MORE, what people say of themselves said as what is, a result for one sex said of people): [(part, what)]."""
    bad = []
    for p in parts:
        if p.get("fixed"): continue
        src = " ".join(labels[u]["quote"] + " " + (labels[u].get("passage_text") or "")[:PASSAGE_CHARS] for u in p["uses"])
        found = says_more_text(p["text"], src)
        if found: bad.append((p["part"], found[0][2])); continue
        w = as_was(p["text"], " ".join(labels[u]["quote"] for u in p["uses"]))
        if w: bad.append((p["part"], f"its source says “{w}”: that is what people perceived or said of themselves, not what was measured. Keep the word (“perceived”), or say that people said so"))
    return bad


def lead(question, parts):
    """What the site's way of answering has against a draft's first two sentences: [(part, what)]. A question that can be
    answered with yes or no is answered so, first; the short answer and the But use everyday words."""
    bad = []
    for p in parts:
        if p["part"] not in ("short", "but"): continue
        m = CLINICAL.search(p["text"])
        if m: bad.append((p["part"], f"a clinical word where an everyday one exists (“{m.group(0)}”): say it plainly"))
        if ABOUT_SOURCES.search(p["text"]): bad.append((p["part"], "it says what the sources do not say: only a part of each source was read. Let the But be a finding that says for whom or under what conditions the answer holds, or a limit a source states itself"))
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
    # (2.25.0; the senior author, 19 November 2026, 17:48: "we should not always say 'our system' ... it creates unecessary words") the claims and
    # their evidence, nothing about the system: what the answer rests on
    return f"This rests on {what}."


def mend_uses(parts, labels, years=(), asked=()):
    """(lane 19) What code can mend before a rule judges: a number that a sentence states and that stands, not in the items the writer named for it, but in
    ANOTHER item of a source the sentence already rests on (the item that says what kind of study it was, most often: "16 healthy participants"). That item is
    added to what the sentence rests on, so the second reader, the further readers and our own checker read the sentence beside it too. The rule itself stands:
    every number of a sentence is in the words it rests on. Never an item of another source, never a year. Returns [(part, the item added, the number)].
    (17 November 2026: the writer wrote "in 16 healthy people" three times over, named the finding and not the item that holds the 16, and a good answer to a
    question the senior author had sent was thrown away.)"""
    mended = []; skip = {str(y) for y in years} | {str(a) for a in asked}
    for p in parts:
        if p.get("fixed") or not p.get("uses"): continue
        refs = {labels[u].get("ref") for u in p["uses"]} - {None}
        for x in sorted(numbers(p["text"]) - skip):
            if x in set().union(*[numbers(labels[u].get("quote") or "") for u in p["uses"]]): continue
            more = sorted((u for u in labels if u not in p["uses"] and labels[u].get("ref") in refs and x in numbers(labels[u].get("quote") or "")), key=lambda u: (0 if u.startswith("D") else 1, u))
            if more: p["uses"].append(more[0]); mended.append((p["part"], more[0], x))
    return mended


# (lane 19, 18 November 2026) "Relatively large amounts of kratom need to be consumed before a noticeable psychoactive effect occurs" was the But of a published
# answer: a health charity's own words, with no number in them, and yet it tells a reader how much it takes to feel the drug. The site gives no such guidance
# anywhere. Narrow by design: of the 523 sentences the lane had written by that day (shown, refused or dropped) it stops this one and no other; what tolerance
# is (more is needed for the same effect) is a fact about dependence and is not stopped.
NEEDED_FOR = re.compile(r"\b(?:amounts?|doses?|quantit(?:y|ies))\b[^.]{0,60}\b(?:needs?|needed|required|necessary|must|have to|has to)\b[^.]{0,40}\b(?:to be (?:consumed|taken|used|eaten|swallowed|smoked)|before|to (?:feel|get|notice|produce|have|reach|achieve|experience))\b[^.]{0,60}\b(?:effects?|high)\b"
                        r"|\b(?:takes?|needs?|requires?)\s+(?:a\s+)?(?:relatively\s+|fairly\s+|quite\s+|very\s+)?(?:large|larger|high|higher|big|bigger)\s+(?:amounts?|doses?)\b[^.]{0,60}\b(?:to|before|for)\b[^.]{0,40}\b(?:effects?|high|feel\w*)\b", re.I)
NEEDED_SKIP = re.compile(r"\btoleran\w*|\bsame effect\b", re.I)


def rules(parts, labels, years=(), asked=()):
    """What the site's content rules have against a draft: [(part, what)]. Empty when nothing. years: the years the answer's
    sources were published. A sentence may name the year of a source IT rests on ("a 2022 review"), not another source's
    (lane 11: the first real run of lane 10 wrote "A 2022 review says" over the words of a paper of 2023, because the answer
    also had a source of 2022; the second reader and our own checker let it through). asked: the numbers of the question itself."""
    bad = []; all_years = {str(y) for y in years}
    for p in parts:
        for what, rx in RULES:
            m = rx.search(p["text"])
            if m: bad.append((p["part"], f"{what} (“{m.group(0)}”)"))
        for sent in re.split(r"(?<=[.!?])\s+", p["text"]):
            m = NEEDED_FOR.search(sent)
            if m and not NEEDED_SKIP.search(sent): bad.append((p["part"], f"how much is needed for an effect (“{m.group(0)}”): say what the drug does, never how much it takes to feel it")); break
        if words(p["text"]) > LIMITS.get(p["part"], 40): bad.append((p["part"], f"too long ({words(p['text'])} words)"))
        # (lane 16) what a source reports from another study is not what that source found
        cited = [u for u in p["uses"] if labels[u].get("second_hand")]; m = OWN_FIND.search(p["text"])
        if cited and m and not SECOND_SAID.search(p["text"]):
            bad.append((p["part"], f"it says its source found (“{m.group(0)}”) what that source only reports from another study ({', '.join(cited)}): say that the source reports or cites that earlier work, called what the passage calls it (“an earlier meta-analysis”, “one study”), or name no finder"))
        have = set().union(*[numbers(labels[u]["quote"]) for u in p["uses"]])
        known = [labels[u] for u in p["uses"] if "year" in labels[u]]                       # (labels that say which year their source is of; where none does, as before: any source's year)
        own = {str(l["year"]) for l in known if l.get("year")} if known else all_years
        extra = numbers(p["text"]) - have - own - {str(a) for a in asked}
        other = sorted(x for x in extra if x in all_years)
        if other: bad.append((p["part"], f"the year {', '.join(other)} belongs to another source: the source this sentence rests on is " + (f"of {', '.join(sorted(own))}" if own else "a page with no year") + ". Name the right one, or no year"))
        extra -= set(other)
        if extra:
            at = sorted(u for u in labels if u not in p["uses"] and any(x in numbers(labels[u].get("quote") or "") for x in extra))[:3]      # (lane 19) the writer is told where the number does stand
            bad.append((p["part"], "a number that is not in the paper's words it rests on (" + ", ".join(sorted(extra)) + ")" + (": it stands in " + ", ".join("[" + u + "]" for u in at) + "; name that item too among the ones this sentence rests on if the sentence is about that same study, or leave the number out" if at else "")))
    return bad


# ---------- 7 stakes ----------
STAKES = [("dying", re.compile(r"\b(?:die|dies|died|dying|death|deaths|deadly|fatal\w*|lethal\w*|kill|kills|killed|killing)\b", re.I)),
          ("overdose or an emergency", re.compile(r"\boverdos\w*|\bod(?:'?ing|'?ed)?\b|\bemergenc\w*|\bnaloxone\b|\bnarcan\b|\bpoisoning\b|\bunconscious\w*|\bnot breathing\b|\bseizures?\b|\boveramp\w*", re.I)),
          ("mixing drugs", re.compile(r"\b(?:mix|mixing|mixed|combin\w*|together with|at the same time|on top of|interact\w*)\b", re.I)),
          ("pregnancy or children", re.compile(r"\bpregnan\w*|\breproductive[- ]aged?\b|\bchild-?bearing\b|\bconceiv\w*|\bconception\b|\bbreast-?feed\w*|\bf(?:o)?etus\b|\bf(?:o)?etal\b|\bbab(?:y|ies)\b|\bbirth defects?\b|\bnewborns?\b|\bchild(?:ren)?\b|\bkids?\b|\bteen\w*|\badolescen\w*|\bminors?\b|\byouths?\b|\byoung people\b|\bp(?:a)?ediatric\w*|\binfants?\b|\btoddlers?\b|\bunderage\b|\bunder\s+(?:the\s+age\s+of\s+)?(?:1[0-8]|[1-9])\b|\bboys?\b|\bgirls?\b|\bschool\w*|\blactat\w*|\bnursing (?:mothers?|women)\b", re.I)),
          ("suicide or self-harm", re.compile(r"\bsuicid\w*|\bself-harm\w*", re.I))]


def stakes(question, parts):
    """Why this answer waits for a person, or "". The question decides first; then the answer's own words."""
    text = question + " " + " ".join(p["text"] for p in parts)
    for what, rx in STAKES:
        if rx.search(question) or (what != "mixing drugs" and rx.search(text)): return what
    return ""


# (lane 19) The senior author, 18 November 2026, 13:34 Athens: "the questions should be automatically answered no 'Written. A person has to check it first' ---
# this should happen for every pending question"; "can the answers get ... answered by themselves?". Until that day every answer about dying, overdose, an
# emergency, mixing, pregnancy, children or suicide waited for a person (the editor's rule of 15 November). What each kind does now is a setting, not code
# (data/auto/lane/policy.json, "stakes": {kind: "strict" | "person"}; a kind that is not named there waits for a person, as before):
#   "strict"  published by the system only where it meets a bar that is higher than every other answer's, all of it code (strict_lacks): its short answer
#             rests on an official body's page or on a review read in full; a further reader read it (none was out of reach); no word of its first two
#             sentences can be read as a promise of safety (plays_down), its opening word does not say that a danger is absent or that a thing may be done,
#             and every reader, asked that very question, said that it does not play a danger down. An answer that does not meet the bar is not parked for a
#             person: there is no answer yet, and the system tries again like for any other question.
#   "person"  written, and it waits for an editor.
# Whatever the setting says, three things never go out by themselves: an amount that kills (make_amounts), what to do in an emergency (NEVER_ALONE: emergency
# guidance is the senior author's own text), and an answer that disagrees with a checked claim.
NEVER_ALONE = re.compile(r"\bwhat\s+(?:should|do|can|must|to)\s+(?:(?:i|you|we|one|someone|somebody|a person|people)\s+)?(?:do|to do)\b|\bwhat to do\b|\bhow\s+(?:to|do\s+(?:i|you|we)|can\s+(?:i|you|we)|should\s+(?:i|you|we))\s+(?:help|treat|save|revive|respond|reverse|handle|deal with|wake|stop an?)\b|\bfirst[- ]aid\b|\bnaloxone\b|\bnarcan\b|\brecovery position\b|\bcpr\b", re.I)
ASKS_LEAVE = re.compile(r"\b(?:safe|safely|ok|okay|fine|alright|all right|harmless|allowed)\b|^\s*(?:can|could|may|should)\s+(?:i|you|we|one|someone|people|a person|my\s+\w+|pregnant\s+\w+|kids|children|teens?|teenagers)\b(?![^?]*\b(?:die|dying|overdos\w*|od|addict\w*|hooked|harm\w*|hurt\w*|kill\w*|damag\w*|poison\w*|sick|ill|dangerous)\b)", re.I)   # a question that asks whether a thing may be done: there "Yes" is the word that reassures
REASSURES = re.compile(r"\b(?:safe|safely|safer|safest|harmless|low[- ]risk|risk[- ]free|well[- ]tolerated|no\s+(?:known\s+|real\s+|serious\s+|major\s+|significant\s+|clear\s+)?(?:risks?|dangers?|harms?|deaths?|problems?|effects?|link|evidence)|not\s+(?:dangerous|harmful|risky|toxic|deadly|fatal|lethal|a\s+(?:risk|danger|problem|concern))|un(?:likely|common)|rare(?:ly)?(?!,?\s+but\b)|seldom|hardly|minimal|negligible|mild(?:ly)?|small\s+(?:risk|chance)|little\s+(?:risk|danger|harm|evidence)|cannot\s+(?:overdose|die|kill)|can'?t\s+(?:overdose|die|kill)|impossible|fine|okay|nothing\s+to\s+worry)\b", re.I)


def plays_down(question, parts):
    """(lane 19) Why the first two sentences of an answer can be read as saying that a danger is small or absent, by code; "" where the code sees nothing.
    The words (REASSURES), and the word the answer opens with: "Yes" where the question asks whether a thing may be done or is safe, "No" where it asks
    whether a thing harms. This is one of two looks; the readers are asked the same of the whole lead (checker_prompt, risk)."""
    for p in parts:
        if p["part"] not in ("short", "but") or p.get("fixed"): continue
        m = REASSURES.search(p["text"])
        if m: return f"its {p['part']} holds words that can be read as saying a danger is small or absent (“{m.group(0)}”)"
    short = next((p["text"] for p in parts if p["part"] == "short"), "").strip()
    m = re.match(r"(yes|no|not|unlikely|rarely|usually|often|mostly|probably|likely)\b", short, re.I); op = m.group(1).lower() if m else ""
    if ASKS_LEAVE.search(question or ""):
        if op in ("yes", "usually", "often", "mostly", "probably", "likely"): return f"the question asks whether a thing may be done, and the answer opens with “{m.group(1)}”"
    elif op in ("no", "not", "unlikely", "rarely"): return f"the question asks about a danger, and the answer opens with “{m.group(1)}”"
    return ""


def strict_lacks(question, rec, parts, sources, labels, said):
    """(lane 19) What an answer about dying, overdose, mixing, pregnancy or children lacks of the stricter bar ([] where it meets it). said: what each reader
    answered when asked whether the lead plays a danger down (True, False, or None for no clear word)."""
    lacks = []
    refs = {labels[u].get("ref") for p in parts if p["part"] == "short" for u in p["uses"]}
    if not any(s["ref"]["id"] in refs and ((s["read"] == "page" and s.get("tier", 1) == 1) or (s["read"] == "full" and s.get("kind") == "review")) for s in sources): lacks.append("its short answer rests on no official body's page and on no review read in full")
    if rec.get("panel_gap") or not any(isinstance(v, dict) for v in (rec.get("panel") or {}).values()): lacks.append("no further reader read it")
    code = plays_down(question, parts)
    if code: lacks.append(code)
    if not said or any(v is not False for v in said): lacks.append("a reader found that its lead can be read as saying a danger is small or absent" if any(v is True for v in said) else "a reader gave no clear word on whether its lead plays a danger down")
    return lacks


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


CLAIMS = ROOT / "data" / "claims"
AGREE_SYS = ("You compare sentences for Pharmakon, a drug encyclopedia. In each numbered PAIR, A is a sentence a machine wrote from sources it read, and B is a statement of the site that readers checked against studies. "
             "You say how A stands to B. JSON only.")


def checked_claims(drugs):
    """The checked claims of these drugs' pages: [{"id", "drug", "text"}], each with its plain line (and its exact
    statement, which the second reader sees). The machine lane never edits them: it reads them to see whether what it
    wrote agrees with what was checked."""
    out = []
    for d in drugs or []:
        try: cs = json.load(open(CLAIMS / (d + ".json"), encoding="utf-8"))
        except (OSError, ValueError): continue
        for c in cs if isinstance(cs, list) else []:
            if isinstance(c, dict) and c.get("id") and (c.get("plain") or c.get("statement")): out.append({"id": c["id"], "drug": d, "plain": str(c.get("plain") or ""), "statement": str(c.get("statement") or "")})
    return out


def with_checked(chat, model, enc, parts, claims, near=0.5, most=8):
    """How a machine-written answer stands to the checked claims of the same page (decision 17d; the senior author,
    15 November 2026: the answers must be "coherent with the rest of the website"): ([{"part", "claim", "why"}] where a
    sentence cannot be true together with a checked claim, [{"part", "claim"}] where it says the same). Each sentence is
    set beside the checked claims nearest to it in meaning (at most three, none that is far), and the second reader says
    of each pair: the same, differs, or about something else. Nothing here changes a claim."""
    sents = [p for p in parts if not p.get("fixed") and p.get("text")]
    if not sents or not claims: return [], []
    import numpy as np
    S = enc([p["text"] for p in sents]); C = enc([c["plain"] or c["statement"] for c in claims]); sim = np.asarray(S @ C.T)
    pairs = sorted(((float(sim[i, j]), i, j) for i in range(len(sents)) for j in np.argsort(-sim[i])[:3] if sim[i, j] >= near), reverse=True)[:most]
    if not pairs: return [], []
    body = "\n\n".join(f"PAIR {n}.\nA (machine): {sents[i]['text']}\nB (checked): {claims[j]['plain'] or claims[j]['statement']}" + (f"\n   B in exact words: {claims[j]['statement'][:500]}" if claims[j]["plain"] and claims[j]["statement"] else "") for n, (_, i, j) in enumerate(pairs, 1))
    out = ask_json(chat, model, AGREE_SYS, body + "\n\nFor each pair, \"is\": \"same\" if A says what B says, or a part of it; \"differs\" if A and B cannot both be true as they stand (opposite directions, or different numbers for the very same thing in the same people); "
                   "\"other\" if they are about different things, different people or different conditions, so that both can be true. Say \"differs\" only where they truly cannot both hold.\n"
                   'JSON only: {"pairs": [{"n": 1, "is": "same", "why": ""}, {"n": 2, "is": "other", "why": ""}]}', room_for(model, 100 + 60 * len(pairs)))
    got = {v.get("n"): v for v in (out or {}).get("pairs") or [] if isinstance(v, dict)}
    differs = [{"part": sents[i]["part"], "claim": claims[j]["id"], "why": re.sub(r"\s+", " ", str(got.get(n, {}).get("why") or ""))[:240]} for n, (_, i, j) in enumerate(pairs, 1) if got.get(n, {}).get("is") == "differs"]
    same = [{"part": sents[i]["part"], "claim": claims[j]["id"]} for n, (_, i, j) in enumerate(pairs, 1) if got.get(n, {}).get("is") == "same"]
    return differs, same


class Begun:
    """Sources begun together (19 November 2026). With a semaphore: each job in a thread of its own, as many at a time as the semaphore lets; all() gives
    their outcomes in the jobs' own order, and ("late",) for one that had not ended by `until` (a moment: time.time()). The threads are daemons: a job
    stuck in a slow request ends with that request's own time limit and never holds the run. Without a semaphore nothing is begun before all() is asked,
    which runs the jobs one after another (the selftest; a trial). A job's own error comes back as ("error", it): raised where the outcome is taken."""
    def __init__(self, jobs, sem=None, until=None):
        self.jobs, self.sem, self.until = list(jobs), sem, until
        self.out = [("late",)] * len(self.jobs); self.done = [threading.Event() for _ in self.jobs]
        if sem is not None:
            for i in range(len(self.jobs)): threading.Thread(target=self._run, args=(i,), daemon=True).start()
    def _one(self, i):
        if self.until is not None and time.time() >= self.until: return ("late",)
        try: return self.jobs[i]()
        except llm.Late: return ("late",)
        except BaseException as e: return ("error", e)
    def _run(self, i):
        with self.sem:
            self.out[i] = self._one(i); self.done[i].set()
    def all(self):
        if self.sem is None: return [self._one(i) for i in range(len(self.jobs))]
        for ev in self.done: ev.wait(None if self.until is None else max(0.0, self.until - time.time()))
        return [o if ev.is_set() else ("late",) for o, ev in zip(list(self.out), self.done)]


def make(item, found, chat, enc, models, fulltext=None, crossref=None, ex=None, official=None, page=None, summary=None, names=None, before=None, claims=None, own_check=None, stakes_how=None, note="", agreed=(), last="", pool=None, at_once=1, read_secs=None):
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
    spent = llm.ledger()["neurons"]; t_began = time.time()
    def done(status, why):
        rec["status"], rec["why"] = status, why; rec["made"]["neurons"] = round(llm.ledger()["neurons"] - spent, 1); rec["made"]["seconds"] = round(time.time() - t_began); return rec
    dwords = O.drug_words(item, names)[1] if names else [d.replace("-", " ") for d in item.get("drugs") or []]
    # 2 read: papers in full, then official pages, then (where that is not yet enough) reviews in summary
    # (19 November 2026; the senior author, 18 November, 23:42 Athens: "the site is taking too long to answer my pending questions ... it should be answered
    # almost immediately".) The sources are read AT ONCE. Until then each was fetched and read after the one before, each call waiting out its model's minute:
    # a question none of whose sources answered it took 21 calls and 34 minutes. Now the nearest papers and the first official pages are fetched and read at
    # the same time (at_once threads), by every model that may read (the team's reader and the readers of data/auto/lane/models.json, "readers": each has its
    # own calls a minute), and what they found is KEPT IN THE SOURCES' OWN ORDER, exactly as if they had been read one after another: the two first papers
    # that give a finding, then the two first pages. What was read ahead and is not needed is put aside (it serves if a third paper is wanted). The reading
    # has its own time (read_secs): a source not read by then is written down as not read, and the answer is written from the rest. No gate changes: a reader
    # only copies, and every quote it copies is checked by code against the passage. With at_once 1 (the selftest; a trial) nothing is read ahead.
    sources, tags, thrown, ref_ids = [], "ABCDEFGHIJKL" if amounts else "ABCDEFGH", 0, set()      # (lane 11) twelve sources at most for a question about amounts: six official pages have room beside the papers
    looked = rec["looked"] = []                                         # every source the reader was given, with what was thrown away and why (for the editor)
    QV = enc([item["q"]] + list(item.get("ways") or [])[:6])
    threaded = at_once > 1; guard = threading.RLock(); enc_guard = threading.Lock()
    read_until = (time.time() + read_secs) if read_secs else None
    not_these = {base(v) for v in (models.get("writer"), models.get("writer_2"), models.get("checker")) if isinstance(v, str) and v}
    extra = [m for m in (pool or []) if isinstance(m.get("model"), str) and m["model"] not in (models.get("reader"), models.get("reader_2")) and base(m["model"]) not in not_these]
    mains = [models["reader"]] + [m["model"] for m in extra]            # the models that read side by side
    by_turn = [m for m in [models.get("reader_2")] if m and m != models["reader"]]      # the reader that stands by: asked only where another could not be
    takes = dict({m["model"]: float(m.get("secs") or 10) for m in extra}, **{models["reader"]: float(next((m.get("secs") for m in (pool or []) if m.get("model") == models["reader"]), 10) or 10)})
    gone, read_by, busy = {}, {}, {}                                    # a reader that could not be asked, and why (it is not asked again for this answer); how many sources each model read; when each is free again
    def between(m):
        """Seconds between two reading calls of one model, as its free plan lets it take them (calls a minute; tokens a minute for a call of a reader's size)."""
        try:
            if m.startswith("groq:"): return max(2.2, 60.0 * (3600 + room_for(m, 900)) / llm.GROQ_FREE[m[5:]]["tpm"])
            if llm.service_of(m)[0]: lim = llm.limits_of(m); return max(lim["gap"], 60.0 * (3600 + room_for(m, 900)) / (llm.OF_A_DAY * lim["tpm"]) if lim["tpm"] else 0)
        except Exception: pass
        return 0.5
    def readers_for_one():
        """The readers for the next source, the one that will have read it soonest first; then the others, then the one that stands by."""
        with guard:
            live = [m for m in mains if m not in gone]
            if len(live) > 1:
                now = time.time(); best = min(live, key=lambda m: max(now, busy.get(m, 0)) + takes.get(m, 10)); busy[best] = max(now, busy.get(best, 0)) + between(best)
                live = [best] + [m for m in live if m != best]
            return (live or mains[:1]) + by_turn
    def by_reader(fn, *a):
        """(lane 14) The reader's call. A reader of a free service that is busy or used up must not cost the answer: another reader reads this source, and
        that one is not asked again for this answer. Returns (what the reader gave, the model that read)."""
        order = readers_for_one(); last = None; tried = []
        for m in order:
            with guard:
                if m in gone and len(order) > 1: continue
            tried.append(m)
            try: return fn(chat, m, *a), m
            except llm.Late: raise
            except (llm.Unavailable, llm.Budget) as e:
                last = e
                if "larger than Groq's free plan allows" in str(e) and len(order) > 1: continue        # (this call is too large for that model's minute: another reader takes this source; the model reads on)
                with guard: gone.setdefault(m, re.sub(r'[ \t\n]+', ' ', str(e))[:140])
                if len(order) == 1 or "larger than Groq's free plan allows" in str(e): raise
        # (18 November 2026, 21:36 and 22:55 Athens: with questions people had sent still waiting, team L's reader could not read on, the reader that stands
        # by (at Groq) had no tokens left, and that came up as "an allowance ran out in the middle of an answer": twice, and the run said "stopped for
        # today" although the team's own models had room.) Readers without room are not the day's end: the answer is given up for THIS run, as when a
        # model cannot be reached, with what the first reader said, and the question is tried again in the next run
        if isinstance(last, llm.Budget) and len(tried) > 1: raise llm.Unavailable(f"{base(tried[0])} could not read on ({gone.get(tried[0], '')}), and the reader that stands by ({base(tried[-1])}) has no room left today")
        raise last if last is not None else llm.Unavailable("no reader could be asked")
    def keep(src, picked, got, by):
        """What a reader gave for one source, taken into the answer (in the sources' own order): True when it gave something."""
        nonlocal thrown
        read_by[by] = read_by.get(by, 0) + 1
        if amounts: rows, dropped = got; src["rows"] = rows; ok = bool(rows); src.update(design=None, findings=[], limits=[])
        else:
            design, fs, ls, dropped = got
            if len(fs) > N_TO_WRITER:                                    # the nearest to the question, in the order they stand in the source
                near = (enc([f["text"] for f in fs]) @ QV.T).max(1); keep_i = sorted(sorted(range(len(fs)), key=lambda i: -float(near[i]))[:N_TO_WRITER]); fs = [fs[i] for i in keep_i]
            if len(ls) > 1: ls = [ls[int((enc([l["text"] for l in ls]) @ QV.T).max(1).argmax())]]      # one limit: the one nearest the question
            src.update(design=design, findings=fs, limits=ls[:1]); ok = bool(fs)
        thrown += len(dropped)
        looked.append({"title": src.get("title"), "read": src["read"], "kind": src.get("kind"), "at": src.get("address") or src.get("doi"), "kept": len(src.get("rows") or []) if amounts else len(src.get("findings") or []), "thrown": dropped[:12]})
        if not ok: return False
        ref = src["ref"]
        while ref["id"] in ref_ids: ref["id"] = ref["id"] + "b" if not re.search(r"[b-z]$", ref["id"]) else ref["id"][:-1] + chr(ord(ref["id"][-1]) + 1)
        ref_ids.add(ref["id"]); src["tag"] = tags[len(sources)]; src["_text"] = {p["n"]: p["text"] for p in picked}; sources.append(src)
        return True
    def ask(src, picked):
        """One source that is ready, through a reader: ("read", the source, its passages, what the reader gave, the model)."""
        got, by = by_reader(read_amounts, item["q"], src, picked, dwords) if amounts else by_reader(read_source, item["q"], src, picked)
        return ("read", src, picked, got, by)
    paper_ref = lambda doi, pmcid=None: (lambda cr: P.reference(doi, cr[0], pmcid) if cr[0] else None)(crossref(doi))
    def paper(c):
        """One paper fetched and read in full (no word of it is kept here: `taken` does that, in the papers' own order)."""
        if not c.get("doi"): return ("skip",)
        if c["kind"] not in ("review", "study", "case") and not c.get("people"): return ("skip",)   # an editorial, an opinion, a paper on animals or cells alone: not a source for an answer
        ref = paper_ref(c["doi"], c.get("pmcid"))
        if not ref or P.retraction(ref) in ("retracted", "concern"): return ("skip",)      # GATE 6, first half: never a retracted paper
        try: xml = fulltext(c.get("pmcid"))
        except (P.Refused, IOError, ValueError) as e:                 # (lane 19, 18 November 2026) one paper whose full text the service fails on (Europe PMC answers 500 for some) cost a question every try it had: "the lane itself failed on it (HTTPError)". The paper is passed over and the record says so
            return ("fault", {"title": c.get("title"), "read": "full", "kind": c.get("kind"), "at": c.get("doi"), "kept": 0, "thrown": [], "fault": f"its full text could not be fetched ({type(e).__name__})"})
        if not xml: return ("skip",)
        doc = P.jats_passages(xml)
        if len(doc["passages"]) < 4: return ("skip",)
        with enc_guard: picked = pick_passages(item["q"], item.get("ways"), doc["passages"], enc, c["kind"])
        return ask({"read": "full", "ref": ref, "doi": c["doi"], "pmcid": c.get("pmcid"), "title": c["title"], "year": c.get("year"), "journal": c.get("journal"), "kind": c["kind"], "people": bool(c.get("people")), "near": c.get("near"), "money": doc["money"][:3],
                    "_abbr": abbreviations(" ".join(p["text"] for p in doc["passages"]))}, picked)
    def a_page(o):
        """One official page fetched and read."""
        try: got = page(o)
        except P.Refused: return ("skip",)                                      # (a site that says no is not asked again and not gone around)
        except (IOError, ValueError) as e: return ("fault", {"title": o.get("title") or o.get("name"), "read": "page", "kind": "official", "at": o.get("address"), "kept": 0, "thrown": [], "fault": f"the page could not be fetched ({type(e).__name__})"})
        if not got or len(got[0]["passages"]) < 2: return ("skip",)
        pg, ref = got
        with enc_guard: picked = pick_passages(item["q"], item.get("ways"), [dict(p, n=p["n"] + 1, where=p["where"] or "Top of the page") for p in pg["passages"]], enc, "review", k=7)
        return ask({"read": "page", "ref": ref, "title": pg["title"] or o.get("title") or "", "year": ((ref.get("issued") or {}).get("date-parts") or [[]])[0][:1] and ref["issued"]["date-parts"][0][0] or None, "kind": "official", "people": True,
                    "near": o.get("near"), "name": o["name"], "short": o.get("short") or o["name"], "tier": o.get("tier", 1), "address": ref.get("URL"), "money": [], "label": bool(o.get("label")),
                    "_abbr": abbreviations(" ".join(p["text"] for p in pg["passages"]))}, picked)
    def a_summary(w):
        """One review that cannot be read in full, read in its summary."""
        if not w.get("doi"): return ("skip",)
        ref = paper_ref(w["doi"])
        if not ref or P.retraction(ref) in ("retracted", "concern"): return ("skip",)
        try: got = summary(w["doi"])
        except (P.Refused, IOError, ValueError) as e: return ("fault", {"title": "", "read": "summary", "kind": "review", "at": w.get("doi"), "kept": 0, "thrown": [], "fault": f"its summary could not be fetched ({type(e).__name__})"})
        if not got: return ("skip",)
        pp, passages = got
        return ask({"read": "summary", "ref": ref, "doi": w["doi"], "title": pp["title"], "year": pp.get("year"), "journal": pp.get("journal"), "kind": pp["kind"] if pp.get("kind") in ("review", "study", "case") else "review",
                    "people": bool(P.HUMAN.search(pp["title"] + " " + (pp.get("abstract") or ""))), "near": w.get("near"), "money": [],
                    "_abbr": abbreviations(" ".join(p["text"] for p in passages))}, passages)
    sem = threading.Semaphore(max(1, at_once))
    def begin(fn, things):
        """Sources begun now (each in a thread of its own, at_once at a time); with at_once 1 nothing is begun before it is asked for."""
        return Begun([(lambda x=x: fn(x)) for x in things], sem if threaded else None, read_until)
    late = 0
    def taken(got, what=None):
        """One source's outcome taken into the answer, in the sources' own order: True when it gave something."""
        nonlocal late
        if got[0] == "read": return keep(*got[1:])
        if got[0] == "fault": looked.append(got[1])
        elif got[0] == "late":
            late += 1; looked.append(dict({"title": "", "read": "", "kind": "", "at": ""}, **(what or {}), kept=0, thrown=[], fault="it was not read: the time this run has for reading was over"))
        elif got[0] == "error": raise got[1]
        return False
    in_time = lambda: not late and (read_until is None or time.time() < read_until)
    said_of = {"paper": lambda c: {"title": c.get("title"), "read": "full", "kind": c.get("kind"), "at": c.get("doi")}, "page": lambda o: {"title": o.get("title") or o.get("name"), "read": "page", "kind": "official", "at": o.get("address")},
               "summary": lambda w: {"title": "", "read": "summary", "kind": "review", "at": w.get("doi")}}
    bodies = amounts and bool(ASKS_BODIES.search(item["q"]))             # (lane 13) "How much ... do health bodies call ...?": the bodies' own pages answer it; a paper is read only where no page states an amount (lane 12 showed a review's retelling of a guideline beside the guideline, and spent half its reading on papers)
    cands = list(found.get("can_read") or [])
    pages = [o for o in (official or []) if not (amounts and o.get("tier", 1) != 1)]                # amounts only from a body of tier 1 or a medicine's label
    most_pages = 6 if amounts else N_OFFICIAL                                                       # (lane 11: six pages for a question about amounts; with four, the US bodies' pages on drinking were never opened)
    wave_p = (N_PAPERS + 2) if threaded else 1; wave_o = (most_pages + 1) if threaded else 1
    ahead = begin(a_page, pages[:wave_o]) if threaded and pages else None                          # the first pages are fetched and read while the papers are
    n = 0; later = []; i = 0
    while i < len(cands) and n < N_PAPERS and not bodies and in_time():
        some = cands[i:i + wave_p]; i += len(some)
        for c, got in zip(some, begin(paper, some).all()):
            if n >= N_PAPERS: later.append((c, got)); continue                                       # read ahead and not needed now: put aside
            n += taken(got, said_of["paper"](c))
    later += [(c, None) for c in cands[i:]]
    n = 0; i = 0
    while i < len(pages) and n < most_pages and len(sources) < len(tags) - 1 and in_time():
        some = pages[i:i + wave_o]; got_all = (ahead if (i == 0 and ahead is not None) else begin(a_page, some)).all(); i += len(some)
        for o, got in zip(some, got_all):
            if n >= most_pages or len(sources) >= len(tags) - 1: break
            n += taken(got, said_of["page"](o))
    for c, got in later:                                                # a third paper (and no more) where what was read is not yet enough to rest on
        if (bool(sources) if amounts else sum(weight(s) for s in sources) >= 2) or len(sources) >= len(tags) - 1 or not in_time(): break
        if taken(got if got is not None else begin(paper, [c]).all()[0], said_of["paper"](c)): break
    if in_time() and ((amounts and not (bodies and sources)) or (not amounts and (sum(weight(s) for s in sources) < 2 or not any(s["kind"] == "review" for s in sources)))):
        n = 0; ws = list(found.get("wanted") or []); i = 0; wave_s = (N_SUMMARIES + 1) if threaded else 1
        while i < len(ws) and n < N_SUMMARIES and len(sources) < len(tags) and in_time():
            some = ws[i:i + wave_s]; i += len(some)
            for w, got in zip(some, begin(a_summary, some).all()):
                if n >= N_SUMMARIES or len(sources) >= len(tags): break
                n += taken(got, said_of["summary"](w))
    # the reader that read, where the team's own could not (the record says so, as before lane 20); and every model that read, where more than one did
    first = rec["made"]["models"].get("reader")
    if first in gone and read_by:
        alt = max(read_by, key=lambda m: (read_by[m], m != first))
        if alt != first:
            rec["gates"]["reader"] = f"{base(first)} could not read on ({gone[first]}): {base(alt)} read from there"
            rec["made"]["models"].update(reader=alt, reader_first=first); models["reader"], models["reader_2"] = alt, ""
    if len(read_by) > 1: rec["made"]["read_by"] = {base(m): k for m, k in sorted(read_by.items(), key=lambda x: -x[1])}
    if late: rec["gates"]["time"] = f"{late} source(s) were not read: the time this run has for reading one question" + (f" ({read_secs:.0f} seconds)" if read_secs else "") + " was over"
    rec["made"]["read_seconds"] = round(time.time() - t_began)
    cn = counts(sources); rec["made"]["from"] = {k: cn[k] for k in ("papers", "summaries", "official")}
    rec["gates"]["read"] = (f"{sum(len(s.get('rows') or []) for s in sources)} amounts" if amounts else f"{sum(len(s['findings']) for s in sources)} findings") + f" kept from {len(sources)} sources ({cn['papers']} papers read in full, {cn['official']} official pages, {cn['summaries']} papers read in summary); {thrown} thrown away (the quote was not in the passage, or a number was not in the quote)"
    def keep_sources():
        rec["sources"] = [{k: v for k, v in s.items() if not k.startswith("_")} for s in sources]     # (what begins with _ is for the work only: the passages' text, the abbreviations a source writes out)
        cn = counts(sources); rec["made"]["from"] = {k: cn[k] for k in ("papers", "summaries", "official")}
    keep_sources()
    # (lane 19, 18 November 2026, the afternoon Europe PMC took 25 seconds a request and answered 500 for some) A source that could not be FETCHED is not a
    # source that says nothing: where the answer falls for want of sources and one or more could not be fetched, or the finder's own searches did not all
    # come back, the fault is not the answer's ("soft"): the question is tried again in the next run, not in a day, and its line says why.
    def out_of_reach():
        n = sum(1 for x in looked if x.get("fault")); lost = [str(x)[:80] for x in (found.get("problems") or [])]
        if not n and not lost: return ""
        rec["soft"] = "a source could not be fetched"
        return " (" + "; ".join(([f"{n} source(s) could not be fetched just now" + (f", {late} of them for want of time" if late else "")] if n else []) + (["the search for papers did not all come back"] if lost else [])) + ": tried again in the next run)"
    if not sources: return done("none", "no source that can be read " + ("states an amount for people" if amounts else "gave a finding") + " for this question" + out_of_reach())
    paper_name = lambda s: (f"{s['name']}: {s['title']}" if s["read"] == "page" else f"{s['title']} ({s['year']})")
    if amounts:
        every = [r for s in sources for r in s["rows"]]                 # (lane 12) how near each amount stands to the question: where there are more than the second reader is asked about, the nearest are
        if every:
            for r, x in zip(every, (enc([f"{r['what']}, for {r['who']}: {r['show']}" for r in every]) @ QV.T).max(1)): r["near"] = round(float(x), 4)
        return make_amounts(item, rec, sources, chat, models, done, keep_sources, paper_name)
    # GATE 6: enough to rest on
    said = lambda: f"{cn['reviews']} review(s) or meta-analyses, {cn['studies in people']} single studies in people, {cn['case reports']} case report(s) (which do not count), {cn['official']} official page(s), {cn['summaries']} paper(s) read in summary only"
    rec["gates"]["sources"] = said()
    labels, n_f, n_l = {}, 0, 0
    for s in sources:
        if s["design"]: labels["D" + s["tag"]] = dict(s["design"], paper=paper_name(s), title=s.get("title") or "", ref=s["ref"]["id"], year=s.get("year"), passage_text=s["_text"][s["design"]["passage"]])
        for f in s["findings"]: n_f += 1; f["id"] = f"F{n_f}"; f["second_hand"] = second_hand(s["_text"][f["passage"]], f["quote"]); labels[f["id"]] = dict(f, paper=paper_name(s), title=s.get("title") or "", ref=s["ref"]["id"], year=s.get("year"), passage_text=s["_text"][f["passage"]])
        for l in s["limits"]: n_l += 1; l["id"] = f"L{n_l}"; l["second_hand"] = second_hand(s["_text"][l["passage"]], l["quote"]); labels[l["id"]] = dict(l, paper=paper_name(s), title=s.get("title") or "", ref=s["ref"]["id"], year=s.get("year"), passage_text=s["_text"][l["passage"]])
    keep_sources()
    if sum(weight(s) for s in sources) < 2: return done("none", "not enough sources: an answer needs one review or meta-analysis read in full, or one official page, or two of: a study in people, a review read in summary, a page of a government-paid service" + out_of_reach())
    ex = ex if ex is not None else examples()
    # (lane 11) What did not stand is kept too: every draft that was written again, with what each judge said of each sentence, and
    # every line that was dropped, with who dropped it. The editor reads those as well (was it rightly refused?), and each such
    # sentence can be judged for the exam of the lane's own sentences (scripts/editor/label_auto.py): the first real batch of lane 10
    # lost a line to our own checker and an answer to the second reader, and neither text was on file to be read.
    rests = lambda p: [{"label": u, "ref": labels[u]["ref"], "where": labels[u]["where"], "quote": labels[u]["quote"], "sha": hashlib.sha256(norm(labels[u]["passage_text"]).encode("utf-8")).hexdigest()[:16]} for u in p["uses"]]
    who_said = lambda w: "our own checker" if w.startswith("our own checker") else "a further reader" if w.startswith("a further reader") else "a rule" if w.startswith("a rule") else "the second reader"
    def keep_try(n, parts, said, why):
        rec.setdefault("tries", []).append({"try": n, "why": why[:400], "parts": [{"part": p["part"], "text": p["text"], "rests_on": rests(p), "ok": p["part"] not in said, **({"by": who_said(said[p["part"]]), "said": said[p["part"]][:300]} if p["part"] in said else {})} for p in parts]})
    def keep_dropped(n, p, why):
        rec.setdefault("dropped", []).append({"try": n, "part": p["part"], "text": p["text"], "rests_on": rests(p), "by": who_said(why), "said": why[:300]})
    # 2b the plan (lane 9): where a team names a planner, the model that reasons best chooses the items before a sentence is written
    plan = None
    if models.get("planner"):
        plan = make_plan(chat, models["planner"], item["q"], sources, labels)
        rec["plan"] = plan or "the planner gave no plan that could be used: the writer chose the items itself"
        if plan and plan["unanswered"]: rec["missing"] = rec.get("missing") or plan["unanswered"]
    if last: rec["gates"]["told"] = "the writer was told what the readers said of the last draft that was not accepted: " + last[:300]
    # 3 write, 5 rules (one more try when a rule is broken), 4 check (one more try for the short answer or the But)
    fix, draft, verdicts, downs = "", None, [], []      # (downs: what each reader said when asked whether the lead plays a danger down)
    def other_writer(why):
        """(lane 19) A writer that cannot be asked, or that twice gave no answer in the form asked for, must not cost the answer: the team's other writer
        writes from there on, and the record says so. (18 November 2026: Gemma wrote 8,726 characters that were no JSON, twice, for a question the senior
        author had sent, and there was no answer.) Never a model that is this answer's reader, second reader or further reader."""
        alt = models.get("writer_2"); busy_with = {base(v.split("#")[0]) for k, v in models.items() if isinstance(v, str) and v and (k in ("reader", "checker") or re.fullmatch(r"also\d+", k))} | {base(m) for m in read_by}
        if not alt or alt == models["writer"] or base(alt) in busy_with: return False
        rec["gates"]["writer"] = (rec["gates"].get("writer", "") + f" {base(models['writer'])} {why}: {base(alt)} wrote from there.").strip()
        rec["made"]["models"].update(writer=alt, writer_first=models["writer"]); models["writer"], models["writer_2"] = alt, ""
        return True
    for attempt in range(3):
        ask = lambda: chat(models["writer"], [{"role": "system", "content": WRITER_SYS}, {"role": "user", "content": writer_prompt(item["q"], sources, ex, fix, plan, note, last)}], room_for(models["writer"], 900))
        try: reply = ask()
        except (llm.Unavailable, llm.Budget) as e:
            if "larger than Groq's free plan allows" in str(e) or not other_writer("could not be asked (" + re.sub(r"\s+", " ", str(e))[:120] + ")"): raise
            reply = ask()
        out = llm.as_json(reply)
        draft, why = draft_of(out, labels)
        if not draft:
            rec["gates"]["writer"] = (rec["gates"].get("writer", "") + f" try {attempt + 1}: {why}" + (f" (how the reply ended: {llm.LAST.get('finish')}; reasoned {llm.LAST.get('reasoned')} characters, wrote {llm.LAST.get('wrote')})" if llm.LAST else "")).strip()
            if why == "no JSON" and other_writer("gave no answer in the form asked for"): continue      # the same question, to the other writer
            if fix.startswith("the form was wrong") and why == "no JSON": rec["soft"] = "the writer's reply was not in the form asked for"; break       # the same call would fail the same way: not paid for a third time
            # (20 November 2026) a draft in the wrong form twice ("but names no item it rests on": the senior author's own question on LSD fell so, try after try):
            # the third try goes to the team's other writer, told what was wrong. No gate is touched: the form asked for is the same
            if fix.startswith("the form was wrong") and other_writer("twice wrote a draft in the wrong form (" + why + ")"): fix = "the form was wrong: " + why; continue
            fix = "the form was wrong: " + why; continue
        mended = mend_uses(draft["parts"], labels, [s["year"] for s in sources if s.get("year")], asked=sorted(numbers(item["q"])))
        if mended: rec["gates"]["mended"] = "the item that holds a number of a sentence was added to what the sentence rests on: " + "; ".join(f"{p} + {u} ({x})" for p, u, x in mended)
        bad = rules(draft["parts"], labels, [s["year"] for s in sources if s.get("year")], asked=sorted(numbers(item["q"]))) + lead(item["q"], draft["parts"]) + hedges(draft["parts"], labels) + says_more(draft["parts"], labels)   # (a year a source was published in, or a number of the question itself, may be named)
        lines_bad = {p for p, _ in bad if p.startswith("how")}
        if bad and all(p.startswith("how") for p, _ in bad) and sum(p["part"].startswith("how") for p in draft["parts"]) > len(lines_bad):
            for p in draft["parts"]:
                if p["part"] in lines_bad: keep_dropped(attempt + 1, p, "a rule: " + "; ".join(w for q, w in bad if q == p["part"]))
            draft["parts"] = [p for p in draft["parts"] if p["part"] not in lines_bad]          # (lane 4) the line goes, the answer stays
            rec["gates"]["rules"] = f"{len(lines_bad)} How-do-we-know line(s) left out for a rule (" + "; ".join(f"{p}: {w}" for p, w in bad)[:300] + ")"; bad = []
        if bad:
            rec["gates"]["rules"] = "broken at try " + str(attempt + 1) + ": " + "; ".join(f"{p}: {w}" for p, w in bad); fix = "; ".join(f"in {p}: {w}" + (" (write “people who use it”, with the drug's name where it helps, even where the source says “users”)" if "not person-first" in w else "") for p, w in bad)
            keep_try(attempt + 1, draft["parts"], {q: "a rule: " + "; ".join(w for q2, w in bad if q2 == q) for q, _ in bad}, "a rule was broken: written again"); draft = None; continue
        whole = {}; risk = stakes(item["q"], draft["parts"]); risk = risk if risk and str((stakes_how or {}).get(risk) or "") == "strict" and not NEVER_ALONE.search(item["q"]) else ""
        verdicts = check(chat, models["checker"], draft["parts"], labels, question=item["q"], whole=whole, risk=risk)
        downs = [whole.get("plays_down")] if risk else []
        # the second reader's word on the answer as a whole counts like its word on a sentence: a short answer that answers
        # another question, or a But about something else, is not accepted
        verdicts = [((v[0] and not (p["part"] == "short" and whole.get("answers") is False) and not (p["part"] == "but" and whole.get("but_fits") is False)),
                     v[1] if not v[0] else ("it does not answer the question itself" if p["part"] == "short" and whole.get("answers") is False else "it is about something else than the short answer" if p["part"] == "but" and whole.get("but_fits") is False else "") + (f" ({whole.get('why')})" if whole.get("why") and p["part"] in ("short", "but") and (whole.get("answers") is False or whole.get("but_fits") is False) else ""))
                    for p, v in zip(draft["parts"], verdicts)]
        # 4a further readers (lane 10; scripts/auto/panel.py): a team may name more second readers ("also"), each another model than the
        # writer and than the second reader. Every one of them must accept a sentence too: what one reader misses another may catch
        # (no reader we have catches enough alone: data/auto/exam). They are not asked when the short answer or the But is refused
        # already, because the answer is then written again anyway.
        gap = []                                                         # the further readers of the team that could not be asked about THIS draft
        for k in sorted(k for k in models if re.fullmatch(r"also\d+", k)):
            if any(not v[0] for p, v in zip(draft["parts"], verdicts) if p["part"] in ("short", "but")): break
            # (lane 16) a place that names several models: where the first cannot be asked (busy, or its day's free calls are used up, as
            # Gemini 4 Hydrogen's were on 17 November 2026 for the senior author's own question), the next one named for that place is asked
            more = asked = None
            for mdl in [models[k]] + [x for x in str(models.get(k + "_else") or "").split("|") if x]:
                w2 = {}
                try: more = check_marks(chat, mdl.split("#")[0], draft["parts"], labels) if mdl.endswith("#marks") else check(chat, mdl, draft["parts"], labels, whole=w2, risk=risk)
                except (llm.Unavailable, llm.Budget) as e:                 # a free service that is busy or used up must not cost the answer: what the other judges said stands, and the answer waits for this reader
                    rec.setdefault("panel", {})[mdl] = "could not be asked: " + re.sub(r"\s+", " ", str(e))[:160]; more = None; continue
                # (lane 17) a further reader whose reply held no verdict at all, asked twice, has not read the answer: on 17 November 2026 Gemini 3.8
                # Flash answered so, and an answer that every other judge had accepted was thrown away as if it had refused every sentence
                if more and all(not w[0] and w[1] == NO_VERDICT for w in more):
                    rec.setdefault("panel", {})[mdl] = "could not be asked: its reply held no verdict, twice" + (f" (how the last reply ended: {llm.LAST.get('finish')}; it reasoned {llm.LAST.get('reasoned')} characters and wrote {llm.LAST.get('wrote')}; it began: {LAST_REPLY['head']})" if llm.LAST else ""); more = None; continue
                asked = mdl
                if risk and not mdl.endswith("#marks"): downs.append(w2.get("plays_down"))
                break
            if asked is None: gap.append(base(models[k])); continue
            rec.setdefault("panel", {})[asked] = {p["part"]: [bool(w[0]), w[1]] for p, w in zip(draft["parts"], more)}
            verdicts = [((v[0] and w[0]), v[1] if not v[0] else ("" if w[0] else f"a further reader ({base(asked)}) did not accept it: {w[1] or 'it gave no reason'}")) for v, w in zip(verdicts, more)]
        if rec.get("panel"): rec["gates"]["panel"] = "further readers, each of which must accept every sentence too: " + "; ".join(f"{base(m)} accepted {sum(1 for x in vs.values() if x[0])} of {len(vs)}" if isinstance(vs, dict) else f"{base(m)} {vs}" for m, vs in rec["panel"].items())
        rec["panel_gap"] = gap
        # 4b our own checker (decision 23): a second judge that must also accept every sentence a model wrote. Its word counts like the
        # second reader's: a How line it does not find in the source's words is dropped, a short answer or a But is written again.
        if own_check is not None:
            sc = own_word(draft["parts"], labels, own_check); t = float(own_check.e.get("threshold") or 0.5)
            rec["own"] = {"model": own_check.e.get("name"), "threshold": t, "scores": sc, "scores_quotes_alone": own_word(draft["parts"], labels, own_check, passage=False)}     # (the second: measured only, it decides nothing)
            rec["gates"]["own"] = "our own checker (" + str(own_check.e.get("name")) + ", at least " + str(t) + "): " + ", ".join(f"{k} {v:.2f}" for k, v in sc.items())
            verdicts = [((v[0] and sc.get(p["part"], 1.0) >= t), v[1] if not v[0] else ("" if sc.get(p["part"], 1.0) >= t else f"our own checker does not find it in the words it rests on ({sc[p['part']]:.2f}): say only what those words say, in their own measure"))
                        for p, v in zip(draft["parts"], verdicts)]
        head_bad = [(p["part"], v[1]) for p, v in zip(draft["parts"], verdicts) if not v[0] and p["part"] in ("short", "but")]
        if head_bad and attempt < 2:
            fix = "a second reader did not accept " + "; ".join(f"{p} ({w})" for p, w in head_bad) + ". Say only what the items say, answer the question itself, and let the But be a limit of that answer."
            rec["gates"]["check"] = "not accepted at try " + str(attempt + 1) + ": " + fix
            keep_try(attempt + 1, draft["parts"], {p["part"]: v[1] or "not accepted (no reason given)" for p, v in zip(draft["parts"], verdicts) if not v[0]}, "the short answer or the But was not accepted: written again"); draft = None; continue
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
        keep_dropped(attempt + 1, draft["parts"][i], by_part["but"][1] or "not accepted (no reason given)")
        draft["parts"][i] = {"part": "but", "text": own_but(rest, nearer), "uses": [next(u for u in labels if labels[u]["ref"] == s["ref"]["id"]) for s in rest], "fixed": True}
        verdicts[i] = (True, "")
    kept = [(p, v) for p, v in zip(draft["parts"], verdicts) if v[0]]
    dropped_how = [p["part"] for p, v in zip(draft["parts"], verdicts) if not v[0] and p["part"].startswith("how")]
    for p, v in zip(draft["parts"], verdicts):
        if not v[0] and p["part"].startswith("how"): keep_dropped(attempt + 1, p, v[1] or "not accepted (no reason given)")
    if any(not v[0] for p, v in zip(draft["parts"], verdicts) if p["part"] in ("short", "but")) or sum(p["part"].startswith("how") for p, _ in kept) < 1:
        rec["gates"]["check"] = "; ".join(f"{p['part']}: {'accepted' if v[0] else 'NOT accepted: ' + v[1]}" for p, v in zip(draft["parts"], verdicts))
        ours = [v[1] for p, v in zip(draft["parts"], verdicts) if not v[0] and (v[1].startswith("our own checker") or v[1].startswith("a further reader"))]
        keep_try(attempt + 1, draft["parts"], {p["part"]: v[1] or "not accepted (no reason given)" for p, v in zip(draft["parts"], verdicts) if not v[0]}, "the last draft: no answer")
        return done("none", "the second reader did not accept the answer" if not ours else "the answer was not accepted: " + ours[0])
    rec["gates"]["check"] = f"every sentence kept was accepted by the second reader ({models['checker']})" + ("".join(f" and by {models[k]}" for k in sorted(models) if re.fullmatch(r"also\d+", k))) + (f"; {len(dropped_how)} How-do-we-know line(s) dropped" if dropped_how else "") + ("; it also found that the short answer answers the question and that the But is about that answer" if whole.get("answers") and whole.get("but_fits") else "")
    rec["gates"].setdefault("rules", "nothing against it")
    if rec["gates"]["rules"].startswith("broken"): rec["gates"]["rules"] += "; written again, then nothing against it"
    parts = [p for p, _ in kept]; used_refs = []
    for p in parts:
        p["rests_on"] = rests(p)
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
    why = stakes(item["q"], parts); strict = False
    if why:
        rec["stakes"] = why
        strict = str((stakes_how or {}).get(why) or "") == "strict" and not NEVER_ALONE.search(item["q"])
        if not strict: rec["for"] = "editor"; return done("waiting", "about " + why + ": written, and waiting for a person before it is published")
    # 7 the checked claims of the same page (lane 10): an answer that cannot be true together with a checked claim waits for a person, and
    # the disagreement is written down for the editor; the claim itself is never touched
    if claims:
        differs, same = with_checked(chat, models["checker"], enc, parts, claims(rec["drugs"]))
        # (lane 19) the editor's word on such a disagreement (data/auto/lane/agreed.json): where the editor has set this question's answer beside a checked claim and
        # found that both can hold (the second reader called them apart for the wrong reason), that claim does not stop the next answer to the question
        set_aside = [d for d in differs if d["claim"] in agreed]; differs = [d for d in differs if d["claim"] not in agreed]
        rec["with_checked"] = {"differs": differs, "same": same, **({"editor_found_both_can_hold": set_aside} if set_aside else {})}
        rec["gates"]["checked"] = (f"{len(differs)} sentence(s) cannot be true together with a checked claim of the same page (" + "; ".join(f"{d['part']} against {d['claim']}: {d['why']}" for d in differs)[:400] + ")" if differs
                                   else f"set beside the checked claims of the same page: nothing against them" + (f"; {len(same)} sentence(s) say what a checked claim says" if same else ""))
        if differs: rec["for"] = "editor"; return done("waiting", "it disagrees with a checked claim of the same page (" + ", ".join(sorted({d["claim"] for d in differs})) + "): waiting for a person; the claim is not changed")
    # (lane 19) a further reader that could not be asked: nothing is parked for it. The answer is kept, not shown, and the question is worked on again in the
    # next run, when that reader can be asked (run: "for": "again"). Until lane 18 it waited "until that reader, or the editor, has read it", and five did.
    if rec.get("panel_gap"): rec["for"] = "again"; rec["soft"] = "a further reader could not be asked"; return done("waiting", "passed every reader that could be asked, but a further reader of its team could not be (" + ", ".join(rec["panel_gap"]) + "): it is worked on again by itself when that reader can be asked")
    if strict:                                                         # the stricter bar of a question where a wrong word can hurt (see NEVER_ALONE above)
        lacks = strict_lacks(item["q"], rec, parts, sources, labels, downs)
        rec["gates"]["stakes"] = "about " + why + ": the stricter bar for such an answer: " + ("met (an official page or a review read in full under the short answer; a further reader read it; no word that plays a danger down, by code and by every reader)" if not lacks else "NOT met: " + "; ".join(lacks))
        if lacks: return done("none", "about " + why + ": written, but it does not meet the stricter bar for such an answer (" + "; ".join(lacks) + "): no answer yet")
        return done("published", "passed every gate, and the stricter bar for an answer about " + why)
    return done("published", "passed every gate")


NOT_THEM = re.compile(r"\b(?:non[- ]?|not\s+|except(?:\s+for)?\s+|excluding\s+|other\s+than\s+|apart\s+from\s+)(?:pregnan\w+|breast-?feeding|lactating)(?:\s+(?:women|adults|people|persons))?", re.I)   # (lane 13) "non-pregnant adults", "except pregnant women": the people an amount is NOT for; lane 12 left the body's own daily amount for adults to a person for the word "pregnant" in it
ASKS_BODIES = re.compile(r"\b(?:health bod(?:y|ies)|official\w*|guidelines?|guidance|recommend\w*|authorit\w+|governments?|agenc(?:y|ies)|regulators?|labels?|leaflets?|prescribing information)\b", re.I)   # (lane 13) a question about what official bodies say is answered from their own pages


def make_amounts(item, rec, sources, chat, models, done, keep_sources, paper_name):
    """An answer to a question about amounts (decision 11): rows in the sources' own words, each read by the second reader
    beside its passage, under the lines the code writes. No writer model."""
    # an amount stated for pregnancy, for children or about suicide is not the system's to publish: that row is left out
    # (a person's part); the question itself is looked at below
    n_all = sum(len(s["rows"]) for s in sources)
    persons = lambda r: any(rx.search(NOT_THEM.sub(" ", r["who"] + " " + r["what"] + " " + (r.get("clause") or r["quote"]))) for what, rx in STAKES if what in ("pregnancy or children", "suicide or self-harm"))
    rec["person_rows"] = [{"who": r["who"], "what": r["what"], "quote": r["show"], "where": r["where"], "source": s["ref"]["id"]} for s in sources for r in s["rows"] if persons(r)]      # (lane 13) kept for the person whose part they are; never shown by the system
    for s in sources: s["rows"] = [r for r in s["rows"] if not persons(r)]
    n_person = n_all - sum(len(s["rows"]) for s in sources)
    if not rec["person_rows"]: rec.pop("person_rows")
    solid = lambda s: (s["read"] == "page" and s.get("tier", 1) == 1) or (s["read"] in ("full", "summary") and s["people"] and s["kind"] in ("review", "study"))
    nearest = lambda rs, k: [r for r in rs if id(r) in {id(x) for x in sorted(rs, key=lambda r: -(r.get("near") or 0))[:k]}]      # the k nearest the question, in the order they stand
    L = lines(); rows = [(s, r) for s in sorted(sources, key=lambda s: 0 if s["read"] == "page" else 1 if s["read"] == "full" else 2) if solid(s) for r in nearest(s["rows"], 6)]   # (official pages first, then papers read in full, then summaries)
    n_solid = len(rows); rows = one_of_each(rows); n_twins = n_solid - len(rows)                       # (lane 11) the same amount for the same people twice from one source is one row; the sources that do not count no longer take room from those that do
    # (lane 12) the second reader is asked about 20 amounts at most: the ones nearest the question. With the first 18 in the order of
    # reading, five amounts about binge and heavy drinking took the room of a page's answer to the question itself. What the room
    # did not hold is kept in the record.
    if len(rows) > N_ROWS:
        # (lane 13) amounts that stand together in a source (the same passage, called the same) are asked about together or not at all:
        # lane 12 asked about the men's amount of a page and had no room for the women's
        group = lambda s, r: (s["ref"]["id"], r["passage"], r.get("what_read") or r["what"]); best = {}
        for s, r in rows: best[group(s, r)] = max(best.get(group(s, r), 0), r.get("near") or 0)
        take, n = set(), 0
        for g in sorted(best, key=lambda g: -best[g]):
            mine = [id(r) for s, r in rows if group(s, r) == g]
            if n and n + len(mine) > N_ROWS: continue
            take.update(mine); n += len(mine)
        rec["not_checked_rows"] = [{"who": r["who"], "what": r["what"], "quote": r["show"], "where": r["where"], "source": s["ref"]["id"], "near": r.get("near")} for s, r in rows if id(r) not in take]
        rows = [(s, r) for s, r in rows if id(r) in take]
    rec["gates"]["sources"] = (f"{len(rows)} amounts from {len({s['ref']['id'] for s, _ in rows})} sources that count for amounts (an official body of tier 1, a medicine's label, a study in people)"
                               + (f"; {n_person} amount(s) stated for pregnancy, for children or about suicide left out (a person's part)" if n_person else "") + (f"; {n_twins} that said the same amount for the same people again left out" if n_twins else ""))
    if not rows: return done("none", "no official page and no study in people states an amount for this question")
    labels, parts = {}, []
    for i, (s, r) in enumerate(rows, 1):
        labels[f"R{i}"] = {"paper": paper_name(s), "where": r["where"], "passage_text": s["_text"][r["passage"]], "quote": r["quote"], "ref": s["ref"]["id"]}
        parts.append({"part": f"row{i}", "text": f"This amount was {r['what']}, for {r['who']}: {r['show']}", "uses": [f"R{i}"]})
    step = 6 if models["checker"].startswith("groq:") else len(parts)      # (Groq's free plan takes 8,000 tokens a minute in one call: many amounts are checked six at a time)
    verdicts = [v for i in range(0, len(parts), step) for v in check(chat, models["checker"], parts[i:i + step], labels, each=item["q"])]
    kept = [(s, r, f"R{i}") for i, ((s, r), v) in enumerate(zip(rows, verdicts), 1) if v[0]]
    rec["gates"]["check"] = f"{len(kept)} of {len(rows)} amounts accepted by the second reader ({models['checker']})" + "".join(f"; not accepted: {v[1]}" for v in verdicts if not v[0])[:400]
    rec["gates"]["rules"] = "every quote stands in its source, holds a number with its unit and is cut to 15 words at most; no animal, no amount that harmed, no timing between uses"
    # (lane 11) the amounts the second reader did not accept are kept with its reason, for the editor: in the first real batch of lane 10
    # it refused seven and none was on file, so whether it was right could not be read
    rec["refused_rows"] = [{"who": r["who"], "what": r["what"], "quote": r["show"], "full": r["quote"][:400], "where": r["where"], "source": s["ref"]["id"], "said": (v[1] or "not accepted (no reason given)")[:300]} for (s, r), v in zip(rows, verdicts) if not v[0]]
    if not kept: return done("none", "the second reader did not accept any amount")
    used = {s["ref"]["id"] for s, _, _ in kept}; sources[:] = [s for s in sources if s["ref"]["id"] in used]; keep_sources()
    first = next((v["text"] for k, v in L["first"].items() if set(v["drugs"]) & set(item.get("drugs") or [])), "")
    guidance = bool(L.get("amounts_but_guidance")) and all(s["read"] == "page" and not s.get("label") for s in sources)     # every amount is an official body's guidance (no medicine's label, no study): the But that is true of that
    out = ([{"part": "first", "text": first, "fixed": True, "rests_on": []}] if first else []) + [{"part": "short", "text": L["amounts"], "fixed": True, "rests_on": []}, {"part": "but", "text": L["amounts_but_guidance" if guidance else "amounts_but"], "fixed": True, "rests_on": []}]
    for n, (s, r, lab) in enumerate(kept, 1):
        who = spelled(r["who"], s.get("_abbr")); who = who[0].upper() + who[1:]           # (lane 11) "TRD" written out, as the source itself writes it out
        out.append({"part": f"row{n}", "text": f"{who}; {r['what']}.", "who": who, **({"who_read": r["who"]} if who.lower() != r["who"].lower() else {}), "what": r["what"], **({"what_read": r["what_read"]} if r.get("what_read") else {}), "quote": r["show"], "source": s["ref"]["id"], "read": s["read"], "uses": [lab],
                    "rests_on": [{"label": lab, "ref": s["ref"]["id"], "where": r["where"], "quote": r["quote"], "sha": hashlib.sha256(norm(s["_text"][r["passage"]]).encode("utf-8")).hexdigest()[:16]}]})
    rec["parts"] = out
    rec["complete"] = len(used) >= 2 and not any(s["read"] == "summary" for s in sources)
    rec["missing"] = "" if rec["complete"] else ("a paper could be read in summary only" if any(s["read"] == "summary" for s in sources) else "only one source states an amount")
    why = stakes(item["q"], [{"text": NOT_THEM.sub(" ", p.get("who", "") + " " + p.get("what", ""))} for p in out if p["part"].startswith("row")])
    if why: return done("waiting", "about " + why + ": written, and waiting for a person before it is published")
    return done("published", "passed every gate (an answer about amounts: decision 11)")


def holds(hold_new, kind):
    """Is what the lane writes of this kind held for the editor's reading (data/auto/lane/policy.json, hold_new)? true: everything;
    {"answer": true, "amounts": false}: by kind (17 November 2026: the two kinds are made in two ways and are read clean at
    different times), and a kind that is not named is held."""
    return bool(hold_new.get(kind or "answer", True)) if isinstance(hold_new, dict) else bool(hold_new)


# ---------- the run ----------
def found_now(w):
    """How many sources the finders hold for a question now: the papers that can be read, and the official pages."""
    n = 0
    for f, k in ((ROOT / "data" / "auto" / "papers" / (w["id"] + ".json"), "can_read"), (FOUND_OFFICIAL / (w["id"] + ".json"), "pages")):
        try: n += len(json.load(open(f, encoding="utf-8")).get(k) or [])
        except (OSError, ValueError, TypeError): pass
    return n


def _searched(path):
    """The day a finder last searched for a question ("" where it has not)."""
    try: return str(json.load(open(path, encoding="utf-8")).get("searched_on") or "")
    except (OSError, ValueError): return ""


RESERVE = {"neurons": 2400, "groq": 50000, "google": 60}     # google: calls of the two Flash-Lite models together (team Z's second readers: five an answer)
def kept_for_sent(w):
    """(17 November 2026; the senior author, of the questions he had sent: "they are hours pending this is disappointing".) On that day
    the system's own questions had used the whole free allowance by 16:15 UTC, and a question a person sent in the evening could not be
    tried until the next day. So the end of a day's allowance is kept for the questions people send: once Cloudflare has fewer than
    RESERVE["neurons"] left AND Groq's strongest model fewer than RESERVE["groq"] tokens (room for three or four answers), the system's
    own questions wait for the next day, and a sent question is still worked on at once. True: this question waits."""
    if w.get("from") == "a question visitors sent" or w.get("trial"): return False
    try:
        low = llm.left() < RESERVE["neurons"] and llm.groq_left("openai/gpt-oss-120b") < RESERVE["groq"]
        # (19 November 2026, team Z) where Google's models still have room the lane writes on with them, and the end of THEIR day is kept for the
        # questions people send: the two Flash-Lite models, which read second in team Z, together fewer than RESERVE["google"] calls
        if low and llm.has("gemini:gemini-3.5-flash-lite"):
            low = llm.calls_left("gemini:gemini-3.5-flash-lite") + llm.calls_left("gemini:gemini-3.1-flash-lite") < RESERVE["google"]
        return low
    except Exception: return False


SOFT_FETCH_A_DAY, SOFT_FETCH_TRIES = 3, 6               # a source that could not be fetched: three tries a day; from the seventh try in all it is no fault of the moment, and the question waits as any other without an answer
SOFT_A_DAY, HARD_A_DAY, HARD_SENT_A_DAY = 6, 2, 3       # tries of one question in one day: after a fault that was not the answer's; after an answer that did not pass (the system's own question; one a person sent)


ROOM_FILE = ROOT / "data" / "auto" / "lane" / "room.json"


def room_note(room):
    """(19 November 2026; his words, 20:22: "still the same ... problem") what the lane itself found when it chose a team: room, or none until the next day
    (00:00 UTC, when Cloudflare's and Groq's days turn). The page of a reader who waits reads it (scripts/auto/live.py): it never says that an answer is
    being written while no team can write one. Only a real run writes it; a check or a trial does not."""
    if os.environ.get("LANE_NO_ROOM_NOTE"): return
    now = datetime.datetime.now(datetime.timezone.utc)
    try:
        was = json.load(open(ROOM_FILE, encoding="utf-8")) if ROOM_FILE.exists() else {}
        out = {"_note": "Written by scripts/auto/lane.py when it chose a team for an answer: room (true) or no team with room until 'until' (false).", "room": bool(room), "at": now.isoformat(timespec="seconds"),
               "until": None if room else (datetime.datetime.combine(now.date() + datetime.timedelta(days=1), datetime.time(0, 0), datetime.timezone.utc)).isoformat(timespec="seconds")}
        if was.get("room") == out["room"] and was.get("until") == out["until"]: return          # (nothing new: the file is not written again)
        ROOM_FILE.parent.mkdir(parents=True, exist_ok=True); json.dump(out, open(ROOM_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    except (OSError, ValueError): pass


def wait_days(tries):
    """(lane 19) After a day's tries gave no answer: how many days until the next. Every day at first; then further apart, so that a question the sources
    cannot answer yet does not take the free allowance from the questions that can be answered (new sources bring it back at once: turn 2)."""
    return 1 if tries <= 4 else 2 if tries <= 8 else 4 if tries <= 14 else 7


def turn_of(w, done):
    """When a question's turn comes (the smaller, the sooner), or None when there is nothing to do for it now. done: the lane's state.
      0    never tried
      0.5  (lane 19) the last try was lost to a fault that was not the answer's (the writer's malformed reply, a fault of the network or of the lane, a
           further reader that could not be asked): again in the next run, up to SOFT_A_DAY tries a day
      1    written by an older lane and not shown: written again by the lane as it is
      2    the second look: not complete, or no answer, and the finders have found something since
      2.5  (lane 19) no answer passed today: once or twice more the same day, by another team of models (HARD_A_DAY; HARD_SENT_A_DAY for a question a person sent)
      3    no answer, and the days of wait_days have passed since the last try
      4    (lane 19) shown, and written by an older lane: its second look comes last (the answer that is shown stays shown if the second look does not pass)
    An answer that waits for an editor (an amount; suicide; what to do in an emergency; one that disagrees with a checked claim) is not tried again."""
    s = done.get(w["id"]) or {}
    if not s: return 0
    st, last = s.get("status"), str(s.get("last") or "")
    n = int(s.get("n") or 1) if last == TODAY else 0                      # tries today (a try noted before lane 19 has no count: one)
    older = int(s.get("lane") or 1) < LANE
    if st == "published" and older: return 4
    if st == "waiting" and s.get("for") == "editor":                    # an editor reads it; a newer lane does not write it again by itself,
        # (20 November 2026) unless the editor has read it and held it (data/auto/held.json): then it is written again by itself, with what the editor found (held_say).
        # Until now such a hold stopped nothing and started nothing: five answers the editor held on 18 November had waited two days, never written again.
        try: rec = json.load(open(OUT / ("au_" + str(w["id"]) + ".json"), encoding="utf-8"))
        except (OSError, ValueError): rec = None
        return 1 if rec and is_held(rec) else None
    if older: return 1
    if st == "waiting" and s.get("for") != "again": return None
    newer = max([_searched(ROOT / "data" / "auto" / "papers" / (w["id"] + ".json")), _searched(FOUND_OFFICIAL / (w["id"] + ".json"))])
    if st == "published": return 2 if s.get("complete") is False and newer > last else None
    if s.get("soft") or s.get("for") == "again":
        fetch = s.get("soft") == "a source could not be fetched"           # (the index of papers slow or failing: an afternoon of it on 18 November 2026; one paper's full text may also fail for good)
        if not (fetch and int(s.get("tries") or 1) > SOFT_FETCH_TRIES): return 0.5 if n < (SOFT_FETCH_A_DAY if fetch else SOFT_A_DAY) else None
    if newer > last: return 2
    # (17 November 2026, 20:10) the finders may find more on the very day the lane tried: kanna was tried at 17:36 UTC with nothing to read and
    # searched by its own name at 17:55 (12 papers that can be read). A day is too coarse: the lane notes how many sources it had ("had"), and a
    # question with no answer is looked at again as soon as the finders hold more. (A try noted before this rule: only where it had nothing to read.)
    found, had = found_now(w), s.get("had")
    if (had is None and "no source that can be read" in str(s.get("why") or "") and found > 0) or (had is not None and found > int(had)): return 2
    nothing = "no source that can be read" in str(s.get("why") or "") or "not enough sources" in str(s.get("why") or "")      # nothing to write from: another try the same day would find the same (new sources bring it back at once, above)
    if n and not nothing and n < (HARD_SENT_A_DAY if w.get("from") == "a question visitors sent" else HARD_A_DAY): return 2.5
    if last <= (datetime.date.today() - datetime.timedelta(days=wait_days(int(s.get("tries") or 1)))).isoformat(): return 3
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


NEED = {"reader": (600, 22000), "writer": (350, 16000), "checker": (500, 16000), "planner": (250, 7000), "also": (350, 9000), "also#marks": (900, 24000)}     # what one answer may take of a day's free allowance, by role: (Cloudflare neurons, Groq tokens)


def base(model): return re.sub(r":free$", "", re.sub(r"^(?:groq:|@cf/|mistral:|gemini:|openrouter:|sambanova:|local:|claude:)", "", model or "")).split("/")[-1]       # the model itself, whichever service runs it
CALLS = {"reader": 6, "writer": 3, "checker": 5, "planner": 1, "also": 3, "also#marks": 15}       # for a service that counts calls (llm.SERVICES): how many one answer may need of each role


def reading_pool(file=None):
    """(19 November 2026) The models that read sources side by side with a team's own reader: "readers" of data/auto/lane/models.json
    ([{"model", "secs": how long one reading call takes it}]), each only where its service has a key on this machine and room left today. A reader only
    copies, and every quote it copies is checked by code against the passage: which model reads changes how much is found, never what is true."""
    try: mf = json.load(open(file or MODELS_FILE, encoding="utf-8"))
    except (OSError, ValueError): mf = {}
    out = []
    for r in mf.get("readers") or []:
        m = r.get("model") if isinstance(r, dict) else None
        if not isinstance(m, str) or not m or not llm.has(m): continue
        try:
            if m.startswith("groq:"): ok = llm.groq_left(m[5:]) >= 2 * NEED["reader"][1] / CALLS["reader"]
            elif llm.service_of(m)[0]: ok = llm.calls_left(m) >= 4
            else: ok = llm.left() >= ROOM / 2
        except Exception: ok = False
        if ok: out.append({"model": m, "secs": float(r.get("secs") or 10)})
    return out


def team(file=None, only=None, avoid=()):
    """The models for the next answer: the first team of data/auto/lane/models.json whose services have a key on this
    machine and room left today (two free services, each with its own day's allowance: Cloudflare Workers AI in neurons,
    Groq in tokens for each model). A team names a reader, a writer and a second reader; "reader_else" and "checker_else"
    are used where the first choice has no key or no room. Never the same model twice in a row: the writer is not the
    reader's model and the second reader is not the writer's, on whichever service. None when no team has room."""
    try: mf = json.load(open(file or MODELS_FILE, encoding="utf-8"))
    except (OSError, ValueError): mf = {}
    teams = mf.get("teams") or [{k: mf.get(k) or MODELS[k] for k in MODELS}]
    teams = [t for t in teams if t.get("name") not in avoid] + [t for t in teams if t.get("name") in avoid]      # (lane 19) a question that got no answer today is tried by another team first: other models, another draft
    for t in teams:
        if only and t.get("name") != only: continue                        # (a request may name its team: a new reader is tried on a question or two before it stands in the order)
        planners = [p for p in dict.fromkeys([t.get("planner"), t.get("planner_else")]) if isinstance(p, str) and p and base(p) != base(t.get("writer") or "")] or [None]
        for reader in dict.fromkeys([t.get("reader"), t.get("reader_else")]):
            for checker in dict.fromkeys([t.get("checker"), t.get("checker_else")]):
                for planner in planners:                                   # (lane 10: "planner_else", as for the reader and the second reader: the plan is made where there is room)
                    m = {"reader": reader, "writer": t.get("writer"), "checker": checker}
                    if planner: m["planner"] = planner
                    also, lacking, rest = [], False, {}                   # (lane 10) further second readers: a team that names them is that team only with all of them
                    for a in (t.get("also") or []) if isinstance(t.get("also"), list) else []:
                        if isinstance(a, list):                               # one place, several models: the first that has a key and room today (the strong free models have 20 calls a day each)
                            # (19 November 2026) a model with a handful of free calls a day (Google's strong readers: 20) is asked once for an answer, seldom twice: it is
                            # taken while it has ONE call left, not three. On 18 November two of them stood unused at 16 of 18 calls while answers waited for a strong reader
                            few = lambda x: bool(llm.service_of(x)[0]) and 0 < llm.limits_of(x)["calls"] <= 20
                            # (19 November 2026, team Z) never the writer's or the second reader's own model: the next one named for the place is taken instead
                            pick = next((x for x in a if isinstance(x, str) and x and llm.has(x.split("#")[0]) and x not in also and base(x.split("#")[0]) not in (base(t.get("writer") or ""), base(checker or "")) and (llm.calls_fit({x.split("#")[0]: 1 if few(x.split("#")[0]) else CALLS["also#marks" if x.endswith("#marks") else "also"]}) if llm.service_of(x)[0] else True)), None)
                            if pick: also.append(pick); rest[len(also)] = [x for x in a[a.index(pick) + 1:] if isinstance(x, str) and x and llm.has(x.split("#")[0]) and base(x.split("#")[0]) not in (base(t.get("writer") or ""), base(checker or ""))]   # (lane 16) the others named for this place, asked in turn where the first cannot be
                            else: lacking = True
                        elif isinstance(a, str) and a: also.append(a)
                    if lacking: continue
                    for n, a in enumerate(also, 1): m[f"also{n}"] = a
                    if not all(isinstance(v, str) and v and llm.has(v.split("#")[0]) for v in m.values()): continue
                    if base(m["checker"]) == base(m["writer"]) or base(m["reader"]) == base(m["writer"]) or base(m["reader"]) == base(m["checker"]): continue
                    if base(m["writer"]) in {base(a.split("#")[0]) for a in also} or base(m["checker"]) in {base(a.split("#")[0]) for a in also if not a.endswith("#marks")} or len(set(also)) < len(also): continue   # a further reader is another model than the writer; one asked the same way as the second reader is another model than it, too
                    need, calls = {}, {}
                    for role, v in m.items():
                        kind = ("also#marks" if v.endswith("#marks") else "also") if role.startswith("also") else role; v = v.split("#")[0]
                        svc = llm.service_of(v)[0]
                        if svc: calls[v] = calls.get(v, 0) + (1 if kind == "also" and 0 < llm.limits_of(v)["calls"] <= 20 else CALLS[kind])      # (a strong reader with 20 calls a day: one call an answer, see above)
                        else: need[v] = need.get(v, 0) + NEED[kind][1 if v.startswith("groq:") else 0]
                    if sum(n for v, n in need.items() if not v.startswith("groq:")) > llm.left(): continue
                    if any(v.startswith("groq:") and n > llm.groq_left(v[5:]) for v, n in need.items()): continue
                    if not llm.calls_fit(calls): continue                   # (each model of a call-counted service has its own free allowance: llm.limits_of)
                    other = next((r for r in (t.get("reader"), t.get("reader_else")) if isinstance(r, str) and r and r != m["reader"] and llm.has(r) and base(r) not in (base(m["writer"]), base(m["checker"]))), None)
                    # (lane 19) the writer's stand-in: the team's "writer_else", else the first of the writers we know that is another model than every other of this answer
                    taken = {base(v.split("#")[0]) for v in m.values()}
                    w2 = next((x for x in [t.get("writer_else"), "groq:qwen/qwen3.8-27b", "@cf/meta/llama-3.3-70b-instruct-fp8-fast"] if isinstance(x, str) and x and llm.has(x) and base(x) not in taken), None)
                    return dict(m, team=t.get("name") or "", **({"reader_2": other} if other else {}), **({"writer_2": w2} if w2 else {}), **{f"also{n}_else": "|".join(r) for n, r in rest.items() if r})
    return None


def fitting(chat):
    """chat, with a call that Groq's free plan cannot take in one minute asked again with less room for the answer (never
    less than 700 tokens): the prompt cannot be cut here, but a model seldom needs all the room it is given."""
    def ask(model, messages, room=700):
        try: return chat(model, messages, room)
        except llm.Unavailable as e:
            m = re.search(r"\((\d+) of (\d+) tokens\)", str(e))
            if not (m and model.startswith("groq:")): raise
            less = room - (int(m.group(1)) - int(m.group(2))) - 60
            if less < 700: raise
            return chat(model, messages, less)
    return ask


def trial_items(raw):
    """The trial questions of a request, as items the lane can work on: [{"id": "t_...", "q", "ways", "drugs"}]. A trial question is
    one the site's list does not hold: the editor writes it to try the lane on something it has never seen. What the lane makes of it
    is written to data/auto/trial/ and is never shown, never placed on a page, never counted as an answer. Anything else in the
    request's list is left out."""
    out = []
    for x in raw if isinstance(raw, list) else []:
        if not isinstance(x, dict) or not re.fullmatch(r"t_[a-z0-9_]{1,40}", str(x.get("id") or "")) or not isinstance(x.get("q"), str) or not 10 <= len(x["q"]) <= 200: continue
        drugs = [d for d in x.get("drugs") or [] if isinstance(d, str) and re.fullmatch(r"[a-z0-9][a-z0-9-]{1,40}", d)][:4]
        out.append({"id": x["id"], "q": re.sub(r"\s+", " ", x["q"]).strip(), "ways": [re.sub(r"\s+", " ", w).strip() for w in x.get("ways") or [] if isinstance(w, str) and 3 <= len(w) <= 120][:6], "drugs": drugs, "trial": True})
    return out[:12]


def held_say(aid, lane=None):
    """(lane 19) What the editor found in an answer it holds (data/auto/held.json, "say"), for the writer of the next one: "" where there is none. The editor's
    reading goes back into the lane by itself: until lane 18 a held answer waited "to be written again" for a person to ask for it."""
    try: held = json.load(open(ROOT / "data" / "auto" / "held.json", encoding="utf-8")).get("held") or []
    except (OSError, ValueError): return ""
    return next((re.sub(r"\s+", " ", str(h.get("say") or ""))[:600] for h in held if isinstance(h, dict) and h.get("id") == aid and h.get("say")), "")


def is_held(rec, held=None):
    """Does the editor hold THIS version of an answer (data/auto/held.json)? By the run that wrote it where the hold names one ("run": site 2.21.1), else by its
    lane (a hold of lane N holds every version written by lane N or older). The same test as site/build.js makes before it shows an answer."""
    if held is None:
        try: held = json.load(open(ROOT / "data" / "auto" / "held.json", encoding="utf-8")).get("held") or []
        except (OSError, ValueError): return False
    for h in held:
        if isinstance(h, dict) and h.get("id") == (rec or {}).get("id"):
            if h.get("run") is not None: return str(((rec or {}).get("made") or {}).get("run") or "") == str(h["run"])
            return h.get("lane") is None or int((rec or {}).get("lane") or 1) <= int(h["lane"])
    return False


def last_refusal(before):
    """(lane 19, 18 November 2026) What the readers said of the last draft of an answer that was not accepted, for the writer of the next one: "" where there is
    none. A question that is tried again by itself was written afresh each time by a writer that knew nothing of why the last draft fell, and the same
    sentence fell again (the senior author's own "is sex better with weed": three drafts that day said more than the 'potential' their source spoke of, each
    refused by a reader, each written by a writer that had not been told). Only of an answer of THIS lane that ended with none, and only what a reader or our own
    checker said of its short answer or its But (a rule's word is in the code and is told in the same run). The readers' words are data, cut short; the writer
    stays bound by every rule and is read by every reader as before: no gate is touched."""
    if not isinstance(before, dict) or before.get("status") != "none" or int(before.get("lane") or 0) != LANE: return ""
    said = []
    for x in (before.get("tries") or [])[-1:]:
        for q in x.get("parts") or []:
            if q.get("ok") is False and q.get("said") and q.get("part") in ("short", "but") and q.get("by") in ("the second reader", "a further reader", "our own checker"):
                said.append(f'the {"short answer" if q["part"] == "short" else "But"} “{re.sub(r"[ \t\n]+", " ", str(q.get("text") or ""))[:220]}”: {re.sub(r"[ \t\n]+", " ", str(q["said"]))[:260]}')
    return " | ".join(said)[:900]


def shown_from():
    """The oldest lane whose answers the site shows (data/auto/lane/policy.json, show_from_lane)."""
    try: return int(json.load(open(ROOT / "data" / "auto" / "lane" / "policy.json", encoding="utf-8")).get("show_from_lane") or 1)
    except (OSError, ValueError, TypeError): return 1


def agreed_claims(wid):
    """(lane 19) The checked claims the editor has found an answer to this question can stand beside (data/auto/lane/agreed.json: {"pairs": [{"question", "claim", "on", "why"}]})."""
    try: pairs = json.load(open(ROOT / "data" / "auto" / "lane" / "agreed.json", encoding="utf-8")).get("pairs") or []
    except (OSError, ValueError): return ()
    return tuple(str(x.get("claim")) for x in pairs if isinstance(x, dict) and x.get("question") == wid and x.get("claim"))


def stakes_policy():
    """What each kind of question where a wrong word can hurt does (data/auto/lane/policy.json, "stakes"): {kind: "strict" | "person"}."""
    try: p = json.load(open(ROOT / "data" / "auto" / "lane" / "policy.json", encoding="utf-8")).get("stakes")
    except (OSError, ValueError): p = None
    return {k: v for k, v in p.items() if v in ("strict", "person")} if isinstance(p, dict) else {}


SOFT_FAULT = ("HTTPError", "URLError", "TimeoutError", "ConnectionError", "ConnectionResetError", "RemoteDisconnected", "IncompleteRead", "SSLError", "gaierror", "timeout")   # a fault of the network: the next try may not meet it


def runs_waiting(run=None):
    """How many runs of the work (auto.yml) wait behind the one that is working: GitHub lets one run of it work and one wait. (18 November 2026, 20:50 Athens: the
    first question that started a run by itself, four seconds after it was typed, then waited behind the clock's run, which was 36 minutes into the system's own
    questions.) A run that works on the system's OWN questions gives way to a run that waits: that one was started by a new question, or reads one first. Asked
    of GitHub with the run's own token (gh, which the runners have); 0 where it cannot be asked: a run then works on as before."""
    import subprocess
    try:
        r = (run or subprocess.run)(["gh", "run", "list", "--workflow", "auto.yml", "--limit", "12", "--json", "status"], capture_output=True, text=True, timeout=30)
        if r.returncode != 0: return 0
        return sum(1 for x in json.loads(r.stdout or "[]") if isinstance(x, dict) and x.get("status") in ("queued", "pending", "waiting", "requested"))
    except Exception: return 0


def next_up(limit=3):
    """(19 November 2026) The questions people sent that the next pass of a run works on, in the order run() takes them (for scripts/auto/live.py: the page
    of a person who waits says that their question is being written now)."""
    items = P.listed(); st = load_state(); rep = ROOT / "data" / "auto" / "report.json"
    asked = {w["id"]: w.get("asked", 0) + w.get("sent_too", 0) for w in (json.load(open(rep, encoding="utf-8")).get("wanted") or [])} if rep.exists() else {}
    order = [w for w in sorted(items, key=lambda w: (-(asked.get(w["id"], 0) + int(w.get("asked") or 0)), w["id"])) if w.get("from") == "a question visitors sent" and turn_of(w, st["items"]) is not None]
    order.sort(key=lambda w: turn_of(w, st["items"]))
    return [w["id"] for w in order[:limit]]


def run(ids=None, limit=3, again=False, chat=None, enc=None, only_team=None, trial=None, minutes=None, only_sent=False, give_way=None):
    models = dict(MODELS); real = chat is None; began = datetime.datetime.now()
    chat = fitting(chat or llm.chat)
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
    # (a stable sort: within one turn, the most asked first. 17 November 2026: a question a person sent comes before every question of the system's
    # own, whatever its turn: kanna, sent and waiting for its second look, would have stood behind 46 of the system's own that were never tried)
    if not ids and not again: order.sort(key=lambda w: (0 if w.get("from") == "a question visitors sent" else 1, turn(w)))
    if only_sent: order = [w for w in order if w.get("from") == "a question visitors sent"]      # (lane 19) the first pass of a run: the questions people sent, alone, so that what is written for them is published before the system's own are begun
    if trial: order = list(trial); limit = max(limit, len(order))                  # (trial questions only: nothing of the site's list is worked on in such a run)
    enc = enc or P.General(); import build_index as bi; names = bi.names_table(); made = []; out_of_room = 0; begun = 0
    pool = reading_pool() if real else None
    if pool: print("lane: sources are read at once, by " + ", ".join(base(m["model"]) for m in pool) + " beside the team's own reader")
    OUT.mkdir(parents=True, exist_ok=True); STATE.parent.mkdir(parents=True, exist_ok=True)
    # our own checker (decision 23), where one is in use (data/auto/own/models.json): the file that sat the exam, by its SHA-256. If it
    # is in use and cannot be run here, nothing is published by itself in this run: an answer it did not judge waits for the editor.
    own_chk, own_err = None, ""
    if real:
        try:
            import own
            own_chk = own.Check() if own.in_use("check") else None
        except Exception as e: own_err = str(e)[:200] or type(e).__name__
        if own_chk: print(f"lane: our own checker is {own_chk.e.get('name')} (from {own_chk.e.get('from')}), at least {own_chk.e.get('threshold')}")
        if own_err: print("lane: our own checker is in use and could NOT be run here: every answer of this run waits for the editor:", own_err)
    if real and not trial and not ids: order = [w for w in order if not kept_for_sent(w)] or order[:0]      # (what is left of the day is for the questions people send)
    def note_try(w, status, why, **more):
        """One try in the lane's state: when, how many today, by which teams, and whether the fault was the answer's ("soft": it was not)."""
        was = st["items"].get(w["id"]) or {}; same_day = was.get("last") == TODAY
        st["items"][w["id"]] = dict({"status": status, "why": why, "last": TODAY, "at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "lane": LANE, "kind": "", "complete": False,
                                     "tries": int(was.get("tries") or 0) + 1, "n": (int(was.get("n") or 1) if same_day else 0) + 1, "teams": ((was.get("teams") or []) if same_day else []) + ([models.get("team")] if models.get("team") else []), "had": found_now(w)}, **more)
        json.dump(st, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    cut = 0
    for w in order[:limit]:
        gone_by = (datetime.datetime.now() - began).total_seconds()
        if minutes and begun and 60 * minutes - gone_by < BEGIN_WITH: print(f"lane: {minutes} minutes are nearly over: the rest waits for the next run"); break      # (lane 19) a run is short, so that what it wrote is published soon
        # the clock for this question: what one question may take, and never much past the end of the pass
        if real: llm.STOP_AT = P.STOP_AT = time.time() + (min(QUESTION_SECONDS, max(BEGIN_WITH, 60 * minutes - gone_by + 30)) if minutes else QUESTION_SECONDS)
        if real: llm.GIVE_WAY = give_way if (give_way and w.get("from") != "a question visitors sent") else None; llm._gave[:] = [time.time(), False]      # one of the system's own gives way in the middle too (asked every 25 seconds)
        begun += 1
        if give_way and made and give_way(): print("lane: a run is waiting behind this one (a new question came): the rest is left to it"); break      # (between two of the system's own questions; never in the pass for the questions people sent)
        if real:
            was = st["items"].get(w["id"]) or {}
            models = team(only=only_team, avoid=tuple(was.get("teams") or []) if was.get("last") == TODAY else ())
            if not models: print(f"lane: no team of models has room left today (Cloudflare: {llm.left():.0f} neurons left): it goes on tomorrow"); room_note(False); break
            room_note(True)
            print(f"lane: {models.get('team') or 'the models'}: {models['reader']} reads, {models['writer']} writes, {models['checker']} is the second reader")   # (an answer begun and not finished is lost, and its neurons with it: on 15 November 563 went that way)
        pf = ROOT / "data" / "auto" / "papers" / (w["id"] + ".json"); of = FOUND_OFFICIAL / (w["id"] + ".json"); af = OUT / ("au_" + w["id"] + ".json")
        if w.get("trial"): pf = TRIAL / "papers" / (w["id"] + ".json"); of = TRIAL / "official" / (w["id"] + ".json"); af = TRIAL / "answers" / ("au_" + w["id"] + ".json")
        try:
            found = json.load(open(pf, encoding="utf-8")) if pf.exists() and not again else P.find(w, names, enc)
            if not pf.exists() or again: pf.parent.mkdir(parents=True, exist_ok=True); json.dump(found, open(pf, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            if w.get("trial") and not of.exists():                             # the official pages for a trial question are looked for here (for a listed question official.py has done it before)
                try:
                    import official as O; res = O.find(w, names, enc); of.parent.mkdir(parents=True, exist_ok=True); json.dump(res, open(of, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
                except Exception as e: print(f"lane: {w['id']}: the official pages could not be looked for ({type(e).__name__}: {str(e)[:120]})")
            try: official = json.load(open(of, encoding="utf-8"))["pages"]
            except (OSError, ValueError, KeyError): official = []               # (official.py has not searched for this question yet, or found nothing)
            try: before = json.load(open(af, encoding="utf-8"))
            except (OSError, ValueError): before = None
            rec = make(w, found, chat, enc, models, official=official, names=names, before=before, claims=checked_claims, own_check=own_chk, stakes_how=stakes_policy() if real else None, note=held_say("au_" + w["id"]) if real else "", agreed=agreed_claims(w["id"]) if real else (), last=last_refusal(before) if real else "",
                       pool=pool, at_once=AT_ONCE if real else 1, read_secs=(READ_SECONDS_SENT if w.get("from") == "a question visitors sent" else READ_SECONDS) if real else None)
            if own_err and rec.get("status") == "published": rec["status"] = "waiting"; rec["for"] = "again"; rec["soft"] = "our own checker could not be run"; rec["why"] = "our own checker is in use and could not be run in this run (" + own_err + "): worked on again by itself in the next run"
            cut = 0
        except llm.Budget as e:
            # an allowance ran out in the middle of an answer (our count was too low, or Groq said so itself and llm wrote that down): the next
            # question is begun with whichever team still has room; the question that was cut short keeps its turn for the next run
            out_of_room += 1; print("lane: an allowance ran out in the middle of an answer:", e)
            if out_of_room >= 2: print("lane: stopped for today"); break
            continue
        except llm.Late as e:
            # (19 November 2026) the question's time was over in the middle of the answer: it is put down for this run and tried again in the next (a fault
            # of the moment, not of the answer); the run goes on with the next question, which has its own time
            way = "a run is waiting behind this one" in str(e)
            print(f"lane: {w['id']}: " + ("left for the next run:" if way else "the time one question has was over:"), e)
            if not w.get("trial"): note_try(w, "none", ("a new question came while this one was being worked on: left for the next run" if way else "the time a run has for one question was over (" + re.sub(r"\s+", " ", str(e))[:140] + "): tried again in the next run"), soft="a new question came" if way else "the time for one question was over")
            if way: break
            continue
        except llm.Unavailable as e:
            print("lane: the models cannot be used now:", e)
            if "larger than Groq's free plan allows" in str(e): continue        # (this question's call was too large; the next question's may not be)
            # (lane 19) a model that could not be reached in the middle of an answer: the question is tried again in the next run (not in a day or two), by
            # another team first, and this run goes on with the next question; two such in a row, and the run stops
            if not w.get("trial"): note_try(w, "none", "a model could not be reached in the middle of the answer (" + re.sub(r"\s+", " ", str(e))[:140] + ")", soft="a model could not be reached")
            cut += 1
            if cut >= 2: break
            continue
        except P.Refused as e: print("lane: a source said no:", e); break
        except Exception as e:                                           # a fault of the lane itself on this question: written down, and the question is not tried again by this lane (it would fail the same way and spend the day's allowance)
            import traceback
            print(f"lane: {w['id']}: the lane itself failed ({type(e).__name__}: {str(e)[:200]})"); print("".join(traceback.format_exc().splitlines(True)[-6:]))
            # (lane 19) a fault of the network is not the question's: it is tried again in the next run. On 17 and 18 November 2026 three questions were left
            # for a day or more as "the lane itself failed on it (HTTPError)".
            if not w.get("trial"): note_try(w, "none", f"the lane itself failed on it ({type(e).__name__})", **({"soft": "a fault of the network"} if type(e).__name__ in SOFT_FAULT else {}))
            continue
        if w.get("trial"):                                              # a trial: what the lane would have done is kept beside the record, and the record itself can never be shown
            rec["trial"] = {"would_be": rec["status"], "why": rec.get("why")}
            if rec["status"] == "published": rec["status"] = "waiting"; rec["held"] = "a trial question"; rec["why"] = (rec.get("why") or "") + "; a trial question: never shown"
            af.parent.mkdir(parents=True, exist_ok=True); json.dump(rec, open(af, "w", encoding="utf-8"), ensure_ascii=False, indent=1); made.append(rec)
            f = rec["made"].get("from") or {}
            print(f"lane: TRIAL {w['id']} {w['q'][:56]!r}: would be {rec['trial']['would_be']} ({rec['trial']['why']}); {f.get('papers', 0)} papers, {f.get('official', 0)} official pages, {f.get('summaries', 0)} summaries; {rec['made'].get('neurons', 0)} neurons")
            continue
        try: hold = holds(json.load(open(ROOT / "data" / "auto" / "lane" / "policy.json", encoding="utf-8")).get("hold_new"), rec.get("kind"))
        except (OSError, ValueError): hold = False
        if hold and rec.get("status") == "published":                  # the editor reads the first answers of a new version of the lane before they are shown (data/auto/lane/policy.json, hold_new; scripts/editor/release_auto.py lets them out)
            rec["status"] = "waiting"; rec["held"] = "the editor's first reading of lane " + str(LANE); rec["why"] = (rec.get("why") or "") + "; held until the editor has read it (the first answers of this version of the lane)"
        try:                                                           # where the answer belongs on the site (scripts/auto/place.py): a drug's page, a page to start, or one of the general pages
            import place; pl = place.Placer(names).place(w["q"], w.get("ways") or []); rec["place"] = {k: pl[k] for k in ("home", "also", "cls", "why")}
            if w.get("page") and rec["place"]["home"] != "new:" + w["page"]:        # a question the system asked for a page it should start (scripts/auto/grow.py) belongs on that page, whatever its words name first
                rec["place"] = dict(rec["place"], home="new:" + w["page"], also=[h for h in dict.fromkeys([pl["home"]] + list(pl["also"])) if h and h != "new:" + w["page"]], why="asked by the system for the page it should start: " + w["page"])
        except Exception as e: rec["place"] = {"home": None, "why": "the place could not be worked out: " + str(e)[:120]}
        if rec["status"] == "waiting" and not rec.get("for"): rec["for"] = "editor"      # (held for the editor's first reading of a kind: hold_new)
        # (lane 19) the second look at an answer that is shown: if it does not pass, the answer that is shown stays, with a note of what the second look made of
        # it (until lane 18 the answer was replaced by "no answer", and a reader lost what they had)
        # (not where the editor holds the version that is "shown": that one is not shown, and a draft that did not pass does not bring it back)
        if before and before.get("status") == "published" and not is_held(before) and rec["status"] != "published" and int(before.get("lane") or 1) >= shown_from():
            before["second_look"] = {"on": TODAY, "lane": LANE, "status": rec["status"], "why": rec["why"], "short": next((p.get("text") for p in rec.get("parts") or [] if p.get("part") == "short"), "")}
            json.dump(before, open(OUT / (rec["id"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            note_try(w, "published", (before.get("why") or "") + f"; a second look by lane {LANE} did not pass ({rec['why'][:160]}): the answer of lane {before.get('lane')} stays", kind=before.get("kind") or "", complete=before.get("complete"))
            made.append(rec); print(f"lane: {w['id']} {w['q'][:56]!r}: the second look did not pass ({rec['why'][:120]}); the answer that is shown stays"); continue
        json.dump(rec, open(OUT / (rec["id"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        note_try(w, rec["status"], rec["why"], kind=rec["kind"], complete=rec["complete"], **({"soft": rec["soft"]} if rec.get("soft") else {}), **({"for": rec["for"]} if rec.get("for") else {}))
        made.append(rec)
        f = rec["made"].get("from") or {}
        print(f"lane: {w['id']} {w['q'][:56]!r}: {rec['status']} ({rec['why']}); {f.get('papers', 0)} papers, {f.get('official', 0)} official pages, {f.get('summaries', 0)} summaries; {rec['made'].get('neurons', 0)} neurons; {rec['made'].get('seconds', 0)} seconds, {rec['made'].get('read_seconds', 0)} of them reading" + (f" ({', '.join(f'{m} {k}' for m, k in rec['made']['read_by'].items())})" if rec["made"].get("read_by") else ""))
    llm.STOP_AT = P.STOP_AT = None; llm.GIVE_WAY = None
    json.dump({"_note": "Papers the machine lane wants and cannot read (their full text is not open), with the questions they are wanted for. References from Crossref, made by scripts/build_references.py. For the senior author's list of papers to save.",
               "made_on": TODAY, "papers": wanted_list()}, open(WANTED, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"lane: {len(made)} questions worked on: " + ", ".join(f"{k} {sum(r['status'] == k for r in made)}" for k in ("published", "waiting", "none")) + f"; today {llm.ledger()['neurons']:.0f} of {llm.OUR_LIMIT} neurons used")
    return made


def _reserve_selftest():
    keep = (llm.left, llm.groq_left, llm.has)
    try:
        # (20 November 2026) without Google's models: on GitHub's machines, where the key is there, their room decided this test, and it failed whenever they had room
        llm.has = lambda m: False
        llm.left = lambda: 5000; llm.groq_left = lambda n: 10000
        assert not kept_for_sent({"id": "w_1"}) and not kept_for_sent({"id": "w_a1", "from": "a question visitors sent"})          # room at Cloudflare: every question is worked on
        llm.left = lambda: 800
        assert kept_for_sent({"id": "w_1"}) and kept_for_sent({"id": "w_g1", "from": "the system's own question"}) and not kept_for_sent({"id": "w_a1", "from": "a question visitors sent"}) and not kept_for_sent({"id": "t_1", "trial": True})
        llm.groq_left = lambda n: 90000
        assert not kept_for_sent({"id": "w_1"})                                                                                    # room at Groq: the system's own go on
    finally: llm.left, llm.groq_left, llm.has = keep


def selftest():
    _reserve_selftest()
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
    V = lambda *xs: {"verdicts": [{"n": i + 1, "supported": x is True, "problem": "" if x is True else x} for i, x in enumerate(xs)], "opening": True}
    item = {"id": "w_0024", "q": "Can you get addicted to ketamine?", "ways": ["is ketamine addictive"]}
    ex = [{"q": "Q?", "short": "S.", "but": "B.", "how": ["H1.", "H2."]}] * 3
    mk = lambda it=item: make(it, found, chat, Enc(), MODELS, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex)
    # (lane 19, 18 November 2026) a paper whose full text the service fails on: passed over with a note, and the question keeps its try (it was "the lane itself failed on it (HTTPError)" on every try before)
    import urllib.error
    def broken(pmcid): raise urllib.error.HTTPError("https://example.org/" + str(pmcid) + "/fullTextXML", 500, "Internal Server Error", {}, None)
    r = make(item, dict(found, wanted=[]), chat, Enc(), MODELS, fulltext=broken, crossref=crossref, ex=ex, summary=lambda doi: None)
    assert r["status"] == "none" and "no source that can be read" in r["why"] and [x.get("fault") for x in r["looked"]] == ["its full text could not be fetched (HTTPError)"], (r["status"], r["why"], r["looked"])
    assert r["soft"] == "a source could not be fetched" and "1 source(s) could not be fetched just now: tried again in the next run" in r["why"], (r.get("soft"), r["why"])      # not the answer's fault: tried again in the next run
    r = make(item, dict(found, can_read=[], wanted=[], problems=["a search failed: timed out"]), chat, Enc(), MODELS, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex, summary=lambda doi: None)
    assert r["status"] == "none" and r["soft"] and "the search for papers did not all come back" in r["why"], (r["status"], r["why"])
    r = make(item, dict(found, can_read=[], wanted=[]), chat, Enc(), MODELS, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex, summary=lambda doi: None)
    assert r["status"] == "none" and not r.get("soft") and r["why"] == "no source that can be read gave a finding for this question", (r["status"], r["why"], r.get("soft"))   # nothing to read, and nothing failed: the answer's own
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
    # (lane 11) what did not stand is kept: the draft that broke a rule with the rule beside the sentence, and the line that was dropped with who dropped it and why
    assert [x["try"] for x in r["tries"]] == [1] and r["tries"][0]["why"].startswith("a rule was broken") and all(p["rests_on"] and p["rests_on"][0]["quote"] for p in r["tries"][0]["parts"]), r.get("tries")
    assert [(p["part"], p["by"]) for p in r["tries"][0]["parts"] if not p["ok"]] == [("short", "a rule")] and "said" not in next(p for p in r["tries"][0]["parts"] if p["ok"]), r["tries"][0]["parts"]
    assert len(r["dropped"]) == 1 and r["dropped"][0]["try"] == 2 and r["dropped"][0]["by"] == "the second reader" and "trouble stopping" in r["dropped"][0]["said"] and r["dropped"][0]["text"] not in [p["text"] for p in r["parts"]] and r["dropped"][0]["rests_on"][0]["quote"], r.get("dropped")
    # 3. a number that is not in the paper's words: refused by code even though the checker would not be asked
    script["writer"] = [W("Yes. About 40% of people who used ketamine regularly met criteria for dependence.")] * 3; script["checker"] = []
    r = mk(); assert r["status"] == "none" and "a number that is not in the paper's words" in r["why"], r["why"]
    # 4. the checker refuses the short answer twice: no answer
    script["writer"] = [W(ok_short)] * 3; script["checker"] = [V("stronger than the passage", True, True, True)] * 3
    r = mk(); assert r["status"] == "none" and r["why"] == "the second reader did not accept the answer" or "no draft passed" in r["why"], r["why"]
    assert [x["try"] for x in r["tries"]] == [1, 2, 3] and r["tries"][-1]["why"] == "the last draft: no answer" and all(next(p for p in x["parts"] if p["part"] == "short")["said"] == "stronger than the passage" and next(p for p in x["parts"] if p["part"] == "short")["by"] == "the second reader" for x in r["tries"]), r.get("tries")   # (lane 11) an answer that was not given is on file to be read, sentence by sentence
    # (lane 4) a question that can be answered with yes or no is answered so, first, and in everyday words: written again when it is not
    assert len(lead(item["q"], [{"part": "short", "text": "People with ketamine use disorder experience abstinence symptoms."}])) == 2 and not lead("What is synthetic weed like?", [{"part": "short", "text": "Synthetic weed is riskier."}]) and not lead(item["q"], [{"part": "short", "text": ok_short}])
    calls.clear(); script["writer"] = [W("People who use ketamine regularly can become dependent on it."), W(ok_short)]; script["checker"] = [V(True, True, True, True)]
    r = mk(); assert r["status"] == "published" and "yes or no" in r["gates"]["rules"] and "begin the short answer with Yes" in [c for c in calls if c[0] == "writer"][1][2], r["gates"]
    assert lead(item["q"], [{"part": "but", "text": "The sources do not say how many people who use ketamine actually become addicted."}]) and not lead(item["q"], [{"part": "but", "text": "It has been reported mainly after frequent use over a long time."}])
    # (lane 9) the plan: the planner chooses the items; only they reach the writer, with the plan; a plan with unknown labels or no How group is not used
    lbl = {"F1": {"ref": "a"}, "F2": {"ref": "a"}, "L1": {"ref": "a"}, "F3": {"ref": "b"}, "DA": {"ref": "a"}}
    fake = lambda reply: (lambda model, messages, room: json.dumps(reply))
    pl = make_plan(fake({"short": ["F3", "F1", "F99"], "direct": "Yes", "but": ["F2", "L1"], "how": [["DA", "F1", "F3"], ["F3"], ["F2"]], "unanswered": ""}), "m", "Can you?", [], lbl)
    assert pl == {"short": ["F3", "F1"], "direct": "Yes", "but": ["F2"], "how": [["DA", "F1"], ["F3"]], "unanswered": ""}, pl
    assert make_plan(fake({"short": ["F99"], "how": [["F1"]]}), "m", "q", [], lbl) is None and make_plan(fake({"short": ["F1"], "how": []}), "m", "q", [], lbl) is None
    srcs = [{"tag": "A", "read": "full", "kind": "review", "title": "T", "year": 2022, "design": {"text": "a review", "quote": "q"}, "findings": [{"id": "F1", "text": "one", "quote": "q1"}, {"id": "F2", "text": "two", "quote": "q2"}], "limits": [{"id": "L1", "text": "lim", "quote": "q3"}]}]
    wp = writer_prompt("Can you?", srcs, [], "", {"short": ["F1"], "direct": "Yes", "but": ["F2"], "how": [["DA", "F1"]], "unanswered": ""})
    assert "[F1] one" in wp and "[F2] two" in wp and "[L1]" not in wp and 'begin it with "Yes"' in wp and '"but": write it from F2 and nothing else' in wp and "a line of \"how\" from DA, F1" in wp
    assert lead(item["q"], [{"part": "but", "text": "The sources lack a full framework to judge how likely addiction is."}])
    assert not NOT_AN_AMOUNT_FOR_PEOPLE.search("400 mg a day for adults") and NOT_AN_AMOUNT_FOR_PEOPLE.search("400 mg/day for adults [10 g for lethality]")
    # a word of how often or how sure must be the source's own
    lb = {"F1": {"quote": "Effects can be similar to cannabis but can also be stronger or more unpleasant."}, "F2": {"quote": "synthetic cannabinoids are often more potent than natural cannabis"}}
    # (lane 10) words that say more than their source: a praising word, a rank, "most", "both", a word that makes it bigger or smaller, "causes", a result for men said of people
    sm = lambda ours, src: [k for k, _, _ in says_more_text(ours, src)]
    assert sm("In a famous UK ranking, alcohol came top.", "A UK panel ranked alcohol most harmful overall.") == ["a praising word"] and not sm("In a well-known UK ranking, alcohol came top.", "In this well-known ranking by a UK panel, alcohol came top.")
    assert sm("Numbness was the most common problem.", "Of 100 people in published reports, 80 had numbness and 58 had trouble walking.") == ["a rank"] and not sm("Numbness was the most common problem.", "Numbness was the most frequently reported complaint.")
    assert sm("Most people handed their drugs over.", "Some people handed their drugs over; 15 of 164 did.") == ["“most”"] and not sm("Most people handed their drugs over.", "30 of 45 people handed drugs over.") and not sm("Most people got better.", "62 in 100 improved.")
    assert over_half("55 in 100 of these deaths") and over_half("62 of 64 people") and over_half("about two thirds") and not over_half("15 of 164 people") and not over_half("26 to 27 in 100")
    assert sm("Both reviews say withdrawal can resemble the first problem.", "The review says withdrawal symptoms can resemble the original problem.") == ["“both”"]
    assert sm("Drug use rose slightly.", "Use went from about 8 to 12 in 100 adults.") == ["a word that makes it smaller"] and not sm("Drug use rose slightly.", "There was a small rise in use.")
    assert sm("It severely damages memory.", "Scores on memory tests were lower.") == ["a word that makes it bigger"] and not sm("It severely damages memory.", "Marked impairment of memory was seen.")
    assert sm("Cannabis causes psychosis.", "Cannabis use was associated with psychosis.") == ["“causes”"] and not sm("Ketamine causes bladder damage.", "Frequent ketamine use damages the bladder lining.") and not sm("It can lead to dependence.", "Repeated use may result in dependence.")
    assert not sm("Yes, kratom can lead to addiction.", "prolonged drug use, which under certain circumstances can degenerate into outright addiction") and not sm("Regular use can lead to tolerance.", "If you use it regularly your body may become tolerant of the drug's effects.")
    assert sm("It raises the risk of a bleed in the brain 2–5 times.", "Meth increases the likelihood of intracerebral hemorrhage (ICH) by as much as 2–5 times") == ["a ceiling said as the size"]
    assert not sm("It raises the risk of a bleed in the brain by as much as 2 to 5 times.", "Meth increases the likelihood of intracerebral hemorrhage (ICH) by as much as 2–5 times") and not sm("Up to 30 in 100 had it.", "up to 30% of patients") and not sm("About 30 in 100 had it; 12 did not.", "up to 45% of patients, and 30% in one study")
    assert sm("People who believed their drink was alcoholic drank more.", "Men told their drink had vodka drank about twice as much.") == ["a result for men, said of people"] and not sm("Men who believed their drink was alcoholic drank more.", "Men told their drink had vodka drank about twice as much.")
    assert says_more([{"part": "short", "text": "In a famous UK ranking, alcohol came top.", "uses": ["F1"]}], {"F1": {"quote": "A UK panel ranked alcohol most harmful overall.", "passage_text": ""}})[0][0] == "short"
    assert not says_more([{"part": "but", "text": "It has not read every famous study on this question.", "uses": [], "fixed": True}], {})
    assert not hedges([{"part": "short", "text": "Research does not show a clear, proven boost.", "uses": ["F1"]}], lb) and hedges([{"part": "short", "text": "It is proven to be stronger.", "uses": ["F1"]}], lb)
    assert not sm("No study found a statistically significant rise.", "no study to date has revealed an effect") and sm("There was a significant rise.", "use went from 8 to 12 in 100") == ["a word that makes it bigger"]
    assert hedges([{"part": "short", "text": "It is often stronger and more unpleasant.", "uses": ["F1"]}], lb) and not hedges([{"part": "short", "text": "It is often stronger than cannabis.", "uses": ["F1", "F2"]}], lb) and not hedges([{"part": "short", "text": "It can be stronger and more unpleasant.", "uses": ["F1"]}], lb)
    assert words15("Easy to want more and take larger doses. Mental health can get worse. Psychotic episodes can be triggered, usually in those already susceptible, and last for weeks.", "FRANK says psychotic episodes can be triggered.") == "Psychotic episodes can be triggered, usually in those already susceptible, and last for weeks"
    f = fitting(lambda model, messages, room: (_ for _ in ()).throw(llm.Unavailable("this call is larger than Groq's free plan allows in a minute (8012 of 8000 tokens)")) if room > 2850 else f"room {room}")
    assert f("groq:openai/gpt-oss-120b", [], 2900) == "room 2828" and f("groq:x", [], 800) == "room 800"
    # the second reader also judges the answer as a whole. A But about something else, three times: the code writes the But from what the answer rests on, and the answer stands
    off = dict(V(True, True, True, True), answers_question=True, but_fits=False, why="it is about a treatment")
    calls.clear(); script["writer"] = [W(ok_short)] * 3; script["checker"] = [off] * 3
    r = mk(); assert r["status"] == "published" and r["parts"][1]["text"] == "This rests on 1 review." and r["parts"][1]["rests_on"] and "the code wrote the But itself" in r["gates"]["but"], (r["status"], r["why"], r["parts"][1:2], r["gates"])
    assert "QUESTION that was asked: Can you get addicted to ketamine?" in [c for c in calls if c[0] == "checker"][0][2] and "a second reader did not accept but (it is about something else than the short answer" in [c for c in calls if c[0] == "writer"][1][2]
    # a short answer that answers another question, three times: no answer
    script["writer"] = [W(ok_short)] * 3; script["checker"] = [dict(V(True, True, True, True), answers_question=False, but_fits=True, why="it says how it is treated")] * 3
    r = mk(); assert r["status"] == "none" and "it does not answer the question itself" in r["gates"]["check"], (r["status"], r["why"], r["gates"])
    assert own_but([{"read": "full", "kind": "review", "people": True}, {"read": "full", "kind": "study", "people": True}, {"read": "page", "kind": "official", "people": True}, {"read": "page", "kind": "official", "people": True}], True) == "This rests on 1 review, 1 study in people and 2 official pages."
    # the choice of a team of models across two free services: keys, room, and never the same model twice in a row
    import tempfile
    tf = pathlib.Path(tempfile.mkdtemp()) / "models.json"
    tf.write_text(json.dumps({"reader": "@cf/r", "writer": "@cf/w", "checker": "@cf/c", "teams": [
        {"name": "A", "reader": "@cf/r", "reader_else": "groq:openai/gpt-oss-20b", "writer": "groq:openai/gpt-oss-120b", "checker": "groq:qwen/qwen3.8-27b"},
        {"name": "B", "reader": "@cf/r", "reader_else": "groq:openai/gpt-oss-20b", "writer": "@cf/w", "checker": "groq:openai/gpt-oss-120b", "checker_else": "@cf/openai/gpt-oss-120b"}]}), encoding="utf-8")
    keep = (llm.has, llm.left, llm.groq_left); cf = [9000]; gq = {"openai/gpt-oss-120b": 180000, "openai/gpt-oss-20b": 180000, "qwen/qwen3.8-27b": 180000}; keys = {"groq": True, "cf": True}
    llm.has = lambda m: keys["groq"] if m.startswith("groq:") else keys["cf"]; llm.left = lambda: cf[0]; llm.groq_left = lambda n: gq.get(n, 0)
    try:
        T = lambda *a, **k: (lambda t: t and {x: y for x, y in t.items() if x != "writer_2"})(team(*a, **k))        # (the team without its writer's stand-in, which has its own test below)
        assert T(tf) == {"reader": "@cf/r", "writer": "groq:openai/gpt-oss-120b", "checker": "groq:qwen/qwen3.8-27b", "team": "A", "reader_2": "groq:openai/gpt-oss-20b"}      # (lane 14: the team's other reader stands by)
        assert team(tf)["writer_2"] == "@cf/meta/llama-3.3-70b-instruct-fp8-fast" and team(tf, avoid=("A",))["team"] == "B" and team(tf, avoid=("A", "B"))["team"] == "A"      # (lane 19) the writer's stand-in is another model than every other of the answer; a team that tried today comes after the others
        assert team(tf, only="B")["team"] == "B" and team(tf, only="Z") is None                                               # (a request may name its team)
        cf[0] = 100; assert team(tf)["reader"] == "groq:openai/gpt-oss-20b" and team(tf)["team"] == "A"                    # Cloudflare's day is used up: the reader works at Groq
        gq["qwen/qwen3.8-27b"] = 1000; assert team(tf) is None                                                             # team A's second reader has no room, and team B's writer is at Cloudflare, which has none
        cf[0] = 9000; assert T(tf) == {"reader": "@cf/r", "writer": "@cf/w", "checker": "groq:openai/gpt-oss-120b", "team": "B", "reader_2": "groq:openai/gpt-oss-20b"}
        keys["groq"] = False; assert T(tf) == {"reader": "@cf/r", "writer": "@cf/w", "checker": "@cf/openai/gpt-oss-120b", "team": "B"}   # no second service: every model at Cloudflare, as before
        cf[0] = 900; assert team(tf) is None
        assert base("groq:openai/gpt-oss-120b") == base("@cf/openai/gpt-oss-120b") == "gpt-oss-120b"
        # the planner has a second choice too: with little left of it at Groq, the plan is made at Cloudflare and the answer still gets one
        tf.write_text(json.dumps({"teams": [{"name": "C", "reader": "@cf/r", "writer": "groq:qwen/qwen3.8-27b", "checker": "groq:openai/gpt-oss-120b", "checker_else": "@cf/openai/gpt-oss-120b",
                                             "planner": "groq:openai/gpt-oss-120b", "planner_else": "@cf/openai/gpt-oss-120b"}]}), encoding="utf-8")
        keys["groq"] = True; cf[0] = 9000; gq.update({"qwen/qwen3.8-27b": 180000, "openai/gpt-oss-120b": 180000})
        assert {k: v for k, v in T(tf).items() if k != "reader_2"} == {"reader": "@cf/r", "writer": "groq:qwen/qwen3.8-27b", "checker": "groq:openai/gpt-oss-120b", "planner": "groq:openai/gpt-oss-120b", "team": "C"}
        gq["openai/gpt-oss-120b"] = 20000; t = team(tf); assert t["checker"] == "groq:openai/gpt-oss-120b" and t["planner"] == "@cf/openai/gpt-oss-120b", t      # room for the check (16,000) but not for the plan as well (7,000 more)
        gq["openai/gpt-oss-120b"] = 5000; t = team(tf); assert t["checker"] == "@cf/openai/gpt-oss-120b" and t["planner"] == "@cf/openai/gpt-oss-120b", t
        # a team with further second readers is that team only with all of them: each needs a key and room, and is another model than the writer and the second reader
        tf.write_text(json.dumps({"teams": [{"name": "D", "reader": "@cf/r", "writer": "groq:qwen/qwen3.8-27b", "checker": "groq:openai/gpt-oss-120b", "also": ["gemini:gemma-4-31b-it", "gemini:gemini-3.5-flash-lite"]},
                                            {"name": "E", "reader": "@cf/r", "writer": "groq:qwen/qwen3.8-27b", "checker": "groq:openai/gpt-oss-120b"}]}), encoding="utf-8")
        gq["openai/gpt-oss-120b"] = 180000; keys["gemini"] = True; fits = [True]; keep2 = (llm.calls_fit,)
        llm.has = lambda m: keys.get("gemini", False) if m.startswith("gemini:") else keys["groq"] if m.startswith("groq:") else keys["cf"]; llm.calls_fit = lambda by: not by or (fits[0] and by == {"gemini:gemma-4-31b-it": 3, "gemini:gemini-3.5-flash-lite": 3})
        try:
            t = team(tf); assert t["team"] == "D" and t["also1"] == "gemini:gemma-4-31b-it" and t["also2"] == "gemini:gemini-3.5-flash-lite", t
            fits[0] = False; assert team(tf)["team"] == "E"                                                         # no room for a further reader today: the next team, which names none
            fits[0] = True; keys["gemini"] = False; assert team(tf)["team"] == "E"                                    # no key for it: the same
            keys["gemini"] = True
            # one place, several models: the first that has room today; none of them: the team is not that team
            tf.write_text(json.dumps({"teams": [{"name": "G", "reader": "@cf/r", "writer": "groq:qwen/qwen3.8-27b", "checker": "groq:openai/gpt-oss-120b", "also": ["gemini:gemini-3.5-flash-lite", ["gemini:gemini-4-hydrogen", "gemini:gemini-3.8-flash"]]},
                                                {"name": "E", "reader": "@cf/r", "writer": "groq:qwen/qwen3.8-27b", "checker": "groq:openai/gpt-oss-120b"}]}), encoding="utf-8")
            used_up = {"gemini:gemini-4-hydrogen"}; llm.calls_fit = lambda by: not (set(by) & used_up)
            t = team(tf); assert t["team"] == "G" and t["also1"] == "gemini:gemini-3.5-flash-lite" and t["also2"] == "gemini:gemini-3.8-flash", t
            used_up.add("gemini:gemini-3.8-flash"); assert team(tf)["team"] == "E"
            # (19 November 2026) a strong reader with 20 free calls a day is asked for one call an answer, so it serves while it has one left (three were asked for until then)
            wanted_of = []; llm.calls_fit = lambda by: wanted_of.append(dict(by)) or True
            assert team(tf)["also2"] == "gemini:gemini-4-hydrogen" and {"gemini:gemini-4-hydrogen": 1} in wanted_of and wanted_of[-1] == {"gemini:gemini-3.5-flash-lite": 3, "gemini:gemini-4-hydrogen": 1}, wanted_of
            # a reader asked for marks is named "<model>#marks": the key and the room are the model's, and it needs a call for every sentence; the second reader's own model may be asked that other way
            tf.write_text(json.dumps({"teams": [{"name": "M", "reader": "@cf/r", "writer": "groq:qwen/qwen3.8-27b", "checker": "gemini:gemini-3.5-flash-lite", "also": ["gemini:gemini-3.5-flash-lite#marks"]}]}), encoding="utf-8")
            asked_for = []; llm.calls_fit = lambda by: asked_for.append(dict(by)) or True
            t = team(tf); assert t["also1"] == "gemini:gemini-3.5-flash-lite#marks" and asked_for[-1] == {"gemini:gemini-3.5-flash-lite": 5 + 15}, (t, asked_for[-1:])
            llm.calls_fit = lambda by: not by or (fits[0] and by == {"gemini:gemma-4-31b-it": 3, "gemini:gemini-3.5-flash-lite": 3})
            tf.write_text(json.dumps({"teams": [{"name": "F", "reader": "@cf/r", "writer": "groq:qwen/qwen3.8-27b", "checker": "groq:openai/gpt-oss-120b", "also": ["@cf/openai/gpt-oss-120b"]}]}), encoding="utf-8")
            assert team(tf) is None                                                                                 # the second reader's own model at another service is not a further reader
        finally: llm.calls_fit, = keep2
    finally: llm.has, llm.left, llm.groq_left = keep
    # (lane 10) the checked claims of the same page: an answer that cannot be true together with one waits for a person; one that says the same is noted; a far claim is not asked about
    cl = lambda drugs: [{"id": "cl_ket_dependence", "drug": "ketamine", "plain": "People who use ketamine often can become dependent on it.", "statement": "Regular ketamine use is associated with dependence."},
                        {"id": "cl_ket_far", "drug": "ketamine", "plain": "Zebra finches sing at dawn.", "statement": ""}]
    calls.clear(); script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True), {"pairs": [{"n": 1, "is": "differs", "why": "A says nobody becomes dependent"}, {"n": 2, "is": "same", "why": ""}]}]
    r = make(item, found, chat, Enc(), MODELS, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex, claims=cl)
    assert r["status"] == "waiting" and "cl_ket_dependence" in r["why"] and r["with_checked"]["differs"][0]["claim"] == "cl_ket_dependence" and "B (checked): People who use ketamine often can become dependent on it." in calls[-1][2] and "Zebra finches" not in calls[-1][2], (r["status"], r["why"], r.get("with_checked"))
    script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True), {"pairs": [{"n": 1, "is": "same", "why": ""}]}]
    r = make(item, found, chat, Enc(), MODELS, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex, claims=cl)
    assert r["status"] == "published" and r["with_checked"]["same"] and "nothing against them" in r["gates"]["checked"], (r["status"], r["gates"])
    # (decision 23) our own checker is a second judge: a How line it does not find in the source's words is dropped; a short answer it
    # refuses is written again, and refused twice there is no answer; what it said is kept in the record
    class Own:
        e = {"name": "pharmakon-check-test", "threshold": 0.5}
        def __init__(self, low): self.low, self.asked = low, []
        def score(self, pairs): self.asked.append(pairs); return [0.2 if any(w in t for w in self.low) else 0.9 for _, t in pairs]
    script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True)]
    o = Own([]); r = make(item, found, chat, Enc(), MODELS, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex, own_check=o)
    n_how = sum(p["part"].startswith("how") for p in r["parts"])
    assert r["status"] == "published" and r["own"]["model"] == "pharmakon-check-test" and set(r["own"]["scores"]) >= {"short", "but"} and all(v == 0.9 for v in r["own"]["scores"].values()) and "our own checker" in r["gates"]["own"], r.get("own")
    assert all(src.strip() and text.strip() for src, text in o.asked[0])                                    # every sentence is asked about beside the words it rests on
    assert len(o.asked) == 2 and set(r["own"]["scores_quotes_alone"]) == set(r["own"]["scores"]) and all(len(a[0]) > len(b[0]) and a[1] == b[1] for a, b in zip(o.asked[0], o.asked[1]))    # (lane 11) and once more against the quotes alone: measured, it decides nothing
    a_how = next(p["text"] for p in r["parts"] if p["part"].startswith("how"))
    script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True)]
    r2 = make(item, found, chat, Enc(), MODELS, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex, own_check=Own([a_how[:25]]))
    assert r2["status"] == "published" and sum(p["part"].startswith("how") for p in r2["parts"]) == n_how - 1 and not any(p["text"] == a_how for p in r2["parts"]), [p["part"] for p in r2["parts"]]
    assert [(d["by"], d["text"]) for d in r2["dropped"]] == [("our own checker", a_how)] and "(0.20)" in r2["dropped"][0]["said"], r2.get("dropped")       # (lane 11) the line our own checker dropped is kept with its score
    a_short = next(p["text"] for p in r["parts"] if p["part"] == "short")
    script["writer"] = [W(ok_short), W(ok_short), W(ok_short)]; script["checker"] = [V(True, True, True, True)] * 3
    r3 = make(item, found, chat, Enc(), MODELS, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex, own_check=Own([a_short[:25]]))
    assert r3["status"] == "none" and "our own checker does not find it" in r3["why"], (r3["status"], r3["why"])
    assert len(r3["tries"]) == 3 and all(next(p for p in x["parts"] if p["part"] == "short")["by"] == "our own checker" for x in r3["tries"]), r3.get("tries")
    # the second reader's marks: the code gives the verdict; words of measure need the source's own words, and copied words that are not in the passages count for nothing
    mp = marks_prompt("It often is so for people.", ["It can be so.", "Men said so in one survey."])
    assert "SENTENCE: It often is so for people.\n   PASSAGE: It can be so.\n   PASSAGE: Men said so in one survey." in mp and '"report_as_fact"' in mp
    clean = {"measure": [], "report_as_fact": False, "wider": False, "cause_added": False, "extra": False, "which": ""}
    assert marks_verdict(clean, ["It can be so."]) == {"through": True, "clear": True, "problem": ""}
    assert marks_verdict(dict(clean, measure=[{"word": "often", "passage_words": "NONE"}]), ["It can be so."])["problem"] == "“often”: no passage says it"
    assert marks_verdict(dict(clean, measure=[{"word": "often", "passage_words": "is frequently so"}]), ["It can be so."])["problem"] == "“often”: the words given for it are not in the passages"
    assert marks_verdict(dict(clean, measure=[{"word": "often", "passage_words": "Often, it is so"}]), ["Often it is so."])["through"]
    v = marks_verdict(dict(clean, wider=True, which="people"), ["Men said so."]); assert not v["through"] and v["clear"] and "more, or about something else" in v["problem"] and "(people)" in v["problem"]
    assert marks_verdict({"measure": [], "wider": False}, ["x"]) == {"through": False, "clear": False, "problem": "the reader did not answer the five questions"} and not marks_verdict(None, ["x"])["clear"]
    # (lane 10) further second readers: each must accept every sentence too. A How line one of them refuses is dropped; a short answer
    # one refuses is written again; they are not asked when the second reader has refused the head already; what each said is kept
    M2 = dict(MODELS, also1="gemini:gemma-4-31b-it")
    calls.clear(); script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True), V(True, True, True, False)]
    r = make(item, found, chat, Enc(), M2, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex)
    assert r["status"] == "published" and sum(p["part"].startswith("how") for p in r["parts"]) == n_how - 1 and r["panel"]["gemini:gemma-4-31b-it"]["how2"][0] is False and "gemma-4-31b-it accepted 3 of 4" in r["gates"]["panel"] and "and by gemini:gemma-4-31b-it" in r["gates"]["check"], (r["status"], r["gates"])
    assert [c[1] for c in calls if c[0] == "checker"][:2] == [MODELS["checker"], "gemini:gemma-4-31b-it"] and "QUESTION that was asked" not in [c for c in calls if c[0] == "checker"][1][2]      # the further reader is asked about the sentences, not about the answer as a whole
    calls.clear(); script["writer"] = [W(ok_short)] * 3; script["checker"] = [V(True, True, True, True), V(False, True, True, True)] * 3
    r = make(item, found, chat, Enc(), M2, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex)
    assert r["status"] == "none" and "a further reader (gemma-4-31b-it) did not accept it" in r["why"] and "a second reader did not accept short (a further reader (gemma-4-31b-it)" in [c for c in calls if c[0] == "writer"][1][2], (r["status"], r["why"])
    calls.clear(); script["writer"] = [W(ok_short)] * 3; script["checker"] = [V(False, True, True, True)] * 3
    r = make(item, found, chat, Enc(), M2, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex)
    assert r["status"] == "none" and not any(c[1] == "gemini:gemma-4-31b-it" for c in calls) and "panel" not in r, (r["status"], r["why"])
    # a further reader asked for marks ("<model>#marks"): five small questions a sentence, the code gives the verdict; a How line with a word of measure the passages do not carry is dropped
    M3 = dict(MODELS, also1="gemini:gemini-3.5-flash-lite#marks"); marked = []
    def chat_marks(model, messages, max_tokens=0):
        if messages[0]["content"] == MARKS_SYS:
            marked.append((model, messages[1]["content"])); bad_one = "SENTENCE: With frequent use, tolerance came quickly" in messages[1]["content"]
            return json.dumps({"measure": [{"word": "quickly", "passage_words": "NONE"}] if bad_one else [], "report_as_fact": False, "wider": False, "cause_added": False, "extra": False, "which": ""})
        return chat(model, messages, max_tokens)
    calls.clear(); script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True)]
    r = make(item, found, chat_marks, Enc(), M3, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex)
    assert r["status"] == "published" and len(marked) == 4 and marked[0][0] == "gemini:gemini-3.5-flash-lite" and "   PASSAGE: (" in marked[0][1] and sum(p["part"].startswith("how") for p in r["parts"]) == n_how - 1, (r["status"], r["why"], len(marked))
    assert r["panel"]["gemini:gemini-3.5-flash-lite#marks"]["how2"] == [False, "“quickly”: no passage says it"] and "and by gemini:gemini-3.5-flash-lite#marks" in r["gates"]["check"]
    # a further reader that cannot be reached: the answer is not lost; it has passed the others and waits for that reader or the editor
    def chat_gap(model, messages, max_tokens=0):
        if model == "gemini:gemma-4-31b-it": raise llm.Unavailable("gemini answered 503: high demand")
        return chat(model, messages, max_tokens)
    calls.clear(); script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True)]
    r = make(item, found, chat_gap, Enc(), M2, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex)
    assert r["status"] == "waiting" and "a further reader of its team could not be (gemma-4-31b-it)" in r["why"] and r["panel"]["gemini:gemma-4-31b-it"].startswith("could not be asked") and "could not be asked" in r["gates"]["panel"] and len(r["parts"]) >= 4, (r["status"], r["why"], r["gates"])
    # (lane 16) where the place names more than one model, the next one is asked: the answer does not wait, and the record says who could not be asked and who read it
    calls.clear(); script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True), V(True, True, True, True)]
    r = make(item, found, chat_gap, Enc(), dict(M2, also1_else="gemini:gemini-3.8-flash|gemini:gemini-3.6-flash"), fulltext=lambda pmcid: xml, crossref=crossref, ex=ex)
    assert r["status"] == "published" and not r.get("panel_gap") and r["panel"]["gemini:gemma-4-31b-it"].startswith("could not be asked") and r["panel"]["gemini:gemini-3.8-flash"]["short"][0] is True and "gemini:gemini-3.6-flash" not in r["panel"], (r["status"], r["why"], r.get("panel"))
    assert [c[1] for c in calls if c[0] == "checker"] == [MODELS["checker"], "gemini:gemini-3.8-flash"]
    # (lane 17) a further reader whose reply holds no verdict, twice, has not read the answer: the next one named is asked; with none left the answer waits, it is not thrown away
    calls.clear(); script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True), {"x": 1}, {"x": 1}, V(True, True, True, True)]
    r = make(item, found, chat, Enc(), dict(MODELS, also1="gemini:gemini-3.8-flash", also1_else="gemini:gemini-3.6-flash"), fulltext=lambda pmcid: xml, crossref=crossref, ex=ex)
    assert r["status"] == "published" and r["panel"]["gemini:gemini-3.8-flash"] == "could not be asked: its reply held no verdict, twice" and r["panel"]["gemini:gemini-3.6-flash"]["short"][0] is True, (r["status"], r["why"], r.get("panel"))
    calls.clear(); script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True), {"x": 1}, {"x": 1}]
    r = make(item, found, chat, Enc(), dict(MODELS, also1="gemini:gemini-3.8-flash"), fulltext=lambda pmcid: xml, crossref=crossref, ex=ex)
    assert r["status"] == "waiting" and "could not be (gemini-3.8-flash)" in r["why"] and len(r["parts"]) >= 4, (r["status"], r["why"])
    # (lane 16) the word a short answer opens with is not part of the sentence the readers set beside the passages; the second reader judges it apart, as the answer to the question
    assert opener_of(ok_short) == ("Yes", "In a review of studies, between 9% and 27% of people who used ketamine regularly met criteria for dependence.")
    assert opener_of("It depends. Cannabis smoke has cancer-causing chemicals.") == ("It depends", "Cannabis smoke has cancer-causing chemicals.") and opener_of("No, the studies found no such link in people.")[0] == "No"
    assert opener_of("It can improve perceived sexual functioning for men and women.")[0] == "" and opener_of("Yes. It can.")[0] == "" and opener_of("Sometimes, in some people, it does so after long use.")[0] == ""
    lab1 = {"F1": {"paper": "P", "where": "Results", "passage_text": "between 9% and 27% met criteria", "quote": "between 9% and 27% met criteria"}}
    cp = checker_prompt([{"part": "short", "text": ok_short, "uses": ["F1"]}, {"part": "but", "text": "B.", "uses": ["F1"]}], lab1, question="Can you get addicted to ketamine?")
    assert "1. SENTENCE: In a review of studies" in cp and "SENTENCE: Yes." not in cp and "opens with the word “Yes”" in cp and '"opening": true, "answers_question"' in cp, cp[:300]
    cp = checker_prompt([{"part": "short", "text": ok_short, "uses": ["F1"]}], lab1); assert "1. SENTENCE: In a review of studies" in cp and "opening" not in cp      # a further reader sees the sentence without the word, and is not asked about it
    calls.clear(); script["writer"] = [W(ok_short)] * 3; script["checker"] = [dict(V(True, True, True, True), opening=False, why="the passages only say that some people do: It can")] * 3
    r = mk(); assert r["status"] == "none" and "the word it opens with (“Yes”) is not the answer the passages bear out: the passages only say that some people do: It can" in r["gates"]["check"], (r["status"], r["why"], r["gates"]["check"])
    assert "the word it opens with (“Yes”) is not the answer the passages bear out" in [c for c in calls if c[0] == "writer"][1][2]                 # and the writer is told so when it writes again
    calls.clear(); script["writer"] = [W(ok_short)]; script["checker"] = [{"verdicts": V(True, True, True, True)["verdicts"]}, V(True, True, True, True)]          # no word on the opening: asked once more
    r = mk(); assert r["status"] == "published" and len([c for c in calls if c[0] == "checker"]) == 2, (r["status"], r["why"])
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
    assert room_for("@cf/openai/gpt-oss-120b", 900) == 3100 and room_for("@cf/meta/llama-3.3-70b-instruct-fp8-fast", 900) == 900 and room_for("groq:openai/gpt-oss-20b", 900) == 2100 and room_for("groq:qwen/qwen3.8-27b", 900) == 900
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
    assert windows15("For men—two drinks or less in a day. For women—one drink or less in a day.") == ["For men—two drinks or less in a day", "For women—one drink or less in a day"] and not AMT.search("one study found that two reviews agree")       # (lane 13: with the source's own long dash, not a hyphen)
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
    assert rows[0]["quote"] == "Participants received 80 to 120 mg of MDMA in each of three sessions" and words(rows[0]["quote"]) <= 15 and rows[0]["rests_on"][0]["quote"] == mp[1].rstrip("."), rows
    assert rows[0]["who"].startswith("Adults with severe post-traumatic stress disorder in a clinical trial") and rows[0]["who_read"].startswith("adults with severe PTSD") and "_abbr" not in r["sources"][0] and "_text" not in r["sources"][0], rows   # (lane 11) written out for the reader; what the system's reader gave is kept beside it
    assert "4 thrown away" in r["gates"]["read"] and not any(c[0] == "writer" for c in calls) and r["complete"] is False and "only one source" in r["missing"], (r["gates"], r["missing"])
    assert "This amount was the amount in one session, for adults with severe PTSD" in calls[-1][2] and "list the AMOUNTS of mdma" in calls[0][2]
    # the second reader says of each amount whether it is of the kind the question asks for: one that is not is left out
    script["amounts"] = [mrows]; script["checker"] = [{"verdicts": [{"n": 1, "supported": True, "on_question": False, "problem": ""}]}]
    r = make(mitem, mfound, chat, Enc(), MODELS, fulltext=lambda pmcid: mxml, crossref=crossref, ex=ex, names=nm); assert r["status"] == "none" and "not an amount of the kind the question asks for" in r["gates"]["check"] and "QUESTION that was asked: What dosage of MDMA is used in studies?" in calls[-1][2], (r["status"], r["gates"])
    assert [(x["quote"], x["said"], x["source"]) for x in r["refused_rows"]] == [("Participants received 80 to 120 mg of MDMA in each of three sessions", "not an amount of the kind the question asks for", r["sources"][0]["ref"]["id"] if r["sources"] else x["source"])] and r["refused_rows"][0]["who"].startswith("adults with severe PTSD"), r.get("refused_rows")   # (lane 11) a refused amount is on file with the reason
    # (lane 11) whom ONE amount of a sentence is for: the one sex its own part names; never an amount under the other sex's name
    hse = "do not drink more than: 11 standard drinks per week, if you are a woman; 17 standard drinks per week, if you are a man"
    assert [who_of_shown("Women, men", w, c) for w, c in windows15(hse, clauses=True)] == ["Women", "men"]
    assert who_of_shown("men and women aged 18 to 64", "no more than 1 drink per day for women", "") == "women aged 18 to 64" and who_of_shown("healthy men and women", "2 drinks per day", "2 drinks per day for men and") == "healthy men"
    assert who_of_shown("Men and women", "men and women are advised not to drink more than 14 units a week", "") == "Men and women" and who_of_shown("adults", "14 units a week for women", "") == "adults"
    assert who_of_shown("women", "17 standard drinks per week, if you are a man", "") is None and who_of_shown("adults (men and women)", "3 drinks for men", "") == "men"
    g = amount_gate({"amounts": [{"passage": 1, "quote": hse, "who": "women, men", "what": "weekly low-risk guidelines"}]}, [{"n": 1, "where": "Guidelines", "text": "To keep the risk low, " + hse + ". Alcohol is a drug."}], {"read": "page", "title": "Weekly low-risk alcohol guidelines"}, ["alcohol"])
    assert [(x["who"], x["show"]) for x in g[0]] == [("women", "do not drink more than: 11 standard drinks per week, if you are a woman"), ("men", "17 standard drinks per week, if you are a man")], g
    ti = trial_items([{"id": "t_lsd_1", "q": "What amounts  of LSD have studies given to people?", "drugs": ["lsd", "Not A Slug"], "ways": ["lsd dose in studies", 5]}, {"id": "w_0001", "q": "A listed question is not a trial"}, {"id": "t_x", "q": "short"}, "words"])
    assert ti == [{"id": "t_lsd_1", "q": "What amounts of LSD have studies given to people?", "ways": ["lsd dose in studies"], "drugs": ["lsd"], "trial": True}] and trial_items(None) == [] and trial_items({"id": "t_a"}) == []
    assert holds(True, "amounts") and not holds(False, "answer") and not holds(None, "answer") and holds({"answer": True, "amounts": False}, "answer") and not holds({"answer": True, "amounts": False}, "amounts") and holds({"amounts": False}, None) and holds({}, "amounts")
    # (lane 12) the words that lead into a further part belong to that part; whom another amount is for belongs to that amount; a group's name that leads into the reader's quote is taken into it
    niaaa = "five or more drinks containing alcohol for males or four or more drinks containing alcohol for females"
    assert [w for w, _ in windows15(niaaa, clauses=True)] == ["five or more drinks containing alcohol for males", "four or more drinks containing alcohol for females"]       # lane 11 showed "... for males or four or more drinks" under "males"
    heavy = "For men, consuming five or more drinks on any day or 15 or more per week; For women, consuming four or more on any day or eight or more drinks per week"
    cl = windows15(heavy, clauses=True); assert "women" not in cl[0][1] and cl[1][1].startswith("For women, consuming four") and "men," in cl[0][1], cl      # lane 11 gave "For women," to the part before it: the men's amount stood under "women"
    g = amount_gate({"amounts": [{"passage": 1, "quote": heavy.split(", ", 1)[1], "who": "men or women", "what": "daily and weekly amounts"}]}, [{"n": 1, "where": "Drinking patterns", "text": "The institute describes it this way: " + heavy + ". Alcohol is a drug."}], {"read": "page", "title": "Understanding alcohol drinking patterns"}, ["alcohol"])
    assert [(x["who"], x["show"]) for x in g[0]] == [("men", "For men, consuming five or more drinks on any day"), ("women", "consuming four or more on any day or eight or more drinks per week")] and g[0][0]["quote"].startswith("For men, consuming five"), g
    assert who_of_shown("men or women", "15 or more per week", "15 or more per week; For women,") == "women"      # (what the old stretch did: kept here as the reason the stretch was mended, not as a wish)
    # (lane 12) what an amount is CALLED must be the passage's word: where the reader borrowed the question's, the code says what the shown words say and no more
    ccsa = [{"n": 1, "where": "Overview", "text": "A continuum of risk for people in Canada: 2 standard drinks or less per week: you are likely to avoid alcohol-related consequences for yourself or others at this level; 3-6 standard drinks per week: your risk of developing several types of cancer increases at this level."}]
    g = amount_gate({"amounts": [{"passage": 1, "quote": "2 standard drinks or less per week", "who": "people in Canada", "what": "weekly low-risk drinking level"}, {"passage": 1, "quote": "3-6 standard drinks per week", "who": "people in Canada", "what": "weekly level at which the risk of cancer increases"}]}, ccsa, {"read": "page", "title": "Canada's Guidance on Alcohol and Health"}, ["alcohol"])
    assert [(x["what"], x.get("what_read")) for x in g[0]] == [("an amount for a week", "weekly low-risk drinking level"), ("weekly level at which the risk of cancer increases", None)], g
    assert plain_what("recommended maximum daily intake", "Adults (18 years and over) 400 mg", "Adults (18 years and over) 400 mg Recommended maximum daily intake") == "recommended maximum daily intake"
    assert plain_what("daily low-risk guideline", "no more than: 2 standard drinks per day", "no more than: 2 standard drinks per day Low-risk alcohol drinking guidelines") == "daily low-risk guideline"
    assert plain_what("a safe single amount", "single doses of 200 mg", "single doses do not raise concerns") == "an amount for one occasion" and plain_what("amount in one session", "25 mg", "x") == "amount in one session" and plain_what("the safe amount", "400 mg", "x") == "an amount"
    assert "Begin with the amounts that answer the QUESTION most directly; ten items at most." in amounts_prompt("How much?", {"read": "page", "title": "T", "name": "N"}, [{"n": 1, "where": "W", "text": "x"}], ["caffeine"]) and "never borrow such a word from the QUESTION" in amounts_prompt("How much?", {"read": "page", "title": "T", "name": "N"}, [{"n": 1, "where": "W", "text": "x"}], ["caffeine"])
    assert "A limit for one day or for one occasion that the same guidance gives beside its weekly amount is of the kind asked." in checker_prompt([{"text": "x", "uses": ["R1"]}], {"R1": {"paper": "p", "where": "w", "passage_text": "t"}}, each="How much?")
    # ---- lane 14: what the editor's reading of lane 13's two answers about amounts asked for (17 November 2026, 01:55 UTC) ----
    lowq = "How much alcohol do health bodies call low-risk drinking?"
    post = "Canada's Guidance on Alcohol & Health shows 6 or fewer drinks/wk helps avoid increasingly high risks for health issues."      # (a sample post on the body's page; the page calls 1 to 2 drinks low risk and 3 to 6 moderate: lane 13 showed it under the question about low-risk drinking)
    assert other_way(lowq, post) and not other_way(lowq, "2 standard drinks or less per week: you are likely to avoid alcohol-related consequences for yourself or others at this level") and not other_way(lowq, "men and women are advised not to drink more than 14 units a week on a regular basis")
    assert other_way("How much is heavy drinking?", "For men, two drinks or less in a day is moderate drinking") and not other_way("What amounts of psilocybin have studies given to people?", "a high dose (25 mg) raised the risk of headache") and not other_way("How much caffeine a day do health bodies call safe for adults?", "Intakes up to 400mg per day do not raise safety concerns for healthy adults")
    g = amount_gate({"amounts": [{"passage": 1, "quote": "6 or fewer drinks/wk helps avoid increasingly high risks for health issues", "who": "people in Canada", "what": "weekly low-risk drinking guideline"}]}, [{"n": 1, "where": "Social media", "text": "A post that may be shared: " + post + " Read more on our site."}], {"read": "page", "title": "Canada's Guidance on Alcohol and Health"}, ["alcohol"], lowq)
    assert not g[0] and "speaks of high risk" in g[1][0]["why"], g
    assert plain_what("daily safe intake", "Intakes up to 400mg per day", "Intakes up to 400mg per day do not raise safety concerns for healthy adults FAQ Caffeine") == "an amount for a day" and plain_what("safe daily amount", "400 mg a day", "400 mg a day is considered safe for most adults") == "safe daily amount"      # "safety concerns" does not call the amount safe
    # a reader that cannot be asked does not cost the answer: the team's other reader reads from there on, and the record says so
    def chat_busy(model, messages, max_tokens=0):
        if model == "gemini:gemma-x": raise llm.Unavailable("gemini answered 503: this model is in high demand")
        return chat(model, messages, max_tokens)
    script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True)]
    r = make(item, found, chat_busy, Enc(), dict(MODELS, reader="gemini:gemma-x", reader_2=MODELS["reader"]), fulltext=lambda pmcid: xml, crossref=crossref, ex=ex)
    assert r["status"] == "published" and "gemma-x could not read on" in r["gates"]["reader"] and r["made"]["models"]["reader"] == MODELS["reader"] and r["made"]["models"]["reader_first"] == "gemini:gemma-x", (r["status"], r["why"], r["gates"].get("reader"))
    try: make(item, found, chat_busy, Enc(), dict(MODELS, reader="gemini:gemma-x"), fulltext=lambda pmcid: xml, crossref=crossref, ex=ex); raise AssertionError("no reader, and no error")
    except llm.Unavailable: pass
    # the reader that stands by has no room left today: that is "a model could not be reached" for this run (tried again in the next), with what the first reader said; never "an allowance ran out"
    def chat_both(model, messages, max_tokens=0):
        if model == "gemini:gemma-x": raise llm.Unavailable("gemini answered 503: this model is in high demand")
        if model == "groq:stand-by": raise llm.Budget("today's free tokens at Groq cannot hold this call for stand-by")
        return chat(model, messages, max_tokens)
    try: make(item, found, chat_both, Enc(), dict(MODELS, reader="gemini:gemma-x", reader_2="groq:stand-by"), fulltext=lambda pmcid: xml, crossref=crossref, ex=ex); raise AssertionError("no reader with room, and no error")
    except llm.Budget: raise AssertionError("a stand-by reader without room must not end the day")
    except llm.Unavailable as e: assert "gemma-x could not read on (gemini answered 503" in str(e) and "has no room left today" in str(e), str(e)
    # ---- lane 13: what the editor's reading of lane 12's three answers about amounts asked for (17 November 2026, 01:40 UTC) ----
    PG = lambda text, where="W": [{"n": 1, "where": where, "text": text}]
    # the parts of one quote never overlap, and a list the reader copied twice gives each amount once
    hc = "Women: limit alcohol to no more than: 2 standard drinks per day; 10 standard drinks per week; 3 standard drinks on special occasions; avoid drinking alcohol on some days. Men: limit alcohol to no more than: 3 standard drinks per day; 15 standard drinks per week; 4 standard drinks on special occasions."
    assert windows15("no more than: 2 standard drinks per day; 10 standard drinks per week; 3 standard drinks on special occasions") == ["no more than: 2 standard drinks per day; 10 standard drinks per week", "3 standard drinks on special occasions"]      # lane 12: "10 standard drinks per week" stood in both parts
    g = amount_gate({"amounts": [{"passage": 1, "quote": "no more than: 2 standard drinks per day; 10 standard drinks per week; 3 standard drinks on special occasions;", "who": "women", "what": "low-risk drinking guidelines"},
                                 {"passage": 1, "quote": "Women: limit alcohol to no more than: 2 standard drinks per day; 10 standard drinks per week", "who": "women", "what": "daily and weekly limits"}]}, PG(hc, "Canada's low-risk alcohol drinking guidelines"), {"read": "page", "title": "Low-risk alcohol drinking guidelines"}, ["alcohol"])
    assert [x["show"] for x in g[0]] == ["Women: limit alcohol to no more than: 2 standard drinks per day", "10 standard drinks per week; 3 standard drinks on special occasions", "10 standard drinks per week"], g      # the words that lead in are taken whole ("Women: limit alcohol to")
    hcs = {"ref": {"id": "hc"}}
    assert [r["show"] for _, r in one_of_each([(hcs, x) for x in g[0]])] == ["Women: limit alcohol to no more than: 2 standard drinks per day", "10 standard drinks per week; 3 standard drinks on special occasions"]      # and the second copy states nothing new: left out
    sx = {"ref": {"id": "x"}}; rw = lambda who, what, show: {"who": who, "what": what, "show": show}
    one = one_of_each([(sx, rw("women", "limits", "Women: limit alcohol to no more than: 2 standard drinks per day")), (sx, rw("women", "guidelines", "no more than: 2 standard drinks per day; 10 standard drinks per week")), (sx, rw("women", "guidelines", "3 standard drinks on special occasions")),
                       (sx, rw("women", "special occasions", "10 standard drinks per week; 3 standard drinks on special occasions")), (sx, rw("men", "limits", "no more than: 3 standard drinks per day")), (sx, rw("women", "one occasion", "3 standard drinks in one day"))])
    assert [r["show"] for _, r in one] == ["no more than: 2 standard drinks per day; 10 standard drinks per week", "3 standard drinks on special occasions", "no more than: 3 standard drinks per day", "3 standard drinks in one day"], [r["show"] for _, r in one]
    # a comparison's own words are not the amount's limit: "..., which is less than the two drinks and five drinks suggested for men" was shown for men as "less than the two drinks ..."
    greaves = "The guidelines suggest that women drink one drink or less per day and no more than three in one sitting, which is less than the two drinks and five drinks suggested for men."
    assert [w for w, _ in windows15(greaves, clauses=True)] == ["The guidelines suggest that women drink one drink or less per day", "the two drinks and five drinks suggested for men"]
    assert windows15("less than the two drinks and five drinks suggested for men") == ["the two drinks and five drinks suggested for men"] and windows15("Doses in these studies were lower than 25 mg of the medicine") == []
    assert windows15("the limit is no more than 14 units a week for men") == ["the limit is no more than 14 units a week for men"] and windows15("less than 30 mg of the medicine was given to adults") == ["less than 30 mg of the medicine was given to adults"] and windows15("more than 6 standard drinks a week") == ["more than 6 standard drinks a week"]
    # an amount for each kilogram in a summary's flat notation, a summary's flattened signs, and what the passage's own sentence says of an amount outside the reader's quote
    nw = "For the healthy adult population, moderate daily caffeine intake at a dose level up to 400 mg day(-1) (equivalent to 6 mg kg(-1) body weight day(-1) in a 65-kg person) is not associated with adverse effects. Reproductive-aged women should consume </=300 mg caffeine per day. Adults in the trial took 200 mg day(-1) of caffeine."
    assert [m.group(0) for m in AMT.finditer(nw)] == ["400 mg", "300 mg", "200 mg"] and PER_KG.search("6 mg kg(-1) body weight") and PER_KG.search("0.5 mg·kg-1") and not PER_KG.search("400 mg day(-1)") and not PER_KG.search("30 mg/70 kg")
    assert ODD_SIGNS.search("up to 400 mg day(-1)") and ODD_SIGNS.search("</=300 mg caffeine per day") and not ODD_SIGNS.search("a low dose (10 mg) of psilocybin") and not ODD_SIGNS.search("a very low dose (1 or 3 mg/70 kg)")
    g = amount_gate({"amounts": [{"passage": 1, "quote": "up to 400 mg day(-1)", "who": "healthy adult population", "what": "moderate daily caffeine intake"}, {"passage": 1, "quote": "6 mg kg(-1) body weight day(-1) in a 65-kg person", "who": "healthy adult population", "what": "moderate daily caffeine intake"},
                                 {"passage": 1, "quote": "Reproductive-aged women should consume </=300 mg caffeine per day", "who": "reproductive-aged women", "what": "daily caffeine intake"}, {"passage": 1, "quote": "Adults in the trial took 200 mg day(-1) of caffeine", "who": "adults in the trial", "what": "daily amount"}]}, PG(nw, "Summary"), {"read": "summary", "kind": "review", "title": "Effects of caffeine on human health"}, ["caffeine"])
    assert not g[0] and ["worked out from another" in x["why"] for x in g[1]] == [True, False, False, False] and "no amount with its unit" in g[1][1]["why"] and all("no part of 15 words" in x["why"] for x in g[1][2:]), g      # lane 12 showed "6 mg kg(-1) body weight day(-1) in a 65-kg person"
    g = amount_gate({"amounts": [{"passage": 1, "quote": "the dose regimen of 35-50 mg/70kg", "who": "adults with major depressive disorder", "what": "dose regimen"}]}, PG("In adults with major depressive disorder, the dose regimen of 35-50 mg/70kg was the optimal one in the dose-response analysis of psilocybin.", "Summary"), {"read": "summary", "kind": "review", "title": "Therapeutic effects of psilocybin in major depressive disorder"}, ["psilocybin"])
    assert not g[0] and "worked out from another" in g[1][0]["why"], g                       # the reader's quote left "was the optimal one" out; the passage's sentence holds it
    g = amount_gate({"amounts": [{"passage": 1, "quote": "at levels of 70 to 240 mg in a 16-oz. drink", "who": "people", "what": "caffeine in a drink"}]}, PG("Caffeine is added to these products at levels of 70 to 240 mg in a 16-oz. drink and people often do not know it.", "Top"), {"read": "page", "title": "Energy Drinks and caffeine"}, ["caffeine"])
    assert not g[0] and "a product's amount" in g[1][0]["why"], g
    # a word that calls an amount something must stand in the amount's own sentence, its heading or the title: not elsewhere in the passage
    cc = "Canada's Guidance on Alcohol and Health replaces the Low-Risk Alcohol Drinking Guidelines of 2011. It gives a continuum of risk: 2 standard drinks or less per week: you are likely to avoid alcohol-related consequences for yourself or others at this level."
    g = amount_gate({"amounts": [{"passage": 1, "quote": "2 standard drinks or less per week", "who": "people in Canada", "what": "weekly low-risk drinking"}]}, PG(cc, "Overview"), {"read": "page", "title": "Canada's Guidance on Alcohol and Health"}, ["alcohol"])
    assert [(x["what"], x["what_read"]) for x in g[0]] == [("an amount for a week", "weekly low-risk drinking")], g
    assert sentence_around(cc, "2 standard drinks or less per week").startswith("It gives a continuum") and sentence_around("One; two words here; three.", "two words") == "two words here" and sentence_around("x", "not there") == "not there"
    # the people an amount is NOT for are not a reason to leave it to a person; a group's name that leads into a quote is taken whole or not at all
    ef = "Habitual caffeine consumption up to 400mg per day does not give rise to safety concerns for non-pregnant adults. Pregnant women: habitual caffeine consumption up to 200mg per day does not give rise to safety concerns for the foetus."
    g = amount_gate({"amounts": [{"passage": 1, "quote": "Habitual caffeine consumption up to 400mg per day does not give rise to safety concerns for non-pregnant adults", "who": "non-pregnant adults", "what": "habitual daily consumption"},
                                 {"passage": 1, "quote": "habitual caffeine consumption up to 200mg per day does not give rise to safety concerns for the foetus", "who": "pregnant women", "what": "habitual daily consumption"}]}, PG(ef, "FAQ"), {"read": "page", "title": "Caffeine"}, ["caffeine"])
    assert [x["show"] for x in g[0]] == ["Habitual caffeine consumption up to 400mg per day", "Pregnant women: habitual caffeine consumption up to 200mg per day"], g       # never "women: habitual ..." for an amount that is for pregnant women
    theirs = lambda r: any(rx.search(NOT_THEM.sub(" ", r["who"] + " " + r["what"] + " " + (r.get("clause") or r["quote"]))) for what, rx in STAKES if what in ("pregnancy or children", "suicide or self-harm"))
    assert [theirs(x) for x in g[0]] == [False, True] and theirs({"who": "reproductive-aged women", "what": "daily intake", "quote": "300 mg caffeine per day"}) and theirs({"who": "women of childbearing age", "what": "x", "quote": "300 mg"})
    assert not theirs({"who": "healthy adults", "what": "x", "quote": "400 mg per day do not raise safety concerns for healthy adults, except pregnant women"}) and theirs({"who": "adults", "what": "x", "quote": "not for children: 100 mg"})
    assert ASKS_BODIES.search("How much caffeine a day do health bodies call safe for adults?") and ASKS_BODIES.search("What is the recommended amount?") and not ASKS_BODIES.search("What amounts of psilocybin have studies given to people?") and ASKS_BODIES.search("What daily amount of methadone does the medicine's label state?")
    # (lane 12) the second reader is asked about the amounts nearest the question when there are more than its room; what the room did not hold is on file
    mp2 = mp[:2] + ["In the second trial, participants received 100 mg of MDMA in each of two sessions, with two trained therapists present throughout.",
                    "The sessions were held in a quiet room with music, and participants stayed overnight at the site after each one of them.",
                    "Symptoms were rated by assessors who did not know which participants had received the medicine and which the placebo."]
    mxml2 = "<article><front><article-meta><abstract><p>" + mp2[0] + "</p></abstract></article-meta></front><body><sec><title>Methods</title>" + "".join(f"<p>{t}</p>" for t in mp2[1:]) + "</sec></body></article>"
    two = {"amounts": [mrows["amounts"][0], {"passage": 3, "quote": mp2[2].rstrip("."), "who": "participants of the second trial, with two trained therapists present", "what": "the amount in one session"}]}
    script["amounts"] = [two]; script["checker"] = [V(True, True)]
    r = make(mitem, mfound, chat, Enc(), MODELS, fulltext=lambda pmcid: mxml2, crossref=crossref, ex=ex, names=nm); assert sum(p["part"].startswith("row") for p in r["parts"]) == 2 and "not_checked_rows" not in r, r["gates"]
    globals()["N_ROWS"] = 1; script["amounts"] = [two]; script["checker"] = [V(True)]
    try: r = make(mitem, mfound, chat, Enc(), MODELS, fulltext=lambda pmcid: mxml2, crossref=crossref, ex=ex, names=nm)
    finally: globals()["N_ROWS"] = 30
    assert sum(p["part"].startswith("row") for p in r["parts"]) == 1 and len(r["not_checked_rows"]) == 1 and r["not_checked_rows"][0]["quote"] and "near" in r["not_checked_rows"][0], (r["parts"], r.get("not_checked_rows"))
    # (lane 11) a cell of a table quoted bare is widened to its row, when it stands in one place only; never where it stands twice
    cells = [{"n": 1, "where": "How much", "text": "Population group Recommended maximum daily intake; Adults (18 years and over) 400 mg; People who are breastfeeding 300 mg; People planning to become pregnant 300 mg"}]
    assert widen("400 mg", cells)[0] == "Adults (18 years and over) 400 mg" and widen("300 mg", cells) is None and widen("40 mg", cells) is None and widen("Adults", cells) is None
    g = amount_gate({"amounts": [{"passage": 1, "quote": "400 mg", "who": "Adults (18 years and over)", "what": "Recommended maximum daily intake"}, {"passage": 1, "quote": "300 mg", "who": "People who are breastfeeding", "what": "Recommended maximum daily intake"}]}, cells, {"read": "page", "title": "Caffeine in foods"}, ["caffeine"])
    assert [(x["who"], x["show"], x["quote"]) for x in g[0]] == [("Adults (18 years and over)", "Adults (18 years and over) 400 mg", "Adults (18 years and over) 400 mg")] and len(g[1]) == 1, g
    # (lane 11) an amount for each kilogram of body weight is never shown, however it is written, and a part never stops just before "per"
    efsa = "single doses of caffeine up to 200 mg - about 3 mg per kilogram of body weight (mg/kg bw) - from all sources do not raise safety concerns for the general healthy adult population"
    assert [m.group(0) for m in AMT.finditer(efsa)] == ["200 mg"] and windows15(efsa) == ["single doses of caffeine up to 200 mg"]
    assert windows15("Single doses of caffeine up to 200mg (about 3mg/kg bw for a 70-kg adult) do not give rise to safety concerns") == ["Single doses of caffeine up to 200mg"]
    assert windows15("a very low dose (1 or 3 mg/70 kg) and a high dose (22 or 30 mg/70 kg) of psilocybin") == ["a very low dose (1 or 3 mg/70 kg)", "a high dose (22 or 30 mg/70 kg) of psilocybin"]      # a study's own unit (for 70 kg) stays whole
    assert PER_KG.search("about 3 mg per kilogram") and PER_KG.search("5.7 mg/kg bw per day") and PER_KG.search("2.5 mg of caffeine per kg") and not PER_KG.search("30 mg/70 kg") and not PER_KG.search("400 mg per day")
    assert windows15("adults were given 20 mg per 24 hours of the medicine for a week") == ["adults were given 20 mg per 24 hours"] or "per 24" in windows15("adults were given 20 mg per 24 hours of the medicine for a week")[0]
    # (lane 11) the same amount for the same people twice from one source is one row (the one that carries the limit); two sources that agree stay two rows
    sa, sb = {"ref": {"id": "a"}}, {"ref": {"id": "b"}}; row = lambda who, what, show: {"who": who, "what": what, "show": show}
    one = one_of_each([(sa, row("Healthy adults", "daily amount", "400 mg/day for adults")), (sa, row("healthy adults", "daily amount", "up to 400 mg caffeine/day")), (sb, row("Healthy adults", "daily amount", "400 mg/day for adults")),
                       (sa, row("Healthy adults", "single amount", "single doses of 400 mg")), (sa, row("Healthy adults", "weekly amount", "400 mg a week")), (sa, row("Adults with a diagnosis", "daily amount", "400 mg/day"))])
    assert [(s["ref"]["id"], r["show"]) for s, r in one] == [("a", "up to 400 mg caffeine/day"), ("b", "400 mg/day for adults"), ("a", "single doses of 400 mg"), ("a", "400 mg a week"), ("a", "400 mg/day")], one
    # (lane 11) an abbreviation is written out as the source itself writes it out, or from the ten that have one meaning here; a drug's name is never taken apart, and what is not known stays
    ab = abbreviations("Adults with Treatment-Resistant Depression (TRD) took part. Major depressive disorder (MDD) is common. Cannabidiol (CBD) and gamma-hydroxybutyrate (GHB) were not given. People with Parkinson's Disease (PD) were left out. A total score (HAM) was used.")
    assert ab == {"TRD": "treatment-resistant depression", "MDD": "major depressive disorder", "PD": "Parkinson's disease"}, ab
    assert spelled("12 subjects with moderate-to-severe TRD", ab) == "12 subjects with moderate-to-severe treatment-resistant depression" and spelled("patients with MDD or PTSD", {}) == "patients with major depressive disorder or post-traumatic stress disorder"
    assert spelled("people who use MDMA or GHB, with XYZ", ab) == "people who use MDMA or GHB, with XYZ" and spelled("people with PD", ab) == "people with Parkinson's disease" and spelled("people taking SSRIs", {"SSRI": "selective serotonin reuptake inhibitors"}) == "people taking selective serotonin reuptake inhibitors"
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
    # (lane 13) a question about what official bodies say is answered from their own pages: no paper and no summary is read where a page states an amount; where none does, the papers are
    def never(*a): raise AssertionError("a paper or a summary was read for a question that an official page answered")
    calls.clear(); script["amounts"] = [orows]; script["checker"] = [V(True, True)]
    r = make(dict(oitem, q="What dose of methadone do official bodies recommend?"), {"can_read": [dict(mfound["can_read"][0])], "wanted": [{"doi": "10.1000/w.9", "near": 0.9}]}, chat, Enc(), MODELS, fulltext=never, crossref=crossref, ex=ex, names=nm, official=[lab], page=lambda o: ({"title": "Methadone Hydrochloride", "passages": lab_ps}, dict(lab_ref)), summary=never)
    assert r["status"] == "published" and r["made"]["from"] == {"papers": 0, "summaries": 0, "official": 1} and sum("list the AMOUNTS" in c[2] for c in calls) == 1, (r["status"], r["why"], r["made"]["from"])
    calls.clear(); script["amounts"] = [mrows]; script["checker"] = [V(True)]
    r = make(dict(mitem, q="What dose of MDMA do official bodies recommend?"), mfound, chat, Enc(), MODELS, fulltext=lambda pmcid: mxml, crossref=crossref, ex=ex, names=nm, official=[])
    assert r["status"] == "published" and r["made"]["from"]["papers"] == 1, (r["status"], r["why"], r["made"]["from"])
    # a question about the amount that kills is a question about dying: whatever is written waits for a person
    script["amounts"] = [orows]; script["checker"] = [V(True, True)]
    r = make(dict(oitem, q="What dose of methadone is lethal?"), {"can_read": [], "wanted": []}, chat, Enc(), MODELS, fulltext=lambda pmcid: None, crossref=crossref, ex=ex, names=nm, official=[lab], page=lambda o: ({"title": "Methadone Hydrochloride", "passages": lab_ps}, dict(lab_ref)))
    assert r["status"] == "waiting" and "dying" in r["why"], (r["status"], r["why"])
    assert stakes("Is ketamine addictive?", [{"text": "Some people who use it become dependent."}]) == "" and stakes("Do psychedelics and antidepressants interact?", []) == "mixing drugs" and stakes("x", [{"text": "It can be fatal."}]) == "dying"
    assert not rules([{"part": "short", "text": "Between 9% and 27% of people met criteria for dependence.", "uses": ["F1"]}], {"F1": {"quote": "between 9% and 27% met criteria"}})
    for bad in ("Take it 2 hours after the first dose.", "It is generally safe.", "Snorting it hits faster and stronger.", "Addicts relapse.", 'The paper says "yes".', "You should wait.", "It potentiates the high.", "Passages show a link.",
                "A 2023 online survey of adults who used cannabis found both men and women saw benefits, with wax and flower forms linked to higher satisfaction.", "People reported a stronger high from edibles."):      # (lane 16) forms compared for a wanted effect
        assert rules([{"part": "short", "text": bad, "uses": ["F1"]}], {"F1": {"quote": "2"}}), bad
    assert not [w for p, w in rules([{"part": "how1", "text": "Edibles were linked to more emergency visits than smoked cannabis in one study.", "uses": ["F1"]}], {"F1": {"quote": "more emergency visits"}}) if "form of a drug" in w]   # a risk fact about a form is not that
    # (lane 16) what a source reports from another study is not what that source found
    disc = ("Our pooled analysis of cohort studies showed a statistically significant relationship. A meta-analysis in 2019 evaluated the association between marijuana use and risk of cancer and found no significant association between ever using marijuana and the risk of head and neck or oral cancers. "
            "However, long-term marijuana use (over 10 years) was associated with an increased risk of testicular germ cell tumors (TGCT), particularly nonseminoma TGCT. Evidence for other cancers, including lung cancer, was inconclusive due to low exposure levels. In this review, we found a potential association with lung cancer.")
    assert second_hand(disc, "long-term marijuana use (over 10 years) was associated with an increased risk of testicular germ cell tumors") and second_hand(disc, "Evidence for other cancers, including lung cancer, was inconclusive") and second_hand(disc, "found no significant association between ever using marijuana")
    assert not second_hand(disc, "we found a potential association with lung cancer") and not second_hand(disc, "Our pooled analysis of cohort studies showed a statistically significant relationship") and not second_hand("Smoke from cannabis has many of the same toxins as tobacco smoke.", "Smoke from cannabis has many of the same toxins")
    assert second_hand("According to a study of women with difficulty achieving orgasm, cannabis use before partnered sex eased reaching orgasm.", "cannabis use before partnered sex eased reaching orgasm") and second_hand("In a review of recent studies, Kipping and Lynn found that moderate doses of cannabis improved female sexual function.", "moderate doses of cannabis improved female sexual function")
    assert second_hand("Smith et al. (2019) reported that half of the sample relapsed. They also noted cravings in most.", "They also noted cravings in most") and not second_hand("Results from this study indicated that both men and women see benefits.", "both men and women see benefits") and not second_hand("Men and women reported benefits.", "Men and women reported benefits")
    assert second_hand(disc, "long-term marijuana use (over 10 years) was associated with an increased risk of testicular germ cell tumors").startswith("A meta-analysis in 2019 evaluated")          # (lane 17) it says which earlier work
    # (lane 18) "A 2023 survey found ... A 2024 review reports ...": the second sentence says who reports it, so the rule has nothing against the first sentence's "found"
    assert not rules([{"part": "short", "text": "A 2023 survey found cannabis tends to improve perceived sexual satisfaction. A 2024 review reports that moderate doses improved female sexual function.", "uses": ["F5", "F1"]}], {"F5": {"quote": "x", "second_hand": ""}, "F1": {"quote": "y", "second_hand": "In a review of recent studies, Kipping and Lynn found"}}, years=[2023, 2024])
    # (lane 18) what people perceive or say of themselves, said as what is
    Lp = {"F5": {"quote": "Overall, cannabis use tends to have a positive influence on perceived sexual functioning and satisfaction for individuals despite gender or age", "passage_text": ""}}
    told = says_more([{"part": "how3", "text": "A 2023 online survey of adults who used cannabis found it tends to positively influence sexual functioning and satisfaction.", "uses": ["F5"]}], Lp)
    assert len(told) == 1 and "perceived sexual functioning" in told[0][1] and "Keep the word" in told[0][1], told
    assert not says_more([{"part": "how3", "text": "A 2023 online survey found it tends to positively influence perceived sexual functioning.", "uses": ["F5"]}], Lp)
    assert not says_more([{"part": "how3", "text": "In a 2023 online survey, people said cannabis tended to make their sexual functioning better.", "uses": ["F5"]}], Lp)
    assert not says_more([{"part": "how3", "text": "A 2023 online survey was of adults who had used cannabis.", "uses": ["F5"]}], Lp)          # it does not name the thing: nothing to say
    assert not rules([{"part": "how2", "text": "A 2026 review found a potential link between smoking marijuana and lung cancer, and reports a link to testicular tumors from an earlier meta-analysis.", "uses": ["F2", "F4"]}], {"F2": {"quote": "x"}, "F4": {"quote": "y", "second_hand": "A meta-analysis in 2019 found"}}, years=[2026])
    cp = checker_prompt([{"part": "short", "text": ok_short, "uses": ["F1"]}, {"part": "but", "text": "B.", "uses": ["F1"]}], lab1, question="Can you get addicted to ketamine?")
    assert "does the answer (the opening word “Yes” followed by sentence 1) answer that QUESTION itself" in cp
    L2 = {"F2": {"quote": "a potential association between marijuana smoking and an increased risk of lung cancer", "second_hand": ""}, "F4": {"quote": "long-term marijuana use (over 10 years) was associated with an increased risk of testicular germ cell tumors", "second_hand": "A meta-analysis in 2019 evaluated the association"}}
    told = rules([{"part": "how2", "text": "A 2026 review found a potential link between smoking marijuana and lung cancer, and long-term use over 10 years and testicular tumors.", "uses": ["F2", "F4"]}], L2, years=[2026])
    assert len(told) == 1 and "what that source only reports from another study (F4)" in told[0][1], told
    assert not rules([{"part": "how2", "text": "A 2026 review found a potential link between smoking marijuana and lung cancer. It cites an earlier analysis that linked long-term use over 10 years to testicular tumors.", "uses": ["F2", "F4"]}], L2, years=[2026])
    assert not rules([{"part": "how2", "text": "A 2026 review found a potential link between smoking marijuana and lung cancer.", "uses": ["F2"]}], L2, years=[2026]) and not rules([{"part": "short", "text": "In one study, long-term use was linked to testicular tumors.", "uses": ["F4"]}], L2)
    assert "IT REPORTS THIS FROM ANOTHER STUDY" in writer_prompt("Q?", [{"read": "full", "tag": "A", "title": "T", "year": 2026, "kind": "review", "design": None, "findings": [{"id": "F4", "text": "x", "quote": "y", "second_hand": True}, {"id": "F2", "text": "x", "quote": "y", "second_hand": False}], "limits": []}], ex).split("[F4]")[1].split("[F2]")[0]
    # ---------- lane 19 ----------
    # a number that stands in another item of the same source: the item is added to what the sentence rests on, and the answer is not lost for it
    calls.clear(); script["writer"] = [W("Yes. In 2,405 people who used ketamine regularly, between 9% and 27% met criteria for dependence.")]; script["checker"] = [V(True, True, True, True)]
    r = mk(); assert r["status"] == "published" and "short + DA (2405)" in r["gates"]["mended"] and [x["label"] for x in r["parts"][0]["rests_on"]] == ["F1", "DA"], (r["status"], r["why"], r["gates"])
    assert "Across 12 studies of 2,405 people" in [c for c in calls if c[0] == "checker"][0][2].split("2. SENTENCE")[0]                    # the second reader reads the sentence beside that item too
    Lm = {"F1": {"quote": "anxiety fell", "ref": "a"}, "DA": {"quote": "16 healthy participants were scanned", "ref": "a"}, "DB": {"quote": "a survey of 40 adults", "ref": "b"}}
    pm = [{"part": "short", "text": "In 16 healthy people anxiety fell, as in 40 adults elsewhere.", "uses": ["F1"]}]
    assert mend_uses(pm, Lm) == [("short", "DA", "16")] and pm[0]["uses"] == ["F1", "DA"]                                               # never an item of another source: the 40 stays against the rule
    told = rules(pm, Lm); assert len(told) == 1 and "(40): it stands in [DB]; name that item too" in told[0][1], told
    assert mend_uses([{"part": "short", "text": "A 2021 review found it in 16 people.", "uses": ["F1"]}], Lm, years=[2021]) == [("short", "DA", "16")]      # a year is not mended (the rule on years judges it)
    # "male rats" is no result for men; a result for men still is
    assert not [k for k, w, h in says_more_text("It reduced anxiety in healthy people.", "Sceletium reduced anxiety in male Wistar rats and in female mice. The extract promoted calmness.") if "said of people" in k]
    assert [k for k, w, h in says_more_text("It reduced anxiety in healthy people.", "In 20 healthy men the extract reduced anxiety.") if "said of people" in k] == ["a result for men, said of people"]
    assert ANIMAL_SEX.search("in male Sprague-Dawley rats") and ANIMAL_SEX.search("female mice") and not ANIMAL_SEX.search("male and female students") and not ANIMAL_SEX.search("in males aged 18 to 25")
    # a writer that gives no answer in the form asked for: the team's other writer writes from there, and the record says so
    def chat_w(model, messages, max_tokens=0):
        if model == "gemini:gemma-4-26b-a4b-it": calls.append(("writer", model, "")); return "Let me think about this question at length. " * 40
        return chat(model, messages, max_tokens)
    calls.clear(); script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True)]
    r = make(item, found, chat_w, Enc(), dict(MODELS, writer="gemini:gemma-4-26b-a4b-it", writer_2="groq:qwen/qwen3.8-27b"), fulltext=lambda pmcid: xml, crossref=crossref, ex=ex)
    assert r["status"] == "published" and r["made"]["models"]["writer"] == "groq:qwen/qwen3.8-27b" and r["made"]["models"]["writer_first"] == "gemini:gemma-4-26b-a4b-it" and "gave no answer in the form asked for: qwen3.8-27b wrote from there" in r["gates"]["writer"], (r["status"], r["why"], r["gates"])
    assert [c[1] for c in calls if c[0] == "writer"] == ["gemini:gemma-4-26b-a4b-it", "groq:qwen/qwen3.8-27b"]
    script["writer"] = []; r = make(item, found, chat_w, Enc(), dict(MODELS, writer="gemini:gemma-4-26b-a4b-it"), fulltext=lambda pmcid: xml, crossref=crossref, ex=ex)
    assert r["status"] == "none" and "no JSON" in r["why"] and r["soft"], (r["status"], r["why"], r.get("soft"))                         # no other writer: no answer, and the fault is noted as not the answer's (tried again in the next run)
    def chat_down(model, messages, max_tokens=0):
        if model == "groq:qwen/qwen3.8-27b" and messages[0]["content"].startswith("You write"): raise llm.Unavailable("groq answered 503")
        return chat(model, messages, max_tokens)
    script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True)]
    r = make(item, found, chat_down, Enc(), dict(MODELS, writer="groq:qwen/qwen3.8-27b", writer_2=MODELS["writer"]), fulltext=lambda pmcid: xml, crossref=crossref, ex=ex)
    assert r["status"] == "published" and "could not be asked (groq answered 503)" in r["gates"]["writer"], (r["status"], r["why"], r["gates"])
    # a further reader that cannot be asked: the answer is kept, not shown, and marked to be worked on again by itself (not parked for a person)
    calls.clear(); script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True)]
    r = make(item, found, chat_gap, Enc(), M2, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex)
    assert r["status"] == "waiting" and r["for"] == "again" and r["soft"] and "worked on again by itself" in r["why"], (r["status"], r["why"], r.get("for"))
    # how much is needed for an effect: refused as a rule, in any part; what tolerance is, and what a drug does at low and at high amounts, are not
    nf = lambda s: [w for _, w in rules([{"part": "but", "text": s, "uses": []}], {})]
    assert any(w.startswith("how much is needed for an effect") for w in nf("Relatively large amounts of kratom need to be consumed before a noticeable psychoactive effect occurs.")) and any(w.startswith("how much is needed") for w in nf("It takes a large amount to feel anything."))
    assert not nf("With tolerance, higher doses are needed to feel the same effect.") and not nf("The mix depends on the dose, with stimulant effects at low amounts and opioid effects at higher doses.") and not nf("Larger doses produce more pronounced psychoactive effects.")
    # a run that waits behind this one: counted from what GitHub says; none where it cannot be asked
    class GH:
        def __init__(self, out, code=0): self.stdout, self.returncode = out, code
    assert runs_waiting(lambda *a, **k: GH('[{"status":"in_progress"},{"status":"pending"},{"status":"completed"},{"status":"queued"}]')) == 2 and runs_waiting(lambda *a, **k: GH('[{"status":"in_progress"}]')) == 0
    assert runs_waiting(lambda *a, **k: GH("", 1)) == 0 and runs_waiting(lambda *a, **k: GH("not json")) == 0 and runs_waiting(lambda *a, **k: (_ for _ in ()).throw(OSError("no gh"))) == 0
    # which version the editor holds: the one a named run wrote, or every version up to a lane
    hl = [{"id": "au_w_1", "lane": 19, "run": "77"}, {"id": "au_w_2", "lane": 18}, "au_w_3"]
    assert is_held({"id": "au_w_1", "lane": 19, "made": {"run": "77"}}, hl) and not is_held({"id": "au_w_1", "lane": 19, "made": {"run": "78"}}, hl) and is_held({"id": "au_w_2", "lane": 18, "made": {"run": "5"}}, hl)
    assert not is_held({"id": "au_w_2", "lane": 19}, hl) and not is_held({"id": "au_w_9", "lane": 1}, hl) and not is_held(None, hl)
    # the editor's note goes to the writer
    calls.clear(); script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True)]
    r = make(item, found, chat, Enc(), MODELS, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex, note="say what people report, as reports")
    assert r["status"] == "published" and "AN EDITOR READ AN EARLIER ANSWER" in [c for c in calls if c[0] == "writer"][0][2] and "say what people report, as reports" in [c for c in calls if c[0] == "writer"][0][2]
    # what the readers said of the last draft that fell goes to the writer of the next one (only of this lane, only a reader's word on the short answer or the But)
    fell = {"status": "none", "lane": LANE, "tries": [{"try": 1, "parts": [{"part": "short", "text": "Old.", "ok": False, "by": "a rule", "said": "a rule: x"}]},
            {"try": 3, "why": "the last draft: no answer", "parts": [{"part": "short", "text": "People who use it report better sleep.", "ok": False, "by": "a further reader", "said": "a further reader (x) did not accept it: the passage says 'potential' only"},
                                                                   {"part": "but", "text": "B.", "ok": True}, {"part": "how1", "text": "H.", "ok": False, "by": "the second reader", "said": "no"}]}]}
    lr = last_refusal(fell)
    assert lr.startswith("the short answer “People who use it report better sleep.”: a further reader (x) did not accept it") and "B." not in lr and "H." not in lr and "Old." not in lr, lr
    assert last_refusal(dict(fell, lane=LANE - 1)) == "" and last_refusal(dict(fell, status="published")) == "" and last_refusal(None) == "" and last_refusal({"status": "none", "lane": LANE}) == ""
    assert last_refusal({"status": "none", "lane": LANE, "tries": [{"parts": [{"part": "short", "text": "S.", "ok": False, "by": "a rule", "said": "a rule: an amount"}]}]}) == ""
    calls.clear(); script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True)]
    r = make(item, found, chat, Enc(), MODELS, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex, last=lr)
    wp = [c for c in calls if c[0] == "writer"][0][2]
    assert r["status"] == "published" and "ITS READERS DID NOT ACCEPT IT" in wp and "the passage says 'potential' only" in wp and r["gates"]["told"].startswith("the writer was told"), (r["status"], r["gates"])
    calls.clear(); script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True)]
    r = mk(); assert "ITS READERS DID NOT ACCEPT IT" not in [c for c in calls if c[0] == "writer"][0][2] and "told" not in r["gates"]
    # a question where a wrong word can hurt. The setting decides (data/auto/lane/policy.json, "stakes"); with none, it waits for a person, as before
    kq = {"id": "w_0027", "q": "Can ketamine kill you?", "ways": []}; VD = lambda down: dict(V(True, True, True, True), plays_down=down)
    strict = lambda models=None, q=kq, **k: make(q, found, chat, Enc(), models or dict(MODELS, also1="gemini:gemini-3.6-flash"), fulltext=lambda pmcid: xml, crossref=crossref, ex=ex, stakes_how={"dying": "strict", "overdose or an emergency": "strict", "suicide or self-harm": "person"}, **k)
    calls.clear(); script["writer"] = [W(ok_short)]; script["checker"] = [VD(False), VD(False)]
    r = strict(); assert r["status"] == "published" and r["stakes"] == "dying" and "the stricter bar for such an answer: met" in r["gates"]["stakes"] and "stricter bar for an answer about dying" in r["why"], (r["status"], r["why"], r["gates"])
    assert all("\"plays_down\": true if sentence 1 or sentence 2" in c[2] and "This answer is about dying" in c[2] for c in calls if c[0] == "checker") and len([c for c in calls if c[0] == "checker"]) == 2     # the second reader and the further reader are both asked
    script["writer"] = [W(ok_short)]; script["checker"] = [VD(False), VD(True)]
    r = strict(); assert r["status"] == "none" and "does not meet the stricter bar" in r["why"] and "a reader found that its lead can be read as saying a danger is small or absent" in r["why"] and r["parts"], (r["status"], r["why"])
    script["writer"] = [W(ok_short)]; script["checker"] = [VD(False), V(True, True, True, True)]                                        # a reader that gave no word on it: not published by the system
    r = strict(); assert r["status"] == "none" and "gave no clear word on whether its lead plays a danger down" in r["why"], (r["status"], r["why"])
    script["writer"] = [W(ok_short)]; script["checker"] = [VD(False)]                                                                   # a team with no further reader: never by itself
    r = strict(models=dict(MODELS)); assert r["status"] == "none" and "no further reader read it" in r["why"], (r["status"], r["why"])
    script["writer"] = [W("No. In a review of studies, between 9% and 27% of people who used ketamine regularly met criteria for dependence.")]; script["checker"] = [VD(False), VD(False)]
    r = strict(); assert r["status"] == "none" and "the question asks about a danger, and the answer opens with “No”" in r["why"], (r["status"], r["why"])
    script["writer"] = [W(ok_short, but="Deaths are rare, and most studies were online surveys of volunteers.")]; script["checker"] = [VD(False), VD(False)]
    r = strict(); assert r["status"] == "none" and "its but holds words that can be read as saying a danger is small or absent (“rare”)" in r["why"], (r["status"], r["why"])
    script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True), V(True, True, True, True)]                         # what to do in an emergency is the senior author's own text: it waits, whatever the setting
    r = strict(q={"id": "w_0031", "q": "What should I do if someone overdoses on ketamine?", "ways": []}); assert r["status"] == "waiting" and r["for"] == "editor" and "overdose or an emergency" in r["why"], (r["status"], r["why"])
    script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True), V(True, True, True, True)]                         # a kind the setting gives to a person
    r = strict(q={"id": "w_0032", "q": "Does ketamine help with suicidal thoughts?", "ways": []}); assert r["status"] == "waiting" and r["for"] == "editor" and "suicide" in r["why"], (r["status"], r["why"])
    script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True), V(True, True, True, True)]                         # a kind the setting does not name (mixing): a person, as before
    r = strict(q={"id": "w_0033", "q": "Can you mix ketamine and alcohol?", "ways": []}); assert r["status"] == "waiting" and "mixing drugs" in r["why"], (r["status"], r["why"])
    assert plays_down("Is it safe to mix ketamine and alcohol?", [{"part": "short", "text": "Yes. Many people do."}]) and not plays_down("Is it safe to mix ketamine and alcohol?", [{"part": "short", "text": "No. Both slow breathing."}])
    assert plays_down("Can I take ketamine with alcohol?", [{"part": "short", "text": "Yes, it has been done."}]) and plays_down("Can you die from ketamine?", [{"part": "short", "text": "No. It has not been reported."}]) and not plays_down("Can you die from ketamine?", [{"part": "short", "text": "Yes. Deaths have been reported."}])
    assert plays_down("Can ketamine harm a baby?", [{"part": "short", "text": "It can. Studies in animals found harm."}, {"part": "but", "text": "The risk in people is unlikely to be large."}]) and not plays_down("x", [{"part": "how1", "text": "A review found deaths were rare."}])     # (the lead only: a line under How do we know reports what a source found)
    assert not plays_down("What side effects does kratom have?", [{"part": "short", "text": "Reported side effects include nausea. Rare but serious effects include seizures."}]) and plays_down("x", [{"part": "short", "text": "Seizures are rare."}])     # a source's own "rare but serious" warns
    script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True), {"pairs": [{"n": 1, "is": "differs", "why": "x"}]}]
    cl = lambda drugs: [{"id": "cl_ket_dependence", "drug": "ketamine", "plain": "People who use ketamine often can become dependent on it.", "statement": ""}]
    r = make(dict(item, drugs=["ketamine"]), found, chat, Enc(), MODELS, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex, claims=cl, agreed=("cl_ket_dependence",))
    assert r["status"] == "published" and r["with_checked"]["differs"] == [] and r["with_checked"]["editor_found_both_can_hold"][0]["claim"] == "cl_ket_dependence", (r["status"], r["why"], r.get("with_checked"))     # the editor's word on a disagreement: that claim does not stop the answer
    assert NEVER_ALONE.search("what to do if a friend overdoses") and NEVER_ALONE.search("How do I help someone who took too much GHB?") and NEVER_ALONE.search("does narcan work on fentanyl") and not NEVER_ALONE.search("Can you overdose on ketamine?")
    # a reader's reply is read as it was given: the list alone, a verdict as a word, no numbers
    assert [v["supported"] for v in verdicts_json('[{"n":1,"supported":true,"problem":""},{"n":2,"supported":false,"problem":"x"}]')["verdicts"]] == [True, False]
    assert verdicts_json('{"verdicts": [{"n": "1", "supported": "true"}, {"n": "2", "supported": "no", "problem": "y"}], "opening": true}')["verdicts"][1] == {"n": 2, "supported": False, "problem": "y"}
    assert [v["n"] for v in verdicts_json('```json\n[{"supported": true}, {"supported": true}, {"supported": false}]\n```')["verdicts"]] == [1, 2, 3] and verdicts_json("I cannot say.") is None and verdicts_json('{"x": 1}') == {"x": 1}
    calls.clear(); script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True), V(True, True, True, True)["verdicts"]]          # a further reader that answers with the list alone has read the answer
    r = make(item, found, chat, Enc(), dict(MODELS, also1="gemini:gemini-3.5-flash-lite"), fulltext=lambda pmcid: xml, crossref=crossref, ex=ex)
    assert r["status"] == "published" and r["panel"]["gemini:gemini-3.5-flash-lite"]["short"] == [True, ""] and not r.get("panel_gap"), (r["status"], r["why"], r.get("panel"))
    # when a question's turn comes
    yday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat(); wk = (datetime.date.today() - datetime.timedelta(days=9)).isoformat()
    sent, own_q = {"id": "w_a1", "from": "a question visitors sent"}, {"id": "w_1"}
    S = lambda **k: {"w_a1": dict({"lane": LANE, "last": TODAY, "tries": 1, "n": 1, "had": 0}, **k), "w_1": dict({"lane": LANE, "last": TODAY, "tries": 1, "n": 1, "had": 0}, **k)}
    assert turn_of(sent, {}) == 0 and turn_of(sent, S(status="none", why="x", soft="a fault of the network")) == 0.5 and turn_of(sent, S(status="none", why="x", soft="y", n=SOFT_A_DAY)) is None     # a fault that was not the answer's: again in the next run, six times a day at most
    fs = "a source could not be fetched"; nf = "no source that can be read gave a finding for this question (1 source(s) could not be fetched just now: tried again in the next run)"
    assert turn_of(sent, S(status="none", why=nf, soft=fs)) == 0.5 and turn_of(sent, S(status="none", why=nf, soft=fs, n=SOFT_FETCH_A_DAY)) is None                   # the index did not answer: the next run, three times a day
    assert turn_of(sent, S(status="none", why=nf, soft=fs, tries=SOFT_FETCH_TRIES + 1)) is None and turn_of(sent, S(status="none", why=nf, soft=fs, tries=SOFT_FETCH_TRIES + 1, last=wk)) == 3   # try after try: no fault of the moment any more
    assert turn_of(sent, S(status="waiting", **{"for": "again"})) == 0.5 and turn_of(sent, S(status="waiting", **{"for": "editor"})) is None and turn_of(sent, S(status="waiting", **{"for": "editor"}, lane=LANE - 1)) is None
    assert turn_of(sent, S(status="none", why="the second reader did not accept the answer")) == 2.5 and turn_of(sent, S(status="none", why="x", n=2)) == 2.5 and turn_of(sent, S(status="none", why="x", n=3)) is None      # the same day, by another team: three tries for a question a person sent
    assert turn_of(own_q, S(status="none", why="x")) == 2.5 and turn_of(own_q, S(status="none", why="x", n=2)) is None                                                                                  # two for the system's own
    assert turn_of(sent, S(status="none", why="no source that can be read gave a finding for this question")) is None and turn_of(sent, S(status="none", why="no source that can be read gave a finding", last=yday)) == 3
    assert turn_of(sent, S(status="none", why="x", last=yday, tries=3)) == 3 and turn_of(sent, S(status="none", why="x", last=yday, tries=6)) is None and turn_of(sent, S(status="none", why="x", last=wk, tries=20)) == 3   # every day at first, then further apart
    assert turn_of(sent, S(status="none", why="x", lane=LANE - 1)) == 1 and turn_of(sent, S(status="waiting", lane=LANE - 1)) == 1 and turn_of(sent, S(status="published", lane=LANE - 1)) == 4 and turn_of(sent, S(status="published", complete=True)) is None
    assert [wait_days(n) for n in (1, 4, 5, 8, 9, 14, 15)] == [1, 1, 2, 2, 4, 4, 7]
    # ---- 19 November 2026: sources read at once, kept in their own order; the clock ----
    found4 = {"can_read": [{"doi": f"10.1000/k.{i}", "pmcid": f"PMC{i}", "title": f"Ketamine dependence: review {i}", "year": 2022, "journal": "Addiction", "kind": "review", "people": True, "near": 0.71 - i / 100} for i in (1, 2, 3, 4)], "wanted": []}
    slow_first = lambda pmcid: (time.sleep(0.35) if pmcid == "PMC1" else None) or xml              # the nearest paper comes back last
    answer = lambda **k: (script.update(writer=[W(ok_short)], checker=[V(True, True, True, True)]), calls.clear(), make(item, found4, chat, Enc(), MODELS, fulltext=slow_first, crossref=crossref, ex=ex, **k))[2]
    one_by_one = answer(); n_one = sum(c[0] == "reader" for c in calls)
    at_the_same_time = answer(at_once=4); n_same = sum(c[0] == "reader" for c in calls)
    same = lambda r: (r["status"], [(s["doi"], s["tag"], s["ref"]["id"]) for s in r["sources"]], [p["text"] for p in r["parts"]], [x["at"] for x in r["looked"]])
    assert one_by_one["status"] == "published" and same(one_by_one) == same(at_the_same_time), (same(one_by_one), same(at_the_same_time))      # the same answer, from the same sources in the same order
    assert [x["at"] for x in at_the_same_time["looked"]] == ["10.1000/k.1", "10.1000/k.2"] and n_one == 2 and n_same == 4, (n_one, n_same)        # two more were read ahead and put aside: the record holds the two the answer needed
    # a source that is not read in the time the reading has: written down as not read, and the answer is written from the rest
    stuck = lambda pmcid: (time.sleep(3) if pmcid == "PMC2" else None) or xml
    script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True)]; t0 = time.time()
    r = make(item, dict(found4, can_read=found4["can_read"][:2]), chat, Enc(), MODELS, fulltext=stuck, crossref=crossref, ex=ex, at_once=4, read_secs=0.6)
    assert r["status"] == "published" and time.time() - t0 < 2.5 and [s["doi"] for s in r["sources"]] == ["10.1000/k.1"] and "1 source(s) were not read" in r["gates"]["time"], (r["status"], r["why"], r["gates"].get("time"), time.time() - t0)
    assert [x.get("fault") for x in r["looked"]] == [None, "it was not read: the time this run has for reading was over"] and r["looked"][1]["at"] == "10.1000/k.2", r["looked"]
    r = make(item, dict(found4, can_read=found4["can_read"][1:2]), chat, Enc(), MODELS, fulltext=stuck, crossref=crossref, ex=ex, at_once=4, read_secs=0.5, summary=lambda doi: None)
    assert r["status"] == "none" and r["soft"] == "a source could not be fetched" and "1 of them for want of time" in r["why"], (r["status"], r["why"])            # nothing was read in time: not the answer's fault, tried again in the next run
    # the readers of the pool read side by side with the team's own; never the model that writes or the second reader; one that cannot be asked costs nothing
    pl = [{"model": "pool:one", "secs": 1}, {"model": MODELS["writer"], "secs": 1}, {"model": MODELS["checker"], "secs": 1}, {"model": "pool:down", "secs": 0.1}]
    def chat_pool(model, messages, max_tokens=0):
        if model == "pool:down": raise llm.Unavailable("pool answered 503")
        return chat(model, messages, max_tokens)
    script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True)]; calls.clear()
    r = make(item, found4, chat_pool, Enc(), MODELS, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex, at_once=4, pool=pl)
    who = {c[1] for c in calls if c[0] == "reader"}
    assert r["status"] == "published" and who <= {MODELS["reader"], "pool:one"} and len(who) == 2 and set(r["made"]["read_by"]) == {base(MODELS["reader"]), "pool:one"} and "reader" not in r["gates"], (r["status"], r["why"], who, r["made"].get("read_by"))
    assert same(r)[1:3] == same(one_by_one)[1:3]                                                                                                       # whoever read: the same sources in the same order, the same answer
    # the clock: a model that cannot be asked in time ends the question for this run (Late), and nothing is waited for
    def chat_late(model, messages, max_tokens=0):
        if messages[0]["content"].startswith("You write"): raise llm.Late("the time for this question was over before the writer could be asked")
        return chat(model, messages, max_tokens)
    try: make(item, found4, chat_late, Enc(), MODELS, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex, at_once=4); raise AssertionError("the writer was late, and the answer went on")
    except llm.Late: pass
    def chat_read_late(model, messages, max_tokens=0):
        if messages[0]["content"].startswith("You read") and "review 2" in messages[1]["content"]: raise llm.Late("the time for this question was over before the reader could be asked")
        return chat(model, messages, max_tokens)
    script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True)]
    r = make(item, dict(found4, can_read=found4["can_read"][:2]), chat_read_late, Enc(), MODELS, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex, at_once=4)
    assert r["status"] == "published" and [s["doi"] for s in r["sources"]] == ["10.1000/k.1"] and r["looked"][1].get("fault", "").startswith("it was not read"), (r["status"], r["why"], r["looked"])
    b1 = Begun([lambda: 1, lambda: (_ for _ in ()).throw(ValueError("x")), lambda: 3]); o = b1.all(); assert o[0] == 1 and o[1][0] == "error" and isinstance(o[1][1], ValueError) and o[2] == 3
    b2 = Begun([lambda: time.sleep(2) or 1, lambda: 2], threading.Semaphore(2), time.time() + 0.3); assert b2.all() == [("late",), 2]
    print("lane selftest: ok (published with every sentence tied to the paper's own words; a retracted paper never read; quotes that are not in the paper and numbers that are not in the quote thrown away; "
          "a broken rule written again; a refused line dropped; a refused short answer means no answer; a question about dying waits for a person; one study alone is not enough; a nearer paper that cannot be read means not complete; "
          "an official body's page is a source and is named; a review behind a paywall is read in summary and the answer says so; an answer about amounts holds only the sources' own words, 15 at most, under the lines the code writes, "
          "with the line about tolerance first for an opioid, and nothing from animals, harm or timing; the answer it replaces is kept in its history; "
          "sources read at once give the same answer from the same sources in the same order; a source not read in time is written down and the answer is written from the rest; past its clock a question is put down for the next run)")


if __name__ == "__main__":
    if "--selftest" in sys.argv: selftest()
    elif len(sys.argv) > 1 and sys.argv[1] == "requests":
        # the requests waiting in data/auto/requests (lane-*.json: {"ids": [...], "max": N, "again": true}), each taken off when read.
        # A request is a file in the repository, written by the editor: read as data, never run.
        ids, limit, again, any_req, only_team, trial, mins = [], 3, False, False, None, [], None
        for f in sorted((ROOT / "data" / "auto" / "requests").glob("lane-*.json")):
            try: r = json.load(open(f, encoding="utf-8"))
            except ValueError: r = {}
            any_req = True; ids += [x for x in (r.get("ids") or []) if isinstance(x, str) and re.fullmatch(r"w_[a-z0-9_]{1,40}", x)]
            if isinstance(r.get("max"), int): limit = max(1, min(20, r["max"]))
            if isinstance(r.get("minutes"), (int, float)) and 1 <= r["minutes"] <= 40: mins = float(r["minutes"])      # ("minutes": 8: the pass is on the clock, as a run of the Auto workflow is)
            again = again or r.get("again") is True
            if isinstance(r.get("team"), str) and re.fullmatch(r"[A-Za-z0-9 ]{1,24}", r["team"]): only_team = r["team"]      # ("team": "team G": only that team of data/auto/lane/models.json)
            trial += trial_items(r.get("trial"))                              # ("trial": [{"id": "t_...", "q": "...", "drugs": ["lsd"]}]: questions that are not on the site's list; see trial_items)
            f.unlink()
        if trial: run(limit=len(trial), only_team=only_team, trial=trial, minutes=mins)
        if any_req and (ids or not trial): run(ids=ids or None, limit=max(limit, len(ids)) if ids else limit, again=again, only_team=only_team, minutes=mins)
        else: print("lane: no request waiting")
    elif len(sys.argv) > 1 and sys.argv[1] == "run":
        a = sys.argv[2:]; opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
        run(ids=[x for x in (opt("--ids") or "").split(",") if x] or None, limit=int(opt("--max", "3")), again="--again" in a, minutes=float(opt("--minutes")) if opt("--minutes") else None, only_sent="--sent" in a, give_way=runs_waiting if "--give-way" in a and "--sent" not in a else None)
    elif len(sys.argv) > 1 and sys.argv[1] == "waiting":      # for the workflow: exit 0 where a run waits behind this one, 1 where none does (or it cannot be asked)
        n = runs_waiting(); print(f"lane: {n} run(s) waiting behind this one"); sys.exit(0 if n else 1)
    else: sys.exit(__doc__)
