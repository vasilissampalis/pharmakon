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
  const PAGES = ["#home", "#facts", "#quiz", "#numbers", "#checking", "#methods", "#about", "#howto", "#s-cannabis", "#substances", "#interactions", "#glossary", "#emergency", "#law"];
  for (const width of [1280, 390]) {
    const p = await open(ON, width), seen = [];
    for (const h of PAGES) {
      await go(p, h, 350);
      const brand = await box(p, ".topbar .brand"), menu = await box(p, "#menubtn"), h1 = await box(p, ".view.active h1");
      const col = await p.evaluate(() => { const v = document.querySelector(".view.active .wrap"); const r = v.getBoundingClientRect(), s = getComputedStyle(v); return Math.round(r.left + parseFloat(s.paddingLeft)); });
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
    await typeQ(p, "how can you die from alcohol");
    const before = await p.evaluate(() => ({ none: (document.querySelector(".sr-fit-none") || {}).textContent || "", note: (document.querySelector(".sr-fit .ask-note") || {}).textContent || "", insNote: (document.querySelector(".sr-note") || {}).textContent || "" }));
    ok("with the store on: the button says what it sends", /We haven.t checked exactly this yet/.test(before.none) && before.note === "Sends only this question. No name, no address.", JSON.stringify(before));
    await p.click(".sr-fit button[data-ask]"); await p.waitForTimeout(900);
    const said = await p.evaluate(() => (document.querySelector(".ask-said") || {}).textContent || "");
    ok("one tap: the page says it was sent", /^Sent\./.test(said), said);
    const kept = [...ON.kv.entries()].filter(([k]) => k.startsWith("q:")).map(([, v]) => JSON.parse(v));
    ok("the store holds the question's words, its page, the site version, the day and a count, and nothing else", kept.length === 1 && kept[0].q === "how can you die from alcohol" && Object.keys(kept[0]).sort().join() === "d,first,last,n,q,v" && /^\d+\.\d+\.\d+$/.test(kept[0].v), JSON.stringify(kept));
    await p.fill("#search", ""); await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    let list = await p.evaluate(() => { const b = document.getElementById("home-asked"); return { hidden: b.hidden, rows: [...b.querySelectorAll(".aq")].map(r => r.className + " | " + r.querySelector(".aq-k").textContent + " | " + r.querySelector(".aq-q").textContent) }; });
    ok("start page: Your questions lists it as being checked", !list.hidden && list.rows.length === 1 && /wait \| We are checking \| how can you die from alcohol/.test(list.rows[0]), JSON.stringify(list));
    await typeQ(p, "can you overdose on lsd"); await p.click(".sr-fit button[data-ask]"); await p.waitForTimeout(800);
    await p.fill("#search", ""); await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    list = await p.evaluate(() => [...document.querySelectorAll("#home-asked .aq-q")].map(e => e.textContent));
    ok("a second question is kept beside the first", list.length === 2 && list.includes("can you overdose on lsd"), JSON.stringify(list));
    await shot(p, "390-home-asked");
    await p.reload(); await p.waitForTimeout(900);
    ok("the list is still there after a reload", (await p.evaluate(() => document.querySelectorAll("#home-asked .aq").length)) === 2);
    await p.click("#home-asked .aq-x"); await p.waitForTimeout(300);
    ok("the cross takes a question off the list", (await p.evaluate(() => document.querySelectorAll("#home-asked .aq").length)) === 1);
    // answered: a question kept under an older version of the site, which the site can answer now
    await p.evaluate(() => { localStorage.setItem("pk-asked", JSON.stringify([{ k: "is weed addictive", q: "is weed addictive", d: "", t: Date.now() - 864e5, cv: "0.0.1", st: "wait", sent: 1 }, { k: "what is the capital of mongolia", q: "what is the capital of mongolia", d: "", t: Date.now(), cv: "0.0.1", st: "wait", sent: 1 }])); });
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
    await typeQ(p, "how can you die from alcohol");
    const note = await p.evaluate(() => ({ note: !!document.querySelector(".sr-fit .ask-note"), ins: (document.querySelector(".sr-note") || {}).textContent || "" }));
    ok("with the store off: no promise of sending, and Insight still says nothing typed leaves the device", !note.note && /Nothing you type leaves it/.test(note.ins), JSON.stringify(note));
    await p.click(".sr-fit button[data-ask]"); await p.waitForTimeout(900);
    const fb = await p.evaluate(() => ({ open: document.getElementById("report").classList.contains("open"), text: document.getElementById("report-message").value, kept: JSON.parse(localStorage.getItem("pk-asked") || "[]").map(x => x.q + "|" + x.sent) }));
    ok("with the store off: the email form opens with the question, and it is kept on the device", fb.open && fb.text === "how can you die from alcohol" && fb.kept.join() === "how can you die from alcohol|0", JSON.stringify(fb));
    await p.click("#report-close"); await p.fill("#search", ""); await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    const row = await p.evaluate(() => (document.querySelector("#home-asked .aq-k") || {}).textContent || "");
    ok("with the store off: the list says it is kept on this device, not that we are checking", row === "Kept on this device", row);
    await p.context().close();
  }

  ok("no error in any page's console", errors.length === 0, errors.slice(0, 5).join(" || "));
  await browser.close(); ON.server.close(); OFF.server.close();
  console.log(fail ? fail + " of " + (pass + fail) + " checks failed" : "All " + (pass + fail) + " checks passed");
  process.exit(fail ? 1 : 0);
})();
