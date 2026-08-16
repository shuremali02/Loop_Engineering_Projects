---
name: fix-loop
description: Draft a fix for one real bug in an isolated git worktree, grade it PASS/FAIL with an independent reviewer running the real test suite, and open a PR only on PASS.
---

# Fix Loop (worktree isolation + maker-checker)

Use this for a single, well-scoped bug: one implementer drafts a fix in
its own checkout, one reviewer grades it using a real command — never
the implementer's own opinion.

## Procedure

1. **Isolate:** create a new git worktree on a new branch for the fix
   attempt, so the fix never touches the main working tree until it's
   proven correct.
   ```bash
   git worktree add .worktrees/<name> -b fix/<slug>
   ```
2. **Implementer (maker):** edit the buggy file inside that worktree
   only. Make a targeted change based on what the failing test actually
   says, not a guess.
3. **Reviewer (checker):** run `reviewer.py <worktree>/sample_repo`. It
   runs the real test suite (`python3 -m unittest test_inventory -v`)
   and reports PASS/FAIL from the actual exit code, plus the real
   failure output as reasons — never the agent's self-assessment.
4. **On PASS:** commit inside the worktree, push the branch, open a PR.
5. **On FAIL:** do not open a PR. Read the reviewer's reasons, fix
   again, or discard the attempt (remove the worktree + branch) if it
   was only a test of the reviewer's strictness.
6. **Sanity check the reviewer itself:** deliberately plant a bad fix
   once. If the reviewer PASSes it, the checker is too soft — tighten
   it (e.g. it might be checking the wrong file, or not actually
   running the tests).

## Files
- `sample_repo/inventory.py` — target with the real bug.
- `sample_repo/test_inventory.py` — tests, 1 of 4 fails on the bug.
- `reviewer.py` — the reviewer agent (real exit code, real reasons).
- `run_log.md` — actual PASS and FAIL runs from this project.

## This project's actual result
Good fix (`/` → `//`): reviewer said **PASS**, all 4 tests green.
Deliberately bad fix (`// + 1`): reviewer said **FAIL**, with 2 real
assertion failures printed as reasons. The bad attempt was never pushed
or PR'd — proof the checker is not "soft."
