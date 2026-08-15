---
name: morning-brief
description: Run a scheduled loop that scans a repo for open TODO comments, compares against progress.md's memory of what was already found, and appends only new findings — never repeating what a previous run already recorded.
---

# Morning Brief (scheduled loop, the spine)

Use this when a loop needs to run periodically (e.g. once a day) and each
run must build on the last run's memory, not start from a blank slate.

## Procedure

1. **Target:** scan `sample_repo/**/*.py` for lines containing `TODO`.
2. **Spine file:** `progress.md`. Before scanning, read its
   `## Recorded TODOs` section — this is the set of everything already
   known from past runs.
3. Compare the current scan against the recorded set.
   - Items already in `Recorded TODOs` → **not** reported as new.
   - Items not yet recorded → reported as new, and added to
     `Recorded TODOs` for next time.
4. Append a dated entry to `## Run history` in `progress.md` saying either
   "Found N new TODO(s): ..." or "No new TODOs found — same as last run."
   History entries are append-only; never delete a past entry.
5. Rewrite the `Recorded TODOs` section (cumulative) each run so the next
   run's comparison set is always up to date.

## Run command
```bash
python3 morning_brief.py
```

## Files
- `morning_brief.py` — the scan-compare-append script.
- `sample_repo/` — stand-in target repo with real `TODO` comments.
- `progress.md` — the spine (memory across runs).
- `run_log.md` — actual output from two real runs proving the spine works.

## This project's actual result
Run 1: 3 TODOs found, all new (progress.md didn't exist yet).
A 4th TODO was then added to `sample_repo/app.py` to simulate a day
passing. Run 2: 4 TODOs found total, but only **1** reported as new —
the other 3 were correctly recognized as already recorded. This proves
the loop has memory (Concept 12), not just a schedule (Concept 6).
