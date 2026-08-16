# Project 3 — Morning Brief

**Difficulty:** Medium
**Concepts used:** Concept 6 (unattended schedule), Concept 12 (the spine)

## Task (verbatim from course)
Build. Make a scheduled loop that runs once, reads a progress.md, gathers
something simple from the repo (open TODO comments, or the last day's
commits), writes a short summary, and updates progress.md with what it
found and the date.

Done when you run it twice and the second run clearly builds on the first,
meaning it does not repeat what it already recorded. That proves your
spine works. If the second run starts from nothing, your loop has no
memory yet.

## How this was implemented
- `sample_repo/` — stand-in target repo with `app.py` and `utils.py`,
  containing real `TODO` comments to scan (this project's "code TODOs"
  choice, over "last day's commits", since this folder isn't a git repo).
- `morning_brief.py` — scans `sample_repo/**/*.py` for lines with `TODO`,
  reads `progress.md`'s "Recorded TODOs" section for what's already known,
  reports/appends only the *new* ones, and rewrites the cumulative list.
- `progress.md` — the spine. Has a "Recorded TODOs" section (cumulative,
  used for dedup) and a "Run history" section (append-only log of what
  each run found).
- `run_log.md` — proof of two real runs: Run 1 found 3 TODOs (all new,
  `progress.md` didn't exist yet). Then 1 new TODO was added to
  `sample_repo/app.py` to simulate a day passing. Run 2 found 4 TODOs
  total but reported **only the 1 new one** — the spine worked.

## Status
Implemented and verified. See `run_log.md` for the two real runs proving
`progress.md` carries memory across runs (Concept 12).
