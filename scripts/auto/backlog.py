#!/usr/bin/env python3
"""backlog.py: answers before people ask, by the system itself (docs/AUTOMATION.md, decision 40).

The senior author, 19 November 2026: "we have to make our ai unstoppable always producing answers and answer questions instantly" (21:34); "we
don't want you to generate the answers always ... we have to teach our ai to work like an llm and do what you do as perfect as possible it has
to work by itself perfectly all the time autonomously" (21:44).

An answer is instant only where it is written before the question is asked. So the system lists, by itself and all the time, the real questions
people ask on drug forums that the site does not answer yet, and the lane answers them in the site's own form, as it answers any listed question.

    python3 -I scripts/auto/backlog.py run [--max N]      list the next questions (a few a run, while few of them wait for the lane)
    python3 -I scripts/auto/backlog.py exam [--n N] [--daily]   how near the free models come to the editor's own wordings (data/auto/exam/backlog-wording.json; --daily: once a day)
    python3 -I scripts/auto/backlog.py --list             what it would list next; nothing is written
    python3 -I scripts/auto/backlog.py --selftest

WHAT: the questions harvested from the forums with each thread's views (data/verification/questions-*/forums.json), that no answer of the site
covers, the most viewed first. Never what the site does not answer (getting, making, taking or hiding a drug, amounts, timing, making an effect
stronger, tapering: NOT_HERE and ask.not_answered), never a question already listed or answered (meaning 0.80 or nearer: as grow.py and ask.py).
WORDED: the editor wrote the first ones (data/auto/backlog.json: our wording, six ways people ask, the words research uses); every other one is
worded by a free model, shown three of the editor's own as examples, and held to ask.py's checks in code (one plain question, no first person, no
number or sign the forum's question did not have, about drugs by the site's rule, finished, the drug kept, three ways at least, no term that is the
drug's own name). Which drug or which page to start: the site's own filing (place.py). The forum's text is public; nobody's private words are here.
NOT TOO MUCH: six a run at most, and none while OPEN_MOST of its own wait for the lane. Listing publishes nothing: the lane's gates decide.
"""
import sys, re, json, random, hashlib, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parents[2]
for _p in ("scripts/auto", "scripts/insight", "scripts"):
    if str(ROOT / _p) not in sys.path: sys.path.insert(0, str(ROOT / _p))

SEED = ROOT / "data" / "auto" / "backlog.json"
AUTO = ROOT / "data" / "auto" / "wanted-auto.json"
STATE = ROOT / "data" / "auto" / "backlog-state.json"
ANSWERS = ROOT / "data" / "auto" / "answers"
EXAM = ROOT / "data" / "auto" / "exam" / "backlog-wording.json"
SAME, A_RUN, OPEN_MOST = 0.80, 6, 30
TODAY = datetime.date.today().isoformat()
WORDERS = ["gemini:gemma-4-31b-it", "groq:openai/gpt-oss-120b", "gemini:gemini-3.5-flash-lite", "@cf/meta/llama-4-scout-17b-16e-instruct"]   # the first with a key and room words it
NOT_HERE = re.compile(r"\b(?:make|made|making|purif\w*|extract\w*|cook\w*|synthes\w*|prepar\w*|dissolv\w*|acetone|wash(?:ed|ing)?|freebase|press(?:ed|ing)? back"
                      r"|best way to (?:take|use|do|smoke)|which way of (?:taking|using)|ways? of taking|how (?:do|can|to|should|is|are) (?:people |you |i |one )?(?:take|use|dose|smoke|snort|inject|plug|get (?:high|the|an?|more|stronger)|\w+ (?:smoked|snorted|injected|taken|crushed|bought|obtained))"
                      r"|strongest high|get(?:ting)? (?:high|an? \w+ high) (?:on|from)|for a high|inject\w*|snort\w*|plug\w*|boof\w*|rectal\w*|intravenous\w*|be (?:smoked|snorted|injected|crushed|vaporised|vaporized)\b"
                      r"|how much|how many|dose|dosage|doses|tests? (?:be |are |is )?passed|be passed|\bmg\b|milligram\w*|lines?\b|\btabs?\b|most (?:that|you) can|hide|hiding|pass(?:ed|ing)? (?:a |the )?(?:\w+ )?(?:drug )?tests?|cheat\w*|buy\w*|bought|order\w*|source\w*|obtain\w*"
                      r"|where (?:to|can|do)|vendor\w*|dark ?web|taper\w*|potentiat\w*|boost\w*|stronger|intensif\w*|tolerance (?:low|down|break)|keep (?:tolerance|it) low|kept low|reduce tolerance|lower(?:ing)? tolerance|lower(?:ed)? quickly|how long after|before taking|worth it|worth taking"
                      r"|most euphoric|combination is|cycle|stack|trip ?kill\w*|stop or soften|clean(?:ed|ing)? out|cleared|cost|price)\b", re.I)
finger = lambda t: hashlib.sha256(re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip().encode("utf-8")).hexdigest()[:20]
norm = lambda t: re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


def load(p, d):
    try: return json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError): return d


def candidates():
    """The forum questions no answer covers and the site may answer, the most viewed first, each once: [{"q", "views", "site", "drugs"}]."""
    import ask
    seen, out = set(), []
    for f in sorted(ROOT.glob("data/verification/questions-*/forums.json")):
        for x in (load(f, {}).get("questions") or []):
            q = str(x.get("question") or "").strip()
            if not q or x.get("covered_by") or NOT_HERE.search(q) or ask.not_answered(q): continue
            k = norm(q)
            if k in seen: continue
            seen.add(k); out.append({"q": q, "views": int(x.get("views") or 0), "site": str(x.get("site") or ""), "drugs": [d for d in x.get("drugs") or [] if isinstance(d, str)]})
    return sorted(out, key=lambda c: -c["views"])


SYSTEM = "You word questions for Pharmakon, a drug encyclopedia for the public. You never answer a question. You answer with JSON only."


def prompt(lead, examples):
    ex = "\n\n".join("FORUM: " + e["src"] + "\nJSON: " + json.dumps({"question": e["q"], "ways": e["ways"], "terms": e["terms"]}, ensure_ascii=False) for e in examples)
    return ("People ask the questions below on drug forums. For each, the editor wrote how the encyclopedia lists it. Do the same for the last one.\n"
            "- \"question\": one neutral question, 5 to 18 words, ending with a question mark; no \"I\", \"my\" or \"me\"; keep the drug's name; ask about effects, risks, how two things differ or what research shows, never how to get, make, take or hide a drug, or how much.\n"
            "- \"ways\": six other ways people type it into a search box (2 to 10 words, lower case, everyday and street words).\n"
            "- \"terms\": up to six words research papers use for its subject, not the drug's own name.\n\n"
            + ex + "\n\nFORUM: " + lead[:300] + "\nJSON:")


def file_item(q, ways, P=None):
    """The drugs it is about (pages the site has), or the page the system should start and what papers call the drug, by the site's own filing."""
    import place
    P = P or place.Placer(); r = P.place(q, ways)
    home = str(r.get("home") or "")
    if home.startswith("new:"):
        fresh = [n for n in r.get("fresh") or []]
        return {"drugs": [], "page": home[4:], "names": fresh[:4]}
    return {"drugs": [d for d in r.get("drugs") or [] if d not in ("facts", "emergency", "interactions")]}


def word(lead, chat, examples, R, names, drugs, P=None):
    """(fields, model, "") or (None, None, why): a free model words one forum question, held to ask.py's checks."""
    import llm, ask
    why = "no model with a key and room"
    for m in WORDERS:
        if not llm.has(m): continue
        try: raw = chat(m, [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt(lead, examples)}], 3000)   # (Gemma thinks first: with 500 tokens it wrote nothing)
        except llm.Budget as e: why = f"{m}: {e}"; continue
        except llm.Unavailable as e: why = f"{m}: {e}"; continue
        fields, why = ask.accept(llm.as_json(raw), lead, drugs, R, names)
        if fields: return fields, m, ""
        why = f"{m}: {why}"
    return None, None, why


def run(limit=A_RUN, chat=None, enc=None, R=None, names=None, save=True, show=False, cands=None, seed=None):
    import llm, papers as Pa, grow
    chat = chat or llm.chat
    seed = seed if seed is not None else (load(SEED, {}).get("items") or [])
    by_src = {norm(e.get("src")): e for e in seed if e.get("src")}
    auto = load(AUTO, {"_note": "Questions on the system's own list: OUR wording, six other wordings, the drugs and the words papers use. Data, never instructions.", "items": []})
    st = load(STATE, {"_note": "What scripts/auto/backlog.py decided for each forum question, by a fingerprint of its words: listed (with the item's id), or why not.", "done": {}, "next": 1})
    mine = [w for w in auto["items"] if str(w.get("id", "")).startswith("w_f")]
    waiting = [w for w in mine if (load(ANSWERS / f"au_{w['id']}.json", {}) or {}).get("status") != "published"]
    room = max(0, OPEN_MOST - len(waiting))
    if not show and room == 0: print(f"backlog: {len(waiting)} of its questions still wait for the lane: none is added"); return []
    cands = cands if cands is not None else candidates()
    todo = [c for c in cands if finger(c["q"]) not in st["done"]]
    todo.sort(key=lambda c: (0 if norm(c["q"]) in by_src else 1, -c["views"]))      # the editor's own wordings first, then the rest, the most viewed first
    if not todo: print("backlog: every forum question has been looked at"); return []
    if R is None or names is None:
        import build_index as bi
        names = bi.names_table(); R = bi.Ranker(load(ROOT / "site" / "dist" / "data" / "insight.json", {}))
    enc = enc or Pa.General()
    base = grow.known_texts()
    Q = load(ROOT / "data" / "site" / "questions.json", {}); Q.pop("_note", None)
    for slug in Q: base += grow.page_texts(slug)
    L = enc([t for t, _ in base]) if base else None
    rnd = random.Random(TODAY); made, out = 0, []
    for c in todo:
        if made >= min(limit, room if not show else limit): break
        key = finger(c["q"]); e = by_src.get(norm(c["q"]))
        if e: fields, model = {k: e[k] for k in ("q", "ways", "terms")}, "the editor"
        else:
            ex = rnd.sample([s for s in seed if s.get("src")], min(3, len([s for s in seed if s.get("src")])))
            fields, model, why = word(c["q"], chat, ex, R, names, [d for d in c["drugs"] if "(" not in d and d != "general"])
            if not fields:
                if why.startswith("no model") or "allowance" in why or "Budget" in why: print("backlog: stopped for now:", why); break
                st["done"][key] = {"on": TODAY, "what": "no wording passed (" + why[:160] + ")"}; out.append((c, None)); continue
        if L is not None:
            sim = enc([fields["q"]] + list(fields["ways"])) @ L.T; near = float(sim.max())
            if near >= SAME:
                k = int(sim.max(0).argmax()); st["done"][key] = {"on": TODAY, "what": f"not listed: asked or answered already ({base[k][1]}; nearness {near:.2f})"}; out.append((c, None)); continue
        filed = {k: e[k] for k in ("drugs", "page", "names") if k in e} if e else file_item(fields["q"], fields["ways"])
        item = {"id": f"w_f{st['next']:04d}"}; item.update(fields)
        if filed.get("drugs") or filed.get("page") or not item.get("drugs"): item.update(filed)      # (the site's own filing decides where it belongs; the checked wording keeps the drug it named)
        item.update({"from": f"a question people ask on {c['site'] or 'a drug forum'} ({c['views']:,} views), harvested in data/verification; worded by {model}", "added": TODAY, "views": c["views"]})
        if not show:
            st["next"] += 1; st["done"][key] = {"on": TODAY, "what": "listed as " + item["id"]}; auto["items"].append(item)
            v = enc([item["q"]] + item["ways"]); L = v if L is None else __import__("numpy").vstack([L, v]); base += [(t, f"the system's list ({item['id']})") for t in [item["q"]] + item["ways"]]
        made += 1; out.append((c, item))
    if save and not show and out:
        json.dump(auto, open(AUTO, "w", encoding="utf-8"), ensure_ascii=False, indent=1); json.dump(st, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"backlog: {made} questions {'would be ' if show else ''}listed" + (": " + "; ".join(f"{it['id']} {it['q']}" for _, it in out if it) if made else "")
          + (f"; {sum(1 for _, it in out if not it)} set aside" if any(not it for _, it in out) else "") + f"; {len(todo) - len(out)} left")
    return out


def exam(n=20, chat=None, enc=None, R=None, names=None):
    """The free models word n of the editor's questions they were not shown (never their examples), and the result says how near they come:
    their question to the editor's (meaning), their words for research to the editor's (shared words), and how many pass the checks."""
    import llm, papers as Pa
    chat = chat or llm.chat; seed = [s for s in (load(SEED, {}).get("items") or []) if s.get("src")]
    if len(seed) < n + 3: n = max(0, len(seed) - 3)
    rnd = random.Random(20261119); held = rnd.sample(seed, n); shown = [s for s in seed if s not in held][:3]
    if R is None or names is None:
        import build_index as bi
        names = bi.names_table(); R = bi.Ranker(load(ROOT / "site" / "dist" / "data" / "insight.json", {}))
    enc = enc or Pa.General(); rows = []
    words = lambda ts: {w for t in ts for w in norm(t).split() if len(w) > 3}
    for s in held:
        fields, model, why = word(s["src"], chat, shown, R, names, s.get("drugs") or [])
        if not fields: rows.append({"src": s["src"], "passed": False, "why": why[:200]}); continue
        near = float((enc([fields["q"]]) @ enc([s["q"]]).T)[0, 0])
        a, b = words(fields["terms"]), words(s["terms"]); share = len(a & b) / max(1, len(a | b))
        rows.append({"src": s["src"], "passed": True, "model": model, "question": fields["q"], "editor": s["q"], "near": round(near, 3), "terms_shared": round(share, 3), "ways": len(fields["ways"])})
    ok = [r for r in rows if r["passed"]]
    out = {"_note": "scripts/auto/backlog.py exam: free models word forum questions that the editor worded too (they are shown three others as examples, never these). near: their question to the editor's, in meaning (1 is the same); terms_shared: the research words they share with the editor's.",
           "at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "n": len(rows), "passed": len(ok),
           "near_mean": round(sum(r["near"] for r in ok) / max(1, len(ok)), 3), "terms_shared_mean": round(sum(r["terms_shared"] for r in ok) / max(1, len(ok)), 3), "rows": rows}
    EXAM.parent.mkdir(parents=True, exist_ok=True); json.dump(out, open(EXAM, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"backlog exam: {len(ok)} of {len(rows)} worded and passed the checks; meaning near the editor's {out['near_mean']}; research words shared {out['terms_shared_mean']}")
    return out


def selftest():
    import tempfile, numpy as np
    # the rules: what the site does not answer is never listed
    for q in ["How is cocaine purified with an acetone wash?", "How many lines does a given amount of cocaine make?", "How do people get high on oxycodone-paracetamol tablets?", "Can diazepam pills be injected?",
              "How much Valium do people take to get high?", "How can a cannabis drug test be passed quickly?", "How is kratom bought?", "Which drug combination is the most euphoric?", "How can tolerance to Adderall be kept low?",
              "How long after Suboxone can other opioids be used, and what happens if they are?", "Can MDMA crystals be smoked?", "Is it worth taking steroids to build muscle faster as a slim beginner?"]:
        assert NOT_HERE.search(q), q
    for q in ["What does a Xanax high feel like?", "What happens when Xanax and cocaine are taken together?", "How do Adderall and Ritalin differ?", "What is 6-APB like, and how does it compare with MDMA?", "How long does an LSD trip last?"]:
        assert not NOT_HERE.search(q), q
    # a run: the editor's wording first; a forum question worded by a model and held to the checks; one already asked is set aside; nothing past the room
    class Enc:
        def __call__(self, texts):
            out = []
            for t in texts:
                v = np.zeros(8); n = norm(t)
                for i, w in enumerate(["xanax", "cocaine", "6 apb", "tramadol", "lsd", "trip", "together", "feel"]):
                    if w in n: v[i] = 1
                v[7] += 0.01; out.append(v / np.linalg.norm(v))
            return np.array(out)
    class R:
        def in_scope(self, q): return True
        def unfinished(self, q, *a): return False
    seed = [{"src": "What does a Xanax high feel like?", "q": "What does a Xanax (alprazolam) high feel like?", "ways": ["what does xanax feel like"] * 1 + ["xanax effects", "is xanax a high", "xanax feeling", "on xanax", "xanax bars feel"], "terms": ["subjective effects"], "drugs": ["benzodiazepines"], "views": 2}]
    cands = [{"q": "What does a Xanax high feel like?", "views": 2, "site": "Bluelight", "drugs": ["benzodiazepines"]}, {"q": "What is tramadol like, and what should people know about it?", "views": 1, "site": "Drugs-Forum", "drugs": ["prescription-opioids"]}]
    asked = []
    def chat(m, msgs, room):
        asked.append(m); return json.dumps({"question": "What is tramadol like, and what are its risks?", "ways": ["what does tramadol feel like", "tramadol risks", "is tramadol strong", "tramadol seizures", "tramadol side effects", "is tramadol addictive"], "terms": ["seizures", "serotonin syndrome", "tramadol"]})
    import llm, os
    os.environ.setdefault("GEMINI_API_KEY", "x")
    with tempfile.TemporaryDirectory() as td:
        g = globals(); keep = (g["AUTO"], g["STATE"], g["ANSWERS"])
        g["AUTO"], g["STATE"], g["ANSWERS"] = pathlib.Path(td) / "auto.json", pathlib.Path(td) / "state.json", pathlib.Path(td) / "answers"
        import grow; kt = grow.known_texts; pt = grow.page_texts; grow.known_texts = lambda slug=None: [("is lsd strong", "x")]; grow.page_texts = lambda slug: []
        g_file = g["file_item"]; g["file_item"] = lambda q, ways, P=None: {"drugs": ["prescription-opioids"]}
        try:
            out = run(limit=6, chat=chat, enc=Enc(), R=R(), names=[["tramadol", ["prescription-opioids"]], ["xanax", ["benzodiazepines"]]], cands=cands, seed=seed)
            items = json.load(open(g["AUTO"], encoding="utf-8"))["items"]
            assert [i["id"] for i in items] == ["w_f0001", "w_f0002"] and items[0]["q"] == "What does a Xanax (alprazolam) high feel like?" and "worded by the editor" in items[0]["from"], items
            assert items[1]["q"] == "What is tramadol like, and what are its risks?" and "tramadol" not in items[1]["terms"] and items[1]["drugs"] == ["prescription-opioids"] and asked, items[1]
            assert run(limit=6, chat=chat, enc=Enc(), R=R(), names=[], cands=cands, seed=seed) == []          # looked at already: nothing twice
        finally:
            g["AUTO"], g["STATE"], g["ANSWERS"] = keep; grow.known_texts = kt; grow.page_texts = pt; g["file_item"] = g_file
    print("backlog selftest: ok (what the site does not answer is never listed; the editor's own wordings first, then a model's held to ask.py's checks; never twice)")


if __name__ == "__main__":
    a = sys.argv[1:]; opt = lambda k, d=None: a[a.index(k) + 1] if k in a and a.index(k) + 1 < len(a) else d
    if "--selftest" in a: selftest()
    elif "--list" in a: run(limit=int(opt("--max", "12")), show=True, save=False)
    elif a[:1] == ["run"]: run(limit=int(opt("--max", str(A_RUN))))
    elif a[:1] == ["exam"]:
        if "--daily" in a and str(load(EXAM, {}).get("at") or "")[:10] == TODAY: print("backlog exam: sat today already")
        else: exam(int(opt("--n", "20")))
    else: sys.exit(__doc__)
