# The editor's next steps for the machine lane (a working note, kept in the repository so that it survives a reset)

Written 17 November 2026, 05:00 UTC, by the AI co-editor for itself. Not a decision of the senior author; nothing here
lets anything out. The state it starts from is the two newest entries of `docs/STATUS.md`.

Rules that stand: nothing new is shown (`hold_new` true, `amounts` false, the lane's clock paused, `show_from_lane` 9)
until a whole batch on questions the lane has never seen reads clean. Requests go one after the other, never two at
once. Commit and push after every step. `mkdir -p data/auto/requests` before writing a request.

## After 08:00 UTC, 17 November (Google's day is new)

1. **Lessons and training.** `git pull`; `python3 -I scripts/auto/teach.py show`; read
   `data/auto/own/teach/_last-run.txt` (also on the side branch: `git fetch origin lessons-wip` and
   `git show FETCH_HEAD:data/auto/own/teach/_last-run.txt`). When no Lessons run is going and there are about 800
   lessons or more, ask for the first training run, to prove the whole path on GitHub's machines:
   `data/auto/requests/train-0001.json` = `{"from": "lytang/MiniCheck-RoBERTa-Large", "as": "pharmakon-check-1", "top": 4, "epochs": 2, "minutes": 80}`.
   Adopt its model only by the rule (`own.better`; `workshop.py pick`).
2. **The strong reader's exam, an answer at a time**:
   `exam-00NN.json` = `{"models": ["gemini:gemini-4-hydrogen"], "exam": "lane", "how": ["together"], "keep": 9}`
   (about seven calls; nine are kept for the lane). Compare with the editor's verdicts. Gemini 3.8 Flash the same way
   only if Hydrogen answered within its time (3.8 timed out three times at 80 seconds; it has 170 now).
3. **A trial on questions about amounts the lane has never seen, with team F** (Gemini 3.5 Flash Lite reads: no neurons):
   `lane-00NN.json` = `{"team": "team F", "trial": [
   {"id": "t_lsd_studies", "q": "What amounts of LSD have studies given to people?", "drugs": ["lsd"], "ways": ["lsd dose in studies"]},
   {"id": "t_methadone_label", "q": "What daily amount of methadone does the medicine's label state for treatment?", "drugs": ["methadone-buprenorphine"], "ways": ["methadone dose on the label"]},
   {"id": "t_dmt_studies", "q": "What amounts of DMT have studies given to people?", "drugs": ["dmt-ayahuasca"], "ways": ["dmt dose in studies"]}]}`.
   Read with `python3 -I scripts/editor/read_auto.py --trial`; judge with `python3 -I scripts/editor/label_rows.py show --trial` and `add FILE --trial`.
4. **One ordinary question with Hydrogen as the further reader**, only if Groq's gpt-oss-120b or Cloudflare has room
   (8,279 of 9,000 neurons were used at 02:13 UTC): `{"ids": ["w_0041"], "max": 1}`. Read it with
   `read_auto.py --ids au_w_0041 --all`; judge every sentence, kept or not, with `label_auto.py`.
5. Whatever is wrong: a rule with a test in `scripts/auto/lane.py`, the lane's number up by one, and the run again.
6. Tell the senior author briefly and plainly what was written, what is shown, what is held and why.

## After 00:00 UTC, 18 November (Cloudflare's day is new)

- The rest of ten trial questions about amounts (same form): THC in studies (`cannabis`); the buprenorphine label
  (`methadone-buprenorphine`); the esketamine label for depression (`ketamine`); the diazepam label for anxiety in
  adults (`benzodiazepines`); the dexamfetamine label for adults (`amphetamine`); "How many drinks a day do US health
  bodies call moderate drinking?" (`alcohol`); "How much caffeine at one time do health bodies say raises no safety
  concern?" (`caffeine`).
- The listed questions about amounts that no late lane has written: `w_0043` (MDMA in studies), `w_0045` (ketamine for
  depression), `w_0044` (psilocybin, last written by lane 12).
- The other two ordinary questions: `w_0001`, `w_0002`.
- If ten unseen questions about amounts read clean: `amounts` true, `hold_new` `{"answer": true, "amounts": false}`,
  release what was read (`scripts/editor/release_auto.py`), a deploy request, and `deployed.json` checked. If not: the
  faults get their rules, and another ten unseen questions.

## Open with the senior author (asked before; no answer yet)

- Whether Google's free tier may be used at all ("no Google" switches it off): its terms let Google use what is sent
  to improve its products; we send our own sentences and passages of public sources, never a visitor's words.
