# Project 7 — Break It On Purpose

**Difficulty:** Medium
**Concepts used:** Observability, Concept 13 (cost), Concept 14

## Task (verbatim from course)
Build. Take your Project 3 loop. First, measure one beat: note roughly how
many tokens a run reads and writes, and multiply by your cadence to get a
monthly cost, which is Concept 13's math on your own loop. Then sabotage
it: point the prompt at a file that does not exist, or give it a success
condition it can never meet (with a limit set). Let it fire on schedule
and fail. Now diagnose the failure using only what the loop left behind,
meaning the log line and progress.md, without replaying the full run.

Done when three things are true. You can say what failed, and when, from
the spine alone. The loop left a clear "needs a human" note instead of
failing silently. And you know your loop's monthly cost at its current
cadence. If it failed silently, fix that before anything else by adding
the log line. You are rehearsing the overnight failure now, while it is
cheap and you are watching.

## Status
✅ Implemented & verified — real cost measurement, real sabotage, real fix.
See `run_log.md` for full evidence.

## Result

- **Cost:** ≈ **$0.17/month** at daily cadence (Sonnet 5 intro pricing,
  real measured file sizes for the input/output payload plus a documented
  agent-overhead estimate — see `run_log.md` Part 1).
- **Sabotage:** `sample_repo/` renamed to simulate a moved/deleted repo.
  Confirmed the pre-fix loop **failed silently** — `Path.rglob()` on a
  missing directory returns `[]`, not an error, so the loop reported
  "0 new TODOs" exactly as it would for a genuinely clean repo.
- **Fix:** added an explicit existence check that writes
  `NEEDS HUMAN: sample_repo not found at <path>` to the log and exits
  non-zero, before `progress.md` can be touched. Re-ran the same sabotage
  with the fix — the failure is now unmissable from the log alone.
- **Diagnosis:** after the fix, `run_log_entries.txt` alone answers what
  failed and when, with no need to replay the run.
