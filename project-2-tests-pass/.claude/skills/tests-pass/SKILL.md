---
name: tests-pass
description: Run a maker-checker loop that keeps fixing code and re-running the real test command (not the agent's own judgment) until it exits 0, capped at N tries.
---

# Tests Pass (conditional loop, maker-checker)

Use this when there are 2-3 small failing tests and the goal is to make
them pass — but the thing that decides "done" must be the test runner's
exit code, never the agent's self-assessment.

## Procedure

1. **Checker command:** `python3 -m unittest test_calc -v` (run from this
   folder). Exit code `0` = done. Anything else = not done.
2. **Cap:** 6 tries maximum.
3. Each iteration:
   - Run the checker command.
   - If exit code is `0`: stop immediately, report PASS, do not run again.
   - If exit code is non-zero: read the failure output, make a targeted
     fix to `calc.py` based on what actually failed (not a guess), then
     loop back to step 1.
   - If the cap (6) is reached and it is still failing: stop and report
     that the cap was hit — this is a signal that the stop condition or
     the fix prompt needs work, not a signal to keep trying blindly.
4. **Never let the agent declare victory on its own reading of the code.**
   Only the checker's exit code ends the loop.

## Files
- `calc.py` — the module being fixed.
- `test_calc.py` — 3 unittest cases (`add`, `is_even`, `factorial`).
- `run_log.md` — actual try-by-try log from the last real run.

## This project's actual result
Stopped at **try 2 of 6** — exit code 0 on try 2. Never hit the cap. See
`run_log.md` for the full failure output and the fixes applied per try.
