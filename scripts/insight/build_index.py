"""build_index.py IN.json OUT.json [NEXT.json] [--eval]: Pharmakon Insight's index (site 2.2.0, 14 November 2026; honest
tiers and next questions for site 2.3, 15 November 2026). Called by site/build.js, which writes IN.json: every answer on the
page with its substance, section, pages, the drugs it is about, every wording of its question on the site and its short
answer. Adds the ways people ask each answer (data/verification/insight/variants_reader696.json and the "more" wordings
of nearmiss_*.json, when present; the "near" questions of those files, which an answer does NOT answer, are never indexed
and never reach the page), embeds every wording and short answer with Insight's model (site/insight/model.json names the
file in site/insight/vendor; where the files came from: scripts/insight/MODELS.md) exactly as the page does in the browser
(BERT uncased WordPiece, [CLS] text [SEP], at most 128 tokens, mean over the tokens, unit length), and writes OUT.json: the
vectors (int8; the page scales each row back to unit length), each answer's words for the word-overlap score, the drugs
each answer is about, the names that name a drug in a question, the model's file name, and the weights, the tiers and
the judge of site/insight/model.json (the page and the checks read them from OUT.json only). NEXT.json gets each answer's next questions
(the nearest answers by the meaning of their questions, never from another drug, never itself): site/build.js puts them in
the page, for "Read next" and "People also ask".

Two looks at every question (2.3; the senior author, 15 November: "it has a high error rate"). The first is 2.2.0's score:
the question, with the drug's own name brought along, against every wording and short answer. Its weakness, measured on
the gold set: the drug's name carries so much of the meaning that any question about kratom scores high against any answer
about kratom. So every wording is embedded a second time with the drug names taken out ("is it addictive"), and so is the
question: that is the topic score. Which drug is meant is then settled by the names themselves, not by the model: an answer
is a best match only when it is about every drug the question names (or the drug of the page the reader is on).

The weights, the tiers and the judge (site/insight/model.json; nothing here or in the page holds a number of its own):
  weights  q, short, words: the first look, as tuned in tune.py and scored in eval_gold.py: 0.7 x the best wording, 0.3 x
           the short answer, plus 0.2 x word overlap (TF-IDF over each answer's wordings on the site and its short answer);
           topic: answers are put in order by first look + topic x the topic score; same: an answer about the drugs the
           question names goes this far ahead (in effect: first).
  judge    what makes a best match (the editor, 15 November; scripts/insight/judge2.py trains and measures it). Two
           thresholds on the two looks gave a best match that was wrong for 20 of 77 gold questions. The judge is a small
           logistic regression on six numbers the page has at hand for its first candidate (features, in order: its best
           wording, its second-best wording, its short answer, word overlap, topic, its lead over the next answer about
           the drugs named), each standardized (mu, sd), weighed (w) and summed with b; trained on our own wordings and
           near-miss questions only, never on a gold question. The first candidate is the best match when it is about
           every drug the question names and the judge's number is `best` or more; there is never a second best match.
  tiers    related: a related answer needs a first look of this or more ... near: ... and a topic score of this or more,
           and to be about at least one of the drugs named (or the drug of the page the reader is on).
Measured on the gold set with the page's own rule (--eval; 400 forum questions, 79 with a full answer by either reader,
126 that neither reader could answer): scripts/insight/MODELS.md has the table.

The tokens are made here by the tokenizers library (BertWordPieceTokenizer, lowercase); the model is run by the page's own
runtime under Node (scripts/insight/embed.js: ONNX Runtime Web from site/insight/vendor), one text at a time, so the
index's numbers are the very numbers the page computes for the same words (bit-identical; the Python onnxruntime on a PC
gives cosine 0.994 to 1 against the page, as its int8 kernels round differently: parity.js). Vectors are cached by text in
site/insight/.cache/, in a file named after the model file's SHA-256 (not committed): a build embeds only new or changed
texts, and a new model embeds everything again.
--eval: also ranks the forum questions of the gold set (two blind readers, data/verification/insight/) with the page's own
rule (class Ranker below, which scripts/insight/parity.js holds the page to), and prints how often a best match is a full
answer, a partial one or wrong, how the related answers do, the same for other cuts of the judge's number, and how often
an answer is given as best match to a question the near-miss readers wrote as one it does not answer."""
import base64, glob, hashlib, json, math, os, pathlib, re, shutil, subprocess, sys
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
VENDOR = ROOT / "site/insight/vendor"
CONFIG = json.load(open(os.environ.get("PK_INSIGHT_MODEL_JSON") or (ROOT / "site/insight/model.json"), encoding="utf-8"))   # the model's file name, the weights, the tiers (PK_INSIGHT_MODEL_JSON: another copy, for scripts/insight/candidate.py only)
MODEL = CONFIG["file"]
MODEL_SHA256 = hashlib.sha256((VENDOR / MODEL).read_bytes()).hexdigest() if (VENDOR / MODEL).exists() else "missing"
CACHE = ROOT / "site/insight/.cache" / ("vectors-" + MODEL_SHA256[:16] + ".npz")   # made by the page's runtime, one text at a time (see embed_all)
VARIANTS = ROOT / "data/verification/insight/variants_reader696.json"
NEARMISS = ROOT / "data/verification/insight"   # nearmiss_*.json: per answer, "more" (wordings it answers) and "near" (questions it does not)
N_NEXT = 10      # next questions kept for each answer about its own drugs (three for each drug, when that is more); the page shows three
N_PAGE = 5       # ... and at least this many on each page the answer is told on (three are shown; the others stand in for answers already opened)
# Names that name a drug in a question (for the tiers, the routes and the topic score): each drug's slug, the parts of its
# name and its street names of three letters or more (data/site/substances.json, aliases.json), without the WEAK ones:
# everyday words that are also street names. "pills" in "sleeping pills" must not make a question about ecstasy, nor
# "drink" in "drink water" one about alcohol, nor "analogues" one about fentanyl; they still bring the drug's name along
# for the first look (expand, as 2.2.0 tuned it).
WEAK = set("drink pills crystal ice speed tabs brown lean glue toad robo balloons spice oat microdosing vaping pouches solvents butane analogues".split())
# everyday names beyond aliases.json (the word search has its own list, SR_NAMES in site/src/app.simple.js)
EXTRA = {"benzo": ["benzodiazepines"], "benzodiazepine": ["benzodiazepines"], "xans": ["benzodiazepines"], "ativan": ["benzodiazepines"], "klonopin": ["benzodiazepines"],
         "sleeping pills": ["benzodiazepines"], "sleeping pill": ["benzodiazepines"], "sleeping tablets": ["benzodiazepines"],
         "magic mushrooms": ["psilocybin"], "laughing gas": ["nitrous-oxide"], "nos": ["nitrous-oxide"], "nangs": ["nitrous-oxide"], "whippets": ["nitrous-oxide"],
         "painkillers": ["prescription-opioids"], "oxy": ["prescription-opioids"], "percocet": ["prescription-opioids"], "vicodin": ["prescription-opioids"],
         "fent": ["fentanyl-and-analogues"], "nitazene": ["fentanyl-and-analogues"], "amphetamines": ["amphetamine"], "cathinones": ["synthetic-cathinones"], "2cb": ["2c-x"],
         "beer": ["alcohol"], "beers": ["alcohol"], "wine": ["alcohol"], "liquor": ["alcohol"], "cigarettes": ["nicotine"], "cigarette": ["nicotine"],
         "edible": ["cannabis"], "energy drink": ["caffeine"], "robotussin": ["dxm"]}
# a family's name names every drug of the family (substances.json, cls): an answer about any one of them is about it
FAMILY_WORDS = {"Opioids": ["opioids", "opioid", "opiates", "opiate"], "Stimulants": ["stimulants", "stimulant"], "Depressants": ["depressants", "downers"],
                "Classic psychedelics": ["psychedelics", "psychedelic", "hallucinogens"], "Atypical psychedelics": ["psychedelics", "psychedelic", "hallucinogens"],
                "Dissociatives": ["dissociatives", "dissociative"], "Cannabinoids": ["cannabinoids"], "Inhalants": ["inhalants"]}
SUB = json.load(open(ROOT / "data/site/substances.json", encoding="utf-8"))
AL = json.load(open(ROOT / "data/site/aliases.json", encoding="utf-8"))


class PyEncoder:
    """The same model run by the Python onnxruntime (texts in padded batches, mean over the real tokens, unit length):
    parity.js compares it with the page as an independent check of the model; the index itself is made with the page's
    runtime (embed_ids)."""
    def __init__(self):
        import onnxruntime as ort
        self.tok = tokenizer(); self.tok.enable_padding()
        self.s = ort.InferenceSession(str(VENDOR / MODEL), providers=["CPUExecutionProvider"])
        self.inputs = [i.name for i in self.s.get_inputs()]
    def __call__(self, texts):
        out = []
        for i in range(0, len(texts), 64):
            enc = self.tok.encode_batch(texts[i:i + 64])
            ii = np.array([e.ids for e in enc], dtype=np.int64); am = np.array([e.attention_mask for e in enc], dtype=np.int64)
            feed = {"input_ids": ii, "attention_mask": am}
            if "token_type_ids" in self.inputs: feed["token_type_ids"] = np.zeros_like(ii)
            h = self.s.run(None, feed)[0]; m = am[..., None].astype(np.float32)
            v = (h * m).sum(1) / np.maximum(m.sum(1), 1e-9)
            out.append(v / np.maximum(np.linalg.norm(v, axis=-1, keepdims=True), 1e-9))
        return np.vstack(out)


def encoder(): return PyEncoder()


def tokenizer():
    from tokenizers import BertWordPieceTokenizer
    tok = BertWordPieceTokenizer(str(VENDOR / "vocab.txt"), lowercase=True)
    tok.enable_truncation(128)   # the page truncates at 128 tokens, [CLS] and [SEP] included; no padding
    return tok


def embed_ids(ids):
    """Unit vectors for lists of token ids, made by the page's runtime under Node (scripts/insight/embed.js)."""
    d = CACHE.parent; d.mkdir(parents=True, exist_ok=True)
    inp, out = d / "embed-in.json", d / "embed-out.f32"
    inp.write_text(json.dumps({"ids": ids}), encoding="utf-8")
    node = os.environ.get("PK_NODE") or shutil.which("node") or "node"
    r = subprocess.run([node, str(ROOT / "scripts/insight/embed.js"), str(inp), str(out)], capture_output=True, text=True)
    if r.returncode != 0: sys.exit("insight: the page's runtime could not embed the texts: " + r.stderr.strip()[-600:])
    V = np.fromfile(out, dtype="<f4").reshape(len(ids), -1)
    inp.unlink(); out.unlink()
    return V


def embed_all(texts, quiet=False):
    """Unit vectors for texts, from the cache where a text was embedded before. Each text is run alone, as the page runs a
    question (the int8 model sets its scale from all the numbers in a batch: a text run in a padded batch comes out slightly
    different)."""
    key = lambda t: hashlib.sha1(t.encode("utf-8")).hexdigest()
    have = {}
    if CACHE.exists():
        z = np.load(CACHE, allow_pickle=False)
        have = dict(zip(z["keys"].tolist(), z["vecs"]))
    need = sorted({t for t in texts if key(t) not in have})
    if need:
        tok = tokenizer()
        for t, v in zip(need, embed_ids([tok.encode(t).ids for t in need])): have[key(t)] = v.astype(np.float32)
        ks = sorted(have); np.savez(CACHE, keys=np.array(ks), vecs=np.vstack([have[k] for k in ks]))
    if not quiet: print(f"insight: {len(texts)} texts embedded ({len(need)} new)", file=sys.stderr)
    return np.vstack([have[key(t)] for t in texts]) if texts else np.zeros((0, 384), np.float32)


def int8(M):
    """Each row as int8 (scaled to its largest value) in base64, and the unit rows the page gets back from it: the page
    reads the int8 values and scales each row to unit length, so no scale needs to be sent."""
    s = np.maximum(np.abs(M).max(1), 1e-12) / 127.0
    q = np.clip(np.round(M / s[:, None]), -127, 127).astype(np.int8)
    back = q.astype(np.float32); back /= np.maximum(np.linalg.norm(back, axis=1, keepdims=True), 1e-9)
    return base64.b64encode(q.tobytes()).decode("ascii"), back


def unit_rows(b64, dim):
    """The rows as the page reads them: int8 from base64, each scaled to unit length."""
    q = np.frombuffer(base64.b64decode(b64), dtype=np.int8).astype(np.float32).reshape(-1, dim)
    return q / np.maximum(np.linalg.norm(q, axis=1, keepdims=True), 1e-9)


# word overlap as eval_match.py's Lexical: words are runs of a-z and 0-9; a word's weight is log(1 + N / df) over the answers
words = lambda s: re.findall(r"[a-z0-9]+", s.lower())


class Words:
    def __init__(self, docs):
        self.N = len(docs); self.df = {}
        for d in docs:
            for w in set(words(d)): self.df[w] = self.df.get(w, 0) + 1
        self.D = [self.vec(d) for d in docs]
    def vec(self, t):
        v = {}
        for w in words(t):
            if w in self.df: v[w] = v.get(w, 0.0) + math.log(1 + self.N / self.df[w])
        n = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {w: x / n for w, x in v.items()}
    def sims(self, t):
        q = self.vec(t)
        return np.array([sum(x * d.get(w, 0.0) for w, x in q.items()) for d in self.D], np.float32)


def drug_name_sets():
    """Each drug's names, as tune.py's: its slug, the parts of its name and its street names of three letters or more."""
    out = {}
    for s in SUB:
        ns = {s["slug"].replace("-", " ")}
        for part in re.split(r"[()/,;]| and ", s["name"]):
            p = part.strip().lower()
            if len(p) >= 3: ns.add(p)
        for a in AL.get(s["slug"], []):
            if len(a) >= 3: ns.add(a.lower())
        out[s["slug"]] = ns
    return out


# drug names for the first look (as tune.py's expand): a street or brand name in a question brings the drug's own name along
def drug_names():
    pats, canon = {}, {}
    for slug, ns in drug_name_sets().items():
        pats[slug] = re.compile(r"\b(" + "|".join(re.escape(n) for n in sorted(ns, key=len, reverse=True)) + r")\b")
    for s in SUB: canon[s["slug"]] = s["name"].split(" (")[0]
    def expand(t):
        tl = t.lower(); d = sorted(slug for slug, p in pats.items() if p.search(tl))
        extra = [canon[x] for x in d if canon[x].lower() not in tl]
        return t + (" (" + ", ".join(extra) + ")" if extra else "")
    return expand


def names_table():
    """[name, [drugs]] for every name that names a drug in a question, the longest first (so "crystal meth" is read before
    "meth"): the drugs' own names without the WEAK ones, the EXTRA everyday names, and the families' names."""
    t = {}
    for slug, ns in drug_name_sets().items():
        for n in ns:
            if n not in WEAK: t.setdefault(n, set()).add(slug)
    for n, slugs in EXTRA.items(): t.setdefault(n, set()).update(slugs)
    for fam, ws in FAMILY_WORDS.items():
        members = {s["slug"] for s in SUB if s["cls"] == fam}
        for w in ws: t.setdefault(w, set()).update(members)
    return [[n, sorted(t[n])] for n in sorted(t, key=lambda n: (-len(n), n))]


def name_pattern(names):
    """One pattern for all the names, in the order given; the page builds the same one (insPrepare in app.insight.js)."""
    return re.compile(r"(?<!\w)(" + "|".join(re.escape(n) for n in names) + r")(?!\w)", re.I)


class Ranker:
    """The page's ranking (insRank in site/src/app.insight.js) in Python, from the index the page reads: for --eval, and
    for scripts/insight/parity.js, which requires the page to give the same best match, the same related answers and the
    same judge's number."""
    def __init__(self, D):
        dim = D["dim"]; self.ids = D["ids"]; self.n = len(self.ids); self.rows = np.array(D["rows"])
        self.W, self.M, self.S = unit_rows(D["W"], dim), unit_rows(D["M"], dim), unit_rows(D["S"], dim)
        self.lex = Words(D["docs"]); self.wt = D["weights"]; self.t = D["tiers"]; self.J = D["judge"]
        # 2.22: (what the question asks about, which answers speak of it, the judge's cut for such a question, the narrower cases with the answers that are about each, the answers about two drugs)
        self.aspects = [(re.compile(a["ask"], re.I | re.A), a["has"], float(a.get("best") or 0), [(re.compile(n, re.I | re.A), bits) for n, bits in a.get("narrow") or []], a.get("two") or "") for a in D.get("aspects") or []]
        self.about = [set(D["slugs"][k] for k in xs) for xs in D["about"]]
        self.name_of = {n: [D["slugs"][k] for k in xs] for n, xs in D["names"]}
        self.pat = name_pattern([n for n, _ in D["names"]])
        self.expand = drug_names(); self.canon = {s["slug"]: s["name"].split(" (")[0] for s in SUB}
        # 2.5: the list of questions not answered yet, as a ranker of its own over the same names, weights and judge
        Sc = D.get("scope"); self.scope_re = re.compile(SCOPE_B + Sc["src"] + SCOPE_E, re.I | re.A) if Sc else None
        self.unfin = unfinished_rule((Sc or {}).get("unfinished"), [n for n, _ in D["names"]], vocabulary())
        self.spell = spell_rule((Sc or {}).get("spell"), self.name_of, ((Sc or {}).get("unfinished") or {}).get("names") or [], vocabulary(), (self.unfin or {}).get("known") or ()) if Sc else None
        self.scope_not = re.compile(SCOPE_B + Sc["not"] + SCOPE_E, re.I | re.A) if Sc else None
        Wd = D.get("wanted"); self.wanted = None; self.want_cut = (Wd or {}).get("cut", 1.0); self.want_near = (Wd or {}).get("near", [0.0, 0.0])
        if Wd: self.wanted = Ranker({"dim": dim, "ids": Wd["ids"], "rows": Wd["rows"], "W": Wd["W"], "M": Wd["M"], "S": Wd["S"], "docs": Wd["docs"], "weights": D["weights"], "tiers": D["tiers"], "judge": D["judge"],
                                     "slugs": D["slugs"], "about": Wd["about"], "names": D["names"]})
    def named(self, q):
        """The drugs a question names, each as the list of drugs its name stands for (a family's name: every drug of it)."""
        out = []
        for m in self.pat.finditer(q):
            g = self.name_of.get(m.group(1).lower())
            if g and g not in out: out.append(g)
        return out
    def mask(self, q): return self.pat.sub("it", q)
    def texts(self, q, drug=None):
        """What is embedded for a question: with the drug's own name brought along, and with the drug names taken out; and
        the drugs it is about (on a drug's page, a question that names none is about that drug)."""
        groups = self.named(q); full = self.expand(q)
        if not groups and drug: groups = [[drug]]; full += " (" + self.canon[drug] + ")"
        return full, self.mask(q), groups
    def look(self, v, mv, q, groups):
        """Everything the page computes for a question, for every answer: bw and bw2, the best and the second-best wording
        of the answer in the first look (-1 where it has no second wording); sh, its short answer; lx, word overlap; plain,
        the first look (the three weighed); topic, its best wording with the drug names taken out; ok, it is about every
        drug the question names; some, about at least one of them; by, plain + weights.topic x topic; key, the page's
        order: by, the answers about the drugs named weights.same ahead. (The reference for these numbers is look() in
        scripts/insight/judge2.py, which trains the judge on them.)"""
        sw, sm = self.W @ v, self.M @ mv
        bw = np.full(self.n, -1.0, np.float32); bw2 = np.full(self.n, -1.0, np.float32); bm = np.full(self.n, -1.0, np.float32)
        np.maximum.at(bw, self.rows, sw); np.maximum.at(bm, self.rows, sm)
        order = np.argsort(-sw, kind="stable")
        rest = sw.copy(); rest[order[np.unique(self.rows[order], return_index=True)[1]]] = -1.0   # without each answer's best wording
        np.maximum.at(bw2, self.rows, rest)
        sh = self.S @ v; lx = self.lex.sims(q)
        plain = self.wt["q"] * bw + self.wt["short"] * sh + self.wt["words"] * lx
        has = lambda i, g: any(s in self.about[i] for s in g)
        ok = np.array([all(has(i, g) for g in groups) for i in range(self.n)])
        some = np.array([not groups or any(has(i, g) for g in groups) for i in range(self.n)])
        by = plain + self.wt["topic"] * bm
        return {"bw": bw, "bw2": bw2, "sh": sh, "lx": lx, "plain": plain, "topic": bm, "ok": ok, "some": some, "by": by, "key": by + self.wt["same"] * ok, "groups": groups, "q": q}
    def six(self, L, c):
        """The judge's six numbers for answer c (judge.features, in that order): its best wording, its second-best wording
        (0 if it has one wording), its short answer, word overlap, topic, and its lead over the next answer: by[c] less the
        highest by among the other answers about every drug the question names (less 0 if there is no other)."""
        el = L["ok"].copy(); el[c] = False
        lead = float(L["by"][c] - (L["by"][el].max() if el.any() else 0.0))
        return [float(L["bw"][c]), float(max(L["bw2"][c], 0.0)), float(L["sh"][c]), float(L["lx"][c]), float(L["topic"][c]), lead]
    def judge(self, f):
        """The judge's number for six numbers f: how sure it is that the first candidate answers what was asked."""
        J = self.J; z = sum(w * (x - m) / d for w, x, m, d in zip(J["w"], f, J["mu"], J["sd"])) + J["b"]
        return 1.0 / (1.0 + math.exp(-z))
    def speaks(self, q, c, p=1.0, ng=0):
        """(2.22) Does answer c speak of what the question asks about, and of no narrower case than the question does?
        False where the question asks about something that does harm when it is got wrong (dying: model.json, aspects)
        and: none of the answer's wordings nor its short answer speaks of it; or the judge's number p is under the cut
        the aspect sets; or the answer's own question is about a narrower case (withdrawal, touching, pregnancy ...)
        that the question does not name; or it is about two drugs and the question names fewer (ng: how many it names).
        q None: not asked (the callers that have no question at hand)."""
        if q is None: return True
        for ask, has, best, narrow, two in self.aspects:
            if not ask.search(q): continue
            if has[c] != "1" or p < best: return False
            if any(bits[c] == "1" and not rx.search(q) for rx, bits in narrow): return False
            if two and two[c] == "1" and ng < 2: return False
        return True
    def tiers(self, plain, topic, groups, feats, q=None):
        """The page's rule. c, the first candidate in the page's order, is the best match if it is about every drug the
        question names, the judge's number for it (feats(c): its six numbers) is judge.best or more, and (2.22, with q
        given) it speaks of what the question asks about; there is never a
        second best match. Related: the next answers in that order, up to three, with a first look of tiers.related or
        more and a topic of tiers.near or more, about at least one of the drugs named (c first among them when it is not
        the best match). Returns the best match (a list of none or one), the related answers and the judge's number."""
        t = self.t; has = lambda i, g: any(s in self.about[i] for s in g)
        ok = np.array([all(has(i, g) for g in groups) for i in range(self.n)])
        some = np.array([not groups or any(has(i, g) for g in groups) for i in range(self.n)])
        order = np.argsort(-(plain + self.wt["topic"] * topic + self.wt["same"] * ok), kind="stable")
        c = int(order[0]); p = self.judge(feats(c))
        best = [c] if ok[c] and p >= self.J["best"] and self.speaks(q, c, p, len(groups)) else []
        related = [int(i) for i in order if int(i) not in best and plain[i] >= t["related"] and topic[i] >= t["near"] and some[i]][:3]
        return best, related, p
    def rank_vectors(self, q, v, mv, groups):
        L = self.look(v, mv, q, groups); best, related, p = self.tiers(L["plain"], L["topic"], groups, lambda c: self.six(L, c), q)
        c = int(np.argsort(-L["key"], kind="stable")[0])
        row = lambda i: {"id": self.ids[i], "plain": round(float(L["plain"][i]), 4), "topic": round(float(L["topic"][i]), 4), "off": not bool(L["ok"][i])}
        return {"best": [row(i) for i in best], "related": [row(i) for i in related], "first": {"id": self.ids[c], "p": p, "f": self.six(L, c)},
                "plain": L["plain"], "topic": L["topic"], "ok": L["ok"], "look": L}
    def rank(self, q, drug=None):
        full, masked, groups = self.texts(q, drug)
        v, mv = embed_all([full, masked], quiet=True)
        return self.rank_vectors(q, v, mv, groups)
    def correct(self, q):
        """(the question with every misspelt name of a drug read as that name, [[the word as typed, the name]]): the page's
        insSpell. site/insight/scope.json ("spell") explains the rule."""
        R = getattr(self, "spell", None); read = []
        if not R: return q, read
        if R.get("phr_re") is not None:                                                            # a learned name typed wrong, of one word or more
            def whole(m):
                name = R["phr"][re.sub(r"\s+", " ", m.group(0).lower())]; read.append([m.group(0), name]); return name
            q = R["phr_re"].sub(whole, str(q))
        def one(m):
            n = spell_word(R, m.group(0).lower(), self.scope_re)
            if not n: return m.group(0)
            read.append([m.group(0), n]); return n
        return SPELL_WORD.sub(one, str(q)), read
    def unfinished(self, q, on_page=False):
        """Is this question not finished yet, by its words alone (the page's insUnfinished; site/insight/scope.json,
        "unfinished")? "" when it is finished; else why it is not: "ends" (it ends on a word a question cannot end on),
        "bare" (a drug is named, or it is asked on a drug's page, and nothing but function words is said about it),
        "which" (it names no drug and every word could be asked of any drug), "typing" (its last word is the beginning of
        a word). on_page: it is asked on a drug's page and names no drug."""
        U = self.unfin
        if not U: return ""
        w, nm = self.unf_tokens(q); names = sum(1 for n in nm if n is not None)
        if not w: return ""
        s = " ".join(w)
        if any(p.search(s) for p in U["whole"]): return ""
        if w[-1] in U["ends"] and not any(p.search(s) for p in U["strand"]): return "ends"
        if names >= 2 and all(x == "it" or x in U["join"] for x in w): return ""               # two drugs and a word that joins them
        # (2.9.2) nothing but function words and words for people: a subject, and nothing said of it ("do gay people"), unless
        # a form of "be" stands before a last word that describes people ("are people gay": finished, and not about drugs)
        people = all(x in U["aux"] or x in U["who"] or x in U["whoadj"] for x in w)
        be = next((i for i, x in enumerate(w) if x in U["be"]), -1); gap = any(x in U["gap"] for x in w)
        said = be >= 0 and w[-1] in U["whoadj"] and be < len(w) - 1                                     # "are people gay"
        said_of = be >= 0 and any(x in U["pp"] for x in w[be + 2:-1])                                   # "is weed for kids": something is said of it
        if names or on_page:
            if people and not said and not said_of:
                return "" if names and any(p.search(s) for p in U["named"]) else "bare"                 # "what is ketamine" is finished
            if not people and self.verbless(w, nm): return "verb"
        elif all(x in U["known"] for x in w):
            if people: return "" if said or (said_of and not gap) else "open"
            if self.verbless(w, nm): return "verb"                                                     # "how long does withdrawal"
            # a word for people that is not an everyday one, and no "it": the question is about people, and finished ("how do i get a girlfriend")
            if not gap and any((x in U["who"] or x in U["whoadj"]) and x not in U["func"] and x not in U["aux"] and x not in U["topic"] for x in w): return ""
            general = not gap and (any(x in U["nouns"] for x in w) or (w[0] == "why" and any(x in U["topic"] for x in w)))
            return "" if general else "which"
        elif self.verbless(w, nm): return "verb"                                                       # "does the government", "can dogs"
        # the last word is still being typed: not a word, and the beginning of a drug's name, or (in a question that otherwise
        # reads as one about drugs) of a word this rule knows
        last = w[-1]
        if len(w) >= 2 and last not in U["known"] and not (U["vocab"] and last in U["vocab"]):
            if last in U["begin_name"]: return "typing"
            if last in U["begin"] and (names or on_page or all(x in U["known"] for x in w[:-1]) or self.in_scope(" ".join(w[:-1]))): return "typing"
        return ""
    def unf_tokens(self, q):
        """The words of a question as the rule 'is it finished?' reads them (the page's insUnfTokens): small letters, each drug's
        name read as "it", and beside each word the name it stands for (None for a word that is not a name). A name inside a
        phrase that is not drug talk ("weed my garden", "diet coke": the scope rule's 'not') is not a name."""
        t = str(q).lower().replace("\u2019", "'")
        blank = self.scope_not.sub(lambda m: " " * len(m.group(0)), t) if getattr(self, "scope_not", None) is not None else t
        out, surf, at = [], [], 0
        for m in self.pat.finditer(blank):
            out += [t[at:m.start()], " 0n0 "]; surf.append(t[m.start():m.end()]); at = m.end()
        out.append(t[at:]); w, nm, k = [], [], 0
        short = (self.unfin or {}).get("short") or {}
        for y in re.findall(r"[a-z0-9']+", "".join(out)):
            y = y.strip("'")
            if not y: continue
            if y == "0n0" and k < len(surf): w.append("it"); nm.append(surf[k]); k += 1
            else:
                for z in (short[y].split(" ") if y in short else [y]): w.append(z); nm.append(None)    # "u" is "you", "gonna" is "going to"
        return w, nm
    def verbless(self, w, nm):
        """(2.9.2) A helper verb and no main verb after it: "do gay people", "does smoking weed", "how long does the high",
        "can dogs". Grammar, not topic: after do, does, can, should, will … a question needs a verb in its base form.
        site/insight/scope.json ("unfinished": help, do, open, det, be, verbs) explains what can be that verb. Only short
        questions (six words or fewer) are read this way: a longer one has room for a second clause this rule cannot see."""
        U = self.unfin
        if len(w) > 6: return False
        thing = lambda x: self.scope_re is not None and bool(self.scope_re.search(x))               # a drug word
        def base(j):                                                                                # may word j be the main verb where it stands?
            x, prev = w[j], (w[j - 1] if j else "")
            if prev in U["det"]: return False                                                       # "the high", "a test": a thing
            if nm[j] is not None:                                                                   # a drug's name: only where its own word can be a verb ("can i speed up")
                return j > 0 and prev not in U["help"] and not prev.endswith("ing") and re.fullmatch(r"[a-z]+", nm[j]) is not None and verbish(nm[j], U["vocab"])
            if x in U["verbs"] or x in U["be"]: return True
            if x in U["aux"] or x in U["gap"] or x in U["who"] or x in U["whoadj"]: return False
            if j and (nm[j - 1] is not None or prev in UNF_SUBJ): return True                       # right after a pronoun or a drug's name: the verb's place
            if thing(x): return False
            return verbish(x, U["vocab"])
        for i, x in enumerate(w):
            prev = w[i - 1] if i else ""
            if nm[i] is None and x in U["help"] and prev not in U["det"] and prev != "to":
                if x in U["do"] and any(y not in U["open"] for y in w[:i]): return False            # "people do drugs": do can be the main verb
                return not any(base(j) for j in range(i + 1, len(w)))
            # before the helper: question words, function words, people, drugs' names and drug words, a word in -ing ("smoking weed can"); nothing else
            if nm[i] is None and (x in U["be"] or x == "to" or not (x in U["open"] or x in U["aux"] or x in U["ends"] or x in U["gap"] or x in U["who"] or x in U["whoadj"] or x.endswith("ing") or thing(x))): return False
        return False
    def in_scope(self, q):
        """Is this a question about drugs, by its words alone (the page's insScope; site/insight/scope.json)? Yes when,
        with the phrases that are not drug talk taken out, it names a drug the site covers or holds a drug word, the name
        of a drug the site does not cover, or a research chemical's name by its shape."""
        if self.scope_re is None: return True
        t = self.scope_not.sub(" ", q)
        return bool(self.named(t)) or bool(self.scope_re.search(t))
    def want(self, q, v, mv, groups):
        """The page's second look (insWant): the listed question a typed question is like, or None. The list is ranked as
        the answers are, by its own small index; the first candidate is taken when it is about every drug the question
        names, the judge's number for it is the list's cut or more, and its best wording is near enough in both looks:
        with the drug's name (the judge's first number) and with the drug names taken out (its fifth), each at least
        the list's 'near' (wanted_index says why the judge alone is not enough on a small list)."""
        if self.wanted is None: return None
        r = self.wanted.rank_vectors(q, v, mv, groups); c = r["first"]
        on = bool(r["ok"][self.wanted.ids.index(c["id"])])
        return {"id": c["id"], "p": c["p"]} if on and c["p"] >= self.want_cut and c["f"][0] >= self.want_near[0] and c["f"][4] >= self.want_near[1] else None


class WordRules:
    """The rules that read a question's words alone (the drugs it names; is it about drugs; is it finished), without the
    model and without a built index: from the same tables the index is built from. For --words and for callers that only
    need these."""
    def __init__(self):
        t = names_table(); self.name_of = {n: g for n, g in t}; self.pat = name_pattern([n for n, _ in t]); Sc = scope_block()
        self.scope_re = re.compile(SCOPE_B + Sc["src"] + SCOPE_E, re.I | re.A); self.scope_not = re.compile(SCOPE_B + Sc["not"] + SCOPE_E, re.I | re.A)
        self.unfin = unfinished_rule(Sc["unfinished"], [n for n, _ in t], vocabulary())
        self.spell = spell_rule(Sc["spell"], self.name_of, Sc["unfinished"]["names"], vocabulary(), self.unfin["known"])
    named = Ranker.named; in_scope = Ranker.in_scope; unfinished = Ranker.unfinished; correct = Ranker.correct; unf_tokens = Ranker.unf_tokens; verbless = Ranker.verbless
    def unknown(self, q): return unknown_words(q, self.unfin["vocab"] or set(), self.unfin["known"])


def forum_questions():
    """The real questions the word rules are measured on: the forum questions of 14 November 2026 and the gold set's."""
    F = [x["question"] if isinstance(x, dict) else x for x in json.load(open(ROOT / "data/verification/questions-2026-11-14/forums.json", encoding="utf-8"))["questions"]]
    G = [x["question"] for x in json.load(open(ROOT / "data/verification/insight/gold-sample.json", encoding="utf-8"))["questions"]]
    return list(dict.fromkeys(F + G))


def repo_questions():
    """Every sentence that ends in a question mark in the repository's question files (the forum questions' own rewordings,
    the near-miss readers' wordings, the site's own questions, the list of questions not answered yet), without the ones
    the word rules were written with (forum_questions) and without the questions about other things: finished questions
    that the rule 'is it finished?' was not tuned on (site 2.9.2: the fresh measure of decision 26, step d)."""
    out = []
    def walk(o):
        if isinstance(o, str):
            s = o.strip()
            if s.endswith("?") and 8 <= len(s) <= 220 and "\n" not in s: out.append(s)
        elif isinstance(o, list):
            for x in o: walk(x)
        elif isinstance(o, dict):
            for v in o.values(): walk(v)
    for f in sorted((ROOT / "data/verification").glob("questions-*/*.json")) + sorted((ROOT / "data/verification/insight").glob("*.json")) + sorted((ROOT / "data/site").glob("*.json")):
        if f.name == "scope-other.json": continue
        try: walk(json.load(open(f, encoding="utf-8")))
        except (OSError, ValueError): pass
    tuned = set(forum_questions())
    return [q for q in dict.fromkeys(out) if q not in tuned]


def measure_words(R, show=True):
    """The rule 'is this question finished?' on real questions (no model needed). Three numbers: of the forum questions,
    whole, how many it wrongly calls unfinished; of the questions about other things, how many it calls unfinished (they
    are finished: they get the line for a question that is not about drugs); and of forum questions cut off as a reader
    who is still typing leaves them (just before the first drug they name; after the first half of that name; after each
    word a question cannot end on), how many it catches. Returns the numbers."""
    real = forum_questions(); other = json.load(open(ROOT / "data/verification/insight/scope-other.json", encoding="utf-8"))["questions"]
    wrong = [(R.unfinished(q), q) for q in real if R.unfinished(q)]; wrong_o = [(R.unfinished(q), q) for q in other if R.unfinished(q)]
    before, inside, after = [], [], []
    for q in real:
        m = R.pat.search(q)
        if m:
            pre = q[:m.start()].strip()
            if len(pre.split()) >= 2 and not R.named(pre):
                before.append(pre); half = q[:m.start() + max(3, (len(m.group(1)) + 1) // 2)]
                if not R.named(half): inside.append(half)                                   # (half a name can be a name: "meth" of "methadone")
        w = q.rstrip("?!. ").split()
        for i in range(2, len(w)):
            if w[i - 1].lower().strip(",;:()'\"") in R.unfin["ends"]: after.append(" ".join(w[:i]))
    out = {"real": len(real), "real_called_unfinished": len(wrong), "other": len(other), "other_called_unfinished": len(wrong_o)}
    for name, cuts in (("cut_before_the_name", before), ("cut_inside_the_name", inside), ("cut_after_a_word_that_cannot_end", after)):
        cuts = list(dict.fromkeys(cuts)); miss = [c for c in cuts if not R.unfinished(c)]; out[name] = [len(cuts) - len(miss), len(cuts)]
        if show:
            print(f"unfinished rule, forum questions {name.replace('_', ' ')}: {len(cuts) - len(miss)} of {len(cuts)} called unfinished")
            for c in miss[:400]: print("    not caught:", repr(c), "" if R.in_scope(c) else "(and not taken as about drugs)")
    # what a question that is not taken as about drugs is told: with a word the model does not know, "We do not know <word>.
    # If it is a drug, send us your question"; with none, "This does not look like a question about drugs"
    plain = [q for q in other if not R.in_scope(q) and not R.unfinished(q)]; with_word = [(R.unknown(q), q) for q in plain if R.unknown(q)]
    missed = [q for q in real if not R.in_scope(q) and not R.unfinished(q)]; missed_word = [(R.unknown(q), q) for q in missed if R.unknown(q)]
    out.update({"other_plain": len(plain), "other_with_an_unknown_word": len(with_word), "real_not_taken_as_about_drugs": len(missed), "of_which_with_an_unknown_word": len(missed_word)})
    # (2.9.2) the fresh measure: question sentences the rule was not written with. Many of the site's own are asked on a drug's
    # page ("How do people take it?"): there "it" is that drug, and off the page "which drug?" is the right reading
    fresh = repo_questions(); fresh_hit = {}
    for q in fresh:
        u = R.unfinished(q)
        if u: fresh_hit.setdefault(u, []).append(q)
    out.update({"fresh": len(fresh), "fresh_called_unfinished": {k: len(v) for k, v in sorted(fresh_hit.items())}})
    if show:
        print(f"unfinished rule, fresh: of {len(fresh)} question sentences it was not written with, called unfinished: {out['fresh_called_unfinished']}")
        for k, v in sorted(fresh_hit.items()):
            for q in v: print(f"    {k}: {q}")
    if show:
        print(f"unfinished rule: whole forum questions called unfinished {len(wrong)} of {len(real)}:", wrong)
        print(f"unfinished rule: questions about other things called unfinished {len(wrong_o)} of {len(other)}:", wrong_o)
        print(f"unknown words: of {len(plain)} questions about other things that get the line for them, {len(with_word)} hold a word the model does not know:", with_word[:40])
        print(f"unknown words: of {len(missed)} forum questions the scope rule does not take as about drugs, {len(missed_word)} hold a word the model does not know:", [(u, q) for u, q in missed_word], "; without one:", [q for q in missed if not R.unknown(q)])
    return out



PLACE_AT = 0.62   # (2.27) an answer the system wrote stands under the topic of the nearest checked answer of its page only from this likeness (set by place_eval below)


def auto_place(A, rows, Wv, quiet=False):
    """(2.27; the senior author, 20 November 2026, 00:51: "our ai should enrichen the drug page menus and all the other sections of the site with new
    information ... it should categorize the answers to sections of the menu or create new sections") Where each answer the system wrote stands on its
    page: under the topic of the checked answer of the same page whose wordings are nearest to its own (the best likeness of any wording of one to any
    wording of the other), where that likeness reaches PLACE_AT; otherwise in the page's part of its own for more questions. An answer about amounts never
    stands among checked answers. Returns {answer id: [nearest checked id or "", likeness]}. Measured on the checked answers themselves (place_eval): how
    often the nearest other checked answer of the same page is of the same topic, by likeness."""
    by = {}
    for k, r in enumerate(rows): by.setdefault(r, []).append(k)
    unit = Wv / np.maximum(np.linalg.norm(Wv, axis=1, keepdims=True), 1e-9)
    def best(i, cands):
        if not cands or i not in by: return "", 0.0
        mi = unit[by[i]]; top, at = -1.0, ""
        for j in cands:
            if j not in by: continue
            v = float((mi @ unit[by[j]].T).max())
            if v > top: top, at = v, A[j]["id"]
        return at, top
    checked = [j for j, a in enumerate(A) if not a["id"].startswith("au_")]
    out = {}
    for i, a in enumerate(A):
        if not a["id"].startswith("au_"): continue
        page = a.get("substance") or (a["pages"][0] if a["pages"] else "")
        cands = [j for j in checked if page in A[j]["pages"]]
        at, v = best(i, cands)
        out[a["id"]] = [at, round(v, 3)]
    return out


def place_eval(A, rows, Wv):
    """Leave one out: each checked answer on a page with topics (data/site/questions.json), placed by the same rule among the OTHER checked answers of
    that page. Prints, for each likeness from which an answer would be placed, how many are placed and how often under their own topic."""
    Q = json.load(open(ROOT / "data/site/questions.json", encoding="utf-8")); topic = {}
    for page, groups in Q.items():
        if page.startswith("_"): continue
        for g in groups:
            for cid, q in g["items"]: topic[(page, cid)] = g["topic"]
    by = {}
    for k, r in enumerate(rows): by.setdefault(r, []).append(k)
    unit = Wv / np.maximum(np.linalg.norm(Wv, axis=1, keepdims=True), 1e-9)
    idx = {a["id"]: j for j, a in enumerate(A)}
    res = []
    for (page, cid), t in topic.items():
        i = idx.get(cid)
        if i is None or i not in by: continue
        cands = [idx[c] for (p, c) in topic if p == page and c != cid and c in idx and idx[c] in by]
        if not cands: continue
        mi = unit[by[i]]; top, at = -1.0, None
        for j in cands:
            v = float((mi @ unit[by[j]].T).max())
            if v > top: top, at = v, j
        res.append((top, topic.get((page, A[at]["id"])) == t))
    for cut in (0.5, 0.55, 0.6, 0.62, 0.65, 0.7, 0.75, 0.8):
        got = [ok for v, ok in res if v >= cut]
        print(f"place: from likeness {cut:.2f}: {len(got)} of {len(res)} placed, under their own topic {sum(got)} ({100 * sum(got) / max(1, len(got)):.0f}%)")

def next_lists(A, sim):
    """Each answer's next questions: the answers nearest by the meaning of their questions, never itself. The same drug
    first: the nearest answers about each of its drugs, in turn. After them come the nearest on each page the answer is
    told on (a drug's page, mixing, drug checking, facts about drug use), so that every such page has some to offer under
    "Read next". Nothing else is ever offered: no answer about another drug that shares no page with it (the senior
    author, 15 November: a cannabis answer offered a cocaine question). An answer alone on its drug and its page has no
    next questions."""
    about = [set(a.get("about") or []) for a in A]
    pages = [set(a["pages"]) for a in A]
    out = []
    for i, a in enumerate(A):
        order = [int(j) for j in np.argsort(-sim[i], kind="stable") if j != i]
        first = lambda h: (h != a["substance"], h)
        nx = []
        # 1. the same drug first
        mine = sorted(about[i], key=first)
        lists = [[j for j in order if h in about[j]] for h in mine]
        want = max(N_NEXT, 3 * len(mine)); k = 0
        while len(nx) < want and any(k < len(l) for l in lists):
            for l in lists:
                if k < len(l) and l[k] not in nx and len(nx) < want: nx.append(l[k])
            k += 1
        # 2. then its pages, until each has enough to offer (an answer about no drug has only these)
        homes = sorted(pages[i], key=first)
        need = N_PAGE if nx else N_NEXT
        lists = [[j for j in order if p in pages[j]] for p in homes]
        got = [sum(1 for j in nx if p in pages[j]) for p in homes]; k = 0
        while any(got[x] < need and k < len(l) for x, l in enumerate(lists)):
            for x, l in enumerate(lists):
                if got[x] < need and k < len(l) and l[k] not in nx:
                    nx.append(l[k])
                    for y, p in enumerate(homes): got[y] += p in pages[l[k]]
            k += 1
        out.append(nx)
    return out


def people_wordings():
    """The ways people ask each answer: the six wordings of phrasings writer 696 (variants) and the three hurried wordings
    of the near-miss readers ("more" in nearmiss_*.json, when those files are there; they are still growing, so a file that
    cannot be read is left out, with a line saying so). The same readers' "near" questions are questions an answer does
    NOT answer: they come back apart, for --eval alone; they are never indexed and never reach the page."""
    var = dict(json.load(open(VARIANTS, encoding="utf-8")).get("variants", {})) if VARIANTS.exists() else {}
    more, near = {}, {}
    for f in sorted(NEARMISS.glob("nearmiss_*.json")):
        try: items = json.load(open(f, encoding="utf-8")).get("items", {})
        except ValueError:
            print(f"insight: {f.name} could not be read (still being written?): left out of this build", file=sys.stderr); continue
        for k, v in items.items():
            more.setdefault(k, []).extend(w for w in (v.get("more") or []) if isinstance(w, str) and w.strip())
            near.setdefault(k, []).extend(w for w in (v.get("near") or []) if isinstance(w, str) and w.strip())
    # (2.26, decision 41) the teachers' ways of asking, where model.json says how many of them an answer is indexed with ("index_teachers"; none
    # when it is not set): the editor's round 0 first (data/verification/insight/variants_teacher.json), then the free models' (data/auto/insight/teachers.json)
    n_t = int(CONFIG.get("index_teachers") or 0)
    if n_t > 0:
        tea = {}
        for f in (NEARMISS / "variants_teacher.json", ROOT / "data" / "auto" / "insight" / "teachers.json"):
            try: d = json.load(open(f, encoding="utf-8"))
            except (OSError, ValueError): continue
            for k, ws in (d.get("variants") or {}).items():
                tea.setdefault(k, []).extend((w.get("w") if isinstance(w, dict) else w) for w in ws if (isinstance(w, str) and w.strip()) or (isinstance(w, dict) and w.get("w")))
        for k, ws in tea.items(): more.setdefault(k, []).extend(list(dict.fromkeys(ws))[:n_t])
    return var, more, near


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    IN, OUT = pathlib.Path(args[0]), pathlib.Path(args[1])
    A = json.load(open(IN, encoding="utf-8"))["answers"]
    var, more, near = people_wordings()
    ids = [a["id"] for a in A]
    drugs = [s["slug"] for s in SUB]
    for a in A: a["about"] = sorted(set(a.get("about") or [p for p in a["pages"] if p in drugs]))
    rows, W_txt = [], []
    for i, a in enumerate(A):
        ws = list(dict.fromkeys([w for w in a["wordings"] if w] + [w for w in var.get(a["id"], []) if isinstance(w, str) and w.strip()] + more.get(a["id"], [])))
        for w in ws: rows.append(i); W_txt.append(w)
    shorts = [a["short"] for a in A]
    docs = [" ".join(a["wordings"]) + " " + a["short"] for a in A]   # word overlap: the site's own wordings and the short answer
    names = names_table(); pat = name_pattern([n for n, _ in names])
    M_txt = [pat.sub("it", w) for w in W_txt]                          # every wording again, with the drug names taken out
    V = embed_all(W_txt + shorts + M_txt)
    Wv, Sv, Mv = V[:len(W_txt)], V[len(W_txt):len(W_txt) + len(shorts)], V[len(W_txt) + len(shorts):]
    # next questions: the answers nearest by the meaning of their questions as the site words them
    site_rows = [k for k, (r, w) in enumerate(zip(rows, W_txt)) if w in A[r]["wordings"]]
    Q = np.zeros((len(A), Wv.shape[1]), np.float32)
    for k in site_rows: Q[rows[k]] += Wv[k]
    Q /= np.maximum(np.linalg.norm(Q, axis=1, keepdims=True), 1e-9)
    nxt = next_lists(A, Q @ Q.T)
    wb, _ = int8(Wv); sb, _ = int8(Sv); mb, _ = int8(Mv)
    slugs = sorted({s for a in A for s in a["about"]} | {s for _, xs in names for s in xs})
    at = {s: k for k, s in enumerate(slugs)}
    out = {"_note": "Pharmakon Insight's index (scripts/insight/build_index.py): vectors of every answer's wordings (W), of the same wordings with the drug names taken out (M) and of its short answer (S) (made with the model named here, int8, each row scaled to unit length by the page); its words for the overlap score; the drugs it is about; the names that name a drug in a question; and the weights, the tiers and the judge (from site/insight/model.json).",
           "model": MODEL, "model_sha256": MODEL_SHA256, "dim": int(Wv.shape[1]), "weights": CONFIG["weights"], "tiers": CONFIG["tiers"], "judge": CONFIG["judge"],
           "ids": ids, "rows": rows, "W": wb, "M": mb, "S": sb, "docs": docs, "slugs": slugs, "about": [[at[s] for s in a["about"]] for a in A],
           "names": [[n, [at[s] for s in xs]] for n, xs in names], "variants": len(var), "more": sum(1 for a in A if more.get(a["id"]))}
    out["scope"] = scope_block()   # 2.5: what makes a question a question about drugs (site/insight/scope.json)
    # 2.22: what a question asks about, where getting it wrong does harm (site/insight/model.json, aspects): each answer is marked once, by ALL its wordings and its short answer
    spoken = [" ".join(w for r, w in zip(rows, W_txt) if r == i) + " " + shorts[i] for i in range(len(A))]
    # ... and, for an answer about a NARROWER case than a question may ask about, by its OWN question as the site words it: each narrow pattern it holds, and whether it names two drugs
    name_of = {n: xs for n, xs in names}
    def two(text):
        seen = []
        for m in pat.finditer(text):
            g = name_of.get(m.group(1).lower())
            if g and g not in seen: seen.append(g)
        # two drugs TOGETHER ("Cocaine with alcohol", "opioid deaths that also involve benzodiazepines"); "people who use meth or amphetamine" names two of a kind, not a mix
        return len(seen) >= 2 and bool(re.search(r"\b(?:with|plus|mix\w*|combin\w*|together|involve[sd]?|alongside|on top of)\b", text, re.I | re.A))
    own = [a["wordings"][0] if a["wordings"] else "" for a in A]
    out["aspects"] = [dict({"name": a["name"], "ask": a["ask"], "has": "".join("1" if re.search(a["has"], s, re.I | re.A) else "0" for s in spoken)}, **({"best": float(a["best"])} if a.get("best") else {}),
                           **({"narrow": [[n, "".join("1" if re.search(n, s, re.I | re.A) else "0" for s in own)] for n in a["narrow"]]} if a.get("narrow") else {}),
                           **({"two": "".join("1" if two(s) else "0" for s in own)} if a.get("two") else {})) for a in CONFIG.get("aspects") or []]
    # 2.5: the list of questions not answered yet (data/site/wanted.json), as a second, small index of the same kind
    wl = wanted_index(json.load(open(IN, encoding="utf-8")).get("wanted") or [], out, names, pat, at)
    if wl: out["wanted"] = wl
    pl = places_index()   # 2.13: the places of the site, found by the meaning of a question (site/insight/places.json)
    if pl: out["places"] = pl
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    place = auto_place(A, rows, Wv)
    if "--place-eval" in sys.argv: place_eval(A, rows, Wv)
    if len(args) > 2:
        pathlib.Path(args[2]).write_text(json.dumps({"ids": ids, "next": nxt, "place": place, "place_at": PLACE_AT}, separators=(",", ":")), encoding="utf-8")
    changed = sum(1 for w, m in zip(W_txt, M_txt) if w != m)
    idset = set(ids); bare = [a["id"] for a in A if not var.get(a["id"]) and not more.get(a["id"])]
    print(f"insight: model {MODEL} (SHA-256 {MODEL_SHA256[:12]}…); {len(ids)} answers, {len(W_txt)} wordings ({sum(len(v) for k, v in var.items() if k in idset)} from the phrasings writer, "
          f"{sum(len(v) for k, v in more.items() if k in idset)} hurried ones from the near-miss readers; {changed} name a drug), {len(names)} names, {OUT.stat().st_size // 1024} KB", file=sys.stderr)
    if bare: print(f"insight: {len(bare)} answers have only the site's own questions to be found by (no wordings written for them yet): {', '.join(bare[:30])}{' …' if len(bare) > 30 else ''}", file=sys.stderr)
    print(f"insight: next questions for {sum(1 for x in nxt if x)} answers ({sum(len(x) for x in nxt)} in all)", file=sys.stderr)
    if "--eval" in sys.argv: evaluate(out, near)


SCOPE_B, SCOPE_E = r"(?<![A-Za-z0-9_])(?:", r")(?![A-Za-z0-9_])"   # a word boundary that reads the same in JavaScript and in Python
UNF_SETS, UNF_PATS = ("ends", "aux", "func", "topic", "nouns", "gap", "join", "who", "whoadj", "help", "do", "det", "be", "open", "verbs", "wants", "pp", "abbr"), ("strand", "whole", "named")
UNF_KNOWN = ("ends", "aux", "func", "topic", "nouns", "gap", "join", "who", "whoadj", "help", "det", "be", "abbr")   # the words that could be asked of any drug ('verbs', 'open', 'wants' only say how a word is read)
UNF_SUBJ = ("i", "you", "we", "they", "he", "she", "it")                                                    # after one of these stands the verb


def verb_forms(x):
    """The -ing and -ed forms a verb with this base form would have (the page's insVerbForms)."""
    f = [x + "ing", x + "ed"]
    if x.endswith("e"): f += [x[:-1] + "ing", x + "d"]
    if x.endswith("ie"): f.append(x[:-2] + "ying")
    if len(x) > 2 and x.endswith("y") and x[-2] not in "aeiou": f.append(x[:-1] + "ied")
    if len(x) >= 2 and x[-1] not in "aeiouwxy" and x[-2] in "aeiou": f += [x + x[-1] + "ing", x + x[-1] + "ed"]
    if x.endswith("c"): f += [x + "king", x + "ked"]
    return f


def verbish(x, vocab):
    """May this word be the base form of a verb, by the model's word list alone (the page's insVerbish)? A word the list
    knows: when it also knows an -ing or -ed form of it. A word it does not know: yes (it may be a verb we do not know),
    unless it has an ending (-ing, -ed, a plural or third-person -s on a word the list knows): then it is not a base form."""
    if not vocab: return True
    if x in vocab: return any(f in vocab for f in verb_forms(x))
    if x.endswith("ing") or x.endswith("ed"): return False
    if x.endswith("s") and not x.endswith("ss") and (x[:-1] in vocab or (x.endswith("es") and x[:-2] in vocab) or (x.endswith("ies") and x[:-3] + "y" in vocab)): return False
    return True


def unfinished_rule(U, names, vocab):
    """The rule 'is this question finished?' ready to use: the lists as sets, the patterns compiled, and every beginning (of
    two letters or more) of a word the rule knows or of a word of a drug's name, for a last word that is still being typed.
    names: every name that names a drug; vocab: the model's vocabulary (a set of words), or None."""
    if not U: return None
    R = {k: set(U.get(k) or []) for k in UNF_SETS}; R.update({k: [re.compile(p) for p in U.get(k) or []] for k in UNF_PATS})
    R["short"] = dict(U.get("short") or {}); R["known"] = set().union(*(R[k] for k in UNF_KNOWN)) | set(R["short"]); R["vocab"] = vocab
    of_names = set()
    for n in list(names) + list(U.get("names") or []): of_names.update(x for x in re.findall(r"[a-z0-9]+", n.lower()) if len(x) >= 4)
    begin = lambda words, start: {w[:i] for w in words for i in range(start, len(w))} - {w[:-1] for w in words if w.endswith("s")}   # (a word without its plural s is a word)
    R["begin"] = begin(R["known"], 2); R["begin_name"] = begin(of_names, 3)
    return R


UNK_ENDS = (("s", ""), ("es", ""), ("ies", "y"), ("ed", ""), ("ed", "e"), ("d", ""), ("ing", ""), ("ing", "e"), ("ly", ""), ("er", ""), ("est", ""))


def unknown_words(q, vocab, known=()):
    """The words of a question that are not words the model knows (the page's insUnknown): three letters or more, not in
    its vocabulary with or without an ending, not a word of the unfinished rule's lists. A question that is not about
    drugs by its words and holds one gets "We do not know <word>. If it is a drug, send us your question"."""
    t = re.sub(r"['\u2019](?:s|re|ve|ll|d|m)\b", " ", re.sub(r"n['\u2019]t\b", " not", str(q).lower())); out = []
    for w in dict.fromkeys(re.findall(r"[a-z]{3,}", t)):
        if w in known: continue
        forms = [w] + [w[:-len(end)] + put for end, put in UNK_ENDS if len(w) > len(end) + 2 and w.endswith(end)]
        if not any(f in vocab for f in forms): out.append(w)
    return out


def stranger(R, q):
    """The unknown word or words (three at most) of a question whose other words could be asked of any drug, in the order
    typed ("is tusi dangerous": "tusi"; "what is mytragina javanica": "mytragina javanica"), or "" (the page's insStranger).
    R: a Ranker or WordRules. What the half-hourly run looks up in open name lists (scripts/auto/names_open.py, learn)."""
    U = R.unfin
    if not U: return ""
    unk = unknown_words(q, U["vocab"] or set(), U["known"])
    if not unk or len(unk) > 3: return ""
    toks = [x for x in (y.strip("'") for y in re.findall(r"[a-z0-9']+", str(q).lower().replace("\u2019", "'"))) if x]
    rest = [x for x in toks if x not in unk]
    if not rest or not all(x in U["known"] for x in rest): return ""
    return " ".join(dict.fromkeys(x for x in toks if x in unk))


LEARNED = ROOT / "data" / "auto" / "names" / "learned.json"


LEARNED_LANGUAGE = ROOT / "data" / "auto" / "language" / "learned.json"


def learned_verbs():
    """The verbs the school learned by itself (scripts/auto/language.py; docs/AUTOMATION.md, decision 28): words it found used
    as verbs in questions people really typed, which the model's word list does not show to be verbs. They join the rule's
    own list ('unfinished.verbs' of site/insight/scope.json), so the page and the build read the same list. Only plain
    words of 3 to 14 letters with their evidence beside them count. No file: nothing learned yet."""
    try: L = json.load(open(LEARNED_LANGUAGE, encoding="utf-8")).get("verbs") or {}
    except (OSError, ValueError, AttributeError): return []
    return sorted(w for w, e in L.items() if isinstance(w, str) and re.fullmatch(r"[a-z]{3,14}", w) and isinstance(e, dict) and int(e.get("in_a_verbs_place") or 0) >= 3 and e.get("forms"))


ASK_WORDS = ("who", "whom", "whose", "what", "when", "where", "which", "why", "how", "is", "are", "was", "were", "do", "does", "did", "can", "could", "will", "would", "should", "has", "have", "had", "may", "might", "must")


def ending_pattern(pairs):
    """One pattern for the endings the school learned (scripts/auto/language.py, lesson 3): a question that begins as a question
    does (a question word or a helper verb) and ends on one of these pairs of words ("played in", "named after") is finished,
    though its last word is one a question usually cannot end on. "" when there is none. The same string for the page and the build."""
    pairs = sorted({p for p in pairs if isinstance(p, str) and re.fullmatch(r"[a-z]{2,14} [a-z]{2,8}", p)})
    return "^(?:" + "|".join(ASK_WORDS) + ")\\b.* (?:" + "|".join(pairs) + ")$" if pairs else ""


def learned_endings():
    """The endings the school learned by itself (data/auto/language/learned.json, "endings"): only two plain words, each with its count of real questions (five or more)."""
    try: L = json.load(open(LEARNED_LANGUAGE, encoding="utf-8")).get("endings") or {}
    except (OSError, ValueError, AttributeError): return []
    return sorted(p for p, e in L.items() if isinstance(p, str) and re.fullmatch(r"[a-z]{2,14} [a-z]{2,8}", p) and isinstance(e, dict) and int(e.get("questions") or 0) >= 5)


def learned_names():
    """(names, phrases) from data/auto/names/learned.json (scripts/auto/names_open.py, learn; decision 27, step a): the names
    the system looked up in open name lists and found to be drugs, in small letters, and what people typed for them
    ({what was typed: the name as it is written}). Only entries marked as a drug count. No file: nothing learned yet."""
    try: L = json.load(open(LEARNED, encoding="utf-8")).get("names") or {}
    except (OSError, ValueError, AttributeError): return [], {}
    names, phr = [], {}
    for key, e in sorted(L.items()):
        if not (isinstance(e, dict) and e.get("drug") is True and re.fullmatch(r"[a-z][a-z -]{3,60}", key)): continue
        names.append(key)
        for t in e.get("typed") or []:
            if isinstance(t, str) and re.fullmatch(r"[a-z]{3,30}(?: [a-z]{3,30}){0,2}", t) and t != key: phr[t] = str(e.get("name") or key)
    return names, phr


SPELL_WORD = re.compile(r"(?<![A-Za-z0-9'\u2019-])[A-Za-z]+(?![A-Za-z0-9'\u2019-])")


def near(a, b):
    """Are two words one letter apart: a letter put in, left out or changed, or two neighbours swapped (the page's insNear)?"""
    la, lb = len(a), len(b)
    if a == b or abs(la - lb) > 1: return False
    i = 0
    while i < la and i < lb and a[i] == b[i]: i += 1
    if la == lb: return a[i + 1:] == b[i + 1:] or (i + 1 < la and a[i] == b[i + 1] and a[i + 1] == b[i] and a[i + 2:] == b[i + 2:])
    return a[i:] == b[i + 1:] if la < lb else a[i + 1:] == b[i:]


def spell_rule(Sp, names, other, vocab, known):
    """The rule 'a drug's name with a letter wrong' ready to use (site/insight/scope.json, "spell"). names: {a name the page
    knows: the drugs it stands for}; other: the names of drugs without a page; vocab: the model's vocabulary; known: the
    words of the unfinished rule's lists."""
    if Sp is None: return None
    group = {n: "|".join(g) for n, g in names.items()}; group.update({n: "other:" + n for n in other if n not in group})
    # (2.9.3) what people typed for a name the system learned ("mytragina javanica"), read as that name before the words are read
    phr = dict(Sp.get("phr") or {})
    phr_re = re.compile(r"(?<![A-Za-z0-9'\u2019-])(?:" + "|".join(r"\s+".join(re.escape(w) for w in k.split(" ")) for k in sorted(phr, key=lambda k: (-len(k), k))) + r")(?![A-Za-z0-9'\u2019-])", re.I) if phr else None
    return {"map": dict(Sp.get("map") or {}), "keep": set(Sp.get("keep") or []), "exact": set(group), "vocab": vocab or set(), "known": set(known), "phr": phr, "phr_re": phr_re,
            "targets": sorted((n for n in group if len(n) >= 6 and re.fullmatch(r"[a-z]+", n)), key=lambda n: (-len(n), n)), "group": group}


def spell_word(R, w, scope_re):
    """The name a word is read as, or None (w in small letters)."""
    if w in R["map"]: return R["map"][w]
    if len(w) < 5 or w in R["exact"] or w in R["keep"] or w in R["known"]: return None
    forms = [w] + [w[:-len(end)] + put for end, put in UNK_ENDS if len(w) > len(end) + 2 and w.endswith(end)]
    if any(f in R["vocab"] for f in forms): return None                                    # a word
    for end in ("s", "es"):                                                                 # a name with a plural or possessive s: the name
        if len(w) > len(end) + 2 and w.endswith(end) and w[:-len(end)] in R["exact"]: return w[:-len(end)]
    if any(f in R["exact"] for f in forms[1:]) or (scope_re is not None and scope_re.search(w)): return None   # a name with another ending, or drug talk
    hits = [n for n in R["targets"] if abs(len(n) - len(w)) <= 1 and near(w, n)]
    if not hits or len({R["group"][n] for n in hits}) != 1: return None
    return hits[0]


def vocabulary():
    """The model's vocabulary as a set of whole words (site/insight/vendor/vocab.txt, the file the page reads)."""
    try: return {l.rstrip("\n").rstrip() for l in open(VENDOR / "vocab.txt", encoding="utf-8")}
    except OSError: return None


def scope_block():
    """The scope rule as the index carries it: 'src', one pattern of every drug word, every name of a drug the site does
    not cover and the shape of a research chemical's name; 'not', one pattern of the phrases taken out first. The page
    (insPrepare) and the Ranker put the same word boundaries around them. site/insight/scope.json explains the rule."""
    S = json.load(open(ROOT / "site" / "insight" / "scope.json", encoding="utf-8"))
    plain = lambda n: re.sub(r"([.^$*+?()\[\]{}|\\])", r"\\\1", n)
    src = "|".join(["(?:" + w + ")" for w in S["words"]] + [plain(n) for n in S["names"]] + ["(?:" + S["chem"] + ")"])
    U = S.get("unfinished") or {}
    # (2.9.3) the names the system learned by looking them up (data/auto/names/learned.json) are names of drugs the site does not cover yet
    more, phr = learned_names(); S = dict(S, names=list(S["names"]) + [n for n in more if n not in S["names"]])
    src = "|".join(["(?:" + w + ")" for w in S["words"]] + [plain(n) for n in S["names"]] + ["(?:" + S["chem"] + ")"])
    # (2.9) is a question finished? the page's insUnfinished and Ranker.unfinished read the same lists and patterns; 'names':
    # the names of drugs the site does not cover, for a name that is still being typed
    unf = {k: sorted(set(U.get(k) or [])) for k in UNF_SETS}; unf.update({k: list(U.get(k) or []) for k in UNF_PATS}); unf["names"] = sorted(set(S["names"]))
    # (2.15) the verbs the school learned by itself: never a word the rule's other lists already read another way
    other = set().union(*(set(U.get(k) or []) for k in UNF_SETS if k != "verbs"))
    unf["verbs"] = sorted(set(unf["verbs"]) | {w for w in learned_verbs() if w not in other})
    pat = ending_pattern(learned_endings())
    if pat: unf["strand"] = list(unf["strand"]) + [pat]
    unf["short"] = dict(sorted((U.get("short") or {}).items()))
    # (2.9.1) a drug's name with a letter wrong: 'map' (only to names the site knows) and 'keep'; the names of drugs without a page are in unfinished.names
    Sp = S.get("spell") or {}; known = {n for n, _ in names_table()} | set(S["names"])
    spell = {"map": {k: v for k, v in sorted((Sp.get("map") or {}).items()) if v in known and k not in known}, "keep": sorted(set(Sp.get("keep") or [])),
             "phr": {k: v for k, v in sorted(phr.items()) if k not in known}}
    for k, v in sorted((Sp.get("map") or {}).items()):
        if k not in spell["map"]: print(f"NOTE: scope.json spell.map: “{k}” -> “{v}” left out ({'the word is itself a name' if k in known else 'not a name the site knows'})")
    return {"src": src, "not": "|".join("(?:" + w + ")" for w in S["not"]), "unfinished": unf, "spell": spell}


WANT_CUT = 0.75            # the judge's number from which a typed question can be a listed one (see wanted_index)
WANT_NEAR = [0.70, 0.70]   # and how near its best wording must be: with the drug's name, and with the drug names taken out


PLACES = ROOT / "site/insight/places.json"


def places_table():
    """site/insight/places.json: the places of the site with the ways people ask for what each holds, and the entries that say
    what is not a place ('none')."""
    try: D = json.load(open(PLACES, encoding="utf-8"))
    except (OSError, ValueError): return None
    P = [p for p in D.get("places") or [] if isinstance(p, dict) and p.get("id") and p.get("ways")]
    for p in P: p["ways"] = list(dict.fromkeys(str(x).strip().lower() for x in p["ways"] if isinstance(x, str) and x.strip()))
    return {"cut": float(D.get("cut", 0.8)), "near": float(D.get("near", 0.66)), "places": P} if P else None


def places_index():
    """(2.13, 17 November 2026; the senior author asked "how can i use test kits at home", was told "We haven't checked exactly
    this yet" although the site has a part on test kits to use at home, and wrote: "we have to incorporate every instance of
    human language it is still stupid".) The places of the site as a third small index: every way of asking for a place as
    the model's numbers. The page compares a question (its drug names read as "it") with every way and takes the place of
    the nearest one (insWhere; here: where). An entry marked 'none' is not a place: when its way is the nearest, the
    question asks for an answer and is led nowhere ("does it show up on a drug test" is not drug checking)."""
    T = places_table()
    if not T: return None
    rows, W = [], []
    for i, p in enumerate(T["places"]):
        for w in p["ways"]: rows.append(i); W.append(w)
    wb, _ = int8(embed_all(W))
    print(f"insight: {sum(1 for p in T['places'] if not p.get('none'))} places of the site can be found by the meaning of a question ({len(W)} ways of asking; "
          f"{sum(1 for p in T['places'] if p.get('none'))} entries say what is not a place)", file=sys.stderr)
    return {"ids": [p["id"] for p in T["places"]], "rows": rows, "W": wb, "cut": T["cut"], "near": T["near"],
            "meta": [{"none": 1} if p.get("none") else {k: p[k] for k in ("href", "icon", "k", "t", "part", "topic") if p.get(k)} for p in T["places"]]}


def where(Wv, rows, n, mv):
    """The page's insWhere: (the entry whose nearest way is nearest to the question, how near)."""
    s = Wv @ mv; best = np.full(n, -1.0)
    for k, i in enumerate(rows):
        if s[k] > best[i]: best[i] = s[k]
    i = int(best.argmax()); return i, float(best[i])


def measure_places(show=True):
    """How well the look for a place by meaning does (no index needed, the model is): on the questions written for it
    (data/verification/insight/places-gold.json, none of them a way of the table), on the 1,021 forum questions and on the
    165 questions about other things. A question is read as the page reads it: a misspelt name as the name, every drug's
    name as "it". Prints what is sent where, for the editor to read; returns the numbers."""
    T = places_table(); P = T["places"]; R = WordRules()
    G = json.load(open(ROOT / "data/verification/insight/places-gold.json", encoding="utf-8"))["questions"]
    forum = forum_questions(); other = json.load(open(ROOT / "data/verification/insight/scope-other.json", encoding="utf-8"))["questions"]
    rows, W = [], []
    for i, p in enumerate(P):
        for w in p["ways"]: rows.append(i); W.append(w)
    ways = set(W); again = [g["q"] for g in G if g["q"].strip().lower() in ways]
    read = lambda qs: [R.pat.sub("it", R.correct(q)[0]).lower() for q in qs]
    V = embed_all(W + read([g["q"] for g in G]) + read(forum) + read(other), quiet=True); _, Wv = int8(V[:len(W)])
    a, b = len(W), len(W) + len(G); c = b + len(forum)
    look = lambda v: (lambda i, s: (P[i]["id"], s, bool(P[i].get("none"))))(*where(Wv, rows, len(P), v))
    topic = {p["id"] for p in P if p.get("topic")}   # (2.22) a part of the Big questions page: a place to look, never the answer
    g = [look(v) for v in V[a:b]]; f = [look(v) for v in V[b:c]]; o = [look(v) for v in V[c:]]
    near, cut = T["near"], T["cut"]
    out = {"places": sum(1 for p in P if not p.get("none")), "ways": len(W), "near": near, "cut": cut, "gold": len(G), "gold_also_a_way": len(again),
           "gold_right": sum(1 for x, (pid, s, none) in zip(G, g) if s >= near and pid == x["place"]), "gold_wrong_place": sum(1 for x, (pid, s, none) in zip(G, g) if s >= near and not none and pid != x["place"]),
           "gold_right_as_the_answer": sum(1 for x, (pid, s, none) in zip(G, g) if s >= cut and pid == x["place"] and pid not in topic), "gold_wrong_as_the_answer": sum(1 for x, (pid, s, none) in zip(G, g) if s >= cut and not none and pid != x["place"] and pid not in topic),
           "forum": len(forum), "forum_sent_to_a_place": sum(1 for pid, s, none in f if s >= near and not none), "forum_as_the_answer": sum(1 for pid, s, none in f if s >= cut and not none and pid not in topic),
           "forum_held_back_as_not_a_place": sum(1 for pid, s, none in f if s >= near and none),
           "other": len(other), "other_sent_to_a_place": sum(1 for pid, s, none in o if s >= near and not none),
           "other_read_as_about_drugs": sum(1 for pid, s, none in o if s >= near and not none and pid in topic)}   # (2.22) nearest to a part of the Big questions page: taken as a question about drugs
    if show:
        print(f"places by meaning: {out['places']} places, {out['ways']} ways; a place to look from {near}, the answer from {cut}")
        print(f"  the {len(G)} questions written for it: the right place {out['gold_right']}, a wrong place {out['gold_wrong_place']}, none {len(G) - out['gold_right'] - out['gold_wrong_place']}; as the answer: right {out['gold_right_as_the_answer']}, wrong {out['gold_wrong_as_the_answer']}")
        for x, (pid, s, none) in zip(G, g):
            if not (s >= near and pid == x["place"]): print(f"    not found: {s:.2f} {pid} (wanted {x['place']}) | {x['q']}")
        print(f"  the {len(forum)} forum questions: sent to a place {out['forum_sent_to_a_place']} (as the answer {out['forum_as_the_answer']}); held back because the nearest way is not a place {out['forum_held_back_as_not_a_place']}")
        for q, (pid, s, none) in zip(forum, f):
            if s >= near and not none: print(f"    {s:.2f} {pid} | {q}")
        print(f"  the {len(other)} questions about other things: sent to a place {out['other_sent_to_a_place']}")
        for q, (pid, s, none) in zip(other, o):
            if s >= near and not none: print(f"    {s:.2f} {pid} | {q}")
        if again: print("  !! questions of the measure that are also ways of the table (they measure nothing):", again)
    return out


def wanted_index(items, out, names, pat, at):
    """The list of questions the site does not answer yet (site 2.5; the senior author, 15 November 2026: "make the site
    understand on its own what the users want added in the website in-app and not via email"). When no answer is a best
    match, the page takes a second look, at this list, with the same ranking and the same judge: a typed question that is
    one of the listed questions gets "Not answered yet. It is on our list", and the site counts one more person asking
    it, by the item's number alone (the words never leave the device).

    Each item is indexed as an answer is: its question and its other ways of asking as the wordings, its question again
    as the short line. An item the site answers by now (its own question gets a best match among the answers) is left
    out, so the list empties itself as answers are written. How well this finds a listed question was measured on
    answered questions standing in for listed ones (42 at random, five times; hurried rewordings held out): with the
    question alone 10 in 100 found their item; with six ways of asking and the judge at 0.75, 82 in 100, none a wrong
    item, and 4 in 100 questions that were not on the list were taken for a listed one (at the answers' own cut, 0.60:
    87 and 6). So every item carries six ways, and the cut for the list is 0.75 (WANT_CUT).

    The judge alone is not enough, and real questions showed it (15 November 2026, the 1,021 forum questions of the
    harvest, 845 of them without a best match). On a small list an item often stands alone for its drug, so the judge's
    sixth number (the lead over the next candidate) is always large: the judge took 52 forum questions for a listed
    one and 26 of them wrongly, most of them any question about Adderall for the one listed question that names it.
    What tells them apart is how near the best wording is in both looks, with the drug's name and with the drug names
    taken out: asking 0.70 of each (WANT_NEAR) leaves 20 taken, 18 of them the listed question and 2 a neighbouring
    one, and of held-out rewordings 74 in 100 still find their item (a wrong item 0.2; a question not on the list 1.9).
    Stricter (0.80 of each): 8 taken, none wrong, 53 in 100. A typed question that is missed loses nothing (it gets
    "We haven't checked exactly this yet" and the one tap that sends it); one taken wrongly would be shown another
    question as its own. So the page says "A question like yours is on our list", which is true of a neighbouring
    question too, and keeps "Not the same? Send yours to us"."""
    if not items: return None
    R = Ranker(out); keep, gone = [], []
    for w in items:
        k = R.rank(w["q"])
        (gone if k["best"] else keep).append((w, k["best"][0]["id"] if k["best"] else None))
    if gone: print("insight: " + str(len(gone)) + " listed questions are answered by now and left off the list: " + ", ".join(w["id"] + " by " + c for w, c in gone), file=sys.stderr)
    items = [w for w, _ in keep]
    if not items: return None
    rows, W_txt = [], []
    for i, w in enumerate(items):
        for t in list(dict.fromkeys([w["q"]] + [x for x in w.get("ways") or [] if isinstance(x, str) and x.strip()])): rows.append(i); W_txt.append(t)
    shorts = [w["q"] for w in items]; M_txt = [pat.sub("it", t) for t in W_txt]
    V = embed_all(W_txt + shorts + M_txt)
    Wv, Sv, Mv = V[:len(W_txt)], V[len(W_txt):len(W_txt) + len(shorts)], V[len(W_txt) + len(shorts):]
    wb, _ = int8(Wv); sb, _ = int8(Sv); mb, _ = int8(Mv)
    name_of = {n: xs for n, xs in names}
    about = []
    for w in items:   # the drugs an item is about: the ones its question names (a family's name: every drug of it), and the ones the list itself gives it ("drugs": a K-hole is about ketamine)
        ab = set(w.get("drugs") or [])
        for m in pat.finditer(w["q"]): ab |= set(name_of.get(m.group(1).lower(), []))
        about.append(sorted(at[s] for s in ab if s in at))
    print(f"insight: {len(items)} questions on the list of those not answered yet, {len(W_txt)} wordings", file=sys.stderr)
    # (2.26.2) each item's research words (the words papers use for its subject: the editor's or the system's), for the page's own look-up of published research
    terms = [[str(t)[:60] for t in (w.get("terms") or []) if isinstance(t, str) and t.strip()][:6] for w in items]
    return {"ids": [w["id"] for w in items], "q": shorts, "rows": rows, "W": wb, "M": mb, "S": sb, "docs": [" ".join(dict.fromkeys([w["q"]] + (w.get("ways") or []))) for w in items], "about": about, "cut": WANT_CUT, "near": WANT_NEAR, "terms": terms}


def evaluate(D, near=None):
    """The page's rule on the gold set's forum questions (full answer: either reader names an answer that fully answers
    it; partial: a reader names it as answering part; unanswerable: both readers say none does), printed as
    scripts/insight/judge2.py prints it: the best matches at the judge's cut of model.json and at other cuts, on the
    odd-numbered questions (dev: where a cut is chosen), the even-numbered ones (test: where it is reported) and all; the
    related answers at each cut; and the near-miss readers' questions (each written as a question one answer does NOT
    answer: is that answer given as its best match?)."""
    G = json.load(open(ROOT / "data/verification/insight/gold-sample.json", encoding="utf-8"))["questions"]
    readers = [json.load(open(f, encoding="utf-8"))["labels"] for f in sorted(glob.glob(str(ROOT / "data/verification/insight/gold_reader*.json")))]
    lab = {}
    for R in readers:
        for x in R: lab.setdefault(x["n"], []).append(x)
    R = Ranker(D); idset = set(R.ids); tests = []
    for g in G:
        ls = lab.get(g["n"], [])
        if len(ls) < len(readers): continue
        full = {a for x in ls for a in x.get("answers", []) if a in idset}
        part = {a for x in ls for a in x.get("partly", []) if a in idset} - full
        tests.append((g["n"], g["question"], full, part, all(x.get("none") for x in ls)))
    def looks(questions):
        tx = [R.texts(q) for q in questions]; V = embed_all([t[0] for t in tx] + [t[1] for t in tx])
        return [R.look(V[i], V[len(tx) + i], questions[i], tx[i][2]) for i in range(len(tx))]
    LG = looks([t[1] for t in tests])
    n_full = sum(bool(t[2]) for t in tests); n_un = sum(t[4] for t in tests)
    order = [np.argsort(-L["by"], kind="stable") for L in LG]
    h1 = sum(R.ids[o[0]] in tests[i][2] for i, o in enumerate(order) if tests[i][2]) / n_full
    h3 = sum(any(R.ids[j] in tests[i][2] for j in o[:3]) for i, o in enumerate(order) if tests[i][2]) / n_full
    print(f"model {D['model']}; gold questions: {len(tests)}; {n_full} with a full answer, {n_un} unanswerable; candidates in order of first look + weights.topic x topic: a full answer first {h1 * 100:.1f}%, in the first three {h3 * 100:.1f}%")
    print("judge weights (on standardized numbers):", {f: round(float(w), 2) for f, w in zip(R.J["features"], R.J["w"])}, "bias", round(float(R.J["b"]), 2), "; a best match from", R.J["best"])
    keep = R.J; cuts = sorted({0.5, 0.6, 0.7, 0.8, float(keep["best"])})
    # the near-miss questions: (question, the answer it must not get), for answers on the page
    nm = [(q, a) for a, qs in sorted((near or {}).items()) if a in idset for q in qs]
    LN = looks([q for q, _ in nm]) if nm else []
    def ranked(L): return R.tiers(L["plain"], L["topic"], L["groups"], lambda c: R.six(L, c), L.get("q"))
    for split, use in (("dev (odd-numbered)", lambda n: n % 2 == 1), ("test (even-numbered)", lambda n: n % 2 == 0), ("all", lambda n: True)):
        rs = [(t, L) for t, L in zip(tests, LG) if use(t[0])]
        nun = sum(t[4] for t, _ in rs); nf = sum(bool(t[2]) for t, _ in rs)
        print(f"gold, {split}: {len(rs)} questions")
        for th in cuts:
            R.J = dict(keep, best=th); b = f = p = un = 0; rel = {"rows": 0, "good": 0, "q": 0, "un": 0}; miss = 0
            for (nq, q, full, part, u), L in rs:
                best, related, _ = ranked(L)
                if best: a = R.ids[best[0]]; b += 1; f += a in full; p += a in part; un += u
                elif full and any(R.ids[j] in full for j in related): miss += 1
                if related:
                    rel["q"] += 1; rel["rows"] += len(related); rel["un"] += u; rel["good"] += sum(R.ids[j] in full or R.ids[j] in part for j in related)
            w = b - f - p; label = f"judge >= {th:g} (and about the drugs named)" + (" <- model.json" if th == float(keep["best"]) else "")
            print(f"  {label:<46} best match for {b:3d} of {len(rs)}: full {f:3d} ({100 * f / max(1, b):3.0f}%), partial {p:3d} ({100 * p / max(1, b):3.0f}%), wrong {w:3d} ({100 * w / max(1, b):3.0f}%); "
                  f"unanswerable given one {un} of {nun}; questions with a full answer that get it as best match {f} of {nf}; "
                  f"related: {rel['rows']} rows for {rel['q']} questions, {100 * rel['good'] / max(1, rel['rows']):.0f}% full or partial, {rel['un']} of {nun} unanswerable questions get some; "
                  f"no best match but a full answer under Related {miss}")
    # 2.5, the scope rule (words only): the forum questions are all about drugs; scope-other.json holds questions that are not
    if R.scope_re is not None:
        other = json.load(open(ROOT / "data/verification/insight/scope-other.json", encoding="utf-8"))["questions"]
        gq = [t[1] for t in tests]; ins = [R.in_scope(q) for q in gq]; outs = [q for q, x in zip(gq, ins) if not x]; let = [q for q in other if R.in_scope(q)]
        print(f"scope (words only): forum questions taken as about drugs {sum(ins)} of {len(gq)}; questions that are not about drugs taken as about drugs {len(let)} of {len(other)}")
        print("  forum questions not taken as about drugs:", outs)
        print("  other questions taken as about drugs:", let)
    if nm:
        for th in cuts:
            R.J = dict(keep, best=th); hit = sum(any(R.ids[j] == a for j in ranked(L)[0]) for (q, a), L in zip(nm, LN))
            print(f"near-miss questions given the answer they do not get as best match, judge >= {th:g}: {hit} of {len(nm)} ({100 * hit / len(nm):.1f}%)")
    R.J = keep


if __name__ == "__main__":
    if "--words" in sys.argv: print(json.dumps(measure_words(WordRules(), "--quiet" not in sys.argv)))
    elif "--places" in sys.argv: print(json.dumps(measure_places("--quiet" not in sys.argv)))
    else: main()
