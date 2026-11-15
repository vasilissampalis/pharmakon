// Insight (site 2.3, 15 November 2026), checked in a real browser at 390 x 844 and 1280 x 800, with the site served as
// Cloudflare Pages serves it (the file types, revalidated caching, and the security policy of site/public/_headers).
// What must hold (the 2.3 brief, scripts/insight/BRIEF-2.3-insight.md):
// - every published file is under 25 MiB; the start page fetches none of Insight's files; the cursor in the search box fetches
//   them, from the site itself only, the model being the one the index names; a second visit downloads nothing again; on a
//   connection that saves data nothing is fetched until the reader taps the line that offers it;
// - honest tiers: a question the site answers has its answer as "Best match", the short answer in full in the list; a question
//   it does not answer ("how can you die from alcohol") says "We haven't checked exactly this yet" with "Ask us to check it",
//   and a near answer shows under "Related" at most; the thresholds and weights the page uses are those of data/insight.json;
// - routes, each with its test: two drugs (the mixing row first, opening the mixing tool with both chosen), a dose (the
//   Doses row, no amount), an emergency (the help row and the emergency number line, which shows nowhere else), testing a
//   sample, "what is X", and no route and no answer for getting drugs, hiding use or beating a drug test;
// - Enter opens the sheet for the question as asked, headed with the person's own words, depth words understood ("full
//   evidence": How do we know? open; "tl;dr": the short answer and its But), with no guess step anywhere;
// - on a drug's page the box reads "Ask about <drug>" and a question that names no drug is about that drug;
// - an answer linked from outside its own page opens over the page: Myth or fact's "Read the answer" (Back, Escape and the
//   browser's Back return to the same card, scrolled as it was), the questions to try, a shared answer's other questions;
// - next questions ("People also ask", "Read next") are about the same drug, without the answers opened in this visit;
// - Back from the sheet puts the search back as it was; nothing typed leaves the page or is stored; no "AI" words; no console
//   errors; no sideways scroll; nothing Insight adds moves. Prints the time each search takes (median and slowest).
// Usage: node scripts/ux/insight_check.js [--shots DIR] [--port N]   (build first: node site/build.js && python3 -I site/build_public.py)
const http = require("http"), fs = require("fs"), path = require("path"), os = require("os");
const { chromium } = require("playwright");
const REPO = path.resolve(__dirname, "..", ".."), ROOT = path.join(REPO, "site", "public");
const arg = k => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : null; };
const SHOTS = arg("--shots"), PORT = +(arg("--port") || 0);
const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".mjs": "text/javascript", ".wasm": "application/wasm", ".json": "application/json", ".css": "text/css",
  ".webp": "image/webp", ".png": "image/png", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".txt": "text/plain; charset=utf-8", ".xml": "application/xml" };
// questions the site answers, as people type them, and the answer each should get as its best match
const REAL = [["does ecstasy damage your brain permanently", "cl_mdma_neurotoxicity_contested"], ["can you fail a drug test from secondhand weed smoke", "cl_can_secondhand_test"],
  ["how long does ketamine stay in your blood", "cl_ket_halflife_norketamine"]];
const ALCOHOL = "how can you die from alcohol", KETAMINE = "give me the full evidence about how can i die from ketamine", NONE = "what is the capital of mongolia";
const MIX = "can i mix molly and alcohol", DOSE = "how much mdma should i take", HELP = "my friend took ketamine and is not breathing what do i do", TEST = "how do i test my mdma", BUY = "where can i buy mdma online";
// Each route has its test: questions that must take it, and questions close to it that must not ("" = no route). A third
// item is the drug page the question is asked on.
const ROUTES = [
  ["can i mix molly and alcohol", "mix"], ["weed and alcohol together", "mix"], ["is it safe to take xanax with alcohol", "mix"], ["ketamine after cocaine is it ok", "mix"], ["lsd + mdma", "mix"],
  ["is fentanyl stronger than heroin", ""], ["lsd or mushrooms what's the difference", ""], ["does mdma therapy help people with alcohol problems", ""], ["is fentanyl found in cocaine", ""], ["should i drink water on mdma", ""],
  ["how much mdma should i take", "dose"], ["what is a safe dose of ketamine", "dose"], ["lsd dosage for first time", "dose"], ["how many mg of xanax is too much", "dose"], ["is 200mg of mdma too much", "dose"], ["how many pills can i take", "dose"], ["lethal dose of caffeine", "dose"],
  ["what does one dose of meth do to the body", ""], ["after high doses of dxm how long is balance affected", ""], ["how many people who use weed get addicted", ""], ["how much does cannabis affect driving", ""], ["how many deaths does alcohol cause", ""], ["why can the usual amount be dangerous after a break", ""],
  ["my friend is not breathing", "help"], ["he won't wake up after taking ghb", "help"], ["my friend passed out", "help"], ["i think i'm overdosing", "help"], ["she is having a seizure", "help"], ["i am too high right now", "help"], ["greening out help", "help"], ["bad trip help please", "help"], ["im freaking out on acid", "help"],
  ["my friend took too much ketamine what do i do", "help"], ["i feel suicidal after a coke binge", "help"],
  ["would i know if someone was overdosing on opioids", ""], ["what does an opioid overdose look like", ""], ["my teenager smokes weed what should i do", ""], ["is teenage cannabis use linked to suicidal thoughts", ""], ["can medicine stop me having a seizure when i stop drinking", ""],
  ["how do i test my mdma", "test"], ["is my coke cut with something", "test"], ["where can i get fentanyl test strips", "test"], ["which test kit for ketamine", "test"], ["mdma test kit", "test"], ["how to test for fentanyl", "test"], ["is this pill real mdma", "test"],
  ["do fentanyl test strips work", ""], ["can you fail a drug test from secondhand weed smoke", ""], ["can test kits do harm by making people feel falsely safe", ""], ["i felt sober after coke is that real", ""],
  ["what is ketamine", "page"], ["what's ghb", "page"], ["tell me about kratom", "page"], ["what is speed", "page"], ["what is ketamine used for in hospitals", ""],
  ["where can i buy mdma online", "blocked"], ["how to get weed without my parents knowing", "blocked"], ["how do i pass a drug test for weed", "blocked"], ["how to make dmt at home", "blocked"], ["how is meth made", "blocked"], ["how to hide being high from my mom", "blocked"],
  ["best darknet vendor for lsd", "blocked"], ["how to get thc out of my system fast", "blocked"], ["can you grow shrooms at home", "blocked"], ["fake pee for a drug test", "blocked"],
  ["where can i get naloxone", ""], ["where can i get help for my cocaine use", ""], ["does cocaine hide how drunk someone is", ""], ["why do some medicines make mdma stronger", ""], ["does alcohol make ghb more sedating", ""], ["what is mdma made of", ""],
  ["does it kill brain cells", "", "cannabis"], ["how much should i take", "dose", "cannabis"], ["how do i test it", "test", "mdma"], ["im way too high what do i do", "help", "cannabis"]
];
// depth words: [question, depth, what is left to match]
const DEPTH = [[KETAMINE, "full", "how can i die from ketamine"], ["all the evidence on mdma and memory", "full", "mdma and memory"], ["mdma neurotoxicity sources", "full", "mdma neurotoxicity"], ["does lsd damage dna in detail", "full", "does lsd damage dna"],
  ["explain how ketamine works", "full", "how ketamine works"], ["is weed addictive tl;dr", "short", "is weed addictive"], ["eli5 how does ketamine work", "short", "how does ketamine work"], ["in a sentence does alcohol kill brain cells", "short", "does alcohol kill brain cells"],
  ["short answer: is weed addictive", "short", "is weed addictive"], ["why was my trip so short", "", "why was my trip so short"], ["is it simple to quit weed", "", "is it simple to quit weed"]];
const AI_WORDS = /\b(AI|A\.I\.|artificial intelligence|machine learning|neural|algorithm|language model|chatbot|GPT)\b/i;
const AMOUNT = /\d\s?(?:mg|µg|ug|mcg|ml|milligrams?|micrograms?|grams?)\b/i;
const results = [], errors = [], times = [];
const ok = (name, pass, detail) => { results.push(!!pass); console.log((pass ? "PASS " : "FAIL ") + name + (detail ? "  (" + String(detail).slice(0, 700) + ")" : "")); };
if (!fs.existsSync(path.join(ROOT, "index.html"))) { console.error("No site/public/index.html: build first."); process.exit(2); }
const csp = (fs.readFileSync(path.join(ROOT, "_headers"), "utf8").match(/Content-Security-Policy: (.*)/) || [])[1];
const INDEX = JSON.parse(fs.readFileSync(path.join(ROOT, "data", "insight.json"), "utf8")), MODEL = INDEX.model;
const CONFIG = JSON.parse(fs.readFileSync(path.join(REPO, "site", "insight", "model.json"), "utf8"));
// as Cloudflare Pages does: an ETag, and "revalidate before use", so a file already in the browser's cache comes back as 304
const served = [];
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split("?")[0]); if (p.endsWith("/")) p += "index.html";
  const f = path.join(ROOT, path.normalize(p)); if (!f.startsWith(ROOT)) { res.writeHead(403); res.end(); return; }
  fs.stat(f, (err, st) => { if (err || !st.isFile()) { res.writeHead(404); res.end("not found"); return; }
    const tag = '"' + st.size.toString(36) + "-" + Math.floor(st.mtimeMs).toString(36) + '"';
    const head = Object.assign({ "Content-Type": TYPES[path.extname(f)] || "application/octet-stream", "X-Content-Type-Options": "nosniff", ETag: tag, "Cache-Control": "public, max-age=0, must-revalidate" }, csp ? { "Content-Security-Policy": csp } : {});
    if (req.headers["if-none-match"] === tag) { served.push({ p, status: 304, bytes: 0 }); res.writeHead(304, head); res.end(); return; }
    fs.readFile(f, (e2, buf) => { if (e2) { res.writeHead(500); res.end(); return; } served.push({ p, status: 200, bytes: buf.length }); res.writeHead(200, head); res.end(buf); }); });
});
// every file the site publishes stays under Cloudflare Pages' limit of 25 MiB a file
{ const walk = d => fs.readdirSync(d, { withFileTypes: true }).flatMap(e => e.isDirectory() ? walk(path.join(d, e.name)) : [[path.join(d, e.name), fs.statSync(path.join(d, e.name)).size]]);
  const files = walk(ROOT).sort((a, b) => b[1] - a[1]);
  ok("every published file is under 25 MiB", files[0][1] < 25 * 1024 * 1024, files.slice(0, 2).map(([f, n]) => path.relative(ROOT, f) + " " + (n / 1048576).toFixed(1) + " MiB").join(", ")); }
// the model's name, the weights and the tiers are written in one place (site/insight/model.json) and reach the page through the index
ok("the index carries the model's name, the weights and the tiers of site/insight/model.json", MODEL === CONFIG.file && JSON.stringify(INDEX.tiers) === JSON.stringify(CONFIG.tiers) && JSON.stringify(INDEX.weights) === JSON.stringify(CONFIG.weights) && fs.existsSync(path.join(ROOT, "insight", MODEL)),
  MODEL + "; tiers " + JSON.stringify(INDEX.tiers));
// each answer's next questions travel in the page itself (no fetch): every answer but one alone on its drug has some, none offers itself
{ const page = fs.readFileSync(path.join(ROOT, "index.html"), "utf8"), m = page.match(/\nconst INS_NEXT = (\{.*?\});\n/), NX = m ? JSON.parse(m[1]) : null;
  const withNext = NX ? NX.next.filter(l => l.length).length : 0, self = NX ? NX.next.filter((l, i) => l.includes(i) || new Set(l).size !== l.length).length : 0;
  ok("the page carries each answer's next questions (never the answer itself, none twice)", !!NX && NX.ids.length === INDEX.ids.length && withNext >= NX.ids.length - 3 && !self && (m[1].length < 60000),
    NX ? withNext + " of " + NX.ids.length + " answers have next questions, " + NX.next.reduce((a, l) => a + l.length, 0) + " in all, " + Math.round(m[1].length / 1024) + " KB in the page" : "INS_NEXT missing from the page"); }
(async () => {
  await new Promise(r => server.listen(PORT, "127.0.0.1", r));
  const ORIGIN = "http://127.0.0.1:" + server.address().port, BASE = ORIGIN + "/#";
  if (SHOTS) fs.mkdirSync(SHOTS, { recursive: true });
  const browser = await chromium.launch({ args: ["--no-proxy-server"] });
  for (const w of [390, 1280]) {
    const H = w < 700 ? 844 : 800;
    const ctx = await browser.newContext({ viewport: { width: w, height: H }, deviceScaleFactor: 1, hasTouch: w < 700, isMobile: w < 700 }), p = await ctx.newPage();
    p.on("pageerror", e => errors.push(w + " page error: " + String(e).slice(0, 200)));
    p.on("console", m => { if (m.type() === "error") errors.push(w + " console error: " + m.text().slice(0, 200)); });
    const reqs = [], sent = []; p.on("request", r => { reqs.push(r.url()); sent.push(r.url() + " " + (r.postData() || "")); });
    const typed = [];   // every question typed, to make sure none leaves the page
    const shot = async name => { await p.waitForTimeout(200); const [sw, cw] = await p.evaluate(() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]); if (sw > cw) errors.push(w + " horizontal scroll at " + name);
      if (SHOTS) await p.screenshot({ path: path.join(SHOTS, w + "-insight-" + name + ".png") }); };
    const ins = u => /\/data\/insight\.json|\/insight\//.test(u);
    const whenReady = () => p.waitForFunction(() => window.pkInsight && pkInsight.state() === "ready", null, { timeout: 120000 }).then(() => true, () => false);
    // what Insight shows in the results for the question in the box
    const snap = () => p.evaluate(() => { const box = document.getElementById("search-results"), f = box.querySelector(".sr-fit"); if (!f) return { kids: [], routes: [], best: [], related: [], none: "", askBtn: "", sos: "", text: "", open: !box.hidden, value: document.getElementById("search").value };
      const cut = e => e.scrollHeight > e.clientHeight + 1 || getComputedStyle(e).textOverflow === "ellipsis" || getComputedStyle(e).webkitLineClamp !== "none";
      return { kids: [...f.children].filter(e => !e.hidden).map(e => e.matches("a.sr-route") ? "route:" + e.dataset.insRoute : e.matches(".sr-sos") ? "sos" : e.matches(".sr-fit-h") ? "h:" + e.textContent : e.matches("a.sr-best") ? "best" : e.matches("a.sr-fit-a") ? "related" : e.matches(".sr-fit-none") ? "none" : e.className),
        routes: [...f.querySelectorAll("a.sr-route")].map(a => ({ kind: a.dataset.insRoute, k: a.querySelector(".k").textContent, t: a.querySelector(".t").textContent, href: a.getAttribute("href") })),
        best: [...f.querySelectorAll("a.sr-best")].map(a => ({ id: a.dataset.insight, k: a.querySelector(".k").textContent, q: a.querySelector(".t").textContent, a: a.querySelector(".a").textContent, whole: a.querySelector(".a").textContent === SIMPLE.claims[a.dataset.insight].short && !cut(a.querySelector(".a")), bars: !!a.querySelector(".m .meter") })),
        related: [...f.querySelectorAll("a.sr-fit-a:not(.sr-best)")].map(a => ({ id: a.dataset.insight, k: a.querySelector(".k").textContent, q: a.querySelector(".t").textContent })),
        none: (f.querySelector(".sr-fit-none b") || {}).textContent || "", askBtn: (f.querySelector(".sr-fit-none button") || {}).textContent || "", sos: (f.querySelector(".sr-sos") || {}).textContent || "", text: f.innerText,
        note: (box.querySelector(":scope > .sr-note") || {}).textContent || "", first: box.firstElementChild && box.firstElementChild.className, live: document.getElementById("search-count").textContent,
        wordAsk: !!box.querySelector(":scope > .sr-ask"), wordBest: box.querySelectorAll(":scope > a.sr-ans.best").length + [...box.querySelectorAll(":scope > a .k")].filter(k => /^Best answer/.test(k.textContent)).length,
        open: !box.hidden, value: document.getElementById("search").value }; });
    // ask a question; wait for Insight's block for exactly these words
    const ask = async q => { typed.push(q); await p.fill("#search", q);
      await p.waitForFunction(q => { const b = document.querySelector("#search-results > .sr-fit"); return b && b.dataset.q === q; }, q, { timeout: 20000 }).catch(() => {});
      return snap(); };
    // what the sheet shows
    const sheet = () => p.evaluate(() => { const s = document.querySelector("#evsheet.open .panel .ins"); if (!s) return null; const one = o => ({ short: (o.querySelector(".ask-short") || {}).textContent || "", but: !!o.querySelector(".ask-but"),
        how: o.querySelector("details.ask-how") ? o.querySelector("details.ask-how").open : null, bars: !!o.querySelector(".ask-foot .meter"), ev: !!o.querySelector('a.ask-ev[href^="#cl_"]'), page: (o.querySelector(".ins-page a") || {}).textContent || "" });
      return { title: document.getElementById("ev-title").textContent, cls: s.className, eye: (document.querySelector("#evsheet .ins-eye") || {}).textContent || "",
        guess: !!s.querySelector(".ins-guess, [data-ins-guess], [data-ins-skip], .ins-verdict") || /First, a guess|Skip to the answer/.test(s.textContent),
        routes: [...s.querySelectorAll("a.ins-route")].map(a => a.dataset.insRoute + ": " + a.querySelector(".t").textContent),
        ones: [...s.querySelectorAll(".ins-one")].map(o => Object.assign({ label: o.querySelector(".ins-l-k").textContent, q: o.querySelector(".ins-l-q").textContent }, one(o))), single: s.querySelector(":scope > .ins-ans") ? one(s) : null,
        none: (s.querySelector(".ins-none-t") || {}).textContent || "", askBtn: (s.querySelector(".ins-none button") || {}).textContent || "", related: [...s.querySelectorAll(".ins-rel a")].map(a => a.dataset.insightNext),
        next: [...s.querySelectorAll(".ins-next a")].map(a => a.dataset.insightNext), nextLabel: (s.querySelector(".ins-next .rn-k") || {}).textContent || "", sos: (s.querySelector(".ins-sos") || {}).textContent || "", end: (s.querySelector(".ins-end-t") || {}).textContent || "",
        moving: [...s.querySelectorAll("*")].filter(e => getComputedStyle(e).animationName !== "none").map(e => e.className).slice(0, 3), focus: document.activeElement && document.activeElement.id, searchOpen: !document.getElementById("search-results").hidden, hash: location.hash }; });
    const enter = async () => { await p.press("#search", "Enter"); await p.waitForSelector("#evsheet.open .panel .ins", { timeout: 15000 }).catch(() => {}); await p.waitForTimeout(150); return sheet(); };
    const closed = () => p.evaluate(() => ({ sheet: !!document.querySelector("#evsheet.open"), value: document.getElementById("search").value, open: !document.getElementById("search-results").hidden, fit: (document.querySelector("#search-results > .sr-fit") || { dataset: {} }).dataset.q || "", hash: location.hash,
      focus: (document.activeElement && (document.activeElement.id || document.activeElement.className)) || "" }));
    const uiText = () => p.evaluate(() => [...document.querySelectorAll(".sr-note, .sr-fit-h, .sr-fit-none, .sr-route, .sr-sos, .sr-get, .ins-route, .ins-l-k, .ins-none, .ins-end, .ins-next .rn-k, .ins-rel .rn-k, .ins-eye, .ins-sos, .ins-page")].map(e => e.textContent).join(" | "));
    let ui = "";

    // ---- the start page: nothing of Insight's fetched
    await p.goto(BASE + "home"); await p.waitForTimeout(2500);
    ok(w + ": the start page fetches none of Insight's files", !reqs.some(ins), reqs.filter(ins).join(", ") || "none");
    // the cursor in the search box: the files come, from the site itself, and the quiet line shows once ready
    const t0 = Date.now(); await p.focus("#search");
    const ready = await whenReady(); const loadMs = Date.now() - t0; await p.waitForTimeout(300);
    const got = reqs.filter(ins).map(u => u.replace(/^.*\//, "")), outside = reqs.filter(u => !u.startsWith(ORIGIN) && !u.startsWith("data:") && !u.startsWith("blob:"));
    const need = ["insight.json", "ort.wasm.min.js", "ort-wasm-simd-threaded.mjs", "ort-wasm-simd-threaded.wasm", MODEL, "vocab.txt"];
    ok(w + ": the cursor in the search box fetches Insight's files from the site itself (the model the index names, once), with no cache-busting, and it gets ready", ready && need.every(f => got.includes(f)) && got.filter(f => /\.onnx$/.test(f)).length === 1 && !outside.length && !got.some(f => /jsep|webgpu/i.test(f)) && !reqs.filter(ins).some(u => u.includes("?")),
      "ready in " + loadMs + " ms; fetched " + got.join(", ") + (outside.length ? "; OUTSIDE: " + outside.join(", ") : ""));
    const sug = await p.evaluate(() => { const b = document.getElementById("search-results"); return { note: (b.querySelector(":scope > .sr-note") || {}).textContent || "", sug: b.querySelectorAll("a.sr-sug").length }; });
    ok(w + ": once ready, one quiet line under the box says it runs on the device", /^Runs on your (phone|computer)\. Nothing you type leaves it\.$/.test(sug.note.trim()) && sug.sug > 0, JSON.stringify(sug));
    const set = await p.evaluate(() => ({ tiers: pkInsight.tiers(), weights: pkInsight.weights() }));
    ok(w + ": the page's thresholds and weights are those of data/insight.json", JSON.stringify(set.tiers) === JSON.stringify(INDEX.tiers) && JSON.stringify(set.weights) === JSON.stringify(INDEX.weights), JSON.stringify(set.tiers));

    // ---- honest tiers
    for (const [q, want] of REAL) {
      const r = await ask(q); ui += " " + await uiText();
      if (q === REAL[0][0]) await shot("list-matched");
      const b = r.best[0] || {};
      ok(w + ": “" + q + "” has its answer as best match, the short answer in full in the list, with its rating", r.open && r.first === "sr-note" && r.kids[0] === "h:Best match" && b.id === want && b.whole && b.bars && r.best.length <= 2 && r.related.length <= 3 && !r.none && !r.wordBest && /^Best match: /.test(r.live),
        (b.id ? b.k + ": " + b.q + " / " + b.a : "no best match") + "; related " + r.related.length + "; heard: " + r.live);
    }
    const al = await ask(ALCOHOL); ui += " " + await uiText(); await shot("list-unmatched");
    ok(w + ": “" + ALCOHOL + "” says “We haven’t checked exactly this yet” with “Ask us to check it”, no best match; a near answer shows under Related at most", al.kids[0] === "none" && !al.best.length && al.none === "We haven’t checked exactly this yet." && al.askBtn === "Ask us to check it" && al.kids.indexOf("h:Related") === 1 &&
      al.related.length >= 1 && al.related.length <= 3 && !al.kids.includes("h:Best match") && !al.wordBest && /^We haven’t checked exactly this yet/.test(al.live), al.kids.join(" > ") + "; related: " + al.related.map(x => x.k + ": " + x.q).join("; ") + "; heard: " + al.live);
    const no = await ask(NONE); ui += " " + await uiText();
    ok(w + ": a question about something else (“" + NONE + "”) says it has not been checked, offers nothing, and “Ask us to check it” carries the words typed", !no.best.length && !no.related.length && no.kids.join() === "none" && no.askBtn === "Ask us to check it" && !no.wordAsk, no.kids.join(" > ") + " | " + no.text.replace(/\s+/g, " "));
    await p.click("#search-results .sr-fit-none button"); await p.waitForTimeout(400);
    const pn = await p.evaluate(() => ({ open: document.getElementById("report").classList.contains("open"), msg: document.getElementById("report-message").value, mode: (document.querySelector('.fb-opt[aria-pressed="true"]') || { dataset: {} }).dataset.mode }));
    ok(w + ": its “Ask us to check it” opens Ask a question with the words typed", pn.open && pn.msg === NONE && pn.mode === "feedback", JSON.stringify(pn));
    await p.keyboard.press("Escape"); await p.waitForTimeout(200);

    // ---- routes: each has its test
    const rt = await p.evaluate(E => E.map(([q, want, drug]) => { const r = pkInsight.read(q, drug ? { drug } : {}); return r.note === "blocked" ? "blocked" : r.routes.join("+"); }), ROUTES);
    const rbad = ROUTES.map(([q, want], i) => rt[i] === want ? null : "“" + q + "” took [" + rt[i] + "], not [" + want + "]").filter(Boolean);
    ok(w + ": every route takes the questions that are its own and leaves the ones that only look like it (" + ROUTES.length + " questions: mixing, doses, an emergency, testing, a drug's page, and what we do not answer)", !rbad.length, rbad.slice(0, 4).join("; ") || ROUTES.filter(x => x[1]).length + " routed, " + ROUTES.filter(x => !x[1]).length + " left alone");
    const dp = await p.evaluate(E => E.map(([q]) => { const r = pkInsight.read(q); return [r.depth, r.core]; }), DEPTH);
    const dbad = DEPTH.map(([q, d, core], i) => dp[i][0] === d && dp[i][1] === core ? null : "“" + q + "” read as [" + dp[i].join(": ") + "]").filter(Boolean);
    ok(w + ": depth words are understood and taken out before matching (" + DEPTH.length + " questions)", !dbad.length, dbad.slice(0, 3).join("; ") || "“" + KETAMINE + "” is matched as “" + dp[0][1] + "”");
    // two drugs: the mixing row first; it opens the mixing tool with both chosen
    const mx = await ask(MIX); ui += " " + await uiText(); await shot("list-mixing-row");
    ok(w + ": “" + MIX + "” shows the mixing row first, then the checked mixing answer", mx.kids[0] === "route:mix" && mx.routes[0].t === "MDMA + alcohol: what’s known about mixing them" && (mx.best[0] || {}).id === "cl_mix_mdma_alcohol" && mx.kids[1] === "h:Best match",
      mx.kids.join(" > ") + "; " + JSON.stringify(mx.routes[0]));
    await p.click("#search-results a.sr-route"); await p.waitForTimeout(900);
    const tool = await p.evaluate(() => ({ hash: location.hash, pressed: [...document.querySelectorAll('#mix2 .mixchip[aria-pressed="true"]')].map(b => b.dataset.mix).sort().join("+"), line: (document.querySelector("#mix2 .mix-n") || {}).textContent || "",
      shown: [...document.querySelectorAll("#mix2 details.ask[data-cid]")].filter(d => !d.hidden).map(d => d.dataset.cid), both: [...document.querySelectorAll("#mix2 details.ask[data-cid]")].filter(d => !d.hidden).every(d => (MIXFOR[d.dataset.cid] || []).includes("mdma") && (MIXFOR[d.dataset.cid] || []).includes("alcohol")),
      top: Math.round(document.getElementById("mix2").getBoundingClientRect().top), search: document.getElementById("search").value }));
    await shot("mixing-tool-both-chosen");
    ok(w + ": the mixing row opens the mixing tool with both drugs chosen, on the answers about both", tool.hash === "#interactions" && tool.pressed === "alcohol+mdma" && tool.shown.includes("cl_mix_mdma_alcohol") && tool.both && tool.top >= 0 && tool.top < H * 0.6 && tool.search === "", JSON.stringify(tool));
    // a dose question: the Doses row, and no amount from us
    await p.goto(BASE + "home"); await p.waitForTimeout(500); await p.focus("#search"); await whenReady();
    const ds = await ask(DOSE); ui += " " + await uiText(); await shot("list-doses-row");
    ok(w + ": “" + DOSE + "” shows the Doses row first and no amount", ds.kids[0] === "route:dose" && ds.routes[0].t === "We don’t list doses. These harm reduction groups do" && ds.routes[0].k === "MDMA" && !AMOUNT.test(ds.text) && !ds.none && !ds.best.length,
      ds.kids.join(" > ") + "; " + ds.text.replace(/\s+/g, " ").slice(0, 160));
    await p.press("#search", "Enter"); await p.waitForTimeout(1500);
    const dose = await p.evaluate(() => { const el = document.getElementById("sf-dose"), r = el ? el.getBoundingClientRect() : null; return { hash: location.hash, sheet: !!document.querySelector("#evsheet.open"), top: r ? Math.round(r.top) : null, text: el ? el.innerText.replace(/\s+/g, " ").slice(0, 120) : "", search: document.getElementById("search").value }; });
    await shot("doses-block");
    ok(w + ": Enter on a dose question goes to that drug's Doses block (which lists no dose of ours)", dose.hash === "#s-mdma" && !dose.sheet && dose.top !== null && dose.top >= 0 && dose.top < H * 0.6 && /We don’t list doses/.test(dose.text) && !AMOUNT.test(dose.text) && dose.search === "", JSON.stringify(dose));
    // an emergency in progress: the help row and the emergency number line; no nearby answers
    await p.goto(BASE + "home"); await p.waitForTimeout(500); await p.focus("#search"); await whenReady();
    const hp = await ask(HELP); ui += " " + await uiText(); await shot("list-emergency");
    ok(w + ": an emergency (“" + HELP + "”) shows “If it gets too much: what helps” first, with the emergency number line and no related answers", hp.kids[0] === "route:help" && hp.kids[1] === "sos" && hp.routes[0].t === "If it gets too much: what helps" && hp.routes[0].k === "Ketamine" && hp.routes[0].href === "#s-ketamine/part-d-help" &&
      /Emergency numbers by country|Emergency number in /.test(hp.sos) && !hp.related.length && !hp.none, hp.kids.join(" > ") + "; " + hp.sos);
    await p.click("#search-results a.sr-route"); await p.waitForTimeout(1300);
    const help = await p.evaluate(() => { const el = document.getElementById("d-help"), r = el ? el.getBoundingClientRect() : null; return { hash: location.hash, top: r ? Math.round(r.top) : null, h: el ? el.querySelector("h2").textContent : "" }; });
    ok(w + ": its row opens the drug's “If it gets too much” part", help.hash === "#s-ketamine/part-d-help" && help.top !== null && help.top >= 0 && help.top < H * 0.6 && help.h.length > 5, JSON.stringify(help));
    // testing a sample; "what is X"; and what we do not answer
    await p.goto(BASE + "home"); await p.waitForTimeout(500); await p.focus("#search"); await whenReady();
    const ts = await ask(TEST); ui += " " + await uiText();
    await p.click("#search-results a.sr-route"); await p.waitForTimeout(1500);
    const kit = await p.evaluate(() => { const el = document.getElementById("sf-test"), r = el ? el.getBoundingClientRect() : null; return { hash: location.hash, top: r ? Math.round(r.top) : null }; });
    ok(w + ": “" + TEST + "” shows the test kits row first, and it opens that drug's test kits", ts.kids[0] === "route:test" && ts.routes[0].t === "Test kits for MDMA" && kit.hash === "#s-mdma" && kit.top !== null && kit.top >= 0 && kit.top < H * 0.6, ts.kids.join(" > ") + "; " + JSON.stringify(kit));
    await p.goto(BASE + "home"); await p.waitForTimeout(500); await p.focus("#search"); await whenReady();
    const wk = await ask("what is ketamine"); await p.press("#search", "Enter"); await p.waitForTimeout(900);
    const wkAt = await p.evaluate(() => ({ hash: location.hash, sheet: !!document.querySelector("#evsheet.open") }));
    ok(w + ": “what is ketamine” puts the drug's page first, and Enter goes there", wk.kids[0] === "route:page" && wk.routes[0].t === "Ketamine" && wk.routes[0].href === "#s-ketamine" && wkAt.hash === "#s-ketamine" && !wkAt.sheet, wk.kids.join(" > ") + "; " + JSON.stringify(wkAt));
    await p.goto(BASE + "home"); await p.waitForTimeout(500); await p.focus("#search"); await whenReady();
    const by = await ask(BUY); ui += " " + await uiText(); await shot("list-not-answered");
    // (the word search may still list the drug's own page; never an answer, never a way to ask us)
    const byRows = await p.evaluate(() => { const rows = [...document.querySelectorAll("#search-results > a")]; return { all: rows.length, ans: rows.filter(a => a.matches(".sr-ans")).length, pages: rows.filter(a => /^#s-[a-z0-9-]+$/.test(a.getAttribute("href") || "")).length }; });
    ok(w + ": getting drugs (“" + BUY + "”): no route, no answer, “We haven’t checked exactly this yet” without the way to ask us (the drug's own page at most)", by.kids[0] === "none" && by.kids.every(k => k === "none" || k === "h:More results") && by.none === "We haven’t checked exactly this yet." && !by.askBtn && !by.best.length && !by.related.length && !by.routes.length && !by.wordAsk &&
      byRows.ans === 0 && byRows.all <= 2 && byRows.pages === byRows.all, by.kids.join(" > ") + " | " + by.text.replace(/\s+/g, " ") + " | rows under it: " + JSON.stringify(byRows));

    // ---- Enter: the sheet for the question as asked
    const kl = await ask(KETAMINE); const ks = await enter(); ui += " " + await uiText(); await shot("sheet-after-enter-full-evidence");
    const kOnes = ks ? ks.ones : [];
    ok(w + ": “" + KETAMINE + "” + Enter opens a sheet headed with those words, with no guess step, and “How do we know?” open under the checked question it answers",
      ks && ks.title === "Give me the full evidence about how can i die from ketamine" && !ks.guess && /ins-full/.test(ks.cls) && /Your question/.test(ks.eye) && !ks.searchOpen && !ks.sos &&
        (kOnes.length ? kOnes.length === kl.best.length && kOnes.every(o => o.how === true && o.short && o.bars && o.ev && /^Checked answer · /.test(o.label) && o.q.length > 10 && /^See it on the /.test(o.page)) : ks.none === "We haven’t checked exactly this yet."),
      ks ? ks.title + " | " + (kOnes.length ? kOnes.map(o => o.label + ": " + o.q + " (How do we know? " + (o.how ? "open" : "closed") + ")").join("; ") : "no best match: “" + ks.none + "”") + " | people also ask " + ks.next.length : "no sheet");
    // Back puts the search back as it was
    await p.click("#evsheet .ev-back"); await p.waitForTimeout(350); const b1 = await closed();
    await enter(); await p.keyboard.press("Escape"); await p.waitForTimeout(350); const b2 = await closed();
    await enter(); await p.goBack(); await p.waitForTimeout(350); const b3 = await closed();
    ok(w + ": Back, Escape and the browser's Back close the sheet and put the search back as it was: the question in the box, its answers under it", [b1, b2, b3].every(b => !b.sheet && b.value === KETAMINE && b.open && b.fit === KETAMINE && b.hash === "#home"), [b1, b2, b3].map(b => JSON.stringify(b)).join(" / "));
    // depth on a question that has a best match; and the short of it
    await ask(REAL[0][0] + ", with sources"); const fs1 = await enter();
    ok(w + ": “…, with sources” opens the best match with “How do we know?” open and the way to the evidence", fs1 && fs1.ones.length >= 1 && fs1.ones[0].q === "Does ecstasy harm the brain for good?" && fs1.ones.every(o => o.how === true && o.ev) && /ins-full/.test(fs1.cls) && !fs1.guess && fs1.nextLabel === "People also ask" && fs1.next.length >= 1 && fs1.next.length <= 3,
      fs1 ? fs1.title + " | " + fs1.ones.map(o => o.q).join("; ") + " | people also ask " + fs1.next.length : "no sheet");
    await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    await ask(REAL[0][0] + " tl;dr"); const sh1 = await enter(); await shot("sheet-after-enter-short");
    ok(w + ": “… tl;dr” shows the short answer and its But, nothing more", sh1 && sh1.ones.length >= 1 && sh1.ones.every(o => o.short && o.but && o.how === null && o.bars && o.ev) && /ins-short/.test(sh1.cls) && sh1.title === "Does ecstasy damage your brain permanently tl;dr", sh1 ? sh1.title + " | " + JSON.stringify(sh1.ones[0]) : "no sheet");
    await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    await ask(ALCOHOL); const as = await enter(); await shot("sheet-not-checked");
    ok(w + ": Enter on a question with no best match says so in the sheet, with “Ask us to check it” and the related questions as links", as && as.title === "How can you die from alcohol" && !as.ones.length && as.none === "We haven’t checked exactly this yet." && as.askBtn === "Ask us to check it" && as.related.length >= 1 && as.related.length <= 3 && !as.guess && !as.sos,
      as ? as.none + " | related " + as.related.join(", ") + " | people also ask " + as.next.join(", ") : "no sheet");
    await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    await ask(MIX); const ms = await enter(); await shot("sheet-mixing");
    ok(w + ": Enter on a mixing question: the mixing row first in the sheet, then the checked answer in full", ms && ms.routes[0] === "mix: MDMA + alcohol: what’s known about mixing them" && ms.ones.length >= 1 && ms.ones[0].q === "What happens when you mix MDMA with alcohol?" && ms.ones[0].short, ms ? ms.routes.join("; ") + " | " + ms.ones.map(o => o.q).join("; ") : "no sheet");
    await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    await ask(HELP); const hs = await enter();   // (an emergency with no checked answer of its own: Enter goes straight to the help part)
    const hAt = await p.evaluate(() => location.hash);
    ok(w + ": Enter on an emergency goes straight to “If it gets too much”", !hs && hAt === "#s-ketamine/part-d-help", hAt);
    await p.goto(BASE + "home"); await p.waitForTimeout(500); await p.focus("#search"); await whenReady();

    // ---- one row tapped: that one answer, at once (no guess), no emergency line; its evidence comes back to it; next questions; the calm end
    await ask(REAL[0][0]);
    await p.click('#search-results a[data-insight="' + REAL[0][1] + '"]'); await p.waitForSelector("#evsheet.open .ins"); await p.waitForTimeout(200);
    const o1 = await sheet(); ui += " " + await uiText(); await shot("sheet-one-answer");
    ok(w + ": a row tapped opens that one answer at once: no guess, no emergency line; the short answer, its rating, the evidence, the way to its page, and up to 3 next questions", o1 && o1.title === "Does ecstasy harm the brain for good?" && !o1.guess && !o1.sos && o1.single && o1.single.short && o1.single.bars && o1.single.ev && o1.single.how === false &&
      /^See it on the MDMA page/.test(o1.single.page) && o1.nextLabel === "People also ask" && o1.next.length >= 1 && o1.next.length <= 3 && !o1.searchOpen && !o1.moving.length, o1 ? JSON.stringify({ title: o1.title, single: o1.single, next: o1.next, moving: o1.moving }) : "no sheet");
    await p.click("#evsheet .ins-ans a.ask-ev"); await p.waitForFunction(() => document.querySelector("#evsheet.open") && !document.querySelector("#evsheet .ins") && !document.querySelector("#evsheet .loading"), null, { timeout: 15000 }).catch(() => {});
    await p.click("#evsheet .ev-back"); await p.waitForTimeout(300);
    const back = await p.evaluate(() => ({ open: !!document.querySelector("#evsheet.open"), ins: !!document.querySelector("#evsheet .ins .ins-ans"), title: (document.getElementById("ev-title") || {}).textContent }));
    ok(w + ": the evidence opened from the answer comes back to it with Back", back.open && back.ins && back.title === "Does ecstasy harm the brain for good?", JSON.stringify(back));
    const run = [REAL[0][1]];
    for (let i = 0; i < 3; i++) {
      const nx = await p.evaluate(() => { const a = document.querySelector("#evsheet .ins-next a[data-insight-next]"); return a ? a.dataset.insightNext : null; }); if (!nx) break;
      await p.click('#evsheet .ins-next a[data-insight-next="' + nx + '"]'); await p.waitForTimeout(250); run.push(nx);
    }
    const end = await p.evaluate(() => { const e = document.querySelector("#evsheet .ins-end"); return e ? { t: e.querySelector(".ins-end-t").textContent, ask: !!e.querySelector("[data-ins-ask]"), more: !!e.querySelector("[data-ins-more]"), next: document.querySelectorAll("#evsheet .ins-next").length, guess: !!document.querySelector("#evsheet .ins-guess") } : null; });
    ui += " " + await uiText();
    ok(w + ": next questions open one after the other, none twice, none with a guess; after four answers in a row, a calm end (Ask something else, or Keep reading)", run.length === 4 && new Set(run).size === 4 && end && end.t === "You’ve read 4 answers" && end.ask && end.more && !end.next && !end.guess, run.join(" > ") + "; " + JSON.stringify(end));
    await p.click("#evsheet [data-ins-ask]"); await p.waitForTimeout(300);
    const after = await p.evaluate(() => ({ closed: !document.querySelector("#evsheet.open"), focus: document.activeElement && document.activeElement.id, value: document.getElementById("search").value }));
    ok(w + ": Ask something else closes the answer and puts the cursor in an empty search box", after.closed && after.focus === "search" && after.value === "", JSON.stringify(after));
    // the questions to try (answer links on the start page) open over the page too
    await p.goto(BASE + "home"); await p.waitForTimeout(500); await p.focus("#search"); await whenReady(); await p.waitForTimeout(200);
    await p.click("#search-results a.sr-sug"); await p.waitForSelector("#evsheet.open .ins", { timeout: 5000 }).catch(() => {});
    const sg = await sheet();
    ok(w + ": a question to try, on the start page, opens its answer over the page", sg && sg.single && sg.single.short && sg.hash === "#home" && !sg.guess, sg ? sg.title + " at " + sg.hash : "no sheet");
    await p.keyboard.press("Escape"); await p.waitForTimeout(300);

    // ---- on a drug's page: "Ask about cannabis"; a question that names no drug is about cannabis
    const ph0 = await p.getAttribute("#search", "placeholder");
    await p.goto(BASE + "s-cannabis"); await p.waitForTimeout(900);
    const ph1 = await p.getAttribute("#search", "placeholder"), boxSeen = await p.evaluate(() => { const r = document.getElementById("search").getBoundingClientRect(); return r.width > 150 && r.top >= 0 && r.bottom <= innerHeight; });
    await p.focus("#search"); await whenReady();
    const bc = await ask("does it kill brain cells"); ui += " " + await uiText(); await shot("list-on-cannabis-page");
    const alc = bc.related.find(x => x.id === "cl_alc_brain_cells");
    ok(w + ": on the cannabis page the box is there and reads “Ask about cannabis”; “does it kill brain cells” does not get the alcohol answer as best match (related at most, under its own drug's name)", ph1 === "Ask about cannabis" && ph0 === "Search or ask a question" && boxSeen &&
      !bc.best.some(x => x.id === "cl_alc_brain_cells") && bc.best.every(x => x.k === "Cannabis") && (!alc || alc.k === "Alcohol") && (bc.best.length > 0 || bc.none === "We haven’t checked exactly this yet."),
      "placeholder “" + ph1 + "”; " + bc.kids.join(" > ") + "; related: " + bc.related.map(x => x.k + ": " + x.q).join("; "));
    const ad = await ask("is it addictive");
    ok(w + ": on the cannabis page “is it addictive” is about cannabis: a cannabis answer is its best match", (ad.best[0] || {}).id === "cl_can_dependence_how_many" && ad.best[0].k === "Cannabis" && ad.best[0].whole, ad.best.map(x => x.k + ": " + x.q).join("; ") || "no best match");
    // next questions of a cannabis answer are about cannabis: in the sheet ...
    await p.click('#search-results a[data-insight="cl_can_dependence_how_many"]'); await p.waitForSelector("#evsheet.open .ins"); await p.waitForTimeout(200);
    const cn = await sheet(), cnAbout = await p.evaluate(ids => ids.map(id => insOnPage("cannabis").has(id) || (KITSFOR[id] || []).includes("cannabis")), cn ? cn.next : []);
    ok(w + ": next questions of a cannabis answer are about cannabis (People also ask)", cn && cn.next.length >= 1 && cn.next.length <= 3 && cnAbout.every(Boolean) && !cn.next.includes("cl_can_dependence_how_many"), cn ? cn.next.join(", ") : "no sheet");
    await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    // the rule, for every answer: the same drug first (its first three next questions are about one of its drugs, as far as its
    // drugs have other answers), and never an answer that shares neither a drug nor a page with it
    const rule = await p.evaluate(() => { const pagesOf = {}; Object.entries(QUESTIONS).forEach(([slug, groups]) => (groups || []).forEach(g => (g.items || []).forEach(it => { if (it[0]) (pagesOf[it[0]] = pagesOf[it[0]] || new Set()).add(slug); })));
      const ids = INS_NEXT.ids, drugsOf = id => INS.idx.has(id) ? INS.about[INS.idx.get(id)] : new Set(), pgs = id => pagesOf[id] || new Set([claimById[id].substance]), share = (a, b) => [...a].some(x => b.has(x));
      const out = { pairs: 0, off: [], late: [], cannabis: 0, cannabisOff: [] };
      ids.forEach((id, i) => { const mine = drugsOf(id), others = mine.size ? ids.filter(x => x !== id && share(mine, drugsOf(x))).length : 0;
        if (mine.has("cannabis")) out.cannabis++;
        INS_NEXT.next[i].forEach((j, n) => { const x = ids[j], same = share(mine, drugsOf(x)); out.pairs++;
          if (!same && !share(pgs(id), pgs(x))) out.off.push(id + " > " + x);
          if (!same && n < Math.min(3, others)) out.late.push(id + " > " + x);
          if (mine.size === 1 && mine.has("cannabis") && n < 3 && !drugsOf(x).has("cannabis")) out.cannabisOff.push(id + " > " + x); }); });
      return out; });
    ok(w + ": for every answer, the next questions are about the same drug first, and none shares neither a drug nor a page with its answer (a cannabis answer never offers a cocaine question)", rule.pairs > 1000 && !rule.off.length && !rule.late.length && rule.cannabis > 20 && !rule.cannabisOff.length,
      rule.pairs + " next questions; " + rule.cannabis + " answers about cannabis; from elsewhere: " + (rule.off.slice(0, 3).join(", ") || "none") + "; another drug before its own: " + (rule.late.concat(rule.cannabisOff).slice(0, 3).join(", ") || "none"));
    // ... and on its page (Read next): on this page only, opening in place, without the answers already opened in this visit
    await p.goto(BASE + "home"); await p.waitForTimeout(300); await p.goto(BASE + "s-cannabis/q-cl_can_dependence_how_many"); await p.waitForTimeout(1500);
    const rnOf = id => p.evaluate(id => [...document.querySelectorAll("#ask-" + id + " .rn-l a")].map(a => ({ id: a.dataset.rnId, href: a.getAttribute("href"), on: insOnPage("cannabis").has(a.dataset.rnId), label: document.querySelector("#ask-" + id + " .rn-k").textContent })), id);
    const rn1 = await rnOf("cl_can_dependence_how_many");
    await p.click("#ask-cl_can_dependence_how_many .rn-l a >> nth=0"); await p.waitForTimeout(1300);
    const inPlace = await p.evaluate(id => ({ open: !!(document.getElementById("ask-" + id) || {}).open, prev: document.getElementById("ask-cl_can_dependence_how_many").open, hash: location.hash, sheet: !!document.querySelector("#evsheet.open") }), rn1.length ? rn1[0].id : "x");
    await p.evaluate(() => document.querySelector("#ask-cl_can_dependence_how_many > summary").click()); await p.waitForTimeout(400);
    const rn2 = await rnOf("cl_can_dependence_how_many");
    const everyPage = await p.evaluate(() => { let n = 0, bad = []; SUBSTANCES.forEach(s => { const here = insOnPage(s.slug); here.forEach(id => { const h = insReadNext(id, [], s.slug, null); [...h.matchAll(/data-rn-id="([^"]+)"/g)].forEach(m => { n++; if (!here.has(m[1]) || m[1] === id) bad.push(s.slug + ": " + id + " > " + m[1]); }); }); }); return { n, bad: bad.slice(0, 3) }; });
    ok(w + ": Read next on the cannabis page offers up to 3 cannabis answers, opens them in place, and leaves out the ones already opened in this visit; on every drug page it keeps to that page", rn1.length >= 1 && rn1.length <= 3 && rn1.every(x => x.on && x.href.startsWith("#s-cannabis/q-") && x.label === "Read next") &&
      inPlace.open && !inPlace.prev && !inPlace.sheet && inPlace.hash === "#s-cannabis/q-cl_can_dependence_how_many" && rn2.length >= 1 && !rn2.some(x => x.id === rn1[0].id) && rn2.every(x => x.on) && everyPage.n > 300 && !everyPage.bad.length,
      rn1.map(x => x.id).join(", ") + " | after opening the first: " + rn2.map(x => x.id).join(", ") + " | " + everyPage.n + " links on all drug pages, off the page: " + (everyPage.bad.join("; ") || "none"));

    // ---- Myth or fact: Read the answer opens over the deck, and the way back returns to the same card, scrolled as it was
    for (const [where, hash, box] of [["the Myth or fact? page", "quiz", "#quizpage"], ["the start page's deck", "home", "#tf"], ["a drug page's own deck", "s-cannabis", "#qz-drug"]]) {
      await p.goto(BASE + "about"); await p.waitForTimeout(200); await p.goto(BASE + hash); await p.waitForTimeout(1100);
      await p.click(box + " .qz2-o >> nth=0"); await p.waitForTimeout(800);
      await p.$eval(box + " .qz2-ev", e => e.scrollIntoView({ block: "center" })); await p.waitForTimeout(200);
      const card = () => p.evaluate(box => ({ q: document.querySelector(box + " .mf-q").textContent, flipped: document.querySelector(box + " .mf-card").classList.contains("flipped"), n: document.querySelector(box + " .qz2-score").textContent, y: Math.round(window.scrollY), hash: location.hash, sheet: !!document.querySelector("#evsheet.open") }), box);
      const c0 = await card(), outs = [];
      for (const how of ["Back", "Escape", "the browser's Back"]) {
        await p.click(box + " .qz2-ev"); await p.waitForSelector("#evsheet.open .ins", { timeout: 5000 }).catch(() => {}); await p.waitForTimeout(200);
        const s = await sheet(); if (how === "Back" && where === "the Myth or fact? page") { ui += " " + await uiText(); await shot("quiz-sheet-open"); }
        if (how === "Back") await p.click("#evsheet .ev-back"); else if (how === "Escape") await p.keyboard.press("Escape"); else await p.goBack();
        await p.waitForTimeout(400); const c = await card();
        outs.push({ how, sheet: !!(s && s.single && s.single.short && !s.guess && s.hash === c0.hash), same: !c.sheet && c.q === c0.q && c.flipped && c.n === c0.n && c.hash === c0.hash && Math.abs(c.y - c0.y) <= 2, y: c.y });
      }
      ok(w + ": " + where + ": Read the answer opens the answer over the deck; Back, Escape and the browser's Back return to the same card, scrolled as it was", c0.flipped && outs.every(o => o.sheet && o.same), "card “" + c0.q.slice(0, 50) + "” " + c0.n + " at y " + c0.y + "; " + outs.map(o => o.how + ": " + (o.sheet ? "sheet" : "NO SHEET") + ", " + (o.same ? "same card" : "MOVED (y " + o.y + ")")).join("; "));
    }
    // a shared answer's other questions open over it
    await p.goto(BASE + "a/lsd/cl_lsd_chromosomes"); await p.waitForTimeout(900);
    await p.click("#shared-body .sh-others a >> nth=0"); await p.waitForSelector("#evsheet.open .ins", { timeout: 5000 }).catch(() => {});
    const so = await sheet();
    ok(w + ": on a shared answer's page, another question opens over it (the page stays)", so && so.single && so.single.short && so.hash === "#a/lsd/cl_lsd_chromosomes", so ? so.title + " at " + so.hash : "no sheet");
    await p.keyboard.press("Escape"); await p.waitForTimeout(300);

    ok(w + ": no “AI” words in what Insight shows", ui.trim().length > 200 && !AI_WORDS.test(ui), (ui.match(AI_WORDS) || ["none"])[0]);
    // the promise under the box: nothing typed is sent anywhere, or kept (Ask us sends nothing either: it opens a form)
    const forms = q => [q, encodeURIComponent(q), q.replace(/ /g, "+"), q.replace(/ /g, "%20")];
    const leaked = sent.filter(x => typed.some(q => forms(q).some(f => x.includes(f))));
    const kept = await p.evaluate(qs => { const all = [JSON.stringify(history.state || "")]; for (const st of [localStorage, sessionStorage]) for (let i = 0; i < st.length; i++) all.push(st.getItem(st.key(i)) || ""); return qs.filter(q => all.some(v => v.includes(q))); }, typed);
    ok(w + ": nothing typed leaves the page or is kept on the device (" + new Set(typed).size + " questions, " + sent.length + " requests)", typed.length >= 15 && !leaked.length && !kept.length, (leaked.concat(kept).join(" | ") || "none").slice(0, 200));
    times.push(...await p.evaluate(() => pkInsight.times()));
    await ctx.close();
  }
  // where the reader's country is known, the emergency row carries that country's number (and only the emergency row)
  { const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true }), p = await ctx.newPage();
    p.on("pageerror", e => errors.push("country page error: " + String(e).slice(0, 200)));
    await p.addInitScript(() => { try { localStorage.setItem("pk-country", "Greece"); } catch (e) {} });
    await p.goto(BASE + "home"); await p.waitForTimeout(800); await p.focus("#search");
    await p.waitForFunction(() => window.pkInsight && pkInsight.state() === "ready", null, { timeout: 120000 }).catch(() => {});
    await p.fill("#search", HELP); await p.waitForFunction(q => { const b = document.querySelector("#search-results > .sr-fit"); return b && b.dataset.q === q; }, HELP, { timeout: 20000 }).catch(() => {});
    const sos = await p.evaluate(() => { const e = document.querySelector("#search-results .sr-sos"); return e ? { t: e.textContent, tel: (e.querySelector('a[href^="tel:"]') || { getAttribute: () => "" }).getAttribute("href") } : null; });
    if (SHOTS) await p.screenshot({ path: path.join(SHOTS, "390-insight-list-emergency-country-known.png") });
    await p.fill("#search", REAL[0][0]); await p.waitForFunction(q => { const b = document.querySelector("#search-results > .sr-fit"); return b && b.dataset.q === q; }, REAL[0][0], { timeout: 20000 }).catch(() => {});
    await p.press("#search", "Enter"); await p.waitForSelector("#evsheet.open .ins", { timeout: 10000 }).catch(() => {});
    const calm = await p.evaluate(() => ({ list: !!document.querySelector("#search-results .sr-sos"), sheet: !!document.querySelector("#evsheet .ins-sos"), unwell: /Someone unwell/.test((document.querySelector("#evsheet .panel") || {}).textContent || "") }));
    ok("390, country known: the emergency row carries the local emergency number; an ordinary answer carries no emergency line at all", sos && /^Emergency number in Greece: 112 · Other numbers$/.test(sos.t.trim()) && sos.tel === "tel:112" && !calm.list && !calm.sheet && !calm.unwell, JSON.stringify(sos) + " " + JSON.stringify(calm));
    await ctx.close(); }
  // Enter before Insight is ready: the question waits, and its sheet opens once ready
  { const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } }), p = await ctx.newPage();
    p.on("pageerror", e => errors.push("early-enter page error: " + String(e).slice(0, 200)));
    let release; const hold = new Promise(r => { release = r; });
    await p.route(/\/insight\/vocab\.txt$/, async r => { await hold; await r.continue(); });
    await p.goto(BASE + "home"); await p.waitForTimeout(800); await p.focus("#search"); await p.fill("#search", REAL[2][0]); await p.waitForTimeout(400);
    await p.press("#search", "Enter"); await p.waitForTimeout(500);
    const mid = await p.evaluate(() => ({ state: pkInsight.state(), sheet: !!document.querySelector("#evsheet.open"), hash: location.hash, line: (document.querySelector("#search-results .sr-get") || {}).textContent || "" }));
    release(); await p.waitForSelector("#evsheet.open .ins", { timeout: 120000 }).catch(() => {});
    const done = await p.evaluate(() => ({ title: (document.getElementById("ev-title") || {}).textContent || "", q: (document.querySelector("#evsheet .ins-l-q") || {}).textContent || "" }));
    ok("1280, Enter before Insight is ready: the page stays, a quiet line says it is getting ready, and the sheet opens once ready", mid.state === "loading" && !mid.sheet && mid.hash === "#home" && /getting ready/.test(mid.line) && done.title === "How long does ketamine stay in your blood" && done.q === "How long does ketamine stay in the blood?", JSON.stringify(mid) + " then " + JSON.stringify(done));
    await ctx.close(); }
  // a second visit, in a browser with a profile of its own as people have (a test context keeps no disk cache): the files
  // come back from the browser's cache, revalidated (304), and nothing is downloaded again
  { const dir = fs.mkdtempSync(path.join(os.tmpdir(), "pk-insight-"));
    const ctx = await chromium.launchPersistentContext(dir, { args: ["--no-proxy-server"], viewport: { width: 390, height: 844 } }), p = ctx.pages()[0] || await ctx.newPage();
    p.on("pageerror", e => errors.push("second-visit page error: " + String(e).slice(0, 200)));
    const visit = async again => { await p.goto(BASE + "home"); if (again) await p.reload(); await p.waitForTimeout(600); await p.focus("#search");
      return p.waitForFunction(() => window.pkInsight && pkInsight.state() === "ready", null, { timeout: 120000 }).then(() => true, () => false); };
    const first = await visit(false), mark = served.length, second = await visit(true);
    const big = served.slice(mark).filter(x => /\/insight\//.test(x.p)), bytes = big.reduce((a, x) => a + x.bytes, 0);
    ok("a second visit downloads the model and runtime nothing again (the browser's cache, revalidated)", first && second && big.some(x => /\.onnx$/.test(x.p)) && big.some(x => /\.wasm$/.test(x.p)) && bytes === 0,
      big.map(x => x.p.replace(/^.*\//, "") + " " + x.status).join(", ") || "not requested");
    await ctx.close(); fs.rmSync(dir, { recursive: true, force: true }); }
  // saving data: nothing fetched on focus; one quiet line offers it, and the word search works meanwhile
  { const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
    await ctx.addInitScript(() => { try { Object.defineProperty(Navigator.prototype, "connection", { configurable: true, get: () => ({ saveData: true, effectiveType: "4g", addEventListener() {} }) }); } catch (e) {} });
    const p = await ctx.newPage();
    p.on("pageerror", e => errors.push("save-data page error: " + String(e).slice(0, 200)));
    p.on("console", m => { if (m.type() === "error") errors.push("save-data console error: " + m.text().slice(0, 200)); });
    const reqs = []; p.on("request", r => reqs.push(r.url()));
    const ins = u => /\/data\/insight\.json|\/insight\//.test(u);
    await p.goto(BASE + "home"); await p.waitForTimeout(800); await p.focus("#search"); await p.fill("#search", REAL[1][0]); await p.waitForTimeout(1500);
    const s1 = await p.evaluate(() => { const b = document.getElementById("search-results"); return { get: (b.querySelector(":scope > .sr-get") || {}).textContent || "", last: !!(b.lastElementChild && b.lastElementChild.matches(".sr-get")), words: b.querySelectorAll("a.sr-ans").length, fit: !!b.querySelector(".sr-fit") }; });
    if (SHOTS) await p.screenshot({ path: path.join(SHOTS, "390-insight-save-data.png") });
    ok("390, saving data: nothing of Insight's fetched on focus or typing; the word search answers; one quiet line under the results offers it, with its size", !reqs.some(ins) && /^Understand questions in your own words \(downloads about \d\d MB once\)$/.test(s1.get) && s1.last && s1.words > 0 && !s1.fit, JSON.stringify(s1) + "; fetched " + (reqs.filter(ins).join(", ") || "none"));
    await p.click("#search-results [data-ins-get]");
    const ready = await p.waitForFunction(() => window.pkInsight && pkInsight.state() === "ready", null, { timeout: 120000 }).then(() => true, () => false);
    await p.waitForFunction(id => document.querySelector('#search-results a[data-insight="' + id + '"]'), REAL[1][1], { timeout: 20000 }).catch(() => {});
    const s2 = await p.evaluate(() => ({ best: [...document.querySelectorAll("#search-results .sr-fit a.sr-best")].map(a => a.dataset.insight), get: !!document.querySelector("#search-results .sr-get") }));
    ok("390, saving data: tapping the line downloads it, and the question gets its best match", ready && reqs.some(ins) && s2.best.includes(REAL[1][1]) && !s2.get, JSON.stringify(s2));
    await ctx.close(); }
  // less motion, and motion allowed: nothing that Insight adds moves (the guess and its turning verdict are gone)
  for (const reduce of [true, false]) { const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, reducedMotion: reduce ? "reduce" : "no-preference" }), p = await ctx.newPage();
    p.on("pageerror", e => errors.push("motion page error: " + String(e).slice(0, 200)));
    p.on("console", m => { if (m.type() === "error") errors.push("motion console error: " + m.text().slice(0, 200)); });
    await p.goto(BASE + "home"); await p.waitForTimeout(800); await p.focus("#search");
    await p.waitForFunction(() => window.pkInsight && pkInsight.state() === "ready", null, { timeout: 120000 }).catch(() => {});
    await p.fill("#search", MIX);
    await p.waitForFunction(q => { const b = document.querySelector("#search-results > .sr-fit"); return b && b.dataset.q === q; }, MIX, { timeout: 20000 }).catch(() => {});
    const moving = sel => p.evaluate(sel => [...document.querySelectorAll(sel)].filter(e => { const c = getComputedStyle(e); return c.animationName !== "none" || parseFloat(c.transitionDuration) > 0 && /transform|all|opacity|height/.test(c.transitionProperty) && (e.matches(".sr-fit, .sr-fit > *, .ins, .ins-one, .ins-l, .ins-none, .ins-route, .sr-route")); }).map(e => e.className).slice(0, 4), sel);
    const m1 = await moving("#search-results .sr-fit, #search-results .sr-fit *");
    await p.press("#search", "Enter"); await p.waitForSelector("#evsheet.open .ins", { timeout: 10000 }).catch(() => {});
    const m2 = await moving("#evsheet .ins, #evsheet .ins-route, #evsheet .ins-one, #evsheet .ins-one > *, #evsheet .ins-l");
    ok("390, " + (reduce ? "less motion" : "motion allowed") + ": the answers in the list and in the sheet appear without moving", !m1.length && !m2.length && !!(await p.$("#evsheet.open .ins-one")), "moving: " + (m1.concat(m2).join(", ") || "nothing"));
    await ctx.close(); }
  await browser.close(); server.close();
  const s = times.slice().sort((a, b) => a - b), med = s.length ? s[Math.floor(s.length / 2)] : NaN;
  console.log("Time per question (two looks: the question to numbers twice, then every answer ranked; " + s.length + " questions): median " + med.toFixed(1) + " ms, slowest " + (s[s.length - 1] || NaN).toFixed(1) + " ms");
  ok("no console errors or sideways scroll", !errors.length, errors.slice(0, 6).join(" | "));
  const failed = results.filter(x => !x).length;
  console.log(failed ? failed + " of " + results.length + " checks failed" : "All " + results.length + " checks passed");
  process.exit(failed ? 1 : 0);
})().catch(e => { console.error(e); server.close(); process.exit(1); });
