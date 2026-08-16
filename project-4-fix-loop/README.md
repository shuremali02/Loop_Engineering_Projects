# Project 4 — Fix Loop

**Difficulty:** Medium to hard
**Concepts used:** Concept 8 (worktree), Concept 9 (skill), Concept 11 (maker-checker)

## Task (verbatim from course)
Build. A smaller version of the Part 5 loop. Write a short skill with your
fix steps, and a reviewer agent that replies PASS or FAIL. Take one real
bug, have the implementer draft a fix in its own checkout (worktree or
branch), and let the reviewer grade it. Open a PR only on PASS.

Done when two things are both true: a good fix gets a PASS and a PR, and a
deliberately bad fix you plant gets a FAIL with reasons. If the reviewer
passes the bad fix, your checker is too soft, so tighten it. A checker
that approves everything is no checker.

## How this was implemented
- `sample_repo/inventory.py` — one real bug: `days_of_stock_left` used
  `/` instead of `//`, returning fractional days.
- `sample_repo/test_inventory.py` — 4 unittest cases; 1 fails on the
  buggy version.
- `reviewer.py` — the reviewer agent. Runs the real test command in a
  given worktree path and returns PASS/FAIL based on the actual exit
  code, printing the real failure output as the reasons.
- **Good fix:** worktree `.worktrees/fix-good` on branch
  `fix/days-of-stock-off-by-one`, implementer changed `/` to `//`.
  Reviewer verdict: **PASS**.
- **Bad fix (planted):** worktree `.worktrees/fix-bad` on branch
  `fix/days-of-stock-bad-attempt`, implementer changed the logic to
  `current_stock // daily_usage + 1` (a plausible-looking but wrong
  fix). Reviewer verdict: **FAIL**, with the exact assertion failures
  as reasons. Worktree/branch removed after grading — it was never
  meant to be pushed.
- See `run_log.md` for the full real output of both reviews.

### Opening the PR (good fix)
```bash
cd .worktrees/fix-good
git push -u origin fix/days-of-stock-off-by-one
gh pr create --title "Fix off-by-one in days_of_stock_left" \
  --body "Reviewer verdict: PASS. See project-4-fix-loop/run_log.md."
```

## Status
Implemented and verified. Both reviewer verdicts (PASS on the good fix,
FAIL with reasons on the planted bad fix) confirmed with real test runs.
Real PR opened for the good fix:
https://github.com/shuremali02/Loop_Engineering_Projects/pull/1
