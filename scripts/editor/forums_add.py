#!/usr/bin/env python3
"""Merge a batch of coded forum questions into data/verification/questions-2026-11-14/forums.json.

Usage:  python3 -I scripts/editor/forums_add.py BATCH.json      (merge and validate)
        python3 -I scripts/editor/forums_add.py --stats         (counts per site and theme)

A batch is {"sources": [...], "questions": [...]} as in BRIEF-forums.md, with two shorthands:
- "theme": "T<n>" is the n-th of the 58 Reddit themes (rank order in reddit-themes.json);
  "N<n>" is a new theme registered in NEW_THEMES below; a full exact name is also accepted.
- "drugs": page slugs, or "<name> (no page yet)".
Questions are de-duplicated on (site, title_short, views). Unknown themes, slugs or claim ids stop the merge.

A batch may also be a rows file (*.txt), one listing page after another:
    @site Bluelight
    @page https://...            (starts a new source page)
    @sorted_by views, descending
    title | views | replies | theme | drug1, drug2 | question | claim1, claim2
    - title | views | replies     (seen on the page, no question: counted in posts_seen only)
Views and replies may be written as shown (2M, 763K, 1K) or "null"; a "#" line is a comment.
"""
import json
import os
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "data/verification/questions-2026-11-14/forums.json")
THEMES = os.path.join(ROOT, "data/verification/questions-2026-11-13/reddit-themes.json")
ANSWERS = os.path.join(ROOT, "data/verification/questions-2026-11-13/existing_answers.json")
SUBST = os.path.join(ROOT, "data/site/substances.json")

# New themes (not among the 58 Reddit themes). Reuse these names consistently.
NEW_THEMES = {
    "N1": "Can prescription or over-the-counter medicines get you high, and what are the risks?",
    "N2": "How long does a drug stay in your body, and how long can a test find it?",
    "N3": "What does this drug feel like, and how long does it last?",
    "N4": "How do methadone and buprenorphine (Suboxone) work, and what happens if other opioids are used with them?",
    "N5": "What long-term harm does regular use do to the body (heart, liver, teeth, nose, bladder)?",
    "N6": "What is withdrawal from stimulants, cannabis, gabapentinoids or other drugs like, and how long does it last?",
    "N7": "How can people who inject, smoke or snort drugs avoid infections and damage to veins, lungs and nose?",
    "N8": "What are 'research chemicals' and legal highs (phenibut, etizolam, synthetic drugs), and how risky are they?",
    "N9": "Is it safe to use drugs with a health condition or while pregnant or breastfeeding?",
    "N10": "What do anabolic steroids and other image-enhancing drugs do, and how risky are they?",
    "N11": "How do I stop or cut down, and is it safe to taper on my own?",
    "N12": "Why did a drug not work, feel weak or feel different this time?",
    "N13": "Where can I find harm reduction help: drug checking, clean needles, naloxone or a safe place to use?",
    "N14": "Why does a drug cause this side effect (stomach, bladder, sleep, skin, sweating), and is it a danger sign?",
    "N15": "Which medicine works better for anxiety, depression, sleep, pain or ADHD?",
    "N16": "Can stimulants help you lose weight, and is it safe?",
}


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def num(s):
    s = s.strip().replace(",", "")
    if s.lower() in ("null", "none", ""):
        return None
    mult = 1
    if s[-1] in "kK":
        mult, s = 1000, s[:-1]
    elif s[-1] in "mM":
        mult, s = 1000000, s[:-1]
    return int(round(float(s) * mult))


def parse_rows(path, fetched_on="2026-11-14"):
    sources, questions = [], []
    site = sorted_by = None
    cur = None
    with open(path, encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            line = line.rstrip("\n")
            if not line.strip() or line.startswith("#"):
                continue
            if line.startswith("@site "):
                site = line[6:].strip()
            elif line.startswith("@sorted_by "):
                sorted_by = line[11:].strip()
                if cur is not None:
                    cur["sorted_by"] = sorted_by
            elif line.startswith("@page "):
                cur = {"site": site, "page": line[6:].strip(), "sorted_by": sorted_by,
                       "fetched_on": fetched_on, "posts_seen": 0, "with_question": 0}
                sources.append(cur)
            elif line.startswith("- "):
                parts = [p.strip() for p in line[2:].split(" | ")]
                if len(parts) != 3:
                    sys.exit("line %d: skipped row needs title | views | replies" % ln)
                cur["posts_seen"] += 1
            else:
                parts = [p.strip() for p in line.split(" | ")]
                if len(parts) != 7:
                    sys.exit("line %d: row needs 7 fields, has %d: %s" % (ln, len(parts), line))
                title, views, replies, theme, drugs, question, covered = parts
                cur["posts_seen"] += 1
                cur["with_question"] += 1
                questions.append({
                    "site": site, "page": cur["page"], "title_short": title,
                    "views": num(views), "replies": num(replies),
                    "drugs": [d.strip() for d in drugs.split(",") if d.strip()],
                    "question": question, "theme": theme,
                    "covered_by": [c.strip() for c in covered.split(",") if c.strip() and c.strip() != "-"],
                })
    return {"sources": sources, "questions": questions}


def main():
    themes = [t["theme"] for t in load(THEMES)["themes"]]
    claim_ids = {a["id"] for a in load(ANSWERS)}
    slugs = {s["slug"] for s in load(SUBST)} | {a["page"] for a in load(ANSWERS)}
    if os.path.exists(OUT):
        data = load(OUT)
    else:
        data = {"sources": [], "questions": []}

    if sys.argv[1:] == ["--stats"]:
        stats(data, themes)
        return

    batch = parse_rows(sys.argv[1]) if sys.argv[1].endswith(".txt") else load(sys.argv[1])
    errors = []
    added_q = 0
    seen = {(q["site"], q["title_short"], q["views"]) for q in data["questions"]}
    for q in batch.get("questions", []):
        t = q["theme"]
        if t.startswith("T") and t[1:].isdigit():
            q["theme"] = themes[int(t[1:]) - 1]
        elif t in NEW_THEMES:
            q["theme"] = NEW_THEMES[t]
        elif t not in themes and t not in NEW_THEMES.values():
            errors.append("unknown theme: %r (%s)" % (t, q["title_short"]))
        for d in q["drugs"]:
            if d not in slugs and not d.endswith("(no page yet)"):
                errors.append("unknown slug: %r (%s)" % (d, q["title_short"]))
        for c in q["covered_by"]:
            if c not in claim_ids:
                errors.append("unknown claim id: %r (%s)" % (c, q["title_short"]))
        for k in ("site", "page", "title_short", "views", "replies", "drugs", "question", "theme", "covered_by"):
            if k not in q:
                errors.append("missing %s (%s)" % (k, q.get("title_short")))
        words = [w for w in q["title_short"].split() if any(ch.isalnum() for ch in w)]
        if len(words) > 15 and "(paraphrase)" not in q["title_short"]:
            errors.append("title over 15 words, not marked paraphrase: %s" % q["title_short"])
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    keys = ("site", "page", "title_short", "views", "replies", "drugs", "question", "theme", "covered_by")
    for q in batch.get("questions", []):
        k = (q["site"], q["title_short"], q["views"])
        if k in seen:
            continue
        seen.add(k)
        data["questions"].append({key: q[key] for key in keys})
        added_q += 1
    src_seen = {(s["site"], s["page"]) for s in data["sources"]}
    for s in batch.get("sources", []):
        if (s["site"], s["page"]) not in src_seen:
            data["sources"].append(s)
            src_seen.add((s["site"], s["page"]))
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("added %d questions; total %d questions, %d source pages" % (added_q, len(data["questions"]), len(data["sources"])))


def stats(data, themes):
    by_site = Counter(q["site"] for q in data["questions"])
    seen_site = defaultdict(lambda: [0, 0])
    for s in data["sources"]:
        seen_site[s["site"]][0] += s["posts_seen"]
        seen_site[s["site"]][1] += s["with_question"]
    print("questions per site:")
    for site, n in by_site.most_common():
        print("  %-22s %4d   (pages %d, posts seen %d, with question %d)" % (
            site, n, sum(1 for s in data["sources"] if s["site"] == site), seen_site[site][0], seen_site[site][1]))
    print("total", len(data["questions"]))
    agg = defaultdict(lambda: {"n": 0, "views": 0, "sites": Counter(), "uncovered": 0})
    for q in data["questions"]:
        a = agg[q["theme"]]
        a["n"] += 1
        a["views"] += q["views"] or 0
        a["sites"][q["site"]] += 1
        if not q["covered_by"]:
            a["uncovered"] += 1
    print("\nthemes by questions (views):")
    for t, a in sorted(agg.items(), key=lambda x: (-x[1]["n"], -x[1]["views"])):
        tag = ("T%d" % (themes.index(t) + 1)) if t in themes else [k for k, v in NEW_THEMES.items() if v == t][0]
        print("  %-4s %3d q  %9d views  uncovered %3d  %s | %s" % (
            tag, a["n"], a["views"], a["uncovered"], t[:70], dict(a["sites"])))


if __name__ == "__main__":
    main()
