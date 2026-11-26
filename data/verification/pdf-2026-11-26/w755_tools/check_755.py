"""Checks for claim writer 755's files: the validator's claim rules, quotation limits, words, and reading grades (site/build.js
formula). Run from the repository root: python3 -I data/verification/pdf-2026-11-26/w755_tools/check_755.py"""
import json, re

claims = json.load(open("data/claims/_incoming/pdf1126_w755.json"))
simple = json.load(open("data/verification/pdf-2026-11-26/755_simple.json"))
cards = {}
for cid, path in [("sc_wood_2015", "lsd/sc_wood_2015"), ("sc_brunetti_2021", "benzodiazepines/sc_brunetti_2021"),
                  ("sc_carpenter_2019", "benzodiazepines/sc_carpenter_2019")]:
    cards[cid] = json.load(open(f"data/study-cards/_incoming/{path}.json"))
refs = {r["id"] for f in ["data/references/other-drugs.json"] for r in json.load(open(f))}
problems = []
lv = ["very-low", "low", "moderate", "high"]
for c in claims:
    g = c["grade"]; d = g["domains"]
    down = sum(d[k]["levels"] for k in ("risk_of_bias", "inconsistency", "indirectness", "imprecision", "publication_bias"))
    up = sum(d.get(k, {"levels": 0})["levels"] for k in ("large_effect", "dose_response", "plausible_confounding"))
    exp = lv[max(0, min(3, (3 if g["starting_level"] == "high" else 1) - down + up))]
    if exp != g["certainty"]: problems.append(f"{c['id']} GRADE {exp} != {g['certainty']}")
    quotes = [e["quote"] for e in c["evidence"] if e.get("quote")]
    if len(quotes) > 1: problems.append(f"{c['id']} more than one quote")
    for q in quotes:
        if len(q.split()) > 15: problems.append(f"{c['id']} long quote")
    for e in c["evidence"]:
        if e["reference"] not in refs: problems.append(f"{c['id']} unknown ref {e['reference']}")
        if e["study_card"] not in cards: problems.append(f"{c['id']} unknown card {e['study_card']}")
    sup = [e for e in c["evidence"] if e["role"] == "supports"]
    narrative_only = all(cards[e["study_card"]]["design"] in ("narrative-review", "commentary", "editorial") for e in sup)
    if narrative_only:
        if c["verification"]["status"] != "draft": problems.append(f"{c['id']} narrative-only but not draft")
        if not any(w in c["statement"] for w in ("narrative review", "second-hand", "as summarized", "as described")):
            problems.append(f"{c['id']} narrative-only, statement silent")
    fields = [c.get(f) or "" for f in ("statement", "plain", "magnitude", "population", "exposure", "comparator", "outcome")]
    fields += [g["reasoning"]] + [e["extracted"] for e in c["evidence"]] + [v.get("note", "") for v in d.values()]
    for t in fields:
        low = t.lower()
        for term in ("addict", "abuser", "junkie", "clean urine", "dirty urine", "harmless", "devastating"):
            if term in low: problems.append(f"{c['id']} uses {term}")
        if re.search(r"\bcl_[a-z]+_\w+", t): problems.append(f"{c['id']} raw claim id")
        unq = re.sub(r"'[^']*'|\"[^\"]*\"|‘[^’]*’|“[^”]*”", "", low)
        if re.search(r"\b(non-)?users?\b", unq): problems.append(f"{c['id']} 'user(s)': ...{t[max(0, low.find('user') - 40):low.find('user') + 20]}")
    print(c["id"], "narrative-only" if narrative_only else "not narrative-only", "| anchors", len(c["evidence"]),
          "| statement words", len(c["statement"].split()), "| plain words", len(c["plain"].split()))


def syl(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    if not w: return 0
    if len(w) <= 3: return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    m = re.findall(r"[aeiouy]{1,2}", w)
    return len(m) if m else 1


def grade(t):
    words = [x for x in t.split() if x]
    sents = max(1, len(re.findall(r"[.!?]+", t)))
    sy = sum(syl(w) for w in words)
    return 0.39 * len(words) / sents + 11.8 * sy / len(words) - 15.59


for cid, s in simple["claims"].items():
    ver = next(c["version"] for c in claims if c["id"] == cid)
    if s["v"] != ver: problems.append(f"{cid} simple v {s['v']} != {ver}")
    if len(s["q"].split()) > 12: problems.append(f"{cid} q too long")
    if len(s["how"]) != len(s["how_src"]) or not (2 <= len(s["how"]) <= 4): problems.append(f"{cid} how/how_src")
    evref = {e["reference"] for e in next(c for c in claims if c["id"] == cid)["evidence"]}
    for l in s["how_src"]:
        if any(r not in evref for r in l): problems.append(f"{cid} how_src not in evidence")
    print(f"{cid}: q {len(s['q'].split())} words; short {len(s['short'].split())} words, grade {grade(s['short']):.1f}; "
          f"but grade {grade(s['but']):.1f}; how grades {[round(grade(h), 1) for h in s['how']]}; rate {len(s['rate'].split())} words")
    for k in ("short", "but", "rate", "q"):
        low = re.sub(r"'[^']*'", "", s[k].lower())
        if re.search(r"\b(non-)?users?\b", low): problems.append(f"{cid}.{k} user(s)")
for page, items in simple["tf"].items():
    for i, x in enumerate(items):
        print(f"tf {page}[{i}] grade {grade(x['statement']):.1f}, {len(x['statement'].split())} words: {x['statement']}")
        if x["v"] != next(c["version"] for c in claims if c["id"] == x["claim"]): problems.append("tf version")
print("PROBLEMS:", problems or "none")
