#!/usr/bin/env python3
"""live_check.py [BASE]: what the site's own server answers on the live site, in a few plain lines.

Why: the editor's workspace cannot reach pharmakon.world, so it cannot see the server work. GitHub's machines can: the publishing
run asks the server after it has published and writes down what came back. Every line starts with "server:".
It holds no key and prints none. What it asks for is the editor's own fixed test (drugs and key words of ours), never a visitor's
words:

  1. GET  /api/ask      what the server can do: take questions, look research up, take questions the page sends by itself.
  2. POST /api/find     the published research on "kanna" and "anxiety": how many papers and how long it took, and for the first
                        papers their title and the words of their own that the server's rules took from their summaries (site
                        2.20: by fixed rule; no model takes part).
  3. POST /api/find     eleven more questions of ours, for the time each takes on the real site: how long, how long each of the
                        three searches took at Europe PMC, how many were asked again because they hung, whether the list was
                        given with a search still out; then the first question once more (Europe PMC's replies are kept for a
                        day: it should be quicker), and the middle and the slowest of them all.

Nothing here can fail a publishing: a server that does not answer is a line in the notes.
"""
import sys, json, time, urllib.request, urllib.error

BASE = "https://pharmakon.world"
Q = {"names": ["kanna", "sceletium tortuosum"], "words": ["anxiety"]}
MORE = [("modafinil and memory", {"names": ["modafinil"], "words": ["memory"]}), ("MDMA and PTSD", {"names": ["mdma"], "words": ["ptsd"]}), ("caffeine and headaches", {"names": ["caffeine"], "words": ["headaches"]}),
        ("tianeptine and addiction", {"names": ["tianeptine"], "words": ["addiction|addictive"]}), ("what phenibut is", {"names": ["phenibut"], "words": [], "def": 1}),
        ("ketamine and depression", {"names": ["ketamine"], "words": ["depression"]}), ("cannabis and psychosis", {"names": ["cannabis"], "words": ["psychosis"]}), ("nicotine and attention", {"names": ["nicotine"], "words": ["attention|concentrate"]}),
        ("psilocybin and depression", {"names": ["psilocybin"], "words": ["depression"]}), ("cocaine and the heart", {"names": ["cocaine"], "words": ["cardiac|heart"]}), ("kratom and addiction", {"names": ["kratom"], "words": ["addiction|addictive"]})]


def ask(opener, base, path, body=None):
    req = urllib.request.Request(base + path, method="POST" if body is not None else "GET", data=None if body is None else json.dumps(body).encode("utf-8"),
                                 headers={"content-type": "application/json", "accept": "application/json", "origin": base, "user-agent": "pharmakon.world publishing run (contact@pharmakon.world)"})
    with opener(req, timeout=40) as r:
        return json.loads(r.read().decode("utf-8"))


def how(f, took):
    """One question's time, in words: the reply's time, each search's time at Europe PMC, askings repeated, a search still out."""
    ms = f.get("ms") if isinstance(f.get("ms"), list) else []
    parts = [f"{took:.1f} s"]
    won, own = (f.get("won") if isinstance(f.get("won"), list) else []), (f.get("own") if isinstance(f.get("own"), list) else [])
    nth = lambda i: "" if i >= len(won) or not won[i] else (" by its second asking" if won[i] == 1 else " by its third asking") + (f" in {own[i] / 1000:.1f} s" if i < len(own) and own[i] is not None else "")
    if ms: parts.append("searches " + ", ".join("not back" if m is None else f"{m / 1000:.1f} s" + nth(i) for i, m in enumerate(ms[:3])))
    if f.get("again"): parts.append(f"{f.get('again')} asked again")
    if f.get("kept"): parts.append(f"{f.get('kept')} from what was kept")
    if f.get("more"): parts.append("given without the most cited, more to come")
    return "; ".join(parts)


def lines(opener=urllib.request.urlopen, base=BASE):
    out, yes = [], lambda d, k: "yes" if d.get(k) is True else "no"
    try:
        d = ask(opener, base, "/api/ask")
        out.append(f"server: takes questions {yes(d, 'ok')}; looks research up {yes(d, 'find')}; takes questions the page sends by itself {yes(d, 'auto')}" + ("; AND SAYS IT ASKS A MODEL (it should not, since site 2.20)" if d.get("quick") is True else ""))
    except Exception as e:
        out.append("server: /api/ask did not answer (" + type(e).__name__ + ")"); return out
    times, still = [], 0
    try:
        t0 = time.time(); f = ask(opener, base, "/api/find", Q); took = time.time() - t0; ps = f.get("papers") or []; times.append(took); still += 1 if f.get("more") else 0
        out.append(f"server: research on kanna and anxiety: {len(ps)} papers in {how(f, took)}; {sum(1 for p in ps if p.get('q'))} with words of their own")
        for i, p in enumerate(ps[:4], 1):
            about = " (in animals or cells)" if p.get("an") == 1 else " (its summary covers animals or cells too)" if p.get("an") == 2 else ""
            out.append(f"server: paper {i}: {str(p.get('t'))[:100]} ({p.get('kind')}, {p.get('y')}) | " + ("its own words: " + str(p.get("q"))[:200] + about if p.get("q") else "no words"))
    except Exception as e:
        out.append("server: /api/find did not answer (" + type(e).__name__ + ")"); return out
    for name, q in MORE:
        try:
            t0 = time.time(); f = ask(opener, base, "/api/find", q); took = time.time() - t0; ps = f.get("papers") or []; times.append(took); still += 1 if f.get("more") else 0
            first = next((p for p in ps if p.get("q")), None)
            out.append(f"server: {name}: {len(ps)} papers in {how(f, took)}; {sum(1 for p in ps if p.get('q'))} with words" + (": \u201C" + str(first.get("q"))[:160] + "\u201D" if first else ""))
        except Exception as e:
            out.append(f"server: {name}: no answer (" + type(e).__name__ + ")")
    try:
        t0 = time.time(); f = ask(opener, base, "/api/find", Q); again = time.time() - t0
        out.append(f"server: kanna and anxiety once more: {len(f.get('papers') or [])} papers in {how(f, again)}")
    except Exception as e:
        out.append("server: kanna and anxiety once more: no answer (" + type(e).__name__ + ")")
    if times:
        s = sorted(times); out.append(f"server: {len(s)} questions nobody asked before: the middle one took {s[len(s) // 2]:.1f} s, three in four under {s[(len(s) * 3) // 4]:.1f} s, the slowest {s[-1]:.1f} s; {still} given without the most cited")
    return out


def selftest():
    class R:
        def __init__(self, d): self.d = d
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self): return json.dumps(self.d).encode("utf-8")
    seen = []
    def opener(req, timeout=0):
        seen.append((req.get_method(), req.full_url, req.get_header("Origin"), req.data))
        if req.full_url.endswith("/api/ask"): return R({"ok": True, "find": True, "auto": True, "quick": False})
        body = json.loads(req.data)
        if body.get("names") == ["mdma"]: return R({"ok": True, "more": 1, "ms": [None, 210, 480], "again": 2, "won": [None, 0, 1], "own": [None, 210, 130], "kept": 0, "papers": [{"t": "A trial", "kind": "Trial", "y": "2021", "q": "\u2026MDMA-assisted therapy is highly efficacious\u2026"}]})
        return R({"ok": True, "ms": [300, 200, 250], "again": 0, "won": [0, 0, 0], "own": [300, 200, 250], "kept": 0, "papers": [{"t": "A Chewable Cure", "kind": "Review", "y": "2021", "q": "\u2026the plant reduced anxiety", "an": 1}, {"t": "Another", "kind": "Study", "y": "2019"}]})
    L = lines(opener, "https://x.test")
    assert L[0] == "server: takes questions yes; looks research up yes; takes questions the page sends by itself yes", L[0]
    assert L[1].startswith("server: research on kanna and anxiety: 2 papers in 0.0 s; searches 0.3 s, 0.2 s, 0.2 s; 1 with words of their own"), L[1]
    assert L[2] == "server: paper 1: A Chewable Cure (Review, 2021) | its own words: \u2026the plant reduced anxiety (in animals or cells)" and L[3] == "server: paper 2: Another (Study, 2019) | no words", L
    assert L[5] == "server: MDMA and PTSD: 1 papers in 0.0 s; searches not back, 0.2 s, 0.5 s by its second asking in 0.1 s; 2 asked again; given without the most cited, more to come; 1 with words: \u201C\u2026MDMA-assisted therapy is highly efficacious\u2026\u201D", L[5]
    assert L[15].startswith("server: kanna and anxiety once more: 2 papers in ") and L[16] == "server: 12 questions nobody asked before: the middle one took 0.0 s, three in four under 0.0 s, the slowest 0.0 s; 1 given without the most cited", L[15:]
    assert all(x.startswith("server:") for x in L) and len(L) == 17 and seen[0][0] == "GET" and seen[1][0] == "POST" and seen[1][2] == "https://x.test" and json.loads(seen[1][3]) == Q and len(seen) == 14
    old = lines(lambda req, timeout=0: R({"ok": True, "find": True, "auto": True, "quick": True, "papers": []}), "https://x.test")
    assert "AND SAYS IT ASKS A MODEL" in old[0] and "0 papers" in old[1], old
    def down(req, timeout=0): raise urllib.error.URLError("no route")
    assert lines(down, "https://x.test") == ["server: /api/ask did not answer (URLError)"]
    print("live_check selftest: ok (what the server can do; the research found with each paper's own words; the time of twelve questions with each search's time, askings repeated and searches still out; a server that says it asks a model is named; a server that does not answer is one line)")


if __name__ == "__main__":
    if "--selftest" in sys.argv: selftest()
    else:
        for l in lines(base=(sys.argv[1] if len(sys.argv) > 1 else BASE)): print(l)
