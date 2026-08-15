# Run log — Project 3 (morning-brief)

Spine file: `progress.md`. Target: `sample_repo/` (stands in for "the repo").
Checker of "did the spine work": second run must not repeat findings from
the first run.

## Run 1 — 2026-08-16 01:18
`sample_repo/` had 3 TODO comments, `progress.md` did not exist yet.

```
[morning-brief] Scanned 3 TODO(s) total.
[morning-brief] 3 new since last run:
  - app.py:2: TODO: validate user_id before querying the database
  - app.py:7: TODO: add retry logic if the SMTP server times out
  - utils.py:6: TODO: handle missing config file gracefully instead of crashing
[morning-brief] progress.md updated.
```
Result: `progress.md` created with a "Recorded TODOs" section (3 items) and
a Run history entry for this run.

## Simulated day 2
Added one new TODO to `sample_repo/app.py` (`# TODO: apply discount codes
before summing the total`) to simulate a day passing with one real code
change. The 3 original TODOs were left untouched.

## Run 2 — 2026-08-16 01:18
```
[morning-brief] Scanned 4 TODO(s) total.
[morning-brief] 1 new since last run:
  - app.py:12: TODO: apply discount codes before summing the total
[morning-brief] progress.md updated.
```
Result: even though 4 TODOs existed in the repo, the run reported **only
the 1 new one** — the 3 from Run 1 were recognized as already recorded
and were not repeated in the "new" list. `progress.md`'s "Recorded TODOs"
section grew to 4, and a second Run history entry was appended below the
first (history is never overwritten).

## Conclusion
The second run clearly built on the first: it did not repeat what was
already recorded, because it read `progress.md` before scanning and
compared against it. This is the spine (Concept 12) working as intended.
If Run 2 had reported all 4 as "new," the loop would have had no memory
— that did not happen here.
