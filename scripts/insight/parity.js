// Insight (site 2.3): the page and the build must make the same numbers and take the same decisions. The page tokenizes
// in JavaScript, runs the model with ONNX Runtime Web and ranks with insRank (site/src/app.insight.js); the build
// (scripts/insight/build_index.py) tokenizes with the tokenizers library in Python, runs the model with the same ONNX
// Runtime Web files under Node (scripts/insight/embed.js) and holds the page's ranking rule a second time, in Python
// (class Ranker: what --eval measures on the gold set, so the gold table is the page's own behaviour only if the two agree).
// This runs both on the same texts (site questions, readers' wordings, real forum questions, and awkward ones: accents,
// punctuation, Chinese and Greek, emoji, special tokens, control characters, a word over 100 letters, text past 128 tokens)
// and requires: the same tokens; cosine >= 0.999 between the two vectors of every text; the same drug names added, the
// same drugs named and the same text with the names taken out; and, for real questions (forum questions, the 2.3 brief's
// own, and questions asked on a drug's page), the same best matches and the same related answers, in the same order, with
// both scores of each within 0.005. As an independent check of the model itself it also compares the page with the Python
// onnxruntime (PyEncoder), whose int8 kernels round a little differently on a PC: cosine >= 0.99 for every text.
// The model's file name, the weights and the tiers are read from the built data/insight.json by both sides.
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
const goldAll = readJ("data/verification/insight/gold-sample.json").questions.map(q => q.question);
const gold = goldAll.filter((_, i) => i % 8 === 0).slice(0, 15);
const odd = ["Café crème, ñandú and Ångström: naïve façade", "WHAT'S UP?! (really) — 'quotes' & “curly” stuff... #1 @home 50% $5", "1,4-butanediol, 2C-B, 3-MMC and 4-FA (e.g. N2O)",
  "大麻は安全ですか", "Είναι ασφαλές το MDMA; ΣΊΓΜΑ ΤΕΛΟΣ", "is 🍄 safe? 😅👍🏽", "[CLS] what [SEP] is [MASK] really[UNK]", "tab\there\nnew line\u0000nul​zero width nbsp",
  "a" + "bcdefghij".repeat(12) + " and a short word", Array.from({ length: 90 }, (_, i) => "word" + i + " ok").join(" "), "İstanbul ǅemal ﬁne Straße", "Mixing molly, xanax and booze?",
  "KETAMINE vs. ketamine’s cousin (K), weed/WEED and Xanax®", "are opioids, benzos and sleeping pills downers?", "ſpeed, ice and pills: everyday words"];
const texts = site.concat(wordings, gold, odd);
// the questions: [question, the drug page it is asked on or null]
const queries = goldAll.filter((_, i) => i % 5 === 2).slice(0, 60).map(q => [q, null]).concat([
  "does ecstasy damage your brain permanently", "can you fail a drug test from secondhand weed smoke", "how long does ketamine stay in your blood", "how can you die from alcohol",
  "give me the full evidence about how can i die from ketamine", "can i mix molly and alcohol", "how much mdma should i take", "what does an opioid overdose look like",
  "is it dangerous to mix molly and alcohol", "does weed make you lazy", "can lsd stay in your spine", "what is the capital of mongolia", "how addictive is meth", "is nitrous bad for you",
  "is fentanyl stronger than heroin", "do shrooms and acid feel the same", "my friend took ketamine and is not breathing what do i do", "does alcohol kill brain cells tl;dr",
  "are psychedelics addictive", "is coke or meth worse for your heart, with sources", "what happens if you take xanax with opioids"].map(q => [q, null]),
  [["does it kill brain cells", "cannabis"], ["is it addictive", "cannabis"], ["how long does it stay in your blood", "ketamine"], ["is it addictive", "kratom"], ["can it damage my bladder", "ketamine"],
   ["what does mdma do to serotonin", "cannabis"], ["how long does it last", "lsd"], ["is it safe with alcohol", "mdma"]]);
// the build's side, in Python: the same reading of every text, and the page's ranking rule from the same index
const py = `
import sys, json, importlib.util, numpy as np
spec = importlib.util.spec_from_file_location("bi", sys.argv[1]); bi = importlib.util.module_from_spec(spec); spec.loader.exec_module(bi)
req = json.load(sys.stdin); tok = bi.tokenizer(); enc = bi.encoder()
D = json.load(open(sys.argv[2], encoding="utf-8")); R = bi.Ranker(D)
texts = req["texts"]; ids = [tok.encode(t).ids for t in texts]; allt = texts + req["raw"]
out = {"model": bi.MODEL, "ids": ids, "vecs": bi.embed_ids(ids).tolist(), "pyvecs": [enc([t])[0].tolist() for t in texts],
       "expand": [R.expand(t) for t in allt], "mask": [R.mask(t) for t in allt], "named": [R.named(t) for t in allt]}
read = [R.texts(q, d) for q, d in req["queries"]]
uniq = list(dict.fromkeys(t for full, masked, groups in read for t in (full, masked)))
vec = dict(zip(uniq, bi.embed_all(uniq, quiet=True)))
rank = []
for (q, d), (full, masked, groups) in zip(req["queries"], read):
    r = R.rank_vectors(q, vec[full], vec[masked], groups)
    rank.append({"full": full, "masked": masked, "groups": groups, "best": r["best"], "related": r["related"]})
out["rank"] = rank
print(json.dumps(out))
`;
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
    const out = { ids: [], vecs: [], expand: [], mask: [], named: [], rank: [], tiers: pkInsight.tiers(), weights: pkInsight.weights() };
    for (const t of texts) { out.ids.push(pkInsight.encode(t)); out.vecs.push(await pkInsight.embed(t)); }
    for (const t of texts.concat(queries.map(q => q[0]))) { out.expand.push(pkInsight.expand(t)); out.mask.push(pkInsight.mask(t)); out.named.push(pkInsight.named(t)); }
    for (const [q, drug] of queries) out.rank.push(await pkInsight.rank(q, drug ? { drug } : {}));
    return out;
  }, { texts, queries });
  await browser.close(); server.close();
  // the build ranks what the page ranks: the question without its depth words (the page says which words those were)
  const asked = queries.map(([q, d], i) => [js.rank[i].core, d]);
  const r = spawnSync("python3", ["-I", "-c", py, path.join(REPO, "scripts/insight/build_index.py"), path.join(ROOT, "data/insight.json")], { input: JSON.stringify({ texts, raw: queries.map(q => q[0]), queries: asked }), maxBuffer: 1 << 28, encoding: "utf8" });
  if (r.status !== 0) { console.error(r.stderr); process.exit(2); }
  const ref = JSON.parse(r.stdout), D = JSON.parse(fs.readFileSync(path.join(ROOT, "data", "insight.json"), "utf8"));
  let fails = 0; const say = (pass, name, detail) => { if (!pass) fails++; console.log((pass ? "PASS " : "FAIL ") + name + (detail ? "  (" + detail + ")" : "")); };
  say(ref.model === D.model && JSON.stringify(js.tiers) === JSON.stringify(D.tiers) && JSON.stringify(js.weights) === JSON.stringify(D.weights), "the page and the build read the same model, weights and tiers (data/insight.json)", D.model + "; tiers " + JSON.stringify(D.tiers) + "; weights " + JSON.stringify(D.weights));
  const tokBad = texts.map((t, i) => JSON.stringify(js.ids[i]) === JSON.stringify(ref.ids[i]) ? null : JSON.stringify(t.slice(0, 40)) + ": page " + js.ids[i].slice(0, 12) + " / build " + ref.ids[i].slice(0, 12)).filter(Boolean);
  say(!tokBad.length, "the same tokens for all " + texts.length + " texts", tokBad.slice(0, 3).join("; ") || (Math.max(...ref.ids.map(x => x.length)) + " tokens at most"));
  const cosOf = (A, B) => texts.map((_, i) => { const a = A[i], b = B[i]; let d = 0, na = 0, nb = 0; for (let j = 0; j < a.length; j++) { d += a[j] * b[j]; na += a[j] * a[j]; nb += b[j] * b[j]; } return d / Math.sqrt(na * nb); });
  const cos = cosOf(js.vecs, ref.vecs), worst = cos.indexOf(Math.min(...cos)), same = texts.filter((_, i) => js.vecs[i].every((x, j) => Math.fround(x) === Math.fround(ref.vecs[i][j]))).length;
  say(cos.every(c => c >= 0.999), "cosine >= 0.999 between the page's and the build's vectors for every text", "lowest " + cos[worst].toFixed(6) + " for " + JSON.stringify(texts[worst].slice(0, 50)) + "; " + same + " of " + texts.length + " bit-identical");
  const pc = cosOf(js.vecs, ref.pyvecs), pw = pc.indexOf(Math.min(...pc)), ps = pc.slice().sort((a, b) => a - b);
  say(pc.every(c => c >= 0.99), "independent check, the Python onnxruntime: cosine >= 0.99 against the page for every text", "median " + ps[ps.length >> 1].toFixed(6) + ", " + pc.filter(c => c >= 0.999).length + " of " + texts.length + " at 0.999 or more, lowest " + pc[pw].toFixed(6) + " for " + JSON.stringify(texts[pw].slice(0, 40)));
  const all = texts.concat(queries.map(q => q[0]));
  const differ = (a, b) => a.map((x, i) => JSON.stringify(x) === JSON.stringify(b[i]) ? null : JSON.stringify(all[i].slice(0, 40)) + ": page " + JSON.stringify(x) + " / build " + JSON.stringify(b[i])).filter(Boolean);
  const exBad = differ(js.expand, ref.expand);
  say(!exBad.length, "the same drug names added to " + all.length + " texts", exBad.slice(0, 3).join("; ") || js.expand.filter((x, i) => x !== all[i]).length + " of them get names");
  const nmBad = differ(js.named, ref.named), mkBad = differ(js.mask, ref.mask);
  say(!nmBad.length && !mkBad.length, "the same drugs named in them, and the same text with the names taken out", nmBad.concat(mkBad).slice(0, 3).join("; ") || js.named.filter(g => g.length).length + " name a drug, " + js.named.filter(g => g.length > 1).length + " more than one, " + js.named.filter(g => g.some(x => x.length > 1)).length + " a family of drugs");
  // the ranking: the same best matches and related answers, in order, with both scores within 0.005. (What the page adds on top
  // of the rule: a question we do not answer gets nothing, and an emergency gets no related answers: by design, counted apart.)
  let maxd = 0, nBest = 0, nRel = 0, nNone = 0, blocked = 0, urgent = 0, whole = 0; const rkBad = [];
  queries.forEach(([q, drug], i) => { const a = js.rank[i], b = ref.rank[i], tag = JSON.stringify(q.slice(0, 50)) + (drug ? " on " + drug : "");
    if (a.note === "blocked") { blocked++; return; }
    if (!a.best.length && !a.related.length && a.routes.some(x => x.kind === "page") && a.core.split(/\s+/).length < 3) { whole++; return; }
    const pairs = [["best", a.best, b.best]]; if (a.emergency) urgent++; else pairs.push(["related", a.related, b.related]);
    for (const [k, x, y] of pairs) {
      if (x.map(r => r.id).join() !== y.map(r => r.id).join()) { rkBad.push(tag + " " + k + ": page [" + x.map(r => r.id + " " + r.plain + "/" + r.topic) + "] build [" + y.map(r => r.id + " " + r.plain + "/" + r.topic) + "]"); continue; }
      x.forEach((r, j) => { const d = Math.max(Math.abs(r.plain - y[j].plain), Math.abs(r.topic - y[j].topic)); maxd = Math.max(maxd, d); if (d > 0.005 || r.off !== y[j].off) rkBad.push(tag + " " + k + " " + r.id + ": page " + r.plain + "/" + r.topic + (r.off ? " off" : "") + " build " + y[j].plain + "/" + y[j].topic + (y[j].off ? " off" : "")); });
    }
    nBest += a.best.length; if (!a.emergency) nRel += a.related.length; if (!a.best.length) nNone++; });
  const compared = queries.length - blocked - whole;
  say(!rkBad.length && compared >= queries.length - 6 && nBest >= 15 && nRel >= 40 && nNone >= 15, "the same best matches and related answers, in the same order, both scores within 0.005, for " + compared + " questions (" + queries.filter(q => q[1]).length + " asked on a drug's page)",
    rkBad.slice(0, 3).join("; ") || nBest + " best matches, " + nRel + " related answers, " + nNone + " questions with no best match; largest score difference " + maxd.toFixed(5) + "; by design not compared: " + blocked + " not answered, " + whole + " a drug's name alone; related left out for " + urgent + " emergencies");
  say(!errors.length, "no console errors", errors.slice(0, 3).join(" | "));
  console.log(fails ? fails + " parity checks failed" : "All parity checks passed");
  process.exit(fails ? 1 : 0);
})().catch(e => { console.error(e); server.close(); process.exit(1); });
