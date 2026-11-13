#!/usr/bin/env python3
"""Build reference records from Crossref metadata (METHODS §4.1–4.3). Metadata is never typed by hand.

Inputs
  data/access/crossref-cache.jsonl     one compact Crossref record per line (fetched through the browser)
  data/access/crossref-webfetch-verified.jsonl   the same format, for records transcribed twice through WebFetch
                                       (works/<DOI> and a works search) that agreed on every field (WORKFLOW.md)
  data/references/_incoming/<sub>.txt  lines  reference_id>DOI>where-read   (written by reading agents)
  extra pairs on the command line      id=DOI@where  (e.g. volkow_2001c=10.1176/appi.ajp.158.3.383@pdf:PDFs/...)
Output
  appends new records to data/references/<sub>.json; never overwrites an existing id.
  prints DOIs missing from the cache so they can be fetched.
"""
import json, re, sys, glob, pathlib, datetime, html

ROOT = pathlib.Path(__file__).resolve().parents[1]
TODAY = datetime.date.today().isoformat()

# Words kept capitalized when converting titles to APA sentence case.
PROPER = set("""January February March April May June July August September October November December Monday Tuesday Wednesday Thursday Friday Saturday Sunday Parkinson Parkinson's Alzheimer Alzheimer's Huntington Utah California Toronto Ontario Canada Canadian American
America US USA U.S. United States Europe European EU UK England English British Scotland Scottish Wales Welsh Ireland Irish
Australia Australian New Zealand Sydney Melbourne China Chinese Japan Japanese Korea Korean Taiwan Thai Thailand Iran Iranian
India Indian Mexico Mexican Brazil Brazilian Africa African Asia Asian Latin Hispanic Denmark Danish Sweden Swedish Norway
Norwegian Finland Finnish Netherlands Dutch Germany German France French Greece Greek Italy Italian Spain Spanish Switzerland Swiss
Czech Portugal Portuguese Russia Russian Ukraine Poland Polish Vietnam Vietnamese Philippines Filipino Malaysia Indonesia
Wistar Sprague-Dawley Bayesian Mendelian Cochrane Hunter Sternbach Radomski Newcastle-Ottawa Wernicke Korsakoff Stroop Wisconsin
Rey Wechsler Hedges Egger GRADE Kaplan-Meier Cox Poisson Medicaid Medicare Veterans NESARC NSDUH ESPAD PET MRI fMRI DTI SPECT
FDG DSM DSM-IV DSM-5 ICD ICD-10 ICD-11 HIV AIDS HCV HBV CYP2D6 CYP3A4 COVID-19 SARS-CoV-2 LSD MDMA DMT GHB GBL THC CBD PCP
DXM NMDA GABA AMPA MAO MAOI SSRI SSRIs SNRI ADHD PTSD OCD ECT TMS RCT RCTs ED EDs ICU US-based UK-based Bupropion Kingdom Southeast Columbia""".split())
SMALL_AFTER_COLON = True

def clean(t):
    t = re.sub(r"(\w)<i>", r"\1 ", t or "")
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t).replace("‐", "-").replace("‑", "-").replace("‐", "-")
    return re.sub(r"\s+", " ", t).strip().rstrip(".")

def _lone_capital(pieces, i):
    """A single capital letter that is a word of its own (vitamin E, hepatitis C, type B; a lone "A" is the article) or a
    stereodescriptor before a bracket (S-(+)-methamphetamine), but not the E of e-cigarette."""
    core = re.sub(r"^[\[\(\"'“‘]+|[\]\)\"'”’.,;:?!]+$", "", pieces[i])
    if len(core) != 1 or not core.isupper() or core == "A": return False
    if len(pieces) == 1: return True
    return i + 2 < len(pieces) and pieces[i + 1] == "-" and pieces[i + 2].startswith("(")

def _keep_part(part):
    core = re.sub(r"^[\[\(\"'“‘]+|[\]\)\"'”’.,;:?!]+$", "", part)
    if not core: return True
    if core in PROPER or (core.endswith("'s") and core[:-2] in PROPER): return True
    letters = [c for c in core if c.isalpha()]
    if len(letters) >= 2 and all(c.isupper() for c in letters): return True          # acronym: PET, NESARC, WIN
    if re.search(r"\d", core) and any(c.isupper() for c in core): return True        # CYP2D6, 5-HT2A, [11C]WIN
    if any(c.isupper() for c in core[1:]) and not core[1:].isupper(): return True     # McCann, fMRI, iPhone
    return False

def sentence_case(t):
    out, cap_next = [], True
    for w in t.split(" "):
        core_w = re.sub(r"^[\[\(\"'“‘]+|[\]\)\"'”’.,;:?!]+$", "", w)
        letters_w = [c for c in core_w if c.isalpha()]
        if len(letters_w) >= 2 and all(c.isupper() for c in letters_w):
            out.append(w)                       # an all-capital compound keeps every part: ROBINS-I, QUADAS-2, COVID-19
            cap_next = w.endswith(":") or w.endswith("?") or w.endswith("!")
            continue
        pieces = re.split(r"([-/—–])", w)
        new_parts = []
        for i, part in enumerate(pieces):
            if cap_next and i == 0:
                # APA 7: the first word of the title and of a subtitle (after a colon, question or exclamation mark) is capitalized
                m = re.match(r"[^A-Za-zÀ-ÿ0-9]*([A-Za-zÀ-ÿ])", part)  # a word that starts with a digit keeps its letters: "21st-century"
                new_parts.append(part[:m.start(1)] + part[m.start(1)].upper() + part[m.start(1) + 1:] if m else part)
            elif part in ("-", "/", "—", "–") or _keep_part(part) or _lone_capital(pieces, i):
                new_parts.append(part)
            else:
                new_parts.append(part.lower())
        out.append("".join(new_parts))
        cap_next = w.endswith(":") or w.endswith("?") or w.endswith("!")
    s = " ".join(out)
    return s[0].upper() + s[1:] if s else s

def load_cache():
    cache = {}
    for name in ("crossref-cache.jsonl", "crossref-webfetch-verified.jsonl"):
        f = ROOT / "data" / "access" / name
        if not f.exists():
            continue
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                r.setdefault("_via", "browser" if name == "crossref-cache.jsonl" else "webfetch")
                # update links are strings: '<type>:<DOI>' (updated-by) or 'to:<type>:<DOI>' (update-to)
                r["upd"] = [u if isinstance(u, str) else (("to:" if u.get("direction") == "to" else "") + f"{u.get('type','')}:{u.get('DOI','')}") for u in r.get("upd", [])]
                cache.setdefault(r["DOI"].lower(), r)          # a browser record wins over a WebFetch one
    return cache

def full_title(cr):
    """Crossref keeps a subtitle separately for some publishers (AMA journals, for example); APA prints title: subtitle."""
    t, sub = cr.get("title", ""), cr.get("sub")
    return f"{t}: {sub}" if sub and sub.strip() and sub.strip().lower() not in t.lower() else t

def load_overrides():
    f = ROOT / "data" / "access" / "metadata-overrides.json"
    return {k.lower(): v for k, v in json.load(open(f, encoding="utf-8")).items()} if f.exists() else {}

OVERRIDES = load_overrides()
_CACHE = None  # the Crossref cache, loaded when a record needs another record (a retraction notice)

HY = lambda x: re.sub(r"\s+", " ", x.replace("\u2010", "-").replace("\u2011", "-")).strip() if isinstance(x, str) else x  # Wiley writes "Hartmann\u2010Boyce" with a Unicode hyphen (APA prints a plain one); ACS records can hold a line break inside a name ("Justin\nC.")

def record(rid, cr, where):
    ov = OVERRIDES.get(cr["DOI"].lower())
    if ov:
        cr = {**cr, **{k: v for k, v in ov.items() if k not in ("note", "source", "hold")}}
    yr = (cr.get("print") or cr.get("issued") or cr.get("online") or [None])[0]
    online = (cr.get("online") or [None])[0]
    rec = {
        "id": rid,
        "type": "article-journal" if cr.get("type") in ("journal-article", None) else ("chapter" if cr.get("type") == "book-chapter" else "report" if cr.get("type") == "report" else "book" if cr.get("type") in ("book", "edited-book", "monograph") else "article-journal"),
        "title": cr["title_apa"] if cr.get("title_apa") else sentence_case(clean(full_title(cr))),  # title_apa: a documented override for proper nouns the casing rules cannot know
        "author": [({"family": a[0], "given": a[1], "suffix": a[2]} if len(a) > 2 else {"family": a[0], "given": a[1]}) if len(a) > 1 else {"literal": a[0]} for a in [[HY(x) for x in a] for a in cr["au"]]] or [{"literal": cr.get("pub", "Anonymous")}],
        "container-title": clean(cr.get("ct", "")),
        "issued": {"date-parts": [[int(yr)]]},
        "DOI": cr["DOI"],
        "verification": {
            "status": "metadata-verified", "metadata_source": "crossref", "metadata_route": "browser" if cr.get("_via") == "browser" else "two agreeing WebFetch transcriptions", "verified_by": "AI (build_references.py)", "verified_on": TODAY,
            "retraction_check": {"status": "clear", "checked_on": TODAY},
        },
    }
    if rec["type"] in ("book", "report") and cr.get("pub"): rec["publisher"] = cr["pub"]  # APA 7: a book ends with its publisher (omitted by the formatter when it is the author)
    for k_out, k_in in (("volume", "vol"), ("issue", "iss"), ("page", "pg"), ("number", "number")):  # number: article number or e-locator
        if cr.get(k_in): rec[k_out] = cr[k_in]
    if re.fullmatch(r"(\w+)-\1", rec.get("page", "")): rec["page"] = rec["page"].split("-")[0]  # Crossref writes a one-page item as "1479-1479"
    if rec.get("number") and rec.get("page") == rec["number"]: del rec["page"]  # Elsevier repeats the article number as the page ("106479")
    if not rec.get("number") and re.fullmatch(r"\d+", rec.get("page", "")) and re.match(r"10\.(1186|3390|3389|1371)/", cr["DOI"]):
        rec["number"] = rec.pop("page")  # BioMed Central, MDPI, Frontiers and PLOS number their articles; Crossref sometimes puts the number in 'page'
    if rec.get("number") and rec.get("page"): del rec["page"]  # an article with an article number has no page range to print (APA 7: "Article 390")
    if rec.get("issue") and re.search(r"[a-z]{3}\d", rec["issue"]): del rec["issue"]  # BMJ's Crossref 'issue' is a date code ("jun10 9"), not an issue
    if re.fullmatch(r"[a-z]\d+", rec.get("page", "")) and not rec.get("number"): rec["number"] = rec.pop("page")  # an e-locator (BMJ h2698, e536): APA prints "Article h2698"
    if online and online != yr: rec["verification"]["online_first_year"] = int(online)
    upd = [u for u in cr.get("upd", []) if not u.startswith("to:")]
    if any("retraction" in u for u in upd):
        rec["verification"]["retraction_check"] = {"status": "retracted", "checked_on": TODAY, "note": "Crossref lists a retraction notice for this DOI."}
        # APA 7: the retraction goes in parentheses after the DOI, from the notice's own Crossref record when it is cached
        global _CACHE
        _CACHE = _CACHE if _CACHE is not None else load_cache()
        for u in upd:
            if u.startswith("retraction:") and _CACHE.get(u.split(":", 1)[1].lower()):
                n = _CACHE[u.split(":", 1)[1].lower()]
                pg = n.get("pg") or ""
                rec["retraction_notice"] = {"DOI": n["DOI"], "year": int((n.get("print") or n.get("issued") or n.get("online"))[0]), "container-title": clean(n.get("ct", "")),
                                            "volume": n.get("vol"), "issue": n.get("iss"), "page": pg.split("-")[0] if re.fullmatch(r"(\w+)-\1", pg) else pg}
                break
    elif any("concern" in u for u in upd):
        rec["verification"]["retraction_check"] = {"status": "expression-of-concern", "checked_on": TODAY}
    elif any("correct" in u or "erratum" in u for u in upd):
        rec["verification"]["retraction_check"] = {"status": "correction", "checked_on": TODAY, "note": "Crossref lists a correction; read it with the paper."}
    if ov:
        rec["verification"]["metadata_corrections"] = {"note": ov["note"], "source": ov.get("source", "")}
    if where.startswith("PMC"):
        rec["PMCID"] = where
    elif where.startswith("pdf:"):
        rec["verification"]["pdf_path"] = where[4:]
    return rec

def retitle():
    """--retitle: recompute the sentence-case title of every existing record from its Crossref cache entry (and any
    documented override), after a change to the casing rules. Prints each change; touches no other field."""
    cache = load_cache(); n = 0
    for f in sorted(glob.glob(str(ROOT / "data" / "references" / "*.json"))):
        cur = json.load(open(f, encoding="utf-8")); changed = False
        for r in cur:
            cr = cache.get((r.get("DOI") or "").lower())
            if not cr: continue
            ov = OVERRIDES.get(cr["DOI"].lower())
            merged = {**cr, **{k: v for k, v in (ov or {}).items() if k not in ("note", "source")}}
            raw = merged.get("title") if (ov or {}).get("title") else full_title(merged)
            t = (ov or {}).get("title_apa") or sentence_case(clean(raw))
            if t != r["title"]:
                print(f"  {r['id']}: {r['title']!r} -> {t!r}"); r["title"] = t; changed = True; n += 1
        if changed:
            pathlib.Path(f).write_text(json.dumps(cur, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"retitled {n} records")

def main():
    if "--retitle" in sys.argv:
        return retitle()
    cache = load_cache()
    pairs = []  # (substance, id, doi, where)
    for f in sorted(glob.glob(str(ROOT / "data" / "references" / "_incoming" / "*.txt"))):
        sub = pathlib.Path(f).stem
        for line in pathlib.Path(f).read_text(encoding="utf-8").splitlines():
            if line.strip() and not line.startswith("#"):
                parts = line.strip().split(">")
                pairs.append((sub, parts[0], parts[1], parts[2] if len(parts) > 2 else ""))
    for arg in sys.argv[1:]:
        sub, rest = arg.split(":", 1) if ":" in arg.split("=")[0] else ("methamphetamine", arg)
        rid, rhs = rest.split("=", 1)
        doi, where = (rhs.split("@", 1) + [""])[:2]
        pairs.append((sub, rid, doi, where))
    existing = {}
    for f in glob.glob(str(ROOT / "data" / "references" / "*.json")):
        for r in json.load(open(f, encoding="utf-8")):
            existing[r["id"]] = r.get("DOI", "").lower()
    missing, added, clashes, enriched = [], 0, [], []
    by_sub = {}
    for sub, rid, doi, where in pairs:
        if rid in existing:
            if existing[rid] and existing[rid] != doi.lower():
                clashes.append(f"{rid}: existing DOI {existing[rid]} ≠ {doi}")
            elif where.startswith("PMC"):
                enriched.append((rid, where))
            continue
        hold = (OVERRIDES.get(doi.lower()) or {}).get("hold")
        if hold:
            missing.append(f"{doi} (held: {hold})"); continue
        cr = cache.get(doi.lower())
        if not cr:
            missing.append(doi); continue
        if cr.get("error"):
            missing.append(doi + " (Crossref error)"); continue
        by_sub.setdefault(sub, []).append(record(rid, cr, where))
        existing[rid] = doi.lower(); added += 1
    if enriched:  # add a PMCID to an existing record that lacks one; nothing else is touched
        want = dict(enriched)
        for f in glob.glob(str(ROOT / "data" / "references" / "*.json")):
            cur = json.load(open(f, encoding="utf-8")); changed = False
            for r in cur:
                if r["id"] in want and not r.get("PMCID"):
                    r["PMCID"] = want[r["id"]]; changed = True
                    print(f"  PMCID {want[r['id']]} added to {r['id']}")
            if changed:
                pathlib.Path(f).write_text(json.dumps(cur, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    for sub, recs in by_sub.items():
        p = ROOT / "data" / "references" / f"{sub}.json"
        cur = json.load(open(p, encoding="utf-8")) if p.exists() else []
        cur += recs
        p.write_text(json.dumps(cur, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"added {added} references; missing from Crossref cache: {len(missing)}")
    for m in missing: print("  MISSING", m)
    for c in clashes: print("  CLASH", c)

if __name__ == "__main__":
    main()
