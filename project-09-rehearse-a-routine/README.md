# Project 9 — Rehearse a Routine for Free

**Difficulty:** Easy (20-30 min)
**Concepts used:** A1, A3 (one-off schedules), A5 (reading runs)

## Task (verbatim from course)
Build. In a throwaway repo, create a routine whose prompt does one small,
checkable thing, for example summarizing yesterday's commits onto a
`claude/summary` branch. Do not put it on a repeating schedule. Fire it
with a one-off run (`/schedule tomorrow at 9am, …` or *Run now*) and read
the full transcript, not the status column. Then change the prompt so the
task must fail, by having it read a file that does not exist, and fire it
once more.

Done when you have seen two green runs: one whose transcript shows
success, and one whose transcript shows failure. You should be able to
say, in one sentence, why the status column could not tell them apart.
That sentence is the A5 lesson: green means the session ended without an
infrastructure error, nothing more.

## Status
Not yet implemented — scaffold only. Needs a real Claude Code cloud
Routine (`claude.ai/code/routines`) — a different product surface than
the CronCreate scheduler used in Projects 1 and 8.
