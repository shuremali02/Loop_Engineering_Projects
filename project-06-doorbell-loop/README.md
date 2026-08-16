# Project 6 — The Doorbell

**Difficulty:** Medium
**Concepts used:** Concept 7 (event-driven), Concept 10 (connectors)

## Task (verbatim from course)
Build. Make your throwaway repo review its own pull requests. On the
OpenCode approach, run `opencode github install` and accept the workflow
it generates. On the Claude Code approach, create a Routine with a
GitHub pull-request trigger (the appendix walks through the filters).
Then open a PR that contains one planted bug, such as an off-by-one or a
deleted null check, and wait.

Done when the PR gets a review you never asked for, and the review flags
the planted bug. If the review misses it, tighten the prompt and push
again. The push fires the loop once more through the synchronize event,
and that re-fire is the event heartbeat working. With Projects 1 to 3,
this completes all four heartbeats: in-session, conditional, scheduled,
and event-driven.

## Status
✅ Implemented & verified — real GitHub Actions workflow, real PR, real
review comments. See `run_log.md` for full evidence.

## Implementation

Claude Code Routines need a repo `environment_id` provisioned through the
claude.ai Settings UI (no tool in this session can do that step, confirmed
by a real API error), so this project uses a native **GitHub Actions**
workflow instead as the event-driven connector — a deliberate, disclosed
trade-off: deterministic AST-based review instead of an LLM reviewer.

- `.github/workflows/pr-review.yml` — triggers on `pull_request: [opened,
  synchronize]`.
- `review_pr.py` — scans changed `.py` files with Python's `ast` module for
  one real bug class: a `None`-default parameter used in arithmetic with no
  `is None` guard. Posts the finding as a real PR comment via
  `gh pr comment`, using the auto-provided `GITHUB_TOKEN` (no extra secrets
  needed).

## Real run

PR #2 (https://github.com/shuremali02/Loop_Engineering_Projects/pull/2)
planted two such bugs in `sample_repo/shipping.py`. The workflow fired
unprompted on `opened`, flagged both bugs by file/line/reason. A follow-up
push (fixing the bugs) re-fired the workflow via `synchronize`, and the
second review correctly reported clean. PR merged. Full log in
`run_log.md`.
