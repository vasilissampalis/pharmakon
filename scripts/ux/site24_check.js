// site24_check.js [--shots DIR]: what site 2.4 changed, checked on the built public site (site/public).
// The senior author's notes on 2.3.0 (15 November 2026): one top bar and one column on every page; a line that says where
// Back leads, and Back putting the page as it was; one Myth or fact deck, kept; every long page as a menu of sections,
// one open at a time; a clearer statistics page; "Ask us to check it" in one tap, with "Your questions" on the start page;
// the opioid pages speaking to a friend first; the email with the message in its subject.
// The question endpoint is the real one (site/worker/_worker.js) with a store kept in memory.
const http = require("http"), fs = require("fs"), path = require("path");
const { chromium } = require("playwright");
const ROOT = path.join(__dirname, "..", "..", "site", "public");
const SHOTS = process.argv.includes("--shots") ? process.argv[process.argv.indexOf("--shots") + 1] : null;
const TYPES = { ".html": "text/html; charset=utf-8", ".json": "application/json", ".webp": "image/webp", ".png": "image/png", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".css": "text/css", ".js": "text/javascript", ".mjs": "text/javascript", ".wasm": "application/wasm", ".txt": "text/plain; charset=utf-8", ".onnx": "application/octet-stream" };
let pass = 0, fail = 0;
const ok = (name, cond, extra) => { if (cond) { pass++; console.log("PASS " + name); } else { fail++; console.log("FAIL " + name + (extra ? " | " + String(extra).slice(0, 400) : "")); } };

(async () => {
  const worker = (await import("file://" + path.join(__dirname, "..", "..", "site", "worker", "_worker.js"))).default;
  // one server per state of the store: on (a store kept in memory) and off (no store bound: the worker answers 503)
  const serve = withStore => new Promise(resolve => {
    const kv = new Map(), store = { get: async (k, how) => { const v = kv.get(k); return v == null ? null : how === "json" ? JSON.parse(v) : v; }, put: async (k, v) => { kv.set(k, v); } };
    const env = Object.assign({ ASSETS: { fetch: async () => new Response("", { status: 404 }) } }, withStore ? { QUESTIONS: store } : {});
    const server = http.createServer(async (req, res) => {
      const p0 = decodeURIComponent(req.url.split("?")[0]);
      if (p0.startsWith("/api/")) {
        const chunks = []; for await (const c of req) chunks.push(c);
        const r = await worker.fetch(new Request("http://" + req.headers.host + req.url, { method: req.method, headers: req.headers, body: ["GET", "HEAD"].includes(req.method) ? undefined : Buffer.concat(chunks) }), env);
        res.writeHead(r.status, { "Content-Type": r.headers.get("content-type") || "application/json" }); res.end(await r.text()); return;
      }
      let p = p0; if (p.endsWith("/")) p += "index.html";
      const f = path.join(ROOT, path.normalize(p)); if (!f.startsWith(ROOT)) { res.writeHead(403); res.end(); return; }
      fs.readFile(f, (err, buf) => { if (err) { res.writeHead(404); res.end(); return; } res.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream" }); res.end(buf); });
    });
    server.listen(0, "127.0.0.1", () => resolve({ server, kv, base: "http://127.0.0.1:" + server.address().port + "/" }));
  });
  const ON = await serve(true), OFF = await serve(false);
  const browser = await chromium.launch({ args: ["--no-proxy-server"] });
  const errors = [];
  const open = async (S, width, opts) => {
    const ctx = await browser.newContext(Object.assign({ viewport: { width, height: width < 600 ? 844 : 800 } }, opts || {}));
    const p = await ctx.newPage();
    p.on("pageerror", e => errors.push("page error: " + String(e).slice(0, 300)));
    p.on("console", m => { if (m.type() === "error" && !/favicon|Failed to load resource/.test(m.text())) errors.push("console: " + m.text().slice(0, 300)); });
    await p.goto(S.base + "#home"); await p.waitForTimeout(700);
    return p;
  };
  const go = async (p, hash, ms) => { await p.evaluate(h => { location.hash = h; }, hash); await p.waitForTimeout(ms || 500); };
  const shot = async (p, name) => { if (SHOTS) { fs.mkdirSync(SHOTS, { recursive: true }); await p.screenshot({ path: path.join(SHOTS, name + ".png"), fullPage: true }); } };
  const box = (p, sel) => p.evaluate(s => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect(); return { x: Math.round(r.left), r: Math.round(r.right), y: Math.round(r.top), w: Math.round(r.width) }; }, sel);

  /* ---- A. one top bar and one column, at 1280 and at 390 ---- */
  const PAGES = ["#home", "#facts", "#quiz", "#numbers", "#checking", "#methods", "#about", "#howto", "#s-cannabis", "#substances", "#interactions", "#glossary", "#emergency", "#law", "#wanted", "#auto"];
  for (const width of [1280, 390]) {
    const p = await open(ON, width), seen = [];
    // (2.12) a page our system started is a page like the others: the first one the build shows today is walked through too
    const started = await p.evaluate(() => (typeof AUTO_PAGES === "object" && AUTO_PAGES ? Object.keys(AUTO_PAGES)[0] || "" : ""));
    for (const h of PAGES.concat(started ? ["#auto/p-" + started] : [])) {
      await go(p, h, 350);
      const brand = await box(p, ".topbar .brand"), menu = await box(p, "#menubtn"), h1 = await box(p, ".view.active h1");
      const col = await p.evaluate(() => { const v = [...document.querySelectorAll(".view.active .wrap")].find(e => e.getClientRects().length); const r = v.getBoundingClientRect(), s = getComputedStyle(v); return Math.round(r.left + parseFloat(s.paddingLeft)); });   // (the column that is shown: a view may hold one that is not)
      seen.push({ h, brand: brand.x, menu: menu.x, gap: menu.x - brand.r, col, h1: h1 ? h1.x : null });
    }
    const same = k => new Set(seen.map(x => x[k])).size === 1;
    ok(width + " px: the Menu button is in the same place on every page", same("menu"), JSON.stringify(seen.map(x => [x.h, x.menu])));
    if (width === 1280) ok("1280 px: the Menu button stands right after the name on every page", seen.every(x => x.gap >= 0 && x.gap <= 40), JSON.stringify(seen.map(x => [x.h, x.gap])));
    ok(width + " px: every page starts at the same left edge as the top bar's name", same("col") && seen.every(x => Math.abs(x.col - x.brand) <= 1), JSON.stringify(seen.map(x => [x.h, x.col, x.brand])));
    if (width === 1280) { await go(p, "#facts"); await shot(p, "1280-facts"); await go(p, "#numbers", 900); await shot(p, "1280-numbers"); }
    await p.context().close();
  }

  /* ---- B. the start page ---- */
  {
    const p = await open(ON, 390);
    const n = await p.evaluate(() => ({ tiles: document.querySelectorAll("#dgrid .dcard").length, all: (document.querySelector("#home-all a") || {}).textContent || "", more: [...document.querySelectorAll("#home-more a .sm-n")].map(e => e.textContent), crumb: document.getElementById("crumb").hidden, asked: document.getElementById("home-asked").hidden }));
    ok("start page: twelve drugs, then a row to all of them", n.tiles === 12 && /^All \d+ drugs/.test(n.all), JSON.stringify(n));
    ok("start page: what is not about one drug is three rows (mixing, big questions, statistics)", n.more.length === 3 && /mix/i.test(n.more[0]) && /Big questions/.test(n.more[1]) && /Statistics/.test(n.more[2]), n.more.join(" | "));
    ok("start page: no Back line, and no list of questions while none was asked", n.crumb && n.asked);
    await shot(p, "390-home");

    /* ---- C. where Back leads, and the page as it was ---- */
    await p.click('#home .qz2-more a, .qz2-more a'); await p.waitForTimeout(500);
    let c = await p.evaluate(() => ({ hash: location.hash, hidden: document.getElementById("crumb").hidden, text: document.getElementById("crumb").textContent.trim() }));
    ok("Myth or fact? page: the line under the top bar says Back to Start page", c.hash === "#quiz" && !c.hidden && c.text === "Back to Start page", JSON.stringify(c));
    await p.click("#crumb a"); await p.waitForTimeout(500);
    c = await p.evaluate(() => ({ hash: location.hash, hidden: document.getElementById("crumb").hidden }));
    ok("the Back line goes back (to the start page, where it is not shown)", (c.hash === "#home" || c.hash === "") && c.hidden, JSON.stringify(c));
    // a drug page: a section, a question open, scrolled down; then another page, and Back
    await go(p, "#s-mdma"); await p.click('#drug2 .secmenu .sm-b[data-sec="d-risk"]'); await p.waitForTimeout(600);
    const qid = await p.evaluate(() => { const d = [...document.querySelectorAll("#d-risk details.ask")][2]; d.open = true; return d.id; });
    await p.waitForTimeout(700); await p.mouse.wheel(0, 420); await p.waitForTimeout(600);
    const before = await p.evaluate(() => ({ y: Math.round(window.scrollY), hash: location.hash }));
    const inSec = await p.evaluate(() => ({ hidden: document.getElementById("crumb").hidden, up: ((document.querySelector("#drug2 .secmenu .sm-up") || {}).textContent || "").trim(), shown: !!(document.querySelector("#drug2 .secmenu .sm-up") || { getClientRects: () => [] }).getClientRects().length }));
    ok("in a section opened from its page's list, the section menu's first chip leads back to the list and the Back line rests (one way back, not two)", inSec.hidden && inSec.up === "MDMA" && inSec.shown, JSON.stringify(inSec));
    await go(p, "#about", 600);
    c = await p.evaluate(() => document.getElementById("crumb").textContent.trim());
    ok("on the next page the Back line names the section left", /^Back to MDMA: /.test(c), c);
    await p.goBack(); await p.waitForTimeout(1500);
    let after = await p.evaluate(id => ({ y: Math.round(window.scrollY), hash: location.hash, open: document.getElementById(id).open, others: document.querySelectorAll("#d-risk details.ask[open]").length }), qid);
    ok("Back puts the page as it was: the same section, the same question open, the same place", after.hash === before.hash && after.open && after.others === 1 && Math.abs(after.y - before.y) <= 6, JSON.stringify({ before, after }));
    await p.reload(); await p.waitForTimeout(1800);
    after = await p.evaluate(id => ({ y: Math.round(window.scrollY), hash: location.hash, open: !!(document.getElementById(id) || {}).open }), qid);
    ok("a reload does the same", after.hash === before.hash && after.open && Math.abs(after.y - before.y) <= 6, JSON.stringify({ before, after }));
    await p.goForward(); await p.waitForTimeout(700);
    ok("Forward goes forward again", (await p.evaluate(() => location.hash)) === "#about");
    await p.context().close();
  }

  /* ---- D. one Myth or fact deck, kept ---- */
  {
    const p = await open(ON, 390);
    const card = sel => p.evaluate(s => { const b = document.querySelector(s); if (!b) return null; const c = b.querySelector(".mf-card"); return { n: (b.querySelector(".mf-card.flipped .mf-back .qz2-score") || b.querySelector(".mf-front .qz2-score")).textContent, q: b.querySelector(".mf-q").textContent, flipped: c.classList.contains("flipped") }; }, sel);
    await p.click("#tf .qz2-o[data-v='fact']"); await p.waitForTimeout(700);
    await p.click("#tf .qz2-nb"); await p.waitForTimeout(400);
    const home2 = await card("#tf");
    ok("start page: after one card the deck is at 2 of 10", home2.n === "2 of 10" && !home2.flipped, JSON.stringify(home2));
    await go(p, "#quiz");
    let q2 = await card("#quizpage");
    ok("Myth or fact? page: the same deck, at the same card", q2.n === "2 of 10" && q2.q === home2.q && !q2.flipped, JSON.stringify({ home2, q2 }));
    await p.click("#quizpage .qz2-o[data-v='myth']"); await p.waitForTimeout(700);
    const score = await p.evaluate(() => document.getElementById("mf-score").textContent);
    ok("Myth or fact? page: the count of cards answered on this device", /answered 2 cards: [0-2] right/.test(score), score);
    await go(p, "#home");
    let h3 = await card("#tf");
    ok("back on the start page the deck shows that card answered", h3.n === "2 of 10" && h3.q === home2.q && h3.flipped, JSON.stringify(h3));
    await p.reload(); await p.waitForTimeout(900);
    h3 = await card("#tf");
    ok("after a reload the deck is where it was", h3.n === "2 of 10" && h3.q === home2.q && h3.flipped, JSON.stringify(h3));
    await go(p, "#quiz"); await p.click('#mf-pick [data-mfp="cannabis"]'); await p.waitForTimeout(500);
    const can = await p.evaluate(() => ({ n: document.querySelector("#quizpage .mf-front .qz2-score").textContent, k: document.querySelector("#quizpage .qz2-k").textContent, pressed: document.querySelector('#mf-pick [data-mfp="cannabis"]').getAttribute("aria-pressed") }));
    ok("Myth or fact? page: a drug can be chosen, and its own deck starts", /^1 of \d+$/.test(can.n) && /Cannabis/.test(can.k) && can.pressed === "true", JSON.stringify(can));
    await p.click('#mf-pick [data-mfp=""]'); await p.waitForTimeout(400);
    q2 = await card("#quizpage");
    ok("and All drugs brings the kept deck back", q2.n === "2 of 10" && q2.q === home2.q, JSON.stringify(q2));
    // ten cards: the result of ten
    for (let i = 0; i < 9; i++) { if (await p.$("#quizpage .mf-card:not(.flipped) .qz2-o[data-v='fact']")) { await p.click("#quizpage .mf-card:not(.flipped) .qz2-o[data-v='fact']"); await p.waitForTimeout(520); } const last = await p.evaluate(() => /Another 10/.test((document.querySelector("#quizpage .qz2-nb") || {}).textContent || "")); if (last) break; await p.click("#quizpage .qz2-nb"); await p.waitForTimeout(260); }
    const res = await p.evaluate(() => ({ res: (document.querySelector("#quizpage .mf-res") || {}).textContent || "", nb: (document.querySelector("#quizpage .qz2-nb") || {}).textContent || "" }));
    ok("after the tenth card the deck says how many were right", /^\d+ of 10 right$/.test(res.res) && res.nb === "Another 10", JSON.stringify(res));
    await shot(p, "390-quiz-end");
    await p.context().close();
  }

  /* ---- E. every long page as a menu of sections ---- */
  {
    const p = await open(ON, 390);
    const state = sel => p.evaluate(s => { const pg = document.querySelector(s); return pg ? { rows: pg.querySelectorAll(".secmenu .sm-b").length, open: [...pg.querySelectorAll(".secs > .sec")].filter(x => !x.hidden).map(x => x.id), on: pg.querySelector(".secmenu").classList.contains("on"), hash: location.hash } : null; }, sel);
    await go(p, "#facts");
    let st = await state("#facts-box");
    ok("Big questions about drugs: a menu of sections, none open", st.rows >= 7 && st.open.length === 0 && !st.on, JSON.stringify(st));
    ok("Big questions about drugs: its name on the page, in the menu and as the tab's title", await p.evaluate(() => document.querySelector("#view-facts h1").textContent === "Big questions about drugs" && /Big questions about drugs/.test(document.title) && [...document.querySelectorAll("#menu a")].some(a => a.textContent === "Big questions about drugs")));
    await shot(p, "390-facts");
    await p.click("#facts-box .sm-b"); await p.waitForTimeout(500);
    st = await state("#facts-box"); const first = st.open[0];
    ok("a row opens its section alone, and the address carries it", st.open.length === 1 && st.on && st.hash === "#facts/part-" + first, JSON.stringify(st));
    await p.click('#facts-box .secmenu .sm-b[aria-expanded="false"]'); await p.waitForTimeout(500);
    st = await state("#facts-box");
    ok("another section closes the first", st.open.length === 1 && st.open[0] !== first, JSON.stringify(st));
    await p.click("#facts-box .sm-up"); await p.waitForTimeout(400);
    st = await state("#facts-box"); ok("the page's name in the chips brings the list back", st.open.length === 0 && st.hash === "#facts", JSON.stringify(st));
    await go(p, "#facts/q-cl_gen_portugal", 800);
    let q = await p.evaluate(() => { const d = document.getElementById("fx-cl_gen_portugal"), sec = d && d.closest(".sec"); return { open: !!(d && d.open), sec: sec ? sec.id : null, hidden: sec ? sec.hidden : null, top: d ? Math.round(d.getBoundingClientRect().top) : null, stick: parseInt(getComputedStyle(document.documentElement).getPropertyValue("--stick-h")) }; });
    ok("a question's address opens its section with the question open, clear of the bars", q.open && q.sec === "f-laws" && q.hidden === false && q.top >= q.stick - 2 && q.top < 420, JSON.stringify(q));
    await go(p, "#home"); await go(p, "#cl_gen_remission", 1200);
    q = await p.evaluate(() => ({ view: document.querySelector(".view.active").id, sheet: document.getElementById("evsheet").classList.contains("open"), open: !!(document.getElementById("fx-cl_gen_remission") || {}).open }));
    ok("a general answer's own address opens it on that page with its evidence over it", q.view === "view-facts" && q.sheet && q.open, JSON.stringify(q));
    await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    // drug checking
    await go(p, "#checking");
    st = await state("#dc-page");
    ok("Drug checking: four sections, none open", st.rows === 4 && st.open.length === 0, JSON.stringify(st));
    await shot(p, "390-checking");
    await go(p, "#checking/kits", 600); st = await state("#dc-page");
    ok("Drug checking: the old address of the answers on test kits opens that section", st.open.join() === "c-work", JSON.stringify(st));
    ok("Drug checking: the answers are listed under their topics, with no second heading or In short", await p.evaluate(() => document.querySelectorAll("#c-work details.ask").length >= 10 && !document.querySelector("#c-work .inshort2") && document.querySelectorAll("#c-work h2").length === 1));
    await go(p, "#checking/c-Greece", 700); st = await state("#dc-page");
    ok("Drug checking: a country's address opens the services", st.open.join() === "c-near" && await p.evaluate(() => document.getElementById("dc-all").open), JSON.stringify(st));
    await go(p, "#checking/part-c-kits", 600);
    ok("Drug checking: test kits for home are their own section, asking for the country or showing it", await p.evaluate(() => { const s = document.getElementById("c-kits"); return !s.hidden && !!s.querySelector(".cq"); }));
    await go(p, "#checking/part-c-look", 600);
    ok("Drug checking: the look-alikes are their own section, with photos", await p.evaluate(() => { const s = document.getElementById("c-look"); return !s.hidden && s.querySelectorAll("img").length >= 4; }));
    // the text pages
    for (const [view, min] of [["methods", 8], ["about", 8], ["howto", 2]]) {
      await go(p, "#" + view); st = await state("#view-" + view + " .secpage");
      ok(view + ": its text is a menu of sections, none open", st && st.rows >= min && st.open.length === 0, JSON.stringify(st));
      const lines = await p.evaluate(v => [...document.querySelectorAll("#view-" + v + " .secmenu .sm-b")].map(b => (b.querySelector(".sm-l") || { textContent: "" }).textContent), view);
      ok(view + ": every row says in a few words what its section holds", lines.length >= min && lines.every(t => t.length > 12 && t.length < 110), lines.join(" | ").slice(0, 300));
      await p.click("#view-" + view + " .secpage .sm-b"); await p.waitForTimeout(450); const s1 = await state("#view-" + view + " .secpage");
      ok(view + ": a row opens its section alone, with its text", s1.open.length === 1 && s1.hash === "#" + view + "/part-" + s1.open[0] && await p.evaluate(id => document.getElementById(id).textContent.trim().length > 80, s1.open[0]), JSON.stringify(s1));
      if (view === "methods") await shot(p, "390-methods-section");
    }
    // (a row's quiet line is cut from its section's text; the words of neighbouring elements must not run together: "draftNot yet")
    const glued = await p.evaluate(() => [...document.querySelectorAll("#view-methods .secpage .secs > .sec")].map(sec => { const b = sec.querySelector(".sec-b") || sec, tmp = document.createElement("div"); tmp.innerHTML = b.innerHTML.replace(/<[^>]+>/g, " ");
      const t = tmp.textContent.replace(/\s+/g, " ").replace(/ ([,.;:])/g, "$1").trim(), l = document.querySelector('#view-methods .secmenu .sm-b[data-sec="' + sec.id + '"] .sm-l'), line = l ? l.textContent.replace(/…$/, "") : "";
      return !line || !t.startsWith(line) ? sec.id + ": " + line : null; }).filter(Boolean));
    ok("methods: every row's quiet line is the start of its section's text, word for word", glued.length === 0, glued.join(" | "));
    await p.context().close();
  }

  /* ---- F. statistics ---- */
  {
    const p = await open(ON, 390);
    await go(p, "#numbers", 1500);
    const rows = await p.evaluate(() => [...document.querySelectorAll("#num-page .secmenu .sm-b")].map(b => b.querySelector(".sm-n").textContent + " | " + (b.querySelector(".sm-l") || { textContent: "" }).textContent));
    ok("Statistics: a menu of places, each naming where its figures come from (a name, never a record's id)", rows.length >= 3 && rows.some(r => r.startsWith("The world |")) && rows.every(r => /\| From [A-Z]/.test(r) && !/_/.test(r)), rows.join(" || "));
    await p.click('#num-page .sm-b[data-sec="n-global"]'); await p.waitForTimeout(600);
    const w = await p.evaluate(() => { const s = document.getElementById("n-global"), t = s.textContent, card = [...s.querySelectorAll(".fig2")].map(c => ({ d: (c.querySelector(".f2-d") || {}).textContent || "", v: c.querySelector(".f2-v").textContent.trim(), t: c.querySelector(".f2-t").textContent }));
      return { bars: s.querySelectorAll(".fbars .fb-l li").length, rows: card.length, first: card[0], inTwelve: card.some(c => c.v === "1 in 12"), labels: card.filter(c => c.d).length, kinds: [...s.querySelectorAll("h3.tp")].map(h => h.textContent), src: s.querySelectorAll(".f2-src").length }; });
    ok("Statistics, the world: drugs counted the same way are bars side by side", w.bars >= 3, JSON.stringify(w));
    ok("Statistics: a figure is its drug, its number in everyday words (316 million, 1 in 12) and what it counts", w.first && w.first.d === "Any drug" && w.first.v === "316 million" && /^People who used a drug/.test(w.first.t) && w.inTwelve && w.labels === w.rows, JSON.stringify(w));
    ok("Statistics: figures under plain headings, each with its source one tap away", w.kinds.length >= 3 && /How many people use it/.test(w.kinds[0]) && w.kinds.some(k => /use disorder/.test(k)) && w.src === w.rows && w.rows >= 8, JSON.stringify(w));
    // every figure of every place: no number is said in a source's shorthand, and none is left without words
    const words = await p.evaluate(() => { const bad = [], all = EPI_ALL.filter(r => r.status === "verified"); all.forEach(r => { const tmp = document.createElement("div"); tmp.innerHTML = figRow2(r, false); const v = tmp.querySelector(".f2-v").textContent, t = tmp.querySelector(".f2-t").textContent, m = tmp.querySelector(".f2-m").textContent;
      if (/persons|one in N|\((approximate|lower bound|upper bound)|unit word|\d \d{3}\b|population|NaN|undefined|^\s*$/.test(v) || /NaN|undefined|^\s*$/.test(t) || /\(civilian|\bpopulation aged\b|undefined/.test(m) || !tmp.querySelector(".f2-d").textContent) bad.push(r.id + ": " + v + " / " + t.slice(0, 40) + " / " + m); });
      const val = id => { const r = all.find(x => x.id === id), x = r && figVal(r); return x ? (x.v + " " + x.u).trim() : "missing"; }, find = re => { const r = all.find(x => re.test(x.unit)), x = r && figVal(r); return x ? x.v : "missing"; };
      return { n: all.length, bad: bad.slice(0, 5), approx: find(/^persons \(approximate/), lower: find(/^persons \(lower bound/), upper: find(/^percent \(upper bound/), half: find(/^percent \('Half/), change: [...new Set(all.filter(r => /^percent change/.test(r.unit)).map(r => figVal(r).v[0]))].sort().join(""), thc: (r => r ? figVal(r) : null)(all.find(r => r.unit === "percent THC")) }; });
    ok("Statistics: all " + words.n + " figures say their number plainly (about, more than, less than, half, a rise or a fall with its sign), none in a source's shorthand", words.n > 250 && !words.bad.length && /^About /.test(words.approx) && /^More than /.test(words.lower) && /^Less than /.test(words.upper) && words.half === "Half" && words.change === "+−" && words.thc && /%$/.test(words.thc.v) && words.thc.u === "THC", JSON.stringify(words));
    await p.click("#n-global .f2-src summary"); await p.waitForTimeout(200);
    ok("Statistics: a figure's source opens with its link and where it was checked", await p.evaluate(() => { const d = document.querySelector("#n-global .f2-src[open]"); return !!d && !!d.querySelector('a[href^="http"]') && /Checked/.test(d.textContent); }));
    await p.selectOption("#num-sub-global", "cocaine"); await p.waitForTimeout(300);
    const w2 = await p.evaluate(() => ({ rows: document.querySelectorAll("#n-global .fig2").length, labels: document.querySelectorAll("#n-global .fig2 .f2-d").length, all: [...document.querySelectorAll("#n-global .fig2 .f2-t")].every(e => /cocaine/i.test(e.textContent)) }));
    ok("Statistics: a drug can be chosen; its figures alone are listed, without repeating its name on each", w2.rows >= 2 && w2.rows < w.rows && w2.labels === 0 && w2.all, JSON.stringify(w2));
    await shot(p, "390-numbers-world-cocaine");
    await p.selectOption("#num-sub-global", ""); await p.waitForTimeout(300); await shot(p, "390-numbers-world");
    await p.click('#num-page .sm-b[data-sec="n-europe"]'); await p.waitForTimeout(700);
    const e = await p.evaluate(() => { const s = document.getElementById("n-europe"); return { shown: s.querySelectorAll(".figs2:not([hidden]) .fig2").length, more: s.querySelectorAll(".morebtn").length, world: document.getElementById("n-global").hidden, kinds: [...s.querySelectorAll("h3.tp")].map(h => h.firstChild.textContent.trim()) }; });
    ok("Statistics, Europe: a long list shows its first figures and keeps the rest one tap away; the world has closed", e.shown > 5 && e.shown <= 60 && e.more >= 1 && e.world && e.kinds.includes("Hospital emergencies") && e.kinds.includes("Deaths"), JSON.stringify(e));
    await p.click('#num-page .sm-b[data-sec="n-us"]'); await p.waitForTimeout(700);
    const us = await p.evaluate(() => { const s = document.getElementById("n-us"), caps = [...s.querySelectorAll(".fbars figcaption")].map(c => c.textContent), src = [...new Set([...s.querySelectorAll(".f2-src > summary")].map(x => x.textContent))];
      return { caps, src, who: [...new Set([...s.querySelectorAll(".f2-m")].map(m => m.textContent))].slice(0, 3), counted: /Counted among: people aged 12 or older \(civilian, non-institutionalized\)\./.test(s.textContent) }; });
    ok("Statistics, United States: use and use disorders are drawn apart, as shares; the source is named; who was counted is short, with the source's wording one tap away",
      us.caps.length >= 2 && us.caps.some(c => /^Used in the last 12 months/.test(c)) && us.caps.some(c => /^Had a use disorder in the last 12 months/.test(c)) && us.src.join() === "SAMHSA, 2025" && us.who.every(m => /ages 12 or older$/.test(m)) && us.counted, JSON.stringify(us));
    await shot(p, "390-numbers-us");
    await p.context().close();
  }

  /* ---- G. if it gets too much: a friend first on the opioid pages ---- */
  {
    const p = await open(ON, 390);
    const order = slug => p.evaluate(() => { const b = document.querySelector("#d-help .sec-b"); return { heads: [...b.querySelectorAll("h3, h4, details > summary")].map(h => h.tagName[0] + ":" + h.textContent.trim()), fold: !!b.querySelector("details.hp-aid") }; });
    await go(p, "#s-heroin/part-d-help", 800); let o = await order();
    ok("heroin: a friend first, the ambulance signs first, the breathing steps in view, then For you", o.heads[0] === "H:For a friend" && o.heads[1] === "H:Call an ambulance if" && o.heads.indexOf("H:What helps") === 2 && o.heads.includes("H:If they pass out or stop breathing") && !o.fold && o.heads.indexOf("H:For you") > o.heads.indexOf("H:What not to do"), JSON.stringify(o));
    ok("heroin: naloxone leads what helps", await p.evaluate(() => { const hs = [...document.querySelectorAll("#d-help h4")].find(h => h.textContent === "What helps"); return /naloxone/i.test(hs.nextElementSibling.querySelector("li").textContent); }));
    ok("heroin: the way to the emergency numbers stands with the ambulance signs, before what helps", await p.evaluate(() => { const m = document.querySelector("#d-help .hp-more"), hs = [...document.querySelectorAll("#d-help h4")].find(h => h.textContent === "What helps"); return !!m && !!m.querySelector('a[href="#emergency"]') && !!(m.compareDocumentPosition(hs) & Node.DOCUMENT_POSITION_FOLLOWING) && document.querySelectorAll("#d-help .hp-more").length === 1; }));
    await shot(p, "390-heroin-help");
    await go(p, "#s-cannabis/part-d-help", 800); o = await order();
    ok("cannabis: as in 2.3 (yourself first, the ambulance last, first aid one tap away)", o.heads[0] === "H:For you" && o.fold && o.heads.indexOf("H:Call an ambulance if") > o.heads.indexOf("H:What helps"), JSON.stringify(o));
    await p.context().close();
  }

  /* ---- H. the email: the message in the subject, and first in the body ---- */
  {
    const p = await open(OFF, 390);
    await p.click(".fb-fab"); await p.click('.fb-opt[data-mode="feedback"]'); await p.fill("#report-message", "can i have hallucinations from alcohol?\nand how long do they last");
    const m = await p.evaluate(() => { const u = new URL(document.getElementById("fb-mailto").href.replace("mailto:", "https://x/")); return { subject: u.searchParams.get("subject"), body: u.searchParams.get("body") }; });
    ok("email: the subject is a tag and the person's own first words", m.subject === "[Pharmakon question] can i have hallucinations from alcohol? and how long do they last", m.subject);
    const lines = m.body.split("\n");
    ok("email: the body starts with the message; what the page adds stands under a line; the last line is in a fixed form", lines[0] === "can i have hallucinations from alcohol?" && lines.includes("--") && lines.indexOf("--") > 1 && /^pharmakon \| question \| home \| \d+\.\d+\.\d+$/.test(lines[lines.length - 1]), JSON.stringify(lines));
    await p.click('.fb-opt[data-mode="issue"]');
    const s2 = await p.evaluate(() => new URL(document.getElementById("fb-mailto").href.replace("mailto:", "https://x/")).searchParams.get("subject"));
    ok("email: a mistake carries its own tag", s2.startsWith("[Pharmakon mistake] can i have"), s2);
    await p.context().close();
  }

  /* ---- I. Ask us to check it, and Your questions ---- */
  const typeQ = async (p, text) => { await p.click("#search"); await p.fill("#search", text); await p.waitForFunction(() => window.pkInsight && window.pkInsight.state() === "ready", null, { timeout: 90000 }); await p.waitForSelector("#search-results .sr-fit", { timeout: 20000 }); await p.waitForTimeout(300); };
  {
    const p = await open(ON, 390);
    await p.waitForTimeout(1500);   // the page asks once whether it can send
    await typeQ(p, "is modafinil safe");
    const before = await p.evaluate(() => ({ none: (document.querySelector(".sr-fit-none") || {}).textContent || "", note: (document.querySelector(".sr-fit .ask-note") || {}).textContent || "", insNote: (document.querySelector(".sr-note") || {}).textContent || "" }));
    ok("with the store on: the button says what it sends", /We haven.t checked exactly this yet/.test(before.none) && before.note === "Sends only this question. No name, no address.", JSON.stringify(before));
    await p.click(".sr-fit button[data-ask]"); await p.waitForTimeout(900);
    const said = await p.evaluate(() => (document.querySelector(".ask-said") || {}).textContent || "");
    ok("one tap: the page says it was sent, and promises only what is true (no answer within the hour until the half-hourly run keeps it)", said === "Sent. We will check it. It is kept under “Your questions” on the start page, and turns green there when it is answered." && await p.evaluate(() => AUTO_LOOP === false), said);
    const kept = [...ON.kv.entries()].filter(([k]) => k.startsWith("q:")).map(([, v]) => JSON.parse(v));
    ok("the store holds the question's words, its page, the site version, the day and a count, and nothing else", kept.length === 1 && kept[0].q === "is modafinil safe" && Object.keys(kept[0]).sort().join() === "d,dn,first,last,n,q,v" && /^\d+\.\d+\.\d+$/.test(kept[0].v), JSON.stringify(kept));
    await p.fill("#search", ""); await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    let list = await p.evaluate(() => { const b = document.getElementById("home-asked"); return { hidden: b.hidden, rows: [...b.querySelectorAll(".aq")].map(r => r.className + " | " + r.querySelector(".aq-k").textContent + " | " + r.querySelector(".aq-q").textContent) }; });
    ok("start page: Your questions lists it as sent and being checked", !list.hidden && list.rows.length === 1 && /wait \| Sent\. We are checking \| is modafinil safe/.test(list.rows[0]), JSON.stringify(list));
    ok("the list says where it is kept, and that we see a question only if it is sent", await p.evaluate(() => (document.querySelector("#home-asked .aq-note") || {}).textContent === "This list is kept on this device only. We see a question only if you send it. A question turns green here when it is answered."));
    // (2.9; the senior author, of his two sent questions: "i cannot click on them to see the answer") a question that waits opens too
    await p.click("#home-asked .aq.wait button.aq-look"); await p.waitForTimeout(900);
    const lk = await p.evaluate(() => ({ value: document.getElementById("search").value, open: !document.getElementById("search-results").hidden, go: (document.querySelector("#home-asked .aq.wait .aq-go") || {}).textContent || "", fit: !!document.querySelector("#search-results .sr-fit, #search-results a, #search-results .sr-get") }));
    ok("a question that waits can be opened: its row asks it again in the box, which shows what the site has on it so far", lk.value === "is modafinil safe" && lk.open && lk.fit && /^See what we have so far/.test(lk.go), JSON.stringify(lk));
    await p.fill("#search", ""); await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    await typeQ(p, "why do people take drugs"); await p.click(".sr-fit button[data-ask]"); await p.waitForTimeout(800);
    await p.fill("#search", ""); await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    list = await p.evaluate(() => [...document.querySelectorAll("#home-asked .aq-q")].map(e => e.textContent));
    ok("a second question is kept beside the first", list.length === 2 && list.includes("why do people take drugs"), JSON.stringify(list));
    await shot(p, "390-home-asked");
    await p.reload(); await p.waitForTimeout(900);
    ok("the list is still there after a reload", (await p.evaluate(() => document.querySelectorAll("#home-asked .aq").length)) === 2);
    await p.click("#home-asked .aq-x"); await p.waitForTimeout(300);
    ok("the cross takes a question off the list", (await p.evaluate(() => document.querySelectorAll("#home-asked .aq").length)) === 1);
    // answered: a question kept under an older version of the site, which the site can answer now
    // (2.5: the first one is a question the reader asked to be told about from our list; it turns green the same way)
    await p.evaluate(() => { localStorage.setItem("pk-asked", JSON.stringify([{ k: "is weed addictive", q: "is weed addictive", d: "", t: Date.now() - 864e5, cv: "0.0.1", st: "wait", sent: 1, w: "w_0000" }, { k: "what is the capital of mongolia", q: "what is the capital of mongolia", d: "", t: Date.now(), cv: "0.0.1", st: "wait", sent: 1 }])); });
    await p.reload(); await p.waitForSelector("#home-asked .aq.ans", { timeout: 90000 });
    const ans = await p.evaluate(() => [...document.querySelectorAll("#home-asked .aq")].map(r => ({ cls: r.className, k: r.querySelector(".aq-k").textContent, q: r.querySelector(".aq-q").textContent, href: (r.querySelector("a.aq-a") || {}).getAttribute ? r.querySelector("a.aq-a").getAttribute("href") : null })));
    ok("a kept question that the site can answer now shows first, in green, as Answered; the other is still being checked", ans.length === 2 && /ans/.test(ans[0].cls) && ans[0].k === "Answered" && ans[0].q === "is weed addictive" && /^#/.test(ans[0].href || "") && /wait/.test(ans[1].cls), JSON.stringify(ans));
    await shot(p, "390-home-answered");
    await p.click("#home-asked .aq.ans a.aq-a"); await p.waitForTimeout(900);
    const opened = await p.evaluate(() => ({ sheet: document.getElementById("evsheet").classList.contains("open"), left: JSON.parse(localStorage.getItem("pk-asked")).map(x => x.k) }));
    ok("reading it opens the answer over the page and takes it off the list", opened.sheet && opened.left.join() === "what is the capital of mongolia", JSON.stringify(opened));
    await p.context().close();
  }
  {
    const p = await open(OFF, 390);
    await p.waitForTimeout(1500);
    await typeQ(p, "is modafinil safe");
    const note = await p.evaluate(() => ({ note: !!document.querySelector(".sr-fit .ask-note"), ins: (document.querySelector(".sr-note") || {}).textContent || "" }));
    ok("with the store off: no promise of sending, and Insight still says nothing typed leaves the device", !note.note && /Nothing you type leaves it/.test(note.ins), JSON.stringify(note));
    await p.click(".sr-fit button[data-ask]"); await p.waitForTimeout(900);
    const fb = await p.evaluate(() => ({ open: document.getElementById("report").classList.contains("open"), text: document.getElementById("report-message").value, kept: JSON.parse(localStorage.getItem("pk-asked") || "[]").map(x => x.q + "|" + x.sent) }));
    ok("with the store off: the email form opens with the question, and it is kept on the device", fb.open && fb.text === "is modafinil safe" && fb.kept.join() === "is modafinil safe|0", JSON.stringify(fb));
    await p.click("#report-close"); await p.fill("#search", ""); await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    const row = await p.evaluate(() => { const r = document.querySelector("#home-asked .aq"); return r ? { cls: r.className, k: r.querySelector(".aq-k").textContent, send: (r.querySelector("button.aq-send") || {}).textContent || "", note: (document.querySelector("#home-asked .aq-note") || {}).textContent || "" } : null; });
    ok("with the store off: the list says Not sent, where the list is kept, and offers to send it", row && /unsent/.test(row.cls) && row.k === "Not sent" && row.send === "Send it to us" && /kept on this device only/.test(row.note), JSON.stringify(row));
    await p.click("#home-asked button.aq-send"); await p.waitForTimeout(700);
    const again = await p.evaluate(() => ({ open: document.getElementById("report").classList.contains("open"), text: document.getElementById("report-message").value, how: (document.querySelector("#report .fb-how") || {}).textContent || "", head: document.querySelector("#report .fb-head p").textContent, k: document.querySelector("#home-asked .aq-k").textContent }));
    ok("with the store off: Send it to us opens the email form with the question; the form says nothing is sent until Send is pressed there; the row stays Not sent", again.open && again.text === "is modafinil safe" && /Nothing is sent until you press Send there/.test(again.how) && again.k === "Not sent", JSON.stringify(again));
    ok("the form's head no longer says that the most asked questions are answered first (nor does any page)", again.head === "Both reach the editors. We read everything." && await p.evaluate(() => { location.hash = "#s-cannabis"; return new Promise(r => setTimeout(() => r(!/ask most are answered first/.test([...document.querySelectorAll("main, #report, #menu, footer.site")].map(e => e.textContent).join(" "))), 500)); }), again.head);   // (the page's text, not its script)
    await p.context().close();
  }
  {
    // a question kept while sending was off can be sent from the list once sending is on
    const p = await open(ON, 390);
    await p.evaluate(() => localStorage.setItem("pk-asked", JSON.stringify([{ k: "does cannabis cause cancer", q: "does cannabis cause cancer", d: "", t: Date.now(), cv: SITE_VERSION, st: "wait", sent: 0 }])));
    await p.reload(); await p.waitForTimeout(1600);
    const before = await p.evaluate(() => (document.querySelector("#home-asked .aq-k") || {}).textContent || "");
    await p.click("#home-asked button.aq-send"); await p.waitForTimeout(900);
    const after = await p.evaluate(() => ({ k: (document.querySelector("#home-asked .aq-k") || {}).textContent || "", form: document.getElementById("report").classList.contains("open"), send: !!document.querySelector("#home-asked button.aq-send") }));
    const stored = [...ON.kv.entries()].filter(([k]) => k.startsWith("q:")).map(([, v]) => JSON.parse(v).q);
    ok("with the store on: a question that was not sent is sent from the list in one tap, and the row says so", before === "Not sent" && after.k === "Sent. We are checking" && !after.form && !after.send && stored.includes("does cannabis cause cancer"), JSON.stringify({ before, after, stored }));
    await p.context().close();
  }

  /* ---- I2 (site 2.5). On our list: a listed question is recognised on the device and counted by its number only; the off
     switch; the browser's own wish; the list's page; a question that is not about drugs ---- */
  {
    const wkeys = S => [...S.kv.entries()].filter(([k]) => k.startsWith("w:")).map(([k, v]) => [k, JSON.parse(v)]);
    const typeW = async (p, text) => { await p.click("#search"); await p.fill("#search", text); await p.waitForFunction(() => window.pkInsight && window.pkInsight.state() === "ready", null, { timeout: 90000 }); await p.waitForFunction(q => { const b = document.querySelector("#search-results > .sr-fit"); return b && b.dataset.q === q; }, text, { timeout: 20000 }); await p.waitForTimeout(200); };
    const card = p => p.evaluate(() => { const c = document.querySelector("#search-results .sr-want"); return c ? { id: c.dataset.want, count: c.hasAttribute("data-count"), note: (c.querySelector(".want-n") || {}).textContent || "", q: c.querySelector(".want-q").textContent, t: c.querySelector(".want-t").textContent } : null; });
    const p = await open(ON, 390), reqs = []; p.on("request", r => { if (/\/api\//.test(r.url())) reqs.push(r.method() + " " + r.url().replace(/^.*\/api\//, "api/") + " " + (r.postData() || "")); });
    await p.waitForTimeout(1500);
    await typeW(p, "how can you die from alcohol");
    const c1 = await card(p);
    ok("a listed question: the card names the listed question and says what is counted", c1 && /^w_\d+$/.test(c1.id) && c1.count && c1.q === "How can you die from alcohol?" && c1.t === "Not answered yet. A question like yours is on our list:" && c1.note === "We count how many people ask this. Your words are not sent.", JSON.stringify(c1));
    ok("nothing is counted at once (the card must stand for a moment)", !reqs.some(x => /api\/want/.test(x)) && !wkeys(ON).length, reqs.join(" | ") || "no request yet");
    await p.waitForTimeout(3000);
    let w = wkeys(ON);
    ok("after a moment the device sends the item's number, and only that", reqs.filter(x => /api\/want/.test(x)).join() === 'POST api/want {"id":"' + c1.id + '"}' && w.length === 1 && w[0][0] === "w:" + c1.id && w[0][1].n === 1 && Object.keys(w[0][1]).sort().join() === "dn,first,last,n", reqs.join(" | ") + " || " + JSON.stringify(w));
    ok("the words typed are nowhere in the store, and no question was sent", ![...ON.kv.entries()].some(([k, v]) => /die from alcohol/i.test(k + v)) && !reqs.some(x => /POST api\/ask/.test(x)), [...ON.kv.keys()].join(", "));
    await typeW(p, "can alcohol kill you"); await p.waitForTimeout(3000); w = wkeys(ON);
    ok("the same item asked again in other words is not counted twice in one visit", w.length === 1 && w[0][1].n === 1 && reqs.filter(x => /api\/want/.test(x)).length === 1, JSON.stringify(w));
    await p.click("#search-results button[data-want-keep]"); await p.waitForTimeout(300);
    await p.fill("#search", ""); await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    const row = await p.evaluate(() => { const r = document.querySelector("#home-asked .aq"); return r ? r.className + " | " + r.querySelector(".aq-k").textContent + " | " + r.querySelector(".aq-q").textContent : ""; });
    ok("Tell me when it is answered: Your questions keeps the LISTED question, as On our list", /onlist \| On our list \| How can you die from alcohol\?$/.test(row), row);
    await shot(p, "390-home-onlist");
    // its own words instead
    await typeW(p, "does weed cause cancer"); await p.click("#search-results .sr-want .want-other"); await p.waitForTimeout(900);
    const sentOwn = [...ON.kv.entries()].filter(([k]) => k.startsWith("q:")).map(([, v]) => JSON.parse(v).q);
    ok("Not the same? Send yours to us: the reader's own words are sent, by their press", sentOwn.includes("does weed cause cancer") && /^Sent\./.test(await p.evaluate(() => (document.querySelector("#search-results .sr-want .ask-said") || {}).textContent || "")), sentOwn.join(" | "));
    // Enter counts at once
    // (16 November 2026: the question this check used, "Can you get addicted to ketamine?", has been answered by the system and left the list.
    // The check now takes a question that IS on the page's list, another one than the item counted above, whatever the list holds that day.)
    const other = await p.evaluate(first => { const x = WANTED.find(([id, q]) => id !== first && /^(?:Can|Is|Does|Do|What|How|Why)\b/.test(q) && !/alcohol/i.test(q)); return x ? { id: x[0], q: x[1] } : null; }, c1.id);
    await typeW(p, other.q.replace(/\?$/, "").toLowerCase()); await p.keyboard.press("Enter"); await p.waitForTimeout(700);
    const sh = await p.evaluate(() => { const c = document.querySelector("#evsheet .ins-want"); return c ? { t: c.querySelector(".ins-none-t").textContent, q: c.querySelector(".want-q").textContent, note: (c.querySelector(".want-n") || {}).textContent || "", id: c.dataset.want } : null; });
    w = wkeys(ON);
    ok("Enter on a listed question: the sheet says so and the item is counted at once", sh && sh.t === "Not answered yet. A question like yours is on our list." && sh.q === other.q && sh.id === other.id && /We count how many people ask this/.test(sh.note) && w.some(([k, v]) => k === "w:" + sh.id && v.n === 1), JSON.stringify(other) + " || " + JSON.stringify(sh) + " || " + JSON.stringify(w));
    await shot(p, "390-sheet-onlist");
    await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    // a question that is not about drugs, with the store on: no promise, a quiet way to send
    await typeW(p, "can i die from mosquito bites");
    const oth = await p.evaluate(() => { const e = document.querySelector("#search-results .sr-other"); return e ? { text: e.textContent.replace(/\s+/g, " "), btn: e.querySelector("button[data-ask]").textContent, askUs: /Ask us to check it/.test(document.getElementById("search-results").textContent) } : null; });
    ok("the senior author's question, “can i die from mosquito bites”: no “Ask us to check it”; “This does not look like a question about drugs. Pharmakon answers questions about drugs”, with a quiet way to send it", oth && /^This does not look like a question about drugs\. Pharmakon answers questions about drugs\. If yours is about one, name the drug, or send it to us\.Sends only this question\. No name, no address\.$/.test(oth.text) && oth.btn === "send it to us" && !oth.askUs, JSON.stringify(oth));
    await shot(p, "390-not-about-drugs");
    // the list's own page
    await p.fill("#search", ""); await p.keyboard.press("Escape"); await go(p, "#wanted", 600);
    const pg = await p.evaluate(() => ({ title: document.title, h1: document.querySelector("#view-wanted h1").textContent, rows: document.querySelectorAll("#wanted-list .wl-i").length, listed: WANTED.length, kept: [...document.querySelectorAll("#wanted-list .wl-s")].map(e => e.closest(".wl-i").querySelector(".wl-q").textContent), first: document.querySelector("#wanted-list .wl-b").dataset.wantKeep, wide: document.documentElement.scrollWidth > innerWidth + 1 }));
    ok("the list has its own page: every listed question, the one already kept marked so, nothing wider than the phone", pg.title === "On our list · Pharmakon" && pg.h1 === "On our list" && pg.rows === pg.listed && pg.rows >= 30 && pg.kept.join() === "How can you die from alcohol?" && !pg.wide, JSON.stringify(pg));
    await shot(p, "390-wanted");
    await p.click("#wanted-list .wl-b"); await p.waitForTimeout(500); w = wkeys(ON);
    ok("on that page, Tell me when it is answered counts the item and keeps it in Your questions", w.some(([k, v]) => k === "w:" + pg.first && v.n === 1) && (await p.evaluate(() => JSON.parse(localStorage.getItem("pk-asked")).filter(x => x.w).length)) === 2 && /^We will tell you on this device/.test(await p.evaluate(() => (document.querySelector("#wanted-list .ask-said") || {}).textContent || "")), JSON.stringify(w));
    // the switch in Privacy
    await go(p, "#about/part-a-privacy", 700);
    const sw = await p.evaluate(() => { const s = document.getElementById("count-switch"); return { there: !!(s && s.offsetParent), checked: s.checked, disabled: s.disabled, state: document.getElementById("count-state").textContent, text: s.closest("li").textContent.replace(/\s+/g, " ").slice(0, 160), old: /no tracking or analytics/.test(document.getElementById("view-about").textContent) }; });
    ok("Privacy says what is counted, with a switch that is on, and no longer says “no tracking or analytics”", sw.there && sw.checked && !sw.disabled && sw.state === "On." && /^One thing is counted\./.test(sw.text) && !sw.old, JSON.stringify(sw));
    await shot(p, "390-privacy");
    await p.click("#count-switch"); await p.waitForTimeout(200);
    const off = await p.evaluate(() => ({ stored: localStorage.getItem("pk-count"), state: document.getElementById("count-state").textContent, checked: document.getElementById("count-switch").checked }));
    ok("switching it off is kept on the device", off.stored === "0" && off.state === "Off on this device." && !off.checked, JSON.stringify(off));
    const nBefore = reqs.filter(x => /api\/want/.test(x)).length;
    await go(p, "#home", 400); await typeW(p, "what is a k hole"); const c2 = await card(p); await p.waitForTimeout(3000);
    ok("with counting switched off: the card still helps, says nothing about counting, and nothing is sent", c2 && !c2.count && !c2.note && c2.q === "What is a K-hole?" && reqs.filter(x => /api\/want/.test(x)).length === nBefore, JSON.stringify(c2));
    await p.context().close();
    // a browser that asks sites not to track (Global Privacy Control): nothing is counted, and the switch says why
    const g = await browser.newContext({ viewport: { width: 390, height: 844 } }); await g.addInitScript(() => { Object.defineProperty(Navigator.prototype, "globalPrivacyControl", { get: () => true, configurable: true }); });
    const gp = await g.newPage(), greqs = []; gp.on("request", r => { if (/\/api\/want/.test(r.url())) greqs.push(r.url()); });
    await gp.goto(ON.base + "#home"); await gp.waitForTimeout(1500);
    await typeW(gp, "what is ego death"); const c3 = await card(gp); await gp.waitForTimeout(3000);
    await gp.evaluate(() => { document.getElementById("search").value = ""; location.hash = "#about/part-a-privacy"; }); await gp.waitForTimeout(700);
    const gsw = await gp.evaluate(() => { const s = document.getElementById("count-switch"); return { checked: s.checked, disabled: s.disabled, state: document.getElementById("count-state").textContent }; });
    ok("a browser that asks not to be tracked is not counted, and the switch says so", c3 && !c3.count && !c3.note && !greqs.length && !gsw.checked && gsw.disabled && gsw.state === "Off: your browser asks sites not to track you.", JSON.stringify(c3) + " " + JSON.stringify(gsw));
    await g.close();
    // with the store off: the card helps, counts nothing, asks nothing of the site
    const q = await open(OFF, 390), oreqs = []; q.on("request", r => { if (/\/api\/want/.test(r.url())) oreqs.push(r.url()); });
    await q.waitForTimeout(1500); await typeW(q, "how can you die from alcohol"); const c4 = await card(q); await q.waitForTimeout(3000);
    ok("with the store off: a listed question still gets its card, nothing is counted and nothing says it is", c4 && !c4.count && !c4.note && !oreqs.length, JSON.stringify(c4));
    await q.context().close();
  }

  /* ---- J. the other long pages: the glossary, the treaties, Find a drug, the emergency numbers ---- */
  {
    const p = await open(ON, 390);
    await go(p, "#glossary", 600);
    let g = await p.evaluate(() => { const rows = [...document.querySelectorAll("#glossary-list details.gterm")], names = rows.map(r => r.querySelector(".ask-q").textContent);
      return { n: rows.length, open: rows.filter(r => r.open).length, sorted: names.every((t, i) => !i || names[i - 1].localeCompare(t, "en", { sensitivity: "base" }) <= 0), shorts: rows.filter(r => r.querySelector(".ask-s")).length, first: names[0], h: Math.round(document.getElementById("glossary-list").getBoundingClientRect().height) }; });
    ok("Glossary: every term is a row with its one-line meaning, from A to Z, none open", g.n >= 40 && g.open === 0 && g.sorted && g.shorts === g.n, JSON.stringify(g));
    await p.click("#glossary-list details.gterm >> nth=2 >> summary"); await p.waitForTimeout(500);
    await p.click("#glossary-list details.gterm >> nth=6 >> summary"); await p.waitForTimeout(700);
    g = await p.evaluate(() => { const rows = [...document.querySelectorAll("#glossary-list details.gterm")], open = rows.filter(r => r.open); return { open: open.map(r => rows.indexOf(r)), text: open.length ? open[0].querySelector(".ask-a").textContent.length : 0, src: open.length ? /Source: /.test(open[0].textContent) : false, top: open.length ? Math.round(open[0].getBoundingClientRect().top) : -1 }; });
    ok("Glossary: a tap opens a term's full meaning and its source; the one open before closes; the term stays in view", g.open.join() === "6" && g.text > 60 && g.src && g.top >= 0 && g.top < 400, JSON.stringify(g));
    await go(p, "#home"); await go(p, "#g-21", 900);
    g = await p.evaluate(() => { const d = document.getElementById("g-21"); return { view: document.querySelector(".view.active").id, open: !!d && d.open, name: d ? d.querySelector(".ask-q").textContent : "", top: d ? Math.round(d.getBoundingClientRect().top) : -1, others: document.querySelectorAll("#glossary-list details.gterm[open]").length }; });
    ok("Glossary: a term's own address opens that term", g.view === "view-glossary" && g.open && g.others === 1 && g.top >= 0 && g.top < 400, JSON.stringify(g));
    await p.fill("#gloss-filter", "odds"); await p.waitForTimeout(300);
    const f = await p.evaluate(() => ({ shown: [...document.querySelectorAll("#glossary-list details.gterm")].filter(r => !r.hidden && r.getClientRects().length).length, count: document.getElementById("gloss-count").textContent }));
    ok("Glossary: the filter still narrows the list", f.shown >= 1 && f.shown < 10 && /of \d+ terms/.test(f.count), JSON.stringify(f));
    await shot(p, "390-glossary-filter");
    // the treaties: the reader's country first
    await go(p, "#law", 700);
    let l = await p.evaluate(() => ({ ask: !!document.querySelector("#law-mine .cq"), lines: document.querySelectorAll("#law-mine .lm").length, fold: document.getElementById("law-all").open, rows: document.querySelectorAll("#law-list tr").length, shown: (tr => !!tr && (tr.checkVisibility ? tr.checkVisibility() : !!tr.offsetParent))(document.querySelector("#law-list tr")) }));   // (a closed fold keeps its boxes in Chromium: ask whether the row is drawn)
    ok("Treaties: the page asks the country first; the table of all countries is one tap away, not spread over the page", l.ask && l.lines === 0 && !l.fold && l.rows > 150 && !l.shown, JSON.stringify(l));
    await p.evaluate(() => localStorage.setItem("pk-country", "Greece")); await p.reload(); await p.waitForTimeout(900);
    l = await p.evaluate(() => ({ where: (document.querySelector("#law-mine .cq-where") || {}).textContent || "", lines: [...document.querySelectorAll("#law-mine .lm")].map(x => x.querySelector(".lm-t b").textContent + ": " + x.querySelector(".lm-s").textContent), wide: document.documentElement.scrollWidth > document.documentElement.clientWidth }));
    ok("Treaties: with the country known, three plain lines say when it joined each treaty", /Greece/.test(l.where) && l.lines.length === 3 && l.lines.every(x => /^19(61|71|88) treaty: Joined in \d{4}/.test(x)) && !l.wide, JSON.stringify(l));
    await shot(p, "390-law-greece");
    await p.click("#law-all > summary"); await p.fill("#law-filter", "Portu"); await p.waitForTimeout(300);
    ok("Treaties: all countries, with the filter", await p.evaluate(() => { const on = [...document.querySelectorAll("#law-list tr")].filter(tr => !tr.hidden); return on.length === 1 && /Portugal/.test(on[0].textContent); }));
    // the emergency numbers: both folds look alike; Find a drug: the start page's cards, two across on a phone
    await go(p, "#emergency", 600);
    ok("Emergency numbers: the two folds under the country look alike", await p.evaluate(() => { const d = [...document.querySelectorAll("#view-emergency details")]; return d.length === 2 && d.every(x => x.classList.contains("allc") && x.querySelector("summary .ask-i")); }));
    await go(p, "#substances", 700);
    const sub = await p.evaluate(() => { const c = [...document.querySelectorAll("#subgrid a.dcard")], r = c.slice(0, 3).map(x => x.getBoundingClientRect()); return { n: c.length, two: Math.abs(r[0].top - r[1].top) < 2 && r[2].top > r[0].top + 50, h: Math.round(document.getElementById("subgrid").getBoundingClientRect().height), old: document.querySelectorAll("#subgrid .dtile").length }; });
    ok("Find a drug: the start page's picture cards, two across on a phone", sub.n === 30 && sub.two && sub.h < 5200 && !sub.old, JSON.stringify(sub));
    await p.click('#filters .chip[data-cls="Opioids"]'); await p.waitForTimeout(300);
    ok("Find a drug: a family can be chosen", await p.evaluate(() => { const c = [...document.querySelectorAll("#subgrid a.dcard")]; return c.length >= 3 && c.length < 12 && c.every(x => /Opioids/.test(x.textContent)); }));
    await shot(p, "390-find-a-drug-opioids");
    const names = await p.evaluate(() => { const out = [], seen = new Set(); document.querySelectorAll("#menu a[data-view], footer.site a[href^='#']").forEach(a => { const v = a.dataset.view || a.getAttribute("href").slice(1); if (v === "review" || !document.getElementById("view-" + v) || a.dataset.email) return;
      const h1 = document.querySelector("#view-" + v + " h1"); out.push({ v, where: a.closest("#menu") ? "menu" : "footer", link: a.textContent.trim(), h1: h1 ? h1.textContent.trim() : "", title: PAGE_TITLES[v] }); seen.add(v); }); return out; });
    ok("every page has one name: the same in the menu, in the footer, on the page and in the tab's title", names.length >= 16 && names.every(x => x.link === x.h1 && x.h1 === x.title), names.filter(x => !(x.link === x.h1 && x.h1 === x.title)).map(x => x.where + " “" + x.link + "” / page “" + x.h1 + "” / title “" + x.title + "”").join(" | "));
    const eyebrows = await p.evaluate(() => [...document.querySelectorAll("main .view > .wrap .eyebrow, main .view .prose > .eyebrow")].filter(e => !e.closest("#view-review, #view-notfound")).map(e => e.textContent));
    ok("no page of the site starts with a small label above its title any more (one look for every page)", eyebrows.length === 0, eyebrows.join(" | "));
    await p.context().close();
  }

  /* ---- Site 2.15 (17 November 2026): simple first, the science one quiet tap away; every citation a link; a source opens where the reader
     is; Insight the same on every page, with the way back and the place always in view. The senior author's words are in docs/AUTOMATION.md
     (decision 29). ---- */
  for (const w of [390, 1280]) {
    const p = await open(ON, w);
    await p.evaluate(() => Promise.all(FULL_FILES.map(loadFull).concat(loadRefs())));
    // every citation of an answer's own source is a link, in every text the evidence shows (the two-author ones never were: "&amp;" was cut at its semicolon)
    const cit = await p.evaluate(() => { let texts = 0, links = 0; const left = [];
      for (const c of CLAIMS) { const refs = [...new Set(c.evidence.map(e => e.reference))].filter(r => refById[r]);
        const f = { statement: c.statement, reasoning: c.grade && c.grade.reasoning, population: c.population, exposure: c.exposure, comparator: c.comparator, outcome: c.outcome, magnitude: c.magnitude };
        if (c.debate) for (const k of ["evidence_yes", "evidence_no", "neither_can_show", "editors_reading", "what_would_settle_it"]) f["debate." + k] = c.debate[k];
        for (const [k, t] of Object.entries(f)) { if (!t) continue; texts++; const d = document.createElement("div"); d.innerHTML = sheetCites(String(t), refs); links += d.querySelectorAll("a").length;
          d.querySelectorAll("a").forEach(a => a.replaceWith("\u0001")); const bare = d.textContent;
          for (const r of refs) { const L = inTextLabel(refById[r], REFS), cut = L.lastIndexOf(", "), n = L.slice(0, cut), y = L.slice(cut + 2);
            for (const form of [L, n + " (" + y + ")", n.replace(" & ", " and ") + ", " + y, n.replace(" & ", " and ") + " (" + y + ")"]) if (cut > 0 && bare.includes(form)) left.push(c.id + " " + k + ": " + form); } } }
      return { texts, links, left }; });
    ok(w + " px: in every text the evidence shows, an answer's own source is a link wherever it is named (with “&”, with “and”, in a sentence)", cit.texts > 2500 && cit.links > 2650 && cit.left.length === 0, cit.texts + " texts, " + cit.links + " links; left: " + cit.left.slice(0, 6).join(" | "));
    await go(p, "#s-cannabis"); await p.evaluate(() => openEvidence("cl_can_deaths_attributed")); await p.waitForTimeout(900);
    // the debate: plain words first, the researchers' five texts under one closed fold; the citation the senior author named is a link
    const deb = await p.evaluate(() => { const b = document.getElementById("ev-debate"), full = b.querySelector("details.evd-full");
      const first = b.querySelector(".evd-plain, .evd-sides"), partsOutside = [...b.querySelectorAll(".evd-part")].filter(x => !x.closest(".evd-full")).length;
      full.open = true; const no = full.querySelector(".evd-part.no"); no.open = true;
      return { first: first ? first.textContent.trim().slice(0, 80) : "", closed: !b.querySelector("details.evd-full[open] ~ *") && true, parts: full.querySelectorAll(".evd-part").length, partsOutside, q: !!full.querySelector(".evd-q"),
        link: [...no.querySelectorAll("a.evcite")].some(a => a.textContent === "Launiainen & Ojanperä, 2014") }; });
    ok(w + " px: “Researchers disagree” starts in plain words; the researchers' question and five texts are under one fold; “(Launiainen & Ojanperä, 2014)” there is a link", deb.first.length > 20 && deb.parts === 5 && deb.partsOutside === 0 && deb.q && deb.link, JSON.stringify(deb));
    // a citation opens its source where the reader is: the line does not move; a second tap folds it away
    const inl = await p.evaluate(async () => { const a = [...document.querySelectorAll("#evsheet .evd-part.no a.evcite")].find(x => /Launiainen/.test(x.textContent)); a.scrollIntoView({ block: "center" });
      await new Promise(r => setTimeout(r, 80)); const y0 = a.getBoundingClientRect().top; a.click(); await new Promise(r => setTimeout(r, 120));
      const box = document.querySelector("#evsheet .ev-inl"), y1 = a.getBoundingClientRect().top;
      const out = { moved: Math.round(y1 - y0), open: !!box, after: box ? (box.previousElementSibling && box.previousElementSibling.contains(a)) || box.parentNode.contains(a) : false, expanded: a.getAttribute("aria-expanded"),
        plain: box ? !!box.querySelector(".ev-src-p") : false, kind: box ? (box.querySelector(".ev-src-kind") || {}).textContent || "" : "", sciClosed: box ? !box.querySelector(".ev-src-sci").open : false, sciHas: box ? box.querySelectorAll(".ev-src-sci .ev-quotes li, .ev-src-sci .ev-apa").length : 0 };
      a.click(); await new Promise(r => setTimeout(r, 120)); out.closedAgain = !document.querySelector("#evsheet .ev-inl"); out.moved2 = Math.round(a.getBoundingClientRect().top - y1); return out; });
    ok(w + " px: a citation opens its source under the line being read, in plain words first (what it adds, what kind of study), the science folded; the line does not move; a second tap folds it away",
      inl.open && inl.after && Math.abs(inl.moved) <= 2 && inl.expanded === "true" && inl.plain && /snapshot/i.test(inl.kind) && inl.sciClosed && inl.sciHas >= 2 && inl.closedAgain && Math.abs(inl.moved2) <= 2, JSON.stringify(inl));
    // the list of sources: plain first
    const src = await p.evaluate(() => { const li = document.getElementById("ev-src-drummer_2019"), d = li.querySelector("details"); d.open = true; const b = li.querySelector(".ev-src-b");
      return { order: [...b.children].map(x => x.className.split(" ").pop()), plain: b.querySelectorAll(".ev-src-p li").length, sci: !b.querySelector(".ev-src-sci").open, sub: (document.querySelector("#evsheet .ev-sub") || {}).textContent }; });
    ok(w + " px: a source in the list says what it adds to the answer and what kind of study it is; “Scientific detail” is the last thing and closed", src.plain === 3 && src.order[0] === "ev-src-p" && src.order[src.order.length - 1] === "ev-src-sci" && src.sci && /what it adds/.test(src.sub), JSON.stringify(src));
    await p.evaluate(() => closeEvidence()); await p.waitForTimeout(300);
    // a part of a drug page: a closed answer is its question and one line; its topics are signposts; many answers start with their topics
    await go(p, "#s-heroin/part-d-risk", 900);
    const part = await p.evaluate(() => { const sec = document.querySelector("#drug2 .sec:not([hidden])"), cards = [...sec.querySelectorAll("details.ask")], s = cards[0].querySelector(".ask-s"), lh = parseFloat(getComputedStyle(s).lineHeight);
      const closed = Math.round(s.getBoundingClientRect().height / lh); cards[0].open = true; const open = Math.round(s.getBoundingClientRect().height / lh); cards[0].open = false;
      return { cards: cards.length, closed, open, chips: [...sec.querySelectorAll(".tpj-b")].map(b => b.dataset.tp), heads: [...sec.querySelectorAll("h3.tp")].map(h => h.id), mw: getComputedStyle(cards[0].querySelector(".ask-m .mw")).position }; });
    ok(w + " px: on a part with many answers a closed answer shows one line of its answer (the whole of it when open), and the part starts with its topics, each a jump to its answers",
      part.cards >= 8 && part.closed === 1 && part.open >= (w < 600 ? 2 : 1) && part.chips.length >= 3 && part.chips.every(x => part.heads.includes(x)) && part.mw === "absolute", JSON.stringify(part));
    await p.click(".view.active .tpj-b:nth-of-type(3)"); await p.waitForTimeout(900);
    const jump = await p.evaluate(() => { const b = document.querySelectorAll(".view.active .tpj-b")[2], h = document.getElementById(b.dataset.tp), sm = document.querySelector(".view.active .secmenu"); return { top: Math.round(h.getBoundingClientRect().top), under: Math.round(sm.getBoundingClientRect().bottom) }; });
    ok(w + " px: a topic's button lands on that topic, just under the bars that stay", jump.top >= jump.under && jump.top <= jump.under + 40, JSON.stringify(jump));
    // the top bar: the same Insight on every page, where the reader is, and the way back once the Back line is out of sight
    await go(p, "#home"); await go(p, "#s-cannabis", 700); await go(p, "#s-heroin/part-d-risk", 900);
    await p.mouse.move(Math.round(w / 2), 400); await p.mouse.wheel(0, -6000); await p.waitForTimeout(500);   // (a reader's own scroll: a jump is kept in place until the reader moves)
    const bar0 = await p.evaluate(() => ({ y: Math.round(window.scrollY), here: document.getElementById("here").textContent, hereSeen: document.getElementById("here").getClientRects().length > 0, back: document.getElementById("barback").hidden, crumb: document.getElementById("crumb").textContent.trim(),
      pill: getComputedStyle(document.querySelector("#bar-search .sicon .ic-pill")).display, glass: getComputedStyle(document.querySelector("#bar-search .sicon .ic")).display, ph: document.getElementById("search").placeholder }));
    await p.mouse.wheel(0, 1200); await p.waitForTimeout(500);
    const bar1 = await p.evaluate(() => { const s = document.getElementById("search").getBoundingClientRect(), b = document.getElementById("barback"); return { boxTop: Math.round(s.top), boxSeen: s.top >= 0 && s.bottom <= 90 && s.width > 150, back: b.hidden, label: b.getAttribute("aria-label"), backSeen: b.getClientRects().length > 0 && b.getBoundingClientRect().top >= 0 }; });
    ok(w + " px: on every page the box is Insight's capsule and says so (“Ask Insight about heroin”), and the bar says where the reader is (“Heroin › Risks”)", bar0.pill === "block" && bar0.glass === "none" && bar0.ph === "Ask Insight about heroin" && bar0.here === "Heroin › Risks" && bar0.hereSeen, JSON.stringify(bar0));
    ok(w + " px: at the top of a page the Back line is the way back (no second Back beside it); further down, Insight is still in view and the bar holds the way back, named", bar0.back === true && /^Back to Cannabis/.test(bar0.crumb) && bar1.boxSeen && bar1.back === false && bar1.backSeen && /^Back to Cannabis/.test(bar1.label || ""), JSON.stringify([bar0.back, bar0.crumb, bar1]));
    await p.click("#barback"); await p.waitForTimeout(700);
    ok(w + " px: the bar's Back leads back", (await p.evaluate(() => location.hash)) === "#s-cannabis");
    // the empty box on a drug's page offers what people ask most about that drug
    await p.click("#search"); await p.waitForTimeout(600);
    const sug = await p.evaluate(() => ({ hint: (document.querySelector("#search-results .sr-hint") || {}).textContent || "", hrefs: [...document.querySelectorAll("#search-results a.sr-sug")].map(a => a.getAttribute("href")) }));
    ok(w + " px: before a word is typed, the box on the cannabis page offers what people ask most about cannabis", sug.hint === "Most asked about cannabis" && sug.hrefs.length >= 3 && sug.hrefs.every(h => h.startsWith("#s-cannabis/q-")), JSON.stringify(sug));
    await p.context().close();
  }

  ok("no error in any page's console", errors.length === 0, errors.slice(0, 5).join(" || "));
  await browser.close(); ON.server.close(); OFF.server.close();
  console.log(fail ? fail + " of " + (pass + fail) + " checks failed" : "All " + (pass + fail) + " checks passed");
  process.exit(fail ? 1 : 0);
})();
