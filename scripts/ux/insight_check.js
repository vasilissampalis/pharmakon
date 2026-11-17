// Insight (site 2.3, 15 November 2026), checked in a real browser at 390 x 844 and 1280 x 800, with the site served as
// Cloudflare Pages serves it (the file types, revalidated caching, and the security policy of site/public/_headers).
// What must hold (the 2.3 brief, scripts/insight/BRIEF-2.3-insight.md):
// - every published file is under 25 MiB; the start page fetches none of Insight's files; the cursor in the search box fetches
//   them, from the site itself only, the model being the one the index names; a second visit downloads nothing again; on a
//   connection that saves data nothing is fetched until the reader taps the line that offers it;
// - honest tiers: a question the site answers in so many words ("is weed addictive") has its answer as "Best match", the short
//   answer in full in the list; a drug question it does not answer exactly ("is modafinil safe", "give me the full evidence
//   about how can i die from ketamine") says "We haven't checked exactly this yet" with "Ask us to check it", and a near
//   answer shows under "Related" at most; (2.5) a question on our list ("how can you die from alcohol") says "Not answered
//   yet. A question like yours is on our list"; a question that is not about drugs gets no promise ("This does not look like a question about drugs"); (2.9) a question that is not finished gets no verdict ("Which drug do you mean?", "Go on."), and one whose single unknown word may be a drug's name is told so. What is a best match is decided by the judge whose numbers,
//   like the weights and the tiers, the page reads from data/insight.json (set in site/insight/model.json): no number here;
// - routes, each with its test: two drugs (the mixing row first, opening the mixing tool with both chosen), a dose (the
//   Doses row, no amount), an emergency (the help row and the emergency number line, which shows nowhere else), testing a
//   sample, "what is X", and no route and no answer for getting drugs, hiding use or beating a drug test;
// - Enter opens the sheet for the question as asked, headed with the person's own words, depth words understood ("full
//   evidence": How do we know? open, also in a related answer opened from there; "tl;dr": the short answer and its But), with
//   no guess step anywhere;
// - on a drug's page the box reads "Ask Insight about <drug>" (2.15: the same Insight on every page, and named) and a question that names no drug is about that drug;
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
const REAL = [["is weed addictive", "cl_can_dependence_how_many"], ["can you fail a drug test from secondhand weed smoke", "cl_can_secondhand_test"],
  ["how long does ketamine stay in your blood", "cl_ket_halflife_norketamine"]];
// a question whose answer is on the site in other words: its answer must come first, as best match or, when the judge is not sure, first under Related
const ECSTASY = ["does ecstasy damage your brain permanently", "cl_mdma_neurotoxicity_contested"];
// (2.5) UNCHECKED: a drug question with no answer that is not on our list; LISTED: one that is on the list (data/site/wanted.json);
// NONE: a question that is not about drugs
const UNCHECKED = "is modafinil safe", LISTED = "how can you die from alcohol", KETAMINE = "give me the full evidence about how can i die from ketamine", NONE = "what is the capital of mongolia";
// (2.9) a question that is not finished, with no drug named and with one; a question whose one unknown word may be a drug's name;
// and questions each read as finished or not by their words alone: [question, how it is read ("" finished), asked on a drug's page]
const UNFIN = "can i die from", UNFIN_DRUG = "can i mix cocaine with", STRANGER = "is tusi dangerous", MISSPELT = "is cocane bad for your heart";
const WORDS = [["can i die from ", "ends"], ["is it addictive", "which"], ["is it addictive", "", true], ["can you overdose", "which"], ["how long does it last", "which"], ["how long does it last", "", true],
  ["what is tolerance", ""], ["how long does withdrawal last", ""], ["why do people get addicted", ""], ["what is it cut with", "which"], ["what are pills cut with", ""], ["what is heroin cut with", ""],
  ["is cocaine", "bare"], ["what is ketamine", ""], ["what is ketamine for", ""], ["weed and alcohol", ""], ["weed and", "ends"], ["how does mdma", "bare"], ["can i die from coc", "typing"], ["is weed lega", "typing"],
  ["is cocaine addi", "typing"], ["can a gay man go to the court", ""], ["who are you", ""], ["what time is it", ""], ["how much ecstasy is too much", ""], ["what does it feel like", "which"], ["what does lsd feel like", ""],
  ["does cannabis cause cancer", ""], ["is sex better with weed", ""], ["what happens if i take", "which"], ["what should i know about", "ends"], ["what is the best way to", "ends"], ["is it", "bare", true], ["how much", "bare", true],
  ["how do i fix a flat tire", ""], ["why does meth not work like it used to", ""], ["what might someone have been spiked with", ""], ["is it legal", "which"], ["hello", ""], ["what are the side effects of", "ends"],
  // (2.9.2) a subject and nothing said of it; a helper verb and no main verb; and the questions that only look like these
  ["do gay people", "open"], ["can a gay man", "open"], ["why do women", "open"], ["how many people", "open"], ["are gay people", "open"], ["are people gay", ""], ["do gay people", "bare", true], ["do gay people use more drugs", ""],
  ["does smoking weed", "verb"], ["how long does the high", "verb"], ["can dogs", "verb"], ["does the government", "verb"], ["how long does withdrawal", "verb"], ["what drugs can", "verb"], ["can you digest", ""],
  ["how do i weed my garden", ""], ["can i speed up the comedown", ""], ["what happens when you do drugs", ""], ["how to do drugs", ""], ["is weed for kids", ""], ["how do i get a girlfriend", ""], ["does he like me", ""],
  ["can u die from", "ends"], ["do ppl", "open"], ["is it safe rn", "which"], ["eating before drinking lower bac", ""], ["what does cbd actually work for", ""], ["how long does gabapentin take to kick in", ""],
  ["has anyone tried this before", "which"], ["is it safe to take it before", "ends"], ["are legal highs safe", ""], ["what is cannabis (thc)", ""], ["why are people who use drugs looked down on", ""]];
// (2.9.2) every circumstance has its response: [question, the line, what its text must hold, is there a way to send it]
const CIRC = [["do gay people", "Go on.", /Finish your question and we will look\./, false], ["why do women", "Go on.", /Finish your question and we will look\./, false],
  ["how long does the high", "Go on.", /Finish your question and we will look\./, false], ["does smoking weed", "Go on.", /Finish your question about cannabis and we will look\./, false],
  ["what is blorptia javanensis", "We do not know “blorptia javanensis” as a drug.", /If it is one, send us your question and we will look into it\./, true],
  ["είναι ασφαλές το MDMA", "Pharmakon reads questions in English for now.", /Please ask in English\. Προς το παρόν διαβάζουμε ερωτήσεις μόνο στα αγγλικά\./, false],
  ["является ли кокаин опасным", "Pharmakon reads questions in English for now.", /Please ask in English\.$/, false],
  ["who are you", "This is Pharmakon Insight.", /finds the answer on this site\. No person and no chatbot replies to you\. Ask about a drug: for example, “is ketamine addictive\?” About us$/, false], ["are you an ai", "This is Pharmakon Insight.", /reads your question on your own device/, false],
  ["hello there pharmakon", "Hello.", /Ask a question about a drug and Insight will look: for example, “is ketamine addictive\?”$/, false]];
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
  // (2.9.2) the site's other sections, by country: the law, the emergency numbers, drug checking
  ["are drugs legal in greece", "law"], ["is weed legal in greece", "law"], ["is cocaine legal", "law"], ["drug laws in the uk", "law"], ["is it allowed in japan", "law"], ["can you go to jail for weed", "law"],
  ["what is the penalty for cocaine possession in spain", "law"], ["why is weed illegal", ""], ["should drugs be legal", ""], ["can cocaine cause cardiac arrest", ""], ["are legal highs safe", ""], ["does legalization increase cannabis use", ""],
  ["what is the emergency number in greece", "numbers"], ["who do i call", "numbers"], ["where can i get my drugs tested in spain", "test"], ["drug checking in germany", "test"],
  // (2.11) every place on the site can be asked for; a part of a drug's page; the meaning of a word of the glossary
  ["show me all drugs", "go"], ["where is the quiz", "go"], ["how do you check facts", "go"], ["is this site reliable", "go"], ["do you track me", "go"], ["who made this site", "go"], ["open the glossary", "go"],
  ["report a mistake please", "go"], ["what did i ask", "go"], ["where does your information come from", "go"], ["what does tolerance mean", "term"], ["what is half-life", "term"], ["define bioavailability", "term"],
  ["what does lsd look like", "part"], ["pictures of cocaine", "part"], ["cocaine risks", "part"], ["what are the side effects of kratom", "part"], ["what does lsd feel like", "part"], ["what does cocaine feel like", ""], ["what is the best way to quit smoking", ""], ["how many people use cocaine", ""],
  ["does cocaine feel different when snorted", ""], ["is cocaine dangerous for the heart", ""],
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
  if (p === "/api/ask") { res.writeHead(200, { "Content-Type": "application/json" }); res.end('{"ok":false}'); return; }   // as the site's worker answers before its store is set up (the question endpoint itself: scripts/ux/site24_check.js)
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
const JUDGE = INDEX.judge || {};
ok("the index carries the model's name, the weights, the tiers and the judge of site/insight/model.json (the judge: six numbers, a best match from judge.best; the tiers: related and near only)", MODEL === CONFIG.file && JSON.stringify(INDEX.tiers) === JSON.stringify(CONFIG.tiers) &&
  JSON.stringify(INDEX.weights) === JSON.stringify(CONFIG.weights) && JSON.stringify(INDEX.judge) === JSON.stringify(CONFIG.judge) && fs.existsSync(path.join(ROOT, "insight", MODEL)) && Object.keys(INDEX.tiers).sort().join() === "near,related" &&
  ["features", "mu", "sd", "w"].every(k => Array.isArray(JUDGE[k]) && JUDGE[k].length === 6) && typeof JUDGE.b === "number" && JUDGE.best > 0 && JUDGE.best < 1,
  MODEL + "; tiers " + JSON.stringify(INDEX.tiers) + "; a best match from " + JUDGE.best + "; the judge weighs " + (JUDGE.features || []).map((f, i) => f + " " + JUDGE.w[i].toFixed(2)).join(", "));
// the judge's number, worked out here from the six numbers the page reports and the index's numbers
const judged = f => 1 / (1 + Math.exp(-(f.reduce((z, x, i) => z + JUDGE.w[i] * (x - JUDGE.mu[i]) / JUDGE.sd[i], JUDGE.b))));
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
    const set = await p.evaluate(() => ({ tiers: pkInsight.tiers(), weights: pkInsight.weights(), judge: pkInsight.judge() }));
    ok(w + ": the page's weights, tiers and judge are those of data/insight.json", JSON.stringify(set.tiers) === JSON.stringify(INDEX.tiers) && JSON.stringify(set.weights) === JSON.stringify(INDEX.weights) && JSON.stringify(set.judge) === JSON.stringify(INDEX.judge), JSON.stringify(set.tiers) + ", best match from " + set.judge.best);
    // the judge decides, with the index's numbers: its number is the formula on the six numbers of the first answer, and that answer is the best match exactly when it is about the drugs named and the number is judge.best or more
    const jq = REAL.map(x => [x[0], null]).concat([[ECSTASY[0], null], [UNCHECKED, null], [LISTED, null], [KETAMINE, null], [MIX, null], ["is it addictive", "cannabis"], ["does it kill brain cells", "cannabis"], ["is lsd addictive", null], ["does weed make you lazy", null]]);
    const jr = await p.evaluate(async qs => { const out = []; for (const [q, drug] of qs) { const r = await pkInsight.rank(q, drug ? { drug } : {}); out.push({ judge: r.judge, best: r.best.map(x => x.id), off: r.best.concat(r.related).filter(x => x.id === r.judge.id).map(x => x.off)[0] }); } return out; }, jq);
    const jbad = jq.map(([q, drug], i) => { const r = jr[i], pj = judged(r.judge.f), is = r.best.length === 1 && r.best[0] === r.judge.id;
      return Math.abs(pj - r.judge.p) < 1e-9 && r.best.length <= 1 && (is ? r.judge.p >= JUDGE.best : (r.judge.p < JUDGE.best || r.off !== false)) ? null : "“" + q + "”" + (drug ? " on " + drug : "") + ": page " + r.judge.p + ", here " + pj + ", best " + r.best; }).filter(Boolean);
    ok(w + ": the judge's number in the page is the index's formula on the six numbers of the first answer, and it alone decides the best match (" + jq.length + " questions)", !jbad.length && jr.some(r => r.best.length) && jr.some(r => !r.best.length),
      jbad.slice(0, 2).join("; ") || jq.map(([q], i) => "“" + q + "” " + jr[i].judge.p.toFixed(2) + (jr[i].best.length ? " best" : "")).join("; "));

    // ---- honest tiers
    let Q0 = "", K0 = "";   // the first question's answer as the list shows it: its checked question and its page
    for (const [q, want] of REAL) {
      const r = await ask(q); ui += " " + await uiText();
      if (q === REAL[0][0]) await shot("list-matched");
      const b = r.best[0] || {}; if (q === REAL[0][0]) { Q0 = b.q || ""; K0 = b.k || ""; }
      ok(w + ": “" + q + "” has its answer as best match, the short answer in full in the list, with its rating", r.open && r.first === "sr-note" && r.kids[0] === "h:Best match" && b.id === want && b.whole && b.bars && r.best.length === 1 && r.related.length <= 3 && !r.none && !r.wordBest && /^Best match: /.test(r.live),
        (b.id ? b.k + ": " + b.q + " / " + b.a : "no best match") + "; related " + r.related.length + "; heard: " + r.live);
    }
    { const r = await ask(ECSTASY[0]), b = r.best[0], first = b || r.related[0] || {};
      ok(w + ": “" + ECSTASY[0] + "” puts its answer first: as the best match with the short answer in full, or, when the judge is not sure, first under Related after the honest line", first.id === ECSTASY[1] && first.k === "MDMA" && r.best.length <= 1 &&
        (b ? b.whole && r.kids[0] === "h:Best match" && !r.none : r.none === "We haven’t checked exactly this yet." && r.kids[0] === "none" && r.kids[1] === "h:Related"),
        (b ? "BEST MATCH" : "NOT a best match (first under Related; the judge is not sure)") + ": " + first.k + ": " + first.q + "; " + r.kids.join(" > ")); }
    const al = await ask(UNCHECKED); ui += " " + await uiText(); await shot("list-unmatched");
    ok(w + ": “" + UNCHECKED + "” says “We haven’t checked exactly this yet” with “Ask us to check it”, no best match; a near answer shows under Related at most", al.kids[0] === "none" && !al.best.length && al.none === "We haven’t checked exactly this yet." && al.askBtn === "Ask us to check it" && al.kids.indexOf("h:Related") === 1 &&
      al.related.length >= 1 && al.related.length <= 3 && !al.kids.includes("h:Best match") && !al.wordBest && /^We haven’t checked exactly this yet/.test(al.live), al.kids.join(" > ") + "; related: " + al.related.map(x => x.k + ": " + x.q).join("; ") + "; heard: " + al.live);
    // (2.5) a question on our list: "Not answered yet. A question like yours is on our list", with the listed question in our words; here the site's
    // store is off, so nothing is counted and the card does not say that it is
    const li = await ask(LISTED); ui += " " + await uiText(); await shot("list-on-our-list");
    const liMore = await p.evaluate(() => { const c = document.querySelector("#search-results .sr-want"); return c ? { q: (c.querySelector(".want-q") || {}).textContent || "", id: c.dataset.want, count: c.hasAttribute("data-count"), note: !!c.querySelector(".want-n"), other: (c.querySelector(".want-other") || {}).textContent || "", link: (c.querySelector('a[href="#wanted"]') || {}).textContent || "" } : null; });
    ok(w + ": a question on our list (“" + LISTED + "”) says “Not answered yet. A question like yours is on our list” with the listed question, “Tell me when it is answered” and the way to send one's own words; nothing says it is counted while the store is off",
      li.kids[0] === "none" && !li.best.length && li.none === "Not answered yet." && li.askBtn === "Tell me when it is answered" && liMore && liMore.q === "How can you die from alcohol?" && /^w_\d+$/.test(liMore.id) && !liMore.count && !liMore.note &&
        liMore.other === "Not the same? Send yours to us" && liMore.link === "on our list" && !li.wordAsk && /^Not answered yet\. A question like yours is on our list: How can you die from alcohol\?/.test(li.live), li.kids.join(" > ") + " | " + JSON.stringify(liMore) + " | heard: " + li.live);
    await p.waitForTimeout(3000);
    ok(w + ": with the store off, a listed question is not counted (no request to api/want)", !sent.some(x => /api\/want/.test(x)), sent.filter(x => /api\/want/.test(x)).join(" | ") || "none");
    const no = await ask(NONE); ui += " " + await uiText(); await shot("list-not-about-drugs");
    ok(w + ": a question that is not about drugs (“" + NONE + "”) is told what the page read, with no promise to check it: “This does not look like a question about drugs. Pharmakon answers questions about drugs”, and a quiet way to send it all the same, which carries the words typed",
      !no.best.length && !no.related.length && no.kids.join() === "none" && no.none === "This does not look like a question about drugs." && no.askBtn === "send it to us" && /Pharmakon answers questions about drugs\. If yours is about one, name the drug, or send it to us\./.test(no.text.replace(/\s+/g, " ")) && !no.wordAsk &&
        /^This does not look like a question about drugs/.test(no.live), no.kids.join(" > ") + " | " + no.text.replace(/\s+/g, " ") + " | heard: " + no.live);
    await p.click("#search-results .sr-fit-none button"); await p.waitForTimeout(400);
    const pn = await p.evaluate(() => ({ open: document.getElementById("report").classList.contains("open"), msg: document.getElementById("report-message").value, mode: (document.querySelector('.fb-opt[aria-pressed="true"]') || { dataset: {} }).dataset.mode }));
    ok(w + ": its “send it to us” opens Ask a question with the words typed (the store is off here)", pn.open && pn.msg === NONE && pn.mode === "feedback", JSON.stringify(pn));
    await p.keyboard.press("Escape"); await p.waitForTimeout(200);
    // ---- (2.9) a question that is not finished gets no verdict and no way to send it: which drug is meant, or go on
    const un = await ask(UNFIN); ui += " " + await uiText(); await shot("list-unfinished");
    ok(w + ": a question that is not finished (“" + UNFIN + "”) gets no verdict: “Which drug do you mean? Finish your question with its name and we will look.”, nothing to send, no best match, and what was found stands under “You may mean”",
      !un.best.length && un.kids[0] === "none" && un.none === "Which drug do you mean?" && !un.askBtn && !un.wordAsk && /Which drug do you mean\? Finish your question with its name and we will look\./.test(un.text.replace(/\s+/g, " ")) &&
        un.related.length >= 1 && un.kids.includes("h:You may mean") && !un.kids.includes("h:Related") && !un.kids.includes("h:Best match") && /^Which drug do you mean\? Finish your question with its name and we will look/.test(un.live),
      un.kids.join(" > ") + " | " + un.text.replace(/\s+/g, " ").slice(0, 160) + " | heard: " + un.live);
    const unS = await enter(); await shot("sheet-unfinished");
    ok(w + ": Enter on it says the same in the sheet, with nothing to send", unS && unS.none === "Which drug do you mean?" && !unS.askBtn && !unS.ones.length && !unS.guess &&
      await p.evaluate(() => /Finish your question with its name and we will look\./.test((document.querySelector("#evsheet .ins-unfin") || {}).textContent || "") && (!document.querySelector("#evsheet .ins-rel") || document.querySelector("#evsheet .ins-rel .rn-k").textContent === "You may mean")), unS ? unS.none + " | " + unS.askBtn : "no sheet");
    await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    const un2 = await ask(UNFIN_DRUG);
    ok(w + ": the same with a drug named (“" + UNFIN_DRUG + "”): “Go on. Finish your question about cocaine and we will look.”, nothing to send", !un2.best.length && un2.none === "Go on." && !un2.askBtn && !un2.wordAsk &&
      /Go on\. Finish your question about cocaine and we will look\./.test(un2.text.replace(/\s+/g, " ")), un2.kids.join(" > ") + " | " + un2.text.replace(/\s+/g, " ").slice(0, 160));
    const unk = await ask(STRANGER);
    ok(w + ": a question whose one unknown word may be a drug's name (“" + STRANGER + "”): “We do not know “tusi” as a drug. If it is one, send us your question and we will look into it.”", !unk.best.length && unk.none === "We do not know “tusi” as a drug." && unk.askBtn === "send us your question" &&
      /If it is one, send us your question and we will look into it\./.test(unk.text.replace(/\s+/g, " ")) && /^We do not know “tusi” as a drug/.test(unk.live), unk.kids.join(" > ") + " | " + unk.text.replace(/\s+/g, " ").slice(0, 200) + " | heard: " + unk.live);
    // ---- (2.9.2) every circumstance has its response: a subject with nothing said of it, a helper with no main verb, a name
    // of two words that we do not know, a question that is not in English
    const cbad = [];
    for (const [q, line, re, send] of CIRC) { const r = await ask(q);
      if (!(r.none === line && re.test(r.text.replace(/\s+/g, " ").trim()) && !!r.askBtn === send && !r.best.length && !r.wordAsk)) cbad.push("“" + q + "”: " + r.none + " | " + r.text.replace(/\s+/g, " ").slice(0, 150) + " | send: " + r.askBtn); }
    await shot("list-go-on");
    // (2.9.3) a name the system learned by looking it up: what people typed for it is read as the name (when the table holds it)
    let learned = {}; try { learned = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "..", "data", "auto", "names", "learned.json"), "utf8")).names || {}; } catch (e) { learned = {}; }
    const lk = Object.keys(learned).find(k => learned[k].drug === true && (learned[k].typed || []).length);
    if (lk) { const typed = learned[lk].typed[0], r = await ask("what is " + typed), rd = await p.evaluate(() => (document.querySelector("#search-results .sr-fit .sr-read") || {}).textContent || "");
      // (2.12: when a page our system started lists this very question, the line is "Not answered yet.": it is on our list)
      ok(w + ": a name the system learned by looking it up: “what is " + typed + "” is read as " + learned[lk].name + ", and is a question about drugs", rd === "We read “" + typed + "” as " + learned[lk].name + "." && (r.none === "We haven’t checked exactly this yet." || r.none === "Not answered yet."), rd + " | " + r.none); }
    // (2.13; the senior author asked "how can i use test kits at home" and was told "We haven't checked exactly this yet") a place of the site
    // is found by the meaning of a question, not only by patterns of words; a drug test of the body is not drug checking; a question about
    // the site itself is led to its place and is not called "not about drugs"
    { const k1 = await ask("how can i use test kits at home");
      ok(w + ": “how can i use test kits at home” is led to the part on test kits to use at home, first, and nothing says “we haven't checked”",
        k1.routes.length >= 1 && k1.routes[0].kind === "go" && k1.routes[0].href === "#checking/part-c-kits" && /^Test kits to use at home/.test(k1.routes[0].t) && !k1.none && k1.kids[0] === "route:go", JSON.stringify(k1.routes) + " | " + k1.none + " | " + k1.kids.join(","));
      const k2 = await ask("does weed show up on a drug test");
      ok(w + ": “does weed show up on a drug test” is not led to drug checking (a test of the body is not a test of a drug)", !k2.routes.some(r => /^#checking/.test(r.href)), JSON.stringify(k2.routes));
      const k3 = await ask("is my search private");
      ok(w + ": “is my search private” is led to the part on privacy and is not called “not about drugs”", k3.routes.length === 1 && k3.routes[0].href === "#about/part-a-privacy" && !k3.none, JSON.stringify(k3.routes) + " | " + k3.none); }
    // (2.13; "How many people die from methamphetamine": the rows under "More results" were "completely irrelevant ... visual clutter") an
    // answer the word search found by a word in common stays under Insight's block only when it is near the question in meaning
    { const m1 = await ask("how many people die from methamphetamine");
      const left = await p.evaluate(async () => { const r = await insAnswer("how many people die from methamphetamine", insCtx()); return [...document.querySelectorAll("#search-results > a.sr-ans[data-cid]")].map(a => [a.querySelector(".t").textContent.slice(0, 60), +r.sc.topic[INS.idx.get(a.dataset.cid)].toFixed(2)]); });
      ok(w + ": “how many people die from methamphetamine” gets its answer, and no answer about something else that only shares a word (“people”, “meth”) stands under “More results”",
        m1.best.length === 1 && m1.best[0].id === "cl_meth_mortality" && left.every(x => x[1] >= 0.4) && !left.some(x => /cash|dopamine|grey matter/.test(x[0])), JSON.stringify(m1.best.map(b => b.id)) + " | " + JSON.stringify(left)); }
    // (2.14; the senior author asked "How many people die from heroin", was told "We haven't checked exactly this yet" and found the statistics
    // page "irrelevant": "this is such a simple question") a question that asks for a count is answered from the official figures the site holds
    { const f1 = await ask("how many people die from heroin"), r1 = f1.routes[0] || {};
      ok(w + ": “how many people die from heroin” is answered with the official figure, first, with its place, year and source, and nothing says “we haven't checked”",
        r1.kind === "figure" && r1.k === "Statistics · Heroin · Deaths" && /^[\d,.]+(?: deaths)?: .*heroin/i.test(r1.t) && /^#numbers\/part-n-/.test(r1.href) && !f1.none && f1.kids[0] === "route:figure" &&
          await p.evaluate(() => /\d{4}/.test((document.querySelector('#search-results a.sr-route[data-ins-route="figure"] .rm') || {}).textContent || "")), JSON.stringify(f1.routes) + " | " + f1.none);
      const f2 = await ask("heroin deaths");
      ok(w + ": “heroin deaths”, two words, gets the same figure", (f2.routes[0] || {}).kind === "figure" && (f2.routes[0] || {}).t === r1.t, JSON.stringify(f2.routes));
      // (2.16.1; the senior author asked "how many heroin deaths in america" and was shown the EU's figure as the answer: "the ai should understand what i mean!")
      const f5 = await ask("how many heroin deaths in america"), h5 = await p.evaluate(() => [...document.querySelectorAll("#search-results .sr-fit > *")].map(e => e.matches(".sr-fit-none") ? "none" : e.matches(".sr-fit-h") ? "h:" + e.textContent : e.matches("a.sr-route") ? "route:" + (e.classList.contains("sr-way") ? "way" : "answer") : e.matches("a") ? "row" : ""));
      ok(w + ": “how many heroin deaths in america” is not answered with the EU's figure: the page says it has no checked figure for the United States, and the EU's stands under “Figures we do have”",
        /^We have no checked figure on this for the United States yet\./.test(f5.none) && f5.routes.length === 1 && f5.routes[0].kind === "figure" && /in the EU/.test(f5.routes[0].t) && h5.indexOf("none") >= 0 && h5.indexOf("h:Figures we do have") === h5.indexOf("none") + 1 && h5[h5.indexOf("none") + 2] === "route:way" && !h5.includes("route:answer"), JSON.stringify(f5.routes) + " | " + f5.none + " | " + h5.join(","));
      const f6 = await p.evaluate(async () => { const out = {}; for (const q of ["us heroin deaths", "how many of us use heroin", "heroin deaths in the us", "how many americans use heroin", "how many people use cocaine in greece", "how many people use cocaine in germany", "how many heroin deaths in europe", "how many people use cannabis worldwide"]) { const r = await pkInsight.rank(q, {}); out[q] = [r.note || "", r.routes.filter(x => x.kind === "figure").map(x => x.t).join(" / ")]; } return out; });
      ok(w + ": the place a count names is read (“in the us”, “americans”, “in greece”, “in europe”, “worldwide”): its own figure where the site has one, the plain truth where it has none",
        f6["us heroin deaths"][0] === "none" && f6["how many of us use heroin"][0] === "" && !/United States/.test(f6["how many of us use heroin"][1]) && f6["heroin deaths in the us"][0] === "none" && /in the EU/.test(f6["heroin deaths in the us"][1]) && f6["how many americans use heroin"][0] === "" && /^556,000/.test(f6["how many americans use heroin"][1]) && f6["how many people use cocaine in greece"][0] === "" && /cocaine/.test(f6["how many people use cocaine in greece"][1]) &&
          f6["how many people use cocaine in germany"][0] === "none" && f6["how many heroin deaths in europe"][0] === "" && /in the EU/.test(f6["how many heroin deaths in europe"][1]) && f6["how many people use cannabis worldwide"][0] === "" && /worldwide/.test(f6["how many people use cannabis worldwide"][1]), JSON.stringify(f6));
      const f3 = await ask("how many mg of mdma do people take");
      ok(w + ": “how many mg of mdma do people take” asks for an amount, not a count of people: no figure, the line on doses", !f3.routes.some(r => r.kind === "figure") && f3.routes.some(r => r.kind === "dose"), JSON.stringify(f3.routes));
      await ask("how many people die from heroin"); await p.click('#search-results a.sr-route[data-ins-route="figure"]'); await p.waitForTimeout(1500);
      const arr = await p.evaluate(() => { const g = location.hash.replace("#numbers/part-n-", "").replace(/\/f-.*$/, ""), sel = document.getElementById("num-sub-" + g), a = document.activeElement; return { hash: location.hash, sub: sel ? sel.value : "", at: a ? a.textContent.slice(0, 20) : "", view: document.getElementById("view-numbers").classList.contains("active") }; });
      ok(w + ": its row opens the statistics page at that place, with that drug's figures chosen, at “Deaths”", arr.view && /^#numbers\/part-n-[a-z]+\/f-death-heroin$/.test(arr.hash) && arr.sub === "heroin" && /^Deaths/.test(arr.at), JSON.stringify(arr));
      // (2.15.3) the address alone does the same (the senior author opened the answer from “Your questions” and stood before every drug's figures, at the top)
      await p.goto(BASE + "home"); await p.waitForTimeout(300); await p.goto(BASE + arr.hash.slice(1)); await p.waitForTimeout(1600);
      const arr2 = await p.evaluate(() => { const g = location.hash.replace("#numbers/part-n-", "").replace(/\/f-.*$/, ""), sel = document.getElementById("num-sub-" + g), a = document.activeElement; return { sub: sel ? sel.value : "", at: a ? a.textContent.slice(0, 20) : "" }; });
      ok(w + ": a figure's own address opens the same place, drug and kind, however it is reached", arr2.sub === "heroin" && /^Deaths/.test(arr2.at), JSON.stringify(arr2));
      await p.evaluate(() => { location.hash = "#home"; }); await p.waitForTimeout(600); }
    // (2.12) a page our system started (people asked about a drug that had no page): a question that names it is shown the way to that
    // page and is never called "not about drugs"; its name alone finds the page; asked what it looks like, its pictures are the answer.
    // The check goes by the pages the build shows today, whatever they are.
    { const sp = await p.evaluate(() => { if (typeof AUTO_NAMES !== "object" || !AUTO_NAMES) return null;
        const n = Object.keys(AUTO_NAMES).filter(x => /^[a-z]{5,}$/.test(x)).sort((a, b) => ((AUTO_PICS[AUTO_NAMES[b]] || []).length - (AUTO_PICS[AUTO_NAMES[a]] || []).length) || a.localeCompare(b))[0];
        return n ? { n, k: AUTO_NAMES[n], pics: (AUTO_PICS[AUTO_NAMES[n]] || []).length, parts: ((AUTO_PICS[AUTO_NAMES[n]] || []).length ? 1 : 0) + (AUTO_SHELL[AUTO_NAMES[n]] && AUTO_SHELL[AUTO_NAMES[n]].asked.length ? 1 : 0) + (Object.keys(AUTO).some(id => AUTO[id].page === "new:" + AUTO_NAMES[n]) ? 1 : 0) } : null; });
      if (!sp) ok(w + ": (no page our system started is shown today: nothing to ask about one)", true);
      else {
        const r1 = await ask("can people get addicted to " + sp.n), rt1 = r1.routes.find(x => x.href === "#auto/p-" + sp.k);
        ok(w + ": a question that names a drug of a page our system started (“can people get addicted to " + sp.n + "”) is shown the way to that page, is not called “not about drugs”, and is not shown answers about other drugs",
          !!rt1 && rt1.kind === "page" && rt1.k === "A page our system started" && !/does not look like a question about drugs|as a drug/.test(r1.none) && !r1.best.length && await p.evaluate(() => !document.querySelector("#search-results > a.sr-ans")), JSON.stringify(r1.routes) + " | " + r1.none);
        typed.push(sp.n); await p.fill("#search", sp.n); await p.waitForTimeout(700);
        const r2 = await p.evaluate(k => ({ row: !!document.querySelector('#search-results a[href="#auto/p-' + k + '"]'), unfin: !!document.querySelector("#search-results .sr-unfin"), none: !!document.querySelector("#search-results > .none") }), sp.k);
        ok(w + ": its name alone (“" + sp.n + "”) finds the page, with no “finish your question” and no “no match”", r2.row && !r2.unfin && !r2.none, JSON.stringify(r2));
        if (sp.pics) { const r3 = await ask("what does " + sp.n + " look like"), rt3 = r3.routes[0];
          ok(w + ": “what does " + sp.n + " look like” goes to its pictures, says that our system found them and that no person has checked them, and nothing says “we haven't checked”",
            !!rt3 && rt3.kind === "page" && rt3.href === "#auto/p-" + sp.k + (sp.parts > 1 ? "/part-p-looks" : "") && /our system found, not yet checked by a person$/.test(rt3.t) && !r3.none, JSON.stringify(r3.routes) + " | " + r3.none); }
      } }
    ok(w + ": every circumstance has its response (" + CIRC.length + " questions: “do gay people” and “why do women” are told “Go on. Finish your question and we will look.” with nothing to send; a name of two words we do not know is named; a question in Greek or Russian is asked for in English)", !cbad.length, cbad.slice(0, 3).join(" ;; ") || "all as they should be");
    // the law by country: the route is the answer, from the page of treaties; with a drug named, from that drug's law part, shown for the country asked about
    const lw = await ask("are drugs legal in greece"); await shot("list-law-country");
    ok(w + ": “are drugs legal in greece” goes to Greece on the page of treaties: the route says what Greece has joined, nothing says “we haven't checked”, nothing to send",
      lw.routes.length === 1 && lw.routes[0].kind === "law" && lw.routes[0].href === "#law/c-Greece" && /^Greece has joined all three UN drug treaties\. Its own law on each drug is on that drug’s page$/.test(lw.routes[0].t) && !lw.none && !lw.askBtn,
      JSON.stringify(lw.routes) + " | " + lw.none + " | " + lw.askBtn);
    const lw2 = await ask("is weed legal in greece");
    const lw2ok = lw2.routes.length >= 1 && lw2.routes[0].kind === "law" && lw2.routes[0].href === "#s-cannabis/part-d-law" && /Greece/.test(lw2.routes[0].t) && !/^What the law of/.test(lw2.routes[0].t) && !lw2.none;
    await p.click('#search-results a.sr-route[data-ins-route="law"]'); await p.waitForTimeout(900);
    const lawPart = await p.evaluate(() => { const b = document.querySelector("#drug2 #d-law .sec-b"); let own = null; try { own = localStorage.getItem("pk-country"); } catch (e) { own = "?"; }
      return { hash: location.hash, where: b ? (b.querySelector(".cq-where") || {}).textContent || "" : "", asked: b ? (b.querySelector(".cq-asked") || {}).textContent || "" : "", say: b ? (b.querySelector(".say") || {}).textContent || "" : "", own }; });
    ok(w + ": “is weed legal in greece”: the route says what the law of Greece says about cannabis, and opens cannabis' law part for Greece, “The country you asked about”, without changing the reader's own country",
      lw2ok && lawPart.hash === "#s-cannabis/part-d-law" && lawPart.where === "Greece" && lawPart.asked === "The country you asked about" && /Greece/.test(lawPart.say) && lawPart.own === null, JSON.stringify(lw2.routes).slice(0, 260) + " | " + JSON.stringify(lawPart));
    await p.goto(BASE + "home"); await p.waitForTimeout(300);
    const lw3 = await ask("can you go to jail for weed");
    ok(w + ": a question of the law that the law part does not answer by itself (“can you go to jail for weed”) gets the route and keeps the line and the way to send it", lw3.routes.some(r => r.kind === "law") && lw3.none === "We haven’t checked exactly this yet." && !!lw3.askBtn, JSON.stringify(lw3.routes) + " | " + lw3.none + " | " + lw3.askBtn);
    const nm = await ask("what is the emergency number in greece");
    ok(w + ": “what is the emergency number in greece”: the route says the number and opens Greece on the emergency page", nm.routes.length === 1 && nm.routes[0].kind === "numbers" && nm.routes[0].href === "#emergency/c-Greece" && nm.routes[0].t === "In Greece, call 112" && !nm.none, JSON.stringify(nm.routes));
    // an entry of one or two words that is a beginning: told to go on, in place of "No match … Ask us"
    await p.fill("#search", "can i"); await p.waitForTimeout(500);
    const sh = await p.evaluate(() => { const b = document.getElementById("search-results"); return { unf: (b.querySelector(".sr-fit .sr-unfin") || {}).textContent || "", ask: !!b.querySelector(".sr-ask, button[data-ask]"), none: !!b.querySelector(":scope > .none"), live: document.getElementById("search-count").textContent }; });
    ok(w + ": two words that are a beginning (“can i”) are told “Go on. Finish your question and we will look.”, with no “No match” and nothing to send", sh.unf === "Go on. Finish your question and we will look." && !sh.ask && !sh.none && sh.live === sh.unf, JSON.stringify(sh));
    // a question the reader already sent, opened again: it says so, and offers no second way to send it
    const keptWas = await p.evaluate(q => { const was = localStorage.getItem("pk-asked"), list = JSON.parse(was || "[]"); list.push({ k: q, q, d: "", t: Date.now(), cv: "x", st: "wait", sent: 1 }); localStorage.setItem("pk-asked", JSON.stringify(list)); return was; }, UNCHECKED);
    await p.fill("#search", ""); const st = await ask(UNCHECKED);
    ok(w + ": a question already sent (“" + UNCHECKED + "”), opened again, says “You sent us this question. No answer yet …” and offers no second way to send it", st.none === "You sent us this question." && !st.askBtn && /No answer yet\. It turns green under “Your questions” on the start page when there is one\./.test(st.text.replace(/\s+/g, " ")), st.none + " | " + st.text.replace(/\s+/g, " ").slice(0, 200));
    await p.evaluate(was => { if (was === null) localStorage.removeItem("pk-asked"); else localStorage.setItem("pk-asked", was); }, keptWas);
    // ---- (2.10) the first screen is Insight: its name, the capsule, and things to try; pressing one asks it
    await p.fill("#search", ""); await p.goto(BASE + "home"); await p.evaluate(() => { document.getElementById("search").blur(); closeSearch(); }); await p.waitForTimeout(300);   // (at rest: the answers are closed, the things to try are in view)
    const hero = await p.evaluate(() => { const h = document.getElementById("insight-hero"), s = document.getElementById("search"), cap = document.querySelector("#home-search .sicon"), r = s.getBoundingClientRect(), c = cap.getBoundingClientRect();
      return { mark: (h.querySelector(".ins-mark") || {}).textContent || "", markLogo: !!h.querySelector(".ins-mark svg"), h1: (h.querySelector("h1") || {}).textContent || "", inHero: !!h.querySelector("#search"), tall: r.height, cap: c.width, capBg: getComputedStyle(cap).backgroundColor, bg: getComputedStyle(s).backgroundColor,
        tries: [...h.querySelectorAll(".ins-try button")].filter(b => b.offsetParent).map(b => b.dataset.try), pill: !!cap.querySelector(".ic-pill") && getComputedStyle(cap.querySelector(".ic-pill")).display !== "none" && getComputedStyle(cap.querySelector(".ic")).display === "none" }; });
    await shot("hero");
    ok(w + ": the first screen is Insight: its name by its own word alone (the bar above already says Pharmakon, with the mark: 2.16.1), the question, and the box as a capsule (a coloured cap with the site's mark, at least 56px tall), and no example questions under it (2.15.3, at the senior author's word)",
      hero.mark.replace(/\s+/g, " ").trim() === "Insight" && !hero.markLogo && hero.h1 === "What do you want to know?" && hero.inHero && hero.tall >= 56 && hero.cap >= 56 && hero.capBg !== hero.bg && hero.pill && hero.tries.length === 0, JSON.stringify(hero));
    await p.fill("#search", "are drugs legal in greece"); await p.waitForTimeout(1700);
    const tried = await snap();
    ok(w + ": pressing a thing to try asks it: “are drugs legal in greece” is in the box and its answer is shown", tried.value === "are drugs legal in greece" && tried.open && tried.routes.length === 1 && tried.routes[0].kind === "law", tried.value + " | " + JSON.stringify(tried.routes));
    // (2.9.1) a drug's name with a letter wrong is read as the name, and the page says what it read
    const sp = await ask(MISSPELT); await shot("list-misspelt");
    const spRead = await p.evaluate(() => (document.querySelector("#search-results .sr-fit .sr-read") || {}).textContent || "");
    ok(w + ": a drug's name with a letter wrong (“" + MISSPELT + "”) is read as the name and the page says so: “We read “cocane” as cocaine.”; what it shows is about cocaine",
      spRead === "We read “cocane” as cocaine." && sp.kids[0] === "sr-read" && sp.best.concat(sp.related).length >= 1 && sp.best.concat(sp.related).every(x => /cocaine|mix/i.test(x.k + " " + x.q)) && /^We read cocane as cocaine/.test(sp.live),
      spRead + " | " + sp.kids.join(" > ") + " | " + sp.best.concat(sp.related).map(x => x.k + ": " + x.q).join(" / ").slice(0, 200) + " | heard: " + sp.live.slice(0, 80));
    const spS = await enter();
    ok(w + ": Enter on it: the sheet keeps the words as typed in its heading and says what it read", spS && /cocane/i.test(spS.title) && await p.evaluate(() => (document.querySelector("#evsheet .ins-read") || {}).textContent === "We read “cocane” as cocaine."), spS ? spS.title : "no sheet");
    await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    const words = await p.evaluate(Q => Q.map(([q, on]) => pkInsight.unfinished(q, on)), WORDS.map(x => [x[0], !!x[2]]));
    const wbad = WORDS.map(([q, want, on], i) => words[i] === want ? null : "“" + q + "”" + (on ? " on a drug's page" : "") + " read as [" + words[i] + "], not [" + want + "]").filter(Boolean);
    ok(w + ": finished or not, by the words alone: " + WORDS.length + " questions each read as it should be", !wbad.length, wbad.slice(0, 4).join("; ") || WORDS.filter(x => x[1]).length + " not finished, " + WORDS.filter(x => !x[1]).length + " finished");

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
    ok(w + ": Enter on a dose question goes to that drug's Doses block (which lists no dose of ours)", dose.hash === "#s-mdma/part-d-doses" && !dose.sheet && dose.top !== null && dose.top >= 0 && dose.top < H * 0.6 && /We don’t list doses/.test(dose.text) && !AMOUNT.test(dose.text) && dose.search === "", JSON.stringify(dose));
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
    const kit = await p.evaluate(() => { const el = document.querySelector("#d-kits:not([hidden])"), r = el ? el.getBoundingClientRect() : null; return { hash: location.hash, top: r ? Math.round(r.top) : null }; });
    ok(w + ": “" + TEST + "” shows the test kits row first, and it opens that drug's test kits", ts.kids[0] === "route:test" && ts.routes[0].t === "Test kits for MDMA" && kit.hash === "#s-mdma/part-d-kits" && kit.top !== null && kit.top >= 0 && kit.top < H * 0.6, ts.kids.join(" > ") + "; " + JSON.stringify(kit));
    await p.goto(BASE + "home"); await p.waitForTimeout(500); await p.focus("#search"); await whenReady();
    const wk = await ask("what is ketamine"); await p.press("#search", "Enter"); await p.waitForTimeout(900);
    const wkAt = await p.evaluate(() => ({ hash: location.hash, sheet: !!document.querySelector("#evsheet.open") }));
    ok(w + ": “what is ketamine” puts the drug's page first, and Enter goes there", wk.kids[0] === "route:page" && wk.routes[0].t === "Ketamine" && wk.routes[0].href === "#s-ketamine" && wkAt.hash === "#s-ketamine" && !wkAt.sheet, wk.kids.join(" > ") + "; " + JSON.stringify(wkAt));
    await p.goto(BASE + "home"); await p.waitForTimeout(500); await p.focus("#search"); await whenReady();
    const by = await ask(BUY); ui += " " + await uiText(); await shot("list-not-answered");
    // (the word search may still list the drug's own page; never an answer, never a way to ask us)
    const byRows = await p.evaluate(() => { const rows = [...document.querySelectorAll("#search-results > a")]; return { all: rows.length, ans: rows.filter(a => a.matches(".sr-ans")).length, pages: rows.filter(a => /^#s-[a-z0-9-]+$/.test(a.getAttribute("href") || "")).length }; });
    ok(w + ": getting drugs (“" + BUY + "”): no route, no answer, “We haven’t checked exactly this yet” without the way to ask us (the drug's own page at most)", by.kids[0] === "none" && by.kids.every(k => k === "none" || /^h:More results( \(\d+\))?$/.test(k) || /sr-words/.test(k)) && by.none === "We haven’t checked exactly this yet." && !by.askBtn && !by.best.length && !by.related.length && !by.routes.length && !by.wordAsk &&
      byRows.ans === 0 && byRows.all <= 2 && byRows.pages === byRows.all, by.kids.join(" > ") + " | " + by.text.replace(/\s+/g, " ") + " | rows under it: " + JSON.stringify(byRows));

    // ---- Enter: the sheet for the question as asked
    const kl = await ask(KETAMINE); ui += " " + await uiText(); await shot("list-full-evidence-ketamine");
    ok(w + ": “" + KETAMINE + "” gets no best match: “We haven’t checked exactly this yet” with “Ask us to check it”, related answers at most", kl.kids[0] === "none" && !kl.best.length && kl.none === "We haven’t checked exactly this yet." && kl.askBtn === "Ask us to check it" &&
      kl.related.length <= 3 && !kl.kids.includes("h:Best match") && !kl.wordBest && /^We haven’t checked exactly this yet/.test(kl.live), kl.kids.join(" > ") + "; related: " + (kl.related.map(x => x.k + ": " + x.q).join("; ") || "none"));
    const ks = await enter(); ui += " " + await uiText(); await shot("sheet-after-enter-full-evidence");
    ok(w + ": “" + KETAMINE + "” + Enter opens a sheet headed with those words (depth words understood), with no guess step: the honest line, “Ask us to check it”, the related questions as links",
      ks && ks.title === "Give me the full evidence about how can i die from ketamine" && !ks.guess && /ins-full/.test(ks.cls) && /Your question/.test(ks.eye) && !ks.searchOpen && !ks.sos && !ks.ones.length &&
        ks.none === "We haven’t checked exactly this yet." && ks.askBtn === "Ask us to check it" && ks.related.length === kl.related.length && ks.related.every((id, i) => id === kl.related[i].id),
      ks ? ks.title + " | " + (ks.ones.length ? "BEST MATCH: " + ks.ones.map(o => o.q).join("; ") : "“" + ks.none + "”") + " | related " + (ks.related.join(", ") || "none") + " | people also ask " + ks.next.length : "no sheet");
    // Back puts the search back as it was
    await p.click("#evsheet .ev-back"); await p.waitForTimeout(350); const b1 = await closed();
    await enter(); await p.keyboard.press("Escape"); await p.waitForTimeout(350); const b2 = await closed();
    await enter(); await p.goBack(); await p.waitForTimeout(350); const b3 = await closed();
    ok(w + ": Back, Escape and the browser's Back close the sheet and put the search back as it was: the question in the box, its answers under it", [b1, b2, b3].every(b => !b.sheet && b.value === KETAMINE && b.open && b.fit === KETAMINE && b.hash === "#home"), [b1, b2, b3].map(b => JSON.stringify(b)).join(" / "));
    // the full evidence was asked for: a related answer opened from that sheet opens with "How do we know?" open
    const closeSheet = async () => { for (let i = 0; i < 3 && await p.$("#evsheet.open"); i++) { await p.keyboard.press("Escape"); await p.waitForTimeout(300); } };
    if (kl.related.length) { await enter(); await p.click("#evsheet .ins-rel a >> nth=0"); await p.waitForTimeout(350); const kr = await sheet(); await shot("sheet-related-answer-full-evidence");
      ok(w + ": a related answer opened from that sheet opens with “How do we know?” open (the full evidence was asked for), with no guess step", kr && kr.single && kr.single.how === true && kr.single.short && kr.single.ev && !kr.guess && !kr.sos,
        kr ? kr.title + " | How do we know? " + (kr.single && kr.single.how ? "open" : "closed") : "no sheet");
      await closeSheet(); }
    // depth on a question that has a best match; and the short of it
    const cap = t => t.charAt(0).toUpperCase() + t.slice(1);
    await ask(REAL[0][0] + ", with sources"); const fs1 = await enter(); await shot("sheet-after-enter-with-sources");
    ok(w + ": “" + REAL[0][0] + ", with sources” opens the best match with “How do we know?” open and the way to the evidence", fs1 && fs1.ones.length === 1 && fs1.ones[0].q === Q0 && Q0.length > 10 && fs1.ones.every(o => o.how === true && o.ev && o.short && /^Checked answer · /.test(o.label) && /^See it on the /.test(o.page)) &&
      /ins-full/.test(fs1.cls) && !fs1.guess && fs1.title === cap(REAL[0][0]) + ", with sources" && fs1.nextLabel === "People also ask" && fs1.next.length >= 1 && fs1.next.length <= 3,
      fs1 ? fs1.title + " | " + fs1.ones.map(o => o.label + ": " + o.q).join("; ") + " | people also ask " + fs1.next.length : "no sheet");
    await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    await ask(REAL[0][0] + " tl;dr"); const sh1 = await enter(); await shot("sheet-after-enter-short");
    ok(w + ": “" + REAL[0][0] + " tl;dr” shows the short answer and its But, nothing more", sh1 && sh1.ones.length === 1 && sh1.ones.every(o => o.short && o.but && o.how === null && o.bars && o.ev) && /ins-short/.test(sh1.cls) && sh1.title === cap(REAL[0][0]) + " tl;dr", sh1 ? sh1.title + " | " + JSON.stringify(sh1.ones[0]) : "no sheet");
    await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    await ask(LISTED); const ws = await enter(); await shot("sheet-on-our-list");
    const wsMore = await p.evaluate(() => { const c = document.querySelector("#evsheet .ins-want"); return c ? { q: (c.querySelector(".want-q") || {}).textContent || "", other: (c.querySelector(".want-other") || {}).textContent || "", all: (c.querySelector('a.want-all[href="#wanted"]') || {}).textContent || "", count: c.hasAttribute("data-count") } : null; });
    ok(w + ": Enter on a question on our list says so in the sheet, with the listed question, the way to send one's own words and the way to the whole list", ws && ws.title === "How can you die from alcohol" && !ws.ones.length && ws.none === "Not answered yet. A question like yours is on our list." &&
      wsMore && wsMore.q === "How can you die from alcohol?" && wsMore.other === "Not the same? Send yours to us" && /^See the whole list/.test(wsMore.all) && !wsMore.count && !ws.guess && !ws.sos, ws ? ws.none + " | " + JSON.stringify(wsMore) : "no sheet");
    // (2.17: "the user should be notified") the LISTED question is put on the reader's own list by itself, at once on Enter; nothing of the reader's is sent for it
    await p.waitForTimeout(400);
    const kept1 = await p.evaluate(() => ({ btn: !!document.querySelector("#evsheet button[data-want-keep]"), said: (document.querySelector("#evsheet .ins-want .ask-said") || {}).textContent || "", list: JSON.parse(localStorage.getItem("pk-asked") || "[]").filter(x => x.w).map(x => x.q + " / " + x.w + " / " + x.st) }));
    ok(w + ": the LISTED question (not the words typed) goes on the reader's own list by itself, as waiting, and the sheet says so in place of the button", !kept1.btn && kept1.said === "It is on your list: we will tell you on this device when it is answered." && kept1.list.length === 1 && /^How can you die from alcohol\? \/ w_\d+ \/ wait$/.test(kept1.list[0]), JSON.stringify(kept1));
    await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    await ask(NONE); const os = await enter(); await shot("sheet-not-about-drugs");
    ok(w + ": Enter on a question that is not about drugs says so calmly in the sheet, without “Ask us to check it”", os && os.title === "What is the capital of mongolia" && !os.ones.length && os.none === "This does not look like a question about drugs." && os.askBtn === "Send it to us" && !os.related.length && !os.guess && !os.sos &&
      await p.evaluate(() => /Pharmakon answers questions about drugs\. If yours is about one, name the drug, or send it to us\./.test((document.querySelector("#evsheet .ins-other") || {}).textContent || "")), os ? os.none + " | " + os.askBtn : "no sheet");
    await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    await ask(UNCHECKED); const as = await enter(); await shot("sheet-not-checked");
    ok(w + ": Enter on a drug question with no best match says so in the sheet, with “Ask us to check it” and the related questions as links", as && as.title === cap(UNCHECKED) && !as.ones.length && as.none === "We haven’t checked exactly this yet." && as.askBtn === "Ask us to check it" && as.related.length >= 1 && as.related.length <= 3 && !as.guess && !as.sos,
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
    ok(w + ": a row tapped opens that one answer at once: no guess, no emergency line; the short answer, its rating, the evidence, the way to its page, and up to 3 next questions", o1 && o1.title === Q0 && !o1.guess && !o1.sos && o1.single && o1.single.short && o1.single.bars && o1.single.ev && o1.single.how === false &&
      o1.single.page.toLowerCase().startsWith("see it on the " + K0.toLowerCase() + " page") && o1.nextLabel === "People also ask" && o1.next.length >= 1 && o1.next.length <= 3 && !o1.searchOpen && !o1.moving.length, o1 ? JSON.stringify({ title: o1.title, single: o1.single, next: o1.next, moving: o1.moving }) : "no sheet");
    // (2.15.3; the senior author: "the sources should just come down and when I click on 'See the evidence' again they should hide") the evidence unfolds under the answer, in place
    await p.click("#evsheet .ins-ans a.ask-ev"); await p.waitForSelector("#evsheet .ins-ans .ask-srcs li.ev-src", { timeout: 15000 }).catch(() => {});
    const srcs = await p.evaluate(() => { const b = document.querySelector("#evsheet .ins-ans .ask-srcs"); return { n: b ? b.querySelectorAll("li.ev-src").length : 0, ins: !!document.querySelector("#evsheet .ins .ins-ans"), exp: document.querySelector("#evsheet .ins-ans a.ask-ev").getAttribute("aria-expanded"), all: b ? (b.querySelector(".ask-srcs-all a") || {}).textContent : "" }; });
    await p.click("#evsheet .ins-ans a.ask-ev"); await p.waitForTimeout(200);
    const shut = await p.evaluate(() => !document.querySelector("#evsheet .ins-ans .ask-srcs"));
    ok(w + ": “The evidence” unfolds the sources under the answer, which stays where it is; a second tap folds them away; the whole research view is one link further", srcs.n >= 1 && srcs.ins && srcs.exp === "true" && /All the scientific detail/.test(srcs.all || "") && shut, JSON.stringify([srcs, shut]));
    await p.click("#evsheet .ins-ans a.ask-ev"); await p.waitForSelector("#evsheet .ins-ans .ask-srcs-all a", { timeout: 15000 }).catch(() => {});
    await p.click("#evsheet .ins-ans .ask-srcs-all a"); await p.waitForFunction(() => document.querySelector("#evsheet.open") && !document.querySelector("#evsheet .ins") && !document.querySelector("#evsheet .loading"), null, { timeout: 15000 }).catch(() => {});
    await p.click("#evsheet .ev-back"); await p.waitForTimeout(300);
    const back = await p.evaluate(() => ({ open: !!document.querySelector("#evsheet.open"), ins: !!document.querySelector("#evsheet .ins .ins-ans"), title: (document.getElementById("ev-title") || {}).textContent }));
    ok(w + ": the whole research view opened from the answer comes back to it with Back", back.open && back.ins && back.title === Q0, JSON.stringify(back));
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
    ok(w + ": on the cannabis page the box is there and reads “Ask Insight about cannabis”; “does it kill brain cells” does not get the alcohol answer as best match (related at most, under its own drug's name)", ph1 === "Ask Insight about cannabis" && ph0 === "Ask anything about drugs" && boxSeen &&
      !bc.best.some(x => x.id === "cl_alc_brain_cells") && bc.best.every(x => x.k === "Cannabis") && (!alc || alc.k === "Alcohol") && (bc.best.length > 0 || bc.none === "We haven’t checked exactly this yet."),
      "placeholder “" + ph1 + "”; " + bc.kids.join(" > ") + "; related: " + bc.related.map(x => x.k + ": " + x.q).join("; "));
    const ad = await ask("is it addictive");
    const ad1 = ad.best[0] || ad.related[0] || {};
    ok(w + ": on the cannabis page “is it addictive” is about cannabis: the cannabis answer comes first (best match, or first under Related), and no answer about another drug is shown", ad1.id === "cl_can_dependence_how_many" && ad1.k === "Cannabis" &&
      ad.best.concat(ad.related).every(x => x.k === "Cannabis") && (ad.best.length ? ad.best[0].whole : ad.none === "We haven’t checked exactly this yet."), (ad.best.length ? "best match: " : "first under Related: ") + ad1.k + ": " + ad1.q + "; " + ad.kids.join(" > "));
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
    for (const [where, hash, box] of [["the Myth or fact? page", "quiz", "#quizpage"], ["the start page's deck", "home", "#tf"], ["a drug page's own deck", "s-cannabis/part-d-quiz", "#qz-drug"]]) {
      await p.goto(BASE + "about"); await p.waitForTimeout(200); await p.goto(BASE + hash); await p.waitForTimeout(1100);
      // (site 2.4) the start page and the Myth or fact? page share one deck, kept on the device: the card answered on one
      // is answered on the other, so the next turn starts on the next card
      if (await p.$(box + " .mf-card.flipped")) { await p.click(box + " .qz2-nb"); await p.waitForTimeout(350); }
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
    // the promise under the box: nothing typed is sent anywhere, or kept. One exception, by the reader's own press (site 2.4):
    // the question they pressed "Ask us to check it" for is kept in the list of their questions (here the store is off, so it
    // is not sent: the email form opens). The sending itself is checked in scripts/ux/site24_check.js.
    const forms = q => [q, encodeURIComponent(q), q.replace(/ /g, "+"), q.replace(/ /g, "%20")];
    const leaked = sent.filter(x => typed.some(q => forms(q).some(f => x.includes(f))));
    const kept = await p.evaluate(qs => { const all = [JSON.stringify(history.state || "")]; for (const st of [localStorage, sessionStorage]) for (let i = 0; i < st.length; i++) { if (st === localStorage && st.key(i) === "pk-asked") continue; all.push(st.getItem(st.key(i)) || ""); } return qs.filter(q => all.some(v => v.includes(q))); }, typed);
    const askedQ = await p.evaluate(() => { try { return JSON.parse(localStorage.getItem("pk-asked") || "[]").map(x => x.q); } catch (e) { return ["unreadable"]; } });
    ok(w + ": nothing typed leaves the page or is kept on the device, except the one question the reader pressed to send, kept in the reader's own list beside the listed question (the list's own words, put there by itself: 2.17) (" + new Set(typed).size + " questions, " + sent.length + " requests)", typed.length >= 15 && !leaked.length && !kept.length && askedQ.slice().sort().join("|") === [NONE, "How can you die from alcohol?"].sort().join("|"), ((leaked.concat(kept).join(" | ") || "none") + "; in the reader's list: " + askedQ.join(" | ")).slice(0, 260));
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
    // (2.16.1; "did you make insight more stupid?" ... "for a few seconds it didn't and i thought it was stupid") a whole question while Insight is getting
    // ready: one calm line, and no row found by a word in common shown as if it were the answer; a drug's name alone keeps its rows
    const wait = await p.evaluate(() => { const b = document.getElementById("search-results"); return { state: pkInsight.state(), line: (b.querySelector(":scope > .sr-wait") || {}).textContent || "", first: !!(b.firstElementChild && b.firstElementChild.matches(".sr-wait")),
      shown: [...b.querySelectorAll(":scope > a.sr-ans")].filter(a => !a.hidden).length, all: b.querySelectorAll(":scope > a.sr-ans").length, ask: !!b.querySelector(".sr-ask, .none") }; });
    await p.fill("#search", "ketamine"); await p.waitForTimeout(300);
    const name = await p.evaluate(() => { const b = document.getElementById("search-results"); return { line: !!b.querySelector(".sr-wait"), rows: [...b.querySelectorAll(":scope > a")].filter(a => !a.hidden).length }; });
    ok("1280, a whole question while Insight is getting ready: one calm line first and no row found by a word in common; a drug's name alone keeps its rows", wait.state === "loading" && wait.line === "One moment: Insight is getting ready to read your question…" && wait.first && wait.shown === 0 && wait.all > 0 && !wait.ask && !name.line && name.rows > 0, JSON.stringify(wait) + " " + JSON.stringify(name));
    await p.fill("#search", REAL[2][0]); await p.waitForTimeout(300);
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
    // (2.16.1) and it is ready before the first question: a device that fetched Insight before starts it when the page opens, with the box untouched
    await p.reload(); const warm = await p.waitForFunction(() => window.pkInsight && pkInsight.state() === "ready", null, { timeout: 120000 }).then(() => true, () => false);
    const touched = await p.evaluate(() => document.activeElement && document.activeElement.id === "search");
    ok("a device that fetched Insight before starts it when the page opens (the box untouched), so it is ready before the first question", warm && !touched, "ready " + warm + ", box focused " + touched);
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
