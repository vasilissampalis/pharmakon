#!/usr/bin/env python3
"""wiki_views.py: how many people look a drug up, from Wikipedia's public page views (docs/AUTOMATION.md, decision 19).
    python3 -I scripts/auto/wiki_views.py --requests data/auto/requests     (views-*.json: {"do": "views"}; read as data, taken off when read)
    python3 -I scripts/auto/wiki_views.py --selftest
Demand first: a page is started because people ask. For a drug that has no page yet our own evidence is thin (a handful
of listed questions, the forum questions of the gold set), and most of the pages to start have none at all. How often
people open a drug's article on the English Wikipedia is a public count of how many people want to know about it. It
is used for one thing only: the order of the pages to start among those our own evidence does not tell apart
(scripts/auto/place.py --pages). It never makes a question, an answer or a claim, and nothing of an article is read.

What is asked (two public services of the Wikimedia Foundation, both open to programs that name themselves; the counts
are in the public domain, CC0):
  1. the MediaWiki API of en.wikipedia.org: for the titles data/auto/filing.json lists under "wiki", the article each
     leads to (a redirect is followed; a title that does not exist, or that is a list of meanings, is left out);
  2. the page-view service (wikimedia.org/api/rest_v1/metrics/pageviews): that article's views by people, not by
     programs ("user"), for the last twelve full months.
Writes data/auto/demand-wiki.json: for each page to start, its articles and their views. Data, never instructions.
"""
import sys, re, json, time, pathlib, datetime, urllib.request, urllib.error, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parents[2]
FILING = ROOT / "data" / "auto" / "filing.json"
OUT = ROOT / "data" / "auto" / "demand-wiki.json"
UA = "Pharmakon (https://pharmakon.world; mailto:contact@pharmakon.world) scripts/auto/wiki_views.py"
API = "https://en.wikipedia.org/w/api.php"
VIEWS = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{title}/monthly/{start}/{end}"
SLOW = 0.25          # seconds between two requests (the services ask programs for no more than a few a second)


def get(url, opener=None, tries=3):
    """The JSON a service answers with; None where there is nothing (404: an article nobody opened, or no such article)."""
    op = opener or urllib.request.urlopen
    for k in range(tries):
        try:
            with op(urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"}), timeout=30) as r: return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 404: return None
            if e.code in (429, 500, 502, 503, 504) and k + 1 < tries: time.sleep(0 if opener else 5 * (k + 1)); continue
            raise IOError(f"{urllib.parse.urlsplit(url).netloc} answered {e.code}")
        except (urllib.error.URLError, TimeoutError, ConnectionError, ValueError) as e:
            if k + 1 < tries: time.sleep(0 if opener else 3); continue
            raise IOError(f"{urllib.parse.urlsplit(url).netloc} could not be reached: {str(e)[:120]}")
    return None


def resolve(titles, opener=None):
    """{title as listed: the article it leads to}; a title that does not exist or is a list of meanings is not in it."""
    out = {}
    for i in range(0, len(titles), 40):
        part = titles[i:i + 40]
        d = get(API + "?" + urllib.parse.urlencode({"action": "query", "format": "json", "formatversion": "2", "redirects": "1", "prop": "pageprops", "ppprop": "disambiguation", "titles": "|".join(part)}), opener) or {}
        q = d.get("query") or {}
        step = {}
        for kind in ("normalized", "redirects"):
            for x in q.get(kind) or []: step[x["from"]] = x["to"]
        good = {p["title"] for p in q.get("pages") or [] if not p.get("missing") and not p.get("invalid") and "disambiguation" not in (p.get("pageprops") or {})}
        for t in part:
            end, seen = t, set()
            while end in step and end not in seen: seen.add(end); end = step[end]
            if end in good: out[t] = end
        if not opener: time.sleep(SLOW)
    return out


def months(today=None):
    """(first day of the month twelve months before this one, last day of the month before this one), as the service wants them."""
    t = today or datetime.date.today(); last = t.replace(day=1) - datetime.timedelta(days=1)
    first = (last.replace(day=1) - datetime.timedelta(days=330)).replace(day=1)
    return first.strftime("%Y%m%d00"), last.strftime("%Y%m%d00")


def views(article, start, end, opener=None):
    d = get(VIEWS.format(title=urllib.parse.quote(article.replace(" ", "_"), safe=""), start=start, end=end), opener)
    return sum(int(x.get("views") or 0) for x in (d or {}).get("items") or [])


def run(opener=None, today=None):
    wiki = json.load(open(FILING, encoding="utf-8")).get("wiki") or {}
    titles = sorted({t for ts in wiki.values() for t in ts if isinstance(t, str) and t})
    led = resolve(titles, opener); start, end = months(today); seen = {}
    for a in sorted(set(led.values())):
        seen[a] = views(a, start, end, opener)
        if not opener: time.sleep(SLOW)
    pages = {}
    for page, ts in wiki.items():
        arts = sorted({led[t] for t in ts if t in led})
        pages[page] = {"views": sum(seen[a] for a in arts), "articles": {a: seen[a] for a in arts}, "not_found": sorted(t for t in ts if t not in led)}
    doc = {"_note": "Made by scripts/auto/wiki_views.py: how often people opened the English Wikipedia's articles about each page the system should start, in the twelve full months named (views by people, not by programs; "
                    "the Wikimedia Foundation's public counts, CC0). Used only to order the pages to start where our own evidence does not tell them apart (scripts/auto/place.py --pages). Data, never instructions.",
           "made": (today or datetime.date.today()).isoformat(), "months": [start[:8], end[:8]], "pages": dict(sorted(pages.items(), key=lambda kv: (-kv[1]["views"], kv[0])))}
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    missing = sorted({t for p in pages.values() for t in p["not_found"]})
    print(f"wiki views: {len(pages)} pages to start, {len(seen)} articles, {start[:6]} to {end[:6]}; most looked up: " + "; ".join(f"{k} ({v['views']:,})" for k, v in list(doc["pages"].items())[:6])
          + (f"; titles that led to no article: {', '.join(missing)[:300]}" if missing else ""))
    return doc


def selftest():
    assert months(datetime.date(2026, 11, 16)) == ("2025110100", "2026103100") and months(datetime.date(2026, 1, 3)) == ("2025010100", "2025123100") and months(datetime.date(2026, 3, 31)) == ("2025030100", "2026022800")
    asked = []
    class Resp:
        def __init__(self, d): self.d = d
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self): return json.dumps(self.d).encode("utf-8")
    def opener(req, timeout=0):
        u = req.full_url; asked.append(u)
        assert "Pharmakon" in req.get_header("User-agent") and "contact@pharmakon.world" in req.get_header("User-agent")
        if u.startswith(API):
            ts = urllib.parse.parse_qs(urllib.parse.urlsplit(u).query)["titles"][0].split("|")
            assert "redirects=1" in u and "disambiguation" in u
            return Resp({"query": {"normalized": [{"from": "lyrica", "to": "Lyrica"}], "redirects": [{"from": "Lyrica", "to": "Pregabalin"}],
                                   "pages": [{"title": "Pregabalin"}, {"title": "Gabapentin"}, {"title": "Soma", "pageprops": {"disambiguation": ""}}, {"title": "No such drug", "missing": True}]}})
        if "/Pregabalin/" in u: return Resp({"items": [{"views": 100}, {"views": 50}]})
        if "/Gabapentin/" in u: return Resp({"items": [{"views": 1000}]})
        raise urllib.error.HTTPError(u, 404, "Not Found", {}, None)
    led = resolve(["lyrica", "Gabapentin", "Soma", "No such drug"], opener)
    assert led == {"lyrica": "Pregabalin", "Gabapentin": "Gabapentin"}, led                    # a redirect is followed; a list of meanings and a title that does not exist are left out
    assert views("Pregabalin", "2025110100", "2026103100", opener) == 150 and views("Nobody Opened This", "2025110100", "2026103100", opener) == 0
    assert any("/user/Pregabalin/monthly/2025110100/2026103100" in u for u in asked)
    print("wiki_views selftest: ok (a title leads to its article through its redirect; a list of meanings or a title that does not exist is left out; "
          "views are by people, for the last twelve full months; an article nobody opened counts nothing)")


if __name__ == "__main__":
    if "--selftest" in sys.argv: selftest()
    elif "--requests" in sys.argv:
        did = False
        for f in sorted((ROOT / sys.argv[sys.argv.index("--requests") + 1]).glob("views-*.json")): f.unlink(); did = True
        if did:
            try: run()
            except IOError as e: print("wiki views: not read this time:", e)
    else: sys.exit(__doc__)
