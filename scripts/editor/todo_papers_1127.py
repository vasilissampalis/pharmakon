"""todo_papers_1127.py: the papers of the paper finder of 27 November 2026, as items for the senior author's to-do page.

Reads data/verification/papers-2026-11-27/candidates.json (the finder's 32 papers, most-asked question first) and the Crossref
records fetched for them on GitHub's machines (data/auto/papers/crossref-candidates-2026-11-27*.json; scripts/auto/papers.py,
lookup), and writes data/verification/papers-2026-11-27/todo_items.json: one item per paper in the page's form
{k, group, star, kind, apa, folder, name, url}, the APA 7 reference made from Crossref's record (journal and volume in
*italics*, as the page shows them), never typed by hand. A paper with no DOI keeps the finder's reference and its link.
"""
import glob, json, os, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]; os.chdir(ROOT)
sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(ROOT / "scripts" / "auto"))
import papers  # scripts/auto/papers.py: reference(), initials()

CR = {}
for f in sorted(glob.glob("data/auto/papers/crossref-candidates-2026-11-27*.json")):
    for r in json.load(open(f, encoding="utf-8"))["results"]:
        if r.get("doi") and r.get("ok"): CR[r["doi"].lower()] = r["crossref"]


def apa_md(rec):
    """papers.apa() with the journal and volume in *italics*."""
    names = [a["literal"] if a.get("literal") else a["family"] + (", " + papers.initials(a.get("given")) if a.get("given") else "") + (", " + a["suffix"] if a.get("suffix") else "") for a in rec.get("author") or []]
    au = names[0] if len(names) == 1 else ", ".join(names[:-1]) + ", & " + names[-1] if len(names) <= 20 else ", ".join(names[:19]) + ", … " + names[-1]
    y = ((rec.get("issued") or {}).get("date-parts") or [["n.d."]])[0][0]
    end = lambda t: "" if re.search(r"[.?!]$", t.strip()) else "."
    s = au + end(au) + f" ({y}). " + rec["title"] + end(rec["title"]) + " *" + rec.get("container-title", "") + "*"
    if rec.get("volume"): s += ", *" + str(rec["volume"]) + "*"
    if rec.get("issue"): s += "(" + str(rec["issue"]).replace("-", "–") + ")"
    s += (", " + str(rec["page"]).replace("-", "–") if rec.get("page") else ", Article " + str(rec["number"]) if rec.get("number") else "") + "."
    return s + (" https://doi.org/" + rec["DOI"] if rec.get("DOI") else "")


def item(doi, group, star, kind, folder, name, apa_fallback=None, url=None):
    cr = CR.get((doi or "").lower())
    if doi and not cr: sys.exit(f"no Crossref record fetched for {doi}")
    rec = papers.reference(doi, cr) if cr else None
    return {"k": re.sub(r"\.pdf$", "", name), "group": group, "star": star, "kind": kind, "apa": apa_md(rec) if rec else apa_fallback,
            "folder": folder, "name": name, "url": ("https://doi.org/" + rec["DOI"]) if rec else url}


C = json.load(open("data/verification/papers-2026-11-27/candidates.json", encoding="utf-8"))
by_q = {}
for c in C: by_q.setdefault(c["question"], []).append(c)
# the groups' titles, in people's words, most-asked first (the finder's order); the DOIs found later for papers it had none for
GROUP = ["6-APB and other benzofurans ('Benzo Fury')", "1P-LSD, and how it compares with LSD", "A pill's logo or look: the one paper that answer still needs",
         "How MDMA differs from meth or speed", "Xanax with coke or Adderall", "Psilocybin for anxiety and depression in people with cancer",
         "Can psilocybin therapy make depression or suicidal thoughts worse?", "Does cannabis make sex better?", "After naloxone (Narcan): withdrawal, and can the overdose come back?",
         "Is sugar as addictive as cocaine?", "How long weed stays in your system", "How long heroin shows up on a drug test", "Medicines that give a false positive: the one paper that answer still needs",
         "How alcohol kills", "Antidepressants taken to get high"]
FOUND = {"Kurtz_2011_BenzodiazepineDependenceClubScene.pdf": "10.1016/j.drugalcdep.2011.05.036", "Zeifman_2022_SuicidalityAfterPsychedelicTherapyIPD.pdf": "10.4088/jcp.21r14057",
         "Odell_2015_ResidualCannabisHeavyUse.pdf": "10.1016/j.forsciint.2015.01.026", "Cone_1991_6AcetylmorphineDetectionTimes.pdf": "10.1093/jat/15.1.1",
         "Esser_2024_DeathsExcessiveAlcoholUS.pdf": "10.15585/mmwr.mm7308a1"}
assert len(by_q) == len(GROUP), (len(by_q), len(GROUP))
out = []
for gi, (q, cs) in enumerate(by_q.items()):
    g = GROUP[gi]
    extra_first = []
    if gi == 10:   # weed: the 2026 systematic review, found by Crossref, goes first (the finder: "once the editor has its record, it should be saved first")
        extra_first.append(item("10.1016/j.phrs.2026.108142", g, True, "review", "Cannabis", "McCartney_2026_UrinaryTHCSystematicReview.pdf"))
    out += extra_first
    for ci, c in enumerate(cs):
        doi = c.get("doi") or FOUND.get(c["name"])
        star = ci == 0 and not extra_first          # the finder's first paper for each question is the one to save first (candidates.md, the stars)
        name = c["name"]
        if doi == "10.2147/SAR.S37917": name = "Sullivan_2014_AntidepressantMisuseReview.pdf"   # Crossref's record names Sullivan first
        out.append(item(doi, g, star, c.get("kind") or "original", c["folder"], name, apa_fallback=c["apa"] if not doi else None, url=None if doi else (re.search(r"https?://\S+$", c["apa"]) or [None])[0]))
        if doi == "10.4088/jcp.21r14057":
            out.append(item("10.4088/jcp.22l14505", g, False, "correction", "Psilocybin", "Zeifman_2022_Corrigendum.pdf"))
        if doi == "10.1016/j.drugalcdep.2015.10.011":
            out.append(item("10.1016/j.drugalcdep.2015.12.001", g, False, "correction", "2C-x", "NugterenVanLonkhuyzen_2016_Corrigendum.pdf"))
        if doi == "10.1080/15563650.2016.1253846":
            out.append(item("10.1080/15563650.2017.1284336", g, False, "comment", "Heroin", "Eggleston_2017_LetterWillman.pdf"))
            out.append(item("10.1080/15563650.2017.1284337", g, False, "comment", "Heroin", "Willman_2017_ReplyEggleston.pdf"))
    if gi == 1:    # 1P-LSD: whether the body turns 1P-LSD and other 1-acyl forms into LSD (the finder's next in line)
        out.append(item("10.1016/j.neuropharm.2019.107856", g, False, "original", "LSD", "Halberstadt_2020_1AcylLSDBiotransformation.pdf"))
    if gi == 8:    # naloxone: deaths after 'treat and release' (the finder's next in line)
        out.append(item("10.1136/emermed-2018-207534", g, False, "review", "Heroin", "Greene_2019_TreatAndReleaseMortality.pdf"))
    if gi == 11:   # heroin: the later study of heroin's markers in urine, found by Crossref
        out.append(item("10.1093/jat/25.7.504", g, False, "original", "Heroin", "Smith_2001_HeroinUrinaryMarkers.pdf"))
# the finder's next in line: can you overdose on LSD?
out.append(item("10.1016/j.forsciint.2018.01.006", "Can you overdose on LSD?", True, "review", "LSD", "Nichols_2018_IsLSDToxic.pdf"))
for x in out:
    s = re.sub(r"[^A-Za-z0-9_.-]", "", x["name"]); assert s == x["name"], x["name"]
assert len({x["k"] for x in out}) == len(out)
json.dump(out, open("data/verification/papers-2026-11-27/todo_items.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "items in", len({x["group"] for x in out}), "groups;", sum(1 for x in out if x["star"]), "marked save first")
