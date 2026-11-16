#!/usr/bin/env python3
"""own.py: the models that are our own (docs/AUTOMATION.md, decision 23).

The senior author, 16 November 2026: "if we can make our own ai we should that's what i was trying to do from the
beginning, our own autonomous self expanding ai".

    python3 -I scripts/auto/own.py adopt NAME      (make a candidate the model in use, IF the rule below allows it)
    python3 -I scripts/auto/own.py --selftest

What a model of our own is, here:
  - a FILE of numbers (ONNX) with its tokenizer's table, made in the workshop job (.github/workflows/own.yml) from an open
    model or from our own training, and kept as a release file of this repository. A file of numbers runs no code: the
    lane reads it with onnxruntime, which it already uses for the search model. Everything fetched from outside (open
    models, the packages that make and train them) runs only in the workshop job, which may read the repository and holds
    no key.
  - the very file that sat the exam. A candidate (data/auto/own/candidates/NAME.json) carries the SHA-256 of its files and
    its numbers on the exam; the lane refuses a file whose SHA-256 is not the one written down.
  - adopted by a rule, not by hope (adopt()): a candidate becomes the model in use (data/auto/own/models.json) only if on
    the exam it lets no more wrong cards through than the model in use AND stops no more good ones, and is better in at
    least one of the two; the first model for a job needs to do better than letting everything through. Every candidate's
    numbers stay in the repository whether it was adopted or not.

The first job is the checker ("does this passage support this sentence?", kind "seq": the passage and the sentence joined
by the tokenizer's end sign, two numbers out, the second is "supported"). The lane asks it about every sentence after the
second reader (scripts/auto/lane.py, the step "our own checker").

A passage too long for the model. The model reads some 500 word-pieces at once; a checked claim, or the passages of three
sources, are longer. MiniCheck's own way is to cut the passage into parts and let the best part count. A second way is
written here (focus): the sentences of the passage that share most words and numbers with the sentence to check are taken,
in their own order, until the model's room is full, and the model reads those; which are taken is decided by counting
shared words, with no model. Measured on the plain lines with the open model as it is (17 November 2026, pharmakon-check-0):
neither way tells a wrong line from a good one there (a good line scores above a wrong one 55 times in 100 either way), and
the second way stopped more good lines at every threshold. So FOCUS is off, the model's own way stands, and the second way
waits for a model that has learned from our lessons, to be measured again then.
"""
import sys, os, re, json, math, hashlib, pathlib, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
OWN = ROOT / "data" / "auto" / "own"
REG = OWN / "models.json"
CACHE = pathlib.Path(os.environ.get("PHARMAKON_OWN_CACHE") or (pathlib.Path.home() / ".cache" / "pharmakon-own"))
RELEASES = "https://github.com/vasilissampalis/pharmakon/releases/download/"       # the only place a model file is ever fetched from


class Missing(Exception):
    """The model in use cannot be run here (no file, a wrong SHA-256, no onnxruntime): the lane then publishes nothing by itself."""


def registry():
    try: return json.load(open(REG, encoding="utf-8"))
    except (OSError, ValueError): return {}


def in_use(job="check"):
    """The entry of the model in use for a job, or None when there is none yet."""
    e = registry().get(job)
    return e if isinstance(e, dict) and e.get("files") else None


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for part in iter(lambda: f.read(1 << 20), b""): h.update(part)
    return h.hexdigest()


def fetch(entry, opener=None):
    """The model's files on this machine, each with the SHA-256 the registry names: {"model": path, "tokenizer": path}."""
    out = {}
    for kind, f in entry["files"].items():
        url, want = str(f.get("url") or ""), str(f.get("sha256") or "")
        if not url.startswith(RELEASES) or not re.fullmatch(r"[0-9a-f]{64}", want): raise Missing(f"the {kind} file of {entry.get('name')} has no address in this repository's releases or no SHA-256")
        p = CACHE / want[:16] / url.rsplit("/", 1)[-1]
        if not p.exists() or sha256(p) != want:
            p.parent.mkdir(parents=True, exist_ok=True)
            try:
                with (opener or urllib.request.urlopen)(urllib.request.Request(url, headers={"User-Agent": "pharmakon-lane/1 (+https://pharmakon.world)"}), timeout=600) as r, open(p, "wb") as o:
                    for part in iter(lambda: r.read(1 << 20), b""): o.write(part)
            except Exception as e: raise Missing(f"the {kind} file of {entry.get('name')} could not be fetched: {type(e).__name__}: {str(e)[:120]}")
            if sha256(p) != want: p.unlink(); raise Missing(f"the {kind} file of {entry.get('name')} is not the file that sat the exam (its SHA-256 differs): not used")
        out[kind] = p
    return out


SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9“\"'(\[])")
FOCUS = False         # how a passage too long for the model is read: True, its sentences nearest the sentence to check; False, in parts (the best part counts)
STOP = set("""a an the and or but if then than that this these those of in on at to for from by with without into over under about as is are was were be been being it its they them their there here he she his her
you your we our i me my not no nor do does did done have has had having can could may might must should would will shall who whom whose which what when where why how all any both each few more most other some such only own
same so too very just also still even ever never much many""".split())


def stems(text):
    """The content words of a text cut roughly to their stems, and its numbers (no dictionary: endings only)."""
    out = set()
    for w in re.findall(r"[a-z]+|\d+(?:[.,]\d+)*", (text or "").lower()):
        if w[0].isdigit(): out.add(w.replace(",", "")); continue
        if w in STOP or len(w) < 3: continue
        for suf in ("ingly", "edly", "ing", "ed", "ies", "es", "ly", "s"):
            if w.endswith(suf) and len(w) - len(suf) >= 3: w = w[:-len(suf)] + ("y" if suf == "ies" else ""); break
        out.add(w)
    return out


def bits(passage, most, count):
    """A passage as sentences; a sentence longer than `most` word-pieces is cut further, at semicolons and then at commas."""
    out = []
    for sn in [x.strip() for x in SENT.split(passage or "") if x.strip()]:
        if count(sn) <= most: out.append(sn); continue
        for part in re.split(r"(?<=;)\s+", sn):
            if count(part) <= most: out.append(part); continue
            cur = ""
            for piece in re.split(r"(?<=,)\s+", part):
                if cur and count(cur + " " + piece) > most: out.append(cur); cur = piece
                else: cur = (cur + " " + piece).strip()
            if cur: out.append(cur)
    return out


def focus(passage, sentence, room, count):
    """The sentences of a long passage that share most words and numbers with the sentence to check, in the passage's own order,
    as many as fit in `room` word-pieces."""
    bs = bits(passage, max(24, room // 3), count); key = stems(sentence)
    near = sorted(range(len(bs)), key=lambda i: (-len(key & stems(bs[i])) / (1 + 0.02 * len(stems(bs[i]))), i))
    take, used = [], 0
    for i in near:
        c = count(bs[i]) + 1
        if used + c > room: continue                                  # this one does not fit any more; a shorter one further down may
        take.append(i); used += c
    return " ".join(bs[i] for i in sorted(take))


def parts_of(passage, room, count):
    """A passage as parts of at most `room` tokens (count(text) tells how many a text has), cut at sentence ends; a single
    sentence longer than that stands alone and is cut off by the tokenizer."""
    out, cur = [], ""
    for sn in [x.strip() for x in SENT.split(passage or "") if x.strip()]:
        if cur and count(cur + " " + sn) > room: out.append(cur); cur = sn
        else: cur = (cur + " " + sn).strip()
    if cur: out.append(cur)
    return out or [""]


class Check:
    """The checker in use: score([(passage, sentence)]) -> [how sure it is, 0 to 1, that the passage supports the sentence]."""
    def __init__(self, entry=None, files=None, session=None, tokenizer=None):
        self.e = entry or in_use("check")
        if not self.e: raise Missing("no checker of our own is in use yet")
        self.max = int(self.e.get("max_len") or 512); self.kind = self.e.get("kind") or "seq"
        if session is not None: self.sess, self.tok = session, tokenizer; return          # (a test's own)
        try:
            import onnxruntime as ort
            from tokenizers import Tokenizer
        except ImportError as e: raise Missing("onnxruntime or tokenizers is not on this machine: " + str(e)[:80])
        files = files or fetch(self.e)
        so = ort.SessionOptions(); so.intra_op_num_threads = max(1, min(4, os.cpu_count() or 1))
        self.sess = ort.InferenceSession(str(files["model"]), so, providers=["CPUExecutionProvider"]); self.tok = Tokenizer.from_file(str(files["tokenizer"]))
        self.tok.no_padding(); self.tok.enable_truncation(max_length=self.max)
    def _run(self, text):
        import numpy as np
        enc = self.tok.encode(text); ids = np.array([enc.ids], dtype=np.int64); feed = {"input_ids": ids, "attention_mask": np.ones_like(ids)}
        names = {i.name for i in self.sess.get_inputs()}
        if "token_type_ids" in names: feed["token_type_ids"] = np.zeros_like(ids)
        z = self.sess.run(None, {k: v for k, v in feed.items() if k in names})[0][0]
        m = float(max(z)); ex = [math.exp(float(v) - m) for v in z]
        return ex[1] / sum(ex)
    def score(self, pairs):
        eos = self.e.get("join") or "</s>"; count = lambda t: len(self.tok.encode(t).ids)
        out = []
        for passage, sentence in pairs:
            room = max(64, self.max - count(sentence) - 6)
            if FOCUS and not self.e.get("parts"): parts = [passage if count(passage) <= room else focus(passage, sentence, room, count)]
            else: parts = parts_of(passage, room, count)
            out.append(round(max(self._run(part + eos + sentence) for part in parts), 4))
        return out


def better(cand, cur):
    """May a candidate replace the model in use? (the rule; cand and cur are their numbers on the exam: {"wrong_through", "good_stopped", "wrong", "good"})
    Returns (yes or no, why)."""
    need = ("wrong_through", "good_stopped", "wrong", "good")
    if not all(isinstance(cand.get(k), int) for k in need): return False, "the candidate has no whole numbers on the exam"
    if cand["wrong"] < 20 or cand["good"] < 100: return False, "the candidate did not sit enough of the exam (20 wrong cards and 100 good ones at least)"
    if cur is None:
        ok = cand["wrong_through"] < cand["wrong"] and cand["good_stopped"] <= 0.4 * cand["good"]
        return ok, "the first model for this job: it catches wrong items and stops no more than 4 good ones in 10" if ok else "it catches nothing, or stops more than 4 good items in 10"
    if (cand["wrong"], cand["good"], cand.get("on")) != (cur.get("wrong"), cur.get("good"), cur.get("on")): return False, "the two did not sit the same exam: sit the model in use again first"
    if cand["wrong_through"] > cur["wrong_through"]: return False, f"it lets more wrong cards through ({cand['wrong_through']} against {cur['wrong_through']})"
    if cand["good_stopped"] > cur["good_stopped"]: return False, f"it stops more good cards ({cand['good_stopped']} against {cur['good_stopped']})"
    if cand["wrong_through"] == cur["wrong_through"] and cand["good_stopped"] == cur["good_stopped"]: return False, "it is no better than the model in use"
    return True, f"wrong cards let through {cur['wrong_through']} -> {cand['wrong_through']}, good cards stopped {cur['good_stopped']} -> {cand['good_stopped']}"


def adopt(name, job="check", today=None):
    import datetime
    c = json.load(open(OWN / "candidates" / (name + ".json"), encoding="utf-8")); reg = registry(); cur = reg.get(job) if isinstance(reg.get(job), dict) else None
    ok, why = better(c.get("exam") or {}, (cur or {}).get("exam") if cur else None)
    if not ok: print(f"own: {name} is NOT adopted for {job}: {why}"); return False
    reg.setdefault("_note", "The models of our own that are in use (scripts/auto/own.py), each with the SHA-256 of its files and its numbers on the exam. A model comes here only through own.py adopt, by the rule written there. 'before': the models it replaced.")
    entry = dict(c, adopted=(today or datetime.date.today().isoformat()), why=why)
    if cur: reg.setdefault("before", {}).setdefault(job, []).append({k: cur.get(k) for k in ("name", "adopted", "exam")})
    reg[job] = entry; OWN.mkdir(parents=True, exist_ok=True); json.dump(reg, open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"own: {name} is the model in use for {job}: {why}"); return True


def selftest():
    import tempfile
    # the rule
    cur = {"wrong_through": 16, "good_stopped": 40, "wrong": 31, "good": 287}
    assert better({"wrong_through": 12, "good_stopped": 40, "wrong": 31, "good": 287}, cur)[0] and better({"wrong_through": 16, "good_stopped": 30, "wrong": 31, "good": 287}, cur)[0]
    assert not better({"wrong_through": 10, "good_stopped": 41, "wrong": 31, "good": 287}, cur)[0] and not better({"wrong_through": 17, "good_stopped": 10, "wrong": 31, "good": 287}, cur)[0] and not better(dict(cur), cur)[0]
    assert not better({"wrong_through": 5, "good_stopped": 10, "wrong": 31, "good": 287, "on": "plain lines"}, dict(cur, on="the cards"))[0]          # numbers from another exam are not compared
    assert not better({"wrong_through": 5, "good_stopped": 10, "wrong": 11, "good": 11}, None)[0] and not better({"wrong_through": 10, "good_stopped": 30, "wrong": 30, "good": 287}, cur)[0]       # too little of the exam; not the same exam
    assert better({"wrong_through": 20, "good_stopped": 100, "wrong": 31, "good": 287}, None)[0] and not better({"wrong_through": 31, "good_stopped": 0, "wrong": 31, "good": 287}, None)[0] and not better({"wrong_through": 2, "good_stopped": 200, "wrong": 31, "good": 287}, None)[0]
    # a long passage is cut at sentence ends and the best part counts; the sentence always stands whole after the end sign
    words = lambda t: len(t.split())
    ps = parts_of("One two three. Four five six seven. Eight nine. Ten eleven twelve thirteen fourteen.", 7, words)
    assert ps == ["One two three. Four five six seven.", "Eight nine. Ten eleven twelve thirteen fourteen."] and parts_of("", 7, words) == [""], ps
    class Enc:
        def __init__(self, ids): self.ids = ids
    class Tok:
        def encode(self, t): return Enc(list(range(len(t.split()))))
    seen = []
    class In:
        def __init__(self, n): self.name = n
    class Sess:
        def get_inputs(self): return [In("input_ids"), In("attention_mask")]
        def run(self, _, feed):
            seen.append(sorted(feed)); n = feed["input_ids"].shape[1]
            return [[[0.0, 3.0] if n == 8 else [2.0, 0.0]]]                 # the part of 5 words with the sentence of 3 supports; the long part does not
    c = Check(entry={"name": "t", "kind": "seq", "max_len": 80, "files": {}, "parts": True}, session=Sess(), tokenizer=Tok())
    c.tok.encode = lambda t: Enc(list(range(len(t.replace("</s>", " ").split()))))
    s = c.score([(" ".join(["word"] * 69) + " end. Two words here now ok.", "it is so")])
    assert s == [round(math.exp(3) / (1 + math.exp(3)), 4)] and seen[0] == ["attention_mask", "input_ids"] and len(seen) == 2, (s, seen)
    # a passage too long for the model: its sentences nearest the sentence to check are read, in their own order, as many as fit
    assert stems("Deaths fell by 33, about a third, in 2003.") == {"death", "fell", "33", "third", "2003"} and "the" not in stems("The pills")
    long = "Alpha beta gamma delta one. " * 6 + "In Vancouver 56 deaths were recorded before the site opened. " + "Epsilon zeta eta theta two. " * 6 + "After it opened 33 deaths were recorded. " + "Iota kappa lambda mu three. " * 6
    f = focus(long, "Deaths went from 56 before the site opened to 33 after.", 30, words)
    assert "In Vancouver 56 deaths were recorded before the site opened." in f and "After it opened 33 deaths were recorded." in f and words(f) <= 30 and f.index("56") < f.index("33"), f     # both facts, though they stand far apart; what room is left is filled in the passage's order
    assert bits("One, two, three, four, five, six; seven eight nine ten eleven twelve thirteen.", 6, words) == ["One, two, three, four, five, six;", "seven eight nine ten eleven twelve thirteen."]
    assert bits("One two, three four, five six, seven eight, nine ten.", 4, words) == ["One two, three four,", "five six, seven eight,", "nine ten."]
    global FOCUS
    seen.clear(); c2 = Check(entry={"name": "t", "kind": "seq", "max_len": 46, "files": {}}, session=Sess(), tokenizer=Tok()); c2.tok.encode = lambda t: Enc(list(range(len(t.replace("</s>", " ").split()))))
    FOCUS = True; c2.score([(long, "Deaths went from 56 before the site opened to 33 after.")]); n_focus = len(seen)
    FOCUS = False; c2.score([(long, "Deaths went from 56 before the site opened to 33 after.")]); assert n_focus == 1 and len(seen) >= n_focus + 2      # the second way reads once; the model's own way reads every part
    # a file that is not the one written down is refused; an address outside this repository's releases is refused
    global CACHE, OWN, REG
    keep = (CACHE, OWN, REG); tmp = pathlib.Path(tempfile.mkdtemp()); CACHE, OWN, REG = tmp / "cache", tmp / "own", tmp / "own" / "models.json"
    try:
        class R:
            def __init__(self, b): self.b = [b, b""]
            def __enter__(self): return self
            def __exit__(self, *a): return False
            def read(self, n): return self.b.pop(0) if self.b else b""
        good = hashlib.sha256(b"numbers").hexdigest()
        e = {"name": "x", "files": {"model": {"url": RELEASES + "own-models/x.onnx", "sha256": good}}}
        assert fetch(e, lambda req, timeout=0: R(b"numbers"))["model"].read_bytes() == b"numbers"
        try: fetch({"name": "x", "files": {"model": {"url": RELEASES + "own-models/y.onnx", "sha256": hashlib.sha256(b"other").hexdigest()}}}, lambda req, timeout=0: R(b"numbers")); raise AssertionError("a file with another SHA-256 was used")
        except Missing as m: assert "not the file that sat the exam" in str(m)
        try: fetch({"name": "x", "files": {"model": {"url": "https://example.org/x.onnx", "sha256": good}}}); raise AssertionError("a file from elsewhere")
        except Missing: pass
        assert in_use("check") is None
        (OWN / "candidates").mkdir(parents=True)
        json.dump({"name": "c1", "from": "an open model", "kind": "seq", "files": e["files"], "exam": {"wrong_through": 20, "good_stopped": 60, "wrong": 31, "good": 287}}, open(OWN / "candidates" / "c1.json", "w"))
        json.dump({"name": "c2", "kind": "seq", "files": e["files"], "exam": {"wrong_through": 21, "good_stopped": 10, "wrong": 31, "good": 287}}, open(OWN / "candidates" / "c2.json", "w"))
        json.dump({"name": "c3", "kind": "seq", "files": e["files"], "exam": {"wrong_through": 15, "good_stopped": 60, "wrong": 31, "good": 287}}, open(OWN / "candidates" / "c3.json", "w"))
        assert adopt("c1", today="2026-11-17") and in_use("check")["name"] == "c1" and not adopt("c2") and in_use("check")["name"] == "c1"         # worse on wrong cards: never, however few good ones it stops
        assert adopt("c3", today="2026-11-18") and in_use("check")["name"] == "c3" and registry()["before"]["check"][0]["name"] == "c1"
    finally: CACHE, OWN, REG = keep
    print("own selftest: ok (a model replaces the one in use only if it lets no more wrong cards through and stops no more good ones, and is better in one; a long passage is cut at sentence ends and its best part counts; "
          "a file whose SHA-256 is not the one written down, or that is not from this repository's releases, is refused)")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a: selftest()
    elif len(a) == 2 and a[0] == "adopt" and re.fullmatch(r"[a-z0-9.-]{3,60}", a[1]): sys.exit(0 if adopt(a[1]) else 1)
    else: sys.exit(__doc__)
