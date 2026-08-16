# Run log — Project 5 (codify-body)

`run_fixes.sh` codifies Project 4's fix-loop body into one command: for
3 candidate bugs in `sample_repo/utils.py`, it fans out into 3 parallel
git worktrees (`&`/`wait`), applies each candidate's fix, grades it with
`reviewer.py` (the same real-exit-code reviewer pattern as Project 4),
and prints one verdict table. No step-by-step prompting after launch.

## Base state (before either run)
`sample_repo/utils.py` has 3 real bugs: `average` uses `//` instead of
`/`, `truncate` is off-by-one, `is_weekend` checks the wrong day
indices. Confirmed failing (3 of 4 tests) before any run.

## Run 1
```
$ bash project-5-codify-body/run_fixes.sh
[codify-body] Fanning out 3 candidates in parallel...

[codify-body] Verdicts:
  - is_weekend: PASS
  - truncate: PASS
  - average: PASS
```

## Run 2 (immediately after, no changes made in between)
```
$ bash project-5-codify-body/run_fixes.sh
[codify-body] Fanning out 3 candidates in parallel...

[codify-body] Verdicts:
  - is_weekend: PASS
  - truncate: PASS
  - average: PASS
```

## Proving the interlude's warning: no memory between runs
After both runs:
- `git worktree list` shows no leftover `codify-*` worktrees — each run
  creates and destroys its own in `.worktrees/`.
- `sample_repo/utils.py` (the base file on `main`) is **still buggy** —
  `//`, `length - 1`, and `(6, 7)` are all unchanged. The script never
  writes back to the base; it only ever fixes a throwaway worktree copy,
  grades it, and discards it.
- There is no progress file, log, or any other state Run 2 could have
  read from Run 1. Run 2 re-derived the exact same 3 PASS verdicts from
  scratch, purely because the fix logic and the bugs are unchanged —
  not because it remembered Run 1 happened.

This is the engine-vs-loop distinction from the interlude: `run_fixes.sh`
is a reliable **engine** (one command, real isolation, real grading) but
it has **no spine**. It would need two things to become an actual loop:

1. **A heartbeat** — something that fires `run_fixes.sh` on its own
   (e.g. the Cron mechanism from Project 1, or a scheduled trigger like
   Project 3), instead of a human typing the command.
2. **A progress file** — a `progress.md` (Concept 12, same as Project 3)
   that each run reads before fanning out and writes after, so a second
   run could skip candidates already fixed/merged, or track which ones
   keep failing across multiple scheduled attempts, instead of re-doing
   identical work every single time.
