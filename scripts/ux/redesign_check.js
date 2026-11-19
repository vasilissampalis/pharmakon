// The pages of site 2.3 (scripts/ux/BRIEF-2.3-pages.md) checked in a real browser, at 390 x 844 and 1280 x 800 (the jumps
// also at 1600 x 900, where they used to end under the chips): every jump lands on the start of what it points to (nine
// kinds of link, with slow photos, no scroll anchoring as on an iPhone, and a block arriving late above the target); a drug
// page is its name, a description with its sources and the section menu, nothing else, the sections in the order worked out
// from the demand scores; a row opens its section alone, the list becomes chips, another row swaps, the open one brings the
// list back, the address carries it and Back and Forward walk through it; a question's address opens its section with the
// question open; one question is open at a time; "If it gets too much" runs from what helps to calling an ambulance, last,
// every line with its source chips; "Test kits" starts with buying and cites every line; the evidence and the answers carry
// no stamp and no search line, only a quiet version line in the deepest fold; "How to read this site" has no example; the
// menu has no doors to drug checking or the emergency numbers; the research page (Quick answers / Full evidence) is gone.
// Kept from redesign 2 (docs/REDESIGN-2.md): the Myth or fact? deck turns over and counts, Another 10 deals new cards (now
// the most interesting first, none under the cut of data/site/tf-interest.json), the Myth or fact? page is the same deck,
// endless; drug pages and the facts page have a deck of their own statements (none under 3); "Before, during and after" keeps
// its time order; Read next links work on the page, across its sections and across pages; the 100-dot picture; the start
// page at first paint; "Ask us" on drug pages and in search; keyboard focus is visible; dark theme; reduced motion.
// Every step also checks for horizontal scroll, and every page for console and page errors.
// It serves site/public itself (build first: node site/build.js && python3 -I site/build_public.py).
// Usage: node scripts/ux/redesign_check.js [--shots DIR] [--port N]   (exit code 1 if a check fails; images go to DIR only)
const http = require("http"), fs = require("fs"), path = require("path");
const { chromium } = require("playwright");
const ROOT = path.resolve(__dirname, "..", "..", "site", "public"), REPO = path.resolve(__dirname, "..", "..");
const arg = k => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : null; };
const SHOTS = arg("--shots"), PORT = +(arg("--port") || 0);
const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".mjs": "text/javascript", ".wasm": "application/wasm", ".json": "application/json", ".css": "text/css", ".webp": "image/webp", ".png": "image/png", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".txt": "text/plain", ".xml": "application/xml" };
const results = [], errors = [];
const ok = (name, pass, detail) => { results.push({ name, pass: !!pass, detail: detail || "" }); console.log((pass ? "PASS " : "FAIL ") + name + (detail ? "  (" + detail + ")" : "")); };
const readJson = f => { try { return JSON.parse(fs.readFileSync(path.join(REPO, f), "utf8")); } catch (e) { return null; } };
const TFI = readJson("data/site/tf-interest.json");   // the cards' interest scores, when the file exists

function serve() {
  if (!fs.existsSync(path.join(ROOT, "index.html"))) { console.error("No site/public/index.html: build first."); process.exit(2); }
  const server = http.createServer((req, res) => {
    let p = decodeURIComponent(req.url.split("?")[0]); if (p.endsWith("/")) p += "index.html";
    if (p === "/api/ask") { res.writeHead(200, { "Content-Type": "application/json" }); res.end('{"ok":false}'); return; }   // as the site's worker answers before its store is set up
    const f = path.join(ROOT, path.normalize(p));
    if (!f.startsWith(ROOT)) { res.writeHead(403); res.end(); return; }
    fs.readFile(f, (err, buf) => { if (err) { res.writeHead(404); res.end("not found"); return; } res.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream" }); res.end(buf); });
  });
  return new Promise(r => server.listen(PORT, "127.0.0.1", () => r(server)));
}
// Where a jump's target ended (run in the page): its top edge against the lowest bar stuck over it. A side column or a bar
// beside the target covers nothing; the floating "Ask or report" button sits at the bottom and is not a bar.
const landedAt = sel => {
  const el = typeof sel === "string" ? document.querySelector(sel) : null; if (!el || !el.getClientRects().length) return { missing: sel };
  const box = el.closest(".drawer .panel"), r = el.getBoundingClientRect(); let cover = box ? box.getBoundingClientRect().top : 0;
  (box || document.body).querySelectorAll("*").forEach(x => { const s = getComputedStyle(x); if (s.position !== "sticky" && s.position !== "fixed") return; if (x.contains(el) || el.contains(x)) return; if (!box && x.closest(".drawer")) return;
    const q = x.getBoundingClientRect(); if (q.height < 1 || q.bottom <= 0 || q.top > 220 || q.height > innerHeight / 2 || q.right <= r.left + 1 || q.left >= r.right - 1) return; if (q.bottom > cover) cover = q.bottom; });
  const sc = box || document.scrollingElement, end = Math.ceil(sc.scrollTop + sc.clientHeight) >= sc.scrollHeight - 2;
  return { top: Math.round(r.top), cover: Math.round(cover), gap: Math.round(r.top - cover), end, y: Math.round(sc.scrollTop) };
};
// a target has landed: its top edge shows just under the bars (or, at the very end of a page, as high as the page allows)
const good = m => m && !m.missing && m.gap >= 0 && (m.gap <= 40 || m.end);

(async () => {
  const server = await serve(), BASE = "http://127.0.0.1:" + server.address().port + "/#";
  if (SHOTS) fs.mkdirSync(SHOTS, { recursive: true });
  const browser = await chromium.launch({ args: ["--no-proxy-server"] });
  for (const w of [390, 1280, 1600]) {
    const H = w < 700 ? 844 : w > 1500 ? 900 : 800;
    // one browser context: its errors are collected, horizontal scroll is checked before every screenshot and at every step
    async function session(opts = {}) {
      const ctx = await browser.newContext({ viewport: { width: w, height: H }, deviceScaleFactor: 1, colorScheme: opts.dark ? "dark" : "light", reducedMotion: opts.reduce ? "reduce" : "no-preference", timezoneId: "Europe/Athens" });
      if (opts.storage) await ctx.addInitScript(st => { try { for (const [k, v] of Object.entries(st)) if (localStorage.getItem(k) == null) localStorage.setItem(k, v); } catch (e) { /* no storage */ } }, opts.storage);
      // as on an iPhone: nothing keeps the view in place when the layout above it changes; and photos arrive late
      if (opts.slow) { await ctx.addInitScript(() => document.addEventListener("DOMContentLoaded", () => { const st = document.createElement("style"); st.textContent = "* { overflow-anchor: none !important; }"; document.head.appendChild(st); }));
        await ctx.route(/\.webp$/, r => setTimeout(() => r.continue().catch(() => {}), 700)); }
      const p = await ctx.newPage(), tag = w + (opts.dark ? " dark" : "") + (opts.reduce ? " reduced-motion" : "");
      p.on("pageerror", e => errors.push(tag + " page error: " + String(e).slice(0, 200)));
      p.on("console", m => { if (m.type() === "error") errors.push(tag + " console error: " + m.text().slice(0, 200)); });
      const hscroll = async step => { const [sw, cw] = await p.evaluate(() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]); if (sw > cw) errors.push(tag + " horizontal scroll at " + step + ": " + sw + " > " + cw); };
      const shot = async (name, sel, full) => { await hscroll(name); if (!SHOTS || w > 1500) return; await p.mouse.move(2, 300); const f = path.join(SHOTS, w + "-" + name + ".png");
        if (sel) await (await p.$(sel)).screenshot({ path: f }); else await p.screenshot({ path: f, fullPage: !!full }); };
      const go = async (h, wait) => { await p.goto(BASE + h); await p.waitForTimeout(wait || 1100); };
      const hash = async (h, wait) => { await p.evaluate(x => { location.hash = x; }, "#" + h); await p.waitForTimeout(wait || 500); await hscroll(h); };
      const land = async (sel, wait) => { await p.waitForTimeout(wait == null ? 1500 : wait); await hscroll("landing " + sel); return p.evaluate(landedAt, sel); };
      return { ctx, p, shot, go, hash, hscroll, land };
    }
    const T = 650;   // the card turns in about half a second
    let s;

    // ================= 1. Every jump lands on the start of what it points to =================
    s = await session({ slow: true });
    const jumps = [], jump = (name, m) => { jumps.push([name, m]); if (!good(m)) console.log("   " + w + " " + name + ": " + JSON.stringify(m)); };
    // (a) a question link from the start page: an answer found by the search box (through the answer sheet, where it opens one)
    await s.go("home", 1300); await s.p.fill("#search", "does weed cause psychosis"); await s.p.waitForTimeout(900);
    const hit = await s.p.$('#search-results a[href^="#s-"]');
    if (hit) { await s.p.click('#search-results a[href^="#s-"]'); await s.p.waitForTimeout(700);   // (by its place in the list: Insight may draw the list again)
      const onPage = await s.p.$("#evsheet.open a[href^=\"#s-\"]"); if (onPage) await onPage.click();   // the sheet's "See it on the … page"
      jump("a question found from the start page", await s.land(".view.active .secs > .sec:not([hidden]) details.ask[open]")); }
    else jump("a question found from the start page", { missing: "no answer among the search results" });
    // (b) the deck's "Read the answer" (a link to #s-<drug>/q-<claim>, or to the facts, mixing or drug checking page)
    let read = null; await s.go("home", 900);
    for (let k = 0; k < 10 && !read; k++) { await s.p.click("#tf .qz2-o:not([disabled])"); await s.p.waitForTimeout(T);
      const h = await s.p.$eval("#tf .qz2-ev", a => a.getAttribute("href")); if (/^#s-[a-z0-9-]+\/q-/.test(h)) read = h; else { await s.p.click("#tf .qz2-nb"); await s.p.waitForTimeout(200); } }
    if (read) { await s.p.click("#tf .qz2-ev"); await s.p.waitForTimeout(700);
      const onPage = await s.p.$("#evsheet.open a[href^=\"#s-\"]"); if (onPage) await onPage.click();   // with Insight the answer opens over the deck first; its "See it on the … page" is the jump
      const m = await s.land(".view.active .secs > .sec:not([hidden]) details.ask[open]");
      m.addr = (await s.p.evaluate(() => location.hash)) === read; jump("Read the answer (" + read + ")", m.addr ? m : Object.assign(m, { missing: "address" })); }
    else jump("Read the answer", { missing: "no card of a drug page among the first ten" });
    // (c) a section link: "See all n forms" on the photo, and a section's bare name (#d-help)
    await s.go("s-cannabis", 1300); await s.p.click("#drug2 a.dh-forms"); jump("a section link (See all forms)", await s.land("#d-looks"));
    await s.hash("d-help", 100); jump("a section's bare name (#d-help)", await s.land("#d-help"));
    // (d) the section menu: a row, then a chip
    await s.go("s-cannabis", 1300); await s.p.click("#sm-d-risk"); jump("a row of the section menu", await s.land("#d-risk"));
    await s.p.click("#sm-d-med"); jump("a chip of the section menu", await s.land("#d-med"));
    // (e) opening a question, with another one open above it; then a block arrives late above it
    await s.p.click("#sm-d-risk"); await s.p.waitForTimeout(900);
    await s.p.click("#d-risk details.ask >> nth=1 >> summary"); await s.p.waitForTimeout(900);
    await s.p.click("#d-risk details.ask >> nth=5 >> summary"); const opened = await s.land("#d-risk details.ask[open]");
    opened.one = (await s.p.$$("#d-risk details.ask[open]")).length === 1; jump("opening a question (the one above closes)", opened.one ? opened : Object.assign(opened, { missing: "two open" }));
    await s.go("s-cannabis/q-cl_can_dependence_how_many", 200);
    await s.p.evaluate(() => setTimeout(() => { const d = document.createElement("div"); d.id = "late-block"; d.style.height = "320px"; const v = document.getElementById("drug2"); v.insertBefore(d, v.firstChild); }, 900));
    jump("a question's address, with a block arriving late above it", await s.land("#ask-cl_can_dependence_how_many", 2200));
    // (f) Read next: on the same section, and on another section of the page (LSD's myth sits under another section)
    await s.go("s-cannabis/q-cl_can_dependence_how_many", 1200); await s.p.click("#ask-cl_can_dependence_how_many .rn-l a >> nth=0"); jump("Read next, same section", await s.land("#d-risk details.ask[open]"));
    await s.go("s-lsd", 1200);
    const cross = await s.p.evaluate(() => { for (const a of document.querySelectorAll("#drug2 .rn-l a[data-open]")) { const t = document.getElementById(a.dataset.open), from = a.closest(".secs > .sec"); if (t && from && t.closest(".secs > .sec") !== from) return { from: from.id, q: a.closest("details.ask").id, to: t.id, sec: t.closest(".secs > .sec").id }; } return null; });
    if (cross) { await s.hash("s-lsd/q-" + cross.q.slice(4), 1200); await s.p.click("#" + cross.q + ' .rn-l a[data-open="' + cross.to + '"]'); const m = await s.land("#" + cross.to);
      const st = await s.p.evaluate(c => ({ open: document.getElementById(c.to).open, sec: openSec(), hash: location.hash }), cross);
      jump("Read next, another section (" + cross.from + " to " + cross.sec + ")", st.open && st.sec === cross.sec && st.hash === "#s-lsd/q-" + cross.to.slice(4) ? m : Object.assign(m, { missing: JSON.stringify(st) }));
      await s.p.goBack(); await s.p.waitForTimeout(700); const back = await s.p.evaluate(() => openSec());
      ok(w + ": Back after a Read next into another section returns to the section the reader was in", back === cross.from, back + " (was " + cross.from + ")"); }
    // (g) a link from the menu: the page starts at its top, its heading clear of the bar
    await s.p.click("#menubtn"); await s.p.waitForTimeout(250); await s.p.click('#menu a[href="#methods"]'); await s.p.waitForTimeout(900);
    const top = await s.p.evaluate(landedAt, "#view-methods h1"); jumps.push(["a link from the menu", top]);
    const topOk = top && !top.missing && top.y === 0 && top.gap >= 0 && top.top < H / 2; if (!topOk) console.log("   " + w + " menu link: " + JSON.stringify(top));
    // (h) other pages: a glossary term, a question on the facts page, the answers on test kits, a pair on the mixing page
    await s.go("g-3", 300); jump("a glossary term", await s.land("#g-3"));
    const fq = await s.p.evaluate(() => { const q = drugQuestions(GEN); return q.length ? q[Math.min(6, q.length - 1)][0] : null; });
    if (fq) { await s.go("facts/q-" + fq, 300); jump("a question on the facts page", await s.land("#fx-" + fq)); }
    await s.go("checking/kits", 300); jump("the answers on test kits", await s.land("#c-work"));
    // (i) inside the answer sheet: the source named after a "How do we know?" point
    await s.go("s-cannabis/q-cl_can_dependence_how_many", 1200); await s.p.click("#ask-cl_can_dependence_how_many .howsrc a"); await s.p.waitForTimeout(1600);
    jump("a source inside the answer sheet", await s.p.evaluate(landedAt, "#evsheet.open .ev-src.hit"));
    ok(w + ": every jump lands on the start of what it points to, just under the stuck bars (" + jumps.length + " kinds of link; slow photos, no scroll anchoring, a block arriving late)",
      jumps.length >= 14 && jumps.every(([n, m]) => n === "a link from the menu" ? topOk : good(m)), jumps.map(([n, m]) => n + ": " + (m.missing ? "MISSING " + m.missing : m.gap + (m.end ? " (end)" : ""))).join("; "));
    const marg = await s.p.evaluate(() => { const v = getComputedStyle(document.documentElement).getPropertyValue("--stick-h"), d = document.querySelector(".view.active details.ask");
      return { v: v.trim(), same: !!d && getComputedStyle(d).scrollMarginTop === v.trim(), pad: getComputedStyle(document.documentElement).scrollPaddingTop }; });
    ok(w + ": the offset is one variable (--stick-h), carried by the targets as scroll-margin-top; the page's scroll padding is off", /^\d+px$/.test(marg.v) && marg.same && (marg.pad === "0px" || marg.pad === "auto"), JSON.stringify(marg));
    await s.ctx.close();
    if (w > 1500) continue;   // the wide window is here for the jumps only

    // ================= pages render (a smoke pass over the main views) =================
    s = await session();
    await s.go("home");
    const views = [["home", "view-home"], ["quiz", "view-quiz"], ["s-cannabis", "view-drug"], ["s-lsd", "view-drug"], ["s-mdma", "view-drug"], ["s-heroin", "view-drug"], ["s-2c-x", "view-drug"], ["facts", "view-facts"],
      ["checking/kits", "view-checking"], ["interactions", "view-interactions"], ["emergency", "view-emergency"], ["howto", "view-howto"], ["methods", "view-methods"], ["substances", "view-substances"], ["a/lsd/cl_lsd_chromosomes", "view-shared"]];
    const wrong = [];
    for (const [h, v] of views) { await s.hash(h, 400); const a = await s.p.evaluate(() => (document.querySelector(".view.active") || {}).id); if (a !== v) wrong.push(h + " -> " + a); }
    ok(w + ": main views render", !wrong.length, wrong.join("; "));
    // each drug has one page: the research page's addresses lead to it
    const old = [];
    for (const [h, want] of [["s-cannabis/evidence", "#s-cannabis"], ["s-mdma/sec-13", "#s-mdma/part-d-law"], ["s-mdma/sec-5", "#s-mdma"], ["s-ketamine/not-yet", "#s-ketamine"], ["s-mdma/part-d-safer", "#s-mdma/part-d-safer"]]) {
      await s.hash(h, 500); old.push(await s.p.evaluate(want => ({ ok: location.hash === want && document.querySelector(".view.active").id === "view-drug", hash: location.hash, sec: openSec() }), want)); }
    const gone = await s.p.evaluate(() => ({ view: !!document.getElementById("view-monograph"), sw: document.querySelectorAll(".modebtn, .modebar").length, deep: !!document.querySelector("#drug2 .deep"), link: document.querySelectorAll('a[href$="/evidence"]').length }));
    const words = await s.p.evaluate(() => { const t = document.querySelector("main").textContent; return (t.match(/Quick answers|Someone unwell\?|At a glance|A real example|Want the details\?|All the research on/g) || []).concat([...document.querySelectorAll(".glance2, .dh-help, #howto-example, .readprog, #quick, #full, #toc")].map(e => e.className || e.id)); });
    ok(w + ": nothing on any page of the Quick/Full switch, the research page, \"Someone unwell?\", At a glance, the how-to example or \"Want the details?\"", !words.length, [...new Set(words)].join(", "));
    ok(w + ": each drug has one page: no Quick/Full switch, no research page; its old addresses lead to the drug page (section 13 to the law, the old Staying safer to Test kits)",
      old.every(x => x.ok) && old[1].sec === "d-law" && old[4].sec === "d-kits" && !gone.view && !gone.sw && !gone.deep && !gone.link, old.map(x => x.hash).join(", ") + " " + JSON.stringify(gone));
    await s.ctx.close();

    // ================= 2. The drug page: a description, a menu, one section at a time =================
    s = await session();
    await s.go("s-cannabis", 1300); await s.shot("drug-first-view"); if (w === 390) await s.shot("drug-first-view-full", null, true);
    const fv = await s.p.evaluate(() => { const page = document.getElementById("drug2"), kids = [...page.children].map(e => e.tagName.toLowerCase() + (e.classList[0] ? "." + e.classList[0] : "")), desc = page.querySelector(".dh-desc");
      const rows = [...page.querySelectorAll("#secmenu .sm-b")];
      return { kids: kids.join(" "), h1: page.querySelector(".dh h1").textContent, aka: (page.querySelector(".dh-aka") || {}).textContent || "", desc: desc ? desc.textContent.trim() : "", chips: desc ? desc.querySelectorAll(".srcs2 .srcl").length : 0,
        unwell: /someone unwell/i.test(page.textContent) || !!page.querySelector(".dh-help"), glance: !!page.querySelector(".glance2, .in-key, .dh-key"), prog: !!page.querySelector(".readprog, #pgprog"),
        shown: [...page.querySelectorAll(".secs > .sec")].filter(x => !x.hidden).length, secs: page.querySelectorAll(".secs > .sec").length, nav: page.querySelector("#secmenu").getAttribute("aria-label"),
        rows: rows.map(b => ({ sec: b.dataset.sec, tag: b.tagName, exp: b.getAttribute("aria-expanded"), ctl: b.getAttribute("aria-controls"), name: (b.querySelector(".sm-n") || {}).textContent, n: (b.querySelector(".sm-c") || {}).textContent || "", line: (b.querySelector(".sm-l") || {}).textContent || "", h: Math.round(b.getBoundingClientRect().height) })),
        asks: Object.fromEntries([...page.querySelectorAll(".secs > .sec")].map(x => [x.id, x.querySelectorAll("details.ask").length])), sticky: getComputedStyle(page.querySelector("#secmenu")).position }; });
    ok(w + ": a drug page is its name, its other names and a description with its sources, then the section menu and nothing else (no \"Someone unwell?\", no At a glance, no count of answers opened)",
      /^header\.dh (?:p|div)\.dh-desc nav\.secmenu div\.secs section\.sec h2\.qh div\.popular$/.test(fv.kids) && /Cannabis/.test(fv.h1) && /^Also called /.test(fv.aka) && fv.desc.length > 40 && fv.chips >= 1 && !fv.unwell && !fv.glance && !fv.prog && fv.shown === 0,
      fv.kids + " | " + fv.desc.slice(0, 60) + "… | " + fv.chips + " source chips");
    const rowsOk = fv.rows.length >= 6 && fv.rows.length === fv.secs && fv.rows.every(r => r.tag === "BUTTON" && r.exp === "false" && r.ctl === r.sec && r.name && r.line && r.h >= 56)
      && fv.rows.every(r => /^d-(risk|after|mix|med|feel)$/.test(r.sec) ? r.n === fv.asks[r.sec] + (fv.asks[r.sec] === 1 ? " answer" : " answers") : true) && fv.sticky !== "sticky";
    ok(w + ": the section menu is a list of large rows, each a button that says whether its section is open: name, how many answers, a quiet line of what is inside", rowsOk && /sections/i.test(fv.nav || ""),
      fv.rows.map(r => r.name + (r.n ? " [" + r.n + "]" : "")).join(" | "));
    // the order: the kinds of section that hold answers by the sum of their answers' demand scores over all drugs, then looks,
    // law and the cards, and last "If it gets too much", "Test kits", "Doses"; the same on every page
    const order = await s.p.evaluate(() => { const sum = { "d-risk": 0, "d-after": 0, "d-mix": 0, "d-med": 0, "d-feel": 0 }, sc = id => DEMAND[id] && typeof DEMAND[id].score === "number" ? DEMAND[id].score : 0;
      SUBSTANCES.forEach(x => { drugQuestions(x.slug).forEach(([id, , t]) => { const z = topicZone(t); if (z !== "mix") sum["d-" + z] += sc(id); }); mixQuestions(x.slug).forEach(([id]) => { sum["d-mix"] += sc(id); }); });
      return { sum, want: Object.keys(sum).sort((a, b) => sum[b] - sum[a]).concat(["d-auto", "d-looks", "d-law", "d-quiz", "d-help", "d-kits", "d-doses"]) }; });      // ("d-auto": what our system wrote about the drug, after the checked answers and before the rest; a page has it since 16 November 2026)
    const pages = [];
    for (const slug of ["cannabis", "mdma", "heroin", "lsd", "alcohol", "ketamine", "2c-x"]) { await s.hash("s-" + slug, 350); pages.push([slug, await s.p.evaluate(() => [...document.querySelectorAll("#secmenu .sm-b")].map(b => b.dataset.sec))]); }
    const inOrder = pages.every(([, got]) => got.join() === order.want.filter(id => got.includes(id)).join());
    ok(w + ": the sections come in one order on every drug page: by how much people ask (the sum of the demand scores), then looks, the law and the cards, and last If it gets too much, Test kits, Doses",
      inOrder && order.want.slice(-3).join() === "d-help,d-kits,d-doses" && pages[0][1].slice(-3).join() === "d-help,d-kits,d-doses", order.want.join(" > ") + " | sums " + JSON.stringify(order.sum));
    // a row opens its section alone; the list becomes chips; another swaps; the open one brings the list back
    await s.hash("s-cannabis", 500); await s.p.click("#sm-d-risk"); await s.p.waitForTimeout(900);
    const state = () => s.p.evaluate(() => { const nav = document.getElementById("secmenu"), open = [...document.querySelectorAll("#drug2 .secs > .sec")].filter(x => !x.hidden).map(x => x.id), b = nav.querySelector('.sm-b[aria-expanded="true"]');
      return { hash: location.hash, open: open.join(), exp: [...nav.querySelectorAll('.sm-b[aria-expanded="true"]')].map(x => x.dataset.sec).join(), chips: nav.classList.contains("on"), pos: getComputedStyle(nav).position, navH: Math.round(nav.getBoundingClientRect().height),
        label: b ? b.innerText.trim() : "", up: (nav.querySelector(".sm-up") || {}).offsetParent ? nav.querySelector(".sm-up").innerText.trim() : "", focus: document.activeElement.id || document.activeElement.tagName,
        inRow: b ? b.getBoundingClientRect().left >= 0 && b.getBoundingClientRect().right <= innerWidth + 1 : null }; });
    const a1 = await state(), l1 = await s.p.evaluate(landedAt, "#d-risk");
    await s.shot("section-open");
    await s.p.click("#sm-d-med"); await s.p.waitForTimeout(900); const a2 = await state(), l2 = await s.p.evaluate(landedAt, "#d-med");
    await s.p.click("#sm-d-med"); await s.p.waitForTimeout(900); const a3 = await state(), l3 = await s.p.evaluate(landedAt, "#secmenu");
    ok(w + ": a row opens its section alone and the list becomes a row of chips stuck under the header, the drug's name first; the address carries the section; the heading takes the focus",
      a1.hash === "#s-cannabis/part-d-risk" && a1.open === "d-risk" && a1.exp === "d-risk" && a1.chips && a1.pos === "sticky" && a1.navH < 80 && a1.label === "Risks" && a1.up === "Cannabis" && a1.focus === "d-risk-h" && a1.inRow && good(l1), JSON.stringify(a1));
    ok(w + ": another chip closes the first section and opens the new one at its start; the open one again closes it and brings the list back, at the row just left",
      a2.hash === "#s-cannabis/part-d-med" && a2.open === "d-med" && a2.exp === "d-med" && good(l2) && a3.hash === "#s-cannabis" && a3.open === "" && a3.exp === "" && !a3.chips && a3.pos !== "sticky" && a3.focus === "sm-d-med" && good(l3), JSON.stringify(a2) + " " + JSON.stringify(a3));
    const hist = [];
    for (const step of ["back", "back", "back", "forward", "forward"]) { await (step === "back" ? s.p.goBack() : s.p.goForward()); await s.p.waitForTimeout(600); hist.push((await state()).open || "list"); }
    ok(w + ": Back and Forward walk through the sections", hist.join() === "d-med,d-risk,list,d-risk,d-med", hist.join(" > "));
    await s.p.click("#secmenu .sm-up"); await s.p.waitForTimeout(700); const up = await state();
    ok(w + ": the drug's name, first among the chips, brings the list back", up.open === "" && up.hash === "#s-cannabis", JSON.stringify({ hash: up.hash, open: up.open }));
    // a question's address opens its section with the question open and in view; topics are plain headings; one question at a time
    await s.go("s-cannabis/q-cl_can_dependence_how_many", 1300);
    const dq = await s.p.evaluate(() => { const d = document.getElementById("ask-cl_can_dependence_how_many"), sec = d.closest(".secs > .sec");
      return { open: d.open, sec: sec.id, shown: !sec.hidden, others: [...document.querySelectorAll("#drug2 .secs > .sec")].filter(x => !x.hidden).length, focus: document.activeElement === d.querySelector("summary"),
        topics: [...sec.querySelectorAll(".sec-b > h3.tp")].map(h => h.textContent), tap: sec.querySelectorAll(".sec-b > h3.tp button, .sec-b > h3.tp a, .sec-b > details:not(.ask)").length, more: sec.querySelectorAll(".morebtn, .asks-more").length, asks: sec.querySelectorAll("details.ask").length }; });
    const dql = await s.p.evaluate(landedAt, "#ask-cl_can_dependence_how_many");
    await s.shot("question-after-deep-link");
    ok(w + ": a question's address opens its section with the question open and in view", dq.open && dq.sec === "d-risk" && dq.shown && dq.others === 1 && dq.focus && good(dql), JSON.stringify(Object.assign({}, dq, { topics: dq.topics.length })) + " gap " + dql.gap);
    ok(w + ": inside a section, topics are plain headings and every question shows: nothing between a section and its questions to tap", dq.topics.length >= 3 && dq.tap === 0 && dq.more === 0 && dq.asks > 10, dq.topics.length + " topics (" + dq.topics.slice(0, 4).join(", ") + "…), " + dq.asks + " questions");
    await s.p.click("#d-risk details.ask >> nth=3 >> summary"); await s.p.waitForTimeout(1200);
    const one = await s.p.evaluate(() => [...document.querySelectorAll("#d-risk details.ask[open]")].map(d => d.id)), onel = await s.p.evaluate(landedAt, "#d-risk details.ask[open]");
    ok(w + ": one question is open at a time: opening another closes the first, and the new one starts in view", one.length === 1 && one[0] !== "ask-cl_can_dependence_how_many" && good(onel), one.join() + " gap " + onel.gap);
    // an answer's own address: its page and section, with its evidence over it
    await s.go("home", 300); await s.go("cl_can_cbd_epilepsy", 1500);
    const own = await s.p.evaluate(() => ({ view: document.querySelector(".view.active").id, sec: openSec(), q: (document.getElementById("ask-cl_can_cbd_epilepsy") || {}).open, sheet: !!document.querySelector("#evsheet.open") }));
    ok(w + ": an answer's own address opens its drug page at the question, with the evidence over it", own.view === "view-drug" && own.sec === "d-med" && own.q && own.sheet, JSON.stringify(own));
    // "Before, during and after" keeps its time order: before and during, the day after, after stopping, each in the editors' order
    const seq = [];
    for (const slug of ["psilocybin", "methamphetamine", "alcohol"]) {
      await s.go("s-" + slug, 700);
      seq.push([slug, await s.p.evaluate(slug => { const want = [/^before/i, /day after/i, /after stopping/i].flatMap(re => drugQuestions(slug).filter(([, , t]) => topicZone(t) === "after" && re.test(t))).map(x => "ask-" + x[0]);
        const got = [...document.querySelectorAll("#d-after details.ask")].map(d => d.id); return want.length > 1 && got.join() === want.join() ? got.length : -1; }, slug)]);
    }
    ok(w + ": Before, during and after keeps its time order (psilocybin, methamphetamine, alcohol)", seq.every(([, n]) => n > 1), seq.map(([k, n]) => k + " " + n + " questions").join(", "));
    // within the other sections: the topics by their most-asked answer, each topic's answers from most to least asked
    await s.go("s-mdma/part-d-risk", 900);
    const dem = await s.p.evaluate(() => { const sc = id => DEMAND[id] && typeof DEMAND[id].score === "number" ? DEMAND[id].score : -1, groups = []; let cur = null;
      [...document.querySelectorAll("#d-risk .sec-b > *")].forEach(el => { if (el.matches("h3.tp")) { cur = []; groups.push(cur); } else if (cur) el.querySelectorAll("details.ask").forEach(d => cur.push(sc(d.dataset.cid || d.id.slice(4)))); });
      const best = groups.map(g => Math.max(...g)); return { groups: groups.length, within: groups.every(g => g.every((v, i) => !i || g[i - 1] >= v)), between: best.every((v, i) => !i || best[i - 1] >= v), best: best.join(" ") }; });
    ok(w + ": in a section, the topic with the most-asked answer comes first and each topic runs from most to least asked (MDMA)", dem.groups > 3 && dem.within && dem.between, dem.groups + " topics, best scores " + dem.best);
    await s.ctx.close();

    // ================= 3. If it gets too much =================
    s = await session();
    await s.go("s-cannabis/part-d-help", 1300); await s.shot("if-it-gets-too-much"); if (w === 390) await s.shot("if-it-gets-too-much-full", "#d-help");
    const helpAt = () => s.p.evaluate(() => { const b = document.querySelector("#d-help .sec-b"); if (!b) return null; const heads = [...b.querySelectorAll("h3, h4")].map(h => h.textContent), lis = [...b.querySelectorAll("ul.sf-list > li")];
      return { title: document.querySelector("#d-help > h2").textContent.trim(), heads: heads.join(" > "), lines: lis.length, cited: lis.filter(li => li.querySelector(".srcs2 .srcl")).length, box: !!b.querySelector(".hp-now, .callbtn"), folds: b.querySelectorAll("details").length, fold: (d => d ? { open: d.open, label: d.querySelector("summary").textContent, lines: [...d.querySelectorAll("li")].map(li => li.firstChild.textContent.trim()), after: (d.previousElementSibling || {}).className || (d.previousElementSibling || {}).tagName } : null)(b.querySelector("details.hp-aid")),
        helps: (h => h ? [...h.nextElementSibling.querySelectorAll("li")].map(li => li.firstChild.textContent.trim()) : [])([...b.querySelectorAll("h4")].find(x => x.textContent === "What helps")),
        aidOpen: (h => h ? [...h.nextElementSibling.querySelectorAll("li")].map(li => li.firstChild.textContent.trim()) : [])([...b.querySelectorAll("h4")].find(x => x.textContent === "If they pass out or stop breathing")),
        srcList: /Sources \(\d+\)/.test(b.textContent), note: /our editor has not checked|official and non-profit/i.test(b.textContent), first: lis[0] ? lis[0].textContent : "", num: (b.querySelector(".hp-num") || {}).textContent || "", more: (b.querySelector(".hp-more a") || {}).getAttribute ? b.querySelector(".hp-more a").getAttribute("href") : "",
        last: b.lastElementChild.className, tel: !!b.querySelector('.hp-num a[href^="tel:"]'), elsewhere: document.querySelectorAll('#drug2 a[href^="tel:"], #drug2 .callbtn').length - b.querySelectorAll('a[href^="tel:"]').length }; });
    const hp = await helpAt();
    const self = await s.p.evaluate(() => !!((STAY_SAFER.signs[subBySlug.cannabis.cls] || {}).self || []).length);
    ok(w + ": If it gets too much: " + (self ? "for you, then " : "") + "for a friend (what helps, what not to do), calling an ambulance last, then first aid behind one closed fold; no box",
      hp && hp.title === "If it gets too much" && hp.heads === (self ? "For you > " : "") + "For a friend > What helps > What not to do > Call an ambulance if" && !hp.box && hp.folds === 1 && hp.fold && !hp.fold.open && hp.fold.label === "If they pass out or stop breathing" && hp.fold.lines.length >= 1 && hp.last === "hp-more" && hp.more === "#emergency", hp ? hp.heads + " | fold: " + (hp.fold ? hp.fold.label + (hp.fold.open ? " (open)" : " (closed, " + hp.fold.lines.length + " lines)") : "none") + " | last: " + hp.last : "missing");
    ok(w + ": every line there carries its sources as chips; no \"Sources (n)\" list and no note on how the lines were checked", hp && hp.lines >= 8 && hp.cited === hp.lines && !hp.srcList && !hp.note, hp ? hp.cited + " of " + hp.lines + " lines cited" : "missing");
    // a chip shows the publisher, the page's title and the link; Escape or a second tap puts it away
    await s.p.click("#d-help .srcs2 button.srcl"); await s.p.waitForTimeout(300);
    const pop = await s.p.evaluate(() => { const p = document.querySelector(".popover.srclpop"), chip = document.querySelector("#d-help .srcs2 button.srcl"); if (!p) return null; const a = p.querySelector("a"), r = p.getBoundingClientRect();
      return { chip: chip.textContent, label: chip.getAttribute("aria-label"), pub: p.querySelector(".sp-pub").textContent, title: a.textContent, href: a.getAttribute("href"), blank: a.target === "_blank" && /noopener/.test(a.rel), inView: r.left >= 0 && r.right <= innerWidth + 1 && r.top >= 0 }; });
    await s.shot("source-chip-open");
    await s.p.keyboard.press("Escape"); await s.p.waitForTimeout(150); const popGone = await s.p.evaluate(() => !document.querySelector(".popover.srclpop"));
    ok(w + ": a source chip is the publisher's short name; a tap shows the publisher, the page's title and its link", pop && pop.chip.length <= 30 && pop.pub.includes(pop.chip.replace(/…$/, "")) && pop.label === "Source: " + pop.pub && pop.title.length > 2 && /^https:\/\//.test(pop.href) && pop.blank && pop.inView && popGone, pop ? pop.chip + " = " + pop.pub + " | " + pop.title : "no popover");
    await s.p.focus("#d-help .srcs2 button.srcl"); await s.p.keyboard.press("Enter"); await s.p.waitForTimeout(250);
    const kb = await s.p.evaluate(() => !!document.activeElement.closest(".popover.srclpop")); await s.p.keyboard.press("Escape"); await s.p.waitForTimeout(150);
    const kb2 = await s.p.evaluate(() => !document.querySelector(".popover.srclpop") && document.activeElement.classList.contains("srcl"));
    ok(w + ": with the keyboard, Enter on a chip opens its sources with the focus on the link, and Escape gives the focus back to the chip", kb && kb2, kb + ", " + kb2);
    // opioids (site 2.4): the page speaks to a friend first: when to call, then what helps with naloxone first, then the lines
    // for someone who has passed out or is not breathing, in sight; on every other page the calm lines come first and
    // those lines stay inside the closed fold
    await s.go("s-heroin/part-d-help", 1000); const hh = await helpAt();
    await s.go("s-mdma/part-d-help", 1000);
    const kinds = await s.p.evaluate(() => { const fold = /pass(?:ed)? out|won.t wake|not breathing|\bCPR\b|breathing is weak|has stopped/i, part = slug => { const f = STAY_SAFER.signs[subBySlug[slug].cls], k = x => x.kind || "calm", inFold = x => k(x) === "aid" && fold.test(x.line) && !/naloxone/i.test(x.line);
        return { open: f.while_waiting.filter(x => k(x) !== "aid").concat(f.while_waiting.filter(x => k(x) === "aid" && !inFold(x))).map(x => x.line), folded: f.while_waiting.filter(inFold).map(x => x.line) }; };
      return { heroin: part("heroin"), cannabis: part("cannabis") }; });
    const same = (a, b) => a.join("|") === b.join("|");
    const nalFirst = a => a.filter(x => /naloxone/i.test(x)).concat(a.filter(x => !/naloxone/i.test(x)));
    ok(w + ": what helps holds the calm and help lines; the lines for someone who has passed out or is not breathing are inside the closed fold, except on the opioid pages, which speak to a friend first: when to call an ambulance, what helps with naloxone first, then those lines in sight without opening anything, then what not to do",
      hh && /^For a friend > Call an ambulance if > What helps > If they pass out or stop breathing > What not to do/.test(hh.heads) && /^Give naloxone/.test(hh.helps[0] || "") && same(hh.helps, nalFirst(kinds.heroin.open)) && !hh.fold && hh.folds === 0 && same(hh.aidOpen, kinds.heroin.folded) && hh.aidOpen.some(x => /CPR/.test(x)) &&
      same(hp.helps, kinds.cannabis.open) && same(hp.fold.lines, kinds.cannabis.folded) && !hp.helps.some(x => /CPR|pass out/.test(x)),
      hh.heads + " | " + (hh.helps[0] || "").slice(0, 40) + "… | heroin: " + hh.helps.length + " lines of help, " + hh.aidOpen.length + " in sight for someone passed out, " + hh.folds + " folds | cannabis: " + hp.helps.length + " open, " + hp.fold.lines.length + " in the fold");
    // "For you" lines written from pages about cannabis are not shown for synthetic cannabinoids
    await s.go("s-synthetic-cannabinoids/part-d-help", 1000); const hs = await helpAt();
    ok(w + ": the cannabis page shows its \"For you\" lines; the synthetic cannabinoids page, whose sources they are not, shows none", self && /^For you/.test(hp.heads) && hs && /^For a friend/.test(hs.heads), "cannabis: " + hp.heads.split(" > ")[0] + " | synthetic cannabinoids: " + (hs ? hs.heads.split(" > ")[0] : "missing"));
    await s.ctx.close();
    // with the reader's country known: one line with the emergency number, and the quiet link; nowhere else on the page
    s = await session({ storage: { "pk-country": "Greece" } });
    await s.go("s-cannabis/part-d-help", 1300); const hg = await helpAt();
    ok(w + ": with the country known, one line gives its emergency number, last, with the quiet link to the numbers by country; the number is nowhere else on the page",
      hg && /The emergency number in Greece is 112\./.test(hg.num) && hg.tel && hg.last === "hp-more" && hg.elsewhere === 0 && !hg.box, hg ? hg.num.trim() + " | elsewhere " + hg.elsewhere : "missing");

    // ================= 4. Test kits =================
    await s.go("s-mdma/part-d-kits", 1300); await s.shot("test-kits"); if (w === 390) await s.shot("test-kits-full", "#d-kits");
    const kitsAt = () => s.p.evaluate(() => { const b = document.querySelector("#d-kits .sec-b"); if (!b) return null; const un = PREF_COUNTRY || guessCountry(), heads = [...b.querySelectorAll(":scope > h3")].map(h => h.textContent);
      const rows = [...b.querySelectorAll(".kit-row")], lis = [...b.querySelectorAll("ul.sf-list > li")], ships = TESTS_WORLD.sellers.filter(x => shipsTo(x, un)), want = ships.filter(x => ((typeof KIT_LINKS !== "undefined" && KIT_LINKS[norm(x.name)]) || {})[renderedDrug]);
      return { title: document.querySelector("#d-kits > h2").textContent.trim(), first: b.firstElementChild.textContent, heads: heads.join(" > "), rows: rows.length, want: want.length, where: (b.querySelector(".tk-cq .cq-where") || {}).textContent || "",
        ships: ships.length, links: rows.map(r => { const a = r.querySelector("a.kit-go"); return { name: a.querySelector(".kit-n").textContent, href: a.getAttribute("href"), blank: a.target === "_blank", label: (a.querySelector(".kit-l") || {}).textContent || "", cited: !!r.querySelector(".srcs2 .srcl"), sub: (r.querySelector(".kit-s") || {}).textContent || "" }; }),
        shops: Object.fromEntries(want.map(x => [x.name, x.url])), direct: Object.fromEntries(want.map(x => [x.name, ((typeof KIT_LINKS !== "undefined" && KIT_LINKS[norm(x.name)]) || {})[renderedDrug] || null])),
        lines: lis.length, cited: lis.filter(li => li.querySelector(".srcs2 .srcl")).length, srcList: /Sources \(\d+\)/.test(b.textContent), note: !!b.querySelector(".kit-note"), dc: !!b.querySelector('a[href="#checking"]') }; });
    const tk = await kitsAt();
    const linksOk = tk && tk.links.every(l => l.blank && !l.cited && tk.direct[l.name] && l.href === tk.direct[l.name].url && l.label && l.label === tk.direct[l.name].label);
    ok(w + ": Test kits is a section of its own and starts with buying: \"Test kits for MDMA\", one compact row per seller that sends to the reader's country and has a confirmed page for MDMA kits, each straight to that page, named by what is sold; no chips in the rows",
      tk && tk.title === "Test kits" && tk.first === "Test kits for MDMA" && tk.rows === tk.want && tk.rows >= 3 && tk.rows <= tk.ships && /Greece/.test(tk.where) && linksOk && tk.note, tk ? tk.rows + " of " + tk.ships + " sellers that send there; " + tk.links.map(l => l.name + ": " + l.label).slice(0, 2).join("; ") + " | " + tk.where.trim() : "missing");
    ok(w + ": then the facts about the tests, what home tests cannot tell, and drug checking; every line with its source chips, no \"Sources (n)\" list",
      tk && tk.heads === "Test kits for MDMA > Home tests > What home tests can’t tell you > Drug checking" && tk.lines >= 6 && tk.cited === tk.lines && !tk.srcList && tk.dc, tk ? tk.heads + " | " + tk.cited + " of " + tk.lines + " lines cited" : "missing");
    // another country: its sellers; a drug no home test works for has no buying block
    await s.p.click("#d-kits .tk-cq .cq-change"); await s.p.selectOption("#d-kits .tk-cq select", "Australia"); await s.p.waitForTimeout(500);
    const au = await kitsAt();
    await s.go("s-kratom/part-d-kits", 900); const kr = await kitsAt();
    await s.go("s-pcp/part-d-kits", 900); const pc = await kitsAt();
    ok(w + ": another country shows its own sellers; a drug no home test is shown to work for, or none is found for, has no buying block", au && /Australia/.test(au.where) && au.rows === au.want && kr && kr.rows === 0 && /^No home test has been shown to work/.test(kr.first) && pc && pc.rows === 0 && /^We have not found a home test/.test(pc.first),
      (au ? au.rows + " sellers for Australia" : "") + " | kratom: " + (kr ? kr.first.slice(0, 40) : "") + " | PCP: " + (pc ? pc.first.slice(0, 40) : ""));
    await s.ctx.close();
    // the drug checking page: the same lines for the reader's country, each with its sources, no list of sources
    s = await session({ storage: { "pk-country": "United Kingdom of Great Britain and Northern Ireland" } });
    await s.go("checking/part-c-kits", 1200);
    const dck = await s.p.evaluate(() => { const b = document.querySelector("#c-kits:not([hidden]) #dc-kitsbox .kw-box"); if (!b) return null; const lis = [...b.querySelectorAll("ul.sf-list > li, .kit-row")]; return { rows: b.querySelectorAll(".kit-row").length, lines: lis.length, cited: lis.filter(li => li.querySelector(".srcs2 .srcl")).length, srcList: /Sources \(\d+\)/.test(b.textContent) }; });
    ok(w + ": the drug checking page cites its test-kit lines the same way (in its section on test kits to use at home)", dck && dck.rows >= 2 && dck.cited === dck.lines && !dck.srcList, JSON.stringify(dck));
    await s.ctx.close();

    // ================= 5. The evidence and the answers: only what helps a reader =================
    s = await session();
    await s.go("cl_meth_psychosis_dose", 1300); await s.p.waitForFunction(() => document.querySelector("#evsheet.open") && !document.querySelector("#evsheet .loading"), null, { timeout: 15000 }).catch(() => {});
    const ev = await s.p.evaluate(() => { const sh = document.querySelector("#evsheet.open .panel"); if (!sh) return null; const t = sh.textContent, sci = sh.querySelector("details.sf-sci"), ver = sci && sci.querySelector(".verline"), refs = sh.querySelector(".ev-refs");
      return { stamp: !!sh.querySelector(".ev-stamp") || /approved by our editor|second AI reader/i.test(t), searched: /searched for newer research on|titles and abstracts screened|listed for reading/i.test(t), counts: /findings? used here|findings? from \d+ sources?/i.test(t), research: /all the research on/i.test(t),
        ver: ver ? ver.textContent : "", verShown: !!(ver && (ver.checkVisibility ? ver.checkVisibility() : ver.offsetParent)), sci: sci ? sci.querySelector("summary").textContent : "", under: !!(refs && sci && refs.compareDocumentPosition(sci) & Node.DOCUMENT_POSITION_FOLLOWING), pieces: sci ? sci.querySelectorAll(".ev-precise .pc-group, .ev-precise > p").length : 0,
        report: (sh.querySelector(".ev-foot [data-fb]") || {}).textContent, srcs: sh.querySelectorAll(".ev-refs li.ev-src").length }; });
    await s.shot("evidence");
    ok(w + ": the evidence carries no stamp (\"Approved by our editor … · version · n findings from m sources\"), no \"Searched for newer research\" line, no counts, no link to a research page",
      ev && !ev.stamp && !ev.searched && !ev.counts && !ev.research && ev.srcs >= 1 && ev.report === "Report a mistake in this answer", JSON.stringify(ev));
    ok(w + ": the version is one quiet line inside the deepest fold (Scientific detail, under the sources, in short pieces), with the date of the last search for newer research",
      ev && ev.sci === "Scientific detail" && ev.under && ev.pieces > 0 && !ev.verShown && /^Version \d+\.\d+\.\d+ · last search for newer research \d{1,2} \w{3} \d{4}$/.test(ev.ver), ev ? ev.ver : "missing");
    await s.p.evaluate(() => { const d = document.querySelector("#evsheet.open details.sf-sci"); d.open = true; d.scrollIntoView({ block: "start" }); }); await s.p.waitForTimeout(250); await s.shot("evidence-scientific-detail-open");
    // an answer card on a drug page, and a claim in full (the mixing table)
    await s.go("s-methamphetamine/q-cl_meth_psychosis_dose", 1200);
    const cardT = await s.p.evaluate(() => { const t = document.getElementById("ask-cl_meth_psychosis_dose").textContent; return /approved by our editor|second AI reader|searched for newer research|listed for reading|· v\d/i.test(t); });
    await s.go("interactions", 900);
    const mixOpen = await s.p.evaluate(() => { const d = document.querySelector("details.mixfull[data-full]"); if (!d) return false; for (let x = d; x; x = x.parentElement && x.parentElement.closest("details")) x.open = true; d.scrollIntoView({ block: "start" }); return true; });
    await s.p.waitForFunction(() => document.querySelector("details.mixfull[data-full][open] .claim"), null, { timeout: 15000 }).catch(() => {});
    const cl = await s.p.evaluate(() => { const c = document.querySelector("details.mixfull[data-full][open] .claim"); if (!c) return null; const v = c.querySelector(".cdetail .verline");
      return { stamp: !!c.querySelector(".stampline, .verif") || /approved by our editor|second AI reader ·|searched for newer research/i.test(c.textContent), ver: v ? v.textContent : "", fold: c.querySelector(".cdetail > summary").textContent }; });
    ok(w + ": an answer card and a claim in full carry no stamp and no search line either; the claim's version sits inside \"Precise statement, study details and sources\"", !cardT && mixOpen && cl && !cl.stamp && /^Version \d/.test(cl.ver) && /^Precise statement, study details and sources/.test(cl.fold), cl ? cl.ver + " | " + cl.fold : "missing");
    await s.ctx.close();

    // ================= 6. How to read this site, and How we check facts =================
    s = await session();
    await s.go("howto", 900); await s.shot("how-to-read"); if (w === 390) await s.shot("how-to-read-full", null, true);
    const ht = await s.p.evaluate(() => { const v = document.getElementById("view-howto"), t = v.textContent;
      return { h1: v.querySelector("h1").textContent, heads: [...v.querySelectorAll("h2")].map(h => h.textContent).join(" | "), use: v.querySelectorAll(".howsteps > li").length, seven: v.querySelectorAll("ol > li").length, example: !!v.querySelector("#howto-example, .claim") || /a real example/i.test(t),
        other: v.querySelectorAll("details, .eyebrow").length, old: /full evidence|five parts|is a draft|found a mistake/i.test(t), bars: /One to four bars/.test(t), evid: /“?"The evidence" shows the studies/.test(t) || /The evidence.{0,3} shows the studies/.test(t) }; });
    ok(w + ": How to read this site: four plain lines on using the site, then \"Linked to\" is not \"causes\" and the seven questions; no example, nothing else",
      ht.h1 === "How to read this site" && ht.heads === "\"Linked to\" is not \"causes\" | Seven questions to ask about any drug story" && ht.use === 4 && ht.seven === 7 && !ht.example && !ht.other && !ht.old && ht.bars && ht.evid, JSON.stringify(ht));
    await s.go("methods", 700);
    const me = await s.p.evaluate(() => /what to do if it gets too much, the lines on test kits and each drug's short description are sourced facts too:[^.]*checked at its source by a second AI reader/.test(document.getElementById("view-methods").textContent));
    ok(w + ": How we check facts says, once, how the lines on first aid, test kits and the descriptions are checked", me);
    await s.go("substances", 700);
    const fd = await s.p.evaluate(() => ({ labels: document.querySelectorAll("#subgrid .dt-st").length, tiles: document.querySelectorAll("#subgrid a.dcard").length, lede: document.querySelector("#view-substances .lede").textContent }));
    ok(w + ": Find a drug: no page-state labels on the tiles, no outdated note", fd.tiles === 30 && !fd.labels && !/first full page|basics for now/i.test(fd.lede), fd.tiles + " tiles; " + fd.lede);
    await s.ctx.close();

    // ================= the menu and the start page =================
    s = await session();
    await s.go("home"); await s.shot("home");
    if (w === 390) await s.shot("home-full", null, true);
    await s.p.$eval("#mf-h", h => h.scrollIntoView({ block: "start" })); await s.p.waitForTimeout(200); await s.shot("deck-card1-front");
    const first = await s.p.evaluate(() => { const h = document.getElementById("mf-h"), b = [...document.querySelectorAll("#mf-h ~ *")].map(e => e.className); let pv = h.previousElementSibling; while (pv && pv.hidden) pv = pv.previousElementSibling; return { heading: h.textContent, prev: pv ? pv.id : "", holds: !!(pv && pv.querySelector("#home-search")), order: b.slice(0, 3).join(" | ") }; });
    const doors = await s.p.evaluate(() => ({ home: document.querySelectorAll("#view-home a.do, #view-home a[href='#checking'], #view-home a[href='#emergency']").length, menu: document.querySelectorAll("#menu a.do, #menu a[href='#checking'], #menu a[href='#emergency']").length,
      foot: ["#emergency", "#checking"].map(h => document.querySelectorAll('footer.site a[href="' + h + '"]').length).join() }));
    ok(w + ": home shows Myth or fact? first under the search box (the reader's own questions, when there are any, stand between them); no door to drug checking or the emergency numbers on the start page or in the menu; both pages are in the footer",
      first.heading === "Myth or fact?" && first.prev === "insight-hero" && first.holds && /qz2 mf/.test(first.order) && doors.home === 0 && doors.menu === 0 && doors.foot === "1,1", first.prev + " | " + first.order + " | " + JSON.stringify(doors));
    // ---- the deck: turns over, counts, Previous, Another 10; each card drawn at random when it is reached (2.23.1), none under the cut
    const deck = [], verdicts = [], counts = [];
    const dealt = await s.p.evaluate(() => { const firsts = new Set(); for (let k = 0; k < 12; k++) { const st = { pool: mfPool(), n: 10, used: new Set(), cards: [], picks: [], pos: 0 }; mfFresh(st); firsts.add(st.cards[0].key); }
      return { firsts: firsts.size, drawn: MF.tf.cards.filter(Boolean).length, min: Math.min(...mfPool().map(x => x.i)), scored: mfPool().filter(x => x.i >= 0).length, pool: mfPool().length }; });
    if (TFI) ok(w + ": the deck draws each card at random when it is reached (the senior author, 19 November 2026: twelve new decks begin with many different cards; one card drawn at the start), never a card under the cut (data/site/tf-interest.json: interest " + TFI.cut.interest + ", clear " + TFI.cut.clear + ")",
      dealt.scored === dealt.pool && dealt.min >= TFI.cut.interest && dealt.firsts >= 8 && dealt.drawn === 1, JSON.stringify(dealt));
    let turned = true, during = true;
    for (let k = 1; k <= 10; k++) {
      deck.push(await s.p.$eval("#tf .mf-q", e => e.textContent)); counts.push(await s.p.$eval("#tf .qz2-score", e => e.textContent));
      await s.p.click("#tf .qz2-o >> nth=" + (k % 2));
      if (k === 1) during = await s.p.evaluate(() => { const c = document.querySelector("#tf .mf-card"); return c.classList.contains("out") && !c.classList.contains("flipped"); });
      await s.p.waitForTimeout(T);
      const st = await s.p.evaluate(() => { const c = document.querySelector("#tf .mf-card"); return { flipped: c.classList.contains("flipped"), back: !!document.querySelector("#tf .mf-back").offsetParent, front: !!document.querySelector("#tf .mf-front").offsetParent,
        verdict: document.querySelector("#tf .mf-v b").textContent, fb: document.querySelector("#tf .mf-fb").textContent, link: document.querySelector("#tf .qz2-ev").getAttribute("href"), bars: !!document.querySelector("#tf .mf-back .meter .mw"), next: (document.querySelector("#tf .qz2-nb") || {}).textContent }; });
      verdicts.push(st.verdict);
      if (!(st.flipped && st.back && !st.front && /^(Myth|Fact)$/.test(st.verdict) && /^(Right!|Not quite\.)$/.test(st.fb) && /^#/.test(st.link) && st.bars && st.next === (k < 10 ? "Next" : "Another 10"))) { turned = false; console.log("   card " + k + ": " + JSON.stringify(st)); }
      if (k <= 3) { await s.p.$eval("#tf", e => e.scrollIntoView({ block: "start" })); await s.p.waitForTimeout(150); await s.shot("deck-card" + k + "-back"); }
      if (k === 3) {   // back to card 2, which shows turned, then on again
        await s.p.click("#tf .qz2-prev"); await s.p.waitForTimeout(200);
        const back2 = await s.p.evaluate(() => [document.querySelector("#tf .qz2-score").textContent, document.querySelector("#tf .mf-card").classList.contains("flipped"), document.querySelector("#tf .mf-q").textContent]);
        ok(w + ": deck Previous shows the card before, already turned", back2[0] === "2 of 10" && back2[1] && back2[2] === deck[1], back2.slice(0, 2).join(", "));
        await s.p.click("#tf .qz2-nb"); await s.p.waitForTimeout(200);
      }
      if (k === 10) { await s.p.$eval("#tf .mf-nav", e => e.scrollIntoView({ block: "center" })); await s.p.waitForTimeout(150); await s.shot("deck-card10-back-another-10"); }
      if (k < 10) { await s.p.click("#tf .qz2-nb"); await s.p.waitForTimeout(150); }
    }
    ok(w + ": deck card turns over (verdict, why, bars, link) and turns with motion allowed", turned && during);
    ok(w + ": deck counts 1 of 10 to 10 of 10", counts.join(",") === Array.from({ length: 10 }, (_, i) => (i + 1) + " of 10").join(","), counts[0] + " ... " + counts[9]);
    ok(w + ": deck: 10 different statements, drawn at random", new Set(deck).size === 10, verdicts.filter(v => v === "Myth").length + " myths this time");
    await s.p.click("#tf .qz2-nb"); await s.p.waitForTimeout(300);
    const another = await s.p.evaluate(() => [document.querySelector("#tf .qz2-score").textContent, document.querySelector("#tf .mf-q").textContent]);
    ok(w + ": Another 10 deals new cards", another[0] === "1 of 10" && !deck.includes(another[1]), another[0]);
    await s.p.$eval("#mf-h", h => h.scrollIntoView({ block: "start" })); await s.p.waitForTimeout(150); await s.shot("deck-another-10-new-deck");
    await s.p.click(".qz2-more a"); await s.p.waitForTimeout(800);
    const quiz = await s.p.evaluate(() => ({ title: document.title, h1: document.querySelector("#view-quiz h1").textContent, menu: document.querySelector('#menu a[href="#quiz"]').textContent, foot: document.querySelector('footer a[href="#quiz"]').textContent, label: document.getElementById("quizpage").getAttribute("aria-label") }));
    ok(w + ": the quiz page loads under Myth or fact?", quiz.title === "Myth or fact? · Pharmakon" && quiz.h1 === "Myth or fact?" && quiz.menu === "Myth or fact?" && quiz.foot === "Myth or fact?", quiz.title + " | menu: " + quiz.menu);
    await s.shot("myth-or-fact-page");
    const asked = [], ends = [];
    const isDeck = await s.p.evaluate(() => { const b = document.querySelector("#quizpage.mf .mf-card"); return !!b && [...document.querySelectorAll("#quizpage .mf-front .qz2-o")].map(x => x.textContent).join("/") === "Myth/Fact" && !document.querySelector("#quizpage .qz2-ans"); });
    for (let k = 0; k < 25; k++) {
      const q = await s.p.$eval("#quizpage .qz2-q", e => e.textContent).catch(() => null); if (!q) break; asked.push(q);
      await s.p.click("#quizpage .qz2-o:not([disabled]) >> nth=0"); await s.p.waitForTimeout(k === 0 ? T : 60);
      if (k === 0) { ends.push(await s.p.evaluate(() => document.querySelector("#quizpage .mf-card").classList.contains("flipped") && /^(Myth|Fact)$/.test(document.querySelector("#quizpage .mf-v b").textContent))); await s.shot("myth-or-fact-page-answered"); }
      const nb = await s.p.$("#quizpage .qz2-nb"); if (!nb) break; if (k === 9 || k === 19) ends.push((await nb.textContent()) === "Another 10"); await nb.click(); await s.p.waitForTimeout(60);
    }
    ok(w + ": the Myth or fact? page is the same deck, endless (Another 10 after each ten), and asks nothing the start page's deck asked, nothing twice", isDeck && ends.length === 3 && ends.every(Boolean) && asked.length >= 25 && !asked.some(q => deck.includes(q)) && new Set(asked).size === asked.length, asked.length + " cards answered; turned and Another 10 twice: " + ends.join(","));
    await s.ctx.close();

    // ---- the menu: All drugs, Is it safe to mix? and Myth or fact? first, then the quieter links; the open page marked
    s = await session();
    await s.go("interactions"); await s.p.click("#menubtn"); await s.p.waitForTimeout(250);
    const mn = await s.p.evaluate(() => { const top = document.querySelector("#menu .menu-top"), links = [...top.querySelectorAll(":scope > a")];
      return { top: links.map(a => a.textContent.trim() + " " + a.getAttribute("href")).join(" | "), icons: links.every(a => !!a.querySelector(".mi svg")), more: [...document.querySelectorAll("#menu .menu-top + .menu-more > a:not([hidden])")].map(a => a.getAttribute("href")).join(" "),
        cur: (links.find(a => a.getAttribute("aria-current") === "page") || { getAttribute: () => "" }).getAttribute("href"), doors: document.querySelectorAll("#menu .menu-do, #menu a.do").length }; });
    await s.shot("menu-open");
    ok(w + ": menu: All drugs, Is it safe to mix? and Myth or fact? first, then the quieter links; no doors to drug checking or the emergency numbers; the open page marked",
      mn.top === "All drugs #substances | Is it safe to mix? #interactions | Myth or fact? #quiz" && mn.icons && /#about #methods #howto #glossary #numbers #law/.test(mn.more) && !/checking|emergency/.test(mn.top + mn.more) && mn.cur === "#interactions" && !mn.doors, JSON.stringify(mn));
    await s.p.click('#menu a[href="#substances"]'); await s.p.waitForTimeout(500);
    const after = await s.p.evaluate(() => ({ view: (document.querySelector(".view.active") || {}).id, closed: document.getElementById("menu").hidden }));
    ok(w + ": a link in the menu opens its page and closes the menu", after.view === "view-substances" && after.closed, JSON.stringify(after));
    await s.ctx.close();

    // ---- a drug page and the facts page have a deck of their own statements, as a section of the page; a page with fewer than 3 has none
    s = await session();
    await s.go("s-cannabis", 1300);
    const dk = await s.p.evaluate(() => { const st = MF["qz-drug"], mine = new Set(mfPagePool("cannabis").map(x => x.claim)), row = document.getElementById("sm-d-quiz");
      return { box: !!document.querySelector("#d-quiz #qz-drug.mf .mf-card"), row: row ? row.querySelector(".sm-c").textContent : "", n: st ? st.n : 0, own: st ? st.cards.every(x => mine.has(x.claim)) : false, pool: mine.size }; });
    await s.p.click("#sm-d-quiz"); await s.p.waitForTimeout(900); await s.p.click("#qz-drug .qz2-o >> nth=1"); await s.p.waitForTimeout(T);
    dk.turned = await s.p.evaluate(() => document.querySelector("#qz-drug .mf-card").classList.contains("flipped"));
    await s.shot("drug-page-myth-or-fact");
    ok(w + ": a drug page has its own Myth or fact? deck (its statements only), as a section with its row in the menu", dk.box && dk.row === dk.pool + " cards" && dk.own && dk.n === Math.min(10, dk.pool) && dk.turned, JSON.stringify(dk));
    const few = await s.p.evaluate(() => SUBSTANCES.map(x => x.slug).filter(x => drugQuestions(x).length && mfCount(mfPagePool(x)) < 3)[0] || null);
    if (few) { await s.go("home", 300); await s.go("s-" + few, 1000);
      const none = await s.p.evaluate(() => !document.querySelector("#d-quiz") && !document.getElementById("sm-d-quiz"));
      ok(w + ": a drug page with fewer than 3 statements has no Myth or fact? section (" + few + ")", none); }
    await s.go("facts", 1000);
    const fk = await s.p.evaluate(() => { const st = MF["qz-facts"], mine = new Set(mfPagePool(GEN).map(x => x.claim)); return { box: !!document.querySelector("#qz-facts.mf .mf-card"), own: st ? st.cards.every(x => mine.has(x.claim)) : false, n: st ? st.n : 0 }; });
    ok(w + ": the facts page ends with its own Myth or fact? deck", fk.box && fk.own && fk.n >= 3, JSON.stringify(fk));

    // ---- an open answer: the closed card's parts, the dots for "N in 100", Read next on the page and to another page
    await s.go("s-cannabis/q-cl_can_dependence_how_many", 1300);
    const card = await s.p.evaluate(() => { const d = document.getElementById("ask-cl_can_dependence_how_many"); if (!d) return null; const sm = d.querySelector("summary"), a = d.querySelector(".ask-a"), dots = a.querySelector(".freq .dots100");
      return { open: d.open, q: !!sm.querySelector(".ask-q"), short: !!sm.querySelector(".ask-s"), label: (sm.querySelector(".meter .mw") || {}).textContent, butFirst: a.firstElementChild.classList.contains("ask-but"), howFlat: !!a.querySelector("div.ask-how .ask-howl") && !a.querySelector("details"),
        dots: dots ? dots.querySelectorAll("i").length + "/" + dots.querySelectorAll("i.on").length + "/" + dots.getAttribute("aria-hidden") : "", words: (a.querySelector(".freq-row b") || {}).textContent, rn: a.querySelectorAll(".rn-l a").length }; });
    ok(w + ": closed card shows question, short answer, bars and label; open card starts with But, no third fold", card && card.q && card.short && /evidence/.test(card.label || "") && card.butFirst && card.howFlat, card ? "label " + card.label : "missing");
    ok(w + ": 100 dots for About 9 in 100 (9 filled, hidden from screen readers, words read out)", card && card.dots === "100/9/true" && card.words === "9 in 100", card ? card.dots + ' "' + card.words + '"' : "missing");
    await s.shot("cannabis-answer-9-in-100-open"); await s.shot("cannabis-answer-9-in-100-whole-card", "#ask-cl_can_dependence_how_many");
    await s.p.$eval("#ask-cl_can_dependence_how_many .rn", e => e.scrollIntoView({ block: "center" })); await s.p.waitForTimeout(200); await s.shot("cannabis-read-next");
    const links = await s.p.$$eval("#ask-cl_can_dependence_how_many .rn-l a", as => as.map(a => [a.getAttribute("href"), a.dataset.open, a.textContent]));
    ok(w + ": Read next has up to 3 titles: the topic's next answers, then a Myths and facts answer", links.length >= 1 && links.length <= 3, links.map(l => l[2]).join(" | "));
    await s.p.click("#ask-cl_can_dependence_how_many .rn-l a >> nth=0"); await s.p.waitForTimeout(1300);
    const r1 = await s.p.evaluate(id => ({ open: document.getElementById(id).open, prev: document.getElementById("ask-cl_can_dependence_how_many").open, hash: location.hash }), links[0][1]);
    ok(w + ": Read next opens an answer in the same section (this one closes, the address stays)", r1.open && !r1.prev && r1.hash === "#s-cannabis/q-cl_can_dependence_how_many", JSON.stringify(r1));
    await s.shot("cannabis-read-next-followed");
    const other = links.find(l => !l[0].startsWith("#s-cannabis/"));
    // (the same address again would not reopen the card the step before closed, so go by another address first)
    if (other) { await s.go("home", 400); await s.go("s-cannabis/q-cl_can_dependence_how_many", 1300); await s.p.click('#ask-cl_can_dependence_how_many .rn-l a[href="' + other[0] + '"]'); await s.p.waitForTimeout(1500);
      const r2 = await s.p.evaluate(dom => { const d = document.getElementById(dom); return { hash: location.hash, open: !!(d && d.open && d.closest(".view.active") && d.getClientRects().length) }; }, other[1]);
      ok(w + ": Read next opens an answer on another page, in its section", r2.hash === other[0] && r2.open, other[2] + " -> " + r2.hash); }
    // the dots made from a short answer's own words, and none for a range
    await s.go("s-heroin/q-cl_opi_naloxone_programs", 1300);
    const nal = await s.p.evaluate(() => { const a = document.querySelector("#ask-cl_opi_naloxone_programs .ask-a"); const d = a && a.querySelector(".dotpic .dots100"); return d ? d.querySelectorAll("i.on").length + ' "' + a.querySelector(".dotpic b").textContent + '"' : "none"; });
    ok(w + ': 100 dots from the words "At least 96 in 100"', nal === '96 "At least 96 in 100"', nal);
    await s.shot("heroin-answer-dots-from-words", "#ask-cl_opi_naloxone_programs");
    await s.go("s-cannabis/q-cl_can_cbd_epilepsy", 1300);
    const range = await s.p.evaluate(() => { const d = document.getElementById("ask-cl_can_cbd_epilepsy"); return d ? (/\d+ to \d+ in 100/.test(d.querySelector(".ask-s").textContent) ? (d.querySelector(".dotpic") ? "dots shown" : "no dots") : "no range in this answer") : "missing"; });
    ok(w + ': no dots for a range ("43 to 49 in 100")', range === "no dots", range);
    await s.ctx.close();

    // ---- keyboard: the deck, the section menu and an answer, with visible focus
    s = await session();
    await s.go("home");
    for (let i = 0; i < 14; i++) { await s.p.keyboard.press("Tab"); if (await s.p.evaluate(() => document.activeElement.classList.contains("qz2-o"))) break; }
    const f1 = await s.p.evaluate(() => [document.activeElement.textContent, getComputedStyle(document.activeElement).outlineStyle]);
    await s.shot("focus-deck-myth-button");
    await s.p.keyboard.press("Enter"); await s.p.waitForFunction(() => document.querySelector("#tf .mf-card.flipped"), null, { timeout: 4000 }).catch(() => {}); await s.p.waitForTimeout(150);
    const f2 = await s.p.evaluate(() => document.activeElement.className);
    await s.p.keyboard.press("Tab"); const f3 = await s.p.evaluate(() => document.activeElement.className);
    await s.p.keyboard.press("Tab"); await s.p.waitForTimeout(150);
    const f4 = await s.p.evaluate(() => [document.activeElement.className, document.activeElement.textContent, getComputedStyle(document.activeElement).outlineStyle]);
    await s.shot("focus-deck-next-button");
    ok(w + ": keyboard: Tab to Myth, Enter turns the card, Tab reaches Read the answer and Next, focus visible", f1[0] === "Myth" && f1[1] === "solid" && f2 === "mf-v" && /qz2-ev/.test(f3) && /qz2-nb/.test(f4[0]) && f4[2] === "solid", [f1.join(" "), f2, f3, f4.join(" ")].join(" > "));
    await s.go("s-cannabis"); await s.p.$eval("#drug2 .dh h1", h => { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); });
    let tabs = 0; for (; tabs < 30; tabs++) { await s.p.keyboard.press("Tab"); if (await s.p.evaluate(() => document.activeElement.classList.contains("sm-b"))) break; }
    await s.p.waitForTimeout(200);
    const f5 = await s.p.evaluate(() => [document.activeElement.id, getComputedStyle(document.activeElement).outlineStyle, document.activeElement.getAttribute("aria-expanded")]);
    await s.shot("focus-section-menu-row");
    await s.p.keyboard.press("Enter"); await s.p.waitForTimeout(900);
    const f6 = await s.p.evaluate(() => [document.activeElement.id, openSec(), document.querySelector('#secmenu .sm-b[aria-expanded="true"]').dataset.sec]);
    // the section's topic jumps (its groups of questions) come first, each with its focus visible; then the first question
    const passed = []; for (let k = 0; k < 60; k++) { await s.p.keyboard.press("Tab"); await s.p.waitForTimeout(80);
      const a = await s.p.evaluate(() => [document.activeElement.className, !!document.activeElement.closest("#d-risk details.ask"), getComputedStyle(document.activeElement).outlineStyle]); if (a[1]) break; passed.push(a[0] + ":" + a[2]); }
    const f7 = await s.p.evaluate(() => [document.activeElement.tagName, !!document.activeElement.closest("#d-risk details.ask"), getComputedStyle(document.activeElement).outlineStyle]);
    await s.p.keyboard.press("Enter"); await s.p.waitForTimeout(900);
    const f8 = await s.p.evaluate(() => [document.activeElement.tagName, document.activeElement.parentElement.open]);
    await s.shot("focus-answer-opened-from-keyboard");
    ok(w + ": keyboard: a row of the section menu takes focus visibly, Enter opens its section and the focus moves to its heading; Tab goes through the section's topic jumps (focus visible) to the first question, and Enter opens it",
      f5[0] === "sm-d-risk" && f5[1] === "solid" && f5[2] === "false" && f6.join() === "d-risk-h,d-risk,d-risk" && passed.every(x => x === "tpj-b:solid") && f7[0] === "SUMMARY" && f7[1] && f7[2] === "solid" && f8[0] === "SUMMARY" && f8[1], f5.join(" ") + " > " + f6.join(" ") + " > " + passed.length + " topic jumps " + [...new Set(passed)].join() + " > " + f7.join(" ") + " > " + f8.join(" "));
    await s.go("s-cannabis/q-cl_can_dependence_how_many", 1300);
    await s.p.$eval("#ask-cl_can_dependence_how_many .ask-ev", a => a.focus()); await s.p.keyboard.press("Tab"); await s.p.waitForTimeout(150);
    await s.p.evaluate(() => document.activeElement.scrollIntoView({ block: "center" })); await s.p.waitForTimeout(150);
    const f9 = await s.p.evaluate(() => !!document.activeElement.closest(".rn") && getComputedStyle(document.activeElement).outlineStyle === "solid");
    await s.shot("focus-read-next-link");
    ok(w + ": keyboard: Read next links follow The evidence, focus visible", f9);
    await s.ctx.close();

    // ---- the start page at first paint (before any script runs, with the deck's place held); "Ask us" at the end of a drug
    // page and of a search (the words typed come along into the message); the "Ask or report" labels
    { const ctx = await browser.newContext({ viewport: { width: w, height: H }, deviceScaleFactor: 1, javaScriptEnabled: false }), p0 = await ctx.newPage();
      await p0.goto(BASE.replace(/#$/, "")); await p0.waitForTimeout(300);
      const fp = await p0.evaluate(() => { const v = document.getElementById("view-home"), vis = el => !!(el && el.getBoundingClientRect().height > 0);
        return { active: v.classList.contains("active"), h1: vis(v.querySelector("h1")), mf: vis(document.getElementById("mf-h")), wait: vis(v.querySelector(".mf-wait")), doors: v.querySelectorAll("a.do").length, emergency: !!document.querySelector('footer.site a[href="#emergency"]') }; });
      ok(w + ": first paint, before the script: the start page with Myth or fact? (its place held); no help doors there; Emergency numbers in the footer", fp.active && fp.h1 && fp.mf && fp.wait && fp.doors === 0 && fp.emergency, JSON.stringify(fp));
      if (SHOTS) await p0.screenshot({ path: path.join(SHOTS, w + "-first-paint-home.png") }); await ctx.close(); }
    s = await session();
    await s.go("s-cannabis");
    const fl = await s.p.evaluate(() => { const f = document.querySelector(".view.active .fbline"); return f ? { t: f.querySelector("p").textContent, b: [...f.querySelectorAll("button")].map(x => x.textContent + "=" + x.dataset.fb).join(" | ") } : null; });
    ok(w + ": a drug page ends with Didn't find your question? Ask us (Ask a question first)", fl && /^Didn’t find your question\? Ask us/.test(fl.t) && fl.b === "Ask a question=feedback | Report a mistake=issue", fl ? fl.b : "missing");
    await s.p.$eval(".view.active .fbline", e => e.scrollIntoView({ block: "center" })); await s.p.waitForTimeout(200); await s.shot("drug-page-ask-us");
    await s.go("home", 700); await s.p.fill("#search", "cannabis sleep"); await s.p.waitForTimeout(700);
    const s1 = await s.p.evaluate(() => { const r = document.getElementById("search-results"), a = r.querySelector(".sr-ask"); return { n: r.querySelectorAll("a").length, ask: a && a.textContent, last: r.lastElementChild === a }; });
    await s.shot("search-results-ask-us");
    await s.p.fill("#search", "zzqx blorptang"); await s.p.waitForTimeout(700);
    const s2 = await s.p.evaluate(() => { const r = document.getElementById("search-results"); return { none: !!r.querySelector(".none"), ask: (r.querySelector(".sr-ask") || {}).textContent }; });
    await s.shot("search-none-ask-us");
    await s.p.click("#search-results .sr-ask button"); await s.p.waitForTimeout(400);
    const pn = await s.p.evaluate(() => ({ open: document.getElementById("report").classList.contains("open"), title: document.getElementById("fb-title").textContent, opts: [...document.querySelectorAll(".fb-opt")].map(b => b.dataset.mode).join(","),
      mode: (document.querySelector('.fb-opt[aria-pressed="true"]') || { dataset: {} }).dataset.mode, msg: document.getElementById("report-message").value }));
    await s.shot("panel-ask-prefilled");
    ok(w + ": search ends with Ask us (and with it when nothing matched); Ask us opens Ask a question with the words typed", s1.n > 0 && /^Not what you were looking for\? Ask us/.test(s1.ask || "") && s1.last && s2.none && /^Didn’t find your question\? Ask us/.test(s2.ask || "") &&
      pn.open && pn.title === "Ask or report" && pn.opts === "feedback,issue" && pn.mode === "feedback" && pn.msg === "zzqx blorptang", s1.n + " results; " + JSON.stringify(pn));
    await s.p.keyboard.press("Escape"); await s.p.waitForTimeout(300);
    const lab = await s.p.evaluate(() => [document.querySelector(".fb-fab").getAttribute("aria-label"), document.querySelector("#menu .menu-fb").textContent, [...document.querySelectorAll("footer [data-fb]")].map(b => b.textContent).join(" | "), document.querySelector('footer a[href="#quiz"]').textContent]);
    ok(w + ": Ask or report labels on the button, the menu and the footer (with Myth or fact?)", lab.join(" / ") === "Ask a question or report a mistake / Ask a question or report a mistake / Ask a question | Report a mistake / Myth or fact?", lab.join(" / "));
    await s.ctx.close();

    // ---- dark theme
    s = await session({ dark: true });
    await s.go("home"); await s.shot("dark-home");
    const bg = await s.p.evaluate(() => getComputedStyle(document.body).backgroundColor);
    ok(w + ": dark theme applies", /rgb\((\d+), (\d+), (\d+)\)/.test(bg) && bg.match(/\d+/g).slice(0, 3).every(n => +n < 60), bg);
    await s.p.click("#tf .qz2-o >> nth=0"); await s.p.waitForTimeout(T); await s.p.$eval("#mf-h", h => h.scrollIntoView({ block: "start" })); await s.p.waitForTimeout(150); await s.shot("dark-deck-back");
    await s.go("s-cannabis", 1200); await s.shot("dark-drug-first-view");
    await s.p.$eval("#secmenu", e => e.scrollIntoView({ block: "start" })); await s.p.waitForTimeout(200); await s.shot("dark-section-menu");
    await s.go("s-cannabis/q-cl_can_dependence_how_many", 1300); await s.shot("dark-question-after-deep-link");
    await s.go("s-cannabis/part-d-help", 1000); await s.shot("dark-if-it-gets-too-much");
    await s.go("s-mdma/part-d-kits", 1000); await s.shot("dark-test-kits");
    await s.go("quiz"); await s.shot("dark-myth-or-fact-page");
    await s.ctx.close();

    // ---- reduced motion: the card's sides swap at once, with no turning; an answer opens where it is without gliding
    s = await session({ reduce: true });
    await s.go("home"); await s.p.click("#tf .qz2-o >> nth=1"); await s.p.waitForTimeout(60);
    const rm = await s.p.evaluate(() => { const c = document.querySelector("#tf .mf-card"); return { flipped: c.classList.contains("flipped"), turning: c.classList.contains("out"), anim: getComputedStyle(document.querySelector("#tf .mf-in")).animationName }; });
    ok(w + ": reduced motion: the card swaps sides at once, no animation", rm.flipped && !rm.turning && rm.anim === "none", JSON.stringify(rm));
    await s.p.$eval("#mf-h", h => h.scrollIntoView({ block: "start" })); await s.shot("reduced-motion-deck-back");
    await s.go("s-cannabis/part-d-risk", 900); await s.p.click("#d-risk details.ask >> nth=4 >> summary"); await s.p.waitForTimeout(120);
    const rmq = await s.p.evaluate(landedAt, "#d-risk details.ask[open]");
    ok(w + ": reduced motion: a question opened lower on the screen is at its place at once (a jump, no glide)", good(rmq), JSON.stringify(rmq));
    await s.ctx.close();
  }
  await browser.close(); server.close();
  const pageText = fs.readFileSync(path.join(ROOT, "index.html"), "utf8"), old = pageText.match(/test yourself|true or false\?|quick question/gi) || [];
  ok("no \"Test yourself\", \"True or false?\" or \"Quick question\" left in the page", !old.length, old.slice(0, 4).join(", "));
  ok("no horizontal scroll, no console or page errors (all widths, light, dark, reduced motion)", !errors.length, errors.slice(0, 8).join(" | "));
  const failed = results.filter(r => !r.pass).length;
  console.log("\n" + (results.length - failed) + " of " + results.length + " checks passed" + (SHOTS ? "; screenshots in " + SHOTS : ""));
  process.exit(failed ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
