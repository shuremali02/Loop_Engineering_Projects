# Project 8 — Run Log (real results, updated as the week progresses)

## Day 1 — 2026-08-17 (manual, pre-schedule verification)

Before trusting the cron heartbeat to run this unattended, ran the loop
body manually twice to prove every part works end to end.

**Firing 1** — real bug present in the repo (`morning_brief.py:99`, an
f-string with no placeholder, found by `/usr/bin/python3 -m pyflakes`):

```
[daily-lint-sweep] PASS — fixed 1 issue(s), reviewer confirmed clean, PR opened: https://github.com/shuremali02/Loop_Engineering_Projects/pull/3
```

- Maker: pyflakes found `F541` at `project-3-morning-brief/morning_brief.py:99`.
- Fix applied: stripped the `f` prefix (`f"[morning-brief] progress.md updated."` → `"[morning-brief] progress.md updated."`).
- Checker: re-ran pyflakes on the fixed worktree — line 99 confirmed clean.
  Real diff: `gh pr diff 3` showed exactly one line changed, nothing else.
- Connector: real PR opened (#3), reviewed the diff, merged
  (`gh pr merge --merge --delete-branch`), `git merge origin/main` synced
  the local checkout.
- Worktree: created at `.worktrees/lint-sweep-<tag>`, force-removed after —
  confirmed via `git worktree list` showing no leftover.

**Firing 2** — same command, right after the merge (idempotency check):

```
[daily-lint-sweep] Clean sweep — 0 issues found across 16 .py file(s). No PR needed.
```

Confirms the loop correctly recognizes "nothing to do" once the real issue
is fixed — same spine-memory principle as Project 3.

**Bug found and fixed during this verification (documented, not hidden):**
the first draft of `py_files()` excluded any path containing `.worktrees`
in its parts — but the worktree itself lives *under* `.worktrees/`, so
every file inside it matched the exclusion and 0 files were ever scanned.
First real run showed `0 issues found across 0 .py file(s)` — caught
immediately because the count didn't match the known 16 real `.py` files
in the repo. Fixed by dropping the unnecessary `.worktrees` check (it's
gitignored, so it's never checked out inside a worktree anyway) and
re-verified with Firing 1 above.

## Heartbeat scheduled

Real `CronCreate` job, ID `ac5cede1`, cron `17 9 * * *` (9:17 AM daily,
deliberately off the :00/:30 mark), `recurring: true`. Auto-expires after
7 days per the scheduler's own design.

**First attempt was blocked.** The cron prompt originally included
auto-merging any PR the script opened. Claude Code's auto-mode classifier
denied that call — a 7-day unattended job that both opens *and* merges PRs
without a human in the loop was judged too autonomous to allow silently.
Asked the user how to proceed (AskUserQuestion); they chose to remove
auto-merge rather than approve the riskier version. The cron job now opens
PRs but never merges them — merging stays a manual, human step. This is
itself a real budget guard, not just a workaround, and it's documented as
one in `README.md`.

## Known limitation, disclosed up front

`CronCreate` jobs are **session-only** — they live in this Claude Code
session's memory, not on disk, and die if the session ends before 7 days
pass. This is a real constraint of the scheduling primitive available in
this environment, not a design choice. If this session ends early, the
honest record of what actually happened (as opposed to what was
*supposed* to happen) is this file plus `progress.md` — both will simply
stop gaining new entries, which is itself diagnosable from the spine,
same as Project 7 taught.

## Remaining days

This section will be updated as real firings land in `progress.md` over
the coming week — each day's entry summarized here with a link back to
the spine, plus a final check-in on Concept 15 (did understanding of the
repo keep up with what the loop changed?) once a full week of real data
exists.
