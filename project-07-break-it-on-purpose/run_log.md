# Project 7 — Run Log (real results)

## Part 1 — Measure one beat (Concept 13's math)

The loop's worker (`loop_runner.py`, taken from Project 3's `morning_brief.py`)
is a deterministic Python script — it has no LLM call inside it, so the
script itself costs $0 in tokens. That's a real, valid finding on its own.

But the intended shape of this loop (and the one Concept 13 asks us to cost)
is an **agent-orchestrated** firing: something wakes up on a schedule, reads
the spine + repo, runs the check, and reports — the same shape as every
other project in this course. Costed honestly with real measured inputs:

**Real measured data per beat** (steady-state run, `sample_repo` unchanged):

| Item | Size |
|---|---|
| `progress.md` read | 759 chars |
| `sample_repo/app.py` read | 408 chars |
| `sample_repo/utils.py` read | 203 chars |
| Appended run entry (output) | 63 chars |
| **Total data payload** | **1,370 in / 63 out chars** |

Converted to tokens using the documented ~4 chars/token English-text ballpark
(no `ant messages count-tokens` available in this environment, and `tiktoken`
is the wrong tokenizer for Claude — see the `claude-api` skill's Token
Counting section): ≈ 343 input tokens / 16 output tokens for the raw data
alone.

**Realistic agent-firing overhead.** A real scheduled agent invocation also
carries a system-prompt fragment, tool-call framing (Read/Bash calls), and a
short "here's what I found" summary — none of which is captured by the raw
file sizes above. Estimated at a conservative ~1,500 input tokens / ~250
output tokens per firing (data payload + orchestration overhead), rounded up
deliberately since underestimating cost is the failure mode that matters.

**Pricing** (from the `claude-api` skill, Claude Sonnet 5, intro pricing
through 2026-08-31 — today is 2026-08-17, so intro pricing applies):
$2.00 / 1M input tokens, $10.00 / 1M output tokens.

```
cost per beat  = (1500 / 1,000,000) * $2.00 + (250 / 1,000,000) * $10.00
               = $0.0030 + $0.0025
               = $0.0055
```

**Cadence.** Project 3 is a "morning brief" — daily cadence, once per day.

```
monthly cost = $0.0055 * 30 = $0.165 / month
```

**Result: this loop costs roughly $0.17/month at its current daily cadence.**
Cheap even as a rough overestimate — the real number is almost certainly
lower, since the worker does no LLM reasoning at all.

## Part 2 — Sabotage and rehearse the overnight failure

**Setup:** `sample_repo/` renamed to `sample_repo_MOVED` (simulates a repo
that moved, got deleted, or the mount path went stale — a realistic
overnight failure, not a contrived one).

### Before the fix — silent failure (real, observed)

```
$ python3 loop_runner.py
[loop-runner] Scanned 0 TODO(s) total.
[loop-runner] 0 new since last run.
[2026-08-17 01:20] scanned=0 new=0
```

`Path.rglob()` on a missing directory returns an empty iterator instead of
raising — confirmed directly in this environment before writing the fix (see
below). The loop reported "0 new TODOs" and appended "No new TODOs found —
same as last run." to `progress.md`. **From the spine alone
(`run_log_entries.txt` + `progress.md`), this run is indistinguishable from
a legitimately clean repo.** You cannot say what failed, or that anything
failed at all — the loop failed silently. This is exactly the risk the
project asks us to catch before it happens overnight and unwatched.

```python
>>> from pathlib import Path
>>> p = Path('.../nonexistent_repo')
>>> p.exists()
False
>>> list(p.rglob('*.py'))
[]        # no exception — silent empty result
```

### The fix

Added an explicit existence check at the top of `scan_todos()`: if
`sample_repo` doesn't exist, write a `NEEDS HUMAN: ...` line to the log and
exit with a non-zero code — *before* touching `progress.md` at all, so a
broken run can never masquerade as a clean one.

### After the fix — same sabotage, real re-run

```
$ python3 loop_runner.py
[loop-runner] NEEDS HUMAN: sample_repo not found at .../sample_repo — nothing was scanned
$ echo $?
1
```

`run_log_entries.txt`:
```
[2026-08-17 01:20] NEEDS HUMAN: sample_repo not found at .../sample_repo — nothing was scanned
```

`progress.md` unchanged from the prior clean run — no false "clean" entry
written.

### Diagnosis from the spine alone

Reading only `run_log_entries.txt` (the log line) after the fix tells you,
without replaying anything: **what failed** (`sample_repo` missing),
**when** (`2026-08-17 01:20`), and that a human is needed. That's the exact
"Done when" bar: say what failed and when from the spine alone.

### Restore and confirm

`sample_repo` renamed back; re-ran — real exit code 0, correctly scanned 4
TODOs, 0 new (steady state). The fix does not affect the healthy path.

## Result

All three "Done when" conditions met with real evidence:
1. What failed, and when — readable from `run_log_entries.txt` alone.
2. The loop leaves a clear "needs a human" note (`NEEDS HUMAN: ...`, nonzero
   exit) instead of failing silently — verified it *was* silent before the
   fix, then verified the fix closes that gap.
3. Monthly cost at current (daily) cadence: **≈ $0.17/month**, computed from
   real measured file sizes and documented Sonnet 5 pricing.
