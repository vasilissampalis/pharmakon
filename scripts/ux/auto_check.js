// Site 2.6: answers written by our system (the machine lane), as a visitor meets them. The site is built here with two
// PRETEND answers (scripts/ux/fixtures/auto: one about ketamine that is "not complete", one about no drug), served from
// site/dist, looked at on a phone and on a desktop, and then built again without them. site/build_public.py refuses to
// publish a build that holds the pretend answers, so they can never reach the site.
// What must hold: the quiet line is on every such answer, everywhere it is shown ("Written by our system from N papers. Not
// yet checked by a person.", and "Not complete yet." where papers could not be read); no evidence bars (nobody has rated it);
// its sources as APA 7 references with their DOI links; a way to report a mistake; the search box finds it by a question in
// other words and says what it is before it is opened; its drug's page lists it in a section of its own, never among the
// checked answers; one page lists every one; a question it answers leaves the list of questions not answered yet; a kept
// question turns "Answered"; nothing is wider than the phone; no console errors.
// Usage: node scripts/ux/auto_check.js [--shots DIR] [--keep]   (--keep: leave site/dist built with the pretend answers)
const http = require("http"), fs = require("fs"), path = require("path"), { spawnSync } = require("child_process");
const { chromium } = require("playwright");
const REPO = path.resolve(__dirname, "..", ".."), ROOT = path.join(REPO, "site", "dist");
const arg = k => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : null; }, SHOTS = arg("--shots");
const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".mjs": "text/javascript", ".wasm": "application/wasm", ".json": "application/json", ".css": "text/css", ".txt": "text/plain; charset=utf-8", ".webp": "image/webp", ".svg": "image/svg+xml", ".png": "image/png" };
let pass = 0, fail = 0;
const ok = (name, cond, extra) => { if (cond) { pass++; console.log("PASS " + name); } else { fail++; console.log("FAIL " + name + (extra ? " | " + String(extra).slice(0, 500) : "")); } };
const build = env => spawnSync("node", [path.join(REPO, "site", "build.js")], { env: Object.assign({}, process.env, env), encoding: "utf8", maxBuffer: 1 << 26 });

(async () => {
  // the pretend answers, in a folder of their own for this run: the three written out, and two about amounts made from their
  // templates with the lines the code writes itself (data/auto/lane/lines.json), so that the check always holds today's lines
  const LINES = JSON.parse(fs.readFileSync(path.join(REPO, "data", "auto", "lane", "lines.json"), "utf8")), FIX = fs.mkdtempSync(path.join(require("os").tmpdir(), "pk-auto-"));
  for (const f of fs.readdirSync(path.join(REPO, "scripts", "ux", "fixtures", "auto"))) fs.copyFileSync(path.join(REPO, "scripts", "ux", "fixtures", "auto", f), path.join(FIX, f));
  for (const f of fs.readdirSync(path.join(REPO, "scripts", "ux", "fixtures", "auto-amounts"))) fs.writeFileSync(path.join(FIX, f),
    fs.readFileSync(path.join(REPO, "scripts", "ux", "fixtures", "auto-amounts", f), "utf8").replace('"LINE_FIRST"', JSON.stringify(LINES.first.opioids.text)).replace('"LINE_SHORT"', JSON.stringify(LINES.amounts)).replace('"LINE_BUT_GUIDANCE"', JSON.stringify(LINES.amounts_but_guidance)).replace('"LINE_BUT"', JSON.stringify(LINES.amounts_but)));
  const b = build({ PK_AUTO_FIXTURE: FIX, PK_AUTO_LOOP: "1" });
  if (b.status !== 0) { console.error(b.stderr.slice(-2000)); process.exit(2); }
  ok("the build shows the two pretend answers and takes the questions they answer off the list of questions not answered yet", /machine lane: 6 answers written by the system are shown/.test(b.stdout) && /w_0024 by au_fixture_ketamine/.test(b.stderr) && /w_0007 by au_fixture_police/.test(b.stderr), (b.stdout + b.stderr).split("\n").filter(l => /machine lane|listed questions/.test(l)).join(" | "));
  // (2.8) an answer for a drug that has no page stands on a page the system starts, by a name the filing knows; another name never reaches the site
  ok("the build starts a page for a drug that has none (by a name the filing knows) and leaves out an answer whose page the filing does not know", /machine lane: 1 pages started by the system are shown: Kava/.test(b.stdout) && /au_fixture_nopage \(a page to start that the filing does not know\)/.test(b.stderr),
    (b.stdout + b.stderr).split("\n").filter(l => /pages started|left out/.test(l)).join(" | ").slice(0, 400));
  const pub = spawnSync("python3", ["-I", path.join(REPO, "site", "build_public.py")], { encoding: "utf8" });
  ok("the publishing step refuses a build that holds the pretend answers", pub.status !== 0 && /pretend answers/.test(pub.stderr + pub.stdout), (pub.stderr + pub.stdout).slice(-200));
  const server = http.createServer((req, res) => {
    let p = decodeURIComponent(req.url.split("?")[0]); if (p.endsWith("/")) p += "index.html";
    if (p.startsWith("/api/")) { res.writeHead(200, { "Content-Type": "application/json" }); res.end('{"ok":false}'); return; }
    const f = path.join(ROOT, path.normalize(p)); if (!f.startsWith(ROOT)) { res.writeHead(403); res.end(); return; }
    fs.readFile(f, (err, buf) => { if (err) { res.writeHead(404); res.end(); return; } res.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream" }); res.end(buf); });
  });
  await new Promise(r => server.listen(0, "127.0.0.1", r));
  const base = "http://127.0.0.1:" + server.address().port + "/", browser = await chromium.launch({ args: ["--no-proxy-server"] }), errors = [];
  const open = async width => { const ctx = await browser.newContext({ viewport: { width, height: width < 600 ? 844 : 800 } }), p = await ctx.newPage();
    p.on("pageerror", e => errors.push("page error: " + String(e).slice(0, 300))); p.on("console", m => { if (m.type() === "error" && !/favicon|Failed to load resource/.test(m.text())) errors.push("console: " + m.text().slice(0, 300)); });
    await p.goto(base + "#home"); await p.waitForTimeout(700); return p; };
  const go = async (p, hash, ms) => { await p.evaluate(h => { location.hash = h; }, hash); await p.waitForTimeout(ms || 500); };
  const shot = async (p, name) => { if (SHOTS) { fs.mkdirSync(SHOTS, { recursive: true }); await p.screenshot({ path: path.join(SHOTS, name + ".png") }); } };
  const LINE2 = "Written by our system from 2 papers. Not yet checked by a person. Not complete yet.", LINE1 = "Written by our system from 1 paper. Not yet checked by a person.";
  // what the open sheet shows of an answer
  const sheet = p => p.evaluate(() => { const s = document.querySelector("#evsheet.open .panel .ins"); if (!s) return null; const a = s.querySelector(".ins-ans") || s;
    return { title: document.getElementById("ev-title").textContent, eye: (document.querySelector("#evsheet .ins-eye") || {}).textContent || "", short: (a.querySelector(".ask-short") || {}).textContent || "", but: (a.querySelector(".ask-but") || {}).textContent || "",
      how: [...a.querySelectorAll(".ask-howl li")].map(e => e.textContent), line: (a.querySelector(".auto-l") || {}).textContent || "", bars: a.querySelectorAll(".meter").length, evLink: a.querySelectorAll('a.ask-ev, a[href^="#cl_"]').length,
      refs: [...a.querySelectorAll(".auto-refs li")].map(li => ({ text: li.textContent, italic: (li.querySelector("i") || {}).textContent || "", link: (li.querySelector("a") || {}).href || "" })), srcSummary: (a.querySelector(".auto-src summary") || {}).textContent || "",
      report: (a.querySelector("button[data-auto-report]") || {}).textContent || "", all: (s.querySelector('.ins-page a[href="#auto"]') || {}).textContent || "", label: (s.querySelector(".ins-l-k") || {}).textContent || "", next: s.querySelectorAll(".ins-next a").length, wide: document.documentElement.scrollWidth > innerWidth + 1 }; });

  for (const width of [390, 1280]) {
    const w = width + ": ", p = await open(width);
    // ---- the page that lists them all
    await go(p, "#auto", 600);
    const pg = await p.evaluate(() => ({ title: document.title, h1: document.querySelector("#view-auto h1").textContent, n: (document.querySelector("#auto-list .auto-n") || {}).textContent || "", rows: [...document.querySelectorAll("#auto-list .auto-i")].map(r => r.querySelector(".wl-q").textContent + " | " + r.querySelector(".auto-meta").textContent),
      how: !!document.querySelector("#view-auto details.auto-how"), foot: [...document.querySelectorAll('footer.site a[href="#auto"]')].map(a => a.textContent).join(), wide: document.documentElement.scrollWidth > innerWidth + 1 }));
    ok(w + "the page “Written by our system” lists every such answer with its page, its number of papers, its day and “not complete yet” where that is so; one name in the tab, on the page and in the footer",
      pg.title === "Written by our system · Pharmakon" && pg.h1 === "Written by our system" && pg.foot === "Written by our system" && pg.n === "6 answers, the newest first." && pg.rows.length === 6 && pg.how && !pg.wide && pg.rows[0] === "How much pretend drinking do pretend bodies call low-risk in the checks? | Alcohol · 1 official page · 16 November 2026 · not complete yet" &&
        pg.rows.includes("Can you get addicted to ketamine? | Ketamine · 2 papers · 15 November 2026 · not complete yet") && pg.rows.some(r => /^Do police crackdowns cut drug use, or just move it somewhere else\? \| .+ · 1 paper · 15 November 2026$/.test(r)), JSON.stringify(pg));
    await shot(p, width + "-auto-page");
    // ---- (2.8) a page the system started: listed on this page and under the drugs, with an address of its own and its label
    const st = await p.evaluate(() => ({ h: [...document.querySelectorAll("#auto-list .auto-h")].map(e => e.textContent), pages: [...document.querySelectorAll("#auto-list .auto-pages a")].map(a => a.getAttribute("href") + " | " + a.textContent),
      row: [...document.querySelectorAll("#auto-list .auto-i")].map(r => r.textContent).find(t => /^Is kava addictive\?/.test(t)) || "" }));
    ok(w + "the list page names the pages our system started, each with its number of answers and its label, before every answer; an answer on such a page names the page",
      st.h.join("|") === "Pages our system started|Every answer" && st.pages.includes("#auto/p-kava | Kava1 answer") && /^Is kava addictive\?Kava · 1 paper/.test(st.row), JSON.stringify(st));
    await go(p, "#auto/p-kava", 600);
    // (2.12) in the form of a drug's page: a drug page's header with the name, the line that says who made it, and its parts
    const kp = await p.evaluate(() => { const pg = document.getElementById("auto-page"); return { title: document.title, h1: document.querySelector("#view-auto h1").textContent, head: !!pg.querySelector("header.dh h1"), top: (pg.querySelector(".auto-top") || {}).textContent || "",
      main: document.getElementById("auto-main").hidden, shown: !pg.hidden, secs: [...pg.querySelectorAll("section.sec > h2")].map(e => e.textContent), cls: pg.querySelectorAll(".dh-fam").length,
      rows: [...pg.querySelectorAll(".auto-i .wl-q")].map(e => e.textContent), back: (pg.querySelector('.auto-back a[href="#auto"]') || {}).textContent || "", ask: (pg.querySelector("button[data-ask-fill]") || {}).textContent || "",
      active: document.getElementById("view-auto").classList.contains("active"), wide: document.documentElement.scrollWidth > innerWidth + 1 }; });
    ok(w + "a started page has an address of its own and the form of a drug's page: its name as the heading and in the tab, a first line that says our system started it and that nobody has checked it, its answers, a way to ask, and the way back; it shows no class nobody checked",
      kp.active && kp.title === "Kava · Pharmakon" && kp.h1 === "Kava" && kp.head && kp.shown && kp.main && kp.top === "People asked about kava, and the site had no page. Our system started this one by itself and wrote what is on it. A person has not checked it yet." &&
        kp.secs.join("|") === "Written by our system" && kp.rows.join() === "Is kava addictive?" && kp.back === "Everything written by our system" && kp.ask === "Ask a question" && kp.cls === 0 && !kp.wide, JSON.stringify(kp));
    await shot(p, width + "-started-page");
    await p.click('#auto-page button[data-ask-fill]'); await p.waitForTimeout(300);
    ok(w + "“Ask a question” there puts the page's name in the box and the cursor after it", await p.evaluate(() => { const s = document.getElementById("search"); return s.value === "kava " && document.activeElement === s; }));
    await p.fill("#search", ""); await p.keyboard.press("Escape");
    await p.click('#auto-page a[data-sheet="au_fixture_kava"]'); await p.waitForTimeout(600);
    const sk = await p.evaluate(() => { const s = document.querySelector("#evsheet.open .panel .ins"); return s ? { title: document.getElementById("ev-title").textContent, line: (s.querySelector(".auto-l") || {}).textContent || "", link: (s.querySelector(".ins-page a") || {}).getAttribute("href") || "", linkText: (s.querySelector(".ins-page a") || {}).textContent || "" } : null; });
    ok(w + "its answer opens over the page with its line, and leads back to the page our system started", sk && sk.title === "Is kava addictive?" && sk.line === LINE1 && sk.link === "#auto/p-kava" && /^Kava: the page our system started/.test(sk.linkText), JSON.stringify(sk));
    await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    await go(p, "#auto", 400);
    const back = await p.evaluate(() => ({ h1: document.querySelector("#view-auto h1").textContent, how: document.querySelector("#view-auto .auto-how").hidden, n: (document.querySelector("#auto-list .auto-n") || {}).textContent || "", pg: document.getElementById("auto-page").hidden, main: document.getElementById("auto-main").hidden }));
    ok(w + "back on the list page, its own heading and lines are there again", back.h1 === "Written by our system" && back.how === false && back.n === "6 answers, the newest first." && back.pg && !back.main, JSON.stringify(back));
    // ---- (2.12) the pages people asked about, shown before there is an answer: whatever pages the build shows today
    const shells = await p.evaluate(() => Object.keys(AUTO_SHELL).map(k => ({ k, name: AUTO_PAGES[k], asked: AUTO_SHELL[k].asked.map(a => a.id), pics: (AUTO_PICS[k] || []).length, ans: Object.keys(AUTO).filter(id => AUTO[id].page === "new:" + k).length, kind: (AUTO_SHELL[k].science[0] || {}).kind || "" })));
    const look = shells.filter(s => s.pics).slice(0, 2).concat(shells.filter(s => !s.pics && !s.ans).slice(0, 2));
    if (!look.length) ok(w + "(no page people asked about is shown without an answer today)", true);
    for (const s of look) {
      await go(p, "#auto/p-" + s.k, 600);
      const parts = (s.pics ? 1 : 0) + (s.asked.length ? 1 : 0) + (s.ans ? 1 : 0);
      const sp = await p.evaluate(() => { const pg = document.getElementById("auto-page"), img = pg.querySelector("header.dh .dh-ph img"); return { h1: (pg.querySelector("header.dh h1") || {}).textContent || "", top: (pg.querySelector(".auto-top") || {}).textContent || "", fam: (pg.querySelector(".dh-fam") || {}).textContent || "",
        menu: [...pg.querySelectorAll(".secmenu .sm-b .sm-n")].map(e => e.textContent), one: [...pg.querySelectorAll("section.auto-one > h2")].map(e => e.textContent), head: img ? img.complete && img.naturalWidth > 0 && !!img.alt : null, title: document.title, wide: document.documentElement.scrollWidth > innerWidth + 1 }; });
      ok(w + "“" + s.name + "”, a page people asked about: a drug page's header with its name, a line that says our system started it and that nobody has checked it, " + (parts > 1 ? "a menu of its " + parts + " parts" : "its one part shown at once") + (s.pics ? ", its picture at the top" : "") + "; the only word above the name is what the open list of species says it is",
        sp.h1 === s.name && sp.title === s.name + " · Pharmakon" && /Our system started this one by itself/.test(sp.top) && /A person has not checked/.test(sp.top) && (parts > 1 ? sp.menu.length === parts && !sp.one.length : sp.one.length === parts && !sp.menu.length) &&
          (s.pics ? sp.head === true : sp.head === null) && sp.fam === (s.kind === "plant" ? "Plant" : s.kind === "fungus" ? "Fungus" : "") && !sp.wide, JSON.stringify(sp));
      if (s.pics) {
        await go(p, "#auto/p-" + s.k + (parts > 1 ? "/part-p-looks" : ""), 700);
        await p.evaluate(() => document.querySelectorAll("#p-looks img").forEach(i => i.scrollIntoView())); await p.waitForTimeout(500);
        const lk = await p.evaluate(() => { const sec = document.getElementById("p-looks"); const cr = sec.querySelector("details.look-credits"); return { shown: !sec.hidden, imgs: [...sec.querySelectorAll(".look img")].map(i => i.complete && i.naturalWidth > 0 && !!i.alt && /^img\/auto\/[a-z0-9-]+-t\.webp$/.test(i.getAttribute("src"))),
          credits: cr ? [...cr.querySelectorAll("a")].map(a => a.href) : [], creditText: cr ? cr.textContent : "", note: (sec.querySelector(".auto-picnote") || {}).textContent || "", wide: document.documentElement.scrollWidth > innerWidth + 1 }; });
        ok(w + "its pictures: each one loads and says what it shows, each has its maker and its licence (CC0 or CC BY, nothing else) one tap away, and a small line says that our system found them and that no person has checked them",
          lk.shown && lk.imgs.length === s.pics && lk.imgs.every(Boolean) && lk.credits.filter(h => /^https:\/\/creativecommons\.org\/(?:publicdomain\/zero\/1\.0|licenses\/by\/[1-4]\.0)\/$/.test(h)).length === s.pics && lk.credits.length >= 2 * s.pics - 1 && !/\b(?:NC|ND|SA)\b/.test(lk.creditText) &&
            /^Our system found these pictures by itself\..+A person here has not checked them yet\./.test(lk.note) && !lk.wide, JSON.stringify(lk));
        await shot(p, width + "-started-looks");
      }
      if (s.asked.length) {
        await go(p, "#auto/p-" + s.k + (parts > 1 ? "/part-p-asked" : ""), 600);
        const before = await p.evaluate(() => localStorage.getItem("pk-asked"));
        const aq = await p.evaluate(() => { const sec = document.getElementById("p-asked"); return { shown: !sec.hidden, rows: [...sec.querySelectorAll(".wl-i")].map(li => ({ q: li.querySelector(".wl-q").textContent, open: !!li.querySelector(".wl-n"), keep: (li.querySelector("button[data-want-keep]") || {}).dataset ? li.querySelector("button[data-want-keep]").dataset.wantKeep : "", link: (li.querySelector("a.wl-b") || {}).href || "" })) }; });
        ok(w + "what people asked about it: every listed question in our words, each “Not answered yet” with the way to be told, or with the way to what our system wrote",
          aq.shown && aq.rows.length === s.asked.length && aq.rows.every(r => r.q.length > 8 && (r.open ? s.asked.includes(r.keep) : /#auto\/q-au_/.test(r.link))), JSON.stringify(aq));
        const first = aq.rows.find(r => r.keep);
        if (first) { await p.click('#p-asked button[data-want-keep="' + first.keep + '"]'); await p.waitForTimeout(300);
          const kept = await p.evaluate(id => { const l = JSON.parse(localStorage.getItem("pk-asked") || "[]"), it = l.find(x => x.w === id); return { it: it ? { q: it.q, sent: it.sent, st: it.st } : null, said: (document.querySelector("#p-asked .ask-said") || {}).textContent || "" }; }, first.keep);
          ok(w + "“Tell me when it is answered” keeps the listed question (our words) on this device and says where", !!kept.it && kept.it.q === first.q.slice(0, 200) && kept.it.sent === 1 && kept.it.st === "wait" && /^We will tell you on this device\./.test(kept.said), JSON.stringify(kept));
          await p.evaluate(v => { if (v === null) localStorage.removeItem("pk-asked"); else localStorage.setItem("pk-asked", v); }, before); }
        await shot(p, width + "-started-asked");
      }
    }
    await go(p, "#auto", 400);
    await go(p, "#substances", 600);
    const sub = await p.evaluate(() => ({ h: (document.querySelector("#sub-started .auto-h") || {}).textContent || "", a: [...document.querySelectorAll("#sub-started .auto-pages a")].map(a => a.getAttribute("href") + " | " + a.querySelector(".wl-q").textContent), cards: document.querySelectorAll("#subgrid > *").length, wide: document.documentElement.scrollWidth > innerWidth + 1 }));
    ok(w + "under the drugs, “All drugs” lists the pages our system started, apart from the 30 checked pages", sub.h === "Pages our system started" && sub.a.includes("#auto/p-kava | Kava") && sub.cards === 30 && !sub.wide, JSON.stringify(sub));
    await p.click('#filters .chip:nth-child(2)'); await p.waitForTimeout(300);
    ok(w + "a family chosen shows that family's checked pages only", await p.evaluate(() => !document.querySelector("#sub-started .auto-pages") && document.querySelectorAll("#subgrid > *").length < 30));
    await p.click('#filters .chip:nth-child(1)'); await p.waitForTimeout(200);
    await go(p, "#auto/p-no-such-page", 500);
    ok(w + "an address of a page nobody started is the page for unknown addresses, never another page", await p.evaluate(() => !document.getElementById("view-auto").classList.contains("active")));
    await go(p, "#auto", 500);
    await p.click('#auto-list a[data-sheet="au_fixture_ketamine"]'); await p.waitForTimeout(600);
    const s1 = await sheet(p);
    ok(w + "an answer opens over the page in the site's own form: its question, the short answer, But, How do we know?", s1 && s1.title === "Can you get addicted to ketamine?" && /^FIXTURE\. Yes, some people do\./.test(s1.short) && /^But Most of the pretend studies/.test(s1.but) && s1.how.length === 2 && /Ketamine/.test(s1.eye), JSON.stringify(s1).slice(0, 400));
    ok(w + "it carries its quiet line, with “Not complete yet.”, and no evidence bars and no link to an evidence page it does not have", s1 && s1.line === LINE2 && s1.bars === 0 && s1.evLink === 0, s1 && s1.line + " | bars " + s1.bars + " | evidence links " + s1.evLink);
    ok(w + "its sources are APA 7 references with the journal in italics and the DOI as a link", s1 && s1.srcSummary === "Sources (2)" && s1.refs.length === 2 && s1.refs[0].text === "Fixture, A. B., & Sample, C. (2022). A pretend review of ketamine dependence for the checks. Journal of Checks, 11(2), 300–312. https://doi.org/10.0000/fixture.1" &&
      s1.refs[0].italic === "Journal of Checks, 11" && s1.refs[0].link === "https://doi.org/10.0000/fixture.1", s1 && JSON.stringify(s1.refs));
    ok(w + "it offers a way to report a mistake, the way to every answer the system wrote, and next questions from the checked answers", s1 && s1.report === "Report a mistake in this answer" && /^Everything written by our system/.test(s1.all) && s1.next >= 1 && !s1.wide, s1 && s1.report + " | " + s1.all + " | next " + s1.next);
    await shot(p, width + "-auto-sheet");
    await p.click("#evsheet button[data-auto-report]"); await p.waitForTimeout(400);
    const fb = await p.evaluate(() => ({ open: document.getElementById("report").classList.contains("open"), mode: (document.querySelector('.fb-opt[aria-pressed="true"]') || { dataset: {} }).dataset.mode, sheet: document.getElementById("evsheet").classList.contains("open") }));
    ok(w + "“Report a mistake in this answer” opens the report form", fb.open && fb.mode === "issue" && !fb.sheet, JSON.stringify(fb));
    await p.click("#report-close"); await p.waitForTimeout(200);
    // ---- the search box
    await go(p, "#home", 400);
    await p.click("#search"); await p.fill("#search", "is ketamine addictive"); await p.waitForFunction(() => window.pkInsight && pkInsight.state() === "ready", null, { timeout: 120000 });
    await p.waitForFunction(() => { const b = document.querySelector("#search-results > .sr-fit"); return b && b.dataset.q === "is ketamine addictive"; }, null, { timeout: 20000 }); await p.waitForTimeout(200);
    const row = await p.evaluate(() => { const a = document.querySelector("#search-results .sr-fit a.sr-best"); return a ? { auto: a.classList.contains("sr-auto"), id: a.dataset.insight, k: a.querySelector(".k").textContent, t: a.querySelector(".t").textContent, a: a.querySelector(".a").textContent, m: a.querySelector(".m").textContent, bars: a.querySelectorAll(".meter").length,
      head: (document.querySelector("#search-results .sr-fit .sr-fit-h") || {}).textContent || "", live: document.getElementById("search-count").textContent, want: !!document.querySelector("#search-results .sr-want") } : null; });
    ok(w + "the search box finds it by a question in other words, as the best match, and says before it is opened that our system wrote it and that a person has not checked it", row && row.auto && row.id === "au_fixture_ketamine" && row.k === "Ketamine" && row.t === "Can you get addicted to ketamine?" && /^FIXTURE\. Yes/.test(row.a) &&
      row.m === "Written by our system · not yet checked by a person" && row.bars === 0 && row.head === "Best match" && /^Best match: Can you get addicted to ketamine\?/.test(row.live) && !row.want, JSON.stringify(row));
    await shot(p, width + "-auto-search");
    await p.keyboard.press("Enter"); await p.waitForTimeout(700);
    const s2 = await sheet(p);
    ok(w + "Enter opens the reader's own question with the answer under it, labelled as written by our system", s2 && s2.title === "Is ketamine addictive" && s2.label === "Written by our system · Ketamine" && s2.line === LINE2 && s2.bars === 0 && s2.refs.length === 2, s2 && s2.title + " | " + s2.label + " | " + s2.line);
    await p.keyboard.press("Escape"); await p.waitForTimeout(300); await p.fill("#search", ""); await p.keyboard.press("Escape");
    // ---- its drug's page
    await go(p, "#s-ketamine", 700);
    const sec = await p.evaluate(() => { const b = document.getElementById("sm-d-auto"); return b ? { name: b.querySelector(".sm-n").textContent, n: (b.querySelector(".sm-c") || {}).textContent || "", line: (b.querySelector(".sm-l") || {}).textContent || "", among: [...document.querySelectorAll("#drug2 details.ask[data-cid]")].some(d => /^au_/.test(d.dataset.cid)) } : null; });
    ok(w + "the ketamine page lists it in a section of its own, “Written by our system”, never among the checked answers", sec && sec.name === "Written by our system" && sec.n === "1 answer" && sec.line === "Not yet checked by a person" && !sec.among, JSON.stringify(sec));
    await p.click("#sm-d-auto"); await p.waitForTimeout(500);
    const inSec = await p.evaluate(() => { const s = document.getElementById("d-auto"); return s ? { note: (s.querySelector(".auto-sec") || {}).textContent || "", rows: [...s.querySelectorAll(".auto-i")].map(r => r.querySelector(".wl-q").textContent + " | " + r.querySelector(".auto-meta").textContent), hash: location.hash } : null; });
    ok(w + "the section says what these are, and lists the answer", inSec && /A person has not checked them yet\.$/.test(inSec.note) && inSec.rows.join() === "Can you get addicted to ketamine? | 2 papers · 15 November 2026 · not complete yet" && inSec.hash === "#s-ketamine/part-d-auto", JSON.stringify(inSec));
    await shot(p, width + "-auto-drug-page");
    await p.click('#d-auto a[data-sheet="au_fixture_ketamine"]'); await p.waitForTimeout(600);
    const s3 = await sheet(p); ok(w + "from the drug's page it opens over the page, and Back returns to the section", s3 && s3.line === LINE2 && (await p.evaluate(() => location.hash)) === "#s-ketamine/part-d-auto", s3 && s3.line);
    await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    ok(w + "a drug the system wrote nothing about has no such section", !(await (async () => { await go(p, "#s-cannabis", 600); return p.evaluate(() => !!document.getElementById("sm-d-auto")); })()));
    // ---- an answer about no drug, complete: the other line
    await go(p, "#auto/q-au_fixture_police", 900);
    const s4 = await sheet(p);
    ok(w + "an address of its own opens the answer over the list; a complete answer from one paper says so in its line", s4 && s4.title === "Do police crackdowns cut drug use, or just move it somewhere else?" && s4.line === LINE1 && s4.srcSummary === "Sources (1)" && (await p.evaluate(() => document.getElementById("view-auto").classList.contains("active"))), s4 && s4.title + " | " + s4.line);
    await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    // ---- 2.7: an answer that read a paper in full, a paper in summary and an official body's page
    await go(p, "#auto/q-au_fixture_caffeine", 900);
    const s6 = await sheet(p);
    ok(w + "an answer that read a paper, a summary and an official page says so in its line; the page's reference is APA 7 for a web page, with its exact date, its title in italics and its address as a link",
      s6 && s6.line === "Written by our system from 1 paper, the summary of 1 paper and 1 official page. Not yet checked by a person. Not complete yet." && s6.srcSummary === "Sources (3)" && s6.how.length === 3 &&
        s6.refs.some(r => r.text === "Pretend Health Service. (2025, March 2). A pretend page about caffeine for the checks. https://example.org/pretend-caffeine" && r.italic === "A pretend page about caffeine for the checks" && r.link === "https://example.org/pretend-caffeine"), s6 && s6.line + " | " + JSON.stringify(s6.refs));
    const hq = await p.evaluate(() => { const d = document.querySelector("#evsheet.open .ask-how"); if (d) d.open = true; return [...document.querySelectorAll("#evsheet.open .ask-howl li")].map(li => ({ q: (li.querySelector(".how-q q") || {}).textContent || "", src: (li.querySelector(".how-src") || {}).textContent || "" })); });
    ok(w + "under a How-do-we-know line stand its source's own words, 15 at most, with whose they are; words that are not in the source are never shown", hq.length === 3 && hq[0].q === "pretend words of a pretend trial" && hq[0].src === "Fixture, 2023" && hq[1].q === "" && hq[2].q === "" && !(await p.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)), JSON.stringify(hq));
    await shot(p, width + "-auto-how-quote");
    await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    // ---- 2.7: an answer about amounts (decision 11): the code's own lines, then each amount in its source's own words
    await go(p, "#auto/q-au_fixture_methadone", 900);
    const am = await p.evaluate(() => { const s = document.querySelector("#evsheet.open .panel .ins"); if (!s) return null; const a = s.querySelector(".ins-ans") || s, first = a.querySelector(".auto-first"), short = a.querySelector(".ask-short");
      return { first: first ? first.textContent : "", firstFirst: !!(first && short && (first.compareDocumentPosition(short) & Node.DOCUMENT_POSITION_FOLLOWING)), short: short ? short.textContent : "", but: (a.querySelector(".ask-but") || {}).textContent || "",
        rows: [...a.querySelectorAll(".auto-rows .ar")].map(li => ({ who: li.querySelector(".ar-who").textContent, q: li.querySelector(".ar-q").textContent, src: li.querySelector(".ar-src").textContent })), how: !!a.querySelector(".ask-how"),
        line: (a.querySelector(".auto-l") || {}).textContent || "", refs: [...a.querySelectorAll(".auto-refs li")].map(li => li.textContent), bars: a.querySelectorAll(".meter").length, wide: document.documentElement.scrollWidth > innerWidth + 1 }; });
    ok(w + "an answer about amounts opens with the line about tolerance (an opioid), then the two lines the code writes: none of them a model's", am && am.first === LINES.first.opioids.text && am.firstFirst && am.short === LINES.amounts && am.but === LINES.amounts_but, JSON.stringify(am).slice(0, 400));
    ok(w + "each amount stands in its source's own words, 15 at most, with who received it, under what care, and whose words they are; a paper read in summary says so", am && am.rows.length === 2 && am.rows.every(r => r.q.split(/\s+/).length <= 15 && /\d/.test(r.q)) &&
      am.rows[0].who === "FIXTURE. People starting pretend treatment, under supervision; the first amount on a pretend label." && am.rows[0].q === "the pretend first amount should not exceed 30 mg" && am.rows[0].src === "Pretend Maker, n.d." && am.rows[1].src === "Fixture, 2021, read in summary only", am && JSON.stringify(am.rows));
    ok(w + "it has no “How do we know?” of a writer, no bars, its quiet line, and its label's reference with the day it was read (a page without a date)", am && !am.how && am.bars === 0 && !am.wide && am.line === "Written by our system from the summary of 1 paper and 1 official page. Not yet checked by a person. Not complete yet." &&
      am.refs.includes("Pretend Maker. (n.d.). A pretend label for the checks [Drug label]. DailyMed. Retrieved November 15, 2026, from https://example.org/pretend-label"), am && am.line + " | " + JSON.stringify(am.refs));
    await shot(p, width + "-auto-amounts");
    // ---- 2.7.2: amounts that are an official body's guidance: the But written for that, and a count of drinks written as a word
    await go(p, "#auto/q-au_fixture_drinks", 900);
    const dr = await p.evaluate(() => { const s = document.querySelector("#evsheet.open .panel .ins"); if (!s) return null; const a = s.querySelector(".ins-ans") || s;
      return { first: !!a.querySelector(".auto-first"), short: (a.querySelector(".ask-short") || {}).textContent || "", but: (a.querySelector(".ask-but") || {}).textContent || "", rows: [...a.querySelectorAll(".auto-rows .ar")].map(li => ({ who: li.querySelector(".ar-who").textContent, q: li.querySelector(".ar-q").textContent, src: li.querySelector(".ar-src").textContent })) }; });
    ok(w + "an answer whose amounts are all an official body's guidance carries the But written for guidance, and no line about tolerance", dr && !dr.first && dr.short === LINES.amounts && dr.but === LINES.amounts_but_guidance && dr.but !== LINES.amounts_but, JSON.stringify(dr).slice(0, 300));
    ok(w + "a count of drinks written as a word is an amount: one row for men and one for women, each in the body's own words", dr && dr.rows.length === 2 && dr.rows[0].q === "For pretend men-two drinks or less in a day" && dr.rows[1].q === "For pretend women-one drink or less in a day" && dr.rows.every(r => r.src === "Pretend Health Body, 2026"), dr && JSON.stringify(dr.rows));
    await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    ok(w + "an amount that is not in its source's own words never reaches the page: the build leaves that answer out and names it", /au_fixture_badamount \(an amount that is not in its source's own words/.test(b.stderr) && await p.evaluate(() => !AUTO.au_fixture_badamount));
    ok(w + "an amount for each kilogram of body weight, or a summary's flattened signs, never reaches the page even in its source's own words (2.8.1)", /au_fixture_perkg \(an amount for each kilogram of body weight/.test(b.stderr) && await p.evaluate(() => !AUTO.au_fixture_perkg));
    await p.keyboard.press("Escape"); await p.waitForTimeout(300);
    // ---- the list of questions not answered yet, and a kept question
    await go(p, "#wanted", 500);
    const wl = await p.evaluate(() => ({ ids: WANTED.map(x => x[0]), text: document.getElementById("wanted-list").textContent }));
    ok(w + "the questions the system answered have left “On our list”", !wl.ids.includes("w_0024") && !wl.ids.includes("w_0007") && !/Can you get addicted to ketamine\?/.test(wl.text) && wl.ids.length >= 30, wl.ids.length + " listed");
    await p.evaluate(() => { localStorage.setItem("pk-asked", JSON.stringify([{ k: "can you get addicted to ketamine?", q: "Can you get addicted to ketamine?", d: "", t: Date.now() - 864e5, cv: "0.0.1", st: "wait", sent: 1, w: "w_0024" }])); });
    await go(p, "#home", 300); await p.reload(); await p.waitForSelector("#yousheet .aq.ans", { state: "attached", timeout: 120000 });
    const an = await p.evaluate(() => { const r = document.querySelector("#yousheet .aq.ans"); return { k: r.querySelector(".aq-k").textContent, q: r.querySelector(".aq-q").textContent, href: r.querySelector("a.aq-a").getAttribute("href") }; });
    ok(w + "a question the reader asked to be told about turns “Answered” when the system has answered it, and leads to that answer", an.k === "Answered" && an.q === "Can you get addicted to ketamine?" && an.href === "#auto/q-au_fixture_ketamine", JSON.stringify(an));
    await p.click("#home-asked .you-bar"); await p.waitForTimeout(400); await p.click("#yousheet .aq.ans a.aq-a"); await p.waitForTimeout(1100);
    const s5 = await sheet(p); ok(w + "reading it opens the answer with its line", s5 && s5.line === LINE2, s5 && s5.line);
    await p.context().close();
  }
  {
    // ---- the build's own stamp: a question that waits is asked again once per publishing, and an open page learns of a newer site
    const p = await open(390), stamp = JSON.parse(fs.readFileSync(path.join(ROOT, "data", "build.json"), "utf8"));
    const pg = await p.evaluate(() => ({ build: SITE_BUILD, loop: AUTO_LOOP, sent: ASK_SENT }));
    ok("the build has a stamp of its own, in the page and in a small file beside it", /^\d{12}$/.test(pg.build) && stamp.build === pg.build && stamp.site === (await p.evaluate(() => SITE_VERSION)), JSON.stringify(stamp) + " / " + pg.build);
    ok("a site whose half-hourly run is on says so to a reader who sends a question (this build has the switch on)", pg.loop === true && /^Sent\. Our system starts on it within half an hour\. If it finds research it can read, the answer is usually here within the hour: your question then turns green/.test(pg.sent), pg.sent);
    await p.evaluate(() => localStorage.setItem("pk-asked", JSON.stringify([{ k: "what is the capital of mongolia", q: "what is the capital of mongolia", d: "", t: Date.now(), cv: SITE_BUILD, st: "wait", sent: 1 }])));
    await p.reload(); await p.waitForTimeout(900);
    const quiet = await p.evaluate(async () => ({ rows: document.querySelectorAll("#yousheet .aq.wait").length, newer: !!document.querySelector("#home-asked .aq-new"), look: await askedLook() }));
    ok("a question that waits: nothing is said while the site on the server is this one", quiet.rows === 1 && !quiet.newer && quiet.look === false, JSON.stringify(quiet));
    await p.route("**/data/build.json", r => r.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ build: "209901010000", site: "9.9.9" }) }));
    const told = await p.evaluate(async () => { const n = await askedLook(), el = document.querySelector("#home-asked .aq-new"); return { n, text: el ? el.textContent : "", btn: !!document.querySelector("#home-asked button[data-asked-reload]"), wide: document.documentElement.scrollWidth > innerWidth }; });
    ok("when a newer site is on the server, the list says so once and offers to load it", told.n === true && told.text === "The site has new answers. Load them to see whether yours is among them." && told.btn && !told.wide, JSON.stringify(told));
    await shot(p, "390-newer-site");
    await p.unroute("**/data/build.json");
    await Promise.all([p.waitForNavigation({ timeout: 20000 }).catch(() => null), p.click("#home-asked button[data-asked-reload]")]); await p.waitForTimeout(900);
    ok("Load them loads the page again; the question still waits and the line is gone", await p.evaluate(() => document.querySelectorAll("#yousheet .aq.wait").length === 1 && !document.querySelector("#home-asked .aq-new")));
    await p.context().close();
  }
  ok("no error in any page's console", !errors.length, errors.slice(0, 3).join(" | "));
  await browser.close(); server.close();
  if (!process.argv.includes("--keep")) { const r = build({ PK_AUTO_FIXTURE: "", PK_AUTO_LOOP: "" }); ok("the site is built again without the pretend answers", r.status === 0 && !fs.readFileSync(path.join(ROOT, "index.html"), "utf8").includes("au_fixture_") /* (since 16 November 2026 the site shows real answers of the system: their count is no longer a sign of a pretend one) */, (r.stdout + r.stderr).slice(-300)); }
  console.log(fail ? fail + " checks failed, " + pass + " passed" : "All " + pass + " checks passed");
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
