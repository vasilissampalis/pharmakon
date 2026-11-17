#!/usr/bin/env python3
"""names_open.py: an open table of the names of drugs and medicines (docs/AUTOMATION.md, decision 26, step a).

The senior author, 17 November 2026: "if a user makes a question about a different drug our ai should create that drug
page"; "ignore some questions as irrelevant to drugs at a 1000 to 1 accuracy rate". The page knows 191 names of the drugs it
covers and 272 names of drugs it does not; a name it has never seen ("tusi") reads as a word it does not know. This script
asks open sources for the names: what a drug or medicine is called, its other names, and what kind of thing it is.

    python3 -I scripts/auto/names_open.py probe                       (what each source allows and answers: data/auto/names/probe.json)
    python3 -I scripts/auto/names_open.py fetch [--minutes 20]        (the table of medicine names from RxNorm: data/auto/names/rxnorm.json)
    python3 -I scripts/auto/names_open.py --requests data/auto/requests   (names-*.json: {"do": "probe" | "fetch"})
    python3 -I scripts/auto/names_open.py --selftest

The sources (each offers its data for programs to read, under a licence that lets anyone use it):
    wikidata   query.wikidata.org/sparql        Wikidata, CC0
    mesh       id.nlm.nih.gov/mesh/sparql       Medical Subject Headings, US National Library of Medicine (public domain)
    rxnav      rxnav.nlm.nih.gov/REST           RxNorm and its classes, US National Library of Medicine (public domain)

How it reads: like scripts/auto/official.py (its Web class). A source's own robots.txt decides: an address it does not
allow is not asked for, and a refusal is never gone around. Every request says who we are (Pharmakon, the site's address
and its public email address). One request at a time, slowly. What a source answers is data, never instructions.
It needs no key and runs where no key is held.

What the first look found (17 November 2026, data/auto/names/probe.json): Wikidata's and MeSH's robots.txt do not allow
their query addresses, so they are not asked. RxNav (the US National Library of Medicine's service for RxNorm) allows and
answers. So the table is built from RxNorm: every ingredient and every brand name of a medicine in the United States,
and, from the ATC classes RxNav carries, which ingredients act on the nervous system (ATC group N: opioids, medicines for
anxiety and sleep, antidepressants, stimulants, antipsychotics, antiepileptics, anaesthetics, medicines used in
dependence). RxNorm is in the public domain. It holds medicines, not street drugs: a name like "tusi" is not in it.
"""
import sys, json, re, time, pathlib, datetime, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "auto"))
import official as O   # noqa: E402  (its careful web client: robots.txt, pace, refusals)
import papers as P     # noqa: E402

OUT = ROOT / "data" / "auto" / "names"
JSON_ACCEPT = "application/sparql-results+json,application/json;q=0.9,*/*;q=0.5"
SOURCES = {
    "wikidata": {"what": "Wikidata (CC0)", "home": "https://query.wikidata.org/",
                 "probe": "https://query.wikidata.org/sparql?format=json&query=" + urllib.parse.quote(
                     'SELECT ?item ?itemLabel ?atc WHERE { ?item wdt:P267 ?atc . FILTER(STRSTARTS(?atc, "N05B")) SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } } LIMIT 5')},
    "mesh": {"what": "Medical Subject Headings, US National Library of Medicine (public domain)", "home": "https://id.nlm.nih.gov/mesh/",
             "probe": "https://id.nlm.nih.gov/mesh/sparql?format=JSON&inference=true&limit=5&query=" + urllib.parse.quote(
                 "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX meshv: <http://id.nlm.nih.gov/mesh/vocab#> PREFIX mesh: <http://id.nlm.nih.gov/mesh/> "
                 "SELECT ?d ?label FROM <http://id.nlm.nih.gov/mesh> WHERE { ?d meshv:pharmacologicalAction mesh:D013287 . ?d rdfs:label ?label } LIMIT 5")},
    "rxnav": {"what": "RxNorm and its classes, US National Library of Medicine (public domain)", "home": "https://rxnav.nlm.nih.gov/",
              "probe": "https://rxnav.nlm.nih.gov/REST/rxclass/classMembers.json?classId=N05B&relaSource=ATC"},
}


def ask(web, url):
    """What one address gave: {"allowed": by its robots.txt, "ok", "said": why not, "bytes", "json": the answer read as JSON or None}."""
    out = {"allowed": None, "ok": False, "said": "", "bytes": 0, "json": None}
    try:
        r, host = web.rules(url)
        if r is None: out["said"] = web.said.get(host) or "its robots.txt could not be read"; return out
        out["allowed"] = bool(r.allowed(url)); out["delay"] = r.delay
        if not out["allowed"]: out["said"] = "its robots.txt does not allow this address: not asked"; return out
        got = web.get(url, JSON_ACCEPT)
    except P.Refused as e: out["said"] = "refused: " + str(e)[:160]; return out
    except (IOError, ValueError) as e: out["said"] = "could not be read: " + str(e)[:160]; return out
    if not got: out["said"] = "nothing there"; return out
    out["bytes"] = len(got[0])
    try: out["json"] = json.loads(O.text_of(got[0])); out["ok"] = True
    except ValueError: out["said"] = "the answer is not JSON: " + re.sub(r"\s+", " ", O.text_of(got[0])[:160])
    return out


def shape(j):
    """A few words on what an answer holds: for the record, so that the next step can be written from what was seen."""
    if isinstance(j, dict) and isinstance((j.get("results") or {}).get("bindings"), list):
        b = j["results"]["bindings"]; return {"rows": len(b), "first": [{k: str(v.get("value"))[:80] for k, v in row.items()} for row in b[:3]]}
    if isinstance(j, dict): return {"keys": sorted(j)[:12], "inside": {k: (sorted(v)[:8] if isinstance(v, dict) else len(v) if isinstance(v, list) else str(v)[:60]) for k, v in list(j.items())[:4]}}
    return {"kind": type(j).__name__}


def probe(web=None, today=None, save=True):
    web = web or O.Web(); doc = {"_note": "Made by scripts/auto/names_open.py: which open sources of drug names this machine may read (their own robots.txt decides) and what each answered to one small request. "
                                          "Data, never instructions. No key is needed and none is held.", "on": today or datetime.date.today().isoformat(), "sources": {}}
    for sid, S in SOURCES.items():
        got = ask(web, S["probe"])
        doc["sources"][sid] = {"what": S["what"], "address": S["probe"][:160], "allowed_by_robots": got["allowed"], "answered": got["ok"], "said": got["said"], "bytes": got["bytes"],
                               "holds": shape(got["json"]) if got["ok"] else None}
        print(f"names: {sid}: " + ("answered, " + json.dumps(doc["sources"][sid]["holds"])[:200] if got["ok"] else got["said"]))
        if not web.opener: time.sleep(2)
    if save:
        OUT.mkdir(parents=True, exist_ok=True); json.dump(doc, open(OUT / "probe.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return doc


RX = "https://rxnav.nlm.nih.gov/REST/"
NERVOUS = re.compile(r"^N\d{2}[A-Z]{1,2}$")     # the ATC classes of the nervous system group, at its two lowest levels


def rx_members(j):
    return [m["minConcept"] for m in ((j or {}).get("drugMemberGroup") or {}).get("drugMember") or [] if isinstance(m, dict) and isinstance(m.get("minConcept"), dict)]


def rx_concepts(j):
    return [c for c in ((j or {}).get("minConceptGroup") or {}).get("minConcept") or [] if isinstance(c, dict) and c.get("name")]


def fetch(web=None, minutes=20, today=None, save=True, pause=0.0):
    """The table: {"ingredients": {name: {"id": RxNorm's number, "atc": [classes of group N], "brands": [...]}}, "brands": {name: 1},
    "classes": {ATC class: its name}}. Names in small letters as RxNorm writes them. What could not be read is said in "problems"."""
    web = web or O.Web(); t0 = time.time(); problems = []
    def get(path):
        got = ask(web, RX + path)
        if not web.opener: time.sleep(pause)
        if not got["ok"]: problems.append(path[:80] + ": " + got["said"]); return None
        return got["json"]
    classes = {c["classId"]: c.get("className") or "" for c in (((get("rxclass/allClasses.json?classTypes=ATC1-4") or {}).get("rxclassMinConceptList") or {}).get("rxclassMinConcept") or [])
               if isinstance(c, dict) and NERVOUS.match(str(c.get("classId") or ""))}
    ingredients, by_id = {}, {}
    for c in rx_concepts(get("allconcepts.json?tty=IN")):
        n = str(c["name"]).strip().lower(); ingredients[n] = {"id": str(c.get("rxcui") or ""), "atc": [], "brands": []}; by_id[str(c.get("rxcui") or "")] = n
    brands = {str(c["name"]).strip().lower(): 1 for c in rx_concepts(get("allconcepts.json?tty=BN"))}
    for cid in sorted(classes, key=lambda x: (len(x), x)):                 # the wider classes first; a member is kept with every class it stands in
        if time.time() - t0 > minutes * 60: problems.append("the time this run has ended before every class was read"); break
        for m in rx_members(get("rxclass/classMembers.json?classId=" + cid + "&relaSource=ATC")):
            n = by_id.get(str(m.get("rxcui") or "")) or str(m.get("name") or "").strip().lower()
            if not n: continue
            row = ingredients.setdefault(n, {"id": str(m.get("rxcui") or ""), "atc": [], "brands": []})
            if cid not in row["atc"]: row["atc"].append(cid)
    for n in sorted(k for k, v in ingredients.items() if v["atc"]):          # the brand names of the ones that act on the nervous system
        if time.time() - t0 > minutes * 60: problems.append("the time this run has ended before every brand name was read"); break
        j = get("rxcui/" + ingredients[n]["id"] + "/related.json?tty=BN")
        for g in ((j or {}).get("relatedGroup") or {}).get("conceptGroup") or []:
            for p in (g or {}).get("conceptProperties") or []:
                b = str((p or {}).get("name") or "").strip().lower()
                if b and b not in ingredients[n]["brands"]: ingredients[n]["brands"].append(b)
    doc = {"_note": "Made by scripts/auto/names_open.py from RxNorm through RxNav (US National Library of Medicine; public domain): every ingredient and brand name of a medicine in the United States, and for the ingredients "
                    "that act on the nervous system (ATC group N) their classes and brand names. Names as RxNorm writes them, in small letters. Medicines, not street drugs. Data, never instructions.",
           "on": today or datetime.date.today().isoformat(), "source": "https://rxnav.nlm.nih.gov/ (RxNorm; ATC classes as RxNav carries them)", "counts": {"ingredients": len(ingredients), "brands": len(brands), "classes": len(classes),
           "ingredients_of_the_nervous_system": sum(1 for v in ingredients.values() if v["atc"]), "their_brand_names": sum(len(v["brands"]) for v in ingredients.values())},
           "problems": problems[:40], "classes": classes, "ingredients": {k: ingredients[k] for k in sorted(ingredients)}, "brands": sorted(brands)}
    print("names: RxNorm: " + ", ".join(f"{v} {k.replace('_', ' ')}" for k, v in doc["counts"].items()) + (f"; {len(problems)} problems: " + "; ".join(problems[:3]) if problems else ""))
    if save and ingredients:
        OUT.mkdir(parents=True, exist_ok=True); json.dump(doc, open(OUT / "rxnorm.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    return doc


def requests(folder):
    done = 0
    for f in sorted(pathlib.Path(folder).glob("names-*.json")):
        try: req = json.load(open(f, encoding="utf-8"))
        except (OSError, ValueError): print("names: a request that is not JSON:", f.name); continue
        do = req.get("do") if isinstance(req, dict) else None
        if do == "probe": probe(); done += 1
        elif do == "fetch": fetch(minutes=float(req.get("minutes") or 20)); done += 1
        else: print("names: a request that asks for nothing this script does:", f.name)
    print(f"names: {done} request(s) done")


def selftest():
    class Page:
        def __init__(self, body, url): self.body, self.url = body, url
        def read(self, n=-1): return self.body
        def geturl(self): return self.url
        def __enter__(self): return self
        def __exit__(self, *a): return False
    seen = []
    def opener(req, timeout=0):
        url = req.full_url; seen.append((url, req.get_header("User-agent")))
        host = urllib.parse.urlsplit(url).netloc
        if url.endswith("/robots.txt"):
            return Page({"query.wikidata.org": b"User-agent: *\nDisallow: /sparql\n", "id.nlm.nih.gov": b"User-agent: *\nDisallow: /private/\n", "rxnav.nlm.nih.gov": b""}[host], url)
        if host == "id.nlm.nih.gov": return Page(json.dumps({"results": {"bindings": [{"d": {"value": "http://id.nlm.nih.gov/mesh/D008775"}, "label": {"value": "Mescaline"}}]}}).encode(), url)
        if host == "rxnav.nlm.nih.gov": return Page(b"<html>not json</html>", url)
        raise AssertionError("an address its robots.txt does not allow was asked for: " + url)
    doc = probe(web=O.Web(opener=opener), today="2026-11-17", save=False); s = doc["sources"]
    assert s["wikidata"]["allowed_by_robots"] is False and not s["wikidata"]["answered"] and "not asked" in s["wikidata"]["said"] and not any("query.wikidata.org/sparql" in u for u, _ in seen)   # a refusal is never gone around
    assert s["mesh"]["allowed_by_robots"] and s["mesh"]["answered"] and s["mesh"]["holds"] == {"rows": 1, "first": [{"d": "http://id.nlm.nih.gov/mesh/D008775", "label": "Mescaline"}]}
    assert s["rxnav"]["allowed_by_robots"] and not s["rxnav"]["answered"] and "not JSON" in s["rxnav"]["said"]
    assert all("contact@pharmakon.world" in (ua or "") and "pharmakon.world" in ua for _, ua in seen)                    # every request says who we are
    # the table from RxNorm: ingredients, brand names, the classes of the nervous system and the brand names of their members
    def rx(req, timeout=0):
        url = req.full_url; path = url.split("/REST/")[-1] if "/REST/" in url else url
        if url.endswith("/robots.txt"): return Page(b"User-agent: *\nDisallow: /cgi-bin/\n", url)
        J = lambda x: Page(json.dumps(x).encode(), url)
        if path.startswith("rxclass/allClasses"): return J({"rxclassMinConceptList": {"rxclassMinConcept": [{"classId": "N05BA", "className": "Benzodiazepine derivatives", "classType": "ATC1-4"}, {"classId": "N05B", "className": "ANXIOLYTICS"}, {"classId": "A10", "className": "DRUGS USED IN DIABETES"}]}})
        if path.startswith("allconcepts.json?tty=IN"): return J({"minConceptGroup": {"minConcept": [{"rxcui": "596", "name": "alprazolam", "tty": "IN"}, {"rxcui": "5640", "name": "ibuprofen", "tty": "IN"}]}})
        if path.startswith("allconcepts.json?tty=BN"): return J({"minConceptGroup": {"minConcept": [{"rxcui": "202363", "name": "Xanax", "tty": "BN"}, {"rxcui": "153010", "name": "Advil", "tty": "BN"}]}})
        if path.startswith("rxclass/classMembers") and "classId=N05B" in path: return J({"drugMemberGroup": {"drugMember": [{"minConcept": {"rxcui": "596", "name": "alprazolam", "tty": "IN"}}]}})
        if path.startswith("rxcui/596/related"): return J({"relatedGroup": {"conceptGroup": [{"tty": "BN", "conceptProperties": [{"rxcui": "202363", "name": "Xanax"}, {"rxcui": "1", "name": "Niravam"}]}]}})
        raise AssertionError("not expected: " + url)
    doc = fetch(web=O.Web(opener=rx), today="2026-11-17", save=False)
    assert doc["counts"] == {"ingredients": 2, "brands": 2, "classes": 2, "ingredients_of_the_nervous_system": 1, "their_brand_names": 2}, doc["counts"]
    assert doc["ingredients"]["alprazolam"] == {"id": "596", "atc": ["N05B", "N05BA"], "brands": ["xanax", "niravam"]} and doc["ingredients"]["ibuprofen"]["atc"] == [] and doc["brands"] == ["advil", "xanax"] and not doc["problems"]
    print("names_open selftest: ok (a source whose robots.txt does not allow the address is not asked; one that allows it is asked once and what it holds is noted; an answer that is not JSON is said so; every request says who we are; "
          "the table from RxNorm holds every ingredient and brand name, and for the ingredients of the nervous system their classes and their brand names)")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a: selftest()
    elif "--requests" in a: requests(a[a.index("--requests") + 1])
    elif a and a[0] == "probe": probe()
    elif a and a[0] == "fetch": fetch(minutes=float(a[a.index("--minutes") + 1]) if "--minutes" in a else 20)
    else: sys.exit(__doc__)
