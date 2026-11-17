// Insight (site 2.3): the page and the build must make the same numbers and take the same decisions. The page tokenizes
// in JavaScript, runs the model with ONNX Runtime Web and ranks with insRank (site/src/app.insight.js); the build
// (scripts/insight/build_index.py) tokenizes with the tokenizers library in Python, runs the model with the same ONNX
// Runtime Web files under Node (scripts/insight/embed.js) and holds the page's ranking rule a second time, in Python
// (class Ranker: what --eval measures on the gold set, so the gold table is the page's own behaviour only if the two agree).
// This runs both on the same texts (site questions, readers' wordings, real forum questions, and awkward ones: accents,
// punctuation, Chinese and Greek, emoji, special tokens, control characters, a word over 100 letters, text past 128 tokens)
// and requires: the same tokens; cosine >= 0.999 between the two vectors of every text; the same drug names added, the
// same drugs named and the same text with the names taken out; and, for real questions (forum questions, the 2.3 brief's
// own, and questions asked on a drug's page), the same first candidate with the same six numbers and the same judge's
// number (to 1e-4), the same best match and the same related answers, in the same order, with both scores of each within
// 0.005. As an independent check of the model itself it also compares the page with the Python onnxruntime (PyEncoder),
// whose int8 kernels round a little differently on a PC: cosine >= 0.99 for every text.
// The model's file name, the weights, the tiers and the judge are read from the built data/insight.json by both sides.
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
  "are psychedelics addictive", "is coke or meth worse for your heart, with sources", "what happens if you take xanax with opioids",
  // 2.5: questions on our list in other words, questions that are not about drugs, and drug questions the site's names do not give away
  "can alcohol kill you", "does weed cause cancer", "is ketamine addictive", "what is a k hole", "can you overdose on acid", "why does weed make me paranoid", "is sugar as addictive as coke", "how long is weed in your system",
  "can i die from mosquito bites", "how do i cook mushrooms in butter", "is diet coke bad for your teeth", "can you die from a bee sting", "how do i get high scores in tetris", "do vaccines cause autism", "is stomach acid dangerous",
  "what is 6-apb like", "is modafinil safe", "how long does the high last", "is it ok to take ibuprofen every day", "why do people take drugs", "what is the best tablet for drawing"].map(q => [q, null]),
  [["does it kill brain cells", "cannabis"], ["is it addictive", "cannabis"], ["how long does it stay in your blood", "ketamine"], ["is it addictive", "kratom"], ["can it damage my bladder", "ketamine"],
   ["what does mdma do to serotonin", "cannabis"], ["how long does it last", "lsd"], ["is it safe with alcohol", "mdma"]]);
// 2.9: questions as a reader who is still typing leaves them: every third forum question of the gold set cut after each of its
// words and in the middle of each word of five letters or more, and the ones the rule was written for
const cuts = [...new Set(goldAll.filter((_, i) => i % 3 === 0).flatMap(q => { const w = q.replace(/[?!.]+$/, "").split(" "), out = [];
  for (let i = 1; i <= w.length; i++) { out.push(w.slice(0, i).join(" ")); if (i < w.length && w[i].length >= 5) out.push(w.slice(0, i).join(" ") + " " + w[i].slice(0, Math.ceil(w[i].length / 2))); }
  return out; }).concat(["can i die from ", "can i die from", "is it addictive", "can you overdose", "how long does it last", "what is tolerance", "how long does withdrawal last", "why do people get addicted",
  "what is it cut with", "what are pills cut with", "what is heroin cut with", "is cocaine", "what is ketamine", "what is ketamine for", "weed and alcohol", "weed and", "how does mdma", "can i die from coc", "is weed lega",
  "is cocaine addi", "can a gay man go to the court", "who are you", "what time is it", "how much ecstasy is too much", "what does it feel like", "what’s it like", "DOES IT SHOW UP ON A DRUG TEST", "is tusi dangerous",
  "what is photosynthesis", "how do i stop snoring", "don't you know what's in it", "Why does meth not work like it used to?", "what might someone have been spiked with", "xanax vs", "'quoted' words and", "",
  // 2.9.2: a subject and nothing said of it; a helper verb and no main verb; the endings and short forms the fresh questions showed
  "do gay people", "can a gay man", "why do women", "how many people", "are gay people", "are people gay", "is my mom", "does smoking weed", "how long does the high", "can dogs", "does the government",
  "do antidepressants", "what drugs can", "smoking weed can", "how long does withdrawal", "can you digest", "how do i weed my garden", "can i speed up the comedown", "how to do drugs", "what happens when you do drugs",
  "people do drugs", "is weed for kids", "how do i get a girlfriend", "does he like me", "can u die from", "do ppl", "wat is", "is it safe rn", "eating before drinking lower bac", "what is mytragina javanica",
  "what do you use it for", "what does cbd actually work for", "has anyone tried this before", "how long does gabapentin take to kick in", "what is cannabis (thc)", "do old people", "should parents", "will the police",
  "does my doctor", "gay people", "can pregnant women", "is she pregnant", "is diet coke", "why are people who use drugs looked down on", "does anyone have any idea what i was spiked with"]))];
// 2.9.1: names with a letter wrong, and words that must be left as they are
const spells = ["what is mytragina javanica", "mitragina  JANANICA effects", "can i die from cocane", "is ketamin addictive", "herion withdrawal", "is adderal safe", "does marijauna cause cancer", "how long does xanex last", "is heroine addictive", "can you overdose on tramadole",
  "what is extasy", "is canabis legal", "mushroms and alcohol", "is morphing a thing", "what is escaline", "how do i treat a sunburn", "is it safe to eat moldy bread", "why do cats purr", "what is photosynthesis",
  "is tusi dangerous", "does caffiene keep you awake", "alchohol and benzodiazapines", "is codiene an opiod", "how does methamphetamin work", "what is the capital of mongolia", "is gabapentine addictive",
  "is modafanil safe", "are steriods bad", "psycadelics and anxiety", "can i mix oxycodon and alcohol", "how long does 4-mmc last", "is nicotene addictive", "what about ayahuaska", "is cocaines effect long",
  "asteroids and comets", "what is a ketimine", "do peppers help", "is tobaco worse than weed", "valum for sleep", "is vyvance like adderall", "fentanil test strips", "does mdna hurt the brain", "COCANE and Ketamin?",
  "cocane-like drugs", "the heroine's journey", "xanaxes", "weeds in my garden", "is MDNA an album"];
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
    rank.append({"full": full, "masked": masked, "groups": groups, "best": r["best"], "related": r["related"], "first": r["first"], "want": R.want(q, vec[full], vec[masked], groups), "scope": R.in_scope(q), "unf": R.unfinished(q, bool(d) and not R.named(q))})
out["rank"] = rank
# 2.9: is the question finished, and which of its words are not known: the two rules on words alone, on every cut
out["cuts"] = [[R.unfinished(c, False), R.unfinished(c, True), bi.unknown_words(c, R.unfin["vocab"] or set(), R.unfin["known"])] for c in req["cuts"]]
# 2.9.1: a drug's name with a letter wrong, read as the name: on the cuts and on misspellings and words that must be left alone
out["spell"] = [list(R.correct(c)) for c in req["cuts"] + req["spells"]]
print(json.dumps(out))
`;
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split("?")[0]); if (p.endsWith("/")) p += "index.html";
  if (p === "/api/ask") { res.writeHead(200, { "Content-Type": "application/json" }); res.end('{"ok":false}'); return; }   // as the site's worker answers before its store is set up
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
  const js = await p.evaluate(async ({ texts, queries, cuts, spells }) => {
    const out = { ids: [], vecs: [], expand: [], mask: [], named: [], rank: [], tiers: pkInsight.tiers(), weights: pkInsight.weights(), judge: pkInsight.judge() };
    for (const t of texts) { out.ids.push(pkInsight.encode(t)); out.vecs.push(await pkInsight.embed(t)); }
    for (const t of texts.concat(queries.map(q => q[0]))) { out.expand.push(pkInsight.expand(t)); out.mask.push(pkInsight.mask(t)); out.named.push(pkInsight.named(t)); }
    for (const [q, drug] of queries) { const r = await pkInsight.rank(q, drug ? { drug } : {}); r.scope = pkInsight.scope(r.core); out.rank.push(r); }
    out.listed = pkInsight.listed();
    out.cuts = cuts.map(c => [pkInsight.unfinished(c, false), pkInsight.unfinished(c, true), pkInsight.unknown(c)]);
    out.spell = cuts.concat(spells).map(c => { const r = pkInsight.spell(c); return [r.text, r.read]; });
    return out;
  }, { texts, queries, cuts, spells });
  await browser.close(); server.close();
  // the build ranks what the page ranks: the question without its depth words (the page says which words those were)
  const asked = queries.map(([q, d], i) => [js.rank[i].core, d]);
  const r = spawnSync("python3", ["-I", "-c", py, path.join(REPO, "scripts/insight/build_index.py"), path.join(ROOT, "data/insight.json")], { input: JSON.stringify({ texts, raw: queries.map(q => q[0]), queries: asked, cuts, spells }), maxBuffer: 1 << 28, encoding: "utf8" });
  if (r.status !== 0) { console.error(r.stderr); process.exit(2); }
  const ref = JSON.parse(r.stdout), D = JSON.parse(fs.readFileSync(path.join(ROOT, "data", "insight.json"), "utf8"));
  let fails = 0; const say = (pass, name, detail) => { if (!pass) fails++; console.log((pass ? "PASS " : "FAIL ") + name + (detail ? "  (" + detail + ")" : "")); };
  say(ref.model === D.model && JSON.stringify(js.tiers) === JSON.stringify(D.tiers) && JSON.stringify(js.weights) === JSON.stringify(D.weights) && JSON.stringify(js.judge) === JSON.stringify(D.judge), "the page and the build read the same model, weights, tiers and judge (data/insight.json)",
    D.model + "; tiers " + JSON.stringify(D.tiers) + "; weights " + JSON.stringify(D.weights) + "; a best match from " + D.judge.best);
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
  // the ranking: the same first candidate with the same six numbers and the same judge's number (to 1e-4), the same best match and
  // related answers, in order, with both scores within 0.005. (What the page adds on top of the rule: a question we do not answer
  // gets nothing, and an emergency gets no related answers: by design, counted apart.)
  let maxd = 0, maxp = 0, maxf = 0, nBest = 0, nRel = 0, nNone = 0, blocked = 0, urgent = 0, whole = 0, demoted = 0; const rkBad = [], pj = [];
  queries.forEach(([q, drug], i) => { const a = js.rank[i], b = ref.rank[i], tag = JSON.stringify(q.slice(0, 50)) + (drug ? " on " + drug : "");
    if (a.note === "blocked") { blocked++; return; }
    if (!a.judge) { whole++; return; }
    const dp = Math.abs(a.judge.p - b.first.p), df = Math.max(...a.judge.f.map((x, j) => Math.abs(x - b.first.f[j]))); maxp = Math.max(maxp, dp); maxf = Math.max(maxf, df); pj.push(a.judge.p);
    if (a.judge.id !== b.first.id || dp > 1e-4 || df > 1e-4) rkBad.push(tag + " the judge: page " + a.judge.id + " " + a.judge.p.toFixed(5) + " [" + a.judge.f.map(x => x.toFixed(4)) + "] build " + b.first.id + " " + b.first.p.toFixed(5) + " [" + b.first.f.map(x => x.toFixed(4)) + "]");
    // (2.9) a question that is not finished and names no drug has no best match on the page: the answers found are shown as ways to go on
    const bb = a.demoted ? [] : b.best, br = a.demoted ? b.best.concat(b.related).slice(0, 3) : b.related; if (a.demoted) demoted++;
    const pairs = [["best", a.best, bb]]; if (a.emergency) urgent++; else pairs.push(["related", a.related, br]);
    for (const [k, x, y] of pairs) {
      if (x.map(r => r.id).join() !== y.map(r => r.id).join()) { rkBad.push(tag + " " + k + ": page [" + x.map(r => r.id + " " + r.plain + "/" + r.topic) + "] build [" + y.map(r => r.id + " " + r.plain + "/" + r.topic) + "]"); continue; }
      x.forEach((r, j) => { const d = Math.max(Math.abs(r.plain - y[j].plain), Math.abs(r.topic - y[j].topic)); maxd = Math.max(maxd, d); if (d > 0.005 || r.off !== y[j].off) rkBad.push(tag + " " + k + " " + r.id + ": page " + r.plain + "/" + r.topic + (r.off ? " off" : "") + " build " + y[j].plain + "/" + y[j].topic + (y[j].off ? " off" : "")); });
    }
    if (a.best.length > 1) rkBad.push(tag + ": more than one best match");
    nBest += a.best.length; if (!a.emergency) nRel += a.related.length; if (!a.best.length) nNone++; });
  const compared = queries.length - blocked - whole;
  say(!rkBad.length && compared >= queries.length - 6 && nBest >= 5 && nRel >= 40 && nNone >= 15 && pj.some(x => x >= D.judge.best) && pj.some(x => x < D.judge.best),
    "the same first candidate, six numbers and judge's number (to 1e-4), the same best match and related answers in the same order, both scores within 0.005, for " + compared + " questions (" + queries.filter(q => q[1]).length + " asked on a drug's page)",
    rkBad.slice(0, 3).join("; ") || nBest + " best matches, " + nRel + " related answers, " + nNone + " questions with no best match; the judge's number from " + Math.min(...pj).toFixed(3) + " to " + Math.max(...pj).toFixed(3) + ", largest difference " + maxp.toExponential(1) +
      " (six numbers " + maxf.toExponential(1) + ", scores " + maxd.toFixed(5) + "); by design not compared: " + blocked + " not answered, " + whole + " a drug's name alone; related left out for " + urgent + " emergencies; " + demoted + " not finished and naming no drug: their best match shown as a way to go on");
  // 2.5: the second look and the scope rule. Where the page has no best match and no route that answers, it looks at the list:
  // the same listed question as the build, with the same judge's number (to 1e-4), or none on both sides; and by its words the
  // question is, or is not, a question about drugs on both sides; the line the page then says follows from the two.
  const wBad = [], seen = { want: 0, other: 0, none: 0, unfinished: 0 }; let maxw = 0;
  queries.forEach(([q, drug], i) => { const a = js.rank[i], b = ref.rank[i], tag = JSON.stringify(q.slice(0, 50)) + (drug ? " on " + drug : "");
    if (a.scope !== b.scope) wBad.push(tag + " about drugs: page " + a.scope + " build " + b.scope);
    if (!["want", "other", "none", "unfinished"].includes(a.note)) return;
    // (2.9) not finished yet, by the same rule on both sides: that is what the page says, before anything else
    if ((a.note === "unfinished") !== !!b.unf || a.unf !== b.unf) { wBad.push(tag + " finished: page " + JSON.stringify(a.unf) + " (says " + a.note + ") build " + JSON.stringify(b.unf)); return; }
    if (a.note === "unfinished") { seen.unfinished++; return; }
    const pw = a.want ? a.want.id : null, bw = b.want ? b.want.id : null;
    if (pw !== bw) { wBad.push(tag + " on our list: page " + pw + " build " + bw); return; }
    if (pw) { const d = Math.abs(a.want.p - b.want.p); maxw = Math.max(maxw, d); if (d > 1e-4) wBad.push(tag + " the judge's number for the listed question: page " + a.want.p + " build " + b.want.p); }
    const should = pw ? "want" : drug || b.scope ? "none" : "other";
    if (a.note !== should) wBad.push(tag + " says " + a.note + ", should say " + should); seen[a.note]++; });
  say(JSON.stringify(js.listed) === JSON.stringify((D.wanted || { ids: [] }).ids) && !wBad.length && seen.want >= 6 && seen.other >= 5 && seen.none >= 8,
    "the same listed question (or none) with the same judge's number, and the same reading of what is a question about drugs, for all " + queries.length + " questions; the page's line follows from them",
    wBad.slice(0, 3).join("; ") || js.listed.length + " questions on the list; of the questions with no answer, " + seen.unfinished + " are not finished, " + seen.want + " are on the list, " + seen.none + " are drug questions not checked yet, " + seen.other + " are not about drugs; largest difference of the judge's number " + maxw.toExponential(1));
  // 2.9: the two rules on words alone, the same on both sides for every cut
  const cBad = cuts.map((c, i) => JSON.stringify(js.cuts[i]) === JSON.stringify(ref.cuts[i]) ? null : JSON.stringify(c) + ": page " + JSON.stringify(js.cuts[i]) + " build " + JSON.stringify(ref.cuts[i])).filter(Boolean);
  const nUnf = js.cuts.filter(x => x[0]).length, kinds = {}; js.cuts.forEach(x => { if (x[0]) kinds[x[0]] = (kinds[x[0]] || 0) + 1; });
  say(!cBad.length && cuts.length >= 800 && ["ends", "bare", "which", "typing", "open", "verb"].every(k => kinds[k] >= 5),
    "the same reading of whether a question is finished (off and on a drug's page) and of which words are not known, for " + cuts.length + " questions cut as a reader who is still typing leaves them",
    cBad.slice(0, 3).join("; ") || nUnf + " not finished off a drug's page (" + Object.keys(kinds).sort().map(k => kinds[k] + " " + k).join(", ") + "); " + js.cuts.filter(x => x[2].length).length + " hold a word that is not known");
  // 2.9.1: the same word read as the same name, and the same words left alone, on both sides
  const sAll = cuts.concat(spells), sBad = sAll.map((c, i) => JSON.stringify(js.spell[i]) === JSON.stringify(ref.spell[i]) ? null : JSON.stringify(c) + ": page " + JSON.stringify(js.spell[i]) + " build " + JSON.stringify(ref.spell[i])).filter(Boolean);
  const nRead = js.spell.slice(cuts.length).filter(x => x[1].length).length, inCuts = js.spell.slice(0, cuts.length).filter(x => x[1].length).length;
  say(!sBad.length && nRead >= 25 && nRead <= spells.length - 12, "the same misspelt names read as the same names, and the same words left as they are, for " + sAll.length + " questions",
    sBad.slice(0, 3).join("; ") || nRead + " of " + spells.length + " test questions hold a word read as a name; " + inCuts + " of the " + cuts.length + " cuts of real questions do");
  say(!errors.length, "no console errors", errors.slice(0, 3).join(" | "));
  console.log(fails ? fails + " parity checks failed" : "All parity checks passed");
  process.exit(fails ? 1 : 0);
})().catch(e => { console.error(e); server.close(); process.exit(1); });
