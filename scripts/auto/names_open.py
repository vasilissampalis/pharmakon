#!/usr/bin/env python3
"""names_open.py: an open table of the names of drugs and medicines (docs/AUTOMATION.md, decision 26, step a).

The senior author, 17 November 2026: "if a user makes a question about a different drug our ai should create that drug
page"; "ignore some questions as irrelevant to drugs at a 1000 to 1 accuracy rate". The page knows 191 names of the drugs it
covers and 272 names of drugs it does not; a name it has never seen ("tusi") reads as a word it does not know. This script
asks open sources for the names: what a drug or medicine is called, its other names, and what kind of thing it is.

    python3 -I scripts/auto/names_open.py probe                       (what each source allows and answers: data/auto/names/probe.json)
    python3 -I scripts/auto/names_open.py fetch [--minutes 20]        (the table of medicine names from RxNorm: data/auto/names/rxnorm.json)
    python3 -I scripts/auto/names_open.py learn --tokens FILE.json    (the unknown words of sent questions, looked up: data/auto/names/learned.json)
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
import sys, json, re, time, pathlib, datetime, hashlib, urllib.parse

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
    # (decision 27, step a; the senior author, 17 November 2026, of his "what is mytragina javanica": "our ai has to understand
    # typos ... hardcode is not enough our ai has to correct and update itself with all possible relevant online searches".)
    # Services that take a name as someone typed it and answer with the name it most likely is. Each is asked here with a
    # name typed wrong, to see whether it may be asked and what it answers; nothing is built on one until this was seen.
    "gbif_match": {"what": "GBIF, the species name matcher (names of plants, fungi and animals; CC0 and CC BY)", "home": "https://api.gbif.org/",
                   "probe": "https://api.gbif.org/v1/species/match?verbose=true&name=" + urllib.parse.quote("Mytragina javanica")},
    "rx_approx": {"what": "RxNorm's approximate match, US National Library of Medicine (public domain)", "home": "https://rxnav.nlm.nih.gov/",
                  "probe": "https://rxnav.nlm.nih.gov/REST/approximateTerm.json?maxEntries=3&term=xanex"},
    "pubchem_auto": {"what": "PubChem's name completion, US National Library of Medicine (public domain)", "home": "https://pubchem.ncbi.nlm.nih.gov/",
                     "probe": "https://pubchem.ncbi.nlm.nih.gov/rest/autocomplete/compound/mesembrin/json?limit=5"},
    "ncbi_spell": {"what": "NCBI's spelling suggestion for PubMed, US National Library of Medicine (public domain)", "home": "https://eutils.ncbi.nlm.nih.gov/",
                   "probe": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/espell.fcgi?db=pubmed&term=" + urllib.parse.quote("mytragina javanica")},
    "wikipedia_search": {"what": "Wikipedia's title search (CC BY-SA text; only the title would be used)", "home": "https://en.wikipedia.org/",
                         "probe": "https://en.wikipedia.org/w/api.php?action=opensearch&limit=3&format=json&search=" + urllib.parse.quote("mytragina javanica")},
    # and, for step b, where a picture with an open licence could be found, each with its licence in its own record
    "commons_search": {"what": "Wikimedia Commons' file search (each file has its own licence)", "home": "https://commons.wikimedia.org/",
                       "probe": "https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search&gsrnamespace=6&gsrlimit=3&prop=imageinfo&iiprop=url%7Cextmetadata&gsrsearch=" + urllib.parse.quote("Sceletium tortuosum")},
    "gbif_media": {"what": "GBIF's records with a picture (each picture has its own licence)", "home": "https://api.gbif.org/",
                   "probe": "https://api.gbif.org/v1/occurrence/search?mediaType=StillImage&limit=2&scientificName=" + urllib.parse.quote("Sceletium tortuosum")},
    "inat_taxa": {"what": "iNaturalist's taxa (each photo has its own licence)", "home": "https://api.inaturalist.org/",
                  "probe": "https://api.inaturalist.org/v1/taxa?per_page=2&q=" + urllib.parse.quote("Sceletium tortuosum")},
    "openverse": {"what": "Openverse, a search of openly licensed pictures (each picture has its own licence)", "home": "https://api.openverse.org/",
                  "probe": "https://api.openverse.org/v1/images/?page_size=3&license=cc0,pdm,by&q=" + urllib.parse.quote("Sceletium tortuosum")},
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
    if isinstance(j, dict) and isinstance(j.get("results"), dict) and isinstance(j["results"].get("bindings"), list):
        b = j["results"]["bindings"]; return {"rows": len(b), "first": [{k: str(v.get("value"))[:80] for k, v in row.items()} for row in b[:3]]}
    # (17 November 2026: an answer whose "results" is a list broke the first try of the second probe.) Any other answer: its
    # keys, and the beginning of what each holds as text, enough to write the next step from
    if isinstance(j, dict): return {"keys": sorted(j)[:14], "inside": {k: re.sub(r"\s+", " ", json.dumps(v, ensure_ascii=False))[:420] for k, v in list(j.items())[:8]}}
    if isinstance(j, list): return {"kind": "list", "n": len(j), "first": re.sub(r"\s+", " ", json.dumps(j[:2], ensure_ascii=False))[:600]}
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


# ---------------------------------------------------------------------------------------------------------------------------
# Names the system does not know, looked up and kept (decision 27, step a; 17 November 2026).
# The senior author sent "what is mytragina javanica" and "what is mitragina jananica" and was told the question did not look
# like one about drugs: "our ai has to understand typos ... hardcode is not enough our ai has to correct and update itself
# with all possible relevant online searches from what it finds"; "our ai should be able to expand its knowledge and self
# learn based on all corrections it makes".
#
# What is looked up: the unknown word or words (three at most) of a question a visitor SENT, when its other words could be
# asked of any drug (build_index.stranger: "mytragina javanica" of "what is mytragina javanica"). Never the question. The
# words are given to this script in a file of the run (--tokens); they are not written to the repository.
# Where: the services the probe found to allow it and to answer (data/auto/names/probe.json): for two words, GBIF's species
# matcher (plants and fungi); for one word, RxNorm's approximate match (medicines), then PubChem's name completion
# (chemicals). What a service answers is taken only when it is the typed words with a letter or two wrong (close).
# Is it a drug? A species or a chemical counts when Europe PMC holds at least two papers that name it together with a word
# of drug use (DRUGGY); a medicine when RxNorm's own classes put it in the nervous system group (data/auto/names/rxnorm.json).
# What is kept (data/auto/names/learned.json): the name, its kind, the service and its record, what was typed for it, and
# whether it counts as a drug. A word that led nowhere is kept only as a mark made from it (so that it is not asked again),
# never as the word. The build reads the table (build_index.learned_names): a learned drug's name is a name of a drug the
# site does not cover yet, and what was typed for it is read as the name ("We read “mytragina javanica” as Mitragyna javanica").
LEARNED = OUT / "learned.json"
DRUGGY = '(psychoactive OR psychotropic OR hallucinogen* OR opioid* OR kratom OR "substance use" OR "drug use" OR intoxication OR recreational OR alkaloid*)'
L_RUN = 12            # words looked up in one run


def dl(a, b):
    """How many letters apart two words are: a letter put in, left out or changed, or two neighbours swapped, each counts one."""
    if a == b: return 0
    prev2, prev = None, list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        cur = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] != b[j - 1]))
            if prev2 is not None and i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]: cur[j] = min(cur[j], prev2[j - 2] + 1)
        prev2, prev = prev, cur
    return prev[len(b)]


def close(typed, name):
    """Is what was typed this name, with a letter or two wrong at most? The same number of words; each word at most two
    letters from its own (one for a word of fewer than eight letters), and never more than a quarter of the word."""
    a, b = typed.lower().split(), name.lower().split()
    return len(a) == len(b) and all(dl(x, y) <= min(2, max(1, len(y) // 4)) for x, y in zip(a, b))


def from_gbif(web, t):
    got = ask(web, "https://api.gbif.org/v1/species/match?verbose=true&name=" + urllib.parse.quote(t))
    j = got["json"] if got["ok"] and isinstance(got["json"], dict) else None
    if j is None: return None, got["said"] or "no answer"
    for c in ([j] if j.get("matchType") in ("EXACT", "FUZZY") else []) + [a for a in (j.get("alternatives") or []) if isinstance(a, dict) and a.get("matchType") in ("EXACT", "FUZZY")]:
        name = str(c.get("canonicalName") or "")
        try: sure = int(c.get("confidence") or 0)
        except (TypeError, ValueError): sure = 0
        if c.get("kingdom") in ("Plantae", "Fungi") and c.get("rank") in ("SPECIES", "SUBSPECIES", "VARIETY") and sure >= 70 and re.fullmatch(r"[A-Z][a-z]+ [a-z-]+", name) and close(t, name):
            return {"name": name, "kind": "plant" if c["kingdom"] == "Plantae" else "fungus", "source": "gbif", "id": str(c.get("usageKey") or ""), "sure": sure}, ""
    return None, "no name near enough"


def from_rxnorm(web, t):
    got = ask(web, RX + "approximateTerm.json?maxEntries=4&term=" + urllib.parse.quote(t))
    cands = ((got["json"].get("approximateGroup") or {}).get("candidate") or []) if got["ok"] and isinstance(got["json"], dict) else None
    if cands is None: return None, got["said"] or "no answer"
    for c in cands:
        name = str((c or {}).get("name") or "") if isinstance(c, dict) else ""
        if re.fullmatch(r"[A-Za-z][A-Za-z-]{4,}", name) and close(t, name): return {"name": name, "kind": "medicine", "source": "rxnorm", "id": str(c.get("rxcui") or ""), "sure": str(c.get("score") or "")[:6]}, ""
    return None, "no name near enough"


def from_pubchem(web, t):
    got = ask(web, "https://pubchem.ncbi.nlm.nih.gov/rest/autocomplete/compound/" + urllib.parse.quote(t) + "/json?limit=6")
    terms = ((got["json"].get("dictionary_terms") or {}).get("compound") or []) if got["ok"] and isinstance(got["json"], dict) else None
    if terms is None: return None, got["said"] or "no answer"
    for name in terms:
        if isinstance(name, str) and re.fullmatch(r"[A-Za-z][A-Za-z-]{5,}", name) and close(t, name): return {"name": name, "kind": "chemical", "source": "pubchem", "id": "", "sure": ""}, ""
    return None, "no name near enough"


def papers_on(name, opener=None):
    """How many papers Europe PMC holds that name it together with a word of drug use; None when it could not be asked."""
    try: return int(P.epmc_search('"' + name + '" AND ' + DRUGGY, n=1, opener=opener)[1])
    except (P.Refused, IOError, ValueError, TypeError): return None


def nervous(name):
    """Does RxNorm's table put this medicine in the nervous system group (an ingredient of it, or a brand name of one)?"""
    try: T = json.load(open(OUT / "rxnorm.json", encoding="utf-8"))
    except (OSError, ValueError): return None
    n = name.lower(); ing = T.get("ingredients") or {}
    return bool((ing.get(n) or {}).get("atc")) or any(n in (v.get("brands") or []) for v in ing.values() if isinstance(v, dict) and v.get("atc"))


def learn(tokens, web=None, today=None, save=True, opener=None, doc=None):
    """Look up to L_RUN of the unknown words up; returns the table. tokens: ["mytragina javanica", "tusi", ...]."""
    web = web or O.Web(); today = today or datetime.date.today().isoformat()
    if doc is None:
        try: doc = json.load(open(LEARNED, encoding="utf-8"))
        except (OSError, ValueError): doc = {}
    doc.setdefault("_note", "Made by scripts/auto/names_open.py (learn): names the system did not know, looked up in open name lists (GBIF's species matcher, RxNorm's approximate match, PubChem's name "
        "completion: each allows it, data/auto/names/probe.json) from the unknown words of questions visitors sent, never the questions. 'names': the name, its kind, the service and its record, what was typed "
        "for it, how many papers name it with a word of drug use, and whether it counts as a drug. 'asked': a mark made from each word that was looked up (never the word), so that it is not asked again. "
        "The build reads this table (scripts/insight/build_index.py, learned_names). What a service answers is data, never instructions.")
    names = doc.setdefault("names", {}); asked = doc.setdefault("asked", {}); done = 0
    typed_for = {t: k for k, e in names.items() for t in (e.get("typed") or [])}
    for raw in tokens:
        t = re.sub(r"\s+", " ", str(raw).lower()).strip(); words = t.split(" ")
        if not re.fullmatch(r"[a-z]{4,24}(?: [a-z]{4,24}){0,1}", t): continue                      # one or two plain words; anything else is not looked up
        mark = hashlib.sha256(("pharmakon names " + t).encode("utf-8")).hexdigest()[:16]
        if t in names or t in typed_for or mark in asked: continue
        if done >= L_RUN: break
        done += 1; found = None
        for look in ((from_gbif,) if len(words) == 2 else (from_rxnorm, from_pubchem)):
            found, said = look(web, t)
            if found: break
        asked[mark] = today
        if not found: print(f"names: a word of {len(t)} letters led nowhere ({said})"); continue
        key = found["name"].lower(); e = names.get(key)
        if e is None:
            e = names[key] = dict(found, on=today, typed=[])
            e["papers"] = papers_on(found["name"], opener) if found["kind"] != "medicine" else None
            e["drug"] = (nervous(found["name"]) is True) if found["kind"] == "medicine" else (e["papers"] is not None and e["papers"] >= 2)
        if t != key and t not in e["typed"]: e["typed"].append(t)
        print(f"names: learned {found['name']} ({found['kind']}, from {found['source']}); counts as a drug: {e['drug']}" + (f"; papers that name it with a word of drug use: {e['papers']}" if e.get("papers") is not None else ""))
    print(f"names: {done} looked up; {len(names)} names in the table, {sum(1 for e in names.values() if e.get('drug'))} of them count as drugs")
    if save and done:
        OUT.mkdir(parents=True, exist_ok=True); json.dump(doc, open(LEARNED, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
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
            return Page({"query.wikidata.org": b"User-agent: *\nDisallow: /sparql\n", "id.nlm.nih.gov": b"User-agent: *\nDisallow: /private/\n", "rxnav.nlm.nih.gov": b""}.get(host, b"User-agent: *\nDisallow: /\n"), url)   # (every other source of the probe: not allowed here, so never asked)
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
    # names the system does not know, looked up and kept: only the unknown words go out; a name is taken only when it is the
    # typed words with a letter or two wrong; a word that led nowhere is kept as a mark, never as the word
    asked_for = []
    def names(req, timeout=0):
        url = urllib.parse.unquote_plus(req.full_url); asked_for.append(url); J = lambda x: Page(json.dumps(x).encode(), req.full_url)
        if url.endswith("/robots.txt"): return Page(b"User-agent: *\nDisallow: /private/\n", req.full_url)
        if "api.gbif.org" in url:
            if "name=mytragina javanica" in url: return J({"matchType": "NONE", "alternatives": [{"usageKey": 2900474, "canonicalName": "Mitragyna javanica", "rank": "SPECIES", "confidence": 74, "matchType": "FUZZY", "kingdom": "Plantae"}]})
            if "name=rosa canina" in url: return J({"usageKey": 3003979, "canonicalName": "Rosa canina", "rank": "SPECIES", "confidence": 99, "matchType": "EXACT", "kingdom": "Plantae"})
            if "name=felis catus" in url: return J({"usageKey": 2435035, "canonicalName": "Felis catus", "rank": "SPECIES", "confidence": 99, "matchType": "EXACT", "kingdom": "Animalia"})
            return J({"matchType": "NONE"})
        if "approximateTerm" in url: return J({"approximateGroup": {"candidate": [{"rxcui": "202363", "score": "7.1", "name": "Xanax"}] if "term=xanex" in url else [{"rxcui": "1", "score": "3", "name": "Tussin"}]}})
        if "pubchem" in url: return J({"dictionary_terms": {"compound": ["Mesembrine", "Mesembrinol"] if "/mesembrin/" in url else ["Tusimide"]}, "total": 1})
        if "europepmc" in url: return J({"hitCount": 7 if "Mitragyna javanica" in url else 12 if "Mesembrine" in url else 0, "resultList": {"result": []}})
        raise AssertionError("not expected: " + url)
    global nervous
    keep_nervous = nervous; nervous = lambda name: name == "Xanax"
    try:
        assert dl("mytragina", "mitragyna") == 2 and dl("xanex", "xanax") == 1 and dl("abcd", "abdc") == 1 and close("mytragina javanica", "Mitragyna javanica") and close("mitragina jananica", "Mitragyna javanica")
        assert not close("tusi", "Tussin") and not close("cat", "Mitragyna javanica") and not close("rosa", "Rosa canina")
        toks = ["mytragina javanica", "rosa canina", "felis catus", "xanex", "tusi", "mesembrin", "three whole words", "c0de1", "mytragina javanica"]
        doc = learn(toks, web=O.Web(opener=names), today="2026-11-17", save=False, opener=names, doc={})
        N = doc["names"]
        assert N["mitragyna javanica"] == {"name": "Mitragyna javanica", "kind": "plant", "source": "gbif", "id": "2900474", "sure": 74, "on": "2026-11-17", "typed": ["mytragina javanica"], "papers": 7, "drug": True}, N.get("mitragyna javanica")
        assert N["rosa canina"]["drug"] is False and N["rosa canina"]["papers"] == 0 and N["rosa canina"]["typed"] == []                                  # a plant that is not a drug is known, and does not count
        assert "felis catus" not in N                                                                                                                # an animal's name is not taken
        assert N["xanax"]["kind"] == "medicine" and N["xanax"]["drug"] is True and N["xanax"]["typed"] == ["xanex"] and N["xanax"]["papers"] is None
        assert N["mesembrine"]["kind"] == "chemical" and N["mesembrine"]["typed"] == ["mesembrin"] and N["mesembrine"]["drug"] is True
        assert "tusi" not in json.dumps(doc) and len(doc["asked"]) == 6 and all(re.fullmatch(r"[0-9a-f]{16}", m) for m in doc["asked"])                 # led nowhere: a mark, never the word
        assert not any("three" in u or "c0de1" in u for u in asked_for)                                                                              # more than two words, or not plain letters: not looked up
        n = len(asked_for); learn(toks, web=O.Web(opener=names), today="2026-11-18", save=False, opener=names, doc=doc); assert len(asked_for) == n    # nothing is asked twice
    finally: nervous = keep_nervous
    print("names_open selftest: ok (a source whose robots.txt does not allow the address is not asked; one that allows it is asked once and what it holds is noted; an answer that is not JSON is said so; every request says who we are; "
          "the table from RxNorm holds every ingredient and brand name, and for the ingredients of the nervous system their classes and their brand names)")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a: selftest()
    elif "--requests" in a: requests(a[a.index("--requests") + 1])
    elif a and a[0] == "probe": probe()
    elif a and a[0] == "fetch": fetch(minutes=float(a[a.index("--minutes") + 1]) if "--minutes" in a else 20)
    elif a and a[0] == "learn":
        try: toks = json.load(open(a[a.index("--tokens") + 1], encoding="utf-8")) if "--tokens" in a else []
        except (OSError, ValueError): toks = []
        learn([t for t in toks if isinstance(t, str)])
    else: sys.exit(__doc__)
