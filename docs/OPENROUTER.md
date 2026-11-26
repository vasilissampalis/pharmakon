# OpenRouter as a paid backup (prepared 26 November 2026; ON since the evening of 26 November 2026, on the senior author's word)

The senior author, 26 November 2026, 18:26: "keep Groq and Gemini on their existing free tiers and use OpenRouter as a paid
backup", with six conditions: every key unchanged; nothing live or deployed before he approves; a strict $10 monthly
OpenRouter limit with auto top-up disabled; every evidence and publication safeguard kept; any stronger model tested on our
exams before it writes a published answer; costs, configuration and rollback shown first. Decision 46 of `docs/AUTOMATION.md`.

## State (26 November 2026, evening)

He bought $10 of credit (invoiced $10.85, automatic top-up off), set the workspace's monthly budget to $10 and kept the key
unchanged; at 19:21 he wrote "deploy". On `main`: `paid`, `lane`, `credits_bought` and `even` on (`data/auto/lane/pay.json`).
The key's check (`data/auto/or-check.json`), the two exams (`data/auto/exam/model-openrouter-*.json`) and the writers' trial
(`data/auto/exam/writer-trial-openrouter-*.json`) were started in the same push. Claude Haiku 5.5 and GPT-6 Luna are examined
only: neither stands in a team until he names it.

## The first tests (26 November 2026, 17:36 to 18:04 UTC; `data/auto/or-check.json`, `data/auto/exam/model-openrouter-*.json`, `data/auto/exam/writer-trial-openrouter-*.json`)

- **The key.** The key the runs use ends as the dashboard's Default key (`e7c`), and so does its label: it is that key. The
  workspace's budget applies to it ($10 a month, from the 1st, nothing spent before the tests); the account holds $10 of
  credit; the free models' day is now 1,000 calls. The key's own limit is $100 (above the budget, so the budget is what
  binds), and the key expires on 15 May 2027. The dashboard's "never" was most likely because every earlier call was to a
  free model; the check settles which key it is either way.
- **Prices as OpenRouter lists them.** Llama 3.3 70B: only DeepInfra (fp8, $0.10/$0.32) is under our ceiling. gpt-oss-120b:
  eleven providers under the ceiling (most in fp4, the model's own format). Claude Haiku 5.5 and GPT-6 Luna: $0.10/$0.50.
- **As the checker, on the lane's own sentences (108 the editor judged; one verdict a sentence).** gpt-oss-120b at
  OpenRouter: caught 16 of 35 wrong, stopped 4 of 73 good (21.6 in 100 of what it lets through would be wrong). At Groq, on
  the cards exam, the same model caught 5 of 11 wrong: the model judges alike at both; it is weak alone, as the lane knew
  (it never decides alone: the code's gates and the further readers stand after it). Claude Haiku 5.5: caught 26 of 35,
  stopped 13 of 73 (13.0 in 100). GPT-6 Luna (37 of the 108 before the run's time ran out): caught 16 of 19, stopped 7 of 18.
  Haiku on the plain lines: caught 30 of 56, stopped 32 of 112; on the cards: caught 23 of 31, stopped 31 of 62. None reaches
  the bar for a checker trusted alone (2 in 100).
- **As the writer (three real prompts of the lane).** Llama 3.3 70B through OpenRouter (DeepInfra) wrote a draft in the
  right form for all three, at about $0.0003 a draft. Claude Haiku 5.5 and GPT-6 Luna ran out of room at 900 tokens (they
  reason first): tried again with room. Cloudflare's free day was used up, so the same model there could not be compared.
- **Cost of all of it:** $0.19 (523 calls).

## The second tests, and the choice (26 November 2026, 18:07 to 18:31 UTC; his words, 21:39: "Make the choice that absolutely has the best results", "The best and fastest results", "People don't like waiting at all and want outmost accuracy")

- **Asked as the lane asks its second reader (one answer's sentences in one call; `-lane-together.json`).** Claude Haiku 5.5:
  caught 22 of the 35 wrong sentences, stopped 9 of the 73 good. gpt-oss-120b: caught 16, stopped 6. GPT-6 Luna: the run's
  time ran out after 20 sentences (caught 5 of 6 wrong, stopped 4 of 14 good); finished in a later sitting.
- **One verdict a sentence, every exam finished.** GPT-6 Luna: the lane's sentences, caught 29 of 35 and stopped 18 of 73;
  the plain lines, caught 32 of 56 and stopped 26 of 112; the cards, caught 24 of 31 and stopped 28 of 62 (Haiku: 26 and 13,
  30 and 32, 23 and 31). Luna catches a little more, but it reasons before every verdict, so it is slower.
- **Writers with room (3,000 tokens).** Claude Haiku 5.5: drafts for two of three, long (2,000 to 2,600 tokens), one with a
  promise of safety the code refused. GPT-6 Luna: drafts for all three, one with a number not in its passage. Llama 3.3 70B
  (900 tokens): drafts for all three, short, no rule broken. The writer stays Llama.
- **The choice.** Claude Haiku 5.5 is asked first as the second reader in EVERY team, wherever it can be asked (`checker_first`
  in `data/auto/lane/models.json`; `lane.team`), and each team's own second reader after it, so that nothing stops where it
  cannot be asked (switched off, money spent, OpenRouter down). The second reader is the gate a model holds; Haiku held it
  best of all the models examined, asked the lane's way, and answers fast. A check costs about $0.0005; the system makes some
  sixty checks a day, so about $1 to $3 a month. Groq's free tokens that went to checking now go to writing and planning, so
  the free teams last longer each day. Team R: Llama 3.3 70B writes, Haiku checks, gpt-oss-120b after it.

## GPT-6 Luna asked the lane's way, finished (26 November 2026, late; `model-openrouter-openai-gpt-6-luna-lane-together.json`)

Caught 32 of the 35 wrong sentences and stopped 22 of the 73 good ones, in 21 calls. Beside the same exam:
Claude Haiku 5.5 caught 22 and stopped 9; gpt-oss-120b caught 16 and stopped 6. Of the sentences each lets through, the share
that is wrong: Luna about 6 in 100 (3 of 54), Haiku about 17 in 100 (13 of 77), gpt-oss-120b about 22 in 100 (19 of 86)
(editors' arithmetic). Luna reasons before every verdict, so each check takes longer, and it stops about 3 in 10 good
sentences (Haiku about 1 in 8), so more drafts are rewritten or dropped. Haiku stays the second reader asked first tonight;
whether Luna should take its place, or read after it for the answers where a wrong word can hurt most, is for the plan of
27 November (docs/EXPANSION-PLAN.md) and the senior author, after its speed is measured.

## The checker, decided on the timed exams (27 November 2026, 01:30 Athens; exam-0026, `*-lane-together-timed.json`)

A fresh sitting of each, the lane's way, with the seconds of every call: GPT-6 Luna caught 32 of 35 wrong and stopped 20 of 73
good, median 4.0 seconds a call; Claude Haiku 5.5 caught 24 and stopped 11, median 5.3 seconds; gpt-oss-120b caught 17 and
stopped 8, median 4.6 seconds. Luna's two sittings agree (32 caught both times). So Luna is both the most accurate gate and the
fastest, at the price of stopping more good sentences (about 1 in 4 against Haiku's 1 in 7), which means more drafts written
again. On his words ("the choice that absolutely has the best results", "the best and fastest results", "outmost accuracy"),
GPT-6 Luna is now the second reader asked first in every team (`checker_first`); Haiku stands after it in team R; each team's
own second reader after that.

## What changes (only in the background system that writes "New answers"; the website itself calls no model)

| File | Change |
|---|---|
| `scripts/auto/llm.py` | A model that costs money at OpenRouter is asked only while `openrouter.paid` is true AND `pay.json` names its price ceiling. The lane's teams may use it only while `openrouter.lane` is true (exams and trials may ask it before). Every request carries the ceiling (`provider.max_price`) and `data_collection: "deny"`. The real cost of each call (OpenRouter's `usage.cost`) is written in the ledger. Money as in Groq's design (decision 45): one pot a month (our stop: $9.50), a question a person sent first, the lane's own list within a day's share above a floor kept for visitors. A refusal for want of credit (HTTP 402) ends the budget at once. A team with no money left is never chosen. OpenRouter's free models: 45 calls a day, 900 once `credits_bought` is true. Tested: `or_selftest`. |
| `data/auto/lane/pay.json` | New section `openrouter`: `paid` false, `lane` false, `usd_a_month` 9.5, ceilings for four models. |
| `data/auto/lane/models.json` | Team R: team B (the best share of published answers since 20 November, 10 of 24) with OpenRouter in Groq's and Cloudflare's places. It stands after the teams of Groq's free plan and before the teams of Google's free models only, so it works when Groq's free day is used up. |
| `scripts/auto/exam_models.py`, `scripts/auto/trial.py` | An exam or a writers' trial may ask a paid model before any team may; its spending is counted as an exam's. Writers' trials can be asked for by request. |
| `data/auto/requests-prepared/` | Two exams and a writers' trial, ready; nothing runs until they are moved into `data/auto/requests/`. |

Unchanged: every gate of the lane (`lane.py`), Groq, Gemini, Cloudflare, every key, the website, the publishing.

## Models and ceilings (prices read on OpenRouter's model pages, 26 November 2026; $ per million tokens, in / out)

| Model | Role | Ceiling | Who serves it at or under the ceiling |
|---|---|---|---|
| `openai/gpt-oss-120b` | second reader and planner (team R) | 0.10 / 0.50 | Crusoe 0.05/0.25, Google Vertex 0.09/0.36, Baseten 0.10/0.50 (Groq itself 0.15/0.60 is above it) |
| `meta-llama/llama-3.3-70b-instruct` | writer (team R) | 0.12 / 0.35 | DeepInfra Turbo 0.10/0.32 (slow, about 18 tokens a second; a draft is short) |
| `anthropic/claude-haiku-5.5` | exam only | 0.10 / 0.50 | Anthropic, Bedrock, Vertex 0.10/0.50 |
| `openai/gpt-6-luna` | exam only | 0.10 / 0.50 | its exact OpenRouter id is checked before the exam |

## Expected costs

- Buying $10 of credit: OpenRouter adds 5.5% with a minimum of $0.80, so $10.80 is charged once. Credits may expire a year after purchase.
- Exams and the writers' trial: about $0.30 in all, once (at the ceilings).
- An answer tried by team R: about 30,000 tokens in and 5,000 out on the paid models, about $0.006 at the ceilings (the reader is Google's free model).
- A day: the lane's own list may spend at most the month's pot over its days (`even`: about $0.31, so at most about 50 extra tries a day), and less while the floor kept for visitors needs it; nothing unspent is carried to the next day. A question a person sent may spend from the pot at any hour.
- The money follows the credit (`follow_credit`, his word of 19:48 that it must last the whole month): the account's own balance, read at most once an hour, is spread over the days left in the month, less what is kept for people's questions; so whatever is left, of one purchase or many, lasts to the month's end.
- A month: never more than $9.50 by our code, $10 by the workspace's budget in OpenRouter, and never more than the credit bought (no automatic top-up). November (from the 26th): at most about $1.60 and the exams. December: up to $9.50, so the $10 bought lasts until about the last week of December; then OpenRouter refuses (402), team R stands aside, and the free teams go on as before. Expected: about $3 to $9.50 a month, depending on how often Groq's free day runs out (today it runs out every afternoon).

## Rollback

1. At once: `data/auto/lane/pay.json`, `"openrouter": {"paid": false, ...}` (one line, one commit). From the next run (at most five minutes) nothing is asked at OpenRouter for money and team R is never chosen; the free teams go on as before.
2. In OpenRouter (he): set the workspace's budget to $0 or the key's credit limit to 0, or turn the key off (that also stops OpenRouter's free models, which no team uses).
3. Whole: `git revert` of the merge commit puts the code back exactly as it was. Groq, Gemini and Cloudflare were never touched.

## The order of steps, each only on his word

1. He buys $10 of credit, sets the key's monthly credit limit to $10, and keeps automatic top-up off (`OpenRouter` steps below).
2. The editor merges this branch into `main` with both switches off and `credits_bought` true: the lane behaves as before.
3. With `paid` on and `lane` off, the exams and the writers' trial run (moved into `data/auto/requests/`). Nothing is published by them.
4. The editor reads every result and shows it to him: does gpt-oss-120b at OpenRouter's providers judge as at Groq; are the writer's drafts in the right form; how did the stronger models do.
5. Only on his word: `lane` on, and team R works as the backup. A stronger model enters a team only after it passed the exams, and only on his word.
