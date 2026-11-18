// instant_trial.mjs: the papers' own words on a question (site/worker/_worker.js, /api/find), tried with the REAL index of papers on the
// editor's own questions (GitHub's machines; .github/workflows/lane.yml, requests instant-*.json).
//
//   node scripts/auto/instant_trial.mjs REQUESTS_DIR OUT_DIR [USAGE.json]
//
// Why: the editor's workspace cannot reach Europe PMC or the site. This runs the very code the site's server runs (the same file, imported)
// against the real Europe PMC, so that what a reader would be shown is read by the editor before a reader meets it.
// Since site 2.20 no model takes part: no key is used, nothing is spent, and USAGE.json (still written, for the workflow's step) is empty.
// A request: {"questions": [{"q": "...", "names": ["..."], "words": ["..."], "also": ["..."], "def": 1, "t": 1}]}. The questions are the editor's own (never a
// visitor's); "q" is only a label here: the server gets the names and the key words, as it does from the page.
// What is written (OUT_DIR/trial-<time>.json), for each question: what Europe PMC was asked and how many papers each search gave; the
// papers in the order a reader would see them (title, kind, year, journal) with the words shown for each, or why none were; the time it
// took, and the server's own computing time for it (the same request run again from memory).
// Time (after the sixth trial). The server no longer waits for a slow search: it gives the list it has and says "more"; the page then asks again
// after half a second, and once more two seconds after that. The trial does the same: ms is when the first list came; more whether a search was still out then;
// whole_ms when the whole list was there; asks how often the server was asked. As on the site, each reply of Europe PMC is kept once it is complete (here in
// memory, there in Cloudflare's cache), so that a search asked again is not made again. Each search that went to Europe PMC is written under the
// question that began it, with whether it was a later asking of a slow one (second).
// A paper's summary is never copied here (it is its publisher's). For each line shown, "around" gives only the SHAPE of the rest of its
// sentence, so that the editor can see whether a word the sentence turns on was left outside the words shown: little words are written
// out (no, not, may, but, only, than, in rats ...), every other word is a "_" and every number a "#".
import fs from "node:fs";
import path from "node:path";
import { performance } from "node:perf_hooks";
import worker, { iaParts, iaPick, readFind, iaNearStems, nameForms } from "../../site/worker/_worker.js";

const [dir, outDir, usageFile] = process.argv.slice(2);
if (!dir || !outDir) { console.log("usage: node scripts/auto/instant_trial.mjs REQUESTS_DIR OUT_DIR [USAGE.json]"); process.exit(2); }
const files = fs.existsSync(dir) ? fs.readdirSync(dir).filter(f => /^instant-.*\.json$/.test(f)).sort() : [];
if (usageFile) fs.writeFileSync(usageFile, "[]");
if (!files.length) { console.log("instant trial: no request"); process.exit(0); }
console.log("instant trial: " + files.length + " request(s); no model takes part");

// what Europe PMC gave, kept in memory only: to work out "around", to say why a paper got no words, and to run the request again without the network
const summaries = new Map(), replies = new Map(); let asked = [];
const viaNet = async (u, o) => { const t0 = Date.now(), url = String(u), mine = asked, second = !/search\?query=/.test(url), q = decodeURIComponent((url.split(/[?&]query=/)[1] || "").split("&")[0]).slice(0, 700), sort = (url.match(/&sort=([A-Z_]+)/) || [])[1] || "";
  let r = null, text = "";
  try { r = await fetch(u, o); text = await r.text(); } catch (e) { mine.push(Object.assign({ q, sort, failed: String(e && e.name), ms: Date.now() - t0 }, second ? { second: true } : {})); throw e; }
  let list = []; try { list = ((JSON.parse(text).resultList || {}).result) || []; } catch (e) { list = []; }
  for (const x of list) { const ab = String(x.abstractText || ""); if (x.doi) summaries.set("doi:" + x.doi, ab); if (x.pmid) summaries.set("pmid:" + x.pmid, ab); }
  replies.set(url, { status: r.status, text });
  mine.push(Object.assign({ q, sort, status: r.status, ms: Date.now() - t0, kb: Math.round(text.length / 1024), papers: list.map(x => String(x.pubYear || "") + " " + String(x.title || "").replace(/<[^>]+>/g, "").slice(0, 110)) }, second ? { second: true } : {}));
  return new Response(text, { status: r.status, headers: { "content-type": "application/json" } }); };
// what the server keeps of Europe PMC's replies (on the site: Cloudflare's cache), stood in for by a list in memory
const KEPT = new Map(), CACHE = { match: async u => (KEPT.has(String(u)) ? new Response(KEPT.get(String(u))) : undefined), put: async (u, res) => { KEPT.set(String(u), await res.text()); } };
const fromMemory = async u => { const r = replies.get(String(u)); return r ? new Response(r.text, { status: r.status, headers: { "content-type": "application/json" } }) : new Response("{}", { status: 200 }); };
const LITTLE = new Set(("a an the of in on at to for from by with and or but that which who whom whose than as is are was were be been being it its their they this these those there into over under after before during while when where also both either neither nor not no none never without cannot " +
  "may might could can would should must suggest suggests suggested appear appears seem seems possibly possible potential potentially likely unlikely unclear unknown whether if although though however whereas despite except unless only just even rather instead versus compared comparison " +
  "all most many much some few fewer several any each every more less least higher lower greater smaller significant significantly non-significant rats rat mice mouse animals animal cells vitro vivo humans human people patients participants volunteers adults placebo controls " +
  "did does do has have had will limited preliminary mixed inconsistent inconclusive claimed reported believed thought examined investigated assessed evaluated aimed remains remain case cases pilot open-label survey observational " +
  "safe safely safety tolerated well-tolerated recommend recommended dose doses dosage daily children adolescents pregnant death deaths combination combined together among within across between through via per about against until since because due given based using including such other another same our we he she his her here then thus therefore hence moreover furthermore additionally overall taken conclusion conclusions summary results findings data study studies evidence authors report reports show shows showed shown found demonstrate demonstrated demonstrates indicate indicated indicates reveal revealed provide provided support supported confirm confirmed associated association increased decreased reduced improved impaired").split(" "));
const shape = words => words.filter(w => /[A-Za-z0-9]/.test(w)).map(w => { const core = w.toLowerCase().replace(/[^a-z'-]/g, ""), tail = (w.match(/[,;:.)]+$/) || [""])[0], head = (w.match(/^[(]+/) || [""])[0]; return head + (/\d/.test(w) ? "#" : LITTLE.has(core) || /n't$/.test(core) ? core : "_") + tail; }).join(" ");
const abOf = p => summaries.get(p.doi ? "doi:" + p.doi : "pmid:" + p.pmid) || "";
const around = p => { const words = String(p.q).replace(/…/g, "").trim();
  for (const x of iaParts(abOf(p))) { const i = x.s.indexOf(words); if (i < 0) continue;
    return { before: shape(x.s.slice(0, i).trim().split(/\s+/)), shown: words.split(/\s+/).length, after: shape(x.s.slice(i + words.length).trim().split(/\s+/)), part: x.sec || "no label" }; }
  return { missing: true }; };
// why a paper got no words, in the rule's own terms (worked out here from the summary in memory; nothing of the summary is written)
// tried: for a sentence that stood in the right place and held the key word, yet gave no 15 words that pass: its SHAPE (little words; K a key word of the question,
// D the drug's name, # a number, _ any other word), so that the editor can see which rule stopped it. Never the sentence.
const whyNone = (p, r) => { const ab = abOf(p); if (!ab) return { why: "it has no summary in Europe PMC" }; if (r.noq) return { why: r.gen ? "titles only: the question names no single drug" : "titles only: the question is about the law, prices or drug tests, about pregnancy or children, or the page asked for titles" };
  const parts = iaParts(ab), notes = [], at = [], all = r.names.concat(r.also || []); iaPick(Object.assign({}, p, { ab }), r.groups, all, r.def, (n, i) => { notes.push(n); if (typeof i === "number" && !at.includes(i)) at.push(i); });
  const stems = [...new Set(r.groups.flat().flatMap(iaNearStems))], names = all.flatMap(x => nameForms(x.split(" ")[0]));
  const mark = w => { const core = w.toLowerCase().replace(/[^a-z0-9'/-]/g, "").replace(/'s$/, ""), tail = (w.match(/[,;:.)]+$/) || [""])[0], head = (w.match(/^[(]+/) || [""])[0];
    return names.includes(core) || names.some(nm => core.startsWith(nm + "-")) ? head + "D" + tail : stems.some(st => core.split(/[-/]/).some(x => x.startsWith(st))) ? head + "K" + tail : null; };
  const tried = at.slice(0, 2).map(i => parts[i].s.split(/\s+/).filter(w => /[A-Za-z0-9]/.test(w)).map(w => mark(w) || shape([w])).join(" ") + " [" + (parts[i].sec || "no label") + "]");
  return Object.assign({ why: (notes.length ? [...new Set(notes)].join("; ") : "no sentence passed") + " (" + parts.length + " sentences" + (parts.some(x => x.sec) ? ", with labels" : "") + ")" }, tried.length ? { tried } : {}); };

fs.mkdirSync(outDir, { recursive: true });
for (const f of files) {
  let req = null; try { req = JSON.parse(fs.readFileSync(path.join(dir, f), "utf8")); } catch (e) { console.log("instant trial: " + f + " is not JSON"); continue; }
  const items = [];
  for (const q of Array.isArray(req.questions) ? req.questions.slice(0, 60) : []) {
    asked = []; const body = JSON.stringify(Object.assign({ names: q.names, words: q.words }, Array.isArray(q.also) && q.also.length ? { also: q.also } : {}, q.def ? { def: 1 } : {}, q.t ? { t: 1 } : {})), rf = readFind(JSON.parse(body));   // (t: titles only, as the page asks for a question about pregnancy or children or one that names no single drug)
    const post = env => worker.fetch(new Request("https://pharmakon.world/api/find", { method: "POST", headers: { "content-type": "application/json", origin: "https://pharmakon.world" }, body }), env);
    const t0 = Date.now(), mine = asked, live = { ASSETS: { fetch: async () => new Response("", { status: 404 }) }, FETCH: viaNet, CACHE }; let reply = null, status = 0;
    try { const r = await post(live); status = r.status; reply = await r.json(); } catch (e) { reply = { error: String(e && e.message).slice(0, 200) }; }
    const ms = Date.now() - t0, firstReply = reply; let asks = 1, wholeMs = ms;
    // as the page does: where a search was still out, ask again after half a second, and once more two seconds after that; the newer list takes the place of the first
    for (const wait of [500, 2000]) { if (!(reply && reply.more)) break; await new Promise(r => setTimeout(r, wait)); let r2 = null; try { r2 = await (await post(live)).json(); } catch (e) { r2 = null; } asks++;
      if (r2 && r2.ok && ((r2.papers || []).length || !((reply.papers || []).length))) { reply = r2; wholeMs = Date.now() - t0; } else break; }
    const idOf = p => p.doi || p.pmid, firstIds = ((firstReply && firstReply.papers) || []).map(idOf);
    // the server's own computing time: the same request again, from memory (the middle one of five)
    const again = []; for (let i = 0; i < 5; i++) { const c0 = performance.now(); try { await (await post({ ASSETS: {}, FETCH: fromMemory, CACHE })).json(); } catch (e) { /* not timed */ } again.push(performance.now() - c0); } again.sort((a, b) => a - b);
    const papers = ((reply && reply.papers) || []).map(p => Object.assign({ title: p.t, kind: p.kind, y: p.y, j: p.j, free: !!p.oa, id: p.doi || p.pmid }, p.q ? { shown: p.q, about: p.an === 1 ? "animals or cells" : p.an === 2 ? "its summary covers animals or cells too" : "", around: around(p) } : Object.assign({ shown: null }, rf.error ? { why: "" } : whyNone(p, rf))));
    items.push(Object.assign({ q: q.q, names: q.names, also: q.also || [], words: q.words, def: !!q.def, titles_only: !!(firstReply && firstReply.titles), status, ms, more: !!(firstReply && firstReply.more), search_ms: (firstReply && firstReply.ms) || [], asked_twice: (firstReply && firstReply.again) || 0, which_asking_answered: (firstReply && firstReply.won) || [], its_own_ms: (firstReply && firstReply.own) || [], from_kept: (firstReply && firstReply.kept) || 0 },
      firstReply && firstReply.more ? { asks, whole_ms: wholeMs, still_more: !!(reply && reply.more), first_list: firstIds.length, of_them_in_the_whole_list: firstIds.filter(i => ((reply && reply.papers) || []).some(p => idOf(p) === i)).length } : {},
      { server_ms: Math.round(again[2] * 10) / 10, held: !!(reply && reply.held), papers, searches: mine }));
    await new Promise(r => setTimeout(r, 400));   // (one question after another, with a breath between: Europe PMC is a shared service)
    console.log("instant trial: " + JSON.stringify(q.q) + ": " + papers.length + " paper(s), " + papers.filter(p => p.shown).length + " with their own words, first list after " + ms + " ms" + (firstReply && firstReply.more ? ", the whole list after " + wholeMs + " ms (" + asks + " askings)" : "") + " (the server's own share " + (Math.round(again[2] * 10) / 10) + " ms)");
  }
  const stamp = new Date().toISOString().replace(/[-:]/g, "").slice(0, 13), outFile = path.join(outDir, "trial-" + stamp + "-" + f.replace(/^instant-|\.json$/g, "") + ".json");
  fs.writeFileSync(outFile, JSON.stringify({ _note: "Made by scripts/auto/instant_trial.mjs: the papers' own words on a question (site/worker/_worker.js, /api/find) tried with the real index of papers on the editor's own questions. No model takes part. Nothing here is shown on the site. papers: in the order a reader would see them; shown: the paper's own words a reader would see under its title (null: none, with why); around: the shape of the rest of that sentence, little words only, every other word a '_' (a summary is never copied here); tried: the shape of a sentence that held the key word in the right place and gave no words (K a key word, D the drug's name); searches: what Europe PMC was asked, how long it took and what it gave (second: a slow search asked a second time; kept: answered from the reply kept before); ms: when the first list came; more: a search was still out then; whole_ms: when the whole list was there, the page asking again as it does; server_ms: the server's own computing time for the request.", made: new Date().toISOString(), why: String(req.why || "").slice(0, 300), v: 6, items }, null, 1));
  console.log("instant trial: written " + outFile);
}
