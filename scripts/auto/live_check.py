#!/usr/bin/env python3
"""live_check.py [BASE]: what the site's own server answers on the live site, in a few plain lines.

    python3 -I scripts/auto/live_check.py                  (https://pharmakon.world)
    python3 -I scripts/auto/live_check.py --selftest

For the notes of a publishing run (.github/workflows/deploy.yml): the editor's own workspace cannot reach the site, so the
run asks the server three things after it has published and writes down what came back. Every line starts with "server:".
It holds no key and prints none. The one question it asks is the editor's own fixed question, never a visitor's:

  1. GET  /api/ask      what the server can do: take questions, look research up, take questions the page sends by itself,
                        write an answer within seconds (only where the senior author has bound a language model to the site).
  2. POST /api/find     the published research on "kanna" and "anxiety": how many papers, and the first title.
  3. POST /api/answer   the answer within seconds to "does kanna help with anxiety": every sentence that passed the
                        server's own checks, with its paper's own words. (The server keeps an answer for 30 days, so this
                        costs the free allowance once, not once a publishing.)

Nothing here can fail a publishing: a server that does not answer is a line in the notes.
"""
import sys, json, urllib.request, urllib.error

BASE = "https://pharmakon.world"
Q = {"q": "does kanna help with anxiety", "names": ["kanna", "sceletium tortuosum"], "words": ["anxiety"]}


def ask(opener, base, path, body=None):
    req = urllib.request.Request(base + path, method="POST" if body is not None else "GET", data=None if body is None else json.dumps(body).encode("utf-8"),
                                 headers={"content-type": "application/json", "accept": "application/json", "origin": base, "user-agent": "pharmakon.world publishing run (contact@pharmakon.world)"})
    with opener(req, timeout=40) as r:
        return json.loads(r.read().decode("utf-8"))


def lines(opener=urllib.request.urlopen, base=BASE):
    out, yes = [], lambda d, k: "yes" if d.get(k) is True else "no"
    try:
        d = ask(opener, base, "/api/ask")
        out.append(f"server: takes questions {yes(d, 'ok')}; looks research up {yes(d, 'find')}; takes questions the page sends by itself {yes(d, 'auto')}; writes an answer within seconds {yes(d, 'quick')}")
    except Exception as e:
        out.append("server: /api/ask did not answer (" + type(e).__name__ + ")"); return out
    try:
        f = ask(opener, base, "/api/find", {"names": Q["names"], "words": Q["words"]}); ps = f.get("papers") or []
        out.append(f"server: research on kanna and anxiety: {len(ps)} papers" + (": first, " + str(ps[0].get("t"))[:110] + " (" + str(ps[0].get("kind")) + ", " + str(ps[0].get("y")) + ")" if ps else ""))
    except Exception as e:
        out.append("server: /api/find did not answer (" + type(e).__name__ + ")")
    try:
        a = ask(opener, base, "/api/answer", Q)
        if a.get("off"): out.append("server: the answer within seconds is off: no language model is bound to the site yet (the senior author's one step at Cloudflare)")
        elif a.get("full"): out.append("server: the answer within seconds has used its share of today's free allowance")
        elif a.get("held"): out.append("server: the answer within seconds held the test question back (it should not)")
        elif a.get("none"): out.append("server: the answer within seconds showed nothing for the test question: " + str(a.get("why"))[:120])
        else:
            ls = ((a.get("answer") or {}).get("lines") or [])[:3]
            out.append(f"server: the answer within seconds: {len(ls)} sentence(s) passed the checks" + (" (given again from the store)" if a.get("again") else ""))
            for i, l in enumerate(ls, 1):
                out.append(f"server: sentence {i}: {str(l.get('t'))[:260]} | the paper's own words: {str(l.get('quote'))[:160]} | {l.get('kind')}, {l.get('y')}, {str(l.get('j'))[:60]}")
    except Exception as e:
        out.append("server: /api/answer did not answer (" + type(e).__name__ + ")")
    return out


def selftest():
    import io
    class R:
        def __init__(self, d): self.d = d
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self): return json.dumps(self.d).encode("utf-8")
    seen = []
    def opener(req, timeout=0):
        seen.append((req.get_method(), req.full_url, req.get_header("Origin"), req.data))
        if req.full_url.endswith("/api/ask"): return R({"ok": True, "find": True, "auto": True, "quick": True})
        if req.full_url.endswith("/api/find"): return R({"ok": True, "papers": [{"t": "A Chewable Cure", "kind": "Review", "y": "2021"}, {"t": "Another"}]})
        return R({"ok": True, "answer": {"lines": [{"t": "A 2021 review says something.", "quote": "the plant reduced anxiety", "kind": "Review", "y": "2021", "j": "Molecules"}]}})
    L = lines(opener, "https://x.test")
    assert L[0] == "server: takes questions yes; looks research up yes; takes questions the page sends by itself yes; writes an answer within seconds yes", L[0]
    assert L[1].startswith("server: research on kanna and anxiety: 2 papers: first, A Chewable Cure (Review, 2021)") and L[2] == "server: the answer within seconds: 1 sentence(s) passed the checks" and "the plant reduced anxiety" in L[3], L
    assert all(x.startswith("server:") for x in L) and seen[0][0] == "GET" and seen[1][0] == "POST" and seen[1][2] == "https://x.test" and json.loads(seen[2][3])["q"] == Q["q"]
    off = lines(lambda req, timeout=0: R({"ok": True, "find": True, "auto": True, "quick": False, "off": True, "papers": []}), "https://x.test")
    assert "writes an answer within seconds no" in off[0] and "0 papers" in off[1] and "is off: no language model is bound" in off[2], off
    def down(req, timeout=0): raise urllib.error.URLError("no route")
    assert lines(down, "https://x.test") == ["server: /api/ask did not answer (URLError)"]
    print("live_check selftest: ok (what the server can do, the research found, every sentence that passed; a server without a model says so; a server that does not answer is one line)")


if __name__ == "__main__":
    if "--selftest" in sys.argv: selftest()
    else:
        for l in lines(base=(sys.argv[1] if len(sys.argv) > 1 else BASE)): print(l)
