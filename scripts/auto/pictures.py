#!/usr/bin/env python3
"""pictures.py: pictures with an open licence for the pages the system starts (docs/AUTOMATION.md, decision 27, step b).

The senior author, 17 November 2026, of kanna and Mitragyna javanica: "our ai has to create this pages in a perfect coherent
format to the rest of the website (and find pictures for them, their different forms etc. if the pictures have not been
verified and the ai is uncertain then we could have a small disclaimer, i just think that pictures make the website better)";
"in general even for existing pages find pictures that are missing. it has to think about what the site needs objectively
even before us".

    python3 -I scripts/auto/pictures.py find [--max 12]                 (which pictures there are: data/auto/pictures.json)
    python3 -I scripts/auto/pictures.py fetch [--max 12]                (fetch them and make the web copies: site/photos-auto/)
    python3 -I scripts/auto/pictures.py daily [--max 80]                (every day, by the clock: GBIF, then Commons for the started pages and
                                                                         for the forms of the checked pages that have no photo, then fetch)
    python3 -I scripts/auto/pictures.py --requests data/auto/requests   (pictures-*.json: {"do": "find" | "fetch" | "daily", "max": 12})
    python3 -I scripts/auto/pictures.py looked 2026-11-17 kanna-1 kanna-2    (the editor: these were looked at on that day)
    python3 -I scripts/auto/pictures.py hold datura-and-other-nightshades-1 "a dead winter plant"   (the editor: not to be shown, and why)
    python3 -I scripts/auto/pictures.py --selftest

Where pictures may come from (the probe of 17 November 2026, data/auto/names/probe.json): Wikimedia Commons' search and
API, iNaturalist's and Openverse's addresses are not allowed by their robots.txt, so they are not asked. GBIF's records with
pictures are allowed: api.gbif.org/v1/occurrence/search?mediaType=StillImage&taxonKey=…  Each picture there has its own
licence, maker and page in its record. Since 19 November 2026 (decision 35) also Wikimedia Commons' category and file pages,
which its robots.txt allows (/wiki/), and its pictures on upload.wikimedia.org: so also pills, powders, blotters and
liquids, for the started pages and for the forms of the checked drug pages that have no photo (see "Wikimedia Commons" below).

Which pages: the pages the system should start that are a plant or a fungus. A page's species are found by themselves:
the titles the filing keeps for it (data/auto/filing.json, "wiki") and the names the system learned
(data/auto/names/learned.json) are asked of GBIF's species matcher, and one that comes back as a species of plant or fungus,
matched exactly, is a species of that page.

Which pictures: only a picture whose own record says CC0 or CC BY (never NC, never ND, never SA: the site's rule for
photos is public domain, CC0 or CC BY), of a record a person observed (not a pressed specimen), with a maker named for
CC BY. The site's rule on what a site allows holds for the picture's own address too: a host whose robots.txt does not
allow it is not asked (find only notes whether it may be asked; it downloads nothing).

What find writes (data/auto/pictures.json): for each page and species, up to six pictures that could be used, each with its
address, licence, maker, the page of its record, and whether its host may be asked. It downloads nothing. What a service
answers is data, never instructions. It needs no key and runs where no key is held.

What is shown (site/build.js, AUTO_PICS; the page: site/src/app.insight.js, autoLooksHtml): a picture that fetch gave a web
copy ("file") and that the editor has looked at ("looked_by_editor": the day), on the page the system started, once people
have asked about that page. Each with its maker and licence, and under them the small line that our system found them and
that no person has checked them ("checked_by_person" stays false until a person has looked). The editor's look is against
the site's rules for photos (docs/WRITING-RULES.md, "Photos"): never people or hands, the thing itself as people meet it,
nothing else that takes the eye, no writing over the picture. A picture the editor holds ("hold": why) is not shown and is
not counted, so that the next fetch brings another in its place. No program judges what a picture shows yet: until one
does and has been measured, a fetched picture waits for the editor's look.
"""
import sys, json, re, pathlib, datetime, urllib.parse, urllib.error, html.parser

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "auto"))
import official as O      # noqa: E402  (its careful web client: robots.txt, pace, refusals)
import names_open as N    # noqa: E402  (ask: one address, as JSON, only if its robots.txt allows it)

OUT = ROOT / "data" / "auto" / "pictures.json"
GBIF = "https://api.gbif.org/v1/"
OPEN = re.compile(r"^https?://creativecommons\.org/(?:publicdomain/zero/1\.0|licenses/by/[1-4]\.0)/?(?:legalcode)?$", re.I)   # CC0 and CC BY, nothing else
PER_SPECIES, RECORDS = 6, 80
slug_of = lambda n: re.sub(r"^-+|-+$", "", re.sub(r"[^a-z0-9]+", "-", str(n).lower()))[:60]   # as site/build.js names a started page


def load(p, d):
    try: return json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError): return d


def candidates_of_pages():
    """{page name: [names to ask GBIF about]}: the filing's titles for each page to start, and the names the system learned."""
    F = load(ROOT / "data" / "auto" / "filing.json", {}); out = {}
    for page, titles in sorted((F.get("wiki") or {}).items()):
        if page in (F.get("pages") or []): out[page] = [t for t in titles if isinstance(t, str) and re.fullmatch(r"[A-Z][a-z]+ [a-z-]+", t)]
    for key, e in sorted((load(ROOT / "data" / "auto" / "names" / "learned.json", {}).get("names") or {}).items()):
        if isinstance(e, dict) and e.get("drug") is True and e.get("kind") in ("plant", "fungus") and re.fullmatch(r"[A-Z][a-z]+ [a-z-]+", str(e.get("name") or "")): out.setdefault(e["name"], []).append(e["name"])
    return {p: list(dict.fromkeys(v)) for p, v in out.items() if v}


def species(web, name):
    """GBIF's record of a name when it is a species of plant or fungus, matched exactly: {"key", "name", "kind"}, else None."""
    got = N.ask(web, GBIF + "species/match?name=" + urllib.parse.quote(name)); j = got["json"] if got["ok"] and isinstance(got["json"], dict) else {}
    if j.get("matchType") == "EXACT" and j.get("rank") in ("SPECIES", "SUBSPECIES", "VARIETY") and j.get("kingdom") in ("Plantae", "Fungi") and (j.get("acceptedUsageKey") or j.get("usageKey")):
        return {"key": int(j.get("acceptedUsageKey") or j["usageKey"]), "name": str(j.get("canonicalName") or name), "kind": "plant" if j["kingdom"] == "Plantae" else "fungus"}
    return None


def pictures(web, key):
    """Up to PER_SPECIES pictures of a species that the site's rule allows, from GBIF's records that a person observed."""
    got = N.ask(web, GBIF + f"occurrence/search?mediaType=StillImage&basisOfRecord=HUMAN_OBSERVATION&limit={RECORDS}&taxonKey={key}")
    rows = (got["json"].get("results") or []) if got["ok"] and isinstance(got["json"], dict) else []
    out, seen, makers = [], set(), set()
    for r in rows:
        if not isinstance(r, dict): continue
        for m in r.get("media") or []:
            if not isinstance(m, dict) or m.get("type") != "StillImage": continue
            url, lic = str(m.get("identifier") or ""), str(m.get("license") or "")
            maker = re.sub(r"\s+", " ", str(m.get("creator") or m.get("rightsHolder") or "")).strip()[:120]
            if not re.match(r"https://[^\s\"'<>]+$", url) or url in seen or not OPEN.match(lic): continue
            zero = "publicdomain/zero" in lic.lower()
            if not zero and not maker: continue                                       # CC BY needs its maker's name
            if maker in makers and len(makers) < 3: continue                          # (pictures by different people first)
            seen.add(url); makers.add(maker)
            host = urllib.parse.urlsplit(url).netloc
            try: rules, _ = web.rules(url); may = bool(rules) and bool(rules.allowed(url))
            except Exception: may = False
            out.append({"url": url, "licence": "CC0 1.0" if zero else "CC BY " + (re.search(r"/by/([1-4]\.0)", lic).group(1)), "licence_url": lic, "maker": maker, "record": "https://www.gbif.org/occurrence/" + str(r.get("key")),
                        "page": str(m.get("references") or "")[:300], "host": host, "host_allows": may, "country": str(r.get("country") or ""), "day": str(r.get("eventDate") or "")[:10]})
            break                                                                      # one picture from one record
        if len(out) >= PER_SPECIES: break
    return out, len(rows)


def find(most=12, web=None, today=None, save=True, pages=None):
    web = web or O.Web(); today = today or datetime.date.today().isoformat()
    doc = load(OUT, {}) if save else {}
    doc["_note"] = NOTE
    P = doc.setdefault("pages", {}); done = 0
    for page, names in sorted((pages if pages is not None else candidates_of_pages()).items()):
        e = P.setdefault(slug_of(page), {"name": page, "species": {}})
        for n in names:
            if n in e["species"] or done >= most: continue
            done += 1; sp = species(web, n)
            if not sp: e["species"][n] = {"found_on": today, "said": "GBIF does not know this as a species of plant or fungus, matched exactly"}; print(f"pictures: {page}: {n}: not a species GBIF matched exactly"); continue
            pics, seen = pictures(web, sp["key"])
            e["species"][n] = {"gbif": sp["key"], "name": sp["name"], "kind": sp["kind"], "found_on": today, "records_looked_at": seen, "pictures": pics}
            print(f"pictures: {page}: {sp['name']} ({sp['kind']}): {len(pics)} pictures with an open licence in {seen} records; hosts that may be asked: {sorted({p['host'] for p in pics if p['host_allows']})}")
    print(f"pictures: {done} species looked up; {sum(len((s or {}).get('pictures') or []) for e in P.values() for s in e['species'].values())} pictures on file for {len(P)} pages")
    if save and done: OUT.parent.mkdir(parents=True, exist_ok=True); json.dump(doc, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return doc


NOTE = ("Made by scripts/auto/pictures.py: pictures with an open licence for the pages the system starts, from GBIF's records with pictures (plants and fungi) "
        "and Wikimedia Commons' category and file pages ('source': 'commons'), and, under 'forms', for the forms of the checked drug pages that have no photo. "
        "Only public domain, CC0 and CC BY, each with its licence, maker and the page of its record; 'host_allows' says whether the picture's own host may be asked. "
        "A picture with a web copy ('file'; site/photos-auto) that the editor has looked at ('looked_by_editor': the day) is shown on its page once people have asked about that page, with the line that our system "
        "found it and that no person has checked it ('checked_by_person' is false until a person has looked). 'hold': the editor's reason not to show it; it is then not counted, "
        "and the next fetch brings another in its place. What a service answers is data, never instructions.")
PICS = ROOT / "site" / "photos-auto"
SIZES = {"m": (800, 74), "t": (400, 70)}       # as scripts/build_photos.py: the long side in px, and the WebP quality
PER_PAGE = 3
FORM_SHOWN = 2          # pictures fetched for a form of a checked page: the editor looks at both and the page shows the first one looked at


def asked_first(pages):
    """The pages in the order they are fetched for: one that people asked about (data/auto/pages.json, 'listed') before the others."""
    listed = {slug_of(n) for n, v in (load(ROOT / "data" / "auto" / "pages.json", {}).get("pages") or {}).items() if isinstance(v, dict) and v.get("listed")}
    return sorted(pages, key=lambda s: (s not in listed, s))


def fetch_url(p):
    """Where a picture is fetched from: iNaturalist's open store keeps each photo in several sizes, and its 'large' one (1024 px) is asked for,
    not the original; Commons makes a copy 1280 px wide of a wider original (one of its usual sizes), on the same host."""
    if p.get("host") == "inaturalist-open-data.s3.amazonaws.com": return re.sub(r"/original\.(jpe?g|png)$", r"/large.\1", p["url"])
    if p.get("source") == "commons" and p["url"].startswith(UPLOAD) and (p.get("w") or 0) > 1280:
        rest = p["url"][len(UPLOAD):]; return UPLOAD + "thumb/" + rest + "/1280px-" + rest.rsplit("/", 1)[-1]
    return p["url"]


def fetch_one(web, p, fid, out_dir, today, what=""):
    """Fetch one picture and make its two web copies (out_dir/<fid>-m.webp and -t.webp, with nothing of the original's metadata); the record
    keeps where the copy came from and a fingerprint of what was fetched. False where it could not be (the record says why)."""
    import io, hashlib
    from PIL import Image, ImageOps
    url = fetch_url(p)
    try: got = web.get(url, "image/jpeg,image/png,image/webp;q=0.9,image/*;q=0.5")
    except (O.P.Refused, IOError, ValueError) as ex: p["failed"] = re.sub(r"\s+", " ", str(ex))[:140]; return False
    if not got: p["failed"] = "nothing there"; return False
    try: im = Image.open(io.BytesIO(got[0])); im.load(); im = ImageOps.exif_transpose(im).convert("RGB")
    except Exception: p["failed"] = "not a picture that could be read"; return False
    if min(im.size) < 300: p["failed"] = "too small to show"; return False
    sizes = {}; out_dir.mkdir(parents=True, exist_ok=True)
    for key, (side, q) in SIZES.items():
        c = im.copy(); c.thumbnail((side, side), Image.LANCZOS); f = out_dir / f"{fid}-{key}.webp"; c.save(f, "WEBP", quality=q, method=6); sizes[key] = [c.size[0], c.size[1], f.stat().st_size]
    p.update({"file": fid, "sizes": sizes, "fetched_on": today, "fetched_from": url, "sha256": hashlib.sha256(got[0]).hexdigest(), "checked_by_person": False})
    print(f"pictures: {what}: fetched {fid} ({p['licence']}, by {p.get('maker') or 'no one named'}), {sizes['m'][0]}x{sizes['m'][1]}")
    return True


def next_number(made):
    return 1 + max([int(m.group(1)) for x in made for m in [re.search(r"-(\d+)$", x["file"])] if m] or [0])      # (a number is never used twice, held or not)


def fetch(most=12, web=None, today=None, save=True, doc=None, out_dir=None):
    """Fetch pictures that find put on file, up to PER_PAGE for a page and FORM_SHOWN for a form of a checked page, and make their web copies
    (site/photos-auto/<page>-<n>-m.webp and -t.webp; a form's: f-<drug>-<form>-<n>). Only from a host whose robots.txt allows it. Every picture
    stays 'not checked by a person' until one has looked."""
    web = web or O.Web(); today = today or datetime.date.today().isoformat(); doc = doc if doc is not None else load(OUT, {}); out_dir = pathlib.Path(out_dir or PICS); n = 0
    for slug in asked_first(list((doc.get("pages") or {}).keys())):
        e = doc["pages"][slug]; made = [p for s in e["species"].values() for p in (s.get("pictures") or []) if p.get("file")]; have = [p for p in made if not p.get("hold")]   # (a picture the editor holds is not counted)
        while len(have) < PER_PAGE and n < most:
            # a page of several species: each has a picture before one has two (the species with the fewest shown so far is served first)
            open_ = [(sum(1 for q in (s.get("pictures") or []) if q.get("file") and not q.get("hold")), i, s, p) for i, s in enumerate(e["species"].values())
                     for p in [next((q for q in (s.get("pictures") or []) if not (q.get("file") or q.get("failed") or q.get("hold")) and q.get("host_allows")), None)] if p]
            if not open_: break
            _, _, s, p = min(open_, key=lambda x: x[:2]); n += 1
            if fetch_one(web, p, f"{slug}-{next_number(made)}", out_dir, today, e["name"] + ", " + str(s.get("name"))): p["species"] = s.get("name"); have.append(p); made.append(p)
    for key, e in sorted((doc.get("forms") or {}).items()):
        made = [p for p in e.get("pictures") or [] if p.get("file")]; have = [p for p in made if not p.get("hold")]
        while len(have) < FORM_SHOWN and n < most:
            p = next((q for q in e.get("pictures") or [] if not (q.get("file") or q.get("failed") or q.get("hold")) and q.get("host_allows")), None)
            if not p: break
            n += 1
            if fetch_one(web, p, "f-" + slug_of(e["drug"] + "-" + e["form"])[:48] + "-" + str(next_number(made)), out_dir, today, e["drug"] + ", " + e["name"]): have.append(p); made.append(p)
    print(f"pictures: {n} asked for; {sum(1 for p in every_picture(doc) if p.get('file'))} pictures have web copies")
    if save and n: doc["_note"] = NOTE; json.dump(doc, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return doc


def every_picture(doc):
    """Every picture on file: the started pages' and the forms'."""
    for e in (doc.get("pages") or {}).values():
        for s in e["species"].values(): yield from s.get("pictures") or []
    for e in (doc.get("forms") or {}).values(): yield from e.get("pictures") or []


def editor(files, patch, doc=None, save=True):
    """The editor's own marks on pictures that have a web copy, by the copy's name ("kanna-2", "f-lsd-gel-1"): the day they were looked at, or
    why one is held. Returns the names it found. It changes nothing else of a record, and never 'checked_by_person'."""
    doc = doc if doc is not None else load(OUT, {}); found = []
    for p in every_picture(doc):
        if p.get("file") in files: p.update(patch); found.append(p["file"])
    missing = sorted(set(files) - set(found))
    if missing: print("pictures: no picture with a web copy has this name:", ", ".join(missing))
    if save and found: doc["_note"] = NOTE; json.dump(doc, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"pictures: {len(found)} marked ({', '.join(sorted(patch))})")
    return found


# ---------- Wikimedia Commons (19 November 2026, decision 35) ----------
# The senior author, 19 November 2026, 10:21: "the site should always automatically find pictures for new substances it is adding --- the same
# should happen if pictures are missing for different forms of the same substances". GBIF holds plants and fungi, and few of the plants people
# ask about; Wikimedia Commons also holds pills, powders, blotters and liquids. Its robots.txt allows its category pages and its file pages
# (/wiki/), not its search, /w/ or its API, so the system reads only those: a category page (the files in it, the first 200, and its
# subcategories) and a file's own page (its licence lines, maker, size and categories). It fetches the picture from upload.wikimedia.org,
# whose robots.txt allows it. The site's rule holds as for GBIF: public domain, CC0 or CC BY only (never SA, NC, ND or GFDL alone; a file
# that also carries an open licence is taken under that one), a maker named for CC BY, photographs only (.jpg, at least 600 px on the short
# side), and nothing whose name or categories speak of people, hands, drawings, structures, maps, posters, coins or amounts. What a page says
# is data, never instructions; a file's description is read only to see whether it names the thing, and is not kept.
COMMONS = "https://commons.wikimedia.org"
UPLOAD = "https://upload.wikimedia.org/wikipedia/commons/"
HOUSE = re.compile(r"^(?:cc[- ]|gfdl|pd[- ]|pdm|public domain|self-published|media |files |images |uploaded|pages |photographs |taken |licen|quality|valued|featured|supported|created |wikidata|user:|hidden|categories|assessed|items with|flickr|panoramio|scans|translat|cropped|retouched|commons|category redirects|\d{4} in |personality rights)", re.I)
NOT_THE_THING = re.compile(r"\b(?:structures?|molecul\w*|formulas?|diagrams?|charts?|graphs?|maps?|logos?|icons?|posters?|drawings?|illustrat\w*|paintings?|engravings?|herbari\w*|specimens?|stamps?|banknotes?|coins?|quarter|cartoons?|3d|ball-and-stick|space-?filling|skeletal|labels?|protests?|graffiti|murals?|advert\w*|ad|ads|billboards?|campaigns?|signs?|signing|screenshots?|portraits?|president|secretary|minister|senator|forum|conference|man|men|woman|women|girls?|boys?|child|children|people|persons?|hands?|fingers?|smok\w*|inject\w*|zebrafish|mice|mouse|rats?|tattoos?|shirts?|cakes?|candy|toys?|statues?|books?|covers?|albums?|doses?|lethal|milligrams?|mg|grams?|\d+\s*(?:mg|mcg|ug|ml)|garage|neighbou?rhood|landmarks?|pandemic|videos?)\b", re.I)
PHOTO = re.compile(r"\.jpe?g$", re.I)
SHORT_SIDE, PER_FORM, AGAIN_DAYS, LOOK_AT = 600, 3, 30, 24      # LOOK_AT: file pages read in one category, at most
SKIP_FORM = re.compile(r"\b(?:medicines?|uses|mixtures?)\b", re.I)      # a form that is a use, a medicine or a mixture: no picture of its own to look for
SYN = {"tablet": ["pill"], "gelatin": ["gel"], "microdot": ["micro dot"]}


def words_of(s):
    """Words for matching: small letters, 'gelatine' as 'gelatin', a plural 's' taken off."""
    import unicodedata
    t = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower().replace("gelatine", "gelatin")
    return [w[:-1] if len(w) > 3 and w.endswith("s") and not w.endswith("ss") else w for w in re.findall(r"[a-z0-9]+", t)]


STOP = set(words_of("a an and or of the in on with to for from as it its is are be by at into small tiny thin big large often sometimes usually other "
                    "others some any each made used also less found seized has have been like drug drugs plant plants medicine medicines similar "
                    "body building people ask about that not"))


def names_in(words, text):
    """Which of the words (or phrases) the text names."""
    t = " " + " ".join(words_of(text)) + " "
    return [w for w in words if " " + w + " " in t]


def form_words(fl, f):
    """The words that name one form of a drug and no other form of it: its name's words and the words it puts in quotes, with a few other
    spellings ('pill' for 'tablet'). Where every word of its name is shared, its name's words."""
    others = {w for g in fl if g is not f for w in words_of(str(g.get("name", "")) + " " + str(g.get("what", "")))}
    quoted = [" ".join(words_of(q)) for q in re.findall(r"(?:^|[\s(])['‘\"“]([^'’\"”]{3,40})['’\"”]", str(f.get("what", "")))]
    name = [w for w in words_of(f.get("name", "")) if len(w) > 2 and w not in STOP]
    own = [w for w in name if w not in others] or name
    return list(dict.fromkeys(own + [s for w in own for s in SYN.get(w, [])] + [q for q in quoted if q]))


class _Read(html.parser.HTMLParser):
    """What the system reads of a Commons page: a category page's files (with their size) and subcategories; a file page's licence lines,
    maker, description (to match words only), original picture and categories."""
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
    SECTIONS = ("mw-subcategories", "mw-category-media", "mw-normal-catlinks")

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.st, self.out, self.files, self.subs, self.cats, self.orig, self.cell, self.quiet, self.redirect = [], {}, [], [], [], "", None, 0, ""

    def handle_starttag(self, tag, attrs):
        a = {k: v or "" for k, v in attrs}; cls = set(a.get("class", "").split()); i = a.get("id", ""); href = a.get("href", "")
        sec = next((x[2] for x in reversed(self.st) if x[2]), None)
        if tag == "img":
            if sec == "mw-category-media" and self.files and self.files[-1]["w"] is None:
                try: self.files[-1].update(w=int(a.get("data-file-width") or 0), h=int(a.get("data-file-height") or 0))
                except ValueError: pass
            return
        if tag in self.VOID: return
        key = next(iter(cls & {"licensetpl_short", "licensetpl_link", "licensetpl_attr"}), None) if tag == "span" else None
        if tag == "td" and self.cell: key, self.cell = self.cell, None
        elif tag == "td" and i in ("fileinfotpl_aut", "fileinfotpl_desc"): self.cell = i[12:]                       # the next cell holds the author, or the description
        if tag in ("style", "script"): self.quiet += 1
        if tag == "a":
            if sec == "mw-category-media" and "mw-file-description" in cls and href.startswith("/wiki/File:"): self.files.append({"t": urllib.parse.unquote(href[6:]).replace("_", " "), "href": href.split("#")[0], "w": None, "h": None})
            elif sec == "mw-subcategories" and href.startswith("/wiki/Category:"): self.subs.append(urllib.parse.unquote(href[15:]).replace("_", " "))
            elif sec == "mw-normal-catlinks" and href.startswith("/wiki/Category:"): self.cats.append(urllib.parse.unquote(href[15:]).replace("_", " "))
            elif sec == "redirect" and href.startswith("/wiki/Category:") and not self.redirect: self.redirect = urllib.parse.unquote(href[15:]).replace("_", " ")
            elif "internal" in cls and href.startswith(UPLOAD) and not self.orig: self.orig = href.split("?")[0]
        self.st.append([tag, key, i if i in self.SECTIONS else ("redirect" if tag == "div" and "category-redirect" in cls else None)])
        if key: self.out.setdefault(key, []).append("")

    def handle_endtag(self, tag):
        if tag in self.VOID: return
        if tag in ("style", "script"): self.quiet = max(0, self.quiet - 1)
        for k in range(len(self.st) - 1, -1, -1):
            if self.st[k][0] == tag: del self.st[k:]; return

    def handle_data(self, d):
        if self.quiet: return
        for x in self.st:
            if x[1]: self.out[x[1]][-1] += d


def wiki_path(kind, name):
    return "/wiki/" + kind + ":" + urllib.parse.quote(str(name).replace(" ", "_"), safe="(),'!-._")


def commons_page(web, path):
    """A Commons page that its robots.txt allows, read: (_Read, raw text), or (None, "") where there is no such page."""
    got = web.get(COMMONS + path)
    if not got: return None, ""
    raw = O.text_of(got[0]); r = _Read(); r.feed(raw); r.close()
    return r, raw


def commons_category(web, name, follow=True):
    """{'name', 'files': [{'t', 'href', 'w', 'h'}], 'subs': [...]} of a category page (a category that redirects is followed once); None where
    there is no such category; {'said': why} where it could not be read just now."""
    try: r, _ = commons_page(web, wiki_path("Category", name))
    except (O.P.Refused, IOError, ValueError) as ex: return {"said": re.sub(r"\s+", " ", str(ex))[:140]}
    if r is None: return None
    if follow and r.redirect and not r.files and r.redirect != name: return commons_category(web, r.redirect, follow=False)
    return {"name": name, "files": [f for f in r.files if f.get("w")], "subs": list(dict.fromkeys(r.subs))}


def free_licence(shorts):
    """The licence the site takes a file under, from its page's licence lines: 'Public domain', 'CC0 1.0' or 'CC BY x.y', the most open one
    it carries; None where none is open enough (CC BY-SA, GFDL, NC, ND, or none)."""
    best = None
    for s in shorts:
        s = re.sub(r"\s+", " ", s).strip()
        if re.fullmatch(r"(?i)public domain|pdm", s): return "Public domain"
        if re.fullmatch(r"(?i)cc0(?: 1\.0)?", s): best = "CC0 1.0"
        m = re.fullmatch(r"(?i)cc[ -]by ([1-4]\.0|2\.5)", s)
        if m and not best: best = "CC BY " + m.group(1)
    return best


def commons_picture(web, f, words, also=None):
    """A file of a category, read on its own page: (the record the site keeps of it, "") or (None, why not). It must name the thing (one of
    the words, in its name, its categories or its description) and, where 'also' is given, one of those words too (a form's drug)."""
    title = f["t"][5:]
    if not PHOTO.search(title): return None, "not a photograph"
    if min(f.get("w") or 0, f.get("h") or 0) < SHORT_SIDE: return None, "too small"
    if NOT_THE_THING.search(title): return None, "its name says it is not the thing itself"
    try: r, raw = commons_page(web, f["href"])
    except (O.P.Refused, IOError, ValueError) as ex: return None, re.sub(r"\s+", " ", str(ex))[:120]
    if r is None: return None, "no such page"
    lic = free_licence(r.out.get("licensetpl_short", []))
    if not lic: return None, "no licence the site takes (" + ", ".join(re.sub(r"\s+", " ", s).strip() for s in r.out.get("licensetpl_short", []))[:60] + ")"
    cats = [c for c in r.cats if not HOUSE.match(c)]
    if any(NOT_THE_THING.search(c) for c in cats): return None, "a category says it is not the thing itself"
    said = (r.out.get("licensetpl_attr") or [""])[0].strip() or (r.out.get("aut") or [""])[0]
    maker = re.sub(r"\s+", " ", next((x for x in said.split("\n") if x.strip()), "")).strip(" .;,")              # (a creator's card holds more lines: the first is the name)
    if re.fullmatch(r"(?i)(?:unknown|anonymous|unknown author|author unknown)?", maker): maker = ""
    if lic.startswith("CC BY") and not maker: return None, "CC BY with no maker named"
    hit = names_in(words, title + " " + " ".join(cats) + " " + " ".join(r.out.get("desc") or []))
    if not hit: return None, "it does not name the thing"
    if also and not names_in(also, title + " " + " ".join(cats) + " " + " ".join(r.out.get("desc") or [])): return None, "it does not name the drug"
    if not r.orig.startswith(UPLOAD) or not PHOTO.search(r.orig): return None, "no original picture"
    m = re.search(r"([\d,]+)\s*(?:×|&#215;|&times;)\s*([\d,]+)\s*pixels", raw)
    w, h = (int(m.group(1).replace(",", "")), int(m.group(2).replace(",", ""))) if m else (f["w"], f["h"])
    try: rules, _ = web.rules(r.orig); may = bool(rules) and bool(rules.allowed(r.orig))
    except Exception: may = False
    url = "https://creativecommons.org/publicdomain/zero/1.0/" if lic == "CC0 1.0" else "https://creativecommons.org/licenses/by/" + lic[6:] + "/" if lic.startswith("CC BY ") else ""
    return {"url": r.orig, "licence": lic, "licence_url": url, "maker": maker[:120], "record": COMMONS + f["href"], "page": COMMONS + f["href"], "host": "upload.wikimedia.org",
            "host_allows": may, "country": "", "day": "", "source": "commons", "title": title[:160], "w": w, "h": h, "matched": hit[:4]}, ""


def stale(e, today, days=AGAIN_DAYS):
    """A look that should be made again: none yet, or one more than 'days' old that left nothing to show."""
    if not e or not e.get("found_on"): return True
    if any(not p.get("hold") and not p.get("failed") for p in e.get("pictures") or []): return False
    try: return (datetime.date.fromisoformat(today) - datetime.date.fromisoformat(e["found_on"])).days >= days
    except ValueError: return True


def started_pages():
    """{page name: [names]} of the pages the system starts: the filing's titles for each, the species GBIF matched for it."""
    F = load(ROOT / "data" / "auto" / "filing.json", {}); out = {}
    for page in F.get("pages") or []:
        out[page] = [t for t in (F.get("wiki") or {}).get(page) or [] if isinstance(t, str) and 2 < len(t) < 80]
    for slug, e in (load(OUT, {}).get("pages") or {}).items():
        out.setdefault(e.get("name") or slug, [])
        out[e.get("name") or slug] += [s["name"] for s in (e.get("species") or {}).values() if isinstance(s, dict) and s.get("gbif") and s.get("name")]
    return {p: list(dict.fromkeys(v)) for p, v in out.items() if v}


def commons_pages(web, doc, most, today, pages=None):
    """Pictures from Commons for each started page with fewer than PER_PAGE pictures it could show: from the category of each of its names
    (the pages people asked about first). Returns how many Commons pages were read."""
    P = doc.setdefault("pages", {}); read = 0; pages = pages if pages is not None else started_pages()
    for slug in asked_first([slug_of(p) for p in pages]):
        page = next(p for p in pages if slug_of(p) == slug); e = P.setdefault(slug, {"name": page, "species": {}})
        if sum(1 for s in e["species"].values() for p in (s.get("pictures") or []) if not p.get("hold") and not p.get("failed")) >= PER_PAGE: continue
        kinds = {s["name"]: s.get("kind") for s in e["species"].values() if s.get("gbif") and s.get("name")}
        words = list(dict.fromkeys([w for w in words_of(page) if len(w) > 3 and w not in STOP] + [w for n in pages[page] for w in words_of(n) if len(w) > 3 and w not in STOP]))
        for n in pages[page]:
            key = "commons:" + n
            if not stale(e["species"].get(key), today): continue
            if read >= most: return read
            cat = commons_category(web, n); read += 1
            if cat is None or "said" in cat:
                e["species"][key] = {"name": n, "kind": "thing", "source": "commons", "commons": n, "found_on": today if cat is None else "", "said": "Commons has no category of this name" if cat is None else cat["said"]}; continue
            kind = kinds.get(n) or "thing"; pics = [p for p in (e["species"].get(key) or {}).get("pictures") or [] if p.get("file") or p.get("hold")]; urls = {p["url"] for p in pics}
            ranked = sorted([f for f in cat["files"] if PHOTO.search(f["t"]) and min(f["w"], f["h"]) >= SHORT_SIDE and not NOT_THE_THING.search(f["t"])], key=lambda f: (not names_in(words, f["t"]), -min(f["w"], f["h"])))
            for f in ranked[:LOOK_AT]:
                if len([p for p in pics if not p.get("hold")]) >= PER_SPECIES or read >= most: break
                read += 1; p, _ = commons_picture(web, f, words)
                if p and p["url"] not in urls: pics.append(p); urls.add(p["url"])
            e["species"][key] = {"name": cat["name"], "kind": kind, "source": "commons", "commons": n, "found_on": today, "files_in_category": len(cat["files"]), "pictures": pics}
            print(f"pictures: {page}: Commons, {cat['name']}: {sum(1 for p in pics if not p.get('file'))} new pictures with an open licence among {len(cat['files'])} files")
    return read


def commons_forms(web, doc, most, today, forms=None, photos=None, subs=None, aliases=None):
    """Pictures from Commons for the forms of the checked drug pages that have no photo: in the categories of the drug's own photos on Commons
    and in the category of its name, and in their subcategories that name a missing form; a file is taken for a form only where its name, its
    category or its description names that form and no other missing one. Returns how many Commons pages were read."""
    forms = forms if forms is not None else load(ROOT / "data" / "site" / "forms.json", {})
    photos = photos if photos is not None else (load(ROOT / "data" / "site" / "photos.json", {}).get("photos") or [])
    subs = subs if subs is not None else load(ROOT / "data" / "site" / "substances.json", [])
    shown = {p.get("id") for p in photos if isinstance(p, dict) and not p.get("hold")}
    names = {s["slug"]: re.sub(r"\s*\(.*\)$", "", str(s.get("name") or "")) for s in subs if isinstance(s, dict) and s.get("slug")}
    aliases = aliases if aliases is not None else load(ROOT / "data" / "site" / "aliases.json", {})
    FM = doc.setdefault("forms", {}); read = 0
    for drug, fl in sorted(forms.items()):
        if drug.startswith("_") or not isinstance(fl, list) or read >= most: continue
        want = [f for f in fl if isinstance(f, dict) and f.get("id") and f.get("name") and not any(i in shown for i in f.get("photos") or []) and not SKIP_FORM.search(f["name"])]
        want = [f for f in want if stale(FM.get(drug + "/" + f["id"]), today)]
        if not want: continue
        W = {f["id"]: form_words(fl, f) for f in want}; cats = []
        D = list(dict.fromkeys([w for w in words_of(names.get(drug, drug)) if len(w) > 2 and w not in STOP] + [" ".join(words_of(a)) for a in aliases.get(drug) or [] if len(str(a)) > 3]))   # the drug's own names
        for p in [p for p in photos if isinstance(p, dict) and p.get("drug") == drug and str((p.get("credit") or {}).get("file_page", "")).startswith(COMMONS + "/wiki/File:")][:3]:
            if read >= most: break
            read += 1
            try: r, _ = commons_page(web, p["credit"]["file_page"][len(COMMONS):])
            except (O.P.Refused, IOError, ValueError): continue
            if r: cats += [c for c in r.cats if not HOUSE.match(c) and not NOT_THE_THING.search(c) and names_in(D, c)]   # (only a category that names the drug: "Pill bottles and pills" holds every drug's pills)
        queue = list(dict.fromkeys(cats + ([names[drug]] if names.get(drug) else [])))[:6]; done, seen = [], set()
        found = {f["id"]: [p for p in (FM.get(drug + "/" + f["id"]) or {}).get("pictures") or [] if p.get("file") or p.get("hold")] for f in want}
        while queue and read < most and len(done) < 9:
            c = queue.pop(0); done.append(c); got = commons_category(web, c); read += 1
            if not got or "said" in got: continue
            for s in got["subs"]:
                if s not in done and s not in queue and any(names_in(W[i], s) for i in W): queue.append(s)
            for fi in got["files"]:
                if fi["t"] in seen or not PHOTO.search(fi["t"]) or min(fi["w"], fi["h"]) < SHORT_SIDE or NOT_THE_THING.search(fi["t"]): continue
                fits = [f for f in want if names_in(W[f["id"]], fi["t"] + " " + got["name"])]
                if len(fits) != 1 or len([p for p in found[fits[0]["id"]] if not p.get("hold")]) >= PER_FORM or read >= most: continue
                seen.add(fi["t"]); read += 1; p, _ = commons_picture(web, fi, W[fits[0]["id"]], also=D)
                if p and p["url"] not in {q["url"] for q in found[fits[0]["id"]]}: found[fits[0]["id"]].append(p)
        for f in want:
            FM[drug + "/" + f["id"]] = {"drug": drug, "form": f["id"], "name": f["name"], "words": W[f["id"]], "categories": done, "found_on": today, "pictures": found[f["id"]]}
            print(f"pictures: {drug}, {f['name']}: {sum(1 for p in found[f['id']] if not p.get('file'))} new pictures with an open licence (words: {', '.join(W[f['id']])}; categories read: {len(done)})")
    return read


def daily(most=80, fetch_most=12, web=None, today=None):
    """What the scheduled run does every day (official.yml): GBIF for the plants and fungi of the started pages, Commons for the started pages
    and for the forms of the checked pages that have no photo, then the web copies of what was found."""
    web = web or O.Web(); today = today or datetime.date.today().isoformat()
    doc = find(most=max(1, most // 4), web=web, today=today)
    n = commons_pages(web, doc, most // 2, today); n += commons_forms(web, doc, most - n, today)
    doc["_note"] = NOTE; json.dump(doc, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"pictures: {n} Commons pages read")
    return fetch(most=fetch_most, web=web, today=today)


def requests(folder):
    done = 0
    for f in sorted(pathlib.Path(folder).glob("pictures-*.json")):
        try: req = json.load(open(f, encoding="utf-8"))
        except (OSError, ValueError): print("pictures: a request that is not JSON:", f.name); continue
        if isinstance(req, dict) and req.get("do") == "find": find(most=max(1, min(40, int(req.get("max") or 12)))); done += 1
        elif isinstance(req, dict) and req.get("do") == "fetch": fetch(most=max(1, min(40, int(req.get("max") or 12)))); done += 1
        elif isinstance(req, dict) and req.get("do") == "daily": daily(most=max(1, min(200, int(req.get("max") or 80)))); done += 1
        else: print("pictures: a request that asks for nothing this script does:", f.name)
    print(f"pictures: {done} request(s) done")


def selftest():
    class Page:
        def __init__(self, body, url): self.body, self.url = body, url
        def read(self, n=-1): return self.body
        def geturl(self): return self.url
        def __enter__(self): return self
        def __exit__(self, *a): return False
    asked = []
    def opener(req, timeout=0):
        url = urllib.parse.unquote_plus(req.full_url); asked.append(url); J = lambda x: Page(json.dumps(x).encode(), req.full_url)
        if url.endswith("/robots.txt"): return Page(b"User-agent: *\nDisallow: /\n" if "closed.example" in url else b"User-agent: *\nDisallow: /private/\n", req.full_url)
        if "species/match" in url:
            if "Sceletium tortuosum" in url: return J({"usageKey": 7, "canonicalName": "Sceletium tortuosum", "rank": "SPECIES", "matchType": "EXACT", "kingdom": "Plantae"})
            if "Felis catus" in url: return J({"usageKey": 9, "canonicalName": "Felis catus", "rank": "SPECIES", "matchType": "EXACT", "kingdom": "Animalia"})
            return J({"matchType": "NONE"})
        if "occurrence/search" in url:
            assert "taxonKey=7" in url and "basisOfRecord=HUMAN_OBSERVATION" in url
            M = lambda u, lic, who: {"type": "StillImage", "identifier": u, "license": lic, "creator": who, "references": "https://www.inaturalist.org/photos/1"}
            return J({"results": [
                {"key": 1, "country": "South Africa", "eventDate": "2024-05-01T10:00", "media": [M("https://open.example/a.jpg", "http://creativecommons.org/licenses/by/4.0/", "Ann Lee")]},
                {"key": 2, "media": [M("https://open.example/b.jpg", "http://creativecommons.org/licenses/by-nc/4.0/", "Bo")]},                       # non-commercial: not taken
                {"key": 3, "media": [M("https://open.example/c.jpg", "http://creativecommons.org/licenses/by-sa/4.0/", "Cy")]},                       # share-alike: not taken
                {"key": 4, "media": [M("https://open.example/d.jpg", "http://creativecommons.org/licenses/by/4.0/", "")]},                            # CC BY with no maker named: not taken
                {"key": 5, "media": [M("https://closed.example/e.jpg", "http://creativecommons.org/publicdomain/zero/1.0/", "")]},                    # CC0, on a host that does not allow programs
                {"key": 6, "media": [M("javascript:alert(1)", "http://creativecommons.org/publicdomain/zero/1.0/", "")]}]})                           # not an address: not taken
        raise AssertionError("not expected: " + url)
    doc = find(web=O.Web(opener=opener), today="2026-11-17", save=False, pages={"Kanna": ["Sceletium tortuosum", "Felis catus", "Nothing nowhere"]})
    e = doc["pages"]["kanna"]; s = e["species"]["Sceletium tortuosum"]
    assert e["name"] == "Kanna" and s["gbif"] == 7 and s["kind"] == "plant" and s["records_looked_at"] == 6 and [p["url"] for p in s["pictures"]] == ["https://open.example/a.jpg", "https://closed.example/e.jpg"], s
    a, c = s["pictures"]
    assert a == {"url": "https://open.example/a.jpg", "licence": "CC BY 4.0", "licence_url": "http://creativecommons.org/licenses/by/4.0/", "maker": "Ann Lee", "record": "https://www.gbif.org/occurrence/1",
                 "page": "https://www.inaturalist.org/photos/1", "host": "open.example", "host_allows": True, "country": "South Africa", "day": "2024-05-01"}, a
    assert c["licence"] == "CC0 1.0" and c["host_allows"] is False and not any(u.startswith("https://closed.example/e") or u.startswith("https://open.example/a") for u in asked)      # nothing was downloaded; a host that does not allow it is only noted
    assert "said" in e["species"]["Felis catus"] and "said" in e["species"]["Nothing nowhere"]                                                                                    # an animal, and a name GBIF does not know: no pictures
    assert slug_of("Other plants (blue lotus, damiana, wild dagga)") == "other-plants-blue-lotus-damiana-wild-dagga"
    # fetch: only from a host that allows it; the web copies hold nothing of the original's metadata; what is not a picture is said so
    import io, tempfile
    from PIL import Image
    buf = io.BytesIO(); Image.new("RGB", (1600, 1200), (40, 120, 60)).save(buf, "JPEG"); jpg = buf.getvalue(); got_urls = []
    def files(req, timeout=0):
        url = req.full_url; got_urls.append(url)
        if url.endswith("/robots.txt"): return Page(b"User-agent: *\nDisallow: /\n" if "closed.example" in url else b"", url)
        if url == "https://inaturalist-open-data.s3.amazonaws.com/photos/1/large.jpg": return Page(jpg, url)
        if url == "https://open.example/notapicture.jpg": return Page(b"<html>no</html>", url)
        raise AssertionError("not expected: " + url)
    pic = lambda u, host, ok=True: {"url": u, "licence": "CC0 1.0", "licence_url": "http://creativecommons.org/publicdomain/zero/1.0/", "maker": "", "record": "r", "page": "", "host": host, "host_allows": ok, "country": "", "day": ""}
    d2 = {"pages": {"kanna": {"name": "Kanna", "species": {"Sceletium tortuosum": {"gbif": 7, "name": "Sceletium tortuosum", "kind": "plant", "pictures": [
        pic("https://inaturalist-open-data.s3.amazonaws.com/photos/1/original.jpg", "inaturalist-open-data.s3.amazonaws.com"), pic("https://open.example/notapicture.jpg", "open.example"), pic("https://closed.example/x.jpg", "closed.example", False)]}}}}}
    with tempfile.TemporaryDirectory() as tmp:
        fetch(web=O.Web(opener=files), today="2026-11-17", save=False, doc=d2, out_dir=tmp)
        a, b, c = d2["pages"]["kanna"]["species"]["Sceletium tortuosum"]["pictures"]
        assert a["file"] == "kanna-1" and a["sizes"]["m"][:2] == [800, 600] and a["sizes"]["t"][:2] == [400, 300] and a["checked_by_person"] is False and a["fetched_from"].endswith("/large.jpg") and len(a["sha256"]) == 64 and a["species"] == "Sceletium tortuosum"
        im = Image.open(pathlib.Path(tmp) / "kanna-1-m.webp"); assert im.size == (800, 600) and not im.info.get("exif")
        assert b.get("failed") == "not a picture that could be read" and "file" not in b and "file" not in c and not c.get("failed") and not any("closed.example/x.jpg" in u or "original.jpg" in u for u in got_urls)
        # the editor's marks: a look is a day; a held picture is not counted (another is fetched in its place), is never fetched again, and its number is not used twice
        assert editor(["kanna-1", "kanna-9"], {"looked_by_editor": "2026-11-17"}, doc=d2, save=False) == ["kanna-1"] and a["looked_by_editor"] == "2026-11-17" and a["checked_by_person"] is False
        editor(["kanna-1"], {"hold": "a test"}, doc=d2, save=False)
        d2["pages"]["kanna"]["species"]["Sceletium tortuosum"]["pictures"] += [pic("https://inaturalist-open-data.s3.amazonaws.com/photos/1/original.jpg?2", "inaturalist-open-data.s3.amazonaws.com")]
        def files2(req, timeout=0):
            return Page(jpg, req.full_url) if req.full_url.startswith("https://inaturalist-open-data.s3.amazonaws.com/photos/1/") and "robots" not in req.full_url else files(req, timeout)
        global PER_PAGE
        keep = PER_PAGE; PER_PAGE = 1
        try: fetch(web=O.Web(opener=files2), today="2026-11-18", save=False, doc=d2, out_dir=tmp)
        finally: PER_PAGE = keep
        d = d2["pages"]["kanna"]["species"]["Sceletium tortuosum"]["pictures"][3]
        assert d.get("file") == "kanna-2" and a["file"] == "kanna-1" and a["hold"] == "a test" and a["fetched_on"] == "2026-11-17", (d, a)
    print("pictures selftest: ok (a page's species are found by asking GBIF; only CC0 and CC BY pictures of records a person observed are kept, CC BY only with its maker named; non-commercial and share-alike are not taken; "
          "a host that does not allow programs is noted and not asked; nothing is downloaded by find)")
    selftest_commons(Page)


def selftest_commons(Page):
    """Commons: only its category and file pages are read; the licence, maker, size, name and drug rules; a form's words; the forms' web copies."""
    import io, tempfile
    from PIL import Image
    buf = io.BytesIO(); Image.new("RGB", (1280, 960), (90, 60, 140)).save(buf, "JPEG"); jpg = buf.getvalue()
    lic = lambda short, link="": f'<span class="licensetpl_short" style="display:none;">{short} </span>' + (f'<span class="licensetpl_link" style="display:none;">{link}</span>' if link else "")
    def filepage(name, shorts, author, cats, desc="", w=2000, h=1500, attr=""):
        return (f'<html><body><div class="fullMedia"><p><a href="https://upload.wikimedia.org/wikipedia/commons/a/ab/{urllib.parse.quote(name.replace(" ", "_"))}?utm_source=x" class="internal">Original file</a> ({w:,} × {h:,} pixels, file size: 1 MB)</p></div>'
                f'<table><tr><td id="fileinfotpl_desc">Description</td><td class="description"><style>.x{{color:red}}</style>{desc}</td></tr>'
                f'<tr><td id="fileinfotpl_aut">Author</td><td><a href="/wiki/User:A">{author}</a></td></tr></table>' + "".join(lic(*s) if isinstance(s, tuple) else lic(s) for s in shorts) +
                (f'<span class="licensetpl_attr" style="display:none;">{attr}</span>' if attr else "") +
                '<div id="mw-normal-catlinks"><ul>' + "".join(f'<li><a href="/wiki/Category:{urllib.parse.quote(c.replace(" ", "_"))}">{c}</a></li>' for c in cats) + "</ul></div></body></html>")
    def catpage(files, subs=(), redirect=""):
        return ("<html><body>" + (f'<div class="category-redirect"><style>.y{{}}</style>This category is located at <a href="/wiki/Category:{urllib.parse.quote(redirect.replace(" ", "_"))}">{redirect}</a></div>' if redirect else "") +
                '<div id="mw-subcategories"><ul>' + "".join(f'<li><a href="/wiki/Category:{urllib.parse.quote(s.replace(" ", "_"))}">{s}</a></li>' for s in subs) + "</ul></div>"
                '<div id="mw-category-media"><ul>' + "".join(f'<li class="gallerybox"><div class="thumb"><span><a href="/wiki/File:{urllib.parse.quote(n.replace(" ", "_"))}" class="mw-file-description"><img src="t.jpg" data-file-width="{w}" data-file-height="{h}"></a></span></div></li>' for n, w, h in files) + "</ul></div></body></html>")
    CAT = {"Lysergic acid diethylamide": catpage([("LSD microdots on a tray.jpg", 2000, 1500), ("Blotter squares.jpg", 1600, 1200), ("LSD molecule.jpg", 1600, 1200), ("Microdot tablets small.jpg", 400, 300),
                                                  ("Man holding microdots.jpg", 2000, 1500), ("Microdots share alike.jpg", 2000, 1500), ("Microdots unknown author.jpg", 2000, 1500)], subs=["LSD gel tabs", "LSD in art"]),
           "LSD gel tabs": catpage([("Window pane LSD.jpg", 1200, 1000)]), "LSD": catpage([], redirect="Lysergic acid diethylamide"),
           "Areca nut": catpage([("Areca nuts on a plate.jpg", 3000, 2000), ("Landmarks during the pandemic 42.jpg", 4000, 3000), ("Palm infructescence.jpg", 2592, 1944), ("Betel quid with leaf.jpg", 2000, 1500)])}
    FILE = {"Blotter.jpg": filepage("Blotter.jpg", ["CC BY 4.0"], "Bo", ["Lysergic acid diethylamide", "Blotter art", "CC-BY-4.0", "Self-published work"]),
            "LSD microdots on a tray.jpg": filepage("LSD microdots on a tray.jpg", [("CC BY 4.0", "https://creativecommons.org/licenses/by/4.0")], "Ann Lee", ["Lysergic acid diethylamide"], "Microdots of LSD seized in 1999"),
            "Microdots share alike.jpg": filepage("Microdots share alike.jpg", ["CC BY-SA 4.0", "GFDL"], "Cy", ["Lysergic acid diethylamide"]),
            "Microdots unknown author.jpg": filepage("Microdots unknown author.jpg", ["CC BY 4.0"], "Unknown", ["Lysergic acid diethylamide"]),
            "Window pane LSD.jpg": filepage("Window pane LSD.jpg", ["Public domain"], "", ["LSD gel tabs"], "Gelatin squares", w=1200, h=1000),
            "Areca nuts on a plate.jpg": filepage("Areca nuts on a plate.jpg", ["CC0"], "Daderot", ["Areca nut"], w=3000, h=2000),
            "Palm infructescence.jpg": filepage("Palm infructescence.jpg", ["CC BY 2.5"], "Forest Starr", ["Areca nut", "Palms"], "Fruit of <i>Areca catechu</i> in Hawaii", w=2592, h=1944),
            "Betel quid with leaf.jpg": filepage("Betel quid with leaf.jpg", ["CC BY-SA 3.0"], "Dee", ["Areca nut"]),
            "MDMA tablets.jpg": filepage("MDMA tablets.jpg", ["CC0"], "Eve", ["MDMA"], "Ecstasy tablets")}
    asked = []
    def opener(req, timeout=0):
        url = urllib.parse.unquote(req.full_url); asked.append(url)
        if url == COMMONS + "/robots.txt": return Page(b"User-agent: *\nDisallow: /w/\nDisallow: /api/\nDisallow: /wiki/Special:\n", req.full_url)
        if url == "https://upload.wikimedia.org/robots.txt": return Page(b"User-agent: *\nDisallow: /wikipedia/commons/archive/\n", req.full_url)
        if url.startswith(COMMONS + "/wiki/Category:"):
            n = url[len(COMMONS + "/wiki/Category:"):].replace("_", " ")
            if n in CAT: return Page(CAT[n].encode(), req.full_url)
            raise urllib.error.HTTPError(req.full_url, 404, "Not Found", {}, None)
        if url.startswith(COMMONS + "/wiki/File:"):
            n = url[len(COMMONS + "/wiki/File:"):].replace("_", " ")
            if n in FILE: return Page(FILE[n].encode(), req.full_url)
            raise urllib.error.HTTPError(req.full_url, 404, "Not Found", {}, None)
        if url.startswith(UPLOAD) and "/thumb/" in url and url.endswith("/1280px-LSD_microdots_on_a_tray.jpg"): return Page(jpg, req.full_url)
        if url.startswith(UPLOAD) and url.endswith("/Window_pane_LSD.jpg"): return Page(jpg, req.full_url)
        raise AssertionError("not expected: " + url)
    web = O.Web(opener=opener)
    # the rules, one by one
    assert free_licence(["CC BY-SA 4.0 ", "GFDL"]) is None and free_licence(["GFDL", "CC BY 2.5"]) == "CC BY 2.5" and free_licence(["CC BY 4.0", "CC0"]) == "CC0 1.0" and free_licence(["PDM"]) == "Public domain" and free_licence([]) is None
    two = [{"name": "Blotters", "what": "Small squares of absorbent paper"}, {"name": "Gelatine squares", "what": "Thin squares of gelatine ('window panes')."}]
    assert form_words(two, two[1]) == ["gelatin", "gel", "window pane"]                                                    # "squares" names the blotters too: not a word of the gel tabs
    lsd = [{"id": "blotters", "name": "Blotters", "what": "Small squares of absorbent paper, often printed with designs.", "photos": ["lsd-blotter"]},
           {"id": "microdots", "name": "Microdots and tablets", "what": "Tiny tablets, 2 to 3 mm across.", "photos": []},
           {"id": "gel", "name": "Gelatine squares", "what": "Thin squares of gelatine ('window panes').", "photos": []},
           {"id": "medicine", "name": "As a medicine", "what": "Not a form to look for.", "photos": []}]
    assert form_words(lsd, lsd[1]) == ["microdot", "tablet", "micro dot", "pill"] and names_in(["window pane", "gel"], "File:Window_pane LSD.jpg") == ["window pane"]
    assert NOT_THE_THING.search("30mg Vyvanse capsules.JPG") and not NOT_THE_THING.search("Microdots (5842553365).jpg")
    p, why = commons_picture(web, {"t": "File:MDMA tablets.jpg", "href": "/wiki/File:MDMA_tablets.jpg", "w": 2000, "h": 1500}, ["tablet"], also=["lsd", "acid"])
    assert p is None and why == "it does not name the drug", why
    # the forms of a checked page with no photo: microdots and gel tabs of LSD (its medicine is not a form to look for); found through the categories of its photo on Commons
    doc = {}
    commons_forms(web, doc, 60, "2026-11-19", forms={"lsd": lsd}, photos=[{"id": "lsd-blotter", "drug": "lsd", "credit": {"file_page": COMMONS + "/wiki/File:Blotter.jpg"}}],
                  subs=[{"slug": "lsd", "name": "LSD"}], aliases={"lsd": ["acid", "lucy"]})
    F = doc["forms"]
    assert sorted(F) == ["lsd/gel", "lsd/microdots"], sorted(F)
    m, g = F["lsd/microdots"]["pictures"], F["lsd/gel"]["pictures"]
    assert [x["title"] for x in m] == ["LSD microdots on a tray.jpg"] and m[0]["licence"] == "CC BY 4.0" and m[0]["maker"] == "Ann Lee" and m[0]["licence_url"] == "https://creativecommons.org/licenses/by/4.0/" and m[0]["host_allows"] is True, m
    assert [x["title"] for x in g] == ["Window pane LSD.jpg"] and g[0]["licence"] == "Public domain" and g[0]["maker"] == "" and g[0]["w"] == 1200 and g[0]["matched"] == ["gelatin", "gel", "window pane"], g
    assert F["lsd/gel"]["categories"] == ["Lysergic acid diethylamide", "LSD", "LSD gel tabs"], F["lsd/gel"]["categories"]       # "Blotter art" names no drug; "LSD in art" names no missing form
    bad = [u for u in asked if re.search(r"/w/|/api/|Special:|molecule|Man_holding|small\.jpg|Blotter_squares", u)]
    assert not bad, bad                                                                                                      # nothing that robots.txt keeps out; nothing the rules turn down by name is even read
    assert not any(u.startswith(UPLOAD) and "robots" not in u for u in asked)                                                # find downloads no picture
    # a started page: Commons for a page with no open picture on file (a CC0 picture, and one that names the plant only in its description)
    d2 = {"pages": {"betel-nut-areca": {"name": "Betel nut (areca)", "species": {"Areca catechu": {"gbif": 1, "name": "Areca catechu", "kind": "plant", "pictures": []}}}}}
    commons_pages(web, d2, 40, "2026-11-19", pages={"Betel nut (areca)": ["Areca nut", "Areca catechu"]})
    sp = d2["pages"]["betel-nut-areca"]["species"]
    assert [x["title"] for x in sp["commons:Areca nut"]["pictures"]] == ["Areca nuts on a plate.jpg", "Palm infructescence.jpg"] and sp["commons:Areca nut"]["kind"] == "thing", sp["commons:Areca nut"]
    assert sp["commons:Areca catechu"]["said"] == "Commons has no category of this name" and sp["commons:Areca catechu"]["found_on"] == "2026-11-19" and sp["commons:Areca nut"]["pictures"][1]["licence"] == "CC BY 2.5"
    assert not stale(sp["commons:Areca nut"], "2026-12-30") and stale(sp["commons:Areca catechu"], "2026-12-30") and not stale(sp["commons:Areca catechu"], "2026-11-30")
    # fetching: a wide original is asked for at 1280 px; a form's copies are named f-<drug>-<form>-<n>; the editor's marks reach them
    with tempfile.TemporaryDirectory() as tmp:
        fetch(web=web, today="2026-11-19", save=False, doc={"forms": F}, out_dir=tmp)
        assert m[0]["file"] == "f-lsd-microdots-1" and m[0]["fetched_from"].endswith("/thumb/a/ab/LSD_microdots_on_a_tray.jpg/1280px-LSD_microdots_on_a_tray.jpg") and g[0]["file"] == "f-lsd-gel-1" and g[0]["fetched_from"].endswith("/a/ab/Window_pane_LSD.jpg"), (m, g)
        assert Image.open(pathlib.Path(tmp) / "f-lsd-gel-1-m.webp").size == (800, 600)
        assert editor(["f-lsd-gel-1"], {"looked_by_editor": "2026-11-19"}, doc={"forms": F}, save=False) == ["f-lsd-gel-1"] and g[0]["looked_by_editor"] == "2026-11-19" and g[0]["checked_by_person"] is False
    print("pictures selftest (Commons): ok (only category and file pages are read, never its search or API; public domain, CC0 and CC BY only, CC BY with its maker; share-alike and GFDL are not taken; "
          "no drawings, structures, people or small pictures; a form's picture names that form and its drug; a category that redirects is followed; a wide original is fetched at 1280 px)")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a: selftest()
    elif "--requests" in a: requests(a[a.index("--requests") + 1])
    elif a[:1] == ["find"]: find(most=int(a[a.index("--max") + 1]) if "--max" in a else 12)
    elif a[:1] == ["fetch"]: fetch(most=int(a[a.index("--max") + 1]) if "--max" in a else 12)
    elif a[:1] == ["daily"]: daily(most=int(a[a.index("--max") + 1]) if "--max" in a else 80)
    elif a[:1] == ["looked"] and len(a) >= 3 and re.fullmatch(r"\d{4}-\d{2}-\d{2}", a[1]): editor(a[2:], {"looked_by_editor": a[1]})
    elif a[:1] == ["hold"] and len(a) == 3 and a[2].strip(): editor([a[1]], {"hold": a[2].strip()[:200]})
    else: sys.exit(__doc__)
