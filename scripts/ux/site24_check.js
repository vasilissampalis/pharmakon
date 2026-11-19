// site24_check.js [--shots DIR]: what site 2.4 changed, checked on the built public site (site/public).
// The senior author's notes on 2.3.0 (15 November 2026): one top bar and one column on every page; a line that says where
// Back leads, and Back putting the page as it was; one Myth or fact deck, kept; every long page as a menu of sections,
// one open at a time; a clearer statistics page; "Ask us to check it" in one tap, with "Your questions" on the start page;
// the opioid pages speaking to a friend first; the email with the message in its subject.
// The question endpoint is the real one (site/worker/_worker.js) with a store kept in memory.
const http = require("http"), fs = require("fs"), path = require("path");
const { chromium } = require("playwright");
const ASKED_EPMC = [];   // (2.16) what the worker asked Europe PMC's stand-in
const LIVE_FILE = { d: null, asked: [] };   // (2.23) the system's state file, stood in for: what the worker reads for a reader who waits (GET /api/asked); null: there is none
const EPMC_BACK = { on: false };   // (2.21.1) the stand-in gives nothing on psilocybin until this is on: Europe PMC on an afternoon when it took 25 seconds a search
const ROOT = path.join(__dirname, "..", "..", "site", "public");
const SHOTS = process.argv.includes("--shots") ? process.argv[process.argv.indexOf("--shots") + 1] : null;
const TYPES = { ".html": "text/html; charset=utf-8", ".json": "application/json", ".webp": "image/webp", ".png": "image/png", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".css": "text/css", ".js": "text/javascript", ".mjs": "text/javascript", ".wasm": "application/wasm", ".txt": "text/plain; charset=utf-8", ".onnx": "application/octet-stream" };
let pass = 0, fail = 0;
const ok = (name, cond, extra) => { if (cond) { pass++; console.log("PASS " + name); } else { fail++; console.log("FAIL " + name + (extra ? " | " + String(extra).slice(0, 400) : "")); } };

(async () => {
  const workerModule = await import("file://" + path.join(__dirname, "..", "..", "site", "worker", "_worker.js")), worker = workerModule.default, liveForget = workerModule.liveForget;
  const liveSet = d => { LIVE_FILE.d = d; liveForget(); };   // (2.23) the stand-in for the system's state file changes: the server reads it afresh
  // one server per state of the store: on (a store kept in memory) and off (no store bound: the worker answers 503)
  const serve = (withStore) => new Promise(resolve => {
    const kv = new Map(), store = { get: async (k, how) => { const v = kv.get(k); return v == null ? null : how === "json" ? JSON.parse(v) : v; }, put: async (k, v) => { kv.set(k, v); } };
    // (2.16) Europe PMC, stood in for: the worker asks it through env.FETCH here; what it was asked is kept for the check. (2.20) Two papers about the drug,
    // with summaries: the server takes each paper's own words on the question from them by rule
    // (2.20, after the sixth trial) and a slow search, as Europe PMC has them: the most cited papers on ketamine take four and a half seconds the first time they are
    // asked for; after that their reply is there at once (on the site Cloudflare keeps it)
    const SLOW = new Map(), K = (i, title) => ({ title, authorString: "Delta D.", journalTitle: "Journal of Tests", pubYear: String(2010 + i), pmid: String(900 + i), isOpenAccess: "N", pubType: "journal article", abstractText: "" });
    const epmc = async url => { ASKED_EPMC.push(decodeURIComponent(String(url)));
      const s = decodeURIComponent(String(url));
      if (/TITLE:"mescaline"/.test(s)) return new Response("busy", { status: 503 });   // (2.21.1) the index says no: that is not "nothing was found"
      if (/TITLE:"psilocybin"/.test(s)) { while (!EPMC_BACK.on) await new Promise(r => setTimeout(r, 150));   // (2.21.1) a search that does not come back
        return new Response(JSON.stringify({ resultList: { result: [K(5, "Psilocybin and eye colour: a paper that came late"), K(6, "Psilocybin and the eye: another paper that came late")] } }), { status: 200, headers: { "content-type": "application/json" } }); }
      if (/TITLE:"ketamine"/.test(s)) { const q = (s.split(/[?&]query=/)[1] || "").split("&")[0], cited = /sort=CITED/.test(s);
        if (cited) { if (!SLOW.has(q)) SLOW.set(q, Date.now() + 4500); const wait = SLOW.get(q) - Date.now(); if (wait > 0) await new Promise(r => setTimeout(r, wait)); }
        const list = cited ? [K(1, "Ketamine and eye colour: the most cited paper"), K(2, "Ketamine and eye colour: a newer paper")] : /sort=P_PDATE_D/.test(s) ? [K(2, "Ketamine and eye colour: a newer paper")] : [K(2, "Ketamine and eye colour: a newer paper"), K(3, "A paper that mentions ketamine and eye colour"), K(4, "Another paper that mentions ketamine and eye colour")];
        return new Response(JSON.stringify({ resultList: { result: list } }), { status: 200, headers: { "content-type": "application/json" } }); }
      return new Response(JSON.stringify({ resultList: { result: [
      { title: "A review of <i>LSD</i> and the eye.", authorString: "Alpha A, Beta B.", journalTitle: "Journal of Tests", pubYear: "2021", doi: "10.1234/test.2021.1", pmid: "111", isOpenAccess: "Y", pubType: "review; journal article",
        abstractText: "This review brings together what studies in people report about the drug and the eye. In the studies reviewed, the colour of the iris did not change in any volunteer given LSD, while the pupils grew wider for several hours. Reports of lasting changes to the eye were not found. More work with careful measurement is needed before firm statements can be made." },
      { title: "LSD and the eye: a trial in forty volunteers", authorString: "Gamma C.", journalTitle: "Trials Today", pubYear: "2013", pmid: "222", isOpenAccess: "N", pubType: "randomized controlled trial; journal article",
        abstractText: "Forty healthy volunteers took part in a placebo-controlled trial with photographs of the eye taken before and after. After the drug, the pupils of the forty volunteers grew wider, and the colour of the eye stayed the same after LSD on every photograph. The size of the pupil returned to its starting value by the next morning in all who took part." }] } }), { status: 200, headers: { "content-type": "application/json" } }); };
    const liveFetch = async url => { LIVE_FILE.asked.push(String(url)); return LIVE_FILE.d ? new Response(JSON.stringify(LIVE_FILE.d), { status: 200 }) : new Response("no such file", { status: 404 }); };
    const env = Object.assign({ ASSETS: { fetch: async () => new Response("", { status: 404 }) }, FETCH: epmc, LIVE_FETCH: liveFetch }, withStore ? { QUESTIONS: store } : {});
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
    const can = await p.evaluate(() => { const q = (document.querySelector("#quizpage .mf-front .mf-q") || {}).textContent || ""; return { n: document.querySelector("#quizpage .mf-front .qz2-score").textContent, k: document.querySelector("#quizpage .qz2-k").textContent, mine: mfPagePool("cannabis").some(x => x.q === q), pressed: document.querySelector('#mf-pick [data-mfp="cannabis"]').getAttribute("aria-pressed") }; });
    // (the cannabis deck is the cards of the cannabis page: its own answers, and the mixing and test-kit answers that page shows: mfPagePool)
    ok("Myth or fact? page: a drug can be chosen, and its own deck starts (its cards drawn at random since 2.23.1: the first is one of that drug's page)", /^1 of \d+$/.test(can.n) && can.mine && can.pressed === "true", JSON.stringify(can));
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
    // (site 2.17; the senior author: "it should send the question immediately in every instance and the user should be notified") a question the site
    // has no answer to is sent by itself, and the page says so in the same place; nothing is pressed
    const before = await p.evaluate(() => ({ none: (document.querySelector(".sr-fit-none") || {}).textContent || "", btn: !!document.querySelector(".sr-fit button[data-ask]"), insNote: (document.querySelector(".sr-note") || {}).textContent || "" }));
    ok("with the store on: no button to press, and the line at the head of the results says that a question we cannot answer is sent by itself", /We haven.t checked exactly this yet/.test(before.none) && !before.btn && /^Runs on your (phone|computer)\. A question we have no answer to is sent on by itself, so that it gets answered: no name, no address\.$/.test(before.insNote.trim()), JSON.stringify(before));
    const early = [...ON.kv.keys()].filter(k => /^a?q:/.test(k)).length;
    await p.waitForSelector(".sr-fit .ask-auto-said", { timeout: 9000 }).catch(() => {});
    const said = await p.evaluate(() => (document.querySelector(".sr-fit .ask-auto-said") || {}).textContent || "");
    ok("after a moment (not while it is being typed) the question is sent by itself, and the page says so in the same place, with a way to stop it", early === 0 && said === "Sent. You can stay or come back: it is kept under “Your questions” on the start page. Don’t send mine", early + " | " + said);   // (2.23: what the system is doing stands under this line, so the line itself is shorter)
    const kept = [...ON.kv.entries()].filter(([k]) => k.startsWith("aq:")).map(([, v]) => JSON.parse(v));
    ok("the store holds it apart, marked as sent by the page: the question's words, its page, the site version, the day and a count, and nothing else", kept.length === 1 && kept[0].q === "is modafinil safe" && kept[0].a === 1 && Object.keys(kept[0]).sort().join() === "a,d,dn,first,last,n,q,v" && /^\d+\.\d+\.\d+$/.test(kept[0].v) && ![...ON.kv.keys()].some(k => k.startsWith("q:")), JSON.stringify(kept));
    await p.fill("#search", ""); await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    let list = await p.evaluate(() => { const b = document.getElementById("home-asked"); return { hidden: b.hidden, bar: (b.querySelector(".you-bar") || {}).textContent || "", words: /modafinil/.test(b.textContent), rows: [...document.querySelectorAll("#yousheet .aq")].map(r => r.className + " | " + r.querySelector(".aq-k").textContent + " | " + r.querySelector(".aq-q").textContent) }; });
    ok("start page (2.21): one quiet line, Your questions, with how many are in progress and no question's own words", !list.hidden && list.bar === "Your questions1 in progress" && !list.words, JSON.stringify(list));
    ok("its panel lists the question as sent and being checked", list.rows.length === 1 && /wait \| Sent\. We are checking · sent less than an hour ago \| is modafinil safe/.test(list.rows[0]), JSON.stringify(list));   // (2.15.2: a row says how long ago it was sent)
    ok("the list says where it is kept, and that a question we had no answer to is sent by itself (and where that is switched off)", await p.evaluate(() => (document.querySelector("#yousheet .ev-eye") || {}).textContent === "Kept on this device only" && (document.querySelector("#yousheet .aq-note") || {}).textContent === "A question we had no answer to is sent on by itself to be answered (About us, Privacy switches that off). It turns green here when it is answered."));
    // (2.21) the line opens the panel at the right, built like the evidence of an answer: the same sheet, a Back button, a title; Back and the phone's Back close it
    await p.click("#home-asked .you-bar"); await p.waitForTimeout(400);
    const pan = await p.evaluate(() => { const s = document.getElementById("yousheet"), pn = s.querySelector(".panel"), r = pn.getBoundingClientRect(); return { open: s.classList.contains("open") && YOU.open, cls: s.className, back: (pn.querySelector(".ev-bar .ev-back") || {}).textContent || "", h: (pn.querySelector("#you-title") || {}).textContent, past: (pn.querySelector("#you-past") || {}).textContent, right: Math.round(innerWidth - r.right), focus: document.activeElement === pn.querySelector(".ev-back"), wide: document.documentElement.scrollWidth > innerWidth }; });
    ok("the line opens a panel at the right, in the frame of the evidence sheet (Back, a title), with the questions and then the past searches", pan.open && /drawer evsheet yousheet/.test(pan.cls) && pan.back === "Back" && pan.h === "Your questions" && pan.past === "Past searches" && pan.right === 0 && pan.focus && !pan.wide, JSON.stringify(pan));
    await p.goBack(); await p.waitForTimeout(400);
    ok("the phone's Back closes the panel and stays on the start page", await p.evaluate(() => !YOU.open && !document.getElementById("yousheet").classList.contains("open") && document.getElementById("view-home").classList.contains("active")));
    await p.click("#home-asked .you-bar"); await p.waitForTimeout(400);
    // (2.9; the senior author, of his two sent questions: "i cannot click on them to see the answer") a question that waits opens too
    await p.click("#yousheet .aq.wait button.aq-look"); await p.waitForTimeout(1100);
    const lk = await p.evaluate(() => ({ value: document.getElementById("search").value, open: !document.getElementById("search-results").hidden, go: (document.querySelector("#yousheet .aq.wait .aq-go") || {}).textContent || "", shut: !YOU.open, fit: !!document.querySelector("#search-results .sr-fit, #search-results a, #search-results .sr-get") }));
    ok("a question that waits can be opened: its row asks it again in the box, which shows what the site has on it so far", lk.value === "is modafinil safe" && lk.open && lk.shut && lk.fit && /^See what we have so far/.test(lk.go), JSON.stringify(lk));
    await p.fill("#search", ""); await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    // a pause in the middle of a sentence: the beginning that went out leaves the reader's list when the whole question follows
    const sentFor = q => p.waitForFunction(q => { const f = document.querySelector("#search-results .sr-fit"); return f && f.dataset.q === q && f.querySelector(".ask-auto-said"); }, q, { timeout: 12000 }).then(() => true, () => false);
    await typeQ(p, "is modafinil bad"); const part = await sentFor("is modafinil bad"); await typeQ(p, "is modafinil bad for the liver"); const whole = await sentFor("is modafinil bad for the liver");
    await p.fill("#search", ""); await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    list = await p.evaluate(() => [...document.querySelectorAll("#yousheet .aq-q")].map(e => e.textContent));
    ok("a second question is kept beside the first; a beginning that was sent a moment before the whole question does not stay on the list", part && whole && list.length === 2 && list.includes("is modafinil bad for the liver") && !list.includes("is modafinil bad") && [...ON.kv.keys()].filter(k => k.startsWith("aq:")).length === 3, JSON.stringify(list) + " " + [...ON.kv.keys()].join(","));
    // Enter sends at once (the sheet); "Don't send mine" turns it off on this device, and the way to send by hand is back
    await typeQ(p, "does modafinil cause hair loss"); await p.keyboard.press("Enter"); await p.waitForSelector("#evsheet.open .ins-none .ask-auto-said", { timeout: 6000 }).catch(() => {});
    const atOnce = await p.evaluate(() => ({ said: (document.querySelector("#evsheet .ins-none .ask-auto-said") || {}).textContent || "", btn: !!document.querySelector("#evsheet .ins-none button[data-ask]") }));
    ok("Enter: the sheet sends the question at once and says so", /^Sent\. /.test(atOnce.said) && !atOnce.btn && [...ON.kv.keys()].filter(k => k.startsWith("aq:")).length === 4, JSON.stringify(atOnce));
    await p.click("#evsheet .ins-none button[data-auto-stop]"); await p.waitForTimeout(200);
    const stopped = await p.evaluate(() => ({ text: (document.querySelector("#evsheet .ins-none .ask-auto-said") || {}).textContent || "", off: localStorage.getItem("pk-auto") }));
    await p.keyboard.press("Escape"); await p.waitForTimeout(400); await p.fill("#search", ""); await p.waitForTimeout(100);
    await typeQ(p, "does modafinil make you smarter"); await p.waitForTimeout(3200);
    const byHand = await p.evaluate(() => ({ btn: !!document.querySelector(".sr-fit button[data-ask]"), note: (document.querySelector(".sr-fit .ask-note") || {}).textContent || "", auto: !!document.querySelector(".sr-fit .ask-auto-said"), line: (document.querySelector(".sr-note") || {}).textContent || "" }));
    ok("“Don’t send mine” switches it off on this device and says so; from then on nothing is sent by itself and the button to send by hand is back, saying what it sends",
      /^Off on this device: from now on nothing is sent or looked up by itself/.test(stopped.text) && stopped.off === "0" && byHand.btn && byHand.note === "Sends only this question. No name, no address." && !byHand.auto && /What you type stays on it, unless you ask us to check a question\.$/.test(byHand.line) && [...ON.kv.keys()].filter(k => k.startsWith("aq:")).length === 4, JSON.stringify(stopped) + " " + JSON.stringify(byHand));
    await p.click(".sr-fit button[data-ask]"); await p.waitForTimeout(900);
    const saidHand = await p.evaluate(() => (document.querySelector(".sr-fit .ask-said") || {}).textContent || ""), keptHand = [...ON.kv.entries()].filter(([k]) => k.startsWith("q:")).map(([, v]) => JSON.parse(v));
    ok("sent by hand: the page says it was sent, promises only what is true (no answer within the hour until the half-hourly run keeps it), and the store keeps it among the questions people chose to send",
      saidHand === "Sent. It is worked on until an answer passes the checks. It turns green under “Your questions” on the start page." && await p.evaluate(() => AUTO_LOOP === false) && keptHand.length === 1 && keptHand[0].q === "does modafinil make you smarter" && Object.keys(keptHand[0]).sort().join() === "d,dn,first,last,n,q,v", saidHand + " " + JSON.stringify(keptHand));
    await p.evaluate(() => { localStorage.removeItem("pk-auto"); const a = JSON.parse(localStorage.getItem("pk-asked") || "[]").filter(x => /modafinil safe|for the liver/.test(x.q)); localStorage.setItem("pk-asked", JSON.stringify(a)); });
    await p.reload(); await p.waitForTimeout(900);
    await p.fill("#search", ""); await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    await shot(p, "390-home-asked");
    await p.reload(); await p.waitForTimeout(900);
    ok("the list is still there after a reload", (await p.evaluate(() => document.querySelectorAll("#yousheet .aq").length)) === 2);
    await p.click("#home-asked .you-bar"); await p.waitForTimeout(400); await shot(p, "390-you-panel");
    await p.click("#yousheet .aq-x"); await p.waitForTimeout(300);
    ok("the cross takes a question off the list (the panel stays open)", (await p.evaluate(() => document.querySelectorAll("#yousheet .aq").length === 1 && YOU.open)));
    await p.click("#yousheet .ev-back"); await p.waitForTimeout(400);
    // answered: a question kept under an older version of the site, which the site can answer now
    // (2.5: the first one is a question the reader asked to be told about from our list; it turns green the same way)
    await p.evaluate(() => { localStorage.setItem("pk-asked", JSON.stringify([{ k: "is weed addictive", q: "is weed addictive", d: "", t: Date.now() - 864e5, cv: "0.0.1", st: "wait", sent: 1, w: "w_0000" }, { k: "what is the capital of mongolia", q: "what is the capital of mongolia", d: "", t: Date.now(), cv: "0.0.1", st: "wait", sent: 1 },
      // (2.15.2; the senior author, of "do gay people" on his list: "why are non drug questions included... bad design") a question that is not about drugs, and a beginning
      // that is not a whole question, leave the list; a drug question the site cannot answer yet stays
      { k: "do gay people", q: "do gay people", d: "", t: Date.now() - 2e7, cv: "0.0.1", st: "wait", sent: 1, u: 1 }, { k: "does lsd change your eye colour", q: "does lsd change your eye colour", d: "", t: Date.now() - 3e7, cv: "0.0.1", st: "wait", sent: 1 }])); });
    await p.reload(); await p.waitForSelector("#yousheet .aq.ans", { state: "attached", timeout: 90000 }); await p.waitForTimeout(1500);
    const ans = await p.evaluate(() => [...document.querySelectorAll("#yousheet .aq")].map(r => ({ cls: r.className, k: r.querySelector(".aq-k").textContent, q: r.querySelector(".aq-q").textContent, href: (r.querySelector("a.aq-a") || {}).getAttribute ? r.querySelector("a.aq-a").getAttribute("href") : null })));
    ok("a kept question that the site can answer now shows first, in green, as Answered; the other is still being checked", ans.length === 2 && /ans/.test(ans[0].cls) && ans[0].k === "Answered" && ans[0].q === "is weed addictive" && /^#/.test(ans[0].href || "") && /wait/.test(ans[1].cls) && ans[1].q === "does lsd change your eye colour" && /sent \d+ hours ago$/.test(ans[1].k), JSON.stringify(ans));
    ok("a question that is not about drugs, and a beginning that is not a whole question, are not kept on the list", !ans.some(x => /mongolia|gay/.test(x.q)) && (await p.evaluate(() => JSON.parse(localStorage.getItem("pk-asked")).map(x => x.k).join("|"))) === "is weed addictive|does lsd change your eye colour", JSON.stringify(ans));
    ok("the line on the start page turns green and says so", await p.evaluate(() => { const b = document.querySelector("#home-asked .you-bar"); return !!b && b.classList.contains("has-ans") && b.textContent === "Your questions1 answered · 1 in progress"; }));
    await shot(p, "390-home-answered");
    await p.click("#home-asked .you-bar"); await p.waitForTimeout(400);
    await p.click("#yousheet .aq.ans a.aq-a"); await p.waitForTimeout(1100);
    const opened = await p.evaluate(() => ({ sheet: document.getElementById("evsheet").classList.contains("open"), left: JSON.parse(localStorage.getItem("pk-asked")).map(x => x.k) }));
    ok("reading it opens the answer over the page and takes it off the list", opened.sheet && opened.left.join() === "does lsd change your eye colour", JSON.stringify(opened));
    await p.context().close();
  }
  {
    const p = await open(OFF, 390);
    await p.waitForTimeout(1500);
    await typeQ(p, "is modafinil safe");
    const note = await p.evaluate(() => ({ note: !!document.querySelector(".sr-fit .ask-note"), ins: (document.querySelector(".sr-note") || {}).textContent || "" }));
    ok("with the store off: no promise of sending; Insight's line says what does go out (the drug's name and key words, to look up research)", !note.note && /^Runs on your (phone|computer)\. With no answer of ours, only the drug’s name and a few key words go out, to look up research\.$/.test(note.ins.trim()), JSON.stringify(note));
    await p.click(".sr-fit button[data-ask]"); await p.waitForTimeout(900);
    const fb = await p.evaluate(() => ({ open: document.getElementById("report").classList.contains("open"), text: document.getElementById("report-message").value, kept: JSON.parse(localStorage.getItem("pk-asked") || "[]").map(x => x.q + "|" + x.sent) }));
    ok("with the store off: the email form opens with the question, and it is kept on the device", fb.open && fb.text === "is modafinil safe" && fb.kept.join() === "is modafinil safe|0", JSON.stringify(fb));
    await p.click("#report-close"); await p.fill("#search", ""); await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    const row = await p.evaluate(() => { const r = document.querySelector("#yousheet .aq"); return r ? { cls: r.className, k: r.querySelector(".aq-k").textContent, send: (r.querySelector("button.aq-send") || {}).textContent || "", note: (document.querySelector("#yousheet .aq-note") || {}).textContent || "", eye: (document.querySelector("#yousheet .ev-eye") || {}).textContent || "", bar: (document.querySelector("#home-asked .you-bar") || {}).textContent || "" } : null; });
    ok("with the store off: the list says Not sent, where the list is kept, and offers to send it", row && /unsent/.test(row.cls) && row.k === "Not sent" && row.send === "Send it to us" && row.eye === "Kept on this device only" && /^We see a question only if you send it\./.test(row.note) && row.bar === "Your questions1 not sent", JSON.stringify(row));
    await p.click("#home-asked .you-bar"); await p.waitForTimeout(400);
    await p.click("#yousheet button.aq-send"); await p.waitForTimeout(1100);
    const again = await p.evaluate(() => ({ open: document.getElementById("report").classList.contains("open"), text: document.getElementById("report-message").value, how: (document.querySelector("#report .fb-how") || {}).textContent || "", head: document.querySelector("#report .fb-head p").textContent, k: document.querySelector("#yousheet .aq-k").textContent }));
    ok("with the store off: Send it to us opens the email form with the question; the form says nothing is sent until Send is pressed there; the row stays Not sent", again.open && again.text === "is modafinil safe" && /Nothing is sent until you press Send there/.test(again.how) && again.k === "Not sent", JSON.stringify(again));
    ok("the form's head no longer says that the most asked questions are answered first (nor does any page)", again.head === "Both reach the editors. We read everything." && await p.evaluate(() => { location.hash = "#s-cannabis"; return new Promise(r => setTimeout(() => r(!/ask most are answered first/.test([...document.querySelectorAll("main, #report, #menu, footer.site")].map(e => e.textContent).join(" "))), 500)); }), again.head);   // (the page's text, not its script)
    await p.context().close();
  }
  {
    // a question kept while sending was off can be sent from the list once sending is on
    const p = await open(ON, 390);
    await p.evaluate(() => localStorage.setItem("pk-asked", JSON.stringify([{ k: "does cannabis cause cancer", q: "does cannabis cause cancer", d: "", t: Date.now(), cv: SITE_VERSION, st: "wait", sent: 0 }])));
    await p.reload(); await p.waitForTimeout(1600);
    const before = await p.evaluate(() => (document.querySelector("#yousheet .aq-k") || {}).textContent || "");
    await p.click("#home-asked .you-bar"); await p.waitForTimeout(400);
    await p.click("#yousheet button.aq-send"); await p.waitForTimeout(900);
    const after = await p.evaluate(() => ({ k: (document.querySelector("#yousheet .aq-k") || {}).textContent || "", form: document.getElementById("report").classList.contains("open"), send: !!document.querySelector("#yousheet button.aq-send") }));
    const stored = [...ON.kv.entries()].filter(([k]) => k.startsWith("q:")).map(([, v]) => JSON.parse(v).q);
    ok("with the store on: a question that was not sent is sent from the list in one tap, and the row says so", before === "Not sent" && after.k === "Sent. We are checking · sent less than an hour ago" && !after.form && !after.send && stored.includes("does cannabis cause cancer"), JSON.stringify({ before, after, stored }));
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
    // (2.17: "the user should be notified") the listed question is put on the reader's own list by itself, after the same moment; the card then says so
    const onCard = await p.evaluate(() => ({ btn: !!document.querySelector("#search-results .sr-want button[data-want-keep]"), said: (document.querySelector("#search-results .sr-want .ask-said") || {}).textContent || "" }));
    await p.fill("#search", ""); await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    const row = await p.evaluate(() => { const r = document.querySelector("#yousheet .aq"); return r ? r.className + " | " + r.querySelector(".aq-k").textContent + " | " + r.querySelector(".aq-q").textContent : ""; });
    ok("a listed question goes on the reader's own list by itself: Your questions keeps the LISTED question (never the words typed), as On our list, and the card says so in place of its button",
      /onlist \| (?:In line\. Not tried yet|Being answered|No answer passed the checks yet\. Trying again|Written\. An editor reads this kind first|Searched\. What is published says nothing on it yet|Searched\. Nothing we can read is published on it yet) · asked less than an hour ago \| How can you die from alcohol\?$/.test(row) && !onCard.btn && onCard.said === "It is on your list: we will tell you on this device when it is answered." && (await p.evaluate(() => JSON.parse(localStorage.getItem("pk-asked")).map(x => x.q).join("|"))) === "How can you die from alcohol?" && !reqs.some(x => /POST api\/ask/.test(x)), row + " " + JSON.stringify(onCard));   // (2.15.2: what our system has done with it so far, and since when)
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
    ok("the list has its own page: every listed question, the one already kept marked so, nothing wider than the phone", pg.title === "On our list · Pharmakon" && pg.h1 === "On our list" && pg.rows === pg.listed && pg.rows >= 30 && pg.kept.slice().sort().join("|") === ["How can you die from alcohol?", other.q].sort().join("|") && !pg.wide, JSON.stringify(pg));   // (2.17: the one the sheet was opened on with Enter was put on the list by itself too)
    await shot(p, "390-wanted");
    await p.click("#wanted-list .wl-b"); await p.waitForTimeout(500); w = wkeys(ON);
    ok("on that page, Tell me when it is answered counts the item and keeps it in Your questions", w.some(([k, v]) => k === "w:" + pg.first && v.n === 1) && (await p.evaluate(() => JSON.parse(localStorage.getItem("pk-asked")).filter(x => x.w).length)) === 3 && /^We will tell you on this device/.test(await p.evaluate(() => (document.querySelector("#wanted-list .ask-said") || {}).textContent || "")), JSON.stringify(w));
    // the switch in Privacy
    await go(p, "#about/part-a-privacy", 700);
    const sw = await p.evaluate(() => { const s = document.getElementById("count-switch"); return { there: !!(s && s.offsetParent), checked: s.checked, disabled: s.disabled, state: document.getElementById("count-state").textContent, text: s.closest("li").textContent.replace(/\s+/g, " ").slice(0, 160), old: /no tracking or analytics/.test(document.getElementById("view-about").textContent) }; });
    ok("Privacy says what is counted, with a switch that is on, and no longer says “no tracking or analytics”", sw.there && sw.checked && !sw.disabled && sw.state === "On." && /^One thing is counted\./.test(sw.text) && !sw.old, JSON.stringify(sw));
    await shot(p, "390-privacy");
    await p.click("#count-switch"); await p.waitForTimeout(200);
    const off = await p.evaluate(() => ({ stored: localStorage.getItem("pk-count"), state: document.getElementById("count-state").textContent, checked: document.getElementById("count-switch").checked }));
    ok("switching it off is kept on the device", off.stored === "0" && off.state === "Off on this device." && !off.checked, JSON.stringify(off));
    const nBefore = reqs.filter(x => /api\/want/.test(x)).length;
    // (a listed question about dying, which waits for a person and so stays listed: "What is a K-hole?" was answered by the lane on 19 November)
    await go(p, "#home", 400); await typeW(p, "how does an opioid overdose kill you"); const c2 = await card(p); await p.waitForTimeout(3000);
    ok("with counting switched off: the card still helps, says nothing about counting, and nothing is sent", c2 && !c2.count && !c2.note && c2.q === "How does an opioid overdose actually kill you?" && reqs.filter(x => /api\/want/.test(x)).length === nBefore, JSON.stringify(c2));
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
    const bar0 = await p.evaluate(() => ({ y: Math.round(window.scrollY), here: document.getElementById("here").textContent, hereSeen: document.getElementById("here").getClientRects().length > 0 && getComputedStyle(document.getElementById("here")).visibility !== "hidden", back: document.getElementById("barback").hidden, crumb: document.getElementById("crumb").textContent.trim(),
      pill: getComputedStyle(document.querySelector("#bar-search .sicon .ic-pill")).display, glass: getComputedStyle(document.querySelector("#bar-search .sicon .ic")).display, ph: document.getElementById("search").placeholder }));
    await p.mouse.wheel(0, 1200); await p.waitForTimeout(500);
    const bar1 = await p.evaluate(() => { const s = document.getElementById("search").getBoundingClientRect(), b = document.getElementById("barback"), h = document.getElementById("here"); return { boxTop: Math.round(s.top), boxSeen: s.top >= 0 && s.bottom <= 90 && s.width > 150, back: b.hidden, label: b.getAttribute("aria-label"), backSeen: b.getClientRects().length > 0 && b.getBoundingClientRect().top >= 0, here: h.textContent, hereSeen: h.getClientRects().length > 0 && getComputedStyle(h).visibility !== "hidden" }; });
    // (2.23.1; the senior author, 19 November 2026, 10:21: the page's name is not said twice: in the bar only once the page's own title is out of sight)
    ok(w + " px: on every page the box is Insight's capsule and says so (“Ask Insight about heroin”); at the top of a page the bar does not repeat the page's own title, and further down it says where the reader is (“Heroin › Risks”)",
      bar0.pill === "block" && bar0.glass === "none" && bar0.ph === "Ask Insight about heroin" && bar0.here === "Heroin › Risks" && !bar0.hereSeen && bar1.here === "Heroin › Risks" && (bar1.hereSeen || w < 600), JSON.stringify([bar0, bar1.here, bar1.hereSeen]));
    ok(w + " px: at the top of a page the Back line is the way back (no second Back beside it); further down, Insight is still in view and the bar holds the way back, named", bar0.back === true && /^Back to Cannabis/.test(bar0.crumb) && bar1.boxSeen && bar1.back === false && bar1.backSeen && /^Back to Cannabis/.test(bar1.label || ""), JSON.stringify([bar0.back, bar0.crumb, bar1]));
    await p.click("#barback"); await p.waitForTimeout(700);
    ok(w + " px: the bar's Back leads back", (await p.evaluate(() => location.hash)) === "#s-cannabis");
    // (2.23.1, decision 35) a form with no photo of its own shows the picture our system found for it (once the editor looked at it), with its line and its credit
    // (the picture here is one of kanna's, which the site publishes: only the drawing is tested)
    await p.evaluate(() => { AUTO_FORMS.lsd = { gel: { file: "kanna-1", m: [800, 600], t: [400, 300], maker: "Ann Lee", licence: "CC BY 4.0", licence_url: "https://creativecommons.org/licenses/by/4.0/", page: "https://commons.wikimedia.org/wiki/File:Window_pane_LSD.jpg", src: "commons" } }; });
    await go(p, "#home"); await go(p, "#s-lsd/part-d-looks", 900);
    const fa = await p.evaluate(() => { const li = [...document.querySelectorAll("#d-looks li.look")], g = li.find(x => /Gelatine squares/.test(x.textContent)), b = li.find(x => /Blotters/.test(x.textContent)), m = li.find(x => /Microdots/.test(x.textContent)), cr = document.querySelector("#d-looks details.look-credits");
      return { img: g && g.querySelector("img") ? g.querySelector("img").getAttribute("src") + " | " + g.querySelector("img").alt : "", line: g ? (g.querySelector(".look-auto-t") || {}).textContent || "" : "", blotLine: b ? !!b.querySelector(".look-auto-t") : null,
        micro: m ? !!m.querySelector("img") : null, credit: cr ? cr.textContent.replace(/\s+/g, " ") : "", links: cr ? [...cr.querySelectorAll("a")].map(a => a.href) : [] }; });
    ok(w + " px (2.23.1): a form with no photo of its own (LSD's gelatine squares) shows the picture found for it, and its maker, licence and file page among the credits; a form with its own photo, or with none found, is as before",
      fa.img === "img/auto/kanna-1-t.webp | Gelatine squares: an example" && fa.line === "" && fa.blotLine === false && fa.micro === false &&
        /Gelatine squares, Ann Lee, CC BY 4\.0, via Wikimedia Commons/.test(fa.credit) && fa.links.includes("https://commons.wikimedia.org/wiki/File:Window_pane_LSD.jpg") && fa.links.includes("https://creativecommons.org/licenses/by/4.0/"), JSON.stringify(fa));
    await p.evaluate(() => { delete AUTO_FORMS.lsd; });
    // (2.23.1) on a page the system started, a picture from a Commons category that is not a species: an example of the drug, said to come from Wikimedia Commons
    const th = await p.evaluate(() => { AUTO_PICS["zz-test"] = [{ file: "kanna-1", m: [800, 600], t: [400, 300], species: "Anabolic steroids", kind: "thing", maker: "", licence: "Public domain", licence_url: "", page: "https://commons.wikimedia.org/wiki/File:X.jpg", src: "commons", country: "" }];
      const d = document.createElement("div"); d.innerHTML = autoLooksHtml("zz-test"); delete AUTO_PICS["zz-test"];
      return { t: (d.querySelector(".look-t") || {}).textContent || "", alt: (d.querySelector("img") || {}).alt || "", credit: ((d.querySelector(".look-credits p") || {}).textContent || ""), href: (d.querySelector(".look-credits a") || {}).href || "", note: (d.querySelector(".auto-picnote") || {}).textContent || "" }; });
    ok(w + " px (2.23.1): a started page's picture from Wikimedia Commons that shows the drug itself is “An example”, credited to its file page (public domain, so no licence link), and the note says only where it comes from",
      th.t === "An exampleAnabolic steroids" && th.alt === "An example of Anabolic steroids" && th.credit === "Photo 1: Wikimedia Commons, public domain." && th.href === "https://commons.wikimedia.org/wiki/File:X.jpg" &&
        /^From Wikimedia Commons\. They are examples: the same drug can look different, and different drugs can look the same\./.test(th.note) && !/our system|checked/i.test(th.note), JSON.stringify(th));
    await go(p, "#home"); await go(p, "#s-cannabis", 900);   // (back where the next check begins)
    // the empty box on a drug's page offers what people ask most about that drug
    await p.click("#search"); await p.waitForTimeout(600);
    const sug = await p.evaluate(() => ({ hint: (document.querySelector("#search-results .sr-hint") || {}).textContent || "", hrefs: [...document.querySelectorAll("#search-results a.sr-sug")].map(a => a.getAttribute("href")) }));
    ok(w + " px: before a word is typed, the box on the cannabis page offers what people ask most about cannabis", sug.hint === "Most asked about cannabis" && sug.hrefs.length >= 3 && sug.hrefs.every(h => h.startsWith("#s-cannabis/q-")), JSON.stringify(sug));
    // (2.24.1; his words of 19 November, 17:46: "the questions should be in random order and always new ones should appear") elsewhere the box offers a
    // new draw each time it opens: five questions of five drugs, none this device was shown before (until all were), kept on the device by number only
    await go(p, "#home", 600); const draws = [];
    for (let k = 0; k < 6; k++) {
      await p.evaluate(() => { const s = document.getElementById("search"); s.blur(); if (typeof closeSearch === "function") closeSearch(); }); await p.waitForTimeout(150);
      await p.click("#search"); await p.waitForTimeout(350);
      draws.push(await p.evaluate(() => ({ hint: (document.querySelector("#search-results .sr-hint") || {}).textContent || "", hrefs: [...document.querySelectorAll("#search-results a.sr-sug")].map(a => a.getAttribute("href")) })));
    }
    const ids = draws.flatMap(d => d.hrefs.map(h => h.replace(/^.*\/q-/, ""))), kept = await p.evaluate(() => JSON.parse(localStorage.getItem("pk-sug-seen") || "[]"));
    ok(w + " px (2.24.1): each time the box opens on the start page it offers a new draw: five questions of five different drugs, none shown before on this device, the numbers kept on the device",
      draws.every(d => d.hint === "Try a question like these" && d.hrefs.length === 5 && new Set(d.hrefs.map(h => h.split("/")[0])).size === 5) && new Set(ids).size === 30 && ids.every(i => kept.includes(i)) && kept.every(i => /^cl_[a-z0-9_]+$/.test(i)),
      draws.map(d => d.hrefs.map(h => h.replace(/^#s-/, "")).join(" ")).join(" || "));
    await p.evaluate(() => { document.getElementById("search").blur(); if (typeof closeSearch === "function") closeSearch(); });
    // (2.16, 2.16.1) a question we have no answer to gets published research at once and BY ITSELF (no tap): the papers on its drug and key words,
    // from Europe PMC through the site's own server; only the drug's names and plain key words leave the device for it, never the sentence;
    // it stands there again when the question is typed again, sent or not; a question about dying is not looked up
    await go(p, "#home"); await p.evaluate(() => pkInsight.load()); await p.waitForFunction(() => pkInsight.state() === "ready", null, { timeout: 120000 });
    const bodies = []; const onReq = r => { if (/\/api\/find$/.test(r.url())) bodies.push(r.postData() || ""); }; p.on("request", onReq); ASKED_EPMC.length = 0;
    await p.fill("#search", "does lsd change your eye colour"); await p.waitForSelector("#search-results .sr-fit-none", { timeout: 20000 });
    const byItself = await p.waitForSelector("#search-results .ins-found-l li", { timeout: 15000 }).then(() => true, () => false);
    ok(w + " px: with no answer of ours, the published research comes by itself, without a tap", byItself && bodies.length === 1, JSON.stringify(bodies));
    await p.waitForSelector("#search-results .ask-auto-said", { timeout: 9000 }).catch(() => {});   // (2.17: sent by itself)
    await p.fill("#search", ""); await p.waitForTimeout(200); await p.fill("#search", "does lsd change your eye colour"); await p.waitForSelector("#search-results .sr-sent", { timeout: 20000 }).catch(() => {});
    const again = await p.evaluate(() => ({ sent: !!document.querySelector("#search-results .sr-sent"), rows: document.querySelectorAll("#search-results .ins-found-l li").length }));
    ok(w + " px: typed again after it was sent, the question shows the research again (and nothing is asked of the server twice)", again.sent && again.rows === 2 && bodies.length === 1, JSON.stringify(again) + " " + bodies.length);
    const found = await p.evaluate(() => { const b = document.querySelector("#search-results .ins-found"); return b ? { h: (b.querySelector(".ins-found-h") || {}).textContent, rows: [...b.querySelectorAll(".ins-found-l li")].map(li => li.querySelector("a").textContent + " | " + li.querySelector("a").getAttribute("href") + " | " + li.querySelector(".m").textContent), quotes: [...b.querySelectorAll(".ins-found-l li")].map(li => (li.querySelector(".pq") || {}).textContent || ""), wide: document.documentElement.scrollWidth > innerWidth + 1, note: [...b.querySelectorAll(".ins-found-n")].map(x => x.textContent).join(" ") } : null; });
    const sentBody = bodies.length ? JSON.parse(bodies[0]) : {};
    ok(w + " px: the research found: title, kind, year, journal, free to read or not, and its link; and it says we have not read these",
      found && found.h === "Published research on this, found just now" && found.rows.length === 2 && found.rows[0] === "A review of LSD and the eye | https://doi.org/10.1234/test.2021.1 | Review \u00B7 2021 \u00B7 Journal of Tests \u00B7 free to read" && found.rows[1] === "LSD and the eye: a trial in forty volunteers | https://europepmc.org/article/MED/222 | Trial \u00B7 2013 \u00B7 Trials Today" && /We have not read these yet, and a title is not a finding/.test(found.note), JSON.stringify(found));
    ok(w + " px: under each paper's title stand its own words on the question, in quotation marks: at most 15, from the end of its summary, by rule; and the line under the list says whose words they are and that they are no answer of ours",
      found && found.quotes.length === 2 && found.quotes[0] === "\u201C\u2026the colour of the iris did not change in any volunteer given LSD\u2026\u201D" && found.quotes[1] === "\u201C\u2026the colour of the eye stayed the same after LSD on every photograph\u201D" && /The words in quotation marks are each paper\u2019s own, from the end of its summary: a fixed rule picked them, not a person, and they are not an answer of ours\.$/.test(found.note) && !found.wide, JSON.stringify(found));
    ok(w + " px: for it only the drug's names and plain key words leave the device (never the sentence), and Europe PMC is asked for exactly those",
      bodies.length === 1 && Object.keys(sentBody).sort().join() === "names,words" && sentBody.names.join() === "lsd" && sentBody.words.join() === "eye,colour" && ASKED_EPMC.length >= 4 && ASKED_EPMC.every(u => u.startsWith("https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=(") && /TITLE:"lsd"/.test(u) && /resultType=core/.test(u)) && ASKED_EPMC.filter(u => /\(TITLE:"lsd" AND \(TITLE:"lysergic"/.test(u)).length >= 2 && !ASKED_EPMC.some(u => /does lsd change/.test(u)), JSON.stringify([ASKED_EPMC.length, ASKED_EPMC.map(u => u.slice(60, 110) + " … " + u.slice(-70)), bodies]));
    // (2.22) an amount that kills is not looked up: one line says so, with the way to the emergency numbers. (A question of fact about dying is looked up since 2.22: below)
    await p.fill("#search", "how much lsd kills you"); await p.waitForSelector("#search-results .ins-shut", { timeout: 15000 }).catch(() => {}); await p.waitForTimeout(600);
    const heldN = bodies.length, shut = await p.evaluate(() => { const x = document.querySelector("#search-results .ins-shut"); return x ? { t: x.textContent, sos: !!x.querySelector('a[href="#emergency"]'), list: !!document.querySelector("#search-results .ins-found-l") } : null; });
    ok(w + " px: an amount that kills is not looked up: one line says so, with the way to the emergency numbers", bodies.length === 1 && !!shut && /^We do not look up published research for a question like this one/.test(shut.t) && shut.sos && !shut.list, JSON.stringify([bodies.slice(1), shut]));
    { await p.fill("#search", ""); await p.fill("#search", "can lsd kill you"); await p.waitForSelector("#search-results .ins-found-l li", { timeout: 20000 }).catch(() => {}); await p.waitForTimeout(400);
      const d = await p.evaluate(() => ({ rows: document.querySelectorAll("#search-results .ins-found-l li").length, quotes: document.querySelectorAll("#search-results .ins-found-l .pq").length, note: [...document.querySelectorAll("#search-results .ins-found .ins-found-n")].map(e => e.textContent).join(" ") }));
      const b = bodies.length > heldN ? JSON.parse(bodies[bodies.length - 1]) : {};
      ok(w + " px (2.22): a question of fact about dying is looked up under the words papers use for dying, and its papers are listed by title only: no words of theirs",
        bodies.length === heldN + 1 && (b.names || []).join() === "lsd" && /^mortality\|deaths\|fatal/.test((b.words || [])[0] || "") && b.t === 1 && d.rows >= 1 && d.quotes === 0 && /with no words from them/.test(d.note), JSON.stringify([b, d]));
      await p.fill("#search", ""); await p.evaluate(() => closeSearch()); }
    const heldM = bodies.length;
    // (2.21) a question about children, and one that names no single drug: looked up now, and listed by title only (no words of a paper)
    // (2.21.2: the system answers more every hour, and on 18 November it answered the question this check had typed) the first of these that the site has no
    // answer to, by the page's own reading; what is sent must be what the page's key words say
    const genQ = await p.evaluate(async qs => { for (const q of qs) { const t = insFindWanted(await insRank(q, {})); if (t && t.t === 1 && t.names.join() === "drug use,substance use" && /adolescents/.test(t.words.join())) return { q, words: t.words.join() }; } return null; },
      ["does parenting affect whether teenagers use drugs", "does boredom make teenagers try drugs", "do strict schools keep teenagers off drugs", "does moving house make teenagers try drugs", "do teenagers in villages use drugs less"]);
    await p.fill("#search", genQ ? genQ.q : "does boredom make teenagers try drugs"); await p.waitForSelector("#search-results .ins-found-l li", { timeout: 20000 }).catch(() => {}); await p.waitForTimeout(700);
    const gen = await p.evaluate(() => ({ rows: document.querySelectorAll("#search-results .ins-found-l li").length, quotes: document.querySelectorAll("#search-results .ins-found-l .pq").length, note: [...document.querySelectorAll("#search-results .ins-found .ins-found-n")].map(e => e.textContent).join(" ") }));
    const genBody = bodies.length > heldM ? JSON.parse(bodies[bodies.length - 1]) : {};
    ok(w + " px (2.21): a question that names no single drug, about children, is looked up under what research calls the subject, and its papers are listed by title only",
      !!genQ && (genBody.names || []).join() === "drug use,substance use" && genBody.t === 1 && (genBody.words || []).join() === genQ.words && gen.rows >= 1 && gen.quotes === 0 && /For a question like this one we list the papers only, with no words from them\.$/.test(gen.note), JSON.stringify([genBody, gen]));
    await p.fill("#search", ""); await p.evaluate(() => closeSearch()); const genN = bodies.length;
    // the reader's own switch (About us, Privacy): off, nothing is looked up by itself, and one quiet button looks it up
    await p.evaluate(() => localStorage.setItem("pk-auto", "0")); await p.fill("#search", "does lsd make your pupils bigger"); await p.waitForSelector("#search-results .sr-fit", { timeout: 20000 }); await p.waitForTimeout(1600);
    const offN = bodies.length, btn = await p.$("#search-results .ins-found button[data-find-now]");
    if (btn) { await btn.click(); await p.waitForSelector("#search-results .ins-found-l li", { timeout: 15000 }).catch(() => {}); }
    ok(w + " px: with the reader's switch off nothing is looked up by itself; one quiet button looks it up", offN === genN && !!btn && bodies.length === genN + 1 && (await p.$$("#search-results .ins-found-l li")).length === 2, offN + " " + bodies.length);
    await p.evaluate(() => localStorage.removeItem("pk-auto"));
    /* ---- site 2.22 (18 November 2026; the senior author, 22:15: "it think it knows but it does not"; "there should be instant searches available at least when
       the user is waiting ... should they hide under an arrow? what's the best design"): one layout for a question the site has no answer to; what is only a
       place to look; the way out under an answer; the pages of official bodies ---- */
    { await p.fill("#search", ""); await p.evaluate(() => { closeSearch(); PREF_COUNTRY = ""; }); await p.fill("#search", "does lsd change your eye colour"); await p.waitForSelector("#search-results .ins-found-l li", { timeout: 20000 }).catch(() => {}); await p.waitForTimeout(400);
      const read = () => p.evaluate(() => { const f = document.querySelector("#search-results .sr-fit"); if (!f) return null;
        const kids = [...f.children].filter(e => !e.hidden).map(e => e.matches(".sr-fit-none") ? "line" : e.matches(".ins-live") ? "live" : e.matches(".ins-jump") ? "jumps" : e.matches(".sr-fit-h") ? "h:" + e.textContent : e.matches("a.sr-fit-a") ? "answer" : e.matches('.ins-slot[data-slot="found"]') ? (e.children.length ? "research" : "") : e.matches('.ins-slot[data-slot="official"]') ? (e.children.length ? "official" : "") : e.matches("a.sr-route") ? "route" : e.matches(".sr-exit") ? "exit" : e.matches(".sr-read") ? "" : e.className).filter(Boolean);
        return { kids, chips: [...f.querySelectorAll(".ins-jump .chip")].map(b => b.textContent), off: [...f.querySelectorAll(".ins-off .ins-off-l li")].map(li => li.querySelector("a").textContent + " | " + li.querySelector(".m").textContent + " | " + li.querySelector("a").getAttribute("href")), offSeen: [...f.querySelectorAll(".ins-off .ins-off-l li")].filter(li => !li.hidden).length,
          all: (f.querySelector(".ins-off [data-show-all]") || {}).textContent || "", offH: (f.querySelector(".ins-off .ins-found-h") || {}).textContent || "", offN: [...f.querySelectorAll(".ins-off .ins-found-n")].map(x => x.textContent).join(" "), arrows: f.querySelectorAll("details, summary").length, wide: document.documentElement.scrollWidth > innerWidth + 1 }; });
      const L = await read(); if (L) L.kids = L.kids.filter(k => k !== "live"); const at = k => L.kids.indexOf(k), near = at("h:Closest answers we have");   // (2.23: what the system is doing for a question that was sent stands under the line; it has its own checks)
      ok(w + " px (2.22): a question the site has no answer to reads, from the top: the line; what stands below, as a row of jumps; the closest answers we have; the research found; the official pages. Nothing is folded under an arrow",
        !!L && at("line") === 0 && at("jumps") === 1 && at("research") > 1 && at("official") === at("research") + 1 && (near < 0 || (near > 1 && near < at("research"))) && !L.kids.includes("h:Related") && !L.kids.includes("h:Best match") && L.arrows === 0 && !L.wide &&
        L.chips.some(c => /^Research 2$/.test(c)) && L.chips.some(c => /^Official pages \d+$/.test(c)), JSON.stringify(L && [L.kids, L.chips, L.arrows, L.wide]));
      ok(w + " px (2.22): the pages of official bodies about the drug stand under the research: each body's own page on it, as a link to its own site, three shown and the rest behind a plain “Show all”; it says that they are not about the question and that we have not checked them",
        !!L && L.offH === "Official pages about LSD" && L.off.length >= 4 && L.offSeen === 3 && L.all === "Show all " + L.off.length && L.off.every(r => / \| https:\/\//.test(r)) && L.off.some(r => /^FRANK on LSD \| United Kingdom \| https:\/\/www\.talktofrank\.com\//.test(r)) &&
        /each on its own site/.test(L.offN) && /not about your question as you asked it, and we have not checked them/.test(L.offN), JSON.stringify(L && [L.offH, L.off, L.offSeen, L.all, L.offN]));
      await p.click("#search-results .ins-off [data-show-all]"); await p.waitForTimeout(200); const L2 = await read();
      ok(w + " px (2.22): “Show all” shows the rest in place, and its button is gone", !!L2 && L2.offSeen === L2.off.length && L2.all === "", JSON.stringify(L2 && [L2.offSeen, L2.off.length, L2.all]));
      // a jump leads to its block
      const y0 = await p.evaluate(() => { const y = Math.round(scrollY); const b = document.querySelector('#search-results .ins-jump [data-jump="official"]'); b.click(); return y; }); await p.waitForTimeout(900);
      const jumped = await p.evaluate(() => { const s = document.querySelector('#search-results .ins-slot[data-slot="official"]'), r = s.getBoundingClientRect(), a = document.activeElement, box = document.getElementById("search-results"), bt = box.getBoundingClientRect().top;
        return { top: Math.round(r.top), inBox: Math.round(r.top - bt), h: innerHeight, focus: !!(a && s.contains(a)), y: Math.round(scrollY), boxScroll: Math.round(box.scrollTop), scrolls: box.scrollHeight > box.clientHeight + 1, end: box.scrollTop + box.clientHeight >= box.scrollHeight - 2, boxH: box.clientHeight }; });
      // (2.25.0; his words of 17:57: "the site has to get stationary and scroll down only in the dropdown") where the results box scrolls, only it moves
      ok(w + " px (2.22, 2.25.0): a jump leads to its block and puts the reader there; where the results scroll in their own box, only that box moves, never the page", jumped.top >= -4 && jumped.top < jumped.h * 0.75 && jumped.focus &&
        (!jumped.scrolls || (jumped.y === y0 && jumped.boxScroll > 0 && jumped.inBox >= -4 && (jumped.inBox < 60 || (jumped.end && jumped.inBox < jumped.boxH * 0.75)))), JSON.stringify([y0, jumped]));
      // the reader's own country's bodies first
      await p.evaluate(() => { PREF_COUNTRY = "Canada"; }); await p.fill("#search", ""); await p.fill("#search", "does lsd change your eye colour"); await p.waitForSelector("#search-results .ins-off .ins-off-l li", { timeout: 15000 }).catch(() => {}); await p.waitForTimeout(300);
      const L3 = await read(); await p.evaluate(() => { PREF_COUNTRY = ""; });
      ok(w + " px (2.22): the bodies of the reader's own country stand first", !!L3 && /\| Canada \| /.test(L3.off[0] || "") && !/\| Canada \| /.test((L && L.off[0]) || ""), JSON.stringify(L3 && L3.off.slice(0, 2)));
      await p.fill("#search", ""); await p.evaluate(() => closeSearch()); }
    // a part of the Big questions page is a place to look, never the answer: the question stays open, is looked up, and (after a moment) sent
    { const n0 = bodies.length; await p.fill("#search", "is use more common among men than women"); await p.waitForSelector("#search-results .ins-found-l li", { timeout: 20000 }).catch(() => {}); await p.waitForTimeout(300);
      const T = await p.evaluate(async () => { const f = document.querySelector("#search-results .sr-fit"), r = await pkInsight.rank("is use more common among men than women", {});
        return { note: r.note, line: (f.querySelector(".sr-fit-none b") || {}).textContent || "", way: [...f.querySelectorAll("a.sr-route.sr-way")].map(a => a.getAttribute("href")), top: [...f.querySelectorAll("a.sr-route:not(.sr-way)")].length, h: [...f.querySelectorAll(".sr-fit-h")].map(x => x.textContent) }; });
      const b = bodies.length > n0 ? JSON.parse(bodies[bodies.length - 1]) : {};
      ok(w + " px (2.22): a question that names no drug and is nearest to a part of the Big questions page (“is use more common among men than women”) is a question about drugs, and is not answered by that part: the line says we have not checked it, the part stands last as a place to look, and research on drug use by sex is looked up by title",
        T.note === "none" && T.line === "We haven’t checked exactly this yet." && T.top === 0 && T.way.join() === "#facts/part-f-sex" && T.h.includes("A place to look") && (b.names || []).join() === "drug use,substance use" && /men\|male/.test((b.words || []).join()) && /women\|female/.test((b.words || []).join()) && b.t === 1, JSON.stringify([T, b]));
      await p.fill("#search", ""); await p.evaluate(() => closeSearch()); }
    // the way out under an answer: "Not what you asked? Search wider"
    { const pick = await p.evaluate(async () => { for (const q of ["does alcohol kill brain cells", "can poppy seeds make you fail a drug test", "does lsd stay in your body forever"]) { const r = await pkInsight.rank(q, {}); if (r.best.length && r.judge.p >= 0.8) return { q, id: r.best[0].id }; } return null; });
      const n0 = bodies.length; await p.fill("#search", pick ? pick.q : ""); await p.waitForSelector("#search-results a.sr-best", { timeout: 20000 }).catch(() => {}); await p.waitForTimeout(1200);
      const before = await p.evaluate(() => { const f = document.querySelector("#search-results .sr-fit"), kids = [...f.children].filter(e => !e.hidden); const i = kids.findIndex(e => e.matches("a.sr-best"));
        return { exit: kids[i + 1] && kids[i + 1].matches(".sr-exit") ? kids[i + 1].textContent : "", line: !!f.querySelector(".sr-fit-none"), found: !!f.querySelector(".ins-found") }; });
      ok(w + " px (2.22): under a best match stands the way out, “Not what you asked? Search wider”; nothing is looked up or sent while the page takes the question for answered", !!pick && before.exit === "Not what you asked? Search wider" && !before.line && !before.found && bodies.length === n0, JSON.stringify([pick, before, bodies.length - n0]));
      await p.click("#search-results .sr-exit [data-ins-notit]"); await p.waitForSelector("#search-results .sr-fit-none", { timeout: 15000 }).catch(() => {}); await p.waitForSelector("#search-results .ins-found-l li", { timeout: 15000 }).catch(() => {}); await p.waitForSelector("#search-results .ask-auto-said, #search-results .sr-sent", { timeout: 9000 }).catch(() => {});
      const after = await p.evaluate(id => { const f = document.querySelector("#search-results .sr-fit"), rows = [...f.querySelectorAll("a.sr-fit-a")]; const it = JSON.parse(localStorage.getItem("pk-asked") || "[]").find(x => x.x);
        return { best: !!f.querySelector("a.sr-best"), line: (f.querySelector(".sr-fit-none") || {}).textContent || "", first: rows[0] ? rows[0].dataset.insight : "", h: [...f.querySelectorAll(".sr-fit-h")].map(x => x.textContent), rows: f.querySelectorAll(".ins-found-l li").length, exit: !!f.querySelector(".sr-exit"), kept: it ? [it.q, it.x, it.sent] : null }; }, pick && pick.id);
      const rec = [...ON.kv.entries()].filter(([k]) => k.startsWith("aq:")).map(([, v]) => JSON.parse(v)).find(v => pick && v.q === pick.q);
      ok(w + " px (2.22): one tap, and the same question is read as not answered, in place: the line, sent at once; what stood as the answer is the first of the closest answers we have; the research is there",
        !!pick && !after.best && /^We haven’t checked exactly this yet\./.test(after.line) && /Sent\b|You sent us this question/.test(after.line) && after.first === pick.id && after.h[0] === "Closest answers we have" && after.rows >= 1 && !after.exit && bodies.length === n0 + 1, JSON.stringify([after, bodies.length - n0]));
      ok(w + " px (2.22): it is sent with which answer it was, so that the system learns which answer does not answer it; the reader's own list keeps that too", !!rec && rec.a === 1 && Array.isArray(rec.x) && rec.x.includes(pick.id) && !!after.kept && after.kept[0] === pick.q && after.kept[1] === pick.id && after.kept[2] === 1, JSON.stringify([rec, after.kept]));
      await p.fill("#search", ""); await p.fill("#search", pick ? pick.q : ""); await p.waitForSelector("#search-results .sr-fit", { timeout: 15000 }).catch(() => {}); await p.waitForTimeout(700);
      const again = await p.evaluate(() => { const f = document.querySelector("#search-results .sr-fit"); return { best: !!f.querySelector("a.sr-best"), sent: !!f.querySelector(".sr-sent"), h: [...f.querySelectorAll(".sr-fit-h")].map(x => x.textContent)[0] }; });
      ok(w + " px (2.22): asked again, it is still read as not answered (as long as that same answer is all the page would give)", !again.best && again.sent && again.h === "Closest answers we have", JSON.stringify(again));
      await p.fill("#search", ""); await p.evaluate(() => { closeSearch(); localStorage.removeItem("pk-asked"); INS.cache.clear(); }); }
    // a best match the judge is not sure of: it stands as the best match, and the research and the official pages come under it by themselves; nothing is sent
    { const pick = await p.evaluate(async () => { for (const q of ["can kratom be addictive", "is ketamine deadly", "does mdma cause depression the day after", "is cocaine bad for your heart"]) { const r = await pkInsight.rank(q, {}); if (r.best.length && r.judge.p < 0.8 && insFindWanted(r) && !/ketamine|psilocybin|mescaline/.test(q)) return { q, p: r.judge.p }; } return null; });
      const n0 = bodies.length, k0 = ON.kv.size; if (pick) { await p.fill("#search", pick.q); await p.waitForSelector("#search-results .ins-found-l li", { timeout: 20000 }).catch(() => {}); await p.waitForTimeout(3200); }
      const U = pick ? await p.evaluate(() => { const f = document.querySelector("#search-results .sr-fit"); return { best: !!f.querySelector("a.sr-best"), exit: !!f.querySelector(".sr-exit"), line: !!f.querySelector(".sr-fit-none"), lead: (f.querySelector(".ins-found .ins-lead") || {}).textContent || "", rows: f.querySelectorAll(".ins-found-l li").length, jumps: !!f.querySelector(".ins-jump:not([hidden])") }; }) : null;
      ok(w + " px (2.22): a best match the judge is not sure of keeps its place, and the research comes under it by itself, “in case the answer above is not what you asked”; nothing is sent and nothing says that we have no answer",
        !pick || (U.best && U.exit && !U.line && /^In case the answer above is not what you asked:/.test(U.lead) && U.rows >= 1 && !U.jumps && bodies.length === n0 + 1 && ON.kv.size === k0), JSON.stringify([pick, U, bodies.length - n0, ON.kv.size - k0]));
      await p.fill("#search", ""); await p.evaluate(() => closeSearch()); }
    p.off("request", onReq); await p.fill("#search", ""); await p.evaluate(() => { closeSearch(); localStorage.removeItem("pk-asked"); });
    // (2.21) past searches: kept by themselves on this device (a question that stays in the box, or Enter), each with the answer the site gave; listed in the panel
    // under the questions that wait; "Delete my search history" clears them, "Don't keep my searches" clears them and stops it
    await go(p, "#home"); await p.evaluate(() => { closeSearch(); localStorage.removeItem("pk-hist"); localStorage.removeItem("pk-hist-on"); askedBox(); });
    const h0 = await p.evaluate(() => ({ bar: !document.getElementById("home-asked").hidden, kept: localStorage.getItem("pk-hist") }));
    await typeQ(p, "is ketamine addictive"); await p.waitForTimeout(3300);                                   // it stays in the box: kept without Enter
    const h1 = await p.evaluate(() => JSON.parse(localStorage.getItem("pk-hist") || "[]").map(x => x.q + "|" + (x.id || "")));
    await p.fill("#search", "does lsd change your eye colour"); await p.waitForTimeout(500); await p.keyboard.press("Enter"); await p.waitForTimeout(600);     // Enter: at once
    await p.evaluate(() => { if (EV.open) closeEvidence(); closeSearch(); }); await p.waitForTimeout(300); await p.fill("#search", ""); await go(p, "#home"); await p.evaluate(() => closeSearch());
    await p.evaluate(() => { const a = JSON.parse(localStorage.getItem("pk-asked") || "[]"); localStorage.setItem("pk-asked", "[]"); askedBox(); });   // (only the past searches: the line then counts them)
    const h2 = await p.evaluate(() => ({ bar: (document.querySelector("#home-asked .you-bar") || {}).textContent || "", words: /ketamine|lsd/i.test(document.getElementById("home-asked").textContent), rows: [...document.querySelectorAll("#yousheet .you-hist li")].map(li => li.querySelector(".you-hq").textContent + " | " + li.querySelector(".you-ha").textContent.slice(0, 12)), arrows: document.querySelectorAll("#yousheet details, #yousheet summary").length }));
    await p.reload(); await p.waitForTimeout(900);
    const h2b = await p.evaluate(() => (document.querySelector("#home-asked .you-bar") || {}).textContent || "");                          // (on the next opening of the page the line is there at once, with only past searches kept)
    await p.click("#home-asked .you-bar"); await p.waitForTimeout(400); await shot(p, w + "-you-past");
    await p.click('#yousheet .you-hist button[data-hist="is ketamine addictive"]'); await p.waitForTimeout(1300);
    const h3 = await p.evaluate(() => ({ shut: !YOU.open, value: document.getElementById("search").value, open: !document.getElementById("search-results").hidden }));
    await p.fill("#search", ""); await p.evaluate(() => closeSearch()); await p.click("#home-asked .you-bar"); await p.waitForTimeout(400);
    const del = await p.evaluate(() => { const b = document.querySelector("#yousheet button[data-hist-clear]"), r = b && b.getBoundingClientRect(); return b ? { text: b.textContent, h: Math.round(r.height), off: (document.querySelector("#yousheet button[data-hist-off]") || {}).textContent || "" } : null; });
    await p.click("#yousheet button[data-hist-clear]"); await p.waitForTimeout(300);
    const h4 = await p.evaluate(() => ({ kept: localStorage.getItem("pk-hist"), on: localStorage.getItem("pk-hist-on"), rows: document.querySelectorAll("#yousheet .you-hist li").length, open: YOU.open, said: (document.querySelector("#you-past + .aq-note") || {}).textContent || "" }));
    await p.click("#yousheet button[data-hist-off]"); await p.waitForTimeout(300); await p.click("#yousheet .ev-back"); await p.waitForTimeout(400);
    await typeQ(p, "is ketamine addictive"); await p.keyboard.press("Enter"); await p.waitForTimeout(700); await p.evaluate(() => { if (EV.open) closeEvidence(); closeSearch(); }); await p.waitForTimeout(300);
    const h5 = await p.evaluate(() => ({ kept: localStorage.getItem("pk-hist"), on: localStorage.getItem("pk-hist-on"), sw: (location.hash = "#about", document.getElementById("hist-switch").checked) }));
    ok(w + " px: past searches (2.21) are kept by themselves on this device, with the answer the site gave: a question that stays in the box without Enter, and one asked with Enter",
      h0.bar === false && h0.kept === null && h1.length === 1 && /^is ketamine addictive\|(au_|cl_)/.test(h1[0]) && h2.bar === "Your questions2 past searches" && h2b === "Your questions2 past searches" && !h2.words && h2.rows.length === 2 && /^does lsd change your eye colour \| /.test(h2.rows[0]) && /^is ketamine addictive \| Answered/.test(h2.rows[1]) && h2.arrows === 0, JSON.stringify([h0, h1, h2]));
    ok(w + " px: a past search asks its question again; one plain button deletes the history, and another stops keeping it (the same switch stands on About us, Privacy)",
      h3.shut && h3.value === "is ketamine addictive" && h3.open && del && del.text === "Delete my search history" && del.h >= 44 && del.off === "Don’t keep my searches" && h4.kept === null && h4.on === null && h4.rows === 0 && h4.open && /^Nothing yet\./.test(h4.said) && h5.kept === null && h5.on === "0" && h5.sw === false, JSON.stringify([h3, del, h4, h5]));
    await p.context().close();
  }

  /* ---- (site 2.23) what our system is doing for a question the reader sent, as it happens; and the answer the moment it is written ---- */
  for (const w of [390, 1280]) {
    const crypto = require("crypto"), keyOf = q => crypto.createHash("sha256").update(q.toLowerCase()).digest("hex").slice(0, 20);
    const Q = "does modafinil make teeth yellow", K = keyOf(Q);
    liveSet(null);
    const p = await open(ON, w), askedReqs = []; p.on("request", r => { if (/\/api\/asked/.test(r.url())) askedReqs.push(r.url().replace(/^.*\/api\//, "")); });
    await p.evaluate(() => { localStorage.removeItem("pk-asked"); localStorage.removeItem("pk-auto"); });
    await typeQ(p, Q); await p.waitForSelector("#search-results .ask-auto-said", { timeout: 15000 }).catch(() => {}); await p.waitForSelector("#search-results .ins-live li", { timeout: 15000 }).catch(() => {});
    const L0 = await p.evaluate(() => { const f = document.querySelector("#search-results .sr-fit"), b = f.querySelector(".ins-live"), it = JSON.parse(localStorage.getItem("pk-asked") || "[]")[0] || {};
      return { said: (f.querySelector(".ask-auto-said") || {}).textContent || "", prev: b && b.previousElementSibling ? b.previousElementSibling.className : "", steps: b ? [...b.querySelectorAll("li")].map(x => x.className + "|" + x.textContent) : [], sk: it.sk || "", ts: !!it.ts, live: b ? b.querySelector("[aria-live]") !== null : false }; });
    ok(w + " px (2.23): a question sent by the page keeps its key from the server's reply, and under the line stands what our system is doing: at first, that it is reading the question",
      /^Sent\. You can stay or come back/.test(L0.said) && /sr-fit-none/.test(L0.prev) && L0.steps.length === 1 && /^lv-now\|Reading your question now\.$/.test(L0.steps[0]) && L0.sk === K && L0.ts && L0.live, JSON.stringify(L0));
    await p.waitForTimeout(1800);
    ok(w + " px (2.23): the page asks the server what became of it by the question's key alone: no word of the question is in the address", askedReqs.length >= 1 && askedReqs.every(u => /^asked\?h=[0-9a-f]{20}$/.test(u)) && askedReqs[0] === "asked?h=" + K, JSON.stringify(askedReqs.slice(0, 3)));
    const item = (st, more) => ({ at: "2026-11-19T01:00:00+00:00", q: { [K]: { id: "w_a0900" } }, items: { w_a0900: Object.assign({ q: "Does modafinil stain the teeth?", st, say: "", n: { papers: 0, pages: 0 }, terms: ["tooth discoloration"] }, more || {}) }, answers: {} });
    liveSet(item("new")); await p.waitForFunction(() => /read it as/.test((document.querySelector("#search-results .ins-live") || {}).textContent || ""), null, { timeout: 15000 }).catch(() => {});
    const L1 = await p.evaluate(() => [...document.querySelectorAll("#search-results .ins-live li")].map(x => x.className + "|" + x.textContent));
    ok(w + " px (2.23): once our system has read it, the page shows how: in OUR wording, so that the reader sees whether they were understood; then that the search is on",
      L1.length === 2 && L1[0] === "lv-done|Read as: Does modafinil stain the teeth?" && L1[1] === "lv-now|Looking for papers and official pages", JSON.stringify(L1));
    liveSet(Object.assign(item("found", { n: { papers: 12, pages: 4 } }), { working: { ids: ["w_a0900"], since: "2026-11-19T01:01:00+00:00" } }));
    await p.waitForFunction(() => /Writing the answer now/.test((document.querySelector("#search-results .ins-live") || {}).textContent || ""), null, { timeout: 15000 }).catch(() => {}); await shot(p, w + "-live-writing");
    const L2 = await p.evaluate(() => [...document.querySelectorAll("#search-results .ins-live li")].map(x => x.className + "|" + x.textContent));
    ok(w + " px (2.23): what was found, and that the answer is being written now", L2.length === 3 && L2[1] === "lv-done|Found 12 papers it can read and 4 official pages" && /^lv-now\|Writing the answer now\. Every sentence is tied to a source’s own words and checked\./.test(L2[2]), JSON.stringify(L2));
    liveSet(Object.assign(item("found", { n: { papers: 12, pages: 4 } }), { room: false, room_at: "2026-11-20T00:00:00+00:00" }));
    await p.waitForFunction(() => /used up today/.test((document.querySelector("#search-results .ins-live") || {}).textContent || ""), null, { timeout: 15000 }).catch(() => {});
    const L3 = await p.evaluate(() => [...document.querySelectorAll("#search-results .ins-live li")].map(x => x.className + "|" + x.textContent));
    ok(w + " px (2.23): where the free models have no room left today the page says so, and when it goes on: nothing is promised that the system cannot keep",
      L3.length === 4 && L3[2] === "lv-next|Next: writing the answer" && /^lv-wait\|Today’s writing allowance is used up\. It goes on at \d/.test(L3[3]), JSON.stringify(L3));
    // the answer, the moment it is written: in the page's own form, with its line; the list of the reader's questions turns green; nothing was published in between
    const ans = { q: "Does modafinil stain the teeth?", short: "No study read reports it.", but: "This rests on 1 review. It has not read every study on this question.", how: ["A 2019 review of modafinil’s unwanted effects does not list any change to the teeth."],
      refs: [{ id: "tester_2019", type: "article-journal", title: "Unwanted effects of modafinil: a review", author: [{ family: "Tester", given: "T." }], issued: { "date-parts": [[2019]] }, "container-title": "Journal of Tests", volume: "3", page: "1-9", DOI: "10.1234/test.2019.9" }],
      from: { papers: 1, summaries: 0, official: 0 }, made: "2026-11-19", complete: false, wanted: 0, drugs: [], page: "general" };
    liveSet(Object.assign(item("answered", { n: { papers: 12, pages: 4 }, aid: "au_w_a0900" }), { answers: { au_w_a0900: ans } }));
    await p.waitForSelector("#search-results .ins-live .lv-card a[data-you-live]", { timeout: 15000 }).catch(() => {}); await shot(p, w + "-live-answered");
    const L4 = await p.evaluate(() => { const f = document.querySelector("#search-results .sr-fit"), c = f.querySelector(".ins-live .lv-card"), it = JSON.parse(localStorage.getItem("pk-asked") || "[]")[0] || {}, line = f.querySelector(".sr-fit-none");
      return { h: c ? c.querySelector(".lv-h").textContent : "", q: c ? c.querySelector(".lv-q").textContent : "", a: c ? c.querySelector(".lv-a").textContent : "", btn: c ? c.querySelector("a[data-you-live]").textContent : "", bh: c ? Math.round(c.querySelector("a[data-you-live]").getBoundingClientRect().height) : 0,
        lineHidden: !!line && line.hidden, st: it.st, id: it.id, bar: (document.querySelector("#home-asked .you-bar") || {}).textContent || "", known: isAuto("au_w_a0900") }; });
    ok(w + " px (2.23): the moment the answer is written it stands there: “Answered just now”, our question, the short answer and the way in; the line that said we had no answer gives way; the reader's list counts it as answered",
      L4.h === "Answered just now" && L4.q === ans.q && L4.a === ans.short && L4.btn === "Read the answer" && L4.bh >= 44 && L4.lineHidden && L4.st === "ans" && L4.id === "au_w_a0900" && /1 answered/.test(L4.bar) && L4.known, JSON.stringify(L4));
    await p.click("#search-results .ins-live a[data-you-live]"); await p.waitForSelector("#evsheet.open .auto-l", { timeout: 10000 }).catch(() => {}); await shot(p, w + "-live-answer-open");
    const L5 = await p.evaluate(() => { const s = document.querySelector("#evsheet.open"); return s ? { title: (document.getElementById("ev-title") || {}).textContent, short: (s.querySelector(".ask-short") || {}).textContent, label: (s.querySelector(".auto-l") || {}).textContent, bars: !!s.querySelector(".ev-cert, .meter"), refs: s.querySelectorAll(".auto-refs li").length } : null; });
    ok(w + " px (2.23): it opens as every answer written by our system does: its question, its short answer, its line “Written with AI …”, its sources, and no certainty bars",
      !!L5 && L5.title === ans.q && L5.short === ans.short && /^Drafted automatically from 1 paper\. Not complete yet\.$/.test(L5.label) && !L5.bars && L5.refs === 1, JSON.stringify(L5));
    await p.evaluate(() => { if (EV.open) closeEvidence(); closeSearch(); }); await p.waitForTimeout(300);
    // an answer whose shape is not the build's is never taken; a question our system did not list says why; a listed question the reader keeps is asked for by its number
    await p.evaluate(() => { localStorage.setItem("pk-asked", JSON.stringify([{ k: "is modafinil a vitamin", q: "is modafinil a vitamin", d: "", t: Date.now(), ts: Date.now(), cv: "x", st: "wait", sent: 1, auto: 1, sk: "1".repeat(20) }, { k: "why is the sky blue on modafinil", q: "why is the sky blue on modafinil", d: "", t: Date.now() - 1000, ts: Date.now() - 1000, cv: "x", st: "wait", sent: 1, auto: 1, sk: "2".repeat(20) },
      { k: "does modafinil help with jet lag?", q: "Does modafinil help with jet lag?", d: "", t: Date.now() - 2000, cv: "x", st: "wait", sent: 1, kept: 1, w: "w_0031" }])); askedBox(); });
    const n1 = askedReqs.length;
    liveSet({ at: "t", q: { ["1".repeat(20)]: { id: "w_a0901" }, ["2".repeat(20)]: { no: "This was not read as a question about drugs. If it is one, ask it again with the drug's name in it." } },
      items: { w_a0901: { q: "Is modafinil a vitamin?", st: "answered", say: "", aid: "au_w_a0901" }, w_0031: { q: "Does modafinil help with jet lag?", st: "tried", say: "" } }, answers: { au_w_a0901: { q: "Is modafinil a vitamin?", short: "<img src=x onerror=alert(1)>", how: "not a list", refs: [] } } });
    await p.evaluate(() => liveKick(true)); await p.waitForFunction(() => { const l = JSON.parse(localStorage.getItem("pk-asked") || "[]"); return l.length === 3 && l.every(x => x.lv); }, null, { timeout: 15000 }).catch(() => {});
    const L6 = await p.evaluate(() => { const l = JSON.parse(localStorage.getItem("pk-asked") || "[]"); document.querySelector("#home-asked .you-bar").click(); return { lv: l.map(x => [x.st, x.lv && (x.lv.no ? "no" : x.lv.reload ? "reload" : x.lv.st)]), known: isAuto("au_w_a0901"), rows: [...document.querySelectorAll("#yousheet .aq .aq-k")].map(x => x.textContent.replace(/\s*·.*$/, "")) }; });
    ok(w + " px (2.23): an answer that does not have the build's shape is never taken into the page (the row says it is answered and to open the site again); a question our system did not list says so; a listed question the reader keeps is asked for by its number, and says what was done",
      !L6.known && JSON.stringify(L6.lv) === JSON.stringify([["wait", "reload"], ["wait", "no"], ["wait", "tried"]]) && L6.rows.join("|") === "Answered. Open the site again to read it|Read. Not listed|No answer passed the checks yet. Trying again" && askedReqs.slice(n1).some(u => /^asked\?h=1{20},2{20}&w=w_0031$/.test(u)), JSON.stringify([L6, askedReqs.slice(n1)]));
    await p.evaluate(() => { if (YOU.open) youClose(); }); await p.waitForTimeout(300);
    // switched off: nothing is asked
    const n2 = askedReqs.length; await p.evaluate(() => { localStorage.setItem("pk-auto", "0"); liveKick(true); }); await p.waitForTimeout(2500);
    ok(w + " px (2.23): a reader who switched off what the page does by itself is asked for nothing here either", askedReqs.length === n2, String(askedReqs.length - n2));
    await p.evaluate(() => { localStorage.removeItem("pk-auto"); localStorage.removeItem("pk-asked"); }); liveSet(null);
    // ---- (2.23.1) the reader is told only of an answer to a question of THEIR OWN, wherever they are on the site; and not when it stands before them ----
    { const K5 = "5".repeat(20), Q5 = "Does modafinil make you sweat?";
      await p.evaluate(([Q5, K5]) => { localStorage.setItem("pk-asked", JSON.stringify([{ k: Q5.toLowerCase(), q: Q5, d: "", t: Date.now(), ts: Date.now(), cv: SITE_BUILD, st: "wait", sent: 1, auto: 1, sk: K5 }])); location.hash = "#home"; askedBox(); }, [Q5, K5]);
      await p.waitForTimeout(400);
      const a5 = { q: "Does modafinil make people sweat more?", short: "Some people who took it in studies did.", but: "This rests on 1 review.", how: ["A review lists sweating among the unwanted effects people reported."],
        refs: [{ id: "tester_2020", type: "article-journal", title: "Modafinil: a review", author: [{ family: "Tester", given: "T." }], issued: { "date-parts": [[2020]] }, "container-title": "Journal of Tests", volume: "4", page: "1-9", DOI: "10.1234/test.2020.4" }], from: { papers: 1, summaries: 0, official: 0 }, made: "2026-11-19", complete: false, wanted: 0, drugs: [], page: "general" };
      liveSet({ at: "t", q: { [K5]: { id: "w_a0905" } }, items: { w_a0905: { q: a5.q, st: "answered", say: "", aid: "au_w_a0905" } }, answers: { au_w_a0905: a5 } });
      await p.evaluate(() => liveKick(true)); await p.waitForSelector("#you-tell", { timeout: 15000 }).catch(() => {}); await shot(p, w + "-told-own-answer");
      const T1 = await p.evaluate(() => { const b = document.getElementById("you-tell"); if (!b) return null; const r = b.getBoundingClientRect(), sos = document.querySelector(".sos-pill"), sr = sos && sos.offsetParent ? sos.getBoundingClientRect() : null;
        return { h: b.querySelector(".you-tell-h").textContent, q: (b.querySelector(".you-tell-q") || {}).textContent, btn: (b.querySelector("a[data-you-live]") || {}).textContent, x: !!b.querySelector("button[data-you-told-x]"), inView: r.top >= 0 && r.bottom <= innerHeight && r.left >= 0 && r.right <= innerWidth, coversSos: !!sr && !(sr.bottom <= r.top || sr.top >= r.bottom || sr.right <= r.left || sr.left >= r.right) }; });
      ok(w + " px (2.23.1): an answer to the reader's OWN question, while they are elsewhere on the site, is told in a small note: that their question has an answer, our question, and the way in; never over the way to the emergency numbers",
        !!T1 && T1.h === "Your question has an answer" && T1.q === a5.q && T1.btn === "Read the answer" && T1.x && T1.inView && !T1.coversSos, JSON.stringify(T1));
      await p.click("#you-tell a[data-you-live]"); await p.waitForSelector("#evsheet.open .auto-l", { timeout: 10000 }).catch(() => {});
      const T2 = await p.evaluate(() => ({ title: (document.getElementById("ev-title") || {}).textContent, gone: !document.getElementById("you-tell"), news: JSON.parse(localStorage.getItem("pk-asked") || "[]").some(x => x.news) }));
      ok(w + " px (2.23.1): the note opens the answer, and goes; it does not come back", T2.title === a5.q && T2.gone && !T2.news, JSON.stringify(T2));
      await p.evaluate(() => { if (EV.open) closeEvidence(); }); await p.waitForTimeout(300);
      // the general word is gone: a newer site on the server makes the page say nothing
      await p.evaluate(() => { localStorage.setItem("pk-asked", JSON.stringify([{ k: "does modafinil make teeth yellow", q: "does modafinil make teeth yellow", d: "", t: Date.now(), cv: SITE_BUILD, st: "wait", sent: 1, sk: "6".repeat(20) }])); ASK_NEWER = true; askedBox(); });
      const T3 = await p.evaluate(() => ({ newer: !!document.querySelector(".aq-new"), told: !!document.getElementById("you-tell"), text: document.body.innerText.includes("see whether yours is among them") }));
      ok(w + " px (2.23.1): a newer site with answers to other people's questions is not told at all", !T3.newer && !T3.told && !T3.text, JSON.stringify(T3));
      await p.evaluate(() => { ASK_NEWER = false; localStorage.removeItem("pk-asked"); askedBox(); }); liveSet(null); }
    // ---- (2.23.1) one question asked twice with a slip of the keyboard is one question: one row, sent once; two different questions stay two ----
    { const sends = []; p.on("request", r => { if (/\/api\/ask$/.test(r.url()) && r.method() === "POST") sends.push(JSON.parse(r.postData() || "{}").q); });
      await p.evaluate(() => { const now = Date.now(); localStorage.setItem("pk-asked", JSON.stringify([
        { k: "is kratom the same as kava", q: "is kratom the same as kava", d: "", t: now - 60000, ts: now - 60000, cv: SITE_BUILD, st: "wait", sent: 1, auto: 1, sk: "7".repeat(20) },
        { k: "is kratom the same as kavva", q: "is kratom the same as kavva", d: "", t: now - 30000, ts: now - 30000, cv: SITE_BUILD, st: "wait", sent: 1, auto: 1, sk: "8".repeat(20) },
        { k: "is mdma safe for the heart", q: "is mdma safe for the heart", d: "", t: now - 20000, cv: SITE_BUILD, st: "wait", sent: 1, auto: 1 },
        { k: "is mdea safe for the heart", q: "is mdea safe for the heart", d: "", t: now - 10000, cv: SITE_BUILD, st: "wait", sent: 1, auto: 1 },
        { k: "does kratom help with pain", q: "does kratom help with pain", d: "", t: now - 9000, cv: SITE_BUILD, st: "wait", sent: 1, auto: 1 },
        { k: "does kratom help with gain", q: "does kratom help with gain", d: "", t: now - 8000, cv: SITE_BUILD, st: "wait", sent: 1, auto: 1 }])); askedBox(); });
      await p.evaluate(() => insightLoad && insightLoad()); await p.waitForFunction(() => INS.state === "ready", null, { timeout: 60000 }).catch(() => {}); await p.evaluate(() => askedCheck()); await p.waitForTimeout(400);
      const S1 = await p.evaluate(() => JSON.parse(localStorage.getItem("pk-asked") || "[]").map(x => x.q));
      ok(w + " px (2.23.1): “is kratom the same as kava” and “… kavva” are one question: one row, the one sent first; “mdma” and “mdea”, “pain” and “gain” stay two questions each",
        JSON.stringify(S1) === JSON.stringify(["is kratom the same as kava", "is mdma safe for the heart", "is mdea safe for the heart", "does kratom help with pain", "does kratom help with gain"]), JSON.stringify(S1));
      await p.evaluate(() => { const l = JSON.parse(localStorage.getItem("pk-asked")); localStorage.setItem("pk-asked", JSON.stringify(l.slice(0, 1))); askedBox(); });
      const n0 = sends.length; await typeQ(p, "Is kratom the same as kavva?"); await p.waitForTimeout(4500);
      const S2 = await p.evaluate(() => ({ line: ((document.querySelector("#search-results .sr-fit-none") || {}).textContent || "").slice(0, 40), rows: JSON.parse(localStorage.getItem("pk-asked") || "[]").length }));
      ok(w + " px (2.23.1): asking it again with the slip is not a new question: nothing is sent again, the page says it was sent, and the list keeps one row",
        sends.length === n0 && /^You sent us this question/.test(S2.line) && S2.rows === 1, JSON.stringify([sends.slice(n0), S2]));
      await p.evaluate(() => { localStorage.removeItem("pk-asked"); closeSearch(); }); }
    // ---- (2.26.1; his words of 19 November, 23:42: two rows a word apart "were different ... questions ... they should be merged") one question, one row:
    // the same question with one word more ("together"), and two questions the system read as one question of its list; never a "not" or a second drug ----
    { await p.evaluate(() => { const now = Date.now(); localStorage.setItem("pk-asked", JSON.stringify([
        { k: "do people on mescaline really see the same patterns", q: "do people on mescaline really see the same patterns", d: "", t: now - 50000, cv: SITE_BUILD, st: "wait", sent: 1, auto: 1 },
        { k: "do people on mescaline see the same patterns", q: "do people on mescaline see the same patterns", d: "", t: now - 40000, cv: SITE_BUILD, st: "wait", sent: 1, auto: 1 },
        { k: "can kratom be mixed with alcohol safely", q: "can kratom be mixed with alcohol safely", d: "", t: now - 30000, cv: SITE_BUILD, st: "wait", sent: 1, auto: 1 },
        { k: "can kratom be mixed with alcohol and kava safely", q: "can kratom be mixed with alcohol and kava safely", d: "", t: now - 25000, cv: SITE_BUILD, st: "wait", sent: 1, auto: 1 },
        { k: "is ketamine addictive for most people", q: "is ketamine addictive for most people", d: "", t: now - 20000, cv: SITE_BUILD, st: "wait", sent: 1, auto: 1 },
        { k: "is ketamine not addictive for most people", q: "is ketamine not addictive for most people", d: "", t: now - 15000, cv: SITE_BUILD, st: "wait", sent: 1, auto: 1 },
        { k: "does kava make you sleepy the next day", q: "does kava make you sleepy the next day", d: "", t: now - 9000, cv: SITE_BUILD, st: "wait", sent: 1, auto: 1, w: "w_test1" },
        { k: "kava next day drowsiness", q: "kava next day drowsiness", d: "", t: now - 8000, cv: SITE_BUILD, st: "wait", sent: 1, auto: 1, w: "w_test1" }])); askedBox(); });
      await p.evaluate(() => askedCheck()); await p.waitForTimeout(400);
      const M1 = await p.evaluate(() => JSON.parse(localStorage.getItem("pk-asked") || "[]").map(x => x.q));
      ok(w + " px (2.26.1): a question with one word more is the same question (one row); two rows the system read as one listed question are one row; a “not” and a second drug keep two",
        JSON.stringify(M1) === JSON.stringify(["do people on mescaline really see the same patterns", "can kratom be mixed with alcohol safely", "can kratom be mixed with alcohol and kava safely", "is ketamine addictive for most people", "is ketamine not addictive for most people", "does kava make you sleepy the next day"]), JSON.stringify(M1));
      await p.evaluate(() => { localStorage.removeItem("pk-asked"); askedBox(); }); }
    // ---- (2.25.0; his words of 19 November, 17:49: "i want to be able to delete all my questions at once if i want") one tap, then a yes ----
    { await p.evaluate(() => { const now = Date.now(); localStorage.setItem("pk-asked", JSON.stringify(["sleep", "pain", "anxiety"].map((w, i) => ({ k: "does kanna help with " + w, q: "does kanna help with " + w, d: "", t: now - (i + 1) * 1000, cv: SITE_BUILD, st: "wait", sent: 1, auto: 1 })))); askedBox(); if (typeof youOpen === "function") youOpen(); });
      await p.waitForTimeout(300);
      const D0 = await p.evaluate(() => ({ btn: ((document.querySelector("#yousheet button[data-asked-clear]") || {}).textContent || ""), rows: document.querySelectorAll("#yousheet .aq-l > li").length }));
      await p.evaluate(() => document.querySelector("#yousheet button[data-asked-clear]").click()); await p.waitForTimeout(150);
      const D1 = await p.evaluate(() => ({ sure: ((document.querySelector("#yousheet .aq-sure") || {}).textContent || ""), yes: ((document.querySelector("#yousheet [data-asked-clear-yes]") || {}).textContent || ""), focus: document.activeElement && document.activeElement.hasAttribute("data-asked-clear-yes"), kept: JSON.parse(localStorage.getItem("pk-asked") || "[]").length }));
      await p.evaluate(() => document.querySelector("#yousheet [data-asked-clear-no]").click()); await p.waitForTimeout(150);
      const D2 = await p.evaluate(() => ({ rows: document.querySelectorAll("#yousheet .aq-l > li").length, kept: JSON.parse(localStorage.getItem("pk-asked") || "[]").length }));
      await p.evaluate(() => document.querySelector("#yousheet button[data-asked-clear]").click()); await p.waitForTimeout(150);
      await p.evaluate(() => document.querySelector("#yousheet [data-asked-clear-yes]").click()); await p.waitForTimeout(250);
      const D3 = await p.evaluate(() => ({ rows: document.querySelectorAll("#yousheet .aq-l > li").length, kept: JSON.parse(localStorage.getItem("pk-asked") || "[]").length, note: ((document.querySelector("#yousheet .aq-note") || {}).textContent || ""), bar: (document.getElementById("home-asked") || {}).hidden }));
      ok(w + " px (2.25.0): under the list, “Delete all my questions”; one tap asks first (“Delete all 3 questions from this device?”), “Keep them” keeps them, “Delete all” empties the list on this device",
        /Delete all my questions$/.test(D0.btn) && D0.rows === 3 && D1.sure === "Delete all 3 questions from this device?" && /Delete all$/.test(D1.yes) && D1.focus && D1.kept === 3 && D2.rows === 3 && D2.kept === 3 &&
          D3.rows === 0 && D3.kept === 0 && /^No question of yours is waiting/.test(D3.note), JSON.stringify([D0, D1, D2, D3]));
      await p.evaluate(() => { const b = document.querySelector("#yousheet [data-ev-close], #yousheet .ev-back"); if (b) b.click(); }); await p.waitForTimeout(200); }
    await p.context().close();
  }

  /* ---- (site 2.20) the papers' own words: in the sheet as in the results; no model is asked anywhere ---- */
  for (const w of [1280, 390]) {
    const p = await open(ON, w), posts = []; p.on("request", r => { if (/\/api\/(?:answer|find)$/.test(r.url())) posts.push(r.url().replace(/^.*\/api\//, "") + " " + (r.postData() || "")); });
    await p.evaluate(() => pkInsight.load()); await p.waitForFunction(() => pkInsight.state() === "ready", null, { timeout: 120000 }); await p.waitForTimeout(1200);
    await p.fill("#search", "does lsd change your eye colour"); await p.waitForSelector("#search-results .ins-found-l li .pq", { timeout: 20000 }).catch(() => {});
    // (2.22) the papers stand in their own place under the line and the closest answers we have (the slot), in the list and in the sheet
    const order = await p.evaluate(() => { const f = document.querySelector("#search-results .sr-fit"); return f ? [...f.children].map(e => (e.matches('.ins-slot[data-slot="found"]') && e.querySelector(".ins-found") ? "ins-found" : e.className.split(" ")[0])).filter(c => /sr-fit-none|ins-quick|ins-found/.test(c)).join(">") : ""; });
    await shot(p, w + "-papers-own-words");
    await p.keyboard.press("Enter"); await p.waitForSelector("#evsheet.open .ins-found-l li .pq", { timeout: 10000 }).catch(() => {});
    const inSheet = await p.evaluate(() => { const s = document.querySelector("#evsheet .ins"); return s ? { order: [...s.children].map(e => (e.matches('.ins-slot[data-slot="found"]') && e.querySelector(".ins-found") ? "ins-found" : e.className.split(" ")[0])).filter(c => /ins-none|ins-quick|ins-found/.test(c)).join(">"), quotes: [...s.querySelectorAll(".ins-found-l .pq")].map(x => x.textContent) } : null; });
    ok(w + " px: the papers stand under the line that says we have no answer of ours (and under the closest answers we have), each with its own words; Enter: the sheet shows the same, and the server is asked once, for the papers only (no model anywhere)",
      order === "sr-fit-none>ins-found" && inSheet && inSheet.order === "ins-none>ins-found" && inSheet.quotes.length === 2 && inSheet.quotes[1] === "\u201C\u2026the colour of the eye stayed the same after LSD on every photograph\u201D" && posts.length === 1 && /^find \{"names":\["lsd"\],"words":\["eye","colour"\]\}$/.test(posts[0]), JSON.stringify([order, inSheet, posts]));
    await p.keyboard.press("Escape"); await p.waitForTimeout(400);
    await p.fill("#search", "how much lsd kills you"); await p.waitForSelector("#search-results .sr-fit", { timeout: 20000 }); await p.waitForTimeout(2200);
    ok(w + " px: an amount that kills gets no papers this way (it waits for a person): the server is not even asked", posts.length === 1 && !(await p.$("#search-results .ins-found-l")), String(posts.length));
    // (2.20, after the sixth trial) nobody waits for a slow search: the list comes within about a second and says that we are still looking; the page asks
    // once more a moment later, and the whole list stands in the place of the first, the most cited first
    const look = () => p.evaluate(() => ({ rows: [...document.querySelectorAll("#search-results .ins-found-l li a")].map(a => a.textContent), wait: (document.querySelector("#search-results .ins-found-w") || {}).textContent || "" }));
    const t0 = Date.now(); await p.fill("#search", w === 1280 ? "does ketamine change your eye colour" : "does ketamine change your eye color"); await p.waitForSelector("#search-results .ins-found-l li", { timeout: 15000 }).catch(() => {});   // (another spelling at the second width: another search, slow once more)
    const firstAt = Date.now() - t0, first = await look(); await shot(p, w + "-papers-still-looking");
    await p.waitForFunction(() => !document.querySelector("#search-results .ins-found-w") && document.querySelectorAll("#search-results .ins-found-l li").length === 4, null, { timeout: 15000 }).catch(() => {});
    const whole = await look(), finds = posts.filter(x => /^find \{"names":\["ketamine"\]/.test(x)).length;
    ok(w + " px: the most cited papers are not waited for longer than two seconds: the list comes with a line that says we are still looking; a moment later the whole list stands in its place, the most cited first",
      firstAt < 3900 && first.rows.length === 3 && first.rows[0] === "Ketamine and eye colour: a newer paper" && /^Still looking for the most cited papers on this/.test(first.wait) && whole.rows.length === 4 && whole.rows[0] === "Ketamine and eye colour: the most cited paper" && whole.wait === "" && finds === 2, JSON.stringify([firstAt, first, whole, finds]));
    if (w === 1280) {
      /* (2.21.1, 18 November 2026, 15:40 Athens: Europe PMC took 25 seconds a search, and the page said "nothing was found on these words" of a question with 78
         papers.) The index says no: the page says that it did not answer, not that nothing was found. The index does not come back: the page says that it is
         still looking, then that the index is slow, asks on for some forty seconds, and then says that it did not answer, with a way to look again; "nothing
         was found" never stands there; "Look again" asks afresh and shows the list. */
      // (2.21.2, after the twelfth trial) what the page asks the index for: the names and key words it makes for a question
      const termsOf = q => p.evaluate(async q => insFindTerms(await insRank(q, {})), q), same = async (q, want) => { const got = await termsOf(q); return JSON.stringify(got) === JSON.stringify(want) ? "" : q + " -> " + JSON.stringify(got); };
      const wrong = (await Promise.all([
        same("why do people take drugs", { names: ["drug use", "substance use"], words: ["motives|reasons"], t: 1 }),
        same("why do some people get addicted and others don't", null),
        same("does trauma lead to addiction", { names: ["addiction", "substance use disorder"], words: ["trauma"], t: 1 }),
        same("does smoking weed while pregnant harm the baby", { names: ["cannabis", "thc", "cbd"], words: ["pregnancy|pregnant", "infants|baby"], t: 1 }),
        same("does drinking while breastfeeding harm the baby", { names: ["alcohol"], words: ["lactation|breastfeeding", "infants|baby"], t: 1 }),
        same("can teenagers get addicted to weed faster", { names: ["cannabis", "thc", "cbd"], words: ["adolescents|teenagers", "addiction|addicted"], t: 1 }),
        same("is tianeptine addictive", { names: ["tianeptine"], words: ["addiction|addictive"] }),
        // (2.22) a question of fact about dying or overdose: looked up under the words papers use, by title only; an amount that kills, a way of dying asked for on purpose, and ending a life are not
        same("can you die from lsd", { names: ["lsd"], words: ["mortality|deaths|fatal|die"], t: 1 }),
        same("how many people overdose on heroin each year in greece", { names: ["heroin"], words: ["overdose|overdoses|poisoning|overdose", "greece"], t: 1 }),
        same("how do people avoid an overdose", { names: ["drug overdose", "overdose"], words: ["prevention|prevent|avoid"], t: 1 }),
        same("does alcohol kill brain cells", { names: ["alcohol"], words: ["brain", "cells"] }),   // ("kill" said of a thing: no word about dying, no key word)
        same("how much lsd kills you", null), same("what is a painless way to die from pills", null), same("can cocaine make you kill yourself", null), same("how many pills of xanax is deadly", null),
        // (2.22) who uses more or less, with no drug word: drug use, by the words papers use for men and women
        same("do women use less than men", { names: ["drug use", "substance use"], words: ["women|female|women", "men|male|men"], t: 1 })])).filter(Boolean);
      ok("1280 px: the key words the page makes: 'why do people take drugs' is asked as the reasons for drug use; a key word that only says the subject again, and 'others', are none (nothing is looked up for 'why do some people get addicted and others don't'); a question about pregnancy or a child gets two key words, those about the pregnancy or the child first; drinking with no drug named is alcohol; (2.22) a question of fact about dying or overdose is asked under the words papers use, by title only, and an amount that kills or a way of dying is not looked up; who uses more is drug use", wrong.length === 0, wrong.join(" || "));
      const box = () => p.evaluate(() => { const b = document.querySelector("#search-results .ins-found"); return b ? b.textContent : ""; });
      await p.fill("#search", "does mescaline change your eye colour"); await p.waitForSelector("#search-results .ins-found [data-find-again]", { timeout: 15000 }).catch(() => {});
      const downTxt = await box();
      ok("1280 px: where the index of papers says no, the page says that it did not answer just now and offers to look again; it does not say that nothing was found", /^Europe PMC, the open index of medical research we search, did not answer just now, so we cannot say yet what is published on this\. Look again$/.test(downTxt), downTxt);
      EPMC_BACK.on = false; const seen = [], n0 = posts.length, t1 = Date.now();
      await p.fill("#search", "does psilocybin change your eye colour");
      let late = ""; while (Date.now() - t1 < 70000) { const x = await box(); if (x && seen[seen.length - 1] !== x) seen.push(x); if (/did not answer just now/.test(x)) { late = x; break; } await p.waitForTimeout(400); }
      const took = Date.now() - t1, asks = posts.length - n0; await shot(p, "1280-papers-index-slow");
      ok("1280 px: where the index does not come back, the page says that it is looking, then that the index is slow, asks on for some forty seconds (seven askings), and then says that it did not answer, with a way to look again; it never says that nothing was found",
        seen[0] === "Looking for published research on it\u2026" && seen.some(x => /^Still looking\. Europe PMC, the open index of research we search, is answering slowly right now/.test(x)) && !seen.some(x => /nothing was found/.test(x)) && /Look again$/.test(late) && asks === 7 && took > 35000 && took < 60000, JSON.stringify([seen, asks, took]));
      EPMC_BACK.on = true; await p.click("#search-results .ins-found [data-find-again]"); await p.waitForSelector("#search-results .ins-found-l li", { timeout: 15000 }).catch(() => {});
      const againRows = await p.evaluate(() => [...document.querySelectorAll("#search-results .ins-found-l li a")].map(a => a.textContent));
      ok("1280 px: 'Look again' asks afresh, and the list stands there when the index answers", againRows.length === 2 && againRows[0] === "Psilocybin and eye colour: a paper that came late" && posts.length === n0 + 8, JSON.stringify([againRows, posts.length - n0]));
    }
    EPMC_BACK.on = true;
    await p.context().close();
  }
  ok("no error in any page's console", errors.length === 0, errors.slice(0, 5).join(" || "));
  await browser.close(); ON.server.close(); OFF.server.close();
  console.log(fail ? fail + " of " + (pass + fail) + " checks failed" : "All " + (pass + fail) + " checks passed");
  process.exit(fail ? 1 : 0);
})();
