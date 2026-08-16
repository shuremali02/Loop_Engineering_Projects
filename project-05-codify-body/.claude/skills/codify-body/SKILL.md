---
name: codify-body
description: Codify a multi-candidate fix-loop body (draft fix + isolated worktree + reviewer verdict) into one shell command that fans candidates out in parallel with &/wait and has no memory of its own between runs.
---

# Codify the Body (engine, not a loop)

Use this when you have several independent fix candidates and want one
command to draft-and-review all of them without prompting step by step.

## Procedure

1. List candidates and, for each, the specific fix to apply and the
   specific test(s) that prove it (never grade a candidate against
   unrelated tests still-broken by other candidates — that produces
   false FAILs).
2. `for` loop over candidates; inside, launch each with `&`:
   - `git worktree add` an isolated checkout on its own throwaway branch
   - apply that candidate's fix
   - run `reviewer.py <worktree> <test target(s)>` — PASS/FAIL from
     the real exit code
   - remove the worktree + branch when done (grading is the only
     purpose, nothing here is meant to persist)
3. `wait` for all background jobs, then print one verdict table.
4. Run it twice. Confirm the base file is unchanged and there is no
   state file after either run — that's the proof this is an engine,
   not a loop.

## Files
- `sample_repo/utils.py` / `test_utils.py` — 3 independent bugs.
- `reviewer.py` — real exit-code reviewer, takes a worktree path plus
  specific test target(s).
- `run_fixes.sh` — the single codified command.
- `run_log.md` — two real runs, identical PASS table, plus the
  no-memory proof (base file still buggy after both runs).

## Turning this into a real loop
Name these two before calling it done:
1. **Heartbeat** — what fires `run_fixes.sh` without a human (Cron).
2. **Spine** — a `progress.md` each run reads/writes so later runs
   build on earlier ones instead of repeating identical work.

## This project's actual result
Run 1 and Run 2: `average: PASS`, `truncate: PASS`, `is_weekend: PASS`,
identical both times. `sample_repo/utils.py` on `main` still has all 3
original bugs after both runs — confirming zero memory between runs.
