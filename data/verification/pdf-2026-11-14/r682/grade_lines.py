"""Reading grade of plain lines, using the same rough Flesch-Kincaid formula as site/build.js.
Usage: python3 -I grade_lines.py <simple.json>"""
import json, re, sys


def syl(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    m = re.findall(r"[aeiouy]{1,2}", w)
    return len(m) if m else 1


def grade(t):
    words = [x for x in t.split() if x]
    sents = max(1, len(re.findall(r"[.!?]+", t)))
    sy = sum(syl(w) for w in words)
    return 0.39 * len(words) / sents + 11.8 * sy / len(words) - 15.59


d = json.load(open(sys.argv[1], encoding="utf-8"))
for cid, c in d["claims"].items():
    print(cid, "| q words", len(c["q"].split()), "| short words", len(c["short"].split()), "| rate words", len(c["rate"].split()))
    for k in ("short", "but"):
        g = grade(c[k]); print(f"  {k:5s} {g:4.1f} {'OVER 6' if g > 6 else ''}")
    for i, t in enumerate(c["how"]):
        g = grade(t); print(f"  how[{i}] {g:4.1f} {'OVER 8' if g > 8 else ''}")
for slug, lst in d["tf"].items():
    for i, x in enumerate(lst):
        g = grade(x["statement"]); print(f"tf.{slug}[{i}] {g:4.1f} {'OVER 6' if g > 6 else ''} | words {len(x['statement'].split())} | {x['claim']}")
