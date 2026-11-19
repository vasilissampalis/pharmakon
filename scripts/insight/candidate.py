#!/usr/bin/env python3
"""candidate.py MODEL.onnx [--name FILE] [--keep] [--out RESULT.json]: a model made by scripts/insight/train.py, walked through the measured path
of scripts/insight/MODELS.md in one go, beside the model on the site, with the page's own rule (decision 41; 19 November 2026).

  1. the candidate is put in site/insight/vendor/ (as FILE; default: its own file name) and named in a COPY of site/insight/model.json (the real
     one is not touched: build_index.py reads the copy through PK_INSIGHT_MODEL_JSON);
  2. the index is made with it (every text embedded again, by the page's own runtime, one text at a time), and its judge is trained for it on our
     own wordings and near-miss questions (judge2.py --six --save), as every new model needs; the weights, the tiers, the judge's cut and the
     aspects stay as model.json has them;
  3. the gold set is ranked with the page's rule for the candidate and for the model on the site (build_index.py --eval), and the two are set side
     by side: how many best matches, how many of them full, partial, wrong; how often a question nobody can answer gets one; where the full answer
     comes in the candidates' order; and how often a near-miss question gets the answer it does not have.
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
        if split and "<- model.json" in l:
            g = LINE.search(l)
            if g:
                b, n, f, p, w, u, nu = map(int, g.groups())
                out[split] = {"best": b, "of": n, "full": f, "partial": p, "wrong": w, "unanswerable_given_one": u, "unanswerable": nu}
        m = re.search(r"a full answer first ([\d.]+)%, in the first three ([\d.]+)%", l)
        if m: out["order"] = {"full_first": float(m.group(1)), "full_in_three": float(m.group(2))}
        m = re.search(r"near-miss questions given the answer they do not get as best match, judge >= ([\d.]+): (\d+) of (\d+)", l)
        if m: out.setdefault("near_miss_given_the_answer", {})[m.group(1)] = [int(m.group(2)), int(m.group(3))]
    return out


def run(cmd, env=None):
    r = subprocess.run(cmd, cwd=ROOT, env=dict(os.environ, **(env or {})), capture_output=True, text=True)
    if r.returncode != 0: raise SystemExit(f"candidate: {' '.join(map(str, cmd[:4]))} failed:\n{r.stderr[-2000:]}")
    return r.stdout + r.stderr


def verdict(cand, site):
    a, b = cand.get("all") or {}, site.get("all") or {}
    if not a or not b: return "not measured"
    rate = lambda x: x["wrong"] / max(1, x["best"])
    ok = rate(a) <= rate(b) + 1e-9 and a["unanswerable_given_one"] <= b["unanswerable_given_one"] and (a["full"] > b["full"] or (a["full"] == b["full"] and a["wrong"] < b["wrong"]))
    return "better" if ok else "not better"


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
    print("candidate selftest: ok")


def main():
    if "--selftest" in sys.argv: return selftest()
    args = [a for a in sys.argv[1:] if not a.startswith("--") and a not in (arg("--name"), arg("--out"))]
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
        mj = tmp / "model.json"; json.dump(cfg, open(mj, "w", encoding="utf-8"), ensure_ascii=False, indent=1); env = {"PK_INSIGHT_MODEL_JSON": str(mj)}
        print("candidate: the index with the candidate (every text embedded again) ...", flush=True)
        run(["python3", "-I", "scripts/insight/build_index.py", str(INPUT), str(tmp / "index0.json")], env)
        print("candidate: its judge, trained on our own wordings and near-miss questions ...", flush=True)
        jlog = run(["python3", "-I", "scripts/insight/judge2.py", str(INPUT), str(tmp / "index0.json"), "--six", "--save", str(tmp / "judge.json")], env)
        j = json.load(open(tmp / "judge.json", encoding="utf-8"))
        cfg["judge"] = dict(cfg["judge"], **{k: j[k] for k in ("features", "mu", "sd", "w", "b")}); json.dump(cfg, open(mj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("candidate: the gold set with the page's rule, the candidate ...", flush=True)
        c_log = run(["python3", "-I", "scripts/insight/build_index.py", str(INPUT), str(tmp / "index1.json"), "--eval"], env)
        print("candidate: ... and the model on the site", flush=True)
        s_log = run(["python3", "-I", "scripts/insight/build_index.py", str(INPUT), str(tmp / "index-site.json"), "--eval"])
        C, S = parse(c_log), parse(s_log)
        res = {"_note": "scripts/insight/candidate.py: a trained model on the gold set with the page's own rule (its own judge; model.json's weights, tiers, cut and aspects), beside the model on the site. Nothing shipped.",
               "candidate": {"file": name, "sha256": hashlib.sha256(src.read_bytes()).hexdigest(), "bytes": src.stat().st_size, "gold": C},
               "site": {"file": json.load(open(MODEL_JSON, encoding="utf-8"))["file"], "gold": S}, "verdict": verdict(C, S),
               "judge_for_the_candidate": {k: cfg["judge"][k] for k in ("mu", "sd", "w", "b")}, "judge_log": [l for l in jlog.splitlines() if l.startswith(("our own examples", "judge weights", "model "))][:6]}
        json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        json.dump(cfg, open(out.with_suffix(".model.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        (out.with_suffix(".eval.txt")).write_text("== candidate\n" + c_log[-12000:] + "\n== site\n" + s_log[-12000:], encoding="utf-8")
        for who, g in (("candidate", C), ("site", S)):
            a = g.get("all") or {}; o = g.get("order") or {}
            print(f"candidate: {who:9s} best matches {a.get('best')}: full {a.get('full')}, partial {a.get('partial')}, wrong {a.get('wrong')}; unanswerable given one {a.get('unanswerable_given_one')} of {a.get('unanswerable')}; full answer first {o.get('full_first')}%, in three {o.get('full_in_three')}%")
        print("candidate: verdict:", res["verdict"], "->", out)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        if placed and "--keep" not in sys.argv: dst.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
