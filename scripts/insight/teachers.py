#!/usr/bin/env python3
"""teachers.py: the big free models teach Insight's own model how people type each answer's question (docs/AUTOMATION.md, decision 37 (2);
19 November 2026).

The senior author, 19 November 2026, 21:44: "we don't want you to generate the answers always ... we have to teach our ai to work like an llm
and do what you do as perfect as possible it has to work by itself perfectly all the time autonomously". Insight's own model (the small
encoder on the reader's device) learns from examples: ways of asking each answer's question. The editor wrote the first eight for every answer
(data/verification/insight/variants_teacher.json, round 0). From then on the free models write more (data/auto/insight/teachers.json), every day, for the answers that have the
fewest, the newest first (the machine lane's answers among them), and scripts/insight/train.py teaches the model with them on Sundays.

    python3 -I scripts/insight/teachers.py run [--max N] [--minutes M]   word the next answers (N a run, eight at most)
    python3 -I scripts/insight/teachers.py --list                        which answers it would word next; nothing is written
    python3 -I scripts/insight/teachers.py --selftest

WHAT A MODEL IS GIVEN: the answer's question as the site words it and the ways it is already asked (OUR words: the site's, the readers', the
editor's), and three answers' worth of the editor's own examples. Never a visitor's words, never a gold question.
WHAT IS KEPT (in code): a way of asking that a second model, of another family, says asks exactly the same question (not narrower, not broader,
not another); 2 to 14 words; that keeps the drug (one of its names or street names, where the site's question names one); that is not already a
way of asking any answer; that is not near a question of the gold sets (70% of its words or more: they stay a fair test); with no address, no
link and no long number. At most TARGET for an answer in all (the editor's included).
Writing changes nothing a reader sees: the model learns from these only through train.py, measured on the gold set, and a model reaches the
page only with its own judge, tiers, build and checks.
"""
import sys, re, json, random, pathlib, datetime, time

ROOT = pathlib.Path(__file__).resolve().parents[2]
for _p in ("scripts/auto", "scripts/insight", "scripts"):
    if str(ROOT / _p) not in sys.path: sys.path.insert(0, str(ROOT / _p))

V = ROOT / "data" / "verification" / "insight"
SEED = V / "variants_teacher.json"
AUTO = ROOT / "data" / "auto" / "insight" / "teachers.json"   # with the machines' other records (the Auto run keeps data/auto)
INPUT = ROOT / "site" / "insight" / ".cache" / "index-input.json"
TARGET, A_RUN, ASK = 16, 8, 10
NEAR_TARGET, NEAR_ASK = 6, 6          # near-miss questions per answer: questions that sound close and that the answer does not answer
ROOM = {"groq": 100000, "cf": 4000, "google": 200}   # what is left of each free allowance today before the teachers stop asking it: the lane's room comes first
WRITERS = ["gemini:gemma-4-26b-a4b-it", "gemini:gemma-4-31b-it", "groq:openai/gpt-oss-120b", "@cf/meta/llama-4-scout-17b-16e-instruct"]   # (the first a quick one: 4B at work of 26B)
ROOM_TOKENS = 3000   # Google's Gemma thinks before it writes: with 700 tokens of room its thought filled them and it wrote nothing (the Auto run of 19 November, 20:31 UTC)
CHECKERS = ["groq:openai/gpt-oss-120b", "gemini:gemini-3.5-flash-lite", "@cf/meta/llama-4-scout-17b-16e-instruct", "gemini:gemma-4-31b-it"]
TODAY = datetime.date.today().isoformat()
norm = lambda t: re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()
words = lambda t: set(norm(t).split())


def family(m):
    """Models of one family do not check each other (as the lane's base())."""
    m = m.lower()
    for k in ("gemma", "gemini", "gpt-oss", "llama", "qwen", "mistral", "deepseek", "phi"):
        if k in m: return "google" if k in ("gemma", "gemini") else k
    return m


def load(p, d):
    try: return json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError): return d


def teachers_of(seed, auto):
    """{answer id: [wordings]}, the editor's and the models'."""
    out = {}
    for k, ws in (seed.get("variants") or {}).items(): out.setdefault(k, []).extend(w for w in ws if isinstance(w, str))
    for k, ws in (auto.get("variants") or {}).items(): out.setdefault(k, []).extend(w["w"] for w in ws if isinstance(w, dict) and w.get("w"))
    return out


def near_of(auto):
    """{answer id: [near-miss questions]} the models wrote."""
    return {k: [w["w"] for w in ws if isinstance(w, dict) and w.get("w")] for k, ws in (auto.get("near") or {}).items()}


def gold_words():
    out = []
    for f, key in (("gold-sample.json", "question"), ("places-gold.json", "q")):
        for q in (load(V / f, {}).get("questions") or []):
            if isinstance(q, dict) and q.get(key): out.append(words(q[key]))
    return out


def near_gold(t, G):
    w = words(t)
    return any(len(w & g) / max(1, len(w | g)) >= 0.7 for g in G)


SYSTEM = "You write search queries for Pharmakon, a drug encyclopedia for the public. You never answer a question. You answer with JSON only."
CHECK_SYSTEM = "You check search queries for a drug encyclopedia. You never answer a question. You answer with JSON only."


def prompt(target, examples, n=ASK):
    ex = "\n\n".join("QUESTION: " + e["q"] + ("\nALSO ASKED AS: " + "; ".join(e["also"][:4]) if e["also"] else "") + "\nJSON: " + json.dumps({"ways": e["ways"][:8]}, ensure_ascii=False) for e in examples)
    return ("Each answer of the encyclopedia answers one question. People type that question into a search box in many ways: short searches, everyday "
            "and street words, slang, typos, chatty phrasing, all lower case. The editor wrote such ways for the questions below. Do the same for the last one.\n"
            f"- \"ways\": {n} different ways, each 2 to 14 words.\n"
            "- Each must ask EXACTLY the same question: not a narrower one, not a broader one, not another question.\n"
            "- Keep the drug: its name or one of its street names, where the question names one.\n"
            "- Not a copy of the question or of a way it is already asked.\n\n"
            + ex + "\n\nQUESTION: " + target["q"] + ("\nALSO ASKED AS: " + "; ".join(target["also"][:6]) if target["also"] else "") + "\nJSON:")


def check_prompt(q, ways):
    lines = "\n".join(f"{i + 1}. {w}" for i, w in enumerate(ways))
    return (f"The encyclopedia's question: \"{q}\"\n\nFor each search below, answer true only if a person typing it is asking exactly that question: the "
            "same drug and the same thing asked; not a narrower question, not a broader one, not another. Typos and slang are fine.\n\n"
            f"SEARCHES:\n{lines}\n\nJSON: {{\"same\": [{len(ways)} values, true or false, in order]}}")


def near_prompt(target, examples, n=NEAR_ASK):
    ex = "\n\n".join("QUESTION: " + e["q"] + "\nJSON: " + json.dumps({"near": e["near"][:5]}, ensure_ascii=False) for e in examples)
    return ("Each answer of the encyclopedia answers one question. For the questions below, the editors wrote searches that SOUND close to the question "
            "but ask something else, which its answer does not answer: another effect or risk of the same drug, the same thing about another drug, a "
            "narrower or a broader question. Do the same for the last one.\n"
            f"- \"near\": {n} such searches, each 3 to 14 words, as people type them; never the same question asked another way.\n\n"
            + ex + "\n\nQUESTION: " + target["q"] + "\nJSON:")


def near_check_prompt(q, items):
    lines = "\n".join(f"{i + 1}. {w}" for i, w in enumerate(items))
    return (f"The encyclopedia's question: \"{q}\"\n\nFor each search below, answer true if the encyclopedia's answer to that question would answer it "
            "(the same question, asked another way), and false if it asks something else: another effect or risk, another drug, a narrower or broader question.\n\n"
            f"SEARCHES:\n{lines}\n\nJSON: {{\"same\": [{len(items)} values, true or false, in order]}}")


def room(m):
    """Has this model's free allowance room for the teachers today, after the lane's share (ROOM)?"""
    import llm
    try:
        if m.startswith("groq:"): return llm.groq_left(m.split(":", 1)[1]) > ROOM["groq"]
        if m.startswith("@cf/"): return llm.left() > ROOM["cf"]
        if m.startswith("gemini:"): return llm.calls_left(m) > ROOM["google"]
    except Exception: return False
    return True


class Names:
    """Which drugs a text names, by the page's own table of names (build_index.names_table)."""
    def __init__(self, table=None):
        import build_index as bi
        self.t = table if table is not None else bi.names_table()
        self.of = {n.lower(): set(s) for n, s in self.t}; self.pat = bi.name_pattern([n for n, _ in self.t])

    def __call__(self, text):
        out = set()
        for m in self.pat.finditer(text or ""): out |= self.of.get(m.group(1).lower(), set())
        return out


def keep(ways, a, taken, G, names):
    """The ways that pass the checks in code (before the second model reads them): (kept, why each other was left out)."""
    must = names(a["wordings"][0]) & set(a.get("about") or []) if a.get("wordings") else set()
    kept, out = [], []
    for w in ways:
        w = re.sub(r"\s+", " ", str(w or "")).strip().strip("\"'").strip()
        n = norm(w); k = len(n.split())
        if not n or k < 2 or k > 14 or len(w) > 100: out.append((w, "length")); continue
        if re.search(r"https?:|www\.|@|\d{5,}", w, re.I): out.append((w, "an address, a link or a long number")); continue
        if n in taken or n in {norm(x) for x in kept}: out.append((w, "already a way of asking")); continue
        if near_gold(w, G): out.append((w, "near a gold question")); continue
        if must and not (names(w) & must): out.append((w, "the drug is not kept")); continue
        kept.append(w)
    return kept, out


def listed(raw, key):
    """The list of strings a model gave under key: {"key": [...]} as asked, or a bare JSON list, or numbered or bulleted lines."""
    import llm
    d = llm.as_json(raw) or {}
    got = d.get(key) if isinstance(d, dict) else None
    if isinstance(got, list): return [w for w in got if isinstance(w, str)]
    text = raw or ""
    a, b = text.find("["), text.rfind("]")
    if 0 <= a < b:
        try:
            v = json.loads(text[a:b + 1])
            if isinstance(v, list) and all(isinstance(w, str) for w in v): return v
        except ValueError: pass
    lines = [re.sub(r"^\s*(?:[-*\u2022]|\d+[.)])\s*", "", l).strip().strip("\"',") for l in text.splitlines()]
    return [l for l in lines if l and not l.startswith(("{", "}", "[", "]", "JSON", "QUESTION", "Here")) and len(l.split()) >= 2][:ASK + 4]


def ask_model(models, messages, chat, avoid=None, tokens=ROOM_TOKENS):
    """(answer, model) from the first model with a key and room, not of the family to avoid; (None, why) otherwise."""
    import llm
    why = "no model with a key and room"
    for m in models:
        if avoid and family(m) == avoid: continue
        if chat is llm.chat and (not llm.has(m) or not room(m)): continue
        try: return chat(m, messages, tokens), m
        except llm.Budget as e: why = f"{m}: {e}"
        except llm.Unavailable as e: why = f"{m}: {e}"
    return None, why


def order(A, T, today=TODAY, NT=None):
    """The answers that have the fewest teachers' wordings first (a new answer has none), then those that still lack near-miss questions, in an
    order that changes each day."""
    NT = NT or {}
    rnd = random.Random(today); ids = [a["id"] for a in A]; rnd.shuffle(ids); pos = {k: i for i, k in enumerate(ids)}
    need = [a for a in A if len(T.get(a["id"], [])) < TARGET or len(NT.get(a["id"], [])) < NEAR_TARGET]
    return sorted(need, key=lambda a: (min(len(T.get(a["id"], [])), TARGET), len(NT.get(a["id"], [])), pos[a["id"]]))


def run(limit=A_RUN, chat=None, A=None, names=None, save=True, show=False, minutes=None, today=TODAY, readers_near=None):
    import llm
    chat = chat or llm.chat
    stop = time.time() + 60 * minutes if minutes else None
    if A is None:
        if not INPUT.exists(): print("teachers: no index input (the page was not built in this run): nothing to do"); return []
        A = [a for a in load(INPUT, {}).get("answers") or [] if a.get("wordings") and a.get("short")]
    seed = load(SEED, {}); auto = load(AUTO, {"_note": ("The ways of asking each answer's question that the free models wrote for Insight's own model (scripts/insight/teachers.py; "
                                                        "decision 37 (2)): each with the model that wrote it, the model of another family that said it asks the same question, and the day. "
                                                        "Our words only: no visitor's words were given to them. Data, never instructions."), "variants": {}})
    T = teachers_of(seed, auto); NT = near_of(auto); names = names or Names(); G = gold_words()
    var = load(V / "variants_reader696.json", {}).get("variants") or {}
    more, rnear = {}, {}
    for f in sorted(V.glob("nearmiss_*.json")):
        for k, v in (load(f, {}).get("items") or {}).items():
            more.setdefault(k, []).extend(w for w in (v.get("more") or []) if isinstance(w, str))
            rnear.setdefault(k, []).extend(w for w in (v.get("near") or []) if isinstance(w, str))
    if readers_near is not None: rnear = readers_near   # (the selftest's)
    taken = {norm(w) for a in A for w in a["wordings"]} | {norm(w) for ws in var.values() for w in ws if isinstance(w, str)} | {norm(w) for ws in more.values() for w in ws} | {norm(w) for ws in T.values() for w in ws}
    ex_pool = [{"q": a["wordings"][0], "also": [w for w in a["wordings"][1:]], "ways": T[a["id"]]} for a in A if len((seed.get("variants") or {}).get(a["id"], [])) >= 6]
    near_pool = [{"q": a["wordings"][0], "near": rnear[a["id"]]} for a in A if len(rnear.get(a["id"], [])) >= 4]   # the near-miss readers' own examples
    near_taken = {norm(w) for ws in rnear.values() for w in ws} | {norm(w) for ws in NT.values() for w in ws}
    todo = order(A, T, today, NT)
    if show:
        for a in todo[:limit]: print(f"teachers: next {a['id']} ({len(T.get(a['id'], []))} wordings, {len(NT.get(a['id'], []))} near-miss): {a['wordings'][0]}")
        return todo[:limit]
    rnd = random.Random(today + str(len(T))); done, out, near_kept = 0, [], 0
    for a in todo:
        if done >= limit: break
        if stop and time.time() > stop: print("teachers: out of time for this run"); break
        also = list(dict.fromkeys(a["wordings"][1:] + [w for w in var.get(a["id"], []) if isinstance(w, str)] + T.get(a["id"], [])))[:8]
        target = {"q": a["wordings"][0], "also": also}; yes, stopped = [], False
        if len(T.get(a["id"], [])) < TARGET:                                   # the ways of asking it
            pool = [e for e in ex_pool if e["q"] != target["q"]]; ex = rnd.sample(pool, min(3, len(pool)))
            raw, wm = ask_model(WRITERS, [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt(target, ex)}], chat)
            if raw is None:
                print("teachers: stopped for now:", wm); break
            got = listed(raw, "ways")
            if not got: print(f"teachers: {a['id']}: nothing could be read in what {wm} wrote: {re.sub(chr(10), ' ', (raw or '')[:160])!r}")
            kept, left = keep([w for w in got if isinstance(w, str)][:ASK + 4], a, taken, G, names)
            space = TARGET - len(T.get(a["id"], []))
            cm = None
            if kept:
                raw2, cm = ask_model(CHECKERS, [{"role": "system", "content": CHECK_SYSTEM}, {"role": "user", "content": check_prompt(target["q"], kept)}], chat, avoid=family(wm), tokens=300)
                same = (llm.as_json(raw2) or {}).get("same") if raw2 is not None else None
                if not isinstance(same, list) or len(same) != len(kept):
                    print(f"teachers: {a['id']}: no check could be read ({cm if raw2 is None else 'the checker did not answer in form'}): nothing kept"); kept, cm = [], None
                else: yes = [w for w, s in zip(kept, same) if s is True][:max(0, space)]
            if yes:
                auto["variants"].setdefault(a["id"], []).extend({"w": w, "by": wm, "ok": cm, "at": today} for w in yes)
                T.setdefault(a["id"], []).extend(yes); taken |= {norm(w) for w in yes}
            print(f"teachers: {a['id']}: {len(yes)} kept of {len(got)} written by {wm}" + (f" (checked by {cm})" if cm else "") + (f"; left out: {'; '.join(sorted({why for _, why in left}))}" if left else ""))
        if len(NT.get(a["id"], [])) < NEAR_TARGET and near_pool:              # questions that sound close and that it does not answer
            pool = [e for e in near_pool if e["q"] != target["q"]]; ex = rnd.sample(pool, min(3, len(pool)))
            raw, wm = ask_model(WRITERS, [{"role": "system", "content": SYSTEM}, {"role": "user", "content": near_prompt(target, ex)}], chat)
            if raw is None: print("teachers: stopped for now:", wm); stopped = True
            else:
                got = [re.sub(r"\s+", " ", str(w or "")).strip() for w in listed(raw, "near")][:NEAR_ASK + 2]
                cand = []
                for w in got:
                    n_ = norm(w); k = len(n_.split())
                    if 3 <= k <= 14 and len(w) <= 100 and not re.search(r"https?:|www\.|@|\d{5,}", w, re.I) and n_ not in taken and n_ not in near_taken and not near_gold(w, G) and n_ not in {norm(x) for x in cand}: cand.append(w)
                nyes, ncm = [], None
                if cand:
                    raw2, ncm = ask_model(CHECKERS, [{"role": "system", "content": CHECK_SYSTEM}, {"role": "user", "content": near_check_prompt(target["q"], cand)}], chat, avoid=family(wm), tokens=300)
                    same = (llm.as_json(raw2) or {}).get("same") if raw2 is not None else None
                    if isinstance(same, list) and len(same) == len(cand):
                        nyes = [w for w, s in zip(cand, same) if s is False][:max(0, NEAR_TARGET - len(NT.get(a["id"], [])))]
                if nyes:
                    auto.setdefault("near", {}).setdefault(a["id"], []).extend({"w": w, "by": wm, "ok": ncm, "at": today} for w in nyes)
                    NT.setdefault(a["id"], []).extend(nyes); near_taken |= {norm(w) for w in nyes}; near_kept += len(nyes)
                print(f"teachers: {a['id']}: {len(nyes)} near-miss questions kept of {len(got)} written by {wm}" + (f" (checked by {ncm})" if ncm else ""))
        out.append((a, yes)); done += 1
        if stopped: break
    if save and (any(y for _, y in out) or near_kept):
        AUTO.parent.mkdir(parents=True, exist_ok=True); json.dump(auto, open(AUTO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"teachers: {sum(len(y) for _, y in out)} ways of asking kept for {sum(1 for _, y in out if y)} answers, and {near_kept} near-miss questions; "
          f"{sum(1 for a in A if len(T.get(a['id'], [])) < TARGET)} answers still have fewer than {TARGET} ways, {sum(1 for a in A if len(NT.get(a['id'], [])) < NEAR_TARGET)} fewer than {NEAR_TARGET} near-miss questions")
    return out


def selftest():
    import tempfile, llm
    global AUTO, SEED
    keep_auto, keep_seed = AUTO, SEED
    d = pathlib.Path(tempfile.mkdtemp()); AUTO = d / "auto.json"; SEED = d / "seed.json"
    json.dump({"variants": {"x_old": ["is weed bad for you", "cannabis harms", "marijuana dangers", "pot risks", "weed health effects", "is cannabis harmful"]}}, open(SEED, "w"))
    A = [{"id": "x_meth", "about": ["methamphetamine"], "wordings": ["How long does meth stay in the blood?"], "short": "s"},
         {"id": "x_old", "about": ["cannabis"], "wordings": ["Is cannabis harmful?"], "short": "s"},
         {"id": "x_gen", "about": [], "wordings": ["Did Portugal's decriminalization work?"], "short": "s"}]
    names = Names([["crystal meth", ["methamphetamine"]], ["meth", ["methamphetamine"]], ["cannabis", ["cannabis"]], ["weed", ["cannabis"]]])
    calls = []
    def chat(m, messages, tokens):
        calls.append(m); u = messages[-1]["content"]
        if u.startswith("The encyclopedia's question"):
            n = len(re.findall(r"^\d+\. ", u, re.M)); return json.dumps({"same": [True] * (n - 1) + [False]})
        if "Portugal" in u.split("QUESTION:")[-1]:
            return json.dumps({"ways": ["did decriminalisation work in portugal", "portugal drug policy results", "what happened after portugal decriminalized drugs"]})
        return json.dumps({"ways": ["how long does crystal meth stay in your blood", "meth in blood how long", "how long is it in your blood",
                                    "how long does meth stay in the blood", "meth blood test window http://x.y", "how long does meth last in blood?", "x"]})
    out = run(limit=2, chat=chat, A=A, names=names, today="2026-11-19")
    got = {a["id"]: y for a, y in out}
    assert set(got) == {"x_meth", "x_gen"}, got   # x_old has six already: the two that have none come first
    assert got["x_meth"] == ["how long does crystal meth stay in your blood", "meth in blood how long"], got["x_meth"]   # no drug, a copy, a link, a word: out; the checker's last "false": out
    assert got["x_gen"] == ["did decriminalisation work in portugal", "portugal drug policy results"], got["x_gen"]
    saved = json.load(open(AUTO)); assert saved["variants"]["x_meth"][0]["by"] == WRITERS[0] and family(saved["variants"]["x_meth"][0]["ok"]) != family(WRITERS[0])
    assert all(family(c) != "google" for c in calls[1::2]), calls
    assert family("gemini:gemma-4-31b-it") == family("gemini:gemini-3.5-flash-lite") == "google" and family("groq:openai/gpt-oss-120b") == "gpt-oss"
    assert listed('{"ways": ["a b", "c d"]}', "ways") == ["a b", "c d"] and listed('Sure: ["is weed bad", "weed risks"]', "ways") == ["is weed bad", "weed risks"]
    assert listed("1. is weed bad for you\n2) weed risks\n- pot dangers", "ways") == ["is weed bad for you", "weed risks", "pot dangers"] and listed("", "ways") == []
    assert near_gold("what is serotonin syndrome", [words("What is serotonin syndrome?")]) and not near_gold("weed and memory", [words("what is serotonin syndrome")])
    # a second run: the teachers' wordings now count, and the same answers are not worded again first
    T = teachers_of(load(SEED, {}), load(AUTO, {}))
    assert [a["id"] for a in order(A, T, "2026-11-19")][0] in ("x_meth", "x_gen") and len(T["x_meth"]) == 2
    # near-miss questions: the checker's "false" (another question) is what is kept; a copy, a gold question or a short one is not even asked about
    def chat2(m, messages, tokens):
        u = messages[-1]["content"]
        if u.startswith("The encyclopedia's question") and "would answer it" in u:
            n = len(re.findall(r"^\d+\. ", u, re.M)); return json.dumps({"same": [True] + [False] * (n - 1)})
        if "SOUND close" in u: return json.dumps({"near": ["how long does meth stay in your blood for", "does meth show up in hair tests", "how long does cocaine stay in the blood",
                                                           "what is serotonin syndrome", "meth", "how long does crystal meth stay in your blood"]})
        return chat(m, messages, tokens)
    AUTO.unlink(missing_ok=True)
    out = run(limit=1, chat=chat2, A=A, names=names, today="2026-11-19", readers_near={"x_old": ["is weed bad for your lungs", "is cbd harmful", "can weed cause psychosis", "is alcohol harmful"]})
    saved = json.load(open(AUTO)); nm = [w["w"] for w in saved.get("near", {}).get(out[0][0]["id"], [])]
    assert out[0][0]["id"] in ("x_meth", "x_gen") and (nm == ["does meth show up in hair tests", "how long does cocaine stay in the blood"] if out[0][0]["id"] == "x_meth" else len(nm) >= 1), (out[0][0]["id"], nm)
    assert all(not near_gold(w, gold_words()) for w in nm)
    # a model that has no room stops the run without writing anything
    def broke(m, messages, tokens): raise llm.Budget("used up")
    AUTO.unlink(); assert run(limit=2, chat=broke, A=A, names=names) == [] and not AUTO.exists()
    AUTO, SEED = keep_auto, keep_seed
    print("teachers selftest: ok")


def main():
    a = sys.argv[1:]
    if "--selftest" in a: return selftest()
    lim = int(a[a.index("--max") + 1]) if "--max" in a else A_RUN
    mins = float(a[a.index("--minutes") + 1]) if "--minutes" in a else None
    if "--list" in a: run(limit=lim, show=True); return
    if a and a[0] == "run": run(limit=min(lim, A_RUN), minutes=mins); return
    print(__doc__)


if __name__ == "__main__":
    main()
