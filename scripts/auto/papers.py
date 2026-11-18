#!/usr/bin/env python3
"""papers.py: finding the papers that can answer a question, on a machine that may read them (docs/AUTOMATION.md).

The senior author, 15 November 2026: "not only the papers we hold but whatever it can find online"; "if there are
paywalled papers and the info for an answer is not full we should be able to access which papers pharmakon insight wants
to make a complete answer"; "it should find more than one sources if they are relevant, whatever is relevant".

    python3 -I scripts/auto/papers.py find [--ids w_0027,w_0041] [--max N] [--out data/auto/papers] [--requests data/auto/requests]
    python3 -I scripts/auto/papers.py --selftest

What it reads, and how:
  Europe PMC   the search (it holds PubMed's records and abstracts too) and, for papers in its open-access set, the
               full text as XML. No key. https://www.ebi.ac.uk/europepmc/webservices/rest/
  Crossref     every reference's metadata (never typed by hand: scripts/build_references.py makes the record) and its
               update links: a retracted paper is refused, a corrected one is flagged. No key.
  Each request names the site and its public address (contact@pharmakon.world), never a person's own address.
  A service that says no (403, or 429 after waiting) is not asked again in the same run, and nothing goes around it.
  Sci-Hub, sign-ins and paywalls are never touched: a paper that cannot be read is listed for the senior author instead.

For each question it writes <out>/<id>.json: the searches as they were sent (so that anyone can repeat them), how many
records each found, and the candidates in the order it would read them, with what kind of paper each is, whether its
full text can be read, and why it stands where it stands. Titles, names, years and identifiers only: no abstract and no
passage is kept in the repository (they are the publishers'); a full text is read where it is fetched and not stored.

Ranking without a writer's opinion: the question and its other wordings are compared, by meaning, with each paper's
title and the sentences of its abstract (the general model all-MiniLM-L6-v2, the same file the site's own model was
trained from); reviews and meta-analyses stand ahead of single studies, studies in people ahead of others, newer and
more cited papers a little ahead. This only decides the order of reading. What an answer may rest on is decided by the
gates of the lane (scripts/auto/lane.py), never here.
"""
import sys, os, re, json, time, html, hashlib, pathlib, datetime, urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(ROOT / "scripts" / "insight"))
sys.path.insert(0, str(ROOT / "scripts" / "auto"))   # (17 November 2026, 19:50) GitHub runs this file with -I, which leaves its own folder off the path: page_names could not load place.py there, said nothing, and kanna and Mitragyna javanica were searched without their names all afternoon
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/"
CROSSREF = "https://api.crossref.org/works/"
UA = "Pharmakon/2.5 (https://pharmakon.world; mailto:contact@pharmakon.world) scripts/auto/papers.py"
PAUSE = 0.4            # seconds between requests to one service
N_SEARCH = 40          # records asked for in each search
N_KEEP = 12            # candidates kept for a question
N_WANTED = 3           # papers that cannot be read, listed for the senior author, for a question
FINDER = 3             # the finder's own number: a question searched by an older finder is searched again
TODAY = datetime.date.today().isoformat()


class Refused(Exception):
    """The service said no. It is not asked again in this run."""


_last, _refused = {}, set()


def fetch(url, opener=None, accept="application/json", tries=3):
    """The bytes at url, None for 'not there' (404). Waits between requests to one host; backs off on 429 and 503."""
    host = urllib.parse.urlparse(url).netloc
    if host in _refused: raise Refused(host)
    opener = opener or urllib.request.urlopen
    for k in range(tries):
        wait = PAUSE - (time.time() - _last.get(host, 0))
        if wait > 0 and opener is urllib.request.urlopen: time.sleep(wait)
        _last[host] = time.time()
        try:
            with opener(urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept}), timeout=40) as r: return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404: return None
            if e.code in (429, 500, 502, 503, 504) and k + 1 < tries: time.sleep(3 * (k + 1) if opener is urllib.request.urlopen else 0); continue
            if e.code in (401, 403, 429): _refused.add(host); raise Refused(f"{host} answered {e.code}")
            raise
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            if k + 1 < tries: time.sleep(2 if opener is urllib.request.urlopen else 0); continue
            raise IOError(f"{host} could not be reached: {e}")
    return None


def listed():
    """Every question the system works on: the editors' list (data/site/wanted.json) and the system's own
    (data/auto/wanted-auto.json, made by scripts/auto/ask.py from questions visitors sent, in our words)."""
    out = list(json.load(open(ROOT / "data" / "site" / "wanted.json", encoding="utf-8"))["items"])
    try: out += json.load(open(ROOT / "data" / "auto" / "wanted-auto.json", encoding="utf-8"))["items"]
    except (OSError, ValueError, KeyError): pass
    return out


# ---------- Europe PMC ----------
clean = lambda t: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", t or ""))).strip()
REVIEW = ("review", "systematic review", "meta-analysis", "meta analysis", "practice guideline", "guideline")
OPINION = ("editorial", "comment", "letter", "news", "interview", "biography", "historical article", "personal narrative", "lecture", "congress")   # never a source
TRIAL = ("randomized controlled trial", "clinical trial", "controlled clinical trial", "observational study", "comparative study", "multicenter study", "clinical study")


def paper(r):
    """One Europe PMC record ('core'), as this lane keeps it. The abstract stays in memory for the ranking only."""
    types = [str(t).lower() for t in ((r.get("pubTypeList") or {}).get("pubType") or [])]
    j = ((r.get("journalInfo") or {}).get("journal") or {})
    y = str(r.get("pubYear") or "")
    return {"epmc": f"{r.get('source') or ''}/{r.get('id') or ''}", "pmid": r.get("pmid") or None, "pmcid": r.get("pmcid") or None, "doi": (r.get("doi") or "").lower() or None,
            "title": clean(r.get("title")).rstrip("."), "authors": clean(r.get("authorString")), "journal": clean(j.get("title") or j.get("medlineAbbreviation") or ""), "year": int(y) if y.isdigit() else None,
            "abstract": clean(r.get("abstractText")), "oa": r.get("isOpenAccess") == "Y", "in_epmc": r.get("inEPMC") == "Y", "types": types, "cited": int(r.get("citedByCount") or 0),
            "license": r.get("license") or "", "lang": (r.get("language") or "").lower(),
            "kind": "retracted" if any("retracted publication" in t for t in types) else "notice" if any(t in ("retraction of publication", "published erratum", "expression of concern") for t in types)
                    else "opinion" if any(t in OPINION for t in types) else "review" if any(t in REVIEW for t in types) else "case" if any(t == "case reports" for t in types)
                    else "study" if any(t in TRIAL for t in types) else "other"}


def epmc_search(query, n=N_SEARCH, opener=None, sort=None):
    """(records, how many the service says there are) for a query in Europe PMC's own syntax, most relevant first (or in
    the order of sort, such as "CITED desc": the most cited first)."""
    url = EPMC + "search?" + urllib.parse.urlencode(dict({"query": query, "format": "json", "resultType": "core", "pageSize": str(n)}, **({"sort": sort} if sort else {})))
    raw = fetch(url, opener)
    d = json.loads(raw.decode("utf-8")) if raw else {}
    return [paper(r) for r in ((d.get("resultList") or {}).get("result") or []) if isinstance(r, dict)], int(d.get("hitCount") or 0)


def epmc_fulltext(pmcid, opener=None):
    """A paper's full text as JATS XML, for papers in Europe PMC's open-access set; None when it is not offered."""
    if not re.fullmatch(r"PMC\d+", str(pmcid or "")): return None
    raw = fetch(EPMC + pmcid + "/fullTextXML", opener, accept="application/xml")
    return raw.decode("utf-8", "replace") if raw else None


# ---------- a full text as passages ----------
SKIP = {"xref", "table-wrap", "table", "fig", "disp-formula", "inline-formula", "supplementary-material", "fn", "label", "graphic", "media", "object-id", "ext-link"}
NOT_BODY = re.compile(r"^(references?|bibliography|acknowledge?ments?|author contributions?|authors' contributions|contributors|abbreviations|supplementary|supporting information|additional files?|"
                      r"data availability|availability of data|ethics|ethical approval|consent|publisher'?s note|footnotes?|competing interests?|conflicts? of interest|declarations?|funding|financial support|disclosures?)\b", re.I)
MONEY = re.compile(r"^(funding|financial support|competing interests?|conflicts? of interest|declarations? of (competing )?interests?|disclosures?)\b", re.I)
local = lambda tag: tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


def text_of(el):
    """The words of an element, without its reference marks, tables, figures and formulas (their tails are kept)."""
    out = [el.text or ""]
    for c in el:
        if local(c.tag) not in SKIP: out.append(text_of(c))
        out.append(c.tail or "")
    return "".join(out)


def tidy(t):
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\s*[\[(]\s*[,;–-]*\s*[\])]", "", t)       # the empty brackets a removed reference mark leaves behind
    return re.sub(r"\s+([,.;:)])", r"\1", t)


def jats_passages(xml_text):
    """{"passages": [{"n", "where", "text"}], "money": [what the paper says about funding and interests]} from JATS XML.
    A passage is one paragraph; "where" is the path of its section's headings ("Results › Primary outcome")."""
    try: root = ET.fromstring(xml_text.encode("utf-8"))
    except ET.ParseError:
        try: root = ET.fromstring(re.sub(r"&(?!amp;|lt;|gt;|quot;|apos;|#)\w+;", " ", xml_text).encode("utf-8"))
        except ET.ParseError: return {"passages": [], "money": []}
    out, money = [], []
    def add(where, p):
        t = tidy(text_of(p))
        if len(t) >= 80: out.append({"n": len(out) + 1, "where": where, "text": t})
    for ab in root.iter():
        if local(ab.tag) == "abstract" and (ab.get("abstract-type") or "") not in ("graphical", "teaser", "toc", "author-highlights"):
            for p in ab.iter():
                if local(p.tag) == "p": add("Abstract", p)
            break
    def walk(sec, path):
        title = next((tidy(text_of(c)) for c in sec if local(c.tag) == "title"), "")
        here = path + [title] if title else path
        kind = title or (sec.get("sec-type") or "")
        if MONEY.match(kind):
            money.extend(tidy(text_of(p)) for p in sec.iter() if local(p.tag) == "p"); return
        if NOT_BODY.match(kind): return
        for c in sec:
            if local(c.tag) == "p": add(" › ".join(here) or "Text", c)
            elif local(c.tag) == "sec": walk(c, here)
    for body in root.iter():
        if local(body.tag) == "body": walk(body, []); break
    for el in root.iter():                                   # funding and interests are often kept in the back matter
        if local(el.tag) in ("funding-statement", "ack") or (local(el.tag) == "fn" and (el.get("fn-type") or "") in ("COI-statement", "conflict", "financial-disclosure")):
            t = tidy(text_of(el))
            if t and t not in money: money.append(t)
    return {"passages": out, "money": [m for m in money if m][:6]}


# ---------- Crossref ----------
def crossref_compact(m):
    """A Crossref record in the short form scripts/build_references.py reads (data/access/crossref-cache.jsonl)."""
    dp = lambda k: ((m.get(k) or {}).get("date-parts") or [[None]])[0] if (m.get(k) or {}).get("date-parts") and (m.get(k) or {})["date-parts"][0] and (m.get(k) or {})["date-parts"][0][0] else None
    au = []
    for a in m.get("author") or []:
        if a.get("family"): au.append([a["family"], a.get("given") or ""] + ([a["suffix"]] if a.get("suffix") else []))
        elif a.get("name"): au.append([a["name"]])
    upd = [f"{u.get('type', '')}:{u.get('DOI', '')}" for u in m.get("updated-by") or []] + [f"to:{u.get('type', '')}:{u.get('DOI', '')}" for u in m.get("update-to") or []]
    return {"DOI": m.get("DOI"), "type": m.get("type"), "title": (m.get("title") or [""])[0], "sub": (m.get("subtitle") or [None])[0], "au": au, "ct": (m.get("container-title") or [""])[0],
            "vol": m.get("volume"), "iss": m.get("issue"), "pg": m.get("page"), "number": m.get("article-number"), "print": dp("published-print"), "online": dp("published-online"), "issued": dp("issued"),
            "upd": upd, "pub": m.get("publisher"), "_via": "api"}


def crossref(doi, opener=None):
    """(the short record, None) or (None, why not) for a DOI."""
    try: raw = fetch(CROSSREF + urllib.parse.quote(doi, safe="/") + "?mailto=contact@pharmakon.world", opener)
    except Refused as e: return None, "Crossref said no: " + str(e)
    except IOError as e: return None, str(e)
    if not raw: return None, "Crossref has no record of this DOI"
    m = (json.loads(raw.decode("utf-8")) or {}).get("message") or {}
    if not m.get("DOI") or not m.get("title"): return None, "Crossref's record has no title"
    return crossref_compact(m), None


def reference(doi, cr, pmcid=None):
    """The reference record, as data/references/*.json holds them, made by scripts/build_references.py from Crossref's
    record; its id is the first author's family name and the year (the lane adds a letter where two would be the same)."""
    import build_references as br
    fam = re.sub(r"[^a-z]+", "", (cr["au"][0][0] if cr.get("au") else "anon").lower()) or "anon"
    yr = (cr.get("print") or cr.get("issued") or cr.get("online") or [None])[0]
    if not yr: return None
    rec = br.record(f"{fam}_{yr}", cr, pmcid or "")
    rec["verification"]["metadata_route"] = "Crossref's API, read by scripts/auto/papers.py"; rec["verification"]["verified_by"] = "the system (scripts/auto)"
    return rec


def initials(given):
    out = []
    for p in re.split(r"\s+", (given or "").replace(".", ". ").strip()):
        if not p: continue
        if "-" in p: out.append("-".join(q[0] + "." for q in p.split("-") if q))
        elif re.fullmatch(r"[A-Z]{1,3}", p): out.extend(c + "." for c in p)
        else: out.append(p[0] + ".")
    return " ".join(out)


def apa(rec):
    """A reference record as an APA 7 reference in plain text (the site's page formats the same record itself, with its
    italics: apaReference in site/src/app.core.js). Journal articles; anything else falls back to the same parts."""
    names = [a["literal"] if a.get("literal") else a["family"] + (", " + initials(a.get("given")) if a.get("given") else "") + (", " + a["suffix"] if a.get("suffix") else "") for a in rec.get("author") or []]
    au = names[0] if len(names) == 1 else ", ".join(names[:-1]) + ", & " + names[-1] if len(names) <= 20 else ", ".join(names[:19]) + ", … " + names[-1]
    y = ((rec.get("issued") or {}).get("date-parts") or [["n.d."]])[0][0]
    end = lambda t: "" if re.search(r"[.?!]$", t.strip()) else "."
    s = au + end(au) + f" ({y}). " + rec["title"] + end(rec["title"]) + " " + rec.get("container-title", "")
    if rec.get("volume"): s += ", " + str(rec["volume"])
    if rec.get("issue"): s += "(" + str(rec["issue"]).replace("-", "–") + ")"
    s += (", " + str(rec["page"]).replace("-", "–") if rec.get("page") else ", Article " + str(rec["number"]) if rec.get("number") else "") + "."
    if not rec.get("volume") and not rec.get("page") and not rec.get("number"): s += " Advance online publication."
    return s + (" https://doi.org/" + rec["DOI"] if rec.get("DOI") else "")


def retraction(rec, epmc_kind=None):
    """"retracted", "concern", "corrected" or "" for a reference record (Crossref's update links) and Europe PMC's own
    mark. A retracted paper, or one under an expression of concern, is never read for an answer."""
    st = ((rec or {}).get("verification") or {}).get("retraction_check", {}).get("status", "clear")
    if st == "retracted" or epmc_kind == "retracted": return "retracted"
    return {"expression-of-concern": "concern", "correction": "corrected"}.get(st, "")


# ---------- the searches for a question ----------
STOP = set("""a an the and or but if then than that this these those of in on at to for from by with without into over under about as is are was were be been being it its they them their there here he she
his her you your we our i me my not no nor do does did done have has had having can could may might must should would will shall who whom whose which what when where why how all any both each few more most other
some such only own same so too very just also still even ever never much many one two three really actually get gets getting got make makes made take takes taking took use uses using used people person someone
thing things like feel feels felt go goes going long time times way ways kind sort lot bit true real still does""".split())
# what a drug is called in papers: the words searched for each drug the site covers (and a few names people use)
# (an entry in round brackets is a search of its own: a short name that also means something else is searched only beside
# a word that says which meaning; in papers "LSD" is also a group of storage diseases, "DMT" a kind of treatment)
PSY = '(ABSTRACT:"psychedelic" OR ABSTRACT:"psychedelics" OR ABSTRACT:"hallucinogen" OR ABSTRACT:"hallucinogens" OR ABSTRACT:"hallucinogenic")'
SYN = {"alcohol": ["alcohol", "ethanol", "alcohol drinking"], "cannabis": ["cannabis", "marijuana", "cannabinoids", "tetrahydrocannabinol"], "cocaine": ["cocaine"], "heroin": ["heroin", "diacetylmorphine"],
       "ketamine": ["ketamine"], "lsd": ["lysergic acid diethylamide", "lysergide", f'((TITLE:"LSD" OR ABSTRACT:"LSD") AND {PSY})'], "mdma": ["MDMA", "3,4-methylenedioxymethamphetamine", '(TITLE:"ecstasy" AND ABSTRACT:"drug")'], "methamphetamine": ["methamphetamine"],
       "amphetamine": ["amphetamine", "amphetamines", "dextroamphetamine", "Adderall"], "psilocybin": ["psilocybin", "psilocin", "magic mushrooms"], "kratom": ["kratom", "mitragynine", "Mitragyna speciosa"],
       "dxm": ["dextromethorphan"], "benzodiazepines": ["benzodiazepines", "alprazolam", "diazepam"], "caffeine": ["caffeine", "coffee"], "nicotine": ["nicotine", "tobacco", "smoking", "e-cigarettes"],
       "nitrous-oxide": ["nitrous oxide"], "pcp": ["phencyclidine"], "ghb-gbl": ["gamma-hydroxybutyrate", "gamma-hydroxybutyric acid", "sodium oxybate"], "mescaline": ["mescaline", "peyote"], "dmt-ayahuasca": ["N,N-dimethyltryptamine", "dimethyltryptamine", "ayahuasca", f'((TITLE:"DMT" OR ABSTRACT:"DMT") AND {PSY})'],
       "5-meo-dmt": ["5-MeO-DMT", "5-methoxy-N,N-dimethyltryptamine"], "2c-x": ["2C-B", "2C drugs", "psychedelic phenethylamines"], "salvia-divinorum": ["Salvia divinorum", "salvinorin A"], "synthetic-cannabinoids": ["synthetic cannabinoids", "synthetic cannabinoid receptor agonists", "JWH-018"],
       "synthetic-cathinones": ["synthetic cathinones", "mephedrone", "bath salts"], "fentanyl-and-analogues": ["fentanyl", "fentanyl analogues"], "prescription-opioids": ["opioids", "oxycodone", "opioid analgesics"],
       "methadone-buprenorphine": ["methadone", "buprenorphine", "opioid agonist treatment"], "methylphenidate": ["methylphenidate"], "alkyl-nitrites-and-inhalants": ["alkyl nitrites", "poppers", "inhalants", "volatile substance"]}
FAMILY = {"psychedelics": ["psychedelics", "hallucinogens", "psilocybin", "LSD"], "opioids": ["opioids", "heroin", "opioid"], "stimulants": ["stimulants", "amphetamine", "cocaine"], "drugs": ["illicit drugs", "substance use", "psychoactive drugs"]}


def drug_terms(question, names):
    """The words to search for the drugs a question names: [names of each drug], and the question's words that name them."""
    groups, used = [], []
    for n, slugs in names:                                   # the site's own table of names, the longest first
        m = re.search(r"(?<!\w)" + re.escape(n) + r"(?!\w)", question, re.I)
        if not m or any(a <= m.start() < b for a, b in used): continue
        used.append((m.start(), m.end()))
        terms = []
        if len(slugs) > 1 and n.rstrip("s") + "s" in FAMILY: terms = FAMILY[n.rstrip("s") + "s"]
        else:
            for s in slugs[:3]: terms += SYN.get(s, [s.replace("-", " ")])
        g = list(dict.fromkeys(terms))
        if g and g not in groups: groups.append(g)
    return groups, used


def topic_terms(texts, used_spans_text):
    """The words of a question and its other wordings that are not small words and not a drug's name, the most used first."""
    count = {}
    for t in texts:
        for w in set(re.findall(r"[a-z][a-z'-]{2,}", used_spans_text(t).lower())):
            w = w.strip("'-")
            if w in STOP or len(w) < 3: continue
            count[w] = count.get(w, 0) + 1
    return [w for w, _ in sorted(count.items(), key=lambda x: (-x[1], x[0]))][:10]


def field(terms, title_only=False):
    """The words of one group as a search: any of them in the title or the abstract (a word in round brackets is a search
    of its own and stands as it is)."""
    return "(" + " OR ".join(t if t.startswith("(") else f'TITLE:"{t}"' if title_only else f'TITLE:"{t}" OR ABSTRACT:"{t}"' for t in terms) + ")"


# (18 November 2026, 22:40 Athens) A question about a place is about that place. "What is the mortality rate associated with heroin use in Greece?" was searched
# under words for deaths from opioids, none of which was the country: the lane read papers on other countries and wrote that no source it could read gave a
# finding. The countries a question names (data/site/world-law.json, with the everyday names of a few), and Europe: its papers must name the place.
PLACE_MORE = {"United States of America": ["United States", "USA", "U.S.", "America", "American"], "United Kingdom of Great Britain and Northern Ireland": ["United Kingdom", "UK", "Britain", "British", "England", "Scotland", "Wales"],
              "Russian Federation": ["Russia", "Russian"], "Netherlands (Kingdom of the)": ["Netherlands", "Dutch", "Holland"], "Iran (Islamic Republic of)": ["Iran", "Iranian"], "Republic of Korea": ["South Korea", "Korea", "Korean"],
              "Czech Republic": ["Czechia", "Czech Republic", "Czech"], "Greece": ["Greece", "Greek"], "Germany": ["Germany", "German"], "France": ["France", "French"], "Spain": ["Spain", "Spanish"], "Italy": ["Italy", "Italian"],
              "Portugal": ["Portugal", "Portuguese"], "Sweden": ["Sweden", "Swedish"], "Norway": ["Norway", "Norwegian"], "Australia": ["Australia", "Australian"], "Canada": ["Canada", "Canadian"], "Ireland": ["Ireland", "Irish"]}
def places_named(question):
    """The places a question names, each as the words a paper may use for it: [["Greece", "Greek"]]. Read from the question as our own wording puts it."""
    try: C = [c["name"] for c in json.load(open(ROOT / "data" / "site" / "world-law.json", encoding="utf-8"))["countries"] if c.get("name") and c["name"] != "European Union"]
    except (OSError, ValueError, KeyError): C = []
    out, text = [], " " + re.sub(r"[^A-Za-z.' -]+", " ", str(question)) + " "
    for name in C:
        ways = list(dict.fromkeys(PLACE_MORE.get(name) or [re.sub(r"\s*\(.*\)$", "", name)]))
        said = [w for w in ways if re.search(r"(?<![A-Za-z])" + re.escape(w) + r"(?![A-Za-z])", text)]      # (as written, with its capital: "cold turkey" is not Turkey)
        if said and ways not in out: out.append(ways)
    if re.search(r"(?<![A-Za-z])(?:Europe|European Union|the EU)(?![A-Za-z])", text): out.append(["Europe", "European"])
    return out[:2]


def searches(question, ways, names, drugs=None, terms=None, extra=None):
    """The searches for a question, in Europe PMC's syntax, each with what it is for. Reviews that can be read first; then
    any paper that can be read; then reviews that cannot (for the list of papers wanted); then the drug's most cited
    reviews. drugs: the drugs the question is about, by the site's names for them (also where it names none); terms: the
    words papers use for its subject (data/site/wanted.json): without them, the question's own words are searched."""
    groups, _ = drug_terms(question, names)
    for s in drugs or []:
        g = list(dict.fromkeys(SYN.get(s, [s.replace("-", " ")])))
        if g not in groups: groups.append(g)
    if drugs and len(drugs) > 1 and len(groups) > 1 and not drug_terms(question, names)[0]: groups = [[t for g in groups for t in g]]   # several drugs the question does not name one by one: any of them
    if extra and not groups: groups = [list(dict.fromkeys(str(n) for n in extra if n))]      # a drug that has no page yet: what papers call it comes with the question (scripts/auto/grow.py)
    pat = re.compile(r"(?<!\w)(" + "|".join(re.escape(n) for n, _ in names) + r")(?!\w)", re.I)
    own_words = lambda: topic_terms([question] + list(ways or []), lambda t: pat.sub(" ", t))
    topics = list(terms)[:10] if terms else own_words()
    # (18 November 2026) A topic word that IS the drug's name, or holds it, says nothing of the subject: with it, every paper on the drug counted as a paper on
    # the question. The words for "Does caffeine affect growth?" (written by the model that words a visitor's question) began with "caffeine": the lane read 23
    # sources on caffeine and sport, none on growth, for 39 minutes, and wrote that nothing readable had a finding. Seven of the 74 questions searched by then
    # had such a word, six of them questions visitors had sent. Such words are left out; where none is left, the question's own words are the topic. (Only a
    # word that IS a name of the drug: "opioid withdrawal" is a subject, and as one of several words it finds only papers that say exactly that.)
    one = lambda w: re.sub(r"s$", "", str(w).lower().strip())
    drugw = {one(x) for g in groups for x in g}
    kept = [w for w in topics if str(w).startswith("(") or one(w) not in drugw]
    if len(kept) != len(topics): topics = kept or [w for w in own_words() if one(w) not in drugw]
    drug = " AND ".join(field(g) for g in groups) if groups else field(FAMILY["drugs"])
    topic = field(topics) if topics else ""
    core = drug + (" AND " + topic if topic else "")
    for pl in places_named(question): core += " AND " + field(pl)          # (a question about a place: its papers name the place)
    rev = '(PUB_TYPE:"review" OR PUB_TYPE:"systematic review" OR PUB_TYPE:"meta-analysis")'
    not_retr = 'NOT PUB_TYPE:"retracted publication" NOT PUB_TYPE:"retraction of publication"'
    out = [{"for": "reviews and meta-analyses whose full text is open", "query": f"{core} AND {rev} AND OPEN_ACCESS:y AND LANG:eng {not_retr}"},
           {"for": "any paper whose full text is open", "query": f"{core} AND OPEN_ACCESS:y AND LANG:eng {not_retr}"},
           {"for": "reviews and meta-analyses, open or not (the ones that cannot be read are listed as wanted)", "query": f"{core} AND {rev} AND LANG:eng {not_retr}"}]
    if topic: out.append({"for": "the most cited papers on it, open or not", "query": f"{core} AND LANG:eng {not_retr}", "sort": "CITED desc"})
    if groups and topic:   # a wider net: the drug in the title, any topic, reviews that can be read (the ranking by meaning then picks)
        out.append({"for": "reviews of the drug itself, open, whatever their topic (ranked by meaning afterwards)", "query": " AND ".join(field(g, True) for g in groups) + f" AND {rev} AND OPEN_ACCESS:y AND LANG:eng {not_retr}"})
    return out, groups, topics


# ---------- the order of reading ----------
class General:
    """all-MiniLM-L6-v2 (site/insight/vendor), run by the Python onnxruntime: sentences to unit vectors, for meaning."""
    def __init__(self):
        import numpy as np, onnxruntime as ort
        from tokenizers import BertWordPieceTokenizer
        v = ROOT / "site" / "insight" / "vendor"
        self.np = np; self.tok = BertWordPieceTokenizer(str(v / "vocab.txt"), lowercase=True); self.tok.enable_truncation(200); self.tok.enable_padding()
        self.s = ort.InferenceSession(str(v / "all-MiniLM-L6-v2-q8.onnx"), providers=["CPUExecutionProvider"]); self.inputs = [i.name for i in self.s.get_inputs()]
    def __call__(self, texts):
        np, out = self.np, []
        for i in range(0, len(texts), 32):
            enc = self.tok.encode_batch(texts[i:i + 32]); ii = np.array([e.ids for e in enc], dtype=np.int64); am = np.array([e.attention_mask for e in enc], dtype=np.int64)
            feed = {"input_ids": ii, "attention_mask": am}
            if "token_type_ids" in self.inputs: feed["token_type_ids"] = np.zeros_like(ii)
            h = self.s.run(None, feed)[0]; m = am[..., None].astype(np.float32); v = (h * m).sum(1) / np.maximum(m.sum(1), 1e-9)
            out.append(v / np.maximum(np.linalg.norm(v, axis=-1, keepdims=True), 1e-9))
        return np.vstack(out) if out else np.zeros((0, 384), np.float32)


sentences = lambda t: [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", t or "") if len(s.strip()) >= 30]
HUMAN = re.compile(r"\b(participants?|patients?|volunteers?|adults?|adolescents?|people|persons?|individuals|users?|men|women|cohort|survey|randomi[sz]ed|trial|respondents|students|drinkers|smokers)\b", re.I)
ANIMAL = re.compile(r"\b(rats?|mice|mouse|rodents?|zebrafish|in vitro|cell lines?|primates?|monkeys?)\b", re.I)


def rank(question, ways, cands, enc):
    """The candidates in the order of reading. near: how near in meaning the paper's title or any sentence of its abstract
    is to the question or one of its wordings (0 to 1). The order: near, a little more for a review, for people, for
    paper much cited (a new paper nobody has cited yet stands behind an established one that is as near); a little less
    for animals or cells alone."""
    if not cands: return []
    import numpy as np, math
    Q = enc([question] + list(ways or [])[:6])
    for c in cands:
        ss = sentences(c["abstract"]); S = enc([c["title"]] + (ss if len(ss) <= 9 else ss[:6] + ss[-3:])); sim = S @ Q.T   # the title, and the abstract's first and last sentences (its aim and its conclusion)
        c["near"] = round(float(max(sim[0].max(), sim.max() * 0.97, float(np.sort(sim.max(1))[-3:].mean()) if len(S) > 3 else 0)), 3)
        text = c["title"] + " " + c["abstract"]
        people = bool(HUMAN.search(text)); animal = bool(ANIMAL.search(text)) and not people
        c["people"] = people and not animal
        c["score"] = round(c["near"] + (0.06 if c["kind"] == "review" else 0.02 if c["kind"] == "study" else 0) + (0.02 if c["people"] else -0.06 if animal else 0)
                           + (0.01 if (c["year"] or 0) >= 2010 else 0) + min(0.07, 0.025 * math.log10(1 + c["cited"])), 3)
    return sorted(cands, key=lambda c: (-c["score"], c["epmc"]))


_PLACE = None


def page_names(item):
    """(17 November 2026) The names papers may use for a drug that has no page here, for a question that brings none with it (a
    question a visitor sent, listed by scripts/auto/ask.py). The senior author asked about kanna and Mitragyna javanica; both
    were searched as (illicit drugs OR substance use OR psychoactive drugs) AND (kanna OR psychoactive OR euphoric ...): the
    name was one word among the topic's, so papers about anything psychoactive came back and none about kanna. The names are
    the ones the question itself uses (the filing's and the ones the system learned: scripts/auto/place.py), and, where the
    page is the page of one drug, the titles the filing keeps for it (its species: "Sceletium tortuosum" for kanna).
    [] where the question names a drug that has a page, or none."""
    global _PLACE
    try:
        import place as PL
        if _PLACE is None: _PLACE = PL.Placer()
        got = _PLACE.place(item["q"], item.get("ways") or [])
    except Exception as e:                                                    # (never silently again: the run's notes say it)
        if not getattr(page_names, "said", False): page_names.said = True; print("papers: !! the names of a drug without a page could not be worked out:", type(e).__name__, str(e)[:160])
        return []
    home = got.get("home") or ""
    if not home.startswith("new:") or got.get("drugs"): return []
    page = home[4:]; out = [n for n in got.get("fresh") or [] if isinstance(n, str)]
    try: F = json.load(open(ROOT / "data" / "auto" / "filing.json", encoding="utf-8"))
    except (OSError, ValueError): F = {}
    of_page = [n for n, v in (F.get("names") or {}).items() if isinstance(v, dict) and v.get("new") == page]
    if len(of_page) <= 3: out += of_page + [t for t in (F.get("wiki") or {}).get(page) or [] if isinstance(t, str)]      # the page of one drug: every name of it
    if not of_page and re.fullmatch(r"[A-Z][a-z]+ [a-z-]+", page): out.append(page)                                             # a name the system learned: the page is named after it
    seen, names_ = set(), []
    for n in out:
        n = (n or "").strip()
        if n and n.lower() not in seen: seen.add(n.lower()); names_.append(n)
    return names_[:8]


def find(item, names, enc, opener=None):
    """Everything found for one question (see the head of this file)."""
    extra = item.get("names") or (page_names(item) if not item.get("drugs") else [])
    qs, groups, topics = searches(item["q"], item.get("ways") or [], names, item.get("drugs"), item.get("terms"), extra)
    seen, log, problems = {}, [], []
    for s in qs:
        try: got, hits = epmc_search(s["query"], opener=opener, sort=s.get("sort"))
        except Refused as e: problems.append("Europe PMC said no: " + str(e)); break
        except (IOError, ValueError) as e: problems.append("a search failed: " + str(e)[:200]); continue
        log.append(dict({"for": s["for"], "query": s["query"], "found": hits, "read": len(got)}, **({"sort": s["sort"]} if s.get("sort") else {})))
        for p in got:
            if p["kind"] in ("retracted", "notice", "opinion") or not p["title"]: continue
            k = p["doi"] or p["epmc"]
            if k not in seen: seen[k] = p
    # (18 November 2026) A drug with few papers, or a question that asks what a drug IS: the topic words find little, and what there is on the drug itself is
    # the answer's material ("What is Mitragyna javanica?"). Where the searches above found fewer than four papers that can be read, every open paper that
    # names the drug in its title or its summary is searched as well (a rare plant is named in the summaries of papers on its better-known relatives: the
    # title alone found none of them); the ranking by meaning then picks.
    if groups and not problems and sum(1 for p in seen.values() if p["oa"] and p["pmcid"]) < 4:
        s = {"for": "any open paper that names the drug in its title or summary, whatever its topic (the searches above found few that can be read)",
             "query": " AND ".join(field(g) for g in groups) + ' AND OPEN_ACCESS:y AND LANG:eng NOT PUB_TYPE:"retracted publication" NOT PUB_TYPE:"retraction of publication"'}
        try:
            got, hits = epmc_search(s["query"], opener=opener)
            log.append({"for": s["for"], "query": s["query"], "found": hits, "read": len(got)})
            for p in got:
                if p["kind"] in ("retracted", "notice", "opinion") or not p["title"]: continue
                k = p["doi"] or p["epmc"]
                if k not in seen: seen[k] = p
        except Refused as e: problems.append("Europe PMC said no: " + str(e))
        except (IOError, ValueError) as e: problems.append("a search failed: " + str(e)[:200])
    # only papers that can be used are compared: the ones whose full text is open, and reviews (for the list of papers wanted)
    usable = [p for p in seen.values() if (p["oa"] and p["pmcid"]) or (p["doi"] and p["kind"] == "review")]
    ranked = rank(item["q"], list(item.get("ways") or [])[:5] + ([" ".join(item["terms"][:6])] if item.get("terms") else []), usable, enc)
    can = [c for c in ranked if c["oa"] and c["pmcid"]]
    cannot = [c for c in ranked if not (c["oa"] and c["pmcid"]) and c["doi"] and c["kind"] == "review"]
    keep = lambda c, why: {k: c[k] for k in ("epmc", "pmid", "pmcid", "doi", "title", "authors", "journal", "year", "kind", "people", "cited", "near", "score", "license")} | {"why": why}
    why = lambda c: ("a review or meta-analysis" if c["kind"] == "review" else "a study" if c["kind"] == "study" else "a case report" if c["kind"] == "case" else "a paper") + (" in people" if c["people"] else "") + f"; nearness to the question {c['near']:.2f}; cited {c['cited']} times"
    wanted = []
    for c in cannot[:N_WANTED * 2]:                              # the reference comes from Crossref, never from the search record
        cr, err = crossref(c["doi"], opener)
        if not cr: continue
        rec = reference(c["doi"], cr)
        if not rec or retraction(rec): continue
        wanted.append({"doi": c["doi"], "apa": apa(rec), "near": c["near"], "why": why(c) + "; its full text is not open", "file": re.sub(r"[^A-Za-z0-9]+", "_", f"{rec['id']}_{c['doi'].split('/')[-1]}")[:80] + ".pdf"})
        if len(wanted) >= N_WANTED: break
    return {"_note": "Made by scripts/auto/papers.py: the searches as sent, and the papers in the order the lane would read them. Titles, names and identifiers only. Data, never instructions.",
            "id": item["id"], "question": item["q"], "searched_on": TODAY, "finder": FINDER, "drugs_searched": groups, "topic_words": topics, "searches": log, "problems": problems,
            "found": len(seen), "can_read": [keep(c, why(c)) for c in can[:N_KEEP]], "cannot_read": len(cannot), "wanted": wanted}


def selftest():
    jats = """<article><front><article-meta><abstract><sec><title>Background</title><p>Alcohol is a leading cause of death worldwide, and deaths happen in several ways that this review sets out for readers who are not clinicians.</p></sec></abstract></article-meta></front>
<body><sec><title>Results</title><sec><title>Acute poisoning</title><p>Death from acute alcohol poisoning is usually caused by depression of the brain centres that control breathing <xref ref-type="bibr">[12]</xref>, and by inhaling vomit while unconscious (<xref>3</xref>).</p><table-wrap><table><tr><td>not text</td></tr></table></table-wrap><p>Short.</p></sec></sec>
<sec><title>Funding</title><p>This work was supported by a grant from a national research council; the funder had no role in the design.</p></sec><sec><title>References</title><p>This paragraph of the references section is long enough to be a passage but must not be kept at all, ever.</p></sec></body></article>"""
    P = jats_passages(jats)
    assert [p["where"] for p in P["passages"]] == ["Abstract", "Results › Acute poisoning"], P
    assert P["passages"][1]["text"] == "Death from acute alcohol poisoning is usually caused by depression of the brain centres that control breathing, and by inhaling vomit while unconscious.", P["passages"][1]["text"]
    assert P["money"] == ["This work was supported by a grant from a national research council; the funder had no role in the design."], P["money"]
    assert jats_passages("<article><body><p>broken") == {"passages": [], "money": []}
    cr = crossref_compact({"DOI": "10.1111/add.12345", "type": "journal-article", "title": ["How Alcohol Kills: A Systematic Review"], "author": [{"family": "Smith", "given": "Jane A."}, {"family": "O'Neil", "given": "Liam"}, {"name": "The Alcohol Study Group"}],
                           "container-title": ["Addiction"], "volume": "118", "issue": "4", "page": "601-615", "issued": {"date-parts": [[2023, 4]]}, "published-print": {"date-parts": [[2023, 4]]}, "publisher": "Wiley",
                           "updated-by": [{"type": "correction", "DOI": "10.1111/add.99999"}]})
    rec = reference("10.1111/add.12345", cr, "PMC1234567")
    assert rec["id"] == "smith_2023" and rec["title"] == "How alcohol kills: A systematic review" and rec["PMCID"] == "PMC1234567" and retraction(rec) == "corrected", rec
    assert apa(rec) == "Smith, J. A., O'Neil, L., & The Alcohol Study Group. (2023). How alcohol kills: A systematic review. Addiction, 118(4), 601–615. https://doi.org/10.1111/add.12345", apa(rec)
    assert retraction(reference("10.1/x", dict(cr, upd=["retraction:10.1/y"]))) == "retracted"
    names = [["crystal meth", ["methamphetamine"]], ["alcohol", ["alcohol"]], ["psychedelics", ["lsd", "psilocybin", "mescaline"]], ["weed", ["cannabis"]], ["meth", ["methamphetamine"]]]
    qs, groups, topics = searches("How can you die from alcohol?", ["can alcohol kill you", "what kills you when you drink too much alcohol", "alcohol death causes"], names)
    assert groups == [["alcohol", "ethanol", "alcohol drinking"]] and topics[:2] == ["die", "kill"] or "die" in topics, (groups, topics)
    assert len(qs) == 5 and qs[3].get("sort") == "CITED desc" and 'TITLE:"ethanol"' in qs[0]["query"] and "OPEN_ACCESS:y" in qs[0]["query"] and "OPEN_ACCESS" not in qs[2]["query"] and 'NOT PUB_TYPE:"retracted publication"' in qs[1]["query"], qs
    g2, _ = drug_terms("Do psychedelics help with crystal meth problems?", names); assert g2 == [["methamphetamine"], ["psychedelics", "hallucinogens", "psilocybin", "LSD"]], g2
    q3, g3, t3 = searches("What is a K-hole?", ["what does a k hole feel like"], names, ["ketamine"], ["k-hole", "dissociation"]); assert g3 == [["ketamine"]] and t3 == ["k-hole", "dissociation"] and 'ABSTRACT:"dissociation"' in q3[0]["query"], (g3, t3)
    q4, g4, _ = searches("Does LSD stay in your body forever?", [], [["lsd", ["lsd"]]], None, ["half-life"]); assert 'TITLE:"lysergide"' in q4[0]["query"] and '((TITLE:"LSD" OR ABSTRACT:"LSD") AND (ABSTRACT:"psychedelic"' in q4[0]["query"] and 'TITLE:"LSD" OR ABSTRACT:"LSD" OR' not in q4[0]["query"], q4[0]["query"]
    # a topic word that is the drug's own name is left out (with it, every paper on the drug counted as a paper on the question); a phrase that holds it stays;
    # where nothing is left, the question's own words are the topic
    q5, g5, t5 = searches("Does caffeine affect growth?", ["can caffeine stunt growth", "caffeine and height growth"], [["caffeine", ["caffeine"]]], ["caffeine"], ["Caffeine", "growth", "height", "caffeine intake"])
    assert t5 == ["growth", "height", "caffeine intake"] and '(TITLE:"growth" OR ABSTRACT:"growth" OR TITLE:"height"' in q5[0]["query"] and ' AND (TITLE:"caffeine" OR ABSTRACT:"caffeine" OR TITLE:"growth"' not in q5[0]["query"], (t5, q5[0]["query"])
    q6, g6, t6 = searches("Does caffeine affect growth?", ["can caffeine stunt growth", "caffeine and height growth"], [["caffeine", ["caffeine"]]], ["caffeine"], ["caffeine", "coffee"])
    assert "growth" in t6 and "caffeine" not in t6 and "coffee" not in t6, t6
    # a question about a place: its papers must name the place (and "cold turkey" is no country)
    assert places_named("What is the mortality rate associated with heroin use in Greece?") == [["Greece", "Greek"]] and places_named("How do people come off opioids cold turkey?") == [] and places_named("How many people in the United States and in Europe use cocaine?") == [["United States", "USA", "U.S.", "America", "American"], ["Europe", "European"]], places_named("How many people in the United States and in Europe use cocaine?")
    q7, _, _ = searches("What is the mortality rate associated with heroin use in Greece?", [], [["heroin", ["heroin"]]], ["heroin"], ["opioid-related mortality", "drug-related deaths"])
    assert all(' AND (TITLE:"Greece" OR ABSTRACT:"Greece" OR TITLE:"Greek" OR ABSTRACT:"Greek")' in q["query"] for q in q7[:4]) and "Greece" not in q7[-1]["query"], [q["query"][:200] for q in q7]
    # a pretend service: two searches answer, the full text is offered for one paper, Crossref knows the DOIs
    core = lambda i, **k: dict({"id": str(100 + i), "source": "MED", "pmid": str(100 + i), "doi": f"10.1000/j.{i}", "title": f"Causes of death from alcohol: review number {i}.", "authorString": "Smith J, Jones K.",
                               "journalInfo": {"journal": {"title": "Addiction"}}, "pubYear": "2021", "abstractText": "<p>Alcohol can cause death by acute poisoning that stops breathing. Participants were adults in ten countries.</p>",
                               "isOpenAccess": "N", "inEPMC": "N", "citedByCount": 10 * i, "pubTypeList": {"pubType": ["Journal Article", "Review"]}, "language": "eng"}, **k)
    calls = []
    class Resp:
        def __init__(self, b): self.b = b
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self): return self.b
    def opener(req, timeout=0):
        u = req.full_url; calls.append(u); assert "pharmakon.world" in req.get_header("User-agent")
        if "/search?" in u:
            res = [core(1, isOpenAccess="Y", inEPMC="Y", pmcid="PMC111"), core(2), core(3, pubTypeList={"pubType": ["Retracted Publication"]}), core(4, title="Sleep in the mouse after ethanol.", abstractText="Mice were given ethanol in vitro.", isOpenAccess="Y", pmcid="PMC444", pubTypeList={"pubType": ["Journal Article"]})]
            return Resp(json.dumps({"hitCount": 57, "resultList": {"result": res}}).encode())
        if "api.crossref.org/works/" in u:
            if "j.2" in u: return Resp(json.dumps({"message": {"DOI": "10.1000/j.2", "type": "journal-article", "title": ["Causes of Death From Alcohol"], "author": [{"family": "Smith", "given": "J."}], "container-title": ["Addiction"], "volume": "1", "page": "1-9", "issued": {"date-parts": [[2021]]}}}).encode())
            raise urllib.error.HTTPError(u, 404, "nf", {}, None)
        raise AssertionError(u)
    class Enc2:   # nearness without the model: a few words in common
        def __call__(self, texts):
            import numpy as np
            words = "alcohol die death kill causes poisoning breathing mouse sleep ethanol review".split()
            M = np.array([[1.0 if w in t.lower() else 0.0 for w in words] + [0.1] for t in texts], np.float32)
            return M / np.linalg.norm(M, axis=1, keepdims=True)
    out = find({"id": "w_0027", "q": "How can you die from alcohol?", "ways": ["can alcohol kill you", "alcohol death causes"]}, names, Enc2(), opener)
    assert out["found"] == 3 and [c["pmcid"] for c in out["can_read"]] == ["PMC111", "PMC444"] and out["can_read"][0]["kind"] == "review" and not out["can_read"][1]["people"], out["can_read"]
    assert len(out["wanted"]) == 1 and out["wanted"][0]["apa"].startswith("Smith, J. (2021). Causes of death from alcohol. Addiction, 1, 1–9. https://doi.org/10.1000/j.2") and out["wanted"][0]["file"].endswith(".pdf"), out["wanted"]
    # (two papers that can be read are fewer than four: every open paper that names the drug is searched as well, last)
    assert all("abstract" not in c for c in out["can_read"]) and len(out["searches"]) == 6 and out["searches"][0]["found"] == 57 and out["searches"][5]["for"].startswith("any open paper that names the drug in its title or summary") and out["searches"][5]["query"].startswith('(TITLE:"alcohol" OR ABSTRACT:"alcohol" OR TITLE:"ethanol" OR ABSTRACT:"ethanol" OR TITLE:"alcohol drinking" OR ABSTRACT:"alcohol drinking") AND OPEN_ACCESS:y'), out["searches"]
    print("papers selftest: ok (a full text as passages without its reference marks, tables and reference list; a Crossref record as an APA 7 reference; the searches; a pretend search with a retracted paper left out and a paper that cannot be read listed as wanted)")


def main():
    if "--selftest" in sys.argv: return selftest()
    arg = sys.argv[1:]
    if not arg or arg[0] != "find": sys.exit(__doc__)
    opt = lambda k, d=None: arg[arg.index(k) + 1] if k in arg else d
    out = ROOT / opt("--out", "data/auto/papers"); out.mkdir(parents=True, exist_ok=True)
    items = listed()
    import build_index as bi
    names = bi.names_table()                                                   # (before old(), which asks what the finder would search today)
    ids = [x for x in (opt("--ids") or "").split(",") if x]; limit = int(opt("--max", "50")); t0 = time.time(); minutes = float(opt("--minutes", "0") or 0)
    def old(w):   # not searched yet, or searched by an older finder, or searched without the name of its drug (page_names: a drug without a page)
        f = out / (w["id"] + ".json")
        try: rec = json.load(open(f, encoding="utf-8"))
        except (OSError, ValueError): return True
        if int(rec.get("finder") or 1) < FINDER: return True
        if rec.get("problems"): return True                                    # (18 November 2026) its searches did not all come back (the index was slow or said no): searched again, not kept as "searched"
        try:                                                                   # (18 November 2026) the finder would ask something else today (its searches were mended since): searched again
            extra = w.get("names") or (page_names(w) if not w.get("drugs") else [])
            today = searches(w["q"], w.get("ways") or [], names, w.get("drugs"), w.get("terms"), extra)[0]
            then = [s.get("query") for s in rec.get("searches") or []]
            if then and today and then[0] != today[0]["query"]: return True
        except Exception: pass
        return not rec.get("drugs_searched") and not w.get("drugs") and (bool(w.get("names")) or bool(page_names(w)))
    # --requests DIR: the requests waiting there (papers-*.json: {"ids": [...], "max": N, "again": true}), each taken off when read.
    # A request is a file in the repository, written by the editor: it is read as data here and never reaches a command line.
    if "--requests" in arg:
        again = False
        for f in sorted((ROOT / opt("--requests")).glob("papers-*.json")):
            try: r = json.load(open(f, encoding="utf-8"))
            except ValueError: r = {}
            ids += [x for x in (r.get("ids") or []) if isinstance(x, str) and re.fullmatch(r"w_[a-z0-9_]{1,40}", x)]
            if isinstance(r.get("max"), int): limit = max(1, min(60, r["max"]))
            again = again or r.get("again") is True
            f.unlink()
        if ids: items = [w for w in items if w["id"] in ids]
        elif not again: items = [w for w in items if old(w)]
    elif ids: items = [w for w in items if w["id"] in ids]
    else: items = [w for w in items if old(w)]
    if "--sent" in arg: items = [w for w in items if w.get("from") == "a question visitors sent"]      # (18 November 2026) the first pass of a run: only the questions people sent
    items = sorted(items, key=lambda w: ((out / (w["id"] + ".json")).exists(), 0 if w.get("from") == "a question visitors sent" else 1))[:limit]     # a question never searched comes before one searched by an older finder; among those, one a person sent comes first (18 November 2026: it is answered in the same run)
    enc = General(); done = 0
    for w in items:
        if minutes and time.time() - t0 > minutes * 60: print(f"papers: the time for this run is up; {len(items) - done} questions are left for the next run"); break
        try: res = find(w, names, enc)
        except Refused as e: print("papers: stopped,", e); break
        json.dump(res, open(out / (w["id"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1); done += 1
        print(f"papers: {w['id']} {w['q'][:60]!r}: {res['found']} found, {len(res['can_read'])} that can be read, {len(res['wanted'])} wanted" + (f"; problems: {'; '.join(res['problems'])}" if res["problems"] else ""))
    print(f"papers: {done} questions searched")


if __name__ == "__main__":
    main()
