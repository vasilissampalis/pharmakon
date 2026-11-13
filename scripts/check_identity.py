#!/usr/bin/env python3
"""Check identity files before they enter data/identity/ (METHODS §10.3): schema, sources, CAS check digits, formula
against molar mass, quotation length and wording. The same checks run in validate.py on the merged files.

Usage: check_identity.py FILE.json [FILE.json ...]     (exit code 1 on any failure)
"""
import json, re, sys, pathlib
import jsonschema

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCHEMA = json.load(open(ROOT / "schema" / "identity.schema.json", encoding="utf-8"))
CAS_RN = re.compile(r"(?<![\d-])(\d{2,7})-(\d{2})-(\d)(?![\d-])")
QUOTE = re.compile(r"(?<![A-Za-z])'[^']*'(?![A-Za-z])|\"[^\"]*\"|“[^”]*”")
ATOMIC = {"C": 12.011, "H": 1.008, "N": 14.007, "O": 15.999, "P": 30.974, "Cl": 35.45, "S": 32.06, "Na": 22.990, "Br": 79.904,
          "F": 18.998, "He": 4.0026, "Si": 28.085, "B": 10.81, "I": 126.904, "K": 39.098}


def mass(formula):
    tot = 0.0
    for el, k in re.findall(r"([A-Z][a-z]?)(\d*)", formula):
        if el not in ATOMIC: return None
        tot += ATOMIC[el] * (int(k) if k else 1)
    return tot


def cas_ok(a, b, c):
    return sum((j + 1) * int(x) for j, x in enumerate((a + b)[::-1])) % 10 == int(c)


def strings(o, at=""):
    if isinstance(o, dict):
        for k, v in o.items(): yield from strings(v, f"{at}/{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from strings(v, f"{at}[{i}]")
    elif isinstance(o, str): yield at, o


def check(path):
    d = json.load(open(path, encoding="utf-8")); fails, warns = [], []
    for e in jsonschema.Draft202012Validator(SCHEMA).iter_errors(d):
        fails.append(f"schema /{'/'.join(map(str, e.path))}: {e.message[:140]}")
    sid = {s["id"] for s in d.get("sources", [])}
    used = set(d.get("names", {}).get("source_ids", []))
    for k in ("members", "forms", "street_names", "drug_checking"):
        for x in d.get(k, []): used |= set(x.get("source_ids", []))
    fails += [f"source id {i} is not in sources" for i in sorted(used - sid)]
    warns += [f"source {i} is listed but supports nothing (pages not read belong in the log, not in sources)" for i in sorted(sid - used)]
    blocks = [("names", d.get("names", {}))] + [(f"members[{i}] {m.get('name', '')}", m) for i, m in enumerate(d.get("members", []))]
    texts = [x.get("detail", "") for x in d.get("forms", [])]
    for label, b in blocks:
        for t in b.get("cas", []) or []:
            for a, b2, c in CAS_RN.findall(QUOTE.sub(" ", t)):
                if not cas_ok(a, b2, c): fails.append(f"{label}: CAS {a}-{b2}-{c} fails its check digit")
        fm = re.match(r"\s*([A-Z][A-Za-z0-9]*)", b.get("formula", "") or ""); mm = re.match(r"\s*(\d+(?:\.\d+)?)", b.get("molar_mass", "") or "")
        if fm and mm:
            m = mass(fm.group(1))
            if m is None or abs(m - float(mm.group(1))) > 0.05:
                warns.append(f"{label}: molar mass {mm.group(1)} does not match formula {fm.group(1)} (computed {m and round(m, 3)})")
    for t in texts:
        for a, b2, c in CAS_RN.findall(QUOTE.sub(" ", t)):
            if not cas_ok(a, b2, c): fails.append(f"forms: CAS {a}-{b2}-{c} fails its check digit")
    for at, t in strings({k: v for k, v in d.items() if k != "sources"}):
        for q in re.findall(r"'([^']{2,})'|\"([^\"]{2,})\"|“([^”]{2,})”", t):
            q = next(x for x in q if x)
            if len(q.split()) > 15: fails.append(f"{at}: quotation of {len(q.split())} words (limit 15)")
        if re.search(r"\b(non-)?users?\b|\babusers?\b|\baddicts?\b", QUOTE.sub(" ", t), re.I):
            warns.append(f"{at}: wording ('user', 'abuser' or 'addict'; METHODS §9)")
        if re.search(r"\b\d+(\.\d+)?\s?(mg|µg|mcg|g|ml|mL)\b(?!/mol)", t) and not any(k in at for k in ("/forms", "/members", "molar_mass")):
            warns.append(f"{at}: an amount appears; identity sections carry no dosing (check it is a product or seizure size)")
    return d.get("substance", path), fails, warns


def main():
    bad = 0
    for p in sys.argv[1:]:
        name, fails, warns = check(p)
        print(f"{name}: {'OK' if not fails else 'FAIL'} ({len(fails)} failures, {len(warns)} warnings)")
        for f in fails: print("  FAIL", f)
        for w in warns: print("  WARN", w)
        bad += bool(fails)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
