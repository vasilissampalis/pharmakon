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
    asked.length >= 2 && asked[0][0].startsWith('https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=(TITLE:"kanna" OR ABSTRACT:"kanna" OR TITLE:"sceletium tortuosum" OR ABSTRACT:"sceletium tortuosum") AND (TITLE:"psychoactive" OR ABSTRACT:"psychoactive" OR TITLE:"effects" OR ABSTRACT:"effects" OR TITLE:"effect" OR ABSTRACT:"effect") AND (PUB_TYPE:"review"') && asked[0][0].endsWith("&format=json&resultType=lite&pageSize=8") && asked[0][1].cf.cacheTtl === 86400, asked[0] && asked[0][0]);
  const n0 = asked.length;
  x = await post(envF, { names: ["heroin"], words: ["overdose"] }); ok("find: words about dying, overdose or amounts are not looked up", x.status === 200 && x.j.held === true && x.j.papers.length === 0 && asked.length === n0);
  x = await post(envF, { names: ["mdma"], words: ["pregnancy"] }); ok("find: nor words about pregnancy or children", x.j.held === true && asked.length === n0);
  x = await post(envF, { names: [], words: ["anxiety"] }); ok("find: without a drug's name nothing is looked up", x.status === 422 && asked.length === n0);
  x = await post(envF, { names: ['kanna" OR TITLE:"x', "a", "<b>"], words: ["two words", "x", "ok123"] }); ok("find: a name or word that is not plain is dropped; none left: nothing is looked up", x.status === 422 && asked.length === n0, JSON.stringify(x));
  x = await post(envF, { names: ["kanna"], words: [] }, "https://evil.example"); ok("find: another site's page may not ask", x.status === 403 && asked.length === n0);
  x = await post({ ASSETS: assets, FETCH: async () => { throw new Error("down"); } }, { names: ["kanna"], words: [] }); ok("find: when Europe PMC cannot be reached the reply is an empty list, not an error on the reader's page", x.status === 200 && x.j.ok && x.j.papers.length === 0);
  const g = await W.default.fetch(new Request("https://pharmakon.world/api/find"), envF); ok("find: only POST", g.status === 405);
  ok("find: nothing is written to the store", sF.m.size === 0); }
// (site 2.18) /api/answer: a written answer within seconds, from the papers' summaries, through the code's own checks. A stand-in for the model and
// one for Europe PMC: no network, no key.
{ const { IA, iaGate, iaParse, iaPaper } = await import("../../site/worker/_worker.js");
  const day = new Date().toISOString().slice(0, 10);
  const mk = () => { const m = new Map(), puts = []; return { m, puts, get: async (k, how) => { const v = m.get(k); return v == null ? null : how === "json" ? JSON.parse(v) : v; }, put: async (k, v, o) => { m.set(k, v); puts.push([k, o || null]); } }; };
  const AB1 = "<h4>Background</h4> Sceletium tortuosum, known as kanna, has a long history of traditional use in southern Africa. This review brings together the laboratory and clinical work on its alkaloids. In two small trials in healthy adults, an extract of the plant reduced anxiety-related activity in the amygdala. The evidence in people is still limited, and larger controlled studies are needed before firm conclusions can be drawn.";
  const AB2 = "Sixteen healthy volunteers took part in a double-blind, placebo-controlled, cross-over study of a kanna extract. After a single 25 mg administration, the extract attenuated amygdala reactivity to fearful faces compared with placebo. Amygdala-hypothalamus coupling was also reduced. These results suggest that the extract may have anxiolytic potential, which should be examined in people with anxiety.";
  const AB3 = "The effects of a Sceletium tortuosum extract on stress were examined in rats. Animals received the extract before restraint. In rats, the extract decreased restraint stress-induced self-soothing behaviour and lowered corticosterone. The kanna extract also caused mild sedation at the highest amount tested. Whether anxiety is affected in the same way remains to be shown in further work on this preparation.";
  const RESULTS = [{ title: "Kanna and anxiety: a review.", authorString: "Alpha A, Beta B.", journalTitle: "Journal of Tests", pubYear: "2021", doi: "10.1234/kanna.2021.1", pmid: "111", isOpenAccess: "Y", pubType: "review; journal article", abstractText: AB1 },
    { title: "A trial of a kanna extract in sixteen volunteers", authorString: "Gamma C.", journalTitle: "Trials Today", pubYear: "2013", pmid: "222", isOpenAccess: "N", pubType: "randomized controlled trial; journal article", abstractText: AB2 },
    { title: "Kanna extract and stress in rats", authorString: "Delta D.", journalTitle: "Animal Work", pubYear: "2011", pmid: "333", isOpenAccess: "N", pubType: "journal article", abstractText: AB3 },
    { title: "A paper with no summary on kanna", authorString: "Eps E.", journalTitle: "Short Notes", pubYear: "2019", pmid: "444", pubType: "journal article", abstractText: "" }];
  const asked = [], epmc = (results) => async url => { asked.push(decodeURIComponent(String(url))); return new Response(JSON.stringify({ resultList: { result: results || RESULTS } }), { status: 200, headers: { "content-type": "application/json" } }); };
  const model = reply => ({ calls: [], run: async function (name, input) { this.calls.push([name, input]); const r = typeof reply === "function" ? reply(name, input, this.calls.length) : reply; if (r instanceof Error) throw r; return r; } });
  const post = async (env, body, origin) => { const h = { "content-type": "application/json" }; if (origin !== null) h.origin = origin || "https://pharmakon.world";
    const r = await worker.fetch(new Request("https://pharmakon.world/api/answer", { method: "POST", headers: h, body: JSON.stringify(body) }), env); let j = null; try { j = await r.clone().json(); } catch (e) {} return { status: r.status, j }; };
  const Q = { q: "does kanna help with anxiety", names: ["kanna", "sceletium tortuosum"], words: ["anxiety"] };
  const GOOD = { enough: true, findings: [
    { n: 1, quote: "an extract of the plant reduced anxiety-related activity in the amygdala", text: "A 2021 review says that in two small trials in healthy adults a kanna extract reduced anxiety-related activity in a part of the brain." },
    { n: 2, quote: "the extract attenuated amygdala reactivity to fearful faces compared with placebo", text: "A 2013 trial in sixteen healthy volunteers found less reactivity to fearful faces in a brain area tied to anxiety after the extract than after placebo." },
    { n: 3, quote: "Whether anxiety is affected in the same way remains to be shown", text: "A 2011 study in rats found less stress behaviour, and says it remains to be shown whether anxiety is affected in the same way." }] };
  const P = RESULTS.map(iaPaper).filter(Boolean);
  ok("answer: a paper counts only with a summary long enough to say something; its summary is plain text", P.length === 3 && !/<h4>/.test(P[0].ab) && P[0].kind === "Review" && P[1].kind === "Trial" && P[2].kind === "Study");
  // --- the gates, one by one
  const g = (f, words) => iaGate(f, P, words === undefined ? ["anxiety"] : words);
  ok("gate: a finding whose quoted words stand in its paper's summary, that names its kind of paper and year, passes", !!g(GOOD.findings[0]) && !!g(GOOD.findings[1]) && !!g(GOOD.findings[2]), JSON.stringify(GOOD.findings.map(f => !!g(f))));
  const l0 = g(GOOD.findings[0]); ok("gate: what passes carries its paper: kind, year, journal and link", l0 && l0.kind === "Review" && l0.y === "2021" && l0.j === "Journal of Tests" && l0.doi === "10.1234/kanna.2021.1" && l0.n === 1 && /\.$/.test(l0.t), JSON.stringify(l0));
  const bad = (name, f, words) => ok("gate refuses: " + name, g(f, words) === null, JSON.stringify(g(f, words)));
  bad("quoted words that are not in the summary", { n: 1, quote: "kanna reliably removes anxiety in all adults who take it", text: "A 2021 review says a kanna extract reduced anxiety-related activity in a part of the brain." });
  bad("quoted words from another paper's summary", { n: 1, quote: "the extract attenuated amygdala reactivity to fearful faces compared with placebo", text: "A 2021 review says a kanna extract reduced anxiety-related activity in a part of the brain." });
  bad("a paper that was not given", { n: 7, quote: GOOD.findings[0].quote, text: GOOD.findings[0].text });
  bad("the wrong kind of paper (a review called a trial)", { n: 1, quote: GOOD.findings[0].quote, text: "A 2021 trial found that a kanna extract reduced anxiety-related activity in a part of the brain." });
  bad("another year than the paper's", { n: 1, quote: GOOD.findings[0].quote, text: "A 2019 review says a kanna extract reduced anxiety-related activity in a part of the brain." });
  bad("a number the summary does not hold", { n: 2, quote: GOOD.findings[1].quote, text: "A 2013 trial in 40 healthy volunteers found less reactivity to fearful faces tied to anxiety after the extract." });
  ok("gate: a number the summary writes as a word may be written as a figure (sixteen, 16)", !!g({ n: 2, quote: GOOD.findings[1].quote, text: "A 2013 trial in 16 healthy volunteers found less reactivity to fearful faces tied to anxiety after the extract than after placebo." }));
  bad("an amount", { n: 2, quote: GOOD.findings[1].quote, text: "A 2013 trial found less reactivity to fearful faces tied to anxiety after 25 mg of the extract." });
  bad("a dose in words", { n: 2, quote: GOOD.findings[1].quote, text: "A 2013 trial found less reactivity to fearful faces tied to anxiety after a single dose of the extract." });
  bad("advice", { n: 1, quote: GOOD.findings[0].quote, text: "A 2021 review says kanna reduced anxiety-related activity, so people with anxiety should try it." });
  bad("a promise of safety", { n: 1, quote: GOOD.findings[0].quote, text: "A 2021 review says kanna is safe and reduced anxiety-related activity in a part of the brain." });
  bad("speaking to the reader", { n: 1, quote: GOOD.findings[0].quote, text: "A 2021 review says kanna may reduce your anxiety-related activity in a part of the brain." });
  bad("a word surer than the summary's own (“proves”)", { n: 1, quote: GOOD.findings[0].quote, text: "A 2021 review proves that a kanna extract reduced anxiety-related activity in a part of the brain." });
  bad("a word wider than the summary's own (“all”)", { n: 1, quote: GOOD.findings[0].quote, text: "A 2021 review says a kanna extract reduced anxiety-related activity in all adults in the trials." });
  bad("“treats”, where the summary does not say so", { n: 1, quote: GOOD.findings[0].quote, text: "A 2021 review says a kanna extract treats anxiety-related activity in a part of the brain." });
  bad("a summary about rats, told as if about people", { n: 3, quote: "the extract decreased restraint stress-induced self-soothing behaviour", text: "A 2011 study found that the extract decreased stress behaviour, which bears on anxiety." });
  bad("a finding that does not bear on the question", { n: 3, quote: "The kanna extract also caused mild sedation", text: "A 2011 study in rats found that the kanna extract caused mild sedation." });
  ok("gate: the same finding passes when the question has no key words (“what is kanna”)", !!g({ n: 3, quote: "The kanna extract also caused mild sedation", text: "A 2011 study in rats found that the kanna extract caused mild sedation." }, []));
  bad("a way of taking compared with another", { n: 2, quote: GOOD.findings[1].quote, text: "A 2013 trial found less anxiety-tied reactivity, and says the extract acts faster when smoked than when swallowed." });
  bad("making an effect stronger", { n: 2, quote: GOOD.findings[1].quote, text: "A 2013 trial found less anxiety-tied reactivity, an effect the review says is stronger with alcohol." });
  bad("a question about dying, told through a finding", { n: 1, quote: GOOD.findings[0].quote, text: "A 2021 review says a kanna extract reduced anxiety-related activity and reports no deaths." });
  bad("a sentence that is too long", { n: 1, quote: GOOD.findings[0].quote, text: "A 2021 review says " + "that in small trials ".repeat(9) + "a kanna extract reduced anxiety-related activity." });
  bad("markup or a link", { n: 1, quote: GOOD.findings[0].quote, text: "A 2021 review says <b>kanna</b> reduced anxiety-related activity, see https://x.example now." });
  ok("the model's reply is read whether it comes as words or already parsed, and words around the JSON are left out", iaParse({ response: GOOD }).findings.length === 3 && iaParse({ response: "Here you go:\n" + JSON.stringify(GOOD) + "\nHope it helps" }).findings.length === 3 && iaParse({ response: "no json here" }) === null && iaParse({ response: { enough: true } }) === null);
  // --- the endpoint
  { const s = mk(), ai = model({ response: GOOD, usage: { prompt_tokens: 2000, completion_tokens: 220 } }), env = { ASSETS: assets, QUESTIONS: s, AI: ai, FETCH: epmc() };
    let x = await call(env, "GET"); ok("answer: with the model bound the page learns it can ask for a quick answer", x.j.quick === true && x.j.auto === true);
    x = await call({ ASSETS: assets, QUESTIONS: mk() }, "GET"); ok("answer: without the model it cannot", x.j.quick === false);
    x = await post({ ASSETS: assets, QUESTIONS: mk(), FETCH: epmc() }, Q); ok("answer: without the model nothing is written, and that is a state, not an error", x.status === 200 && x.j.ok === true && x.j.off === true);
    x = await post(env, Q, null); ok("answer: a request that does not say it comes from this site's own page is refused", x.status === 403 && ai.calls.length === 0);
    x = await post(env, Q, "https://evil.example"); ok("answer: another site's page is refused", x.status === 403 && ai.calls.length === 0);
    x = await post(env, { q: "can kanna kill you", names: ["kanna"], words: ["kill"] }); ok("answer: a question about dying is not answered here (it waits for a person), and no model is asked", x.j.held === true && ai.calls.length === 0);
    x = await post(env, { q: "is kanna legal in greece", names: ["kanna"], words: ["greece"] }); ok("answer: a question about the law is not one for research summaries; no model is asked", x.j.none === true && ai.calls.length === 0);
    x = await post(env, { q: "hi", names: ["kanna"], words: [] }); ok("answer: the same refusals as for a sent question (too short)", x.status === 422);
    x = await post(env, { q: "does it help with anxiety", names: [], words: ["anxiety"] }); ok("answer: no drug named, nothing looked up", x.status === 422);
    asked.length = 0; x = await post(env, Q);
    const L = (x.j.answer || {}).lines || [];
    ok("answer: one to three sentences, each with its paper's own words, kind, year and link", x.status === 200 && x.j.ok === true && L.length === 3 && L[0].t === GOOD.findings[0].text && L[0].quote === GOOD.findings[0].quote && L[0].kind === "Review" && L[0].y === "2021" && L[0].doi === "10.1234/kanna.2021.1" && L[1].kind === "Trial" && L[1].pmid === "222" && L[2].kind === "Study", JSON.stringify(x.j).slice(0, 400));
    const [name, input] = ai.calls[0] || [], sys = input ? input.messages[0].content : "", usr = input ? input.messages[1].content : "";
    ok("answer: one call to the writer, with the question, the summaries with their kind and year, room for a short reply, and the form asked for", ai.calls.length === 1 && name === IA.writer && /QUESTION: does kanna help with anxiety/.test(usr) && /\[1\] \(review, 2021, Journal of Tests\) Kanna and anxiety: a review/.test(usr) && /\[2\] \(trial, 2013, Trials Today\)/.test(usr) && !/<h4>/.test(usr) && !/no summary/.test(usr) && input.max_tokens === IA.room && input.temperature === 0 && input.response_format.type === "json_schema" && /Use only the summaries/.test(sys), usr.slice(0, 300));
    ok("answer: Europe PMC is asked for the summaries by the drug's names and key words, never by the sentence", asked.length >= 2 && asked.every(u => /resultType=core/.test(u) && u.startsWith("https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=(TITLE:\"kanna\"")) && !asked.some(u => /does kanna help/.test(u)), asked[0]);
    const ik = [...s.m.keys()].find(k => k.startsWith("ia:")), rec = ik ? JSON.parse(s.m.get(ik)) : {}, cnt = JSON.parse(s.m.get("ian:" + day) || "{}");
    ok("answer: what is kept is the drug's names, the key words, the sentences with their papers, the model and the time; never the reader's sentence; for 30 days", /^ia:[0-9a-f]{20}$/.test(ik || "") && Object.keys(rec).sort().join() === "at,lines,model,names,v,words" && rec.names.join() === "kanna,sceletium tortuosum" && rec.words.join() === "anxiety" && rec.lines.length === 3 && rec.model === IA.writer && !/does kanna help/.test(JSON.stringify([...s.m.entries()])) && s.puts.some(([k, o]) => k === ik && o && o.expirationTtl === 30 * 86400), JSON.stringify(rec).slice(0, 200));
    ok("answer: the day's count holds the neurons it cost (by the service's own count of tokens) and one answer", cnt.a === 1 && Math.abs(cnt.n - (2000 * IA.price[0] / 1e6 + 220 * IA.price[1] / 1e6)) < 0.2, JSON.stringify(cnt));
    x = await post(env, Q); ok("answer: the same question again is given from the store; no model is asked twice", x.j.again === true && x.j.answer.lines.length === 3 && ai.calls.length === 1);
    x = await post(env, { q: "Does kanna help with anxiety", names: Q.names, words: Q.words }); ok("answer: and in other capitals it is the same question", x.j.again === true && ai.calls.length === 1); }
  { const s = mk(), ai = model({ response: { enough: true, findings: [{ n: 1, quote: GOOD.findings[0].quote, text: "A 2021 review proves that kanna cures anxiety in all adults, so you should try it." }, { n: 2, quote: "words that are nowhere in the summary at all", text: "A 2013 trial found less reactivity to fearful faces tied to anxiety after the extract." }] } }), env = { ASSETS: assets, QUESTIONS: s, AI: ai, FETCH: epmc() };
    let x = await post(env, Q); const rec = JSON.parse(s.m.get([...s.m.keys()].find(k => k.startsWith("ia:"))));
    ok("answer: when no sentence passes the checks nothing is shown, and that is kept too, so the model is not asked again for it", x.j.none === true && x.j.why === "nothing passed the checks" && !x.j.answer && rec.lines.length === 0 && rec.why === "nothing passed the checks" && (await post(env, Q)).j.again === true && ai.calls.length === 1, JSON.stringify(x.j));
    ok("answer: what the checks refused is kept beside it with the reason, for the editors, and never given to the page", rec.drop.length === 2 && /^A 2021 review proves/.test(rec.drop[0].t) && /^a word the summary does not have \(proves\)$|^advice/.test(rec.drop[0].why) && rec.drop[1].why === "the quoted words are not in the paper's summary" && !/drop|proves/.test(JSON.stringify(x.j)), JSON.stringify(rec.drop)); }
  { const s = mk(), ai = model({ response: { enough: false, findings: [] } }), env = { ASSETS: assets, QUESTIONS: s, AI: ai, FETCH: epmc() };
    const x = await post(env, Q); ok("answer: when the model says the summaries do not bear on the question, nothing is shown", x.j.none === true && x.j.why === "the summaries do not bear on the question"); }
  { const s = mk(), ai = model((name, input, k) => (k === 1 ? new Error("JSON Mode couldn't be met") : { response: "Sure. " + JSON.stringify({ enough: true, findings: [GOOD.findings[1], GOOD.findings[1]] }) })), env = { ASSETS: assets, QUESTIONS: s, AI: ai, FETCH: epmc() };
    const x = await post(env, Q); ok("answer: when the service cannot keep to the form, it is asked once more in plain words; a paper is used once", x.j.answer && x.j.answer.lines.length === 1 && ai.calls.length === 2 && !ai.calls[1][1].response_format, JSON.stringify(x.j).slice(0, 200)); }
  { const s = mk(), ai = model(new Error("4006: you have used up your daily free allocation of 10,000 neurons")), env = { ASSETS: assets, QUESTIONS: s, AI: ai, FETCH: epmc() };
    const x = await post(env, Q); ok("answer: when the account's free day is used up, the page is told so and nothing is asked again", x.j.full === true && ai.calls.length === 1 && ![...s.m.keys()].some(k => k.startsWith("ia:"))); }
  { const s = mk(), ai = model({ response: GOOD }), env = { ASSETS: assets, QUESTIONS: s, AI: ai, FETCH: epmc() };
    s.m.set("ian:" + day, JSON.stringify({ n: IA.neurons - 100, a: 3 })); let x = await post(env, Q); ok("answer: it stops by itself at its own share of the day's free allowance", x.j.full === true && ai.calls.length === 0);
    s.m.set("ian:" + day, JSON.stringify({ n: 10, a: IA.answers })); x = await post(env, Q); ok("answer: and at its number of new answers a day", x.j.full === true && ai.calls.length === 0); }
  { const s = mk(), ai = model({ response: GOOD }), env = { ASSETS: assets, QUESTIONS: s, AI: ai, FETCH: epmc([RESULTS[3]]) };
    const x = await post(env, Q); ok("answer: with no summary to read, no model is asked", x.j.none === true && x.j.why === "no summaries found" && ai.calls.length === 0); }
  { const s = mk(), ai = model({ response: GOOD }), env = { ASSETS: assets, QUESTIONS: s, AI: ai, FETCH: async () => { throw new Error("down"); } };
    const x = await post(env, Q); ok("answer: Europe PMC not reachable is not an error for the reader", x.status === 200 && x.j.none === true && ai.calls.length === 0);
    const g2 = await worker.fetch(new Request("https://pharmakon.world/api/answer"), env); ok("answer: only POST", g2.status === 405); }
}
console.log(fail ? fail + " of " + (pass + fail) + " checks failed" : "All " + pass + " checks passed"); process.exit(fail ? 1 : 0);
