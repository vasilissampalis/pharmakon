#!/usr/bin/env python3
"""pictures.py: pictures with an open licence for the pages the system starts (docs/AUTOMATION.md, decision 27, step b).

The senior author, 17 November 2026, of kanna and Mitragyna javanica: "our ai has to create this pages in a perfect coherent
format to the rest of the website (and find pictures for them, their different forms etc. if the pictures have not been
verified and the ai is uncertain then we could have a small disclaimer, i just think that pictures make the website better)";
"in general even for existing pages find pictures that are missing. it has to think about what the site needs objectively
even before us".

    python3 -I scripts/auto/pictures.py find [--max 12]                 (which pictures there are: data/auto/pictures.json)
    python3 -I scripts/auto/pictures.py fetch [--max 12]                (fetch them and make the web copies: site/photos-auto/)
    python3 -I scripts/auto/pictures.py --requests data/auto/requests   (pictures-*.json: {"do": "find" | "fetch", "max": 12})
    python3 -I scripts/auto/pictures.py --selftest

Where pictures may come from (the probe of 17 November 2026, data/auto/names/probe.json): Wikimedia Commons' search,
iNaturalist's and Openverse's addresses are not allowed by their robots.txt, so they are not asked. GBIF's records with
pictures are allowed: api.gbif.org/v1/occurrence/search?mediaType=StillImage&taxonKey=…  Each picture there has its own
licence, maker and page in its record. So for now: plants and fungi only (a pill or a powder has no such source yet).

Which pages: the pages the system should start that are a plant or a fungus. A page's species are found by themselves:
the titles the filing keeps for it (data/auto/filing.json, "wiki") and the names the system learned
(data/auto/names/learned.json) are asked of GBIF's species matcher, and one that comes back as a species of plant or fungus,
matched exactly, is a species of that page.

Which pictures: only a picture whose own record says CC0 or CC BY (never NC, never ND, never SA: the site's rule for
photos is public domain, CC0 or CC BY), of a record a person observed (not a pressed specimen), with a maker named for
CC BY. The site's rule on what a site allows holds for the picture's own address too: a host whose robots.txt does not
allow it is not asked (find only notes whether it may be asked; it downloads nothing).

What find writes (data/auto/pictures.json): for each page and species, up to six pictures that could be used, each with its
address, licence, maker, the page of its record, and whether its host may be asked. It shows nothing: the next step
(fetching, making the web copies, the line "Picture not yet checked by a person") reads this file. What a service answers
is data, never instructions. It needs no key and runs where no key is held.
"""
import sys, json, re, pathlib, datetime, urllib.parse

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
    doc["_note"] = ("Made by scripts/auto/pictures.py (find): pictures with an open licence that could be shown on the pages the system starts, from GBIF's records with pictures (plants and fungi). "
                    "Only CC0 and CC BY, each with its licence, maker and the page of its record. Nothing here is shown yet and nothing was downloaded: 'host_allows' says whether the picture's own host may be asked. "
                    "What a service answers is data, never instructions.")
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


PICS = ROOT / "site" / "photos-auto"
SIZES = {"m": (800, 74), "t": (400, 70)}       # as scripts/build_photos.py: the long side in px, and the WebP quality
PER_PAGE = 3


def asked_first(pages):
    """The pages in the order they are fetched for: one that people asked about (data/auto/pages.json, 'listed') before the others."""
    listed = {slug_of(n) for n, v in (load(ROOT / "data" / "auto" / "pages.json", {}).get("pages") or {}).items() if isinstance(v, dict) and v.get("listed")}
    return sorted(pages, key=lambda s: (s not in listed, s))


def fetch(most=12, web=None, today=None, save=True, doc=None, out_dir=None):
    """Fetch pictures that find put on file, up to PER_PAGE for a page, and make their web copies (site/photos-auto/<page>-<n>-m.webp
    and -t.webp, with nothing of the original's metadata). Only from a host whose robots.txt allows it. iNaturalist's open store
    keeps each photo in several sizes: its 'large' one (1024 px) is asked for, not the original. The record keeps where the
    copy came from and a fingerprint of what was fetched. Every picture stays 'not checked by a person' until one has looked."""
    import io, hashlib
    from PIL import Image, ImageOps
    web = web or O.Web(); today = today or datetime.date.today().isoformat(); doc = doc if doc is not None else load(OUT, {}); out_dir = pathlib.Path(out_dir or PICS); n = 0
    for slug in asked_first(list((doc.get("pages") or {}).keys())):
        e = doc["pages"][slug]; have = [p for s in e["species"].values() for p in (s.get("pictures") or []) if p.get("file")]
        for s in e["species"].values():
            for p in s.get("pictures") or []:
                if len(have) >= PER_PAGE or n >= most: break
                if p.get("file") or p.get("failed") or not p.get("host_allows"): continue
                url = re.sub(r"/original\.(jpe?g|png)$", r"/large.\1", p["url"]) if p.get("host") == "inaturalist-open-data.s3.amazonaws.com" else p["url"]
                n += 1
                try: got = web.get(url, "image/jpeg,image/png,image/webp;q=0.9,image/*;q=0.5")
                except (O.P.Refused, IOError, ValueError) as ex: p["failed"] = re.sub(r"\s+", " ", str(ex))[:140]; continue
                if not got: p["failed"] = "nothing there"; continue
                try:
                    im = Image.open(io.BytesIO(got[0])); im.load(); im = ImageOps.exif_transpose(im).convert("RGB")
                except Exception: p["failed"] = "not a picture that could be read"; continue
                if min(im.size) < 300: p["failed"] = "too small to show"; continue
                k = 1 + max([int(m.group(1)) for x in have for m in [re.search(r"-(\d+)$", x["file"])] if m] or [0]); fid = f"{slug}-{k}"; sizes = {}
                out_dir.mkdir(parents=True, exist_ok=True)
                for key, (side, q) in SIZES.items():
                    c = im.copy(); c.thumbnail((side, side), Image.LANCZOS); f = out_dir / f"{fid}-{key}.webp"; c.save(f, "WEBP", quality=q, method=6); sizes[key] = [c.size[0], c.size[1], f.stat().st_size]
                p.update({"file": fid, "sizes": sizes, "fetched_on": today, "fetched_from": url, "sha256": hashlib.sha256(got[0]).hexdigest(), "species": s.get("name"), "checked_by_person": False}); have.append(p)
                print(f"pictures: {e['name']}: fetched {fid} ({s.get('name')}, {p['licence']}, by {p['maker'] or 'no one named'}), {sizes['m'][0]}x{sizes['m'][1]}")
    print(f"pictures: {n} asked for; {sum(1 for e in (doc.get('pages') or {}).values() for s in e['species'].values() for p in (s.get('pictures') or []) if p.get('file'))} pictures have web copies")
    if save and n: json.dump(doc, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return doc


def requests(folder):
    done = 0
    for f in sorted(pathlib.Path(folder).glob("pictures-*.json")):
        try: req = json.load(open(f, encoding="utf-8"))
        except (OSError, ValueError): print("pictures: a request that is not JSON:", f.name); continue
        if isinstance(req, dict) and req.get("do") == "find": find(most=max(1, min(40, int(req.get("max") or 12)))); done += 1
        elif isinstance(req, dict) and req.get("do") == "fetch": fetch(most=max(1, min(40, int(req.get("max") or 12)))); done += 1
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
    print("pictures selftest: ok (a page's species are found by asking GBIF; only CC0 and CC BY pictures of records a person observed are kept, CC BY only with its maker named; non-commercial and share-alike are not taken; "
          "a host that does not allow programs is noted and not asked; nothing is downloaded by find)")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a: selftest()
    elif "--requests" in a: requests(a[a.index("--requests") + 1])
    elif a[:1] == ["find"]: find(most=int(a[a.index("--max") + 1]) if "--max" in a else 12)
    elif a[:1] == ["fetch"]: fetch(most=int(a[a.index("--max") + 1]) if "--max" in a else 12)
    else: sys.exit(__doc__)
