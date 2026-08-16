---
name: your-own-daily-loop
description: Capstone daily lint-sweep loop for Loop_Engineering_Projects — real cron heartbeat, worktree isolation, pyflakes maker-checker, PR connector, and a progress.md spine, running unattended for 7 days.
---

# Your Own Daily Loop (Capstone)

## Task (verbatim from course)

**Build.** Pick one real, boring, recurring chore in a project you
actually work on: a dependency audit, a docs-freshness check, a
changelog draft, a lint sweep. Build the full loop: heartbeat, worktree,
skill, maker-checker, connector, and the spine. Add budget guards. Let
it run.

**Done when** it has run unattended for a week and you trust what it
ships because you read it, not because you stopped reading. Then answer
Concept 15 honestly: did your understanding of the project keep up with
what the loop changed? If not, slow the loop down until it does. (When
it fails overnight, and it will, work through "When an unattended loop
fails" before you blame the model.)

## The chore

Daily `pyflakes` lint sweep of every `.py` file in this repo — real,
boring, recurring, genuinely useful (this repo gains new Python files
every session).

## All six parts, real implementation

1. **Heartbeat** — `CronCreate`, cron `17 9 * * *`, recurring, real job ID
   `ac5cede1`. Auto-expires after 7 days by the scheduler's own design.
2. **Worktree** — `daily_lint_sweep.py` creates `.worktrees/lint-sweep-<tag>`
   per firing with retry-with-backoff (same pattern as Project 5), does
   all work there, force-removes it in a `finally` block.
3. **Skill** — this file.
4. **Maker-checker** — maker: `pyflakes` finds issues, script auto-fixes
   only `F541` (f-string missing placeholder). Checker: `pyflakes` re-run
   on the fixed worktree; PASS requires every touched line confirmed clean
   in fresh output — a real independent re-check, not self-judgment.
5. **Connector** — `gh pr create` on a real PASS with a real diff.
   Merging is intentionally NOT automated (see Budget guards).
6. **Spine** — `progress.md`, one dated entry per firing regardless of
   outcome.

## Budget guards

- Auto-fix capped at 5 issues/firing — over that, skip auto-fix entirely
  and log `NEEDS HUMAN` instead of a wide unreviewed change.
- Auto-fix scope capped to exactly one safe, mechanical issue class
  (`F541`); everything else pyflakes finds is reported, never touched.
- No auto-merge — PRs are opened, never merged, by the loop. This was an
  explicit ask-first moment: the first cron-scheduling attempt included
  auto-merge and was denied by Claude Code's own auto-mode classifier as
  too autonomous for a 7-day unattended job; asked the user, who chose to
  remove auto-merge rather than approve it.
- 7-day hard stop, built into the scheduling primitive itself.

## Real verification before scheduling

Ran the loop body manually twice before trusting the cron heartbeat:

1. Real bug present (`morning_brief.py:99`, f-string with no placeholder)
   → real PR #3 opened, diffed, reviewed, merged.
2. Same command again → `Clean sweep — 0 issues found across 16 .py
   file(s). No PR needed.` — confirms idempotency, same spine-memory
   principle as Project 3.

A real bug was also found and fixed *in this loop's own code* during
verification (an overly-broad `.worktrees` exclusion filter that
accidentally excluded every file inside the worktree itself, since the
worktree lives under `.worktrees/`) — caught because Firing 1's file
count (0) didn't match the known 16 real `.py` files in the repo.

Full evidence: `../../run_log.md`. Live results as the week progresses:
`../../progress.md`.

## Known limitation

`CronCreate` jobs are session-only (not written to disk). If this Claude
Code session ends before 7 days pass, the heartbeat stops with it —
disclosed in `README.md` and `run_log.md` rather than hidden.
