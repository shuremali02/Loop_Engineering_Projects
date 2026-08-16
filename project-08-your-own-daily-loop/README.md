# Project 8 — Your Own Daily Loop (Capstone)

**Difficulty:** Capstone
**Concepts used:** All six parts

## Task (verbatim from course)
Build. Pick one real, boring, recurring chore in a project you actually
work on: a dependency audit, a docs-freshness check, a changelog draft, a
lint sweep. Build the full loop: heartbeat, worktree, skill,
maker-checker, connector, and the spine. Add budget guards. Let it run.

Done when it has run unattended for a week and you trust what it ships
because you read it, not because you stopped reading. Then answer Concept
15 honestly: did your understanding of the project keep up with what the
loop changed? If not, slow the loop down until it does. (When it fails
overnight, and it will, work through "When an unattended loop fails"
before you blame the model.)

## Status
🔄 In progress — infrastructure built, verified with a real firing, and a
real 7-day cron heartbeat is now running. The "unattended for a week"
bar needs real elapsed time; see `run_log.md` for what's confirmed so
far and what's still pending.

## The chore

**Daily lint sweep** of this repo's own `.py` files with `pyflakes` — real,
boring, recurring, and useful for a project that keeps growing new Python
files every session (16 of them as of Project 8).

## The six loop parts

| Part | Implementation |
|---|---|
| **Heartbeat** | A real `CronCreate` job (`17 9 * * *`, recurring), firing once daily. It auto-expires after exactly 7 days — which is also this project's "Done when" bar. |
| **Worktree** | Every firing creates a fresh, isolated `git worktree` under `.worktrees/lint-sweep-<timestamp>`, does all its work there, and is force-removed in a `finally` block — the main checkout is never touched directly. |
| **Skill** | `.claude/skills/your-own-daily-loop/SKILL.md` documents the exact procedure. |
| **Maker-checker** | Maker: `pyflakes` finds issues; the script auto-fixes only one safe, mechanical class (`F541` f-string-without-placeholder) by stripping the `f` prefix. Checker: `pyflakes` is re-run on the fixed worktree, and PASS requires every touched line to be confirmed clean in *fresh* output — not self-judgment, a real independent re-check. |
| **Connector** | On a real PASS with a real diff, opens a real PR via `gh pr create`. Merging is **not** automated — that's a deliberate human-in-the-loop boundary (see Budget guards). |
| **Spine** | `progress.md` gets one dated entry every single firing — clean, pass, fail, or needs-human — so the whole week's history is readable without replaying anything. |

## Budget guards

- **Auto-fix cap:** at most 5 issues auto-fixed per firing. Above that, the
  run skips auto-fixing entirely and logs `NEEDS HUMAN` rather than taking
  a wide, unreviewed action across many files at once.
- **Scope cap:** only `F541` (f-string missing a placeholder) is ever
  auto-fixed. Every other pyflakes finding (unused imports, undefined
  names, etc.) is reported but never touched automatically.
- **No auto-merge:** the loop opens PRs but never merges them — merging is
  a human decision. (This was also an explicit ask-first moment: my first
  attempt to schedule the cron job with auto-merge included was blocked by
  Claude Code's own auto-mode classifier as too autonomous for a 7-day
  unattended action; the user chose to remove auto-merge rather than
  approve it.)
- **7-day hard stop:** the cron heartbeat auto-expires after 7 days by the
  scheduler's own design — no manual cutoff needed.
- **Cost:** the maker/checker steps are deterministic (`pyflakes`, `git`,
  `gh`) with no LLM call inside them — real $0 marginal cost per firing
  beyond the orchestrating agent turn that runs the script (same honest
  accounting approach as Project 7).

## Known limitation — session-only cron

`CronCreate` jobs are session-only: "not written to disk, dies when Claude
exits." If this Claude Code session ends before the 7 days are up, the
heartbeat stops with it. This is disclosed here rather than hidden — see
`run_log.md` for how this is being tracked.
