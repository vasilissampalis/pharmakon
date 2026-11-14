// Insight (site 2.2.0): the page and the build must make the same numbers. The page tokenizes in JavaScript and runs the
// model with ONNX Runtime Web (site/src/app.insight.js); the build (scripts/insight/build_index.py) tokenizes with the
// tokenizers library in Python and runs the model with the same ONNX Runtime Web files under Node (scripts/insight/embed.js).
// This runs both on the same texts (site questions, readers' wordings, real forum questions, and awkward ones: accents,
// punctuation, Chinese and Greek, emoji, special tokens, control characters, a word over 100 letters, text past 128 tokens)
// and requires the same tokens, cosine >= 0.999 between the two vectors of every text, the same drug names added, and the
// same answers ranked first and shown, with the same scores to within 0.005, for real questions. As an independent check of
// the model itself it also compares the page with the Python onnxruntime (eval_match.py's MiniLM class), whose int8 kernels
// round a little differently on a PC: it must agree to cosine >= 0.99 for every text.
// Usage: node scripts/insight/parity.js [--port N]   (build first: node site/build.js && python3 -I site/build_public.py)
const http = require("http"), fs = require("fs"), path = require("path"), { spawnSync } = require("child_process");
const { chromium } = require("playwright");
const REPO = path.resolve(__dirname, "..", ".."), ROOT = path.join(REPO, "site", "public");
const arg = k => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : null; };
const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".mjs": "text/javascript", ".wasm": "application/wasm", ".json": "application/json", ".css": "text/css", ".txt": "text/plain; charset=utf-8" };
if (!fs.existsSync(path.join(ROOT, "data", "insight.json"))) { console.error("No site/public/data/insight.json: build first."); process.exit(2); }
const readJ = f => JSON.parse(fs.readFileSync(path.join(REPO, f), "utf8"));
// the texts: every 7th site question, every 40th reader wording, every 8th forum question of the gold set, and the awkward ones
const QS = readJ("data/site/questions.json"); delete QS._note;
const site = [...new Set(Object.values(QS).flatMap(gs => gs.flatMap(g => g.items.map(it => it[1]).filter(Boolean))))].filter((_, i) => i % 7 === 0).slice(0, 20);
const V = fs.existsSync(path.join(REPO, "data/verification/insight/variants_reader696.json")) ? readJ("data/verification/insight/variants_reader696.json").variants : {};
const wordings = Object.values(V).flat().filter((_, i) => i % 40 === 0).slice(0, 15);
const gold = readJ("data/verification/insight/gold-sample.json").questions.map(q => q.question).filter((_, i) => i % 8 === 0).slice(0, 15);
const odd = ["Café crème, ñandú and Ångström: naïve façade", "WHAT'S UP?! (really) — 'quotes' & “curly” stuff... #1 @home 50% $5", "1,4-butanediol, 2C-B, 3-MMC and 4-FA (e.g. N2O)",
  "大麻は安全ですか", "Είναι ασφαλές το MDMA; ΣΊΓΜΑ ΤΕΛΟΣ", "is 🍄 safe? 😅👍🏽", "[CLS] what [SEP] is [MASK] really[UNK]", "tab\there\nnew line\u0000nul​zero width nbsp",
  "a" + "bcdefghij".repeat(12) + " and a short word", Array.from({ length: 90 }, (_, i) => "word" + i + " ok").join(" "), "İstanbul ǅemal ﬁne Straße", "Mixing molly, xanax and booze?"];
const texts = site.concat(wordings, gold, odd);
const queries = gold.slice(0, 10).concat(["does ecstasy damage your brain permanently", "can you fail a drug test from secondhand weed smoke", "how long does ketamine stay in your blood",
  "what does an opioid overdose look like", "is it dangerous to mix molly and alcohol", "does weed make you lazy", "can lsd stay in your spine", "what is the capital of mongolia", "how addictive is meth", "is nitrous bad for you"]);
// the build's side, in Python
const py = `
import sys, json, base64, importlib.util, numpy as np
spec = importlib.util.spec_from_file_location("bi", sys.argv[1]); bi = importlib.util.module_from_spec(spec); spec.loader.exec_module(bi)
req = json.load(sys.stdin); tok = bi.tokenizer(); enc = bi.encoder(); expand = bi.drug_names()
texts = req["texts"]; ids = [tok.encode(t).ids for t in texts]
out = {"ids": ids, "vecs": bi.embed_ids(ids).tolist(), "pyvecs": [enc([t])[0].tolist() for t in texts], "expand": [expand(t) for t in texts + req["queries"]]}
D = json.load(open(sys.argv[2], encoding="utf-8")); dim = D["dim"]
def rows(b):
    q = np.frombuffer(base64.b64decode(b), dtype=np.int8).astype(np.float32).reshape(-1, dim)
    return q / np.maximum(np.linalg.norm(q, axis=1, keepdims=True), 1e-9)
W, S = rows(D["W"]), rows(D["S"]); lex = bi.Words(D["docs"]); wt = D["weights"]; n = len(D["ids"])
rank = []
Q = bi.embed_ids([tok.encode(expand(q)).ids for q in req["queries"]])
for q, v in zip(req["queries"], Q):
    sw = W @ v; best = np.full(n, -1.0, np.float32)
    for k, r in enumerate(D["rows"]): best[r] = max(best[r], sw[k])
    sc = wt["q"] * best + wt["short"] * (S @ v) + wt["words"] * lex.sims(q)
    order = list(np.argsort(-sc)[:3])
    top = [D["ids"][i] for k, i in enumerate(order) if sc[order[0]] >= D["threshold"] and (k == 0 or sc[i] >= D["also"])]
    rank.append({"cand": [D["ids"][i] for i in order], "scores": [round(float(sc[i]), 4) for i in order], "ids": top})
out["rank"] = rank
print(json.dumps(out))
`;
const r = spawnSync("python3", ["-I", "-c", py, path.join(REPO, "scripts/insight/build_index.py"), path.join(ROOT, "data/insight.json")], { input: JSON.stringify({ texts, queries }), maxBuffer: 1 << 28, encoding: "utf8" });
if (r.status !== 0) { console.error(r.stderr); process.exit(2); }
const ref = JSON.parse(r.stdout);
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split("?")[0]); if (p.endsWith("/")) p += "index.html";
  const f = path.join(ROOT, path.normalize(p)); if (!f.startsWith(ROOT)) { res.writeHead(403); res.end(); return; }
  fs.readFile(f, (err, buf) => { if (err) { res.writeHead(404); res.end(); return; } res.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream" }); res.end(buf); });
});
(async () => {
  await new Promise(ok => server.listen(+(arg("--port") || 0), "127.0.0.1", ok));
  const browser = await chromium.launch({ args: ["--no-proxy-server"] }), p = await browser.newPage();
  const errors = []; p.on("pageerror", e => errors.push(String(e))); p.on("console", m => { if (m.type() === "error") errors.push(m.text()); });
  await p.goto("http://127.0.0.1:" + server.address().port + "/#home"); await p.waitForTimeout(500);
  const loaded = await p.evaluate(() => pkInsight.load());
  if (!loaded) { console.error("Insight did not load in the page", errors); process.exit(1); }
  const js = await p.evaluate(async ({ texts, queries }) => {
    const out = { ids: [], vecs: [], expand: [], rank: [] };
    for (const t of texts) { out.ids.push(pkInsight.encode(t)); out.vecs.push(await pkInsight.embed(t)); }
    for (const t of texts.concat(queries)) out.expand.push(pkInsight.expand(t));
    for (const q of queries) out.rank.push(await pkInsight.rank(q));
    return out;
  }, { texts, queries });
  await browser.close(); server.close();
  let fails = 0; const say = (pass, name, detail) => { if (!pass) fails++; console.log((pass ? "PASS " : "FAIL ") + name + (detail ? "  (" + detail + ")" : "")); };
  const tokBad = texts.map((t, i) => JSON.stringify(js.ids[i]) === JSON.stringify(ref.ids[i]) ? null : JSON.stringify(t.slice(0, 40)) + ": page " + js.ids[i].slice(0, 12) + " / build " + ref.ids[i].slice(0, 12)).filter(Boolean);
  say(!tokBad.length, "the same tokens for all " + texts.length + " texts", tokBad.slice(0, 3).join("; ") || (Math.max(...ref.ids.map(x => x.length)) + " tokens at most"));
  const cosOf = (A, B) => texts.map((_, i) => { const a = A[i], b = B[i]; let d = 0, na = 0, nb = 0; for (let j = 0; j < a.length; j++) { d += a[j] * b[j]; na += a[j] * a[j]; nb += b[j] * b[j]; } return d / Math.sqrt(na * nb); });
  const cos = cosOf(js.vecs, ref.vecs), worst = cos.indexOf(Math.min(...cos)), same = texts.filter((_, i) => js.vecs[i].every((x, j) => Math.fround(x) === Math.fround(ref.vecs[i][j]))).length;
  say(cos.every(c => c >= 0.999), "cosine >= 0.999 between the page's and the build's vectors for every text", "lowest " + cos[worst].toFixed(6) + " for " + JSON.stringify(texts[worst].slice(0, 50)) + "; " + same + " of " + texts.length + " bit-identical");
  const pc = cosOf(js.vecs, ref.pyvecs), pw = pc.indexOf(Math.min(...pc)), ps = pc.slice().sort((a, b) => a - b);
  say(pc.every(c => c >= 0.99), "independent check, the Python onnxruntime: cosine >= 0.99 against the page for every text", "median " + ps[ps.length >> 1].toFixed(6) + ", " + pc.filter(c => c >= 0.999).length + " of " + texts.length + " at 0.999 or more, lowest " + pc[pw].toFixed(6) + " for " + JSON.stringify(texts[pw].slice(0, 40)));
  const exBad = js.expand.map((x, i) => x === ref.expand[i] ? null : JSON.stringify(x) + " / " + JSON.stringify(ref.expand[i])).filter(Boolean);
  say(!exBad.length, "the same drug names added to " + js.expand.length + " texts", exBad.slice(0, 3).join("; ") || js.expand.filter((x, i) => x !== texts.concat(queries)[i]).length + " of them get names");
  const rkBad = queries.map((q, i) => { const a = js.rank[i], b = ref.rank[i], diff = Math.max(...a.scores.map((s, k) => Math.abs(s - b.scores[k])));
    return a.cand[0] === b.cand[0] && JSON.stringify(a.ids) === JSON.stringify(b.ids) && diff <= 0.005 ? null : JSON.stringify(q.slice(0, 40)) + ": page " + a.cand.join(",") + " " + a.scores + " / build " + b.cand.join(",") + " " + b.scores; }).filter(Boolean);
  const maxd = Math.max(...queries.map((q, i) => Math.max(...js.rank[i].scores.map((s, k) => Math.abs(s - ref.rank[i].scores[k])))));
  say(!rkBad.length, "the same first answer, the same answers shown and scores within 0.005 for " + queries.length + " questions", rkBad.slice(0, 2).join("; ") || "largest score difference " + maxd.toFixed(5));
  say(!errors.length, "no console errors", errors.slice(0, 3).join(" | "));
  console.log(fails ? fails + " parity checks failed" : "All parity checks passed");
  process.exit(fails ? 1 : 0);
})().catch(e => { console.error(e); server.close(); process.exit(1); });
