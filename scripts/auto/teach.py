#!/usr/bin/env python3
"""teach.py: lesson material for our own checker (docs/AUTOMATION.md, decision 23, step two).

    python3 -I scripts/auto/teach.py requests            (data/auto/requests/teach-*.json: {"max": 600, "minutes": 40, "models": [...], "at_once": 4})
    python3 -I scripts/auto/teach.py show                 (what has been made, by kind)
    python3 -I scripts/auto/teach.py --selftest

Our own checker has to learn the faults OUR blind checkers find, and the open models as they are barely see them (step
one: data/auto/exam/nli-*.json). Real faulty sentences are few (22 on the cards, 56 plain lines, the lane's own), and they
are the measure: a model that has learned from them cannot be measured on them. So the lessons are made, not taken:

  from   the sentences a blind checker PASSED (the good cards' true parts, each beside the lines it was written from; the
         lane's own sentences the editor judged good, beside the words they rest on)
  to     for each, one made-up wrong sentence of each kind our checkers have named (a word of measure the source does not
         carry; a report said as a fact; a wider group or another thing counted; a cause or a reason added; a detail from
         nowhere; a hedge or a limit dropped), and one faithful rewording, which stays good

written by a free open model that is told exactly which fault to make. The examples in its instructions are invented for
this file; none is a real fault from the exams. What the model returns is checked by code (it must differ from the good
sentence, stay near its length, and say which words now say more) and kept, one line each, in
data/auto/own/teach/made.jsonl with where it came from, so that the training (the workshop) can leave out whole cards.

The exams stay the measure, and stay apart: the cards' real faulty sentences, every plain line (lines.json: none of it is
used here) and the lane's sentences the editor judged not good are never lessons.

What is sent to the model service: our own sentences and our own plain lines. Never a visitor's words.
"""
import sys, re, json, time, random, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import llm

EXAM = ROOT / "data" / "auto" / "exam"
OUT = ROOT / "data" / "auto" / "own" / "teach"
MADE = OUT / "made.jsonl"
MODELS = ["gemini:gemma-4-31b-it", "gemini:gemma-4-26b-a4b-it"]          # two writers, in turn: lessons in more than one hand
ROOM = 2600                                                                # room for a reply: Gemma thinks aloud first, in <thought> marks, at length (the first run, with 400, and the second, with 1,200, got next to nothing out of it)

KINDS = {   # kind: (what to do, an invented example: passage, good sentence, the wrong one)
    "measure": ("Add or strengthen ONE word of measure that the PASSAGES do not carry: how often (often, usually, always), how many (most, all, both), how sure (clearly, proven), how big (severe, far more, slightly) or how good (famous, leading, trained).",
                "In one survey of 300 students, 41 said they had tried it.", "In one survey of 300 students, 41 said they had tried it.", "In one large survey of 300 students, many said they had tried it."),
    "report": ("State as a plain fact something the PASSAGES give only as what people said, reported, rated or recalled, or as what the authors suggest or think. Remove the words that mark it as a report.",
               "Volunteers rated themselves calmer afterwards. The authors suggest sleep may explain it.", "Volunteers rated themselves calmer afterwards.", "Volunteers were calmer afterwards."),
    "wider": ("Make the sentence about more than the PASSAGES, or about something else: people in general where it was men, patients or one study's volunteers; studies in general where it was one; another place or time; another thing counted.",
              "Among 64 men in a hospital ward in Oslo, 12 had the symptom.", "Among 64 men on one hospital ward, 12 had the symptom.", "Among people in hospital, about 1 in 5 had the symptom."),
    "cause": ("Say or imply that one thing causes, explains or follows from another (because, so, leads to, which is why) where the PASSAGES only put the two side by side or report a link.",
              "People who slept less also scored lower. The study measured both once.", "People who slept less also scored lower.", "People scored lower because they slept less."),
    "extra": ("Add ONE small detail that sounds right but is not in the PASSAGES: a number, a name, a place, a year, or a short clause.",
              "The trial had 40 adults and lasted six weeks.", "The trial had 40 adults and lasted six weeks.", "The trial had 40 adults in two clinics and lasted six weeks."),
    "hedge": ("Drop ONE hedge or limit that the PASSAGES state and the SENTENCE keeps: may, can, might, about, up to, at least, in some people, in this study, so far.",
              "It may help some people sleep, in two small trials.", "It may help some people sleep, in two small trials.", "It helps people sleep, in two small trials."),
    "same": ("Say exactly the same in other plain words. Nothing may be added, strengthened, weakened or left out.",
             "Of 120 people asked, 30 said the pills helped.", "Of 120 people asked, 30 said the pills helped.", "30 of the 120 people asked said the pills had helped them."),
}
SYS = ("You help to train a checker of sentences. You are given PASSAGES and a SENTENCE that says only what the passages say. You rewrite the sentence in the one way you are told, "
       "changing as little as you can, in plain everyday English. You answer with JSON only.")


def prompt(kind, passages, sentence):
    what, ex_p, ex_s, ex_new = KINDS[kind]
    return (f"TASK: {what}\n\n"
            f"An example of this task (invented):\n   PASSAGES: {ex_p}\n   SENTENCE: {ex_s}\n   YOUR SENTENCE: {ex_new}\n\n"
            f"Now do it for this one.\nPASSAGES: {passages}\nSENTENCE: {sentence}\n\n"
            + ("Keep every fact, number and limit of the SENTENCE. " if kind == "same" else "Change only what the task asks; keep the rest of the SENTENCE as it is, so that the result reads like a careless but honest sentence. ")
            + "If the task cannot be done for this sentence (there is nothing of that kind to change), answer {\"skip\": true}.\n"
            + 'JSON only: {"sentence": "your sentence", "changed": "the words of your sentence that are new or different"}')


def true_part(card):
    why = [x.strip() for x in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9“\"'(\[])", re.sub(r"^(?:true|false|myth|fact)[.!:]?\s+", "", card.get("why") or "", flags=re.I)) if x.strip()]
    return ([card["statement"]] if card["answer"] else []) + why


def sources(exam=None):
    """The good sentences lessons are made from: [{"id", "group", "passages", "sentence"}]. group: what is left out together
    when a model trained on these is measured (a card's sentences share its lines). Never a plain line of lines.json."""
    E = exam or EXAM; out = []
    try: cards = json.load(open(E / "cards.json", encoding="utf-8"))["items"]
    except (OSError, ValueError): cards = []
    for i in cards:
        if not i["good"]: continue                                   # a wrong card gives no lesson: its faulty sentence is the exam's, and its other sentences share its lines
        L = i["lines"]; ps = " ".join(t for t in [L.get("short") or "", L.get("but") or ""] + list(L.get("how") or []) if t)
        out += [{"id": f"cards:{i['id']}#{k}", "group": "cards:" + str(i.get("claim") or i["id"]), "passages": ps, "sentence": s} for k, s in enumerate(true_part(i["card"]))]
    try: sents = json.load(open(E / "lane-sentences.json", encoding="utf-8"))["items"]
    except (OSError, ValueError): sents = []
    out += [{"id": "lane:" + i["id"], "group": "lane:" + i["id"].split("#")[0], "passages": " ".join(i["rests_on"]), "sentence": i["sentence"]} for i in sents if i["good"]]
    return out


def accept(kind, was, out):
    """(the new sentence, the words it changed) when what the model returned can be a lesson, else (None, why not)."""
    if not isinstance(out, dict): return None, "no JSON"
    if out.get("skip") is True: return None, "skip"
    new = re.sub(r"\s+", " ", str(out.get("sentence") or "")).strip(); ch = re.sub(r"\s+", " ", str(out.get("changed") or "")).strip()[:160]
    norm = lambda t: re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()
    if not new or norm(new) == norm(was): return None, "the same sentence"
    if not 0.5 <= len(new) / max(1, len(was)) <= 1.7: return None, "too far from the sentence's length"
    if kind != "same" and not ch: return None, "it did not say what it changed"
    if re.search(r"\b(?:PASSAGES?|SENTENCE|TASK)\b", new): return None, "words of the task itself"
    return new, ch


def made(path=None):
    out = []
    try:
        for line in open(path or MADE, encoding="utf-8"):
            if line.strip(): out.append(json.loads(line))
    except OSError: pass
    return out


def merge(other, path=None):
    """Lessons saved elsewhere (the branch a run saves to while it goes on) that this file does not hold yet are added to it:
    one lesson for a sentence and a kind, the one already here. Returns how many were added."""
    path = path or MADE; have = {(x["from"], x["kind"]) for x in made(path)}; new = []
    for x in made(other):
        if isinstance(x, dict) and all(isinstance(x.get(k), str) for k in ("from", "kind", "sentence", "by")) and x["kind"] in KINDS and (x["from"], x["kind"]) not in have: have.add((x["from"], x["kind"])); new.append(x)
    if new:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            for x in new: f.write(json.dumps(x, ensure_ascii=False) + "\n")
    return len(new)


def run(limit=600, minutes=40, models=None, chat=None, exam=None, path=None, today=None, at_once=1, rests=3, rest=300, day_of=None):
    """Makes lessons until the limit, the time or the day's allowance ends. Returns how many were written.
    (17 November 2026) A writer that gives nothing usable twelve times running RESTS for five minutes and is asked again, three
    times at most, before it is left out: on the night of 16 November both Gemma writers were answered "high demand" for a
    quarter of an hour, were left out for good, and the run ended two hours early. A writer whose day's allowance is used
    up comes back when its service's day turns (Google's, at midnight Pacific time): a run that goes through that hour uses
    the new day. And the run says how far it is every five minutes, so that the notes saved while it goes on can be read."""
    path = path or MADE; path.parent.mkdir(parents=True, exist_ok=True)
    models = [m for m in (models or MODELS) if chat or llm.has(m)]
    if not models: print("teach: no model with a key on this machine: nothing made"); return 0
    have = {(x["from"], x["kind"]) for x in made(path)}; skipped = set()
    try: skipped = {tuple(x) for x in json.load(open(path.with_name("skipped.json"), encoding="utf-8"))}
    except (OSError, ValueError): pass
    src = sources(exam); rnd = random.Random(20261116); rnd.shuffle(src)                 # the same order every run: a run goes on where the last one stopped
    todo = [(s, k) for s in src for k in KINDS if (s["id"], k) not in have and (s["id"], k) not in skipped]
    t0 = time.time(); n = asked = 0; why_not = {}; samples = []; wrote = {m: 0 for m in models}; misses = {m: 0 for m in models}; live = list(models)
    rested = {m: 0 for m in models}; back = {}                                # how often a writer has rested; when a resting writer comes back
    day = day_of or ((lambda m: llm.day_of(llm.service_of(m)[0])) if not chat else None); spent = {}; told = [t0]      # the day on which a writer's allowance ran out
    def say(*a): print(*a, flush=True)
    import concurrent.futures as cf

    def ask(s, kind, model):
        """One lesson asked of one writer (run in a worker): (s, kind, model, the reply or None, the service's refusal or "", how the reply ended)."""
        try: raw = (chat or llm.chat)(model, [{"role": "system", "content": SYS}, {"role": "user", "content": prompt(kind, s["passages"], s["sentence"])}], ROOM)
        except llm.Budget as e: return s, kind, model, None, "the day's allowance: " + str(e)[:100], ""
        except llm.Unavailable as e: return s, kind, model, None, "the service: " + str(e)[:60], ""
        return s, kind, model, raw, "", f"the reply ended: {llm.LAST.get('finish')}"

    # several writers are asked at once (each some calls at a time: a free model that thinks aloud takes half a minute a lesson); the main thread alone writes the files
    with open(path, "a", encoding="utf-8") as f, cf.ThreadPoolExecutor(max_workers=max(1, at_once * len(models))) as pool:
        queue = iter(todo); running = set()
        def more():
            nonlocal asked
            for m in [m for m, t in back.items() if time.time() >= t]: back.pop(m); live.append(m); say(f"teach: {m} is asked again after its rest")
            for m in [m for m, d0 in spent.items() if day and day(m) != d0]: spent.pop(m); live.append(m); say(f"teach: {m} is asked again: its service's day has turned")
            if time.time() - told[0] >= 300: told[0] = time.time(); say(f"teach: {(time.time() - t0) / 60:.0f} minutes in: {n} lessons written ({asked} asked; by writer: {wrote}; not usable: {why_not or 'none'}); asked now: {live}; resting: {sorted(back)}; waiting for a new day: {sorted(spent)}")
            while live and len(running) < at_once * len(live) and n + len(running) < limit and time.time() - t0 < minutes * 60:
                item = next(queue, None)
                if item is None: return
                model = live[asked % len(live)]; asked += 1; running.add(pool.submit(ask, item[0], item[1], model))
        more()
        while running:
            done, running = cf.wait(running, return_when=cf.FIRST_COMPLETED)
            for fu in done:
                s, kind, model, raw, refused, ended = fu.result()
                def miss(why):                                            # a writer that gives nothing usable twelve times running is left out of this run (it may be busy, or not write in the form asked)
                    why_not[why] = why_not.get(why, 0) + 1; misses[model] += 1
                    if len(samples) < 6 and raw: samples.append(f"{model} ({why}; {ended}): " + re.sub(r"\s+", " ", raw)[:260])
                    if misses[model] >= 12 and model in live:
                        live.remove(model); misses[model] = 0
                        if rested[model] < rests: rested[model] += 1; back[model] = time.time() + rest; say(f"teach: {model} gave nothing usable twelve times running ({why}): it rests for {rest / 60:.0f} minutes (rest {rested[model]} of {rests})")
                        else: say(f"teach: {model} gave nothing usable twelve times running, after {rests} rests ({why}): left out of this run")
                if refused.startswith("the day's allowance"):
                    if model in live:
                        live.remove(model); say(f"teach: {model}: {refused}")
                        if day: spent[model] = day(model)
                    continue
                if refused: miss(refused); continue
                new, ch = accept(kind, s["sentence"], llm.as_json(raw))
                if new is None:
                    if ch == "skip": why_not[ch] = why_not.get(ch, 0) + 1; skipped.add((s["id"], kind)); misses[model] = 0        # the writer's own word that the task cannot be done for this sentence: not asked again
                    else: miss(ch)
                    continue
                misses[model] = 0; wrote[model] += 1
                f.write(json.dumps({"from": s["id"], "group": s["group"], "kind": kind, "good": kind == "same", "sentence": new, "changed": ch, "by": model, "on": today or datetime.date.today().isoformat()}, ensure_ascii=False) + "\n"); f.flush(); n += 1
            more()
            while not running and (back or spent) and time.time() - t0 < minutes * 60 and n < limit:      # every writer is resting or waits for its new day: wait for the first to come back
                time.sleep(max(0.0, min(min(back.values()) - time.time() if back else 60.0, 60.0 if spent else 1e9))); more()
    json.dump(sorted(skipped), open(path.with_name("skipped.json"), "w", encoding="utf-8"))
    print(f"teach: {n} lessons written ({asked} asked; by writer: {wrote}; not usable: {why_not or 'none'}); {len(todo) - asked} still to make; {len(src)} good sentences to make them from")
    for x in samples: print("teach: a reply that could not be used:", x)
    return n


def show(path=None):
    rows = made(path); by = {}
    for x in rows: by[x["kind"]] = by.get(x["kind"], 0) + 1
    print(f"teach: {len(rows)} lessons from {len({x['from'] for x in rows})} good sentences: " + ", ".join(f"{k} {v}" for k, v in sorted(by.items())) + f"; of them {sum(x['good'] for x in rows)} stay good (faithful rewordings)")


def selftest():
    import tempfile
    d = pathlib.Path(tempfile.mkdtemp()); (d / "exam").mkdir()
    json.dump({"items": [{"id": "c1", "claim": "cl_a", "good": True, "lines": {"short": "It can be so.", "but": "", "how": ["Men said so."]}, "card": {"statement": "It can be so.", "answer": True, "why": "True. Men said so. It was one survey."}},
                         {"id": "c2", "good": False, "lines": {"short": "x", "how": []}, "card": {"statement": "It often is so.", "answer": True, "why": ""}}]}, open(d / "exam" / "cards.json", "w"))
    json.dump({"items": [{"id": "au_w_1#short~a", "good": True, "sentence": "Some said so.", "rests_on": ["Some", "said so."]}, {"id": "au_w_1#how1~b", "good": False, "sentence": "All said so.", "rests_on": ["Some said so."]}]}, open(d / "exam" / "lane-sentences.json", "w"))
    json.dump({"claims": {}, "items": [{"id": "never", "good": True, "line": "A plain line."}]}, open(d / "exam" / "lines.json", "w"))
    src = sources(d / "exam")
    assert [s["id"] for s in src] == ["cards:c1#0", "cards:c1#1", "cards:c1#2", "lane:au_w_1#short~a"] and src[0]["group"] == "cards:cl_a" and src[0]["passages"] == "It can be so. Men said so." and src[3]["group"] == "lane:au_w_1"   # no wrong card, no sentence judged not good, no plain line
    assert accept("measure", "It can be so.", {"sentence": "It often is so.", "changed": "often"}) == ("It often is so.", "often")
    assert accept("measure", "It can be so.", {"sentence": "It can be so.", "changed": "x"})[0] is None and accept("measure", "It can be so.", {"skip": True}) == (None, "skip") and accept("measure", "It can be so.", {"sentence": "It often is so."})[0] is None
    assert accept("same", "It can be so.", {"sentence": "So it can be."})[0] == "So it can be." and accept("extra", "It can be so.", {"sentence": "It can be so, " + "and more " * 9, "changed": "x"})[1] == "too far from the sentence's length"
    assert accept("extra", "It can be so.", None) == (None, "no JSON") and accept("extra", "It can be so.", {"sentence": "The SENTENCE can be so.", "changed": "x"})[0] is None
    pr = prompt("cause", "A and B.", "A, and B.")
    assert "TASK: Say or imply that one thing causes" in pr and "PASSAGES: A and B.\nSENTENCE: A, and B." in pr and "careless but honest" in pr and "Keep every fact" in prompt("same", "A", "A")
    asked = []
    def chat(model, messages, room):
        asked.append((model, messages[1]["content"])); kind = next(k for k in KINDS if KINDS[k][0] in messages[1]["content"])
        if kind == "hedge": return json.dumps({"skip": True})
        was = messages[1]["content"].split("\nSENTENCE: ")[-1].split("\n")[0]
        return json.dumps({"sentence": "Indeed " + was, "changed": "indeed"})
    p = d / "teach" / "made.jsonl"
    n = run(limit=5, minutes=5, chat=chat, exam=d / "exam", path=p, today="2026-11-16")
    rows = made(p); assert n == 5 and len(rows) == 5 and {r["good"] for r in rows if r["kind"] == "same"} <= {True} and all(not r["good"] for r in rows if r["kind"] != "same") and rows[0]["by"] in MODELS and rows[0]["group"]
    assert sorted([m for m, _ in asked].count(x) for x in MODELS) == [2, 3]                          # two writers, in turn (which of two calls made at once is noted first is chance: the count is not)
    n2 = run(limit=100, minutes=5, chat=chat, exam=d / "exam", path=p, today="2026-11-16")
    rows = made(p); assert len(rows) == 4 * 6 and n2 == 24 - 5 and len({(r["from"], r["kind"]) for r in rows}) == 24 and not any(r["kind"] == "hedge" for r in rows)      # it goes on where it stopped, never twice; what cannot be done is not asked again
    k = len(asked); assert run(limit=100, minutes=5, chat=chat, exam=d / "exam", path=p) == 0 and len(asked) == k
    # a writer that gives nothing usable twelve times running is left out of the run; what it failed on is asked again another time (only its own "skip" is remembered)
    p2 = d / "teach2" / "made.jsonl"; seen2 = []
    def chat2(model, messages, room): seen2.append(model); return "I think about it..." if model == MODELS[0] else json.dumps({"sentence": "Indeed " + messages[1]["content"].split("\nSENTENCE: ")[-1].split("\n")[0], "changed": "indeed"})
    n3 = run(limit=100, minutes=5, chat=chat2, exam=d / "exam", path=p2, today="2026-11-16", rests=0)
    assert seen2.count(MODELS[0]) == 12 and n3 == 28 - 12 and not json.load(open(p2.with_name("skipped.json"))), (seen2.count(MODELS[0]), n3)
    # a writer that fails twelve times running rests and is asked again (here: one rest of no length), and only then is left out; a run whose every writer rests waits for them
    p3 = d / "teach3" / "made.jsonl"; seen3 = []
    def chat3(model, messages, room): seen3.append(model); return "I think about it..."
    assert run(limit=100, minutes=5, models=[MODELS[0]], chat=chat3, exam=d / "exam", path=p3, rests=1, rest=0) == 0 and len(seen3) == 24, len(seen3)
    # a writer whose day's allowance is used up comes back when its service's day turns, and writes on
    p5 = d / "teach5" / "made.jsonl"; turn = {"looks": 0, "n": 0}
    def day5(m): turn["looks"] += 1; return "d1" if turn["looks"] == 1 else "d2"       # the day as it was when the allowance ran out, and a new day at every look after
    def chat5(model, messages, room):
        turn["n"] += 1
        if turn["n"] == 1: raise llm.Budget("the free calls of the day are used")
        return json.dumps({"sentence": "Indeed " + messages[1]["content"].split("\nSENTENCE: ")[-1].split("\n")[0], "changed": "indeed"})
    assert run(limit=3, minutes=5, models=[MODELS[0]], chat=chat5, exam=d / "exam", path=p5, day_of=day5) == 3 and turn["n"] == 4, turn
    # lessons saved elsewhere are added once: the one already here stays
    p4 = d / "teach4" / "made.jsonl"; p4.parent.mkdir(parents=True); rows2 = made(p2)
    open(p4, "w").write(json.dumps(dict(rows2[0], sentence="The one that is here.")) + "\n")
    assert merge(p2, p4) == len(rows2) - 1 and merge(p2, p4) == 0 and made(p4)[0]["sentence"] == "The one that is here." and len(made(p4)) == len(rows2) and merge(d / "nothing.jsonl", p4) == 0
    n4 = run(limit=100, minutes=5, chat=chat, exam=d / "exam", path=p2); sk = json.load(open(p2.with_name("skipped.json")))
    assert n4 + len(sk) == 12 and len(made(p2)) + len(sk) == 28 and all(k == "hedge" for _, k in sk)          # the twelve it failed on are asked again: each becomes a lesson, or the writer's own "skip"
    print("teach selftest: ok (lessons come only from sentences a checker passed or the editor judged good, never from a plain line of the third exam; one made-up fault of each kind and one faithful rewording; "
          "a result that is the same sentence, far from its length or silent on what it changed is not a lesson; a run goes on where the last stopped)")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a: selftest()
    elif a and a[0] == "show": show()
    elif len(a) == 2 and a[0] == "merge": print(f"teach: {merge(pathlib.Path(a[1]))} lessons that a run had saved while it went on were added"); show()
    elif a and a[0] == "requests":
        llm.LEDGER = OUT / "ledger.json"                               # its own count of the day's calls: the lane's ledger is not touched from this workflow
        for f in sorted((ROOT / "data" / "auto" / "requests").glob("teach-*.json")):
            try: r = json.load(open(f, encoding="utf-8"))
            except ValueError: r = {}
            f.unlink()
            ms = [m for m in (r.get("models") or []) if isinstance(m, str) and re.fullmatch(r"(?:gemini:|openrouter:)[A-Za-z0-9._/:-]{3,90}", m)] or None
            run(limit=int(r["max"]) if isinstance(r.get("max"), int) else 600, minutes=float(r["minutes"]) if isinstance(r.get("minutes"), (int, float)) else 40, models=ms,
                at_once=min(6, max(1, int(r["at_once"]))) if isinstance(r.get("at_once"), int) else 1)
        show()
    else: sys.exit(__doc__)
