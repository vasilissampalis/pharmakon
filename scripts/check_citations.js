// Every author–year citation written inside prose (debate boxes, statements) must resolve to a reference record,
// using the same APA 7 labels the site renders (app.core.js), or it would appear as dead text.
// Usage: node scripts/check_citations.js   (exit code 1 if any citation does not resolve)
const fs = require("fs"), path = require("path");
const ROOT = path.resolve(__dirname, "..");
const REFS = fs.readdirSync(path.join(ROOT, "data/references")).filter(f => f.endsWith(".json")).flatMap(f => JSON.parse(fs.readFileSync(path.join(ROOT, "data/references", f), "utf8")));
const STUDY_CARDS = {}; const CLAIMS = [];
eval(fs.readFileSync(path.join(ROOT, "site/src/app.core.js"), "utf8") + "\nglobalThis.inTextLabel = inTextLabel;");
const labels = new Set(REFS.map(r => inTextLabel(r, REFS)));
const claims = fs.readdirSync(path.join(ROOT, "data/claims")).filter(f => f.endsWith(".json")).flatMap(f => JSON.parse(fs.readFileSync(path.join(ROOT, "data/claims", f), "utf8")));
let bad = 0;
for (const c of claims) {
  const texts = [];
  if (c.debate) for (const [k, v] of Object.entries(c.debate)) if (typeof v === "string") texts.push(["debate." + k, v]);
  for (const [field, t] of texts) {
    for (const m of t.matchAll(/\(([^()]*?\d{4}[a-z]?)\)/g)) {
      for (const part of m[1].split(";").map(s => s.trim())) {
        if (!/^[A-Z][^,]*(, [^,]+)*, \d{4}[a-z]?$/.test(part)) continue;            // not an author–year form
        if (/as described (by|in)|as reported (by|in)|as relayed (by|in)|cited (in|by)/.test(part)) continue;  // a study named inside the citation of the review that relays it
        // one author group with several years, APA 7 style: (Hughes & Stevens, 2010, 2012)
        const multi = part.match(/^(.*?), ((?:\d{4}[a-z]?, )+\d{4}[a-z]?)$/);
        if (multi && multi[2].includes(",")) {
          const miss = multi[2].split(", ").filter(y => !labels.has(multi[1] + ", " + y));
          if (miss.length) { console.log(`  UNRESOLVED ${c.id} ${field}: (${part})`); bad++; }
          continue;
        }
        if (!labels.has(part)) {
          // a study not in the reference list may be named inside a citation of the review that describes it
          if (/ as described by | as reported by | as relayed by | as cited by /.test(t.slice(m.index, m.index + m[0].length + 60))) continue;
          console.log(`  UNRESOLVED ${c.id} ${field}: (${part})`); bad++;
        }
      }
    }
  }
}
console.log(bad ? `${bad} unresolved in-text citations` : "all in-text citations in debate boxes resolve");
process.exit(bad ? 1 : 0);
