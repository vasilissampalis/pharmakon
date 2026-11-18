// instant_trial.mjs: the papers' own words on a question (site/worker/_worker.js, /api/find), tried with the REAL index of papers on the
// editor's own questions (GitHub's machines; .github/workflows/lane.yml, requests instant-*.json).
//
//   node scripts/auto/instant_trial.mjs REQUESTS_DIR OUT_DIR [USAGE.json]
//
// Why: the editor's workspace cannot reach Europe PMC or the site. This runs the very code the site's server runs (the same file, imported)
// against the real Europe PMC, so that what a reader would be shown is read by the editor before a reader meets it.
// Since site 2.20 no model takes part: no key is used, nothing is spent, and USAGE.json (still written, for the workflow's step) is empty.
// A request: {"questions": [{"q": "...", "names": ["..."], "words": ["..."], "also": ["..."], "def": 1}]}. The questions are the editor's own (never a
// visitor's); "q" is only a label here: the server gets the names and the key words, as it does from the page.
// What is written (OUT_DIR/trial-<time>.json), for each question: what Europe PMC was asked and how many papers each search gave; the
// papers in the order a reader would see them (title, kind, year, journal) with the words shown for each, or why none were; the time it
// took, and the server's own computing time for it (the same request run again from memory).
// A paper's summary is never copied here (it is its publisher's). For each line shown, "around" gives only the SHAPE of the rest of its
// sentence, so that the editor can see whether a word the sentence turns on was left outside the words shown: little words are written
// out (no, not, may, but, only, than, in rats ...), every other word is a "_" and every number a "#".
import fs from "node:fs";
import path from "node:path";
import { performance } from "node:perf_hooks";
import worker, { iaParts, iaPick, readFind } from "../../site/worker/_worker.js";

const [dir, outDir, usageFile] = process.argv.slice(2);
if (!dir || !outDir) { console.log("usage: node scripts/auto/instant_trial.mjs REQUESTS_DIR OUT_DIR [USAGE.json]"); process.exit(2); }
const files = fs.existsSync(dir) ? fs.readdirSync(dir).filter(f => /^instant-.*\.json$/.test(f)).sort() : [];
if (usageFile) fs.writeFileSync(usageFile, "[]");
if (!files.length) { console.log("instant trial: no request"); process.exit(0); }
console.log("instant trial: " + files.length + " request(s); no model takes part");

// what Europe PMC gave, kept in memory only: to work out "around", to say why a paper got no words, and to run the request again without the network
const summaries = new Map(), replies = new Map(); let asked = [];
const viaNet = async (u, o) => { const t0 = Date.now(), url = String(u); let r = null, text = "";
  try { r = await fetch(u, o); text = await r.text(); } catch (e) { asked.push({ q: decodeURIComponent(url.split("?query=")[1] || "").slice(0, 600), failed: String(e && e.name) }); throw e; }
  let list = []; try { list = ((JSON.parse(text).resultList || {}).result) || []; } catch (e) { list = []; }
  for (const x of list) { const ab = String(x.abstractText || ""); if (x.doi) summaries.set("doi:" + x.doi, ab); if (x.pmid) summaries.set("pmid:" + x.pmid, ab); }
  replies.set(url, { status: r.status, text });
  asked.push({ q: decodeURIComponent(url.split("?query=")[1] || "").slice(0, 700), status: r.status, ms: Date.now() - t0, kb: Math.round(text.length / 1024), papers: list.map(x => String(x.pubYear || "") + " " + String(x.title || "").replace(/<[^>]+>/g, "").slice(0, 110)) });
  return new Response(text, { status: r.status, headers: { "content-type": "application/json" } }); };
const fromMemory = async u => { const r = replies.get(String(u)); return r ? new Response(r.text, { status: r.status, headers: { "content-type": "application/json" } }) : new Response("{}", { status: 200 }); };
const LITTLE = new Set(("a an the of in on at to for from by with and or but that which who whom whose than as is are was were be been being it its their they this these those there into over under after before during while when where also both either neither nor not no none never without cannot " +
  "may might could can would should must suggest suggests suggested appear appears seem seems possibly possible potential potentially likely unlikely unclear unknown whether if although though however whereas despite except unless only just even rather instead versus compared comparison " +
  "all most many much some few fewer several any each every more less least higher lower greater smaller significant significantly non-significant rats rat mice mouse animals animal cells vitro vivo humans human people patients participants volunteers adults placebo controls " +
  "did does do has have had will limited preliminary mixed inconsistent inconclusive claimed reported believed thought examined investigated assessed evaluated aimed remains remain case cases pilot open-label survey observational").split(" "));
const shape = words => words.filter(w => /[A-Za-z0-9]/.test(w)).map(w => { const core = w.toLowerCase().replace(/[^a-z'-]/g, ""), tail = (w.match(/[,;:.)]+$/) || [""])[0], head = (w.match(/^[(]+/) || [""])[0]; return head + (/\d/.test(w) ? "#" : LITTLE.has(core) || /n't$/.test(core) ? core : "_") + tail; }).join(" ");
const abOf = p => summaries.get(p.doi ? "doi:" + p.doi : "pmid:" + p.pmid) || "";
const around = p => { const words = String(p.q).replace(/…/g, "").trim();
  for (const x of iaParts(abOf(p))) { const i = x.s.indexOf(words); if (i < 0) continue;
    return { before: shape(x.s.slice(0, i).trim().split(/\s+/)), shown: words.split(/\s+/).length, after: shape(x.s.slice(i + words.length).trim().split(/\s+/)), part: x.sec || "no label" }; }
  return { missing: true }; };
// why a paper got no words, in the rule's own terms (worked out here from the summary in memory; nothing of the summary is written)
const whyNone = (p, r) => { const ab = abOf(p); if (!ab) return "it has no summary in Europe PMC"; if (r.noq) return "the question is about the law, prices or drug tests";
  const parts = iaParts(ab), notes = []; iaPick(Object.assign({}, p, { ab }), r.groups, r.names, r.def, n => notes.push(n));
  return (notes.length ? [...new Set(notes)].join("; ") : "no sentence passed") + " (" + parts.length + " sentences" + (parts.some(x => x.sec) ? ", with labels" : "") + ")"; };

fs.mkdirSync(outDir, { recursive: true });
for (const f of files) {
  let req = null; try { req = JSON.parse(fs.readFileSync(path.join(dir, f), "utf8")); } catch (e) { console.log("instant trial: " + f + " is not JSON"); continue; }
  const items = [];
  for (const q of Array.isArray(req.questions) ? req.questions.slice(0, 60) : []) {
    asked = []; const body = JSON.stringify(Object.assign({ names: q.names, words: q.words }, Array.isArray(q.also) && q.also.length ? { also: q.also } : {}, q.def ? { def: 1 } : {})), rf = readFind(JSON.parse(body));
    const post = env => worker.fetch(new Request("https://pharmakon.world/api/find", { method: "POST", headers: { "content-type": "application/json", origin: "https://pharmakon.world" }, body }), env);
    const t0 = Date.now(); let reply = null, status = 0;
    try { const r = await post({ ASSETS: { fetch: async () => new Response("", { status: 404 }) }, FETCH: viaNet }); status = r.status; reply = await r.json(); } catch (e) { reply = { error: String(e && e.message).slice(0, 200) }; }
    const ms = Date.now() - t0;
    // the server's own computing time: the same request again, from memory (the middle one of five)
    const again = []; for (let i = 0; i < 5; i++) { const c0 = performance.now(); try { await (await post({ ASSETS: {}, FETCH: fromMemory })).json(); } catch (e) { /* not timed */ } again.push(performance.now() - c0); } again.sort((a, b) => a - b);
    const papers = ((reply && reply.papers) || []).map(p => Object.assign({ title: p.t, kind: p.kind, y: p.y, j: p.j, free: !!p.oa, id: p.doi || p.pmid }, p.q ? { shown: p.q, about: p.an === 1 ? "animals or cells" : p.an === 2 ? "its summary covers animals or cells too" : "", around: around(p) } : { shown: null, why: rf.error ? "" : whyNone(p, rf) }));
    items.push({ q: q.q, names: q.names, also: q.also || [], words: q.words, def: !!q.def, status, ms, server_ms: Math.round(again[2] * 10) / 10, held: !!(reply && reply.held), papers, searches: asked });
    await new Promise(r => setTimeout(r, 400));   // (one question after another, with a breath between: Europe PMC is a shared service)
    console.log("instant trial: " + JSON.stringify(q.q) + ": " + papers.length + " paper(s), " + papers.filter(p => p.shown).length + " with their own words, " + ms + " ms (the server's own share " + (Math.round(again[2] * 10) / 10) + " ms)");
  }
  const stamp = new Date().toISOString().replace(/[-:]/g, "").slice(0, 13), outFile = path.join(outDir, "trial-" + stamp + "-" + f.replace(/^instant-|\.json$/g, "") + ".json");
  fs.writeFileSync(outFile, JSON.stringify({ _note: "Made by scripts/auto/instant_trial.mjs: the papers' own words on a question (site/worker/_worker.js, /api/find) tried with the real index of papers on the editor's own questions. No model takes part. Nothing here is shown on the site. papers: in the order a reader would see them; shown: the paper's own words a reader would see under its title (null: none, with why); around: the shape of the rest of that sentence, little words only, every other word a '_' (a summary is never copied here); searches: what Europe PMC was asked, how long it took and what it gave; server_ms: the server's own computing time for the request.", made: new Date().toISOString(), why: String(req.why || "").slice(0, 300), v: 3, items }, null, 1));
  console.log("instant trial: written " + outFile);
}
