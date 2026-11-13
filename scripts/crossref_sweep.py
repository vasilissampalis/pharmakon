#!/usr/bin/env python3
"""Independent Crossref sweep of every DOI in every evidence map (METHODS §4.2).

The lists are written by co-editors; this checks each row against Crossref: the DOI resolves, the first author's family
name, the second author's (when the list names two, "A & B"), the year (print issue, or online-first), the title (word
overlap), and Crossref's update links (retraction, correction, expression of concern).

  crossref_sweep.py fetch-list [N]   print a JSON array of up to N DOIs not yet in the sweep cache (for the browser)
  crossref_sweep.py add FILE         append compact Crossref records (one JSON object per line) to the cache
  crossref_sweep.py report           compare and write search-logs/_VERIFICATION-SWEEP_<date>.md

Cache: data/access/crossref-sweep.jsonl (same compact shape as crossref-cache.jsonl).
"""
import json, re, sys, pathlib, datetime, unicodedata
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from parse_lists import all_lists, ROOT

CACHE = ROOT / "data" / "access" / "crossref-sweep.jsonl"
TODAY = datetime.date.today().isoformat()

def fold(s):
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).lower().replace("’", "'")

def load_cache():
    out = {}
    for f in (CACHE, ROOT / "data" / "access" / "crossref-cache.jsonl"):
        if f.exists():
            for line in f.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    r = json.loads(line); out.setdefault(r["DOI"].lower(), r)
    return out

def rows():
    seen = {}
    for folder, t in all_lists().items():
        for tier in ("A", "B", "C"):
            for r in t[tier]:
                if r["doi"]:
                    seen.setdefault(r["doi"].lower(), dict(r, folder=folder, tier=tier))
    return seen

def list_authors(paper):
    head = paper.split(" — ")[0].split(" - ")[0]
    head = re.sub(r"\bet al\.?", "", head)
    parts = [p.strip(" ,.") for p in re.split(r",|&|\band\b", head) if p.strip(" ,.")]
    return parts

def list_year(r):
    for src in (r.get("venue", ""), r.get("save_as", "")):
        m = re.findall(r"(?<!\d)(19[5-9]\d|20[0-3]\d)(?!\d)", src)
        if m:
            return int(m[-1]) if src is r.get("venue", "") else int(m[0])
    return None

STOP = set("a an the of and in on for with to by at from vs versus or is are was were its their among after during".split())
def title_words(t):
    return set(w for w in re.findall(r"[a-z0-9]+", fold(t)) if w not in STOP and len(w) > 2)

def compare(r, cr):
    issues = []
    la = list_authors(r["paper"])
    au = [fold(a[0]) for a in cr.get("au", []) if a and a[0]]
    if la and au:
        first = fold(la[0]).split()[-1] if la[0] else ""
        if first and not any(first in a or a in first for a in au[:1]):
            # group authors listed first in Crossref are common; accept a match anywhere in the first three
            if not any(first in a for a in au[:3]):
                issues.append(f"first author: list '{la[0]}', Crossref '{cr['au'][0][0]}'")
        if len(la) >= 2 and len(au) >= 2 and "et al" not in r["paper"].split(" — ")[0]:
            second = fold(la[1]).split()[-1]
            if second and not any(second in a for a in au[1:3]):
                issues.append(f"second author: list '{la[1]}', Crossref '{cr['au'][1][0]}'")
    y = list_year(r)
    years = {v[0] for v in (cr.get("print"), cr.get("online"), cr.get("issued")) if v}
    if y and years and y not in years:
        issues.append(f"year: list {y}, Crossref {sorted(years)}")
    tw = title_words(r["paper"].split(" — ", 1)[1] if " — " in r["paper"] else r["paper"])
    cw = title_words(cr.get("title", ""))
    if tw and cw:
        overlap = len(tw & cw) / max(1, min(len(tw), len(cw)))
        if overlap < 0.5:
            issues.append(f"title: low word overlap ({overlap:.2f}) with Crossref '{cr.get('title','')[:90]}'")
    upd = [u for u in cr.get("upd", []) if not u.startswith("to:")]
    return issues, upd

def main():
    cmd = sys.argv[1]
    if cmd == "fetch-list":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 80
        cache = load_cache()
        todo = [d for d in rows() if d not in cache]
        print(json.dumps(todo[:n])); print(f"# {len(todo)} DOIs not yet fetched", file=sys.stderr)
    elif cmd == "add":
        have = set(load_cache())
        n = 0
        with open(CACHE, "a", encoding="utf-8") as f:
            for line in open(sys.argv[2], encoding="utf-8"):
                line = line.strip()
                if not line: continue
                r = json.loads(line)
                if r.get("DOI", "").lower() in have and not r.get("error"): continue
                f.write(json.dumps(r, ensure_ascii=False) + "\n"); n += 1
        print("added", n)
    elif cmd == "report":
        cache = load_cache(); R = rows()
        unresolved, flagged, retracted, corrected = [], [], [], []
        for d, r in R.items():
            cr = cache.get(d)
            if not cr:
                unresolved.append((d, r, "not fetched")); continue
            if cr.get("error"):
                unresolved.append((d, r, f"Crossref error {cr['error']}")); continue
            issues, upd = compare(r, cr)
            if any("retraction" in u for u in upd): retracted.append((d, r, upd))
            elif upd: corrected.append((d, r, upd))
            if issues: flagged.append((d, r, issues))
        lines = [f"# Independent DOI verification sweep — {TODAY}", "",
                 "Every DOI in every evidence map present on this date, checked against the Crossref record fetched through "
                 "the app's browser: resolution, first author, second author where the list names two, year (print issue or "
                 "online-first), title word overlap, and Crossref update links (retraction, correction, expression of concern).", "",
                 "| Check | Result |", "|---|---|",
                 f"| Distinct DOIs | {len(R)} |", f"| Resolved in Crossref | {len(R) - len(unresolved)} |",
                 f"| Retracted | **{len(retracted)}** |", f"| Corrections or notices linked | {len(corrected)} |",
                 f"| Rows with an author, year or title mismatch to check | {len(flagged)} |", ""]
        if retracted:
            lines += ["## Retracted", ""] + [f"- `{d}` · {r['folder']} · {r['paper']} · {', '.join(u)}" for d, r, u in retracted] + [""]
        if unresolved:
            lines += ["## Not resolved", ""] + [f"- `{d}` · {r['folder']} · {r['paper']} · {why}" for d, r, why in unresolved] + [""]
        if flagged:
            lines += ["## Mismatches to check (list text vs Crossref)", ""] + [f"- `{d}` · {r['folder']} · {r['paper'][:110]} — " + "; ".join(i) for d, r, i in flagged] + [""]
        if corrected:
            lines += ["## Corrections and notices linked in Crossref (obtain with the paper)", ""] + [f"- `{d}` · {r['folder']} · {r['paper'][:100]} · {', '.join(u)}" for d, r, u in corrected] + [""]
        out = ROOT / "search-logs" / f"_VERIFICATION-SWEEP_{TODAY}.md"
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("\n".join(lines[:14])); print("written", out)

if __name__ == "__main__":
    main()
