#!/usr/bin/env python3
"""candidate.py MODEL.onnx [--name FILE] [--keep] [--out RESULT.json] [--index-teachers N]: a model made by scripts/insight/train.py, walked through the measured path
of scripts/insight/MODELS.md in one go, beside the model on the site, with the page's own rule (decision 41; 19 November 2026).

  1. the candidate is put in site/insight/vendor/ (as FILE; default: its own file name) and named in a COPY of site/insight/model.json (the real
     one is not touched: build_index.py reads the copy through PK_INSIGHT_MODEL_JSON);
  2. the index is made with it (every text embedded again, by the page's own runtime, one text at a time), and its judge is trained for it on our
     own wordings and near-miss questions (judge2.py --six --save), as every new model needs; the weights, the tiers, the judge's cut and the
     aspects stay as model.json has them;
  3. the gold set is ranked with the page's rule for the candidate and for the model on the site (build_index.py --eval), and the two are set side
     by side: how many best matches, how many of them full, partial, wrong; how often a question nobody can answer gets one; where the full answer
     comes in the candidates' order; and how often a near-miss question gets the answer it does not have.
  --index-teachers N: the candidate's index also holds N of the teachers' ways of asking for each answer (model.json, "index_teachers"); the
  candidate may then be the site's own model file, to measure the index alone.
  --judge-teachers: its judge also learns from the teachers' ways of asking that the index does not hold (judge2.py --teachers).
  VERDICT: "better" only where the candidate's best match is wrong no more often than the site's (the rule of MODELS.md), it gives a question nobody
  can answer a best match no more often, and it gives more full answers as best match or the same number with fewer wrong; else "not better".
  Nothing is shipped by this: the candidate's file is taken out of vendor/ again unless --keep, and the model.json it used is written beside the
  result (RESULT.model.json) for the editor, who ships it with its NOTICE, its build and every check.
Needs site/insight/.cache/index-input.json (node site/build.js first).
"""
import sys, os, re, json, shutil, subprocess, pathlib, hashlib, tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
VENDOR = ROOT / "site" / "insight" / "vendor"
MODEL_JSON = ROOT / "site" / "insight" / "model.json"
INPUT = ROOT / "site" / "insight" / ".cache" / "index-input.json"
LINE = re.compile(r"best match for\s+(\d+) of\s+(\d+): full\s+(\d+) \(\s*\d+%\), partial\s+(\d+) \(\s*\d+%\), wrong\s+(\d+) \(\s*\d+%\); unanswerable given one (\d+) of (\d+)")


def arg(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


def parse(text):
    """The page's rule at model.json's cut, per split, and the candidates' order, from build_index.py --eval's lines."""
    out, split = {}, None
    for l in text.splitlines():
        m = re.match(r"gold, (\w+)", l)
        if m: split = m.group(1); continue
        cut = re.search(r"judge >= ([\d.]+) \(and about the drugs named\)", l)
        if split and cut:
            g = LINE.search(l)
            if g:
                b, n, f, p, w, u, nu = map(int, g.groups())
                row = {"best": b, "of": n, "full": f, "partial": p, "wrong": w, "unanswerable_given_one": u, "unanswerable": nu}
                out.setdefault("cuts", {}).setdefault(split, {})[cut.group(1)] = row
                if "<- model.json" in l: out[split] = row
        m = re.search(r"a full answer first ([\d.]+)%, in the first three ([\d.]+)%", l)
        if m: out["order"] = {"full_first": float(m.group(1)), "full_in_three": float(m.group(2))}
        m = re.search(r"near-miss questions given the answer they do not get as best match, judge >= ([\d.]+): (\d+) of (\d+)", l)
        if m: out.setdefault("near_miss_given_the_answer", {})[m.group(1)] = [int(m.group(2)), int(m.group(3))]
    return out


INPUT_SHA = []


def inputs_sha():
    """The build's input and every file of wordings an index is made from: a trial is only fair if none of them changes while it runs."""
    h = hashlib.sha256(INPUT.read_bytes())
    for f in sorted((ROOT / "data" / "verification" / "insight").glob("*.json")) + [ROOT / "data" / "auto" / "insight" / "teachers.json"]:
        if f.exists() and (f.name.startswith(("variants_", "nearmiss_")) or f.name == "teachers.json"): h.update(f.name.encode() + f.read_bytes())
    return h.hexdigest()


def run(cmd, env=None):
    sha = inputs_sha()
    if INPUT_SHA and sha != INPUT_SHA[0]: raise SystemExit("candidate: the build's input or a file of wordings changed during the trial (another build or a pull ran): run it again alone")
    INPUT_SHA[:1] = [sha]
    r = subprocess.run(cmd, cwd=ROOT, env=dict(os.environ, **(env or {})), capture_output=True, text=True)
    if r.returncode != 0: raise SystemExit(f"candidate: {' '.join(map(str, cmd[:4]))} failed:\n{r.stderr[-2000:]}")
    return r.stdout + r.stderr


def rate(x): return x["wrong"] / max(1, x["best"])


def dev_cut(cand, site):
    """A judge trained for another model or index weighs its numbers otherwise, so its cut is chosen afresh, on the dev half alone (the odd-numbered
    gold questions): of the cuts measured, the one with the most full answers as best match whose best matches are wrong no more often than the
    site's are on the dev half, and that gives a question nobody can answer one no more often (the fewer wrong, where two give as many full).
    None where no cut does so."""
    sd = site.get("dev") or {}; cd = (cand.get("cuts") or {}).get("dev") or {}
    ok = [(c, r) for c, r in cd.items() if sd and rate(r) <= rate(sd) + 1e-9 and r["unanswerable_given_one"] <= sd["unanswerable_given_one"]]
    if not ok: return None
    return max(ok, key=lambda cr: (cr[1]["full"], -cr[1]["wrong"], -float(cr[0])))[0]


def verdict(cand, site, cut=None):
    """MODELS.md's rule first: its best match is wrong no more often, and a question nobody can answer gets one no more often. Then it must do
    better where it counts for the reader: more questions get their full answer as best match (or as many, with fewer wrong); or, at the judge's
    own cut, what Insight shows (the best match and the related rows, sweep_related.py at the tiers now) helps more questions and misleads no
    more (help up, junk not up; or junk down, help not down)."""
    a = ((cand.get("cuts") or {}).get("all") or {}).get(cut) if cut else cand.get("all")
    b = site.get("all") or {}
    if not a or not b: return "not measured"
    if not (rate(a) <= rate(b) + 1e-9 and a["unanswerable_given_one"] <= b["unanswerable_given_one"]): return "not better"
    if a["full"] > b["full"] or (a["full"] == b["full"] and a["wrong"] < b["wrong"]): return "better"
    ra, rb = cand.get("related_now"), site.get("related_now")
    if cut is None and ra and rb and ((ra["help"] > rb["help"] and ra["junk"] <= rb["junk"]) or (ra["junk"] < rb["junk"] and ra["help"] >= rb["help"])) and a["full"] >= b["full"] - 1: return "better"
    return "not better"


def selftest():
    t = ("model x; gold questions: 400; 79 with a full answer, 126 unanswerable; candidates in order of first look + weights.topic x topic: a full answer first 63.3%, in the first three 74.7%\n"
         "gold, dev (odd-numbered): 200 questions\n  judge >= 0.6 (and about the drugs named) <- model.json   best match for  20 of 200: full  14 ( 70%), partial   6 ( 30%), wrong   0 (  0%); unanswerable given one 0 of 63; x\n"
         "gold, all: 400 questions\n  judge >= 0.5 (and about the drugs named)   best match for  50 of 400: full  30 ( 60%), partial  12 ( 24%), wrong   8 ( 16%); unanswerable given one 2 of 126; x\n"
         "  judge >= 0.6 (and about the drugs named) <- model.json   best match for  36 of 400: full  24 ( 67%), partial  11 ( 31%), wrong   1 (  3%); unanswerable given one 0 of 126; x\n"
         "near-miss questions given the answer they do not get as best match, judge >= 0.6: 150 of 1810 (8.3%)\n")
    p = parse(t)
    assert p["all"] == {"best": 36, "of": 400, "full": 24, "partial": 11, "wrong": 1, "unanswerable_given_one": 0, "unanswerable": 126}, p
    assert p["dev"]["best"] == 20 and p["order"] == {"full_first": 63.3, "full_in_three": 74.7} and p["near_miss_given_the_answer"] == {"0.6": [150, 1810]}
    site = {"all": p["all"]}
    assert verdict({"all": dict(p["all"], full=26, best=38)}, site) == "better"
    assert verdict({"all": dict(p["all"], full=26, best=40, wrong=3)}, site) == "not better"          # more wrong, as a share
    assert verdict({"all": dict(p["all"], unanswerable_given_one=1, full=30, best=42)}, site) == "not better"
    assert verdict({"all": dict(p["all"])}, site) == "not better" and verdict({}, site) == "not measured"
    # the cut chosen on the dev half (19 November 2026: the site's model with the teachers' wordings in its index)
    R = lambda b, f, p_, w, u: {"best": b, "full": f, "partial": p_, "wrong": w, "unanswerable_given_one": u, "unanswerable": 63}
    S = {"dev": R(25, 14, 6, 5, 2), "all": R(40, 24, 10, 6, 2)}
    C = {"cuts": {"dev": {"0.5": R(35, 16, 10, 9, 3), "0.6": R(31, 16, 8, 7, 1), "0.7": R(22, 15, 4, 3, 1), "0.8": R(14, 13, 0, 1, 1)},
                  "all": {"0.7": R(36, 23, 9, 4, 1)}}}
    assert dev_cut(C, S) == "0.7" and verdict(C, S, "0.7") == "not better"     # fewer wrong, but one full answer fewer
    C["cuts"]["all"]["0.7"] = R(37, 25, 8, 4, 1); assert verdict(C, S, "0.7") == "better"
    # what is shown when there is no best match counts too (19 November 2026: the model taught with the teachers' wordings)
    S2 = {"all": R(40, 24, 10, 6, 2), "related_now": {"help": 133, "junk": 60}}
    C2 = {"all": R(41, 23, 12, 6, 2), "related_now": {"help": 138, "junk": 58}}
    assert verdict(C2, S2) == "better" and verdict(dict(C2, related_now={"help": 138, "junk": 61}), S2) == "not better"
    assert verdict(dict(C2, all=R(41, 22, 13, 6, 2)), S2) == "not better" and verdict(dict(C2, all=R(42, 23, 12, 7, 2)), S2) == "not better"
    print("candidate selftest: ok")


def main():
    if "--selftest" in sys.argv: return selftest()
    args = [a for a in sys.argv[1:] if not a.startswith("--") and a not in (arg("--name"), arg("--out"), arg("--index-teachers"))]
    if not args: print(__doc__); return
    src = pathlib.Path(args[0]).resolve(); name = arg("--name", src.name); assert re.fullmatch(r"[A-Za-z0-9._-]+\.onnx", name), "the file name must be plain"
    if not INPUT.exists(): raise SystemExit("candidate: no site/insight/.cache/index-input.json: run node site/build.js first")
    out = pathlib.Path(arg("--out", str(ROOT / "data" / "verification" / "insight" / "train" / (pathlib.Path(name).stem + ".candidate.json"))))
    out.parent.mkdir(parents=True, exist_ok=True)
    dst = VENDOR / name; placed = False
    if dst.exists() and hashlib.sha256(dst.read_bytes()).hexdigest() != hashlib.sha256(src.read_bytes()).hexdigest():
        raise SystemExit(f"candidate: {dst} is another file already")
    if not dst.exists(): shutil.copyfile(src, dst); placed = True
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="pk-candidate-"))
    try:
        cfg = json.load(open(MODEL_JSON, encoding="utf-8")); cfg["file"] = name
        if arg("--index-teachers") is not None: cfg["index_teachers"] = int(arg("--index-teachers"))   # the teachers' ways of asking in the index too (that many an answer)
        mj = tmp / "model.json"; json.dump(cfg, open(mj, "w", encoding="utf-8"), ensure_ascii=False, indent=1); env = {"PK_INSIGHT_MODEL_JSON": str(mj)}
        print("candidate: the index with the candidate (every text embedded again) ...", flush=True)
        run(["python3", "-I", "scripts/insight/build_index.py", str(INPUT), str(tmp / "index0.json")], env)
        print("candidate: its judge, trained on our own wordings and near-miss questions ...", flush=True)
        jlog = run(["python3", "-I", "scripts/insight/judge2.py", str(INPUT), str(tmp / "index0.json"), "--six", "--save", str(tmp / "judge.json")] + (["--teachers"] if "--judge-teachers" in sys.argv else []), env)
        j = json.load(open(tmp / "judge.json", encoding="utf-8"))
        cfg["judge"] = dict(cfg["judge"], **{k: j[k] for k in ("features", "mu", "sd", "w", "b")}); json.dump(cfg, open(mj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("candidate: the gold set with the page's rule, the candidate ...", flush=True)
        c_log = run(["python3", "-I", "scripts/insight/build_index.py", str(INPUT), str(tmp / "index1.json"), "--eval"], env)
        print("candidate: ... and the model on the site", flush=True)
        s_log = run(["python3", "-I", "scripts/insight/build_index.py", str(INPUT), str(tmp / "index-site.json"), "--eval"])
        C, S = parse(c_log), parse(s_log)
        # what is shown when there is no best match, at the tiers model.json has: help (a full or partial answer among the rows), junk, miss, rows
        rel_re = re.compile(r"\| all\s+help\s+(\d+) junk\s+(\d+) miss\s+(\d+) ok\s+(\d+) \| seen\s+(\d+) of (\d+) \|\s+(\d+) rows,\s+(\d+)% answers \| unanswerable with rows\s+(\d+) of (\d+)")
        def related(index, e):
            out_ = run(["python3", "-I", "scripts/insight/sweep_related.py", str(INPUT), str(index)], e)
            m = rel_re.search(out_.split("related 0.44")[0])
            return dict(zip(("help", "junk", "miss", "ok", "seen", "with_full", "rows", "answers_pct", "unanswerable_with_rows", "unanswerable"), map(int, m.groups()))) if m else None
        C["related_now"] = related(tmp / "index1.json", env); S["related_now"] = related(tmp / "index-site.json", None)
        cut = dev_cut(C, S); v_same = verdict(C, S); v_dev = verdict(C, S, cut) if cut else "not better"
        if v_dev == "better": cfg["judge"]["best"] = float(cut)          # (where only the site's cut makes it better, that cut stays)
        res = {"_note": "scripts/insight/candidate.py: a trained model on the gold set with the page's own rule (its own judge; model.json's weights, tiers, cut and aspects), beside the model on the site. Nothing shipped.",
               "candidate": {"file": name, "sha256": hashlib.sha256(src.read_bytes()).hexdigest(), "bytes": src.stat().st_size, "gold": C},
               "site": {"file": json.load(open(MODEL_JSON, encoding="utf-8"))["file"], "gold": S},
               "verdict": "better" if "better" in (v_same, v_dev) else "not better",
               "verdict_at_the_site_cut": v_same, "cut_chosen_on_dev": cut, "verdict_at_the_dev_cut": v_dev,
               "judge_for_the_candidate": {k: cfg["judge"][k] for k in ("mu", "sd", "w", "b")}, "judge_log": [l for l in jlog.splitlines() if l.startswith(("our own examples", "judge weights", "model "))][:6]}
        json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        json.dump(cfg, open(out.with_suffix(".model.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        (out.with_suffix(".eval.txt")).write_text("== candidate\n" + c_log[-12000:] + "\n== site\n" + s_log[-12000:], encoding="utf-8")
        for who, g in (("candidate", C), ("site", S)): print(f"candidate: {who:12s} when there is no best match, at the tiers now: {g.get('related_now')}")
        for who, g, a in (("candidate", C, C.get("all") or {}), (f"cand.@{cut}", C, ((C.get("cuts") or {}).get("all") or {}).get(cut) or {}), ("site", S, S.get("all") or {})):
            o = g.get("order") or {}
            print(f"candidate: {who:12s} best matches {a.get('best')}: full {a.get('full')}, partial {a.get('partial')}, wrong {a.get('wrong')}; unanswerable given one {a.get('unanswerable_given_one')} of {a.get('unanswerable')}; full answer first {o.get('full_first')}%, in three {o.get('full_in_three')}%")
        print(f"candidate: verdict: {res['verdict']} (at the site's cut: {v_same}; at the cut chosen on the dev half, {cut}: {v_dev}) ->", out)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        if placed and "--keep" not in sys.argv: dst.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
