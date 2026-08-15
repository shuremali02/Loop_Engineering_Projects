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
Not yet implemented — scaffold only. Requires a real GitHub repo (not just
a local folder) to receive PR webhook events.
