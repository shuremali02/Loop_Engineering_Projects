---
name: break-it-on-purpose
description: Cost-measures and deliberately sabotages the Project 3 morning-brief loop to rehearse an overnight silent failure, then fixes it with a "needs a human" log line — Concept 13 (cost) + observability.
---

# Break It On Purpose

## Task (verbatim from course)

**Build.** Take your Project 3 loop. First, measure one beat: note roughly
how many tokens a run reads and writes, and multiply by your cadence to get
a monthly cost, which is Concept 13's math on your own loop. Then sabotage
it: point the prompt at a file that does not exist, or give it a success
condition it can never meet (with a limit set). Let it fire on schedule
and fail. Now diagnose the failure using only what the loop left behind,
meaning the log line and `progress.md`, without replaying the full run.

**Done when** three things are true. You can say what failed, and when,
from the spine alone. The loop left a clear "needs a human" note instead
of failing silently. And you know your loop's monthly cost at its current
cadence. If it failed silently, fix that before anything else by adding
the log line. You are rehearsing the overnight failure now, while it is
cheap and you are watching.

## Procedure

1. Copy Project 3's loop logic into `loop_runner.py` (own `sample_repo`
   copy — never touch Project 3's already-verified files).
2. Run it once cold, once steady-state; measure real byte sizes of every
   file it reads/writes for one beat.
3. Convert to a token estimate (~4 chars/token, documented ballpark — no
   `count_tokens` endpoint available in this environment), add a
   conservative agent-firing overhead, price with Sonnet 5 intro pricing,
   multiply by cadence (daily) for a monthly figure.
4. Sabotage: rename `sample_repo` to simulate it going missing. Run the
   **pre-fix** loop against it and observe the real result — `Path.rglob()`
   on a missing dir returns `[]`, not an error, so the loop silently
   reports "0 new TODOs", indistinguishable from a genuinely clean repo.
5. Fix: add an explicit existence check at the top of the scan function
   that logs `NEEDS HUMAN: ...` and exits non-zero *before* `progress.md`
   can be written to — so a broken run can never look like a clean one.
6. Re-run the same sabotage with the fix; confirm the log now states the
   failure plainly. Restore `sample_repo`; confirm the healthy path still
   works (exit 0).

## Real run

Full numbers, real command output, and file diffs: `../../run_log.md`.

- Cost: ≈ $0.17/month at daily cadence.
- Pre-fix: confirmed real silent failure (log line `scanned=0 new=0`,
  identical to a clean-repo result).
- Post-fix: log line `NEEDS HUMAN: sample_repo not found at <path> —
  nothing was scanned`, exit code 1, `progress.md` left untouched.

## Result

All three "Done when" conditions met with real evidence: diagnosable from
the spine alone, clear "needs a human" note (not silent), and a known
monthly cost figure at current cadence.
