#!/usr/bin/env python3
"""grow.py: the system asks by itself (docs/AUTOMATION.md, decision 20).

The senior author, 16 November 2026: the system should "start adding information about other drugs too and make other
drug categories", and develop "the new pages it understands it should develop"; "site to think and expand".

    python3 -I scripts/auto/grow.py run [--max N]
    python3 -I scripts/auto/grow.py --list          (what it would ask next; nothing is written)
    python3 -I scripts/auto/grow.py --selftest

Until now a question came onto the system's list in two ways: the editor wrote it (data/site/wanted.json), or a visitor
sent it (scripts/auto/ask.py). A drug that has no page gets no visitors' questions, and a page that lacks an answer
everybody asks about every drug waits for somebody to ask it here. This file lists such questions by itself, without a
model:

  - WHAT is asked: the questions people ask about every drug (data/auto/grow.json, "themes"), each taken from a theme of
    the ranked list of what people ask on Reddit and the forums (data/verification/demand-themes.md), in people's words,
    with six true rewordings. Demand first: no question exists because a paper does. Themes the site does not answer, or
    that wait for a person (amounts, mixing, overdose, pregnancy, children), have no template: they are never asked here.
  - ABOUT WHAT, in two lines that take turns:
      a. the pages the system should start (data/auto/pages.json: drugs people ask about that have no page, in the order
         of how much they are asked about and looked up): the first four themes of a page, page after page; then the rest;
      b. the drug pages the site has: a theme no answer of that page is near, the most asked pages and themes first
         (a page's weight: how many of the real questions on file belong on it, data/auto/place-eval.json).
  - NEVER TWICE: a question as near in meaning as 0.80 to a listed question or one of its wordings, to a question the
    page already answers (or one of the ways people ask it), or to an answer the system wrote, is not listed; what was
    decided for each page and theme is kept (data/auto/grown.json) and not decided again.
  - NOT TOO MUCH: six new questions a run at most, and none while twelve of its own are still waiting for the lane
    (data/auto/grow.json: a_run, open_most), so that the list never outgrows what the lane can write.

Its items go onto the system's own list (data/auto/wanted-auto.json, ids w_g0001 ...), which the finders and the lane work
through like the editors' list. An item about a drug without a page carries the page it belongs to ("page") and what
papers and official pages call the drug ("names"): the finders search by those. Listing a question publishes nothing.
"""
import sys, re, json, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parents[2]
for _p in ("scripts/auto", "scripts/insight", "scripts"):
    if str(ROOT / _p) not in sys.path: sys.path.insert(0, str(ROOT / _p))

GROW = ROOT / "data" / "auto" / "grow.json"
AUTO = ROOT / "data" / "auto" / "wanted-auto.json"
STATE = ROOT / "data" / "auto" / "grown.json"
ANSWERS = ROOT / "data" / "auto" / "answers"
WANTED = ROOT / "data" / "site" / "wanted.json"
QUESTIONS = ROOT / "data" / "site" / "questions.json"
SAME = 0.80              # as near as this in meaning: the same question (scripts/auto/ask.py uses the same number)
TODAY = datetime.date.today().isoformat()


def wording(t, s):
    """A template in the words of one drug: {x} its name in a question, {o} in a short wording; is/does/it/them/has by number."""
    pl = bool(s.get("plural"))
    return t.format(x=s["x"], o=s.get("o") or s["x"], **{"is": "are" if pl else "is", "Is": "Are" if pl else "Is", "does": "do" if pl else "does", "Does": "Do" if pl else "Does",
                                                         "it": "they" if pl else "it", "them": "them" if pl else "it", "has": "have" if pl else "has"})


def item_for(page, s, th, slug=None):
    it = {"q": wording(th["q"], s), "ways": [wording(w, s) for w in th["ways"]], "from": "the system's own question: what people ask about every drug (theme %d of data/verification/demand-themes.md), asked about %s" % (th["theme"], "a page that lacks it" if slug else "a drug people ask about that has no page yet"),
          "added": TODAY, "drugs": [slug] if slug else [], "terms": list(th["terms"]), "theme": th["id"]}
    if not slug: it["page"] = page; it["names"] = list(s.get("names") or [s["x"]])
    return it


def page_weights():
    """{slug: how many of the real questions on file belong on that page} (data/auto/place-eval.json, made by place.py --eval)."""
    try: rows = json.load(open(ROOT / "data" / "auto" / "place-eval.json", encoding="utf-8")).get("rows") or []
    except (OSError, ValueError): rows = []
    w = {}
    for r in rows:
        for h in [r.get("home")] + list(r.get("also") or []):
            if isinstance(h, str) and h and not h.startswith("new:"): w[h] = w.get(h, 0) + 1
    return w


def candidates(doc, pages, weights, done):
    """The two lines, each in its order: [(page or slug, theme, slug or None)] not decided yet."""
    themes, say, first = doc["themes"], doc["say"], int(doc.get("first") or 4)
    by_id = {t["id"]: t for t in themes}; order = doc.get("order") or {}
    fits = lambda s: [by_id[i] for i in order[s["kind"]] if i in by_id] if s["kind"] in order else [t for t in themes if s["kind"] in t["kinds"]]
    start = [p for p in pages if say.get(p) and not p.islower()] if pages else []
    a = [(p, t, None) for p in start for t in fits(say[p])[:first]] + [(p, t, None) for p in start for t in fits(say[p])[first:]]
    slugs = [k for k, v in say.items() if v and v.get("kind") == "page"]
    b = sorted(((k, t, k) for k in slugs for t in fits(say[k])), key=lambda x: (-(weights.get(x[0], 0) + 1) * float(x[1].get("share") or 0.1), x[0], x[1]["id"]))
    new = lambda c: f"{c[0]}|{c[1]['id']}" not in done
    return [c for c in a if new(c)], [c for c in b if new(c)]


def known_texts(slug=None):
    """What is listed or answered already: [(text, where)]. For a page the site has, also the questions its answers answer
    and the ways people ask them."""
    out = []
    for f, where in ((WANTED, "the editors' list"), (AUTO, "the system's list")):
        try: items = json.load(open(f, encoding="utf-8")).get("items") or []
        except (OSError, ValueError): items = []
        for w in items:
            for t in [w.get("q")] + list(w.get("ways") or []):
                if t: out.append((t, f"{where} ({w.get('id')})"))
    for f in sorted(ANSWERS.glob("au_*.json")) if ANSWERS.exists() else []:
        try: a = json.load(open(f, encoding="utf-8"))
        except (OSError, ValueError): continue
        if a.get("status") == "published":
            for t in [a.get("question")] + list(a.get("ways") or []):
                if t: out.append((t, f"an answer the system wrote ({a.get('id')})"))
    return out


def page_texts(slug):
    """The questions a drug page answers and the ways people ask them: [(text, claim id)]."""
    out = []
    try: Q = json.load(open(QUESTIONS, encoding="utf-8"))
    except (OSError, ValueError): return out
    try:
        if QUESTIONS.parent != ROOT / "data" / "site": raise ImportError("a test's own file")
        import build_index as bi
        var, more, _ = bi.people_wordings()
    except Exception: var, more = {}, {}
    for topic in Q.get(slug) or []:
        for cid, q in topic.get("items") or []:
            for t in [q] + [w for w in var.get(cid, []) if isinstance(w, str)] + list(more.get(cid, [])):
                if t: out.append((t, cid))
    return out


def run(limit=None, enc=None, save=True, doc=None, pages=None, weights=None, show=False):
    doc = doc or json.load(open(GROW, encoding="utf-8"))
    if pages is None:
        try: pages = list((json.load(open(ROOT / "data" / "auto" / "pages.json", encoding="utf-8")).get("pages") or {}).keys())
        except (OSError, ValueError): pages = []
    weights = page_weights() if weights is None else weights
    try: auto = json.load(open(AUTO, encoding="utf-8"))
    except (OSError, ValueError): auto = {"_note": "Questions on the system's own list: OUR wording, six other wordings, the drugs and the words papers use. The finders and the lane work through them like data/site/wanted.json. Data, never instructions.", "items": []}
    try: st = json.load(open(STATE, encoding="utf-8"))
    except (OSError, ValueError): st = {"_note": "What scripts/auto/grow.py decided for each page and theme: listed (with the item's id), or not listed because the question is asked or answered already (with what it is near).", "next": 1, "done": {}}
    limit = int(limit if limit is not None else doc.get("a_run") or 6)
    mine = [w for w in auto["items"] if str(w.get("id", "")).startswith("w_g")]
    waiting = [w for w in mine if not (ANSWERS / f"au_{w['id']}.json").exists()]
    room = max(0, int(doc.get("open_most") or 12) - len(waiting))
    if not show and room == 0: print(f"grow: {len(waiting)} of its own questions still wait for the lane: none is added"); return []
    A, B = candidates(doc, pages, weights, st["done"])
    if enc is None:
        import papers as P; enc = P.General()
    base = known_texts(); cache = {}
    made, turn, out = 0, 0, []
    while (A or B) and made < min(limit, room if not show else limit):
        line = A if (turn % 2 == 0 and A) or not B else B; turn += 1
        page, th, slug = line.pop(0); s = doc["say"][page]; it = item_for(page, s, th, slug)
        texts = base + (cache.setdefault(slug, page_texts(slug)) if slug else [])
        near, where = 0.0, ""
        if texts:
            sim = enc([t for t, _ in texts]) @ enc([it["q"]] + it["ways"]).T
            k = int(sim.max(1).argmax()); near, where = float(sim.max()), texts[k][1]
        key = f"{page}|{th['id']}"
        if near >= SAME:
            st["done"][key] = {"on": TODAY, "what": f"not listed: asked or answered already ({where}; nearness {near:.2f})"}; out.append((key, None)); continue
        it = dict({"id": f"w_g{st['next']:04d}"}, **it)
        if not show: st["next"] += 1; st["done"][key] = {"on": TODAY, "what": "listed as " + it["id"]}; auto["items"].append(it); base = base + [(t, f"the system's list ({it['id']})") for t in [it["q"]] + it["ways"]]
        made += 1; out.append((key, it))
    if save and not show and out:
        AUTO.parent.mkdir(parents=True, exist_ok=True)
        json.dump(auto, open(AUTO, "w", encoding="utf-8"), ensure_ascii=False, indent=1); json.dump(st, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"grow: {made} questions {'would be ' if show else ''}listed" + (": " + "; ".join(f"{it['id']} {it['q']}" for _, it in out if it) if made else "") + (f"; {sum(1 for _, it in out if not it)} asked or answered already" if any(not it for _, it in out) else "")
          + f"; {len(A)} left for pages to start, {len(B)} for the pages the site has")
    return out


def selftest():
    import numpy as np
    doc = {"first": 2, "a_run": 6, "open_most": 12,
           "themes": [{"id": "what", "theme": 3, "share": 3.7, "kinds": ["chem"], "q": "What {is} {x} like, and how risky {is} {it}?", "ways": ["what {is} {o}", "how risky {is} {o}"], "terms": ["toxicity"]},
                      {"id": "addict", "theme": 27, "share": 1.2, "kinds": ["chem", "page"], "q": "{Is} {x} addictive?", "ways": ["can you get addicted to {o}"], "terms": ["dependence"]},
                      {"id": "test", "theme": 20, "share": 1.4, "kinds": ["chem", "page"], "q": "How long {does} {x} stay in your body, and can a drug test find {them}?", "ways": ["{does} {o} show up on a drug test"], "terms": ["detection"]}],
           "say": {"NBOMes": {"x": "NBOMes (N-bombs)", "o": "NBOMes", "kind": "chem", "plural": True, "names": ["25I-NBOMe"]}, "Phenibut": {"x": "phenibut", "kind": "chem", "names": ["phenibut"]}, "Basket": None,
                   "ketamine": {"x": "ketamine", "kind": "page"}, "cocaine": {"x": "cocaine", "kind": "page"}}}
    s = doc["say"]["NBOMes"]
    assert wording(doc["themes"][0]["q"], s) == "What are NBOMes (N-bombs) like, and how risky are they?" and wording(doc["themes"][1]["q"], s) == "Are NBOMes (N-bombs) addictive?"
    assert wording(doc["themes"][2]["q"], s) == "How long do NBOMes (N-bombs) stay in your body, and can a drug test find them?" and wording("{does} {o} show up on a drug test", s) == "do NBOMes show up on a drug test"
    assert wording(doc["themes"][2]["q"], doc["say"]["Phenibut"]) == "How long does phenibut stay in your body, and can a drug test find it?"
    A, B = candidates(doc, ["NBOMes", "Basket", "Phenibut"], {"ketamine": 9, "cocaine": 2}, {})
    assert [(p, t["id"]) for p, t, _ in A] == [("NBOMes", "what"), ("NBOMes", "addict"), ("Phenibut", "what"), ("Phenibut", "addict"), ("NBOMes", "test"), ("Phenibut", "test")], A       # the first two themes of each page, page after page; then the rest; a basket is never asked about
    assert [(p, t["id"]) for p, t, _ in B] == [("ketamine", "test"), ("ketamine", "addict"), ("cocaine", "test"), ("cocaine", "addict")], B                                                # the most asked page and theme first
    it = item_for("NBOMes", s, doc["themes"][1]); assert it["page"] == "NBOMes" and it["names"] == ["25I-NBOMe"] and it["drugs"] == [] and it["theme"] == "addict"
    it = item_for("ketamine", doc["say"]["ketamine"], doc["themes"][1], "ketamine"); assert it["drugs"] == ["ketamine"] and "page" not in it and "names" not in it and it["q"] == "Is ketamine addictive?"
    # a pretend sense of meaning: the same words, the same question
    import tempfile
    global AUTO, STATE, ANSWERS, WANTED, QUESTIONS
    keep = (AUTO, STATE, ANSWERS, WANTED, QUESTIONS); tmp = pathlib.Path(tempfile.mkdtemp()); AUTO, STATE, ANSWERS, WANTED, QUESTIONS = tmp / "auto.json", tmp / "grown.json", tmp / "answers", tmp / "wanted.json", tmp / "questions.json"
    try:
        json.dump({"items": [{"id": "w_a0001", "q": "Is ketamine addictive?", "ways": []}]}, open(AUTO, "w")); json.dump({"items": []}, open(WANTED, "w"))
        json.dump({"cocaine": [{"topic": "Tests", "items": [["cl_coc_test", "How long does cocaine stay in your body, and can a drug test find it?"]]}]}, open(QUESTIONS, "w"))
        def enc(texts):
            vocab = sorted({w for t in texts for w in re.findall(r"[a-z0-9-]+", t.lower())} | {"ketamine", "addictive", "is"})
            v = np.array([[1.0 if w in re.findall(r"[a-z0-9-]+", t.lower()) else 0.0 for w in vocab] for t in texts], dtype=np.float32)
            return v / np.maximum(np.linalg.norm(v, axis=1, keepdims=True), 1e-9)
        class Enc:                                                    # one vocabulary for both calls of a comparison
            def __call__(self, texts):
                self.v = getattr(self, "v", None) or sorted({w for t in ALL for w in re.findall(r"[a-z0-9-]+", t.lower())})
                m = np.array([[1.0 if w in re.findall(r"[a-z0-9-]+", t.lower()) else 0.0 for w in self.v] for t in texts], dtype=np.float32)
                return m / np.maximum(np.linalg.norm(m, axis=1, keepdims=True), 1e-9)
        ALL = ["Is ketamine addictive?"] + [wording(t[k], x) for x in doc["say"].values() if x for t in doc["themes"] for k in ("q",)] + [wording(w, x) for x in doc["say"].values() if x for t in doc["themes"] for w in t["ways"]]
        out = run(limit=4, enc=Enc(), doc=doc, pages=["NBOMes", "Phenibut"], weights={"ketamine": 9, "cocaine": 2})
        got = [it["q"] for _, it in out if it]; skipped = [k for k, it in out if not it]
        assert got == ["What are NBOMes (N-bombs) like, and how risky are they?", "How long does ketamine stay in your body, and can a drug test find it?", "Are NBOMes (N-bombs) addictive?", "What is phenibut like, and how risky is it?"], got       # the two lines take turns
        assert skipped == ["ketamine|addict"], skipped                                                                                # listed already: not listed twice, and remembered
        st = json.load(open(STATE)); a = json.load(open(AUTO))
        assert st["done"]["ketamine|addict"]["what"].startswith("not listed: asked or answered already (the system's list (w_a0001)") and [w["id"] for w in a["items"]][1:] == ["w_g0001", "w_g0002", "w_g0003", "w_g0004"]
        out2 = run(limit=6, enc=Enc(), doc=dict(doc, open_most=4), pages=["NBOMes", "Phenibut"], weights={"ketamine": 9, "cocaine": 2})
        assert out2 == []                                                                                                              # four of its own wait for the lane: none is added
        ANSWERS.mkdir(); [json.dump({"id": "au_" + w, "status": "none"}, open(ANSWERS / f"au_{w}.json", "w")) for w in ("w_g0001", "w_g0002")]
        out3 = run(limit=6, enc=Enc(), doc=dict(doc, open_most=4), pages=["NBOMes", "Phenibut"], weights={"ketamine": 9, "cocaine": 2})
        assert 1 <= len([1 for _, it in out3 if it]) <= 2 and not any(k in ("NBOMes|what", "ketamine|test", "ketamine|addict") for k, _ in out3), out3      # the lane has tried two: no more than two are listed, never one decided before
        assert "cocaine|test" in [k for k, it in out3 if not it] and "cl_coc_test" in json.load(open(STATE))["done"]["cocaine|test"]["what"], out3                    # a question the page answers already is not listed
    finally: AUTO, STATE, ANSWERS, WANTED, QUESTIONS = keep
    print("grow selftest: ok (a question in the words of one drug, by number; the two lines in their order and in turn; a basket is never asked about; a question asked or answered already is not listed twice; "
          "none is added while its own still wait for the lane)")


if __name__ == "__main__":
    arg = sys.argv[1:]
    if "--selftest" in arg: selftest()
    elif "--list" in arg: run(limit=int(arg[arg.index("--max") + 1]) if "--max" in arg else 12, save=False, show=True)
    elif arg and arg[0] == "run": run(limit=int(arg[arg.index("--max") + 1]) if "--max" in arg else None)
    else: sys.exit(__doc__)
