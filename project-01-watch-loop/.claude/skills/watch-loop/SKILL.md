---
name: watch-loop
description: Start a long-running background task and poll for its completion on a fixed interval, reporting exactly once when it finishes, without blocking the terminal or requiring the user to watch it.
---

# Watch Loop

Use this skill whenever a task takes longer than a single turn (a build,
a sleep-then-write script, a long download) and the user should not have
to sit and stare at the terminal until it's done.

## Procedure

1. **Start the task in the background**, not in the foreground.
   - `nohup bash long_task.sh > run.out 2>&1 & disown`
   - The task should end by writing an unambiguous completion marker file
     (`task_done.txt`) plus a human-readable log (`task.log` with
     "Task started at ..." / "Task finished at ..." lines). Do not rely on
     parsing partial log output — the marker file is what gates the loop.

2. **Register a real recurring cron job** (`* * * * *`, every minute) —
   not just a session-local wakeup — so the check survives independent of
   the current turn.
   - Each fire: check whether `task_done.txt` exists.
   - If it does not exist yet: print nothing, end the tick silently
     (a `noop` poll).
   - If it exists: read `task.log`, tell the user **once** that the task
     finished (show the started/finished lines), state the done-criteria
     are met, then call `CronList` to find this job's id and `CronDelete`
     it — stopping the loop cleanly with no leftover job and no duplicate
     reports on later ticks.

3. **Never poll synchronously.** Do not `sleep 60` in a foreground Bash
   call and block the conversation — that defeats the point (the user
   would be back to watching a terminal, just yours instead of theirs).
   Use `CronCreate`/`CronDelete` so the user is free to do other things
   between checks.

## Files in this project
- `long_task.sh` — the simulated long task (`DURATION` seconds, default
  180; writes `task.log`, then `task_done.txt`).
- `run.out` — captured stdout/stderr of the backgrounded task launch.
- `task.log` — "Task started at ..." / "Task finished at ..." timestamps.
- `task_done.txt` — completion marker; its existence is the only thing the
  loop checks. Delete it before re-running the demo.

## Done-when checklist
- [x] Loop notices the task finished (checked the marker file)
- [x] Says so exactly once (not once per tick)
- [x] Stops itself cleanly (no dangling scheduled wakeups)
- [x] User never had to watch the terminal between start and finish
