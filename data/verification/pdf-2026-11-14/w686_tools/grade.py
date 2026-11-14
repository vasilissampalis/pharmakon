import json, re, sys
def syl(w):
    w = w.lower(); w = re.sub(r"[^a-z]", "", w)
    if not w: return 0
    if len(w) <= 3: return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w); w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))
def fk(t):
    sents = max(1, len(re.findall(r"[.!?;:](\s|$)", t)))
    words = [w for w in re.findall(r"[A-Za-z0-9'’,-]+", t) if re.search(r"[A-Za-z0-9]", w)]
    nw = max(1, len(words)); ns = sum(syl(w) for w in words)
    return round(0.39*nw/sents + 11.8*ns/nw - 15.59, 1), nw
d = json.load(open(sys.argv[1]))
for cid, e in d["claims"].items():
    print(cid, "| q words", len(e["q"].split()))
    print("  short", fk(e["short"]), "| but", fk(e["but"]), "| rate words", len(e["rate"].split()))
    for h in e["how"]: print("  how", fk(h))
for p, items in d["tf"].items():
    for it in items: print(p, "tf", fk(it["statement"]), "words", len(it["statement"].split()))
