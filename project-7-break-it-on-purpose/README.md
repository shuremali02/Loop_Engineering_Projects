# Project 7 — Break It On Purpose

**Difficulty:** Medium
**Concepts used:** Observability, Concept 13 (cost), Concept 14

## Task (verbatim from course)
Build. Take your Project 3 loop. First, measure one beat: note roughly how
many tokens a run reads and writes, and multiply by your cadence to get a
monthly cost, which is Concept 13's math on your own loop. Then sabotage
it: point the prompt at a file that does not exist, or give it a success
condition it can never meet (with a limit set). Let it fire on schedule
and fail. Now diagnose the failure using only what the loop left behind,
meaning the log line and progress.md, without replaying the full run.

Done when three things are true. You can say what failed, and when, from
the spine alone. The loop left a clear "needs a human" note instead of
failing silently. And you know your loop's monthly cost at its current
cadence. If it failed silently, fix that before anything else by adding
the log line. You are rehearsing the overnight failure now, while it is
cheap and you are watching.

## Status
Not yet implemented — scaffold only. Depends on Project 3 being built
first (this project deliberately breaks it).
