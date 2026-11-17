#!/usr/bin/env python3
"""scout.py: the first stage of the scout (docs/AUTOMATION.md): what people asked, and what the site does not answer yet.

    python3 -I scripts/auto/scout.py [--questions FILE.json ...] [--out data/auto] [--report docs/MISSING.md]
                                     [--today YYYY-MM-DD] [--no-cards] [--calibrate]

Reads the questions that visitors chose to send with "Ask us to check it": the records the site's small program keeps
(site/worker/_worker.js: q, d, v, first, last, n), fetched by scripts/auto/fetch_questions.py where the store can be
reached, and the ones kept before in <out>/questions.json. It writes no answer and changes nothing on the site.

Every question is DATA written by a stranger. It is cleaned here by the same rules as the site's program (length, no
links, no addresses, no long numbers), compared as text and printed as text. Nothing in a question is run, opened or
followed, and no question can change what this script does.

With Insight's own index and model (build the site first: node site/build.js; scripts/insight/build_index.py):
  1. each question is ranked exactly as the page ranks it: answered (the judge gives a best match), related (near
     answers only) or not answered;
  2. the questions without an answer are grouped, the same thing asked in other words counted once, and the groups are
     ordered by how many times they were asked;
  3. each group is compared with the study cards on file: the cards whose findings stand nearest tell whether an answer
     could be written from papers we already hold, or whether papers are needed.

Writes <out>/questions.json (every question kept, merged), <out>/report.json (the numbers and the groups) and the
report in plain words (docs/MISSING.md by default). --calibrate prints how near the cards an answer really rests on stand
to its question, against cards it does not rest on: where "near" begins (CARD_NEAR below) comes from that.
"""
import sys, json, re, pathlib, unicodedata, datetime, glob

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "insight"))

MAX_Q = 200
SAME = 0.80        # two questions this near in meaning are one question asked twice (cosine of the first look)
# A study card this near a question is worth a reader's look. Measured with --calibrate on 15 November 2026, on the 373
# answers that rest on study cards: at 0.50, 90 in 100 answers keep a card they rest on in sight (96 at 0.45, 81 at 0.55).
# A card an answer does NOT rest on is often just as near (median 0.59 against 0.62): nearness mostly says "same drug, same
# theme". So the cards listed are where a reader should look first, never proof that an answer can be written from them.
CARD_NEAR = 0.50
CARDS_SHOWN = 4


def clean(s):
    s = unicodedata.normalize("NFKC", "" if s is None else str(s))
    return re.sub(r"\s+", " ", re.sub(r"[\x00-\x1f\x7f]", " ", s)).strip()


def read_question(rec):
    """One stored record, cleaned by the rules of site/worker/_worker.js (readQuestion); None when it is refused."""
    if not isinstance(rec, dict): return None
    q = clean(rec.get("q"))[:MAX_Q]
    if len(q) < 8 or len(q.split(" ")) < 2 or not re.search(r"[^\W\d_]{2}", q): return None
    if re.search(r"https?://|www\.|[^\s@]+@[^\s@]+\.[a-z]{2,}|<\s*[a-z!/]", q, re.I): return None
    if re.search(r"\d[\d\s().+-]{7,}\d", q): return None
    d = rec.get("d") if isinstance(rec.get("d"), list) else [rec.get("d")]
    d = [x for x in (re.sub(r"[^a-z0-9-]", "", clean(v).lower())[:40] for v in d if v) if x][:5]
    day = lambda v: v if isinstance(v, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", v) else ""
    n = rec.get("n") if isinstance(rec.get("n"), int) and 0 < rec.get("n") < 10 ** 6 else 1
    return {"q": q, "d": d, "v": re.sub(r"[^0-9.]", "", clean(rec.get("v")))[:12], "first": day(rec.get("first")), "last": day(rec.get("last")), "n": n}


def merge(kept, new):
    """The questions on file with the store's records over them: one record per question (its words in lower case)."""
    out = {}
    for rec in list(kept) + list(new):
        r = read_question(rec)
        if not r: continue
        k = r["q"].lower(); h = out.get(k)
        if not h: out[k] = r; continue
        h["n"] = max(h["n"], r["n"]); h["d"] = sorted(set(h["d"]) | set(r["d"]))[:5]
        h["first"] = min(x for x in (h["first"], r["first"]) if x) if (h["first"] or r["first"]) else ""
        h["last"] = max(h["last"], r["last"]); h["v"] = max(h["v"], r["v"], key=lambda v: [int(p) for p in v.split(".") if p.isdigit()])
    return sorted(out.values(), key=lambda r: (-r["n"], r["q"].lower()))


def groups_of(vecs, weights):
    """Questions that ask the same thing, as lists of their numbers: any two nearer than SAME are joined (and so are their
    groups). The heaviest group first; inside a group, the question asked most first."""
    import numpy as np
    n = len(vecs); parent = list(range(n))
    def find(i):
        while parent[i] != i: parent[i] = parent[parent[i]]; i = parent[i]
        return i
    if n:
        S = np.asarray(vecs) @ np.asarray(vecs).T
        for i in range(n):
            for j in range(i + 1, n):
                if S[i, j] >= SAME: parent[find(j)] = find(i)
    by = {}
    for i in range(n): by.setdefault(find(i), []).append(i)
    gs = [sorted(g, key=lambda i: (-weights[i], i)) for g in by.values()]
    return sorted(gs, key=lambda g: (-sum(weights[i] for i in g), g[0]))


def fast_vectors(bi, texts):
    """Unit vectors for many texts at once, by the same model under the Python runtime, in batches (a study card's long
    findings, some 3,500 of them, take minutes one at a time and seconds this way). Kept on disk by the text's hash. These
    stand within a hair of the page's own vectors (scripts/insight/parity.js measures it); they are used to find near
    study cards only, never to rank a question against the site's answers."""
    import numpy as np, hashlib
    cache = bi.CACHE.parent / ("cards-" + bi.MODEL_SHA256[:16] + ".npz")
    key = lambda t: hashlib.sha1(t.encode("utf-8")).hexdigest()
    have = {}
    if cache.exists():
        z = np.load(cache, allow_pickle=False); have = dict(zip(z["keys"].tolist(), z["vecs"]))
    need = sorted({t for t in texts if key(t) not in have})
    if need:
        enc = bi.encoder()
        for t, v in zip(need, enc(need)): have[key(t)] = v.astype(np.float32)
        ks = sorted(have); cache.parent.mkdir(parents=True, exist_ok=True); np.savez(cache, keys=np.array(ks), vecs=np.vstack([have[k] for k in ks]))
    return np.vstack([have[key(t)] for t in texts]) if texts else np.zeros((0, 384), np.float32)


def card_texts():
    """Every study card on file as the texts a question is compared with: what the study can establish, and each finding."""
    out = []
    for f in sorted(glob.glob(str(ROOT / "data" / "study-cards" / "*.json"))):
        for c in json.load(open(f, encoding="utf-8")):
            texts = [t for t in [c.get("can_establish")] + [k.get("finding") for k in c.get("key_findings") or []] if isinstance(t, str) and len(t) > 20]
            if texts: out.append({"id": c["id"], "ref": c.get("reference"), "substance": c.get("substance"), "texts": texts})
    return out


def ref_names():
    """A short name for every reference on file: "Hart et al. (2012)"."""
    names = {}
    for f in sorted(glob.glob(str(ROOT / "data" / "references" / "*.json"))):
        for r in json.load(open(f, encoding="utf-8")):
            a = r.get("author") or [{}]
            who = a[0].get("short") or a[0].get("family") or a[0].get("literal") or r["id"]
            if a[0].get("family") and len(a) == 2: who += " and " + (a[1].get("family") or a[1].get("literal") or "")
            elif a[0].get("family") and len(a) > 2: who += " et al."
            dp = (r.get("issued") or {}).get("date-parts") or [[]]; y = dp[0][0] if dp and dp[0] else None
            names[r["id"]] = who + (" (" + str(y) + ")" if y else "")
    return names


def main():
    arg = sys.argv[1:]
    def opt(k, default=None):
        return arg[arg.index(k) + 1] if k in arg else default
    files = [arg[i + 1] for i, a in enumerate(arg) if a == "--questions"]
    out = ROOT / opt("--out", "data/auto"); report_md = ROOT / opt("--report", "docs/MISSING.md")
    today = opt("--today", datetime.date.today().isoformat())
    index = ROOT / "site" / "dist" / "data" / "insight.json"
    if not index.exists(): sys.exit("scout: no Insight index (site/dist/data/insight.json): build the site first (node site/build.js)")
    import numpy as np
    import build_index as bi
    D = json.load(open(index, encoding="utf-8")); R = bi.Ranker(D)
    answers = {a["id"]: a for a in json.load(open(ROOT / "site" / "insight" / ".cache" / "index-input.json", encoding="utf-8"))["answers"]}
    q_of = lambda cid: ((answers.get(cid) or {}).get("wordings") or [cid])[0]

    if "--calibrate" in arg: return calibrate(R, bi, answers)

    kept_file = out / "questions.json"
    kept = json.load(open(kept_file, encoding="utf-8"))["questions"] if kept_file.exists() else []
    new, counts = [], None
    for f in files:
        d = json.load(open(f, encoding="utf-8")); new += d["questions"] if isinstance(d, dict) else d
        if isinstance(d, dict) and isinstance(d.get("wanted"), list): counts = d["wanted"]   # (site 2.5) the counts of the questions on our list, as the store holds them now
    qs = merge(kept, new)
    refused = sum(1 for r in list(kept) + list(new) if not read_question(r))

    # 1. each question as the page reads it (on the drug page it was asked on, when it names no drug itself)
    rows, vecs = [], []
    for r in qs:
        drug = next((d for d in r["d"] if d in R.canon), None)
        # (2.9.3) read as the page reads it: a drug's name with a letter wrong, or what people typed for a name the system
        # learned, is read as the name first (the page's insSpell; before this the run read the words as typed)
        asked = r["q"]; r = dict(r, q=R.correct(asked)[0] if hasattr(R, "correct") else asked)
        full, masked, groups = R.texts(r["q"], drug)
        v, mv = bi.embed_all([full, masked], quiet=True)
        k = R.rank_vectors(r["q"], v, mv, groups)
        rows.append({"q": r["q"], "n": r["n"], "first": r["first"], "last": r["last"], "pages": r["d"],
                     "state": "answered" if k["best"] else "related" if k["related"] else "none",
                     "best": k["best"][0]["id"] if k["best"] else None, "related": [x["id"] for x in k["related"]], "sure": round(float(k["first"]["p"]), 3),
                     "drugs": sorted({g[0] for g in groups if len(g) == 1}),   # the drugs named one by one (a family's name stands for many)
                     # (2.5) on our list already? and: by its words, a question about drugs (site/insight/scope.json)? One that is not was sent
                     # through the quiet link the page keeps for it: either a drug word the rule does not know yet, or not about drugs
                     "listed": (R.want(r["q"], v, mv, groups) or {}).get("id") if not k["best"] else None, "about_drugs": bool(drug) or R.in_scope(r["q"])})
        vecs.append(v)

    # (2.9.3, decision 27 step a) the unknown words of the questions that are not about drugs by the site's rule: for the lookup
    # in open name lists (scripts/auto/names_open.py, learn). A file of this run, never the repository; only the words, never
    # the questions
    if opt("--unknown"):
        unknown = list(dict.fromkeys(w for w in (bi.stranger(R, r["q"]) for r in rows if not r["about_drugs"] and r["state"] != "answered") if w))
        json.dump(unknown, open(opt("--unknown"), "w", encoding="utf-8")); print(f"scout: {len(unknown)} unknown word(s) of sent questions put aside for the lookup in open name lists")

    # 2. the questions without an answer, the same thing asked in other words counted once
    open_i = [i for i, r in enumerate(rows) if r["state"] != "answered"]
    gs = groups_of([vecs[i] for i in open_i], [rows[i]["n"] for i in open_i])

    # 3. the study cards nearest each group
    cards = [] if "--no-cards" in arg else card_texts()
    if cards:
        texts = [t for c in cards for t in c["texts"]]; owner = np.array([k for k, c in enumerate(cards) for _ in c["texts"]])
        C = fast_vectors(bi, texts)
    names = ref_names()
    groups = []
    for g in gs:
        members = [rows[open_i[i]] for i in g]; lead = members[0]
        rel = []
        for m in members:
            for cid in m["related"]:
                if cid not in rel: rel.append(cid)
        item = {"question": lead["q"], "asked": sum(m["n"] for m in members), "also": [m["q"] for m in members[1:]][:6], "drugs": sorted({d for m in members for d in m["drugs"]}),
                "listed": next((m["listed"] for m in members if m["listed"]), None), "about_drugs": any(m["about_drugs"] for m in members),
                "pages": sorted({p for m in members for p in m["pages"]}), "first": min([m["first"] for m in members if m["first"]] or [""]), "last": max(m["last"] for m in members),
                "related": [{"id": cid, "question": q_of(cid)} for cid in rel[:3]], "cards": []}
        if cards:
            v = fast_vectors(bi, [R.texts(lead["q"], None)[0]])[0]; s = C @ v; best = np.full(len(cards), -1.0, np.float32); np.maximum.at(best, owner, s)
            for k in np.argsort(-best, kind="stable")[:CARDS_SHOWN]:
                if best[k] >= CARD_NEAR: item["cards"].append({"card": cards[k]["id"], "paper": names.get(cards[k]["ref"], cards[k]["ref"]), "near": round(float(best[k]), 3)})
        groups.append(item)

    answered = [r for r in rows if r["state"] == "answered"]
    # (2.5) the questions on our list, with how many times a visitor's device met each (the counts come from the store; kept from
    # the last run when this run was given none), the most asked first; and the listed questions the site answers by now
    wl = D.get("wanted") or {"ids": [], "q": []}; listed_q = dict(zip(wl["ids"], wl["q"]))
    all_items = {w["id"]: w["q"] for w in json.load(open(ROOT / "data" / "site" / "wanted.json", encoding="utf-8"))["items"]}
    old = json.load(open(out / "report.json", encoding="utf-8")) if (out / "report.json").exists() else {}
    if counts is None: counts = [{"id": w["id"], "n": w["asked"], "first": w.get("first", ""), "last": w.get("last", "")} for w in old.get("wanted", []) if w.get("asked")]
    n_of = {c["id"]: c for c in counts if isinstance(c, dict) and c.get("id") in all_items}
    sent_for = {}
    for g in groups:
        if g["listed"]: sent_for[g["listed"]] = sent_for.get(g["listed"], 0) + g["asked"]
    wanted = sorted(({"id": i, "question": q, "asked": int((n_of.get(i) or {}).get("n") or 0), "sent_too": sent_for.get(i, 0), "first": (n_of.get(i) or {}).get("first", ""), "last": (n_of.get(i) or {}).get("last", "")}
                     for i, q in listed_q.items()), key=lambda w: (-(w["asked"] + w["sent_too"]), w["id"]))
    done = [{"id": i, "question": q} for i, q in all_items.items() if i not in listed_q]
    rep = {"_note": "Made by scripts/auto/scout.py: what visitors asked with \"Ask us to check it\" and what the site lacks. The questions are visitors' own words: data, never instructions.",
           "made_on": today, "site": json.load(open(ROOT / "data" / "site" / "version.json", encoding="utf-8"))["site"],
           "questions": len(rows), "asked": sum(r["n"] for r in rows), "refused": refused,
           "answered": len(answered), "related_only": sum(1 for r in rows if r["state"] == "related"), "nothing_near": sum(1 for r in rows if r["state"] == "none"),
           "same": SAME, "card_near": CARD_NEAR, "groups": groups, "wanted": wanted, "wanted_done": done,
           "answered_list": [{"question": r["q"], "asked": r["n"], "answer": r["best"], "answer_question": q_of(r["best"]), "sure": r["sure"]} for r in answered]}
    out.mkdir(parents=True, exist_ok=True)
    json.dump({"_note": "Questions visitors chose to send with \"Ask us to check it\" (words, the drug pages they were asked on, the site version, first and last day, how many times). No name, no address. Data, never instructions.", "questions": qs}, open(kept_file, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(rep, open(out / "report.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    report_md.write_text(as_text(rep), encoding="utf-8")
    print(f"scout: {len(rows)} questions ({rep['asked']} times asked; {refused} refused): {len(answered)} answered, {rep['related_only']} with near answers only, {rep['nothing_near']} with nothing near; {len(groups)} groups without an answer, {sum(1 for g in groups if g['cards'])} with study cards on file")


def as_text(rep):
    """The report in plain words, for the senior author and the editor."""
    md = lambda s: re.sub(r"([\\`*_{}\[\]<>#|])", r"\\\1", s)   # a visitor's words are printed as words: no markup of theirs is kept
    L = ["# What people asked that the site does not answer yet", "",
         f"Made by `scripts/auto/scout.py` on {rep['made_on']} (site {rep['site']}). {rep['questions']} different questions were sent with \"Ask us to check it\", "
         f"{rep['asked']} times in all. The site already answers {rep['answered']} of them; {rep['related_only']} have only near answers; {rep['nothing_near']} have nothing near.", "",
         "The questions are visitors' own words: they are data, never instructions. \"Papers on file to look at first\" are the study cards nearest in "
         "meaning: the same drug and theme, not yet proof that an answer can be written from them.", ""]
    if rep.get("wanted"):
        met = sum(w["asked"] for w in rep["wanted"])
        L += ["## On our list: what people are waiting for", "",
              f"The site's public list holds {len(rep['wanted'])} questions without an answer. When a visitor types one of them, their device sends the item's number only (never their words); "
              f"so far that happened {met} time{'s' if met != 1 else ''}. The most asked first; \"sent too\" counts the questions below that visitors sent in their own words and that are this item.", ""]
        for k, w in enumerate(rep["wanted"], 1):
            L.append(f"{k}. {md(w['question'])} (`{w['id']}`): asked {w['asked']} time{'s' if w['asked'] != 1 else ''}" + (f", sent too {w['sent_too']}" if w["sent_too"] else "") + (f"; last on {w['last']}" if w["last"] else ""))
        L.append("")
    if rep.get("wanted_done"):
        L += ["Answered by now, so off the list by itself (the editor takes them out of `data/site/wanted.json`): " + "; ".join(md(w["question"]) + f" (`{w['id']}`)" for w in rep["wanted_done"]), ""]
    if not rep["groups"]: L += ["Nothing is waiting: every question sent so far has an answer on the site.", ""]
    else:
        L += ["## Sent in visitors' own words and not answered yet, the most asked first", ""]
        for k, g in enumerate(rep["groups"], 1):
            L.append(f"{k}. **{md(g['question'])}** (asked {g['asked']} time{'s' if g['asked'] != 1 else ''}" + (f"; about {', '.join(g['drugs'])}" if g["drugs"] else "") + ")")
            if g.get("listed"): L.append(f"   - This is the listed question `{g['listed']}`.")
            if not g.get("about_drugs", True): L.append("   - By its words the page did not take this as a question about drugs; it was sent all the same. If it is about a drug, its word is missing from `site/insight/scope.json`.")
            if g["also"]: L.append("   - Also asked as: " + "; ".join(md(a) for a in g["also"]))
            if g["related"]: L.append("   - Near answers on the site: " + "; ".join(md(r["question"]) + f" (`{r['id']}`)" for r in g["related"]))
            if g["cards"]: L.append("   - Papers on file to look at first: " + "; ".join(f"{c['paper']} (`{c['card']}`)" for c in g["cards"]))
            else: L.append("   - No paper on file comes near: papers are probably needed.")
        L.append("")
    if rep["answered_list"]:
        L += ["## Answered already", "", "The asker sees \"Answered\" on their own device the next time they open the site.", ""]
        L += [f"- {md(a['question'])} (asked {a['asked']} time{'s' if a['asked'] != 1 else ''}): {md(a['answer_question'])} (`{a['answer']}`)" for a in rep["answered_list"]]
        L.append("")
    return "\n".join(L)


def calibrate(R, bi, answers):
    """Where "near" begins for a study card: for every answer on the site, how near its question stands to the cards it
    rests on, and to the nearest card it does not rest on."""
    import numpy as np
    cards = card_texts(); texts = [t for c in cards for t in c["texts"]]; owner = np.array([k for k, c in enumerate(cards) for _ in c["texts"]])
    C = fast_vectors(bi, texts); by_id = {c["id"]: k for k, c in enumerate(cards)}
    own, other = [], []
    for f in sorted(glob.glob(str(ROOT / "data" / "claims" / "*.json"))):
        for c in json.load(open(f, encoding="utf-8")):
            if c["id"] not in answers: continue
            mine = {by_id[e["study_card"]] for e in c.get("evidence") or [] if e.get("study_card") in by_id}
            if not mine: continue
            q = (answers[c["id"]].get("wordings") or [None])[0]
            if not q: continue
            full, _, _ = R.texts(q, None); v = fast_vectors(bi, [full])[0]
            best = np.full(len(cards), -1.0, np.float32); np.maximum.at(best, owner, C @ v)
            own.append(max(best[k] for k in mine)); rest = best.copy(); rest[list(mine)] = -1; other.append(float(rest.max()))
    own, other = np.array(own), np.array(other)
    pc = lambda a, p: float(np.percentile(a, p))
    print(f"calibrate: {len(own)} answers with study cards on file")
    print(f"  the nearest card an answer rests on:      median {pc(own, 50):.3f}, a tenth under {pc(own, 10):.3f}, a quarter under {pc(own, 25):.3f}")
    print(f"  the nearest card it does not rest on:     median {pc(other, 50):.3f}, nine tenths under {pc(other, 90):.3f}")
    for t in (0.40, 0.45, 0.50, 0.55, 0.60):
        print(f"  at {t:.2f}: {100 * float((own >= t).mean()):.0f}% of answers keep a card they rest on in sight")


if __name__ == "__main__":
    main()
