# Project 1 — Watch Loop

**Difficulty:** Easy
**Concept used:** Concept 4 — In-session loop

## Task (verbatim from course)
Build: Start a long task in your repo (for example, a script that sleeps for
a while and then writes a file). Set up an in-session loop that checks every
minute whether the task has finished, and tells you the moment it has.

Done when: the loop notices the task finished, says so once, and you can
stop it cleanly, and you never sat watching the terminal.

## How this was implemented
- `long_task.sh` — takes `DURATION` (default 180s), writes `Task started at
  <ISO8601>` to `task.log`, sleeps, writes `Task finished at <ISO8601>` to
  `task.log`, then writes `done` to `task_done.txt` as the completion marker.
- `run.out` — captures stdout/stderr of the background-launched task.
- The task is launched in the background:
  `nohup bash long_task.sh > run.out 2>&1 & disown`
- A real recurring cron job (`* * * * *`, every minute) polls for
  `task_done.txt`:
  - Not found yet → silent no-op tick, nothing printed.
  - Found → reads `task.log`, reports **once**, then calls `CronDelete` on
    itself to stop the loop cleanly. No duplicate messages, no leftover job.

This matches the "Done when" criteria exactly: the loop notices completion,
says so once, stops itself, and the user never had to watch the terminal.
