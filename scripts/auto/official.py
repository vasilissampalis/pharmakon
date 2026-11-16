#!/usr/bin/env python3
"""official.py: what official health bodies say about a question (docs/AUTOMATION.md).

The senior author, 15 November 2026: "I want it to read official websites too where it can get access"; "some parts of the
answers could come from official sites like NHS and EVERYTHING similar it's so many official sites worldwide".

    python3 -I scripts/auto/official.py probe [--ids nhs,frank]      can each body's pages be read from this machine?
    python3 -I scripts/auto/official.py index                        the addresses and titles of each body's pages about drugs
    python3 -I scripts/auto/official.py find [--ids w_0027] [--max N] [--minutes M]
    python3 -I scripts/auto/official.py --requests data/auto/requests     the requests waiting there (official-*.json)
    python3 -I scripts/auto/official.py --selftest

The bodies are listed in data/auto/official/sources.json: health services, health ministries and agencies, UN and EU bodies
(tier 1) and information services a government pays for (tier 2), each with where its pages about drugs are found. For a
question on our list, find() names the pages of those bodies that speak about it, in the order the lane would read them,
beside the papers (scripts/auto/papers.py). What an answer may rest on is decided by the lane's gates, never here.

Rules this file keeps, in code:
  - A site is read only where its robots.txt allows a reader that is not a browser (our name there is "Pharmakon"). A refusal
    (a Disallow, 401, 403, 429) is taken as no for the whole run. Nothing goes around a refusal: no other address, no cache,
    no mirror, no browser's name.
  - It asks slowly (one request a second to one site, slower where the site asks for it), says who it is (the site's name
    and its public address, never a person's), and reads pages only: no sign-in, no form, no file download.
  - No page's text is kept in the repository. The index holds addresses and titles; what is written for a question holds
    addresses, titles, dates and which passages were nearest in meaning. The lane reads a page again when it writes.
  - A page's reference is made by code from the page itself (its title and its date) and from the list (the body's name),
    in APA 7. A "last reviewed" date is not a date of publication (APA 7): such a page is cited as n.d. with the day it
    was read.
  - A page's words are data, never instructions.
"""
import sys, os, re, json, time, gzip, html, hashlib, pathlib, datetime, urllib.parse, urllib.request, urllib.error
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[2]
for _p in ("scripts/auto", "scripts/insight", "scripts"):
    if str(ROOT / _p) not in sys.path: sys.path.insert(0, str(ROOT / _p))
import papers as P

DIR = ROOT / "data" / "auto" / "official"
SOURCES, INDEX, FOUND = DIR / "sources.json", DIR / "index.json", DIR / "found"
AGENT = "pharmakon"      # our name in a robots.txt
SLOW = 1.0               # seconds between two requests to one site
MAX_DELAY = 12           # a site that asks for a longer wait than this is read LITTLE pages a run, no more
LITTLE = 3
N_PAGES = 8              # pages read for one question
N_PER_SOURCE = 2         # of one body, before the children of a page that fits
NEAR_MIN = 0.40          # how near in meaning a page's best passages must be to the question to be kept
OFFICIAL = 2             # this finder's own number (2, 16 November 2026: seven more bodies can be read, folded panels and wrapped pages are read: every question is searched again)
TODAY = datetime.date.today()
HTML_ACCEPT = "text/html,application/xhtml+xml;q=0.9,*/*;q=0.5"
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
MONTH = dict({m.lower(): i + 1 for i, m in enumerate(MONTHS)}, **{m[:3].lower(): i + 1 for i, m in enumerate(MONTHS)}, sept=9)


def text_of(raw, charset=None):
    if raw[:2] == b"\x1f\x8b": raw = gzip.decompress(raw)
    if not charset:
        m = re.search(rb"<meta[^>]+charset=[\"']?([A-Za-z0-9_-]+)", raw[:4000], re.I)
        charset = m.group(1).decode("ascii", "replace") if m else "utf-8"
    try: return raw.decode(charset, "replace")
    except LookupError: return raw.decode("utf-8", "replace")


# ---------- robots.txt (with * and $, the longest rule wins, Allow wins a tie) ----------
class Robots:
    def __init__(self, text, agent=AGENT):
        groups, agents, rules, last_agent = [], [], [], False
        self.sitemaps = []
        for raw in (text or "").splitlines():
            line = raw.split("#", 1)[0].strip()
            if ":" not in line: continue
            k, v = line.split(":", 1); k, v = k.strip().lower(), v.strip()
            if k == "user-agent":
                if not last_agent and agents: groups.append((agents, rules)); agents, rules = [], []
                agents.append(v.lower()); last_agent = True
            elif k in ("allow", "disallow", "crawl-delay"):
                last_agent = False
                if agents: rules.append((k, v))
            elif k == "sitemap": self.sitemaps.append(v)
        if agents: groups.append((agents, rules))
        mine = [r for a, r in groups if agent in a]
        self.rules = [x for r in mine for x in r] if mine else [x for a, r in groups if "*" in a for x in r]
        self.delay = 0.0
        for k, v in self.rules:
            if k == "crawl-delay":
                try: self.delay = max(self.delay, float(v))
                except ValueError: pass

    @staticmethod
    def _fits(pat, path):
        rx = "".join(".*" if c == "*" else re.escape(c) for c in pat.rstrip("$")) + ("$" if pat.endswith("$") else "")
        return re.match(rx, path) is not None

    def allowed(self, url):
        p = urllib.parse.urlsplit(url); path = (p.path or "/") + ("?" + p.query if p.query else "")
        best, verdict = -1, True
        for kind, pat in self.rules:
            if kind == "crawl-delay" or not pat: continue          # an empty Disallow disallows nothing
            if self._fits(pat, path) and (len(pat) > best or (len(pat) == best and kind == "allow")): best, verdict = len(pat), kind == "allow"
        return verdict


bare = lambda host: host.lower()[4:] if host.lower().startswith("www.") else host.lower()
same_site = lambda a, b: bare(urllib.parse.urlsplit(a).netloc) == bare(urllib.parse.urlsplit(b).netloc)


class Web:
    """Reading a site's pages the way the head of this file says. opener: for the selftest (no waiting, no network)."""
    def __init__(self, opener=None):
        self.opener, self.robots, self.said, self.last, self.count = opener, {}, {}, {}, {}
        self.kept = {}                                                    # the last pages read in this run: one asked for twice (a hub that is also a page) is read once
        try: srcs = json.load(open(SOURCES, encoding="utf-8"))["sources"]
        except (OSError, ValueError, KeyError, TypeError): srcs = []
        self.pace = {bare(urllib.parse.urlsplit(b["base"]).netloc): float(b["slow"]) for b in srcs if b.get("slow")}      # a body that asked us to slow down: seconds between two requests
        self.most = {bare(urllib.parse.urlsplit(b["base"]).netloc): int(b["most"]) for b in srcs if b.get("most")}        # a body that answers "too many requests" after a page or two: pages read in one run

    def rules(self, url):
        p = urllib.parse.urlsplit(url); host = p.scheme + "://" + p.netloc
        if host not in self.robots:
            try: got = self._open(host + "/robots.txt", "text/plain,*/*;q=0.5")
            except P.Refused as e: self.robots[host] = None; self.said[host] = "its robots.txt was refused (" + str(e)[:80] + ")"
            except (IOError, ValueError) as e: self.robots[host] = None; self.said[host] = "its robots.txt could not be read (" + str(e)[:80] + ")"
            else: self.robots[host] = Robots(text_of(got[0]) if got and not got[0][:200].lstrip().lower().startswith((b"<!doctype", b"<html")) else "")
        return self.robots[host], host

    def may(self, url):
        r, _ = self.rules(url)
        return bool(r) and r.allowed(url)

    def _open(self, url, accept, tries=2):
        """(bytes, the address it ended at), or None where there is nothing (404, 410)."""
        host = urllib.parse.urlsplit(url).netloc
        if host in P._refused: raise P.Refused(host + " said no earlier in this run")
        op = self.opener or urllib.request.urlopen
        for k in range(tries):
            try:
                with op(urllib.request.Request(url, headers={"User-Agent": P.UA.replace("scripts/auto/papers.py", "scripts/auto/official.py"), "Accept": accept, "Accept-Language": "en"}), timeout=25) as r:
                    raw = r.read(6_000_000); final = getattr(r, "geturl", lambda: url)() or url
                    return raw, final
            except urllib.error.HTTPError as e:
                if e.code in (404, 410): return None
                if e.code in (500, 502, 503, 504) and k + 1 < tries: time.sleep(0 if self.opener else 3 * (k + 1)); continue
                if e.code == 429 and k + 1 < tries:                          # "too many requests" means slower, not no: wait what the site asks (a minute at most) and ask once more
                    ra = str((e.headers or {}).get("Retry-After") or "").strip(); secs = int(ra) if ra.isdigit() else 20
                    if secs <= 60: time.sleep(0 if self.opener else secs); self.pace[bare(host)] = max(self.pace.get(bare(host), 0), 10.0); continue
                if e.code in (401, 403, 429, 451): P._refused.add(host); raise P.Refused(f"{host} answered {e.code}")
                raise IOError(f"{host} answered {e.code}")
            except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
                if k + 1 < tries: time.sleep(0 if self.opener else 2); continue
                raise IOError(f"{host} could not be reached: {str(e)[:120]}")
        return None

    def get(self, url, accept=HTML_ACCEPT):
        """(bytes, final address) of a page the site allows us to read; None where it is not there. Refused where the site says no."""
        r, host = self.rules(url)
        if r is None: raise P.Refused(urllib.parse.urlsplit(url).netloc + ": " + self.said[host])
        if not r.allowed(url): raise P.Refused("robots.txt does not allow " + urllib.parse.urlsplit(url).path)
        if url in self.kept: return self.kept[url]
        if r.delay > MAX_DELAY and self.count.get(host, 0) >= LITTLE: raise P.Refused(f"{urllib.parse.urlsplit(url).netloc} asks for {r.delay:.0f} seconds between requests: only {LITTLE} pages are read in a run")
        if self.count.get(host, 0) >= self.most.get(bare(urllib.parse.urlsplit(url).netloc), 10 ** 9): raise P.Refused(f"{urllib.parse.urlsplit(url).netloc}: only {self.most[bare(urllib.parse.urlsplit(url).netloc)]} of its pages are read in a run (it answers 'too many requests' to more)")
        wait = max(SLOW, self.pace.get(bare(urllib.parse.urlsplit(url).netloc), 0), min(r.delay, MAX_DELAY)) - (time.time() - self.last.get(host, 0))
        if wait > 0 and not self.opener: time.sleep(wait)
        self.last[host] = time.time(); self.count[host] = self.count.get(host, 0) + 1
        got = self._open(url, accept)
        if got and not same_site(got[1], url) and not self.may(got[1]): raise P.Refused("it led to " + urllib.parse.urlsplit(got[1]).netloc + ", whose robots.txt does not allow the page")
        if got and len(got[0]) < 1_500_000:
            if len(self.kept) >= 8: self.kept.pop(next(iter(self.kept)))
            self.kept[url] = got
        return got


# ---------- a page: its title, its dates, its passages, its links ----------
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
DROP = {"script", "style", "noscript", "template", "svg", "nav", "footer", "aside", "form", "button", "select", "iframe", "dialog", "canvas", "video", "audio", "menu", "object", "map"}
BLOCK = {"p", "div", "section", "article", "main", "li", "ul", "ol", "dl", "dd", "dt", "table", "tr", "td", "th", "blockquote", "h1", "h2", "h3", "h4", "h5", "h6", "details", "summary", "header", "figure", "figcaption", "pre", "hr", "caption", "address"}
NOISE = re.compile(r"(?:^|[\s_-])(cookies?|breadcrumbs?|share|sharing|social|related|feedback|newsletter|pagination|pager|skip|skiplink|visually-hidden|sr-only|screen-reader-text|toc|sidebar|sidenav|side-nav|subnav|navbar|footer|survey|promo|advert|modal|popup|back-to-top|print)(?:$|[\s_-])", re.I)
PANEL = re.compile(r"accordion|collaps|disclosure|expand|faq|panel|tab-?pane|toggle-content|answer", re.I)
GENERIC = re.compile(r"^(?:english|français|francais|español|espanol|deutsch|en|fr|learn more|read more|more|more info(?:rmation)?|here|home|view|view all|details|link|click here|see more|find out more|download|load more[^/]*|next|previous|back|\W*)$", re.I)
LAYOUT_SAYS = re.compile(r"(?:with|has|have|no|without|show|hide|is)[-_]+(?:[a-z]+[-_]+)?(?:sidebar|sidenav|side-nav|toc|subnav|navbar|breadcrumbs?|share|social|related|print|footer)|--[a-z-]*(?:sidebar|toc|print|share)", re.I)
JUNK = re.compile(r"^(back to top|print this page|share this page|skip to (main )?content|on this page|table of contents|contents|more in .{0,60}|was this (page|information) helpful.*|give feedback.*|page last reviewed.*|next review due.*|last (updated|reviewed|modified).{0,60}|date modified.{0,40}|report a problem.*)$", re.I)
spaces = lambda t: re.sub(r"\s+", " ", t or "").strip()


class _Page(HTMLParser):
    def __init__(self, base, let=()):
        super().__init__(convert_charrefs=True)
        self.base, self.stack, self.drop, self.main, self.has_main = base, [], 0, 0, False
        self.let, self.left, self.cur_left, self.in_left_a = set(let), [], None, False         # what is let through on a second look; what was left out
        self.buf, self.blocks, self.heads, self.links, self.meta, self.title, self.h1, self.lang = [], [], {}, [], {}, "", "", ""
        self.in_title, self.a, self.cur_h = False, None, None

    def _flush(self):
        t = spaces("".join(self.buf)); self.buf = []
        if not t: return
        if self.cur_h:
            lvl = int(self.cur_h[1])
            if lvl == 1 and not self.h1 and (self.main or not self.has_main): self.h1 = t
            self.heads = {k: v for k, v in self.heads.items() if k < lvl}; self.heads[lvl] = t
            return
        if JUNK.match(t): return
        self.blocks.append({"where": " / ".join(self.heads[k] for k in sorted(self.heads) if k > 1), "text": t, "main": self.main > 0, "li": any(x[0] == "li" for x in self.stack)})

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html": self.lang = (a.get("lang") or "")[:5]
        if tag == "meta":
            k = (a.get("property") or a.get("name") or a.get("itemprop") or "").lower()
            if k and a.get("content") and k not in self.meta: self.meta[k] = a["content"].strip()
            return
        if tag == "title": self.in_title = True
        if tag in VOID:
            if tag == "br" and not self.drop: self.buf.append(" ")
            return
        ident = (a.get("class") or "") + " " + (a.get("id") or "")
        is_main = tag == "main" or a.get("role") == "main" or (tag == "article" and not self.main)
        noise = None if is_main else NOISE.search(ident)
        if noise and spaces(ident) in self.let: noise = None
        whole_form = tag == "form" and ("form " + spaces(ident)) in self.let          # a form that holds the page itself (second look)
        # (16 November 2026) a part that is only folded shut (an answer under its question, a tab) is the page's own content: it is read
        # where its class or its role says that it is such a panel; a hidden menu, pop-up or banner still is not
        folded = ("hidden" in a or a.get("aria-hidden") == "true") and not ((PANEL.search(ident) or a.get("role") in ("region", "tabpanel")) and not noise and (self.main or not self.has_main))
        why = ("" if whole_form else "form" if tag == "form" else "tag" if tag in DROP else "header" if tag == "header" and not self.main else "hidden" if folded
               else "role" if a.get("role") in ("navigation", "banner", "contentinfo", "search", "complementary") else "class" if noise else "")
        gone = bool(why)
        if tag in BLOCK and not self.drop: self._flush()
        self.stack.append((tag, gone, is_main))
        if gone and not self.drop: self.cur_left = [why, (tag + " " + spaces(ident))[:90], 0, ("form " if why == "form" else "") + spaces(ident), False, 0]; self.left.append(self.cur_left)   # [why, what, characters, key, holds the heading, characters inside links]
        if self.drop and tag == "a": self.in_left_a = True
        if self.drop and tag == "h1" and self.cur_left is not None: self.cur_left[4] = True     # it holds the page's own heading
        if gone: self.drop += 1
        if is_main: self.main += 1; self.has_main = True
        if self.drop: return
        if tag in ("h1", "h2", "h3", "h4"): self.cur_h = tag
        if tag == "a" and a.get("href"): self.a = [a["href"], []]

    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
        if tag == "a": self.in_left_a = False
        if tag in VOID: return
        i = next((j for j in range(len(self.stack) - 1, -1, -1) if self.stack[j][0] == tag), None)
        if i is None: return
        if tag == "a" and self.a and not self.drop:
            href, words = self.a; self.a = None
            u = urllib.parse.urldefrag(urllib.parse.urljoin(self.base, href.strip()))[0]
            if u.startswith("http"): self.links.append((u, spaces("".join(words)), self.main > 0))
        if (tag in BLOCK or tag == self.cur_h) and not self.drop: self._flush()
        if tag == self.cur_h: self.cur_h = None
        for t, gone, is_main in reversed(self.stack[i:]):                 # an element left open closes with its parent
            if gone: self.drop -= 1
            if is_main: self.main -= 1
        del self.stack[i:]

    def handle_data(self, data):
        if self.in_title: self.title += data
        if self.drop:
            if self.cur_left is not None and not any(t in ("script", "style", "noscript", "template", "svg") for t, _, _ in self.stack):
                self.cur_left[2] += len(data.strip())
                if self.in_left_a: self.cur_left[5] += len(data.strip())
            return
        self.buf.append(data)
        if self.a: self.a[1].append(data)


def parse_date(s):
    """[year, month, day], [year, month] or [year] read from a date as pages write it; None where there is none."""
    s = spaces(s)[:60]; now = TODAY.year + 1; out = None
    m = re.search(r"(?<!\d)(19\d\d|20\d\d)-(\d\d)-(\d\d)(?!\d)", s)
    if m: out = [int(m[1]), int(m[2]), int(m[3])]
    if not out:
        m = re.search(r"\b(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]{3,9})\.?,?\s+(19\d\d|20\d\d)\b", s)
        if m and m[2].lower() in MONTH: out = [int(m[3]), MONTH[m[2].lower()], int(m[1])]
    if not out:
        m = re.search(r"\b([A-Za-z]{3,9})\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(19\d\d|20\d\d)\b", s)
        if m and m[1].lower() in MONTH: out = [int(m[3]), MONTH[m[1].lower()], int(m[2])]
    if not out:
        m = re.search(r"\b([A-Za-z]{3,9})\.?\s+(19\d\d|20\d\d)\b", s)
        if m and m[1].lower() in MONTH: out = [int(m[2]), MONTH[m[1].lower()]]
    if not out:
        m = re.search(r"(?<!\d)(19\d\d|20\d\d)(\d\d)(\d\d)(?!\d)", s)
        if m: out = [int(m[1]), int(m[2]), int(m[3])]
    if not out:
        m = re.search(r"\b(19\d\d|20\d\d)\b", s)
        if m: out = [int(m[1])]
    if not out or not 1990 <= out[0] <= now or (len(out) > 1 and not 1 <= out[1] <= 12) or (len(out) > 2 and not 1 <= out[2] <= 31): return None
    return out


UPDATED_META = ("article:modified_time", "og:updated_time", "dcterms.modified", "dc.date.modified", "last-modified", "lastmod", "revised", "date.modified", "datemodified", "modified")
ISSUED_META = ("article:published_time", "dcterms.issued", "dc.date.issued", "dcterms.date", "dc.date", "date", "citation_publication_date", "citation_date", "dcterms.created", "dc.date.created", "datepublished")
UPDATED_TEXT = re.compile(r"\b(?:page |content |date |this page was )?(?:last )?(?:updated|modified|revised)(?: on| date)?\s*[:\-]?\s*(.{4,40})", re.I)
REVIEWED_TEXT = re.compile(r"\b(?:page |content |medically |date )?(?:last )?reviewed(?: on| date)?\s*[:\-]?\s*(.{4,40})", re.I)


def extract(html_text, url, size=1000):
    """What a page says: {title, site, lang, updated, issued, reviewed, passages: [{n, where, text}], links}.
    Only the page's own content is read (its <main> or <article> where it has one): no menus, no footers, no forms."""
    def look(let=()):
        p = _Page(url, let)
        try: p.feed(html_text); p.close()
        except Exception: pass
        p._flush(); return p
    p = look(); kept = sum(len(b["text"]) for b in p.blocks)
    # a layout whose class only SAYS it has a sidebar or a table of contents ("layout--with-sidebar") is not one; nor is a form
    # that wraps the whole page (ASP.NET), nor a block of text whose class names a feature ("share-selection"). Where nearly
    # nothing was kept, nothing of the page's main part, and an element left out for its class or as a form holds the page
    # (its heading is inside it, or its class is written the way layouts are, or it is text and not a list of links: a
    # sidebar is made of links), the page is read once more with it let through.
    big = [x for x in p.left if x[0] in ("class", "form") and x[2] >= 1500 and x[2] > 4 * kept and not any(b["main"] for b in p.blocks)
           and (x[4] or LAYOUT_SAYS.search(x[3]) or x[5] < 0.25 * x[2])]
    if big:
        q = look({x[3] for x in big})
        if sum(len(b["text"]) for b in q.blocks) > 2 * kept: p = q
    blocks = [b for b in p.blocks if b["main"]] if any(b["main"] for b in p.blocks) else p.blocks
    passages, cur = [], None
    def close():
        nonlocal cur
        if cur and len(cur["text"]) >= 60: passages.append({"n": len(passages), "where": cur["where"], "text": cur["text"]})
        cur = None
    for b in blocks:
        parts = [b["text"]]
        if len(b["text"]) > size * 1.4:                               # one very long block: cut at sentence ends
            parts, acc = [], ""
            for s in re.split(r"(?<=[.!?])\s+", b["text"]):
                if acc and len(acc) + len(s) > size: parts.append(acc); acc = s
                else: acc = (acc + " " + s).strip()
            if acc: parts.append(acc)
        for t in parts:
            if cur and (cur["where"] != b["where"] or len(cur["text"]) + len(t) > size): close()
            if cur is None: cur = {"where": b["where"], "text": t}
            else: cur["text"] += ("; " if b["li"] and not re.search(r"[.:;!?]$", cur["text"]) else " ") + t
    close()
    whole = " ".join(b["text"] for b in p.blocks) + " " + spaces(re.sub(r"<[^>]+>", " ", html_text[-6000:]))
    ld = lambda k: next((m for m in re.findall(r'"' + k + r'"\s*:\s*"([^"]{4,40})"', html_text)), "")
    first = lambda cands: next((d for d in (parse_date(c) for c in cands if c) if d), None)
    updated = first([m for m in UPDATED_TEXT.findall(whole)][:3] + [p.meta.get(k) for k in UPDATED_META] + [ld("dateModified")])
    issued = first([p.meta.get(k) for k in ISSUED_META] + [ld("datePublished")])
    reviewed = first([m for m in REVIEWED_TEXT.findall(whole)][:3] + [ld("lastReviewed")])
    title = spaces(p.h1) or spaces(p.meta.get("og:title", "")) or spaces(p.title)
    if not p.h1: title = re.split(r"\s+[|–—-]\s+", title)[0] if len(title) > 12 else title
    links = list(dict.fromkeys((u, t) for u, t, m in p.links if m or not p.has_main))
    return {"title": title[:200], "site": spaces(p.meta.get("og:site_name", ""))[:80], "lang": p.lang.lower(), "updated": updated, "issued": issued, "reviewed": reviewed, "passages": passages, "links": links,
            "org": spaces(p.meta.get("govuk:primary-publishing-organisation", ""))[:120],
            "left": [[x[0], x[1], x[2]] for x in sorted(p.left, key=lambda x: -x[2])[:6] if x[2] >= 200]}     # the largest parts left out and why (for the probe)


# ---------- the reference, in APA 7 ----------
def slug_words(url):
    path = urllib.parse.unquote(urllib.parse.urlsplit(url).path).rstrip("/")
    last = re.sub(r"\.(html?|aspx|php)$", "", path.rsplit("/", 1)[-1])
    return spaces(re.sub(r"[-_+]+", " ", re.sub(r"_en$", "", last)))


def reference(src, page, url, kind="webpage"):
    """The record of a page, in the form the site's references have (CSL). The body's name comes from the list; the title
    and the date from the page. Dated by its last update where the page gives one, else by its publication; a page that
    gives neither (or only when it was last reviewed) is n.d. and carries the day it was read."""
    date = page.get("updated") or page.get("issued")
    slug = re.sub(r"[^a-z0-9]+", "-", slug_words(url).lower()).strip("-")[:40] or hashlib.sha1(url.encode()).hexdigest()[:8]
    author = page.get("org") if src.get("author_from_page") and page.get("org") else src["author"]      # GOV.UK names the body that published each page
    rec = {"id": f"{src['id']}_{slug}", "type": kind, "title": page["title"] or slug_words(url).capitalize(), "author": [{"literal": author}],
           "issued": {"date-parts": [date or []]}, "URL": url, "accessed": {"date-parts": [[TODAY.year, TODAY.month, TODAY.day]]},
           "verification": {"status": "made by code", "metadata_source": "the page itself (title, date) and data/auto/official/sources.json (the body's name)", "verified_on": TODAY.isoformat()}}
    if src.get("site") and src["site"] != author: rec["publisher"] = src["site"]
    if page.get("reviewed") and not date: rec["notes"] = "The page says when it was last reviewed (" + "-".join(f"{x:02d}" for x in page["reviewed"]) + "), which APA 7 does not take as a date of publication."
    return rec


def apa(rec):
    """The reference as APA 7 writes a web page (the title is in italics on the site; here between asterisks)."""
    d = (rec.get("issued") or {}).get("date-parts", [[]])[0]
    when = "n.d." if not d else str(d[0]) + (", " + MONTHS[d[1] - 1] + (" " + str(d[2]) if len(d) > 2 else "") if len(d) > 1 else "")
    t = rec["title"]; au = rec["author"][0]["literal"]
    out = f"{au}{'' if au.endswith('.') else '.'} ({when}). *{t}*{' [' + rec['genre'] + ']' if rec.get('genre') else ''}{'' if re.search(r'[.?!]$', t) and not rec.get('genre') else '.'} "
    if rec.get("publisher") and rec["publisher"] != au: out += rec["publisher"] + ". "
    a = (rec.get("accessed") or {}).get("date-parts", [[]])[0]
    if not d and len(a) == 3: out += f"Retrieved {MONTHS[a[1] - 1]} {a[2]}, {a[0]}, from "
    return out + rec["URL"]


# ---------- the list of bodies, and the index of their pages ----------
def sources(ids=None):
    """The bodies on the list. One that refused our reader (its line says when: "refused") is left alone until it is named."""
    d = json.load(open(SOURCES, encoding="utf-8"))["sources"]
    return [s for s in d if (s["id"] in ids if ids else not s.get("refused"))]


def all_links(html_text, base):
    """Every link of a page, wherever it stands: a hub's list of pages is often outside its main part. [(address, words)]"""
    out = []
    for m in re.finditer(r"<a\b[^>]*?\bhref\s*=\s*([\"'])(.*?)\1[^>]*>(.*?)</a>", html_text, re.I | re.S):
        if m.group(2).strip().startswith("#"): continue                 # a place on the same page ("Skip to main content") is not a page's name
        u = urllib.parse.urldefrag(urllib.parse.urljoin(base, html.unescape(m.group(2).strip())))[0]
        if u.startswith("http"): out.append((u, spaces(html.unescape(re.sub(r"<[^>]+>", " ", m.group(3))))))
    return out


def wanted_by(src):
    inc = [re.compile(x) for x in src.get("include", [])]; exc = [re.compile(x) for x in src.get("exclude", [])]
    def want(u):
        if not same_site(u, src["base"]): return False
        path = urllib.parse.urlsplit(u).path or "/"
        return any(r.search(path) for r in inc) and not any(r.search(path) for r in exc) and not re.search(r"\.(pdf|docx?|xlsx?|pptx?|zip|jpe?g|png|gif|mp[34])$", path, re.I)
    return want


def sitemap(url, web, want, files=30, cap=20000, saw=None):
    """The addresses a sitemap lists that we want (a sitemap of sitemaps is followed, files of them at most).
    saw: a dict that is told how many files were read and how many addresses they listed in all."""
    out, queue, seen = {}, [url], set(); saw = saw if saw is not None else {}; saw.update(files=0, listed=0, eg=[])
    while queue and len(seen) < files and len(out) < cap:
        u = queue.pop(0)
        if u in seen: continue
        seen.add(u)
        got = web.get(u, "application/xml,text/xml;q=0.9,*/*;q=0.5")
        if not got: continue
        try: root = ET.fromstring(text_of(got[0]).encode("utf-8"))
        except ET.ParseError: continue
        saw["files"] += 1
        tag = lambda e: e.tag.rsplit("}", 1)[-1]
        for e in root:
            loc = next((spaces(c.text) for c in e if tag(c) == "loc"), ""); mod = next((spaces(c.text) for c in e if tag(c) == "lastmod"), "")
            if not loc: continue
            if tag(e) == "sitemap": queue.append(loc); continue
            saw["listed"] += 1
            if len(saw["eg"]) < 4 and saw["listed"] % 37 == 1: saw["eg"].append(urllib.parse.urlsplit(loc).path[:70])
            if want(loc): out[loc] = mod[:10]
    return out


def index_source(src, web):
    """{address: title} of a body's pages about drugs: the links of its hub pages (and of the pages its 'deep' rules name),
    and its sitemaps where the list asks for them. Returns (pages, notes)."""
    want, pages, notes = wanted_by(src), {}, []
    deep = [re.compile(x) for x in src.get("deep", [])]; second = []
    def take(hub, into):
        got = web.get(hub)
        if got is None: notes.append(f"{hub}: not there"); return 0
        n = 0; links = all_links(text_of(got[0]), got[1])
        if not any(want(u.split("?", 1)[0]) for u, _ in links):          # a hub that led nowhere: what it looked like (a page of the site, or a wall?)
            tops = {}
            for u, _ in links:
                if same_site(u, src["base"]): k = "/".join(urllib.parse.urlsplit(u).path.split("/")[:2]); tops[k] = tops.get(k, 0) + 1
            title = spaces(re.sub(r"<[^>]+>", " ", (re.search(r"<title[^>]*>(.*?)</title>", text_of(got[0]), re.I | re.S) or [None, ""])[1]))[:70]
            notes.append(f"{hub}: led nowhere: {len(got[0])} bytes, {len(links)} links, title '{title}', its links go under " + ", ".join(f"{k} ({v})" for k, v in sorted(tops.items(), key=lambda x: -x[1])[:6]))
        for u, t in links:
            if not src.get("keep_query"): u = u.split("?", 1)[0]          # one page under one address (FRANK links a drug once for every name it has)
            if not want(u): continue
            t = t if 3 <= len(t) <= 120 and not GENERIC.match(t) else ""       # ("Learn more", "English": words that name nothing; the address's own words are used)
            if u in pages:
                if t and t.lower() not in pages[u].lower() and len(pages[u]) < 200: pages[u] += " / " + t      # its other names help to find it
                continue
            pages[u] = t or slug_words(u); n += 1
            if into is not None and any(r.search(urllib.parse.urlsplit(u).path) for r in deep): into.append(u)
        return n
    try:
        for hub in src.get("hubs", []):
            try: n = take(hub, second); notes.append(f"{hub}: {n} pages")
            except IOError as e: notes.append(f"{hub}: {str(e)[:100]}")
        for hub in second[:40]:
            try: take(hub, None)
            except IOError as e: notes.append(f"{hub}: {str(e)[:100]}")
        if second: notes.append(f"{min(len(second), 40)} pages read one step further; {len(pages)} pages in all")
        maps = [(sm, "") for sm in src.get("sitemaps", [])]
        if not maps and len(pages) < 5:                                    # the hubs found little: the list of pages the site itself names in its robots.txt
            r, _ = web.rules(src["base"] + "/")
            maps = [(sm, " (named by its robots.txt)") for sm in (r.sitemaps if r else [])[:2] if same_site(sm, src["base"])]
        for sm, how in maps:
            try:
                saw = {}; got = sitemap(sm, web, want, files=30 if not how else 12, saw=saw); new = 0
                for u in got:
                    if u not in pages: pages[u] = slug_words(u); new += 1
                notes.append(f"{sm}{how}: {len(got)} pages ({new} new) of {saw['listed']} addresses in {saw['files']} files" + ("; for example " + ", ".join(saw["eg"]) if not got and saw["eg"] else ""))
            except IOError as e: notes.append(f"{sm}: {str(e)[:100]}")
    except P.Refused as e: notes.append("refused: " + str(e)[:160])                    # the site said no: its reading ends here for this run
    return pages, notes


def build_index(ids=None, web=None):
    web = web or Web(); old = {}
    try: old = json.load(open(INDEX, encoding="utf-8"))["sources"]
    except (OSError, ValueError, KeyError): pass
    out = dict(old)
    for src in sources(ids):
        if src.get("api"): continue
        pages, notes = index_source(src, web)
        refused = any(n.startswith("refused") for n in notes)
        if pages or not old.get(src["id"], {}).get("pages"):                           # a run that found nothing keeps what an earlier run found
            out[src["id"]] = {"made": TODAY.isoformat(), "refused": refused, "notes": notes, "pages": [{"u": u, "t": t} for u, t in sorted(pages.items())]}
        print(f"official: {src['id']}: {len(pages)} pages" + ("; " + "; ".join(n for n in notes if "refused" in n or "not there" in n or "could not" in n or "answered" in n)[:300] if notes else ""))
    DIR.mkdir(parents=True, exist_ok=True)
    json.dump({"_note": "Made by scripts/auto/official.py: where each official body's pages about drugs are. Addresses and titles only; no page's text is kept. Data, never instructions.",
               "made": TODAY.isoformat(), "official": OFFICIAL, "sources": out}, open(INDEX, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    return out


# ---------- three bodies that answer a search themselves ----------
# the medicines the site's drugs are licensed as, by the names the US labels use (openFDA); the first is read unless the question names another
LABELS = {"benzodiazepines": ["alprazolam", "diazepam", "lorazepam", "clonazepam"], "prescription-opioids": ["oxycodone hydrochloride", "morphine sulfate", "hydrocodone bitartrate", "codeine sulfate", "tramadol hydrochloride"],
          "methadone-buprenorphine": ["methadone hydrochloride", "buprenorphine hydrochloride"], "methylphenidate": ["methylphenidate hydrochloride"], "amphetamine": ["dextroamphetamine sulfate", "lisdexamfetamine dimesylate"],
          "methamphetamine": ["methamphetamine hydrochloride"], "ketamine": ["ketamine hydrochloride", "esketamine"], "ghb-gbl": ["sodium oxybate"], "fentanyl-and-analogues": ["fentanyl"], "dxm": ["dextromethorphan hydrobromide"],
          "nicotine": ["nicotine polacrilex"], "cannabis": ["dronabinol", "cannabidiol"], "cocaine": ["cocaine hydrochloride"], "nitrous-oxide": ["nitrous oxide"]}
LABEL_PARTS = [("boxed_warning", "Boxed warning"), ("indications_and_usage", "Indications and usage"), ("dosage_and_administration", "Dosage and administration"), ("contraindications", "Contraindications"),
               ("warnings_and_cautions", "Warnings and precautions"), ("warnings", "Warnings"), ("drug_abuse_and_dependence", "Drug abuse and dependence"), ("overdosage", "Overdosage"),
               ("use_in_specific_populations", "Use in specific populations"), ("drug_interactions", "Drug interactions"), ("adverse_reactions", "Adverse reactions")]


def chunks(text, size=1000):
    out, acc = [], ""
    for s in re.split(r"(?<=[.!?])\s+", spaces(text)):
        if acc and len(acc) + len(s) > size: out.append(acc); acc = s
        else: acc = (acc + " " + s).strip()
    if acc: out.append(acc)
    return out


def fda_label(generic, web, src):
    """The current US label of a medicine (openFDA, public domain): a page of passages and its reference, or None."""
    q = urllib.parse.quote(f'openfda.generic_name:"{generic}"')
    got = web.get(f"https://api.fda.gov/drug/label.json?search={q}&sort=effective_time:desc&limit=3", "application/json")
    if not got: return None
    try: res = json.loads(got[0].decode("utf-8")).get("results") or []
    except ValueError: return None
    res = [r for r in res if any(r.get(k) for k, _ in LABEL_PARTS)]
    if not res: return None
    r = res[0]; fda = r.get("openfda") or {}; passages = []
    for k, name in LABEL_PARTS:
        for t in chunks(" ".join(x for x in (r.get(k) or []) if isinstance(x, str))):
            if len(t) >= 60: passages.append({"n": len(passages), "where": name, "text": t})
    brand = (fda.get("brand_name") or [generic])[0]; maker = (fda.get("manufacturer_name") or [src["author"]])[0]; setid = r.get("set_id") or ""
    title = brand.title() if brand.isupper() else brand
    if generic.split()[0].lower() not in title.lower(): title += " (" + generic + ")"
    page = {"title": title, "site": "DailyMed", "lang": "en", "updated": parse_date(str(r.get("effective_time") or "")), "issued": None, "reviewed": None, "passages": passages, "links": []}
    url = "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=" + setid if setid else "https://api.fda.gov/drug/label.json?search=" + q
    ref = reference(dict(src, author=maker, short=src.get("short"), site="DailyMed"), page, url)
    ref["id"] = "label_" + re.sub(r"[^a-z0-9]+", "-", generic.lower()).strip("-")[:40]; ref["genre"] = "Drug label"
    return page, url, ref


def medlineplus(words, web):
    """MedlinePlus health topics (US National Library of Medicine) that a search of its own finds: [(address, title)]."""
    got = web.get("https://wsearch.nlm.nih.gov/ws/query?db=healthTopics&retmax=6&term=" + urllib.parse.quote(" ".join(words)), "application/xml,text/xml;q=0.9,*/*;q=0.5")
    if not got: return []
    try: root = ET.fromstring(got[0])
    except ET.ParseError: return []
    out = []
    for d in root.iter("document"):
        t = next((spaces(re.sub(r"<[^>]+>", "", c.text or "")) for c in d.iter("content") if c.get("name") == "title"), "")
        if d.get("url") and t: out.append((d.get("url"), t))
    return out


def govuk(words, web):
    """GOV.UK pages a search of its own finds (its public search API): guidance and publications of the health bodies."""
    q = urllib.parse.urlencode([("q", " ".join(words)), ("count", "10"), ("fields", "title,link,format,public_timestamp")] + [("filter_organisations", o) for o in
        ("office-for-health-improvement-and-disparities", "department-of-health-and-social-care", "uk-health-security-agency", "public-health-england", "advisory-council-on-the-misuse-of-drugs", "medicines-and-healthcare-products-regulatory-agency")])
    got = web.get("https://www.gov.uk/api/search.json?" + q, "application/json")
    if not got: return []
    try: res = json.loads(got[0].decode("utf-8")).get("results") or []
    except ValueError: return []
    return [("https://www.gov.uk" + r["link"], spaces(r.get("title", ""))) for r in res if isinstance(r.get("link"), str) and r["link"].startswith("/") and r.get("format") not in ("statistics", "national_statistics", "official_statistics", "consultation", "press_release", "news_story", "speech", "foi_release", "transparency")]


# ---------- for one question ----------
flat = lambda t: " " + re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip() + " "


def drug_words(item, names):
    """(the site's drugs a question is about, the names official pages may use for them)."""
    slugs = list(item.get("drugs") or [])
    for n, ss in names:
        if len(ss) <= 2 and re.search(r"(?<!\w)" + re.escape(n) + r"(?!\w)", item["q"], re.I):
            slugs += [s for s in ss if s not in slugs]
    words = [n.lower() for n, ss in names if len(n) >= 3 and len(ss) <= 2 and any(s in slugs for s in ss)]
    for s in slugs: words += [t.lower() for t in P.SYN.get(s, []) if not t.startswith("(")] + [s.replace("-", " ")]
    words += [str(n).lower() for n in item.get("names") or [] if len(str(n)) >= 3]         # a drug that has no page yet: what official pages call it comes with the question (scripts/auto/grow.py)
    return slugs, list(dict.fromkeys(words))


def has_word(fl, words): return any(" " + w + " " in fl or " " + w + "s " in fl for w in words)


def candidates(item, names, index, srcs):
    """The pages of the index that may speak about a question, the likeliest first: [(score, source id, address, title)]."""
    slugs, dwords = drug_words(item, names)
    pat = re.compile(r"(?<!\w)(" + "|".join(re.escape(n) for n, _ in names) + r")(?!\w)", re.I)
    topics = list(item.get("terms") or [])[:8] + P.topic_terms([item["q"]] + list(item.get("ways") or []), lambda t: pat.sub(" ", t))
    topics = [w.lower() for w in dict.fromkeys(topics) if len(w) >= 4][:14]
    out = []
    for src in srcs:
        for pg in (index.get(src["id"]) or {}).get("pages", []):
            fl = flat(pg["t"] + " " + slug_words(pg["u"]))
            drug = has_word(fl, dwords) if dwords else False
            topic = sum(1 for w in topics if " " + w in fl)
            if dwords and not drug and topic < 2: continue
            if not dwords and not topic: continue
            out.append((round((2.0 if drug else 0) + 0.35 * min(topic, 3) + (0.2 if src.get("tier", 1) == 1 else 0), 2), src["id"], pg["u"], pg["t"]))
    out.sort(key=lambda x: (-x[0], x[2]))
    return out, slugs, dwords, topics


def find(item, names, enc, index=None, web=None, srcs=None):
    """The official pages that speak about one question, in the order the lane would read them (see the head of this file)."""
    web = web or Web(); srcs = srcs if srcs is not None else sources()
    if index is None: index = json.load(open(INDEX, encoding="utf-8"))["sources"]
    by_id = {s["id"]: s for s in srcs}
    cands, slugs, dwords, topics = candidates(item, names, index, [s for s in srcs if not s.get("api")])
    queue, per = [], {}
    for sc, sid, u, t in cands:                                           # two pages of one body at most, bodies in turn
        if per.get(sid, 0) < N_PER_SOURCE: per[sid] = per.get(sid, 0) + 1; queue.append((sid, u, t, "its title names the drug or the subject"))
    log, problems, pages, labels = [], [], [], []
    search_words = (dwords[:2] if dwords else []) + topics[:3]
    for src in srcs:                                                      # the bodies that answer a search themselves
        if not src.get("api") or not search_words: continue
        try:
            if src["api"] == "medlineplus": got = medlineplus(search_words[:3], web)
            elif src["api"] == "govuk": got = govuk(search_words[:4], web)
            elif src["api"] == "openfda":
                got = []
                for s in slugs[:2]:
                    gens = LABELS.get(s) or []
                    gen = next((g for g in gens if re.search(r"(?<!\w)" + re.escape(g.split()[0]) + r"(?!\w)", item["q"], re.I)), gens[0] if gens else None)
                    if gen: labels.append((src, gen))
            else: got = []
            log.append({"body": src["id"], "search": " ".join(search_words[:4]), "found": len(got) + (len(labels) if src["api"] == "openfda" else 0)})
            for u, t in got[:N_PER_SOURCE + 1]: queue.append((src["id"], u, t, "the body's own search found it"))
        except P.Refused as e: problems.append(f"{src['id']} said no: {str(e)[:120]}")
        except (IOError, ValueError) as e: problems.append(f"{src['id']}: {str(e)[:120]}")
    Q = enc([item["q"]] + list(item.get("ways") or [])[:6] + ([" ".join(item["terms"][:6])] if item.get("terms") else []))
    def weigh(sid, page, url, ref, why, more=None):
        ps = page["passages"]
        if not ps: return
        body = " ".join(p["text"] for p in ps)
        if dwords and not has_word(flat(page["title"] + " " + body), dwords): return     # a page that never names the drug says nothing about it
        sim = (enc([(page["title"] + ". " if page["title"] else "") + (p["where"] + ". " if p["where"] else "") + p["text"][:700] for p in ps]) @ Q.T).max(1)   # a passage is read under its page's title and its own heading
        order = sorted(range(len(ps)), key=lambda i: -float(sim[i])); top = float(sim[order[0]])
        near = round(sum(float(sim[i]) for i in order[:2]) / min(2, len(order)), 3)
        keep = [i for i in order[:6] if float(sim[i]) >= max(0.25, top - 0.18)]
        src = by_id[sid]
        pages.append({"body": sid, "name": src["author"], "short": (more or {}).get("short") or (src.get("short") or src["author"] if ref["author"][0]["literal"] == src["author"] else ref["author"][0]["literal"]), "tier": src.get("tier", 1), "country": src.get("country", ""), "address": url, "title": page["title"],
                      "updated": page["updated"], "reviewed": page["reviewed"], "near": near, "passages": sorted(keep), "of": len(ps), "sha": hashlib.sha1(body.encode("utf-8")).hexdigest()[:16],
                      "why": why + f"; nearness to the question {near:.2f}", "apa": apa(ref), "ref": ref, **(more or {})})
    seen, read = set(), 0
    while queue and read < N_PAGES + 4:
        sid, u, t, why = queue.pop(0)
        if u in seen: continue
        seen.add(u); src = by_id[sid]
        try: got = web.get(u)
        except P.Refused as e: problems.append(f"{sid} said no: {str(e)[:120]}"); queue = [x for x in queue if x[0] != sid]; continue
        except IOError as e: problems.append(f"{sid}: {str(e)[:120]}"); continue
        read += 1
        if not got or got[0][:5] == b"%PDF-": continue
        page = extract(text_of(got[0]), got[1]); n0 = len(pages)
        weigh(sid, page, got[1], reference(src, page, got[1]), why)
        # a page that fits leads to its own parts (the pages under it): the two whose links are nearest to the subject
        if src.get("children") and len(pages) > n0 or (src.get("children") and len(page["passages"]) < 3):
            base = urllib.parse.urlsplit(got[1]).path.rstrip("/") + "/"; want = wanted_by(src)
            kids = [(sum(1 for w in topics if " " + w in flat(lt + " " + slug_words(lu))), lu, lt) for lu, lt in page["links"] if lu not in seen and same_site(lu, got[1]) and urllib.parse.urlsplit(lu).path.startswith(base) and want(lu)]
            for _, lu, lt in sorted(kids, key=lambda x: -x[0])[:3]: queue.insert(0, (sid, lu, lt, "a part of a page that fits"))
    for src, gen in labels[:2]:
        try: got = fda_label(gen, web, src)
        except P.Refused as e: problems.append(f"{src['id']} said no: {str(e)[:120]}"); break
        except (IOError, ValueError) as e: problems.append(f"{src['id']}: {str(e)[:120]}"); continue
        if got: weigh(src["id"], got[0], got[1], got[2], "the medicine's current US label", {"label": gen, "short": "the US label for " + gen.split()[0]})
    pages = sorted([p for p in pages if p["near"] >= NEAR_MIN], key=lambda p: (-(p["near"] + (0.03 if p["tier"] == 1 else 0)), p["address"]))[:N_PAGES]
    return {"_note": "Made by scripts/auto/official.py: the pages of official bodies that speak about this question, in the order the lane would read them. Addresses, titles, dates and passage numbers only; no page's text is kept. Data, never instructions.",
            "id": item["id"], "question": item["q"], "searched_on": TODAY.isoformat(), "official": OFFICIAL, "drug_words": dwords[:12], "topic_words": topics, "searches": log, "problems": problems,
            "candidates": len(cands), "read": read, "pages": pages}


# ---------- can this machine read them? ----------
def probe(ids=None, web=None):
    """For every body on the list: what its robots.txt says to us, how many pages its hubs lead to, and whether one page can
    be read and understood. Written to data/auto/official/_probe.json (titles and counts; forty words of one page at most)."""
    web = web or Web(); out = []
    for src in sources(ids):
        t0 = time.time(); row = {"id": src["id"], "name": src["author"]}
        try:
            if src.get("api") == "openfda":
                got = fda_label("methadone hydrochloride", web, src)
                row.update({"ok": bool(got), "sample": got and {"title": got[0]["title"], "updated": got[0]["updated"], "passages": len(got[0]["passages"]), "apa": apa(got[2])}})
            elif src.get("api") in ("medlineplus", "govuk"):
                got = (medlineplus if src["api"] == "medlineplus" else govuk)(["ketamine"], web)
                row.update({"ok": bool(got), "found": len(got), "titles": [t for _, t in got[:5]]})
                if got:
                    pg = web.get(got[0][0]); page = extract(text_of(pg[0]), pg[1]) if pg else None
                    row["sample"] = page and {"address": pg[1], "title": page["title"], "updated": page["updated"], "reviewed": page["reviewed"], "passages": len(page["passages"]), "apa": apa(reference(src, page, pg[1]))}
            else:
                r, host = web.rules(src["base"] + "/")
                row["robots"] = web.said.get(host) if r is None else {"delay": r.delay, "rules": len(r.rules), "sitemaps": r.sitemaps[:4], "hubs_allowed": [web.may(h) for h in src.get("hubs", [])]}
                pages, notes = index_source(src, web); row["notes"] = notes; row["pages"] = len(pages)
                row["titles"] = [t for _, t in sorted(pages.items())[:400:max(1, len(pages) // 8)]][:8]
                tops = {}
                for u in pages:
                    k = "/".join(urllib.parse.urlsplit(u).path.split("/")[:3]); tops[k] = tops.get(k, 0) + 1
                row["under"] = sorted(tops.items(), key=lambda x: -x[1])[:6]
                if pages:
                    u = next((u for u in sorted(pages) if u in web.kept), None) or next((u for u in sorted(pages) if re.search(r"ketamin|cannabis|alcohol|cocaine|mdma|ecstasy|opioid|heroin", u, re.I)), sorted(pages)[0])
                    pg = web.get(u); page = extract(text_of(pg[0]), pg[1]) if pg else None; row["sample_address"] = u; row["sample_there"] = bool(pg)
                    row["sample"] = page and {"address": pg[1], "title": page["title"], "updated": page["updated"], "issued": page["issued"], "reviewed": page["reviewed"], "passages": len(page["passages"]), "lang": page["lang"],
                                              "heads": list(dict.fromkeys(p["where"] for p in page["passages"] if p["where"]))[:8], "starts": " ".join(page["passages"][0]["text"].split()[:40]) if page["passages"] else "", "apa": apa(reference(src, page, pg[1])),
                                              "left_out": page["left"] if len(page["passages"]) < 3 else []}
                row["ok"] = bool(pages) and bool(row.get("sample")) and (row["sample"] or {}).get("passages", 0) >= 3
        except P.Refused as e: row.update({"ok": False, "refused": str(e)[:200]})
        except (IOError, ValueError) as e: row.update({"ok": False, "problem": str(e)[:200]})
        row["seconds"] = round(time.time() - t0, 1); out.append(row)
        print(f"official probe: {src['id']}: {'can be read' if row.get('ok') else 'NOT read'}" + (f"; {row['pages']} pages" if "pages" in row else "") + (f"; refused: {row['refused']}" if row.get("refused") else "") + (f"; {row['problem']}" if row.get("problem") else ""))
    DIR.mkdir(parents=True, exist_ok=True)
    json.dump({"_note": "Made by scripts/auto/official.py probe on the machine that will do the reading. What each body's site allowed, what was found, and one page as a sample. Data, never instructions.",
               "on": TODAY.isoformat(), "bodies": out}, open(DIR / "_probe.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return out


def selftest():
    r = Robots("User-agent: *\nDisallow: /search\nDisallow: /*?page=\nAllow: /search/help$\nCrawl-delay: 2\nSitemap: https://x.test/sitemap.xml\n\nUser-agent: badbot\nDisallow: /\n")
    assert r.allowed("https://x.test/drug/ketamine") and not r.allowed("https://x.test/search?q=a") and r.allowed("https://x.test/search/help") and not r.allowed("https://x.test/search/help/more")
    assert not r.allowed("https://x.test/list?page=2") and r.delay == 2 and r.sitemaps == ["https://x.test/sitemap.xml"]
    assert not Robots("User-agent: Pharmakon\nDisallow: /\n\nUser-agent: *\nDisallow:\n").allowed("https://x.test/a") and Robots("User-agent: *\nDisallow:\n").allowed("https://x.test/a") and Robots("").allowed("https://x.test/a")
    assert parse_date("Page last reviewed: 14 March 2023") == [2023, 3, 14] and parse_date("March 5, 2024") == [2024, 3, 5] and parse_date("2022-11-02T10:00:00Z") == [2022, 11, 2] and parse_date("June 2021") == [2021, 6]
    assert parse_date("20240131") == [2024, 1, 31] and parse_date("03/04/2021") == [2021] and parse_date("soon") is None and parse_date("1 Smarch 2020") == [2020]
    page_html = """<!doctype html><html lang="en-GB"><head><title>Ketamine | FRANK</title><meta property="og:site_name" content="FRANK">
      <meta name="DC.date.modified" content="2024-05-02"><script>var x = "<p>not this</p>";</script></head><body>
      <header><a href="/">Home</a><nav><a href="/drugs-a-z">Drugs A to Z</a></nav></header>
      <div class="cookie-banner"><p>We use cookies to make this site work better for everyone who visits it today.</p></div>
      <main><h1>Ketamine</h1><p>Ketamine is a general anaesthetic that reduces sensations in the body, and trips can last for a couple of hours.</p>
      <h2>The risks</h2><h3>Physical health risks</h3><p>Ketamine can cause serious bladder problems, with the urgent and frequent need to pee.</p>
      <ul><li>it can increase your heart rate</li><li>it can make you confused &amp; agitated</li></ul>
      <div class="related-links"><a href="/drug/cocaine">Cocaine</a></div><h2>Mixing</h2><p>Mixing ketamine with alcohol is dangerous: both slow the body down a great deal.</p>
      <a href="/drug/ketamine/the-law">The law</a><p>Page last reviewed: 3 January 2023</p><form><input name="q"><button>Search</button></form></main>
      <footer><p>Copyright FRANK 2019. All rights reserved, as written in a footer that is long enough to be a block.</p></footer></body></html>"""
    pg = extract(page_html, "https://f.test/drug/ketamine")
    assert pg["title"] == "Ketamine" and pg["site"] == "FRANK" and pg["lang"] == "en-gb" and pg["updated"] == [2024, 5, 2] and pg["reviewed"] == [2023, 1, 3], pg
    texts = [p["text"] for p in pg["passages"]]; wheres = [p["where"] for p in pg["passages"]]
    assert len(texts) == 3 and wheres == ["", "The risks / Physical health risks", "Mixing"], (wheres, texts)
    assert "it can increase your heart rate; it can make you confused & agitated" in texts[1] and not any("cookies" in t or "Copyright" in t or "not this" in t or "reviewed" in t for t in texts), texts
    assert ("https://f.test/drug/ketamine/the-law", "The law") in pg["links"] and not any("cocaine" in u for u, _ in pg["links"]) and not any(u.endswith("/drugs-a-z") for u, _ in pg["links"]), pg["links"]
    src = {"id": "frank", "author": "FRANK", "short": "FRANK", "site": "", "tier": 1, "base": "https://f.test", "hubs": ["https://f.test/drugs-a-z"], "include": ["^/drug/[a-z0-9-]+(/[a-z-]+)?$"], "children": True}
    ref = reference(src, pg, "https://f.test/drug/ketamine")
    assert apa(ref) == "FRANK. (2024, May 2). *Ketamine*. https://f.test/drug/ketamine" and ref["id"] == "frank_ketamine", apa(ref)
    nd = reference(dict(src, author="National Health Service", site="NHS"), dict(pg, updated=None, issued=None), "https://f.test/drug/ketamine")
    assert apa(nd) == f"National Health Service. (n.d.). *Ketamine*. NHS. Retrieved {MONTHS[TODAY.month - 1]} {TODAY.day}, {TODAY.year}, from https://f.test/drug/ketamine" and "last reviewed" in nd["notes"], apa(nd)
    # a pretend web: a hub, two drug pages, a part of one, a site that says no in its robots.txt, a site that answers 403
    served = {"https://f.test/robots.txt": "User-agent: *\nDisallow: /search\n", "https://f.test/drugs-a-z": '<main><h1>Drugs A to Z</h1><a href="/drug/ketamine">Ketamine</a> <a href="/drug/cocaine">Cocaine</a> <a href="/search?q=x">Search</a> <a href="https://other.test/drug/x">Elsewhere</a></main>',
              "https://f.test/drug/ketamine": page_html, "https://f.test/drug/ketamine/the-law": "<main><h1>Ketamine and the law</h1><p>Ketamine is a Class B drug, which means it is illegal to have for yourself, give away or sell.</p><p>Possession can get you up to five years in prison, an unlimited fine or both of these.</p><p>Supplying someone else, even your friends, can get you up to fourteen years in prison.</p></main>",
              "https://f.test/drug/cocaine": "<main><h1>Cocaine</h1><p>Cocaine is a stimulant, so it makes people feel wide awake and confident for a short while.</p><p>The effects of snorted cocaine do not last long, around twenty to thirty minutes, which is short.</p><p>Cocaine is risky for anyone with high blood pressure or a heart condition of some kind.</p></main>",
              "https://no.test/robots.txt": "User-agent: *\nDisallow: /\n", "https://no.test/a": "<p>never read</p>"}
    asked = []
    class Resp:
        def __init__(self, b, u): self.b, self.u = b, u
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self, n=-1): return self.b
        def geturl(self): return self.u
    def opener(req, timeout=0):
        u = req.full_url; asked.append(u)
        assert "Pharmakon" in req.get_header("User-agent") and "contact@pharmakon.world" in req.get_header("User-agent")
        if u.startswith("https://wall.test/"): raise urllib.error.HTTPError(u, 403, "Forbidden", {}, None)
        if u not in served: raise urllib.error.HTTPError(u, 404, "Not Found", {}, None)
        return Resp(served[u].encode("utf-8"), u)
    web = Web(opener)
    pages, notes = index_source(src, web)
    assert sorted(pages) == ["https://f.test/drug/cocaine", "https://f.test/drug/ketamine"] and pages["https://f.test/drug/ketamine"] == "Ketamine", (pages, notes)
    for bad, why in (("https://no.test/a", "robots"), ("https://wall.test/a", "403")):
        try: web.get(bad); raise AssertionError("read a page of a site that said no")
        except P.Refused as e: assert why in str(e).lower() or "refused" in str(e).lower(), str(e)
    assert "https://no.test/a" not in asked and "https://wall.test/a" not in asked                 # never asked for: the robots.txt was the answer
    try: web.get("https://f.test/search?q=ketamine"); raise AssertionError("read a page its robots.txt disallows")
    except P.Refused: pass
    class Enc:                                                                                       # a pretend sense of meaning: shared words
        def __call__(self, texts):
            import numpy as np
            vocab = ["ketamine", "bladder", "law", "illegal", "prison", "cocaine", "class", "pee", "risks", "heart"]
            v = np.array([[1.0 if w in t.lower() else 0.0 for w in vocab] + [0.2] for t in texts], dtype=np.float32)
            return v / np.linalg.norm(v, axis=1, keepdims=True)
    names = [["ketamine", ["ketamine"]], ["cocaine", ["cocaine"]], ["ket", ["ketamine"]]]
    index = {"frank": {"pages": [{"u": u, "t": t} for u, t in pages.items()]}}
    item = {"id": "w_x", "q": "Is ketamine illegal?", "ways": ["what does the law say about ket", "can you go to prison for ketamine"], "drugs": ["ketamine"], "terms": ["law", "illegal", "prison"]}
    res = find(item, names, Enc(), index, web, [src])
    got = [(p["address"], p["passages"]) for p in res["pages"]]
    assert got and got[0][0] == "https://f.test/drug/ketamine/the-law" and "https://f.test/drug/cocaine" not in [a for a, _ in got], (got, res["problems"])
    assert res["pages"][0]["apa"].startswith("FRANK. (n.d.). *Ketamine and the law*. Retrieved ") and all("text" not in json.dumps(p) for p in res["pages"]) and res["pages"][0]["short"] == "FRANK" and "short" not in res["pages"][0]["ref"]["author"][0], res["pages"][0]
    # (16 November 2026) a layout whose class only says it HAS a sidebar holds the page: it is read on a second look; a real sidebar stays out
    body = " ".join(f"Caffeine intakes from all sources up to four hundred milligrams a day do not raise safety concerns for adults, sentence {i}." for i in range(30))
    lay = extract(f'<html><body><div class="layout layout--with-sidebar"><h1>Caffeine</h1><p>{body}</p><div class="sidebar"><p>Related topics: energy drinks and other things that belong to a sidebar.</p></div></div></body></html>', "https://e.test/caffeine")
    assert lay["title"] == "Caffeine" and len(lay["passages"]) >= 3 and not any("Related topics" in p["text"] for p in lay["passages"]), lay
    side = extract('<html><body><main><h1>Ketamine</h1><p>Ketamine is a general anaesthetic that reduces sensations in the body, as its page says in its main part.</p></main><div class="page-sidebar"><p>'
                   + "A long list of other pages that is not this page's own content. " * 40 + "</p></div></body></html>", "https://e.test/k")
    assert len(side["passages"]) == 1 and side["left"] and side["left"][0][0] == "class" and "sidebar" in side["left"][0][1], side
    assert all_links('<a href="#main">Skip to main content</a> <a href="/a#x">A page</a>', "https://e.test/caffeine") == [("https://e.test/a", "A page")]
    # an answer folded shut under its question is read; a hidden menu is not; "Learn more" is not a page's name; "too many requests" is asked once more
    fold = extract('<html><body><main><h1>Caffeine</h1><p>Caffeine is found in coffee, tea, cola and in what are sold as energy drinks, as this page says first.</p>'
                   '<div class="accordion-panel" hidden><p>Single doses of caffeine up to an amount the page names do not raise safety concerns for adults in the general population.</p></div>'
                   '<div class="mega-menu" hidden><p>Topics, publications, applications, engage, news, about us, and the other things a hidden menu holds for its site.</p></div></main></body></html>', "https://e.test/c")
    assert any("Single doses" in p["text"] for p in fold["passages"]) and not any("mega" in p["text"] or "hidden menu" in p["text"] for p in fold["passages"]), fold
    served.update({"https://g.test/robots.txt": "", "https://g.test/hub": '<a href="/drugs/alcohol">Learn more</a> <a href="/drugs/alcohol">Load More Experts +</a> <a href="/drugs/kava">Kava</a>', "https://slow.test/robots.txt": "", "https://slow.test/a": "<main><p>read on the second asking</p></main>"})
    gpages, _ = index_source({"id": "g", "author": "G", "base": "https://g.test", "hubs": ["https://g.test/hub"], "include": ["^/drugs/[a-z]+$"]}, web)
    assert gpages == {"https://g.test/drugs/alcohol": "alcohol", "https://g.test/drugs/kava": "Kava"}, gpages
    busy = {"n": 0}
    def opener2(req, timeout=0):
        if req.full_url == "https://slow.test/a":
            busy["n"] += 1
            if busy["n"] == 1: raise urllib.error.HTTPError(req.full_url, 429, "Too Many Requests", {"Retry-After": "5"}, None)
        return opener(req, timeout)
    w2 = Web(opener2); assert w2.get("https://slow.test/a")[0].startswith(b"<main>") and busy["n"] == 2 and w2.pace.get("slow.test") == 10.0
    # a form that wraps the whole page, and a block of text with a feature's class, are read on the second look; a block of links is not
    para = " ".join(f"Ashwagandha is a plant whose root is sold as a supplement for stress and sleep, as sentence {i} of its fact sheet says." for i in range(20))
    wrapped = extract(f'<html><body><form id="aspnetForm"><h1>Ashwagandha</h1><p>{para}</p></form></body></html>', "https://e.test/a")
    assert wrapped["title"] == "Ashwagandha" and len(wrapped["passages"]) >= 2, wrapped
    feat = extract(f'<html><body><header><h1>Alcohol</h1></header><section class="content-block share-selection"><p>{para}</p></section><div class="related"><ul>'
                   + "".join(f'<li><a href="/p{i}">Another page about another thing with a long enough name number {i}</a></li>' for i in range(40)) + "</ul></div></body></html>", "https://e.test/b")
    assert len(feat["passages"]) >= 2 and not any("Another page" in p["text"] for p in feat["passages"]), feat
    # a page asked for twice in one run is read once; a body that allows one page a run is asked for one
    n0 = len(asked); web.get("https://f.test/drug/cocaine"); web.get("https://f.test/drug/cocaine"); assert len(asked) - n0 <= 1
    w3 = Web(opener); w3.most["f.test"] = 1; w3.get("https://f.test/drug/ketamine")
    try: w3.get("https://f.test/drug/cocaine"); raise AssertionError("a second page of a body that allows one")
    except P.Refused as e: assert "only 1 of its pages" in str(e)
    assert w3.get("https://f.test/drug/ketamine")                                                # the page it already has is not a new request
    # a hub that leads nowhere says what it looked like, and the list of pages the site itself names in its robots.txt is read
    served.update({"https://m.test/robots.txt": "User-agent: *\nDisallow:\nSitemap: https://m.test/sitemap.xml\nSitemap: https://elsewhere.test/sitemap.xml\n",
                   "https://m.test/drugs": '<html><head><title>Drugs | M</title></head><body><a href="/about/us">About</a> <a href="/about/team">Team</a></body></html>',
                   "https://m.test/sitemap.xml": '<?xml version="1.0"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><sitemap><loc>https://m.test/sm1.xml</loc></sitemap></sitemapindex>',
                   "https://m.test/sm1.xml": '<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://m.test/drugs/ketamine</loc><lastmod>2026-01-02</lastmod></url><url><loc>https://m.test/blog/a</loc></url></urlset>'})
    msrc = {"id": "m", "author": "M", "short": "M", "tier": 2, "base": "https://m.test", "hubs": ["https://m.test/drugs"], "include": ["^/drugs/[a-z0-9-]+$"]}
    mpages, mnotes = index_source(msrc, web)
    assert list(mpages) == ["https://m.test/drugs/ketamine"] and "led nowhere" in mnotes[0] and "title 'Drugs | M'" in mnotes[0] and "/about (2)" in mnotes[0], (mpages, mnotes)
    assert any("named by its robots.txt" in n and "1 pages (1 new) of 2 addresses in 2 files" in n for n in mnotes) and not any("elsewhere.test" in u for u in asked), mnotes
    print("official selftest: ok (robots.txt with * and $ is obeyed and a refusal is never gone around; a page's own content, dates and links are read without menus, cookies or footers; "
          "the reference is APA 7 from the page itself; for a question, the part of a body's page that speaks about it stands first; no page's text is kept)")


def main():
    arg = sys.argv[1:]
    if "--selftest" in arg: return selftest()
    opt = lambda k, d=None: arg[arg.index(k) + 1] if k in arg else d
    do, ids, limit = (arg[0] if arg and not arg[0].startswith("--") else None), [x for x in (opt("--ids") or "").split(",") if x], int(opt("--max", "60"))
    if "--requests" in arg:                       # official-*.json: {"do": "probe" | "index" | "find", "ids": [...], "max": N}; read as data, taken off when read
        for f in sorted((ROOT / opt("--requests")).glob("official-*.json")):
            try: r = json.load(open(f, encoding="utf-8"))
            except ValueError: r = {}
            todo = [x for x in (r["do"] if isinstance(r.get("do"), list) else [r.get("do")]) if x in ("probe", "index", "find")]
            if todo: do = todo
            ids += [x for x in (r.get("ids") or []) if isinstance(x, str) and re.fullmatch(r"[a-z0-9_-]{1,40}", x)]
            if isinstance(r.get("max"), int): limit = max(1, min(80, r["max"]))
            f.unlink()
    do = do if isinstance(do, list) else [do]
    body_ids = [x for x in ids if not x.startswith("w_")] or None
    if "probe" in do: probe(body_ids)
    if "index" in do: build_index(body_ids)
    if "find" not in do:
        if not set(do) & {"probe", "index"}: sys.exit(__doc__)
        return
    ids = [x for x in ids if x.startswith("w_")]
    import build_index as bi
    names, enc, web, t0, minutes = bi.names_table(), P.General(), Web(), time.time(), float(opt("--minutes", "0") or 0)
    items = P.listed()
    def old(w):
        try: return int(json.load(open(FOUND / (w["id"] + ".json"), encoding="utf-8")).get("official") or 0) < OFFICIAL
        except (OSError, ValueError): return True
    items = sorted([w for w in items if (w["id"] in ids if ids else old(w))], key=lambda w: (FOUND / (w["id"] + ".json")).exists())[:limit]     # a question never searched comes before one searched by an older finder
    FOUND.mkdir(parents=True, exist_ok=True); index = json.load(open(INDEX, encoding="utf-8"))["sources"]; done = 0
    for w in items:
        if minutes and time.time() - t0 > minutes * 60: print(f"official: the time for this run is up; {len(items) - done} questions are left for the next run"); break
        res = find(w, names, enc, index, web)
        json.dump(res, open(FOUND / (w["id"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1); done += 1
        print(f"official: {w['id']} {w['q'][:60]!r}: {len(res['pages'])} pages of {len({p['body'] for p in res['pages']})} bodies" + (f"; problems: {'; '.join(res['problems'])[:200]}" if res["problems"] else ""))
    print(f"official: {done} questions searched")


if __name__ == "__main__":
    main()
