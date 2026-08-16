# Project 2 — Tests Pass

**Difficulty:** Easy to medium
**Concepts used:** Concept 5 (conditional loop), Concept 11 (maker-checker)

## Task (verbatim from course)
Build. Put 2 or 3 small failing tests in your repo. Build a loop that keeps
working until the tests pass, but let a command (the test runner), not the
agent, decide when it is done. Cap it at, say, 6 tries.

Done when the loop stops because the tests actually passed, not because it
hit the cap. If it keeps hitting the cap, your stop condition or your
prompt needs work. That is the lesson.

## How this was implemented
- `calc.py` — small module with real, deliberate bugs.
- `test_calc.py` — 3 tests that fail against the buggy module.
- The stop condition is `pytest`'s own exit code — 0 means done. The agent
  (maker) never gets to declare victory on its own opinion; the checker is
  a command, not a self-assessment.
- Loop is capped at 6 attempts. See `.claude/skills/tests-pass/SKILL.md`
  for the exact maker/checker procedure and the run log.
