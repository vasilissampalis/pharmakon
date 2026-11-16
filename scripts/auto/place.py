#!/usr/bin/env python3
"""Where a question, and the answer to it, belongs on the site (docs/AUTOMATION.md; the senior author, 16 November 2026,
13:52: the system should "taxinomize where the new information belongs, in which drug page, or if it belongs in the
statistics page, the test kit page, the emergency number, the general drug facts page all the pages that already exist
and the new pages it understands it should develop").

Words only, no model, so that it costs nothing, is the same every time and can be measured on real questions:
  python3 -I scripts/auto/place.py --eval      (the 400 forum questions of the gold set and the listed questions)
  python3 -I scripts/auto/place.py --selftest

place(question, ways) gives:
  home    the one page the answer lives on: a drug's page (its slug), "new:<page>" (a page the system should start: the
          drug has none), or one of the site's general pages: "interactions" (mixing), "numbers" (statistics),
          "checking" (drug checking, test kits, what is in a product), "law", "facts" (big questions about drugs),
          "emergency" (the system never writes there: the page is the senior author's, and such a question waits for a
          person; the place says where a visitor is pointed)
  also    other pages that list it (a statistics question about one drug lives on the drug's page and is listed under
          Statistics as well)
  drugs   the pages of the drugs it names; fresh: the names it holds of drugs that have no page; cls: the class a new
          page is filed under (data/auto/filing.json, the editor's filing)
  why     the words that decided it
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "insight"))

GENERAL = ("interactions", "numbers", "checking", "law", "facts", "emergency")
TOPIC = [   # (page, what in a question says so). The order is the order of a tie.
    ("checking", re.compile(r"\btest(?:ing)? kits?\b|\breagents?\b|\btest(?:ing)? strips?\b|\bfentanyl strips?\b|\bdrug checking\b|\bcheck(?:ing)? (?:my|your|the|a|if|whether)\b.{0,30}\b(?:drugs?|pills?|powder|tabs?|real|pure|laced|cut)\b"
                             r"|\bhow (?:do i|do you|can i|to) (?:test|check|tell if|know if)\b|\bpurity\b|\bhow pure\b|\bcut with\b|\blaced\b|\badulterat\w*|\bcontaminat\w*|\bfake\b|\bcounterfeit\b|\bgenuine\b|\bbe (?:checked|tested)\b|\breally (?:lsd|mdma|cocaine|ketamine|heroin|xanax)\b|\bpressed (?:pills?|bars?)\b|\bwhat(?:'s| is| are)(?: really| actually)? in\b", re.I)),
    ("numbers", re.compile(r"\bhow many (?:people|deaths|users|adults|teens|students|americans|europeans|percent)\b|\bhow common\b|\bhow (?:often|frequently) do people\b|\bwhat (?:percent\w*|share|proportion|fraction)\b|\bpercent(?:age)? of (?:people|users|adults|deaths)\b"
                            r"|\bstatistic\w*|\bprevalen\w*|\bmost (?:used|popular|common(?:ly used)?|widely used) drugs?\b|\bdeaths? (?:a|per|each|every) year\b|\bnumber of (?:deaths|people|users)\b|\bhow many die\b|\bdeath rates?\b|\brates? of (?:use|death|addiction|overdose)\b", re.I)),
    ("law", re.compile(r"\b(?:il)?legal(?:ly|ity|ized?|ised?|ization|isation)?\b|\blaws?\b|\bdecriminal\w*|\bpenalt\w*|\bprison\b|\bjail\b|\barrest\w*|\bschedule (?:[ivx]+|[1-5])\b|\bcontrolled substances?\b|\bpossession\b|\bprescription[- ]only\b|\bbanned\b|\bdrug[- ]driving\b", re.I)),
]
MIX = re.compile(r"\bmix(?:ing|ed|es)?\b|\bcombin\w+|\binteract\w*|\btogether\b|\bat the same time\b|\bon top of\b|\bwhile (?:on|taking|drinking|using)\b|\b(?:taken|take|taking|used?|using|combined?) (?:\w+ ){0,2}with\b|\bwith (?:alcohol|booze|weed|my (?:meds|medication|antidepressants?|ssri))\b|\band alcohol\b|\bcandy ?flip\w*|\bhippie ?flip\w*|\bnexus ?flip\w*", re.I)
COMPARES = re.compile(r"\bcompar\w+|\bdiffer\w*|\bversus\b|\bvs\.?\b|\b(?:better|worse|stronger|weaker|safer|riskier|more \w+|less \w+) than\b|\bthe same as\b|\binstead of\b", re.I)      # two drugs set side by side are not two drugs taken together
PLAINLY_MIXED = re.compile(r"\bmix(?:ing|ed|es)?\b|\bcombin\w+|\btogether\b|\bat the same time\b|\binteract\w*", re.I)
OTHER_THING = re.compile(r"\b(?:meds|medications?|medicines?|antidepressants?|ssris?|snris?|maois?|antibiotics?|birth control|the pill|painkillers?|sleeping pills?|blood pressure (?:pills?|meds|medication)|adhd meds|energy drinks?|grapefruit|other drugs?|another drug|other substances?|other medicines?)\b", re.I)
ACT_NOW = re.compile(r"\bwhat (?:do i|do you|should i|should you|to) do (?:if|when) (?:someone|somebody|my friend|a friend|they|he|she|a person)\b|\bhow (?:do i|do you|can i|to) help (?:someone|somebody|a friend|my friend)\b|\bambulance\b|\b(?:911|112|999)\b"
                     r"|\bnot breathing\b|\bstopped breathing\b|\bwon'?t wake\b|\bunconscious\b|\brecovery position\b|\bpoison control\b|\bemergency (?:number|services|room|help)\b", re.I)      # a question about what to do now
OVERDOSE = re.compile(r"\boverdos\w*|\b(?:od|o\.d\.)(?:'?d|ing)?\b|\boveramp\w*|\bemergenc\w*|\bnaloxone\b|\bnarcan\b|\bpassed out\b|\bfatal\b|\blethal\b", re.I)                               # a question about an overdose: it lives on the drug's page, waits for a person, and points to the emergency page


def _filing():
    try: return json.load(open(ROOT / "data" / "auto" / "filing.json", encoding="utf-8"))["names"]
    except (OSError, ValueError, KeyError): return {}


def _chem():
    try: return re.compile(r"(?<![\w-])(?:" + json.load(open(ROOT / "site" / "insight" / "scope.json", encoding="utf-8"))["chem"] + r")(?![\w-])", re.I)
    except (OSError, ValueError, KeyError): return None


class Placer:
    """names: [[name, [slugs]]] of the drugs that have a page, the longest name first (build_index.names_table());
    filing: the names of drugs without a page and where each belongs (data/auto/filing.json)."""

    def __init__(self, names=None, filing=None, chem=None):
        if names is None:
            import build_index as bi; names = bi.names_table()
        one = lambda n: (re.escape(n[:-1]) + "s?") if n.endswith("s") and len(n) > 5 and not n.endswith("ss") else (re.escape(n) + "s?")        # "synthetic cannabinoid" and "synthetic cannabinoids" are one name
        self.names = [(n, ss, re.compile(r"(?<![\w-])" + one(n) + r"(?![\w-])", re.I)) for n, ss in names]
        try: self.shapes = [(re.compile(x["shape"], re.I), x) for x in json.load(open(ROOT / "data" / "auto" / "filing.json", encoding="utf-8")).get("shapes") or []]
        except (OSError, ValueError): self.shapes = []
        self.filing = [(n, v, re.compile(r"(?<![\w-])" + re.escape(n) + r"(?![\w-])", re.I)) for n, v in sorted((filing if filing is not None else _filing()).items(), key=lambda kv: -len(kv[0]))]
        self.chem = chem if chem is not None else _chem()

    def pages_to_start(self):
        """Every page the filing names for drugs that have none (data/auto/filing.json, "pages")."""
        try: return list(json.load(open(ROOT / "data" / "auto" / "filing.json", encoding="utf-8")).get("pages") or [])
        except (OSError, ValueError): return []

    def read(self, text):
        """(the pages of the drugs named, in the order they are named; the names of drugs without a page, with where each belongs)."""
        found, taken, fresh = [], [], []
        def free(m): return not any(a < m.end() and m.start() < b for a, b in taken)
        for n, v, rx in self.filing:                                    # a longer name is read before a shorter one inside it ("nicotine pouches" before "nicotine")
            for m in rx.finditer(text):
                if free(m): taken.append(m.span()); fresh.append((m.start(), n, v))
        for n, ss, rx in self.names:
            for m in rx.finditer(text):
                if free(m):
                    taken.append(m.span())
                    if len(ss) <= 2: found += [(m.start(), s) for s in ss]      # (a family's name, "opioids", names a class, not a page)
        if self.chem:
            for m in self.chem.finditer(text):
                if free(m):
                    nm = m.group(0).lower(); by = next((x for rx, x in self.shapes if rx.search(nm)), None)      # a name known by its shape: where names of that shape belong
                    taken.append(m.span()); fresh.append((m.start(), nm, ({"page": by["page"]} if by and by.get("page") else {"new": by["new"], "cls": by.get("cls")} if by else {"new": m.group(0).upper(), "cls": None})))
        pages = []
        for _, s in sorted(found):
            if s not in pages: pages.append(s)
        self.first = min([p for p, _ in found] or [10 ** 6]), min([p for p, n, v in fresh if v.get("new")] or [10 ** 6])      # where the first drug with a page, and the first without, stand
        return pages, [(n, v) for _, n, v in sorted(fresh, key=lambda x: x[0])]

    def place(self, question, ways=()):
        q = re.sub(r"\s+", " ", str(question)).strip(); text = " ".join([q] + [str(w) for w in ways])
        pages, fresh = self.read(q)                                     # what the question itself names decides; its other wordings only add
        if not pages and not fresh: pages, fresh = self.read(text)
        on_page = [v["page"] for n, v in fresh if v.get("page") and v["page"] not in GENERAL]      # a name without a page that belongs on a page that exists
        to_start = [(v["new"], v.get("cls")) for n, v in fresh if v.get("new")]
        drugs = list(dict.fromkeys(pages + on_page)); topics = [t for t, rx in TOPIC if rx.search(q)]
        things = len(set(drugs)) + len({p for p, _ in to_start}) + (1 if OTHER_THING.search(q) else 0) + (1 if re.search(r"\b(?:alcohol|booze|drinking|drunk|beer|wine)\b", q, re.I) and "alcohol" not in drugs else 0)
        out = {"home": None, "also": [], "drugs": drugs, "fresh": [n for n, v in fresh], "cls": None, "why": ""}
        def home(h, why): out["home"] = h; out["why"] = why
        if ACT_NOW.search(q): home("emergency", "it asks what to do in an emergency: that page is the senior author's own, the system never writes there, and the answer waits for a person")
        elif any(v.get("page") == "interactions" for n, v in fresh) or (MIX.search(q) and things >= 2 and (PLAINLY_MIXED.search(q) or not COMPARES.search(q))): home("interactions", "it asks about two things taken together")
        elif drugs and not (to_start and self.first[1] < self.first[0] and not on_page): home(drugs[0], "it names a drug that has a page" + (" (" + ", ".join(n for n, v in fresh if v.get("page") == drugs[0]) + " belongs there)" if drugs[0] in on_page and drugs[0] not in pages else ""))
        elif to_start: home("new:" + to_start[0][0], "it names a drug that has no page yet"); out["cls"] = to_start[0][1]
        elif topics: home(topics[0], "no one drug is named, and it asks about " + {"checking": "what is in a product or how to check it", "numbers": "how many or how common", "law": "the law"}[topics[0]])
        else: home("facts", "no one drug is named: a question about drugs in general")
        out["also"] = [x for x in dict.fromkeys(drugs + ["new:" + p for p, _ in to_start] + topics + (["emergency"] if OVERDOSE.search(q) else [])) if x != out["home"]]
        out["waits"] = bool(ACT_NOW.search(q) or OVERDOSE.search(q))      # (the lane's own rule decides what waits for a person; this only says why a visitor is pointed to the emergency page)
        return out


def selftest():
    names = [["crystal meth", ["methamphetamine"]], ["ketamine", ["ketamine"]], ["cocaine", ["cocaine"]], ["alcohol", ["alcohol"]], ["nicotine", ["nicotine"]], ["heroin", ["heroin"]], ["xanax", ["benzodiazepines"]], ["mdma", ["mdma"]], ["lsd", ["lsd"]], ["weed", ["cannabis"]],
             ["opioids", ["heroin", "fentanyl-and-analogues", "prescription-opioids", "methadone-buprenorphine", "kratom"]], ["meth", ["methamphetamine"]]]
    filing = {"nicotine pouches": {"page": "nicotine"}, "lorazepam": {"page": "benzodiazepines"}, "pregabalin": {"new": "Gabapentinoids (gabapentin, pregabalin)", "cls": "Depressants"}, "speedball": {"page": "interactions"}, "entheogens": {"page": "facts"}}
    P = Placer(names, filing, re.compile(r"(?<![\w-])(?:\d-?(?:fa|mmc))(?![\w-])", re.I)); pl = lambda q, w=(): P.place(q, w)
    assert pl("Can you get addicted to ketamine?")["home"] == "ketamine" and pl("Is crystal meth worse than cocaine?") == dict(pl("Is crystal meth worse than cocaine?"), home="methamphetamine", also=["cocaine"])
    assert pl("Are nicotine pouches bad for your gums?")["home"] == "nicotine" and "nicotine pouches belongs there" in pl("Are nicotine pouches bad for your gums?")["why"] and pl("Is lorazepam stronger than xanax?")["home"] == "benzodiazepines"
    r = pl("Is pregabalin addictive?"); assert r["home"] == "new:Gabapentinoids (gabapentin, pregabalin)" and r["cls"] == "Depressants" and r["fresh"] == ["pregabalin"], r
    r = pl("What does 3-MMC feel like?"); assert r["home"] in ("new:3-MMC", "synthetic-cathinones"), r      # (by its shape it belongs with the synthetic cathinones, where the filing says so)
    assert pl("Is it dangerous to mix cocaine and alcohol?")["home"] == "interactions" and pl("Can I drink on ketamine?")["home"] == "ketamine" and pl("What happens if you take MDMA while on antidepressants?")["home"] == "interactions" and pl("What is a speedball?")["home"] == "interactions"
    assert pl("How many people use cocaine?") == dict(pl("How many people use cocaine?"), home="cocaine", also=["numbers"]) and pl("What are the most used drugs in Europe?")["home"] == "numbers"
    assert pl("How do test kits work?")["home"] == "checking" and pl("What is really in fake Xanax bars?") == dict(pl("What is really in fake Xanax bars?"), home="benzodiazepines", also=["checking"]) and pl("Is LSD legal anywhere?") == dict(pl("Is LSD legal anywhere?"), home="lsd", also=["law"])
    r = pl("What is pregabalin like, and how does it compare with weed?"); assert r["home"].startswith("new:Gabapentinoids") and r["also"] == ["cannabis"], r      # the thing named first decides
    assert pl("What happens when cocaine is combined with other drugs?")["home"] == "interactions" and pl("What happens when MDMA is taken with antidepressants?")["home"] == "interactions"
    r = pl("Can you overdose on LSD?"); assert r["home"] == "lsd" and r["also"] == ["emergency"] and r["waits"], r
    assert pl("What are the effects of a synthetic cannabinoid product?", ())["home"] == "facts"        # (this pretend table has no such name)
    assert pl("What happens when cocaine and MDMA are taken together?")["also"] == ["cocaine", "mdma"]
    assert pl("What should I do if someone overdoses on heroin?")["home"] == "emergency" and pl("Why do people take drugs?")["home"] == "facts" and pl("Are opioids all the same?")["home"] == "facts" and pl("What are entheogens?")["home"] == "facts"
    assert pl("Does it damage the bladder?", ["does ketamine hurt your bladder"])["home"] == "ketamine"       # (what the question itself does not name, its other wordings may)
    f = _filing(); sc = json.load(open(ROOT / "site" / "insight" / "scope.json", encoding="utf-8")); sub = {s["slug"] for s in json.load(open(ROOT / "data" / "site" / "substances.json", encoding="utf-8"))}
    assert set(f) == set(sc["names"]) and all((v.get("page") in sub | set(GENERAL)) if "page" in v else (v.get("new") and v.get("cls")) for v in f.values())        # every name the site knows is filed, on a page that exists or on one to start
    print("place selftest: ok (a drug's page, a name without a page on the page it belongs to, a page to start with its class, mixing, statistics, checking, law, emergency, general; every known name is filed)")


def evaluate():
    import collections
    P = Placer(); rows = []
    gold = json.load(open(ROOT / "data" / "verification" / "insight" / "gold-sample.json", encoding="utf-8"))["questions"]
    for g in gold: rows.append(("forum", g.get("q") or g.get("question") or g.get("text") or ""))
    for w in json.load(open(ROOT / "data" / "site" / "wanted.json", encoding="utf-8"))["items"]: rows.append(("listed", w["q"]))
    out = {"_note": "Where scripts/auto/place.py puts real questions: the 400 forum questions of the gold set and the listed questions. Made by --eval; read by the editor.", "counts": {}, "new_pages": {}, "rows": []}
    for kind, q in rows:
        r = P.place(q); out["rows"].append({"from": kind, "q": q, "home": r["home"], "also": r["also"], "why": r["why"]})
    c = collections.Counter(("a drug's page" if r["home"] not in GENERAL and not r["home"].startswith("new:") else "a page to start" if r["home"].startswith("new:") else r["home"]) for r in out["rows"])
    out["counts"] = dict(c.most_common()); out["new_pages"] = dict(collections.Counter(r["home"][4:] for r in out["rows"] if r["home"].startswith("new:")).most_common())
    (ROOT / "data" / "auto" / "place-eval.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"place: {len(rows)} questions:", "; ".join(f"{k} {v}" for k, v in c.most_common())); print("pages to start, by how many questions ask:", out["new_pages"])


def pages():
    """The pages the system should start, by how much people ask (data/auto/pages.json): from every listed question (the
    editors' list and the system's own, which holds what visitors sent) and, as a first sign of demand, from the forum
    questions of the gold set. Demand first: a page is started because people ask, never because a paper exists."""
    P = Placer(); out = {}
    def add(q, wid, kind):
        r = P.place(q)
        for h in [r["home"]] + r["also"]:
            if h.startswith("new:"):
                e = out.setdefault(h[4:], {"cls": None, "listed": [], "forum": 0})
                e["cls"] = e["cls"] or (r["cls"] if h == r["home"] else next((v.get("cls") for n, v, rx in P.filing if v.get("new") == h[4:]), None) or next((x.get("cls") for rx, x in P.shapes if x.get("new") == h[4:]), None))
                if kind == "listed": e["listed"].append(wid)
                else: e["forum"] += 1
    for f in ("data/site/wanted.json", "data/auto/wanted-auto.json"):
        try: items = json.load(open(ROOT / f, encoding="utf-8")).get("items") or []
        except (OSError, ValueError): items = []
        for w in items: add(w["q"], w["id"], "listed")
    for g in json.load(open(ROOT / "data" / "verification" / "insight" / "gold-sample.json", encoding="utf-8"))["questions"]: add(g.get("q") or g.get("question") or g.get("text") or "", None, "forum")
    # (16 November 2026) every page the filing names is in the list, also one nobody has asked us about yet; among pages our own evidence does not
    # tell apart, the one more people look up on Wikipedia comes first (data/auto/demand-wiki.json, scripts/auto/wiki_views.py)
    try: wiki = json.load(open(ROOT / "data" / "auto" / "demand-wiki.json", encoding="utf-8")).get("pages") or {}
    except (OSError, ValueError): wiki = {}
    for name in P.pages_to_start():
        e = out.setdefault(name, {"cls": next((v.get("cls") for n, v, rx in P.filing if v.get("new") == name), None) or next((x.get("cls") for rx, x in P.shapes if x.get("new") == name), None), "listed": [], "forum": 0})
    for name, e in out.items(): e["looked_up"] = int((wiki.get(name) or {}).get("views") or 0)
    doc = {"_note": "The pages the system should start: drugs and medicines people ask about that have no page (scripts/auto/place.py --pages; data/auto/filing.json says which names belong to which page). 'listed': the listed questions that belong there (the editors' and those visitors sent); "
                    "'forum': how many of the 400 forum questions of the gold set ask about it; 'looked_up': how often people opened its articles on the English Wikipedia in twelve months (data/auto/demand-wiki.json). "
                    "Ranked by what people asked us first (listed, then forum); pages that this does not tell apart, by how often they are looked up. A page is started because people ask.",
           "pages": dict(sorted(out.items(), key=lambda kv: (-len(kv[1]["listed"]), -kv[1]["forum"], -kv[1]["looked_up"], kv[0])))}
    (ROOT / "data" / "auto" / "pages.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"pages to start: {len(out)}; first in line:", "; ".join(f"{k} ({len(v['listed'])} listed, {v['forum']} forum, {v['looked_up']:,} looked up)" for k, v in list(doc["pages"].items())[:8]))


if __name__ == "__main__":
    if "--selftest" in sys.argv: selftest()
    elif "--eval" in sys.argv: evaluate()
    elif "--pages" in sys.argv: pages()
    else: print(json.dumps(Placer().place(" ".join(a for a in sys.argv[1:] if not a.startswith("--"))), ensure_ascii=False, indent=1))
