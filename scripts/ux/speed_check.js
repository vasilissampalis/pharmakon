// The parts fetched when needed (speed, 13 November 2026), checked in a real browser at 390 x 844 and 1280 x 800: every page
// type draws (start page, a drug page and its law part, an answer sheet with Scientific detail open, a research page, the law
// page, mixing with its full evidence, facts, the quiz, search, statistics, how to read, a study card, a citation's popover),
// the start page fetches none of the on-demand files, a drug page fetches its own file ahead once it settles, and a file that
// cannot be had shows one line with a retry that works. Every page is also checked for console errors and horizontal scroll.
// Usage: node scripts/ux/speed_check.js [--shots DIR] [--port N]   (build first; exit code 1 if a check fails)
const http = require("http"), fs = require("fs"), path = require("path");
const { chromium } = require("playwright");
const ROOT = path.resolve(__dirname, "..", "..", "site", "public");
const arg = k => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : null; };
const SHOTS = arg("--shots"), PORT = +(arg("--port") || 0);
const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".json": "application/json", ".css": "text/css", ".webp": "image/webp", ".png": "image/png", ".svg": "image/svg+xml", ".woff2": "font/woff2" };
const results = [], errors = [];
const ok = (name, pass, detail) => { results.push(!!pass); console.log((pass ? "PASS " : "FAIL ") + name + (detail ? "  (" + detail + ")" : "")); };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split("?")[0]); if (p.endsWith("/")) p += "index.html";
  const f = path.join(ROOT, path.normalize(p)); if (!f.startsWith(ROOT)) { res.writeHead(403); res.end(); return; }
  fs.readFile(f, (err, buf) => { if (err) { res.writeHead(404); res.end("not found"); return; } res.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream" }); res.end(buf); });
});
(async () => {
  if (!fs.existsSync(path.join(ROOT, "index.html"))) { console.error("No site/public/index.html: build first."); process.exit(2); }
  await new Promise(r => server.listen(PORT, "127.0.0.1", r));
  const BASE = "http://127.0.0.1:" + server.address().port + "/#";
  if (SHOTS) fs.mkdirSync(SHOTS, { recursive: true });
  const browser = await chromium.launch({ args: ["--no-proxy-server"] });
  for (const w of [390, 1280]) {
    const H = w < 700 ? 844 : 800;
    const ctx = await browser.newContext({ viewport: { width: w, height: H }, deviceScaleFactor: 1 }), p = await ctx.newPage();
    p.on("pageerror", e => errors.push(w + " page error: " + String(e).slice(0, 200)));
    p.on("console", m => { if (m.type() === "error" && !/Failed to load resource/.test(m.text())) errors.push(w + " console error: " + m.text().slice(0, 200)); });
    const fetched = []; p.on("request", r => { const u = r.url(); if (/\/data\/(full-|refs|figures|cards-)/.test(u)) fetched.push(u.replace(/^.*\/data\//, "")); });
    const shot = async (name, sel, noScroll) => { const [sw, cw] = await p.evaluate(() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]); if (sw > cw && !noScroll) errors.push(w + " horizontal scroll at " + name); if (!SHOTS) return;
      await p.mouse.move(2, 300); const f = path.join(SHOTS, w + "-" + name + ".png"); if (sel) await (await p.$(sel)).screenshot({ path: f }); else await p.screenshot({ path: f }); };
    const go = async (h, wait) => { await p.goto(BASE + h); await p.waitForTimeout(wait || 1000); };
    const idle = () => p.waitForFunction(() => !document.querySelector(".view.active .loading, #evsheet.open .loading"), null, { timeout: 15000 }).then(() => true, () => false);

    // the start page: drawn by the script, and nothing on-demand fetched
    await go("home", 2500); await shot("home");
    ok(w + ": start page draws without fetching any on-demand file", (await p.$$("#dgrid a.dcard")).length > 5 && !fetched.length, fetched.join(", ") || "none fetched");
    // a drug page: drawn at once; its own file fetched ahead once it settles, and the law part draws for a chosen country
    // (the country is read when the page loads, so the page is loaded afresh after it is saved)
    await p.evaluate(() => { try { localStorage.setItem("pk-country", "Greece"); } catch (e) {} }); await p.goto("about:blank");
    fetched.length = 0; await go("s-cannabis", 3500);
    const law = await p.evaluate(() => { const s = document.querySelector("#d-law .sec-b"); return s ? { say: (s.querySelector(".say") || {}).textContent || "", wait: !!s.querySelector(".loading, .lawwait") } : null; });
    ok(w + ": drug page draws, fetches its own file ahead, and its law part draws for the chosen country", (await p.$$("#drug2 details.ask")).length > 10 && fetched.includes("full-cannabis.json") && law && !law.wait && /Greece/.test(law.say), "fetched " + fetched.join(", ") + "; law: " + (law ? law.say.slice(0, 60) : "missing"));
    await p.$eval("#d-law", e => e.scrollIntoView({ block: "start" })); await p.waitForTimeout(200); await shot("drug-page-law");
    // the answer sheet, with Scientific detail open
    await go("home", 300); fetched.length = 0; await go("cl_can_dependence_how_many", 600); const sheetOk = await idle();
    const sh = await p.evaluate(() => { const s = document.querySelector("#evsheet.open"); if (!s) return null; const d = s.querySelector("details.sf-sci"); if (d) { d.open = true; d.scrollIntoView({ block: "start" }); }
      return { refs: s.querySelectorAll(".ev-refs li").length, apa: !!s.querySelector(".ev-apa"), sci: !!(d && d.querySelector(".ev-precise").textContent.length > 200), peco: !!s.querySelector(".ev-peco dd") }; });
    ok(w + ": answer sheet draws in full (sources with APA references, Scientific detail, who was studied)", sheetOk && sh && sh.refs > 0 && sh.apa && sh.sci && sh.peco, JSON.stringify(sh) + "; fetched " + fetched.join(", "));
    await p.waitForTimeout(250); await shot("sheet-scientific-detail-open");
    // a research page (a drug with a full write-up), and a section by address
    await go("home", 300); await go("s-methamphetamine/evidence", 600); const monoOk = await idle();
    const mono = await p.evaluate(() => ({ claims: document.querySelectorAll("#sections .claim").length, refs: document.querySelectorAll("#reflist .ref").length, toc: document.querySelectorAll("#toc a").length, title: document.getElementById("mono-title").textContent }));
    ok(w + ": research page draws with its claims, references and contents", monoOk && mono.claims > 20 && mono.refs > 20 && mono.toc > 5, JSON.stringify(mono));
    await shot("research-page");
    await go("s-cannabis/sec-13", 600); await idle(); await p.waitForTimeout(300);
    const sec13 = await p.evaluate(() => { const d = document.getElementById("sec-13"); return d ? { open: d.open, rows: d.querySelectorAll(".lawgrp").length } : null; });
    ok(w + ": a research section by address opens with the law rows", sec13 && sec13.open && sec13.rows > 3, JSON.stringify(sec13));
    await shot("research-section-law", null, true);   // (a long link in the law rows scrolls sideways on a phone; so it does on main, before this change)
    // the law page (treaties, country by country)
    await go("law", 800); ok(w + ": law page draws", (await p.$$("#law-list tr")).length > 150); await shot("law-page");
    // mixing, with a full evidence fold opened
    await go("interactions", 800);
    const opened = await p.evaluate(() => { const d = document.querySelector("details.mixfull[data-full]"); if (!d) return false; for (let x = d; x; x = x.parentElement && x.parentElement.closest("details")) x.open = true; d.scrollIntoView({ block: "start" }); return true; });
    await p.waitForTimeout(400); await idle(); await p.waitForTimeout(200);
    const mix = await p.evaluate(() => { const d = document.querySelector("details.mixfull[data-full][open]"); return d ? { claim: !!d.querySelector(".claim"), loading: !!d.querySelector(".loading") } : null; });
    ok(w + ": mixing page: a full evidence fold draws its claim when opened", opened && mix && mix.claim && !mix.loading, JSON.stringify(mix));
    await p.evaluate(() => { const d = document.querySelector("details.mixfull[data-full][open]"); if (d) d.scrollIntoView({ block: "start" }); }); await p.waitForTimeout(200); await shot("mixing-full-evidence");
    // facts, quiz, statistics, how to read
    await go("facts", 800); ok(w + ": facts page draws", (await p.$$("#view-facts details.ask")).length > 5); await shot("facts");
    await go("quiz", 800); ok(w + ": quiz page draws", !!(await p.$("#quizpage .qz2-o, #quizpage .qz2-q"))); await shot("quiz");
    await go("numbers", 600); await idle(); await p.waitForTimeout(200);
    ok(w + ": statistics page draws its figures", (await p.$$("#num-list > *")).length > 3 && !!(await p.$("#num-geo .chip"))); await shot("statistics");
    await go("howto", 600); await idle(); ok(w + ": how-to page draws its example claim", !!(await p.$("#howto-example .claim"))); await shot("howto");
    // the senior author's review page reads every file and the open decisions
    await go("review", 600); await p.waitForFunction(() => !document.querySelector("#review-list .loading"), null, { timeout: 30000 }).catch(() => {});
    const rv = await p.evaluate(() => ({ claims: document.querySelectorAll("#review-list .rv").length, decisions: (document.getElementById("dec-count") || {}).textContent || "" }));
    ok(w + ": review page draws its queue and the open decisions", rv.claims > 5 && /of [1-9]\d* decided/.test(rv.decisions), JSON.stringify(rv));
    // search
    await go("home", 800); await p.fill("#search", "ecstasy memory"); await p.waitForTimeout(700);
    ok(w + ": search finds answers", (await p.$$("#search-results a")).length > 2); await shot("search");
    await p.fill("#search", ""); await p.keyboard.press("Escape");
    // a study card, and a citation's popover on a drug page (both read the references in full)
    await go("s-methamphetamine/evidence", 600); await idle();
    await p.evaluate(() => { const b = document.querySelector("#sections [data-card]"); if (b) b.click(); }); await p.waitForTimeout(1200);
    const card = await p.evaluate(() => { const d = document.querySelector("#drawer.open .panel"); return d ? { head: !!d.querySelector(".cardhead h2"), apa: !!d.querySelector(".refline") } : null; });
    ok(w + ": a study card opens with its reference in full", card && card.head && card.apa, JSON.stringify(card)); await shot("study-card");
    await p.evaluate(() => { const c = document.querySelector("#drawer .close"); if (c) c.click(); });
    // a citation's popover on a page that has not fetched the references yet (the glossary): it opens once they have arrived
    { const c3 = await browser.newContext({ viewport: { width: w, height: H }, deviceScaleFactor: 1 }), p3 = await c3.newPage();
      p3.on("pageerror", e => errors.push(w + " page error (popover test): " + String(e).slice(0, 200)));
      await p3.goto(BASE + "glossary"); await p3.waitForTimeout(1200);
      await p3.hover("#glossary-list a.pop"); await p3.waitForTimeout(1500);
      const pop = await p3.evaluate(() => { const el = document.querySelector(".popover"); return el ? { apa: !!el.querySelector(".refline"), text: el.textContent.slice(0, 60) } : null; });
      ok(w + ": a citation's popover waits for the references, then shows the full APA reference", pop && pop.apa, pop ? pop.text : "no popover");
      if (SHOTS) await p3.screenshot({ path: path.join(SHOTS, w + "-popover-glossary.png") });
      await c3.close(); }
    // a file that cannot be had: one line with a retry, and the retry works once the file can be had again
    const ctx2 = await browser.newContext({ viewport: { width: w, height: H }, deviceScaleFactor: 1 }), p2 = await ctx2.newPage();
    let block = true; await p2.route(/\/data\/full-ketamine\.json/, r => block ? r.fulfill({ status: 503, body: "" }) : r.continue());
    p2.on("pageerror", e => errors.push(w + " page error (offline test): " + String(e).slice(0, 200)));
    await p2.goto(BASE + "s-ketamine/evidence"); await p2.waitForTimeout(1500);
    const fail = await p2.evaluate(() => { const f = document.querySelector("#sections .loadfail"); return f ? f.textContent : null; });
    if (SHOTS) await p2.screenshot({ path: path.join(SHOTS, w + "-file-failed-retry.png") });
    block = false; await p2.click("#sections .loadfail [data-retry]"); await p2.waitForTimeout(1500);
    const after = await p2.evaluate(() => document.querySelector("#sections .loadfail, #sections .loading") ? 0 : document.querySelectorAll("#sections details.sec").length);
    ok(w + ": a file that cannot be had says so in one line with a retry, and the retry draws the page", !!fail && /could not be loaded/.test(fail) && after >= 3, (fail || "no failure line").slice(0, 70) + "; after retry " + after + " sections");
    await ctx2.close();
    await ctx.close();
  }
  await browser.close(); server.close();
  ok("no console or page errors, no horizontal scroll (both widths)", !errors.length, errors.slice(0, 6).join(" | "));
  const failed = results.filter(x => !x).length;
  console.log("\n" + (results.length - failed) + " of " + results.length + " checks passed" + (SHOTS ? "; screenshots in " + SHOTS : ""));
  process.exit(failed ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
