#!/usr/bin/env python3
"""trial.py: writers tried on a real prompt of the lane (docs/AUTOMATION.md).

On 16 November 2026 the first real run of lane 3 wrote no answer: twice the writer's reply held no JSON in three tries, at
1,000 neurons a question. This file asks the same thing of several models and settings, once each, on the very items the
readers had kept for one question (data/auto/answers/au_<id>.json), and writes down for each: whether a draft in the
right form came back, how the reply ended, how many tokens it took, how long the model reasoned before it wrote, what it
cost, and the draft itself, so that the editor can read the writers side by side. Nothing is published by it.

    python3 -I scripts/auto/trial.py [au_w_0001]
"""
import sys, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import llm, lane

TRIALS = [("@cf/openai/gpt-oss-120b", 1400, None, "as the lane asked it on 16 November"),
          ("@cf/openai/gpt-oss-120b", 1400, {"reasoning_effort": "low"}, "asked to reason little"),
          ("@cf/openai/gpt-oss-120b", 3000, None, "with twice the room"),
          ("@cf/meta/llama-3.3-70b-instruct-fp8-fast", 900, None, ""),
          ("@cf/mistralai/mistral-small-3.1-24b-instruct", 900, None, "")]


def main(aid):
    a = json.load(open(ROOT / "data" / "auto" / "answers" / (aid + ".json"), encoding="utf-8"))
    sources = [s for s in a["sources"] if s.get("findings")]
    for s in sources: s["findings"] = s["findings"][:3]; s["limits"] = s["limits"][:1]            # the lane's next form: three findings and one limit of each source
    labels = {}
    for s in sources:
        if s.get("design"): labels["D" + s["tag"]] = s["design"]
        for x in s["findings"] + s["limits"]: labels[x["id"]] = x
    prompt = lane.writer_prompt(a["question"], sources, lane.examples(), "")
    out = {"_note": "Made by scripts/auto/trial.py: several writers on the same real prompt, once each. Drafts are for the editor's reading; none is published.", "answer": aid, "question": a["question"],
           "prompt_chars": len(prompt), "trials": []}
    for model, room, extra, note in TRIALS:
        before = llm.ledger()["neurons"]; row = {"model": model, "room": room, "extra": extra, "note": note}
        try:
            raw = llm.chat(model, [{"role": "system", "content": lane.WRITER_SYS}, {"role": "user", "content": prompt}], room, extra=extra)
            draft, why = lane.draft_of(llm.as_json(raw), labels)
            row.update({"ok": bool(draft), "why": why, "last": dict(llm.LAST), "neurons": round(llm.ledger()["neurons"] - before, 1)})
            if draft:
                row["draft"] = [{"part": p["part"], "text": p["text"], "uses": p["uses"]} for p in draft["parts"]]; row["complete"], row["missing"] = draft["complete"], draft["missing"]
                row["rules"] = [f"{p}: {w}" for p, w in lane.rules(draft["parts"], labels, [s["year"] for s in sources if s.get("year")])]
            else: row["starts"] = raw[:160]
        except (llm.Budget, llm.Unavailable) as e: row.update({"ok": False, "why": str(e)[:300]})
        out["trials"].append(row); print("trial:", model, room, extra or "", "a draft" if row.get("ok") else "NO draft (" + str(row.get("why"))[:80] + ")", row.get("last"), row.get("neurons"))
    json.dump(out, open(ROOT / "data" / "auto" / "exam" / "writer-trial.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "au_w_0001")
