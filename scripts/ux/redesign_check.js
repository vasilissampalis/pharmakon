// Redesign 2 (docs/REDESIGN-2.md) checked in a real browser, at 390 x 844 and 1280 x 800: the Myth or fact? deck turns over and
// counts, Another 10 deals new cards, the quiz does not repeat what the deck asked; At a glance tiles open their answers in
// place, and start with the answers people ask about most (DEMAND: MDMA, psilocybin, heroin), never passing one over for a
// less-asked one, then fill up the old way (alcohol); "Before, during and after" keeps its time order; Read next links work
// on the page and across pages; the 100-dot picture shows for "N in 100" (and not for a range);
// the quiz page loads as "Myth or fact?"; reduced motion swaps the card without turning it; keyboard focus is visible; dark
// theme; main's 1.13.0 carried into the redesign (first paint, Scientific detail, "Ask us" on drug pages and in search); the
// quick-help doors first in the menu; and one quiz format everywhere: the Myth or fact? page is the same deck as the start
// page, endless, and drug pages and the facts page end with a deck of their own statements (none under 3); no "Test
// yourself", "True or false?" or "Quick question" left in the page.
// Every step also checks for horizontal scroll, and every page for console and page errors.
// It serves site/public itself (build first: node site/build.js && python3 -I site/build_public.py).
// Usage: node scripts/ux/redesign_check.js [--shots DIR] [--port N]   (exit code 1 if a check fails; images go to DIR only)
const http = require("http"), fs = require("fs"), path = require("path");
const { chromium } = require("playwright");
const ROOT = path.resolve(__dirname, "..", "..", "site", "public");
const arg = k => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : null; };
const SHOTS = arg("--shots"), PORT = +(arg("--port") || 0);
const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".mjs": "text/javascript", ".wasm": "application/wasm", ".json": "application/json", ".css": "text/css", ".webp": "image/webp", ".png": "image/png", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".txt": "text/plain", ".xml": "application/xml" };
const results = [], errors = [];
const ok = (name, pass, detail) => { results.push({ name, pass: !!pass, detail: detail || "" }); console.log((pass ? "PASS " : "FAIL ") + name + (detail ? "  (" + detail + ")" : "")); };

function serve() {
  if (!fs.existsSync(path.join(ROOT, "index.html"))) { console.error("No site/public/index.html: build first."); process.exit(2); }
  const server = http.createServer((req, res) => {
    let p = decodeURIComponent(req.url.split("?")[0]); if (p.endsWith("/")) p += "index.html";
    const f = path.join(ROOT, path.normalize(p));
    if (!f.startsWith(ROOT)) { res.writeHead(403); res.end(); return; }
    fs.readFile(f, (err, buf) => { if (err) { res.writeHead(404); res.end("not found"); return; } res.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream" }); res.end(buf); });
  });
  return new Promise(r => server.listen(PORT, "127.0.0.1", () => r(server)));
}

(async () => {
  const server = await serve(), BASE = "http://127.0.0.1:" + server.address().port + "/#";
  if (SHOTS) fs.mkdirSync(SHOTS, { recursive: true });
  const browser = await chromium.launch({ args: ["--no-proxy-server"] });
  for (const w of [390, 1280]) {
    const H = w < 700 ? 844 : 800;
    // one browser context: its errors are collected, horizontal scroll is checked before every screenshot and at every step
    async function session(opts = {}) {
      const ctx = await browser.newContext({ viewport: { width: w, height: H }, deviceScaleFactor: 1, colorScheme: opts.dark ? "dark" : "light", reducedMotion: opts.reduce ? "reduce" : "no-preference" });
      const p = await ctx.newPage(), tag = w + (opts.dark ? " dark" : "") + (opts.reduce ? " reduced-motion" : "");
      p.on("pageerror", e => errors.push(tag + " page error: " + String(e).slice(0, 200)));
      p.on("console", m => { if (m.type() === "error") errors.push(tag + " console error: " + m.text().slice(0, 200)); });
      const hscroll = async step => { const [sw, cw] = await p.evaluate(() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]); if (sw > cw) errors.push(tag + " horizontal scroll at " + step + ": " + sw + " > " + cw); };
      const shot = async (name, sel, full) => { await hscroll(name); if (!SHOTS) return; await p.mouse.move(2, 300); const f = path.join(SHOTS, w + "-" + name + ".png");
        if (sel) await (await p.$(sel)).screenshot({ path: f }); else await p.screenshot({ path: f, fullPage: !!full }); };
      const go = async (h, wait) => { await p.goto(BASE + h); await p.waitForTimeout(wait || 1100); };
      const hash = async (h, wait) => { await p.evaluate(x => { location.hash = x; }, "#" + h); await p.waitForTimeout(wait || 500); await hscroll(h); };
      return { ctx, p, shot, go, hash, hscroll };
    }
    const T = 650;   // the card turns in about half a second

    // ---- pages render (a smoke pass over the main views)
    let s = await session();
    await s.go("home");
    const views = [["home", "view-home"], ["quiz", "view-quiz"], ["s-cannabis", "view-drug"], ["s-lsd", "view-drug"], ["s-mdma", "view-drug"], ["s-heroin", "view-drug"], ["facts", "view-facts"],
      ["checking/kits", "view-checking"], ["interactions", "view-interactions"], ["emergency", "view-emergency"], ["s-cannabis/evidence", "view-monograph"], ["a/lsd/cl_lsd_chromosomes", "view-shared"]];
    const wrong = [];
    for (const [h, v] of views) { await s.hash(h, 400); const a = await s.p.evaluate(() => (document.querySelector(".view.active") || {}).id); if (a !== v) wrong.push(h + " -> " + a); }
    ok(w + ": main views render", !wrong.length, wrong.join("; "));
    await s.ctx.close();

    // ---- the deck: turns over, counts, Previous, Another 10; the quiz does not ask again what the deck asked
    s = await session();
    await s.go("home"); await s.shot("home");
    if (w === 390) await s.shot("home-full", null, true);
    await s.p.$eval("#mf-h", h => h.scrollIntoView({ block: "start" })); await s.p.waitForTimeout(200); await s.shot("deck-card1-front");
    const first = await s.p.evaluate(() => { const h = document.getElementById("mf-h"), b = [...document.querySelectorAll("#mf-h ~ *")].map(e => e.className); return { heading: h.textContent, prev: h.previousElementSibling.id, order: b.slice(0, 3).join(" | ") }; });
    const once = await s.p.evaluate(() => ({ home: document.querySelectorAll("#view-home a.do").length, menu: document.querySelectorAll("#menu .menu-do a.do").length,
      each: ["#interactions", "#checking", "#emergency"].map(h => document.querySelectorAll('a.do[href="' + h + '"]').length) }));
    ok(w + ": home shows Myth or fact? first under the search box; the three help doors appear once, in the menu", first.heading === "Myth or fact?" && first.prev === "home-search" && /qz2 mf/.test(first.order)
      && once.home === 0 && once.menu === 3 && once.each.every(n => n === 1), first.prev + " | " + first.order + " | " + JSON.stringify(once));
    const deck = [], verdicts = [], counts = [];
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
    const words = deck.map(t => t.split(/\s+/).length);
    ok(w + ": deck: 10 different statements of 20 words or fewer, 5 myths and 5 facts", new Set(deck).size === 10 && Math.max(...words) <= 20 && verdicts.filter(v => v === "Myth").length === 5, "longest " + Math.max(...words) + " words; " + verdicts.filter(v => v === "Myth").length + " myths");
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

    // ---- the menu: the three quick-help doors first (as on the start page), then All drugs and Myth or fact?, then the quieter links
    s = await session();
    await s.go("interactions"); await s.p.click("#menubtn"); await s.p.waitForTimeout(250);
    const mn = await s.p.evaluate(() => { const top = document.querySelector("#menu .menu-top"), doors = [...top.querySelectorAll(":scope > .menu-do > a.do")];
      const box = d => d.getBoundingClientRect(), next = [...top.querySelectorAll(":scope > a")].map(a => a.textContent.trim());
      return { first: top.firstElementChild.classList.contains("menu-do"), doors: doors.map(d => d.querySelector(".do-t").textContent + " / " + d.querySelector(".do-s").textContent + " / " + d.getAttribute("href") + " / " + d.dataset.view),
        icons: doors.every(d => !!d.querySelector(".do-ic svg")), grid: doors.every(d => getComputedStyle(d).display === "grid" && getComputedStyle(d.querySelector(".do-t")).fontWeight >= 800),
        row: doors.every(d => Math.abs(box(d).top - box(doors[0]).top) < 2), stacked: doors.every((d, i) => !i || (box(d).top > box(doors[i - 1]).bottom - 1 && Math.abs(box(d).left - box(doors[0]).left) < 2)),
        next, more: !!document.querySelector("#menu .menu-top + .menu-more"), cur: (doors.find(d => d.getAttribute("aria-current") === "page") || {}).className || "",
        // the open page's door keeps its dark title (the top bar's rule for its own links would make it white)
        ink: (() => { const c = doors.find(d => d.getAttribute("aria-current") === "page"), o = doors.find(d => d !== c); return !!c && getComputedStyle(c.querySelector(".do-t")).color === getComputedStyle(o.querySelector(".do-t")).color; })() }; });
    await s.shot("menu-open");
    const wantDoors = "Is it safe to mix? / Two drugs together / #interactions / interactions|Test what you have / Drug checking near you / #checking / checking|Someone is unwell / Emergency numbers / #emergency / emergency";
    ok(w + ": menu: the three doors first, as on the start page (" + (w < 700 ? "stacked" : "a row of three") + "), then All drugs and Myth or fact?, then the quieter links; the open page marked",
      mn.first && mn.doors.join("|") === wantDoors && mn.icons && mn.grid && (w < 700 ? mn.stacked : mn.row) && mn.next.join("|") === "All drugs|Myth or fact?" && mn.more && /\bmix\b/.test(mn.cur) && mn.ink, JSON.stringify(Object.assign({}, mn, { doors: mn.doors.length })));
    await s.p.click('#menu a.do.sos'); await s.p.waitForTimeout(500);
    const after = await s.p.evaluate(() => ({ view: (document.querySelector(".view.active") || {}).id, closed: document.getElementById("menu").hidden }));
    ok(w + ": a door in the menu opens its page and closes the menu", after.view === "view-emergency" && after.closed, JSON.stringify(after));
    await s.ctx.close();

    // ---- a drug page and the facts page end with a deck of their own statements; a page with fewer than 3 has none
    s = await session();
    await s.go("s-cannabis", 1300);
    const dk = await s.p.evaluate(() => { const st = MF["qz-drug"], mine = new Set(mfPagePool("cannabis").map(x => x.claim));
      return { box: !!document.querySelector("#d-quiz #qz-drug.mf .mf-card"), chip: !!document.querySelector('#drug2 .chips a[data-go="d-quiz"]'), n: st ? st.cards.length : 0, own: st ? st.cards.every(x => mine.has(x.claim)) : false, pool: mine.size }; });
    await s.p.$eval("#d-quiz", e => e.scrollIntoView({ block: "start" })); await s.p.waitForTimeout(250); await s.p.click("#qz-drug .qz2-o >> nth=1"); await s.p.waitForTimeout(T);
    dk.turned = await s.p.evaluate(() => document.querySelector("#qz-drug .mf-card").classList.contains("flipped"));
    await s.p.$eval("#d-quiz", e => e.scrollIntoView({ block: "start" })); await s.p.waitForTimeout(150); await s.shot("drug-page-myth-or-fact");
    ok(w + ": a drug page ends with its own Myth or fact? deck (its statements only), with a chip to it", dk.box && dk.chip && dk.own && dk.n === Math.min(10, dk.pool) && dk.turned, JSON.stringify(dk));
    const few = await s.p.evaluate(() => SUBSTANCES.map(x => x.slug).filter(x => monographFor(x) && drugQuestions(x).length && mfCount(mfPagePool(x)) < 3)[0] || null);
    if (few) { await s.go("home", 300); await s.go("s-" + few, 1000);
      const none = await s.p.evaluate(() => !document.querySelector("#d-quiz") && !document.querySelector('#drug2 .chips a[data-go="d-quiz"]'));
      ok(w + ": a drug page with fewer than 3 statements has no Myth or fact? section (" + few + ")", none); }
    await s.go("facts", 1000);
    const fk = await s.p.evaluate(() => { const st = MF["qz-facts"], mine = new Set(mfPagePool(GEN).map(x => x.claim)); return { box: !!document.querySelector("#qz-facts.mf .mf-card"), own: st ? st.cards.every(x => mine.has(x.claim)) : false, n: st ? st.cards.length : 0 }; });
    ok(w + ": the facts page ends with its own Myth or fact? deck", fk.box && fk.own && fk.n >= 3, JSON.stringify(fk));
    await s.ctx.close();

    // ---- At a glance on cannabis and LSD: at most 6 groups and 8 tiles (6 on a phone), each tile opens its answer in place
    s = await session();
    for (const slug of ["cannabis", "lsd"]) {
      await s.go("s-" + slug); if (slug === "cannabis") await s.shot("cannabis-top");
      const g = await s.p.evaluate(() => { const box = document.querySelector(".view.active .glance2"); if (!box) return null; const tiles = [...box.querySelectorAll(".gl-a")];
        const help = document.querySelector(".view.active .dh-help"); return { groups: box.querySelectorAll(".gl-g").length, tiles: tiles.length, shown: tiles.filter(a => a.offsetParent).length, dead: tiles.filter(a => !document.getElementById(a.dataset.open)).length,
          afterHelp: !!(help && help.nextElementSibling === box), labels: [...box.querySelectorAll(".gl-t")].map(e => e.textContent).join(", "), long: tiles.map(a => a.querySelector(".gl-s").textContent).filter(t => t.length > 73).length }; });
      ok(w + ": " + slug + " At a glance right under the emergency line: <= 6 groups, <= 8 tiles (" + (w < 700 ? "<= 6 shown" : "all shown") + "), clauses short",
        g && g.afterHelp && g.groups <= 6 && g.tiles <= 8 && (w < 700 ? g.shown <= 6 : g.shown === g.tiles) && !g.dead && !g.long, g ? g.groups + " groups (" + g.labels + "), " + g.tiles + " tiles, " + g.shown + " shown" : "missing");
      await s.p.$eval("#gl-h", h => h.scrollIntoView({ block: "start" })); await s.p.waitForTimeout(250); await s.shot(slug + "-at-a-glance");
      const target = await s.p.$eval(".glance2 .gl-a", a => a.dataset.open);
      await s.p.click(".glance2 .gl-a"); await s.p.waitForTimeout(1300);
      const t = await s.p.evaluate(id => { const d = document.getElementById(id), r = d.getBoundingClientRect(), pad = parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop) || 0;
        return { open: d.open, hash: location.hash, top: Math.round(r.top), pad: Math.round(pad), focus: document.activeElement === d.querySelector("summary") }; }, target);
      ok(w + ": " + slug + " tile opens its answer in place, clear of the sticky bars", t.open && t.hash === "#s-" + slug && t.top >= t.pad - 12 && t.top < H / 2 && t.focus, JSON.stringify(t));
      if (slug === "cannabis") await s.shot("cannabis-tile-tapped-answer-open");
    }
    // ---- At a glance starts with what people ask about most (DEMAND): the first tile is the page's most-asked answer (of
    // equals, the editors' first), the groups follow their best tile, each group runs from most to least asked, no answer is
    // left out while a less-asked one is shown, a page with 8 such answers in reach shows 8 (in up to 6 groups), and a
    // phone keeps the most-asked six. Alcohol runs out of asked-about answers: all of them, then the rest filled up the old way.
    const glanceAt = slug => s.p.evaluate(slug => {
      const box = document.querySelector(".view.active .glance2"); if (!box) return null;
      const sc = id => DEMAND[id] && typeof DEMAND[id].score === "number" ? DEMAND[id].score : -1;
      const own = drugQuestions(slug).map(x => x[0]).filter(id => SIMPLE.claims[id] && claimById[id].verification.status !== "draft");
      const top = Math.max(...own.map(sc)), groups = [...box.querySelectorAll(".gl-g")].map(g => [...g.querySelectorAll(".gl-a")].map(a => ({ id: a.dataset.open.slice(4), shown: !!a.offsetParent })).map(t => ({ ...t, s: sc(t.id) })));
      const tiles = groups.flat(), ids = tiles.map(t => t.id), best = groups.map(g => g[0].s), shown = tiles.filter(t => t.shown), hidden = tiles.filter(t => !t.shown), low = Math.min(...tiles.filter(t => t.s >= 0).map(t => t.s));
      return { first: tiles[0].id === own.find(id => sc(id) === top), groups: best.every((v, i) => !i || best[i - 1] >= v), within: groups.every(g => g.every((t, i) => !i || g[i - 1].s >= t.s)),
        scored: tiles.every(t => t.s >= 0), none: own.filter(id => sc(id) > low && !ids.includes(id)).length, asked: own.filter(id => sc(id) >= 0).length, nGroups: groups.length,
        phone: hidden.every(h => shown.every(t => t.s >= h.s)), shown: shown.length, all: tiles.length, list: groups.map(g => g.map(t => (t.s >= 0 ? t.s : "-") + (t.shown ? "" : "*")).join(" ")).join(" | ") };
    }, slug);
    const dem = [];
    for (const slug of ["mdma", "psilocybin", "heroin"]) {
      await s.go("s-" + slug); dem.push([slug, await glanceAt(slug)]);
      await s.p.$eval("#gl-h", h => h.scrollIntoView({ block: "start" })); await s.p.waitForTimeout(250); await s.shot(slug + "-at-a-glance");
    }
    ok(w + ": MDMA, psilocybin and heroin At a glance start with their most-asked answers and leave none out for a less-asked one (DEMAND" + (w < 700 ? "; the phone keeps the top 6)" : ")"),
      dem.every(([, d]) => d && d.first && d.groups && d.within && d.scored && !d.none && d.nGroups <= 6 && d.all === Math.min(8, d.asked) && d.phone && (w < 700 ? d.shown === Math.min(6, d.all) : d.shown === d.all)), dem.map(([k, d]) => k + ": " + (d ? d.list : "missing")).join("; ") + (w < 700 ? " (* not on a phone)" : ""));
    await s.go("s-alcohol"); const alc = await glanceAt("alcohol");
    await s.p.$eval("#gl-h", h => h.scrollIntoView({ block: "start" })); await s.p.waitForTimeout(250); await s.shot("alcohol-at-a-glance");
    // with the combined demand ranking (14 November) alcohol has more asked-about answers than tiles: then the check is the one
    // above (none left out for a less-asked one); with fewer, the asked-about ones come first and the rest fill up the old way
    ok(w + ": alcohol At a glance: its most-asked answers first (filled up the old way to 8 tiles, 6 on a phone, when fewer are asked about)",
      alc && alc.first && alc.groups && alc.within && alc.all === 8 && alc.shown === (w < 700 ? 6 : 8) && alc.nGroups <= 6
        && (alc.asked >= 8 ? alc.scored && !alc.none : alc.list.split(" ").filter(x => /^\d/.test(x)).length === alc.asked), alc ? alc.list + " (" + alc.asked + " asked about; left out for a less-asked one: " + alc.none + ")" : "missing");
    // ---- "Before, during and after" keeps its time order: before and during, the day after, after stopping, each in the editors' order
    const seq = [];
    for (const slug of ["psilocybin", "methamphetamine", "alcohol"]) {
      await s.go("s-" + slug, 700);
      seq.push([slug, await s.p.evaluate(slug => { const want = [/^before/i, /day after/i, /after stopping/i].flatMap(re => drugQuestions(slug).filter(([, , t]) => topicZone(t) === "after" && re.test(t))).map(x => "ask-" + x[0]);
        const got = [...document.querySelectorAll("#d-after details.ask")].map(d => d.id); return want.length > 1 && got.join() === want.join() ? got.length : -1; }, slug)]);
    }
    ok(w + ": Before, during and after keeps its time order (psilocybin, methamphetamine, alcohol)", seq.every(([, n]) => n > 1), seq.map(([k, n]) => k + " " + n + " questions").join(", "));
    // ---- an open answer: the closed card's parts, the dots for "N in 100", Read next on the page and to another page
    await s.go("s-cannabis/q-cl_can_dependence_how_many", 1300);
    const card = await s.p.evaluate(() => { const d = document.getElementById("ask-cl_can_dependence_how_many"); if (!d) return null; const sm = d.querySelector("summary"), a = d.querySelector(".ask-a"), dots = a.querySelector(".freq .dots100");
      return { open: d.open, q: !!sm.querySelector(".ask-q"), short: !!sm.querySelector(".ask-s"), label: (sm.querySelector(".meter .mw") || {}).textContent, butFirst: a.firstElementChild.classList.contains("ask-but"), howFlat: !!a.querySelector("div.ask-how .ask-howl") && !a.querySelector("details"),
        dots: dots ? dots.querySelectorAll("i").length + "/" + dots.querySelectorAll("i.on").length + "/" + dots.getAttribute("aria-hidden") : "", words: (a.querySelector(".freq-row b") || {}).textContent, rn: a.querySelectorAll(".rn-l a").length }; });
    ok(w + ": closed card shows question, short answer, bars and label; open card starts with But, no third fold", card && card.q && card.short && /evidence/.test(card.label || "") && card.butFirst && card.howFlat, card ? "label " + card.label : "missing");
    ok(w + ": 100 dots for About 9 in 100 (9 filled, hidden from screen readers, words read out)", card && card.dots === "100/9/true" && card.words === "9 in 100", card ? card.dots + ' "' + card.words + '"' : "missing");
    await s.shot("cannabis-answer-9-in-100-open"); await s.shot("cannabis-answer-9-in-100-whole-card", "#ask-cl_can_dependence_how_many");
    await s.p.waitForTimeout(1000);   // the page keeps a just-opened answer in place for a moment while photos load
    await s.p.$eval("#ask-cl_can_dependence_how_many .rn", e => e.scrollIntoView({ block: "center" })); await s.p.waitForTimeout(200); await s.shot("cannabis-read-next");
    const links = await s.p.$$eval("#ask-cl_can_dependence_how_many .rn-l a", as => as.map(a => [a.getAttribute("href"), a.dataset.open, a.textContent]));
    ok(w + ": Read next has up to 3 titles: the topic's next answers, then a Myths and facts answer", links.length >= 1 && links.length <= 3, links.map(l => l[2]).join(" | "));
    await s.p.click("#ask-cl_can_dependence_how_many .rn-l a >> nth=0"); await s.p.waitForTimeout(1300);
    const r1 = await s.p.evaluate(id => ({ open: document.getElementById(id).open, prev: document.getElementById("ask-cl_can_dependence_how_many").open, hash: location.hash }), links[0][1]);
    ok(w + ": Read next opens an answer on the same page (this one closes, the address stays)", r1.open && !r1.prev && r1.hash === "#s-cannabis/q-cl_can_dependence_how_many", JSON.stringify(r1));
    await s.shot("cannabis-read-next-followed");
    const other = links.find(l => !l[0].startsWith("#s-cannabis/"));
    // (the same address again would not reopen the card the step before closed, so go by another address first)
    if (other) { await s.go("home", 400); await s.go("s-cannabis/q-cl_can_dependence_how_many", 1300); await s.p.click('#ask-cl_can_dependence_how_many .rn-l a[href="' + other[0] + '"]'); await s.p.waitForTimeout(1500);
      const r2 = await s.p.evaluate(dom => { const d = document.getElementById(dom); return { hash: location.hash, open: !!(d && d.open && d.closest(".view.active")) }; }, other[1]);
      ok(w + ": Read next opens an answer on another page", r2.hash === other[0] && r2.open, other[2] + " -> " + r2.hash); }
    // the dots made from a short answer's own words, and none for a range
    await s.go("s-heroin/q-cl_opi_naloxone_programs", 1300);
    const nal = await s.p.evaluate(() => { const a = document.querySelector("#ask-cl_opi_naloxone_programs .ask-a"); const d = a && a.querySelector(".dotpic .dots100"); return d ? d.querySelectorAll("i.on").length + ' "' + a.querySelector(".dotpic b").textContent + '"' : "none"; });
    ok(w + ': 100 dots from the words "At least 96 in 100"', nal === '96 "At least 96 in 100"', nal);
    await s.shot("heroin-answer-dots-from-words", "#ask-cl_opi_naloxone_programs");
    await s.go("s-cannabis/q-cl_can_cbd_epilepsy", 1300);
    const range = await s.p.evaluate(() => { const d = document.getElementById("ask-cl_can_cbd_epilepsy"); return d ? (/\d+ to \d+ in 100/.test(d.querySelector(".ask-s").textContent) ? (d.querySelector(".dotpic") ? "dots shown" : "no dots") : "no range in this answer") : "missing"; });
    ok(w + ': no dots for a range ("43 to 49 in 100")', range === "no dots", range);
    await s.ctx.close();

    // ---- keyboard: the deck and a tile, with visible focus
    s = await session();
    await s.go("home");
    for (let i = 0; i < 14; i++) { await s.p.keyboard.press("Tab"); if (await s.p.evaluate(() => document.activeElement.classList.contains("qz2-o"))) break; }
    const f1 = await s.p.evaluate(() => [document.activeElement.textContent, getComputedStyle(document.activeElement).outlineStyle]);
    await s.shot("focus-deck-myth-button");
    await s.p.keyboard.press("Enter"); await s.p.waitForTimeout(T);
    const f2 = await s.p.evaluate(() => document.activeElement.className);
    await s.p.keyboard.press("Tab"); const f3 = await s.p.evaluate(() => document.activeElement.className);
    await s.p.keyboard.press("Tab"); await s.p.waitForTimeout(150);
    const f4 = await s.p.evaluate(() => [document.activeElement.className, document.activeElement.textContent, getComputedStyle(document.activeElement).outlineStyle]);
    await s.shot("focus-deck-next-button");
    ok(w + ": keyboard: Tab to Myth, Enter turns the card, Tab reaches Read the answer and Next, focus visible", f1[0] === "Myth" && f1[1] === "solid" && f2 === "mf-v" && /qz2-ev/.test(f3) && /qz2-nb/.test(f4[0]) && f4[2] === "solid", [f1.join(" "), f2, f3, f4.join(" ")].join(" > "));
    await s.go("s-cannabis"); await s.p.$eval("#gl-h", h => { h.scrollIntoView({ block: "start" }); h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); });
    await s.p.keyboard.press("Tab"); await s.p.waitForTimeout(150);
    const f5 = await s.p.evaluate(() => [document.activeElement.className, getComputedStyle(document.activeElement).outlineStyle]);
    await s.shot("focus-at-a-glance-tile");
    await s.p.keyboard.press("Enter"); await s.p.waitForTimeout(1300);
    const f6 = await s.p.evaluate(() => [document.activeElement.tagName, document.activeElement.parentElement.open]);
    await s.shot("focus-answer-opened-from-tile");
    ok(w + ": keyboard: a tile takes focus visibly and Enter opens its answer", f5[0] === "gl-a" && f5[1] === "solid" && f6[0] === "SUMMARY" && f6[1], f5.join(" ") + " > " + f6.join(" "));
    await s.go("s-cannabis/q-cl_can_dependence_how_many", 1300);
    await s.p.$eval("#ask-cl_can_dependence_how_many .ask-ev", a => a.focus()); await s.p.keyboard.press("Tab"); await s.p.waitForTimeout(150);
    await s.p.evaluate(() => document.activeElement.scrollIntoView({ block: "center" })); await s.p.waitForTimeout(150);
    const f7 = await s.p.evaluate(() => !!document.activeElement.closest(".rn") && getComputedStyle(document.activeElement).outlineStyle === "solid");
    await s.shot("focus-read-next-link");
    ok(w + ": keyboard: Read next links follow The evidence, focus visible", f7);
    await s.ctx.close();

    // ---- main's 1.13.0 in the redesign: the start page at first paint (before any script runs, with the deck's place held),
    // the answer sheet's quiet "Scientific detail" under the sources, "Ask us" at the end of a drug page and of a search
    // (the words typed come along into the message), and the "Ask or report" labels
    { const ctx = await browser.newContext({ viewport: { width: w, height: H }, deviceScaleFactor: 1, javaScriptEnabled: false }), p0 = await ctx.newPage();
      await p0.goto(BASE.replace(/#$/, "")); await p0.waitForTimeout(300);
      const fp = await p0.evaluate(() => { const v = document.getElementById("view-home"), vis = el => !!(el && el.getBoundingClientRect().height > 0);
        return { active: v.classList.contains("active"), h1: vis(v.querySelector("h1")), mf: vis(document.getElementById("mf-h")), wait: vis(v.querySelector(".mf-wait")), doors: v.querySelectorAll("a.do").length, emergency: !!document.querySelector('footer.site a[href="#emergency"]') }; });
      ok(w + ": first paint, before the script: the start page with Myth or fact? (its place held); no help doors repeated there; Emergency numbers in the footer", fp.active && fp.h1 && fp.mf && fp.wait && fp.doors === 0 && fp.emergency, JSON.stringify(fp));
      if (SHOTS) await p0.screenshot({ path: path.join(SHOTS, w + "-first-paint-home.png") }); await ctx.close(); }
    s = await session();
    await s.go("cl_can_dependence_how_many", 1300);
    const sh = await s.p.evaluate(() => { const d = document.querySelector("#evsheet.open details.sf-sci"), refs = document.querySelector("#evsheet.open .ev-refs");
      return d ? { sci: d.querySelector("summary").textContent, under: !!(refs && refs.compareDocumentPosition(d) & Node.DOCUMENT_POSITION_FOLLOWING), pieces: d.querySelectorAll(".ev-precise .pc-group, .ev-precise > p").length, report: (document.querySelector("#evsheet.open .ev-foot [data-fb]") || {}).textContent } : null; });
    ok(w + ": answer sheet: a quiet Scientific detail fold under the sources, in short pieces; Report a mistake", sh && sh.sci === "Scientific detail" && sh.under && sh.pieces > 0 && sh.report === "Report a mistake in this answer", JSON.stringify(sh));
    await s.p.evaluate(() => { const d = document.querySelector("#evsheet.open details.sf-sci"); d.open = true; d.scrollIntoView({ block: "start" }); }); await s.p.waitForTimeout(250); await s.shot("sheet-scientific-detail-open");
    await s.go("home", 400); await s.go("s-cannabis");
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
    await s.go("s-cannabis"); await s.p.$eval("#gl-h", h => h.scrollIntoView({ block: "start" })); await s.p.waitForTimeout(250); await s.shot("dark-cannabis-at-a-glance");
    await s.go("s-cannabis/q-cl_can_dependence_how_many", 1300); await s.shot("dark-cannabis-answer-open");
    await s.go("s-lsd"); await s.p.$eval("#gl-h", h => h.scrollIntoView({ block: "start" })); await s.p.waitForTimeout(250); await s.shot("dark-lsd-at-a-glance");
    await s.go("quiz"); await s.shot("dark-myth-or-fact-page");
    await s.ctx.close();

    // ---- reduced motion: the sides swap at once, with no turning
    s = await session({ reduce: true });
    await s.go("home"); await s.p.click("#tf .qz2-o >> nth=1"); await s.p.waitForTimeout(60);
    const rm = await s.p.evaluate(() => { const c = document.querySelector("#tf .mf-card"); return { flipped: c.classList.contains("flipped"), turning: c.classList.contains("out"), anim: getComputedStyle(document.querySelector("#tf .mf-in")).animationName }; });
    ok(w + ": reduced motion: the card swaps sides at once, no animation", rm.flipped && !rm.turning && rm.anim === "none", JSON.stringify(rm));
    await s.p.$eval("#mf-h", h => h.scrollIntoView({ block: "start" })); await s.shot("reduced-motion-deck-back");
    await s.ctx.close();
  }
  await browser.close(); server.close();
  const pageText = fs.readFileSync(path.join(ROOT, "index.html"), "utf8"), old = pageText.match(/test yourself|true or false\?|quick question/gi) || [];
  ok("no \"Test yourself\", \"True or false?\" or \"Quick question\" left in the page", !old.length, old.slice(0, 4).join(", "));
  ok("no horizontal scroll, no console or page errors (both widths, light, dark, reduced motion)", !errors.length, errors.slice(0, 8).join(" | "));
  const failed = results.filter(r => !r.pass).length;
  console.log("\n" + (results.length - failed) + " of " + results.length + " checks passed" + (SHOTS ? "; screenshots in " + SHOTS : ""));
  process.exit(failed ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
