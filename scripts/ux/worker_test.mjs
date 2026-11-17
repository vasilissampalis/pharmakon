// worker_test.mjs: the question endpoint (site/worker/_worker.js) against a store kept in memory. usage: node scripts/ux/worker_test.mjs
import worker, { readQuestion } from "../../site/worker/_worker.js";
const kv = () => { const m = new Map(); return { m, get: async (k, how) => { const v = m.get(k); return v == null ? null : how === "json" ? JSON.parse(v) : v; }, put: async (k, v) => { m.set(k, v); } }; };
let pass = 0, fail = 0; const ok = (name, cond, extra) => { if (cond) pass++; else { fail++; console.log("FAIL", name, extra || ""); } };
const call = async (env, method, body, headers, path) => { const r = await worker.fetch(new Request("https://pharmakon.world" + (path || "/api/ask"), { method, headers: Object.assign({ "content-type": "application/json" }, headers || {}), body: body == null ? undefined : typeof body === "string" ? body : JSON.stringify(body) }), env); let j = null; try { j = await r.clone().json(); } catch (e) {} return { status: r.status, j, r }; };
const assets = { fetch: async () => new Response("the page", { status: 200 }) };
{ const env = { ASSETS: assets }; let x = await call(env, "GET"); ok("GET without the store answers 200 with ok false (a state, not an error)", x.status === 200 && x.j.ok === false);
  x = await call(env, "POST", { q: "can you overdose on lsd" }); ok("POST without the store is 503", x.status === 503); }
{ const s = kv(), env = { ASSETS: assets, QUESTIONS: s };
  let x = await call(env, "GET"); ok("GET with the store says ok", x.status === 200 && x.j.ok === true);
  x = await call(env, "POST", { q: "  Can you overdose   on LSD? ", d: "lsd", v: "2.4.0" }); ok("a question is kept", x.status === 200 && x.j.ok === true && !x.j.again);
  const keys = [...s.m.keys()], item = JSON.parse(s.m.get(keys.find(k => k.startsWith("q:"))));
  ok("what is kept: the words, the page, the version, the day, a count, and nothing else", item.q === "Can you overdose on LSD?" && item.d[0] === "lsd" && item.v === "2.4.0" && item.n === 1 && item.dn === 1 && Object.keys(item).sort().join() === "d,dn,first,last,n,q,v", JSON.stringify(item));
  x = await call(env, "POST", { q: "can you overdose on lsd?", d: "mdma" }); ok("the same question again is counted, not stored twice", x.j.again === true && [...s.m.keys()].filter(k => k.startsWith("q:")).length === 1);
  const again = JSON.parse(s.m.get(keys.find(k => k.startsWith("q:")))); ok("its count and pages grow", again.n === 2 && again.dn === 2 && again.d.join() === "lsd,mdma");
  { const writes = () => s.m.get("count:" + new Date().toISOString().slice(0, 10)); for (let i = 0; i < 30; i++) x = await call(env, "POST", { q: "Can you overdose on LSD?" });
    const many = JSON.parse(s.m.get(keys.find(k => k.startsWith("q:")))); ok("one question is counted at most 20 times a day, and the rest write nothing", x.status === 200 && x.j.again === true && many.n === 20 && many.dn === 20 && writes() === "20", JSON.stringify(many) + " " + writes());
    const old = Object.assign({}, many, { last: "2026-01-01" }); s.m.set(keys.find(k => k.startsWith("q:")), JSON.stringify(old)); x = await call(env, "POST", { q: "Can you overdose on LSD?" });
    const next = JSON.parse(s.m.get(keys.find(k => k.startsWith("q:")))); ok("on another day it counts again, from one", next.n === 21 && next.dn === 1 && next.last === new Date().toISOString().slice(0, 10), JSON.stringify(next)); }
  for (const [q, why] of [["hi", "too short"], ["cocaine", "too short"], ["see http://x.example for more", "no links"], ["mail me at someone@example.com please", "no links"], ["call me on +30 210 1234567 now", "no long numbers"], ["12345678 9", "too short"], ["<script>alert(1)</script> hello there", "no links"]]) {
    x = await call(env, "POST", { q }); ok("refused: " + q, x.status === 422 && x.j.error.startsWith(why.split(" ")[0] === "no" ? "no" : "too"), JSON.stringify(x.j)); }
  x = await call(env, "POST", "{not json"); ok("bad JSON is 400", x.status === 400);
  x = await call(env, "POST", { q: "x".repeat(3000) }); ok("a body that is too long is 413", x.status === 413);
  x = await call(env, "POST", { q: "is it safe to mix alcohol and ghb" }, { origin: "https://evil.example" }); ok("another site's page cannot send", x.status === 403);
  x = await call(env, "POST", { q: "is it safe to mix alcohol and ghb" }, { origin: "https://pharmakon.world" }); ok("this site's page can", x.status === 200);
  x = await call(env, "PUT", { q: "is it safe to mix alcohol and ghb" }); ok("other methods are 405", x.status === 405);
  x = await call(env, "GET", null, null, "/api/other"); ok("another /api address is 404", x.status === 404);
  x = await call(env, "GET", null, null, "/index.html"); ok("every other address is the site's own file", x.status === 200 && (await x.r.text()) === "the page");
  const long = await call(env, "POST", { q: "why " + "really ".repeat(60) + "does this happen" }); const stored = [...s.m.entries()].filter(([k]) => k.startsWith("q:")).map(([, v]) => JSON.parse(v)).find(v => v.q.startsWith("why really"));
  ok("a long question is cut at 200 characters", long.status === 200 && stored && stored.q.length <= 200);
  s.m.set("count:" + new Date().toISOString().slice(0, 10), "400"); x = await call(env, "POST", { q: "a brand new question about ketamine" }); ok("the daily cap holds for a new question", x.status === 429);
  x = await call(env, "POST", { q: "is it safe to mix alcohol and ghb" }); ok("and for one asked before", x.status === 429);
  ok("no key holds anything but questions and the day's count", [...s.m.keys()].every(k => /^(q:[0-9a-f]{20}|count:\d{4}-\d\d-\d\d)$/.test(k))); }
// an address with a slash at its end is the same address (the senior author's first check of the live site met "not found")
{ const s = kv(), env = { ASSETS: assets, QUESTIONS: s }; let x = await call(env, "GET", null, null, "/api/ask/"); ok("GET /api/ask/ (a slash at the end) answers as /api/ask", x.status === 200 && x.j.ok === true);
  x = await call(env, "POST", { q: "can you overdose on lsd" }, null, "/api/ask//"); ok("POST with slashes at the end keeps the question", x.status === 200 && x.j.ok === true); }
// the list's counts: only an item's number arrives
{ const s = kv(), env = { ASSETS: assets, QUESTIONS: s }, day = new Date().toISOString().slice(0, 10);
  let x = await call(env, "POST", { id: "w_0041" }, null, "/api/want"); ok("a count for a listed question is kept", x.status === 200 && x.j.ok === true);
  const rec = JSON.parse(s.m.get("w:w_0041")); ok("what is kept: a count, the day, and nothing else", rec.n === 1 && rec.dn === 1 && rec.last === day && Object.keys(rec).sort().join() === "dn,first,last,n", JSON.stringify(rec));
  x = await call(env, "POST", { id: "w_0041", q: "my own words about my own life" }, null, "/api/want"); const rec2 = JSON.parse(s.m.get("w:w_0041"));
  ok("words sent along are not kept", rec2.n === 2 && !JSON.stringify([...s.m.values()]).includes("my own words"), JSON.stringify(rec2));
  for (const bad of ["", "41", "w_", "W_0041", "w_0041; drop", "q:abc", "w_" + "a".repeat(60)]) { x = await call(env, "POST", { id: bad }, null, "/api/want"); ok("refused as a list number: " + JSON.stringify(bad), x.status === 422); }
  x = await call(env, "GET", null, null, "/api/want"); ok("GET /api/want is 405", x.status === 405);
  x = await call(env, "POST", { id: "w_0041" }, { origin: "https://evil.example" }, "/api/want"); ok("another site's page cannot count", x.status === 403);
  for (let i = 0; i < 80; i++) x = await call(env, "POST", { id: "w_0002" }, null, "/api/want");
  ok("one item is counted at most 60 times a day", JSON.parse(s.m.get("w:w_0002")).n === 60, s.m.get("w:w_0002"));
  s.m.set("count:" + day, "300"); x = await call(env, "POST", { id: "w_0003" }, null, "/api/want"); ok("counts stop at 300 a day and write nothing more", x.status === 200 && x.j.full === true && !s.m.has("w:w_0003"));
  x = await call(env, "POST", { q: "a question someone chose to send about ketamine" }); ok("a question someone sends is still taken after that", x.status === 200 && x.j.ok === true);
  x = await call({ ASSETS: assets }, "POST", { id: "w_0041" }, null, "/api/want"); ok("without the store a count is 503", x.status === 503);
  ok("the store's keys are questions, list numbers and the day's count", [...s.m.keys()].every(k => /^(q:[0-9a-f]{20}|w:w_[a-z0-9_]{1,40}|count:\d{4}-\d\d-\d\d)$/.test(k))); }
ok("readQuestion keeps Greek", readQuestion({ q: "είναι ασφαλές το αλκοόλ με κοκαΐνη" }).q.length > 10);
// (site 2.17) a question the page sent by itself: kept apart ("aq:"), for 180 days, counted like the others; it never crowds out one somebody chose to send
{ const puts = [], m = new Map(), s = { m, get: async (k, how) => { const v = m.get(k); return v == null ? null : how === "json" ? JSON.parse(v) : v; }, put: async (k, v, o) => { m.set(k, v); puts.push([k, o || null]); } };
  const env = { ASSETS: assets, QUESTIONS: s }, day = new Date().toISOString().slice(0, 10);
  let x = await call(env, "GET"); ok("the page learns from one GET that it can send, that research can be looked up, and that it may send by itself", x.j.ok === true && x.j.find === true && x.j.auto === true);
  x = await call({ ASSETS: assets }, "GET"); ok("without the store it may not send by itself (research can still be looked up)", x.j.ok === false && x.j.find === true && x.j.auto === false);
  x = await call(env, "POST", { q: "does kanna help with anxiety", d: "", v: "2.17.0", a: 1 }); const ak = [...m.keys()].find(k => k.startsWith("aq:")), rec = ak ? JSON.parse(m.get(ak)) : {};
  ok("a question the page sent by itself is kept apart, marked, with no key among the questions people chose to send", x.status === 200 && x.j.ok === true && /^aq:[0-9a-f]{20}$/.test(ak || "") && rec.a === 1 && rec.q === "does kanna help with anxiety" && rec.n === 1 && ![...m.keys()].some(k => k.startsWith("q:")), JSON.stringify([...m.keys()]));
  ok("it is kept for 180 days, not for ever", puts.some(([k, o]) => k === ak && o && o.expirationTtl === 180 * 86400), JSON.stringify(puts));
  x = await call(env, "POST", { q: "Does kanna help with anxiety", a: 1 }); ok("sent by itself again: counted, not stored twice", x.j.again === true && JSON.parse(m.get(ak)).n === 2 && [...m.keys()].filter(k => k.startsWith("aq:")).length === 1);
  x = await call(env, "POST", { q: "is kratom addictive at all" }); x = await call(env, "POST", { q: "is kratom addictive at all", a: 1 }); const qk = [...m.keys()].find(k => k.startsWith("q:"));
  ok("a question somebody already chose to send is counted there when the page sends it by itself", x.j.again === true && JSON.parse(m.get(qk)).n === 2 && [...m.keys()].filter(k => k.startsWith("aq:")).length === 1, JSON.stringify([...m.keys()]));
  x = await call(env, "POST", { q: "see http://x.example about kanna", a: 1 }); ok("the same refusals hold for it (a link)", x.status === 422);
  m.set("count:" + day, "250"); x = await call(env, "POST", { q: "does kanna change your sleep at night", a: 1 }); ok("questions sent by the page stop at 250 a day and write nothing more", x.status === 429 && [...m.keys()].filter(k => k.startsWith("aq:")).length === 1);
  x = await call(env, "POST", { q: "does kanna change your sleep at night" }); ok("a question somebody chooses to send is still taken after that", x.status === 200 && x.j.ok === true);
  ok("the store's keys: questions, questions the page sent by itself, and the day's count", [...m.keys()].every(k => /^(a?q:[0-9a-f]{20}|count:\d{4}-\d\d-\d\d)$/.test(k)), JSON.stringify([...m.keys()])); }
// (site 2.16) /api/find: published research on a drug, looked up at once in Europe PMC; only names and plain key words arrive, nothing is kept
{ const W = await import("../../site/worker/_worker.js"), asked = [];
  const reply = { resultList: { result: [{ title: "A review of <i>kanna</i>.", authorString: "A B.", journalTitle: "Molecules", pubYear: "2021", doi: "10.3390/molecules26092557", pmid: "1", isOpenAccess: "Y", pubType: "review; journal article" },
    { title: "A trial in people", pubYear: "2013", pmid: "22", pubType: "randomized controlled trial" }, { title: "short" }, { title: "No link to this paper at all", pubYear: "2020" }, { title: "A review of <i>kanna</i>.", doi: "10.3390/molecules26092557" }] } };
  const sF = kv(), envF = { ASSETS: assets, QUESTIONS: sF, FETCH: async (u, o) => { asked.push([decodeURIComponent(String(u)), o]); return new Response(JSON.stringify(reply), { status: 200 }); } };
  const post = async (env, body, origin) => { const r = await W.default.fetch(new Request("https://pharmakon.world/api/find", { method: "POST", headers: Object.assign({ "content-type": "application/json" }, origin ? { origin } : {}), body: JSON.stringify(body) }), env); return { status: r.status, j: await r.json() }; };
  let x = await post(envF, { names: ["Kanna", "Sceletium tortuosum"], words: ["psychoactive", "effects"] }, "https://pharmakon.world");
  ok("find: the papers come back with title, journal, year, kind, free or not and a link; one without a link, a title too short and a second copy are left out",
    x.status === 200 && x.j.ok && x.j.papers.length === 2 && x.j.papers[0].t === "A review of kanna" && x.j.papers[0].kind === "Review" && x.j.papers[0].oa === true && x.j.papers[0].doi === "10.3390/molecules26092557" && x.j.papers[1].kind === "Trial" && x.j.papers[1].pmid === "22" && x.j.papers[1].oa === false, JSON.stringify(x.j));
  ok("find: Europe PMC is asked for the names and the key words, in its own syntax, reviews first, and its reply may be kept for a day",
    asked.length >= 2 && asked[0][0].startsWith('https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=(TITLE:"kanna" OR ABSTRACT:"kanna" OR TITLE:"sceletium tortuosum" OR ABSTRACT:"sceletium tortuosum") AND (TITLE:"psychoactive" OR ABSTRACT:"psychoactive" OR TITLE:"effects" OR ABSTRACT:"effects") AND (PUB_TYPE:"review"') && asked[0][0].endsWith("&format=json&resultType=lite&pageSize=8") && asked[0][1].cf.cacheTtl === 86400, asked[0] && asked[0][0]);
  const n0 = asked.length;
  x = await post(envF, { names: ["heroin"], words: ["overdose"] }); ok("find: words about dying, overdose or amounts are not looked up", x.status === 200 && x.j.held === true && x.j.papers.length === 0 && asked.length === n0);
  x = await post(envF, { names: ["mdma"], words: ["pregnancy"] }); ok("find: nor words about pregnancy or children", x.j.held === true && asked.length === n0);
  x = await post(envF, { names: [], words: ["anxiety"] }); ok("find: without a drug's name nothing is looked up", x.status === 422 && asked.length === n0);
  x = await post(envF, { names: ['kanna" OR TITLE:"x', "a", "<b>"], words: ["two words", "x", "ok123"] }); ok("find: a name or word that is not plain is dropped; none left: nothing is looked up", x.status === 422 && asked.length === n0, JSON.stringify(x));
  x = await post(envF, { names: ["kanna"], words: [] }, "https://evil.example"); ok("find: another site's page may not ask", x.status === 403 && asked.length === n0);
  x = await post({ ASSETS: assets, FETCH: async () => { throw new Error("down"); } }, { names: ["kanna"], words: [] }); ok("find: when Europe PMC cannot be reached the reply is an empty list, not an error on the reader's page", x.status === 200 && x.j.ok && x.j.papers.length === 0);
  const g = await W.default.fetch(new Request("https://pharmakon.world/api/find"), envF); ok("find: only POST", g.status === 405);
  ok("find: nothing is written to the store", sF.m.size === 0); }
console.log(fail ? fail + " of " + (pass + fail) + " checks failed" : "All " + pass + " checks passed"); process.exit(fail ? 1 : 0);
