"""apa_from_cache.py DOI [DOI ...]: APA 7 references (with *italics* marks) built from the cached Crossref records
(data/access/crossref-cache.jsonl) and documented overrides, with the same title casing as scripts/build_references.py.
Used for the senior author's list of papers to save; nothing here is typed by hand."""
import sys, json, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import build_references as br
cache = br.load_cache()
import glob as _g
RECORDS = {}
for _f in _g.glob(str(ROOT / "data" / "references" / "*.json")):
    for _r in json.load(open(_f, encoding="utf-8")):
        if _r.get("DOI"): RECORDS[_r["DOI"].lower()] = _r
def initials(given):
    parts = re.split(r"\s+", (given or "").replace(".", ". ").strip())
    out = []
    for p in parts:
        if not p: continue
        if "-" in p or "‐" in p:
            out.append("-".join(q[0] + "." for q in re.split(r"[-‐]", p) if q))
        elif re.fullmatch(r"[A-Z]+", p) and len(p) <= 3:
            out.extend(c + "." for c in p)
        else:
            out.append(p[0] + ".")
    return " ".join(out)
def authors(au):
    names = []
    for a in au:
        a = [br.HY(x) for x in a]
        names.append(a[0] if len(a) == 1 else f"{a[0]}, {initials(a[1])}")
    if len(names) == 1: return names[0]
    if len(names) <= 20: return ", ".join(names[:-1]) + ", & " + names[-1]
    return ", ".join(names[:19]) + ", . . . " + names[-1]
def apa(doi):
    cr = cache[doi.lower()]
    ov = br.OVERRIDES.get(doi.lower())
    if ov: cr = {**cr, **{k: v for k, v in ov.items() if k not in ("note", "source", "hold")}}
    yr = (cr.get("print") or cr.get("issued") or cr.get("online"))[0]
    title = cr.get("title_apa") or br.sentence_case(br.clean(br.full_title(cr)))
    ct = br.clean(cr.get("ct", ""))
    vol, iss, pg, num = cr.get("vol"), cr.get("iss"), cr.get("pg"), cr.get("number")
    tail = f"*{ct}*"
    if vol: tail += f", *{vol}*" + (f"({iss})" if iss else "")
    if num and (not pg or pg == num): tail += f", Article {num}"
    elif pg and re.fullmatch(r"[a-z]\d+", pg): tail += f", Article {pg}"
    elif pg: tail += ", " + pg.replace("-", "–")
    rec = RECORDS.get(doi.lower())   # an existing reference record may carry documented author corrections
    au = [[x.get("family") or x.get("literal"), x.get("given")] if x.get("given") else [x.get("family") or x.get("literal")] for x in rec["author"]] if rec else cr["au"]
    return f"{authors(au)} ({yr}). {title}{'' if title.endswith(('?', '!')) else '.'} {tail}. https://doi.org/{cr['DOI']}"
if __name__ == "__main__":
    for d in sys.argv[1:]: print(apa(d))
