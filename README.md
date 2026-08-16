# Loop Engineering Projects

Hands-on work for the [Loop Engineering crash course](https://agentfactory.panaversity.org/docs/loop-engineering-crash-course) — 12 real, working loops built one at a time, in order, with real files, real commands, and real GitHub activity (no simulated steps).

See **[PROJECTS.md](./PROJECTS.md)** for the full verbatim task list and the live progress-status table.

## What's here

| # | Project | Heartbeat / Concept | Status |
|---|---------|---------------------|--------|
| 1 | [watch-loop](./project-1-watch-loop) | In-session (Concept 4) | ✅ |
| 2 | [tests-pass](./project-2-tests-pass) | Conditional (Concept 5) | ✅ |
| 3 | [morning-brief](./project-3-morning-brief) | Scheduled (Concept 6) | ✅ |
| 4 | [fix-loop](./project-4-fix-loop) | Worktree + maker-checker | ✅ — real [PR #1](https://github.com/shuremali02/Loop_Engineering_Projects/pull/1) |
| 5 | [codify-body](./project-5-codify-body) | Dynamic workflows | ✅ |
| 6 | [doorbell-loop](./project-6-doorbell-loop) | Event-driven (Concept 7) | ✅ — real [PR #2](https://github.com/shuremali02/Loop_Engineering_Projects/pull/2) |
| 7 | [break-it-on-purpose](./project-7-break-it-on-purpose) | Cost + observability | ✅ |
| 8 | [your-own-daily-loop](./project-8-your-own-daily-loop) | Capstone — all six parts | 🔄 running (real 7-day cron heartbeat) |
| 9 | [rehearse-a-routine](./project-9-rehearse-a-routine) | Claude Code cloud Routine | ⏳ |
| 10 | [secrets-drill](./project-10-secrets-drill) | Routine environment variables | ⏳ |
| 11 | [two-routine-gate](./project-11-two-routine-gate) | Two-routine human gate | ⏳ |
| 12 | [dreaming-loop](./project-12-dreaming-loop) | Second capstone | ⏳ |

Each project folder has its own `README.md` (verbatim task + real results) and `.claude/skills/<slug>/SKILL.md` (real procedure, once implemented).

## Loop anatomy (six parts, used throughout)

Heartbeat · Worktree · Skill · Maker-checker · Connector · Spine

Projects 1-8 cover all four heartbeats (in-session, conditional, scheduled, event-driven) plus worktree isolation, maker-checker review, real GitHub connectors, and spine-backed memory across runs. Projects 9-12 go further into the platform-specific Routines product: rehearsing safely, secrets handling, the two-routine human-approval gate, and a self-improving "dreaming" loop that reads its own history.
