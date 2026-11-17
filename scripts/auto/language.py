#!/usr/bin/env python3
"""language.py: the school. The system gets better at reading people's language by itself (docs/AUTOMATION.md, decision 28).

The senior author, 17 November 2026: "our ai system has to always improve how it understands human language by learning from
the language people use online and from the language people use in our website. it has to always improve by itself";
"it should not depend on us to get better".

What it is. Every day, on GitHub's machine, with no key at all: it reads open collections of questions that people really
typed (data/auto/language/sources.json; each with its licence; only where the site's robots.txt allows it), lets the
page's own reader read every one of them (the same rules the page runs on a visitor's device: scripts/insight/build_index.py,
WordRules), measures where that reader is wrong, learns what the evidence allows, and keeps a lesson only if the reader
is no worse afterwards on the site's own test sets. What it learns is a small table (data/auto/language/learned.json)
that the next build reads; the half-hourly run sees the table change and publishes the site. No editor is needed.

    python3 -I scripts/auto/language.py learn [--minutes 12]
    python3 -I scripts/auto/language.py --selftest

A lesson is five things: a source of real language; a measure; a rule for what may be learned from the evidence; a gate;
a report. The lessons so far:

  1. Whole questions (the measure). A question someone typed into a search engine and got an answer to is a finished
     question. Of every thousand, how many does our reader call unfinished ("Go on. Finish your question"), and why
     ("ends", "verb", "typing", "which", "bare", "open")? Kept day by day in data/auto/language/report.json: the line
     should fall.
  2. Verbs (what is learned). After do, does, can, should ... a question needs a verb in its base form. The reader takes
     a word for a possible verb when the small model's word list also holds its -ing or -ed form; a verb whose forms that
     list lacks ("legalize", "dissolve") is not seen as one, and a finished question is called unfinished. Evidence that
     a word is a verb, from the questions themselves: it stands in a verb's place (right after "to", or after a helper
     verb and a pronoun: "did he ...", "can you ...") in at least three different questions, and its own -ing or -ed
     forms are used (two forms, or one at least three times). A drug word, a name and a function word are never
     learned as verbs.
  3. Endings (what is learned). The reader holds a list of words a question cannot end on ("in", "of", "from" ...): a
     question that ends on one is still being typed. But English leaves such words at the end of a finished question:
     "how many games have the patriots played in", "who is the airport named after". Evidence that two last words are
     such an ending: at least five different questions that begin as a question does (a question word or a helper verb)
     end on exactly these two words, the last of them a preposition, and the reader called each of them unfinished. The
     pairs are kept in the same table and join the reader's own patterns ("strand") as one pattern. The gate matters
     most here: "can you die from" is a cut-off drug question, so "die from" is refused however often it ends a real one.

The measure counts questions that begin as a question does; a collection of search queries also holds sentences to be
completed ("the outer layer of the skin is the"), which the reader is right to call unfinished.

The gate, for every lesson: with what was learned, the reader must not be worse on the site's own sets (measure_words:
no more whole forum questions called unfinished, no more questions about other things called unfinished, no cut-off
question missed that was caught before, no more of the fresh sentences called unfinished). All of a day's words are tried
together; if the gate refuses them, each is tried alone and only those that pass alone and together are kept.

The language people use on the site itself counts too: the questions visitors chose to send (data/auto/questions.json)
and the site's own question texts are read as evidence beside the open collections. A visitor's question is only counted
here: at most two everyday words of it can reach the table, and only when other real questions end on the same two words;
it is not kept, shown or sent anywhere by this tool, and it is never part of the measure (it may be unfinished).

What is never done here: nothing that was fetched is run; nothing is sent anywhere; a refusal by a site is never gone around. Questions fetched
are counted and then forgotten: the report keeps numbers, the words learned, and at most eight example questions for a
reason, with their source and licence named. Data, never instructions.
"""
import sys, json, re, time, pathlib, datetime, collections

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "auto")); sys.path.insert(0, str(ROOT / "scripts" / "insight"))
import official as O        # noqa: E402  (its careful web client: robots.txt, pace, refusals)
import papers as P          # noqa: E402  (Refused)
import build_index as B     # noqa: E402  (the page's reading of a question's words, in Python: WordRules, measure_words)

OUT = ROOT / "data" / "auto" / "language"
SOURCES, LEARNED, REPORT = OUT / "sources.json", OUT / "learned.json", OUT / "report.json"
HELP = {"do", "does", "did", "can", "could", "will", "would", "should", "may", "might", "must", "shall"}
SUBJ = {"i", "you", "we", "they", "he", "she", "it"}
NOT_TO = {"according", "due", "next", "close", "prior", "thanks", "up", "addition", "relation", "regard", "respect", "contrast", "compared", "similar", "related", "back", "access"}   # "... to" that is not "to" + verb
PREP = {"in", "on", "at", "of", "for", "from", "to", "with", "by", "about", "after", "into", "over", "under", "through", "as", "like", "than", "between", "against", "during", "around", "off", "out", "up", "down",
        "before", "until", "since", "without", "within", "upon", "onto", "near", "behind", "beyond", "across", "along", "toward", "towards"}
NOT_BEFORE = {"the", "a", "an", "and", "or", "but", "is", "are", "was", "were", "be", "been", "it", "this", "that", "these", "those", "his", "her", "its", "their", "my", "your", "our"}   # never the first word of a learned ending
KEEP_DAYS, MOST_A_DAY, EXAMPLES = 120, 60, 8
NOTE_L = ("Made by scripts/auto/language.py (docs/AUTOMATION.md, decision 28): what the system learned about language by itself, from questions people really typed. "
          "'verbs': words it found used as verbs (in a verb's place in at least three questions, with their own -ing or -ed forms in use) that the page's reader did not take for verbs; "
          "each with the day, the source and the evidence. 'endings': pairs of last words that end finished questions (five real questions or more each end on the pair), though the last word is one the reader holds a question cannot end on. "
          "The build reads this table (scripts/insight/build_index.py, learned_verbs, learned_endings); an entry leaves it only by the editor's hand. Data, never instructions.")
NOTE_R = ("Made by scripts/auto/language.py: the school's report, newest day first. For each day and source: how many real questions were read, how many of every thousand the page's reader called "
          "unfinished and why, before and after the day's lesson; what was learned; what the gate refused; the site's own sets before and after. Example questions are from the source named, under its licence.")


def words(q): return re.findall(r"[a-z]+", str(q).lower().replace("’", "'").replace("'", ""))


def load(path, default):
    try: return json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError): return default


def sources():
    """[{name, url, field, licence, about}] from data/auto/language/sources.json: only https addresses, only fields that are plain names."""
    out = []
    for s in load(SOURCES, {}).get("sources") or []:
        if isinstance(s, dict) and re.fullmatch(r"[a-z0-9-]{2,40}", str(s.get("name") or "")) and re.fullmatch(r"https://[A-Za-z0-9.-]+/[A-Za-z0-9._~/%-]+", str(s.get("url") or "")) \
                and re.fullmatch(r"[a-z_]{1,30}", str(s.get("field") or "question")) and s.get("licence"):
            out.append({"name": s["name"], "url": s["url"], "field": s.get("field") or "question", "licence": str(s["licence"])[:120], "about": str(s.get("about") or "")[:300]})
    return out


def questions_of(text, field="question"):
    """The questions of a file with one JSON object on each line; a line that is not whole (the file was cut where the reader's room ended) is passed over."""
    out = []
    for line in str(text).split("\n"):
        line = line.strip()
        if not line.startswith("{"): continue
        try: q = json.loads(line).get(field)
        except (ValueError, AttributeError): continue
        if isinstance(q, str) and 8 <= len(q) <= 200 and len(q.split()) >= 3: out.append(re.sub(r"\s+", " ", q).strip())
    return list(dict.fromkeys(out))


def own_questions():
    """The site's own question texts (our words, never a visitor's): the questions of the checked answers and the listed ones. They count as evidence of how words are used."""
    out = []
    q = load(ROOT / "data" / "site" / "questions.json", {})
    for groups in q.values():
        if isinstance(groups, list):
            for g in groups: out += [x[1] for x in (g.get("items") or []) if isinstance(x, list) and len(x) > 1 and isinstance(x[1], str)]
    for f in (ROOT / "data" / "site" / "wanted.json", ROOT / "data" / "auto" / "wanted-auto.json"):
        for it in load(f, {}).get("items") or []:
            if isinstance(it, dict): out += [x for x in [it.get("q")] + list(it.get("ways") or []) if isinstance(x, str)]
    return list(dict.fromkeys(out))


def visitor_questions():
    """The questions visitors chose to send, as the scout keeps them (data/auto/questions.json): evidence only, never the measure."""
    return list(dict.fromkeys(x["q"] for x in load(ROOT / "data" / "auto" / "questions.json", {}).get("questions") or [] if isinstance(x, dict) and isinstance(x.get("q"), str) and 8 <= len(x["q"]) <= 200))


def measure(R, questions, examples=EXAMPLES):
    """How the page's reader reads real, finished questions: {"n", "called_unfinished": {why: n}, "per_1000", "examples": {why: [...]}}."""
    c, ex = collections.Counter(), collections.defaultdict(list)
    for q in questions:
        u = R.unfinished(q)
        if u:
            c[u] += 1
            if len(ex[u]) < examples: ex[u].append(q)
    n = len(questions)
    return {"n": n, "called_unfinished": dict(sorted(c.items())), "per_1000": round(1000 * sum(c.values()) / n, 2) if n else 0.0, "examples": {k: v for k, v in sorted(ex.items())}}


def evidence(questions):
    """(base, seen): base[w] = the questions in which w stands in a verb's place (right after "to"; after a helper verb and a pronoun); seen[w] = how often w is written at all."""
    base, seen = collections.defaultdict(set), collections.Counter()
    for n, q in enumerate(questions):
        w = words(q)
        seen.update(w)
        for i in range(1, len(w)):
            if w[i - 1] == "to" and not (i >= 2 and w[i - 2] in NOT_TO): base[w[i]].add(n)
            elif i >= 2 and w[i - 1] in SUBJ and w[i - 2] in HELP: base[w[i]].add(n)
    return base, seen


def asked(q):
    """Does it begin as a question does (a question word or a helper verb)? A search query that is a sentence to be completed does not."""
    w = words(q); return bool(w) and w[0] in B.ASK_WORDS


def ending_candidates(R, questions, have=()):
    """{"played in": how many questions} for the endings of lesson 3 (the head of this file)."""
    U = R.unfin; c = collections.defaultdict(set)
    for n, q in enumerate(questions):
        w, nm = R.unf_tokens(q)
        if len(w) < 4 or w[0] not in B.ASK_WORDS or w[-1] not in PREP or w[-1] not in U["ends"] or nm[-1] is not None or nm[-2] is not None: continue
        v = w[-2]
        if not re.fullmatch(r"[a-z]{2,14}", v) or v in NOT_BEFORE or v in PREP or v in U["det"] or R.unfinished(q) != "ends": continue
        c[v + " " + w[-1]].add(n)
    out = sorted(((p, len(s)) for p, s in c.items() if len(s) >= 5 and p not in have and re.fullmatch(r"[a-z]{2,14} [a-z]{2,8}", p)), key=lambda kv: (-kv[1], kv[0]))
    return {p: {"questions": n} for p, n in out[:MOST_A_DAY * 4]}


def verb_candidates(R, base, seen, have=()):
    """{word: evidence} for the words used as verbs that the reader does not take for verbs (lesson 2 at the head of this file)."""
    U = R.unfin; out = {}
    never = set().union(*(U[k] for k in ("aux", "be", "help", "gap", "who", "whoadj", "det", "func", "ends", "open", "nouns", "topic", "join") if k in U))
    for w, where in base.items():
        if len(where) < 3 or not re.fullmatch(r"[a-z]{3,14}", w) or w in have or w in U["verbs"] or w in never: continue
        if B.verbish(w, U["vocab"]): continue                                   # the reader takes it for a possible verb already
        if R.in_scope(w): continue                                              # a drug word or a drug's name is never learned as a verb
        forms = {f: seen[f] for f in dict.fromkeys(B.verb_forms(w)) if seen.get(f)}
        if len(forms) >= 2 or sum(forms.values()) >= 3: out[w] = {"in_a_verbs_place": len(where), "forms": forms}
    return dict(sorted(out.items(), key=lambda kv: (-kv[1]["in_a_verbs_place"], kv[0]))[:MOST_A_DAY])


def worse(a, b):
    """Is the reader worse on the site's own sets with b than with a (measure_words' numbers)? What got worse, or ""."""
    for k in ("real_called_unfinished", "other_called_unfinished"):
        if b.get(k, 0) > a.get(k, 0): return f"{k}: {a.get(k)} -> {b.get(k)}"
    for k, v in a.items():
        if isinstance(v, list) and len(v) == 2 and isinstance(b.get(k), list) and b[k][0] < v[0]: return f"{k}: {v[0]} -> {b[k][0]} of {v[1]}"
    fa, fb = sum((a.get("fresh_called_unfinished") or {}).values()), sum((b.get("fresh_called_unfinished") or {}).values())
    return f"fresh_called_unfinished: {fa} -> {fb}" if fb > fa else ""


def trial(R, verbs=(), endings=()):
    """The reader with more verbs and more endings, for a trial: the same object, widened. Returns what takes them back."""
    v0, s0 = R.unfin["verbs"], R.unfin["strand"]
    pat = B.ending_pattern(list(endings))
    R.unfin["verbs"] = set(v0) | set(verbs); R.unfin["strand"] = list(s0) + ([re.compile(pat)] if pat else [])
    def back(): R.unfin["verbs"], R.unfin["strand"] = v0, s0
    return back


def gate(R, cand, kind="verbs", site=None, also=None):
    """(kept, refused, before, after): the candidates the site's own sets allow. kind: "verbs" or "endings". also: what an earlier
    lesson of the day kept (it stays in the trial). site: measure_words(R) -> numbers (the selftest gives its own)."""
    site = site or (lambda r: B.measure_words(r, show=False)); also = also or {}
    def numbers(subset):
        back = trial(R, **dict(also, **{kind: list(also.get(kind) or []) + list(subset)}))
        try: return site(R)
        finally: back()
    before = numbers([])
    if not cand: return {}, {}, before, before
    all_at_once = numbers(cand); why = worse(before, all_at_once)
    if not why: return dict(cand), {}, before, all_at_once
    kept, refused = {}, {}
    for w, ev in cand.items():
        one = worse(before, numbers([w]))
        if one: refused[w] = one
        else: kept[w] = ev
    after = numbers(kept); why = worse(before, after)
    if why: return {}, dict({w: "together with the others: " + why for w in kept}, **refused), before, before
    return kept, refused, before, after


def learn(by_source, R=None, today=None, save=True, site=None, own=None):
    """One day at school. by_source: {name: {"questions": [...], "licence": "...", "problem": "" }}. Returns the day's report."""
    R = R or B.WordRules(); day = today or datetime.date.today().isoformat()
    L = load(LEARNED, {}) if save else {}; verbs = dict(L.get("verbs") or {}); endings = dict(L.get("endings") or {})
    allq = list(dict.fromkeys(q for s in by_source.values() for q in s.get("questions") or []))
    rep = {"day": day, "sources": {n: {"questions": len(s.get("questions") or []), "licence": s.get("licence") or "", **({"problem": s["problem"]} if s.get("problem") else {})} for n, s in by_source.items()}}
    if not allq:
        rep["said"] = "no questions could be read today: nothing measured, nothing learned"
    else:
        qs = [q for q in allq if asked(q)]                                    # the measure: what begins as a question does
        before = measure(R, qs)
        src = "+".join(sorted(by_source))
        sent = [] if own is not None else visitor_questions()
        ends, no_e, s0, s1 = gate(R, ending_candidates(R, list(dict.fromkeys(qs + [q for q in sent if asked(q)])), have=set(endings)), "endings", site)
        base, seen = evidence(allq + sent + list(own if own is not None else own_questions()))
        kept, no_v, _, s2 = gate(R, verb_candidates(R, base, seen, have=set(verbs)), "verbs", site, also={"endings": list(ends)})
        back = trial(R, verbs=kept, endings=ends); after = measure(R, qs); back()
        for w, ev in kept.items(): verbs[w] = dict(ev, on=day, source=src)
        for p, ev in ends.items(): endings[p] = dict(ev, on=day, source=src)
        refused = dict(no_e, **no_v)
        rep.update({"read": len(allq), "site_questions_counted_as_evidence": len(sent), "begin_as_a_question": len(qs), "per_1000_called_unfinished": [before["per_1000"], after["per_1000"]], "called_unfinished": [before["called_unfinished"], after["called_unfinished"]],
                    "examples_still_called_unfinished": after["examples"], "learned_endings": sorted(ends), "learned_verbs": sorted(kept), "refused_by_the_gate": refused, "site_sets": [s0, s2 if kept else s1],
                    "endings_known_in_all": len(endings), "verbs_known_in_all": len(verbs)})
        rep["said"] = (f"{len(allq)} real questions read, {len(qs)} of them begin as a question does; of those, called unfinished per thousand: {before['per_1000']} before, {after['per_1000']} with today's lessons; "
                       f"{len(ends)} ending(s) learned" + (": " + ", ".join(sorted(ends)[:12]) if ends else "") + f"; {len(kept)} verb(s) learned" + (": " + ", ".join(sorted(kept)[:12]) if kept else "")
                       + (f"; {len(refused)} refused by the gate" if refused else ""))
    if save:
        OUT.mkdir(parents=True, exist_ok=True)
        if rep.get("learned_verbs") or rep.get("learned_endings"): json.dump({"_note": NOTE_L, "verbs": dict(sorted(verbs.items())), "endings": dict(sorted(endings.items()))}, open(LEARNED, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        R0 = load(REPORT, {}); days = [d for d in (R0.get("days") or []) if isinstance(d, dict) and d.get("day") != day]
        json.dump({"_note": NOTE_R, "days": ([rep] + days)[:KEEP_DAYS]}, open(REPORT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("language:", rep["said"])
    return rep


def fetch_all(web=None, minutes=12.0):
    """{name: {"questions", "licence", "problem"}} for every source that may be read now."""
    web = web or O.Web(); t0 = time.time(); out = {}
    for s in sources():
        e = {"questions": [], "licence": s["licence"], "problem": ""}; out[s["name"]] = e
        if time.time() - t0 > minutes * 60: e["problem"] = "the time for this run was up"; continue
        try: got = web.get(s["url"], "application/json,text/plain;q=0.9,*/*;q=0.5")
        except P.Refused as x: e["problem"] = "refused: " + str(x)[:160]; continue
        except (IOError, ValueError) as x: e["problem"] = "could not be read: " + str(x)[:160]; continue
        if not got: e["problem"] = "not there"; continue
        e["questions"] = questions_of(O.text_of(got[0]), s["field"])
        if not e["questions"]: e["problem"] = "no question could be read from it"
        print(f"language: {s['name']}: {len(e['questions'])} questions" + (f" ({e['problem']})" if e["problem"] else ""))
    return out


def selftest():
    class U(dict): pass
    class Reader:                                                    # a small reader with the real rule's shape: a helper verb needs a verb the word list knows as one
        def __init__(self):
            self.unfin = {"strand": [], "verbs": {"take"}, "vocab": {"take", "taking", "legalize", "dissolve", "school", "happen", "happening", "people", "weed"},
                          "aux": {"the", "a"}, "be": {"is", "are"}, "help": set(HELP), "gap": {"it"}, "who": {"people"}, "whoadj": set(), "det": {"the", "a"}, "func": {"of", "in"}, "ends": {"the", "of"}, "open": {"how", "what", "why"}, "nouns": set(), "topic": set(), "join": {"and"}}
        def in_scope(self, w): return w in ("weed", "ketamine")
        def unf_tokens(self, q): w = words(q); return w, [None] * len(w)
        def unfinished(self, q):
            w = words(q)
            if w and w[-1] in self.unfin["ends"] and not any(p.search(" ".join(w)) for p in self.unfin["strand"]): return "ends"
            for i, x in enumerate(w):
                if x in HELP:                                        # the first word after the helper and its subject must be a verb
                    y = next((y for y in w[i + 1:] if y not in SUBJ and y not in self.unfin["who"] and y not in self.unfin["det"] and not self.in_scope(y)), "")
                    return "" if y and (y in self.unfin["verbs"] or B.verbish(y, self.unfin["vocab"])) else "verb"
            return ""
    qs = ["when did they legalize weed in canada", "how to legalize a business name", "why did he legalize it then", "who is legalizing weed", "when was it legalized there",
          "how long does sugar take to dissolve in water", "can you dissolve salt in oil", "does it dissolve in cold water", "what is dissolving in chemistry", "the powder dissolved quickly why",
          "how to school a horse", "going to school in france", "close to school zones", "when did people happen to move", "who was the king of"]
    assert questions_of('{"question": "who sang the first song", "answer": ["x"]}\n{"question": "short"}\nnot json\n{"question": "when did they legalize weed in ca') == ["who sang the first song"]
    R = Reader(); m = measure(R, qs)
    assert m["called_unfinished"] == {"ends": 1, "verb": 4} and m["per_1000"] == 333.33 and m["examples"]["ends"] == ["who was the king of"], m
    base, seen = evidence(qs)
    assert len(base["legalize"]) == 3 and len(base["dissolve"]) == 3 and "school" in base and len(base["school"]) == 2 and seen["legalizing"] == 1 and "zones" not in base
    cand = verb_candidates(R, base, seen)
    assert set(cand) == {"legalize", "dissolve"} and cand["legalize"]["forms"] == {"legalizing": 1, "legalized": 1} and cand["dissolve"]["forms"] == {"dissolving": 1, "dissolved": 1}, cand   # "school": twice only, no forms; "happen": the list knows "happening"; "weed": a drug word
    assert "weed" not in verb_candidates(R, {"weed": {1, 2, 3}}, collections.Counter({"weeding": 3, "weeded": 2})) and "the" not in verb_candidates(R, {"the": {1, 2, 3}}, collections.Counter({"theing": 3, "thed": 3}))
    calls = []
    def site(r):                                                     # the site's own sets: "dissolve" as a verb lets one cut-off question through
        calls.append(sorted(r.unfin["verbs"])); bad = "dissolve" in r.unfin["verbs"]
        return {"real_called_unfinished": 0, "other_called_unfinished": 1, "cut_before_the_name": [291 if bad else 292, 399], "fresh_called_unfinished": {"which": 14}}
    kept, refused, s0, s1 = gate(R, cand, "verbs", site)
    assert set(kept) == {"legalize"} and "cut_before_the_name: 292 -> 291" in refused["dissolve"] and R.unfin["verbs"] == {"take"} and s1["cut_before_the_name"][0] == 292, (kept, refused)
    # lesson 3: an ending is learned from five questions that begin as questions do; a sentence to be completed is no evidence; the gate refuses an ending that a cut-off drug question has
    R.unfin["ends"] = {"the", "of", "in", "from"}
    eq = [f"how many games have the {t} played in" for t in ("patriots", "giants", "jets", "bears", "colts")] + [f"what did {p} die from" for p in ("mozart", "bach", "elvis", "prince", "lincoln")] + \
         ["the capital city that the romans lived in", "what is the song in", "who is this named from", "the outer layer of the skin is the"]
    ec = ending_candidates(R, eq)
    assert ec == {"die from": {"questions": 5}, "played in": {"questions": 5}} and asked("what did bach die from") and not asked("the outer layer of the skin is the"), ec
    assert B.ending_pattern(["played in", "Bad One", "x y z"]) == "^(?:" + "|".join(B.ASK_WORDS) + ")\\b.* (?:played in)$" and B.ending_pattern([]) == ""
    def site2(r):                                                    # "can you die from" is a cut-off drug question in the site's own set
        miss = not r.unfinished("can you die from")
        return {"real_called_unfinished": 0, "other_called_unfinished": 1, "cut_after_a_word_that_cannot_end": [1114 if miss else 1115, 1176], "fresh_called_unfinished": {}}
    ek, er, _, _ = gate(R, ec, "endings", site2)
    assert set(ek) == {"played in"} and "cut_after_a_word_that_cannot_end: 1115 -> 1114" in er["die from"] and R.unfin["strand"] == [] and R.unfinished("how many games have the jets played in") == "ends", (ek, er)
    back = trial(R, endings=ek); assert R.unfinished("how many games have the jets played in") == "" and R.unfinished("the team the jets played in") == "ends" and R.unfinished("what did bach die from") == "ends"; back()
    R.unfin["ends"] = {"the", "of"}
    assert worse({"a": [5, 9], "real_called_unfinished": 0}, {"a": [5, 9], "real_called_unfinished": 1}).startswith("real_called_unfinished") and not worse(s0, s0)
    assert worse({"fresh_called_unfinished": {"which": 2}}, {"fresh_called_unfinished": {"which": 2, "verb": 1}}) == "fresh_called_unfinished: 2 -> 3"
    rep = learn({"made-up": {"questions": qs, "licence": "none: written for this test"}}, R=R, today="2026-11-17", save=False, site=site, own=[])
    # (of the 15, 12 begin as a question does: "going to school in france", "close to school zones" and "the powder dissolved quickly why" do not)
    assert rep["learned_verbs"] == ["legalize"] and rep["begin_as_a_question"] == 12 and rep["per_1000_called_unfinished"] == [416.67, 250.0] and rep["called_unfinished"][1] == {"ends": 1, "verb": 2} and "dissolve" in rep["refused_by_the_gate"] and R.unfin["verbs"] == {"take"}, rep
    assert learn({"x": {"questions": [], "licence": "y", "problem": "refused: robots.txt"}}, R=R, save=False, site=site, own=[])["said"].startswith("no questions could be read")
    # the list of sources is read as data: an address that is not https, or a field that is not a plain name, is passed over
    global SOURCES
    import tempfile; keep = SOURCES
    with tempfile.TemporaryDirectory() as d:
        SOURCES = pathlib.Path(d) / "s.json"
        SOURCES.write_text(json.dumps({"sources": [{"name": "nq-open-dev", "url": "https://raw.githubusercontent.com/x/y/master/a.jsonl", "licence": "CC BY-SA 3.0"}, {"name": "bad", "url": "http://x/y", "licence": "z"},
                                                   {"name": "no-licence", "url": "https://x.org/y.jsonl"}, {"name": "odd", "url": "https://x.org/y.jsonl", "field": "a b", "licence": "z"}]}), encoding="utf-8")
        assert [s["name"] for s in sources()] == ["nq-open-dev"] and sources()[0]["field"] == "question"
        class Resp:
            def __init__(self, b, url): self.b, self.url = b, url
            def read(self, n=-1): return self.b
            def geturl(self): return self.url
            def __enter__(self): return self
            def __exit__(self, *a): return False
        def opener(req, timeout=0):
            if req.full_url.endswith("/robots.txt"): import urllib.error; raise urllib.error.HTTPError(req.full_url, 404, "no", None, None)
            return Resp(b'{"question": "when did they legalize weed in canada", "answer": []}\n{"question": "who sang the first song"}\n{"question": "cut he', req.full_url)
        got = fetch_all(O.Web(opener))
        assert got["nq-open-dev"]["questions"] == ["when did they legalize weed in canada", "who sang the first song"] and not got["nq-open-dev"]["problem"], got
    SOURCES = keep
    print("language selftest: ok (real questions are read by the page's own reader and counted by why they were called unfinished; a word is learned as a verb only with the evidence the head of this file names, "
          "never a drug word or a function word; the site's own sets refuse a word that lets a cut-off question through, alone or together; a line cut off in the middle and a source with no licence are passed over)")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a: selftest()
    elif a[:1] == ["learn"]:
        learn(fetch_all(minutes=float(a[a.index("--minutes") + 1]) if "--minutes" in a else 12.0))
    else: sys.exit(__doc__)
