#!/usr/bin/env python3
"""lane.py: the machine lane. Answers written by the system from papers it found and read (docs/AUTOMATION.md).

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
  6 sources  GATE at least one review or meta-analysis, or two studies in people, each with a Crossref record made by
             scripts/build_references.py; a retracted paper, or one under an expression of concern, is never used.
  7 stakes   A question about dying, overdose, an emergency, mixing two drugs, pregnancy, children or suicide is written
             and then WAITS FOR A PERSON: it is not published by the system (the editor's rule; emergency guidance is the
             senior author's own domain). Everything else that passed is published with the label.

What it writes: data/auto/answers/<id>.json (the answer; every sentence with the passages it rests on, kept short, for the
person who checks; the papers; the models; what each gate said; "published", "waiting" or "none", and why), the papers it
still wants (data/auto/papers-wanted.json, in APA 7), and data/auto/lane/state.json. The site shows only "published"
answers (site/build.js), each with "Written by our system from N papers. Not yet checked by a person." and, where papers
were missing, "Not complete yet".
"""
import sys, os, re, json, hashlib, pathlib, datetime, unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); sys.path.insert(0, str(ROOT / "scripts" / "insight"))
import papers as P, llm

OUT = ROOT / "data" / "auto" / "answers"
STATE = ROOT / "data" / "auto" / "lane" / "state.json"
MODELS_FILE = ROOT / "data" / "auto" / "lane" / "models.json"
WANTED = ROOT / "data" / "auto" / "papers-wanted.json"
MODELS = {"reader": "@cf/qwen/qwen3-30b-a3b-fp8", "writer": "@cf/meta/llama-3.3-70b-instruct-fp8-fast", "checker": "@cf/google/gemma-4-26b-a4b-it"}
N_PAPERS = 3            # papers read for one answer
N_PASSAGES = 9          # passages of a paper shown to the reader
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


def numbers(text):
    """The numbers a sentence states: every figure ("2,405" and "2405" are one number), the words for a share (half, twice,
    a third), and a number word where it counts something measured ("one in five", "three times"). Not "one study" or
    "two reviews": those count the sources, which the gate on sources counts itself."""
    t = (text or "").lower(); t = re.sub(r"(?<=\d),(?=\d{3}\b)", "", t)
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


READER_SYS = ("You read one research paper for Pharmakon, a drug encyclopedia for the public. You only copy what the paper itself says. "
              "You never add anything you know from elsewhere, and you never guess. You answer with JSON only.")


def reader_prompt(question, paper, picked):
    ps = "\n".join(f"[{p['n']}] ({p['where']}) {p['text'][:PASSAGE_CHARS]}" for p in picked)
    return (f"QUESTION that people ask: {question}\n\nPAPER: {paper['title']} ({paper.get('year') or 'n.d.'}), {paper.get('journal') or ''}.\n\n"
            f"PASSAGES of this paper (each is one paragraph, with its number and where it stands):\n{ps}\n\n"
            "TASK. From these passages only:\n"
            '1. "design": what kind of paper this is and who or what was studied, in one short phrase, with "quote": a part of ONE passage copied exactly, word for word (6 to 40 words), that shows it, and "passage": that passage\'s number.\n'
            '2. "findings": up to 5 things this paper found or concluded that help answer the question. For each: "passage" (its number), "quote" (a part of that passage copied exactly, word for word, 8 to 40 words, that states it), '
            '"finding" (the same thing in one plain sentence: no new facts, every number exactly as in the quote, and say "in rats", "in a laboratory" or "in one survey" when the quote does).\n'
            '3. "limits": up to 2 limits or uncertainties that the passages themselves state, each with "passage", "quote" (copied exactly) and "limit" (one plain sentence).\n'
            'Copy quotes exactly: do not correct, shorten in the middle or join two places. If nothing in the passages helps answer the question, return {"findings": []}.\n'
            'JSON only, in this form: {"design": {"text": "...", "quote": "...", "passage": 3}, "findings": [{"passage": 7, "quote": "...", "finding": "..."}], "limits": [{"passage": 9, "quote": "...", "limit": "..."}]}')


def read_gate(out, picked):
    """What of a reader's answer may be used: each item's quote must stand in a passage that was shown (GATE 1), and every
    number in its plain sentence must be in its quote (GATE 2). Returns (design or None, findings, limits, how many were thrown away)."""
    out = out if isinstance(out, dict) else {}
    by = {p["n"]: p for p in picked}; dropped = 0
    def place(item):
        q = str(item.get("quote") or "").strip()
        if not (5 <= words(q) <= 70): return None
        p = by.get(item.get("passage")) if isinstance(item.get("passage"), int) else None
        if not p or not found_in(q, p["text"][:PASSAGE_CHARS]): p = next((x for x in picked if found_in(q, x["text"][:PASSAGE_CHARS])), None)
        return (p, q) if p else None
    def one(item, key):
        nonlocal dropped
        if not isinstance(item, dict): dropped += 1; return None
        text = re.sub(r"\s+", " ", str(item.get(key) or "")).strip(); got = place(item)
        if not text or not got or not numbers(text) <= numbers(got[1]): dropped += 1; return None
        return {"passage": got[0]["n"], "where": got[0]["where"], "quote": got[1], "text": text}
    d = out.get("design"); design = one(d, "text") if isinstance(d, dict) else None
    fs = [x for x in (one(f, "finding") for f in (out.get("findings") or [])[:6]) if x]
    ls = [x for x in (one(l, "limit") for l in (out.get("limits") or [])[:3]) if x]
    return design, fs, ls, dropped


def read_paper(chat, model, question, paper, picked):
    for attempt in range(2):
        raw = chat(model, [{"role": "system", "content": READER_SYS}, {"role": "user", "content": reader_prompt(question, paper, picked) + ("" if not attempt else "\n\nYour last answer was not valid JSON. Answer with the JSON object only.")}], 900)
        out = llm.as_json(raw)
        if out is not None: return read_gate(out, picked)
    return None, [], [], 0


# ---------- 3 write ----------
WRITER_SYS = ("You write one answer for Pharmakon, a free drug encyclopedia that tells the public what research found, without judging. "
              "You write ONLY from the findings you are given: nothing from memory. You answer with JSON only.\n"
              "The rules of the site:\n"
              "- Plain words a 14-year-old can read. Short sentences. Lead the short answer with what people want to know.\n"
              "- Say who was studied when the findings say it (how many people, where, or that it was animals or a laboratory).\n"
              "- Keep every number exactly as the finding has it. Never claim more than the findings do: a link is not a cause; one study is not proof.\n"
              "- Never give amounts, doses, timing between uses, or ways of taking a drug. Never say how to make an effect stronger. No advice: never 'you should'. Never call anything 'safe'.\n"
              "- Person-first words: 'people who use cannabis', 'people with an alcohol use disorder'. Never 'users', 'addicts', 'abusers', 'abuse', 'alcoholics', 'clean'.\n"
              "- No quotation marks, no brackets with sources, no mention of 'findings', 'passages' or 'the paper says F1'.\n"
              "- If the findings do not answer the question, say plainly what they do show, and set \"complete\" to false.")


def writer_prompt(question, sources, examples, fix=""):
    lines = []
    for s in sources:
        lines.append(f"PAPER {s['tag']}: {s['title']} ({s.get('year') or 'n.d.'}). {('A review or meta-analysis.' if s['kind'] == 'review' else 'A single study.')}")
        if s.get("design"): lines.append(f"  [D{s['tag']}] what it is and who was studied: {s['design']['text']} (the paper's words: {s['design']['quote']})")
        for f in s["findings"]: lines.append(f"  [{f['id']}] {f['text']} (the paper's words: {f['quote']})")
        for l in s["limits"]: lines.append(f"  [{l['id']}] a limit the paper states: {l['text']} (the paper's words: {l['quote']})")
    ex = "\n\n".join(f"Question: {e['q']}\nshort: {e['short']}\nbut: {e['but']}\nhow: " + " | ".join(e["how"][:3]) for e in examples)
    return (f"QUESTION that people ask: {question}\n\nWHAT THE PAPERS FOUND (each item has a label in square brackets):\n" + "\n".join(lines) + "\n\n"
            "HOW THE SITE WRITES (three answers from the site, for the form only, not for their facts):\n" + ex + "\n\n"
            "TASK. Write the answer to the QUESTION from the labelled items only:\n"
            '- "short": the answer itself, 1 or 2 sentences, at most 45 words.\n'
            '- "but": the main limit or doubt, 1 sentence, at most 35 words. It must rest on a limit item or on what kind of study it was.\n'
            '- "how": 2 to 4 lines, one for each paper used, each at most 35 words: what kind of study, who was studied, what it found.\n'
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


def checker_prompt(parts, labels):
    blocks = []
    for n, p in enumerate(parts, 1):
        ps = "\n".join(f"   PASSAGE ({labels[u]['paper']}; {labels[u]['where']}): {labels[u]['passage_text'][:PASSAGE_CHARS]}" for u in p["uses"])
        blocks.append(f"{n}. SENTENCE: {p['text']}\n{ps}")
    return ("For each numbered SENTENCE below, decide whether its PASSAGES support it. Supported means ALL of this: everything the sentence says is stated in its passages; "
            "it is about the same people, animals or setting; every number is the same; it is not stronger or more certain than the passages; it does not say one thing causes another "
            "where the passages only report a link; it does not turn what one study found into a general fact. If any part of the sentence is not in the passages, it is not supported.\n\n"
            + "\n\n".join(blocks) +
            '\n\nJSON only, one verdict for every sentence, in this form: {"verdicts": [{"n": 1, "supported": true, "problem": ""}, {"n": 2, "supported": false, "problem": "what the passages do not say"}]}')


def check(chat, model, parts, labels):
    """[(supported?, problem)] for the parts, in order. A sentence without a clear verdict is not supported."""
    for attempt in range(2):
        out = llm.as_json(chat(model, [{"role": "system", "content": CHECKER_SYS}, {"role": "user", "content": checker_prompt(parts, labels)}], 120 + 90 * len(parts)))
        vs = {v.get("n"): v for v in (out or {}).get("verdicts") or [] if isinstance(v, dict)}
        if out is not None and all(isinstance(vs.get(n, {}).get("supported"), bool) for n in range(1, len(parts) + 1)):
            return [(vs[n]["supported"] is True, re.sub(r"\s+", " ", str(vs[n].get("problem") or ""))[:240]) for n in range(1, len(parts) + 1)]
    return [(False, "the checker gave no clear verdict")] * len(parts)


# ---------- 5 rules ----------
RULES = [
    ("an amount of a drug", re.compile(r"\b\d+(?:[.,]\d+)?\s?(?:mg|milligrams?|µg|ug|mcg|micrograms?|g|grams?|ml|millilit(?:re|er)s?|mg/kg|iu|ounces?|oz)\b|\b\d+(?:[.,]\d+)?\s?(?:pills?|tablets?|tabs?|capsules?|lines?|hits?|drops?|puffs?|joints?|shots?|bumps?|blotters?)\b", re.I)),
    ("timing between uses", re.compile(r"\bre-?dos\w*|\b(?:wait|space)\w*\s+(?:at least\s+)?\d|\bevery\s+\d+\s+(?:minutes?|hours?)\b|\b\d+\s+(?:minutes?|hours?)\s+(?:before|after|apart)\s+(?:taking|using|the (?:first|last|next))", re.I)),
    ("a way of taking compared for strength", re.compile(r"\b(?:snort\w*|inject\w*|smok\w*|swallow\w*|plugg\w*|boof\w*|vap\w*|eaten|eating)\b[^.]{0,70}\b(?:stronger|faster|harder|more intense|more potent|better high)\b|\b(?:stronger|faster|more intense|more potent)\b[^.]{0,50}\b(?:when|if)\s+(?:snorted|injected|smoked|swallowed|vaped|eaten)\b", re.I)),
    ("how to prepare or take a drug", re.compile(r"\b(?:crush(?:ed|ing)?|dissolv\w*|cook(?:ed|ing)? (?:it|the)|extract\w* (?:it|the)|filter\w* (?:it|the)|hold (?:it )?under the tongue|on an empty stomach)\b", re.I)),
    ("making an effect stronger", re.compile(r"\bpotentiat\w*|\b(?:boost|enhanc|intensif|strengthen)\w*\s+(?:the\s+)?(?:high|effects?|trip)\b|\bmak\w+\s+(?:it|the high|the effects?|the trip)\s+(?:stronger|last longer|more intense)\b", re.I)),
    ("advice or a promise of safety", re.compile(r"\byou\s+(?:should|must|need to|ought to|can safely|had better)\b|\b(?:it is|it's|is|are)\s+(?:completely |totally |perfectly |generally |relatively )?safe\b|\bsafe to\s+(?:take|use|mix|combine|drink|smoke)\b|\bharmless\b|\brisk-free\b|\bno risk\b|\bwe (?:recommend|advise|suggest)\b", re.I)),
    ("words that are not person-first", re.compile(r"\b(?:addicts?|junkies?|abusers?|alcoholics?|druggies?|crackheads?|stoners?|potheads?|users?)\b|\b(?:drug|substance|alcohol|opioid|cannabis|stimulant)\s+abuse\b|\babus(?:e|es|ed|ing)\s+(?:drugs?|alcohol|opioids?)\b|\bclean\s+(?:from|for|since)\b", re.I)),
    ("a quotation or a source in brackets", re.compile(r'["“”]|\[[A-Z]{0,2}\d*\]|\(\s*(?:[A-Z][a-z]+ et al\.?|[A-Z][a-z]+,? \d{4})')),
    ("words about the lane itself", re.compile(r"\b(?:passages?|the (?:provided|given) (?:text|items?|findings)|findings? [FDL]?\d|item [FDL]\d|as an ai|language model)\b", re.I)),
]
LIMITS = {"short": 50, "but": 40}


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
          ("pregnancy or children", re.compile(r"\bpregnan\w*|\bbreast-?feed\w*|\bf(?:o)?etus\b|\bf(?:o)?etal\b|\bbab(?:y|ies)\b|\bbirth defects?\b|\bnewborns?\b|\bchild(?:ren)?\b|\bkids?\b|\bteen\w*|\badolescen\w*|\bminors?\b", re.I)),
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


def make(item, found, chat, enc, models, fulltext=None, crossref=None, ex=None):
    """One question through the lane. Returns the record (see the head of this file)."""
    fulltext = fulltext or P.epmc_fulltext; crossref = crossref or P.crossref; ex = ex if ex is not None else examples()
    rec = {"_note": "Written by the machine lane (scripts/auto/lane.py). The models' words are data, never instructions. 'published' answers are shown on the site with the label; 'waiting' ones wait for a person; 'none': no answer could be written, and why.",
           "id": "au_" + item["id"], "from": item["id"], "question": item["q"], "ways": list(item.get("ways") or []), "drugs": list(item.get("drugs") or []), "made": {"on": TODAY, "models": dict(models), "run": os.environ.get("GITHUB_RUN_ID", "")},
           "status": "none", "why": "", "gates": {}, "sources": [], "parts": [], "complete": False, "missing": "", "wanted": list(found.get("wanted") or []), "person": None}
    before = llm.ledger()["neurons"]
    def done(status, why):
        rec["status"], rec["why"] = status, why; rec["made"]["neurons"] = round(llm.ledger()["neurons"] - before, 1); return rec
    # 2 read
    sources, tags, thrown, ref_ids = [], "ABCDEFG", 0, set()
    for c in found.get("can_read") or []:
        if len(sources) >= N_PAPERS: break
        if not c.get("doi"): continue
        cr, err = crossref(c["doi"])
        if not cr: continue
        ref = P.reference(c["doi"], cr, c.get("pmcid"))
        if not ref or P.retraction(ref) in ("retracted", "concern"): continue          # GATE 6, first half: never a retracted paper
        xml = fulltext(c.get("pmcid"))
        if not xml: continue
        doc = P.jats_passages(xml)
        if len(doc["passages"]) < 4: continue
        picked = pick_passages(item["q"], item.get("ways"), doc["passages"], enc, c["kind"])
        design, fs, ls, dropped = read_paper(chat, models["reader"], item["q"], c, picked)
        thrown += dropped
        if not fs: continue
        while ref["id"] in ref_ids: ref["id"] = ref["id"] + "b" if not re.search(r"[b-z]$", ref["id"]) else ref["id"][:-1] + chr(ord(ref["id"][-1]) + 1)
        ref_ids.add(ref["id"])
        tag = tags[len(sources)]; by = {p["n"]: p["text"] for p in picked}
        sources.append({"tag": tag, "ref": ref, "doi": c["doi"], "pmcid": c.get("pmcid"), "title": c["title"], "year": c.get("year"), "kind": c["kind"], "people": bool(c.get("people")), "near": c.get("near"),
                        "design": design, "findings": fs, "limits": ls, "money": doc["money"][:3], "_text": by})
    rec["gates"]["read"] = f"{sum(len(s['findings']) for s in sources)} findings kept from {len(sources)} papers; {thrown} thrown away (the quote was not in the passage, or a number was not in the quote)"
    if not sources: return done("none", "no paper that can be read gave a finding for this question")
    # GATE 6: one review or meta-analysis, or two studies in people
    reviews = sum(s["kind"] == "review" for s in sources); people = sum(s["kind"] != "review" and s["people"] for s in sources)
    rec["gates"]["sources"] = f"{reviews} review(s) or meta-analyses, {people} single studies in people"
    labels, n_f, n_l = {}, 0, 0
    for s in sources:
        paper = f"{s['title']} ({s['year']})"
        if s["design"]: labels["D" + s["tag"]] = dict(s["design"], paper=paper, ref=s["ref"]["id"], passage_text=s["_text"][s["design"]["passage"]])
        for f in s["findings"]: n_f += 1; f["id"] = f"F{n_f}"; labels[f["id"]] = dict(f, paper=paper, ref=s["ref"]["id"], passage_text=s["_text"][f["passage"]])
        for l in s["limits"]: n_l += 1; l["id"] = f"L{n_l}"; labels[l["id"]] = dict(l, paper=paper, ref=s["ref"]["id"], passage_text=s["_text"][l["passage"]])
    def keep_sources():
        rec["sources"] = [{k: v for k, v in s.items() if k != "_text"} for s in sources]
    keep_sources()
    if not reviews and people < 2: return done("none", "not enough sources: an answer needs one review or meta-analysis, or two studies in people")
    # 3 write, 5 rules (one more try when a rule is broken), 4 check (one more try for the short answer or the But)
    fix, draft, verdicts = "", None, []
    for attempt in range(3):
        out = llm.as_json(chat(models["writer"], [{"role": "system", "content": WRITER_SYS}, {"role": "user", "content": writer_prompt(item["q"], sources, ex, fix)}], 700))
        draft, why = draft_of(out, labels)
        if not draft: fix = "the form was wrong: " + why; continue
        bad = rules(draft["parts"], labels, [s["year"] for s in sources if s.get("year")])
        if bad: rec["gates"]["rules"] = "broken at try " + str(attempt + 1) + ": " + "; ".join(f"{p}: {w}" for p, w in bad); fix = "; ".join(f"in {p}: {w}" for p, w in bad); draft = None; continue
        verdicts = check(chat, models["checker"], draft["parts"], labels)
        head_bad = [(p["part"], v[1]) for p, v in zip(draft["parts"], verdicts) if not v[0] and p["part"] in ("short", "but")]
        if head_bad and attempt < 2: fix = "a second reader found that the paper's words do not support " + "; ".join(f"{p} ({w})" for p, w in head_bad) + ". Say only what the items say."; rec["gates"]["check"] = "not accepted at try " + str(attempt + 1) + ": " + fix; draft = None; continue
        break
    if not draft:
        return done("none", "no draft passed: " + (rec["gates"].get("check") or rec["gates"].get("rules") or fix))
    kept = [(p, v) for p, v in zip(draft["parts"], verdicts) if v[0]]
    dropped_how = [p["part"] for p, v in zip(draft["parts"], verdicts) if not v[0] and p["part"].startswith("how")]
    if any(not v[0] for p, v in zip(draft["parts"], verdicts) if p["part"] in ("short", "but")) or sum(p["part"].startswith("how") for p, _ in kept) < 1:
        rec["gates"]["check"] = "; ".join(f"{p['part']}: {'accepted' if v[0] else 'NOT accepted: ' + v[1]}" for p, v in zip(draft["parts"], verdicts))
        return done("none", "the second reader did not accept the answer")
    rec["gates"]["check"] = f"every sentence kept was accepted by the second reader ({models['checker']})" + (f"; {len(dropped_how)} How-do-we-know line(s) dropped" if dropped_how else "")
    rec["gates"].setdefault("rules", "nothing against it")
    if rec["gates"]["rules"].startswith("broken"): rec["gates"]["rules"] += "; written again, then nothing against it"
    parts = [p for p, _ in kept]; used_refs = []
    for p in parts:
        p["rests_on"] = [{"label": u, "ref": labels[u]["ref"], "where": labels[u]["where"], "quote": labels[u]["quote"], "sha": hashlib.sha256(norm(labels[u]["passage_text"]).encode("utf-8")).hexdigest()[:16]} for u in p["uses"]]
        for u in p["uses"]:
            if labels[u]["ref"] not in used_refs: used_refs.append(labels[u]["ref"])
    sources[:] = [s for s in sources if s["ref"]["id"] in used_refs]; keep_sources()
    reviews = sum(s["kind"] == "review" for s in sources); people = sum(s["kind"] != "review" and s["people"] for s in sources)
    if not reviews and people < 2: return done("none", "after the second reader's check the answer rests on too few sources")
    rec["parts"] = parts
    best_wanted = max([w.get("near") or 0 for w in rec["wanted"]] or [0]); best_read = max([s.get("near") or 0 for s in sources] or [0])
    rec["complete"] = bool(draft["complete"]) and not (rec["wanted"] and best_wanted > best_read)
    rec["missing"] = draft["missing"] if not draft["complete"] else ("a paper that stands nearer the question could not be read" if not rec["complete"] else "")
    why = stakes(item["q"], parts)
    if why: return done("waiting", "about " + why + ": written, and waiting for a person before it is published")
    return done("published", "passed every gate")


# ---------- the run ----------
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
    if MODELS_FILE.exists(): models.update({k: v for k, v in json.load(open(MODELS_FILE, encoding="utf-8")).items() if k in MODELS and isinstance(v, str)})
    chat = chat or llm.chat
    items = json.load(open(ROOT / "data" / "site" / "wanted.json", encoding="utf-8"))["items"]
    st = load_state(); order = []
    rep = ROOT / "data" / "auto" / "report.json"
    asked = {w["id"]: w.get("asked", 0) + w.get("sent_too", 0) for w in (json.load(open(rep, encoding="utf-8")).get("wanted") or [])} if rep.exists() else {}
    for w in sorted(items, key=lambda w: (-asked.get(w["id"], 0), w["id"])):       # what the most people wait for, first
        s = st["items"].get(w["id"]) or {}
        if ids:
            if w["id"] in ids: order.append(w)
        elif again or not s or (s.get("status") == "none" and s.get("last", "") < (datetime.date.today() - datetime.timedelta(days=7)).isoformat()): order.append(w)
    enc = enc or P.General(); import build_index as bi; names = bi.names_table(); made = []
    OUT.mkdir(parents=True, exist_ok=True); STATE.parent.mkdir(parents=True, exist_ok=True)
    for w in order[:limit]:
        pf = ROOT / "data" / "auto" / "papers" / (w["id"] + ".json")
        try:
            found = json.load(open(pf, encoding="utf-8")) if pf.exists() and not again else P.find(w, names, enc)
            if not pf.exists() or again: pf.parent.mkdir(parents=True, exist_ok=True); json.dump(found, open(pf, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            rec = make(w, found, chat, enc, models)
        except llm.Budget as e: print("lane: stopped for today:", e); break
        except llm.Unavailable as e: print("lane: the models cannot be used now:", e); break
        except P.Refused as e: print("lane: a source said no:", e); break
        json.dump(rec, open(OUT / (rec["id"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        st["items"][w["id"]] = {"status": rec["status"], "why": rec["why"], "last": TODAY, "tries": int((st["items"].get(w["id"]) or {}).get("tries") or 0) + 1}
        json.dump(st, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1); made.append(rec)
        print(f"lane: {w['id']} {w['q'][:56]!r}: {rec['status']} ({rec['why']}); {len(rec['sources'])} papers; {rec['made'].get('neurons', 0)} neurons")
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
    script = {"writer": [], "checker": []}; calls = []
    def chat(model, messages, max_tokens=0):
        sysm = messages[0]["content"]; role = "reader" if sysm.startswith("You read") else "writer" if sysm.startswith("You write") else "checker"; calls.append((role, model, messages[1]["content"]))
        llm.spend(model, 1000, 100, save=True)
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
    # 5. a question about dying: written, checked, and it waits for a person
    script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True)]
    r = mk({"id": "w_0027", "q": "Can ketamine kill you?", "ways": []}); assert r["status"] == "waiting" and "dying" in r["why"], (r["status"], r["why"])
    # 6. a single study alone is not enough
    found1 = {"can_read": [dict(found["can_read"][0], kind="study")], "wanted": []}
    script["writer"] = []; r = make(item, found1, chat, Enc(), MODELS, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex); assert r["status"] == "none" and "not enough sources" in r["why"], r["why"]
    # 7. a wanted paper that stands nearer than the ones read: published, and not complete
    found2 = dict(found, wanted=[dict(found["wanted"][0], near=0.9)]); script["writer"] = [W(ok_short)]; script["checker"] = [V(True, True, True, True)]
    r = make(item, found2, chat, Enc(), MODELS, fulltext=lambda pmcid: xml, crossref=crossref, ex=ex); assert r["status"] == "published" and r["complete"] is False and "could not be read" in r["missing"], r
    assert stakes("Is ketamine addictive?", [{"text": "Some people who use it become dependent."}]) == "" and stakes("Do psychedelics and antidepressants interact?", []) == "mixing drugs" and stakes("x", [{"text": "It can be fatal."}]) == "dying"
    assert not rules([{"part": "short", "text": "Between 9% and 27% of people met criteria for dependence.", "uses": ["F1"]}], {"F1": {"quote": "between 9% and 27% met criteria"}})
    for bad in ("Take it 2 hours after the first dose.", "It is generally safe.", "Snorting it hits faster and stronger.", "Addicts relapse.", 'The paper says "yes".', "You should wait.", "It potentiates the high.", "Passages show a link."):
        assert rules([{"part": "short", "text": bad, "uses": ["F1"]}], {"F1": {"quote": "2"}}), bad
    print("lane selftest: ok (published with every sentence tied to the paper's own words; a retracted paper never read; quotes that are not in the paper and numbers that are not in the quote thrown away; "
          "a broken rule written again; a refused line dropped; a refused short answer means no answer; a question about dying waits for a person; one study alone is not enough; a nearer paper that cannot be read means not complete)")


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
