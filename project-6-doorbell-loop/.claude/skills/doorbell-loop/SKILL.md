---
name: doorbell-loop
description: Event-driven PR review connector for project-6-doorbell-loop — a GitHub Actions workflow that reviews every PR unprompted and re-fires on push, proving the event heartbeat (Concept 7 + Concept 10).
---

# Doorbell Loop

## Task (verbatim from course)

**Build.** Make your throwaway repo review its own pull requests. On the
OpenCode approach, run `opencode github install` and accept the workflow
it generates. On the Claude Code approach, create a Routine with a
GitHub pull-request trigger (the appendix walks through the filters).
Then open a PR that contains one planted bug, such as an off-by-one or a
deleted null check, and wait.

**Done when** the PR gets a review you never asked for, and the review
flags the planted bug. If the review misses it, tighten the prompt and
push again. The push fires the loop once more through the `synchronize`
event, and that re-fire is the event heartbeat working. With Projects 1
to 3, this completes all four heartbeats: in-session, conditional,
scheduled, and event-driven.

## Why not a Claude Code Routine

Creating a Routine via the API requires a repo `environment_id`, which is
only provisioned by connecting the repo through the claude.ai Settings UI
— confirmed by a real `RemoteTrigger create` call returning HTTP 400
(`job_config must set ccr.environment_id`). No tool in this session can do
that UI step, and the account constraint for this project (`shuremali02`
only, never switching to another GitHub account) ruled out the one repo
where a working Routine already existed. So the event-driven connector was
built as a native **GitHub Actions** workflow instead — same trigger
semantics (`pull_request: opened` / `synchronize`), deterministic
AST-based review instead of an LLM reviewer. This trade-off was surfaced
to the user before building.

## Procedure

1. `.github/workflows/pr-review.yml` triggers on
   `pull_request: [opened, synchronize]`, checks out the PR, and runs
   `project-6-doorbell-loop/review_pr.py` with `GITHUB_TOKEN`,
   `PR_NUMBER`, `BASE_SHA`, `HEAD_SHA` as env vars. No extra secrets
   needed — `GITHUB_TOKEN` is auto-provided by Actions and scoped with
   `pull-requests: write` in the workflow's `permissions:` block.
2. `review_pr.py`:
   - `git diff --name-only base...head` to get changed `.py` files.
   - Parses each with `ast.parse`, walks every `FunctionDef`.
   - For each parameter defaulting to `None`, checks the whole function
     body for an `is None` / `is not None` guard on that name
     (`is_guarded`), and whether it's used directly in an `ast.BinOp`
     (`used_unsafely`).
   - Flags file/line/function/param when used unsafely with no guard.
   - Posts the result — bug list or "no issues" — as a real PR comment
     via `gh pr comment "$PR_NUMBER" --body "..."`.
   - Exits 1 if findings exist, 0 otherwise (this makes the Action run
     show red/green in the PR checks list, on top of the comment).

## Real run (PR #2)

1. Branch `feature/shipping-calculator` added `sample_repo/shipping.py`
   with two planted bugs: `calculate_shipping_cost(weight, discount=None)`
   and `apply_bulk_rate(item_count, rate=None)`, both using the `None`
   default directly in arithmetic with no guard.
2. Opened PR #2. Workflow fired on `opened` (run #31969734448, 13s,
   `failure` exit as expected — that's the "bugs found" signal). Real PR
   comment posted, unprompted, correctly flagging both bugs by exact
   file/line/function/param, with the concrete `TypeError` explained.
3. Pushed a fix commit (added `if x is None: x = <default>` guards) to
   the same branch. Workflow re-fired automatically on `synchronize` (run
   #31969784600, 9s, `success`) — this is the event heartbeat: no manual
   re-trigger, the push alone caused the second review.
4. Second comment: "No correctness issues found by the automated
   checker." PR merged (`gh pr merge --merge --delete-branch`).

Full evidence: `../../run_log.md`.

## Result

Both "Done when" conditions verified:
- PR review fired unprompted and flagged the planted bug with reasons.
- The follow-up push re-fired review via `synchronize` (event heartbeat).

Completes the four-heartbeat set: in-session (Project 1), conditional
(Project 2), scheduled (Project 3), event-driven (Project 6).
