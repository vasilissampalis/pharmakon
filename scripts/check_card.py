#!/usr/bin/env python3
"""Check one or more study-card files before they are merged (METHODS §5).

Usage: python3 -I scripts/check_card.py data/study-cards/_incoming/<substance>/<card>.json [...]
Hard failures: schema errors, placeholders left in required fields, key findings without a page,
quotations longer than 15 words, card id / file name mismatch.
Warnings: replication-timeline references that do not exist yet, stigmatizing terms outside titles.
Exit code 1 if any file fails.
"""
import json, sys, re, glob, pathlib
import jsonschema
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from rob_vocab import problems as rob_problems

ROOT = pathlib.Path(__file__).resolve().parents[1]
schema = json.load(open(ROOT / "schema" / "study-card.schema.json", encoding="utf-8"))
V = jsonschema.Draft202012Validator(schema)
ref_ids = set()
for f in glob.glob(str(ROOT / "data" / "references" / "*.json")):
    ref_ids |= {r["id"] for r in json.load(open(f, encoding="utf-8"))}
QUOTE = re.compile(r"[\"“]([^\"“”]{20,}?)[\"”]|(?<![A-Za-z])'([^']{20,}?)'(?![A-Za-z])")
STIGMA = re.compile(r"\b(abusers?|addicts?|junkies?)\b", re.I)
USERS = re.compile(r"\b(non-)?users?\b", re.I)

def walk(x, path=""):
    if isinstance(x, dict):
        for k, v in x.items(): yield from walk(v, f"{path}/{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x): yield from walk(v, f"{path}/{i}")
    elif isinstance(x, str):
        yield path, x

def check(fp):
    try:
        card = json.load(open(fp, encoding="utf-8"))
    except Exception as e:
        return [f"not valid JSON: {e}"], []
    fails, warns = check_card(card)
    if pathlib.Path(fp).stem != card.get("id"):
        fails.append(f"file name {pathlib.Path(fp).stem} does not match card id {card.get('id')}")
    return fails, warns

def check_card(card):
    """The checks for one card object; used by check() for incoming files and by validate.py for merged cards."""
    fails, warns = [], []
    for e in V.iter_errors(card):
        fails.append(f"schema /{'/'.join(map(str, e.path))}: {e.message[:160]}")
    for pr in rob_problems(card):
        fails.append(f"risk of bias: {pr} (METHODS §5.3)")
    for path, s in walk(card):
        if "[to be" in s or "[?" in s or "[p. ?]" in s:
            fails.append(f"placeholder left at {path}: {s[:60]}")
        for m in QUOTE.finditer(s):
            q = m.group(1) or m.group(2)
            words = len(q.split())
            if words > 15:
                fails.append(f"quotation of {words} words at {path} (limit 15): {q[:60]}…")
        if USERS.search(s) and not path.endswith("/title"):
            m = USERS.search(s)
            warns.append(f"'user(s)' at {path}: write 'people who use…' or 'the methamphetamine group' (METHODS §9): …{s[max(0, m.start()-30):m.end()+10]}…")
        if STIGMA.search(s) and not path.endswith("/title"):
            warns.append(f"stigmatizing term at {path} (allowed only inside quoted titles, instrument or programme names): …{s[max(0, STIGMA.search(s).start()-30):STIGMA.search(s).end()+10]}…")
    for kf in card.get("key_findings", []):
        if not kf.get("page") or kf["page"].strip() in ("", "-"):
            fails.append(f"key finding without page: {kf.get('finding', '')[:60]}")
    if not card.get("key_findings"):
        fails.append("no key_findings: every card must list its anchored results")
    for t in (card.get("replication", {}) or {}).get("timeline", []) or []:
        r = t.get("reference")
        if r and r not in ref_ids:
            warns.append(f"timeline reference '{r}' is not in data/references yet (create it or drop the id)")
    sr = card.get("verification", {}).get("source_read", "")
    if not sr:
        fails.append("verification.source_read missing: say what was read (PDF pages or PMC full text)")
    elif sr.lower().startswith("abstract") and card["verification"]["status"] != "draft":
        fails.append("a card written from an abstract must stay in draft")
    return fails, warns

if __name__ == "__main__":
    files = sys.argv[1:] or sorted(glob.glob(str(ROOT / "data" / "study-cards" / "_incoming" / "*" / "*.json")))
    bad = 0
    for fp in files:
        f, w = check(fp)
        status = "FAIL" if f else "ok"
        print(f"{status:4} {fp}")
        for x in f: print(f"     ✗ {x}")
        for x in w: print(f"     ! {x}")
        bad += bool(f)
    print(f"{len(files)} checked, {bad} failing")
    sys.exit(1 if bad else 0)
